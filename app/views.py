from django.shortcuts import render, redirect, get_object_or_404
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
    if request.method == "POST":
        conteudo_id = request.POST.get("conteudo")
        nome_questionario = request.POST.get("nome")

        conteudo = Conteudo.objects.get(id=conteudo_id)
        questionario = Questionario.objects.create(
            conteudo=conteudo, nome=nome_questionario
        )

        # Criar perguntas e alternativas
        for i in range(int(request.POST.get("numero_perguntas"))):
            enunciado = request.POST.get(f"pergunta_{i}")
            pergunta = Pergunta.objects.create(
                questionario=questionario, enunciado=enunciado
            )

            # Criar alternativas
            for j in range(4):  # Supondo 4 alternativas
                enunciado_alt = request.POST.get(f"alternativa_{i}_{j}")
                alternativa = Alternativa.objects.create(enunciado=enunciado_alt)
                pergunta.alternativas.add(alternativa)

                # Verifica se é a alternativa correta
                if request.POST.get(f"correta_{i}") == str(j):
                    pergunta.alternativa_correta = alternativa

            pergunta.save()

        return redirect("home")

    conteudos = Conteudo.objects.all()
    return render(request, "add_questionario.html", {"conteudos": conteudos})


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


def anatomia_funcional(request):
    disciplina = get_object_or_404(Disciplina, nome="Anatomia Funcional")
    conteudos = Conteudo.objects.filter(disciplina=disciplina)
    return render(request, "anatomia_funcional.html", {"conteudos": conteudos})


def fisiologia_exercicio(request):
    disciplina = get_object_or_404(Disciplina, nome="Fisiologia do Exercício")
    conteudos = Conteudo.objects.filter(disciplina=disciplina)
    return render(request, "fisiologia_exercicio.html", {"conteudos": conteudos})


def biomecanica(request):
    disciplina = get_object_or_404(Disciplina, nome="Biomecânica")
    conteudos = Conteudo.objects.filter(disciplina=disciplina)
    return render(request, "biomecanica.html", {"conteudos": conteudos})


def controle_motor(request):
    disciplina = get_object_or_404(Disciplina, nome="Controle Motor")
    conteudos = Conteudo.objects.filter(disciplina=disciplina)
    return render(request, "controle_motor.html", {"conteudos": conteudos})


def cinesiologia_clinica(request):
    disciplina = get_object_or_404(Disciplina, nome="Cinesiologia Clínica")
    conteudos = Conteudo.objects.filter(disciplina=disciplina)
    return render(request, "cinesiologia_clinica.html", {"conteudos": conteudos})


def analise_movimento(request):
    disciplina = get_object_or_404(Disciplina, nome="Análise do Movimento")
    conteudos = Conteudo.objects.filter(disciplina=disciplina)
    return render(request, "analise_movimento.html", {"conteudos": conteudos})


def detalhe_conteudo(request, conteudo_id):
    conteudo = get_object_or_404(Conteudo, id=conteudo_id)
    questionarios = Questionario.objects.filter(conteudo=conteudo)

    return render(
        request,
        "detalhe_conteudo.html",
        {"conteudo": conteudo, "questionarios": questionarios},
    )


from django.shortcuts import render, get_object_or_404
from .models import Questionario, Pergunta, Alternativa


@login_required(login_url="/auth/login/")
def realizar_questionario(request, questionario_id):
    questionario = get_object_or_404(Questionario, id=questionario_id)
    perguntas = Pergunta.objects.filter(questionario=questionario)

    if request.method == "POST":
        corretas = 0
        total = perguntas.count()

        for pergunta in perguntas:
            resposta_id = request.POST.get(f"resposta_{pergunta.id}")
            if resposta_id:
                resposta = get_object_or_404(Alternativa, id=resposta_id)
                if resposta == pergunta.alternativa_correta:
                    corretas += 1

        # Calcular a pontuação
        pontuacao = (corretas / total) * 100 if total > 0 else 0

        # Retornar uma resposta com os resultados
        return render(
            request,
            "resultado_questionario.html",
            {
                "pontuacao": pontuacao,
                "total": total,
                "corretas": corretas,
            },
        )

    return render(
        request,
        "realizar_questionario.html",
        {
            "questionario": questionario,
            "perguntas": perguntas,
        },
    )
