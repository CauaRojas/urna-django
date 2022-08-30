from os import path
from django.conf import settings
try:
    open(path.join(settings.BASE_DIR, 'vote.txt'), 'x')
    open(path.join(settings.BASE_DIR, 'vote2.txt'), 'x')
except FileExistsError:
    open(path.join(settings.BASE_DIR, 'vote.txt'), 'w').close()
    open(path.join(settings.BASE_DIR, 'vote2.txt'), 'w').close()
