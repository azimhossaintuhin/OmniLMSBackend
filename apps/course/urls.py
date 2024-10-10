from django.urls import path
from .views import CategoryListApiView,CourseListApiView


urlpatterns = [
    path("category/" , CategoryListApiView.as_view() , name="category"),
    path("course/" , CourseListApiView.as_view(), name="courseList")
]
