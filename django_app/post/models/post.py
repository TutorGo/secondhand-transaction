import locale
from django.db import models
from django.conf import settings

# Create your models here.
from utils.customfield import CustomImageField

__all__ = (
    'Post',
)

class Post(models.Model):
    CATEGORY_TYPE = (
        ('e', '전자기기'),
        ('fc', '패션의류'),
        ('fg', '패션잡화'),
        ('cb', '화장품/미용'),
        ('s', '스포츠/레저'),
        ('b', '도서'),
    )
    POST_TYPE = (
        ('s', 'Sell'),
        ('b', 'Buy')
    )
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    category = models.CharField(max_length=2, choices=CATEGORY_TYPE)
    sell_or_buy = models.CharField(max_length=4, choices=POST_TYPE)
    price = models.CharField(max_length=10)
    title = models.CharField(max_length=50)
    content = models.TextField()
    image_1 = models.ImageField(upload_to='post/%Y/%m/%d', default=None)
    image_2 = CustomImageField(upload_to='post/%Y/%m/%d', default=None, blank=True)
    image_3 = CustomImageField(upload_to='post/%Y/%m/%d', default=None, blank=True)

    class Meta:
        ordering = ['-pk']

    def __str__(self):
        return "[{}]{}({})".format(self.category, self.title, self.pk)

    def clean(self):
        print(self.price)
        self.price = format(int(self.price), ',d')

        super(Post, self).clean()


