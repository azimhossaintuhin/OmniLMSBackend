from django.urls import path
from .views import (
    CategoryListApiView,
    CourseListApiView,
    CourseRetriveApiView,
    ReviewListApiView  # Assuming this is the correct view name for reviews
)

urlpatterns = [
    path("category/", CategoryListApiView.as_view(), name="category"),
    path("course/", CourseListApiView.as_view(), name="courseList"),
    path("course/<str:slug>/", CourseRetriveApiView.as_view(), name="courseRetrieve"),
    path("course/<str:course_slug>/review/", ReviewListApiView.as_view(), name="courseReviews"),
]
