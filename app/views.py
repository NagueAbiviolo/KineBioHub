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

@login_required(login_url="/auth/login/")
def add_conteudo(request):
    if request.method == "GET":
        return render(request, "add_conteudo.html")
    else:
        titulo = request.POST.get("titulo")
        descricao = request.POST.get("descricao")
        imagens = request.POST.get("imagens")
        conteudo = Conteudo.objects.filter(titulo=titulo).first()
        if conteudo:
            return HttpResponse("Já existe um conteudo com esse título")
        conteudo=Conteudo.objects.create(titulo=titulo, descricao=descricao, imagens=imagens)
        conteudo.save()
        return HttpResponse("Foi")    
@login_required(login_url="/auth/login/")
def add_questionario(request):
    
    if request.method == "GET":
        conteudos = Conteudo.objects.all()
        return render(request, "add_questionario.html",  {'conteudos': conteudos})
    
    else:
        conteudo = request.POST.get("conteudo")
        nome =  request.POST.get("nome")
        questionario = Questionario.objects.filter(nome=nome).first()
        if questionario:
            return HttpResponse("Já existe um questionario com esse nome")
        questionario = Questionario.objects.create(conteudo=conteudo, nome=nome)
        questionario.save()
        return HttpResponse("Foi")        
        

def cadastro(request):
    if request.method == "GET":
        return render(request, "cadastro.html")
    else:
        username = request.POST.get("username")
        email = request.POST.get("email")
        senha = request.POST.get("senha")
        user = User.objects.filter(username=username).first()
        if user:
            return HttpResponse("Já existe um usuário com esse username")
        user = User.objects.create_user(username=username, email=email, password=senha)
        user.save()

        return HttpResponse("Usuário cadastrado com sucesso")


def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        username = request.POST.get("username")
        senha = request.POST.get("senha")
    user = authenticate(username=username, password=senha)
    if user:
        login_django(request, user)
        return HttpResponseRedirect(reverse("home"))
    else:
        return HttpResponse("Usuário ou senha inválidos")


def logout(request):
    logout_django(request)
    return HttpResponseRedirect(reverse("index"))


@login_required(login_url="/auth/login/")
def home(request):
    return render(request, "home.html")
