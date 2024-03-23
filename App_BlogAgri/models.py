from django.db import models
from django.contrib.auth.models import User
from App_BlogAgri.choices import *
from django.utils import timezone
from django.utils.text import slugify

# Create your models here.


class Post(models.Model):

    titulo = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250, unique_for_date='publicacion_post', verbose_name='URL amigable')
    autor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='blog_posts')
    contenido = models.TextField()
    publicacion_post = models.DateTimeField(default=timezone.now)
    creacion_post = models.DateTimeField(auto_now_add=True)
    actualizacion_post = models.DateTimeField(auto_now=True)
    status_post = models.IntegerField(
        choices=STATUS_CHOICES, verbose_name='Privacidad')
    tema_post = models.CharField(
        max_length=50, choices=TEMAS_AGRICULTURA, default='General', verbose_name='Tema')
    imagen = models.ImageField(upload_to='post_images', blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Si no hay un slug definido, genera uno a partir del título
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ('-publicacion_post',)

    def __str__(self):
        return f'[{self.titulo} por {self.autor}]'
