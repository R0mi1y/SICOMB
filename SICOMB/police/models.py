# from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Police(User):
    patent = models.CharField("Patente", max_length=100)
    plate = models.CharField("Matricula", max_length=20)
    posto = models.CharField(max_length=10, default="Policial")
    telefone = models.CharField(max_length=11)


class RegisterPolice(models.Model):
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=20, primary_key=True)
    telefone = models.CharField(max_length=20)
    lotacao = models.CharField(max_length=50)
    posto = models.CharField(max_length=10)
    email = models.EmailField(max_length=254)
    foto = models.FileField(upload_to="media/")
