from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.
MyUser = get_user_model()


class Message(models.Model):
    sender = models.ForeignKey(MyUser, related_name='sent_message')
    recipient = models.ForeignKey(MyUser, related_name='received_message')
    content = models.TextField()
    send_time = models.DateTimeField(auto_now_add=True)
    read_time = models.DateTimeField(null=True, blank=True)
    message_read = models.BooleanField(default=False)
    sender_delete = models.BooleanField(default=False)
    recipient_delete = models.BooleanField(default=False)

    class Meta:
        ordering = ['-pk']

