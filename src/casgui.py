# casgui.py - full-screen graphical mode for nCAS on the TI-Nspire CX II
# (ti_draw + ti_system; loaded only when used).
#   type on the entry line, enter = evaluate, left/right = cursor,
#   up/down = pick an earlier input or result (enter copies it),
#   menu or tab = command menus, del = backspace, clear = clear line,
#   esc = leave the history / clear the line / quit on an empty line.
from cascore import CASError
from casfun import SET
from casout import fmt, OPT, TINAME
from casparse import parse

# Layout in pixels. The TI font is proportional: drawn text uses about AW
# pixels per character; the entry line puts each character in a CW cell so
# that the cursor position is exact. Text is drawn with its baseline BASE
# pixels below the top of its row (TI's DrawText anchors at the bottom left).
LH = 18
CW = 9
AW = 7
BASE = 14
MAXH = 30          # history entries
HISTCH = 6000      # history characters in all (a long result counts for many)
UNDON = 30         # undo steps
UNDOCH = 3000      # characters held by the undo steps in all

C_BAR = (30, 60, 130)
C_BART = (255, 255, 255)
C_TXT = (0, 0, 0)
C_RES = (0, 70, 170)
C_ERR = (190, 0, 0)
C_SEL = (205, 225, 255)
C_RULE = (215, 215, 215)
C_BOX = (240, 240, 240)
C_CUR = (220, 0, 0)
C_DIM = (110, 110, 110)

ENTER = ('enter', 'ret', 'return', 'center', '\r', '\n')
MENU = ('menu',)                    # command menus
TABKEYS = ('tab',)                  # next field
BACKTAB = ('shift+tab', 'shift tab', 'shifttab', 'backtab', 'btab')
CATKEYS = ('cat', 'catalog', 'book')  # A-Z command catalog
# keys whose name is not the text they should type (names that a key does
# not produce on a given OS are simply never used)
TEXT = {'space': ' ', 'sqrt': 'sqrt(', '√': 'sqrt(', 'pi': 'π',
'exp': 'e^', 'ln': 'ln(', 'log': 'log10(', 'square': '^2', '²': '^2',
        'ee': 'E', 'EE': 'E', 'ᴇ': 'E', 'neg': '-', '(-)': '-', '−': '-',
        '×': '*', '÷': '/', '≤': '<=', '≥': '>=', '≠': '/=',
        '→': '->', 'ans': 'ans', 'theta': 'θ', 'abs': 'abs(',
        'sin': 'sin(', 'cos': 'cos(', 'tan': 'tan(', 'sin⁻¹': 'arcsin(',
        'cos⁻¹': 'arccos(', 'tan⁻¹': 'arctan(', 'inf': 'inf',
        'i': 'i', 'e': 'e'}
TRIG = ('sin(', 'cos(', 'tan(', 'arcsin(', 'arccos(', 'arctan(',
        'sinh(', 'cosh(', 'tanh(', 'sec(', 'csc(', 'cot(')
NEEDANS = '+*/^'
KEYS = '123456789abcdefghijklmnop'

G = {}      # screen state: drawing functions, size, history, entry line


def rungui(run):
    G.setdefault('hist', [])
    key = findkey()
    try:
        import ti_draw
    except ImportError:
        ti_draw = None
    if key is None or ti_draw is None:
        # older systems: no way to read single keys (or to draw)
        return screen(run, key is None)
    G['d'] = ti_draw
    G['key'] = key
    G['cmode'] = 0
    G['gui'] = True
    try:
        w, h = ti_draw.get_screen_dim()
        w = int(w)
        h = int(h)
    except Exception:
        w, h = 318, 212
    G['w'] = w
    G['h'] = h
    G['rows'] = (h - 2 * LH - 5) // LH  # history rows between bar and entry line
    G['ncell'] = (w - 16) // CW         # entry-line cells
    G['wrap'] = (w - 12) // AW          # characters per history line
    ed_reset()
    G['sel'] = None
    G['top'] = None
    G['msg'] = ''
    try:
        ti_draw.use_buffer()
        G['buffer'] = True
    except Exception:
        G['buffer'] = False
    try:
        loop(run)
    except KeyboardInterrupt:
        pass
    return ''


# ---------------------------------------------------------------- keys

KEYFN = ('get_key', 'getkey', 'getKey', 'wait_key', 'waitkey')


def findkey():
    # the function that reads one key: ti_system.get_key on current systems;
    # other names and modules are tried for older or different systems
    for mn in ('ti_system', 'ti_draw', 'ti_plotlib'):
        try:
            m = __import__(mn)
        except ImportError:
            continue
        for fn in KEYFN:
            f = getattr(m, fn, None)
            if f is not None:
                return keyfun(f)
    return tibasic()


# Without a Python key function, TI-Basic's getKey() can be reached through
# ti_system.eval_function and a TI-Basic function ncaskey defined in the same
# problem (text in onefile/ncaskey.txt): ncaskey(0) returns 0, ncaskey(1)
# waits for a key and returns its first three characters (padded with
# spaces) as one number.
TINAMES = {'ent': 'enter', 'dow': 'down', 'lef': 'left', 'rig': 'right',
           'cle': 'clear', 'men': 'menu', 'tri': 'trig', 'hom': 'home',
           'ctr': 'ctrl', 'shi': 'shift', 'cen': 'center', 'ret': 'return',
           'squ': 'square', 'spa': 'space', 'sqr': 'sqrt', 'bac': 'backspace'}


def tibasic():
    try:
        import ti_system
        ev = ti_system.eval_function
    except (ImportError, AttributeError):
        return None
    try:
        if ev('ncaskey', 0) != 0:
            return None
    except Exception:
        return None

    def wait(x=1):
        c = int(ev('ncaskey', 1))
        s = ''
        for v in (c >> 32, (c >> 16) & 65535, c & 65535):
            s += chr(v)
        s = s.rstrip(' ') or ' '    # the key is padded with two spaces
        return TINAMES.get(s, s)
    return wait


def keyfun(f):
    # wait for a key: get_key(1) waits on current systems; where the
    # argument is not accepted, f() is polled
    try:
        from time import sleep
    except ImportError:
        sleep = None
    mode = [1]

    def wait(x=1):
        if mode[0]:
            try:
                return str(f(1))
            except TypeError:
                mode[0] = 0
        while True:
            k = f()
            if k:
                return str(k)
            if sleep:
                sleep(0.02)
    return wait


# ---------------------------------------------------------------- drawing

def color(c):
    # set_color(r, g, b); some versions may want one (r, g, b) tuple
    d = G['d']
    if G['cmode'] == 0:
        try:
            d.set_color(c[0], c[1], c[2])
            return
        except TypeError:
            G['cmode'] = 1
    d.set_color(c)


def text(x, y, s, c):
    color(c)
    G['d'].draw_text(x, y + BASE, s)


def box(x, y, w, h, c):
    color(c)
    G['d'].fill_rect(x, y, w, h)


def show():
    if G['buffer']:
        G['d'].paint_buffer()


def wrap(s, n):
    out = []
    while len(s) > n:
        out.append(s[:n])
        s = s[n:]
    out.append(s)
    return out


def selected():
    # (entry index, part) of the selected history item
    s = G['sel']
    if s is None:
        return None
    k = len(G['hist']) - 1 - s // 2
    return (k, 'out' if s % 2 == 0 else 'in')


def status():
    if G['msg']:
        return G['msg']
    n = callname()
    if n:
        import cashelp
        sy = cashelp.SYN.get(n.lower())
        if sy:
            return sy.split('\n')[0][:(G['w'] - 8) // CW]
    a = SET['angle'].upper()
    m = SET['mode'].upper()
    c = 'REAL' if SET['cplx'] == 'real' else 'CPLX'
    return 'nCAS  ' + a + ' ' + m + ' ' + c + ('   menu: commands' if G.get('gui') else '')


def callname():
    # the command whose '(' is open at the cursor (innermost first), for the
    # syntax hint in the status bar
    chain = []
    r = G['row']
    for i, sl in G['path']:
        chain.append((r, i))
        r = r[i][sl]
    chain.append((r, G['pos']))
    for r, p in reversed(chain):
        depth = 0
        j = min(p, len(r)) - 1
        while j >= 0:
            c = r[j]
            if c == ')':
                depth += 1
            elif c == '(':
                if depth:
                    depth -= 1
                else:
                    k = j
                    while k > 0 and type(r[k - 1]) is str and (r[k - 1].isalpha() or r[k - 1].isdigit()):
                        k -= 1
                    if k < j:
                        return ''.join(r[k:j])
            j -= 1
    return None


def draw():
    d = G['d']
    w = G['w']
    h = G['h']
    color((255, 255, 255))
    d.fill_rect(0, 0, w, h)
    # status bar
    box(0, 0, w, LH, C_BAR)
    text(4, 0, status(), C_BART)
    # history (above the entry area, whose height depends on the expression):
    # inputs on the left, results on the right, in 2D where possible
    wq, aq, dq = meas(G['row'])
    etop = h - (max(LH, aq + dq + 2) + 2) - 2
    avail = etop - LH - 4
    sel = selected()
    if sel is None:
        # only the newest entries that fit on the screen are laid out
        bl = []
        k = len(G['hist'])
        hh = 0
        while k > 0 and hh < avail:
            k -= 1
            eb = entry_blocks(k)
            hh += sum([b[2] for b in eb])
            bl = eb + bl
    else:
        bl = blocks(max(0, min(sel[0], G.get('hendk', sel[0])) - 8))
    if bl:
        if sel is None:
            end = len(bl) - 1
            start = startfor(bl, end, avail)
        else:
            idx = [i for i in range(len(bl)) if (bl[i][3], bl[i][4]) == sel]
            a = idx[0]
            b = idx[-1]
            G['tall'] = None
            if sum([bl[i][2] for i in idx]) > avail:
                # taller than the screen: up/down scroll through it
                n = fitfrom(bl, a, avail) - a + 1
                st = G.get('stop', 0)
                if st == 'end' or st > len(idx) - n:
                    st = len(idx) - n
                G['stop'] = max(0, st)
                start = a + G['stop']
                end = fitfrom(bl, start, avail)
                G['tall'] = (G['stop'], len(idx) - n)
            else:
                end = len(bl) - 1
                hk = G.get('hend')
                for j in range(len(bl)):
                    if (bl[j][3], bl[j][4]) == hk:
                        end = j
                start = startfor(bl, end, avail)
                if b > end:
                    end = b
                    start = startfor(bl, end, avail)
                if a < start:
                    start = a
                    end = fitfrom(bl, start, avail)
        G['hend'] = (bl[end][3], bl[end][4])
        G['hendk'] = bl[end][3]
        y = LH + 2
        last = None
        for i in range(start, end + 1):
            kind, data, bh, k, part = bl[i]
            if last is not None and k != last:
                box(2, y - 1, w - 4, 1, C_RULE)
            if sel is not None and (k, part) == sel:
                box(0, y, w, bh, C_SEL)
            if kind == '2d':
                r, rw, ra, rd, col = data
                G['ink'] = col
                rowdraw(r, 4 if part == 'in' else w - 6 - rw, y + 2 + ra, True)
                G['ink'] = C_TXT
            else:
                text(4, y, data[0], data[1])
            last = k
            y += bh
    # entry line (2D): its height follows the expression
    G['crow'] = ed_row()
    wq, aq, dq = meas(G['row'])
    hgt = max(LH, aq + dq + 2) + 2
    top = h - hgt - 2
    box(0, top - 1, w, hgt + 3, C_BOX)
    box(0, top - 2, w, 1, C_DIM)
    base = top + 2 + max(aq, A_)
    G['cxy'] = (0, base, A_, D_)
    rowdraw(G['row'], 0, base, False)
    cx = G['cxy'][0]
    hoff = G.get('hoff', 0)
    if cx - hoff > w - 16:
        hoff = cx - (w - 16)
    if cx - hoff < 0:
        hoff = max(0, cx - 20)
    G['hoff'] = hoff
    # the cursor keeps the place measured above (from x = 0); drawing the
    # row again must not move it, or it shows one character too far right
    cxy = G['cxy']
    rowdraw(G['row'], 6 - hoff, base, True)
    G['cxy'] = cxy
    if hoff > 0:
        box(0, top, 5, hgt, C_BOX)
        text(0, base - BASE, '<', C_DIM)
    if wq - hoff > w - 12:
        box(w - 8, top, 8, hgt, C_BOX)
        text(w - 7, base - BASE, '>', C_DIM)
    if G['sel'] is None:
        x, y, ca, cd = G['cxy']
        box(x + 5 - hoff, y - ca + 1, 2, ca + cd - 1, C_CUR)
    show()


# ---------------------------------------------------------------- editing

def insert(s, back=0):
    # insert s at the cursor, then move the cursor back 'back' characters;
    # template texts ('^', 'sqrt()', '()/()', ...) become 2D templates
    if not G['row'] and not G['path'] and s and s[0] in NEEDANS and G['hist']:
        ed_chars('ans')
    t = NODETEXT.get(s)
    if t is not None:
        ed_chars(t[0])
        ed_node(t[1], t[2])
        return
    ed_chars(s)
    G['pos'] = max(0, G['pos'] - back)


def evaluate(run, s):
    G['msg'] = 'Working...'
    if G.get('gui'):
        try:
            draw()
        except MemoryError:
            freemem(5)      # the input itself is still evaluated
    bad = False
    try:
        out = run(s)
    except CASError as ex:
        out = 'Error: ' + str(ex)
        bad = True
    except ZeroDivisionError:
        out = 'Error: Division by zero'
        bad = True
    except MemoryError:
        freemem(5)
        out = 'Error: Out of memory (history shortened, undo cleared; variables kept)'
        bad = True
    except RuntimeError:
        out = 'Error: Too complex'
        bad = True
    except KeyboardInterrupt:
        out = 'Interrupted'
        bad = True
    except Exception as ex:
        out = 'Error: ' + str(ex)
        bad = True
    G['msg'] = ''
    if out is None:
        out = ''
    G['hist'].append((s, out, bad))
    trimhist(MAXH, HISTCH)


def freemem(keep):
    # out of memory: drop everything that can be rebuilt or is only
    # convenience (layouts, undo, all but 'keep' history entries); the
    # user's variables and functions are kept
    G['lay'] = {}
    G['undo'] = []
    G['tinames'] = None
    G['typing'] = False
    trimhist(keep, 500 * keep)
    G['sel'] = None
    try:
        import gc
        gc.collect()
    except ImportError:
        pass


def trimhist(n, chars):
    # keep at most n entries and about 'chars' characters of history; the
    # 2D layouts of dropped entries go too
    h = G['hist']
    tot = sum([len(e[0]) + len(e[1]) for e in h])
    c = G.get('lay', {})
    while h and (len(h) > n or (tot > chars and len(h) > 1)):
        e = h.pop(0)
        tot -= len(e[0]) + len(e[1])
        c.pop(e[0], None)
        c.pop(e[1], None)


def loop(run):
    while True:
        try:
            step(run)
        except MemoryError:
            freemem(3)
            G['msg'] = 'Out of memory: history shortened, undo cleared'


def step(run):
    # one key: draw, read it, act on it
    draw()
    k = G['key'](1)
    G['msg'] = ''
    if not k:
        return
    # a run of typed characters is one undo step: the editor is copied
    # only at the first of them
    typing = len(k) == 1 and k not in ENTER
    before = None if typing and G.get('typing') else ed_snap()
    G['typing'] = typing
    a = ctrlaction(k)
    if a == 'wait':
        G['msg'] = 'ctrl  (next key: blue label)'
        return
    if a is not None:
        doaction(run, a, k)
    else:
        key(run, k)
    if before is not None and a != ('undo',) and ed_text() != before[3]:
        u = G.setdefault('undo', [])
        u.append(before)
        tot = sum([len(x[3]) for x in u])
        while u and (len(u) > UNDON or tot > UNDOCH):
            tot -= len(u.pop(0)[3])


def key(run, k):
    # one key without ctrl
    if k == 'esc':
        if G['sel'] is not None:
            G['sel'] = None
        elif G['row']:
            ed_reset()
        else:
            raise KeyboardInterrupt
    elif k in ENTER:
        if G['sel'] is not None:
            k2, part = selected()
            inp, res, bad = G['hist'][k2]
            G['sel'] = None
            insert(inp if part == 'in' else res.replace('\n ', '').replace('\n', ''))
        elif ed_text().strip():
            s = ed_text()
            ed_reset()
            special(run, s)
    elif k in ('up', 'down') and G['sel'] is None and ed_vert(1 if k == 'down' else -1):
        pass
    elif k == 'up' and G['sel'] is not None and G.get('tall') and G['tall'][0] > 0:
        G['stop'] = G['tall'][0] - 1
    elif k == 'down' and G['sel'] is not None and G.get('tall') and G['tall'][0] < G['tall'][1]:
        G['stop'] = G['tall'][0] + 1
    elif k == 'up':
        n = 2 * len(G['hist'])
        if n:
            G['sel'] = 0 if G['sel'] is None else min(G['sel'] + 1, n - 1)
            G['stop'] = 'end'
            G['tall'] = None
    elif k == 'down':
        if G['sel'] is not None:
            G['sel'] = None if G['sel'] == 0 else G['sel'] - 1
            G['stop'] = 0
            G['tall'] = None
    elif k == 'left':
        G['sel'] = None
        ed_left()
    elif k == 'right':
        G['sel'] = None
        ed_right()
    elif k in ('del', 'backspace'):
        G['sel'] = None
        ed_del()
    elif k == 'clear':
        G['sel'] = None
        ed_reset()
    elif k in MENU:
        G['sel'] = None
        r = menus()
        if r is not None:
            act(run, r)
    elif k in TABKEYS or k in BACKTAB:
        G['sel'] = None
        ed_tab(-1 if k in BACKTAB else 1)
    elif k in CATKEYS:
        G['sel'] = None
        catalog()
    elif k in TEMPLKEYS:
        G['sel'] = None
        templates()
    elif k in SYMKEYS:
        G['sel'] = None
        symbols()
    elif k == 'trig':
        G['sel'] = None
        j = choose('Trig', TRIG)
        if j is not None:
            insert(TRIG[j] + ')', 1)
    elif k in TEXT:
        G['sel'] = None
        t = TEXT[k]
        if t.endswith('('):
            insert(t + ')', 1)
        else:
            insert(t)
    elif len(k) == 1:
        G['sel'] = None
        ed_autoexit(k)
        insert(k)
    else:
        G['msg'] = 'key ' + repr(k) + ' not used'


# ctrl layer: the blue labels on the keypad. A system may report ctrl as a key
# of its own ('ctrl', then the next key), as a combined name ('ctrl+('), or
# send the finished symbol ('[]', '\u2248'); all three work. The doc key also
# acts as ctrl, in case a system reports neither.
CTRLKEYS = ('ctrl', 'doc')
CTRL = {'(': ('ins', '[]', 1), ')': ('ins', '{}', 1), '^': ('ins', 'root(,)', 2),
        '^2': ('ins', 'sqrt()', 1), 'e^': ('ins', 'ln()', 1), '10^': ('ins', 'log10()', 1),
        '=': ('rel',), 'trig': ('help',), 'del': ('clear',), 'clear': ('clear',),
        '-': ('ins', 'ans', 0), '*': ('ins', '""', 1), '/': ('ins', '()/()', 4),
        'enter': ('approx',), 'var': ('ins', '->', 0), 'esc': ('undo',),
        'cat': ('symbols',), 'catalog': ('symbols',), 'book': ('symbols',),
        'template': ('ins', ':=', 0), 'templates': ('ins', ':=', 0), 'templ': ('ins', ':=', 0),
        'tmpl': ('ins', ':=', 0), 'tab': ('menu',), 'menu': ('symbols',)}
DIRECT = {'[]': ('ins', '[]', 1), '{}': ('ins', '{}', 1), '""': ('ins', '""', 1),
          '()': ('ins', '()', 1), '\u2248': ('approx',), 'approx': ('approx',),
          'undo': ('undo',), 'sto': ('ins', '->', 0), 'sto\u2192': ('ins', '->', 0),
          'store': ('ins', '->', 0), '\u2254': ('ins', ':=', 0), ':=': ('ins', ':=', 0),
          'nroot': ('ins', 'root(,)', 2), 'root': ('ins', 'root(,)', 2), 'help': ('help',),
          '10^x': ('ins', '10^', 0), 'pow10': ('ins', '10^', 0), '10^': ('ins', '10^', 0)}
RELS = (('=', '='), ('\u2260  not equal', '/='), ('<', '<'), ('>', '>'),
        ('\u2264', '<='), ('\u2265', '>='), ('|  with', '|'), ('>>  convert', '>>'))
CTRLHELP = ('ctrl ( = [ ]      ctrl ) = { }', 'ctrl ^ = root      ctrl x\u00b2 = \u221a',
            'ctrl e^x = ln      ctrl 10^x = log10', 'ctrl = = \u2260 \u2264 \u2265 | >>',
            'ctrl (-) = ans     ctrl \u00d7 = " "', 'ctrl \u00f7 = fraction  ctrl var = \u2192',
            'ctrl enter = \u2248 decimal', 'ctrl del = clear   ctrl esc = undo',
            'ctrl catalog = Symbols', 'doc works as ctrl too')


def ctrlbase(k):
    # a key name in the form the CTRL table uses
    t = TEXT.get(k, k)
    return '10^' if k in ('10^x', 'pow10', '10^') else t


def ctrlaction(k):
    # 'wait' after ctrl itself, an action tuple, or None (an ordinary key)
    if G.get('ctrl'):
        G['ctrl'] = False
        return CTRL.get(ctrlbase(k)) or CTRL.get(k) or ('none', k)
    if k in CTRLKEYS:
        G['ctrl'] = True
        return 'wait'
    if len(k) > 4 and k[:4].lower() == 'ctrl':
        r = k[4:].lstrip('+-_ ')
        return CTRL.get(ctrlbase(r)) or CTRL.get(r) or ('none', k)
    return DIRECT.get(k)


def doaction(run, a, k):
    G['sel'] = None
    kind = a[0]
    if kind == 'ins':
        insert(a[1], a[2])
    elif kind == 'clear':
        ed_reset()
    elif kind == 'undo':
        u = G.get('undo')
        if u:
            ed_restore(u.pop())
    elif kind == 'approx':
        s = ed_text().strip()
        if not s and G['hist']:
            s = 'ans'
        if s:
            ed_reset()
            evaluate(run, 'approx(' + s + ')')
    elif kind == 'rel':
        j = choose('Relations', [r[0] for r in RELS])
        if j is not None:
            insert(RELS[j][1])
    elif kind == 'symbols':
        symbols()
    elif kind == 'menu':
        r = menus()
        if r is not None:
            act(run, r)
    elif kind == 'help':
        panel('ctrl keys', 'any key to close')
        for i in range(len(CTRLHELP)):
            text(10, LH + 4 + i * LH, CTRLHELP[i], C_TXT)
        show()
        G['key'](1)
    else:
        G['msg'] = 'ctrl+' + str(a[1]) + ' not used'


def special(run, s):
    low = s.strip().lower()
    if low in (':keys', 'keys'):
        keytest()
    elif low in (':clearhist', ':clearhistory'):
        G['hist'] = []
        G['undo'] = []
        G['lay'] = {}
        G['msg'] = 'History and undo cleared'
    elif low == ':free':
        freemem(0)
        G['msg'] = 'Freed: history, undo, ans (variables kept)'
        run(':clearans')
    elif low in ('q', 'quit', ':q'):
        raise KeyboardInterrupt
    else:
        evaluate(run, s)


def keytest():
    # shows the name of every key pressed (esc twice to stop)
    last = ''
    while True:
        d = G['d']
        color((255, 255, 255))
        d.fill_rect(0, 0, G['w'], G['h'])
        box(0, 0, G['w'], LH, C_BAR)
        text(4, 0, 'Key test: press keys, esc twice to stop', C_BART)
        text(10, 3 * LH, 'Last key:', C_DIM)
        text(10, 4 * LH + 4, repr(last), C_TXT)
        show()
        k = G['key'](1)
        if k == 'esc' and last == 'esc':
            return
        last = k


# ---------------------------------------------------------------- menus

def choose(title, labels, jump=False, hint=None):
    # a list to pick from: arrows + enter, or the key shown before an item
    # (jump: a letter goes to the next item starting with it, as in the
    # catalog; hint(i): a line shown under the list); returns the index or
    # None (esc / left)
    n = len(labels)
    i = 0
    rows = G['rows'] - 1 - (1 if hint else 0)
    top = 0
    w = G['w']
    while True:
        if i < top:
            top = i
        if i >= top + rows:
            top = i - rows + 1
        box(10, LH + 4, w - 20, (rows + 1) * LH + 6, C_DIM)
        box(11, LH + 5, w - 22, (rows + 1) * LH + 4, (255, 255, 255))
        box(11, LH + 5, w - 22, LH, C_BAR)
        text(16, LH + 5, title, C_BART)
        y = 2 * LH + 7
        for j in range(top, min(n, top + rows)):
            if j == i:
                box(12, y, w - 24, LH, C_SEL)
            key = KEYS[j] if j < len(KEYS) and not jump else ' '
            text(16, y, key, C_DIM)
            text(34, y, labels[j], C_TXT)
            y += LH
        if top + rows < n:
            text(w - 30, y - LH, 'v', C_DIM)
        if hint:
            box(12, y, w - 24, LH, C_BAR)
            text(16, y, (hint(i) or '')[:(w - 32) // CW], C_BART)
        show()
        k = G['key'](1)
        if k == 'up':
            i = (i - 1) % n
        elif k == 'down':
            i = (i + 1) % n
        elif k in ENTER or k == 'right':
            return i
        elif k in ('esc', 'left') or k in MENU:
            return None
        elif jump and len(k) == 1 and k.isalpha():
            c = k.lower()
            for d in range(1, n + 1):
                if labels[(i + d) % n][:1].lower() == c:
                    i = (i + d) % n
                    break
        elif not jump and len(k) == 1 and k in KEYS[:n]:
            return KEYS.index(k)


def menus():
    # main menu -> item; returns the item or None
    import casmenu
    main = casmenu.MAIN
    while True:
        a = choose('Menu', [m[0] for m in main] + ['Templates', 'Symbols'])
        if a is None:
            return None
        if a == len(main):
            templates()
            return None
        if a == len(main) + 1:
            symbols()
            return None
        title, items = main[a]
        b = choose(title, [it[0] for it in items])
        if b is not None:
            return items[b]


def act(run, item):
    # put the item's command on the entry line with the cursor where the
    # first value goes; commands without values run at once
    import casmenu
    label, tpl, prompts = item
    if not prompts:
        special(run, tpl)
        return
    vals = []
    mark = '\u0001'
    first = True
    for p in prompts:
        d = p[1]
        if d is None:
            v = '[]' if len(p) > 2 and p[2] == 'm' else ''
            if first:
                v = '[' + mark + ']' if v else mark
                first = False
        else:
            v = d
        vals.append(v)
    s = casmenu.fill(tpl, vals)
    i = s.find(mark)
    if i < 0:
        i = len(s)
    else:
        s = s[:i] + s[i + 1:]
    ed_chars(s)
    G['pos'] -= len(s) - i


# ---------------------------------------------------------------- no keys

def screen(run, nokeys=True):
    # For systems where a program cannot read single keys: a compact screen
    # in the Shell, redrawn after every entry. Type a command and press enter;
    # m = menus, #n = result n (for example #2*3), q = quit.
    G['gui'] = False
    G['msg'] = ''
    try:
        import ti_system
        have = [n for n in dir(ti_system) if n[0] != '_']
    except ImportError:
        have = None
    print('nCAS screen mode: this OS gives programs no single-key input.')
    if have is None:
        print('(no ti_system module)')
    else:
        print('ti_system: ' + ' '.join(have))
    rows = 4
    while True:
        hist = G['hist']
        print('-' * 30)
        first = max(0, len(hist) - rows)
        for k in range(first, len(hist)):
            inp, res, bad = hist[k]
            print('#' + str(k + 1) + ' ' + inp)
            for r in res.split('\n'):
                print('   ' + r)
        print(status() + '  m menu  q quit')
        try:
            s = input('> ').strip()
        except (EOFError, KeyboardInterrupt):
            return ''
        if s in ('q', 'quit', ':q'):
            return ''
        if s in ('m', 'menu'):
            cmd = pickmenu()
            if not cmd:
                continue
            print('> ' + cmd)
            s = cmd
        if not s:
            continue
        s = refs(s, hist)
        if s.strip().lower() in (':keys', 'keys'):
            print('No key reading on this OS.')
            continue
        evaluate(run, s)


def pickmenu():
    # numbered menus with the text-mode questions; returns the command
    import casmenu
    try:
        while True:
            k = casmenu.pick('nCAS menu', [m[0] for m in casmenu.MAIN])
            if k is None:
                return None
            title, items = casmenu.MAIN[k]
            j = casmenu.pick(title, [it[0] for it in items])
            if j is None:
                continue
            cmd = casmenu.build(items[j])
            if cmd:
                return cmd
    except casmenu.Quit:
        return None


def refs(s, hist):
    # #n in an entry stands for result n, in parentheses
    out = ''
    i = 0
    while i < len(s):
        if s[i] == '#' and i + 1 < len(s) and s[i + 1].isdigit():
            j = i + 1
            while j < len(s) and s[j].isdigit():
                j += 1
            n = int(s[i + 1:j])
            if 1 <= n <= len(hist) and not hist[n - 1][2]:
                out += '(' + hist[n - 1][1].split('\n')[0] + ')'
            else:
                out += s[i:j]
            i = j
        else:
            out += s[i]
            i += 1
    return out


# ---------------------------------------------------------------- templates

TEMPLKEYS = ('template', 'templates', 'templ', 'tmpl')
SYMKEYS = ('symbols', 'symbol', 'punc', '?!', '?!>', 'palette')
TPLS = ('Matrix m\u00d7n', 'Column vector', 'Row vector')

# the Symbols page: (shown, text typed, characters to step back, meaning).
# These cannot be typed while a program runs (the symbol palette is off).
SYMS = (
    (';', ';', 0, 'next row in a matrix [1,2;3,4]'), (',', ',', 0, 'separates arguments'),
    ('[ ]', '[]', 1, 'matrix or vector'), ('{ }', '{}', 1, 'list {1,2,3}'),
    ('( )', '()', 1, 'parentheses'), ('|', '|', 0, 'with: x^2|x=3'),
    ("'", "'", 0, "derivative in deSolve: y'"), ('" "', '""', 1, 'text'),
    ('=', '=', 0, 'equation'), ('\u2260', '/=', 0, 'not equal'),
    ('<', '<', 0, 'less than'), ('>', '>', 0, 'greater than'),
    ('\u2264', '<=', 0, 'less or equal'), ('\u2265', '>=', 0, 'greater or equal'),
    (':=', ':=', 0, 'define: f(x):=x^2'), ('\u2192', '->', 0, 'store: 5->a'),
    ('^', '^', 0, 'power'), ('^2', '^2', 0, 'square'),
    ('^-1', '^-1', 0, 'inverse: [1,2;3,4]^-1'), ('\u221a', 'sqrt()', 1, 'square root'),
    ('root', 'root(,)', 2, 'n-th root: root(8,3)'), ('!', '!', 0, 'factorial'),
    ('\u03c0', '\u03c0', 0, 'pi'), ('e', 'e', 0, "Euler's number"),
    ('i', 'i', 0, 'imaginary unit'), ('\u221e', 'inf', 0, 'infinity'),
    ('\u00b0', '\u00b0', 0, 'degrees: sin(30\u00b0)'), ('E', 'E', 0, 'times 10^: 2E3'),
    ('>>', '>>', 0, 'convert: pi>>Decimal'), ('%', '%', 0, 'percent'),
    ('and', ' and ', 0, 'both: x>0 and x<1'), ('or', ' or ', 0, 'either'),
    ('not', 'not ', 0, 'negation'), ('ans', 'ans', 0, 'last result'),
    (':', ':', 0, 'command: :deg :rad :test'), ('_', '_', 0, 'underscore'),
    ('&', '&', 0, 'join text'), ('x', 'x', 0, 'variable x'),
    ('y', 'y', 0, 'variable y'), ('t', 't', 0, 'variable t'),
)
SCOLS = 8


def templates():
    # Templates menu: matrix and vector grids
    j = choose('Templates', list(TPLS) + [t[0] for t in MATHTPL])
    if j is None:
        return
    if j >= len(TPLS):
        insert(MATHTPL[j - len(TPLS)][1])
        return
    fix = ('', 'c', 'r')[j]
    size = gridsize(3 if fix == 'c' else 2, 1 if fix == 'c' else (3 if fix == 'r' else 2), fix)
    if size is None:
        return
    s = grid(size[0], size[1])
    if s is None:
        return
    fillpair(s)


def fillpair(s):
    # put a matrix [ ... ] at the cursor; an empty [] at or next to the cursor
    # (det([|]), det(|[]), det([]|)) is filled instead of left behind
    r = ed_row()
    p = G['pos']
    for a in (p - 1, p, p - 2):
        if 0 <= a and a + 1 < len(r) and r[a] == '[' and r[a + 1] == ']':
            G['pos'] = a + 1
            s = s[1:-1]
            break
    ed_chars(s)


def symbols():
    # the Symbols page: a grid like the calculator's symbol palette;
    # arrows move, enter types the symbol, esc closes
    n = len(SYMS)
    rows = (n + SCOLS - 1) // SCOLS
    k0 = G.get('symk', 0)
    w = G['w']
    cw = (w - 8) // SCOLS
    ch = LH + 6
    while True:
        panel('Symbols', SYMS[k0][3])
        y0 = LH + 4
        for r in range(rows):
            for c in range(SCOLS):
                k = r * SCOLS + c
                if k >= n:
                    break
                x = 4 + c * cw
                y = y0 + r * ch
                box(x + 1, y + 1, cw - 2, ch - 2, C_SEL if k == k0 else C_BOX)
                lab = SYMS[k][0]
                text(x + max(2, (cw - len(lab) * AW) // 2), y + 2, lab, C_TXT)
        show()
        key = G['key'](1)
        if key == 'esc' or key in SYMKEYS or key in MENU:
            G['symk'] = k0
            return
        if key in ENTER:
            G['symk'] = k0
            t = SYMS[k0]
            insert(t[1], t[2])
            return
        if key == 'right':
            k0 = (k0 + 1) % n
        elif key == 'left':
            k0 = (k0 - 1) % n
        elif key == 'down':
            k0 = k0 + SCOLS if k0 + SCOLS < n else k0 % SCOLS
        elif key == 'up':
            if k0 - SCOLS >= 0:
                k0 -= SCOLS
            else:
                last = (rows - 1) * SCOLS + k0 % SCOLS
                k0 = last if last < n else last - SCOLS


def panel(title, hint):
    # a white panel over the screen with a title bar and a hint line
    w = G['w']
    h = G['h']
    color((255, 255, 255))
    G['d'].fill_rect(0, 0, w, h)
    box(0, 0, w, LH, C_BAR)
    text(4, 0, title, C_BART)
    box(0, h - LH - 2, w, LH + 2, C_BOX)
    text(4, h - LH - 2, hint, C_DIM)


def gridsize(r, c, fix):
    # choose the size: up/down rows, left/right columns, or type two digits
    # (rows then columns); enter = OK, esc = cancel
    typed = []
    while True:
        panel('Matrix size', 'arrows or digits, enter OK, esc cancel')
        text(20, 2 * LH, 'Rows: ' + str(r) + '    Columns: ' + str(c), C_TXT)
        cw = min(24, (G['w'] - 40) // max(c, 1))
        ch = min(16, (G['h'] - 6 * LH) // max(r, 1))
        for i in range(r):
            for j in range(c):
                box(20 + j * cw, 4 * LH + i * ch, cw - 3, ch - 3, C_SEL)
        show()
        k = G['key'](1)
        if k == 'esc':
            return None
        if k in ENTER:
            return (r, c)
        if k == 'up' and fix != 'r':
            r = min(9, r + 1)
        elif k == 'down' and fix != 'r':
            r = max(1, r - 1)
        elif k == 'right' and fix != 'c':
            c = min(9, c + 1)
        elif k == 'left' and fix != 'c':
            c = max(1, c - 1)
        elif len(k) == 1 and '1' <= k <= '9':
            if fix == 'c':
                r = int(k)
            elif fix == 'r':
                c = int(k)
            else:
                typed.append(int(k))
                if len(typed) == 1:
                    r = typed[0]
                else:
                    c = typed[1]
                    typed = []


def keytext(k):
    # the text a key types, or None
    if k in TEXT:
        return TEXT[k]
    if len(k) == 1:
        return k
    return None


def grid(r, c):
    # fill an r x c grid: type into the current cell, arrows or tab move,
    # del deletes, clear empties the cell, enter = done, esc = cancel;
    # empty cells become 0
    cells = [[''] * c for i in range(r)]
    i = 0
    j = 0
    w = G['w']
    cw = max(30, min(80, (w - 24) // c))
    ncw = max(1, (cw - 6) // AW)
    rows = G['rows']
    while True:
        panel('Matrix ' + str(r) + '\u00d7' + str(c),
              'tab/arrows move, enter done, esc cancel')
        top = max(0, i - rows + 2)
        y0 = LH + 6
        nshow = min(r - top, rows - 1)
        box(8, y0, 2, nshow * (LH + 4), C_TXT)
        box(8, y0, 5, 2, C_TXT)
        box(8, y0 + nshow * (LH + 4) - 2, 5, 2, C_TXT)
        x1 = 14 + c * cw
        box(x1, y0, 2, nshow * (LH + 4), C_TXT)
        box(x1 - 3, y0, 5, 2, C_TXT)
        box(x1 - 3, y0 + nshow * (LH + 4) - 2, 5, 2, C_TXT)
        for a in range(top, top + nshow):
            y = y0 + (a - top) * (LH + 4)
            for b in range(c):
                x = 14 + b * cw
                cur = (a == i and b == j)
                box(x + 1, y + 1, cw - 4, LH + 2, C_SEL if cur else C_BOX)
                t = cells[a][b]
                if len(t) > ncw:
                    t = t[-ncw:]
                text(x + 3, y + 2, t, C_TXT)
                if cur:
                    box(x + 3 + len(t) * AW, y + 3, 2, LH - 2, C_CUR)
        show()
        k = G['key'](1)
        if k == 'esc':
            return None
        if k in ENTER:
            return '[' + ';'.join([','.join([v or '0' for v in row]) for row in cells]) + ']'
        if k == 'tab' or k == 'right':
            j += 1
            if j == c:
                j = 0
                i = (i + 1) % r
        elif k == 'left':
            j -= 1
            if j < 0:
                j = c - 1
                i = (i - 1) % r
        elif k == 'down':
            i = (i + 1) % r
        elif k == 'up':
            i = (i - 1) % r
        elif k in ('del', 'backspace'):
            cells[i][j] = cells[i][j][:-1]
        elif k == 'clear':
            cells[i][j] = ''
        else:
            a = ctrlaction(k)
            if a is not None and a != 'wait' and a[0] == 'ins':
                t = a[1][:len(a[1]) - a[2]]     # '[]' -> '[', 'sqrt()' -> 'sqrt('
            elif a is not None:
                t = None
            else:
                t = keytext(k)
            if t is not None:
                cells[i][j] += t


# ---------------------------------------------------------------- 2D entry
# The entry line is a row: a list of characters and templates.
#   ['frac', num, den]  ['pow', exponent]  ['sqrt', x]  ['root', n, x]
#   ['abs', x]          (num, den, ... are rows themselves)
# The cursor is G['path'], a list of (index of a template, slot) from the top
# row down, and G['pos'], a position in that innermost row. ed_text() turns
# the row into the plain text nCAS reads: a fraction (3)/(x+1), x^2, sqrt(x).

A_ = 13         # character height above the baseline
D_ = 4          # below the baseline
AX = 5          # fraction bar above the baseline
RAISE = 8       # exponent baseline above the baseline

# texts that become templates: (characters typed first, template, prefill)
NODETEXT = {'^': ('', 'pow', ''), '^2': ('', 'pow', '2'), '^-1': ('', 'pow', '-1'),
            'sqrt()': ('', 'sqrt', ''), 'root(,)': ('', 'root', ''),
            '()/()': ('', 'frac', ''), 'abs()': ('', 'abs', ''),
            'e^': ('e', 'pow', ''), '10^': ('10', 'pow', ''),
            'integral()': ('', 'int', ''), 'integral(,,,)': ('', 'dint', ''),
            'd()': ('', 'der', '')}
MATHTPL = (('Fraction', '()/()'), ('Power  x^n', '^'), ('Square root', 'sqrt()'),
           ('n-th root', 'root(,)'), ('Absolute value', 'abs()'), ('e^x', 'e^'),
           ('Integral  \u222b f dx', 'integral()'), ('Definite integral  \u222b[a,b]', 'integral(,,,)'),
           ('Derivative  d/dx', 'd()'))
# calculus templates: the slots, which slot holds the variable (filled with
# x) and where the cursor starts
CALC = {'int': (2, 2, 1), 'dint': (4, 4, 1), 'der': (2, 1, 2)}
# typed in an exponent at its top level, these leave it first (x^2-5x)
EXITCHARS = '+-*/=<>,)'


def ed_reset():
    G['row'] = []
    G['path'] = []
    G['pos'] = 0
    G['hoff'] = 0


def ed_row():
    r = G['row']
    for i, sl in G['path']:
        r = r[i][sl]
    return r


def ed_parent():
    # the row holding the innermost template, and that template
    r = G['row']
    for i, sl in G['path'][:-1]:
        r = r[i][sl]
    return r, r[G['path'][-1][0]]


def ed_chars(s):
    r = ed_row()
    p = G['pos']
    for c in s:
        r.insert(p, c)
        p += 1
    G['pos'] = p


def ed_node(kind, pre=''):
    r = ed_row()
    p = G['pos']
    if kind in CALC:
        n, var, first = CALC[kind]
        node = [kind] + [[] for i in range(n)]
        node[var].append('x')
        r.insert(p, node)
        G['path'].append((p, first))
        G['pos'] = 0
        return
    n = 3 if kind in ('frac', 'root') else 2
    node = [kind] + [[] for i in range(n - 1)]
    for c in pre:
        node[1].append(c)
    r.insert(p, node)
    if pre:
        G['pos'] = p + 1        # x^2: the exponent is filled, stay outside
    else:
        G['path'].append((p, 1))
        G['pos'] = 0


def ed_empty(node):
    for sl in node[1:]:
        if sl:
            return False
    return True


def ed_right():
    r = ed_row()
    p = G['pos']
    if p < len(r):
        if type(r[p]) is str:
            G['pos'] = p + 1
        else:
            G['path'].append((p, 1))
            G['pos'] = 0
    elif G['path']:
        i, sl = G['path'][-1]
        par, node = ed_parent()
        if sl + 1 < len(node):
            G['path'][-1] = (i, sl + 1)
            G['pos'] = 0
        else:
            G['path'].pop()
            G['pos'] = i + 1


def ed_left():
    r = ed_row()
    p = G['pos']
    if p > 0:
        if type(r[p - 1]) is str:
            G['pos'] = p - 1
        else:
            node = r[p - 1]
            G['path'].append((p - 1, len(node) - 1))
            G['pos'] = len(node[-1])
    elif G['path']:
        i, sl = G['path'][-1]
        par, node = ed_parent()
        if sl > 1:
            G['path'][-1] = (i, sl - 1)
            G['pos'] = len(node[sl - 1])
        else:
            G['path'].pop()
            G['pos'] = i


def ed_vert(d):
    # down / up between the slots of the innermost template; False when the
    # cursor is not inside a template (then the arrows go to the history)
    if not G['path']:
        return False
    i, sl = G['path'][-1]
    par, node = ed_parent()
    k = node[0]
    if k in ('frac', 'root'):
        t = 2 if d > 0 else 1
        if t != sl:
            G['path'][-1] = (i, t)
            G['pos'] = min(G['pos'], len(node[t]))
    elif k == 'pow' and d > 0:
        G['path'].pop()
        G['pos'] = i + 1
    elif k == 'dint':
        # up: the upper limit, down: the lower limit
        t = 2 if d < 0 else 1
        if t != sl:
            G['path'][-1] = (i, t)
            G['pos'] = len(node[t])
    return True


def ed_del():
    r = ed_row()
    p = G['pos']
    if p > 0:
        it = r[p - 1]
        if type(it) is str or ed_empty(it):
            del r[p - 1]
            G['pos'] = p - 1
        else:
            G['path'].append((p - 1, len(it) - 1))
            G['pos'] = len(it[-1])
    elif G['path']:
        i, sl = G['path'].pop()
        par = ed_row()
        if ed_empty(par[i]):
            del par[i]
        G['pos'] = i


def ed_autoexit(c):
    # leave an exponent when a lower-precedence character is typed at its end
    if not G['path'] or c not in EXITCHARS:
        return
    par, node = ed_parent()
    r = ed_row()
    if node[0] != 'pow' or G['pos'] != len(r) or not r:
        return              # (an empty exponent keeps a leading minus: x^-1)
    depth = 0
    for it in r:
        if it == '(':
            depth += 1
        elif it == ')':
            depth -= 1
    if depth <= 0:
        G['pos'] = G['path'].pop()[0] + 1


def ed_text(row=None):
    if row is None:
        row = G['row']
    out = ''
    for it in row:
        if type(it) is str:
            out += it
            continue
        k = it[0]
        if k == 'frac':
            f = grp(ed_text(it[1]), True) + '/' + grp(ed_text(it[2]), False)
            out += f if len(row) == 1 else '(' + f + ')'
        elif k == 'pow':
            e = ed_text(it[1])
            out += '^' + (e if e.isdigit() or (len(e) == 1 and e.isalpha()) or enclosed(e)
                          else '(' + e + ')')
        elif k == 'sqrt':
            out += 'sqrt(' + ed_text(it[1]) + ')'
        elif k == 'root':
            out += 'root(' + ed_text(it[2]) + ',' + ed_text(it[1]) + ')'
        elif k == 'abs':
            out += 'abs(' + ed_text(it[1]) + ')'
        elif k == 'int':
            out += 'integral(' + ed_text(it[1]) + ',' + ed_text(it[2]) + ')'
        elif k == 'dint':
            lo, hi = ed_text(it[1]), ed_text(it[2])
            out += 'integral(' + ed_text(it[3]) + ',' + ed_text(it[4])
            out += (',' + lo + ',' + hi + ')') if lo or hi else ')'
        elif k == 'der':
            out += 'd(' + ed_text(it[2]) + ',' + ed_text(it[1]) + ')'
    return out


def enclosed(s):
    # '(x+1)': one pair of parentheses around everything
    if len(s) < 2 or s[0] != '(' or s[-1] != ')':
        return False
    depth = 0
    for i in range(len(s)):
        if s[i] == '(':
            depth += 1
        elif s[i] == ')':
            depth -= 1
            if depth == 0 and i < len(s) - 1:
                return False
    return True


def grp(s, num):
    # a fraction part needs no parentheses when it is one number or name
    ok = s != ''
    digits = True
    for c in s:
        if not (c.isdigit() or c == '.'):
            digits = False
        if not (c.isdigit() or c == '.' or c.isalpha()):
            ok = False
    if ok and not digits and not s.isalpha():
        ok = False              # 2x: keep (2x) so 1/(2x) stays a quotient
    i = s.find('(')
    if i > 0 and s[:i].isalpha() and enclosed(s[i:]):
        ok = True               # one function call: sqrt(2)
    return s if ok or enclosed(s) else '(' + s + ')'


def ed_cp(row):
    return [it if type(it) is str else [it[0]] + [ed_cp(r) for r in it[1:]] for it in row]


def ed_snap():
    return (ed_cp(G['row']), list(G['path']), G['pos'], ed_text())


def ed_restore(sn):
    G['row'] = sn[0]
    G['path'] = sn[1]
    G['pos'] = sn[2]


# measuring and drawing: a row is laid out on a baseline; each part reports
# (width, height above the baseline, depth below it)

def meas(row):
    if not row:
        return (9, A_, D_)
    w = 0
    a = A_
    d = D_
    for it in row:
        iw, ia, idd = measi(it)
        w += iw
        a = max(a, ia)
        d = max(d, idd)
    return (w, a, d)


def measi(it):
    if type(it) is str:
        return (CW, A_, D_)
    k = it[0]
    if k == 'frac':
        w1, a1, d1 = meas(it[1])
        w2, a2, d2 = meas(it[2])
        return (max(w1, w2) + 6, AX + 2 + a1 + d1, max(D_, 2 - AX + a2 + d2))
    if k == 'pow':
        w, a, d = meas(it[1])
        return (w + 2, max(A_, RAISE + a), max(D_, d - RAISE))
    if k == 'abs':
        w, a, d = meas(it[1])
        return (w + 7, a, d)
    if k == 'mat':
        cw, ra, rd, W, H = matsize(it[1])
        asc = H // 2 + AX
        return (W, asc + 1, H - asc + 1)
    if k == 'root':
        w, a, d = meas(it[2])
        wi, ai, di = meas(it[1])
        return (wi + w + 11, max(a + 3, RAISE + ai), d)
    if k in CALC:
        return calcbox(it)[0]
    w, a, d = meas(it[1])
    return (w + 11, a + 3, d)


def calcbox(it):
    # the size of an integral or derivative, and where its parts go
    k = it[0]
    if k == 'der':
        wx, ax, dx = meas(it[1])
        wf, af, df = meas(it[2])
        W = CW + wx + 6
        fa = AX + 2 + A_ + D_
        fd = max(D_, 2 - AX + ax + dx)
        return ((W + 2 * CW + wf + 2, max(fa, af), max(fd, df)), W)
    f, x = (it[1], it[2]) if k == 'int' else (it[3], it[4])
    wf, af, df = meas(f)
    wx, ax, dx = meas(x)
    a = max(af, A_) + 2
    d = max(df, D_) + 2
    wb = 0
    A = a
    D = d
    if k == 'dint':
        wl, al, dl = meas(it[1])
        wh, ah, dh = meas(it[2])
        wb = max(wl, wh) + 1
        A = a + 1 + ah + dh
        D = d + 1 + al + dl
    return ((9 + wb + wf + 3 + CW + wx, A, D), (a, d, wb))


def line(x1, y1, x2, y2):
    color(G.get('ink', C_TXT))
    try:
        G['d'].draw_line(x1, y1, x2, y2)
    except Exception:
        pass


def rowdraw(row, x, y, dr):
    # draw row with its baseline at y (dr False: only find the cursor)
    cur = row is G['crow']
    if not row:
        if dr:
            box(x + 1, y - A_ + 3, 7, 1, C_DIM)
            box(x + 1, y + D_ - 1, 7, 1, C_DIM)
            box(x + 1, y - A_ + 3, 1, A_ + D_ - 3, C_DIM)
            box(x + 7, y - A_ + 3, 1, A_ + D_ - 3, C_DIM)
        if cur:
            G['cxy'] = (x + 2, y, A_, D_)
        return 9
    x0 = x
    for i in range(len(row)):
        if cur and i == G['pos']:
            G['cxy'] = (x, y, A_, D_)
        x += itemdraw(row[i], x, y, dr)
    if cur and G['pos'] == len(row):
        G['cxy'] = (x, y, A_, D_)
    return x - x0


def itemdraw(it, x, y, dr):
    ink = G.get('ink', C_TXT)
    if type(it) is str:
        if dr:
            text(x, y - BASE, it, ink)
        return CW
    k = it[0]
    if k == 'frac':
        w1, a1, d1 = meas(it[1])
        w2, a2, d2 = meas(it[2])
        W = max(w1, w2) + 6
        by = y - AX
        if dr:
            box(x + 1, by, W - 2, 1, ink)
        rowdraw(it[1], x + (W - w1) // 2, by - 2 - d1, dr)
        rowdraw(it[2], x + (W - w2) // 2, by + 2 + a2, dr)
        return W
    if k == 'pow':
        return rowdraw(it[1], x + 1, y - RAISE, dr) + 2
    if k == 'mat':
        cw, ra, rd, W, H = matsize(it[1])
        top = y - (H // 2 + AX)
        if dr:
            for bx, tx in ((x + 1, x + 1), (x + W - 2, x + W - 4)):
                box(bx, top, 1, H, ink)
                box(tx, top, 3, 1, ink)
                box(tx, top + H - 1, 3, 1, ink)
        cy = top
        for i in range(len(it[1])):
            cx = x + 5
            r = it[1][i]
            for j in range(len(r)):
                w2 = meas(r[j])[0]
                rowdraw(r[j], cx + (cw[j] - w2) // 2, cy + ra[i], dr)
                cx += cw[j] + 8
            cy += ra[i] + rd[i] + 7
        return W
    if k in CALC:
        return calcdraw(it, x, y, dr, ink)
    xi = x
    if k == 'root':
        xi += rowdraw(it[1], x, y - RAISE, dr)
        rad = it[2]
    else:
        rad = it[1]
    w, a, d = meas(rad)
    if k == 'abs':
        if dr:
            box(xi + 1, y - a, 1, a + d, ink)
            box(xi + w + 5, y - a, 1, a + d, ink)
        rowdraw(rad, xi + 3, y, dr)
        return xi - x + w + 7
    if dr:
        top = y - a - 2
        line(xi, y - 4, xi + 2, y - 5)
        line(xi + 2, y - 5, xi + 4, y + d - 1)
        line(xi + 4, y + d - 1, xi + 8, top)
        line(xi + 8, top, xi + 10 + w, top)
    rowdraw(rad, xi + 9, y, dr)
    return xi - x + w + 11


def calcdraw(it, x, y, dr, ink):
    k = it[0]
    (W, A, D), geo = calcbox(it)
    if k == 'der':
        # d over d(var), then (f)
        fw = geo
        wx = meas(it[1])[0]
        by = y - AX
        if dr:
            box(x + 1, by, fw - 2, 1, ink)
            text(x + (fw - CW) // 2, by - 2 - D_ - BASE, 'd', ink)
            text(x + 3, by + 2 + A_ - BASE, 'd', ink)
        rowdraw(it[1], x + 3 + CW, by + 2 + A_, dr)
        xf = x + fw + 1
        if dr:
            text(xf, y - BASE, '(', ink)
        wf = rowdraw(it[2], xf + CW, y, dr)
        if dr:
            text(xf + CW + wf, y - BASE, ')', ink)
        return W
    a, d, wb = geo
    top = y - a
    bot = y + d
    if dr:
        # the integral sign: a long stroke with a hook at each end
        line(x + 5, top + 2, x + 3, bot - 2)
        line(x + 5, top + 2, x + 6, top)
        line(x + 6, top, x + 8, top + 1)
        line(x + 3, bot - 2, x + 2, bot)
        line(x + 2, bot, x, bot - 1)
    xb = x + 9
    if k == 'dint':
        wl, al, dl = meas(it[1])
        wh, ah, dh = meas(it[2])
        rowdraw(it[2], xb, top - 1 - dh, dr)
        rowdraw(it[1], xb, bot + 1 + al, dr)
        f, v = it[3], it[4]
    else:
        f, v = it[1], it[2]
    xf = xb + wb
    wf = rowdraw(f, xf, y, dr)
    if dr:
        text(xf + wf + 3, y - BASE, 'd', ink)
    rowdraw(v, xf + wf + 3 + CW, y, dr)
    return W


# ---------------------------------------------------------------- catalog

def catalog():
    # every command, A to Z: a letter jumps, enter types name() with the
    # cursor inside
    import cashelp
    names = []
    for key, title, words in cashelp.CATS:
        if key in ('conv', 'cmd'):
            continue
        for wd in words.split():
            if wd[0].isalpha() and wd not in names and okname(wd):
                names.append(wd)
    names.sort(key=lambda t: t.lower())
    def hint(i):
        sy = cashelp.SYN.get(names[i].lower())
        return sy.split('\n')[0] if sy else names[i] + '(...)'
    j = choose('Catalog: type a letter', names, True, hint)
    if j is not None:
        insert(names[j] + '()', 1)


def okname(wd):
    # letters, digits and _ only (MicroPython has no str.isalnum)
    for c in wd:
        if not (c.isalpha() or c.isdigit() or c == '_'):
            return False
    return True


# ---------------------------------------------------------------- tab fields

def ed_stops():
    # every cursor position in reading order: (path, pos, is it a field?)
    # Fields: the end of each template slot, and the place after each comma
    # (the next argument of a command such as integral(f,x,a,b)).
    out = []

    def walk(row, path):
        for i in range(len(row) + 1):
            out.append((path, i, (i > 0 and row[i - 1] == ',') or (bool(path) and i == len(row))))
            if i < len(row) and type(row[i]) is not str:
                for sl in range(1, len(row[i])):
                    walk(row[i][sl], path + [(i, sl)])
    walk(G['row'], [])
    return out


def ed_tab(d):
    # tab: the next field (after the last one, the end of the line);
    # shift+tab: the previous field
    ps = ed_stops()
    cur = 0
    for j in range(len(ps)):
        if ps[j][0] == G['path'] and ps[j][1] == G['pos']:
            cur = j
    t = len(ps) - 1 if d > 0 else 0
    if d > 0:
        for j in range(cur + 1, len(ps)):
            if ps[j][2]:
                t = j
                break
    else:
        for j in range(cur - 1, -1, -1):
            if ps[j][2]:
                t = j
                break
    G['path'] = list(ps[t][0])
    G['pos'] = ps[t][1]



# ---------------------------------------------------------------- 2D results
# A printed result (or input) is read back with the parser and laid out in
# 2D: fractions stacked, powers raised, roots, matrices as grids. Anything
# that is not plainly an expression (messages, DMS, polar form, := , ->) is
# left as text, so the picture never says something the text does not.

SAFE = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_+-*/^().,;=<>{}[]! \u221a\u03c0\u221e\u2260\u2264\u2265\u03b8\u222b'
SHOW = {'pi': '\u03c0', 'inf': '\u221e', 'theta': '\u03b8'}
SHOWF = {'sumseq': '\u03a3', 'prodseq': '\u03a0', 'integral': '\u222b'}
REL2 = {'=': '=', '/=': '\u2260', '<': '<', '>': '>', '<=': '\u2264', '>=': '\u2265'}
DOT = '\u00b7'


def anyfunc(n):
    return True


def tolayout(s):
    # the 2D row for a printed expression, or None (show it as text)
    c = G.setdefault('lay', {})
    if s in c:
        return c[s]
    t = s.replace('\n ', '').replace('\n', '')
    ok = t != '' and len(t) < 400
    for ch in t:
        if ch not in SAFE:
            ok = False
            break
    if ok:
        u = t.replace(' and ', '').replace(' or ', '').replace(' xor ', '').replace('not ', '')
        if ' ' in u:
            ok = False
    r = None
    if ok:
        try:
            r = []
            lay(parse(t, anyfunc), r)
            w, a, d = meas(r)
            r = (r, w, a, d)            # measured once, drawn many times
        except Exception:
            r = None
    if len(c) > 60:
        keep = {}
        for e in G.get('hist', [])[-10:]:
            for t2 in e[:2]:
                if t2 in c:
                    keep[t2] = c[t2]
        c.clear()
        c.update(keep)
    c[s] = r
    return r


def prec(t):
    if type(t) is not tuple:
        return 5
    h = t[0]
    if h in ('+', '-'):
        return 1
    if h in ('*', 'neg'):
        return 2
    if h == '^':
        return 4
    if h in REL2:
        return 0
    if h in ('and', 'or', 'xor', 'not'):
        return -1
    return 5


def layp(t, out, need):
    if need:
        out.append('(')
        lay(t, out)
        out.append(')')
    else:
        lay(t, out)


def sublay(t):
    r = []
    lay(t, r)
    return r


def lay(t, out):
    tt = type(t)
    if tt is int:
        out.extend(list(str(t)))
        return
    if tt is float:
        out.extend(list(fmt(t)))
        return
    if tt is str:
        out.extend(list(SHOW.get(t, t)))
        return
    h = t[0]
    if h == '+' or h == '-':
        lay(t[1], out)
        out.append(h)
        layp(t[2], out, prec(t[2]) <= (1 if h == '-' else 0)
             or (type(t[2]) is tuple and t[2][0] == 'neg'))
    elif h == '*':
        layp(t[1], out, prec(t[1]) < 2)
        out.append(DOT)
        layp(t[2], out, prec(t[2]) < 2 or (type(t[2]) is tuple and t[2][0] == 'neg'))
    elif h == 'neg':
        out.append('-')
        layp(t[1], out, prec(t[1]) <= 1)
    elif h == '/':
        out.append(['frac', sublay(t[1]), sublay(t[2])])
    elif h == '^':
        b = t[1]
        need = prec(b) < 5 or (type(b) is tuple and (b[0] == '/' or (b[0] == 'call' and b[1] in ('sqrt', 'root'))))
        layp(b, out, need)
        out.append(['pow', sublay(t[2])])
    elif h == 'call':
        name = t[1]
        args = t[2:]
        if name == 'sqrt' and len(args) == 1:
            out.append(['sqrt', sublay(args[0])])
        elif name == 'root' and len(args) == 2:
            out.append(['root', sublay(args[1]), sublay(args[0])])
        elif name == 'abs' and len(args) == 1:
            out.append(['abs', sublay(args[0])])
        elif name == 'integral' and len(args) == 2:
            out.append(['int', sublay(args[0]), sublay(args[1])])
        elif name == 'integral' and len(args) == 4:
            out.append(['dint', sublay(args[2]), sublay(args[3]), sublay(args[0]), sublay(args[1])])
        elif name == 'd' and len(args) == 2:
            out.append(['der', sublay(args[1]), sublay(args[0])])
        else:
            nm = SHOWF.get(name) if OPT['uni'] else None
            out.extend(list(nm or tiname(name)))
            out.append('(')
            for i in range(len(args)):
                if i:
                    out.append(',')
                lay(args[i], out)
            out.append(')')
    elif h == 'list':
        out.append('{')
        for i in range(1, len(t)):
            if i > 1:
                out.append(',')
            lay(t[i], out)
        out.append('}')
    elif h == 'mat':
        out.append(['mat', [[sublay(c) for c in r[1:]] for r in t[1:]]])
    elif h in REL2:
        lay(t[1], out)
        out.extend(list(REL2[h]))
        lay(t[2], out)
    elif h in ('and', 'or', 'xor'):
        lay(t[1], out)
        out.extend(list(' ' + h + ' '))
        lay(t[2], out)
    elif h == 'not':
        out.extend(list('not '))
        layp(t[1], out, prec(t[1]) < 0)
    elif h == '!':
        layp(t[1], out, prec(t[1]) < 5 or type(t[1]) is tuple and t[1][0] == '/')
        out.append('!')
    else:
        raise ValueError('no 2D form')


def tiname(name):
    # TI capitalization of a command name (eigvc -> eigVc), from the catalog
    c = G.get('tinames')
    if c is None:
        import cashelp
        c = {}
        for key, title, words in cashelp.CATS:
            for wd in words.split():
                c[wd.lower()] = wd
        c.update(TINAME)
        G['tinames'] = c
    return c.get(name, name)


def matsize(rows):
    nc = max([len(r) for r in rows])
    cw = [0] * nc
    ra = []
    rd = []
    for r in rows:
        a = A_
        d = D_
        for j in range(len(r)):
            w, ca, cd = meas(r[j])
            cw[j] = max(cw[j], w)
            a = max(a, ca)
            d = max(d, cd)
        ra.append(a)
        rd.append(d)
    W = sum(cw) + 8 * (nc - 1) + 10
    H = sum(ra) + sum(rd) + 7 * (len(rows) - 1)
    return cw, ra, rd, W, H


def blocks(first=0):
    # the history from entry 'first' on as display blocks:
    # (kind, data, height, entry, part)
    out = []
    for k in range(first, len(G['hist'])):
        out += entry_blocks(k)
    return out


def entry_blocks(k):
    out = []
    n = G['wrap']
    w = G['w']
    inp, res, bad = G['hist'][k]
    for part, s, col in (('in', inp, C_TXT), ('out', res, C_ERR if bad else C_RES)):
        lt = None if bad else tolayout(s)
        if lt is not None:
            r, rw, ra, rd = lt
            if rw <= w - 10 and ra + rd + 4 <= G['h'] - 3 * LH - 8:
                out.append(('2d', (r, rw, ra, rd, col), ra + rd + 4, k, part))
                continue
        pre = '  ' if part == 'out' else ''
        for line in s.split('\n'):
            for t in wrap(line, n - len(pre)):
                out.append(('txt', (pre + t, col), LH, k, part))
    return out


def startfor(bl, end, avail):
    # first block of a window that ends with block 'end'
    hh = 0
    i = end
    while i >= 0 and hh + bl[i][2] <= avail:
        hh += bl[i][2]
        i -= 1
    return min(i + 1, end)


def fitfrom(bl, start, avail):
    # last block of a window that starts with block 'start'
    hh = 0
    i = start
    while i < len(bl) and hh + bl[i][2] <= avail:
        hh += bl[i][2]
        i += 1
    return max(start, i - 1)
