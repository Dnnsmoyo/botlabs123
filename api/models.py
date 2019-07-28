from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User

# Create your models here.
class User(AbstractUser):
    free = models.BooleanField('free status',default=False)
    premium = models.BooleanField('premium status',default=False)
    business = models.BooleanField('business status',default=False)