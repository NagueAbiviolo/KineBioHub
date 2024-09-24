from django.contrib.auth.backends import BaseBackend
from .models import Pessoa  # Ajuste o caminho de importação conforme necessário
from django.contrib.auth.hashers import check_password

class CustomAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # O username aqui é o email
            pessoa = Pessoa.objects.get(email=username)
            if check_password(password, pessoa.password):  # Verifica a senha
                return pessoa
        except Pessoa.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Pessoa.objects.get(pk=user_id)
        except Pessoa.DoesNotExist:
            return None