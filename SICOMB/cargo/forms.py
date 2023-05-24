from django import forms
from cargo.models import Cargo


class CargoForm(forms.ModelForm):
    
    date_cargo = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class':''}), label='Data da Carga')
    
    class Meta:
        model = Cargo
        fields = '__all__'