# Generated by Django 5.1.1 on 2024-10-07 16:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sedes', '0007_sede_ciudad_sede_pais_alter_sede_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='salareuniones',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='salas_reuniones/'),
        ),
    ]
