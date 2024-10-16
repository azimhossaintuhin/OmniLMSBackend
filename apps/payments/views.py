from django.shortcuts import render
from constant.Response import SuccessResponse , ErrorResponse 
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.utils import timezone
from .models import *
from .serializers import (
    CouponSerializer
)



class  CuponApiView(APIView):
    permission_classes=[AllowAny]

    #  Get all the cupon 
    def get(self , request  , *args, **kwargs):
        try:
            cupons =  Coupon.objects.filter(start_date__lte = timezone.now() , end_date__gte = timezone.now() )
            serializer =  CouponSerializer(cupons , many=True)
            if cupons.exists():
                return SuccessResponse("cupons" , serializer.data)
            else:
                return SuccessResponse("message" , "There are no Cupons")
        except Coupon.DoesNotExist:
            return ErrorResponse("No Cupon Exsits")
        


    def post(self, request, *args, **kwargs):
        cupon = request.data.get("cupon")
        course_slug = request.data.get("slug")

        try:
            cupon_query = Coupon.objects.get(cupon=cupon)

            if cupon_query.start_date <= timezone.now() <= cupon_query.end_date:
                course_query = Course.objects.get(slug=course_slug)
                if course_query:
                    discount_amount = course_query.new_price * (cupon_query.discount_parcentige / 100)
                    discounted_price = course_query.new_price - discount_amount
                    
                    return SuccessResponse("cupon_price", discounted_price)
                else:
                    return ErrorResponse("No Course Found")
            else:
                return ErrorResponse("Coupon is not valid at this time.")

        except Coupon.DoesNotExist:
            return ErrorResponse("Please Enter A Valid Coupon Code")
        except Course.DoesNotExist:
            return ErrorResponse("No Course Found")
        except Exception as e:
            return ErrorResponse(str(e))
            
            
        
   
