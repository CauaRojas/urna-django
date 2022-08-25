from django.conf import settings
import requests
from django.http import HttpResponse
from django.template import loader
from os import path

alunos = {"07340": "Allice Sales da silva",
          "07242": "Cauã Alencar Rojas Romero",
          "07449": "Diogo William da Silva Rodrigues",
          "07228": "Felipe Oliveira dos Santos",
          "07277": "Fernando Marques dos Santos",
          "07346": "Gabriel Da Silva Freitas",
          "07520": "Gabriel David Souza do Carmo",
          "07541": "Gabriel de Moura Nardy Alexandroni",
          "07371": "Guilherme Pereira Luz",
          "07249": "Gustavo de Oliveira",
          "07361": "Heloiza Oliveira da Silva",
          "07303": "Isabella Sofia Martins",
          "07397": "Julia Sampaio Moreira",
          "07264": "Lucas Pessoa Froes",
          "07360": "Matheus Lourenço Pereira",
          "07295": "Nicolas Fortunato Gomes Cordeiro",
          "07378": "Pedro Henrique Moraes Ferrarezzi",
          "07307": "Rafael da Silva Coimbra",
          "07328": "Richard Barbosa Sanches",
          "07415": "Samuel da Silva Lima"}


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
    response = ''
    rm = request.GET['codigo']
    voto = request.GET['voto']
    if rm in alunos.keys():
        votos = open(path.join(settings.BASE_DIR, 'vote.txt'), 'r')
        for linha in votos:
            if rm in linha:
                response = 'Você já votou!'
                break
        votos.close()
        if response == '':
            votos = open(path.join(settings.BASE_DIR, 'vote.txt'), 'a')
            votos.write(rm + voto + '\n')
            votos.close()
            response = 'Voto computado!'
    return HttpResponse(response or 'Aluno não cadastrado!')


def candidato(request):
    template = loader.get_template('candidato.html')
    context = {
        'candidato': request.GET['candidato'],
    }
    return HttpResponse(template.render(context, request))


def computeVotes():
    votos = open(path.join(settings.BASE_DIR, 'vote.txt'), 'r')
    votos = votos.readlines()
    votos = [voto.strip() for voto in votos]
    votos = set(votos)
    votos = list(votos)
    votos.sort()
    return votos
