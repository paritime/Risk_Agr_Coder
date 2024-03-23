from django import forms
from App_RiskCalc.models import Persona, Ubicacion, Paquete_Tec
from django.shortcuts import redirect


class PersonaForm(forms.ModelForm):
    class Meta:
        model = Persona
        fields = ['nombre', 'apellido_paterno',
                  'apellido_materno', 'edad', 'genero', 'rfc']

    #  validaciones personalizadas para pass
    def clean_rfc(self):
        rfc = self.cleaned_data.get('rfc')

        if Persona.objects.filter(rfc=rfc).exists():
            raise forms.ValidationError(
                "El RFC de este solicitante ya se encuentra registrado")

        if len(rfc) < 12:
            raise forms.ValidationError(
                "El RFC es demasiado corto, ingresa al menos 12 caracteres")

        return rfc

    def clean_edad(self):

        edad = self.cleaned_data.get('edad')
        if edad < 18 or edad > 110:
            raise forms.ValidationError(
                "Parece que hay un problema con la edad: debe ser mayor a 18 años o la edad es invalida")
        return edad


class UbicacionForm(forms.ModelForm):
    class Meta:
        model = Ubicacion
        fields = ['estado', 'municipio']


class Paquete_TecForm(forms.ModelForm):
    class Meta:
        model = Paquete_Tec
        fields = ['nombre_cultivo', 'tecnologia_aplicada',
                  'rendimiento_promedio', 'hectareas', 'persona']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            # Para mostrar en el formulario todos los usuarios registrados
            self.fields['persona'].queryset = Persona.objects.all()
        except Exception as e:
            print("Error en la inicialización del formulario:", str(e))
            redirect('regsol')


class ConsultaPersonaForm(forms.Form):
    # Para crear una instancia cada vez que se inicia el formulario y recopilar los datos. Tambien para poderle pasar el request.user y que vea sus atributos
    def __init__(self, user, *args, **kwargs):
        super(ConsultaPersonaForm, self).__init__(*args, **kwargs)

        if user.is_superuser:
            # Si es un superusuario van todas las personas
            personas = Persona.objects.all()
        else:
            # Si no filtrar por usuario
            personas = Persona.objects.filter(user=user)

        # Utilizamos una función lambda para obtener las personas en el momento en que se crea el formulario
        choices = [(persona.id, str(persona))
                   for persona in personas]

        self.fields['persona'] = forms.ChoiceField(
            choices=choices, label='Selecciona una solicitante registrado')
