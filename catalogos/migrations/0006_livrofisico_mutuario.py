# Generated by Django 4.2 on 2023-05-05 13:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalogos', '0005_rename_imprimir_livrofisico_publicacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='livrofisico',
            name='mutuario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
