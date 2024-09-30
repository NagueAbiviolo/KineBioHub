from django.shortcuts import render
from .models import *
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse

class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "index.html")

    def post(self, request):
        pass


def cadastro(request):
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        user = User.objects.filter(username=username).first()
        if user:
            return HttpResponse('Já existe um usuário com esse username')
        user =  User.objects.create_user(username=username, email=email, password=senha)
        user.save()

        return HttpResponse('Usuário cadastrado com sucesso')

def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')
    user = authenticate(username=username, password=senha)
    if user:
        login_django(request, user)
        return HttpResponseRedirect(reverse('home'))
    else:
        return HttpResponse('Usuário ou senha inválidos')
def logout(request):
    logout_django(request)
    return HttpResponseRedirect(reverse('index'))            
@login_required(login_url="/auth/login/")
def home(request):
    return render(request, 'home.html')
    