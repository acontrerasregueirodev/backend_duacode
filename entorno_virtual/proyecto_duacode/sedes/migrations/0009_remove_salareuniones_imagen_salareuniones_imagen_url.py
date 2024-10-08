# Generated by Django 5.1.1 on 2024-10-08 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sedes', '0008_salareuniones_imagen'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='salareuniones',
            name='imagen',
        ),
        migrations.AddField(
            model_name='salareuniones',
            name='imagen_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
