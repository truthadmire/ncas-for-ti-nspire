# Desktop stand-in for TI's ti_draw module (tests only). It records what is
# drawn and turns every painted frame into text: each draw_text goes to the
# row its baseline falls in (18-pixel rows) at column x // 7; '|' marks the
# cursor (a red bar) and '*' starts a row with the selection colour.
W = 318
H = 212
FRAMES = []
_ops = []
_col = [(0, 0, 0)]
CURSOR = (220, 0, 0)
SELECT = (205, 225, 255)


def get_screen_dim():
    return (W, H)


def use_buffer():
    pass


def set_color(r, g, b):
    _col[0] = (r, g, b)


def fill_rect(x, y, w, h):
    _ops.append(('rect', x, y, w, h, _col[0]))


def draw_rect(x, y, w, h):
    pass


def draw_line(x1, y1, x2, y2):
    _ops.append(('line', x1, y1, x2, y2, _col[0]))


def clear(*a):
    del _ops[:]


def draw_text(x, y, s):
    _ops.append(('text', x, y, str(s), _col[0]))


def paint_buffer():
    FRAMES.append(render())


def render():
    rows = {}
    marks = {}
    for op in _ops:
        if op[0] == 'rect' and op[5] == SELECT:
            marks[(op[2] + 13) // 18] = '*'
    for op in _ops:
        if op[0] == 'text':
            r = (op[2] - 1) // 18
            rows.setdefault(r, []).append((op[1] // 7, op[3]))
        elif op[0] == 'rect' and op[5] == CURSOR:
            r = (op[2] + 12) // 18
            rows.setdefault(r, []).append(((op[1] + 1) // 7, '|'))
    out = []
    for r in range(H // 18 + 1):
        line = ''
        items = rows.get(r, [])
        items.sort(key=lambda t: t[0])
        for c, s in items:
            if len(line) < c:
                line += ' ' * (c - len(line))
            line += s
        out.append(marks.get(r, ' ') + line.rstrip())
    del _ops[:]
    return '\n'.join(out)
