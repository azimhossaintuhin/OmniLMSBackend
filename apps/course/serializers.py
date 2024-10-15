from rest_framework.serializers import ModelSerializer
from apps.account.serializers import UserProfileSerializer
from .models import *


# ========== Instructocr serializer ============ #
class InstructorSerializer(ModelSerializer):    
    class Meta:
        model =  Instructor
        fileds = "__all__"




# ======  Category Serializer ======= #
class CategorySerializer(ModelSerializer):
    class Meta:
        model =  Category
        fields = "__all__"


# ======= Course Serializer ======== #
class CourseSerializer(ModelSerializer):
    category  =  CategorySerializer()
    instructor =  InstructorSerializer(many=True)
    class Meta:
        model = Course
        fields =  "__all__"



# ========= Review Serializer =========== #
class ReviewSerializer(ModelSerializer):
    user_profile = UserProfileSerializer()

    class Meta:
        model =  Review
        fields =  "__all__"



    
    