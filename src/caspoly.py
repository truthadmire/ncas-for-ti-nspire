# caspoly.py - polynomials: multivariate gcd, factorization,
# rational normal form, partial fractions, univariate tools
from cascore import *
from casout import varprio
import cmath

# ===================================================== multivariate Z[x]
# polynomial = dict {exponent tuple: nonzero int}

def p_const(c, nv):
    if c == 0:
        return {}
    return {(0,) * nv: c}

def p_add(A, B):
    C = dict(A)
    for m in B:
        v = C.get(m, 0) + B[m]
        if v:
            C[m] = v
        elif m in C:
            del C[m]
    return C

def p_neg(A):
    return dict([(m, -A[m]) for m in A])

def p_sub(A, B):
    return p_add(A, p_neg(B))

def madd(a, b):
    return tuple([a[i] + b[i] for i in range(len(a))])

def p_mul(A, B):
    C = {}
    for a in A:
        ca = A[a]
        for b in B:
            m = madd(a, b)
            v = C.get(m, 0) + ca * B[b]
            if v:
                C[m] = v
            elif m in C:
                del C[m]
    return C

def p_scale(A, c):
    if c == 0:
        return {}
    return dict([(m, A[m] * c) for m in A])

def p_pow(A, n):
    nv = len(next(iter(A))) if A else 0
    R = p_const(1, nv)
    while n > 0:
        if n & 1:
            R = p_mul(R, A)
        n >>= 1
        if n:
            A = p_mul(A, A)
    return R

def p_deg(A, k):
    d = -1
    for m in A:
        if m[k] > d:
            d = m[k]
    return d

def p_tdeg(A):
    d = -1
    for m in A:
        s = sum(m)
        if s > d:
            d = s
    return d

def setk(m, k, v):
    return m[:k] + (v,) + m[k + 1:]

def p_coeff(A, k, d):
    return dict([(setk(m, k, 0), A[m]) for m in A if m[k] == d])

def p_lc(A, k):
    return p_coeff(A, k, p_deg(A, k))

def p_isconst(A):
    if not A:
        return True
    for m in A:
        if sum(m):
            return False
    return True

def p_cval(A):
    for m in A:
        return A[m]
    return 0

def p_vars(A, nv):
    return [k for k in range(nv) if p_deg(A, k) > 0]

def p_mono(nv, k, d):
    m = [0] * nv
    m[k] = d
    return tuple(m)

def p_divexact(A, B):
    if not B:
        err("Division by zero")
    lmB = max(B)
    lcB = B[lmB]
    nv = len(lmB)
    Qt = {}
    R = dict(A)
    cnt = 0
    while R:
        cnt += 1
        if cnt > 5000:
            return None
        lmR = max(R)
        d = []
        for i in range(nv):
            x = lmR[i] - lmB[i]
            if x < 0:
                return None
            d.append(x)
        c = R[lmR]
        if c % lcB:
            return None
        q = c // lcB
        d = tuple(d)
        Qt[d] = Qt.get(d, 0) + q
        for m in B:
            mm = madd(m, d)
            v = R.get(mm, 0) - q * B[m]
            if v:
                R[mm] = v
            elif mm in R:
                del R[mm]
    return Qt

def p_icont(A):
    g = 0
    for m in A:
        g = igcd(g, A[m])
        if g == 1:
            break
    return g

def p_normsign(A):
    if A and A[max(A)] < 0:
        return p_neg(A)
    return A

def p_diff(A, k):
    C = {}
    for m in A:
        if m[k] > 0:
            mm = setk(m, k, m[k] - 1)
            C[mm] = C.get(mm, 0) + A[m] * m[k]
    return dict([(m, C[m]) for m in C if C[m]])

def p_cont(A, k, nv):
    # content w.r.t. x_k (poly in other vars)
    ds = {}
    for m in A:
        ds[m[k]] = 1
    g = {}
    for d in ds:
        g = p_gcd(g, p_coeff(A, k, d), nv)
        if p_isconst(g) and abs(p_cval(g)) == 1:
            return p_const(1, nv)
    return p_normsign(g)

EVP = (3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41)

def p_at(A, pt):
    s = 0
    for m in A:
        t = A[m]
        for i in range(len(m)):
            if m[i]:
                t *= pt[i] ** m[i]
        s += t
    return s

def p_gcd(A, B, nv):
    if not A:
        return p_normsign(B)
    if not B:
        return p_normsign(A)
    if nv and (len(A) > 2 or len(B) > 2):
        # quick coprimality test by evaluation
        c = igcd(p_icont(A), p_icont(B))
        ok = True
        for sh in (0, 1):
            pt = [EVP[(i + sh * 5) % len(EVP)] * (1 + sh) + i for i in range(nv)]
            g = igcd(p_at(A, pt), p_at(B, pt))
            if g != c:
                ok = False
                break
        if ok:
            return p_const(c, nv)
    return p_gcd0(A, B, nv)

def p_gcd0(A, B, nv):
    if not A:
        return p_normsign(B)
    if not B:
        return p_normsign(A)
    vs = []
    for k in range(nv):
        if p_deg(A, k) > 0 or p_deg(B, k) > 0:
            vs.append(k)
    if not vs:
        return p_const(igcd(p_cval(A), p_cval(B)), nv)
    k = vs[0]
    if p_deg(A, k) == 0 or p_deg(B, k) == 0:
        # one is free of x_k: gcd with content
        if p_deg(A, k) == 0:
            return p_gcd(A, p_cont(B, k, nv), nv)
        return p_gcd(p_cont(A, k, nv), B, nv)
    cA = p_cont(A, k, nv)
    cB = p_cont(B, k, nv)
    c = p_gcd(cA, cB, nv)
    pA = p_divexact(A, cA)
    pB = p_divexact(B, cB)
    if p_deg(pA, k) < p_deg(pB, k):
        pA, pB = pB, pA
    while pB and p_deg(pB, k) > 0:
        r = prem(pA, pB, k, nv)
        pA = pB
        if not r:
            pB = {}
            break
        pB = p_divexact(r, p_cont(r, k, nv))
    if pB:
        g = p_const(1, nv)
    else:
        g = p_divexact(pA, p_cont(pA, k, nv))
    return p_normsign(p_mul(c, g))

def prem(A, B, k, nv):
    dB = p_deg(B, k)
    lcB = p_lc(B, k)
    R = A
    while R and p_deg(R, k) >= dB:
        dR = p_deg(R, k)
        lcR = p_lc(R, k)
        t = p_mul(lcR, {p_mono(nv, k, dR - dB): 1})
        R = p_sub(p_mul(R, lcB), p_mul(t, B))
    return R

def p_sqfree(P, k, nv):
    # Yun: P primitive wrt k, returns [(F,i)]
    dP = p_diff(P, k)
    a = p_gcd(P, dP, nv)
    b = p_divexact(P, a)
    c = p_divexact(dP, a)
    d = p_sub(c, p_diff(b, k))
    res = []
    i = 1
    while p_deg(b, k) > 0:
        a = p_gcd(b, d, nv)
        if p_deg(a, k) > 0:
            res.append((a, i))
        b = p_divexact(b, a)
        c = p_divexact(d, a)
        d = p_sub(c, p_diff(b, k))
        i += 1
        if i > 200:
            break
    return res

def p_sqrt(D):
    if not D:
        return {}
    lm = max(D)
    lc = D[lm]
    if lc <= 0:
        return None
    for x in lm:
        if x % 2:
            return None
    r = isqrt(lc)
    if r * r != lc:
        return None
    hm = tuple([x // 2 for x in lm])
    S = {hm: r}
    nv = len(lm)
    for _ in range(len(D) + 3):
        R = p_sub(D, p_mul(S, S))
        if not R:
            return S
        lmR = max(R)
        lmS = max(S)
        m = []
        for i in range(nv):
            x = lmR[i] - lmS[i]
            if x < 0:
                return None
            m.append(x)
        m = tuple(m)
        if m >= lmS:
            return None
        c = R[lmR]
        if c % (2 * r):
            return None
        S[m] = S.get(m, 0) + c // (2 * r)
    return None

# ===================================================== expr <-> poly
def splitpow(e):
    # e = kernel^n
    b = e[1]
    x = e[2]
    if type(x) is int:
        return b, x
    if isq(x):
        return pw(b, Q(1, x[2])), x[1]
    c, r = coef_rest(x)
    if type(c) is int and c != 1:
        return pw(b, r), c
    if isq(c):
        return pw(b, mul(Q(1, c[2]), r)), c[1]
    return e, 1

def kernels(e, ks):
    t = type(e)
    if t is int or t is float:
        return
    if t is str:
        if e not in ks:
            ks.append(e)
        return
    h = e[0]
    if h == 'Q':
        return
    if h == '+' or h == '*':
        for a in e[1:]:
            kernels(a, ks)
        return
    if h == '^':
        if type(e[2]) is int:
            kernels(e[1], ks)
            return
        k, n = splitpow(e)
        if k == e or not isnode(k, '^') or True:
            if isnode(k, '^') and type(k[2]) is int:
                kernels(k, ks)
                return
            if k not in ks:
                ks.append(k)
        return
    if e not in ks:
        ks.append(e)

def sortkernels(ks):
    ks.sort(key=lambda k: varprio(k) if type(k) is str else (200, okey(k)))
    return ks

def ratform(e, ks):
    # returns (N, D) integer polys over kernels ks, or None (floats)
    nv = len(ks)
    t = type(e)
    if t is int:
        return p_const(e, nv), p_const(1, nv)
    if t is float:
        return None
    if t is tuple and e[0] == 'Q':
        return p_const(e[1], nv), p_const(e[2], nv)
    if e in ks:
        return {p_mono(nv, ks.index(e), 1): 1}, p_const(1, nv)
    h = e[0]
    if h == '+':
        N = {}
        D = p_const(1, nv)
        for a in e[1:]:
            r = ratform(a, ks)
            if r is None:
                return None
            n, d = r
            if D == d:
                N = p_add(N, n)
            else:
                g = p_gcd(D, d, nv)
                d1 = p_divexact(d, g)
                D1 = p_divexact(D, g)
                N = p_add(p_mul(N, d1), p_mul(n, D1))
                D = p_mul(D, d1)
        return N, D
    if h == '*':
        N = p_const(1, nv)
        D = p_const(1, nv)
        for a in e[1:]:
            r = ratform(a, ks)
            if r is None:
                return None
            N = p_mul(N, r[0])
            D = p_mul(D, r[1])
        return N, D
    if h == '^':
        if type(e[2]) is int:
            b = e[1]
            n = e[2]
        else:
            b, n = splitpow(e)
        if b in ks and b != e or (b == e):
            if b not in ks:
                return None
            k = ks.index(b)
            if n >= 0:
                return {p_mono(nv, k, n): 1}, p_const(1, nv)
            return p_const(1, nv), {p_mono(nv, k, -n): 1}
        r = ratform(b, ks)
        if r is None:
            return None
        if n >= 0:
            return p_pow(r[0], n), p_pow(r[1], n)
        return p_pow(r[1], -n), p_pow(r[0], -n)
    return None

def p2e(P, ks):
    terms = []
    for m in P:
        fs = [P[m]]
        for i in range(len(m)):
            if m[i]:
                fs.append(pw(ks[i], m[i]))
        terms.append(mul_list(fs))
    return add_list(terms)

def cancel_pair(N, D, nv):
    g = p_gcd(N, D, nv)
    if not p_isconst(g) or p_cval(g) != 1:
        N = p_divexact(N, g)
        D = p_divexact(D, g)
    if D and D[max(D)] < 0:
        N = p_neg(N)
        D = p_neg(D)
    return N, D

def to_ratform(e):
    ks = []
    kernels(e, ks)
    sortkernels(ks)
    r = ratform(e, ks)
    if r is None:
        return None
    N, D = cancel_pair(r[0], r[1], len(ks))
    return N, D, ks

def comdenom(e):
    if isnode(e, 'list') or isnode(e, 'mat'):
        return mapexpr(comdenom, e)
    if isrel(e):
        return (e[0], comdenom(e[1]), comdenom(e[2]))
    r = to_ratform(e)
    if r is None:
        return e
    N, D, ks = r
    cN = p_icont(N) or 1
    cD = p_icont(D) or 1
    g = igcd(cN, cD)
    num = p2e(N, ks)
    den = p2e(D, ks)
    if isnode(num, '+') and isnode(den, '+') or den == 1 or isnum(den):
        return div(num, den)
    return div(num, den)

def getnum(e):
    r = to_ratform(e)
    if r is None:
        return numer_denom(e)[0]
    return p2e(r[0], r[2])

def getden(e):
    r = to_ratform(e)
    if r is None:
        return numer_denom(e)[1]
    return p2e(r[1], r[2])

def isrel(e):
    return type(e) is tuple and e[0] in ('=', '<', '>', '<=', '>=', '/=')

def hasdenom(e):
    if isnode(e, '^') and isnum(e[2]) and nsign(e[2]) < 0 and not isconst(e[1]):
        return True
    if type(e) is tuple and e[0] in ('+', '*'):
        for a in e[1:]:
            if hasdenom(a):
                return True
    return False

def autocancel(e):
    # cancel common polynomial factors in products (TI default behaviour)
    t = type(e)
    if t is not tuple or e[0] == 'Q' or e[0] == 'str':
        return e
    h = e[0]
    args = [autocancel(a) for a in e[1:]]
    e2 = simp((h,) + tuple(args)) if h != 'hold' else e
    if not isnode(e2, '*'):
        return e2
    hasden = False
    hassum = False
    for f in e2[1:]:
        if isnode(f, '^') and isnum(f[2]) and nsign(f[2]) < 0 and not isconst(f[1]):
            if isnode(f[1], '+') or (isnode(f[1], '^') and isnode(f[1][1], '+')):
                hasden = True
        if isnode(f, '+') or (isnode(f, '^') and isnode(f[1], '+')):
            hassum = True
    if not (hasden and hassum) and not hasden:
        return e2
    if hasfloat(e2):
        return e2
    ks = []
    kernels(e2, ks)
    sortkernels(ks)
    nv = len(ks)
    if nv == 0 or nv > 6:
        return e2
    # factorwise cancellation
    nums = []
    dens = []
    for f in e2[1:]:
        if isnode(f, '^') and isnum(f[2]) and nsign(f[2]) < 0:
            dens.append(pw(f[1], nneg(f[2])))
        else:
            nums.append(f)
    num = mul_list(nums)
    den = mul_list(dens)
    rn = ratform(num, ks)
    rd = ratform(den, ks)
    if rn is None or rd is None:
        return e2
    if len(rn[0]) * len(rd[1]) > 400 or len(rn[1]) * len(rd[0]) > 400:
        return e2
    N = p_mul(rn[0], rd[1])
    D = p_mul(rn[1], rd[0])
    if len(N) > 80 or len(D) > 80 or p_tdeg(N) > 30 or p_tdeg(D) > 30:
        return e2
    g = p_gcd(N, D, nv)
    if p_isconst(g):
        return e2
    N = p_divexact(N, g)
    D = p_divexact(D, g)
    if D and D[max(D)] < 0:
        N = p_neg(N)
        D = p_neg(D)
    return div(p2e(N, ks), p2e(D, ks))

# ===================================================== univariate over Q
# list of rationals (int / ('Q',..)) low -> high

def u_trim(a):
    a = list(a)
    while a and a[-1] == 0:
        a.pop()
    return a

def u_add(a, b):
    n = max(len(a), len(b))
    return u_trim([nadd(a[i] if i < len(a) else 0, b[i] if i < len(b) else 0) for i in range(n)])

def u_neg(a):
    return [nneg(c) for c in a]

def u_sub(a, b):
    return u_add(a, u_neg(b))

def u_mul(a, b):
    if not a or not b:
        return []
    r = [0] * (len(a) + len(b) - 1)
    for i in range(len(a)):
        if a[i] == 0:
            continue
        for j in range(len(b)):
            r[i + j] = nadd(r[i + j], nmul(a[i], b[j]))
    return u_trim(r)

def u_scale(a, c):
    return u_trim([nmul(x, c) for x in a])

def u_divmod(a, b):
    b = u_trim(b)
    if not b:
        err("Division by zero")
    a = u_trim(a)
    q = [0] * max(len(a) - len(b) + 1, 0)
    r = list(a)
    lb = b[-1]
    while len(r) >= len(b) and r:
        c = ndiv(r[-1], lb)
        k = len(r) - len(b)
        q[k] = c
        for j in range(len(b)):
            r[k + j] = nsub(r[k + j], nmul(c, b[j]))
        r = u_trim(r[:-1]) if r[-1] == 0 or True else r
        r = u_trim(r)
    return u_trim(q), r

def u_monic(a):
    if not a:
        return a
    return u_scale(a, ninv(a[-1]))

def u_egcd(a, b):
    # returns g, s, t with s*a + t*b = g (monic)
    r0, r1 = u_trim(a), u_trim(b)
    s0, s1 = [1], []
    t0, t1 = [], [1]
    while r1:
        q, r = u_divmod(r0, r1)
        r0, r1 = r1, r
        s0, s1 = s1, u_sub(s0, u_mul(q, s1))
        t0, t1 = t1, u_sub(t0, u_mul(q, t1))
    if not r0:
        return r0, s0, t0
    c = ninv(r0[-1])
    return u_scale(r0, c), u_scale(s0, c), u_scale(t0, c)

def u_toexpr(a, x):
    return add_list([mul(a[i], pw(x, i)) for i in range(len(a)) if a[i] != 0])

def u_from_expr(e, x):
    cs = coeffs(e, x)
    if cs is None:
        return None
    for c in cs:
        if not israt(c):
            return None
    return u_trim(cs)

def u_toint(a):
    # rational coeffs -> primitive integer coeffs, returns (ints, factor) a = factor*ints
    L = 1
    for c in a:
        L = ilcm(L, nd(c)[1])
    ints = [nmul(c, L) for c in a]
    g = 0
    for c in ints:
        g = igcd(g, c)
    if g == 0:
        return ints, 1
    if ints[-1] < 0:
        g = -g
    ints = [c // g for c in ints]
    return ints, Q(g, L)

def i_divexact(a, b):
    # integer poly exact division or None
    a = list(a)
    if len(a) < len(b):
        return None
    q = [0] * (len(a) - len(b) + 1)
    lb = b[-1]
    for k in range(len(a) - len(b), -1, -1):
        c = a[k + len(b) - 1]
        if c % lb:
            return None
        c //= lb
        q[k] = c
        if c:
            for j in range(len(b)):
                a[k + j] -= c * b[j]
    for x in a:
        if x:
            return None
    return q

# ===================================================== numeric roots
def aberth(c):
    # roots of polynomial with coefficients c (low->high), complex list
    c = [complex(tofl(x)) if type(x) is not complex else x for x in c]
    while c and c[-1] == 0:
        c.pop()
    n = len(c) - 1
    if n < 1:
        return []
    zeros = 0
    while abs(c[0]) == 0:
        c.pop(0)
        zeros += 1
        n -= 1
    out = [0j] * zeros
    if n < 1:
        return out
    if n == 1:
        return out + [-c[0] / c[1]]
    a = [x / c[-1] for x in c]
    r = 0.0
    for i in range(n):
        v = abs(a[i]) ** (1.0 / (n - i))
        if v > r:
            r = v
    r = max(r, 1e-3)
    z = [r * cmath.exp(1j * (2 * math.pi * k / n + 0.4)) for k in range(n)]
    for it in range(600):
        mx = 0.0
        for k in range(n):
            zk = z[k]
            p = a[n]
            dp = 0j
            for j in range(n - 1, -1, -1):
                dp = dp * zk + p
                p = p * zk + a[j]
            if p == 0:
                continue
            ratio = p / dp if dp != 0 else 1e-3
            s = 0j
            for j in range(n):
                if j != k:
                    d = zk - z[j]
                    if d != 0:
                        s += 1 / d
            den = 1 - ratio * s
            w = ratio / den if den != 0 else ratio
            z[k] = zk - w
            aw = abs(w)
            if aw > mx * (1 + abs(zk)) or True:
                mx = max(mx, aw / (1 + abs(zk)))
        if mx < 1e-15:
            break
    # polish with Newton on original poly
    res = []
    for zk in z:
        for _ in range(3):
            p = c[n]
            dp = 0j
            for j in range(n - 1, -1, -1):
                dp = dp * zk + p
                p = p * zk + c[j]
            if dp == 0:
                break
            zk = zk - p / dp
        res.append(zk)
    return out + res

def divisors_int(n, limit=400):
    n = abs(n)
    if n == 0:
        return [1]
    fs, rest = factor_int_small(n)
    if rest > 1:
        fs.append((rest, 1))
    ds = [1]
    for p, k in fs:
        nd_ = []
        for d in ds:
            v = d
            for _ in range(k + 1):
                nd_.append(v)
                v *= p
        ds = nd_
        if len(ds) > limit:
            return None
    ds.sort()
    return ds

def combos(n, k):
    idx = list(range(k))
    while True:
        yield idx
        i = k - 1
        while i >= 0 and idx[i] == i + n - k:
            i -= 1
        if i < 0:
            return
        idx[i] += 1
        for j in range(i + 1, k):
            idx[j] = idx[j - 1] + 1

def ifactor_sqf(f):
    # f primitive square-free integer poly (low->high), lc>0; returns list of factors
    n = len(f) - 1
    if n <= 1:
        return [f]
    res = []
    # x factor
    while f[0] == 0:
        res.append([0, 1])
        f = f[1:]
    if len(f) - 1 <= 1:
        return res + [f] if len(f) > 1 else res
    roots = aberth(f)
    lcd = divisors_int(f[-1]) or [1]
    # rational roots
    rest = []
    for r in roots:
        found = False
        if abs(r.imag) < 1e-6 * (1 + abs(r.real)):
            for q in lcd:
                p = int(round(r.real * q))
                if p == 0 and abs(r.real) > 0.5 / q:
                    continue
                g = [-p, q]
                if igcd(p, q) != 1:
                    continue
                qq = i_divexact(f, g)
                if qq is not None:
                    res.append(g)
                    f = qq
                    found = True
                    break
        if not found:
            rest.append(r)
    if len(f) - 1 <= 3:
        if len(f) > 1:
            res.append(f)
        return res
    # group remaining roots into integer factors
    roots = rest
    if len(roots) != len(f) - 1:
        roots = aberth(f)
    lcd = divisors_int(f[-1]) or [1]
    d = 2
    while d <= (len(f) - 1) // 2 and len(roots) <= 24:
        done = False
        for idx in combos(len(roots), d):
            pc = [1 + 0j]
            for i in idx:
                r = roots[i]
                nw = [0j] * (len(pc) + 1)
                for j in range(len(pc)):
                    nw[j + 1] += pc[j]
                    nw[j] -= pc[j] * r
                pc = nw
            ok = True
            for v in pc:
                if abs(v.imag) > 1e-6 * (1 + abs(v.real)):
                    ok = False
                    break
            if not ok:
                continue
            for q in lcd:
                g = []
                good = True
                for v in pc:
                    x = v.real * q
                    ix = int(round(x))
                    if abs(x - ix) > 1e-5 * (1 + abs(x)):
                        good = False
                        break
                    g.append(ix)
                if not good:
                    continue
                qq = i_divexact(f, g)
                if qq is not None:
                    res.append(g)
                    f = qq
                    roots = [roots[i] for i in range(len(roots)) if i not in idx]
                    done = True
                    break
            if done:
                break
        if not done:
            d += 1
    if len(f) > 1:
        res.append(f)
    return res

def ufactor(a):
    # a: rational coefficient list. returns (const, [(intpoly, mult)])
    ints, c = u_toint(u_trim(a))
    if len(ints) <= 1:
        return nmul(c, ints[0] if ints else 0), []
    nv = 1
    P = dict([((i,), ints[i]) for i in range(len(ints)) if ints[i]])
    out = []
    mn = min([m[0] for m in P])
    if mn > 0:
        out.append(([0, 1], mn))
        P = dict([((m[0] - mn,), P[m]) for m in P])
    if p_deg(P, 0) > 0:
        for F, i in p_sqfree(P, 0, 1):
            fl = [0] * (p_deg(F, 0) + 1)
            for m in F:
                fl[m[0]] = F[m]
            if fl[-1] < 0:
                fl = [-x for x in fl]
                c = nneg(c)
            for g in ifactor_sqf(fl):
                if g[-1] < 0:
                    g = [-x for x in g]
                    c = nneg(c)
                out.append((g, i))
    else:
        c = nmul(c, p_cval(P))
    return c, out

def i2p(f, nv, k):
    return dict([(p_mono(nv, k, i), f[i]) for i in range(len(f)) if f[i]])

# ===================================================== multivariate factor
def mfactor(P, nv):
    # returns (rational const, [(poly, mult)])
    if not P:
        return 0, []
    c = p_icont(P)
    if P[max(P)] < 0:
        c = -c
    P = p_scale(P, 1) if c == 1 else dict([(m, P[m] // c) for m in P])
    res = []
    mins = [min([m[k] for m in P]) for k in range(nv)]
    for k in range(nv):
        if mins[k] > 0:
            res.append(({p_mono(nv, k, 1): 1}, mins[k]))
    if sum(mins):
        mn = tuple(mins)
        P = dict([(tuple([m[i] - mn[i] for i in range(nv)]), P[m]) for m in P])
    c2 = mfac_rec(P, nv, res, 1)
    return c * c2, res

def mfac_rec(P, nv, res, mult):
    vs = p_vars(P, nv)
    if not vs:
        return p_cval(P) ** mult if P else 0
    if len(vs) == 1:
        k = vs[0]
        fl = [0] * (p_deg(P, k) + 1)
        for m in P:
            fl[m[k]] = P[m]
        cc, fs = ufactor(fl)
        for g, i in fs:
            res.append((i2p(g, nv, k), i * mult))
        return cc ** mult if type(cc) is int else nipow(cc, mult)
    vs.sort(key=lambda k: p_deg(P, k))
    k = vs[0]
    cst = 1
    C = p_cont(P, k, nv)
    if not p_isconst(C):
        cst = mfac_rec(C, nv, res, mult)
        P = p_divexact(P, C)
    elif p_cval(C) != 1:
        P = p_divexact(P, C)
    for F, i in p_sqfree(P, k, nv):
        for g in msplit(F, nv, 0):
            g = p_normsign(g)
            res.append((g, i * mult))
    return cst

def ishomog(F):
    d = None
    for m in F:
        s = sum(m)
        if d is None:
            d = s
        elif s != d:
            return False
    return True

def msplit(F, nv, depth):
    vs = p_vars(F, nv)
    if len(vs) <= 1:
        if not vs:
            return [F]
        k = vs[0]
        fl = [0] * (p_deg(F, k) + 1)
        for m in F:
            fl[m[k]] = F[m]
        cc, fs = ufactor(fl)
        out = []
        for g, i in fs:
            for _ in range(i):
                out.append(i2p(g, nv, k))
        return out if out else [F]
    if depth > 8:
        return [F]
    for k in vs:
        if p_deg(F, k) == 1:
            pass
    # homogeneous in two variables
    if len(vs) == 2 and ishomog(F):
        a, b = vs
        fl = [0] * (p_deg(F, a) + 1)
        for m in F:
            fl[m[a]] = F[m]
        cc, fs = ufactor(fl)
        if len(fs) > 1 or (fs and fs[0][1] > 1):
            out = []
            for g, i in fs:
                d = len(g) - 1
                G = {}
                for j in range(len(g)):
                    if g[j]:
                        m = [0] * nv
                        m[a] = j
                        m[b] = d - j
                        G[tuple(m)] = g[j]
                for _ in range(i):
                    out.append(G)
            return out
        return [F]
    # quadratic with square discriminant
    for k in vs:
        if p_deg(F, k) == 2:
            A = p_coeff(F, k, 2)
            B = p_coeff(F, k, 1)
            C = p_coeff(F, k, 0)
            D = p_sub(p_mul(B, B), p_scale(p_mul(A, C), 4))
            S = p_sqrt(D) if D else {}
            if S is not None and S:
                x = {p_mono(nv, k, 1): 1}
                base = p_add(p_mul(p_scale(A, 2), x), B)
                G1 = p_sub(base, S)
                G2 = p_add(base, S)
                G1 = p_divexact(G1, p_mul(p_cont(G1, k, nv), p_const(p_icont(p_divexact(G1, p_cont(G1, k, nv))), nv)))
                G2 = p_divexact(G2, p_mul(p_cont(G2, k, nv), p_const(p_icont(p_divexact(G2, p_cont(G2, k, nv))), nv)))
                if G1 and G2:
                    return msplit(G1, nv, depth + 1) + msplit(G2, nv, depth + 1)
    # linear factor search
    for k in vs:
        if p_deg(F, k) < 2:
            continue
        lc = p_lc(F, k)
        tc = p_coeff(F, k, 0)
        da = pdivisors(lc, nv)
        db = pdivisors(tc, nv)
        if da is None or db is None or len(da) * len(db) > 3000:
            continue
        x = {p_mono(nv, k, 1): 1}
        for a in da:
            ax = p_mul(a, x)
            for b in db:
                for s in (1, -1):
                    G = p_add(ax, p_scale(b, s))
                    Qt = p_divexact(F, G)
                    if Qt is not None:
                        return [G] + msplit(Qt, nv, depth + 1)
    return [F]

def pdivisors(P, nv):
    # all divisors (up to sign) of polynomial P
    c, fs = mfactor(P, nv)
    di = divisors_int(c, 60)
    if di is None:
        return None
    ds = [p_const(d, nv) for d in di]
    for g, m in fs:
        nds = []
        for d in ds:
            v = d
            for _ in range(m + 1):
                nds.append(v)
                v = p_mul(v, g)
        ds = nds
        if len(ds) > 300:
            return None
    return ds

# ===================================================== factor (user level)
def factor_int_full(n):
    # complete factorization using trial division + Pollard rho
    fs = {}
    if n < 0:
        n = -n
    st = [n]
    while st:
        m = st.pop()
        if m == 1:
            continue
        small, m = factor_int_small(m)
        for p, k in small:
            fs[p] = fs.get(p, 0) + k
        if m == 1:
            continue
        if m >> 1024:
            err('Number too large to factor')
        if isprime(m):
            fs[m] = fs.get(m, 0) + 1
            continue
        d = rho(m)
        st.append(d)
        st.append(m // d)
    ks = sorted(fs)
    return [(p, fs[p]) for p in ks]

def powmod(b, e, m):
    r = 1
    b %= m
    while e > 0:
        if e & 1:
            r = r * b % m
        e >>= 1
        b = b * b % m
    return r

def isprime(n):
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if n % p == 0:
            return n == p
    d = n - 1
    s = 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        x = powmod(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = x * x % n
            if x == n - 1:
                break
        else:
            return False
    return True

def rho(n):
    if n % 2 == 0:
        return 2
    r = iroot(n, 2)
    if r * r == n:
        return r
    c = 1
    while True:
        x = 2
        y = 2
        d = 1
        cnt = 0
        while d == 1:
            x = (x * x + c) % n
            y = (y * y + c) % n
            y = (y * y + c) % n
            d = igcd(abs(x - y), n)
            cnt += 1
            if cnt > 10000:
                break
        if d != n and d != 1:
            return d
        c += 1
        if c > 3:
            err("Factorization too hard")

def factor_rat_held(q):
    n, d = nd(q)
    if n == 0:
        return 0
    fs = []
    if n < 0:
        fs.append(-1)
    for p, k in factor_int_full(n):
        fs.append(p if k == 1 else ('^', p, k))
    for p, k in factor_int_full(d):
        fs.append(('^', p, -k))
    if not fs:
        return 1
    if len(fs) == 1 and fs[0] == -1:
        return -1
    if len(fs) == 1:
        return ('hold', fs[0])
    return ('hold', ('*',) + tuple(fs))

def factor_expr(e, var=None, cplx=False):
    if israt(e):
        return factor_rat_held(e)
    if isnode(e, 'list') or isnode(e, 'mat'):
        return mapexpr(lambda a: factor_expr(a, var, cplx), e)
    if isrel(e):
        return (e[0], factor_expr(e[1], var, cplx), factor_expr(e[2], var, cplx))
    if hasfloat(e):
        return e
    ks = []
    kernels(e, ks)
    sortkernels(ks)
    nv = len(ks)
    if nv == 0:
        return e
    r = ratform(e, ks)
    if r is None:
        return e
    N, D = cancel_pair(r[0], r[1], nv)
    cn, fn_ = mfactor(N, nv)
    cd, fd = mfactor(D, nv)
    const = Q(1, 1)
    const = ndiv(cn, cd)
    nfac = []
    for g, m in fn_:
        nfac.extend(split_radical(p2e(g, ks), m, var, cplx))
    dfac = []
    for g, m in fd:
        dfac.extend(split_radical(p2e(g, ks), m, var, cplx))
    # fold numeric constants produced by splitting
    items = []
    for f, m in nfac:
        if isnum(f):
            const = nmul(const, nipow(f, m))
        else:
            items.append((f, m))
    ditems = []
    for f, m in dfac:
        if isnum(f):
            const = ndiv(const, nipow(f, m))
        else:
            ditems.append((f, m))
    items.sort(key=lambda fm: fsortkey(fm[0]))
    ditems.sort(key=lambda fm: fsortkey(fm[0]))
    out = []
    if const != 1 or (not items and not ditems):
        out.append(const)
    for f, m in items:
        out.append(f if m == 1 else ('^', f, m))
    for f, m in ditems:
        out.append(('^', f, -m))
    if len(out) == 1:
        if isnode(out[0], '^') or isnum(out[0]):
            return ('hold', out[0]) if not isnum(out[0]) else out[0]
        return out[0]
    return ('hold', ('*',) + tuple(out))

def fsortkey(f):
    ss = symbols(f)
    ss.sort(key=varprio)
    d = 0
    if ss:
        d = degree(f, ss[0])
        if d is None:
            d = 99
    return (len(ss), okey(ss), d, okey(f))

def split_radical(f, m, var, cplx):
    # split quadratic factor into linear factors (factor with var / cFactor)
    if var is None and not cplx:
        return [(f, m)]
    vs = symbols(f)
    if var is None:
        if len(vs) != 1:
            return [(f, m)]
        x = vs[0]
    else:
        x = var
    cs = coeffs(f, x)
    if cs is None or len(cs) != 3:
        if cs is not None and len(cs) == 2 and cplx:
            return [(f, m)]
        return [(f, m)]
    c, b, a = cs
    D = expand(sub(mul(b, b), mul(4, a, c)))
    if not isconst(D):
        if var is None:
            return [(f, m)]
    else:
        v = nval(D)
        if type(v) is complex:
            v = v.real
        if v < 0 and not cplx:
            return [(f, m)]
    sD = sqrt(D)
    r1 = div(add(neg(b), sD), mul(2, a))
    r2 = div(sub(neg(b), sD), mul(2, a))
    res = [(a, m)] if a != 1 else []
    res.append((sub(x, r2), m))
    res.append((sub(x, r1), m))
    return res

# ===================================================== partial fractions
def partfrac(e, x):
    # partial fraction expansion of rational function in x (rational coeffs)
    r = to_ratform(e)
    if r is None:
        return None
    N, D, ks = r
    if x not in ks:
        return None
    k = ks.index(x)
    for v in p_vars(N, len(ks)) + p_vars(D, len(ks)):
        if v != k:
            return None
    nv = len(ks)
    num = [0] * (max(p_deg(N, k), 0) + 1)
    for m in N:
        num[m[k]] = N[m]
    den = [0] * (p_deg(D, k) + 1)
    for m in D:
        den[m[k]] = D[m]
    if len(den) <= 1:
        return None
    q, rem = u_divmod(num, den)
    cc, fs = ufactor(den)
    terms = [u_toexpr(q, x)]
    if rem:
        # D = cc * prod f_i^m_i
        parts = [u_trim(pw_list(f, m)) for f, m in fs]
        rem = u_scale(rem, ninv(cc))
        for j in range(len(fs)):
            f, m = fs[j]
            Pj = parts[j]
            others = [1]
            for i in range(len(fs)):
                if i != j:
                    others = u_mul(others, parts[i])
            # A_j = rem * others^-1 mod Pj
            g, s, t = u_egcd(others, Pj)
            Aj = u_divmod(u_mul(rem, s), Pj)[1]
            # expand Aj in base f
            fe = u_toexpr(f, x)
            for p in range(m, 0, -1):
                if not Aj:
                    break
                qq, cj = u_divmod(Aj, f)
                if cj:
                    terms.append(div(u_toexpr(cj, x), pw(fe, p)))
                Aj = qq
    return add_list(terms)

def pw_list(f, m):
    r = [1]
    for _ in range(m):
        r = u_mul(r, f)
    return r

def propfrac(e, x=None):
    if israt(e):
        n, d = nd(e)
        if d == 1:
            return e
        qn = abs(n) // d
        if n < 0:
            qn = -qn
        rr = Q(n - qn * d, d)
        if qn == 0:
            return e
        return ('hold', ('+', qn, rr))
    r = to_ratform(e)
    if r is None:
        return e
    N, D, ks = r
    if x is None:
        vs = p_vars(D, len(ks))
        if not vs:
            return e
        x = ks[vs[0]]
    num = p2e(N, ks)
    den = p2e(D, ks)
    cn = coeffs(num, x)
    cd = coeffs(den, x)
    if cn is None or cd is None or len(cd) <= 1:
        return e
    qq, rr = e_divmod(cn, cd)
    return add(fromcoeffs(qq, x), div(fromcoeffs(rr, x), den))

def e_divmod(a, b):
    # polynomial division with expression coefficients
    a = [expand(c) for c in a]
    b = [expand(c) for c in b]
    while b and b[-1] == 0:
        b.pop()
    while a and a[-1] == 0:
        a.pop()
    if not b:
        err("Division by zero")
    q = [0] * max(len(a) - len(b) + 1, 1)
    r = list(a)
    lb = b[-1]
    while len(r) >= len(b) and r:
        c = autocancel(div(r[-1], lb))
        kk = len(r) - len(b)
        q[kk] = c
        for j in range(len(b)):
            r[kk + j] = expand(sub(r[kk + j], mul(c, b[j])))
        r.pop()
        while r and r[-1] == 0:
            r.pop()
    return q, r

def poly_gcd_expr(a, b):
    ks = []
    kernels(a, ks)
    kernels(b, ks)
    sortkernels(ks)
    ra = ratform(a, ks)
    rb = ratform(b, ks)
    if ra is None or rb is None:
        err("Polynomials required")
    nv = len(ks)
    g = p_gcd(ra[0], rb[0], nv)
    if not ks:
        return p_cval(g)
    return p2e(g, ks)

def expand_full(e, var=None):
    if isnode(e, 'list') or isnode(e, 'mat'):
        return mapexpr(lambda a: expand_full(a, var), e)
    if isrel(e):
        return (e[0], expand_full(e[1], var), expand_full(e[2], var))
    x = expand(e)
    if not hasdenom(x) or hasfloat(x):
        return x
    if var is None:
        ks = symbols(x)
        ks.sort(key=varprio)
        for v in ks:
            r = partfrac(x, v)
            if r is not None:
                return expand(r)
        return x
    r = partfrac(x, var)
    if r is not None:
        return expand(r)
    return x
