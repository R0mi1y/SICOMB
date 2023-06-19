from django.contrib.auth.forms import UserCreationForm
from django import forms
from police.models import RegisterPolice
from django.contrib.auth.models import User
from django.forms import ClearableFileInput
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password


class UserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ['first_name', 'username', 'email']



class PoliceForm(forms.ModelForm):
    foto = forms.ImageField(widget=ClearableFileInput(attrs={'class':'file-input', 'accept':'image/*', 'onchange':'handleFileSelection(event)'}), label='Foto')

    class Meta:
        model = RegisterPolice
        fields = '__all__'
        widgets = {
            'nome': forms.TextInput(attrs={'class':'input-data'}),
            'matricula': forms.TextInput(attrs={'id':'matricula-input'}),
            'posto': forms.TextInput(attrs={'class':'input-data'}),
            'email': forms.EmailInput(attrs={'class':'input-data'}),
            'telefone': forms.TextInput(attrs={'class':'input-data'}),
            'lotacao': forms.TextInput(attrs={'class':'input-data'}),
            'senha': forms.PasswordInput(attrs={'class':'input-data', 'type':'password'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        senha_criptografada = make_password(self.cleaned_data['senha'])
        instance.senha = senha_criptografada

        if commit:
            instance.save()
        return instance
