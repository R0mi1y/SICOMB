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
            attrs={"class": "input-data", "id": "serial-number-input"}
        ),
        label="Número de Série",
    )
    type = forms.CharField(
        widget=forms.Select(
            attrs={"class": "input-data", "id": "type-choices"}, choices=OPCOES
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
                "class": "type-choices-type",
            }
        )
        self.fields["armament"].label = ""
        self.fields["armament"].initial = ""
        self.fields["armament"].required = False
        self.fields["armament"].queryset = Model_armament.objects.all()

        self.fields["accessory"].widget = forms.Select(
            attrs={
                "id": "type-choices-accessory",
                "style": "display: none",
                "class": "type-choices-type",
            }
        )
        self.fields["accessory"].label = ""
        self.fields["accessory"].initial = ""
        self.fields["accessory"].required = False
        self.fields["accessory"].queryset = Model_accessory.objects.all()

        self.fields["wearable"].widget = forms.Select(
            attrs={
                "id": "type-choices-wearable",
                "style": "display: none",
                "class": "type-choices-type",
            }
        )
        self.fields["wearable"].label = ""
        self.fields["wearable"].initial = ""
        self.fields["wearable"].required = False
        self.fields["wearable"].queryset = Model_wearable.objects.all()

        self.fields["grenada"].widget = forms.Select(
            attrs={
                "id": "type-choices-grenada",
                "style": "display: none",
                "class": "type-choices-type",
            }
        )
        self.fields["grenada"].label = ""
        self.fields["grenada"].initial = ""
        self.fields["grenada"].required = False
        self.fields["grenada"].queryset = Model_grenada.objects.all()
