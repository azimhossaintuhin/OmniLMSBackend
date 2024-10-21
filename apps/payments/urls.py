from django.urls import  path
from .views import (
    CartApiView,
    CuponApiView,
    PaymentApiView,
 
)
from .gateways.sslcommerz.success import SslCommerzSuccess
from .gateways.sslcommerz.failed import SslCommerzFail


urlpatterns = [
     path("cupons/" , CuponApiView.as_view() , name="cupon"),
     path("cart/" , CartApiView.as_view() , name="cart"),
     path("payment/" ,PaymentApiView.as_view(), name="payment"),
    #  sslcommerz realted routes
     path("sslcz/payment/success/" , SslCommerzSuccess.as_view() , name="sslcz_success"),
     path("sslcz/payment/failed/" , SslCommerzFail.as_view() , name="sslczz_failed")     
]
