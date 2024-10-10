from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

@api_view(["GET"])
def api_schema(request, *args, **kwargs) -> Response:
    main_route = "/api/v1"
    schema = {
        "account_urls": {
                "paths": {
                    "register": {
                        "url": f"{main_route}/register/",
                        "method": "POST",
                        "description": "Register a new user."
                    },
                    "login": {
                        "url": f"{main_route}/token/",
                        "method": "POST",
                        "description": "Obtain authentication tokens for a user."
                    },
                    "refresh_token": {
                        "url": f"{main_route}/refresh/token/",
                        "method": "POST",
                        "description": "Refresh the access token."
                    },
                    "logout": {
                        "url": f"{main_route}/logout/",
                        "method": "POST",
                        "description": "Logout the user and invalidate the session."
                    },
                    "forgot_password": {
                        "url": f"{main_route}/forgot-password/",
                        "method": "POST",
                        "description": "Request a password reset link."
                    },
                    "reset_password": {
                        "url": f"{main_route}/reset-password/<str:uid>/<str:token>/",
                        "method": "POST",
                        "description": "Reset the user's password."
                    },
                    "mobile_login": {
                        "url": f"{main_route}/mobile/token/",
                        "method": "POST",
                        "description": "Obtain authentication tokens for mobile login."
                    },
                    "is_authenticated": {
                        "url": f"{main_route}/is_authenticated/",
                        "method": "GET",
                        "description": "Check if the user is authenticated."
                    },
                    "user-profile":{
                        "url": f"{main_route}/user-profile/",
                        "method": "GET",
                        "description": "Get User  Profile  Info."
                    },
                      "user-profile update":{
                        "url": f"{main_route}/user-profile/",
                        "method": "PATCH",
                        "description": "Partial Update  User Profile"
                    }
                }
        
        },

        "course_url":{

        }
    }

    return Response(schema, status=status.HTTP_200_OK)
