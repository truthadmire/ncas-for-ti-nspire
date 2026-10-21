# The red cursor on the entry line must be drawn where the next character
# goes. After every key, a marker character is put into a copy of the line at
# the cursor and drawn; the cursor bar has to sit at the marker's left edge.
# Covers plain text, brackets, templates (fraction, root, power, integral,
# d/dx), an empty slot and a line long enough to scroll.
#   python3 tests/cursor_check.py [src|dist|onefile]
import sys
where = sys.argv[1] if len(sys.argv) > 1 else 'src'
sys.path.insert(0, 'tests/mock')
sys.path.insert(0, where)
import ti_system
import ti_draw

MARK = '§'


def word(s):
    return list(s)


K = []
K += ['menu', '4', '8'] + ['left'] * 3 + ['right'] * 3 + ['clear']      # eigVc([|])
K += word('sin(cos(x))') + ['left'] * 12 + ['clear']                     # nested brackets
K += ['ctrl', '/', '1', 'down', 'x', '+', '2', 'left', 'left', 'right', 'clear']
K += ['sqrt', '8', 'left', 'left', 'right', 'right', 'right', 'clear']
K += ['ctrl', '^', '3', 'right', '2', '7', 'left', 'left', 'left', 'clear']
K += ['x', '^', '2', '+', '1', 'left', 'left', 'left', 'left', 'clear']
K += ['menu', '9', 'b', '0', 'up', '1', 'right', 'x', 'left', 'left', 'left', 'clear']
K += ['menu', '9', 'c'] + word('x*sin(x)') + ['left'] * 4 + ['clear']
K += ['menu', '9', '1', 'enter', '1', 'tab', '22', 'tab', '3', 'tab', '4', 'enter', 'left', 'left', 'up', 'right', 'down', 'left', 'left', 'clear']
K += word('1+2+3+4+5+6+7+8+9+10+11+12+13+14+15+16+17+18+19+20') + ['left'] * 40
K += ['right'] * 40 + ['clear']
K += ['esc']
ti_system.KEYS[:] = K

OPS = []
paint = ti_draw.paint_buffer


def grab():
    OPS[:] = list(ti_draw._ops)
    paint()


ti_draw.paint_buffer = grab
bad = []
seen = [0]


def hook():
    m = None
    for name in ('casgui', 'ncasgui'):
        m = sys.modules.get(name)
        if m is not None and hasattr(m, 'ed_row'):
            break
    G = m.G
    orig = m.draw

    def draw():
        orig()
        if G['sel'] is not None or G.get('msg') == 'Working...':
            return
        bars = [o for o in OPS if o[0] == 'rect' and o[5] == ti_draw.CURSOR]
        if len(bars) != 1:
            return
        bar = bars[0][1]
        # the same line with a marker at the cursor
        keep = (G['row'], list(G['path']), G['pos'], G.get('hoff', 0))
        G['row'] = m.ed_cp(G['row'])
        m.ed_chars(MARK)
        G['pos'] -= 1
        G['hoff'] = keep[3]
        orig()
        G['row'], G['path'], G['pos'], G['hoff'] = keep
        xs = [o[1] for o in OPS if o[0] == 'text' and o[3] == MARK]
        seen[0] += 1
        if len(xs) != 1:
            bad.append('marker not drawn for %r' % m.ed_text())
        elif not (xs[0] - 2 <= bar <= xs[0] + 2):      # (the bug was 5 px right)
            bad.append('%r pos %d path %r: cursor at x=%d, the next character goes at x=%d'
                       % (m.ed_text(), keep[2], keep[1], bar, xs[0]))
    m.draw = draw


ti_system.HOOK.append(hook)
if where == 'onefile':
    import ncasgui
else:
    import cas
    try:
        cas.start()
    except KeyboardInterrupt:
        pass
if ti_system.KEYS:
    bad.append('keys left over: %r' % ti_system.KEYS[:4])
for b in bad[:12]:
    print('BAD: ' + b)
print('cursor check: %d screens, %s' % (seen[0], 'ok' if not bad else '%d FAILED' % len(bad)))
if bad or seen[0] < 50:
    sys.exit(1)
