from rest_framework.serializers import ModelSerializer
from .models import Cupon

class CouponSerializer(ModelSerializer):
    class Meta:
        model = Cupon
        exclude_fields = ["specific_course" , "is_for_all"]


