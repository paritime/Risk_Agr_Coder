# Generated by Django 5.0.2 on 2024-03-05 07:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App_RiskCalc', '0002_paquete_tec_riesgo'),
    ]

    operations = [
        migrations.AddField(
            model_name='ubicacion',
            name='paquete_tec',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='App_RiskCalc.paquete_tec'),
        ),
    ]
