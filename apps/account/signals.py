from  django.db.models.signals import post_save
from django.dispatch import receiver
# ======== Models ======== #
from .models import User , UserProfile



@receiver(post_save , sender=User)
def create_profile(sender, instance , created , **kwargs):
    if created:
        user_profile = UserProfile(
            user =  instance
        )
        user_profile.save()
