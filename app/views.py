from django.shortcuts import render, redirect
from .models import *
from django.views import View
from django.contrib.auth import login
from .forms import RegisterForm, LoginForm
from django.contrib.auth.views import LoginView as AuthLoginView


class IndexView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "index.html")

    def post(self, request):
        pass


def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = RegisterForm()
    return render(request, "register.html", {"form": form})


class LoginView(AuthLoginView):
    template_name = "login.html"
    form_class = LoginForm

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super(LoginView, self).__init__(*args, **kwargs)

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        password = form.cleaned_data["password"]

        user = self.authenticate(self.request, username=email, password=password)
        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, "Email ou senha inválidos.")
            return self.form_invalid(form)