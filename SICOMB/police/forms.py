from django.contrib.auth.forms import UserCreationForm
from django import forms
from police.models import Police
from django.contrib.auth.models import User
from django.forms import ClearableFileInput
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password


class PoliceForm(forms.ModelForm):
    image_path = forms.ImageField(widget=ClearableFileInput(attrs={'class':'file-input', 'accept':'image/*', 'onchange':'handleFileSelection(event)'}), label='Foto')

    class Meta:
        model = Police
        fields = [
            'name',
            'matricula',
            'posto',
            'email',
            'telefone',
            'lotacao',
            'password',
            'image_path'
        ]
        
        widgets = {
            'name': forms.TextInput(attrs={'class':'input-data', "required": True}),
            'matricula': forms.TextInput(attrs={'id':'matricula-input'}),
            'posto': forms.TextInput(attrs={'class':'input-data'}),
            'email': forms.EmailInput(attrs={'class':'input-data'}),
            'telefone': forms.TextInput(attrs={'class':'input-data'}),
            'lotacao': forms.TextInput(attrs={'class':'input-data'}),
            'password': forms.PasswordInput(attrs={'class':'input-data'}),
        }

    def clean_password(self):
        data = self.cleaned_data["password"]
        password = make_password(data)
        return password
    
