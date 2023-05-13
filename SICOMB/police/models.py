# from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class Police(models.Model):
    name = models.CharField('Nome', max_length=100)
    patent = models.CharField('Patente', max_length=100)
    plate = models.CharField('Matricula', max_length=20)
    password = models.CharField('Senha', max_length=20)
    
# class adjunto(models.Model):
