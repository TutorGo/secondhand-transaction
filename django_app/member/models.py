from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class MyUserManager(UserManager):
    def get_or_create_facebook_user(self, user_info):
        email = '{}_{}'.format(
            self.model.USER_TYPE_FACEBOOK,
            user_info['id']
        )
        nickname = '{}_{}'.format(
            user_info.get('name', ''),
            user_info['id'],
        )

        user, _ = self.get_or_create(
            email=email,
            user_type=self.model.USER_TYPE_FACEBOOK,
            nickname=nickname
        )

        return user

# Create your models here.
class MyUser(AbstractUser):
    USER_TYPE_GENERAL = 'g'
    USER_TYPE_FACEBOOK = 'f'
    USER_TYPE_NAVER = 'n'
    USER_TYPE = (
        (USER_TYPE_FACEBOOK, 'Facebook'),
        (USER_TYPE_NAVER, 'Naver'),
        (USER_TYPE_GENERAL, 'General')
    )
    user_type = models.CharField(max_length=1, default='g', choices=USER_TYPE)
    email = models.CharField(unique=True, max_length=30)
    nickname = models.CharField(max_length=15)
    REQUIRED_FIELDS = ['email']

    objects = MyUserManager()