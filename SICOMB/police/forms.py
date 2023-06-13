from django.contrib.auth.forms import UserCreationForm
from django import forms
from police.models import RegisterPolice
from django.contrib.auth.models import User
from django.forms import ClearableFileInput
from django.utils.translation import gettext_lazy as _


class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'username', 'email']


class PoliceForm(forms.ModelForm):
    
    # nome = forms.CharField( label='Nome')
    # sobrenome = forms.CharField(widget=forms.TextInput(attrs={'class':'input-data'}), label='Sobrenome')
    matricula = forms.CharField(widget=forms.TextInput(attrs={'class':'input-data'}), label='Matrícula')
    posto = forms.CharField(widget=forms.TextInput(attrs={'class':'input-data'}), label='Posto')
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'input-data'}), label='Email')
    telefone = forms.CharField(widget=forms.TextInput(attrs={'class':'input-data'}), label='Telefone')
    lotacao = forms.CharField(widget=forms.TextInput(attrs={'class':'input-data'}), label='Lotação')
    foto = forms.ImageField(widget=ClearableFileInput(attrs={'class':'file-input', 'accept':'image/*', 'onchange':'handleFileSelection(event)'}), label='Foto')
    # foto = forms.ImageField(widget=forms.FileInput(attrs={'class':'file-input', 'accept':'image/*', 'onchange':'handleFileSelection(event)'}), label='Foto')
    
    class Meta:
        model = RegisterPolice
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class':'input-data'})
        }
        
