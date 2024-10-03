# Generated by Django 5.1.1 on 2024-10-03 08:19

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sedes', '0006_remove_sede_ciudad_remove_sede_pais_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sede',
            name='ciudad',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='sede',
            name='pais',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterModelTable(
            name='sede',
            table=None,
        ),
    ]
