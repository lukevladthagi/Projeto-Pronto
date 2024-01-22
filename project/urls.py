from django.contrib import admin
from django.urls import path, include
from administrativo import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('prontocardio/', include('administrativo.urls')),
    path('totem/', include('totem.urls')),
    path('notificar/', include('notificar.urls')),
]


