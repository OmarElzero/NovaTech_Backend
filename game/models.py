from django.db import models
import requests

from django.contrib.auth.models import User

# Create your models here.

class Exoplanet(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Users(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=100, unique=True)
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    unlocked_exoplanets = models.ManyToManyField(Exoplanet, blank=True)
    def __str__(self):
        return self.username