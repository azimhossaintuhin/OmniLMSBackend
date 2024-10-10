from django.shortcuts import render
from . models import Course , Category
from .serializers import CategorySeiralizer , CourseSerializer
from rest_framework.permissions import IsAuthenticated
from constant.Response import SuccessResponse , ErrorResponse
from rest_framework.generics import ListAPIView,RetrieveAPIView




# ========= Category List Api View ============ #
class CategoryListApiView(ListAPIView):
    serializer_class =  CategorySeiralizer
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

                  