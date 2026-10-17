# Out-of-memory recovery in the full-screen mode: a MemoryError during a
# calculation, while drawing, and during the "Working..." redraw must leave
# nCAS running, keep the user's variables and keep the input being evaluated.
#   python3 tests/oom_check.py [src|dist]
import sys
where = sys.argv[1] if len(sys.argv) > 1 else 'src'
sys.path.insert(0, 'tests/mock')
sys.path.insert(0, where)
import ti_system
import cas
import casgui

cas.run('keepme:=42')
K = (list('1+1') + ['enter'] + list('boom') + ['enter'] + list('3+3') + ['enter', 'tick']
     + list('keepme') + ['enter'] + list('7*6') + ['enter', 'esc'])
ti_system.KEYS[:] = K
orun = cas.run


def run(s):
    if s == 'boom':
        raise MemoryError
    return orun(s)


cas.run = run
odraw = casgui.draw


def draw():
    # 'tick' in the key list: the next drawing runs out of memory once
    if ti_system.KEYS and ti_system.KEYS[0] == 'tick':
        ti_system.KEYS.pop(0)
        raise MemoryError
    odraw()


casgui.draw = draw
try:
    cas.gui()
except KeyboardInterrupt:
    pass
got = [(h[0], h[1]) for h in casgui.G['hist']]
want = [('3+3', '6'), ('keepme', '42'), ('7*6', '42')]
bad = [w for w in want if w not in got]
if not any([h[0] == 'boom' and 'Out of memory' in h[1] for h in casgui.G['hist']]):
    bad.append('no out-of-memory message for boom')
if ti_system.KEYS:
    bad.append('keys left over: %r' % ti_system.KEYS[:3])
for b in bad:
    print('MISSING: %r' % (b,))
print('oom check: %s' % ('ok' if not bad else 'FAILED'))
if bad:
    sys.exit(1)
