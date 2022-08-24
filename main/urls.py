from django.urls import path
from .views import index, votar, cadastro, candidato


urlpatterns = [
    path('', index, name='index'),
    path('votar/', votar, name='votar'),
    path('cadastro/', cadastro, name='cadastro'),
    path('candidato/', candidato, name='candidato'),
]
