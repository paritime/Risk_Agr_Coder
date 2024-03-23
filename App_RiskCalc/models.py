from django.db import models
from App_RiskCalc.choices import *
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
# Create your models here.


class Persona(models.Model):
    """
 Modelo que representa una persona que solicita un crédito en el sector agroalimentario.

    Atributos:
        nombre (str): El nombre de la persona.
        apellido_paterno (str): El apellido paterno de la persona.
        apellido_materno (str): El apellido materno de la persona.
        edad (int): La edad de la persona.
        genero (str): El género de la persona. Puede ser 'M' para masculino o 'F' para femenino.
        rfc (str): El Registro Federal de Contribuyentes (RFC) de la persona que se utiliza en Mexico para identificación.
        user (User): El usuario registrado que crea el registro de la persona.

    Métodos:
        __str__: Retorna una representación de cadena de la persona en el formato "nombre apellido_paterno apellido_materno".
    """
    nombre = models.CharField(max_length=100)
    apellido_paterno = models.CharField(max_length=100)
    apellido_materno = models.CharField(max_length=100)
    edad = models.PositiveIntegerField()
    genero = models.CharField(
        max_length=1, choices=genero_choices)
    rfc = models.CharField(max_length=13,
                           null=False, blank=False, default=None, verbose_name='RFC')
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno}"


class Paquete_Tec(models.Model):
    """
Modelo que representa un paquete tecnológico para un cultivo.

    Atributos:
        nombre_cultivo (str): El nombre del cultivo al que se aplica el paquete tecnológico.
        tecnologia_aplicada (str): La tecnología aplicada para el cultivo.
        rendimiento_promedio (Decimal): El rendimiento promedio que ha reportado el productor.
        hectareas (Decimal): La cantidad de hectáreas en las que se aplica el paquete tecnológico.
        riesgo (str): El nivel de riesgo asociado al paquete tecnológico.
        persona (Persona): La persona que solicita un credito asociada con el paquete tecnológico.

    Métodos:
        __str__: Retorna una representación de cadena del paquete tecnológico.
    """
    nombre_cultivo = models.CharField(
        max_length=20, choices=cultivo_choices)
    tecnologia_aplicada = models.CharField(
        max_length=200, choices=tecnologia_choices)
    rendimiento_promedio = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    hectareas = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    riesgo = models.CharField(
        max_length=200, choices=riesgo_choices, default=None)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)

    def __str__(self):
        return fr'Cultivo de {self.nombre_cultivo}, con un rendimiento promedio de {self.rendimiento_promedio} en {self.hectareas} ha, aplicando {self.tecnologia_aplicada}'


class Ubicacion(models.Model):
    """
Modelo que representa la ubicación de un paquete tecnológico.

    Atributos:
        estado (str): El estado de México donde se ubica el paquete tecnológico.
        municipio (str): El municipio donde se ubica el paquete tecnológico.
        persona (Persona): La persona que solicita el credito asociada con la ubicación del paquete tecnológico.
        paquete_tec (Paquete_Tec): El paquete tecnológico asociado con la ubicación.

    Métodos:
        __str__: Retorna una representación de cadena de la ubicación en el formato "municipio, estado".
    """
    estado = models.CharField(
        max_length=3, choices=estado_choices)
    municipio = models.CharField(max_length=100)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    paquete_tec = models.ForeignKey(
        Paquete_Tec, on_delete=models.CASCADE, default=None)

    def __str__(self):
        return f"{self.municipio}, {self.estado}"
