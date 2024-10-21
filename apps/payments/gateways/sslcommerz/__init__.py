
from sslcommerz_lib import SSLCOMMERZ
from rest_framework.views import APIView
from rest_framework import status
from constant.Response import ErrorResponse
from apps.account.models import User
from decouple import config
from django.shortcuts import redirect


class SslCommerzFail(APIView):

    def post(self, request, *args, **kwargs):
        payment_info = request.data
        try:
            store = {
                'store_id': config("STOREID"),
                'store_pass': config("STOREPASS"),
                'issandbox': config("SANDBOX", default=True, cast=bool)
            }
            sslcommerz = SSLCOMMERZ(store)

          
            if sslcommerz.hash_validate_ipn(payment_info):
                response = sslcommerz.validationTransactionOrder(payment_info.get("val_id"))

                if response.get("status").upper() == "FAILED":  
                    return redirect("http://localhost:5173/")
                
            return ErrorResponse("Hash Validation Failed")
        except Exception as e:
            return ErrorResponse(str(e))
