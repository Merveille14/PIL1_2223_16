from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)