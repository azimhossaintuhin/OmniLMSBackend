from django.shortcuts import get_object_or_404 
from .models import  *
from rest_framework.permissions import IsAuthenticated ,AllowAny
from constant.Response import SuccessResponse , ErrorResponse
from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework.views import APIView
from .serializers import (
     CategorySerializer , 
     CourseSerializer , 
     ReviewSerializer,
     ModuleSerializer
)



# ========= Category List Api View ============ #
class CategoryListApiView(ListAPIView):
    serializer_class =  CategorySerializer
    queryset =  Category.objects.all()
    permission_classes=[AllowAny]
    authentication_classes = []
 

    def list(self, request, *args, **kwargs):
                try:
                    queryset = self.get_queryset()
                    if not queryset.exists():
                        return ErrorResponse("No categories found.")

                    serializer = self.get_serializer(queryset, many=True)
                    return SuccessResponse("category", serializer.data)
                
                except Exception as e:
                    print(f"Error retrieving categories: {str(e)}")
                    return ErrorResponse("An error occurred while retrieving categories.")


# ============ Course List Api View ========== #
class CourseListApiView(ListAPIView):
      serializer_class = CourseSerializer
      queryset =  Course.objects.all()
      permission_classes = [AllowAny]

    # ====== Overriding the  list ======== #
      def list(self,request ,*args, **kwargs):
            print(request.user)
            try:
                qeuryset = self.get_queryset()
                if not qeuryset.exists():
                      return ErrorResponse("No course found.")
                context =  {
                    "request":request    
                }
                serializer =  self.get_serializer(qeuryset , many=True, context=context)
                return SuccessResponse("course" ,  serializer.data)
            except Exception as e:
                  print(e)
                  return ErrorResponse(str(e))

      
    
# ========== Course  Retrive Api View ============= #
class CourseRetriveApiView(RetrieveAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    lookup_field = 'slug'
    permission_classes = [AllowAny]
    

    def retrieve(self, request, *args, **kwargs):
        try:
            context =  {
                 "request": request
            }
            print(request.user)
            course = self.get_object()
            serializer = self.get_serializer(course , context =context)
            return SuccessResponse("course_details", serializer.data ,)
        
        except Course.DoesNotExist:
            return ErrorResponse("Course not found.")
        except Exception as e:
            return ErrorResponse(str(e))


#  ============ Module api view =========== #
class ModuleApiView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, *args, **kwargs):
        try:
            course_slug = kwargs.get("course_slug")
            user = request.user
            context = {}

            if user.is_authenticated:
                context["user"] = user
                try:
                    is_enrolled = Enrollment.objects.get(user=user, course__slug=course_slug)
                    context["is_enrolled"] = True
                except Enrollment.DoesNotExist:
                    context["is_enrolled"] = False

            modules = Module.objects.filter(course__slug=course_slug)
            if modules.exists():
                serializer = ModuleSerializer(modules, many=True, context=context)
                return SuccessResponse("modules", serializer.data)

            return ErrorResponse("No Modules Exist")

        except Module.DoesNotExist as e:
            print("Module exception:", str(e))
            return ErrorResponse(str(e))
        
# ======== Course Review  Api View ============ #
class ReviewApiView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = []

    def get(self,*args, **kwargs):
         try:
            course_slug =  kwargs.get("course_slug")
            review =  Review.objects.filter(course__slug =  course_slug)
            if review.exists():
                 serializer =  ReviewSerializer(review ,many=True)
                 return SuccessResponse("reviews" , serializer.data)
            else :
                 return ErrorResponse("NO Reviews Exisits")
         except Exception as e :
            print("Review Exception" , str(e))
            return ErrorResponse(str(e))
         



# ========== Completed Video Api View ====== #
class CompletedApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        lession_id = request.data.get("lession_id")
        user = request.user
        lession = get_object_or_404(Lession, pk=lession_id)
        try:
            complete_lession, created = CompleteLession.objects.get_or_create(
                user=user,
                lession=lession
            )
            if created:
                complete_lession.save()
                return SuccessResponse("message", f'{lession} is now marked as completed.')
            else:
                return SuccessResponse("message", "Lesson already marked as completed.")
        except Exception as e:
            return ErrorResponse("An unexpected error occurred: " + str(e))



