from django import forms
from django.contrib.auth.models import User
from .models import Profile

# Formulario de autenticación de usuarios
class LoginForm(forms.Form):
    username = forms.CharField(
        label='Nombre de usuario',
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa tu usuario o dirección de correo'
            }
        )
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Ingresa tu contraseña'
            }
        )
    )

class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('photo', 'phone_number')