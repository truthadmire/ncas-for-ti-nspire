# Editing keys of the full-screen mode: a typed closing bracket steps over
# one already there (or out of √, |x|, the n-th root and d/dx), brackets
# left open are closed at enter, ctrl ◄ ► go to the start / end of the line,
# shift ◄ ► move a word or template at a time, var lists the variables, and
# a matrix from the template is a grid on the line whose cells can be edited.
# Each case types keys and checks the input as the history shows it.
#   python3 tests/edit_check.py [src|dist|onefile]
import sys
where = sys.argv[1] if len(sys.argv) > 1 else 'src'
sys.path.insert(0, 'tests/mock')
sys.path.insert(0, where)
import ti_system
import ti_draw

CASES = [
    # (what, keys, evaluated input, result or None)
    ('no variables yet', ['var'], None, None),
    ('sin key, ) steps over', ['sin', 'x', ')', '+', '1'], 'sin(x)+1', None),
    ('nested, both step over', ['sin', 'cos', 'x', ')', ')', '+', '1'], 'sin(cos(x))+1', None),
    ('an open ( gets its own )', ['sin'] + list('(x+1)*2)'), 'sin((x+1)*2)', None),
    ('typed by hand', list('f((x))'), 'f((x))', None),
    ('out of a square root', ['sqrt', '8', ')', '+', '1'], 'sqrt(8)+1', '2*√2+1'),
    ('out of an exponent and d/dx', ['menu', '9', 'c', 'x', '^', '2', ')', '+', '1'], 'd(x^2,x)+1', '2*x+1'),
    ('closed at enter', list('factor(x^2-1'), 'factor(x^2-1)', '(x-1)*(x+1)'),
    ('closed at enter, nested', list('abs(sin(pi/2'), 'abs(sin(pi/2))', '1'),
    ('ctrl left / right', list('2+3') + ['ctrl', 'left', '1', 'ctrl', 'right', '0'], '12+30', '42'),
    ('ctrl+left combined', list('5') + ['ctrl+left', '-'], '-5', '-5'),
    ('ctrl left leaves a template', ['ctrl', '/', '1', 'down', '3', 'ctrl', 'left'] + list('2+'), '2+(1/3)', '7/3'),
    ('shift left: words', list('sin(x)+cos(y)') + ['shift', 'left'] * 3 + list('2*'), 'sin(x)+2*cos(y)', None),
    ('shift+right combined', list('ab+cd') + ['ctrl', 'left', 'shift+right', '*', '3'], 'ab*3+cd', None),
    ('shift right over a template', ['ctrl', '/', '1', 'down', '2', 'ctrl', 'left', 'shift+right', '+', '1'], '(1/2)+1', '3/2'),
    ('shift then a letter', ['shift', 'a', '+', 'a'], 'A+a', '2*a'),
    ('5x5 matrix template in det(', ['d', 'e', 't', '(', 'menu', '9', '1', '5', '5', 'enter', '2', 'tab', '0', 'tab', '0', 'tab', '0', 'tab', '0', 'tab', '0', 'tab', '2', 'tab', '0', 'tab', '0', 'tab', '0', 'tab', '0', 'tab', '0', 'tab', '2', 'tab', '0', 'tab', '0', 'tab', '0', 'tab', '0', 'tab', '0', 'tab', '2', 'tab', '0', 'tab', '0', 'tab', '0', 'tab', '0', 'tab', '0', 'tab', '2', 'enter', ')'], 'det([2,0,0,0,0;0,2,0,0,0;0,0,2,0,0;0,0,0,2,0;0,0,0,0,2])', '32'),
    ('edit a cell, ) leaves the matrix', list('det(') + ['menu', '9', '1', 'enter', '1', 'tab', '2', 'tab', '3', 'tab', '4', 'enter', 'left', 'del', '5', ')'], 'det([1,2;3,5])', '-1'),
    (', and ; move between cells', ['menu', '9', '1', 'enter', 'enter', 'left', 'up', 'left'] + list('1,2;3,4,') + ['*', '2'], '[1,2;3,4]*2', '[[2,4][6,8]]'),
    ('] leaves the matrix', ['menu', '9', '1', 'enter', '1', 'tab', '2', 'tab', '3', 'tab', '4', 'enter', 'left', ']', '^', '2'], '[1,2;3,4]^2', '[[7,10][15,22]]'),
    ('a comma inside brackets stays in the cell', ['menu', '9', '1', 'enter', '1', 'tab', '2', 'tab', '3', 'tab', '4', 'enter', 'left', 'del'] + list('gcd(4,6)'), '[1,2;3,gcd(4,6)]', '[[1,2][3,2]]'),
    ('ctrl left leaves a matrix', ['menu', '9', '1', 'enter', '1', 'tab', '2', 'tab', '3', 'tab', '4', 'enter', 'left', 'ctrl', 'left'] + list('det('), 'det([1,2;3,4])', '-2'),
    ('var: pick a function', list('a:=5') + ['enter'] + list('f(x):=x^2+1') + ['enter', 'var', '2', '3'], 'f(3)', '10'),
    ('var: ans comes first', ['var', '1', '+', '1'], 'ans+1', '11'),
    ('var: pick a variable', ['var', '2', '*', '2'], 'a*2', '10'),
]
K = []
for what, keys, want_in, want_out in CASES:
    K += keys + ['enter' if want_in else 'clear']
K += ['esc']
ti_system.KEYS[:] = K
LOG = []


def hook():
    for name in ('casgui', 'ncasgui'):
        m = sys.modules.get(name)
        if m is not None and hasattr(m, 'evaluate'):
            orig = m.evaluate

            def ev(run, s, orig=orig, m=m):
                orig(run, s)
                LOG.append((m.G['hist'][-1][0], m.G['hist'][-1][1]))   # as the history shows it
            m.evaluate = ev
            return


ti_system.HOOK.append(hook)
if where == 'onefile':
    import ncasgui
else:
    import cas
    try:
        cas.start()
    except KeyboardInterrupt:
        pass
bad = []
got = [x for x in LOG if x[0] not in ('a:=5', 'f(x):=x^2+1')]
want = [c for c in CASES if c[2]]
for i in range(len(want)):
    what, keys, wi, wo = want[i]
    g = got[i] if i < len(got) else ('(nothing)', '')
    if g[0] != wi or (wo is not None and g[1] != wo):
        bad.append('%s: evaluated %r -> %r, wanted %r%s' % (what, g[0], g[1], wi, ' -> %r' % wo if wo else ''))
if not [f for f in ti_draw.FRAMES if 'No variables yet' in f]:
    bad.append('var with no variables: no message')
if not [f for f in ti_draw.FRAMES if 'Variables' in f and 'a = 5' in f and 'f(x) = x^2+1' in f]:
    bad.append('var list not drawn with a = 5 and f(x) = x^2+1')
if ti_system.KEYS:
    bad.append('keys left over: %r' % ti_system.KEYS[:4])
for b in bad:
    print('BAD: ' + b)
print('edit check: %d cases, %s' % (len(CASES), 'ok' if not bad else '%d FAILED' % len(bad)))
if bad:
    sys.exit(1)
