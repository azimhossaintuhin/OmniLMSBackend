from  django.urls import path
from .views import *

urlpatterns:list= [
     path("token/" , CustomTokenObtainPairView.as_view() , name="token_obtain"),
     path("refresh/token/" , CustomTokenRefreshView.as_view(), name="refresh_view"),
     path("register/" , RegisterApiView.as_view() , name='register_view'),
     path("logout/" , LogoutApiView.as_view() , name="logout"),
     path("forgot-password/" ,ForgotPasswordApiView.as_view() , name="forgot password"),
     path("reset-password/<str:uid>/<str:token>/", ResetPasswordApiView.as_view() , name="reset password" ),
    #  for mobile authentication
     path("mobile/token" , mobileLoginApiView.as_view() , name="mobile_login"),
     path("is_authenticated/" ,AuthenticatedApiView.as_view() , name="is_authenticated"),
    # User Profile Related 
    path('user-profile/' , UserProfileApiView.as_view() , name="user_profile" )

    
 ]
 