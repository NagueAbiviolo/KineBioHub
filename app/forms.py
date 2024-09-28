from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Pessoa
from django.contrib.auth import authenticate

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Pessoa
        fields = ["email", "password1", "password2"]


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email', max_length=50)
    password = forms.CharField(label='Senha', widget=forms.PasswordInput)

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        user = authenticate(email=email, password=password)
        if user is None:
            raise forms.ValidationError('Email ou senha inválidos.')
        return self.cleaned_data
