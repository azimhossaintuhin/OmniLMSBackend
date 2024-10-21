from django.urls import  path
from .views import (
    CartApiView,
    CuponApiView,
    PaymentApiView,
    PaymentSuccessApiView
)


urlpatterns = [
     path("cupons/" , CuponApiView.as_view() , name="cupon"),
     path("cart/" , CartApiView.as_view() , name="cart"),
     path("payment/" ,PaymentApiView.as_view(), name="payment"),
     path("payment/success/" , PaymentSuccessApiView.as_view() , name="payment success")
     
]
