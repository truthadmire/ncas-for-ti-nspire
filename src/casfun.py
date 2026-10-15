# casfun.py - built-in TI functions taking evaluated arguments
from cascore import *
import caspoly as PO
import cascalc as CA
import casmat as MA
from casout import fmt, OPT

SET = {'angle': 'rad', 'mode': 'auto', 'cplx': 'real'}

def ismat(e):
    return isnode(e, 'mat')

def islist(e):
    return isnode(e, 'list')

def lmap(f, a):
    # distribute over lists / matrices
    if islist(a):
        return ('list',) + tuple(lmap(f, v) for v in a[1:])
    if ismat(a):
        return ('mat',) + tuple(lmap(f, r) for r in a[1:])
    return f(a)

def lmap2(f, a, b):
    if islist(a) and islist(b):
        if len(a) != len(b):
            err("Dimension error")
        return ('list',) + tuple(lmap2(f, a[i], b[i]) for i in range(1, len(a)))
    if islist(a):
        return ('list',) + tuple(lmap2(f, v, b) for v in a[1:])
    if islist(b):
        return ('list',) + tuple(lmap2(f, a, v) for v in b[1:])
    if ismat(a) and ismat(b):
        return ('mat',) + tuple(lmap2(f, a[i], b[i]) for i in range(1, len(a)))
    if ismat(a):
        return ('mat',) + tuple(lmap2(f, r, b) for r in a[1:])
    if ismat(b):
        return ('mat',) + tuple(lmap2(f, a, r) for r in b[1:])
    return f(a, b)

# ------------------------------------------------ arithmetic with lists/mats
def vadd(a, b):
    if ismat(a) and ismat(b):
        return MA.m_add(a, b)
    if islist(a) or islist(b) or ismat(a) or ismat(b):
        return lmap2(add, a, b)
    if isrel(a) or isrel(b):
        return relop(add, a, b)
    if isstr(a) or isstr(b):
        err("Data type error")
    return add(a, b)

def vsub(a, b):
    return vadd(a, vneg(b))

def vneg(a):
    return lmap(neg, a) if not isrel(a) else (a[0], neg(a[1]), neg(a[2]))

def vmul(a, b):
    if ismat(a) and ismat(b):
        return MA.m_mul(a, b)
    if ismat(a) and islist(b) or islist(a) and ismat(b):
        return MA.m_mul(MA.tomat(a), MA.tomat(b) if ismat(b) else MA.transpose(b))
    if islist(a) or islist(b) or ismat(a) or ismat(b):
        return lmap2(mul, a, b)
    if isrel(a) or isrel(b):
        return relop(mul, a, b)
    return mul(a, b)

def vdiv(a, b):
    if ismat(b):
        if ismat(a):
            return MA.m_mul(a, MA.m_inv(b))
        return vmul(a, MA.m_inv(b))
    if islist(a) or islist(b) or ismat(a):
        return lmap2(div, a, b)
    if isrel(a) or isrel(b):
        return relop(div, a, b)
    if b == 0 and isconst(a):
        return 'undef'
    return div(a, b)

def vpow(a, b):
    if ismat(a):
        if type(b) is int:
            return MA.m_pow(a, b)
        if b == 'T_t':
            return MA.transpose(a)
        err("Domain error")
    if islist(a) or islist(b):
        return lmap2(pw, a, b)
    if isrel(a):
        return (a[0], pw(a[1], b), pw(a[2], b))
    return pw(a, b)

def relop(f, a, b):
    if isrel(a) and isrel(b):
        return (a[0], f(a[1], b[1]), f(a[2], b[2]))
    if isrel(a):
        return (a[0], f(a[1], b), f(a[2], b))
    return (b[0], f(a, b[1]), f(a, b[2]))

def isrel(e):
    return type(e) is tuple and e[0] in ('=', '<', '>', '<=', '>=', '/=')

def isstr(e):
    return isnode(e, 'str')

def dotop(op, a, b):
    if op == '.*':
        return lmap2(mul, a, b)
    if op == './':
        return lmap2(div, a, b)
    return lmap2(pw, a, b)

# ------------------------------------------------ relations / logic
def rel(op, a, b):
    if islist(a) or islist(b):
        return lmap2(lambda x, y: rel(op, x, y), a, b)
    if isstr(a) and isstr(b):
        r = cmpstr(op, a[1], b[1])
        if r is not None:
            return 'true' if r else 'false'
    d = PO.autocancel(sub(a, b)) if not (isstr(a) or isstr(b)) else None
    if d is not None and isconst(d) and d != 'undef':
        try:
            v = nval(d)
        except Exception:
            v = None
        if v is not None:
            if type(v) is complex:
                if op == '=':
                    return 'true' if abs(v) < 1e-13 else 'false'
                if op == '/=':
                    return 'false' if abs(v) < 1e-13 else 'true'
                err("Non-real comparison")
            if d == 0 or abs(v) < 1e-300:
                v = 0.0
            r = {'=': v == 0, '/=': v != 0, '<': v < 0, '>': v > 0, '<=': v <= 0, '>=': v >= 0}[op]
            return 'true' if r else 'false'
    if op == '=' and d == 0:
        return 'true'
    return (op, a, b)

def cmpstr(op, a, b):
    if op == '=':
        return a == b
    if op == '/=':
        return a != b
    return None

def tobool(v):
    if v == 'true':
        return True
    if v == 'false':
        return False
    return None

def land(a, b):
    ta = tobool(a)
    tb = tobool(b)
    if ta is False or tb is False:
        return 'false'
    if ta is True:
        return b
    if tb is True:
        return a
    return flat('and', a, b)

def lor(a, b):
    ta = tobool(a)
    tb = tobool(b)
    if ta is True or tb is True:
        return 'true'
    if ta is False:
        return b
    if tb is False:
        return a
    return flat('or', a, b)

def flat(op, a, b):
    xs = []
    for v in (a, b):
        if isnode(v, op):
            xs.extend(v[1:])
        else:
            xs.append(v)
    return (op,) + tuple(xs)

def lnot(a):
    t = tobool(a)
    if t is not None:
        return 'false' if t else 'true'
    if isint(a):
        return ~a
    neg_ = {'<': '>=', '>': '<=', '<=': '>', '>=': '<', '=': '/=', '/=': '='}
    if isrel(a):
        return (neg_[a[0]], a[1], a[2])
    return ('not', a)

def lxor(a, b):
    ta = tobool(a)
    tb = tobool(b)
    if ta is not None and tb is not None:
        return 'true' if ta != tb else 'false'
    if isint(a) and isint(b):
        return a ^ b
    return ('xor', a, b)

# ------------------------------------------------ number theory
def need_int(n):
    if isfl(n) and finite(n) and n == math.floor(n):
        return int(n)
    if not isint(n):
        err("Argument must be an integer")
    return n

def gcd_(a, b):
    if israt(a) and israt(b):
        an, ad = nd(a)
        bn, bd = nd(b)
        return Q(igcd(an, bn), ilcm(ad, bd))
    if isfl(a) or isfl(b):
        return float(igcd(int(a), int(b)))
    return PO.poly_gcd_expr(a, b)

def lcm_(a, b):
    if israt(a) and israt(b):
        an, ad = nd(a)
        bn, bd = nd(b)
        return Q(ilcm(an, bn), igcd(ad, bd))
    g = gcd_(a, b)
    return PO.autocancel(div(mul(a, b), g))

def mod_(a, b):
    if isnode(a, '^') and isint(a[1]) and isint(a[2]) and a[2] > 0 and isint(b) and b != 0:
        # a huge power that was left unevaluated: modular exponentiation
        r = PO.powmod(a[1], a[2], abs(b))
        return r - abs(b) if b < 0 and r else r
    if isnum(a) and isnum(b):
        if b == 0:
            return a
        return nsub(a, nmul(b, nfloor(ndiv(a, b))))
    return ('mod', a, b)

def remain_(a, b):
    if isnum(a) and isnum(b):
        if b == 0:
            return a
        q = ndiv(a, b)
        t = nfloor(q) if nsign(q) >= 0 else -nfloor(nneg(q))
        return nsub(a, nmul(b, t))
    return ('remain', a, b)

def intdiv_(a, b):
    q = ndiv(a, b)
    if nsign(q) >= 0:
        return nfloor(q)
    return -nfloor(nneg(q))

def bigcomb(n, k):
    # would nCr(n,k) / nPr(n,k) be a huge exact number?
    if not (isint(n) and isint(k)) or k <= 0:
        return False
    m = min(k, abs(n - k)) if n >= k else k
    return m * ibits(n) > MAXBITS

def ncr_(n, k):
    if isint(n) and isint(k):
        if k < 0 or (n >= 0 and k > n):
            return 0
        if bigcomb(n, k):
            return ('ncr', n, k)
        return CA.binom(n, k) if n >= 0 else gen_ncr(n, k)
    if isint(k) and k >= 0:
        return gen_ncr(n, k)
    if isfl(n) or isfl(k):
        return CA_gamma_ratio(n, k)
    return ('ncr', n, k)

def gen_ncr(n, k):
    r = 1
    for i in range(k):
        r = mul(r, sub(n, i))
    f = 1
    for i in range(2, k + 1):
        f *= i
    return mul(r, Q(1, f))

def npr_(n, k):
    if isint(n) and isint(k) and k * ibits(n) > MAXBITS:
        return ('npr', n, k)
    if isint(k) and k >= 0:
        r = 1
        for i in range(k):
            r = mul(r, sub(n, i))
        return r
    return ('npr', n, k)

def CA_gamma_ratio(n, k):
    n = tofl(n)
    k = tofl(k)
    return gamma(n + 1) / (gamma(k + 1) * gamma(n - k + 1))

def isprime_(n):
    n = need_int(n)
    if abs(n) >> 1024:
        err('Number too large for isPrime')
    return 'true' if PO.isprime(abs(n)) else 'false'

def round_(x, d=0):
    if isconst(x) and not isnum(x):
        x = evalf(x)
    if isnum(x):
        if israt(x) and d == 0:
            return nfloor(nadd(x, HALF)) if nsign(x) >= 0 else -nfloor(nadd(nneg(x), HALF))
        v = tofl(x)
        if not finite(v):
            return x
        p = 10.0 ** d
        r = math.floor(abs(v) * p + 0.5) / p
        return r if v >= 0 else -r
    return ('round', x, d)

def ipart_(x):
    if isconst(x) and not isnum(x):
        x = evalf(x)
    if isnum(x):
        if type(x) is float:
            return float(int(x))
        return nfloor(x) if nsign(x) >= 0 else -nfloor(nneg(x))
    return ('ipart', x)

def fpart_(x):
    i = ipart_(x)
    if isnode(i, 'ipart'):
        return ('fpart', x)
    return sub(x, i)

# ------------------------------------------------ misc
def approx_(e):
    return evalf(e)

def exact_(e, tol=None):
    if tol is not None:
        tol = tofl(tol)
    return exactify(e, tol)

def approxfraction(e, tol=None):
    t = tofl(tol) if tol is not None else 5e-14
    return lmap(lambda v: float2rat(tofl(evalf(v)), t) if isconst(v) else exactify(v, t), e)

def left_(e, n=None):
    if isrel(e):
        return e[1]
    if islist(e):
        return ('list',) + e[1:1 + n]
    if isstr(e):
        return ('str', e[1][:n])
    err("Argument error")

def right_(e, n=None):
    if isrel(e):
        return e[2]
    if islist(e):
        return ('list',) + (e[len(e) - n:] if n else ())
    if isstr(e):
        return ('str', e[1][len(e[1]) - n:] if n else '')
    err("Argument error")

def mid_(e, start, n=None):
    if isstr(e):
        s = e[1][start - 1:]
        return ('str', s if n is None else s[:n])
    xs = list(e[1:])[start - 1:]
    return ('list',) + tuple(xs if n is None else xs[:n])

def dim_(e):
    if islist(e):
        return len(e) - 1
    if ismat(e):
        r, c = MA.dims(e)
        return ('list', r, c)
    if isstr(e):
        return len(e[1])
    err("Argument error")

def max_(a, b=None):
    if b is None:
        xs = list(a[1:]) if islist(a) else [a]
        return MA.maxexpr(xs)
    return lmap2(lambda x, y: x if cmpv(x, y) >= 0 else y, a, b)

def min_(a, b=None):
    if b is None:
        xs = list(a[1:]) if islist(a) else [a]
        best = None
        bv = None
        for x in xs:
            v = nval(x)
            if best is None or v < bv:
                best = x
                bv = v
        return best
    return lmap2(lambda x, y: x if cmpv(x, y) <= 0 else y, a, b)

def cmpv(x, y):
    if isconst(x) and isconst(y):
        d = nval(sub(x, y))
        d = d.real if type(d) is complex else d
        return 1 if d > 0 else (-1 if d < 0 else 0)
    err("Cannot compare")

def when_(c, a, b=None, u=None):
    t = tobool(c)
    if t is True:
        return a
    if t is False:
        return b if b is not None else 'undef'
    if b is None:
        return ('when', c, a)
    if u is None:
        return ('when', c, a, b)
    return u

def piecewise_(*a):
    a = list(a)
    if len(a) % 2 == 1:
        r = a[-1]
        a = a[:-1]
    else:
        r = 'undef'
    for i in range(len(a) - 2, -1, -2):
        r = when_(a[i + 1], a[i], r)
    return r

def string_(e):
    if isstr(e):
        return e
    return ('str', fmt(e))

def char_(n):
    return ('str', chr(need_int(n)))

def ord_(s):
    return ord(s[1][0])

def instring_(s, t, start=1):
    i = s[1].find(t[1], start - 1)
    return i + 1

def polyeval(L, x):
    r = 0
    for c in L[1:]:
        r = add(mul(r, x), c)
    return expand(r)

def randpoly(v, n):
    import random
    return add_list([mul(random.randint(-9, 9), pw(v, k)) for k in range(n + 1)])

def randmat(r, c):
    import random
    return MA.mk([[random.randint(-9, 9) for _ in range(c)] for _ in range(r)])

def newmat(r, c):
    return MA.mk([[0] * c for _ in range(r)])

def newlist(n):
    return ('list',) + (0,) * n

def rand_(n=None):
    import random
    if n is None:
        return random.random()
    return ('list',) + tuple(random.random() for _ in range(n))

def randint_(a, b, n=None):
    import random
    if n is None:
        return random.randint(a, b)
    return ('list',) + tuple(random.randint(a, b) for _ in range(n))

def count_(*args):
    n = 0
    for a in args:
        n += (len(a) - 1) if islist(a) else 1
    return n

# ------------------------------------------------ distributions
def erf(x):
    # Abramowitz-Stegun 7.1.26 refined by series for small x
    if abs(x) < 2.5:
        s = 0.0
        t = x
        k = 0
        while True:
            term = t / (2 * k + 1)
            s += term
            k += 1
            t = -t * x * x / k
            if abs(term) < 1e-17:
                break
        return 2 / math.sqrt(math.pi) * s
    # continued fraction for erfc
    z = abs(x)
    t = 0.0
    for k in range(60, 0, -1):
        t = (k / 2.0) / (z + t)
    erfc = math.exp(-z * z) / math.sqrt(math.pi) / (z + t)
    return (1 - erfc) if x > 0 else (erfc - 1)

def numarg(v):
    # numeric (float) value of an argument or an error
    if v == 'inf':
        return float('inf')
    if v == ('*', -1, 'inf'):
        return float('-inf')
    if isconst(v):
        x = cv(v) if not isnum(v) else tofl(v)
        if x is not None and type(x) is not complex:
            return x
    err('Numeric argument required')

def normcdf(lo, hi, mu=0.0, sig=1.0):
    mu = numarg(mu)
    sig = numarg(sig)
    def F(v):
        if v == 'inf':
            return 1.0
        if v == ('*', -1, 'inf'):
            return 0.0
        z = (numarg(v) - mu) / sig
        return 0.5 * (1 + erf(z / math.sqrt(2)))
    return F(hi) - F(lo)

def normpdf(x, mu=0.0, sig=1.0):
    x = numarg(x)
    s = numarg(sig)
    return math.exp(-0.5 * ((x - numarg(mu)) / s) ** 2) / (s * math.sqrt(2 * math.pi))

def invnorm(p, mu=0.0, sig=1.0):
    p = numarg(p)
    mu = numarg(mu)
    sig = numarg(sig)
    if not 0 < p < 1:
        err('Area must be between 0 and 1')
    lo, hi = -40.0, 40.0
    for _ in range(200):
        m = 0.5 * (lo + hi)
        if 0.5 * (1 + erf(m / math.sqrt(2))) < p:
            lo = m
        else:
            hi = m
    return mu + sig * 0.5 * (lo + hi)

def binompdf(n, p, x=None):
    if x is None:
        return ('list',) + tuple(binompdf(n, p, k) for k in range(n + 1))
    if israt(p):
        return mul(CA.binom(n, x), pw(p, x), pw(sub(1, p), n - x))
    p = tofl(p)
    return CA.binom(n, x) * p ** x * (1 - p) ** (n - x)

def binomcdf(n, p, a, b=None):
    if b is None:
        a, b = 0, a
    return add_list([binompdf(n, p, k) for k in range(int(a), int(b) + 1)])

def poisspdf(lam, x):
    return evalf(mul(pw(lam, x), pw('e', neg(lam)), Q(1, fact_int(x))))

def poisscdf(lam, a, b=None):
    if b is None:
        a, b = 0, a
    return add_list([poisspdf(lam, k) for k in range(int(a), int(b) + 1)])

def geompdf(p, x):
    return mul(p, pw(sub(1, p), x - 1))

def geomcdf(p, a, b=None):
    if b is None:
        a, b = 1, a
    return add_list([geompdf(p, k) for k in range(int(a), int(b) + 1)])

def fact_int(n):
    r = 1
    for k in range(2, n + 1):
        r *= k
    return r

# ------------------------------------------------ angle helpers
def toang(x):
    a = SET['angle']
    if a == 'deg':
        return mul(x, div('pi', 180))
    if a == 'grad':
        return mul(x, div('pi', 200))
    return x

def fromang(x):
    a = SET['angle']
    if a == 'deg':
        return expand(mul(x, div(180, 'pi')))
    if a == 'grad':
        return expand(mul(x, div(200, 'pi')))
    return x

TRIG = ('sin', 'cos', 'tan', 'sec', 'csc', 'cot')
ITRIG = ('arcsin', 'arccos', 'arctan', 'arcsec', 'arccsc', 'arccot')

def mathfn(name):
    def f(*a):
        if name in TRIG and SET['angle'] != 'rad':
            return lmap(lambda u: fn(name, toang(u)), a[0])
        if name in ITRIG and SET['angle'] != 'rad':
            return lmap(lambda u: fromang(fn(name, u)), a[0])
        if len(a) == 1:
            return lmap(lambda u: fn(name, u), a[0])
        return fn(name, *a)
    return f

def angle_fn(z):
    return lmap(lambda u: fromang(fn('angle', u)), z)

# ------------------------------------------------ table
F = {}
for _n in ('sin', 'cos', 'tan', 'sec', 'csc', 'cot', 'arcsin', 'arccos',
           'arctan', 'arcsec', 'arccsc', 'arccot', 'sinh', 'cosh', 'tanh',
           'sech', 'csch', 'coth', 'arcsinh', 'arccosh', 'arctanh',
           'arcsech', 'arccsch', 'arccoth', 'ln', 'exp', 'abs', 'sign',
           'floor', 'ceiling', 'real', 'imag', 'conj', 'fact'):
    F[_n] = mathfn(_n)
ALIAS = {'asin': 'arcsin', 'acos': 'arccos', 'atan': 'arctan', 'asinh': 'arcsinh',
         'acosh': 'arccosh', 'atanh': 'arctanh', 'ceil': 'ceiling',
         'factorial': 'fact', 'derivative': 'd', 'integral': 'integral',
         'int_': 'integral', 'sumseq': 'sumseq', 'prodseq': 'prodseq',
         'lim': 'limit', 'nderiv': 'nderivative', 'polycoef': 'polycoeffs',
         'stddevsamp': 'stddev', 'varsamp': 'variance', 'cumsum': 'cumulativesum',
         'nsolve': 'nsolve', 'arg': 'angle', 'inv': 'inverse', 'mat2list': 'matlist',
         'list2mat': 'listmat', 'explist': 'explist', 'tran': 'transpose',
         'log10': 'log10', 'sqr': 'sqrt'}

F['sqrt'] = lambda u: lmap(sqrt, u)
F['root'] = lambda u, n=2: lmap(lambda v: fn('root', v, n), u)
F['log'] = lambda u, b=None: lmap(lambda v: fn('ln', v) if b is None else fn('log', v, b), u)
F['atan2'] = lambda y, x: lmap2(lambda b, a: fromang(fn('angle', add(a, mul('i', b)))), y, x)
F['log10'] = lambda u: lmap(lambda v: fn('log', v, 10), u)
F['angle'] = angle_fn
F['round'] = lambda x, d=0: lmap(lambda v: round_(v, d), x)
F['ipart'] = lambda x: lmap(ipart_, x)
F['int'] = lambda x: lmap(lambda v: fn('floor', v), x)
F['fpart'] = lambda x: lmap(fpart_, x)
F['gcd'] = lambda a, b: lmap2(gcd_, a, b)
F['lcm'] = lambda a, b: lmap2(lcm_, a, b)
F['mod'] = lambda a, b: lmap2(mod_, a, b)
F['remain'] = lambda a, b: lmap2(remain_, a, b)
F['intdiv'] = lambda a, b: lmap2(intdiv_, a, b)
F['ncr'] = lambda a, b: lmap2(ncr_, a, b)
F['npr'] = lambda a, b: lmap2(npr_, a, b)
F['isprime'] = isprime_
F['approx'] = approx_
F['exact'] = exact_
F['approxrational'] = approxfraction
F['getnum'] = lambda e: lmap(PO.getnum, e)
F['getdenom'] = lambda e: lmap(PO.getden, e)
F['polyeval'] = polyeval
F['polygcd'] = lambda a, b: PO.poly_gcd_expr(a, b)
F['randpoly'] = randpoly
F['texpand'] = lambda e: lmap(lambda v: CA.texpand(v), e)
F['tcollect'] = lambda e: lmap(lambda v: CA.tcollect(v), e)
F['left'] = left_
F['right'] = right_
F['mid'] = mid_
F['dim'] = dim_
F['max'] = max_
F['min'] = min_
F['when'] = when_
F['piecewise'] = piecewise_
F['string'] = string_
F['char'] = char_
F['ord'] = ord_
F['instring'] = instring_
F['det'] = MA.det
F['identity'] = MA.ident
F['transpose'] = MA.transpose
F['rref'] = lambda A, tol=None: MA.rref(A, True)
F['ref'] = lambda A, tol=None: ref_(A)
F['inverse'] = MA.m_inv
F['rowdim'] = lambda A: MA.dims(A)[0]
F['coldim'] = lambda A: MA.dims(A)[1]
F['rownorm'] = MA.rownorm
F['colnorm'] = MA.colnorm
F['norm'] = MA.norm
F['trace'] = MA.trace
F['diag'] = MA.diag
F['augment'] = MA.augment
F['colaugment'] = MA.colaugment
F['submat'] = MA.submat
F['rowswap'] = MA.rowswap
F['rowadd'] = MA.rowadd
F['mrow'] = MA.mrow
F['mrowadd'] = MA.mrowadd
F['crossp'] = MA.crossp
F['dotp'] = MA.dotp
F['unitv'] = MA.unitv
F['eigvl'] = MA.eigvl
F['eigvc'] = MA.eigvc
F['lu'] = lambda A, tol=None: ('list',) + MA.lu(A)
F['qr'] = lambda A, tol=None: ('list',) + MA.qr(A)
F['newmat'] = newmat
F['newlist'] = newlist
F['randmat'] = randmat
F['matlist'] = MA.matlist
F['listmat'] = MA.listmat
F['simult'] = MA.simult
F['cumulativesum'] = MA.cumsum
F['sum'] = lambda L, a=1, b=None: MA.lsum(L, a, b) if islist(L) else colwise(L, MA.lsum)
F['product'] = lambda L, a=1, b=None: MA.lprod(L, a, b) if islist(L) else colwise(L, MA.lprod)
F['mean'] = lambda L, f=None: MA.mean(L, f) if islist(L) else colwise(L, MA.mean)
F['median'] = MA.median
F['stddev'] = lambda L: MA.stddev(L)
F['stddevpop'] = lambda L: MA.stddev(L, True)
F['variance'] = lambda L: MA.variance(L)
F['varpop'] = lambda L: MA.variance(L, True)
F['sorta'] = MA.sorta
F['sortd'] = MA.sortd
F['deltalist'] = MA.deltalist
F['count'] = count_
F['rand'] = rand_
F['randint'] = randint_
F['normcdf'] = normcdf
F['normpdf'] = normpdf
F['invnorm'] = invnorm
F['binompdf'] = binompdf
F['binomcdf'] = binomcdf
F['poisspdf'] = poisspdf
F['poisscdf'] = poisscdf
F['geompdf'] = geompdf
F['geomcdf'] = geomcdf
F['getmode'] = lambda *a: ('str', 'angle=' + SET['angle'] + ' mode=' + SET['mode'] + ' cplx=' + SET['cplx'])

def colwise(M, f):
    cols = MA.rows(MA.transpose(M))
    return MA.mk([[f(('list',) + tuple(c)) for c in cols]])

def ref_(A):
    return MA.rref(A, False)

# ------------------------------------------------ conversions (►)
def conv(e, name, args):
    if name == 'decimal':
        return evalf(e)
    if name == 'approxfraction':
        return approxfraction(e, args[0] if args else None)
    if name in ('dms', 'dd', 'rad', 'grad', 'deg'):
        return angconv(e, name)
    if name == 'polar':
        if islist(e) or ismat(e):
            return MA.polar_vec(e)
        r = PO.autocancel(fn('abs', e))
        th = fn('angle', e)
        return ('str', '(' + fmt(r) + '∠' + fmt(fromang(th)) + ')')
    if name == 'rect':
        if islist(e) or ismat(e):
            return e
        r, i = reim(e)
        return add(r, mul('i', i))
    if name == 'cylind':
        return MA.cylind(e)
    if name == 'sphere':
        return MA.sphere(e)
    if name in ('base2', 'base10', 'base16'):
        return baseconv(e, name)
    if name == 'exp':
        return toexp(e)
    if name == 'ln':
        return toln(e)
    if name == 'logbase':
        return tologbase(e, args[0])
    if name == 'sin':
        return CA.pyth_to(e, 'sin')
    if name == 'cos':
        return CA.pyth_to(e, 'cos')
    err("Unknown conversion " + name)

def angconv(e, name):
    if name == 'dms':
        v = tofl(evalf(e))
        if SET['angle'] == 'rad':
            v = v * 180 / math.pi
        elif SET['angle'] == 'grad':
            v = v * 0.9
        sg = '-' if v < 0 else ''
        v = abs(v)
        d = int(v)
        m = int((v - d) * 60)
        s = ((v - d) * 60 - m) * 60
        if s > 59.9999995:
            s = 0.0
            m += 1
        if m == 60:
            m = 0
            d += 1
        ss = ('%.4f' % s).rstrip('0').rstrip('.')
        return ('str', sg + str(d) + '°' + str(m) + "'" + ss + '"')
    if name == 'dd':
        if SET['angle'] == 'rad':
            return evalf(mul(e, div(180, 'pi')))
        return evalf(e)
    if name == 'rad':
        if SET['angle'] == 'deg':
            return mul(e, div('pi', 180))
        if SET['angle'] == 'grad':
            return mul(e, div('pi', 200))
        return e
    if name == 'grad':
        if SET['angle'] == 'deg':
            return mul(e, Q(10, 9))
        if SET['angle'] == 'rad':
            return mul(e, div(200, 'pi'))
        return e
    if SET['angle'] == 'rad':
        return mul(e, div(180, 'pi'))
    return e

def baseconv(e, name):
    n = need_int(e)
    if name == 'base10':
        return n
    if name == 'base2':
        s = bin(n) if n >= 0 else '-' + bin(-n)
        return ('str', s.replace('0b', '0b'))
    s = hex(n) if n >= 0 else '-' + hex(-n)
    return ('str', s.replace('0x', '0h').upper().replace('0H', '0h'))

def toexp(e):
    if type(e) is not tuple or e[0] == 'Q':
        return e
    args = [toexp(a) for a in e[1:]]
    h = e[0]
    if len(args) == 1:
        u = args[0]
        if h == 'sinh':
            return mul(HALF, sub(pw('e', u), pw('e', neg(u))))
        if h == 'cosh':
            return mul(HALF, add(pw('e', u), pw('e', neg(u))))
        if h == 'tanh':
            return div(sub(pw('e', u), pw('e', neg(u))), add(pw('e', u), pw('e', neg(u))))
        if h == 'sin':
            iu = mul('i', u)
            return div(sub(pw('e', iu), pw('e', neg(iu))), mul(2, 'i'))
        if h == 'cos':
            iu = mul('i', u)
            return mul(HALF, add(pw('e', iu), pw('e', neg(iu))))
        if h == 'arcsinh':
            return fn('ln', add(u, sqrt(add(pw(u, 2), 1))))
        if h == 'arccosh':
            return fn('ln', add(u, sqrt(sub(pw(u, 2), 1))))
        if h == 'arctanh':
            return mul(HALF, fn('ln', div(add(1, u), sub(1, u))))
    return simp((h,) + tuple(args))

def toln(e):
    if type(e) is not tuple or e[0] == 'Q':
        return e
    args = [toln(a) for a in e[1:]]
    if e[0] == 'log':
        b = args[1] if len(args) > 1 else 10
        return div(fn('ln', args[0]), fn('ln', b))
    return simp((e[0],) + tuple(args))

def tologbase(e, b):
    e = toln(e)
    def walk(t):
        if type(t) is not tuple or t[0] == 'Q':
            return t
        if t[0] == 'ln':
            return div(('log', walk(t[1]), b), ('log', 'e', b))
        return (t[0],) + tuple(walk(a) for a in t[1:])
    return ('hold', walk(e))
