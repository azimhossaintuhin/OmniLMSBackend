from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
from django.utils import timezone
# ====== Custom User Model ======= #
class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    _is_verified = models.BooleanField(default=False) 
    
    REQUIRED_FIELDS = [] 
    USERNAME_FIELD = 'email'
    objects = UserManager()

    # Getter for is_verified property
    @property
    def is_verified(self):
        return self._is_verified
    
    # Setter for is_verified property
    @is_verified.setter
    def is_verified(self, value):
        self._is_verified = value

    def save(self, *args, **kwargs):
        if self.is_superuser:
            self._is_verified = True
        super().save(*args, **kwargs)


#  ======== User  Profile =========== # 
class UserProfile(models.Model):
    user = models.OneToOneField(User , related_name="user_profile" , on_delete=models.CASCADE)
    image =  models.ImageField("profile" , null=True , blank=True)
    full_name =  models.CharField(max_length=255 , null=True , blank=True)
    address =  models.TextField(null=True , blank=True)
    crated =  models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username



# ========== Forgot password ============= # 
class Token(models.Model):
    user =  models.ForeignKey(User,related_name="user_token",on_delete=models.CASCADE)
    token =  models.CharField(max_length=25555 , null=True , blank=True)
    created_at =  models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.token
    
    def is_expired(self):
        expiration_time = timezone.timedelta(minutes=5) 
        print("now time" , timezone.now())
        print("expired time " , self.created_at + expiration_time)
        return timezone.now() > self.created_at + expiration_time















    

