from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=20, null=True, blank=True)

class Article(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    tags = models.ManyToManyField('Tag')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

class Question(models.Model):
    question_text = models.TextField()
    answer_text = models.TextField(null=True, blank=True)
    asked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    asked_at = models.DateTimeField(auto_now_add=True)

