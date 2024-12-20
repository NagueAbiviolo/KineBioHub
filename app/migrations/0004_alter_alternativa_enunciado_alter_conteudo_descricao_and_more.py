# Generated by Django 5.1.1 on 2024-09-29 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_remove_pessoa_ocupacao_remove_pessoa_groups_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alternativa',
            name='enunciado',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='conteudo',
            name='descricao',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='conteudo',
            name='imagens',
            field=models.ImageField(blank=True, null=True, upload_to='imagens/'),
        ),
        migrations.AlterField(
            model_name='pergunta',
            name='enunciado',
            field=models.TextField(),
        ),
    ]
