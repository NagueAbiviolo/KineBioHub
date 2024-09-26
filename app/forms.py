from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from .models import Pessoa


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = Pessoa
        fields = ["email", "password1", "password2"]


class LoginForm(AuthenticationForm):
<<<<<<< HEAD
    email = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput, label='Senha')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(LoginForm, self).__init__(*args, **kwargs)
=======
    email = forms.EmailField(label="Email", max_length=254)
    password = forms.CharField(label="Senha", widget=forms.PasswordInput)
>>>>>>> 5c8965bd859e96575eed6184d308810fb4f113c1
