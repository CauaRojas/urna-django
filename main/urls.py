from django.urls import path
from .views import index, votar, cadastro, candidato, cadastrar, encerrar

urlpatterns = [
    path('', index, name='index'),
    path('votar/', votar, name='votar'),
    path('cadastro/', cadastro, name='cadastro'),
    path('candidato/', candidato, name='candidato'),
    path('cadastrar/', cadastrar, name='cadastrar'),
    path('encerrar/', encerrar, name='encerrar')
]
