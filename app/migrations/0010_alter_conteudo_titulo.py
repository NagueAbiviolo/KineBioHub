# Generated by Django 5.1.1 on 2024-10-03 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_alter_conteudo_titulo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conteudo',
            name='titulo',
            field=models.CharField(max_length=100, null=True),
        ),
    ]