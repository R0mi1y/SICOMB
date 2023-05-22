# from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Police(User):
    patent = models.CharField('Patente', max_length=100)
    plate = models.CharField('Matricula', max_length=20)
    
# class adjunto(models.Model):

class RegisterPolice(models.Model):
    
    nome = models.CharField(max_length=200)
    sobrenome = models.CharField(max_length=200)
    matricula = models.CharField(max_length=20)
    posto = models.CharField(max_length=10)
    email = models.EmailField(max_length=200)
    telefone = models.CharField(max_length=11)
    lotacao = models.CharField(max_length=50)