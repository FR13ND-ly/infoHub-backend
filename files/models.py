from django.conf import settings
from django.db import models
from django.utils import timezone

class File(models.Model):
    file = models.FileField(blank=False, null=False)
    date = models.DateTimeField(default=timezone.now)
    hidden = models.BooleanField(default=False)
    def __str__(self):
        return self.file.name