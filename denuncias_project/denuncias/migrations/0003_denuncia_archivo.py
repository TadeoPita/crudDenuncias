# Generated by Django 4.2.7 on 2024-06-18 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('denuncias', '0002_denuncia_documento_adjunto'),
    ]

    operations = [
        migrations.AddField(
            model_name='denuncia',
            name='archivo',
            field=models.FileField(blank=True, null=True, upload_to='archivos_denuncias/'),
        ),
    ]
