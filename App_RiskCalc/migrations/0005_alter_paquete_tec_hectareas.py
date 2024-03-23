# Generated by Django 5.0.2 on 2024-03-05 08:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_RiskCalc', '0004_alter_paquete_tec_rendimiento_promedio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='paquete_tec',
            name='hectareas',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
