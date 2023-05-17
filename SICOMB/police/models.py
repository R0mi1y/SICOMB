# from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Police(User):
    patent = models.CharField('Patente', max_length=100)
    plate = models.CharField('Matricula', max_length=20)
    
# class adjunto(models.Model):
