<<<<<<< HEAD
# Generated by Django 5.1.1 on 2024-09-29 23:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_pessoa_groups_pessoa_user_permissions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pessoa',
            name='ocupacao',
        ),
        migrations.RemoveField(
            model_name='pessoa',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='pessoa',
            name='user_permissions',
        ),
        migrations.DeleteModel(
            name='Ocupacao',
        ),
        migrations.DeleteModel(
            name='Pessoa',
        ),
    ]
=======
# Generated by Django 5.1.1 on 2024-09-29 23:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_pessoa_groups_pessoa_user_permissions'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pessoa',
            name='ocupacao',
        ),
        migrations.RemoveField(
            model_name='pessoa',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='pessoa',
            name='user_permissions',
        ),
        migrations.DeleteModel(
            name='Ocupacao',
        ),
        migrations.DeleteModel(
            name='Pessoa',
        ),
    ]
>>>>>>> c513ced (Primeio commit)
