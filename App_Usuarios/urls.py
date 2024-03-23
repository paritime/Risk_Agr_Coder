from django.urls import path
from App_Usuarios.views import registro, ingresar, logout, perfil
# perfil

urlpatterns = [
    path('signup/', registro, name='signup'),
    path('login/', ingresar, name='login'),
    path('logout/', logout, name='logout'),
    path('perfil/', perfil, name='perfil'),

]
