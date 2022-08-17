from django.http import HttpResponse


def votar(request):
    return HttpResponse("You're voting!")
