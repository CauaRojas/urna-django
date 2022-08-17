from django.http import HttpResponse
from django.template import loader


def cadastro(request):
    #template = loader.get_template('cadastro.html')
    return HttpResponse('2')
