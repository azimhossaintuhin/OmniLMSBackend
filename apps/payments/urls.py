from django.urls import  path
from .views import (
    CuponApiView,
)


urlpatterns = [
     path("cupons/" , CuponApiView.as_view() , name="cupon")
]
