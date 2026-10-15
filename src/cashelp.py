# cashelp.py - on-line help for nCAS
CATS = (
    ('alg', 'Algebra', 'solve csolve zeros czeros nsolve linsolve factor cfactor expand comdenom propfrac getnum getdenom completesquare polycoeffs polydegree polyquotient polyremainder polygcd polyroots cpolyroots polyeval tExpand tCollect simplify exact approx domain'),
    ('calc', 'Calculus', 'd integral limit sumseq prodseq taylor series dominantTerm deSolve impDif arcLen tangentLine normalLine fMin fMax nfMin nfMax nInt nDerivative avgRC centralDiff'),
    ('mat', 'Matrix/vector', 'det identity transpose rref ref inverse eigVl eigVc charPoly LU QR trace norm rowNorm colNorm diag augment colAugment subMat rowSwap rowAdd mRow mRowAdd crossP dotP unitV simult constructMat newMat randMat dim rowDim colDim mat>list list>mat'),
    ('num', 'Numbers', 'gcd lcm mod remain intDiv isPrime nCr nPr ! floor ceiling round iPart fPart sign abs real imag conj angle'),
    ('list', 'Lists/stats', 'seq sum product mean median stdDev stdDevPop variance varPop max min sortA sortD cumulativeSum deltaList augment left right mid count normPdf normCdf invNorm binomPdf binomCdf poissPdf poissCdf geomPdf geomCdf'),
    ('conv', 'Conversions (expr>>name)', '>>Decimal >>approxFraction() >>DMS >>DD >>Rad >>Grad >>Polar >>Rect >>Cylind >>Sphere >>exp >>ln >>logbase() >>sin >>cos >>Base2 >>Base10 >>Base16 exp>list()'),
    ('cmd', 'Commands', ':deg :rad :grad :auto :exact :approx :real :complex :digits n :ascii :unicode :vars :clear :mode :mem  delvar a  q=quit'),
)

SYN = {
    'solve': 'solve(eqn,var) solve(eqn,var=guess)\nsolve(ineq,var) solve(eq1 and eq2,{x,y})\nsolve(...)|x>0  (n1,n2..=any integer)',
    'csolve': 'cSolve(eqn,var) complex solutions',
    'zeros': 'zeros(expr,var) -> list of roots\nzeros({e1,e2},{x,y}) -> matrix',
    'czeros': 'cZeros(expr,var) complex roots',
    'nsolve': 'nSolve(eqn,var[=guess][,lo,hi])',
    'linsolve': 'linSolve({eq1,eq2},{x,y})',
    'factor': 'factor(expr[,var]) factor(integer)\nwith var: irrational factors',
    'cfactor': 'cFactor(expr[,var]) complex factors',
    'expand': 'expand(expr[,var]) incl. partial fractions',
    'comdenom': 'comDenom(expr) common denominator',
    'propfrac': 'propFrac(expr[,var]) proper fraction',
    'getnum': 'getNum(expr) numerator',
    'getdenom': 'getDenom(expr) denominator',
    'completesquare': 'completeSquare(expr_or_eqn,var)',
    'polycoeffs': 'polyCoeffs(poly[,var]) -> {an..a0}',
    'polydegree': 'polyDegree(poly[,var])',
    'polyquotient': 'polyQuotient(p1,p2[,var])',
    'polyremainder': 'polyRemainder(p1,p2[,var])',
    'polygcd': 'polyGcd(p1,p2)',
    'polyroots': 'polyRoots(poly,var) polyRoots({coeffs})',
    'cpolyroots': 'cPolyRoots(poly,var)',
    'polyeval': 'polyEval({coeffs},x)',
    'texpand': 'tExpand(expr) expand trig of sums/multiples',
    'tcollect': 'tCollect(expr) products -> multiple angles',
    'simplify': 'simplify(expr) extra simplification',
    'exact': 'exact(expr[,tol]) floats -> fractions',
    'approx': 'approx(expr) decimal value',
    'domain': 'domain(expr,var)',
    'd': 'd(expr,var[,order])  d(expr,var)|var=val\nderivative(...) same',
    'integral': 'integral(expr,var) antiderivative\nintegral(expr,var,a,b) definite\n(∫ also accepted)',
    'limit': 'limit(expr,var,point[,dir]) dir:-1 left,1 right\npoint may be inf or -inf',
    'sumseq': 'sumSeq(expr,var,lo,hi)  (Σ) hi may be inf',
    'prodseq': 'prodSeq(expr,var,lo,hi)  (Π)',
    'taylor': 'taylor(expr,var,order[,point])',
    'series': 'series(expr,var,order[,point])',
    'dominantterm': 'dominantTerm(expr,var[,point])',
    'desolve': "deSolve(ode,x,y) use y' and y''\ndeSolve(y''+y=0 and y(0)=0 and y'(0)=1,x,y)",
    'impdif': 'impDif(eqn,x,y[,order]) dy/dx',
    'arclen': 'arcLen(expr,var,a,b)',
    'tangentline': 'tangentLine(expr,var,point)',
    'normalline': 'normalLine(expr,var,point)',
    'fmin': 'fMin(expr,var[,lo,hi]) -> var=value',
    'fmax': 'fMax(expr,var[,lo,hi])',
    'nfmin': 'nfMin(expr,var[,lo,hi]) numeric',
    'nfmax': 'nfMax(expr,var[,lo,hi]) numeric',
    'nint': 'nInt(expr,var,a,b) numeric integral',
    'nderivative': 'nDerivative(expr,var=val[,order])',
    'avgrc': 'avgRC(expr,var[=val][,h])',
    'centraldiff': 'centralDiff(expr,var[=val][,h])',
    'det': 'det(M)', 'inverse': 'M^-1 or inverse(M)', 'rref': 'rref(M)', 'ref': 'ref(M)',
    'eigvl': 'eigVl(M) eigenvalues', 'eigvc': 'eigVc(M) unit eigenvectors (columns)',
    'charpoly': 'charPoly(M,var)', 'lu': 'LU(M) -> {L,U,P} with P*M=L*U', 'qr': 'QR(M) -> {Q,R}',
    'simult': 'simult(A,b) solves A*x=b', 'constructmat': 'constructMat(expr,i,j,rows,cols)',
    'crossp': 'crossP(u,v)', 'dotp': 'dotP(u,v)', 'unitv': 'unitV(v)', 'norm': 'norm(M)',
    'seq': 'seq(expr,var,lo,hi[,step])',
    'ncr': 'nCr(n,k)', 'npr': 'nPr(n,k)', 'gcd': 'gcd(a,b)', 'lcm': 'lcm(a,b)',
    'mod': 'mod(a,b)', 'isprime': 'isPrime(n)',
    'define': 'Define f(x)=expr   or   f(x):=expr\nexpr->a  or  a:=expr   delvar a',
    'with': 'expr|x=3   expr|x>0   solve(...)|0<=x<=2pi',
    'menu': 'm or menu: numbered menus build the\ncommand for you; 0 back, q quit.\nMatrices may be typed 1,2;3,4',
    'syntax': 'implicit mult: 2x  3(x+1)  x(x+1)\n^ or ** power, sqrt( or √, pi, e, i, inf\n<= >= /= and or not, ans = last result\nlog(x)=ln(x) ([ln] key); log10(x), log(x,b)',
    'log': 'log(x) natural log (= ln, the [ln] key)\nlog10(x) base 10, log(x,b) base b',
}

def help(name=None):
    if name is None:
        out = ['nCAS help: ?topic or ?command']
        for k, t, items in CATS:
            out.append('?' + k + '  ' + t)
        out.append('?define ?with ?syntax ?menu')
        out.append('m = menus (no typing of names)')
        return '\n'.join(out)
    name = name.lower().replace('(', '').strip()
    for k, t, items in CATS:
        if name == k:
            return t + ':\n' + items
    if name in SYN:
        return SYN[name]
    for k in SYN:
        if k.startswith(name):
            return SYN[k]
    return 'No help for ' + name

SELFTEST = (
    ('factor(x^2-5x+6)', '(x-2)*(x-3)'),
    ('expand((x+1)^3)', 'x^3+3*x^2+3*x+1'),
    ('solve(x^2-5x+6=0,x)', 'x=2 or x=3'),
    ('solve(x^2=2,x)', 'x=-\u221a2 or x=\u221a2'),
    ('d(x^3*sin(x),x)', 'x^3*cos(x)+3*x^2*sin(x)'),
    ('integral(x*e^x,x)', 'x*e^x-e^x'),
    ('integral(1/(1+x^2),x,0,1)', '\u03c0/4'),
    ('limit(sin(x)/x,x,0)', '1'),
    ('taylor(e^x,x,3)', 'x^3/6+x^2/2+x+1'),
    ('sumSeq(k,k,1,n)', 'n*(n+1)/2'),
    ("deSolve(y'=y,x,y)", 'y=c1*e^x'),
    ('det([[1,2][3,4]])', '-2'),
    ('[[1,2][3,4]]^-1', '[[-2,1][3/2,-1/2]]'),
    ('sqrt(12)', '2*\u221a3'),
    ('cSolve(x^2+1=0,x)', 'x=-i or x=i'),
    ('factor(360)', '2^3*3^2*5'),
    ('solve(x^2-4>0,x)', 'x<-2 or x>2'),
    ('nSolve(cos(x)=x,x)', '0.7390851332'),
)

def selftest(run):
    ok = 0
    out = []
    for q, a in SELFTEST:
        try:
            r = run(q)
        except Exception as ex:
            r = 'ERR ' + str(ex)
        if r == a:
            ok += 1
        else:
            out.append('FAIL ' + q + ' -> ' + r)
    out.append('%d/%d tests passed' % (ok, len(SELFTEST)))
    return '\n'.join(out)
