from django.conf import settings
from django.db import models
from django.utils import timezone

class Like(models.Model):
    article = models.TextField(null=True)
    user = models.TextField(null=True)
    date = models.DateTimeField(default=timezone.now)