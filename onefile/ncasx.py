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
 for s in _L.pop(m, ()):
  exec(_u(s), globals())""")
print('Loading nCAS...')
_W={'!': 'return', '#': 'self', '%': 'isnode', '&': 'append', '(': 'type', ')': 'None', '*': 'and', '+': 'else', ',': 'complex', '-': 'float', '.': 'def', '/': 'tuple', '0': 'isnum', '1': 'isconst', '2': 'not', '3': 'math', '4': 'for', '5': 'FSIMP', '6': 'False', '7': 'continue', '8': 'undef', '9': 'coef_rest', ':': 'CASError', ';': 'name', '<': 'ZeroDivisionError', '=': 'while', '>': 'args', '?': 'nsign', '@': 'lambda', 'A': 'mul', 'B': 'isreal_expr', 'C': 'mul_list', 'D': 'startswith', 'E': 'P_ATOM', 'F': 'add_list', 'G': 'coef', 'H': 'rest', 'I': 'OverflowError', 'J': 'except', 'K': 'elif', 'L': 'ValueError', 'M': 'cmath', 'N': 'sqrt', 'O': 'keep', 'P': 'terms', 'Q': 'int', 'R': 'True', 'S': 'hasfloat', 'T': 'inf', 'U': 'isop', 'V': 'rationalize_inv', 'W': 'expand_mul', 'X': 'facs', 'Y': 'HALF', 'Z': 'vals', '[': 'raise', ']': 'arcsin', '^': 'expand', '_': 'expand_pow', '`': 'len', 'a': 'str', 'b': 'arctan', 'c': 'num', 'd': 'israt', 'e': 'isneg', 'f': 'list', 'g': 'out', 'h': 'real', 'i': 'fromcomplex', 'j': 'P_PROD', 'k': 'arccos', 'l': 'nmul', 'm': 'floor', 'n': 'range', 'o': 'SPECIAL', 'p': 'reim_generic', 'q': 'nxt', 'r': 'parts', 's': 'imag', 't': 'isfunc', 'u': 'radorder', 'v': 'TypeError', 'w': 'arcsinh', 'x': 'nval', 'y': 'outs', 'z': 'fvalc', '{': 'neg', '|': 'isposconst', '}': 'nfloor', '~': 'trig_table'}
_x(r'''import $3
class $:(Exception):
 pass
$. err(msg):
 $[ $:(msg)
CONSTS=('pi','e','i')
$o=('pi','e','i','$T','$8','true','false')
$. igcd(a,b):
 if a<0:
  a=-a
 if b<0:
  b=-b
 $= b:
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
$Y=('Q',1,2)
$. isq(x):
 $! $((x)is $/ $* x[0]=='Q'
$. isint(x):
 $! $((x)is $Q
$. isfl(x):
 $! $((x)is $-
$. $d(x):
 t=$((x)
 $! t is $Q or(t is $/ $* x[0]=='Q')
$. $0(x):
 t=$((x)
 $! t is $Q or t is $- or(t is $/ $* x[0]=='Q')
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
 if ta is $Q $* tb is $Q:
  $! a+b
 if ta is $- or tb is $-:
  $! tofl(a)+tofl(b)
 an,ad=nd(a)
 bn,bd=nd(b)
 $! Q(an*bd+bn*ad,ad*bd)
$. $l(a,b):
 ta=$((a)
 tb=$((b)
 if ta is $Q $* tb is $Q:
  $! a*b
 if ta is $- or tb is $-:
  $! tofl(a)*tofl(b)
 an,ad=nd(a)
 bn,bd=nd(b)
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
 $! $l(a,ninv(b))
$. $?(a):
 if $((a)is $/:
  a=a[1]
 if a>0:
  $! 1
 if a<0:
  $!-1
 $! 0
$. ncmp(a,b):
 $! $?(nsub(a,b))
$. $}(a):
 t=$((a)
 if t is $Q:
  $! a
 if t is $-:
  if a!=a or a in($-('$T'),$-('-$T')):
   err("Domain error")
  $! $Q($3.$m(a))
 $! a[1]//a[2]
$. nabs(a):
 if $?(a)<0:
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
 x=$Q($3.pow(n,1.0/k))if n<10**300 $+ 1<<(($`(bin(n))-2)//k+1)
 if x<1:
  x=1
 $= $R:
  y=((k-1)*x+n//(x**(k-1)))//k
  if y>=x:
   break
  x=y
 $= x**k>n:
  x-=1
 $=(x+1)**k<=n:
  x+=1
 $! x
$. isqrt(n):
 $! iroot(n,2)
SMALLP=$)
$. smallprimes():
 global SMALLP
 if SMALLP is $):
  N=1000
  s=bytearray(N)
  ps=[]
  $4 i in $n(2,N):
   if $2 s[i]:
    ps.$&(i)
    $4 j in $n(i*i,N,i):
     s[j]=1
  SMALLP=ps
 $! SMALLP
$. $%(e,h):
 $! $((e)is $/ $* e[0]==h
$. head(e):
 if $((e)is $/:
  $! e[0]
 $! $)
$. okey(e):
 $! repr(e)
$. has(e,x):
 if e==x:
  $! $R
 if $((e)is $/ $* e[0]!='Q':
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
$. symbols(e,$g=$)):
 if $g is $):
  $g=[]
 t=$((e)
 if t is $a:
  if e $2 in $o $* e $2 in $g:
   $g.$&(e)
 $K t is $/ $* e[0]!='Q' $* e[0]!='$a':
  $4 a in e[1:]:
   symbols(a,$g)
 $! $g
$. $1(e):
 t=$((e)
 if t is $a:
  $! e in $o
 if t is $/ $* e[0]!='Q':
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
 if t is $/ $* e[0]!='Q':
  $4 a in e[1:]:
   if $S(a):
    $! $R
 $! $6
$. $9(a):
 if $((a)is $/ $* a[0]=='*' $* $0(a[1]):
  if $`(a)==3:
   $! a[1],a[2]
  $! a[1],('*',)+a[2:]
 $! 1,a
$. cmul(c,r):
 if $((c)is $Q $* c==1:
  $! r
 if $((r)is $/ $* r[0]=='*':
  if $0(r[1]):
   c=$l(c,r[1])
   if $((c)is $Q $* c==1:
    $!('*',)+r[2:]if $`(r)>3 $+ r[2]
   $!('*',c)+r[2:]
  $!('*',c)+r[1:]
 $!('*',c,r)
$. add(*$>):
 $! $F($>)
$. $F($>):
 $c=0
 $P={}
 order=[]
 st=$f($>)
 infs=0
 $= st:
  a=st.pop()
  t=$((a)
  if t is $Q or t is $-:
   $c=nadd($c,a)
   $7
  if t is $/:
   h=a[0]
   if h=='Q':
    $c=nadd($c,a)
    $7
   if h=='+':
    st.extend(a[1:])
    $7
   if h=='*' $* $0(a[1]):
    c=a[1]
    r=a[2]if $`(a)==3 $+('*',)+a[2:]
   $+:
    c=1
    r=a
  $+:
   if a=='$8':
    $! '$8'
   c=1
   r=a
  if r=='$T':
   s=$?(c)
   if s==0:
    $7
   if infs $* infs!=s:
    $! '$8'
   infs=s
   $7
  if r in $P:
   $P[r]=nadd($P[r],c)
  $+:
   $P[r]=c
   order.$&(r)
 if infs:
  $! '$T' if infs>0 $+('*',-1,'$T')
 $g=[]
 $4 r in order:
  c=$P[r]
  if c==0:
   $7
  $g.$&(cmul(c,r))
 if $c!=0 or $2 $g:
  if $g $* $c==0:
   pass
  $+:
   $g.$&($c)
 if $`($g)==1:
  $! $g[0]
 $g.sort(key=okey)
 $!('+',)+$/($g)
$. isrrad(e):
 $! $((e)is $/ $* e[0]=='^' $* $((e[1])is $Q $* isq(e[2])
$. $A(*$>):
 $! $C($>)
''')
_x(r'''$. $C($>):
 $G=1
 bases={}
 order=[]
 st=$f($>)
 $= st:
  a=st.pop()
  t=$((a)
  if t is $Q or t is $-:
   $G=$l($G,a)
   $7
  if t is $/:
   h=a[0]
   if h=='Q':
    $G=$l($G,a)
    $7
   if h=='*':
    st.extend(a[1:])
    $7
   if h=='^':
    b=a[1]
    x=a[2]
   $+:
    b=a
    x=1
  $+:
   if a=='$8':
    $! '$8'
   b=a
   x=1
  if b in bases:
   bases[b]=add(bases[b],x)
  $+:
   bases[b]=x
   order.$&(b)
 if $G==0:
  if '$T' in bases:
   $! '$8'
  $4 b in order:
   if b=='$8' or has(b,'$8'):
    $! '$8'
  $! $G
 $X=[]
 rad={}
 $u=[]
 $. collect(p):
  c=1
  t=$((p)
  if t is $Q or t is $- or(t is $/ $* p[0]=='Q'):
   $! p
  if t is $/ $* p[0]=='*':
   items=p[1:]
  $+:
   items=(p,)
  $4 f in items:
   if $0(f):
    c=$l(c,f)
   $K isrrad(f):
    ex=f[2]
    if ex in rad:
     rad[ex]=rad[ex]*f[1]
     $u.$&($))
    $+:
     rad[ex]=f[1]
     $u.$&(ex)
   $+:
    $X.$&(f)
  $! c
 $4 b in order:
  p=pw(b,bases[b])
  if p=='$8':
   $! '$8'
  $G=$l($G,collect(p))
 if rad:
  multi=$`($u)!=$`(rad)
  if multi:
   items=[(ex,rad[ex])$4 ex in $u if ex is $2 $)]
   rad.clear()
   del $u[:]
   pend=[]
   $4 ex,b in items:
    pend.$&(pw_num(b,ex))
   $4 p in pend:
    $G=$l($G,collect(p))
  $4 ex in rad:
   $X.$&(('^',rad[ex],ex))
 if $G==0:
  $! 0
 if '$T' in $X:
  if $`($X)==1 or $R:
   $G=$?($G)if $(($G)is $2 $- $+(1.0 if $G>0 $+-1.0)
   if $(($G)is $-:
    $G=$Q($G)
 if $2 $X:
  $! $G
 if $`($X)>1:
  algs=[f $4 f in $X if $%(f,'+')$* isalg(f)]
  if algs $* all([isalg(f)$4 f in $X]):
   r=$G
   $4 f in $X:
    r=$W(r,f)
   $! r
 if $`($X)==1:
  f=$X[0]
  if $(($G)is $Q $* $G==1:
   $! f
  if $((f)is $/ $* f[0]=='+':
   $! $F([$A($G,t)$4 t in f[1:]])
  $!('*',$G,f)
 $X.sort(key=okey)
 if $(($G)is $Q $* $G==1:
  $!('*',)+$/($X)
 $!('*',$G)+$/($X)
$. ${(a):
 $! $A(-1,a)
$. sub(a,b):
 $! add(a,$A(-1,b))
$. div(a,b):
 $! $A(a,pw(b,-1))
$. inv(a):
 $! pw(a,-1)
$. $N(a):
 $! pw(a,$Y)
$. factor_int_small(n):
 fs=[]
 $4 p in smallprimes():
  if p*p>n:
   break
  if n%p==0:
   k=0
   $= n%p==0:
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
 a,m=radical(n**p,q)if p>1 $+ radical(n,q)
 if m==1:
  $! a
 ex=Q(1,q)
 k=2
 best=$)
 $=(1<<k)<=m:
  r=iroot(m,k)
  if r**k==m:
   best=(r,k)
  k+=1
 if best is $2 $):
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
 $! 4*$`(h)-(3 if v<2 $+ 2 if v<4 $+ 1 if v<8 $+ 0)
$. bigpow(b,x):
 n,d=nd(b)
 if d==1 $* abs(n)<=1:
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
   $! '$8'
  if bf!=bf or xf!=xf:
   $! '$8'
  if bf<0 $*(xf in($-('$T'),$-('-$T'))or xf!=$3.$m(xf)):
   if $d(x)$* nd(x)[1]%2==1:
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
    $! '$8'
   $! 0
  if bigpow(b,x):
   $!('^',b,x)
  $! nipow(b,x)
 p,q=nd(x)
 if b==0:
  $! 0 if p>0 $+ '$8'
 if $?(b)<0:
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
   c=$l(c,pt)
  $K pt[0]=='*':
   c=$l(c,pt[1])
   $X.$&(pt[2])
  $+:
   $X.$&(pt)
 if $`($X)==2:
  if $X[0][2]==$X[1][2]:
   $! $A(c,pw_num($X[0][1]*$X[1][1],$X[0][2]))
  $X.sort(key=okey)
 if $2 $X:
  $! c
 if c==1:
  if $`($X)==1:
   $! $X[0]
  $!('*',)+$/($X)
 $!('*',c)+$/($X)
$. $|(e):
 if $0(e):
  $! $?(e)>0
 if e=='pi' or e=='e':
  $! $R
 if isrrad(e):
  $! e[1]>0
 if $%(e,'^')$*(e[1]=='e' or e[1]=='pi')$* $B(e[2]):
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
  $! $0(e[1])$* $0(e[2])
 if h=='+' or h=='*':
  $4 a in e[1:]:
   if $2 isalg(a):
    $! $6
  $! $R
 $! $6
''')
_x(r'''$. pw(b,x):
 if x==0:
  if b=='$8' or b=='$T':
   $! '$8'
  $! 1
 if $((x)is $Q $* x==1:
  $! b
 if b=='$8' or x=='$8':
  $! '$8'
 bn=$0(b)
 xn=$0(x)
 if bn $* xn:
  $! pw_num(b,x)
 if b==1 $* $((b)is $Q:
  $! 1
 if b=='$T':
  if xn:
   $! '$T' if $?(x)>0 $+ 0
  if x=='$T':
   $! '$T'
 if xn $* b==0:
  $! 0 if $?(x)>0 $+ '$8'
 if b=='i' $* $((x)is $Q:
  r=x%4
  $!(1,'i',-1,('*',-1,'i'))[r]
 if x=='$T' $* bn:
  if nabs(b)==1:
   $! '$8' if b==1 $+ '$8'
  if ncmp(nabs(b),1)>0:
   $! '$T' if $?(b)>0 $+ '$8'
  $! 0
 if b=='e':
  if x=='$T':
   $! '$T'
  if $%(x,'*')$* $`(x)==3 $* x[1]==-1 $* x[2]=='$T':
   $! 0
  if $((x)is $-:
   $! $3.exp(x)
  if $%(x,'ln'):
   $! x[1]
  if $%(x,'*'):
   c,r=$9(x)
   if $%(r,'ln')$* $d(c):
    $! pw(r[1],c)
  if $%(x,'+'):
   $y=[]
   $H=[]
   $4 t in x[1:]:
    c,r=$9(t)
    if $%(r,'ln')$* $d(c):
     $y.$&(pw(r[1],c))
    $+:
     $H.$&(t)
   if $y:
    $! $C($y+[pw('e',$F($H))])
  if $%(x,'*')$* 'i' in x $* 'pi' in x:
   c,r=$9(x)
   if r==('*','i','pi')$* $d(c):
    $! add(cos_($A(c,'pi')),$A('i',sin_($A(c,'pi'))))
 if b!='e' $* $1(b)$* $1(x)$* $2 $d(x)$*(has(b,'i')or has(x,'i'))$* $2 $S(x):
  L=fn('ln',b)
  if $2 $%(L,'ln')$* $2($%(L,'+')$* any([$%(t,'ln')$4 t in L[1:]])):
   $! pw('e',$^($A(x,L)))
 if $((b)is $/:
  h=b[0]
  if h=='^':
   bb=b[1]
   ee=b[2]
   if $((x)is $Q:
    $! pw(bb,$A(ee,x))
   if $|(bb):
    $! pw(bb,$A(ee,x))
   if $d(ee)$* $d(x):
    r=$l(ee,x)
    if $((ee)is $Q:
     if ee%2==0:
      if $((r)is $Q $* r%2==0:
       $! pw(bb,r)
      $! pw(fn('abs',bb),r)
     $! pw(bb,r)
    if nd(ee)[0]%2==1 $* nd(ee)[1]%2==1:
     $! pw(bb,r)
    if nd(ee)[0]%2==1:
     $! pw(bb,r)
  $K h=='*':
   if $((x)is $Q:
    $! $C([pw(f,x)$4 f in b[1:]])
   $y=[]
   $H=[]
   $4 f in b[1:]:
    if $0(f):
     if $?(f)>0:
      $y.$&(pw(f,x))
     $K f!=-1:
      $y.$&(pw(nneg(f),x))
      $H.$&(-1)
     $+:
      $H.$&(f)
    $K $|(f)or $%(f,'abs'):
     $y.$&(pw(f,x))
    $+:
     $H.$&(f)
   if $y:
    $! $C($y+[pw($C($H),x)])
  $K h=='abs':
   if $((x)is $Q $* x%2==0:
    $! pw(b[1],x)
  $K h=='+':
   if x==$Y $* isalg(b)$* $2 has(b,'i'):
    dn=denest(b)
    if dn is $2 $):
     $! dn
   if isq(x)$* x[2]==2 $* $?(x)<0 $* isalg(b)$* $2 has(b,'i'):
    dn=denest(b)
    if dn is $2 $):
     $! pw(pw(dn,-1),-x[1])if x[1]!=-1 $+ pw(dn,-1)
   if $((x)is $Q $* x!=1 $* $2 isalg(b):
    c=sumcontent(b)
    if c!=1:
     $! $A(pw(c,x),pw($A(ninv(c),b),x))
    if leadneg(b):
     nb=$A(-1,b)
     if x%2==0:
      $! pw(nb,x)
     $! $A(-1,pw(nb,x))
   if $((x)is $Q $* isalg(b):
    if x>0 $* x<=64:
     $! $_(b,x)
    if x<0 $* x>=-64:
     r=$V(b)
     if r is $2 $):
      if x==-1:
       $! r
      $! $_(r,-x)
 $!('^',b,x)
$. tdeg(r):
 d=0
 fs=r[1:]if $%(r,'*')$+(r,)
 $4 f in fs:
  if $((f)is $a $* f $2 in $o:
   d+=1
  $K $%(f,'^')$* $((f[1])is $a $* f[1]$2 in $o $* $0(f[2]):
   d+=tofl(f[2])
 $! d
$. leadneg(b):
 best=$)
 bk=$)
 $4 t in b[1:]:
  if $0(t):
   $7
  c,r=$9(t)
  k=(-tdeg(r),okey(r))
  if bk is $) or k<bk:
   bk=k
   best=c
 if best is $):
  $! $6
 $! $?(best)<0 if $0(best)$+ $6
$. sumcontent(b):
 g=0
 L=1
 $4 t in b[1:]:
  c,r=$9(t)
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
 n=$)
 $4 t in b[1:]:
  if $d(t):
   a=nadd(a,t)
   $7
  cc,r=$9(t)
  if isrrad(r)$* r[2]==$Y $* $d(cc)$*(n is $) or n==r[1]):
   n=r[1]
   c=nadd(c,cc)
  $+:
   $! $)
 if n is $) or c==0:
  $! $)
 d2=nsub($l(a,a),$l($l(c,c),n))
 if $?(d2)<0:
  $! $)
 dn,dd=nd(d2)
 rn=isqrt(dn)
 rd=isqrt(dd)
 if rn*rn!=dn or rd*rd!=dd:
  $! $)
 d=Q(rn,rd)
 p=ndiv(nadd(a,d),2)
 m=ndiv(nsub(a,d),2)
 if $?(p)<0 or $?(m)<0:
  $! $)
 r=add(pw(p,$Y),$A($?(c),pw(m,$Y)))
 if $%(r,'+')$* $`(r)<=3:
  $! r
 $! $)
$. $W(a,b):
 ta=a[1:]if $%(a,'+')$+(a,)
 tb=b[1:]if $%(b,'+')$+(b,)
 $g=[]
 $4 u in ta:
  $4 v in tb:
   $g.$&($A(u,v))
 $! $F($g)
$. $_(b,n):
 r=1
 p=b
 $= n>0:
  if n&1:
   r=$W(r,p)
  n>>=1
  if n:
   p=$W(p,p)
 $! r
$. $V(b):
 re_,im_=reim(b)
 if im_!=0:
  d=add($A(re_,re_),$A(im_,im_))
  d=$^(d)
  if $%(d,'+'):
   r2=$V(d)
   if r2 is $):
    $! $)
  $+:
   r2=pw(d,-1)
  $! $W(sub(re_,$A('i',im_)),r2)
 $P=b[1:]if $%(b,'+')$+(b,)
 kern=$)
 kerns=[]
 $4 t in $P:
  c,r=$9(t)
  if r!=1 $* $2 $0(r):
   if isrrad(r)$* r[2]==$Y:
    if r $2 in kerns:
     kerns.$&(r)
   $+:
    $! $)
 if $2 kerns or $`(kerns)>3:
  $! $)
 kern=kerns[0]
 if $`(kerns)>1:
  A=$F([t $4 t in $P if $9(t)[1]!=kern])
  B=$F([$9(t)[0]$4 t in $P if $9(t)[1]==kern])
  den=$^(sub($A(A,A),$A(B,B,kern[1])))
  if den==0:
   $! $)
  if $%(den,'+'):
   r2=$V(den)
   if r2 is $):
    $! $)
  $+:
   r2=pw(den,-1)
  $! $W(sub(A,$A(B,kern)),r2)
 a0=0
 a1=0
 $4 t in $P:
  c,r=$9(t)
  if r==kern:
   a1=nadd(a1,c)
  $+:
   a0=add(a0,t)
 den=sub($A(a0,a0),$A($l(a1,a1),kern[1]))
 if den==0:
  $! $)
 $! $W(sub(a0,$A(a1,kern)),pw(den,-1))
''')
_x(r'''$. reim(e):
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
  if $2 has(b,'i')$* $2 has(x,'i'):
   if $0(x)$* $2 $d(x):
    $! e,0
   if $d(x)$* nd(x)[1]%2==0:
    if $1(b):
     v=cv(b)
     if v is $2 $) $* $((v)is $2 $, $* v<0:
      $! $p(e)
    $! e,0
   $! e,0
  if $((x)is $Q:
   br,bi=reim(b)
   if x>0:
    z=$_(add(br,$A('i',bi)),x)
    if has(z,'i')$* z!=e:
     $! reim(z)
   $K $1(b):
    r=$V(b)
    if r is $2 $):
     $! reim($_(r,-x))if x!=-1 $+ reim(r)
  $! $p(e)
 if h in('$f','mat','$a'):
  $! e,0
 $4 a in e[1:]:
  if has(a,'i'):
   $! $p(e)
 $! e,0
$. cv(u):
 try:
  v=$x(u)
 $J($:,$L,$<,$I,$v):
  $! $)
 if v!=v:
  $! $)
 if $((v)is $,:
  if v.$h!=v.$h or v.$s!=v.$s:
   $! $)
  if abs(v.$h)==$-('$T')or abs(v.$s)==$-('$T'):
   $! $)
 $K abs(v)==$-('$T'):
  $! $)
 $! v
$. $p(e):
 if $1(e):
  v=cv(e)
  if v is $):
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
$. fn($;,*$>):
 if $`($>)==1 $* $(($>[0])is $f:
  $>=$/($>[0])
 $4 a in $>:
  if a=='$8':
   $! '$8'
 f=$5.get($;)
 if f is $2 $):
  r=f(*$>)
  if r is $2 $):
   $! r
 $!($;,)+$/($>)
$. $e(e):
 if $0(e):
  $! $?(e)<0
 if $%(e,'*'):
  $! $0(e[1])$* $?(e[1])<0
 if $%(e,'+'):
  $! leadneg(e)
 $! $6
$. $B(e):
 if $0(e):
  $! $R
 if $((e)is $a:
  $! e!='i' $* e!='$8'
 $! $2 has(e,'i')
$. fval($;,x):
 $! $i(NUMF[$;](x))
$. $z($;,u):
 try:
  v=NUMF[$;]($x(u))
 $J($:,$L,$<,$I,$v):
  $! $)
 if $((v)is $,:
  if v.$h!=v.$h or v.$s!=v.$s:
   $! $)
 $K v!=v:
  $! $)
 $! $i(v)
$. pi_coef(u):
 if u=='pi':
  $! 1
 if u==0:
  $! 0
 if $%(u,'*')$* $`(u)==3 $* u[2]=='pi' $* $d(u[1]):
  $! u[1]
 $! $)
$. split_pi(u):
 if $%(u,'+'):
  $4 t in u[1:]:
   c=pi_coef(t)
   if c is $2 $) $* c!=0:
    $H=$F([s $4 s in u[1:]if s is $2 t])
    $! c,$H
 $! $)
TRIGT=$)
$. $~():
 global TRIGT
 if TRIGT is $):
  s2=$N(2)
  s3=$N(3)
  s5=$N(5)
  s6=$N(6)
  q=Q
  T={}
  T[0]=0
  T[q(1,12)]=$A(q(1,4),sub(s6,s2))
  T[q(1,10)]=$A(q(1,4),sub(s5,1))
  T[q(1,8)]=$A($Y,$N(sub(2,s2)))
  T[q(1,6)]=$Y
  T[q(1,5)]=$A(q(1,4),$N(sub(10,$A(2,s5))))
  T[q(1,4)]=$A($Y,s2)
  T[q(3,10)]=$A(q(1,4),add(s5,1))
  T[q(1,3)]=$A($Y,s3)
  T[q(3,8)]=$A($Y,$N(add(2,s2)))
  T[q(2,5)]=$A(q(1,4),$N(add(10,$A(2,s5))))
  T[q(5,12)]=$A(q(1,4),add(s6,s2))
  T[$Y]=1
  TT={}
  TT[0]=0
  TT[q(1,12)]=sub(2,s3)
  TT[q(1,8)]=sub(s2,1)
  TT[q(1,6)]=$A(q(1,3),s3)
  TT[q(1,4)]=1
  TT[q(1,3)]=s3
  TT[q(3,8)]=add(s2,1)
  TT[q(5,12)]=add(2,s3)
  TT[q(1,5)]=$N(sub(5,$A(2,s5)))
  TT[q(2,5)]=$N(add(5,$A(2,s5)))
  TT[q(1,10)]=$A(q(1,5),$N(sub(25,$A(10,s5))))
  TT[q(3,10)]=$A(q(1,5),$N(add(25,$A(10,s5))))
  TRIGT=(T,TT)
 $! TRIGT
$. sin_pi(c):
 c=nsub(c,$l(2,$}($l(c,$Y))))
 sg=1
 if ncmp(c,1)>=0:
  c=nsub(c,1)
  sg=-1
 if ncmp(c,$Y)>0:
  c=nsub(1,c)
 T=$~()[0]
 if c in T:
  $! $A(sg,T[c])
 if sg<0:
  $! ${(('sin',$A(c,'pi')))
 $!('sin',$A(c,'pi'))
$. tan_pi(c):
 c=nsub(c,$}(c))
 sg=1
 if ncmp(c,$Y)>0:
  c=nsub(1,c)
  sg=-1
 if c==$Y:
  $! '$8'
 TT=$~()[1]
 if c in TT:
  $! $A(sg,TT[c])
 $! $A(sg,('tan',$A(c,'pi')))
$. sin_(u):
 if $0(u):
  if u==0:
   $! 0
  if $((u)is $-:
   $! $3.sin(u)
  $! $)
 if u=='$T' or u==('*',-1,'$T'):
  $! '$8'
 c=pi_coef(u)
 if c is $2 $):
  $! sin_pi(c)
 if $S(u)$* $1(u):
  $! $z('sin',u)
 if $e(u):
  $! ${(fn('sin',${(u)))
 sp=split_pi(u)
 if sp is $2 $):
  c,$H=sp
  c=nsub(c,$l(2,$}($l(c,$Y))))
  if c==0:
   $! fn('sin',$H)
  if c==1:
   $! ${(fn('sin',$H))
  if c==$Y:
   $! fn('cos',$H)
  if c==Q(3,2):
   $! ${(fn('cos',$H))
  if ncmp(c,1)>0:
   $!('sin',add($H,$A(nsub(c,2),'pi')))
  $!('sin',add($H,$A(c,'pi')))
 if $%(u,'$]'):
  $! u[1]
 if $%(u,'$k'):
  $! $N(sub(1,pw(u[1],2)))
 if $%(u,'$b'):
  $! div(u[1],$N(add(1,pw(u[1],2))))
 $! $)
''')
_x(r'''$. cos_(u):
 if $0(u):
  if u==0:
   $! 1
  if $((u)is $-:
   $! $3.cos(u)
  $! $)
 if u=='$T' or u==('*',-1,'$T'):
  $! '$8'
 c=pi_coef(u)
 if c is $2 $):
  $! sin_pi(nadd(c,$Y))
 if $S(u)$* $1(u):
  $! $z('cos',u)
 if $e(u):
  $! fn('cos',${(u))
 sp=split_pi(u)
 if sp is $2 $):
  c,$H=sp
  c=nsub(c,$l(2,$}($l(c,$Y))))
  if c==0:
   $! fn('cos',$H)
  if c==1:
   $! ${(fn('cos',$H))
  if c==$Y:
   $! ${(fn('sin',$H))
  if c==Q(3,2):
   $! fn('sin',$H)
  if ncmp(c,1)>0:
   $!('cos',add($H,$A(nsub(c,2),'pi')))
  $!('cos',add($H,$A(c,'pi')))
 if $%(u,'$k'):
  $! u[1]
 if $%(u,'$]'):
  $! $N(sub(1,pw(u[1],2)))
 if $%(u,'$b'):
  $! pw(add(1,pw(u[1],2)),Q(-1,2))
 $! $)
$. tan_(u):
 if $0(u):
  if u==0:
   $! 0
  if $((u)is $-:
   $! $3.tan(u)
  $! $)
 c=pi_coef(u)
 if c is $2 $):
  $! tan_pi(c)
 if $S(u)$* $1(u):
  $! $z('tan',u)
 if $e(u):
  $! ${(fn('tan',${(u)))
 sp=split_pi(u)
 if sp is $2 $):
  c,$H=sp
  c=nsub(c,$}(c))
  if c==0:
   $! fn('tan',$H)
  if c==$Y:
   $! ${(pw(fn('tan',$H),-1))
  $!('tan',add($H,$A(c,'pi')))
 if $%(u,'$b'):
  $! u[1]
 $! $)
INVT=$)
$. inv_table():
 global INVT
 if INVT is $):
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
   $! fval('$]',u)
 if $e(u):
  $! ${(fn('$]',${(u)))
 S=inv_table()[0]
 if u in S:
  $! $A(S[u],'pi')
 if $1(u)$* $S(u):
  $! $z('$]',u)
 $! $)
$. acos_(u):
 if $0(u)$* $((u)is $-:
  if-1.0<=u<=1.0:
   $! $3.acos(u)
  $! fval('$k',u)
 a=asin_(u)
 if a is $2 $) $* $2 $%(a,'$]')$* freeof(a,'$]'):
  $! sub($A($Y,'pi'),a)
 if $e(u):
  $! sub('pi',fn('$k',${(u)))
 $! $)
$. atan_(u):
 if $0(u):
  if $((u)is $-:
   $! $3.atan(u)
 if u=='$T':
  $! $A($Y,'pi')
 if u==('*',-1,'$T'):
  $! $A(Q(-1,2),'pi')
 if $e(u):
  $! ${(fn('$b',${(u)))
 Tn=inv_table()[1]
 if u in Tn:
  $! $A(Tn[u],'pi')
 if $1(u)$* $S(u):
  $! $z('$b',u)
 $! $)
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
  if $?(u)<0:
   $! add(fn('ln',nneg(u)),$A('i','pi'))
  n,d=nd(u)
  if n==1:
   $! ${(fn('ln',d))
  $! $)
 if u=='e':
  $! 1
 if u=='$T':
  $! '$T'
 if u=='i':
  $! $A($Y,'i','pi')
 if $%(u,'^'):
  if u[1]=='e' $* $B(u[2]):
   $! u[2]
  if $|(u[1])$* $B(u[2])$* $0(u[2]):
   $! $A(u[2],fn('ln',u[1]))
 if $1(u)$* $S(u):
  $! $z('ln',u)
 $! $)
$. log_(u,b=10):
 if $0(u)$* $0(b):
  if $((u)is $- or $((b)is $-:
   a1=$z('ln',u)
   a2=$z('ln',b)
   if a1 is $2 $) $* a2 is $2 $) $* a2!=0:
    $! div(a1,a2)
   $! $)
  if u==1:
   $! 0
  if $d(u)$* $d(b)$* $?(u)>0 $* $?(b)>0 $* b!=1:
   k=exact_log(u,b)
   if k is $2 $):
    $! k
 if u==b:
  $! 1
 if $%(u,'^')$* u[1]==b $* $B(u[2]):
  $! u[2]
 if $1(u)$* $1(b)$*($S(u)or $S(b)):
  a1=$z('ln',u)
  a2=$z('ln',b)
  if a1 is $2 $) $* a2 is $2 $) $* a2!=0:
   $! div(a1,a2)
  $! $)
 $! $)
$. exact_log(u,b):
 un,ud=nd(u)
 bn,bd=nd(b)
 lu=$3.log(tofl(u))
 lb=$3.log(tofl(b))
 if lb==0:
  $! $)
 k=lu/lb
 $4 den in $n(1,13):
  $c=$Q(round(k*den))
  if abs(k*den-$c)<1e-9:
   kk=Q($c,den)
   if pw_num(b,kk)==u:
    $! kk
   $! $)
 $! $)
$. abs_(u):
 if $0(u):
  $! nabs(u)
 if u=='$T' or u==('*',-1,'$T'):
  $! '$T'
 if $%(u,'abs'):
  $! u
 if $%(u,'^')$* $((u[2])is $Q $* u[2]%2==0 $* $B(u[1]):
  $! u
 if has(u,'i'):
  r,i=reim(u)
  if i!=0 $* $2 has(r,'i')$* $2 has(i,'i'):
   $! $N(add(pw(r,2),pw(i,2)))
 if $1(u):
  v=cv(u)
  if v is $2 $) $* $((v)is $2 $,:
   if v>=0:
    $! u
   $! ${(u)
 if $%(u,'*'):
  $y=[]
  $H=[]
  $4 f in u[1:]:
   if $0(f):
    $y.$&(nabs(f))
   $K $1(f):
    $y.$&(abs_(f)or('abs',f))
   $K $%(f,'^')$* $((f[2])is $Q $* f[2]%2==0:
    $y.$&(f)
   $K $%(f,'^')$* f[1]=='e':
    $y.$&(f)
   $+:
    $H.$&(f)
  if $y:
   $! $C($y+[fn('abs',$C($H))])
 if $e(u):
  $! fn('abs',${(u))
 if $%(u,'^')$* u[1]=='e' $* $B(u[2]):
  $! u
 $! $)
$. sign_(u):
 if $0(u):
  $! $?(u)if $((u)is $2 $- $+ $-($?(u))
 if u=='$T':
  $! 1
 if $1(u):
  v=cv(u)
  if v is $2 $) $* $((v)is $2 $,:
   $! 1 if v>0 $+(-1 if v<0 $+ 0)
 if $%(u,'*')$* $0(u[1]):
  $! $A($?(u[1]),fn('sign',cmul(nabs(u[1]),$9(u)[1])))
 if $%(u,'^')$* $((u[2])is $Q $* u[2]%2==0:
  $! $)
 $! $)
$. finite(v):
 $! v==v $* v!=$-('$T')$* v!=$-('-$T')
$. floor_(u):
 if $0(u):
  if $((u)is $-:
   $! $-($3.$m(u))if finite(u)$+ $)
  $! $}(u)
 if $1(u)$* $2 has(u,'i'):
  v=cv(u)
  if v is $2 $) $* $((v)is $2 $,:
   $! $Q($3.$m(v))
 $! $)
$. ceil_(u):
 f=floor_(${(u))
 if f is $2 $):
  $! ${(f)
 $! $)
$. sinh_(u):
 if u==0:
  $! 0
 if $e(u):
  $! ${(fn('sinh',${(u)))
 if $%(u,'$w'):
  $! u[1]
 $! $)
''')
_x(r'''$. cosh_(u):
 if u==0:
  $! 1
 if $e(u):
  $! fn('cosh',${(u))
 if $%(u,'arccosh'):
  $! u[1]
 $! $)
$. tanh_(u):
 if u==0:
  $! 0
 if $e(u):
  $! ${(fn('tanh',${(u)))
 $! $)
$. odd0($;):
 $. g(u):
  if u==0:
   $! 0
  if $e(u):
   $! ${(fn($;,${(u)))
  $! $)
 $! g
$. fact_(u):
 if $((u)is $Q:
  if u<0:
   $! '$8'
  if u>1000:
   $! $)
  r=1
  $4 k in $n(2,u+1):
   r*=k
  $! r
 if isq(u)$* u[2]==2 $* u[1]>0:
  n=u[1]
  r=$A($N('pi'),Q(1,1))
  k=Q(1,2)
  $= ncmp(k,u)<=0:
   r=$A(r,k)
   k=nadd(k,1)
  $! r
 if $((u)is $-:
  if u<0 $* u==$3.$m(u):
   $! '$8'
  try:
   $! gamma(u+1.0)
  $J($I,$<,$L):
   $! '$T' if u>0 $+ '$8'
 $! $)
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
 $4 k in $n(1,9):
  a+=c[k]/(x+k)
 h=t**((x+0.5)/2)
 $! $3.$N(2*$3.pi)*h*$3.exp(-t)*h*a
$. real_(u):
 if $1(u)or has(u,'i'):
  r,i=reim(u)
  if $2 $%(r,'$h'):
   $! r
 if $B(u):
  $! u
 $! $)
$. imag_(u):
 if $B(u):
  $! 0
 r,i=reim(u)
 if $2 $%(i,'$s'):
  $! i
 $! $)
$. conj_(u):
 if $B(u):
  $! u
 r,i=reim(u)
 if $2 $%(r,'$h'):
  $! sub(r,$A('i',i))
 $! $)
$. angle_(u):
 r,i=reim(u)
 if $%(r,'$h')or $%(i,'$s'):
  $! $)
 if i==0:
  if $1(r):
   v=cv(r)
   if v is $2 $) $* $((v)is $2 $,:
    if v>=0:
     $! 0
    $! 'pi'
  $! $)
 if r==0:
  if $1(i):
   v=cv(i)
   if v is $2 $) $* $((v)is $2 $,:
    $! $A(Q(1 if v>0 $+-1,2),'pi')
  $! $)
 if $1(r)$* $1(i):
  vr=cv(r)
  vi=cv(i)
  if vr is $) or vi is $) or $((vr)is $, or $((vi)is $,:
   $! $)
  a=fn('$b',div(i,r))
  if vr<0:
   if vi>=0:
    a=add(a,'pi')
   $+:
    a=sub(a,'pi')
  $! a
 $! $)
$5['sin']=sin_
$5['cos']=cos_
$5['tan']=tan_
$5['$]']=asin_
$5['$k']=acos_
$5['$b']=atan_
$5['ln']=ln_
$5['log']=log_
$5['abs']=abs_
$5['sign']=sign_
$5['$m']=floor_
$5['ceiling']=ceil_
$5['sinh']=sinh_
$5['cosh']=cosh_
$5['tanh']=tanh_
$5['$w']=odd0('$w')
$5['arctanh']=odd0('arctanh')
$5['arccosh']=$@ u:0 if u==1 $+ $)
$5['fact']=fact_
$5['$h']=real_
$5['$s']=imag_
$5['conj']=conj_
$5['angle']=angle_
$5['exp']=$@ u:pw('e',u)
$5['$N']=$@ u:pw(u,$Y)
$5['sec']=$@ u:pw(fn('cos',u),-1)
$5['csc']=$@ u:pw(fn('sin',u),-1)
$5['cot']=$@ u:pw(fn('tan',u),-1)
$5['sech']=$@ u:pw(fn('cosh',u),-1)
$5['csch']=$@ u:pw(fn('sinh',u),-1)
$5['coth']=$@ u:pw(fn('tanh',u),-1)
$5['arcsec']=$@ u:fn('$k',pw(u,-1))
$5['arccsc']=$@ u:fn('$]',pw(u,-1))
$5['arccot']=$@ u:sub($A($Y,'pi'),fn('$b',u))
$5['arcsech']=$@ u:fn('arccosh',pw(u,-1))
$5['arccsch']=$@ u:fn('$w',pw(u,-1))
$5['arccoth']=$@ u:fn('arctanh',pw(u,-1))
$. root_(u,n=2):
 $! pw(u,pw(n,-1))
$5['root']=root_
import $M
$. _c(f):
 $. g(x):
  try:
   if $((x)is $,:
    $! f[1](x)
   $! f[0](x)
  $J($L,$v):
   $! f[1]($,(x))
 $! g
$. _ln(x):
 if $((x)is $2 $, $* x>0:
  $! $3.log(x)
 if x==0:
  $! $-('-$T')
 $! $M.log($,(x))
$. _asinr(x):
 if-1<=x<=1:
  $! $3.asin(x)
 $[ $L
$. _acosr(x):
 if-1<=x<=1:
  $! $3.acos(x)
 $[ $L
$. _casin(z):
 $!-1j*$M.log(1j*z+$M.$N(1-z*z))
$. _cacos(z):
 $! $3.pi/2-_casin(z)
$. _catan(z):
 $! 0.5j*$M.log((1-1j*z)/(1+1j*z))
$. _sinh(x):
 $!($M.exp(x)-$M.exp(-x))/2 if $((x)is $, $+($3.exp(x)-$3.exp(-x))/2
$. _cosh(x):
 $!($M.exp(x)+$M.exp(-x))/2 if $((x)is $, $+($3.exp(x)+$3.exp(-x))/2
$. _tanh(x):
 if $((x)is $2 $,:
  if x>20:
   $! 1.0
  if x<-20:
   $!-1.0
  a=$3.exp(2*x)
  $!(a-1)/(a+1)
 a=$M.exp(2*x)
 $!(a-1)/(a+1)
$. _asinh(x):
 if $((x)is $2 $,:
  $! $3.log(x+$3.$N(x*x+1))if x>=0 $+-$3.log(-x+$3.$N(x*x+1))
 $! $M.log(x+$M.$N(x*x+1))
$. _acosh(x):
 if $((x)is $2 $, $* x>=1:
  $! $3.log(x+$3.$N(x*x-1))
 x=$,(x)
 $! $M.log(x+$M.$N(x+1)*$M.$N(x-1))
$. _atanh(x):
 if $((x)is $2 $, $*-1<x<1:
  $! 0.5*$3.log((1+x)/(1-x))
 x=$,(x)
 $! 0.5*$M.log((1+x)/(1-x))
$. _sign(x):
 if $((x)is $,:
  $! x/abs(x)if x!=0 $+ 0.0
 $! 1.0 if x>0 $+(-1.0 if x<0 $+ 0.0)
$. _floor(x):
 if $((x)is $,:
  $! $,($3.$m(x.$h),$3.$m(x.$s))
 $! $-($3.$m(x))
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
  $! $M.phase(x)
 $! 0.0 if x>=0 $+ $3.pi
$. _fact(x):
 if $((x)is $,:
  $[ $L
 $! gamma(x+1.0)
''')
_x(r'''NUMF={
 'sin':_c(($3.sin,$M.sin)),'cos':_c(($3.cos,$M.cos)),
 'tan':_c(($3.tan,$@ z:$M.sin(z)/$M.cos(z))),
 '$]':_c((_asinr,_casin)),'$k':_c((_acosr,_cacos)),
 '$b':_c(($3.atan,_catan)),
 'ln':_ln,'exp':_c(($3.exp,$M.exp)),
 '$N':_c(($@ x:$3.$N(x)if x>=0 $+ $M.$N(x),$M.$N)),
 'abs':abs,'sign':_sign,'$m':_floor,'ceiling':_ceil,
 'sinh':_sinh,'cosh':_cosh,'tanh':_tanh,
 '$w':_asinh,'arccosh':_acosh,'arctanh':_atanh,
 '$h':_real,'$s':_imag,'conj':_conj,'angle':_angle,
 'fact':_fact,
 }
$. nfun_call($;,$Z):
 if $;=='log':
  b=$Z[1]if $`($Z)>1 $+ 10.0
  $! _ln($Z[0])/_ln(b)
 if $;=='root':
  n=$Z[1]if $`($Z)>1 $+ 2.0
  $! npow($Z[0],1.0/n)
 if $;=='round':
  d=$Q($Z[1])if $`($Z)>1 $+ 0
  $! round($Z[0],d)
 if $;=='when':
  $! $Z[1]if $Z[0]$+ $Z[2]
 if $;=='max':
  $! max($Z)
 if $;=='min':
  $! min($Z)
 if $;=='mod':
  $! $Z[0]-$Z[1]*$3.$m($Z[0]/$Z[1])if $Z[1]!=0 $+ $Z[0]
 f=NUMF.get($;)
 if f is $):
  if $; in('sec','csc','cot','sech','csch','coth'):
   base={'sec':'cos','csc':'sin','cot':'tan','sech':'cosh','csch':'sinh','coth':'tanh'}[$;]
   $! 1.0/NUMF[base]($Z[0])
  if $; in('arcsec','arccsc','arccot','arcsech','arccsch','arccoth'):
   base={'arcsec':'$k','arccsc':'$]','arccot':'$b','arcsech':'arccosh','arccsch':'$w','arccoth':'arctanh'}[$;]
   $! NUMF[base](1.0/$Z[0])
  if $; in('ipart','$Q'):
   $! $-($Q($Z[0]))
  if $;=='fpart':
   $! $Z[0]-$Q($Z[0])
  err("Cannot evaluate "+$;)
 $! f($Z[0])
$. npow(a,b):
 if $((a)is $2 $, $* $((b)is $2 $,:
  if a<0 $*(b!=b or b in($-('$T'),$-('-$T'))or b!=$3.$m(b)):
   $! $,(a)**b
  if a==0 $* b<0:
   $[ $<
  try:
   $! a**b
  $J $I:
   $! $-('$T')
 if a==0:
  $! 0.0
 $! $,(a)**b
NCONST={'pi':$3.pi,'e':$3.e,'i':1j,'$T':$-('$T')}
$. $x(e,env=$)):
 t=$((e)
 if t is $Q:
  try:
   $! $-(e)
  $J $I:
   $! '$T' if e>0 $+('*',-1,'$T')
 if t is $-:
  $! e
 if t is $a:
  if env is $2 $) $* e in env:
   $! env[e]
  v=NCONST.get(e)
  if v is $):
   err("Not numeric: "+e)
  $! v
 h=e[0]
 if h=='Q':
  $! e[1]/e[2]
 if h=='+':
  s=0.0
  $4 a in e[1:]:
   s=s+$x(a,env)
  $! s
 if h=='*':
  s=1.0
  $4 a in e[1:]:
   s=s*$x(a,env)
  $! s
 if h=='^':
  b=e[1]
  x=e[2]
  if isq(x)$* x[2]%2==1:
   bv=$x(b,env)
   if $((bv)is $2 $, $* bv<0:
    r=(-bv)**(x[1]/x[2])
    $!-r if x[1]%2 $+ r
   $! npow(bv,x[1]/x[2])
  if $((x)is $Q:
   bv=$x(b,env)
   if bv==0 $* x<0:
    $[ $<
   $! bv**x
  $! npow($x(b,env),$x(x,env))
 if h in('$f','mat','$a','Q'):
  err("Not numeric")
 if h=='when':
  c=nbool(e[1],env)
  $! $x(e[2]if c $+ e[3],env)if $`(e)>3 or c $+ $x(e[2],env)
 $Z=[$x(a,env)$4 a in e[1:]]
 $! nfun_call(h,$Z)
$. nbool(c,env):
 h=head(c)
 if h in('<','>','<=','>=','=','/='):
  a=$x(c[1],env)
  b=$x(c[2],env)
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
 if h=='$*':
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
$. nreal(e,env=$)):
 v=$x(e,env)
 if $((v)is $,:
  if abs(v.$s)>1e-9*(1+abs(v.$h)):
   $[ $L
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
 $>=[simp(a)$4 a in e[1:]]
 if h=='+':
  $! $F($>)
 if h=='*':
  $! $C($>)
 if h=='^':
  $! pw($>[0],$>[1])
 if h in('$f','mat','=','<','>','<=','>=','/=','$*','or','$2'):
  $!(h,)+$/($>)
 $! fn(h,$>)
$. subs(e,old,new):
 if e==old:
  $! new
 t=$((e)
 if t is $2 $/ or e[0]=='Q' or e[0]=='$a':
  $! e
 ch=$6
 $>=[]
 $4 a in e[1:]:
  b=subs(a,old,new)
  if b is $2 a:
   ch=$R
  $>.$&(b)
 if $2 ch:
  $! e
 $! simp((e[0],)+$/($>))
$. subsd(e,d):
 t=$((e)
 if t is $a:
  if e in d:
   $! d[e]
  $! e
 if t is $2 $/ or e[0]=='Q' or e[0]=='$a':
  $! e
 ch=$6
 $>=[]
 $4 a in e[1:]:
  b=subsd(a,d)
  if b is $2 a:
   ch=$R
  $>.$&(b)
 if $2 ch:
  $! e
 $! simp((e[0],)+$/($>))
$. mapexpr(f,e):
 if $%(e,'$f'):
  $!('$f',)+$/(mapexpr(f,a)$4 a in e[1:])
 if $%(e,'mat'):
  $!('mat',)+$/(mapexpr(f,a)$4 a in e[1:])
 $! f(e)
$. $^(e):
 t=$((e)
 if t is $2 $/:
  $! e
 h=e[0]
 if h=='Q' or h=='$a':
  $! e
 if h=='+':
  $! $F([$^(a)$4 a in e[1:]])
 if h=='*':
  r=1
  $4 f in e[1:]:
   r=$W(r,$^(f))
  $! r
 if h=='^':
  b=$^(e[1])
  x=$^(e[2])
  if $%(b,'+')$* $((x)is $Q:
   if x>0:
    $! $_(b,x)
   if x<0:
    $! pw($_(b,-x),-1)
  if $%(b,'*')$* $((x)is $Q:
   $! $^($C([pw(f,x)$4 f in b[1:]]))
  if b=='e' $* $%(x,'+'):
   $! $C([pw('e',a)$4 a in x[1:]])
  if $%(x,'+')$* $0(b):
   $! $C([pw(b,a)$4 a in x[1:]])
  $! pw(b,x)
 if h in('$f','mat','=','<','>','<=','>=','/=','$*','or','$2'):
  $!(h,)+$/($^(a)$4 a in e[1:])
 $! fn(h,[$^(a)$4 a in e[1:]])
''')
_x(r'''$. evalf(e):
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
 if $1(e)$* h $2 in('$f','mat','=','<','>','<=','>=','/=','$*','or','$2'):
  try:
   v=$x(e)
   if $((v)is $,:
    $! $i(v)
   if v!=v:
    $! '$8'
   if v==$-('$T'):
    $! '$T'
   if v==$-('-$T'):
    $!('*',-1,'$T')
   $! v
  $J($<,$L,$I,$v):
   pass
  $J $::
   pass
 $>=[evalf(a)$4 a in e[1:]]
 if h=='^' $* $((e[2])is $Q:
  $>[1]=e[2]
 $! simp((h,)+$/($>))
$. exactify(e,tol=$)):
 t=$((e)
 if t is $-:
  $! float2rat(e,tol)
 if t is $/ $* e[0]!='Q' $* e[0]!='$a':
  $! simp((e[0],)+$/(exactify(a,tol)$4 a in e[1:]))
 $! e
$. float2rat(x,tol=$)):
 if x!=x:
  $! '$8'
 if x==$-('$T'):
  $! '$T'
 if x==$-('-$T'):
  $!('*',-1,'$T')
 if x==$3.$m(x)$* abs(x)<1e18:
  $! $Q(x)
 if tol is $):
  tol=5e-14*max(1.0,abs(x))
 h0,h1=0,1
 k0,k1=1,0
 y=x
 $4 _ in $n(60):
  a=$3.$m(y)
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
   if k is $):
    $! $)
   if k>d:
    d=k
  $! d
 if h=='*':
  d=0
  $4 a in e[1:]:
   k=degree(a,x)
   if k is $):
    $! $)
   d+=k
  $! d
 if h=='^' $* $((e[2])is $Q $* e[2]>0:
  k=degree(e[1],x)
  if k is $):
   $! $)
  $! k*e[2]
 $! $)
$. coeffs(e,x):
 e=$^(e)
 if freeof(e,x):
  $![e]
 $P=e[1:]if $%(e,'+')$+(e,)
 cs={}
 mx=0
 $4 t in $P:
  if $%(t,'*'):
   k=0
   $H=[]
   $4 f in t[1:]:
    if f==x:
     k+=1
    $K $%(f,'^')$* f[1]==x $* $((f[2])is $Q $* f[2]>0:
     k+=f[2]
    $K freeof(f,x):
     $H.$&(f)
    $+:
     $! $)
   c=$C($H)
  $K t==x:
   k=1
   c=1
  $K $%(t,'^')$* t[1]==x $* $((t[2])is $Q $* t[2]>0:
   k=t[2]
   c=1
  $K freeof(t,x):
   k=0
   c=t
  $+:
   $! $)
  cs[k]=add(cs.get(k,0),c)
  if k>mx:
   mx=k
 $![cs.get(k,0)$4 k in $n(mx+1)]
$. fromcoeffs(cs,x):
 $! $F([$A(cs[k],pw(x,k))$4 k in $n($`(cs))])
$. numer_denom(e):
 if $%(e,'*'):
  nu=[]
  de=[]
  $4 f in e[1:]:
   if isq(f):
    nu.$&(f[1])
    de.$&(f[2])
   $K $%(f,'^')$* $0(f[2])$* $?(f[2])<0:
    de.$&(pw(f[1],nneg(f[2])))
   $+:
    nu.$&(f)
  $! $C(nu),$C(de)
 if isq(e):
  $! e[1],e[2]
 if $%(e,'^')$* $0(e[2])$* $?(e[2])<0:
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
$j=6
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
  $! '$8'
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
 $! s,($j if x[1]>0 $+ P_NEG)
$. psym(e):
 if OPT['uni']$* e in USYM:
  $! USYM[e]
 $! e
$. paren(s,p,need):
 if p<need:
  $! '('+s+')'
 $! s
$. pr(e,$O):
 t=$((e)
 if t is $Q or t is $-:
  $! fnum(e)
 if t is $a:
  $! psym(e),$E
 h=e[0]
 if h=='Q':
  $! fnum(e)
 if h=='+':
  $! pr_sum(e,$O)
 if h=='*':
  $! pr_prod(e,$O)
 if h=='^':
  $! pr_pow(e,$O)
 if h=='hold':
  $! pr(e[1],$R)
 $O=$6
 if h=='$f':
  $! '{'+','.join([pr(a,$O)[0]$4 a in e[1:]])+'}',$E
 if h=='mat' $* $`(e)==2:
  $! '['+','.join([pr(a,$O)[0]$4 a in e[1][1:]])+']',$E
 if h=='mat':
  rows=[]
  $4 r in e[1:]:
   rows.$&('['+','.join([pr(a,$O)[0]$4 a in r[1:]])+']')
  $! '['+''.join(rows)+']',$E
 if h=='$a':
  $! '"'+e[1]+'"',$E
 if h in REL:
  op=REL[h]if OPT['uni']$+ h
  a=pr(e[1],$O)
  b=pr(e[2],$O)
  $! paren(a[0],a[1],P_SUM)+op+paren(b[0],b[1],P_SUM),P_REL
 if h=='$*' $* $`(e)==3 $* head(e[1])in('<','<=')$* head(e[2])in('<','<=')$* e[1][2]==e[2][1]:
  op1=REL[e[1][0]]if OPT['uni']$+ e[1][0]
  op2=REL[e[2][0]]if OPT['uni']$+ e[2][0]
  $! pr(e[1][1],$6)[0]+op1+pr(e[1][2],$6)[0]+op2+pr(e[2][2],$6)[0],P_REL
 if h=='$*' or h=='or':
  p=P_AND if h=='$*' $+ P_OR
  ss=[]
  $4 a in e[1:]:
   s,q=pr(a,$O)
   ss.$&(paren(s,q,p+1))
  $!(' '+h+' ').join(ss),p
 if h=='$2':
  s,q=pr(e[1],$O)
  $! '$2 '+paren(s,q,P_NOT+1),P_NOT
 if h=='abs':
  $! '|'+pr(e[1],$O)[0]+'|',$E
 if h=='fact':
  s,q=pr(e[1],$O)
  $! paren(s,q,$E)+'!',P_POST
 if h=='log':
  if $`(e)==2 or e[2]==10:
   $! 'log10('+pr(e[1],$O)[0]+')',$E
  $! 'log('+pr(e[1],$O)[0]+','+pr(e[2],$O)[0]+')',$E
 if h=='call':
  $! e[1]+'('+','.join([pr(a,$O)[0]$4 a in e[2:]])+')',$E
 if h=='prime':
  $! e[1]+"'"*e[2],$E
 if h=='integral':
  nm='\u222b' if OPT['uni']$+ 'integral'
  $! nm+'('+','.join([pr(a,$O)[0]$4 a in e[1:]])+')',$E
 if h=='sumseq':
  nm='\u03a3' if OPT['uni']$+ 'sumseq'
  $! nm+'('+','.join([pr(a,$O)[0]$4 a in e[1:]])+')',$E
 if h=='prodseq':
  nm='\u03a0' if OPT['uni']$+ 'prodseq'
  $! nm+'('+','.join([pr(a,$O)[0]$4 a in e[1:]])+')',$E
 if h=='$N' or h=='root':
  pass
 h=TINAME.get(h,h)
 $! h+'('+','.join([pr(a,$O)[0]$4 a in e[1:]])+')',$E
TINAME={'ncr':'nCr','npr':'nPr'}
MAINV='xyzt'
$. varprio(v):
 i=MAINV.find(v)if $`(v)==1 $+-1
 if i<0:
  $!(100,v)
 $!(i,v)
$. facprio(v):
 i=MAINV.find(v)if $`(v)==1 $+-1
 if i<0:
  $!(0,v)
 $!(1,$a(i))
$. termdegs(t,d):
 c,r=$9(t)
 fs=r[1:]if $%(r,'*')$+(r,)
 $4 f in fs:
  if $((f)is $a $* f $2 in $o:
   d[f]=d.get(f,0)+1
  $K $%(f,'^')$* $((f[1])is $a $* f[1]$2 in $o $* $0(f[2]):
   d[f[1]]=d.get(f[1],0)+tofl(f[2])
  $K $%(f,'^')$* $0(f[2]):
   $4 v in symbols(f[1]):
    d[v]=d.get(v,0)+tofl(f[2])*0.001
  $K $2 $0(f)$* $((f)is $2 $a:
   $4 v in symbols(f):
    d[v]=d.get(v,0)+0.0001
$. sumkeys($P):
 vs=[]
 degs=[]
 $4 t in $P:
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
 $4 k in $n($`($P)):
  t=$P[k]
  d=degs[k]
  if $0(t):
   keys.$&((2,(),0,0,(),''))
  $K $2 d:
   cat=3 if has(t,'i')$+ 1
   keys.$&((cat,(),0,1 if $e(t)$+ 0,(),okey($9(t)[1])))
  $+:
   keys.$&((0,$/([-d.get(v,0)$4 v in mv]),-sum([d.get(v,0)$4 v in ov]),
 1 if $e(t)$+ 0,$/([-d.get(v,0)$4 v in ov]),okey($9(t)[1])))
 $! keys
$. pr_sum(e,$O):
 $P=$f(e[1:])
 if $2 $O:
  ks=sumkeys($P)
  idx=$f($n($`($P)))
  idx.sort(key=$@ i:ks[i])
  $P=[$P[i]$4 i in idx]
 $g=''
 first=$R
 $4 t in $P:
  s,p=pr(t,$6)
  if p<P_SUM+1 $* $2 s.$D('-')$* p<=P_SUM:
   s='('+s+')'
  if first:
   $g=s
   first=$6
  $K s.$D('-'):
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
 if $%(f,'^')$* $((f[1])is $a:
  if f[1]=='e':
   $!(2,(0,''),okey(f))
  $!(1,facprio(f[1]),okey(f))
 if $%(f,'+')or($%(f,'^')$* $%(f[1],'+')):
  $!(4,(0,''),okey(f))
 $!(2,(0,''),okey(f))
$. pr_factor(f,$O,first):
 s,p=pr(f,$O)
 if p<$j or(p==$j $* $2 first)or(s.$D('-')$* $2 first):
  $! '('+s+')'
 $! s
''')
_x(r'''$. pr_prod(e,$O):
 fs=$f(e[1:])
 $G=1
 if fs $* $0(fs[0])$* $2 $O:
  $G=fs[0]
  fs=fs[1:]
 $c=[]
 den=[]
 $4 f in fs:
  if $%(f,'^')$* $0(f[2])$* $?(f[2])<0:
   ex=nneg(f[2])
   den.$&(f[1]if ex==1 $+('^',f[1],ex))
  $K isq(f)$* $O:
   $c.$&(f[1])
   den.$&(f[2])
  $+:
   $c.$&(f)
 if $2 $O:
  $c.sort(key=fackey)
  den.sort(key=fackey)
 sign=''
 if $O $* $c $* $0($c[0])$* $?($c[0])<0:
  sign='-'
  if $c[0]==-1:
   $c=$c[1:]
  $+:
   $c[0]=nneg($c[0])
 cn=$G
 cd=1
 if $0($G):
  if $?($G)<0:
   sign='-'
   $G=nneg($G)
  if isq($G):
   cn=$G[1]
   cd=$G[2]
  $+:
   cn=$G
 if $O:
  $c=[f $4 f in $c if f!=1]or[1]
 if sign $* den $* $2 $O:
  sums=[k $4 k in $n($`($c))if $%($c[k],'+')]
  dsums=[k $4 k in $n($`(den))if $%(den[k],'+')]
  if $`(sums)==1 $* any([$e(t)$4 t in $c[sums[0]][1:]]):
   $c=$f($c)
   $c[sums[0]]=$A(-1,$c[sums[0]])
   sign=''
  $K $`(dsums)==1 $* $2 sums $* $`(den[dsums[0]])==3 $* $1(den[dsums[0]])$* any([$e(t)$4 t in den[dsums[0]][1:]]):
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
  if sign $* $`($c)==1 $* cn==1 $* pr($c[0],$6)[1]<=P_SUM:
   $! sign+'('+pr($c[0],$6)[0]+')',P_NEG
  $! sign+ns,(P_NEG if sign $+ $j)
 if $`($r)==1 $* $`($c)==1 $* cn==1:
  s,p=pr($c[0],$6)
  ns=paren(s,p,$j+1)if p<$j $+ s
  if s.$D('-'):
   ns='('+s+')'
 dparts=[]
 $4 f in den:
  dparts.$&(pr_factor(f,$6,$2 dparts))
 ds='*'.join(dparts)
 if $`(den)>1:
  ds='('+ds+')'
 $+:
  s,p=pr(den[0],$6)
  if p<=$j or s.$D('-'):
   ds='('+s+')'
 $! sign+ns+'/'+ds,(P_NEG if sign $+ $j)
$. pr_pow(e,$O):
 b=e[1]
 x=e[2]
 if $0(x)$* $?(x)<0 $* $2 $O:
  ex=nneg(x)
  d=b if ex==1 $+('^',b,ex)
  s,p=pr(d,$6)
  if p<=$j or s.$D('-'):
   s='('+s+')'
  $! '1/'+s,$j
 if x==$Y:
  s,p=pr(b,$6)
  if OPT['uni']:
   if($((b)is $Q $* b>=0)or($((b)is $a):
    $! '\u221a'+s,P_POW
   $! '\u221a('+s+')',$E
  $! '$N('+s+')',$E
 bs,bp=pr(b,$6)
 if bp<=P_POW or bs.$D('-')or $%(b,'fact'):
  bs='('+bs+')'
 xs,xp=pr(x,$6)
 if $2(($((x)is $Q $* x>=0)or($((x)is $a)):
  xs='('+xs+')'
 $! bs+'^'+xs,P_POW
$. fmt_top(e):
 if $%(e,'mat')$* $`(e)>2:
  rows=[]
  $4 r in e[1:]:
   rows.$&('['+','.join([fmt(a)$4 a in r[1:]])+']')
  if sum([$`(r)$4 r in rows])>28:
   $! '['+('\n '.join(rows))+']'
  $! '['+''.join(rows)+']'
 if $%(e,'$a'):
  $! e[1]
 $! fmt(e)
''')
_x(r'''REPL=(
 ('**','^'),('==','='),('!=','/='),
 ('sin\u207b\u00b9','$]'),('cos\u207b\u00b9','$k'),('tan\u207b\u00b9','$b'),
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
KEYW=('$*','or','xor','$2','nor','nand')
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
 n=$`(s)
 $= i<n:
  c=s[i]
  if c==' ' or c=='\t':
   i+=1
   $7
  if c=='0' $* i+2<n $* s[i+1]in 'bBhH':
   base=2 if s[i+1]in 'bB' $+ 16
   j=i+2
   dg='01' if base==2 $+ '0123456789abcdefABCDEF'
   $= j<n $* s[j]in dg:
    j+=1
   if j>i+2:
    toks.$&(('$c',$Q(s[i+2:j],base)))
    i=j
    $7
  if isdig(c)or(c=='.' $* i+1<n $* isdig(s[i+1])):
   j=i
   $= j<n $* isdig(s[j]):
    j+=1
   isf=$6
   if j<n $* s[j]=='.' $* $2(j+1<n $* s[j+1]in '^*/+-' $* $2 isdig(s[j+1])):
    isf=$R
    j+=1
    $= j<n $* isdig(s[j]):
     j+=1
   if j<n $*(s[j]=='E' or(s[j]=='e' $* j+1<n $* isdig(s[j+1]))):
    k=j+1
    if k<n $* s[k]in '+-':
     k+=1
    if k<n $* isdig(s[k]):
     isf=$R
     j=k
     $= j<n $* isdig(s[j]):
      j+=1
   txt=s[i:j]
   if isf:
    toks.$&(('$c',$-(txt)))
   $+:
    toks.$&(('$c',$Q(txt)))
   i=j
   $7
  if isletter(c):
   j=i
   $= j<n $*(isletter(s[j])or isdig(s[j])):
    j+=1
   $;=s[i:j].lower()
   toks.$&(('id',$;))
   i=j
   k=0
   $= i<n $* s[i]=="'":
    k+=1
    i+=1
   if k:
    toks.$&(('prime',k))
   $7
  if c=='"':
   j=s.find('"',i+1)
   if j<0:
    $[ $:('Missing "')
   toks.$&(('$a',s[i+1:j]))
   i=j+1
   $7
  $4 op in OPS:
   if s.$D(op,i):
    i+=$`(op)
    if op=='<>':
     op='/='
    if op=='>>':
     op='\u25ba'
    toks.$&(('op',op))
    break
  $+:
   $[ $:('Invalid character: '+c)
 toks.$&(('end',$)))
 $! toks
''')
_x(r'''class Parser:
 $. __init__($#,toks,$t):
  $#.t=toks
  $#.i=0
  $#.$t=$t
 $. peek($#):
  $! $#.t[$#.i]
 $. $q($#):
  tk=$#.t[$#.i]
  $#.i+=1
  $! tk
 $. $U($#,op):
  tk=$#.t[$#.i]
  $! tk[0]=='op' $* tk[1]==op
 $. isid($#,$;):
  tk=$#.t[$#.i]
  $! tk[0]=='id' $* tk[1]==$;
 $. expect($#,op):
  if $2 $#.$U(op):
   tk=$#.peek()
   $[ $:('Missing '+op)
  $#.i+=1
 $. top($#):
  e=$#.store()
  $= $#.$U('\u25ba'):
   $#.$q()
   tk=$#.$q()
   if tk[0]!='id':
    $[ $:('Syntax error after conversion')
   $>=[]
   if $#.$U('('):
    $#.$q()
    $>=$#.$>(')')
   e=('conv',e,tk[1])+$/($>)
  if $#.peek()[0]!='end':
   tk=$#.peek()
   $[ $:('Syntax error near '+$a(tk[1])if tk[1]is $2 $) $+ 'Syntax error')
  $! e
 $. store($#):
  if $#.isid('define'):
   $#.$q()
   lhs=$#.sum()
   if $2 $#.$U('='):
    $[ $:('Define needs =')
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
  $= $#.$U('|'):
   $#.$q()
   c=$#.iff()
   e=('|',e,c)
  $! e
 $. iff($#):
  e=$#.imp()
  $= $#.$U('<=>'):
   $#.$q()
   e=('<=>',e,$#.imp())
  $! e
 $. imp($#):
  e=$#.xor()
  $= $#.$U('=>'):
   $#.$q()
   e=('=>',e,$#.xor())
  $! e
 $. xor($#):
  e=$#.lor()
  $= $#.isid('xor')or $#.isid('nor')or $#.isid('nand'):
   op=$#.$q()[1]
   e=(op,e,$#.lor())
  $! e
 $. lor($#):
  e=$#.land()
  $= $#.isid('or'):
   $#.$q()
   e=('or',e,$#.land())
  $! e
 $. land($#):
  e=$#.lnot()
  $= $#.isid('$*'):
   $#.$q()
   e=('$*',e,$#.lnot())
  $! e
 $. lnot($#):
  if $#.isid('$2'):
   $#.$q()
   $!('$2',$#.lnot())
  $! $#.rel()
 $. rel($#):
  a=$#.sum()
  tk=$#.peek()
  if tk[0]=='op' $* tk[1]in('=','/=','<','>','<=','>='):
   $#.$q()
   b=$#.sum()
   r=(tk[1],a,b)
   tk2=$#.peek()
   if tk2[0]=='op' $* tk2[1]in('<','>','<=','>='):
    $#.$q()
    c=$#.sum()
    r=('$*',r,(tk2[1],b,c))
   $! r
  $! a
 $. sum($#):
  a=$#.prod()
  $= $R:
   tk=$#.peek()
   if tk[0]=='op' $* tk[1]in('+','-','.+','.-','&'):
    $#.$q()
    b=$#.prod()
    op=tk[1]
    if op=='.+':
     op='+'
    $K op=='.-':
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
  $= $R:
   tk=$#.peek()
   if tk[0]=='op' $* tk[1]in('*','/','.*','./'):
    $#.$q()
    b=$#.unary()
    op=tk[1]
    a=(op,a,b)
   $K $#.startsprimary():
    b=$#.pw()
    a=('*',a,b)
   $+:
    $! a
 $. unary($#):
  if $#.$U('-'):
   $#.$q()
   $!('${',$#.unary())
  if $#.$U('+'):
   $#.$q()
   $! $#.unary()
  $! $#.pw()
 $. pw($#):
  b=$#.post()
  if $#.$U('^')or $#.$U('.^'):
   op=$#.$q()[1]
   if $#.$U('\u1d40')or $#.isid('t')$* $6:
    pass
   x=$#.unary()
   $!('^' if op=='^' $+ '.^',b,x)
  $! b
 $. post($#):
  a=$#.primary()
  $= $R:
   if $#.$U('!'):
    $#.$q()
    a=('!',a)
   $K $#.$U('%'):
    $#.$q()
    a=('%',a)
   $K $#.$U('\u00b0'):
    $#.$q()
    a=('deg',a)
   $K $#.$U('\u1d40'):
    $#.$q()
    a=('call','transpose',a)
   $K $#.$U('['):
    $#.$q()
    idx=$#.$>(']')
    a=('index',a)+$/(idx)
   $+:
    $! a
 $. $>($#,close):
  $g=[]
  if $#.$U(close):
   $#.$q()
   $! $g
  $= $R:
   $g.$&($#.store_in())
   if $#.$U(','):
    $#.$q()
    $7
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
    $[ $:('Syntax error: '+$;)
   if $#.peek()[0]=='prime':
    n=$#.$q()[1]
    if $#.$U('('):
     $#.$q()
     a=$#.$>(')')
     $!('primecall',$;,n)+$/(a)
    $!('prime',$;,n)
   if $#.$U('(')$*($#.$t($;)or($`($;)>1 $* $; $2 in('pi','$T','$8','theta'))):
    $#.$q()
    a=$#.$>(')')
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
    $!('$f',)+$/($#.$>('}'))
   if op=='[':
    $! $#.matrix()
   if op=='\u221a':
    $!('call','$N',$#.post())
   if op=='-':
    $!('${',$#.pw())
  if k=='end':
   $[ $:('Incomplete expression')
  $[ $:('Syntax error near '+$a(tk[1]))
 $. matrix($#):
  rows=[]
  if $#.$U('['):
   $= $#.$U('['):
    $#.$q()
    rows.$&(('$f',)+$/($#.$>(']')))
    if $#.$U(','):
     $#.$q()
   $#.expect(']')
  $+:
   row=[]
   $= $R:
    if $#.$U(']'):
     $#.$q()
     break
    row.$&($#.store_in())
    if $#.$U(','):
     $#.$q()
    $K $#.$U(';'):
     $#.$q()
     rows.$&(('$f',)+$/(row))
     row=[]
    $K $#.$U(']'):
     $7
    $+:
     $[ $:('Missing ]')
   rows.$&(('$f',)+$/(row))
  n=$`(rows[0])
  $4 r in rows:
   if $`(r)!=n:
    $[ $:('Dimension error')
  $!('mat',)+$/(rows)
''')
_x(r'''$. parse(s,$t):
 toks=tokenize(s)
 if toks[0][0]=='end':
  $[ $:('Empty input')
 $! Parser(toks,$t).top()
''')
_x(r'''ENV={}
UFUN={}
ST={'ans':0,'deg':$6,'tmp':[]}
TRIG=('sin','cos','tan','sec','csc','cot')
ATRIG=('$]','$k','$b','arcsec','arccsc','arccot')
ALIAS={'asin':'$]','acos':'$k','atan':'$b','ceil':'ceiling',
 'asinh':'$w','acosh':'arccosh','atanh':'arctanh'}
$. $c(a,what='an integer'):
 if $2 isint(a):
  err('Argument must be '+what)
 $! a
$. x_log(u,b=$)):
 $! fn('ln',u)if b is $) $+ fn('log',u,b)
$. x_root(u,n=2):
 $! fn('root',u,n)
$. x_gcd(a,b):
 $! igcd($c(a),$c(b))
$. x_lcm(a,b):
 $! ilcm($c(a),$c(b))
$. x_mod(a,b):
 if $%(a,'^')$* isint(a[1])$* isint(a[2])$* a[2]>0 $* isint(b)$* b:
  r=1
  m=abs(b)
  x=a[1]%m
  e=a[2]
  $= e:
   if e&1:
    r=r*x%m
   x=x*x%m
   e>>=1
  $! r-m if b<0 $* r $+ r
 if $0(a)$* $0(b):
  if b==0:
   $! a
  $! nsub(a,$l(b,$}(ndiv(a,b))))
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
 $4 i in $n(k):
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
 $4 i in $n(k):
  r*=n-i
 $! r
$. primes(n):
 $g=[]
 p=2
 step=0
 $= p*p<=n:
  if n%p==0:
   k=0
   $= n%p==0:
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
 if $`(fs)==1:
  $!('hold',fs[0])
 $!('hold',('*',)+$/(fs))
$. x_approx(a):
 $! evalf(a)
$. x_exact(a):
 $! exactify(a)
$. x_expand(a):
 $! $^(a)
EXTRA={'log':x_log,'log10':$@ u:fn('log',u,10),'root':x_root,
 '$N':$@ u:fn('$N',u),'gcd':x_gcd,'lcm':x_lcm,
 'mod':x_mod,'ncr':x_ncr,'npr':x_npr,'factor':x_factor,
 'approx':x_approx,'exact':x_exact,'$^':x_expand,
 'numer':$@ a:numer_denom(a)[0],'denom':$@ a:numer_denom(a)[1]}
$. $t(n):
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
 if h=='${':
  $! ${(ev(t[1]))
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
 $>=[ev(a)$4 a in raw]
 if $; in UFUN:
  params,body=UFUN[$;]
  if $`($>)!=$`(params):
   err('Wrong number of arguments')
  $! subsd(body,dict(zip(params,$>)))
 if ST['deg']$* $; in TRIG $* $`($>)==1:
  $>[0]=$A($>[0],div('pi',180))
 f=EXTRA.get($;)
 try:
  r=f(*$>)if f is $2 $) $+ fn($;,*$>)
 $J $v:
  err('Wrong number of arguments $4 '+$;)
 if ST['deg']$* $; in ATRIG:
  r=$A(r,div(180,'pi'))
 $! r
$. ev_with(e,cond):
 d={}
 cs=[cond]
 $= cs:
  c=cs.pop()
  if $%(c,'$*'):
   cs.$&(c[1])
   cs.$&(c[2])
  $K $%(c,'=')$* $((c[1])is $a:
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
 if $((lhs)is $2 $a or lhs in $o or $t(lhs):
  err('Invalid variable $;')
 v=ev(rhs)
 ENV[lhs]=v
 $! v
$. relation(op,a,b):
 d=sub(a,b)
 if $0(d)$* $((d)is $2 $,:
  s=$?(d)
  ok={'=':s==0,'/=':s!=0,'<':s<0,'>':s>0,
 '<=':s<=0,'>=':s>=0}[op]
  $! 'true' if ok $+ 'false'
 if $1(d):
  v=$x(d)
  if $((v)is $-:
   ok={'=':abs(v)<1e-12,'/=':abs(v)>=1e-12,'<':v<0,'>':v>0,
 '<=':v<=0,'>=':v>=0}[op]
   $! 'true' if ok $+ 'false'
 $!(op,a,b)
$. register(s):
 low=s.replace(' ','')
 $4 part in(low.split(':=')[0],low.split('->')[-1]):
  i=part.find('(')
  if i>0 $* part[:i].isalpha()$* part[:i]$2 in ST['tmp']:
   ST['tmp'].$&(part[:i])
$. decimal(r):
 if $((r)is $Q or $((r)is $- or $2 $1(r)or has(r,'i'):
  $! $)
 if $((r)is $/ $* r[0]in('$a','hold'):
  $! $)
 try:
  v=evalf(r)
 $J Exception:
  $! $)
 if $((v)is $- or($((v)is $/ $* $1(v)):
  $! fmt(v)
 $! $)
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
 r=ev(parse(s,$t))
 if $%(r,'$a'):
  $! r[1]
 if $%(r,'hold'):
  ST['ans']=simp(r[1])
  $! fmt(r)
 ST['ans']=r
 $g=fmt(r)
 d=decimal(r)
 if d is $2 $) $* d!=$g:
  sep='  \u2248 ' if OPT['uni']$+ '  ~ '
  if $`($g)+$`(d)+4>32:
   sep='\n  \u2248 ' if OPT['uni']$+ '\n  ~ '
  $g+=sep+d
 $! $g
$. xcalc():
 print('nCAS exact calculator')
 print('Type an expression; q quits')
 blank=0
 $= $R:
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
    print('($( q $* enter to quit)')
    blank=0
   $7
  blank=0
  try:
   $g=run(s)
  $J $: as ex:
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
