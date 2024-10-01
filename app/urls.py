from django.urls import path
from . import views
urlpatterns = [
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/',  views.login, name='login'),
    path('home/',  views.home, name='home'),
    path('logout/', views.logout, name='logout'),
    path("add_conteudo/", views.add_conteudo, name='add_conteudo'),
    path("add_questionario/", views.add_questionario, name='add_questionario')

]