# MicroPython stand-in: no alarms (the run has no time limit)
SIGALRM = 14
def signal(n, f):
    pass
def alarm(n):
    pass
