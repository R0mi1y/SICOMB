from django import forms
from load.models import Load


class LoadForm(forms.ModelForm):
    date_load = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class':''}), label='Data da Carga')
    
    class Meta:
        model = Load
        fields = '__all__'