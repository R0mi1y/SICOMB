# from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Adjunct(User):
    nome = models.CharField(max_length=100, unique=True)
    matricula = models.CharField(max_length=20, primary_key=True)
    telefone = models.CharField(max_length=20, unique=True)
    lotacao = models.CharField(max_length=50)
    posto = models.CharField(max_length=10)
    foto = models.FileField(upload_to="media/")


class RegisterPolice(models.Model):
    nome = models.CharField(max_length=100, unique=True)
    matricula = models.CharField(max_length=20, primary_key=True)
    telefone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=254, unique=True)
    lotacao = models.CharField(max_length=50)
    posto = models.CharField(max_length=10)
    senha = models.CharField(max_length=100)
    foto = models.FileField(upload_to="media/")

    class Meta:
        verbose_name = 'Policial'
        verbose_name_plural = 'Policiais'