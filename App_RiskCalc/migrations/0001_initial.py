# Generated by Django 5.0.2 on 2024-03-03 08:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Persona',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellido_paterno', models.CharField(max_length=100)),
                ('apellido_materno', models.CharField(max_length=100)),
                ('edad', models.PositiveIntegerField()),
                ('genero', models.CharField(choices=[('M', 'Masculino'), ('F', 'Femenino'), ('O', 'Otro')], max_length=1)),
                ('rfc', models.CharField(default=None, max_length=13)),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Paquete_Tec',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_cultivo', models.CharField(choices=[('maiz', 'Maíz'), ('frijol', 'Frijol'), ('arroz', 'Arroz'), ('cebada', 'Cebada'), ('trigo', 'Trigo'), ('soya', 'Soya')], max_length=20)),
                ('tecnologia_aplicada', models.CharField(choices=[('RA', 'Riego por Aspersión'), ('RG', 'Riego por Goteo'), ('TEMP', 'Temporal')], max_length=200)),
                ('rendimiento_promedio', models.FloatField()),
                ('hectareas', models.PositiveIntegerField()),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_RiskCalc.persona')),
            ],
        ),
        migrations.CreateModel(
            name='Ubicacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(choices=[('AGU', 'Aguascalientes'), ('BCN', 'Baja California'), ('BCS', 'Baja California Sur'), ('CAM', 'Campeche'), ('CHP', 'Chiapas'), ('CHH', 'Chihuahua'), ('CMX', 'Ciudad de México'), ('COA', 'Coahuila'), ('COL', 'Colima'), ('DUR', 'Durango'), ('GUA', 'Guanajuato'), ('GRO', 'Guerrero'), ('HID', 'Hidalgo'), ('JAL', 'Jalisco'), ('MEX', 'Estado de México'), ('MIC', 'Michoacán'), ('MOR', 'Morelos'), ('NAY', 'Nayarit'), ('NLE', 'Nuevo León'), ('OAX', 'Oaxaca'), ('PUE', 'Puebla'), ('QUE', 'Querétaro'), ('ROO', 'Quintana Roo'), ('SLP', 'San Luis Potosí'), ('SIN', 'Sinaloa'), ('SON', 'Sonora'), ('TAB', 'Tabasco'), ('TAM', 'Tamaulipas'), ('TLA', 'Tlaxcala'), ('VER', 'Veracruz'), ('YUC', 'Yucatán'), ('ZAC', 'Zacatecas')], max_length=3)),
                ('municipio', models.CharField(max_length=100)),
                ('persona', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App_RiskCalc.persona')),
            ],
        ),
    ]