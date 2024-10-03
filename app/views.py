from django.shortcuts import render, get_object_or_404
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
@login_required(login_url="/auth/login/")
def add_conteudo(request):
    if request.method == "GET":
        disciplinas = Disciplina.objects.all()
        return render(request, "add_conteudo.html", {"disciplinas": disciplinas})
    else:
        disciplina_id = request.POST.get("disciplina")
        titulo = request.POST.get("titulo")
        descricao = request.POST.get("descricao")
        imagens = request.FILES.get("imagens")  # Captura o arquivo enviado

        conteudo = Conteudo.objects.filter(titulo=titulo).first()
        if conteudo:
            return HttpResponse("Já existe um conteúdo com esse título")
        disciplina = get_object_or_404(Disciplina, id=disciplina_id)
        conteudo = Conteudo.objects.create(
            disciplina=disciplina, titulo=titulo, descricao=descricao, imagens=imagens
        )
        return HttpResponse("Conteúdo criado com sucesso")


@login_required(login_url="/auth/login/")
def add_questionario(request):
    if request.method == "GET":
        conteudos = Conteudo.objects.all()
        return render(request, "add_questionario.html", {"conteudos": conteudos})

    else:
        conteudo_id = request.POST.get("conteudo")
        nome = request.POST.get("nome")
        enunciado = request.POST.get("enunciado")
        alternativas = [
            request.POST.get("alternativa_1"),
            request.POST.get("alternativa_2"),
            request.POST.get("alternativa_3"),
            request.POST.get("alternativa_4"),
        ]
        alternativa_correta_index = int(request.POST.get("alternativa_correta")) - 1

        # Verifique se já existe um questionário com esse nome
        if Questionario.objects.filter(nome=nome).exists():
            return HttpResponse("Já existe um questionário com esse nome")

        conteudo = get_object_or_404(Conteudo, id=conteudo_id)

        # Crie o questionário
        questionario = Questionario.objects.create(conteudo=conteudo, nome=nome)

        # Crie as alternativas
        alternativas_obj = []
        for alternativa in alternativas:
            alt = Alternativa.objects.create(enunciado=alternativa)
            alternativas_obj.append(alt)

        # Crie a pergunta
        pergunta = Pergunta.objects.create(
            questionario=questionario,
            enunciado=enunciado,
            alternativa_correta=alternativas_obj[alternativa_correta_index]
        )

        # Associe as alternativas à pergunta
        pergunta.alternativas.set(alternativas_obj)

        return HttpResponse("Questionário criado com sucesso com a pergunta.")



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
