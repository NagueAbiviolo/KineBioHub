from django.urls import path
from . import views

urlpatterns = [
    path("cadastro/", views.cadastro, name="cadastro"),
    path("login/", views.login, name="login"),
    path("home/", views.home, name="home"),
    path("logout/", views.logout, name="logout"),
    path("add_conteudo/", views.add_conteudo, name="add_conteudo"),
    path("add_questionario/", views.add_questionario, name="add_questionario"),
    path("anatomia_funcional/", views.anatomia_funcional, name="anatomia_funcional"),
    path(
        "fisiologia_exercicio/", views.fisiologia_exercicio, name="fisiologia_exercicio"
    ),
    path("biomecanica/", views.biomecanica, name="biomecanica"),
    path("controle_motor/", views.controle_motor, name="controle_motor"),
    path(
        "cinesiologia_clinica/", views.cinesiologia_clinica, name="cinesiologia_clinica"
    ),
    path("analise_movimento/", views.analise_movimento, name="analise_movimento"),
    path(
        "conteudo/<int:conteudo_id>/", views.detalhe_conteudo, name="detalhe_conteudo"
    ),
    path(
        "questionario/<int:questionario_id>/",
        views.realizar_questionario,
        name="realizar_questionario",
    ),
]
