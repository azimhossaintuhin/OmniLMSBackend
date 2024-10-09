from rest_framework import serializers
from .models import User , UserProfile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer , TokenRefreshSerializer
from rest_framework.exceptions import ValidationError

# ===== Custom Token serializer
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.email
        
        # Assuming the user model has a profile with an image field
       

        return token


#Register serializer
class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    
    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match.")

        return attrs
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')  # Remove confirm_password from the validated data

        # Ensure the user object is created and returned
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data["password"]  # Hash the password before saving
        )
        return user  # Make sure to return the created user


# custom token refresh  serializer
class CustomTokenRefreshSerializer(TokenRefreshSerializer):

    refresh = serializers.CharField(required=False)  # Set required=False

    def validate(self, attrs):
        # Retrieve the refresh token from cookies
        refresh_token = self.context['request'].COOKIES.get('refresh')
        print("refresh token " , refresh_token)

        
        if not refresh_token:
            refresh_token = attrs.get('refresh')  
            print("from body" , refresh_token)
            if not refresh_token:
                raise ValidationError("Refresh token is required either in cookies or request body.")
      
        # Set the refresh token in the attributes to make it available
        attrs['refresh'] = refresh_token

        # Call the parent class's validate method to continue validation
        return super().validate(attrs)
    


# ========== User Serializer ====== #
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =  ['username' , 'email', 'phone']


# =========== User Profile   ========== # 
class UserProfileSerializer(serializers.ModelSerializer):
    user =  UserSerializer()
    class  Meta:
        model =  UserProfile
        fields = "__all__"


    def update(self,instance,validated_data):
        print("profile update",validated_data)
        print("Data called")
        user_data =  validated_data.pop("user",None)

        if user_data:
            user  =  instance.user
            for attr , value in user_data.items():
                setattr(user , attr , value)
            user.save()
        
        for attr , value in validated_data.items():
            setattr(instance ,  attr , value)
        instance.save()

        return instance




