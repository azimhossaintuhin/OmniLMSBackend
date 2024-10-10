from django.db import models
from uuid import uuid4
from ckeditor.fields import RichTextField





# ========== Category  Model ========= #
class Category(models.Model):
    image =  models.ImageField("category")
    title =  models.CharField(max_length=255)
    is_top =  models.BooleanField(default=False)
    crated_at =  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



#  ======= Course Model ======= #
class Course(models.Model):
    level_choices =[
        ('biggner',"Biggner"),
        ('medium,' , "Medium"),
        ("expert" , "expert")
    ]
    
    type_choices =  [
        ('free',"Free"),
        ('paid','Paid')
    ]
    image =  models.ImageField("course")
    title =  models.CharField(max_length=255)
    category =  models.ForeignKey(Category,on_delete=models.CASCADE, related_name="course_category")
    level =  models.CharField(max_length=255 , choices=level_choices , default='bignner')
    learnings =  models.TextField(help_text="text must  be ',' separeted ")
    type =  models.CharField(max_length=255 ,choices=type_choices , default="paid")
    description = RichTextField()
    old_price =  models.PositiveIntegerField()
    base_price =  models.PositiveBigIntegerField()

    def __str__(self):
        return self.title
    


