from django.shortcuts import render
from App_Usuarios.forms import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout as auth_logout
from django.db import IntegrityError
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
def registro(request):
    """
Vista para el registro de usuarios en RiskAgro.

    Parámetros:
        request (HttpRequest): La solicitud HTTP recibida por la vista.

    Returns:
        HttpResponse: Una respuesta HTTP que renderiza la plantilla 'signup.html' con un formulario de registro
                      o redirige al usuario a la página 'simulador' si el registro es exitoso.
    """
    if request.method == 'GET':
        Titulo = 'RiskAgro'
        return render(request, 'signup.html', {
            'form': CustomUserCreationForm, 'mensaje': Titulo
        })

    else:
        if request.POST['password1'] == request.POST['password2']:
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                try:
                    user = User.objects.create_user(
                        username=request.POST['username'], password=request.POST['password1'],
                        email=request.POST['email'], first_name=request.POST['nombres'], last_name=request.POST['apellidos'])
                    user.save()
                    login(request, user)
                    return redirect('simulador')
                except IntegrityError as e:
                    return render(request, 'signup.html',
                                  {'form': CustomUserCreationForm,
                                   'error_message': 'Este usuario ya se encuentra registrado', })
            else:
                return render(request, 'signup.html', {'form': form, })
        else:
            return render(request, 'signup.html',
                          {'form': CustomUserCreationForm,
                           'error_message': 'Contraseñas no coinciden',
                           })


def ingresar(request):
    """
Vista para iniciar sesión en RiskAgro.

    Parámetros:
        request (HttpRequest): La solicitud HTTP recibida por la vista.

    Returns:
        HttpResponse: Una respuesta HTTP que renderiza la plantilla 'signin.html' con un formulario de inicio de sesión
                      o redirige al usuario a la página 'simulador' si la autenticación es exitosa.
    """
    if request.method == 'GET':
        Titulo = 'RiskAgro'
        return render(request, 'login.html', {
            'form': AuthenticationForm, 'mensaje': Titulo,
        })
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        print(request.POST)
        if user is None:
            return render(request, 'login.html', {
                'form': AuthenticationForm,
                'error_message': 'El nombre de usuario o contraseña es incorrecto',

            })
        else:
            login(request, user)
            return redirect('blog')


def logout(request):
    """
Vista para cerrar sesión en RiskAgro.

    Parámetros:
        request (HttpRequest): La solicitud HTTP recibida por la vista.

    Returns:
        HttpResponseRedirect: Una respuesta HTTP que redirige al usuario a la página de inicio ('inicio').
    """
    auth_logout(request)
    return redirect('inicio')


@login_required(login_url='login')
def perfil(request):
    """Vista para edit información del perfil y mostrar template

    Args:
        request (HttpRequest): request (HttpRequest): La solicitud HTTP recibida por la vista.

    Returns:
        None: La vista mediante GET devuelve el foprmulario con la instancia del objeto de 
        usuario identificado por request.user. Para el método POST devuelve un mensaje de confirmación en caso de que el formulario sea valido y se ejecute
        el metodo save()
    """
    confirm = 'Se han actualizado los datos'
    user = request.user
    etiqueta = 'Inicio'
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            # Redirige a la URL del perfil
            return render(request, 'perfil.html', {'form': form, 'etiqueta': etiqueta, 'user': user, 'confirm': confirm})
    else:
        form = CustomUserChangeForm(instance=user, initial={
                                    'nombres': user.first_name, 'apellidos': user.last_name, 'user': user})

    return render(request, 'perfil.html', {'form': form, 'etiqueta': etiqueta, 'user': user})
