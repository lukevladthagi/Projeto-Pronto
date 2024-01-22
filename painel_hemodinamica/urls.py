from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.painel_hemodinamica, name='painel_hemodinamica'),
]


