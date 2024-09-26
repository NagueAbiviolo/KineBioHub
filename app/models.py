from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group,
    Permission
)


class PessoaManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O email deve ser fornecido")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  # Armazena a senha como hash
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class Ocupacao(models.Model):
    nome = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "Ocupações"

    def __str__(self):
        return self.nome


class Disciplina(models.Model):
    nome = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "Disciplinas"

    def __str__(self):
        return self.nome


class Topico(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    nome = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "Tópicos"

    def __str__(self):
        return self.nome


class Pessoa(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=50, unique=True)
    password = models.CharField(max_length=128)
    ocupacao = models.ForeignKey(
        "Ocupacao", on_delete=models.CASCADE, null=True, blank=True
    )
    datanasc = models.DateField(null=True, blank=True)

    Masculino = "Masc"
    Feminino = "Fem"
    Outro = "Outro"
    GEN_CHOICES = [
        (Masculino, "Masculino"),
        (Feminino, "Feminino"),
        (Outro, "Outro"),
    ]
    genero = models.CharField(max_length=5, choices=GEN_CHOICES, null=True, blank=True)
    telefone = models.CharField(max_length=30, null=True, blank=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    last_login = models.DateTimeField(null=True, blank=True)

    # Define o manager customizado
    objects = PessoaManager()

    # Define que o login será feito com email
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    groups = models.ManyToManyField(
        Group,
        verbose_name=("groups"),
        blank=True,
        help_text=(
            "The groups this user belongs to. A user will get all permissions granted to each of their groups."
        ),
        related_name="pessoa_set",
        related_query_name="pessoa",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=("user permissions"),
        blank=True,
        help_text=("Specific permissions for this user."),
        related_name="pessoa_set",
    )

    def save(self, *args, **kwargs):
        # Hash a senha antes de salvar
        if self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Pessoas"

    def __str__(self):
        return self.email


class Conteudo(models.Model):
    topico = models.ForeignKey(Topico, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descricao = models.CharField(max_length=1000)
    imagens = models.ImageField(
        upload_to="imagens/"
    )  # Ajuste o caminho para o upload de imagens

    class Meta:
        verbose_name_plural = "Conteúdos"

    def __str__(self):
        return self.titulo


class Questionario(models.Model):
    conteudo = models.ForeignKey(Conteudo, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Questionários"

    def __str__(self):
        return self.nome


class Alternativa(models.Model):
    enunciado = models.CharField(max_length=1000)

    class Meta:
        verbose_name_plural = "Alternativas"

    def __str__(self):
        return self.enunciado


class Pergunta(models.Model):
    questionario = models.ForeignKey(Questionario, on_delete=models.CASCADE)
    enunciado = models.CharField(max_length=1000)
    alternativas = models.ManyToManyField(Alternativa, related_name="perguntas")
    alternativa_correta = models.ForeignKey(
        Alternativa, related_name="corretas", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = "Perguntas"

    def __str__(self):
        return self.enunciado
