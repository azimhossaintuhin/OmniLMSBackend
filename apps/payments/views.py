from django.shortcuts import render
from constant.Response import SuccessResponse , ErrorResponse 
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.utils import timezone
from .models import *
from apps.course.serializers import CourseSerializer
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    CouponSerializer
)
from .gateways.sslcommerz.sslcommzer import SslCommerzPayment

# ====== Cart Api View ======= #
class CartApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self ,request ,*args, **kwargs):
        try:
            cart = Cart.objects.get(user =request.user)
           
            context = {
                     "course_title": cart.course.title ,
                        "course_image": request.build_absolute_uri(cart.course.image.url) ,
                        "course_price": cart.course.new_price,
                        "cupon" : cart.cupon.cupon,
                        "discount_ammount": cart.get_disscout_ammount(),
                        "total_price":cart.total_ammount()
                }
            return SuccessResponse("cart" , context)
    
        except Cart.DoesNotExist:
            return ErrorResponse("Please Select A Course")

    def post(self, request, *args, **kwargs):
        course_slug = request.data.get("slug")
        cupon_code = request.data.get("cupon", "")

        try:
            # Validate that course_slug is provided
            if not course_slug:
                return ErrorResponse("Please select a course")

            # Fetch the course using the provided slug
            course = Course.objects.get(slug=course_slug)

            # Try to fetch the coupon if one is provided
            cupon_used = None
            if cupon_code != "":
                cupon_used = Cupon.objects.get(cupon=cupon_code)

            # Get or create a cart for the current user
            cart, created = Cart.objects.get_or_create(user=request.user)
            # Associate the course with the cart
            cart.course = course
            # If a valid coupon is provided, associate it with the cart
            if cupon_used:
                cart.cupon = cupon_used
            # Save the updated cart
            cart.save()

            # Prepare the response context
            context = {
                "course_title": course.title,
                "course_image": request.build_absolute_uri(course.image.url),
                "course_price": course.new_price,
                "cupon": cart.cupon.cupon if cart.cupon else "",
                "discount_amount": cart.get_disscout_ammount() if cart.cupon else "",
                "total_price": cart.total_ammount(),
            }

            # Return success response with cart details
            return SuccessResponse("cart", context)

        # Handle specific exceptions
        except Course.DoesNotExist:
            return ErrorResponse("Course does not exist")
        except Cupon.DoesNotExist:
            return ErrorResponse("Please provide a valid coupon")
        except Exception as e:
            return ErrorResponse(str(e))

# ========= Cupon Api View ======= #
class  CuponApiView(APIView):
    permission_classes=[AllowAny]

    #  Get all the cupon 
    def get(self , request  , *args, **kwargs):
        try:
            cupons =  Cupon.objects.filter(start_date__lte = timezone.now() , end_date__gte = timezone.now() )
            serializer =  CouponSerializer(cupons , many=True)
            if cupons.exists():
                return SuccessResponse("cupons" , serializer.data)
            else:
                return SuccessResponse("message" , "There are no Cupons")
        except Cupon.DoesNotExist:
            return ErrorResponse("No Cupon Exsits")
        


    def post(self, request, *args, **kwargs):
        cupon = request.data.get("cupon")
        course_slug = request.data.get("slug")

        try:
            cupon_query = Cupon.objects.get(cupon=cupon)

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

        except Cupon.DoesNotExist:
            return ErrorResponse("Please Enter A Valid Coupon Code")
        except Course.DoesNotExist:
            return ErrorResponse("No Course Found")
        except Exception as e:
            return ErrorResponse(str(e))
            
        
# ========= Payment Api View ========= #
class  PaymentApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self,request,*args, **kwargs):
        method =  request.data.get("payment_method")
        try:
            cart = Cart.objects.get(user =  request.user)
            if method == "sslcommerz":
                product_name = cart.course.title 
                amount = cart.total_ammount()
                email = request.user.email  
                phone = request.user.phone if hasattr(request.user, 'phone') else None  

                # Call the SSL Commerz payment function
                payment_url = SslCommerzPayment(product_name=product_name, amount=amount,email=email, phone=phone)
                
                response = SuccessResponse("payment_url",payment_url.get("GatewayPageURL"))
                return response
            return ErrorResponse("Please Select A Payment Gateway")


        except Cart.DoesNotExist:
            return ErrorResponse("Nothing In The Cart")
        except Exception as e:
            return ErrorResponse(str(e))

