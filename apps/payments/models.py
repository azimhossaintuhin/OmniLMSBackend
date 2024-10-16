from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from apps.course.models import Course
from django.db import models

class Coupon(models.Model):
    cupon = models.CharField(max_length=255)
    discount_parcentige =  models.IntegerField(default=0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    specific_course = models.ManyToManyField(Course, blank=True)
    is_for_all = models.BooleanField(default=False)
  
    def __str__(self):
        return self.title
