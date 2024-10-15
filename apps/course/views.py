from django.shortcuts import render
from . models import  *
from .serializers import CategorySerializer , CourseSerializer , ReviewSerializer
from rest_framework.permissions import IsAuthenticated
from constant.Response import SuccessResponse , ErrorResponse
from rest_framework.generics import ListAPIView,RetrieveAPIView
from rest_framework.views import APIView




# ========= Category List Api View ============ #
class CategoryListApiView(ListAPIView):
    serializer_class =  CategorySerializer
    queryset =  Category.objects.all()
    permission_classes=[]
    authentication_classes=[]

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
      permission_classes = []
      authentication_classes=[]

    # ====== Overriding the  list ======== #
      def list(self,request ,*args, **kwargs):
            try:
                qeuryset = self.get_queryset()
                print("queryset" , qeuryset)
                if not qeuryset.exists():
                      return ErrorResponse("No course found.")
                serializer =  self.get_serializer(qeuryset , many=True)
                return SuccessResponse("course" ,  serializer.data)
            except Exception as e:
                  print(e)
                  return ErrorResponse("An error occurred while retrieving categories.")




# ========== Course  Retrive Api View ============= #
class CourseRetriveApiView(RetrieveAPIView):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    lookup_field = 'slug'
    permission_classes = []
    authentication_classes = []

    def retrieve(self, request, *args, **kwargs):
        try:
            course = self.get_object()
            serializer = self.get_serializer(course)
            return SuccessResponse("course_details", serializer.data)
        
        except Course.DoesNotExist:
            return ErrorResponse("Course not found.")
        except Exception as e:
            print(f"Error retrieving course details: {str(e)}")
            return ErrorResponse("An error occurred while retrieving course details.")

# ======== Course Review List Api View ============ #
class ReviewListApiView(ListAPIView):
    permission_classes = []
    authentication_classes = []
    serializer_class = ReviewSerializer

    def get(self,*args, **kwargs):
         try:
            course_slug =  kwargs.get("course_slug")
            review =  Review.objects.filter(course__slug =  course_slug)
            if review.exists():
                 return SuccessResponse("reviews" , review)
            else :
                 return ErrorResponse("NO Reviews Exisits")
         except Exception as e :
            print("Review Exception" , str(e))
            return ErrorResponse(str(e))
         

    
    
         
         