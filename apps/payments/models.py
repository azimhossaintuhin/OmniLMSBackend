from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from apps.course.models import Course
from django.db import models
from apps.account.models import User
from apps.course.models import Course

class Cupon(models.Model):
    cupon = models.CharField(max_length=255)
    discount_parcentige =  models.IntegerField(default=0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    specific_course = models.ManyToManyField(Course, blank=True)
    is_for_all = models.BooleanField(default=False)
  
    def __str__(self):
        return self.cupon
    

class Cart(models.Model):
    user =  models.ForeignKey(User , on_delete=models.CASCADE , related_name='cart_user')
    course =  models.ForeignKey(Course,on_delete=models.CASCADE , related_name="cart_course" ,null=True , blank=True)
    cupon =  models.ForeignKey(Cupon , on_delete=models.SET_NULL , null=True , blank=True)
    created_at =  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email
    

    def total_ammount(self):
        original_price =  self.course.new_price
        if self.cupon:
            discount_ammount =  (self.cupon.discount_parcentige/100)*original_price
            discount_price =  original_price - discount_ammount
            return discount_price
        return original_price


    def get_disscout_ammount(self):
        discount_ammout = 0
        original_price = self.course.new_price
        if self.cupon:
            return (self.cupon.discount_parcentige/100)*original_price
        
        return discount_ammout
    









