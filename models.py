from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
from rp5_portal import settings

class User(AbstractUser):
    pass

class File(models.Model):
    name = models.CharField(max_length=255, default='none')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    