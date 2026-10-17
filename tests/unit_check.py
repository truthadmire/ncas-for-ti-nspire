# Checks the unit converter unitconv: conversions against exact or published
# values, the unit tables, number formatting, and a key-driven session of
# the full-screen mode (with the stand-in ti_draw / ti_system in tests/mock).
#   python3 tests/unit_check.py [src|dist|onefile] [-v]
#   micropython tests/unit_check.py onefile
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
K += ['1'] + ['down'] * 6 + ['1']               # Length: 1 mile
SHOT_MI = len(K)
K += ['down', 'del', 'del']                     # nmi row: edit its result
SHOT_DEL = len(K)
K += ['esc', '5']                               # Temperature starts at 20 C
SHOT_TEMP0 = len(K)
K += ['clear', '(-)'] + word('40')              # -40 C
SHOT_TEMP = len(K)
K += ['down', 'clear'] + word('500') + ['(-)']  # -500 F
SHOT_ZERO = len(K)
K += ['esc', 'e']                               # Fuel economy: 7.5 L/100 km
SHOT_FUEL = len(K)
K += ['up', 'clear', '0']                       # 0 km/L
SHOT_FUEL0 = len(K)
K += ['down', 'clear', '0']                     # 0 L/100 km
SHOT_FUEL1 = len(K)
K += ['esc', '1', 'clear'] + word('1..')
SHOT_BAD = len(K)
K += ['clear'] + word('1.5') + ['EE', '(-)', '3']   # 1.5E-3 nmi
SHOT_EE = len(K)
K += ['right', 'right', 'left', 'foo']
SHOT_FOO = len(K)
K += ['esc', 'h', 'any', 'i', 'x', 'esc', 'esc', '1', '?', 'any', 'esc', 'esc']

ti_system.KEYS[:] = K
frames = []
orig = ti_draw.paint_buffer


def paint():
    orig()
    frames.append((len(K) - len(ti_system.KEYS), ti_draw.FRAMES[-1]))


ti_draw.paint_buffer = paint
if where == 'onefile':
    import unitconv as U      # runs unitconv() on import
else:
    import unitconv as U
    U.unitconv()


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


def shot(name, n, *want):
    f = frame(n)
    for w in want:
        check(name + ' shows ' + w, w in f, '\n' + f)


def line(n, has):
    # the frame line that contains has
    for s in frame(n).split('\n'):
        if has in s:
            return s
    return ''


def typed(name, n, s):
    # s is on the row with the cursor (the typed row)
    check(name + ' typed ' + s, '|' in line(n, s), '\n' + frame(n))


shot('mile', SHOT_MI, '1609.344', 'Mile', '1.609344', '5280', '11/15', '= 1 mi')
typed('mile', SHOT_MI, 'Mile ')
shot('edit result', SHOT_DEL, '12/15')
typed('edit result', SHOT_DEL, '0.8689762419')
shot('temperature', SHOT_TEMP0, '68', '293.15', '= 20 °C')
shot('-40', SHOT_TEMP, '233.15')
typed('-40', SHOT_TEMP, 'Celsius')
check('-40 F', '-40' in line(SHOT_TEMP, '°F'), line(SHOT_TEMP, '°F'))
shot('absolute zero', SHOT_ZERO, 'below absolute zero')
typed('absolute zero', SHOT_ZERO, '-500')
shot('fuel', SHOT_FUEL, '31.361944', '13.333333')
typed('fuel', SHOT_FUEL, '7.5')
z = line(SHOT_FUEL0, 'L/100km').replace('Litres/100 km', '').replace('L/100km', '')
check('0 km/L: no L/100 km', not [c for c in z if c in '0123456789'], z)
shot('0 L/100 km', SHOT_FUEL1, 'no value for 0 L/100km')
shot('bad number', SHOT_BAD, 'not a number')
shot('exponent', SHOT_EE, '2.778', '0.002778')
typed('exponent', SHOT_EE, '1.5E-3')
shot('unknown key', SHOT_FOO, 'not used')
check('session used every key', not ti_system.KEYS, ti_system.KEYS)
check('help screen drawn', [f for k, f in frames if 'unitconv help' in f])
check('key test drawn', [f for k, f in frames if 'Key test' in f and "'x'" in f])


# conversions
def conv(cat, frm, x, to):
    us = U.units([c[0] for c in U.CATS].index(cat))[0]
    sy = [u[1] for u in us]
    return U.frombase(U.tobase(x, us[sy.index(frm)]), us[sy.index(to)])


def near(name, got, want, rel=1e-9):
    check(name, abs(got - want) <= rel * abs(want) + 1e-300, (got, want))


near('1 mi = 1609.344 m', conv('Length', 'mi', 1, 'm'), 1609.344)
near('1 nmi = 1852 m', conv('Length', 'nmi', 1, 'm'), 1852)
near('1 ft = 12 in', conv('Length', 'ft', 1, 'in'), 12)
near('1 ly in au', conv('Length', 'ly', 1, 'au'), 63241.077, 1e-7)
near('1 pc in ly', conv('Length', 'pc', 1, 'ly'), 3.2615638, 1e-7)
near('1 acre = 4046.8564224 m2', conv('Area', 'acre', 1, 'm²'), 4046.8564224)
near('1 mi2 = 640 acre', conv('Area', 'mi²', 1, 'acre'), 640)
near('1 US gal = 3.785411784 L', conv('Volume', 'US gal', 1, 'L'), 3.785411784)
near('1 US gal = 128 fl oz', conv('Volume', 'US gal', 1, 'US floz'), 128)
near('1 US cup = 48 tsp', conv('Volume', 'cup', 1, 'tsp'), 48)
near('1 UK gal = 160 UK fl oz', conv('Volume', 'UK gal', 1, 'UK floz'), 160)
near('1 bbl = 42 US gal', conv('Volume', 'bbl', 1, 'US gal'), 42)
near('1 lb = 0.45359237 kg', conv('Mass', 'lb', 1, 'kg'), 0.45359237)
near('1 lb = 16 oz', conv('Mass', 'lb', 1, 'oz'), 16)
near('1 lb = 7000 gr', conv('Mass', 'lb', 1, 'gr'), 7000)
near('1 st = 14 lb', conv('Mass', 'st', 1, 'lb'), 14)
near('1 US ton = 2000 lb', conv('Mass', 'US ton', 1, 'lb'), 2000)
near('1 UK ton = 2240 lb', conv('Mass', 'UK ton', 1, 'lb'), 2240)
near('212 F = 100 C', conv('Temperature', '°F', 212, '°C'), 100)
near('100 C = 373.15 K', conv('Temperature', '°C', 100, 'K'), 373.15)
near('-40 C = -40 F', conv('Temperature', '°C', -40, '°F'), -40)
near('0 F in R', conv('Temperature', '°F', 0, '°R'), 459.67)
near('1 yr = 365.25 d', conv('Time', 'yr', 1, 'd'), 365.25)
near('1 wk = 10080 min', conv('Time', 'wk', 1, 'min'), 10080)
near('1 kn = 1.852 km/h', conv('Speed', 'kn', 1, 'km/h'), 1.852)
near('60 mph = 88 ft/s', conv('Speed', 'mph', 60, 'ft/s'), 88)
near('1 atm = 101325 Pa', conv('Pressure', 'atm', 1, 'Pa'), 101325)
near('1 atm in psi', conv('Pressure', 'atm', 1, 'psi'), 14.6959488, 1e-8)
near('1 atm = 760 Torr', conv('Pressure', 'atm', 1, 'Torr'), 760)
near('1013.25 hPa in inHg', conv('Pressure', 'hPa', 1013.25, 'inHg'), 29.9212, 1e-5)
near('1 kWh = 3.6E6 J', conv('Energy', 'kWh', 1, 'J'), 3.6e6)
near('1 kcal = 1000 cal', conv('Energy', 'kcal', 1, 'cal'), 1000)
near('1 therm = 100000 BTU', conv('Energy', 'thm', 1, 'BTU'), 99976.13, 1e-6)
near('1 hp = 550 ft lbf/s', conv('Power', 'hp', 1, 'ftlbf/s'), 550)
near('1 hp in W', conv('Power', 'hp', 1, 'W'), 745.69987, 1e-8)
near('1 lbf = 16 ozf', conv('Force', 'lbf', 1, 'ozf'), 16)
near('1 kgf = 9.80665 N', conv('Force', 'kgf', 1, 'N'), 9.80665)
near('1 rad in degrees', conv('Angle', 'rad', 1, '°'), 57.2957795131, 1e-11)
near('1 turn = 400 grad', conv('Angle', 'turn', 1, 'grad'), 400)
near('1 GiB = 1073741824 B', conv('Data size', 'GiB', 1, 'B'), 1073741824)
near('1 MB = 8 Mbit', conv('Data size', 'MB', 1, 'Mbit'), 8)
near('30 mpg US in L/100 km', conv('Fuel economy', 'mpg US', 30, 'L/100km'), 7.84049, 1e-5)
near('5 L/100 km in km/L', conv('Fuel economy', 'L/100km', 5, 'km/L'), 20)
near('1 mpg UK in mpg US', conv('Fuel economy', 'mpg UK', 1, 'mpg US'), 0.83267418, 1e-7)
near('water: 1 g/cm3 in lb/ft3', conv('Density', 'g/cm³', 1, 'lb/ft³'), 62.427961, 1e-7)
near('1 lb/in3 = 1728 lb/ft3', conv('Density', 'lb/in³', 1, 'lb/ft³'), 1728)
near('60 rpm = 1 Hz', conv('Frequency', 'rpm', 60, 'Hz'), 1)
near('1 Hz = 2 pi rad/s', conv('Frequency', 'Hz', 1, 'rad/s'), 6.283185307, 1e-9)

# the tables
import random
random.seed(5)
check('categories have menu keys', len(U.CATS) <= len(U.KEYS) - 2)
for c in range(len(U.CATS)):
    title = U.CATS[c][0]
    us, start, first = U.units(c)
    sy = [u[1] for u in us]
    check(title + ': symbols unique', len(set(sy)) == len(sy), sy)
    check(title + ': symbols fit', max([len(s) for s in sy]) <= U.UW, sy)
    check(title + ': labels fit', max([len(u[0]) for u in us]) <= 22)
    check(title + ': starting value', U.convert(us, start, first)[1] == '')
    for u in us:
        check(title + ' ' + u[1] + ': factor positive', u[2] > 0)
        for t in range(20):
            x = (random.random() * 2 - 0.5) * 10 ** random.randint(-6, 9)
            if u[4] and x == 0:
                continue
            y = U.frombase(U.tobase(x, u), u)
            if abs(y - x) > 1e-12 * abs(x) + 1e-9 * abs(u[3]):
                check(title + ' ' + u[1] + ' round trip', 0, (x, y))
                break

# formatting and typed text
FMT = [(0, '0'), (1, '1'), (-2.5, '-2.5'), (0.1 + 0.2, '0.3'), (1e-7, '1E-7'),
       (1.5e12, '1.5E12'), (-1.234e-5, '-1.234E-5'), (123456789.0, '123456789'),
       (1609.344, '1609.344'), (2.0 / 3, '0.66666667'), (999999999.7, '1E9'),
       (0.001, '0.001'), (-1e-20, '-1E-20'), (1e400, 'inf')]
for x, want in FMT:
    check('fmt %r' % x, U.fmt(x) == want, U.fmt(x))
check('fmt 12 digits', U.fmt(2.0 / 3, 12) == '0.666666666667', U.fmt(2.0 / 3, 12))
check('parse partial', U.parse('1.5E-') == 1.5 and U.parse('-') is None and U.parse('') is None)
try:
    U.parse('1..')
    check('parse 1..', 0)
except ValueError:
    check('parse 1..', 1)

print('unit check: %d/%d' % (count[0] - bad[0], count[0]))
if bad[0]:
    sys.exit(1)
