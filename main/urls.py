from django.urls import path
from main.views import index, votar

urlpatterns = [
    path('', index, name='index'),
    path('votar/', votar, name='votar'),
]
