from django.shortcuts import redirect, get_object_or_404
from sslcommerz_lib import SSLCOMMERZ
from rest_framework.views import APIView
from constant.Response import  ErrorResponse
from apps.course.models import Enrollment, Course
from apps.account.models import User
from decouple import config


class SslCommerzSuccess(APIView):

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
                if response.get("status") == "VALID":
                    user = get_object_or_404(User, email=response.get("value_b"))
                    course = get_object_or_404(Course, title=response.get("value_a"))
                    enrollment = Enrollment.objects.filter(payment_id=response.get("tran_id")).first()
                    if enrollment:
                        return ErrorResponse("Transection Id Already  Exsits")
                    else:
                       
                        enrollment = Enrollment.objects.create(
                            user=user,
                            course=course,
                            payment_method=f"ssl_{response.get('card_type')}",
                            payment_id=response.get("tran_id")
                        )
                        enrollment.save()
                       

                    return redirect("http://localhost:5173/payment/success/")
                else:
                    return redirect("http://localhost:5173/")
            
            else:
                return ErrorResponse("Hash Validation Is Failed Or Invalid  Hash")

        except Exception as e:
            return ErrorResponse(str(e))
