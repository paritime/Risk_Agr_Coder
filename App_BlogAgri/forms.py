from django import forms
from App_BlogAgri.models import Post
from App_BlogAgri.choices import *


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'contenido',
                  'tema_post', 'imagen', 'status_post',]

    #  validaciones personalizadas para post
    def clean_titulo(self):
        titulo = self.cleaned_data.get('titulo')
        if not titulo:
            raise forms.ValidationError("Se tiene que ingresar un título")

        # Si es una edición y el título no ha cambiado, no es necesario realizar la validación
        if self.instance and self.instance.pk:
            if self.instance.titulo == titulo:
                return titulo

        # Verifica si el título ya existe en otras publicaciones
        if Post.objects.filter(titulo=titulo).exists():
            raise forms.ValidationError(
                "Ya existe una publicación con este título, selecciona otro título.")

        return titulo

    def clean_contenido(self):
        contenido = self.cleaned_data.get('contenido')
        if len(contenido) < 100:  # Establece el mínimo a 100 caracteres
            raise forms.ValidationError(
                "El contenido debe tener al menos 100 caracteres.")
        return contenido

    def clean_status_post(self):
        status_post = self.cleaned_data.get('status_post')
        if status_post is None:
            raise forms.ValidationError(
                "Debe seleccionar un estado para el post.")
        return status_post

    def clean_tema_post(self):
        tema_post = self.cleaned_data.get('tema_post')
        if tema_post not in [choice[0] for choice in TEMAS_AGRICULTURA]:
            raise forms.ValidationError("Selecciona un tema válido.")
        return tema_post

    def clean(self):
        cleaned_data = super().clean()
        imagen = cleaned_data.get('imagen')
        status_post = cleaned_data.get('status_post')

        if status_post == 1 and imagen is None:
            self.add_error('imagen', forms.ValidationError(
                "Debes subir una imagen para poder publicar o seleccionar la opción de borrador.",
                code='missing_image'))
        return cleaned_data
