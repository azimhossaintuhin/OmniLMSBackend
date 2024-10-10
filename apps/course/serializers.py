from rest_framework.serializers import ModelSerializer
from .models import Course , Category


# ======  Category Serializer ======= #
class CategorySeiralizer(ModelSerializer):
    class Meta:
        model =  Category
        fields = "__all__"

class CourseSerializer(ModelSerializer):
    category  =  CategorySeiralizer()
    class Meta:
        model = Course
        fields =  "__all__"

    
    