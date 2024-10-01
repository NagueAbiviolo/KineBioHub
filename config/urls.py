

from django.contrib import admin
from django.urls import path, include
from app.views import *
from django.views.generic import TemplateView
from app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", IndexView.as_view(), name="index"),
    path('auth/', include('app.urls'))
]