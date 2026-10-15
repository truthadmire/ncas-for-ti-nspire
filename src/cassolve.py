# cassolve.py - equation / inequality / system solving, ODEs, optimization
from cascore import *
from caspoly import (factor_expr, comdenom, ufactor, u_from_expr, aberth,
                     autocancel, kernels, sortkernels, ratform, p2e, p_gcd,
                     p_deg, p_coeff, p_mul, p_sub, p_divexact, p_isconst,
                     p_vars, p_const, cancel_pair)
from cascalc import (diff, integ, integrate, linear, nice, texpand, limit,
                     nint, pyth)

def unhold(e):
    if isnode(e, 'hold'):
        return simp(e[1])
    return e

def isrealc(e):
    # constant expression with real value
    if not isconst(e):
        return False
    try:
        v = nval(e)
    except Exception:
        return False
    if type(v) is complex:
        return abs(v.imag) <= 1e-10 * (1 + abs(v.real))
    return v == v

def fv(e):
    v = nval(e)
    if type(v) is complex:
        return v.real
    return v

def clean(e):
    # tidy a solution value
    e = autocancel(e)
    if hasfloat(e):
        e = evalf(e)
        if has(e, 'i'):
            r, i = reim(e)
            if type(i) is float and abs(i) < 1e-11 * (1 + abs(tofl(r) if isnum(r) else 1)):
                e = r
    return e

# ===================================================== solving one equation
class Sols:
    # container for solutions of one equation
    def __init__(self):
        self.vals = []
        self.all = False
        self.fail = False
        self.ints = []

def solve_eq(f, x, cplx=False, depth=0):
    # solutions of f = 0 for x: returns list of values or None (unsolved), or 'all'
    if depth > 6:
        return None
    f = autocancel(unhold(f))
    if freeof(f, x):
        if f == 0:
            return 'all'
        if isconst(f) or not cplx:
            return []
        return []
    nu = numer_of(f)
    if freeof(nu, x):
        return [] if nu != 0 else 'all'
    sols = solve_num(nu, x, cplx, depth)
    if sols is None or sols == 'all':
        return sols
    # exclude zeros of the original denominators / undefined points
    out = []
    for s in sols:
        if valid(f, x, s, cplx):
            out.append(s)
    return out

def numer_of(f):
    try:
        c = comdenom(f)
    except Exception:
        c = f
    return numer_denom(c)[0]

def valid(f, x, s, cplx):
    if has(s, 'n1') or symbols(s) and not isconst(s):
        return True
    try:
        v = subs(f, x, s)
        if v == 'undef' or has(v, 'undef'):
            return False
        if has(v, 'inf'):
            return False
        vv = nval(v)
        mag = 1.0
        if type(vv) is complex:
            ok = abs(vv) < 1e-6
        else:
            ok = abs(vv) < 1e-6
        if not ok:
            # relative check
            try:
                sc = nval(s)
                ok = abs(vv) < 1e-8 * (1 + abs(sc)) * 1e4
            except Exception:
                ok = False
        if not cplx:
            sv = nval(s)
            if type(sv) is complex and abs(sv.imag) > 1e-9 * (1 + abs(sv.real)):
                return False
        return ok
    except (CASError, ZeroDivisionError, ValueError, TypeError, OverflowError):
        return False

def solve_num(nu, x, cplx, depth):
    # nu: numerator (no denominators with x)
    d = degree(nu, x)
    if d is not None:
        r = solve_poly(nu, x, cplx)
        if r is not None:
            return r
    # factor into products
    fac = factor_expr(nu)
    fac = fac[1] if isnode(fac, 'hold') else fac
    if isnode(fac, '*'):
        allsol = []
        for g in fac[1:]:
            if isnode(g, '^') and isnum(g[2]) and nsign(g[2]) > 0:
                g = g[1]
            if freeof(g, x):
                continue
            r = solve_eq(g, x, cplx, depth + 1)
            if r is None:
                return numeric_solve(nu, x, cplx)
            if r == 'all':
                return 'all'
            allsol.extend(r)
        return dedup(allsol)
    if isnode(fac, '^') and isnum(fac[2]) and nsign(fac[2]) > 0:
        return solve_eq(fac[1], x, cplx, depth + 1)
    # isolation
    r = isolate(nu, 0, x, cplx, depth)
    if r is not None:
        return r
    # single radical: A + B*u^(1/q) = 0  ->  (-A)^q = B^q * u
    r = radical_solve(nu, x, cplx, depth)
    if r is not None:
        return r
    r = explog_solve(nu, x, cplx, depth)
    if r is not None:
        return r
    r = ln_solve(nu, x, cplx, depth)
    if r is not None:
        return r
    # substitution: single kernel
    r = kernel_solve(nu, x, cplx, depth)
    if r is not None:
        return r
    # trig rewriting
    if hastrigx(nu, x):
        g = texpand(nu)
        if g != nu:
            r = kernel_solve(g, x, cplx, depth + 1)
            if r is None:
                fg = factor_expr(g)
                fg = fg[1] if isnode(fg, 'hold') else fg
                if isnode(fg, '*'):
                    return solve_num(g, x, cplx, depth + 1)
            if r is not None:
                return r
        r = trig_lin(nu, x, cplx)
        if r is not None:
            return r
    return numeric_solve(nu, x, cplx)

def radical_solve(nu, x, cplx, depth):
    ks = []
    xkernels(nu, x, ks)
    if not ks:
        return None
    for k in ks:
        if not (isnode(k, '^') and isq(k[2]) and k[2][1] == 1):
            return None
    if len(ks) > 1:
        if depth > 4 or len(ks) > 3:
            return None
        for k in ks:
            if k[2] != HALF:
                return None
        k = ks[0]
        W = 'W_'
        g = expand(subs(nu, k, W))
        cs_ = coeffs(g, W)
        if cs_ is None or len(cs_) != 2:
            return None
        A, B = cs_
        g2 = expand(sub(pw(A, 2), mul(pw(B, 2), k[1])))
        rs = solve_eq(g2, x, cplx, depth + 1)
        if rs is None or rs == 'all':
            return None
        return [r for r in rs if valid(nu, x, r, cplx)]
    k = ks[0]
    base = k[1]
    q = k[2][2]
    W = 'W_'
    g = expand(subs(nu, k, W))
    cs_ = coeffs(g, W)
    if cs_ is None or len(cs_) != 2 or has(cs_[0], W):
        return None
    A, B = cs_
    if degree(A, x) is None or degree(B, x) is None or degree(base, x) is None:
        return None
    poly = expand(sub(pw(neg(A), q), mul(pw(B, q), base)))
    rs = solve_poly(poly, x, cplx)
    if rs is None or rs == 'all':
        return None
    out = []
    for r in rs:
        if valid(nu, x, r, cplx):
            out.append(r)
    return out

def expterm(t, x):
    # t = c * prod b_i^(L_i) with L_i linear in x; returns (c, sum L_i*ln b_i) or None
    fs = t[1:] if isnode(t, '*') else (t,)
    c = []
    L = []
    for f in fs:
        if freeof(f, x):
            c.append(f)
        elif isnode(f, '^') and freeof(f[1], x) and linear(f[2], x) is not None and isrealc(f[1]) and fv(f[1]) > 0:
            L.append(mul(f[2], fn('ln', f[1])) if f[1] != 'e' else f[2])
        else:
            return None
    return mul_list(c), add_list(L)

def explog_solve(nu, x, cplx, depth):
    # c1*a^(L1) + c2*b^(L2) = 0  ->  take logarithms
    if not isnode(nu, '+'):
        return None
    dep = [t for t in nu[1:] if not freeof(t, x)]
    ind = add_list([t for t in nu[1:] if freeof(t, x)])
    if len(dep) == 2 and ind == 0:
        A = expterm(dep[0], x)
        B = expterm(dep[1], x)
        if A is None or B is None:
            return None
        r = autocancel(neg(div(B[0], A[0])))
        if isrealc(r) and fv(r) <= 0 and not cplx:
            return []
        eq = expand(sub(A[1], add(B[1], fn('ln', r))))
        lx = linear(eq, x)
        if lx is None:
            return None
        return [nice(autocancel(neg(div(lx[1], lx[0]))))]
    return None

def ln_solve(nu, x, cplx, depth):
    # sum of c_i*ln(u_i) + const = 0  ->  prod u_i^c_i = e^(-const)
    terms = nu[1:] if isnode(nu, '+') else (nu,)
    lns = []
    rest = []
    for t in terms:
        c, r = coef_rest(t)
        if isnode(r, 'log') and len(r) == 3:
            c = div(c, fn('ln', r[2]))
            r = ('ln', r[1])
        if isnode(r, 'ln') and israt(c) and not freeof(r, x):
            lns.append((c, r[1]))
        elif freeof(t, x):
            rest.append(t)
        elif isnode(r, 'ln') and isconst(c) and not freeof(r, x):
            lns.append((c, r[1]))
        else:
            return None
    if len(lns) < 2 and not (len(lns) == 1 and rest):
        return None
    k = rest_k = add_list(rest)
    # pull constant multiplier: all c_i equal to c -> ln(prod u_i) = -rest/c
    c0 = lns[0][0]
    if all([c == c0 for c, u in lns]):
        P = mul_list([u for c, u in lns])
        rhs = pw('e', autocancel(neg(div(rest_k, c0))))
    elif all([israt(c) for c, u in lns]):
        P = mul_list([pw(u, c) for c, u in lns])
        rhs = pw('e', neg(rest_k))
    else:
        return None
    rs = solve_eq(sub(P, rhs), x, cplx, depth + 1)
    if rs is None or rs == 'all':
        return rs
    out = []
    for r in rs:
        if valid(nu, x, r, cplx):
            out.append(r)
    return out

def hastrigx(e, x):
    if type(e) is not tuple or e[0] == 'Q':
        return False
    if e[0] in ('sin', 'cos', 'tan') and has(e, x):
        return True
    for a in e[1:]:
        if hastrigx(a, x):
            return True
    return False

def dedup(sols):
    out = []
    for s in sols:
        if s not in out:
            dup = False
            for t in out:
                try:
                    if isconst(s) and isconst(t) and abs(nval(s) - nval(t)) < 1e-12 * (1 + abs(nval(s))):
                        dup = True
                        break
                except Exception:
                    pass
            if not dup:
                out.append(s)
    return out

def sortsols(sols):
    def key(s):
        t = s
        for w in symbols(s):
            if w[0] == 'n' and w[1:].isdigit():
                t = subs(t, w, 0)
        try:
            v = nval(t)
            if type(v) is complex:
                return (1, v.real, v.imag, okey(s))
            return (0, v, 0.0, okey(s))
        except Exception:
            return (2, 0.0, 0.0, okey(s))
    return sorted(sols, key=key)

# ----------------------------------------------------- polynomials
def solve_poly(p, x, cplx):
    cs = coeffs(p, x)
    if cs is None:
        return None
    while cs and cs[-1] == 0:
        cs.pop()
    n = len(cs) - 1
    if n <= 0:
        return [] if cs and cs[0] != 0 else 'all'
    # x^k factor
    sols = []
    k = 0
    while cs[k] == 0:
        k += 1
    if k:
        sols.append(0)
        cs = cs[k:]
        n = len(cs) - 1
    if n == 0:
        return sols
    allrat = True
    anyfl = False
    for c in cs:
        if not israt(c):
            allrat = False
        if hasfloat(c):
            anyfl = True
    if anyfl and all([isconst(c) for c in cs]):
        return sols + numroots(cs, cplx)
    if allrat:
        cc, fs = ufactor(cs)
        for g, m in fs:
            sols.extend(solve_small(g, x, cplx))
        return dedup(sols)
    if n == 1:
        return sols + [autocancel(neg(div(cs[0], cs[1])))]
    if n == 2:
        return sols + quad(cs[2], cs[1], cs[0], cplx)
    # try factoring
    fac = factor_expr(p, x)
    fac = fac[1] if isnode(fac, 'hold') else fac
    if isnode(fac, '*'):
        for g in fac[1:]:
            if isnode(g, '^') and isnum(g[2]):
                g = g[1]
            if freeof(g, x):
                continue
            dg = degree(g, x)
            if dg is not None and dg < n:
                r = solve_poly(g, x, cplx)
                if r is None:
                    return None
                sols.extend(r)
            else:
                return None
        return dedup(sols)
    # binomial / power substitution
    r = solve_binom(cs, x, cplx)
    if r is not None:
        return sols + r
    if all([isconst(c) for c in cs]):
        return sols + numroots(cs, cplx)
    return None

def quad(a, b, c, cplx):
    D = autocancel(expand(sub(mul(b, b), mul(4, a, c))))
    if isrealc(D) and not cplx:
        if fv(D) < 0:
            return []
    if D == 0:
        return [autocancel(div(neg(b), mul(2, a)))]
    s = sqrt(D)
    r1 = autocancel(div(sub(neg(b), s), mul(2, a)))
    r2 = autocancel(div(add(neg(b), s), mul(2, a)))
    if isconst(r1):
        r1 = expand(r1)
        r2 = expand(r2)
    return [r1, r2]

def solve_small(g, x, cplx):
    # g integer coefficient list, irreducible over Q
    n = len(g) - 1
    if n == 1:
        return [Q(-g[0], g[1])]
    if n == 2:
        return quad(g[2], g[1], g[0], cplx)
    r = solve_binom(g, x, cplx)
    if r is not None:
        return r
    if n == 3:
        r = cardano(g, cplx)
        if r is not None:
            from casout import fmt
            if len(fmt(r[0])) <= 32:
                return r
    return numroots(g, cplx)

def solve_binom(cs, x, cplx):
    # polynomial in x^m
    n = len(cs) - 1
    m = 0
    for i in range(1, n + 1):
        if cs[i] != 0:
            m = igcd(m, i)
    if m <= 1:
        return None
    sub_cs = [cs[i] for i in range(0, n + 1, m)]
    if len(sub_cs) - 1 > 2 and not (len([c for c in sub_cs if c != 0]) == 2):
        return None
    u = 'U_'
    if len(sub_cs) == 2:
        roots_u = [autocancel(neg(div(sub_cs[0], sub_cs[1])))]
    else:
        roots_u = solve_poly(fromcoeffs(sub_cs, u), u, cplx)
        if roots_u is None:
            return None
    out = []
    for r in roots_u:
        out.extend(nthroots(r, m, cplx))
    return dedup(out)

def nthroots(r, m, cplx):
    # solutions of x^m = r
    if not cplx:
        if isrealc(r):
            v = fv(r)
            if m % 2 == 1:
                if v < 0:
                    return [neg(pw(neg(r), Q(1, m)))]
                return [pw(r, Q(1, m))]
            if v < 0:
                return []
            if v == 0:
                return [0]
            rt = pw(r, Q(1, m))
            return [neg(rt), rt]
        if m % 2 == 1:
            return [pw(r, Q(1, m))]
        rt = pw(r, Q(1, m))
        return [neg(rt), rt]
    # complex: all m roots
    if isconst(r):
        v = nval(r)
        mod = fn('abs', r)
        ang = fn('angle', r)
        out = []
        for k in range(m):
            th = div(add(ang, mul(2 * k, 'pi')), m)
            z = mul(pw(mod, Q(1, m)), add(fn('cos', th), mul('i', fn('sin', th))))
            z = expand(z)
            out.append(z)
        return out
    rt = pw(r, Q(1, m))
    return [mul(rt, pw('e', div(mul(2 * k, 'i', 'pi'), m))) for k in range(m)]

def cardano(g, cplx):
    # depressed cubic with one real root (discriminant < 0) -> exact real root
    d, c, b, a = [Q(v) if type(v) is int else v for v in g]
    p = div(sub(mul(3, a, c), mul(b, b)), mul(3, a, a))
    q = div(add(mul(2, pw(b, 3)), mul(-9, a, b, c), mul(27, a, a, d)), mul(27, pw(a, 3)))
    disc = add(div(pw(q, 2), 4), div(pw(p, 3), 27))
    if not israt(disc) or nsign(disc) <= 0:
        return None
    s = sqrt(disc)
    u = add(neg(div(q, 2)), s)
    v = sub(neg(div(q, 2)), s)
    def cbrt(w):
        wv = fv(w)
        if wv < 0:
            return neg(pw(neg(w), Q(1, 3)))
        return pw(w, Q(1, 3))
    t = add(cbrt(u), cbrt(v))
    root = sub(t, div(b, mul(3, a)))
    if not cplx:
        return [root]
    return [root] + [clean(r) for r in numroots_after(g, root)]

def numroots_after(g, root):
    rv = fv(root)
    rs = aberth(g)
    return [fromcomplex(z) for z in rs if abs(z - rv) > 1e-6]

def numroots(cs, cplx):
    rs = aberth([evalf(c) if not isnum(c) else c for c in cs])
    out = []
    for z in rs:
        if abs(z.imag) < 1e-9 * (1 + abs(z.real)):
            out.append(float(z.real))
        elif cplx:
            out.append(fromcomplex(z))
    return out

# ----------------------------------------------------- isolation
NC = [0]

def newint():
    NC[0] += 1
    return 'n' + str(NC[0])

def isolate(lhs, rhs, x, cplx, depth):
    # solve lhs = rhs where rhs free of x; returns list or None
    if depth > 12:
        return None
    if lhs == x:
        return [rhs]
    if freeof(lhs, x):
        return 'all' if autocancel(sub(lhs, rhs)) == 0 else []
    h = head(lhs)
    if h == '+':
        dep = [t for t in lhs[1:] if not freeof(t, x)]
        ind = [t for t in lhs[1:] if freeof(t, x)]
        if len(dep) == 1:
            return isolate(dep[0], sub(rhs, add_list(ind)), x, cplx, depth + 1)
        return None
    if h == '*':
        dep = [t for t in lhs[1:] if not freeof(t, x)]
        ind = [t for t in lhs[1:] if freeof(t, x)]
        if len(dep) == 1:
            c = mul_list(ind)
            r = div(rhs, c)
            if isconst(c) and isnode(rhs, '+'):
                r = expand(r)
            return isolate(dep[0], r, x, cplx, depth + 1)
        return None
    if h == '^':
        b, p = lhs[1], lhs[2]
        if freeof(p, x):
            if p == -1 or (isnum(p) and nsign(p) < 0):
                if rhs == 0:
                    return []
                return isolate(pw(b, nneg(p)), pw(rhs, -1), x, cplx, depth + 1)
            if type(p) is int:
                out = []
                for r in nthroots(rhs, p, cplx):
                    rr = isolate(b, r, x, cplx, depth + 1)
                    if rr is None:
                        return None
                    if rr == 'all':
                        return 'all'
                    out.extend(rr)
                return out
            if isq(p):
                pn, pd = p[1], p[2]
                if pd % 2 == 0 and not cplx and isrealc(rhs) and fv(rhs) < 0:
                    return []
                # b^(pn/pd) = r  ->  b^pn = r^pd
                return isolate(pw(b, pn), pw(rhs, pd), x, cplx, depth + 1)
            return isolate(b, pw(rhs, pw(p, -1)), x, cplx, depth + 1)
        if freeof(b, x):
            if rhs == 0:
                return []
            if not cplx and isrealc(rhs) and fv(rhs) < 0 and isrealc(b) and fv(b) > 0:
                return []
            if b == 'e':
                return isolate(p, fn('ln', rhs), x, cplx, depth + 1)
            if isnum(b) and isconst(rhs):
                return isolate(p, fn('log', rhs, b), x, cplx, depth + 1)
            return isolate(p, div(fn('ln', rhs), fn('ln', b)), x, cplx, depth + 1)
        return None
    if type(lhs) is tuple and len(lhs) >= 2:
        u = lhs[1]
        if not all([freeof(a, x) for a in lhs[2:]]):
            return None
        rs = invfun(h, lhs, rhs, cplx)
        if rs is None:
            return None
        out = []
        for r in rs:
            rr = isolate(u, r, x, cplx, depth + 1)
            if rr is None:
                return None
            if rr == 'all':
                return 'all'
            out.extend(rr)
        return out
    return None

def invfun(h, lhs, r, cplx):
    rv = None
    if isrealc(r):
        rv = fv(r)
    if h == 'ln':
        return [pw('e', r)]
    if h == 'log':
        b = lhs[2] if len(lhs) > 2 else 10
        return [pw(b, r)]
    if h == 'abs':
        if rv is not None:
            if rv < 0:
                return []
            if rv == 0:
                return [0]
        return [neg(r), r]
    if h == 'sqrt':
        return [pw(r, 2)]
    if h == 'sin':
        if rv is not None and abs(rv) > 1 and not cplx:
            return []
        n = newint()
        if r == 0:
            return [mul(n, 'pi')]
        a = fn('arcsin', r)
        if r == 1 or r == -1:
            return [add(a, mul(2, n, 'pi'))]
        return [add(a, mul(2, n, 'pi')), add(sub('pi', a), mul(2, n, 'pi'))]
    if h == 'cos':
        if rv is not None and abs(rv) > 1 and not cplx:
            return []
        n = newint()
        if r == 0:
            return [add(mul(HALF, 'pi'), mul(n, 'pi'))]
        a = fn('arccos', r)
        if r == 1 or r == -1:
            return [add(a, mul(2, n, 'pi'))]
        return [add(a, mul(2, n, 'pi')), add(neg(a), mul(2, n, 'pi'))]
    if h == 'tan':
        n = newint()
        return [add(fn('arctan', r), mul(n, 'pi'))]
    if h == 'arcsin':
        if rv is not None and abs(rv) > math.pi / 2 + 1e-12:
            return []
        return [fn('sin', r)]
    if h == 'arccos':
        if rv is not None and (rv < -1e-12 or rv > math.pi + 1e-12):
            return []
        return [fn('cos', r)]
    if h == 'arctan':
        if rv is not None and abs(rv) >= math.pi / 2:
            return []
        return [fn('tan', r)]
    if h == 'sinh':
        return [fn('arcsinh', r)]
    if h == 'cosh':
        if rv is not None and rv < 1:
            return []
        a = fn('arccosh', r)
        return [neg(a), a]
    if h == 'tanh':
        if rv is not None and abs(rv) >= 1:
            return []
        return [fn('arctanh', r)]
    if h == 'arcsinh':
        return [fn('sinh', r)]
    if h == 'arccosh':
        return [fn('cosh', r)]
    if h == 'arctanh':
        return [fn('tanh', r)]
    return None

# ----------------------------------------------------- kernel substitution
def xkernels(e, x, out):
    if type(e) is not tuple or e[0] == 'Q' or freeof(e, x):
        return
    h = e[0]
    if h in ('+', '*'):
        for a in e[1:]:
            xkernels(a, x, out)
        return
    if h == '^' and type(e[2]) is int:
        xkernels(e[1], x, out)
        return
    if h == '^' and isq(e[2]) and e[1] == x:
        k = pw(x, Q(1, e[2][2]))
        if k not in out:
            out.append(k)
        return
    if e not in out:
        out.append(e)

def kernel_solve(nu, x, cplx, depth):
    W = 'W_'
    g = nu
    # exponentials with linear exponents -> powers of W
    exps = []
    findexp(g, x, exps)
    if exps:
        base = exps[0][0]
        if all([b == base for b, a, c in exps]):
            gg = 0
            for b, a, c in exps:
                gg = a if gg == 0 else rgcd(gg, a)
            if gg != 0:
                g2 = repl_exp(g, x, base, gg, W)
                if freeof(g2, x):
                    rs = solve_eq(g2, W, cplx, depth + 1)
                    if rs is None or rs == 'all':
                        return rs
                    out = []
                    for r in rs:
                        rr = isolate(pw(base, mul(gg, x)), r, x, cplx, depth + 1)
                        if rr is None:
                            return None
                        out.extend(rr)
                    return out
    ks = []
    xkernels(g, x, ks)
    if len(ks) == 1 and ks[0] != x:
        k = ks[0]
        g2 = subs(g, k, W)
        if freeof(g2, x):
            rs = solve_eq(g2, W, cplx, depth + 1)
            if rs is None or rs == 'all':
                return rs
            out = []
            for r in rs:
                rr = isolate(k, r, x, cplx, depth + 1)
                if rr is None:
                    return None
                if rr == 'all':
                    return 'all'
                out.extend(rr)
            return out
    # sin/cos with even powers of one of them
    if len(ks) == 2:
        names = sorted([head(k) for k in ks])
        if names == ['cos', 'sin'] and ks[0][1] == ks[1][1]:
            u = ks[0][1]
            s = fn('sin', u)
            c = fn('cos', u)
            for a, b in ((c, s), (s, c)):
                g2 = expand(g)
                cc = coeffs(subs(g2, a, W), W)
                if cc is not None and all([cc[i] == 0 for i in range(1, len(cc), 2)]):
                    g3 = expand(subs(subs(g2, a, W), W, sqrt(sub(1, pw(b, 2)))))
                    if not has(g3, a):
                        return kernel_solve(g3, x, cplx, depth + 1) if depth < 4 else None
    return None

def rgcd(a, b):
    if israt(a) and israt(b):
        an, ad = nd(a)
        bn, bd = nd(b)
        return Q(igcd(an, bn), ilcm(ad, bd))
    return a if a == b else 0

def findexp(e, x, out):
    if type(e) is not tuple or e[0] == 'Q':
        return
    if e[0] == '^' and freeof(e[1], x) and not freeof(e[2], x):
        l = linear(e[2], x)
        if l is not None:
            out.append((e[1], l[0], l[1]))
            return
        out.append((None, 0, 0))
        return
    for a in e[1:]:
        findexp(a, x, out)

def repl_exp(e, x, base, gg, W):
    if type(e) is not tuple or e[0] == 'Q':
        return e
    if e[0] == '^' and e[1] == base and not freeof(e[2], x):
        l = linear(e[2], x)
        if l is not None:
            return mul(pw(base, l[1]), pw(W, div(l[0], gg)))
    return simp((e[0],) + tuple(repl_exp(a, x, base, gg, W) for a in e[1:]))

def trig_lin(nu, x, cplx):
    # a*sin(u) + b*cos(u) + c = 0
    ks = []
    xkernels(nu, x, ks)
    if len(ks) != 2:
        return None
    names = sorted([head(k) for k in ks])
    if names != ['cos', 'sin'] or ks[0][1] != ks[1][1]:
        return None
    u = ks[0][1]
    S = 'S_'
    C = 'C_'
    g = expand(subs(subs(nu, fn('sin', u), S), fn('cos', u), C))
    if has(g, x):
        return None
    cs_s = coeffs(g, S)
    if cs_s is None or len(cs_s) != 2:
        return None
    a = cs_s[1]
    rest = cs_s[0]
    cc = coeffs(rest, C)
    if cc is None or len(cc) != 2 or has(a, C):
        return None
    b = cc[1]
    c = cc[0]
    if c == 0:
        return isolate(fn('tan', u), autocancel(neg(div(b, a))), x, cplx, 0)
    R = sqrt(add(pw(a, 2), pw(b, 2)))
    phi = fn('arctan', div(b, a))
    if isrealc(a) and fv(a) < 0:
        phi = add(phi, 'pi')
    return isolate(fn('sin', add(u, phi)), autocancel(neg(div(c, R))), x, cplx, 0)

# ----------------------------------------------------- numeric
def numeric_solve(f, x, cplx, lo=None, hi=None, maxn=12):
    others = [s for s in symbols(f) if s != x]
    if others:
        return None
    def F(t):
        try:
            v = nval(f, {x: t})
        except (ZeroDivisionError, ValueError, OverflowError, CASError, TypeError):
            return None
        if type(v) is complex:
            if abs(v.imag) > 1e-9 * (1 + abs(v.real)):
                return None
            v = v.real
        if v != v:
            return None
        return v
    pts = []
    if lo is not None and hi is not None:
        N = 400
        for i in range(N + 1):
            pts.append(lo + (hi - lo) * i / N)
    else:
        for i in range(-400, 401):
            pts.append(i * 0.05)
        for k in range(-40, 61):
            v = 10 ** (k / 10.0)
            if v > 20:
                pts.append(v)
                pts.append(-v)
        pts.sort()
    roots = []
    prev = None
    pv = None
    vals0 = [F(t) for t in pts]
    for k in range(len(pts)):
        t = pts[k]
        v = vals0[k]
        if v is not None and v == 0:
            a = vals0[k - 1] if k > 0 else None
            b = vals0[k + 1] if k + 1 < len(pts) else None
            if (a is not None and a != 0) or (b is not None and b != 0):
                roots.append(t)
        elif v is not None and pv is not None and v != 0 and pv != 0 and (v < 0) != (pv < 0):
            r = bisect(F, prev, t, pv, v)
            if r is not None:
                roots.append(r)
        prev = t
        pv = v
        if len(roots) > 40:
            break
    # local minima of |f| touching zero
    vals = [(pts[k], vals0[k]) for k in range(len(pts))]
    for i in range(1, len(vals) - 1):
        t0, a = vals[i - 1]
        t1, b = vals[i]
        t2, c = vals[i + 1]
        if a is None or b is None or c is None:
            continue
        if b != 0 and abs(b) < abs(a) and abs(b) < abs(c) and (a > 0) == (b > 0) == (c > 0) and abs(b) < 1e-2:
            r = newton(F, t1)
            if r is not None and t0 <= r <= t2:
                roots.append(r)
    out = []
    for r in sorted(roots):
        if not out or abs(r - out[-1]) > 1e-9 * (1 + abs(r)):
            out.append(r)
    if len(out) > maxn and lo is None:
        out = out[:maxn]
    return [snap(r) for r in out]

def snap(r):
    if abs(r - round(r)) < 1e-12:
        return float(round(r))
    return r

def bisect(F, a, b, fa, fb):
    for _ in range(200):
        m = 0.5 * (a + b)
        fm = F(m)
        if fm is None:
            return None
        if fm == 0 or abs(b - a) < 1e-15 * (1 + abs(m)):
            break
        if (fm < 0) == (fa < 0):
            a, fa = m, fm
        else:
            b, fb = m, fm
    m = 0.5 * (a + b)
    fm = F(m)
    if fm is None or abs(fm) > 1e-6 * (1 + abs(fa) + abs(fb)):
        # sign change across a pole
        if fm is not None and abs(fm) > 1e3:
            return None
    return m

def newton(F, t):
    for _ in range(60):
        v = F(t)
        if v is None:
            return None
        h = 1e-7 * (1 + abs(t))
        v2 = F(t + h)
        if v2 is None:
            return None
        d = (v2 - v) / h
        if d == 0:
            break
        t2 = t - v / d
        if abs(t2 - t) < 1e-14 * (1 + abs(t)):
            t = t2
            break
        t = t2
    v = F(t)
    if v is not None and abs(v) < 1e-9:
        return t
    return None

def nsolve(f, x, guess=None, lo=None, hi=None):
    def F(t):
        try:
            v = nval(f, {x: t})
        except (ZeroDivisionError, ValueError, OverflowError, CASError, TypeError):
            return None
        if type(v) is complex:
            if abs(v.imag) > 1e-9 * (1 + abs(v.real)):
                return None
            v = v.real
        return v
    if guess is not None:
        r = secant(F, guess, lo, hi)
        if r is not None:
            return r
    if lo is not None and hi is not None:
        rs = numeric_solve(f, x, False, lo, hi)
    else:
        rs = numeric_solve(f, x, False)
        if lo is not None:
            rs = [r for r in rs if r >= lo]
        if hi is not None:
            rs = [r for r in rs if r <= hi]
    if rs:
        if guess is not None:
            rs.sort(key=lambda r: abs(r - guess))
        else:
            rs.sort(key=lambda r: abs(r))
        return rs[0]
    return None

def secant(F, g, lo, hi):
    t = g
    r = newton(F, t)
    if r is not None and (lo is None or r >= lo) and (hi is None or r <= hi):
        return r
    return None

# ===================================================== inequalities
FLIP = {'<': '>', '>': '<', '<=': '>=', '>=': '<=', '/=': '/='}

def solve_ineq(rel, f, x):
    # f rel 0, returns boolean expression or None
    f = autocancel(f)
    if not isconst(subs(f, x, 0)) or not isconst(diff(f, x)):
        r = ineq_param(rel, f, x)
        if r is not None:
            return r
    pts = []
    rs = solve_eq(f, x, False)
    if rs is None:
        return None
    if rs == 'all':
        rs = []
    for r in rs:
        if not isrealc(r):
            return None
        pts.append(r)
    dens = []
    domainpts(f, x, dens)
    for d in dens:
        r2 = solve_eq(d, x, False)
        if r2 is None or r2 == 'all':
            continue
        for r in r2:
            if isrealc(r):
                pts.append(r)
            else:
                return None
    pts = dedup(pts)
    pts = sortsols(pts)
    def test(t):
        try:
            v = nval(f, {x: t})
        except Exception:
            return False
        if type(v) is complex:
            if abs(v.imag) > 1e-9 * (1 + abs(v.real)):
                return False
            v = v.real
        if v != v:
            return False
        return relok(rel, v)
    vals = [fv(p) for p in pts]
    segs = []
    if not vals:
        ok = test(0.5)
        return 'true' if ok else 'false'
    first = vals[0] - max(1.0, abs(vals[0]))
    segs.append(('I', None, pts[0], test(first)))
    for i in range(len(pts)):
        p = pts[i]
        okp = False
        try:
            v = subs(f, x, p)
            if v != 'undef' and not has(v, 'undef') and not has(v, 'inf'):
                vv = nval(v)
                if type(vv) is complex:
                    vv = vv.real if abs(vv.imag) < 1e-9 else None
                if vv is not None:
                    if abs(vv) < 1e-10:
                        vv = 0.0
                    okp = relok(rel, vv)
        except Exception:
            okp = False
        segs.append(('P', p, p, okp))
        if i + 1 < len(pts):
            m = 0.5 * (vals[i] + vals[i + 1])
            segs.append(('I', p, pts[i + 1], test(m)))
    last = vals[-1] + max(1.0, abs(vals[-1]))
    segs.append(('I', pts[-1], None, test(last)))
    return segs_to_bool(segs, x)

def sgn(e):
    # 1 or -1 when e is provably positive or negative for real variables,
    # else 0
    if isconst(e):
        try:
            v = fv(e)
        except Exception:
            return 0
        return 1 if v > 0 else (-1 if v < 0 else 0)
    if isnode(e, '*'):
        s = 1
        for a in e[1:]:
            k = sgn(a)
            if not k:
                return 0
            s *= k
        return s
    if isnode(e, '+'):
        ks = [sgn(a) or (2 if nonneg(a) else 0) for a in e[1:]]
        if all(k in (1, 2) for k in ks) and 1 in ks:
            return 1
        ks = [sgn(neg(a)) or (2 if nonneg(neg(a)) else 0) for a in e[1:]]
        if all(k in (1, 2) for k in ks) and 1 in ks:
            return -1
        return 0
    if isnode(e, '^') and isint(e[2]) and e[2] % 2 == 1:
        return sgn(e[1])
    if head(e) == 'exp' or (isnode(e, '^') and e[1] == 'e'):
        return 1
    return 0

def nonneg(e):
    # e >= 0 for all real values of its variables
    if isnode(e, '^') and isint(e[2]) and e[2] % 2 == 0:
        return True
    if head(e) == 'abs':
        return True
    if isnode(e, '*'):
        return all(nonneg(a) or sgn(a) > 0 for a in e[1:])
    return sgn(e) > 0

def ineq_param(rel, f, x):
    # a*x+b rel 0 where a and b hold other variables: answer by the sign
    # of a, e.g. a*x<5 -> (x<5/a and a>0) or (x>5/a and a<0) or a=0
    cs = coeffs(f, x)
    if cs is None or len(cs) != 2:
        return None
    a = nice(comdenom(cs[1]))
    b = cs[0]
    v = nice(comdenom(div(neg(b), a)))
    k = sgn(a)
    if k:
        return (rel if k > 0 else FLIP[rel], x, v)
    n = numer_denom(a)[0]
    if rel == '/=':
        out = [('and', ('/=', x, v), ('/=', n, 0))]
    else:
        out = [('and', (rel, x, v), ('>', a, 0)),
               ('and', (FLIP[rel], x, v), ('<', a, 0))]
    # a = 0: the inequality is b rel 0
    if type(n) is str:
        b = subs(b, n, 0)
    if isconst(b):
        if relok(rel, fv(b)):
            out.append(('=', n, 0))
    else:
        out.append(('and', ('=', n, 0), (rel, b, 0)))
    return ('or',) + tuple(out) if len(out) > 1 else out[0]

def relok(rel, v):
    if rel == '<':
        return v < 0
    if rel == '>':
        return v > 0
    if rel == '<=':
        return v <= 0
    if rel == '>=':
        return v >= 0
    if rel == '/=':
        return v != 0
    return v == 0

def domainpts(f, x, out):
    if type(f) is not tuple or f[0] == 'Q':
        return
    h = f[0]
    if h == '^' and not freeof(f[1], x):
        if isnum(f[2]) and nsign(f[2]) < 0:
            out.append(f[1])
        if isq(f[2]) and f[2][2] % 2 == 0:
            out.append(f[1])
    if h in ('ln', 'log', 'abs', 'sign', 'floor', 'ceiling') and not freeof(f[1], x):
        out.append(f[1])
    for a in f[1:]:
        domainpts(a, x, out)

def segs_to_bool(segs, x):
    # merge consecutive true segments into intervals
    ivs = []
    cur = None
    for kind, a, b, ok in segs:
        if ok:
            if cur is None:
                if kind == 'I':
                    cur = [a, False, b, False]
                else:
                    cur = [a, True, b, True]
            else:
                cur[2] = b
                cur[3] = (kind == 'P')
        else:
            if cur is not None:
                ivs.append(cur)
                cur = None
    if cur is not None:
        ivs.append(cur)
    if not ivs:
        return 'false'
    # x /= p pattern
    if len(ivs) >= 2 and ivs[0][0] is None and ivs[-1][2] is None:
        okp = True
        for i in range(len(ivs) - 1):
            if not (ivs[i][2] == ivs[i + 1][0] and not ivs[i][3] and not ivs[i + 1][1]):
                okp = False
        if okp:
            ne = [('/=', x, ivs[i][2]) for i in range(len(ivs) - 1)]
            return ne[0] if len(ne) == 1 else ('and',) + tuple(ne)
    out = []
    for lo, li, hi, hiinc in ivs:
        if lo is None and hi is None:
            return 'true'
        if lo is not None and hi is not None and lo == hi:
            out.append(('=', x, lo))
        elif lo is None:
            out.append(('<=' if hiinc else '<', x, hi))
        elif hi is None:
            out.append(('>=' if li else '>', x, lo))
        else:
            out.append(('and', ('<=' if li else '<', lo, x), ('<=' if hiinc else '<', x, hi)))
    if len(out) == 1:
        return out[0]
    return ('or',) + tuple(out)

# ===================================================== systems
def eqexpr(eq):
    if isnode(eq, '='):
        return autocancel(sub(eq[1], eq[2]))
    return eq

def is_linear_sys(fs, vs):
    for f in fs:
        for v in vs:
            d = degree(f, v)
            if d is None or d > 1:
                return False
        g = expand(f)
        for i in range(len(vs)):
            for j in range(len(vs)):
                cs_ = coeffs(g, vs[i])
                if cs_ is None:
                    return False
                if len(cs_) > 1 and has(cs_[1], vs[j]):
                    return False
    return True

def linsys(fs, vs):
    # Gauss-Jordan on augmented matrix; returns list of dicts or [] or 'inf'
    m = len(fs)
    n = len(vs)
    A = []
    for f in fs:
        g = expand(f)
        row = []
        rest = g
        for v in vs:
            cs_ = coeffs(g, v)
            c = cs_[1] if len(cs_) > 1 else 0
            row.append(c)
        const = g
        for v in vs:
            const = subs(const, v, 0)
        row.append(neg(const))
        A.append(row)
    piv = []
    r = 0
    for c in range(n):
        p = None
        for i in range(r, m):
            if autocancel(A[i][c]) != 0:
                p = i
                break
        if p is None:
            continue
        A[r], A[p] = A[p], A[r]
        pv = A[r][c]
        A[r] = [autocancel(div(a, pv)) for a in A[r]]
        for i in range(m):
            if i != r and A[i][c] != 0:
                fct = A[i][c]
                A[i] = [autocancel(expand(sub(A[i][j], mul(fct, A[r][j])))) for j in range(n + 1)]
        piv.append(c)
        r += 1
        if r == m:
            break
    for i in range(r, m):
        if autocancel(A[i][n]) != 0:
            return []
    sol = {}
    free = [c for c in range(n) if c not in piv]
    params = {}
    k = 1
    for c in free:
        params[vs[c]] = 'c' + str(k)
        k += 1
    for i in range(len(piv)):
        c = piv[i]
        val = A[i][n]
        for c2 in free:
            val = sub(val, mul(A[i][c2], params[vs[c2]]))
        sol[vs[c]] = nice(autocancel(val))
    for c in free:
        sol[vs[c]] = params[vs[c]]
    return [sol]

def solve_system(eqs, vs, cplx=False, guesses=None):
    NC[0] = 0
    fs = []
    for e in eqs:
        f = eqexpr(e)
        f = numer_of(f) if hasdenom_x(f, vs) else f
        if f != 0:
            fs.append(f)
    if guesses:
        return newton_sys(fs, vs, guesses)
    if is_linear_sys(fs, vs):
        return linsys(fs, vs)
    r = elim(fs, vs, cplx, 0)
    if r is None:
        return newton_sys(fs, vs, [0.0] * len(vs))
    out = []
    for s in r:
        ok = True
        for v in vs:
            if v not in s:
                s[v] = v
        if not cplx:
            for v in vs:
                if isconst(s[v]) and not isrealc(s[v]):
                    ok = False
        if ok and s not in out:
            out.append(s)
    return out

def hasdenom_x(f, vs):
    for v in vs:
        nu, de = numer_denom(f)
        if has(de, v):
            return True
    return False

def elim(fs, vs, cplx, depth):
    # recursive elimination; returns list of dicts or None
    fs = [autocancel(expand(f)) for f in fs]
    fs = [f for f in fs if f != 0]
    if not fs:
        return [{}]
    for f in fs:
        if freeofall(f, vs):
            if isconst(f) or f != 0:
                return []
    if depth > 8:
        return None
    # equation with one unknown
    best = None
    for f in fs:
        inv = [v for v in vs if has(f, v)]
        if len(inv) == 1:
            best = (f, inv[0])
            break
    if best is None:
        # linear in some variable with constant coefficient
        for f in fs:
            for v in vs:
                d = degree(f, v)
                if d == 1:
                    c = coeffs(f, v)
                    if c is not None and isconst(c[1]) and c[1] != 0:
                        best = (f, v)
                        break
            if best:
                break
    if best is None:
        for f in fs:
            for v in vs:
                if degree(f, v) == 1:
                    best = (f, v)
                    break
            if best:
                break
    if best is not None:
        f, v = best
        rs = solve_eq(f, v, cplx)
        if rs is None:
            return None
        if rs == 'all':
            rs = []
        out = []
        rest = [g for g in fs if g is not f]
        ovs = [w for w in vs if w != v]
        for r in rs:
            sub_ = [autocancel(subs(g, v, r)) for g in rest]
            rr = elim(sub_, ovs, cplx, depth + 1)
            if rr is None:
                return None
            for s in rr:
                s2 = dict(s)
                val = r
                for w in s2:
                    val = subs(val, w, s2[w])
                s2[v] = clean(val)
                out.append(s2)
        return out
    # resultant elimination of the last variable between first two polys
    if len(fs) >= 2 and len(vs) >= 2:
        y = vs[-1]
        R = resultant(fs[0], fs[1], y)
        if R is None or R == 0:
            return None
        rr = elim([R] + fs[2:], vs[:-1], cplx, depth + 1)
        if rr is None:
            return None
        out = []
        for s in rr:
            gs = []
            for g in fs:
                h = g
                for w in s:
                    h = subs(h, w, s[w])
                gs.append(autocancel(expand(h)))
            ys = elim(gs, [y], cplx, depth + 1)
            if ys is None:
                continue
            for t in ys:
                s2 = dict(s)
                s2.update(t)
                out.append(s2)
        return out
    return None

def resultant(f, g, y):
    a = coeffs(f, y)
    b = coeffs(g, y)
    if a is None or b is None:
        return None
    m = len(a) - 1
    n = len(b) - 1
    if m < 1 or n < 1:
        return None
    N = m + n
    M = []
    for i in range(n):
        row = [0] * N
        for j in range(m + 1):
            row[i + j] = a[m - j]
        M.append(row)
    for i in range(m):
        row = [0] * N
        for j in range(n + 1):
            row[i + j] = b[n - j]
        M.append(row)
    return expand(bareiss(M))

def bareiss(M):
    n = len(M)
    M = [list(r) for r in M]
    sign = 1
    prev = 1
    for k in range(n - 1):
        if M[k][k] == 0:
            sw = None
            for i in range(k + 1, n):
                if M[i][k] != 0:
                    sw = i
                    break
            if sw is None:
                return 0
            M[k], M[sw] = M[sw], M[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                num = expand(sub(mul(M[i][j], M[k][k]), mul(M[i][k], M[k][j])))
                M[i][j] = exdiv(num, prev)
        prev = M[k][k]
    return mul(sign, M[n - 1][n - 1])

def exdiv(a, b):
    if b == 1:
        return a
    if isnum(b):
        return expand(mul(a, ninv(b)) if israt(b) else div(a, b))
    ks = []
    kernels(a, ks)
    kernels(b, ks)
    sortkernels(ks)
    ra = ratform(a, ks)
    rb = ratform(b, ks)
    if ra is None or rb is None:
        return autocancel(div(a, b))
    q = p_divexact(p_mul(ra[0], rb[1]), p_mul(ra[1], rb[0]))
    if q is None:
        return autocancel(div(a, b))
    return p2e(q, ks)

def newton_sys(fs, vs, guess):
    n = len(vs)
    if len(fs) != n:
        return None
    others = []
    for f in fs:
        for s in symbols(f):
            if s not in vs:
                return None
    J = [[diff(f, v) for v in vs] for f in fs]
    xv = [float(nval(g).real) if isnum(g) or isconst(g) else 0.0 for g in guess]
    for it in range(100):
        env = dict(zip(vs, xv))
        try:
            F = [nval(f, env) for f in fs]
            Jv = [[nval(J[i][j], env) for j in range(n)] for i in range(n)]
        except Exception:
            return None
        F = [v.real if type(v) is complex else v for v in F]
        Jv = [[v.real if type(v) is complex else v for v in r] for r in Jv]
        dx = linsolve_float(Jv, [-v for v in F])
        if dx is None:
            return None
        xv = [xv[i] + dx[i] for i in range(n)]
        if max([abs(d) for d in dx]) < 1e-13 * (1 + max([abs(v) for v in xv])):
            break
    env = dict(zip(vs, xv))
    try:
        if max([abs(nval(f, env)) for f in fs]) > 1e-8:
            return []
    except Exception:
        return []
    return [dict([(vs[i], snap(xv[i])) for i in range(n)])]

def linsolve_float(A, b):
    n = len(A)
    M = [list(A[i]) + [b[i]] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda i: abs(M[i][c]))
        if abs(M[p][c]) < 1e-300:
            return None
        M[c], M[p] = M[p], M[c]
        for i in range(n):
            if i != c:
                f = M[i][c] / M[c][c]
                for j in range(c, n + 1):
                    M[i][j] -= f * M[c][j]
    return [M[i][n] / M[i][i] for i in range(n)]

# ===================================================== output helpers
def sols_to_bool(x, sols):
    if sols == 'all':
        return 'true'
    if sols is None:
        return None
    if not sols:
        return 'false'
    eqs = [('=', x, s) for s in sols]
    if len(eqs) == 1:
        return eqs[0]
    return ('or',) + tuple(eqs)

def apply_constraints(sols, x, cons):
    # filter solutions using constraints like x>0, 0<=x<=2pi
    if not cons or sols == 'all' or sols is None:
        return sols
    lo = None
    hi = None
    out = []
    expanded = []
    for s in sols:
        ns = [w for w in symbols(s) if w[0] == 'n' and w[1:].isdigit()]
        if ns and len(ns) == 1:
            b = bounds(cons, x)
            if b is None:
                expanded.append(s)
                continue
            n = ns[0]
            for k in range(-60, 61):
                v = subs(s, n, k)
                expanded.append(v)
        else:
            expanded.append(s)
    for s in expanded:
        if satisfies(s, x, cons):
            out.append(s)
    return sortsols(dedup(out))

def bounds(cons, x):
    lo = None
    hi = None
    for c in cons:
        if head(c) in ('<', '<=', '>', '>=') and isconst(c[1]) and c[2] == x:
            if c[0] in ('<', '<='):
                lo = c[1]
            else:
                hi = c[1]
        elif head(c) in ('<', '<=', '>', '>=') and c[1] == x and isconst(c[2]):
            if c[0] in ('<', '<='):
                hi = c[2]
            else:
                lo = c[2]
    if lo is None or hi is None:
        return None
    return lo, hi

def satisfies(s, x, cons):
    for c in cons:
        h = head(c)
        if h in ('<', '<=', '>', '>=', '/=', '='):
            try:
                a = fv(subs(c[1], x, s))
                b = fv(subs(c[2], x, s))
            except Exception:
                if not isconst(s):
                    continue
                return False
            eps = 1e-12 * (1 + abs(a) + abs(b))
            if h == '<' and not a < b - eps * 0:
                return False
            if h == '<=' and not a <= b + eps:
                return False
            if h == '>' and not a > b:
                return False
            if h == '>=' and not a >= b - eps:
                return False
            if h == '/=' and abs(a - b) <= eps:
                return False
        elif h == 'and':
            if not satisfies(s, x, list(c[1:])):
                return False
    return True

# ===================================================== top-level solve
def solve(eq, x, cplx=False, cons=None):
    NC[0] = 0
    if isnode(eq, 'and') or isnode(eq, 'list'):
        return None
    h = head(eq)
    if h in ('<', '>', '<=', '>=', '/='):
        f = sub(eq[1], eq[2])
        r = solve_ineq(h, f, x)
        return r
    if h == '=':
        f = sub(eq[1], eq[2])
    elif h == 'or':
        parts = []
        for e in eq[1:]:
            r = solve(e, x, cplx, cons)
            if r is None:
                return None
            if r != 'false':
                parts.append(r)
        if not parts:
            return 'false'
        return ('or',) + tuple(parts) if len(parts) > 1 else parts[0]
    elif eq == 'true':
        return 'true'
    else:
        f = eq
    sols = solve_eq(f, x, cplx)
    if sols is None:
        return None
    if sols != 'all':
        sols = [clean(s) for s in sols]
        if not cplx:
            sols = [s for s in sols if not (isconst(s) and not isrealc(s))]
            sols = [realpart(s) for s in sols]
        sols = sortsols(dedup(sols))
    if cons:
        sols = apply_constraints(sols, x, cons)
    return sols_to_bool(x, sols)

def realpart(s):
    if isconst(s) and has(s, 'i'):
        r, i = reim(s)
        if i == 0 or (isnum(i) and abs(tofl(i)) < 1e-12):
            return r
    return s

def zeros(e, x, cplx=False, cons=None):
    NC[0] = 0
    if isnode(e, '='):
        e = sub(e[1], e[2])
    sols = solve_eq(e, x, cplx)
    if sols is None:
        return None
    if sols == 'all':
        return ('list',)
    sols = [clean(s) for s in sols]
    if not cplx:
        sols = [realpart(s) for s in sols if not (isconst(s) and not isrealc(s))]
    sols = sortsols(dedup(sols))
    if cons:
        sols = apply_constraints(sols, x, cons)
    return ('list',) + tuple(sols)

# ===================================================== deSolve
YP = ('Y1_', 'Y2_')

def desolve(ode, x, y, conds):
    # ode uses YP[0] for y', YP[1] for y''; conds list of (order, x0, value)
    NC[0] = 0
    F = eqexpr(ode) if isnode(ode, '=') else ode
    F = autocancel(F)
    if has(F, YP[1]):
        sol = de2(F, x, y)
        nconst = 2
    else:
        sol = de1(F, x, y)
        nconst = 1
    if sol is None:
        return None
    if conds:
        sol = apply_ic(sol, x, y, conds, nconst)
    return sol

def de1(F, x, y):
    y1 = YP[0]
    cs_ = coeffs(F, y1)
    if cs_ is not None and len(cs_) == 2 and freeof(cs_[1], y1):
        g = autocancel(neg(div(cs_[0], cs_[1])))
    else:
        rs = solve_eq(F, y1)
        if not rs or rs == 'all' or len(rs) != 1:
            return None
        g = rs[0]
    c1 = 'c1'
    # linear: g = A(x) y + B(x)
    gy = coeffs(expand(g), y)
    if gy is not None and len(gy) == 2 and freeof(gy[1], y):
        P = neg(gy[1])
        Bq = gy[0]
        if Bq == 0 or freeof(P, x) and freeof(Bq, x) and False:
            pass
        mu = pw('e', integrate(P, x))
        mu = dropabs(simp(mu))
        I = integ(autocancel(expand(mul(mu, Bq))), x)
        if I is not None:
            yy = autocancel(div(add(I, c1), mu))
            return ('=', y, nice(expand(yy)) if not hasden_free(yy) else nice(yy))
    # separable
    sep = separate(g, x, y)
    if sep is not None:
        p, q = sep
        L = integ(autocancel(pw(q, -1)), y)
        R = integ(p, x)
        if L is not None and R is not None:
            rs = isolate_eq(L, add(R, c1), y)
            if rs is not None and len(rs) == 1:
                return ('=', y, nice(simp(rs[0])))
            G = lncombine(L, y)
            if G is not None:
                # |G| = e^(R+c1)  ->  G = c1*e^R
                rs = solve_eq(sub(G, mul(c1, pw('e', R))), y)
                if rs and rs != 'all' and len(rs) == 1:
                    return ('=', y, nice(rs[0]))
            return ('=', L, add(R, c1))
    # Bernoulli: g = a(x) y + b(x) y^n
    bern_ = bernoulli(g, x, y)
    if bern_ is not None:
        return bern_
    # homogeneous: g(x, v x) free of x
    V = 'V_'
    h = autocancel(subs(g, y, mul(V, x)))
    if freeof(h, x) and has(h, V):
        dv = autocancel(sub(h, V))
        if dv != 0:
            L = integ(autocancel(pw(dv, -1)), V)
            if L is not None:
                R = add(fn('ln', fn('abs', x)), c1)
                rs = isolate_eq(L, R, V)
                if rs is not None and len(rs) == 1:
                    return ('=', y, nice(expand(mul(x, rs[0]))))
                L2 = subs(L, V, div(y, x))
                return ('=', L2, R)
    return None

def dropabs(e):
    if type(e) is not tuple or e[0] == 'Q':
        return e
    if e[0] == 'abs':
        return dropabs(e[1])
    return simp((e[0],) + tuple(dropabs(a) for a in e[1:]))

def lncombine(L, y):
    # sum of c*ln(|u|) -> prod u^c (None if other terms)
    terms = L[1:] if isnode(L, '+') else (L,)
    fs = []
    for t in terms:
        c, r = coef_rest(t)
        if isnode(r, 'ln') and israt(c):
            u = r[1]
            if isnode(u, 'abs'):
                u = u[1]
            fs.append(pw(u, c))
        else:
            return None
    if len(fs) < 1:
        return None
    return autocancel(mul_list(fs))

def hasden_free(e):
    return False

def isolate_eq(L, R, y):
    try:
        r = isolate(L, R, y, False, 0)
    except Exception:
        return None
    if r is None or r == 'all':
        return None
    return r

def separate(g, x, y):
    if freeof(g, y):
        return g, 1
    if freeof(g, x):
        return 1, g
    fs = g[1:] if isnode(g, '*') else (g,)
    px = []
    qy = []
    for f in fs:
        if freeof(f, y):
            px.append(f)
        elif freeof(f, x):
            qy.append(f)
        elif isnode(f, '^') and freeof(f[1], x) and freeof(f[1], y) and isnode(f[2], '+'):
            tx = [t for t in f[2][1:] if freeof(t, y)]
            ty = [t for t in f[2][1:] if freeof(t, x)]
            if len(tx) + len(ty) != len(f[2]) - 1:
                return None
            px.append(pw(f[1], add_list(tx)))
            qy.append(pw(f[1], add_list(ty)))
        else:
            return None
    return mul_list(px), mul_list(qy)

def expand_exp(e):
    if type(e) is not tuple or e[0] == 'Q':
        return e
    if e[0] == '^' and isnode(e[2], '+') and (e[1] == 'e' or isnum(e[1])):
        return mul_list([pw(e[1], t) for t in e[2][1:]])
    return simp((e[0],) + tuple(expand_exp(a) for a in e[1:]))

def bernoulli(g, x, y):
    g = expand(g)
    terms = g[1:] if isnode(g, '+') else (g,)
    groups = {}
    for t in terms:
        k = None
        fs = t[1:] if isnode(t, '*') else (t,)
        rest = []
        for f in fs:
            if f == y:
                k = 1 if k is None else None
            elif isnode(f, '^') and f[1] == y and isnum(f[2]):
                k = f[2]
            elif freeof(f, y):
                rest.append(f)
            else:
                return None
        if k is None:
            return None
        groups[k] = add(groups.get(k, 0), mul_list(rest))
    if len(groups) != 2 or 1 not in groups:
        return None
    n = [k for k in groups if k != 1][0]
    a = groups[1]
    b = groups[n]
    # v = y^(1-n): v' = (1-n)(a v + b)
    m = nsub(1, n)
    V = 'V_'
    vs = de1(sub(YP[0], mul(m, add(mul(a, V), b))), x, V)
    if vs is None or not isnode(vs, '=') or vs[1] != V:
        return None
    return ('=', y, nice(pw(vs[2], ninv(m))))

def de2(F, x, y):
    y1, y2 = YP
    c1, c2 = 'c1', 'c2'
    G = expand(F)
    a = coeffs(G, y2)
    if a is None or len(a) != 2:
        return None
    A = a[1]
    rest = a[0]
    b = coeffs(rest, y1)
    if b is None or len(b) > 2:
        return None
    B = b[1] if len(b) == 2 else 0
    rest = b[0]
    c = coeffs(rest, y)
    if c is None or len(c) > 2:
        return None
    C = c[1] if len(c) == 2 else 0
    g = neg(c[0])
    for t in (A, B, C):
        if has(t, y) or has(t, y1) or has(t, y2):
            return None
    if freeof(A, x) and freeof(B, x) and freeof(C, x):
        y1s, y2s = charsol(A, B, C, x)
    else:
        ce = cauchy_euler(A, B, C, x)
        if ce is None:
            if C == 0:
                # reduce order: v = y'
                V = 'V_'
                r = de1(add(mul(A, YP[0]), mul(B, V), neg(g)), x, V)
                if r is None or not isnode(r, '=') or r[1] != V:
                    return None
                r2 = integ(subs(r[2], 'c1', 'c2'), x)
                if r2 is None:
                    return None
                return ('=', y, add(r2, c1))
            return None
        y1s, y2s = ce
    yh = add(mul(c1, y1s), mul(c2, y2s))
    if g == 0:
        return ('=', y, yh)
    W = pyth(autocancel(expand(sub(mul(y1s, diff(y2s, x)), mul(diff(y1s, x), y2s)))))
    gg = autocancel(div(g, A))
    I1 = integ(autocancel(expand(div(mul(y2s, gg), W))), x)
    I2 = integ(autocancel(expand(div(mul(y1s, gg), W))), x)
    if I1 is None or I2 is None:
        return None
    yp = pyth(expand(add(mul(neg(y1s), I1), mul(y2s, I2))))
    return ('=', y, nice(add(yh, yp)))

def charsol(A, B, C, x):
    D = autocancel(expand(sub(mul(B, B), mul(4, A, C))))
    if isrealc(D) and fv(D) < 0:
        al = autocancel(div(neg(B), mul(2, A)))
        be = autocancel(div(sqrt(neg(D)), mul(2, A)))
        ex = pw('e', mul(al, x))
        return mul(ex, fn('cos', mul(be, x))), mul(ex, fn('sin', mul(be, x)))
    if D == 0:
        r = autocancel(div(neg(B), mul(2, A)))
        return pw('e', mul(r, x)), mul(x, pw('e', mul(r, x)))
    s = sqrt(D)
    r1 = autocancel(div(add(neg(B), s), mul(2, A)))
    r2 = autocancel(div(sub(neg(B), s), mul(2, A)))
    return pw('e', mul(r1, x)), pw('e', mul(r2, x))

def cauchy_euler(A, B, C, x):
    a = autocancel(div(A, pw(x, 2)))
    b = autocancel(div(B, x))
    if not (freeof(a, x) and freeof(b, x) and freeof(C, x)):
        return None
    # a r(r-1) + b r + c = 0
    aa = a
    bb = sub(b, a)
    cc = C
    D = autocancel(expand(sub(mul(bb, bb), mul(4, aa, cc))))
    lx = fn('ln', x)
    if isrealc(D) and fv(D) < 0:
        al = autocancel(div(neg(bb), mul(2, aa)))
        be = autocancel(div(sqrt(neg(D)), mul(2, aa)))
        return mul(pw(x, al), fn('cos', mul(be, lx))), mul(pw(x, al), fn('sin', mul(be, lx)))
    if D == 0:
        r = autocancel(div(neg(bb), mul(2, aa)))
        return pw(x, r), mul(pw(x, r), lx)
    s = sqrt(D)
    r1 = autocancel(div(add(neg(bb), s), mul(2, aa)))
    r2 = autocancel(div(sub(neg(bb), s), mul(2, aa)))
    return pw(x, r1), pw(x, r2)

def apply_ic(sol, x, y, conds, nconst):
    cs_ = ['c1', 'c2'][:nconst]
    eqs = []
    if sol[1] == y:
        Y = sol[2]
        for order, x0, v in conds:
            e = Y
            for _ in range(order):
                e = diff(e, x)
            eqs.append(('=', subs(e, x, x0), v))
    else:
        for order, x0, v in conds:
            if order == 0:
                eqs.append(subs(subs(sol, x, x0), y, v))
    used = [c for c in cs_ if has(sol, c)]
    if not eqs or not used:
        return sol
    rs = solve_system(eqs, used)
    if not rs:
        return 'false'
    s = rs[0]
    r = sol
    for c in used:
        if c in s:
            r = (r[0], subs(r[1], c, s[c]), subs(r[2], c, s[c]))
    if r[1] == y:
        return ('=', y, nice(r[2]))
    rs2 = isolate_eq(r[1], r[2], y)
    if rs2 is not None and len(rs2) >= 1:
        for cand in rs2:
            ok = True
            for order, x0, v in conds:
                if order == 0:
                    try:
                        if abs(nval(subs(cand, x, x0)) - nval(v)) > 1e-9:
                            ok = False
                    except Exception:
                        pass
            if ok:
                return ('=', y, nice(cand))
    return r

# ===================================================== fMin / fMax
def fextreme(f, x, kind, lo=None, hi=None):
    NC[0] = 0
    d = autocancel(diff(f, x))
    cands = []
    rs = solve_eq(d, x)
    if rs is None:
        rs = numeric_solve(d, x, False, tofl(nval(lo)) if lo is not None and isconst(lo) else None,
                           tofl(nval(hi)) if hi is not None and isconst(hi) else None) or []
    if rs == 'all':
        return 'true'
    exp_ = []
    for r in rs:
        ns = [w for w in symbols(r) if w[0] == 'n' and w[1:].isdigit()]
        if ns and lo is not None and hi is not None:
            for k in range(-50, 51):
                exp_.append(subs(r, ns[0], k))
        elif ns:
            exp_.append(r)
        else:
            exp_.append(r)
    rs = exp_
    for r in rs:
        r = clean(r)
        ns = [w for w in symbols(r) if w[0] == 'n' and w[1:].isdigit()]
        if ns:
            cands.append(r)
            continue
        if not isrealc(r):
            continue
        if lo is not None and fv(r) < fv(lo) - 1e-12:
            continue
        if hi is not None and fv(r) > fv(hi) + 1e-12:
            continue
        cands.append(r)
    ends = []
    ends.append(lo if lo is not None else ('*', -1, 'inf'))
    ends.append(hi if hi is not None else 'inf')
    best = None
    bv = None
    pts = []
    for c in cands + ends:
        if c == 'inf' or c == ('*', -1, 'inf'):
            v = limit(f, x, c)
        else:
            cz = c
            for w in symbols(c):
                if w[0] == 'n' and w[1:].isdigit():
                    cz = subs(cz, w, 0)
            v = subs(f, x, cz)
            if has(v, 'undef'):
                continue
        try:
            if v == 'inf':
                vv = float('inf')
            elif v == ('*', -1, 'inf'):
                vv = float('-inf')
            else:
                vv = fv(v)
        except Exception:
            continue
        if kind == 'max':
            vv = -vv
        pts.append((vv, c))
    if not pts:
        return None
    pts.sort(key=lambda p: p[0])
    m = pts[0][0]
    win = [p[1] for p in pts if abs(p[0] - m) <= 1e-10 * (1 + abs(m)) or p[0] == m]
    win = sortsols(dedup(win))
    eqs = [('=', x, w) for w in win]
    return eqs[0] if len(eqs) == 1 else ('or',) + tuple(eqs)

def nfextreme(f, x, kind, lo=None, hi=None):
    sg = 1.0 if kind == 'min' else -1.0
    def F(t):
        try:
            v = nval(f, {x: t})
            if type(v) is complex:
                v = v.real
            return sg * v
        except Exception:
            return float('inf')
    if lo is None or hi is None:
        # coarse scan
        a = -100.0 if lo is None else lo
        b = 100.0 if hi is None else hi
    else:
        a, b = lo, hi
    N = 400
    best = a
    bv = F(a)
    for i in range(N + 1):
        t = a + (b - a) * i / N
        v = F(t)
        if v < bv:
            bv = v
            best = t
    h = (b - a) / N
    l = max(a, best - h)
    r = min(b, best + h)
    g = (math.sqrt(5) - 1) / 2
    for _ in range(200):
        c = r - g * (r - l)
        d = l + g * (r - l)
        if F(c) < F(d):
            r = d
        else:
            l = c
        if abs(r - l) < 1e-12 * (1 + abs(l)):
            break
    t = 0.5 * (l + r)
    try:
        d = diff(f, x)
        def G(u):
            try:
                v = nval(d, {x: u})
                return v.real if type(v) is complex else v
            except Exception:
                return None
        t2 = newton(G, t)
        if t2 is not None and abs(t2 - t) < 10 * h and (lo is None or t2 >= lo) and (hi is None or t2 <= hi):
            t = t2
    except Exception:
        pass
    return snap(t)

# ===================================================== domain
def domain(f, x):
    conds = []
    domconds(f, x, conds)
    if not conds:
        return ('<', ('*', -1, 'inf'), x) if False else 'true'
    # intersect solution sets numerically using sample points
    pts = []
    for rel, g in conds:
        rs = solve_eq(g, x)
        if rs is None:
            return None
        if rs == 'all':
            continue
        for r in rs:
            if isrealc(r):
                pts.append(r)
    pts = sortsols(dedup(pts))
    def ok(t):
        for rel, g in conds:
            try:
                v = nval(g, {x: t})
            except Exception:
                return False
            if type(v) is complex:
                if abs(v.imag) > 1e-9:
                    return False
                v = v.real
            if not relok(rel, v):
                return False
        return True
    def okexact(p):
        for rel, g in conds:
            try:
                v = subs(g, x, p)
                vv = fv(v)
            except Exception:
                return False
            if abs(vv) < 1e-12:
                vv = 0.0
            if not relok(rel, vv):
                return False
        return True
    vals = [fv(p) for p in pts]
    if not vals:
        return 'true' if ok(0.5) else 'false'
    segs = [('I', None, pts[0], ok(vals[0] - max(1.0, abs(vals[0]))))]
    for i in range(len(pts)):
        segs.append(('P', pts[i], pts[i], okexact(pts[i])))
        if i + 1 < len(pts):
            segs.append(('I', pts[i], pts[i + 1], ok(0.5 * (vals[i] + vals[i + 1]))))
    segs.append(('I', pts[-1], None, ok(vals[-1] + max(1.0, abs(vals[-1])))))
    return segs_to_bool(segs, x)

def domconds(f, x, out):
    if type(f) is not tuple or f[0] == 'Q' or freeof(f, x):
        return
    h = f[0]
    if h == '^':
        b, p = f[1], f[2]
        if isnum(p) and nsign(p) < 0:
            out.append(('/=', b))
        if isq(p) and p[2] % 2 == 0:
            out.append(('>=' if nsign(p) > 0 else '>', b))
    elif h in ('ln', 'log'):
        out.append(('>', f[1]))
    elif h in ('arcsin', 'arccos'):
        out.append(('<=', sub(fn('abs', f[1]), 1)))
    elif h == 'tan':
        out.append(('/=', fn('cos', f[1])))
    for a in f[1:]:
        domconds(a, x, out)
