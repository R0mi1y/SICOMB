from django.db import models
from equipment.models import Equipment, Bullet
from police.models import Police
from django.utils import timezone
# Create your models here.


class Load(models.Model):
    load_unload = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    date_load = models.DateTimeField(default=timezone.now)
    expected_load_return_date = models.DateTimeField(
        "Data Prevista de Devolução", null=True
    )
    returned_load_date = models.DateTimeField("Data de Descarregamento", null=True)
    turn_type = models.CharField(max_length=20)
    # nomear atributo que receberá os dados: 6h, 12h, 24h, conserto, requisição judicial ou indeterminado
    status = models.CharField(
        "horário_carga",
        max_length=50,
        default="DENTRO DO PRAZO",
        choices=(("Devolvido", "Devolvido"), ("Pendente", "Pendente"), ("Parcialmente devolvido", "Parcialmente devolvido")),
    )
    police = models.ForeignKey(
        Police, on_delete=models.DO_NOTHING, related_name="policial"
    )
    adjunct = models.ForeignKey(
        Police, on_delete=models.DO_NOTHING, related_name="adjunto"
    )

    def __str__(self):
        return str(self.pk)


# Tabela que faz o relacionamento entre a carga e os equipamentos
class Equipment_load(models.Model):
    load = models.ForeignKey(Load, on_delete=models.CASCADE, related_name='equipment_loads')
    equipment = models.ForeignKey(
        Equipment, on_delete=models.CASCADE, null=True, default=None
    )
    bullet = models.ForeignKey(
        Bullet, on_delete=models.CASCADE, null=True, default=None
    )
    amount = models.IntegerField("Quantidade", null=True, default="1")
    observation = models.TextField("Observação", default=None, null=True)
    status = models.CharField(
        "Status",
        max_length=20,
        default="Pendente",
        choices=(("Devolvido", "Devolvido"), ("Pendente", "Pendente")),
    )

    # o amount diz, caso seja uma munição, a quantidade selecionada nessa carga em específico e dessa munição em específico


