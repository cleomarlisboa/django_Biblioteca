# Generated by Django 4.2 on 2023-05-05 18:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalogos', '0007_alter_livrofisico_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='livrofisico',
            options={'ordering': ['dataDevolucao'], 'permissions': (('fazer-devolucao', 'definir livro como devolvido'),)},
        ),
    ]
