from django.conf import settings
from django.db import models
from django.utils import timezone

class Comment(models.Model):
    author = models.TextField(null=True)
    text = models.TextField(null=True)
    article = models.TextField(null=True)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.text