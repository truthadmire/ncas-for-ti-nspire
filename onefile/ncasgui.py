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
_W={'!': 'return', '#': 'None', '%': 'append', '&': 'else', '(': 'isnode', ')': 'for', '*': 'and', '+': 'range', ',': 'def', '-': 'not', '.': 'autocancel', '/': 'type', '0': 'tuple', '1': 'len', '2': 'False', '3': 'complex', '4': 'isconst', '5': 'except', '6': 'continue', '7': 'Exception', '8': 'freeof', '9': 'out', ':': 'lambda', ';': 'depth', '<': 'mul', '=': 'add_list', '>': 'self', '?': 'expand', '@': 'elif', 'A': 'True', 'B': 'name', 'C': 'cplx', 'D': 'float', 'E': 'ZeroDivisionError', 'F': 'isnum', 'G': 'while', 'H': 'undef', 'I': 'mul_list', 'J': 'abs', 'K': 'list', 'L': 'integral', 'M': 'args', 'N': 'sqrt', 'O': 'break', 'P': 'inf', 'Q': 'terms', 'R': 'real', 'S': 'CASError', 'T': 'ValueError', 'U': 'div', 'V': 'p_divexact', 'W': 'subs', 'X': 'nval', 'Y': 'math', 'Z': 'coeffs', '[': 'rows', ']': 'sub', '^': 'add', '_': 'hasfloat', '`': 'nsign', 'a': 'OverflowError', 'b': 'coef_rest', 'c': 'vals', 'd': 'Expression', 'e': 'islist', 'f': 'rest', 'g': 'symbols', 'h': 'sols', 'i': 'linear', 'j': 'onevar_expr', 'k': 'raise', 'l': 'neg', 'm': 'NoSeries', 'n': 'isint', 'o': 'solve_eq', 'p': 'str', 'q': 'FSIMP', 'r': 'angle', 's': 'int', 't': 'KeyboardInterrupt', 'u': 'israt', 'v': 'HALF', 'w': 'arctan', 'x': 'isrealc', 'y': 'startswith', 'z': 'limit', '{': 'try', '|': 'arcsin', '}': 'extend', '~': 'parts'}
_x(r'''import $Y
class $S($7):
 pass
$, err(msg):
 $k $S(msg)
CONSTS=('pi','e','i')
SPECIAL=('pi','e','i','$P','$H','true','false')
$, igcd(a,b):
 if a<0:
  a=-a
 if b<0:
  b=-b
 $G b:
  a,b=b,a%b
 $! a
$, ilcm(a,b):
 if a==0 or b==0:
  $! 0
 $! $J(a//igcd(a,b)*b)
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
$v=('Q',1,2)
$, isq(x):
 $! $/(x)is $0 $* x[0]=='Q'
$, $n(x):
 $! $/(x)is $s
$, isfl(x):
 $! $/(x)is $D
$, $u(x):
 t=$/(x)
 $! t is $s or(t is $0 $* x[0]=='Q')
$, $F(x):
 t=$/(x)
 $! t is $s or t is $D or(t is $0 $* x[0]=='Q')
$, nd(x):
 if $/(x)is $s:
  $! x,1
 $! x[1],x[2]
$, tofl(x):
 t=$/(x)
 if t is $D:
  $! x
 if t is $s:
  $! $D(x)
 $! x[1]/x[2]
$, nadd(a,b):
 ta=$/(a)
 tb=$/(b)
 if ta is $s $* tb is $s:
  $! a+b
 if ta is $D or tb is $D:
  $! tofl(a)+tofl(b)
 an,ad=nd(a)
 bn,bd=nd(b)
 $! Q(an*bd+bn*ad,ad*bd)
$, nmul(a,b):
 ta=$/(a)
 tb=$/(b)
 if ta is $s $* tb is $s:
  $! a*b
 if ta is $D or tb is $D:
  $! tofl(a)*tofl(b)
 an,ad=nd(a)
 bn,bd=nd(b)
 $! Q(an*bn,ad*bd)
$, nneg(a):
 if $/(a)is $0:
  $!('Q',-a[1],a[2])
 $!-a
$, nsub(a,b):
 $! nadd(a,nneg(b))
$, ninv(a):
 t=$/(a)
 if t is $D:
  if a==0.0:
   err("Division by zero")
  $! 1.0/a
 n,d=nd(a)
 $! Q(d,n)
$, ndiv(a,b):
 $! nmul(a,ninv(b))
$, $`(a):
 if $/(a)is $0:
  a=a[1]
 if a>0:
  $! 1
 if a<0:
  $!-1
 $! 0
$, ncmp(a,b):
 $! $`(nsub(a,b))
$, nfloor(a):
 t=$/(a)
 if t is $s:
  $! a
 if t is $D:
  if a!=a or a in($D('$P'),$D('-$P')):
   err("Domain error")
  $! $s($Y.floor(a))
 $! a[1]//a[2]
$, nabs(a):
 if $`(a)<0:
  $! nneg(a)
 $! a
$, nipow(a,k):
 if k<0:
  $! nipow(ninv(a),-k)
 if $/(a)is $D:
  $! a**k
 n,d=nd(a)
 $! Q(n**k,d**k)
$, iroot(n,k):
 if n<2:
  $! n
 x=$s($Y.pow(n,1.0/k))if n<10**300 $& 1<<(($1(bin(n))-2)//k+1)
 if x<1:
  x=1
 $G $A:
  y=((k-1)*x+n//(x**(k-1)))//k
  if y>=x:
   $O
  x=y
 $G x**k>n:
  x-=1
 $G(x+1)**k<=n:
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
  $) i in $+(2,N):
   if $- s[i]:
    ps.$%(i)
    $) j in $+(i*i,N,i):
     s[j]=1
  SMALLP=ps
 $! SMALLP
$, $((e,h):
 $! $/(e)is $0 $* e[0]==h
$, head(e):
 if $/(e)is $0:
  $! e[0]
 $! $#
$, okey(e):
 $! repr(e)
$, has(e,x):
 if e==x:
  $! $A
 if $/(e)is $0 $* e[0]!='Q':
  $) a in e[1:]:
   if has(a,x):
    $! $A
 $! $2
$, $8(e,x):
 $! $- has(e,x)
$, freeofall(e,xs):
 $) x in xs:
  if has(e,x):
   $! $2
 $! $A
$, $g(e,$9=$#):
 if $9 is $#:
  $9=[]
 t=$/(e)
 if t is $p:
  if e $- in SPECIAL $* e $- in $9:
   $9.$%(e)
 $@ t is $0 $* e[0]!='Q' $* e[0]!='$p':
  $) a in e[1:]:
   $g(a,$9)
 $! $9
$, $4(e):
 t=$/(e)
 if t is $p:
  $! e in SPECIAL
 if t is $0 $* e[0]!='Q':
  if e[0]=='$p':
   $! $2
  $) a in e[1:]:
   if $- $4(a):
    $! $2
 $! $A
$, $_(e):
 t=$/(e)
 if t is $D:
  $! $A
 if t is $0 $* e[0]!='Q':
  $) a in e[1:]:
   if $_(a):
    $! $A
 $! $2
$, $b(a):
 if $/(a)is $0 $* a[0]=='*' $* $F(a[1]):
  if $1(a)==3:
   $! a[1],a[2]
  $! a[1],('*',)+a[2:]
 $! 1,a
$, cmul(c,r):
 if $/(c)is $s $* c==1:
  $! r
 if $/(r)is $0 $* r[0]=='*':
  if $F(r[1]):
   c=nmul(c,r[1])
   if $/(c)is $s $* c==1:
    $!('*',)+r[2:]if $1(r)>3 $& r[2]
   $!('*',c)+r[2:]
  $!('*',c)+r[1:]
 $!('*',c,r)
$, $^(*$M):
 $! $=($M)
$, $=($M):
 num=0
 $Q={}
 order=[]
 st=$K($M)
 infs=0
 $G st:
  a=st.pop()
  t=$/(a)
  if t is $s or t is $D:
   num=nadd(num,a)
   $6
  if t is $0:
   h=a[0]
   if h=='Q':
    num=nadd(num,a)
    $6
   if h=='+':
    st.$}(a[1:])
    $6
   if h=='*' $* $F(a[1]):
    c=a[1]
    r=a[2]if $1(a)==3 $&('*',)+a[2:]
   $&:
    c=1
    r=a
  $&:
   if a=='$H':
    $! '$H'
   c=1
   r=a
  if r=='$P':
   s=$`(c)
   if s==0:
    $6
   if infs $* infs!=s:
    $! '$H'
   infs=s
   $6
  if r in $Q:
   $Q[r]=nadd($Q[r],c)
  $&:
   $Q[r]=c
   order.$%(r)
 if infs:
  $! '$P' if infs>0 $&('*',-1,'$P')
 $9=[]
 $) r in order:
  c=$Q[r]
  if c==0:
   $6
  $9.$%(cmul(c,r))
 if num!=0 or $- $9:
  if $9 $* num==0:
   pass
  $&:
   $9.$%(num)
 if $1($9)==1:
  $! $9[0]
 $9.sort(key=okey)
 $!('+',)+$0($9)
$, isrrad(e):
 $! $/(e)is $0 $* e[0]=='^' $* $/(e[1])is $s $* isq(e[2])
$, $<(*$M):
 $! $I($M)
''')
_x(r'''$, $I($M):
 coef=1
 bases={}
 order=[]
 st=$K($M)
 $G st:
  a=st.pop()
  t=$/(a)
  if t is $s or t is $D:
   coef=nmul(coef,a)
   $6
  if t is $0:
   h=a[0]
   if h=='Q':
    coef=nmul(coef,a)
    $6
   if h=='*':
    st.$}(a[1:])
    $6
   if h=='^':
    b=a[1]
    x=a[2]
   $&:
    b=a
    x=1
  $&:
   if a=='$H':
    $! '$H'
   b=a
   x=1
  if b in bases:
   bases[b]=$^(bases[b],x)
  $&:
   bases[b]=x
   order.$%(b)
 if coef==0:
  if '$P' in bases:
   $! '$H'
  $) b in order:
   if b=='$H' or has(b,'$H'):
    $! '$H'
  $! coef
 facs=[]
 rad={}
 radorder=[]
 $, collect(p):
  c=1
  t=$/(p)
  if t is $s or t is $D or(t is $0 $* p[0]=='Q'):
   $! p
  if t is $0 $* p[0]=='*':
   items=p[1:]
  $&:
   items=(p,)
  $) f in items:
   if $F(f):
    c=nmul(c,f)
   $@ isrrad(f):
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
 $) b in order:
  p=pw(b,bases[b])
  if p=='$H':
   $! '$H'
  coef=nmul(coef,collect(p))
 if rad:
  multi=$1(radorder)!=$1(rad)
  if multi:
   items=[(ex,rad[ex])$) ex in radorder if ex is $- $#]
   rad.clear()
   del radorder[:]
   pend=[]
   $) ex,b in items:
    pend.$%(pw_num(b,ex))
   $) p in pend:
    coef=nmul(coef,collect(p))
  $) ex in rad:
   facs.$%(('^',rad[ex],ex))
 if coef==0:
  $! 0
 if '$P' in facs:
  if $1(facs)==1 or $A:
   coef=$`(coef)if $/(coef)is $- $D $&(1.0 if coef>0 $&-1.0)
   if $/(coef)is $D:
    coef=$s(coef)
 if $- facs:
  $! coef
 if $1(facs)>1:
  algs=[f $) f in facs if $((f,'+')$* isalg(f)]
  if algs $* all([isalg(f)$) f in facs]):
   r=coef
   $) f in facs:
    r=expand_mul(r,f)
   $! r
 if $1(facs)==1:
  f=facs[0]
  if $/(coef)is $s $* coef==1:
   $! f
  if $/(f)is $0 $* f[0]=='+':
   $! $=([$<(coef,t)$) t in f[1:]])
  $!('*',coef,f)
 facs.sort(key=okey)
 if $/(coef)is $s $* coef==1:
  $!('*',)+$0(facs)
 $!('*',coef)+$0(facs)
$, $l(a):
 $! $<(-1,a)
$, $](a,b):
 $! $^(a,$<(-1,b))
$, $U(a,b):
 $! $<(a,pw(b,-1))
$, inv(a):
 $! pw(a,-1)
$, $N(a):
 $! pw(a,$v)
$, factor_int_small(n):
 fs=[]
 $) p in smallprimes():
  if p*p>n:
   $O
  if n%p==0:
   k=0
   $G n%p==0:
    n//=p
    k+=1
   fs.$%((p,k))
 $! fs,n
$, radical(n,q):
 if n<2:
  $! n,1
 a=1
 m=1
 fs,$f=factor_int_small(n)
 $) p,k in fs:
  a*=p**(k//q)
  m*=p**(k%q)
 if $f>1:
  r=iroot($f,q)
  if r**q==$f:
   a*=r
  $&:
   m*=$f
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
 $G(1<<k)<=m $* k<=64:
  r=iroot(m,k)
  if r**k==m:
   best=(r,k)
  k+=1
 if best is $- $#:
  m=best[0]
  ex=Q(best[1],q)
 if ex==1:
  $! a*m
 if $n(ex):
  $! a*m**ex
 if a==1:
  $!('^',m,ex)
 $!('*',a,('^',m,ex))
MAXBITS=12000
$, ibits(n):
 if n==0:
  $! 0
 h='%x'%$J(n)
 v=$s(h[0],16)
 $! 4*$1(h)-(3 if v<2 $& 2 if v<4 $& 1 if v<8 $& 0)
$, bigpow(b,x):
 n,d=nd(b)
 if d==1 $* $J(n)<=1:
  $! $2
 $! $J(x)*(ibits(n)+(ibits(d)if d>1 $& 0))>MAXBITS
$, pw_num(b,x):
 if $/(b)is $D or $/(x)is $D:
  bf=tofl(b)
  xf=tofl(x)
  if bf==0.0:
   if xf>0:
    $! 0.0
   if xf==0:
    $! 1.0
   $! '$H'
  if bf!=bf or xf!=xf:
   $! '$H'
  if bf<0 $*(xf in($D('$P'),$D('-$P'))or xf!=$Y.floor(xf)):
   if $u(x)$* nd(x)[1]%2==1:
    r=(-bf)**xf
    $!-r if nd(x)[0]%2 $& r
   z=$3(bf)**xf
   $! fromcomplex(z)
  ${:
   $! bf**xf
  $5 $a:
   $! '$P'
 if $/(x)is $s:
  if b==0:
   if x<0:
    $! '$H'
   $! 0
  if bigpow(b,x):
   $!('^',b,x)
  $! nipow(b,x)
 p,q=nd(x)
 if b==0:
  $! 0 if p>0 $& '$H'
 if $`(b)<0:
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
 $~=[]
 if n>1:
  $~.$%(ipow_root(n,fp,fq))
 if d>1:
  $~.$%(Q(1,d))
  $~.$%(ipow_root(d,fq-fp,fq))
 c=res
 facs=[]
 $) pt in $~:
  if $F(pt):
   c=nmul(c,pt)
  $@ pt[0]=='*':
   c=nmul(c,pt[1])
   facs.$%(pt[2])
  $&:
   facs.$%(pt)
 if $1(facs)==2:
  if facs[0][2]==facs[1][2]:
   $! $<(c,pw_num(facs[0][1]*facs[1][1],facs[0][2]))
  facs.sort(key=okey)
 if $- facs:
  $! c
 if c==1:
  if $1(facs)==1:
   $! facs[0]
  $!('*',)+$0(facs)
 $!('*',c)+$0(facs)
$, isposconst(e):
 if $F(e):
  $! $`(e)>0
 if e=='pi' or e=='e':
  $! $A
 if isrrad(e):
  $! e[1]>0
 if $((e,'^')$*(e[1]=='e' or e[1]=='pi')$* isreal_expr(e[2]):
  $! $A
 $! $2
$, isalg(e):
 t=$/(e)
 if t is $s or t is $D:
  $! $A
 if t is $p:
  $! e=='i'
 h=e[0]
 if h=='Q':
  $! $A
 if h=='^':
  $! $F(e[1])$* $F(e[2])
 if h=='+' or h=='*':
  $) a in e[1:]:
   if $- isalg(a):
    $! $2
  $! $A
 $! $2
''')
_x(r'''$, pw(b,x):
 if x==0:
  if b=='$H' or b=='$P':
   $! '$H'
  $! 1
 if $/(x)is $s $* x==1:
  $! b
 if b=='$H' or x=='$H':
  $! '$H'
 bn=$F(b)
 xn=$F(x)
 if bn $* xn:
  $! pw_num(b,x)
 if b==1 $* $/(b)is $s:
  $! 1
 if b=='$P':
  if xn:
   $! '$P' if $`(x)>0 $& 0
  if x=='$P':
   $! '$P'
 if xn $* b==0:
  $! 0 if $`(x)>0 $& '$H'
 if b=='i' $* $/(x)is $s:
  r=x%4
  $!(1,'i',-1,('*',-1,'i'))[r]
 if x=='$P' $* bn:
  if nabs(b)==1:
   $! '$H' if b==1 $& '$H'
  if ncmp(nabs(b),1)>0:
   $! '$P' if $`(b)>0 $& '$H'
  $! 0
 if b=='e':
  if x=='$P':
   $! '$P'
  if $((x,'*')$* $1(x)==3 $* x[1]==-1 $* x[2]=='$P':
   $! 0
  if $/(x)is $D:
   $! $Y.exp(x)
  if $((x,'ln'):
   $! x[1]
  if $((x,'*'):
   c,r=$b(x)
   if $((r,'ln')$* $u(c):
    $! pw(r[1],c)
  if $((x,'+'):
   outs=[]
   $f=[]
   $) t in x[1:]:
    c,r=$b(t)
    if $((r,'ln')$* $u(c):
     outs.$%(pw(r[1],c))
    $&:
     $f.$%(t)
   if outs:
    $! $I(outs+[pw('e',$=($f))])
  if $((x,'*')$* 'i' in x $* 'pi' in x:
   c,r=$b(x)
   if r==('*','i','pi')$* $u(c):
    $! $^(cos_($<(c,'pi')),$<('i',sin_($<(c,'pi'))))
 if b!='e' $* $4(b)$* $4(x)$* $- $u(x)$*(has(b,'i')or has(x,'i'))$* $- $_(x):
  L=fn('ln',b)
  if $- $((L,'ln')$* $-($((L,'+')$* any([$((t,'ln')$) t in L[1:]])):
   $! pw('e',$?($<(x,L)))
 if $/(b)is $0:
  h=b[0]
  if h=='^':
   bb=b[1]
   ee=b[2]
   if $/(x)is $s:
    $! pw(bb,$<(ee,x))
   if isposconst(bb):
    $! pw(bb,$<(ee,x))
   if $u(ee)$* $u(x):
    r=nmul(ee,x)
    if $/(ee)is $s:
     if ee%2==0:
      if $/(r)is $s $* r%2==0:
       $! pw(bb,r)
      $! pw(fn('$J',bb),r)
     $! pw(bb,r)
    if nd(ee)[0]%2==1 $* nd(ee)[1]%2==1:
     $! pw(bb,r)
    if nd(ee)[0]%2==1:
     $! pw(bb,r)
  $@ h=='*':
   if $/(x)is $s:
    $! $I([pw(f,x)$) f in b[1:]])
   outs=[]
   $f=[]
   $) f in b[1:]:
    if $F(f):
     if $`(f)>0:
      outs.$%(pw(f,x))
     $@ f!=-1:
      outs.$%(pw(nneg(f),x))
      $f.$%(-1)
     $&:
      $f.$%(f)
    $@ isposconst(f)or $((f,'$J'):
     outs.$%(pw(f,x))
    $&:
     $f.$%(f)
   if outs:
    $! $I(outs+[pw($I($f),x)])
  $@ h=='$J':
   if $/(x)is $s $* x%2==0:
    $! pw(b[1],x)
  $@ h=='+':
   if x==$v $* isalg(b)$* $- has(b,'i'):
    dn=denest(b)
    if dn is $- $#:
     $! dn
   if isq(x)$* x[2]==2 $* $`(x)<0 $* isalg(b)$* $- has(b,'i'):
    dn=denest(b)
    if dn is $- $#:
     $! pw(pw(dn,-1),-x[1])if x[1]!=-1 $& pw(dn,-1)
   if $/(x)is $s $* x!=1 $* $- isalg(b):
    c=sumcontent(b)
    if c!=1:
     $! $<(pw(c,x),pw($<(ninv(c),b),x))
    if leadneg(b):
     nb=$<(-1,b)
     if x%2==0:
      $! pw(nb,x)
     $! $<(-1,pw(nb,x))
   if $/(x)is $s $* isalg(b):
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
 fs=r[1:]if $((r,'*')$&(r,)
 $) f in fs:
  if $/(f)is $p $* f $- in SPECIAL:
   d+=1
  $@ $((f,'^')$* $/(f[1])is $p $* f[1]$- in SPECIAL $* $F(f[2]):
   d+=tofl(f[2])
 $! d
$, leadneg(b):
 best=$#
 bk=$#
 $) t in b[1:]:
  if $F(t):
   $6
  c,r=$b(t)
  k=(-tdeg(r),okey(r))
  if bk is $# or k<bk:
   bk=k
   best=c
 if best is $#:
  $! $2
 $! $`(best)<0 if $F(best)$& $2
$, sumcontent(b):
 g=0
 L=1
 $) t in b[1:]:
  c,r=$b(t)
  if $- $u(c):
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
 $) t in b[1:]:
  if $u(t):
   a=nadd(a,t)
   $6
  cc,r=$b(t)
  if isrrad(r)$* r[2]==$v $* $u(cc)$*(n is $# or n==r[1]):
   n=r[1]
   c=nadd(c,cc)
  $&:
   $! $#
 if n is $# or c==0:
  $! $#
 d2=nsub(nmul(a,a),nmul(nmul(c,c),n))
 if $`(d2)<0:
  $! $#
 dn,dd=nd(d2)
 rn=isqrt(dn)
 rd=isqrt(dd)
 if rn*rn!=dn or rd*rd!=dd:
  $! $#
 d=Q(rn,rd)
 p=ndiv(nadd(a,d),2)
 m=ndiv(nsub(a,d),2)
 if $`(p)<0 or $`(m)<0:
  $! $#
 r=$^(pw(p,$v),$<($`(c),pw(m,$v)))
 if $((r,'+')$* $1(r)<=3:
  $! r
 $! $#
$, expand_mul(a,b):
 ta=a[1:]if $((a,'+')$&(a,)
 tb=b[1:]if $((b,'+')$&(b,)
 $9=[]
 $) u in ta:
  $) v in tb:
   $9.$%($<(u,v))
 $! $=($9)
$, expand_pow(b,n):
 r=1
 p=b
 $G n>0:
  if n&1:
   r=expand_mul(r,p)
  n>>=1
  if n:
   p=expand_mul(p,p)
 $! r
$, rationalize_inv(b):
 re_,im_=reim(b)
 if im_!=0:
  d=$^($<(re_,re_),$<(im_,im_))
  d=$?(d)
  if $((d,'+'):
   r2=rationalize_inv(d)
   if r2 is $#:
    $! $#
  $&:
   r2=pw(d,-1)
  $! expand_mul($](re_,$<('i',im_)),r2)
 $Q=b[1:]if $((b,'+')$&(b,)
 kern=$#
 kerns=[]
 $) t in $Q:
  c,r=$b(t)
  if r!=1 $* $- $F(r):
   if isrrad(r)$* r[2]==$v:
    if r $- in kerns:
     kerns.$%(r)
   $&:
    $! $#
 if $- kerns or $1(kerns)>3:
  $! $#
 kern=kerns[0]
 if $1(kerns)>1:
  A=$=([t $) t in $Q if $b(t)[1]!=kern])
  B=$=([$b(t)[0]$) t in $Q if $b(t)[1]==kern])
  den=$?($]($<(A,A),$<(B,B,kern[1])))
  if den==0:
   $! $#
  if $((den,'+'):
   r2=rationalize_inv(den)
   if r2 is $#:
    $! $#
  $&:
   r2=pw(den,-1)
  $! expand_mul($](A,$<(B,kern)),r2)
 a0=0
 a1=0
 $) t in $Q:
  c,r=$b(t)
  if r==kern:
   a1=nadd(a1,c)
  $&:
   a0=$^(a0,t)
 den=$]($<(a0,a0),$<(nmul(a1,a1),kern[1]))
 if den==0:
  $! $#
 $! expand_mul($](a0,$<(a1,kern)),pw(den,-1))
''')
_x(r'''$, reim(e):
 t=$/(e)
 if t is $s or t is $D:
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
  $) a in e[1:]:
   r,i=reim(a)
   rs.$%(r)
   ims.$%(i)
  $! $=(rs),$=(ims)
 if h=='*':
  r=1
  i=0
  $) a in e[1:]:
   ar,ai=reim(a)
   if ai==0:
    r=$<(r,ar)
    i=$<(i,ar)
   $&:
    r,i=$]($<(r,ar),$<(i,ai)),$^($<(r,ai),$<(i,ar))
  $! r,i
 if h=='^':
  b=e[1]
  x=e[2]
  if $- has(b,'i')$* $- has(x,'i'):
   if $F(x)$* $- $u(x):
    $! e,0
   if $u(x)$* nd(x)[1]%2==0:
    if $4(b):
     v=cv(b)
     if v is $- $# $* $/(v)is $- $3 $* v<0:
      $! reim_generic(e)
    $! e,0
   $! e,0
  if $/(x)is $s:
   br,bi=reim(b)
   if x>0:
    z=expand_pow($^(br,$<('i',bi)),x)
    if has(z,'i')$* z!=e:
     $! reim(z)
   $@ $4(b):
    r=rationalize_inv(b)
    if r is $- $#:
     $! reim(expand_pow(r,-x))if x!=-1 $& reim(r)
  $! reim_generic(e)
 if h in('$K','mat','$p'):
  $! e,0
 $) a in e[1:]:
  if has(a,'i'):
   $! reim_generic(e)
 $! e,0
$, cv(u):
 ${:
  v=$X(u)
 $5($S,$T,$E,$a,TypeError):
  $! $#
 if v!=v:
  $! $#
 if $/(v)is $3:
  if v.$R!=v.$R or v.imag!=v.imag:
   $! $#
  if $J(v.$R)==$D('$P')or $J(v.imag)==$D('$P'):
   $! $#
 $@ $J(v)==$D('$P'):
  $! $#
 $! v
$, reim_generic(e):
 if $4(e):
  v=cv(e)
  if v is $#:
   $!('$R',e),('imag',e)
  z=$3(v)
  $! z.$R,z.imag
 $!('$R',e),('imag',e)
$, conj(e):
 r,i=reim(e)
 $! $](r,$<('i',i))
$, fromcomplex(z):
 if $/(z)is $- $3:
  $! z
 if z.imag==0:
  $! z.$R
 if z.$R==0:
  $! $<(z.imag,'i')
 $! $^(z.$R,$<(z.imag,'i'))
$q={}
$, fn($B,*$M):
 if $1($M)==1 $* $/($M[0])is $K:
  $M=$0($M[0])
 $) a in($M[:1]if $B=='when' $& $M):
  if a=='$H':
   $! '$H'
 f=$q.get($B)
 if f is $- $#:
  r=f(*$M)
  if r is $- $#:
   $! r
 $!($B,)+$0($M)
$, isneg(e):
 if $F(e):
  $! $`(e)<0
 if $((e,'*'):
  $! $F(e[1])$* $`(e[1])<0
 if $((e,'+'):
  $! leadneg(e)
 $! $2
$, isreal_expr(e):
 if $F(e):
  $! $A
 if $/(e)is $p:
  $! e!='i' $* e!='$H'
 $! $- has(e,'i')
$, fval($B,x):
 $! fromcomplex(NUMF[$B](x))
$, fvalc($B,u):
 ${:
  v=NUMF[$B]($X(u))
 $5($S,$T,$E,$a,TypeError):
  $! $#
 if $/(v)is $3:
  if v.$R!=v.$R or v.imag!=v.imag:
   $! $#
 $@ v!=v:
  $! $#
 $! fromcomplex(v)
$, pi_coef(u):
 if u=='pi':
  $! 1
 if u==0:
  $! 0
 if $((u,'*')$* $1(u)==3 $* u[2]=='pi' $* $u(u[1]):
  $! u[1]
 $! $#
$, split_pi(u):
 if $((u,'+'):
  $) t in u[1:]:
   c=pi_coef(t)
   if c is $- $# $* c!=0:
    $f=$=([s $) s in u[1:]if s is $- t])
    $! c,$f
 $! $#
TRIGT=$#
$, trig_table():
 global TRIGT
 if TRIGT is $#:
  s2=$N(2)
  s3=$N(3)
  s5=$N(5)
  s6=$N(6)
  q=Q
  T={}
  T[0]=0
  T[q(1,12)]=$<(q(1,4),$](s6,s2))
  T[q(1,10)]=$<(q(1,4),$](s5,1))
  T[q(1,8)]=$<($v,$N($](2,s2)))
  T[q(1,6)]=$v
  T[q(1,5)]=$<(q(1,4),$N($](10,$<(2,s5))))
  T[q(1,4)]=$<($v,s2)
  T[q(3,10)]=$<(q(1,4),$^(s5,1))
  T[q(1,3)]=$<($v,s3)
  T[q(3,8)]=$<($v,$N($^(2,s2)))
  T[q(2,5)]=$<(q(1,4),$N($^(10,$<(2,s5))))
  T[q(5,12)]=$<(q(1,4),$^(s6,s2))
  T[$v]=1
  TT={}
  TT[0]=0
  TT[q(1,12)]=$](2,s3)
  TT[q(1,8)]=$](s2,1)
  TT[q(1,6)]=$<(q(1,3),s3)
  TT[q(1,4)]=1
  TT[q(1,3)]=s3
  TT[q(3,8)]=$^(s2,1)
  TT[q(5,12)]=$^(2,s3)
  TT[q(1,5)]=$N($](5,$<(2,s5)))
  TT[q(2,5)]=$N($^(5,$<(2,s5)))
  TT[q(1,10)]=$<(q(1,5),$N($](25,$<(10,s5))))
  TT[q(3,10)]=$<(q(1,5),$N($^(25,$<(10,s5))))
  TRIGT=(T,TT)
 $! TRIGT
$, sin_pi(c):
 c=nsub(c,nmul(2,nfloor(nmul(c,$v))))
 sg=1
 if ncmp(c,1)>=0:
  c=nsub(c,1)
  sg=-1
 if ncmp(c,$v)>0:
  c=nsub(1,c)
 T=trig_table()[0]
 if c in T:
  $! $<(sg,T[c])
 if sg<0:
  $! $l(('sin',$<(c,'pi')))
 $!('sin',$<(c,'pi'))
$, tan_pi(c):
 c=nsub(c,nfloor(c))
 sg=1
 if ncmp(c,$v)>0:
  c=nsub(1,c)
  sg=-1
 if c==$v:
  $! '$H'
 TT=trig_table()[1]
 if c in TT:
  $! $<(sg,TT[c])
 $! $<(sg,('tan',$<(c,'pi')))
$, sin_(u):
 if $F(u):
  if u==0:
   $! 0
  if $/(u)is $D:
   $! $Y.sin(u)
  if $`(u)<0:
   $! $l(fn('sin',$l(u)))
  $! $#
 if u=='$P' or u==('*',-1,'$P'):
  $! '$H'
 c=pi_coef(u)
 if c is $- $#:
  $! sin_pi(c)
 if $_(u)$* $4(u):
  $! fvalc('sin',u)
 if isneg(u):
  $! $l(fn('sin',$l(u)))
 sp=split_pi(u)
 if sp is $- $#:
  c,$f=sp
  c=nsub(c,nmul(2,nfloor(nmul(c,$v))))
  if c==0:
   $! fn('sin',$f)
  if c==1:
   $! $l(fn('sin',$f))
  if c==$v:
   $! fn('cos',$f)
  if c==Q(3,2):
   $! $l(fn('cos',$f))
  if ncmp(c,1)>0:
   $!('sin',$^($f,$<(nsub(c,2),'pi')))
  $!('sin',$^($f,$<(c,'pi')))
 if $((u,'$|'):
  $! u[1]
 if $((u,'arccos'):
  $! $N($](1,pw(u[1],2)))
 if $((u,'$w'):
  $! $U(u[1],$N($^(1,pw(u[1],2))))
 $! $#
''')
_x(r'''$, cos_(u):
 if $F(u):
  if u==0:
   $! 1
  if $/(u)is $D:
   $! $Y.cos(u)
  if $`(u)<0:
   $! fn('cos',$l(u))
  $! $#
 if u=='$P' or u==('*',-1,'$P'):
  $! '$H'
 c=pi_coef(u)
 if c is $- $#:
  $! sin_pi(nadd(c,$v))
 if $_(u)$* $4(u):
  $! fvalc('cos',u)
 if isneg(u):
  $! fn('cos',$l(u))
 sp=split_pi(u)
 if sp is $- $#:
  c,$f=sp
  c=nsub(c,nmul(2,nfloor(nmul(c,$v))))
  if c==0:
   $! fn('cos',$f)
  if c==1:
   $! $l(fn('cos',$f))
  if c==$v:
   $! $l(fn('sin',$f))
  if c==Q(3,2):
   $! fn('sin',$f)
  if ncmp(c,1)>0:
   $!('cos',$^($f,$<(nsub(c,2),'pi')))
  $!('cos',$^($f,$<(c,'pi')))
 if $((u,'arccos'):
  $! u[1]
 if $((u,'$|'):
  $! $N($](1,pw(u[1],2)))
 if $((u,'$w'):
  $! pw($^(1,pw(u[1],2)),Q(-1,2))
 $! $#
$, tan_(u):
 if $F(u):
  if u==0:
   $! 0
  if $/(u)is $D:
   $! $Y.tan(u)
  if $`(u)<0:
   $! $l(fn('tan',$l(u)))
  $! $#
 c=pi_coef(u)
 if c is $- $#:
  $! tan_pi(c)
 if $_(u)$* $4(u):
  $! fvalc('tan',u)
 if isneg(u):
  $! $l(fn('tan',$l(u)))
 sp=split_pi(u)
 if sp is $- $#:
  c,$f=sp
  c=nsub(c,nfloor(c))
  if c==0:
   $! fn('tan',$f)
  if c==$v:
   $! $l(pw(fn('tan',$f),-1))
  $!('tan',$^($f,$<(c,'pi')))
 if $((u,'$w'):
  $! u[1]
 $! $#
INVT=$#
$, inv_table():
 global INVT
 if INVT is $#:
  T,TT=trig_table()
  S={}
  $) k in T:
   S[T[k]]=k
  Tn={}
  $) k in TT:
   Tn[TT[k]]=k
  INVT=(S,Tn)
 $! INVT
$, asin_(u):
 if $F(u):
  if $/(u)is $D:
   if-1.0<=u<=1.0:
    $! $Y.asin(u)
   $! fval('$|',u)
 if isneg(u):
  $! $l(fn('$|',$l(u)))
 S=inv_table()[0]
 if u in S:
  $! $<(S[u],'pi')
 if $4(u)$* $_(u):
  $! fvalc('$|',u)
 $! $#
$, acos_(u):
 if $F(u)$* $/(u)is $D:
  if-1.0<=u<=1.0:
   $! $Y.acos(u)
  $! fval('arccos',u)
 a=asin_(u)
 if a is $- $# $* $- $((a,'$|')$* $8(a,'$|'):
  $! $]($<($v,'pi'),a)
 if isneg(u):
  $! $]('pi',fn('arccos',$l(u)))
 $! $#
$, atan_(u):
 if $F(u):
  if $/(u)is $D:
   $! $Y.atan(u)
 if u=='$P':
  $! $<($v,'pi')
 if u==('*',-1,'$P'):
  $! $<(Q(-1,2),'pi')
 if isneg(u):
  $! $l(fn('$w',$l(u)))
 Tn=inv_table()[1]
 if u in Tn:
  $! $<(Tn[u],'pi')
 if $4(u)$* $_(u):
  $! fvalc('$w',u)
 $! $#
$, ln_(u):
 if $F(u):
  if u==1:
   $! 0
  if u==0:
   $!('*',-1,'$P')
  if $/(u)is $D:
   if u>0:
    $! $Y.log(u)
   $! $^($Y.log(-u),$<($Y.pi,'i'))
  if $`(u)<0:
   $! $^(fn('ln',nneg(u)),$<('i','pi'))
  n,d=nd(u)
  if n==1:
   $! $l(fn('ln',d))
  $! $#
 if u=='e':
  $! 1
 if u=='$P':
  $! '$P'
 if u=='i':
  $! $<($v,'i','pi')
 if $((u,'^'):
  if u[1]=='e' $* isreal_expr(u[2]):
   $! u[2]
  if isposconst(u[1])$* isreal_expr(u[2])$* $F(u[2]):
   $! $<(u[2],fn('ln',u[1]))
 if $4(u)$* $_(u):
  $! fvalc('ln',u)
 $! $#
$, log_(u,b=10):
 if $F(u)$* $F(b):
  if $/(u)is $D or $/(b)is $D:
   a1=fvalc('ln',u)
   a2=fvalc('ln',b)
   if a1 is $- $# $* a2 is $- $# $* a2!=0:
    $! $U(a1,a2)
   $! $#
  if u==1:
   $! 0
  if $u(u)$* $u(b)$* $`(u)>0 $* $`(b)>0 $* b!=1:
   k=exact_log(u,b)
   if k is $- $#:
    $! k
 if u==b:
  $! 1
 if $((u,'^')$* u[1]==b $* isreal_expr(u[2]):
  $! u[2]
 if $4(u)$* $4(b)$*($_(u)or $_(b)):
  a1=fvalc('ln',u)
  a2=fvalc('ln',b)
  if a1 is $- $# $* a2 is $- $# $* a2!=0:
   $! $U(a1,a2)
  $! $#
 $! $#
$, exact_log(u,b):
 un,ud=nd(u)
 bn,bd=nd(b)
 lu=$Y.log(tofl(u))
 lb=$Y.log(tofl(b))
 if lb==0:
  $! $#
 k=lu/lb
 $) den in $+(1,13):
  num=$s(round(k*den))
  if $J(k*den-num)<1e-9:
   kk=Q(num,den)
   if pw_num(b,kk)==u:
    $! kk
   $! $#
 $! $#
$, abs_(u):
 if $F(u):
  $! nabs(u)
 if u=='$P' or u==('*',-1,'$P'):
  $! '$P'
 if $((u,'$J'):
  $! u
 if $((u,'^')$* $/(u[2])is $s $* u[2]%2==0 $* isreal_expr(u[1]):
  $! u
 if has(u,'i'):
  r,i=reim(u)
  if i!=0 $* $- has(r,'i')$* $- has(i,'i'):
   $! $N($^(pw(r,2),pw(i,2)))
 if $4(u):
  v=cv(u)
  if v is $- $# $* $/(v)is $- $3:
   if v>=0:
    $! u
   $! $l(u)
 if $((u,'*'):
  outs=[]
  $f=[]
  $) f in u[1:]:
   if $F(f):
    outs.$%(nabs(f))
   $@ $4(f):
    outs.$%(abs_(f)or('$J',f))
   $@ $((f,'^')$* $/(f[2])is $s $* f[2]%2==0:
    outs.$%(f)
   $@ $((f,'^')$* f[1]=='e':
    outs.$%(f)
   $&:
    $f.$%(f)
  if outs:
   $! $I(outs+[fn('$J',$I($f))])
 if isneg(u):
  $! fn('$J',$l(u))
 if $((u,'^')$* u[1]=='e' $* isreal_expr(u[2]):
  $! u
 $! $#
$, sign_(u):
 if $F(u):
  $! $`(u)if $/(u)is $- $D $& $D($`(u))
 if u=='$P':
  $! 1
 if $4(u):
  v=cv(u)
  if v is $- $# $* $/(v)is $- $3:
   $! 1 if v>0 $&(-1 if v<0 $& 0)
 if $((u,'*')$* $F(u[1]):
  $! $<($`(u[1]),fn('sign',cmul(nabs(u[1]),$b(u)[1])))
 if $((u,'^')$* $/(u[2])is $s $* u[2]%2==0:
  $! $#
 $! $#
$, finite(v):
 $! v==v $* v!=$D('$P')$* v!=$D('-$P')
$, floor_(u):
 if $F(u):
  if $/(u)is $D:
   $! $D($Y.floor(u))if finite(u)$& $#
  $! nfloor(u)
 if $4(u)$* $- has(u,'i'):
  v=cv(u)
  if v is $- $# $* $/(v)is $- $3:
   $! $s($Y.floor(v))
 $! $#
$, ceil_(u):
 f=floor_($l(u))
 if f is $- $#:
  $! $l(f)
 $! $#
$, sinh_(u):
 if u==0:
  $! 0
 if isneg(u):
  $! $l(fn('sinh',$l(u)))
 if $((u,'arcsinh'):
  $! u[1]
 $! $#
''')
_x(r'''$, cosh_(u):
 if u==0:
  $! 1
 if isneg(u):
  $! fn('cosh',$l(u))
 if $((u,'arccosh'):
  $! u[1]
 $! $#
$, tanh_(u):
 if u==0:
  $! 0
 if isneg(u):
  $! $l(fn('tanh',$l(u)))
 $! $#
$, odd0($B):
 $, g(u):
  if u==0:
   $! 0
  if isneg(u):
   $! $l(fn($B,$l(u)))
  $! $#
 $! g
$, fact_(u):
 if $/(u)is $s:
  if u<0:
   $! '$H'
  if u>1000:
   $! $#
  r=1
  $) k in $+(2,u+1):
   r*=k
  $! r
 if isq(u)$* u[2]==2 $* u[1]>0:
  n=u[1]
  r=$<($N('pi'),Q(1,1))
  k=Q(1,2)
  $G ncmp(k,u)<=0:
   r=$<(r,k)
   k=nadd(k,1)
  $! r
 if $/(u)is $D:
  if u<0 $* u==$Y.floor(u):
   $! '$H'
  ${:
   $! gamma(u+1.0)
  $5($a,$E,$T):
   $! '$P' if u>0 $& '$H'
 $! $#
$, gamma(x):
 ${:
  $! $Y.gamma(x)
 $5 AttributeError:
  pass
 if x<0.5:
  $! $Y.pi/($Y.sin($Y.pi*x)*gamma(1.0-x))
 x-=1.0
 g=7
 c=(0.99999999999980993,676.5203681218851,-1259.1392167224028,
 771.32342877765313,-176.61502916214059,12.507343278686905,
 -0.13857109526572012,9.9843695780195716e-6,1.5056327351493116e-7)
 a=c[0]
 t=x+g+0.5
 $) k in $+(1,9):
  a+=c[k]/(x+k)
 h=t**((x+0.5)/2)
 $! $Y.$N(2*$Y.pi)*h*$Y.exp(-t)*h*a
$, real_(u):
 if $4(u)or has(u,'i'):
  r,i=reim(u)
  if $- $((r,'$R'):
   $! r
 if isreal_expr(u):
  $! u
 $! $#
$, imag_(u):
 if isreal_expr(u):
  $! 0
 r,i=reim(u)
 if $- $((i,'imag'):
  $! i
 $! $#
$, conj_(u):
 if isreal_expr(u):
  $! u
 r,i=reim(u)
 if $- $((r,'$R'):
  $! $](r,$<('i',i))
 $! $#
$, angle_(u):
 r,i=reim(u)
 if $((r,'$R')or $((i,'imag'):
  $! $#
 if i==0:
  if $4(r):
   v=cv(r)
   if v is $- $# $* $/(v)is $- $3:
    if v>=0:
     $! 0
    $! 'pi'
  $! $#
 if r==0:
  if $4(i):
   v=cv(i)
   if v is $- $# $* $/(v)is $- $3:
    $! $<(Q(1 if v>0 $&-1,2),'pi')
  $! $#
 if $4(r)$* $4(i):
  vr=cv(r)
  vi=cv(i)
  if vr is $# or vi is $# or $/(vr)is $3 or $/(vi)is $3:
   $! $#
  a=fn('$w',$U(i,r))
  if vr<0:
   if vi>=0:
    a=$^(a,'pi')
   $&:
    a=$](a,'pi')
  $! a
 $! $#
$q['sin']=sin_
$q['cos']=cos_
$q['tan']=tan_
$q['$|']=asin_
$q['arccos']=acos_
$q['$w']=atan_
$q['ln']=ln_
$q['log']=log_
$q['$J']=abs_
$q['sign']=sign_
$q['floor']=floor_
$q['ceiling']=ceil_
$q['sinh']=sinh_
$q['cosh']=cosh_
$q['tanh']=tanh_
$q['arcsinh']=odd0('arcsinh')
$q['arctanh']=odd0('arctanh')
$q['arccosh']=$: u:0 if u==1 $& $#
$q['fact']=fact_
$q['$R']=real_
$q['imag']=imag_
$q['conj']=conj_
$q['$r']=angle_
$q['exp']=$: u:pw('e',u)
$q['$N']=$: u:pw(u,$v)
$q['sec']=$: u:pw(fn('cos',u),-1)
$q['csc']=$: u:pw(fn('sin',u),-1)
$q['cot']=$: u:pw(fn('tan',u),-1)
$q['sech']=$: u:pw(fn('cosh',u),-1)
$q['csch']=$: u:pw(fn('sinh',u),-1)
$q['coth']=$: u:pw(fn('tanh',u),-1)
$q['arcsec']=$: u:fn('arccos',pw(u,-1))
$q['arccsc']=$: u:fn('$|',pw(u,-1))
$q['arccot']=$: u:$]($<($v,'pi'),fn('$w',u))
$q['arcsech']=$: u:fn('arccosh',pw(u,-1))
$q['arccsch']=$: u:fn('arcsinh',pw(u,-1))
$q['arccoth']=$: u:fn('arctanh',pw(u,-1))
$, root_(u,n=2):
 $! pw(u,pw(n,-1))
$q['root']=root_
import cmath
$, _c(f):
 $, g(x):
  ${:
   if $/(x)is $3:
    $! f[1](x)
   $! f[0](x)
  $5($T,TypeError):
   $! f[1]($3(x))
 $! g
$, _ln(x):
 if $/(x)is $- $3 $* x>0:
  $! $Y.log(x)
 if x==0:
  $! $D('-$P')
 $! cmath.log($3(x))
$, _asinr(x):
 if-1<=x<=1:
  $! $Y.asin(x)
 $k $T
$, _acosr(x):
 if-1<=x<=1:
  $! $Y.acos(x)
 $k $T
$, _casin(z):
 $!-1j*cmath.log(1j*z+cmath.$N(1-z*z))
$, _cacos(z):
 $! $Y.pi/2-_casin(z)
$, _catan(z):
 $! 0.5j*cmath.log((1-1j*z)/(1+1j*z))
$, _sinh(x):
 $!(cmath.exp(x)-cmath.exp(-x))/2 if $/(x)is $3 $&($Y.exp(x)-$Y.exp(-x))/2
$, _cosh(x):
 $!(cmath.exp(x)+cmath.exp(-x))/2 if $/(x)is $3 $&($Y.exp(x)+$Y.exp(-x))/2
$, _tanh(x):
 if $/(x)is $- $3:
  if x>20:
   $! 1.0
  if x<-20:
   $!-1.0
  a=$Y.exp(2*x)
  $!(a-1)/(a+1)
 a=cmath.exp(2*x)
 $!(a-1)/(a+1)
$, _asinh(x):
 if $/(x)is $- $3:
  $! $Y.log(x+$Y.$N(x*x+1))if x>=0 $&-$Y.log(-x+$Y.$N(x*x+1))
 $! cmath.log(x+cmath.$N(x*x+1))
$, _acosh(x):
 if $/(x)is $- $3 $* x>=1:
  $! $Y.log(x+$Y.$N(x*x-1))
 x=$3(x)
 $! cmath.log(x+cmath.$N(x+1)*cmath.$N(x-1))
$, _atanh(x):
 if $/(x)is $- $3 $*-1<x<1:
  $! 0.5*$Y.log((1+x)/(1-x))
 x=$3(x)
 $! 0.5*cmath.log((1+x)/(1-x))
$, _sign(x):
 if $/(x)is $3:
  $! x/$J(x)if x!=0 $& 0.0
 $! 1.0 if x>0 $&(-1.0 if x<0 $& 0.0)
$, _floor(x):
 if $/(x)is $3:
  $! $3($Y.floor(x.$R),$Y.floor(x.imag))
 $! $D($Y.floor(x))
$, _ceil(x):
 if $/(x)is $3:
  $! $3($Y.ceil(x.$R),$Y.ceil(x.imag))
 $! $D($Y.ceil(x))
$, _real(x):
 $! x.$R if $/(x)is $3 $& x
$, _imag(x):
 $! x.imag if $/(x)is $3 $& 0.0
$, _conj(x):
 $! x.conjugate()if $/(x)is $3 $& x
$, _angle(x):
 if $/(x)is $3:
  $! cmath.phase(x)
 $! 0.0 if x>=0 $& $Y.pi
$, _fact(x):
 if $/(x)is $3:
  $k $T
 $! gamma(x+1.0)
''')
_x(r'''NUMF={
 'sin':_c(($Y.sin,cmath.sin)),'cos':_c(($Y.cos,cmath.cos)),
 'tan':_c(($Y.tan,$: z:cmath.sin(z)/cmath.cos(z))),
 '$|':_c((_asinr,_casin)),'arccos':_c((_acosr,_cacos)),
 '$w':_c(($Y.atan,_catan)),
 'ln':_ln,'exp':_c(($Y.exp,cmath.exp)),
 '$N':_c(($: x:$Y.$N(x)if x>=0 $& cmath.$N(x),cmath.$N)),
 '$J':$J,'sign':_sign,'floor':_floor,'ceiling':_ceil,
 'sinh':_sinh,'cosh':_cosh,'tanh':_tanh,
 'arcsinh':_asinh,'arccosh':_acosh,'arctanh':_atanh,
 '$R':_real,'imag':_imag,'conj':_conj,'$r':_angle,
 'fact':_fact,
 }
$, nfun_call($B,$c):
 if $B=='log':
  b=$c[1]if $1($c)>1 $& 10.0
  $! _ln($c[0])/_ln(b)
 if $B=='root':
  n=$c[1]if $1($c)>1 $& 2.0
  $! npow($c[0],1.0/n)
 if $B=='round':
  d=$s($c[1])if $1($c)>1 $& 0
  $! round($c[0],d)
 if $B=='when':
  $! $c[1]if $c[0]$&($c[2]if $1($c)>2 $& $D('nan'))
 if $B=='max':
  $! max($c)
 if $B=='min':
  $! min($c)
 if $B=='mod':
  $! $c[0]-$c[1]*$Y.floor($c[0]/$c[1])if $c[1]!=0 $& $c[0]
 f=NUMF.get($B)
 if f is $#:
  if $B in('sec','csc','cot','sech','csch','coth'):
   base={'sec':'cos','csc':'sin','cot':'tan','sech':'cosh','csch':'sinh','coth':'tanh'}[$B]
   $! 1.0/NUMF[base]($c[0])
  if $B in('arcsec','arccsc','arccot','arcsech','arccsch','arccoth'):
   base={'arcsec':'arccos','arccsc':'$|','arccot':'$w','arcsech':'arccosh','arccsch':'arcsinh','arccoth':'arctanh'}[$B]
   $! NUMF[base](1.0/$c[0])
  if $B in('ipart','$s'):
   $! $D($s($c[0]))
  if $B=='fpart':
   $! $c[0]-$s($c[0])
  err("Cannot evaluate "+$B)
 $! f($c[0])
$, npow(a,b):
 if $/(a)is $- $3 $* $/(b)is $- $3:
  if a<0 $*(b!=b or b in($D('$P'),$D('-$P'))or b!=$Y.floor(b)):
   $! $3(a)**b
  if a==0 $* b<0:
   $k $E
  ${:
   $! a**b
  $5 $a:
   $! $D('$P')
 if a==0:
  $! 0.0
 $! $3(a)**b
NCONST={'pi':$Y.pi,'e':$Y.e,'i':1j,'$P':$D('$P')}
$, $X(e,env=$#):
 t=$/(e)
 if t is $s:
  ${:
   $! $D(e)
  $5 $a:
   $! '$P' if e>0 $&('*',-1,'$P')
 if t is $D:
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
  $) a in e[1:]:
   s=s+$X(a,env)
  $! s
 if h=='*':
  s=1.0
  $) a in e[1:]:
   s=s*$X(a,env)
  $! s
 if h=='^':
  b=e[1]
  x=e[2]
  if isq(x)$* x[2]%2==1:
   bv=$X(b,env)
   if $/(bv)is $- $3 $* bv<0:
    r=(-bv)**(x[1]/x[2])
    $!-r if x[1]%2 $& r
   $! npow(bv,x[1]/x[2])
  if $/(x)is $s:
   bv=$X(b,env)
   if bv==0 $* x<0:
    $k $E
   $! bv**x
  $! npow($X(b,env),$X(x,env))
 if h in('$K','mat','$p','Q'):
  err("Not numeric")
 if h=='when':
  c=nbool(e[1],env)
  if c:
   $! $X(e[2],env)
  $! $X(e[3],env)if $1(e)>3 $& $D('nan')
 $c=[$X(a,env)$) a in e[1:]]
 $! nfun_call(h,$c)
$, nbool(c,env):
 h=head(c)
 if h in('<','>','<=','>=','=','/='):
  a=$X(c[1],env)
  b=$X(c[2],env)
  if $/(a)is $3:
   a=a.$R
  if $/(b)is $3:
   b=b.$R
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
  $) a in c[1:]:
   if $- nbool(a,env):
    $! $2
  $! $A
 if h=='or':
  $) a in c[1:]:
   if nbool(a,env):
    $! $A
  $! $2
 if h=='$-':
  $! $- nbool(c[1],env)
 if c=='true':
  $! $A
 if c=='false':
  $! $2
 err("Not a condition")
$, nreal(e,env=$#):
 v=$X(e,env)
 if $/(v)is $3:
  if $J(v.imag)>1e-9*(1+$J(v.$R)):
   $k $T
  $! v.$R
 $! v
$, simp(e):
 t=$/(e)
 if t is $- $0:
  $! e
 h=e[0]
 if h=='Q' or h=='$p' or h=='hold':
  if h=='hold':
   $! simp(e[1])
  $! e
 $M=[simp(a)$) a in e[1:]]
 if h=='+':
  $! $=($M)
 if h=='*':
  $! $I($M)
 if h=='^':
  $! pw($M[0],$M[1])
 if h in('$K','mat','=','<','>','<=','>=','/=','$*','or','$-'):
  $!(h,)+$0($M)
 $! fn(h,$M)
$, $W(e,old,new):
 if e==old:
  $! new
 t=$/(e)
 if t is $- $0 or e[0]=='Q' or e[0]=='$p':
  $! e
 ch=$2
 $M=[]
 $) a in e[1:]:
  b=$W(a,old,new)
  if b is $- a:
   ch=$A
  $M.$%(b)
 if $- ch:
  $! e
 $! simp((e[0],)+$0($M))
$, subsd(e,d):
 t=$/(e)
 if t is $p:
  if e in d:
   $! d[e]
  $! e
 if t is $- $0 or e[0]=='Q' or e[0]=='$p':
  $! e
 ch=$2
 $M=[]
 $) a in e[1:]:
  b=subsd(a,d)
  if b is $- a:
   ch=$A
  $M.$%(b)
 if $- ch:
  $! e
 $! simp((e[0],)+$0($M))
$, mapexpr(f,e):
 if $((e,'$K'):
  $!('$K',)+$0(mapexpr(f,a)$) a in e[1:])
 if $((e,'mat'):
  $!('mat',)+$0(mapexpr(f,a)$) a in e[1:])
 $! f(e)
$, $?(e):
 t=$/(e)
 if t is $- $0:
  $! e
 h=e[0]
 if h=='Q' or h=='$p':
  $! e
 if h=='+':
  $! $=([$?(a)$) a in e[1:]])
 if h=='*':
  r=1
  $) f in e[1:]:
   r=expand_mul(r,$?(f))
  $! r
 if h=='^':
  b=$?(e[1])
  x=$?(e[2])
  if $((b,'+')$* $/(x)is $s:
   if x>0:
    $! expand_pow(b,x)
   if x<0:
    $! pw(expand_pow(b,-x),-1)
  if $((b,'*')$* $/(x)is $s:
   $! $?($I([pw(f,x)$) f in b[1:]]))
  if b=='e' $* $((x,'+'):
   $! $I([pw('e',a)$) a in x[1:]])
  if $((x,'+')$* $F(b):
   $! $I([pw(b,a)$) a in x[1:]])
  $! pw(b,x)
 if h in('$K','mat','=','<','>','<=','>=','/=','$*','or','$-'):
  $!(h,)+$0($?(a)$) a in e[1:])
 $! fn(h,[$?(a)$) a in e[1:]])
''')
_x(r'''$, evalf(e):
 t=$/(e)
 if t is $s:
  $! $D(e)
 if t is $D:
  $! e
 if t is $p:
  if e=='pi':
   $! $Y.pi
  if e=='e':
   $! $Y.e
  $! e
 h=e[0]
 if h=='Q':
  $! e[1]/e[2]
 if h=='$p':
  $! e
 if $4(e)$* h $- in('$K','mat','=','<','>','<=','>=','/=','$*','or','$-'):
  ${:
   v=$X(e)
   if $/(v)is $3:
    $! fromcomplex(v)
   if v!=v:
    $! '$H'
   if v==$D('$P'):
    $! '$P'
   if v==$D('-$P'):
    $!('*',-1,'$P')
   $! v
  $5($E,$T,$a,TypeError):
   pass
  $5 $S:
   pass
 $M=[evalf(a)$) a in e[1:]]
 if h=='^' $* $/(e[2])is $s:
  $M[1]=e[2]
 $! simp((h,)+$0($M))
$, exactify(e,tol=$#):
 t=$/(e)
 if t is $D:
  $! float2rat(e,tol)
 if t is $0 $* e[0]!='Q' $* e[0]!='$p':
  $! simp((e[0],)+$0(exactify(a,tol)$) a in e[1:]))
 $! e
$, float2rat(x,tol=$#):
 if x!=x:
  $! '$H'
 if x==$D('$P'):
  $! '$P'
 if x==$D('-$P'):
  $!('*',-1,'$P')
 if x==$Y.floor(x)$* $J(x)<1e18:
  $! $s(x)
 if tol is $#:
  tol=5e-14*max(1.0,$J(x))
 h0,h1=0,1
 k0,k1=1,0
 y=x
 $) _ in $+(60):
  a=$Y.floor(y)
  h0,h1=h1,$s(a)*h1+h0
  k0,k1=k1,$s(a)*k1+k0
  if $J(h1/k1-x)<=tol:
   $O
  f=y-a
  if f==0:
   $O
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
  $) a in e[1:]:
   k=degree(a,x)
   if k is $#:
    $! $#
   if k>d:
    d=k
  $! d
 if h=='*':
  d=0
  $) a in e[1:]:
   k=degree(a,x)
   if k is $#:
    $! $#
   d+=k
  $! d
 if h=='^' $* $/(e[2])is $s $* e[2]>0:
  k=degree(e[1],x)
  if k is $#:
   $! $#
  $! k*e[2]
 $! $#
$, $Z(e,x):
 e=$?(e)
 if $8(e,x):
  $![e]
 $Q=e[1:]if $((e,'+')$&(e,)
 cs={}
 mx=0
 $) t in $Q:
  if $((t,'*'):
   k=0
   $f=[]
   $) f in t[1:]:
    if f==x:
     k+=1
    $@ $((f,'^')$* f[1]==x $* $/(f[2])is $s $* f[2]>0:
     k+=f[2]
    $@ $8(f,x):
     $f.$%(f)
    $&:
     $! $#
   c=$I($f)
  $@ t==x:
   k=1
   c=1
  $@ $((t,'^')$* t[1]==x $* $/(t[2])is $s $* t[2]>0:
   k=t[2]
   c=1
  $@ $8(t,x):
   k=0
   c=t
  $&:
   $! $#
  cs[k]=$^(cs.get(k,0),c)
  if k>mx:
   mx=k
 $![cs.get(k,0)$) k in $+(mx+1)]
$, fromcoeffs(cs,x):
 $! $=([$<(cs[k],pw(x,k))$) k in $+($1(cs))])
$, numer_denom(e):
 if $((e,'*'):
  nu=[]
  de=[]
  $) f in e[1:]:
   if isq(f):
    nu.$%(f[1])
    de.$%(f[2])
   $@ $((f,'^')$* $F(f[2])$* $`(f[2])<0:
    de.$%(pw(f[1],nneg(f[2])))
   $&:
    nu.$%(f)
  $! $I(nu),$I(de)
 if isq(e):
  $! e[1],e[2]
 if $((e,'^')$* $F(e[2])$* $`(e[2])<0:
  $! 1,pw(e[1],nneg(e[2]))
 $! e,1
''')
_x(r'''OPT={'uni':$A,'digits':10}
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
  $! '$H'
 if x==$D('$P'):
  $! USYM['$P']if OPT['uni']$& '$P'
 if x==$D('-$P'):
  $! '-'+(USYM['$P']if OPT['uni']$& '$P')
 if x==0:
  $! '0.'
 d=OPT['digits']
 s=('%.'+$p(d)+'g')%x
 m=s
 ex=''
 if 'e' in s:
  m,ex=s.split('e')
  ex=$s(ex)
  ex='E'+$p(ex)
 if '.' in m:
  m=m.rstrip('0')
 $&:
  m=m+'.'
 $! m+ex
$, fnum(x):
 t=$/(x)
 if t is $s:
  $! $p(x),(P_ATOM if x>=0 $& P_NEG)
 if t is $D:
  s=ffloat(x)
  $! s,(P_ATOM if $- s.$y('-')$& P_NEG)
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
 t=$/(e)
 if t is $s or t is $D:
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
  $! pr(e[1],$A)
 keep=$2
 if h=='$K':
  $! '{'+','.join([pr(a,keep)[0]$) a in e[1:]])+'}',P_ATOM
 if h=='mat' $* $1(e)==2:
  $! '['+','.join([pr(a,keep)[0]$) a in e[1][1:]])+']',P_ATOM
 if h=='mat':
  $[=[]
  $) r in e[1:]:
   $[.$%('['+','.join([pr(a,keep)[0]$) a in r[1:]])+']')
  $! '['+''.join($[)+']',P_ATOM
 if h=='$p':
  $! '"'+e[1]+'"',P_ATOM
 if h in REL:
  op=REL[h]if OPT['uni']$& h
  a=pr(e[1],keep)
  b=pr(e[2],keep)
  $! paren(a[0],a[1],P_SUM)+op+paren(b[0],b[1],P_SUM),P_REL
 if h=='$*' $* $1(e)==3 $* head(e[1])in('<','<=')$* head(e[2])in('<','<=')$* e[1][2]==e[2][1]:
  op1=REL[e[1][0]]if OPT['uni']$& e[1][0]
  op2=REL[e[2][0]]if OPT['uni']$& e[2][0]
  $! pr(e[1][1],$2)[0]+op1+pr(e[1][2],$2)[0]+op2+pr(e[2][2],$2)[0],P_REL
 if h=='$*' or h=='or':
  p=P_AND if h=='$*' $& P_OR
  ss=[]
  $) a in e[1:]:
   s,q=pr(a,keep)
   ss.$%(paren(s,q,p+1))
  $!(' '+h+' ').join(ss),p
 if h=='$-':
  s,q=pr(e[1],keep)
  $! '$- '+paren(s,q,P_NOT+1),P_NOT
 if h=='$J':
  $! '|'+pr(e[1],keep)[0]+'|',P_ATOM
 if h=='fact':
  s,q=pr(e[1],keep)
  $! paren(s,q,P_ATOM)+'!',P_POST
 if h=='log':
  if $1(e)==2 or e[2]==10:
   $! 'log10('+pr(e[1],keep)[0]+')',P_ATOM
  $! 'log('+pr(e[1],keep)[0]+','+pr(e[2],keep)[0]+')',P_ATOM
 if h=='call':
  $! e[1]+'('+','.join([pr(a,keep)[0]$) a in e[2:]])+')',P_ATOM
 if h=='prime':
  $! e[1]+"'"*e[2],P_ATOM
 if h=='$L':
  nm='\u222b' if OPT['uni']$& '$L'
  $! nm+'('+','.join([pr(a,keep)[0]$) a in e[1:]])+')',P_ATOM
 if h=='sumseq':
  nm='\u03a3' if OPT['uni']$& 'sumseq'
  $! nm+'('+','.join([pr(a,keep)[0]$) a in e[1:]])+')',P_ATOM
 if h=='prodseq':
  nm='\u03a0' if OPT['uni']$& 'prodseq'
  $! nm+'('+','.join([pr(a,keep)[0]$) a in e[1:]])+')',P_ATOM
 if h=='$N' or h=='root':
  pass
 h=TINAME.get(h,h)
 $! h+'('+','.join([pr(a,keep)[0]$) a in e[1:]])+')',P_ATOM
TINAME={'ncr':'nCr','npr':'nPr'}
MAINV='xyzt'
$, varprio(v):
 i=MAINV.find(v)if $1(v)==1 $&-1
 if i<0:
  $!(100,v)
 $!(i,v)
$, facprio(v):
 i=MAINV.find(v)if $1(v)==1 $&-1
 if i<0:
  $!(0,v)
 $!(1,$p(i))
$, termdegs(t,d):
 c,r=$b(t)
 fs=r[1:]if $((r,'*')$&(r,)
 $) f in fs:
  if $/(f)is $p $* f $- in SPECIAL:
   d[f]=d.get(f,0)+1
  $@ $((f,'^')$* $/(f[1])is $p $* f[1]$- in SPECIAL $* $F(f[2]):
   d[f[1]]=d.get(f[1],0)+tofl(f[2])
  $@ $((f,'^')$* $F(f[2]):
   $) v in $g(f[1]):
    d[v]=d.get(v,0)+tofl(f[2])*0.001
  $@ $- $F(f)$* $/(f)is $- $p:
   $) v in $g(f):
    d[v]=d.get(v,0)+0.0001
$, sumkeys($Q):
 vs=[]
 degs=[]
 $) t in $Q:
  d={}
  termdegs(t,d)
  degs.$%(d)
  $) v in d:
   if v $- in vs:
    vs.$%(v)
 vs.sort(key=varprio)
 mv=[v $) v in vs if varprio(v)[0]<100]
 ov=[v $) v in vs if varprio(v)[0]>=100]
 keys=[]
 $) k in $+($1($Q)):
  t=$Q[k]
  d=degs[k]
  if $F(t):
   keys.$%((2,(),0,0,(),''))
  $@ $- d:
   cat=3 if has(t,'i')$& 1
   keys.$%((cat,(),0,1 if isneg(t)$& 0,(),okey($b(t)[1])))
  $&:
   keys.$%((0,$0([-d.get(v,0)$) v in mv]),-sum([d.get(v,0)$) v in ov]),
 1 if isneg(t)$& 0,$0([-d.get(v,0)$) v in ov]),okey($b(t)[1])))
 $! keys
$, pr_sum(e,keep):
 $Q=$K(e[1:])
 if $- keep:
  ks=sumkeys($Q)
  idx=$K($+($1($Q)))
  idx.sort(key=$: i:ks[i])
  $Q=[$Q[i]$) i in idx]
 $9=''
 first=$A
 $) t in $Q:
  s,p=pr(t,$2)
  if p<P_SUM+1 $* $- s.$y('-')$* p<=P_SUM:
   s='('+s+')'
  if first:
   $9=s
   first=$2
  $@ s.$y('-'):
   $9+=s
  $&:
   $9+='+'+s
 $! $9,P_SUM
$, fackey(f):
 if f=='pi' or f=='e' or isrrad(f)or $F(f):
  $!(0,(0,''),okey(f))
 if f=='i':
  $!(3,(0,''),'')
 if $/(f)is $p:
  $!(1,facprio(f),'')
 if $((f,'^')$* $/(f[1])is $p:
  if f[1]=='e':
   $!(2,(0,''),okey(f))
  $!(1,facprio(f[1]),okey(f))
 if $((f,'+')or($((f,'^')$* $((f[1],'+')):
  $!(4,(0,''),okey(f))
 $!(2,(0,''),okey(f))
$, pr_factor(f,keep,first):
 s,p=pr(f,keep)
 if p<P_PROD or(p==P_PROD $* $- first)or(s.$y('-')$* $- first):
  $! '('+s+')'
 $! s
''')
_x(r'''$, pr_prod(e,keep):
 fs=$K(e[1:])
 coef=1
 if fs $* $F(fs[0])$* $- keep:
  coef=fs[0]
  fs=fs[1:]
 num=[]
 den=[]
 $) f in fs:
  if $((f,'^')$* $F(f[2])$* $`(f[2])<0:
   ex=nneg(f[2])
   den.$%(f[1]if ex==1 $&('^',f[1],ex))
  $@ isq(f)$* keep:
   num.$%(f[1])
   den.$%(f[2])
  $&:
   num.$%(f)
 if $- keep:
  num.sort(key=fackey)
  den.sort(key=fackey)
 sign=''
 if keep $* num $* $F(num[0])$* $`(num[0])<0:
  sign='-'
  if num[0]==-1:
   num=num[1:]
  $&:
   num[0]=nneg(num[0])
 cn=coef
 cd=1
 if $F(coef):
  if $`(coef)<0:
   sign='-'
   coef=nneg(coef)
  if isq(coef):
   cn=coef[1]
   cd=coef[2]
  $&:
   cn=coef
 if keep:
  num=[f $) f in num if f!=1]or[1]
 if sign $* den $* $- keep:
  sums=[k $) k in $+($1(num))if $((num[k],'+')]
  dsums=[k $) k in $+($1(den))if $((den[k],'+')]
  if $1(sums)==1 $* any([isneg(t)$) t in num[sums[0]][1:]]):
   num=$K(num)
   num[sums[0]]=$<(-1,num[sums[0]])
   sign=''
  $@ $1(dsums)==1 $* $- sums $* $1(den[dsums[0]])==3 $* $4(den[dsums[0]])$* any([isneg(t)$) t in den[dsums[0]][1:]]):
   den=$K(den)
   den[dsums[0]]=$<(-1,den[dsums[0]])
   sign=''
 $~=[]
 if cn!=1 or $/(cn)is $D:
  $~.$%(fnum(cn)[0])
 $) f in num:
  $~.$%(pr_factor(f,$2,$- $~))
 if $- $~:
  $~.$%('1')
 ns='*'.join($~)
 if cd!=1:
  den.insert(0,cd)
 if $- den:
  if sign $* $1(num)==1 $* cn==1 $* pr(num[0],$2)[1]<=P_SUM:
   $! sign+'('+pr(num[0],$2)[0]+')',P_NEG
  $! sign+ns,(P_NEG if sign $& P_PROD)
 if $1($~)==1 $* $1(num)==1 $* cn==1:
  s,p=pr(num[0],$2)
  ns=paren(s,p,P_PROD+1)if p<P_PROD $& s
  if s.$y('-'):
   ns='('+s+')'
 dparts=[]
 $) f in den:
  dparts.$%(pr_factor(f,$2,$- dparts))
 ds='*'.join(dparts)
 if $1(den)>1:
  ds='('+ds+')'
 $&:
  s,p=pr(den[0],$2)
  if p<=P_PROD or s.$y('-'):
   ds='('+s+')'
 $! sign+ns+'/'+ds,(P_NEG if sign $& P_PROD)
$, pr_pow(e,keep):
 b=e[1]
 x=e[2]
 if $F(x)$* $`(x)<0 $* $- keep:
  ex=nneg(x)
  d=b if ex==1 $&('^',b,ex)
  s,p=pr(d,$2)
  if p<=P_PROD or s.$y('-'):
   s='('+s+')'
  $! '1/'+s,P_PROD
 if x==$v:
  s,p=pr(b,$2)
  if OPT['uni']:
   if($/(b)is $s $* b>=0)or($/(b)is $p):
    $! '\u221a'+s,P_POW
   $! '\u221a('+s+')',P_ATOM
  $! '$N('+s+')',P_ATOM
 bs,bp=pr(b,$2)
 if bp<=P_POW or bs.$y('-')or $((b,'fact'):
  bs='('+bs+')'
 xs,xp=pr(x,$2)
 if $-(($/(x)is $s $* x>=0)or($/(x)is $p)):
  xs='('+xs+')'
 $! bs+'^'+xs,P_POW
$, fmt_top(e):
 if $((e,'mat')$* $1(e)>2:
  $[=[]
  $) r in e[1:]:
   $[.$%('['+','.join([fmt(a)$) a in r[1:]])+']')
  if sum([$1(r)$) r in $[])>28:
   $! '['+('\n '.join($[))+']'
  $! '['+''.join($[)+']'
 if $((e,'$p'):
  $! e[1]
 $! fmt(e)
''')
_x(r'''REPL=(
 ('**','^'),('==','='),('!=','/='),
 ('sin\u207b\u00b9','$|'),('cos\u207b\u00b9','arccos'),('tan\u207b\u00b9','$w'),
 ('\u2212','-'),('\u2013','-'),('\u00d7','*'),('\u00b7','*'),
 ('\u2022','*'),('\u22c5','*'),('\u00f7','/'),('\u2264','<='),
 ('\u2265','>='),('\u2260','/='),('\u2192','->'),('\u21d2','=>'),
 ('\u21d4','<=>'),('\u207b\u00b9','^(-1)'),('\u00b2','^2'),
 ('\u00b3','^3'),('\u03c0',' pi '),('\u221e',' $P '),
 ('\u212f',' e '),('\u2148',' i '),('\u03b8','theta'),
 ('\u222b',' $L'),('\u03a3',' sumseq'),('\u2211',' sumseq'),
 ('\u03a0',' prodseq'),('\u220f',' prodseq'),('\u1d07','E'),
 ('\u2032',"'"),('\u2033',"''"),('@i',' i '),('@e',' e '),
 ('@>','\u25ba'),('@d','\u00b0'),('@t','\u1d40'),('\u2044','/'),
 ('infinity','$P'),('\u03b1','alpha'),('\u03b2','beta'),
 ('\u03bb','$:'),('\u03bc','mu'),('\u03c3','sigma'),
 ('\u0394','delta'),
 )
OPS=('<=>','=>','->','=:',':=','<=','>=','/=','<>','.^','.*',
 './','.+','.-','>>','+','-','*','/','^','(',')','{','}',
 '[',']',',',';','=','<','>','|','!','%','&','\u00b0',
 '\u2220','\u25ba','\u221a',"'",'\u1d40')
KEYW=('$*','or','xor','$-','nor','nand')
NOTLETTER='\u221a\u00b0\u2220\u25ba\u1d40'
$, normalize(s):
 $) a,b in REPL:
  if a in s:
   s=s.replace(a,b)
 $! s
$, isletter(c):
 if c=='_':
  $! $A
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
 n=$1(s)
 $G i<n:
  c=s[i]
  if c==' ' or c=='\t':
   i+=1
   $6
  if c=='0' $* i+2<n $* s[i+1]in 'bBhH':
   base=2 if s[i+1]in 'bB' $& 16
   j=i+2
   dg='01' if base==2 $& '0123456789abcdefABCDEF'
   $G j<n $* s[j]in dg:
    j+=1
   if j>i+2:
    toks.$%(('num',$s(s[i+2:j],base)))
    i=j
    $6
  if isdig(c)or(c=='.' $* i+1<n $* isdig(s[i+1])):
   j=i
   $G j<n $* isdig(s[j]):
    j+=1
   isf=$2
   if j<n $* s[j]=='.' $* $-(j+1<n $* s[j+1]in '^*/+-' $* $- isdig(s[j+1])):
    isf=$A
    j+=1
    $G j<n $* isdig(s[j]):
     j+=1
   if j<n $*(s[j]=='E' or(s[j]=='e' $* j+1<n $* isdig(s[j+1]))):
    k=j+1
    if k<n $* s[k]in '+-':
     k+=1
    if k<n $* isdig(s[k]):
     isf=$A
     j=k
     $G j<n $* isdig(s[j]):
      j+=1
   txt=s[i:j]
   if isf:
    toks.$%(('num',$D(txt)))
   $&:
    toks.$%(('num',$s(txt)))
   i=j
   $6
  if isletter(c):
   j=i
   $G j<n $*(isletter(s[j])or isdig(s[j])):
    j+=1
   $B=s[i:j].lower()
   toks.$%(('id',$B))
   i=j
   k=0
   $G i<n $* s[i]=="'":
    k+=1
    i+=1
   if k:
    toks.$%(('prime',k))
   $6
  if c=='"':
   j=s.find('"',i+1)
   if j<0:
    $k $S('Missing "')
   toks.$%(('$p',s[i+1:j]))
   i=j+1
   $6
  $) op in OPS:
   if s.$y(op,i):
    i+=$1(op)
    if op=='<>':
     op='/='
    if op=='>>':
     op='\u25ba'
    toks.$%(('op',op))
    $O
  $&:
   $k $S('Invalid character: '+c)
 toks.$%(('end',$#))
 $! toks
''')
_x(r'''class Parser:
 $, __init__($>,toks,isfunc):
  $>.t=toks
  $>.i=0
  $>.isfunc=isfunc
 $, peek($>):
  $! $>.t[$>.i]
 $, nxt($>):
  tk=$>.t[$>.i]
  $>.i+=1
  $! tk
 $, isop($>,op):
  tk=$>.t[$>.i]
  $! tk[0]=='op' $* tk[1]==op
 $, isid($>,$B):
  tk=$>.t[$>.i]
  $! tk[0]=='id' $* tk[1]==$B
 $, expect($>,op):
  if $- $>.isop(op):
   tk=$>.peek()
   $k $S('Missing '+op)
  $>.i+=1
 $, top($>):
  e=$>.store()
  $G $>.isop('\u25ba'):
   $>.nxt()
   tk=$>.nxt()
   if tk[0]!='id':
    $k $S('Syntax error after conversion')
   $M=[]
   if $>.isop('('):
    $>.nxt()
    $M=$>.$M(')')
   e=('conv',e,tk[1])+$0($M)
  if $>.peek()[0]!='end':
   tk=$>.peek()
   $k $S('Syntax error near '+$p(tk[1])if tk[1]is $- $# $& 'Syntax error')
  $! e
 $, store($>):
  if $>.isid('define'):
   $>.nxt()
   lhs=$>.sum()
   if $- $>.isop('='):
    $k $S('Define needs =')
   $>.nxt()
   rhs=$>.wth()
   $!('define',lhs,rhs)
  e=$>.wth()
  if $>.isop('->')or $>.isop('=:'):
   $>.nxt()
   tgt=$>.wth()
   $!('store',e,tgt)
  if $>.isop(':='):
   $>.nxt()
   rhs=$>.wth()
   $!('define',e,rhs)
  $! e
 $, wth($>):
  e=$>.iff()
  $G $>.isop('|'):
   $>.nxt()
   c=$>.iff()
   e=('|',e,c)
  $! e
 $, iff($>):
  e=$>.imp()
  $G $>.isop('<=>'):
   $>.nxt()
   e=('<=>',e,$>.imp())
  $! e
 $, imp($>):
  e=$>.xor()
  $G $>.isop('=>'):
   $>.nxt()
   e=('=>',e,$>.xor())
  $! e
 $, xor($>):
  e=$>.lor()
  $G $>.isid('xor')or $>.isid('nor')or $>.isid('nand'):
   op=$>.nxt()[1]
   e=(op,e,$>.lor())
  $! e
 $, lor($>):
  e=$>.land()
  $G $>.isid('or'):
   $>.nxt()
   e=('or',e,$>.land())
  $! e
 $, land($>):
  e=$>.lnot()
  $G $>.isid('$*'):
   $>.nxt()
   e=('$*',e,$>.lnot())
  $! e
 $, lnot($>):
  if $>.isid('$-'):
   $>.nxt()
   $!('$-',$>.lnot())
  $! $>.rel()
 $, rel($>):
  a=$>.sum()
  tk=$>.peek()
  if tk[0]=='op' $* tk[1]in('=','/=','<','>','<=','>='):
   $>.nxt()
   b=$>.sum()
   r=(tk[1],a,b)
   tk2=$>.peek()
   if tk2[0]=='op' $* tk2[1]in('<','>','<=','>='):
    $>.nxt()
    c=$>.sum()
    r=('$*',r,(tk2[1],b,c))
   $! r
  $! a
 $, sum($>):
  a=$>.prod()
  $G $A:
   tk=$>.peek()
   if tk[0]=='op' $* tk[1]in('+','-','.+','.-','&'):
    $>.nxt()
    b=$>.prod()
    op=tk[1]
    if op=='.+':
     op='+'
    $@ op=='.-':
     op='-'
    a=(op,a,b)
   $&:
    $! a
 $, startsprimary($>):
  tk=$>.peek()
  if tk[0]=='num' or tk[0]=='$p':
   $! $A
  if tk[0]=='id':
   $! tk[1]$- in KEYW
  if tk[0]=='op':
   $! tk[1]in('(','{','\u221a')
  $! $2
 $, prod($>):
  a=$>.unary()
  $G $A:
   tk=$>.peek()
   if tk[0]=='op' $* tk[1]in('*','/','.*','./'):
    $>.nxt()
    b=$>.unary()
    op=tk[1]
    a=(op,a,b)
   $@ $>.startsprimary():
    b=$>.pw()
    a=('*',a,b)
   $&:
    $! a
 $, unary($>):
  if $>.isop('-'):
   $>.nxt()
   $!('$l',$>.unary())
  if $>.isop('+'):
   $>.nxt()
   $! $>.unary()
  $! $>.pw()
 $, pw($>):
  b=$>.post()
  if $>.isop('^')or $>.isop('.^'):
   op=$>.nxt()[1]
   if $>.isop('\u1d40')or $>.isid('t')$* $2:
    pass
   x=$>.unary()
   $!('^' if op=='^' $& '.^',b,x)
  $! b
 $, post($>):
  a=$>.primary()
  $G $A:
   if $>.isop('!'):
    $>.nxt()
    a=('!',a)
   $@ $>.isop('%'):
    $>.nxt()
    a=('%',a)
   $@ $>.isop('\u00b0'):
    $>.nxt()
    a=('deg',a)
   $@ $>.isop('\u1d40'):
    $>.nxt()
    a=('call','transpose',a)
   $@ $>.isop('['):
    $>.nxt()
    idx=$>.$M(']')
    a=('index',a)+$0(idx)
   $&:
    $! a
 $, $M($>,close):
  $9=[]
  if $>.isop(close):
   $>.nxt()
   $! $9
  $G $A:
   $9.$%($>.store_in())
   if $>.isop(','):
    $>.nxt()
    $6
   $>.expect(close)
   $! $9
 $, store_in($>):
  e=$>.wth()
  $! e
 $, primary($>):
  tk=$>.nxt()
  k=tk[0]
  if k=='num':
   $! tk[1]
  if k=='$p':
   $!('$p',tk[1])
  if k=='id':
   $B=tk[1]
   if $B in KEYW:
    $k $S('Syntax error: '+$B)
   if $>.peek()[0]=='prime':
    n=$>.nxt()[1]
    if $>.isop('('):
     $>.nxt()
     a=$>.$M(')')
     $!('primecall',$B,n)+$0(a)
    $!('prime',$B,n)
   if $>.isop('(')$*($>.isfunc($B)or($1($B)>1 $* $B $- in('pi','$P','$H','theta'))):
    $>.nxt()
    a=$>.$M(')')
    $!('call',$B)+$0(a)
   $! $B
  if k=='op':
   op=tk[1]
   if op=='(':
    e=$>.store_in()
    if $>.isop('\u2220'):
     $>.nxt()
     th=$>.store_in()
     $>.expect(')')
     $!('polar',e,th)
    $>.expect(')')
    $! e
   if op=='{':
    $!('$K',)+$0($>.$M('}'))
   if op=='[':
    $! $>.matrix()
   if op=='\u221a':
    $!('call','$N',$>.post())
   if op=='-':
    $!('$l',$>.pw())
  if k=='end':
   $k $S('Incomplete expression')
  $k $S('Syntax error near '+$p(tk[1]))
 $, matrix($>):
  $[=[]
  if $>.isop('['):
   $G $>.isop('['):
    $>.nxt()
    $[.$%(('$K',)+$0($>.$M(']')))
    if $>.isop(','):
     $>.nxt()
   $>.expect(']')
  $&:
   row=[]
   $G $A:
    if $>.isop(']'):
     $>.nxt()
     $O
    row.$%($>.store_in())
    if $>.isop(','):
     $>.nxt()
    $@ $>.isop(';'):
     $>.nxt()
     $[.$%(('$K',)+$0(row))
     row=[]
    $@ $>.isop(']'):
     $6
    $&:
     $k $S('Missing ]')
   $[.$%(('$K',)+$0(row))
  n=$1($[[0])
  $) r in $[:
   if $1(r)!=n:
    $k $S('Dimension error')
  $!('mat',)+$0($[)
''')
_x(r'''$, parse(s,isfunc):
 toks=tokenize(s)
 if toks[0][0]=='end':
  $k $S('Empty input')
 $! Parser(toks,isfunc).top()
''')
_x(r'''import cmath
$, p_const(c,nv):
 if c==0:
  $!{}
 $!{(0,)*nv:c}
$, p_add(A,B):
 C=dict(A)
 $) m in B:
  v=C.get(m,0)+B[m]
  if v:
   C[m]=v
  $@ m in C:
   del C[m]
 $! C
$, p_neg(A):
 $! dict([(m,-A[m])$) m in A])
$, p_sub(A,B):
 $! p_add(A,p_neg(B))
$, madd(a,b):
 $! $0([a[i]+b[i]$) i in $+($1(a))])
$, p_mul(A,B):
 C={}
 $) a in A:
  ca=A[a]
  $) b in B:
   m=madd(a,b)
   v=C.get(m,0)+ca*B[b]
   if v:
    C[m]=v
   $@ m in C:
    del C[m]
 $! C
$, p_scale(A,c):
 if c==0:
  $!{}
 $! dict([(m,A[m]*c)$) m in A])
$, p_pow(A,n):
 nv=$1(next(iter(A)))if A $& 0
 R=p_const(1,nv)
 $G n>0:
  if n&1:
   R=p_mul(R,A)
  n>>=1
  if n:
   A=p_mul(A,A)
 $! R
$, p_deg(A,k):
 d=-1
 $) m in A:
  if m[k]>d:
   d=m[k]
 $! d
$, p_tdeg(A):
 d=-1
 $) m in A:
  s=sum(m)
  if s>d:
   d=s
 $! d
$, setk(m,k,v):
 $! m[:k]+(v,)+m[k+1:]
$, p_coeff(A,k,d):
 $! dict([(setk(m,k,0),A[m])$) m in A if m[k]==d])
$, p_lc(A,k):
 $! p_coeff(A,k,p_deg(A,k))
$, p_isconst(A):
 if $- A:
  $! $A
 $) m in A:
  if sum(m):
   $! $2
 $! $A
$, p_cval(A):
 $) m in A:
  $! A[m]
 $! 0
$, p_vars(A,nv):
 $![k $) k in $+(nv)if p_deg(A,k)>0]
$, p_mono(nv,k,d):
 m=[0]*nv
 m[k]=d
 $! $0(m)
$, $V(A,B):
 if $- B:
  err("Division by zero")
 lmB=max(B)
 lcB=B[lmB]
 nv=$1(lmB)
 Qt={}
 R=dict(A)
 cnt=0
 $G R:
  cnt+=1
  if cnt>5000:
   $! $#
  lmR=max(R)
  d=[]
  $) i in $+(nv):
   x=lmR[i]-lmB[i]
   if x<0:
    $! $#
   d.$%(x)
  c=R[lmR]
  if c%lcB:
   $! $#
  q=c//lcB
  d=$0(d)
  Qt[d]=Qt.get(d,0)+q
  $) m in B:
   mm=madd(m,d)
   v=R.get(mm,0)-q*B[m]
   if v:
    R[mm]=v
   $@ mm in R:
    del R[mm]
 $! Qt
$, p_icont(A):
 g=0
 $) m in A:
  g=igcd(g,A[m])
  if g==1:
   $O
 $! g
$, p_normsign(A):
 if A $* A[max(A)]<0:
  $! p_neg(A)
 $! A
$, p_diff(A,k):
 C={}
 $) m in A:
  if m[k]>0:
   mm=setk(m,k,m[k]-1)
   C[mm]=C.get(mm,0)+A[m]*m[k]
 $! dict([(m,C[m])$) m in C if C[m]])
$, p_cont(A,k,nv):
 ds={}
 $) m in A:
  ds[m[k]]=1
 g={}
 $) d in ds:
  g=p_gcd(g,p_coeff(A,k,d),nv)
  if p_isconst(g)$* $J(p_cval(g))==1:
   $! p_const(1,nv)
 $! p_normsign(g)
EVP=(3,5,7,11,13,17,19,23,29,31,37,41)
$, p_at(A,pt):
 s=0
 $) m in A:
  t=A[m]
  $) i in $+($1(m)):
   if m[i]:
    t*=pt[i]**m[i]
  s+=t
 $! s
$, p_gcd(A,B,nv):
 if $- A:
  $! p_normsign(B)
 if $- B:
  $! p_normsign(A)
 if nv $*($1(A)>2 or $1(B)>2):
  c=igcd(p_icont(A),p_icont(B))
  ok=$A
  $) sh in(0,1):
   pt=[EVP[(i+sh*5)%$1(EVP)]*(1+sh)+i $) i in $+(nv)]
   g=igcd(p_at(A,pt),p_at(B,pt))
   if g!=c:
    ok=$2
    $O
  if ok:
   $! p_const(c,nv)
 $! p_gcd0(A,B,nv)
$, p_gcd0(A,B,nv):
 if $- A:
  $! p_normsign(B)
 if $- B:
  $! p_normsign(A)
 vs=[]
 $) k in $+(nv):
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
 pA=$V(A,cA)
 pB=$V(B,cB)
 if p_deg(pA,k)<p_deg(pB,k):
  pA,pB=pB,pA
 $G pB $* p_deg(pB,k)>0:
  r=prem(pA,pB,k,nv)
  pA=pB
  if $- r:
   pB={}
   $O
  pB=$V(r,p_cont(r,k,nv))
 if pB:
  g=p_const(1,nv)
 $&:
  g=$V(pA,p_cont(pA,k,nv))
 $! p_normsign(p_mul(c,g))
$, prem(A,B,k,nv):
 dB=p_deg(B,k)
 lcB=p_lc(B,k)
 R=A
 $G R $* p_deg(R,k)>=dB:
  dR=p_deg(R,k)
  lcR=p_lc(R,k)
  t=p_mul(lcR,{p_mono(nv,k,dR-dB):1})
  R=p_sub(p_mul(R,lcB),p_mul(t,B))
 $! R
$, p_sqfree(P,k,nv):
 dP=p_diff(P,k)
 a=p_gcd(P,dP,nv)
 b=$V(P,a)
 c=$V(dP,a)
 d=p_sub(c,p_diff(b,k))
 res=[]
 i=1
 $G p_deg(b,k)>0:
  a=p_gcd(b,d,nv)
  if p_deg(a,k)>0:
   res.$%((a,i))
  b=$V(b,a)
  c=$V(d,a)
  d=p_sub(c,p_diff(b,k))
  i+=1
  if i>200:
   $O
 $! res
$, p_sqrt(D):
 if $- D:
  $!{}
 lm=max(D)
 lc=D[lm]
 if lc<=0:
  $! $#
 $) x in lm:
  if x%2:
   $! $#
 r=isqrt(lc)
 if r*r!=lc:
  $! $#
 hm=$0([x//2 $) x in lm])
 S={hm:r}
 nv=$1(lm)
 $) _ in $+($1(D)+3):
  R=p_sub(D,p_mul(S,S))
  if $- R:
   $! S
  lmR=max(R)
  lmS=max(S)
  m=[]
  $) i in $+(nv):
   x=lmR[i]-lmS[i]
   if x<0:
    $! $#
   m.$%(x)
  m=$0(m)
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
 if $/(x)is $s:
  $! b,x
 if isq(x):
  $! pw(b,Q(1,x[2])),x[1]
 c,r=$b(x)
 if $/(c)is $s $* c!=1:
  $! pw(b,r),c
 if isq(c):
  $! pw(b,$<(Q(1,c[2]),r)),c[1]
 $! e,1
$, kernels(e,ks):
 t=$/(e)
 if t is $s or t is $D:
  $!
 if t is $p:
  if e $- in ks:
   ks.$%(e)
  $!
 h=e[0]
 if h=='Q':
  $!
 if h=='+' or h=='*':
  $) a in e[1:]:
   kernels(a,ks)
  $!
 if h=='^':
  if $/(e[2])is $s:
   kernels(e[1],ks)
   $!
  k,n=splitpow(e)
  if k==e or $- $((k,'^')or $A:
   if $((k,'^')$* $/(k[2])is $s:
    kernels(k,ks)
    $!
   if k $- in ks:
    ks.$%(k)
  $!
 if e $- in ks:
  ks.$%(e)
$, sortkernels(ks):
 ks.sort(key=$: k:varprio(k)if $/(k)is $p $&(200,okey(k)))
 $! ks
''')
_x(r'''$, ratform(e,ks):
 nv=$1(ks)
 t=$/(e)
 if t is $s:
  $! p_const(e,nv),p_const(1,nv)
 if t is $D:
  $! $#
 if t is $0 $* e[0]=='Q':
  $! p_const(e[1],nv),p_const(e[2],nv)
 if e in ks:
  $!{p_mono(nv,ks.index(e),1):1},p_const(1,nv)
 h=e[0]
 if h=='+':
  N={}
  D=p_const(1,nv)
  $) a in e[1:]:
   r=ratform(a,ks)
   if r is $#:
    $! $#
   n,d=r
   if D==d:
    N=p_add(N,n)
   $&:
    g=p_gcd(D,d,nv)
    d1=$V(d,g)
    D1=$V(D,g)
    N=p_add(p_mul(N,d1),p_mul(n,D1))
    D=p_mul(D,d1)
  $! N,D
 if h=='*':
  N=p_const(1,nv)
  D=p_const(1,nv)
  $) a in e[1:]:
   r=ratform(a,ks)
   if r is $#:
    $! $#
   N=p_mul(N,r[0])
   D=p_mul(D,r[1])
  $! N,D
 if h=='^':
  if $/(e[2])is $s:
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
 $) m in P:
  fs=[P[m]]
  $) i in $+($1(m)):
   if m[i]:
    fs.$%(pw(ks[i],m[i]))
  $Q.$%($I(fs))
 $! $=($Q)
$, cancel_pair(N,D,nv):
 g=p_gcd(N,D,nv)
 if $- p_isconst(g)or p_cval(g)!=1:
  N=$V(N,g)
  D=$V(D,g)
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
 N,D=cancel_pair(r[0],r[1],$1(ks))
 $! N,D,ks
$, comdenom(e):
 if $((e,'$K')or $((e,'mat'):
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
 if $((num,'+')$* $((den,'+')or den==1 or $F(den):
  $! $U(num,den)
 $! $U(num,den)
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
 $! $/(e)is $0 $* e[0]in('=','<','>','<=','>=','/=')
$, hasdenom(e):
 if $((e,'^')$* $F(e[2])$* $`(e[2])<0 $* $- $4(e[1]):
  $! $A
 if $/(e)is $0 $* e[0]in('+','*'):
  $) a in e[1:]:
   if hasdenom(a):
    $! $A
 $! $2
$, $.(e):
 t=$/(e)
 if t is $- $0 or e[0]=='Q' or e[0]=='$p':
  $! e
 h=e[0]
 $M=[$.(a)$) a in e[1:]]
 e2=simp((h,)+$0($M))if h!='hold' $& e
 if $- $((e2,'*'):
  $! e2
 hasden=$2
 hassum=$2
 $) f in e2[1:]:
  if $((f,'^')$* $F(f[2])$* $`(f[2])<0 $* $- $4(f[1]):
   if $((f[1],'+')or($((f[1],'^')$* $((f[1][1],'+')):
    hasden=$A
  if $((f,'+')or($((f,'^')$* $((f[1],'+')):
   hassum=$A
 if $-(hasden $* hassum)$* $- hasden:
  $! e2
 if $_(e2):
  $! e2
 ks=[]
 kernels(e2,ks)
 sortkernels(ks)
 nv=$1(ks)
 if nv==0 or nv>6:
  $! e2
 nums=[]
 dens=[]
 $) f in e2[1:]:
  if $((f,'^')$* $F(f[2])$* $`(f[2])<0:
   dens.$%(pw(f[1],nneg(f[2])))
  $&:
   nums.$%(f)
 num=$I(nums)
 den=$I(dens)
 rn=ratform(num,ks)
 rd=ratform(den,ks)
 if rn is $# or rd is $#:
  $! e2
 if $1(rn[0])*$1(rd[1])>400 or $1(rn[1])*$1(rd[0])>400:
  $! e2
 N=p_mul(rn[0],rd[1])
 D=p_mul(rn[1],rd[0])
 if $1(N)>80 or $1(D)>80 or p_tdeg(N)>30 or p_tdeg(D)>30:
  $! e2
 g=p_gcd(N,D,nv)
 if p_isconst(g):
  $! e2
 N=$V(N,g)
 D=$V(D,g)
 if D $* D[max(D)]<0:
  N=p_neg(N)
  D=p_neg(D)
 $! $U(p2e(N,ks),p2e(D,ks))
$, u_trim(a):
 a=$K(a)
 $G a $* a[-1]==0:
  a.pop()
 $! a
$, u_add(a,b):
 n=max($1(a),$1(b))
 $! u_trim([nadd(a[i]if i<$1(a)$& 0,b[i]if i<$1(b)$& 0)$) i in $+(n)])
$, u_neg(a):
 $![nneg(c)$) c in a]
$, u_sub(a,b):
 $! u_add(a,u_neg(b))
$, u_mul(a,b):
 if $- a or $- b:
  $![]
 r=[0]*($1(a)+$1(b)-1)
 $) i in $+($1(a)):
  if a[i]==0:
   $6
  $) j in $+($1(b)):
   r[i+j]=nadd(r[i+j],nmul(a[i],b[j]))
 $! u_trim(r)
$, u_scale(a,c):
 $! u_trim([nmul(x,c)$) x in a])
$, u_divmod(a,b):
 b=u_trim(b)
 if $- b:
  err("Division by zero")
 a=u_trim(a)
 q=[0]*max($1(a)-$1(b)+1,0)
 r=$K(a)
 lb=b[-1]
 $G $1(r)>=$1(b)$* r:
  c=ndiv(r[-1],lb)
  k=$1(r)-$1(b)
  q[k]=c
  $) j in $+($1(b)):
   r[k+j]=nsub(r[k+j],nmul(c,b[j]))
  r=u_trim(r[:-1])if r[-1]==0 or $A $& r
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
 $G r1:
  q,r=u_divmod(r0,r1)
  r0,r1=r1,r
  s0,s1=s1,u_sub(s0,u_mul(q,s1))
  t0,t1=t1,u_sub(t0,u_mul(q,t1))
 if $- r0:
  $! r0,s0,t0
 c=ninv(r0[-1])
 $! u_scale(r0,c),u_scale(s0,c),u_scale(t0,c)
$, u_toexpr(a,x):
 $! $=([$<(a[i],pw(x,i))$) i in $+($1(a))if a[i]!=0])
$, u_from_expr(e,x):
 cs=$Z(e,x)
 if cs is $#:
  $! $#
 $) c in cs:
  if $- $u(c):
   $! $#
 $! u_trim(cs)
$, u_toint(a):
 L=1
 $) c in a:
  L=ilcm(L,nd(c)[1])
 ints=[nmul(c,L)$) c in a]
 g=0
 $) c in ints:
  g=igcd(g,c)
 if g==0:
  $! ints,1
 if ints[-1]<0:
  g=-g
 ints=[c//g $) c in ints]
 $! ints,Q(g,L)
$, i_divexact(a,b):
 a=$K(a)
 if $1(a)<$1(b):
  $! $#
 q=[0]*($1(a)-$1(b)+1)
 lb=b[-1]
 $) k in $+($1(a)-$1(b),-1,-1):
  c=a[k+$1(b)-1]
  if c%lb:
   $! $#
  c//=lb
  q[k]=c
  if c:
   $) j in $+($1(b)):
    a[k+j]-=c*b[j]
 $) x in a:
  if x:
   $! $#
 $! q
''')
_x(r'''$, aberth(c):
 c=[$3(tofl(x))if $/(x)is $- $3 $& x $) x in c]
 $G c $* c[-1]==0:
  c.pop()
 n=$1(c)-1
 if n<1:
  $![]
 zeros=0
 $G $J(c[0])==0:
  c.pop(0)
  zeros+=1
  n-=1
 $9=[0j]*zeros
 if n<1:
  $! $9
 if n==1:
  $! $9+[-c[0]/c[1]]
 a=[x/c[-1]$) x in c]
 r=0.0
 $) i in $+(n):
  v=$J(a[i])**(1.0/(n-i))
  if v>r:
   r=v
 r=max(r,1e-3)
 z=[r*cmath.exp(1j*(2*$Y.pi*k/n+0.4))$) k in $+(n)]
 $) it in $+(600):
  mx=0.0
  $) k in $+(n):
   zk=z[k]
   p=a[n]
   dp=0j
   $) j in $+(n-1,-1,-1):
    dp=dp*zk+p
    p=p*zk+a[j]
   if p==0:
    $6
   ratio=p/dp if dp!=0 $& 1e-3
   s=0j
   $) j in $+(n):
    if j!=k:
     d=zk-z[j]
     if d!=0:
      s+=1/d
   den=1-ratio*s
   w=ratio/den if den!=0 $& ratio
   z[k]=zk-w
   aw=$J(w)
   if aw>mx*(1+$J(zk))or $A:
    mx=max(mx,aw/(1+$J(zk)))
  if mx<1e-15:
   $O
 res=[]
 $) zk in z:
  $) _ in $+(3):
   p=c[n]
   dp=0j
   $) j in $+(n-1,-1,-1):
    dp=dp*zk+p
    p=p*zk+c[j]
   if dp==0:
    $O
   zk=zk-p/dp
  res.$%(zk)
 $! $9+res
$, divisors_int(n,$z=400):
 n=$J(n)
 if n==0:
  $![1]
 fs,$f=factor_int_small(n)
 if $f>1:
  fs.$%(($f,1))
 ds=[1]
 $) p,k in fs:
  nd_=[]
  $) d in ds:
   v=d
   $) _ in $+(k+1):
    nd_.$%(v)
    v*=p
  ds=nd_
  if $1(ds)>$z:
   $! $#
 ds.sort()
 $! ds
$, combos(n,k):
 idx=$K($+(k))
 $G $A:
  yield idx
  i=k-1
  $G i>=0 $* idx[i]==i+n-k:
   i-=1
  if i<0:
   $!
  idx[i]+=1
  $) j in $+(i+1,k):
   idx[j]=idx[j-1]+1
$, ifactor_sqf(f):
 n=$1(f)-1
 if n<=1:
  $![f]
 res=[]
 $G f[0]==0:
  res.$%([0,1])
  f=f[1:]
 if $1(f)-1<=1:
  $! res+[f]if $1(f)>1 $& res
 roots=aberth(f)
 lcd=divisors_int(f[-1])or[1]
 $f=[]
 $) r in roots:
  found=$2
  if $J(r.imag)<1e-6*(1+$J(r.$R)):
   $) q in lcd:
    p=$s(round(r.$R*q))
    if p==0 $* $J(r.$R)>0.5/q:
     $6
    g=[-p,q]
    if igcd(p,q)!=1:
     $6
    qq=i_divexact(f,g)
    if qq is $- $#:
     res.$%(g)
     f=qq
     found=$A
     $O
  if $- found:
   $f.$%(r)
 if $1(f)-1<=3:
  if $1(f)>1:
   res.$%(f)
  $! res
 roots=$f
 if $1(roots)!=$1(f)-1:
  roots=aberth(f)
 lcd=divisors_int(f[-1])or[1]
 d=2
 $G d<=($1(f)-1)//2 $* $1(roots)<=24:
  done=$2
  $) idx in combos($1(roots),d):
   pc=[1+0j]
   $) i in idx:
    r=roots[i]
    nw=[0j]*($1(pc)+1)
    $) j in $+($1(pc)):
     nw[j+1]+=pc[j]
     nw[j]-=pc[j]*r
    pc=nw
   ok=$A
   $) v in pc:
    if $J(v.imag)>1e-6*(1+$J(v.$R)):
     ok=$2
     $O
   if $- ok:
    $6
   $) q in lcd:
    g=[]
    good=$A
    $) v in pc:
     x=v.$R*q
     ix=$s(round(x))
     if $J(x-ix)>1e-5*(1+$J(x)):
      good=$2
      $O
     g.$%(ix)
    if $- good:
     $6
    qq=i_divexact(f,g)
    if qq is $- $#:
     res.$%(g)
     f=qq
     roots=[roots[i]$) i in $+($1(roots))if i $- in idx]
     done=$A
     $O
   if done:
    $O
  if $- done:
   d+=1
 if $1(f)>1:
  res.$%(f)
 $! res
$, ufactor(a):
 ints,c=u_toint(u_trim(a))
 if $1(ints)<=1:
  $! nmul(c,ints[0]if ints $& 0),[]
 nv=1
 P=dict([((i,),ints[i])$) i in $+($1(ints))if ints[i]])
 $9=[]
 mn=min([m[0]$) m in P])
 if mn>0:
  $9.$%(([0,1],mn))
  P=dict([((m[0]-mn,),P[m])$) m in P])
 if p_deg(P,0)>0:
  $) F,i in p_sqfree(P,0,1):
   fl=[0]*(p_deg(F,0)+1)
   $) m in F:
    fl[m[0]]=F[m]
   if fl[-1]<0:
    fl=[-x $) x in fl]
    c=nneg(c)
   $) g in ifactor_sqf(fl):
    if g[-1]<0:
     g=[-x $) x in g]
     c=nneg(c)
    $9.$%((g,i))
 $&:
  c=nmul(c,p_cval(P))
 $! c,$9
$, i2p(f,nv,k):
 $! dict([(p_mono(nv,k,i),f[i])$) i in $+($1(f))if f[i]])
$, mfactor(P,nv):
 if $- P:
  $! 0,[]
 c=p_icont(P)
 if P[max(P)]<0:
  c=-c
 P=p_scale(P,1)if c==1 $& dict([(m,P[m]//c)$) m in P])
 res=[]
 mins=[min([m[k]$) m in P])$) k in $+(nv)]
 $) k in $+(nv):
  if mins[k]>0:
   res.$%(({p_mono(nv,k,1):1},mins[k]))
 if sum(mins):
  mn=$0(mins)
  P=dict([($0([m[i]-mn[i]$) i in $+(nv)]),P[m])$) m in P])
 c2=mfac_rec(P,nv,res,1)
 $! c*c2,res
$, mfac_rec(P,nv,res,mult):
 vs=p_vars(P,nv)
 if $- vs:
  $! p_cval(P)**mult if P $& 0
 if $1(vs)==1:
  k=vs[0]
  fl=[0]*(p_deg(P,k)+1)
  $) m in P:
   fl[m[k]]=P[m]
  cc,fs=ufactor(fl)
  $) g,i in fs:
   res.$%((i2p(g,nv,k),i*mult))
  $! cc**mult if $/(cc)is $s $& nipow(cc,mult)
 vs.sort(key=$: k:p_deg(P,k))
 k=vs[0]
 cst=1
 C=p_cont(P,k,nv)
 if $- p_isconst(C):
  cst=mfac_rec(C,nv,res,mult)
  P=$V(P,C)
 $@ p_cval(C)!=1:
  P=$V(P,C)
 $) F,i in p_sqfree(P,k,nv):
  $) g in msplit(F,nv,0):
   g=p_normsign(g)
   res.$%((g,i*mult))
 $! cst
$, ishomog(F):
 d=$#
 $) m in F:
  s=sum(m)
  if d is $#:
   d=s
  $@ s!=d:
   $! $2
 $! $A
''')
_x(r'''$, msplit(F,nv,$;):
 vs=p_vars(F,nv)
 if $1(vs)<=1:
  if $- vs:
   $![F]
  k=vs[0]
  fl=[0]*(p_deg(F,k)+1)
  $) m in F:
   fl[m[k]]=F[m]
  cc,fs=ufactor(fl)
  $9=[]
  $) g,i in fs:
   $) _ in $+(i):
    $9.$%(i2p(g,nv,k))
  $! $9 if $9 $&[F]
 if $;>8:
  $![F]
 $) k in vs:
  if p_deg(F,k)==1:
   pass
 if $1(vs)==2 $* ishomog(F):
  a,b=vs
  fl=[0]*(p_deg(F,a)+1)
  $) m in F:
   fl[m[a]]=F[m]
  cc,fs=ufactor(fl)
  if $1(fs)>1 or(fs $* fs[0][1]>1):
   $9=[]
   $) g,i in fs:
    d=$1(g)-1
    G={}
    $) j in $+($1(g)):
     if g[j]:
      m=[0]*nv
      m[a]=j
      m[b]=d-j
      G[$0(m)]=g[j]
    $) _ in $+(i):
     $9.$%(G)
   $! $9
  $![F]
 $) k in vs:
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
    G1=$V(G1,p_mul(p_cont(G1,k,nv),p_const(p_icont($V(G1,p_cont(G1,k,nv))),nv)))
    G2=$V(G2,p_mul(p_cont(G2,k,nv),p_const(p_icont($V(G2,p_cont(G2,k,nv))),nv)))
    if G1 $* G2:
     $! msplit(G1,nv,$;+1)+msplit(G2,nv,$;+1)
 $) k in vs:
  if p_deg(F,k)<2:
   $6
  lc=p_lc(F,k)
  tc=p_coeff(F,k,0)
  da=pdivisors(lc,nv)
  db=pdivisors(tc,nv)
  if da is $# or db is $# or $1(da)*$1(db)>3000:
   $6
  x={p_mono(nv,k,1):1}
  $) a in da:
   ax=p_mul(a,x)
   $) b in db:
    $) s in(1,-1):
     G=p_add(ax,p_scale(b,s))
     Qt=$V(F,G)
     if Qt is $- $#:
      $![G]+msplit(Qt,nv,$;+1)
 $![F]
$, pdivisors(P,nv):
 c,fs=mfactor(P,nv)
 di=divisors_int(c,60)
 if di is $#:
  $! $#
 ds=[p_const(d,nv)$) d in di]
 $) g,m in fs:
  nds=[]
  $) d in ds:
   v=d
   $) _ in $+(m+1):
    nds.$%(v)
    v=p_mul(v,g)
  ds=nds
  if $1(ds)>300:
   $! $#
 $! ds
$, factor_int_full(n):
 fs={}
 if n<0:
  n=-n
 st=[n]
 $G st:
  m=st.pop()
  if m==1:
   $6
  small,m=factor_int_small(m)
  $) p,k in small:
   fs[p]=fs.get(p,0)+k
  if m==1:
   $6
  if m>>1024:
   err('Number too large to factor')
  if isprime(m):
   fs[m]=fs.get(m,0)+1
   $6
  d=rho(m)
  st.$%(d)
  st.$%(m//d)
 ks=sorted(fs)
 $![(p,fs[p])$) p in ks]
$, powmod(b,e,m):
 r=1
 b%=m
 $G e>0:
  if e&1:
   r=r*b%m
  e>>=1
  b=b*b%m
 $! r
$, isprime(n):
 if n<2:
  $! $2
 $) p in(2,3,5,7,11,13,17,19,23,29,31,37):
  if n%p==0:
   $! n==p
 d=n-1
 s=0
 $G d%2==0:
  d//=2
  s+=1
 $) a in(2,3,5,7,11,13,17,19,23,29,31,37):
  x=powmod(a,d,n)
  if x==1 or x==n-1:
   $6
  $) _ in $+(s-1):
   x=x*x%n
   if x==n-1:
    $O
  $&:
   $! $2
 $! $A
$, rho(n):
 if n%2==0:
  $! 2
 r=iroot(n,2)
 if r*r==n:
  $! r
 c=1
 $G $A:
  x=2
  y=2
  d=1
  cnt=0
  $G d==1:
   x=(x*x+c)%n
   y=(y*y+c)%n
   y=(y*y+c)%n
   d=igcd($J(x-y),n)
   cnt+=1
   if cnt>10000:
    $O
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
 $) p,k in factor_int_full(n):
  fs.$%(p if k==1 $&('^',p,k))
 $) p,k in factor_int_full(d):
  fs.$%(('^',p,-k))
 if $- fs:
  $! 1
 if $1(fs)==1 $* fs[0]==-1:
  $!-1
 if $1(fs)==1:
  $!('hold',fs[0])
 $!('hold',('*',)+$0(fs))
$, factor_expr(e,var=$#,$C=$2):
 if $u(e):
  $! factor_rat_held(e)
 if $((e,'$K')or $((e,'mat'):
  $! mapexpr($: a:factor_expr(a,var,$C),e)
 if isrel(e):
  $!(e[0],factor_expr(e[1],var,$C),factor_expr(e[2],var,$C))
 if $_(e):
  $! e
 ks=[]
 kernels(e,ks)
 sortkernels(ks)
 nv=$1(ks)
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
 $) g,m in fn_:
  nfac.$}(split_radical(p2e(g,ks),m,var,$C))
 dfac=[]
 $) g,m in fd:
  dfac.$}(split_radical(p2e(g,ks),m,var,$C))
 items=[]
 $) f,m in nfac:
  if $F(f):
   const=nmul(const,nipow(f,m))
  $&:
   items.$%((f,m))
 ditems=[]
 $) f,m in dfac:
  if $F(f):
   const=ndiv(const,nipow(f,m))
  $&:
   ditems.$%((f,m))
 items.sort(key=$: fm:fsortkey(fm[0]))
 ditems.sort(key=$: fm:fsortkey(fm[0]))
 $9=[]
 if const!=1 or($- items $* $- ditems):
  $9.$%(const)
 $) f,m in items:
  $9.$%(f if m==1 $&('^',f,m))
 $) f,m in ditems:
  $9.$%(('^',f,-m))
 if $1($9)==1:
  if $(($9[0],'^')or $F($9[0]):
   $!('hold',$9[0])if $- $F($9[0])$& $9[0]
  $! $9[0]
 $!('hold',('*',)+$0($9))
$, fsortkey(f):
 ss=$g(f)
 ss.sort(key=varprio)
 d=0
 if ss:
  d=degree(f,ss[0])
  if d is $#:
   d=99
 $!($1(ss),okey(ss),d,okey(f))
$, split_radical(f,m,var,$C):
 if var is $# $* $- $C:
  $![(f,m)]
 vs=$g(f)
 if var is $#:
  if $1(vs)!=1:
   $![(f,m)]
  x=vs[0]
 $&:
  x=var
 cs=$Z(f,x)
 if cs is $# or $1(cs)!=3:
  if cs is $- $# $* $1(cs)==2 $* $C:
   $![(f,m)]
  $![(f,m)]
 c,b,a=cs
 D=$?($]($<(b,b),$<(4,a,c)))
 if $- $4(D):
  if var is $#:
   $![(f,m)]
 $&:
  v=$X(D)
  if $/(v)is $3:
   v=v.$R
  if v<0 $* $- $C:
   $![(f,m)]
 sD=$N(D)
 r1=$U($^($l(b),sD),$<(2,a))
 r2=$U($]($l(b),sD),$<(2,a))
 res=[(a,m)]if a!=1 $&[]
 res.$%(($](x,r2),m))
 res.$%(($](x,r1),m))
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
 $) v in p_vars(N,$1(ks))+p_vars(D,$1(ks)):
  if v!=k:
   $! $#
 nv=$1(ks)
 num=[0]*(max(p_deg(N,k),0)+1)
 $) m in N:
  num[m[k]]=N[m]
 den=[0]*(p_deg(D,k)+1)
 $) m in D:
  den[m[k]]=D[m]
 if $1(den)<=1:
  $! $#
 q,rem=u_divmod(num,den)
 cc,fs=ufactor(den)
 $Q=[u_toexpr(q,x)]
 if rem:
  $~=[u_trim(pw_list(f,m))$) f,m in fs]
  rem=u_scale(rem,ninv(cc))
  $) j in $+($1(fs)):
   f,m=fs[j]
   Pj=$~[j]
   others=[1]
   $) i in $+($1(fs)):
    if i!=j:
     others=u_mul(others,$~[i])
   g,s,t=u_egcd(others,Pj)
   Aj=u_divmod(u_mul(rem,s),Pj)[1]
   fe=u_toexpr(f,x)
   $) p in $+(m,0,-1):
    if $- Aj:
     $O
    qq,cj=u_divmod(Aj,f)
    if cj:
     $Q.$%($U(u_toexpr(cj,x),pw(fe,p)))
    Aj=qq
 $! $=($Q)
$, pw_list(f,m):
 r=[1]
 $) _ in $+(m):
  r=u_mul(r,f)
 $! r
$, propfrac(e,x=$#):
 if $u(e):
  n,d=nd(e)
  if d==1:
   $! e
  qn=$J(n)//d
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
  vs=p_vars(D,$1(ks))
  if $- vs:
   $! e
  x=ks[vs[0]]
 num=p2e(N,ks)
 den=p2e(D,ks)
 cn=$Z(num,x)
 cd=$Z(den,x)
 if cn is $# or cd is $# or $1(cd)<=1:
  $! e
 qq,rr=e_divmod(cn,cd)
 $! $^(fromcoeffs(qq,x),$U(fromcoeffs(rr,x),den))
$, e_divmod(a,b):
 a=[$?(c)$) c in a]
 b=[$?(c)$) c in b]
 $G b $* b[-1]==0:
  b.pop()
 $G a $* a[-1]==0:
  a.pop()
 if $- b:
  err("Division by zero")
 q=[0]*max($1(a)-$1(b)+1,1)
 r=$K(a)
 lb=b[-1]
 $G $1(r)>=$1(b)$* r:
  c=$.($U(r[-1],lb))
  kk=$1(r)-$1(b)
  q[kk]=c
  $) j in $+($1(b)):
   r[kk+j]=$?($](r[kk+j],$<(c,b[j])))
  r.pop()
  $G r $* r[-1]==0:
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
 nv=$1(ks)
 g=p_gcd(ra[0],rb[0],nv)
 if $- ks:
  $! p_cval(g)
 $! p2e(g,ks)
$, expand_full(e,var=$#):
 if $((e,'$K')or $((e,'mat'):
  $! mapexpr($: a:expand_full(a,var),e)
 if isrel(e):
  $!(e[0],expand_full(e[1],var),expand_full(e[2],var))
 x=$?(e)
 if $- hasdenom(x)or $_(x):
  $! x
 if var is $#:
  ks=$g(x)
  ks.sort(key=varprio)
  $) v in ks:
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
class $m($7):
 pass
$, dfun($B,u):
 if $B=='sin':
  $! fn('cos',u)
 if $B=='cos':
  $! $l(fn('sin',u))
 if $B=='tan':
  $! pw(fn('cos',u),-2)
 if $B=='$|':
  $! pw($](1,pw(u,2)),Q(-1,2))
 if $B=='arccos':
  $! $l(pw($](1,pw(u,2)),Q(-1,2)))
 if $B=='$w':
  $! pw($^(pw(u,2),1),-1)
 if $B=='sinh':
  $! fn('cosh',u)
 if $B=='cosh':
  $! fn('sinh',u)
 if $B=='tanh':
  $! pw(fn('cosh',u),-2)
 if $B=='arcsinh':
  $! pw($^(pw(u,2),1),Q(-1,2))
 if $B=='arccosh':
  $! pw($](pw(u,2),1),Q(-1,2))
 if $B=='arctanh':
  $! pw($](1,pw(u,2)),-1)
 if $B=='ln':
  $! pw(u,-1)
 if $B=='$J':
  $! fn('sign',u)
 if $B in('sign','floor','ceiling','round','ipart','$s'):
  $! 0
 $! $#
$, diff(e,x,n=1):
 if n<0:
  r=e
  $) _ in $+(-n):
   r=integrate(r,x)
  $! r
 $) _ in $+(n):
  e=diff1(e,x)
 $! e
$, diff1(e,x):
 if $((e,'$K')or $((e,'mat'):
  $! mapexpr($: a:diff1(a,x),e)
 if $((e,'=')or $((e,'<')or $((e,'>'):
  $!(e[0],diff1(e[1],x),diff1(e[2],x))
 if $8(e,x):
  $! 0
 if e==x:
  $! 1
 h=e[0]
 if h=='+':
  $! $=([diff1(a,x)$) a in e[1:]])
 if h=='*':
  fs=e[1:]
  $Q=[]
  $) i in $+($1(fs)):
   d=diff1(fs[i],x)
   if d!=0:
    $Q.$%($I([d]+[fs[j]$) j in $+($1(fs))if j!=i]))
  $! $=($Q)
 if h=='^':
  b=e[1]
  p=e[2]
  if $8(p,x):
   $! $<(p,pw(b,$](p,1)),diff1(b,x))
  if $8(b,x):
   $! $<(e,fn('ln',b),diff1(p,x))
  $! $<(e,$^($<(diff1(p,x),fn('ln',b)),$U($<(p,diff1(b,x)),b)))
 if h=='log':
  b=e[2]if $1(e)>2 $& 10
  $! diff1($U(fn('ln',e[1]),fn('ln',b)),x)
 if h=='when':
  $! fn('when',e[1],diff1(e[2],x),diff1(e[3],x))if $1(e)>3 $& fn('when',e[1],diff1(e[2],x))
 if h=='$L' $* $1(e)==3 $* e[2]==x:
  $! e[1]
 if h=='$L' $* $1(e)==5 $* $8(e[1],x)is $2 $* e[2]!=x:
  f,v,a,b=e[1],e[2],e[3],e[4]
  $! $]($<($W(f,v,b),diff1(b,x)),$<($W(f,v,a),diff1(a,x)))
 if $1(e)==2:
  d=dfun(h,e[1])
  if d is $- $#:
   $! $<(d,diff1(e[1],x))
 $!('d',e,x)
$, $i(u,x):
 cs=$Z(u,x)
 if cs is $# or $1(cs)!=2 or cs[1]==0:
  $! $#
 $! cs[1],cs[0]
$, nice(e):
 ${:
  e=$.(e)
 $5 $7:
  $! e
 if $- hasdenom(e)or $_(e)or $((e,'$K')or $((e,'mat'):
  $! e
 best=e
 bl=$1(fmt(e))
 if bl>400:
  $! e
 $) f in(comdenom,factor_expr):
  ${:
   c=f(e)
   l=$1(fmt(c))
   if l<bl:
    best=c
    bl=l
  $5 $7:
   pass
 $! best
BUDGET=[0]
$, integrate(f,x,$;=0):
 BUDGET[0]=0
 r=integ(f,x,$;)
 if r is $# $* hasdenom(f):
  g=$.(f)
  if g!=f:
   BUDGET[0]=0
   r=integ(g,x,$;)
 if r is $#:
  $!('$L',f,x)
 $! r
$, integ(f,x,$;=0):
 if $;>7:
  $! $#
 if $;==0:
  BUDGET[0]=0
 BUDGET[0]+=1
 if BUDGET[0]>400:
  $! $#
 if $8(f,x):
  $! $<(f,x)
 if f==x:
  $! $<($v,pw(x,2))
 h=f[0]if $/(f)is $0 $& $#
 if h=='+':
  $9=[]
  $) t in f[1:]:
   r=integ(t,x,$;+1)
   if r is $#:
    $! integ_whole(f,x,$;)
   $9.$%(r)
  $! $=($9)
 if h=='*':
  c=[g $) g in f[1:]if $8(g,x)]
  v=[g $) g in f[1:]if $- $8(g,x)]
  if c:
   r=integ($I(v),x,$;)
   if r is $#:
    $! $#
   $! $<($I(c),r)
 if h=='when':
  a=integ(f[2],x,$;+1)
  b=integ(f[3],x,$;+1)if $1(f)>3 $& $#
  if a is $# or($1(f)>3 $* b is $#):
   $! $#
  $!('when',f[1],a,b)if b is $- $# $&('when',f[1],a)
 r=itable(f,x)
 if r is $- $#:
  $! r
 $! integ_whole(f,x,$;)
$, integ_whole(f,x,$;):
 d=degree(f,x)
 if d is $- $#:
  g=$?(f)
  if g!=f:
   $! integ(g,x,$;+1)
 r=irational(f,x)
 if r is $- $#:
  $! r
 r=itanpow(f,x,$;)
 if r is $- $#:
  $! r
 r=isecpow(f,x,$;)
 if r is $- $#:
  $! r
 r=isubst(f,x,$;)
 if r is $- $#:
  $! r
 r=itrigsub(f,x,$;)
 if r is $- $#:
  $! r
 if hastrig(f):
  g=tcollect(f)
  if g!=f:
   r=integ(g,x,$;+1)
   if r is $- $#:
    $! r
 r=iparts(f,x,$;)
 if r is $- $#:
  $! r
 g=$?(f)
 if g!=f:
  r=integ(g,x,$;+1)
  if r is $- $#:
   $! r
 if $;<4:
  g=untan(f)
  if g!=f:
   r=integ(g,x,$;+2)
   if r is $- $#:
    $! r
  g=unhyp(f)
  if g!=f:
   r=integ($?(g),x,$;+2)
   if r is $- $#:
    $! r
  r=iweier(f,x,$;)
  if r is $- $#:
   $! r
  r=iquartic(f,x,$;)
  if r is $- $#:
   $! r
 $! $#
$, qfrac(A,B,p,q,x):
 w=$N($]($<(4,q),pw(p,2)))
 P=$^(pw(x,2),$<(p,x),q)
 $! $^($<(A,$v,fn('ln',P)),
 $<($](B,$<(A,p,$v)),$U(2,w),fn("$w",$?($U($^($<(2,x),p),w)))))
$, iquartic(f,x,$;):
 n,d=numer_denom(f)
 cd=$Z(d,x)
 cn=$Z(n,x)
 if cd is $# or cn is $# or $1(cd)!=5 or $1(cn)>4:
  $! $#
 if cd[1]!=0 or cd[3]!=0 or $- all([$4(q)$) q in cd+cn]):
  $! $#
 a,b,c=cd[4],cd[2],cd[0]
 ${:
  if fv_(c)/fv_(a)<=0:
   $! $#
  q=$N($U(c,a))
  s2=$]($<(2,q),$U(b,a))
  if fv_(s2)<=0:
   $! $#
 $5 $7:
  $! $#
 sr=$N(s2)
 cn=[$U(v,a)$) v in cn]+[0]*(4-$1(cn))
 n0,n1,n2,n3=cn
 BE=$U(n0,q)
 EmB=$U($](n1,$<(q,n3)),sr)
 B=$<($v,$](BE,EmB))
 E=$<($v,$^(BE,EmB))
 CmA=$U($](n2,BE),sr)
 A=$<($v,$](n3,CmA))
 C=$<($v,$^(n3,CmA))
 P1=$^(pw(x,2),$<(sr,x),q)
 P2=$^($](pw(x,2),$<(sr,x)),q)
 R=$^(qfrac(A,B,sr,q,x),qfrac(C,E,$l(sr),q,x))
 $! R if antiok(R,f,x)$& $#
$, unhyp(e):
 if $/(e)is $- $0 or e[0]=='Q':
  $! e
 a=[unhyp(b)$) b in e[1:]]
 if $1(a)==1 $* e[0]in('sinh','cosh','tanh'):
  p=pw('e',a[0])
  m=pw('e',$l(a[0]))
  if e[0]=='sinh':
   $! $<($v,$](p,m))
  if e[0]=='cosh':
   $! $<($v,$^(p,m))
  $! $U($](p,m),$^(p,m))
 $! simp((e[0],)+$0(a))
''')
_x(r'''$, trigargs_x(f,x,$9):
 if $/(f)is $- $0 or f[0]=='Q':
  $!
 if f[0]in('sin','cos','tan')$* $- $8(f[1],x):
  if f[1]$- in $9:
   $9.$%(f[1])
  $!
 $) b in f[1:]:
  trigargs_x(b,x,$9)
$, iweier(f,x,$;):
 us=[]
 trigargs_x(f,x,us)
 if $1(us)!=1:
  $! $#
 u=us[0]
 lu=$i(u,x)
 if lu is $#:
  $! $#
 t='W%d_'%$;
 q=$^(1,pw(t,2))
 $, rep(e):
  if $/(e)is $- $0 or e[0]=='Q':
   $! e
  if $1(e)==2 $* e[1]==u:
   if e[0]=='sin':
    $! $U($<(2,t),q)
   if e[0]=='cos':
    $! $U($](1,pw(t,2)),q)
   if e[0]=='tan':
    $! $U($<(2,t),$](1,pw(t,2)))
  $! simp((e[0],)+$0(rep(b)$) b in e[1:]))
 g=rep(f)
 if $- $8(g,x):
  $! $#
 g=$.($U($<(2,g),$<(lu[0],q)))
 R=integ(g,t,$;+2)
 if R is $#:
  $! $#
 R=$W(R,t,fn('tan',$<($v,u)))
 $! R if antiok(R,f,x)$& $#
$, itable(f,x):
 h=head(f)
 if h=='^':
  b=f[1]
  p=f[2]
  if $8(p,x):
   lb=$i(b,x)
   if lb is $- $#:
    a=lb[0]
    if p==-1:
     $! $U(fn('ln',fn('$J',b)),a)
    $! $U(pw(b,$^(p,1)),$<(a,$^(p,1)))
   if(p==$v or p==Q(-1,2))$* degree(b,x)==2:
    $! iquadrad(b,p,x)
   if $1(b)==2 $* head(b)in('sin','cos','tan','sinh','cosh')$* $/(b)is $0:
    lu=$i(b[1],x)
    if lu is $- $#:
     a=lu[0]
     u=b[1]
     n=b[0]
     if n=='cos' $* p==-2:
      $! $U(fn('tan',u),a)
     if n=='sin' $* p==-2:
      $! $U($l(pw(fn('tan',u),-1)),a)
     if n=='cos' $* p==-1:
      $! $U(fn('ln',fn('$J',$^(pw(fn('cos',u),-1),fn('tan',u)))),a)
     if n=='sin' $* p==-1:
      $! $U(fn('ln',fn('$J',fn('tan',$<($v,u)))),a)
     if n=='tan' $* p==-1:
      $! $U(fn('ln',fn('$J',fn('sin',u))),a)
     if n=='cosh' $* p==-2:
      $! $U(fn('tanh',u),a)
  if $8(b,x):
   lu=$i(p,x)
   if lu is $- $#:
    a=lu[0]
    if b=='e':
     $! $U(f,a)
    $! $U(f,$<(a,fn('ln',b)))
  $! $#
 if $/(f)is $0 $* $1(f)==2:
  u=f[1]
  lu=$i(u,x)
  if lu is $#:
   $! $#
  a=lu[0]
  r=$#
  if h=='sin':
   r=$l(fn('cos',u))
  $@ h=='cos':
   r=fn('sin',u)
  $@ h=='tan':
   r=$l(fn('ln',fn('$J',fn('cos',u))))
  $@ h=='sinh':
   r=fn('cosh',u)
  $@ h=='cosh':
   r=fn('sinh',u)
  $@ h=='tanh':
   r=fn('ln',fn('cosh',u))
  $@ h=='ln':
   r=$]($<(u,fn('ln',u)),u)
  $@ h=='$w':
   r=$]($<(u,fn('$w',u)),$<($v,fn('ln',$^(pw(u,2),1))))
  $@ h=='$|':
   r=$^($<(u,fn('$|',u)),$N($](1,pw(u,2))))
  $@ h=='arccos':
   r=$]($<(u,fn('arccos',u)),$N($](1,pw(u,2))))
  $@ h=='$J':
   r=$<($v,u,fn('$J',u))
  $@ h=='sign':
   r=fn('$J',u)
  $@ h=='arcsinh':
   r=$]($<(u,fn('arcsinh',u)),$N($^(pw(u,2),1)))
  $@ h=='arctanh':
   r=$^($<(u,fn('arctanh',u)),$<($v,fn('ln',$](1,pw(u,2)))))
  if r is $- $#:
   $! $U(r,a)
 if h=='log' $* $1(f)==3:
  lu=$i(f[1],x)
  if lu is $- $#:
   u=f[1]
   $! $U($]($<(u,fn('ln',u)),u),$<(lu[0],fn('ln',f[2])))
 $! $#
$, iquadrad(b,p,x):
 cs=$Z(b,x)
 C,B,A=cs
 if $- $4(A):
  $! $#
 av=$X(A)
 if $/(av)is $3:
  $! $#
 D=$]($<(B,B),$<(4,A,C))
 if p==Q(-1,2):
  if av<0:
   $! $<(pw($l(A),Q(-1,2)),fn('$|',$U($l($^($<(2,A,x),B)),$N(D))))
  sA=$N(A)
  $! $<(pw(A,Q(-1,2)),fn('ln',fn('$J',$^($N(b),$<(sA,x),$U(B,$<(2,sA))))))
 J=iquadrad(b,Q(-1,2),x)
 if J is $#:
  $! $#
 $! $^($U($<($^($<(2,A,x),B),$N(b)),$<(4,A)),
 $<($U($]($<(4,A,C),$<(B,B)),$<(8,A)),J))
$, irational(f,x):
 ks=[]
 kernels(f,ks)
 $) k in ks:
  if k!=x:
   $! $#
 if $- hasdenom(f):
  $! $#
 pf=partfrac(f,x)
 if pf is $#:
  $! $#
 $Q=pf[1:]if $((pf,'+')$&(pf,)
 $9=[]
 $) t in $Q:
  if $- hasdenom(t):
   r=integ(t,x,5)
   if r is $#:
    $! $#
   $9.$%(r)
   $6
  fs=t[1:]if $((t,'*')$&(t,)
  num=[]
  den=$#
  k=1
  $) g in fs:
   if $((g,'^')$* $/(g[2])is $s $* g[2]<0:
    den=g[1]
    k=-g[2]
   $&:
    num.$%(g)
  if den is $#:
   $! $#
  N=$I(num)
  dg=degree(den,x)
  if dg==1:
   r=integ(t,x,5)
   if r is $#:
    $! $#
   $9.$%(r)
  $@ dg==2:
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
 $! $=($9)
$, iquadfrac(N,Qd,k,x):
 cs=$Z(N,x)
 if cs is $# or $1(cs)>2:
  $! $#
 n0=cs[0]
 n1=cs[1]if $1(cs)>1 $& 0
 C,B,A=$Z(Qd,x)
 res=[]
 if n1!=0:
  if k==1:
   D=$]($<(B,B),$<(4,A,C))
   dv=$X(D)if $4(D)$& 0
   arg=Qd if($/(dv)is $- $3 $* dv<0 $* $X(A)>0)$& fn('$J',Qd)
   res.$%($<($U(n1,$<(2,A)),fn('ln',arg)))
  $&:
   res.$%($<($U(n1,$<(2,A)),$U(-1,$<(k-1,pw(Qd,k-1)))))
 c0=$](n0,$U($<(n1,B),$<(2,A)))
 if c0!=0:
  J=jquad(A,B,C,Qd,k,x)
  if J is $#:
   $! $#
  res.$%($<(c0,J))
 $! $=(res)
$, jquad(A,B,C,Qd,k,x):
 D=$?($]($<(B,B),$<(4,A,C)))
 if k==1:
  if $- $4(D):
   $! $#
  dv=$X(D)
  if $/(dv)is $3:
   $! $#
  L=$^($<(2,A,x),B)
  if dv<0:
   s=$N($l(D))
   $! $<($U(2,s),fn('$w',$U(L,s)))
  if dv>0:
   s=$N(D)
   $! $<(pw(s,-1),fn('ln',fn('$J',$U($](L,s),$^(L,s)))))
  $! $U(-2,L)
 Jp=jquad(A,B,C,Qd,k-1,x)
 if Jp is $#:
  $! $#
 Dl=$l(D)
 L=$^($<(2,A,x),B)
 $! $^($<($U(L,$<(k-1,Dl)),pw(Qd,1-k)),
 $<($U($<(2*k-3,2,A),$<(k-1,Dl)),Jp))
$, itanpow(f,x,$;):
 if $((f,'^')$* $((f[1],'tan')$* $/(f[2])is $s $* f[2]>=2:
  u=f[1][1]
  lu=$i(u,x)
  if lu is $#:
   $! $#
  n=f[2]
  a=lu[0]
  t=f[1]
  first=$U(pw(t,n-1),$<(n-1,a))
  $f=integ(pw(t,n-2),x,$;+1)
  if $f is $#:
   $! $#
  $! $](first,$f)
 $! $#
''')
_x(r'''$, isecpow(f,x,$;):
 if($((f,'^')$* head(f[1])in('cos','sin')$* $1(f[1])==2
 $* $/(f[2])is $s $* f[2]<=-3):
  u=f[1][1]
  lu=$i(u,x)
  if lu is $#:
   $! $#
  n=-f[2]
  a=lu[0]
  if f[1][0]=='cos':
   first=$<(pw(fn('cos',u),2-n),fn('tan',u))
  $&:
   first=$l($<(pw(fn('sin',u),2-n),pw(fn('tan',u),-1)))
  $f=integ(pw(f[1],2-n),x,$;+1)
  if $f is $#:
   $! $#
  $! $^($U(first,$<(n-1,a)),$<(Q(n-2,n-1),$f))
 $! $#
$, cands(f,x,$9):
 if $/(f)is $- $0 or $8(f,x)or f[0]=='Q':
  $!
 h=f[0]
 if h=='+' or h=='*':
  $) a in f[1:]:
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
  if f[1]==x $* f $- in $9 $* $F(f[2])$* f[2]!=-1:
   $9.$%(f)
   if $n(f[2])$* f[2]%2==0 $* f[2]>2 $* pw(x,2)$- in $9:
    $9.$%(pw(x,2))
  cands(f[1],x,$9)
  cands(f[2],x,$9)
  $!
 if f $- in $9:
  $9.$%(f)
 $) a in f[1:]:
  if a!=x $* $- $8(a,x)$* a $- in $9:
   $9.$%(a)
  cands(a,x,$9)
$, subst_kernel(q,u,V,x):
 if $((u,'^')$* u[1]==x $* $F(u[2]):
  q2=$W(q,x,pw(V,pw(u[2],-1)))
  $! $W(q2,fn('$J',V),V)
 if $((u,'ln'):
  lu=$i(u[1],x)
  if lu is $- $#:
   a,b=lu
   $! $W(q,x,$U($](pw('e',V),b),a))
 if $((u,'^')$* isq(u[2])$* $- $8(u[1],x):
  cs_=$Z(u[1],x)
  q2=$W(q,u,V)
  if cs_ is $- $# $* $- $8(q2,x):
   nz=[k $) k in $+(1,$1(cs_))if cs_[k]!=0]
   if $1(nz)==1:
    k=nz[0]
    xk=$U($](pw(V,pw(u[2],-1)),cs_[0]),cs_[k])
    q3=$W(q2,x,pw(xk,Q(1,k)))
    if $8(q3,x):
     $! q3
  $! q2
 if $((u,'^')$* u[1]=='e':
  lu=$i(u[2],x)
  if lu is $- $# $* lu[1]==0:
   a=lu[0]
   $! subst_exp(q,a,V,x)
 $! $W(q,u,V)
$, subst_exp(q,a,V,x):
 if $/(q)is $- $0 or q[0]=='Q':
  $! q
 if q[0]=='^' $* q[1]=='e':
  lm=$i(q[2],x)
  if lm is $- $#:
   $! $<(pw(V,$U(lm[0],a)),pw('e',lm[1]))
 $! simp((q[0],)+$0(subst_exp(b,a,V,x)$) b in q[1:]))
$, isubst(f,x,$;):
 if $;>5:
  $! $#
 VV='V%d_'%$;
 $G has(f,VV)or VV==x:
  VV=VV+'_'
 cs=[]
 cands(f,x,cs)
 fracf=hasfracpow(f,x)
 big=$1(okey(f))>500
 $) u in cs[:14]:
  if u==x:
   $6
  du=diff(u,x)
  if du==0:
   $6
  q=$U(f,du)
  if $- big:
   q=$.(q)
  q2=subst_kernel(q,u,VV,x)
  if $8(q2,x)$*(fracf or $- hasfracpow(q2,VV))$* $1(okey(q2))<800:
   r=integ(q2,VV,$;+2)
   if r is $- $#:
    r=$W(r,VV,u)
    if antiok(r,f,x):
     $! r
 $) u in cs:
  if $((u,'+'):
   lu=$i(u,x)
   if lu is $- $#:
    a,b=lu
    g=$?($U($W(f,x,$U($](VV,b),a)),a))
    r=integ(g,VV,$;+2)
    if r is $- $#:
     $! $W(r,VV,u)
 $! $#
TPTS=(-2.3,-1.7,-0.8,-0.35,0.3,0.75,1.6,2.4)
$, antiok(F,f,x):
 if $1($g(f))>1 or $1($g(F))>1:
  $! $A
 $, v(e,t):
  ${:
   z=$X(e,{x:t})
  $5 $7:
   $! $#
  if $/(z)is $3:
   if $J(z.imag)>1e-9*(1+$J(z.$R)):
    $! $#
   z=z.$R
  if z!=z or $J(z)>1e12:
   $! $#
  $! z
 $) t in TPTS:
  y=v(f,t)
  if y is $#:
   $6
  h=1e-5*(1+$J(t))
  a=v(F,t+h)
  b=v(F,t-h)
  if a is $# or b is $#:
   $6
  if $J((a-b)/(2*h)-y)>1e-4*(1+$J(y)):
   $! $2
 $! $A
$, itrigsub(f,x,$;):
 rad=[]
 radicals(f,x,rad)
 if $- rad:
  $! $#
 B=rad[0]
 cs=$Z(B,x)
 if cs is $# or $1(cs)!=3 or cs[1]!=0 or $- $4(cs[0])or $- $4(cs[2]):
  $! $#
 if any([q!=B $) q in rad]):
  $! $#
 c0,c2=cs[0],cs[2]
 T='T%d_'%$;
 if fv_(c0)<0 $* fv_(c2)>0:
  r=$N($U($l(c0),c2))
  xs=$U(r,fn('cos',T))
  rt=$<($N(c2),r,fn('tan',T))
  dx=$<(r,fn('tan',T),pw(fn('cos',T),-1))
  g=$<(subrad(f,B,rt,x,xs),dx)
  R=$#
  $) h in(pyth_to(g,'cos'),pyth_to(g,'sin'),pyth(g)):
   R=integ(h,T,$;+2)
   if R is $- $#:
    $O
  if R is $#:
   $! $#
  R=backtrig(texpand(R),T,$U(pw(B,$v),$<($N(c2),x)),$U(r,x))
  R=$W(R,T,fn('arccos',$U(r,x)))
  if $- $8(R,T)or $- antiok(R,f,x):
   $! $#
  $! R
 if fv_(c0)<=0:
  $! $#
 sc0=$N(c0)
 if fv_(c2)<0:
  r=$N($U(c0,$l(c2)))
  xs=$<(r,fn('sin',T))
  rt=$<(sc0,fn('cos',T))
  dx=$<(r,fn('cos',T))
 $&:
  r=$N($U(c0,c2))
  xs=$<(r,fn('tan',T))
  rt=$U(sc0,fn('cos',T))
  dx=$U(r,pw(fn('cos',T),2))
 g=$<(subrad(f,B,rt,x,xs),dx)
 R=$#
 $) h in(pyth(g),pyth_to(g,'cos'),pyth_to(g,'sin')):
  R=integ(h,T,$;+2)
  if R is $- $#:
   $O
 if R is $#:
  $! $#
 R=texpand(R)
 sq=pw(B,$v)
 if fv_(c2)<0:
  sinT=$U(x,r)
  cosT=$U(sq,sc0)
  Tx=fn('$|',$U(x,r))
 $&:
  cosT=$U(sc0,sq)
  sinT=$<($U(x,r),cosT)
  Tx=fn('$w',$U(x,r))
 R=backtrig(R,T,sinT,cosT)
 R=$W(R,T,Tx)
 if $- $8(R,T)or $- antiok(R,f,x):
  $! $#
 $! R
$, radicals(f,x,$9):
 if $/(f)is $- $0 or f[0]=='Q':
  $!
 if f[0]=='^' $* isq(f[2])$* f[2][2]==2 $* $- $8(f[1],x):
  $9.$%(f[1])
 $) a in f[1:]:
  radicals(a,x,$9)
$, subrad(f,B,rt,x,xs):
 if f==x:
  $! xs
 if $/(f)is $- $0 or f[0]=='Q':
  $! f
 if f[0]=='^' $* f[1]==B $* isq(f[2])$* f[2][2]==2:
  $! pw(rt,f[2][1])
 $! simp((f[0],)+$0(subrad(a,B,rt,x,xs)$) a in f[1:]))
$, backtrig(R,T,sinT,cosT):
 if $/(R)is $- $0 or R[0]=='Q':
  $! R
 if $1(R)==2 $* R[1]==T:
  if R[0]=='sin':
   $! sinT
  if R[0]=='cos':
   $! cosT
  if R[0]=='tan':
   $! $U(sinT,cosT)
 $! simp((R[0],)+$0(backtrig(a,T,sinT,cosT)$) a in R[1:]))
$, hasfracpow(e,x):
 if $/(e)is $- $0 or e[0]=='Q':
  $! $2
 if e[0]=='^' $* $- $n(e[2])$* $- $8(e[1],x):
  $! $A
 $) a in e[1:]:
  if hasfracpow(a,x):
   $! $A
 $! $2
''')
_x(r'''$, hastrig(f):
 if $/(f)is $- $0 or f[0]=='Q':
  $! $2
 if f[0]in('sin','cos'):
  $! $A
 $) a in f[1:]:
  if hastrig(a):
   $! $A
 $! $2
$, ispoly(e,x):
 $! degree(e,x)is $- $#
$, iparts(f,x,$;):
 if $;>5:
  $! $#
 fs=f[1:]if $((f,'*')$&(f,)
 P=[]
 G=[]
 $) g in fs:
  if ispoly(g,x):
   P.$%(g)
  $&:
   G.$%(g)
 if $1(G)==2:
  ex=$#
  tr=$#
  $) g in G:
   if $((g,'^')$* g[1]=='e' $* $i(g[2],x):
    ex=g
   $@ head(g)in('sin','cos')$* $i(g[1],x):
    tr=g
  if ex is $- $# $* tr is $- $# $* $- P:
   a=$i(ex[2],x)[0]
   b=$i(tr[1],x)[0]
   u=tr[1]
   den=$^($<(a,a),$<(b,b))
   if tr[0]=='sin':
    r=$<(ex,$]($<(a,fn('sin',u)),$<(b,fn('cos',u))))
   $&:
    r=$<(ex,$^($<(a,fn('cos',u)),$<(b,fn('sin',u))))
   $! $U(r,den)
  $! $#
 if $1(G)!=1:
  $! $#
 g=G[0]
 Pp=$I(P)
 gh=head(g)
 tabular=$2
 if $((g,'^')$* g[1]=='e' $* $i(g[2],x):
  tabular=$A
 $@ $((g,'^')$* $F(g[1])$* $i(g[2],x):
  tabular=$A
 $@ gh in('sin','cos','sinh','cosh')$* $i(g[1],x):
  tabular=$A
 if tabular $* P:
  res=[]
  sg=1
  Gi=g
  Pd=Pp
  $) _ in $+(40):
   Gi=integ(Gi,x,$;+1)
   if Gi is $#:
    $! $#
   res.$%($<(sg,Pd,Gi))
   Pd=diff(Pd,x)
   sg=-sg
   if Pd==0:
    $! $=(res)
  $! $#
 if gh in('ln','$w','$|','arccos','log','arcsinh','arctanh')or($((g,'^')$* head(g[1])in('ln','$|','$w')$* $n(g[2])$* g[2]>0):
  V=integ(Pp,x,$;+1)
  if V is $#:
   $! $#
  $f=integ($.($?($<(V,diff(g,x)))),x,$;+1)
  if $f is $#:
   $! $#
  $! $]($<(g,V),$f)
 $! $#
$, defint(f,x,a,b):
 if a==b:
  $! 0
 if $4(a)$* $4(b):
  ${:
   if numpt(a)>numpt(b):
    r=defint(f,x,b,a)
    $! $l(r)if $- $((r,'$L')$&('$L',f,x,a,b)
  $5 $7:
   pass
 if haswhen(f,x)$* $4(a)$* $4(b):
  ps=whensplit(f,x,a,b)
  if ps is $- $#:
   total=0
   $) p,q,g in ps:
    if g=='$H' or has(g,'$H'):
     $! '$H'
    total=$^(total,defint(g,x,p,q))
   $! total
 BUDGET[0]=0
 F=integ(f,x)
 if F is $# $* hasdenom(f):
  BUDGET[0]=0
  F=integ($.(f),x)
 sing=singular_points(f,x,a,b)or[]
 if F is $- $# $* $- $_(f):
  $) p in singular_points(F,x,a,b)or[]:
   if all([$J(fv_(p)-fv_(q))>1e-9 $) q in sing]):
    sing.$%(p)
  sing.sort(key=fv_)
  if $4(a)$* $4(b)$* fv_(a)>fv_(b):
   sing.reverse()
  pts=[a]+sing+[b]
  total=0
  infs=[]
  $) i in $+($1(pts)-1):
   lo=pts[i]
   hi=pts[i+1]
   vb=$z(F,x,hi,-1 if $- isinf(hi)$& 0)
   va=$z(F,x,lo,1 if $- isinf(lo)$& 0)
   if $((vb,'$z')or $((va,'$z'):
    total=$#
    $O
   d=$](vb,va)
   if va=='$H' or vb=='$H':
    $! '$H'
   if has(va,'$P')or has(vb,'$P'):
    if d $- in('$P',('*',-1,'$P')):
     $! '$H'
   if d=='$H' or has(d,'$H'):
    total=$#
    $O
   if has(d,'$P'):
    infs.$%(d)
   total=$^(total,d)
  if total is $- $# $* infs:
   if all([q==infs[0]$) q in infs])$* infs[0]in('$P',('*',-1,'$P')):
    $! infs[0]
   $! '$H'
  if total is $- $# $* total!='$H':
   $! total
 if $4(a)$* $4(b)$* freeofall(f,[s $) s in $g(f)if s!=x]):
  ${:
   $! nint_split(f,x,a,b)
  $5 $7:
   pass
 $!('$L',f,x,a,b)
$, haswhen(f,x):
 if $/(f)is $- $0 or f[0]=='Q':
  $! $2
 if f[0]in('when','$J')$* $- $8(f[1],x):
  $! $A
 $) a in f[1:]:
  if haswhen(a,x):
   $! $A
 $! $2
$, gensol(r):
 ns=[w $) w in $g(r)if w[0]=='n' $* w[1:].isdigit()]
 if $1(ns)==1 $* $4($W(r,ns[0],0)):
  $! ns[0]
 $! $#
$, firstwhen_(f,x):
 if $/(f)is $- $0 or f[0]=='Q':
  $! $2
 if f[0]=='when' $* $- $8(f[1],x):
  $! $A
 $! any([firstwhen_(a,x)$) a in f[1:]])
$, whenpts(f,x,$9):
 if $/(f)is $- $0 or f[0]=='Q':
  $!
 if f[0]=='$J' $* $- $8(f[1],x):
  rs=$o(f[1],x,$2)
  if rs $* rs!='all':
   $) r in rs:
    if($x(r)or gensol(r))$* r $- in $9:
     $9.$%(r)
 if f[0]=='when' $* $- $8(f[1],x):
  cs=[f[1]]
  $G cs:
   c=cs.pop()
   if head(c)in('$*','or','$-'):
    cs.$}(c[1:])
   $@ head(c)in('<','>','<=','>=','=','/='):
    rs=$o($](c[1],c[2]),x,$2)
    if rs $* rs!='all':
     $) r in rs:
      if($x(r)or gensol(r))$* r $- in $9:
       $9.$%(r)
 $) a in f[1:]:
  whenpts(a,x,$9)
$, pickwhen(f,x,t):
 if $/(f)is $- $0 or f[0]=='Q':
  $! f
 if f[0]=='when' $* $- $8(f[1],x):
  ${:
   c=nbool(f[1],{x:t})
  $5 $7:
   $! '$H'
  if c:
   $! pickwhen(f[2],x,t)
  $! pickwhen(f[3],x,t)if $1(f)>3 $& '$H'
 if f[0]=='$J' $* $- $8(f[1],x):
  u=pickwhen(f[1],x,t)
  ${:
   $! u if fv_($W(u,x,t))>=0 $& $l(u)
  $5 $7:
   $! f
 $! simp((f[0],)+$0(pickwhen(a,x,t)$) a in f[1:]))
$, numpt(v):
 if v=='$P':
  $! 1e300
 if v==('*',-1,'$P'):
  $!-1e300
 $! fv_(v)
$, fv_(v):
 z=$X(v)
 $! z.$R if $/(z)is $3 $& z
$, whensplit(f,x,a,b):
 pts=[]
 whenpts(f,x,pts)
 lo=numpt(a)
 hi=numpt(b)
 if lo>hi:
  $! $#
 ex=[]
 $) p in pts:
  n=gensol(p)
  if n is $#:
   ex.$%(p)
  $@ hi-lo<1e4:
   $) k in $+(-300,301):
    q=$W(p,n,k)
    if lo<fv_(q)<hi $* q $- in ex:
     ex.$%(q)
 ins=[p $) p in ex if lo<fv_(p)<hi]
 ins.sort(key=fv_)
 ends=[a]+ins+[b]
 $9=[]
 $) i in $+($1(ends)-1):
  p,q=ends[i],ends[i+1]
  pv,qv=numpt(p),numpt(q)
  if pv<-1e299:
   t=qv-1.0
  $@ qv>1e299:
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
  $! $z(pickwhen(f,x,t),x,a,dirn)
 av=fv_(a)
 d=1e-6
 $) p in pts:
  q=$J(fv_(p)-av)
  if q>1e-12:
   d=min(d,q/2)
 r=$z(pickwhen(f,x,av+d),x,a,1)if dirn>=0 $& $#
 l=$z(pickwhen(f,x,av-d),x,a,-1)if dirn<=0 $& $#
 if dirn==1:
  $! r
 if dirn==-1:
  $! l
 if r==l:
  $! r
 ${:
  if $4(r)$* $4(l)$* $J($X(r)-$X(l))<1e-12:
   $! r
 $5 $7:
  pass
 $! '$H'
$, isinf(v):
 $! v=='$P' or v==('*',-1,'$P')
$, singular_points(f,x,a,b):
 if $-($4(a)$* $4(b)):
  $![]
 ${:
  av=nreal(a)if $- isinf(a)$&(-1e300 if a!='$P' $& 1e300)
  bv=nreal(b)if $- isinf(b)$&(1e300 if b=='$P' $&-1e300)
 $5 $7:
  $![]
 lo,hi=min(av,bv),max(av,bv)
 pts=[]
 dens=[]
 collect_dens(f,x,dens)
 $) d in dens:
  u=u_from_expr(d,x)
  if u is $- $# $* $1(u)<2:
   $6
  if u is $#:
   if hi-lo<1e6:
    $) r in scanzeros(d,x,lo,hi):
     if all([$J(fv_(q)-r)>1e-9 $) q in pts]):
      pts.$%(snapzero(d,x,r))
   $6
  $) r in aberth(u):
   if $J(r.imag)<1e-9 $* lo<r.$R<hi:
    rr=exactify(r.$R)if $J(r.$R-round(r.$R))<1e-12 $& r.$R
    pts.$%(rr)
 pts.sort(key=fv_)
 if av>bv:
  pts.reverse()
 $! pts
$, collect_dens(f,x,$9):
 if $/(f)is $- $0 or f[0]=='Q':
  $!
 if f[0]=='^' $* $F(f[2])$* $`(f[2])<0 $* $- $8(f[1],x):
  $9.$%(f[1])
 if f[0]=='tan' $* $- $8(f[1],x):
  $9.$%(fn('cos',f[1]))
 if f[0]in('ln','log')$* $- $8(f[1],x):
  $9.$%(f[1])
 $) a in f[1:]:
  collect_dens(a,x,$9)
$, scanzeros(d,x,lo,hi,n=400):
 $9=[]
 $, g(t):
  ${:
   v=$X(d,{x:t})
   $! v.$R if $/(v)is $3 $& v
  $5 $7:
   $! $#
 h=(hi-lo)/n
 t0=lo+h*1e-3
 v0=g(t0)
 $) k in $+(1,n+1):
  t1=lo+h*k-(h*1e-3 if k==n $& 0)
  v1=g(t1)
  if v0 is $- $# $* v1 is $- $# $* v0*v1<=0:
   a,b,fa=t0,t1,v0
   $) it in $+(60):
    m=0.5*(a+b)
    fm=g(m)
    if fm is $#:
     $O
    if(fm<=0)==(fa<=0):
     a,fa=m,fm
    $&:
     b=m
   m=0.5*(a+b)
   fm=g(m)
   if fm is $- $# $* $J(fm)<1e-6 $* lo<m<hi:
    $9.$%(m)
  t0,v0=t1,v1
 $! $9
$, snapzero(d,x,r):
 $) c in(exactify_guess(r/$Y.pi),exactify_guess(r)):
  if $/(c)is $D:
   $6
  v=$<(c,'pi')if c is $- exactify_guess(r)$& c
  ${:
   if $J(fv_($W(d,x,v)))<1e-9:
    $! v
  $5 $7:
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
  if NERR[0]>1e-7*max(1.0,$J(r))$* $- isinf(a)$* $- isinf(b):
   NERR[0]=0.0
   a0=nreal(a)
   w=nreal(b)-a0
   g=$: u:_nv(f,x,a0+w*u)
   $) k in $+(3):
    g=smooth(g)
    NERR[0]=0.0
    r=w*_gk_adapt(g,0.0,1.0,tol,0)
    if NERR[0]<=1e-7*max(1.0,$J(r)):
     $O
  if NERR[0]>1e-7*max(1.0,$J(r))$*(isinf(a)!=isinf(b)):
   if isinf(a):
    f,a,b=$W(f,x,$l(x)),$l(b),'$P'
   a0=nreal(a)
   g=$: t:_nv(f,x,a0+t/(1-t))/(1-t)**2 if t<1 $& 0.0
   $) j in $+(3):
    g=smooth(g)
    NERR[0]=0.0
    r=_gk_adapt(g,0.0,1.0,tol,0)
    if NERR[0]<=1e-7*max(1.0,$J(r)):
     $O
  if NERR[0]>1e-7*max(1.0,$J(r)):
   err('Questionable accuracy: the $L may diverge')
 if r!=r or $J(r)==$D('$P'):
  err('Questionable accuracy: the $L may diverge')
 if $/(r)is $3:
  if $J(r.imag)<1e-12*(1+$J(r.$R)):
   $! r.$R
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
   g=$: t:_nv(f,x,t/(1-t*t))*(1+t*t)/(1-t*t)**2
   $! _gk_adapt(g,-1.0,1.0,tol,0)
  if isinf(b):
   a0=nreal(a)
   g=$: t:_nv(f,x,a0+t/(1-t))/(1-t)**2
   $! _gk_adapt(g,0.0,1.0,tol,0)
  b0=nreal(b)
  g=$: t:_nv(f,x,b0-(1-t)/t)/(t*t)
  $! _gk_adapt(g,0.0,1.0,tol,0)
 a0=nreal(a)
 b0=nreal(b)
 g=$: t:_nv(f,x,t)
 $! _gk_adapt(g,a0,b0,tol,0)
$, smooth(g):
 $! $: t:g(t*t*(3-2*t))*6*t*(1-t)
$, nint_split(f,x,a,b):
 pts=[a]+(singular_points(f,x,a,b)or[])+[b]
 r=0
 $) i in $+($1(pts)-1):
  r=$^(r,nint(f,x,pts[i],pts[i+1]))
 $! r
$, trigk(f,x,$9):
 if $/(f)is $- $0 or f[0]=='Q':
  $!
 if f[0]in('sin','cos')$* $- $8(f[1],x):
  lu=$i(f[1],x)
  $9.$%(lu[0]if lu is $- $# $* $4(lu[0])$& $#)
 $) a in f[1:]:
  trigk(a,x,$9)
$, nint_osc(f,x,a,b,tol):
 ks=[]
 trigk(f,x,ks)
 if $- ks or $# in ks:
  $! $#
 k=max([$J(tofl($X(q)))$) q in ks])
 if k==0:
  $! $#
 sgn_=1.0
 if isinf(a):
  f=$W(f,x,$l(x))
  a,b=$l(b),'$P'
  if a==('*',-1,('*',-1,'$P')):
   a='$P'
 a0=tofl($X(a))
 h=$Y.pi/k
 g=$: t:_nv(f,x,t)
 sums=[]
 $Q=[]
 s_=0.0
 t=a0
 $) i in $+(40):
  c=_gk_adapt(g,t,t+h,tol,6)
  s_+=c
  $Q.$%($J(c))
  t+=h
  sums.$%(s_)
 if max($Q[-4:])>0.25*max($Q[:4])$* max($Q[-4:])>1e-12:
  err('Questionable accuracy: the $L may diverge')
 est=wynn(sums)
 est2=wynn(sums[:-6])
 if est is $# or est2 is $# or $J(est-est2)>1e-7*max(1.0,$J(est)):
  err('Questionable accuracy: the $L may diverge')
 $! sgn_*est
$, wynn(S):
 n=$1(S)
 e0=[0.0]*(n+1)
 e1=$K(S)
 best=S[-1]
 $) k in $+(1,n):
  e2=[]
  $) j in $+($1(e1)-1):
   d=e1[j+1]-e1[j]
   if d==0:
    $! e1[j+1]
   e2.$%(e0[j+1]+1.0/d)
  if k%2==0 $* e2:
   best=e2[-1]
  e0,e1=e1,e2
  if $1(e1)<2:
   $O
 $! best
$, _nv(f,x,t):
 ${:
  v=$X(f,{x:t})
 $5 $E:
  $! 0.0
 $5($T,$a):
  $! 0.0
 if $/(v)is $3:
  if $J(v.imag)>1e-12*(1+$J(v.$R)):
   $! v
  v=v.$R
 if v!=v or v in($D('$P'),$D('-$P')):
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
 $) j in $+(7):
  dx=h*XGK[j]
  f1=g(c-dx)
  f2=g(c+dx)
  rk+=WGK[j]*(f1+f2)
  if j%2==1:
   rg+=WG[j//2]*(f1+f2)
 $! rk*h,$J((rk-rg)*h)
$, _gk_adapt(g,a,b,tol,$;):
 r,e=_gk(g,a,b)
 NBUD[0]-=1
 if NBUD[0]<0:
  NERR[0]+=e+1e-6*(1+$J(r))
  $! r
 if e<=tol*max(1.0,$J(r)):
  $! r
 if $;>18:
  NERR[0]+=e
  $! r
 m=0.5*(a+b)
 $! _gk_adapt(g,a,m,tol/2,$;+1)+_gk_adapt(g,m,b,tol/2,$;+1)
BIGP=10**6
$, s_const(c):
 if c==0:
  $!({},BIGP)
 $!({0:c},BIGP)
$, s_val(A):
 if $- A[0]:
  $! A[1]
 m=$#
 $) k in A[0]:
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
 $) S in(A,B):
  $) k in S[0]:
   if ncmp(k,p)<0:
    d[k]=$^(d.get(k,0),S[0][k])
 $9={}
 $) k in d:
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
 $) a in A[0]:
  $) b in B[0]:
   k=nadd(a,b)
   if ncmp(k,p)<0:
    d[k]=$^(d.get(k,0),$<(A[0][a],B[0][b]))
 $9={}
 $) k in d:
  v=cs(d[k])
  if v!=0:
   $9[k]=v
 $!($9,p)
$, s_scale(A,c,shift=0):
 $9={}
 $) k in A[0]:
  v=cs($<(A[0][k],c))
  if v!=0:
   $9[nadd(k,shift)]=v
 $!($9,nadd(A[1],shift))
$, s_lead(A):
 if $- A[0]:
  $k $m()
 v=s_val(A)
 $! v,A[0][v]
$, s_split(A):
 a,c=s_lead(A)
 U=s_scale(A,pw(c,-1),nneg(a))
 U=(dict([(k,U[0][k])$) k in U[0]if k!=0]),U[1])
 $! a,c,U
$, s_powser(U,coefs):
 res=s_const(coefs[0])
 res=(res[0],U[1])
 P=({0:1},BIGP)
 $) k in $+(1,$1(coefs)):
  P=s_mul(P,U)
  if $- P[0]:
   $O
  if coefs[k]!=0:
   res=s_add(res,s_scale(P,coefs[k]))
 $! res
$, nterms(U):
 v=s_val(U)
 if ncmp(v,0)<=0:
  $k $m()
 p=U[1]
 if ncmp(p,BIGP)>=0:
  $! 0 if $- U[0]$& 30
 n=nfloor(ndiv(p,v))+1
 if n>30:
  n=30
 $! n
$, s_pow(A,p):
 if $/(p)is $s $* p>=0:
  R=({0:1},BIGP)
  $) _ in $+(p):
   R=s_mul(R,A)
  $! R
 a,c,U=s_split(A)
 n=nterms(U)if U[0]$& 0
 coefs=[1]
 b=1
 $) k in $+(1,n+1):
  b=$<(b,$U($](p,k-1),k))
  coefs.$%(b)
 S=s_powser(U,coefs)if U[0]$&({0:1},U[1])
 ap=$<(a,p)
 if $- $u(ap):
  $k $m()
 cp=pw(c,p)
 $! s_scale(S,cp,ap)
$, s_exp(A):
 neg_=[k $) k in A[0]if ncmp(k,0)<0]
 if neg_:
  $k $m()
 c0=A[0].get(0,0)
 U=(dict([(k,A[0][k])$) k in A[0]if k!=0]),A[1])
 shift=0
 if has(c0,LNT):
  cc=$Z(c0,LNT)
  if cc is $# or $1(cc)!=2 or $- $u(cc[1]):
   $k $m()
  shift=cc[1]
  c0=cc[0]
 n=nterms(U)if U[0]$& 0
 coefs=[1]
 f=1
 $) k in $+(1,n+1):
  f=f*k
  coefs.$%(Q(1,f))
 S=s_powser(U,coefs)if U[0]$&({0:1},U[1])
 $! s_scale(S,pw('e',c0),shift)
$, s_ln(A):
 a,c,U=s_split(A)
 n=nterms(U)if U[0]$& 0
 coefs=[0]
 $) k in $+(1,n+1):
  coefs.$%(Q((-1)**(k+1),k))
 S=s_powser(U,coefs)if U[0]$&({},U[1])
 base=$^(fn('ln',c),$<(a,LNT))
 $! s_add(S,(({0:base}if base!=0 $&{}),BIGP))
$, s_fun($B,A):
 neg_=[k $) k in A[0]if ncmp(k,0)<0]
 if neg_:
  if $B=='$w':
   a,c=s_lead(A)
   sg=$X(c)
   sg=1 if($/(sg)is $- $3 $* sg>0)$&-1
   inv_=s_pow(A,-1)
   $! s_add(s_const($<(sg,$v,'pi')),s_scale(s_fun('$w',inv_),-1))
  if $B=='tanh':
   a,c=s_lead(A)
   $! s_const(1 if $X(c).$R>0 $&-1)
  $k $m()
 c0=A[0].get(0,0)
 if has(c0,LNT):
  $k $m()
 U=(dict([(k,A[0][k])$) k in A[0]if k!=0]),A[1])
 if $B=='$J' or $B=='sign':
  a,c=s_lead(A)
  v=$X($W(c,LNT,-1000))if has(c,LNT)$& $X(c)
  if $/(v)is $3:
   $k $m()
  sg=1 if v>0 $&-1
  if $B=='sign':
   $! s_const(sg)
  $! s_scale(A,sg)
 if $B in('floor','ceiling','ipart','round','$s','fpart'):
  $k $m()
 n=nterms(U)if U[0]$& 0
 z='Z_'
 g=fn($B,z)
 coefs=[$W(g,z,c0)]
 fact=1
 $) k in $+(1,n+1):
  g=diff(g,z)
  fact*=k
  coefs.$%(cs($U($W(g,z,c0),fact)))
 $) cc in coefs:
  if has(cc,'$H')or cc=='$H' or has(cc,'$P'):
   $k $m()
 if $- U[0]:
  $! s_const(coefs[0])if $A $& $#
 $! s_powser(U,coefs)
$, ser(e,N):
 if $8(e,TV):
  $! s_const(e)
 if e==TV:
  $!({1:1},BIGP)
 h=e[0]
 if h=='+':
  R=({},BIGP)
  $) a in e[1:]:
   R=s_add(R,ser(a,N))
  $! trunc(R,N)
 if h=='*':
  R=({0:1},BIGP)
  $) a in e[1:]:
   R=trunc(s_mul(R,ser(a,N)),N)
  $! R
 if h=='^':
  b=e[1]
  p=e[2]
  if $8(p,TV):
   B=ser(b,N)
   if $u(p):
    $! trunc(s_pow(B,p),N)
   if $4(p)or $A:
    a,c,U=s_split(B)
    if a!=0:
     $k $m()
    $! trunc(s_pow(B,p),N)
  if $8(b,TV):
   $! trunc(s_exp(s_scale(ser(p,N),fn('ln',b))),N)
  $! trunc(s_exp(s_mul(ser(p,N),s_ln(ser(b,N)))),N)
 if h=='ln':
  $! trunc(s_ln(ser(e[1],N)),N)
 if h=='log':
  b=e[2]if $1(e)>2 $& 10
  $! trunc(s_scale(s_ln(ser(e[1],N)),pw(fn('ln',b),-1)),N)
 if $1(e)==2:
  $! trunc(s_fun(h,ser(e[1],N)),N)
 $k $m()
$, trunc(A,N):
 if ncmp(A[1],N)<=0:
  $! A
 $!(dict([(k,A[0][k])$) k in A[0]if ncmp(k,N)<0]),N)
''')
_x(r'''$, series_t(e,order,need=$#):
 extra=3
 $) _ in $+(4):
  S=ser(e,nadd(order,extra))
  if ncmp(S[1],order)>0 $*(need is $# or S[0]):
   $! S
  extra=extra*2+2
 $! S
$, lead_t(e):
 $) N in(3,6,12,24):
  S=ser(e,N)
  if S[0]:
   v=s_val(S)
   if ncmp(v,S[1])<0:
    $! v,S[0][v]
 $! $#
$, lnt_lim(c):
 n,d=numer_denom(c)
 cn=$Z(n,LNT)
 cd=$Z(d,LNT)
 if cn is $# or cd is $#:
  $k $m()
 p=$1(cn)-1
 q=$1(cd)-1
 if p<q:
  $! 0
 if p==q:
  $! $U(cn[p],cd[q])
 v=lnt_sign(c)
 if $/(v)is $3:
  $! '$H'
 $! '$P' if v>0 $&('*',-1,'$P')
$, lnt_sign(c):
 cc=$Z(c,LNT)
 if cc is $#:
  v=$X($W(c,LNT,-1e6))
  $! v
 k=$1(cc)-1
 lead=cc[k]
 v=$X(lead)
 if $/(v)is $3:
  $! v
 if k%2:
  v=-v
 $! v
$, $z(f,x,a,dirn=0):
 $! infnorm(limit0(f,x,a,dirn))
$, infnorm(r):
 if $((r,'*')$*('$P' in r[1:]):
  c=$I([b $) b in r[1:]if b!='$P'])
  if $4(c):
   ${:
    v=fv_(c)
    $! '$P' if v>0 $&(('*',-1,'$P')if v<0 $& '$H')
   $5 $7:
    pass
 $! r
$, limit0(f,x,a,dirn=0):
 if $((f,'$K')or $((f,'mat'):
  $! mapexpr($: g:$z(g,x,a,dirn),f)
 if $8(f,x):
  $! f
 if haswhen(f,x)$* $4(a)$* firstwhen_(f,x):
  $! whenlimit(f,x,a,dirn)
 if hashead(f,'fact')$* isinf(a):
  g=stirling(factnorm(f,x),x)
  if g!=f:
   $! $z(g,x,a,dirn)
 if $4(a):
  r=lim_bounded(f,x,a,dirn)
  if r is $- $#:
   $! r
 if a=='$P' or a==('*',-1,'$P'):
  sub_=pw(TV,-1)if a=='$P' $& $l(pw(TV,-1))
  $! lim_side(f,x,sub_,a)
 if dirn==0 $* $- has_disc(f):
  ${:
   v=$W(f,x,a)
   if v!='$H' $* $8(v,'$H')$* $- has(v,'$P'):
    v2=v
    if $4(v2):
     vv=$X(v2)
     if $/(vv)is $3 $* $J(vv.imag)>1e-12 $* $8(f,'i'):
      $k $T
    $! v
  $5($S,$E,$T,TypeError):
   pass
 if dirn==1:
  $! lim_side(f,x,$^(a,TV),a)
 if dirn==-1:
  $! lim_side(f,x,$](a,TV),a)
 r=lim_side(f,x,$^(a,TV),a)
 l=lim_side(f,x,$](a,TV),a)
 if r==l:
  $! r
 if $((r,'$z')or $((l,'$z'):
  $!('$z',f,x,a)
 ${:
  if $4(r)$* $4(l)$* $- has(r,'$P')$* $- has(l,'$P'):
   if $J($X(r)-$X(l))<1e-12:
    $! r
 $5 $7:
  pass
 $! '$H'
$, hashead(f,h):
 if $/(f)is $- $0 or f[0]=='Q':
  $! $2
 $! f[0]==h or any([hashead(b,h)$) b in f[1:]])
STEPF=('floor','ceiling','fpart','ipart','$s','round')
$, factnorm(f,x):
 fs=[]
 $, walk(e):
  if $/(e)is $- $0 or e[0]=='Q':
   $!
  if e[0]=='fact' $* $- $8(e[1],x):
   fs.$%(e[1])
  $) b in e[1:]:
   walk(b)
 walk(f)
 if $- fs:
  $! f
 base=fs[0]
 $) u in fs:
  d=$](base,u)
  if $n(d)$* d>0:
   base=u
 $, rep(e):
  if $/(e)is $- $0 or e[0]=='Q':
   $! e
  if e[0]=='fact' $* $- $8(e[1],x):
   k=$](e[1],base)
   if $n(k)$* 0<k<=50:
    $! $I([$^(base,j)$) j in $+(1,k+1)]+[fn('fact',base)])
   $! e
  $! simp((e[0],)+$0(rep(b)$) b in e[1:]))
 $! $.(rep(f))
$, stirling(f,x):
 if $/(f)is $- $0 or f[0]=='Q':
  $! f
 if f[0]=='fact' $* $- $8(f[1],x):
  u=stirling(f[1],x)
  $! $<($N($<(2,'pi',u)),pw($U(u,'e'),u))
 $! simp((f[0],)+$0(stirling(b,x)$) b in f[1:]))
$, bounded_nodes(f,x,a,dirn,$9):
 if $/(f)is $- $0 or f[0]=='Q':
  $!
 $) b in f[1:]:
  bounded_nodes(b,x,a,dirn,$9)
 if $1(f)==2 $* $- $8(f[1],x)$* f[0]in STEPF+('sin','cos'):
  ${:
   L=$z(f[1],x,a,dirn)
  $5 $7:
   $!
  if L in('$P',('*',-1,'$P'))or L=='$H' or $((L,'$z'):
   if(f,1)$- in $9:
    $9.$%((f,1))
  $@ f[0]in STEPF $* $- isinf(a):
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
   $! r if r==l $& '$H'
  stp=[n $) n,k in ns if k==0]
  ns=[n $) n,k in ns if k==1]
  if stp:
   t=fv_(a)+dirn*1e-7*(1+$J(fv_(a)))
   g=f
   $) n in stp:
    ${:
     g=replnode_(g,n,exactify($X(n,{x:t})))
    $5 $7:
     $! $#
   $! $z(g,x,a,dirn)
 $&:
  ns=[n $) n,k in ns]
 if $- ns:
  $! $#
 C='C_'
 reps=[]
 $) n in ns:
  if n[0]in('sin','cos'):
   reps.$%((n,C,(-1,0,1)))
  $@ n[0]in('floor','$s','ipart'):
   reps.$%((n,$](n[1],C),(0,Q(1,2),1)))
  $@ n[0]=='ceiling':
   reps.$%((n,$^(n[1],C),(0,Q(1,2),1)))
  $@ n[0]=='round':
   reps.$%((n,$^(n[1],C),(Q(-1,2),0,Q(1,2))))
  $&:
   reps.$%((n,C,(0,Q(1,2),1)))
 if $1(reps)>1:
  $! $#
 n,r,cs=reps[0]
 g=replnode_(f,n,r)
 $c=[]
 $) c in cs:
  v=$z($W(g,C,c),x,a,dirn)
  if $((v,'$z'):
   $! $#
  $c.$%(v)
 if $c[0]==$c[1]==$c[2]$* $c[0]!='$H':
  $! $c[0]
 $! '$H'
$, replnode_(f,w,r):
 if f==w:
  $! r
 if $/(f)is $- $0 or f[0]=='Q':
  $! f
 $! simp((f[0],)+$0(replnode_(b,w,r)$) b in f[1:]))
$, has_disc(f):
 if $/(f)is $- $0 or f[0]=='Q':
  $! $2
 if f[0]in('floor','ceiling','sign','ipart','round','fpart','$s','when','$J','mod'):
  $! $A
 $) a in f[1:]:
  if has_disc(a):
   $! $A
 $! $2
''')
_x(r'''$, lim_side(f,x,sub_,a):
 g=$W(f,x,sub_)
 ${:
  r=lead_t(g)
  if r is $#:
   $! 0
  al,c=r
  if has(c,TV):
   $k $m()
  if ncmp(al,0)>0:
   $! 0
  if has(c,LNT)$* al==0:
   $! lnt_lim(c)
  if has(c,LNT):
   v=lnt_sign(c)
   if $/(v)is $3:
    $! '$H'
   if v==0:
    $k $m()
   $! '$P' if v>0 $&('*',-1,'$P')
  if al==0:
   $! c
  if $- $4(c):
   $! $<(c,'$P')
  v=$X(c)
  if $/(v)is $3:
   $! '$H'
  $! '$P' if v>0 $&('*',-1,'$P')
 $5($m,$S,$E,$T,TypeError,$a):
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
  $! $=([lnexp(b)$) b in g[1:]])
 if h=='^':
  if g[1]=='e':
   $! g[2]
  $! $<(g[2],lnexp(g[1]))
 if $F(g)$* $`(g)>0:
  $! fn('ln',g)
 $! fn('ln',g)
$, lim_log(g,$;=0):
 if head(g)$- in('*','^'):
  $! $#
 v=$#
 $) t in(1e-3,1e-2,1e-1):
  ${:
   v=$X(g,{TV:t})
  $5 $7:
   v=$#
  if v is $- $# $* $/(v)is $- $3 $* v==v $* v!=0 $* $J(v)!=$D('$P'):
   $O
  v=$#
 if v is $#:
  $! $#
 sg=1 if v>0 $&-1
 L=lim_val($.(lnexp($<(sg,g))),$;)
 if L is $# or $((L,'$z')or L=='$H':
  $! $#
 if L=='$P':
  $! '$P' if sg>0 $&('*',-1,'$P')
 if L==('*',-1,'$P'):
  $! 0
 if $4(L):
  $! $<(sg,pw('e',L))
 $! $#
$, lim_val(g,$;):
 ${:
  r=lead_t(g)
  if r is $#:
   $! 0
  al,c=r
  if has(c,TV):
   $k $m()
  if ncmp(al,0)>0:
   $! 0
  if has(c,LNT)$* al==0:
   $! lnt_lim(c)
  if has(c,LNT):
   v=lnt_sign(c)
   $! '$P' if v>0 $&('*',-1,'$P')
  if al==0:
   $! c
  v=$X(c)
  $! '$P' if v>0 $&('*',-1,'$P')
 $5($m,$S,$E,$T,TypeError,$a):
  pass
 r=lim_lh(g,$;+1)
 if r is $# $* $;<3:
  r=lim_log(g,$;+1)
 $! r
$, lim_lh(g,$;):
 if $;>4:
  $! $#
 if $8(g,TV):
  $! g
 h=head(g)
 if h=='^' $* $- $8(g[2],TV):
  L=lim_val($<(g[2],fn('ln',g[1])),$;)
  if L is $#:
   $! $#
  $! pw('e',L)
 if h=='^' $* $F(g[2]):
  L=lim_val(g[1],$;)
  if L is $#:
   $! $#
  if L==0 $* $`(g[2])<0:
   $! '$P'
  $! pw(L,g[2])
 if h=='*':
  nu,de=numer_denom(g)
  if de!=1:
   ln_=lim_val(nu,$;)
   ld=lim_val(de,$;)
   if ln_ is $# or ld is $#:
    $! $#
   if(ln_==0 $* ld==0)or(isinfv(ln_)$* isinfv(ld)):
    $! lim_val($.($U(diff(nu,TV),diff(de,TV))),$;)
   if ld==0:
    s=$X($W(de,TV,1e-9))
    sn=$X(ln_)if $4(ln_)$* $- isinfv(ln_)$&(1 if ln_=='$P' $&-1)
    $! '$P' if(s.$R if $/(s)is $3 $& s)*(sn.$R if $/(sn)is $3 $& sn)>0 $&('*',-1,'$P')
   $! $U(ln_,ld)
  ls=[lim_val(fct,$;)$) fct in g[1:]]
  if $# in ls:
   $! $#
  zero=[i $) i in $+($1(ls))if ls[i]==0]
  infs=[i $) i in $+($1(ls))if isinfv(ls[i])]
  if zero $* infs:
   r=lim_log(g,$;+1)
   if r is $- $#:
    $! r
   i=zero[0]
   j=infs[0]
   $f=$I([g[k+1]$) k in $+($1(ls))if k!=i $* k!=j])
   q=$U(g[i+1],pw(g[j+1],-1))
   r=lim_val(q,$;)
   if r is $#:
    $! $#
   $! $<(r,lim_val($f,$;))
  $! $I(ls)
 if h=='+':
  ls=[lim_val(t,$;)$) t in g[1:]]
  if $# in ls:
   $! $#
  r=$=(ls)
  if r!='$H':
   $! r
  ii=[k $) k in $+($1(ls))if isinfv(ls[k])]
  if $- ii:
   $! $#
  $) i in ii:
   A=g[i+1]
   $f=$=([g[k+1]$) k in $+($1(ls))if k!=i])
   q=lim_val($.($U($f,A)),$;)
   if q is $# or q=='$H' or isinfv(q)or q==-1:
    $6
   $! $<(ls[i],$^(1,q))
  $! $#
 if $/(g)is $0 $* $1(g)==2:
  L=lim_val(g[1],$;)
  if L is $#:
   $! $#
  $! fn(h,L)
 $! $#
$, isinfv(v):
 $! v=='$P' or v==('*',-1,'$P')
$, lim_num(g,a):
 ${:
  $c=[]
  $) k in $+(4,9):
   t=10.0**(-k)
   $c.$%($X(g,{TV:t}))
  v1=$c[-1]
  v2=$c[-2]
  if $/(v1)is $3 or $/(v2)is $3:
   $!('$z',g)
  if $J(v1)>1e12 $* $J(v1)>$J(v2):
   $! '$P' if v1>0 $&('*',-1,'$P')
  if $J(v1)<1e-6 $* $J(v1)<$J($c[-3])$* $J(v2)<$J($c[-3]):
   $! 0
  if $J(v1-v2)<1e-6*(1+$J(v1)):
   $! exactify_guess(v1)
 $5 $7:
  pass
 $!('$z',g)
$, exactify_guess(v):
 r=float2rat(v,1e-9)
 n,d=nd(r)
 if d<1000:
  $! r
 $! v
$, series_at(f,x,a,order):
 if a=='$P' or a==('*',-1,'$P'):
  sub_=pw(TV,-1)if a=='$P' $& $l(pw(TV,-1))
  back=pw(x,-1)if a=='$P' $& $l(pw(x,-1))
 $&:
  sub_=$^(a,TV)
  back=$](x,a)
 g=$W(f,x,sub_)
 S=series_t(g,order)
 $! S,back
$, taylor(f,x,n,a=0):
 ${:
  S,back=series_at(f,x,a,n)
 $5($m,$S,$E,$T):
  $! taylor_d(f,x,n,a)
 $Q=[]
 $) k in S[0]:
  if ncmp(k,n)>0:
   $6
  if $-($/(k)is $s $* k>=0)or has(S[0][k],LNT):
   $!('taylor',f,x,n,a)
  $Q.$%($<(S[0][k],pw(back,k)))
 $! $=($Q)
$, taylor_d(f,x,n,a):
 $Q=[]
 g=f
 fact=1
 $) k in $+(n+1):
  if k:
   fact*=k
   g=diff(g,x)
  v=$W(g,x,a)
  if has(v,'$H')or v=='$H' or has(v,'$P'):
   $!('taylor',f,x,n,a)
  $Q.$%($<($U(v,fact),pw($](x,a),k)))
 $! $=($Q)
$, series_cmd(f,x,n,a=0):
 ${:
  S,back=series_at(f,x,a,n)
 $5($m,$S,$E,$T):
  $!('series',f,x,n,a)
 $Q=[]
 lnback=fn('ln',back)if $-(a=='$P' or a==('*',-1,'$P'))$& $l(fn('ln',fn('$J',x)))
 $) k in S[0]:
  if ncmp(k,n)>0:
   $6
  c=$W(S[0][k],LNT,lnback)
  $Q.$%($<(c,pw(back,k)))
 $! $=($Q)
''')
_x(r'''$, dominant(f,x,a=0):
 if a=='$P' or a==('*',-1,'$P'):
  sub_=pw(TV,-1)if a=='$P' $& $l(pw(TV,-1))
  back=pw(x,-1)if a=='$P' $& $l(pw(x,-1))
  lnback=$l(fn('ln',fn('$J',x)))
 $&:
  sub_=$^(a,TV)
  back=$](x,a)
  lnback=fn('ln',back)
 ${:
  r=lead_t($W(f,x,sub_))
 $5($m,$S,$E,$T):
  $!('dominantterm',f,x,a)
 if r is $#:
  $! 0
 k,c=r
 $! $<($W(c,LNT,lnback),pw(back,k))
$, bern(n):
 B=[1]
 $) m in $+(1,n+1):
  s=0
  c=1
  $) k in $+(m):
   s=nadd(s,nmul(binom(m+1,k),B[k]))
  B.$%(nneg(ndiv(s,m+1)))
 $! B
$, binom(n,k):
 if k<0 or k>n:
  $! 0
 r=1
 $) i in $+(1,k+1):
  r=r*(n-k+i)//i
 $! r
$, powsum(j,n):
 B=bern(j)
 if j>=1:
  B[1]=Q(1,2)
 $Q=[]
 $) i in $+(j+1):
  $Q.$%($<(binom(j+1,i),B[i],pw(n,j+1-i)))
 $! $<(Q(1,j+1),$=($Q))
ZETA={2:('Q',1,6),4:('Q',1,90),6:('Q',1,945),8:('Q',1,9450),10:('Q',1,93555)}
$, sumseq(f,k,a,b):
 if $n(a)$* $n(b):
  if b<a-1:
   $! $l(sumseq(f,k,b+1,a-1))
  if b-a<=300:
   $Q=[$W(f,k,j)$) j in $+(a,b+1)]
   $! $=($Q)
 if $8(f,k):
  $! $<(f,$^($](b,a),1))
 cs_=$Z(f,k)
 if cs_ is $- $# $* b!='$P':
  res=[]
  $) j in $+($1(cs_)):
   if cs_[j]!=0:
    if j==0:
     res.$%($<(cs_[0],$^($](b,a),1)))
    $&:
     res.$%($<(cs_[j],$](powsum(j,b),powsum(j,$](a,1)))))
  $! $?($=(res))
 r=geomsum(f,k,a,b)
 if r is $- $#:
  $! r
 r=telesum(f,k,a,b)
 if r is $- $#:
  $! r
 if b=='$P' $* $n(a)$* has(f,('fact',k)):
  g=$<(f,('fact',k))
  gs=geomsum(g,k,0,'$P')if $2 $& $#
  cr=expsum(g,k)
  if cr is $- $#:
   C,r=cr
   tot=$<(C,pw('e',r))
   if a>0:
    tot=$](tot,$=([$<(C,$U(pw(r,j),fact_(j)))$) j in $+(a)]))
   $! tot
 if b=='$P' $* $n(a):
  nu,de=numer_denom(f)
  if $8(nu,k):
   dd=$Z(de,k)
   if dd is $- $# $* $1(dd)>=2 $* all([c==0 $) c in dd[:-1]]):
    p=$1(dd)-1
    if p==1:
     $! '$P' if $X($U(nu,dd[-1])).$R>0 $&('*',-1,'$P')
    if p in ZETA $* a>=1:
     z=$<(ZETA[p],pw('pi',p))
     z=$](z,$=([pw(j,-p)$) j in $+(1,a)]))
     $! $<($U(nu,dd[-1]),z)
 if($n(a)or $4(a))$*(b=='$P' or $n(b))$* freeofall(f,[s $) s in $g(f)if s!=k]):
  $! nsum(f,k,a,b)
 $!('sumseq',f,k,a,b)
$, expsum(g,k):
 if $8(g,k):
  $! g,1
 fs=g[1:]if $((g,'*')$&(g,)
 C=[]
 r=$#
 $) h in fs:
  if $8(h,k):
   C.$%(h)
  $@ $((h,'^')$* $8(h[1],k)$* h[2]==k $* r is $#:
   r=h[1]
  $@ $((h,'^')$* $8(h[1],k)$* $i(h[2],k)$* $i(h[2],k)[1]==0 $* r is $#:
   r=pw(h[1],$i(h[2],k)[0])
  $&:
   $! $#
 if r is $#:
  $! $#
 $! $I(C),r
$, geomsum(f,k,a,b):
 fs=f[1:]if $((f,'*')$&(f,)
 C=[]
 base=$#
 ex=$#
 $) g in fs:
  if $8(g,k):
   C.$%(g)
  $@ $((g,'^')$* $8(g[1],k)$* $i(g[2],k):
   if base is $- $#:
    if g[1]==base or($F(g[1])$* $F(base)):
     lp=$i(g[2],k)
     lb=$i(ex,k)
     if lp[0]==1 $* lb[0]==1:
      C.$%(pw(g[1],lp[1]))
      C.$%(pw(base,lb[1]))
      base=$<(base,g[1])
      ex=k
      $6
    $! $#
   base=g[1]
   ex=g[2]
  $&:
   $! $#
 if base is $#:
  $! $#
 p,q=$i(ex,k)
 r=pw(base,p)
 Cq=$<($I(C),pw(base,q))
 if b=='$P':
  if $4(r):
   v=$X(r)
   if $J(v)<1:
    $! $U($<(Cq,pw(r,a)),$](1,r))
   $! '$P' if $X(Cq).$R>0 $* v.$R>0 $& '$H'
  $! $#
 if r==1:
  $! $<(Cq,$^($](b,a),1))
 $! $U($<(Cq,$](pw(r,$^(b,1)),pw(r,a))),$](r,1))
$, telesum(f,k,a,b):
 if $- hasdenom(f):
  $! $#
 pf=partfrac(f,k)
 if pf is $#:
  $! $#
 $Q=pf[1:]if $((pf,'+')$&(pf,)
 groups=[]
 $) t in $Q:
  c,r=$b(t)
  if $((r,'^')$* r[2]==-1:
   lb=$i(r[1],k)
   if lb is $# or lb[0]!=1:
    $! $#
   groups.$%((c,lb[1]))
  $@ $8(t,k):
   $! $#
  $&:
   $! $#
 if $- groups:
  $! $#
 s0=groups[0][1]
 tot=0
 ms=[]
 $) c,s in groups:
  m=nsub(s,s0)if $u(s)$* $u(s0)$& $#
  if m is $# or $- $n(m):
   $! $#
  ms.$%(m)
  tot=$^(tot,c)
 if tot!=0:
  if b=='$P':
   $! '$P'
  $! $#
 mn=min(ms)
 if mn!=0:
  s0=nadd(s0,mn)
  ms=[m-mn $) m in ms]
 M=max(ms)
 res=[]
 $) idx in $+($1(groups)):
  c=groups[idx][0]
  m=ms[idx]
  part=[]
  $) j in $+(m,M):
   part.$%(pw($^(a,j,s0),-1))
  if b!='$P':
   $) j in $+(1,m+1):
    part.$%(pw($^(b,j,s0),-1))
  res.$%($<(c,$=(part)))
 $! $=(res)
$, nsum(f,k,a,b):
 av=$s(nreal(a))
 if b=='$P':
  $! nsum_inf(f,k,av)
 s=0.0
 $) n in $+(av,$s(b)+1):
  s+=$X(f,{k:$D(n)})
 $! s
''')
_x(r'''$, nsum_inf(f,k,av):
 L=$z(f,k,'$P')
 if L!=0 $* $- $((L,'$z'):
  if L=='$H' or $- $4(L):
   $! '$H'
  ${:
   v=fv_(L)
  $5 $7:
   $! '$H'
  $! '$P' if v>0 $&('*',-1,'$P')
 $, t(n):
  z=$X(f,{k:$D(n)})
  if $/(z)is $3:
   if $J(z.imag)>1e-12*(1+$J(z.$R)):
    $k $T
   z=z.$R
  $! z
 first=[t(n)$) n in $+(av,av+40)]
 tail=first[10:]
 if all([tail[i]*tail[i+1]<0 $) i in $+($1(tail)-1)]):
  S=[]
  s_=0.0
  $) n in $+(av,av+60):
   s_+=t(n)
   S.$%(s_)
  e1=wynn(S)
  e2=wynn(S[:-10])
  if $J(e1-e2)>1e-8*max(1.0,$J(e1)):
   err('Questionable accuracy: the series may diverge')
  $! e1
 N=av+200
 tn=[t(n)$) n in $+(N,N+20)]
 if all([v>0 $) v in tn])or all([v<0 $) v in tn]):
  ${:
   fe=exactify(f)
  $5 $7:
   fe=f
  I=defint(fe,k,N,'$P')
  if I in('$P',('*',-1,'$P')):
   $! I
  if $- $4(I)or has(I,'$H'):
   I=nint(f,k,N,'$P')
  s_=0.0
  $) n in $+(av,N):
   s_+=t(n)
  d1=diff(f,k)
  d3=diff(diff(d1,k),k)
  s_+=fv_(I)+t(N)/2-fv_($W(d1,k,N))/12+fv_($W(d3,k,N))/720
  $! s_
 s_=0.0
 prev=$#
 $) n in $+(av,av+20000):
  s_+=t(n)
  if n-av in(9999,19999):
   if prev is $- $# $* $J(s_-prev)>1e-9*max(1.0,$J(s_)):
    err('Questionable accuracy: the series may diverge')
   prev=s_
 $! s_
$, prodseq(f,k,a,b):
 if $n(a)$* $n(b):
  if b<a-1:
   $! pw(prodseq(f,k,b+1,a-1),-1)
  if b-a<=300:
   $! $I([$W(f,k,j)$) j in $+(a,b+1)])
 if $8(f,k):
  $! pw(f,$^($](b,a),1))
 if f==k $* a==1:
  $! fn('fact',b)
 if $((f,'^')$* f[1]==k $* $n(f[2])$* a==1:
  $! pw(fn('fact',b),f[2])
 if $((f,'*')$* a==1:
  c=[g $) g in f[1:]if $8(g,k)]
  r=[g $) g in f[1:]if $- $8(g,k)]
  if c $* $1(r)==1:
   rr=prodseq(r[0],k,a,b)
   if $- $((rr,'prodseq'):
    $! $<(pw($I(c),b),rr)
 fs=f[1:]if $((f,'*')$&(f,)
 if $((f,'^')$* $8(f[1],k):
  $! pw(f[1],sumseq(f[2],k,a,b))
 $!('prodseq',f,k,a,b)
$, texpand(e):
 if $/(e)is $- $0 or e[0]=='Q':
  $! e
 $M=[texpand(a)$) a in e[1:]]
 e=simp((e[0],)+$0($M))
 if $/(e)is $- $0:
  $! e
 h=e[0]
 if h in('sin','cos','tan')$* $1(e)==2:
  u=e[1]
  if h=='tan':
   $! texpand($U(fn('sin',u),fn('cos',u)))
  if $((u,'+'):
   a=u[1]
   b=$=($K(u[2:]))
   sa,ca=texpand(fn('sin',a)),texpand(fn('cos',a))
   sb,cb=texpand(fn('sin',b)),texpand(fn('cos',b))
   if h=='sin':
    $! $?($^($<(sa,cb),$<(ca,sb)))
   $! $?($]($<(ca,cb),$<(sa,sb)))
  c,r=$b(u)
  if $n(c)$* c>1 $* c<=30:
   s1=texpand(fn('sin',r))
   c1=texpand(fn('cos',r))
   z=expand_pow($^(c1,$<('i',s1)),c)
   re_,im_=reim(z)
   $! $?(im_ if h=='sin' $& re_)
 $! e
$, trigfactor(f):
 if head(f)in('sin','cos')$* $1(f)==2:
  $![(f[0],f[1])]
 if $((f,'^')$* head(f[1])in('sin','cos')$* $n(f[2])$* f[2]>0:
  $![(f[1][0],f[1][1])]*f[2]
 $! $#
$, tmul(a,b):
 n1,u=a
 n2,v=b
 if n1=='sin' $* n2=='sin':
  $! $<($v,$](fn('cos',$](u,v)),fn('cos',$^(u,v))))
 if n1=='cos' $* n2=='cos':
  $! $<($v,$^(fn('cos',$](u,v)),fn('cos',$^(u,v))))
 if n1=='cos':
  u,v=v,u
 $! $<($v,$^(fn('sin',$^(u,v)),fn('sin',$](u,v))))
$, tcollect(e):
 if $/(e)is $- $0 or e[0]=='Q':
  $! e
 e=$?(e)
 if $((e,'+'):
  $! $=([tcollect_term(t)$) t in e[1:]])
 $! tcollect_term(e)
$, tcollect_term(t):
 fs=t[1:]if $((t,'*')$&(t,)
 other=[]
 trig=[]
 $) f in fs:
  tf=trigfactor(f)
  if tf is $#:
   other.$%(f)
  $&:
   trig.$}(tf)
 if $1(trig)<=1:
  $! t
 acc=fn(trig[0][0],trig[0][1])
 $) tf in trig[1:]:
  $Q=acc[1:]if $((acc,'+')$&(acc,)
  $9=[]
  $) term in $Q:
   c,r=$b(term)
   ftf=trigfactor(r)
   if ftf is $# or $1(ftf)!=1:
    if freeof_trig(r):
     $9.$%($<(term,fn(tf[0],tf[1])))
     $6
    $9.$%($<(term,fn(tf[0],tf[1])))
    $6
   $9.$%($<(c,tmul(ftf[0],tf)))
  acc=$?($=($9))
 $! $?($<($I(other),acc))
$, trigargs(e,$9):
 if $/(e)is $- $0 or e[0]=='Q':
  $!
 if e[0]in('sin','cos')$* $1(e)==2:
  if e[1]$- in $9:
   $9.$%(e[1])
 $) a in e[1:]:
  trigargs(a,$9)
$, pyth(e):
 us=[]
 trigargs(e,us)
 if $- us:
  $! e
 best=e
 bl=$1(fmt(e))
 $) u in us:
  s=fn('sin',u)
  c=fn('cos',u)
  $) a,b in((s,c),(c,s)):
   g=rsquare(e,a,b)
   if g is $- $#:
    g=$?(g)
    l=$1(fmt(g))
    if l<bl:
     best=g
     bl=l
 $! best
$, rsquare(e,a,b):
 if $/(e)is $- $0 or e[0]=='Q':
  $! e
 if e[0]=='^' $* e[1]==a $* $n(e[2])$* e[2]>=2:
  $! $<(pw(a,e[2]-2),$](1,pw(b,2)))
 $! simp((e[0],)+$0(rsquare(t,a,b)$) t in e[1:]))
$, freeof_trig(e):
 $! $- hastrig(e)
$, arclen(f,x,a,b):
 g=$.($?($^(1,pw(diff(f,x),2))))
 $! defint($N(g),x,a,b)
$, tangentline(f,x,a):
 d=$W(diff(f,x),x,a)
 $! $?($^($W(f,x,a),$<(d,$](x,a))))
$, normalline(f,x,a):
 d=$W(diff(f,x),x,a)
 if d==0:
  $!('=',x,a)
 $! $?($]($W(f,x,a),$U($](x,a),d)))
$, impdif(eq,x,y,n=1):
 F=$](eq[1],eq[2])if $((eq,'=')$& eq
 yp=$.($l($U(diff(F,x),diff(F,y))))
 d=yp
 $) _ in $+(n-1):
  d=$.($^(diff(d,x),$<(diff(d,y),yp)))
 $! nice(d)
$, avgrc(f,x,v,h=Q(1,1000)):
 $! $U($]($W(f,x,$^(v,h)),$W(f,x,v)),h)
$, centraldiff(f,x,v,h=Q(1,1000)):
 $! $U($]($W(f,x,$^(v,h)),$W(f,x,$](v,h))),$<(2,h))
$, untan(e):
 if $/(e)is $- $0 or e[0]=='Q':
  $! e
 $M=[untan(a)$) a in e[1:]]
 if e[0]=='tan' $* $1($M)==1:
  $! $U(fn('sin',$M[0]),fn('cos',$M[0]))
 $! simp((e[0],)+$0($M))
$, pyth_to(e,which):
 other='cos' if which=='sin' $& 'sin'
 e=untan(e)
 us=[]
 trigargs(e,us)
 $) u in us:
  e=rsquare(e,fn(other,u),fn(which,u))
 $! $?(e)
''')
_x(r'''$, unhold(e):
 if $((e,'hold'):
  $! simp(e[1])
 $! e
$, $x(e):
 if $- $4(e):
  $! $2
 ${:
  v=$X(e)
 $5 $7:
  $! $2
 if $/(v)is $3:
  $! $J(v.imag)<=1e-10*(1+$J(v.$R))
 $! v==v
$, fv(e):
 v=$X(e)
 if $/(v)is $3:
  $! v.$R
 $! v
$, clean(e):
 e=$.(e)
 if $_(e):
  e=evalf(e)
  if has(e,'i'):
   r,i=reim(e)
   if $/(i)is $D $* $J(i)<1e-11*(1+$J(tofl(r)if $F(r)$& 1)):
    e=r
 $! e
class Sols:
 $, __init__($>):
  $>.$c=[]
  $>.all=$2
  $>.fail=$2
  $>.ints=[]
$, $o(f,x,$C=$2,$;=0):
 if $;>6:
  $! $#
 f=$.(unhold(f))
 if $8(f,x):
  if f==0:
   $! 'all'
  if $4(f)or $- $C:
   $![]
  $![]
 nu=numer_of(f)
 if $8(nu,x):
  $![]if nu!=0 $& 'all'
 if $- $C $* firstabs(nu,x)is $- $# $* $;<4:
  r=abs_cases(nu,x,[],$;)
  if r is $- $# $* r!='interval':
   $![q $) q in r if valid(f,x,q,$C)]
 $h=solve_num(nu,x,$C,$;)
 numeric=$h is $# or($h!='all' $* any([$_(q)$) q in $h]))
 if numeric $* hastrigx(nu,x)$* $;<3:
  ${:
   g=tcollect(nu)
  $5 $7:
   g=nu
  if g!=nu:
   s2=$o(g,x,$C,$;+2)
   if s2 is $- $# $* s2!='all' $* $- any([$_(q)$) q in s2]):
    $h=s2
 if $h is $# or $h=='all':
  $! $h
 $9=[]
 $) s in $h:
  if valid(f,x,s,$C):
   $9.$%(s)
 $! $9
$, numer_of(f):
 ${:
  c=comdenom(f)
 $5 $7:
  c=f
 $! numer_denom(c)[0]
$, valid(f,x,s,$C):
 if has(s,'n1')or $g(s)$* $- $4(s):
  $! $A
 ${:
  v=$W(f,x,s)
  if v=='$H' or has(v,'$H'):
   $! $2
  if has(v,'$P'):
   $! $2
  vv=$X(v)
  mag=1.0
  if $/(vv)is $3:
   ok=$J(vv)<1e-6
  $&:
   ok=$J(vv)<1e-6
  if $- ok:
   ${:
    sc=$X(s)
    ok=$J(vv)<1e-8*(1+$J(sc))*1e4
   $5 $7:
    ok=$2
  if $- $C:
   sv=$X(s)
   if $/(sv)is $3 $* $J(sv.imag)>1e-9*(1+$J(sv.$R)):
    $! $2
  $! ok
 $5($S,$E,$T,TypeError,$a):
  $! $2
$, solve_num(nu,x,$C,$;):
 d=degree(nu,x)
 if d is $- $#:
  r=solve_poly(nu,x,$C)
  if r is $- $#:
   $! r
 fac=factor_expr(nu)
 fac=fac[1]if $((fac,'hold')$& fac
 if $((fac,'*'):
  allsol=[]
  $) g in fac[1:]:
   if $((g,'^')$* $F(g[2])$* $`(g[2])>0:
    g=g[1]
   if $8(g,x):
    $6
   r=$o(g,x,$C,$;+1)
   if r is $#:
    $! numeric_solve(nu,x,$C)
   if r=='all':
    $! 'all'
   allsol.$}(r)
  $! dedup(allsol)
 if $((fac,'^')$* $F(fac[2])$* $`(fac[2])>0:
  $! $o(fac[1],x,$C,$;+1)
 r=isolate(nu,0,x,$C,$;)
 if r is $- $#:
  $! r
 r=radical_solve(nu,x,$C,$;)
 if r is $- $#:
  $! r
 r=explog_solve(nu,x,$C,$;)
 if r is $- $#:
  $! r
 r=ln_solve(nu,x,$C,$;)
 if r is $- $#:
  $! r
 r=kernel_solve(nu,x,$C,$;)
 if r is $- $#:
  $! r
 if hastrigx(nu,x):
  g=texpand(nu)
  if g!=nu:
   r=kernel_solve(g,x,$C,$;+1)
   if r is $#:
    fg=factor_expr(g)
    fg=fg[1]if $((fg,'hold')$& fg
    if $((fg,'*'):
     $! solve_num(g,x,$C,$;+1)
   if r is $- $#:
    $! r
  r=trig_lin(nu,x,$C)
  if r is $- $#:
   $! r
 $! numeric_solve(nu,x,$C)
$, radical_solve(nu,x,$C,$;):
 ks=[]
 xkernels(nu,x,ks)
 if $- ks:
  $! $#
 $) k in ks:
  if $-($((k,'^')$* isq(k[2])$* k[2][1]==1):
   $! $#
 if $1(ks)>1:
  if $;>4 or $1(ks)>3:
   $! $#
  $) k in ks:
   if k[2]!=$v:
    $! $#
  k=ks[0]
  W='W_'
  g=$?($W(nu,k,W))
  cs_=$Z(g,W)
  if cs_ is $# or $1(cs_)!=2:
   $! $#
  A,B=cs_
  g2=$?($](pw(A,2),$<(pw(B,2),k[1])))
  rs=$o(g2,x,$C,$;+1)
  if rs is $# or rs=='all':
   $! $#
  $![r $) r in rs if valid(nu,x,r,$C)]
 k=ks[0]
 base=k[1]
 q=k[2][2]
 W='W_'
 g=$?($W(nu,k,W))
 cs_=$Z(g,W)
 if cs_ is $# or $1(cs_)!=2 or has(cs_[0],W):
  $! $#
 A,B=cs_
 if degree(A,x)is $# or degree(B,x)is $# or degree(base,x)is $#:
  $! $#
 poly=$?($](pw($l(A),q),$<(pw(B,q),base)))
 rs=solve_poly(poly,x,$C)
 if rs is $# or rs=='all':
  $! $#
 $9=[]
 $) r in rs:
  if valid(nu,x,r,$C):
   $9.$%(r)
 $! $9
$, expterm(t,x):
 fs=t[1:]if $((t,'*')$&(t,)
 c=[]
 L=[]
 $) f in fs:
  if $8(f,x):
   c.$%(f)
  $@ $((f,'^')$* $8(f[1],x)$* $i(f[2],x)is $- $# $* $x(f[1])$* fv(f[1])>0:
   L.$%($<(f[2],fn('ln',f[1]))if f[1]!='e' $& f[2])
  $&:
   $! $#
 $! $I(c),$=(L)
$, explog_solve(nu,x,$C,$;):
 if $- $((nu,'+'):
  $! $#
 dep=[t $) t in nu[1:]if $- $8(t,x)]
 ind=$=([t $) t in nu[1:]if $8(t,x)])
 if $1(dep)==2 $* ind==0:
  A=expterm(dep[0],x)
  B=expterm(dep[1],x)
  if A is $# or B is $#:
   $! $#
  r=$.($l($U(B[0],A[0])))
  if $x(r)$* fv(r)<=0 $* $- $C:
   $![]
  eq=$?($](A[1],$^(B[1],fn('ln',r))))
  lx=$i(eq,x)
  if lx is $#:
   $! $#
  $![nice($.($l($U(lx[1],lx[0]))))]
 $! $#
''')
_x(r'''$, ln_solve(nu,x,$C,$;):
 $Q=nu[1:]if $((nu,'+')$&(nu,)
 lns=[]
 $f=[]
 $) t in $Q:
  c,r=$b(t)
  if $((r,'log')$* $1(r)==3:
   c=$U(c,fn('ln',r[2]))
   r=('ln',r[1])
  if $((r,'ln')$* $u(c)$* $- $8(r,x):
   lns.$%((c,r[1]))
  $@ $8(t,x):
   $f.$%(t)
  $@ $((r,'ln')$* $4(c)$* $- $8(r,x):
   lns.$%((c,r[1]))
  $&:
   $! $#
 if $1(lns)<2 $* $-($1(lns)==1 $* $f):
  $! $#
 k=rest_k=$=($f)
 c0=lns[0][0]
 if all([c==c0 $) c,u in lns]):
  P=$I([u $) c,u in lns])
  rhs=pw('e',$.($l($U(rest_k,c0))))
 $@ all([$u(c)$) c,u in lns]):
  P=$I([pw(u,c)$) c,u in lns])
  rhs=pw('e',$l(rest_k))
 $&:
  $! $#
 rs=$o($](P,rhs),x,$C,$;+1)
 if rs is $# or rs=='all':
  $! rs
 $9=[]
 $) r in rs:
  if valid(nu,x,r,$C):
   $9.$%(r)
 $! $9
$, hastrigx(e,x):
 if $/(e)is $- $0 or e[0]=='Q':
  $! $2
 if e[0]in('sin','cos','tan')$* has(e,x):
  $! $A
 $) a in e[1:]:
  if hastrigx(a,x):
   $! $A
 $! $2
$, dedup($h):
 $9=[]
 $) s in $h:
  if s $- in $9:
   dup=$2
   $) t in $9:
    ${:
     if $4(s)$* $4(t)$* $J($X(s)-$X(t))<1e-12*(1+$J($X(s))):
      dup=$A
      $O
    $5 $7:
     pass
   if $- dup:
    $9.$%(s)
 $! $9
$, sortsols($h):
 $, key(s):
  t=s
  $) w in $g(s):
   if w[0]=='n' $* w[1:].isdigit():
    t=$W(t,w,0)
  ${:
   v=$X(t)
   if $/(v)is $3:
    $!(1,v.$R,v.imag,okey(s))
   $!(0,v,0.0,okey(s))
  $5 $7:
   $!(2,0.0,0.0,okey(s))
 $! sorted($h,key=key)
$, solve_poly(p,x,$C):
 cs=$Z(p,x)
 if cs is $#:
  $! $#
 $G cs $* cs[-1]==0:
  cs.pop()
 n=$1(cs)-1
 if n<=0:
  $![]if cs $* cs[0]!=0 $& 'all'
 $h=[]
 k=0
 $G cs[k]==0:
  k+=1
 if k:
  $h.$%(0)
  cs=cs[k:]
  n=$1(cs)-1
 if n==0:
  $! $h
 allrat=$A
 anyfl=$2
 $) c in cs:
  if $- $u(c):
   allrat=$2
  if $_(c):
   anyfl=$A
 if anyfl $* all([$4(c)$) c in cs]):
  $! $h+numroots(cs,$C)
 if allrat:
  cc,fs=ufactor(cs)
  $) g,m in fs:
   $h.$}(solve_small(g,x,$C))
  $! dedup($h)
 if n==1:
  $! $h+[$.($l($U(cs[0],cs[1])))]
 if n==2:
  $! $h+quad(cs[2],cs[1],cs[0],$C)
 fac=factor_expr(p,x)
 fac=fac[1]if $((fac,'hold')$& fac
 if $((fac,'*'):
  $) g in fac[1:]:
   if $((g,'^')$* $F(g[2]):
    g=g[1]
   if $8(g,x):
    $6
   dg=degree(g,x)
   if dg is $- $# $* dg<n:
    r=solve_poly(g,x,$C)
    if r is $#:
     $! $#
    $h.$}(r)
   $&:
    $! $#
  $! dedup($h)
 r=solve_binom(cs,x,$C)
 if r is $- $#:
  $! $h+r
 if all([$4(c)$) c in cs]):
  $! $h+numroots(cs,$C)
 $! $#
$, quad(a,b,c,$C):
 D=$.($?($]($<(b,b),$<(4,a,c))))
 if $x(D)$* $- $C:
  if fv(D)<0:
   $![]
 if D==0:
  $![$.($U($l(b),$<(2,a)))]
 s=$N(D)
 r1=$.($U($]($l(b),s),$<(2,a)))
 r2=$.($U($^($l(b),s),$<(2,a)))
 if $4(r1):
  r1=$?(r1)
  r2=$?(r2)
 $![r1,r2]
$, solve_small(g,x,$C):
 n=$1(g)-1
 if n==1:
  $![Q(-g[0],g[1])]
 if n==2:
  $! quad(g[2],g[1],g[0],$C)
 r=solve_binom(g,x,$C)
 if r is $- $#:
  $! r
 if n==3:
  r=cardano(g,$C)
  if r is $- $#:
   if $1(fmt(r[0]))<=32:
    $! r
 $! numroots(g,$C)
$, solve_binom(cs,x,$C):
 n=$1(cs)-1
 m=0
 $) i in $+(1,n+1):
  if cs[i]!=0:
   m=igcd(m,i)
 if m<=1:
  $! $#
 sub_cs=[cs[i]$) i in $+(0,n+1,m)]
 if $1(sub_cs)-1>2 $* $-($1([c $) c in sub_cs if c!=0])==2):
  $! $#
 u='U_'
 if $1(sub_cs)==2:
  roots_u=[$.($l($U(sub_cs[0],sub_cs[1])))]
 $&:
  roots_u=solve_poly(fromcoeffs(sub_cs,u),u,$C)
  if roots_u is $#:
   $! $#
 $9=[]
 $) r in roots_u:
  $9.$}(nthroots(r,m,$C))
 $! dedup($9)
$, nthroots(r,m,$C):
 if $- $C:
  if $x(r):
   v=fv(r)
   if m%2==1:
    if v<0:
     $![$l(pw($l(r),Q(1,m)))]
    $![pw(r,Q(1,m))]
   if v<0:
    $![]
   if v==0:
    $![0]
   rt=pw(r,Q(1,m))
   $![$l(rt),rt]
  if m%2==1:
   $![pw(r,Q(1,m))]
  rt=pw(r,Q(1,m))
  $![$l(rt),rt]
 if $4(r):
  v=$X(r)
  mod=fn('$J',r)
  ang=fn('$r',r)
  $9=[]
  $) k in $+(m):
   th=$U($^(ang,$<(2*k,'pi')),m)
   z=$<(pw(mod,Q(1,m)),$^(fn('cos',th),$<('i',fn('sin',th))))
   z=$?(z)
   $9.$%(z)
  $! $9
 rt=pw(r,Q(1,m))
 $![$<(rt,pw('e',$U($<(2*k,'i','pi'),m)))$) k in $+(m)]
$, cardano(g,$C):
 d,c,b,a=[Q(v)if $/(v)is $s $& v $) v in g]
 p=$U($]($<(3,a,c),$<(b,b)),$<(3,a,a))
 q=$U($^($<(2,pw(b,3)),$<(-9,a,b,c),$<(27,a,a,d)),$<(27,pw(a,3)))
 disc=$^($U(pw(q,2),4),$U(pw(p,3),27))
 if $- $u(disc)or $`(disc)<=0:
  $! $#
 s=$N(disc)
 u=$^($l($U(q,2)),s)
 v=$]($l($U(q,2)),s)
 $, cbrt(w):
  wv=fv(w)
  if wv<0:
   $! $l(pw($l(w),Q(1,3)))
  $! pw(w,Q(1,3))
 t=$^(cbrt(u),cbrt(v))
 root=$](t,$U(b,$<(3,a)))
 if $- $C:
  $![root]
 $![root]+[clean(r)$) r in numroots_after(g,root)]
$, numroots_after(g,root):
 rv=fv(root)
 rs=aberth(g)
 $![fromcomplex(z)$) z in rs if $J(z-rv)>1e-6]
$, numroots(cs,$C):
 rs=aberth([evalf(c)if $- $F(c)$& c $) c in cs])
 $9=[]
 $) z in rs:
  if $J(z.imag)<1e-9*(1+$J(z.$R)):
   $9.$%($D(z.$R))
  $@ $C:
   $9.$%(fromcomplex(z))
 $! $9
NC=[0]
$, newint():
 NC[0]+=1
 $! 'n'+$p(NC[0])
''')
_x(r'''$, isolate(lhs,rhs,x,$C,$;):
 if $;>12:
  $! $#
 if lhs==x:
  $![rhs]
 if $8(lhs,x):
  $! 'all' if $.($](lhs,rhs))==0 $&[]
 h=head(lhs)
 if h=='+':
  dep=[t $) t in lhs[1:]if $- $8(t,x)]
  ind=[t $) t in lhs[1:]if $8(t,x)]
  if $1(dep)==1:
   $! isolate(dep[0],$](rhs,$=(ind)),x,$C,$;+1)
  $! $#
 if h=='*':
  dep=[t $) t in lhs[1:]if $- $8(t,x)]
  ind=[t $) t in lhs[1:]if $8(t,x)]
  if $1(dep)==1:
   c=$I(ind)
   r=$U(rhs,c)
   if $4(c)$* $((rhs,'+'):
    r=$?(r)
   $! isolate(dep[0],r,x,$C,$;+1)
  $! $#
 if h=='^':
  b,p=lhs[1],lhs[2]
  if $8(p,x):
   if p==-1 or($F(p)$* $`(p)<0):
    if rhs==0:
     $![]
    $! isolate(pw(b,nneg(p)),pw(rhs,-1),x,$C,$;+1)
   if $/(p)is $s:
    $9=[]
    $) r in nthroots(rhs,p,$C):
     rr=isolate(b,r,x,$C,$;+1)
     if rr is $#:
      $! $#
     if rr=='all':
      $! 'all'
     $9.$}(rr)
    $! $9
   if isq(p):
    pn,pd=p[1],p[2]
    if pd%2==0 $* $- $C $* $x(rhs)$* fv(rhs)<0:
     $![]
    $! isolate(pw(b,pn),pw(rhs,pd),x,$C,$;+1)
   $! isolate(b,pw(rhs,pw(p,-1)),x,$C,$;+1)
  if $8(b,x):
   if rhs==0:
    $![]
   if $- $C $* $x(rhs)$* fv(rhs)<0 $* $x(b)$* fv(b)>0:
    $![]
   if b=='e':
    $! isolate(p,fn('ln',rhs),x,$C,$;+1)
   if $F(b)$* $4(rhs):
    $! isolate(p,fn('log',rhs,b),x,$C,$;+1)
   $! isolate(p,$U(fn('ln',rhs),fn('ln',b)),x,$C,$;+1)
  $! $#
 if $/(lhs)is $0 $* $1(lhs)>=2:
  u=lhs[1]
  if $- all([$8(a,x)$) a in lhs[2:]]):
   $! $#
  rs=invfun(h,lhs,rhs,$C)
  if rs is $#:
   $! $#
  $9=[]
  $) r in rs:
   rr=isolate(u,r,x,$C,$;+1)
   if rr is $#:
    $! $#
   if rr=='all':
    $! 'all'
   $9.$}(rr)
  $! $9
 $! $#
$, invfun(h,lhs,r,$C):
 rv=$#
 if $x(r):
  rv=fv(r)
 if h=='ln':
  $![pw('e',r)]
 if h=='log':
  b=lhs[2]if $1(lhs)>2 $& 10
  $![pw(b,r)]
 if h=='$J':
  if rv is $- $#:
   if rv<0:
    $![]
   if rv==0:
    $![0]
  $![$l(r),r]
 if h=='$N':
  $![pw(r,2)]
 if h=='sin':
  if rv is $- $# $* $J(rv)>1 $* $- $C:
   $![]
  n=newint()
  if r==0:
   $![$<(n,'pi')]
  a=fn('$|',r)
  if r==1 or r==-1:
   $![$^(a,$<(2,n,'pi'))]
  $![$^(a,$<(2,n,'pi')),$^($]('pi',a),$<(2,n,'pi'))]
 if h=='cos':
  if rv is $- $# $* $J(rv)>1 $* $- $C:
   $![]
  n=newint()
  if r==0:
   $![$^($<($v,'pi'),$<(n,'pi'))]
  a=fn('arccos',r)
  if r==1 or r==-1:
   $![$^(a,$<(2,n,'pi'))]
  $![$^(a,$<(2,n,'pi')),$^($l(a),$<(2,n,'pi'))]
 if h=='tan':
  n=newint()
  $![$^(fn('$w',r),$<(n,'pi'))]
 if h=='$|':
  if rv is $- $# $* $J(rv)>$Y.pi/2+1e-12:
   $![]
  $![fn('sin',r)]
 if h=='arccos':
  if rv is $- $# $*(rv<-1e-12 or rv>$Y.pi+1e-12):
   $![]
  $![fn('cos',r)]
 if h=='$w':
  if rv is $- $# $* $J(rv)>=$Y.pi/2:
   $![]
  $![fn('tan',r)]
 if h=='sinh':
  $![fn('arcsinh',r)]
 if h=='cosh':
  if rv is $- $# $* rv<1:
   $![]
  a=fn('arccosh',r)
  $![$l(a),a]
 if h=='tanh':
  if rv is $- $# $* $J(rv)>=1:
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
 if $/(e)is $- $0 or e[0]=='Q' or $8(e,x):
  $!
 h=e[0]
 if h in('+','*'):
  $) a in e[1:]:
   xkernels(a,x,$9)
  $!
 if h=='^' $* $/(e[2])is $s:
  xkernels(e[1],x,$9)
  $!
 if h=='^' $* isq(e[2])$* e[1]==x:
  k=pw(x,Q(1,e[2][2]))
  if k $- in $9:
   $9.$%(k)
  $!
 if e $- in $9:
  $9.$%(e)
$, kernel_solve(nu,x,$C,$;):
 W='W_'
 g=nu
 exps=[]
 findexp(g,x,exps)
 if exps:
  base=exps[0][0]
  if all([b==base $) b,a,c in exps]):
   gg=0
   $) b,a,c in exps:
    gg=a if gg==0 $& rgcd(gg,a)
   if gg!=0:
    g2=repl_exp(g,x,base,gg,W)
    if $8(g2,x):
     rs=$o(g2,W,$C,$;+1)
     if rs is $# or rs=='all':
      $! rs
     $9=[]
     $) r in rs:
      rr=isolate(pw(base,$<(gg,x)),r,x,$C,$;+1)
      if rr is $#:
       $! $#
      $9.$}(rr)
     $! $9
 ks=[]
 xkernels(g,x,ks)
 if $1(ks)==1 $* ks[0]!=x:
  k=ks[0]
  g2=$W(g,k,W)
  if $8(g2,x):
   rs=$o(g2,W,$C,$;+1)
   if rs is $# or rs=='all':
    $! rs
   $9=[]
   $) r in rs:
    rr=isolate(k,r,x,$C,$;+1)
    if rr is $#:
     $! $#
    if rr=='all':
     $! 'all'
    $9.$}(rr)
   $! $9
 if $1(ks)==2:
  names=sorted([head(k)$) k in ks])
  if names==['cos','sin']$* ks[0][1]==ks[1][1]:
   u=ks[0][1]
   s=fn('sin',u)
   c=fn('cos',u)
   $) a,b in((c,s),(s,c)):
    g2=$?(g)
    cc=$Z($W(g2,a,W),W)
    if cc is $- $# $* all([cc[i]==0 $) i in $+(1,$1(cc),2)]):
     g3=$?($W($W(g2,a,W),W,$N($](1,pw(b,2)))))
     if $- has(g3,a):
      $! kernel_solve(g3,x,$C,$;+1)if $;<4 $& $#
 $! $#
$, rgcd(a,b):
 if $u(a)$* $u(b):
  an,ad=nd(a)
  bn,bd=nd(b)
  $! Q(igcd(an,bn),ilcm(ad,bd))
 $! a if a==b $& 0
$, findexp(e,x,$9):
 if $/(e)is $- $0 or e[0]=='Q':
  $!
 if e[0]=='^' $* $8(e[1],x)$* $- $8(e[2],x):
  l=$i(e[2],x)
  if l is $- $#:
   $9.$%((e[1],l[0],l[1]))
   $!
  $9.$%(($#,0,0))
  $!
 $) a in e[1:]:
  findexp(a,x,$9)
$, repl_exp(e,x,base,gg,W):
 if $/(e)is $- $0 or e[0]=='Q':
  $! e
 if e[0]=='^' $* e[1]==base $* $- $8(e[2],x):
  l=$i(e[2],x)
  if l is $- $#:
   $! $<(pw(base,l[1]),pw(W,$U(l[0],gg)))
 $! simp((e[0],)+$0(repl_exp(a,x,base,gg,W)$) a in e[1:]))
''')
_x(r'''$, trig_lin(nu,x,$C):
 ks=[]
 xkernels(nu,x,ks)
 if $1(ks)!=2:
  $! $#
 names=sorted([head(k)$) k in ks])
 if names!=['cos','sin']or ks[0][1]!=ks[1][1]:
  $! $#
 u=ks[0][1]
 S='S_'
 C='C_'
 g=$?($W($W(nu,fn('sin',u),S),fn('cos',u),C))
 if has(g,x):
  $! $#
 cs_s=$Z(g,S)
 if cs_s is $# or $1(cs_s)!=2:
  $! $#
 a=cs_s[1]
 $f=cs_s[0]
 cc=$Z($f,C)
 if cc is $# or $1(cc)!=2 or has(a,C):
  $! $#
 b=cc[1]
 c=cc[0]
 if c==0:
  $! isolate(fn('tan',u),$.($l($U(b,a))),x,$C,0)
 R=$N($^(pw(a,2),pw(b,2)))
 phi=fn('$w',$U(b,a))
 if $x(a)$* fv(a)<0:
  phi=$^(phi,'pi')
 $! isolate(fn('sin',$^(u,phi)),$.($l($U(c,R))),x,$C,0)
$, numeric_solve(f,x,$C,lo=$#,hi=$#,maxn=12):
 others=[s $) s in $g(f)if s!=x]
 if others:
  $! $#
 $, F(t):
  ${:
   v=$X(f,{x:t})
  $5($E,$T,$a,$S,TypeError):
   $! $#
  if $/(v)is $3:
   if $J(v.imag)>1e-9*(1+$J(v.$R)):
    $! $#
   v=v.$R
  if v!=v:
   $! $#
  $! v
 $, points():
  if lo is $- $# $* hi is $- $#:
   $) i in $+(401):
    yield lo+(hi-lo)*i/400
   $!
  big=[10**(k/10.0)$) k in $+(60,-41,-1)]
  $) v in big:
   if v>20:
    yield-v
  $) i in $+(-400,401):
   yield i*0.05
  $) v in reversed(big):
   if v>20:
    yield v
 roots=[]
 t0=a=$#
 t1=b=$#
 $) t2 in points():
  c=F(t2)
  if b is $- $# $* b==0:
   if(a is $- $# $* a!=0)or(c is $- $# $* c!=0):
    roots.$%(t1)
  if b is $- $# $* c is $- $# $* b!=0 $* c!=0 $*(b<0)!=(c<0):
   r=bisect(F,t1,t2,b,c)
   if r is $- $#:
    roots.$%(r)
  if(a is $- $# $* b is $- $# $* c is $- $# $* b!=0
 $* $J(b)<$J(a)$* $J(b)<$J(c)$*(a>0)==(b>0)==(c>0)$* $J(b)<1e-2):
   r=newton(F,t1)
   if r is $- $# $* t0<=r<=t2:
    roots.$%(r)
  t0,a=t1,b
  t1,b=t2,c
  if $1(roots)>200:
   $O
 if b is $- $# $* b==0 $* a is $- $# $* a!=0:
  roots.$%(t1)
 $9=[]
 $) r in sorted(roots):
  if $- $9 or $J(r-$9[-1])>1e-9*(1+$J(r)):
   $9.$%(r)
 if $1($9)>maxn $* lo is $#:
  $9.sort(key=$J)
  $9=sorted($9[:maxn])
 $![snap(r)$) r in $9]
$, snap(r):
 if $J(r-round(r))<1e-12:
  $! $D(round(r))
 $! r
$, bisect(F,a,b,fa,fb):
 $) _ in $+(200):
  m=0.5*(a+b)
  fm=F(m)
  if fm is $#:
   $! $#
  if fm==0 or $J(b-a)<1e-15*(1+$J(m)):
   $O
  if(fm<0)==(fa<0):
   a,fa=m,fm
  $&:
   b,fb=m,fm
 m=0.5*(a+b)
 fm=F(m)
 if fm is $# or $J(fm)>1e-6*(1+$J(fa)+$J(fb)):
  if fm is $- $# $* $J(fm)>1e3:
   $! $#
 $! m
$, newton(F,t):
 $) _ in $+(60):
  v=F(t)
  if v is $#:
   $! $#
  h=1e-7*(1+$J(t))
  v2=F(t+h)
  if v2 is $#:
   $! $#
  d=(v2-v)/h
  if d==0:
   $O
  t2=t-v/d
  if $J(t2-t)<1e-14*(1+$J(t)):
   t=t2
   $O
  t=t2
 v=F(t)
 if v is $- $# $* $J(v)<1e-9:
  $! t
 $! $#
$, nsolve(f,x,guess=$#,lo=$#,hi=$#):
 $, F(t):
  ${:
   v=$X(f,{x:t})
  $5($E,$T,$a,$S,TypeError):
   $! $#
  if $/(v)is $3:
   if $J(v.imag)>1e-9*(1+$J(v.$R)):
    $! $#
   v=v.$R
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
   rs=[r $) r in rs if r>=lo]
  if hi is $- $#:
   rs=[r $) r in rs if r<=hi]
 if rs:
  if guess is $- $#:
   rs.sort(key=$: r:$J(r-guess))
  $&:
   rs.sort(key=$: r:$J(r))
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
 if $- $4($W(f,x,0))or $- $4(diff(f,x)):
  r=ineq_param(rel,f,x)
  if r is $- $#:
   $! r
 $! solve_rels([(rel,f)],x)
$, rel_pairs(cs,x):
 $9=[]
 $) c in cs:
  h=head(c)
  if h=='$*':
   r=rel_pairs(c[1:],x)
   if r is $#:
    $! $#
   $9+=r
  $@ h in('<','>','<=','>=','/=','='):
   $9.$%((h,$.($](c[1],c[2]))))
  $&:
   $! $#
 $) rel,f in $9:
  if $- $8(f,x)$* fvars(f,x):
   $! $#
 $! $9
$, fvars(f,x):
 $! any(w!=x $* w $- in('pi','e','i','$P')$) w in $g(f))
''')
_x(r'''$, solve_rels(pairs,x,anyof=$2):
 pts=[]
 $) rel,f in pairs:
  if $8(f,x):
   $6
  rs=$o(f,x,$2)
  if rs is $#:
   $! $#
  if rs=='all':
   rs=[]
  $) r in rs:
   if $- $x(r):
    if $4(r):
     $6
    $! $#
   pts.$%(r)
  dens=[]
  domainpts(f,x,dens)
  $) d in dens:
   r2=$o(d,x,$2)
   if r2 is $# or r2=='all':
    $6
   $) r in r2:
    if $x(r):
     pts.$%(r)
    $@ $- $4(r):
     $! $#
 pts=sortsols(dedup(pts))
 $, ok1(rel,f,t):
  ${:
   v=$X(f,{x:t})
  $5 $7:
   $! $2
  if $/(v)is $3:
   if $J(v.imag)>1e-9*(1+$J(v.$R)):
    $! $2
   v=v.$R
  if v!=v:
   $! $2
  $! relok(rel,v)
 $, test(t):
  $) rel,f in pairs:
   if ok1(rel,f,t)==anyof:
    $! anyof
  $! $- anyof
 $, testp(p):
  if anyof:
   $) q in pairs:
    if testp1([q],p):
     $! $A
   $! $2
  $! testp1(pairs,p)
 $, testp1(pairs,p):
  $) rel,f in pairs:
   ${:
    v=$W(f,x,p)
    if v=='$H' or has(v,'$H')or has(v,'$P'):
     $! $2
    vv=$X(v)
    if $/(vv)is $3:
     if $J(vv.imag)>=1e-9:
      $! $2
     vv=vv.$R
    if $J(vv)<1e-10:
     vv=0.0
    if $- relok(rel,vv):
     $! $2
   $5 $7:
    $! $2
  $! $A
 $c=[fv(p)$) p in pts]
 if $- $c:
  $! 'true' if test(0.5)$& 'false'
 segs=[('I',$#,pts[0],test($c[0]-max(1.0,$J($c[0]))))]
 $) i in $+($1(pts)):
  p=pts[i]
  segs.$%(('P',p,p,testp(p)))
  if i+1<$1(pts):
   segs.$%(('I',p,pts[i+1],test(0.5*($c[i]+$c[i+1]))))
 segs.$%(('I',pts[-1],$#,test($c[-1]+max(1.0,$J($c[-1])))))
 $! segs_to_bool(segs,x)
$, sgn(e):
 if $4(e):
  ${:
   v=fv(e)
  $5 $7:
   $! 0
  $! 1 if v>0 $&(-1 if v<0 $& 0)
 if $((e,'*'):
  s=1
  $) a in e[1:]:
   k=sgn(a)
   if $- k:
    $! 0
   s*=k
  $! s
 if $((e,'+'):
  ks=[sgn(a)or(2 if nonneg(a)$& 0)$) a in e[1:]]
  if all(k in(1,2)$) k in ks)$* 1 in ks:
   $! 1
  ks=[sgn($l(a))or(2 if nonneg($l(a))$& 0)$) a in e[1:]]
  if all(k in(1,2)$) k in ks)$* 1 in ks:
   $!-1
  $! 0
 if $((e,'^')$* $n(e[2])$* e[2]%2==1:
  $! sgn(e[1])
 if head(e)=='exp' or($((e,'^')$* e[1]=='e'):
  $! 1
 $! 0
$, nonneg(e):
 if $((e,'^')$* $n(e[2])$* e[2]%2==0:
  $! $A
 if head(e)=='$J':
  $! $A
 if $((e,'*'):
  $! all(nonneg(a)or sgn(a)>0 $) a in e[1:])
 $! sgn(e)>0
$, ineq_param(rel,f,x):
 cs=$Z(f,x)
 if cs is $# or $1(cs)!=2:
  $! $#
 a=nice(comdenom(cs[1]))
 b=cs[0]
 v=nice(comdenom($U($l(b),a)))
 k=sgn(a)
 if k:
  $!(rel if k>0 $& FLIP[rel],x,v)
 n=numer_denom(a)[0]
 if rel=='/=':
  $9=[('$*',('/=',x,v),('/=',n,0))]
 $&:
  $9=[('$*',(rel,x,v),('>',a,0)),
 ('$*',(FLIP[rel],x,v),('<',a,0))]
 if $/(n)is $p:
  b=$W(b,n,0)
 if $4(b):
  if relok(rel,fv(b)):
   $9.$%(('=',n,0))
 $&:
  $9.$%(('$*',('=',n,0),(rel,b,0)))
 $!('or',)+$0($9)if $1($9)>1 $& $9[0]
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
 if $/(f)is $- $0 or f[0]=='Q':
  $!
 h=f[0]
 if h=='^' $* $- $8(f[1],x):
  if $F(f[2])$* $`(f[2])<0:
   $9.$%(f[1])
  if isq(f[2])$* f[2][2]%2==0:
   $9.$%(f[1])
 if h in('ln','log','$J','sign','floor','ceiling')$* $- $8(f[1],x):
  $9.$%(f[1])
 $) a in f[1:]:
  domainpts(a,x,$9)
$, segs_to_bool(segs,x):
 ivs=[]
 cur=$#
 $) kind,a,b,ok in segs:
  if ok:
   if cur is $#:
    if kind=='I':
     cur=[a,$2,b,$2]
    $&:
     cur=[a,$A,b,$A]
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
 if $1(ivs)>=2 $* ivs[0][0]is $# $* ivs[-1][2]is $#:
  okp=$A
  $) i in $+($1(ivs)-1):
   if $-(ivs[i][2]==ivs[i+1][0]$* $- ivs[i][3]$* $- ivs[i+1][1]):
    okp=$2
  if okp:
   ne=[('/=',x,ivs[i][2])$) i in $+($1(ivs)-1)]
   $! ne[0]if $1(ne)==1 $&('$*',)+$0(ne)
 $9=[]
 $) lo,li,hi,hiinc in ivs:
  if lo is $# $* hi is $#:
   $! 'true'
  if lo is $- $# $* hi is $- $# $* lo==hi:
   $9.$%(('=',x,lo))
  $@ lo is $#:
   $9.$%(('<=' if hiinc $& '<',x,hi))
  $@ hi is $#:
   $9.$%(('>=' if li $& '>',x,lo))
  $&:
   $9.$%(('$*',('<=' if li $& '<',lo,x),('<=' if hiinc $& '<',x,hi)))
 if $1($9)==1:
  $! $9[0]
 $!('or',)+$0($9)
$, eqexpr(eq):
 if $((eq,'='):
  $! $.($](eq[1],eq[2]))
 $! eq
$, is_linear_sys(fs,vs):
 $) f in fs:
  $) v in vs:
   d=degree(f,v)
   if d is $# or d>1:
    $! $2
  g=$?(f)
  $) i in $+($1(vs)):
   $) j in $+($1(vs)):
    cs_=$Z(g,vs[i])
    if cs_ is $#:
     $! $2
    if $1(cs_)>1 $* has(cs_[1],vs[j]):
     $! $2
 $! $A
''')
_x(r'''$, linsys(fs,vs):
 m=$1(fs)
 n=$1(vs)
 A=[]
 $) f in fs:
  g=$?(f)
  row=[]
  $f=g
  $) v in vs:
   cs_=$Z(g,v)
   c=cs_[1]if $1(cs_)>1 $& 0
   row.$%(c)
  const=g
  $) v in vs:
   const=$W(const,v,0)
  row.$%($l(const))
  A.$%(row)
 piv=[]
 r=0
 $) c in $+(n):
  p=$#
  $) i in $+(r,m):
   if $.(A[i][c])!=0:
    p=i
    $O
  if p is $#:
   $6
  A[r],A[p]=A[p],A[r]
  pv=A[r][c]
  A[r]=[$.($U(a,pv))$) a in A[r]]
  $) i in $+(m):
   if i!=r $* A[i][c]!=0:
    fct=A[i][c]
    A[i]=[$.($?($](A[i][j],$<(fct,A[r][j]))))$) j in $+(n+1)]
  piv.$%(c)
  r+=1
  if r==m:
   $O
 $) i in $+(r,m):
  if $.(A[i][n])!=0:
   $![]
 sol={}
 free=[c $) c in $+(n)if c $- in piv]
 params={}
 k=1
 $) c in free:
  params[vs[c]]='c'+$p(k)
  k+=1
 $) i in $+($1(piv)):
  c=piv[i]
  val=A[i][n]
  $) c2 in free:
   val=$](val,$<(A[i][c2],params[vs[c2]]))
  sol[vs[c]]=nice($.(val))
 $) c in free:
  sol[vs[c]]=params[vs[c]]
 $![sol]
$, solve_system(eqs,vs,$C=$2,guesses=$#):
 NC[0]=0
 fs=[]
 $) e in eqs:
  f=eqexpr(e)
  f=numer_of(f)if hasdenom_x(f,vs)$& f
  if f!=0:
   fs.$%(f)
 if guesses:
  $! newton_sys(fs,vs,guesses)
 if is_linear_sys(fs,vs):
  $! linsys(fs,vs)
 r=elim(fs,vs,$C,0)
 if r is $#:
  $! newton_sys(fs,vs,[0.0]*$1(vs))
 $9=[]
 $) s in r:
  ok=$A
  $) v in vs:
   if v $- in s:
    s[v]=v
  if $- $C:
   $) v in vs:
    if $4(s[v])$* $- $x(s[v]):
     ok=$2
  if ok $* s $- in $9:
   $9.$%(s)
 $! $9
$, hasdenom_x(f,vs):
 $) v in vs:
  nu,de=numer_denom(f)
  if has(de,v):
   $! $A
 $! $2
$, elim(fs,vs,$C,$;):
 fs=[$.($?(f))$) f in fs]
 fs=[f $) f in fs if f!=0]
 if $- fs:
  $![{}]
 $) f in fs:
  if freeofall(f,vs):
   if $4(f)or f!=0:
    $![]
 if $;>8:
  $! $#
 best=$#
 $) f in fs:
  inv=[v $) v in vs if has(f,v)]
  if $1(inv)==1:
   best=(f,inv[0])
   $O
 if best is $#:
  $) f in fs:
   $) v in vs:
    d=degree(f,v)
    if d==1:
     c=$Z(f,v)
     if c is $- $# $* $4(c[1])$* c[1]!=0:
      best=(f,v)
      $O
   if best:
    $O
 if best is $#:
  $) f in fs:
   $) v in vs:
    if degree(f,v)==1:
     best=(f,v)
     $O
   if best:
    $O
 if best is $- $#:
  f,v=best
  rs=$o(f,v,$C)
  if rs is $#:
   $! $#
  if rs=='all':
   rs=[]
  $9=[]
  $f=[g $) g in fs if g is $- f]
  ovs=[w $) w in vs if w!=v]
  $) r in rs:
   sub_=[$.($W(g,v,r))$) g in $f]
   rr=elim(sub_,ovs,$C,$;+1)
   if rr is $#:
    $! $#
   $) s in rr:
    s2=dict(s)
    val=r
    $) w in s2:
     val=$W(val,w,s2[w])
    s2[v]=clean(val)
    $9.$%(s2)
  $! $9
 if $1(fs)>=2 $* $1(vs)>=2:
  y=vs[-1]
  R=resultant(fs[0],fs[1],y)
  if R is $# or R==0:
   $! $#
  rr=elim([R]+fs[2:],vs[:-1],$C,$;+1)
  if rr is $#:
   $! $#
  $9=[]
  $) s in rr:
   gs=[]
   $) g in fs:
    h=g
    $) w in s:
     h=$W(h,w,s[w])
    gs.$%($.($?(h)))
   ys=elim(gs,[y],$C,$;+1)
   if ys is $#:
    $6
   $) t in ys:
    s2=dict(s)
    s2.update(t)
    $9.$%(s2)
  $! $9
 $! $#
$, resultant(f,g,y):
 a=$Z(f,y)
 b=$Z(g,y)
 if a is $# or b is $#:
  $! $#
 m=$1(a)-1
 n=$1(b)-1
 if m<1 or n<1:
  $! $#
 N=m+n
 M=[]
 $) i in $+(n):
  row=[0]*N
  $) j in $+(m+1):
   row[i+j]=a[m-j]
  M.$%(row)
 $) i in $+(m):
  row=[0]*N
  $) j in $+(n+1):
   row[i+j]=b[n-j]
  M.$%(row)
 $! $?(bareiss(M))
$, bareiss(M):
 n=$1(M)
 M=[$K(r)$) r in M]
 sign=1
 prev=1
 $) k in $+(n-1):
  if M[k][k]==0:
   sw=$#
   $) i in $+(k+1,n):
    if M[i][k]!=0:
     sw=i
     $O
   if sw is $#:
    $! 0
   M[k],M[sw]=M[sw],M[k]
   sign=-sign
  $) i in $+(k+1,n):
   $) j in $+(k+1,n):
    num=$?($]($<(M[i][j],M[k][k]),$<(M[i][k],M[k][j])))
    M[i][j]=exdiv(num,prev)
  prev=M[k][k]
 $! $<(sign,M[n-1][n-1])
$, exdiv(a,b):
 if b==1:
  $! a
 if $F(b):
  $! $?($<(a,ninv(b))if $u(b)$& $U(a,b))
 ks=[]
 kernels(a,ks)
 kernels(b,ks)
 sortkernels(ks)
 ra=ratform(a,ks)
 rb=ratform(b,ks)
 if ra is $# or rb is $#:
  $! $.($U(a,b))
 q=$V(p_mul(ra[0],rb[1]),p_mul(ra[1],rb[0]))
 if q is $#:
  $! $.($U(a,b))
 $! p2e(q,ks)
$, newton_sys(fs,vs,guess):
 n=$1(vs)
 if $1(fs)!=n:
  $! $#
 others=[]
 $) f in fs:
  $) s in $g(f):
   if s $- in vs:
    $! $#
 J=[[diff(f,v)$) v in vs]$) f in fs]
 xv=[$D($X(g).$R)if $F(g)or $4(g)$& 0.0 $) g in guess]
 $) it in $+(100):
  env=dict(zip(vs,xv))
  ${:
   F=[$X(f,env)$) f in fs]
   Jv=[[$X(J[i][j],env)$) j in $+(n)]$) i in $+(n)]
  $5 $7:
   $! $#
  F=[v.$R if $/(v)is $3 $& v $) v in F]
  Jv=[[v.$R if $/(v)is $3 $& v $) v in r]$) r in Jv]
  dx=linsolve_float(Jv,[-v $) v in F])
  if dx is $#:
   $! $#
  xv=[xv[i]+dx[i]$) i in $+(n)]
  if max([$J(d)$) d in dx])<1e-13*(1+max([$J(v)$) v in xv])):
   $O
 env=dict(zip(vs,xv))
 ${:
  if max([$J($X(f,env))$) f in fs])>1e-8:
   $![]
 $5 $7:
  $![]
 $![dict([(vs[i],snap(xv[i]))$) i in $+(n)])]
$, linsolve_float(A,b):
 n=$1(A)
 M=[$K(A[i])+[b[i]]$) i in $+(n)]
 $) c in $+(n):
  p=max($+(c,n),key=$: i:$J(M[i][c]))
  if $J(M[p][c])<1e-300:
   $! $#
  M[c],M[p]=M[p],M[c]
  $) i in $+(n):
   if i!=c:
    f=M[i][c]/M[c][c]
    $) j in $+(c,n+1):
     M[i][j]-=f*M[c][j]
 $![M[i][n]/M[i][i]$) i in $+(n)]
$, sols_to_bool(x,$h):
 if $h=='all':
  $! 'true'
 if $h is $#:
  $! $#
 if $- $h:
  $! 'false'
 eqs=[('=',x,s)$) s in $h]
 if $1(eqs)==1:
  $! eqs[0]
 $!('or',)+$0(eqs)
''')
_x(r'''$, apply_constraints($h,x,cons):
 if $- cons or $h=='all' or $h is $#:
  $! $h
 lo=$#
 hi=$#
 $9=[]
 expanded=[]
 $) s in $h:
  ns=[w $) w in $g(s)if w[0]=='n' $* w[1:].isdigit()]
  if ns $* $1(ns)==1:
   b=bounds(cons,x)
   if b is $#:
    expanded.$%(s)
    $6
   n=ns[0]
   $) k in $+(-60,61):
    v=$W(s,n,k)
    expanded.$%(v)
  $&:
   expanded.$%(s)
 $) s in expanded:
  if satisfies(s,x,cons):
   $9.$%(s)
 $! sortsols(dedup($9))
$, bounds(cons,x):
 lo=$#
 hi=$#
 $) c in cons:
  if head(c)in('<','<=','>','>=')$* $4(c[1])$* c[2]==x:
   if c[0]in('<','<='):
    lo=c[1]
   $&:
    hi=c[1]
  $@ head(c)in('<','<=','>','>=')$* c[1]==x $* $4(c[2]):
   if c[0]in('<','<='):
    hi=c[2]
   $&:
    lo=c[2]
 if lo is $# or hi is $#:
  $! $#
 $! lo,hi
$, satisfies(s,x,cons):
 $) c in cons:
  h=head(c)
  if h in('<','<=','>','>=','/=','='):
   ${:
    a=fv($W(c[1],x,s))
    b=fv($W(c[2],x,s))
   $5 $7:
    if $- $4(s):
     $6
    $! $2
   eps=1e-12*(1+$J(a)+$J(b))
   if h=='<' $* $- a<b-eps*0:
    $! $2
   if h=='<=' $* $- a<=b+eps:
    $! $2
   if h=='>' $* $- a>b:
    $! $2
   if h=='>=' $* $- a>=b-eps:
    $! $2
   if h=='/=' $* $J(a-b)<=eps:
    $! $2
   if h=='=' $* $J(a-b)>1e-9*(1+$J(a)+$J(b)):
    $! $2
  $@ h=='$*':
   if $- satisfies(s,x,$K(c[1:])):
    $! $2
 $! $A
$, solve(eq,x,$C=$2,cons=$#):
 NC[0]=0
 if $((eq,'$*')or $((eq,'$K'):
  $! $#
 h=head(eq)
 if h in('<','>','<=','>=','/='):
  f=$](eq[1],eq[2])
  cp=rel_pairs(cons,x)if cons $& $#
  if cp:
   $! solve_rels([(h,$.(f))]+cp,x)
  r=solve_ineq(h,f,x)
  $! r
 if h=='=':
  f=$](eq[1],eq[2])
 $@ h=='or':
  if $- $C $* any([head(q)in('<','>','<=','>=','/=')$) q in eq[1:]]):
   ps=rel_pairs(eq[1:],x)if all([head(q)!='$*' $) q in eq[1:]])$& $#
   if ps:
    r=solve_rels(ps,x,$A)
    if r is $- $#:
     $! r
  $~=[]
  $) e in eq[1:]:
   r=solve(e,x,$C,cons)
   if r is $#:
    $! $#
   if r=='true':
    $! 'true'
   if $((r,'or'):
    $~.$}([q $) q in r[1:]if q $- in $~])
   $@ r!='false' $* r $- in $~:
    $~.$%(r)
  if $- $~:
   $! 'false'
  $!('or',)+$0($~)if $1($~)>1 $& $~[0]
 $@ eq=='true':
  $! 'true'
 $&:
  f=eq
 w=firstwhen(f,x)
 if w is $- $#:
  r=solve_when(f,w,x,$C,cons)
  if r is $- $#:
   $! r
 if $- $C $* firstabs(f,x)is $- $# $* abs_cases(numer_of(f),x,[],0)=='interval':
  r=abs_region(f,x,cons)
  if r is $- $#:
   $! r
 $h=$o(f,x,$C)
 if $h is $#:
  $! $#
 if $h!='all':
  $h=[clean(s)$) s in $h]
  if $- $C:
   $h=[s $) s in $h if $-($4(s)$* $- $x(s))]
   $h=[realpart(s)$) s in $h]
  $h=sortsols(dedup($h))
 if cons:
  $h=apply_constraints($h,x,cons)
 $! sols_to_bool(x,$h)
$, firstabs(f,x):
 if $/(f)is $- $0 or f[0]=='Q':
  $! $#
 if f[0]=='$J' $* $- $8(f[1],x):
  $! f
 $) a in f[1:]:
  w=firstabs(a,x)
  if w is $- $#:
   $! w
 $! $#
$, abs_cases(f,x,conds,$;):
 w=firstabs(f,x)
 if w is $#:
  rs=$o(f,x,$2,$;+1)
  if rs=='all':
   ps=rel_pairs(conds,x)
   r=solve_rels(ps,x)if ps is $- $# $& $#
   if r=='false':
    $![]
   if r is $# or $((r,'$*')or head(r)in('<','>','<=','>=','/=','or')or r=='true':
    $! 'interval'
   $![r[2]]if $((r,'=')$& 'interval'
  if rs is $#:
   $! $#
  $9=[]
  $) q in rs:
   ns=[w $) w in $g(q)if w[0]=='n' $* w[1:].isdigit()]
   q0=$W(q,ns[0],0)if $1(ns)==1 $& q
   if $x(q0)$* satisfies(q0,x,conds):
    $9.$%(q)
  $! $9
 u=w[1]
 $9=[]
 $) g,c in((replnode(f,w,u),('>=',u,0)),(replnode(f,w,$l(u)),('<',u,0))):
  r=abs_cases(g,x,conds+[c],$;)
  if r is $# or r=='interval':
   $! r
  $) q in r:
   if q $- in $9:
    $9.$%(q)
 $! sortsols($9)
$, abs_region(f,x,cons):
 pts=[]
 $, walk(e):
  if $/(e)is $- $0 or e[0]=='Q':
   $!
  if e[0]=='$J' $* $- $8(e[1],x):
   rs=$o(e[1],x,$2)
   if rs $* rs!='all':
    pts.$}([q $) q in rs if $x(q)])
  $) b in e[1:]:
   walk(b)
 walk(f)
 $, ok(t):
  ${:
   v=fv($W(f,x,t))if $- $/(t)is $D $& $X(f,{x:t})
   if $/(v)is $3:
    v=v.$R
   $! $J(v)<1e-9 $* satisfies(t,x,cons or[])
  $5 $7:
   $! $2
 pts=sortsols(dedup(pts))
 if $- pts:
  $! $#
 $c=[fv(p)$) p in pts]
 segs=[('I',$#,pts[0],ok($c[0]-1.0))]
 $) i in $+($1(pts)):
  segs.$%(('P',pts[i],pts[i],ok(pts[i])))
  if i+1<$1(pts):
   segs.$%(('I',pts[i],pts[i+1],ok(0.5*($c[i]+$c[i+1]))))
 segs.$%(('I',pts[-1],$#,ok($c[-1]+1.0)))
 $! segs_to_bool(segs,x)
NOTREL={'<':'>=','>':'<=','<=':'>','>=':'<','=':'/=','/=':'='}
$, firstwhen(f,x):
 if $/(f)is $- $0 or f[0]=='Q':
  $! $#
 if f[0]=='when' $* $- $8(f[1],x):
  $! f
 $) a in f[1:]:
  w=firstwhen(a,x)
  if w is $- $#:
   $! w
 $! $#
$, replnode(f,w,r):
 if f==w:
  $! r
 if $/(f)is $- $0 or f[0]=='Q':
  $! f
 $! simp((f[0],)+$0(replnode(a,w,r)$) a in f[1:]))
''')
_x(r'''$, solve_when(f,w,x,$C,cons):
 c=w[1]
 cs=$K(c[1:])if head(c)=='$*' $&[c]
 if $- all([head(q)in NOTREL $) q in cs]):
  $! $#
 $~=[]
 r=solve(('=',replnode(f,w,w[2]),0),x,$C,(cons or[])+cs)
 if r is $#:
  $! $#
 $~.$%(r)
 if $1(w)>3:
  $) k in $+($1(cs)):
   nc=cs[:k]+[(NOTREL[cs[k][0]],cs[k][1],cs[k][2])]
   r=solve(('=',replnode(f,w,w[3]),0),x,$C,(cons or[])+nc)
   if r is $#:
    $! $#
   $~.$%(r)
 $9=[]
 $) r in $~:
  $) q in(r[1:]if $((r,'or')$&(r,)):
   if q!='false' $* q $- in $9:
    $9.$%(q)
 if 'true' in $9:
  $! $#
 if $- $9:
  $! 'false'
 $! $9[0]if $1($9)==1 $&('or',)+$0($9)
$, realpart(s):
 if $4(s)$* has(s,'i'):
  r,i=reim(s)
  if i==0 or($F(i)$* $J(tofl(i))<1e-12):
   $! r
 $! s
$, zeros(e,x,$C=$2,cons=$#):
 NC[0]=0
 if $((e,'='):
  e=$](e[1],e[2])
 if firstwhen(e,x)is $- $#:
  r=solve(('=',e,0),x,$C,cons)
  qs=r[1:]if $((r,'or')$&(r,)
  if r is $- $# $* all([r=='false' or($((q,'=')$* q[1]==x)$) q in qs]):
   $!('$K',)+$0([q[2]$) q in qs if r!='false'])
 $h=$o(e,x,$C)
 if $h is $#:
  $! $#
 if $h=='all':
  $!('$K',)
 $h=[clean(s)$) s in $h]
 if $- $C:
  $h=[realpart(s)$) s in $h if $-($4(s)$* $- $x(s))]
 $h=sortsols(dedup($h))
 if cons:
  $h=apply_constraints($h,x,cons)
 $!('$K',)+$0($h)
YP=('Y1_','Y2_')
$, desolve(ode,x,y,conds):
 NC[0]=0
 F=eqexpr(ode)if $((ode,'=')$& ode
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
 cs_=$Z(F,y1)
 if cs_ is $- $# $* $1(cs_)==2 $* $8(cs_[1],y1):
  g=$.($l($U(cs_[0],cs_[1])))
 $&:
  rs=$o(F,y1)
  if $- rs or rs=='all' or $1(rs)!=1:
   $! $#
  g=rs[0]
 c1='c1'
 gy=$Z($?(g),y)
 if gy is $- $# $* $1(gy)==2 $* $8(gy[1],y):
  P=$l(gy[1])
  Bq=gy[0]
  if Bq==0 or $8(P,x)$* $8(Bq,x)$* $2:
   pass
  mu=pw('e',integrate(P,x))
  mu=dropabs(simp(mu))
  I=integ($.($?($<(mu,Bq))),x)
  if I is $- $#:
   yy=$.($U($^(I,c1),mu))
   $!('=',y,nice($?(yy))if $- hasden_free(yy)$& nice(yy))
 sep=separate(g,x,y)
 if sep is $- $#:
  p,q=sep
  L=integ($.(pw(q,-1)),y)
  R=integ(p,x)
  if L is $- $# $* R is $- $#:
   rs=isolate_eq(L,$^(R,c1),y)
   if rs is $- $# $* $1(rs)==1:
    $!('=',y,nice(simp(rs[0])))
   G=lncombine(L,y)
   if G is $- $#:
    rs=$o($](G,$<(c1,pw('e',R))),y)
    if rs $* rs!='all' $* $1(rs)==1:
     $!('=',y,nice(rs[0]))
   $!('=',L,$^(R,c1))
 bern_=bernoulli(g,x,y)
 if bern_ is $- $#:
  $! bern_
 V='V_'
 h=$.($W(g,y,$<(V,x)))
 if $8(h,x)$* has(h,V):
  dv=$.($](h,V))
  if dv!=0:
   L=integ($.(pw(dv,-1)),V)
   if L is $- $#:
    R=$^(fn('ln',fn('$J',x)),c1)
    rs=isolate_eq(L,R,V)
    if rs is $- $# $* $1(rs)==1:
     $!('=',y,nice($?($<(x,rs[0]))))
    L2=$W(L,V,$U(y,x))
    $!('=',L2,R)
 $! $#
$, dropabs(e):
 if $/(e)is $- $0 or e[0]=='Q':
  $! e
 if e[0]=='$J':
  $! dropabs(e[1])
 $! simp((e[0],)+$0(dropabs(a)$) a in e[1:]))
$, lncombine(L,y):
 $Q=L[1:]if $((L,'+')$&(L,)
 fs=[]
 $) t in $Q:
  c,r=$b(t)
  if $((r,'ln')$* $u(c):
   u=r[1]
   if $((u,'$J'):
    u=u[1]
   fs.$%(pw(u,c))
  $&:
   $! $#
 if $1(fs)<1:
  $! $#
 $! $.($I(fs))
$, hasden_free(e):
 $! $2
$, isolate_eq(L,R,y):
 ${:
  r=isolate(L,R,y,$2,0)
 $5 $7:
  $! $#
 if r is $# or r=='all':
  $! $#
 $! r
$, separate(g,x,y):
 if $8(g,y):
  $! g,1
 if $8(g,x):
  $! 1,g
 fs=g[1:]if $((g,'*')$&(g,)
 px=[]
 qy=[]
 $) f in fs:
  if $8(f,y):
   px.$%(f)
  $@ $8(f,x):
   qy.$%(f)
  $@ $((f,'^')$* $8(f[1],x)$* $8(f[1],y)$* $((f[2],'+'):
   tx=[t $) t in f[2][1:]if $8(t,y)]
   ty=[t $) t in f[2][1:]if $8(t,x)]
   if $1(tx)+$1(ty)!=$1(f[2])-1:
    $! $#
   px.$%(pw(f[1],$=(tx)))
   qy.$%(pw(f[1],$=(ty)))
  $&:
   $! $#
 $! $I(px),$I(qy)
$, expand_exp(e):
 if $/(e)is $- $0 or e[0]=='Q':
  $! e
 if e[0]=='^' $* $((e[2],'+')$*(e[1]=='e' or $F(e[1])):
  $! $I([pw(e[1],t)$) t in e[2][1:]])
 $! simp((e[0],)+$0(expand_exp(a)$) a in e[1:]))
$, bernoulli(g,x,y):
 g=$?(g)
 $Q=g[1:]if $((g,'+')$&(g,)
 groups={}
 $) t in $Q:
  k=$#
  fs=t[1:]if $((t,'*')$&(t,)
  $f=[]
  $) f in fs:
   if f==y:
    k=1 if k is $# $& $#
   $@ $((f,'^')$* f[1]==y $* $F(f[2]):
    k=f[2]
   $@ $8(f,y):
    $f.$%(f)
   $&:
    $! $#
  if k is $#:
   $! $#
  groups[k]=$^(groups.get(k,0),$I($f))
 if $1(groups)!=2 or 1 $- in groups:
  $! $#
 n=[k $) k in groups if k!=1][0]
 a=groups[1]
 b=groups[n]
 m=nsub(1,n)
 V='V_'
 vs=de1($](YP[0],$<(m,$^($<(a,V),b))),x,V)
 if vs is $# or $- $((vs,'=')or vs[1]!=V:
  $! $#
 $!('=',y,nice(pw(vs[2],ninv(m))))
''')
_x(r'''$, de2(F,x,y):
 y1,y2=YP
 c1,c2='c1','c2'
 G=$?(F)
 a=$Z(G,y2)
 if a is $# or $1(a)!=2:
  $! $#
 A=a[1]
 $f=a[0]
 b=$Z($f,y1)
 if b is $# or $1(b)>2:
  $! $#
 B=b[1]if $1(b)==2 $& 0
 $f=b[0]
 c=$Z($f,y)
 if c is $# or $1(c)>2:
  $! $#
 C=c[1]if $1(c)==2 $& 0
 g=$l(c[0])
 $) t in(A,B,C):
  if has(t,y)or has(t,y1)or has(t,y2):
   $! $#
 if $8(A,x)$* $8(B,x)$* $8(C,x):
  y1s,y2s=charsol(A,B,C,x)
 $&:
  ce=cauchy_euler(A,B,C,x)
  if ce is $#:
   if C==0:
    V='V_'
    r=de1($^($<(A,YP[0]),$<(B,V),$l(g)),x,V)
    if r is $# or $- $((r,'=')or r[1]!=V:
     $! $#
    r2=integ($W(r[2],'c1','c2'),x)
    if r2 is $#:
     $! $#
    $!('=',y,$^(r2,c1))
   $! $#
  y1s,y2s=ce
 yh=$^($<(c1,y1s),$<(c2,y2s))
 if g==0:
  $!('=',y,yh)
 W=pyth($.($?($]($<(y1s,diff(y2s,x)),$<(diff(y1s,x),y2s)))))
 gg=$.($U(g,A))
 I1=integ($.($?($U($<(y2s,gg),W))),x)
 I2=integ($.($?($U($<(y1s,gg),W))),x)
 if I1 is $# or I2 is $#:
  $! $#
 yp=pyth($?($^($<($l(y1s),I1),$<(y2s,I2))))
 $!('=',y,nice($^(yh,yp)))
$, charsol(A,B,C,x):
 D=$.($?($]($<(B,B),$<(4,A,C))))
 if $x(D)$* fv(D)<0:
  al=$.($U($l(B),$<(2,A)))
  be=$.($U($N($l(D)),$<(2,A)))
  ex=pw('e',$<(al,x))
  $! $<(ex,fn('cos',$<(be,x))),$<(ex,fn('sin',$<(be,x)))
 if D==0:
  r=$.($U($l(B),$<(2,A)))
  $! pw('e',$<(r,x)),$<(x,pw('e',$<(r,x)))
 s=$N(D)
 r1=$.($U($^($l(B),s),$<(2,A)))
 r2=$.($U($]($l(B),s),$<(2,A)))
 $! pw('e',$<(r1,x)),pw('e',$<(r2,x))
$, cauchy_euler(A,B,C,x):
 a=$.($U(A,pw(x,2)))
 b=$.($U(B,x))
 if $-($8(a,x)$* $8(b,x)$* $8(C,x)):
  $! $#
 aa=a
 bb=$](b,a)
 cc=C
 D=$.($?($]($<(bb,bb),$<(4,aa,cc))))
 lx=fn('ln',x)
 if $x(D)$* fv(D)<0:
  al=$.($U($l(bb),$<(2,aa)))
  be=$.($U($N($l(D)),$<(2,aa)))
  $! $<(pw(x,al),fn('cos',$<(be,lx))),$<(pw(x,al),fn('sin',$<(be,lx)))
 if D==0:
  r=$.($U($l(bb),$<(2,aa)))
  $! pw(x,r),$<(pw(x,r),lx)
 s=$N(D)
 r1=$.($U($^($l(bb),s),$<(2,aa)))
 r2=$.($U($]($l(bb),s),$<(2,aa)))
 $! pw(x,r1),pw(x,r2)
$, apply_ic(sol,x,y,conds,nconst):
 cs_=['c1','c2'][:nconst]
 eqs=[]
 if sol[1]==y:
  Y=sol[2]
  $) order,x0,v in conds:
   e=Y
   $) _ in $+(order):
    e=diff(e,x)
   eqs.$%(('=',$W(e,x,x0),v))
 $&:
  $) order,x0,v in conds:
   if order==0:
    eqs.$%($W($W(sol,x,x0),y,v))
 used=[c $) c in cs_ if has(sol,c)]
 if $- eqs or $- used:
  $! sol
 rs=solve_system(eqs,used)
 if $- rs:
  $! 'false'
 s=rs[0]
 r=sol
 $) c in used:
  if c in s:
   r=(r[0],$W(r[1],c,s[c]),$W(r[2],c,s[c]))
 if r[1]==y:
  $!('=',y,nice(r[2]))
 rs2=isolate_eq(r[1],r[2],y)
 if rs2 is $- $# $* $1(rs2)>=1:
  $) cand in rs2:
   ok=$A
   $) order,x0,v in conds:
    if order==0:
     ${:
      if $J($X($W(cand,x,x0))-$X(v))>1e-9:
       ok=$2
     $5 $7:
      pass
   if ok:
    $!('=',y,nice(cand))
 $! r
$, fextreme(f,x,kind,lo=$#,hi=$#):
 NC[0]=0
 d=$.(diff(f,x))
 cands=[]
 rs=$o(d,x)
 if rs is $#:
  rs=numeric_solve(d,x,$2,tofl($X(lo))if lo is $- $# $* $4(lo)$& $#,
 tofl($X(hi))if hi is $- $# $* $4(hi)$& $#)or[]
 if rs=='all':
  $! 'true'
 exp_=[]
 $) r in rs:
  ns=[w $) w in $g(r)if w[0]=='n' $* w[1:].isdigit()]
  if ns $* lo is $- $# $* hi is $- $#:
   $) k in $+(-50,51):
    exp_.$%($W(r,ns[0],k))
  $@ ns:
   exp_.$%(r)
  $&:
   exp_.$%(r)
 rs=exp_
 $) r in rs:
  r=clean(r)
  ns=[w $) w in $g(r)if w[0]=='n' $* w[1:].isdigit()]
  if ns:
   cands.$%(r)
   $6
  if $- $x(r):
   $6
  if lo is $- $# $* fv(r)<fv(lo)-1e-12:
   $6
  if hi is $- $# $* fv(r)>fv(hi)+1e-12:
   $6
  cands.$%(r)
 ends=[]
 ends.$%(lo if lo is $- $# $&('*',-1,'$P'))
 ends.$%(hi if hi is $- $# $& '$P')
 best=$#
 bv=$#
 pts=[]
 $) c in cands+ends:
  if c=='$P' or c==('*',-1,'$P'):
   v=$z(f,x,c)
  $&:
   cz=c
   $) w in $g(c):
    if w[0]=='n' $* w[1:].isdigit():
     cz=$W(cz,w,0)
   v=$W(f,x,cz)
   if has(v,'$H'):
    $6
  ${:
   if v=='$P':
    vv=$D('$P')
   $@ v==('*',-1,'$P'):
    vv=$D('-$P')
   $&:
    vv=fv(v)
  $5 $7:
   $6
  if kind=='max':
   vv=-vv
  pts.$%((vv,c))
 if $- pts:
  $! $#
 pts.sort(key=$: p:p[0])
 m=pts[0][0]
 if m==$D('-$P'):
  win=[p[1]$) p in pts if p[0]==m]
 $&:
  win=[p[1]$) p in pts if $J(p[0]-m)<=1e-10*(1+$J(m))]
 win=sortsols(dedup(win))
 eqs=[('=',x,w)$) w in win]
 $! eqs[0]if $1(eqs)==1 $&('or',)+$0(eqs)
''')
_x(r'''$, nfextreme(f,x,kind,lo=$#,hi=$#):
 sg=1.0 if kind=='min' $&-1.0
 $, F(t):
  ${:
   v=$X(f,{x:t})
   if $/(v)is $3:
    v=v.$R
   $! sg*v
  $5 $7:
   $! $D('$P')
 if lo is $# or hi is $#:
  a=-100.0 if lo is $# $& lo
  b=100.0 if hi is $# $& hi
 $&:
  a,b=lo,hi
 N=400
 best=a
 bv=F(a)
 $) i in $+(N+1):
  t=a+(b-a)*i/N
  v=F(t)
  if v<bv:
   bv=v
   best=t
 h=(b-a)/N
 l=max(a,best-h)
 r=min(b,best+h)
 g=($Y.$N(5)-1)/2
 $) _ in $+(200):
  c=r-g*(r-l)
  d=l+g*(r-l)
  if F(c)<F(d):
   r=d
  $&:
   l=c
  if $J(r-l)<1e-12*(1+$J(l)):
   $O
 t=0.5*(l+r)
 $) side,bound in((1.0,hi),(-1.0,lo)):
  if bound is $#:
   vs=[F(side*10.0**k)$) k in(3,5,7)]
   if vs[0]<=bv $* vs[1]<=vs[0]$* vs[2]<=vs[1]$* vs[2]<bv:
    $! '$P' if side>0 $&('*',-1,'$P')
 ${:
  d=diff(f,x)
  $, G(u):
   ${:
    v=$X(d,{x:u})
    $! v.$R if $/(v)is $3 $& v
   $5 $7:
    $! $#
  t2=newton(G,t)
  if t2 is $- $# $* $J(t2-t)<10*h $*(lo is $# or t2>=lo)$*(hi is $# or t2<=hi):
   t=t2
 $5 $7:
  pass
 $! snap(t)
$, domain(f,x):
 conds=[]
 domconds(f,x,conds)
 if $- conds:
  $!('<',('*',-1,'$P'),x)if $2 $& 'true'
 pts=[]
 $) rel,g in conds:
  rs=$o(g,x)
  if rs is $#:
   $! $#
  if rs=='all':
   $6
  $) r in rs:
   if $x(r):
    pts.$%(r)
 pts=sortsols(dedup(pts))
 $, ok(t):
  $) rel,g in conds:
   ${:
    v=$X(g,{x:t})
   $5 $7:
    $! $2
   if $/(v)is $3:
    if $J(v.imag)>1e-9:
     $! $2
    v=v.$R
   if $- relok(rel,v):
    $! $2
  $! $A
 $, okexact(p):
  $) rel,g in conds:
   ${:
    v=$W(g,x,p)
    vv=fv(v)
   $5 $7:
    $! $2
   if $J(vv)<1e-12:
    vv=0.0
   if $- relok(rel,vv):
    $! $2
  $! $A
 $c=[fv(p)$) p in pts]
 if $- $c:
  $! 'true' if ok(0.5)$& 'false'
 segs=[('I',$#,pts[0],ok($c[0]-max(1.0,$J($c[0]))))]
 $) i in $+($1(pts)):
  segs.$%(('P',pts[i],pts[i],okexact(pts[i])))
  if i+1<$1(pts):
   segs.$%(('I',pts[i],pts[i+1],ok(0.5*($c[i]+$c[i+1]))))
 segs.$%(('I',pts[-1],$#,ok($c[-1]+max(1.0,$J($c[-1])))))
 $! segs_to_bool(segs,x)
$, domconds(f,x,$9):
 if $/(f)is $- $0 or f[0]=='Q' or $8(f,x):
  $!
 h=f[0]
 if h=='^':
  b,p=f[1],f[2]
  if $F(p)$* $`(p)<0:
   $9.$%(('/=',b))
  if isq(p)$* p[2]%2==0:
   $9.$%(('>=' if $`(p)>0 $& '>',b))
 $@ h in('ln','log'):
  $9.$%(('>',f[1]))
 $@ h in('$|','arccos'):
  $9.$%(('<=',$](fn('$J',f[1]),1)))
 $@ h=='tan':
  $9.$%(('/=',fn('cos',f[1])))
 $) a in f[1:]:
  domconds(a,x,$9)
''')
_x(r'''import $Y
$, ismat(e):
 $! $((e,'mat')
$, $e(e):
 $! $((e,'$K')
$, $[(M):
 $![$K(r[1:])$) r in M[1:]]
$, mk(R):
 $!('mat',)+$0(('$K',)+$0(r)$) r in R)
$, lst(xs):
 $!('$K',)+$0(xs)
$, dims(M):
 $! $1(M)-1,$1(M[1])-1
$, tomat(e):
 if ismat(e):
  $! e
 if $e(e):
  $! mk([$K(e[1:])])
 err("Matrix expected")
$, ac(e):
 $! $.($?(e))if hasdenom(e)$& $?(e)
$, m_add(A,B,sgn=1):
 if dims(A)!=dims(B):
  err("Dimension error")
 a=$[(A)
 b=$[(B)
 $! mk([[$^(a[i][j],$<(sgn,b[i][j]))$) j in $+($1(a[0]))]$) i in $+($1(a))])
$, m_scale(A,c):
 $! mk([[$<(c,v)$) v in r]$) r in $[(A)])
$, m_map(A,f):
 $! mk([[f(v)$) v in r]$) r in $[(A)])
$, m_mul(A,B):
 a=$[(A)
 b=$[(B)
 if $1(a[0])!=$1(b):
  err("Dimension error")
 n=$1(b)
 $! mk([[ac($=([$<(a[i][k],b[k][j])$) k in $+(n)]))$) j in $+($1(b[0]))]$) i in $+($1(a))])
$, ident(n):
 $! mk([[1 if i==j $& 0 $) j in $+(n)]$) i in $+(n)])
$, m_pow(A,k):
 m,n=dims(A)
 if m!=n:
  err("Square matrix required")
 if k<0:
  A=m_inv(A)
  k=-k
 R=ident(n)
 $G k>0:
  if k&1:
   R=m_mul(R,A)
  k>>=1
  if k:
   A=m_mul(A,A)
 $! R
$, transpose(A):
 if $e(A):
  $! mk([[v]$) v in A[1:]])
 a=$[(A)
 $! mk([[a[i][j]$) i in $+($1(a))]$) j in $+($1(a[0]))])
$, det(A):
 a=$[(A)
 n=$1(a)
 if n!=$1(a[0]):
  err("Square matrix required")
 if n==1:
  $! a[0][0]
 if n==2:
  $! ac($]($<(a[0][0],a[1][1]),$<(a[0][1],a[1][0])))
 if n==3:
  t=[]
  $) j in $+(3):
   minor=$]($<(a[1][(j+1)%3],a[2][(j+2)%3]),$<(a[1][(j+2)%3],a[2][(j+1)%3]))
   t.$%($<(a[0][j],minor))
  $! ac($=(t))
 M=[$K(r)$) r in a]
 sign=1
 prev=1
 $) k in $+(n-1):
  if ac(M[k][k])==0:
   sw=$#
   $) i in $+(k+1,n):
    if ac(M[i][k])!=0:
     sw=i
     $O
   if sw is $#:
    $! 0
   M[k],M[sw]=M[sw],M[k]
   sign=-sign
  $) i in $+(k+1,n):
   $) j in $+(k+1,n):
    M[i][j]=ac($U($]($<(M[i][j],M[k][k]),$<(M[i][k],M[k][j])),prev))
  prev=M[k][k]
 $! ac($<(sign,M[n-1][n-1]))
$, iszero(v):
 v=ac(v)
 if v==0:
  $! $A
 if $/(v)is $D $* $J(v)<1e-13:
  $! $A
 $! $2
$, rref(A,full=$A):
 M=[$K(r)$) r in $[(A)]
 m=$1(M)
 n=$1(M[0])
 r=0
 $) c in $+(n):
  if r>=m:
   $O
  p=$#
  if hasfloat_m(M):
   best=0.0
   $) i in $+(r,m):
    ${:
     v=$J($X(M[i][c]))
    $5 $7:
     v=1.0 if $- iszero(M[i][c])$& 0.0
    if v>best+1e-14:
     best=v
     p=i
   if best<1e-13:
    p=$#
  $&:
   $) i in $+(r,m):
    if $- iszero(M[i][c]):
     p=i
     $O
  if p is $#:
   $6
  M[r],M[p]=M[p],M[r]
  pv=M[r][c]
  if full:
   M[r]=[ac($U(v,pv))$) v in M[r]]
  $&:
   M[r]=[ac($U(v,pv))$) v in M[r]]
  rng=$+(m)if full $& $+(r+1,m)
  $) i in rng:
   if i!=r $* $- iszero(M[i][c]):
    f=M[i][c]
    M[i]=[ac($](M[i][j],$<(f,M[r][j])))$) j in $+(n)]
  r+=1
 $) i in $+(m):
  $) j in $+(n):
   if $/(M[i][j])is $D $* $J(M[i][j])<1e-13:
    M[i][j]=0.0
 $! mk(M)
$, hasfloat_m(M):
 $) r in M:
  $) v in r:
   if $_(v):
    $! $A
 $! $2
$, minor(a,i,j):
 $![[a[r][c]$) c in $+($1(a))if c!=j]$) r in $+($1(a))if r!=i]
$, m_inv(A):
 m,n=dims(A)
 if m!=n:
  err("Square matrix required")
 a0=$[(A)
 if n<=3 $* $- all([$F(v)$) r in a0 $) v in r]):
  D=det(A)
  if iszero(D):
   err("Singular matrix")
  if n==1:
   $! mk([[nice(pw(D,-1))]])
  $9=[]
  $) i in $+(n):
   row=[]
   $) j in $+(n):
    c=det(mk(minor(a0,j,i)))
    if(i+j)%2:
     c=$l(c)
    row.$%(nice(ac($U(c,D))))
   $9.$%(row)
  $! mk($9)
 a=$[(A)
 aug=mk([a[i]+[1 if i==j $& 0 $) j in $+(n)]$) i in $+(n)])
 R=$[(rref(aug))
 $) i in $+(n):
  $) j in $+(n):
   if $- iszero($](R[i][j],1 if i==j $& 0)):
    err("Singular matrix")
 $! mk([[nice(R[i][n+j])$) j in $+(n)]$) i in $+(n)])
$, trace(A):
 a=$[(A)
 $! $=([a[i][i]$) i in $+($1(a))])
$, charpoly(A,lam):
 a=$[(A)
 n=$1(a)
 if n!=$1(a[0]):
  err("Square matrix required")
 I=ident(n)
 Mk=mk([[0]*n $) _ in $+(n)])
 cs=[0]*(n+1)
 cs[n]=1
 $) k in $+(1,n+1):
  Mk=m_add(m_mul(A,Mk),m_scale(I,cs[n-k+1]))
  cs[n-k]=ac($U($l(trace(m_mul(A,Mk))),k))
 $! $=([$<(cs[k],pw(lam,k))$) k in $+(n+1)])
$, eigvl(A):
 if hasfloat_m($[(A)):
  ${:
   E=m_map(A,exactify)
  $5 $7:
   E=$#
  if E is $- $# $* $- hasfloat_m($[(E)):
   $! evalf(eigvl(E))
 lam='L_'
 p=charpoly(A,lam)
 f=p
 if $- hasfloat_m($[(A)):
  ${:
   f=factor_expr(p)
  $5 $7:
   f=p
  if $((f,'hold'):
   f=f[1]
 $9=[]
 $) g in(f[1:]if $((f,'*')$&(f,)):
  k=1
  if $((g,'^')$* $n(g[2])$* g[2]>0:
   g,k=g[1],g[2]
  if $8(g,lam):
   $6
  z=zeros(g,lam,$A)
  if z is $#:
   err("Cannot compute eigenvalues")
  z=$K(z[1:])
  d=degree(g,lam)
  $) v in z:
   m=mult(g,lam,v,d)if d is $- $# $* $1(z)<d $& 1
   $9+=[v]*(k*m)
 if $- $9:
  err("Cannot compute eigenvalues")
 $, key(v):
  if $- $4(v):
   $!(1,0.0,0.0,okey(v))
  z=$3($X(v))
  $!(0,-$J(z),-z.$R,-z.imag)
 $9.sort(key=key)
 $! lst($9)
$, mult(g,lam,v,d):
 m=1
 h=g
 $G m<d:
  h=diff_(h,lam)
  w=$W(h,lam,v)
  if $_(w)or $_(v):
   ${:
    if $J($3($X(w)))>1e-6*(1+$J($3($X(v))))**d:
     $O
   $5 $7:
    $O
  $@ $- iszero(ac($?(w))):
   $O
  m+=1
 $! m
$, diff_(e,x):
 $! diff(e,x)
''')
_x(r'''$, nullspace(A):
 R=$[(rref(A))
 m=$1(R)
 n=$1(R[0])
 piv=[]
 $) i in $+(m):
  $) j in $+(n):
   if $- iszero(R[i][j]):
    piv.$%((i,j))
    $O
 pc=[j $) i,j in piv]
 free=[j $) j in $+(n)if j $- in pc]
 basis=[]
 $) f in free:
  v=[0]*n
  v[f]=1
  $) i,j in piv:
   v[j]=ac($l(R[i][f]))
  basis.$%(v)
 $! basis
$, eigvc(A):
 if hasfloat_m($[(A)):
  ${:
   E=m_map(A,exactify)
  $5 $7:
   E=$#
  if E is $- $# $* $- hasfloat_m($[(E)):
   $! evalf(eigvc(E))
 $c=eigvl(A)
 n=dims(A)[0]
 cols=[]
 seen=[]
 $) lv in $c[1:]:
  if lv in seen:
   $6
  seen.$%(lv)
  if $_(lv)or hasfloat_m($[(A)):
   cols.$%(numeigvec(A,lv))
   $6
  B=m_add(A,m_scale(ident(n),lv),-1)
  B=m_map(B,$: v:ac(v))
  ns=nullspace(B)
  $) v in ns:
   cols.$%(unitvec(v))
 if $- cols:
  err("Cannot compute eigenvectors")
 M=mk([[cols[j][i]$) j in $+($1(cols))]$) i in $+(n)])
 $) c in cols:
  $) v in c:
   if esize(v)>60:
    $! evalf(M)
 $! M
$, numeigvec(A,lam):
 a=[[$3($X(c))$) c in r]$) r in $[(A)]
 n=$1(a)
 mu=$3($X(lam))
 mu+=1e-9*(1+$J(mu))
 M=[[a[i][j]-(mu if i==j $& 0)$) j in $+(n)]$) i in $+(n)]
 x=[$3(1.0+0.37*i)$) i in $+(n)]
 $) it in $+(4):
  y=clsolve(M,x)
  big=max([$J(v)$) v in y])or 1.0
  x=[v/big $) v in y]
 nrm=$Y.$N(sum([$J(v)**2 $) v in x]))or 1.0
 x=[v/nrm $) v in x]
 k=0
 $) i in $+(n):
  if $J(x[i])>$J(x[k])+1e-12:
   k=i
 ph=x[k]/$J(x[k])
 $9=[]
 $) v in x:
  v=v/ph
  re=0.0 if $J(v.$R)<1e-12 $& v.$R
  im=0.0 if $J(v.imag)<1e-12 $& v.imag
  $9.$%(re if im==0.0 $& fromcomplex($3(re,im)))
 $! $9
$, clsolve(M,b):
 n=$1(M)
 a=[$K(M[i])+[b[i]]$) i in $+(n)]
 $) c in $+(n):
  p=c
  $) r in $+(c+1,n):
   if $J(a[r][c])>$J(a[p][c]):
    p=r
  a[c],a[p]=a[p],a[c]
  if $J(a[c][c])<1e-14:
   a[c][c]=1e-14
  $) r in $+(c+1,n):
   f=a[r][c]/a[c][c]
   if f:
    $) k in $+(c,n+1):
     a[r][k]-=f*a[c][k]
 x=[0j]*n
 $) i in $+(n-1,-1,-1):
  t=a[i][n]
  $) k in $+(i+1,n):
   t-=a[i][k]*x[k]
  x[i]=t/a[i][i]
 $! x
$, coefs(e,$9):
 if $F(e):
  $9.$%(e)
 $@ $((e,'+'):
  $) t in e[1:]:
   coefs(t,$9)
 $@ $((e,'*')$* $F(e[1]):
  $9.$%(e[1])
 $&:
  $9.$%(1)
$, unitvec(v):
 if hasfloat_m([v]):
  nrm=$N($=([$<(c,fn('conj',c))$) c in v]))
  $![nice(ac($U(c,nrm)))$) c in v]
 cs=[]
 $) c in v:
  coefs(c,cs)
 den=1
 num=0
 $) q in cs:
  if $u(q)$* q!=0:
   a,b=nd(q)
   den=ilcm(den,b)
   num=igcd(num,a)
 k=Q(den,num)if num $& 1
 $) c in v:
  if $- iszero(c):
   if isneg(c):
    k=$l(k)
   $O
 w=[ac($?($<(k,c)))$) c in v]
 n2=ac($?($=([$<(c,fn('conj',c))$) c in w])))
 r=$N(n2)
 if $F(r)or $- $((r,'^'):
  $![ac($U(c,r))$) c in w]
 inv=('^',r[1],$l(r[2]))
 $![c if iszero(c)$&('*',c,inv)if $((c,'+')$& $<(c,inv)$) c in w]
$, esize(e):
 if $/(e)is $- $0 or e[0]=='Q':
  $! 1
 k=1
 $) a in e[1:]:
  k+=esize(a)
 $! k
$, lu(A):
 a=[$K(r)$) r in $[(A)]
 m=$1(a)
 n=$1(a[0])
 L=[[1 if i==j $& 0 $) j in $+(m)]$) i in $+(m)]
 P=$K($+(m))
 U=a
 $) k in $+(min(m,n)):
  p=$#
  if hasfloat_m(U):
   best=-1.0
   $) i in $+(k,m):
    v=$J($X(U[i][k]))
    if v>best:
     best=v
     p=i
   if best<1e-14:
    p=$#
  $&:
   $) i in $+(k,m):
    if $- iszero(U[i][k]):
     p=i
     $O
  if p is $#:
   $6
  if p!=k:
   U[k],U[p]=U[p],U[k]
   P[k],P[p]=P[p],P[k]
   $) j in $+(k):
    L[k][j],L[p][j]=L[p][j],L[k][j]
  $) i in $+(k+1,m):
   f=ac($U(U[i][k],U[k][k]))
   L[i][k]=f
   U[i]=[ac($](U[i][j],$<(f,U[k][j])))$) j in $+(n)]
 Pm=[[1 if P[i]==j $& 0 $) j in $+(m)]$) i in $+(m)]
 $! mk(L),mk(U),mk(Pm)
$, qr(A):
 a=$[(A)
 m=$1(a)
 n=$1(a[0])
 cols=[[a[i][j]$) i in $+(m)]$) j in $+(n)]
 Qc=[]
 R=[[0]*n $) _ in $+(n)]
 $) j in $+(n):
  v=cols[j]
  $) k in $+($1(Qc)):
   r=ac($=([$<(Qc[k][i],v[i])$) i in $+(m)]))
   R[k][j]=r
   v=[ac($](v[i],$<(r,Qc[k][i])))$) i in $+(m)]
  nrm=nice($N(ac($=([pw(c,2)$) c in v]))))
  R[j][j]=nrm
  if iszero(nrm):
   Qc.$%([0]*m)
  $&:
   Qc.$%([nice(ac($U(c,nrm)))$) c in v])
 Qm=mk([[Qc[j][i]$) j in $+(n)]$) i in $+(m)])
 $! Qm,mk(R)
$, crossp(u,v):
 a=vec(u)
 b=vec(v)
 if $1(a)==2:
  a=a+[0]
  b=b+[0]
 if $1(a)!=3 or $1(b)!=3:
  err("Dimension error")
 r=[ac($]($<(a[1],b[2]),$<(a[2],b[1]))),
 ac($]($<(a[2],b[0]),$<(a[0],b[2]))),
 ac($]($<(a[0],b[1]),$<(a[1],b[0])))]
 $! revec(r,u)
$, vec(u):
 if $e(u):
  $! $K(u[1:])
 if ismat(u):
  R=$[(u)
  if $1(R)==1:
   $! R[0]
  if $1(R[0])==1:
   $![r[0]$) r in R]
 err("Vector expected")
$, revec(r,like):
 if $e(like):
  $! lst(r)
 R=$[(like)
 if $1(R)==1:
  $! mk([r])
 $! mk([[v]$) v in r])
$, dotp(u,v):
 a=vec(u)
 b=vec(v)
 if $1(a)!=$1(b):
  err("Dimension error")
 $! ac($=([$<(a[i],b[i])$) i in $+($1(a))]))
$, norm(A):
 if $e(A)or ismat(A)$*(dims(A)[0]==1 or dims(A)[1]==1):
  v=vec(A)
  $! nice($N(ac($=([$<(c,fn('conj',c))$) c in v]))))
 $! nice($N(ac($=([$<(c,fn('conj',c))$) r in $[(A)$) c in r]))))
$, unitv(u):
 nrm=norm(u)
 $! revec([nice(ac($U(c,nrm)))$) c in vec(u)],u)
$, rownorm(A):
 if $- ismat(A):
  err('Argument must be a matrix')
 $! maxexpr([ac($=([fn('$J',c)$) c in r]))$) r in $[(A)])
$, colnorm(A):
 if $- ismat(A):
  err('Argument must be a matrix')
 $! rownorm(transpose(A))
$, maxexpr(xs):
 best=$#
 bv=$#
 $) x in xs:
  v=$X(x)
  if best is $# or v>bv:
   best=x
   bv=v
 $! best
''')
_x(r'''$, augment(A,B):
 if $e(A)$* $e(B):
  $! A+B[1:]
 a=$[(tomat(A))
 b=$[(tomat(B))
 if $1(a)!=$1(b):
  err("Dimension error")
 $! mk([a[i]+b[i]$) i in $+($1(a))])
$, colaugment(A,B):
 a=$[(tomat(A))
 b=$[(tomat(B))
 if $1(a[0])!=$1(b[0]):
  err("Dimension error")
 $! mk(a+b)
$, submat(A,r1=1,c1=1,r2=$#,c2=$#):
 a=$[(A)
 if r2 is $#:
  r2=$1(a)
 if c2 is $#:
  c2=$1(a[0])
 $! mk([a[i][c1-1:c2]$) i in $+(r1-1,r2)])
$, rowswap(A,i,j):
 a=$[(A)
 a[i-1],a[j-1]=a[j-1],a[i-1]
 $! mk(a)
$, rowadd(A,i,j):
 a=$[(A)
 a[j-1]=[$^(a[j-1][k],a[i-1][k])$) k in $+($1(a[0]))]
 $! mk(a)
$, mrow(c,A,i):
 a=$[(A)
 a[i-1]=[$<(c,v)$) v in a[i-1]]
 $! mk(a)
$, mrowadd(c,A,i,j):
 a=$[(A)
 a[j-1]=[ac($^(a[j-1][k],$<(c,a[i-1][k])))$) k in $+($1(a[0]))]
 $! mk(a)
$, diag(A):
 if $e(A):
  n=$1(A)-1
  $! mk([[A[i+1]if i==j $& 0 $) j in $+(n)]$) i in $+(n)])
 a=$[(A)
 if $1(a)==1 or $1(a[0])==1:
  v=vec(A)
  $! diag(lst(v))
 $! lst([a[i][i]$) i in $+(min($1(a),$1(a[0])))])
$, matlist(A):
 $! lst([v $) r in $[(A)$) v in r])
$, listmat(L,c=$#):
 xs=$K(L[1:])
 if c is $#:
  c=$1(xs)
 if $- $n(c)or c<1:
  err('Invalid number of columns')
 $9=[]
 $G xs:
  r=xs[:c]
  xs=xs[c:]
  $G $1(r)<c:
   r.$%(0)
  $9.$%(r)
 $! mk($9)
$, simult(A,b):
 a=$[(A)
 n=$1(a)
 bb=$[(tomat(b))if ismat(b)$&[[v]$) v in b[1:]]
 if $1(bb)!=n:
  bb=$[(transpose(b))
 k=$1(bb[0])
 R=$[(rref(mk([a[i]+bb[i]$) i in $+(n)])))
 $) i in $+(n):
  if iszero(R[i][i]):
   err("Singular matrix")
 $! mk([[nice(R[i][n+j])$) j in $+(k)]$) i in $+(n)])
$, cumsum(L):
 if $e(L):
  $9=[]
  s=0
  $) v in L[1:]:
   s=$^(s,v)
   $9.$%(s)
  $! lst($9)
 a=$[(L)
 $9=[]
 acc=[0]*$1(a[0])
 $) r in a:
  acc=[$^(acc[j],r[j])$) j in $+($1(r))]
  $9.$%($K(acc))
 $! mk($9)
$, polar_vec(u):
 v=vec(u)
 if $1(v)==2:
  r=nice($N(ac($^(pw(v[0],2),pw(v[1],2)))))
  th=fn('$r',$^(v[0],$<('i',v[1])))
  $!('$p','['+fmtx(r)+' \u2220'+fmtx(th)+']')
 err("Dimension error")
$, fmtx(e):
 $! fmt(e)
$, cylind(u):
 v=vec(u)
 if $1(v)!=3:
  err("Dimension error")
 r=nice($N(ac($^(pw(v[0],2),pw(v[1],2)))))
 th=fn('$r',$^(v[0],$<('i',v[1])))
 $!('$p','['+fmtx(r)+' \u2220'+fmtx(th)+' '+fmtx(v[2])+']')
$, sphere(u):
 v=vec(u)
 if $1(v)!=3:
  err("Dimension error")
 rho=nice($N(ac($^(pw(v[0],2),pw(v[1],2),pw(v[2],2)))))
 th=fn('$r',$^(v[0],$<('i',v[1])))
 ph=fn('arccos',$U(v[2],rho))if rho!=0 $& 0
 $!('$p','['+fmtx(rho)+' \u2220'+fmtx(th)+' \u2220'+fmtx(ph)+']')
$, lsum(L,a=1,b=$#):
 xs=$K(L[1:])
 if b is $#:
  b=$1(xs)
 $! $=(xs[a-1:b])
$, lprod(L,a=1,b=$#):
 xs=$K(L[1:])
 if b is $#:
  b=$1(xs)
 $! $I(xs[a-1:b])
$, mean(L,F=$#):
 xs=$K(L[1:])
 if F is $#:
  $! $U($=(xs),$1(xs))
 fs=$K(F[1:])
 $! $U($=([$<(xs[i],fs[i])$) i in $+($1(xs))]),$=(fs))
$, sortkey(v):
 ${:
  x=$X(v)
  $! x.$R if $/(x)is $3 $& x
 $5 $7:
  $! 0.0
$, median(L):
 xs=sorted($K(L[1:]),key=sortkey)
 n=$1(xs)
 if n%2:
  $! xs[n//2]
 $! $U($^(xs[n//2-1],xs[n//2]),2)
$, variance(L,pop=$2):
 xs=$K(L[1:])
 n=$1(xs)
 m=mean(L)
 s=$=([pw($](v,m),2)$) v in xs])
 $! ac($U(s,n if pop $& n-1))
$, stddev(L,pop=$2):
 $! nice($N(variance(L,pop)))
$, sorta(L):
 $! lst(sorted($K(L[1:]),key=sortkey))
$, sortd(L):
 $! lst(sorted($K(L[1:]),key=sortkey,reverse=$A))
$, deltalist(L):
 xs=$K(L[1:])
 $! lst([$](xs[i+1],xs[i])$) i in $+($1(xs)-1)])
''')
_x(r'''SET={'$r':'rad','mode':'auto','$C':'$R'}
$, lmap(f,a):
 if $e(a):
  $!('$K',)+$0(lmap(f,v)$) v in a[1:])
 if ismat(a):
  $!('mat',)+$0(lmap(f,r)$) r in a[1:])
 $! f(a)
$, lmap2(f,a,b):
 if $e(a)$* $e(b):
  if $1(a)!=$1(b):
   err("Dimension error")
  $!('$K',)+$0(lmap2(f,a[i],b[i])$) i in $+(1,$1(a)))
 if $e(a):
  $!('$K',)+$0(lmap2(f,v,b)$) v in a[1:])
 if $e(b):
  $!('$K',)+$0(lmap2(f,a,v)$) v in b[1:])
 if ismat(a)$* ismat(b):
  $!('mat',)+$0(lmap2(f,a[i],b[i])$) i in $+(1,$1(a)))
 if ismat(a):
  $!('mat',)+$0(lmap2(f,r,b)$) r in a[1:])
 if ismat(b):
  $!('mat',)+$0(lmap2(f,a,r)$) r in b[1:])
 $! f(a,b)
$, vadd(a,b):
 if ismat(a)$* ismat(b):
  $! m_add(a,b)
 if $e(a)or $e(b)or ismat(a)or ismat(b):
  $! lmap2($^,a,b)
 if isrel(a)or isrel(b):
  $! relop($^,a,b)
 if isstr(a)or isstr(b):
  err("Data $/ error")
 $! $^(a,b)
$, vsub(a,b):
 $! vadd(a,vneg(b))
$, vneg(a):
 $! lmap($l,a)if $- isrel(a)$&(a[0],$l(a[1]),$l(a[2]))
$, vmul(a,b):
 if ismat(a)$* ismat(b):
  $! m_mul(a,b)
 if ismat(a)$* $e(b)or $e(a)$* ismat(b):
  $! m_mul(tomat(a),tomat(b)if ismat(b)$& transpose(b))
 if $e(a)or $e(b)or ismat(a)or ismat(b):
  $! lmap2($<,a,b)
 if isrel(a)or isrel(b):
  $! relop($<,a,b)
 $! $<(a,b)
$, vdiv(a,b):
 if ismat(b):
  if ismat(a):
   $! m_mul(a,m_inv(b))
  $! vmul(a,m_inv(b))
 if $e(a)or $e(b)or ismat(a):
  $! lmap2($U,a,b)
 if isrel(a)or isrel(b):
  $! relop($U,a,b)
 if b==0 $* $4(a):
  $! '$H'
 $! $U(a,b)
$, vpow(a,b):
 if ismat(a):
  if $/(b)is $s:
   $! m_pow(a,b)
  if b=='T_t':
   $! transpose(a)
  err("Domain error")
 if $e(a)or $e(b):
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
 $! $((e,'$p')
$, dotop(op,a,b):
 if op=='.*':
  $! lmap2($<,a,b)
 if op=='./':
  $! lmap2($U,a,b)
 $! lmap2(pw,a,b)
$, rel(op,a,b):
 if $e(a)or $e(b):
  $! lmap2($: x,y:rel(op,x,y),a,b)
 if isstr(a)$* isstr(b):
  r=cmpstr(op,a[1],b[1])
  if r is $- $#:
   $! 'true' if r $& 'false'
 d=$.($](a,b))if $-(isstr(a)or isstr(b))$& $#
 if d is $- $# $* $4(d)$* d!='$H':
  ${:
   v=$X(d)
  $5 $7:
   v=$#
  if v is $- $#:
   if $/(v)is $3:
    if op=='=':
     $! 'true' if $J(v)<1e-13 $& 'false'
    if op=='/=':
     $! 'false' if $J(v)<1e-13 $& 'true'
    err("Non-$R comparison")
   if d==0 or $J(v)<1e-300:
    v=0.0
   $&:
    ${:
     sc=$J($X(a))+$J($X(b))
    $5 $7:
     sc=0.0
    if $J(v)<1e-12*(1+sc):
     v=0.0
   r={'=':v==0,'/=':v!=0,'<':v<0,'>':v>0,'<=':v<=0,'>=':v>=0}[op]
   $! 'true' if r $& 'false'
 if d is $- $# $* op in('=','/=')$* $- $4(d):
  ${:
   z=expand_full(d)if hasattr(PO,'expand_full')$& $?(d)
  $5 $7:
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
  $! $A
 if v=='false':
  $! $2
 $! $#
$, land(a,b):
 ta=tobool(a)
 tb=tobool(b)
 if ta is $2 or tb is $2:
  $! 'false'
 if ta is $A:
  $! b
 if tb is $A:
  $! a
 $! flat('$*',a,b)
$, lor(a,b):
 ta=tobool(a)
 tb=tobool(b)
 if ta is $A or tb is $A:
  $! 'true'
 if ta is $2:
  $! b
 if tb is $2:
  $! a
 $! flat('or',a,b)
$, flat(op,a,b):
 xs=[]
 $) v in(a,b):
  if $((v,op):
   xs.$}(v[1:])
  $&:
   xs.$%(v)
 $!(op,)+$0(xs)
$, lnot(a):
 t=tobool(a)
 if t is $- $#:
  $! 'false' if t $& 'true'
 if $n(a):
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
 if $n(a)$* $n(b):
  $! a^b
 $!('xor',a,b)
$, need_int(n):
 if isfl(n)$* finite(n)$* n==$Y.floor(n):
  $! $s(n)
 if $- $n(n):
  err("Argument must be an integer")
 $! n
$, gcd_(a,b):
 if $u(a)$* $u(b):
  an,ad=nd(a)
  bn,bd=nd(b)
  $! Q(igcd(an,bn),ilcm(ad,bd))
 if isfl(a)or isfl(b):
  $! $D(igcd($s(a),$s(b)))
 $! poly_gcd_expr(a,b)
$, lcm_(a,b):
 if $u(a)$* $u(b):
  an,ad=nd(a)
  bn,bd=nd(b)
  $! Q(ilcm(an,bn),igcd(ad,bd))
 g=gcd_(a,b)
 $! $.($U($<(a,b),g))
$, mod_(a,b):
 if $((a,'^')$* $n(a[1])$* $n(a[2])$* a[2]>0 $* $n(b)$* b!=0:
  r=powmod(a[1],a[2],$J(b))
  $! r-$J(b)if b<0 $* r $& r
 if $F(a)$* $F(b):
  if b==0:
   $! a
  $! nsub(a,nmul(b,nfloor(ndiv(a,b))))
 $!('mod',a,b)
$, remain_(a,b):
 if $F(a)$* $F(b):
  if b==0:
   $! a
  q=ndiv(a,b)
  t=nfloor(q)if $`(q)>=0 $&-nfloor(nneg(q))
  $! nsub(a,nmul(b,t))
 $!('remain',a,b)
$, intdiv_(a,b):
 q=ndiv(a,b)
 if $`(q)>=0:
  $! nfloor(q)
 $!-nfloor(nneg(q))
$, bigcomb(n,k):
 if $-($n(n)$* $n(k))or k<=0:
  $! $2
 m=min(k,$J(n-k))if n>=k $& k
 $! m*ibits(n)>MAXBITS
$, ncr_(n,k):
 if $n(n)$* $n(k):
  if k<0 or(n>=0 $* k>n):
   $! 0
  if bigcomb(n,k):
   $!('ncr',n,k)
  $! binom(n,k)if n>=0 $& gen_ncr(n,k)
 if $n(k)$* k>=0:
  $! gen_ncr(n,k)
 if isfl(n)or isfl(k):
  $! CA_gamma_ratio(n,k)
 $!('ncr',n,k)
$, gen_ncr(n,k):
 r=1
 $) i in $+(k):
  r=$<(r,$](n,i))
 f=1
 $) i in $+(2,k+1):
  f*=i
 $! $<(r,Q(1,f))
''')
_x(r'''$, npr_(n,k):
 if $n(n)$* $n(k)$* k*ibits(n)>MAXBITS:
  $!('npr',n,k)
 if $n(k)$* k>=0:
  r=1
  $) i in $+(k):
   r=$<(r,$](n,i))
  $! r
 $!('npr',n,k)
$, CA_gamma_ratio(n,k):
 n=tofl(n)
 k=tofl(k)
 $! gamma(n+1)/(gamma(k+1)*gamma(n-k+1))
$, isprime_(n):
 n=need_int(n)
 if $J(n)>>1024:
  err('Number too large $) isPrime')
 $! 'true' if isprime($J(n))$& 'false'
$, round_(x,d=0):
 if $4(x)$* $- $F(x):
  x=evalf(x)
 if $F(x):
  if $u(x)$* d==0:
   $! nfloor(nadd(x,$v))if $`(x)>=0 $&-nfloor(nadd(nneg(x),$v))
  v=tofl(x)
  if $- finite(v):
   $! x
  p=10.0**d
  r=$Y.floor($J(v)*p+0.5)/p
  $! r if v>=0 $&-r
 $!('round',x,d)
$, ipart_(x):
 if $4(x)$* $- $F(x):
  x=evalf(x)
 if $F(x):
  if $/(x)is $D:
   $! $D($s(x))
  $! nfloor(x)if $`(x)>=0 $&-nfloor(nneg(x))
 $!('ipart',x)
$, fpart_(x):
 i=ipart_(x)
 if $((i,'ipart'):
  $!('fpart',x)
 $! $](x,i)
$, approx_(e):
 $! evalf(e)
$, exact_(e,tol=$#):
 if tol is $- $#:
  tol=tofl(tol)
 $! exactify(e,tol)
$, approxfraction(e,tol=$#):
 t=tofl(tol)if tol is $- $# $& 5e-14
 $! lmap($: v:float2rat(tofl(evalf(v)),t)if $4(v)$& exactify(v,t),e)
$, left_(e,n=$#):
 if isrel(e):
  $! e[1]
 if $e(e):
  $!('$K',)+e[1:1+n]
 if isstr(e):
  $!('$p',e[1][:n])
 err("Argument error")
$, right_(e,n=$#):
 if isrel(e):
  $! e[2]
 if $e(e):
  $!('$K',)+(e[$1(e)-n:]if n $&())
 if isstr(e):
  $!('$p',e[1][$1(e[1])-n:]if n $& '')
 err("Argument error")
$, mid_(e,start,n=$#):
 if isstr(e):
  s=e[1][start-1:]
  $!('$p',s if n is $# $& s[:n])
 xs=$K(e[1:])[start-1:]
 $!('$K',)+$0(xs if n is $# $& xs[:n])
$, dim_(e):
 if $e(e):
  $! $1(e)-1
 if ismat(e):
  r,c=dims(e)
  $!('$K',r,c)
 if isstr(e):
  $! $1(e[1])
 err("Argument error")
$, max_(a,b=$#):
 if b is $#:
  xs=$K(a[1:])if $e(a)$&[a]
  $! maxexpr(xs)
 $! lmap2($: x,y:x if cmpv(x,y)>=0 $& y,a,b)
$, min_(a,b=$#):
 if b is $#:
  xs=$K(a[1:])if $e(a)$&[a]
  best=$#
  bv=$#
  $) x in xs:
   v=$X(x)
   if best is $# or v<bv:
    best=x
    bv=v
  $! best
 $! lmap2($: x,y:x if cmpv(x,y)<=0 $& y,a,b)
$, cmpv(x,y):
 if $4(x)$* $4(y):
  d=$X($](x,y))
  d=d.$R if $/(d)is $3 $& d
  $! 1 if d>0 $&(-1 if d<0 $& 0)
 err("Cannot compare")
$, when_(c,a,b=$#,u=$#):
 if b=='$H':
  b=$#
 t=tobool(c)
 if t is $A:
  $! a
 if t is $2:
  $! b if b is $- $# $& '$H'
 if b is $#:
  $!('when',c,a)
 if u is $#:
  $!('when',c,a,b)
 $! u
$, piecewise_(*a):
 a=$K(a)
 if $1(a)<2:
  err('Wrong number of arguments')
 if $1(a)%2==1:
  r=a[-1]
  a=a[:-1]
 $&:
  r=$#
 $) i in $+($1(a)-2,-1,-2):
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
 $) c in L[1:]:
  r=$^($<(r,x),c)
 $! $?(r)
$, randpoly(v,n):
 import random
 $! $=([$<(random.randint(-9,9),pw(v,k))$) k in $+(n+1)])
$, randmat(r,c):
 import random
 $! mk([[random.randint(-9,9)$) _ in $+(c)]$) _ in $+(r)])
$, newmat(r,c):
 $! mk([[0]*c $) _ in $+(r)])
$, newlist(n):
 $!('$K',)+(0,)*n
$, rand_(n=$#):
 import random
 if n is $#:
  $! random.random()
 $!('$K',)+$0(random.random()$) _ in $+(n))
$, randint_(a,b,n=$#):
 import random
 if n is $#:
  $! random.randint(a,b)
 $!('$K',)+$0(random.randint(a,b)$) _ in $+(n))
$, count_(*$M):
 n=0
 $) a in $M:
  n+=($1(a)-1)if $e(a)$& 1
 $! n
$, erf(x):
 if $J(x)<2.5:
  s=0.0
  t=x
  k=0
  $G $A:
   term=t/(2*k+1)
   s+=term
   k+=1
   t=-t*x*x/k
   if $J(term)<1e-17:
    $O
  $! 2/$Y.$N($Y.pi)*s
 z=$J(x)
 t=0.0
 $) k in $+(60,0,-1):
  t=(k/2.0)/(z+t)
 erfc=$Y.exp(-z*z)/$Y.$N($Y.pi)/(z+t)
 $!(1-erfc)if x>0 $&(erfc-1)
$, numarg(v):
 if v=='$P':
  $! $D('$P')
 if v==('*',-1,'$P'):
  $! $D('-$P')
 if $4(v):
  x=cv(v)if $- $F(v)$& tofl(v)
  if x is $- $# $* $/(x)is $- $3:
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
  $! 0.5*(1+erf(z/$Y.$N(2)))
 $! F(hi)-F(lo)
$, normpdf(x,mu=0.0,sig=1.0):
 x=numarg(x)
 s=numarg(sig)
 $! $Y.exp(-0.5*((x-numarg(mu))/s)**2)/(s*$Y.$N(2*$Y.pi))
$, invnorm(p,mu=0.0,sig=1.0):
 p=numarg(p)
 mu=numarg(mu)
 sig=numarg(sig)
 if $- 0<p<1:
  err('Area must be between 0 $* 1')
 lo,hi=-40.0,40.0
 $) _ in $+(200):
  m=0.5*(lo+hi)
  if 0.5*(1+erf(m/$Y.$N(2)))<p:
   lo=m
  $&:
   hi=m
 $! mu+sig*0.5*(lo+hi)
$, binompdf(n,p,x=$#):
 if x is $#:
  $!('$K',)+$0(binompdf(n,p,k)$) k in $+(n+1))
 if $u(p):
  $! $<(binom(n,x),pw(p,x),pw($](1,p),n-x))
 p=tofl(p)
 $! binom(n,x)*p**x*(1-p)**(n-x)
$, binomcdf(n,p,a,b=$#):
 if b is $#:
  a,b=0,a
 $! $=([binompdf(n,p,k)$) k in $+($s(a),$s(b)+1)])
$, poisspdf(lam,x):
 $! evalf($<(pw(lam,x),pw('e',$l(lam)),Q(1,fact_int(x))))
$, poisscdf(lam,a,b=$#):
 if b is $#:
  a,b=0,a
 $! $=([poisspdf(lam,k)$) k in $+($s(a),$s(b)+1)])
$, geompdf(p,x):
 $! $<(p,pw($](1,p),x-1))
$, geomcdf(p,a,b=$#):
 if b is $#:
  a,b=1,a
 $! $=([geompdf(p,k)$) k in $+($s(a),$s(b)+1)])
$, fact_int(n):
 r=1
 $) k in $+(2,n+1):
  r*=k
 $! r
$, toang(x):
 a=SET['$r']
 if a=='deg':
  $! $<(x,$U('pi',180))
 if a=='grad':
  $! $<(x,$U('pi',200))
 $! x
''')
_x(r'''$, fromang(x):
 a=SET['$r']
 if a=='deg':
  $! $?($<(x,$U(180,'pi')))
 if a=='grad':
  $! $?($<(x,$U(200,'pi')))
 $! x
TRIG=('sin','cos','tan','sec','csc','cot')
ITRIG=('$|','arccos','$w','arcsec','arccsc','arccot')
$, mathfn($B):
 $, f(*a):
  if $B in TRIG $* SET['$r']!='rad':
   $! lmap($: u:fn($B,toang(u)),a[0])
  if $B in ITRIG $* SET['$r']!='rad':
   $! lmap($: u:fromang(fn($B,u)),a[0])
  if $1(a)==1:
   $! lmap($: u:fn($B,u),a[0])
  $! fn($B,*a)
 $! f
$, angle_fn(z):
 $! lmap($: u:fromang(fn('$r',u)),z)
F={}
$) _n in('sin','cos','tan','sec','csc','cot','$|','arccos',
 '$w','arcsec','arccsc','arccot','sinh','cosh','tanh',
 'sech','csch','coth','arcsinh','arccosh','arctanh',
 'arcsech','arccsch','arccoth','ln','exp','$J','sign',
 'floor','ceiling','$R','imag','conj','fact'):
 F[_n]=mathfn(_n)
ALIAS={'asin':'$|','acos':'arccos','atan':'$w','asinh':'arcsinh',
 'acosh':'arccosh','atanh':'arctanh','ceil':'ceiling',
 'factorial':'fact','derivative':'d','$L':'$L',
 'int_':'$L','sumseq':'sumseq','prodseq':'prodseq',
 'lim':'$z','nderiv':'nderivative','polycoef':'polycoeffs',
 'stddevsamp':'stddev','varsamp':'variance','cumsum':'cumulativesum',
 'nsolve':'nsolve','arg':'$r','inv':'inverse','mat2list':'matlist',
 'list2mat':'listmat','explist':'explist','tran':'transpose',
 'log10':'log10','sqr':'$N','diff':'d','deriv':'d',
 'differentiate':'d','integrate':'$L','avg':'mean',
 'average':'mean'}
F['$N']=$: u:lmap($N,u)
F['root']=$: u,n=2:lmap($: v:fn('root',v,n),u)
F['cbrt']=$: u:lmap($: v:fn('root',v,3),u)
F['log']=$: u,b=$#:lmap($: v:fn('ln',v)if b is $# $& fn('log',v,b),u)
F['atan2']=$: y,x:lmap2($: b,a:fromang(fn('$r',$^(a,$<('i',b)))),y,x)
F['log10']=$: u:lmap($: v:fn('log',v,10),u)
F['$r']=angle_fn
F['round']=$: x,d=0:lmap($: v:round_(v,d),x)
F['ipart']=$: x:lmap(ipart_,x)
F['$s']=$: x:lmap($: v:fn('floor',v),x)
F['fpart']=$: x:lmap(fpart_,x)
F['gcd']=$: a,b:lmap2(gcd_,a,b)
F['lcm']=$: a,b:lmap2(lcm_,a,b)
F['mod']=$: a,b:lmap2(mod_,a,b)
F['remain']=$: a,b:lmap2(remain_,a,b)
F['intdiv']=$: a,b:lmap2(intdiv_,a,b)
F['ncr']=$: a,b:lmap2(ncr_,a,b)
F['npr']=$: a,b:lmap2(npr_,a,b)
F['isprime']=isprime_
F['approx']=approx_
F['exact']=exact_
F['approxrational']=approxfraction
F['getnum']=$: e:lmap(getnum,e)
F['getdenom']=$: e:lmap(getden,e)
F['polyeval']=polyeval
F['polygcd']=$: a,b:poly_gcd_expr(a,b)
F['randpoly']=randpoly
F['texpand']=$: e:lmap($: v:texpand(v),e)
F['tcollect']=$: e:lmap($: v:tcollect(v),e)
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
F['rref']=$: A,tol=$#:rref(A,$A)
F['ref']=$: A,tol=$#:ref_(A)
F['inverse']=m_inv
F['rowdim']=$: A:dims(A)[0]
F['coldim']=$: A:dims(A)[1]
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
F['lu']=$: A,tol=$#:('$K',)+lu(A)
F['qr']=$: A,tol=$#:('$K',)+qr(A)
F['newmat']=newmat
F['newlist']=newlist
F['randmat']=randmat
F['matlist']=matlist
F['listmat']=listmat
F['simult']=simult
F['cumulativesum']=cumsum
F['sum']=$: L,a=1,b=$#:lsum(L,a,b)if $e(L)$& colwise(L,lsum)
F['product']=$: L,a=1,b=$#:lprod(L,a,b)if $e(L)$& colwise(L,lprod)
F['mean']=$: L,f=$#:mean(L,f)if $e(L)$& colwise(L,mean)
F['median']=median
F['stddev']=$: L:stddev(L)
F['stddevpop']=$: L:stddev(L,$A)
F['variance']=$: L:variance(L)
F['varpop']=$: L:variance(L,$A)
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
F['getmode']=$:*a:('$p','$r='+SET['$r']+' mode='+SET['mode']+' $C='+SET['$C'])
$, colwise(M,f):
 cols=$[(transpose(M))
 $! mk([[f(('$K',)+$0(c))$) c in cols]])
$, ref_(A):
 $! rref(A,$2)
$, conv(e,$B,$M):
 if $B=='decimal':
  $! evalf(e)
 if $B=='approxfraction':
  $! approxfraction(e,$M[0]if $M $& $#)
 if $B in('dms','dd','rad','grad','deg'):
  $! angconv(e,$B)
 if $B=='polar':
  if $e(e)or ismat(e):
   $! polar_vec(e)
  r=$.(fn('$J',e))
  th=fn('$r',e)
  $!('$p','('+fmt(r)+'\u2220'+fmt(fromang(th))+')')
 if $B=='rect':
  if $e(e)or ismat(e):
   $! e
  r,i=reim(e)
  $! $^(r,$<('i',i))
 if $B=='cylind':
  $! cylind(e)
 if $B=='sphere':
  $! sphere(e)
 if $B in('base2','base10','base16'):
  $! baseconv(e,$B)
 if $B=='exp':
  $! toexp(e)
 if $B=='ln':
  $! toln(e)
 if $B=='logbase':
  $! tologbase(e,$M[0])
 if $B=='sin':
  $! pyth_to(e,'sin')
 if $B=='cos':
  $! pyth_to(e,'cos')
 err("Unknown conversion "+$B)
''')
_x(r'''$, angconv(e,$B):
 if $B=='dms':
  v=tofl(evalf(e))
  if SET['$r']=='rad':
   v=v*180/$Y.pi
  $@ SET['$r']=='grad':
   v=v*0.9
  sg='-' if v<0 $& ''
  v=$J(v)
  d=$s(v)
  m=$s((v-d)*60)
  s=((v-d)*60-m)*60
  if s>59.9999995:
   s=0.0
   m+=1
  if m==60:
   m=0
   d+=1
  ss=('%.4f'%s).rstrip('0').rstrip('.')
  $!('$p',sg+$p(d)+'\u00b0'+$p(m)+"'"+ss+'"')
 if $B=='dd':
  if SET['$r']=='rad':
   $! evalf($<(e,$U(180,'pi')))
  $! evalf(e)
 if $B=='rad':
  if SET['$r']=='deg':
   $! $<(e,$U('pi',180))
  if SET['$r']=='grad':
   $! $<(e,$U('pi',200))
  $! e
 if $B=='grad':
  if SET['$r']=='deg':
   $! $<(e,Q(10,9))
  if SET['$r']=='rad':
   $! $<(e,$U(200,'pi'))
  $! e
 if SET['$r']=='rad':
  $! $<(e,$U(180,'pi'))
 $! e
$, baseconv(e,$B):
 n=need_int(e)
 if $B=='base10':
  $! n
 if $B=='base2':
  s=bin(n)if n>=0 $& '-'+bin(-n)
  $!('$p',s.replace('0b','0b'))
 s=hex(n)if n>=0 $& '-'+hex(-n)
 $!('$p',s.replace('0x','0h').upper().replace('0H','0h'))
$, toexp(e):
 if $/(e)is $- $0 or e[0]=='Q':
  $! e
 $M=[toexp(a)$) a in e[1:]]
 h=e[0]
 if $1($M)==1:
  u=$M[0]
  if h=='sinh':
   $! $<($v,$](pw('e',u),pw('e',$l(u))))
  if h=='cosh':
   $! $<($v,$^(pw('e',u),pw('e',$l(u))))
  if h=='tanh':
   $! $U($](pw('e',u),pw('e',$l(u))),$^(pw('e',u),pw('e',$l(u))))
  if h=='sin':
   iu=$<('i',u)
   $! $U($](pw('e',iu),pw('e',$l(iu))),$<(2,'i'))
  if h=='cos':
   iu=$<('i',u)
   $! $<($v,$^(pw('e',iu),pw('e',$l(iu))))
  if h=='arcsinh':
   $! fn('ln',$^(u,$N($^(pw(u,2),1))))
  if h=='arccosh':
   $! fn('ln',$^(u,$N($](pw(u,2),1))))
  if h=='arctanh':
   $! $<($v,fn('ln',$U($^(1,u),$](1,u))))
 $! simp((h,)+$0($M))
$, toln(e):
 if $/(e)is $- $0 or e[0]=='Q':
  $! e
 $M=[toln(a)$) a in e[1:]]
 if e[0]=='log':
  b=$M[1]if $1($M)>1 $& 10
  $! $U(fn('ln',$M[0]),fn('ln',b))
 $! simp((e[0],)+$0($M))
$, tologbase(e,b):
 e=toln(e)
 $, walk(t):
  if $/(t)is $- $0 or t[0]=='Q':
   $! t
  if t[0]=='ln':
   $! $U(('log',walk(t[1]),b),('log','e',b))
  $!(t[0],)+$0(walk(a)$) a in t[1:])
 $!('hold',walk(e))
''')
_x(r'''VERSION='1.1'
ENV={}
UFUN={}
ASSUME=[]
STATE={'ans':0,'$C':$2,'tmpf':[]}
COMPLEXF=('csolve','czeros','cfactor','cpolyroots','eigvl','eigvc','conj',
 '$R','imag','$r')
$, isfunc(n):
 $!(n in F or n in SF or n in UFUN or n in ALIAS
 or n in STATE['tmpf']or n in('expr','$N','log','root'))
$, lookup(n):
 if n in ENV:
  $! ENV[n]
 if n=='ans':
  $! STATE['ans']
 if n=='i':
  STATE['$C']=$A
 $! n
$, ev(t):
 tt=$/(t)
 if tt is $s or tt is $D:
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
 if h=='$l':
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
  $! lmap($: a:fn('fact',a),ev(t[1]))
 if h=='%':
  $! lmap($: a:$U(a,100),ev(t[1]))
 if h=='deg':
  v=ev(t[1])
  if SET['$r']=='rad':
   $! lmap($: a:$<(a,$U('pi',180)),v)
  if SET['$r']=='grad':
   $! lmap($: a:$<(a,Q(10,9)),v)
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
 if h=='$K':
  $!('$K',)+$0(ev(a)$) a in t[1:])
 if h=='mat':
  $!('mat',)+$0(('$K',)+$0(ev(a)$) a in r[1:])$) r in t[1:])
 if h=='$p':
  $! t
 if h=='&':
  a=ev(t[1])
  b=ev(t[2])
  $!('$p',string_(a)[1]+string_(b)[1])
 if h=='index':
  $! ev_index(ev(t[1]),[ev(a)$) a in t[2:]])
 if h=='prime':
  $! t[1]+"'"*t[2]
 if h=='primecall':
  $!('call',t[1]+"'"*t[2])+$0(ev(a)$) a in t[3:])
 if h=='polar':
  STATE['$C']=$A
  $! $<(ev(t[1]),pw('e',$<('i',toang(ev(t[2])))))
 if h=='conv':
  $! ev_conv(t)
 err('Syntax error')
$, evw(raw,names):
 saved={}
 $) n in names:
  if n in ENV:
   saved[n]=ENV.pop(n)
 ${:
  $! ev(raw)
 finally:
  $) n in saved:
   ENV[n]=saved[n]
$, split_and(c):
 if $((c,'$*'):
  $! split_and(c[1])+split_and(c[2])
 $![c]
$, ev_with(t):
 conds=split_and(t[2])
 pairs={}
 ineq=[]
 $) c in conds:
  if $((c,'=')$* $/(c[1])is $p:
   pairs[c[1]]=ev(c[2])
  $&:
   v=evw(c,$K(pairs.keys()))
   if $((v,'$*'):
    ineq.$}($K(v[1:]))
   $@ v!='true':
    ineq.$%(v)
 n0=$1(ASSUME)
 ASSUME.$}(ineq)
 ${:
  r=evw(t[1],$K(pairs.keys()))
 finally:
  del ASSUME[n0:]
 if pairs:
  r=subsd(unhold(r),pairs)
 $) c in ineq:
  r=assume_sign(r,c)
 $! r
$, assume_sign(r,c):
 h=head(c)
 if h $- in('<','>','<=','>='):
  $! r
 a,b=c[1],c[2]
 if $/(a)is $p $* b==0:
  v=a
  pos=h in('>','>=')
 $@ $/(b)is $p $* a==0:
  v=b
  pos=h in('<','<=')
 $&:
  $! r
 rep=v if pos $& $l(v)
 r=$W(r,('$J',v),rep)
 r=$W(r,('sign',v),1 if pos $&-1)
 $! r
$, target_fn(t):
 if $((t,'call'):
  $! t[1],[p $) p in t[2:]]
 if $((t,'*')$* $/(t[1])is $p:
  p=t[2]
  $! t[1],[p]
 $! $#
$, ev_store(raw,tgt):
 tf=target_fn(tgt)
 if tf is $- $#:
  $! ev_define(tgt,raw)
 if $/(tgt)is $- $p:
  err('Invalid variable $B')
 if tgt in SPECIAL or tgt in F or tgt in SF:
  err('Reserved $B')
 v=ev(raw)
 ENV[tgt]=unhold(v)if $- $((v,'$p')$& v
 $! v
$, ev_define(lhs,rhs):
 tf=target_fn(lhs)
 if tf is $#:
  if $/(lhs)is $p:
   $! ev_store(rhs,lhs)
  err('Invalid definition')
 $B,params=tf
 $) p in params:
  if $/(p)is $- $p:
   err('Invalid parameter')
 body=unhold(evw(rhs,params))
 UFUN[$B]=(params,body)
 if $B in STATE['tmpf']:
  STATE['tmpf'].remove($B)
 $!('$p','Done')
$, ev_index(a,idx):
 if $- idx:
  err('Invalid index')
 if $((a,'$K'):
  i=idx[0]
  if $- $n(i)or i<1 or i>=$1(a):
   err('Invalid index')
  $! a[i]
 if $((a,'mat'):
  $) k in idx:
   if $- $n(k)or k<1:
    err('Invalid index')
  if $1(idx)==1:
   if $1(a)==2:
    if idx[0]>=$1(a[1]):
     err('Invalid index')
    $! a[1][idx[0]]
   if idx[0]>=$1(a):
    err('Invalid index')
   $!('mat',a[idx[0]])
  if idx[0]>=$1(a)or idx[1]>=$1(a[idx[0]]):
   err('Invalid index')
  $! a[idx[0]][idx[1]]
 if $((a,'$p'):
  k=idx[0]
  if $1(idx)!=1 or $- $n(k)or k<1 or k>$1(a[1]):
   err('Invalid index')
  $!('$p',a[1][k-1])
 err('Invalid index')
$, ev_conv(t):
 e=t[1]
 $B=t[2]
 $M=[ev(a)$) a in t[3:]]
 if $B=='$K':
  if e=='exp':
   $! explist($M[0],$M[1])
  if e=='mat':
   $! matlist($M[0])
  err('Unknown conversion')
 if $B=='mat' $* e=='$K':
  $! listmat(*$M)
 v=ev(e)
 v=finalize(v,$A)
 $! builtin($B,conv,(v,$B,$M))
$, explist(e,v):
 $9=[]
 $~=e[1:]if $((e,'or')$&(e,)
 $) p in $~:
  if $((p,'=')$* p[1]==v:
   $9.$%(p[2])
 $!('$K',)+$0($9)
$, call($B,raw):
 $B=ALIAS.get($B,$B)
 if $B in UFUN:
  params,body=UFUN[$B]
  $M=[ev(a)$) a in raw]
  if $1($M)!=$1(params):
   err('Wrong number of arguments')
  $! subsd(body,dict(zip(params,$M)))
 f=SF.get($B)
 if f is $- $#:
  if $B in COMPLEXF:
   STATE['$C']=$A
  $! builtin($B,f,(raw,))
 f=F.get($B)
 if f is $- $#:
  $M=[ev(a)$) a in raw]
  if $B in COMPLEXF:
   STATE['$C']=$A
  $! builtin($B,f,$M)
 if $B=='expr':
  s=ev(raw[0])
  $! ev(parse(s[1],isfunc))
 $M=[ev(a)$) a in raw]
 $!('call',$B)+$0($M)
''')
_x(r'''$, builtin($B,f,$M):
 ${:
  $! f(*$M)
 $5 $S as ex:
  if $p(ex).$y('Wrong number of arguments'):
   argerr($B)
  $k
 $5 TypeError as ex:
  msg=$p(ex)
  if 'positional' in msg or 'takes' in msg or 'required' in msg or 'missing' in msg:
   argerr($B)
  err('Invalid argument $) '+$B)
 $5(IndexError,$T,AttributeError,KeyError):
  err('Invalid argument $) '+$B)
 $5 $a:
  err('Number too large in '+$B)
$, tinames():
 c=STATE.get('tinames')
 if c is $#:
  _load('cashelp')
  c={}
  $) key,title,words in CATS:
   $) wd in words.split():
    if wd[0].isalpha():
     c[wd.lower()]=wd
  STATE['tinames']=c
 $! c
$, argerr($B):
 _load('cashelp')
 n=tinames().get($B,$B)
 sy=SYN.get($B)
 err('Wrong number of arguments $) '+n+('\n'+sy.split('\n')[0]if sy $& ''))
$, suggest($B):
 if $1($B)<4:
  $! $#
 best=$#
 $) k in tinames():
  if $J($1(k)-$1($B))>1:
   $6
  if close(k,$B.lower()):
   best=tinames()[k]
   $O
 $! best
$, close(a,b):
 if a==b:
  $! $2
 if $1(a)==$1(b):
  d=[i $) i in $+($1(a))if a[i]!=b[i]]
  if $1(d)==2 $* d[1]==d[0]+1 $* a[d[0]]==b[d[1]]$* a[d[1]]==b[d[0]]:
   $! $A
  $! $1(d)==1
 if $1(a)>$1(b):
  a,b=b,a
 $) i in $+($1(b)):
  if b[:i]+b[i+1:]==a:
   $! $A
 $! $2
$, unknown_calls(e,$9):
 if $/(e)is $- $0 or $- e or e[0]=='Q':
  $!
 if e[0]=='call' $* e[1]$- in UFUN $* e[1]$- in STATE['tmpf']$* e[1]$- in $9:
  $9.$%(e[1])
 $) a in e[1:]:
  unknown_calls(a,$9)
$, var_of(raw):
 if $/(raw)is $p:
  $! raw,$#
 if $((raw,'='):
  if $/(raw[1])is $- $p:
   err('Variable expected')
  $! raw[1],ev(raw[2])
 err('Variable expected')
$, nargs(a,lo,hi):
 if $1(a)<lo or $1(a)>hi:
  err('Wrong number of arguments')
$, $j(a,k=1):
 v,val=var_of(a[k])
 e=unhold(evw(a[0],[v]))
 $! e,v,val
$, post_subst(r,v,val):
 if val is $- $#:
  $! $W(r,v,val)
 if v in ENV:
  $! $W(r,v,ENV[v])
 $! r
$, sf_d(a):
 nargs(a,2,3)
 e,v,val=$j(a)
 n=ev(a[2])if $1(a)>2 $& 1
 if $- $n(n):
  err('Order must be an integer')
 r=lmap($: u:nice(diff(u,v,n)),e)
 $! post_subst(r,v,val)
$, sf_int(a):
 nargs(a,2,4)
 e,v,val=$j(a)
 if $1(a)==2:
  $! lmap($: u:nice(integrate(u,v)),e)
 if $1(a)==3:
  c=ev(a[2])
  $! lmap($: u:$^(nice(integrate(u,v)),c),e)
 lo=ev(a[2])
 hi=ev(a[3])
 $! lmap($: u:nice(defint(u,v,lo,hi)),e)
$, sf_limit(a):
 nargs(a,3,4)
 e,v,val=$j(a)
 pt=ev(a[2])
 dirn=0
 if $1(a)>3:
  d=ev(a[3])
  if $- $F(d):
   err('Direction must be -1, 0 or 1')
  dirn=0 if d==0 $&(1 if $`(d)>0 $&-1)
 $, L(u):
  r=$z(u,v,pt,dirn)
  if $((r,'$z'):
   $!('$z',u,v,pt)if dirn==0 $&('$z',u,v,pt,dirn)
  $! nice(r)
 $! lmap(L,e)
$, cs_bounds(a,i):
 $! ev(a[i]),ev(a[i+1])
$, sf_sum(a):
 nargs(a,4,4)
 e,v,val=$j(a)
 lo,hi=cs_bounds(a,2)
 r=sumseq(e,v,lo,hi)
 $! prefer_fact(nice(r))
$, prefer_fact(r):
 if $((r,'+')$* $- $_(r)$* $1($g(r))==1:
  ${:
   f=factor_expr(r)
   if $((f,'hold')$* $((f[1],'*'):
    $! f
  $5 $7:
   pass
 $! r
$, sf_prod(a):
 nargs(a,4,4)
 e,v,val=$j(a)
 lo,hi=cs_bounds(a,2)
 $! prodseq(e,v,lo,hi)
$, sf_seq(a):
 nargs(a,4,5)
 e,v,val=$j(a)
 lo,hi=cs_bounds(a,2)
 st=ev(a[4])if $1(a)>4 $& 1
 $9=[]
 k=lo
 cnt=0
 $G ncmp(k,hi)<=0 if $F(k)$& $2:
  $9.$%($W(e,v,k))
  k=nadd(k,st)
  cnt+=1
  if cnt>5000:
   err('Too many elements')
 $!('$K',)+$0($9)
$, sf_taylor(a):
 nargs(a,3,4)
 e,v,val=$j(a)
 n=ev(a[2])
 pt=ev(a[3])if $1(a)>3 $& 0
 $! lmap($: u:taylor(u,v,n,pt),e)
$, sf_series(a):
 nargs(a,3,4)
 e,v,val=$j(a)
 n=ev(a[2])
 pt=ev(a[3])if $1(a)>3 $& 0
 $! lmap($: u:series_cmd(u,v,n,pt),e)
$, sf_dominant(a):
 nargs(a,2,3)
 e,v,val=$j(a)
 pt=ev(a[2])if $1(a)>2 $& 0
 $! lmap($: u:dominant(u,v,pt),e)
$, solvevars(rawvs):
 vs=[]
 gs=[]
 $) r in rawvs:
  if $((r,'$K'):
   $) q in r[1:]:
    v,g=var_of(q)
    vs.$%(v)
    gs.$%(g)
  $&:
   v,g=var_of(r)
   vs.$%(v)
   gs.$%(g)
 $! vs,gs
$, eqlist(e):
 if $((e,'$*'):
  $9=[]
  $) p in e[1:]:
   $9.$}(eqlist(p))
  $! $9
 if $((e,'$K'):
  $! $K(e[1:])
 $![e]
$, cons_for(v):
 $9=[]
 $) c in ASSUME:
  if has(c,v):
   $9.$%(c)
 $! $9
$, sf_solve(a,$C=$2):
 if $1(a)<2:
  err('Wrong number of arguments')
 vs,gs=solvevars(a[1:])
 e=evw(a[0],vs)
 eqs=eqlist(e)
 if $1(vs)==1 $* $1(eqs)==1:
  v=vs[0]
  eq=eqs[0]
  if gs[0]is $- $#:
   f=$](eq[1],eq[2])if $((eq,'=')$& eq
   r=nsolve(f,v,tofl(evalf(gs[0])))
   $!('=',v,r)if r is $- $# $& 'false'
  r=solve(eq,v,$C,cons_for(v))
  if r is $#:
   f=$](eq[1],eq[2])if $((eq,'=')$& eq
   ns=numeric_solve(f,v,$C)if head(eq)=='=' or head(eq)is $# $& $#
   if ns:
    r=sols_to_bool(v,apply_constraints(ns,v,cons_for(v)))
   $&:
    $!('solve',eq,v)
  $! finish_sol(r)
 if $1(eqs)>1 $* any([head(q)in('<','>','<=','>=','/=')$) q in eqs]):
  if $1(vs)>1:
   $!('solve',e)+$0(vs)
  $! finish_sol(solve_and(eqs,vs[0],$C))
 $h=solve_system(eqs,vs,$C,gs if any([g is $- $# $) g in gs])$& $#)
 if $h is $#:
  $!('solve',e)+$0(vs)
 if $- $h:
  $! 'false'
 $9=[]
 $) s in $h:
  conj=[('=',v,clean(s.get(v,v)))$) v in vs]
  $9.$%(conj[0]if $1(conj)==1 $&('$*',)+$0(conj))
 $! finish_sol($9[0]if $1($9)==1 $&('or',)+$0($9))
''')
_x(r'''$, solve_and(eqs,v,$C):
 cons=cons_for(v)
 $) i in $+($1(eqs)):
  if head(eqs[i])=='=':
   $f=eqs[:i]+eqs[i+1:]
   r=solve(eqs[i],v,$C,$f+cons)
   if r is $#:
    $!('solve',('$*',)+$0(eqs),v)
   $! r
 ps=rel_pairs(eqs+cons,v)
 r=solve_rels(ps,v)if ps is $- $# $& $#
 if r is $#:
  $!('solve',('$*',)+$0(eqs),v)
 $! r
$, finish_sol(r):
 ns=[]
 $, walk(e):
  if $/(e)is $p $* e[0]=='n' $* e[1:].isdigit()$* e $- in ns:
   ns.$%(e)
  $@ $/(e)is $0 $* e $* e[0]!='Q':
   $) a in e[1:]:
    walk(a)
 walk(r)
 if $- ns or ns==['n%d'%(i+1)$) i in $+($1(ns))]:
  $! r
 tmp=dict([(ns[i],'N%d_'%i)$) i in $+($1(ns))])
 r=subsd(r,tmp)
 $! subsd(r,dict([('N%d_'%i,'n%d'%(i+1))$) i in $+($1(ns))]))
$, sf_csolve(a):
 $! sf_solve(a,$A)
$, sf_zeros(a,$C=$2):
 nargs(a,2,2)
 vs,gs=solvevars(a[1:])
 e=evw(a[0],vs)
 if $1(vs)==1 $* $- $((e,'$K'):
  r=zeros(e,vs[0],$C,cons_for(vs[0]))
  if r is $#:
   ns=numeric_solve(e,vs[0],$C)
   $!('$K',)+$0(ns or[])
  $! r
 eqs=eqlist(e)
 $h=solve_system(eqs,vs,$C)
 if $- $h:
  $!('$K',)
 $! mk([[clean(s.get(v,v))$) v in vs]$) s in $h])
$, sf_czeros(a):
 $! sf_zeros(a,$A)
$, sf_nsolve(a):
 nargs(a,2,4)
 v,g=var_of(a[1])
 e=unhold(evw(a[0],[v]))
 f=$](e[1],e[2])if $((e,'=')$& e
 lo=tofl(evalf(ev(a[2])))if $1(a)>2 $& $#
 hi=tofl(evalf(ev(a[3])))if $1(a)>3 $& $#
 $) c in cons_for(v):
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
 if $/(x)is $- $p or $/(y)is $- $p:
  err('Variable expected')
 $~=split_and(a[0])
 ode=$#
 conds=[]
 $) p in $~:
  if $((p,'=')$* $((p[1],'primecall')$* p[1][1]==y:
   conds.$%((p[1][2],evw(p[1][3],[x,y]),evw(p[2],[x,y])))
  $@ $((p,'=')$* $((p[1],'*')$* p[1][1]==y $* $- hasprime(p):
   conds.$%((0,ev(p[1][2]),ev(p[2])))
  $@ $((p,'=')$* $((p[1],'call')$* p[1][1]==y:
   conds.$%((0,ev(p[1][2]),ev(p[2])))
  $&:
   ode=p
 if ode is $#:
  err('ODE expected')
 o=evw(ode,[x,y,y+"'",y+"''"])
 o=$W($W(o,y+"''",YP[1]),y+"'",YP[0])
 r=desolve(o,x,y,conds)
 if r is $#:
  $!('desolve',o,x,y)
 $! r
$, hasprime(t):
 if $/(t)is $- $0:
  $! $2
 if t[0]in('prime','primecall'):
  $! $A
 $) a in t[1:]:
  if hasprime(a):
   $! $A
 $! $2
$, bnd_args(a,i,v):
 lo=ev(a[i])if $1(a)>i $& $#
 hi=ev(a[i+1])if $1(a)>i+1 $& $#
 cb=bounds(cons_for(v),v)
 if cb is $- $#:
  lo,hi=cb
 $&:
  $) c in cons_for(v):
   h=head(c)
   if h in('>','>=')$* c[1]==v:
    lo=c[2]
   $@ h in('<','<=')$* c[1]==v:
    hi=c[2]
 $! lo,hi
$, sf_fmin(a,kind='min'):
 nargs(a,2,4)
 e,v,val=$j(a)
 lo,hi=bnd_args(a,2,v)
 r=fextreme(e,v,kind,lo,hi)
 if r is $#:
  $!('f'+kind,e,v)
 $! r
$, sf_fmax(a):
 $! sf_fmin(a,'max')
$, sf_nfmin(a,kind='min'):
 nargs(a,2,4)
 e,v,val=$j(a)
 lo,hi=bnd_args(a,2,v)
 $! nfextreme(e,v,kind,tofl(evalf(lo))if lo is $- $# $& $#,
 tofl(evalf(hi))if hi is $- $# $& $#)
$, sf_nfmax(a):
 $! sf_nfmin(a,'max')
$, sf_nint(a):
 nargs(a,4,4)
 e,v,val=$j(a)
 lo,hi=cs_bounds(a,2)
 $! nint_split(e,v,lo,hi)
$, sf_arclen(a):
 nargs(a,4,4)
 e,v,val=$j(a)
 lo,hi=cs_bounds(a,2)
 $! nice(arclen(e,v,lo,hi))
$, pt_arg(a):
 if $1(a)==2 $* $((a[1],'='):
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
 n=ev(a[3])if $1(a)>3 $& 1
 $! impdif(e,x,y,n)
$, rc_args(a):
 v,val=var_of(a[1])
 e=unhold(evw(a[0],[v]))
 h=ev(a[2])if $1(a)>2 $& 0.001
 if val is $#:
  val=v
 $! e,v,val,h
$, sf_avgrc(a):
 nargs(a,2,3)
 e,v,val,h=rc_args(a)
 $! lmap($: u:$?(avgrc(u,v,val,h)),e)
$, sf_central(a):
 nargs(a,2,3)
 e,v,val,h=rc_args(a)
 $! lmap($: u:$?(centraldiff(u,v,val,h)),e)
$, sf_nderiv(a):
 nargs(a,2,3)
 v,val=var_of(a[1])
 e=unhold(evw(a[0],[v]))
 n=ev(a[2])if $1(a)>2 $& 1
 if val is $#:
  val=ENV.get(v)
  if val is $#:
   err('Value required: var=value')
 $! evalf($W(diff(e,v,n),v,val))
$, opt_var(a,i):
 if $1(a)>i:
  v,_=var_of(a[i])
  $! v
 $! $#
$, sf_expand(a):
 nargs(a,1,2)
 v=opt_var(a,1)
 e=ev(a[0])
 $! expand_full(unhold(e),v)
$, sf_factor(a,$C=$2):
 nargs(a,1,2)
 v=opt_var(a,1)
 e=unhold(ev(a[0]))
 $! factor_expr(e,v,$C)
$, sf_cfactor(a):
 $! sf_factor(a,$A)
$, sf_comdenom(a):
 nargs(a,1,2)
 $! comdenom(unhold(ev(a[0])))
$, sf_propfrac(a):
 nargs(a,1,2)
 v=opt_var(a,1)
 $! lmap($: u:propfrac(u,v),unhold(ev(a[0])))
$, polyvar(e,a,i):
 v=opt_var(a,i)
 if v is $#:
  ss=$g(e)
  v='x' if 'x' in ss or $- ss $& ss[0]
 $! v
$, sf_polycoeffs(a):
 nargs(a,1,2)
 e=unhold(ev(a[0]))
 v=polyvar(e,a,1)
 cs=$Z(e,v)
 if cs is $#:
  err('Polynomial expected')
 $G $1(cs)>1 $* cs[-1]==0:
  cs.pop()
 $!('$K',)+$0(reversed(cs))
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
 v=polyvar($^(p,q),a,2)
 cp=$Z(p,v)
 cq=$Z(q,v)
 if cp is $# or cq is $#:
  err('Polynomial expected')
 qq,rr=e_divmod(cp,cq)
 $! fromcoeffs(qq if which==0 $& rr,v)
$, sf_polyrem(a):
 $! sf_polyquo(a,1)
''')
_x(r'''$, sf_polyroots(a,$C=$2):
 nargs(a,1,2)
 if $1(a)==1:
  L=ev(a[0])
  if $- $((L,'$K'):
   err('List expected')
  v='X_'
  e=polyeval(L,v)
 $&:
  v,_=var_of(a[1])
  e=evw(a[0],[v])
 r=zeros(e,v,$C)
 $! r if r is $- $# $&('$K',)
$, sf_cpolyroots(a):
 $! sf_polyroots(a,$A)
$, sf_linsolve(a):
 vs,gs=solvevars(a[1:])
 e=evw(a[0],vs)
 eqs=eqlist(e)
 fs=[eqexpr(q)$) q in eqs]
 if $- is_linear_sys(fs,vs):
  err('Argument error: $i system required')
 $h=linsys(fs,vs)
 if $- $h:
  $! 'false'
 $!('$K',)+$0($h[0][v]$) v in vs)
$, sf_domain(a):
 nargs(a,2,2)
 e,v,val=$j(a)
 r=domain(e,v)
 $! r if r is $- $# $&('domain',e,v)
$, sf_completesq(a):
 nargs(a,2,2)
 v,_=var_of(a[1])
 e=unhold(evw(a[0],[v]))
 if $((e,'='):
  lhs=complete_sq($](e[1],e[2]),v,$A)
  $! lhs
 $! complete_sq(e,v,$2)
$, complete_sq(e,v,eq):
 cs=$Z(e,v)
 if cs is $# or $1(cs)!=3:
  err('Quadratic expected')
 c,b,a=cs
 h=$.($U(b,$<(2,a)))
 k=$.($](c,$U($<(b,b),$<(4,a))))
 sq=('^',$^(v,h),2)
 t=sq if a==1 $&('*',a,sq)
 if eq:
  $!('=',('hold',t),$l(k))
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
 $! mk([[subsd(e,{i:ii,j:jj})$) jj in $+(1,c+1)]$) ii in $+(1,r+1)])
$, sf_charpoly(a):
 nargs(a,2,2)
 A=ev(a[0])
 v=a[1]if $/(a[1])is $p $& ev(a[1])
 $! charpoly(A,v)
$, sf_simplify(a):
 e=unhold(ev(a[0]))
 $! nice(pyth(e))
SF={
 'd':sf_d,'$L':sf_int,'$z':sf_limit,'sumseq':sf_sum,
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
 'linsolve':sf_linsolve,'domain':sf_domain,
 'completesquare':sf_completesq,'constructmat':sf_constructmat,
 'charpoly':sf_charpoly,'simplify':sf_simplify,
 }
$, when_simp(c,a,b=$#):
 t=tobool(rel(c[0],c[1],c[2]))if isrel(c)$& tobool(c)
 if t is $A:
  $! a
 if t is $2:
  $! b if b is $- $# $& '$H'
 $! $#
$q['when']=when_simp
$, finalize(r,quiet=$2):
 if $((r,'$p'):
  $! r
 if $- $((r,'hold'):
  r=$.(r)if $-($((r,'$K')or $((r,'mat'))$& lmap($.,r)
  if needpyth(r):
   r=pyth(r)
  if SET['mode']=='approx' or $_(r):
   r=evalf(r)
  $@ SET['mode']=='exact':
   r=exactify(r)
 if SET['$C']=='$R' $* $- STATE['$C']$* has(r,'i')$* $- quiet:
  err('Non-$R result')
 $! r
$, sqtrig(e,$9):
 if $/(e)is $- $0 or e[0]=='Q':
  $!
 if e[0]=='^' $* head(e[1])in('sin','cos')$* $n(e[2])$* e[2]>=2:
  $9.$%((e[1][0],e[1][1]))
 $) a in e[1:]:
  sqtrig(a,$9)
$, needpyth(r):
 if $- $((r,'+'):
  $! $2
 $9=[]
 sqtrig(r,$9)
 $) n,u in $9:
  if(('cos' if n=='sin' $& 'sin'),u)in $9:
   $! $A
 $! $2
$, pre_register(s):
 low=s.replace(' ','').lower()
 cands=[]
 if ':=' in low:
  cands.$%(low.split(':=')[0])
 if low.$y('define'):
  cands.$%(low[6:].split('=')[0])
 $) arrow in('->','\u2192','=:'):
  if arrow in low:
   cands.$%(low.split(arrow)[-1])
 $) c in cands:
  i=c.find('(')
  if i>0:
   nm=c[:i]
   ok=$A
   $) ch in nm:
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
  SET['$r']='deg'
  $! 'Angle: degree'
 if k in('rad','radian'):
  SET['$r']='rad'
  $! 'Angle: radian'
 if k in('grad','gradian'):
  SET['$r']='grad'
  $! 'Angle: gradian'
 if k in('approx','auto','exact'):
  SET['mode']=k
  $! 'Mode: '+k
 if k in('$R','$3','rect'):
  SET['$C']='$R' if k=='$R' $& 'rect'
  $! 'Complex format: '+SET['$C']
 if k in('digits','$D'):
  if $1(p)>1 $* $- p[1].isdigit():
   $! 'Use :digits n with n from 1 to 15'
  n=$s(p[1])if $1(p)>1 $& 10
  OPT['digits']=max(1,min(15,n))
  $! 'Digits: '+$p(OPT['digits'])
 if k=='ascii':
  OPT['uni']=$2
  $! 'ASCII output'
 if k in('unicode','uni'):
  OPT['uni']=$A
  $! 'Unicode output'
 if k=='vars':
  $9=[]
  $) n in sorted(ENV):
   $9.$%(n+' = '+fmt(ENV[n]))
  $) n in sorted(UFUN):
   ps,b=UFUN[n]
   $9.$%(n+'('+','.join(ps)+') = '+fmt(b))
  $! '\n'.join($9)if $9 $& '(none)'
 if k in('clear','clearaz','reset'):
  ENV.clear()
  UFUN.clear()
  $! 'Cleared'
 if k in('mem','memory'):
  ${:
   import gc
   gc.collect()
   $! 'Memory: %d KB free, %d KB used'%(gc.mem_free()//1024,gc.mem_alloc()//1024)
  $5 $7:
   $! 'Memory information is $- available'
 if k in('mode','modes','getmode'):
  $!('$r='+SET['$r']+' mode='+SET['mode']+' $C='+SET['$C']+
 ' digits='+$p(OPT['digits']))
 if k=='test':
  _load('cashelp')
  saved=(dict(SET),dict(OPT))
  SET.update({'$r':'rad','mode':'auto','$C':'$R'})
  OPT.update({'uni':$A,'digits':10})
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
  $5 ImportError:
   $! 'The key test needs the calculator (ti_system)'
  print('Press keys; esc twice to stop')
  last=''
  $G $A:
   key=get_key(1)
   print(repr(key))
   if key=='esc' $* last=='esc':
    $! ''
   last=key
 if k in('help','?','h'):
  _load('cashelp')
  $! help(p[1]if $1(p)>1 $& $#)
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
 if low.$y('help'):
  $! command(low)
 if low.$y('delvar'):
  $) n in low[6:].replace(',',' ').split():
   ENV.pop(n,$#)
   UFUN.pop(n,$#)
  keep()
  $! 'Done'
 if low in('clearaz','clear'):
  $! command('clear')
 pre_register(s)
 t=parse(s,isfunc)
 STATE['$C']=(SET['$C']!='$R')
 r=ev(t)
 r=finalize(r)
 if $-($((t,'define')or($((r,'$p')$* r[1]=='Done')):
  STATE['ans']=unhold(r)if $- $((r,'$p')$& r
 keep()
 $9=fmt_top(r)
 un=[]
 unknown_calls(r,un)
 $) n in un:
  g=suggest(n)
  if g:
   $9+='\n('+n+' is $- a command; did you mean '+g+'?)'
 $! $9
KEEP='ncasmem'
$, memtext():
 u=OPT['uni']
 OPT['uni']=$2
 ${:
  $9=[':'+SET['$r'],':'+SET['mode'],
 ':'+('$R' if SET['$C']=='$R' $& '$3'),
 ':digits '+$p(OPT['digits'])]
  if $- u:
   $9.$%(':ascii')
  $) n in sorted(ENV):
   $9.$%(n+':='+fmt(ENV[n]))
  $) n in sorted(UFUN):
   ps,b=UFUN[n]
   $9.$%(n+'('+','.join(ps)+'):='+fmt(b))
 finally:
  OPT['uni']=u
 $! '\n'.join([l $) l in $9 if $1(l)<2000 $* all([0<ord(c)<128 $) c in l])])
$, pack(t):
 $9=[]
 $) i in $+(0,$1(t),6):
  n=0
  $) c in reversed(t[i:i+6]):
   n=n*128+ord(c)
  $9.$%(n)
 $! $9
$, unpack(xs):
 cs=[]
 $) v in xs:
  n=$s(round(v))
  $G n:
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
 $5 $7:
  pass
$, restore():
 if STATE.get('kept')is $- $#:
  $!
 STATE['kept']=memtext()
 ${:
  from ti_system import recall_list
  t=unpack(recall_list(KEEP))
 $5 $7:
  $!
 STATE['restoring']=$A
 ${:
  $) line in t.split('\n'):
   ${:
    run(line)
   $5 $7:
    pass
 finally:
  STATE['restoring']=$2
 STATE['ans']=0
 STATE['kept']=memtext()
$, menu():
 _load('casmenu')
 runmenu(run)
GUI=$A
$, gui():
 if $- GUI:
  $! 'The full-screen mode is the separate program ncasgui.'
 ${:
  _load('casgui')
 $5 ImportError as ex:
  if 'casgui' $- in $p(ex):
   $k
  $! 'casgui is $- installed (needed $) the full-screen mode); using text mode.'
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
 $5 ImportError:
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
 $5 $S as ex:
  $! 'Error: '+$p(ex)
$, prompt():
 p=[]
 if SET['$r']!='rad':
  p.$%(SET['$r'])
 if SET['mode']!='auto':
  p.$%(SET['mode'])
 if SET['$C']!='$R':
  p.$%('$C')
 $! ' '.join(p)+'> '
''')
_x(r'''$, cas():
 restore()
 print('nCAS '+VERSION+' $) TI-Nspire CX II')
 print(('? help, m menu, g full screen, q quit')if GUI $& '? help, m menu, q quit')
 blank=0
 $G $A:
  ${:
   s=input(prompt())
  $5(EOFError,$t):
   $O
  s=s.strip()
  if s in('q','quit','exit',':q'):
   $O
  if $- s:
   blank+=1
   if blank>=2:
    print('($/ q $* enter to quit)')
    blank=0
   $6
  blank=0
  if s.lower()in('m','menu'):
   ${:
    menu()
   $5 $7 as ex:
    print('Error: '+$p(ex))
   $6
  if s.lower()in('g','gui'):
   ${:
    r=gui()
   $5 $7 as ex:
    r='Error: '+$p(ex)
   if r:
    print(r)
   $6
  ${:
   $9=run(s)
   if $9:
    print($9)
  $5 $S as ex:
   print('Error: '+$p(ex))
  $5 $E:
   print('Error: Division by zero')
  $5 MemoryError:
   ${:
    import gc
    gc.collect()
   $5 ImportError:
    pass
   print('Error: Out of memory')
  $5 $t:
   print('Break')
  $5 RuntimeError as ex:
   print('Error: Too $3 ('+$p(ex)+')')
  $5 $7 as ex:
   print('Error: '+$p(ex))
''')
_L['cashelp']=(r'''CATS=(
 ('alg','Algebra','solve csolve zeros czeros nsolve linsolve factor cfactor $? comdenom propfrac getnum getdenom completesquare polycoeffs polydegree polyquotient polyremainder polygcd polyroots cpolyroots polyeval tExpand tCollect simplify exact approx domain'),
 ('calc','Calculus','d $L $z sumseq prodseq taylor series dominantTerm deSolve impDif arcLen tangentLine normalLine fMin fMax nfMin nfMax nInt nDerivative avgRC centralDiff'),
 ('mat','Matrix/vector','det identity transpose rref ref inverse eigVl eigVc charPoly LU QR trace norm rowNorm colNorm diag augment colAugment subMat rowSwap rowAdd mRow mRowAdd crossP dotP unitV simult constructMat newMat randMat dim rowDim colDim mat>$K $K>mat'),
 ('num','Numbers','gcd lcm mod remain intDiv isPrime nCr nPr ! floor ceiling round iPart fPart sign $J $R imag conj $r'),
 ('$K','Lists/stats','seq sum product mean median stdDev stdDevPop variance varPop max min sortA sortD cumulativeSum deltaList augment left right mid count normPdf normCdf invNorm binomPdf binomCdf poissPdf poissCdf geomPdf geomCdf'),
 ('conv','Conversions (expr>>$B)','>>Decimal >>approxFraction() >>DMS >>DD >>Rad >>Grad >>Polar >>Rect >>Cylind >>Sphere >>exp >>ln >>logbase() >>sin >>cos >>Base2 >>Base10 >>Base16 exp>$K()'),
 ('cmd','Commands',':deg :rad :grad :auto :exact :approx :$R :$3 :digits n :ascii :unicode :vars :clear :mode :mem  delvar a  q=quit'),
 )
SYN={
 'solve':'solve(eqn,var) solve(eqn,var=guess)\nsolve(ineq,var) solve(eq1 $* eq2,{x,y})\nsolve(...)|x>0  (n1,n2..=any integer)',
 'csolve':'cSolve(eqn,var) $3 solutions',
 'zeros':'zeros(expr,var) -> $K of roots\nzeros({e1,e2},{x,y}) -> matrix',
 'czeros':'cZeros(expr,var) $3 roots',
 'nsolve':'nSolve(eqn,var[=guess][,lo,hi])',
 'linsolve':'linSolve({eq1,eq2},{x,y})',
 'factor':'factor(expr[,var]) factor(integer)\nwith var: irrational factors',
 'cfactor':'cFactor(expr[,var]) $3 factors',
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
 'polyroots':'polyRoots(poly,var) polyRoots({$Z})',
 'cpolyroots':'cPolyRoots(poly,var)',
 'polyeval':'polyEval({$Z},x)',
 'texpand':'tExpand(expr) $? trig of sums/multiples',
 'tcollect':'tCollect(expr) products -> multiple angles',
 'simplify':'simplify(expr) extra simplification',
 'exact':'exact(expr[,tol]) floats -> fractions',
 'approx':'approx(expr) decimal value',
 'domain':'domain(expr,var)',
 'd':'d(expr,var[,order])  d(expr,var)|var=val\nderivative(...) same',
 '$L':'$L(expr,var) antiderivative\nintegral(expr,var,a,b) definite\n(\u222b also accepted)',
 '$z':'$z(expr,var,point[,dir]) dir:-1 left,1 right\npoint may be $P or -$P',
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
 'nint':'nInt(expr,var,a,b) numeric $L',
 'nderivative':'nDerivative(expr,var=val[,order])',
 'avgrc':'avgRC(expr,var[=val][,h])',
 'centraldiff':'centralDiff(expr,var[=val][,h])',
 'det':'det(M)','inverse':'M^-1 or inverse(M)','rref':'rref(M)','ref':'ref(M)',
 'eigvl':'eigVl(M) eigenvalues','eigvc':'eigVc(M) unit eigenvectors (columns)',
 'charpoly':'charPoly(M,var)','lu':'LU(M) -> {L,U,P} with P*M=L*U','qr':'QR(M) -> {Q,R}',
 'simult':'simult(A,b) solves A*x=b','constructmat':'constructMat(expr,i,j,$[,cols)',
 'crossp':'crossP(u,v)','dotp':'dotP(u,v)','unitv':'unitV(v)','norm':'norm(M)',
 'seq':'seq(expr,var,lo,hi[,step])',
 'ncr':'nCr(n,k)','npr':'nPr(n,k)','gcd':'gcd(a,b)','lcm':'lcm(a,b)',
 'mod':'mod(a,b)','isprime':'isPrime(n)',
 'define':'Define f(x)=expr   or   f(x):=expr\nexpr->a  or  a:=expr   delvar a',
 'with':'expr|x=3   expr|x>0   solve(...)|0<=x<=2pi',
 'menu':'m or menu: numbered menus build the\ncommand $) you; 0 back, q quit.\nMatrices may be typed 1,2;3,4',
 'syntax':'implicit mult: 2x  3(x+1)  x(x+1)\n^ or ** power, $N( or \u221a, pi, e, i, $P\n<= >= /= $* or $-, ans = last result\nlog(x)=ln(x) ([ln] key); log10(x), log(x,b)',
 'log':'log(x) natural log (= ln, the [ln] key)\nlog10(x) base 10, log(x,b) base b',
 }
$, help($B=$#):
 if $B is $#:
  $9=['nCAS help: ?topic or ?command']
  $) k,t,items in CATS:
   $9.$%('?'+k+'  '+t)
  $9.$%('?define ?with ?syntax ?menu')
  $9.$%('m = menus (no typing of names)')
  $! '\n'.join($9)
 $B=$B.lower().replace('(','').strip()
 $) k,t,items in CATS:
  if $B==k:
   $! t+':\n'+items
 if $B in SYN:
  $! SYN[$B]
 $) k in SYN:
  if k.$y($B):
   $! SYN[k]
 $! 'No help $) '+$B
''',
r'''SELFTEST=(
 ('factor(x^2-5x+6)','(x-2)*(x-3)'),
 ('$?((x+1)^3)','x^3+3*x^2+3*x+1'),
 ('solve(x^2-5x+6=0,x)','x=2 or x=3'),
 ('solve(x^2=2,x)','x=-\u221a2 or x=\u221a2'),
 ('d(x^3*sin(x),x)','x^3*cos(x)+3*x^2*sin(x)'),
 ('$L(x*e^x,x)','x*e^x-e^x'),
 ('$L(1/(1+x^2),x,0,1)','\u03c0/4'),
 ('$z(sin(x)/x,x,0)','1'),
 ('taylor(e^x,x,3)','x^3/6+x^2/2+x+1'),
 ('sumSeq(k,k,1,n)','n*(n+1)/2'),
 ("deSolve(y'=y,x,y)",'y=c1*e^x'),
 ('det([[1,2][3,4]])','-2'),
 ('[[1,2][3,4]]^-1','[[-2,1][3/2,-1/2]]'),
 ('$N(12)','2*\u221a3'),
 ('cSolve(x^2+1=0,x)','x=-i or x=i'),
 ('factor(360)','2^3*3^2*5'),
 ('solve(x^2-4>0,x)','x<-2 or x>2'),
 ('nSolve(cos(x)=x,x)','0.7390851332'),
 )
$, selftest(run):
 ok=0
 $9=[]
 $) q,a in SELFTEST:
  ${:
   r=run(q)
  $5 $7 as ex:
   r='ERR '+$p(ex)
  if r==a:
   ok+=1
  $&:
   $9.$%('FAIL '+q+' -> '+r)
 $9.$%('%d/%d tests passed'%(ok,$1(SELFTEST)))
 $! '\n'.join($9)
''',)
_L['casmenu']=(r'''ALG=(
 ('Expand','$?(@1`,@2`)',(('$d',$#),('Var (blank=all)',''))),
 ('Factor','factor(@1`,@2`)',(('$d',$#),('Var (blank=Q)',''))),
 ('cFactor','cFactor(@1`,@2`)',(('$d',$#),('Var (blank=all)',''))),
 ('Simplify','simplify(@1)',(('$d',$#),)),
 ('comDenom','comDenom(@1)',(('$d',$#),)),
 ('propFrac','propFrac(@1`,@2`)',(('$d',$#),('Var',''))),
 ('Partial frac','$?(@1,@2)',(('Rational expr',$#),('Var','x'))),
 ('Complete sq','completeSquare(@1,@2)',(('Quadratic/eqn',$#),('Var','x'))),
 ('Poly divide','polyQuotient(@1,@2,@3)',(('Dividend',$#),('Divisor',$#),('Var','x'))),
 ('Poly remain','polyRemainder(@1,@2,@3)',(('Dividend',$#),('Divisor',$#),('Var','x'))),
 ('Poly gcd','polyGcd(@1,@2)',(('Poly 1',$#),('Poly 2',$#))),
 ('Substitute','(@1)|@2=@3',(('$d',$#),('Var','x'),('Value',$#))),
 ('tExpand','tExpand(@1)',(('$d',$#),)),
 ('tCollect','tCollect(@1)',(('$d',$#),)),
 ('Decimal','approx(@1)',(('$d',$#),)),
 ('Exact','exact(@1)',(('$d',$#),)),
 )
CALC=(
 ('Derivative','d(@1,@2`,@3`)',(('f',$#),('Var','x'),('Order',''))),
 ('Deriv at pt','d(@1,@2)|@2=@3',(('f',$#),('Var','x'),('At',$#))),
 ('Integral','$L(@1,@2)',(('f',$#),('Var','x'))),
 ('Def $L','$L(@1,@2,@3,@4)',(('f',$#),('Var','x'),('Lower ($P ok)',$#),('Upper',$#))),
 ('Limit','$z(@1,@2,@3`,@4`)',(('f',$#),('Var','x'),('Point ($P ok)','0'),('Side 1/-1',''))),
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
 ('Zeros','zeros(@1,@2)',(('$d',$#),('Var','x'))),
 ('cZeros','cZeros(@1,@2)',(('$d',$#),('Var','x'))),
 ('nSolve','nSolve(@1,@2`,@3,@4`)',(('Equation',$#),('Var or x=guess','x'),('Lower',''),('Upper',''))),
 ('System 2 eqs','solve(@1 $* @2,{@3})',(('Eq 1',$#),('Eq 2',$#),('Vars','x,y'))),
 ('System 3 eqs','solve(@1 $* @2 $* @3,{@4})',(('Eq 1',$#),('Eq 2',$#),('Eq 3',$#),('Vars','x,y,z'))),
 ('Poly roots','polyRoots(@1,@2)',(('Polynomial',$#),('Var','x'))),
 ('Domain','domain(@1,@2)',(('$d',$#),('Var','x'))),
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
 ('Factor $s','factor(@1)',(('Integer',$#),)),
 ('isPrime','isPrime(@1)',(('Integer',$#),)),
 ('gcd','gcd(@1,@2)',(('a',$#),('b',$#))),
 ('lcm','lcm(@1,@2)',(('a',$#),('b',$#))),
 ('mod','mod(@1,@2)',(('a',$#),('b',$#))),
 ('nCr','nCr(@1,@2)',(('n',$#),('r',$#))),
 ('nPr','nPr(@1,@2)',(('n',$#),('r',$#))),
 ('Factorial','(@1)!',(('n',$#),)),
 ('Real part','$R(@1)',(('Complex z',$#),)),
 ('Imag part','imag(@1)',(('Complex z',$#),)),
 ('Conjugate','conj(@1)',(('Complex z',$#),)),
 ('|z|','$J(@1)',(('Complex z',$#),)),
 ('Angle','$r(@1)',(('Complex z',$#),)),
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
 ('>Decimal','(@1)>>Decimal',(('$d',$#),)),
 ('>Fraction','(@1)>>approxFraction()',(('Decimal',$#),)),
 ('>DMS','(@1)>>DMS',(('Angle',$#),)),
 ('>Polar','(@1)>>Polar',(('Complex/vector',$#),)),
 ('>Rect','(@1)>>Rect',(('Complex',$#),)),
 ('>exp form','(@1)>>exp',(('$d',$#),)),
 ('>ln form','(@1)>>ln',(('$d',$#),)),
 ('>sin form','(@1)>>sin',(('$d',$#),)),
 ('>cos form','(@1)>>cos',(('$d',$#),)),
 ('>Binary','(@1)>>Base2',(('Integer',$#),)),
 ('>Hex','(@1)>>Base16',(('Integer',$#),)),
 )
SETS=(
 ('Degree',':deg',()),
 ('Radian',':rad',()),
 ('Auto mode',':auto',()),
 ('Exact mode',':exact',()),
 ('Approx mode',':approx',()),
 ('Real res',':$R',()),
 ('Complex res',':$3',()),
 ('Digits',':digits @1',(('Digits 1-15','10'),)),
 ('Show vars',':vars',()),
 ('Clear vars',':clear',()),
 ('Define f(x)','@1(@2):=@3',(('Name','f'),('Params','x'),('Body',$#))),
 ('Store var','@1:=@2',(('Name',$#),('Value',$#))),
 ('Self-test',':test',()),
 ('Memory',':mem',()),
 ('Key test',':keys',()),
 )
MAIN=(
 ('Algebra',ALG),('Calculus',CALC),('Solve',SOLV),('Matrix',MATX),
 ('Number/$C',NUMB),('Lists/stats',LIST),('Convert',CONV),
 ('Settings',SETS),
 )
KEYS='123456789abcdefghijklmnop'
class Quit($7):
 pass
$, ask(q):
 ${:
  s=input(q)
 $5 EOFError:
  $k Quit()
 s=s.strip()
 if s.lower()in('q','quit'):
  $k Quit()
 $! s
$, show(title,labels):
 print('-- '+title+' --')
 line=''
 $) i in $+($1(labels)):
  cell=KEYS[i]+' '+labels[i]
  if line:
   print(line+' '*max(1,16-$1(line))+cell)
   line=''
  $&:
   line=cell
 if line:
  print(line)
 print('0 back  q quit')
$, pick(title,labels):
 show(title,labels)
 $G $A:
  s=ask('#: ').lower()
  if s in('','0'):
   $! $#
  i=KEYS.find(s)
  if $1(s)==1 $* 0<=i<$1(labels):
   $! i
  print('Choose '+KEYS[0]+'-'+KEYS[$1(labels)-1]+', 0 or q')
$, matrix_text(s):
 s=s.strip()
 if s $* s[0]$- in '[(' $*(';' in s or ',' in s):
  $! '['+s+']'
 $! s
$, build(item):
 label,tpl,prompts=item
 $c=[]
 $) p in prompts:
  q=p[0]
  d=p[1]
  hint='' if $- d $& ' ['+d+']'
  s=ask(q+hint+': ')
  if $- s:
   if d is $#:
    print('(cancelled)')
    $! $#
   s=d
  if $1(p)>2 $* p[2]=='m' $* s:
   s=matrix_text(s)
  $c.$%(s)
 $! fill(tpl,$c)
$, fill(tpl,$c):
 $9=''
 $~=tpl.split('`')
 $) k in $+($1($~)):
  seg=$~[k]
  if k%2==1:
   blank=$2
   $) i in $+($1($c)):
    if('@'+$p(i+1))in seg $* $- $c[i]:
     blank=$A
   if blank:
    $6
  $9+=seg
 res=''
 i=0
 $G i<$1($9):
  c=$9[i]
  if c=='@' $* i+1<$1($9)$* '1'<=$9[i+1]<='9':
   res+=$c[$s($9[i+1])-1]
   i+=2
  $&:
   res+=c
   i+=1
 $! res
$, runmenu(run):
 print('Menus: pick a number or letter.')
 print("Type ans $) the last result.")
 ${:
  $G $A:
   k=pick('nCAS menu',[m[0]$) m in MAIN])
   if k is $#:
    $!
   title,items=MAIN[k]
   $G $A:
    j=pick(title,[it[0]$) it in items])
    if j is $#:
     $O
    cmd=build(items[j])
    if cmd is $#:
     $6
    print('> '+cmd)
    ${:
     $9=run(cmd)
    $5 $S as ex:
     $9='Error: '+$p(ex)
    $5 $E:
     $9='Error: Division by zero'
    $5 MemoryError:
     $9='Error: Out of memory'
    $5 RuntimeError as ex:
     $9='Error: Too $3'
    $5 Quit:
     $k
    $5 $7 as ex:
     $9='Error: '+$p(ex)
    if $9:
     print($9)
    ask('(enter) ')
 $5 Quit:
  $!
 $5 $t:
  $!
''',)
_L['casgui']=(r'''LH=18
CW=9
AW=7
BASE=14
MAXH=30
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
TEXT={'space':' ','$N':'$N(','\u221a':'$N(','pi':'\u03c0',
 'exp':'e^','ln':'ln(','log':'log10(','square':'^2','\u00b2':'^2',
 'ee':'E','EE':'E','\u1d07':'E','$l':'-','(-)':'-','\u2212':'-',
 '\u00d7':'*','\u00f7':'/','\u2264':'<=','\u2265':'>=','\u2260':'/=',
 '\u2192':'->','ans':'ans','theta':'\u03b8','$J':'$J(',
 'sin':'sin(','cos':'cos(','tan':'tan(','sin\u207b\u00b9':'$|(',
 'cos\u207b\u00b9':'arccos(','tan\u207b\u00b9':'$w(','$P':'$P',
 'i':'i','e':'e'}
gu_TRIG=('sin(','cos(','tan(','$|(','arccos(','$w(',
 'sinh(','cosh(','tanh(','sec(','csc(','cot(')
NEEDANS='+*/^'
G={}
$, rungui(run):
 G.setdefault('hist',[])
 key=findkey()
 ${:
  import ti_draw
 $5 ImportError:
  ti_draw=$#
 if key is $# or ti_draw is $#:
  $! screen(run,key is $#)
 G['d']=ti_draw
 G['key']=key
 G['cmode']=0
 G['gui']=$A
 ${:
  w,h=ti_draw.get_screen_dim()
  w=$s(w)
  h=$s(h)
 $5 $7:
  w,h=318,212
 G['w']=w
 G['h']=h
 G['$[']=(h-2*LH-5)//LH
 G['ncell']=(w-16)//CW
 G['wrap']=(w-12)//AW
 ed_reset()
 G['sel']=$#
 G['top']=$#
 G['msg']=''
 ${:
  ti_draw.use_buffer()
  G['buffer']=$A
 $5 $7:
  G['buffer']=$2
 ${:
  loop(run)
 $5 $t:
  pass
 $! ''
KEYFN=('get_key','getkey','getKey','wait_key','waitkey')
$, findkey():
 $) mn in('ti_system','ti_draw','ti_plotlib'):
  ${:
   m=__import__(mn)
  $5 ImportError:
   $6
  $) fn in KEYFN:
   f=getattr(m,fn,$#)
   if f is $- $#:
    $! keyfun(f)
 $! tibasic()
TINAMES={'ent':'enter','dow':'down','lef':'left','rig':'right',
 'cle':'clear','men':'menu','tri':'trig','hom':'home',
 'ctr':'ctrl','shi':'shift','cen':'center','ret':'$!',
 'squ':'square','spa':'space','sqr':'$N','bac':'backspace'}
$, tibasic():
 ${:
  import ti_system
  ev=ti_system.eval_function
 $5(ImportError,AttributeError):
  $! $#
 ${:
  if ev('ncaskey',0)!=0:
   $! $#
 $5 $7:
  $! $#
 $, wait(x=1):
  c=$s(ev('ncaskey',1))
  s=''
  $) v in(c>>32,(c>>16)&65535,c&65535):
   s+=chr(v)
  s=s.rstrip(' ')or ' '
  $! TINAMES.get(s,s)
 $! wait
$, keyfun(f):
 ${:
  from time import sleep
 $5 ImportError:
  sleep=$#
 mode=[1]
 $, wait(x=1):
  if mode[0]:
   ${:
    $! $p(f(1))
   $5 TypeError:
    mode[0]=0
  $G $A:
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
  $5 TypeError:
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
 $G $1(s)>n:
  $9.$%(s[:n])
  s=s[n:]
 $9.$%(s)
 $! $9
$, selected():
 s=G['sel']
 if s is $#:
  $! $#
 k=$1(G['hist'])-1-s//2
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
 a=SET['$r'].upper()
 m=SET['mode'].upper()
 c='REAL' if SET['$C']=='$R' $& 'CPLX'
 $! 'nCAS  '+a+' '+m+' '+c+('   menu: commands' if G.get('gui')$& '')
$, callname():
 chain=[]
 r=G['row']
 $) i,sl in G['path']:
  chain.$%((r,i))
  r=r[i][sl]
 chain.$%((r,G['pos']))
 $) r,p in reversed(chain):
  $;=0
  j=min(p,$1(r))-1
  $G j>=0:
   c=r[j]
   if c==')':
    $;+=1
   $@ c=='(':
    if $;:
     $;-=1
    $&:
     k=j
     $G k>0 $* $/(r[k-1])is $p $*(r[k-1].isalpha()or r[k-1].isdigit()):
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
 bl=blocks()
 sel=selected()
 if bl:
  if sel is $#:
   end=$1(bl)-1
   start=startfor(bl,end,avail)
  $&:
   idx=[i $) i in $+($1(bl))if(bl[i][3],bl[i][4])==sel]
   a=idx[0]
   b=idx[-1]
   G['tall']=$#
   if sum([bl[i][2]$) i in idx])>avail:
    n=fitfrom(bl,a,avail)-a+1
    st=G.get('stop',0)
    if st=='end' or st>$1(idx)-n:
     st=$1(idx)-n
    G['stop']=max(0,st)
    start=a+G['stop']
    end=fitfrom(bl,start,avail)
    G['tall']=(G['stop'],$1(idx)-n)
   $&:
    end=min(G.get('hend',$1(bl)-1),$1(bl)-1)
    start=startfor(bl,end,avail)
    if b>end:
     end=b
     start=startfor(bl,end,avail)
    if a<start:
     start=a
     end=fitfrom(bl,start,avail)
  G['hend']=end
  y=LH+2
  last=$#
  $) i in $+(start,end+1):
   kind,data,bh,k,part=bl[i]
   if last is $- $# $* k!=last:
    box(2,y-1,w-4,1,C_RULE)
   if sel is $- $# $*(k,part)==sel:
    box(0,y,w,bh,C_SEL)
   if kind=='2d':
    r,rw,ra,rd,col=data
    G['ink']=col
    rowdraw(r,4 if part=='in' $& w-6-rw,y+2+ra,$A)
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
 rowdraw(G['row'],6-hoff,base,$A)
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
 G['msg']='Working...'
 if G.get('gui'):
  draw()
 bad=$2
 ${:
  $9=run(s)
 $5 $S as ex:
  $9='Error: '+$p(ex)
  bad=$A
 $5 $E:
  $9='Error: Division by zero'
  bad=$A
 $5 MemoryError:
  $9='Error: Out of memory'
  bad=$A
 $5 RuntimeError:
  $9='Error: Too $3'
  bad=$A
 $5 $t:
  $9='Interrupted'
  bad=$A
 $5 $7 as ex:
  $9='Error: '+$p(ex)
  bad=$A
 G['msg']=''
 if $9 is $#:
  $9=''
 G['hist'].$%((s,$9,bad))
 if $1(G['hist'])>MAXH:
  G['hist'].pop(0)
$, loop(run):
 $G $A:
  draw()
  k=G['key'](1)
  G['msg']=''
  if $- k:
   $6
  before=ed_snap()
  a=ctrlaction(k)
  if a=='wait':
   G['msg']='ctrl  (next key: blue label)'
   $6
  if a is $- $#:
   doaction(run,a,k)
  $&:
   key(run,k)
  if ed_text()!=before[3]$* a!=('undo',):
   G.setdefault('undo',[]).$%(before)
   del G['undo'][:-30]
$, key(run,k):
 if k=='esc':
  if G['sel']is $- $#:
   G['sel']=$#
  $@ G['row']:
   ed_reset()
  $&:
   $k $t
 $@ k in ENTER:
  if G['sel']is $- $#:
   k2,part=selected()
   inp,res,bad=G['hist'][k2]
   G['sel']=$#
   insert(inp if part=='in' $& res.replace('\n ','').replace('\n',''))
  $@ ed_text().strip():
   s=ed_text()
   ed_reset()
   special(run,s)
 $@ k in('up','down')$* G['sel']is $# $* ed_vert(1 if k=='down' $&-1):
  pass
 $@ k=='up' $* G['sel']is $- $# $* G.get('tall')$* G['tall'][0]>0:
  G['stop']=G['tall'][0]-1
 $@ k=='down' $* G['sel']is $- $# $* G.get('tall')$* G['tall'][0]<G['tall'][1]:
  G['stop']=G['tall'][0]+1
 $@ k=='up':
  n=2*$1(G['hist'])
  if n:
   G['sel']=0 if G['sel']is $# $& min(G['sel']+1,n-1)
   G['stop']='end'
   G['tall']=$#
 $@ k=='down':
  if G['sel']is $- $#:
   G['sel']=$# if G['sel']==0 $& G['sel']-1
   G['stop']=0
   G['tall']=$#
 $@ k=='left':
  G['sel']=$#
  ed_left()
 $@ k=='right':
  G['sel']=$#
  ed_right()
 $@ k in('del','backspace'):
  G['sel']=$#
  ed_del()
 $@ k=='clear':
  G['sel']=$#
  ed_reset()
 $@ k in MENU:
  G['sel']=$#
  r=menus()
  if r is $- $#:
   act(run,r)
 $@ k in TABKEYS or k in BACKTAB:
  G['sel']=$#
  ed_tab(-1 if k in BACKTAB $& 1)
 $@ k in CATKEYS:
  G['sel']=$#
  catalog()
 $@ k in TEMPLKEYS:
  G['sel']=$#
  templates()
 $@ k in SYMKEYS:
  G['sel']=$#
  gu_symbols()
 $@ k=='trig':
  G['sel']=$#
  j=choose('Trig',gu_TRIG)
  if j is $- $#:
   insert(gu_TRIG[j]+')',1)
 $@ k in TEXT:
  G['sel']=$#
  t=TEXT[k]
  if t.endswith('('):
   insert(t+')',1)
  $&:
   insert(t)
 $@ $1(k)==1:
  G['sel']=$#
  ed_autoexit(k)
  insert(k)
 $&:
  G['msg']='key '+repr(k)+' $- used'
CTRLKEYS=('ctrl','doc')
CTRL={'(':('ins','[]',1),')':('ins','{}',1),'^':('ins','root(,)',2),
 '^2':('ins','$N()',1),'e^':('ins','ln()',1),'10^':('ins','log10()',1),
 '=':('rel',),'trig':('help',),'del':('clear',),'clear':('clear',),
 '-':('ins','ans',0),'*':('ins','""',1),'/':('ins','()/()',4),
 'enter':('approx',),'var':('ins','->',0),'esc':('undo',),
 'cat':('$g',),'catalog':('$g',),'book':('$g',),
 'template':('ins',':=',0),'templates':('ins',':=',0),'templ':('ins',':=',0),
 'tmpl':('ins',':=',0),'tab':('menu',),'menu':('$g',)}
DIRECT={'[]':('ins','[]',1),'{}':('ins','{}',1),'""':('ins','""',1),
 '()':('ins','()',1),'\u2248':('approx',),'approx':('approx',),
 'undo':('undo',),'sto':('ins','->',0),'sto\u2192':('ins','->',0),
 'store':('ins','->',0),'\u2254':('ins',':=',0),':=':('ins',':=',0),
 'nroot':('ins','root(,)',2),'root':('ins','root(,)',2),'help':('help',),
 '10^x':('ins','10^',0),'pow10':('ins','10^',0),'10^':('ins','10^',0)}
''',
r'''RELS=(('=','='),('\u2260  $- equal','/='),('<','<'),('>','>'),
 ('\u2264','<='),('\u2265','>='),('|  with','|'),('>>  convert','>>'))
CTRLHELP=('ctrl ( = [ ]      ctrl ) = { }','ctrl ^ = root      ctrl x\u00b2 = \u221a',
 'ctrl e^x = ln      ctrl 10^x = log10','ctrl = = \u2260 \u2264 \u2265 | >>',
 'ctrl (-) = ans     ctrl \u00d7 = " "','ctrl \u00f7 = fraction  ctrl var = \u2192',
 'ctrl enter = \u2248 decimal','ctrl del = clear   ctrl esc = undo',
 'ctrl catalog = Symbols','doc works as ctrl too')
$, ctrlbase(k):
 t=TEXT.get(k,k)
 $! '10^' if k in('10^x','pow10','10^')$& t
$, ctrlaction(k):
 if G.get('ctrl'):
  G['ctrl']=$2
  $! CTRL.get(ctrlbase(k))or CTRL.get(k)or('none',k)
 if k in CTRLKEYS:
  G['ctrl']=$A
  $! 'wait'
 if $1(k)>4 $* k[:4].lower()=='ctrl':
  r=k[4:].lstrip('+-_ ')
  $! CTRL.get(ctrlbase(r))or CTRL.get(r)or('none',k)
 $! DIRECT.get(k)
$, doaction(run,a,k):
 G['sel']=$#
 kind=a[0]
 if kind=='ins':
  insert(a[1],a[2])
 $@ kind=='clear':
  ed_reset()
 $@ kind=='undo':
  u=G.get('undo')
  if u:
   ed_restore(u.pop())
 $@ kind=='approx':
  s=ed_text().strip()
  if $- s $* G['hist']:
   s='ans'
  if s:
   ed_reset()
   evaluate(run,'approx('+s+')')
 $@ kind=='rel':
  j=choose('Relations',[r[0]$) r in RELS])
  if j is $- $#:
   insert(RELS[j][1])
 $@ kind=='$g':
  gu_symbols()
 $@ kind=='menu':
  r=menus()
  if r is $- $#:
   act(run,r)
 $@ kind=='help':
  panel('ctrl keys','any key to close')
  $) i in $+($1(CTRLHELP)):
   text(10,LH+4+i*LH,CTRLHELP[i],C_TXT)
  gu_show()
  G['key'](1)
 $&:
  G['msg']='ctrl+'+$p(a[1])+' $- used'
$, special(run,s):
 low=s.strip().lower()
 if low in(':keys','keys'):
  keytest()
 $@ low in('q','quit',':q'):
  $k $t
 $&:
  evaluate(run,s)
$, keytest():
 last=''
 $G $A:
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
$, choose(title,labels,jump=$2,hint=$#):
 n=$1(labels)
 i=0
 $[=G['$[']-1-(1 if hint $& 0)
 top=0
 w=G['w']
 $G $A:
  if i<top:
   top=i
  if i>=top+$[:
   top=i-$[+1
  box(10,LH+4,w-20,($[+1)*LH+6,C_DIM)
  box(11,LH+5,w-22,($[+1)*LH+4,(255,255,255))
  box(11,LH+5,w-22,LH,C_BAR)
  text(16,LH+5,title,C_BART)
  y=2*LH+7
  $) j in $+(top,min(n,top+$[)):
   if j==i:
    box(12,y,w-24,LH,C_SEL)
   key=KEYS[j]if j<$1(KEYS)$* $- jump $& ' '
   text(16,y,key,C_DIM)
   text(34,y,labels[j],C_TXT)
   y+=LH
  if top+$[<n:
   text(w-30,y-LH,'v',C_DIM)
  if hint:
   box(12,y,w-24,LH,C_BAR)
   text(16,y,(hint(i)or '')[:(w-32)//CW],C_BART)
  gu_show()
  k=G['key'](1)
  if k=='up':
   i=(i-1)%n
  $@ k=='down':
   i=(i+1)%n
  $@ k in ENTER or k=='right':
   $! i
  $@ k in('esc','left')or k in MENU:
   $! $#
  $@ jump $* $1(k)==1 $* k.isalpha():
   c=k.lower()
   $) d in $+(1,n+1):
    if labels[(i+d)%n][:1].lower()==c:
     i=(i+d)%n
     $O
  $@ $- jump $* $1(k)==1 $* k in KEYS[:n]:
   $! KEYS.index(k)
$, menus():
 _load('casmenu')
 main=MAIN
 $G $A:
  a=choose('Menu',[m[0]$) m in main]+['Templates','Symbols'])
  if a is $#:
   $! $#
  if a==$1(main):
   templates()
   $! $#
  if a==$1(main)+1:
   gu_symbols()
   $! $#
  title,items=main[a]
  b=choose(title,[it[0]$) it in items])
  if b is $- $#:
   $! items[b]
$, act(run,item):
 _load('casmenu')
 label,tpl,prompts=item
 if $- prompts:
  special(run,tpl)
  $!
 $c=[]
 mark='\u0001'
 first=$A
 $) p in prompts:
  d=p[1]
  if d is $#:
   v='[]' if $1(p)>2 $* p[2]=='m' $& ''
   if first:
    v='['+mark+']' if v $& mark
    first=$2
  $&:
   v=d
  $c.$%(v)
 s=fill(tpl,$c)
 i=s.find(mark)
 if i<0:
  i=$1(s)
 $&:
  s=s[:i]+s[i+1:]
 ed_chars(s)
 G['pos']-=$1(s)-i
$, screen(run,nokeys=$A):
 G['gui']=$2
 G['msg']=''
 ${:
  import ti_system
  have=[n $) n in dir(ti_system)if n[0]!='_']
 $5 ImportError:
  have=$#
 print('nCAS screen mode: this OS gives programs no single-key input.')
 if have is $#:
  print('(no ti_system module)')
 $&:
  print('ti_system: '+' '.join(have))
 $[=4
 $G $A:
  hist=G['hist']
  print('-'*30)
  first=max(0,$1(hist)-$[)
  $) k in $+(first,$1(hist)):
   inp,res,bad=hist[k]
   print('#'+$p(k+1)+' '+inp)
   $) r in res.split('\n'):
    print('   '+r)
  print(status()+'  m menu  q quit')
  ${:
   s=input('> ').strip()
  $5(EOFError,$t):
   $! ''
  if s in('q','quit',':q'):
   $! ''
  if s in('m','menu'):
   cmd=pickmenu()
   if $- cmd:
    $6
   print('> '+cmd)
   s=cmd
  if $- s:
   $6
  s=refs(s,hist)
  if s.strip().lower()in(':keys','keys'):
   print('No key reading on this OS.')
   $6
  evaluate(run,s)
$, pickmenu():
 _load('casmenu')
 ${:
  $G $A:
   k=pick('nCAS menu',[m[0]$) m in MAIN])
   if k is $#:
    $! $#
   title,items=MAIN[k]
   j=pick(title,[it[0]$) it in items])
   if j is $#:
    $6
   cmd=build(items[j])
   if cmd:
    $! cmd
 $5 Quit:
  $! $#
$, refs(s,hist):
 $9=''
 i=0
 $G i<$1(s):
  if s[i]=='#' $* i+1<$1(s)$* s[i+1].isdigit():
   j=i+1
   $G j<$1(s)$* s[j].isdigit():
    j+=1
   n=$s(s[i+1:j])
   if 1<=n<=$1(hist)$* $- hist[n-1][2]:
    $9+='('+hist[n-1][1].split('\n')[0]+')'
   $&:
    $9+=s[i:j]
   i=j
  $&:
   $9+=s[i]
   i+=1
 $! $9
TEMPLKEYS=('template','templates','templ','tmpl')
SYMKEYS=('$g','symbol','punc','?!','?!>','palette')
TPLS=('Matrix m\u00d7n','Column vector','Row vector')
''',
r'''SYMS=(
 (';',';',0,'next row in a matrix [1,2;3,4]'),(',',',',0,'separates arguments'),
 ('[ ]','[]',1,'matrix or vector'),('{ }','{}',1,'$K {1,2,3}'),
 ('( )','()',1,'parentheses'),('|','|',0,'with: x^2|x=3'),
 ("'","'",0,"derivative in deSolve: y'"),('" "','""',1,'text'),
 ('=','=',0,'equation'),('\u2260','/=',0,'$- equal'),
 ('<','<',0,'less than'),('>','>',0,'greater than'),
 ('\u2264','<=',0,'less or equal'),('\u2265','>=',0,'greater or equal'),
 (':=',':=',0,'define: f(x):=x^2'),('\u2192','->',0,'store: 5->a'),
 ('^','^',0,'power'),('^2','^2',0,'square'),
 ('^-1','^-1',0,'inverse: [1,2;3,4]^-1'),('\u221a','$N()',1,'square root'),
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
 j=choose('Templates',$K(TPLS)+[t[0]$) t in MATHTPL])
 if j is $#:
  $!
 if j>=$1(TPLS):
  insert(MATHTPL[j-$1(TPLS)][1])
  $!
 fix=('','c','r')[j]
 size=gridsize(3 if fix=='c' $& 2,1 if fix=='c' $&(3 if fix=='r' $& 2),fix)
 if size is $#:
  $!
 s=grid(size[0],size[1])
 if s is $#:
  $!
 fillpair(s)
$, fillpair(s):
 r=ed_row()
 p=G['pos']
 $) a in(p-1,p,p-2):
  if 0<=a $* a+1<$1(r)$* r[a]=='[' $* r[a+1]==']':
   G['pos']=a+1
   s=s[1:-1]
   $O
 ed_chars(s)
$, gu_symbols():
 n=$1(SYMS)
 $[=(n+SCOLS-1)//SCOLS
 k0=G.get('symk',0)
 w=G['w']
 cw=(w-8)//SCOLS
 ch=LH+6
 $G $A:
  panel('Symbols',SYMS[k0][3])
  y0=LH+4
  $) r in $+($[):
   $) c in $+(SCOLS):
    k=r*SCOLS+c
    if k>=n:
     $O
    x=4+c*cw
    y=y0+r*ch
    box(x+1,y+1,cw-2,ch-2,C_SEL if k==k0 $& C_BOX)
    lab=SYMS[k][0]
    text(x+max(2,(cw-$1(lab)*AW)//2),y+2,lab,C_TXT)
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
  $@ key=='left':
   k0=(k0-1)%n
  $@ key=='down':
   k0=k0+SCOLS if k0+SCOLS<n $& k0%SCOLS
  $@ key=='up':
   if k0-SCOLS>=0:
    k0-=SCOLS
   $&:
    last=($[-1)*SCOLS+k0%SCOLS
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
 $G $A:
  panel('Matrix size','arrows or digits, enter OK, esc cancel')
  text(20,2*LH,'Rows: '+$p(r)+'    Columns: '+$p(c),C_TXT)
  cw=min(24,(G['w']-40)//max(c,1))
  ch=min(16,(G['h']-6*LH)//max(r,1))
  $) i in $+(r):
   $) j in $+(c):
    box(20+j*cw,4*LH+i*ch,cw-3,ch-3,C_SEL)
  gu_show()
  k=G['key'](1)
  if k=='esc':
   $! $#
  if k in ENTER:
   $!(r,c)
  if k=='up' $* fix!='r':
   r=min(9,r+1)
  $@ k=='down' $* fix!='r':
   r=max(1,r-1)
  $@ k=='right' $* fix!='c':
   c=min(9,c+1)
  $@ k=='left' $* fix!='c':
   c=max(1,c-1)
  $@ $1(k)==1 $* '1'<=k<='9':
   if fix=='c':
    r=$s(k)
   $@ fix=='r':
    c=$s(k)
   $&:
    typed.$%($s(k))
    if $1(typed)==1:
     r=typed[0]
    $&:
     c=typed[1]
     typed=[]
$, keytext(k):
 if k in TEXT:
  $! TEXT[k]
 if $1(k)==1:
  $! k
 $! $#
$, grid(r,c):
 cells=[['']*c $) i in $+(r)]
 i=0
 j=0
 w=G['w']
 cw=max(30,min(80,(w-24)//c))
 ncw=max(1,(cw-6)//AW)
 $[=G['$[']
 $G $A:
  panel('Matrix '+$p(r)+'\u00d7'+$p(c),
 'tab/arrows move, enter done, esc cancel')
  top=max(0,i-$[+2)
  y0=LH+6
  nshow=min(r-top,$[-1)
  box(8,y0,2,nshow*(LH+4),C_TXT)
  box(8,y0,5,2,C_TXT)
  box(8,y0+nshow*(LH+4)-2,5,2,C_TXT)
  x1=14+c*cw
  box(x1,y0,2,nshow*(LH+4),C_TXT)
  box(x1-3,y0,5,2,C_TXT)
  box(x1-3,y0+nshow*(LH+4)-2,5,2,C_TXT)
  $) a in $+(top,top+nshow):
   y=y0+(a-top)*(LH+4)
   $) b in $+(c):
    x=14+b*cw
    cur=(a==i $* b==j)
    box(x+1,y+1,cw-4,LH+2,C_SEL if cur $& C_BOX)
    t=cells[a][b]
    if $1(t)>ncw:
     t=t[-ncw:]
    text(x+3,y+2,t,C_TXT)
    if cur:
     box(x+3+$1(t)*AW,y+3,2,LH-2,C_CUR)
  gu_show()
  k=G['key'](1)
  if k=='esc':
   $! $#
  if k in ENTER:
   $! '['+';'.join([','.join([v or '0' $) v in row])$) row in cells])+']'
  if k=='tab' or k=='right':
   j+=1
   if j==c:
    j=0
    i=(i+1)%r
  $@ k=='left':
   j-=1
   if j<0:
    j=c-1
    i=(i-1)%r
  $@ k=='down':
   i=(i+1)%r
  $@ k=='up':
   i=(i-1)%r
  $@ k in('del','backspace'):
   cells[i][j]=cells[i][j][:-1]
  $@ k=='clear':
   cells[i][j]=''
  $&:
   a=ctrlaction(k)
   if a is $- $# $* a!='wait' $* a[0]=='ins':
    t=a[1][:$1(a[1])-a[2]]
   $@ a is $- $#:
    t=$#
   $&:
    t=keytext(k)
   if t is $- $#:
    cells[i][j]+=t
A_=13
D_=4
AX=5
RAISE=8
NODETEXT={'^':('','pow',''),'^2':('','pow','2'),'^-1':('','pow','-1'),
 '$N()':('','$N',''),'root(,)':('','root',''),
 '()/()':('','frac',''),'$J()':('','$J',''),
 'e^':('e','pow',''),'10^':('10','pow',''),
 '$L()':('','$s',''),'$L(,,,)':('','dint',''),
 'd()':('','der','')}
MATHTPL=(('Fraction','()/()'),('Power  x^n','^'),('Square root','$N()'),
 ('n-th root','root(,)'),('Absolute value','$J()'),('e^x','e^'),
 ('Integral  \u222b f dx','$L()'),('Definite $L  \u222b[a,b]','$L(,,,)'),
 ('Derivative  d/dx','d()'))
gu_CALC={'$s':(2,2,1),'dint':(4,4,1),'der':(2,1,2)}
EXITCHARS='+-*/=<>,)'
$, ed_reset():
 G['row']=[]
 G['path']=[]
 G['pos']=0
 G['hoff']=0
$, ed_row():
 r=G['row']
 $) i,sl in G['path']:
  r=r[i][sl]
 $! r
''',
r'''$, ed_parent():
 r=G['row']
 $) i,sl in G['path'][:-1]:
  r=r[i][sl]
 $! r,r[G['path'][-1][0]]
$, ed_chars(s):
 r=ed_row()
 p=G['pos']
 $) c in s:
  r.insert(p,c)
  p+=1
 G['pos']=p
$, ed_node(kind,pre=''):
 r=ed_row()
 p=G['pos']
 if kind in gu_CALC:
  n,var,first=gu_CALC[kind]
  node=[kind]+[[]$) i in $+(n)]
  node[var].$%('x')
  r.insert(p,node)
  G['path'].$%((p,first))
  G['pos']=0
  $!
 n=3 if kind in('frac','root')$& 2
 node=[kind]+[[]$) i in $+(n-1)]
 $) c in pre:
  node[1].$%(c)
 r.insert(p,node)
 if pre:
  G['pos']=p+1
 $&:
  G['path'].$%((p,1))
  G['pos']=0
$, ed_empty(node):
 $) sl in node[1:]:
  if sl:
   $! $2
 $! $A
$, ed_right():
 r=ed_row()
 p=G['pos']
 if p<$1(r):
  if $/(r[p])is $p:
   G['pos']=p+1
  $&:
   G['path'].$%((p,1))
   G['pos']=0
 $@ G['path']:
  i,sl=G['path'][-1]
  par,node=ed_parent()
  if sl+1<$1(node):
   G['path'][-1]=(i,sl+1)
   G['pos']=0
  $&:
   G['path'].pop()
   G['pos']=i+1
$, ed_left():
 r=ed_row()
 p=G['pos']
 if p>0:
  if $/(r[p-1])is $p:
   G['pos']=p-1
  $&:
   node=r[p-1]
   G['path'].$%((p-1,$1(node)-1))
   G['pos']=$1(node[-1])
 $@ G['path']:
  i,sl=G['path'][-1]
  par,node=ed_parent()
  if sl>1:
   G['path'][-1]=(i,sl-1)
   G['pos']=$1(node[sl-1])
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
   G['pos']=min(G['pos'],$1(node[t]))
 $@ k=='pow' $* d>0:
  G['path'].pop()
  G['pos']=i+1
 $@ k=='dint':
  t=2 if d<0 $& 1
  if t!=sl:
   G['path'][-1]=(i,t)
   G['pos']=$1(node[t])
 $! $A
$, ed_del():
 r=ed_row()
 p=G['pos']
 if p>0:
  it=r[p-1]
  if $/(it)is $p or ed_empty(it):
   del r[p-1]
   G['pos']=p-1
  $&:
   G['path'].$%((p-1,$1(it)-1))
   G['pos']=$1(it[-1])
 $@ G['path']:
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
 if node[0]!='pow' or G['pos']!=$1(r)or $- r:
  $!
 $;=0
 $) it in r:
  if it=='(':
   $;+=1
  $@ it==')':
   $;-=1
 if $;<=0:
  G['pos']=G['path'].pop()[0]+1
$, ed_text(row=$#):
 if row is $#:
  row=G['row']
 $9=''
 $) it in row:
  if $/(it)is $p:
   $9+=it
   $6
  k=it[0]
  if k=='frac':
   f=grp(ed_text(it[1]),$A)+'/'+grp(ed_text(it[2]),$2)
   $9+=f if $1(row)==1 $& '('+f+')'
  $@ k=='pow':
   e=ed_text(it[1])
   $9+='^'+(e if e.isdigit()or($1(e)==1 $* e.isalpha())or enclosed(e)
 $& '('+e+')')
  $@ k=='$N':
   $9+='$N('+ed_text(it[1])+')'
  $@ k=='root':
   $9+='root('+ed_text(it[2])+','+ed_text(it[1])+')'
  $@ k=='$J':
   $9+='$J('+ed_text(it[1])+')'
  $@ k=='$s':
   $9+='$L('+ed_text(it[1])+','+ed_text(it[2])+')'
  $@ k=='dint':
   lo,hi=ed_text(it[1]),ed_text(it[2])
   $9+='$L('+ed_text(it[3])+','+ed_text(it[4])
   $9+=(','+lo+','+hi+')')if lo or hi $& ')'
  $@ k=='der':
   $9+='d('+ed_text(it[2])+','+ed_text(it[1])+')'
 $! $9
$, enclosed(s):
 if $1(s)<2 or s[0]!='(' or s[-1]!=')':
  $! $2
 $;=0
 $) i in $+($1(s)):
  if s[i]=='(':
   $;+=1
  $@ s[i]==')':
   $;-=1
   if $;==0 $* i<$1(s)-1:
    $! $2
 $! $A
$, grp(s,num):
 ok=s!=''
 digits=$A
 $) c in s:
  if $-(c.isdigit()or c=='.'):
   digits=$2
  if $-(c.isdigit()or c=='.' or c.isalpha()):
   ok=$2
 if ok $* $- digits $* $- s.isalpha():
  ok=$2
 i=s.find('(')
 if i>0 $* s[:i].isalpha()$* enclosed(s[i:]):
  ok=$A
 $! s if ok or enclosed(s)$& '('+s+')'
$, ed_cp(row):
 $![it if $/(it)is $p $&[it[0]]+[ed_cp(r)$) r in it[1:]]$) it in row]
$, ed_snap():
 $!(ed_cp(G['row']),$K(G['path']),G['pos'],ed_text())
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
 $) it in row:
  iw,ia,idd=measi(it)
  w+=iw
  a=max(a,ia)
  d=max(d,idd)
 $!(w,a,d)
$, measi(it):
 if $/(it)is $p:
  $!(CW,A_,D_)
 k=it[0]
 if k=='frac':
  w1,a1,d1=meas(it[1])
  w2,a2,d2=meas(it[2])
  $!(max(w1,w2)+6,AX+2+a1+d1,max(D_,2-AX+a2+d2))
 if k=='pow':
  w,a,d=meas(it[1])
  $!(w+2,max(A_,RAISE+a),max(D_,d-RAISE))
 if k=='$J':
  w,a,d=meas(it[1])
  $!(w+7,a,d)
 if k=='mat':
  cw,ra,rd,W,H=matsize(it[1])
  asc=H//2+AX
  $!(W,asc+1,H-asc+1)
 if k=='root':
  w,a,d=meas(it[2])
  wi,ai,di=meas(it[1])
  $!(wi+w+11,max(a+3,RAISE+ai),d)
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
 f,x=(it[1],it[2])if k=='$s' $&(it[3],it[4])
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
 $5 $7:
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
 $) i in $+($1(row)):
  if cur $* i==G['pos']:
   G['cxy']=(x,y,A_,D_)
  x+=itemdraw(row[i],x,y,dr)
 if cur $* G['pos']==$1(row):
  G['cxy']=(x,y,A_,D_)
 $! x-x0
''',
r'''$, itemdraw(it,x,y,dr):
 ink=G.get('ink',C_TXT)
 if $/(it)is $p:
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
 if k=='mat':
  cw,ra,rd,W,H=matsize(it[1])
  top=y-(H//2+AX)
  if dr:
   $) bx,tx in((x+1,x+1),(x+W-2,x+W-4)):
    box(bx,top,1,H,ink)
    box(tx,top,3,1,ink)
    box(tx,top+H-1,3,1,ink)
  cy=top
  $) i in $+($1(it[1])):
   cx=x+5
   r=it[1][i]
   $) j in $+($1(r)):
    w2=meas(r[j])[0]
    rowdraw(r[j],cx+(cw[j]-w2)//2,cy+ra[i],dr)
    cx+=cw[j]+8
   cy+=ra[i]+rd[i]+7
  $! W
 if k in gu_CALC:
  $! calcdraw(it,x,y,dr,ink)
 xi=x
 if k=='root':
  xi+=rowdraw(it[1],x,y-RAISE,dr)
  rad=it[2]
 $&:
  rad=it[1]
 w,a,d=meas(rad)
 if k=='$J':
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
 $) key,title,words in CATS:
  if key in('conv','cmd'):
   $6
  $) wd in words.split():
   if wd[0].isalpha()$* wd $- in names $* okname(wd):
    names.$%(wd)
 names.sort(key=$: t:t.lower())
 $, hint(i):
  sy=SYN.get(names[i].lower())
  $! sy.split('\n')[0]if sy $& names[i]+'(...)'
 j=choose('Catalog: $/ a letter',names,$A,hint)
 if j is $- $#:
  insert(names[j]+'()',1)
$, okname(wd):
 $) c in wd:
  if $-(c.isalpha()or c.isdigit()or c=='_'):
   $! $2
 $! $A
$, ed_stops():
 $9=[]
 $, walk(row,path):
  $) i in $+($1(row)+1):
   $9.$%((path,i,(i>0 $* row[i-1]==',')or(bool(path)$* i==$1(row))))
   if i<$1(row)$* $/(row[i])is $- $p:
    $) sl in $+(1,$1(row[i])):
     walk(row[i][sl],path+[(i,sl)])
 walk(G['row'],[])
 $! $9
$, ed_tab(d):
 ps=ed_stops()
 cur=0
 $) j in $+($1(ps)):
  if ps[j][0]==G['path']$* ps[j][1]==G['pos']:
   cur=j
 t=$1(ps)-1 if d>0 $& 0
 if d>0:
  $) j in $+(cur+1,$1(ps)):
   if ps[j][2]:
    t=j
    $O
 $&:
  $) j in $+(cur-1,-1,-1):
   if ps[j][2]:
    t=j
    $O
 G['path']=$K(ps[t][0])
 G['pos']=ps[t][1]
SAFE='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_+-*/^().,;=<>{}[]! \u221a\u03c0\u221e\u2260\u2264\u2265\u03b8\u222b'
SHOW={'pi':'\u03c0','$P':'\u221e','theta':'\u03b8'}
SHOWF={'sumseq':'\u03a3','prodseq':'\u03a0','$L':'\u222b'}
REL2={'=':'=','/=':'\u2260','<':'<','>':'>','<=':'\u2264','>=':'\u2265'}
DOT='\u00b7'
$, anyfunc(n):
 $! $A
$, tolayout(s):
 c=G.setdefault('lay',{})
 if s in c:
  $! c[s]
 t=s.replace('\n ','').replace('\n','')
 ok=t!='' $* $1(t)<400
 $) ch in t:
  if ch $- in SAFE:
   ok=$2
   $O
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
  $5 $7:
   r=$#
 if $1(c)>80:
  c.clear()
 c[s]=r
 $! r
$, prec(t):
 if $/(t)is $- $0:
  $! 5
 h=t[0]
 if h in('+','-'):
  $! 1
 if h in('*','$l'):
  $! 2
 if h=='^':
  $! 4
 if h in REL2:
  $! 0
 if h in('$*','or','xor','$-'):
  $!-1
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
''',
r'''$, lay(t,$9):
 tt=$/(t)
 if tt is $s:
  $9.$}($K($p(t)))
  $!
 if tt is $D:
  $9.$}($K(fmt(t)))
  $!
 if tt is $p:
  $9.$}($K(SHOW.get(t,t)))
  $!
 h=t[0]
 if h=='+' or h=='-':
  lay(t[1],$9)
  $9.$%(h)
  layp(t[2],$9,prec(t[2])<=(1 if h=='-' $& 0)
 or($/(t[2])is $0 $* t[2][0]=='$l'))
 $@ h=='*':
  layp(t[1],$9,prec(t[1])<2)
  $9.$%(DOT)
  layp(t[2],$9,prec(t[2])<2 or($/(t[2])is $0 $* t[2][0]=='$l'))
 $@ h=='$l':
  $9.$%('-')
  layp(t[1],$9,prec(t[1])<=1)
 $@ h=='/':
  $9.$%(['frac',sublay(t[1]),sublay(t[2])])
 $@ h=='^':
  b=t[1]
  need=prec(b)<5 or($/(b)is $0 $*(b[0]=='/' or(b[0]=='call' $* b[1]in('$N','root'))))
  layp(b,$9,need)
  $9.$%(['pow',sublay(t[2])])
 $@ h=='call':
  $B=t[1]
  $M=t[2:]
  if $B=='$N' $* $1($M)==1:
   $9.$%(['$N',sublay($M[0])])
  $@ $B=='root' $* $1($M)==2:
   $9.$%(['root',sublay($M[1]),sublay($M[0])])
  $@ $B=='$J' $* $1($M)==1:
   $9.$%(['$J',sublay($M[0])])
  $@ $B=='$L' $* $1($M)==2:
   $9.$%(['$s',sublay($M[0]),sublay($M[1])])
  $@ $B=='$L' $* $1($M)==4:
   $9.$%(['dint',sublay($M[2]),sublay($M[3]),sublay($M[0]),sublay($M[1])])
  $@ $B=='d' $* $1($M)==2:
   $9.$%(['der',sublay($M[1]),sublay($M[0])])
  $&:
   nm=SHOWF.get($B)if OPT['uni']$& $#
   $9.$}($K(nm or tiname($B)))
   $9.$%('(')
   $) i in $+($1($M)):
    if i:
     $9.$%(',')
    lay($M[i],$9)
   $9.$%(')')
 $@ h=='$K':
  $9.$%('{')
  $) i in $+(1,$1(t)):
   if i>1:
    $9.$%(',')
   lay(t[i],$9)
  $9.$%('}')
 $@ h=='mat':
  $9.$%(['mat',[[sublay(c)$) c in r[1:]]$) r in t[1:]]])
 $@ h in REL2:
  lay(t[1],$9)
  $9.$}($K(REL2[h]))
  lay(t[2],$9)
 $@ h in('$*','or','xor'):
  lay(t[1],$9)
  $9.$}($K(' '+h+' '))
  lay(t[2],$9)
 $@ h=='$-':
  $9.$}($K('$- '))
  layp(t[1],$9,prec(t[1])<0)
 $@ h=='!':
  layp(t[1],$9,prec(t[1])<5 or $/(t[1])is $0 $* t[1][0]=='/')
  $9.$%('!')
 $&:
  $k $T('no 2D form')
$, tiname($B):
 c=G.get('tinames')
 if c is $#:
  _load('cashelp')
  c={}
  $) key,title,words in CATS:
   $) wd in words.split():
    c[wd.lower()]=wd
  c.update(TINAME)
  G['tinames']=c
 $! c.get($B,$B)
$, matsize($[):
 nc=max([$1(r)$) r in $[])
 cw=[0]*nc
 ra=[]
 rd=[]
 $) r in $[:
  a=A_
  d=D_
  $) j in $+($1(r)):
   w,ca,cd=meas(r[j])
   cw[j]=max(cw[j],w)
   a=max(a,ca)
   d=max(d,cd)
  ra.$%(a)
  rd.$%(d)
 W=sum(cw)+8*(nc-1)+10
 H=sum(ra)+sum(rd)+7*($1($[)-1)
 $! cw,ra,rd,W,H
$, blocks():
 $9=[]
 n=G['wrap']
 w=G['w']
 $) k in $+($1(G['hist'])):
  inp,res,bad=G['hist'][k]
  $) part,s,col in(('in',inp,C_TXT),('$9',res,C_ERR if bad $& C_RES)):
   lt=$# if bad $& tolayout(s)
   if lt is $- $#:
    r,rw,ra,rd=lt
    if rw<=w-10 $* ra+rd+4<=G['h']-3*LH-8:
     $9.$%(('2d',(r,rw,ra,rd,col),ra+rd+4,k,part))
     $6
   pre='  ' if part=='$9' $& ''
   $) line in s.split('\n'):
    $) t in wrap(line,n-$1(pre)):
     $9.$%(('txt',(pre+t,col),LH,k,part))
 $! $9
$, startfor(bl,end,avail):
 hh=0
 i=end
 $G i>=0 $* hh+bl[i][2]<=avail:
  hh+=bl[i][2]
  i-=1
 $! min(i+1,end)
$, fitfrom(bl,start,avail):
 hh=0
 i=start
 $G i<$1(bl)$* hh+bl[i][2]<=avail:
  hh+=bl[i][2]
  i+=1
 $! max(start,i-1)
''',)
del _x
startgui()
