from django.shortcuts import render, redirect, get_object_or_404
from .models import *
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "index.html")

    def post(self, request):
        pass


@user_passes_test(lambda user: user.is_staff, login_url="/auth/login/")
def gerenciar_conteudos(request):
    conteudos = Conteudo.objects.all()
    return render(request, "gerenciar_conteudos.html", {"conteudos": conteudos})


@user_passes_test(lambda user: user.is_staff, login_url="/auth/login/")
def add_conteudo(request):
    if request.method == "GET":
        disciplinas = Disciplina.objects.all()
        return render(request, "add_conteudo.html", {"disciplinas": disciplinas})
    else:
        disciplina_id = request.POST.get("disciplina")
        titulo = request.POST.get("titulo")
        descricao = request.POST.get("descricao")
        imagens = request.FILES.get("imagens")

        conteudo = Conteudo.objects.filter(titulo=titulo).first()
        if conteudo:
            return HttpResponse("Já existe um conteúdo com esse título")
        disciplina = get_object_or_404(Disciplina, id=disciplina_id)
        conteudo = Conteudo.objects.create(
            disciplina=disciplina, titulo=titulo, descricao=descricao, imagens=imagens
        )
        return HttpResponse("Conteúdo criado com sucesso")


@user_passes_test(lambda user: user.is_staff, login_url="/auth/login/")
def editar_conteudo(request, conteudo_id):
    conteudo = get_object_or_404(Conteudo, id=conteudo_id)

    if request.method == "POST":
        conteudo.titulo = request.POST.get("titulo")
        conteudo.descricao = request.POST.get("descricao")

        disciplina_id = request.POST.get("disciplina")
        if disciplina_id:
            conteudo.disciplina = get_object_or_404(Disciplina, id=disciplina_id)

        if request.FILES.get("imagens"):
            conteudo.imagens = request.FILES.get("imagens")

        conteudo.save()
        messages.success(request, "Conteúdo atualizado com sucesso")
        return redirect("gerenciar_conteudos")

    disciplinas = Disciplina.objects.all()
    return render(
        request,
        "editar_conteudo.html",
        {"conteudo": conteudo, "disciplinas": disciplinas},
    )


@user_passes_test(lambda user: user.is_staff, login_url="/auth/login/")
def deletar_conteudo(request, conteudo_id):
    conteudo = get_object_or_404(Conteudo, id=conteudo_id)
    conteudo.delete()
    messages.success(request, "Conteúdo deletado com sucesso")
    return redirect("gerenciar_conteudos")


@user_passes_test(lambda user: user.is_staff, login_url="/auth/login/")
def add_questionario(request):
    if request.method == "POST":
        conteudo_id = request.POST.get("conteudo")
        nome_questionario = request.POST.get("nome")

        conteudo = Conteudo.objects.get(id=conteudo_id)
        questionario = Questionario.objects.create(
            conteudo=conteudo, nome=nome_questionario
        )

        for i in range(int(request.POST.get("numero_perguntas"))):
            enunciado = request.POST.get(f"pergunta_{i}")
            pergunta = Pergunta.objects.create(
                questionario=questionario, enunciado=enunciado
            )

            for j in range(4):
                enunciado_alt = request.POST.get(f"alternativa_{i}_{j}")
                alternativa = Alternativa.objects.create(enunciado=enunciado_alt)
                pergunta.alternativas.add(alternativa)

                if request.POST.get(f"correta_{i}") == str(j):
                    pergunta.alternativa_correta = alternativa

            pergunta.save()

        return redirect("home")

    conteudos = Conteudo.objects.all()
    return render(request, "add_questionario.html", {"conteudos": conteudos})


@user_passes_test(lambda user: user.is_staff, login_url="/auth/login/")
def gerenciar_questionarios(request):
    questionarios = Questionario.objects.all()

    if request.method == "POST":
        questionario_id = request.POST.get("delete")
        if questionario_id:
            questionario = get_object_or_404(Questionario, id=questionario_id)
            questionario.delete()
            return redirect("gerenciar_questionarios")

    return render(
        request, "gerenciar_questionarios.html", {"questionarios": questionarios}
    )


@user_passes_test(lambda user: user.is_staff, login_url="/auth/login/")
def editar_questionario(request, questionario_id):
    questionario = get_object_or_404(Questionario, id=questionario_id)
    perguntas = questionario.pergunta_set.all()

    if request.method == "POST":
        nome = request.POST.get("nome")
        conteudo_id = request.POST.get("conteudo")

        if nome and conteudo_id:
            questionario.nome = nome
            questionario.conteudo_id = conteudo_id
            questionario.save()

            for i in range(len(perguntas)):
                pergunta_id = request.POST.get(f"pergunta_id_{i}")
                enunciado_pergunta = request.POST.get(f"pergunta_{i}")

                pergunta = Pergunta.objects.get(id=pergunta_id)
                pergunta.enunciado = enunciado_pergunta
                pergunta.save()

                for j in range(4):
                    alternativa_id = request.POST.get(f"alternativa_id_{i}_{j}")
                    enunciado_alternativa = request.POST.get(f"alternativa_{i}_{j}")

                    if alternativa_id:
                        alternativa = Alternativa.objects.get(id=alternativa_id)
                        if enunciado_alternativa:
                            alternativa.enunciado = enunciado_alternativa
                            alternativa.save()
                    else:
                        if enunciado_alternativa:
                            alternativa = Alternativa.objects.create(
                                enunciado=enunciado_alternativa
                            )
                            pergunta.alternativas.add(alternativa)

                alternativa_correta_id = request.POST.get(f"correta_{i}")
                if alternativa_correta_id:
                    alternativa_correta = Alternativa.objects.get(
                        id=alternativa_correta_id
                    )
                    pergunta.alternativa_correta = alternativa_correta
                else:
                    pergunta.alternativa_correta = None
                pergunta.save()

            return redirect("gerenciar_questionarios")

        else:
            messages.error(request, "Erro: Nome ou conteúdo não pode ser nulo")

    conteudos = Conteudo.objects.all()
    return render(
        request,
        "editar_questionario.html",
        {
            "questionario": questionario,
            "conteudos": conteudos,
            "perguntas": perguntas,
        },
    )


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

        return HttpResponseRedirect(reverse("login"))


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

        pontuacao = (corretas / total) * 100 if total > 0 else 0

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


def contato(request):
    if request.method == "POST":
        nome = request.POST.get("name")
        email = request.POST.get("email")
        mensagem = request.POST.get("message")

        subject = f"Contato de {nome}"
        message = f"Nome: {nome}\nE-mail: {email}\nMensagem:\n{mensagem}"

        try:
            send_mail(
                subject, message, settings.EMAIL_HOST_USER, [settings.EMAIL_HOST_USER]
            )
            messages.success(request, "Mensagem enviada com sucesso!")
        except Exception as e:
            messages.error(
                request, "Erro ao enviar a mensagem. Tente novamente mais tarde."
            )

        return redirect("contato")

    return render(request, "contato.html")
