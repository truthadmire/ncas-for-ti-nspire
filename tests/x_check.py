# Checks the exact calculator ncasx (src/casx.py or onefile/ncasx.py).
#   python3 tests/x_check.py [src|onefile]      micropython tests/x_check.py onefile
import sys
where = sys.argv[1] if len(sys.argv) > 1 else 'src'
sys.path.insert(0, where)
if where == 'onefile':
    import ncasx as X       # runs xcalc() on import; stdin must be empty
else:
    import casx as X
CASES = [
    ('1/3+1/6', '1/2  ≈ 0.5'), ('sqrt(8)', '2*√2  ≈ 2.828427125'),
    ('sin(pi/3)', '√3/2  ≈ 0.8660254038'), ('ln(e^2)', '2'), ('15!', '1307674368000'),
    ('nCr(10,3)', '120'), ('factor(360)', '2^3*3^2*5'), ('(x+1)^2|x=2', '9'),
    ('a:=5', '5'), ('a^2+1', '26'), ('f(x):=x^2+1', 'Done'), ('f(3)', '10'), ('ans/7', '10/7  ≈ 1.428571429'),
    ('deg', 'Degree mode'), ('sin(30)', '1/2  ≈ 0.5'), ('arcsin(1/2)', '30'), ('rad', 'Radian mode'),
    ('1/(1+sqrt(2))', '√2-1  ≈ 0.4142135624'), ('e^(i*pi)', '-1'), ('log(8,2)', '3'),
    ('mod(2^(10^9),7)', '2'), ('2^(10^9)', '2^1000000000'), ('sqrt(2)>1.4', 'true'),
    ('expand((x+1)^3)', 'x^3+3*x^2+3*x+1'), ('100!/98!', '9900'), ('(2/3)^-2', '9/4  ≈ 2.25'),
]
bad = 0
for q, want in CASES:
    try:
        got = X.run(q)
    except Exception as ex:
        got = 'EXC ' + str(ex)
    if got != want:
        bad += 1
        print('FAIL %s -> %r (want %r)' % (q, got, want))
print('x check: %d/%d' % (len(CASES) - bad, len(CASES)))
if bad:
    sys.exit(1)
