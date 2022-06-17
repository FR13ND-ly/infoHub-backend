from django.db import models
from django.utils import timezone

class List(models.Model):
    name = models.CharField(max_length = 200, default = True)
    user = models.TextField(null = True)
    public = models.BooleanField(default = False)
    date = models.DateTimeField(default = timezone.now)
    editable = models.BooleanField(default = True)
    icon = models.TextField(default="bookmark")

    def __str__(self):
        return self.name

class ListItem(models.Model):
    List = models.TextField(null=True)
    article = models.TextField(null=True)
    date = models.DateTimeField(default=timezone.now)

class View(models.Model):
    article = models.TextField(null=True)
    user = models.TextField(null=True)
    date = models.DateTimeField(default=timezone.now)