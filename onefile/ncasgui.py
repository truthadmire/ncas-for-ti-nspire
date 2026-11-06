# ncasgui - nCAS full-screen version for TI-Nspire CX II. Run it (ctrl+R): tab menus, esc quits.
# The program is kept below as text and compiled one part at a time, which needs
# much less memory than compiling everything at once. Do not edit the text parts.
try:
 import gc
except ImportError:
 gc = None
try:
 exec
except NameError:
 print('exec() is missing: use the module install (dist/)')
 raise SystemExit
_L = {}
_P = {}     # parts of a lazy module already compiled (a failed load can be retried)
# the helpers are compiled from text too, so that nothing compiled from this
# file itself keeps the text parts in memory once the program has ended
exec("""def _u(s):
 p = s.split('$')
 return p[0] + ''.join([_W[q[0]] + q[1:] for q in p[1:]])
def _x(s):
 exec(_u(s), globals())
 if gc:
  gc.collect()
def _load(m):
 ps = _L.get(m)
 if ps is None:
  return
 i = _P.get(m, 0)
 while i < len(ps):
  if gc:
   gc.collect()
  exec(_u(ps[i]), globals())
  i += 1
  _P[m] = i
 del _L[m]
 _P.pop(m, None)""")
print('Loading nCAS...')
_W={'!': 'return', '#': 'None', '%': 'append', '&': 'else', '(': 'for', ')': 'isnode', '*': 'and', '+': 'range', ',': 'def', '-': 'not', '.': 'autocancel', '/': 'len', '0': 'type', '1': 'tuple', '2': 'False', '3': 'except', '4': 'complex', '5': 'isconst', '6': 'Exception', '7': 'continue', '8': 'freeof', '9': 'out', ':': 'depth', ';': 'lambda', '<': 'mul', '=': 'elif', '>': 'add_list', '?': 'expand', '@': 'self', 'A': 'name', 'B': 'True', 'C': 'float', 'D': 'cplx', 'E': 'ZeroDivisionError', 'F': 'while', 'G': 'isnum', 'H': 'abs', 'I': 'undef', 'J': 'list', 'K': 'mul_list', 'L': 'args', 'M': 'math', 'N': 'integral', 'O': 'sqrt', 'P': 'inf', 'Q': 'terms', 'R': 'break', 'S': 'CASError', 'T': 'ValueError', 'U': 'real', 'V': 'div', 'W': 'p_divexact', 'X': 'rows', 'Y': 'subs', 'Z': 'nval', '[': 'coeffs', ']': 'Expression', '^': 'OverflowError', '_': 'sub', '`': 'add', 'a': 'rest', 'b': 'hasfloat', 'c': 'nsign', 'd': 'raise', 'e': 'symbols', 'f': 'coef_rest', 'g': 'vals', 'h': 'islist', 'i': 'isint', 'j': 'sols', 'k': 'linear', 'l': 'angle', 'm': 'neg', 'n': 'onevar_expr', 'o': 'NoSeries', 'p': 'str', 'q': 'int', 'r': 'solve_eq', 's': 'arctan', 't': 'FSIMP', 'u': 'KeyboardInterrupt', 'v': 'ed_text', 'w': 'israt', 'x': 'HALF', 'y': 'arcsin', 'z': 'isrealc', '{': 'try', '|': 'limit', '}': 'extend', '~': 'startswith'}
_x(r'''import $M
class $S($6):
 pass
class ResourceLimit($S):
 pass
$, err(msg):
 $d $S(msg)
MAXTERMS=2000
MAXCELLS=2500
MAXLEN=5000
$, toobig(what):
 $d ResourceLimit('Resource $|: '+what)
$, cells(r,c):
 if $-($i(r)$* $i(c))or r<1 or c<1:
  err('Dimensions must be positive integers')
 if r*c>MAXCELLS:
  toobig('a %dx%d matrix has more than %d entries'%(r,c,MAXCELLS))
CONSTS=('pi','e','i')
SPECIAL=('pi','e','i','$P','$I','true','false')
$, igcd(a,b):
 if a<0:
  a=-a
 if b<0:
  b=-b
 $F b:
  a,b=b,a%b
 $! a
$, ilcm(a,b):
 if a==0 or b==0:
  $! 0
 $! $H(a//igcd(a,b)*b)
$, Q(n,d=1):
 if d==0:
  err("Division by zero")
 if d<0:
  n=-n
  d=-d
 g=igcd(n,d)
 if g>1:
  n//=g
  d//=g
 if d==1:
  $! n
 $!('Q',n,d)
$x=('Q',1,2)
$, isq(x):
 $! $0(x)is $1 $* x[0]=='Q'
$, $i(x):
 $! $0(x)is $q
$, isfl(x):
 $! $0(x)is $C
$, $w(x):
 t=$0(x)
 $! t is $q or(t is $1 $* x[0]=='Q')
$, $G(x):
 t=$0(x)
 $! t is $q or t is $C or(t is $1 $* x[0]=='Q')
$, nd(x):
 if $0(x)is $q:
  $! x,1
 $! x[1],x[2]
$, tofl(x):
 t=$0(x)
 if t is $C:
  $! x
 if t is $q:
  $! $C(x)
 $! x[1]/x[2]
$, nadd(a,b):
 ta=$0(a)
 tb=$0(b)
 if ta is $q $* tb is $q:
  $! a+b
 if ta is $C or tb is $C:
  $! tofl(a)+tofl(b)
 an,ad=nd(a)
 bn,bd=nd(b)
 if ad==bd:
  $! Q(an+bn,ad)
 g=igcd(ad,bd)
 if g>1:
  ad//=g
  $! Q(an*(bd//g)+bn*ad,ad*bd)
 $! Q(an*bd+bn*ad,ad*bd)
$, nmul(a,b):
 ta=$0(a)
 tb=$0(b)
 if ta is $q $* tb is $q:
  $! a*b
 if ta is $C or tb is $C:
  $! tofl(a)*tofl(b)
 an,ad=nd(a)
 bn,bd=nd(b)
 g=igcd(an,bd)
 if g>1:
  an//=g
  bd//=g
 g=igcd(bn,ad)
 if g>1:
  bn//=g
  ad//=g
 $! Q(an*bn,ad*bd)
$, nneg(a):
 if $0(a)is $1:
  $!('Q',-a[1],a[2])
 $!-a
$, nsub(a,b):
 $! nadd(a,nneg(b))
$, ninv(a):
 t=$0(a)
 if t is $C:
  if a==0.0:
   err("Division by zero")
  $! 1.0/a
 n,d=nd(a)
 $! Q(d,n)
$, ndiv(a,b):
 $! nmul(a,ninv(b))
$, $c(a):
 if $0(a)is $1:
  a=a[1]
 if a>0:
  $! 1
 if a<0:
  $!-1
 $! 0
$, ncmp(a,b):
 $! $c(nsub(a,b))
$, nfloor(a):
 t=$0(a)
 if t is $q:
  $! a
 if t is $C:
  if a!=a or a in($C('$P'),$C('-$P')):
   err("Domain error")
  $! $q($M.floor(a))
 $! a[1]//a[2]
$, nabs(a):
 if $c(a)<0:
  $! nneg(a)
 $! a
$, nipow(a,k):
 if k<0:
  $! nipow(ninv(a),-k)
 if $0(a)is $C:
  $! a**k
 n,d=nd(a)
 $! Q(n**k,d**k)
$, iroot(n,k):
 if n<2:
  $! n
 x=$q($M.pow(n,1.0/k))if n<10**300 $& 1<<(($/(bin(n))-2)//k+1)
 if x<1:
  x=1
 $F $B:
  y=((k-1)*x+n//(x**(k-1)))//k
  if y>=x:
   $R
  x=y
 $F x**k>n:
  x-=1
 $F(x+1)**k<=n:
  x+=1
 $! x
$, isqrt(n):
 $! iroot(n,2)
SMALLP=$#
$, smallprimes():
 global SMALLP
 if SMALLP is $#:
  N=1000
  s=bytearray(N)
  ps=[]
  $( i in $+(2,N):
   if $- s[i]:
    ps.$%(i)
    $( j in $+(i*i,N,i):
     s[j]=1
  SMALLP=ps
 $! SMALLP
$, $)(e,h):
 $! $0(e)is $1 $* e[0]==h
$, head(e):
 if $0(e)is $1:
  $! e[0]
 $! $#
$, okey(e):
 $! repr(e)
$, has(e,x):
 if e==x:
  $! $B
 if $0(e)is $1 $* e[0]!='Q':
  $( a in e[1:]:
   if has(a,x):
    $! $B
 $! $2
$, $8(e,x):
 $! $- has(e,x)
$, freeofall(e,xs):
 $( x in xs:
  if has(e,x):
   $! $2
 $! $B
$, $e(e,$9=$#):
 if $9 is $#:
  $9=[]
 t=$0(e)
 if t is $p:
  if e $- in SPECIAL $* e $- in $9:
   $9.$%(e)
 $= t is $1 $* e[0]!='Q' $* e[0]!='$p':
  $( a in e[1:]:
   $e(a,$9)
 $! $9
$, $5(e):
 t=$0(e)
 if t is $p:
  $! e in SPECIAL
 if t is $1 $* e[0]!='Q':
  if e[0]=='$p':
   $! $2
  $( a in e[1:]:
   if $- $5(a):
    $! $2
 $! $B
$, $b(e):
 t=$0(e)
 if t is $C:
  $! $B
 if t is $1 $* e[0]!='Q':
  $( a in e[1:]:
   if $b(a):
    $! $B
 $! $2
$, $f(a):
 if $0(a)is $1 $* a[0]=='*' $* $G(a[1]):
  if $/(a)==3:
   $! a[1],a[2]
  $! a[1],('*',)+a[2:]
 $! 1,a
$, cmul(c,r):
 if $0(c)is $q $* c==1:
  $! r
 if $0(r)is $1 $* r[0]=='*':
  if $G(r[1]):
   c=nmul(c,r[1])
   if $0(c)is $q $* c==1:
    $!('*',)+r[2:]if $/(r)>3 $& r[2]
   $!('*',c)+r[2:]
  $!('*',c)+r[1:]
 $!('*',c,r)
$, $`(*$L):
 $! $>($L)
$, $>($L):
 num=0
 $Q={}
 order=[]
 st=$J($L)
 infs=0
 $F st:
  a=st.pop()
  t=$0(a)
  if t is $q or t is $C:
   num=nadd(num,a)
   $7
  if t is $1:
   h=a[0]
   if h=='Q':
    num=nadd(num,a)
    $7
   if h=='+':
    st.$}(a[1:])
    $7
   if h=='*' $* $G(a[1]):
    c=a[1]
    r=a[2]if $/(a)==3 $&('*',)+a[2:]
   $&:
    c=1
    r=a
  $&:
   if a=='$I':
    $! '$I'
   c=1
   r=a
  if r=='$P':
   s=$c(c)
   if s==0:
    $7
   if infs $* infs!=s:
    $! '$I'
   infs=s
   $7
  if r in $Q:
   $Q[r]=nadd($Q[r],c)
  $&:
   $Q[r]=c
   order.$%(r)
 if infs:
  $! '$P' if infs>0 $&('*',-1,'$P')
 $9=[]
 $( r in order:
  c=$Q[r]
  if c==0:
   $7
  $9.$%(cmul(c,r))
 if num!=0 or $- $9:
  if $9 $* num==0:
   pass
  $&:
   $9.$%(num)
 if $/($9)==1:
  $! $9[0]
 $9.sort(key=okey)
 $!('+',)+$1($9)
$, isrrad(e):
 $! $0(e)is $1 $* e[0]=='^' $* $0(e[1])is $q $* isq(e[2])
$, $<(*$L):
 $! $K($L)
''')
_x(r'''$, $K($L):
 coef=1
 bases={}
 order=[]
 st=$J($L)
 $F st:
  a=st.pop()
  t=$0(a)
  if t is $q or t is $C:
   coef=nmul(coef,a)
   $7
  if t is $1:
   h=a[0]
   if h=='Q':
    coef=nmul(coef,a)
    $7
   if h=='*':
    st.$}(a[1:])
    $7
   if h=='^':
    b=a[1]
    x=a[2]
   $&:
    b=a
    x=1
  $&:
   if a=='$I':
    $! '$I'
   b=a
   x=1
  if b in bases:
   bases[b]=$`(bases[b],x)
  $&:
   bases[b]=x
   order.$%(b)
 if coef==0:
  if '$P' in bases:
   $! '$I'
  $( b in order:
   if b=='$I' or has(b,'$I'):
    $! '$I'
  $! coef
 facs=[]
 rad={}
 radorder=[]
 $, collect(p):
  c=1
  t=$0(p)
  if t is $q or t is $C or(t is $1 $* p[0]=='Q'):
   $! p
  if t is $1 $* p[0]=='*':
   items=p[1:]
  $&:
   items=(p,)
  $( f in items:
   if $G(f):
    c=nmul(c,f)
   $= isrrad(f):
    ex=f[2]
    if ex in rad:
     rad[ex]=rad[ex]*f[1]
     radorder.$%($#)
    $&:
     rad[ex]=f[1]
     radorder.$%(ex)
   $&:
    facs.$%(f)
  $! c
 $( b in order:
  p=pw(b,bases[b])
  if p=='$I':
   $! '$I'
  coef=nmul(coef,collect(p))
 if rad:
  multi=$/(radorder)!=$/(rad)
  if multi:
   items=[(ex,rad[ex])$( ex in radorder if ex is $- $#]
   rad.clear()
   del radorder[:]
   pend=[]
   $( ex,b in items:
    pend.$%(pw_num(b,ex))
   $( p in pend:
    coef=nmul(coef,collect(p))
  $( ex in rad:
   facs.$%(('^',rad[ex],ex))
 if coef==0:
  $! 0
 if '$P' in facs:
  if $/(facs)==1 or $B:
   coef=$c(coef)if $0(coef)is $- $C $&(1.0 if coef>0 $&-1.0)
   if $0(coef)is $C:
    coef=$q(coef)
 if $- facs:
  $! coef
 if $/(facs)>1:
  algs=[f $( f in facs if $)(f,'+')$* isalg(f)]
  if algs $* all([isalg(f)$( f in facs]):
   r=coef
   $( f in facs:
    r=expand_mul(r,f)
   $! r
 if $/(facs)==1:
  f=facs[0]
  if $0(coef)is $q $* coef==1:
   $! f
  if $0(f)is $1 $* f[0]=='+':
   $! $>([$<(coef,t)$( t in f[1:]])
  $!('*',coef,f)
 facs.sort(key=okey)
 if $0(coef)is $q $* coef==1:
  $!('*',)+$1(facs)
 $!('*',coef)+$1(facs)
$, $m(a):
 $! $<(-1,a)
$, $_(a,b):
 $! $`(a,$<(-1,b))
$, $V(a,b):
 $! $<(a,pw(b,-1))
$, inv(a):
 $! pw(a,-1)
$, $O(a):
 $! pw(a,$x)
$, factor_int_small(n):
 fs=[]
 $( p in smallprimes():
  if p*p>n:
   $R
  if n%p==0:
   k=0
   $F n%p==0:
    n//=p
    k+=1
   fs.$%((p,k))
 $! fs,n
$, radical(n,q):
 if n<2:
  $! n,1
 a=1
 m=1
 fs,$a=factor_int_small(n)
 $( p,k in fs:
  a*=p**(k//q)
  m*=p**(k%q)
 if $a>1:
  r=iroot($a,q)
  if r**q==$a:
   a*=r
  $&:
   m*=$a
 $! a,m
$, ipow_root(n,p,q):
 if ibits(n)*p>2000 or q>60:
  $!('^',n,Q(p,q))
 a,m=radical(n**p,q)if p>1 $& radical(n,q)
 if m==1:
  $! a
 ex=Q(1,q)
 k=2
 best=$#
 $F(1<<k)<=m $* k<=64:
  r=iroot(m,k)
  if r**k==m:
   best=(r,k)
  k+=1
 if best is $- $#:
  m=best[0]
  ex=Q(best[1],q)
 if ex==1:
  $! a*m
 if $i(ex):
  $! a*m**ex
 if a==1:
  $!('^',m,ex)
 $!('*',a,('^',m,ex))
MAXBITS=12000
$, ibits(n):
 if n==0:
  $! 0
 h='%x'%$H(n)
 v=$q(h[0],16)
 $! 4*$/(h)-(3 if v<2 $& 2 if v<4 $& 1 if v<8 $& 0)
$, bigpow(b,x):
 n,d=nd(b)
 if d==1 $* $H(n)<=1:
  $! $2
 $! $H(x)*(ibits(n)+(ibits(d)if d>1 $& 0))>MAXBITS
$, pw_num(b,x):
 if $0(b)is $C or $0(x)is $C:
  bf=tofl(b)
  xf=tofl(x)
  if bf==0.0:
   if xf>0:
    $! 0.0
   if xf==0:
    $! 1.0
   $! '$I'
  if bf!=bf or xf!=xf:
   $! '$I'
  if bf<0 $*(xf in($C('$P'),$C('-$P'))or xf!=$M.floor(xf)):
   if $w(x)$* nd(x)[1]%2==1:
    r=(-bf)**xf
    $!-r if nd(x)[0]%2 $& r
   z=$4(bf)**xf
   $! fromcomplex(z)
  ${:
   $! bf**xf
  $3 $^:
   $! '$P'
 if $0(x)is $q:
  if b==0:
   if x<0:
    $! '$I'
   $! 0
  if bigpow(b,x):
   $!('^',b,x)
  $! nipow(b,x)
 p,q=nd(x)
 if b==0:
  $! 0 if p>0 $& '$I'
 if $c(b)<0:
  if q%2==1:
   r=pw_num(nneg(b),x)
   if p%2:
    $! $<(-1,r)
   $! r
  if q==2:
   $! $<(pw('i',p),pw_num(nneg(b),x))
  $!('^',b,x)
 if b==1:
  $! 1
 n,d=nd(b)
 k=p//q
 if bigpow(b,k+1):
  $!('^',b,x)
 f=Q(p-k*q,q)
 res=nipow(b,k)
 if f==0:
  $! res
 fp,fq=nd(f)
 parts=[]
 if n>1:
  parts.$%(ipow_root(n,fp,fq))
 if d>1:
  parts.$%(Q(1,d))
  parts.$%(ipow_root(d,fq-fp,fq))
 c=res
 facs=[]
 $( pt in parts:
  if $G(pt):
   c=nmul(c,pt)
  $= pt[0]=='*':
   c=nmul(c,pt[1])
   facs.$%(pt[2])
  $&:
   facs.$%(pt)
 if $/(facs)==2:
  if facs[0][2]==facs[1][2]:
   $! $<(c,pw_num(facs[0][1]*facs[1][1],facs[0][2]))
  facs.sort(key=okey)
 if $- facs:
  $! c
 if c==1:
  if $/(facs)==1:
   $! facs[0]
  $!('*',)+$1(facs)
 $!('*',c)+$1(facs)
$, isposconst(e):
 if $G(e):
  $! $c(e)>0
 if e=='pi' or e=='e':
  $! $B
 if isrrad(e):
  $! e[1]>0
 if $)(e,'^')$*(e[1]=='e' or e[1]=='pi')$* isreal_expr(e[2]):
  $! $B
 $! $2
$, isalg(e):
 t=$0(e)
 if t is $q or t is $C:
  $! $B
 if t is $p:
  $! e=='i'
 h=e[0]
 if h=='Q':
  $! $B
 if h=='^':
  $! $G(e[1])$* $G(e[2])
 if h=='+' or h=='*':
  $( a in e[1:]:
   if $- isalg(a):
    $! $2
  $! $B
 $! $2
''')
_x(r'''$, pw(b,x):
 if x==0:
  if b=='$I' or b=='$P':
   $! '$I'
  $! 1
 if $0(x)is $q $* x==1:
  $! b
 if b=='$I' or x=='$I':
  $! '$I'
 bn=$G(b)
 xn=$G(x)
 if bn $* xn:
  $! pw_num(b,x)
 if b==1 $* $0(b)is $q:
  $! 1
 if b=='$P':
  if xn:
   $! '$P' if $c(x)>0 $& 0
  if x=='$P':
   $! '$P'
 if xn $* b==0:
  $! 0 if $c(x)>0 $& '$I'
 if b=='i' $* $0(x)is $q:
  r=x%4
  $!(1,'i',-1,('*',-1,'i'))[r]
 if x=='$P' $* bn:
  if nabs(b)==1:
   $! '$I' if b==1 $& '$I'
  if ncmp(nabs(b),1)>0:
   $! '$P' if $c(b)>0 $& '$I'
  $! 0
 if b=='e':
  if x=='$P':
   $! '$P'
  if $)(x,'*')$* $/(x)==3 $* x[1]==-1 $* x[2]=='$P':
   $! 0
  if $0(x)is $C:
   $! $M.exp(x)
  if $)(x,'ln'):
   $! x[1]
  if $)(x,'*'):
   c,r=$f(x)
   if $)(r,'ln')$* $w(c):
    $! pw(r[1],c)
  if $)(x,'+'):
   outs=[]
   $a=[]
   $( t in x[1:]:
    c,r=$f(t)
    if $)(r,'ln')$* $w(c):
     outs.$%(pw(r[1],c))
    $&:
     $a.$%(t)
   if outs:
    $! $K(outs+[pw('e',$>($a))])
  if $)(x,'*')$* 'i' in x $* 'pi' in x:
   c,r=$f(x)
   if r==('*','i','pi')$* $w(c):
    $! $`(cos_($<(c,'pi')),$<('i',sin_($<(c,'pi'))))
 if b!='e' $* $5(b)$* $5(x)$* $- $w(x)$*(has(b,'i')or has(x,'i'))$* $- $b(x):
  L=fn('ln',b)
  if $- $)(L,'ln')$* $-($)(L,'+')$* any([$)(t,'ln')$( t in L[1:]])):
   $! pw('e',$?($<(x,L)))
 if $0(b)is $1:
  h=b[0]
  if h=='^':
   bb=b[1]
   ee=b[2]
   if $0(x)is $q:
    $! pw(bb,$<(ee,x))
   if isposconst(bb):
    $! pw(bb,$<(ee,x))
   if $w(ee)$* $w(x):
    r=nmul(ee,x)
    if $0(ee)is $q:
     if ee%2==0:
      if $0(r)is $q $* r%2==0:
       $! pw(bb,r)
      $! pw(fn('$H',bb),r)
     $! pw(bb,r)
    if nd(ee)[0]%2==1 $* nd(ee)[1]%2==1:
     $! pw(bb,r)
    if nd(ee)[0]%2==1:
     $! pw(bb,r)
  $= h=='*':
   if $0(x)is $q:
    $! $K([pw(f,x)$( f in b[1:]])
   outs=[]
   $a=[]
   $( f in b[1:]:
    if $G(f):
     if $c(f)>0:
      outs.$%(pw(f,x))
     $= f!=-1:
      outs.$%(pw(nneg(f),x))
      $a.$%(-1)
     $&:
      $a.$%(f)
    $= isposconst(f)or $)(f,'$H'):
     outs.$%(pw(f,x))
    $&:
     $a.$%(f)
   if outs:
    $! $K(outs+[pw($K($a),x)])
  $= h=='$H':
   if $0(x)is $q $* x%2==0:
    $! pw(b[1],x)
  $= h=='+':
   if x==$x $* isalg(b)$* $- has(b,'i'):
    dn=denest(b)
    if dn is $- $#:
     $! dn
   if isq(x)$* x[2]==2 $* $c(x)<0 $* isalg(b)$* $- has(b,'i'):
    dn=denest(b)
    if dn is $- $#:
     $! pw(pw(dn,-1),-x[1])if x[1]!=-1 $& pw(dn,-1)
   if $0(x)is $q $* x!=1 $* $- isalg(b):
    c=sumcontent(b)
    if c!=1:
     $! $<(pw(c,x),pw($<(ninv(c),b),x))
    if leadneg(b):
     nb=$<(-1,b)
     if x%2==0:
      $! pw(nb,x)
     $! $<(-1,pw(nb,x))
   if $0(x)is $q $* isalg(b):
    if x>0 $* x<=64:
     $! expand_pow(b,x)
    if x<0 $* x>=-64:
     r=rationalize_inv(b)
     if r is $- $#:
      if x==-1:
       $! r
      $! expand_pow(r,-x)
 $!('^',b,x)
$, tdeg(r):
 d=0
 fs=r[1:]if $)(r,'*')$&(r,)
 $( f in fs:
  if $0(f)is $p $* f $- in SPECIAL:
   d+=1
  $= $)(f,'^')$* $0(f[1])is $p $* f[1]$- in SPECIAL $* $G(f[2]):
   d+=tofl(f[2])
 $! d
$, leadneg(b):
 best=$#
 bk=$#
 $( t in b[1:]:
  if $G(t):
   $7
  c,r=$f(t)
  k=(-tdeg(r),okey(r))
  if bk is $# or k<bk:
   bk=k
   best=c
 if best is $#:
  $! $2
 $! $c(best)<0 if $G(best)$& $2
$, sumcontent(b):
 g=0
 L=1
 $( t in b[1:]:
  c,r=$f(t)
  if $- $w(c):
   $! 1
  n,d=nd(c)
  g=igcd(g,n)
  L=ilcm(L,d)
 if g==0:
  $! 1
 $! Q(g,L)
$, denest(b):
 a=0
 c=0
 n=$#
 $( t in b[1:]:
  if $w(t):
   a=nadd(a,t)
   $7
  cc,r=$f(t)
  if isrrad(r)$* r[2]==$x $* $w(cc)$*(n is $# or n==r[1]):
   n=r[1]
   c=nadd(c,cc)
  $&:
   $! $#
 if n is $# or c==0:
  $! $#
 d2=nsub(nmul(a,a),nmul(nmul(c,c),n))
 if $c(d2)<0:
  $! $#
 dn,dd=nd(d2)
 rn=isqrt(dn)
 rd=isqrt(dd)
 if rn*rn!=dn or rd*rd!=dd:
  $! $#
 d=Q(rn,rd)
 p=ndiv(nadd(a,d),2)
 m=ndiv(nsub(a,d),2)
 if $c(p)<0 or $c(m)<0:
  $! $#
 r=$`(pw(p,$x),$<($c(c),pw(m,$x)))
 if $)(r,'+')$* $/(r)<=3:
  $! r
 $! $#
$, expand_mul(a,b):
 ta=a[1:]if $)(a,'+')$&(a,)
 tb=b[1:]if $)(b,'+')$&(b,)
 if $/(ta)*$/(tb)>4*MAXTERMS:
  toobig('the expansion would have more than %d $Q'%MAXTERMS)
 $9=[]
 $( u in ta:
  $( v in tb:
   $9.$%($<(u,v))
 $! $>($9)
$, expand_pow(b,n):
 t=$/(b)-1 if $)(b,'+')$& 1
 if t>1 $* $- $5(b):
  c=1
  $( k in $+(1,t):
   c=c*(n+k)//k
   if c>MAXTERMS:
    toobig('the expansion would have more than %d $Q'%MAXTERMS)
 r=1
 p=b
 $F n>0:
  if n&1:
   r=expand_mul(r,p)
  n>>=1
  if n:
   p=expand_mul(p,p)
 $! r
''')
_x(r'''$, rationalize_inv(b):
 re_,im_=reim(b)
 if im_!=0:
  d=$`($<(re_,re_),$<(im_,im_))
  d=$?(d)
  if $)(d,'+'):
   r2=rationalize_inv(d)
   if r2 is $#:
    $! $#
  $&:
   r2=pw(d,-1)
  $! expand_mul($_(re_,$<('i',im_)),r2)
 $Q=b[1:]if $)(b,'+')$&(b,)
 kern=$#
 kerns=[]
 $( t in $Q:
  c,r=$f(t)
  if r!=1 $* $- $G(r):
   if isrrad(r)$* r[2]==$x:
    if r $- in kerns:
     kerns.$%(r)
   $&:
    $! $#
 if $- kerns or $/(kerns)>3:
  $! $#
 kern=kerns[0]
 if $/(kerns)>1:
  A=$>([t $( t in $Q if $f(t)[1]!=kern])
  B=$>([$f(t)[0]$( t in $Q if $f(t)[1]==kern])
  den=$?($_($<(A,A),$<(B,B,kern[1])))
  if den==0:
   $! $#
  if $)(den,'+'):
   r2=rationalize_inv(den)
   if r2 is $#:
    $! $#
  $&:
   r2=pw(den,-1)
  $! expand_mul($_(A,$<(B,kern)),r2)
 a0=0
 a1=0
 $( t in $Q:
  c,r=$f(t)
  if r==kern:
   a1=nadd(a1,c)
  $&:
   a0=$`(a0,t)
 den=$_($<(a0,a0),$<(nmul(a1,a1),kern[1]))
 if den==0:
  $! $#
 $! expand_mul($_(a0,$<(a1,kern)),pw(den,-1))
$, reim(e):
 t=$0(e)
 if t is $q or t is $C:
  $! e,0
 if t is $p:
  if e=='i':
   $! 0,1
  $! e,0
 h=e[0]
 if h=='Q':
  $! e,0
 if h=='+':
  rs=[]
  ims=[]
  $( a in e[1:]:
   r,i=reim(a)
   rs.$%(r)
   ims.$%(i)
  $! $>(rs),$>(ims)
 if h=='*':
  r=1
  i=0
  $( a in e[1:]:
   ar,ai=reim(a)
   if ai==0:
    r=$<(r,ar)
    i=$<(i,ar)
   $&:
    r,i=$_($<(r,ar),$<(i,ai)),$`($<(r,ai),$<(i,ar))
  $! r,i
 if h=='^':
  b=e[1]
  x=e[2]
  if $- has(b,'i')$* $- has(x,'i'):
   if $G(x)$* $- $w(x):
    $! e,0
   if $w(x)$* nd(x)[1]%2==0:
    if $5(b):
     v=cv(b)
     if v is $- $# $* $0(v)is $- $4 $* v<0:
      $! reim_generic(e)
    $! e,0
   $! e,0
  if $0(x)is $q:
   br,bi=reim(b)
   if x>0:
    z=expand_pow($`(br,$<('i',bi)),x)
    if has(z,'i')$* z!=e:
     $! reim(z)
   $= $5(b):
    r=rationalize_inv(b)
    if r is $- $#:
     $! reim(expand_pow(r,-x))if x!=-1 $& reim(r)
  $! reim_generic(e)
 if h in('$J','mat','$p'):
  $! e,0
 $( a in e[1:]:
  if has(a,'i'):
   $! reim_generic(e)
 $! e,0
$, cv(u):
 ${:
  v=$Z(u)
 $3($S,$T,$E,$^,TypeError):
  $! $#
 if v!=v:
  $! $#
 if $0(v)is $4:
  if v.$U!=v.$U or v.imag!=v.imag:
   $! $#
  if $H(v.$U)==$C('$P')or $H(v.imag)==$C('$P'):
   $! $#
 $= $H(v)==$C('$P'):
  $! $#
 $! v
$, reim_generic(e):
 if $5(e):
  v=cv(e)
  if v is $#:
   $!('$U',e),('imag',e)
  z=$4(v)
  $! z.$U,z.imag
 $!('$U',e),('imag',e)
$, conj(e):
 r,i=reim(e)
 $! $_(r,$<('i',i))
$, fromcomplex(z):
 if $0(z)is $- $4:
  $! z
 if z.imag==0:
  $! z.$U
 if z.$U==0:
  $! $<(z.imag,'i')
 $! $`(z.$U,$<(z.imag,'i'))
$t={}
$, fn($A,*$L):
 if $/($L)==1 $* $0($L[0])is $J:
  $L=$1($L[0])
 $( a in($L[:1]if $A=='when' $& $L):
  if a=='$I':
   $! '$I'
 f=$t.get($A)
 if f is $- $#:
  r=f(*$L)
  if r is $- $#:
   $! r
 $!($A,)+$1($L)
$, isneg(e):
 if $G(e):
  $! $c(e)<0
 if $)(e,'*'):
  $! $G(e[1])$* $c(e[1])<0
 if $)(e,'+'):
  $! leadneg(e)
 $! $2
$, isreal_expr(e):
 if $G(e):
  $! $B
 if $0(e)is $p:
  $! e!='i' $* e!='$I'
 $! $- has(e,'i')
$, fval($A,x):
 $! fromcomplex(NUMF[$A](x))
$, fvalc($A,u):
 ${:
  v=NUMF[$A]($Z(u))
 $3($S,$T,$E,$^,TypeError):
  $! $#
 if $0(v)is $4:
  if v.$U!=v.$U or v.imag!=v.imag:
   $! $#
 $= v!=v:
  $! $#
 $! fromcomplex(v)
$, pi_coef(u):
 if u=='pi':
  $! 1
 if u==0:
  $! 0
 if $)(u,'*')$* $/(u)==3 $* u[2]=='pi' $* $w(u[1]):
  $! u[1]
 $! $#
$, split_pi(u):
 if $)(u,'+'):
  $( t in u[1:]:
   c=pi_coef(t)
   if c is $- $# $* c!=0:
    $a=$>([s $( s in u[1:]if s is $- t])
    $! c,$a
 $! $#
TRIGT=$#
$, trig_table():
 global TRIGT
 if TRIGT is $#:
  s2=$O(2)
  s3=$O(3)
  s5=$O(5)
  s6=$O(6)
  q=Q
  T={}
  T[0]=0
  T[q(1,12)]=$<(q(1,4),$_(s6,s2))
  T[q(1,10)]=$<(q(1,4),$_(s5,1))
  T[q(1,8)]=$<($x,$O($_(2,s2)))
  T[q(1,6)]=$x
  T[q(1,5)]=$<(q(1,4),$O($_(10,$<(2,s5))))
  T[q(1,4)]=$<($x,s2)
  T[q(3,10)]=$<(q(1,4),$`(s5,1))
  T[q(1,3)]=$<($x,s3)
  T[q(3,8)]=$<($x,$O($`(2,s2)))
  T[q(2,5)]=$<(q(1,4),$O($`(10,$<(2,s5))))
  T[q(5,12)]=$<(q(1,4),$`(s6,s2))
  T[$x]=1
  TT={}
  TT[0]=0
  TT[q(1,12)]=$_(2,s3)
  TT[q(1,8)]=$_(s2,1)
  TT[q(1,6)]=$<(q(1,3),s3)
  TT[q(1,4)]=1
  TT[q(1,3)]=s3
  TT[q(3,8)]=$`(s2,1)
  TT[q(5,12)]=$`(2,s3)
  TT[q(1,5)]=$O($_(5,$<(2,s5)))
  TT[q(2,5)]=$O($`(5,$<(2,s5)))
  TT[q(1,10)]=$<(q(1,5),$O($_(25,$<(10,s5))))
  TT[q(3,10)]=$<(q(1,5),$O($`(25,$<(10,s5))))
  TRIGT=(T,TT)
 $! TRIGT
$, sin_pi(c):
 c=nsub(c,nmul(2,nfloor(nmul(c,$x))))
 sg=1
 if ncmp(c,1)>=0:
  c=nsub(c,1)
  sg=-1
 if ncmp(c,$x)>0:
  c=nsub(1,c)
 T=trig_table()[0]
 if c in T:
  $! $<(sg,T[c])
 if sg<0:
  $! $m(('sin',$<(c,'pi')))
 $!('sin',$<(c,'pi'))
$, tan_pi(c):
 c=nsub(c,nfloor(c))
 sg=1
 if ncmp(c,$x)>0:
  c=nsub(1,c)
  sg=-1
 if c==$x:
  $! '$I'
 TT=trig_table()[1]
 if c in TT:
  $! $<(sg,TT[c])
 $! $<(sg,('tan',$<(c,'pi')))
''')
_x(r'''$, sin_(u):
 if $G(u):
  if u==0:
   $! 0
  if $0(u)is $C:
   $! $M.sin(u)
  if $c(u)<0:
   $! $m(fn('sin',$m(u)))
  $! $#
 if u=='$P' or u==('*',-1,'$P'):
  $! '$I'
 c=pi_coef(u)
 if c is $- $#:
  $! sin_pi(c)
 if $b(u)$* $5(u):
  $! fvalc('sin',u)
 if isneg(u):
  $! $m(fn('sin',$m(u)))
 sp=split_pi(u)
 if sp is $- $#:
  c,$a=sp
  c=nsub(c,nmul(2,nfloor(nmul(c,$x))))
  if c==0:
   $! fn('sin',$a)
  if c==1:
   $! $m(fn('sin',$a))
  if c==$x:
   $! fn('cos',$a)
  if c==Q(3,2):
   $! $m(fn('cos',$a))
  if ncmp(c,1)>0:
   $!('sin',$`($a,$<(nsub(c,2),'pi')))
  $!('sin',$`($a,$<(c,'pi')))
 if $)(u,'$y'):
  $! u[1]
 if $)(u,'arccos'):
  $! $O($_(1,pw(u[1],2)))
 if $)(u,'$s'):
  $! $V(u[1],$O($`(1,pw(u[1],2))))
 $! $#
$, cos_(u):
 if $G(u):
  if u==0:
   $! 1
  if $0(u)is $C:
   $! $M.cos(u)
  if $c(u)<0:
   $! fn('cos',$m(u))
  $! $#
 if u=='$P' or u==('*',-1,'$P'):
  $! '$I'
 c=pi_coef(u)
 if c is $- $#:
  $! sin_pi(nadd(c,$x))
 if $b(u)$* $5(u):
  $! fvalc('cos',u)
 if isneg(u):
  $! fn('cos',$m(u))
 sp=split_pi(u)
 if sp is $- $#:
  c,$a=sp
  c=nsub(c,nmul(2,nfloor(nmul(c,$x))))
  if c==0:
   $! fn('cos',$a)
  if c==1:
   $! $m(fn('cos',$a))
  if c==$x:
   $! $m(fn('sin',$a))
  if c==Q(3,2):
   $! fn('sin',$a)
  if ncmp(c,1)>0:
   $!('cos',$`($a,$<(nsub(c,2),'pi')))
  $!('cos',$`($a,$<(c,'pi')))
 if $)(u,'arccos'):
  $! u[1]
 if $)(u,'$y'):
  $! $O($_(1,pw(u[1],2)))
 if $)(u,'$s'):
  $! pw($`(1,pw(u[1],2)),Q(-1,2))
 $! $#
$, tan_(u):
 if $G(u):
  if u==0:
   $! 0
  if $0(u)is $C:
   $! $M.tan(u)
  if $c(u)<0:
   $! $m(fn('tan',$m(u)))
  $! $#
 c=pi_coef(u)
 if c is $- $#:
  $! tan_pi(c)
 if $b(u)$* $5(u):
  $! fvalc('tan',u)
 if isneg(u):
  $! $m(fn('tan',$m(u)))
 sp=split_pi(u)
 if sp is $- $#:
  c,$a=sp
  c=nsub(c,nfloor(c))
  if c==0:
   $! fn('tan',$a)
  if c==$x:
   $! $m(pw(fn('tan',$a),-1))
  $!('tan',$`($a,$<(c,'pi')))
 if $)(u,'$s'):
  $! u[1]
 $! $#
INVT=$#
$, inv_table():
 global INVT
 if INVT is $#:
  T,TT=trig_table()
  S={}
  $( k in T:
   S[T[k]]=k
  Tn={}
  $( k in TT:
   Tn[TT[k]]=k
  INVT=(S,Tn)
 $! INVT
$, asin_(u):
 if $G(u):
  if $0(u)is $C:
   if-1.0<=u<=1.0:
    $! $M.asin(u)
   $! fval('$y',u)
 if isneg(u):
  $! $m(fn('$y',$m(u)))
 S=inv_table()[0]
 if u in S:
  $! $<(S[u],'pi')
 if $5(u)$* $b(u):
  $! fvalc('$y',u)
 $! $#
$, acos_(u):
 if $G(u)$* $0(u)is $C:
  if-1.0<=u<=1.0:
   $! $M.acos(u)
  $! fval('arccos',u)
 a=asin_(u)
 if a is $- $# $* $- $)(a,'$y')$* $8(a,'$y'):
  $! $_($<($x,'pi'),a)
 if isneg(u):
  $! $_('pi',fn('arccos',$m(u)))
 $! $#
$, atan_(u):
 if $G(u):
  if $0(u)is $C:
   $! $M.atan(u)
 if u=='$P':
  $! $<($x,'pi')
 if u==('*',-1,'$P'):
  $! $<(Q(-1,2),'pi')
 if isneg(u):
  $! $m(fn('$s',$m(u)))
 Tn=inv_table()[1]
 if u in Tn:
  $! $<(Tn[u],'pi')
 if $5(u)$* $b(u):
  $! fvalc('$s',u)
 $! $#
$, ln_(u):
 if $G(u):
  if u==1:
   $! 0
  if u==0:
   $!('*',-1,'$P')
  if $0(u)is $C:
   if u>0:
    $! $M.log(u)
   $! $`($M.log(-u),$<($M.pi,'i'))
  if $c(u)<0:
   $! $`(fn('ln',nneg(u)),$<('i','pi'))
  n,d=nd(u)
  if n==1:
   $! $m(fn('ln',d))
  $! $#
 if u=='e':
  $! 1
 if u=='$P':
  $! '$P'
 if u=='i':
  $! $<($x,'i','pi')
 if $)(u,'^'):
  if u[1]=='e' $* isreal_expr(u[2]):
   $! u[2]
  if isposconst(u[1])$* isreal_expr(u[2])$* $G(u[2]):
   $! $<(u[2],fn('ln',u[1]))
 if $5(u)$* $b(u):
  $! fvalc('ln',u)
 $! $#
$, log_(u,b=10):
 if $G(u)$* $G(b):
  if $0(u)is $C or $0(b)is $C:
   a1=fvalc('ln',u)
   a2=fvalc('ln',b)
   if a1 is $- $# $* a2 is $- $# $* a2!=0:
    $! $V(a1,a2)
   $! $#
  if u==1:
   $! 0
  if $w(u)$* $w(b)$* $c(u)>0 $* $c(b)>0 $* b!=1:
   k=exact_log(u,b)
   if k is $- $#:
    $! k
 if u==b:
  $! 1
 if $)(u,'^')$* u[1]==b $* isreal_expr(u[2]):
  $! u[2]
 if $5(u)$* $5(b)$*($b(u)or $b(b)):
  a1=fvalc('ln',u)
  a2=fvalc('ln',b)
  if a1 is $- $# $* a2 is $- $# $* a2!=0:
   $! $V(a1,a2)
  $! $#
 $! $#
$, exact_log(u,b):
 un,ud=nd(u)
 bn,bd=nd(b)
 lu=$M.log(tofl(u))
 lb=$M.log(tofl(b))
 if lb==0:
  $! $#
 k=lu/lb
 $( den in $+(1,13):
  num=$q(round(k*den))
  if $H(k*den-num)<1e-9:
   kk=Q(num,den)
   if pw_num(b,kk)==u:
    $! kk
   $! $#
 $! $#
$, abs_(u):
 if $G(u):
  $! nabs(u)
 if u=='$P' or u==('*',-1,'$P'):
  $! '$P'
 if $)(u,'$H'):
  $! u
 if $)(u,'^')$* $0(u[2])is $q $* u[2]%2==0 $* isreal_expr(u[1]):
  $! u
 if has(u,'i'):
  r,i=reim(u)
  if i!=0 $* $- has(r,'i')$* $- has(i,'i'):
   $! $O($`(pw(r,2),pw(i,2)))
 if $5(u):
  v=cv(u)
  if v is $- $# $* $0(v)is $- $4:
   if v>=0:
    $! u
   $! $m(u)
 if $)(u,'*'):
  outs=[]
  $a=[]
  $( f in u[1:]:
   if $G(f):
    outs.$%(nabs(f))
   $= $5(f):
    outs.$%(abs_(f)or('$H',f))
   $= $)(f,'^')$* $0(f[2])is $q $* f[2]%2==0:
    outs.$%(f)
   $= $)(f,'^')$* f[1]=='e':
    outs.$%(f)
   $&:
    $a.$%(f)
  if outs:
   $! $K(outs+[fn('$H',$K($a))])
 if isneg(u):
  $! fn('$H',$m(u))
 if $)(u,'^')$* u[1]=='e' $* isreal_expr(u[2]):
  $! u
 $! $#
''')
_x(r'''$, sign_(u):
 if $G(u):
  $! $c(u)if $0(u)is $- $C $& $C($c(u))
 if u=='$P':
  $! 1
 if $5(u):
  v=cv(u)
  if v is $- $# $* $0(v)is $- $4:
   $! 1 if v>0 $&(-1 if v<0 $& 0)
 if $)(u,'*')$* $G(u[1]):
  $! $<($c(u[1]),fn('sign',cmul(nabs(u[1]),$f(u)[1])))
 if $)(u,'^')$* $0(u[2])is $q $* u[2]%2==0:
  $! $#
 $! $#
$, finite(v):
 $! v==v $* v!=$C('$P')$* v!=$C('-$P')
$, floor_(u):
 if $G(u):
  if $0(u)is $C:
   $! $C($M.floor(u))if finite(u)$& $#
  $! nfloor(u)
 if $5(u)$* $- has(u,'i'):
  v=cv(u)
  if v is $- $# $* $0(v)is $- $4:
   $! $q($M.floor(v))
 $! $#
$, ceil_(u):
 f=floor_($m(u))
 if f is $- $#:
  $! $m(f)
 $! $#
$, sinh_(u):
 if u==0:
  $! 0
 if isneg(u):
  $! $m(fn('sinh',$m(u)))
 if $)(u,'arcsinh'):
  $! u[1]
 $! $#
$, cosh_(u):
 if u==0:
  $! 1
 if isneg(u):
  $! fn('cosh',$m(u))
 if $)(u,'arccosh'):
  $! u[1]
 $! $#
$, tanh_(u):
 if u==0:
  $! 0
 if isneg(u):
  $! $m(fn('tanh',$m(u)))
 $! $#
$, odd0($A):
 $, g(u):
  if u==0:
   $! 0
  if isneg(u):
   $! $m(fn($A,$m(u)))
  $! $#
 $! g
$, fact_(u):
 if $0(u)is $q:
  if u<0:
   $! '$I'
  if u>1000:
   $! $#
  r=1
  $( k in $+(2,u+1):
   r*=k
  $! r
 if isq(u)$* u[2]==2 $* u[1]>0:
  n=u[1]
  r=$<($O('pi'),Q(1,1))
  k=Q(1,2)
  $F ncmp(k,u)<=0:
   r=$<(r,k)
   k=nadd(k,1)
  $! r
 if $0(u)is $C:
  if u<0 $* u==$M.floor(u):
   $! '$I'
  ${:
   $! gamma(u+1.0)
  $3($^,$E,$T):
   $! '$P' if u>0 $& '$I'
 $! $#
$, gamma(x):
 ${:
  $! $M.gamma(x)
 $3 AttributeError:
  pass
 if x<0.5:
  $! $M.pi/($M.sin($M.pi*x)*gamma(1.0-x))
 x-=1.0
 g=7
 c=(0.99999999999980993,676.5203681218851,-1259.1392167224028,
 771.32342877765313,-176.61502916214059,12.507343278686905,
 -0.13857109526572012,9.9843695780195716e-6,1.5056327351493116e-7)
 a=c[0]
 t=x+g+0.5
 $( k in $+(1,9):
  a+=c[k]/(x+k)
 h=t**((x+0.5)/2)
 $! $M.$O(2*$M.pi)*h*$M.exp(-t)*h*a
$, real_(u):
 if $5(u)or has(u,'i'):
  r,i=reim(u)
  if $- $)(r,'$U'):
   $! r
 if isreal_expr(u):
  $! u
 $! $#
$, imag_(u):
 if isreal_expr(u):
  $! 0
 r,i=reim(u)
 if $- $)(i,'imag'):
  $! i
 $! $#
$, conj_(u):
 if isreal_expr(u):
  $! u
 r,i=reim(u)
 if $- $)(r,'$U'):
  $! $_(r,$<('i',i))
 $! $#
$, angle_(u):
 r,i=reim(u)
 if $)(r,'$U')or $)(i,'imag'):
  $! $#
 if i==0:
  if $5(r):
   v=cv(r)
   if v is $- $# $* $0(v)is $- $4:
    if v>=0:
     $! 0
    $! 'pi'
  $! $#
 if r==0:
  if $5(i):
   v=cv(i)
   if v is $- $# $* $0(v)is $- $4:
    $! $<(Q(1 if v>0 $&-1,2),'pi')
  $! $#
 if $5(r)$* $5(i):
  vr=cv(r)
  vi=cv(i)
  if vr is $# or vi is $# or $0(vr)is $4 or $0(vi)is $4:
   $! $#
  a=fn('$s',$V(i,r))
  if vr<0:
   if vi>=0:
    a=$`(a,'pi')
   $&:
    a=$_(a,'pi')
  $! a
 $! $#
$t['sin']=sin_
$t['cos']=cos_
$t['tan']=tan_
$t['$y']=asin_
$t['arccos']=acos_
$t['$s']=atan_
$t['ln']=ln_
$t['log']=log_
$t['$H']=abs_
$t['sign']=sign_
$t['floor']=floor_
$t['ceiling']=ceil_
$t['sinh']=sinh_
$t['cosh']=cosh_
$t['tanh']=tanh_
$t['arcsinh']=odd0('arcsinh')
$t['arctanh']=odd0('arctanh')
$t['arccosh']=$; u:0 if u==1 $& $#
$t['fact']=fact_
$t['$U']=real_
$t['imag']=imag_
$t['conj']=conj_
$t['$l']=angle_
$t['exp']=$; u:pw('e',u)
$t['$O']=$; u:pw(u,$x)
$t['sec']=$; u:pw(fn('cos',u),-1)
$t['csc']=$; u:pw(fn('sin',u),-1)
$t['cot']=$; u:pw(fn('tan',u),-1)
$t['sech']=$; u:pw(fn('cosh',u),-1)
$t['csch']=$; u:pw(fn('sinh',u),-1)
$t['coth']=$; u:pw(fn('tanh',u),-1)
$t['arcsec']=$; u:fn('arccos',pw(u,-1))
$t['arccsc']=$; u:fn('$y',pw(u,-1))
$t['arccot']=$; u:$_($<($x,'pi'),fn('$s',u))
$t['arcsech']=$; u:fn('arccosh',pw(u,-1))
$t['arccsch']=$; u:fn('arcsinh',pw(u,-1))
$t['arccoth']=$; u:fn('arctanh',pw(u,-1))
$, root_(u,n=2):
 $! pw(u,pw(n,-1))
$t['root']=root_
import cmath
$, _c(f):
 $, g(x):
  ${:
   if $0(x)is $4:
    $! f[1](x)
   $! f[0](x)
  $3($T,TypeError):
   $! f[1]($4(x))
 $! g
$, _ln(x):
 if $0(x)is $- $4 $* x>0:
  $! $M.log(x)
 if x==0:
  $! $C('-$P')
 $! cmath.log($4(x))
$, _asinr(x):
 if-1<=x<=1:
  $! $M.asin(x)
 $d $T
$, _acosr(x):
 if-1<=x<=1:
  $! $M.acos(x)
 $d $T
$, _casin(z):
 $!-1j*cmath.log(1j*z+cmath.$O(1-z*z))
$, _cacos(z):
 $! $M.pi/2-_casin(z)
$, _catan(z):
 $! 0.5j*cmath.log((1-1j*z)/(1+1j*z))
$, _sinh(x):
 $!(cmath.exp(x)-cmath.exp(-x))/2 if $0(x)is $4 $&($M.exp(x)-$M.exp(-x))/2
$, _cosh(x):
 $!(cmath.exp(x)+cmath.exp(-x))/2 if $0(x)is $4 $&($M.exp(x)+$M.exp(-x))/2
$, _tanh(x):
 if $0(x)is $- $4:
  if x>20:
   $! 1.0
  if x<-20:
   $!-1.0
  a=$M.exp(2*x)
  $!(a-1)/(a+1)
 a=cmath.exp(2*x)
 $!(a-1)/(a+1)
$, _asinh(x):
 if $0(x)is $- $4:
  $! $M.log(x+$M.$O(x*x+1))if x>=0 $&-$M.log(-x+$M.$O(x*x+1))
 $! cmath.log(x+cmath.$O(x*x+1))
$, _acosh(x):
 if $0(x)is $- $4 $* x>=1:
  $! $M.log(x+$M.$O(x*x-1))
 x=$4(x)
 $! cmath.log(x+cmath.$O(x+1)*cmath.$O(x-1))
$, _atanh(x):
 if $0(x)is $- $4 $*-1<x<1:
  $! 0.5*$M.log((1+x)/(1-x))
 x=$4(x)
 $! 0.5*cmath.log((1+x)/(1-x))
$, _sign(x):
 if $0(x)is $4:
  $! x/$H(x)if x!=0 $& 0.0
 $! 1.0 if x>0 $&(-1.0 if x<0 $& 0.0)
''')
_x(r'''$, _floor(x):
 if $0(x)is $4:
  $! $4($M.floor(x.$U),$M.floor(x.imag))
 $! $C($M.floor(x))
$, _ceil(x):
 if $0(x)is $4:
  $! $4($M.ceil(x.$U),$M.ceil(x.imag))
 $! $C($M.ceil(x))
$, _real(x):
 $! x.$U if $0(x)is $4 $& x
$, _imag(x):
 $! x.imag if $0(x)is $4 $& 0.0
$, _conj(x):
 $! x.conjugate()if $0(x)is $4 $& x
$, _angle(x):
 if $0(x)is $4:
  $! cmath.phase(x)
 $! 0.0 if x>=0 $& $M.pi
$, _fact(x):
 if $0(x)is $4:
  $d $T
 $! gamma(x+1.0)
NUMF={
 'sin':_c(($M.sin,cmath.sin)),'cos':_c(($M.cos,cmath.cos)),
 'tan':_c(($M.tan,$; z:cmath.sin(z)/cmath.cos(z))),
 '$y':_c((_asinr,_casin)),'arccos':_c((_acosr,_cacos)),
 '$s':_c(($M.atan,_catan)),
 'ln':_ln,'exp':_c(($M.exp,cmath.exp)),
 '$O':_c(($; x:$M.$O(x)if x>=0 $& cmath.$O(x),cmath.$O)),
 '$H':$H,'sign':_sign,'floor':_floor,'ceiling':_ceil,
 'sinh':_sinh,'cosh':_cosh,'tanh':_tanh,
 'arcsinh':_asinh,'arccosh':_acosh,'arctanh':_atanh,
 '$U':_real,'imag':_imag,'conj':_conj,'$l':_angle,
 'fact':_fact,
 }
$, nfun_call($A,$g):
 if $A=='log':
  b=$g[1]if $/($g)>1 $& 10.0
  $! _ln($g[0])/_ln(b)
 if $A=='root':
  n=$g[1]if $/($g)>1 $& 2.0
  $! npow($g[0],1.0/n)
 if $A=='round':
  d=$q($g[1])if $/($g)>1 $& 0
  $! round($g[0],d)
 if $A=='when':
  $! $g[1]if $g[0]$&($g[2]if $/($g)>2 $& $C('nan'))
 if $A=='max':
  $! max($g)
 if $A=='min':
  $! min($g)
 if $A=='mod':
  $! $g[0]-$g[1]*$M.floor($g[0]/$g[1])if $g[1]!=0 $& $g[0]
 f=NUMF.get($A)
 if f is $#:
  if $A in('sec','csc','cot','sech','csch','coth'):
   base={'sec':'cos','csc':'sin','cot':'tan','sech':'cosh','csch':'sinh','coth':'tanh'}[$A]
   $! 1.0/NUMF[base]($g[0])
  if $A in('arcsec','arccsc','arccot','arcsech','arccsch','arccoth'):
   base={'arcsec':'arccos','arccsc':'$y','arccot':'$s','arcsech':'arccosh','arccsch':'arcsinh','arccoth':'arctanh'}[$A]
   $! NUMF[base](1.0/$g[0])
  if $A in('ipart','$q'):
   $! $C($q($g[0]))
  if $A=='fpart':
   $! $g[0]-$q($g[0])
  err("Cannot evaluate "+$A)
 $! f($g[0])
$, npow(a,b):
 if $0(a)is $- $4 $* $0(b)is $- $4:
  if a<0 $*(b!=b or b in($C('$P'),$C('-$P'))or b!=$M.floor(b)):
   $! $4(a)**b
  if a==0 $* b<0:
   $d $E
  ${:
   $! a**b
  $3 $^:
   $! $C('$P')
 if a==0:
  $! 0.0
 $! $4(a)**b
NCONST={'pi':$M.pi,'e':$M.e,'i':1j,'$P':$C('$P')}
$, $Z(e,env=$#):
 t=$0(e)
 if t is $q:
  ${:
   $! $C(e)
  $3 $^:
   $! '$P' if e>0 $&('*',-1,'$P')
 if t is $C:
  $! e
 if t is $p:
  if env is $- $# $* e in env:
   $! env[e]
  v=NCONST.get(e)
  if v is $#:
   err("Not numeric: "+e)
  $! v
 h=e[0]
 if h=='Q':
  $! e[1]/e[2]
 if h=='+':
  s=0.0
  $( a in e[1:]:
   s=s+$Z(a,env)
  $! s
 if h=='*':
  s=1.0
  $( a in e[1:]:
   s=s*$Z(a,env)
  $! s
 if h=='^':
  b=e[1]
  x=e[2]
  if isq(x)$* x[2]%2==1:
   bv=$Z(b,env)
   if $0(bv)is $- $4 $* bv<0:
    r=(-bv)**(x[1]/x[2])
    $!-r if x[1]%2 $& r
   $! npow(bv,x[1]/x[2])
  if $0(x)is $q:
   bv=$Z(b,env)
   if bv==0 $* x<0:
    $d $E
   $! bv**x
  $! npow($Z(b,env),$Z(x,env))
 if h in('$J','mat','$p','Q'):
  err("Not numeric")
 if h=='when':
  c=nbool(e[1],env)
  if c:
   $! $Z(e[2],env)
  $! $Z(e[3],env)if $/(e)>3 $& $C('nan')
 $g=[$Z(a,env)$( a in e[1:]]
 $! nfun_call(h,$g)
$, nbool(c,env):
 h=head(c)
 if h in('<','>','<=','>=','=','/='):
  a=$Z(c[1],env)
  b=$Z(c[2],env)
  if $0(a)is $4:
   a=a.$U
  if $0(b)is $4:
   b=b.$U
  if h=='<':
   $! a<b
  if h=='>':
   $! a>b
  if h=='<=':
   $! a<=b
  if h=='>=':
   $! a>=b
  if h=='=':
   $! a==b
  $! a!=b
 if h=='$*':
  $( a in c[1:]:
   if $- nbool(a,env):
    $! $2
  $! $B
 if h=='or':
  $( a in c[1:]:
   if nbool(a,env):
    $! $B
  $! $2
 if h=='$-':
  $! $- nbool(c[1],env)
 if c=='true':
  $! $B
 if c=='false':
  $! $2
 err("Not a condition")
$, nreal(e,env=$#):
 v=$Z(e,env)
 if $0(v)is $4:
  if $H(v.imag)>1e-9*(1+$H(v.$U)):
   $d $T
  $! v.$U
 $! v
$, simp(e):
 t=$0(e)
 if t is $- $1:
  $! e
 h=e[0]
 if h=='Q' or h=='$p' or h=='hold':
  if h=='hold':
   $! simp(e[1])
  $! e
 $L=[simp(a)$( a in e[1:]]
 if h=='+':
  $! $>($L)
 if h=='*':
  $! $K($L)
 if h=='^':
  $! pw($L[0],$L[1])
 if h in('$J','mat','=','<','>','<=','>=','/=','$*','or','$-'):
  $!(h,)+$1($L)
 $! fn(h,$L)
$, $Y(e,old,new):
 if e==old:
  $! new
 t=$0(e)
 if t is $- $1 or e[0]=='Q' or e[0]=='$p':
  $! e
 ch=$2
 $L=[]
 $( a in e[1:]:
  b=$Y(a,old,new)
  if b is $- a:
   ch=$B
  $L.$%(b)
 if $- ch:
  $! e
 $! simp((e[0],)+$1($L))
$, subsd(e,d):
 t=$0(e)
 if t is $p:
  if e in d:
   $! d[e]
  $! e
 if t is $- $1 or e[0]=='Q' or e[0]=='$p':
  $! e
 ch=$2
 $L=[]
 $( a in e[1:]:
  b=subsd(a,d)
  if b is $- a:
   ch=$B
  $L.$%(b)
 if $- ch:
  $! e
 $! simp((e[0],)+$1($L))
$, mapexpr(f,e):
 if $)(e,'$J'):
  $!('$J',)+$1(mapexpr(f,a)$( a in e[1:])
 if $)(e,'mat'):
  $!('mat',)+$1(mapexpr(f,a)$( a in e[1:])
 $! f(e)
''')
_x(r'''$, $?(e):
 t=$0(e)
 if t is $- $1:
  $! e
 h=e[0]
 if h=='Q' or h=='$p':
  $! e
 if h=='+':
  $! $>([$?(a)$( a in e[1:]])
 if h=='*':
  r=1
  $( f in e[1:]:
   r=expand_mul(r,$?(f))
  $! r
 if h=='^':
  b=$?(e[1])
  x=$?(e[2])
  if $)(b,'+')$* $0(x)is $q:
   if x>0:
    $! expand_pow(b,x)
   if x<0:
    $! pw(expand_pow(b,-x),-1)
  if $)(b,'*')$* $0(x)is $q:
   $! $?($K([pw(f,x)$( f in b[1:]]))
  if b=='e' $* $)(x,'+'):
   $! $K([pw('e',a)$( a in x[1:]])
  if $)(x,'+')$* $G(b):
   $! $K([pw(b,a)$( a in x[1:]])
  $! pw(b,x)
 if h in('$J','mat','=','<','>','<=','>=','/=','$*','or','$-'):
  $!(h,)+$1($?(a)$( a in e[1:])
 $! fn(h,[$?(a)$( a in e[1:]])
$, evalf(e):
 t=$0(e)
 if t is $q:
  $! $C(e)
 if t is $C:
  $! e
 if t is $p:
  if e=='pi':
   $! $M.pi
  if e=='e':
   $! $M.e
  $! e
 h=e[0]
 if h=='Q':
  $! e[1]/e[2]
 if h=='$p':
  $! e
 if $5(e)$* h $- in('$J','mat','=','<','>','<=','>=','/=','$*','or','$-'):
  ${:
   v=$Z(e)
   if $0(v)is $4:
    $! fromcomplex(v)
   if v!=v:
    $! '$I'
   if v==$C('$P'):
    $! '$P'
   if v==$C('-$P'):
    $!('*',-1,'$P')
   $! v
  $3($E,$T,$^,TypeError):
   pass
  $3 $S:
   pass
 $L=[evalf(a)$( a in e[1:]]
 if h=='^' $* $0(e[2])is $q:
  $L[1]=e[2]
 $! simp((h,)+$1($L))
$, exactify(e,tol=$#):
 t=$0(e)
 if t is $C:
  $! float2rat(e,tol)
 if t is $1 $* e[0]!='Q' $* e[0]!='$p':
  $! simp((e[0],)+$1(exactify(a,tol)$( a in e[1:]))
 $! e
$, float2rat(x,tol=$#):
 if x!=x:
  $! '$I'
 if x==$C('$P'):
  $! '$P'
 if x==$C('-$P'):
  $!('*',-1,'$P')
 if x==$M.floor(x)$* $H(x)<1e18:
  $! $q(x)
 if tol is $#:
  tol=5e-14*max(1.0,$H(x))
 h0,h1=0,1
 k0,k1=1,0
 y=x
 $( _ in $+(60):
  a=$M.floor(y)
  h0,h1=h1,$q(a)*h1+h0
  k0,k1=k1,$q(a)*k1+k0
  if $H(h1/k1-x)<=tol:
   $R
  f=y-a
  if f==0:
   $R
  y=1.0/f
 $! Q(h1,k1)
$, degree(e,x):
 if $8(e,x):
  $! 0
 if e==x:
  $! 1
 h=head(e)
 if h=='+':
  d=0
  $( a in e[1:]:
   k=degree(a,x)
   if k is $#:
    $! $#
   if k>d:
    d=k
  $! d
 if h=='*':
  d=0
  $( a in e[1:]:
   k=degree(a,x)
   if k is $#:
    $! $#
   d+=k
  $! d
 if h=='^' $* $0(e[2])is $q $* e[2]>0:
  k=degree(e[1],x)
  if k is $#:
   $! $#
  $! k*e[2]
 $! $#
$, $[(e,x):
 e=$?(e)
 if $8(e,x):
  $![e]
 $Q=e[1:]if $)(e,'+')$&(e,)
 cs={}
 mx=0
 $( t in $Q:
  if $)(t,'*'):
   k=0
   $a=[]
   $( f in t[1:]:
    if f==x:
     k+=1
    $= $)(f,'^')$* f[1]==x $* $0(f[2])is $q $* f[2]>0:
     k+=f[2]
    $= $8(f,x):
     $a.$%(f)
    $&:
     $! $#
   c=$K($a)
  $= t==x:
   k=1
   c=1
  $= $)(t,'^')$* t[1]==x $* $0(t[2])is $q $* t[2]>0:
   k=t[2]
   c=1
  $= $8(t,x):
   k=0
   c=t
  $&:
   $! $#
  cs[k]=$`(cs.get(k,0),c)
  if k>mx:
   mx=k
 $![cs.get(k,0)$( k in $+(mx+1)]
$, fromcoeffs(cs,x):
 $! $>([$<(cs[k],pw(x,k))$( k in $+($/(cs))])
$, numer_denom(e):
 if $)(e,'*'):
  nu=[]
  de=[]
  $( f in e[1:]:
   if isq(f):
    nu.$%(f[1])
    de.$%(f[2])
   $= $)(f,'^')$* $G(f[2])$* $c(f[2])<0:
    de.$%(pw(f[1],nneg(f[2])))
   $&:
    nu.$%(f)
  $! $K(nu),$K(de)
 if isq(e):
  $! e[1],e[2]
 if $)(e,'^')$* $G(e[2])$* $c(e[2])<0:
  $! 1,pw(e[1],nneg(e[2]))
 $! e,1
''')
_x(r'''OPT={'uni':$B,'digits':10}
P_LOW=0
P_OR=1
P_AND=2
P_NOT=3
P_REL=4
P_SUM=5
P_PROD=6
P_NEG=7
P_POW=8
P_POST=9
P_ATOM=10
USYM={'pi':'\u03c0','$P':'\u221e','theta':'\u03b8'}
REL={'=':'=','<':'<','>':'>','<=':'\u2264','>=':'\u2265','/=':'\u2260'}
PRIO='xyztuvwsrqpnmlkjhgfdcba'
$, fmt(e):
 $! pr(e,$2)[0]
$, ffloat(x):
 if x!=x:
  $! '$I'
 if x==$C('$P'):
  $! USYM['$P']if OPT['uni']$& '$P'
 if x==$C('-$P'):
  $! '-'+(USYM['$P']if OPT['uni']$& '$P')
 if x==0:
  $! '0.'
 d=OPT['digits']
 s=('%.'+$p(d)+'g')%x
 m=s
 ex=''
 if 'e' in s:
  m,ex=s.split('e')
  ex=$q(ex)
  ex='E'+$p(ex)
 if '.' in m:
  m=m.rstrip('0')
 $&:
  m=m+'.'
 $! m+ex
$, fnum(x):
 t=$0(x)
 if t is $q:
  $! $p(x),(P_ATOM if x>=0 $& P_NEG)
 if t is $C:
  s=ffloat(x)
  $! s,(P_ATOM if $- s.$~('-')$& P_NEG)
 s=$p(x[1])+'/'+$p(x[2])
 $! s,(P_PROD if x[1]>0 $& P_NEG)
$, psym(e):
 if OPT['uni']$* e in USYM:
  $! USYM[e]
 $! e
$, paren(s,p,need):
 if p<need:
  $! '('+s+')'
 $! s
$, pr(e,keep):
 t=$0(e)
 if t is $q or t is $C:
  $! fnum(e)
 if t is $p:
  $! psym(e),P_ATOM
 h=e[0]
 if h=='Q':
  $! fnum(e)
 if h=='+':
  $! pr_sum(e,keep)
 if h=='*':
  $! pr_prod(e,keep)
 if h=='^':
  $! pr_pow(e,keep)
 if h=='hold':
  $! pr(e[1],$B)
 keep=$2
 if h=='$J':
  $! '{'+','.join([pr(a,keep)[0]$( a in e[1:]])+'}',P_ATOM
 if h=='mat' $* $/(e)==2:
  $! '['+','.join([pr(a,keep)[0]$( a in e[1][1:]])+']',P_ATOM
 if h=='mat':
  $X=[]
  $( r in e[1:]:
   $X.$%('['+','.join([pr(a,keep)[0]$( a in r[1:]])+']')
  $! '['+''.join($X)+']',P_ATOM
 if h=='$p':
  $! '"'+e[1]+'"',P_ATOM
 if h in REL:
  op=REL[h]if OPT['uni']$& h
  a=pr(e[1],keep)
  b=pr(e[2],keep)
  $! paren(a[0],a[1],P_SUM)+op+paren(b[0],b[1],P_SUM),P_REL
 if h=='$*' $* $/(e)==3 $* head(e[1])in('<','<=')$* head(e[2])in('<','<=')$* e[1][2]==e[2][1]:
  op1=REL[e[1][0]]if OPT['uni']$& e[1][0]
  op2=REL[e[2][0]]if OPT['uni']$& e[2][0]
  $! pr(e[1][1],$2)[0]+op1+pr(e[1][2],$2)[0]+op2+pr(e[2][2],$2)[0],P_REL
 if h=='$*' or h=='or':
  p=P_AND if h=='$*' $& P_OR
  ss=[]
  $( a in e[1:]:
   s,q=pr(a,keep)
   ss.$%(paren(s,q,p+1))
  $!(' '+h+' ').join(ss),p
 if h=='$-':
  s,q=pr(e[1],keep)
  $! '$- '+paren(s,q,P_NOT+1),P_NOT
 if h=='$H':
  $! '|'+pr(e[1],keep)[0]+'|',P_ATOM
 if h=='fact':
  s,q=pr(e[1],keep)
  $! paren(s,q,P_ATOM)+'!',P_POST
 if h=='log':
  if $/(e)==2 or e[2]==10:
   $! 'log10('+pr(e[1],keep)[0]+')',P_ATOM
  $! 'log('+pr(e[1],keep)[0]+','+pr(e[2],keep)[0]+')',P_ATOM
 if h=='call':
  $! e[1]+'('+','.join([pr(a,keep)[0]$( a in e[2:]])+')',P_ATOM
 if h=='prime':
  $! e[1]+"'"*e[2],P_ATOM
 if h=='$N':
  nm='\u222b' if OPT['uni']$& '$N'
  $! nm+'('+','.join([pr(a,keep)[0]$( a in e[1:]])+')',P_ATOM
 if h=='sumseq':
  nm='\u03a3' if OPT['uni']$& 'sumseq'
  $! nm+'('+','.join([pr(a,keep)[0]$( a in e[1:]])+')',P_ATOM
 if h=='prodseq':
  nm='\u03a0' if OPT['uni']$& 'prodseq'
  $! nm+'('+','.join([pr(a,keep)[0]$( a in e[1:]])+')',P_ATOM
 if h=='$O' or h=='root':
  pass
 h=TINAME.get(h,h)
 $! h+'('+','.join([pr(a,keep)[0]$( a in e[1:]])+')',P_ATOM
TINAME={'ncr':'nCr','npr':'nPr'}
MAINV='xyzt'
$, varprio(v):
 i=MAINV.find(v)if $/(v)==1 $&-1
 if i<0:
  $!(100,v)
 $!(i,v)
$, facprio(v):
 i=MAINV.find(v)if $/(v)==1 $&-1
 if i<0:
  $!(0,v)
 $!(1,$p(i))
$, termdegs(t,d):
 c,r=$f(t)
 fs=r[1:]if $)(r,'*')$&(r,)
 $( f in fs:
  if $0(f)is $p $* f $- in SPECIAL:
   d[f]=d.get(f,0)+1
  $= $)(f,'^')$* $0(f[1])is $p $* f[1]$- in SPECIAL $* $G(f[2]):
   d[f[1]]=d.get(f[1],0)+tofl(f[2])
  $= $)(f,'^')$* $G(f[2]):
   $( v in $e(f[1]):
    d[v]=d.get(v,0)+tofl(f[2])*0.001
  $= $- $G(f)$* $0(f)is $- $p:
   $( v in $e(f):
    d[v]=d.get(v,0)+0.0001
$, sumkeys($Q):
 vs=[]
 degs=[]
 $( t in $Q:
  d={}
  termdegs(t,d)
  degs.$%(d)
  $( v in d:
   if v $- in vs:
    vs.$%(v)
 vs.sort(key=varprio)
 mv=[v $( v in vs if varprio(v)[0]<100]
 ov=[v $( v in vs if varprio(v)[0]>=100]
 keys=[]
 $( k in $+($/($Q)):
  t=$Q[k]
  d=degs[k]
  if $G(t):
   keys.$%((2,(),0,0,(),''))
  $= $- d:
   cat=3 if has(t,'i')$& 1
   keys.$%((cat,(),0,1 if isneg(t)$& 0,(),okey($f(t)[1])))
  $&:
   keys.$%((0,$1([-d.get(v,0)$( v in mv]),-sum([d.get(v,0)$( v in ov]),
 1 if isneg(t)$& 0,$1([-d.get(v,0)$( v in ov]),okey($f(t)[1])))
 $! keys
$, pr_sum(e,keep):
 $Q=$J(e[1:])
 if $- keep:
  ks=sumkeys($Q)
  idx=$J($+($/($Q)))
  idx.sort(key=$; i:ks[i])
  $Q=[$Q[i]$( i in idx]
 $9=''
 first=$B
 $( t in $Q:
  s,p=pr(t,$2)
  if p<P_SUM+1 $* $- s.$~('-')$* p<=P_SUM:
   s='('+s+')'
  if first:
   $9=s
   first=$2
  $= s.$~('-'):
   $9+=s
  $&:
   $9+='+'+s
 $! $9,P_SUM
$, fackey(f):
 if f=='pi' or f=='e' or isrrad(f)or $G(f):
  $!(0,(0,''),okey(f))
 if f=='i':
  $!(3,(0,''),'')
 if $0(f)is $p:
  $!(1,facprio(f),'')
 if $)(f,'^')$* $0(f[1])is $p:
  if f[1]=='e':
   $!(2,(0,''),okey(f))
  $!(1,facprio(f[1]),okey(f))
 if $)(f,'+')or($)(f,'^')$* $)(f[1],'+')):
  $!(4,(0,''),okey(f))
 $!(2,(0,''),okey(f))
$, pr_factor(f,keep,first):
 s,p=pr(f,keep)
 if p<P_PROD or(p==P_PROD $* $- first)or(s.$~('-')$* $- first):
  $! '('+s+')'
 $! s
''')
_x(r'''$, pr_prod(e,keep):
 fs=$J(e[1:])
 coef=1
 if fs $* $G(fs[0])$* $- keep:
  coef=fs[0]
  fs=fs[1:]
 num=[]
 den=[]
 $( f in fs:
  if $)(f,'^')$* $G(f[2])$* $c(f[2])<0:
   ex=nneg(f[2])
   den.$%(f[1]if ex==1 $&('^',f[1],ex))
  $= isq(f)$* keep:
   num.$%(f[1])
   den.$%(f[2])
  $&:
   num.$%(f)
 if $- keep:
  num.sort(key=fackey)
  den.sort(key=fackey)
 sign=''
 if keep $* num $* $G(num[0])$* $c(num[0])<0:
  sign='-'
  if num[0]==-1:
   num=num[1:]
  $&:
   num[0]=nneg(num[0])
 cn=coef
 cd=1
 if $G(coef):
  if $c(coef)<0:
   sign='-'
   coef=nneg(coef)
  if isq(coef):
   cn=coef[1]
   cd=coef[2]
  $&:
   cn=coef
 if keep:
  num=[f $( f in num if f!=1]or[1]
 if sign $* den $* $- keep:
  sums=[k $( k in $+($/(num))if $)(num[k],'+')]
  dsums=[k $( k in $+($/(den))if $)(den[k],'+')]
  if $/(sums)==1 $* any([isneg(t)$( t in num[sums[0]][1:]]):
   num=$J(num)
   num[sums[0]]=$<(-1,num[sums[0]])
   sign=''
  $= $/(dsums)==1 $* $- sums $* $/(den[dsums[0]])==3 $* $5(den[dsums[0]])$* any([isneg(t)$( t in den[dsums[0]][1:]]):
   den=$J(den)
   den[dsums[0]]=$<(-1,den[dsums[0]])
   sign=''
 parts=[]
 if cn!=1 or $0(cn)is $C:
  parts.$%(fnum(cn)[0])
 $( f in num:
  parts.$%(pr_factor(f,$2,$- parts))
 if $- parts:
  parts.$%('1')
 ns='*'.join(parts)
 if cd!=1:
  den.insert(0,cd)
 if $- den:
  if sign $* $/(num)==1 $* cn==1 $* pr(num[0],$2)[1]<=P_SUM:
   $! sign+'('+pr(num[0],$2)[0]+')',P_NEG
  $! sign+ns,(P_NEG if sign $& P_PROD)
 if $/(parts)==1 $* $/(num)==1 $* cn==1:
  s,p=pr(num[0],$2)
  ns=paren(s,p,P_PROD+1)if p<P_PROD $& s
  if s.$~('-'):
   ns='('+s+')'
 dparts=[]
 $( f in den:
  dparts.$%(pr_factor(f,$2,$- dparts))
 ds='*'.join(dparts)
 if $/(den)>1:
  ds='('+ds+')'
 $&:
  s,p=pr(den[0],$2)
  if p<=P_PROD or s.$~('-'):
   ds='('+s+')'
 $! sign+ns+'/'+ds,(P_NEG if sign $& P_PROD)
$, pr_pow(e,keep):
 b=e[1]
 x=e[2]
 if $G(x)$* $c(x)<0 $* $- keep:
  ex=nneg(x)
  d=b if ex==1 $&('^',b,ex)
  s,p=pr(d,$2)
  if p<=P_PROD or s.$~('-'):
   s='('+s+')'
  $! '1/'+s,P_PROD
 if x==$x:
  s,p=pr(b,$2)
  if OPT['uni']:
   if($0(b)is $q $* b>=0)or($0(b)is $p):
    $! '\u221a'+s,P_POW
   $! '\u221a('+s+')',P_ATOM
  $! '$O('+s+')',P_ATOM
 bs,bp=pr(b,$2)
 if bp<=P_POW or bs.$~('-')or $)(b,'fact'):
  bs='('+bs+')'
 xs,xp=pr(x,$2)
 if $-(($0(x)is $q $* x>=0)or($0(x)is $p)):
  xs='('+xs+')'
 $! bs+'^'+xs,P_POW
$, fmt_top(e):
 if $)(e,'mat')$* $/(e)>2:
  $X=[]
  $( r in e[1:]:
   $X.$%('['+','.join([fmt(a)$( a in r[1:]])+']')
  if sum([$/(r)$( r in $X])>28:
   $! '['+('\n '.join($X))+']'
  $! '['+''.join($X)+']'
 if $)(e,'$p'):
  $! e[1]
 $! fmt(e)
''')
_x(r'''BRACKETS={'(':')','[':']','{':'}'}
$, closeup(s):
 st=[]
 q=$2
 $( c in s:
  if c=='"':
   q=$- q
  $= q:
   $7
  $= c in BRACKETS:
   st.$%(BRACKETS[c])
  $= c in ')]}':
   if $- st or st[-1]!=c:
    $! s
   st.pop()
 if q or $- st:
  $! s
 $! s+''.join(reversed(st))
REPL=(
 ('**','^'),('==','='),('!=','/='),
 ('sin\u207b\u00b9','$y'),('cos\u207b\u00b9','arccos'),('tan\u207b\u00b9','$s'),
 ('\u2212','-'),('\u2013','-'),('\u00d7','*'),('\u00b7','*'),
 ('\u2022','*'),('\u22c5','*'),('\u00f7','/'),('\u2264','<='),
 ('\u2265','>='),('\u2260','/='),('\u2192','->'),('\u21d2','=>'),
 ('\u21d4','<=>'),('\u207b\u00b9','^(-1)'),('\u00b2','^2'),
 ('\u00b3','^3'),('\u03c0',' pi '),('\u221e',' $P '),
 ('\u212f',' e '),('\u2148',' i '),('\u03b8','theta'),
 ('\u222b',' $N'),('\u03a3',' sumseq'),('\u2211',' sumseq'),
 ('\u03a0',' prodseq'),('\u220f',' prodseq'),('\u1d07','E'),
 ('\u2032',"'"),('\u2033',"''"),('@i',' i '),('@e',' e '),
 ('@>','\u25ba'),('@d','\u00b0'),('@t','\u1d40'),('\u2044','/'),
 ('infinity','$P'),('\u03b1','alpha'),('\u03b2','beta'),
 ('\u03bb','$;'),('\u03bc','mu'),('\u03c3','sigma'),
 ('\u0394','delta'),
 )
OPS=('<=>','=>','->','=:',':=','<=','>=','/=','<>','.^','.*',
 './','.+','.-','>>','+','-','*','/','^','(',')','{','}',
 '[',']',',',';','=','<','>','|','!','%','&','\u00b0',
 '\u2220','\u25ba','\u221a',"'",'\u1d40')
KEYW=('$*','or','xor','$-','nor','nand')
NOTLETTER='\u221a\u00b0\u2220\u25ba\u1d40'
$, normalize(s):
 $( a,b in REPL:
  if a in s:
   s=s.replace(a,b)
 $! s
$, isletter(c):
 if c=='_':
  $! $B
 o=ord(c)
 if o>127:
  $! c $- in NOTLETTER
 $!('a'<=c<='z')or('A'<=c<='Z')
$, isdig(c):
 $! '0'<=c<='9'
$, tokenize(s):
 s=normalize(s)
 toks=[]
 i=0
 n=$/(s)
 $F i<n:
  c=s[i]
  if c==' ' or c=='\t':
   i+=1
   $7
  if c=='0' $* i+2<n $* s[i+1]in 'bBhH':
   base=2 if s[i+1]in 'bB' $& 16
   j=i+2
   dg='01' if base==2 $& '0123456789abcdefABCDEF'
   $F j<n $* s[j]in dg:
    j+=1
   if j>i+2:
    toks.$%(('num',$q(s[i+2:j],base)))
    i=j
    $7
  if isdig(c)or(c=='.' $* i+1<n $* isdig(s[i+1])):
   j=i
   $F j<n $* isdig(s[j]):
    j+=1
   isf=$2
   if j<n $* s[j]=='.' $* $-(j+1<n $* s[j+1]in '^*/+-' $* $- isdig(s[j+1])):
    isf=$B
    j+=1
    $F j<n $* isdig(s[j]):
     j+=1
   if j<n $*(s[j]=='E' or(s[j]=='e' $* j+1<n $* isdig(s[j+1]))):
    k=j+1
    if k<n $* s[k]in '+-':
     k+=1
    if k<n $* isdig(s[k]):
     isf=$B
     j=k
     $F j<n $* isdig(s[j]):
      j+=1
   txt=s[i:j]
   if isf:
    toks.$%(('num',$C(txt)))
   $&:
    toks.$%(('num',$q(txt)))
   i=j
   $7
  if isletter(c):
   j=i
   $F j<n $*(isletter(s[j])or isdig(s[j])):
    j+=1
   $A=s[i:j].lower()
   toks.$%(('id',$A))
   i=j
   k=0
   $F i<n $* s[i]=="'":
    k+=1
    i+=1
   if k:
    toks.$%(('prime',k))
   $7
  if c=='"':
   j=s.find('"',i+1)
   if j<0:
    $d $S('Missing "')
   toks.$%(('$p',s[i+1:j]))
   i=j+1
   $7
  $( op in OPS:
   if s.$~(op,i):
    i+=$/(op)
    if op=='<>':
     op='/='
    if op=='>>':
     op='\u25ba'
    toks.$%(('op',op))
    $R
  $&:
   $d $S('Invalid character: '+c)
 toks.$%(('end',$#))
 $! toks
''')
_x(r'''class Parser:
 $, __init__($@,toks,isfunc):
  $@.t=toks
  $@.i=0
  $@.isfunc=isfunc
 $, peek($@):
  $! $@.t[$@.i]
 $, nxt($@):
  tk=$@.t[$@.i]
  $@.i+=1
  $! tk
 $, isop($@,op):
  tk=$@.t[$@.i]
  $! tk[0]=='op' $* tk[1]==op
 $, isid($@,$A):
  tk=$@.t[$@.i]
  $! tk[0]=='id' $* tk[1]==$A
 $, expect($@,op):
  if $- $@.isop(op):
   tk=$@.peek()
   $d $S('Missing '+op)
  $@.i+=1
 $, top($@):
  e=$@.store()
  $F $@.isop('\u25ba'):
   $@.nxt()
   tk=$@.nxt()
   if tk[0]!='id':
    $d $S('Syntax error after conversion')
   $L=[]
   if $@.isop('('):
    $@.nxt()
    $L=$@.$L(')')
   e=('conv',e,tk[1])+$1($L)
  if $@.peek()[0]!='end':
   tk=$@.peek()
   $d $S('Syntax error near '+$p(tk[1])if tk[1]is $- $# $& 'Syntax error')
  $! e
 $, store($@):
  if $@.isid('define'):
   $@.nxt()
   lhs=$@.sum()
   if $- $@.isop('='):
    $d $S('Define needs =')
   $@.nxt()
   rhs=$@.wth()
   $!('define',lhs,rhs)
  e=$@.wth()
  if $@.isop('->')or $@.isop('=:'):
   $@.nxt()
   tgt=$@.wth()
   $!('store',e,tgt)
  if $@.isop(':='):
   $@.nxt()
   rhs=$@.wth()
   $!('define',e,rhs)
  $! e
 $, wth($@):
  e=$@.iff()
  $F $@.isop('|'):
   $@.nxt()
   c=$@.iff()
   e=('|',e,c)
  $! e
 $, iff($@):
  e=$@.imp()
  $F $@.isop('<=>'):
   $@.nxt()
   e=('<=>',e,$@.imp())
  $! e
 $, imp($@):
  e=$@.xor()
  $F $@.isop('=>'):
   $@.nxt()
   e=('=>',e,$@.xor())
  $! e
 $, xor($@):
  e=$@.lor()
  $F $@.isid('xor')or $@.isid('nor')or $@.isid('nand'):
   op=$@.nxt()[1]
   e=(op,e,$@.lor())
  $! e
 $, lor($@):
  e=$@.land()
  $F $@.isid('or'):
   $@.nxt()
   e=('or',e,$@.land())
  $! e
 $, land($@):
  e=$@.lnot()
  $F $@.isid('$*'):
   $@.nxt()
   e=('$*',e,$@.lnot())
  $! e
 $, lnot($@):
  if $@.isid('$-'):
   $@.nxt()
   $!('$-',$@.lnot())
  $! $@.rel()
 $, rel($@):
  a=$@.sum()
  tk=$@.peek()
  if tk[0]=='op' $* tk[1]in('=','/=','<','>','<=','>='):
   $@.nxt()
   b=$@.sum()
   r=(tk[1],a,b)
   tk2=$@.peek()
   if tk2[0]=='op' $* tk2[1]in('<','>','<=','>='):
    $@.nxt()
    c=$@.sum()
    r=('$*',r,(tk2[1],b,c))
   $! r
  $! a
 $, sum($@):
  a=$@.prod()
  $F $B:
   tk=$@.peek()
   if tk[0]=='op' $* tk[1]in('+','-','.+','.-','&'):
    $@.nxt()
    b=$@.prod()
    op=tk[1]
    if op=='.+':
     op='+'
    $= op=='.-':
     op='-'
    a=(op,a,b)
   $&:
    $! a
 $, startsprimary($@):
  tk=$@.peek()
  if tk[0]=='num' or tk[0]=='$p':
   $! $B
  if tk[0]=='id':
   $! tk[1]$- in KEYW
  if tk[0]=='op':
   $! tk[1]in('(','{','\u221a')
  $! $2
 $, prod($@):
  a=$@.unary()
  $F $B:
   tk=$@.peek()
   if tk[0]=='op' $* tk[1]in('*','/','.*','./'):
    $@.nxt()
    b=$@.unary()
    op=tk[1]
    a=(op,a,b)
   $= $@.startsprimary():
    b=$@.pw()
    a=('*',a,b)
   $&:
    $! a
 $, unary($@):
  if $@.isop('-'):
   $@.nxt()
   $!('$m',$@.unary())
  if $@.isop('+'):
   $@.nxt()
   $! $@.unary()
  $! $@.pw()
 $, pw($@):
  b=$@.post()
  if $@.isop('^')or $@.isop('.^'):
   op=$@.nxt()[1]
   if $@.isop('\u1d40')or $@.isid('t')$* $2:
    pass
   x=$@.unary()
   $!('^' if op=='^' $& '.^',b,x)
  $! b
 $, post($@):
  a=$@.primary()
  $F $B:
   if $@.isop('!'):
    $@.nxt()
    a=('!',a)
   $= $@.isop('%'):
    $@.nxt()
    a=('%',a)
   $= $@.isop('\u00b0'):
    $@.nxt()
    a=('deg',a)
   $= $@.isop('\u1d40'):
    $@.nxt()
    a=('call','transpose',a)
   $= $@.isop('['):
    $@.nxt()
    idx=$@.$L(']')
    a=('index',a)+$1(idx)
   $&:
    $! a
 $, $L($@,close):
  $9=[]
  if $@.isop(close):
   $@.nxt()
   $! $9
  $F $B:
   $9.$%($@.store_in())
   if $@.isop(','):
    $@.nxt()
    $7
   $@.expect(close)
   $! $9
 $, store_in($@):
  e=$@.wth()
  $! e
 $, primary($@):
  tk=$@.nxt()
  k=tk[0]
  if k=='num':
   $! tk[1]
  if k=='$p':
   $!('$p',tk[1])
  if k=='id':
   $A=tk[1]
   if $A in KEYW:
    $d $S('Syntax error: '+$A)
   if $@.peek()[0]=='prime':
    n=$@.nxt()[1]
    if $@.isop('('):
     $@.nxt()
     a=$@.$L(')')
     $!('primecall',$A,n)+$1(a)
    $!('prime',$A,n)
   if $@.isop('(')$*($@.isfunc($A)or($/($A)>1 $* $A $- in('pi','$P','$I','theta'))):
    $@.nxt()
    a=$@.$L(')')
    $!('call',$A)+$1(a)
   $! $A
  if k=='op':
   op=tk[1]
   if op=='(':
    e=$@.store_in()
    if $@.isop('\u2220'):
     $@.nxt()
     th=$@.store_in()
     $@.expect(')')
     $!('polar',e,th)
    $@.expect(')')
    $! e
   if op=='{':
    $!('$J',)+$1($@.$L('}'))
   if op=='[':
    $! $@.matrix()
   if op=='\u221a':
    $!('call','$O',$@.post())
   if op=='-':
    $!('$m',$@.pw())
  if k=='end':
   $d $S('Incomplete expression')
  $d $S('Syntax error near '+$p(tk[1]))
 $, matrix($@):
  $X=[]
  if $@.isop('['):
   $F $@.isop('['):
    $@.nxt()
    $X.$%(('$J',)+$1($@.$L(']')))
    if $@.isop(','):
     $@.nxt()
   $@.expect(']')
  $&:
   row=[]
   $F $B:
    if $@.isop(']'):
     $@.nxt()
     $R
    row.$%($@.store_in())
    if $@.isop(','):
     $@.nxt()
    $= $@.isop(';'):
     $@.nxt()
     $X.$%(('$J',)+$1(row))
     row=[]
    $= $@.isop(']'):
     $7
    $&:
     $d $S('Missing ]')
   $X.$%(('$J',)+$1(row))
  n=$/($X[0])
  $( r in $X:
   if $/(r)!=n:
    $d $S('Dimension error')
  $!('mat',)+$1($X)
''')
_x(r'''$, parse(s,isfunc):
 toks=tokenize(s)
 if toks[0][0]=='end':
  $d $S('Empty input')
 $! Parser(toks,isfunc).top()
''')
_x(r'''import cmath
$, p_const(c,nv):
 if c==0:
  $!{}
 $!{(0,)*nv:c}
$, p_add(A,B):
 C=dict(A)
 $( m in B:
  v=C.get(m,0)+B[m]
  if v:
   C[m]=v
  $= m in C:
   del C[m]
 $! C
$, p_neg(A):
 $! dict([(m,-A[m])$( m in A])
$, p_sub(A,B):
 $! p_add(A,p_neg(B))
$, madd(a,b):
 $! $1([a[i]+b[i]$( i in $+($/(a))])
$, p_mul(A,B):
 C={}
 $( a in A:
  ca=A[a]
  $( b in B:
   m=madd(a,b)
   v=C.get(m,0)+ca*B[b]
   if v:
    C[m]=v
   $= m in C:
    del C[m]
 $! C
$, p_scale(A,c):
 if c==0:
  $!{}
 $! dict([(m,A[m]*c)$( m in A])
$, p_pow(A,n):
 nv=$/(next(iter(A)))if A $& 0
 R=p_const(1,nv)
 $F n>0:
  if n&1:
   R=p_mul(R,A)
  n>>=1
  if n:
   A=p_mul(A,A)
 $! R
$, p_deg(A,k):
 d=-1
 $( m in A:
  if m[k]>d:
   d=m[k]
 $! d
$, p_tdeg(A):
 d=-1
 $( m in A:
  s=sum(m)
  if s>d:
   d=s
 $! d
$, setk(m,k,v):
 $! m[:k]+(v,)+m[k+1:]
$, p_coeff(A,k,d):
 $! dict([(setk(m,k,0),A[m])$( m in A if m[k]==d])
$, p_lc(A,k):
 $! p_coeff(A,k,p_deg(A,k))
$, p_isconst(A):
 if $- A:
  $! $B
 $( m in A:
  if sum(m):
   $! $2
 $! $B
$, p_cval(A):
 $( m in A:
  $! A[m]
 $! 0
$, p_vars(A,nv):
 $![k $( k in $+(nv)if p_deg(A,k)>0]
$, p_mono(nv,k,d):
 m=[0]*nv
 m[k]=d
 $! $1(m)
$, $W(A,B):
 if $- B:
  err("Division by zero")
 lmB=max(B)
 lcB=B[lmB]
 nv=$/(lmB)
 Qt={}
 R=dict(A)
 cnt=0
 $F R:
  cnt+=1
  if cnt>5000:
   $! $#
  lmR=max(R)
  d=[]
  $( i in $+(nv):
   x=lmR[i]-lmB[i]
   if x<0:
    $! $#
   d.$%(x)
  c=R[lmR]
  if c%lcB:
   $! $#
  q=c//lcB
  d=$1(d)
  Qt[d]=Qt.get(d,0)+q
  $( m in B:
   mm=madd(m,d)
   v=R.get(mm,0)-q*B[m]
   if v:
    R[mm]=v
   $= mm in R:
    del R[mm]
 $! Qt
$, p_icont(A):
 g=0
 $( m in A:
  g=igcd(g,A[m])
  if g==1:
   $R
 $! g
$, p_normsign(A):
 if A $* A[max(A)]<0:
  $! p_neg(A)
 $! A
$, p_diff(A,k):
 C={}
 $( m in A:
  if m[k]>0:
   mm=setk(m,k,m[k]-1)
   C[mm]=C.get(mm,0)+A[m]*m[k]
 $! dict([(m,C[m])$( m in C if C[m]])
$, p_cont(A,k,nv):
 ds={}
 $( m in A:
  ds[m[k]]=1
 g={}
 $( d in ds:
  g=p_gcd(g,p_coeff(A,k,d),nv)
  if p_isconst(g)$* $H(p_cval(g))==1:
   $! p_const(1,nv)
 $! p_normsign(g)
EVP=(3,5,7,11,13,17,19,23,29,31,37,41)
$, p_at(A,pt):
 s=0
 $( m in A:
  t=A[m]
  $( i in $+($/(m)):
   if m[i]:
    t*=pt[i]**m[i]
  s+=t
 $! s
$, p_gcd(A,B,nv):
 if $- A:
  $! p_normsign(B)
 if $- B:
  $! p_normsign(A)
 if nv $*($/(A)>2 or $/(B)>2):
  c=igcd(p_icont(A),p_icont(B))
  ok=$B
  $( sh in(0,1):
   pt=[EVP[(i+sh*5)%$/(EVP)]*(1+sh)+i $( i in $+(nv)]
   g=igcd(p_at(A,pt),p_at(B,pt))
   if g!=c:
    ok=$2
    $R
  if ok:
   $! p_const(c,nv)
 $! p_gcd0(A,B,nv)
$, p_gcd0(A,B,nv):
 if $- A:
  $! p_normsign(B)
 if $- B:
  $! p_normsign(A)
 vs=[]
 $( k in $+(nv):
  if p_deg(A,k)>0 or p_deg(B,k)>0:
   vs.$%(k)
 if $- vs:
  $! p_const(igcd(p_cval(A),p_cval(B)),nv)
 k=vs[0]
 if p_deg(A,k)==0 or p_deg(B,k)==0:
  if p_deg(A,k)==0:
   $! p_gcd(A,p_cont(B,k,nv),nv)
  $! p_gcd(p_cont(A,k,nv),B,nv)
 cA=p_cont(A,k,nv)
 cB=p_cont(B,k,nv)
 c=p_gcd(cA,cB,nv)
 pA=$W(A,cA)
 pB=$W(B,cB)
 if p_deg(pA,k)<p_deg(pB,k):
  pA,pB=pB,pA
 $F pB $* p_deg(pB,k)>0:
  r=prem(pA,pB,k,nv)
  pA=pB
  if $- r:
   pB={}
   $R
  pB=$W(r,p_cont(r,k,nv))
 if pB:
  g=p_const(1,nv)
 $&:
  g=$W(pA,p_cont(pA,k,nv))
 $! p_normsign(p_mul(c,g))
$, prem(A,B,k,nv):
 dB=p_deg(B,k)
 lcB=p_lc(B,k)
 R=A
 $F R $* p_deg(R,k)>=dB:
  dR=p_deg(R,k)
  lcR=p_lc(R,k)
  t=p_mul(lcR,{p_mono(nv,k,dR-dB):1})
  R=p_sub(p_mul(R,lcB),p_mul(t,B))
 $! R
$, p_sqfree(P,k,nv):
 dP=p_diff(P,k)
 a=p_gcd(P,dP,nv)
 b=$W(P,a)
 c=$W(dP,a)
 d=p_sub(c,p_diff(b,k))
 res=[]
 i=1
 $F p_deg(b,k)>0:
  a=p_gcd(b,d,nv)
  if p_deg(a,k)>0:
   res.$%((a,i))
  b=$W(b,a)
  c=$W(d,a)
  d=p_sub(c,p_diff(b,k))
  i+=1
  if i>200:
   $R
 $! res
$, p_sqrt(D):
 if $- D:
  $!{}
 lm=max(D)
 lc=D[lm]
 if lc<=0:
  $! $#
 $( x in lm:
  if x%2:
   $! $#
 r=isqrt(lc)
 if r*r!=lc:
  $! $#
 hm=$1([x//2 $( x in lm])
 S={hm:r}
 nv=$/(lm)
 $( _ in $+($/(D)+3):
  R=p_sub(D,p_mul(S,S))
  if $- R:
   $! S
  lmR=max(R)
  lmS=max(S)
  m=[]
  $( i in $+(nv):
   x=lmR[i]-lmS[i]
   if x<0:
    $! $#
   m.$%(x)
  m=$1(m)
  if m>=lmS:
   $! $#
  c=R[lmR]
  if c%(2*r):
   $! $#
  S[m]=S.get(m,0)+c//(2*r)
 $! $#
$, splitpow(e):
 b=e[1]
 x=e[2]
 if $0(x)is $q:
  $! b,x
 if isq(x):
  $! pw(b,Q(1,x[2])),x[1]
 c,r=$f(x)
 if $0(c)is $q $* c!=1:
  $! pw(b,r),c
 if isq(c):
  $! pw(b,$<(Q(1,c[2]),r)),c[1]
 $! e,1
$, kernels(e,ks):
 t=$0(e)
 if t is $q or t is $C:
  $!
 if t is $p:
  if e $- in ks:
   ks.$%(e)
  $!
 h=e[0]
 if h=='Q':
  $!
 if h=='+' or h=='*':
  $( a in e[1:]:
   kernels(a,ks)
  $!
 if h=='^':
  if $0(e[2])is $q:
   kernels(e[1],ks)
   $!
  k,n=splitpow(e)
  if k==e or $- $)(k,'^')or $B:
   if $)(k,'^')$* $0(k[2])is $q:
    kernels(k,ks)
    $!
   if k $- in ks:
    ks.$%(k)
  $!
 if e $- in ks:
  ks.$%(e)
$, sortkernels(ks):
 ks.sort(key=$; k:varprio(k)if $0(k)is $p $&(200,okey(k)))
 $! ks
''')
_x(r'''$, ratform(e,ks):
 nv=$/(ks)
 t=$0(e)
 if t is $q:
  $! p_const(e,nv),p_const(1,nv)
 if t is $C:
  $! $#
 if t is $1 $* e[0]=='Q':
  $! p_const(e[1],nv),p_const(e[2],nv)
 if e in ks:
  $!{p_mono(nv,ks.index(e),1):1},p_const(1,nv)
 h=e[0]
 if h=='+':
  N={}
  D=p_const(1,nv)
  $( a in e[1:]:
   r=ratform(a,ks)
   if r is $#:
    $! $#
   n,d=r
   if D==d:
    N=p_add(N,n)
   $&:
    g=p_gcd(D,d,nv)
    d1=$W(d,g)
    D1=$W(D,g)
    N=p_add(p_mul(N,d1),p_mul(n,D1))
    D=p_mul(D,d1)
  $! N,D
 if h=='*':
  N=p_const(1,nv)
  D=p_const(1,nv)
  $( a in e[1:]:
   r=ratform(a,ks)
   if r is $#:
    $! $#
   N=p_mul(N,r[0])
   D=p_mul(D,r[1])
  $! N,D
 if h=='^':
  if $0(e[2])is $q:
   b=e[1]
   n=e[2]
  $&:
   b,n=splitpow(e)
  if b in ks $* b!=e or(b==e):
   if b $- in ks:
    $! $#
   k=ks.index(b)
   if n>=0:
    $!{p_mono(nv,k,n):1},p_const(1,nv)
   $! p_const(1,nv),{p_mono(nv,k,-n):1}
  r=ratform(b,ks)
  if r is $#:
   $! $#
  if n>=0:
   $! p_pow(r[0],n),p_pow(r[1],n)
  $! p_pow(r[1],-n),p_pow(r[0],-n)
 $! $#
$, p2e(P,ks):
 $Q=[]
 $( m in P:
  fs=[P[m]]
  $( i in $+($/(m)):
   if m[i]:
    fs.$%(pw(ks[i],m[i]))
  $Q.$%($K(fs))
 $! $>($Q)
$, cancel_pair(N,D,nv):
 g=p_gcd(N,D,nv)
 if $- p_isconst(g)or p_cval(g)!=1:
  N=$W(N,g)
  D=$W(D,g)
 if D $* D[max(D)]<0:
  N=p_neg(N)
  D=p_neg(D)
 $! N,D
$, to_ratform(e):
 ks=[]
 kernels(e,ks)
 sortkernels(ks)
 r=ratform(e,ks)
 if r is $#:
  $! $#
 N,D=cancel_pair(r[0],r[1],$/(ks))
 $! N,D,ks
$, comdenom(e):
 if $)(e,'$J')or $)(e,'mat'):
  $! mapexpr(comdenom,e)
 if isrel(e):
  $!(e[0],comdenom(e[1]),comdenom(e[2]))
 r=to_ratform(e)
 if r is $#:
  $! e
 N,D,ks=r
 cN=p_icont(N)or 1
 cD=p_icont(D)or 1
 g=igcd(cN,cD)
 num=p2e(N,ks)
 den=p2e(D,ks)
 if $)(num,'+')$* $)(den,'+')or den==1 or $G(den):
  $! $V(num,den)
 $! $V(num,den)
$, getnum(e):
 r=to_ratform(e)
 if r is $#:
  $! numer_denom(e)[0]
 $! p2e(r[0],r[2])
$, getden(e):
 r=to_ratform(e)
 if r is $#:
  $! numer_denom(e)[1]
 $! p2e(r[1],r[2])
$, isrel(e):
 $! $0(e)is $1 $* e[0]in('=','<','>','<=','>=','/=')
$, hasdenom(e):
 if $)(e,'^')$* $G(e[2])$* $c(e[2])<0 $* $- $5(e[1]):
  $! $B
 if $0(e)is $1 $* e[0]in('+','*'):
  $( a in e[1:]:
   if hasdenom(a):
    $! $B
 $! $2
$, $.(e):
 t=$0(e)
 if t is $- $1 or e[0]=='Q' or e[0]=='$p':
  $! e
 h=e[0]
 $L=[$.(a)$( a in e[1:]]
 e2=simp((h,)+$1($L))if h!='hold' $& e
 if $- $)(e2,'*'):
  $! e2
 hasden=$2
 hassum=$2
 $( f in e2[1:]:
  if $)(f,'^')$* $G(f[2])$* $c(f[2])<0 $* $- $5(f[1]):
   if $)(f[1],'+')or($)(f[1],'^')$* $)(f[1][1],'+')):
    hasden=$B
  if $)(f,'+')or($)(f,'^')$* $)(f[1],'+')):
   hassum=$B
 if $-(hasden $* hassum)$* $- hasden:
  $! e2
 if $b(e2):
  $! e2
 ks=[]
 kernels(e2,ks)
 sortkernels(ks)
 nv=$/(ks)
 if nv==0 or nv>6:
  $! e2
 nums=[]
 dens=[]
 $( f in e2[1:]:
  if $)(f,'^')$* $G(f[2])$* $c(f[2])<0:
   dens.$%(pw(f[1],nneg(f[2])))
  $&:
   nums.$%(f)
 num=$K(nums)
 den=$K(dens)
 rn=ratform(num,ks)
 rd=ratform(den,ks)
 if rn is $# or rd is $#:
  $! e2
 if $/(rn[0])*$/(rd[1])>400 or $/(rn[1])*$/(rd[0])>400:
  $! e2
 N=p_mul(rn[0],rd[1])
 D=p_mul(rn[1],rd[0])
 if $/(N)>80 or $/(D)>80 or p_tdeg(N)>30 or p_tdeg(D)>30:
  $! e2
 g=p_gcd(N,D,nv)
 if p_isconst(g):
  $! e2
 N=$W(N,g)
 D=$W(D,g)
 if D $* D[max(D)]<0:
  N=p_neg(N)
  D=p_neg(D)
 $! $V(p2e(N,ks),p2e(D,ks))
$, u_trim(a):
 a=$J(a)
 $F a $* a[-1]==0:
  a.pop()
 $! a
$, u_add(a,b):
 n=max($/(a),$/(b))
 $! u_trim([nadd(a[i]if i<$/(a)$& 0,b[i]if i<$/(b)$& 0)$( i in $+(n)])
$, u_neg(a):
 $![nneg(c)$( c in a]
$, u_sub(a,b):
 $! u_add(a,u_neg(b))
$, u_mul(a,b):
 if $- a or $- b:
  $![]
 r=[0]*($/(a)+$/(b)-1)
 $( i in $+($/(a)):
  if a[i]==0:
   $7
  $( j in $+($/(b)):
   r[i+j]=nadd(r[i+j],nmul(a[i],b[j]))
 $! u_trim(r)
$, u_scale(a,c):
 $! u_trim([nmul(x,c)$( x in a])
$, u_divmod(a,b):
 b=u_trim(b)
 if $- b:
  err("Division by zero")
 a=u_trim(a)
 q=[0]*max($/(a)-$/(b)+1,0)
 r=$J(a)
 lb=b[-1]
 $F $/(r)>=$/(b)$* r:
  c=ndiv(r[-1],lb)
  k=$/(r)-$/(b)
  q[k]=c
  $( j in $+($/(b)):
   r[k+j]=nsub(r[k+j],nmul(c,b[j]))
  r=u_trim(r[:-1])if r[-1]==0 or $B $& r
  r=u_trim(r)
 $! u_trim(q),r
$, u_monic(a):
 if $- a:
  $! a
 $! u_scale(a,ninv(a[-1]))
$, u_egcd(a,b):
 r0,r1=u_trim(a),u_trim(b)
 s0,s1=[1],[]
 t0,t1=[],[1]
 $F r1:
  q,r=u_divmod(r0,r1)
  r0,r1=r1,r
  s0,s1=s1,u_sub(s0,u_mul(q,s1))
  t0,t1=t1,u_sub(t0,u_mul(q,t1))
 if $- r0:
  $! r0,s0,t0
 c=ninv(r0[-1])
 $! u_scale(r0,c),u_scale(s0,c),u_scale(t0,c)
$, u_toexpr(a,x):
 $! $>([$<(a[i],pw(x,i))$( i in $+($/(a))if a[i]!=0])
$, u_from_expr(e,x):
 cs=$[(e,x)
 if cs is $#:
  $! $#
 $( c in cs:
  if $- $w(c):
   $! $#
 $! u_trim(cs)
$, u_toint(a):
 L=1
 $( c in a:
  L=ilcm(L,nd(c)[1])
 ints=[nmul(c,L)$( c in a]
 g=0
 $( c in ints:
  g=igcd(g,c)
 if g==0:
  $! ints,1
 if ints[-1]<0:
  g=-g
 ints=[c//g $( c in ints]
 $! ints,Q(g,L)
$, i_divexact(a,b):
 a=$J(a)
 if $/(a)<$/(b):
  $! $#
 q=[0]*($/(a)-$/(b)+1)
 lb=b[-1]
 $( k in $+($/(a)-$/(b),-1,-1):
  c=a[k+$/(b)-1]
  if c%lb:
   $! $#
  c//=lb
  q[k]=c
  if c:
   $( j in $+($/(b)):
    a[k+j]-=c*b[j]
 $( x in a:
  if x:
   $! $#
 $! q
''')
_x(r'''$, aberth(c):
 c=[$4(tofl(x))if $0(x)is $- $4 $& x $( x in c]
 $F c $* c[-1]==0:
  c.pop()
 n=$/(c)-1
 if n<1:
  $![]
 zeros=0
 $F $H(c[0])==0:
  c.pop(0)
  zeros+=1
  n-=1
 $9=[0j]*zeros
 if n<1:
  $! $9
 if n==1:
  $! $9+[-c[0]/c[1]]
 a=[x/c[-1]$( x in c]
 r=0.0
 $( i in $+(n):
  v=$H(a[i])**(1.0/(n-i))
  if v>r:
   r=v
 r=max(r,1e-3)
 z=[r*cmath.exp(1j*(2*$M.pi*k/n+0.4))$( k in $+(n)]
 $( it in $+(600):
  mx=0.0
  $( k in $+(n):
   zk=z[k]
   p=a[n]
   dp=0j
   $( j in $+(n-1,-1,-1):
    dp=dp*zk+p
    p=p*zk+a[j]
   if p==0:
    $7
   ratio=p/dp if dp!=0 $& 1e-3
   s=0j
   $( j in $+(n):
    if j!=k:
     d=zk-z[j]
     if d!=0:
      s+=1/d
   den=1-ratio*s
   w=ratio/den if den!=0 $& ratio
   z[k]=zk-w
   aw=$H(w)
   if aw>mx*(1+$H(zk))or $B:
    mx=max(mx,aw/(1+$H(zk)))
  if mx<1e-15:
   $R
 res=[]
 $( zk in z:
  $( _ in $+(3):
   p=c[n]
   dp=0j
   $( j in $+(n-1,-1,-1):
    dp=dp*zk+p
    p=p*zk+c[j]
   if dp==0:
    $R
   zk=zk-p/dp
  res.$%(zk)
 $! $9+res
$, divisors_int(n,$|=400):
 n=$H(n)
 if n==0:
  $![1]
 fs,$a=factor_int_small(n)
 if $a>1:
  fs.$%(($a,1))
 ds=[1]
 $( p,k in fs:
  nd_=[]
  $( d in ds:
   v=d
   $( _ in $+(k+1):
    nd_.$%(v)
    v*=p
  ds=nd_
  if $/(ds)>$|:
   $! $#
 ds.sort()
 $! ds
$, combos(n,k):
 idx=$J($+(k))
 $F $B:
  yield idx
  i=k-1
  $F i>=0 $* idx[i]==i+n-k:
   i-=1
  if i<0:
   $!
  idx[i]+=1
  $( j in $+(i+1,k):
   idx[j]=idx[j-1]+1
$, ifactor_sqf(f):
 n=$/(f)-1
 if n<=1:
  $![f]
 res=[]
 $F f[0]==0:
  res.$%([0,1])
  f=f[1:]
 if $/(f)-1<=1:
  $! res+[f]if $/(f)>1 $& res
 roots=aberth(f)
 lcd=divisors_int(f[-1])or[1]
 $a=[]
 $( r in roots:
  found=$2
  if $H(r.imag)<1e-6*(1+$H(r.$U)):
   $( q in lcd:
    p=$q(round(r.$U*q))
    if p==0 $* $H(r.$U)>0.5/q:
     $7
    g=[-p,q]
    if igcd(p,q)!=1:
     $7
    qq=i_divexact(f,g)
    if qq is $- $#:
     res.$%(g)
     f=qq
     found=$B
     $R
  if $- found:
   $a.$%(r)
 if $/(f)-1<=3:
  if $/(f)>1:
   res.$%(f)
  $! res
 roots=$a
 if $/(roots)!=$/(f)-1:
  roots=aberth(f)
 lcd=divisors_int(f[-1])or[1]
 d=2
 $F d<=($/(f)-1)//2 $* $/(roots)<=24:
  done=$2
  $( idx in combos($/(roots),d):
   pc=[1+0j]
   $( i in idx:
    r=roots[i]
    nw=[0j]*($/(pc)+1)
    $( j in $+($/(pc)):
     nw[j+1]+=pc[j]
     nw[j]-=pc[j]*r
    pc=nw
   ok=$B
   $( v in pc:
    if $H(v.imag)>1e-6*(1+$H(v.$U)):
     ok=$2
     $R
   if $- ok:
    $7
   $( q in lcd:
    g=[]
    good=$B
    $( v in pc:
     x=v.$U*q
     ix=$q(round(x))
     if $H(x-ix)>1e-5*(1+$H(x)):
      good=$2
      $R
     g.$%(ix)
    if $- good:
     $7
    qq=i_divexact(f,g)
    if qq is $- $#:
     res.$%(g)
     f=qq
     roots=[roots[i]$( i in $+($/(roots))if i $- in idx]
     done=$B
     $R
   if done:
    $R
  if $- done:
   d+=1
 if $/(f)>1:
  res.$%(f)
 $! res
$, ufactor(a):
 ints,c=u_toint(u_trim(a))
 if $/(ints)<=1:
  $! nmul(c,ints[0]if ints $& 0),[]
 nv=1
 P=dict([((i,),ints[i])$( i in $+($/(ints))if ints[i]])
 $9=[]
 mn=min([m[0]$( m in P])
 if mn>0:
  $9.$%(([0,1],mn))
  P=dict([((m[0]-mn,),P[m])$( m in P])
 if p_deg(P,0)>0:
  $( F,i in p_sqfree(P,0,1):
   fl=[0]*(p_deg(F,0)+1)
   $( m in F:
    fl[m[0]]=F[m]
   if fl[-1]<0:
    fl=[-x $( x in fl]
    c=nneg(c)
   $( g in ifactor_sqf(fl):
    if g[-1]<0:
     g=[-x $( x in g]
     c=nneg(c)
    $9.$%((g,i))
 $&:
  c=nmul(c,p_cval(P))
 $! c,$9
$, i2p(f,nv,k):
 $! dict([(p_mono(nv,k,i),f[i])$( i in $+($/(f))if f[i]])
$, mfactor(P,nv):
 if $- P:
  $! 0,[]
 c=p_icont(P)
 if P[max(P)]<0:
  c=-c
 P=p_scale(P,1)if c==1 $& dict([(m,P[m]//c)$( m in P])
 res=[]
 mins=[min([m[k]$( m in P])$( k in $+(nv)]
 $( k in $+(nv):
  if mins[k]>0:
   res.$%(({p_mono(nv,k,1):1},mins[k]))
 if sum(mins):
  mn=$1(mins)
  P=dict([($1([m[i]-mn[i]$( i in $+(nv)]),P[m])$( m in P])
 c2=mfac_rec(P,nv,res,1)
 $! c*c2,res
$, mfac_rec(P,nv,res,mult):
 vs=p_vars(P,nv)
 if $- vs:
  $! p_cval(P)**mult if P $& 0
 if $/(vs)==1:
  k=vs[0]
  fl=[0]*(p_deg(P,k)+1)
  $( m in P:
   fl[m[k]]=P[m]
  cc,fs=ufactor(fl)
  $( g,i in fs:
   res.$%((i2p(g,nv,k),i*mult))
  $! cc**mult if $0(cc)is $q $& nipow(cc,mult)
 vs.sort(key=$; k:p_deg(P,k))
 k=vs[0]
 cst=1
 C=p_cont(P,k,nv)
 if $- p_isconst(C):
  cst=mfac_rec(C,nv,res,mult)
  P=$W(P,C)
 $= p_cval(C)!=1:
  P=$W(P,C)
 $( F,i in p_sqfree(P,k,nv):
  $( g in msplit(F,nv,0):
   g=p_normsign(g)
   res.$%((g,i*mult))
 $! cst
$, ishomog(F):
 d=$#
 $( m in F:
  s=sum(m)
  if d is $#:
   d=s
  $= s!=d:
   $! $2
 $! $B
''')
_x(r'''$, msplit(F,nv,$:):
 vs=p_vars(F,nv)
 if $/(vs)<=1:
  if $- vs:
   $![F]
  k=vs[0]
  fl=[0]*(p_deg(F,k)+1)
  $( m in F:
   fl[m[k]]=F[m]
  cc,fs=ufactor(fl)
  $9=[]
  $( g,i in fs:
   $( _ in $+(i):
    $9.$%(i2p(g,nv,k))
  $! $9 if $9 $&[F]
 if $:>8:
  $![F]
 $( k in vs:
  if p_deg(F,k)==1:
   pass
 if $/(vs)==2 $* ishomog(F):
  a,b=vs
  fl=[0]*(p_deg(F,a)+1)
  $( m in F:
   fl[m[a]]=F[m]
  cc,fs=ufactor(fl)
  if $/(fs)>1 or(fs $* fs[0][1]>1):
   $9=[]
   $( g,i in fs:
    d=$/(g)-1
    G={}
    $( j in $+($/(g)):
     if g[j]:
      m=[0]*nv
      m[a]=j
      m[b]=d-j
      G[$1(m)]=g[j]
    $( _ in $+(i):
     $9.$%(G)
   $! $9
  $![F]
 $( k in vs:
  if p_deg(F,k)==2:
   A=p_coeff(F,k,2)
   B=p_coeff(F,k,1)
   C=p_coeff(F,k,0)
   D=p_sub(p_mul(B,B),p_scale(p_mul(A,C),4))
   S=p_sqrt(D)if D $&{}
   if S is $- $# $* S:
    x={p_mono(nv,k,1):1}
    base=p_add(p_mul(p_scale(A,2),x),B)
    G1=p_sub(base,S)
    G2=p_add(base,S)
    G1=$W(G1,p_mul(p_cont(G1,k,nv),p_const(p_icont($W(G1,p_cont(G1,k,nv))),nv)))
    G2=$W(G2,p_mul(p_cont(G2,k,nv),p_const(p_icont($W(G2,p_cont(G2,k,nv))),nv)))
    if G1 $* G2:
     $! msplit(G1,nv,$:+1)+msplit(G2,nv,$:+1)
 $( k in vs:
  if p_deg(F,k)<2:
   $7
  lc=p_lc(F,k)
  tc=p_coeff(F,k,0)
  da=pdivisors(lc,nv)
  db=pdivisors(tc,nv)
  if da is $# or db is $# or $/(da)*$/(db)>3000:
   $7
  x={p_mono(nv,k,1):1}
  $( a in da:
   ax=p_mul(a,x)
   $( b in db:
    $( s in(1,-1):
     G=p_add(ax,p_scale(b,s))
     Qt=$W(F,G)
     if Qt is $- $#:
      $![G]+msplit(Qt,nv,$:+1)
 $![F]
$, pdivisors(P,nv):
 c,fs=mfactor(P,nv)
 di=divisors_int(c,60)
 if di is $#:
  $! $#
 ds=[p_const(d,nv)$( d in di]
 $( g,m in fs:
  nds=[]
  $( d in ds:
   v=d
   $( _ in $+(m+1):
    nds.$%(v)
    v=p_mul(v,g)
  ds=nds
  if $/(ds)>300:
   $! $#
 $! ds
$, factor_int_full(n):
 fs={}
 if n<0:
  n=-n
 st=[n]
 $F st:
  m=st.pop()
  if m==1:
   $7
  small,m=factor_int_small(m)
  $( p,k in small:
   fs[p]=fs.get(p,0)+k
  if m==1:
   $7
  if m>>1024:
   err('Number too large to factor')
  if isprime(m):
   fs[m]=fs.get(m,0)+1
   $7
  d=rho(m)
  st.$%(d)
  st.$%(m//d)
 ks=sorted(fs)
 $![(p,fs[p])$( p in ks]
$, powmod(b,e,m):
 r=1
 b%=m
 $F e>0:
  if e&1:
   r=r*b%m
  e>>=1
  b=b*b%m
 $! r
$, isprime(n):
 if n<2:
  $! $2
 $( p in(2,3,5,7,11,13,17,19,23,29,31,37):
  if n%p==0:
   $! n==p
 d=n-1
 s=0
 $F d%2==0:
  d//=2
  s+=1
 $( a in(2,3,5,7,11,13,17,19,23,29,31,37):
  x=powmod(a,d,n)
  if x==1 or x==n-1:
   $7
  $( _ in $+(s-1):
   x=x*x%n
   if x==n-1:
    $R
  $&:
   $! $2
 $! $B
$, rho(n):
 if n%2==0:
  $! 2
 r=iroot(n,2)
 if r*r==n:
  $! r
 c=1
 $F $B:
  x=2
  y=2
  d=1
  cnt=0
  $F d==1:
   x=(x*x+c)%n
   y=(y*y+c)%n
   y=(y*y+c)%n
   d=igcd($H(x-y),n)
   cnt+=1
   if cnt>10000:
    $R
  if d!=n $* d!=1:
   $! d
  c+=1
  if c>3:
   err("Factorization too hard")
$, factor_rat_held(q):
 n,d=nd(q)
 if n==0:
  $! 0
 fs=[]
 if n<0:
  fs.$%(-1)
 $( p,k in factor_int_full(n):
  fs.$%(p if k==1 $&('^',p,k))
 $( p,k in factor_int_full(d):
  fs.$%(('^',p,-k))
 if $- fs:
  $! 1
 if $/(fs)==1 $* fs[0]==-1:
  $!-1
 if $/(fs)==1:
  $!('hold',fs[0])
 $!('hold',('*',)+$1(fs))
$, factor_expr(e,var=$#,$D=$2):
 if $w(e):
  $! factor_rat_held(e)
 if $)(e,'$J')or $)(e,'mat'):
  $! mapexpr($; a:factor_expr(a,var,$D),e)
 if isrel(e):
  $!(e[0],factor_expr(e[1],var,$D),factor_expr(e[2],var,$D))
 if $b(e):
  $! e
 ks=[]
 kernels(e,ks)
 sortkernels(ks)
 nv=$/(ks)
 if nv==0:
  $! e
 r=ratform(e,ks)
 if r is $#:
  $! e
 N,D=cancel_pair(r[0],r[1],nv)
 cn,fn_=mfactor(N,nv)
 cd,fd=mfactor(D,nv)
 const=Q(1,1)
 const=ndiv(cn,cd)
 nfac=[]
 $( g,m in fn_:
  nfac.$}(split_radical(p2e(g,ks),m,var,$D))
 dfac=[]
 $( g,m in fd:
  dfac.$}(split_radical(p2e(g,ks),m,var,$D))
 items=[]
 $( f,m in nfac:
  if $G(f):
   const=nmul(const,nipow(f,m))
  $&:
   items.$%((f,m))
 ditems=[]
 $( f,m in dfac:
  if $G(f):
   const=ndiv(const,nipow(f,m))
  $&:
   ditems.$%((f,m))
 items.sort(key=$; fm:fsortkey(fm[0]))
 ditems.sort(key=$; fm:fsortkey(fm[0]))
 $9=[]
 if const!=1 or($- items $* $- ditems):
  $9.$%(const)
 $( f,m in items:
  $9.$%(f if m==1 $&('^',f,m))
 $( f,m in ditems:
  $9.$%(('^',f,-m))
 if $/($9)==1:
  if $)($9[0],'^')or $G($9[0]):
   $!('hold',$9[0])if $- $G($9[0])$& $9[0]
  $! $9[0]
 $!('hold',('*',)+$1($9))
$, fsortkey(f):
 ss=$e(f)
 ss.sort(key=varprio)
 d=0
 if ss:
  d=degree(f,ss[0])
  if d is $#:
   d=99
 $!($/(ss),okey(ss),d,okey(f))
$, split_radical(f,m,var,$D):
 if var is $# $* $- $D:
  $![(f,m)]
 vs=$e(f)
 if var is $#:
  if $/(vs)!=1:
   $![(f,m)]
  x=vs[0]
 $&:
  x=var
 cs=$[(f,x)
 if cs is $# or $/(cs)!=3:
  if cs is $- $# $* $/(cs)==2 $* $D:
   $![(f,m)]
  $![(f,m)]
 c,b,a=cs
 D=$?($_($<(b,b),$<(4,a,c)))
 if $- $5(D):
  if var is $#:
   $![(f,m)]
 $&:
  v=$Z(D)
  if $0(v)is $4:
   v=v.$U
  if v<0 $* $- $D:
   $![(f,m)]
 sD=$O(D)
 r1=$V($`($m(b),sD),$<(2,a))
 r2=$V($_($m(b),sD),$<(2,a))
 res=[(a,m)]if a!=1 $&[]
 res.$%(($_(x,r2),m))
 res.$%(($_(x,r1),m))
 $! res
''')
_x(r'''$, partfrac(e,x):
 r=to_ratform(e)
 if r is $#:
  $! $#
 N,D,ks=r
 if x $- in ks:
  $! $#
 k=ks.index(x)
 $( v in p_vars(N,$/(ks))+p_vars(D,$/(ks)):
  if v!=k:
   $! $#
 nv=$/(ks)
 num=[0]*(max(p_deg(N,k),0)+1)
 $( m in N:
  num[m[k]]=N[m]
 den=[0]*(p_deg(D,k)+1)
 $( m in D:
  den[m[k]]=D[m]
 if $/(den)<=1:
  $! $#
 q,rem=u_divmod(num,den)
 cc,fs=ufactor(den)
 $Q=[u_toexpr(q,x)]
 if rem:
  parts=[u_trim(pw_list(f,m))$( f,m in fs]
  rem=u_scale(rem,ninv(cc))
  $( j in $+($/(fs)):
   f,m=fs[j]
   Pj=parts[j]
   others=[1]
   $( i in $+($/(fs)):
    if i!=j:
     others=u_mul(others,parts[i])
   g,s,t=u_egcd(others,Pj)
   Aj=u_divmod(u_mul(rem,s),Pj)[1]
   fe=u_toexpr(f,x)
   $( p in $+(m,0,-1):
    if $- Aj:
     $R
    qq,cj=u_divmod(Aj,f)
    if cj:
     $Q.$%($V(u_toexpr(cj,x),pw(fe,p)))
    Aj=qq
 $! $>($Q)
$, pw_list(f,m):
 r=[1]
 $( _ in $+(m):
  r=u_mul(r,f)
 $! r
$, propfrac(e,x=$#):
 if $w(e):
  n,d=nd(e)
  if d==1:
   $! e
  qn=$H(n)//d
  if n<0:
   qn=-qn
  rr=Q(n-qn*d,d)
  if qn==0:
   $! e
  $!('hold',('+',qn,rr))
 r=to_ratform(e)
 if r is $#:
  $! e
 N,D,ks=r
 if x is $#:
  vs=p_vars(D,$/(ks))
  if $- vs:
   $! e
  x=ks[vs[0]]
 num=p2e(N,ks)
 den=p2e(D,ks)
 cn=$[(num,x)
 cd=$[(den,x)
 if cn is $# or cd is $# or $/(cd)<=1:
  $! e
 qq,rr=e_divmod(cn,cd)
 $! $`(fromcoeffs(qq,x),$V(fromcoeffs(rr,x),den))
$, e_divmod(a,b):
 a=[$?(c)$( c in a]
 b=[$?(c)$( c in b]
 $F b $* b[-1]==0:
  b.pop()
 $F a $* a[-1]==0:
  a.pop()
 if $- b:
  err("Division by zero")
 q=[0]*max($/(a)-$/(b)+1,1)
 r=$J(a)
 lb=b[-1]
 $F $/(r)>=$/(b)$* r:
  c=$.($V(r[-1],lb))
  kk=$/(r)-$/(b)
  q[kk]=c
  $( j in $+($/(b)):
   r[kk+j]=$?($_(r[kk+j],$<(c,b[j])))
  r.pop()
  $F r $* r[-1]==0:
   r.pop()
 $! q,r
$, poly_gcd_expr(a,b):
 ks=[]
 kernels(a,ks)
 kernels(b,ks)
 sortkernels(ks)
 ra=ratform(a,ks)
 rb=ratform(b,ks)
 if ra is $# or rb is $#:
  err("Polynomials required")
 nv=$/(ks)
 g=p_gcd(ra[0],rb[0],nv)
 if $- ks:
  $! p_cval(g)
 $! p2e(g,ks)
$, expand_full(e,var=$#):
 if $)(e,'$J')or $)(e,'mat'):
  $! mapexpr($; a:expand_full(a,var),e)
 if isrel(e):
  $!(e[0],expand_full(e[1],var),expand_full(e[2],var))
 x=$?(e)
 if $- hasdenom(x)or $b(x):
  $! x
 if var is $#:
  ks=$e(x)
  ks.sort(key=varprio)
  $( v in ks:
   r=partfrac(x,v)
   if r is $- $#:
    $! $?(r)
  $! x
 r=partfrac(x,var)
 if r is $- $#:
  $! $?(r)
 $! x
''')
_x(r'''TV='T_'
LNT='LNT_'
VV='V_'
class $o($6):
 pass
$, dfun($A,u):
 if $A=='sin':
  $! fn('cos',u)
 if $A=='cos':
  $! $m(fn('sin',u))
 if $A=='tan':
  $! pw(fn('cos',u),-2)
 if $A=='$y':
  $! pw($_(1,pw(u,2)),Q(-1,2))
 if $A=='arccos':
  $! $m(pw($_(1,pw(u,2)),Q(-1,2)))
 if $A=='$s':
  $! pw($`(pw(u,2),1),-1)
 if $A=='sinh':
  $! fn('cosh',u)
 if $A=='cosh':
  $! fn('sinh',u)
 if $A=='tanh':
  $! pw(fn('cosh',u),-2)
 if $A=='arcsinh':
  $! pw($`(pw(u,2),1),Q(-1,2))
 if $A=='arccosh':
  $! pw($_(pw(u,2),1),Q(-1,2))
 if $A=='arctanh':
  $! pw($_(1,pw(u,2)),-1)
 if $A=='ln':
  $! pw(u,-1)
 if $A=='$H':
  $! fn('sign',u)
 if $A in('sign','floor','ceiling','round','ipart','$q'):
  $! 0
 $! $#
$, diff(e,x,n=1):
 if n<0:
  r=e
  $( _ in $+(-n):
   r=integrate(r,x)
  $! r
 $( _ in $+(n):
  e=diff1(e,x)
 $! e
$, diff1(e,x):
 if $)(e,'$J')or $)(e,'mat'):
  $! mapexpr($; a:diff1(a,x),e)
 if $)(e,'=')or $)(e,'<')or $)(e,'>'):
  $!(e[0],diff1(e[1],x),diff1(e[2],x))
 if $8(e,x):
  $! 0
 if e==x:
  $! 1
 h=e[0]
 if h=='+':
  $! $>([diff1(a,x)$( a in e[1:]])
 if h=='*':
  fs=e[1:]
  $Q=[]
  $( i in $+($/(fs)):
   d=diff1(fs[i],x)
   if d!=0:
    $Q.$%($K([d]+[fs[j]$( j in $+($/(fs))if j!=i]))
  $! $>($Q)
 if h=='^':
  b=e[1]
  p=e[2]
  if $8(p,x):
   $! $<(p,pw(b,$_(p,1)),diff1(b,x))
  if $8(b,x):
   $! $<(e,fn('ln',b),diff1(p,x))
  $! $<(e,$`($<(diff1(p,x),fn('ln',b)),$V($<(p,diff1(b,x)),b)))
 if h=='log':
  b=e[2]if $/(e)>2 $& 10
  $! diff1($V(fn('ln',e[1]),fn('ln',b)),x)
 if h=='when':
  $! fn('when',e[1],diff1(e[2],x),diff1(e[3],x))if $/(e)>3 $& fn('when',e[1],diff1(e[2],x))
 if h=='$N' $* $/(e)==3 $* e[2]==x:
  $! e[1]
 if h=='$N' $* $/(e)==5 $* $8(e[1],x)is $2 $* e[2]!=x:
  f,v,a,b=e[1],e[2],e[3],e[4]
  $! $_($<($Y(f,v,b),diff1(b,x)),$<($Y(f,v,a),diff1(a,x)))
 if $/(e)==2:
  d=dfun(h,e[1])
  if d is $- $#:
   $! $<(d,diff1(e[1],x))
 $!('d',e,x)
$, $k(u,x):
 cs=$[(u,x)
 if cs is $# or $/(cs)!=2 or cs[1]==0:
  $! $#
 $! cs[1],cs[0]
$, nice(e):
 ${:
  e=$.(e)
 $3 $6:
  $! e
 if $- hasdenom(e)or $b(e)or $)(e,'$J')or $)(e,'mat'):
  $! e
 best=e
 bl=$/(fmt(e))
 if bl>400:
  $! e
 $( f in(comdenom,factor_expr):
  ${:
   c=f(e)
   l=$/(fmt(c))
   if l<bl:
    best=c
    bl=l
  $3 $6:
   pass
 $! best
BUDGET=[0]
$, integrate(f,x,$:=0):
 BUDGET[0]=0
 r=integ(f,x,$:)
 if r is $# $* hasdenom(f):
  g=$.(f)
  if g!=f:
   BUDGET[0]=0
   r=integ(g,x,$:)
 if r is $#:
  $!('$N',f,x)
 $! r
$, integ(f,x,$:=0):
 if $:>7:
  $! $#
 if $:==0:
  BUDGET[0]=0
 BUDGET[0]+=1
 if BUDGET[0]>400:
  $! $#
 if $8(f,x):
  $! $<(f,x)
 if f==x:
  $! $<($x,pw(x,2))
 h=f[0]if $0(f)is $1 $& $#
 if h=='+':
  $9=[]
  $( t in f[1:]:
   r=integ(t,x,$:+1)
   if r is $#:
    $! integ_whole(f,x,$:)
   $9.$%(r)
  $! $>($9)
 if h=='*':
  c=[g $( g in f[1:]if $8(g,x)]
  v=[g $( g in f[1:]if $- $8(g,x)]
  if c:
   r=integ($K(v),x,$:)
   if r is $#:
    $! $#
   $! $<($K(c),r)
 if h=='when':
  a=integ(f[2],x,$:+1)
  b=integ(f[3],x,$:+1)if $/(f)>3 $& $#
  if a is $# or($/(f)>3 $* b is $#):
   $! $#
  $!('when',f[1],a,b)if b is $- $# $&('when',f[1],a)
 r=itable(f,x)
 if r is $- $#:
  $! r
 $! integ_whole(f,x,$:)
$, integ_whole(f,x,$:):
 d=degree(f,x)
 if d is $- $#:
  g=$?(f)
  if g!=f:
   $! integ(g,x,$:+1)
 r=irational(f,x)
 if r is $- $#:
  $! r
 r=itanpow(f,x,$:)
 if r is $- $#:
  $! r
 r=isecpow(f,x,$:)
 if r is $- $#:
  $! r
 r=isubst(f,x,$:)
 if r is $- $#:
  $! r
 r=itrigsub(f,x,$:)
 if r is $- $#:
  $! r
 if hastrig(f):
  g=tcollect(f)
  if g!=f:
   r=integ(g,x,$:+1)
   if r is $- $#:
    $! r
 r=iparts(f,x,$:)
 if r is $- $#:
  $! r
 g=$?(f)
 if g!=f:
  r=integ(g,x,$:+1)
  if r is $- $#:
   $! r
 if $:<4:
  g=untan(f)
  if g!=f:
   r=integ(g,x,$:+2)
   if r is $- $#:
    $! r
  g=unhyp(f)
  if g!=f:
   r=integ($?(g),x,$:+2)
   if r is $- $#:
    $! r
  r=iweier(f,x,$:)
  if r is $- $#:
   $! r
  r=iquartic(f,x,$:)
  if r is $- $#:
   $! r
 $! $#
$, qfrac(A,B,p,q,x):
 w=$O($_($<(4,q),pw(p,2)))
 P=$`(pw(x,2),$<(p,x),q)
 $! $`($<(A,$x,fn('ln',P)),
 $<($_(B,$<(A,p,$x)),$V(2,w),fn("$s",$?($V($`($<(2,x),p),w)))))
$, iquartic(f,x,$:):
 n,d=numer_denom(f)
 cd=$[(d,x)
 cn=$[(n,x)
 if cd is $# or cn is $# or $/(cd)!=5 or $/(cn)>4:
  $! $#
 if cd[1]!=0 or cd[3]!=0 or $- all([$5(q)$( q in cd+cn]):
  $! $#
 a,b,c=cd[4],cd[2],cd[0]
 ${:
  if fv_(c)/fv_(a)<=0:
   $! $#
  q=$O($V(c,a))
  s2=$_($<(2,q),$V(b,a))
  if fv_(s2)<=0:
   $! $#
 $3 $6:
  $! $#
 sr=$O(s2)
 cn=[$V(v,a)$( v in cn]+[0]*(4-$/(cn))
 n0,n1,n2,n3=cn
 BE=$V(n0,q)
 EmB=$V($_(n1,$<(q,n3)),sr)
 B=$<($x,$_(BE,EmB))
 E=$<($x,$`(BE,EmB))
 CmA=$V($_(n2,BE),sr)
 A=$<($x,$_(n3,CmA))
 C=$<($x,$`(n3,CmA))
 P1=$`(pw(x,2),$<(sr,x),q)
 P2=$`($_(pw(x,2),$<(sr,x)),q)
 R=$`(qfrac(A,B,sr,q,x),qfrac(C,E,$m(sr),q,x))
 $! R if antiok(R,f,x)$& $#
$, unhyp(e):
 if $0(e)is $- $1 or e[0]=='Q':
  $! e
 a=[unhyp(b)$( b in e[1:]]
 if $/(a)==1 $* e[0]in('sinh','cosh','tanh'):
  p=pw('e',a[0])
  m=pw('e',$m(a[0]))
  if e[0]=='sinh':
   $! $<($x,$_(p,m))
  if e[0]=='cosh':
   $! $<($x,$`(p,m))
  $! $V($_(p,m),$`(p,m))
 $! simp((e[0],)+$1(a))
''')
_x(r'''$, trigargs_x(f,x,$9):
 if $0(f)is $- $1 or f[0]=='Q':
  $!
 if f[0]in('sin','cos','tan')$* $- $8(f[1],x):
  if f[1]$- in $9:
   $9.$%(f[1])
  $!
 $( b in f[1:]:
  trigargs_x(b,x,$9)
$, iweier(f,x,$:):
 us=[]
 trigargs_x(f,x,us)
 if $/(us)!=1:
  $! $#
 u=us[0]
 lu=$k(u,x)
 if lu is $#:
  $! $#
 t='W%d_'%$:
 q=$`(1,pw(t,2))
 $, rep(e):
  if $0(e)is $- $1 or e[0]=='Q':
   $! e
  if $/(e)==2 $* e[1]==u:
   if e[0]=='sin':
    $! $V($<(2,t),q)
   if e[0]=='cos':
    $! $V($_(1,pw(t,2)),q)
   if e[0]=='tan':
    $! $V($<(2,t),$_(1,pw(t,2)))
  $! simp((e[0],)+$1(rep(b)$( b in e[1:]))
 g=rep(f)
 if $- $8(g,x):
  $! $#
 g=$.($V($<(2,g),$<(lu[0],q)))
 R=integ(g,t,$:+2)
 if R is $#:
  $! $#
 R=$Y(R,t,fn('tan',$<($x,u)))
 $! R if antiok(R,f,x)$& $#
$, itable(f,x):
 h=head(f)
 if h=='^':
  b=f[1]
  p=f[2]
  if $8(p,x):
   lb=$k(b,x)
   if lb is $- $#:
    a=lb[0]
    if p==-1:
     $! $V(fn('ln',fn('$H',b)),a)
    $! $V(pw(b,$`(p,1)),$<(a,$`(p,1)))
   if(p==$x or p==Q(-1,2))$* degree(b,x)==2:
    $! iquadrad(b,p,x)
   if $/(b)==2 $* head(b)in('sin','cos','tan','sinh','cosh')$* $0(b)is $1:
    lu=$k(b[1],x)
    if lu is $- $#:
     a=lu[0]
     u=b[1]
     n=b[0]
     if n=='cos' $* p==-2:
      $! $V(fn('tan',u),a)
     if n=='sin' $* p==-2:
      $! $V($m(pw(fn('tan',u),-1)),a)
     if n=='cos' $* p==-1:
      $! $V(fn('ln',fn('$H',$`(pw(fn('cos',u),-1),fn('tan',u)))),a)
     if n=='sin' $* p==-1:
      $! $V(fn('ln',fn('$H',fn('tan',$<($x,u)))),a)
     if n=='tan' $* p==-1:
      $! $V(fn('ln',fn('$H',fn('sin',u))),a)
     if n=='cosh' $* p==-2:
      $! $V(fn('tanh',u),a)
  if $8(b,x):
   lu=$k(p,x)
   if lu is $- $#:
    a=lu[0]
    if b=='e':
     $! $V(f,a)
    $! $V(f,$<(a,fn('ln',b)))
  $! $#
 if $0(f)is $1 $* $/(f)==2:
  u=f[1]
  lu=$k(u,x)
  if lu is $#:
   $! $#
  a=lu[0]
  r=$#
  if h=='sin':
   r=$m(fn('cos',u))
  $= h=='cos':
   r=fn('sin',u)
  $= h=='tan':
   r=$m(fn('ln',fn('$H',fn('cos',u))))
  $= h=='sinh':
   r=fn('cosh',u)
  $= h=='cosh':
   r=fn('sinh',u)
  $= h=='tanh':
   r=fn('ln',fn('cosh',u))
  $= h=='ln':
   r=$_($<(u,fn('ln',u)),u)
  $= h=='$s':
   r=$_($<(u,fn('$s',u)),$<($x,fn('ln',$`(pw(u,2),1))))
  $= h=='$y':
   r=$`($<(u,fn('$y',u)),$O($_(1,pw(u,2))))
  $= h=='arccos':
   r=$_($<(u,fn('arccos',u)),$O($_(1,pw(u,2))))
  $= h=='$H':
   r=$<($x,u,fn('$H',u))
  $= h=='sign':
   r=fn('$H',u)
  $= h=='arcsinh':
   r=$_($<(u,fn('arcsinh',u)),$O($`(pw(u,2),1)))
  $= h=='arctanh':
   r=$`($<(u,fn('arctanh',u)),$<($x,fn('ln',$_(1,pw(u,2)))))
  if r is $- $#:
   $! $V(r,a)
 if h=='log' $* $/(f)==3:
  lu=$k(f[1],x)
  if lu is $- $#:
   u=f[1]
   $! $V($_($<(u,fn('ln',u)),u),$<(lu[0],fn('ln',f[2])))
 $! $#
$, iquadrad(b,p,x):
 cs=$[(b,x)
 C,B,A=cs
 if $- $5(A):
  $! $#
 av=$Z(A)
 if $0(av)is $4:
  $! $#
 D=$_($<(B,B),$<(4,A,C))
 if p==Q(-1,2):
  if av<0:
   $! $<(pw($m(A),Q(-1,2)),fn('$y',$V($m($`($<(2,A,x),B)),$O(D))))
  sA=$O(A)
  $! $<(pw(A,Q(-1,2)),fn('ln',fn('$H',$`($O(b),$<(sA,x),$V(B,$<(2,sA))))))
 J=iquadrad(b,Q(-1,2),x)
 if J is $#:
  $! $#
 $! $`($V($<($`($<(2,A,x),B),$O(b)),$<(4,A)),
 $<($V($_($<(4,A,C),$<(B,B)),$<(8,A)),J))
$, irational(f,x):
 ks=[]
 kernels(f,ks)
 $( k in ks:
  if k!=x:
   $! $#
 if $- hasdenom(f):
  $! $#
 pf=partfrac(f,x)
 if pf is $#:
  $! $#
 $Q=pf[1:]if $)(pf,'+')$&(pf,)
 $9=[]
 $( t in $Q:
  if $- hasdenom(t):
   r=integ(t,x,5)
   if r is $#:
    $! $#
   $9.$%(r)
   $7
  fs=t[1:]if $)(t,'*')$&(t,)
  num=[]
  den=$#
  k=1
  $( g in fs:
   if $)(g,'^')$* $0(g[2])is $q $* g[2]<0:
    den=g[1]
    k=-g[2]
   $&:
    num.$%(g)
  if den is $#:
   $! $#
  N=$K(num)
  dg=degree(den,x)
  if dg==1:
   r=integ(t,x,5)
   if r is $#:
    $! $#
   $9.$%(r)
  $= dg==2:
   r=iquadfrac(N,den,k,x)
   if r is $#:
    $! $#
   $9.$%(r)
  $&:
   r=isubst(t,x,3)if k==1 $& $#
   if r is $# $* k==1:
    r=iquartic(t,x,3)
   if r is $#:
    $! $#
   $9.$%(r)
 $! $>($9)
$, iquadfrac(N,Qd,k,x):
 cs=$[(N,x)
 if cs is $# or $/(cs)>2:
  $! $#
 n0=cs[0]
 n1=cs[1]if $/(cs)>1 $& 0
 C,B,A=$[(Qd,x)
 res=[]
 if n1!=0:
  if k==1:
   D=$_($<(B,B),$<(4,A,C))
   dv=$Z(D)if $5(D)$& 0
   arg=Qd if($0(dv)is $- $4 $* dv<0 $* $Z(A)>0)$& fn('$H',Qd)
   res.$%($<($V(n1,$<(2,A)),fn('ln',arg)))
  $&:
   res.$%($<($V(n1,$<(2,A)),$V(-1,$<(k-1,pw(Qd,k-1)))))
 c0=$_(n0,$V($<(n1,B),$<(2,A)))
 if c0!=0:
  J=jquad(A,B,C,Qd,k,x)
  if J is $#:
   $! $#
  res.$%($<(c0,J))
 $! $>(res)
$, jquad(A,B,C,Qd,k,x):
 D=$?($_($<(B,B),$<(4,A,C)))
 if k==1:
  if $- $5(D):
   $! $#
  dv=$Z(D)
  if $0(dv)is $4:
   $! $#
  L=$`($<(2,A,x),B)
  if dv<0:
   s=$O($m(D))
   $! $<($V(2,s),fn('$s',$V(L,s)))
  if dv>0:
   s=$O(D)
   $! $<(pw(s,-1),fn('ln',fn('$H',$V($_(L,s),$`(L,s)))))
  $! $V(-2,L)
 Jp=jquad(A,B,C,Qd,k-1,x)
 if Jp is $#:
  $! $#
 Dl=$m(D)
 L=$`($<(2,A,x),B)
 $! $`($<($V(L,$<(k-1,Dl)),pw(Qd,1-k)),
 $<($V($<(2*k-3,2,A),$<(k-1,Dl)),Jp))
$, itanpow(f,x,$:):
 if $)(f,'^')$* $)(f[1],'tan')$* $0(f[2])is $q $* f[2]>=2:
  u=f[1][1]
  lu=$k(u,x)
  if lu is $#:
   $! $#
  n=f[2]
  a=lu[0]
  t=f[1]
  first=$V(pw(t,n-1),$<(n-1,a))
  $a=integ(pw(t,n-2),x,$:+1)
  if $a is $#:
   $! $#
  $! $_(first,$a)
 $! $#
''')
_x(r'''$, isecpow(f,x,$:):
 if($)(f,'^')$* head(f[1])in('cos','sin')$* $/(f[1])==2
 $* $0(f[2])is $q $* f[2]<=-3):
  u=f[1][1]
  lu=$k(u,x)
  if lu is $#:
   $! $#
  n=-f[2]
  a=lu[0]
  if f[1][0]=='cos':
   first=$<(pw(fn('cos',u),2-n),fn('tan',u))
  $&:
   first=$m($<(pw(fn('sin',u),2-n),pw(fn('tan',u),-1)))
  $a=integ(pw(f[1],2-n),x,$:+1)
  if $a is $#:
   $! $#
  $! $`($V(first,$<(n-1,a)),$<(Q(n-2,n-1),$a))
 $! $#
$, cands(f,x,$9):
 if $0(f)is $- $1 or $8(f,x)or f[0]=='Q':
  $!
 h=f[0]
 if h=='+' or h=='*':
  $( a in f[1:]:
   cands(a,x,$9)
  $!
 if h=='^':
  if f[1]!=x $* $- $8(f[1],x)$* f[1]$- in $9:
   $9.$%(f[1])
  if isq(f[2])$* $- $8(f[1],x):
   rad=pw(f[1],Q(1,f[2][2]))
   if rad $- in $9:
    $9.$%(rad)
  if $- $8(f[2],x)$* f[2]$- in $9:
   $9.$%(f[2])
   if f $- in $9:
    $9.$%(f)
  if f[1]==x $* f $- in $9 $* $G(f[2])$* f[2]!=-1:
   $9.$%(f)
   if $i(f[2])$* f[2]%2==0 $* f[2]>2 $* pw(x,2)$- in $9:
    $9.$%(pw(x,2))
  cands(f[1],x,$9)
  cands(f[2],x,$9)
  $!
 if f $- in $9:
  $9.$%(f)
 $( a in f[1:]:
  if a!=x $* $- $8(a,x)$* a $- in $9:
   $9.$%(a)
  cands(a,x,$9)
$, subst_kernel(q,u,V,x):
 if $)(u,'^')$* u[1]==x $* $G(u[2]):
  q2=$Y(q,x,pw(V,pw(u[2],-1)))
  $! $Y(q2,fn('$H',V),V)
 if $)(u,'ln'):
  lu=$k(u[1],x)
  if lu is $- $#:
   a,b=lu
   $! $Y(q,x,$V($_(pw('e',V),b),a))
 if $)(u,'^')$* isq(u[2])$* $- $8(u[1],x):
  cs_=$[(u[1],x)
  q2=$Y(q,u,V)
  if cs_ is $- $# $* $- $8(q2,x):
   nz=[k $( k in $+(1,$/(cs_))if cs_[k]!=0]
   if $/(nz)==1:
    k=nz[0]
    xk=$V($_(pw(V,pw(u[2],-1)),cs_[0]),cs_[k])
    q3=$Y(q2,x,pw(xk,Q(1,k)))
    if $8(q3,x):
     $! q3
  $! q2
 if $)(u,'^')$* u[1]=='e':
  lu=$k(u[2],x)
  if lu is $- $# $* lu[1]==0:
   a=lu[0]
   $! subst_exp(q,a,V,x)
 $! $Y(q,u,V)
$, subst_exp(q,a,V,x):
 if $0(q)is $- $1 or q[0]=='Q':
  $! q
 if q[0]=='^' $* q[1]=='e':
  lm=$k(q[2],x)
  if lm is $- $#:
   $! $<(pw(V,$V(lm[0],a)),pw('e',lm[1]))
 $! simp((q[0],)+$1(subst_exp(b,a,V,x)$( b in q[1:]))
$, isubst(f,x,$:):
 if $:>5:
  $! $#
 VV='V%d_'%$:
 $F has(f,VV)or VV==x:
  VV=VV+'_'
 cs=[]
 cands(f,x,cs)
 fracf=hasfracpow(f,x)
 big=$/(okey(f))>500
 $( u in cs[:14]:
  if u==x:
   $7
  du=diff(u,x)
  if du==0:
   $7
  q=$V(f,du)
  if $- big:
   q=$.(q)
  q2=subst_kernel(q,u,VV,x)
  if $8(q2,x)$*(fracf or $- hasfracpow(q2,VV))$* $/(okey(q2))<800:
   r=integ(q2,VV,$:+2)
   if r is $- $#:
    r=$Y(r,VV,u)
    if antiok(r,f,x):
     $! r
 $( u in cs:
  if $)(u,'+'):
   lu=$k(u,x)
   if lu is $- $#:
    a,b=lu
    g=$?($V($Y(f,x,$V($_(VV,b),a)),a))
    r=integ(g,VV,$:+2)
    if r is $- $#:
     $! $Y(r,VV,u)
 $! $#
TPTS=(-2.3,-1.7,-0.8,-0.35,0.3,0.75,1.6,2.4)
$, antiok(F,f,x):
 if $/($e(f))>1 or $/($e(F))>1:
  $! $B
 $, v(e,t):
  ${:
   z=$Z(e,{x:t})
  $3 $6:
   $! $#
  if $0(z)is $4:
   if $H(z.imag)>1e-9*(1+$H(z.$U)):
    $! $#
   z=z.$U
  if z!=z or $H(z)>1e12:
   $! $#
  $! z
 $( t in TPTS:
  y=v(f,t)
  if y is $#:
   $7
  h=1e-5*(1+$H(t))
  a=v(F,t+h)
  b=v(F,t-h)
  if a is $# or b is $#:
   $7
  if $H((a-b)/(2*h)-y)>1e-4*(1+$H(y)):
   $! $2
 $! $B
$, itrigsub(f,x,$:):
 rad=[]
 radicals(f,x,rad)
 if $- rad:
  $! $#
 B=rad[0]
 cs=$[(B,x)
 if cs is $# or $/(cs)!=3 or cs[1]!=0 or $- $5(cs[0])or $- $5(cs[2]):
  $! $#
 if any([q!=B $( q in rad]):
  $! $#
 c0,c2=cs[0],cs[2]
 T='T%d_'%$:
 if fv_(c0)<0 $* fv_(c2)>0:
  r=$O($V($m(c0),c2))
  xs=$V(r,fn('cos',T))
  rt=$<($O(c2),r,fn('tan',T))
  dx=$<(r,fn('tan',T),pw(fn('cos',T),-1))
  g=$<(subrad(f,B,rt,x,xs),dx)
  R=$#
  $( h in(pyth_to(g,'cos'),pyth_to(g,'sin'),pyth(g)):
   R=integ(h,T,$:+2)
   if R is $- $#:
    $R
  if R is $#:
   $! $#
  R=backtrig(texpand(R),T,$V(pw(B,$x),$<($O(c2),x)),$V(r,x))
  R=$Y(R,T,fn('arccos',$V(r,x)))
  if $- $8(R,T)or $- antiok(R,f,x):
   $! $#
  $! R
 if fv_(c0)<=0:
  $! $#
 sc0=$O(c0)
 if fv_(c2)<0:
  r=$O($V(c0,$m(c2)))
  xs=$<(r,fn('sin',T))
  rt=$<(sc0,fn('cos',T))
  dx=$<(r,fn('cos',T))
 $&:
  r=$O($V(c0,c2))
  xs=$<(r,fn('tan',T))
  rt=$V(sc0,fn('cos',T))
  dx=$V(r,pw(fn('cos',T),2))
 g=$<(subrad(f,B,rt,x,xs),dx)
 R=$#
 $( h in(pyth(g),pyth_to(g,'cos'),pyth_to(g,'sin')):
  R=integ(h,T,$:+2)
  if R is $- $#:
   $R
 if R is $#:
  $! $#
 R=texpand(R)
 sq=pw(B,$x)
 if fv_(c2)<0:
  sinT=$V(x,r)
  cosT=$V(sq,sc0)
  Tx=fn('$y',$V(x,r))
 $&:
  cosT=$V(sc0,sq)
  sinT=$<($V(x,r),cosT)
  Tx=fn('$s',$V(x,r))
 R=backtrig(R,T,sinT,cosT)
 R=$Y(R,T,Tx)
 if $- $8(R,T)or $- antiok(R,f,x):
  $! $#
 $! R
$, radicals(f,x,$9):
 if $0(f)is $- $1 or f[0]=='Q':
  $!
 if f[0]=='^' $* isq(f[2])$* f[2][2]==2 $* $- $8(f[1],x):
  $9.$%(f[1])
 $( a in f[1:]:
  radicals(a,x,$9)
$, subrad(f,B,rt,x,xs):
 if f==x:
  $! xs
 if $0(f)is $- $1 or f[0]=='Q':
  $! f
 if f[0]=='^' $* f[1]==B $* isq(f[2])$* f[2][2]==2:
  $! pw(rt,f[2][1])
 $! simp((f[0],)+$1(subrad(a,B,rt,x,xs)$( a in f[1:]))
$, backtrig(R,T,sinT,cosT):
 if $0(R)is $- $1 or R[0]=='Q':
  $! R
 if $/(R)==2 $* R[1]==T:
  if R[0]=='sin':
   $! sinT
  if R[0]=='cos':
   $! cosT
  if R[0]=='tan':
   $! $V(sinT,cosT)
 $! simp((R[0],)+$1(backtrig(a,T,sinT,cosT)$( a in R[1:]))
$, hasfracpow(e,x):
 if $0(e)is $- $1 or e[0]=='Q':
  $! $2
 if e[0]=='^' $* $- $i(e[2])$* $- $8(e[1],x):
  $! $B
 $( a in e[1:]:
  if hasfracpow(a,x):
   $! $B
 $! $2
''')
_x(r'''$, hastrig(f):
 if $0(f)is $- $1 or f[0]=='Q':
  $! $2
 if f[0]in('sin','cos'):
  $! $B
 $( a in f[1:]:
  if hastrig(a):
   $! $B
 $! $2
$, ispoly(e,x):
 $! degree(e,x)is $- $#
$, iparts(f,x,$:):
 if $:>5:
  $! $#
 fs=f[1:]if $)(f,'*')$&(f,)
 P=[]
 G=[]
 $( g in fs:
  if ispoly(g,x):
   P.$%(g)
  $&:
   G.$%(g)
 if $/(G)==2:
  ex=$#
  tr=$#
  $( g in G:
   if $)(g,'^')$* g[1]=='e' $* $k(g[2],x):
    ex=g
   $= head(g)in('sin','cos')$* $k(g[1],x):
    tr=g
  if ex is $- $# $* tr is $- $# $* $- P:
   a=$k(ex[2],x)[0]
   b=$k(tr[1],x)[0]
   u=tr[1]
   den=$`($<(a,a),$<(b,b))
   if tr[0]=='sin':
    r=$<(ex,$_($<(a,fn('sin',u)),$<(b,fn('cos',u))))
   $&:
    r=$<(ex,$`($<(a,fn('cos',u)),$<(b,fn('sin',u))))
   $! $V(r,den)
  $! $#
 if $/(G)!=1:
  $! $#
 g=G[0]
 Pp=$K(P)
 gh=head(g)
 tabular=$2
 if $)(g,'^')$* g[1]=='e' $* $k(g[2],x):
  tabular=$B
 $= $)(g,'^')$* $G(g[1])$* $k(g[2],x):
  tabular=$B
 $= gh in('sin','cos','sinh','cosh')$* $k(g[1],x):
  tabular=$B
 if tabular $* P:
  res=[]
  sg=1
  Gi=g
  Pd=Pp
  $( _ in $+(40):
   Gi=integ(Gi,x,$:+1)
   if Gi is $#:
    $! $#
   res.$%($<(sg,Pd,Gi))
   Pd=diff(Pd,x)
   sg=-sg
   if Pd==0:
    $! $>(res)
  $! $#
 if gh in('ln','$s','$y','arccos','log','arcsinh','arctanh')or($)(g,'^')$* head(g[1])in('ln','$y','$s')$* $i(g[2])$* g[2]>0):
  V=integ(Pp,x,$:+1)
  if V is $#:
   $! $#
  $a=integ($.($?($<(V,diff(g,x)))),x,$:+1)
  if $a is $#:
   $! $#
  $! $_($<(g,V),$a)
 $! $#
$, defint(f,x,a,b):
 if a==b:
  $! 0
 if $5(a)$* $5(b):
  ${:
   if numpt(a)>numpt(b):
    r=defint(f,x,b,a)
    $! $m(r)if $- $)(r,'$N')$&('$N',f,x,a,b)
  $3 $6:
   pass
 if haswhen(f,x)$* $5(a)$* $5(b):
  ps=whensplit(f,x,a,b)
  if ps is $- $#:
   total=0
   $( p,q,g in ps:
    if g=='$I' or has(g,'$I'):
     $! '$I'
    total=$`(total,defint(g,x,p,q))
   $! total
 BUDGET[0]=0
 F=integ(f,x)
 if F is $# $* hasdenom(f):
  BUDGET[0]=0
  F=integ($.(f),x)
 sing=singular_points(f,x,a,b)or[]
 if F is $- $# $* $- $b(f):
  $( p in singular_points(F,x,a,b)or[]:
   if all([$H(fv_(p)-fv_(q))>1e-9 $( q in sing]):
    sing.$%(p)
  sing.sort(key=fv_)
  if $5(a)$* $5(b)$* fv_(a)>fv_(b):
   sing.reverse()
  pts=[a]+sing+[b]
  total=0
  infs=[]
  $( i in $+($/(pts)-1):
   lo=pts[i]
   hi=pts[i+1]
   vb=$|(F,x,hi,-1 if $- isinf(hi)$& 0)
   va=$|(F,x,lo,1 if $- isinf(lo)$& 0)
   if $)(vb,'$|')or $)(va,'$|'):
    total=$#
    $R
   d=$_(vb,va)
   if va=='$I' or vb=='$I':
    $! '$I'
   if has(va,'$P')or has(vb,'$P'):
    if d $- in('$P',('*',-1,'$P')):
     $! '$I'
   if d=='$I' or has(d,'$I'):
    total=$#
    $R
   if has(d,'$P'):
    infs.$%(d)
   total=$`(total,d)
  if total is $- $# $* infs:
   if all([q==infs[0]$( q in infs])$* infs[0]in('$P',('*',-1,'$P')):
    $! infs[0]
   $! '$I'
  if total is $- $# $* total!='$I':
   $! total
 if $5(a)$* $5(b)$* freeofall(f,[s $( s in $e(f)if s!=x]):
  ${:
   $! nint_split(f,x,a,b)
  $3 $6:
   pass
 $!('$N',f,x,a,b)
$, haswhen(f,x):
 if $0(f)is $- $1 or f[0]=='Q':
  $! $2
 if f[0]in('when','$H')$* $- $8(f[1],x):
  $! $B
 $( a in f[1:]:
  if haswhen(a,x):
   $! $B
 $! $2
$, gensol(r):
 ns=[w $( w in $e(r)if w[0]=='n' $* w[1:].isdigit()]
 if $/(ns)==1 $* $5($Y(r,ns[0],0)):
  $! ns[0]
 $! $#
$, firstwhen_(f,x):
 if $0(f)is $- $1 or f[0]=='Q':
  $! $2
 if f[0]=='when' $* $- $8(f[1],x):
  $! $B
 $! any([firstwhen_(a,x)$( a in f[1:]])
$, whenpts(f,x,$9):
 if $0(f)is $- $1 or f[0]=='Q':
  $!
 if f[0]=='$H' $* $- $8(f[1],x):
  rs=$r(f[1],x,$2)
  if rs $* rs!='all':
   $( r in rs:
    if($z(r)or gensol(r))$* r $- in $9:
     $9.$%(r)
 if f[0]=='when' $* $- $8(f[1],x):
  cs=[f[1]]
  $F cs:
   c=cs.pop()
   if head(c)in('$*','or','$-'):
    cs.$}(c[1:])
   $= head(c)in('<','>','<=','>=','=','/='):
    rs=$r($_(c[1],c[2]),x,$2)
    if rs $* rs!='all':
     $( r in rs:
      if($z(r)or gensol(r))$* r $- in $9:
       $9.$%(r)
 $( a in f[1:]:
  whenpts(a,x,$9)
$, pickwhen(f,x,t):
 if $0(f)is $- $1 or f[0]=='Q':
  $! f
 if f[0]=='when' $* $- $8(f[1],x):
  ${:
   c=nbool(f[1],{x:t})
  $3 $6:
   $! '$I'
  if c:
   $! pickwhen(f[2],x,t)
  $! pickwhen(f[3],x,t)if $/(f)>3 $& '$I'
 if f[0]=='$H' $* $- $8(f[1],x):
  u=pickwhen(f[1],x,t)
  ${:
   $! u if fv_($Y(u,x,t))>=0 $& $m(u)
  $3 $6:
   $! f
 $! simp((f[0],)+$1(pickwhen(a,x,t)$( a in f[1:]))
$, numpt(v):
 if v=='$P':
  $! 1e300
 if v==('*',-1,'$P'):
  $!-1e300
 $! fv_(v)
$, fv_(v):
 z=$Z(v)
 $! z.$U if $0(z)is $4 $& z
$, whensplit(f,x,a,b):
 pts=[]
 whenpts(f,x,pts)
 lo=numpt(a)
 hi=numpt(b)
 if lo>hi:
  $! $#
 ex=[]
 $( p in pts:
  n=gensol(p)
  if n is $#:
   ex.$%(p)
  $= hi-lo<1e4:
   $( k in $+(-300,301):
    q=$Y(p,n,k)
    if lo<fv_(q)<hi $* q $- in ex:
     ex.$%(q)
 ins=[p $( p in ex if lo<fv_(p)<hi]
 ins.sort(key=fv_)
 ends=[a]+ins+[b]
 $9=[]
 $( i in $+($/(ends)-1):
  p,q=ends[i],ends[i+1]
  pv,qv=numpt(p),numpt(q)
  if pv<-1e299:
   t=qv-1.0
  $= qv>1e299:
   t=pv+1.0
  $&:
   t=0.5*(pv+qv)
  $9.$%((p,q,pickwhen(f,x,t)))
 $! $9
''')
_x(r'''$, whenlimit(f,x,a,dirn):
 pts=[]
 whenpts(f,x,pts)
 if isinf(a):
  t=1e6 if a=='$P' $&-1e6
  $! $|(pickwhen(f,x,t),x,a,dirn)
 av=fv_(a)
 d=1e-6
 $( p in pts:
  q=$H(fv_(p)-av)
  if q>1e-12:
   d=min(d,q/2)
 r=$|(pickwhen(f,x,av+d),x,a,1)if dirn>=0 $& $#
 l=$|(pickwhen(f,x,av-d),x,a,-1)if dirn<=0 $& $#
 if dirn==1:
  $! r
 if dirn==-1:
  $! l
 if r==l:
  $! r
 ${:
  if $5(r)$* $5(l)$* $H($Z(r)-$Z(l))<1e-12:
   $! r
 $3 $6:
  pass
 $! '$I'
$, isinf(v):
 $! v=='$P' or v==('*',-1,'$P')
$, singular_points(f,x,a,b):
 if $-($5(a)$* $5(b)):
  $![]
 ${:
  av=nreal(a)if $- isinf(a)$&(-1e300 if a!='$P' $& 1e300)
  bv=nreal(b)if $- isinf(b)$&(1e300 if b=='$P' $&-1e300)
 $3 $6:
  $![]
 lo,hi=min(av,bv),max(av,bv)
 pts=[]
 dens=[]
 collect_dens(f,x,dens)
 $( d in dens:
  u=u_from_expr(d,x)
  if u is $- $# $* $/(u)<2:
   $7
  if u is $#:
   if hi-lo<1e6:
    $( r in scanzeros(d,x,lo,hi):
     if all([$H(fv_(q)-r)>1e-9 $( q in pts]):
      pts.$%(snapzero(d,x,r))
   $7
  $( r in aberth(u):
   if $H(r.imag)<1e-9 $* lo<r.$U<hi:
    rr=exactify(r.$U)if $H(r.$U-round(r.$U))<1e-12 $& r.$U
    pts.$%(rr)
 pts.sort(key=fv_)
 if av>bv:
  pts.reverse()
 $! pts
$, collect_dens(f,x,$9):
 if $0(f)is $- $1 or f[0]=='Q':
  $!
 if f[0]=='^' $* $G(f[2])$* $c(f[2])<0 $* $- $8(f[1],x):
  $9.$%(f[1])
 if f[0]=='tan' $* $- $8(f[1],x):
  $9.$%(fn('cos',f[1]))
 if f[0]in('ln','log')$* $- $8(f[1],x):
  $9.$%(f[1])
 $( a in f[1:]:
  collect_dens(a,x,$9)
$, scanzeros(d,x,lo,hi,n=400):
 $9=[]
 $, g(t):
  ${:
   v=$Z(d,{x:t})
   $! v.$U if $0(v)is $4 $& v
  $3 $6:
   $! $#
 h=(hi-lo)/n
 t0=lo+h*1e-3
 v0=g(t0)
 $( k in $+(1,n+1):
  t1=lo+h*k-(h*1e-3 if k==n $& 0)
  v1=g(t1)
  if v0 is $- $# $* v1 is $- $# $* v0*v1<=0:
   a,b,fa=t0,t1,v0
   $( it in $+(60):
    m=0.5*(a+b)
    fm=g(m)
    if fm is $#:
     $R
    if(fm<=0)==(fa<=0):
     a,fa=m,fm
    $&:
     b=m
   m=0.5*(a+b)
   fm=g(m)
   if fm is $- $# $* $H(fm)<1e-6 $* lo<m<hi:
    $9.$%(m)
  t0,v0=t1,v1
 $! $9
$, snapzero(d,x,r):
 $( c in(exactify_guess(r/$M.pi),exactify_guess(r)):
  if $0(c)is $C:
   $7
  v=$<(c,'pi')if c is $- exactify_guess(r)$& c
  ${:
   if $H(fv_($Y(d,x,v)))<1e-9:
    $! v
  $3 $6:
   pass
 $! r
NERR=[0.0]
NBUD=[0]
$, nint(f,x,a,b,tol=1e-10):
 NERR[0]=0.0
 NBUD[0]=1500
 r=$#
 if(isinf(a)or isinf(b))$* $-(isinf(a)$* isinf(b)):
  r=nint_osc(f,x,a,b,tol)
 if r is $#:
  r=nint0(f,x,a,b,tol)
  if NERR[0]>1e-7*max(1.0,$H(r))$* $- isinf(a)$* $- isinf(b):
   NERR[0]=0.0
   a0=nreal(a)
   w=nreal(b)-a0
   g=$; u:_nv(f,x,a0+w*u)
   $( k in $+(3):
    g=smooth(g)
    NERR[0]=0.0
    r=w*_gk_adapt(g,0.0,1.0,tol,0)
    if NERR[0]<=1e-7*max(1.0,$H(r)):
     $R
  if NERR[0]>1e-7*max(1.0,$H(r))$*(isinf(a)!=isinf(b)):
   if isinf(a):
    f,a,b=$Y(f,x,$m(x)),$m(b),'$P'
   a0=nreal(a)
   g=$; t:_nv(f,x,a0+t/(1-t))/(1-t)**2 if t<1 $& 0.0
   $( j in $+(3):
    g=smooth(g)
    NERR[0]=0.0
    r=_gk_adapt(g,0.0,1.0,tol,0)
    if NERR[0]<=1e-7*max(1.0,$H(r)):
     $R
  if NERR[0]>1e-7*max(1.0,$H(r)):
   err('Questionable accuracy: the $N may diverge')
 if r!=r or $H(r)==$C('$P'):
  err('Questionable accuracy: the $N may diverge')
 if $0(r)is $4:
  if $H(r.imag)<1e-12*(1+$H(r.$U)):
   $! r.$U
  $! fromcomplex(r)
 $! r
$, nint0(f,x,a,b,tol=1e-10):
 sgn=1.0
 av=a
 bv=b
 if isinf(a)or isinf(b):
  if a=='$P' or b==('*',-1,'$P'):
   $!-nint0(f,x,b,a,tol)
  if isinf(a)$* isinf(b):
   g=$; t:_nv(f,x,t/(1-t*t))*(1+t*t)/(1-t*t)**2
   $! _gk_adapt(g,-1.0,1.0,tol,0)
  if isinf(b):
   a0=nreal(a)
   g=$; t:_nv(f,x,a0+t/(1-t))/(1-t)**2
   $! _gk_adapt(g,0.0,1.0,tol,0)
  b0=nreal(b)
  g=$; t:_nv(f,x,b0-(1-t)/t)/(t*t)
  $! _gk_adapt(g,0.0,1.0,tol,0)
 a0=nreal(a)
 b0=nreal(b)
 g=$; t:_nv(f,x,t)
 $! _gk_adapt(g,a0,b0,tol,0)
$, smooth(g):
 $! $; t:g(t*t*(3-2*t))*6*t*(1-t)
$, nint_split(f,x,a,b):
 pts=[a]+(singular_points(f,x,a,b)or[])+[b]
 r=0
 $( i in $+($/(pts)-1):
  r=$`(r,nint(f,x,pts[i],pts[i+1]))
 $! r
$, trigk(f,x,$9):
 if $0(f)is $- $1 or f[0]=='Q':
  $!
 if f[0]in('sin','cos')$* $- $8(f[1],x):
  lu=$k(f[1],x)
  $9.$%(lu[0]if lu is $- $# $* $5(lu[0])$& $#)
 $( a in f[1:]:
  trigk(a,x,$9)
$, nint_osc(f,x,a,b,tol):
 ks=[]
 trigk(f,x,ks)
 if $- ks or $# in ks:
  $! $#
 k=max([$H(tofl($Z(q)))$( q in ks])
 if k==0:
  $! $#
 sgn_=1.0
 if isinf(a):
  f=$Y(f,x,$m(x))
  a,b=$m(b),'$P'
  if a==('*',-1,('*',-1,'$P')):
   a='$P'
 a0=tofl($Z(a))
 h=$M.pi/k
 g=$; t:_nv(f,x,t)
 sums=[]
 $Q=[]
 s_=0.0
 t=a0
 $( i in $+(40):
  c=_gk_adapt(g,t,t+h,tol,6)
  s_+=c
  $Q.$%($H(c))
  t+=h
  sums.$%(s_)
 if max($Q[-4:])>0.25*max($Q[:4])$* max($Q[-4:])>1e-12:
  err('Questionable accuracy: the $N may diverge')
 est=wynn(sums)
 est2=wynn(sums[:-6])
 if est is $# or est2 is $# or $H(est-est2)>1e-7*max(1.0,$H(est)):
  err('Questionable accuracy: the $N may diverge')
 $! sgn_*est
$, wynn(S):
 n=$/(S)
 e0=[0.0]*(n+1)
 e1=$J(S)
 best=S[-1]
 $( k in $+(1,n):
  e2=[]
  $( j in $+($/(e1)-1):
   d=e1[j+1]-e1[j]
   if d==0:
    $! e1[j+1]
   e2.$%(e0[j+1]+1.0/d)
  if k%2==0 $* e2:
   best=e2[-1]
  e0,e1=e1,e2
  if $/(e1)<2:
   $R
 $! best
$, _nv(f,x,t):
 ${:
  v=$Z(f,{x:t})
 $3 $E:
  $! 0.0
 $3($T,$^):
  $! 0.0
 if $0(v)is $4:
  if $H(v.imag)>1e-12*(1+$H(v.$U)):
   $! v
  v=v.$U
 if v!=v or v in($C('$P'),$C('-$P')):
  $! 0.0
 $! v
''')
_x(r'''XGK=(0.991455371120812639206854697526329,0.949107912342758524526189684047851,
 0.864864423359769072789712788640926,0.741531185599394439863864773280788,
 0.586087235467691130294144845693013,0.405845151377397166906606412076961,
 0.207784955007898467600689403773245,0.0)
WGK=(0.022935322010529224963732008058970,0.063092092629978553290700663189204,
 0.104790010322250183839876322541518,0.140653259715525918745189590510238,
 0.169004726639267902826583426598550,0.190350578064785409913256402421014,
 0.204432940075298892414161999234649,0.209482141084727828012999174891714)
WG=(0.129484966168869693270611432679082,0.279705391489276667901467771423780,
 0.381830050505118944950369775488975,0.417959183673469387755102040816327)
$, _gk(g,a,b):
 c=0.5*(a+b)
 h=0.5*(b-a)
 fc=g(c)
 rk=fc*WGK[7]
 rg=fc*WG[3]
 $( j in $+(7):
  dx=h*XGK[j]
  f1=g(c-dx)
  f2=g(c+dx)
  rk+=WGK[j]*(f1+f2)
  if j%2==1:
   rg+=WG[j//2]*(f1+f2)
 $! rk*h,$H((rk-rg)*h)
$, _gk_adapt(g,a,b,tol,$:):
 r,e=_gk(g,a,b)
 NBUD[0]-=1
 if NBUD[0]<0:
  NERR[0]+=e+1e-6*(1+$H(r))
  $! r
 if e<=tol*max(1.0,$H(r)):
  $! r
 if $:>18:
  NERR[0]+=e
  $! r
 m=0.5*(a+b)
 $! _gk_adapt(g,a,m,tol/2,$:+1)+_gk_adapt(g,m,b,tol/2,$:+1)
BIGP=10**6
$, s_const(c):
 if c==0:
  $!({},BIGP)
 $!({0:c},BIGP)
$, s_val(A):
 if $- A[0]:
  $! A[1]
 m=$#
 $( k in A[0]:
  if m is $# or ncmp(k,m)<0:
   m=k
 $! m
$, cs(c):
 c=$?(c)
 if hasdenom(c):
  c=$.(c)
 $! c
$, s_add(A,B):
 p=A[1]if ncmp(A[1],B[1])<0 $& B[1]
 d={}
 $( S in(A,B):
  $( k in S[0]:
   if ncmp(k,p)<0:
    d[k]=$`(d.get(k,0),S[0][k])
 $9={}
 $( k in d:
  v=cs(d[k])
  if v!=0:
   $9[k]=v
 $!($9,p)
$, s_mul(A,B):
 vA=s_val(A)
 vB=s_val(B)
 p1=nadd(A[1],vB)
 p2=nadd(B[1],vA)
 p=p1 if ncmp(p1,p2)<0 $& p2
 d={}
 $( a in A[0]:
  $( b in B[0]:
   k=nadd(a,b)
   if ncmp(k,p)<0:
    d[k]=$`(d.get(k,0),$<(A[0][a],B[0][b]))
 $9={}
 $( k in d:
  v=cs(d[k])
  if v!=0:
   $9[k]=v
 $!($9,p)
$, s_scale(A,c,shift=0):
 $9={}
 $( k in A[0]:
  v=cs($<(A[0][k],c))
  if v!=0:
   $9[nadd(k,shift)]=v
 $!($9,nadd(A[1],shift))
$, s_lead(A):
 if $- A[0]:
  $d $o()
 v=s_val(A)
 $! v,A[0][v]
$, s_split(A):
 a,c=s_lead(A)
 U=s_scale(A,pw(c,-1),nneg(a))
 U=(dict([(k,U[0][k])$( k in U[0]if k!=0]),U[1])
 $! a,c,U
$, s_powser(U,coefs):
 res=s_const(coefs[0])
 res=(res[0],U[1])
 P=({0:1},BIGP)
 $( k in $+(1,$/(coefs)):
  P=s_mul(P,U)
  if $- P[0]:
   $R
  if coefs[k]!=0:
   res=s_add(res,s_scale(P,coefs[k]))
 $! res
$, nterms(U):
 v=s_val(U)
 if ncmp(v,0)<=0:
  $d $o()
 p=U[1]
 if ncmp(p,BIGP)>=0:
  $! 0 if $- U[0]$& 30
 n=nfloor(ndiv(p,v))+1
 if n>30:
  n=30
 $! n
$, s_pow(A,p):
 if $0(p)is $q $* p>=0:
  R=({0:1},BIGP)
  $( _ in $+(p):
   R=s_mul(R,A)
  $! R
 a,c,U=s_split(A)
 n=nterms(U)if U[0]$& 0
 coefs=[1]
 b=1
 $( k in $+(1,n+1):
  b=$<(b,$V($_(p,k-1),k))
  coefs.$%(b)
 S=s_powser(U,coefs)if U[0]$&({0:1},U[1])
 ap=$<(a,p)
 if $- $w(ap):
  $d $o()
 cp=pw(c,p)
 $! s_scale(S,cp,ap)
$, s_exp(A):
 neg_=[k $( k in A[0]if ncmp(k,0)<0]
 if neg_:
  $d $o()
 c0=A[0].get(0,0)
 U=(dict([(k,A[0][k])$( k in A[0]if k!=0]),A[1])
 shift=0
 if has(c0,LNT):
  cc=$[(c0,LNT)
  if cc is $# or $/(cc)!=2 or $- $w(cc[1]):
   $d $o()
  shift=cc[1]
  c0=cc[0]
 n=nterms(U)if U[0]$& 0
 coefs=[1]
 f=1
 $( k in $+(1,n+1):
  f=f*k
  coefs.$%(Q(1,f))
 S=s_powser(U,coefs)if U[0]$&({0:1},U[1])
 $! s_scale(S,pw('e',c0),shift)
$, s_ln(A):
 a,c,U=s_split(A)
 n=nterms(U)if U[0]$& 0
 coefs=[0]
 $( k in $+(1,n+1):
  coefs.$%(Q((-1)**(k+1),k))
 S=s_powser(U,coefs)if U[0]$&({},U[1])
 base=$`(fn('ln',c),$<(a,LNT))
 $! s_add(S,(({0:base}if base!=0 $&{}),BIGP))
$, s_fun($A,A):
 neg_=[k $( k in A[0]if ncmp(k,0)<0]
 if neg_:
  if $A=='$s':
   a,c=s_lead(A)
   sg=$Z(c)
   sg=1 if($0(sg)is $- $4 $* sg>0)$&-1
   inv_=s_pow(A,-1)
   $! s_add(s_const($<(sg,$x,'pi')),s_scale(s_fun('$s',inv_),-1))
  if $A=='tanh':
   a,c=s_lead(A)
   $! s_const(1 if $Z(c).$U>0 $&-1)
  $d $o()
 c0=A[0].get(0,0)
 if has(c0,LNT):
  $d $o()
 U=(dict([(k,A[0][k])$( k in A[0]if k!=0]),A[1])
 if $A=='$H' or $A=='sign':
  a,c=s_lead(A)
  v=$Z($Y(c,LNT,-1000))if has(c,LNT)$& $Z(c)
  if $0(v)is $4:
   $d $o()
  sg=1 if v>0 $&-1
  if $A=='sign':
   $! s_const(sg)
  $! s_scale(A,sg)
 if $A in('floor','ceiling','ipart','round','$q','fpart'):
  $d $o()
 n=nterms(U)if U[0]$& 0
 z='Z_'
 g=fn($A,z)
 coefs=[$Y(g,z,c0)]
 fact=1
 $( k in $+(1,n+1):
  g=diff(g,z)
  fact*=k
  coefs.$%(cs($V($Y(g,z,c0),fact)))
 $( cc in coefs:
  if has(cc,'$I')or cc=='$I' or has(cc,'$P'):
   $d $o()
 if $- U[0]:
  $! s_const(coefs[0])if $B $& $#
 $! s_powser(U,coefs)
$, ser(e,N):
 if $8(e,TV):
  $! s_const(e)
 if e==TV:
  $!({1:1},BIGP)
 h=e[0]
 if h=='+':
  R=({},BIGP)
  $( a in e[1:]:
   R=s_add(R,ser(a,N))
  $! trunc(R,N)
 if h=='*':
  R=({0:1},BIGP)
  $( a in e[1:]:
   R=trunc(s_mul(R,ser(a,N)),N)
  $! R
 if h=='^':
  b=e[1]
  p=e[2]
  if $8(p,TV):
   B=ser(b,N)
   if $w(p):
    $! trunc(s_pow(B,p),N)
   if $5(p)or $B:
    a,c,U=s_split(B)
    if a!=0:
     $d $o()
    $! trunc(s_pow(B,p),N)
  if $8(b,TV):
   $! trunc(s_exp(s_scale(ser(p,N),fn('ln',b))),N)
  $! trunc(s_exp(s_mul(ser(p,N),s_ln(ser(b,N)))),N)
 if h=='ln':
  $! trunc(s_ln(ser(e[1],N)),N)
 if h=='log':
  b=e[2]if $/(e)>2 $& 10
  $! trunc(s_scale(s_ln(ser(e[1],N)),pw(fn('ln',b),-1)),N)
 if $/(e)==2:
  $! trunc(s_fun(h,ser(e[1],N)),N)
 $d $o()
$, trunc(A,N):
 if ncmp(A[1],N)<=0:
  $! A
 $!(dict([(k,A[0][k])$( k in A[0]if ncmp(k,N)<0]),N)
''')
_x(r'''$, series_t(e,order,need=$#):
 extra=3
 $( _ in $+(4):
  S=ser(e,nadd(order,extra))
  if ncmp(S[1],order)>0 $*(need is $# or S[0]):
   $! S
  extra=extra*2+2
 $! S
$, lead_t(e):
 $( N in(3,6,12,24):
  S=ser(e,N)
  if S[0]:
   v=s_val(S)
   if ncmp(v,S[1])<0:
    $! v,S[0][v]
 $! $#
$, lnt_lim(c):
 n,d=numer_denom(c)
 cn=$[(n,LNT)
 cd=$[(d,LNT)
 if cn is $# or cd is $#:
  $d $o()
 p=$/(cn)-1
 q=$/(cd)-1
 if p<q:
  $! 0
 if p==q:
  $! $V(cn[p],cd[q])
 v=lnt_sign(c)
 if $0(v)is $4:
  $! '$I'
 $! '$P' if v>0 $&('*',-1,'$P')
$, lnt_sign(c):
 cc=$[(c,LNT)
 if cc is $#:
  v=$Z($Y(c,LNT,-1e6))
  $! v
 k=$/(cc)-1
 lead=cc[k]
 v=$Z(lead)
 if $0(v)is $4:
  $! v
 if k%2:
  v=-v
 $! v
$, $|(f,x,a,dirn=0):
 $! infnorm(limit0(f,x,a,dirn))
$, infnorm(r):
 if $)(r,'*')$*('$P' in r[1:]):
  c=$K([b $( b in r[1:]if b!='$P'])
  if $5(c):
   ${:
    v=fv_(c)
    $! '$P' if v>0 $&(('*',-1,'$P')if v<0 $& '$I')
   $3 $6:
    pass
 $! r
$, limit0(f,x,a,dirn=0):
 if $)(f,'$J')or $)(f,'mat'):
  $! mapexpr($; g:$|(g,x,a,dirn),f)
 if $8(f,x):
  $! f
 if haswhen(f,x)$* $5(a)$* firstwhen_(f,x):
  $! whenlimit(f,x,a,dirn)
 if hashead(f,'fact')$* isinf(a):
  g=stirling(factnorm(f,x),x)
  if g!=f:
   $! $|(g,x,a,dirn)
 if $5(a):
  r=lim_bounded(f,x,a,dirn)
  if r is $- $#:
   $! r
 if a=='$P' or a==('*',-1,'$P'):
  sub_=pw(TV,-1)if a=='$P' $& $m(pw(TV,-1))
  $! lim_side(f,x,sub_,a)
 if dirn==0 $* $- has_disc(f):
  ${:
   v=$Y(f,x,a)
   if v!='$I' $* $8(v,'$I')$* $- has(v,'$P'):
    v2=v
    if $5(v2):
     vv=$Z(v2)
     if $0(vv)is $4 $* $H(vv.imag)>1e-12 $* $8(f,'i'):
      $d $T
    $! v
  $3($S,$E,$T,TypeError):
   pass
 if dirn==1:
  $! lim_side(f,x,$`(a,TV),a)
 if dirn==-1:
  $! lim_side(f,x,$_(a,TV),a)
 r=lim_side(f,x,$`(a,TV),a)
 l=lim_side(f,x,$_(a,TV),a)
 if r==l:
  $! r
 if $)(r,'$|')or $)(l,'$|'):
  $!('$|',f,x,a)
 ${:
  if $5(r)$* $5(l)$* $- has(r,'$P')$* $- has(l,'$P'):
   if $H($Z(r)-$Z(l))<1e-12:
    $! r
 $3 $6:
  pass
 $! '$I'
$, hashead(f,h):
 if $0(f)is $- $1 or f[0]=='Q':
  $! $2
 $! f[0]==h or any([hashead(b,h)$( b in f[1:]])
STEPF=('floor','ceiling','fpart','ipart','$q','round')
$, factnorm(f,x):
 fs=[]
 $, walk(e):
  if $0(e)is $- $1 or e[0]=='Q':
   $!
  if e[0]=='fact' $* $- $8(e[1],x):
   fs.$%(e[1])
  $( b in e[1:]:
   walk(b)
 walk(f)
 if $- fs:
  $! f
 base=fs[0]
 $( u in fs:
  d=$_(base,u)
  if $i(d)$* d>0:
   base=u
 $, rep(e):
  if $0(e)is $- $1 or e[0]=='Q':
   $! e
  if e[0]=='fact' $* $- $8(e[1],x):
   k=$_(e[1],base)
   if $i(k)$* 0<k<=50:
    $! $K([$`(base,j)$( j in $+(1,k+1)]+[fn('fact',base)])
   $! e
  $! simp((e[0],)+$1(rep(b)$( b in e[1:]))
 $! $.(rep(f))
$, stirling(f,x):
 if $0(f)is $- $1 or f[0]=='Q':
  $! f
 if f[0]=='fact' $* $- $8(f[1],x):
  u=stirling(f[1],x)
  $! $<($O($<(2,'pi',u)),pw($V(u,'e'),u))
 $! simp((f[0],)+$1(stirling(b,x)$( b in f[1:]))
$, bounded_nodes(f,x,a,dirn,$9):
 if $0(f)is $- $1 or f[0]=='Q':
  $!
 $( b in f[1:]:
  bounded_nodes(b,x,a,dirn,$9)
 if $/(f)==2 $* $- $8(f[1],x)$* f[0]in STEPF+('sin','cos'):
  ${:
   L=$|(f[1],x,a,dirn)
  $3 $6:
   $!
  if L in('$P',('*',-1,'$P'))or L=='$I' or $)(L,'$|'):
   if(f,1)$- in $9:
    $9.$%((f,1))
  $= f[0]in STEPF $* $- isinf(a):
   if(f,0)$- in $9:
    $9.$%((f,0))
$, lim_bounded(f,x,a,dirn):
 ns=[]
 bounded_nodes(f,x,a,dirn,ns)
 if $- ns:
  $! $#
 if $- isinf(a):
  if dirn==0:
   r=lim_bounded(f,x,a,1)
   l=lim_bounded(f,x,a,-1)
   if r is $# or l is $#:
    $! $#
   $! r if r==l $& '$I'
  stp=[n $( n,k in ns if k==0]
  ns=[n $( n,k in ns if k==1]
  if stp:
   t=fv_(a)+dirn*1e-7*(1+$H(fv_(a)))
   g=f
   $( n in stp:
    ${:
     g=replnode_(g,n,exactify($Z(n,{x:t})))
    $3 $6:
     $! $#
   $! $|(g,x,a,dirn)
 $&:
  ns=[n $( n,k in ns]
 if $- ns:
  $! $#
 C='C_'
 reps=[]
 $( n in ns:
  if n[0]in('sin','cos'):
   reps.$%((n,C,(-1,0,1)))
  $= n[0]in('floor','$q','ipart'):
   reps.$%((n,$_(n[1],C),(0,Q(1,2),1)))
  $= n[0]=='ceiling':
   reps.$%((n,$`(n[1],C),(0,Q(1,2),1)))
  $= n[0]=='round':
   reps.$%((n,$`(n[1],C),(Q(-1,2),0,Q(1,2))))
  $&:
   reps.$%((n,C,(0,Q(1,2),1)))
 if $/(reps)>1:
  $! $#
 n,r,cs=reps[0]
 g=replnode_(f,n,r)
 $g=[]
 $( c in cs:
  v=$|($Y(g,C,c),x,a,dirn)
  if $)(v,'$|'):
   $! $#
  $g.$%(v)
 if $g[0]==$g[1]==$g[2]$* $g[0]!='$I':
  $! $g[0]
 $! '$I'
$, replnode_(f,w,r):
 if f==w:
  $! r
 if $0(f)is $- $1 or f[0]=='Q':
  $! f
 $! simp((f[0],)+$1(replnode_(b,w,r)$( b in f[1:]))
$, has_disc(f):
 if $0(f)is $- $1 or f[0]=='Q':
  $! $2
 if f[0]in('floor','ceiling','sign','ipart','round','fpart','$q','when','$H','mod'):
  $! $B
 $( a in f[1:]:
  if has_disc(a):
   $! $B
 $! $2
''')
_x(r'''$, lim_side(f,x,sub_,a):
 g=$Y(f,x,sub_)
 ${:
  r=lead_t(g)
  if r is $#:
   $! 0
  al,c=r
  if has(c,TV):
   $d $o()
  if ncmp(al,0)>0:
   $! 0
  if has(c,LNT)$* al==0:
   $! lnt_lim(c)
  if has(c,LNT):
   v=lnt_sign(c)
   if $0(v)is $4:
    $! '$I'
   if v==0:
    $d $o()
   $! '$P' if v>0 $&('*',-1,'$P')
  if al==0:
   $! c
  if $- $5(c):
   $! $<(c,'$P')
  v=$Z(c)
  if $0(v)is $4:
   $! '$I'
  $! '$P' if v>0 $&('*',-1,'$P')
 $3($o,$S,$E,$T,TypeError,$^):
  pass
 r=lim_lh(g,0)
 if r is $- $#:
  $! r
 r=lim_log(g)
 if r is $- $#:
  $! r
 $! lim_num(g,a)
$, lnexp(g):
 h=head(g)
 if h=='*':
  $! $>([lnexp(b)$( b in g[1:]])
 if h=='^':
  if g[1]=='e':
   $! g[2]
  $! $<(g[2],lnexp(g[1]))
 if $G(g)$* $c(g)>0:
  $! fn('ln',g)
 $! fn('ln',g)
$, lim_log(g,$:=0):
 if head(g)$- in('*','^'):
  $! $#
 v=$#
 $( t in(1e-3,1e-2,1e-1):
  ${:
   v=$Z(g,{TV:t})
  $3 $6:
   v=$#
  if v is $- $# $* $0(v)is $- $4 $* v==v $* v!=0 $* $H(v)!=$C('$P'):
   $R
  v=$#
 if v is $#:
  $! $#
 sg=1 if v>0 $&-1
 L=lim_val($.(lnexp($<(sg,g))),$:)
 if L is $# or $)(L,'$|')or L=='$I':
  $! $#
 if L=='$P':
  $! '$P' if sg>0 $&('*',-1,'$P')
 if L==('*',-1,'$P'):
  $! 0
 if $5(L):
  $! $<(sg,pw('e',L))
 $! $#
$, lim_val(g,$:):
 ${:
  r=lead_t(g)
  if r is $#:
   $! 0
  al,c=r
  if has(c,TV):
   $d $o()
  if ncmp(al,0)>0:
   $! 0
  if has(c,LNT)$* al==0:
   $! lnt_lim(c)
  if has(c,LNT):
   v=lnt_sign(c)
   $! '$P' if v>0 $&('*',-1,'$P')
  if al==0:
   $! c
  v=$Z(c)
  $! '$P' if v>0 $&('*',-1,'$P')
 $3($o,$S,$E,$T,TypeError,$^):
  pass
 r=lim_lh(g,$:+1)
 if r is $# $* $:<3:
  r=lim_log(g,$:+1)
 $! r
$, lim_lh(g,$:):
 if $:>4:
  $! $#
 if $8(g,TV):
  $! g
 h=head(g)
 if h=='^' $* $- $8(g[2],TV):
  L=lim_val($<(g[2],fn('ln',g[1])),$:)
  if L is $#:
   $! $#
  $! pw('e',L)
 if h=='^' $* $G(g[2]):
  L=lim_val(g[1],$:)
  if L is $#:
   $! $#
  if L==0 $* $c(g[2])<0:
   $! '$P'
  $! pw(L,g[2])
 if h=='*':
  nu,de=numer_denom(g)
  if de!=1:
   ln_=lim_val(nu,$:)
   ld=lim_val(de,$:)
   if ln_ is $# or ld is $#:
    $! $#
   if(ln_==0 $* ld==0)or(isinfv(ln_)$* isinfv(ld)):
    $! lim_val($.($V(diff(nu,TV),diff(de,TV))),$:)
   if ld==0:
    s=$Z($Y(de,TV,1e-9))
    sn=$Z(ln_)if $5(ln_)$* $- isinfv(ln_)$&(1 if ln_=='$P' $&-1)
    $! '$P' if(s.$U if $0(s)is $4 $& s)*(sn.$U if $0(sn)is $4 $& sn)>0 $&('*',-1,'$P')
   $! $V(ln_,ld)
  ls=[lim_val(fct,$:)$( fct in g[1:]]
  if $# in ls:
   $! $#
  zero=[i $( i in $+($/(ls))if ls[i]==0]
  infs=[i $( i in $+($/(ls))if isinfv(ls[i])]
  if zero $* infs:
   r=lim_log(g,$:+1)
   if r is $- $#:
    $! r
   i=zero[0]
   j=infs[0]
   $a=$K([g[k+1]$( k in $+($/(ls))if k!=i $* k!=j])
   q=$V(g[i+1],pw(g[j+1],-1))
   r=lim_val(q,$:)
   if r is $#:
    $! $#
   $! $<(r,lim_val($a,$:))
  $! $K(ls)
 if h=='+':
  ls=[lim_val(t,$:)$( t in g[1:]]
  if $# in ls:
   $! $#
  r=$>(ls)
  if r!='$I':
   $! r
  ii=[k $( k in $+($/(ls))if isinfv(ls[k])]
  if $- ii:
   $! $#
  $( i in ii:
   A=g[i+1]
   $a=$>([g[k+1]$( k in $+($/(ls))if k!=i])
   q=lim_val($.($V($a,A)),$:)
   if q is $# or q=='$I' or isinfv(q)or q==-1:
    $7
   $! $<(ls[i],$`(1,q))
  $! $#
 if $0(g)is $1 $* $/(g)==2:
  L=lim_val(g[1],$:)
  if L is $#:
   $! $#
  $! fn(h,L)
 $! $#
$, isinfv(v):
 $! v=='$P' or v==('*',-1,'$P')
$, lim_num(g,a):
 ${:
  $g=[]
  $( k in $+(4,9):
   t=10.0**(-k)
   $g.$%($Z(g,{TV:t}))
  v1=$g[-1]
  v2=$g[-2]
  if $0(v1)is $4 or $0(v2)is $4:
   $!('$|',g)
  if $H(v1)>1e12 $* $H(v1)>$H(v2):
   $! '$P' if v1>0 $&('*',-1,'$P')
  if $H(v1)<1e-6 $* $H(v1)<$H($g[-3])$* $H(v2)<$H($g[-3]):
   $! 0
  if $H(v1-v2)<1e-6*(1+$H(v1)):
   $! exactify_guess(v1)
 $3 $6:
  pass
 $!('$|',g)
$, exactify_guess(v):
 r=float2rat(v,1e-9)
 n,d=nd(r)
 if d<1000:
  $! r
 $! v
$, series_at(f,x,a,order):
 if a=='$P' or a==('*',-1,'$P'):
  sub_=pw(TV,-1)if a=='$P' $& $m(pw(TV,-1))
  back=pw(x,-1)if a=='$P' $& $m(pw(x,-1))
 $&:
  sub_=$`(a,TV)
  back=$_(x,a)
 g=$Y(f,x,sub_)
 S=series_t(g,order)
 $! S,back
$, taylor(f,x,n,a=0):
 ${:
  S,back=series_at(f,x,a,n)
 $3($o,$S,$E,$T):
  $! taylor_d(f,x,n,a)
 $Q=[]
 $( k in S[0]:
  if ncmp(k,n)>0:
   $7
  if $-($0(k)is $q $* k>=0)or has(S[0][k],LNT):
   $!('taylor',f,x,n,a)
  $Q.$%($<(S[0][k],pw(back,k)))
 $! $>($Q)
$, taylor_d(f,x,n,a):
 $Q=[]
 g=f
 fact=1
 $( k in $+(n+1):
  if k:
   fact*=k
   g=diff(g,x)
  v=$Y(g,x,a)
  if has(v,'$I')or v=='$I' or has(v,'$P'):
   $!('taylor',f,x,n,a)
  $Q.$%($<($V(v,fact),pw($_(x,a),k)))
 $! $>($Q)
$, series_cmd(f,x,n,a=0):
 ${:
  S,back=series_at(f,x,a,n)
 $3($o,$S,$E,$T):
  $!('series',f,x,n,a)
 $Q=[]
 lnback=fn('ln',back)if $-(a=='$P' or a==('*',-1,'$P'))$& $m(fn('ln',fn('$H',x)))
 $( k in S[0]:
  if ncmp(k,n)>0:
   $7
  c=$Y(S[0][k],LNT,lnback)
  $Q.$%($<(c,pw(back,k)))
 $! $>($Q)
''')
_x(r'''$, dominant(f,x,a=0):
 if a=='$P' or a==('*',-1,'$P'):
  sub_=pw(TV,-1)if a=='$P' $& $m(pw(TV,-1))
  back=pw(x,-1)if a=='$P' $& $m(pw(x,-1))
  lnback=$m(fn('ln',fn('$H',x)))
 $&:
  sub_=$`(a,TV)
  back=$_(x,a)
  lnback=fn('ln',back)
 ${:
  r=lead_t($Y(f,x,sub_))
 $3($o,$S,$E,$T):
  $!('dominantterm',f,x,a)
 if r is $#:
  $! 0
 k,c=r
 $! $<($Y(c,LNT,lnback),pw(back,k))
$, bern(n):
 B=[1]
 $( m in $+(1,n+1):
  s=0
  c=1
  $( k in $+(m):
   s=nadd(s,nmul(binom(m+1,k),B[k]))
  B.$%(nneg(ndiv(s,m+1)))
 $! B
$, binom(n,k):
 if k<0 or k>n:
  $! 0
 r=1
 $( i in $+(1,k+1):
  r=r*(n-k+i)//i
 $! r
$, powsum(j,n):
 B=bern(j)
 if j>=1:
  B[1]=Q(1,2)
 $Q=[]
 $( i in $+(j+1):
  $Q.$%($<(binom(j+1,i),B[i],pw(n,j+1-i)))
 $! $<(Q(1,j+1),$>($Q))
ZETA={2:('Q',1,6),4:('Q',1,90),6:('Q',1,945),8:('Q',1,9450),10:('Q',1,93555)}
$, sumseq(f,k,a,b):
 if $i(a)$* $i(b):
  if b<a-1:
   $! $m(sumseq(f,k,b+1,a-1))
  if b-a<=300:
   $Q=[$Y(f,k,j)$( j in $+(a,b+1)]
   $! $>($Q)
 if $8(f,k):
  $! $<(f,$`($_(b,a),1))
 cs_=$[(f,k)
 if cs_ is $- $# $* b!='$P':
  res=[]
  $( j in $+($/(cs_)):
   if cs_[j]!=0:
    if j==0:
     res.$%($<(cs_[0],$`($_(b,a),1)))
    $&:
     res.$%($<(cs_[j],$_(powsum(j,b),powsum(j,$_(a,1)))))
  $! $?($>(res))
 r=geomsum(f,k,a,b)
 if r is $- $#:
  $! r
 r=telesum(f,k,a,b)
 if r is $- $#:
  $! r
 if b=='$P' $* $i(a)$* has(f,('fact',k)):
  g=$<(f,('fact',k))
  gs=geomsum(g,k,0,'$P')if $2 $& $#
  cr=expsum(g,k)
  if cr is $- $#:
   C,r=cr
   tot=$<(C,pw('e',r))
   if a>0:
    tot=$_(tot,$>([$<(C,$V(pw(r,j),fact_(j)))$( j in $+(a)]))
   $! tot
 if b=='$P' $* $i(a):
  nu,de=numer_denom(f)
  if $8(nu,k):
   dd=$[(de,k)
   if dd is $- $# $* $/(dd)>=2 $* all([c==0 $( c in dd[:-1]]):
    p=$/(dd)-1
    if p==1:
     $! '$P' if $Z($V(nu,dd[-1])).$U>0 $&('*',-1,'$P')
    if p in ZETA $* a>=1:
     z=$<(ZETA[p],pw('pi',p))
     z=$_(z,$>([pw(j,-p)$( j in $+(1,a)]))
     $! $<($V(nu,dd[-1]),z)
 if($i(a)or $5(a))$*(b=='$P' or $i(b))$* freeofall(f,[s $( s in $e(f)if s!=k]):
  $! nsum(f,k,a,b)
 $!('sumseq',f,k,a,b)
$, expsum(g,k):
 if $8(g,k):
  $! g,1
 fs=g[1:]if $)(g,'*')$&(g,)
 C=[]
 r=$#
 $( h in fs:
  if $8(h,k):
   C.$%(h)
  $= $)(h,'^')$* $8(h[1],k)$* h[2]==k $* r is $#:
   r=h[1]
  $= $)(h,'^')$* $8(h[1],k)$* $k(h[2],k)$* $k(h[2],k)[1]==0 $* r is $#:
   r=pw(h[1],$k(h[2],k)[0])
  $&:
   $! $#
 if r is $#:
  $! $#
 $! $K(C),r
$, geomsum(f,k,a,b):
 fs=f[1:]if $)(f,'*')$&(f,)
 C=[]
 base=$#
 ex=$#
 $( g in fs:
  if $8(g,k):
   C.$%(g)
  $= $)(g,'^')$* $8(g[1],k)$* $k(g[2],k):
   if base is $- $#:
    if g[1]==base or($G(g[1])$* $G(base)):
     lp=$k(g[2],k)
     lb=$k(ex,k)
     if lp[0]==1 $* lb[0]==1:
      C.$%(pw(g[1],lp[1]))
      C.$%(pw(base,lb[1]))
      base=$<(base,g[1])
      ex=k
      $7
    $! $#
   base=g[1]
   ex=g[2]
  $&:
   $! $#
 if base is $#:
  $! $#
 p,q=$k(ex,k)
 r=pw(base,p)
 Cq=$<($K(C),pw(base,q))
 if b=='$P':
  if $5(r):
   v=$Z(r)
   if $H(v)<1:
    $! $V($<(Cq,pw(r,a)),$_(1,r))
   $! '$P' if $Z(Cq).$U>0 $* v.$U>0 $& '$I'
  $! $#
 if r==1:
  $! $<(Cq,$`($_(b,a),1))
 $! $V($<(Cq,$_(pw(r,$`(b,1)),pw(r,a))),$_(r,1))
$, telesum(f,k,a,b):
 if $- hasdenom(f):
  $! $#
 pf=partfrac(f,k)
 if pf is $#:
  $! $#
 $Q=pf[1:]if $)(pf,'+')$&(pf,)
 groups=[]
 $( t in $Q:
  c,r=$f(t)
  if $)(r,'^')$* r[2]==-1:
   lb=$k(r[1],k)
   if lb is $# or lb[0]!=1:
    $! $#
   groups.$%((c,lb[1]))
  $= $8(t,k):
   $! $#
  $&:
   $! $#
 if $- groups:
  $! $#
 s0=groups[0][1]
 tot=0
 ms=[]
 $( c,s in groups:
  m=nsub(s,s0)if $w(s)$* $w(s0)$& $#
  if m is $# or $- $i(m):
   $! $#
  ms.$%(m)
  tot=$`(tot,c)
 if tot!=0:
  if b=='$P':
   $! '$P'
  $! $#
 mn=min(ms)
 if mn!=0:
  s0=nadd(s0,mn)
  ms=[m-mn $( m in ms]
 M=max(ms)
 res=[]
 $( idx in $+($/(groups)):
  c=groups[idx][0]
  m=ms[idx]
  part=[]
  $( j in $+(m,M):
   part.$%(pw($`(a,j,s0),-1))
  if b!='$P':
   $( j in $+(1,m+1):
    part.$%(pw($`(b,j,s0),-1))
  res.$%($<(c,$>(part)))
 $! $>(res)
$, nsum(f,k,a,b):
 av=$q(nreal(a))
 if b=='$P':
  $! nsum_inf(f,k,av)
 s=0.0
 $( n in $+(av,$q(b)+1):
  s+=$Z(f,{k:$C(n)})
 $! s
''')
_x(r'''$, nsum_inf(f,k,av):
 L=$|(f,k,'$P')
 if L!=0 $* $- $)(L,'$|'):
  if L=='$I' or $- $5(L):
   $! '$I'
  ${:
   v=fv_(L)
  $3 $6:
   $! '$I'
  $! '$P' if v>0 $&('*',-1,'$P')
 $, t(n):
  z=$Z(f,{k:$C(n)})
  if $0(z)is $4:
   if $H(z.imag)>1e-12*(1+$H(z.$U)):
    $d $T
   z=z.$U
  $! z
 first=[t(n)$( n in $+(av,av+40)]
 tail=first[10:]
 if all([tail[i]*tail[i+1]<0 $( i in $+($/(tail)-1)]):
  S=[]
  s_=0.0
  $( n in $+(av,av+60):
   s_+=t(n)
   S.$%(s_)
  e1=wynn(S)
  e2=wynn(S[:-10])
  if $H(e1-e2)>1e-8*max(1.0,$H(e1)):
   err('Questionable accuracy: the series may diverge')
  $! e1
 N=av+200
 tn=[t(n)$( n in $+(N,N+20)]
 if all([v>0 $( v in tn])or all([v<0 $( v in tn]):
  ${:
   fe=exactify(f)
  $3 $6:
   fe=f
  I=defint(fe,k,N,'$P')
  if I in('$P',('*',-1,'$P')):
   $! I
  if $- $5(I)or has(I,'$I'):
   I=nint(f,k,N,'$P')
  s_=0.0
  $( n in $+(av,N):
   s_+=t(n)
  d1=diff(f,k)
  d3=diff(diff(d1,k),k)
  s_+=fv_(I)+t(N)/2-fv_($Y(d1,k,N))/12+fv_($Y(d3,k,N))/720
  $! s_
 s_=0.0
 prev=$#
 $( n in $+(av,av+20000):
  s_+=t(n)
  if n-av in(9999,19999):
   if prev is $- $# $* $H(s_-prev)>1e-9*max(1.0,$H(s_)):
    err('Questionable accuracy: the series may diverge')
   prev=s_
 $! s_
$, prodseq(f,k,a,b):
 if $i(a)$* $i(b):
  if b<a-1:
   $! pw(prodseq(f,k,b+1,a-1),-1)
  if b-a<=300:
   $! $K([$Y(f,k,j)$( j in $+(a,b+1)])
 if $8(f,k):
  $! pw(f,$`($_(b,a),1))
 if f==k $* a==1:
  $! fn('fact',b)
 if $)(f,'^')$* f[1]==k $* $i(f[2])$* a==1:
  $! pw(fn('fact',b),f[2])
 if $)(f,'*')$* a==1:
  c=[g $( g in f[1:]if $8(g,k)]
  r=[g $( g in f[1:]if $- $8(g,k)]
  if c $* $/(r)==1:
   rr=prodseq(r[0],k,a,b)
   if $- $)(rr,'prodseq'):
    $! $<(pw($K(c),b),rr)
 fs=f[1:]if $)(f,'*')$&(f,)
 if $)(f,'^')$* $8(f[1],k):
  $! pw(f[1],sumseq(f[2],k,a,b))
 $!('prodseq',f,k,a,b)
$, texpand(e):
 if $0(e)is $- $1 or e[0]=='Q':
  $! e
 $L=[texpand(a)$( a in e[1:]]
 e=simp((e[0],)+$1($L))
 if $0(e)is $- $1:
  $! e
 h=e[0]
 if h in('sin','cos','tan')$* $/(e)==2:
  u=e[1]
  if h=='tan':
   $! texpand($V(fn('sin',u),fn('cos',u)))
  if $)(u,'+'):
   a=u[1]
   b=$>($J(u[2:]))
   sa,ca=texpand(fn('sin',a)),texpand(fn('cos',a))
   sb,cb=texpand(fn('sin',b)),texpand(fn('cos',b))
   if h=='sin':
    $! $?($`($<(sa,cb),$<(ca,sb)))
   $! $?($_($<(ca,cb),$<(sa,sb)))
  c,r=$f(u)
  if $i(c)$* c>1 $* c<=30:
   s1=texpand(fn('sin',r))
   c1=texpand(fn('cos',r))
   z=expand_pow($`(c1,$<('i',s1)),c)
   re_,im_=reim(z)
   $! $?(im_ if h=='sin' $& re_)
 $! e
$, trigfactor(f):
 if head(f)in('sin','cos')$* $/(f)==2:
  $![(f[0],f[1])]
 if $)(f,'^')$* head(f[1])in('sin','cos')$* $i(f[2])$* f[2]>0:
  $![(f[1][0],f[1][1])]*f[2]
 $! $#
$, tmul(a,b):
 n1,u=a
 n2,v=b
 if n1=='sin' $* n2=='sin':
  $! $<($x,$_(fn('cos',$_(u,v)),fn('cos',$`(u,v))))
 if n1=='cos' $* n2=='cos':
  $! $<($x,$`(fn('cos',$_(u,v)),fn('cos',$`(u,v))))
 if n1=='cos':
  u,v=v,u
 $! $<($x,$`(fn('sin',$`(u,v)),fn('sin',$_(u,v))))
$, tcollect(e):
 if $0(e)is $- $1 or e[0]=='Q':
  $! e
 e=$?(e)
 if $)(e,'+'):
  $! $>([tcollect_term(t)$( t in e[1:]])
 $! tcollect_term(e)
$, tcollect_term(t):
 fs=t[1:]if $)(t,'*')$&(t,)
 other=[]
 trig=[]
 $( f in fs:
  tf=trigfactor(f)
  if tf is $#:
   other.$%(f)
  $&:
   trig.$}(tf)
 if $/(trig)<=1:
  $! t
 acc=fn(trig[0][0],trig[0][1])
 $( tf in trig[1:]:
  $Q=acc[1:]if $)(acc,'+')$&(acc,)
  $9=[]
  $( term in $Q:
   c,r=$f(term)
   ftf=trigfactor(r)
   if ftf is $# or $/(ftf)!=1:
    if freeof_trig(r):
     $9.$%($<(term,fn(tf[0],tf[1])))
     $7
    $9.$%($<(term,fn(tf[0],tf[1])))
    $7
   $9.$%($<(c,tmul(ftf[0],tf)))
  acc=$?($>($9))
 $! $?($<($K(other),acc))
$, trigargs(e,$9):
 if $0(e)is $- $1 or e[0]=='Q':
  $!
 if e[0]in('sin','cos')$* $/(e)==2:
  if e[1]$- in $9:
   $9.$%(e[1])
 $( a in e[1:]:
  trigargs(a,$9)
$, pyth(e):
 us=[]
 trigargs(e,us)
 if $- us:
  $! e
 best=e
 bl=$/(fmt(e))
 $( u in us:
  s=fn('sin',u)
  c=fn('cos',u)
  $( a,b in((s,c),(c,s)):
   g=rsquare(e,a,b)
   if g is $- $#:
    g=$?(g)
    l=$/(fmt(g))
    if l<bl:
     best=g
     bl=l
 $! best
$, rsquare(e,a,b):
 if $0(e)is $- $1 or e[0]=='Q':
  $! e
 if e[0]=='^' $* e[1]==a $* $i(e[2])$* e[2]>=2:
  $! $<(pw(a,e[2]-2),$_(1,pw(b,2)))
 $! simp((e[0],)+$1(rsquare(t,a,b)$( t in e[1:]))
$, freeof_trig(e):
 $! $- hastrig(e)
$, arclen(f,x,a,b):
 g=$.($?($`(1,pw(diff(f,x),2))))
 $! defint($O(g),x,a,b)
$, tangentline(f,x,a):
 d=$Y(diff(f,x),x,a)
 $! $?($`($Y(f,x,a),$<(d,$_(x,a))))
$, normalline(f,x,a):
 d=$Y(diff(f,x),x,a)
 if d==0:
  $!('=',x,a)
 $! $?($_($Y(f,x,a),$V($_(x,a),d)))
$, impdif(eq,x,y,n=1):
 F=$_(eq[1],eq[2])if $)(eq,'=')$& eq
 yp=$.($m($V(diff(F,x),diff(F,y))))
 d=yp
 $( _ in $+(n-1):
  d=$.($`(diff(d,x),$<(diff(d,y),yp)))
 $! nice(d)
$, avgrc(f,x,v,h=Q(1,1000)):
 $! $V($_($Y(f,x,$`(v,h)),$Y(f,x,v)),h)
$, centraldiff(f,x,v,h=Q(1,1000)):
 $! $V($_($Y(f,x,$`(v,h)),$Y(f,x,$_(v,h))),$<(2,h))
$, untan(e):
 if $0(e)is $- $1 or e[0]=='Q':
  $! e
 $L=[untan(a)$( a in e[1:]]
 if e[0]=='tan' $* $/($L)==1:
  $! $V(fn('sin',$L[0]),fn('cos',$L[0]))
 $! simp((e[0],)+$1($L))
$, pyth_to(e,which):
 other='cos' if which=='sin' $& 'sin'
 e=untan(e)
 us=[]
 trigargs(e,us)
 $( u in us:
  e=rsquare(e,fn(other,u),fn(which,u))
 $! $?(e)
''')
_x(r'''$, unhold(e):
 if $)(e,'hold'):
  $! simp(e[1])
 $! e
$, $z(e):
 if $- $5(e):
  $! $2
 ${:
  v=$Z(e)
 $3 $6:
  $! $2
 if $0(v)is $4:
  $! $H(v.imag)<=1e-10*(1+$H(v.$U))
 $! v==v
$, fv(e):
 v=$Z(e)
 if $0(v)is $4:
  $! v.$U
 $! v
$, clean(e):
 e=$.(e)
 if $b(e):
  e=evalf(e)
  if has(e,'i'):
   r,i=reim(e)
   if $0(i)is $C $* $H(i)<1e-11*(1+$H(tofl(r)if $G(r)$& 1)):
    e=r
 $! e
class Sols:
 $, __init__($@):
  $@.$g=[]
  $@.all=$2
  $@.fail=$2
  $@.ints=[]
$, $r(f,x,$D=$2,$:=0):
 if $:>6:
  $! $#
 f=$.(unhold(f))
 if $8(f,x):
  if f==0:
   $! 'all'
  if $5(f)or $- $D:
   $![]
  $![]
 nu=numer_of(f)
 if $8(nu,x):
  $![]if nu!=0 $& 'all'
 if $- $D $* firstabs(nu,x)is $- $# $* $:<4:
  r=abs_cases(nu,x,[],$:)
  if r is $- $# $* r!='interval':
   $![q $( q in r if valid(f,x,q,$D)]
 $j=solve_num(nu,x,$D,$:)
 numeric=$j is $# or($j!='all' $* any([$b(q)$( q in $j]))
 if numeric $* hastrigx(nu,x)$* $:<3:
  ${:
   g=tcollect(nu)
  $3 $6:
   g=nu
  if g!=nu:
   s2=$r(g,x,$D,$:+2)
   if s2 is $- $# $* s2!='all' $* $- any([$b(q)$( q in s2]):
    $j=s2
 if $j is $# or $j=='all':
  $! $j
 $9=[]
 $( s in $j:
  if valid(f,x,s,$D):
   $9.$%(s)
 $! $9
$, numer_of(f):
 ${:
  c=comdenom(f)
 $3 $6:
  c=f
 $! numer_denom(c)[0]
$, valid(f,x,s,$D):
 if has(s,'n1')or $e(s)$* $- $5(s):
  $! $B
 ${:
  v=$Y(f,x,s)
  if v=='$I' or has(v,'$I'):
   $! $2
  if has(v,'$P'):
   $! $2
  vv=$Z(v)
  mag=1.0
  if $0(vv)is $4:
   ok=$H(vv)<1e-6
  $&:
   ok=$H(vv)<1e-6
  if $- ok:
   ${:
    sc=$Z(s)
    ok=$H(vv)<1e-8*(1+$H(sc))*1e4
   $3 $6:
    ok=$2
  if $- $D:
   sv=$Z(s)
   if $0(sv)is $4 $* $H(sv.imag)>1e-9*(1+$H(sv.$U)):
    $! $2
  $! ok
 $3($S,$E,$T,TypeError,$^):
  $! $2
$, solve_num(nu,x,$D,$:):
 d=degree(nu,x)
 if d is $- $#:
  r=solve_poly(nu,x,$D)
  if r is $- $#:
   $! r
 fac=factor_expr(nu)
 fac=fac[1]if $)(fac,'hold')$& fac
 if $)(fac,'*'):
  allsol=[]
  $( g in fac[1:]:
   if $)(g,'^')$* $G(g[2])$* $c(g[2])>0:
    g=g[1]
   if $8(g,x):
    $7
   r=$r(g,x,$D,$:+1)
   if r is $#:
    $! numeric_solve(nu,x,$D)
   if r=='all':
    $! 'all'
   allsol.$}(r)
  $! dedup(allsol)
 if $)(fac,'^')$* $G(fac[2])$* $c(fac[2])>0:
  $! $r(fac[1],x,$D,$:+1)
 r=isolate(nu,0,x,$D,$:)
 if r is $- $#:
  $! r
 r=radical_solve(nu,x,$D,$:)
 if r is $- $#:
  $! r
 r=explog_solve(nu,x,$D,$:)
 if r is $- $#:
  $! r
 r=ln_solve(nu,x,$D,$:)
 if r is $- $#:
  $! r
 r=kernel_solve(nu,x,$D,$:)
 if r is $- $#:
  $! r
 if hastrigx(nu,x):
  g=texpand(nu)
  if g!=nu:
   r=kernel_solve(g,x,$D,$:+1)
   if r is $#:
    fg=factor_expr(g)
    fg=fg[1]if $)(fg,'hold')$& fg
    if $)(fg,'*'):
     $! solve_num(g,x,$D,$:+1)
   if r is $- $#:
    $! r
  r=trig_lin(nu,x,$D)
  if r is $- $#:
   $! r
 $! numeric_solve(nu,x,$D)
$, radical_solve(nu,x,$D,$:):
 ks=[]
 xkernels(nu,x,ks)
 if $- ks:
  $! $#
 $( k in ks:
  if $-($)(k,'^')$* isq(k[2])$* k[2][1]==1):
   $! $#
 if $/(ks)>1:
  if $:>4 or $/(ks)>3:
   $! $#
  $( k in ks:
   if k[2]!=$x:
    $! $#
  k=ks[0]
  W='W_'
  g=$?($Y(nu,k,W))
  cs_=$[(g,W)
  if cs_ is $# or $/(cs_)!=2:
   $! $#
  A,B=cs_
  g2=$?($_(pw(A,2),$<(pw(B,2),k[1])))
  rs=$r(g2,x,$D,$:+1)
  if rs is $# or rs=='all':
   $! $#
  $![r $( r in rs if valid(nu,x,r,$D)]
 k=ks[0]
 base=k[1]
 q=k[2][2]
 W='W_'
 g=$?($Y(nu,k,W))
 cs_=$[(g,W)
 if cs_ is $# or $/(cs_)!=2 or has(cs_[0],W):
  $! $#
 A,B=cs_
 if degree(A,x)is $# or degree(B,x)is $# or degree(base,x)is $#:
  $! $#
 poly=$?($_(pw($m(A),q),$<(pw(B,q),base)))
 rs=solve_poly(poly,x,$D)
 if rs is $# or rs=='all':
  $! $#
 $9=[]
 $( r in rs:
  if valid(nu,x,r,$D):
   $9.$%(r)
 $! $9
$, expterm(t,x):
 fs=t[1:]if $)(t,'*')$&(t,)
 c=[]
 L=[]
 $( f in fs:
  if $8(f,x):
   c.$%(f)
  $= $)(f,'^')$* $8(f[1],x)$* $k(f[2],x)is $- $# $* $z(f[1])$* fv(f[1])>0:
   L.$%($<(f[2],fn('ln',f[1]))if f[1]!='e' $& f[2])
  $&:
   $! $#
 $! $K(c),$>(L)
$, explog_solve(nu,x,$D,$:):
 if $- $)(nu,'+'):
  $! $#
 dep=[t $( t in nu[1:]if $- $8(t,x)]
 ind=$>([t $( t in nu[1:]if $8(t,x)])
 if $/(dep)==2 $* ind==0:
  A=expterm(dep[0],x)
  B=expterm(dep[1],x)
  if A is $# or B is $#:
   $! $#
  r=$.($m($V(B[0],A[0])))
  if $z(r)$* fv(r)<=0 $* $- $D:
   $![]
  eq=$?($_(A[1],$`(B[1],fn('ln',r))))
  lx=$k(eq,x)
  if lx is $#:
   $! $#
  $![nice($.($m($V(lx[1],lx[0]))))]
 $! $#
''')
_x(r'''$, ln_solve(nu,x,$D,$:):
 $Q=nu[1:]if $)(nu,'+')$&(nu,)
 lns=[]
 $a=[]
 $( t in $Q:
  c,r=$f(t)
  if $)(r,'log')$* $/(r)==3:
   c=$V(c,fn('ln',r[2]))
   r=('ln',r[1])
  if $)(r,'ln')$* $w(c)$* $- $8(r,x):
   lns.$%((c,r[1]))
  $= $8(t,x):
   $a.$%(t)
  $= $)(r,'ln')$* $5(c)$* $- $8(r,x):
   lns.$%((c,r[1]))
  $&:
   $! $#
 if $/(lns)<2 $* $-($/(lns)==1 $* $a):
  $! $#
 k=rest_k=$>($a)
 c0=lns[0][0]
 if all([c==c0 $( c,u in lns]):
  P=$K([u $( c,u in lns])
  rhs=pw('e',$.($m($V(rest_k,c0))))
 $= all([$w(c)$( c,u in lns]):
  P=$K([pw(u,c)$( c,u in lns])
  rhs=pw('e',$m(rest_k))
 $&:
  $! $#
 rs=$r($_(P,rhs),x,$D,$:+1)
 if rs is $# or rs=='all':
  $! rs
 $9=[]
 $( r in rs:
  if valid(nu,x,r,$D):
   $9.$%(r)
 $! $9
$, hastrigx(e,x):
 if $0(e)is $- $1 or e[0]=='Q':
  $! $2
 if e[0]in('sin','cos','tan')$* has(e,x):
  $! $B
 $( a in e[1:]:
  if hastrigx(a,x):
   $! $B
 $! $2
$, dedup($j):
 $9=[]
 $( s in $j:
  if s $- in $9:
   dup=$2
   $( t in $9:
    ${:
     if $5(s)$* $5(t)$* $H($Z(s)-$Z(t))<1e-12*(1+$H($Z(s))):
      dup=$B
      $R
    $3 $6:
     pass
   if $- dup:
    $9.$%(s)
 $! $9
$, sortsols($j):
 $, key(s):
  t=s
  $( w in $e(s):
   if w[0]=='n' $* w[1:].isdigit():
    t=$Y(t,w,0)
  ${:
   v=$Z(t)
   if $0(v)is $4:
    $!(1,v.$U,v.imag,okey(s))
   $!(0,v,0.0,okey(s))
  $3 $6:
   $!(2,0.0,0.0,okey(s))
 $! sorted($j,key=key)
$, solve_poly(p,x,$D):
 cs=$[(p,x)
 if cs is $#:
  $! $#
 $F cs $* cs[-1]==0:
  cs.pop()
 n=$/(cs)-1
 if n<=0:
  $![]if cs $* cs[0]!=0 $& 'all'
 $j=[]
 k=0
 $F cs[k]==0:
  k+=1
 if k:
  $j.$%(0)
  cs=cs[k:]
  n=$/(cs)-1
 if n==0:
  $! $j
 allrat=$B
 anyfl=$2
 $( c in cs:
  if $- $w(c):
   allrat=$2
  if $b(c):
   anyfl=$B
 if anyfl $* all([$5(c)$( c in cs]):
  $! $j+numroots(cs,$D)
 if allrat:
  cc,fs=ufactor(cs)
  $( g,m in fs:
   $j.$}(solve_small(g,x,$D))
  $! dedup($j)
 if n==1:
  $! $j+[$.($m($V(cs[0],cs[1])))]
 if n==2:
  $! $j+quad(cs[2],cs[1],cs[0],$D)
 fac=factor_expr(p,x)
 fac=fac[1]if $)(fac,'hold')$& fac
 if $)(fac,'*'):
  $( g in fac[1:]:
   if $)(g,'^')$* $G(g[2]):
    g=g[1]
   if $8(g,x):
    $7
   dg=degree(g,x)
   if dg is $- $# $* dg<n:
    r=solve_poly(g,x,$D)
    if r is $#:
     $! $#
    $j.$}(r)
   $&:
    $! $#
  $! dedup($j)
 r=solve_binom(cs,x,$D)
 if r is $- $#:
  $! $j+r
 if all([$5(c)$( c in cs]):
  $! $j+numroots(cs,$D)
 $! $#
$, quad(a,b,c,$D):
 D=$.($?($_($<(b,b),$<(4,a,c))))
 if $z(D)$* $- $D:
  if fv(D)<0:
   $![]
 if D==0:
  $![$.($V($m(b),$<(2,a)))]
 s=$O(D)
 r1=$.($V($_($m(b),s),$<(2,a)))
 r2=$.($V($`($m(b),s),$<(2,a)))
 if $5(r1):
  r1=$?(r1)
  r2=$?(r2)
 $![r1,r2]
$, solve_small(g,x,$D):
 n=$/(g)-1
 if n==1:
  $![Q(-g[0],g[1])]
 if n==2:
  $! quad(g[2],g[1],g[0],$D)
 r=solve_binom(g,x,$D)
 if r is $- $#:
  $! r
 if n==3:
  r=cardano(g,$D)
  if r is $- $#:
   if $/(fmt(r[0]))<=32:
    $! r
 $! numroots(g,$D)
$, solve_binom(cs,x,$D):
 n=$/(cs)-1
 m=0
 $( i in $+(1,n+1):
  if cs[i]!=0:
   m=igcd(m,i)
 if m<=1:
  $! $#
 sub_cs=[cs[i]$( i in $+(0,n+1,m)]
 if $/(sub_cs)-1>2 $* $-($/([c $( c in sub_cs if c!=0])==2):
  $! $#
 u='U_'
 if $/(sub_cs)==2:
  roots_u=[$.($m($V(sub_cs[0],sub_cs[1])))]
 $&:
  roots_u=solve_poly(fromcoeffs(sub_cs,u),u,$D)
  if roots_u is $#:
   $! $#
 $9=[]
 $( r in roots_u:
  $9.$}(nthroots(r,m,$D))
 $! dedup($9)
$, nthroots(r,m,$D):
 if $- $D:
  if $z(r):
   v=fv(r)
   if m%2==1:
    if v<0:
     $![$m(pw($m(r),Q(1,m)))]
    $![pw(r,Q(1,m))]
   if v<0:
    $![]
   if v==0:
    $![0]
   rt=pw(r,Q(1,m))
   $![$m(rt),rt]
  if m%2==1:
   $![pw(r,Q(1,m))]
  rt=pw(r,Q(1,m))
  $![$m(rt),rt]
 if $5(r):
  v=$Z(r)
  mod=fn('$H',r)
  ang=fn('$l',r)
  $9=[]
  $( k in $+(m):
   th=$V($`(ang,$<(2*k,'pi')),m)
   z=$<(pw(mod,Q(1,m)),$`(fn('cos',th),$<('i',fn('sin',th))))
   z=$?(z)
   $9.$%(z)
  $! $9
 rt=pw(r,Q(1,m))
 $![$<(rt,pw('e',$V($<(2*k,'i','pi'),m)))$( k in $+(m)]
$, cardano(g,$D):
 d,c,b,a=[Q(v)if $0(v)is $q $& v $( v in g]
 p=$V($_($<(3,a,c),$<(b,b)),$<(3,a,a))
 q=$V($`($<(2,pw(b,3)),$<(-9,a,b,c),$<(27,a,a,d)),$<(27,pw(a,3)))
 disc=$`($V(pw(q,2),4),$V(pw(p,3),27))
 if $- $w(disc)or $c(disc)<=0:
  $! $#
 s=$O(disc)
 u=$`($m($V(q,2)),s)
 v=$_($m($V(q,2)),s)
 $, cbrt(w):
  wv=fv(w)
  if wv<0:
   $! $m(pw($m(w),Q(1,3)))
  $! pw(w,Q(1,3))
 t=$`(cbrt(u),cbrt(v))
 root=$_(t,$V(b,$<(3,a)))
 if $- $D:
  $![root]
 $![root]+[clean(r)$( r in numroots_after(g,root)]
$, numroots_after(g,root):
 rv=fv(root)
 rs=aberth(g)
 $![fromcomplex(z)$( z in rs if $H(z-rv)>1e-6]
$, numroots(cs,$D):
 rs=aberth([evalf(c)if $- $G(c)$& c $( c in cs])
 $9=[]
 $( z in rs:
  if $H(z.imag)<1e-9*(1+$H(z.$U)):
   $9.$%($C(z.$U))
  $= $D:
   $9.$%(fromcomplex(z))
 $! $9
NC=[0]
$, newint():
 NC[0]+=1
 $! 'n'+$p(NC[0])
''')
_x(r'''$, isolate(lhs,rhs,x,$D,$:):
 if $:>12:
  $! $#
 if lhs==x:
  $![rhs]
 if $8(lhs,x):
  $! 'all' if $.($_(lhs,rhs))==0 $&[]
 h=head(lhs)
 if h=='+':
  dep=[t $( t in lhs[1:]if $- $8(t,x)]
  ind=[t $( t in lhs[1:]if $8(t,x)]
  if $/(dep)==1:
   $! isolate(dep[0],$_(rhs,$>(ind)),x,$D,$:+1)
  $! $#
 if h=='*':
  dep=[t $( t in lhs[1:]if $- $8(t,x)]
  ind=[t $( t in lhs[1:]if $8(t,x)]
  if $/(dep)==1:
   c=$K(ind)
   r=$V(rhs,c)
   if $5(c)$* $)(rhs,'+'):
    r=$?(r)
   $! isolate(dep[0],r,x,$D,$:+1)
  $! $#
 if h=='^':
  b,p=lhs[1],lhs[2]
  if $8(p,x):
   if p==-1 or($G(p)$* $c(p)<0):
    if rhs==0:
     $![]
    $! isolate(pw(b,nneg(p)),pw(rhs,-1),x,$D,$:+1)
   if $0(p)is $q:
    $9=[]
    $( r in nthroots(rhs,p,$D):
     rr=isolate(b,r,x,$D,$:+1)
     if rr is $#:
      $! $#
     if rr=='all':
      $! 'all'
     $9.$}(rr)
    $! $9
   if isq(p):
    pn,pd=p[1],p[2]
    if pd%2==0 $* $- $D $* $z(rhs)$* fv(rhs)<0:
     $![]
    $! isolate(pw(b,pn),pw(rhs,pd),x,$D,$:+1)
   $! isolate(b,pw(rhs,pw(p,-1)),x,$D,$:+1)
  if $8(b,x):
   if rhs==0:
    $![]
   if $- $D $* $z(rhs)$* fv(rhs)<0 $* $z(b)$* fv(b)>0:
    $![]
   if b=='e':
    $! isolate(p,fn('ln',rhs),x,$D,$:+1)
   if $G(b)$* $5(rhs):
    $! isolate(p,fn('log',rhs,b),x,$D,$:+1)
   $! isolate(p,$V(fn('ln',rhs),fn('ln',b)),x,$D,$:+1)
  $! $#
 if $0(lhs)is $1 $* $/(lhs)>=2:
  u=lhs[1]
  if $- all([$8(a,x)$( a in lhs[2:]]):
   $! $#
  rs=invfun(h,lhs,rhs,$D)
  if rs is $#:
   $! $#
  $9=[]
  $( r in rs:
   rr=isolate(u,r,x,$D,$:+1)
   if rr is $#:
    $! $#
   if rr=='all':
    $! 'all'
   $9.$}(rr)
  $! $9
 $! $#
$, invfun(h,lhs,r,$D):
 rv=$#
 if $z(r):
  rv=fv(r)
 if h=='ln':
  $![pw('e',r)]
 if h=='log':
  b=lhs[2]if $/(lhs)>2 $& 10
  $![pw(b,r)]
 if h=='$H':
  if rv is $- $#:
   if rv<0:
    $![]
   if rv==0:
    $![0]
  $![$m(r),r]
 if h=='$O':
  $![pw(r,2)]
 if h=='sin':
  if rv is $- $# $* $H(rv)>1 $* $- $D:
   $![]
  n=newint()
  if r==0:
   $![$<(n,'pi')]
  a=fn('$y',r)
  if r==1 or r==-1:
   $![$`(a,$<(2,n,'pi'))]
  $![$`(a,$<(2,n,'pi')),$`($_('pi',a),$<(2,n,'pi'))]
 if h=='cos':
  if rv is $- $# $* $H(rv)>1 $* $- $D:
   $![]
  n=newint()
  if r==0:
   $![$`($<($x,'pi'),$<(n,'pi'))]
  a=fn('arccos',r)
  if r==1 or r==-1:
   $![$`(a,$<(2,n,'pi'))]
  $![$`(a,$<(2,n,'pi')),$`($m(a),$<(2,n,'pi'))]
 if h=='tan':
  n=newint()
  $![$`(fn('$s',r),$<(n,'pi'))]
 if h=='$y':
  if rv is $- $# $* $H(rv)>$M.pi/2+1e-12:
   $![]
  $![fn('sin',r)]
 if h=='arccos':
  if rv is $- $# $*(rv<-1e-12 or rv>$M.pi+1e-12):
   $![]
  $![fn('cos',r)]
 if h=='$s':
  if rv is $- $# $* $H(rv)>=$M.pi/2:
   $![]
  $![fn('tan',r)]
 if h=='sinh':
  $![fn('arcsinh',r)]
 if h=='cosh':
  if rv is $- $# $* rv<1:
   $![]
  a=fn('arccosh',r)
  $![$m(a),a]
 if h=='tanh':
  if rv is $- $# $* $H(rv)>=1:
   $![]
  $![fn('arctanh',r)]
 if h=='arcsinh':
  $![fn('sinh',r)]
 if h=='arccosh':
  $![fn('cosh',r)]
 if h=='arctanh':
  $![fn('tanh',r)]
 $! $#
$, xkernels(e,x,$9):
 if $0(e)is $- $1 or e[0]=='Q' or $8(e,x):
  $!
 h=e[0]
 if h in('+','*'):
  $( a in e[1:]:
   xkernels(a,x,$9)
  $!
 if h=='^' $* $0(e[2])is $q:
  xkernels(e[1],x,$9)
  $!
 if h=='^' $* isq(e[2])$* e[1]==x:
  k=pw(x,Q(1,e[2][2]))
  if k $- in $9:
   $9.$%(k)
  $!
 if e $- in $9:
  $9.$%(e)
$, kernel_solve(nu,x,$D,$:):
 W='W_'
 g=nu
 exps=[]
 findexp(g,x,exps)
 if exps:
  base=exps[0][0]
  if all([b==base $( b,a,c in exps]):
   gg=0
   $( b,a,c in exps:
    gg=a if gg==0 $& rgcd(gg,a)
   if gg!=0:
    g2=repl_exp(g,x,base,gg,W)
    if $8(g2,x):
     rs=$r(g2,W,$D,$:+1)
     if rs is $# or rs=='all':
      $! rs
     $9=[]
     $( r in rs:
      rr=isolate(pw(base,$<(gg,x)),r,x,$D,$:+1)
      if rr is $#:
       $! $#
      $9.$}(rr)
     $! $9
 ks=[]
 xkernels(g,x,ks)
 if $/(ks)==1 $* ks[0]!=x:
  k=ks[0]
  g2=$Y(g,k,W)
  if $8(g2,x):
   rs=$r(g2,W,$D,$:+1)
   if rs is $# or rs=='all':
    $! rs
   $9=[]
   $( r in rs:
    rr=isolate(k,r,x,$D,$:+1)
    if rr is $#:
     $! $#
    if rr=='all':
     $! 'all'
    $9.$}(rr)
   $! $9
 if $/(ks)==2:
  names=sorted([head(k)$( k in ks])
  if names==['cos','sin']$* ks[0][1]==ks[1][1]:
   u=ks[0][1]
   s=fn('sin',u)
   c=fn('cos',u)
   $( a,b in((c,s),(s,c)):
    g2=$?(g)
    cc=$[($Y(g2,a,W),W)
    if cc is $- $# $* all([cc[i]==0 $( i in $+(1,$/(cc),2)]):
     g3=$?($Y($Y(g2,a,W),W,$O($_(1,pw(b,2)))))
     if $- has(g3,a):
      $! kernel_solve(g3,x,$D,$:+1)if $:<4 $& $#
 $! $#
$, rgcd(a,b):
 if $w(a)$* $w(b):
  an,ad=nd(a)
  bn,bd=nd(b)
  $! Q(igcd(an,bn),ilcm(ad,bd))
 $! a if a==b $& 0
$, findexp(e,x,$9):
 if $0(e)is $- $1 or e[0]=='Q':
  $!
 if e[0]=='^' $* $8(e[1],x)$* $- $8(e[2],x):
  l=$k(e[2],x)
  if l is $- $#:
   $9.$%((e[1],l[0],l[1]))
   $!
  $9.$%(($#,0,0))
  $!
 $( a in e[1:]:
  findexp(a,x,$9)
$, repl_exp(e,x,base,gg,W):
 if $0(e)is $- $1 or e[0]=='Q':
  $! e
 if e[0]=='^' $* e[1]==base $* $- $8(e[2],x):
  l=$k(e[2],x)
  if l is $- $#:
   $! $<(pw(base,l[1]),pw(W,$V(l[0],gg)))
 $! simp((e[0],)+$1(repl_exp(a,x,base,gg,W)$( a in e[1:]))
''')
_x(r'''$, trig_lin(nu,x,$D):
 ks=[]
 xkernels(nu,x,ks)
 if $/(ks)!=2:
  $! $#
 names=sorted([head(k)$( k in ks])
 if names!=['cos','sin']or ks[0][1]!=ks[1][1]:
  $! $#
 u=ks[0][1]
 S='S_'
 C='C_'
 g=$?($Y($Y(nu,fn('sin',u),S),fn('cos',u),C))
 if has(g,x):
  $! $#
 cs_s=$[(g,S)
 if cs_s is $# or $/(cs_s)!=2:
  $! $#
 a=cs_s[1]
 $a=cs_s[0]
 cc=$[($a,C)
 if cc is $# or $/(cc)!=2 or has(a,C):
  $! $#
 b=cc[1]
 c=cc[0]
 if c==0:
  $! isolate(fn('tan',u),$.($m($V(b,a))),x,$D,0)
 R=$O($`(pw(a,2),pw(b,2)))
 phi=fn('$s',$V(b,a))
 if $z(a)$* fv(a)<0:
  phi=$`(phi,'pi')
 $! isolate(fn('sin',$`(u,phi)),$.($m($V(c,R))),x,$D,0)
$, numeric_solve(f,x,$D,lo=$#,hi=$#,maxn=12):
 others=[s $( s in $e(f)if s!=x]
 if others:
  $! $#
 $, F(t):
  ${:
   v=$Z(f,{x:t})
  $3($E,$T,$^,$S,TypeError):
   $! $#
  if $0(v)is $4:
   if $H(v.imag)>1e-9*(1+$H(v.$U)):
    $! $#
   v=v.$U
  if v!=v:
   $! $#
  $! v
 $, points():
  if lo is $- $# $* hi is $- $#:
   $( i in $+(401):
    yield lo+(hi-lo)*i/400
   $!
  big=[10**(k/10.0)$( k in $+(60,-41,-1)]
  $( v in big:
   if v>20:
    yield-v
  $( i in $+(-400,401):
   yield i*0.05
  $( v in reversed(big):
   if v>20:
    yield v
 roots=[]
 t0=a=$#
 t1=b=$#
 $( t2 in points():
  c=F(t2)
  if b is $- $# $* b==0:
   if(a is $- $# $* a!=0)or(c is $- $# $* c!=0):
    roots.$%(t1)
  if b is $- $# $* c is $- $# $* b!=0 $* c!=0 $*(b<0)!=(c<0):
   r=bisect(F,t1,t2,b,c)
   if r is $- $#:
    roots.$%(r)
  if(a is $- $# $* b is $- $# $* c is $- $# $* b!=0
 $* $H(b)<$H(a)$* $H(b)<$H(c)$*(a>0)==(b>0)==(c>0)$* $H(b)<1e-2):
   r=newton(F,t1)
   if r is $- $# $* t0<=r<=t2:
    roots.$%(r)
  t0,a=t1,b
  t1,b=t2,c
  if $/(roots)>200:
   $R
 if b is $- $# $* b==0 $* a is $- $# $* a!=0:
  roots.$%(t1)
 $9=[]
 $( r in sorted(roots):
  if $- $9 or $H(r-$9[-1])>1e-9*(1+$H(r)):
   $9.$%(r)
 if $/($9)>maxn $* lo is $#:
  $9.sort(key=$H)
  $9=sorted($9[:maxn])
 $![snap(r)$( r in $9]
$, snap(r):
 if $H(r-round(r))<1e-12:
  $! $C(round(r))
 $! r
$, bisect(F,a,b,fa,fb):
 $( _ in $+(200):
  m=0.5*(a+b)
  fm=F(m)
  if fm is $#:
   $! $#
  if fm==0 or $H(b-a)<1e-15*(1+$H(m)):
   $R
  if(fm<0)==(fa<0):
   a,fa=m,fm
  $&:
   b,fb=m,fm
 m=0.5*(a+b)
 fm=F(m)
 if fm is $# or $H(fm)>1e-6*(1+$H(fa)+$H(fb)):
  if fm is $- $# $* $H(fm)>1e3:
   $! $#
 $! m
$, newton(F,t):
 $( _ in $+(60):
  v=F(t)
  if v is $#:
   $! $#
  h=1e-7*(1+$H(t))
  v2=F(t+h)
  if v2 is $#:
   $! $#
  d=(v2-v)/h
  if d==0:
   $R
  t2=t-v/d
  if $H(t2-t)<1e-14*(1+$H(t)):
   t=t2
   $R
  t=t2
 v=F(t)
 if v is $- $# $* $H(v)<1e-9:
  $! t
 $! $#
$, nsolve(f,x,guess=$#,lo=$#,hi=$#):
 $, F(t):
  ${:
   v=$Z(f,{x:t})
  $3($E,$T,$^,$S,TypeError):
   $! $#
  if $0(v)is $4:
   if $H(v.imag)>1e-9*(1+$H(v.$U)):
    $! $#
   v=v.$U
  $! v
 if guess is $- $#:
  r=secant(F,guess,lo,hi)
  if r is $- $#:
   $! r
 if lo is $- $# $* hi is $- $#:
  rs=numeric_solve(f,x,$2,lo,hi)
 $&:
  rs=numeric_solve(f,x,$2)
  if lo is $- $#:
   rs=[r $( r in rs if r>=lo]
  if hi is $- $#:
   rs=[r $( r in rs if r<=hi]
 if rs:
  if guess is $- $#:
   rs.sort(key=$; r:$H(r-guess))
  $&:
   rs.sort(key=$; r:$H(r))
  $! rs[0]
 $! $#
$, secant(F,g,lo,hi):
 t=g
 r=newton(F,t)
 if r is $- $# $*(lo is $# or r>=lo)$*(hi is $# or r<=hi):
  $! r
 $! $#
FLIP={'<':'>','>':'<','<=':'>=','>=':'<=','/=':'/='}
$, solve_ineq(rel,f,x):
 f=$.(f)
 if $- $5($Y(f,x,0))or $- $5(diff(f,x)):
  r=ineq_param(rel,f,x)
  if r is $- $#:
   $! r
 $! solve_rels([(rel,f)],x)
$, rel_pairs(cs,x):
 $9=[]
 $( c in cs:
  h=head(c)
  if h=='$*':
   r=rel_pairs(c[1:],x)
   if r is $#:
    $! $#
   $9+=r
  $= h in('<','>','<=','>=','/=','='):
   $9.$%((h,$.($_(c[1],c[2]))))
  $&:
   $! $#
 $( rel,f in $9:
  if $- $8(f,x)$* fvars(f,x):
   $! $#
 $! $9
$, fvars(f,x):
 $! any(w!=x $* w $- in('pi','e','i','$P')$( w in $e(f))
''')
_x(r'''$, solve_rels(pairs,x,anyof=$2):
 pts=[]
 $( rel,f in pairs:
  if $8(f,x):
   $7
  rs=$r(f,x,$2)
  if rs is $#:
   $! $#
  if rs=='all':
   rs=[]
  $( r in rs:
   if $- $z(r):
    if $5(r):
     $7
    $! $#
   pts.$%(r)
  dens=[]
  domainpts(f,x,dens)
  $( d in dens:
   r2=$r(d,x,$2)
   if r2 is $# or r2=='all':
    $7
   $( r in r2:
    if $z(r):
     pts.$%(r)
    $= $- $5(r):
     $! $#
 pts=sortsols(dedup(pts))
 $, ok1(rel,f,t):
  ${:
   v=$Z(f,{x:t})
  $3 $6:
   $! $2
  if $0(v)is $4:
   if $H(v.imag)>1e-9*(1+$H(v.$U)):
    $! $2
   v=v.$U
  if v!=v:
   $! $2
  $! relok(rel,v)
 $, test(t):
  $( rel,f in pairs:
   if ok1(rel,f,t)==anyof:
    $! anyof
  $! $- anyof
 $, testp(p):
  if anyof:
   $( q in pairs:
    if testp1([q],p):
     $! $B
   $! $2
  $! testp1(pairs,p)
 $, testp1(pairs,p):
  $( rel,f in pairs:
   ${:
    v=$Y(f,x,p)
    if v=='$I' or has(v,'$I')or has(v,'$P'):
     $! $2
    vv=$Z(v)
    if $0(vv)is $4:
     if $H(vv.imag)>=1e-9:
      $! $2
     vv=vv.$U
    if $H(vv)<1e-10:
     vv=0.0
    if $- relok(rel,vv):
     $! $2
   $3 $6:
    $! $2
  $! $B
 $g=[fv(p)$( p in pts]
 if $- $g:
  $! 'true' if test(0.5)$& 'false'
 segs=[('I',$#,pts[0],test($g[0]-max(1.0,$H($g[0]))))]
 $( i in $+($/(pts)):
  p=pts[i]
  segs.$%(('P',p,p,testp(p)))
  if i+1<$/(pts):
   segs.$%(('I',p,pts[i+1],test(0.5*($g[i]+$g[i+1]))))
 segs.$%(('I',pts[-1],$#,test($g[-1]+max(1.0,$H($g[-1])))))
 $! segs_to_bool(segs,x)
$, sgn(e):
 if $5(e):
  ${:
   v=fv(e)
  $3 $6:
   $! 0
  $! 1 if v>0 $&(-1 if v<0 $& 0)
 if $)(e,'*'):
  s=1
  $( a in e[1:]:
   k=sgn(a)
   if $- k:
    $! 0
   s*=k
  $! s
 if $)(e,'+'):
  ks=[sgn(a)or(2 if nonneg(a)$& 0)$( a in e[1:]]
  if all(k in(1,2)$( k in ks)$* 1 in ks:
   $! 1
  ks=[sgn($m(a))or(2 if nonneg($m(a))$& 0)$( a in e[1:]]
  if all(k in(1,2)$( k in ks)$* 1 in ks:
   $!-1
  $! 0
 if $)(e,'^')$* $i(e[2])$* e[2]%2==1:
  $! sgn(e[1])
 if head(e)=='exp' or($)(e,'^')$* e[1]=='e'):
  $! 1
 $! 0
$, nonneg(e):
 if $)(e,'^')$* $i(e[2])$* e[2]%2==0:
  $! $B
 if head(e)=='$H':
  $! $B
 if $)(e,'*'):
  $! all(nonneg(a)or sgn(a)>0 $( a in e[1:])
 $! sgn(e)>0
$, ineq_param(rel,f,x):
 cs=$[(f,x)
 if cs is $# or $/(cs)!=2:
  $! $#
 a=nice(comdenom(cs[1]))
 b=cs[0]
 v=nice(comdenom($V($m(b),a)))
 k=sgn(a)
 if k:
  $!(rel if k>0 $& FLIP[rel],x,v)
 n=numer_denom(a)[0]
 if rel=='/=':
  $9=[('$*',('/=',x,v),('/=',n,0))]
 $&:
  $9=[('$*',(rel,x,v),('>',a,0)),
 ('$*',(FLIP[rel],x,v),('<',a,0))]
 if $0(n)is $p:
  b=$Y(b,n,0)
 if $5(b):
  if relok(rel,fv(b)):
   $9.$%(('=',n,0))
 $&:
  $9.$%(('$*',('=',n,0),(rel,b,0)))
 $!('or',)+$1($9)if $/($9)>1 $& $9[0]
$, relok(rel,v):
 if rel=='<':
  $! v<0
 if rel=='>':
  $! v>0
 if rel=='<=':
  $! v<=0
 if rel=='>=':
  $! v>=0
 if rel=='/=':
  $! v!=0
 $! v==0
$, domainpts(f,x,$9):
 if $0(f)is $- $1 or f[0]=='Q':
  $!
 h=f[0]
 if h=='^' $* $- $8(f[1],x):
  if $G(f[2])$* $c(f[2])<0:
   $9.$%(f[1])
  if isq(f[2])$* f[2][2]%2==0:
   $9.$%(f[1])
 if h in('ln','log','$H','sign','floor','ceiling')$* $- $8(f[1],x):
  $9.$%(f[1])
 $( a in f[1:]:
  domainpts(a,x,$9)
$, segs_to_bool(segs,x):
 ivs=[]
 cur=$#
 $( kind,a,b,ok in segs:
  if ok:
   if cur is $#:
    if kind=='I':
     cur=[a,$2,b,$2]
    $&:
     cur=[a,$B,b,$B]
   $&:
    cur[2]=b
    cur[3]=(kind=='P')
  $&:
   if cur is $- $#:
    ivs.$%(cur)
    cur=$#
 if cur is $- $#:
  ivs.$%(cur)
 if $- ivs:
  $! 'false'
 if $/(ivs)>=2 $* ivs[0][0]is $# $* ivs[-1][2]is $#:
  okp=$B
  $( i in $+($/(ivs)-1):
   if $-(ivs[i][2]==ivs[i+1][0]$* $- ivs[i][3]$* $- ivs[i+1][1]):
    okp=$2
  if okp:
   ne=[('/=',x,ivs[i][2])$( i in $+($/(ivs)-1)]
   $! ne[0]if $/(ne)==1 $&('$*',)+$1(ne)
 $9=[]
 $( lo,li,hi,hiinc in ivs:
  if lo is $# $* hi is $#:
   $! 'true'
  if lo is $- $# $* hi is $- $# $* lo==hi:
   $9.$%(('=',x,lo))
  $= lo is $#:
   $9.$%(('<=' if hiinc $& '<',x,hi))
  $= hi is $#:
   $9.$%(('>=' if li $& '>',x,lo))
  $&:
   $9.$%(('$*',('<=' if li $& '<',lo,x),('<=' if hiinc $& '<',x,hi)))
 if $/($9)==1:
  $! $9[0]
 $!('or',)+$1($9)
$, eqexpr(eq):
 if $)(eq,'='):
  $! $.($_(eq[1],eq[2]))
 $! eq
$, is_linear_sys(fs,vs):
 $( f in fs:
  $( v in vs:
   d=degree(f,v)
   if d is $# or d>1:
    $! $2
  g=$?(f)
  $( i in $+($/(vs)):
   $( j in $+($/(vs)):
    cs_=$[(g,vs[i])
    if cs_ is $#:
     $! $2
    if $/(cs_)>1 $* has(cs_[1],vs[j]):
     $! $2
 $! $B
''')
_x(r'''$, linsys(fs,vs):
 m=$/(fs)
 n=$/(vs)
 A=[]
 $( f in fs:
  g=$?(f)
  row=[]
  $a=g
  $( v in vs:
   cs_=$[(g,v)
   c=cs_[1]if $/(cs_)>1 $& 0
   row.$%(c)
  const=g
  $( v in vs:
   const=$Y(const,v,0)
  row.$%($m(const))
  A.$%(row)
 piv=[]
 r=0
 $( c in $+(n):
  p=$#
  $( i in $+(r,m):
   if $.(A[i][c])!=0:
    p=i
    $R
  if p is $#:
   $7
  A[r],A[p]=A[p],A[r]
  pv=A[r][c]
  A[r]=[$.($V(a,pv))$( a in A[r]]
  $( i in $+(m):
   if i!=r $* A[i][c]!=0:
    fct=A[i][c]
    A[i]=[$.($?($_(A[i][j],$<(fct,A[r][j]))))$( j in $+(n+1)]
  piv.$%(c)
  r+=1
  if r==m:
   $R
 $( i in $+(r,m):
  if $.(A[i][n])!=0:
   $![]
 sol={}
 free=[c $( c in $+(n)if c $- in piv]
 params={}
 k=1
 $( c in free:
  params[vs[c]]='c'+$p(k)
  k+=1
 $( i in $+($/(piv)):
  c=piv[i]
  val=A[i][n]
  $( c2 in free:
   val=$_(val,$<(A[i][c2],params[vs[c2]]))
  sol[vs[c]]=nice($.(val))
 $( c in free:
  sol[vs[c]]=params[vs[c]]
 $![sol]
$, solve_system(eqs,vs,$D=$2,guesses=$#):
 NC[0]=0
 fs=[]
 $( e in eqs:
  f=eqexpr(e)
  f=numer_of(f)if hasdenom_x(f,vs)$& f
  if f!=0:
   fs.$%(f)
 if guesses:
  $! newton_sys(fs,vs,guesses)
 if is_linear_sys(fs,vs):
  $! linsys(fs,vs)
 r=elim(fs,vs,$D,0)
 if r is $#:
  $! newton_sys(fs,vs,[0.0]*$/(vs))
 $9=[]
 $( s in r:
  ok=$B
  $( v in vs:
   if v $- in s:
    s[v]=v
  if $- $D:
   $( v in vs:
    if $5(s[v])$* $- $z(s[v]):
     ok=$2
  if ok $* s $- in $9:
   $9.$%(s)
 $! $9
$, hasdenom_x(f,vs):
 $( v in vs:
  nu,de=numer_denom(f)
  if has(de,v):
   $! $B
 $! $2
$, elim(fs,vs,$D,$:):
 fs=[$.($?(f))$( f in fs]
 fs=[f $( f in fs if f!=0]
 if $- fs:
  $![{}]
 $( f in fs:
  if freeofall(f,vs):
   if $5(f)or f!=0:
    $![]
 if $:>8:
  $! $#
 best=$#
 $( f in fs:
  inv=[v $( v in vs if has(f,v)]
  if $/(inv)==1:
   best=(f,inv[0])
   $R
 if best is $#:
  $( f in fs:
   $( v in vs:
    d=degree(f,v)
    if d==1:
     c=$[(f,v)
     if c is $- $# $* $5(c[1])$* c[1]!=0:
      best=(f,v)
      $R
   if best:
    $R
 if best is $#:
  $( f in fs:
   $( v in vs:
    if degree(f,v)==1:
     best=(f,v)
     $R
   if best:
    $R
 if best is $- $#:
  f,v=best
  rs=$r(f,v,$D)
  if rs is $#:
   $! $#
  if rs=='all':
   rs=[]
  $9=[]
  $a=[g $( g in fs if g is $- f]
  ovs=[w $( w in vs if w!=v]
  $( r in rs:
   sub_=[$.($Y(g,v,r))$( g in $a]
   rr=elim(sub_,ovs,$D,$:+1)
   if rr is $#:
    $! $#
   $( s in rr:
    s2=dict(s)
    val=r
    $( w in s2:
     val=$Y(val,w,s2[w])
    s2[v]=clean(val)
    $9.$%(s2)
  $! $9
 if $/(fs)>=2 $* $/(vs)>=2:
  y=vs[-1]
  R=resultant(fs[0],fs[1],y)
  if R is $# or R==0:
   $! $#
  rr=elim([R]+fs[2:],vs[:-1],$D,$:+1)
  if rr is $#:
   $! $#
  $9=[]
  $( s in rr:
   gs=[]
   $( g in fs:
    h=g
    $( w in s:
     h=$Y(h,w,s[w])
    gs.$%($.($?(h)))
   ys=elim(gs,[y],$D,$:+1)
   if ys is $#:
    $7
   $( t in ys:
    s2=dict(s)
    s2.update(t)
    $9.$%(s2)
  $! $9
 $! $#
$, resultant(f,g,y):
 a=$[(f,y)
 b=$[(g,y)
 if a is $# or b is $#:
  $! $#
 m=$/(a)-1
 n=$/(b)-1
 if m<1 or n<1:
  $! $#
 N=m+n
 M=[]
 $( i in $+(n):
  row=[0]*N
  $( j in $+(m+1):
   row[i+j]=a[m-j]
  M.$%(row)
 $( i in $+(m):
  row=[0]*N
  $( j in $+(n+1):
   row[i+j]=b[n-j]
  M.$%(row)
 $! $?(bareiss(M))
$, bareiss(M):
 n=$/(M)
 M=[$J(r)$( r in M]
 sign=1
 prev=1
 $( k in $+(n-1):
  if M[k][k]==0:
   sw=$#
   $( i in $+(k+1,n):
    if M[i][k]!=0:
     sw=i
     $R
   if sw is $#:
    $! 0
   M[k],M[sw]=M[sw],M[k]
   sign=-sign
  $( i in $+(k+1,n):
   $( j in $+(k+1,n):
    num=$?($_($<(M[i][j],M[k][k]),$<(M[i][k],M[k][j])))
    M[i][j]=exdiv(num,prev)
  prev=M[k][k]
 $! $<(sign,M[n-1][n-1])
$, exdiv(a,b):
 if b==1:
  $! a
 if $G(b):
  $! $?($<(a,ninv(b))if $w(b)$& $V(a,b))
 ks=[]
 kernels(a,ks)
 kernels(b,ks)
 sortkernels(ks)
 ra=ratform(a,ks)
 rb=ratform(b,ks)
 if ra is $# or rb is $#:
  $! $.($V(a,b))
 q=$W(p_mul(ra[0],rb[1]),p_mul(ra[1],rb[0]))
 if q is $#:
  $! $.($V(a,b))
 $! p2e(q,ks)
$, newton_sys(fs,vs,guess):
 n=$/(vs)
 if $/(fs)!=n:
  $! $#
 others=[]
 $( f in fs:
  $( s in $e(f):
   if s $- in vs:
    $! $#
 J=[[diff(f,v)$( v in vs]$( f in fs]
 xv=[$C($Z(g).$U)if $G(g)or $5(g)$& 0.0 $( g in guess]
 $( it in $+(100):
  env=dict(zip(vs,xv))
  ${:
   F=[$Z(f,env)$( f in fs]
   Jv=[[$Z(J[i][j],env)$( j in $+(n)]$( i in $+(n)]
  $3 $6:
   $! $#
  F=[v.$U if $0(v)is $4 $& v $( v in F]
  Jv=[[v.$U if $0(v)is $4 $& v $( v in r]$( r in Jv]
  dx=linsolve_float(Jv,[-v $( v in F])
  if dx is $#:
   $! $#
  xv=[xv[i]+dx[i]$( i in $+(n)]
  if max([$H(d)$( d in dx])<1e-13*(1+max([$H(v)$( v in xv])):
   $R
 env=dict(zip(vs,xv))
 ${:
  if max([$H($Z(f,env))$( f in fs])>1e-8:
   $![]
 $3 $6:
  $![]
 $![dict([(vs[i],snap(xv[i]))$( i in $+(n)])]
$, linsolve_float(A,b):
 n=$/(A)
 M=[$J(A[i])+[b[i]]$( i in $+(n)]
 $( c in $+(n):
  p=max($+(c,n),key=$; i:$H(M[i][c]))
  if $H(M[p][c])<1e-300:
   $! $#
  M[c],M[p]=M[p],M[c]
  $( i in $+(n):
   if i!=c:
    f=M[i][c]/M[c][c]
    $( j in $+(c,n+1):
     M[i][j]-=f*M[c][j]
 $![M[i][n]/M[i][i]$( i in $+(n)]
$, sols_to_bool(x,$j):
 if $j=='all':
  $! 'true'
 if $j is $#:
  $! $#
 if $- $j:
  $! 'false'
 eqs=[('=',x,s)$( s in $j]
 if $/(eqs)==1:
  $! eqs[0]
 $!('or',)+$1(eqs)
''')
_x(r'''$, apply_constraints($j,x,cons):
 if $- cons or $j=='all' or $j is $#:
  $! $j
 lo=$#
 hi=$#
 $9=[]
 expanded=[]
 $( s in $j:
  ns=[w $( w in $e(s)if w[0]=='n' $* w[1:].isdigit()]
  if ns $* $/(ns)==1:
   b=bounds(cons,x)
   if b is $#:
    expanded.$%(s)
    $7
   n=ns[0]
   $( k in $+(-60,61):
    v=$Y(s,n,k)
    expanded.$%(v)
  $&:
   expanded.$%(s)
 $( s in expanded:
  if satisfies(s,x,cons):
   $9.$%(s)
 $! sortsols(dedup($9))
$, bounds(cons,x):
 lo=$#
 hi=$#
 $( c in cons:
  if head(c)in('<','<=','>','>=')$* $5(c[1])$* c[2]==x:
   if c[0]in('<','<='):
    lo=c[1]
   $&:
    hi=c[1]
  $= head(c)in('<','<=','>','>=')$* c[1]==x $* $5(c[2]):
   if c[0]in('<','<='):
    hi=c[2]
   $&:
    lo=c[2]
 if lo is $# or hi is $#:
  $! $#
 $! lo,hi
$, satisfies(s,x,cons):
 $( c in cons:
  h=head(c)
  if h in('<','<=','>','>=','/=','='):
   ${:
    a=fv($Y(c[1],x,s))
    b=fv($Y(c[2],x,s))
   $3 $6:
    if $- $5(s):
     $7
    $! $2
   eps=1e-12*(1+$H(a)+$H(b))
   if h=='<' $* $- a<b-eps*0:
    $! $2
   if h=='<=' $* $- a<=b+eps:
    $! $2
   if h=='>' $* $- a>b:
    $! $2
   if h=='>=' $* $- a>=b-eps:
    $! $2
   if h=='/=' $* $H(a-b)<=eps:
    $! $2
   if h=='=' $* $H(a-b)>1e-9*(1+$H(a)+$H(b)):
    $! $2
  $= h=='$*':
   if $- satisfies(s,x,$J(c[1:])):
    $! $2
 $! $B
$, solve(eq,x,$D=$2,cons=$#):
 NC[0]=0
 if $)(eq,'$*')or $)(eq,'$J'):
  $! $#
 h=head(eq)
 if h in('<','>','<=','>=','/='):
  f=$_(eq[1],eq[2])
  cp=rel_pairs(cons,x)if cons $& $#
  if cp:
   $! solve_rels([(h,$.(f))]+cp,x)
  r=solve_ineq(h,f,x)
  $! r
 if h=='=':
  f=$_(eq[1],eq[2])
 $= h=='or':
  if $- $D $* any([head(q)in('<','>','<=','>=','/=')$( q in eq[1:]]):
   ps=rel_pairs(eq[1:],x)if all([head(q)!='$*' $( q in eq[1:]])$& $#
   if ps:
    r=solve_rels(ps,x,$B)
    if r is $- $#:
     $! r
  parts=[]
  $( e in eq[1:]:
   r=solve(e,x,$D,cons)
   if r is $#:
    $! $#
   if r=='true':
    $! 'true'
   if $)(r,'or'):
    parts.$}([q $( q in r[1:]if q $- in parts])
   $= r!='false' $* r $- in parts:
    parts.$%(r)
  if $- parts:
   $! 'false'
  $!('or',)+$1(parts)if $/(parts)>1 $& parts[0]
 $= eq=='true':
  $! 'true'
 $&:
  f=eq
 w=firstwhen(f,x)
 if w is $- $#:
  r=solve_when(f,w,x,$D,cons)
  if r is $- $#:
   $! r
 if $- $D $* firstabs(f,x)is $- $# $* abs_cases(numer_of(f),x,[],0)=='interval':
  r=abs_region(f,x,cons)
  if r is $- $#:
   $! r
 $j=$r(f,x,$D)
 if $j is $#:
  $! $#
 if $j!='all':
  $j=[clean(s)$( s in $j]
  if $- $D:
   $j=[s $( s in $j if $-($5(s)$* $- $z(s))]
   $j=[realpart(s)$( s in $j]
  $j=sortsols(dedup($j))
 if cons:
  $j=apply_constraints($j,x,cons)
 $! sols_to_bool(x,$j)
$, firstabs(f,x):
 if $0(f)is $- $1 or f[0]=='Q':
  $! $#
 if f[0]=='$H' $* $- $8(f[1],x):
  $! f
 $( a in f[1:]:
  w=firstabs(a,x)
  if w is $- $#:
   $! w
 $! $#
$, abs_cases(f,x,conds,$:):
 w=firstabs(f,x)
 if w is $#:
  rs=$r(f,x,$2,$:+1)
  if rs=='all':
   ps=rel_pairs(conds,x)
   r=solve_rels(ps,x)if ps is $- $# $& $#
   if r=='false':
    $![]
   if r is $# or $)(r,'$*')or head(r)in('<','>','<=','>=','/=','or')or r=='true':
    $! 'interval'
   $![r[2]]if $)(r,'=')$& 'interval'
  if rs is $#:
   $! $#
  $9=[]
  $( q in rs:
   ns=[w $( w in $e(q)if w[0]=='n' $* w[1:].isdigit()]
   q0=$Y(q,ns[0],0)if $/(ns)==1 $& q
   if $z(q0)$* satisfies(q0,x,conds):
    $9.$%(q)
  $! $9
 u=w[1]
 $9=[]
 $( g,c in((replnode(f,w,u),('>=',u,0)),(replnode(f,w,$m(u)),('<',u,0))):
  r=abs_cases(g,x,conds+[c],$:)
  if r is $# or r=='interval':
   $! r
  $( q in r:
   if q $- in $9:
    $9.$%(q)
 $! sortsols($9)
$, abs_region(f,x,cons):
 pts=[]
 $, walk(e):
  if $0(e)is $- $1 or e[0]=='Q':
   $!
  if e[0]=='$H' $* $- $8(e[1],x):
   rs=$r(e[1],x,$2)
   if rs $* rs!='all':
    pts.$}([q $( q in rs if $z(q)])
  $( b in e[1:]:
   walk(b)
 walk(f)
 $, ok(t):
  ${:
   v=fv($Y(f,x,t))if $- $0(t)is $C $& $Z(f,{x:t})
   if $0(v)is $4:
    v=v.$U
   $! $H(v)<1e-9 $* satisfies(t,x,cons or[])
  $3 $6:
   $! $2
 pts=sortsols(dedup(pts))
 if $- pts:
  $! $#
 $g=[fv(p)$( p in pts]
 segs=[('I',$#,pts[0],ok($g[0]-1.0))]
 $( i in $+($/(pts)):
  segs.$%(('P',pts[i],pts[i],ok(pts[i])))
  if i+1<$/(pts):
   segs.$%(('I',pts[i],pts[i+1],ok(0.5*($g[i]+$g[i+1]))))
 segs.$%(('I',pts[-1],$#,ok($g[-1]+1.0)))
 $! segs_to_bool(segs,x)
NOTREL={'<':'>=','>':'<=','<=':'>','>=':'<','=':'/=','/=':'='}
$, firstwhen(f,x):
 if $0(f)is $- $1 or f[0]=='Q':
  $! $#
 if f[0]=='when' $* $- $8(f[1],x):
  $! f
 $( a in f[1:]:
  w=firstwhen(a,x)
  if w is $- $#:
   $! w
 $! $#
$, replnode(f,w,r):
 if f==w:
  $! r
 if $0(f)is $- $1 or f[0]=='Q':
  $! f
 $! simp((f[0],)+$1(replnode(a,w,r)$( a in f[1:]))
''')
_x(r'''$, solve_when(f,w,x,$D,cons):
 c=w[1]
 cs=$J(c[1:])if head(c)=='$*' $&[c]
 if $- all([head(q)in NOTREL $( q in cs]):
  $! $#
 parts=[]
 r=solve(('=',replnode(f,w,w[2]),0),x,$D,(cons or[])+cs)
 if r is $#:
  $! $#
 parts.$%(r)
 if $/(w)>3:
  $( k in $+($/(cs)):
   nc=cs[:k]+[(NOTREL[cs[k][0]],cs[k][1],cs[k][2])]
   r=solve(('=',replnode(f,w,w[3]),0),x,$D,(cons or[])+nc)
   if r is $#:
    $! $#
   parts.$%(r)
 $9=[]
 $( r in parts:
  $( q in(r[1:]if $)(r,'or')$&(r,)):
   if q!='false' $* q $- in $9:
    $9.$%(q)
 if 'true' in $9:
  $! $#
 if $- $9:
  $! 'false'
 $! $9[0]if $/($9)==1 $&('or',)+$1($9)
$, realpart(s):
 if $5(s)$* has(s,'i'):
  r,i=reim(s)
  if i==0 or($G(i)$* $H(tofl(i))<1e-12):
   $! r
 $! s
$, zeros(e,x,$D=$2,cons=$#):
 NC[0]=0
 if $)(e,'='):
  e=$_(e[1],e[2])
 if firstwhen(e,x)is $- $#:
  r=solve(('=',e,0),x,$D,cons)
  qs=r[1:]if $)(r,'or')$&(r,)
  if r is $- $# $* all([r=='false' or($)(q,'=')$* q[1]==x)$( q in qs]):
   $!('$J',)+$1([q[2]$( q in qs if r!='false'])
 $j=$r(e,x,$D)
 if $j is $#:
  $! $#
 if $j=='all':
  $!('$J',)
 $j=[clean(s)$( s in $j]
 if $- $D:
  $j=[realpart(s)$( s in $j if $-($5(s)$* $- $z(s))]
 $j=sortsols(dedup($j))
 if cons:
  $j=apply_constraints($j,x,cons)
 $!('$J',)+$1($j)
YP=('Y1_','Y2_')
$, desolve(ode,x,y,conds):
 NC[0]=0
 F=eqexpr(ode)if $)(ode,'=')$& ode
 F=$.(F)
 if has(F,YP[1]):
  sol=de2(F,x,y)
  nconst=2
 $&:
  sol=de1(F,x,y)
  nconst=1
 if sol is $#:
  $! $#
 if conds:
  sol=apply_ic(sol,x,y,conds,nconst)
 $! sol
$, de1(F,x,y):
 y1=YP[0]
 cs_=$[(F,y1)
 if cs_ is $- $# $* $/(cs_)==2 $* $8(cs_[1],y1):
  g=$.($m($V(cs_[0],cs_[1])))
 $&:
  rs=$r(F,y1)
  if $- rs or rs=='all' or $/(rs)!=1:
   $! $#
  g=rs[0]
 c1='c1'
 gy=$[($?(g),y)
 if gy is $- $# $* $/(gy)==2 $* $8(gy[1],y):
  P=$m(gy[1])
  Bq=gy[0]
  if Bq==0 or $8(P,x)$* $8(Bq,x)$* $2:
   pass
  mu=pw('e',integrate(P,x))
  mu=dropabs(simp(mu))
  I=integ($.($?($<(mu,Bq))),x)
  if I is $- $#:
   yy=$.($V($`(I,c1),mu))
   $!('=',y,nice($?(yy))if $- hasden_free(yy)$& nice(yy))
 sep=separate(g,x,y)
 if sep is $- $#:
  p,q=sep
  L=integ($.(pw(q,-1)),y)
  R=integ(p,x)
  if L is $- $# $* R is $- $#:
   rs=isolate_eq(L,$`(R,c1),y)
   if rs is $- $# $* $/(rs)==1:
    $!('=',y,nice(simp(rs[0])))
   G=lncombine(L,y)
   if G is $- $#:
    rs=$r($_(G,$<(c1,pw('e',R))),y)
    if rs $* rs!='all' $* $/(rs)==1:
     $!('=',y,nice(rs[0]))
   $!('=',L,$`(R,c1))
 bern_=bernoulli(g,x,y)
 if bern_ is $- $#:
  $! bern_
 V='V_'
 h=$.($Y(g,y,$<(V,x)))
 if $8(h,x)$* has(h,V):
  dv=$.($_(h,V))
  if dv!=0:
   L=integ($.(pw(dv,-1)),V)
   if L is $- $#:
    R=$`(fn('ln',fn('$H',x)),c1)
    rs=isolate_eq(L,R,V)
    if rs is $- $# $* $/(rs)==1:
     $!('=',y,nice($?($<(x,rs[0]))))
    L2=$Y(L,V,$V(y,x))
    $!('=',L2,R)
 $! $#
$, dropabs(e):
 if $0(e)is $- $1 or e[0]=='Q':
  $! e
 if e[0]=='$H':
  $! dropabs(e[1])
 $! simp((e[0],)+$1(dropabs(a)$( a in e[1:]))
$, lncombine(L,y):
 $Q=L[1:]if $)(L,'+')$&(L,)
 fs=[]
 $( t in $Q:
  c,r=$f(t)
  if $)(r,'ln')$* $w(c):
   u=r[1]
   if $)(u,'$H'):
    u=u[1]
   fs.$%(pw(u,c))
  $&:
   $! $#
 if $/(fs)<1:
  $! $#
 $! $.($K(fs))
$, hasden_free(e):
 $! $2
$, isolate_eq(L,R,y):
 ${:
  r=isolate(L,R,y,$2,0)
 $3 $6:
  $! $#
 if r is $# or r=='all':
  $! $#
 $! r
$, separate(g,x,y):
 if $8(g,y):
  $! g,1
 if $8(g,x):
  $! 1,g
 fs=g[1:]if $)(g,'*')$&(g,)
 px=[]
 qy=[]
 $( f in fs:
  if $8(f,y):
   px.$%(f)
  $= $8(f,x):
   qy.$%(f)
  $= $)(f,'^')$* $8(f[1],x)$* $8(f[1],y)$* $)(f[2],'+'):
   tx=[t $( t in f[2][1:]if $8(t,y)]
   ty=[t $( t in f[2][1:]if $8(t,x)]
   if $/(tx)+$/(ty)!=$/(f[2])-1:
    $! $#
   px.$%(pw(f[1],$>(tx)))
   qy.$%(pw(f[1],$>(ty)))
  $&:
   $! $#
 $! $K(px),$K(qy)
$, expand_exp(e):
 if $0(e)is $- $1 or e[0]=='Q':
  $! e
 if e[0]=='^' $* $)(e[2],'+')$*(e[1]=='e' or $G(e[1])):
  $! $K([pw(e[1],t)$( t in e[2][1:]])
 $! simp((e[0],)+$1(expand_exp(a)$( a in e[1:]))
$, bernoulli(g,x,y):
 g=$?(g)
 $Q=g[1:]if $)(g,'+')$&(g,)
 groups={}
 $( t in $Q:
  k=$#
  fs=t[1:]if $)(t,'*')$&(t,)
  $a=[]
  $( f in fs:
   if f==y:
    k=1 if k is $# $& $#
   $= $)(f,'^')$* f[1]==y $* $G(f[2]):
    k=f[2]
   $= $8(f,y):
    $a.$%(f)
   $&:
    $! $#
  if k is $#:
   $! $#
  groups[k]=$`(groups.get(k,0),$K($a))
 if $/(groups)!=2 or 1 $- in groups:
  $! $#
 n=[k $( k in groups if k!=1][0]
 a=groups[1]
 b=groups[n]
 m=nsub(1,n)
 V='V_'
 vs=de1($_(YP[0],$<(m,$`($<(a,V),b))),x,V)
 if vs is $# or $- $)(vs,'=')or vs[1]!=V:
  $! $#
 $!('=',y,nice(pw(vs[2],ninv(m))))
''')
_x(r'''$, de2(F,x,y):
 y1,y2=YP
 c1,c2='c1','c2'
 G=$?(F)
 a=$[(G,y2)
 if a is $# or $/(a)!=2:
  $! $#
 A=a[1]
 $a=a[0]
 b=$[($a,y1)
 if b is $# or $/(b)>2:
  $! $#
 B=b[1]if $/(b)==2 $& 0
 $a=b[0]
 c=$[($a,y)
 if c is $# or $/(c)>2:
  $! $#
 C=c[1]if $/(c)==2 $& 0
 g=$m(c[0])
 $( t in(A,B,C):
  if has(t,y)or has(t,y1)or has(t,y2):
   $! $#
 if $8(A,x)$* $8(B,x)$* $8(C,x):
  y1s,y2s=charsol(A,B,C,x)
 $&:
  ce=cauchy_euler(A,B,C,x)
  if ce is $#:
   if C==0:
    V='V_'
    r=de1($`($<(A,YP[0]),$<(B,V),$m(g)),x,V)
    if r is $# or $- $)(r,'=')or r[1]!=V:
     $! $#
    r2=integ($Y(r[2],'c1','c2'),x)
    if r2 is $#:
     $! $#
    $!('=',y,$`(r2,c1))
   $! $#
  y1s,y2s=ce
 yh=$`($<(c1,y1s),$<(c2,y2s))
 if g==0:
  $!('=',y,yh)
 W=pyth($.($?($_($<(y1s,diff(y2s,x)),$<(diff(y1s,x),y2s)))))
 gg=$.($V(g,A))
 I1=integ($.($?($V($<(y2s,gg),W))),x)
 I2=integ($.($?($V($<(y1s,gg),W))),x)
 if I1 is $# or I2 is $#:
  $! $#
 yp=pyth($?($`($<($m(y1s),I1),$<(y2s,I2))))
 $!('=',y,nice($`(yh,yp)))
$, charsol(A,B,C,x):
 D=$.($?($_($<(B,B),$<(4,A,C))))
 if $z(D)$* fv(D)<0:
  al=$.($V($m(B),$<(2,A)))
  be=$.($V($O($m(D)),$<(2,A)))
  ex=pw('e',$<(al,x))
  $! $<(ex,fn('cos',$<(be,x))),$<(ex,fn('sin',$<(be,x)))
 if D==0:
  r=$.($V($m(B),$<(2,A)))
  $! pw('e',$<(r,x)),$<(x,pw('e',$<(r,x)))
 s=$O(D)
 r1=$.($V($`($m(B),s),$<(2,A)))
 r2=$.($V($_($m(B),s),$<(2,A)))
 $! pw('e',$<(r1,x)),pw('e',$<(r2,x))
$, cauchy_euler(A,B,C,x):
 a=$.($V(A,pw(x,2)))
 b=$.($V(B,x))
 if $-($8(a,x)$* $8(b,x)$* $8(C,x)):
  $! $#
 aa=a
 bb=$_(b,a)
 cc=C
 D=$.($?($_($<(bb,bb),$<(4,aa,cc))))
 lx=fn('ln',x)
 if $z(D)$* fv(D)<0:
  al=$.($V($m(bb),$<(2,aa)))
  be=$.($V($O($m(D)),$<(2,aa)))
  $! $<(pw(x,al),fn('cos',$<(be,lx))),$<(pw(x,al),fn('sin',$<(be,lx)))
 if D==0:
  r=$.($V($m(bb),$<(2,aa)))
  $! pw(x,r),$<(pw(x,r),lx)
 s=$O(D)
 r1=$.($V($`($m(bb),s),$<(2,aa)))
 r2=$.($V($_($m(bb),s),$<(2,aa)))
 $! pw(x,r1),pw(x,r2)
$, apply_ic(sol,x,y,conds,nconst):
 cs_=['c1','c2'][:nconst]
 eqs=[]
 if sol[1]==y:
  Y=sol[2]
  $( order,x0,v in conds:
   e=Y
   $( _ in $+(order):
    e=diff(e,x)
   eqs.$%(('=',$Y(e,x,x0),v))
 $&:
  $( order,x0,v in conds:
   if order==0:
    eqs.$%($Y($Y(sol,x,x0),y,v))
 used=[c $( c in cs_ if has(sol,c)]
 if $- eqs or $- used:
  $! sol
 rs=solve_system(eqs,used)
 if $- rs:
  $! 'false'
 s=rs[0]
 r=sol
 $( c in used:
  if c in s:
   r=(r[0],$Y(r[1],c,s[c]),$Y(r[2],c,s[c]))
 if r[1]==y:
  $!('=',y,nice(r[2]))
 rs2=isolate_eq(r[1],r[2],y)
 if rs2 is $- $# $* $/(rs2)>=1:
  $( cand in rs2:
   ok=$B
   $( order,x0,v in conds:
    if order==0:
     ${:
      if $H($Z($Y(cand,x,x0))-$Z(v))>1e-9:
       ok=$2
     $3 $6:
      pass
   if ok:
    $!('=',y,nice(cand))
 $! r
$, fextreme(f,x,kind,lo=$#,hi=$#):
 NC[0]=0
 d=$.(diff(f,x))
 cands=[]
 rs=$r(d,x)
 if rs is $#:
  rs=numeric_solve(d,x,$2,tofl($Z(lo))if lo is $- $# $* $5(lo)$& $#,
 tofl($Z(hi))if hi is $- $# $* $5(hi)$& $#)or[]
 if rs=='all':
  $! 'true'
 exp_=[]
 $( r in rs:
  ns=[w $( w in $e(r)if w[0]=='n' $* w[1:].isdigit()]
  if ns $* lo is $- $# $* hi is $- $#:
   $( k in $+(-50,51):
    exp_.$%($Y(r,ns[0],k))
  $= ns:
   exp_.$%(r)
  $&:
   exp_.$%(r)
 rs=exp_
 $( r in rs:
  r=clean(r)
  ns=[w $( w in $e(r)if w[0]=='n' $* w[1:].isdigit()]
  if ns:
   cands.$%(r)
   $7
  if $- $z(r):
   $7
  if lo is $- $# $* fv(r)<fv(lo)-1e-12:
   $7
  if hi is $- $# $* fv(r)>fv(hi)+1e-12:
   $7
  cands.$%(r)
 ends=[]
 ends.$%(lo if lo is $- $# $&('*',-1,'$P'))
 ends.$%(hi if hi is $- $# $& '$P')
 best=$#
 bv=$#
 pts=[]
 $( c in cands+ends:
  if c=='$P' or c==('*',-1,'$P'):
   v=$|(f,x,c)
  $&:
   cz=c
   $( w in $e(c):
    if w[0]=='n' $* w[1:].isdigit():
     cz=$Y(cz,w,0)
   v=$Y(f,x,cz)
   if has(v,'$I'):
    $7
  ${:
   if v=='$P':
    vv=$C('$P')
   $= v==('*',-1,'$P'):
    vv=$C('-$P')
   $&:
    vv=fv(v)
  $3 $6:
   $7
  if kind=='max':
   vv=-vv
  pts.$%((vv,c))
 if $- pts:
  $! $#
 pts.sort(key=$; p:p[0])
 m=pts[0][0]
 if m==$C('-$P'):
  win=[p[1]$( p in pts if p[0]==m]
 $&:
  win=[p[1]$( p in pts if $H(p[0]-m)<=1e-10*(1+$H(m))]
 win=sortsols(dedup(win))
 eqs=[('=',x,w)$( w in win]
 $! eqs[0]if $/(eqs)==1 $&('or',)+$1(eqs)
''')
_x(r'''$, nfextreme(f,x,kind,lo=$#,hi=$#):
 sg=1.0 if kind=='min' $&-1.0
 $, F(t):
  ${:
   v=$Z(f,{x:t})
   if $0(v)is $4:
    v=v.$U
   $! sg*v
  $3 $6:
   $! $C('$P')
 if lo is $# or hi is $#:
  a=-100.0 if lo is $# $& lo
  b=100.0 if hi is $# $& hi
 $&:
  a,b=lo,hi
 N=400
 best=a
 bv=F(a)
 $( i in $+(N+1):
  t=a+(b-a)*i/N
  v=F(t)
  if v<bv:
   bv=v
   best=t
 h=(b-a)/N
 l=max(a,best-h)
 r=min(b,best+h)
 g=($M.$O(5)-1)/2
 $( _ in $+(200):
  c=r-g*(r-l)
  d=l+g*(r-l)
  if F(c)<F(d):
   r=d
  $&:
   l=c
  if $H(r-l)<1e-12*(1+$H(l)):
   $R
 t=0.5*(l+r)
 $( side,bound in((1.0,hi),(-1.0,lo)):
  if bound is $#:
   vs=[F(side*10.0**k)$( k in(3,5,7)]
   if vs[0]<=bv $* vs[1]<=vs[0]$* vs[2]<=vs[1]$* vs[2]<bv:
    $! '$P' if side>0 $&('*',-1,'$P')
 ${:
  d=diff(f,x)
  $, G(u):
   ${:
    v=$Z(d,{x:u})
    $! v.$U if $0(v)is $4 $& v
   $3 $6:
    $! $#
  t2=newton(G,t)
  if t2 is $- $# $* $H(t2-t)<10*h $*(lo is $# or t2>=lo)$*(hi is $# or t2<=hi):
   t=t2
 $3 $6:
  pass
 $! snap(t)
$, domain(f,x):
 conds=[]
 domconds(f,x,conds)
 if $- conds:
  $!('<',('*',-1,'$P'),x)if $2 $& 'true'
 pts=[]
 $( rel,g in conds:
  rs=$r(g,x)
  if rs is $#:
   $! $#
  if rs=='all':
   $7
  $( r in rs:
   if $z(r):
    pts.$%(r)
 pts=sortsols(dedup(pts))
 $, ok(t):
  $( rel,g in conds:
   ${:
    v=$Z(g,{x:t})
   $3 $6:
    $! $2
   if $0(v)is $4:
    if $H(v.imag)>1e-9:
     $! $2
    v=v.$U
   if $- relok(rel,v):
    $! $2
  $! $B
 $, okexact(p):
  $( rel,g in conds:
   ${:
    v=$Y(g,x,p)
    vv=fv(v)
   $3 $6:
    $! $2
   if $H(vv)<1e-12:
    vv=0.0
   if $- relok(rel,vv):
    $! $2
  $! $B
 $g=[fv(p)$( p in pts]
 if $- $g:
  $! 'true' if ok(0.5)$& 'false'
 segs=[('I',$#,pts[0],ok($g[0]-max(1.0,$H($g[0]))))]
 $( i in $+($/(pts)):
  segs.$%(('P',pts[i],pts[i],okexact(pts[i])))
  if i+1<$/(pts):
   segs.$%(('I',pts[i],pts[i+1],ok(0.5*($g[i]+$g[i+1]))))
 segs.$%(('I',pts[-1],$#,ok($g[-1]+max(1.0,$H($g[-1])))))
 $! segs_to_bool(segs,x)
$, domconds(f,x,$9):
 if $0(f)is $- $1 or f[0]=='Q' or $8(f,x):
  $!
 h=f[0]
 if h=='^':
  b,p=f[1],f[2]
  if $G(p)$* $c(p)<0:
   $9.$%(('/=',b))
  if isq(p)$* p[2]%2==0:
   $9.$%(('>=' if $c(p)>0 $& '>',b))
 $= h in('ln','log'):
  $9.$%(('>',f[1]))
 $= h in('$y','arccos'):
  $9.$%(('<=',$_(fn('$H',f[1]),1)))
 $= h=='tan':
  $9.$%(('/=',fn('cos',f[1])))
 $( a in f[1:]:
  domconds(a,x,$9)
''')
_x(r'''import $M
$, ismat(e):
 $! $)(e,'mat')
$, $h(e):
 $! $)(e,'$J')
$, $X(M):
 $![$J(r[1:])$( r in M[1:]]
$, mk(R):
 $!('mat',)+$1(('$J',)+$1(r)$( r in R)
$, lst(xs):
 $!('$J',)+$1(xs)
$, dims(M):
 $! $/(M)-1,$/(M[1])-1
$, tomat(e):
 if ismat(e):
  $! e
 if $h(e):
  $! mk([$J(e[1:])])
 err("Matrix expected")
$, ac(e):
 $! $.($?(e))if hasdenom(e)$& $?(e)
$, m_add(A,B,sgn=1):
 if dims(A)!=dims(B):
  err("Dimension error")
 a=$X(A)
 b=$X(B)
 $! mk([[$`(a[i][j],$<(sgn,b[i][j]))$( j in $+($/(a[0]))]$( i in $+($/(a))])
$, m_scale(A,c):
 $! mk([[$<(c,v)$( v in r]$( r in $X(A)])
$, m_map(A,f):
 $! mk([[f(v)$( v in r]$( r in $X(A)])
$, m_mul(A,B):
 a=$X(A)
 b=$X(B)
 if $/(a[0])!=$/(b):
  err("Dimension error")
 n=$/(b)
 $! mk([[ac($>([$<(a[i][k],b[k][j])$( k in $+(n)]))$( j in $+($/(b[0]))]$( i in $+($/(a))])
$, ident(n):
 cells(n,n)
 $! mk([[1 if i==j $& 0 $( j in $+(n)]$( i in $+(n)])
$, m_pow(A,k):
 m,n=dims(A)
 if m!=n:
  err("Square matrix required")
 if k<0:
  A=m_inv(A)
  k=-k
 R=ident(n)
 $F k>0:
  if k&1:
   R=m_mul(R,A)
  k>>=1
  if k:
   A=m_mul(A,A)
 $! R
$, transpose(A):
 if $h(A):
  $! mk([[v]$( v in A[1:]])
 a=$X(A)
 $! mk([[a[i][j]$( i in $+($/(a))]$( j in $+($/(a[0]))])
$, det(A):
 a=$X(A)
 n=$/(a)
 if n!=$/(a[0]):
  err("Square matrix required")
 if n==1:
  $! a[0][0]
 if n==2:
  $! ac($_($<(a[0][0],a[1][1]),$<(a[0][1],a[1][0])))
 if n==3:
  t=[]
  $( j in $+(3):
   minor=$_($<(a[1][(j+1)%3],a[2][(j+2)%3]),$<(a[1][(j+2)%3],a[2][(j+1)%3]))
   t.$%($<(a[0][j],minor))
  $! ac($>(t))
 M=a
 sign=1
 prev=1
 $( k in $+(n-1):
  if ac(M[k][k])==0:
   sw=$#
   $( i in $+(k+1,n):
    if ac(M[i][k])!=0:
     sw=i
     $R
   if sw is $#:
    $! 0
   M[k],M[sw]=M[sw],M[k]
   sign=-sign
  $( i in $+(k+1,n):
   $( j in $+(k+1,n):
    M[i][j]=ac($V($_($<(M[i][j],M[k][k]),$<(M[i][k],M[k][j])),prev))
  prev=M[k][k]
 $! ac($<(sign,M[n-1][n-1]))
$, iszero(v):
 v=ac(v)
 if v==0:
  $! $B
 if $0(v)is $C $* $H(v)<1e-13:
  $! $B
 $! $2
$, rref(A,full=$B):
 M=$X(A)
 m=$/(M)
 n=$/(M[0])
 r=0
 $( c in $+(n):
  if r>=m:
   $R
  p=$#
  if hasfloat_m(M):
   best=0.0
   $( i in $+(r,m):
    ${:
     v=$H($Z(M[i][c]))
    $3 $6:
     v=1.0 if $- iszero(M[i][c])$& 0.0
    if v>best+1e-14:
     best=v
     p=i
   if best<1e-13:
    p=$#
  $&:
   $( i in $+(r,m):
    if $- iszero(M[i][c]):
     p=i
     $R
  if p is $#:
   $7
  M[r],M[p]=M[p],M[r]
  pv=M[r][c]
  if full:
   M[r]=[ac($V(v,pv))$( v in M[r]]
  $&:
   M[r]=[ac($V(v,pv))$( v in M[r]]
  rng=$+(m)if full $& $+(r+1,m)
  $( i in rng:
   if i!=r $* $- iszero(M[i][c]):
    f=M[i][c]
    M[i]=[ac($_(M[i][j],$<(f,M[r][j])))$( j in $+(n)]
  r+=1
 $( i in $+(m):
  $( j in $+(n):
   if $0(M[i][j])is $C $* $H(M[i][j])<1e-13:
    M[i][j]=0.0
 $! mk(M)
$, hasfloat_m(M):
 $( r in M:
  $( v in r:
   if $b(v):
    $! $B
 $! $2
$, minor(a,i,j):
 $![[a[r][c]$( c in $+($/(a))if c!=j]$( r in $+($/(a))if r!=i]
$, m_inv(A):
 m,n=dims(A)
 if m!=n:
  err("Square matrix required")
 a0=$X(A)
 if n<=3 $* $- all([$G(v)$( r in a0 $( v in r]):
  D=det(A)
  if iszero(D):
   err("Singular matrix")
  if n==1:
   $! mk([[nice(pw(D,-1))]])
  $9=[]
  $( i in $+(n):
   row=[]
   $( j in $+(n):
    c=det(mk(minor(a0,j,i)))
    if(i+j)%2:
     c=$m(c)
    row.$%(nice(ac($V(c,D))))
   $9.$%(row)
  $! mk($9)
 a=$X(A)
 aug=mk([a[i]+[1 if i==j $& 0 $( j in $+(n)]$( i in $+(n)])
 R=$X(rref(aug))
 $( i in $+(n):
  $( j in $+(n):
   if $- iszero($_(R[i][j],1 if i==j $& 0)):
    err("Singular matrix")
 $! mk([[nice(R[i][n+j])$( j in $+(n)]$( i in $+(n)])
$, trace(A):
 a=$X(A)
 $! $>([a[i][i]$( i in $+($/(a))])
$, charpoly(A,lam):
 a=$X(A)
 n=$/(a)
 if n!=$/(a[0]):
  err("Square matrix required")
 I=ident(n)
 Mk=mk([[0]*n $( _ in $+(n)])
 cs=[0]*(n+1)
 cs[n]=1
 $( k in $+(1,n+1):
  Mk=m_add(m_mul(A,Mk),m_scale(I,cs[n-k+1]))
  cs[n-k]=ac($V($m(trace(m_mul(A,Mk))),k))
 $! $>([$<(cs[k],pw(lam,k))$( k in $+(n+1)])
$, eigvl(A):
 if hasfloat_m($X(A)):
  ${:
   E=m_map(A,exactify)
  $3 $6:
   E=$#
  if E is $- $# $* $- hasfloat_m($X(E)):
   $! evalf(eigvl(E))
 lam='L_'
 p=charpoly(A,lam)
 f=p
 if $- hasfloat_m($X(A)):
  ${:
   f=factor_expr(p)
  $3 $6:
   f=p
  if $)(f,'hold'):
   f=f[1]
 $9=[]
 $( g in(f[1:]if $)(f,'*')$&(f,)):
  k=1
  if $)(g,'^')$* $i(g[2])$* g[2]>0:
   g,k=g[1],g[2]
  if $8(g,lam):
   $7
  z=zeros(g,lam,$B)
  if z is $#:
   err("Cannot compute eigenvalues")
  z=$J(z[1:])
  d=degree(g,lam)
  $( v in z:
   m=mult(g,lam,v,d)if d is $- $# $* $/(z)<d $& 1
   $9+=[v]*(k*m)
 if $- $9:
  err("Cannot compute eigenvalues")
 $, key(v):
  if $- $5(v):
   $!(1,0.0,0.0,okey(v))
  z=$4($Z(v))
  $!(0,-$H(z),-z.$U,-z.imag)
 $9.sort(key=key)
 $! lst($9)
$, mult(g,lam,v,d):
 m=1
 h=g
 $F m<d:
  h=diff_(h,lam)
  w=$Y(h,lam,v)
  if $b(w)or $b(v):
   ${:
    if $H($4($Z(w)))>1e-6*(1+$H($4($Z(v))))**d:
     $R
   $3 $6:
    $R
  $= $- iszero(ac($?(w))):
   $R
  m+=1
 $! m
$, diff_(e,x):
 $! diff(e,x)
$, nullspace(A):
 R=$X(rref(A))
 m=$/(R)
 n=$/(R[0])
 piv=[]
 $( i in $+(m):
  $( j in $+(n):
   if $- iszero(R[i][j]):
    piv.$%((i,j))
    $R
 pc=[j $( i,j in piv]
 free=[j $( j in $+(n)if j $- in pc]
 basis=[]
 $( f in free:
  v=[0]*n
  v[f]=1
  $( i,j in piv:
   v[j]=ac($m(R[i][f]))
  basis.$%(v)
 $! basis
''')
_x(r'''$, eigvc(A):
 if hasfloat_m($X(A)):
  ${:
   E=m_map(A,exactify)
  $3 $6:
   E=$#
  if E is $- $# $* $- hasfloat_m($X(E)):
   $! evalf(eigvc(E))
 $g=eigvl(A)
 n=dims(A)[0]
 cols=[]
 seen=[]
 $( lv in $g[1:]:
  if lv in seen:
   $7
  seen.$%(lv)
  if $b(lv)or hasfloat_m($X(A)):
   cols.$%(numeigvec(A,lv))
   $7
  B=m_add(A,m_scale(ident(n),lv),-1)
  B=m_map(B,$; v:ac(v))
  ns=nullspace(B)
  $( v in ns:
   cols.$%(unitvec(v))
 if $- cols:
  err("Cannot compute eigenvectors")
 M=mk([[cols[j][i]$( j in $+($/(cols))]$( i in $+(n)])
 $( c in cols:
  $( v in c:
   if esize(v)>60:
    $! evalf(M)
 $! M
$, numeigvec(A,lam):
 a=[[$4($Z(c))$( c in r]$( r in $X(A)]
 n=$/(a)
 mu=$4($Z(lam))
 mu+=1e-9*(1+$H(mu))
 M=[[a[i][j]-(mu if i==j $& 0)$( j in $+(n)]$( i in $+(n)]
 x=[$4(1.0+0.37*i)$( i in $+(n)]
 $( it in $+(4):
  y=clsolve(M,x)
  big=max([$H(v)$( v in y])or 1.0
  x=[v/big $( v in y]
 nrm=$M.$O(sum([$H(v)**2 $( v in x]))or 1.0
 x=[v/nrm $( v in x]
 k=0
 $( i in $+(n):
  if $H(x[i])>$H(x[k])+1e-12:
   k=i
 ph=x[k]/$H(x[k])
 $9=[]
 $( v in x:
  v=v/ph
  re=0.0 if $H(v.$U)<1e-12 $& v.$U
  im=0.0 if $H(v.imag)<1e-12 $& v.imag
  $9.$%(re if im==0.0 $& fromcomplex($4(re,im)))
 $! $9
$, clsolve(M,b):
 n=$/(M)
 a=[$J(M[i])+[b[i]]$( i in $+(n)]
 $( c in $+(n):
  p=c
  $( r in $+(c+1,n):
   if $H(a[r][c])>$H(a[p][c]):
    p=r
  a[c],a[p]=a[p],a[c]
  if $H(a[c][c])<1e-14:
   a[c][c]=1e-14
  $( r in $+(c+1,n):
   f=a[r][c]/a[c][c]
   if f:
    $( k in $+(c,n+1):
     a[r][k]-=f*a[c][k]
 x=[0j]*n
 $( i in $+(n-1,-1,-1):
  t=a[i][n]
  $( k in $+(i+1,n):
   t-=a[i][k]*x[k]
  x[i]=t/a[i][i]
 $! x
$, coefs(e,$9):
 if $G(e):
  $9.$%(e)
 $= $)(e,'+'):
  $( t in e[1:]:
   coefs(t,$9)
 $= $)(e,'*')$* $G(e[1]):
  $9.$%(e[1])
 $&:
  $9.$%(1)
$, unitvec(v):
 if hasfloat_m([v]):
  nrm=$O($>([$<(c,fn('conj',c))$( c in v]))
  $![nice(ac($V(c,nrm)))$( c in v]
 cs=[]
 $( c in v:
  coefs(c,cs)
 den=1
 num=0
 $( q in cs:
  if $w(q)$* q!=0:
   a,b=nd(q)
   den=ilcm(den,b)
   num=igcd(num,a)
 k=Q(den,num)if num $& 1
 $( c in v:
  if $- iszero(c):
   if isneg(c):
    k=$m(k)
   $R
 w=[ac($?($<(k,c)))$( c in v]
 n2=ac($?($>([$<(c,fn('conj',c))$( c in w])))
 r=$O(n2)
 if $G(r)or $- $)(r,'^'):
  $![ac($V(c,r))$( c in w]
 inv=('^',r[1],$m(r[2]))
 $![c if iszero(c)$&('*',c,inv)if $)(c,'+')$& $<(c,inv)$( c in w]
$, esize(e):
 if $0(e)is $- $1 or e[0]=='Q':
  $! 1
 k=1
 $( a in e[1:]:
  k+=esize(a)
 $! k
$, lu(A):
 a=$X(A)
 m=$/(a)
 n=$/(a[0])
 L=[[1 if i==j $& 0 $( j in $+(m)]$( i in $+(m)]
 P=$J($+(m))
 U=a
 $( k in $+(min(m,n)):
  p=$#
  if hasfloat_m(U):
   best=-1.0
   $( i in $+(k,m):
    v=$H($Z(U[i][k]))
    if v>best:
     best=v
     p=i
   if best<1e-14:
    p=$#
  $&:
   $( i in $+(k,m):
    if $- iszero(U[i][k]):
     p=i
     $R
  if p is $#:
   $7
  if p!=k:
   U[k],U[p]=U[p],U[k]
   P[k],P[p]=P[p],P[k]
   $( j in $+(k):
    L[k][j],L[p][j]=L[p][j],L[k][j]
  $( i in $+(k+1,m):
   f=ac($V(U[i][k],U[k][k]))
   L[i][k]=f
   U[i]=[ac($_(U[i][j],$<(f,U[k][j])))$( j in $+(n)]
 Pm=[[1 if P[i]==j $& 0 $( j in $+(m)]$( i in $+(m)]
 $! mk(L),mk(U),mk(Pm)
$, qr(A):
 a=$X(A)
 m=$/(a)
 n=$/(a[0])
 cols=[[a[i][j]$( i in $+(m)]$( j in $+(n)]
 Qc=[]
 R=[[0]*n $( _ in $+(n)]
 $( j in $+(n):
  v=cols[j]
  $( k in $+($/(Qc)):
   r=ac($>([$<(Qc[k][i],v[i])$( i in $+(m)]))
   R[k][j]=r
   v=[ac($_(v[i],$<(r,Qc[k][i])))$( i in $+(m)]
  nrm=nice($O(ac($>([pw(c,2)$( c in v]))))
  R[j][j]=nrm
  if iszero(nrm):
   Qc.$%([0]*m)
  $&:
   Qc.$%([nice(ac($V(c,nrm)))$( c in v])
 Qm=mk([[Qc[j][i]$( j in $+(n)]$( i in $+(m)])
 $! Qm,mk(R)
$, crossp(u,v):
 a=vec(u)
 b=vec(v)
 if $/(a)==2:
  a=a+[0]
  b=b+[0]
 if $/(a)!=3 or $/(b)!=3:
  err("Dimension error")
 r=[ac($_($<(a[1],b[2]),$<(a[2],b[1]))),
 ac($_($<(a[2],b[0]),$<(a[0],b[2]))),
 ac($_($<(a[0],b[1]),$<(a[1],b[0])))]
 $! revec(r,u)
$, vec(u):
 if $h(u):
  $! $J(u[1:])
 if ismat(u):
  R=$X(u)
  if $/(R)==1:
   $! R[0]
  if $/(R[0])==1:
   $![r[0]$( r in R]
 err("Vector expected")
$, revec(r,like):
 if $h(like):
  $! lst(r)
 R=$X(like)
 if $/(R)==1:
  $! mk([r])
 $! mk([[v]$( v in r])
$, dotp(u,v):
 a=vec(u)
 b=vec(v)
 if $/(a)!=$/(b):
  err("Dimension error")
 $! ac($>([$<(a[i],b[i])$( i in $+($/(a))]))
$, norm(A):
 if $h(A)or ismat(A)$*(dims(A)[0]==1 or dims(A)[1]==1):
  v=vec(A)
  $! nice($O(ac($>([$<(c,fn('conj',c))$( c in v]))))
 $! nice($O(ac($>([$<(c,fn('conj',c))$( r in $X(A)$( c in r]))))
$, unitv(u):
 nrm=norm(u)
 $! revec([nice(ac($V(c,nrm)))$( c in vec(u)],u)
$, rownorm(A):
 if $- ismat(A):
  err('Argument must be a matrix')
 $! maxexpr([ac($>([fn('$H',c)$( c in r]))$( r in $X(A)])
$, colnorm(A):
 if $- ismat(A):
  err('Argument must be a matrix')
 $! rownorm(transpose(A))
$, maxexpr(xs):
 best=$#
 bv=$#
 $( x in xs:
  v=$Z(x)
  if best is $# or v>bv:
   best=x
   bv=v
 $! best
$, augment(A,B):
 if $h(A)$* $h(B):
  $! A+B[1:]
 a=$X(tomat(A))
 b=$X(tomat(B))
 if $/(a)!=$/(b):
  err("Dimension error")
 $! mk([a[i]+b[i]$( i in $+($/(a))])
$, colaugment(A,B):
 a=$X(tomat(A))
 b=$X(tomat(B))
 if $/(a[0])!=$/(b[0]):
  err("Dimension error")
 $! mk(a+b)
$, submat(A,r1=1,c1=1,r2=$#,c2=$#):
 a=$X(A)
 if r2 is $#:
  r2=$/(a)
 if c2 is $#:
  c2=$/(a[0])
 $! mk([a[i][c1-1:c2]$( i in $+(r1-1,r2)])
$, rowswap(A,i,j):
 a=$X(A)
 a[i-1],a[j-1]=a[j-1],a[i-1]
 $! mk(a)
''')
_x(r'''$, rowadd(A,i,j):
 a=$X(A)
 a[j-1]=[$`(a[j-1][k],a[i-1][k])$( k in $+($/(a[0]))]
 $! mk(a)
$, mrow(c,A,i):
 a=$X(A)
 a[i-1]=[$<(c,v)$( v in a[i-1]]
 $! mk(a)
$, mrowadd(c,A,i,j):
 a=$X(A)
 a[j-1]=[ac($`(a[j-1][k],$<(c,a[i-1][k])))$( k in $+($/(a[0]))]
 $! mk(a)
$, diag(A):
 if $h(A):
  n=$/(A)-1
  $! mk([[A[i+1]if i==j $& 0 $( j in $+(n)]$( i in $+(n)])
 a=$X(A)
 if $/(a)==1 or $/(a[0])==1:
  v=vec(A)
  $! diag(lst(v))
 $! lst([a[i][i]$( i in $+(min($/(a),$/(a[0])))])
$, matlist(A):
 $! lst([v $( r in $X(A)$( v in r])
$, listmat(L,c=$#):
 xs=$J(L[1:])
 if c is $#:
  c=$/(xs)
 if $- $i(c)or c<1:
  err('Invalid number of columns')
 $9=[]
 $F xs:
  r=xs[:c]
  xs=xs[c:]
  $F $/(r)<c:
   r.$%(0)
  $9.$%(r)
 $! mk($9)
$, simult(A,b):
 a=$X(A)
 n=$/(a)
 bb=$X(tomat(b))if ismat(b)$&[[v]$( v in b[1:]]
 if $/(bb)!=n:
  bb=$X(transpose(b))
 k=$/(bb[0])
 R=$X(rref(mk([a[i]+bb[i]$( i in $+(n)])))
 $( i in $+(n):
  if iszero(R[i][i]):
   err("Singular matrix")
 $! mk([[nice(R[i][n+j])$( j in $+(k)]$( i in $+(n)])
$, cumsum(L):
 if $h(L):
  $9=[]
  s=0
  $( v in L[1:]:
   s=$`(s,v)
   $9.$%(s)
  $! lst($9)
 a=$X(L)
 $9=[]
 acc=[0]*$/(a[0])
 $( r in a:
  acc=[$`(acc[j],r[j])$( j in $+($/(r))]
  $9.$%($J(acc))
 $! mk($9)
$, polar_vec(u):
 v=vec(u)
 if $/(v)==2:
  r=nice($O(ac($`(pw(v[0],2),pw(v[1],2)))))
  th=fn('$l',$`(v[0],$<('i',v[1])))
  $!('$p','['+fmtx(r)+' \u2220'+fmtx(th)+']')
 err("Dimension error")
$, fmtx(e):
 $! fmt(e)
$, cylind(u):
 v=vec(u)
 if $/(v)!=3:
  err("Dimension error")
 r=nice($O(ac($`(pw(v[0],2),pw(v[1],2)))))
 th=fn('$l',$`(v[0],$<('i',v[1])))
 $!('$p','['+fmtx(r)+' \u2220'+fmtx(th)+' '+fmtx(v[2])+']')
$, sphere(u):
 v=vec(u)
 if $/(v)!=3:
  err("Dimension error")
 rho=nice($O(ac($`(pw(v[0],2),pw(v[1],2),pw(v[2],2)))))
 th=fn('$l',$`(v[0],$<('i',v[1])))
 ph=fn('arccos',$V(v[2],rho))if rho!=0 $& 0
 $!('$p','['+fmtx(rho)+' \u2220'+fmtx(th)+' \u2220'+fmtx(ph)+']')
$, lsum(L,a=1,b=$#):
 xs=$J(L[1:])
 if b is $#:
  b=$/(xs)
 $! $>(xs[a-1:b])
$, lprod(L,a=1,b=$#):
 xs=$J(L[1:])
 if b is $#:
  b=$/(xs)
 $! $K(xs[a-1:b])
$, mean(L,F=$#):
 xs=$J(L[1:])
 if F is $#:
  $! $V($>(xs),$/(xs))
 fs=$J(F[1:])
 $! $V($>([$<(xs[i],fs[i])$( i in $+($/(xs))]),$>(fs))
$, sortkey(v):
 ${:
  x=$Z(v)
  $! x.$U if $0(x)is $4 $& x
 $3 $6:
  $! 0.0
$, median(L):
 xs=sorted($J(L[1:]),key=sortkey)
 n=$/(xs)
 if n%2:
  $! xs[n//2]
 $! $V($`(xs[n//2-1],xs[n//2]),2)
$, variance(L,pop=$2):
 xs=$J(L[1:])
 n=$/(xs)
 m=mean(L)
 s=$>([pw($_(v,m),2)$( v in xs])
 $! ac($V(s,n if pop $& n-1))
$, stddev(L,pop=$2):
 $! nice($O(variance(L,pop)))
$, sorta(L):
 $! lst(sorted($J(L[1:]),key=sortkey))
$, sortd(L):
 $! lst(sorted($J(L[1:]),key=sortkey,reverse=$B))
$, deltalist(L):
 xs=$J(L[1:])
 $! lst([$_(xs[i+1],xs[i])$( i in $+($/(xs)-1)])
''')
_x(r'''SET={'$l':'rad','mode':'auto','$D':'$U'}
$, lmap(f,a):
 if $h(a):
  $!('$J',)+$1(lmap(f,v)$( v in a[1:])
 if ismat(a):
  $!('mat',)+$1(lmap(f,r)$( r in a[1:])
 $! f(a)
$, lmap2(f,a,b):
 if $h(a)$* $h(b):
  if $/(a)!=$/(b):
   err("Dimension error")
  $!('$J',)+$1(lmap2(f,a[i],b[i])$( i in $+(1,$/(a)))
 if $h(a):
  $!('$J',)+$1(lmap2(f,v,b)$( v in a[1:])
 if $h(b):
  $!('$J',)+$1(lmap2(f,a,v)$( v in b[1:])
 if ismat(a)$* ismat(b):
  $!('mat',)+$1(lmap2(f,a[i],b[i])$( i in $+(1,$/(a)))
 if ismat(a):
  $!('mat',)+$1(lmap2(f,r,b)$( r in a[1:])
 if ismat(b):
  $!('mat',)+$1(lmap2(f,a,r)$( r in b[1:])
 $! f(a,b)
$, vadd(a,b):
 if ismat(a)$* ismat(b):
  $! m_add(a,b)
 if $h(a)or $h(b)or ismat(a)or ismat(b):
  $! lmap2($`,a,b)
 if isrel(a)or isrel(b):
  $! relop($`,a,b)
 if isstr(a)or isstr(b):
  err("Data $0 error")
 $! $`(a,b)
$, vsub(a,b):
 $! vadd(a,vneg(b))
$, vneg(a):
 $! lmap($m,a)if $- isrel(a)$&(a[0],$m(a[1]),$m(a[2]))
$, vmul(a,b):
 if ismat(a)$* ismat(b):
  $! m_mul(a,b)
 if ismat(a)$* $h(b)or $h(a)$* ismat(b):
  $! m_mul(tomat(a),tomat(b)if ismat(b)$& transpose(b))
 if $h(a)or $h(b)or ismat(a)or ismat(b):
  $! lmap2($<,a,b)
 if isrel(a)or isrel(b):
  $! relop($<,a,b)
 $! $<(a,b)
$, vdiv(a,b):
 if ismat(b):
  if ismat(a):
   $! m_mul(a,m_inv(b))
  $! vmul(a,m_inv(b))
 if $h(a)or $h(b)or ismat(a):
  $! lmap2($V,a,b)
 if isrel(a)or isrel(b):
  $! relop($V,a,b)
 if b==0 $* $5(a):
  $! '$I'
 $! $V(a,b)
$, vpow(a,b):
 if ismat(a):
  if $0(b)is $q:
   $! m_pow(a,b)
  if b=='T_t':
   $! transpose(a)
  err("Domain error")
 if $h(a)or $h(b):
  $! lmap2(pw,a,b)
 if isrel(a):
  $!(a[0],pw(a[1],b),pw(a[2],b))
 $! pw(a,b)
$, relop(f,a,b):
 if isrel(a)$* isrel(b):
  $!(a[0],f(a[1],b[1]),f(a[2],b[2]))
 if isrel(a):
  $!(a[0],f(a[1],b),f(a[2],b))
 $!(b[0],f(a,b[1]),f(a,b[2]))
$, isstr(e):
 $! $)(e,'$p')
$, dotop(op,a,b):
 if op=='.*':
  $! lmap2($<,a,b)
 if op=='./':
  $! lmap2($V,a,b)
 $! lmap2(pw,a,b)
$, rel(op,a,b):
 if $h(a)or $h(b):
  $! lmap2($; x,y:rel(op,x,y),a,b)
 if isstr(a)$* isstr(b):
  r=cmpstr(op,a[1],b[1])
  if r is $- $#:
   $! 'true' if r $& 'false'
 d=$.($_(a,b))if $-(isstr(a)or isstr(b))$& $#
 if d is $- $# $* $5(d)$* d!='$I':
  ${:
   v=$Z(d)
  $3 $6:
   v=$#
  if v is $- $#:
   if $0(v)is $4:
    if op=='=':
     $! 'true' if $H(v)<1e-13 $& 'false'
    if op=='/=':
     $! 'false' if $H(v)<1e-13 $& 'true'
    err("Non-$U comparison")
   if d==0 or $H(v)<1e-300:
    v=0.0
   $&:
    ${:
     sc=$H($Z(a))+$H($Z(b))
    $3 $6:
     sc=0.0
    if $H(v)<1e-12*(1+sc):
     v=0.0
   r={'=':v==0,'/=':v!=0,'<':v<0,'>':v>0,'<=':v<=0,'>=':v>=0}[op]
   $! 'true' if r $& 'false'
 if d is $- $# $* op in('=','/=')$* $- $5(d):
  ${:
   z=expand_full(d)if hasattr(PO,'expand_full')$& $?(d)
  $3 $6:
   z=d
  if z==0:
   d=0
 if op=='=' $* d==0:
  $! 'true'
 if op=='/=' $* d==0:
  $! 'false'
 $!(op,a,b)
$, cmpstr(op,a,b):
 if op=='=':
  $! a==b
 if op=='/=':
  $! a!=b
 $! $#
$, tobool(v):
 if v=='true':
  $! $B
 if v=='false':
  $! $2
 $! $#
$, land(a,b):
 ta=tobool(a)
 tb=tobool(b)
 if ta is $2 or tb is $2:
  $! 'false'
 if ta is $B:
  $! b
 if tb is $B:
  $! a
 $! flat('$*',a,b)
$, lor(a,b):
 ta=tobool(a)
 tb=tobool(b)
 if ta is $B or tb is $B:
  $! 'true'
 if ta is $2:
  $! b
 if tb is $2:
  $! a
 $! flat('or',a,b)
$, flat(op,a,b):
 xs=[]
 $( v in(a,b):
  if $)(v,op):
   xs.$}(v[1:])
  $&:
   xs.$%(v)
 $!(op,)+$1(xs)
$, lnot(a):
 t=tobool(a)
 if t is $- $#:
  $! 'false' if t $& 'true'
 if $i(a):
  $!~a
 neg_={'<':'>=','>':'<=','<=':'>','>=':'<','=':'/=','/=':'='}
 if isrel(a):
  $!(neg_[a[0]],a[1],a[2])
 $!('$-',a)
$, lxor(a,b):
 ta=tobool(a)
 tb=tobool(b)
 if ta is $- $# $* tb is $- $#:
  $! 'true' if ta!=tb $& 'false'
 if $i(a)$* $i(b):
  $! a^b
 $!('xor',a,b)
$, need_int(n):
 if isfl(n)$* finite(n)$* n==$M.floor(n):
  $! $q(n)
 if $- $i(n):
  err("Argument must be an integer")
 $! n
$, gcd_(a,b):
 if $w(a)$* $w(b):
  an,ad=nd(a)
  bn,bd=nd(b)
  $! Q(igcd(an,bn),ilcm(ad,bd))
 if isfl(a)or isfl(b):
  $! $C(igcd($q(a),$q(b)))
 $! poly_gcd_expr(a,b)
$, lcm_(a,b):
 if $w(a)$* $w(b):
  an,ad=nd(a)
  bn,bd=nd(b)
  $! Q(ilcm(an,bn),igcd(ad,bd))
 g=gcd_(a,b)
 $! $.($V($<(a,b),g))
$, mod_(a,b):
 if $)(a,'^')$* $i(a[1])$* $i(a[2])$* a[2]>0 $* $i(b)$* b!=0:
  r=powmod(a[1],a[2],$H(b))
  $! r-$H(b)if b<0 $* r $& r
 if $G(a)$* $G(b):
  if b==0:
   $! a
  $! nsub(a,nmul(b,nfloor(ndiv(a,b))))
 $!('mod',a,b)
$, remain_(a,b):
 if $G(a)$* $G(b):
  if b==0:
   $! a
  q=ndiv(a,b)
  t=nfloor(q)if $c(q)>=0 $&-nfloor(nneg(q))
  $! nsub(a,nmul(b,t))
 $!('remain',a,b)
$, intdiv_(a,b):
 q=ndiv(a,b)
 if $c(q)>=0:
  $! nfloor(q)
 $!-nfloor(nneg(q))
$, bigcomb(n,k):
 if $-($i(n)$* $i(k))or k<=0:
  $! $2
 m=min(k,$H(n-k))if n>=k $& k
 $! m*ibits(n)>MAXBITS
$, ncr_(n,k):
 if $i(n)$* $i(k):
  if k<0 or(n>=0 $* k>n):
   $! 0
  if bigcomb(n,k):
   $!('ncr',n,k)
  $! binom(n,k)if n>=0 $& gen_ncr(n,k)
 if $i(k)$* k>=0:
  $! gen_ncr(n,k)
 if isfl(n)or isfl(k):
  $! CA_gamma_ratio(n,k)
 $!('ncr',n,k)
$, gen_ncr(n,k):
 r=1
 $( i in $+(k):
  r=$<(r,$_(n,i))
 f=1
 $( i in $+(2,k+1):
  f*=i
 $! $<(r,Q(1,f))
''')
_x(r'''$, npr_(n,k):
 if $i(n)$* $i(k)$* k*ibits(n)>MAXBITS:
  $!('npr',n,k)
 if $i(k)$* k>=0:
  r=1
  $( i in $+(k):
   r=$<(r,$_(n,i))
  $! r
 $!('npr',n,k)
$, CA_gamma_ratio(n,k):
 n=tofl(n)
 k=tofl(k)
 $! gamma(n+1)/(gamma(k+1)*gamma(n-k+1))
$, isprime_(n):
 n=need_int(n)
 if $H(n)>>1024:
  err('Number too large $( isPrime')
 $! 'true' if isprime($H(n))$& 'false'
$, round_(x,d=0):
 if $5(x)$* $- $G(x):
  x=evalf(x)
 if $G(x):
  if $w(x)$* d==0:
   $! nfloor(nadd(x,$x))if $c(x)>=0 $&-nfloor(nadd(nneg(x),$x))
  v=tofl(x)
  if $- finite(v):
   $! x
  p=10.0**d
  r=$M.floor($H(v)*p+0.5)/p
  $! r if v>=0 $&-r
 $!('round',x,d)
$, ipart_(x):
 if $5(x)$* $- $G(x):
  x=evalf(x)
 if $G(x):
  if $0(x)is $C:
   $! $C($q(x))
  $! nfloor(x)if $c(x)>=0 $&-nfloor(nneg(x))
 $!('ipart',x)
$, fpart_(x):
 i=ipart_(x)
 if $)(i,'ipart'):
  $!('fpart',x)
 $! $_(x,i)
$, approx_(e):
 $! evalf(e)
$, exact_(e,tol=$#):
 if tol is $- $#:
  tol=tofl(tol)
 $! exactify(e,tol)
$, approxfraction(e,tol=$#):
 t=tofl(tol)if tol is $- $# $& 5e-14
 $! lmap($; v:float2rat(tofl(evalf(v)),t)if $5(v)$& exactify(v,t),e)
$, left_(e,n=$#):
 if isrel(e):
  $! e[1]
 if $h(e):
  $!('$J',)+e[1:1+n]
 if isstr(e):
  $!('$p',e[1][:n])
 err("Argument error")
$, right_(e,n=$#):
 if isrel(e):
  $! e[2]
 if $h(e):
  $!('$J',)+(e[$/(e)-n:]if n $&())
 if isstr(e):
  $!('$p',e[1][$/(e[1])-n:]if n $& '')
 err("Argument error")
$, mid_(e,start,n=$#):
 if isstr(e):
  s=e[1][start-1:]
  $!('$p',s if n is $# $& s[:n])
 xs=$J(e[1:])[start-1:]
 $!('$J',)+$1(xs if n is $# $& xs[:n])
$, dim_(e):
 if $h(e):
  $! $/(e)-1
 if ismat(e):
  r,c=dims(e)
  $!('$J',r,c)
 if isstr(e):
  $! $/(e[1])
 err("Argument error")
$, max_(a,b=$#):
 if b is $#:
  xs=$J(a[1:])if $h(a)$&[a]
  $! maxexpr(xs)
 $! lmap2($; x,y:x if cmpv(x,y)>=0 $& y,a,b)
$, min_(a,b=$#):
 if b is $#:
  xs=$J(a[1:])if $h(a)$&[a]
  best=$#
  bv=$#
  $( x in xs:
   v=$Z(x)
   if best is $# or v<bv:
    best=x
    bv=v
  $! best
 $! lmap2($; x,y:x if cmpv(x,y)<=0 $& y,a,b)
$, cmpv(x,y):
 if $5(x)$* $5(y):
  d=$Z($_(x,y))
  d=d.$U if $0(d)is $4 $& d
  $! 1 if d>0 $&(-1 if d<0 $& 0)
 err("Cannot compare")
$, when_(c,a,b=$#,u=$#):
 if b=='$I':
  b=$#
 t=tobool(c)
 if t is $B:
  $! a
 if t is $2:
  $! b if b is $- $# $& '$I'
 if b is $#:
  $!('when',c,a)
 if u is $#:
  $!('when',c,a,b)
 $! u
$, piecewise_(*a):
 a=$J(a)
 if $/(a)<2:
  err('Wrong number of arguments')
 if $/(a)%2==1:
  r=a[-1]
  a=a[:-1]
 $&:
  r=$#
 $( i in $+($/(a)-2,-1,-2):
  r=when_(a[i+1],a[i],r)
 $! r
$, string_(e):
 if isstr(e):
  $! e
 $!('$p',fmt(e))
$, char_(n):
 $!('$p',chr(need_int(n)))
$, ord_(s):
 $! ord(s[1][0])
$, instring_(s,t,start=1):
 i=s[1].find(t[1],start-1)
 $! i+1
$, polyeval(L,x):
 r=0
 $( c in L[1:]:
  r=$`($<(r,x),c)
 $! $?(r)
$, randpoly(v,n):
 if $- $i(n)or n<0:
  err('Degree must be a nonnegative integer')
 if n>=MAXTERMS:
  toobig('a polynomial of degree %d has more than %d $Q'%(n,MAXTERMS))
 import random
 $! $>([$<(random.randint(-9,9),pw(v,k))$( k in $+(n+1)])
$, randmat(r,c):
 cells(r,c)
 import random
 $! mk([[random.randint(-9,9)$( _ in $+(c)]$( _ in $+(r)])
$, newmat(r,c):
 cells(r,c)
 $! mk([[0]*c $( _ in $+(r)])
$, newlist(n):
 if $- $i(n)or n<0:
  err('Length must be a nonnegative integer')
 if n>MAXLEN:
  toobig('a $J of %d elements is longer than %d'%(n,MAXLEN))
 $!('$J',)+(0,)*n
$, rand_(n=$#):
 import random
 if n is $#:
  $! random.random()
 $!('$J',)+$1(random.random()$( _ in $+(n))
$, randint_(a,b,n=$#):
 import random
 if n is $#:
  $! random.randint(a,b)
 $!('$J',)+$1(random.randint(a,b)$( _ in $+(n))
$, count_(*$L):
 n=0
 $( a in $L:
  n+=($/(a)-1)if $h(a)$& 1
 $! n
$, erf(x):
 if $H(x)<2.5:
  s=0.0
  t=x
  k=0
  $F $B:
   term=t/(2*k+1)
   s+=term
   k+=1
   t=-t*x*x/k
   if $H(term)<1e-17:
    $R
  $! 2/$M.$O($M.pi)*s
 z=$H(x)
 t=0.0
 $( k in $+(60,0,-1):
  t=(k/2.0)/(z+t)
 erfc=$M.exp(-z*z)/$M.$O($M.pi)/(z+t)
 $!(1-erfc)if x>0 $&(erfc-1)
$, numarg(v):
 if v=='$P':
  $! $C('$P')
 if v==('*',-1,'$P'):
  $! $C('-$P')
 if $5(v):
  x=cv(v)if $- $G(v)$& tofl(v)
  if x is $- $# $* $0(x)is $- $4:
   $! x
 err('Numeric argument required')
$, normcdf(lo,hi,mu=0.0,sig=1.0):
 mu=numarg(mu)
 sig=numarg(sig)
 $, F(v):
  if v=='$P':
   $! 1.0
  if v==('*',-1,'$P'):
   $! 0.0
  z=(numarg(v)-mu)/sig
  $! 0.5*(1+erf(z/$M.$O(2)))
 $! F(hi)-F(lo)
$, normpdf(x,mu=0.0,sig=1.0):
 x=numarg(x)
 s=numarg(sig)
 $! $M.exp(-0.5*((x-numarg(mu))/s)**2)/(s*$M.$O(2*$M.pi))
$, invnorm(p,mu=0.0,sig=1.0):
 p=numarg(p)
 mu=numarg(mu)
 sig=numarg(sig)
 if $- 0<p<1:
  err('Area must be between 0 $* 1')
 lo,hi=-40.0,40.0
 $( _ in $+(200):
  m=0.5*(lo+hi)
  if 0.5*(1+erf(m/$M.$O(2)))<p:
   lo=m
  $&:
   hi=m
 $! mu+sig*0.5*(lo+hi)
$, binompdf(n,p,x=$#):
 if x is $#:
  $!('$J',)+$1(binompdf(n,p,k)$( k in $+(n+1))
 if $w(p):
  $! $<(binom(n,x),pw(p,x),pw($_(1,p),n-x))
 p=tofl(p)
 $! binom(n,x)*p**x*(1-p)**(n-x)
$, binomcdf(n,p,a,b=$#):
 if b is $#:
  a,b=0,a
 $! $>([binompdf(n,p,k)$( k in $+($q(a),$q(b)+1)])
$, poisspdf(lam,x):
 $! evalf($<(pw(lam,x),pw('e',$m(lam)),Q(1,fact_int(x))))
$, poisscdf(lam,a,b=$#):
 if b is $#:
  a,b=0,a
 $! $>([poisspdf(lam,k)$( k in $+($q(a),$q(b)+1)])
''')
_x(r'''$, geompdf(p,x):
 $! $<(p,pw($_(1,p),x-1))
$, geomcdf(p,a,b=$#):
 if b is $#:
  a,b=1,a
 $! $>([geompdf(p,k)$( k in $+($q(a),$q(b)+1)])
$, fact_int(n):
 r=1
 $( k in $+(2,n+1):
  r*=k
 $! r
$, toang(x):
 a=SET['$l']
 if a=='deg':
  $! $<(x,$V('pi',180))
 if a=='grad':
  $! $<(x,$V('pi',200))
 $! x
$, fromang(x):
 a=SET['$l']
 if a=='deg':
  $! $?($<(x,$V(180,'pi')))
 if a=='grad':
  $! $?($<(x,$V(200,'pi')))
 $! x
TRIG=('sin','cos','tan','sec','csc','cot')
ITRIG=('$y','arccos','$s','arcsec','arccsc','arccot')
$, mathfn($A):
 $, f(*a):
  if $A in TRIG $* SET['$l']!='rad':
   $! lmap($; u:fn($A,toang(u)),a[0])
  if $A in ITRIG $* SET['$l']!='rad':
   $! lmap($; u:fromang(fn($A,u)),a[0])
  if $/(a)==1:
   $! lmap($; u:fn($A,u),a[0])
  $! fn($A,*a)
 $! f
$, angle_fn(z):
 $! lmap($; u:fromang(fn('$l',u)),z)
F={}
$( _n in('sin','cos','tan','sec','csc','cot','$y','arccos',
 '$s','arcsec','arccsc','arccot','sinh','cosh','tanh',
 'sech','csch','coth','arcsinh','arccosh','arctanh',
 'arcsech','arccsch','arccoth','ln','exp','$H','sign',
 'floor','ceiling','$U','imag','conj','fact'):
 F[_n]=mathfn(_n)
ALIAS={'asin':'$y','acos':'arccos','atan':'$s','asinh':'arcsinh',
 'acosh':'arccosh','atanh':'arctanh','ceil':'ceiling',
 'factorial':'fact','derivative':'d','$N':'$N',
 'int_':'$N','sumseq':'sumseq','prodseq':'prodseq',
 'lim':'$|','nderiv':'nderivative','polycoef':'polycoeffs',
 'stddevsamp':'stddev','varsamp':'variance','cumsum':'cumulativesum',
 'nsolve':'nsolve','arg':'$l','inv':'inverse','mat2list':'matlist',
 'list2mat':'listmat','explist':'explist','tran':'transpose',
 'log10':'log10','sqr':'$O','diff':'d','deriv':'d',
 'differentiate':'d','integrate':'$N','avg':'mean',
 'average':'mean'}
F['$O']=$; u:lmap($O,u)
F['root']=$; u,n=2:lmap($; v:fn('root',v,n),u)
F['cbrt']=$; u:lmap($; v:fn('root',v,3),u)
F['log']=$; u,b=$#:lmap($; v:fn('ln',v)if b is $# $& fn('log',v,b),u)
F['atan2']=$; y,x:lmap2($; b,a:fromang(fn('$l',$`(a,$<('i',b)))),y,x)
F['log10']=$; u:lmap($; v:fn('log',v,10),u)
F['$l']=angle_fn
F['round']=$; x,d=0:lmap($; v:round_(v,d),x)
F['ipart']=$; x:lmap(ipart_,x)
F['$q']=$; x:lmap($; v:fn('floor',v),x)
F['fpart']=$; x:lmap(fpart_,x)
F['gcd']=$; a,b:lmap2(gcd_,a,b)
F['lcm']=$; a,b:lmap2(lcm_,a,b)
F['mod']=$; a,b:lmap2(mod_,a,b)
F['remain']=$; a,b:lmap2(remain_,a,b)
F['intdiv']=$; a,b:lmap2(intdiv_,a,b)
F['ncr']=$; a,b:lmap2(ncr_,a,b)
F['npr']=$; a,b:lmap2(npr_,a,b)
F['isprime']=isprime_
F['approx']=approx_
F['exact']=exact_
F['approxrational']=approxfraction
F['getnum']=$; e:lmap(getnum,e)
F['getdenom']=$; e:lmap(getden,e)
F['polyeval']=polyeval
F['polygcd']=$; a,b:poly_gcd_expr(a,b)
F['randpoly']=randpoly
F['texpand']=$; e:lmap($; v:texpand(v),e)
F['tcollect']=$; e:lmap($; v:tcollect(v),e)
F['left']=left_
F['right']=right_
F['mid']=mid_
F['dim']=dim_
F['max']=max_
F['min']=min_
F['when']=when_
F['piecewise']=piecewise_
F['string']=string_
F['char']=char_
F['ord']=ord_
F['instring']=instring_
F['det']=det
F['identity']=ident
F['transpose']=transpose
F['rref']=$; A,tol=$#:rref(A,$B)
F['ref']=$; A,tol=$#:ref_(A)
F['inverse']=m_inv
F['rowdim']=$; A:dims(A)[0]
F['coldim']=$; A:dims(A)[1]
F['rownorm']=rownorm
F['colnorm']=colnorm
F['norm']=norm
F['trace']=trace
F['diag']=diag
F['augment']=augment
F['colaugment']=colaugment
F['submat']=submat
F['rowswap']=rowswap
F['rowadd']=rowadd
F['mrow']=mrow
F['mrowadd']=mrowadd
F['crossp']=crossp
F['dotp']=dotp
F['unitv']=unitv
F['eigvl']=eigvl
F['eigvc']=eigvc
F['lu']=$; A,tol=$#:('$J',)+lu(A)
F['qr']=$; A,tol=$#:('$J',)+qr(A)
F['newmat']=newmat
F['newlist']=newlist
F['randmat']=randmat
F['matlist']=matlist
F['listmat']=listmat
F['simult']=simult
F['cumulativesum']=cumsum
F['sum']=$; L,a=1,b=$#:lsum(L,a,b)if $h(L)$& colwise(L,lsum)
F['product']=$; L,a=1,b=$#:lprod(L,a,b)if $h(L)$& colwise(L,lprod)
F['mean']=$; L,f=$#:mean(L,f)if $h(L)$& colwise(L,mean)
F['median']=median
F['stddev']=$; L:stddev(L)
F['stddevpop']=$; L:stddev(L,$B)
F['variance']=$; L:variance(L)
F['varpop']=$; L:variance(L,$B)
F['sorta']=sorta
F['sortd']=sortd
F['deltalist']=deltalist
F['count']=count_
F['rand']=rand_
F['randint']=randint_
F['normcdf']=normcdf
F['normpdf']=normpdf
F['invnorm']=invnorm
F['binompdf']=binompdf
F['binomcdf']=binomcdf
F['poisspdf']=poisspdf
F['poisscdf']=poisscdf
F['geompdf']=geompdf
F['geomcdf']=geomcdf
F['getmode']=$;*a:('$p','$l='+SET['$l']+' mode='+SET['mode']+' $D='+SET['$D'])
$, colwise(M,f):
 cols=$X(transpose(M))
 $! mk([[f(('$J',)+$1(c))$( c in cols]])
$, ref_(A):
 $! rref(A,$2)
$, conv(e,$A,$L):
 if $A=='decimal':
  $! evalf(e)
 if $A=='approxfraction':
  $! approxfraction(e,$L[0]if $L $& $#)
 if $A in('dms','dd','rad','grad','deg'):
  $! angconv(e,$A)
 if $A=='polar':
  if $h(e)or ismat(e):
   $! polar_vec(e)
  r=$.(fn('$H',e))
  th=fn('$l',e)
  $!('$p','('+fmt(r)+'\u2220'+fmt(fromang(th))+')')
 if $A=='rect':
  if $h(e)or ismat(e):
   $! e
  r,i=reim(e)
  $! $`(r,$<('i',i))
 if $A=='cylind':
  $! cylind(e)
 if $A=='sphere':
  $! sphere(e)
 if $A in('base2','base10','base16'):
  $! baseconv(e,$A)
 if $A=='exp':
  $! toexp(e)
 if $A=='ln':
  $! toln(e)
 if $A=='logbase':
  $! tologbase(e,$L[0])
 if $A=='sin':
  $! pyth_to(e,'sin')
 if $A=='cos':
  $! pyth_to(e,'cos')
 err("Unknown conversion "+$A)
''')
_x(r'''$, angconv(e,$A):
 if $A=='dms':
  v=tofl(evalf(e))
  if SET['$l']=='rad':
   v=v*180/$M.pi
  $= SET['$l']=='grad':
   v=v*0.9
  sg='-' if v<0 $& ''
  v=$H(v)
  d=$q(v)
  m=$q((v-d)*60)
  s=((v-d)*60-m)*60
  if s>59.9999995:
   s=0.0
   m+=1
  if m==60:
   m=0
   d+=1
  ss=('%.4f'%s).rstrip('0').rstrip('.')
  $!('$p',sg+$p(d)+'\u00b0'+$p(m)+"'"+ss+'"')
 if $A=='dd':
  if SET['$l']=='rad':
   $! evalf($<(e,$V(180,'pi')))
  $! evalf(e)
 if $A=='rad':
  if SET['$l']=='deg':
   $! $<(e,$V('pi',180))
  if SET['$l']=='grad':
   $! $<(e,$V('pi',200))
  $! e
 if $A=='grad':
  if SET['$l']=='deg':
   $! $<(e,Q(10,9))
  if SET['$l']=='rad':
   $! $<(e,$V(200,'pi'))
  $! e
 if SET['$l']=='rad':
  $! $<(e,$V(180,'pi'))
 $! e
$, baseconv(e,$A):
 n=need_int(e)
 if $A=='base10':
  $! n
 if $A=='base2':
  s=bin(n)if n>=0 $& '-'+bin(-n)
  $!('$p',s.replace('0b','0b'))
 s=hex(n)if n>=0 $& '-'+hex(-n)
 $!('$p',s.replace('0x','0h').upper().replace('0H','0h'))
$, toexp(e):
 if $0(e)is $- $1 or e[0]=='Q':
  $! e
 $L=[toexp(a)$( a in e[1:]]
 h=e[0]
 if $/($L)==1:
  u=$L[0]
  if h=='sinh':
   $! $<($x,$_(pw('e',u),pw('e',$m(u))))
  if h=='cosh':
   $! $<($x,$`(pw('e',u),pw('e',$m(u))))
  if h=='tanh':
   $! $V($_(pw('e',u),pw('e',$m(u))),$`(pw('e',u),pw('e',$m(u))))
  if h=='sin':
   iu=$<('i',u)
   $! $V($_(pw('e',iu),pw('e',$m(iu))),$<(2,'i'))
  if h=='cos':
   iu=$<('i',u)
   $! $<($x,$`(pw('e',iu),pw('e',$m(iu))))
  if h=='arcsinh':
   $! fn('ln',$`(u,$O($`(pw(u,2),1))))
  if h=='arccosh':
   $! fn('ln',$`(u,$O($_(pw(u,2),1))))
  if h=='arctanh':
   $! $<($x,fn('ln',$V($`(1,u),$_(1,u))))
 $! simp((h,)+$1($L))
$, toln(e):
 if $0(e)is $- $1 or e[0]=='Q':
  $! e
 $L=[toln(a)$( a in e[1:]]
 if e[0]=='log':
  b=$L[1]if $/($L)>1 $& 10
  $! $V(fn('ln',$L[0]),fn('ln',b))
 $! simp((e[0],)+$1($L))
$, tologbase(e,b):
 e=toln(e)
 $, walk(t):
  if $0(t)is $- $1 or t[0]=='Q':
   $! t
  if t[0]=='ln':
   $! $V(('log',walk(t[1]),b),('log','e',b))
  $!(t[0],)+$1(walk(a)$( a in t[1:])
 $!('hold',walk(e))
''')
_x(r'''VERSION='1.3'
ENV={}
UFUN={}
ASSUME=[]
STATE={'ans':0,'$D':$2,'tmpf':[]}
COMPLEXF=('csolve','czeros','cfactor','cpolyroots','eigvl','eigvc','conj',
 '$U','imag','$l')
$, isfunc(n):
 $!(n in F or n in SF or n in UFUN or n in ALIAS
 or n in STATE['tmpf']or n in('expr','$O','log','root'))
$, lookup(n):
 if n in ENV:
  $! ENV[n]
 if n=='ans':
  $! STATE['ans']
 if n=='i':
  STATE['$D']=$B
 $! n
$, ev(t):
 tt=$0(t)
 if tt is $q or tt is $C:
  $! t
 if tt is $p:
  $! lookup(t)
 h=t[0]
 if h=='+':
  a=ev(t[1])
  b=ev(t[2])
  $! vadd(a,b)
 if h=='-':
  $! vsub(ev(t[1]),ev(t[2]))
 if h=='$m':
  $! vneg(ev(t[1]))
 if h=='*':
  $! vmul(ev(t[1]),ev(t[2]))
 if h=='/':
  $! vdiv(ev(t[1]),ev(t[2]))
 if h=='^':
  $! vpow(ev(t[1]),ev(t[2]))
 if h in('.*','./','.^'):
  $! dotop(h,ev(t[1]),ev(t[2]))
 if h=='!':
  $! lmap($; a:fn('fact',a),ev(t[1]))
 if h=='%':
  $! lmap($; a:$V(a,100),ev(t[1]))
 if h=='deg':
  v=ev(t[1])
  if SET['$l']=='rad':
   $! lmap($; a:$<(a,$V('pi',180)),v)
  if SET['$l']=='grad':
   $! lmap($; a:$<(a,Q(10,9)),v)
  $! v
 if h in('=','<','>','<=','>=','/='):
  $! rel(h,ev(t[1]),ev(t[2]))
 if h=='$*':
  $! land(ev(t[1]),ev(t[2]))
 if h=='or':
  $! lor(ev(t[1]),ev(t[2]))
 if h=='$-':
  $! lnot(ev(t[1]))
 if h=='xor':
  $! lxor(ev(t[1]),ev(t[2]))
 if h=='nor':
  $! lnot(lor(ev(t[1]),ev(t[2])))
 if h=='nand':
  $! lnot(land(ev(t[1]),ev(t[2])))
 if h=='=>':
  $! lor(lnot(ev(t[1])),ev(t[2]))
 if h=='<=>':
  $! lnot(lxor(ev(t[1]),ev(t[2])))
 if h=='|':
  $! ev_with(t)
 if h=='store':
  $! ev_store(t[1],t[2])
 if h=='define':
  $! ev_define(t[1],t[2])
 if h=='call':
  $! call(t[1],t[2:])
 if h=='$J':
  $!('$J',)+$1(ev(a)$( a in t[1:])
 if h=='mat':
  $!('mat',)+$1(('$J',)+$1(ev(a)$( a in r[1:])$( r in t[1:])
 if h=='$p':
  $! t
 if h=='&':
  a=ev(t[1])
  b=ev(t[2])
  $!('$p',string_(a)[1]+string_(b)[1])
 if h=='index':
  $! ev_index(ev(t[1]),[ev(a)$( a in t[2:]])
 if h=='prime':
  $! t[1]+"'"*t[2]
 if h=='primecall':
  $!('call',t[1]+"'"*t[2])+$1(ev(a)$( a in t[3:])
 if h=='polar':
  STATE['$D']=$B
  $! $<(ev(t[1]),pw('e',$<('i',toang(ev(t[2])))))
 if h=='conv':
  $! ev_conv(t)
 err('Syntax error')
$, evw(raw,names):
 saved={}
 $( n in names:
  if n in ENV:
   saved[n]=ENV.pop(n)
 ${:
  $! ev(raw)
 finally:
  $( n in saved:
   ENV[n]=saved[n]
$, split_and(c):
 if $)(c,'$*'):
  $! split_and(c[1])+split_and(c[2])
 $![c]
$, ev_with(t):
 conds=split_and(t[2])
 pairs={}
 ineq=[]
 $( c in conds:
  if $)(c,'=')$* $0(c[1])is $p:
   pairs[c[1]]=ev(c[2])
  $&:
   v=evw(c,$J(pairs.keys()))
   if $)(v,'$*'):
    ineq.$}($J(v[1:]))
   $= v!='true':
    ineq.$%(v)
 n0=$/(ASSUME)
 ASSUME.$}(ineq)
 ${:
  r=evw(t[1],$J(pairs.keys()))
 finally:
  del ASSUME[n0:]
 if pairs:
  r=subsd(unhold(r),pairs)
  if head(r)in('=','<','>','<=','>=','/='):
   r=rel(head(r),r[1],r[2])
 $( c in ineq:
  r=assume_sign(r,c)
 $! r
$, assume_sign(r,c):
 h=head(c)
 if h $- in('<','>','<=','>='):
  $! r
 a,b=c[1],c[2]
 if $0(a)is $p $* b==0:
  v=a
  pos=h in('>','>=')
 $= $0(b)is $p $* a==0:
  v=b
  pos=h in('<','<=')
 $&:
  $! r
 rep=v if pos $& $m(v)
 r=$Y(r,('$H',v),rep)
 r=$Y(r,('sign',v),1 if pos $&-1)
 $! r
$, target_fn(t):
 if $)(t,'call'):
  $! t[1],[p $( p in t[2:]]
 if $)(t,'*')$* $0(t[1])is $p:
  p=t[2]
  $! t[1],[p]
 $! $#
$, ev_store(raw,tgt):
 tf=target_fn(tgt)
 if tf is $- $#:
  $! ev_define(tgt,raw)
 if $0(tgt)is $- $p:
  err('Invalid variable $A')
 if tgt in SPECIAL or tgt in F or tgt in SF:
  err('Reserved $A')
 v=ev(raw)
 ENV[tgt]=unhold(v)if $- $)(v,'$p')$& v
 $! v
$, ev_define(lhs,rhs):
 tf=target_fn(lhs)
 if tf is $#:
  if $0(lhs)is $p:
   $! ev_store(rhs,lhs)
  err('Invalid definition')
 $A,params=tf
 $( p in params:
  if $0(p)is $- $p:
   err('Invalid parameter')
 body=unhold(evw(rhs,params))
 UFUN[$A]=(params,body)
 if $A in STATE['tmpf']:
  STATE['tmpf'].remove($A)
 $!('$p','Done')
$, ev_index(a,idx):
 if $- idx:
  err('Invalid index')
 if $)(a,'$J'):
  i=idx[0]
  if $- $i(i)or i<1 or i>=$/(a):
   err('Invalid index')
  $! a[i]
 if $)(a,'mat'):
  $( k in idx:
   if $- $i(k)or k<1:
    err('Invalid index')
  if $/(idx)==1:
   if $/(a)==2:
    if idx[0]>=$/(a[1]):
     err('Invalid index')
    $! a[1][idx[0]]
   if idx[0]>=$/(a):
    err('Invalid index')
   $!('mat',a[idx[0]])
  if idx[0]>=$/(a)or idx[1]>=$/(a[idx[0]]):
   err('Invalid index')
  $! a[idx[0]][idx[1]]
 if $)(a,'$p'):
  k=idx[0]
  if $/(idx)!=1 or $- $i(k)or k<1 or k>$/(a[1]):
   err('Invalid index')
  $!('$p',a[1][k-1])
 err('Invalid index')
$, ev_conv(t):
 e=t[1]
 $A=t[2]
 $L=[ev(a)$( a in t[3:]]
 if $A=='$J':
  if e=='exp':
   $! explist($L[0],$L[1])
  if e=='mat':
   $! matlist($L[0])
  err('Unknown conversion')
 if $A=='mat' $* e=='$J':
  $! listmat(*$L)
 v=ev(e)
 v=finalize(v,$B)
 $! builtin($A,conv,(v,$A,$L))
$, explist(e,v):
 $9=[]
 parts=e[1:]if $)(e,'or')$&(e,)
 $( p in parts:
  if $)(p,'=')$* p[1]==v:
   $9.$%(p[2])
 $!('$J',)+$1($9)
''')
_x(r'''$, call($A,raw):
 $A=ALIAS.get($A,$A)
 if $A=='approx' $* $/(raw)==1:
  v=fastnum(raw[0])
  if v is $- $#:
   $! v
 if $A in UFUN:
  params,body=UFUN[$A]
  $L=[ev(a)$( a in raw]
  if $/($L)!=$/(params):
   err('Wrong number of arguments')
  $! subsd(body,dict(zip(params,$L)))
 f=SF.get($A)
 if f is $- $#:
  if $A in COMPLEXF:
   STATE['$D']=$B
  $! builtin($A,f,(raw,))
 f=F.get($A)
 if f is $- $#:
  $L=[ev(a)$( a in raw]
  if $A in COMPLEXF:
   STATE['$D']=$B
  $! builtin($A,f,$L)
 if $A=='expr':
  s=ev(raw[0])
  $! ev(parse(s[1],isfunc))
 $L=[ev(a)$( a in raw]
 $!('call',$A)+$1($L)
class NoNum($6):
 pass
cs_NUMF={'sin':$M.sin,'cos':$M.cos,'tan':$M.tan,'$y':$M.asin,
 'arccos':$M.acos,'$s':$M.atan,'ln':$M.log,'log':$M.log,
 'log10':$M.log10,'$O':$M.$O,'exp':$M.exp,'$H':$H,
 'sinh':$M.sinh,'cosh':$M.cosh,'tanh':$M.tanh}
TRIGF=('sin','cos','tan')
ATRIGF=('$y','arccos','$s')
NUMST={'big':0.0,'cost':0.0}
$, lfact(n):
 $! $M.lgamma(n+1.0)
$, fastnum(t):
 NUMST['big']=0.0
 NUMST['cost']=0.0
 ${:
  v=numev(t)
 $3(NoNum,$T,$^,$E,TypeError):
  $! $#
 if NUMST['cost']<2000 or v!=v:
  $! $#
 if v!=0 $* $H(v)!=$C('$P')$* $H(v)<1e-8*NUMST['big']:
  $! $#
 if v==0 $* NUMST['big']>0:
  $! $#
 $! v
$, numev(t):
 tt=$0(t)
 if tt is $q:
  $! $C(t)
 if tt is $C:
  $! t
 if tt is $p:
  if t=='pi':
   $! $M.pi
  if t=='e':
   $! $M.e
  v=ENV.get(t)
  if $0(v)in($q,$C)or isq(v):
   $! tofl(v)
  $d NoNum()
 h=t[0]
 if h in('+','-'):
  a=numev(t[1])
  b=numev(t[2])
  NUMST['big']=max(NUMST['big'],$H(a),$H(b))
  $! a+b if h=='+' $& a-b
 if h=='*':
  $! numev(t[1])*numev(t[2])
 if h=='/':
  $! numev(t[1])/numev(t[2])
 if h=='$m':
  $!-numev(t[1])
 if h=='^':
  b=numev(t[1])
  x=numev(t[2])
  if b<0 $* x!=$q(x):
   $d NoNum()
  if $H(b)>1:
   NUMST['cost']+=$H(x)*$M.log($H(b),2)
  $! b**x if $H(x*$M.log($H(b)or 1.0))<709 $&($C('$P')if b>0 or x%2==0 $&-$C('$P'))
 if h=='!':
  n=numev(t[1])
  if n<0 or n!=$q(n):
   $d NoNum()
  lf=lfact(n)
  NUMST['cost']+=lf/$M.log(2)
  $! $M.exp(lf)if lf<709 $& $C('$P')
 if h=='call':
  $A=ALIAS.get(t[1],t[1])
  $L=[numev(a)$( a in t[2:]]
  if $A in('ncr','npr')$* $/($L)==2:
   n,k=$L
   if n!=$q(n)or k!=$q(k)or k<0 or k>n:
    $d NoNum()
   lv=lfact(n)-lfact(n-k)-(lfact(k)if $A=='ncr' $& 0)
   NUMST['cost']+=lv/$M.log(2)
   $! $C(round($M.exp(lv)))if lv<36 $&($M.exp(lv)if lv<709 $& $C('$P'))
  f=cs_NUMF.get($A)
  if f is $# or $/($L)!=1:
   $d NoNum()
  x=$L[0]
  if $A in TRIGF $* SET['$l']!='rad':
   x=x*($M.pi/180 if SET['$l']=='deg' $& $M.pi/200)
  r=f(x)
  if $A in ATRIGF $* SET['$l']!='rad':
   r=r*(180/$M.pi if SET['$l']=='deg' $& 200/$M.pi)
  $! r
 $d NoNum()
$, builtin($A,f,$L):
 ${:
  $! f(*$L)
 $3 $S as ex:
  if $p(ex).$~('Wrong number of arguments'):
   argerr($A)
  $d
 $3 TypeError as ex:
  msg=$p(ex)
  if 'positional' in msg or 'takes' in msg or 'required' in msg or 'missing' in msg:
   argerr($A)
  err('Invalid argument $( '+$A)
 $3(IndexError,$T,AttributeError,KeyError):
  err('Invalid argument $( '+$A)
 $3 $^:
  err('Number too large in '+$A)
$, tinames():
 c=STATE.get('tinames')
 if c is $#:
  _load('cashelp')
  c={}
  $( key,title,words in CATS:
   $( wd in words.split():
    if wd[0].isalpha():
     c[wd.lower()]=wd
  STATE['tinames']=c
 $! c
$, argerr($A):
 _load('cashelp')
 n=tinames().get($A,$A)
 sy=SYN.get($A)
 err('Wrong number of arguments $( '+n+('\n'+sy.split('\n')[0]if sy $& ''))
$, suggest($A):
 if $/($A)<4:
  $! $#
 best=$#
 $( k in tinames():
  if $H($/(k)-$/($A))>1:
   $7
  if close(k,$A.lower()):
   best=tinames()[k]
   $R
 $! best
$, close(a,b):
 if a==b:
  $! $2
 if $/(a)==$/(b):
  d=[i $( i in $+($/(a))if a[i]!=b[i]]
  if $/(d)==2 $* d[1]==d[0]+1 $* a[d[0]]==b[d[1]]$* a[d[1]]==b[d[0]]:
   $! $B
  $! $/(d)==1
 if $/(a)>$/(b):
  a,b=b,a
 $( i in $+($/(b)):
  if b[:i]+b[i+1:]==a:
   $! $B
 $! $2
$, unknown_calls(e,$9):
 if $0(e)is $- $1 or $- e or e[0]=='Q':
  $!
 if e[0]=='call' $* e[1]$- in UFUN $* e[1]$- in STATE['tmpf']$* e[1]$- in $9:
  $9.$%(e[1])
 $( a in e[1:]:
  unknown_calls(a,$9)
$, var_of(raw):
 if $0(raw)is $p:
  $! raw,$#
 if $)(raw,'='):
  if $0(raw[1])is $- $p:
   err('Variable expected')
  $! raw[1],ev(raw[2])
 err('Variable expected')
$, nargs(a,lo,hi):
 if $/(a)<lo or $/(a)>hi:
  err('Wrong number of arguments')
$, $n(a,k=1):
 v,val=var_of(a[k])
 e=unhold(evw(a[0],[v]))
 $! e,v,val
$, post_subst(r,v,val):
 if val is $- $#:
  $! $Y(r,v,val)
 if v in ENV:
  $! $Y(r,v,ENV[v])
 $! r
$, sf_d(a):
 nargs(a,2,3)
 e,v,val=$n(a)
 n=ev(a[2])if $/(a)>2 $& 1
 if $- $i(n):
  err('Order must be an integer')
 r=lmap($; u:nice(diff(u,v,n)),e)
 $! post_subst(r,v,val)
$, sf_int(a):
 nargs(a,2,4)
 e,v,val=$n(a)
 if $/(a)==2:
  $! lmap($; u:nice(integrate(u,v)),e)
 if $/(a)==3:
  c=ev(a[2])
  $! lmap($; u:$`(nice(integrate(u,v)),c),e)
 lo=ev(a[2])
 hi=ev(a[3])
 $! lmap($; u:nice(defint(u,v,lo,hi)),e)
$, sf_limit(a):
 nargs(a,3,4)
 e,v,val=$n(a)
 pt=ev(a[2])
 dirn=0
 if $/(a)>3:
  d=ev(a[3])
  if $- $G(d):
   err('Direction must be -1, 0 or 1')
  dirn=0 if d==0 $&(1 if $c(d)>0 $&-1)
 $, L(u):
  r=$|(u,v,pt,dirn)
  if $)(r,'$|'):
   $!('$|',u,v,pt)if dirn==0 $&('$|',u,v,pt,dirn)
  $! nice(r)
 $! lmap(L,e)
''')
_x(r'''$, cs_bounds(a,i):
 $! ev(a[i]),ev(a[i+1])
$, sf_sum(a):
 nargs(a,4,4)
 e,v,val=$n(a)
 lo,hi=cs_bounds(a,2)
 r=sumseq(e,v,lo,hi)
 $! prefer_fact(nice(r))
$, prefer_fact(r):
 if $)(r,'+')$* $- $b(r)$* $/($e(r))==1:
  ${:
   f=factor_expr(r)
   if $)(f,'hold')$* $)(f[1],'*'):
    $! f
  $3 $6:
   pass
 $! r
$, sf_prod(a):
 nargs(a,4,4)
 e,v,val=$n(a)
 lo,hi=cs_bounds(a,2)
 $! prodseq(e,v,lo,hi)
$, sf_seq(a):
 nargs(a,4,5)
 e,v,val=$n(a)
 lo,hi=cs_bounds(a,2)
 st=ev(a[4])if $/(a)>4 $& 1
 $9=[]
 k=lo
 cnt=0
 $F ncmp(k,hi)<=0 if $G(k)$& $2:
  $9.$%($Y(e,v,k))
  k=nadd(k,st)
  cnt+=1
  if cnt>MAXLEN:
   toobig('seq would make more than %d elements'%MAXLEN)
 $!('$J',)+$1($9)
$, sf_taylor(a):
 nargs(a,3,4)
 e,v,val=$n(a)
 n=ev(a[2])
 pt=ev(a[3])if $/(a)>3 $& 0
 $! lmap($; u:taylor(u,v,n,pt),e)
$, sf_series(a):
 nargs(a,3,4)
 e,v,val=$n(a)
 n=ev(a[2])
 pt=ev(a[3])if $/(a)>3 $& 0
 $! lmap($; u:series_cmd(u,v,n,pt),e)
$, sf_dominant(a):
 nargs(a,2,3)
 e,v,val=$n(a)
 pt=ev(a[2])if $/(a)>2 $& 0
 $! lmap($; u:dominant(u,v,pt),e)
$, solvevars(rawvs):
 vs=[]
 gs=[]
 $( r in rawvs:
  if $)(r,'$J'):
   $( q in r[1:]:
    v,g=var_of(q)
    vs.$%(v)
    gs.$%(g)
  $&:
   v,g=var_of(r)
   vs.$%(v)
   gs.$%(g)
 $! vs,gs
$, eqlist(e):
 if $)(e,'$*'):
  $9=[]
  $( p in e[1:]:
   $9.$}(eqlist(p))
  $! $9
 if $)(e,'$J'):
  $! $J(e[1:])
 $![e]
$, cons_for(v):
 $9=[]
 $( c in ASSUME:
  if has(c,v):
   $9.$%(c)
 $! $9
$, sf_solve(a,$D=$2):
 if $/(a)<2:
  err('Wrong number of arguments')
 vs,gs=solvevars(a[1:])
 e=evw(a[0],vs)
 eqs=eqlist(e)
 if $/(vs)==1 $* $/(eqs)==1:
  v=vs[0]
  eq=eqs[0]
  if gs[0]is $- $#:
   f=$_(eq[1],eq[2])if $)(eq,'=')$& eq
   r=nsolve(f,v,tofl(evalf(gs[0])))
   $!('=',v,r)if r is $- $# $& 'false'
  r=solve(eq,v,$D,cons_for(v))
  if r is $#:
   f=$_(eq[1],eq[2])if $)(eq,'=')$& eq
   ns=numeric_solve(f,v,$D)if head(eq)=='=' or head(eq)is $# $& $#
   if ns:
    r=sols_to_bool(v,apply_constraints(ns,v,cons_for(v)))
   $&:
    $!('solve',eq,v)
  $! finish_sol(r)
 if $/(eqs)>1 $* any([head(q)in('<','>','<=','>=','/=')$( q in eqs]):
  if $/(vs)>1:
   $!('solve',e)+$1(vs)
  $! finish_sol(solve_and(eqs,vs[0],$D))
 $j=solve_system(eqs,vs,$D,gs if any([g is $- $# $( g in gs])$& $#)
 if $j is $#:
  $!('solve',e)+$1(vs)
 if $- $j:
  $! 'false'
 $9=[]
 $( s in $j:
  conj=[('=',v,clean(s.get(v,v)))$( v in vs]
  $9.$%(conj[0]if $/(conj)==1 $&('$*',)+$1(conj))
 $! finish_sol($9[0]if $/($9)==1 $&('or',)+$1($9))
$, solve_and(eqs,v,$D):
 cons=cons_for(v)
 $( i in $+($/(eqs)):
  if head(eqs[i])=='=':
   $a=eqs[:i]+eqs[i+1:]
   r=solve(eqs[i],v,$D,$a+cons)
   if r is $#:
    $!('solve',('$*',)+$1(eqs),v)
   $! r
 ps=rel_pairs(eqs+cons,v)
 r=solve_rels(ps,v)if ps is $- $# $& $#
 if r is $#:
  $!('solve',('$*',)+$1(eqs),v)
 $! r
$, finish_sol(r):
 ns=[]
 $, walk(e):
  if $0(e)is $p $* e[0]=='n' $* e[1:].isdigit()$* e $- in ns:
   ns.$%(e)
  $= $0(e)is $1 $* e $* e[0]!='Q':
   $( a in e[1:]:
    walk(a)
 walk(r)
 if $- ns or ns==['n%d'%(i+1)$( i in $+($/(ns))]:
  $! r
 tmp=dict([(ns[i],'N%d_'%i)$( i in $+($/(ns))])
 r=subsd(r,tmp)
 $! subsd(r,dict([('N%d_'%i,'n%d'%(i+1))$( i in $+($/(ns))]))
$, sf_csolve(a):
 $! sf_solve(a,$B)
$, sf_zeros(a,$D=$2):
 nargs(a,2,2)
 vs,gs=solvevars(a[1:])
 e=evw(a[0],vs)
 if $/(vs)==1 $* $- $)(e,'$J'):
  r=zeros(e,vs[0],$D,cons_for(vs[0]))
  if r is $#:
   ns=numeric_solve(e,vs[0],$D)
   $!('$J',)+$1(ns or[])
  $! r
 eqs=eqlist(e)
 $j=solve_system(eqs,vs,$D)
 if $- $j:
  $!('$J',)
 $! mk([[clean(s.get(v,v))$( v in vs]$( s in $j])
$, sf_czeros(a):
 $! sf_zeros(a,$B)
$, sf_nsolve(a):
 nargs(a,2,4)
 v,g=var_of(a[1])
 e=unhold(evw(a[0],[v]))
 f=$_(e[1],e[2])if $)(e,'=')$& e
 lo=tofl(evalf(ev(a[2])))if $/(a)>2 $& $#
 hi=tofl(evalf(ev(a[3])))if $/(a)>3 $& $#
 $( c in cons_for(v):
  b=bounds([c],v)if $2 $& $#
 cb=bounds(cons_for(v),v)
 if cb is $- $#:
  lo,hi=tofl(evalf(cb[0])),tofl(evalf(cb[1]))
 r=nsolve(f,v,tofl(evalf(g))if g is $- $# $& $#,lo,hi)
 if r is $#:
  $!('$p','No solution found')
 $! r
$, sf_desolve(a):
 nargs(a,3,3)
 x=a[1]
 y=a[2]
 if $0(x)is $- $p or $0(y)is $- $p:
  err('Variable expected')
 parts=split_and(a[0])
 ode=$#
 conds=[]
 $( p in parts:
  if $)(p,'=')$* $)(p[1],'primecall')$* p[1][1]==y:
   conds.$%((p[1][2],evw(p[1][3],[x,y]),evw(p[2],[x,y])))
  $= $)(p,'=')$* $)(p[1],'*')$* p[1][1]==y $* $- hasprime(p):
   conds.$%((0,ev(p[1][2]),ev(p[2])))
  $= $)(p,'=')$* $)(p[1],'call')$* p[1][1]==y:
   conds.$%((0,ev(p[1][2]),ev(p[2])))
  $&:
   ode=p
 if ode is $#:
  err('ODE expected')
 o=evw(ode,[x,y,y+"'",y+"''"])
 o=$Y($Y(o,y+"''",YP[1]),y+"'",YP[0])
 r=desolve(o,x,y,conds)
 if r is $#:
  $!('desolve',o,x,y)
 $! r
$, hasprime(t):
 if $0(t)is $- $1:
  $! $2
 if t[0]in('prime','primecall'):
  $! $B
 $( a in t[1:]:
  if hasprime(a):
   $! $B
 $! $2
$, bnd_args(a,i,v):
 lo=ev(a[i])if $/(a)>i $& $#
 hi=ev(a[i+1])if $/(a)>i+1 $& $#
 cb=bounds(cons_for(v),v)
 if cb is $- $#:
  lo,hi=cb
 $&:
  $( c in cons_for(v):
   h=head(c)
   if h in('>','>=')$* c[1]==v:
    lo=c[2]
   $= h in('<','<=')$* c[1]==v:
    hi=c[2]
 $! lo,hi
$, sf_fmin(a,kind='min'):
 nargs(a,2,4)
 e,v,val=$n(a)
 lo,hi=bnd_args(a,2,v)
 r=fextreme(e,v,kind,lo,hi)
 if r is $#:
  $!('f'+kind,e,v)
 $! r
$, sf_fmax(a):
 $! sf_fmin(a,'max')
''')
_x(r'''$, sf_nfmin(a,kind='min'):
 nargs(a,2,4)
 e,v,val=$n(a)
 lo,hi=bnd_args(a,2,v)
 $! nfextreme(e,v,kind,tofl(evalf(lo))if lo is $- $# $& $#,
 tofl(evalf(hi))if hi is $- $# $& $#)
$, sf_nfmax(a):
 $! sf_nfmin(a,'max')
$, sf_nint(a):
 nargs(a,4,4)
 e,v,val=$n(a)
 lo,hi=cs_bounds(a,2)
 $! nint_split(e,v,lo,hi)
$, sf_arclen(a):
 nargs(a,4,4)
 e,v,val=$n(a)
 lo,hi=cs_bounds(a,2)
 $! nice(arclen(e,v,lo,hi))
$, pt_arg(a):
 if $/(a)==2 $* $)(a[1],'='):
  v,p=var_of(a[1])
  e=evw(a[0],[v])
  $! e,v,p
 nargs(a,3,3)
 v,_=var_of(a[1])
 e=unhold(evw(a[0],[v]))
 $! e,v,ev(a[2])
$, sf_tangent(a):
 e,v,p=pt_arg(a)
 $! tangentline(e,v,p)
$, sf_normal(a):
 e,v,p=pt_arg(a)
 $! normalline(e,v,p)
$, sf_impdif(a):
 nargs(a,3,4)
 x,_=var_of(a[1])
 y,_=var_of(a[2])
 e=evw(a[0],[x,y])
 n=ev(a[3])if $/(a)>3 $& 1
 $! impdif(e,x,y,n)
$, rc_args(a):
 v,val=var_of(a[1])
 e=unhold(evw(a[0],[v]))
 h=ev(a[2])if $/(a)>2 $& 0.001
 if val is $#:
  val=v
 $! e,v,val,h
$, sf_avgrc(a):
 nargs(a,2,3)
 e,v,val,h=rc_args(a)
 $! lmap($; u:$?(avgrc(u,v,val,h)),e)
$, sf_central(a):
 nargs(a,2,3)
 e,v,val,h=rc_args(a)
 $! lmap($; u:$?(centraldiff(u,v,val,h)),e)
$, sf_nderiv(a):
 nargs(a,2,3)
 v,val=var_of(a[1])
 e=unhold(evw(a[0],[v]))
 n=ev(a[2])if $/(a)>2 $& 1
 if val is $#:
  val=ENV.get(v)
  if val is $#:
   err('Value required: var=value')
 $! evalf($Y(diff(e,v,n),v,val))
$, opt_var(a,i):
 if $/(a)>i:
  v,_=var_of(a[i])
  $! v
 $! $#
$, sf_expand(a):
 nargs(a,1,2)
 v=opt_var(a,1)
 e=ev(a[0])
 $! expand_full(unhold(e),v)
$, sf_factor(a,$D=$2):
 nargs(a,1,2)
 v=opt_var(a,1)
 e=unhold(ev(a[0]))
 $! factor_expr(e,v,$D)
$, sf_cfactor(a):
 $! sf_factor(a,$B)
$, sf_comdenom(a):
 nargs(a,1,2)
 $! comdenom(unhold(ev(a[0])))
$, sf_propfrac(a):
 nargs(a,1,2)
 v=opt_var(a,1)
 $! lmap($; u:propfrac(u,v),unhold(ev(a[0])))
$, polyvar(e,a,i):
 v=opt_var(a,i)
 if v is $#:
  ss=$e(e)
  v='x' if 'x' in ss or $- ss $& ss[0]
 $! v
$, sf_polycoeffs(a):
 nargs(a,1,2)
 e=unhold(ev(a[0]))
 v=polyvar(e,a,1)
 cs=$[(e,v)
 if cs is $#:
  err('Polynomial expected')
 $F $/(cs)>1 $* cs[-1]==0:
  cs.pop()
 $!('$J',)+$1(reversed(cs))
$, sf_polydegree(a):
 nargs(a,1,2)
 e=unhold(ev(a[0]))
 v=polyvar(e,a,1)
 d=degree($?(e),v)
 if d is $#:
  err('Polynomial expected')
 if e==0:
  $!('*',-1,'$P')
 $! d
$, sf_polyquo(a,which=0):
 nargs(a,2,3)
 p=unhold(ev(a[0]))
 q=unhold(ev(a[1]))
 v=polyvar($`(p,q),a,2)
 cp=$[(p,v)
 cq=$[(q,v)
 if cp is $# or cq is $#:
  err('Polynomial expected')
 qq,rr=e_divmod(cp,cq)
 $! fromcoeffs(qq if which==0 $& rr,v)
$, sf_polyrem(a):
 $! sf_polyquo(a,1)
$, sf_polyroots(a,$D=$2):
 nargs(a,1,2)
 if $/(a)==1:
  L=ev(a[0])
  if $- $)(L,'$J'):
   err('List expected')
  v='X_'
  e=polyeval(L,v)
 $&:
  v,_=var_of(a[1])
  e=evw(a[0],[v])
 r=zeros(e,v,$D)
 $! r if r is $- $# $&('$J',)
$, sf_cpolyroots(a):
 $! sf_polyroots(a,$B)
$, rawnames(t,$9):
 if $0(t)is $p:
  if t $- in('pi','e','i','$P')$* t $- in $9:
   $9.$%(t)
 $= $0(t)is $1:
  $( u in t[2:]if t[0]=='call' $& t[1:]:
   rawnames(u,$9)
 $! $9
$, vieta_poly(a):
 e=unhold(ev(a[0]))
 if $)(e,'='):
  e=$_(e[1],e[2])
 v=polyvar(e,a,1)
 cs=$[(e,v)
 if cs is $#:
  err('Polynomial expected')
 $F cs $* cs[-1]==0:
  cs.pop()
 if $/(cs)<2:
  err('Polynomial of degree 1 or more expected')
 cs.reverse()
 es=[]
 $( k in $+(1,$/(cs)):
  es.$%($V(cs[k],cs[0])if k%2==0 $& $m($V(cs[k],cs[0])))
 $! v,cs,es
$, sym_terms(e,vs):
 if $- vs:
  $!{():e}if e!=0 $&{}
 cs=$[(e,vs[0])
 if cs is $#:
  err('Polynomial in the roots expected')
 $9={}
 $( k in $+($/(cs)):
  if cs[k]!=0:
   $( m,w in sym_terms(cs[k],vs[1:]).items():
    $9[(k,)+m]=w
 $! $9
$, sym_elem(n):
 E=[{(0,)*n:1}]+[{}$( k in $+(n)]
 $( j in $+(n):
  $( k in $+(j+1,0,-1):
   $( m,w in E[k-1].items():
    m2=m[:j]+(1,)+m[j+1:]
    E[k][m2]=E[k].get(m2,0)+w
 $! E
SYMWORK=[0]
$, sym_mul(p,q):
 SYMWORK[0]+=$/(p)*$/(q)
 if SYMWORK[0]>200000:
  toobig('symmetric expression too large')
 $9={}
 $( m,w in p.items():
  $( m2,w2 in q.items():
   t=$1([m[i]+m2[i]$( i in $+($/(m))])
   $9[t]=$9.get(t,0)+w*w2
 $! $9
$, sym_value(e,vs,es):
 n=$/(vs)
 if n>8:
  toobig('vieta with an expression works up to degree 8')
 f=sym_terms($?(e),vs)
 E=sym_elem(n)
 r=0
 $F f:
  m=max(f)
  c=f[m]
  val=c
  P={(0,)*n:1}
  $( k in $+(1,n+1):
   d=m[k-1]-(m[k]if k<n $& 0)
   if d<0:
    err('Not symmetric in the roots '+','.join(vs))
   val=$<(val,pw(es[k-1],d))
   $( j in $+(d):
    P=sym_mul(P,E[k])
  r=$`(r,val)
  $( t,w in P.items():
   u=$?($_(f.get(t,0),$<(c,w)))
   if u==0:
    f.pop(t,$#)
   $&:
    f[t]=u
 $! r
$, vieta_rel(es):
 n=$/(es)
 E=sym_elem(n)if n<5 $& $#
 r=['$*']
 $( k in $+(1,n+1):
  if E:
   lhs=0
   $( m in E[k]:
    t=1
    $( j in $+(n):
     if m[j]:
      t=$<(t,'r'+$p(j+1))
    lhs=$`(lhs,t)
  $&:
   lhs='e'+$p(k)
  r.$%(('=',lhs,es[k-1]))
 $! $1(r)if n>1 $& r[1]
''')
_x(r'''$, sf_vieta(a):
 nargs(a,1,4)
 L=unhold(ev(a[0]))
 if $)(L,'$J'):
  nargs(a,1,2)
  v=var_of(a[1])[0]if $/(a)>1 $& 'x'
  r=1
  $( c in L[1:]:
   r=$?($<(r,$_(v,c)))
  $! r
 v,cs,es=vieta_poly(a)
 if $/(a)<3:
  $! vieta_rel(es)
 if $/(a)==4:
  vs=[$p(n)$( n in unhold(a[3])[1:]]if $)(a[3],'$J')$&[]
 $&:
  known=[v]
  $( c in cs:
   known+=$e(c)
  vs=[n $( n in rawnames(a[2],[])if n $- in known]
  vs.sort()
 if $/(vs)!=$/(es):
  err('Name all %d roots: $( example vieta(p,x,expr,{a,b})'%$/(es))
 e=unhold(evw(a[2],vs))
 SYMWORK[0]=0
 num=sym_value(getnum(e),vs,es)
 den=sym_value(getden(e),vs,es)
 if den==0:
  $! '$I'
 $! comdenom($V(num,den))
$, sf_linsolve(a):
 vs,gs=solvevars(a[1:])
 e=evw(a[0],vs)
 eqs=eqlist(e)
 fs=[eqexpr(q)$( q in eqs]
 if $- is_linear_sys(fs,vs):
  err('Argument error: $k system required')
 $j=linsys(fs,vs)
 if $- $j:
  $! 'false'
 $!('$J',)+$1($j[0][v]$( v in vs)
$, sf_domain(a):
 nargs(a,2,2)
 e,v,val=$n(a)
 r=domain(e,v)
 $! r if r is $- $# $&('domain',e,v)
$, sf_completesq(a):
 nargs(a,2,2)
 v,_=var_of(a[1])
 e=unhold(evw(a[0],[v]))
 if $)(e,'='):
  lhs=complete_sq($_(e[1],e[2]),v,$B)
  $! lhs
 $! complete_sq(e,v,$2)
$, complete_sq(e,v,eq):
 cs=$[(e,v)
 if cs is $# or $/(cs)!=3:
  err('Quadratic expected')
 c,b,a=cs
 h=$.($V(b,$<(2,a)))
 k=$.($_(c,$V($<(b,b),$<(4,a))))
 sq=('^',$`(v,h),2)
 t=sq if a==1 $&('*',a,sq)
 if eq:
  $!('=',('hold',t),$m(k))
 if k==0:
  $!('hold',t)
 $!('hold',('+',t,k))
$, sf_constructmat(a):
 nargs(a,5,5)
 i,_=var_of(a[1])
 j,_=var_of(a[2])
 e=evw(a[0],[i,j])
 r=ev(a[3])
 c=ev(a[4])
 cells(r,c)
 $! mk([[subsd(e,{i:ii,j:jj})$( jj in $+(1,c+1)]$( ii in $+(1,r+1)])
$, sf_charpoly(a):
 nargs(a,2,2)
 A=ev(a[0])
 v=a[1]if $0(a[1])is $p $& ev(a[1])
 $! charpoly(A,v)
$, sf_simplify(a):
 e=unhold(ev(a[0]))
 $! nice(pyth(e))
SF={
 'd':sf_d,'$N':sf_int,'$|':sf_limit,'sumseq':sf_sum,
 'prodseq':sf_prod,'seq':sf_seq,'taylor':sf_taylor,'series':sf_series,
 'dominantterm':sf_dominant,'solve':sf_solve,'csolve':sf_csolve,
 'zeros':sf_zeros,'czeros':sf_czeros,'nsolve':sf_nsolve,
 'desolve':sf_desolve,'fmin':sf_fmin,'fmax':sf_fmax,'nfmin':sf_nfmin,
 'nfmax':sf_nfmax,'nint':sf_nint,'arclen':sf_arclen,
 'tangentline':sf_tangent,'normalline':sf_normal,'impdif':sf_impdif,
 'avgrc':sf_avgrc,'centraldiff':sf_central,'nderivative':sf_nderiv,
 '$?':sf_expand,'factor':sf_factor,'cfactor':sf_cfactor,
 'comdenom':sf_comdenom,'propfrac':sf_propfrac,
 'polycoeffs':sf_polycoeffs,'polydegree':sf_polydegree,
 'polyquotient':sf_polyquo,'polyremainder':sf_polyrem,
 'polyroots':sf_polyroots,'cpolyroots':sf_cpolyroots,
 'linsolve':sf_linsolve,'domain':sf_domain,'vieta':sf_vieta,
 'completesquare':sf_completesq,'constructmat':sf_constructmat,
 'charpoly':sf_charpoly,'simplify':sf_simplify,
 }
$, when_simp(c,a,b=$#):
 t=tobool(rel(c[0],c[1],c[2]))if isrel(c)$& tobool(c)
 if t is $B:
  $! a
 if t is $2:
  $! b if b is $- $# $& '$I'
 $! $#
$t['when']=when_simp
$, finalize(r,quiet=$2):
 if $)(r,'$p'):
  $! r
 if $- $)(r,'hold'):
  r=$.(r)if $-($)(r,'$J')or $)(r,'mat'))$& lmap($.,r)
  if needpyth(r):
   r=pyth(r)
  if SET['mode']=='approx' or $b(r):
   r=evalf(r)
  $= SET['mode']=='exact':
   r=exactify(r)
 if SET['$D']=='$U' $* $- STATE['$D']$* has(r,'i')$* $- quiet:
  err('Non-$U result')
 $! r
$, sqtrig(e,$9):
 if $0(e)is $- $1 or e[0]=='Q':
  $!
 if e[0]=='^' $* head(e[1])in('sin','cos')$* $i(e[2])$* e[2]>=2:
  $9.$%((e[1][0],e[1][1]))
 $( a in e[1:]:
  sqtrig(a,$9)
$, needpyth(r):
 if $- $)(r,'+'):
  $! $2
 $9=[]
 sqtrig(r,$9)
 $( n,u in $9:
  if(('cos' if n=='sin' $& 'sin'),u)in $9:
   $! $B
 $! $2
$, pre_register(s):
 low=s.replace(' ','').lower()
 cands=[]
 if ':=' in low:
  cands.$%(low.split(':=')[0])
 if low.$~('define'):
  cands.$%(low[6:].split('=')[0])
 $( arrow in('->','\u2192','=:'):
  if arrow in low:
   cands.$%(low.split(arrow)[-1])
 $( c in cands:
  i=c.find('(')
  if i>0:
   nm=c[:i]
   ok=$B
   $( ch in nm:
    if $-(ch.isalpha()or ch.isdigit()or ch=='_'):
     ok=$2
   if ok $* nm $- in STATE['tmpf']:
    STATE['tmpf'].$%(nm)
$, command(c):
 r=command0(c)
 keep()
 $! r
''')
_x(r'''$, command0(c):
 p=c.split()
 if $- p:
  $! ''
 k=p[0]
 if k in('deg','degree'):
  SET['$l']='deg'
  $! 'Angle: degree'
 if k in('rad','radian'):
  SET['$l']='rad'
  $! 'Angle: radian'
 if k in('grad','gradian'):
  SET['$l']='grad'
  $! 'Angle: gradian'
 if k in('approx','auto','exact'):
  SET['mode']=k
  $! 'Mode: '+k
 if k in('$U','$4','rect'):
  SET['$D']='$U' if k=='$U' $& 'rect'
  $! 'Complex format: '+SET['$D']
 if k in('digits','$C'):
  if $/(p)>1 $* $- p[1].isdigit():
   $! 'Use :digits n with n from 1 to 15'
  n=$q(p[1])if $/(p)>1 $& 10
  OPT['digits']=max(1,min(15,n))
  $! 'Digits: '+$p(OPT['digits'])
 if k=='ascii':
  OPT['uni']=$2
  $! 'ASCII output'
 if k in('unicode','uni'):
  OPT['uni']=$B
  $! 'Unicode output'
 if k=='vars':
  $9=[]
  $( n in sorted(ENV):
   $9.$%(n+' = '+fmt(ENV[n]))
  $( n in sorted(UFUN):
   ps,b=UFUN[n]
   $9.$%(n+'('+','.join(ps)+') = '+fmt(b))
  $! '\n'.join($9)if $9 $& '(none)'
 if k in('clear','clearaz','reset'):
  ENV.clear()
  UFUN.clear()
  $! 'Cleared variables $* functions'
 if k=='clearans':
  STATE['ans']=0
  $! 'ans cleared'
 if k in('clearhist','clearhistory'):
  $! 'The history is kept only in the full-screen mode'
 if k=='free':
  STATE['ans']=0
  STATE['tinames']=$#
  ${:
   import gc
   gc.collect()
   $! 'ans cleared, %d KB free'%(gc.mem_free()//1024)
  $3 $6:
   $! 'ans cleared'
 if k in('mem','memory'):
  ${:
   import gc
   gc.collect()
   $! 'Memory: %d KB free, %d KB used'%(gc.mem_free()//1024,gc.mem_alloc()//1024)
  $3 $6:
   $! 'Memory information is $- available'
 if k in('mode','modes','getmode'):
  $!('$l='+SET['$l']+' mode='+SET['mode']+' $D='+SET['$D']+
 ' digits='+$p(OPT['digits']))
 if k=='test':
  _load('cashelp')
  saved=(dict(SET),dict(OPT))
  SET.update({'$l':'rad','mode':'auto','$D':'$U'})
  OPT.update({'uni':$B,'digits':10})
  ${:
   $! selftest(run)
  finally:
   SET.update(saved[0])
   OPT.update(saved[1])
 if k in('menu','m'):
  menu()
  $! ''
 if k in('gui','g'):
  $! gui()
 if k=='keys':
  ${:
   from ti_system import get_key
  $3 ImportError:
   $! 'The key test needs the calculator (ti_system)'
  print('Press keys; esc twice to stop')
  last=''
  $F $B:
   key=get_key(1)
   print(repr(key))
   if key=='esc' $* last=='esc':
    $! ''
   last=key
 if k in('help','?','h'):
  _load('cashelp')
  $! help(p[1]if $/(p)>1 $& $#)
 $! 'Unknown command :'+k
$, run(s):
 s=s.strip()
 if $- s:
  $! ''
 low=s.lower()
 if low[0]==':':
  $! command(low[1:])
 if low[0]=='?':
  $! command('help '+low[1:].strip())
 if low.$~('help'):
  $! command(low)
 if low.$~('delvar'):
  $( n in low[6:].replace(',',' ').split():
   ENV.pop(n,$#)
   UFUN.pop(n,$#)
  keep()
  $! 'Done'
 if low in('clearaz','clear'):
  $! command('clear')
 s=closeup(s)
 pre_register(s)
 t=parse(s,isfunc)
 STATE['$D']=(SET['$D']!='$U')
 r=fastnum(t)if SET['mode']=='approx' $& $#
 if r is $#:
  r=ev(t)
 r=finalize(r)
 if $-($)(t,'define')or($)(r,'$p')$* r[1]=='Done')):
  STATE['ans']=unhold(r)if $- $)(r,'$p')$& r
 keep()
 $9=fmt_top(r)
 un=[]
 unknown_calls(r,un)
 $( n in un:
  g=suggest(n)
  if g:
   $9+='\n('+n+' is $- a command; did you mean '+g+'?)'
 $! $9
KEEP='ncasmem'
$, memtext():
 u=OPT['uni']
 OPT['uni']=$2
 ${:
  $9=[':'+SET['$l'],':'+SET['mode'],
 ':'+('$U' if SET['$D']=='$U' $& '$4'),
 ':digits '+$p(OPT['digits'])]
  if $- u:
   $9.$%(':ascii')
  $( n in sorted(ENV):
   $9.$%(n+':='+fmt(ENV[n]))
  $( n in sorted(UFUN):
   ps,b=UFUN[n]
   $9.$%(n+'('+','.join(ps)+'):='+fmt(b))
 finally:
  OPT['uni']=u
 $! '\n'.join([l $( l in $9 if $/(l)<2000 $* all([0<ord(c)<128 $( c in l])])
$, pack(t):
 $9=[]
 $( i in $+(0,$/(t),6):
  n=0
  $( c in reversed(t[i:i+6]):
   n=n*128+ord(c)
  $9.$%(n)
 $! $9
$, unpack(xs):
 cs=[]
 $( v in xs:
  n=$q(round(v))
  $F n:
   cs.$%(chr(n%128))
   n//=128
 $! ''.join(cs)
$, keep():
 if STATE.get('kept')is $# or STATE.get('restoring'):
  $!
 t=memtext()
 if t==STATE['kept']:
  $!
 STATE['kept']=t
 ${:
  from ti_system import store_list
  store_list(KEEP,pack(t)or[0])
 $3 $6:
  pass
$, restore():
 if STATE.get('kept')is $- $#:
  $!
 STATE['kept']=memtext()
 ${:
  from ti_system import recall_list
  t=unpack(recall_list(KEEP))
 $3 $6:
  $!
 STATE['restoring']=$B
 ${:
  $( line in t.split('\n'):
   ${:
    run(line)
   $3 $6:
    pass
 finally:
  STATE['restoring']=$2
 STATE['ans']=0
 STATE['kept']=memtext()
$, menu():
 _load('casmenu')
 runmenu(run)
GUI=$B
$, gui():
 if $- GUI:
  $! 'The full-screen mode is the separate program ncasgui.'
 ${:
  _load('casgui')
 $3 ImportError as ex:
  if 'casgui' $- in $p(ex):
   $d
  $! 'casgui is $- installed (needed $( the full-screen mode); using text mode.'
 restore()
 $! rungui(run)
$, startgui():
 r=gui()
 if r:
  print(r)
  print('The text version is the program ncastext.')
$, start():
 ${:
  import ti_draw
 $3 ImportError:
  $! cas()
 r=gui()
 if r:
  print(r)
  cas()
$, ver():
 $! 'nCAS '+VERSION
$, calc(s):
 ${:
  $! run(s)
 $3 $S as ex:
  $! 'Error: '+$p(ex)
$, prompt():
 p=[]
 if SET['$l']!='rad':
  p.$%(SET['$l'])
 if SET['mode']!='auto':
  p.$%(SET['mode'])
 if SET['$D']!='$U':
  p.$%('$D')
 $! ' '.join(p)+'> '
''')
_x(r'''$, cas():
 restore()
 print('nCAS '+VERSION+' $( TI-Nspire CX II')
 print(('? help, m menu, g full screen, q quit')if GUI $& '? help, m menu, q quit')
 blank=0
 $F $B:
  ${:
   s=input(prompt())
  $3(EOFError,$u):
   $R
  s=s.strip()
  if s in('q','quit','exit',':q'):
   $R
  if $- s:
   blank+=1
   if blank>=2:
    print('($0 q $* enter to quit)')
    blank=0
   $7
  blank=0
  if s.lower()in('m','menu'):
   ${:
    menu()
   $3 $6 as ex:
    print('Error: '+$p(ex))
   $7
  if s.lower()in('g','gui'):
   ${:
    r=gui()
   $3 $6 as ex:
    r='Error: '+$p(ex)
   if r:
    print(r)
   $7
  ${:
   $9=run(s)
   if $9:
    print($9)
  $3 $S as ex:
   print('Error: '+$p(ex))
  $3 $E:
   print('Error: Division by zero')
  $3 MemoryError:
   ${:
    import gc
    gc.collect()
   $3 ImportError:
    pass
   print('Error: Out of memory')
  $3 $u:
   print('Break')
  $3 RuntimeError as ex:
   print('Error: Too $4 ('+$p(ex)+')')
  $3 $6 as ex:
   print('Error: '+$p(ex))
''')
_L['cashelp']=(r'''CATS=(
 ('alg','Algebra','solve cSolve zeros cZeros nSolve linSolve factor cFactor $? comDenom propFrac getNum getDenom completeSquare polyCoeffs polyDegree polyQuotient polyRemainder polyGcd polyRoots cPolyRoots polyEval vieta tExpand tCollect simplify exact approx domain'),
 ('calc','Calculus','d $N $| sumSeq prodSeq taylor series dominantTerm deSolve impDif arcLen tangentLine normalLine fMin fMax nfMin nfMax nInt nDerivative avgRC centralDiff'),
 ('mat','Matrix/vector','det identity transpose rref ref inverse eigVl eigVc charPoly LU QR trace norm rowNorm colNorm diag augment colAugment subMat rowSwap rowAdd mRow mRowAdd crossP dotP unitV simult constructMat newMat randMat dim rowDim colDim mat>$J $J>mat'),
 ('num','Numbers','gcd lcm mod remain intDiv isPrime nCr nPr ! floor ceiling round iPart fPart sign $H $U imag conj $l'),
 ('$J','Lists/stats','seq sum product mean median stdDev stdDevPop variance varPop max min sortA sortD cumulativeSum deltaList augment left right mid count normPdf normCdf invNorm binomPdf binomCdf poissPdf poissCdf geomPdf geomCdf'),
 ('conv','Conversions (expr>>$A)','>>Decimal >>approxFraction() >>DMS >>DD >>Rad >>Grad >>Polar >>Rect >>Cylind >>Sphere >>exp >>ln >>logbase() >>sin >>cos >>Base2 >>Base10 >>Base16 exp>$J()'),
 ('cmd','Commands',':deg :rad :grad :auto :exact :approx :$U :$4 :digits n :ascii :unicode :vars :clear :clearans :clearhist :free :mode :mem  delvar a  q=quit'),
 )
SYN={
 'solve':'solve(eqn,var) solve(eqn,var=guess)\nsolve(ineq,var) solve(eq1 $* eq2,{x,y})\nsolve(...)|x>0  (n1,n2..=any integer)',
 'csolve':'cSolve(eqn,var) $4 solutions',
 'zeros':'zeros(expr,var) -> $J of roots\nzeros({e1,e2},{x,y}) -> matrix',
 'czeros':'cZeros(expr,var) $4 roots',
 'nsolve':'nSolve(eqn,var[=guess][,lo,hi])',
 'linsolve':'linSolve({eq1,eq2},{x,y})',
 'factor':'factor(expr[,var]) factor(integer)\nwith var: irrational factors',
 'cfactor':'cFactor(expr[,var]) $4 factors',
 '$?':'$?(expr[,var]) incl. partial fractions',
 'comdenom':'comDenom(expr) common denominator',
 'propfrac':'propFrac(expr[,var]) proper fraction',
 'getnum':'getNum(expr) numerator',
 'getdenom':'getDenom(expr) denominator',
 'completesquare':'completeSquare(expr_or_eqn,var)',
 'polycoeffs':'polyCoeffs(poly[,var]) -> {an..a0}',
 'polydegree':'polyDegree(poly[,var])',
 'polyquotient':'polyQuotient(p1,p2[,var])',
 'polyremainder':'polyRemainder(p1,p2[,var])',
 'polygcd':'polyGcd(p1,p2)',
 'polyroots':'polyRoots(poly,var) polyRoots({$[})',
 'cpolyroots':'cPolyRoots(poly,var)',
 'polyeval':'polyEval({$[},x)',
 'vieta':"vieta(poly,x) Vieta's formulas\nvieta({r1,r2,..},x) polynomial from roots\nvieta(poly,x,a^2+b^2) symmetric value",
 'texpand':'tExpand(expr) $? trig of sums/multiples',
 'tcollect':'tCollect(expr) products -> multiple angles',
 'simplify':'simplify(expr) extra simplification',
 'exact':'exact(expr[,tol]) floats -> fractions',
 'approx':'approx(expr) decimal value',
 'domain':'domain(expr,var)',
 'd':'d(expr,var[,order])  d(expr,var)|var=val\nderivative(...) same',
 '$N':'$N(expr,var) antiderivative\nintegral(expr,var,a,b) definite\n(\u222b also accepted)',
 '$|':'$|(expr,var,point[,dir]) dir:-1 left,1 right\npoint may be $P or -$P',
 'sumseq':'sumSeq(expr,var,lo,hi)  (\u03a3) hi may be $P',
 'prodseq':'prodSeq(expr,var,lo,hi)  (\u03a0)',
 'taylor':'taylor(expr,var,order[,point])',
 'series':'series(expr,var,order[,point])',
 'dominantterm':'dominantTerm(expr,var[,point])',
 'desolve':"deSolve(ode,x,y) use y' $* y''\ndeSolve(y''+y=0 $* y(0)=0 $* y'(0)=1,x,y)",
 'impdif':'impDif(eqn,x,y[,order]) dy/dx',
 'arclen':'arcLen(expr,var,a,b)',
 'tangentline':'tangentLine(expr,var,point)',
 'normalline':'normalLine(expr,var,point)',
 'fmin':'fMin(expr,var[,lo,hi]) -> var=value',
 'fmax':'fMax(expr,var[,lo,hi])',
 'nfmin':'nfMin(expr,var[,lo,hi]) numeric',
 'nfmax':'nfMax(expr,var[,lo,hi]) numeric',
 'nint':'nInt(expr,var,a,b) numeric $N',
 'nderivative':'nDerivative(expr,var=val[,order])',
 'avgrc':'avgRC(expr,var[=val][,h])',
 'centraldiff':'centralDiff(expr,var[=val][,h])',
 'det':'det(M)','inverse':'M^-1 or inverse(M)','rref':'rref(M)','ref':'ref(M)',
 'eigvl':'eigVl(M) eigenvalues','eigvc':'eigVc(M) unit eigenvectors (columns)',
 'charpoly':'charPoly(M,var)','lu':'LU(M) -> {L,U,P} with P*M=L*U','qr':'QR(M) -> {Q,R}',
 'simult':'simult(A,b) solves A*x=b','constructmat':'constructMat(expr,i,j,$X,cols)',
 'crossp':'crossP(u,v)','dotp':'dotP(u,v)','unitv':'unitV(v)','norm':'norm(M)',
 'seq':'seq(expr,var,lo,hi[,step])',
 'ncr':'nCr(n,k)','npr':'nPr(n,k)','gcd':'gcd(a,b)','lcm':'lcm(a,b)',
 'mod':'mod(a,b)','isprime':'isPrime(n)',
 'define':'Define f(x)=expr   or   f(x):=expr\nexpr->a  or  a:=expr   delvar a',
 'with':'expr|x=3   expr|x>0   solve(...)|0<=x<=2pi\n(eq)|x=4 checks a solution: true/false',
 'menu':'m or menu: numbered menus build the\ncommand $( you; 0 back, q quit.\nMatrices may be typed 1,2;3,4',
 'syntax':'implicit mult: 2x  3(x+1)  x(x+1)\n^ or ** power, $O( or \u221a, pi, e, i, $P\n<= >= /= $* or $-, ans = last result\nlog(x)=ln(x) ([ln] key); log10(x), log(x,b)',
 'log':'log(x) natural log (= ln, the [ln] key)\nlog10(x) base 10, log(x,b) base b\nmenu Logs: change base, check an answer',
 }
$, help($A=$#):
 if $A is $#:
  $9=['nCAS help: ?topic or ?command']
  $( k,t,items in CATS:
   $9.$%('?'+k+'  '+t)
  $9.$%('?define ?with ?syntax ?menu')
  $9.$%('m = menus (no typing of names)')
  $! '\n'.join($9)
 $A=$A.lower().replace('(','').strip()
 $( k,t,items in CATS:
  if $A==k:
   $! t+':\n'+items
 if $A in SYN:
  $! SYN[$A]
 $( k in SYN:
  if k.$~($A):
   $! SYN[k]
 $! 'No help $( '+$A
''',
r'''SELFTEST=(
 ('factor(x^2-5x+6)','(x-2)*(x-3)'),
 ('$?((x+1)^3)','x^3+3*x^2+3*x+1'),
 ('solve(x^2-5x+6=0,x)','x=2 or x=3'),
 ('solve(x^2=2,x)','x=-\u221a2 or x=\u221a2'),
 ('d(x^3*sin(x),x)','x^3*cos(x)+3*x^2*sin(x)'),
 ('$N(x*e^x,x)','x*e^x-e^x'),
 ('$N(1/(1+x^2),x,0,1)','\u03c0/4'),
 ('$|(sin(x)/x,x,0)','1'),
 ('taylor(e^x,x,3)','x^3/6+x^2/2+x+1'),
 ('sumSeq(k,k,1,n)','n*(n+1)/2'),
 ("deSolve(y'=y,x,y)",'y=c1*e^x'),
 ('det([[1,2][3,4]])','-2'),
 ('[[1,2][3,4]]^-1','[[-2,1][3/2,-1/2]]'),
 ('$O(12)','2*\u221a3'),
 ('cSolve(x^2+1=0,x)','x=-i or x=i'),
 ('factor(360)','2^3*3^2*5'),
 ('solve(x^2-4>0,x)','x<-2 or x>2'),
 ('nSolve(cos(x)=x,x)','0.7390851332'),
 )
$, selftest(run):
 ok=0
 $9=[]
 $( q,a in SELFTEST:
  ${:
   r=run(q)
  $3 $6 as ex:
   r='ERR '+$p(ex)
  if r==a:
   ok+=1
  $&:
   $9.$%('FAIL '+q+' -> '+r)
 $9.$%('%d/%d tests passed'%(ok,$/(SELFTEST)))
 $! '\n'.join($9)
''',)
_L['casmenu']=(r'''ALG=(
 ('Expand','$?(@1`,@2`)',(('$]',$#),('Var (blank=all)',''))),
 ('Factor','factor(@1`,@2`)',(('$]',$#),('Var (blank=Q)',''))),
 ('cFactor','cFactor(@1`,@2`)',(('$]',$#),('Var (blank=all)',''))),
 ('Simplify','simplify(@1)',(('$]',$#),)),
 ('comDenom','comDenom(@1)',(('$]',$#),)),
 ('propFrac','propFrac(@1`,@2`)',(('$]',$#),('Var',''))),
 ('Partial frac','$?(@1,@2)',(('Rational expr',$#),('Var','x'))),
 ('Complete sq','completeSquare(@1,@2)',(('Quadratic/eqn',$#),('Var','x'))),
 ('Poly divide','polyQuotient(@1,@2,@3)',(('Dividend',$#),('Divisor',$#),('Var','x'))),
 ('Poly remain','polyRemainder(@1,@2,@3)',(('Dividend',$#),('Divisor',$#),('Var','x'))),
 ('Poly gcd','polyGcd(@1,@2)',(('Poly 1',$#),('Poly 2',$#))),
 ('Substitute','(@1)|@2=@3',(('$]',$#),('Var','x'),('Value',$#))),
 ('tExpand','tExpand(@1)',(('$]',$#),)),
 ('tCollect','tCollect(@1)',(('$]',$#),)),
 ('Decimal','approx(@1)',(('$]',$#),)),
 ('Exact','exact(@1)',(('$]',$#),)),
 )
CALC=(
 ('Derivative','d(@1,@2`,@3`)',(('f',$#),('Var','x'),('Order',''))),
 ('Deriv at pt','d(@1,@2)|@2=@3',(('f',$#),('Var','x'),('At',$#))),
 ('Integral','$N(@1,@2)',(('f',$#),('Var','x'))),
 ('Def $N','$N(@1,@2,@3,@4)',(('f',$#),('Var','x'),('Lower ($P ok)',$#),('Upper',$#))),
 ('Limit','$|(@1,@2,@3`,@4`)',(('f',$#),('Var','x'),('Point ($P ok)','0'),('Side 1/-1',''))),
 ('Taylor','taylor(@1,@2,@3`,@4`)',(('f',$#),('Var','x'),('Order','5'),('Point',''))),
 ('Series','series(@1,@2,@3`,@4`)',(('f',$#),('Var','x'),('Order','5'),('Point',''))),
 ('Sum (sigma)','sumSeq(@1,@2,@3,@4)',(('Term',$#),('Index','k'),('From','1'),('To ($P ok)','n'))),
 ('Product','prodSeq(@1,@2,@3,@4)',(('Term',$#),('Index','k'),('From','1'),('To','n'))),
 ('deSolve',"deSolve(@1` $* @2`` $* @3`,@4,@5)",
 (("ODE, use y' y''",$#),('Cond eg y(0)=1',''),("Cond eg y'(0)=0",''),('x var','x'),('y var','y'))),
 ('Implicit d/dx','impDif(@1,@2,@3)',(('Equation',$#),('x var','x'),('y var','y'))),
 ('Tangent line','tangentLine(@1,@2,@3)',(('f',$#),('Var','x'),('At',$#))),
 ('Normal line','normalLine(@1,@2,@3)',(('f',$#),('Var','x'),('At',$#))),
 ('Arc length','arcLen(@1,@2,@3,@4)',(('f',$#),('Var','x'),('From',$#),('To',$#))),
 ('fMin','fMin(@1,@2`,@3,@4`)',(('f',$#),('Var','x'),('Lower',''),('Upper',''))),
 ('fMax','fMax(@1,@2`,@3,@4`)',(('f',$#),('Var','x'),('Lower',''),('Upper',''))),
 ('Numeric integ','nInt(@1,@2,@3,@4)',(('f',$#),('Var','x'),('Lower',$#),('Upper',$#))),
 )
SOLV=(
 ('Solve','solve(@1,@2)`|@3`',(('Equation/ineq',$#),('Var','x'),('Condition eg x>0',''))),
 ('cSolve','cSolve(@1,@2)',(('Equation',$#),('Var','x'))),
 ('Zeros','zeros(@1,@2)',(('$]',$#),('Var','x'))),
 ('cZeros','cZeros(@1,@2)',(('$]',$#),('Var','x'))),
 ('nSolve','nSolve(@1,@2`,@3,@4`)',(('Equation',$#),('Var or x=guess','x'),('Lower',''),('Upper',''))),
 ('System 2 eqs','solve(@1 $* @2,{@3})',(('Eq 1',$#),('Eq 2',$#),('Vars','x,y'))),
 ('System 3 eqs','solve(@1 $* @2 $* @3,{@4})',(('Eq 1',$#),('Eq 2',$#),('Eq 3',$#),('Vars','x,y,z'))),
 ('Poly roots','polyRoots(@1,@2)',(('Polynomial',$#),('Var','x'))),
 ('Domain','domain(@1,@2)',(('$]',$#),('Var','x'))),
 ('Vieta formulas','vieta(@1,@2)',(('Polynomial',$#),('Var','x'))),
 ('Roots to poly','vieta({@1},@2)',(('Roots eg 2,3',$#),('Var','x'))),
 ('Expr of roots','vieta(@1,@2,@3)',(('Polynomial',$#),('Var','x'),('Expr eg a^2+b^2',$#))),
 )
MATX=(
 ('det','det(@1)',(('Matrix 1,2;3,4',$#,'m'),)),
 ('Inverse','(@1)^-1',(('Matrix',$#,'m'),)),
 ('rref','rref(@1)',(('Matrix',$#,'m'),)),
 ('Transpose','transpose(@1)',(('Matrix',$#,'m'),)),
 ('A*B','(@1)*(@2)',(('Matrix A',$#,'m'),('Matrix B',$#,'m'))),
 ('A^n','(@1)^(@2)',(('Matrix',$#,'m'),('Power n','2'))),
 ('Eigenvalues','eigVl(@1)',(('Matrix',$#,'m'),)),
 ('Eigenvectors','eigVc(@1)',(('Matrix',$#,'m'),)),
 ('charPoly','charPoly(@1,@2)',(('Matrix',$#,'m'),('Var','x'))),
 ('Solve Ax=b','simult(@1,@2)',(('Matrix A',$#,'m'),('Column b 5;1',$#,'m'))),
 ('LU','LU(@1)',(('Matrix',$#,'m'),)),
 ('QR','QR(@1)',(('Matrix',$#,'m'),)),
 ('Dot product','dotP(@1,@2)',(('Vector u 1,2,3',$#,'m'),('Vector v',$#,'m'))),
 ('Cross product','crossP(@1,@2)',(('Vector u 1,2,3',$#,'m'),('Vector v',$#,'m'))),
 ('Norm','norm(@1)',(('Matrix/vector',$#,'m'),)),
 ('Identity','identity(@1)',(('Size n','3'),)),
 )
NUMB=(
 ('Factor $q','factor(@1)',(('Integer',$#),)),
 ('isPrime','isPrime(@1)',(('Integer',$#),)),
 ('gcd','gcd(@1,@2)',(('a',$#),('b',$#))),
 ('lcm','lcm(@1,@2)',(('a',$#),('b',$#))),
 ('mod','mod(@1,@2)',(('a',$#),('b',$#))),
 ('nCr','nCr(@1,@2)',(('n',$#),('r',$#))),
 ('nPr','nPr(@1,@2)',(('n',$#),('r',$#))),
 ('Factorial','(@1)!',(('n',$#),)),
 ('Real part','$U(@1)',(('Complex z',$#),)),
 ('Imag part','imag(@1)',(('Complex z',$#),)),
 ('Conjugate','conj(@1)',(('Complex z',$#),)),
 ('|z|','$H(@1)',(('Complex z',$#),)),
 ('Angle','$l(@1)',(('Complex z',$#),)),
 ('Polar form','(@1)>>Polar',(('Complex z',$#),)),
 )
LIST=(
 ('Mean','mean({@1})',(('Data 1,2,3',$#),)),
 ('Median','median({@1})',(('Data',$#),)),
 ('Std dev (s)','stdDev({@1})',(('Data',$#),)),
 ('Variance (s2)','variance({@1})',(('Data',$#),)),
 ('Sum','sum({@1})',(('Data',$#),)),
 ('Sort up','sortA({@1})',(('Data',$#),)),
 ('Sequence','seq(@1,@2,@3,@4)',(('Term',$#),('Var','k'),('From','1'),('To','10'))),
 ('normCdf','normCdf(@1,@2`,@3,@4`)',(('Lower (-$P ok)',$#),('Upper',$#),('mu',''),('sigma',''))),
 ('invNorm','invNorm(@1`,@2,@3`)',(('Area',$#),('mu',''),('sigma',''))),
 ('binomPdf','binomPdf(@1,@2,@3)',(('n',$#),('p',$#),('x',$#))),
 ('binomCdf','binomCdf(@1,@2,@3,@4)',(('n',$#),('p',$#),('Lower','0'),('Upper',$#))),
 )
''',
r'''CONV=(
 ('>Decimal','(@1)>>Decimal',(('$]',$#),)),
 ('>Fraction','(@1)>>approxFraction()',(('Decimal',$#),)),
 ('>DMS','(@1)>>DMS',(('Angle',$#),)),
 ('>Polar','(@1)>>Polar',(('Complex/vector',$#),)),
 ('>Rect','(@1)>>Rect',(('Complex',$#),)),
 ('>exp form','(@1)>>exp',(('$]',$#),)),
 ('>ln form','(@1)>>ln',(('$]',$#),)),
 ('>sin form','(@1)>>sin',(('$]',$#),)),
 ('>cos form','(@1)>>cos',(('$]',$#),)),
 ('>Binary','(@1)>>Base2',(('Integer',$#),)),
 ('>Hex','(@1)>>Base16',(('Integer',$#),)),
 )
SETS=(
 ('Degree',':deg',()),
 ('Radian',':rad',()),
 ('Auto mode',':auto',()),
 ('Exact mode',':exact',()),
 ('Approx mode',':approx',()),
 ('Real res',':$U',()),
 ('Complex res',':$4',()),
 ('Digits',':digits @1',(('Digits 1-15','10'),)),
 ('Show vars',':vars',()),
 ('Clear vars',':clear',()),
 ('Define f(x)','@1(@2):=@3',(('Name','f'),('Params','x'),('Body',$#))),
 ('Store var','@1:=@2',(('Name',$#),('Value',$#))),
 ('Self-test',':test',()),
 ('Memory',':mem',()),
 ('Key test',':keys',()),
 )
LOGS=(
 ('log base b','log(@1,@2)',(('Value x',$#),('Base b',$#))),
 ('ln (base e)','ln(@1)',(('Value',$#),)),
 ('log10','log10(@1)',(('Value',$#),)),
 ('Change base','(@1)>>logbase(@2)',(('$]',$#),('New base','10'))),
 ('Solve log/exp','solve(@1,@2)',(('Equation',$#),('Var','x'))),
 ('Check answer','(@1)|@2',(('Equation',$#),('Solution eg x=4',$#))),
 ('Domain','domain(@1,@2)',(('$]',$#),('Var','x'))),
 ('nSolve','nSolve(@1,@2)',(('Equation',$#),('Var or x=guess','x'))),
 )
MAIN=(
 ('Algebra',ALG),('Calculus',CALC),('Solve',SOLV),('Matrix',MATX),
 ('Number/$D',NUMB),('Lists/stats',LIST),('Convert',CONV),
 ('Settings',SETS),('Logs',LOGS),
 )
NFIX=8
KEYS='123456789abcdefghijklmnop'
class Quit($6):
 pass
$, ask(q):
 ${:
  s=input(q)
 $3 EOFError:
  $d Quit()
 s=s.strip()
 if s.lower()in('q','quit'):
  $d Quit()
 $! s
$, show(title,labels):
 print('-- '+title+' --')
 line=''
 $( i in $+($/(labels)):
  cell=KEYS[i]+' '+labels[i]
  if line:
   print(line+' '*max(1,16-$/(line))+cell)
   line=''
  $&:
   line=cell
 if line:
  print(line)
 print('0 back  q quit')
$, pick(title,labels):
 show(title,labels)
 $F $B:
  s=ask('#: ').lower()
  if s in('','0'):
   $! $#
  i=KEYS.find(s)
  if $/(s)==1 $* 0<=i<$/(labels):
   $! i
  print('Choose '+KEYS[0]+'-'+KEYS[$/(labels)-1]+', 0 or q')
$, matrix_text(s):
 s=s.strip()
 if s $* s[0]$- in '[(' $*(';' in s or ',' in s):
  $! '['+s+']'
 $! s
$, build(item):
 label,tpl,prompts=item
 $g=[]
 $( p in prompts:
  q=p[0]
  d=p[1]
  hint='' if $- d $& ' ['+d+']'
  s=ask(q+hint+': ')
  if $- s:
   if d is $#:
    print('(cancelled)')
    $! $#
   s=d
  if $/(p)>2 $* p[2]=='m' $* s:
   s=matrix_text(s)
  $g.$%(s)
 $! fill(tpl,$g)
$, fill(tpl,$g):
 $9=''
 parts=tpl.split('`')
 $( k in $+($/(parts)):
  seg=parts[k]
  if k%2==1:
   blank=$2
   $( i in $+($/($g)):
    if('@'+$p(i+1))in seg $* $- $g[i]:
     blank=$B
   if blank:
    $7
  $9+=seg
 res=''
 i=0
 $F i<$/($9):
  c=$9[i]
  if c=='@' $* i+1<$/($9)$* '1'<=$9[i+1]<='9':
   res+=$g[$q($9[i+1])-1]
   i+=2
  $&:
   res+=c
   i+=1
 $! res
$, runmenu(run):
 print('Menus: pick a number or letter.')
 print("Type ans $( the last result.")
 ${:
  $F $B:
   k=pick('nCAS menu',[m[0]$( m in MAIN])
   if k is $#:
    $!
   title,items=MAIN[k]
   $F $B:
    j=pick(title,[it[0]$( it in items])
    if j is $#:
     $R
    cmd=build(items[j])
    if cmd is $#:
     $7
    print('> '+cmd)
    ${:
     $9=run(cmd)
    $3 $S as ex:
     $9='Error: '+$p(ex)
    $3 $E:
     $9='Error: Division by zero'
    $3 MemoryError:
     $9='Error: Out of memory'
    $3 RuntimeError as ex:
     $9='Error: Too $4'
    $3 Quit:
     $d
    $3 $6 as ex:
     $9='Error: '+$p(ex)
    if $9:
     print($9)
    ask('(enter) ')
 $3 Quit:
  $!
 $3 $u:
  $!
''',)
_L['casgui']=(r'''LH=18
CW=9
AW=7
BASE=14
MAXH=30
HISTCH=6000
UNDON=30
UNDOCH=3000
C_BAR=(30,60,130)
C_BART=(255,255,255)
C_TXT=(0,0,0)
C_RES=(0,70,170)
C_ERR=(190,0,0)
C_SEL=(205,225,255)
C_RULE=(215,215,215)
C_BOX=(240,240,240)
C_CUR=(220,0,0)
C_DIM=(110,110,110)
ENTER=('enter','ret','$!','center','\r','\n')
MENU=('menu',)
TABKEYS=('tab',)
BACKTAB=('shift+tab','shift tab','shifttab','backtab','btab')
CATKEYS=('cat','catalog','book')
TEXT={'space':' ','$O':'$O(','\u221a':'$O(','pi':'\u03c0',
 'exp':'e^','ln':'ln(','log':'log10(','square':'^2','\u00b2':'^2',
 'ee':'E','EE':'E','\u1d07':'E','$m':'-','(-)':'-','\u2212':'-',
 '\u00d7':'*','\u00f7':'/','\u2264':'<=','\u2265':'>=','\u2260':'/=',
 '\u2192':'->','ans':'ans','theta':'\u03b8','$H':'$H(',
 'sin':'sin(','cos':'cos(','tan':'tan(','sin\u207b\u00b9':'$y(',
 'cos\u207b\u00b9':'arccos(','tan\u207b\u00b9':'$s(','$P':'$P',
 'i':'i','e':'e','point':'.','decimal':'.','dot':'.','period':'.',
 'minus':'-','plus':'+','times':'*','multiply':'*','divide':'/',
 'power':'^'}
gu_TRIG=('sin(','cos(','tan(','$y(','arccos(','$s(',
 'sinh(','cosh(','tanh(','sec(','csc(','cot(')
NEEDANS='+*/^'
G={}
$, rungui(run):
 G.setdefault('hist',[])
 key=findkey()
 ${:
  import ti_draw
 $3 ImportError:
  ti_draw=$#
 if key is $# or ti_draw is $#:
  $! screen(run,key is $#)
 G['d']=ti_draw
 G['key']=key
 G['cmode']=0
 G['gui']=$B
 ${:
  w,h=ti_draw.get_screen_dim()
  w=$q(w)
  h=$q(h)
 $3 $6:
  w,h=318,212
 G['w']=w
 G['h']=h
 G['$X']=(h-2*LH-5)//LH
 G['ncell']=(w-16)//CW
 G['wrap']=(w-12)//AW
 ed_reset()
 G['sel']=$#
 G['top']=$#
 G['msg']=''
 ${:
  ti_draw.use_buffer()
  G['buffer']=$B
 $3 $6:
  G['buffer']=$2
 ${:
  loop(run)
 $3 $u:
  pass
 $! ''
KEYFN=('get_key','getkey','getKey','wait_key','waitkey')
$, findkey():
 $( mn in('ti_system','ti_draw','ti_plotlib'):
  ${:
   m=__import__(mn)
  $3 ImportError:
   $7
  $( fn in KEYFN:
   f=getattr(m,fn,$#)
   if f is $- $#:
    $! keyfun(f)
 $! tibasic()
TINAMES={'ent':'enter','dow':'down','lef':'left','rig':'right',
 'cle':'clear','men':'menu','tri':'trig','hom':'home',
 'ctr':'ctrl','shi':'shift','cen':'center','ret':'$!',
 'squ':'square','spa':'space','sqr':'$O','bac':'backspace'}
$, tibasic():
 ${:
  import ti_system
  ev=ti_system.eval_function
 $3(ImportError,AttributeError):
  $! $#
 ${:
  if ev('ncaskey',0)!=0:
   $! $#
 $3 $6:
  $! $#
 $, wait(x=1):
  c=$q(ev('ncaskey',1))
  s=''
  $( v in(c>>32,(c>>16)&65535,c&65535):
   s+=chr(v)
  s=s.rstrip(' ')or ' '
  $! TINAMES.get(s,s)
 $! wait
$, keyfun(f):
 ${:
  from time import sleep
 $3 ImportError:
  sleep=$#
 mode=[1]
 $, wait(x=1):
  if mode[0]:
   ${:
    $! $p(f(1))
   $3 TypeError:
    mode[0]=0
  $F $B:
   k=f()
   if k:
    $! $p(k)
   if sleep:
    sleep(0.02)
 $! wait
$, color(c):
 d=G['d']
 if G['cmode']==0:
  ${:
   d.set_color(c[0],c[1],c[2])
   $!
  $3 TypeError:
   G['cmode']=1
 d.set_color(c)
$, text(x,y,s,c):
 color(c)
 G['d'].draw_text(x,y+BASE,s)
$, box(x,y,w,h,c):
 color(c)
 G['d'].fill_rect(x,y,w,h)
$, gu_show():
 if G['buffer']:
  G['d'].paint_buffer()
$, wrap(s,n):
 $9=[]
 $F $/(s)>n:
  $9.$%(s[:n])
  s=s[n:]
 $9.$%(s)
 $! $9
$, selected():
 s=G['sel']
 if s is $#:
  $! $#
 k=$/(G['hist'])-1-s//2
 $!(k,'$9' if s%2==0 $& 'in')
$, status():
 if G['msg']:
  $! G['msg']
 n=callname()
 if n:
  _load('cashelp')
  sy=SYN.get(n.lower())
  if sy:
   $! sy.split('\n')[0][:(G['w']-8)//CW]
 a=SET['$l'].upper()
 m=SET['mode'].upper()
 c='REAL' if SET['$D']=='$U' $& 'CPLX'
 $! 'nCAS  '+a+' '+m+' '+c+('   menu: commands' if G.get('gui')$& '')
$, callname():
 chain=[]
 r=G['row']
 $( i,sl in G['path']:
  chain.$%((r,i))
  r=r[i][sl]
 chain.$%((r,G['pos']))
 $( r,p in reversed(chain):
  $:=0
  j=min(p,$/(r))-1
  $F j>=0:
   c=r[j]
   if c==')':
    $:+=1
   $= c=='(':
    if $::
     $:-=1
    $&:
     k=j
     $F k>0 $* $0(r[k-1])is $p $*(r[k-1].isalpha()or r[k-1].isdigit()):
      k-=1
     if k<j:
      $! ''.join(r[k:j])
   j-=1
 $! $#
''',
r'''$, draw():
 d=G['d']
 w=G['w']
 h=G['h']
 color((255,255,255))
 d.fill_rect(0,0,w,h)
 box(0,0,w,LH,C_BAR)
 text(4,0,status(),C_BART)
 wq,aq,dq=meas(G['row'])
 etop=h-(max(LH,aq+dq+2)+2)-2
 avail=etop-LH-4
 sel=selected()
 if avail<LH:
  bl=[]
 $= sel is $#:
  bl=[]
  k=$/(G['hist'])
  hh=0
  $F k>0 $* hh<avail:
   k-=1
   eb=entry_blocks(k)
   hh+=sum([b[2]$( b in eb])
   bl=eb+bl
 $&:
  bl=blocks(max(0,min(sel[0],G.get('hendk',sel[0]))-8))
 if bl:
  if sel is $#:
   end=$/(bl)-1
   start=startfor(bl,end,avail)
  $&:
   idx=[i $( i in $+($/(bl))if(bl[i][3],bl[i][4])==sel]
   a=idx[0]
   b=idx[-1]
   G['tall']=$#
   if sum([bl[i][2]$( i in idx])>avail:
    n=fitfrom(bl,a,avail)-a+1
    st=G.get('stop',0)
    if st=='end' or st>$/(idx)-n:
     st=$/(idx)-n
    G['stop']=max(0,st)
    start=a+G['stop']
    end=fitfrom(bl,start,avail)
    G['tall']=(G['stop'],$/(idx)-n)
   $&:
    end=$/(bl)-1
    hk=G.get('hend')
    $( j in $+($/(bl)):
     if(bl[j][3],bl[j][4])==hk:
      end=j
    start=startfor(bl,end,avail)
    if b>end:
     end=b
     start=startfor(bl,end,avail)
    if a<start:
     start=a
     end=fitfrom(bl,start,avail)
  G['hend']=(bl[end][3],bl[end][4])
  G['hendk']=bl[end][3]
  y=LH+2
  last=$#
  $( i in $+(start,end+1):
   kind,data,bh,k,part=bl[i]
   if last is $- $# $* k!=last:
    box(2,y-1,w-4,1,C_RULE)
   if sel is $- $# $*(k,part)==sel:
    box(0,y,w,bh,C_SEL)
   if kind=='2d':
    r,rw,ra,rd,col=data
    G['ink']=col
    rowdraw(r,4 if part=='in' $& w-6-rw,y+2+ra,$B)
    G['ink']=C_TXT
   $&:
    text(4,y,data[0],data[1])
   last=k
   y+=bh
 G['crow']=ed_row()
 wq,aq,dq=meas(G['row'])
 hgt=max(LH,aq+dq+2)+2
 top=h-hgt-2
 box(0,top-1,w,hgt+3,C_BOX)
 box(0,top-2,w,1,C_DIM)
 base=top+2+max(aq,A_)
 G['cxy']=(0,base,A_,D_)
 rowdraw(G['row'],0,base,$2)
 cx=G['cxy'][0]
 hoff=G.get('hoff',0)
 if cx-hoff>w-16:
  hoff=cx-(w-16)
 if cx-hoff<0:
  hoff=max(0,cx-20)
 G['hoff']=hoff
 cxy=G['cxy']
 rowdraw(G['row'],6-hoff,base,$B)
 G['cxy']=cxy
 if hoff>0:
  box(0,top,5,hgt,C_BOX)
  text(0,base-BASE,'<',C_DIM)
 if wq-hoff>w-12:
  box(w-8,top,8,hgt,C_BOX)
  text(w-7,base-BASE,'>',C_DIM)
 if G['sel']is $#:
  x,y,ca,cd=G['cxy']
  box(x+5-hoff,y-ca+1,2,ca+cd-1,C_CUR)
 gu_show()
$, insert(s,back=0):
 if $- G['row']$* $- G['path']$* s $* s[0]in NEEDANS $* G['hist']:
  ed_chars('ans')
 t=NODETEXT.get(s)
 if t is $- $#:
  ed_chars(t[0])
  ed_node(t[1],t[2])
  $!
 ed_chars(s)
 G['pos']=max(0,G['pos']-back)
$, evaluate(run,s):
 s=closeup(s)
 G['msg']='Working...'
 if G.get('gui'):
  ${:
   draw()
  $3 MemoryError:
   freemem(5)
 bad=$2
 ${:
  $9=run(s)
 $3 $S as ex:
  $9='Error: '+$p(ex)
  bad=$B
 $3 $E:
  $9='Error: Division by zero'
  bad=$B
 $3 MemoryError:
  freemem(5)
  $9='Error: Out of memory (history shortened, undo cleared; variables kept)'
  bad=$B
 $3 RuntimeError:
  $9='Error: Too $4'
  bad=$B
 $3 $u:
  $9='Interrupted'
  bad=$B
 $3 $6 as ex:
  $9='Error: '+$p(ex)
  bad=$B
 G['msg']=''
 if $9 is $#:
  $9=''
 G['hist'].$%((s,$9,bad))
 trimhist(MAXH,HISTCH)
$, freemem(keep):
 G['lay']={}
 G['undo']=[]
 G['tinames']=$#
 G['typing']=$2
 trimhist(keep,500*keep)
 G['sel']=$#
 ${:
  import gc
  gc.collect()
 $3 ImportError:
  pass
$, trimhist(n,chars):
 h=G['hist']
 tot=sum([$/(e[0])+$/(e[1])$( e in h])
 c=G.get('lay',{})
 $F h $*($/(h)>n or(tot>chars $* $/(h)>1)):
  e=h.pop(0)
  tot-=$/(e[0])+$/(e[1])
  c.pop(e[0],$#)
  c.pop(e[1],$#)
$, loop(run):
 $F $B:
  ${:
   step(run)
  $3 MemoryError:
   freemem(3)
   G['msg']='Out of memory: history shortened, undo cleared'
$, step(run):
 draw()
 k=G['key'](1)
 G['msg']=''
 if $- k:
  $!
 typing=$/(k)==1 $* k $- in ENTER
 before=$# if typing $* G.get('typing')$& ed_snap()
 G['typing']=typing
 k=shiftkey(k)
 if k is $#:
  G['msg']='shift  (next key: \u25c4 \u25ba jump, tab back)'
  $!
 if k in JUMP:
  G['sel']=$#
  ed_word(JUMP[k])
  $!
 a=ctrlaction(k)
 if a=='wait':
  G['msg']='ctrl  (next key: blue label)'
  $!
 if a is $- $#:
  doaction(run,a,k)
 $&:
  key(run,k)
 if before is $- $# $* a!=('undo',)$* $v()!=before[3]:
  u=G.setdefault('undo',[])
  u.$%(before)
  tot=sum([$/(x[3])$( x in u])
  $F u $*($/(u)>UNDON or tot>UNDOCH):
   tot-=$/(u.pop(0)[3])
''',
r'''$, key(run,k):
 if k=='esc':
  if G['sel']is $- $#:
   G['sel']=$#
  $= G['row']:
   ed_reset()
  $&:
   $d $u
 $= k in ENTER:
  if G['sel']is $- $#:
   k2,part=selected()
   inp,res,bad=G['hist'][k2]
   G['sel']=$#
   insert(inp if part=='in' $& res.replace('\n ','').replace('\n',''))
  $= $v().strip():
   s=$v()
   ed_reset()
   special(run,s)
 $= k in('up','down')$* G['sel']is $# $* ed_vert(1 if k=='down' $&-1):
  pass
 $= k=='up' $* G['sel']is $- $# $* G.get('tall')$* G['tall'][0]>0:
  G['stop']=G['tall'][0]-1
 $= k=='down' $* G['sel']is $- $# $* G.get('tall')$* G['tall'][0]<G['tall'][1]:
  G['stop']=G['tall'][0]+1
 $= k=='up':
  n=2*$/(G['hist'])
  if n:
   G['sel']=0 if G['sel']is $# $& min(G['sel']+1,n-1)
   G['stop']='end'
   G['tall']=$#
 $= k=='down':
  if G['sel']is $- $#:
   G['sel']=$# if G['sel']==0 $& G['sel']-1
   G['stop']=0
   G['tall']=$#
 $= k=='left':
  G['sel']=$#
  ed_left()
 $= k=='right':
  G['sel']=$#
  ed_right()
 $= k in('del','backspace'):
  G['sel']=$#
  ed_del()
 $= k=='clear':
  G['sel']=$#
  ed_reset()
 $= k in MENU:
  G['sel']=$#
  r=menus()
  if r is $- $#:
   act(run,r)
 $= k in TABKEYS or k in BACKTAB:
  G['sel']=$#
  ed_tab(-1 if k in BACKTAB $& 1)
 $= k in CATKEYS:
  G['sel']=$#
  catalog()
 $= k in TEMPLKEYS:
  G['sel']=$#
  templates()
 $= k in SYMKEYS:
  G['sel']=$#
  gu_symbols()
 $= k=='trig':
  G['sel']=$#
  j=choose('Trig',gu_TRIG)
  if j is $- $#:
   insert(gu_TRIG[j]+')',1)
 $= k in TEXT:
  G['sel']=$#
  t=TEXT[k]
  if t.endswith('('):
   insert(t+')',1)
  $&:
   insert(t)
 $= k in VARKEYS:
  G['sel']=$#
  varlist(run)
 $= $/(k)==1:
  G['sel']=$#
  ed_autoexit(k)
  if $-(k in CLOSERS $* ed_close(k))$* $-(k in ',;' $* ed_cell(k)):
   insert(k)
 $&:
  G['msg']='key '+repr(k)+' $- used'
CTRLKEYS=('ctrl','doc')
CTRL={'(':('ins','[]',1),')':('ins','{}',1),'^':('ins','root(,)',2),
 '^2':('ins','$O()',1),'e^':('ins','ln()',1),'10^':('ins','log10()',1),
 '=':('rel',),'trig':('help',),'del':('clear',),'clear':('clear',),
 '-':('ins','ans',0),'*':('ins','""',1),'/':('ins','()/()',4),
 'enter':('approx',),'var':('ins','->',0),'esc':('undo',),
 'cat':('$e',),'catalog':('$e',),'book':('$e',),
 'template':('ins',':=',0),'templates':('ins',':=',0),'templ':('ins',':=',0),
 'tmpl':('ins',':=',0),'tab':('menu',),'menu':('$e',),
 'left':('home',),'right':('end',)}
DIRECT={'[]':('ins','[]',1),'{}':('ins','{}',1),'""':('ins','""',1),
 '()':('ins','()',1),'\u2248':('approx',),'approx':('approx',),
 'undo':('undo',),'sto':('ins','->',0),'sto\u2192':('ins','->',0),
 'store':('ins','->',0),'\u2254':('ins',':=',0),':=':('ins',':=',0),
 'nroot':('ins','root(,)',2),'root':('ins','root(,)',2),'help':('help',),
 '10^x':('ins','10^',0),'pow10':('ins','10^',0),'10^':('ins','10^',0)}
RELS=(('=','='),('\u2260  $- equal','/='),('<','<'),('>','>'),
 ('\u2264','<='),('\u2265','>='),('|  with','|'),('>>  convert','>>'))
CTRLHELP=('ctrl ( [ ]   ctrl ) { }   ctrl \u00d7 " "',
 'ctrl ^ root   ctrl x\u00b2 \u221a   ctrl \u00f7 fraction',
 'ctrl e^x ln   ctrl 10^x log10',
 'ctrl = \u2260 \u2264 \u2265 | >>   ctrl var \u2192',
 'ctrl (-) ans   ctrl enter \u2248 decimal',
 'ctrl del clear   ctrl esc undo',
 'ctrl \u25c4 \u25ba line start / end',
 'shift \u25c4 \u25ba a word   var your variables',
 'ctrl catalog Symbols   doc = ctrl')
$, ctrlbase(k):
 t=TEXT.get(k,k)
 $! '10^' if k in('10^x','pow10','10^')$& t
$, ctrlaction(k):
 if G.get('ctrl'):
  G['ctrl']=$2
  $! CTRL.get(ctrlbase(k))or CTRL.get(k)or('none',k)
 if k in CTRLKEYS:
  G['ctrl']=$B
  $! 'wait'
 if $/(k)>4 $* k[:4].lower()=='ctrl':
  r=k[4:].lstrip('+-_ ')
  $! CTRL.get(ctrlbase(r))or CTRL.get(r)or('none',k)
 $! DIRECT.get(k)
$, doaction(run,a,k):
 G['sel']=$#
 kind=a[0]
 if kind=='ins':
  insert(a[1],a[2])
 $= kind=='clear':
  ed_reset()
 $= kind in('home','end'):
  G['path']=[]
  G['pos']=0 if kind=='home' $& $/(G['row'])
 $= kind=='undo':
  u=G.get('undo')
  if u:
   ed_restore(u.pop())
 $= kind=='approx':
  s=$v().strip()
  if $- s $* G['hist']:
   s='ans'
  if s:
   ed_reset()
   evaluate(run,'approx('+s+')')
 $= kind=='rel':
  j=choose('Relations',[r[0]$( r in RELS])
  if j is $- $#:
   insert(RELS[j][1])
 $= kind=='$e':
  gu_symbols()
 $= kind=='menu':
  r=menus()
  if r is $- $#:
   act(run,r)
 $= kind=='help':
  panel('ctrl keys','any key to close')
  $( i in $+($/(CTRLHELP)):
   text(10,LH+4+i*LH,CTRLHELP[i],C_TXT)
  gu_show()
  G['key'](1)
 $&:
  G['msg']='ctrl+'+$p(a[1])+' $- used'
$, special(run,s):
 low=s.strip().lower()
 if low in(':keys','keys'):
  keytest()
 $= low in(':clearhist',':clearhistory'):
  G['hist']=[]
  G['undo']=[]
  G['lay']={}
  G['msg']='History $* undo cleared'
 $= low==':free':
  freemem(0)
  G['msg']='Freed: history, undo, ans (variables kept)'
  run(':clearans')
 $= low in('q','quit',':q'):
  $d $u
 $&:
  evaluate(run,s)
$, keytest():
 last=''
 $F $B:
  d=G['d']
  color((255,255,255))
  d.fill_rect(0,0,G['w'],G['h'])
  box(0,0,G['w'],LH,C_BAR)
  text(4,0,'Key test: press keys, esc twice to stop',C_BART)
  text(10,3*LH,'Last key:',C_DIM)
  text(10,4*LH+4,repr(last),C_TXT)
  gu_show()
  k=G['key'](1)
  if k=='esc' $* last=='esc':
   $!
  last=k
''',
r'''$, choose(title,labels,jump=$2,hint=$#):
 n=$/(labels)
 i=0
 $X=G['$X']-1-(1 if hint $& 0)
 top=0
 w=G['w']
 $F $B:
  if i<top:
   top=i
  if i>=top+$X:
   top=i-$X+1
  box(10,LH+4,w-20,($X+1)*LH+6,C_DIM)
  box(11,LH+5,w-22,($X+1)*LH+4,(255,255,255))
  box(11,LH+5,w-22,LH,C_BAR)
  text(16,LH+5,title,C_BART)
  y=2*LH+7
  $( j in $+(top,min(n,top+$X)):
   if j==i:
    box(12,y,w-24,LH,C_SEL)
   key=KEYS[j]if j<$/(KEYS)$* $- jump $& ' '
   text(16,y,key,C_DIM)
   text(34,y,labels[j],C_TXT)
   y+=LH
  if top+$X<n:
   text(w-30,y-LH,'v',C_DIM)
  if hint:
   box(12,y,w-24,LH,C_BAR)
   text(16,y,(hint(i)or '')[:(w-32)//CW],C_BART)
  gu_show()
  k=G['key'](1)
  if k=='up':
   i=(i-1)%n
  $= k=='down':
   i=(i+1)%n
  $= k in ENTER or k=='right':
   $! i
  $= k in('esc','left')or k in MENU:
   $! $#
  $= jump $* $/(k)==1 $* k.isalpha():
   c=k.lower()
   $( d in $+(1,n+1):
    if labels[(i+d)%n][:1].lower()==c:
     i=(i+d)%n
     $R
  $= $- jump $* $/(k)==1 $* k in KEYS[:n]:
   $! KEYS.index(k)
$, menus():
 _load('casmenu')
 n=NFIX
 main=$J(MAIN[:n])+[$#,$#]+$J(MAIN[n:])
 $F $B:
  a=choose('Menu',[m[0]if m $&('Templates','Symbols')[i-n]$( i,m in enumerate(main)])
  if a is $#:
   $! $#
  if a==n:
   templates()
   $! $#
  if a==n+1:
   gu_symbols()
   $! $#
  title,items=main[a]
  b=choose(title,[it[0]$( it in items])
  if b is $- $#:
   $! items[b]
$, act(run,item):
 _load('casmenu')
 label,tpl,prompts=item
 if $- prompts:
  special(run,tpl)
  $!
 $g=[]
 mark='\u0001'
 first=$B
 $( p in prompts:
  d=p[1]
  if d is $#:
   v='[]' if $/(p)>2 $* p[2]=='m' $& ''
   if first:
    v='['+mark+']' if v $& mark
    first=$2
  $&:
   v=d
  $g.$%(v)
 s=fill(tpl,$g)
 i=s.find(mark)
 if i<0:
  i=$/(s)
 $&:
  s=s[:i]+s[i+1:]
 ed_chars(s)
 G['pos']-=$/(s)-i
$, screen(run,nokeys=$B):
 G['gui']=$2
 G['msg']=''
 ${:
  import ti_system
  have=[n $( n in dir(ti_system)if n[0]!='_']
 $3 ImportError:
  have=$#
 print('nCAS screen mode: this OS gives programs no single-key input.')
 if have is $#:
  print('(no ti_system module)')
 $&:
  print('ti_system: '+' '.join(have))
 $X=4
 $F $B:
  hist=G['hist']
  print('-'*30)
  first=max(0,$/(hist)-$X)
  $( k in $+(first,$/(hist)):
   inp,res,bad=hist[k]
   print('#'+$p(k+1)+' '+inp)
   $( r in res.split('\n'):
    print('   '+r)
  print(status()+'  m menu  q quit')
  ${:
   s=input('> ').strip()
  $3(EOFError,$u):
   $! ''
  if s in('q','quit',':q'):
   $! ''
  if s in('m','menu'):
   cmd=pickmenu()
   if $- cmd:
    $7
   print('> '+cmd)
   s=cmd
  if $- s:
   $7
  s=refs(s,hist)
  if s.strip().lower()in(':keys','keys'):
   print('No key reading on this OS.')
   $7
  evaluate(run,s)
$, pickmenu():
 _load('casmenu')
 ${:
  $F $B:
   k=pick('nCAS menu',[m[0]$( m in MAIN])
   if k is $#:
    $! $#
   title,items=MAIN[k]
   j=pick(title,[it[0]$( it in items])
   if j is $#:
    $7
   cmd=build(items[j])
   if cmd:
    $! cmd
 $3 Quit:
  $! $#
$, refs(s,hist):
 $9=''
 i=0
 $F i<$/(s):
  if s[i]=='#' $* i+1<$/(s)$* s[i+1].isdigit():
   j=i+1
   $F j<$/(s)$* s[j].isdigit():
    j+=1
   n=$q(s[i+1:j])
   if 1<=n<=$/(hist)$* $- hist[n-1][2]:
    $9+='('+hist[n-1][1].split('\n')[0]+')'
   $&:
    $9+=s[i:j]
   i=j
  $&:
   $9+=s[i]
   i+=1
 $! $9
TEMPLKEYS=('template','templates','templ','tmpl')
SYMKEYS=('$e','symbol','punc','?!','?!>','palette')
TPLS=('Matrix m\u00d7n','Column vector','Row vector')
SYMS=(
 (';',';',0,'next row in a matrix [1,2;3,4]'),(',',',',0,'separates arguments'),
 ('[ ]','[]',1,'matrix or vector'),('{ }','{}',1,'$J {1,2,3}'),
 ('( )','()',1,'parentheses'),('|','|',0,'with: x^2|x=3'),
 ("'","'",0,"derivative in deSolve: y'"),('" "','""',1,'text'),
 ('=','=',0,'equation'),('\u2260','/=',0,'$- equal'),
 ('<','<',0,'less than'),('>','>',0,'greater than'),
 ('\u2264','<=',0,'less or equal'),('\u2265','>=',0,'greater or equal'),
 (':=',':=',0,'define: f(x):=x^2'),('\u2192','->',0,'store: 5->a'),
 ('^','^',0,'power'),('^2','^2',0,'square'),
 ('^-1','^-1',0,'inverse: [1,2;3,4]^-1'),('\u221a','$O()',1,'square root'),
 ('root','root(,)',2,'n-th root: root(8,3)'),('!','!',0,'factorial'),
 ('\u03c0','\u03c0',0,'pi'),('e','e',0,"Euler's number"),
 ('i','i',0,'imaginary unit'),('\u221e','$P',0,'infinity'),
 ('\u00b0','\u00b0',0,'degrees: sin(30\u00b0)'),('E','E',0,'times 10^: 2E3'),
 ('>>','>>',0,'convert: pi>>Decimal'),('%','%',0,'percent'),
 ('$*',' $* ',0,'both: x>0 $* x<1'),('or',' or ',0,'either'),
 ('$-','$- ',0,'negation'),('ans','ans',0,'last result'),
 (':',':',0,'command: :deg :rad :test'),('_','_',0,'underscore'),
 ('&','&',0,'join text'),('x','x',0,'variable x'),
 ('y','y',0,'variable y'),('t','t',0,'variable t'),
 )
SCOLS=8
$, templates():
 j=choose('Templates',$J(TPLS)+[t[0]$( t in MATHTPL])
 if j is $#:
  $!
 if j>=$/(TPLS):
  insert(MATHTPL[j-$/(TPLS)][1])
  $!
 fix=('','c','r')[j]
 size=gridsize(3 if fix=='c' $& 2,1 if fix=='c' $&(3 if fix=='r' $& 2),fix)
 if size is $#:
  $!
 cells=grid(size[0],size[1])
 if cells is $#:
  $!
 fillpair(cells)
$, fillpair(cells):
 r=ed_row()
 p=G['pos']
 $( a in(p-1,p,p-2):
  if 0<=a $* a+1<$/(r)$* r[a]=='[' $* r[a+1]==']':
   del r[a:a+2]
   p=a
   $R
 node=['mx'+$p($/(cells[0]))]
 $( row in cells:
  $( c in row:
   node.$%($J(c))
 r.insert(p,node)
 G['pos']=p+1
''',
r'''$, gu_symbols():
 n=$/(SYMS)
 $X=(n+SCOLS-1)//SCOLS
 k0=G.get('symk',0)
 w=G['w']
 cw=(w-8)//SCOLS
 ch=LH+6
 $F $B:
  panel('Symbols',SYMS[k0][3])
  y0=LH+4
  $( r in $+($X):
   $( c in $+(SCOLS):
    k=r*SCOLS+c
    if k>=n:
     $R
    x=4+c*cw
    y=y0+r*ch
    box(x+1,y+1,cw-2,ch-2,C_SEL if k==k0 $& C_BOX)
    lab=SYMS[k][0]
    text(x+max(2,(cw-$/(lab)*AW)//2),y+2,lab,C_TXT)
  gu_show()
  key=G['key'](1)
  if key=='esc' or key in SYMKEYS or key in MENU:
   G['symk']=k0
   $!
  if key in ENTER:
   G['symk']=k0
   t=SYMS[k0]
   insert(t[1],t[2])
   $!
  if key=='right':
   k0=(k0+1)%n
  $= key=='left':
   k0=(k0-1)%n
  $= key=='down':
   k0=k0+SCOLS if k0+SCOLS<n $& k0%SCOLS
  $= key=='up':
   if k0-SCOLS>=0:
    k0-=SCOLS
   $&:
    last=($X-1)*SCOLS+k0%SCOLS
    k0=last if last<n $& last-SCOLS
$, panel(title,hint):
 w=G['w']
 h=G['h']
 color((255,255,255))
 G['d'].fill_rect(0,0,w,h)
 box(0,0,w,LH,C_BAR)
 text(4,0,title,C_BART)
 box(0,h-LH-2,w,LH+2,C_BOX)
 text(4,h-LH-2,hint,C_DIM)
$, gridsize(r,c,fix):
 typed=[]
 $F $B:
  panel('Matrix size','arrows or digits, enter OK, esc cancel')
  text(20,2*LH,'Rows: '+$p(r)+'    Columns: '+$p(c),C_TXT)
  cw=min(24,(G['w']-40)//max(c,1))
  ch=min(16,(G['h']-6*LH)//max(r,1))
  $( i in $+(r):
   $( j in $+(c):
    box(20+j*cw,4*LH+i*ch,cw-3,ch-3,C_SEL)
  gu_show()
  k=G['key'](1)
  if k=='esc':
   $! $#
  if k in ENTER:
   $!(r,c)
  if k=='up' $* fix!='r':
   r=min(9,r+1)
  $= k=='down' $* fix!='r':
   r=max(1,r-1)
  $= k=='right' $* fix!='c':
   c=min(9,c+1)
  $= k=='left' $* fix!='c':
   c=max(1,c-1)
  $= $/(k)==1 $* '1'<=k<='9':
   if fix=='c':
    r=$q(k)
   $= fix=='r':
    c=$q(k)
   $&:
    typed.$%($q(k))
    if $/(typed)==1:
     r=typed[0]
    $&:
     c=typed[1]
     typed=[]
$, keytext(k):
 if k in TEXT:
  $! TEXT[k]
 if $/(k)==1:
  $! k
 $! $#
$, grid(r,c):
 cells=[['']*c $( i in $+(r)]
 i=0
 j=0
 w=G['w']
 cw=max(30,min(80,(w-24)//c))
 ncw=max(1,(cw-6)//AW)
 $X=G['$X']
 $F $B:
  panel('Matrix '+$p(r)+'\u00d7'+$p(c),
 'tab/arrows move, enter done, esc cancel')
  top=max(0,i-$X+2)
  y0=LH+6
  nshow=min(r-top,$X-1)
  box(8,y0,2,nshow*(LH+4),C_TXT)
  box(8,y0,5,2,C_TXT)
  box(8,y0+nshow*(LH+4)-2,5,2,C_TXT)
  x1=14+c*cw
  box(x1,y0,2,nshow*(LH+4),C_TXT)
  box(x1-3,y0,5,2,C_TXT)
  box(x1-3,y0+nshow*(LH+4)-2,5,2,C_TXT)
  $( a in $+(top,top+nshow):
   y=y0+(a-top)*(LH+4)
   $( b in $+(c):
    x=14+b*cw
    cur=(a==i $* b==j)
    box(x+1,y+1,cw-4,LH+2,C_SEL if cur $& C_BOX)
    t=cells[a][b]
    if $/(t)>ncw:
     t=t[-ncw:]
    text(x+3,y+2,t,C_TXT)
    if cur:
     box(x+3+$/(t)*AW,y+3,2,LH-2,C_CUR)
  gu_show()
  k=G['key'](1)
  if k=='esc':
   $! $#
  if k in ENTER:
   $! cells
  if k=='tab' or k=='right':
   j+=1
   if j==c:
    j=0
    i=(i+1)%r
  $= k=='left':
   j-=1
   if j<0:
    j=c-1
    i=(i-1)%r
  $= k=='down':
   i=(i+1)%r
  $= k=='up':
   i=(i-1)%r
  $= k in('del','backspace'):
   cells[i][j]=cells[i][j][:-1]
  $= k=='clear':
   cells[i][j]=''
  $&:
   a=ctrlaction(k)
   if a is $- $# $* a!='wait' $* a[0]=='ins':
    t=a[1][:$/(a[1])-a[2]]
   $= a is $- $#:
    t=$#
   $&:
    t=keytext(k)
   if t is $- $#:
    cells[i][j]+=t
A_=13
D_=4
AX=5
RAISE=8
LOWER=6
NODETEXT={'^':('','pow',''),'^2':('','pow','2'),'^-1':('','pow','-1'),
 '$O()':('','$O',''),'root(,)':('','root',''),
 '()/()':('','frac',''),'$H()':('','$H',''),
 'e^':('e','pow',''),'10^':('10','pow',''),
 '$N()':('','$q',''),'$N(,,,)':('','dint',''),
 'd()':('','der','')}
MATHTPL=(('Fraction','()/()'),('Power  x^n','^'),('Square root','$O()'),
 ('n-th root','root(,)'),('Absolute value','$H()'),('e^x','e^'),
 ('Integral  \u222b f dx','$N()'),('Definite $N  \u222b[a,b]','$N(,,,)'),
 ('Derivative  d/dx','d()'))
gu_CALC={'$q':(2,2,1),'dint':(4,4,1),'der':(2,1,2)}
EXITCHARS='+-*/=<>,)'
$, ed_reset():
 G['row']=[]
 G['path']=[]
 G['pos']=0
 G['hoff']=0
$, ed_row():
 r=G['row']
 $( i,sl in G['path']:
  r=r[i][sl]
 $! r
$, ed_parent():
 r=G['row']
 $( i,sl in G['path'][:-1]:
  r=r[i][sl]
 $! r,r[G['path'][-1][0]]
$, ed_chars(s):
 r=ed_row()
 p=G['pos']
 $( c in s:
  r.insert(p,c)
  p+=1
 G['pos']=p
$, ed_node(kind,pre=''):
 r=ed_row()
 p=G['pos']
 if kind in gu_CALC:
  n,var,first=gu_CALC[kind]
  node=[kind]+[[]$( i in $+(n)]
  node[var].$%('x')
  r.insert(p,node)
  G['path'].$%((p,first))
  G['pos']=0
  $!
 n=3 if kind in('frac','root')$& 2
 node=[kind]+[[]$( i in $+(n-1)]
 $( c in pre:
  node[1].$%(c)
 r.insert(p,node)
 if pre:
  G['pos']=p+1
 $&:
  G['path'].$%((p,1))
  G['pos']=0
$, ed_empty(node):
 $( sl in node[1:]:
  if sl:
   $! $2
 $! $B
$, ed_right():
 r=ed_row()
 p=G['pos']
 if p<$/(r):
  if $0(r[p])is $p:
   G['pos']=p+1
  $&:
   G['path'].$%((p,1))
   G['pos']=0
 $= G['path']:
  i,sl=G['path'][-1]
  par,node=ed_parent()
  if sl+1<$/(node):
   G['path'][-1]=(i,sl+1)
   G['pos']=0
  $&:
   G['path'].pop()
   G['pos']=i+1
$, ed_left():
 r=ed_row()
 p=G['pos']
 if p>0:
  if $0(r[p-1])is $p:
   G['pos']=p-1
  $&:
   node=r[p-1]
   G['path'].$%((p-1,$/(node)-1))
   G['pos']=$/(node[-1])
 $= G['path']:
  i,sl=G['path'][-1]
  par,node=ed_parent()
  if sl>1:
   G['path'][-1]=(i,sl-1)
   G['pos']=$/(node[sl-1])
  $&:
   G['path'].pop()
   G['pos']=i
$, ed_vert(d):
 if $- G['path']:
  $! $2
 i,sl=G['path'][-1]
 par,node=ed_parent()
 k=node[0]
 if k in('frac','root'):
  t=2 if d>0 $& 1
  if t!=sl:
   G['path'][-1]=(i,t)
   G['pos']=min(G['pos'],$/(node[t]))
 $= k=='pow' $* d>0:
  G['path'].pop()
  G['pos']=i+1
 $= k[:2]=='mx':
  t=sl+d*$q(k[2:])
  if 1<=t<$/(node):
   G['path'][-1]=(i,t)
   G['pos']=min(G['pos'],$/(node[t]))
 $= k=='dint':
  t=2 if d<0 $& 1
  if t!=sl:
   G['path'][-1]=(i,t)
   G['pos']=$/(node[t])
 $! $B
''',
r'''$, ed_del():
 r=ed_row()
 p=G['pos']
 if p>0:
  it=r[p-1]
  if $0(it)is $p or ed_empty(it):
   del r[p-1]
   G['pos']=p-1
  $&:
   G['path'].$%((p-1,$/(it)-1))
   G['pos']=$/(it[-1])
 $= G['path']:
  i,sl=G['path'].pop()
  par=ed_row()
  if ed_empty(par[i]):
   del par[i]
  G['pos']=i
$, ed_autoexit(c):
 if $- G['path']or c $- in EXITCHARS:
  $!
 par,node=ed_parent()
 r=ed_row()
 if node[0]!='pow' or G['pos']!=$/(r)or $- r:
  $!
 $:=0
 $( it in r:
  if it=='(':
   $:+=1
  $= it==')':
   $:-=1
 if $:<=0:
  G['pos']=G['path'].pop()[0]+1
CLOSERS={')':'(',']':'[','}':'{'}
CLOSEWRAP=('$O','$H','root','der')
$, ed_close(c):
 r=ed_row()
 p=G['pos']
 o=CLOSERS[c]
 $:=0
 $( it in r:
  if it==o:
   $:+=1
  $= it==c:
   $:-=1
 if $:>0:
  $! $2
 if p<$/(r)$* r[p]==c:
  G['pos']=p+1
  $! $B
 if G['path']$* ed_parent()[1][0][:2]=='mx':
  if c==']' $* p==$/(r)or c==')':
   G['pos']=G['path'].pop()[0]+1
   if c==')' $* $- ed_close(c):
    insert(c)
   $! $B
 if c==')' $* G['path']$* p==$/(r):
  par,node=ed_parent()
  i,sl=G['path'][-1]
  if node[0]in CLOSEWRAP $* sl==$/(node)-1:
   G['path'].pop()
   G['pos']=i+1
   $! $B
 $! $2
$, ed_cell(c):
 if $- G['path']:
  $! $2
 par,node=ed_parent()
 if node[0][:2]!='mx':
  $! $2
 $:=0
 $( it in ed_row()[:G['pos']]:
  if it in('(','[','{'):
   $:+=1
  $= it in(')',']','}'):
   $:-=1
 if $:>0:
  $! $2
 i,sl=G['path'][-1]
 nc=$q(node[0][2:])
 t=sl+1 if c==',' $&((sl-1)//nc+1)*nc+1
 if t>=$/(node):
  G['path'].pop()
  G['pos']=i+1
 $&:
  G['path'][-1]=(i,t)
  G['pos']=$/(node[t])
 $! $B
$, ed_wch(it):
 $! $0(it)is $p $*(it.isalpha()or it.isdigit()or it in '._')
$, ed_word(d):
 r=ed_row()
 p=G['pos']
 if d>0:
  if p>=$/(r):
   ed_right()
   $!
  q=p+1
  if ed_wch(r[p]):
   $F q<$/(r)$* ed_wch(r[q]):
    q+=1
   if q<$/(r)$* r[q]=='(':
    q+=1
  G['pos']=q
 $&:
  if p==0:
   ed_left()
   $!
  q=p-1
  if r[q]=='(' $* q>0 $* ed_wch(r[q-1]):
   q-=1
  if ed_wch(r[q]):
   $F q>0 $* ed_wch(r[q-1]):
    q-=1
  G['pos']=q
SHIFTKEYS=('shift',)
JUMP={'shift+left':-1,'shift+right':1}
$, shiftkey(k):
 if G.get('shift'):
  G['shift']=$2
  if k in('left','right'):
   $! 'shift+'+k
  if k=='tab':
   $! 'shift+tab'
  $! k.upper()if $/(k)==1 $& k
 if k in SHIFTKEYS:
  G['shift']=$B
  $! $#
 low=k.lower()
 if low[:5]=='shift' $* $/(low)>5:
  $a=low[5:].lstrip('+-_ ')
  if $a in('left','right','tab'):
   $! 'shift+'+$a
 $! k
VARKEYS=('var','vars')
$, varlist(run):
 items=[]
 if G['hist']$* $- G['hist'][-1][2]$* G['hist'][-1][1]$- in('Done',''):
  items.$%(('ans = '+G['hist'][-1][1].replace('\n',' '),'ans',0))
 ${:
  txt=run(':vars')
 $3 $6:
  txt=''
 $( ln in txt.split('\n'):
  j=ln.find(' = ')
  if j>0:
   $A=ln[:j]
   f=$A.find('(')
   items.$%((ln,$A[:f]+'()' if f>0 $& $A,1 if f>0 $& 0))
 if $- items:
  G['msg']='No variables yet: a:=5 or 5\u2192a stores one'
  $!
 wmax=(G['w']-50)//AW
 j=choose('Variables',[t[0]if $/(t[0])<=wmax $& t[0][:wmax-1]+'\u2026' $( t in items])
 if j is $- $#:
  insert(items[j][1],items[j][2])
$, $v(row=$#):
 if row is $#:
  row=G['row']
 $9=''
 $( it in row:
  if $0(it)is $p:
   $9+=it
   $7
  k=it[0]
  if k=='frac':
   f=grp($v(it[1]),$B)+'/'+grp($v(it[2]),$2)
   $9+=f if $/(row)==1 $& '('+f+')'
  $= k=='pow':
   e=$v(it[1])
   $9+='^'+(e if e.isdigit()or($/(e)==1 $* e.isalpha())or enclosed(e)
 $& '('+e+')')
  $= k=='$O':
   $9+='$O('+$v(it[1])+')'
  $= k=='root':
   $9+='root('+$v(it[2])+','+$v(it[1])+')'
  $= k=='$H':
   $9+='$H('+$v(it[1])+')'
  $= k=='$q':
   $9+='$N('+$v(it[1])+','+$v(it[2])+')'
  $= k=='dint':
   lo,hi=$v(it[1]),$v(it[2])
   $9+='$N('+$v(it[3])+','+$v(it[4])
   $9+=(','+lo+','+hi+')')if lo or hi $& ')'
  $= k=='der':
   $9+='d('+$v(it[2])+','+$v(it[1])+')'
  $= k=='logb':
   $9+='log('+$v(it[2])+','+$v(it[1])+')'
  $= k[:2]=='mx':
   $9+='['+';'.join([','.join([$v(c)or '0' $( c in row])$( row in mxrows(it)])+']'
 $! $9
$, mxrows(it):
 nc=$q(it[0][2:])
 $![it[1+i:1+i+nc]$( i in $+(0,$/(it)-1,nc)]
$, enclosed(s):
 if $/(s)<2 or s[0]!='(' or s[-1]!=')':
  $! $2
 $:=0
 $( i in $+($/(s)):
  if s[i]=='(':
   $:+=1
  $= s[i]==')':
   $:-=1
   if $:==0 $* i<$/(s)-1:
    $! $2
 $! $B
$, grp(s,num):
 ok=s!=''
 digits=$B
 $( c in s:
  if $-(c.isdigit()or c=='.'):
   digits=$2
  if $-(c.isdigit()or c=='.' or c.isalpha()):
   ok=$2
 if ok $* $- digits $* $- s.isalpha():
  ok=$2
 i=s.find('(')
 if i>0 $* s[:i].isalpha()$* enclosed(s[i:]):
  ok=$B
 $! s if ok or enclosed(s)$& '('+s+')'
$, ed_cp(row):
 $![it if $0(it)is $p $&[it[0]]+[ed_cp(r)$( r in it[1:]]$( it in row]
$, ed_snap():
 $!(ed_cp(G['row']),$J(G['path']),G['pos'],$v())
$, ed_restore(sn):
 G['row']=sn[0]
 G['path']=sn[1]
 G['pos']=sn[2]
$, meas(row):
 if $- row:
  $!(9,A_,D_)
 w=0
 a=A_
 d=D_
 $( it in row:
  iw,ia,idd=measi(it)
  w+=iw
  a=max(a,ia)
  d=max(d,idd)
 $!(w,a,d)
''',
r'''$, measi(it):
 if $0(it)is $p:
  $!(CW,A_,D_)
 k=it[0]
 if k=='frac':
  w1,a1,d1=meas(it[1])
  w2,a2,d2=meas(it[2])
  $!(max(w1,w2)+6,AX+2+a1+d1,max(D_,2-AX+a2+d2))
 if k=='pow':
  w,a,d=meas(it[1])
  $!(w+2,max(A_,RAISE+a),max(D_,d-RAISE))
 if k=='$H':
  w,a,d=meas(it[1])
  $!(w+7,a,d)
 if k=='mat' or k[:2]=='mx':
  cw,ra,rd,W,H=matsize(it[1]if k=='mat' $& mxrows(it))
  asc=H//2+AX
  $!(W,asc+1,H-asc+1)
 if k=='root':
  w,a,d=meas(it[2])
  wi,ai,di=meas(it[1])
  $!(wi+w+11,max(a+3,RAISE+ai),d)
 if k=='logb':
  wb,ab,db=meas(it[1])
  w,a,d=meas(it[2])
  $!(3*CW+wb+1+2*CW+w,max(a,ab-LOWER),max(d,LOWER+db))
 if k in gu_CALC:
  $! calcbox(it)[0]
 w,a,d=meas(it[1])
 $!(w+11,a+3,d)
$, calcbox(it):
 k=it[0]
 if k=='der':
  wx,ax,dx=meas(it[1])
  wf,af,df=meas(it[2])
  W=CW+wx+6
  fa=AX+2+A_+D_
  fd=max(D_,2-AX+ax+dx)
  $!((W+2*CW+wf+2,max(fa,af),max(fd,df)),W)
 f,x=(it[1],it[2])if k=='$q' $&(it[3],it[4])
 wf,af,df=meas(f)
 wx,ax,dx=meas(x)
 a=max(af,A_)+2
 d=max(df,D_)+2
 wb=0
 A=a
 D=d
 if k=='dint':
  wl,al,dl=meas(it[1])
  wh,ah,dh=meas(it[2])
  wb=max(wl,wh)+1
  A=a+1+ah+dh
  D=d+1+al+dl
 $!((9+wb+wf+3+CW+wx,A,D),(a,d,wb))
$, line(x1,y1,x2,y2):
 color(G.get('ink',C_TXT))
 ${:
  G['d'].draw_line(x1,y1,x2,y2)
 $3 $6:
  pass
$, rowdraw(row,x,y,dr):
 cur=row is G['crow']
 if $- row:
  if dr:
   box(x+1,y-A_+3,7,1,C_DIM)
   box(x+1,y+D_-1,7,1,C_DIM)
   box(x+1,y-A_+3,1,A_+D_-3,C_DIM)
   box(x+7,y-A_+3,1,A_+D_-3,C_DIM)
  if cur:
   G['cxy']=(x+2,y,A_,D_)
  $! 9
 x0=x
 $( i in $+($/(row)):
  if cur $* i==G['pos']:
   G['cxy']=(x,y,A_,D_)
  x+=itemdraw(row[i],x,y,dr)
 if cur $* G['pos']==$/(row):
  G['cxy']=(x,y,A_,D_)
 $! x-x0
$, itemdraw(it,x,y,dr):
 ink=G.get('ink',C_TXT)
 if $0(it)is $p:
  if dr:
   text(x,y-BASE,it,ink)
  $! CW
 k=it[0]
 if k=='frac':
  w1,a1,d1=meas(it[1])
  w2,a2,d2=meas(it[2])
  W=max(w1,w2)+6
  by=y-AX
  if dr:
   box(x+1,by,W-2,1,ink)
  rowdraw(it[1],x+(W-w1)//2,by-2-d1,dr)
  rowdraw(it[2],x+(W-w2)//2,by+2+a2,dr)
  $! W
 if k=='pow':
  $! rowdraw(it[1],x+1,y-RAISE,dr)+2
 if k=='mat' or k[:2]=='mx':
  $X=it[1]if k=='mat' $& mxrows(it)
  cw,ra,rd,W,H=matsize($X)
  top=y-(H//2+AX)
  if dr:
   $( bx,tx in((x+1,x+1),(x+W-2,x+W-4)):
    box(bx,top,1,H,ink)
    box(tx,top,3,1,ink)
    box(tx,top+H-1,3,1,ink)
  cy=top
  gap=mxgap($X)
  $( i in $+($/($X)):
   cx=x+5
   r=$X[i]
   $( j in $+($/(r)):
    w2=meas(r[j])[0]
    rowdraw(r[j],cx+(cw[j]-w2)//2,cy+ra[i],dr)
    cx+=cw[j]+8
   cy+=ra[i]+rd[i]+gap
  $! W
 if k in gu_CALC:
  $! calcdraw(it,x,y,dr,ink)
 if k=='logb':
  if dr:
   $( j in $+(3):
    text(x+j*CW,y-BASE,'log'[j],ink)
  xa=x+3*CW+rowdraw(it[1],x+3*CW,y+LOWER,dr)+1
  if dr:
   text(xa,y-BASE,'(',ink)
  wa=rowdraw(it[2],xa+CW,y,dr)
  if dr:
   text(xa+CW+wa,y-BASE,')',ink)
  $! xa+2*CW+wa-x
 xi=x
 if k=='root':
  xi+=rowdraw(it[1],x,y-RAISE,dr)
  rad=it[2]
 $&:
  rad=it[1]
 w,a,d=meas(rad)
 if k=='$H':
  if dr:
   box(xi+1,y-a,1,a+d,ink)
   box(xi+w+5,y-a,1,a+d,ink)
  rowdraw(rad,xi+3,y,dr)
  $! xi-x+w+7
 if dr:
  top=y-a-2
  line(xi,y-4,xi+2,y-5)
  line(xi+2,y-5,xi+4,y+d-1)
  line(xi+4,y+d-1,xi+8,top)
  line(xi+8,top,xi+10+w,top)
 rowdraw(rad,xi+9,y,dr)
 $! xi-x+w+11
$, calcdraw(it,x,y,dr,ink):
 k=it[0]
 (W,A,D),geo=calcbox(it)
 if k=='der':
  fw=geo
  wx=meas(it[1])[0]
  by=y-AX
  if dr:
   box(x+1,by,fw-2,1,ink)
   text(x+(fw-CW)//2,by-2-D_-BASE,'d',ink)
   text(x+3,by+2+A_-BASE,'d',ink)
  rowdraw(it[1],x+3+CW,by+2+A_,dr)
  xf=x+fw+1
  if dr:
   text(xf,y-BASE,'(',ink)
  wf=rowdraw(it[2],xf+CW,y,dr)
  if dr:
   text(xf+CW+wf,y-BASE,')',ink)
  $! W
 a,d,wb=geo
 top=y-a
 bot=y+d
 if dr:
  line(x+5,top+2,x+3,bot-2)
  line(x+5,top+2,x+6,top)
  line(x+6,top,x+8,top+1)
  line(x+3,bot-2,x+2,bot)
  line(x+2,bot,x,bot-1)
 xb=x+9
 if k=='dint':
  wl,al,dl=meas(it[1])
  wh,ah,dh=meas(it[2])
  rowdraw(it[2],xb,top-1-dh,dr)
  rowdraw(it[1],xb,bot+1+al,dr)
  f,v=it[3],it[4]
 $&:
  f,v=it[1],it[2]
 xf=xb+wb
 wf=rowdraw(f,xf,y,dr)
 if dr:
  text(xf+wf+3,y-BASE,'d',ink)
 rowdraw(v,xf+wf+3+CW,y,dr)
 $! W
$, catalog():
 _load('cashelp')
 names=[]
 $( key,title,words in CATS:
  if key in('conv','cmd'):
   $7
  $( wd in words.split():
   if wd[0].isalpha()$* wd $- in names $* okname(wd):
    names.$%(wd)
 names.sort(key=$; t:t.lower())
 $, hint(i):
  sy=SYN.get(names[i].lower())
  $! sy.split('\n')[0]if sy $& names[i]+'(...)'
 j=choose('Catalog: $0 a letter',names,$B,hint)
 if j is $- $#:
  insert(names[j]+'()',1)
$, okname(wd):
 $( c in wd:
  if $-(c.isalpha()or c.isdigit()or c=='_'):
   $! $2
 $! $B
$, ed_stops():
 $9=[]
 $, walk(row,path):
  $( i in $+($/(row)+1):
   $9.$%((path,i,(i>0 $* row[i-1]in(',','|'))or(bool(path)$* i==$/(row))))
   if i<$/(row)$* $0(row[i])is $- $p:
    $( sl in $+(1,$/(row[i])):
     walk(row[i][sl],path+[(i,sl)])
 walk(G['row'],[])
 $! $9
$, ed_tab(d):
 ps=ed_stops()
 cur=0
 $( j in $+($/(ps)):
  if ps[j][0]==G['path']$* ps[j][1]==G['pos']:
   cur=j
 t=$/(ps)-1 if d>0 $& 0
 if d>0:
  $( j in $+(cur+1,$/(ps)):
   if ps[j][2]:
    t=j
    $R
 $&:
  $( j in $+(cur-1,-1,-1):
   if ps[j][2]:
    t=j
    $R
 G['path']=$J(ps[t][0])
 G['pos']=ps[t][1]
SAFE='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_+-*/^().,;=<>{}[]!| \u221a\u03c0\u221e\u2260\u2264\u2265\u03b8\u222b'
SHOW={'pi':'\u03c0','$P':'\u221e','theta':'\u03b8'}
SHOWF={'sumseq':'\u03a3','prodseq':'\u03a0','$N':'\u222b'}
REL2={'=':'=','/=':'\u2260','<':'<','>':'>','<=':'\u2264','>=':'\u2265'}
DOT='\u00b7'
$, anyfunc(n):
 $! $B
''',
r'''$, tolayout(s):
 c=G.setdefault('lay',{})
 if s in c:
  $! c[s]
 t=s.replace('\n ','').replace('\n','')
 ok=t!='' $* $/(t)<400
 $( ch in t:
  if ch $- in SAFE:
   ok=$2
   $R
 if ok:
  u=t.replace(' $* ','').replace(' or ','').replace(' xor ','').replace('$- ','')
  if ' ' in u:
   ok=$2
 r=$#
 if ok:
  ${:
   r=[]
   lay(parse(t,anyfunc),r)
   w,a,d=meas(r)
   r=(r,w,a,d)
  $3 $6:
   r=$#
 if $/(c)>60:
  keep={}
  $( e in G.get('hist',[])[-10:]:
   $( t2 in e[:2]:
    if t2 in c:
     keep[t2]=c[t2]
  c.clear()
  c.update(keep)
 c[s]=r
 $! r
$, prec(t):
 if $0(t)is $- $1:
  $! 5
 h=t[0]
 if h in('+','-'):
  $! 1
 if h in('*','$m'):
  $! 2
 if h=='^':
  $! 4
 if h in REL2:
  $! 0
 if h in('$*','or','xor','$-'):
  $!-1
 if h=='|':
  $!-2
 $! 5
$, layp(t,$9,need):
 if need:
  $9.$%('(')
  lay(t,$9)
  $9.$%(')')
 $&:
  lay(t,$9)
$, sublay(t):
 r=[]
 lay(t,r)
 $! r
$, lay(t,$9):
 tt=$0(t)
 if tt is $q:
  $9.$}($J($p(t)))
  $!
 if tt is $C:
  $9.$}($J(fmt(t)))
  $!
 if tt is $p:
  $9.$}($J(SHOW.get(t,t)))
  $!
 h=t[0]
 if h=='+' or h=='-':
  lay(t[1],$9)
  $9.$%(h)
  layp(t[2],$9,prec(t[2])<=(1 if h=='-' $& 0)
 or($0(t[2])is $1 $* t[2][0]=='$m'))
 $= h=='*':
  layp(t[1],$9,prec(t[1])<2)
  $9.$%(DOT)
  layp(t[2],$9,prec(t[2])<2 or($0(t[2])is $1 $* t[2][0]=='$m'))
 $= h=='$m':
  $9.$%('-')
  layp(t[1],$9,prec(t[1])<=1)
 $= h=='/':
  $9.$%(['frac',sublay(t[1]),sublay(t[2])])
 $= h=='^':
  b=t[1]
  need=prec(b)<5 or($0(b)is $1 $*(b[0]=='/' or(b[0]=='call' $* b[1]in('$O','root'))))
  layp(b,$9,need)
  $9.$%(['pow',sublay(t[2])])
 $= h=='call':
  $A=t[1]
  $L=t[2:]
  if $A=='$O' $* $/($L)==1:
   $9.$%(['$O',sublay($L[0])])
  $= $A=='root' $* $/($L)==2:
   $9.$%(['root',sublay($L[1]),sublay($L[0])])
  $= $A=='$H' $* $/($L)==1:
   $9.$%(['$H',sublay($L[0])])
  $= $A=='$N' $* $/($L)==2:
   $9.$%(['$q',sublay($L[0]),sublay($L[1])])
  $= $A=='$N' $* $/($L)==4:
   $9.$%(['dint',sublay($L[2]),sublay($L[3]),sublay($L[0]),sublay($L[1])])
  $= $A=='d' $* $/($L)==2:
   $9.$%(['der',sublay($L[1]),sublay($L[0])])
  $= $A=='log' $* $/($L)==2:
   $9.$%(['logb',sublay($L[1]),sublay($L[0])])
  $= $A=='log10' $* $/($L)==1:
   $9.$%(['logb',$J('10'),sublay($L[0])])
  $= $A=='log' $* $/($L)==1:
   $9.$}($J('ln('))
   lay($L[0],$9)
   $9.$%(')')
  $&:
   nm=SHOWF.get($A)if OPT['uni']$& $#
   $9.$}($J(nm or tiname($A)))
   $9.$%('(')
   $( i in $+($/($L)):
    if i:
     $9.$%(',')
    lay($L[i],$9)
   $9.$%(')')
 $= h=='$J':
  $9.$%('{')
  $( i in $+(1,$/(t)):
   if i>1:
    $9.$%(',')
   lay(t[i],$9)
  $9.$%('}')
 $= h=='mat':
  $9.$%(['mat',[[sublay(c)$( c in r[1:]]$( r in t[1:]]])
 $= h in REL2:
  lay(t[1],$9)
  $9.$}($J(REL2[h]))
  lay(t[2],$9)
 $= h in('$*','or','xor'):
  lay(t[1],$9)
  $9.$}($J(' '+h+' '))
  lay(t[2],$9)
 $= h=='|':
  layp(t[1],$9,prec(t[1])<=0)
  $9.$%('|')
  lay(t[2],$9)
 $= h=='$-':
  $9.$}($J('$- '))
  layp(t[1],$9,prec(t[1])<0)
 $= h=='!':
  layp(t[1],$9,prec(t[1])<5 or $0(t[1])is $1 $* t[1][0]=='/')
  $9.$%('!')
 $&:
  $d $T('no 2D form')
$, tiname($A):
 c=G.get('tinames')
 if c is $#:
  _load('cashelp')
  c={}
  $( key,title,words in CATS:
   $( wd in words.split():
    c[wd.lower()]=wd
  c.update(TINAME)
  G['tinames']=c
 $! c.get($A,$A)
$, matsize($X):
 nc=max([$/(r)$( r in $X])
 cw=[0]*nc
 ra=[]
 rd=[]
 $( r in $X:
  a=A_
  d=D_
  $( j in $+($/(r)):
   w,ca,cd=meas(r[j])
   cw[j]=max(cw[j],w)
   a=max(a,ca)
   d=max(d,cd)
  ra.$%(a)
  rd.$%(d)
 W=sum(cw)+8*(nc-1)+10
 H=sum(ra)+sum(rd)+mxgap($X)*($/($X)-1)
 $! cw,ra,rd,W,H
$, mxgap($X):
 $! 7 if $/($X)<=5 $& 2
$, blocks(first=0):
 $9=[]
 $( k in $+(first,$/(G['hist'])):
  $9+=entry_blocks(k)
 $! $9
$, entry_blocks(k):
 $9=[]
 n=G['wrap']
 w=G['w']
 inp,res,bad=G['hist'][k]
 $( part,s,col in(('in',inp,C_TXT),('$9',res,C_ERR if bad $& C_RES)):
  lt=$# if bad $& tolayout(s)
  if lt is $- $#:
   r,rw,ra,rd=lt
   if rw<=w-10 $* ra+rd+4<=G['h']-3*LH-8:
    $9.$%(('2d',(r,rw,ra,rd,col),ra+rd+4,k,part))
    $7
  pre='  ' if part=='$9' $& ''
  $( line in s.split('\n'):
   $( t in wrap(line,n-$/(pre)):
    $9.$%(('txt',(pre+t,col),LH,k,part))
 $! $9
$, startfor(bl,end,avail):
 hh=0
 i=end
 $F i>=0 $* hh+bl[i][2]<=avail:
  hh+=bl[i][2]
  i-=1
 $! min(i+1,end)
$, fitfrom(bl,start,avail):
 hh=0
 i=start
 $F i<$/(bl)$* hh+bl[i][2]<=avail:
  hh+=bl[i][2]
  i+=1
 $! max(start,i-1)
''',)
del _x
startgui()
