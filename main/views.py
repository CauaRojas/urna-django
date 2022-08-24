from re import template
from django.http import HttpResponse
from django.template import loader


def index(request):
    template = loader.get_template('index.html')
    context = {
        'candidatos': [
            {
                'name': 'John Doe',
            },
            {
                'name': 'Jane Doe',
            },
            {
                'name': 'Joe Doe',
            }, ],

    }
    return HttpResponse(template.render(context, request))


def cadastro(request):
    template = loader.get_template('cadastro.html')
    return HttpResponse(template.render())


def votar(request):
    return HttpResponse("You're voting!")
