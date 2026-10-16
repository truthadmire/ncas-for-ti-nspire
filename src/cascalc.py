# cascalc.py - calculus: derivatives, integrals, series, limits, sums,
# trig expansion/collection
from cascore import *
from caspoly import (autocancel, partfrac, factor_expr, comdenom, kernels,
                     u_from_expr, aberth, hasdenom, to_ratform, p_vars)

TV = 'T_'
LNT = 'LNT_'
VV = 'V_'

class NoSeries(Exception):
    pass

# ===================================================== derivative
def dfun(name, u):
    if name == 'sin':
        return fn('cos', u)
    if name == 'cos':
        return neg(fn('sin', u))
    if name == 'tan':
        return pw(fn('cos', u), -2)
    if name == 'arcsin':
        return pw(sub(1, pw(u, 2)), Q(-1, 2))
    if name == 'arccos':
        return neg(pw(sub(1, pw(u, 2)), Q(-1, 2)))
    if name == 'arctan':
        return pw(add(pw(u, 2), 1), -1)
    if name == 'sinh':
        return fn('cosh', u)
    if name == 'cosh':
        return fn('sinh', u)
    if name == 'tanh':
        return pw(fn('cosh', u), -2)
    if name == 'arcsinh':
        return pw(add(pw(u, 2), 1), Q(-1, 2))
    if name == 'arccosh':
        return pw(sub(pw(u, 2), 1), Q(-1, 2))
    if name == 'arctanh':
        return pw(sub(1, pw(u, 2)), -1)
    if name == 'ln':
        return pw(u, -1)
    if name == 'abs':
        return fn('sign', u)
    if name in ('sign', 'floor', 'ceiling', 'round', 'ipart', 'int'):
        return 0
    return None

def diff(e, x, n=1):
    if n < 0:
        r = e
        for _ in range(-n):
            r = integrate(r, x)
        return r
    for _ in range(n):
        e = diff1(e, x)
    return e

def diff1(e, x):
    if isnode(e, 'list') or isnode(e, 'mat'):
        return mapexpr(lambda a: diff1(a, x), e)
    if isnode(e, '=') or isnode(e, '<') or isnode(e, '>'):
        return (e[0], diff1(e[1], x), diff1(e[2], x))
    if freeof(e, x):
        return 0
    if e == x:
        return 1
    h = e[0]
    if h == '+':
        return add_list([diff1(a, x) for a in e[1:]])
    if h == '*':
        fs = e[1:]
        terms = []
        for i in range(len(fs)):
            d = diff1(fs[i], x)
            if d != 0:
                terms.append(mul_list([d] + [fs[j] for j in range(len(fs)) if j != i]))
        return add_list(terms)
    if h == '^':
        b = e[1]
        p = e[2]
        if freeof(p, x):
            return mul(p, pw(b, sub(p, 1)), diff1(b, x))
        if freeof(b, x):
            return mul(e, fn('ln', b), diff1(p, x))
        return mul(e, add(mul(diff1(p, x), fn('ln', b)), div(mul(p, diff1(b, x)), b)))
    if h == 'log':
        b = e[2] if len(e) > 2 else 10
        return diff1(div(fn('ln', e[1]), fn('ln', b)), x)
    if h == 'when':
        return fn('when', e[1], diff1(e[2], x), diff1(e[3], x)) if len(e) > 3 else fn('when', e[1], diff1(e[2], x))
    if h == 'integral' and len(e) == 3 and e[2] == x:
        return e[1]
    if h == 'integral' and len(e) == 5 and freeof(e[1], x) is False and e[2] != x:
        # Leibniz rule for variable limits
        f, v, a, b = e[1], e[2], e[3], e[4]
        return sub(mul(subs(f, v, b), diff1(b, x)), mul(subs(f, v, a), diff1(a, x)))
    if len(e) == 2:
        d = dfun(h, e[1])
        if d is not None:
            return mul(d, diff1(e[1], x))
    return ('d', e, x)

# ===================================================== helpers
def linear(u, x):
    cs = coeffs(u, x)
    if cs is None or len(cs) != 2 or cs[1] == 0:
        return None
    return cs[1], cs[0]

def nice(e):
    # choose the shortest of a few equivalent forms
    from casout import fmt
    try:
        e = autocancel(e)
    except Exception:
        return e
    if not hasdenom(e) or hasfloat(e) or isnode(e, 'list') or isnode(e, 'mat'):
        return e
    best = e
    bl = len(fmt(e))
    if bl > 400:
        return e
    for f in (comdenom, factor_expr):
        try:
            c = f(e)
            l = len(fmt(c))
            if l < bl:
                best = c
                bl = l
        except Exception:
            pass
    return best

# ===================================================== integration
BUDGET = [0]

def integrate(f, x, depth=0):
    BUDGET[0] = 0
    r = integ(f, x, depth)
    if r is None and hasdenom(f):
        g = autocancel(f)
        if g != f:
            BUDGET[0] = 0
            r = integ(g, x, depth)
    if r is None:
        return ('integral', f, x)
    return r

def integ(f, x, depth=0):
    if depth > 7:
        return None
    if depth == 0:
        BUDGET[0] = 0
    BUDGET[0] += 1
    if BUDGET[0] > 400:
        return None
    if freeof(f, x):
        return mul(f, x)
    if f == x:
        return mul(HALF, pw(x, 2))
    h = f[0] if type(f) is tuple else None
    if h == '+':
        out = []
        for t in f[1:]:
            r = integ(t, x, depth + 1)
            if r is None:
                return integ_whole(f, x, depth)
            out.append(r)
        return add_list(out)
    if h == '*':
        c = [g for g in f[1:] if freeof(g, x)]
        v = [g for g in f[1:] if not freeof(g, x)]
        if c:
            r = integ(mul_list(v), x, depth)
            if r is None:
                return None
            return mul(mul_list(c), r)
    if h == 'when':
        a = integ(f[2], x, depth + 1)
        b = integ(f[3], x, depth + 1) if len(f) > 3 else None
        if a is None or (len(f) > 3 and b is None):
            return None
        return ('when', f[1], a, b) if b is not None else ('when', f[1], a)
    r = itable(f, x)
    if r is not None:
        return r
    return integ_whole(f, x, depth)

def integ_whole(f, x, depth):
    # polynomial
    d = degree(f, x)
    if d is not None:
        g = expand(f)
        if g != f:
            return integ(g, x, depth + 1)
    # rational function
    r = irational(f, x)
    if r is not None:
        return r
    # tan powers, sec and csc powers
    r = itanpow(f, x, depth)
    if r is not None:
        return r
    r = isecpow(f, x, depth)
    if r is not None:
        return r
    # substitution
    r = isubst(f, x, depth)
    if r is not None:
        return r
    # trigonometric substitution for sqrt(a^2-x^2), sqrt(x^2+a^2)
    r = itrigsub(f, x, depth)
    if r is not None:
        return r
    # products of trig functions
    if hastrig(f):
        g = tcollect(f)
        if g != f:
            r = integ(g, x, depth + 1)
            if r is not None:
                return r
    # integration by parts
    r = iparts(f, x, depth)
    if r is not None:
        return r
    g = expand(f)
    if g != f:
        r = integ(g, x, depth + 1)
        if r is not None:
            return r
    if depth < 4:
        # last resorts: tan/cot as sin/cos, sinh/cosh as exponentials,
        # tan(x/2) substitution for rational functions of sin and cos
        g = untan(f)
        if g != f:
            r = integ(g, x, depth + 2)
            if r is not None:
                return r
        g = unhyp(f)
        if g != f:
            r = integ(expand(g), x, depth + 2)
            if r is not None:
                return r
        r = iweier(f, x, depth)
        if r is not None:
            return r
        r = iquartic(f, x, depth)
        if r is not None:
            return r
    return None

def qfrac(A, B, p, q, x):
    # integral of (A*x+B)/(x^2+p*x+q) when 4q-p^2 > 0
    w = sqrt(sub(mul(4, q), pw(p, 2)))
    P = add(pw(x, 2), mul(p, x), q)
    return add(mul(A, HALF, fn('ln', P)),
               mul(sub(B, mul(A, p, HALF)), div(2, w), fn("arctan", expand(div(add(mul(2, x), p), w)))))

def iquartic(f, x, depth):
    # N/(a*x^4+b*x^2+c) with no real roots: split the denominator into
    # two real quadratics x^2 +- s*x + q, then partial fractions
    n, d = numer_denom(f)
    cd = coeffs(d, x)
    cn = coeffs(n, x)
    if cd is None or cn is None or len(cd) != 5 or len(cn) > 4:
        return None
    if cd[1] != 0 or cd[3] != 0 or not all([isconst(q) for q in cd + cn]):
        return None
    a, b, c = cd[4], cd[2], cd[0]
    try:
        if fv_(c) / fv_(a) <= 0:
            return None
        q = sqrt(div(c, a))
        s2 = sub(mul(2, q), div(b, a))
        if fv_(s2) <= 0:
            return None
    except Exception:
        return None
    sr = sqrt(s2)
    cn = [div(v, a) for v in cn] + [0] * (4 - len(cn))
    n0, n1, n2, n3 = cn
    BE = div(n0, q)
    EmB = div(sub(n1, mul(q, n3)), sr)
    B = mul(HALF, sub(BE, EmB))
    E = mul(HALF, add(BE, EmB))
    CmA = div(sub(n2, BE), sr)
    A = mul(HALF, sub(n3, CmA))
    C = mul(HALF, add(n3, CmA))
    P1 = add(pw(x, 2), mul(sr, x), q)
    P2 = add(sub(pw(x, 2), mul(sr, x)), q)
    R = add(qfrac(A, B, sr, q, x), qfrac(C, E, neg(sr), q, x))
    return R if antiok(R, f, x) else None

def unhyp(e):
    if type(e) is not tuple or e[0] == 'Q':
        return e
    a = [unhyp(b) for b in e[1:]]
    if len(a) == 1 and e[0] in ('sinh', 'cosh', 'tanh'):
        p = pw('e', a[0])
        m = pw('e', neg(a[0]))
        if e[0] == 'sinh':
            return mul(HALF, sub(p, m))
        if e[0] == 'cosh':
            return mul(HALF, add(p, m))
        return div(sub(p, m), add(p, m))
    return simp((e[0],) + tuple(a))

def trigargs_x(f, x, out):
    if type(f) is not tuple or f[0] == 'Q':
        return
    if f[0] in ('sin', 'cos', 'tan') and not freeof(f[1], x):
        if f[1] not in out:
            out.append(f[1])
        return
    for b in f[1:]:
        trigargs_x(b, x, out)

def iweier(f, x, depth):
    # t = tan(u/2) for a rational function of sin(u), cos(u), u = a*x+b
    us = []
    trigargs_x(f, x, us)
    if len(us) != 1:
        return None
    u = us[0]
    lu = linear(u, x)
    if lu is None:
        return None
    t = 'W%d_' % depth
    q = add(1, pw(t, 2))
    def rep(e):
        if type(e) is not tuple or e[0] == 'Q':
            return e
        if len(e) == 2 and e[1] == u:
            if e[0] == 'sin':
                return div(mul(2, t), q)
            if e[0] == 'cos':
                return div(sub(1, pw(t, 2)), q)
            if e[0] == 'tan':
                return div(mul(2, t), sub(1, pw(t, 2)))
        return simp((e[0],) + tuple(rep(b) for b in e[1:]))
    g = rep(f)
    if not freeof(g, x):
        return None
    g = autocancel(div(mul(2, g), mul(lu[0], q)))
    R = integ(g, t, depth + 2)
    if R is None:
        return None
    R = subs(R, t, fn('tan', mul(HALF, u)))
    return R if antiok(R, f, x) else None

def itable(f, x):
    h = head(f)
    if h == '^':
        b = f[1]
        p = f[2]
        if freeof(p, x):
            lb = linear(b, x)
            if lb is not None:
                a = lb[0]
                if p == -1:
                    return div(fn('ln', fn('abs', b)), a)
                return div(pw(b, add(p, 1)), mul(a, add(p, 1)))
            if (p == HALF or p == Q(-1, 2)) and degree(b, x) == 2:
                return iquadrad(b, p, x)
            if len(b) == 2 and head(b) in ('sin', 'cos', 'tan', 'sinh', 'cosh') and type(b) is tuple:
                lu = linear(b[1], x)
                if lu is not None:
                    a = lu[0]
                    u = b[1]
                    n = b[0]
                    if n == 'cos' and p == -2:
                        return div(fn('tan', u), a)
                    if n == 'sin' and p == -2:
                        return div(neg(pw(fn('tan', u), -1)), a)
                    if n == 'cos' and p == -1:
                        return div(fn('ln', fn('abs', add(pw(fn('cos', u), -1), fn('tan', u)))), a)
                    if n == 'sin' and p == -1:
                        return div(fn('ln', fn('abs', fn('tan', mul(HALF, u)))), a)
                    if n == 'tan' and p == -1:
                        return div(fn('ln', fn('abs', fn('sin', u))), a)
                    if n == 'cosh' and p == -2:
                        return div(fn('tanh', u), a)
        if freeof(b, x):
            lu = linear(p, x)
            if lu is not None:
                a = lu[0]
                if b == 'e':
                    return div(f, a)
                return div(f, mul(a, fn('ln', b)))
        return None
    if type(f) is tuple and len(f) == 2:
        u = f[1]
        lu = linear(u, x)
        if lu is None:
            return None
        a = lu[0]
        r = None
        if h == 'sin':
            r = neg(fn('cos', u))
        elif h == 'cos':
            r = fn('sin', u)
        elif h == 'tan':
            r = neg(fn('ln', fn('abs', fn('cos', u))))
        elif h == 'sinh':
            r = fn('cosh', u)
        elif h == 'cosh':
            r = fn('sinh', u)
        elif h == 'tanh':
            r = fn('ln', fn('cosh', u))
        elif h == 'ln':
            r = sub(mul(u, fn('ln', u)), u)
        elif h == 'arctan':
            r = sub(mul(u, fn('arctan', u)), mul(HALF, fn('ln', add(pw(u, 2), 1))))
        elif h == 'arcsin':
            r = add(mul(u, fn('arcsin', u)), sqrt(sub(1, pw(u, 2))))
        elif h == 'arccos':
            r = sub(mul(u, fn('arccos', u)), sqrt(sub(1, pw(u, 2))))
        elif h == 'abs':
            r = mul(HALF, u, fn('abs', u))
        elif h == 'sign':
            r = fn('abs', u)
        elif h == 'arcsinh':
            r = sub(mul(u, fn('arcsinh', u)), sqrt(add(pw(u, 2), 1)))
        elif h == 'arctanh':
            r = add(mul(u, fn('arctanh', u)), mul(HALF, fn('ln', sub(1, pw(u, 2)))))
        if r is not None:
            return div(r, a)
    if h == 'log' and len(f) == 3:
        lu = linear(f[1], x)
        if lu is not None:
            u = f[1]
            return div(sub(mul(u, fn('ln', u)), u), mul(lu[0], fn('ln', f[2])))
    return None

def iquadrad(b, p, x):
    cs = coeffs(b, x)
    C, B, A = cs
    if not isconst(A):
        return None
    av = nval(A)
    if type(av) is complex:
        return None
    D = sub(mul(B, B), mul(4, A, C))
    if p == Q(-1, 2):
        if av < 0:
            return mul(pw(neg(A), Q(-1, 2)), fn('arcsin', div(neg(add(mul(2, A, x), B)), sqrt(D))))
        sA = sqrt(A)
        return mul(pw(A, Q(-1, 2)), fn('ln', fn('abs', add(sqrt(b), mul(sA, x), div(B, mul(2, sA))))))
    J = iquadrad(b, Q(-1, 2), x)
    if J is None:
        return None
    return add(div(mul(add(mul(2, A, x), B), sqrt(b)), mul(4, A)),
               mul(div(sub(mul(4, A, C), mul(B, B)), mul(8, A)), J))

def irational(f, x):
    ks = []
    kernels(f, ks)
    for k in ks:
        if k != x:
            return None
    if not hasdenom(f):
        return None
    pf = partfrac(f, x)
    if pf is None:
        return None
    terms = pf[1:] if isnode(pf, '+') else (pf,)
    out = []
    for t in terms:
        if not hasdenom(t):
            r = integ(t, x, 5)
            if r is None:
                return None
            out.append(r)
            continue
        fs = t[1:] if isnode(t, '*') else (t,)
        num = []
        den = None
        k = 1
        for g in fs:
            if isnode(g, '^') and type(g[2]) is int and g[2] < 0:
                den = g[1]
                k = -g[2]
            else:
                num.append(g)
        if den is None:
            return None
        N = mul_list(num)
        dg = degree(den, x)
        if dg == 1:
            r = integ(t, x, 5)
            if r is None:
                return None
            out.append(r)
        elif dg == 2:
            r = iquadfrac(N, den, k, x)
            if r is None:
                return None
            out.append(r)
        else:
            # an irreducible higher factor: substitution or quartic split
            r = isubst(t, x, 3) if k == 1 else None
            if r is None and k == 1:
                r = iquartic(t, x, 3)
            if r is None:
                return None
            out.append(r)
    return add_list(out)

def iquadfrac(N, Qd, k, x):
    cs = coeffs(N, x)
    if cs is None or len(cs) > 2:
        return None
    n0 = cs[0]
    n1 = cs[1] if len(cs) > 1 else 0
    C, B, A = coeffs(Qd, x)
    res = []
    if n1 != 0:
        if k == 1:
            D = sub(mul(B, B), mul(4, A, C))
            dv = nval(D) if isconst(D) else 0
            arg = Qd if (type(dv) is not complex and dv < 0 and nval(A) > 0) else fn('abs', Qd)
            res.append(mul(div(n1, mul(2, A)), fn('ln', arg)))
        else:
            res.append(mul(div(n1, mul(2, A)), div(-1, mul(k - 1, pw(Qd, k - 1)))))
    c0 = sub(n0, div(mul(n1, B), mul(2, A)))
    if c0 != 0:
        J = jquad(A, B, C, Qd, k, x)
        if J is None:
            return None
        res.append(mul(c0, J))
    return add_list(res)

def jquad(A, B, C, Qd, k, x):
    D = expand(sub(mul(B, B), mul(4, A, C)))
    if k == 1:
        if not isconst(D):
            return None
        dv = nval(D)
        if type(dv) is complex:
            return None
        L = add(mul(2, A, x), B)
        if dv < 0:
            s = sqrt(neg(D))
            return mul(div(2, s), fn('arctan', div(L, s)))
        if dv > 0:
            s = sqrt(D)
            return mul(pw(s, -1), fn('ln', fn('abs', div(sub(L, s), add(L, s)))))
        return div(-2, L)
    Jp = jquad(A, B, C, Qd, k - 1, x)
    if Jp is None:
        return None
    Dl = neg(D)
    L = add(mul(2, A, x), B)
    return add(mul(div(L, mul(k - 1, Dl)), pw(Qd, 1 - k)),
               mul(div(mul(2 * k - 3, 2, A), mul(k - 1, Dl)), Jp))

def itanpow(f, x, depth):
    if isnode(f, '^') and isnode(f[1], 'tan') and type(f[2]) is int and f[2] >= 2:
        u = f[1][1]
        lu = linear(u, x)
        if lu is None:
            return None
        n = f[2]
        a = lu[0]
        t = f[1]
        first = div(pw(t, n - 1), mul(n - 1, a))
        rest = integ(pw(t, n - 2), x, depth + 1)
        if rest is None:
            return None
        return sub(first, rest)
    return None

def isecpow(f, x, depth):
    # sec^n and csc^n (n >= 3) by the reduction formula
    #   int sec^n = sec^(n-2)*tan/(n-1) + (n-2)/(n-1)*int sec^(n-2)
    if (isnode(f, '^') and head(f[1]) in ('cos', 'sin') and len(f[1]) == 2
            and type(f[2]) is int and f[2] <= -3):
        u = f[1][1]
        lu = linear(u, x)
        if lu is None:
            return None
        n = -f[2]
        a = lu[0]
        if f[1][0] == 'cos':
            first = mul(pw(fn('cos', u), 2 - n), fn('tan', u))
        else:
            first = neg(mul(pw(fn('sin', u), 2 - n), pw(fn('tan', u), -1)))
        rest = integ(pw(f[1], 2 - n), x, depth + 1)
        if rest is None:
            return None
        return add(div(first, mul(n - 1, a)), mul(Q(n - 2, n - 1), rest))
    return None

def cands(f, x, out):
    if type(f) is not tuple or freeof(f, x) or f[0] == 'Q':
        return
    h = f[0]
    if h == '+' or h == '*':
        for a in f[1:]:
            cands(a, x, out)
        return
    if h == '^':
        if f[1] != x and not freeof(f[1], x) and f[1] not in out:
            out.append(f[1])
        if isq(f[2]) and not freeof(f[1], x):
            rad = pw(f[1], Q(1, f[2][2]))
            if rad not in out:
                out.append(rad)
        if not freeof(f[2], x) and f[2] not in out:
            out.append(f[2])
            if f not in out:
                out.append(f)
        if f[1] == x and f not in out and isnum(f[2]) and f[2] != -1:
            out.append(f)
            if isint(f[2]) and f[2] % 2 == 0 and f[2] > 2 and pw(x, 2) not in out:
                out.append(pw(x, 2))
        cands(f[1], x, out)
        cands(f[2], x, out)
        return
    if f not in out:
        out.append(f)
    for a in f[1:]:
        if a != x and not freeof(a, x) and a not in out:
            out.append(a)
        cands(a, x, out)

def subst_kernel(q, u, V, x):
    # replace u by V in q, also powers related to u
    if isnode(u, '^') and u[1] == x and isnum(u[2]):
        q2 = subs(q, x, pw(V, pw(u[2], -1)))
        return subs(q2, fn('abs', V), V)
    if isnode(u, 'ln'):
        lu = linear(u[1], x)
        if lu is not None:
            a, b = lu
            return subs(q, x, div(sub(pw('e', V), b), a))
    if isnode(u, '^') and isq(u[2]) and not freeof(u[1], x):
        cs_ = coeffs(u[1], x)
        q2 = subs(q, u, V)
        if cs_ is not None and not freeof(q2, x):
            nz = [k for k in range(1, len(cs_)) if cs_[k] != 0]
            if len(nz) == 1:
                k = nz[0]
                xk = div(sub(pw(V, pw(u[2], -1)), cs_[0]), cs_[k])
                q3 = subs(q2, x, pw(xk, Q(1, k)))
                if freeof(q3, x):
                    return q3
        return q2
    if isnode(u, '^') and u[1] == 'e':
        lu = linear(u[2], x)
        if lu is not None and lu[1] == 0:
            a = lu[0]
            return subst_exp(q, a, V, x)
    return subs(q, u, V)

def subst_exp(q, a, V, x):
    if type(q) is not tuple or q[0] == 'Q':
        return q
    if q[0] == '^' and q[1] == 'e':
        lm = linear(q[2], x)
        if lm is not None:
            return mul(pw(V, div(lm[0], a)), pw('e', lm[1]))
    return simp((q[0],) + tuple(subst_exp(b, a, V, x) for b in q[1:]))

def isubst(f, x, depth):
    if depth > 5:
        return None
    VV = 'V%d_' % depth
    while has(f, VV) or VV == x:
        VV = VV + '_'
    cs = []
    cands(f, x, cs)
    fracf = hasfracpow(f, x)
    big = len(okey(f)) > 500
    for u in cs[:14]:
        if u == x:
            continue
        du = diff(u, x)
        if du == 0:
            continue
        q = div(f, du)
        if not big:
            q = autocancel(q)
        q2 = subst_kernel(q, u, VV, x)
        if freeof(q2, x) and (fracf or not hasfracpow(q2, VV)) and len(okey(q2)) < 800:
            r = integ(q2, VV, depth + 2)
            if r is not None:
                r = subs(r, VV, u)
                if antiok(r, f, x):
                    return r
    # linear substitution inside radicals
    for u in cs:
        if isnode(u, '+'):
            lu = linear(u, x)
            if lu is not None:
                a, b = lu
                g = expand(div(subs(f, x, div(sub(VV, b), a)), a))
                r = integ(g, VV, depth + 2)
                if r is not None:
                    return subs(r, VV, u)
    return None

TPTS = (-2.3, -1.7, -0.8, -0.35, 0.3, 0.75, 1.6, 2.4)

def antiok(F, f, x):
    # does F' = f where both are real (central differences at a few
    # points)? False only on a clear mismatch
    if len(symbols(f)) > 1 or len(symbols(F)) > 1:
        return True
    def v(e, t):
        try:
            z = nval(e, {x: t})
        except Exception:
            return None
        if type(z) is complex:
            if abs(z.imag) > 1e-9 * (1 + abs(z.real)):
                return None
            z = z.real
        if z != z or abs(z) > 1e12:
            return None
        return z
    for t in TPTS:
        y = v(f, t)
        if y is None:
            continue
        h = 1e-5 * (1 + abs(t))
        a = v(F, t + h)
        b = v(F, t - h)
        if a is None or b is None:
            continue
        if abs((a - b) / (2 * h) - y) > 1e-4 * (1 + abs(y)):
            return False
    return True

def itrigsub(f, x, depth):
    # (c0 + c2*x^2)^(k/2): x = r*sin(T) when c2 < 0, x = r*tan(T) when
    # c2 > 0 (c0 > 0); after integrating in T, back to x
    rad = []
    radicals(f, x, rad)
    if not rad:
        return None
    B = rad[0]
    cs = coeffs(B, x)
    if cs is None or len(cs) != 3 or cs[1] != 0 or not isconst(cs[0]) or not isconst(cs[2]):
        return None
    if any([q != B for q in rad]):
        return None
    c0, c2 = cs[0], cs[2]
    T = 'T%d_' % depth
    if fv_(c0) < 0 and fv_(c2) > 0:
        # x = r/cos(T): sqrt(B) = sqrt(c2)*r*tan(T)
        r = sqrt(div(neg(c0), c2))
        xs = div(r, fn('cos', T))
        rt = mul(sqrt(c2), r, fn('tan', T))
        dx = mul(r, fn('tan', T), pw(fn('cos', T), -1))
        g = mul(subrad(f, B, rt, x, xs), dx)
        R = None
        for h in (pyth_to(g, 'cos'), pyth_to(g, 'sin'), pyth(g)):
            R = integ(h, T, depth + 2)
            if R is not None:
                break
        if R is None:
            return None
        R = backtrig(texpand(R), T, div(pw(B, HALF), mul(sqrt(c2), x)), div(r, x))
        R = subs(R, T, fn('arccos', div(r, x)))
        if not freeof(R, T) or not antiok(R, f, x):
            return None
        return R
    if fv_(c0) <= 0:
        return None
    sc0 = sqrt(c0)
    if fv_(c2) < 0:
        r = sqrt(div(c0, neg(c2)))
        xs = mul(r, fn('sin', T))
        rt = mul(sc0, fn('cos', T))
        dx = mul(r, fn('cos', T))
    else:
        r = sqrt(div(c0, c2))
        xs = mul(r, fn('tan', T))
        rt = div(sc0, fn('cos', T))
        dx = div(r, pw(fn('cos', T), 2))
    g = mul(subrad(f, B, rt, x, xs), dx)
    R = None
    for h in (pyth(g), pyth_to(g, 'cos'), pyth_to(g, 'sin')):
        R = integ(h, T, depth + 2)
        if R is not None:
            break
    if R is None:
        return None
    R = texpand(R)
    sq = pw(B, HALF)
    if fv_(c2) < 0:
        sinT = div(x, r)
        cosT = div(sq, sc0)
        Tx = fn('arcsin', div(x, r))
    else:
        cosT = div(sc0, sq)
        sinT = mul(div(x, r), cosT)
        Tx = fn('arctan', div(x, r))
    R = backtrig(R, T, sinT, cosT)
    R = subs(R, T, Tx)
    if not freeof(R, T) or not antiok(R, f, x):
        return None
    return R

def radicals(f, x, out):
    if type(f) is not tuple or f[0] == 'Q':
        return
    if f[0] == '^' and isq(f[2]) and f[2][2] == 2 and not freeof(f[1], x):
        out.append(f[1])
    for a in f[1:]:
        radicals(a, x, out)

def subrad(f, B, rt, x, xs):
    # f with B^(k/2) -> rt^k and x -> xs
    if f == x:
        return xs
    if type(f) is not tuple or f[0] == 'Q':
        return f
    if f[0] == '^' and f[1] == B and isq(f[2]) and f[2][2] == 2:
        return pw(rt, f[2][1])
    return simp((f[0],) + tuple(subrad(a, B, rt, x, xs) for a in f[1:]))

def backtrig(R, T, sinT, cosT):
    if type(R) is not tuple or R[0] == 'Q':
        return R
    if len(R) == 2 and R[1] == T:
        if R[0] == 'sin':
            return sinT
        if R[0] == 'cos':
            return cosT
        if R[0] == 'tan':
            return div(sinT, cosT)
    return simp((R[0],) + tuple(backtrig(a, T, sinT, cosT) for a in R[1:]))

def hasfracpow(e, x):
    # does e contain a non-integer power of an expression in x
    if type(e) is not tuple or e[0] == 'Q':
        return False
    if e[0] == '^' and not isint(e[2]) and not freeof(e[1], x):
        return True
    for a in e[1:]:
        if hasfracpow(a, x):
            return True
    return False

def hastrig(f):
    if type(f) is not tuple or f[0] == 'Q':
        return False
    if f[0] in ('sin', 'cos'):
        return True
    for a in f[1:]:
        if hastrig(a):
            return True
    return False

def ispoly(e, x):
    return degree(e, x) is not None

def iparts(f, x, depth):
    if depth > 5:
        return None
    fs = f[1:] if isnode(f, '*') else (f,)
    P = []
    G = []
    for g in fs:
        if ispoly(g, x):
            P.append(g)
        else:
            G.append(g)
    if len(G) == 2:
        # e^(ax) * sin/cos(bx)
        ex = None
        tr = None
        for g in G:
            if isnode(g, '^') and g[1] == 'e' and linear(g[2], x):
                ex = g
            elif head(g) in ('sin', 'cos') and linear(g[1], x):
                tr = g
        if ex is not None and tr is not None and not P:
            a = linear(ex[2], x)[0]
            b = linear(tr[1], x)[0]
            u = tr[1]
            den = add(mul(a, a), mul(b, b))
            if tr[0] == 'sin':
                r = mul(ex, sub(mul(a, fn('sin', u)), mul(b, fn('cos', u))))
            else:
                r = mul(ex, add(mul(a, fn('cos', u)), mul(b, fn('sin', u))))
            return div(r, den)
        return None
    if len(G) != 1:
        return None
    g = G[0]
    Pp = mul_list(P)
    gh = head(g)
    tabular = False
    if isnode(g, '^') and g[1] == 'e' and linear(g[2], x):
        tabular = True
    elif isnode(g, '^') and isnum(g[1]) and linear(g[2], x):
        tabular = True
    elif gh in ('sin', 'cos', 'sinh', 'cosh') and linear(g[1], x):
        tabular = True
    if tabular and P:
        res = []
        sg = 1
        Gi = g
        Pd = Pp
        for _ in range(40):
            Gi = integ(Gi, x, depth + 1)
            if Gi is None:
                return None
            res.append(mul(sg, Pd, Gi))
            Pd = diff(Pd, x)
            sg = -sg
            if Pd == 0:
                return add_list(res)
        return None
    if gh in ('ln', 'arctan', 'arcsin', 'arccos', 'log', 'arcsinh', 'arctanh') or (isnode(g, '^') and head(g[1]) in ('ln', 'arcsin', 'arctan') and isint(g[2]) and g[2] > 0):
        V = integ(Pp, x, depth + 1)
        if V is None:
            return None
        rest = integ(autocancel(expand(mul(V, diff(g, x)))), x, depth + 1)
        if rest is None:
            return None
        return sub(mul(g, V), rest)
    return None

# ===================================================== definite / numeric
def defint(f, x, a, b):
    if a == b:
        return 0
    if isconst(a) and isconst(b):
        try:
            if numpt(a) > numpt(b):
                r = defint(f, x, b, a)
                return neg(r) if not isnode(r, 'integral') else ('integral', f, x, a, b)
        except Exception:
            pass
    if haswhen(f, x) and isconst(a) and isconst(b):
        ps = whensplit(f, x, a, b)
        if ps is not None:
            total = 0
            for p, q, g in ps:
                if g == 'undef' or has(g, 'undef'):
                    return 'undef'
                total = add(total, defint(g, x, p, q))
            return total
    BUDGET[0] = 0
    F = integ(f, x)
    if F is None and hasdenom(f):
        BUDGET[0] = 0
        F = integ(autocancel(f), x)
    sing = singular_points(f, x, a, b) or []
    if F is not None and not hasfloat(f):
        # jumps of the antiderivative too (tan(x/2) from the tan(x/2)
        # substitution jumps at x = pi)
        for p in singular_points(F, x, a, b) or []:
            if all([abs(fv_(p) - fv_(q)) > 1e-9 for q in sing]):
                sing.append(p)
        sing.sort(key=fv_)
        if isconst(a) and isconst(b) and fv_(a) > fv_(b):
            sing.reverse()
        pts = [a] + sing + [b]
        total = 0
        infs = []
        for i in range(len(pts) - 1):
            lo = pts[i]
            hi = pts[i + 1]
            vb = limit(F, x, hi, -1 if not isinf(hi) else 0)
            va = limit(F, x, lo, 1 if not isinf(lo) else 0)
            if isnode(vb, 'limit') or isnode(va, 'limit'):
                total = None
                break
            d = sub(vb, va)
            if va == 'undef' or vb == 'undef':
                # the antiderivative has no limit there (it oscillates)
                return 'undef'
            if has(va, 'inf') or has(vb, 'inf'):
                # F is unbounded at an end: the piece diverges
                if d not in ('inf', ('*', -1, 'inf')):
                    return 'undef'
            if d == 'undef' or has(d, 'undef'):
                total = None
                break
            if has(d, 'inf'):
                infs.append(d)
            total = add(total, d)
        if total is not None and infs:
            # a non-integrable singularity: the integral diverges
            if all([q == infs[0] for q in infs]) and infs[0] in ('inf', ('*', -1, 'inf')):
                return infs[0]
            return 'undef'
        if total is not None and total != 'undef':
            return total
    if isconst(a) and isconst(b) and freeofall(f, [s for s in symbols(f) if s != x]):
        try:
            return nint_split(f, x, a, b)
        except Exception:
            pass
    return ('integral', f, x, a, b)

# ===================================================== piecewise (when)
def haswhen(f, x):
    if type(f) is not tuple or f[0] == 'Q':
        return False
    if f[0] in ('when', 'abs') and not freeof(f[1], x):
        return True
    for a in f[1:]:
        if haswhen(a, x):
            return True
    return False

def gensol(r):
    # the integer parameter (n1, n2, ...) of a general solution, or None
    ns = [w for w in symbols(r) if w[0] == 'n' and w[1:].isdigit()]
    if len(ns) == 1 and isconst(subs(r, ns[0], 0)):
        return ns[0]
    return None

def firstwhen_(f, x):
    if type(f) is not tuple or f[0] == 'Q':
        return False
    if f[0] == 'when' and not freeof(f[1], x):
        return True
    return any([firstwhen_(a, x) for a in f[1:]])

def whenpts(f, x, out):
    # real zeros of the conditions of when() nodes in f
    if type(f) is not tuple or f[0] == 'Q':
        return
    if f[0] == 'abs' and not freeof(f[1], x):
        from cassolve import solve_eq, isrealc
        rs = solve_eq(f[1], x, False)
        if rs and rs != 'all':
            for r in rs:
                if (isrealc(r) or gensol(r)) and r not in out:
                    out.append(r)
    if f[0] == 'when' and not freeof(f[1], x):
        from cassolve import solve_eq, isrealc
        cs = [f[1]]
        while cs:
            c = cs.pop()
            if head(c) in ('and', 'or', 'not'):
                cs.extend(c[1:])
            elif head(c) in ('<', '>', '<=', '>=', '=', '/='):
                rs = solve_eq(sub(c[1], c[2]), x, False)
                if rs and rs != 'all':
                    for r in rs:
                        if (isrealc(r) or gensol(r)) and r not in out:
                            out.append(r)
    for a in f[1:]:
        whenpts(a, x, out)

def pickwhen(f, x, t):
    # f with every when() on x replaced by its branch at x=t (a float)
    if type(f) is not tuple or f[0] == 'Q':
        return f
    if f[0] == 'when' and not freeof(f[1], x):
        try:
            c = nbool(f[1], {x: t})
        except Exception:
            return 'undef'
        if c:
            return pickwhen(f[2], x, t)
        return pickwhen(f[3], x, t) if len(f) > 3 else 'undef'
    if f[0] == 'abs' and not freeof(f[1], x):
        u = pickwhen(f[1], x, t)
        try:
            return u if fv_(subs(u, x, t)) >= 0 else neg(u)
        except Exception:
            return f
    return simp((f[0],) + tuple(pickwhen(a, x, t) for a in f[1:]))

def numpt(v):
    if v == 'inf':
        return 1e300
    if v == ('*', -1, 'inf'):
        return -1e300
    return fv_(v)

def fv_(v):
    z = nval(v)
    return z.real if type(z) is complex else z

def whensplit(f, x, a, b):
    # [(lo, hi, piece)] for a when()-expression on [a, b]
    pts = []
    whenpts(f, x, pts)
    lo = numpt(a)
    hi = numpt(b)
    if lo > hi:
        return None
    ex = []
    for p in pts:
        n = gensol(p)
        if n is None:
            ex.append(p)
        elif hi - lo < 1e4:
            for k in range(-300, 301):
                q = subs(p, n, k)
                if lo < fv_(q) < hi and q not in ex:
                    ex.append(q)
    ins = [p for p in ex if lo < fv_(p) < hi]
    ins.sort(key=fv_)
    ends = [a] + ins + [b]
    out = []
    for i in range(len(ends) - 1):
        p, q = ends[i], ends[i + 1]
        pv, qv = numpt(p), numpt(q)
        if pv < -1e299:
            t = qv - 1.0
        elif qv > 1e299:
            t = pv + 1.0
        else:
            t = 0.5 * (pv + qv)
        out.append((p, q, pickwhen(f, x, t)))
    return out

def whenlimit(f, x, a, dirn):
    pts = []
    whenpts(f, x, pts)
    if isinf(a):
        t = 1e6 if a == 'inf' else -1e6
        return limit(pickwhen(f, x, t), x, a, dirn)
    av = fv_(a)
    d = 1e-6
    for p in pts:
        q = abs(fv_(p) - av)
        if q > 1e-12:
            d = min(d, q / 2)
    r = limit(pickwhen(f, x, av + d), x, a, 1) if dirn >= 0 else None
    l = limit(pickwhen(f, x, av - d), x, a, -1) if dirn <= 0 else None
    if dirn == 1:
        return r
    if dirn == -1:
        return l
    if r == l:
        return r
    try:
        if isconst(r) and isconst(l) and abs(nval(r) - nval(l)) < 1e-12:
            return r
    except Exception:
        pass
    return 'undef'

def isinf(v):
    return v == 'inf' or v == ('*', -1, 'inf')

def singular_points(f, x, a, b):
    # real zeros of denominators strictly between a and b
    if not (isconst(a) and isconst(b)):
        return []
    try:
        av = nreal(a) if not isinf(a) else (-1e300 if a != 'inf' else 1e300)
        bv = nreal(b) if not isinf(b) else (1e300 if b == 'inf' else -1e300)
    except Exception:
        return []
    lo, hi = min(av, bv), max(av, bv)
    pts = []
    dens = []
    collect_dens(f, x, dens)
    for d in dens:
        u = u_from_expr(d, x)
        if u is not None and len(u) < 2:
            continue
        if u is None:
            if hi - lo < 1e6:
                for r in scanzeros(d, x, lo, hi):
                    if all([abs(fv_(q) - r) > 1e-9 for q in pts]):
                        pts.append(snapzero(d, x, r))
            continue
        for r in aberth(u):
            if abs(r.imag) < 1e-9 and lo < r.real < hi:
                rr = exactify(r.real) if abs(r.real - round(r.real)) < 1e-12 else r.real
                pts.append(rr)
    pts.sort(key=fv_)
    if av > bv:
        pts.reverse()
    return pts

def collect_dens(f, x, out):
    if type(f) is not tuple or f[0] == 'Q':
        return
    if f[0] == '^' and isnum(f[2]) and nsign(f[2]) < 0 and not freeof(f[1], x):
        out.append(f[1])
    if f[0] == 'tan' and not freeof(f[1], x):
        out.append(fn('cos', f[1]))
    if f[0] in ('ln', 'log') and not freeof(f[1], x):
        out.append(f[1])
    for a in f[1:]:
        collect_dens(a, x, out)

def scanzeros(d, x, lo, hi, n=400):
    # zeros of d in (lo, hi) found by sampling and bisection; poles of d
    # (sign changes through infinity) are skipped
    out = []
    def g(t):
        try:
            v = nval(d, {x: t})
            return v.real if type(v) is complex else v
        except Exception:
            return None
    h = (hi - lo) / n
    t0 = lo + h * 1e-3
    v0 = g(t0)
    for k in range(1, n + 1):
        t1 = lo + h * k - (h * 1e-3 if k == n else 0)
        v1 = g(t1)
        if v0 is not None and v1 is not None and v0 * v1 <= 0:
            a, b, fa = t0, t1, v0
            for it in range(60):
                m = 0.5 * (a + b)
                fm = g(m)
                if fm is None:
                    break
                if (fm <= 0) == (fa <= 0):
                    a, fa = m, fm
                else:
                    b = m
            m = 0.5 * (a + b)
            fm = g(m)
            if fm is not None and abs(fm) < 1e-6 and lo < m < hi:
                out.append(m)
        t0, v0 = t1, v1
    return out

def snapzero(d, x, r):
    # exact form of a numeric zero when an obvious one fits (k*pi/n, n/m)
    for c in (exactify_guess(r / math.pi), exactify_guess(r)):
        if type(c) is float:
            continue
        v = mul(c, 'pi') if c is not exactify_guess(r) else c
        try:
            if abs(fv_(subs(d, x, v))) < 1e-9:
                return v
        except Exception:
            pass
    return r

NERR = [0.0]
NBUD = [0]      # Gauss-Kronrod steps left for one numeric integral

def nint(f, x, a, b, tol=1e-10):
    NERR[0] = 0.0
    NBUD[0] = 1500
    r = None
    if (isinf(a) or isinf(b)) and not (isinf(a) and isinf(b)):
        r = nint_osc(f, x, a, b, tol)
    if r is None:
        r = nint0(f, x, a, b, tol)
        if NERR[0] > 1e-7 * max(1.0, abs(r)) and not isinf(a) and not isinf(b):
            # endpoint singularity: x = a + (b-a)*(3u^2-2u^3) smooths it
            NERR[0] = 0.0
            a0 = nreal(a)
            w = nreal(b) - a0
            g = lambda u: _nv(f, x, a0 + w * u)
            for k in range(3):
                g = smooth(g)
                NERR[0] = 0.0
                r = w * _gk_adapt(g, 0.0, 1.0, tol, 0)
                if NERR[0] <= 1e-7 * max(1.0, abs(r)):
                    break
        if NERR[0] > 1e-7 * max(1.0, abs(r)) and (isinf(a) != isinf(b)):
            # slowly decaying tail: smooth the mapped integrand at t = 1
            if isinf(a):
                f, a, b = subs(f, x, neg(x)), neg(b), 'inf'
            a0 = nreal(a)
            g = lambda t: _nv(f, x, a0 + t / (1 - t)) / (1 - t) ** 2 if t < 1 else 0.0
            for j in range(3):
                g = smooth(g)
                NERR[0] = 0.0
                r = _gk_adapt(g, 0.0, 1.0, tol, 0)
                if NERR[0] <= 1e-7 * max(1.0, abs(r)):
                    break
        if NERR[0] > 1e-7 * max(1.0, abs(r)):
            err('Questionable accuracy: the integral may diverge')
    if r != r or abs(r) == float('inf'):
        err('Questionable accuracy: the integral may diverge')
    if type(r) is complex:
        if abs(r.imag) < 1e-12 * (1 + abs(r.real)):
            return r.real
        return fromcomplex(r)
    return r

def nint0(f, x, a, b, tol=1e-10):
    # adaptive Gauss-Kronrod 7-15
    sgn = 1.0
    av = a
    bv = b
    if isinf(a) or isinf(b):
        # transform
        if a == 'inf' or b == ('*', -1, 'inf'):
            return -nint0(f, x, b, a, tol)
        if isinf(a) and isinf(b):
            g = lambda t: _nv(f, x, t / (1 - t * t)) * (1 + t * t) / (1 - t * t) ** 2
            return _gk_adapt(g, -1.0, 1.0, tol, 0)
        if isinf(b):
            a0 = nreal(a)
            g = lambda t: _nv(f, x, a0 + t / (1 - t)) / (1 - t) ** 2
            return _gk_adapt(g, 0.0, 1.0, tol, 0)
        b0 = nreal(b)
        g = lambda t: _nv(f, x, b0 - (1 - t) / t) / (t * t)
        return _gk_adapt(g, 0.0, 1.0, tol, 0)
    a0 = nreal(a)
    b0 = nreal(b)
    g = lambda t: _nv(f, x, t)
    return _gk_adapt(g, a0, b0, tol, 0)

def smooth(g):
    # u = 3t^2-2t^3: the integrand near both ends gets flatter
    return lambda t: g(t * t * (3 - 2 * t)) * 6 * t * (1 - t)

def nint_split(f, x, a, b):
    # numeric integral, split at the poles inside (a, b)
    pts = [a] + (singular_points(f, x, a, b) or []) + [b]
    r = 0
    for i in range(len(pts) - 1):
        r = add(r, nint(f, x, pts[i], pts[i + 1]))
    return r

def trigk(f, x, out):
    # angular frequencies k of sin/cos(k*x+c) in f
    if type(f) is not tuple or f[0] == 'Q':
        return
    if f[0] in ('sin', 'cos') and not freeof(f[1], x):
        lu = linear(f[1], x)
        out.append(lu[0] if lu is not None and isconst(lu[0]) else None)
    for a in f[1:]:
        trigk(a, x, out)

def nint_osc(f, x, a, b, tol):
    # oscillatory integrand on [a, inf): integrate one half period at a
    # time and extrapolate the partial sums (Wynn epsilon); None if f is
    # not of that kind
    ks = []
    trigk(f, x, ks)
    if not ks or None in ks:
        return None
    k = max([abs(tofl(nval(q))) for q in ks])
    if k == 0:
        return None
    sgn_ = 1.0
    if isinf(a):
        # (-inf, b]: x -> -x
        f = subs(f, x, neg(x))
        a, b = neg(b), 'inf'
        if a == ('*', -1, ('*', -1, 'inf')):
            a = 'inf'
    a0 = tofl(nval(a))
    h = math.pi / k
    g = lambda t: _nv(f, x, t)
    sums = []
    terms = []
    s_ = 0.0
    t = a0
    for i in range(40):
        c = _gk_adapt(g, t, t + h, tol, 6)
        s_ += c
        terms.append(abs(c))
        t += h
        sums.append(s_)
    if max(terms[-4:]) > 0.25 * max(terms[:4]) and max(terms[-4:]) > 1e-12:
        # the half-period pieces do not shrink: it does not converge
        err('Questionable accuracy: the integral may diverge')
    est = wynn(sums)
    est2 = wynn(sums[:-6])
    if est is None or est2 is None or abs(est - est2) > 1e-7 * max(1.0, abs(est)):
        err('Questionable accuracy: the integral may diverge')
    return sgn_ * est

def wynn(S):
    # Wynn epsilon extrapolation of the partial sums S
    n = len(S)
    e0 = [0.0] * (n + 1)
    e1 = list(S)
    best = S[-1]
    for k in range(1, n):
        e2 = []
        for j in range(len(e1) - 1):
            d = e1[j + 1] - e1[j]
            if d == 0:
                return e1[j + 1]
            e2.append(e0[j + 1] + 1.0 / d)
        if k % 2 == 0 and e2:
            best = e2[-1]
        e0, e1 = e1, e2
        if len(e1) < 2:
            break
    return best

def _nv(f, x, t):
    try:
        v = nval(f, {x: t})
    except ZeroDivisionError:
        return 0.0
    except (ValueError, OverflowError):
        return 0.0
    if type(v) is complex:
        if abs(v.imag) > 1e-12 * (1 + abs(v.real)):
            return v
        v = v.real
    if v != v or v in (float('inf'), float('-inf')):
        return 0.0
    return v

XGK = (0.991455371120812639206854697526329, 0.949107912342758524526189684047851,
       0.864864423359769072789712788640926, 0.741531185599394439863864773280788,
       0.586087235467691130294144845693013, 0.405845151377397166906606412076961,
       0.207784955007898467600689403773245, 0.0)
WGK = (0.022935322010529224963732008058970, 0.063092092629978553290700663189204,
       0.104790010322250183839876322541518, 0.140653259715525918745189590510238,
       0.169004726639267902826583426598550, 0.190350578064785409913256402421014,
       0.204432940075298892414161999234649, 0.209482141084727828012999174891714)
WG = (0.129484966168869693270611432679082, 0.279705391489276667901467771423780,
      0.381830050505118944950369775488975, 0.417959183673469387755102040816327)

def _gk(g, a, b):
    c = 0.5 * (a + b)
    h = 0.5 * (b - a)
    fc = g(c)
    rk = fc * WGK[7]
    rg = fc * WG[3]
    for j in range(7):
        dx = h * XGK[j]
        f1 = g(c - dx)
        f2 = g(c + dx)
        rk += WGK[j] * (f1 + f2)
        if j % 2 == 1:
            rg += WG[j // 2] * (f1 + f2)
    return rk * h, abs((rk - rg) * h)

def _gk_adapt(g, a, b, tol, depth):
    r, e = _gk(g, a, b)
    NBUD[0] -= 1
    if NBUD[0] < 0:
        # out of steps (the calculator is slow): report it as inaccurate
        NERR[0] += e + 1e-6 * (1 + abs(r))
        return r
    if e <= tol * max(1.0, abs(r)):
        return r
    if depth > 18:
        NERR[0] += e
        return r
    m = 0.5 * (a + b)
    return _gk_adapt(g, a, m, tol / 2, depth + 1) + _gk_adapt(g, m, b, tol / 2, depth + 1)

# ===================================================== series
BIGP = 10 ** 6

def s_const(c):
    if c == 0:
        return ({}, BIGP)
    return ({0: c}, BIGP)

def s_val(A):
    if not A[0]:
        return A[1]
    m = None
    for k in A[0]:
        if m is None or ncmp(k, m) < 0:
            m = k
    return m

def cs(c):
    c = expand(c)
    if hasdenom(c):
        c = autocancel(c)
    return c

def s_add(A, B):
    p = A[1] if ncmp(A[1], B[1]) < 0 else B[1]
    d = {}
    for S in (A, B):
        for k in S[0]:
            if ncmp(k, p) < 0:
                d[k] = add(d.get(k, 0), S[0][k])
    out = {}
    for k in d:
        v = cs(d[k])
        if v != 0:
            out[k] = v
    return (out, p)

def s_mul(A, B):
    vA = s_val(A)
    vB = s_val(B)
    p1 = nadd(A[1], vB)
    p2 = nadd(B[1], vA)
    p = p1 if ncmp(p1, p2) < 0 else p2
    d = {}
    for a in A[0]:
        for b in B[0]:
            k = nadd(a, b)
            if ncmp(k, p) < 0:
                d[k] = add(d.get(k, 0), mul(A[0][a], B[0][b]))
    out = {}
    for k in d:
        v = cs(d[k])
        if v != 0:
            out[k] = v
    return (out, p)

def s_scale(A, c, shift=0):
    out = {}
    for k in A[0]:
        v = cs(mul(A[0][k], c))
        if v != 0:
            out[nadd(k, shift)] = v
    return (out, nadd(A[1], shift))

def s_lead(A):
    if not A[0]:
        raise NoSeries()
    v = s_val(A)
    return v, A[0][v]

def s_split(A):
    # A = c t^a (1 + U), returns (a, c, U)
    a, c = s_lead(A)
    U = s_scale(A, pw(c, -1), nneg(a))
    U = (dict([(k, U[0][k]) for k in U[0] if k != 0]), U[1])
    return a, c, U

def s_powser(U, coefs):
    # sum coefs[k] * U^k, U with positive valuation
    res = s_const(coefs[0])
    res = (res[0], U[1])
    P = ({0: 1}, BIGP)
    for k in range(1, len(coefs)):
        P = s_mul(P, U)
        if not P[0]:
            break
        if coefs[k] != 0:
            res = s_add(res, s_scale(P, coefs[k]))
    return res

def nterms(U):
    v = s_val(U)
    if ncmp(v, 0) <= 0:
        raise NoSeries()
    p = U[1]
    if ncmp(p, BIGP) >= 0:
        return 0 if not U[0] else 30
    n = nfloor(ndiv(p, v)) + 1
    if n > 30:
        n = 30
    return n

def s_pow(A, p):
    if type(p) is int and p >= 0:
        R = ({0: 1}, BIGP)
        for _ in range(p):
            R = s_mul(R, A)
        return R
    a, c, U = s_split(A)
    n = nterms(U) if U[0] else 0
    coefs = [1]
    b = 1
    for k in range(1, n + 1):
        b = mul(b, div(sub(p, k - 1), k))
        coefs.append(b)
    S = s_powser(U, coefs) if U[0] else ({0: 1}, U[1])
    ap = mul(a, p)
    if not israt(ap):
        raise NoSeries()
    cp = pw(c, p)
    return s_scale(S, cp, ap)

def s_exp(A):
    neg_ = [k for k in A[0] if ncmp(k, 0) < 0]
    if neg_:
        raise NoSeries()
    c0 = A[0].get(0, 0)
    U = (dict([(k, A[0][k]) for k in A[0] if k != 0]), A[1])
    shift = 0
    if has(c0, LNT):
        cc = coeffs(c0, LNT)
        if cc is None or len(cc) != 2 or not israt(cc[1]):
            raise NoSeries()
        shift = cc[1]
        c0 = cc[0]
    n = nterms(U) if U[0] else 0
    coefs = [1]
    f = 1
    for k in range(1, n + 1):
        f = f * k
        coefs.append(Q(1, f))
    S = s_powser(U, coefs) if U[0] else ({0: 1}, U[1])
    return s_scale(S, pw('e', c0), shift)

def s_ln(A):
    a, c, U = s_split(A)
    n = nterms(U) if U[0] else 0
    coefs = [0]
    for k in range(1, n + 1):
        coefs.append(Q((-1) ** (k + 1), k))
    S = s_powser(U, coefs) if U[0] else ({}, U[1])
    base = add(fn('ln', c), mul(a, LNT))
    return s_add(S, (({0: base} if base != 0 else {}), BIGP))

def s_fun(name, A):
    neg_ = [k for k in A[0] if ncmp(k, 0) < 0]
    if neg_:
        if name == 'arctan':
            a, c = s_lead(A)
            sg = nval(c)
            sg = 1 if (type(sg) is not complex and sg > 0) else -1
            inv_ = s_pow(A, -1)
            return s_add(s_const(mul(sg, HALF, 'pi')), s_scale(s_fun('arctan', inv_), -1))
        if name == 'tanh':
            a, c = s_lead(A)
            return s_const(1 if nval(c).real > 0 else -1)
        raise NoSeries()
    c0 = A[0].get(0, 0)
    if has(c0, LNT):
        raise NoSeries()
    U = (dict([(k, A[0][k]) for k in A[0] if k != 0]), A[1])
    if name == 'abs' or name == 'sign':
        a, c = s_lead(A)
        v = nval(subs(c, LNT, -1000)) if has(c, LNT) else nval(c)
        if type(v) is complex:
            raise NoSeries()
        sg = 1 if v > 0 else -1
        if name == 'sign':
            return s_const(sg)
        return s_scale(A, sg)
    if name in ('floor', 'ceiling', 'ipart', 'round', 'int', 'fpart'):
        raise NoSeries()
    n = nterms(U) if U[0] else 0
    z = 'Z_'
    g = fn(name, z)
    coefs = [subs(g, z, c0)]
    fact = 1
    for k in range(1, n + 1):
        g = diff(g, z)
        fact *= k
        coefs.append(cs(div(subs(g, z, c0), fact)))
    for cc in coefs:
        if has(cc, 'undef') or cc == 'undef' or has(cc, 'inf'):
            raise NoSeries()
    if not U[0]:
        return s_const(coefs[0]) if True else None
    return s_powser(U, coefs)

def ser(e, N):
    # series of e in TV (t->0+), working precision N
    if freeof(e, TV):
        return s_const(e)
    if e == TV:
        return ({1: 1}, BIGP)
    h = e[0]
    if h == '+':
        R = ({}, BIGP)
        for a in e[1:]:
            R = s_add(R, ser(a, N))
        return trunc(R, N)
    if h == '*':
        R = ({0: 1}, BIGP)
        for a in e[1:]:
            R = trunc(s_mul(R, ser(a, N)), N)
        return R
    if h == '^':
        b = e[1]
        p = e[2]
        if freeof(p, TV):
            B = ser(b, N)
            if israt(p):
                return trunc(s_pow(B, p), N)
            if isconst(p) or True:
                a, c, U = s_split(B)
                if a != 0:
                    raise NoSeries()
                return trunc(s_pow(B, p), N)
        if freeof(b, TV):
            return trunc(s_exp(s_scale(ser(p, N), fn('ln', b))), N)
        return trunc(s_exp(s_mul(ser(p, N), s_ln(ser(b, N)))), N)
    if h == 'ln':
        return trunc(s_ln(ser(e[1], N)), N)
    if h == 'log':
        b = e[2] if len(e) > 2 else 10
        return trunc(s_scale(s_ln(ser(e[1], N)), pw(fn('ln', b), -1)), N)
    if len(e) == 2:
        return trunc(s_fun(h, ser(e[1], N)), N)
    raise NoSeries()

def trunc(A, N):
    if ncmp(A[1], N) <= 0:
        return A
    return (dict([(k, A[0][k]) for k in A[0] if ncmp(k, N) < 0]), N)

def series_t(e, order, need=None):
    # compute series in TV accurate through exponent 'order'
    extra = 3
    for _ in range(4):
        S = ser(e, nadd(order, extra))
        if ncmp(S[1], order) > 0 and (need is None or S[0]):
            return S
        extra = extra * 2 + 2
    return S

def lead_t(e):
    # leading term (a, c) of e as TV->0+
    for N in (3, 6, 12, 24):
        S = ser(e, N)
        if S[0]:
            v = s_val(S)
            if ncmp(v, S[1]) < 0:
                return v, S[0][v]
    return None

# ===================================================== limits
def lnt_lim(c):
    # limit of c as LNT -> -inf, c a rational function of LNT
    n, d = numer_denom(c)
    cn = coeffs(n, LNT)
    cd = coeffs(d, LNT)
    if cn is None or cd is None:
        raise NoSeries()
    p = len(cn) - 1
    q = len(cd) - 1
    if p < q:
        return 0
    if p == q:
        return div(cn[p], cd[q])
    v = lnt_sign(c)
    if type(v) is complex:
        return 'undef'
    return 'inf' if v > 0 else ('*', -1, 'inf')

def lnt_sign(c):
    # sign of c as LNT -> -inf, c polynomial in LNT
    cc = coeffs(c, LNT)
    if cc is None:
        v = nval(subs(c, LNT, -1e6))
        return v
    k = len(cc) - 1
    lead = cc[k]
    v = nval(lead)
    if type(v) is complex:
        return v
    if k % 2:
        v = -v
    return v

def limit(f, x, a, dirn=0):
    return infnorm(limit0(f, x, a, dirn))

def infnorm(r):
    # c*inf -> inf or -inf for a nonzero constant c
    if isnode(r, '*') and ('inf' in r[1:]):
        c = mul_list([b for b in r[1:] if b != 'inf'])
        if isconst(c):
            try:
                v = fv_(c)
                return 'inf' if v > 0 else (('*', -1, 'inf') if v < 0 else 'undef')
            except Exception:
                pass
    return r

def limit0(f, x, a, dirn=0):
    if isnode(f, 'list') or isnode(f, 'mat'):
        return mapexpr(lambda g: limit(g, x, a, dirn), f)
    if freeof(f, x):
        return f
    if haswhen(f, x) and isconst(a) and firstwhen_(f, x):
        return whenlimit(f, x, a, dirn)
    if hashead(f, 'fact') and isinf(a):
        g = stirling(factnorm(f, x), x)
        if g != f:
            return limit(g, x, a, dirn)
    if isconst(a):
        r = lim_bounded(f, x, a, dirn)
        if r is not None:
            return r
    if a == 'inf' or a == ('*', -1, 'inf'):
        sub_ = pw(TV, -1) if a == 'inf' else neg(pw(TV, -1))
        return lim_side(f, x, sub_, a)
    if dirn == 0 and not has_disc(f):
        try:
            v = subs(f, x, a)
            if v != 'undef' and freeof(v, 'undef') and not has(v, 'inf'):
                v2 = v
                if isconst(v2):
                    vv = nval(v2)
                    if type(vv) is complex and abs(vv.imag) > 1e-12 and freeof(f, 'i'):
                        raise ValueError
                return v
        except (CASError, ZeroDivisionError, ValueError, TypeError):
            pass
    if dirn == 1:
        return lim_side(f, x, add(a, TV), a)
    if dirn == -1:
        return lim_side(f, x, sub(a, TV), a)
    r = lim_side(f, x, add(a, TV), a)
    l = lim_side(f, x, sub(a, TV), a)
    if r == l:
        return r
    if isnode(r, 'limit') or isnode(l, 'limit'):
        return ('limit', f, x, a)
    try:
        if isconst(r) and isconst(l) and not has(r, 'inf') and not has(l, 'inf'):
            if abs(nval(r) - nval(l)) < 1e-12:
                return r
    except Exception:
        pass
    return 'undef'

def hashead(f, h):
    if type(f) is not tuple or f[0] == 'Q':
        return False
    return f[0] == h or any([hashead(b, h) for b in f[1:]])

STEPF = ('floor', 'ceiling', 'fpart', 'ipart', 'int', 'round')

def factnorm(f, x):
    # (u+k)! -> (u+k)*...*(u+1)*u! for the smallest u in f, so factorial
    # ratios cancel
    fs = []
    def walk(e):
        if type(e) is not tuple or e[0] == 'Q':
            return
        if e[0] == 'fact' and not freeof(e[1], x):
            fs.append(e[1])
        for b in e[1:]:
            walk(b)
    walk(f)
    if not fs:
        return f
    base = fs[0]
    for u in fs:
        d = sub(base, u)
        if isint(d) and d > 0:
            base = u
    def rep(e):
        if type(e) is not tuple or e[0] == 'Q':
            return e
        if e[0] == 'fact' and not freeof(e[1], x):
            k = sub(e[1], base)
            if isint(k) and 0 < k <= 50:
                return mul_list([add(base, j) for j in range(1, k + 1)] + [fn('fact', base)])
            return e
        return simp((e[0],) + tuple(rep(b) for b in e[1:]))
    return autocancel(rep(f))

def stirling(f, x):
    # u! -> sqrt(2*pi*u)*(u/e)^u: same limit at infinity of any ratio
    if type(f) is not tuple or f[0] == 'Q':
        return f
    if f[0] == 'fact' and not freeof(f[1], x):
        u = stirling(f[1], x)
        return mul(sqrt(mul(2, 'pi', u)), pw(div(u, 'e'), u))
    return simp((f[0],) + tuple(stirling(b, x) for b in f[1:]))

def bounded_nodes(f, x, a, dirn, out):
    # floor-like and sin/cos nodes whose argument has no finite limit
    if type(f) is not tuple or f[0] == 'Q':
        return
    for b in f[1:]:
        bounded_nodes(b, x, a, dirn, out)
    if len(f) == 2 and not freeof(f[1], x) and f[0] in STEPF + ('sin', 'cos'):
        try:
            L = limit(f[1], x, a, dirn)
        except Exception:
            return
        if L in ('inf', ('*', -1, 'inf')) or L == 'undef' or isnode(L, 'limit'):
            if (f, 1) not in out:
                out.append((f, 1))
        elif f[0] in STEPF and not isinf(a):
            if (f, 0) not in out:
                out.append((f, 0))

def lim_bounded(f, x, a, dirn):
    # squeeze: replace bounded oscillating parts by their bounds; when the
    # limit is the same for every bound, that is the limit
    ns = []
    bounded_nodes(f, x, a, dirn, ns)
    if not ns:
        return None
    if not isinf(a):
        # step functions at a finite point: their value just beside a
        if dirn == 0:
            r = lim_bounded(f, x, a, 1)
            l = lim_bounded(f, x, a, -1)
            if r is None or l is None:
                return None
            return r if r == l else 'undef'
        stp = [n for n, k in ns if k == 0]
        ns = [n for n, k in ns if k == 1]
        if stp:
            t = fv_(a) + dirn * 1e-7 * (1 + abs(fv_(a)))
            g = f
            for n in stp:
                try:
                    g = replnode_(g, n, exactify(nval(n, {x: t})))
                except Exception:
                    return None
            return limit(g, x, a, dirn)
    else:
        ns = [n for n, k in ns]
    if not ns:
        return None
    C = 'C_'
    reps = []
    for n in ns:
        if n[0] in ('sin', 'cos'):
            reps.append((n, C, (-1, 0, 1)))
        elif n[0] in ('floor', 'int', 'ipart'):
            reps.append((n, sub(n[1], C), (0, Q(1, 2), 1)))
        elif n[0] == 'ceiling':
            reps.append((n, add(n[1], C), (0, Q(1, 2), 1)))
        elif n[0] == 'round':
            reps.append((n, add(n[1], C), (Q(-1, 2), 0, Q(1, 2))))
        else:
            reps.append((n, C, (0, Q(1, 2), 1)))
    if len(reps) > 1:
        return None
    n, r, cs = reps[0]
    g = replnode_(f, n, r)
    vals = []
    for c in cs:
        v = limit(subs(g, C, c), x, a, dirn)
        if isnode(v, 'limit'):
            return None
        vals.append(v)
    if vals[0] == vals[1] == vals[2] and vals[0] != 'undef':
        return vals[0]
    return 'undef'

def replnode_(f, w, r):
    if f == w:
        return r
    if type(f) is not tuple or f[0] == 'Q':
        return f
    return simp((f[0],) + tuple(replnode_(b, w, r) for b in f[1:]))

def has_disc(f):
    if type(f) is not tuple or f[0] == 'Q':
        return False
    if f[0] in ('floor', 'ceiling', 'sign', 'ipart', 'round', 'fpart', 'int', 'when', 'abs', 'mod'):
        return True
    for a in f[1:]:
        if has_disc(a):
            return True
    return False

def lim_side(f, x, sub_, a):
    g = subs(f, x, sub_)
    try:
        r = lead_t(g)
        if r is None:
            return 0
        al, c = r
        if has(c, TV):
            raise NoSeries()
        if ncmp(al, 0) > 0:
            return 0
        if has(c, LNT) and al == 0:
            return lnt_lim(c)
        if has(c, LNT):
            v = lnt_sign(c)
            if type(v) is complex:
                return 'undef'
            if v == 0:
                raise NoSeries()
            return 'inf' if v > 0 else ('*', -1, 'inf')
        if al == 0:
            return c
        if not isconst(c):
            return mul(c, 'inf')
        v = nval(c)
        if type(v) is complex:
            return 'undef'
        return 'inf' if v > 0 else ('*', -1, 'inf')
    except (NoSeries, CASError, ZeroDivisionError, ValueError, TypeError, OverflowError):
        pass
    r = lim_lh(g, 0)
    if r is not None:
        return r
    r = lim_log(g)
    if r is not None:
        return r
    return lim_num(g, a)

def lnexp(g):
    # ln(g) with products and powers split up (g > 0 assumed)
    h = head(g)
    if h == '*':
        return add_list([lnexp(b) for b in g[1:]])
    if h == '^':
        if g[1] == 'e':
            return g[2]
        return mul(g[2], lnexp(g[1]))
    if isnum(g) and nsign(g) > 0:
        return fn('ln', g)
    return fn('ln', g)

def lim_log(g, depth=0):
    # limit of a product of powers and exponentials through its logarithm
    if head(g) not in ('*', '^'):
        return None
    v = None
    for t in (1e-3, 1e-2, 1e-1):
        try:
            v = nval(g, {TV: t})
        except Exception:
            v = None
        if v is not None and type(v) is not complex and v == v and v != 0 and abs(v) != float('inf'):
            break
        v = None
    if v is None:
        return None
    sg = 1 if v > 0 else -1
    L = lim_val(autocancel(lnexp(mul(sg, g))), depth)
    if L is None or isnode(L, 'limit') or L == 'undef':
        return None
    if L == 'inf':
        return 'inf' if sg > 0 else ('*', -1, 'inf')
    if L == ('*', -1, 'inf'):
        return 0
    if isconst(L):
        return mul(sg, pw('e', L))
    return None

def lim_val(g, depth):
    # limit of g (in TV -> 0+) by series, then L'Hopital
    try:
        r = lead_t(g)
        if r is None:
            return 0
        al, c = r
        if has(c, TV):
            raise NoSeries()
        if ncmp(al, 0) > 0:
            return 0
        if has(c, LNT) and al == 0:
            return lnt_lim(c)
        if has(c, LNT):
            v = lnt_sign(c)
            return 'inf' if v > 0 else ('*', -1, 'inf')
        if al == 0:
            return c
        v = nval(c)
        return 'inf' if v > 0 else ('*', -1, 'inf')
    except (NoSeries, CASError, ZeroDivisionError, ValueError, TypeError, OverflowError):
        pass
    r = lim_lh(g, depth + 1)
    if r is None and depth < 3:
        r = lim_log(g, depth + 1)
    return r

def lim_lh(g, depth):
    if depth > 4:
        return None
    if freeof(g, TV):
        return g
    h = head(g)
    if h == '^' and not freeof(g[2], TV):
        L = lim_val(mul(g[2], fn('ln', g[1])), depth)
        if L is None:
            return None
        return pw('e', L)
    if h == '^' and isnum(g[2]):
        L = lim_val(g[1], depth)
        if L is None:
            return None
        if L == 0 and nsign(g[2]) < 0:
            return 'inf'
        return pw(L, g[2])
    if h == '*':
        nu, de = numer_denom(g)
        if de != 1:
            ln_ = lim_val(nu, depth)
            ld = lim_val(de, depth)
            if ln_ is None or ld is None:
                return None
            if (ln_ == 0 and ld == 0) or (isinfv(ln_) and isinfv(ld)):
                return lim_val(autocancel(div(diff(nu, TV), diff(de, TV))), depth)
            if ld == 0:
                s = nval(subs(de, TV, 1e-9))
                sn = nval(ln_) if isconst(ln_) and not isinfv(ln_) else (1 if ln_ == 'inf' else -1)
                return 'inf' if (s.real if type(s) is complex else s) * (sn.real if type(sn) is complex else sn) > 0 else ('*', -1, 'inf')
            return div(ln_, ld)
        # product: 0 * inf
        ls = [lim_val(fct, depth) for fct in g[1:]]
        if None in ls:
            return None
        zero = [i for i in range(len(ls)) if ls[i] == 0]
        infs = [i for i in range(len(ls)) if isinfv(ls[i])]
        if zero and infs:
            r = lim_log(g, depth + 1)
            if r is not None:
                return r
            i = zero[0]
            j = infs[0]
            rest = mul_list([g[k + 1] for k in range(len(ls)) if k != i and k != j])
            q = div(g[i + 1], pw(g[j + 1], -1))
            r = lim_val(q, depth)
            if r is None:
                return None
            return mul(r, lim_val(rest, depth))
        return mul_list(ls)
    if h == '+':
        ls = [lim_val(t, depth) for t in g[1:]]
        if None in ls:
            return None
        r = add_list(ls)
        if r != 'undef':
            return r
        # inf - inf: factor out the first infinite term
        ii = [k for k in range(len(ls)) if isinfv(ls[k])]
        if not ii:
            return None
        for i in ii:
            A = g[i + 1]
            rest = add_list([g[k + 1] for k in range(len(ls)) if k != i])
            q = lim_val(autocancel(div(rest, A)), depth)
            if q is None or q == 'undef' or isinfv(q) or q == -1:
                continue
            return mul(ls[i], add(1, q))
        return None
    if type(g) is tuple and len(g) == 2:
        L = lim_val(g[1], depth)
        if L is None:
            return None
        return fn(h, L)
    return None

def isinfv(v):
    return v == 'inf' or v == ('*', -1, 'inf')

def lim_num(g, a):
    try:
        vals = []
        for k in range(4, 9):
            t = 10.0 ** (-k)
            vals.append(nval(g, {TV: t}))
        v1 = vals[-1]
        v2 = vals[-2]
        if type(v1) is complex or type(v2) is complex:
            return ('limit', g)
        if abs(v1) > 1e12 and abs(v1) > abs(v2):
            return 'inf' if v1 > 0 else ('*', -1, 'inf')
        if abs(v1) < 1e-6 and abs(v1) < abs(vals[-3]) and abs(v2) < abs(vals[-3]):
            return 0
        if abs(v1 - v2) < 1e-6 * (1 + abs(v1)):
            return exactify_guess(v1)
    except Exception:
        pass
    return ('limit', g)

def exactify_guess(v):
    r = float2rat(v, 1e-9)
    n, d = nd(r)
    if d < 1000:
        return r
    return v

# ===================================================== taylor / series
def series_at(f, x, a, order):
    if a == 'inf' or a == ('*', -1, 'inf'):
        sub_ = pw(TV, -1) if a == 'inf' else neg(pw(TV, -1))
        back = pw(x, -1) if a == 'inf' else neg(pw(x, -1))
    else:
        sub_ = add(a, TV)
        back = sub(x, a)
    g = subs(f, x, sub_)
    S = series_t(g, order)
    return S, back

def taylor(f, x, n, a=0):
    try:
        S, back = series_at(f, x, a, n)
    except (NoSeries, CASError, ZeroDivisionError, ValueError):
        return taylor_d(f, x, n, a)
    terms = []
    for k in S[0]:
        if ncmp(k, n) > 0:
            continue
        if not (type(k) is int and k >= 0) or has(S[0][k], LNT):
            return ('taylor', f, x, n, a)
        terms.append(mul(S[0][k], pw(back, k)))
    return add_list(terms)

def taylor_d(f, x, n, a):
    terms = []
    g = f
    fact = 1
    for k in range(n + 1):
        if k:
            fact *= k
            g = diff(g, x)
        v = subs(g, x, a)
        if has(v, 'undef') or v == 'undef' or has(v, 'inf'):
            return ('taylor', f, x, n, a)
        terms.append(mul(div(v, fact), pw(sub(x, a), k)))
    return add_list(terms)

def series_cmd(f, x, n, a=0):
    try:
        S, back = series_at(f, x, a, n)
    except (NoSeries, CASError, ZeroDivisionError, ValueError):
        return ('series', f, x, n, a)
    terms = []
    lnback = fn('ln', back) if not (a == 'inf' or a == ('*', -1, 'inf')) else neg(fn('ln', fn('abs', x)))
    for k in S[0]:
        if ncmp(k, n) > 0:
            continue
        c = subs(S[0][k], LNT, lnback)
        terms.append(mul(c, pw(back, k)))
    return add_list(terms)

def dominant(f, x, a=0):
    if a == 'inf' or a == ('*', -1, 'inf'):
        sub_ = pw(TV, -1) if a == 'inf' else neg(pw(TV, -1))
        back = pw(x, -1) if a == 'inf' else neg(pw(x, -1))
        lnback = neg(fn('ln', fn('abs', x)))
    else:
        sub_ = add(a, TV)
        back = sub(x, a)
        lnback = fn('ln', back)
    try:
        r = lead_t(subs(f, x, sub_))
    except (NoSeries, CASError, ZeroDivisionError, ValueError):
        return ('dominantterm', f, x, a)
    if r is None:
        return 0
    k, c = r
    return mul(subs(c, LNT, lnback), pw(back, k))

# ===================================================== sums and products
def bern(n):
    B = [1]
    for m in range(1, n + 1):
        s = 0
        c = 1
        for k in range(m):
            # binom(m+1,k)
            s = nadd(s, nmul(binom(m + 1, k), B[k]))
        B.append(nneg(ndiv(s, m + 1)))
    return B

def binom(n, k):
    if k < 0 or k > n:
        return 0
    r = 1
    for i in range(1, k + 1):
        r = r * (n - k + i) // i
    return r

def powsum(j, n):
    # sum_{k=1}^n k^j as expression in n
    B = bern(j)
    if j >= 1:
        B[1] = Q(1, 2)
    terms = []
    for i in range(j + 1):
        terms.append(mul(binom(j + 1, i), B[i], pw(n, j + 1 - i)))
    return mul(Q(1, j + 1), add_list(terms))

ZETA = {2: ('Q', 1, 6), 4: ('Q', 1, 90), 6: ('Q', 1, 945), 8: ('Q', 1, 9450), 10: ('Q', 1, 93555)}

def sumseq(f, k, a, b):
    if isint(a) and isint(b):
        if b < a - 1:
            return neg(sumseq(f, k, b + 1, a - 1))
        if b - a <= 300:
            terms = [subs(f, k, j) for j in range(a, b + 1)]
            return add_list(terms)
    if freeof(f, k):
        return mul(f, add(sub(b, a), 1))
    # polynomial in k
    cs_ = coeffs(f, k)
    if cs_ is not None and b != 'inf':
        res = []
        for j in range(len(cs_)):
            if cs_[j] != 0:
                if j == 0:
                    res.append(mul(cs_[0], add(sub(b, a), 1)))
                else:
                    res.append(mul(cs_[j], sub(powsum(j, b), powsum(j, sub(a, 1)))))
        return expand(add_list(res))
    # geometric: f = C * B^(p k + q)
    r = geomsum(f, k, a, b)
    if r is not None:
        return r
    # telescoping rational
    r = telesum(f, k, a, b)
    if r is not None:
        return r
    # sum c*r^k/k! = c*e^r
    if b == 'inf' and isint(a) and has(f, ('fact', k)):
        g = mul(f, ('fact', k))
        gs = geomsum(g, k, 0, 'inf') if False else None
        cr = expsum(g, k)
        if cr is not None:
            C, r = cr
            tot = mul(C, pw('e', r))
            if a > 0:
                tot = sub(tot, add_list([mul(C, div(pw(r, j), fact_(j))) for j in range(a)]))
            return tot
    # zeta / harmonic
    if b == 'inf' and isint(a):
        nu, de = numer_denom(f)
        if freeof(nu, k):
            dd = coeffs(de, k)
            if dd is not None and len(dd) >= 2 and all([c == 0 for c in dd[:-1]]):
                p = len(dd) - 1
                if p == 1:
                    return 'inf' if nval(div(nu, dd[-1])).real > 0 else ('*', -1, 'inf')
                if p in ZETA and a >= 1:
                    z = mul(ZETA[p], pw('pi', p))
                    z = sub(z, add_list([pw(j, -p) for j in range(1, a)]))
                    return mul(div(nu, dd[-1]), z)
    if (isint(a) or isconst(a)) and (b == 'inf' or isint(b)) and freeofall(f, [s for s in symbols(f) if s != k]):
        return nsum(f, k, a, b)
    return ('sumseq', f, k, a, b)

def expsum(g, k):
    # g = C * r^k  -> (C, r)
    if freeof(g, k):
        return g, 1
    fs = g[1:] if isnode(g, '*') else (g,)
    C = []
    r = None
    for h in fs:
        if freeof(h, k):
            C.append(h)
        elif isnode(h, '^') and freeof(h[1], k) and h[2] == k and r is None:
            r = h[1]
        elif isnode(h, '^') and freeof(h[1], k) and linear(h[2], k) and linear(h[2], k)[1] == 0 and r is None:
            r = pw(h[1], linear(h[2], k)[0])
        else:
            return None
    if r is None:
        return None
    return mul_list(C), r

def geomsum(f, k, a, b):
    fs = f[1:] if isnode(f, '*') else (f,)
    C = []
    base = None
    ex = None
    for g in fs:
        if freeof(g, k):
            C.append(g)
        elif isnode(g, '^') and freeof(g[1], k) and linear(g[2], k):
            if base is not None:
                if g[1] == base or (isnum(g[1]) and isnum(base)):
                    # combine numeric bases
                    lp = linear(g[2], k)
                    lb = linear(ex, k)
                    if lp[0] == 1 and lb[0] == 1:
                        C.append(pw(g[1], lp[1]))
                        C.append(pw(base, lb[1]))
                        base = mul(base, g[1])
                        ex = k
                        continue
                return None
            base = g[1]
            ex = g[2]
        else:
            return None
    if base is None:
        return None
    p, q = linear(ex, k)
    r = pw(base, p)
    Cq = mul(mul_list(C), pw(base, q))
    if b == 'inf':
        if isconst(r):
            v = nval(r)
            if abs(v) < 1:
                return div(mul(Cq, pw(r, a)), sub(1, r))
            return 'inf' if nval(Cq).real > 0 and v.real > 0 else 'undef'
        return None
    if r == 1:
        return mul(Cq, add(sub(b, a), 1))
    return div(mul(Cq, sub(pw(r, add(b, 1)), pw(r, a))), sub(r, 1))

def telesum(f, k, a, b):
    if not hasdenom(f):
        return None
    pf = partfrac(f, k)
    if pf is None:
        return None
    terms = pf[1:] if isnode(pf, '+') else (pf,)
    groups = []
    for t in terms:
        c, r = coef_rest(t)
        if isnode(r, '^') and r[2] == -1:
            lb = linear(r[1], k)
            if lb is None or lb[0] != 1:
                return None
            groups.append((c, lb[1]))
        elif freeof(t, k):
            return None
        else:
            return None
    if not groups:
        return None
    s0 = groups[0][1]
    tot = 0
    ms = []
    for c, s in groups:
        m = nsub(s, s0) if israt(s) and israt(s0) else None
        if m is None or not isint(m):
            return None
        ms.append(m)
        tot = add(tot, c)
    if tot != 0:
        if b == 'inf':
            return 'inf'
        return None
    mn = min(ms)
    if mn != 0:
        s0 = nadd(s0, mn)
        ms = [m - mn for m in ms]
    M = max(ms)
    res = []
    for idx in range(len(groups)):
        c = groups[idx][0]
        m = ms[idx]
        part = []
        for j in range(m, M):
            part.append(pw(add(a, j, s0), -1))
        if b != 'inf':
            for j in range(1, m + 1):
                part.append(pw(add(b, j, s0), -1))
        res.append(mul(c, add_list(part)))
    # shift sign: sum_{k=a+m}^{N+m} = common + lower tail(-) ...
    # lower part: sum_{k=a+m_j}^{a+M-1} g ; upper part: sum_{N+1}^{N+m_j} g
    return add_list(res)

def nsum(f, k, a, b):
    av = int(nreal(a))
    if b == 'inf':
        return nsum_inf(f, k, av)
    s = 0.0
    for n in range(av, int(b) + 1):
        s += nval(f, {k: float(n)})
    return s

def nsum_inf(f, k, av):
    # sum of f(k) for k = av, av+1, ...: divergence test, alternating
    # series by extrapolation, positive terms by Euler-Maclaurin with the
    # tail integral
    L = limit(f, k, 'inf')
    if L != 0 and not isnode(L, 'limit'):
        if L == 'undef' or not isconst(L):
            return 'undef'
        try:
            v = fv_(L)
        except Exception:
            return 'undef'
        return 'inf' if v > 0 else ('*', -1, 'inf')
    def t(n):
        z = nval(f, {k: float(n)})
        if type(z) is complex:
            if abs(z.imag) > 1e-12 * (1 + abs(z.real)):
                raise ValueError
            z = z.real
        return z
    first = [t(n) for n in range(av, av + 40)]
    tail = first[10:]
    if all([tail[i] * tail[i + 1] < 0 for i in range(len(tail) - 1)]):
        S = []
        s_ = 0.0
        for n in range(av, av + 60):
            s_ += t(n)
            S.append(s_)
        e1 = wynn(S)
        e2 = wynn(S[:-10])
        if abs(e1 - e2) > 1e-8 * max(1.0, abs(e1)):
            err('Questionable accuracy: the series may diverge')
        return e1
    N = av + 200
    tn = [t(n) for n in range(N, N + 20)]
    if all([v > 0 for v in tn]) or all([v < 0 for v in tn]):
        try:
            fe = exactify(f)
        except Exception:
            fe = f
        I = defint(fe, k, N, 'inf')
        if I in ('inf', ('*', -1, 'inf')):
            return I
        if not isconst(I) or has(I, 'undef'):
            I = nint(f, k, N, 'inf')
        s_ = 0.0
        for n in range(av, N):
            s_ += t(n)
        d1 = diff(f, k)
        d3 = diff(diff(d1, k), k)
        s_ += fv_(I) + t(N) / 2 - fv_(subs(d1, k, N)) / 12 + fv_(subs(d3, k, N)) / 720
        return s_
    # other terms: add until they are negligible
    s_ = 0.0
    prev = None
    for n in range(av, av + 20000):
        s_ += t(n)
        if n - av in (9999, 19999):
            if prev is not None and abs(s_ - prev) > 1e-9 * max(1.0, abs(s_)):
                err('Questionable accuracy: the series may diverge')
            prev = s_
    return s_

def prodseq(f, k, a, b):
    if isint(a) and isint(b):
        if b < a - 1:
            return pw(prodseq(f, k, b + 1, a - 1), -1)
        if b - a <= 300:
            return mul_list([subs(f, k, j) for j in range(a, b + 1)])
    if freeof(f, k):
        return pw(f, add(sub(b, a), 1))
    if f == k and a == 1:
        return fn('fact', b)
    if isnode(f, '^') and f[1] == k and isint(f[2]) and a == 1:
        return pw(fn('fact', b), f[2])
    if isnode(f, '*') and a == 1:
        c = [g for g in f[1:] if freeof(g, k)]
        r = [g for g in f[1:] if not freeof(g, k)]
        if c and len(r) == 1:
            rr = prodseq(r[0], k, a, b)
            if not isnode(rr, 'prodseq'):
                return mul(pw(mul_list(c), b), rr)
    fs = f[1:] if isnode(f, '*') else (f,)
    # exponent sums: prod c^g(k) = c^(sum g)
    if isnode(f, '^') and freeof(f[1], k):
        return pw(f[1], sumseq(f[2], k, a, b))
    return ('prodseq', f, k, a, b)

# ===================================================== trig expand/collect
def texpand(e):
    if type(e) is not tuple or e[0] == 'Q':
        return e
    args = [texpand(a) for a in e[1:]]
    e = simp((e[0],) + tuple(args))
    if type(e) is not tuple:
        return e
    h = e[0]
    if h in ('sin', 'cos', 'tan') and len(e) == 2:
        u = e[1]
        if h == 'tan':
            return texpand(div(fn('sin', u), fn('cos', u)))
        if isnode(u, '+'):
            a = u[1]
            b = add_list(list(u[2:]))
            sa, ca = texpand(fn('sin', a)), texpand(fn('cos', a))
            sb, cb = texpand(fn('sin', b)), texpand(fn('cos', b))
            if h == 'sin':
                return expand(add(mul(sa, cb), mul(ca, sb)))
            return expand(sub(mul(ca, cb), mul(sa, sb)))
        c, r = coef_rest(u)
        if isint(c) and c > 1 and c <= 30:
            s1 = texpand(fn('sin', r))
            c1 = texpand(fn('cos', r))
            z = expand_pow(add(c1, mul('i', s1)), c)
            re_, im_ = reim(z)
            return expand(im_ if h == 'sin' else re_)
    return e

def trigfactor(f):
    # f -> (name, arg) or None
    if head(f) in ('sin', 'cos') and len(f) == 2:
        return [(f[0], f[1])]
    if isnode(f, '^') and head(f[1]) in ('sin', 'cos') and isint(f[2]) and f[2] > 0:
        return [(f[1][0], f[1][1])] * f[2]
    return None

def tmul(a, b):
    # product of two trig factors (name, arg) -> sum expression
    n1, u = a
    n2, v = b
    if n1 == 'sin' and n2 == 'sin':
        return mul(HALF, sub(fn('cos', sub(u, v)), fn('cos', add(u, v))))
    if n1 == 'cos' and n2 == 'cos':
        return mul(HALF, add(fn('cos', sub(u, v)), fn('cos', add(u, v))))
    if n1 == 'cos':
        u, v = v, u
    return mul(HALF, add(fn('sin', add(u, v)), fn('sin', sub(u, v))))

def tcollect(e):
    if type(e) is not tuple or e[0] == 'Q':
        return e
    e = expand(e)
    if isnode(e, '+'):
        return add_list([tcollect_term(t) for t in e[1:]])
    return tcollect_term(e)

def tcollect_term(t):
    fs = t[1:] if isnode(t, '*') else (t,)
    other = []
    trig = []
    for f in fs:
        tf = trigfactor(f)
        if tf is None:
            other.append(f)
        else:
            trig.extend(tf)
    if len(trig) <= 1:
        return t
    acc = fn(trig[0][0], trig[0][1])
    for tf in trig[1:]:
        terms = acc[1:] if isnode(acc, '+') else (acc,)
        out = []
        for term in terms:
            c, r = coef_rest(term)
            ftf = trigfactor(r)
            if ftf is None or len(ftf) != 1:
                if freeof_trig(r):
                    out.append(mul(term, fn(tf[0], tf[1])))
                    continue
                out.append(mul(term, fn(tf[0], tf[1])))
                continue
            out.append(mul(c, tmul(ftf[0], tf)))
        acc = expand(add_list(out))
    return expand(mul(mul_list(other), acc))

def trigargs(e, out):
    if type(e) is not tuple or e[0] == 'Q':
        return
    if e[0] in ('sin', 'cos') and len(e) == 2:
        if e[1] not in out:
            out.append(e[1])
    for a in e[1:]:
        trigargs(a, out)

def pyth(e):
    # use sin^2+cos^2=1 when it shortens the expression
    from casout import fmt
    us = []
    trigargs(e, us)
    if not us:
        return e
    best = e
    bl = len(fmt(e))
    for u in us:
        s = fn('sin', u)
        c = fn('cos', u)
        for a, b in ((s, c), (c, s)):
            g = rsquare(e, a, b)
            if g is not None:
                g = expand(g)
                l = len(fmt(g))
                if l < bl:
                    best = g
                    bl = l
    return best

def rsquare(e, a, b):
    # replace a^n (n>=2) by a^(n-2)*(1-b^2)
    if type(e) is not tuple or e[0] == 'Q':
        return e
    if e[0] == '^' and e[1] == a and isint(e[2]) and e[2] >= 2:
        return mul(pw(a, e[2] - 2), sub(1, pw(b, 2)))
    return simp((e[0],) + tuple(rsquare(t, a, b) for t in e[1:]))

def freeof_trig(e):
    return not hastrig(e)

# ===================================================== misc calculus tools
def arclen(f, x, a, b):
    g = autocancel(expand(add(1, pw(diff(f, x), 2))))
    return defint(sqrt(g), x, a, b)

def tangentline(f, x, a):
    d = subs(diff(f, x), x, a)
    return expand(add(subs(f, x, a), mul(d, sub(x, a))))

def normalline(f, x, a):
    d = subs(diff(f, x), x, a)
    if d == 0:
        return ('=', x, a)
    return expand(sub(subs(f, x, a), div(sub(x, a), d)))

def impdif(eq, x, y, n=1):
    F = sub(eq[1], eq[2]) if isnode(eq, '=') else eq
    yp = autocancel(neg(div(diff(F, x), diff(F, y))))
    d = yp
    for _ in range(n - 1):
        d = autocancel(add(diff(d, x), mul(diff(d, y), yp)))
    return nice(d)

def avgrc(f, x, v, h=Q(1, 1000)):
    return div(sub(subs(f, x, add(v, h)), subs(f, x, v)), h)

def centraldiff(f, x, v, h=Q(1, 1000)):
    return div(sub(subs(f, x, add(v, h)), subs(f, x, sub(v, h))), mul(2, h))

def untan(e):
    if type(e) is not tuple or e[0] == 'Q':
        return e
    args = [untan(a) for a in e[1:]]
    if e[0] == 'tan' and len(args) == 1:
        return div(fn('sin', args[0]), fn('cos', args[0]))
    return simp((e[0],) + tuple(args))

def pyth_to(e, which):
    # express using 'which' (sin or cos) as far as possible
    other = 'cos' if which == 'sin' else 'sin'
    e = untan(e)
    us = []
    trigargs(e, us)
    for u in us:
        e = rsquare(e, fn(other, u), fn(which, u))
    return expand(e)
