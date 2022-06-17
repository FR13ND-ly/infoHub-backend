from django.conf import settings
from django.db import models
from django.utils import timezone

class Profile(models.Model):
    token = models.TextField()
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    image = models.IntegerField(default=1)
    allowWriteComments = models.BooleanField(default=True)
    allowChangeAvatar = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username