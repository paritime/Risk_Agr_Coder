from django.urls import path
from .views import inicio, simulador, reg_proy, reg_solicitante, consulta

urlpatterns = [
    path('', inicio, name='inicio'),
    path('inicio', inicio, name='inicio'),
    path('simulador/', simulador, name='simulador'),
    path('reg_proy/', reg_proy, name='regpro'),
    path('reg_solicitante/', reg_solicitante, name='regsol'),
    path('consulta/', consulta, name='consulta'),
]
