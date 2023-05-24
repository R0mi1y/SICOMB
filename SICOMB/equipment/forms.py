from django import forms
from equipment.models import Equipment


class PoliceForm(forms.ModelForm):
    
    serial_number = forms.CharField(widget=forms.TextInput(attrs={'class':'input-data'}), label='Número de Série')
    uid = forms.CharField(widget=forms.TextInput(attrs={'class':'input-data'}), label='UID')
    type = forms.CharField(widget=forms.TextInput(attrs={'class':'input-data'}), label='Tipo')
    type_id = forms.CharField(widget=forms.TextInput(attrs={'class':'input-data'}), label='Tipo')
    observation = forms.CharField(widget=forms.TextInput(attrs={'class':'input-data'}), label='Observação')
    status = forms.CharField(widget=forms.TextInput(attrs={'class':'input-data'}), label='Status')
    
    class Meta:
        model = Equipment
        fields = '__all__'