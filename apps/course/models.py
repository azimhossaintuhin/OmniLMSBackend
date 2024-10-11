from django.db import models
from uuid import uuid4
from ckeditor.fields import RichTextField
from django.utils.text import slugify




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
        ('expert,' , "Expert"),
        ("advanced" , "advanced"),
        ('top_rated' , "Top Rated")
    ]
    type_choices =  [
        ('free',"Free"),
        ('paid','Paid')
    ]
    image =  models.ImageField("course")
    title =  models.CharField(max_length=255)
    slug =  models.CharField(max_length=355,null= True , blank=True)
    category =  models.ForeignKey(Category,on_delete=models.CASCADE, related_name="course_category")
    level =  models.CharField(max_length=255 , choices=level_choices , default='bignner')
    learnings =  models.TextField(help_text="text must  be ',' separeted ")
    type =  models.CharField(max_length=255 ,choices=type_choices , default="paid")
    short_description =  models.TextField(null=True,blank=True)
    description = RichTextField()
    old_price =  models.PositiveIntegerField()
    new_price =  models.PositiveBigIntegerField()
    created_at =  models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title
    

    def save(self,*args,**kwargs):
        if self.type is  "free":
            self.old_price = 0
            self.new_price =  0
            self.slug =  slugify(self.title)
        return super().save(*args , **kwargs)
    
        
# ========== Lessions ========= #
class Lessions(models.Model):
    course =  models.ForeignKey(Course , on_delete=models.CASCADE,related_name="course_lession")
    title =  models.CharField(max_length=255 , null= True , blank=True)
    created_at  =  models.DateField(auto_now_add=True)


    def __str__(self , *args , **kwargs):
        return self.title
    


# ============ Videos ============= #
class Videos(models.Model):
    lession =  models.ForeignKey(Lessions , on_delete=models.CASCADE , related_name="video_lessions")
    title  =  models.CharField(max_length=255 , null= True , blank=True)
    video =  models.FileField(upload_to="videos" , null=True , blank=True)
    video_link = models.URLField(null=True , blank=True)
    durations =  models.CharField(max_length=255 , null=True , blank=True )
    is_free =  models.BooleanField(default=False)
    created =  models.DateField(auto_now_add=True)

    def __str__(self):
        return self.title




# =========== 
class enrollment(models.Model):
    pass


