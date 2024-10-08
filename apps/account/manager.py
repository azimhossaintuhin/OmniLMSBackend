from django.contrib.auth.models import BaseUserManager

# ===== Custom User Manager ====== #

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_kwargs):
        # Email Validation
        if not email:
            raise ValueError("Email must be provided")
        
        # Check if the email already exists
        if self.model.objects.filter(email=email).exists():
            raise ValueError("Email already exists")

        # Normalizing the email
        email = self.normalize_email(email)

        # Creating the user
        user = self.model(email=email, **extra_kwargs)
        user.set_password(password)
        user.save(using=self._db)  # Use the specified database
        return user

    def create_superuser(self, email, password=None, **extra_kwargs):
        # Setting some default values
        extra_kwargs.setdefault("is_staff", True)
        extra_kwargs.setdefault("is_active", True)
        extra_kwargs.setdefault("is_superuser", True)

        # Validate extra kwargs
        if extra_kwargs.get("is_staff") is not True:
            raise ValueError("is_staff must be True")

        if extra_kwargs.get("is_active") is not True:
            raise ValueError("is_active must be True")

        if extra_kwargs.get("is_superuser") is not True:
            raise ValueError("is_superuser must be True")
        
        # Create the user with superuser privileges
        return self.create_user(email, password, **extra_kwargs)
