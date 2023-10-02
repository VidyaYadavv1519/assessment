from django.db import models
from django.contrib.auth.models import User 
from django.db.models import OneToOneField 

# Create your models here.
class UserProfile(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE)
