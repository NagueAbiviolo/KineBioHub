from django.db import models
from django.core.exceptions import ValidationError


class Disciplina(models.Model):
    nome = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "Disciplinas"

    def __str__(self):
        return self.nome


class Conteudo(models.Model):
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, null=True)
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    imagens = models.ImageField(upload_to="imagens/", blank=True, null=True)

    class Meta:
        verbose_name_plural = "Conteúdos"

    def __str__(self):
        return self.titulo if self.titulo else "Titulo desconhecido"


class Questionario(models.Model):
    conteudo = models.ForeignKey(Conteudo, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Questionários"

    def __str__(self):
        return self.nome

    def add_pergunta(self, enunciado, alternativas, alternativa_correta):
        pergunta = Pergunta.objects.create(
            questionario=self,
            enunciado=enunciado,
            alternativa_correta=alternativa_correta,
        )
        pergunta.alternativas.set(alternativas)
        return pergunta


class Alternativa(models.Model):
    enunciado = models.TextField()

    class Meta:
        verbose_name_plural = "Alternativas"

    def __str__(self):
        return self.enunciado


class Pergunta(models.Model):
    questionario = models.ForeignKey(Questionario, on_delete=models.CASCADE)
    enunciado = models.TextField()
    alternativas = models.ManyToManyField(Alternativa, related_name="perguntas")
    alternativa_correta = models.ForeignKey(
        Alternativa, related_name="corretas", on_delete=models.CASCADE
    )

    class Meta:
        verbose_name_plural = "Perguntas"

    def __str__(self):
        return self.enunciado

    def clean(self):
        if self.alternativa_correta not in self.alternativas.all():
            raise ValidationError(
                "A alternativa correta não está entre as alternativas fornecidas."
            )

    def save(self, *args, **kwargs):
        self.clean()
        super(Pergunta, self).save(*args, **kwargs)
