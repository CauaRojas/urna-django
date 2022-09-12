from functools import reduce
from django.conf import settings
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import redirect
from os import path
from django.shortcuts import redirect

firstTurnEnded = False

alunos = {"07340": "Allice Sales da silva",
          "07242": "Cauã Alencar Rojas Romero",
          "07449": "Diogo William da Silva Rodrigues",
          "07228": "Felipe Oliveira dos Santos",
          "07277": "Fernando Marques dos Santos",
          "07346": "Gabriel Da Silva Freitas",
          "07520": "Gabriel David Souza do Carmo",
          "07514": "Gabriel de Moura Nardy Alexandroni",
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

candidatos = [
    {
        'name': 'Juliette BBB',
                'descricao': 'Mulher, Cantora, Empreendedora, Embaixador, Empoderada, Paraibana, LGBTQIA+, lutando pelo direitos de todos. Cuscuz salva vidas!',
                'img': "https://s2.glbimg.com/WU3jadMzNrZMZyqLK24Ej-eV-7k=/0x0:1500x1500/984x0/smart/filters:strip_icc()/i.s3.glbimg.com/v1/AUTH_59edd422c0c84a879bd37670ae4f538a/internal_photos/bs/2021/K/3/ztZD9BQ06ifX4IAv46nA/juliette-chapeu.jpg"
    },
    {
        'name': 'Francisco Pio',
                'descricao': 'Professor, Assoviador, amo soninhos e já fui denunciado por piadas mal compreendidas. Luto pela comunidade escolar!',
                'img': 'https://i.imgur.com/DMexgbj.jpg'
    },
    {
        'name': 'Paulo Muzy',
                'descricao': 'Maromba, peitudo, amo e vivo pela robertinha, vulgo minha vida, Lives matinais são a minha paixão, Vou lutar pela comunidade marombeira. Amo Creatina!',
                "img": "https://www.pragmatismopolitico.com.br/wp-content/uploads/2022/07/paulo-muzy.png"
    }, ]


def index(request):
    template = loader.get_template('index.html')
    context = {
        'candidatos': candidatos
    }
    return HttpResponse(template.render(context, request))


def cadastro(request):
    template = loader.get_template('cadastro.html')
    return HttpResponse(template.render())


def cadastrar(request):
    nome, rm = request.GET['nome'], request.GET['codigo']
    if rm in alunos.keys():
        return redirect('/cadastro?error=1')
    else:
        alunos[rm] = nome
        return redirect('/')


def votar(request):
    response = ''
    rm = request.GET['rm']
    voto = request.GET['vote']
    if rm in alunos.keys():
        votosFile = open(path.join(settings.BASE_DIR, 'vote.txt'), 'r')
        votos = votosFile.readlines()
        for linha in votos:
            if rm in linha:
                response = 'Você já votou!'
                break
        votosFile.close()
        if response == '':
            votos = open(path.join(settings.BASE_DIR, 'vote.txt'), 'a')
            votos.write(rm + " " + voto + '\n')
            votos.close()
            response = 'Voto computado!'
    return HttpResponse(response or 'Aluno não cadastrado!')


def candidato(request):
    template = loader.get_template('candidato.html')
    context = {
        'candidato': request.GET['candidato'],
    }
    return HttpResponse(template.render(context, request))


def computeVotes(firstTurn=True):
    votosFile = open(path.join(settings.BASE_DIR,
                     'vote.txt' if firstTurn else 'vote2.text'), 'r')
    votos = votosFile.readlines()
    votosFile.close()
    votos = [voto.strip().split(' ')[1] for voto in votos]
    votos = list(votos)
    numVotes = {
        1: votos.count('1'),
        2: votos.count('2'),
        3: votos.count('3')
    }
    return numVotes


def computeWinner(votes: "dict[int,int]"):
    totalVotes = sum(list(votes.values()))
    votesList = list(votes.values())
    winner = 0
    for pos, candidateVote in enumerate(votesList):
        if candidateVote > totalVotes/2:
            winner = pos
            break
    return winner


def encerrar(request):
    votes = computeVotes(not firstTurnEnded)

    # return redirect('/')
