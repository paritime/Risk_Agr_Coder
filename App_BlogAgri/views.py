from django.shortcuts import render
from App_BlogAgri.forms import *
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from App_BlogAgri.models import *
from django.shortcuts import render, get_object_or_404


# Create your views here.


def blog(request):
    """
Vista para listar las publicaciones de todos los usuarios del blog

    Parámetros:
        request (HttpRequest): La solicitud HTTP recibida por la vista.

    Returns:
        Render: En donde se devuelven todos las publicaciones que sean publicas (status_post=1)
    """

    Titulo = 'Blog RiskAgri'
    publicaciones = Post.objects.filter(status_post=1)
    return render(request, 'blog.html', {'posts': publicaciones, 'mensaje': Titulo})


@login_required(login_url='login')
def posts_user(request):
    """
Vista para listar las publicaciones unicamente que corresponden al usuario autentificado.

    Parámetros:
        request (HttpRequest): La solicitud HTTP recibida por la vista.

    Returns:
        Render: En donde se devuelven todos las publicaciones del usuario mediante el filtro del modelo
    """
    Titulo = f'Publicaciones'
    user = request.user
    publicaciones = Post.objects.filter(autor=user)
    return render(request, 'blog.html', {'posts': publicaciones, 'mensaje': Titulo})


def post(request, post_slug):
    """Vista para obtener el contexto que permita renderizar los elementos necesarios para el template de cada publicación

    Args:
        request (_type_): La solicitud HTTP recibida por la vista.
        post_slug (_type_): La variable slug que se define en el método save del modelo Post

    Returns:
       El objeto post para poder acceder a el en el template mediante jinja y el contenido dividio por párrafos

    """
    post = get_object_or_404(Post, slug=post_slug)
    # Dividir el contenido en párrafos basado en los saltos de línea
    paragraphs = post.contenido.split('\n')
    return render(request, 'post.html', {'post': post, 'paragraphs': paragraphs})


@login_required(login_url='login')
def create_post(request):
    """Vista para crear nuevas publicaciones

    Args:
        request (_type_): La solicitud HTTP recibida por la vista.

    Returns:
       Devuelve el formulario con la información del request.POST para poder guardar el registro en la base de datos. 

    """
    Titulo = 'Crea una publicación'
    if request.method == 'GET':
        return render(request, 'create_post.html', {
            'form': PostForm, 'mensaje': Titulo
        })
    else:
        try:
            form = PostForm(request.POST, files=request.FILES)
            # print(form.data)
            if form.is_valid():
                new_post = form.save(commit=False)
                new_post.autor = request.user
                new_post.save()
                return redirect('blog')
            else:
                # Si el formulario no es válido, se renderiza nuevamente la plantilla
                # create_post.html con el formulario y los errores
                return render(request, 'create_post.html', {'form': form, 'mensaje': Titulo})
        except:
            return render(request, 'create_post.html', {
                'form': PostForm,
                'error_message': 'Proporciona datos validos'
            })


def edit_post(request, post_id):
    """Genera  para renderizar un formulario que permita editar una publicación
    Args:
        request : La solicitud HTTP recibida por la vista.
        post_id : El id de cada objeto del modelo Post

    Returns:
        Devuelve el formulario con la instancia del objeto de la publicación y si es valido se actualiza con el método POST
    """
    post = get_object_or_404(Post, pk=post_id)
    confirmacion = 'Se actualizó la publicación'
    mensaje = 'Edición de Publicación'

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return render(request, 'editar_post.html', {'confirmacion': confirmacion, 'post': post})
        else:
            return render(request, 'editar_post.html', {'form': form, 'post': post})
    else:
        form = PostForm(instance=post)
        return render(request, 'editar_post.html', {'form': form, 'mensaje': mensaje, 'post': post})


def confirm_delete(request, post_id):
    """Genera un render con la confirmación para borrar un objeto

    Args:
        request : La solicitud HTTP recibida por la vista.
        post_id : El id de cada objeto del modelo Post

    Returns: Devuelve con método GET un render de confirmación para posteriormente borrar uin objeto del modelo Post

    """
    post = get_object_or_404(Post, pk=post_id)
    mensaje = 'Eliminar Publicación'

    if request.method == 'GET':
        return render(request, 'confirm_delete.html', {'mensaje': mensaje, 'post': post})


def delete_post(request, post_id):
    """Sirve para borrar un registro en el modelo Post

    Args:
        request : La solicitud HTTP recibida por la vista.
        post_id : El id de cada objeto del modelo Post

    Returns:
    No devuelve nada, se ejecuta en el template de confirm delete
    """
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('posts_user')
