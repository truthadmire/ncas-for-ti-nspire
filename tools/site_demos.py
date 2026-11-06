# Redraws the demo screens of the website's main page (site/index.html): each
# example is typed into the full-screen mode on the stand-in display and keypad
# in tests/mock, and the screens before and after enter are stored in the
# page's DATA line, with the result as text.
#   python3 tools/site_demos.py            (run from the repository root)
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(ROOT, 'site', 'index.html')

# (tab, label, input, keys; None = the input typed character by character)
EX = (
    ('symbols', 'Indefinite integral', 'integral(x*e^(2x),x)', ['menu', '9', 'a', 'x', '*', 'e', '^', '2', 'x', 'right']),
    ('symbols', 'Definite integral', 'integral(sin(x),x,0,pi)', ['menu', '9', 'b', '0', 'up', 'p', 'i', 'right', 's', 'i', 'n', '(', 'x', ')']),
    ('symbols', 'Area under a curve', 'integral(x^2,x,0,3)', ['menu', '9', 'b', '0', 'up', '3', 'right', 'x', '^', '2', 'right']),
    ('symbols', 'Integral of a fraction', 'integral(1/(x^2+1),x)', ['menu', '9', 'a', 'ctrl', '/', '1', 'down', 'x', '^', '2', 'right', '+', '1', 'right']),
    ('symbols', 'Derivative', 'd(x^3*sin(x),x)', ['menu', '9', 'c', 'x', '^', '3', 'right', '*', 's', 'i', 'n', '(', 'x', ')']),
    ('symbols', 'Chain rule', 'd(ln(x^2+1),x)', ['menu', '9', 'c', 'l', 'n', '(', 'x', '^', '2', 'right', '+', '1', ')']),
    ('symbols', 'Derivative of a quotient', 'd(sin(x)/x,x)', ['menu', '9', 'c', 'ctrl', '/', 's', 'i', 'n', '(', 'x', ')', 'down', 'x', 'right']),
    ('symbols', 'No elementary antiderivative', 'integral(e^(-x^2),x)', ['menu', '9', 'a', 'e', '^', '-', 'x', '^', '2', 'right', 'right']),
    ('algebra', 'Solve a quadratic', 'solve(x^2-5x+6=0,x)', None),
    ('algebra', 'Exact arithmetic', '1/3+1/6+sqrt(8)', None),
    ('algebra', 'Factor over the integers', 'factor(x^4-16)', None),
    ('algebra', 'Partial fractions', 'expand(1/((x+1)*(x+2)))', None),
    ('algebra', 'Rationalize', '1/(1+sqrt(2))', None),
    ('calculus', 'Derivative', 'd(x^3*sin(x),x)', None),
    ('calculus', 'Integral by parts', 'integral(x*e^(2x),x)', None),
    ('calculus', 'Improper integral', 'integral(1/(1+x^2),x,-inf,inf)', None),
    ('calculus', 'Limit', 'limit((1+1/n)^n,n,inf)', None),
    ('calculus', 'Infinite series', 'sumSeq(1/k^2,k,1,inf)', None),
    ('calculus', 'Differential equation', "deSolve(y''+y=0 and y(0)=1 and y'(0)=0,x,y)", None),
    ('calculus', 'Taylor polynomial', 'taylor(sin(x),x,5)', None),
    ('matrix', 'Inverse', '[1,2;3,4]^-1', None),
    ('matrix', 'Exact eigenvalues', 'eigVl([8,5;7,9])', None),
    ('matrix', 'Symbolic eigenvalues', 'eigVl([a,b;b,a])', None),
    ('matrix', 'Determinant', 'det([a,b;c,d])', None),
    ('beyond', 'sec cubed, exactly', 'integral(sec(x)^3,x,0,pi/4)', None),
    ('beyond', 'Parameter inequality', 'solve(a*x<5,x)', None),
    ('beyond', 'Compound inequality', 'solve(1<2x+1<7,x)', None),
    ('beyond', 'Divergent integral', 'integral(1/x,x,-1,1)', None),
    ('beyond', 'Factorial limit', 'limit(n!/2^n,n,inf)', None),
    ('beyond', 'Absolute values', 'solve(abs(x)+abs(x-2)=2,x)', None),
    ('beyond', 'Implicit derivative', 'impDif(y^3-x*y=2,x,y)', None),
    ('beyond', 'Trig substitution', 'integral(x^2/sqrt(9-x^2),x,-3,3)', None),
    ('roots', 'Log with a base', 'log(8,2)', ['menu', 'b', '1', '8', 'tab', '2']),
    ('roots', 'Sum of logs', 'solve(log(x,2)+log(x-2,2)=3,x)', None),
    ('roots', 'Exponential equation', 'solve(2^x=5,x)', None),
    ('roots', 'Quadratic in ln(x)', 'solve(ln(x)^2-3ln(x)+2=0,x)', None),
    ('roots', 'Reject a false root', '(log(x,2)+log(x-2,2)=3)|x=-2', ['menu', 'b', '6', 'l', 'o', 'g', '(', 'x', ',', '2', ')', '+', 'l', 'o', 'g', '(', 'x', '-', '2', ',', '2', ')', '=', '3', 'tab', 'x', '=', '-', '2']),
    ('roots', "Vieta's formulas", 'vieta(x^2-5x+6,x)', ['menu', '3', 'a', 'x', '^', '2', '-', '5', 'x', '+', '6']),
    ('roots', 'Polynomial from roots', 'vieta({1,2,3},x)', None),
    ('roots', 'Roots without solving', 'vieta(2x^2-3x+1,x,a^2+b^2)', ['menu', '3', 'c', '2', 'x', '^', '2', '-', '3', 'x', '+', '1', 'tab', 'tab', 'a', '^', '2', '+', 'b', '^', '2']),
    ('roots', 'Reciprocals of the roots', 'vieta(x^3-6x^2+11x-6,x,1/a+1/b+1/c)', None),
)

RUNNER = r"""
import sys, json
sys.path.insert(0, 'tests/mock'); sys.path.insert(0, 'src')
import ti_system, ti_draw
frames = []
paint = ti_draw.paint_buffer
def grab():
    frames.append((len(ti_system.KEYS), list(ti_draw._ops)))
    paint()
ti_draw.paint_buffer = grab
ti_system.KEYS[:] = json.loads(sys.argv[1]) + ['enter']
import cas
try:
    cas.gui()
except KeyboardInterrupt:
    pass
print(json.dumps([[f for f in frames if f[0] == 1][-1][1], frames[-1][1]]))
"""
RESULT = 'import sys; sys.path.insert(0, "src"); import cas; print(cas.run(sys.argv[1]))'


def run(args):
    r = subprocess.run([sys.executable, '-c'] + args, capture_output=True, text=True, cwd=ROOT)
    if r.returncode:
        sys.stderr.write(r.stderr)
        raise SystemExit('example failed: %r' % (args[1],))
    return r.stdout


COLORS = []


def color(c):
    c = tuple(c)
    if c not in COLORS:
        COLORS.append(c)
    return COLORS.index(c)


def pack(ops):
    out = []
    for o in ops:
        if o[0] == 'rect':
            out.append(['r', o[1], o[2], o[3], o[4], color(o[5])])
        elif o[0] == 'line':
            out.append(['l', o[1], o[2], o[3], o[4], color(o[5])])
        elif o[0] == 'text':
            out.append(['t', o[1], o[2], o[3], color(o[4])])
    return out


def build():
    data = []
    for tab, label, inp, keys in EX:
        a, b = json.loads(run([RUNNER, json.dumps(keys or list(inp))]))
        data.append({'c': tab, 'l': label, 'i': inp, 'r': run([RESULT, inp]).strip(),
                     'a': pack(a), 'b': pack(b), 'k': keys})
    colors = ['rgb(%d,%d,%d)' % c for c in COLORS]
    text = json.dumps({'colors': colors, 'ex': data}, separators=(',', ':'))
    with open(PAGE) as f:
        page = f.read()
    page, n = re.subn(r'^const DATA = .*$', lambda m: 'const DATA = ' + text + ';', page, flags=re.M)
    if n != 1:
        raise SystemExit('no DATA line in the page')
    with open(PAGE, 'w') as f:
        f.write(page)
    print('%d examples, %d KB' % (len(data), len(text) // 1024))


if __name__ == '__main__':
    build()
