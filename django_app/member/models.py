from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class MyUser(AbstractUser):
    USER_TYPE = (
        ('f', 'Facebook'),
        ('n', 'Naver'),
        ('g', 'general')
    )
    user_type = models.CharField(max_length=1, default='g', choices=USER_TYPE)
    phone = models.IntegerField()
    email = models.CharField(unique=True, max_length=30)
    nickname = models.CharField(max_length=15)
    REQUIRED_FIELDS = ['email']


