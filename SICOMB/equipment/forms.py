from django import forms
from equipment.models import *


class EquipmentForm(forms.ModelForm):
    OPCOES = [
        ("", "Selecione"),
        ("wearable", "Vestível"),
        ("accessory", "Acessório"),
        ("armament", "Armamento"),
        ("grenada", "Granada"),
    ]

    uid = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                "id": "input-uid",
                "style": "display: none",
            }
        ),
        label="",
    )
    serial_number = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": "input-data", "id": "serial-number-input", "placeholder": "Número de série"}
        ),
        label="Número de Série",
    )
    type = forms.CharField(
        widget=forms.Select(
            attrs={"class": "select-field", "id": "type-choices"}, choices=OPCOES
        ),
        label="Tipo",
    )

    class Meta:
        model = Equipment
        fields = [
            "uid",
            "serial_number",
            "type",
            "armament",
            "accessory",
            "wearable",
            "grenada",
        ]  # pra definir a ordem

        # os que não devem aparecer
        exclude = ("status", "observation")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # A partir daqui ele modifica todos os campos pois ele já
        # vem setado com td certo e refazer daria mais trabalho

        self.fields["armament"].widget = forms.Select(
            attrs={
                "id": "type-choices-armament",
                "style": "display: none",
                "class": "type-choices-type select-field",
            }
        )
        self.fields["armament"].label = "ARMAMENTOS"
        self.fields["armament"].initial = ""
        self.fields["armament"].required = False
        self.fields["armament"].queryset = Model_armament.objects.all()

        self.fields["accessory"].widget = forms.Select(
            attrs={
                "id": "type-choices-accessory",
                "style": "display: none",
                "class": "type-choices-type select-field",
            }
        )
        self.fields["accessory"].label = "ACESSÓRIOS"
        self.fields["accessory"].initial = ""
        self.fields["accessory"].required = False
        self.fields["accessory"].queryset = Model_accessory.objects.all()

        self.fields["wearable"].widget = forms.Select(
            attrs={
                "id": "type-choices-wearable",
                "style": "display: none",
                "class": "type-choices-type select-field",
            }
        )
        self.fields["wearable"].label = "VESTIMENTOS"
        self.fields["wearable"].initial = ""
        self.fields["wearable"].required = False
        self.fields["wearable"].queryset = Model_wearable.objects.all()

        self.fields["grenada"].widget = forms.Select(
            attrs={
                "id": "type-choices-grenada",
                "style": "display: none",
                "class": "type-choices-type select-field",
            }
        )
        self.fields["grenada"].label = "GRANADAS"
        self.fields["grenada"].initial = ""
        self.fields["grenada"].required = False
        self.fields["grenada"].queryset = Model_grenada.objects.all()


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