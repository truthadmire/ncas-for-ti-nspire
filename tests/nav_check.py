# Checks the aviation calculator navcalc: formulas against known E6B values,
# every solvable choice of blank fields, and a key-driven session of the
# full-screen mode (with the stand-in ti_draw / ti_system in tests/mock).
#   python3 tests/nav_check.py [src|dist|onefile] [-v]
#   micropython tests/nav_check.py onefile
import sys
where = 'src'
for a in sys.argv[1:]:
    if a != '-v':
        where = a
verbose = '-v' in sys.argv
sys.path.insert(0, 'tests/mock')
sys.path.insert(0, where)
import ti_system
import ti_draw


def word(s):
    return list(s)


K = []
K += ['1'] + word('90') + ['enter'] + word('120') + ['enter'] + word('360') + ['enter'] + word('20')
SHOT_WIND = len(K)
K += ['down', 'down', 'right']                 # ground speed in mph
SHOT_MPH = len(K)
K += ['left', 'esc']
K += ['3'] + word('120') + ['down', 'down'] + word('1:30')   # TSD: 1:30 at 120 kt
SHOT_TSD = len(K)
K += ['up', 'up', 'clear', 'down'] + word('200')  # now solve the ground speed
SHOT_TSD2 = len(K)
K += ['esc', '2'] + word('27') + ['enter'] + word('300') + ['enter'] + word('15')
SHOT_XW = len(K)
K += ['esc', '9', '4', 'down'] + word('212')   # units: 212 F
SHOT_UNIT = len(K)
K += ['up'] + word('-40')                       # typing clears the other field
SHOT_UNIT2 = len(K)
K += ['esc', 'esc', '5'] + word('1..')
SHOT_BAD = len(K)
K += ['clear'] + word('5000') + ['enter'] + word('29.92') + ['enter'] + word('30')
SHOT_DA = len(K)
K += ['foo']
SHOT_FOO = len(K)
K += ['esc', 'a', 'x', 'b', 'q', 'esc', 'esc', 'esc']

ti_system.KEYS[:] = K
frames = []
orig = ti_draw.paint_buffer


def paint():
    orig()
    frames.append((len(K) - len(ti_system.KEYS), ti_draw.FRAMES[-1]))


ti_draw.paint_buffer = paint
if where == 'onefile':
    import navcalc as N      # runs navcalc() on import
else:
    import navcalc as N
    N.navcalc()


def frame(n):
    # the frame shown after the first n keys
    for k, f in frames:
        if k == n:
            return f
    return ''


bad = [0]
count = [0]


def check(name, ok, info=''):
    count[0] += 1
    if not ok:
        bad[0] += 1
        print('FAIL ' + name + (': ' + str(info) if info else ''))
    elif verbose:
        print('ok   ' + name)


def near(a, b, tol):
    return a is not None and abs(a - b) <= tol


def shot(name, n, *want):
    f = frame(n)
    for w in want:
        check(name + ' shows ' + w, w in f, '\n' + f)


shot('wind', SHOT_WIND, '080', '118.3', 'solved', '9.6° L')
shot('mph', SHOT_MPH, '136.2', 'mph')
shot('tsd', SHOT_TSD, '180.0', 'nm')
shot('tsd2', SHOT_TSD2, '133.3', '1:30')
shot('crosswind', SHOT_XW, '7.5', '13.0', 'right')
shot('unit', SHOT_UNIT, '100.0', '212')
shot('unit2', SHOT_UNIT2, '-40.0', '-40')
shot('bad number', SHOT_BAD, 'not a number')
shot('density alt', SHOT_DA, '7802', '5001')
shot('unknown key', SHOT_FOO, 'not used')
check('session used every key', not ti_system.KEYS, ti_system.KEYS)

# formulas (base units: kt, nm, ft, deg C, hPa, US gal, minutes)
W, XW, TSD, FUEL, ALT, TAS, TA, CB = N.TOOLS


def solved(t, vals):
    v, msg, done, ex = N.calc(t, vals)
    check(t['title'] + ' ' + repr(vals) + ' solves', msg == 'solved', msg)
    return v


v = solved(W, [90, 120, 360, 20, None, None, None])
check('wind: heading', near(v[4], 80.41, 0.01), v)
check('wind: ground speed', near(v[5], 118.32, 0.01), v)
v = solved(W, [90, 120, None, None, 80.40593, 118.32160, None])
check('find wind: direction', near(v[2] % 360, 0, 0.01) or near(v[2], 360, 0.01), v)
check('find wind: speed', near(v[3], 20, 0.001), v)
v = solved(W, [None, 120, 360, 20, None, 118.32160, None])
check('course from heading', N.resid(W, v) < 1e-6 and near(v[5], 118.32, 0.01), v)
v, msg, done, ex = N.calc(W, [90, 100, 360, 150, None, None, None])
check('wind stronger than the aircraft', msg == 'no solution', msg)
v = solved(XW, [N.parse('27', 'rwy', 0), 300, 15, None, None])
check('crosswind', near(v[3], 7.5, 1e-6) and near(v[4], 12.99, 0.01), v)
v = solved(XW, [270, None, None, 7.5, 12.990381])
check('wind from components', near(v[1], 300, 0.001) and near(v[2], 15, 0.001), v)
v, msg, done, ex = N.calc(XW, [None, None, 15, 7.5, 12.99])
check('runway and wind both blank', msg == 'these blanks need more info', msg)
v = solved(TSD, [None, 200, 90])
check('tsd ground speed', near(v[0], 133.333, 0.001), v)
v = solved(FUEL, [9.5, None, 38])
check('fuel endurance', near(v[1], 240, 1e-6), v)
v = solved(ALT, [5000, 1013.25, 30, None, None])
check('pressure alt', near(v[3], 5000, 0.01), v)
check('density alt', near(v[4], 7800.7, 0.5), v)
v = solved(ALT, [5000, N.parse('30.42', 'press', 0), 15, None, None])
check('pressure alt at 30.42 inHg', near(v[3], 4542, 3), v)
v = solved(ALT, [0, 1013.25, 15, None, None])
check('density alt ISA sea level', near(v[4], 0, 0.5), v)
v = solved(TAS, [150, 10000, N.isa(10000), None, None])
check('TAS from CAS', near(v[3], 174.05, 0.05) and near(v[4], 0.2727, 0.0005), v)
v = solved(TAS, [None, 35000, N.isa(35000), None, 0.8])
check('CAS from Mach', near(v[0], 271.9, 0.5), v)
v = solved(TA, [10000, -15, 0, None])
check('true altitude (cold)', near(v[3], 9620, 2), v)
v = solved(CB, [25, 15, None, 1000])
check('cloud base', near(v[2], 4000, 0.01), v)
v = solved(N.UTOOLS[3], [None, N.parse('212', 'temp', 1)])
check('212 F', near(v[0], 100, 1e-6), v)
check('h:mm', N.show(95.4, 'time') == '1:35' and N.parse('1:30', 'time', 0) == 90)
check('headings', N.show(359.7, 'hdg') == '360' and N.show(5, 'hdg') == '005')
check('runway number', N.parse('9', 'rwy', 0) == 90 and N.parse('270', 'rwy', 0) == 270)
check('inHg', N.show(1013.25, 'press', 0) == '29.92')

# every choice of blanks that can be solved comes back to the same values
import random
random.seed(7)
RANGE = {'hdg': (0, 360), 'spd': (60, 400), 'dist': (5, 500), 'time': (5, 300),
         'rate': (5, 60), 'alt': (0, 15000), 'temp': (-30, 40), 'press': (980, 1040),
         'ang': (-20, 20)}
# blank pairs that cannot be solved together (they enter the equations only
# through one combination)
UNDER = {'Crosswind': [(0, 1)], 'Altitudes / DA': [(0, 1), (2, 4)],
         'Airspeed / TAS': [(0, 1), (2, 3)]}


def combos(xs, k):
    if k == 0:
        return [()]
    out = []
    for i in range(len(xs)):
        for c in combos(xs[i + 1:], k - 1):
            out.append((xs[i],) + c)
    return out


tot = 0
for t in N.TOOLS + N.UTOOLS:
    fs = t['f']
    req = [i for i in range(len(fs)) if fs[i][2] is None]
    for trial in range(6):
        for attempt in range(50):
            v = []
            for f in fs:
                if f[1] == 'rwy':
                    v.append(random.randint(1, 36) * 10.0)
                elif f[1] in RANGE:
                    a, b = RANGE[f[1]]
                    v.append(a + (b - a) * random.random())
                else:
                    v.append(N.DEF[f[1]] * (0.5 + random.random()))
            for i in req[-t['n']:]:
                v[i] = None
            full, msg, d = N.solve(t, v)
            if msg == 'solved':
                break
        for c in combos(req, t['n']):
            if c in UNDER.get(t['title'], []):
                continue
            w = list(full)
            for i in c:
                w[i] = None
            r, msg, d = N.solve(t, w)
            tot += 1
            check('%s blanks %r' % (t['title'], c), msg == 'solved' and N.resid(t, r) < 1e-6,
                  (msg, full))
if verbose:
    print('%d blank combinations' % tot)

print('nav check: %d/%d' % (count[0] - bad[0], count[0]))
if bad[0]:
    sys.exit(1)
