from datetime import datetime
from django.db import models
from equipment.models import Equipment, Bullet
from police.models import Police
from django.utils import timezone
from django.db.models import Q
# Create your models here.


class Load(models.Model):
    load_unload = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    date_load = models.DateTimeField(default=timezone.now)
    expected_load_return_date = models.DateTimeField(
        "Data Prevista de Devolução", null=True
    )
    returned_load_date = models.DateTimeField("Data de Descarregamento", null=True)
    turn_type = models.CharField(max_length=20)
    status = models.CharField(
        "horário_carga",
        max_length=50,
        default="DENTRO DO PRAZO",
        choices=(
            ("Devolvido", "Devolvido"), 
            ("Pendente", "Pendente"), 
            ("Parcialmente devolvido", "Parcialmente devolvido"),
            ("Justificado", "Justificado"),
        ),
    )
    police = models.ForeignKey(
        Police, on_delete=models.DO_NOTHING, related_name="policial"
    )
    adjunct = models.ForeignKey(
        Police, on_delete=models.DO_NOTHING, related_name="adjunto"
    )

    def __str__(self):
        return str(self.pk)
    
    def check_load(self):
        load = self
        data_hora_atual = timezone.now()
        expected_return_date = load.expected_load_return_date
        
        # se tem alguma que já foi devolvida
        has_devolved = load.equipment_loads.filter(Q(status='Devolvido') | Q(status="Justificado")).exists()
        # se tem alguma que ainda não foi devolvida
        has_not_devolved = load.equipment_loads.exclude(Q(status='Devolvido') | Q(status="Justificado")).exists()
        
        status_descarregado = ['DESCARREGADA', 'DESCARREGADA COM ATRASO']
        
        if load.turn_type != 'descarga':
            if load.status not in status_descarregado: 
                if expected_return_date:
                    if data_hora_atual > expected_return_date:
                        if has_devolved:
                            if has_not_devolved:
                                load.status = 'PARCIALMENTE DESCARREGADA COM ATRASO'
                            else:
                                load.status = 'DESCARREGADA COM ATRASO'
                            load.returned_load_date = datetime.now()
                        else:
                            load.status = 'ATRASADA'
                    else:
                        if has_devolved:
                            if has_not_devolved:
                                load.status = 'PARCIALMENTE DESCARREGADA'
                            else:
                                load.status = 'DESCARREGADA'
                            load.returned_load_date = datetime.now()
                        else:
                            load.status = 'DENTRO DO PRAZO'
                else:
                    if has_devolved:
                        if has_not_devolved:
                            load.status = 'PARCIALMENTE DESCARREGADA'
                        else:
                            load.status = 'DESCARREGADA'
                    else:
                        load.status = 'DATA DE RETORNO NÃO DEFINIDA'
        else:
            load.status = 'descarga'
                    
        load.save()
        return True


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
        choices=(
            ("Devolvido", "Devolvido"), 
            ("Pendente", "Pendente"),
            ("Justificado", "Justificado"),
        ),
    )

    # o amount diz, caso seja uma munição, a quantidade selecionada nessa carga em específico e dessa munição em específico


