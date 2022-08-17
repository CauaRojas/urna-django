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
