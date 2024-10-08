from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view



@api_view(["GET"])
def api_schema(request, *args, **kwargs) -> Response:
    main_route = "/api/v1"
    schema = {
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
        "mobile_login": {
            "url": f"{main_route}/mobile/token",
            "method": "POST",
            "description": "Obtain authentication tokens for mobile login."
        },
        "is_authenticated": {
            "url": f"{main_route}/is_authenticated/",
            "method": "GET",
            "description": "Check if the user is authenticated."
        }
    }

    return Response(schema, status=status.HTTP_200_OK)
