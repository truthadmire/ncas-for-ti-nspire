# shots.py - pictures of the full-screen mode for the README, drawn from
# the desktop stand-ins for ti_draw/ti_system (tests/mock), as SVG files in
# docs/img. They are simulated screens: the calculator's font differs.
#   python3 tools/shots.py
import json, os, subprocess, sys
from xml.sax.saxutils import escape

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'docs', 'img')

PROG = r'''
import sys, json
sys.path.insert(0, 'tests/mock'); sys.path.insert(0, 'src')
import ti_system, ti_draw
frames = []
orig = ti_draw.paint_buffer
def paint():
    frames.append((len(ti_system.KEYS), list(ti_draw._ops)))
    orig()
ti_draw.paint_buffer = paint
ti_system.KEYS[:] = json.loads(sys.argv[1])
want = int(sys.argv[2])
import cas
try:
    cas.gui()
except KeyboardInterrupt:
    pass
idx = [i for i in range(len(frames)) if frames[i][0] == want]
i = idx[-1] if idx else len(frames) - 1
# pop-ups are drawn over the previous screen: go back to the last frame
# that cleared the whole screen
j = i
while j > 0 and not any([o[0] == 'rect' and o[1] == 0 and o[2] == 0 and o[3] >= 318 and o[4] >= 212
                         for o in frames[j][1]]):
    j -= 1
ops = []
for f in frames[j:i + 1]:
    ops += f[1]
print(json.dumps(ops))
'''

def keys(entries):
    k = []
    for e in entries:
        k += list(e) + ['enter']
    return k

SHOTS = [
    ('history', keys(['[1,2;3,4]^-1', 'solve(x^2-5x+6=0,x)', '1/3+1/6+sqrt(8)',
                      'integral(sec(x)^3,x,0,pi/4)']), 0),
    ('menu', keys(['factor(x^4-16)', 'd(x^3*sin(x),x)']) + ['menu'], 0),
    ('catalog', keys(['limit((1+1/n)^n,n,inf)']) + ['cat', 'e', 'e'], 0),
]


def svg(ops):
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="477" height="318" viewBox="0 0 318 212">',
           '<rect width="318" height="212" fill="#fff"/>']
    for op in ops:
        c = 'rgb(%d,%d,%d)' % tuple(op[-1])
        if op[0] == 'rect':
            out.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (op[1], op[2], op[3], op[4], c))
        elif op[0] == 'line':
            out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1"/>'
                       % (op[1], op[2], op[3], op[4], c))
        elif op[0] == 'text':
            out.append('<text x="%d" y="%d" fill="%s" font-family="Menlo,Consolas,monospace" '
                       'font-size="12">%s</text>' % (op[1], op[2], c, escape(op[3])))
    return '\n'.join(out) + '\n</svg>\n'


if __name__ == '__main__':
    os.makedirs(OUT, exist_ok=True)
    for name, k, want in SHOTS:
        r = subprocess.run([sys.executable, '-c', PROG, json.dumps(k), str(want)],
                           capture_output=True, text=True, cwd=ROOT)
        if r.returncode:
            raise SystemExit(r.stderr)
        path = os.path.join(OUT, name + '.svg')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(svg(json.loads(r.stdout)))
        print('wrote', os.path.relpath(path, ROOT))
