from django.urls import path
from .views import (
    CategoryListApiView,
    CourseListApiView,
    CourseRetriveApiView,
    ReviewApiView,
    ModuleApiView
)

urlpatterns = [
    path("category/", CategoryListApiView.as_view(), name="category"),
    path("course/", CourseListApiView.as_view(), name="courseList"),
    path("course/<str:slug>/", CourseRetriveApiView.as_view(), name="courseRetrieve"),
    path("course/<str:course_slug>/review/", ReviewApiView.as_view(), name="courseReviews"),
    path("course/<str:course_slug>/module/", ModuleApiView.as_view() , name="course_module")
]
