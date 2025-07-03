from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_admin = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='user_photos/', null=True, blank=True)
