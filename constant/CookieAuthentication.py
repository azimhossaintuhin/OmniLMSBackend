from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class CustomJWTAuthentication(JWTAuthentication):
    def get_jwt_from_cookies(self, request):
        token = request.COOKIES.get('access')
  
        return token

    def authenticate(self, request):
        token = self.get_jwt_from_cookies(request)

        if not token:
            header = self.get_header(request)
            if header is None:
                return None  

            token = self.get_raw_token(header)
           
            if token is None:
                return None
        
        try:
            validated_token = self.get_validated_token(token)
        except AuthenticationFailed as e:
          
            raise AuthenticationFailed("Invalid token") from e
        
        return self.get_user(validated_token), validated_token
