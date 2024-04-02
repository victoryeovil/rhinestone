from django.db import models
from django.contrib.auth.models import AbstractUser

from .fields import ImageField

class User(AbstractUser):
    profile_picture = ImageField(upload_to="users/profilepics", blank=True, null=True)
    
    def __str__(self):
        return self.get_full_name() if all([self.first_name, self.last_name]) else self.username
    