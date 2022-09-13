from multiprocessing import context
from os import path

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

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
removedCandidates = []


def index(request):
    print(removedCandidates)
    template = loader.get_template('index.html')
    votableCandidates = [
        candidato for candidato in candidatos if candidato not in removedCandidates]
    context = {
        'candidatos': votableCandidates
    }
    return HttpResponse(template.render(context, request))


def cadastro(request):
    erro = request.GET['error'] if 'error' in request.GET.keys() else None
    context = {
        'erro': erro
    }
    template = loader.get_template('cadastro.html')
    return HttpResponse(template.render(context, request))


def cadastrar(request):
    nome, rm = request.GET['nome'], request.GET['codigo']
    if rm in alunos.keys():
        return redirect('/cadastro?error=erro')
    else:
        alunos[rm] = nome
        return redirect('/')


def votar(request):
    response = ''
    fileVote = 'vote.txt' if not firstTurnEnded else 'vote2.txt'
    rm = request.GET['rm']
    voto = request.GET['vote']
    if rm in alunos.keys():
        votosFile = open(path.join(settings.BASE_DIR, fileVote), 'r')
        votos = votosFile.readlines()
        for linha in votos:
            if rm in linha:
                response = 'Você já votou!'
                break
        votosFile.close()
        if response == '':
            votos = open(path.join(settings.BASE_DIR, fileVote), 'a')
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
                     'vote.txt' if firstTurn else 'vote2.txt'), 'r')
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

    def itNeedsSecondTurn():
        return not (votes[1] > totalVotes / 2 or votes[2] > totalVotes / 2 or votes[3] > totalVotes / 2)
    votesList = list(votes.values())
    winner = -1
    print(votesList, itNeedsSecondTurn())
    if not itNeedsSecondTurn():
        winner = max(votes, key=votes.get)
    else:
        winner = dict(
            sorted(votes.items(), key=lambda item: item[1], reverse=True))
        winner.popitem()
        # winner = sorted(votes, key=votes.get)[0:2]
    return winner


def encerrar(request):
    global firstTurnEnded
    votes = computeVotes(not firstTurnEnded)
    winner = computeWinner(votes)
    if winner == 0:
        return redirect('/empate')
    elif winner == -1:
        return redirect('/empate?error=erro')
    elif type(winner) == dict:
        print(winner)
        cand1, cand2 = winner.keys()
        cand1, cand2 = candidatos[cand1-1], candidatos[cand2-1]
        for candidato in candidatos:
            if cand1['name'] != candidato['name'] and cand2['name'] != candidato['name']:
                removedCandidates.append(candidato)
        firstTurnEnded = True
        return redirect('/')
    elif type(winner) == int:
        candidates = dict(
            sorted(votes.items(), key=lambda item: item[1], reverse=True))
        candidates.pop(winner)
        return redirect('/vencedor?primeiro='+candidatos[winner-1]['name']+"&segundo="+candidatos[list(candidates.keys())[0] - 1]['name'])


def vencedor(request):
    primeiro, segundo = request.GET['primeiro'], request.GET['segundo']
    terceiro = ''
    for candidato in candidatos:
        if candidato['name'] != primeiro and candidato['name'] != segundo:
            terceiro = candidato['name']
    for candidato in candidatos:
        if candidato['name'] == primeiro:
            primeiro = candidato
        elif candidato['name'] == segundo:
            segundo = candidato
        elif candidato['name'] == terceiro:
            terceiro = candidato
    context = {
        'candidatos': [primeiro, segundo, terceiro]}
    template = loader.get_template('vencedor.html')
    return HttpResponse(template.render(context, request))
