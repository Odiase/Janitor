from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    '''A Regular User Profile'''

    profile_image = models.ImageField(upload_to="user_uploads/user_profile_images")
    