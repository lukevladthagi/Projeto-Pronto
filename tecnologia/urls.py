from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('listar_usuarios/', views.listar_usuario, name='listar_usuario'),
]