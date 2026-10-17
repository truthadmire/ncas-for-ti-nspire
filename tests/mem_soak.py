# Long-session memory check of the full-screen mode, for MicroPython with the
# calculator's heap: cold start, first menu and help use, many calculations
# (more than the history keeps), a long edit with undo, and oversized
# requests. It reports memory after collection for each phase and the least
# free memory seen, and fails if memory keeps growing or a budget is broken.
#   micropython -X heapsize=2000000 tests/mem_soak.py [dist|src]
#   python3 tests/mem_soak.py            (budgets only; no memory numbers)
import sys
where = sys.argv[1] if len(sys.argv) > 1 else 'dist'
sys.path.insert(0, 'tests/mock')
sys.path.insert(0, where)
import gc
import ti_system
import ti_draw


def paint():
    # the stand-in screen keeps every frame as text; here frames are only
    # dropped, so the test measures nCAS and not the stand-in
    del ti_draw._ops[:]


ti_draw.paint_buffer = paint

HAVE = hasattr(gc, 'mem_free')
LOW = [10 ** 9]
PHASES = []


def used():
    gc.collect()
    return gc.mem_alloc() if HAVE else 0


TICK = [0]


def sample():
    # every 10th screen: free memory after a collection (without it, free
    # memory only shows garbage not yet collected)
    TICK[0] += 1
    if HAVE and TICK[0] % 10 == 0:
        gc.collect()
        LOW[0] = min(LOW[0], gc.mem_free())


def word(s):
    return list(s)


EXPRS = ['solve(x^2-5x+6=0,x)', 'factor(x^4-16)', 'integral(x*e^(2x),x)', 'd(x^3*sin(x),x)',
         'expand((x+y+1)^6)', '[1,2;3,4]^-1', 'eigVl([8,5;7,9])', 'taylor(e^x,x,8)',
         'limit((1+1/n)^n,n,inf)', 'sumSeq(1/k^2,k,1,inf)', '100!', 'nCr(60,30)']
K = []
K += ['menu', 'esc'] + word('?solve') + ['enter']              # first menu and help use
MARK1 = len(K)
for i in range(4):                                              # 48 calculations > 30 kept
    for e in EXPRS:
        K += word(e) + ['enter']
MARK2 = len(K)
K += word('x+' * 150 + '1')                                     # a 301-character edit
K += ['ctrl', 'esc'] * 5 + ['clear']                            # undo, then clear
K += word('expand((a+b+c+d+z)^30)') + ['enter']                 # oversized requests
K += word('newMat(500,500)') + ['enter']
K += word('seq(k,k,1,100000)') + ['enter']
MARK3 = len(K)
for e in EXPRS:                                                 # life goes on afterwards
    K += word(e) + ['enter']
K += ['esc']
ti_system.KEYS[:] = K

marks = {}


def hook():
    # sample memory while the session runs, and at the phase boundaries
    m = sys.modules.get('casgui')
    orig = m.draw

    def draw():
        orig()
        sample()
        left = len(ti_system.KEYS)
        for name, at in (('after menu and help', MARK1), ('after 48 calculations', MARK2),
                         ('after edit and oversized requests', MARK3)):
            if len(K) - left == at and name not in marks:
                marks[name] = used()
    m.draw = draw


ti_system.HOOK.append(hook)
start = used()
import cas
loaded = used()
try:
    cas.gui()
except KeyboardInterrupt:
    pass
end = used()
import casgui
G = casgui.G
bad = []
hist = G.get('hist', [])
if len(hist) > casgui.MAXH:
    bad.append('history has %d entries' % len(hist))
if sum([len(e[0]) + len(e[1]) for e in hist]) > casgui.HISTCH + 2000:
    bad.append('history holds too many characters')
u = G.get('undo', [])
if len(u) > casgui.UNDON or sum([len(x[3]) for x in u]) > casgui.UNDOCH + 400:
    bad.append('undo is over budget')
if len(G.get('lay', {})) > 61:
    bad.append('layout cache has %d entries' % len(G['lay']))
if ti_system.KEYS:
    bad.append('keys left over: %r' % ti_system.KEYS[:4])
errs = [e for e in hist if e[1].startswith('Error: Resource limit')]
if HAVE:
    print('memory in use after collection (KB):')
    print('  before import        %4d' % (start // 1024))
    print('  after loading        %4d' % (loaded // 1024))
    for name in ('after menu and help', 'after 48 calculations', 'after edit and oversized requests'):
        if name in marks:
            print('  %-20s %4d' % (name[:20], marks[name] // 1024))
    print('  at the end           %4d' % (end // 1024))
    print('least free memory after collection: %d KB' % (LOW[0] // 1024))
    a = marks.get('after 48 calculations', end)
    if end > a + 120 * 1024:
        bad.append('memory grew by %d KB after the history was full' % ((end - a) // 1024))
for b in bad:
    print('PROBLEM: ' + b)
print('mem soak: %d history entries, %d undo steps, %d layouts, %s' %
      (len(hist), len(u), len(G.get('lay', {})), 'ok' if not bad else 'FAILED'))
if bad:
    sys.exit(1)
