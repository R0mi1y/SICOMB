from django.db import models
from police.models import Police, RegisterPolice
# from adjunct.models import Adjunct #Para importar o modelo do Adjunto

# Create your models here.

class Cargo(models.Model):
    id = models.IntegerField('ID', primary_key=True)
    date_cargo = models.DateTimeField('Data da Carga')
    expected_cargo_return_date = models.DateTimeField('Data Prevista de Devolução')
    #nomear atributo que receberá os dados: 6h, 12h, 24h, conserto, requisição judicial ou indeterminado
    police = models.ForeignKey(RegisterPolice, on_delete=models.CASCADE)
    # adjunct = models.ForeignKey(Adjunct, on_delete=models.CASCADE) #Pega a chave primária do adjunto
    
    
    