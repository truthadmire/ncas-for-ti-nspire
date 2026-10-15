# Property-based correctness checks on random inputs (CPython).
import sys, random, signal
sys.path.insert(0, 'src')
import cas
from cascore import *
from casparse import parse
import cascalc as CA, caspoly as PO, cassolve as SO, casmat as MA

random.seed(int(sys.argv[1]) if len(sys.argv) > 1 else 7)
N = int(sys.argv[2]) if len(sys.argv) > 2 else 200

def E(s):
    return cas.ev(parse(s, cas.isfunc))

def numeq(a, b, var='x', pts=(0.37, 1.21, 2.53)):
    ok = 0
    for p in pts:
        try:
            va = nval(a, {var: p})
            vb = nval(b, {var: p})
        except Exception:
            continue
        if abs(va - vb) > 1e-6 * (1 + abs(va) + abs(vb)):
            return False
        ok += 1
    return ok > 0

def rpoly(deg, var='x'):
    return '+'.join(['(%d)*%s^%d' % (random.randint(-5, 5), var, k) for k in range(deg + 1)])

def rlinfac():
    return '(%d*x+%d)' % (random.choice([1, 1, 2, 3]), random.randint(-4, 4))

ATOM_F = ['sin(%s)', 'cos(%s)', 'e^(%s)', 'ln(%s)', '(%s)^2', '(%s)^3', 'sqrt(%s)', '1/(%s)', 'arctan(%s)', 'x*%s']
def rfun(d=2):
    if d == 0:
        return random.choice(['x', '(2*x+1)', '(x^2+1)', '3*x'])
    return random.choice(ATOM_F) % rfun(d - 1)

class TO(Exception):
    pass
def h(s, f):
    raise TO()
signal.signal(signal.SIGALRM, h)

stats = {}
CUR = [None]
def check(kind, fnc):
    signal.alarm(15)
    try:
        r = fnc()
    except TO:
        r = 'timeout'
        print('TIMEOUT', kind, CUR[0])
    except CASError as ex:
        r = 'caserr'
    except Exception as ex:
        r = 'PYEXC ' + type(ex).__name__ + ' ' + str(ex)
    finally:
        signal.alarm(0)
    st = stats.setdefault(kind, {})
    key = r if r in (True, False, 'skip', 'timeout', 'caserr') else 'pyexc'
    st[key] = st.get(key, 0) + 1
    return r

for k in range(N):
    # integration: d/dx(integral(f)) == f
    f = E(rfun(random.randint(1, 2)))
    CUR[0] = f
    def t_int():
        F = CA.integ(f, 'x')
        if F is None:
            return 'skip'
        ok = numeq(CA.diff(F, 'x'), f)
        if not ok:
            print('INT FAIL', f, '->', F)
        return ok
    check('integral', t_int)
    # factor
    p = E('*'.join([rlinfac() for _ in range(random.randint(1, 3))]) + '*(' + rpoly(random.randint(0, 2)) + ')')
    def t_fac():
        fa = PO.factor_expr(p)
        ok = expand(simp(fa)) == expand(p) if not isnode(fa, 'hold') else expand(simp(fa[1])) == expand(p)
        if not ok:
            print('FACTOR FAIL', p, '->', fa)
        return ok
    check('factor', t_fac)
    # solve polynomial
    q = E(rpoly(random.randint(1, 4)))
    def t_solve():
        rs = SO.solve_eq(q, 'x', True)
        if rs is None or rs == 'all':
            return 'skip'
        for r in rs:
            v = nval(subs(q, 'x', r))
            sc = 1 + sum([abs(nval(c)) for c in (coeffs(q, 'x') or [1])])
            if abs(v) > 1e-6 * sc * (1 + abs(nval(r))) ** 4:
                print('SOLVE FAIL', q, r, v)
                return False
        d = degree(q, 'x')
        if d and len(rs) > d:
            print('TOO MANY', q, rs)
            return False
        return True
    check('csolve', t_solve)
    # matrix inverse
    n = random.randint(2, 3)
    A = MA.mk([[random.randint(-4, 4) for _ in range(n)] for _ in range(n)])
    def t_inv():
        if MA.det(A) == 0:
            return 'skip'
        I = MA.m_mul(A, MA.m_inv(A))
        ok = I == MA.ident(n)
        if not ok:
            print('INV FAIL', A)
        return ok
    check('inverse', t_inv)
    # eigenvalues: det(A - l I) == 0
    def t_eig():
        ev = MA.eigvl(A)
        for l in ev[1:]:
            d = MA.det(MA.m_add(A, MA.m_scale(MA.ident(n), l), -1))
            if abs(nval(d)) > 1e-6 * (1 + abs(nval(l))) ** n * 10:
                print('EIG FAIL', A, l, d)
                return False
        return True
    check('eigvl', t_eig)
    # limits vs numeric
    g = E(rfun(1) + '/' + rfun(1))
    def t_lim():
        L = CA.limit(g, 'x', 1)
        if isnode(L, 'limit') or L == 'undef' or has(L, 'inf'):
            return 'skip'
        try:
            v1 = nval(g, {'x': 1 + 1e-7})
            v2 = nval(g, {'x': 1 - 1e-7})
        except Exception:
            return 'skip'
        ok = abs(nval(L) - v1) < 1e-4 * (1 + abs(v1)) and abs(nval(L) - v2) < 1e-4 * (1 + abs(v2))
        if not ok:
            print('LIM FAIL', g, L, v1, v2)
        return ok
    check('limit', t_lim)
    # deSolve: linear 2nd order constant coefficients
    a, b, c = random.randint(1, 3), random.randint(-4, 4), random.randint(-4, 4)
    rhs = random.choice(['0', 'x', 'e^x', 'sin(x)', '1'])
    def t_de():
        ode = subs(subs(E('%d*yy2+%d*yy1+%d*y-(%s)' % (a, b, c, rhs)), 'yy2', 'Y2_'), 'yy1', 'Y1_')
        r = SO.desolve(ode, 'x', 'y', [])
        if r is None:
            return 'skip'
        Y = r[2]
        env = {'c1': 0.7, 'c2': -1.3}
        resid = add(mul(a, CA.diff(Y, 'x', 2)), mul(b, CA.diff(Y, 'x')), mul(c, Y), neg(E(rhs)))
        for p in (0.3, 1.1):
            env['x'] = p
            v = nval(resid, env)
            if abs(v) > 1e-6:
                print('DE FAIL', a, b, c, rhs, '->', Y, v)
                return False
        return True
    check('desolve2', t_de)
    # taylor vs derivative definition
    t = E(rfun(1))
    def t_tay():
        T = CA.taylor(t, 'x', 3, 1)
        if isnode(T, 'taylor'):
            return 'skip'
        T2 = CA.taylor_d(t, 'x', 3, 1)
        ok = numeq(T, T2)
        if not ok:
            print('TAYLOR FAIL', t, T, T2)
        return ok
    check('taylor', t_tay)

for k in stats:
    print(k, stats[k])
