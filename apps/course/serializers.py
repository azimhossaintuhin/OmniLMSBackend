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
    category = CategorySerializer()
    instructor = InstructorSerializer(many=True)
    
    class Meta:
        model = Course
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get("request")
        print("request" ,  request.user)
        representation["is_enrolled"] = False
        
        if request and request.user.is_authenticated:
            user = request.user
            print(request.user)
            course = instance
            enrollment =  Enrollment.objects.filter(user=user, course=course)
            if enrollment.exists():
                representation["is_enrolled"] = True
        
        return representation




#  ========== Lession Serializer ======== #

class LessionSerializer(ModelSerializer):
    class Meta:
        model = Lession
        fields =  "__all__"
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        print(self.context)
        user = self.context.get('user')
        is_enrolled = self.context.get('is_enrolled', False)

        if not instance.is_free and  not is_enrolled:
            representation.pop('video_link', None)
            representation.pop('video', None)
            
        representation["completed"] = False
        completed_lession =  CompleteLession.objects.filter(lession = instance , user=user)
        if  completed_lession.exists():
            representation["completed"] = True
        
        representation.pop("module")
        return representation


# ======= Module Serializer ======= #
class ModuleSerializer(ModelSerializer):
    class Meta:
        model = Module
        fields = "__all__"

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        lession = Lession.objects.filter(module=instance)
        lession_serializer = LessionSerializer(lession, many=True, context=self.context)
        representation["lession"] = lession_serializer.data 
        return representation


# ========= Review Serializer =========== #
class ReviewSerializer(ModelSerializer):
    user_profile = UserProfileSerializer()

    class Meta:
        model =  Review
        fields =  "__all__"




    
    
