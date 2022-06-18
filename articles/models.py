from django.conf import settings
from django.db import models
from django.utils import timezone

class Article(models.Model):
    title = models.TextField()
    subtitle = models.TextField(null=True)
    text = models.TextField()
    date = models.DateTimeField(default=timezone.now)
    draft = models.BooleanField(default = True)
    framework = models.BooleanField(default = True)
    hideViews = models.BooleanField(default = False)
    hideLikes = models.BooleanField(default = False)
    hideDate = models.BooleanField(default = False)
    restrictComments = models.BooleanField(default = False)
    tags = models.TextField()
    url = models.TextField()
    coverImage = models.PositiveIntegerField(null= True)
    coverImageDescription = models.TextField(default='')
    views = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return self.title + " #" + str(self.id)

class AditionalArticle(models.Model):
    sourceArticle = models.TextField(default='')
    sharedArticle = models.TextField(default='')

class Survey(models.Model):
    article = models.TextField(default='')
    question = models.CharField(max_length=200)
    def __str__(self):
        return self.question

class Variant(models.Model):
    survey = models.TextField(default='')
    content = models.CharField(max_length=200)
    def __str__(self):
        return self.content

class Vote(models.Model):
    user = models.TextField(default='')
    variant = models.TextField(default='') 