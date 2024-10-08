from  django.urls import path , include

urlpatterns = [
    path("" , include("apps.account.urls") , name ="accounts"),
    
]
