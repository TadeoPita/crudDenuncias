# Generated by Django 4.2.7 on 2024-06-18 00:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('denuncias', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='denuncia',
            name='documento_adjunto',
            field=models.FileField(blank=True, null=True, upload_to='documentos_adjuntos/'),
        ),
    ]
