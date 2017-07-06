from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class UserProfile(models.Model):
    #belong_to = models.OneToOneField(to=User, related_name='profile')
    username = models.CharField(null=True, blank=True, max_length=20)
    #profile_image = models.FileField(null=True, blank=True, upload_to='profile_image')
    user_upload_file = models.FileField(null=True, blank=True, upload_to='./upload/')

# class UserProfile(models.Model):
#     belong_to = models.OneToOneField(to=User, related_name='profile')
#     #profile_image = models.FileField(upload_to='profile_image')
#     user_upload_file = models.FileField()