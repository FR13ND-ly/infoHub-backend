from django.db import models

class Widget(models.Model):
    text = models.CharField(max_length=200)
    link = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    activated = models.BooleanField(default = False)