# navcalc.py - aviation flight calculator (E6B) for the TI-Nspire CX II.
# Full-screen with ti_draw + ti_system.get_key; a text version otherwise.
# Every tool is a form: type the values you know, leave the others blank,
# and the blank ones are solved as you type. Any field can be the blank one
# (the wind triangle also finds the wind, time-speed-distance any of the
# three, ...).
#   up/down/tab/enter = field, left/right = unit, del = backspace,
#   clear = blank the field, (-) = sign, esc/menu = back to the tool list
import math

VERSION = '1.0'
RAD = math.pi / 180

# Layout in pixels (as in casgui): text is drawn with its baseline BASE
# pixels below the top of its row; drawn text uses about AW pixels per
# character (the TI font is proportional).
LH = 18          # title and status bars, menu rows
RH = 17          # form rows
BASE = 14
AW = 7

C_BAR = (30, 60, 130)
C_BART = (255, 255, 255)
C_TXT = (0, 0, 0)
C_RES = (0, 70, 170)
C_ERR = (190, 0, 0)
C_SEL = (205, 225, 255)
C_DIM = (110, 110, 110)
C_CUR = (220, 0, 0)
C_WHITE = (255, 255, 255)

ENTER = ('enter', 'ret', 'return', 'center', '\r', '\n')
MENU = ('menu',)
BACKTAB = ('shift+tab', 'shift tab', 'shifttab', 'backtab', 'btab')
DELKEYS = ('del', 'backspace', 'bksp')
NEG = ('-', 'neg', '(-)', '−', '⁻')
KEYS = '123456789abcdefghijklmnop'

# ---------------------------------------------------------------- units
# kind -> units (name, factor, offset, decimals); shown = base*factor+offset.
# Base units: kt, nm, ft, deg C, hPa, US gal, US gal/h, minutes, degrees.
LBKG = 0.45359237
AVGAS = 6.0      # lb per US gal
JETA = 6.7
UNITS = {
    'spd': (('kt', 1.0, 0, 1), ('mph', 1.150779, 0, 1), ('km/h', 1.852, 0, 1)),
    'dist': (('nm', 1.0, 0, 1), ('sm', 1.150779, 0, 1), ('km', 1.852, 0, 1)),
    'alt': (('ft', 1.0, 0, 0), ('m', 0.3048, 0, 0)),
    'temp': (('°C', 1.0, 0, 1), ('°F', 1.8, 32, 1)),
    'press': (('inHg', 1 / 33.8639, 0, 2), ('hPa', 1.0, 0, 1)),
    'fuel': (('USG', 1.0, 0, 1), ('L', 3.785412, 0, 1), ('Imp gal', 0.832674, 0, 1),
             ('lb Avgas', AVGAS, 0, 0), ('kg Avgas', AVGAS * LBKG, 0, 0),
             ('lb Jet-A', JETA, 0, 0), ('kg Jet-A', JETA * LBKG, 0, 0)),
    'rate': (('gph', 1.0, 0, 1), ('L/h', 3.785412, 0, 1),
             ('pph Avgas', AVGAS, 0, 0), ('pph Jet-A', JETA, 0, 0)),
    'time': (('h:mm', 1.0, 0, 0), ('min', 1.0, 0, 1), ('h', 1 / 60.0, 0, 2)),
    'hdg': (('°', 1.0, 0, 0),),
    'ang': (('°', 1.0, 0, 1),),
    'mach': (('M', 1.0, 0, 3),),
}
UNITS['sspd'] = UNITS['spd']        # signed speed (wind components)
UNITS['rwy'] = UNITS['hdg']         # runway: 27 means 270 degrees
HDG = ('hdg', 'rwy')
POS = ('spd', 'dist', 'time', 'fuel', 'rate', 'mach', 'press')
# starting guesses for the solver
DEF = {'spd': 100.0, 'sspd': 10.0, 'dist': 100.0, 'time': 60.0, 'fuel': 20.0,
       'rate': 10.0, 'alt': 3000.0, 'temp': 15.0, 'press': 1013.25, 'mach': 0.3,
       'hdg': 0.0, 'rwy': 0.0, 'ang': 0.0}
ARITH = (ValueError, ZeroDivisionError, OverflowError, TypeError)


def fmtnum(x, dec):
    s = ('%.' + str(dec) + 'f') % x
    if s[:1] == '-' and float(s) == 0:
        s = s[1:]
    return s


def hmm(m):
    if abs(m) > 1e7:
        return fmtnum(m, 0)
    t = int(math.floor(abs(m) + 0.5))
    return ('-' if m < 0 and t else '') + '%d:%02d' % (t // 60, t % 60)


def show(x, kind, u=0):
    # a base value as text in unit u of its kind
    if kind in HDG:
        r = int(math.floor(x % 360 + 0.5)) % 360
        return '%03d' % (r or 360)
    un = UNITS[kind][u]
    if un[0] == 'h:mm':
        return hmm(x)
    return fmtnum(x * un[1] + un[2], un[3])


def edtext(x, kind, u):
    # a base value as text to keep editing (after a unit change)
    un = UNITS[kind][u]
    if un[0] == 'h:mm':
        return hmm(x)
    s = fmtnum(x * un[1] + un[2], un[3] + 2)
    if '.' in s:
        s = s.rstrip('0').rstrip('.')
    return s


def tdiff(x, u):
    # a temperature difference in unit u
    return fmtnum(x * UNITS['temp'][u][1], 1) + ' ' + UNITS['temp'][u][0]


def withunit(x, kind, u):
    return show(x, kind, u) + ' ' + UNITS[kind][u][0]


def parse(s, kind, u):
    # typed text -> base value (ValueError if it is not a number)
    if ':' in s:
        if kind != 'time':
            raise ValueError
        a, b = s.split(':', 1)
        m = abs(float(a or '0')) * 60 + float(b or '0')
        return -m if s[:1] == '-' else m
    x = float(s)
    if kind == 'rwy' and '.' not in s and 'E' not in s and 0 < x <= 36:
        x *= 10
    un = UNITS[kind][u]
    return (x - un[2]) / un[1]


def norm180(a):
    a = a % 360
    return a - 360 if a > 180 else a


def pw(a, b):
    # a**b for real numbers only (a negative base would give a complex result)
    if a < 0:
        raise ValueError
    return a ** b


# ---------------------------------------------------------------- atmosphere
# ICAO standard atmosphere (troposphere), feet and hPa.
P0 = 1013.25
T0 = 288.15
KF = 6.8755856e-6       # lapse rate / T0 per foot
A0 = 661.4786           # speed of sound at sea level, kt


def delta(pa):
    # pressure ratio at pressure altitude pa
    return pw(1 - KF * pa, 5.2558797)


def isa(pa):
    return 15 - 0.0019812 * pa


def palt(ia, qnh):
    return ia + (1 - pw(qnh / P0, 0.190284)) / KF


def dalt(pa, oat):
    sigma = delta(pa) / ((oat + 273.15) / T0)
    return (1 - pw(sigma, 0.234969)) / KF


def sound(oat):
    return 38.967854 * math.sqrt(oat + 273.15)


def cas2mach(cas, pa):
    qc = pw(1 + 0.2 * (cas / A0) ** 2, 3.5) - 1
    return math.sqrt(5 * (pw(qc / delta(pa) + 1, 2 / 7.0) - 1))


# ---------------------------------------------------------------- tools
# field: (label, kind, default, first unit, fixed unit); default None means
# the field is solved when blank, otherwise a blank field uses the default.

def F(label, kind, default=None, unit=0, fixed=0):
    return (label, kind, default, unit, fixed)


def T(title, fields, n, eqs, extra=None, fast=None, one=0):
    # n equations eqs(values) -> residuals (scaled to about 1 per unit of
    # error that matters); fast(values, blanks) -> solution, False (none) or
    # None (use Newton); one: a single input (typing clears the others)
    return {'title': title, 'f': fields, 'n': n, 'eqs': eqs, 'extra': extra,
            'fast': fast, 'one': one}


def sc(a):
    return math.sin(a * RAD), math.cos(a * RAD)


# wind triangle: air vector (TH, TAS) = ground vector (TC, GS) + wind (blowing
# from WD at WS, so towards WD+180)
VECS = ((4, 1, 1), (2, 3, -1), (0, 5, -1))     # (direction, size, sign)


def wind_eqs(v):
    x = y = 0.0
    for d, m, s in VECS:
        a, b = sc(v[d])
        x += s * v[m] * a
        y += s * v[m] * b
    return [x / 100, y / 100]


def wind_fast(v, bl):
    b = set(bl)
    for d, m, s in VECS:
        if b == set((d, m)):
            # one vector unknown: the sum of the other two
            x = y = 0.0
            for d2, m2, s2 in VECS:
                if d2 != d:
                    a, c = sc(v[d2])
                    x -= s2 * v[m2] * a / s
                    y -= s2 * v[m2] * c / s
            return [math.atan2(x, y) / RAD % 360, math.sqrt(x * x + y * y)][::1 if bl[0] == d else -1]
    if b == set((4, 5)):
        # heading and ground speed from course, TAS and wind
        a, c = sc(v[2] - v[0])
        if v[1] <= 0:
            return False
        s = v[3] * a / v[1]
        if abs(s) > 1:
            return False
        wca = math.asin(s) / RAD
        gs = v[1] * math.cos(wca * RAD) - v[3] * c
        if gs < 0:
            return False
        r = {4: (v[0] + wca) % 360, 5: gs}
        return [r[i] for i in bl]
    return None


def wind_extra(v, u):
    wca = norm180(v[4] - v[0])
    side = '' if abs(wca) < 0.05 else (' R' if wca > 0 else ' L')
    hw = v[3] * sc(v[2] - v[0])[1]
    return [('Wind corr. angle', fmtnum(abs(wca), 1) + '°' + side),
            ('Magnetic heading', show(v[4] - v[6], 'hdg') + '°'),
            ('Headwind' if hw >= -0.05 else 'Tailwind', withunit(abs(hw), 'spd', u[1]))]


def xw_eqs(v):
    a, c = sc(v[1] - v[0])
    return [(v[3] - v[2] * a) / 10, (v[4] - v[2] * c) / 10]


def xw_fast(v, bl):
    b = set(bl)
    if b == set((3, 4)):
        a, c = sc(v[1] - v[0])
        r = {3: v[2] * a, 4: v[2] * c}
    elif b == set((1, 2)):
        r = {1: (v[0] + math.atan2(v[3], v[4]) / RAD) % 360,
             2: math.sqrt(v[3] ** 2 + v[4] ** 2)}
    else:
        return None
    return [r[i] for i in bl]


def xw_extra(v, u):
    out = []
    if abs(v[3]) >= 0.05:
        out.append(('Crosswind from', 'right' if v[3] > 0 else 'left'))
    if v[4] < -0.05:
        out.append(('TAILWIND', withunit(-v[4], 'spd', u[2])))
    return out


def tsd_eqs(v):
    return [(v[1] - v[0] * v[2] / 60) / 100]


def tsd_extra(v, u):
    return [('Per minute', withunit(v[0] / 60, 'dist', u[1]))]


def fuel_eqs(v):
    return [(v[2] - v[0] * v[1] / 60) / 10]


def fuel_extra(v, u):
    return [('+45 min reserve', withunit(v[2] + v[0] * 0.75, 'fuel', u[2]))]


def alt_eqs(v):
    return [(v[3] - palt(v[0], v[1])) / 1000, (v[4] - dalt(v[3], v[2])) / 1000]


def alt_extra(v, u):
    t = isa(v[3])
    return [('ISA temperature', withunit(t, 'temp', u[2])),
            ('ISA deviation', tdiff(v[2] - t, u[2]))]


def tas_eqs(v):
    return [(v[4] - cas2mach(v[0], v[1])) * 10, (v[3] - v[4] * sound(v[2])) / 100]


def tas_extra(v, u):
    return [('ISA deviation', tdiff(v[2] - isa(v[1]), u[2])),
            ('Speed of sound', withunit(sound(v[2]), 'spd', u[3]))]


def ta_eqs(v):
    # temperature correction of an indicated altitude: the air column between
    # the station and the aircraft is taken as ISA shifted by the deviation
    # measured at the aircraft
    ia, oat, el, ta = v
    return [(ta - el - (ia - el) * (oat + 273.15) / (isa(ia) + 273.15)) / 1000]


def ta_extra(v, u):
    return [('ISA deviation', tdiff(v[1] - isa(v[0]), u[1])),
            ('Correction', withunit(v[3] - v[0], 'alt', u[3]))]


def cb_eqs(v):
    # convective cloud base: 400 ft per deg C of temperature/dew point spread
    return [(v[2] - (v[0] - v[1]) * 400) / 1000]


def cb_extra(v, u):
    return [('Base MSL', withunit(v[2] + v[3], 'alt', u[2])),
            ('Spread', tdiff(v[0] - v[1], u[0]))]


TOOLS = [
    T('Wind triangle', [F('True course', 'hdg'), F('True airspeed', 'spd'),
                        F('Wind from', 'hdg'), F('Wind speed', 'spd'),
                        F('True heading', 'hdg'), F('Ground speed', 'spd'),
                        F('Variation E+ W-', 'ang', 0.0)],
      2, wind_eqs, wind_extra, wind_fast),
    T('Crosswind', [F('Runway (27=270)', 'rwy'), F('Wind from', 'hdg'),
                    F('Wind speed', 'spd'), F('Crosswind (+R)', 'sspd'),
                    F('Headwind', 'sspd')],
      2, xw_eqs, xw_extra, xw_fast),
    T('Time speed distance', [F('Ground speed', 'spd'), F('Distance', 'dist'),
                              F('Time', 'time')], 1, tsd_eqs, tsd_extra),
    T('Fuel', [F('Fuel flow', 'rate'), F('Time', 'time'), F('Fuel', 'fuel')],
      1, fuel_eqs, fuel_extra),
    T('Altitudes / DA', [F('Indicated alt', 'alt'), F('Altimeter', 'press'),
                         F('OAT', 'temp'), F('Pressure alt', 'alt'),
                         F('Density alt', 'alt')], 2, alt_eqs, alt_extra),
    T('Airspeed / TAS', [F('CAS (IAS)', 'spd'), F('Pressure alt', 'alt'),
                         F('OAT', 'temp'), F('True airspeed', 'spd'),
                         F('Mach', 'mach')], 2, tas_eqs, tas_extra),
    T('True altitude', [F('Indicated alt', 'alt'), F('OAT at altitude', 'temp'),
                        F('Station elev', 'alt', 0.0), F('True altitude', 'alt')],
      1, ta_eqs, ta_extra),
    T('Cloud base', [F('Temperature', 'temp'), F('Dew point', 'temp'),
                     F('Base AGL', 'alt'), F('Field elev', 'alt', 0.0)],
      1, cb_eqs, cb_extra),
]


def unit_eqs(v):
    return [v[i] - v[0] for i in range(1, len(v))]


def unit_tool(title, kind, labels):
    fs = [F(labels[i], kind, None, i, 1) for i in range(len(labels))]
    return T(title, fs, len(fs) - 1, unit_eqs, one=1)


UTOOLS = [
    unit_tool('Speed', 'spd', ('Knots', 'Miles/hour', 'Km/hour')),
    unit_tool('Distance', 'dist', ('Nautical mi', 'Statute mi', 'Kilometres')),
    unit_tool('Altitude', 'alt', ('Feet', 'Metres')),
    unit_tool('Temperature', 'temp', ('Celsius', 'Fahrenheit')),
    unit_tool('Pressure', 'press', ('Inches Hg', 'hPa / mb')),
    unit_tool('Fuel', 'fuel', ('US gallons', 'Litres', 'Imp gallons', 'Avgas 6.0 lb/g', 'Avgas',
                               'Jet-A 6.7 lb/g', 'Jet-A')),
    unit_tool('Fuel flow', 'rate', ('US gal/hour', 'Litres/hour', 'Avgas', 'Jet-A')),
]

# ---------------------------------------------------------------- solver


def resid(t, v):
    return max([abs(r) for r in t['eqs'](v)])


def solve(t, vals, last=None):
    # vals: base values, None = blank. Returns (values with the blanks
    # solved where possible, message, list of solved fields)
    fs = t['f']
    v = list(vals)
    bl = []
    for i in range(len(fs)):
        if v[i] is None:
            if fs[i][2] is None:
                bl.append(i)
            else:
                v[i] = fs[i][2]
    n = t['n']
    if len(bl) > n:
        k = len(bl) - n
        return v, 'enter %d more value%s' % (k, 's' if k > 1 else ''), []
    if len(bl) < n:
        if not bl:
            try:
                ok = resid(t, v) < 1e-6
            except ARITH:
                ok = False
            return v, ('all values agree' if ok else 'values disagree: clear one'), []
        return v, 'too many values: clear %d' % (n - len(bl)), []
    x = None
    if t['fast']:
        try:
            x = t['fast'](v, bl)
        except ARITH:
            x = None
        if x is False:
            return v, 'no solution', []
        if x is not None:
            x = fix(t, bl, x)
    sing = 0
    if x is None:
        ss = seeds(t, v, bl, last)
        for s in ss:
            x = newton(t, v, bl, s)
            if x == 'singular':
                sing += 1
                x = None
            elif x is not None:
                x = fix(t, bl, x)
                if x is not None:
                    break
    if x is None:
        if sing == len(ss):
            return v, 'these blanks need more info', []
        return v, 'no solution', []
    for j in range(len(bl)):
        v[bl[j]] = x[j]
    return v, 'solved', bl


def fix(t, bl, x):
    # normalized solution, or None if a value is out of its range
    out = []
    for j in range(len(bl)):
        k = t['f'][bl[j]][1]
        a = x[j]
        if a != a or abs(a) > 1e9:
            return None
        if k in HDG:
            a = a % 360
        elif k in POS:
            if a < -1e-9 or (k == 'press' and a <= 0):
                return None
            a = max(a, 0.0)
        elif k == 'temp' and a <= -273.15:
            return None
        out.append(a)
    return out


def cmean(angles):
    # mean direction of known headings (start for unknown ones)
    x = y = 0.0
    for a in angles:
        s, c = sc(a)
        x += s
        y += c
    if abs(x) + abs(y) < 1e-9:
        return 0.0
    return math.atan2(x, y) / RAD % 360


def seeds(t, v, bl, last):
    fs = t['f']
    hd = cmean([v[i] for i in range(len(fs)) if fs[i][1] in HDG and v[i] is not None])
    base = []
    for i in bl:
        k = fs[i][1]
        if last and last.get(i) is not None:
            base.append(last[i])
        elif k in HDG:
            base.append(hd)
        else:
            base.append(DEF[k])
    out = [base]
    hdg = [fs[i][1] in HDG for i in bl]
    if True in hdg:
        # equal unknown headings can make the Jacobian singular: spread them
        for r in (0, 90, 180, 270):
            out.append([base[j] + r + 20 * j if hdg[j] else base[j] for j in range(len(bl))])
    for f in (0.2, 4.0):
        out.append([base[j] if hdg[j] else base[j] * f for j in range(len(bl))])
    return out


def resvec(t, v, bl, x):
    w = list(v)
    for j in range(len(bl)):
        w[bl[j]] = x[j]
    return t['eqs'](w)


def newton(t, v, bl, x):
    # damped Newton with a numeric Jacobian; None if it does not converge
    n = len(bl)
    x = list(x)
    try:
        f = resvec(t, v, bl, x)
        nf = max([abs(r) for r in f])
    except ARITH:
        return None
    for it in range(40):
        if nf < 1e-10:
            return x
        cols = []
        for j in range(n):
            # central differences: accurate enough to tell a singular system
            h = 1e-5 * max(1.0, abs(x[j]))
            xp = list(x)
            xm = list(x)
            xp[j] += h
            xm[j] -= h
            try:
                fp = resvec(t, v, bl, xp)
                fm = resvec(t, v, bl, xm)
            except ARITH:
                fp = None
            if fp is None:
                try:
                    fp = resvec(t, v, bl, xp)
                    fm = f
                    h /= 2
                except ARITH:
                    return None
            cols.append([(fp[i] - fm[i]) / (2 * h) for i in range(n)])
        dx = gauss([[cols[j][i] for j in range(n)] + [-f[i]] for i in range(n)], n)
        if dx is None:
            # no unique solution near here (or the blanks depend on each other)
            return 'singular' if it == 0 else None
        lam = 1.0
        while True:
            xn = [x[j] + lam * dx[j] for j in range(n)]
            try:
                fn = resvec(t, v, bl, xn)
                nn = max([abs(r) for r in fn])
            except ARITH:
                nn = None
            if nn is not None and nn < nf:
                break
            lam /= 2
            if lam < 1e-3:
                return x if nf < 1e-8 else None
        x, f, nf = xn, fn, nn
    return x if nf < 1e-8 else None


def gauss(a, n):
    # solve the n x (n+1) augmented system a; None if singular
    big = 0.0
    for r in a:
        for e in r[:n]:
            big = max(big, abs(e))
    for c in range(n):
        p = c
        for r in range(c + 1, n):
            if abs(a[r][c]) > abs(a[p][c]):
                p = r
        if abs(a[p][c]) <= 1e-7 * big:
            return None
        a[c], a[p] = a[p], a[c]
        for r in range(n):
            if r != c:
                m = a[r][c] / a[c][c]
                for k in range(c, n + 1):
                    a[r][k] -= m * a[c][k]
    return [a[i][n] / a[i][i] for i in range(n)]


def calc(t, vals, last=None):
    # solve, then the extra result lines (for the screen and for tests)
    v, msg, done = solve(t, vals, last)
    ex = []
    if t['extra'] and None not in v:
        u = [f[3] for f in t['f']]
        try:
            ex = t['extra'](v, u)
        except ARITH:
            ex = []
    return v, msg, done, ex


# ---------------------------------------------------------------- screen

G = {}      # drawing functions, key function, screen size
MEM = {}    # each tool's fields while the program runs


def navcalc():
    key = findkey()
    try:
        import ti_draw
    except ImportError:
        ti_draw = None
    if key is None or ti_draw is None:
        print('navcalc: no full-screen mode here (%s), text version.'
              % ('no key function' if key is None else 'no ti_draw'))
        return textmode()
    G['d'] = ti_draw
    G['key'] = key
    G['cmode'] = 0
    try:
        w, h = ti_draw.get_screen_dim()
        w = int(w)
        h = int(h)
    except Exception:
        w, h = 318, 212
    G['w'] = w
    G['h'] = h
    try:
        ti_draw.use_buffer()
        G['buffer'] = True
    except Exception:
        G['buffer'] = False
    try:
        mainmenu()
    except KeyboardInterrupt:
        pass
    try:
        color(C_WHITE)
        ti_draw.fill_rect(0, 0, w, h)
        show_()
    except Exception:
        pass


MAIN = [t['title'] for t in TOOLS] + ['Units', 'Help', 'Key test']


def mainmenu():
    while True:
        a = choose('navcalc ' + VERSION + '   esc quits', MAIN)
        if a is None:
            return
        if a < len(TOOLS):
            form(TOOLS[a])
        elif MAIN[a] == 'Units':
            while True:
                b = choose('Units', [t['title'] for t in UTOOLS])
                if b is None:
                    break
                form(UTOOLS[b])
        elif MAIN[a] == 'Help':
            helpscreen()
        else:
            keytest()


KEYFN = ('get_key', 'getkey', 'getKey', 'wait_key', 'waitkey')


def findkey():
    # ti_system.get_key on current systems; other names for older ones
    for mn in ('ti_system', 'ti_draw', 'ti_plotlib'):
        try:
            m = __import__(mn)
        except ImportError:
            continue
        for fn in KEYFN:
            f = getattr(m, fn, None)
            if f is not None:
                return keyfun(f)
    return None


def keyfun(f):
    # get_key(1) waits; where the argument is not accepted, f() is polled
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


def color(c):
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


def show_():
    if G['buffer']:
        G['d'].paint_buffer()


def bars(title, status):
    w = G['w']
    h = G['h']
    box(0, 0, w, h, C_WHITE)
    box(0, 0, w, LH, C_BAR)
    text(4, 0, title, C_BART)
    box(0, h - LH, w, LH, C_BAR)
    text(4, h - LH, status[:(w - 8) // AW], C_BART)


def choose(title, labels):
    # a list to pick from: arrows + enter, or the key shown before an item;
    # returns the index or None (esc / left / menu)
    n = len(labels)
    i = G.get('ch', {}).get(title, 0)
    rows = (G['h'] - 2 * LH - 4) // LH
    top = 0
    while True:
        if i < top:
            top = i
        if i >= top + rows:
            top = i - rows + 1
        bars(title, 'enter or 1-9 a-p picks   esc back')
        y = LH + 2
        for j in range(top, min(n, top + rows)):
            if j == i:
                box(0, y, G['w'], LH, C_SEL)
            text(8, y, KEYS[j] if j < len(KEYS) else ' ', C_DIM)
            text(26, y, labels[j], C_TXT)
            y += LH
        if top + rows < n:
            text(G['w'] - 16, y - LH, 'v', C_DIM)
        show_()
        k = G['key'](1)
        if k == 'up':
            i = (i - 1) % n
        elif k == 'down':
            i = (i + 1) % n
        elif k in ENTER or k == 'right':
            break
        elif k in ('esc', 'left') or k in MENU:
            return None
        elif len(k) == 1 and k in KEYS[:n]:
            i = KEYS.index(k)
            break
    G.setdefault('ch', {})[title] = i
    return i


def newstate(t):
    return {'txt': ['' for f in t['f']], 'u': [f[3] for f in t['f']],
            'sel': 0, 'top': 0, 'last': {}}


def values(t, st):
    # typed texts -> base values; (values, index of a bad number or None)
    v = []
    bad = None
    for i in range(len(t['f'])):
        s = st['txt'][i]
        if s == '':
            v.append(None)
            continue
        try:
            v.append(parse(s, t['f'][i][1], st['u'][i]))
        except ValueError:
            v.append(None)
            if bad is None:
                bad = i
    return v, bad


def form(t):
    st = MEM.get(t['title'])
    if st is None:
        st = newstate(t)
        MEM[t['title']] = st
    msg = ''
    while True:
        vals, bad = values(t, st)
        if bad is not None:
            v, status, done, ex = vals, 'not a number: ' + t['f'][bad][0], [], []
        else:
            v, status, done, ex = calc(t, vals, st['last'])
            st['last'] = dict([(i, v[i]) for i in done])
        drawform(t, st, v, done, ex, msg or status, bad is not None or status[:2] in ('no', 'to', 'va'))
        msg = ''
        k = G['key'](1)
        r = formkey(t, st, k, v, done)
        if r == 'back':
            return
        if r:
            msg = r


def unitname(t, st, i):
    f = t['f'][i]
    return UNITS[f[1]][st['u'][i]][0]


def formkey(t, st, k, v, done):
    # one key on a form; returns 'back', a message, or None
    fs = t['f']
    n = len(fs)
    i = st['sel']
    s = st['txt'][i]
    if k in ('esc',) or k in MENU:
        return 'back'
    if k == 'up' or k in BACKTAB:
        st['sel'] = (i - 1) % n
    elif k in ('down', 'tab') or k in ENTER:
        st['sel'] = (i + 1) % n
    elif k in ('left', 'right'):
        us = UNITS[fs[i][1]]
        if fs[i][4] or len(us) < 2:
            return 'this field has one unit'
        old = st['u'][i]
        new = (old + (1 if k == 'right' else -1)) % len(us)
        if s:
            try:
                st['txt'][i] = edtext(parse(s, fs[i][1], old), fs[i][1], new)
            except ValueError:
                pass
        st['u'][i] = new
    elif k in DELKEYS:
        st['txt'][i] = s[:-1]
    elif k == 'clear':
        st['txt'][i] = ''
    elif k in NEG:
        if s[-1:] == 'E':
            st['txt'][i] = s + '-'
        elif s[:1] == '-':
            st['txt'][i] = s[1:]
        else:
            st['txt'][i] = '-' + s
    elif k in ('.', ':') or (len(k) == 1 and '0' <= k <= '9') or k in ('E', 'ee', 'EE'):
        c = 'E' if k in ('ee', 'EE') else k
        if c == ':' and fs[i][1] != 'time':
            return ': is only for times (h:mm)'
        if t['one']:
            for j in range(n):
                if j != i:
                    st['txt'][j] = ''
        if len(s) < 12:
            st['txt'][i] = s + c
    elif k in ('?', 'help', 'cat', 'catalog'):
        helpscreen()
    else:
        return 'key ' + repr(k)[:20] + ': not used here'
    return None


def drawform(t, st, v, done, ex, status, err):
    w = G['w']
    h = G['h']
    fs = t['f']
    n = len(fs)
    rows = (h - 2 * LH - 2) // RH
    total = n + len(ex)
    sel = st['sel']
    top = st['top']
    if sel < top:
        top = sel
    if sel >= top + rows:
        top = sel - rows + 1
    if sel == n - 1:
        top = max(top, min(sel, total - rows))
    st['top'] = top
    bars(t['title'], status)
    if err:
        box(0, h - LH, w, LH, C_ERR)
        text(4, h - LH, status[:(w - 8) // AW], C_BART)
    xv = w - 70          # right end of the values
    y = LH + 1
    for j in range(top, min(total, top + rows)):
        if j < n:
            f = fs[j]
            if j == sel:
                box(0, y, w, RH, C_SEL)
            text(6, y, f[0], C_TXT)
            s = st['txt'][j]
            c = C_TXT
            if s == '':
                if v[j] is None:
                    s, c = '?', C_DIM
                else:
                    s = show(v[j], f[1], st['u'][j])
                    c = C_RES if j in done else C_DIM
            text(xv - AW * len(s), y, s, c)
            if j == sel:
                box(xv + 1, y + 2, 2, RH - 4, C_CUR)
            text(xv + 6, y, unitname(t, st, j), C_DIM)
        else:
            lab, val = ex[j - n]
            text(6, y, lab, C_DIM)
            text(w - 6 - AW * len(val), y, val, C_RES)
        y += RH
    if top + rows < total:
        text(w - 12, y - RH, 'v', C_DIM)
    show_()


HELP = (
    'Type the values you know; blank',
    'fields (?) are solved as you type.',
    'up/down/tab/enter   next field',
    'left/right   change the unit',
    'del  backspace    clear  blank field',
    '(-)  sign    esc/menu  tool list',
    'Blue = solved. Grey = default.',
    'Runway 27 = 270. Time 1:30 or 90.',
    'Variation: East +, West -.',
    'IAS is taken as CAS.',
)


def helpscreen():
    bars('navcalc help', 'press any key')
    y = LH + 1
    for s in HELP:
        text(6, y, s, C_TXT)
        y += RH
    show_()
    G['key'](1)


def keytest():
    last = ''
    while True:
        bars('Key test', 'esc twice to stop')
        text(10, 3 * LH, 'Last key:', C_DIM)
        text(10, 4 * LH + 4, repr(last), C_TXT)
        show_()
        k = G['key'](1)
        if k == 'esc' and last == 'esc':
            return
        last = k


# ---------------------------------------------------------------- text mode

def textmode():
    # the same tools with input(): blank = solve this field
    all_ = TOOLS + UTOOLS
    while True:
        print('')
        for i in range(len(all_)):
            print('%2d %s%s' % (i + 1, all_[i]['title'], ' (units)' if i >= len(TOOLS) else ''))
        s = input('tool number (q quits): ').strip()
        if s in ('q', 'quit', ''):
            return
        try:
            t = all_[int(s) - 1]
        except (ValueError, IndexError):
            continue
        vals = []
        for f in t['f']:
            un = UNITS[f[1]][f[3]][0]
            while True:
                a = input('%s [%s]: ' % (f[0], un)).strip()
                if a == '':
                    vals.append(None)
                    break
                try:
                    vals.append(parse(a, f[1], f[3]))
                    break
                except ValueError:
                    print('not a number')
        v, msg, done, ex = calc(t, vals)
        print('-- ' + msg)
        for i in range(len(t['f'])):
            f = t['f'][i]
            if v[i] is not None:
                print('%-17s %s %s%s' % (f[0], show(v[i], f[1], f[3]),
                                         UNITS[f[1]][f[3]][0], '  *' if i in done else ''))
        for lab, val in ex:
            print('%-17s %s' % (lab, val))


if __name__ == '__main__':
    navcalc()
