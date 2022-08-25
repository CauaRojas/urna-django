from os import path
import requests
from django.conf import settings
try:
    open('vote.txt', 'x')
    open('vote2.txt', 'x')
except FileExistsError:
    pass


votes = open(path.join(settings.BASE_DIR, 'vote.txt'), 'r')
for vote in votes.readlines():
    rm = vote.split(' ')[0]
    voto = vote.split(' ')[1]
    httpRequest = requests.get(
        'http://localhost:8000/votar?candidato=' + voto + '&codigo=' + rm)
    print(httpRequest.text)
votes.close()
