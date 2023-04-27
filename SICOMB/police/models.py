from django.db import models

# Create your models here.
class Police(models.Model):
    name = models.CharField('Nome', max_length=100)
    patent = models.CharField('Nome', max_length=100)
    