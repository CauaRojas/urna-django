from django.urls import path
from main.views import index, votar, cadastro

urlpatterns = [
    path('', index, name='index'),
    path('votar/', votar, name='votar'),
    path('cadastro/', cadastro, name='cadastro'),
]
