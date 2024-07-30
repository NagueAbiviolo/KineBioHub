from django.db import models

class Ocupacao(models.Model):
    nome = models.CharField(max_length=30)
    class Meta:
        verrbose_name_plural = "Ocupações"
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
class Pessoa(models.Model):
    ocupacao = models.ForeignKey(Ocupacao, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    Masculino = "Masc"
    Feminino = "Fem"
    Outro = "Outro"
    gen = {
        Masculino: "Masculino",
        Feminino: "Feminino",
        Outro: "Outro",
    }
    genero = models. CharField(max_legth=5, choices = gen)
    email = models.CharField(max_length=50)
    telefone = models.CharField(max_length=30)
    senha = models.CharField(max_length=30)
    class Meta:
        verbose_name_plural = "Pessoas"
    def __str__(self):
        return self.nome

class Conteudo(models.Model):
    topico = models.ForeignKey(Topico, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=100)
    descricao = models.CharField()
    imagens = models.ImageField(upload_to='static/') 
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
class Pergunta(models.Model):
    questionario = models.ForeignKey(Questionario, on_delete=models.CASCADE)
    enunciado = models.CharField()
    class Meta:
        verbose_name_plural = "Perguntas"
    def __str__(self):
        return self.enunciado
class Alternativa(models.Model):
    enunciado = models.CharField()
    class Meta:
        verbose_name_plural = "Alternativas"
    def __str__(self):
        return self.enunciado                             
