try:
    open('vote.txt', 'x')
    open('vote2.txt', 'x')
except FileExistsError:
    pass
