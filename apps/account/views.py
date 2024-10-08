from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# ========= Importing utilities ========== #
from constant.Response import SuccessResponse, ErrorResponse
from apps.account.models import Token, User
from constant.email.ForgotPassword import send_forgot_password_email
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes

# ========= Importing serializers ========== #
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer

# ===== Rigiter Api View ======= #
class RegisterApiView(APIView):
    authentication_classes=[]
    def post(self , request ,  *args, **kwargs):
        serializer =  RegisterSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return SuccessResponse("message" , "User Registerd Successfully")
        print(serializer.error_messages)
        return ErrorResponse("something went wrong")



# ======= Custom JWt authentication API View =========== # 
class CustomTokenObtainPairView(TokenObtainPairView):

    serializer_class = CustomTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        tokens = serializer.validated_data
        # Create the response object
        response = SuccessResponse("message", "Login Successfull ")

        # Set the tokens in cookies
        response.set_cookie(
            key='access', 
            value=tokens['access'], 
            httponly=True,  
            secure=True, 
            max_age=1*24*60*60, # Set to True in production (HTTPS only)
            samesite='Lax' , # CSRF protection
         
        )
        response.set_cookie(
            key='refresh', 
            value=tokens['refresh'], 
            httponly=True, 
            secure=True,
            max_age=1*24*60*60,
            samesite='Lax' , # CSRF protection

           
        )

        return response


#  ==== Custom Refresh Token Pair View ======== #
class CustomTokenRefreshView(TokenRefreshView):

    def post(self, request, *args, **kwargs):
        # Retrieve the refresh token from the cookies
        refresh_token = request.COOKIES.get('refresh')
           

        if not refresh_token:
            return ErrorResponse("Refresh token not found")

        # Prepare the data for token refresh
        data = {'refresh': refresh_token}

        # Call the parent class's post method to refresh the tokens
        response = super().post(request, data, *args, **kwargs)
        print( "Custom resposne ",response)

        # Handle successful token refresh
        if response.status_code == status.HTTP_200_OK:
            access_token = response.data.get('access')
            new_refresh_token = response.data.get('refresh')

            # Set the access token in cookies
            response.set_cookie(
                key='access',
                value=access_token,
                httponly=True,  # Makes the cookie inaccessible to JavaScript
                secure=False,   # Set to True if your site is HTTPS
                samesite='Lax', # CSRF protection
                max_age=1*24*60*60  # Token expires in 1 day
            )
            
            # Set the new refresh token in cookies
            response.set_cookie(
                key='refresh',
                value=new_refresh_token,
                httponly=True,
                secure=False,   # Set to True for HTTPS
                samesite='Lax',
                max_age=1*24*60*60  # Refresh token expires in 1 day
            )
        else:
            # If the refresh token is invalid or expired, remove the cookies and send an error
            if response.status_code == status.HTTP_401_UNAUTHORIZED:
                response = ErrorResponse("Token has expired or is invalid.")

                # Remove the access and refresh tokens from cookies
                response.delete_cookie('access')
                response.delete_cookie('refresh')

        

        return response


# ======= Logout Api View ========= #
class LogoutApiView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self , request , *args, **kwargs):
        response =  SuccessResponse("message" , "Logout Successfull")
        response.delete_cookie('access' ,  path='/', samesite='Lax')
        response.delete_cookie("refresh" ,  path='/' ,  samesite='Lax')
        return response


# ======= forgot password ======== #
class ForgotPasswordApiView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        
        # Check if the email is provided
        if not email:
            return ErrorResponse("Please provide your email")

        try:
            user = User.objects.get(email=email)
            token_generator = PasswordResetTokenGenerator()
            user_token = token_generator.make_token(user)
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            
            # Update or create the token
            token, created = Token.objects.update_or_create(user=user, defaults={"token": user_token})
            if created:
                token.save()
            reset_link = f"{request.scheme}://{request.get_host()}/api/v1/reset-password/{uidb64}/{user_token}/"
            
            # Send the reset link via email
            send_forgot_password_email(user, reset_link)

            return SuccessResponse("message","Email sent successfully")

        except User.DoesNotExist:
            return ErrorResponse("User doesn't exist")
        except Exception as e:
            return ErrorResponse(f"An error occurred: {str(e)}")
         

# ========= Reset Password API View =========== #
class ResetPasswordApiView(APIView):
    def post(self, request, *args, **kwargs):
        user_token = kwargs.get("token")
        uid = kwargs.get("uid")

        if not uid or not user_token:
            return ErrorResponse("Invalid URL")

        try:
            uid_decode = urlsafe_base64_decode(uid).decode()
            user = User.objects.get(id=uid_decode)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            return ErrorResponse("Invalid user")

        # Verify token validity
        token_generator = PasswordResetTokenGenerator()
        is_correct_token = token_generator.check_token(user, user_token)

        if not is_correct_token:
            return ErrorResponse("Invalid or expired token")

        # Getting the new password
        password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")

        if not password and not confirm_password:
            return ErrorResponse("Password Can't Be Blank")
        if password != confirm_password :
            return ErrorResponse("Passwords do not match")

        try:
            token = Token.objects.get(token=user_token)
            
            # Check if token is expired
            if token.is_expired():
                print(token.is_expired())
                return ErrorResponse("Token has expired")
            

            # Set the new password
            user.set_password(password)
            user.save()

            # Delete the token after successful password reset
            token.delete()

        except Token.DoesNotExist:
            return ErrorResponse("Token does not exist")

        return SuccessResponse("message","Password updated successfully")



# ======= mobile Login ========= #
class mobileLoginApiView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self,request,*args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens =  serializer.validated_data
        context ={
            "access": tokens["access"],
            "refresh": tokens["refresh"],
            "message": "Login Successfull"
        }
        return SuccessResponse("token",context)


# ====== Authentication Check View =========== #
class AuthenticatedApiView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self,request,*args, **kwargs):
        user =  request.user.username
        return SuccessResponse("user",user )




