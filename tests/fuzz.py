# Random-input robustness test (CPython): reports raw Python exceptions and slow cases.
import sys, random, signal, time, traceback
sys.path.insert(0, 'src')
import cas
from cascore import CASError

random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 1)
N = int(sys.argv[2]) if len(sys.argv) > 2 else 1500
ATOMS = ['x', 'x', 'x', 'y', 'a', '2', '3', '1/2', '-1', 'pi', 'e', '0', '0.5', 'i', 'sqrt(2)']
FUNS = ['sin', 'cos', 'tan', 'ln', 'exp', 'sqrt', 'abs', 'arctan', 'arcsin', 'sinh', 'log10', 'floor']
OPS = ['+', '-', '*', '/', '^']

def expr(d):
    if d <= 0 or random.random() < 0.25:
        return random.choice(ATOMS)
    r = random.random()
    if r < 0.55:
        op = random.choice(OPS)
        a = expr(d - 1)
        b = expr(d - 1) if op != '^' else random.choice(['2', '3', '-1', '1/2', 'x', '-2'])
        return '(' + a + op + b + ')'
    return random.choice(FUNS) + '(' + expr(d - 1) + ')'

CMDS = [
    lambda e: e,
    lambda e: 'expand(' + e + ')',
    lambda e: 'factor(' + e + ')',
    lambda e: 'comDenom(' + e + ')',
    lambda e: 'd(' + e + ',x)',
    lambda e: 'integral(' + e + ',x)',
    lambda e: 'integral(' + e + ',x,0,1)',
    lambda e: 'limit(' + e + ',x,0)',
    lambda e: 'limit(' + e + ',x,inf)',
    lambda e: 'taylor(' + e + ',x,3)',
    lambda e: 'solve(' + e + '=0,x)',
    lambda e: 'solve(' + e + '>0,x)',
    lambda e: 'zeros(' + e + ',x)',
    lambda e: 'tCollect(' + e + ')',
    lambda e: 'tExpand(' + e + ')',
    lambda e: 'propFrac(' + e + ',x)',
    lambda e: e + '|x=2',
    lambda e: 'approx(' + e + ')',
    lambda e: 'fMin(' + e + ',x,0,2)',
    lambda e: 'series(' + e + ',x,2)',
]

class TO(Exception):
    pass

def handler(s, f):
    raise TO()

signal.signal(signal.SIGALRM, handler)
bad = 0
slow = []
for k in range(N):
    q = random.choice(CMDS)(expr(random.randint(1, 4)))
    t0 = time.time()
    signal.alarm(10)
    try:
        cas.run(q)
    except CASError:
        pass
    except ZeroDivisionError:
        pass
    except TO:
        slow.append(q)
        print('TIMEOUT: ' + q)
    except Exception as ex:
        bad += 1
        print('PYEXC %s: %s  <- %s' % (type(ex).__name__, ex, q))
        tb = traceback.extract_tb(sys.exc_info()[2])
        print('   at ' + ' > '.join(['%s:%d' % (f.name, f.lineno) for f in tb[-4:]]))
    finally:
        signal.alarm(0)
    dt = time.time() - t0
    if dt > 2:
        slow.append(q)
        print('SLOW %.1fs: %s' % (dt, q))
print('done', N, 'bad', bad, 'slow', len(slow))
