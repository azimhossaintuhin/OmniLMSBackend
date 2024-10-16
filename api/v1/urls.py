from  django.urls import path , include

urlpatterns = [
    path("" , include("apps.account.urls") , name ="accounts"),
    path("", include("apps.course.urls") ,  name="course"),
    path("" , include("apps.payments.urls") , name="payment")
    
]
