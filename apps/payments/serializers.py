from rest_framework.serializers import ModelSerializer
from .models import Coupon

class CouponSerializer(ModelSerializer):
    class Meta:
        model = Coupon
        exclude_fields = ["specific_course" , "is_for_all"]


