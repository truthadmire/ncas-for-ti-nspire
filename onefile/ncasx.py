# ncasx - nCAS exact calculator for TI-Nspire CX II. Run it (ctrl+R), type an expression; q quits.
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
_W={'!': 'return', '#': 'self', '%': 'isnode', '&': 'append', '(': 'type', ')': 'and', '*': 'None', '+': 'else', ',': 'complex', '-': 'float', '.': 'def', '/': 'tuple', '0': 'isnum', '1': 'isconst', '2': 'not', '3': 'math', '4': 'for', '5': 'FSIMP', '6': 'False', '7': 'CASError', '8': 'continue', '9': 'undef', ':': 'coef_rest', ';': 'name', '<': 'ZeroDivisionError', '=': 'nsign', '>': 'while', '?': 'args', '@': 'lambda', 'A': 'mul', 'B': 'isreal_expr', 'C': 'mul_list', 'D': 'startswith', 'E': 'P_ATOM', 'F': 'add_list', 'G': 'coef', 'H': 'rest', 'I': 'OverflowError', 'J': 'except', 'K': 'terms', 'L': 'elif', 'M': 'ValueError', 'N': 'cmath', 'O': 'sqrt', 'P': 'keep', 'Q': 'int', 'R': 'True', 'S': 'hasfloat', 'T': 'inf', 'U': 'isop', 'V': 'rationalize_inv', 'W': 'expand_mul', 'X': 'facs', 'Y': 'raise', 'Z': 'vals', '[': 'HALF', ']': 'len', '^': 'arcsin', '_': 'expand', '`': 'expand_pow', 'a': 'str', 'b': 'arctan', 'c': 'num', 'd': 'israt', 'e': 'isneg', 'f': 'list', 'g': 'out', 'h': 'real', 'i': 'fromcomplex', 'j': 'range', 'k': 'P_PROD', 'l': 'arccos', 'm': 'nmul', 'n': 'floor', 'o': 'SPECIAL', 'p': 'reim_generic', 'q': 'nxt', 'r': 'parts', 's': 'imag', 't': 'neg', 'u': 'isfunc', 'v': 'radorder', 'w': 'TypeError', 'x': 'arcsinh', 'y': 'nval', 'z': 'outs', '{': 'fvalc', '|': 'isposconst', '}': 'nfloor', '~': 'trig_table'}
_x(r'''import $3
class $7(Exception):
 pass
class ResourceLimit($7):
 pass
$. err(msg):
 $Y $7(msg)
MAXTERMS=2000
MAXCELLS=2500
MAXLEN=5000
$. toobig(what):
 $Y ResourceLimit('Resource limit: '+what)
$. cells(r,c):
 if $2(isint(r)$) isint(c))or r<1 or c<1:
  err('Dimensions must be positive integers')
 if r*c>MAXCELLS:
  toobig('a %dx%d matrix has more than %d entries'%(r,c,MAXCELLS))
CONSTS=('pi','e','i')
$o=('pi','e','i','$T','$9','true','false')
$. igcd(a,b):
 if a<0:
  a=-a
 if b<0:
  b=-b
 $> b:
  a,b=b,a%b
 $! a
$. ilcm(a,b):
 if a==0 or b==0:
  $! 0
 $! abs(a//igcd(a,b)*b)
$. Q(n,d=1):
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
$[=('Q',1,2)
$. isq(x):
 $! $((x)is $/ $) x[0]=='Q'
$. isint(x):
 $! $((x)is $Q
$. isfl(x):
 $! $((x)is $-
$. $d(x):
 t=$((x)
 $! t is $Q or(t is $/ $) x[0]=='Q')
$. $0(x):
 t=$((x)
 $! t is $Q or t is $- or(t is $/ $) x[0]=='Q')
$. nd(x):
 if $((x)is $Q:
  $! x,1
 $! x[1],x[2]
$. tofl(x):
 t=$((x)
 if t is $-:
  $! x
 if t is $Q:
  $! $-(x)
 $! x[1]/x[2]
$. nadd(a,b):
 ta=$((a)
 tb=$((b)
 if ta is $Q $) tb is $Q:
  $! a+b
 if ta is $- or tb is $-:
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
$. $m(a,b):
 ta=$((a)
 tb=$((b)
 if ta is $Q $) tb is $Q:
  $! a*b
 if ta is $- or tb is $-:
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
$. nneg(a):
 if $((a)is $/:
  $!('Q',-a[1],a[2])
 $!-a
$. nsub(a,b):
 $! nadd(a,nneg(b))
$. ninv(a):
 t=$((a)
 if t is $-:
  if a==0.0:
   err("Division by zero")
  $! 1.0/a
 n,d=nd(a)
 $! Q(d,n)
$. ndiv(a,b):
 $! $m(a,ninv(b))
$. $=(a):
 if $((a)is $/:
  a=a[1]
 if a>0:
  $! 1
 if a<0:
  $!-1
 $! 0
$. ncmp(a,b):
 $! $=(nsub(a,b))
$. $}(a):
 t=$((a)
 if t is $Q:
  $! a
 if t is $-:
  if a!=a or a in($-('$T'),$-('-$T')):
   err("Domain error")
  $! $Q($3.$n(a))
 $! a[1]//a[2]
$. nabs(a):
 if $=(a)<0:
  $! nneg(a)
 $! a
$. nipow(a,k):
 if k<0:
  $! nipow(ninv(a),-k)
 if $((a)is $-:
  $! a**k
 n,d=nd(a)
 $! Q(n**k,d**k)
$. iroot(n,k):
 if n<2:
  $! n
 x=$Q($3.pow(n,1.0/k))if n<10**300 $+ 1<<(($](bin(n))-2)//k+1)
 if x<1:
  x=1
 $> $R:
  y=((k-1)*x+n//(x**(k-1)))//k
  if y>=x:
   break
  x=y
 $> x**k>n:
  x-=1
 $>(x+1)**k<=n:
  x+=1
 $! x
$. isqrt(n):
 $! iroot(n,2)
SMALLP=$*
$. smallprimes():
 global SMALLP
 if SMALLP is $*:
  N=1000
  s=bytearray(N)
  ps=[]
  $4 i in $j(2,N):
   if $2 s[i]:
    ps.$&(i)
    $4 j in $j(i*i,N,i):
     s[j]=1
  SMALLP=ps
 $! SMALLP
$. $%(e,h):
 $! $((e)is $/ $) e[0]==h
$. head(e):
 if $((e)is $/:
  $! e[0]
 $! $*
$. okey(e):
 $! repr(e)
$. has(e,x):
 if e==x:
  $! $R
 if $((e)is $/ $) e[0]!='Q':
  $4 a in e[1:]:
   if has(a,x):
    $! $R
 $! $6
$. freeof(e,x):
 $! $2 has(e,x)
$. freeofall(e,xs):
 $4 x in xs:
  if has(e,x):
   $! $6
 $! $R
$. symbols(e,$g=$*):
 if $g is $*:
  $g=[]
 t=$((e)
 if t is $a:
  if e $2 in $o $) e $2 in $g:
   $g.$&(e)
 $L t is $/ $) e[0]!='Q' $) e[0]!='$a':
  $4 a in e[1:]:
   symbols(a,$g)
 $! $g
$. $1(e):
 t=$((e)
 if t is $a:
  $! e in $o
 if t is $/ $) e[0]!='Q':
  if e[0]=='$a':
   $! $6
  $4 a in e[1:]:
   if $2 $1(a):
    $! $6
 $! $R
$. $S(e):
 t=$((e)
 if t is $-:
  $! $R
 if t is $/ $) e[0]!='Q':
  $4 a in e[1:]:
   if $S(a):
    $! $R
 $! $6
$. $:(a):
 if $((a)is $/ $) a[0]=='*' $) $0(a[1]):
  if $](a)==3:
   $! a[1],a[2]
  $! a[1],('*',)+a[2:]
 $! 1,a
$. cmul(c,r):
 if $((c)is $Q $) c==1:
  $! r
 if $((r)is $/ $) r[0]=='*':
  if $0(r[1]):
   c=$m(c,r[1])
   if $((c)is $Q $) c==1:
    $!('*',)+r[2:]if $](r)>3 $+ r[2]
   $!('*',c)+r[2:]
  $!('*',c)+r[1:]
 $!('*',c,r)
$. add(*$?):
 $! $F($?)
$. $F($?):
 $c=0
 $K={}
 order=[]
 st=$f($?)
 infs=0
 $> st:
  a=st.pop()
  t=$((a)
  if t is $Q or t is $-:
   $c=nadd($c,a)
   $8
  if t is $/:
   h=a[0]
   if h=='Q':
    $c=nadd($c,a)
    $8
   if h=='+':
    st.extend(a[1:])
    $8
   if h=='*' $) $0(a[1]):
    c=a[1]
    r=a[2]if $](a)==3 $+('*',)+a[2:]
   $+:
    c=1
    r=a
  $+:
   if a=='$9':
    $! '$9'
   c=1
   r=a
  if r=='$T':
   s=$=(c)
   if s==0:
    $8
   if infs $) infs!=s:
    $! '$9'
   infs=s
   $8
  if r in $K:
   $K[r]=nadd($K[r],c)
  $+:
   $K[r]=c
   order.$&(r)
 if infs:
  $! '$T' if infs>0 $+('*',-1,'$T')
 $g=[]
 $4 r in order:
  c=$K[r]
  if c==0:
   $8
  $g.$&(cmul(c,r))
 if $c!=0 or $2 $g:
  if $g $) $c==0:
   pass
  $+:
   $g.$&($c)
 if $]($g)==1:
  $! $g[0]
 $g.sort(key=okey)
 $!('+',)+$/($g)
$. isrrad(e):
 $! $((e)is $/ $) e[0]=='^' $) $((e[1])is $Q $) isq(e[2])
$. $A(*$?):
 $! $C($?)
''')
_x(r'''$. $C($?):
 $G=1
 bases={}
 order=[]
 st=$f($?)
 $> st:
  a=st.pop()
  t=$((a)
  if t is $Q or t is $-:
   $G=$m($G,a)
   $8
  if t is $/:
   h=a[0]
   if h=='Q':
    $G=$m($G,a)
    $8
   if h=='*':
    st.extend(a[1:])
    $8
   if h=='^':
    b=a[1]
    x=a[2]
   $+:
    b=a
    x=1
  $+:
   if a=='$9':
    $! '$9'
   b=a
   x=1
  if b in bases:
   bases[b]=add(bases[b],x)
  $+:
   bases[b]=x
   order.$&(b)
 if $G==0:
  if '$T' in bases:
   $! '$9'
  $4 b in order:
   if b=='$9' or has(b,'$9'):
    $! '$9'
  $! $G
 $X=[]
 rad={}
 $v=[]
 $. collect(p):
  c=1
  t=$((p)
  if t is $Q or t is $- or(t is $/ $) p[0]=='Q'):
   $! p
  if t is $/ $) p[0]=='*':
   items=p[1:]
  $+:
   items=(p,)
  $4 f in items:
   if $0(f):
    c=$m(c,f)
   $L isrrad(f):
    ex=f[2]
    if ex in rad:
     rad[ex]=rad[ex]*f[1]
     $v.$&($*)
    $+:
     rad[ex]=f[1]
     $v.$&(ex)
   $+:
    $X.$&(f)
  $! c
 $4 b in order:
  p=pw(b,bases[b])
  if p=='$9':
   $! '$9'
  $G=$m($G,collect(p))
 if rad:
  multi=$]($v)!=$](rad)
  if multi:
   items=[(ex,rad[ex])$4 ex in $v if ex is $2 $*]
   rad.clear()
   del $v[:]
   pend=[]
   $4 ex,b in items:
    pend.$&(pw_num(b,ex))
   $4 p in pend:
    $G=$m($G,collect(p))
  $4 ex in rad:
   $X.$&(('^',rad[ex],ex))
 if $G==0:
  $! 0
 if '$T' in $X:
  if $]($X)==1 or $R:
   $G=$=($G)if $(($G)is $2 $- $+(1.0 if $G>0 $+-1.0)
   if $(($G)is $-:
    $G=$Q($G)
 if $2 $X:
  $! $G
 if $]($X)>1:
  algs=[f $4 f in $X if $%(f,'+')$) isalg(f)]
  if algs $) all([isalg(f)$4 f in $X]):
   r=$G
   $4 f in $X:
    r=$W(r,f)
   $! r
 if $]($X)==1:
  f=$X[0]
  if $(($G)is $Q $) $G==1:
   $! f
  if $((f)is $/ $) f[0]=='+':
   $! $F([$A($G,t)$4 t in f[1:]])
  $!('*',$G,f)
 $X.sort(key=okey)
 if $(($G)is $Q $) $G==1:
  $!('*',)+$/($X)
 $!('*',$G)+$/($X)
$. $t(a):
 $! $A(-1,a)
$. sub(a,b):
 $! add(a,$A(-1,b))
$. div(a,b):
 $! $A(a,pw(b,-1))
$. inv(a):
 $! pw(a,-1)
$. $O(a):
 $! pw(a,$[)
$. factor_int_small(n):
 fs=[]
 $4 p in smallprimes():
  if p*p>n:
   break
  if n%p==0:
   k=0
   $> n%p==0:
    n//=p
    k+=1
   fs.$&((p,k))
 $! fs,n
$. radical(n,q):
 if n<2:
  $! n,1
 a=1
 m=1
 fs,$H=factor_int_small(n)
 $4 p,k in fs:
  a*=p**(k//q)
  m*=p**(k%q)
 if $H>1:
  r=iroot($H,q)
  if r**q==$H:
   a*=r
  $+:
   m*=$H
 $! a,m
$. ipow_root(n,p,q):
 if ibits(n)*p>2000 or q>60:
  $!('^',n,Q(p,q))
 a,m=radical(n**p,q)if p>1 $+ radical(n,q)
 if m==1:
  $! a
 ex=Q(1,q)
 k=2
 best=$*
 $>(1<<k)<=m $) k<=64:
  r=iroot(m,k)
  if r**k==m:
   best=(r,k)
  k+=1
 if best is $2 $*:
  m=best[0]
  ex=Q(best[1],q)
 if ex==1:
  $! a*m
 if isint(ex):
  $! a*m**ex
 if a==1:
  $!('^',m,ex)
 $!('*',a,('^',m,ex))
MAXBITS=12000
$. ibits(n):
 if n==0:
  $! 0
 h='%x'%abs(n)
 v=$Q(h[0],16)
 $! 4*$](h)-(3 if v<2 $+ 2 if v<4 $+ 1 if v<8 $+ 0)
$. bigpow(b,x):
 n,d=nd(b)
 if d==1 $) abs(n)<=1:
  $! $6
 $! abs(x)*(ibits(n)+(ibits(d)if d>1 $+ 0))>MAXBITS
$. pw_num(b,x):
 if $((b)is $- or $((x)is $-:
  bf=tofl(b)
  xf=tofl(x)
  if bf==0.0:
   if xf>0:
    $! 0.0
   if xf==0:
    $! 1.0
   $! '$9'
  if bf!=bf or xf!=xf:
   $! '$9'
  if bf<0 $)(xf in($-('$T'),$-('-$T'))or xf!=$3.$n(xf)):
   if $d(x)$) nd(x)[1]%2==1:
    r=(-bf)**xf
    $!-r if nd(x)[0]%2 $+ r
   z=$,(bf)**xf
   $! $i(z)
  try:
   $! bf**xf
  $J $I:
   $! '$T'
 if $((x)is $Q:
  if b==0:
   if x<0:
    $! '$9'
   $! 0
  if bigpow(b,x):
   $!('^',b,x)
  $! nipow(b,x)
 p,q=nd(x)
 if b==0:
  $! 0 if p>0 $+ '$9'
 if $=(b)<0:
  if q%2==1:
   r=pw_num(nneg(b),x)
   if p%2:
    $! $A(-1,r)
   $! r
  if q==2:
   $! $A(pw('i',p),pw_num(nneg(b),x))
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
 $r=[]
 if n>1:
  $r.$&(ipow_root(n,fp,fq))
 if d>1:
  $r.$&(Q(1,d))
  $r.$&(ipow_root(d,fq-fp,fq))
 c=res
 $X=[]
 $4 pt in $r:
  if $0(pt):
   c=$m(c,pt)
  $L pt[0]=='*':
   c=$m(c,pt[1])
   $X.$&(pt[2])
  $+:
   $X.$&(pt)
 if $]($X)==2:
  if $X[0][2]==$X[1][2]:
   $! $A(c,pw_num($X[0][1]*$X[1][1],$X[0][2]))
  $X.sort(key=okey)
 if $2 $X:
  $! c
 if c==1:
  if $]($X)==1:
   $! $X[0]
  $!('*',)+$/($X)
 $!('*',c)+$/($X)
$. $|(e):
 if $0(e):
  $! $=(e)>0
 if e=='pi' or e=='e':
  $! $R
 if isrrad(e):
  $! e[1]>0
 if $%(e,'^')$)(e[1]=='e' or e[1]=='pi')$) $B(e[2]):
  $! $R
 $! $6
$. isalg(e):
 t=$((e)
 if t is $Q or t is $-:
  $! $R
 if t is $a:
  $! e=='i'
 h=e[0]
 if h=='Q':
  $! $R
 if h=='^':
  $! $0(e[1])$) $0(e[2])
 if h=='+' or h=='*':
  $4 a in e[1:]:
   if $2 isalg(a):
    $! $6
  $! $R
 $! $6
''')
_x(r'''$. pw(b,x):
 if x==0:
  if b=='$9' or b=='$T':
   $! '$9'
  $! 1
 if $((x)is $Q $) x==1:
  $! b
 if b=='$9' or x=='$9':
  $! '$9'
 bn=$0(b)
 xn=$0(x)
 if bn $) xn:
  $! pw_num(b,x)
 if b==1 $) $((b)is $Q:
  $! 1
 if b=='$T':
  if xn:
   $! '$T' if $=(x)>0 $+ 0
  if x=='$T':
   $! '$T'
 if xn $) b==0:
  $! 0 if $=(x)>0 $+ '$9'
 if b=='i' $) $((x)is $Q:
  r=x%4
  $!(1,'i',-1,('*',-1,'i'))[r]
 if x=='$T' $) bn:
  if nabs(b)==1:
   $! '$9' if b==1 $+ '$9'
  if ncmp(nabs(b),1)>0:
   $! '$T' if $=(b)>0 $+ '$9'
  $! 0
 if b=='e':
  if x=='$T':
   $! '$T'
  if $%(x,'*')$) $](x)==3 $) x[1]==-1 $) x[2]=='$T':
   $! 0
  if $((x)is $-:
   $! $3.exp(x)
  if $%(x,'ln'):
   $! x[1]
  if $%(x,'*'):
   c,r=$:(x)
   if $%(r,'ln')$) $d(c):
    $! pw(r[1],c)
  if $%(x,'+'):
   $z=[]
   $H=[]
   $4 t in x[1:]:
    c,r=$:(t)
    if $%(r,'ln')$) $d(c):
     $z.$&(pw(r[1],c))
    $+:
     $H.$&(t)
   if $z:
    $! $C($z+[pw('e',$F($H))])
  if $%(x,'*')$) 'i' in x $) 'pi' in x:
   c,r=$:(x)
   if r==('*','i','pi')$) $d(c):
    $! add(cos_($A(c,'pi')),$A('i',sin_($A(c,'pi'))))
 if b!='e' $) $1(b)$) $1(x)$) $2 $d(x)$)(has(b,'i')or has(x,'i'))$) $2 $S(x):
  L=fn('ln',b)
  if $2 $%(L,'ln')$) $2($%(L,'+')$) any([$%(t,'ln')$4 t in L[1:]])):
   $! pw('e',$_($A(x,L)))
 if $((b)is $/:
  h=b[0]
  if h=='^':
   bb=b[1]
   ee=b[2]
   if $((x)is $Q:
    $! pw(bb,$A(ee,x))
   if $|(bb):
    $! pw(bb,$A(ee,x))
   if $d(ee)$) $d(x):
    r=$m(ee,x)
    if $((ee)is $Q:
     if ee%2==0:
      if $((r)is $Q $) r%2==0:
       $! pw(bb,r)
      $! pw(fn('abs',bb),r)
     $! pw(bb,r)
    if nd(ee)[0]%2==1 $) nd(ee)[1]%2==1:
     $! pw(bb,r)
    if nd(ee)[0]%2==1:
     $! pw(bb,r)
  $L h=='*':
   if $((x)is $Q:
    $! $C([pw(f,x)$4 f in b[1:]])
   $z=[]
   $H=[]
   $4 f in b[1:]:
    if $0(f):
     if $=(f)>0:
      $z.$&(pw(f,x))
     $L f!=-1:
      $z.$&(pw(nneg(f),x))
      $H.$&(-1)
     $+:
      $H.$&(f)
    $L $|(f)or $%(f,'abs'):
     $z.$&(pw(f,x))
    $+:
     $H.$&(f)
   if $z:
    $! $C($z+[pw($C($H),x)])
  $L h=='abs':
   if $((x)is $Q $) x%2==0:
    $! pw(b[1],x)
  $L h=='+':
   if x==$[ $) isalg(b)$) $2 has(b,'i'):
    dn=denest(b)
    if dn is $2 $*:
     $! dn
   if isq(x)$) x[2]==2 $) $=(x)<0 $) isalg(b)$) $2 has(b,'i'):
    dn=denest(b)
    if dn is $2 $*:
     $! pw(pw(dn,-1),-x[1])if x[1]!=-1 $+ pw(dn,-1)
   if $((x)is $Q $) x!=1 $) $2 isalg(b):
    c=sumcontent(b)
    if c!=1:
     $! $A(pw(c,x),pw($A(ninv(c),b),x))
    if leadneg(b):
     nb=$A(-1,b)
     if x%2==0:
      $! pw(nb,x)
     $! $A(-1,pw(nb,x))
   if $((x)is $Q $) isalg(b):
    if x>0 $) x<=64:
     $! $`(b,x)
    if x<0 $) x>=-64:
     r=$V(b)
     if r is $2 $*:
      if x==-1:
       $! r
      $! $`(r,-x)
 $!('^',b,x)
$. tdeg(r):
 d=0
 fs=r[1:]if $%(r,'*')$+(r,)
 $4 f in fs:
  if $((f)is $a $) f $2 in $o:
   d+=1
  $L $%(f,'^')$) $((f[1])is $a $) f[1]$2 in $o $) $0(f[2]):
   d+=tofl(f[2])
 $! d
$. leadneg(b):
 best=$*
 bk=$*
 $4 t in b[1:]:
  if $0(t):
   $8
  c,r=$:(t)
  k=(-tdeg(r),okey(r))
  if bk is $* or k<bk:
   bk=k
   best=c
 if best is $*:
  $! $6
 $! $=(best)<0 if $0(best)$+ $6
$. sumcontent(b):
 g=0
 L=1
 $4 t in b[1:]:
  c,r=$:(t)
  if $2 $d(c):
   $! 1
  n,d=nd(c)
  g=igcd(g,n)
  L=ilcm(L,d)
 if g==0:
  $! 1
 $! Q(g,L)
$. denest(b):
 a=0
 c=0
 n=$*
 $4 t in b[1:]:
  if $d(t):
   a=nadd(a,t)
   $8
  cc,r=$:(t)
  if isrrad(r)$) r[2]==$[ $) $d(cc)$)(n is $* or n==r[1]):
   n=r[1]
   c=nadd(c,cc)
  $+:
   $! $*
 if n is $* or c==0:
  $! $*
 d2=nsub($m(a,a),$m($m(c,c),n))
 if $=(d2)<0:
  $! $*
 dn,dd=nd(d2)
 rn=isqrt(dn)
 rd=isqrt(dd)
 if rn*rn!=dn or rd*rd!=dd:
  $! $*
 d=Q(rn,rd)
 p=ndiv(nadd(a,d),2)
 m=ndiv(nsub(a,d),2)
 if $=(p)<0 or $=(m)<0:
  $! $*
 r=add(pw(p,$[),$A($=(c),pw(m,$[)))
 if $%(r,'+')$) $](r)<=3:
  $! r
 $! $*
$. $W(a,b):
 ta=a[1:]if $%(a,'+')$+(a,)
 tb=b[1:]if $%(b,'+')$+(b,)
 if $](ta)*$](tb)>4*MAXTERMS:
  toobig('the expansion would have more than %d $K'%MAXTERMS)
 $g=[]
 $4 u in ta:
  $4 v in tb:
   $g.$&($A(u,v))
 $! $F($g)
$. $`(b,n):
 t=$](b)-1 if $%(b,'+')$+ 1
 if t>1 $) $2 $1(b):
  c=1
  $4 k in $j(1,t):
   c=c*(n+k)//k
   if c>MAXTERMS:
    toobig('the expansion would have more than %d $K'%MAXTERMS)
 r=1
 p=b
 $> n>0:
  if n&1:
   r=$W(r,p)
  n>>=1
  if n:
   p=$W(p,p)
 $! r
''')
_x(r'''$. $V(b):
 re_,im_=reim(b)
 if im_!=0:
  d=add($A(re_,re_),$A(im_,im_))
  d=$_(d)
  if $%(d,'+'):
   r2=$V(d)
   if r2 is $*:
    $! $*
  $+:
   r2=pw(d,-1)
  $! $W(sub(re_,$A('i',im_)),r2)
 $K=b[1:]if $%(b,'+')$+(b,)
 kern=$*
 kerns=[]
 $4 t in $K:
  c,r=$:(t)
  if r!=1 $) $2 $0(r):
   if isrrad(r)$) r[2]==$[:
    if r $2 in kerns:
     kerns.$&(r)
   $+:
    $! $*
 if $2 kerns or $](kerns)>3:
  $! $*
 kern=kerns[0]
 if $](kerns)>1:
  A=$F([t $4 t in $K if $:(t)[1]!=kern])
  B=$F([$:(t)[0]$4 t in $K if $:(t)[1]==kern])
  den=$_(sub($A(A,A),$A(B,B,kern[1])))
  if den==0:
   $! $*
  if $%(den,'+'):
   r2=$V(den)
   if r2 is $*:
    $! $*
  $+:
   r2=pw(den,-1)
  $! $W(sub(A,$A(B,kern)),r2)
 a0=0
 a1=0
 $4 t in $K:
  c,r=$:(t)
  if r==kern:
   a1=nadd(a1,c)
  $+:
   a0=add(a0,t)
 den=sub($A(a0,a0),$A($m(a1,a1),kern[1]))
 if den==0:
  $! $*
 $! $W(sub(a0,$A(a1,kern)),pw(den,-1))
$. reim(e):
 t=$((e)
 if t is $Q or t is $-:
  $! e,0
 if t is $a:
  if e=='i':
   $! 0,1
  $! e,0
 h=e[0]
 if h=='Q':
  $! e,0
 if h=='+':
  rs=[]
  ims=[]
  $4 a in e[1:]:
   r,i=reim(a)
   rs.$&(r)
   ims.$&(i)
  $! $F(rs),$F(ims)
 if h=='*':
  r=1
  i=0
  $4 a in e[1:]:
   ar,ai=reim(a)
   if ai==0:
    r=$A(r,ar)
    i=$A(i,ar)
   $+:
    r,i=sub($A(r,ar),$A(i,ai)),add($A(r,ai),$A(i,ar))
  $! r,i
 if h=='^':
  b=e[1]
  x=e[2]
  if $2 has(b,'i')$) $2 has(x,'i'):
   if $0(x)$) $2 $d(x):
    $! e,0
   if $d(x)$) nd(x)[1]%2==0:
    if $1(b):
     v=cv(b)
     if v is $2 $* $) $((v)is $2 $, $) v<0:
      $! $p(e)
    $! e,0
   $! e,0
  if $((x)is $Q:
   br,bi=reim(b)
   if x>0:
    z=$`(add(br,$A('i',bi)),x)
    if has(z,'i')$) z!=e:
     $! reim(z)
   $L $1(b):
    r=$V(b)
    if r is $2 $*:
     $! reim($`(r,-x))if x!=-1 $+ reim(r)
  $! $p(e)
 if h in('$f','mat','$a'):
  $! e,0
 $4 a in e[1:]:
  if has(a,'i'):
   $! $p(e)
 $! e,0
$. cv(u):
 try:
  v=$y(u)
 $J($7,$M,$<,$I,$w):
  $! $*
 if v!=v:
  $! $*
 if $((v)is $,:
  if v.$h!=v.$h or v.$s!=v.$s:
   $! $*
  if abs(v.$h)==$-('$T')or abs(v.$s)==$-('$T'):
   $! $*
 $L abs(v)==$-('$T'):
  $! $*
 $! v
$. $p(e):
 if $1(e):
  v=cv(e)
  if v is $*:
   $!('$h',e),('$s',e)
  z=$,(v)
  $! z.$h,z.$s
 $!('$h',e),('$s',e)
$. conj(e):
 r,i=reim(e)
 $! sub(r,$A('i',i))
$. $i(z):
 if $((z)is $2 $,:
  $! z
 if z.$s==0:
  $! z.$h
 if z.$h==0:
  $! $A(z.$s,'i')
 $! add(z.$h,$A(z.$s,'i'))
$5={}
$. fn($;,*$?):
 if $]($?)==1 $) $(($?[0])is $f:
  $?=$/($?[0])
 $4 a in($?[:1]if $;=='when' $+ $?):
  if a=='$9':
   $! '$9'
 f=$5.get($;)
 if f is $2 $*:
  r=f(*$?)
  if r is $2 $*:
   $! r
 $!($;,)+$/($?)
$. $e(e):
 if $0(e):
  $! $=(e)<0
 if $%(e,'*'):
  $! $0(e[1])$) $=(e[1])<0
 if $%(e,'+'):
  $! leadneg(e)
 $! $6
$. $B(e):
 if $0(e):
  $! $R
 if $((e)is $a:
  $! e!='i' $) e!='$9'
 $! $2 has(e,'i')
$. fval($;,x):
 $! $i(NUMF[$;](x))
$. ${($;,u):
 try:
  v=NUMF[$;]($y(u))
 $J($7,$M,$<,$I,$w):
  $! $*
 if $((v)is $,:
  if v.$h!=v.$h or v.$s!=v.$s:
   $! $*
 $L v!=v:
  $! $*
 $! $i(v)
$. pi_coef(u):
 if u=='pi':
  $! 1
 if u==0:
  $! 0
 if $%(u,'*')$) $](u)==3 $) u[2]=='pi' $) $d(u[1]):
  $! u[1]
 $! $*
$. split_pi(u):
 if $%(u,'+'):
  $4 t in u[1:]:
   c=pi_coef(t)
   if c is $2 $* $) c!=0:
    $H=$F([s $4 s in u[1:]if s is $2 t])
    $! c,$H
 $! $*
TRIGT=$*
$. $~():
 global TRIGT
 if TRIGT is $*:
  s2=$O(2)
  s3=$O(3)
  s5=$O(5)
  s6=$O(6)
  q=Q
  T={}
  T[0]=0
  T[q(1,12)]=$A(q(1,4),sub(s6,s2))
  T[q(1,10)]=$A(q(1,4),sub(s5,1))
  T[q(1,8)]=$A($[,$O(sub(2,s2)))
  T[q(1,6)]=$[
  T[q(1,5)]=$A(q(1,4),$O(sub(10,$A(2,s5))))
  T[q(1,4)]=$A($[,s2)
  T[q(3,10)]=$A(q(1,4),add(s5,1))
  T[q(1,3)]=$A($[,s3)
  T[q(3,8)]=$A($[,$O(add(2,s2)))
  T[q(2,5)]=$A(q(1,4),$O(add(10,$A(2,s5))))
  T[q(5,12)]=$A(q(1,4),add(s6,s2))
  T[$[]=1
  TT={}
  TT[0]=0
  TT[q(1,12)]=sub(2,s3)
  TT[q(1,8)]=sub(s2,1)
  TT[q(1,6)]=$A(q(1,3),s3)
  TT[q(1,4)]=1
  TT[q(1,3)]=s3
  TT[q(3,8)]=add(s2,1)
  TT[q(5,12)]=add(2,s3)
  TT[q(1,5)]=$O(sub(5,$A(2,s5)))
  TT[q(2,5)]=$O(add(5,$A(2,s5)))
  TT[q(1,10)]=$A(q(1,5),$O(sub(25,$A(10,s5))))
  TT[q(3,10)]=$A(q(1,5),$O(add(25,$A(10,s5))))
  TRIGT=(T,TT)
 $! TRIGT
$. sin_pi(c):
 c=nsub(c,$m(2,$}($m(c,$[))))
 sg=1
 if ncmp(c,1)>=0:
  c=nsub(c,1)
  sg=-1
 if ncmp(c,$[)>0:
  c=nsub(1,c)
 T=$~()[0]
 if c in T:
  $! $A(sg,T[c])
 if sg<0:
  $! $t(('sin',$A(c,'pi')))
 $!('sin',$A(c,'pi'))
$. tan_pi(c):
 c=nsub(c,$}(c))
 sg=1
 if ncmp(c,$[)>0:
  c=nsub(1,c)
  sg=-1
 if c==$[:
  $! '$9'
 TT=$~()[1]
 if c in TT:
  $! $A(sg,TT[c])
 $! $A(sg,('tan',$A(c,'pi')))
''')
_x(r'''$. sin_(u):
 if $0(u):
  if u==0:
   $! 0
  if $((u)is $-:
   $! $3.sin(u)
  if $=(u)<0:
   $! $t(fn('sin',$t(u)))
  $! $*
 if u=='$T' or u==('*',-1,'$T'):
  $! '$9'
 c=pi_coef(u)
 if c is $2 $*:
  $! sin_pi(c)
 if $S(u)$) $1(u):
  $! ${('sin',u)
 if $e(u):
  $! $t(fn('sin',$t(u)))
 sp=split_pi(u)
 if sp is $2 $*:
  c,$H=sp
  c=nsub(c,$m(2,$}($m(c,$[))))
  if c==0:
   $! fn('sin',$H)
  if c==1:
   $! $t(fn('sin',$H))
  if c==$[:
   $! fn('cos',$H)
  if c==Q(3,2):
   $! $t(fn('cos',$H))
  if ncmp(c,1)>0:
   $!('sin',add($H,$A(nsub(c,2),'pi')))
  $!('sin',add($H,$A(c,'pi')))
 if $%(u,'$^'):
  $! u[1]
 if $%(u,'$l'):
  $! $O(sub(1,pw(u[1],2)))
 if $%(u,'$b'):
  $! div(u[1],$O(add(1,pw(u[1],2))))
 $! $*
$. cos_(u):
 if $0(u):
  if u==0:
   $! 1
  if $((u)is $-:
   $! $3.cos(u)
  if $=(u)<0:
   $! fn('cos',$t(u))
  $! $*
 if u=='$T' or u==('*',-1,'$T'):
  $! '$9'
 c=pi_coef(u)
 if c is $2 $*:
  $! sin_pi(nadd(c,$[))
 if $S(u)$) $1(u):
  $! ${('cos',u)
 if $e(u):
  $! fn('cos',$t(u))
 sp=split_pi(u)
 if sp is $2 $*:
  c,$H=sp
  c=nsub(c,$m(2,$}($m(c,$[))))
  if c==0:
   $! fn('cos',$H)
  if c==1:
   $! $t(fn('cos',$H))
  if c==$[:
   $! $t(fn('sin',$H))
  if c==Q(3,2):
   $! fn('sin',$H)
  if ncmp(c,1)>0:
   $!('cos',add($H,$A(nsub(c,2),'pi')))
  $!('cos',add($H,$A(c,'pi')))
 if $%(u,'$l'):
  $! u[1]
 if $%(u,'$^'):
  $! $O(sub(1,pw(u[1],2)))
 if $%(u,'$b'):
  $! pw(add(1,pw(u[1],2)),Q(-1,2))
 $! $*
$. tan_(u):
 if $0(u):
  if u==0:
   $! 0
  if $((u)is $-:
   $! $3.tan(u)
  if $=(u)<0:
   $! $t(fn('tan',$t(u)))
  $! $*
 c=pi_coef(u)
 if c is $2 $*:
  $! tan_pi(c)
 if $S(u)$) $1(u):
  $! ${('tan',u)
 if $e(u):
  $! $t(fn('tan',$t(u)))
 sp=split_pi(u)
 if sp is $2 $*:
  c,$H=sp
  c=nsub(c,$}(c))
  if c==0:
   $! fn('tan',$H)
  if c==$[:
   $! $t(pw(fn('tan',$H),-1))
  $!('tan',add($H,$A(c,'pi')))
 if $%(u,'$b'):
  $! u[1]
 $! $*
INVT=$*
$. inv_table():
 global INVT
 if INVT is $*:
  T,TT=$~()
  S={}
  $4 k in T:
   S[T[k]]=k
  Tn={}
  $4 k in TT:
   Tn[TT[k]]=k
  INVT=(S,Tn)
 $! INVT
$. asin_(u):
 if $0(u):
  if $((u)is $-:
   if-1.0<=u<=1.0:
    $! $3.asin(u)
   $! fval('$^',u)
 if $e(u):
  $! $t(fn('$^',$t(u)))
 S=inv_table()[0]
 if u in S:
  $! $A(S[u],'pi')
 if $1(u)$) $S(u):
  $! ${('$^',u)
 $! $*
$. acos_(u):
 if $0(u)$) $((u)is $-:
  if-1.0<=u<=1.0:
   $! $3.acos(u)
  $! fval('$l',u)
 a=asin_(u)
 if a is $2 $* $) $2 $%(a,'$^')$) freeof(a,'$^'):
  $! sub($A($[,'pi'),a)
 if $e(u):
  $! sub('pi',fn('$l',$t(u)))
 $! $*
$. atan_(u):
 if $0(u):
  if $((u)is $-:
   $! $3.atan(u)
 if u=='$T':
  $! $A($[,'pi')
 if u==('*',-1,'$T'):
  $! $A(Q(-1,2),'pi')
 if $e(u):
  $! $t(fn('$b',$t(u)))
 Tn=inv_table()[1]
 if u in Tn:
  $! $A(Tn[u],'pi')
 if $1(u)$) $S(u):
  $! ${('$b',u)
 $! $*
$. ln_(u):
 if $0(u):
  if u==1:
   $! 0
  if u==0:
   $!('*',-1,'$T')
  if $((u)is $-:
   if u>0:
    $! $3.log(u)
   $! add($3.log(-u),$A($3.pi,'i'))
  if $=(u)<0:
   $! add(fn('ln',nneg(u)),$A('i','pi'))
  n,d=nd(u)
  if n==1:
   $! $t(fn('ln',d))
  $! $*
 if u=='e':
  $! 1
 if u=='$T':
  $! '$T'
 if u=='i':
  $! $A($[,'i','pi')
 if $%(u,'^'):
  if u[1]=='e' $) $B(u[2]):
   $! u[2]
  if $|(u[1])$) $B(u[2])$) $0(u[2]):
   $! $A(u[2],fn('ln',u[1]))
 if $1(u)$) $S(u):
  $! ${('ln',u)
 $! $*
$. log_(u,b=10):
 if $0(u)$) $0(b):
  if $((u)is $- or $((b)is $-:
   a1=${('ln',u)
   a2=${('ln',b)
   if a1 is $2 $* $) a2 is $2 $* $) a2!=0:
    $! div(a1,a2)
   $! $*
  if u==1:
   $! 0
  if $d(u)$) $d(b)$) $=(u)>0 $) $=(b)>0 $) b!=1:
   k=exact_log(u,b)
   if k is $2 $*:
    $! k
 if u==b:
  $! 1
 if $%(u,'^')$) u[1]==b $) $B(u[2]):
  $! u[2]
 if $1(u)$) $1(b)$)($S(u)or $S(b)):
  a1=${('ln',u)
  a2=${('ln',b)
  if a1 is $2 $* $) a2 is $2 $* $) a2!=0:
   $! div(a1,a2)
  $! $*
 $! $*
$. exact_log(u,b):
 un,ud=nd(u)
 bn,bd=nd(b)
 lu=$3.log(tofl(u))
 lb=$3.log(tofl(b))
 if lb==0:
  $! $*
 k=lu/lb
 $4 den in $j(1,13):
  $c=$Q(round(k*den))
  if abs(k*den-$c)<1e-9:
   kk=Q($c,den)
   if pw_num(b,kk)==u:
    $! kk
   $! $*
 $! $*
$. abs_(u):
 if $0(u):
  $! nabs(u)
 if u=='$T' or u==('*',-1,'$T'):
  $! '$T'
 if $%(u,'abs'):
  $! u
 if $%(u,'^')$) $((u[2])is $Q $) u[2]%2==0 $) $B(u[1]):
  $! u
 if has(u,'i'):
  r,i=reim(u)
  if i!=0 $) $2 has(r,'i')$) $2 has(i,'i'):
   $! $O(add(pw(r,2),pw(i,2)))
 if $1(u):
  v=cv(u)
  if v is $2 $* $) $((v)is $2 $,:
   if v>=0:
    $! u
   $! $t(u)
 if $%(u,'*'):
  $z=[]
  $H=[]
  $4 f in u[1:]:
   if $0(f):
    $z.$&(nabs(f))
   $L $1(f):
    $z.$&(abs_(f)or('abs',f))
   $L $%(f,'^')$) $((f[2])is $Q $) f[2]%2==0:
    $z.$&(f)
   $L $%(f,'^')$) f[1]=='e':
    $z.$&(f)
   $+:
    $H.$&(f)
  if $z:
   $! $C($z+[fn('abs',$C($H))])
 if $e(u):
  $! fn('abs',$t(u))
 if $%(u,'^')$) u[1]=='e' $) $B(u[2]):
  $! u
 $! $*
''')
_x(r'''$. sign_(u):
 if $0(u):
  $! $=(u)if $((u)is $2 $- $+ $-($=(u))
 if u=='$T':
  $! 1
 if $1(u):
  v=cv(u)
  if v is $2 $* $) $((v)is $2 $,:
   $! 1 if v>0 $+(-1 if v<0 $+ 0)
 if $%(u,'*')$) $0(u[1]):
  $! $A($=(u[1]),fn('sign',cmul(nabs(u[1]),$:(u)[1])))
 if $%(u,'^')$) $((u[2])is $Q $) u[2]%2==0:
  $! $*
 $! $*
$. finite(v):
 $! v==v $) v!=$-('$T')$) v!=$-('-$T')
$. floor_(u):
 if $0(u):
  if $((u)is $-:
   $! $-($3.$n(u))if finite(u)$+ $*
  $! $}(u)
 if $1(u)$) $2 has(u,'i'):
  v=cv(u)
  if v is $2 $* $) $((v)is $2 $,:
   $! $Q($3.$n(v))
 $! $*
$. ceil_(u):
 f=floor_($t(u))
 if f is $2 $*:
  $! $t(f)
 $! $*
$. sinh_(u):
 if u==0:
  $! 0
 if $e(u):
  $! $t(fn('sinh',$t(u)))
 if $%(u,'$x'):
  $! u[1]
 $! $*
$. cosh_(u):
 if u==0:
  $! 1
 if $e(u):
  $! fn('cosh',$t(u))
 if $%(u,'arccosh'):
  $! u[1]
 $! $*
$. tanh_(u):
 if u==0:
  $! 0
 if $e(u):
  $! $t(fn('tanh',$t(u)))
 $! $*
$. odd0($;):
 $. g(u):
  if u==0:
   $! 0
  if $e(u):
   $! $t(fn($;,$t(u)))
  $! $*
 $! g
$. fact_(u):
 if $((u)is $Q:
  if u<0:
   $! '$9'
  if u>1000:
   $! $*
  r=1
  $4 k in $j(2,u+1):
   r*=k
  $! r
 if isq(u)$) u[2]==2 $) u[1]>0:
  n=u[1]
  r=$A($O('pi'),Q(1,1))
  k=Q(1,2)
  $> ncmp(k,u)<=0:
   r=$A(r,k)
   k=nadd(k,1)
  $! r
 if $((u)is $-:
  if u<0 $) u==$3.$n(u):
   $! '$9'
  try:
   $! gamma(u+1.0)
  $J($I,$<,$M):
   $! '$T' if u>0 $+ '$9'
 $! $*
$. gamma(x):
 try:
  $! $3.gamma(x)
 $J AttributeError:
  pass
 if x<0.5:
  $! $3.pi/($3.sin($3.pi*x)*gamma(1.0-x))
 x-=1.0
 g=7
 c=(0.99999999999980993,676.5203681218851,-1259.1392167224028,
 771.32342877765313,-176.61502916214059,12.507343278686905,
 -0.13857109526572012,9.9843695780195716e-6,1.5056327351493116e-7)
 a=c[0]
 t=x+g+0.5
 $4 k in $j(1,9):
  a+=c[k]/(x+k)
 h=t**((x+0.5)/2)
 $! $3.$O(2*$3.pi)*h*$3.exp(-t)*h*a
$. real_(u):
 if $1(u)or has(u,'i'):
  r,i=reim(u)
  if $2 $%(r,'$h'):
   $! r
 if $B(u):
  $! u
 $! $*
$. imag_(u):
 if $B(u):
  $! 0
 r,i=reim(u)
 if $2 $%(i,'$s'):
  $! i
 $! $*
$. conj_(u):
 if $B(u):
  $! u
 r,i=reim(u)
 if $2 $%(r,'$h'):
  $! sub(r,$A('i',i))
 $! $*
$. angle_(u):
 r,i=reim(u)
 if $%(r,'$h')or $%(i,'$s'):
  $! $*
 if i==0:
  if $1(r):
   v=cv(r)
   if v is $2 $* $) $((v)is $2 $,:
    if v>=0:
     $! 0
    $! 'pi'
  $! $*
 if r==0:
  if $1(i):
   v=cv(i)
   if v is $2 $* $) $((v)is $2 $,:
    $! $A(Q(1 if v>0 $+-1,2),'pi')
  $! $*
 if $1(r)$) $1(i):
  vr=cv(r)
  vi=cv(i)
  if vr is $* or vi is $* or $((vr)is $, or $((vi)is $,:
   $! $*
  a=fn('$b',div(i,r))
  if vr<0:
   if vi>=0:
    a=add(a,'pi')
   $+:
    a=sub(a,'pi')
  $! a
 $! $*
$5['sin']=sin_
$5['cos']=cos_
$5['tan']=tan_
$5['$^']=asin_
$5['$l']=acos_
$5['$b']=atan_
$5['ln']=ln_
$5['log']=log_
$5['abs']=abs_
$5['sign']=sign_
$5['$n']=floor_
$5['ceiling']=ceil_
$5['sinh']=sinh_
$5['cosh']=cosh_
$5['tanh']=tanh_
$5['$x']=odd0('$x')
$5['arctanh']=odd0('arctanh')
$5['arccosh']=$@ u:0 if u==1 $+ $*
$5['fact']=fact_
$5['$h']=real_
$5['$s']=imag_
$5['conj']=conj_
$5['angle']=angle_
$5['exp']=$@ u:pw('e',u)
$5['$O']=$@ u:pw(u,$[)
$5['sec']=$@ u:pw(fn('cos',u),-1)
$5['csc']=$@ u:pw(fn('sin',u),-1)
$5['cot']=$@ u:pw(fn('tan',u),-1)
$5['sech']=$@ u:pw(fn('cosh',u),-1)
$5['csch']=$@ u:pw(fn('sinh',u),-1)
$5['coth']=$@ u:pw(fn('tanh',u),-1)
$5['arcsec']=$@ u:fn('$l',pw(u,-1))
$5['arccsc']=$@ u:fn('$^',pw(u,-1))
$5['arccot']=$@ u:sub($A($[,'pi'),fn('$b',u))
$5['arcsech']=$@ u:fn('arccosh',pw(u,-1))
$5['arccsch']=$@ u:fn('$x',pw(u,-1))
$5['arccoth']=$@ u:fn('arctanh',pw(u,-1))
$. root_(u,n=2):
 $! pw(u,pw(n,-1))
$5['root']=root_
import $N
$. _c(f):
 $. g(x):
  try:
   if $((x)is $,:
    $! f[1](x)
   $! f[0](x)
  $J($M,$w):
   $! f[1]($,(x))
 $! g
$. _ln(x):
 if $((x)is $2 $, $) x>0:
  $! $3.log(x)
 if x==0:
  $! $-('-$T')
 $! $N.log($,(x))
$. _asinr(x):
 if-1<=x<=1:
  $! $3.asin(x)
 $Y $M
$. _acosr(x):
 if-1<=x<=1:
  $! $3.acos(x)
 $Y $M
$. _casin(z):
 $!-1j*$N.log(1j*z+$N.$O(1-z*z))
$. _cacos(z):
 $! $3.pi/2-_casin(z)
$. _catan(z):
 $! 0.5j*$N.log((1-1j*z)/(1+1j*z))
$. _sinh(x):
 $!($N.exp(x)-$N.exp(-x))/2 if $((x)is $, $+($3.exp(x)-$3.exp(-x))/2
$. _cosh(x):
 $!($N.exp(x)+$N.exp(-x))/2 if $((x)is $, $+($3.exp(x)+$3.exp(-x))/2
$. _tanh(x):
 if $((x)is $2 $,:
  if x>20:
   $! 1.0
  if x<-20:
   $!-1.0
  a=$3.exp(2*x)
  $!(a-1)/(a+1)
 a=$N.exp(2*x)
 $!(a-1)/(a+1)
$. _asinh(x):
 if $((x)is $2 $,:
  $! $3.log(x+$3.$O(x*x+1))if x>=0 $+-$3.log(-x+$3.$O(x*x+1))
 $! $N.log(x+$N.$O(x*x+1))
$. _acosh(x):
 if $((x)is $2 $, $) x>=1:
  $! $3.log(x+$3.$O(x*x-1))
 x=$,(x)
 $! $N.log(x+$N.$O(x+1)*$N.$O(x-1))
$. _atanh(x):
 if $((x)is $2 $, $)-1<x<1:
  $! 0.5*$3.log((1+x)/(1-x))
 x=$,(x)
 $! 0.5*$N.log((1+x)/(1-x))
$. _sign(x):
 if $((x)is $,:
  $! x/abs(x)if x!=0 $+ 0.0
 $! 1.0 if x>0 $+(-1.0 if x<0 $+ 0.0)
''')
_x(r'''$. _floor(x):
 if $((x)is $,:
  $! $,($3.$n(x.$h),$3.$n(x.$s))
 $! $-($3.$n(x))
$. _ceil(x):
 if $((x)is $,:
  $! $,($3.ceil(x.$h),$3.ceil(x.$s))
 $! $-($3.ceil(x))
$. _real(x):
 $! x.$h if $((x)is $, $+ x
$. _imag(x):
 $! x.$s if $((x)is $, $+ 0.0
$. _conj(x):
 $! x.conjugate()if $((x)is $, $+ x
$. _angle(x):
 if $((x)is $,:
  $! $N.phase(x)
 $! 0.0 if x>=0 $+ $3.pi
$. _fact(x):
 if $((x)is $,:
  $Y $M
 $! gamma(x+1.0)
NUMF={
 'sin':_c(($3.sin,$N.sin)),'cos':_c(($3.cos,$N.cos)),
 'tan':_c(($3.tan,$@ z:$N.sin(z)/$N.cos(z))),
 '$^':_c((_asinr,_casin)),'$l':_c((_acosr,_cacos)),
 '$b':_c(($3.atan,_catan)),
 'ln':_ln,'exp':_c(($3.exp,$N.exp)),
 '$O':_c(($@ x:$3.$O(x)if x>=0 $+ $N.$O(x),$N.$O)),
 'abs':abs,'sign':_sign,'$n':_floor,'ceiling':_ceil,
 'sinh':_sinh,'cosh':_cosh,'tanh':_tanh,
 '$x':_asinh,'arccosh':_acosh,'arctanh':_atanh,
 '$h':_real,'$s':_imag,'conj':_conj,'angle':_angle,
 'fact':_fact,
 }
$. nfun_call($;,$Z):
 if $;=='log':
  b=$Z[1]if $]($Z)>1 $+ 10.0
  $! _ln($Z[0])/_ln(b)
 if $;=='root':
  n=$Z[1]if $]($Z)>1 $+ 2.0
  $! npow($Z[0],1.0/n)
 if $;=='round':
  d=$Q($Z[1])if $]($Z)>1 $+ 0
  $! round($Z[0],d)
 if $;=='when':
  $! $Z[1]if $Z[0]$+($Z[2]if $]($Z)>2 $+ $-('nan'))
 if $;=='max':
  $! max($Z)
 if $;=='min':
  $! min($Z)
 if $;=='mod':
  $! $Z[0]-$Z[1]*$3.$n($Z[0]/$Z[1])if $Z[1]!=0 $+ $Z[0]
 f=NUMF.get($;)
 if f is $*:
  if $; in('sec','csc','cot','sech','csch','coth'):
   base={'sec':'cos','csc':'sin','cot':'tan','sech':'cosh','csch':'sinh','coth':'tanh'}[$;]
   $! 1.0/NUMF[base]($Z[0])
  if $; in('arcsec','arccsc','arccot','arcsech','arccsch','arccoth'):
   base={'arcsec':'$l','arccsc':'$^','arccot':'$b','arcsech':'arccosh','arccsch':'$x','arccoth':'arctanh'}[$;]
   $! NUMF[base](1.0/$Z[0])
  if $; in('ipart','$Q'):
   $! $-($Q($Z[0]))
  if $;=='fpart':
   $! $Z[0]-$Q($Z[0])
  err("Cannot evaluate "+$;)
 $! f($Z[0])
$. npow(a,b):
 if $((a)is $2 $, $) $((b)is $2 $,:
  if a<0 $)(b!=b or b in($-('$T'),$-('-$T'))or b!=$3.$n(b)):
   $! $,(a)**b
  if a==0 $) b<0:
   $Y $<
  try:
   $! a**b
  $J $I:
   $! $-('$T')
 if a==0:
  $! 0.0
 $! $,(a)**b
NCONST={'pi':$3.pi,'e':$3.e,'i':1j,'$T':$-('$T')}
$. $y(e,env=$*):
 t=$((e)
 if t is $Q:
  try:
   $! $-(e)
  $J $I:
   $! '$T' if e>0 $+('*',-1,'$T')
 if t is $-:
  $! e
 if t is $a:
  if env is $2 $* $) e in env:
   $! env[e]
  v=NCONST.get(e)
  if v is $*:
   err("Not numeric: "+e)
  $! v
 h=e[0]
 if h=='Q':
  $! e[1]/e[2]
 if h=='+':
  s=0.0
  $4 a in e[1:]:
   s=s+$y(a,env)
  $! s
 if h=='*':
  s=1.0
  $4 a in e[1:]:
   s=s*$y(a,env)
  $! s
 if h=='^':
  b=e[1]
  x=e[2]
  if isq(x)$) x[2]%2==1:
   bv=$y(b,env)
   if $((bv)is $2 $, $) bv<0:
    r=(-bv)**(x[1]/x[2])
    $!-r if x[1]%2 $+ r
   $! npow(bv,x[1]/x[2])
  if $((x)is $Q:
   bv=$y(b,env)
   if bv==0 $) x<0:
    $Y $<
   $! bv**x
  $! npow($y(b,env),$y(x,env))
 if h in('$f','mat','$a','Q'):
  err("Not numeric")
 if h=='when':
  c=nbool(e[1],env)
  if c:
   $! $y(e[2],env)
  $! $y(e[3],env)if $](e)>3 $+ $-('nan')
 $Z=[$y(a,env)$4 a in e[1:]]
 $! nfun_call(h,$Z)
$. nbool(c,env):
 h=head(c)
 if h in('<','>','<=','>=','=','/='):
  a=$y(c[1],env)
  b=$y(c[2],env)
  if $((a)is $,:
   a=a.$h
  if $((b)is $,:
   b=b.$h
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
 if h=='$)':
  $4 a in c[1:]:
   if $2 nbool(a,env):
    $! $6
  $! $R
 if h=='or':
  $4 a in c[1:]:
   if nbool(a,env):
    $! $R
  $! $6
 if h=='$2':
  $! $2 nbool(c[1],env)
 if c=='true':
  $! $R
 if c=='false':
  $! $6
 err("Not a condition")
$. nreal(e,env=$*):
 v=$y(e,env)
 if $((v)is $,:
  if abs(v.$s)>1e-9*(1+abs(v.$h)):
   $Y $M
  $! v.$h
 $! v
$. simp(e):
 t=$((e)
 if t is $2 $/:
  $! e
 h=e[0]
 if h=='Q' or h=='$a' or h=='hold':
  if h=='hold':
   $! simp(e[1])
  $! e
 $?=[simp(a)$4 a in e[1:]]
 if h=='+':
  $! $F($?)
 if h=='*':
  $! $C($?)
 if h=='^':
  $! pw($?[0],$?[1])
 if h in('$f','mat','=','<','>','<=','>=','/=','$)','or','$2'):
  $!(h,)+$/($?)
 $! fn(h,$?)
$. subs(e,old,new):
 if e==old:
  $! new
 t=$((e)
 if t is $2 $/ or e[0]=='Q' or e[0]=='$a':
  $! e
 ch=$6
 $?=[]
 $4 a in e[1:]:
  b=subs(a,old,new)
  if b is $2 a:
   ch=$R
  $?.$&(b)
 if $2 ch:
  $! e
 $! simp((e[0],)+$/($?))
$. subsd(e,d):
 t=$((e)
 if t is $a:
  if e in d:
   $! d[e]
  $! e
 if t is $2 $/ or e[0]=='Q' or e[0]=='$a':
  $! e
 ch=$6
 $?=[]
 $4 a in e[1:]:
  b=subsd(a,d)
  if b is $2 a:
   ch=$R
  $?.$&(b)
 if $2 ch:
  $! e
 $! simp((e[0],)+$/($?))
$. mapexpr(f,e):
 if $%(e,'$f'):
  $!('$f',)+$/(mapexpr(f,a)$4 a in e[1:])
 if $%(e,'mat'):
  $!('mat',)+$/(mapexpr(f,a)$4 a in e[1:])
 $! f(e)
''')
_x(r'''$. $_(e):
 t=$((e)
 if t is $2 $/:
  $! e
 h=e[0]
 if h=='Q' or h=='$a':
  $! e
 if h=='+':
  $! $F([$_(a)$4 a in e[1:]])
 if h=='*':
  r=1
  $4 f in e[1:]:
   r=$W(r,$_(f))
  $! r
 if h=='^':
  b=$_(e[1])
  x=$_(e[2])
  if $%(b,'+')$) $((x)is $Q:
   if x>0:
    $! $`(b,x)
   if x<0:
    $! pw($`(b,-x),-1)
  if $%(b,'*')$) $((x)is $Q:
   $! $_($C([pw(f,x)$4 f in b[1:]]))
  if b=='e' $) $%(x,'+'):
   $! $C([pw('e',a)$4 a in x[1:]])
  if $%(x,'+')$) $0(b):
   $! $C([pw(b,a)$4 a in x[1:]])
  $! pw(b,x)
 if h in('$f','mat','=','<','>','<=','>=','/=','$)','or','$2'):
  $!(h,)+$/($_(a)$4 a in e[1:])
 $! fn(h,[$_(a)$4 a in e[1:]])
$. evalf(e):
 t=$((e)
 if t is $Q:
  $! $-(e)
 if t is $-:
  $! e
 if t is $a:
  if e=='pi':
   $! $3.pi
  if e=='e':
   $! $3.e
  $! e
 h=e[0]
 if h=='Q':
  $! e[1]/e[2]
 if h=='$a':
  $! e
 if $1(e)$) h $2 in('$f','mat','=','<','>','<=','>=','/=','$)','or','$2'):
  try:
   v=$y(e)
   if $((v)is $,:
    $! $i(v)
   if v!=v:
    $! '$9'
   if v==$-('$T'):
    $! '$T'
   if v==$-('-$T'):
    $!('*',-1,'$T')
   $! v
  $J($<,$M,$I,$w):
   pass
  $J $7:
   pass
 $?=[evalf(a)$4 a in e[1:]]
 if h=='^' $) $((e[2])is $Q:
  $?[1]=e[2]
 $! simp((h,)+$/($?))
$. exactify(e,tol=$*):
 t=$((e)
 if t is $-:
  $! float2rat(e,tol)
 if t is $/ $) e[0]!='Q' $) e[0]!='$a':
  $! simp((e[0],)+$/(exactify(a,tol)$4 a in e[1:]))
 $! e
$. float2rat(x,tol=$*):
 if x!=x:
  $! '$9'
 if x==$-('$T'):
  $! '$T'
 if x==$-('-$T'):
  $!('*',-1,'$T')
 if x==$3.$n(x)$) abs(x)<1e18:
  $! $Q(x)
 if tol is $*:
  tol=5e-14*max(1.0,abs(x))
 h0,h1=0,1
 k0,k1=1,0
 y=x
 $4 _ in $j(60):
  a=$3.$n(y)
  h0,h1=h1,$Q(a)*h1+h0
  k0,k1=k1,$Q(a)*k1+k0
  if abs(h1/k1-x)<=tol:
   break
  f=y-a
  if f==0:
   break
  y=1.0/f
 $! Q(h1,k1)
$. degree(e,x):
 if freeof(e,x):
  $! 0
 if e==x:
  $! 1
 h=head(e)
 if h=='+':
  d=0
  $4 a in e[1:]:
   k=degree(a,x)
   if k is $*:
    $! $*
   if k>d:
    d=k
  $! d
 if h=='*':
  d=0
  $4 a in e[1:]:
   k=degree(a,x)
   if k is $*:
    $! $*
   d+=k
  $! d
 if h=='^' $) $((e[2])is $Q $) e[2]>0:
  k=degree(e[1],x)
  if k is $*:
   $! $*
  $! k*e[2]
 $! $*
$. coeffs(e,x):
 e=$_(e)
 if freeof(e,x):
  $![e]
 $K=e[1:]if $%(e,'+')$+(e,)
 cs={}
 mx=0
 $4 t in $K:
  if $%(t,'*'):
   k=0
   $H=[]
   $4 f in t[1:]:
    if f==x:
     k+=1
    $L $%(f,'^')$) f[1]==x $) $((f[2])is $Q $) f[2]>0:
     k+=f[2]
    $L freeof(f,x):
     $H.$&(f)
    $+:
     $! $*
   c=$C($H)
  $L t==x:
   k=1
   c=1
  $L $%(t,'^')$) t[1]==x $) $((t[2])is $Q $) t[2]>0:
   k=t[2]
   c=1
  $L freeof(t,x):
   k=0
   c=t
  $+:
   $! $*
  cs[k]=add(cs.get(k,0),c)
  if k>mx:
   mx=k
 $![cs.get(k,0)$4 k in $j(mx+1)]
$. fromcoeffs(cs,x):
 $! $F([$A(cs[k],pw(x,k))$4 k in $j($](cs))])
$. numer_denom(e):
 if $%(e,'*'):
  nu=[]
  de=[]
  $4 f in e[1:]:
   if isq(f):
    nu.$&(f[1])
    de.$&(f[2])
   $L $%(f,'^')$) $0(f[2])$) $=(f[2])<0:
    de.$&(pw(f[1],nneg(f[2])))
   $+:
    nu.$&(f)
  $! $C(nu),$C(de)
 if isq(e):
  $! e[1],e[2]
 if $%(e,'^')$) $0(e[2])$) $=(e[2])<0:
  $! 1,pw(e[1],nneg(e[2]))
 $! e,1
''')
_x(r'''OPT={'uni':$R,'digits':10}
P_LOW=0
P_OR=1
P_AND=2
P_NOT=3
P_REL=4
P_SUM=5
$k=6
P_NEG=7
P_POW=8
P_POST=9
$E=10
USYM={'pi':'\u03c0','$T':'\u221e','theta':'\u03b8'}
REL={'=':'=','<':'<','>':'>','<=':'\u2264','>=':'\u2265','/=':'\u2260'}
PRIO='xyztuvwsrqpnmlkjhgfdcba'
$. fmt(e):
 $! pr(e,$6)[0]
$. ffloat(x):
 if x!=x:
  $! '$9'
 if x==$-('$T'):
  $! USYM['$T']if OPT['uni']$+ '$T'
 if x==$-('-$T'):
  $! '-'+(USYM['$T']if OPT['uni']$+ '$T')
 if x==0:
  $! '0.'
 d=OPT['digits']
 s=('%.'+$a(d)+'g')%x
 m=s
 ex=''
 if 'e' in s:
  m,ex=s.split('e')
  ex=$Q(ex)
  ex='E'+$a(ex)
 if '.' in m:
  m=m.rstrip('0')
 $+:
  m=m+'.'
 $! m+ex
$. fnum(x):
 t=$((x)
 if t is $Q:
  $! $a(x),($E if x>=0 $+ P_NEG)
 if t is $-:
  s=ffloat(x)
  $! s,($E if $2 s.$D('-')$+ P_NEG)
 s=$a(x[1])+'/'+$a(x[2])
 $! s,($k if x[1]>0 $+ P_NEG)
$. psym(e):
 if OPT['uni']$) e in USYM:
  $! USYM[e]
 $! e
$. paren(s,p,need):
 if p<need:
  $! '('+s+')'
 $! s
$. pr(e,$P):
 t=$((e)
 if t is $Q or t is $-:
  $! fnum(e)
 if t is $a:
  $! psym(e),$E
 h=e[0]
 if h=='Q':
  $! fnum(e)
 if h=='+':
  $! pr_sum(e,$P)
 if h=='*':
  $! pr_prod(e,$P)
 if h=='^':
  $! pr_pow(e,$P)
 if h=='hold':
  $! pr(e[1],$R)
 $P=$6
 if h=='$f':
  $! '{'+','.join([pr(a,$P)[0]$4 a in e[1:]])+'}',$E
 if h=='mat' $) $](e)==2:
  $! '['+','.join([pr(a,$P)[0]$4 a in e[1][1:]])+']',$E
 if h=='mat':
  rows=[]
  $4 r in e[1:]:
   rows.$&('['+','.join([pr(a,$P)[0]$4 a in r[1:]])+']')
  $! '['+''.join(rows)+']',$E
 if h=='$a':
  $! '"'+e[1]+'"',$E
 if h in REL:
  op=REL[h]if OPT['uni']$+ h
  a=pr(e[1],$P)
  b=pr(e[2],$P)
  $! paren(a[0],a[1],P_SUM)+op+paren(b[0],b[1],P_SUM),P_REL
 if h=='$)' $) $](e)==3 $) head(e[1])in('<','<=')$) head(e[2])in('<','<=')$) e[1][2]==e[2][1]:
  op1=REL[e[1][0]]if OPT['uni']$+ e[1][0]
  op2=REL[e[2][0]]if OPT['uni']$+ e[2][0]
  $! pr(e[1][1],$6)[0]+op1+pr(e[1][2],$6)[0]+op2+pr(e[2][2],$6)[0],P_REL
 if h=='$)' or h=='or':
  p=P_AND if h=='$)' $+ P_OR
  ss=[]
  $4 a in e[1:]:
   s,q=pr(a,$P)
   ss.$&(paren(s,q,p+1))
  $!(' '+h+' ').join(ss),p
 if h=='$2':
  s,q=pr(e[1],$P)
  $! '$2 '+paren(s,q,P_NOT+1),P_NOT
 if h=='abs':
  $! '|'+pr(e[1],$P)[0]+'|',$E
 if h=='fact':
  s,q=pr(e[1],$P)
  $! paren(s,q,$E)+'!',P_POST
 if h=='log':
  if $](e)==2 or e[2]==10:
   $! 'log10('+pr(e[1],$P)[0]+')',$E
  $! 'log('+pr(e[1],$P)[0]+','+pr(e[2],$P)[0]+')',$E
 if h=='call':
  $! e[1]+'('+','.join([pr(a,$P)[0]$4 a in e[2:]])+')',$E
 if h=='prime':
  $! e[1]+"'"*e[2],$E
 if h=='integral':
  nm='\u222b' if OPT['uni']$+ 'integral'
  $! nm+'('+','.join([pr(a,$P)[0]$4 a in e[1:]])+')',$E
 if h=='sumseq':
  nm='\u03a3' if OPT['uni']$+ 'sumseq'
  $! nm+'('+','.join([pr(a,$P)[0]$4 a in e[1:]])+')',$E
 if h=='prodseq':
  nm='\u03a0' if OPT['uni']$+ 'prodseq'
  $! nm+'('+','.join([pr(a,$P)[0]$4 a in e[1:]])+')',$E
 if h=='$O' or h=='root':
  pass
 h=TINAME.get(h,h)
 $! h+'('+','.join([pr(a,$P)[0]$4 a in e[1:]])+')',$E
TINAME={'ncr':'nCr','npr':'nPr'}
MAINV='xyzt'
$. varprio(v):
 i=MAINV.find(v)if $](v)==1 $+-1
 if i<0:
  $!(100,v)
 $!(i,v)
$. facprio(v):
 i=MAINV.find(v)if $](v)==1 $+-1
 if i<0:
  $!(0,v)
 $!(1,$a(i))
$. termdegs(t,d):
 c,r=$:(t)
 fs=r[1:]if $%(r,'*')$+(r,)
 $4 f in fs:
  if $((f)is $a $) f $2 in $o:
   d[f]=d.get(f,0)+1
  $L $%(f,'^')$) $((f[1])is $a $) f[1]$2 in $o $) $0(f[2]):
   d[f[1]]=d.get(f[1],0)+tofl(f[2])
  $L $%(f,'^')$) $0(f[2]):
   $4 v in symbols(f[1]):
    d[v]=d.get(v,0)+tofl(f[2])*0.001
  $L $2 $0(f)$) $((f)is $2 $a:
   $4 v in symbols(f):
    d[v]=d.get(v,0)+0.0001
$. sumkeys($K):
 vs=[]
 degs=[]
 $4 t in $K:
  d={}
  termdegs(t,d)
  degs.$&(d)
  $4 v in d:
   if v $2 in vs:
    vs.$&(v)
 vs.sort(key=varprio)
 mv=[v $4 v in vs if varprio(v)[0]<100]
 ov=[v $4 v in vs if varprio(v)[0]>=100]
 keys=[]
 $4 k in $j($]($K)):
  t=$K[k]
  d=degs[k]
  if $0(t):
   keys.$&((2,(),0,0,(),''))
  $L $2 d:
   cat=3 if has(t,'i')$+ 1
   keys.$&((cat,(),0,1 if $e(t)$+ 0,(),okey($:(t)[1])))
  $+:
   keys.$&((0,$/([-d.get(v,0)$4 v in mv]),-sum([d.get(v,0)$4 v in ov]),
 1 if $e(t)$+ 0,$/([-d.get(v,0)$4 v in ov]),okey($:(t)[1])))
 $! keys
$. pr_sum(e,$P):
 $K=$f(e[1:])
 if $2 $P:
  ks=sumkeys($K)
  idx=$f($j($]($K)))
  idx.sort(key=$@ i:ks[i])
  $K=[$K[i]$4 i in idx]
 $g=''
 first=$R
 $4 t in $K:
  s,p=pr(t,$6)
  if p<P_SUM+1 $) $2 s.$D('-')$) p<=P_SUM:
   s='('+s+')'
  if first:
   $g=s
   first=$6
  $L s.$D('-'):
   $g+=s
  $+:
   $g+='+'+s
 $! $g,P_SUM
$. fackey(f):
 if f=='pi' or f=='e' or isrrad(f)or $0(f):
  $!(0,(0,''),okey(f))
 if f=='i':
  $!(3,(0,''),'')
 if $((f)is $a:
  $!(1,facprio(f),'')
 if $%(f,'^')$) $((f[1])is $a:
  if f[1]=='e':
   $!(2,(0,''),okey(f))
  $!(1,facprio(f[1]),okey(f))
 if $%(f,'+')or($%(f,'^')$) $%(f[1],'+')):
  $!(4,(0,''),okey(f))
 $!(2,(0,''),okey(f))
$. pr_factor(f,$P,first):
 s,p=pr(f,$P)
 if p<$k or(p==$k $) $2 first)or(s.$D('-')$) $2 first):
  $! '('+s+')'
 $! s
''')
_x(r'''$. pr_prod(e,$P):
 fs=$f(e[1:])
 $G=1
 if fs $) $0(fs[0])$) $2 $P:
  $G=fs[0]
  fs=fs[1:]
 $c=[]
 den=[]
 $4 f in fs:
  if $%(f,'^')$) $0(f[2])$) $=(f[2])<0:
   ex=nneg(f[2])
   den.$&(f[1]if ex==1 $+('^',f[1],ex))
  $L isq(f)$) $P:
   $c.$&(f[1])
   den.$&(f[2])
  $+:
   $c.$&(f)
 if $2 $P:
  $c.sort(key=fackey)
  den.sort(key=fackey)
 sign=''
 if $P $) $c $) $0($c[0])$) $=($c[0])<0:
  sign='-'
  if $c[0]==-1:
   $c=$c[1:]
  $+:
   $c[0]=nneg($c[0])
 cn=$G
 cd=1
 if $0($G):
  if $=($G)<0:
   sign='-'
   $G=nneg($G)
  if isq($G):
   cn=$G[1]
   cd=$G[2]
  $+:
   cn=$G
 if $P:
  $c=[f $4 f in $c if f!=1]or[1]
 if sign $) den $) $2 $P:
  sums=[k $4 k in $j($]($c))if $%($c[k],'+')]
  dsums=[k $4 k in $j($](den))if $%(den[k],'+')]
  if $](sums)==1 $) any([$e(t)$4 t in $c[sums[0]][1:]]):
   $c=$f($c)
   $c[sums[0]]=$A(-1,$c[sums[0]])
   sign=''
  $L $](dsums)==1 $) $2 sums $) $](den[dsums[0]])==3 $) $1(den[dsums[0]])$) any([$e(t)$4 t in den[dsums[0]][1:]]):
   den=$f(den)
   den[dsums[0]]=$A(-1,den[dsums[0]])
   sign=''
 $r=[]
 if cn!=1 or $((cn)is $-:
  $r.$&(fnum(cn)[0])
 $4 f in $c:
  $r.$&(pr_factor(f,$6,$2 $r))
 if $2 $r:
  $r.$&('1')
 ns='*'.join($r)
 if cd!=1:
  den.insert(0,cd)
 if $2 den:
  if sign $) $]($c)==1 $) cn==1 $) pr($c[0],$6)[1]<=P_SUM:
   $! sign+'('+pr($c[0],$6)[0]+')',P_NEG
  $! sign+ns,(P_NEG if sign $+ $k)
 if $]($r)==1 $) $]($c)==1 $) cn==1:
  s,p=pr($c[0],$6)
  ns=paren(s,p,$k+1)if p<$k $+ s
  if s.$D('-'):
   ns='('+s+')'
 dparts=[]
 $4 f in den:
  dparts.$&(pr_factor(f,$6,$2 dparts))
 ds='*'.join(dparts)
 if $](den)>1:
  ds='('+ds+')'
 $+:
  s,p=pr(den[0],$6)
  if p<=$k or s.$D('-'):
   ds='('+s+')'
 $! sign+ns+'/'+ds,(P_NEG if sign $+ $k)
$. pr_pow(e,$P):
 b=e[1]
 x=e[2]
 if $0(x)$) $=(x)<0 $) $2 $P:
  ex=nneg(x)
  d=b if ex==1 $+('^',b,ex)
  s,p=pr(d,$6)
  if p<=$k or s.$D('-'):
   s='('+s+')'
  $! '1/'+s,$k
 if x==$[:
  s,p=pr(b,$6)
  if OPT['uni']:
   if($((b)is $Q $) b>=0)or($((b)is $a):
    $! '\u221a'+s,P_POW
   $! '\u221a('+s+')',$E
  $! '$O('+s+')',$E
 bs,bp=pr(b,$6)
 if bp<=P_POW or bs.$D('-')or $%(b,'fact'):
  bs='('+bs+')'
 xs,xp=pr(x,$6)
 if $2(($((x)is $Q $) x>=0)or($((x)is $a)):
  xs='('+xs+')'
 $! bs+'^'+xs,P_POW
$. fmt_top(e):
 if $%(e,'mat')$) $](e)>2:
  rows=[]
  $4 r in e[1:]:
   rows.$&('['+','.join([fmt(a)$4 a in r[1:]])+']')
  if sum([$](r)$4 r in rows])>28:
   $! '['+('\n '.join(rows))+']'
  $! '['+''.join(rows)+']'
 if $%(e,'$a'):
  $! e[1]
 $! fmt(e)
''')
_x(r'''REPL=(
 ('**','^'),('==','='),('!=','/='),
 ('sin\u207b\u00b9','$^'),('cos\u207b\u00b9','$l'),('tan\u207b\u00b9','$b'),
 ('\u2212','-'),('\u2013','-'),('\u00d7','*'),('\u00b7','*'),
 ('\u2022','*'),('\u22c5','*'),('\u00f7','/'),('\u2264','<='),
 ('\u2265','>='),('\u2260','/='),('\u2192','->'),('\u21d2','=>'),
 ('\u21d4','<=>'),('\u207b\u00b9','^(-1)'),('\u00b2','^2'),
 ('\u00b3','^3'),('\u03c0',' pi '),('\u221e',' $T '),
 ('\u212f',' e '),('\u2148',' i '),('\u03b8','theta'),
 ('\u222b',' integral'),('\u03a3',' sumseq'),('\u2211',' sumseq'),
 ('\u03a0',' prodseq'),('\u220f',' prodseq'),('\u1d07','E'),
 ('\u2032',"'"),('\u2033',"''"),('@i',' i '),('@e',' e '),
 ('@>','\u25ba'),('@d','\u00b0'),('@t','\u1d40'),('\u2044','/'),
 ('infinity','$T'),('\u03b1','alpha'),('\u03b2','beta'),
 ('\u03bb','$@'),('\u03bc','mu'),('\u03c3','sigma'),
 ('\u0394','delta'),
 )
OPS=('<=>','=>','->','=:',':=','<=','>=','/=','<>','.^','.*',
 './','.+','.-','>>','+','-','*','/','^','(',')','{','}',
 '[',']',',',';','=','<','>','|','!','%','&','\u00b0',
 '\u2220','\u25ba','\u221a',"'",'\u1d40')
KEYW=('$)','or','xor','$2','nor','nand')
NOTLETTER='\u221a\u00b0\u2220\u25ba\u1d40'
$. normalize(s):
 $4 a,b in REPL:
  if a in s:
   s=s.replace(a,b)
 $! s
$. isletter(c):
 if c=='_':
  $! $R
 o=ord(c)
 if o>127:
  $! c $2 in NOTLETTER
 $!('a'<=c<='z')or('A'<=c<='Z')
$. isdig(c):
 $! '0'<=c<='9'
$. tokenize(s):
 s=normalize(s)
 toks=[]
 i=0
 n=$](s)
 $> i<n:
  c=s[i]
  if c==' ' or c=='\t':
   i+=1
   $8
  if c=='0' $) i+2<n $) s[i+1]in 'bBhH':
   base=2 if s[i+1]in 'bB' $+ 16
   j=i+2
   dg='01' if base==2 $+ '0123456789abcdefABCDEF'
   $> j<n $) s[j]in dg:
    j+=1
   if j>i+2:
    toks.$&(('$c',$Q(s[i+2:j],base)))
    i=j
    $8
  if isdig(c)or(c=='.' $) i+1<n $) isdig(s[i+1])):
   j=i
   $> j<n $) isdig(s[j]):
    j+=1
   isf=$6
   if j<n $) s[j]=='.' $) $2(j+1<n $) s[j+1]in '^*/+-' $) $2 isdig(s[j+1])):
    isf=$R
    j+=1
    $> j<n $) isdig(s[j]):
     j+=1
   if j<n $)(s[j]=='E' or(s[j]=='e' $) j+1<n $) isdig(s[j+1]))):
    k=j+1
    if k<n $) s[k]in '+-':
     k+=1
    if k<n $) isdig(s[k]):
     isf=$R
     j=k
     $> j<n $) isdig(s[j]):
      j+=1
   txt=s[i:j]
   if isf:
    toks.$&(('$c',$-(txt)))
   $+:
    toks.$&(('$c',$Q(txt)))
   i=j
   $8
  if isletter(c):
   j=i
   $> j<n $)(isletter(s[j])or isdig(s[j])):
    j+=1
   $;=s[i:j].lower()
   toks.$&(('id',$;))
   i=j
   k=0
   $> i<n $) s[i]=="'":
    k+=1
    i+=1
   if k:
    toks.$&(('prime',k))
   $8
  if c=='"':
   j=s.find('"',i+1)
   if j<0:
    $Y $7('Missing "')
   toks.$&(('$a',s[i+1:j]))
   i=j+1
   $8
  $4 op in OPS:
   if s.$D(op,i):
    i+=$](op)
    if op=='<>':
     op='/='
    if op=='>>':
     op='\u25ba'
    toks.$&(('op',op))
    break
  $+:
   $Y $7('Invalid character: '+c)
 toks.$&(('end',$*))
 $! toks
''')
_x(r'''class Parser:
 $. __init__($#,toks,$u):
  $#.t=toks
  $#.i=0
  $#.$u=$u
 $. peek($#):
  $! $#.t[$#.i]
 $. $q($#):
  tk=$#.t[$#.i]
  $#.i+=1
  $! tk
 $. $U($#,op):
  tk=$#.t[$#.i]
  $! tk[0]=='op' $) tk[1]==op
 $. isid($#,$;):
  tk=$#.t[$#.i]
  $! tk[0]=='id' $) tk[1]==$;
 $. expect($#,op):
  if $2 $#.$U(op):
   tk=$#.peek()
   $Y $7('Missing '+op)
  $#.i+=1
 $. top($#):
  e=$#.store()
  $> $#.$U('\u25ba'):
   $#.$q()
   tk=$#.$q()
   if tk[0]!='id':
    $Y $7('Syntax error after conversion')
   $?=[]
   if $#.$U('('):
    $#.$q()
    $?=$#.$?(')')
   e=('conv',e,tk[1])+$/($?)
  if $#.peek()[0]!='end':
   tk=$#.peek()
   $Y $7('Syntax error near '+$a(tk[1])if tk[1]is $2 $* $+ 'Syntax error')
  $! e
 $. store($#):
  if $#.isid('define'):
   $#.$q()
   lhs=$#.sum()
   if $2 $#.$U('='):
    $Y $7('Define needs =')
   $#.$q()
   rhs=$#.wth()
   $!('define',lhs,rhs)
  e=$#.wth()
  if $#.$U('->')or $#.$U('=:'):
   $#.$q()
   tgt=$#.wth()
   $!('store',e,tgt)
  if $#.$U(':='):
   $#.$q()
   rhs=$#.wth()
   $!('define',e,rhs)
  $! e
 $. wth($#):
  e=$#.iff()
  $> $#.$U('|'):
   $#.$q()
   c=$#.iff()
   e=('|',e,c)
  $! e
 $. iff($#):
  e=$#.imp()
  $> $#.$U('<=>'):
   $#.$q()
   e=('<=>',e,$#.imp())
  $! e
 $. imp($#):
  e=$#.xor()
  $> $#.$U('=>'):
   $#.$q()
   e=('=>',e,$#.xor())
  $! e
 $. xor($#):
  e=$#.lor()
  $> $#.isid('xor')or $#.isid('nor')or $#.isid('nand'):
   op=$#.$q()[1]
   e=(op,e,$#.lor())
  $! e
 $. lor($#):
  e=$#.land()
  $> $#.isid('or'):
   $#.$q()
   e=('or',e,$#.land())
  $! e
 $. land($#):
  e=$#.lnot()
  $> $#.isid('$)'):
   $#.$q()
   e=('$)',e,$#.lnot())
  $! e
 $. lnot($#):
  if $#.isid('$2'):
   $#.$q()
   $!('$2',$#.lnot())
  $! $#.rel()
 $. rel($#):
  a=$#.sum()
  tk=$#.peek()
  if tk[0]=='op' $) tk[1]in('=','/=','<','>','<=','>='):
   $#.$q()
   b=$#.sum()
   r=(tk[1],a,b)
   tk2=$#.peek()
   if tk2[0]=='op' $) tk2[1]in('<','>','<=','>='):
    $#.$q()
    c=$#.sum()
    r=('$)',r,(tk2[1],b,c))
   $! r
  $! a
 $. sum($#):
  a=$#.prod()
  $> $R:
   tk=$#.peek()
   if tk[0]=='op' $) tk[1]in('+','-','.+','.-','&'):
    $#.$q()
    b=$#.prod()
    op=tk[1]
    if op=='.+':
     op='+'
    $L op=='.-':
     op='-'
    a=(op,a,b)
   $+:
    $! a
 $. startsprimary($#):
  tk=$#.peek()
  if tk[0]=='$c' or tk[0]=='$a':
   $! $R
  if tk[0]=='id':
   $! tk[1]$2 in KEYW
  if tk[0]=='op':
   $! tk[1]in('(','{','\u221a')
  $! $6
 $. prod($#):
  a=$#.unary()
  $> $R:
   tk=$#.peek()
   if tk[0]=='op' $) tk[1]in('*','/','.*','./'):
    $#.$q()
    b=$#.unary()
    op=tk[1]
    a=(op,a,b)
   $L $#.startsprimary():
    b=$#.pw()
    a=('*',a,b)
   $+:
    $! a
 $. unary($#):
  if $#.$U('-'):
   $#.$q()
   $!('$t',$#.unary())
  if $#.$U('+'):
   $#.$q()
   $! $#.unary()
  $! $#.pw()
 $. pw($#):
  b=$#.post()
  if $#.$U('^')or $#.$U('.^'):
   op=$#.$q()[1]
   if $#.$U('\u1d40')or $#.isid('t')$) $6:
    pass
   x=$#.unary()
   $!('^' if op=='^' $+ '.^',b,x)
  $! b
 $. post($#):
  a=$#.primary()
  $> $R:
   if $#.$U('!'):
    $#.$q()
    a=('!',a)
   $L $#.$U('%'):
    $#.$q()
    a=('%',a)
   $L $#.$U('\u00b0'):
    $#.$q()
    a=('deg',a)
   $L $#.$U('\u1d40'):
    $#.$q()
    a=('call','transpose',a)
   $L $#.$U('['):
    $#.$q()
    idx=$#.$?(']')
    a=('index',a)+$/(idx)
   $+:
    $! a
 $. $?($#,close):
  $g=[]
  if $#.$U(close):
   $#.$q()
   $! $g
  $> $R:
   $g.$&($#.store_in())
   if $#.$U(','):
    $#.$q()
    $8
   $#.expect(close)
   $! $g
 $. store_in($#):
  e=$#.wth()
  $! e
 $. primary($#):
  tk=$#.$q()
  k=tk[0]
  if k=='$c':
   $! tk[1]
  if k=='$a':
   $!('$a',tk[1])
  if k=='id':
   $;=tk[1]
   if $; in KEYW:
    $Y $7('Syntax error: '+$;)
   if $#.peek()[0]=='prime':
    n=$#.$q()[1]
    if $#.$U('('):
     $#.$q()
     a=$#.$?(')')
     $!('primecall',$;,n)+$/(a)
    $!('prime',$;,n)
   if $#.$U('(')$)($#.$u($;)or($]($;)>1 $) $; $2 in('pi','$T','$9','theta'))):
    $#.$q()
    a=$#.$?(')')
    $!('call',$;)+$/(a)
   $! $;
  if k=='op':
   op=tk[1]
   if op=='(':
    e=$#.store_in()
    if $#.$U('\u2220'):
     $#.$q()
     th=$#.store_in()
     $#.expect(')')
     $!('polar',e,th)
    $#.expect(')')
    $! e
   if op=='{':
    $!('$f',)+$/($#.$?('}'))
   if op=='[':
    $! $#.matrix()
   if op=='\u221a':
    $!('call','$O',$#.post())
   if op=='-':
    $!('$t',$#.pw())
  if k=='end':
   $Y $7('Incomplete expression')
  $Y $7('Syntax error near '+$a(tk[1]))
 $. matrix($#):
  rows=[]
  if $#.$U('['):
   $> $#.$U('['):
    $#.$q()
    rows.$&(('$f',)+$/($#.$?(']')))
    if $#.$U(','):
     $#.$q()
   $#.expect(']')
  $+:
   row=[]
   $> $R:
    if $#.$U(']'):
     $#.$q()
     break
    row.$&($#.store_in())
    if $#.$U(','):
     $#.$q()
    $L $#.$U(';'):
     $#.$q()
     rows.$&(('$f',)+$/(row))
     row=[]
    $L $#.$U(']'):
     $8
    $+:
     $Y $7('Missing ]')
   rows.$&(('$f',)+$/(row))
  n=$](rows[0])
  $4 r in rows:
   if $](r)!=n:
    $Y $7('Dimension error')
  $!('mat',)+$/(rows)
''')
_x(r'''$. parse(s,$u):
 toks=tokenize(s)
 if toks[0][0]=='end':
  $Y $7('Empty input')
 $! Parser(toks,$u).top()
''')
_x(r'''ENV={}
UFUN={}
ST={'ans':0,'deg':$6,'tmp':[]}
TRIG=('sin','cos','tan','sec','csc','cot')
ATRIG=('$^','$l','$b','arcsec','arccsc','arccot')
ALIAS={'asin':'$^','acos':'$l','atan':'$b','ceil':'ceiling',
 'asinh':'$x','acosh':'arccosh','atanh':'arctanh'}
$. $c(a,what='an integer'):
 if $2 isint(a):
  err('Argument must be '+what)
 $! a
$. x_log(u,b=$*):
 $! fn('ln',u)if b is $* $+ fn('log',u,b)
$. x_root(u,n=2):
 $! fn('root',u,n)
$. x_gcd(a,b):
 $! igcd($c(a),$c(b))
$. x_lcm(a,b):
 $! ilcm($c(a),$c(b))
$. x_mod(a,b):
 if $%(a,'^')$) isint(a[1])$) isint(a[2])$) a[2]>0 $) isint(b)$) b:
  r=1
  m=abs(b)
  x=a[1]%m
  e=a[2]
  $> e:
   if e&1:
    r=r*x%m
   x=x*x%m
   e>>=1
  $! r-m if b<0 $) r $+ r
 if $0(a)$) $0(b):
  if b==0:
   $! a
  $! nsub(a,$m(b,$}(ndiv(a,b))))
 $!('mod',a,b)
$. x_ncr(n,k):
 $c(n)
 $c(k)
 if k<0 or k>n:
  $! 0
 k=min(k,n-k)
 if k*ibits(n)>MAXBITS:
  err('Result too large')
 r=1
 $4 i in $j(k):
  r=r*(n-i)//(i+1)
 $! r
$. x_npr(n,k):
 $c(n)
 $c(k)
 if k<0 or k>n:
  $! 0
 if k*ibits(n)>MAXBITS:
  err('Result too large')
 r=1
 $4 i in $j(k):
  r*=n-i
 $! r
$. primes(n):
 $g=[]
 p=2
 step=0
 $> p*p<=n:
  if n%p==0:
   k=0
   $> n%p==0:
    n//=p
    k+=1
   $g.$&((p,k))
  p+=1 if p<3 $+ 2
  step+=1
  if step>300000:
   err('Factor too large to find')
 if n>1:
  $g.$&((n,1))
 $! $g
$. x_factor(a):
 if $2 $d(a):
  err('Argument must be an integer or a fraction')
 n,d=nd(a)
 if n==0:
  $! 0
 fs=[-1]if n<0 $+[]
 $4 p,k in primes(abs(n)):
  fs.$&(p if k==1 $+('^',p,k))
 $4 p,k in primes(d):
  fs.$&(('^',p,-k))
 if $2 fs or fs==[-1]:
  $! n
 if $](fs)==1:
  $!('hold',fs[0])
 $!('hold',('*',)+$/(fs))
$. x_approx(a):
 $! evalf(a)
$. x_exact(a):
 $! exactify(a)
$. x_expand(a):
 $! $_(a)
EXTRA={'log':x_log,'log10':$@ u:fn('log',u,10),'root':x_root,
 '$O':$@ u:fn('$O',u),'gcd':x_gcd,'lcm':x_lcm,
 'mod':x_mod,'ncr':x_ncr,'npr':x_npr,'factor':x_factor,
 'approx':x_approx,'exact':x_exact,'$_':x_expand,
 'numer':$@ a:numer_denom(a)[0],'denom':$@ a:numer_denom(a)[1]}
$. $u(n):
 $!(n in $5 or n in EXTRA or n in ALIAS or n in UFUN
 or n in ST['tmp'])
$. ev(t):
 tt=$((t)
 if tt is $Q or tt is $-:
  $! t
 if tt is $a:
  if t in ENV:
   $! ENV[t]
  if t=='ans':
   $! ST['ans']
  $! t
 h=t[0]
 if h=='+':
  $! add(ev(t[1]),ev(t[2]))
 if h=='-':
  $! sub(ev(t[1]),ev(t[2]))
 if h=='*':
  $! $A(ev(t[1]),ev(t[2]))
 if h=='/':
  $! div(ev(t[1]),ev(t[2]))
 if h=='^':
  $! pw(ev(t[1]),ev(t[2]))
 if h=='$t':
  $! $t(ev(t[1]))
 if h=='!':
  $! fn('fact',ev(t[1]))
 if h=='%':
  $! div(ev(t[1]),100)
 if h=='deg':
  v=ev(t[1])
  $! v if ST['deg']$+ $A(v,div('pi',180))
 if h=='call':
  $! call(t[1],t[2:])
 if h=='|':
  $! ev_with(t[1],t[2])
 if h=='define':
  $! define(t[1],t[2])
 if h=='store':
  $! define(t[2],t[1])
 if h in('=','<','>','<=','>=','/='):
  $! relation(h,ev(t[1]),ev(t[2]))
 if h=='$f':
  $!('$f',)+$/(ev(a)$4 a in t[1:])
 err('Not available in ncasx: '+$a(h))
$. call($;,raw):
 $;=ALIAS.get($;,$;)
 $?=[ev(a)$4 a in raw]
 if $; in UFUN:
  params,body=UFUN[$;]
  if $]($?)!=$](params):
   err('Wrong number of arguments')
  $! subsd(body,dict(zip(params,$?)))
 if ST['deg']$) $; in TRIG $) $]($?)==1:
  $?[0]=$A($?[0],div('pi',180))
 f=EXTRA.get($;)
 try:
  r=f(*$?)if f is $2 $* $+ fn($;,*$?)
 $J $w:
  err('Wrong number of arguments $4 '+$;)
 if ST['deg']$) $; in ATRIG:
  r=$A(r,div(180,'pi'))
 $! r
$. ev_with(e,cond):
 d={}
 cs=[cond]
 $> cs:
  c=cs.pop()
  if $%(c,'$)'):
   cs.$&(c[1])
   cs.$&(c[2])
  $L $%(c,'=')$) $((c[1])is $a:
   d[c[1]]=ev(c[2])
  $+:
   err('Use expr|x=value')
 saved={}
 $4 k in d:
  if k in ENV:
   saved[k]=ENV.pop(k)
 try:
  v=ev(e)
 finally:
  ENV.update(saved)
 $! subsd(v,d)
$. define(lhs,rhs):
 if $%(lhs,'call'):
  $;=lhs[1]
  params=$f(lhs[2:])
  $4 p in params:
   if $((p)is $2 $a:
    err('Invalid parameter')
  saved={}
  $4 p in params:
   if p in ENV:
    saved[p]=ENV.pop(p)
  try:
   body=ev(rhs)
  finally:
   ENV.update(saved)
  UFUN[$;]=(params,body)
  $!('$a','Done')
 if $((lhs)is $2 $a or lhs in $o or $u(lhs):
  err('Invalid variable $;')
 v=ev(rhs)
 ENV[lhs]=v
 $! v
$. relation(op,a,b):
 d=sub(a,b)
 if $0(d)$) $((d)is $2 $,:
  s=$=(d)
  ok={'=':s==0,'/=':s!=0,'<':s<0,'>':s>0,
 '<=':s<=0,'>=':s>=0}[op]
  $! 'true' if ok $+ 'false'
 if $1(d):
  v=$y(d)
  if $((v)is $-:
   ok={'=':abs(v)<1e-12,'/=':abs(v)>=1e-12,'<':v<0,'>':v>0,
 '<=':v<=0,'>=':v>=0}[op]
   $! 'true' if ok $+ 'false'
 $!(op,a,b)
$. register(s):
 low=s.replace(' ','')
 $4 part in(low.split(':=')[0],low.split('->')[-1]):
  i=part.find('(')
  if i>0 $) part[:i].isalpha()$) part[:i]$2 in ST['tmp']:
   ST['tmp'].$&(part[:i])
$. decimal(r):
 if $((r)is $Q or $((r)is $- or $2 $1(r)or has(r,'i'):
  $! $*
 if $((r)is $/ $) r[0]in('$a','hold'):
  $! $*
 try:
  v=evalf(r)
 $J Exception:
  $! $*
 if $((v)is $- or($((v)is $/ $) $1(v)):
  $! fmt(v)
 $! $*
''')
_x(r'''$. run(s):
 s=s.strip()
 if $2 s:
  $! ''
 low=s.lower()
 if low in('deg',':deg','degree'):
  ST['deg']=$R
  $! 'Degree mode'
 if low in('rad',':rad','radian'):
  ST['deg']=$6
  $! 'Radian mode'
 if low.$D('digits')or low.$D(':digits'):
  n=low.split()[-1]
  OPT['digits']=max(1,min(15,$Q(n)))if n.isdigit()$+ 10
  $! 'Digits: '+$a(OPT['digits'])
 if low in('clear',':clear'):
  ENV.clear()
  UFUN.clear()
  $! 'Cleared'
 register(s)
 r=ev(parse(s,$u))
 if $%(r,'$a'):
  $! r[1]
 if $%(r,'hold'):
  ST['ans']=simp(r[1])
  $! fmt(r)
 ST['ans']=r
 $g=fmt(r)
 d=decimal(r)
 if d is $2 $* $) d!=$g:
  sep='  \u2248 ' if OPT['uni']$+ '  ~ '
  if $]($g)+$](d)+4>32:
   sep='\n  \u2248 ' if OPT['uni']$+ '\n  ~ '
  $g+=sep+d
 $! $g
$. xcalc():
 print('nCAS exact calculator')
 print('Type an expression; q quits')
 blank=0
 $> $R:
  try:
   s=input('deg> ' if ST['deg']$+ '> ')
  $J(EOFError,KeyboardInterrupt):
   break
  s=s.strip()
  if s.lower()in('q','quit','exit'):
   break
  if $2 s:
   blank+=1
   if blank>=2:
    print('($( q $) enter to quit)')
    blank=0
   $8
  blank=0
  try:
   $g=run(s)
  $J $7 as ex:
   $g='Error: '+$a(ex)
  $J $<:
   $g='Error: Division by zero'
  $J MemoryError:
   $g='Error: Out of memory'
  $J KeyboardInterrupt:
   $g='Break'
  $J RuntimeError:
   $g='Error: Too $,'
  $J Exception as ex:
   $g='Error: '+$a(ex)
  if $g:
   print($g)
''')
del _x
xcalc()
