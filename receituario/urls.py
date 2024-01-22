from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    #path('ficha_identidade/', views.fichaIdentidade, name='ficha_identidade'),
    path('abertura_receituario/', views.abertura_receituario, name='abertura_receituario'),
    
]


