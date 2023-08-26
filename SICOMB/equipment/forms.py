from django import forms
from equipment.models import *


class EquipmentForm(forms.ModelForm):
    OPCOES = [
        ("", "SELECIONE"),
        ("wearable", "VESTÍVEL"),
        ("accessory", "ACESSÓRIO"),
        ("armament", "ARMAMENTO"),
        ("grenada", "GRANADA"),
    ]

    uid = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={"id": "input-uid", "style": "display: none"}),
        label="",
    )
    serial_number = forms.CharField(
        widget=forms.TextInput(attrs={"class": "input-data", "id": "serial-number-input", "placeholder": "Número de série"}),
        label="Número de Série",
    )
    type = forms.CharField(
        widget=forms.Select(attrs={"class": "select-field", "id": "type-choices"}, choices=OPCOES),
        label="Tipo",
    )
    
    armament = forms.ModelChoiceField(
        queryset=Model_armament.objects.all(),
        widget=forms.Select(attrs={"id": "type-choices-armament", "style": "display: none", "class": "type-choices-type select-field", "name": "model"}),
        label="ARMAMENTOS",
        empty_label="SELECIONE",
        required=False,
    )
    accessory = forms.ModelChoiceField(
        queryset=Model_accessory.objects.all(),
        widget=forms.Select(attrs={"id": "type-choices-accessory", "style": "display: none", "class": "type-choices-type select-field", "name": "model"}),
        label="ACESSÓRIOS",
        empty_label="SELECIONE",
        required=False,
    )
    wearable = forms.ModelChoiceField(
        queryset=Model_wearable.objects.all(),
        widget=forms.Select(attrs={"id": "type-choices-wearable", "style": "display: none", "class": "type-choices-type select-field", "name": "model"}),
        label="VESTIMENTOS",
        empty_label="SELECIONE",
        required=False,
    )
    grenada = forms.ModelChoiceField(
        queryset=Model_grenada.objects.all(),
        widget=forms.Select(attrs={"id": "type-choices-grenada", "style": "display: none", "class": "type-choices-type select-field", "name": "model"}),
        label="GRANADAS",
        empty_label="SELECIONE",
        required=False,
    )
    
    def save(self, commit=True):
        equipment = super().save(commit=False)
        
        # Define o tipo de modelo com base na escolha feita no campo "type"
        if self.cleaned_data['type'] == 'armament':
            equipment.model = self.cleaned_data['armament']
        elif self.cleaned_data['type'] == 'accessory':
            equipment.model = self.cleaned_data['accessory']
        elif self.cleaned_data['type'] == 'wearable':
            equipment.model = self.cleaned_data['wearable']
        elif self.cleaned_data['type'] == 'grenada':
            equipment.model = self.cleaned_data['grenada']

        if commit:
            equipment.save()
        return equipment

    class Meta:
        model = Equipment
        fields = ["uid", "serial_number", "type", "status"]
        
        widgets = {
            "status" : forms.Select(attrs={"class": "select-field"}),
        }


class Model_grenadaForm(forms.ModelForm):
    
    class Meta:
        model = Model_grenada
        fields = [
            "model",
            "image_path",
            "description",
        ] 
        widgets = {
            "description": forms.Textarea(attrs={"class": "input-data", "placeholder": "Descrição", "rows":3}),
            "model": forms.TextInput(attrs={"class": "input-data", "placeholder": "Modelo"}),
            "image_path": forms.FileInput(attrs={"class": "input-file", "id":"file", "accept":"image/*"})
        }
        
        
class Model_armamentForm(forms.ModelForm):
    
    class Meta:
        model = Model_armament
        fields = [
            "caliber",
            "model",
            "image_path",
            "description",
        ] 
        # Tava bugando ent coloquei aqui
        widgets = {
            "description": forms.Textarea(attrs={"class": "input-data", "placeholder": "Descrição", "rows":3}),
            "caliber": forms.Select(attrs={"class": "select-field", "placeholder": "Calibre"}),
            "model": forms.TextInput(attrs={"class": "input-data", "placeholder": "Modelo"}),
            "image_path": forms.FileInput(attrs={"class": "input-file", "id":"file", "accept":"image/*"})
        }
        
class Model_wearableForm(forms.ModelForm):
    
    class Meta:
        model = Model_wearable
        fields = [
            "size",
            "model",
            "image_path",
            "description",
        ] 
        widgets = {
            "description": forms.Textarea(attrs={"class": "input-data", "placeholder": "Descrição", "rows":3}),
            "size": forms.TextInput(attrs={"class": "input-data", "placeholder": "Tamanho"}),
            "model": forms.TextInput(attrs={"class": "input-data", "placeholder": "Modelo"}),
            "image_path": forms.FileInput(attrs={"class": "input-file", "id":"file", "accept":"image/*"})
        }
        
class Model_accessoryForm(forms.ModelForm):
    
    class Meta:
        model = Model_accessory
        fields = [
            "model",
            "image_path",
            "description",
        ] 
        widgets = {
            "description": forms.Textarea(attrs={"class": "input-data", "placeholder": "Descrição", "rows":3}),
            "model": forms.TextInput(attrs={"class": "input-data", "placeholder": "Modelo"}),
            "image_path": forms.FileInput(attrs={"class": "input-file", "id":"file", "accept":"image/*"})
        }
        

class BulletForm(forms.ModelForm):
    
    class Meta:
        model = Bullet
        fields = [
            "amount",
            "caliber",
            "image_path",
            "description",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"class": "input-data", "placeholder": "Descrição", "rows":3}),
            "caliber": forms.Select(attrs={"class": "select-field", "placeholder": "Calibre"}),
            "amount": forms.NumberInput(attrs={"class": "input-data", "placeholder": "Modelo", "min":0}),
            "image_path": forms.FileInput(attrs={"class": "input-file", "id":"file", "accept":"image/*"})
        }
        
        
        
        
        
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Equipment

class EquipmentFilterForm(forms.Form):
    equipment_choices = Equipment.CHOICES
    equipment_choices += ((None, "-----------"),)
    
    models_eqipment = (
        (None, '----------'),
        (ContentType.objects.get(app_label='equipment', model='Model_armament').pk, 'Armamento'),
        (ContentType.objects.get(app_label='equipment', model='Model_accessory').pk, 'Acessório'),
        (ContentType.objects.get(app_label='equipment', model='Model_wearable').pk, 'Vestimentos'),
        (ContentType.objects.get(app_label='equipment', model='Model_grenada').pk, 'Granadas'),
    )
    
    serial_number = forms.CharField(label=_("Número de Série"), max_length=20, required=False)
    uid = forms.CharField(label=_("UID"), max_length=20, required=False)
    status = forms.ChoiceField(
        label=_("Estado Atual"),
        choices=equipment_choices,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    model_type = forms.ChoiceField(
        label=_("Tipo do Modelo"),
        choices=models_eqipment,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )

    def filter_queryset(self, queryset):
        data = self.cleaned_data

        if data.get('serial_number'):
            queryset = queryset.filter(serial_number__icontains=data['serial_number'])
        if data.get('uid'):
            queryset = queryset.filter(uid__icontains=data['uid'])
        if data.get('status'):
            queryset = queryset.filter(status__icontains=data['status'])
        if data.get('model_type'):
            queryset = queryset.filter(model_type=data['model_type'])

        return queryset
