from django.urls import path
from .views import CategoryListApiView,CourseListApiView,CourseRetriveApiView


urlpatterns = [
    path("category/" , CategoryListApiView.as_view() , name="category"),
    path("course/" , CourseListApiView.as_view(), name="courseList"),
    path("course/<str:slug>" , CourseRetriveApiView.as_view() , name="course retive")
]
