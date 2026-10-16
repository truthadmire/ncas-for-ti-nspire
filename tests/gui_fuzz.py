# Random key presses into the graphical mode (stand-in ti_draw/ti_system):
# any Python exception that escapes, or a key that takes too long, is a bug.
#   python3 tests/gui_fuzz.py [runs] [keys per run] [src|dist]
#   micropython -X heapsize=2000000 tests/gui_fuzz.py 100 150 dist
import sys
try:
    import signal, traceback
except ImportError:
    # MicroPython: stand-ins without time limits
    sys.path.insert(0, 'tests/mpstub')
    import signal, traceback
import random, time
try:
    RecursionError
except NameError:
    RecursionError = RuntimeError
runs = int(sys.argv[1]) if len(sys.argv) > 1 else 200
nkeys = int(sys.argv[2]) if len(sys.argv) > 2 else 150
where = sys.argv[3] if len(sys.argv) > 3 else 'src'
sys.path.insert(0, 'tests/mock')
sys.path.insert(0, where)
import ti_system, ti_draw
import cas, casgui

NAV = ['up', 'down', 'left', 'right', 'enter', 'tab', 'menu', 'del', 'clear', 'trig',
       'esc', 'center', 'sqrt', 'pi', 'square', 'exp', 'ln', 'log', 'ee', 'neg', 'ans',
       'foo', 'home', 'doc', 'ctrl', 'ctrl', 'ctrl', 'shift', 'ctrl+(', 'ctrl+^', '\u2248',
       '[]', 'var', '10^x', 'undo', 'symbols', 'template', 'exp', 'abs', 'ctrl+/', 'ctrl+^',
       'ctrl+square', '^', '^', 'left', 'right', 'up', 'down', 'del', 'tab', 'tab', 'shift+tab',
       'catalog', 'cat']
CHARS = list('0123456789xyzabcn+-*/^().,=<>!|;[]{}:') + ['π', '√', '²']
SNIPS = ['sin(', 'cos(', 'solve(', 'factor(', 'expand(', 'd(', 'integral(', 'limit(',
         'det(', '[1,2;3,4]', 'x^2', 'sqrt(2)', '1/3', 'e^x', ':deg', ':rad', 'ans',
         '{1,2,3}', 'nCr(', 'mod(', '2^(10^9)', 'deSolve(', 'y\'', '->a', ':=']


class Slow(Exception):
    pass


def alarm(sig, frm):
    raise Slow()


signal.signal(signal.SIGALRM, alarm)
EXPRS = ['solve(x^2-5x+6=0,x)', 'factor(x^4-16)', 'expand((x+1)^3)', 'd(sin(x)^2,x)',
         'integral(x*e^x,x)', 'limit(sin(x)/x,x,0)', 'det([1,2;3,4])', '[1,2;3,4]^-1',
         'sqrt(8)', '1/3+1/6', 'nCr(10,3)', 'factor(360)', 'cos(pi/12)', 'taylor(e^x,x,4)',
         "deSolve(y'=y,x,y)", 'sumSeq(k^2,k,1,n)', 'mean({1,2,3,4})', '2^(10^9)', 'mod(2^100,7)',
         'zeros(x^3-x,x)', 'a:=5', 'a^2', 'f(x):=x^2+1', 'f(3)', 'ans*2', 'eigVl([2,1;1,2])',
         'simult([2,1;1,-1],[5;1])', 'crossP([1,2,3],[4,5,6])', 'pi>>Decimal', 'x^2|x=3', '1/0',
         'sin(', ')(', '[1,2', 'solve(', 'x^^2', '::', '[[1]', '{', '|x=']


def actions(rnd, n):
    keys = []
    while len(keys) < n:
        p = rnd.random()
        if p < 0.35:
            keys.extend(list(rnd.choice(EXPRS)))
            keys.append('enter')
        elif p < 0.5:
            keys.extend(['menu', rnd.choice('12345678'), rnd.choice('123456789abcdefg')])
            keys.extend(rnd.choice(CHARS) for i in range(rnd.randint(0, 6)))
            keys.append(rnd.choice(['enter', 'enter', 'clear', 'left', 'esc']))
        elif p < 0.6:
            keys.extend(['menu', '9', rnd.choice('123456789'), rnd.choice(['enter', '2', 'up', 'right', 'esc'])])
            keys.extend(rnd.choice(['enter', '1', '2', 'tab', 'x', 'del', 'clear', 'up', 'left', '-'])
                        for i in range(rnd.randint(0, 12)))
            keys.extend(['enter', 'enter'])
        elif p < 0.7:
            keys.extend(['menu', 'a'] + [rnd.choice(['up', 'down', 'left', 'right']) for i in range(rnd.randint(0, 9))])
            keys.append(rnd.choice(['enter', 'enter', 'esc']))
        elif p < 0.8:
            keys.extend([rnd.choice(['up', 'up', 'down']) for i in range(rnd.randint(1, 6))] + ['enter'])
        else:
            for i in range(rnd.randint(1, 10)):
                keys.append(rnd.choice(NAV[:-1] + CHARS))
    return [k for k in keys if k != 'esc' or rnd.random() < 0.3]


bad = 0
slow = 0
total = 0
evals = [0]
orig = casgui.evaluate


def counted(run, s):
    evals[0] += 1
    orig(run, s)


casgui.evaluate = counted
from cascore import CASError
raw = {}
orun = cas.run


def checked(line):
    # a Python error that is not a CASError (or an expected arithmetic one) is a bug
    try:
        return orun(line)
    except (CASError, ZeroDivisionError, MemoryError, KeyboardInterrupt, Slow):
        raise
    except RecursionError:
        raise
    except Exception as ex:
        key = type(ex).__name__ + ': ' + str(ex)
        raw.setdefault(key, line)
        raise


cas.run = checked
t0 = time.time()
for run in range(runs):
    if hasattr(random, 'Random'):
        rnd = random.Random(run)
    else:
        random.seed(run)
        rnd = random
    keys = actions(rnd, nkeys)
    total += len(keys)
    ti_system.KEYS[:] = keys
    casgui.G.clear()
    cas.ENV.clear()
    cas.UFUN.clear()
    while ti_system.KEYS:
        n0 = len(ti_system.KEYS)
        signal.alarm(30)
        try:
            cas.gui()
        except Slow:
            slow += 1
            done = len(keys) - n0
            print('SLOW run %d near keys %r' % (run, keys[max(0, done - 30):done + 5]))
            break
        except Exception:
            bad += 1
            print('BUG run %d:' % run)
            traceback.print_exc()
            break
        finally:
            signal.alarm(0)
        del ti_draw.FRAMES[:]
        if len(ti_system.KEYS) == n0:
            break
for k, v in sorted(raw.items()):
    print('RAW ' + k + '   <- ' + repr(v))
bad += len(raw)
print('gui fuzz: %d runs, %d keys, %d evaluations, %d errors, %d slow, %.0f s'
      % (runs, total, evals[0], bad, slow, time.time() - t0))
if bad or slow:
    sys.exit(1)
