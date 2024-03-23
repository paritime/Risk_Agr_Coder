from django.shortcuts import render
from App_RiskCalc.forms import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from App_RiskCalc.models import *

# Create your views here.


def inicio(request):
    """
Vista para la página de inicio de RiskAgro.

    Parámetros:
        request (HttpRequest): La solicitud HTTP recibida por la vista.

    Returns:
        HttpResponse: Una respuesta HTTP que renderiza la plantilla 'inicio.html' con un mensaje.

    """
    Titulo = 'RiskAgro'
    return render(request, 'inicio.html', {'mensaje': Titulo})


@login_required(login_url='login')
def reg_solicitante(request):
    """
Vista para registrar un solicitante de crédito en RiskAgro.

    Solo los usuarios autenticados pueden acceder a esta vista mediante la aplicación del decorador login_required.

    Parámetros:
        request (HttpRequest): La solicitud HTTP recibida por la vista.

    Returns:
        HttpResponseRedirect: Una respuesta HTTP que redirige al usuario a la página de consulta ('consulta') después
                                de registrar un solicitante correctamente.
        HttpResponse: Una respuesta HTTP que renderiza la plantilla 'reg_solicitante.html' con un formulario para
                      registrar un solicitante si la solicitud HTTP es GET, o renderiza el formulario con los errores
                      si la solicitud HTTP es POST y el formulario no es válido.
    """
    if request.method == 'GET':
        Titulo = 'RiskAgro'
        return render(request, 'reg_solicitante.html', {
            'form': PersonaForm, 'mensaje': Titulo
        })
    else:
        form = PersonaForm(request.POST)
        if form.is_valid():
            new_sol = form.save(commit=False)
            new_sol.user = request.user
            new_sol.save()
            return redirect('consulta')
        else:
            return render(request, 'reg_solicitante.html', {
                'form': form, })


@login_required(login_url='login')
def simulador(request):
    """
Vista para acceder al simulador en RiskAgro.

    Solo los usuarios autenticados pueden acceder a esta vista mediante la aplicación del decorador login_required.

    Parámetros:
        request (HttpRequest): La solicitud HTTP recibida por la vista.

    Returns:
        HttpResponse: Una respuesta HTTP que renderiza la plantilla 'simulador.html' con un mensaje si el usuario
                      está autenticado y tiene acceso al simulador.
    """
    Titulo2 = 'RiskAgro'
    return render(request, 'simulador.html', {'mensaje': Titulo2})


@login_required(login_url='login')
def reg_proy(request):
    """
Vista para registrar un proyecto en RiskAgro.

    Solo los usuarios autenticados pueden acceder a esta vista mediante la aplicación del decorador login_required.

    Parámetros:
        request (HttpRequest): La solicitud HTTP recibida por la vista.

    Returns:
        HttpResponseRedirect: Una respuesta HTTP que redirige al usuario a la página de consulta ('consulta') después
                                de registrar un proyecto correctamente.
        HttpResponse: Una respuesta HTTP que renderiza la plantilla 'reg_proy.html' con formularios para registrar un
                      paquete tecnológico y su ubicación si la solicitud HTTP es GET, o renderiza los formularios con
                      los errores si la solicitud HTTP es POST y los formularios no son válidos.
    """
    if request.method == 'GET':
        Titulo = 'RiskAgro'
        return render(request, 'reg_proy.html', {
            'formpaq': Paquete_TecForm, 'formubi': UbicacionForm, 'mensaje': Titulo
        })
    else:
        formpaq = Paquete_TecForm(request.POST)
        formubi = UbicacionForm(request.POST)

        if formpaq.is_valid() and formubi.is_valid:

            tecnologia_aplicada = formpaq.cleaned_data['tecnologia_aplicada']
            print(tecnologia_aplicada)
            hectareas = formpaq.cleaned_data['hectareas']
            print(hectareas)
            rendimiento_promedio = formpaq.cleaned_data['rendimiento_promedio']
            print(rendimiento_promedio)
            persona = formpaq.cleaned_data['persona']
            print(persona)

            # Generamos valores condicionales para riesgo, variable no definida en el formulario y que se calcula en el Backend
            riesgo = ''
            if tecnologia_aplicada == 'RA' and rendimiento_promedio >= 5:
                riesgo = 'Bajo'
            elif tecnologia_aplicada == 'RG' and rendimiento_promedio < 5:
                riesgo = 'Moderado'
            elif tecnologia_aplicada == 'TEMP' and rendimiento_promedio < 5:
                riesgo = 'Alto'
            else:
                riesgo = 'Bajo'
            print(riesgo)

            # Guardamos los datos del formulario de paquete tecnologico
            new_paq = formpaq.save(commit=False)
            new_paq.riesgo = riesgo  # Asignamos el riesgo calculado
            new_paq.save()  # Guardamos el objeto en la base de datos

            # Guardamos los datos del formulario de ubicacion
            '''Aqui definimos una instancia de paquete tec(new_paq) como valor de la variable new_ubi.paquete_tec de la nueva ubicacion, eso se debe
            a que paquete_tec se encuentra definida como una foreingkey del modelo y Django relaciona el objeto con la variable.  
            Para el caso de persona no hay problema por que tanto new_paq.persona como new_ubi.persona son instancias de Persona y sew definen en 
            formulario'''

            new_ubi = formubi.save(commit=False)
            new_ubi.paquete_tec = new_paq
            new_ubi.persona = new_paq.persona
            new_ubi.save()

            print('Registro exitoso')
            return redirect('consulta')

        else:
            return render(request, 'reg_proy.html', {
                'formpaq': formpaq, 'formubi': formubi})


@login_required(login_url='login')
def consulta(request):
    """
Vista para consultar información relacionada con una persona en RiskAgro.

    Solo los usuarios autenticados pueden acceder a esta vista mediante la aplicación del decorador login_required.

    Parámetros:
        request (HttpRequest): La solicitud HTTP recibida por la vista.

    Returns:
        HttpResponse: Una respuesta HTTP que renderiza la plantilla 'consulta.html' con formularios y datos relacionados
                      con una persona si la solicitud HTTP. Para el caso de GET, obtiene las personas solicitantes registradas por el usaurio,
                      para el caso de POST, obtiene los reigstros de los otros formularios. 
                      Si el User es identificado como administrador se mostraran todos los solicitantes (Personas), registrados por todos los 
                      uuarios. Esta lógica se encuentra definida en el formulario asociado a esta vista.
    """
    persona = None
    paquetes_tec = None
    ubicaciones = None

    if request.method == 'POST':
        Titulo = 'RiskAgro'
        form = ConsultaPersonaForm(request.user, request.POST)
        if form.is_valid():
            persona_id = form.cleaned_data['persona']
            persona = Persona.objects.get(pk=persona_id)

            # Filtrar Paquete_Tec y Ubicacion
            paquetes_tec = Paquete_Tec.objects.filter(persona=persona)
            ubicaciones = Ubicacion.objects.filter(persona=persona)

            return render(request, 'consulta.html', {'form': form, 'persona': persona, 'paquetes_tec': paquetes_tec, 'ubicaciones': ubicaciones, 'mensaje': Titulo})
    else:
        Titulo = 'RiskAgro'
        form = ConsultaPersonaForm(request.user)

    return render(request, 'consulta.html', {'form': form, 'persona': persona, 'paquetes_tec': paquetes_tec, 'ubicaciones': ubicaciones, 'mensaje': Titulo})
