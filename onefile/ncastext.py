# ncastext - nCAS text version for TI-Nspire CX II. Run it (ctrl+R): ? help, m menus, q quit.
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
_W={'!': 'return', '#': 'None', '%': 'append', '&': 'isnode', '(': 'else', ')': 'for', '*': 'and', '+': 'range', ',': 'def', '-': 'not', '.': 'autocancel', '/': 'type', '0': 'tuple', '1': 'complex', '2': 'isconst', '3': 'False', '4': 'freeof', '5': 'len', '6': 'Exception', '7': 'lambda', '8': 'continue', '9': 'except', ':': 'mul', ';': 'add_list', '<': 'depth', '=': 'self', '>': 'expand', '?': 'out', '@': 'cplx', 'A': 'float', 'B': 'name', 'C': 'isnum', 'D': 'ZeroDivisionError', 'E': 'True', 'F': 'undef', 'G': 'mul_list', 'H': 'abs', 'I': 'list', 'J': 'while', 'K': 'elif', 'L': 'terms', 'M': 'inf', 'N': 'real', 'O': 'div', 'P': 'p_divexact', 'Q': 'subs', 'R': 'CASError', 'S': 'nval', 'T': 'break', 'U': 'ValueError', 'V': 'sqrt', 'W': 'math', 'X': 'coeffs', 'Y': 'args', 'Z': 'integral', '[': 'sub', ']': 'add', '^': 'hasfloat', '_': 'nsign', '`': 'OverflowError', 'a': 'coef_rest', 'b': 'Expression', 'c': 'islist', 'd': 'rest', 'e': 'vals', 'f': 'sols', 'g': 'linear', 'h': 'onevar_expr', 'i': 'NoSeries', 'j': 'isint', 'k': 'neg', 'l': 'raise', 'm': 'solve_eq', 'n': 'rows', 'o': 'FSIMP', 'p': 'angle', 'q': 'symbols', 'r': 'israt', 's': 'HALF', 't': 'isrealc', 'u': 'startswith', 'v': 'limit', 'w': 'int', 'x': 'arctan', 'y': 'parts', 'z': 'best', '{': 'str', '|': 'integ', '}': 'nargs', '~': 'arcsin'}
_x(r'''import $W
class $R($6):
 pass
$, err(msg):
 $l $R(msg)
CONSTS=('pi','e','i')
SPECIAL=('pi','e','i','$M','$F','true','false')
$, igcd(a,b):
 if a<0:
  a=-a
 if b<0:
  b=-b
 $J b:
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
$s=('Q',1,2)
$, isq(x):
 $! $/(x)is $0 $* x[0]=='Q'
$, $j(x):
 $! $/(x)is $w
$, isfl(x):
 $! $/(x)is $A
$, $r(x):
 t=$/(x)
 $! t is $w or(t is $0 $* x[0]=='Q')
$, $C(x):
 t=$/(x)
 $! t is $w or t is $A or(t is $0 $* x[0]=='Q')
$, nd(x):
 if $/(x)is $w:
  $! x,1
 $! x[1],x[2]
$, tofl(x):
 t=$/(x)
 if t is $A:
  $! x
 if t is $w:
  $! $A(x)
 $! x[1]/x[2]
$, nadd(a,b):
 ta=$/(a)
 tb=$/(b)
 if ta is $w $* tb is $w:
  $! a+b
 if ta is $A or tb is $A:
  $! tofl(a)+tofl(b)
 an,ad=nd(a)
 bn,bd=nd(b)
 $! Q(an*bd+bn*ad,ad*bd)
$, nmul(a,b):
 ta=$/(a)
 tb=$/(b)
 if ta is $w $* tb is $w:
  $! a*b
 if ta is $A or tb is $A:
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
 if t is $A:
  if a==0.0:
   err("Division by zero")
  $! 1.0/a
 n,d=nd(a)
 $! Q(d,n)
$, ndiv(a,b):
 $! nmul(a,ninv(b))
$, $_(a):
 if $/(a)is $0:
  a=a[1]
 if a>0:
  $! 1
 if a<0:
  $!-1
 $! 0
$, ncmp(a,b):
 $! $_(nsub(a,b))
$, nfloor(a):
 t=$/(a)
 if t is $w:
  $! a
 if t is $A:
  if a!=a or a in($A('$M'),$A('-$M')):
   err("Domain error")
  $! $w($W.floor(a))
 $! a[1]//a[2]
$, nabs(a):
 if $_(a)<0:
  $! nneg(a)
 $! a
$, nipow(a,k):
 if k<0:
  $! nipow(ninv(a),-k)
 if $/(a)is $A:
  $! a**k
 n,d=nd(a)
 $! Q(n**k,d**k)
$, iroot(n,k):
 if n<2:
  $! n
 x=$w($W.pow(n,1.0/k))if n<10**300 $( 1<<(($5(bin(n))-2)//k+1)
 if x<1:
  x=1
 $J $E:
  y=((k-1)*x+n//(x**(k-1)))//k
  if y>=x:
   $T
  x=y
 $J x**k>n:
  x-=1
 $J(x+1)**k<=n:
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
$, $&(e,h):
 $! $/(e)is $0 $* e[0]==h
$, head(e):
 if $/(e)is $0:
  $! e[0]
 $! $#
$, okey(e):
 $! repr(e)
$, has(e,x):
 if e==x:
  $! $E
 if $/(e)is $0 $* e[0]!='Q':
  $) a in e[1:]:
   if has(a,x):
    $! $E
 $! $3
$, $4(e,x):
 $! $- has(e,x)
$, freeofall(e,xs):
 $) x in xs:
  if has(e,x):
   $! $3
 $! $E
$, $q(e,$?=$#):
 if $? is $#:
  $?=[]
 t=$/(e)
 if t is ${:
  if e $- in SPECIAL $* e $- in $?:
   $?.$%(e)
 $K t is $0 $* e[0]!='Q' $* e[0]!='${':
  $) a in e[1:]:
   $q(a,$?)
 $! $?
$, $2(e):
 t=$/(e)
 if t is ${:
  $! e in SPECIAL
 if t is $0 $* e[0]!='Q':
  if e[0]=='${':
   $! $3
  $) a in e[1:]:
   if $- $2(a):
    $! $3
 $! $E
$, $^(e):
 t=$/(e)
 if t is $A:
  $! $E
 if t is $0 $* e[0]!='Q':
  $) a in e[1:]:
   if $^(a):
    $! $E
 $! $3
$, $a(a):
 if $/(a)is $0 $* a[0]=='*' $* $C(a[1]):
  if $5(a)==3:
   $! a[1],a[2]
  $! a[1],('*',)+a[2:]
 $! 1,a
$, cmul(c,r):
 if $/(c)is $w $* c==1:
  $! r
 if $/(r)is $0 $* r[0]=='*':
  if $C(r[1]):
   c=nmul(c,r[1])
   if $/(c)is $w $* c==1:
    $!('*',)+r[2:]if $5(r)>3 $( r[2]
   $!('*',c)+r[2:]
  $!('*',c)+r[1:]
 $!('*',c,r)
$, $](*$Y):
 $! $;($Y)
$, $;($Y):
 num=0
 $L={}
 order=[]
 st=$I($Y)
 infs=0
 $J st:
  a=st.pop()
  t=$/(a)
  if t is $w or t is $A:
   num=nadd(num,a)
   $8
  if t is $0:
   h=a[0]
   if h=='Q':
    num=nadd(num,a)
    $8
   if h=='+':
    st.extend(a[1:])
    $8
   if h=='*' $* $C(a[1]):
    c=a[1]
    r=a[2]if $5(a)==3 $(('*',)+a[2:]
   $(:
    c=1
    r=a
  $(:
   if a=='$F':
    $! '$F'
   c=1
   r=a
  if r=='$M':
   s=$_(c)
   if s==0:
    $8
   if infs $* infs!=s:
    $! '$F'
   infs=s
   $8
  if r in $L:
   $L[r]=nadd($L[r],c)
  $(:
   $L[r]=c
   order.$%(r)
 if infs:
  $! '$M' if infs>0 $(('*',-1,'$M')
 $?=[]
 $) r in order:
  c=$L[r]
  if c==0:
   $8
  $?.$%(cmul(c,r))
 if num!=0 or $- $?:
  if $? $* num==0:
   pass
  $(:
   $?.$%(num)
 if $5($?)==1:
  $! $?[0]
 $?.sort(key=okey)
 $!('+',)+$0($?)
$, isrrad(e):
 $! $/(e)is $0 $* e[0]=='^' $* $/(e[1])is $w $* isq(e[2])
$, $:(*$Y):
 $! $G($Y)
''')
_x(r'''$, $G($Y):
 coef=1
 bases={}
 order=[]
 st=$I($Y)
 $J st:
  a=st.pop()
  t=$/(a)
  if t is $w or t is $A:
   coef=nmul(coef,a)
   $8
  if t is $0:
   h=a[0]
   if h=='Q':
    coef=nmul(coef,a)
    $8
   if h=='*':
    st.extend(a[1:])
    $8
   if h=='^':
    b=a[1]
    x=a[2]
   $(:
    b=a
    x=1
  $(:
   if a=='$F':
    $! '$F'
   b=a
   x=1
  if b in bases:
   bases[b]=$](bases[b],x)
  $(:
   bases[b]=x
   order.$%(b)
 if coef==0:
  if '$M' in bases:
   $! '$F'
  $) b in order:
   if b=='$F' or has(b,'$F'):
    $! '$F'
  $! coef
 facs=[]
 rad={}
 radorder=[]
 $, collect(p):
  c=1
  t=$/(p)
  if t is $w or t is $A or(t is $0 $* p[0]=='Q'):
   $! p
  if t is $0 $* p[0]=='*':
   items=p[1:]
  $(:
   items=(p,)
  $) f in items:
   if $C(f):
    c=nmul(c,f)
   $K isrrad(f):
    ex=f[2]
    if ex in rad:
     rad[ex]=rad[ex]*f[1]
     radorder.$%($#)
    $(:
     rad[ex]=f[1]
     radorder.$%(ex)
   $(:
    facs.$%(f)
  $! c
 $) b in order:
  p=pw(b,bases[b])
  if p=='$F':
   $! '$F'
  coef=nmul(coef,collect(p))
 if rad:
  multi=$5(radorder)!=$5(rad)
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
 if '$M' in facs:
  if $5(facs)==1 or $E:
   coef=$_(coef)if $/(coef)is $- $A $((1.0 if coef>0 $(-1.0)
   if $/(coef)is $A:
    coef=$w(coef)
 if $- facs:
  $! coef
 if $5(facs)>1:
  algs=[f $) f in facs if $&(f,'+')$* isalg(f)]
  if algs $* all([isalg(f)$) f in facs]):
   r=coef
   $) f in facs:
    r=expand_mul(r,f)
   $! r
 if $5(facs)==1:
  f=facs[0]
  if $/(coef)is $w $* coef==1:
   $! f
  if $/(f)is $0 $* f[0]=='+':
   $! $;([$:(coef,t)$) t in f[1:]])
  $!('*',coef,f)
 facs.sort(key=okey)
 if $/(coef)is $w $* coef==1:
  $!('*',)+$0(facs)
 $!('*',coef)+$0(facs)
$, $k(a):
 $! $:(-1,a)
$, $[(a,b):
 $! $](a,$:(-1,b))
$, $O(a,b):
 $! $:(a,pw(b,-1))
$, inv(a):
 $! pw(a,-1)
$, $V(a):
 $! pw(a,$s)
$, factor_int_small(n):
 fs=[]
 $) p in smallprimes():
  if p*p>n:
   $T
  if n%p==0:
   k=0
   $J n%p==0:
    n//=p
    k+=1
   fs.$%((p,k))
 $! fs,n
$, radical(n,q):
 if n<2:
  $! n,1
 a=1
 m=1
 fs,$d=factor_int_small(n)
 $) p,k in fs:
  a*=p**(k//q)
  m*=p**(k%q)
 if $d>1:
  r=iroot($d,q)
  if r**q==$d:
   a*=r
  $(:
   m*=$d
 $! a,m
$, ipow_root(n,p,q):
 if ibits(n)*p>2000 or q>60:
  $!('^',n,Q(p,q))
 a,m=radical(n**p,q)if p>1 $( radical(n,q)
 if m==1:
  $! a
 ex=Q(1,q)
 k=2
 $z=$#
 $J(1<<k)<=m $* k<=64:
  r=iroot(m,k)
  if r**k==m:
   $z=(r,k)
  k+=1
 if $z is $- $#:
  m=$z[0]
  ex=Q($z[1],q)
 if ex==1:
  $! a*m
 if $j(ex):
  $! a*m**ex
 if a==1:
  $!('^',m,ex)
 $!('*',a,('^',m,ex))
MAXBITS=12000
$, ibits(n):
 if n==0:
  $! 0
 h='%x'%$H(n)
 v=$w(h[0],16)
 $! 4*$5(h)-(3 if v<2 $( 2 if v<4 $( 1 if v<8 $( 0)
$, bigpow(b,x):
 n,d=nd(b)
 if d==1 $* $H(n)<=1:
  $! $3
 $! $H(x)*(ibits(n)+(ibits(d)if d>1 $( 0))>MAXBITS
$, pw_num(b,x):
 if $/(b)is $A or $/(x)is $A:
  bf=tofl(b)
  xf=tofl(x)
  if bf==0.0:
   if xf>0:
    $! 0.0
   if xf==0:
    $! 1.0
   $! '$F'
  if bf!=bf or xf!=xf:
   $! '$F'
  if bf<0 $*(xf in($A('$M'),$A('-$M'))or xf!=$W.floor(xf)):
   if $r(x)$* nd(x)[1]%2==1:
    r=(-bf)**xf
    $!-r if nd(x)[0]%2 $( r
   z=$1(bf)**xf
   $! fromcomplex(z)
  try:
   $! bf**xf
  $9 $`:
   $! '$M'
 if $/(x)is $w:
  if b==0:
   if x<0:
    $! '$F'
   $! 0
  if bigpow(b,x):
   $!('^',b,x)
  $! nipow(b,x)
 p,q=nd(x)
 if b==0:
  $! 0 if p>0 $( '$F'
 if $_(b)<0:
  if q%2==1:
   r=pw_num(nneg(b),x)
   if p%2:
    $! $:(-1,r)
   $! r
  if q==2:
   $! $:(pw('i',p),pw_num(nneg(b),x))
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
 $y=[]
 if n>1:
  $y.$%(ipow_root(n,fp,fq))
 if d>1:
  $y.$%(Q(1,d))
  $y.$%(ipow_root(d,fq-fp,fq))
 c=res
 facs=[]
 $) pt in $y:
  if $C(pt):
   c=nmul(c,pt)
  $K pt[0]=='*':
   c=nmul(c,pt[1])
   facs.$%(pt[2])
  $(:
   facs.$%(pt)
 if $5(facs)==2:
  if facs[0][2]==facs[1][2]:
   $! $:(c,pw_num(facs[0][1]*facs[1][1],facs[0][2]))
  facs.sort(key=okey)
 if $- facs:
  $! c
 if c==1:
  if $5(facs)==1:
   $! facs[0]
  $!('*',)+$0(facs)
 $!('*',c)+$0(facs)
$, isposconst(e):
 if $C(e):
  $! $_(e)>0
 if e=='pi' or e=='e':
  $! $E
 if isrrad(e):
  $! e[1]>0
 if $&(e,'^')$*(e[1]=='e' or e[1]=='pi')$* isreal_expr(e[2]):
  $! $E
 $! $3
$, isalg(e):
 t=$/(e)
 if t is $w or t is $A:
  $! $E
 if t is ${:
  $! e=='i'
 h=e[0]
 if h=='Q':
  $! $E
 if h=='^':
  $! $C(e[1])$* $C(e[2])
 if h=='+' or h=='*':
  $) a in e[1:]:
   if $- isalg(a):
    $! $3
  $! $E
 $! $3
''')
_x(r'''$, pw(b,x):
 if x==0:
  if b=='$F' or b=='$M':
   $! '$F'
  $! 1
 if $/(x)is $w $* x==1:
  $! b
 if b=='$F' or x=='$F':
  $! '$F'
 bn=$C(b)
 xn=$C(x)
 if bn $* xn:
  $! pw_num(b,x)
 if b==1 $* $/(b)is $w:
  $! 1
 if b=='$M':
  if xn:
   $! '$M' if $_(x)>0 $( 0
  if x=='$M':
   $! '$M'
 if xn $* b==0:
  $! 0 if $_(x)>0 $( '$F'
 if b=='i' $* $/(x)is $w:
  r=x%4
  $!(1,'i',-1,('*',-1,'i'))[r]
 if x=='$M' $* bn:
  if nabs(b)==1:
   $! '$F' if b==1 $( '$F'
  if ncmp(nabs(b),1)>0:
   $! '$M' if $_(b)>0 $( '$F'
  $! 0
 if b=='e':
  if x=='$M':
   $! '$M'
  if $&(x,'*')$* $5(x)==3 $* x[1]==-1 $* x[2]=='$M':
   $! 0
  if $/(x)is $A:
   $! $W.exp(x)
  if $&(x,'ln'):
   $! x[1]
  if $&(x,'*'):
   c,r=$a(x)
   if $&(r,'ln')$* $r(c):
    $! pw(r[1],c)
  if $&(x,'+'):
   outs=[]
   $d=[]
   $) t in x[1:]:
    c,r=$a(t)
    if $&(r,'ln')$* $r(c):
     outs.$%(pw(r[1],c))
    $(:
     $d.$%(t)
   if outs:
    $! $G(outs+[pw('e',$;($d))])
  if $&(x,'*')$* 'i' in x $* 'pi' in x:
   c,r=$a(x)
   if r==('*','i','pi')$* $r(c):
    $! $](cos_($:(c,'pi')),$:('i',sin_($:(c,'pi'))))
 if b!='e' $* $2(b)$* $2(x)$* $- $r(x)$*(has(b,'i')or has(x,'i'))$* $- $^(x):
  L=fn('ln',b)
  if $- $&(L,'ln')$* $-($&(L,'+')$* any([$&(t,'ln')$) t in L[1:]])):
   $! pw('e',$>($:(x,L)))
 if $/(b)is $0:
  h=b[0]
  if h=='^':
   bb=b[1]
   ee=b[2]
   if $/(x)is $w:
    $! pw(bb,$:(ee,x))
   if isposconst(bb):
    $! pw(bb,$:(ee,x))
   if $r(ee)$* $r(x):
    r=nmul(ee,x)
    if $/(ee)is $w:
     if ee%2==0:
      if $/(r)is $w $* r%2==0:
       $! pw(bb,r)
      $! pw(fn('$H',bb),r)
     $! pw(bb,r)
    if nd(ee)[0]%2==1 $* nd(ee)[1]%2==1:
     $! pw(bb,r)
    if nd(ee)[0]%2==1:
     $! pw(bb,r)
  $K h=='*':
   if $/(x)is $w:
    $! $G([pw(f,x)$) f in b[1:]])
   outs=[]
   $d=[]
   $) f in b[1:]:
    if $C(f):
     if $_(f)>0:
      outs.$%(pw(f,x))
     $K f!=-1:
      outs.$%(pw(nneg(f),x))
      $d.$%(-1)
     $(:
      $d.$%(f)
    $K isposconst(f)or $&(f,'$H'):
     outs.$%(pw(f,x))
    $(:
     $d.$%(f)
   if outs:
    $! $G(outs+[pw($G($d),x)])
  $K h=='$H':
   if $/(x)is $w $* x%2==0:
    $! pw(b[1],x)
  $K h=='+':
   if x==$s $* isalg(b)$* $- has(b,'i'):
    dn=denest(b)
    if dn is $- $#:
     $! dn
   if isq(x)$* x[2]==2 $* $_(x)<0 $* isalg(b)$* $- has(b,'i'):
    dn=denest(b)
    if dn is $- $#:
     $! pw(pw(dn,-1),-x[1])if x[1]!=-1 $( pw(dn,-1)
   if $/(x)is $w $* x!=1 $* $- isalg(b):
    c=sumcontent(b)
    if c!=1:
     $! $:(pw(c,x),pw($:(ninv(c),b),x))
    if leadneg(b):
     nb=$:(-1,b)
     if x%2==0:
      $! pw(nb,x)
     $! $:(-1,pw(nb,x))
   if $/(x)is $w $* isalg(b):
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
 fs=r[1:]if $&(r,'*')$((r,)
 $) f in fs:
  if $/(f)is ${ $* f $- in SPECIAL:
   d+=1
  $K $&(f,'^')$* $/(f[1])is ${ $* f[1]$- in SPECIAL $* $C(f[2]):
   d+=tofl(f[2])
 $! d
$, leadneg(b):
 $z=$#
 bk=$#
 $) t in b[1:]:
  if $C(t):
   $8
  c,r=$a(t)
  k=(-tdeg(r),okey(r))
  if bk is $# or k<bk:
   bk=k
   $z=c
 if $z is $#:
  $! $3
 $! $_($z)<0 if $C($z)$( $3
$, sumcontent(b):
 g=0
 L=1
 $) t in b[1:]:
  c,r=$a(t)
  if $- $r(c):
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
  if $r(t):
   a=nadd(a,t)
   $8
  cc,r=$a(t)
  if isrrad(r)$* r[2]==$s $* $r(cc)$*(n is $# or n==r[1]):
   n=r[1]
   c=nadd(c,cc)
  $(:
   $! $#
 if n is $# or c==0:
  $! $#
 d2=nsub(nmul(a,a),nmul(nmul(c,c),n))
 if $_(d2)<0:
  $! $#
 dn,dd=nd(d2)
 rn=isqrt(dn)
 rd=isqrt(dd)
 if rn*rn!=dn or rd*rd!=dd:
  $! $#
 d=Q(rn,rd)
 p=ndiv(nadd(a,d),2)
 m=ndiv(nsub(a,d),2)
 if $_(p)<0 or $_(m)<0:
  $! $#
 r=$](pw(p,$s),$:($_(c),pw(m,$s)))
 if $&(r,'+')$* $5(r)<=3:
  $! r
 $! $#
$, expand_mul(a,b):
 ta=a[1:]if $&(a,'+')$((a,)
 tb=b[1:]if $&(b,'+')$((b,)
 $?=[]
 $) u in ta:
  $) v in tb:
   $?.$%($:(u,v))
 $! $;($?)
$, expand_pow(b,n):
 r=1
 p=b
 $J n>0:
  if n&1:
   r=expand_mul(r,p)
  n>>=1
  if n:
   p=expand_mul(p,p)
 $! r
$, rationalize_inv(b):
 re_,im_=reim(b)
 if im_!=0:
  d=$]($:(re_,re_),$:(im_,im_))
  d=$>(d)
  if $&(d,'+'):
   r2=rationalize_inv(d)
   if r2 is $#:
    $! $#
  $(:
   r2=pw(d,-1)
  $! expand_mul($[(re_,$:('i',im_)),r2)
 $L=b[1:]if $&(b,'+')$((b,)
 kern=$#
 kerns=[]
 $) t in $L:
  c,r=$a(t)
  if r!=1 $* $- $C(r):
   if isrrad(r)$* r[2]==$s:
    if r $- in kerns:
     kerns.$%(r)
   $(:
    $! $#
 if $- kerns or $5(kerns)>3:
  $! $#
 kern=kerns[0]
 if $5(kerns)>1:
  A=$;([t $) t in $L if $a(t)[1]!=kern])
  B=$;([$a(t)[0]$) t in $L if $a(t)[1]==kern])
  den=$>($[($:(A,A),$:(B,B,kern[1])))
  if den==0:
   $! $#
  if $&(den,'+'):
   r2=rationalize_inv(den)
   if r2 is $#:
    $! $#
  $(:
   r2=pw(den,-1)
  $! expand_mul($[(A,$:(B,kern)),r2)
 a0=0
 a1=0
 $) t in $L:
  c,r=$a(t)
  if r==kern:
   a1=nadd(a1,c)
  $(:
   a0=$](a0,t)
 den=$[($:(a0,a0),$:(nmul(a1,a1),kern[1]))
 if den==0:
  $! $#
 $! expand_mul($[(a0,$:(a1,kern)),pw(den,-1))
''')
_x(r'''$, reim(e):
 t=$/(e)
 if t is $w or t is $A:
  $! e,0
 if t is ${:
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
  $! $;(rs),$;(ims)
 if h=='*':
  r=1
  i=0
  $) a in e[1:]:
   ar,ai=reim(a)
   if ai==0:
    r=$:(r,ar)
    i=$:(i,ar)
   $(:
    r,i=$[($:(r,ar),$:(i,ai)),$]($:(r,ai),$:(i,ar))
  $! r,i
 if h=='^':
  b=e[1]
  x=e[2]
  if $- has(b,'i')$* $- has(x,'i'):
   if $C(x)$* $- $r(x):
    $! e,0
   if $r(x)$* nd(x)[1]%2==0:
    if $2(b):
     v=cv(b)
     if v is $- $# $* $/(v)is $- $1 $* v<0:
      $! reim_generic(e)
    $! e,0
   $! e,0
  if $/(x)is $w:
   br,bi=reim(b)
   if x>0:
    z=expand_pow($](br,$:('i',bi)),x)
    if has(z,'i')$* z!=e:
     $! reim(z)
   $K $2(b):
    r=rationalize_inv(b)
    if r is $- $#:
     $! reim(expand_pow(r,-x))if x!=-1 $( reim(r)
  $! reim_generic(e)
 if h in('$I','mat','${'):
  $! e,0
 $) a in e[1:]:
  if has(a,'i'):
   $! reim_generic(e)
 $! e,0
$, cv(u):
 try:
  v=$S(u)
 $9($R,$U,$D,$`,TypeError):
  $! $#
 if v!=v:
  $! $#
 if $/(v)is $1:
  if v.$N!=v.$N or v.imag!=v.imag:
   $! $#
  if $H(v.$N)==$A('$M')or $H(v.imag)==$A('$M'):
   $! $#
 $K $H(v)==$A('$M'):
  $! $#
 $! v
$, reim_generic(e):
 if $2(e):
  v=cv(e)
  if v is $#:
   $!('$N',e),('imag',e)
  z=$1(v)
  $! z.$N,z.imag
 $!('$N',e),('imag',e)
$, conj(e):
 r,i=reim(e)
 $! $[(r,$:('i',i))
$, fromcomplex(z):
 if $/(z)is $- $1:
  $! z
 if z.imag==0:
  $! z.$N
 if z.$N==0:
  $! $:(z.imag,'i')
 $! $](z.$N,$:(z.imag,'i'))
$o={}
$, fn($B,*$Y):
 if $5($Y)==1 $* $/($Y[0])is $I:
  $Y=$0($Y[0])
 $) a in($Y[:1]if $B=='when' $( $Y):
  if a=='$F':
   $! '$F'
 f=$o.get($B)
 if f is $- $#:
  r=f(*$Y)
  if r is $- $#:
   $! r
 $!($B,)+$0($Y)
$, isneg(e):
 if $C(e):
  $! $_(e)<0
 if $&(e,'*'):
  $! $C(e[1])$* $_(e[1])<0
 if $&(e,'+'):
  $! leadneg(e)
 $! $3
$, isreal_expr(e):
 if $C(e):
  $! $E
 if $/(e)is ${:
  $! e!='i' $* e!='$F'
 $! $- has(e,'i')
$, fval($B,x):
 $! fromcomplex(NUMF[$B](x))
$, fvalc($B,u):
 try:
  v=NUMF[$B]($S(u))
 $9($R,$U,$D,$`,TypeError):
  $! $#
 if $/(v)is $1:
  if v.$N!=v.$N or v.imag!=v.imag:
   $! $#
 $K v!=v:
  $! $#
 $! fromcomplex(v)
$, pi_coef(u):
 if u=='pi':
  $! 1
 if u==0:
  $! 0
 if $&(u,'*')$* $5(u)==3 $* u[2]=='pi' $* $r(u[1]):
  $! u[1]
 $! $#
$, split_pi(u):
 if $&(u,'+'):
  $) t in u[1:]:
   c=pi_coef(t)
   if c is $- $# $* c!=0:
    $d=$;([s $) s in u[1:]if s is $- t])
    $! c,$d
 $! $#
TRIGT=$#
$, trig_table():
 global TRIGT
 if TRIGT is $#:
  s2=$V(2)
  s3=$V(3)
  s5=$V(5)
  s6=$V(6)
  q=Q
  T={}
  T[0]=0
  T[q(1,12)]=$:(q(1,4),$[(s6,s2))
  T[q(1,10)]=$:(q(1,4),$[(s5,1))
  T[q(1,8)]=$:($s,$V($[(2,s2)))
  T[q(1,6)]=$s
  T[q(1,5)]=$:(q(1,4),$V($[(10,$:(2,s5))))
  T[q(1,4)]=$:($s,s2)
  T[q(3,10)]=$:(q(1,4),$](s5,1))
  T[q(1,3)]=$:($s,s3)
  T[q(3,8)]=$:($s,$V($](2,s2)))
  T[q(2,5)]=$:(q(1,4),$V($](10,$:(2,s5))))
  T[q(5,12)]=$:(q(1,4),$](s6,s2))
  T[$s]=1
  TT={}
  TT[0]=0
  TT[q(1,12)]=$[(2,s3)
  TT[q(1,8)]=$[(s2,1)
  TT[q(1,6)]=$:(q(1,3),s3)
  TT[q(1,4)]=1
  TT[q(1,3)]=s3
  TT[q(3,8)]=$](s2,1)
  TT[q(5,12)]=$](2,s3)
  TT[q(1,5)]=$V($[(5,$:(2,s5)))
  TT[q(2,5)]=$V($](5,$:(2,s5)))
  TT[q(1,10)]=$:(q(1,5),$V($[(25,$:(10,s5))))
  TT[q(3,10)]=$:(q(1,5),$V($](25,$:(10,s5))))
  TRIGT=(T,TT)
 $! TRIGT
$, sin_pi(c):
 c=nsub(c,nmul(2,nfloor(nmul(c,$s))))
 sg=1
 if ncmp(c,1)>=0:
  c=nsub(c,1)
  sg=-1
 if ncmp(c,$s)>0:
  c=nsub(1,c)
 T=trig_table()[0]
 if c in T:
  $! $:(sg,T[c])
 if sg<0:
  $! $k(('sin',$:(c,'pi')))
 $!('sin',$:(c,'pi'))
$, tan_pi(c):
 c=nsub(c,nfloor(c))
 sg=1
 if ncmp(c,$s)>0:
  c=nsub(1,c)
  sg=-1
 if c==$s:
  $! '$F'
 TT=trig_table()[1]
 if c in TT:
  $! $:(sg,TT[c])
 $! $:(sg,('tan',$:(c,'pi')))
$, sin_(u):
 if $C(u):
  if u==0:
   $! 0
  if $/(u)is $A:
   $! $W.sin(u)
  if $_(u)<0:
   $! $k(fn('sin',$k(u)))
  $! $#
 if u=='$M' or u==('*',-1,'$M'):
  $! '$F'
 c=pi_coef(u)
 if c is $- $#:
  $! sin_pi(c)
 if $^(u)$* $2(u):
  $! fvalc('sin',u)
 if isneg(u):
  $! $k(fn('sin',$k(u)))
 sp=split_pi(u)
 if sp is $- $#:
  c,$d=sp
  c=nsub(c,nmul(2,nfloor(nmul(c,$s))))
  if c==0:
   $! fn('sin',$d)
  if c==1:
   $! $k(fn('sin',$d))
  if c==$s:
   $! fn('cos',$d)
  if c==Q(3,2):
   $! $k(fn('cos',$d))
  if ncmp(c,1)>0:
   $!('sin',$]($d,$:(nsub(c,2),'pi')))
  $!('sin',$]($d,$:(c,'pi')))
 if $&(u,'$~'):
  $! u[1]
 if $&(u,'arccos'):
  $! $V($[(1,pw(u[1],2)))
 if $&(u,'$x'):
  $! $O(u[1],$V($](1,pw(u[1],2))))
 $! $#
''')
_x(r'''$, cos_(u):
 if $C(u):
  if u==0:
   $! 1
  if $/(u)is $A:
   $! $W.cos(u)
  if $_(u)<0:
   $! fn('cos',$k(u))
  $! $#
 if u=='$M' or u==('*',-1,'$M'):
  $! '$F'
 c=pi_coef(u)
 if c is $- $#:
  $! sin_pi(nadd(c,$s))
 if $^(u)$* $2(u):
  $! fvalc('cos',u)
 if isneg(u):
  $! fn('cos',$k(u))
 sp=split_pi(u)
 if sp is $- $#:
  c,$d=sp
  c=nsub(c,nmul(2,nfloor(nmul(c,$s))))
  if c==0:
   $! fn('cos',$d)
  if c==1:
   $! $k(fn('cos',$d))
  if c==$s:
   $! $k(fn('sin',$d))
  if c==Q(3,2):
   $! fn('sin',$d)
  if ncmp(c,1)>0:
   $!('cos',$]($d,$:(nsub(c,2),'pi')))
  $!('cos',$]($d,$:(c,'pi')))
 if $&(u,'arccos'):
  $! u[1]
 if $&(u,'$~'):
  $! $V($[(1,pw(u[1],2)))
 if $&(u,'$x'):
  $! pw($](1,pw(u[1],2)),Q(-1,2))
 $! $#
$, tan_(u):
 if $C(u):
  if u==0:
   $! 0
  if $/(u)is $A:
   $! $W.tan(u)
  if $_(u)<0:
   $! $k(fn('tan',$k(u)))
  $! $#
 c=pi_coef(u)
 if c is $- $#:
  $! tan_pi(c)
 if $^(u)$* $2(u):
  $! fvalc('tan',u)
 if isneg(u):
  $! $k(fn('tan',$k(u)))
 sp=split_pi(u)
 if sp is $- $#:
  c,$d=sp
  c=nsub(c,nfloor(c))
  if c==0:
   $! fn('tan',$d)
  if c==$s:
   $! $k(pw(fn('tan',$d),-1))
  $!('tan',$]($d,$:(c,'pi')))
 if $&(u,'$x'):
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
 if $C(u):
  if $/(u)is $A:
   if-1.0<=u<=1.0:
    $! $W.asin(u)
   $! fval('$~',u)
 if isneg(u):
  $! $k(fn('$~',$k(u)))
 S=inv_table()[0]
 if u in S:
  $! $:(S[u],'pi')
 if $2(u)$* $^(u):
  $! fvalc('$~',u)
 $! $#
$, acos_(u):
 if $C(u)$* $/(u)is $A:
  if-1.0<=u<=1.0:
   $! $W.acos(u)
  $! fval('arccos',u)
 a=asin_(u)
 if a is $- $# $* $- $&(a,'$~')$* $4(a,'$~'):
  $! $[($:($s,'pi'),a)
 if isneg(u):
  $! $[('pi',fn('arccos',$k(u)))
 $! $#
$, atan_(u):
 if $C(u):
  if $/(u)is $A:
   $! $W.atan(u)
 if u=='$M':
  $! $:($s,'pi')
 if u==('*',-1,'$M'):
  $! $:(Q(-1,2),'pi')
 if isneg(u):
  $! $k(fn('$x',$k(u)))
 Tn=inv_table()[1]
 if u in Tn:
  $! $:(Tn[u],'pi')
 if $2(u)$* $^(u):
  $! fvalc('$x',u)
 $! $#
$, ln_(u):
 if $C(u):
  if u==1:
   $! 0
  if u==0:
   $!('*',-1,'$M')
  if $/(u)is $A:
   if u>0:
    $! $W.log(u)
   $! $]($W.log(-u),$:($W.pi,'i'))
  if $_(u)<0:
   $! $](fn('ln',nneg(u)),$:('i','pi'))
  n,d=nd(u)
  if n==1:
   $! $k(fn('ln',d))
  $! $#
 if u=='e':
  $! 1
 if u=='$M':
  $! '$M'
 if u=='i':
  $! $:($s,'i','pi')
 if $&(u,'^'):
  if u[1]=='e' $* isreal_expr(u[2]):
   $! u[2]
  if isposconst(u[1])$* isreal_expr(u[2])$* $C(u[2]):
   $! $:(u[2],fn('ln',u[1]))
 if $2(u)$* $^(u):
  $! fvalc('ln',u)
 $! $#
$, log_(u,b=10):
 if $C(u)$* $C(b):
  if $/(u)is $A or $/(b)is $A:
   a1=fvalc('ln',u)
   a2=fvalc('ln',b)
   if a1 is $- $# $* a2 is $- $# $* a2!=0:
    $! $O(a1,a2)
   $! $#
  if u==1:
   $! 0
  if $r(u)$* $r(b)$* $_(u)>0 $* $_(b)>0 $* b!=1:
   k=exact_log(u,b)
   if k is $- $#:
    $! k
 if u==b:
  $! 1
 if $&(u,'^')$* u[1]==b $* isreal_expr(u[2]):
  $! u[2]
 if $2(u)$* $2(b)$*($^(u)or $^(b)):
  a1=fvalc('ln',u)
  a2=fvalc('ln',b)
  if a1 is $- $# $* a2 is $- $# $* a2!=0:
   $! $O(a1,a2)
  $! $#
 $! $#
$, exact_log(u,b):
 un,ud=nd(u)
 bn,bd=nd(b)
 lu=$W.log(tofl(u))
 lb=$W.log(tofl(b))
 if lb==0:
  $! $#
 k=lu/lb
 $) den in $+(1,13):
  num=$w(round(k*den))
  if $H(k*den-num)<1e-9:
   kk=Q(num,den)
   if pw_num(b,kk)==u:
    $! kk
   $! $#
 $! $#
$, abs_(u):
 if $C(u):
  $! nabs(u)
 if u=='$M' or u==('*',-1,'$M'):
  $! '$M'
 if $&(u,'$H'):
  $! u
 if $&(u,'^')$* $/(u[2])is $w $* u[2]%2==0 $* isreal_expr(u[1]):
  $! u
 if has(u,'i'):
  r,i=reim(u)
  if i!=0 $* $- has(r,'i')$* $- has(i,'i'):
   $! $V($](pw(r,2),pw(i,2)))
 if $2(u):
  v=cv(u)
  if v is $- $# $* $/(v)is $- $1:
   if v>=0:
    $! u
   $! $k(u)
 if $&(u,'*'):
  outs=[]
  $d=[]
  $) f in u[1:]:
   if $C(f):
    outs.$%(nabs(f))
   $K $2(f):
    outs.$%(abs_(f)or('$H',f))
   $K $&(f,'^')$* $/(f[2])is $w $* f[2]%2==0:
    outs.$%(f)
   $K $&(f,'^')$* f[1]=='e':
    outs.$%(f)
   $(:
    $d.$%(f)
  if outs:
   $! $G(outs+[fn('$H',$G($d))])
 if isneg(u):
  $! fn('$H',$k(u))
 if $&(u,'^')$* u[1]=='e' $* isreal_expr(u[2]):
  $! u
 $! $#
$, sign_(u):
 if $C(u):
  $! $_(u)if $/(u)is $- $A $( $A($_(u))
 if u=='$M':
  $! 1
 if $2(u):
  v=cv(u)
  if v is $- $# $* $/(v)is $- $1:
   $! 1 if v>0 $((-1 if v<0 $( 0)
 if $&(u,'*')$* $C(u[1]):
  $! $:($_(u[1]),fn('sign',cmul(nabs(u[1]),$a(u)[1])))
 if $&(u,'^')$* $/(u[2])is $w $* u[2]%2==0:
  $! $#
 $! $#
$, finite(v):
 $! v==v $* v!=$A('$M')$* v!=$A('-$M')
$, floor_(u):
 if $C(u):
  if $/(u)is $A:
   $! $A($W.floor(u))if finite(u)$( $#
  $! nfloor(u)
 if $2(u)$* $- has(u,'i'):
  v=cv(u)
  if v is $- $# $* $/(v)is $- $1:
   $! $w($W.floor(v))
 $! $#
$, ceil_(u):
 f=floor_($k(u))
 if f is $- $#:
  $! $k(f)
 $! $#
$, sinh_(u):
 if u==0:
  $! 0
 if isneg(u):
  $! $k(fn('sinh',$k(u)))
 if $&(u,'arcsinh'):
  $! u[1]
 $! $#
''')
_x(r'''$, cosh_(u):
 if u==0:
  $! 1
 if isneg(u):
  $! fn('cosh',$k(u))
 if $&(u,'arccosh'):
  $! u[1]
 $! $#
$, tanh_(u):
 if u==0:
  $! 0
 if isneg(u):
  $! $k(fn('tanh',$k(u)))
 $! $#
$, odd0($B):
 $, g(u):
  if u==0:
   $! 0
  if isneg(u):
   $! $k(fn($B,$k(u)))
  $! $#
 $! g
$, fact_(u):
 if $/(u)is $w:
  if u<0:
   $! '$F'
  if u>1000:
   $! $#
  r=1
  $) k in $+(2,u+1):
   r*=k
  $! r
 if isq(u)$* u[2]==2 $* u[1]>0:
  n=u[1]
  r=$:($V('pi'),Q(1,1))
  k=Q(1,2)
  $J ncmp(k,u)<=0:
   r=$:(r,k)
   k=nadd(k,1)
  $! r
 if $/(u)is $A:
  if u<0 $* u==$W.floor(u):
   $! '$F'
  try:
   $! gamma(u+1.0)
  $9($`,$D,$U):
   $! '$M' if u>0 $( '$F'
 $! $#
$, gamma(x):
 try:
  $! $W.gamma(x)
 $9 AttributeError:
  pass
 if x<0.5:
  $! $W.pi/($W.sin($W.pi*x)*gamma(1.0-x))
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
 $! $W.$V(2*$W.pi)*h*$W.exp(-t)*h*a
$, real_(u):
 if $2(u)or has(u,'i'):
  r,i=reim(u)
  if $- $&(r,'$N'):
   $! r
 if isreal_expr(u):
  $! u
 $! $#
$, imag_(u):
 if isreal_expr(u):
  $! 0
 r,i=reim(u)
 if $- $&(i,'imag'):
  $! i
 $! $#
$, conj_(u):
 if isreal_expr(u):
  $! u
 r,i=reim(u)
 if $- $&(r,'$N'):
  $! $[(r,$:('i',i))
 $! $#
$, angle_(u):
 r,i=reim(u)
 if $&(r,'$N')or $&(i,'imag'):
  $! $#
 if i==0:
  if $2(r):
   v=cv(r)
   if v is $- $# $* $/(v)is $- $1:
    if v>=0:
     $! 0
    $! 'pi'
  $! $#
 if r==0:
  if $2(i):
   v=cv(i)
   if v is $- $# $* $/(v)is $- $1:
    $! $:(Q(1 if v>0 $(-1,2),'pi')
  $! $#
 if $2(r)$* $2(i):
  vr=cv(r)
  vi=cv(i)
  if vr is $# or vi is $# or $/(vr)is $1 or $/(vi)is $1:
   $! $#
  a=fn('$x',$O(i,r))
  if vr<0:
   if vi>=0:
    a=$](a,'pi')
   $(:
    a=$[(a,'pi')
  $! a
 $! $#
$o['sin']=sin_
$o['cos']=cos_
$o['tan']=tan_
$o['$~']=asin_
$o['arccos']=acos_
$o['$x']=atan_
$o['ln']=ln_
$o['log']=log_
$o['$H']=abs_
$o['sign']=sign_
$o['floor']=floor_
$o['ceiling']=ceil_
$o['sinh']=sinh_
$o['cosh']=cosh_
$o['tanh']=tanh_
$o['arcsinh']=odd0('arcsinh')
$o['arctanh']=odd0('arctanh')
$o['arccosh']=$7 u:0 if u==1 $( $#
$o['fact']=fact_
$o['$N']=real_
$o['imag']=imag_
$o['conj']=conj_
$o['$p']=angle_
$o['exp']=$7 u:pw('e',u)
$o['$V']=$7 u:pw(u,$s)
$o['sec']=$7 u:pw(fn('cos',u),-1)
$o['csc']=$7 u:pw(fn('sin',u),-1)
$o['cot']=$7 u:pw(fn('tan',u),-1)
$o['sech']=$7 u:pw(fn('cosh',u),-1)
$o['csch']=$7 u:pw(fn('sinh',u),-1)
$o['coth']=$7 u:pw(fn('tanh',u),-1)
$o['arcsec']=$7 u:fn('arccos',pw(u,-1))
$o['arccsc']=$7 u:fn('$~',pw(u,-1))
$o['arccot']=$7 u:$[($:($s,'pi'),fn('$x',u))
$o['arcsech']=$7 u:fn('arccosh',pw(u,-1))
$o['arccsch']=$7 u:fn('arcsinh',pw(u,-1))
$o['arccoth']=$7 u:fn('arctanh',pw(u,-1))
$, root_(u,n=2):
 $! pw(u,pw(n,-1))
$o['root']=root_
import cmath
$, _c(f):
 $, g(x):
  try:
   if $/(x)is $1:
    $! f[1](x)
   $! f[0](x)
  $9($U,TypeError):
   $! f[1]($1(x))
 $! g
$, _ln(x):
 if $/(x)is $- $1 $* x>0:
  $! $W.log(x)
 if x==0:
  $! $A('-$M')
 $! cmath.log($1(x))
$, _asinr(x):
 if-1<=x<=1:
  $! $W.asin(x)
 $l $U
$, _acosr(x):
 if-1<=x<=1:
  $! $W.acos(x)
 $l $U
$, _casin(z):
 $!-1j*cmath.log(1j*z+cmath.$V(1-z*z))
$, _cacos(z):
 $! $W.pi/2-_casin(z)
$, _catan(z):
 $! 0.5j*cmath.log((1-1j*z)/(1+1j*z))
$, _sinh(x):
 $!(cmath.exp(x)-cmath.exp(-x))/2 if $/(x)is $1 $(($W.exp(x)-$W.exp(-x))/2
$, _cosh(x):
 $!(cmath.exp(x)+cmath.exp(-x))/2 if $/(x)is $1 $(($W.exp(x)+$W.exp(-x))/2
$, _tanh(x):
 if $/(x)is $- $1:
  if x>20:
   $! 1.0
  if x<-20:
   $!-1.0
  a=$W.exp(2*x)
  $!(a-1)/(a+1)
 a=cmath.exp(2*x)
 $!(a-1)/(a+1)
$, _asinh(x):
 if $/(x)is $- $1:
  $! $W.log(x+$W.$V(x*x+1))if x>=0 $(-$W.log(-x+$W.$V(x*x+1))
 $! cmath.log(x+cmath.$V(x*x+1))
$, _acosh(x):
 if $/(x)is $- $1 $* x>=1:
  $! $W.log(x+$W.$V(x*x-1))
 x=$1(x)
 $! cmath.log(x+cmath.$V(x+1)*cmath.$V(x-1))
$, _atanh(x):
 if $/(x)is $- $1 $*-1<x<1:
  $! 0.5*$W.log((1+x)/(1-x))
 x=$1(x)
 $! 0.5*cmath.log((1+x)/(1-x))
$, _sign(x):
 if $/(x)is $1:
  $! x/$H(x)if x!=0 $( 0.0
 $! 1.0 if x>0 $((-1.0 if x<0 $( 0.0)
$, _floor(x):
 if $/(x)is $1:
  $! $1($W.floor(x.$N),$W.floor(x.imag))
 $! $A($W.floor(x))
$, _ceil(x):
 if $/(x)is $1:
  $! $1($W.ceil(x.$N),$W.ceil(x.imag))
 $! $A($W.ceil(x))
$, _real(x):
 $! x.$N if $/(x)is $1 $( x
$, _imag(x):
 $! x.imag if $/(x)is $1 $( 0.0
$, _conj(x):
 $! x.conjugate()if $/(x)is $1 $( x
$, _angle(x):
 if $/(x)is $1:
  $! cmath.phase(x)
 $! 0.0 if x>=0 $( $W.pi
$, _fact(x):
 if $/(x)is $1:
  $l $U
 $! gamma(x+1.0)
''')
_x(r'''NUMF={
 'sin':_c(($W.sin,cmath.sin)),'cos':_c(($W.cos,cmath.cos)),
 'tan':_c(($W.tan,$7 z:cmath.sin(z)/cmath.cos(z))),
 '$~':_c((_asinr,_casin)),'arccos':_c((_acosr,_cacos)),
 '$x':_c(($W.atan,_catan)),
 'ln':_ln,'exp':_c(($W.exp,cmath.exp)),
 '$V':_c(($7 x:$W.$V(x)if x>=0 $( cmath.$V(x),cmath.$V)),
 '$H':$H,'sign':_sign,'floor':_floor,'ceiling':_ceil,
 'sinh':_sinh,'cosh':_cosh,'tanh':_tanh,
 'arcsinh':_asinh,'arccosh':_acosh,'arctanh':_atanh,
 '$N':_real,'imag':_imag,'conj':_conj,'$p':_angle,
 'fact':_fact,
 }
$, nfun_call($B,$e):
 if $B=='log':
  b=$e[1]if $5($e)>1 $( 10.0
  $! _ln($e[0])/_ln(b)
 if $B=='root':
  n=$e[1]if $5($e)>1 $( 2.0
  $! npow($e[0],1.0/n)
 if $B=='round':
  d=$w($e[1])if $5($e)>1 $( 0
  $! round($e[0],d)
 if $B=='when':
  $! $e[1]if $e[0]$(($e[2]if $5($e)>2 $( $A('nan'))
 if $B=='max':
  $! max($e)
 if $B=='min':
  $! min($e)
 if $B=='mod':
  $! $e[0]-$e[1]*$W.floor($e[0]/$e[1])if $e[1]!=0 $( $e[0]
 f=NUMF.get($B)
 if f is $#:
  if $B in('sec','csc','cot','sech','csch','coth'):
   base={'sec':'cos','csc':'sin','cot':'tan','sech':'cosh','csch':'sinh','coth':'tanh'}[$B]
   $! 1.0/NUMF[base]($e[0])
  if $B in('arcsec','arccsc','arccot','arcsech','arccsch','arccoth'):
   base={'arcsec':'arccos','arccsc':'$~','arccot':'$x','arcsech':'arccosh','arccsch':'arcsinh','arccoth':'arctanh'}[$B]
   $! NUMF[base](1.0/$e[0])
  if $B in('ipart','$w'):
   $! $A($w($e[0]))
  if $B=='fpart':
   $! $e[0]-$w($e[0])
  err("Cannot evaluate "+$B)
 $! f($e[0])
$, npow(a,b):
 if $/(a)is $- $1 $* $/(b)is $- $1:
  if a<0 $*(b!=b or b in($A('$M'),$A('-$M'))or b!=$W.floor(b)):
   $! $1(a)**b
  if a==0 $* b<0:
   $l $D
  try:
   $! a**b
  $9 $`:
   $! $A('$M')
 if a==0:
  $! 0.0
 $! $1(a)**b
NCONST={'pi':$W.pi,'e':$W.e,'i':1j,'$M':$A('$M')}
$, $S(e,env=$#):
 t=$/(e)
 if t is $w:
  try:
   $! $A(e)
  $9 $`:
   $! '$M' if e>0 $(('*',-1,'$M')
 if t is $A:
  $! e
 if t is ${:
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
   s=s+$S(a,env)
  $! s
 if h=='*':
  s=1.0
  $) a in e[1:]:
   s=s*$S(a,env)
  $! s
 if h=='^':
  b=e[1]
  x=e[2]
  if isq(x)$* x[2]%2==1:
   bv=$S(b,env)
   if $/(bv)is $- $1 $* bv<0:
    r=(-bv)**(x[1]/x[2])
    $!-r if x[1]%2 $( r
   $! npow(bv,x[1]/x[2])
  if $/(x)is $w:
   bv=$S(b,env)
   if bv==0 $* x<0:
    $l $D
   $! bv**x
  $! npow($S(b,env),$S(x,env))
 if h in('$I','mat','${','Q'):
  err("Not numeric")
 if h=='when':
  c=nbool(e[1],env)
  if c:
   $! $S(e[2],env)
  $! $S(e[3],env)if $5(e)>3 $( $A('nan')
 $e=[$S(a,env)$) a in e[1:]]
 $! nfun_call(h,$e)
$, nbool(c,env):
 h=head(c)
 if h in('<','>','<=','>=','=','/='):
  a=$S(c[1],env)
  b=$S(c[2],env)
  if $/(a)is $1:
   a=a.$N
  if $/(b)is $1:
   b=b.$N
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
    $! $3
  $! $E
 if h=='or':
  $) a in c[1:]:
   if nbool(a,env):
    $! $E
  $! $3
 if h=='$-':
  $! $- nbool(c[1],env)
 if c=='true':
  $! $E
 if c=='false':
  $! $3
 err("Not a condition")
$, nreal(e,env=$#):
 v=$S(e,env)
 if $/(v)is $1:
  if $H(v.imag)>1e-9*(1+$H(v.$N)):
   $l $U
  $! v.$N
 $! v
$, simp(e):
 t=$/(e)
 if t is $- $0:
  $! e
 h=e[0]
 if h=='Q' or h=='${' or h=='hold':
  if h=='hold':
   $! simp(e[1])
  $! e
 $Y=[simp(a)$) a in e[1:]]
 if h=='+':
  $! $;($Y)
 if h=='*':
  $! $G($Y)
 if h=='^':
  $! pw($Y[0],$Y[1])
 if h in('$I','mat','=','<','>','<=','>=','/=','$*','or','$-'):
  $!(h,)+$0($Y)
 $! fn(h,$Y)
$, $Q(e,old,new):
 if e==old:
  $! new
 t=$/(e)
 if t is $- $0 or e[0]=='Q' or e[0]=='${':
  $! e
 ch=$3
 $Y=[]
 $) a in e[1:]:
  b=$Q(a,old,new)
  if b is $- a:
   ch=$E
  $Y.$%(b)
 if $- ch:
  $! e
 $! simp((e[0],)+$0($Y))
$, subsd(e,d):
 t=$/(e)
 if t is ${:
  if e in d:
   $! d[e]
  $! e
 if t is $- $0 or e[0]=='Q' or e[0]=='${':
  $! e
 ch=$3
 $Y=[]
 $) a in e[1:]:
  b=subsd(a,d)
  if b is $- a:
   ch=$E
  $Y.$%(b)
 if $- ch:
  $! e
 $! simp((e[0],)+$0($Y))
$, mapexpr(f,e):
 if $&(e,'$I'):
  $!('$I',)+$0(mapexpr(f,a)$) a in e[1:])
 if $&(e,'mat'):
  $!('mat',)+$0(mapexpr(f,a)$) a in e[1:])
 $! f(e)
$, $>(e):
 t=$/(e)
 if t is $- $0:
  $! e
 h=e[0]
 if h=='Q' or h=='${':
  $! e
 if h=='+':
  $! $;([$>(a)$) a in e[1:]])
 if h=='*':
  r=1
  $) f in e[1:]:
   r=expand_mul(r,$>(f))
  $! r
 if h=='^':
  b=$>(e[1])
  x=$>(e[2])
  if $&(b,'+')$* $/(x)is $w:
   if x>0:
    $! expand_pow(b,x)
   if x<0:
    $! pw(expand_pow(b,-x),-1)
  if $&(b,'*')$* $/(x)is $w:
   $! $>($G([pw(f,x)$) f in b[1:]]))
  if b=='e' $* $&(x,'+'):
   $! $G([pw('e',a)$) a in x[1:]])
  if $&(x,'+')$* $C(b):
   $! $G([pw(b,a)$) a in x[1:]])
  $! pw(b,x)
 if h in('$I','mat','=','<','>','<=','>=','/=','$*','or','$-'):
  $!(h,)+$0($>(a)$) a in e[1:])
 $! fn(h,[$>(a)$) a in e[1:]])
''')
_x(r'''$, evalf(e):
 t=$/(e)
 if t is $w:
  $! $A(e)
 if t is $A:
  $! e
 if t is ${:
  if e=='pi':
   $! $W.pi
  if e=='e':
   $! $W.e
  $! e
 h=e[0]
 if h=='Q':
  $! e[1]/e[2]
 if h=='${':
  $! e
 if $2(e)$* h $- in('$I','mat','=','<','>','<=','>=','/=','$*','or','$-'):
  try:
   v=$S(e)
   if $/(v)is $1:
    $! fromcomplex(v)
   if v!=v:
    $! '$F'
   if v==$A('$M'):
    $! '$M'
   if v==$A('-$M'):
    $!('*',-1,'$M')
   $! v
  $9($D,$U,$`,TypeError):
   pass
  $9 $R:
   pass
 $Y=[evalf(a)$) a in e[1:]]
 if h=='^' $* $/(e[2])is $w:
  $Y[1]=e[2]
 $! simp((h,)+$0($Y))
$, exactify(e,tol=$#):
 t=$/(e)
 if t is $A:
  $! float2rat(e,tol)
 if t is $0 $* e[0]!='Q' $* e[0]!='${':
  $! simp((e[0],)+$0(exactify(a,tol)$) a in e[1:]))
 $! e
$, float2rat(x,tol=$#):
 if x!=x:
  $! '$F'
 if x==$A('$M'):
  $! '$M'
 if x==$A('-$M'):
  $!('*',-1,'$M')
 if x==$W.floor(x)$* $H(x)<1e18:
  $! $w(x)
 if tol is $#:
  tol=5e-14*max(1.0,$H(x))
 h0,h1=0,1
 k0,k1=1,0
 y=x
 $) _ in $+(60):
  a=$W.floor(y)
  h0,h1=h1,$w(a)*h1+h0
  k0,k1=k1,$w(a)*k1+k0
  if $H(h1/k1-x)<=tol:
   $T
  f=y-a
  if f==0:
   $T
  y=1.0/f
 $! Q(h1,k1)
$, degree(e,x):
 if $4(e,x):
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
 if h=='^' $* $/(e[2])is $w $* e[2]>0:
  k=degree(e[1],x)
  if k is $#:
   $! $#
  $! k*e[2]
 $! $#
$, $X(e,x):
 e=$>(e)
 if $4(e,x):
  $![e]
 $L=e[1:]if $&(e,'+')$((e,)
 cs={}
 mx=0
 $) t in $L:
  if $&(t,'*'):
   k=0
   $d=[]
   $) f in t[1:]:
    if f==x:
     k+=1
    $K $&(f,'^')$* f[1]==x $* $/(f[2])is $w $* f[2]>0:
     k+=f[2]
    $K $4(f,x):
     $d.$%(f)
    $(:
     $! $#
   c=$G($d)
  $K t==x:
   k=1
   c=1
  $K $&(t,'^')$* t[1]==x $* $/(t[2])is $w $* t[2]>0:
   k=t[2]
   c=1
  $K $4(t,x):
   k=0
   c=t
  $(:
   $! $#
  cs[k]=$](cs.get(k,0),c)
  if k>mx:
   mx=k
 $![cs.get(k,0)$) k in $+(mx+1)]
$, fromcoeffs(cs,x):
 $! $;([$:(cs[k],pw(x,k))$) k in $+($5(cs))])
$, numer_denom(e):
 if $&(e,'*'):
  nu=[]
  de=[]
  $) f in e[1:]:
   if isq(f):
    nu.$%(f[1])
    de.$%(f[2])
   $K $&(f,'^')$* $C(f[2])$* $_(f[2])<0:
    de.$%(pw(f[1],nneg(f[2])))
   $(:
    nu.$%(f)
  $! $G(nu),$G(de)
 if isq(e):
  $! e[1],e[2]
 if $&(e,'^')$* $C(e[2])$* $_(e[2])<0:
  $! 1,pw(e[1],nneg(e[2]))
 $! e,1
''')
_x(r'''OPT={'uni':$E,'digits':10}
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
USYM={'pi':'\u03c0','$M':'\u221e','theta':'\u03b8'}
REL={'=':'=','<':'<','>':'>','<=':'\u2264','>=':'\u2265','/=':'\u2260'}
PRIO='xyztuvwsrqpnmlkjhgfdcba'
$, fmt(e):
 $! pr(e,$3)[0]
$, ffloat(x):
 if x!=x:
  $! '$F'
 if x==$A('$M'):
  $! USYM['$M']if OPT['uni']$( '$M'
 if x==$A('-$M'):
  $! '-'+(USYM['$M']if OPT['uni']$( '$M')
 if x==0:
  $! '0.'
 d=OPT['digits']
 s=('%.'+${(d)+'g')%x
 m=s
 ex=''
 if 'e' in s:
  m,ex=s.split('e')
  ex=$w(ex)
  ex='E'+${(ex)
 if '.' in m:
  m=m.rstrip('0')
 $(:
  m=m+'.'
 $! m+ex
$, fnum(x):
 t=$/(x)
 if t is $w:
  $! ${(x),(P_ATOM if x>=0 $( P_NEG)
 if t is $A:
  s=ffloat(x)
  $! s,(P_ATOM if $- s.$u('-')$( P_NEG)
 s=${(x[1])+'/'+${(x[2])
 $! s,(P_PROD if x[1]>0 $( P_NEG)
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
 if t is $w or t is $A:
  $! fnum(e)
 if t is ${:
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
  $! pr(e[1],$E)
 keep=$3
 if h=='$I':
  $! '{'+','.join([pr(a,keep)[0]$) a in e[1:]])+'}',P_ATOM
 if h=='mat' $* $5(e)==2:
  $! '['+','.join([pr(a,keep)[0]$) a in e[1][1:]])+']',P_ATOM
 if h=='mat':
  $n=[]
  $) r in e[1:]:
   $n.$%('['+','.join([pr(a,keep)[0]$) a in r[1:]])+']')
  $! '['+''.join($n)+']',P_ATOM
 if h=='${':
  $! '"'+e[1]+'"',P_ATOM
 if h in REL:
  op=REL[h]if OPT['uni']$( h
  a=pr(e[1],keep)
  b=pr(e[2],keep)
  $! paren(a[0],a[1],P_SUM)+op+paren(b[0],b[1],P_SUM),P_REL
 if h=='$*' $* $5(e)==3 $* head(e[1])in('<','<=')$* head(e[2])in('<','<=')$* e[1][2]==e[2][1]:
  op1=REL[e[1][0]]if OPT['uni']$( e[1][0]
  op2=REL[e[2][0]]if OPT['uni']$( e[2][0]
  $! pr(e[1][1],$3)[0]+op1+pr(e[1][2],$3)[0]+op2+pr(e[2][2],$3)[0],P_REL
 if h=='$*' or h=='or':
  p=P_AND if h=='$*' $( P_OR
  ss=[]
  $) a in e[1:]:
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
  if $5(e)==2 or e[2]==10:
   $! 'log10('+pr(e[1],keep)[0]+')',P_ATOM
  $! 'log('+pr(e[1],keep)[0]+','+pr(e[2],keep)[0]+')',P_ATOM
 if h=='call':
  $! e[1]+'('+','.join([pr(a,keep)[0]$) a in e[2:]])+')',P_ATOM
 if h=='prime':
  $! e[1]+"'"*e[2],P_ATOM
 if h=='$Z':
  nm='\u222b' if OPT['uni']$( '$Z'
  $! nm+'('+','.join([pr(a,keep)[0]$) a in e[1:]])+')',P_ATOM
 if h=='sumseq':
  nm='\u03a3' if OPT['uni']$( 'sumseq'
  $! nm+'('+','.join([pr(a,keep)[0]$) a in e[1:]])+')',P_ATOM
 if h=='prodseq':
  nm='\u03a0' if OPT['uni']$( 'prodseq'
  $! nm+'('+','.join([pr(a,keep)[0]$) a in e[1:]])+')',P_ATOM
 if h=='$V' or h=='root':
  pass
 h=TINAME.get(h,h)
 $! h+'('+','.join([pr(a,keep)[0]$) a in e[1:]])+')',P_ATOM
TINAME={'ncr':'nCr','npr':'nPr'}
MAINV='xyzt'
$, varprio(v):
 i=MAINV.find(v)if $5(v)==1 $(-1
 if i<0:
  $!(100,v)
 $!(i,v)
$, facprio(v):
 i=MAINV.find(v)if $5(v)==1 $(-1
 if i<0:
  $!(0,v)
 $!(1,${(i))
$, termdegs(t,d):
 c,r=$a(t)
 fs=r[1:]if $&(r,'*')$((r,)
 $) f in fs:
  if $/(f)is ${ $* f $- in SPECIAL:
   d[f]=d.get(f,0)+1
  $K $&(f,'^')$* $/(f[1])is ${ $* f[1]$- in SPECIAL $* $C(f[2]):
   d[f[1]]=d.get(f[1],0)+tofl(f[2])
  $K $&(f,'^')$* $C(f[2]):
   $) v in $q(f[1]):
    d[v]=d.get(v,0)+tofl(f[2])*0.001
  $K $- $C(f)$* $/(f)is $- ${:
   $) v in $q(f):
    d[v]=d.get(v,0)+0.0001
$, sumkeys($L):
 vs=[]
 degs=[]
 $) t in $L:
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
 $) k in $+($5($L)):
  t=$L[k]
  d=degs[k]
  if $C(t):
   keys.$%((2,(),0,0,(),''))
  $K $- d:
   cat=3 if has(t,'i')$( 1
   keys.$%((cat,(),0,1 if isneg(t)$( 0,(),okey($a(t)[1])))
  $(:
   keys.$%((0,$0([-d.get(v,0)$) v in mv]),-sum([d.get(v,0)$) v in ov]),
 1 if isneg(t)$( 0,$0([-d.get(v,0)$) v in ov]),okey($a(t)[1])))
 $! keys
$, pr_sum(e,keep):
 $L=$I(e[1:])
 if $- keep:
  ks=sumkeys($L)
  idx=$I($+($5($L)))
  idx.sort(key=$7 i:ks[i])
  $L=[$L[i]$) i in idx]
 $?=''
 first=$E
 $) t in $L:
  s,p=pr(t,$3)
  if p<P_SUM+1 $* $- s.$u('-')$* p<=P_SUM:
   s='('+s+')'
  if first:
   $?=s
   first=$3
  $K s.$u('-'):
   $?+=s
  $(:
   $?+='+'+s
 $! $?,P_SUM
$, fackey(f):
 if f=='pi' or f=='e' or isrrad(f)or $C(f):
  $!(0,(0,''),okey(f))
 if f=='i':
  $!(3,(0,''),'')
 if $/(f)is ${:
  $!(1,facprio(f),'')
 if $&(f,'^')$* $/(f[1])is ${:
  if f[1]=='e':
   $!(2,(0,''),okey(f))
  $!(1,facprio(f[1]),okey(f))
 if $&(f,'+')or($&(f,'^')$* $&(f[1],'+')):
  $!(4,(0,''),okey(f))
 $!(2,(0,''),okey(f))
$, pr_factor(f,keep,first):
 s,p=pr(f,keep)
 if p<P_PROD or(p==P_PROD $* $- first)or(s.$u('-')$* $- first):
  $! '('+s+')'
 $! s
''')
_x(r'''$, pr_prod(e,keep):
 fs=$I(e[1:])
 coef=1
 if fs $* $C(fs[0])$* $- keep:
  coef=fs[0]
  fs=fs[1:]
 num=[]
 den=[]
 $) f in fs:
  if $&(f,'^')$* $C(f[2])$* $_(f[2])<0:
   ex=nneg(f[2])
   den.$%(f[1]if ex==1 $(('^',f[1],ex))
  $K isq(f)$* keep:
   num.$%(f[1])
   den.$%(f[2])
  $(:
   num.$%(f)
 if $- keep:
  num.sort(key=fackey)
  den.sort(key=fackey)
 sign=''
 if keep $* num $* $C(num[0])$* $_(num[0])<0:
  sign='-'
  if num[0]==-1:
   num=num[1:]
  $(:
   num[0]=nneg(num[0])
 cn=coef
 cd=1
 if $C(coef):
  if $_(coef)<0:
   sign='-'
   coef=nneg(coef)
  if isq(coef):
   cn=coef[1]
   cd=coef[2]
  $(:
   cn=coef
 if keep:
  num=[f $) f in num if f!=1]or[1]
 if sign $* den $* $- keep:
  sums=[k $) k in $+($5(num))if $&(num[k],'+')]
  dsums=[k $) k in $+($5(den))if $&(den[k],'+')]
  if $5(sums)==1 $* any([isneg(t)$) t in num[sums[0]][1:]]):
   num=$I(num)
   num[sums[0]]=$:(-1,num[sums[0]])
   sign=''
  $K $5(dsums)==1 $* $- sums $* $5(den[dsums[0]])==3 $* $2(den[dsums[0]])$* any([isneg(t)$) t in den[dsums[0]][1:]]):
   den=$I(den)
   den[dsums[0]]=$:(-1,den[dsums[0]])
   sign=''
 $y=[]
 if cn!=1 or $/(cn)is $A:
  $y.$%(fnum(cn)[0])
 $) f in num:
  $y.$%(pr_factor(f,$3,$- $y))
 if $- $y:
  $y.$%('1')
 ns='*'.join($y)
 if cd!=1:
  den.insert(0,cd)
 if $- den:
  if sign $* $5(num)==1 $* cn==1 $* pr(num[0],$3)[1]<=P_SUM:
   $! sign+'('+pr(num[0],$3)[0]+')',P_NEG
  $! sign+ns,(P_NEG if sign $( P_PROD)
 if $5($y)==1 $* $5(num)==1 $* cn==1:
  s,p=pr(num[0],$3)
  ns=paren(s,p,P_PROD+1)if p<P_PROD $( s
  if s.$u('-'):
   ns='('+s+')'
 dparts=[]
 $) f in den:
  dparts.$%(pr_factor(f,$3,$- dparts))
 ds='*'.join(dparts)
 if $5(den)>1:
  ds='('+ds+')'
 $(:
  s,p=pr(den[0],$3)
  if p<=P_PROD or s.$u('-'):
   ds='('+s+')'
 $! sign+ns+'/'+ds,(P_NEG if sign $( P_PROD)
$, pr_pow(e,keep):
 b=e[1]
 x=e[2]
 if $C(x)$* $_(x)<0 $* $- keep:
  ex=nneg(x)
  d=b if ex==1 $(('^',b,ex)
  s,p=pr(d,$3)
  if p<=P_PROD or s.$u('-'):
   s='('+s+')'
  $! '1/'+s,P_PROD
 if x==$s:
  s,p=pr(b,$3)
  if OPT['uni']:
   if($/(b)is $w $* b>=0)or($/(b)is ${):
    $! '\u221a'+s,P_POW
   $! '\u221a('+s+')',P_ATOM
  $! '$V('+s+')',P_ATOM
 bs,bp=pr(b,$3)
 if bp<=P_POW or bs.$u('-')or $&(b,'fact'):
  bs='('+bs+')'
 xs,xp=pr(x,$3)
 if $-(($/(x)is $w $* x>=0)or($/(x)is ${)):
  xs='('+xs+')'
 $! bs+'^'+xs,P_POW
$, fmt_top(e):
 if $&(e,'mat')$* $5(e)>2:
  $n=[]
  $) r in e[1:]:
   $n.$%('['+','.join([fmt(a)$) a in r[1:]])+']')
  if sum([$5(r)$) r in $n])>28:
   $! '['+('\n '.join($n))+']'
  $! '['+''.join($n)+']'
 if $&(e,'${'):
  $! e[1]
 $! fmt(e)
''')
_x(r'''REPL=(
 ('**','^'),('==','='),('!=','/='),
 ('sin\u207b\u00b9','$~'),('cos\u207b\u00b9','arccos'),('tan\u207b\u00b9','$x'),
 ('\u2212','-'),('\u2013','-'),('\u00d7','*'),('\u00b7','*'),
 ('\u2022','*'),('\u22c5','*'),('\u00f7','/'),('\u2264','<='),
 ('\u2265','>='),('\u2260','/='),('\u2192','->'),('\u21d2','=>'),
 ('\u21d4','<=>'),('\u207b\u00b9','^(-1)'),('\u00b2','^2'),
 ('\u00b3','^3'),('\u03c0',' pi '),('\u221e',' $M '),
 ('\u212f',' e '),('\u2148',' i '),('\u03b8','theta'),
 ('\u222b',' $Z'),('\u03a3',' sumseq'),('\u2211',' sumseq'),
 ('\u03a0',' prodseq'),('\u220f',' prodseq'),('\u1d07','E'),
 ('\u2032',"'"),('\u2033',"''"),('@i',' i '),('@e',' e '),
 ('@>','\u25ba'),('@d','\u00b0'),('@t','\u1d40'),('\u2044','/'),
 ('infinity','$M'),('\u03b1','alpha'),('\u03b2','beta'),
 ('\u03bb','$7'),('\u03bc','mu'),('\u03c3','sigma'),
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
  $! $E
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
 n=$5(s)
 $J i<n:
  c=s[i]
  if c==' ' or c=='\t':
   i+=1
   $8
  if c=='0' $* i+2<n $* s[i+1]in 'bBhH':
   base=2 if s[i+1]in 'bB' $( 16
   j=i+2
   dg='01' if base==2 $( '0123456789abcdefABCDEF'
   $J j<n $* s[j]in dg:
    j+=1
   if j>i+2:
    toks.$%(('num',$w(s[i+2:j],base)))
    i=j
    $8
  if isdig(c)or(c=='.' $* i+1<n $* isdig(s[i+1])):
   j=i
   $J j<n $* isdig(s[j]):
    j+=1
   isf=$3
   if j<n $* s[j]=='.' $* $-(j+1<n $* s[j+1]in '^*/+-' $* $- isdig(s[j+1])):
    isf=$E
    j+=1
    $J j<n $* isdig(s[j]):
     j+=1
   if j<n $*(s[j]=='E' or(s[j]=='e' $* j+1<n $* isdig(s[j+1]))):
    k=j+1
    if k<n $* s[k]in '+-':
     k+=1
    if k<n $* isdig(s[k]):
     isf=$E
     j=k
     $J j<n $* isdig(s[j]):
      j+=1
   txt=s[i:j]
   if isf:
    toks.$%(('num',$A(txt)))
   $(:
    toks.$%(('num',$w(txt)))
   i=j
   $8
  if isletter(c):
   j=i
   $J j<n $*(isletter(s[j])or isdig(s[j])):
    j+=1
   $B=s[i:j].lower()
   toks.$%(('id',$B))
   i=j
   k=0
   $J i<n $* s[i]=="'":
    k+=1
    i+=1
   if k:
    toks.$%(('prime',k))
   $8
  if c=='"':
   j=s.find('"',i+1)
   if j<0:
    $l $R('Missing "')
   toks.$%(('${',s[i+1:j]))
   i=j+1
   $8
  $) op in OPS:
   if s.$u(op,i):
    i+=$5(op)
    if op=='<>':
     op='/='
    if op=='>>':
     op='\u25ba'
    toks.$%(('op',op))
    $T
  $(:
   $l $R('Invalid character: '+c)
 toks.$%(('end',$#))
 $! toks
''')
_x(r'''class Parser:
 $, __init__($=,toks,isfunc):
  $=.t=toks
  $=.i=0
  $=.isfunc=isfunc
 $, peek($=):
  $! $=.t[$=.i]
 $, nxt($=):
  tk=$=.t[$=.i]
  $=.i+=1
  $! tk
 $, isop($=,op):
  tk=$=.t[$=.i]
  $! tk[0]=='op' $* tk[1]==op
 $, isid($=,$B):
  tk=$=.t[$=.i]
  $! tk[0]=='id' $* tk[1]==$B
 $, expect($=,op):
  if $- $=.isop(op):
   tk=$=.peek()
   $l $R('Missing '+op)
  $=.i+=1
 $, top($=):
  e=$=.store()
  $J $=.isop('\u25ba'):
   $=.nxt()
   tk=$=.nxt()
   if tk[0]!='id':
    $l $R('Syntax error after conversion')
   $Y=[]
   if $=.isop('('):
    $=.nxt()
    $Y=$=.$Y(')')
   e=('conv',e,tk[1])+$0($Y)
  if $=.peek()[0]!='end':
   tk=$=.peek()
   $l $R('Syntax error near '+${(tk[1])if tk[1]is $- $# $( 'Syntax error')
  $! e
 $, store($=):
  if $=.isid('define'):
   $=.nxt()
   lhs=$=.sum()
   if $- $=.isop('='):
    $l $R('Define needs =')
   $=.nxt()
   rhs=$=.wth()
   $!('define',lhs,rhs)
  e=$=.wth()
  if $=.isop('->')or $=.isop('=:'):
   $=.nxt()
   tgt=$=.wth()
   $!('store',e,tgt)
  if $=.isop(':='):
   $=.nxt()
   rhs=$=.wth()
   $!('define',e,rhs)
  $! e
 $, wth($=):
  e=$=.iff()
  $J $=.isop('|'):
   $=.nxt()
   c=$=.iff()
   e=('|',e,c)
  $! e
 $, iff($=):
  e=$=.imp()
  $J $=.isop('<=>'):
   $=.nxt()
   e=('<=>',e,$=.imp())
  $! e
 $, imp($=):
  e=$=.xor()
  $J $=.isop('=>'):
   $=.nxt()
   e=('=>',e,$=.xor())
  $! e
 $, xor($=):
  e=$=.lor()
  $J $=.isid('xor')or $=.isid('nor')or $=.isid('nand'):
   op=$=.nxt()[1]
   e=(op,e,$=.lor())
  $! e
 $, lor($=):
  e=$=.land()
  $J $=.isid('or'):
   $=.nxt()
   e=('or',e,$=.land())
  $! e
 $, land($=):
  e=$=.lnot()
  $J $=.isid('$*'):
   $=.nxt()
   e=('$*',e,$=.lnot())
  $! e
 $, lnot($=):
  if $=.isid('$-'):
   $=.nxt()
   $!('$-',$=.lnot())
  $! $=.rel()
 $, rel($=):
  a=$=.sum()
  tk=$=.peek()
  if tk[0]=='op' $* tk[1]in('=','/=','<','>','<=','>='):
   $=.nxt()
   b=$=.sum()
   r=(tk[1],a,b)
   tk2=$=.peek()
   if tk2[0]=='op' $* tk2[1]in('<','>','<=','>='):
    $=.nxt()
    c=$=.sum()
    r=('$*',r,(tk2[1],b,c))
   $! r
  $! a
 $, sum($=):
  a=$=.prod()
  $J $E:
   tk=$=.peek()
   if tk[0]=='op' $* tk[1]in('+','-','.+','.-','&'):
    $=.nxt()
    b=$=.prod()
    op=tk[1]
    if op=='.+':
     op='+'
    $K op=='.-':
     op='-'
    a=(op,a,b)
   $(:
    $! a
 $, startsprimary($=):
  tk=$=.peek()
  if tk[0]=='num' or tk[0]=='${':
   $! $E
  if tk[0]=='id':
   $! tk[1]$- in KEYW
  if tk[0]=='op':
   $! tk[1]in('(','{','\u221a')
  $! $3
 $, prod($=):
  a=$=.unary()
  $J $E:
   tk=$=.peek()
   if tk[0]=='op' $* tk[1]in('*','/','.*','./'):
    $=.nxt()
    b=$=.unary()
    op=tk[1]
    a=(op,a,b)
   $K $=.startsprimary():
    b=$=.pw()
    a=('*',a,b)
   $(:
    $! a
 $, unary($=):
  if $=.isop('-'):
   $=.nxt()
   $!('$k',$=.unary())
  if $=.isop('+'):
   $=.nxt()
   $! $=.unary()
  $! $=.pw()
 $, pw($=):
  b=$=.post()
  if $=.isop('^')or $=.isop('.^'):
   op=$=.nxt()[1]
   if $=.isop('\u1d40')or $=.isid('t')$* $3:
    pass
   x=$=.unary()
   $!('^' if op=='^' $( '.^',b,x)
  $! b
 $, post($=):
  a=$=.primary()
  $J $E:
   if $=.isop('!'):
    $=.nxt()
    a=('!',a)
   $K $=.isop('%'):
    $=.nxt()
    a=('%',a)
   $K $=.isop('\u00b0'):
    $=.nxt()
    a=('deg',a)
   $K $=.isop('\u1d40'):
    $=.nxt()
    a=('call','transpose',a)
   $K $=.isop('['):
    $=.nxt()
    idx=$=.$Y(']')
    a=('index',a)+$0(idx)
   $(:
    $! a
 $, $Y($=,close):
  $?=[]
  if $=.isop(close):
   $=.nxt()
   $! $?
  $J $E:
   $?.$%($=.store_in())
   if $=.isop(','):
    $=.nxt()
    $8
   $=.expect(close)
   $! $?
 $, store_in($=):
  e=$=.wth()
  $! e
 $, primary($=):
  tk=$=.nxt()
  k=tk[0]
  if k=='num':
   $! tk[1]
  if k=='${':
   $!('${',tk[1])
  if k=='id':
   $B=tk[1]
   if $B in KEYW:
    $l $R('Syntax error: '+$B)
   if $=.peek()[0]=='prime':
    n=$=.nxt()[1]
    if $=.isop('('):
     $=.nxt()
     a=$=.$Y(')')
     $!('primecall',$B,n)+$0(a)
    $!('prime',$B,n)
   if $=.isop('(')$*($=.isfunc($B)or($5($B)>1 $* $B $- in('pi','$M','$F','theta'))):
    $=.nxt()
    a=$=.$Y(')')
    $!('call',$B)+$0(a)
   $! $B
  if k=='op':
   op=tk[1]
   if op=='(':
    e=$=.store_in()
    if $=.isop('\u2220'):
     $=.nxt()
     th=$=.store_in()
     $=.expect(')')
     $!('polar',e,th)
    $=.expect(')')
    $! e
   if op=='{':
    $!('$I',)+$0($=.$Y('}'))
   if op=='[':
    $! $=.matrix()
   if op=='\u221a':
    $!('call','$V',$=.post())
   if op=='-':
    $!('$k',$=.pw())
  if k=='end':
   $l $R('Incomplete expression')
  $l $R('Syntax error near '+${(tk[1]))
 $, matrix($=):
  $n=[]
  if $=.isop('['):
   $J $=.isop('['):
    $=.nxt()
    $n.$%(('$I',)+$0($=.$Y(']')))
    if $=.isop(','):
     $=.nxt()
   $=.expect(']')
  $(:
   row=[]
   $J $E:
    if $=.isop(']'):
     $=.nxt()
     $T
    row.$%($=.store_in())
    if $=.isop(','):
     $=.nxt()
    $K $=.isop(';'):
     $=.nxt()
     $n.$%(('$I',)+$0(row))
     row=[]
    $K $=.isop(']'):
     $8
    $(:
     $l $R('Missing ]')
   $n.$%(('$I',)+$0(row))
  n=$5($n[0])
  $) r in $n:
   if $5(r)!=n:
    $l $R('Dimension error')
  $!('mat',)+$0($n)
''')
_x(r'''$, parse(s,isfunc):
 toks=tokenize(s)
 if toks[0][0]=='end':
  $l $R('Empty input')
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
  $K m in C:
   del C[m]
 $! C
$, p_neg(A):
 $! dict([(m,-A[m])$) m in A])
$, p_sub(A,B):
 $! p_add(A,p_neg(B))
$, madd(a,b):
 $! $0([a[i]+b[i]$) i in $+($5(a))])
$, p_mul(A,B):
 C={}
 $) a in A:
  ca=A[a]
  $) b in B:
   m=madd(a,b)
   v=C.get(m,0)+ca*B[b]
   if v:
    C[m]=v
   $K m in C:
    del C[m]
 $! C
$, p_scale(A,c):
 if c==0:
  $!{}
 $! dict([(m,A[m]*c)$) m in A])
$, p_pow(A,n):
 nv=$5(next(iter(A)))if A $( 0
 R=p_const(1,nv)
 $J n>0:
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
  $! $E
 $) m in A:
  if sum(m):
   $! $3
 $! $E
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
$, $P(A,B):
 if $- B:
  err("Division by zero")
 lmB=max(B)
 lcB=B[lmB]
 nv=$5(lmB)
 Qt={}
 R=dict(A)
 cnt=0
 $J R:
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
   $K mm in R:
    del R[mm]
 $! Qt
$, p_icont(A):
 g=0
 $) m in A:
  g=igcd(g,A[m])
  if g==1:
   $T
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
  if p_isconst(g)$* $H(p_cval(g))==1:
   $! p_const(1,nv)
 $! p_normsign(g)
EVP=(3,5,7,11,13,17,19,23,29,31,37,41)
$, p_at(A,pt):
 s=0
 $) m in A:
  t=A[m]
  $) i in $+($5(m)):
   if m[i]:
    t*=pt[i]**m[i]
  s+=t
 $! s
$, p_gcd(A,B,nv):
 if $- A:
  $! p_normsign(B)
 if $- B:
  $! p_normsign(A)
 if nv $*($5(A)>2 or $5(B)>2):
  c=igcd(p_icont(A),p_icont(B))
  ok=$E
  $) sh in(0,1):
   pt=[EVP[(i+sh*5)%$5(EVP)]*(1+sh)+i $) i in $+(nv)]
   g=igcd(p_at(A,pt),p_at(B,pt))
   if g!=c:
    ok=$3
    $T
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
 pA=$P(A,cA)
 pB=$P(B,cB)
 if p_deg(pA,k)<p_deg(pB,k):
  pA,pB=pB,pA
 $J pB $* p_deg(pB,k)>0:
  r=prem(pA,pB,k,nv)
  pA=pB
  if $- r:
   pB={}
   $T
  pB=$P(r,p_cont(r,k,nv))
 if pB:
  g=p_const(1,nv)
 $(:
  g=$P(pA,p_cont(pA,k,nv))
 $! p_normsign(p_mul(c,g))
$, prem(A,B,k,nv):
 dB=p_deg(B,k)
 lcB=p_lc(B,k)
 R=A
 $J R $* p_deg(R,k)>=dB:
  dR=p_deg(R,k)
  lcR=p_lc(R,k)
  t=p_mul(lcR,{p_mono(nv,k,dR-dB):1})
  R=p_sub(p_mul(R,lcB),p_mul(t,B))
 $! R
$, p_sqfree(P,k,nv):
 dP=p_diff(P,k)
 a=p_gcd(P,dP,nv)
 b=$P(P,a)
 c=$P(dP,a)
 d=p_sub(c,p_diff(b,k))
 res=[]
 i=1
 $J p_deg(b,k)>0:
  a=p_gcd(b,d,nv)
  if p_deg(a,k)>0:
   res.$%((a,i))
  b=$P(b,a)
  c=$P(d,a)
  d=p_sub(c,p_diff(b,k))
  i+=1
  if i>200:
   $T
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
 nv=$5(lm)
 $) _ in $+($5(D)+3):
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
 if $/(x)is $w:
  $! b,x
 if isq(x):
  $! pw(b,Q(1,x[2])),x[1]
 c,r=$a(x)
 if $/(c)is $w $* c!=1:
  $! pw(b,r),c
 if isq(c):
  $! pw(b,$:(Q(1,c[2]),r)),c[1]
 $! e,1
$, kernels(e,ks):
 t=$/(e)
 if t is $w or t is $A:
  $!
 if t is ${:
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
  if $/(e[2])is $w:
   kernels(e[1],ks)
   $!
  k,n=splitpow(e)
  if k==e or $- $&(k,'^')or $E:
   if $&(k,'^')$* $/(k[2])is $w:
    kernels(k,ks)
    $!
   if k $- in ks:
    ks.$%(k)
  $!
 if e $- in ks:
  ks.$%(e)
$, sortkernels(ks):
 ks.sort(key=$7 k:varprio(k)if $/(k)is ${ $((200,okey(k)))
 $! ks
''')
_x(r'''$, ratform(e,ks):
 nv=$5(ks)
 t=$/(e)
 if t is $w:
  $! p_const(e,nv),p_const(1,nv)
 if t is $A:
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
   $(:
    g=p_gcd(D,d,nv)
    d1=$P(d,g)
    D1=$P(D,g)
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
  if $/(e[2])is $w:
   b=e[1]
   n=e[2]
  $(:
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
 $L=[]
 $) m in P:
  fs=[P[m]]
  $) i in $+($5(m)):
   if m[i]:
    fs.$%(pw(ks[i],m[i]))
  $L.$%($G(fs))
 $! $;($L)
$, cancel_pair(N,D,nv):
 g=p_gcd(N,D,nv)
 if $- p_isconst(g)or p_cval(g)!=1:
  N=$P(N,g)
  D=$P(D,g)
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
 N,D=cancel_pair(r[0],r[1],$5(ks))
 $! N,D,ks
$, comdenom(e):
 if $&(e,'$I')or $&(e,'mat'):
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
 if $&(num,'+')$* $&(den,'+')or den==1 or $C(den):
  $! $O(num,den)
 $! $O(num,den)
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
 if $&(e,'^')$* $C(e[2])$* $_(e[2])<0 $* $- $2(e[1]):
  $! $E
 if $/(e)is $0 $* e[0]in('+','*'):
  $) a in e[1:]:
   if hasdenom(a):
    $! $E
 $! $3
$, $.(e):
 t=$/(e)
 if t is $- $0 or e[0]=='Q' or e[0]=='${':
  $! e
 h=e[0]
 $Y=[$.(a)$) a in e[1:]]
 e2=simp((h,)+$0($Y))if h!='hold' $( e
 if $- $&(e2,'*'):
  $! e2
 hasden=$3
 hassum=$3
 $) f in e2[1:]:
  if $&(f,'^')$* $C(f[2])$* $_(f[2])<0 $* $- $2(f[1]):
   if $&(f[1],'+')or($&(f[1],'^')$* $&(f[1][1],'+')):
    hasden=$E
  if $&(f,'+')or($&(f,'^')$* $&(f[1],'+')):
   hassum=$E
 if $-(hasden $* hassum)$* $- hasden:
  $! e2
 if $^(e2):
  $! e2
 ks=[]
 kernels(e2,ks)
 sortkernels(ks)
 nv=$5(ks)
 if nv==0 or nv>6:
  $! e2
 nums=[]
 dens=[]
 $) f in e2[1:]:
  if $&(f,'^')$* $C(f[2])$* $_(f[2])<0:
   dens.$%(pw(f[1],nneg(f[2])))
  $(:
   nums.$%(f)
 num=$G(nums)
 den=$G(dens)
 rn=ratform(num,ks)
 rd=ratform(den,ks)
 if rn is $# or rd is $#:
  $! e2
 if $5(rn[0])*$5(rd[1])>400 or $5(rn[1])*$5(rd[0])>400:
  $! e2
 N=p_mul(rn[0],rd[1])
 D=p_mul(rn[1],rd[0])
 if $5(N)>80 or $5(D)>80 or p_tdeg(N)>30 or p_tdeg(D)>30:
  $! e2
 g=p_gcd(N,D,nv)
 if p_isconst(g):
  $! e2
 N=$P(N,g)
 D=$P(D,g)
 if D $* D[max(D)]<0:
  N=p_neg(N)
  D=p_neg(D)
 $! $O(p2e(N,ks),p2e(D,ks))
$, u_trim(a):
 a=$I(a)
 $J a $* a[-1]==0:
  a.pop()
 $! a
$, u_add(a,b):
 n=max($5(a),$5(b))
 $! u_trim([nadd(a[i]if i<$5(a)$( 0,b[i]if i<$5(b)$( 0)$) i in $+(n)])
$, u_neg(a):
 $![nneg(c)$) c in a]
$, u_sub(a,b):
 $! u_add(a,u_neg(b))
$, u_mul(a,b):
 if $- a or $- b:
  $![]
 r=[0]*($5(a)+$5(b)-1)
 $) i in $+($5(a)):
  if a[i]==0:
   $8
  $) j in $+($5(b)):
   r[i+j]=nadd(r[i+j],nmul(a[i],b[j]))
 $! u_trim(r)
$, u_scale(a,c):
 $! u_trim([nmul(x,c)$) x in a])
$, u_divmod(a,b):
 b=u_trim(b)
 if $- b:
  err("Division by zero")
 a=u_trim(a)
 q=[0]*max($5(a)-$5(b)+1,0)
 r=$I(a)
 lb=b[-1]
 $J $5(r)>=$5(b)$* r:
  c=ndiv(r[-1],lb)
  k=$5(r)-$5(b)
  q[k]=c
  $) j in $+($5(b)):
   r[k+j]=nsub(r[k+j],nmul(c,b[j]))
  r=u_trim(r[:-1])if r[-1]==0 or $E $( r
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
 $J r1:
  q,r=u_divmod(r0,r1)
  r0,r1=r1,r
  s0,s1=s1,u_sub(s0,u_mul(q,s1))
  t0,t1=t1,u_sub(t0,u_mul(q,t1))
 if $- r0:
  $! r0,s0,t0
 c=ninv(r0[-1])
 $! u_scale(r0,c),u_scale(s0,c),u_scale(t0,c)
$, u_toexpr(a,x):
 $! $;([$:(a[i],pw(x,i))$) i in $+($5(a))if a[i]!=0])
$, u_from_expr(e,x):
 cs=$X(e,x)
 if cs is $#:
  $! $#
 $) c in cs:
  if $- $r(c):
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
 a=$I(a)
 if $5(a)<$5(b):
  $! $#
 q=[0]*($5(a)-$5(b)+1)
 lb=b[-1]
 $) k in $+($5(a)-$5(b),-1,-1):
  c=a[k+$5(b)-1]
  if c%lb:
   $! $#
  c//=lb
  q[k]=c
  if c:
   $) j in $+($5(b)):
    a[k+j]-=c*b[j]
 $) x in a:
  if x:
   $! $#
 $! q
''')
_x(r'''$, aberth(c):
 c=[$1(tofl(x))if $/(x)is $- $1 $( x $) x in c]
 $J c $* c[-1]==0:
  c.pop()
 n=$5(c)-1
 if n<1:
  $![]
 zeros=0
 $J $H(c[0])==0:
  c.pop(0)
  zeros+=1
  n-=1
 $?=[0j]*zeros
 if n<1:
  $! $?
 if n==1:
  $! $?+[-c[0]/c[1]]
 a=[x/c[-1]$) x in c]
 r=0.0
 $) i in $+(n):
  v=$H(a[i])**(1.0/(n-i))
  if v>r:
   r=v
 r=max(r,1e-3)
 z=[r*cmath.exp(1j*(2*$W.pi*k/n+0.4))$) k in $+(n)]
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
    $8
   ratio=p/dp if dp!=0 $( 1e-3
   s=0j
   $) j in $+(n):
    if j!=k:
     d=zk-z[j]
     if d!=0:
      s+=1/d
   den=1-ratio*s
   w=ratio/den if den!=0 $( ratio
   z[k]=zk-w
   aw=$H(w)
   if aw>mx*(1+$H(zk))or $E:
    mx=max(mx,aw/(1+$H(zk)))
  if mx<1e-15:
   $T
 res=[]
 $) zk in z:
  $) _ in $+(3):
   p=c[n]
   dp=0j
   $) j in $+(n-1,-1,-1):
    dp=dp*zk+p
    p=p*zk+c[j]
   if dp==0:
    $T
   zk=zk-p/dp
  res.$%(zk)
 $! $?+res
$, divisors_int(n,$v=400):
 n=$H(n)
 if n==0:
  $![1]
 fs,$d=factor_int_small(n)
 if $d>1:
  fs.$%(($d,1))
 ds=[1]
 $) p,k in fs:
  nd_=[]
  $) d in ds:
   v=d
   $) _ in $+(k+1):
    nd_.$%(v)
    v*=p
  ds=nd_
  if $5(ds)>$v:
   $! $#
 ds.sort()
 $! ds
$, combos(n,k):
 idx=$I($+(k))
 $J $E:
  yield idx
  i=k-1
  $J i>=0 $* idx[i]==i+n-k:
   i-=1
  if i<0:
   $!
  idx[i]+=1
  $) j in $+(i+1,k):
   idx[j]=idx[j-1]+1
$, ifactor_sqf(f):
 n=$5(f)-1
 if n<=1:
  $![f]
 res=[]
 $J f[0]==0:
  res.$%([0,1])
  f=f[1:]
 if $5(f)-1<=1:
  $! res+[f]if $5(f)>1 $( res
 roots=aberth(f)
 lcd=divisors_int(f[-1])or[1]
 $d=[]
 $) r in roots:
  found=$3
  if $H(r.imag)<1e-6*(1+$H(r.$N)):
   $) q in lcd:
    p=$w(round(r.$N*q))
    if p==0 $* $H(r.$N)>0.5/q:
     $8
    g=[-p,q]
    if igcd(p,q)!=1:
     $8
    qq=i_divexact(f,g)
    if qq is $- $#:
     res.$%(g)
     f=qq
     found=$E
     $T
  if $- found:
   $d.$%(r)
 if $5(f)-1<=3:
  if $5(f)>1:
   res.$%(f)
  $! res
 roots=$d
 if $5(roots)!=$5(f)-1:
  roots=aberth(f)
 lcd=divisors_int(f[-1])or[1]
 d=2
 $J d<=($5(f)-1)//2 $* $5(roots)<=24:
  done=$3
  $) idx in combos($5(roots),d):
   pc=[1+0j]
   $) i in idx:
    r=roots[i]
    nw=[0j]*($5(pc)+1)
    $) j in $+($5(pc)):
     nw[j+1]+=pc[j]
     nw[j]-=pc[j]*r
    pc=nw
   ok=$E
   $) v in pc:
    if $H(v.imag)>1e-6*(1+$H(v.$N)):
     ok=$3
     $T
   if $- ok:
    $8
   $) q in lcd:
    g=[]
    good=$E
    $) v in pc:
     x=v.$N*q
     ix=$w(round(x))
     if $H(x-ix)>1e-5*(1+$H(x)):
      good=$3
      $T
     g.$%(ix)
    if $- good:
     $8
    qq=i_divexact(f,g)
    if qq is $- $#:
     res.$%(g)
     f=qq
     roots=[roots[i]$) i in $+($5(roots))if i $- in idx]
     done=$E
     $T
   if done:
    $T
  if $- done:
   d+=1
 if $5(f)>1:
  res.$%(f)
 $! res
$, ufactor(a):
 ints,c=u_toint(u_trim(a))
 if $5(ints)<=1:
  $! nmul(c,ints[0]if ints $( 0),[]
 nv=1
 P=dict([((i,),ints[i])$) i in $+($5(ints))if ints[i]])
 $?=[]
 mn=min([m[0]$) m in P])
 if mn>0:
  $?.$%(([0,1],mn))
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
    $?.$%((g,i))
 $(:
  c=nmul(c,p_cval(P))
 $! c,$?
$, i2p(f,nv,k):
 $! dict([(p_mono(nv,k,i),f[i])$) i in $+($5(f))if f[i]])
$, mfactor(P,nv):
 if $- P:
  $! 0,[]
 c=p_icont(P)
 if P[max(P)]<0:
  c=-c
 P=p_scale(P,1)if c==1 $( dict([(m,P[m]//c)$) m in P])
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
  $! p_cval(P)**mult if P $( 0
 if $5(vs)==1:
  k=vs[0]
  fl=[0]*(p_deg(P,k)+1)
  $) m in P:
   fl[m[k]]=P[m]
  cc,fs=ufactor(fl)
  $) g,i in fs:
   res.$%((i2p(g,nv,k),i*mult))
  $! cc**mult if $/(cc)is $w $( nipow(cc,mult)
 vs.sort(key=$7 k:p_deg(P,k))
 k=vs[0]
 cst=1
 C=p_cont(P,k,nv)
 if $- p_isconst(C):
  cst=mfac_rec(C,nv,res,mult)
  P=$P(P,C)
 $K p_cval(C)!=1:
  P=$P(P,C)
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
  $K s!=d:
   $! $3
 $! $E
''')
_x(r'''$, msplit(F,nv,$<):
 vs=p_vars(F,nv)
 if $5(vs)<=1:
  if $- vs:
   $![F]
  k=vs[0]
  fl=[0]*(p_deg(F,k)+1)
  $) m in F:
   fl[m[k]]=F[m]
  cc,fs=ufactor(fl)
  $?=[]
  $) g,i in fs:
   $) _ in $+(i):
    $?.$%(i2p(g,nv,k))
  $! $? if $? $([F]
 if $<>8:
  $![F]
 $) k in vs:
  if p_deg(F,k)==1:
   pass
 if $5(vs)==2 $* ishomog(F):
  a,b=vs
  fl=[0]*(p_deg(F,a)+1)
  $) m in F:
   fl[m[a]]=F[m]
  cc,fs=ufactor(fl)
  if $5(fs)>1 or(fs $* fs[0][1]>1):
   $?=[]
   $) g,i in fs:
    d=$5(g)-1
    G={}
    $) j in $+($5(g)):
     if g[j]:
      m=[0]*nv
      m[a]=j
      m[b]=d-j
      G[$0(m)]=g[j]
    $) _ in $+(i):
     $?.$%(G)
   $! $?
  $![F]
 $) k in vs:
  if p_deg(F,k)==2:
   A=p_coeff(F,k,2)
   B=p_coeff(F,k,1)
   C=p_coeff(F,k,0)
   D=p_sub(p_mul(B,B),p_scale(p_mul(A,C),4))
   S=p_sqrt(D)if D $({}
   if S is $- $# $* S:
    x={p_mono(nv,k,1):1}
    base=p_add(p_mul(p_scale(A,2),x),B)
    G1=p_sub(base,S)
    G2=p_add(base,S)
    G1=$P(G1,p_mul(p_cont(G1,k,nv),p_const(p_icont($P(G1,p_cont(G1,k,nv))),nv)))
    G2=$P(G2,p_mul(p_cont(G2,k,nv),p_const(p_icont($P(G2,p_cont(G2,k,nv))),nv)))
    if G1 $* G2:
     $! msplit(G1,nv,$<+1)+msplit(G2,nv,$<+1)
 $) k in vs:
  if p_deg(F,k)<2:
   $8
  lc=p_lc(F,k)
  tc=p_coeff(F,k,0)
  da=pdivisors(lc,nv)
  db=pdivisors(tc,nv)
  if da is $# or db is $# or $5(da)*$5(db)>3000:
   $8
  x={p_mono(nv,k,1):1}
  $) a in da:
   ax=p_mul(a,x)
   $) b in db:
    $) s in(1,-1):
     G=p_add(ax,p_scale(b,s))
     Qt=$P(F,G)
     if Qt is $- $#:
      $![G]+msplit(Qt,nv,$<+1)
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
  if $5(ds)>300:
   $! $#
 $! ds
$, factor_int_full(n):
 fs={}
 if n<0:
  n=-n
 st=[n]
 $J st:
  m=st.pop()
  if m==1:
   $8
  small,m=factor_int_small(m)
  $) p,k in small:
   fs[p]=fs.get(p,0)+k
  if m==1:
   $8
  if m>>1024:
   err('Number too large to factor')
  if isprime(m):
   fs[m]=fs.get(m,0)+1
   $8
  d=rho(m)
  st.$%(d)
  st.$%(m//d)
 ks=sorted(fs)
 $![(p,fs[p])$) p in ks]
$, powmod(b,e,m):
 r=1
 b%=m
 $J e>0:
  if e&1:
   r=r*b%m
  e>>=1
  b=b*b%m
 $! r
$, isprime(n):
 if n<2:
  $! $3
 $) p in(2,3,5,7,11,13,17,19,23,29,31,37):
  if n%p==0:
   $! n==p
 d=n-1
 s=0
 $J d%2==0:
  d//=2
  s+=1
 $) a in(2,3,5,7,11,13,17,19,23,29,31,37):
  x=powmod(a,d,n)
  if x==1 or x==n-1:
   $8
  $) _ in $+(s-1):
   x=x*x%n
   if x==n-1:
    $T
  $(:
   $! $3
 $! $E
$, rho(n):
 if n%2==0:
  $! 2
 r=iroot(n,2)
 if r*r==n:
  $! r
 c=1
 $J $E:
  x=2
  y=2
  d=1
  cnt=0
  $J d==1:
   x=(x*x+c)%n
   y=(y*y+c)%n
   y=(y*y+c)%n
   d=igcd($H(x-y),n)
   cnt+=1
   if cnt>10000:
    $T
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
  fs.$%(p if k==1 $(('^',p,k))
 $) p,k in factor_int_full(d):
  fs.$%(('^',p,-k))
 if $- fs:
  $! 1
 if $5(fs)==1 $* fs[0]==-1:
  $!-1
 if $5(fs)==1:
  $!('hold',fs[0])
 $!('hold',('*',)+$0(fs))
$, factor_expr(e,var=$#,$@=$3):
 if $r(e):
  $! factor_rat_held(e)
 if $&(e,'$I')or $&(e,'mat'):
  $! mapexpr($7 a:factor_expr(a,var,$@),e)
 if isrel(e):
  $!(e[0],factor_expr(e[1],var,$@),factor_expr(e[2],var,$@))
 if $^(e):
  $! e
 ks=[]
 kernels(e,ks)
 sortkernels(ks)
 nv=$5(ks)
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
  nfac.extend(split_radical(p2e(g,ks),m,var,$@))
 dfac=[]
 $) g,m in fd:
  dfac.extend(split_radical(p2e(g,ks),m,var,$@))
 items=[]
 $) f,m in nfac:
  if $C(f):
   const=nmul(const,nipow(f,m))
  $(:
   items.$%((f,m))
 ditems=[]
 $) f,m in dfac:
  if $C(f):
   const=ndiv(const,nipow(f,m))
  $(:
   ditems.$%((f,m))
 items.sort(key=$7 fm:fsortkey(fm[0]))
 ditems.sort(key=$7 fm:fsortkey(fm[0]))
 $?=[]
 if const!=1 or($- items $* $- ditems):
  $?.$%(const)
 $) f,m in items:
  $?.$%(f if m==1 $(('^',f,m))
 $) f,m in ditems:
  $?.$%(('^',f,-m))
 if $5($?)==1:
  if $&($?[0],'^')or $C($?[0]):
   $!('hold',$?[0])if $- $C($?[0])$( $?[0]
  $! $?[0]
 $!('hold',('*',)+$0($?))
$, fsortkey(f):
 ss=$q(f)
 ss.sort(key=varprio)
 d=0
 if ss:
  d=degree(f,ss[0])
  if d is $#:
   d=99
 $!($5(ss),okey(ss),d,okey(f))
$, split_radical(f,m,var,$@):
 if var is $# $* $- $@:
  $![(f,m)]
 vs=$q(f)
 if var is $#:
  if $5(vs)!=1:
   $![(f,m)]
  x=vs[0]
 $(:
  x=var
 cs=$X(f,x)
 if cs is $# or $5(cs)!=3:
  if cs is $- $# $* $5(cs)==2 $* $@:
   $![(f,m)]
  $![(f,m)]
 c,b,a=cs
 D=$>($[($:(b,b),$:(4,a,c)))
 if $- $2(D):
  if var is $#:
   $![(f,m)]
 $(:
  v=$S(D)
  if $/(v)is $1:
   v=v.$N
  if v<0 $* $- $@:
   $![(f,m)]
 sD=$V(D)
 r1=$O($]($k(b),sD),$:(2,a))
 r2=$O($[($k(b),sD),$:(2,a))
 res=[(a,m)]if a!=1 $([]
 res.$%(($[(x,r2),m))
 res.$%(($[(x,r1),m))
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
 $) v in p_vars(N,$5(ks))+p_vars(D,$5(ks)):
  if v!=k:
   $! $#
 nv=$5(ks)
 num=[0]*(max(p_deg(N,k),0)+1)
 $) m in N:
  num[m[k]]=N[m]
 den=[0]*(p_deg(D,k)+1)
 $) m in D:
  den[m[k]]=D[m]
 if $5(den)<=1:
  $! $#
 q,rem=u_divmod(num,den)
 cc,fs=ufactor(den)
 $L=[u_toexpr(q,x)]
 if rem:
  $y=[u_trim(pw_list(f,m))$) f,m in fs]
  rem=u_scale(rem,ninv(cc))
  $) j in $+($5(fs)):
   f,m=fs[j]
   Pj=$y[j]
   others=[1]
   $) i in $+($5(fs)):
    if i!=j:
     others=u_mul(others,$y[i])
   g,s,t=u_egcd(others,Pj)
   Aj=u_divmod(u_mul(rem,s),Pj)[1]
   fe=u_toexpr(f,x)
   $) p in $+(m,0,-1):
    if $- Aj:
     $T
    qq,cj=u_divmod(Aj,f)
    if cj:
     $L.$%($O(u_toexpr(cj,x),pw(fe,p)))
    Aj=qq
 $! $;($L)
$, pw_list(f,m):
 r=[1]
 $) _ in $+(m):
  r=u_mul(r,f)
 $! r
$, propfrac(e,x=$#):
 if $r(e):
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
  vs=p_vars(D,$5(ks))
  if $- vs:
   $! e
  x=ks[vs[0]]
 num=p2e(N,ks)
 den=p2e(D,ks)
 cn=$X(num,x)
 cd=$X(den,x)
 if cn is $# or cd is $# or $5(cd)<=1:
  $! e
 qq,rr=e_divmod(cn,cd)
 $! $](fromcoeffs(qq,x),$O(fromcoeffs(rr,x),den))
$, e_divmod(a,b):
 a=[$>(c)$) c in a]
 b=[$>(c)$) c in b]
 $J b $* b[-1]==0:
  b.pop()
 $J a $* a[-1]==0:
  a.pop()
 if $- b:
  err("Division by zero")
 q=[0]*max($5(a)-$5(b)+1,1)
 r=$I(a)
 lb=b[-1]
 $J $5(r)>=$5(b)$* r:
  c=$.($O(r[-1],lb))
  kk=$5(r)-$5(b)
  q[kk]=c
  $) j in $+($5(b)):
   r[kk+j]=$>($[(r[kk+j],$:(c,b[j])))
  r.pop()
  $J r $* r[-1]==0:
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
 nv=$5(ks)
 g=p_gcd(ra[0],rb[0],nv)
 if $- ks:
  $! p_cval(g)
 $! p2e(g,ks)
$, expand_full(e,var=$#):
 if $&(e,'$I')or $&(e,'mat'):
  $! mapexpr($7 a:expand_full(a,var),e)
 if isrel(e):
  $!(e[0],expand_full(e[1],var),expand_full(e[2],var))
 x=$>(e)
 if $- hasdenom(x)or $^(x):
  $! x
 if var is $#:
  ks=$q(x)
  ks.sort(key=varprio)
  $) v in ks:
   r=partfrac(x,v)
   if r is $- $#:
    $! $>(r)
  $! x
 r=partfrac(x,var)
 if r is $- $#:
  $! $>(r)
 $! x
''')
_x(r'''TV='T_'
LNT='LNT_'
VV='V_'
class $i($6):
 pass
$, dfun($B,u):
 if $B=='sin':
  $! fn('cos',u)
 if $B=='cos':
  $! $k(fn('sin',u))
 if $B=='tan':
  $! pw(fn('cos',u),-2)
 if $B=='$~':
  $! pw($[(1,pw(u,2)),Q(-1,2))
 if $B=='arccos':
  $! $k(pw($[(1,pw(u,2)),Q(-1,2)))
 if $B=='$x':
  $! pw($](pw(u,2),1),-1)
 if $B=='sinh':
  $! fn('cosh',u)
 if $B=='cosh':
  $! fn('sinh',u)
 if $B=='tanh':
  $! pw(fn('cosh',u),-2)
 if $B=='arcsinh':
  $! pw($](pw(u,2),1),Q(-1,2))
 if $B=='arccosh':
  $! pw($[(pw(u,2),1),Q(-1,2))
 if $B=='arctanh':
  $! pw($[(1,pw(u,2)),-1)
 if $B=='ln':
  $! pw(u,-1)
 if $B=='$H':
  $! fn('sign',u)
 if $B in('sign','floor','ceiling','round','ipart','$w'):
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
 if $&(e,'$I')or $&(e,'mat'):
  $! mapexpr($7 a:diff1(a,x),e)
 if $&(e,'=')or $&(e,'<')or $&(e,'>'):
  $!(e[0],diff1(e[1],x),diff1(e[2],x))
 if $4(e,x):
  $! 0
 if e==x:
  $! 1
 h=e[0]
 if h=='+':
  $! $;([diff1(a,x)$) a in e[1:]])
 if h=='*':
  fs=e[1:]
  $L=[]
  $) i in $+($5(fs)):
   d=diff1(fs[i],x)
   if d!=0:
    $L.$%($G([d]+[fs[j]$) j in $+($5(fs))if j!=i]))
  $! $;($L)
 if h=='^':
  b=e[1]
  p=e[2]
  if $4(p,x):
   $! $:(p,pw(b,$[(p,1)),diff1(b,x))
  if $4(b,x):
   $! $:(e,fn('ln',b),diff1(p,x))
  $! $:(e,$]($:(diff1(p,x),fn('ln',b)),$O($:(p,diff1(b,x)),b)))
 if h=='log':
  b=e[2]if $5(e)>2 $( 10
  $! diff1($O(fn('ln',e[1]),fn('ln',b)),x)
 if h=='when':
  $! fn('when',e[1],diff1(e[2],x),diff1(e[3],x))if $5(e)>3 $( fn('when',e[1],diff1(e[2],x))
 if h=='$Z' $* $5(e)==3 $* e[2]==x:
  $! e[1]
 if h=='$Z' $* $5(e)==5 $* $4(e[1],x)is $3 $* e[2]!=x:
  f,v,a,b=e[1],e[2],e[3],e[4]
  $! $[($:($Q(f,v,b),diff1(b,x)),$:($Q(f,v,a),diff1(a,x)))
 if $5(e)==2:
  d=dfun(h,e[1])
  if d is $- $#:
   $! $:(d,diff1(e[1],x))
 $!('d',e,x)
$, $g(u,x):
 cs=$X(u,x)
 if cs is $# or $5(cs)!=2 or cs[1]==0:
  $! $#
 $! cs[1],cs[0]
$, nice(e):
 try:
  e=$.(e)
 $9 $6:
  $! e
 if $- hasdenom(e)or $^(e)or $&(e,'$I')or $&(e,'mat'):
  $! e
 $z=e
 bl=$5(fmt(e))
 if bl>400:
  $! e
 $) f in(comdenom,factor_expr):
  try:
   c=f(e)
   l=$5(fmt(c))
   if l<bl:
    $z=c
    bl=l
  $9 $6:
   pass
 $! $z
BUDGET=[0]
$, integrate(f,x,$<=0):
 BUDGET[0]=0
 r=$|(f,x,$<)
 if r is $# $* hasdenom(f):
  g=$.(f)
  if g!=f:
   BUDGET[0]=0
   r=$|(g,x,$<)
 if r is $#:
  $!('$Z',f,x)
 $! r
$, $|(f,x,$<=0):
 if $<>7:
  $! $#
 if $<==0:
  BUDGET[0]=0
 BUDGET[0]+=1
 if BUDGET[0]>400:
  $! $#
 if $4(f,x):
  $! $:(f,x)
 if f==x:
  $! $:($s,pw(x,2))
 h=f[0]if $/(f)is $0 $( $#
 if h=='+':
  $?=[]
  $) t in f[1:]:
   r=$|(t,x,$<+1)
   if r is $#:
    $! integ_whole(f,x,$<)
   $?.$%(r)
  $! $;($?)
 if h=='*':
  c=[g $) g in f[1:]if $4(g,x)]
  v=[g $) g in f[1:]if $- $4(g,x)]
  if c:
   r=$|($G(v),x,$<)
   if r is $#:
    $! $#
   $! $:($G(c),r)
 if h=='when':
  a=$|(f[2],x,$<+1)
  b=$|(f[3],x,$<+1)if $5(f)>3 $( $#
  if a is $# or($5(f)>3 $* b is $#):
   $! $#
  $!('when',f[1],a,b)if b is $- $# $(('when',f[1],a)
 r=itable(f,x)
 if r is $- $#:
  $! r
 $! integ_whole(f,x,$<)
$, integ_whole(f,x,$<):
 d=degree(f,x)
 if d is $- $#:
  g=$>(f)
  if g!=f:
   $! $|(g,x,$<+1)
 r=irational(f,x)
 if r is $- $#:
  $! r
 r=itanpow(f,x,$<)
 if r is $- $#:
  $! r
 r=isecpow(f,x,$<)
 if r is $- $#:
  $! r
 r=isubst(f,x,$<)
 if r is $- $#:
  $! r
 r=itrigsub(f,x,$<)
 if r is $- $#:
  $! r
 if hastrig(f):
  g=tcollect(f)
  if g!=f:
   r=$|(g,x,$<+1)
   if r is $- $#:
    $! r
 r=iparts(f,x,$<)
 if r is $- $#:
  $! r
 g=$>(f)
 if g!=f:
  r=$|(g,x,$<+1)
  if r is $- $#:
   $! r
 if $<<4:
  g=untan(f)
  if g!=f:
   r=$|(g,x,$<+2)
   if r is $- $#:
    $! r
  g=unhyp(f)
  if g!=f:
   r=$|($>(g),x,$<+2)
   if r is $- $#:
    $! r
  r=iweier(f,x,$<)
  if r is $- $#:
   $! r
  r=iquartic(f,x,$<)
  if r is $- $#:
   $! r
 $! $#
$, qfrac(A,B,p,q,x):
 w=$V($[($:(4,q),pw(p,2)))
 P=$](pw(x,2),$:(p,x),q)
 $! $]($:(A,$s,fn('ln',P)),
 $:($[(B,$:(A,p,$s)),$O(2,w),fn("$x",$>($O($]($:(2,x),p),w)))))
$, iquartic(f,x,$<):
 n,d=numer_denom(f)
 cd=$X(d,x)
 cn=$X(n,x)
 if cd is $# or cn is $# or $5(cd)!=5 or $5(cn)>4:
  $! $#
 if cd[1]!=0 or cd[3]!=0 or $- all([$2(q)$) q in cd+cn]):
  $! $#
 a,b,c=cd[4],cd[2],cd[0]
 try:
  if fv_(c)/fv_(a)<=0:
   $! $#
  q=$V($O(c,a))
  s2=$[($:(2,q),$O(b,a))
  if fv_(s2)<=0:
   $! $#
 $9 $6:
  $! $#
 sr=$V(s2)
 cn=[$O(v,a)$) v in cn]+[0]*(4-$5(cn))
 n0,n1,n2,n3=cn
 BE=$O(n0,q)
 EmB=$O($[(n1,$:(q,n3)),sr)
 B=$:($s,$[(BE,EmB))
 E=$:($s,$](BE,EmB))
 CmA=$O($[(n2,BE),sr)
 A=$:($s,$[(n3,CmA))
 C=$:($s,$](n3,CmA))
 P1=$](pw(x,2),$:(sr,x),q)
 P2=$]($[(pw(x,2),$:(sr,x)),q)
 R=$](qfrac(A,B,sr,q,x),qfrac(C,E,$k(sr),q,x))
 $! R if antiok(R,f,x)$( $#
$, unhyp(e):
 if $/(e)is $- $0 or e[0]=='Q':
  $! e
 a=[unhyp(b)$) b in e[1:]]
 if $5(a)==1 $* e[0]in('sinh','cosh','tanh'):
  p=pw('e',a[0])
  m=pw('e',$k(a[0]))
  if e[0]=='sinh':
   $! $:($s,$[(p,m))
  if e[0]=='cosh':
   $! $:($s,$](p,m))
  $! $O($[(p,m),$](p,m))
 $! simp((e[0],)+$0(a))
''')
_x(r'''$, trigargs_x(f,x,$?):
 if $/(f)is $- $0 or f[0]=='Q':
  $!
 if f[0]in('sin','cos','tan')$* $- $4(f[1],x):
  if f[1]$- in $?:
   $?.$%(f[1])
  $!
 $) b in f[1:]:
  trigargs_x(b,x,$?)
$, iweier(f,x,$<):
 us=[]
 trigargs_x(f,x,us)
 if $5(us)!=1:
  $! $#
 u=us[0]
 lu=$g(u,x)
 if lu is $#:
  $! $#
 t='W%d_'%$<
 q=$](1,pw(t,2))
 $, rep(e):
  if $/(e)is $- $0 or e[0]=='Q':
   $! e
  if $5(e)==2 $* e[1]==u:
   if e[0]=='sin':
    $! $O($:(2,t),q)
   if e[0]=='cos':
    $! $O($[(1,pw(t,2)),q)
   if e[0]=='tan':
    $! $O($:(2,t),$[(1,pw(t,2)))
  $! simp((e[0],)+$0(rep(b)$) b in e[1:]))
 g=rep(f)
 if $- $4(g,x):
  $! $#
 g=$.($O($:(2,g),$:(lu[0],q)))
 R=$|(g,t,$<+2)
 if R is $#:
  $! $#
 R=$Q(R,t,fn('tan',$:($s,u)))
 $! R if antiok(R,f,x)$( $#
$, itable(f,x):
 h=head(f)
 if h=='^':
  b=f[1]
  p=f[2]
  if $4(p,x):
   lb=$g(b,x)
   if lb is $- $#:
    a=lb[0]
    if p==-1:
     $! $O(fn('ln',fn('$H',b)),a)
    $! $O(pw(b,$](p,1)),$:(a,$](p,1)))
   if(p==$s or p==Q(-1,2))$* degree(b,x)==2:
    $! iquadrad(b,p,x)
   if $5(b)==2 $* head(b)in('sin','cos','tan','sinh','cosh')$* $/(b)is $0:
    lu=$g(b[1],x)
    if lu is $- $#:
     a=lu[0]
     u=b[1]
     n=b[0]
     if n=='cos' $* p==-2:
      $! $O(fn('tan',u),a)
     if n=='sin' $* p==-2:
      $! $O($k(pw(fn('tan',u),-1)),a)
     if n=='cos' $* p==-1:
      $! $O(fn('ln',fn('$H',$](pw(fn('cos',u),-1),fn('tan',u)))),a)
     if n=='sin' $* p==-1:
      $! $O(fn('ln',fn('$H',fn('tan',$:($s,u)))),a)
     if n=='tan' $* p==-1:
      $! $O(fn('ln',fn('$H',fn('sin',u))),a)
     if n=='cosh' $* p==-2:
      $! $O(fn('tanh',u),a)
  if $4(b,x):
   lu=$g(p,x)
   if lu is $- $#:
    a=lu[0]
    if b=='e':
     $! $O(f,a)
    $! $O(f,$:(a,fn('ln',b)))
  $! $#
 if $/(f)is $0 $* $5(f)==2:
  u=f[1]
  lu=$g(u,x)
  if lu is $#:
   $! $#
  a=lu[0]
  r=$#
  if h=='sin':
   r=$k(fn('cos',u))
  $K h=='cos':
   r=fn('sin',u)
  $K h=='tan':
   r=$k(fn('ln',fn('$H',fn('cos',u))))
  $K h=='sinh':
   r=fn('cosh',u)
  $K h=='cosh':
   r=fn('sinh',u)
  $K h=='tanh':
   r=fn('ln',fn('cosh',u))
  $K h=='ln':
   r=$[($:(u,fn('ln',u)),u)
  $K h=='$x':
   r=$[($:(u,fn('$x',u)),$:($s,fn('ln',$](pw(u,2),1))))
  $K h=='$~':
   r=$]($:(u,fn('$~',u)),$V($[(1,pw(u,2))))
  $K h=='arccos':
   r=$[($:(u,fn('arccos',u)),$V($[(1,pw(u,2))))
  $K h=='$H':
   r=$:($s,u,fn('$H',u))
  $K h=='sign':
   r=fn('$H',u)
  $K h=='arcsinh':
   r=$[($:(u,fn('arcsinh',u)),$V($](pw(u,2),1)))
  $K h=='arctanh':
   r=$]($:(u,fn('arctanh',u)),$:($s,fn('ln',$[(1,pw(u,2)))))
  if r is $- $#:
   $! $O(r,a)
 if h=='log' $* $5(f)==3:
  lu=$g(f[1],x)
  if lu is $- $#:
   u=f[1]
   $! $O($[($:(u,fn('ln',u)),u),$:(lu[0],fn('ln',f[2])))
 $! $#
$, iquadrad(b,p,x):
 cs=$X(b,x)
 C,B,A=cs
 if $- $2(A):
  $! $#
 av=$S(A)
 if $/(av)is $1:
  $! $#
 D=$[($:(B,B),$:(4,A,C))
 if p==Q(-1,2):
  if av<0:
   $! $:(pw($k(A),Q(-1,2)),fn('$~',$O($k($]($:(2,A,x),B)),$V(D))))
  sA=$V(A)
  $! $:(pw(A,Q(-1,2)),fn('ln',fn('$H',$]($V(b),$:(sA,x),$O(B,$:(2,sA))))))
 J=iquadrad(b,Q(-1,2),x)
 if J is $#:
  $! $#
 $! $]($O($:($]($:(2,A,x),B),$V(b)),$:(4,A)),
 $:($O($[($:(4,A,C),$:(B,B)),$:(8,A)),J))
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
 $L=pf[1:]if $&(pf,'+')$((pf,)
 $?=[]
 $) t in $L:
  if $- hasdenom(t):
   r=$|(t,x,5)
   if r is $#:
    $! $#
   $?.$%(r)
   $8
  fs=t[1:]if $&(t,'*')$((t,)
  num=[]
  den=$#
  k=1
  $) g in fs:
   if $&(g,'^')$* $/(g[2])is $w $* g[2]<0:
    den=g[1]
    k=-g[2]
   $(:
    num.$%(g)
  if den is $#:
   $! $#
  N=$G(num)
  dg=degree(den,x)
  if dg==1:
   r=$|(t,x,5)
   if r is $#:
    $! $#
   $?.$%(r)
  $K dg==2:
   r=iquadfrac(N,den,k,x)
   if r is $#:
    $! $#
   $?.$%(r)
  $(:
   r=isubst(t,x,3)if k==1 $( $#
   if r is $# $* k==1:
    r=iquartic(t,x,3)
   if r is $#:
    $! $#
   $?.$%(r)
 $! $;($?)
$, iquadfrac(N,Qd,k,x):
 cs=$X(N,x)
 if cs is $# or $5(cs)>2:
  $! $#
 n0=cs[0]
 n1=cs[1]if $5(cs)>1 $( 0
 C,B,A=$X(Qd,x)
 res=[]
 if n1!=0:
  if k==1:
   D=$[($:(B,B),$:(4,A,C))
   dv=$S(D)if $2(D)$( 0
   arg=Qd if($/(dv)is $- $1 $* dv<0 $* $S(A)>0)$( fn('$H',Qd)
   res.$%($:($O(n1,$:(2,A)),fn('ln',arg)))
  $(:
   res.$%($:($O(n1,$:(2,A)),$O(-1,$:(k-1,pw(Qd,k-1)))))
 c0=$[(n0,$O($:(n1,B),$:(2,A)))
 if c0!=0:
  J=jquad(A,B,C,Qd,k,x)
  if J is $#:
   $! $#
  res.$%($:(c0,J))
 $! $;(res)
$, jquad(A,B,C,Qd,k,x):
 D=$>($[($:(B,B),$:(4,A,C)))
 if k==1:
  if $- $2(D):
   $! $#
  dv=$S(D)
  if $/(dv)is $1:
   $! $#
  L=$]($:(2,A,x),B)
  if dv<0:
   s=$V($k(D))
   $! $:($O(2,s),fn('$x',$O(L,s)))
  if dv>0:
   s=$V(D)
   $! $:(pw(s,-1),fn('ln',fn('$H',$O($[(L,s),$](L,s)))))
  $! $O(-2,L)
 Jp=jquad(A,B,C,Qd,k-1,x)
 if Jp is $#:
  $! $#
 Dl=$k(D)
 L=$]($:(2,A,x),B)
 $! $]($:($O(L,$:(k-1,Dl)),pw(Qd,1-k)),
 $:($O($:(2*k-3,2,A),$:(k-1,Dl)),Jp))
$, itanpow(f,x,$<):
 if $&(f,'^')$* $&(f[1],'tan')$* $/(f[2])is $w $* f[2]>=2:
  u=f[1][1]
  lu=$g(u,x)
  if lu is $#:
   $! $#
  n=f[2]
  a=lu[0]
  t=f[1]
  first=$O(pw(t,n-1),$:(n-1,a))
  $d=$|(pw(t,n-2),x,$<+1)
  if $d is $#:
   $! $#
  $! $[(first,$d)
 $! $#
''')
_x(r'''$, isecpow(f,x,$<):
 if($&(f,'^')$* head(f[1])in('cos','sin')$* $5(f[1])==2
 $* $/(f[2])is $w $* f[2]<=-3):
  u=f[1][1]
  lu=$g(u,x)
  if lu is $#:
   $! $#
  n=-f[2]
  a=lu[0]
  if f[1][0]=='cos':
   first=$:(pw(fn('cos',u),2-n),fn('tan',u))
  $(:
   first=$k($:(pw(fn('sin',u),2-n),pw(fn('tan',u),-1)))
  $d=$|(pw(f[1],2-n),x,$<+1)
  if $d is $#:
   $! $#
  $! $]($O(first,$:(n-1,a)),$:(Q(n-2,n-1),$d))
 $! $#
$, cands(f,x,$?):
 if $/(f)is $- $0 or $4(f,x)or f[0]=='Q':
  $!
 h=f[0]
 if h=='+' or h=='*':
  $) a in f[1:]:
   cands(a,x,$?)
  $!
 if h=='^':
  if f[1]!=x $* $- $4(f[1],x)$* f[1]$- in $?:
   $?.$%(f[1])
  if isq(f[2])$* $- $4(f[1],x):
   rad=pw(f[1],Q(1,f[2][2]))
   if rad $- in $?:
    $?.$%(rad)
  if $- $4(f[2],x)$* f[2]$- in $?:
   $?.$%(f[2])
   if f $- in $?:
    $?.$%(f)
  if f[1]==x $* f $- in $? $* $C(f[2])$* f[2]!=-1:
   $?.$%(f)
   if $j(f[2])$* f[2]%2==0 $* f[2]>2 $* pw(x,2)$- in $?:
    $?.$%(pw(x,2))
  cands(f[1],x,$?)
  cands(f[2],x,$?)
  $!
 if f $- in $?:
  $?.$%(f)
 $) a in f[1:]:
  if a!=x $* $- $4(a,x)$* a $- in $?:
   $?.$%(a)
  cands(a,x,$?)
$, subst_kernel(q,u,V,x):
 if $&(u,'^')$* u[1]==x $* $C(u[2]):
  q2=$Q(q,x,pw(V,pw(u[2],-1)))
  $! $Q(q2,fn('$H',V),V)
 if $&(u,'ln'):
  lu=$g(u[1],x)
  if lu is $- $#:
   a,b=lu
   $! $Q(q,x,$O($[(pw('e',V),b),a))
 if $&(u,'^')$* isq(u[2])$* $- $4(u[1],x):
  cs_=$X(u[1],x)
  q2=$Q(q,u,V)
  if cs_ is $- $# $* $- $4(q2,x):
   nz=[k $) k in $+(1,$5(cs_))if cs_[k]!=0]
   if $5(nz)==1:
    k=nz[0]
    xk=$O($[(pw(V,pw(u[2],-1)),cs_[0]),cs_[k])
    q3=$Q(q2,x,pw(xk,Q(1,k)))
    if $4(q3,x):
     $! q3
  $! q2
 if $&(u,'^')$* u[1]=='e':
  lu=$g(u[2],x)
  if lu is $- $# $* lu[1]==0:
   a=lu[0]
   $! subst_exp(q,a,V,x)
 $! $Q(q,u,V)
$, subst_exp(q,a,V,x):
 if $/(q)is $- $0 or q[0]=='Q':
  $! q
 if q[0]=='^' $* q[1]=='e':
  lm=$g(q[2],x)
  if lm is $- $#:
   $! $:(pw(V,$O(lm[0],a)),pw('e',lm[1]))
 $! simp((q[0],)+$0(subst_exp(b,a,V,x)$) b in q[1:]))
$, isubst(f,x,$<):
 if $<>5:
  $! $#
 VV='V%d_'%$<
 $J has(f,VV)or VV==x:
  VV=VV+'_'
 cs=[]
 cands(f,x,cs)
 fracf=hasfracpow(f,x)
 big=$5(okey(f))>500
 $) u in cs[:14]:
  if u==x:
   $8
  du=diff(u,x)
  if du==0:
   $8
  q=$O(f,du)
  if $- big:
   q=$.(q)
  q2=subst_kernel(q,u,VV,x)
  if $4(q2,x)$*(fracf or $- hasfracpow(q2,VV))$* $5(okey(q2))<800:
   r=$|(q2,VV,$<+2)
   if r is $- $#:
    r=$Q(r,VV,u)
    if antiok(r,f,x):
     $! r
 $) u in cs:
  if $&(u,'+'):
   lu=$g(u,x)
   if lu is $- $#:
    a,b=lu
    g=$>($O($Q(f,x,$O($[(VV,b),a)),a))
    r=$|(g,VV,$<+2)
    if r is $- $#:
     $! $Q(r,VV,u)
 $! $#
TPTS=(-2.3,-1.7,-0.8,-0.35,0.3,0.75,1.6,2.4)
$, antiok(F,f,x):
 if $5($q(f))>1 or $5($q(F))>1:
  $! $E
 $, v(e,t):
  try:
   z=$S(e,{x:t})
  $9 $6:
   $! $#
  if $/(z)is $1:
   if $H(z.imag)>1e-9*(1+$H(z.$N)):
    $! $#
   z=z.$N
  if z!=z or $H(z)>1e12:
   $! $#
  $! z
 $) t in TPTS:
  y=v(f,t)
  if y is $#:
   $8
  h=1e-5*(1+$H(t))
  a=v(F,t+h)
  b=v(F,t-h)
  if a is $# or b is $#:
   $8
  if $H((a-b)/(2*h)-y)>1e-4*(1+$H(y)):
   $! $3
 $! $E
$, itrigsub(f,x,$<):
 rad=[]
 radicals(f,x,rad)
 if $- rad:
  $! $#
 B=rad[0]
 cs=$X(B,x)
 if cs is $# or $5(cs)!=3 or cs[1]!=0 or $- $2(cs[0])or $- $2(cs[2]):
  $! $#
 if any([q!=B $) q in rad]):
  $! $#
 c0,c2=cs[0],cs[2]
 T='T%d_'%$<
 if fv_(c0)<0 $* fv_(c2)>0:
  r=$V($O($k(c0),c2))
  xs=$O(r,fn('cos',T))
  rt=$:($V(c2),r,fn('tan',T))
  dx=$:(r,fn('tan',T),pw(fn('cos',T),-1))
  g=$:(subrad(f,B,rt,x,xs),dx)
  R=$#
  $) h in(pyth_to(g,'cos'),pyth_to(g,'sin'),pyth(g)):
   R=$|(h,T,$<+2)
   if R is $- $#:
    $T
  if R is $#:
   $! $#
  R=backtrig(texpand(R),T,$O(pw(B,$s),$:($V(c2),x)),$O(r,x))
  R=$Q(R,T,fn('arccos',$O(r,x)))
  if $- $4(R,T)or $- antiok(R,f,x):
   $! $#
  $! R
 if fv_(c0)<=0:
  $! $#
 sc0=$V(c0)
 if fv_(c2)<0:
  r=$V($O(c0,$k(c2)))
  xs=$:(r,fn('sin',T))
  rt=$:(sc0,fn('cos',T))
  dx=$:(r,fn('cos',T))
 $(:
  r=$V($O(c0,c2))
  xs=$:(r,fn('tan',T))
  rt=$O(sc0,fn('cos',T))
  dx=$O(r,pw(fn('cos',T),2))
 g=$:(subrad(f,B,rt,x,xs),dx)
 R=$#
 $) h in(pyth(g),pyth_to(g,'cos'),pyth_to(g,'sin')):
  R=$|(h,T,$<+2)
  if R is $- $#:
   $T
 if R is $#:
  $! $#
 R=texpand(R)
 sq=pw(B,$s)
 if fv_(c2)<0:
  sinT=$O(x,r)
  cosT=$O(sq,sc0)
  Tx=fn('$~',$O(x,r))
 $(:
  cosT=$O(sc0,sq)
  sinT=$:($O(x,r),cosT)
  Tx=fn('$x',$O(x,r))
 R=backtrig(R,T,sinT,cosT)
 R=$Q(R,T,Tx)
 if $- $4(R,T)or $- antiok(R,f,x):
  $! $#
 $! R
$, radicals(f,x,$?):
 if $/(f)is $- $0 or f[0]=='Q':
  $!
 if f[0]=='^' $* isq(f[2])$* f[2][2]==2 $* $- $4(f[1],x):
  $?.$%(f[1])
 $) a in f[1:]:
  radicals(a,x,$?)
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
 if $5(R)==2 $* R[1]==T:
  if R[0]=='sin':
   $! sinT
  if R[0]=='cos':
   $! cosT
  if R[0]=='tan':
   $! $O(sinT,cosT)
 $! simp((R[0],)+$0(backtrig(a,T,sinT,cosT)$) a in R[1:]))
$, hasfracpow(e,x):
 if $/(e)is $- $0 or e[0]=='Q':
  $! $3
 if e[0]=='^' $* $- $j(e[2])$* $- $4(e[1],x):
  $! $E
 $) a in e[1:]:
  if hasfracpow(a,x):
   $! $E
 $! $3
''')
_x(r'''$, hastrig(f):
 if $/(f)is $- $0 or f[0]=='Q':
  $! $3
 if f[0]in('sin','cos'):
  $! $E
 $) a in f[1:]:
  if hastrig(a):
   $! $E
 $! $3
$, ispoly(e,x):
 $! degree(e,x)is $- $#
$, iparts(f,x,$<):
 if $<>5:
  $! $#
 fs=f[1:]if $&(f,'*')$((f,)
 P=[]
 G=[]
 $) g in fs:
  if ispoly(g,x):
   P.$%(g)
  $(:
   G.$%(g)
 if $5(G)==2:
  ex=$#
  tr=$#
  $) g in G:
   if $&(g,'^')$* g[1]=='e' $* $g(g[2],x):
    ex=g
   $K head(g)in('sin','cos')$* $g(g[1],x):
    tr=g
  if ex is $- $# $* tr is $- $# $* $- P:
   a=$g(ex[2],x)[0]
   b=$g(tr[1],x)[0]
   u=tr[1]
   den=$]($:(a,a),$:(b,b))
   if tr[0]=='sin':
    r=$:(ex,$[($:(a,fn('sin',u)),$:(b,fn('cos',u))))
   $(:
    r=$:(ex,$]($:(a,fn('cos',u)),$:(b,fn('sin',u))))
   $! $O(r,den)
  $! $#
 if $5(G)!=1:
  $! $#
 g=G[0]
 Pp=$G(P)
 gh=head(g)
 tabular=$3
 if $&(g,'^')$* g[1]=='e' $* $g(g[2],x):
  tabular=$E
 $K $&(g,'^')$* $C(g[1])$* $g(g[2],x):
  tabular=$E
 $K gh in('sin','cos','sinh','cosh')$* $g(g[1],x):
  tabular=$E
 if tabular $* P:
  res=[]
  sg=1
  Gi=g
  Pd=Pp
  $) _ in $+(40):
   Gi=$|(Gi,x,$<+1)
   if Gi is $#:
    $! $#
   res.$%($:(sg,Pd,Gi))
   Pd=diff(Pd,x)
   sg=-sg
   if Pd==0:
    $! $;(res)
  $! $#
 if gh in('ln','$x','$~','arccos','log','arcsinh','arctanh')or($&(g,'^')$* head(g[1])in('ln','$~','$x')$* $j(g[2])$* g[2]>0):
  V=$|(Pp,x,$<+1)
  if V is $#:
   $! $#
  $d=$|($.($>($:(V,diff(g,x)))),x,$<+1)
  if $d is $#:
   $! $#
  $! $[($:(g,V),$d)
 $! $#
$, defint(f,x,a,b):
 if a==b:
  $! 0
 if $2(a)$* $2(b):
  try:
   if numpt(a)>numpt(b):
    r=defint(f,x,b,a)
    $! $k(r)if $- $&(r,'$Z')$(('$Z',f,x,a,b)
  $9 $6:
   pass
 if haswhen(f,x)$* $2(a)$* $2(b):
  ps=whensplit(f,x,a,b)
  if ps is $- $#:
   total=0
   $) p,q,g in ps:
    if g=='$F' or has(g,'$F'):
     $! '$F'
    total=$](total,defint(g,x,p,q))
   $! total
 BUDGET[0]=0
 F=$|(f,x)
 if F is $# $* hasdenom(f):
  BUDGET[0]=0
  F=$|($.(f),x)
 sing=singular_points(f,x,a,b)or[]
 if F is $- $# $* $- $^(f):
  $) p in singular_points(F,x,a,b)or[]:
   if all([$H(fv_(p)-fv_(q))>1e-9 $) q in sing]):
    sing.$%(p)
  sing.sort(key=fv_)
  if $2(a)$* $2(b)$* fv_(a)>fv_(b):
   sing.reverse()
  pts=[a]+sing+[b]
  total=0
  infs=[]
  $) i in $+($5(pts)-1):
   lo=pts[i]
   hi=pts[i+1]
   vb=$v(F,x,hi,-1 if $- isinf(hi)$( 0)
   va=$v(F,x,lo,1 if $- isinf(lo)$( 0)
   if $&(vb,'$v')or $&(va,'$v'):
    total=$#
    $T
   d=$[(vb,va)
   if va=='$F' or vb=='$F':
    $! '$F'
   if has(va,'$M')or has(vb,'$M'):
    if d $- in('$M',('*',-1,'$M')):
     $! '$F'
   if d=='$F' or has(d,'$F'):
    total=$#
    $T
   if has(d,'$M'):
    infs.$%(d)
   total=$](total,d)
  if total is $- $# $* infs:
   if all([q==infs[0]$) q in infs])$* infs[0]in('$M',('*',-1,'$M')):
    $! infs[0]
   $! '$F'
  if total is $- $# $* total!='$F':
   $! total
 if $2(a)$* $2(b)$* freeofall(f,[s $) s in $q(f)if s!=x]):
  try:
   $! nint_split(f,x,a,b)
  $9 $6:
   pass
 $!('$Z',f,x,a,b)
$, haswhen(f,x):
 if $/(f)is $- $0 or f[0]=='Q':
  $! $3
 if f[0]in('when','$H')$* $- $4(f[1],x):
  $! $E
 $) a in f[1:]:
  if haswhen(a,x):
   $! $E
 $! $3
$, gensol(r):
 ns=[w $) w in $q(r)if w[0]=='n' $* w[1:].isdigit()]
 if $5(ns)==1 $* $2($Q(r,ns[0],0)):
  $! ns[0]
 $! $#
$, firstwhen_(f,x):
 if $/(f)is $- $0 or f[0]=='Q':
  $! $3
 if f[0]=='when' $* $- $4(f[1],x):
  $! $E
 $! any([firstwhen_(a,x)$) a in f[1:]])
$, whenpts(f,x,$?):
 if $/(f)is $- $0 or f[0]=='Q':
  $!
 if f[0]=='$H' $* $- $4(f[1],x):
  rs=$m(f[1],x,$3)
  if rs $* rs!='all':
   $) r in rs:
    if($t(r)or gensol(r))$* r $- in $?:
     $?.$%(r)
 if f[0]=='when' $* $- $4(f[1],x):
  cs=[f[1]]
  $J cs:
   c=cs.pop()
   if head(c)in('$*','or','$-'):
    cs.extend(c[1:])
   $K head(c)in('<','>','<=','>=','=','/='):
    rs=$m($[(c[1],c[2]),x,$3)
    if rs $* rs!='all':
     $) r in rs:
      if($t(r)or gensol(r))$* r $- in $?:
       $?.$%(r)
 $) a in f[1:]:
  whenpts(a,x,$?)
$, pickwhen(f,x,t):
 if $/(f)is $- $0 or f[0]=='Q':
  $! f
 if f[0]=='when' $* $- $4(f[1],x):
  try:
   c=nbool(f[1],{x:t})
  $9 $6:
   $! '$F'
  if c:
   $! pickwhen(f[2],x,t)
  $! pickwhen(f[3],x,t)if $5(f)>3 $( '$F'
 if f[0]=='$H' $* $- $4(f[1],x):
  u=pickwhen(f[1],x,t)
  try:
   $! u if fv_($Q(u,x,t))>=0 $( $k(u)
  $9 $6:
   $! f
 $! simp((f[0],)+$0(pickwhen(a,x,t)$) a in f[1:]))
$, numpt(v):
 if v=='$M':
  $! 1e300
 if v==('*',-1,'$M'):
  $!-1e300
 $! fv_(v)
$, fv_(v):
 z=$S(v)
 $! z.$N if $/(z)is $1 $( z
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
  $K hi-lo<1e4:
   $) k in $+(-300,301):
    q=$Q(p,n,k)
    if lo<fv_(q)<hi $* q $- in ex:
     ex.$%(q)
 ins=[p $) p in ex if lo<fv_(p)<hi]
 ins.sort(key=fv_)
 ends=[a]+ins+[b]
 $?=[]
 $) i in $+($5(ends)-1):
  p,q=ends[i],ends[i+1]
  pv,qv=numpt(p),numpt(q)
  if pv<-1e299:
   t=qv-1.0
  $K qv>1e299:
   t=pv+1.0
  $(:
   t=0.5*(pv+qv)
  $?.$%((p,q,pickwhen(f,x,t)))
 $! $?
''')
_x(r'''$, whenlimit(f,x,a,dirn):
 pts=[]
 whenpts(f,x,pts)
 if isinf(a):
  t=1e6 if a=='$M' $(-1e6
  $! $v(pickwhen(f,x,t),x,a,dirn)
 av=fv_(a)
 d=1e-6
 $) p in pts:
  q=$H(fv_(p)-av)
  if q>1e-12:
   d=min(d,q/2)
 r=$v(pickwhen(f,x,av+d),x,a,1)if dirn>=0 $( $#
 l=$v(pickwhen(f,x,av-d),x,a,-1)if dirn<=0 $( $#
 if dirn==1:
  $! r
 if dirn==-1:
  $! l
 if r==l:
  $! r
 try:
  if $2(r)$* $2(l)$* $H($S(r)-$S(l))<1e-12:
   $! r
 $9 $6:
  pass
 $! '$F'
$, isinf(v):
 $! v=='$M' or v==('*',-1,'$M')
$, singular_points(f,x,a,b):
 if $-($2(a)$* $2(b)):
  $![]
 try:
  av=nreal(a)if $- isinf(a)$((-1e300 if a!='$M' $( 1e300)
  bv=nreal(b)if $- isinf(b)$((1e300 if b=='$M' $(-1e300)
 $9 $6:
  $![]
 lo,hi=min(av,bv),max(av,bv)
 pts=[]
 dens=[]
 collect_dens(f,x,dens)
 $) d in dens:
  u=u_from_expr(d,x)
  if u is $- $# $* $5(u)<2:
   $8
  if u is $#:
   if hi-lo<1e6:
    $) r in scanzeros(d,x,lo,hi):
     if all([$H(fv_(q)-r)>1e-9 $) q in pts]):
      pts.$%(snapzero(d,x,r))
   $8
  $) r in aberth(u):
   if $H(r.imag)<1e-9 $* lo<r.$N<hi:
    rr=exactify(r.$N)if $H(r.$N-round(r.$N))<1e-12 $( r.$N
    pts.$%(rr)
 pts.sort(key=fv_)
 if av>bv:
  pts.reverse()
 $! pts
$, collect_dens(f,x,$?):
 if $/(f)is $- $0 or f[0]=='Q':
  $!
 if f[0]=='^' $* $C(f[2])$* $_(f[2])<0 $* $- $4(f[1],x):
  $?.$%(f[1])
 if f[0]=='tan' $* $- $4(f[1],x):
  $?.$%(fn('cos',f[1]))
 if f[0]in('ln','log')$* $- $4(f[1],x):
  $?.$%(f[1])
 $) a in f[1:]:
  collect_dens(a,x,$?)
$, scanzeros(d,x,lo,hi,n=400):
 $?=[]
 $, g(t):
  try:
   v=$S(d,{x:t})
   $! v.$N if $/(v)is $1 $( v
  $9 $6:
   $! $#
 h=(hi-lo)/n
 t0=lo+h*1e-3
 v0=g(t0)
 $) k in $+(1,n+1):
  t1=lo+h*k-(h*1e-3 if k==n $( 0)
  v1=g(t1)
  if v0 is $- $# $* v1 is $- $# $* v0*v1<=0:
   a,b,fa=t0,t1,v0
   $) it in $+(60):
    m=0.5*(a+b)
    fm=g(m)
    if fm is $#:
     $T
    if(fm<=0)==(fa<=0):
     a,fa=m,fm
    $(:
     b=m
   m=0.5*(a+b)
   fm=g(m)
   if fm is $- $# $* $H(fm)<1e-6 $* lo<m<hi:
    $?.$%(m)
  t0,v0=t1,v1
 $! $?
$, snapzero(d,x,r):
 $) c in(exactify_guess(r/$W.pi),exactify_guess(r)):
  if $/(c)is $A:
   $8
  v=$:(c,'pi')if c is $- exactify_guess(r)$( c
  try:
   if $H(fv_($Q(d,x,v)))<1e-9:
    $! v
  $9 $6:
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
   g=$7 u:_nv(f,x,a0+w*u)
   $) k in $+(3):
    g=smooth(g)
    NERR[0]=0.0
    r=w*_gk_adapt(g,0.0,1.0,tol,0)
    if NERR[0]<=1e-7*max(1.0,$H(r)):
     $T
  if NERR[0]>1e-7*max(1.0,$H(r))$*(isinf(a)!=isinf(b)):
   if isinf(a):
    f,a,b=$Q(f,x,$k(x)),$k(b),'$M'
   a0=nreal(a)
   g=$7 t:_nv(f,x,a0+t/(1-t))/(1-t)**2 if t<1 $( 0.0
   $) j in $+(3):
    g=smooth(g)
    NERR[0]=0.0
    r=_gk_adapt(g,0.0,1.0,tol,0)
    if NERR[0]<=1e-7*max(1.0,$H(r)):
     $T
  if NERR[0]>1e-7*max(1.0,$H(r)):
   err('Questionable accuracy: the $Z may diverge')
 if r!=r or $H(r)==$A('$M'):
  err('Questionable accuracy: the $Z may diverge')
 if $/(r)is $1:
  if $H(r.imag)<1e-12*(1+$H(r.$N)):
   $! r.$N
  $! fromcomplex(r)
 $! r
$, nint0(f,x,a,b,tol=1e-10):
 sgn=1.0
 av=a
 bv=b
 if isinf(a)or isinf(b):
  if a=='$M' or b==('*',-1,'$M'):
   $!-nint0(f,x,b,a,tol)
  if isinf(a)$* isinf(b):
   g=$7 t:_nv(f,x,t/(1-t*t))*(1+t*t)/(1-t*t)**2
   $! _gk_adapt(g,-1.0,1.0,tol,0)
  if isinf(b):
   a0=nreal(a)
   g=$7 t:_nv(f,x,a0+t/(1-t))/(1-t)**2
   $! _gk_adapt(g,0.0,1.0,tol,0)
  b0=nreal(b)
  g=$7 t:_nv(f,x,b0-(1-t)/t)/(t*t)
  $! _gk_adapt(g,0.0,1.0,tol,0)
 a0=nreal(a)
 b0=nreal(b)
 g=$7 t:_nv(f,x,t)
 $! _gk_adapt(g,a0,b0,tol,0)
$, smooth(g):
 $! $7 t:g(t*t*(3-2*t))*6*t*(1-t)
$, nint_split(f,x,a,b):
 pts=[a]+(singular_points(f,x,a,b)or[])+[b]
 r=0
 $) i in $+($5(pts)-1):
  r=$](r,nint(f,x,pts[i],pts[i+1]))
 $! r
$, trigk(f,x,$?):
 if $/(f)is $- $0 or f[0]=='Q':
  $!
 if f[0]in('sin','cos')$* $- $4(f[1],x):
  lu=$g(f[1],x)
  $?.$%(lu[0]if lu is $- $# $* $2(lu[0])$( $#)
 $) a in f[1:]:
  trigk(a,x,$?)
$, nint_osc(f,x,a,b,tol):
 ks=[]
 trigk(f,x,ks)
 if $- ks or $# in ks:
  $! $#
 k=max([$H(tofl($S(q)))$) q in ks])
 if k==0:
  $! $#
 sgn_=1.0
 if isinf(a):
  f=$Q(f,x,$k(x))
  a,b=$k(b),'$M'
  if a==('*',-1,('*',-1,'$M')):
   a='$M'
 a0=tofl($S(a))
 h=$W.pi/k
 g=$7 t:_nv(f,x,t)
 sums=[]
 $L=[]
 s_=0.0
 t=a0
 $) i in $+(40):
  c=_gk_adapt(g,t,t+h,tol,6)
  s_+=c
  $L.$%($H(c))
  t+=h
  sums.$%(s_)
 if max($L[-4:])>0.25*max($L[:4])$* max($L[-4:])>1e-12:
  err('Questionable accuracy: the $Z may diverge')
 est=wynn(sums)
 est2=wynn(sums[:-6])
 if est is $# or est2 is $# or $H(est-est2)>1e-7*max(1.0,$H(est)):
  err('Questionable accuracy: the $Z may diverge')
 $! sgn_*est
$, wynn(S):
 n=$5(S)
 e0=[0.0]*(n+1)
 e1=$I(S)
 $z=S[-1]
 $) k in $+(1,n):
  e2=[]
  $) j in $+($5(e1)-1):
   d=e1[j+1]-e1[j]
   if d==0:
    $! e1[j+1]
   e2.$%(e0[j+1]+1.0/d)
  if k%2==0 $* e2:
   $z=e2[-1]
  e0,e1=e1,e2
  if $5(e1)<2:
   $T
 $! $z
$, _nv(f,x,t):
 try:
  v=$S(f,{x:t})
 $9 $D:
  $! 0.0
 $9($U,$`):
  $! 0.0
 if $/(v)is $1:
  if $H(v.imag)>1e-12*(1+$H(v.$N)):
   $! v
  v=v.$N
 if v!=v or v in($A('$M'),$A('-$M')):
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
 $! rk*h,$H((rk-rg)*h)
$, _gk_adapt(g,a,b,tol,$<):
 r,e=_gk(g,a,b)
 NBUD[0]-=1
 if NBUD[0]<0:
  NERR[0]+=e+1e-6*(1+$H(r))
  $! r
 if e<=tol*max(1.0,$H(r)):
  $! r
 if $<>18:
  NERR[0]+=e
  $! r
 m=0.5*(a+b)
 $! _gk_adapt(g,a,m,tol/2,$<+1)+_gk_adapt(g,m,b,tol/2,$<+1)
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
 c=$>(c)
 if hasdenom(c):
  c=$.(c)
 $! c
$, s_add(A,B):
 p=A[1]if ncmp(A[1],B[1])<0 $( B[1]
 d={}
 $) S in(A,B):
  $) k in S[0]:
   if ncmp(k,p)<0:
    d[k]=$](d.get(k,0),S[0][k])
 $?={}
 $) k in d:
  v=cs(d[k])
  if v!=0:
   $?[k]=v
 $!($?,p)
$, s_mul(A,B):
 vA=s_val(A)
 vB=s_val(B)
 p1=nadd(A[1],vB)
 p2=nadd(B[1],vA)
 p=p1 if ncmp(p1,p2)<0 $( p2
 d={}
 $) a in A[0]:
  $) b in B[0]:
   k=nadd(a,b)
   if ncmp(k,p)<0:
    d[k]=$](d.get(k,0),$:(A[0][a],B[0][b]))
 $?={}
 $) k in d:
  v=cs(d[k])
  if v!=0:
   $?[k]=v
 $!($?,p)
$, s_scale(A,c,shift=0):
 $?={}
 $) k in A[0]:
  v=cs($:(A[0][k],c))
  if v!=0:
   $?[nadd(k,shift)]=v
 $!($?,nadd(A[1],shift))
$, s_lead(A):
 if $- A[0]:
  $l $i()
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
 $) k in $+(1,$5(coefs)):
  P=s_mul(P,U)
  if $- P[0]:
   $T
  if coefs[k]!=0:
   res=s_add(res,s_scale(P,coefs[k]))
 $! res
$, nterms(U):
 v=s_val(U)
 if ncmp(v,0)<=0:
  $l $i()
 p=U[1]
 if ncmp(p,BIGP)>=0:
  $! 0 if $- U[0]$( 30
 n=nfloor(ndiv(p,v))+1
 if n>30:
  n=30
 $! n
$, s_pow(A,p):
 if $/(p)is $w $* p>=0:
  R=({0:1},BIGP)
  $) _ in $+(p):
   R=s_mul(R,A)
  $! R
 a,c,U=s_split(A)
 n=nterms(U)if U[0]$( 0
 coefs=[1]
 b=1
 $) k in $+(1,n+1):
  b=$:(b,$O($[(p,k-1),k))
  coefs.$%(b)
 S=s_powser(U,coefs)if U[0]$(({0:1},U[1])
 ap=$:(a,p)
 if $- $r(ap):
  $l $i()
 cp=pw(c,p)
 $! s_scale(S,cp,ap)
$, s_exp(A):
 neg_=[k $) k in A[0]if ncmp(k,0)<0]
 if neg_:
  $l $i()
 c0=A[0].get(0,0)
 U=(dict([(k,A[0][k])$) k in A[0]if k!=0]),A[1])
 shift=0
 if has(c0,LNT):
  cc=$X(c0,LNT)
  if cc is $# or $5(cc)!=2 or $- $r(cc[1]):
   $l $i()
  shift=cc[1]
  c0=cc[0]
 n=nterms(U)if U[0]$( 0
 coefs=[1]
 f=1
 $) k in $+(1,n+1):
  f=f*k
  coefs.$%(Q(1,f))
 S=s_powser(U,coefs)if U[0]$(({0:1},U[1])
 $! s_scale(S,pw('e',c0),shift)
$, s_ln(A):
 a,c,U=s_split(A)
 n=nterms(U)if U[0]$( 0
 coefs=[0]
 $) k in $+(1,n+1):
  coefs.$%(Q((-1)**(k+1),k))
 S=s_powser(U,coefs)if U[0]$(({},U[1])
 base=$](fn('ln',c),$:(a,LNT))
 $! s_add(S,(({0:base}if base!=0 $({}),BIGP))
$, s_fun($B,A):
 neg_=[k $) k in A[0]if ncmp(k,0)<0]
 if neg_:
  if $B=='$x':
   a,c=s_lead(A)
   sg=$S(c)
   sg=1 if($/(sg)is $- $1 $* sg>0)$(-1
   inv_=s_pow(A,-1)
   $! s_add(s_const($:(sg,$s,'pi')),s_scale(s_fun('$x',inv_),-1))
  if $B=='tanh':
   a,c=s_lead(A)
   $! s_const(1 if $S(c).$N>0 $(-1)
  $l $i()
 c0=A[0].get(0,0)
 if has(c0,LNT):
  $l $i()
 U=(dict([(k,A[0][k])$) k in A[0]if k!=0]),A[1])
 if $B=='$H' or $B=='sign':
  a,c=s_lead(A)
  v=$S($Q(c,LNT,-1000))if has(c,LNT)$( $S(c)
  if $/(v)is $1:
   $l $i()
  sg=1 if v>0 $(-1
  if $B=='sign':
   $! s_const(sg)
  $! s_scale(A,sg)
 if $B in('floor','ceiling','ipart','round','$w','fpart'):
  $l $i()
 n=nterms(U)if U[0]$( 0
 z='Z_'
 g=fn($B,z)
 coefs=[$Q(g,z,c0)]
 fact=1
 $) k in $+(1,n+1):
  g=diff(g,z)
  fact*=k
  coefs.$%(cs($O($Q(g,z,c0),fact)))
 $) cc in coefs:
  if has(cc,'$F')or cc=='$F' or has(cc,'$M'):
   $l $i()
 if $- U[0]:
  $! s_const(coefs[0])if $E $( $#
 $! s_powser(U,coefs)
$, ser(e,N):
 if $4(e,TV):
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
  if $4(p,TV):
   B=ser(b,N)
   if $r(p):
    $! trunc(s_pow(B,p),N)
   if $2(p)or $E:
    a,c,U=s_split(B)
    if a!=0:
     $l $i()
    $! trunc(s_pow(B,p),N)
  if $4(b,TV):
   $! trunc(s_exp(s_scale(ser(p,N),fn('ln',b))),N)
  $! trunc(s_exp(s_mul(ser(p,N),s_ln(ser(b,N)))),N)
 if h=='ln':
  $! trunc(s_ln(ser(e[1],N)),N)
 if h=='log':
  b=e[2]if $5(e)>2 $( 10
  $! trunc(s_scale(s_ln(ser(e[1],N)),pw(fn('ln',b),-1)),N)
 if $5(e)==2:
  $! trunc(s_fun(h,ser(e[1],N)),N)
 $l $i()
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
 cn=$X(n,LNT)
 cd=$X(d,LNT)
 if cn is $# or cd is $#:
  $l $i()
 p=$5(cn)-1
 q=$5(cd)-1
 if p<q:
  $! 0
 if p==q:
  $! $O(cn[p],cd[q])
 v=lnt_sign(c)
 if $/(v)is $1:
  $! '$F'
 $! '$M' if v>0 $(('*',-1,'$M')
$, lnt_sign(c):
 cc=$X(c,LNT)
 if cc is $#:
  v=$S($Q(c,LNT,-1e6))
  $! v
 k=$5(cc)-1
 lead=cc[k]
 v=$S(lead)
 if $/(v)is $1:
  $! v
 if k%2:
  v=-v
 $! v
$, $v(f,x,a,dirn=0):
 $! infnorm(limit0(f,x,a,dirn))
$, infnorm(r):
 if $&(r,'*')$*('$M' in r[1:]):
  c=$G([b $) b in r[1:]if b!='$M'])
  if $2(c):
   try:
    v=fv_(c)
    $! '$M' if v>0 $((('*',-1,'$M')if v<0 $( '$F')
   $9 $6:
    pass
 $! r
$, limit0(f,x,a,dirn=0):
 if $&(f,'$I')or $&(f,'mat'):
  $! mapexpr($7 g:$v(g,x,a,dirn),f)
 if $4(f,x):
  $! f
 if haswhen(f,x)$* $2(a)$* firstwhen_(f,x):
  $! whenlimit(f,x,a,dirn)
 if hashead(f,'fact')$* isinf(a):
  g=stirling(factnorm(f,x),x)
  if g!=f:
   $! $v(g,x,a,dirn)
 if $2(a):
  r=lim_bounded(f,x,a,dirn)
  if r is $- $#:
   $! r
 if a=='$M' or a==('*',-1,'$M'):
  sub_=pw(TV,-1)if a=='$M' $( $k(pw(TV,-1))
  $! lim_side(f,x,sub_,a)
 if dirn==0 $* $- has_disc(f):
  try:
   v=$Q(f,x,a)
   if v!='$F' $* $4(v,'$F')$* $- has(v,'$M'):
    v2=v
    if $2(v2):
     vv=$S(v2)
     if $/(vv)is $1 $* $H(vv.imag)>1e-12 $* $4(f,'i'):
      $l $U
    $! v
  $9($R,$D,$U,TypeError):
   pass
 if dirn==1:
  $! lim_side(f,x,$](a,TV),a)
 if dirn==-1:
  $! lim_side(f,x,$[(a,TV),a)
 r=lim_side(f,x,$](a,TV),a)
 l=lim_side(f,x,$[(a,TV),a)
 if r==l:
  $! r
 if $&(r,'$v')or $&(l,'$v'):
  $!('$v',f,x,a)
 try:
  if $2(r)$* $2(l)$* $- has(r,'$M')$* $- has(l,'$M'):
   if $H($S(r)-$S(l))<1e-12:
    $! r
 $9 $6:
  pass
 $! '$F'
$, hashead(f,h):
 if $/(f)is $- $0 or f[0]=='Q':
  $! $3
 $! f[0]==h or any([hashead(b,h)$) b in f[1:]])
STEPF=('floor','ceiling','fpart','ipart','$w','round')
$, factnorm(f,x):
 fs=[]
 $, walk(e):
  if $/(e)is $- $0 or e[0]=='Q':
   $!
  if e[0]=='fact' $* $- $4(e[1],x):
   fs.$%(e[1])
  $) b in e[1:]:
   walk(b)
 walk(f)
 if $- fs:
  $! f
 base=fs[0]
 $) u in fs:
  d=$[(base,u)
  if $j(d)$* d>0:
   base=u
 $, rep(e):
  if $/(e)is $- $0 or e[0]=='Q':
   $! e
  if e[0]=='fact' $* $- $4(e[1],x):
   k=$[(e[1],base)
   if $j(k)$* 0<k<=50:
    $! $G([$](base,j)$) j in $+(1,k+1)]+[fn('fact',base)])
   $! e
  $! simp((e[0],)+$0(rep(b)$) b in e[1:]))
 $! $.(rep(f))
$, stirling(f,x):
 if $/(f)is $- $0 or f[0]=='Q':
  $! f
 if f[0]=='fact' $* $- $4(f[1],x):
  u=stirling(f[1],x)
  $! $:($V($:(2,'pi',u)),pw($O(u,'e'),u))
 $! simp((f[0],)+$0(stirling(b,x)$) b in f[1:]))
$, bounded_nodes(f,x,a,dirn,$?):
 if $/(f)is $- $0 or f[0]=='Q':
  $!
 $) b in f[1:]:
  bounded_nodes(b,x,a,dirn,$?)
 if $5(f)==2 $* $- $4(f[1],x)$* f[0]in STEPF+('sin','cos'):
  try:
   L=$v(f[1],x,a,dirn)
  $9 $6:
   $!
  if L in('$M',('*',-1,'$M'))or L=='$F' or $&(L,'$v'):
   if(f,1)$- in $?:
    $?.$%((f,1))
  $K f[0]in STEPF $* $- isinf(a):
   if(f,0)$- in $?:
    $?.$%((f,0))
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
   $! r if r==l $( '$F'
  stp=[n $) n,k in ns if k==0]
  ns=[n $) n,k in ns if k==1]
  if stp:
   t=fv_(a)+dirn*1e-7*(1+$H(fv_(a)))
   g=f
   $) n in stp:
    try:
     g=replnode_(g,n,exactify($S(n,{x:t})))
    $9 $6:
     $! $#
   $! $v(g,x,a,dirn)
 $(:
  ns=[n $) n,k in ns]
 if $- ns:
  $! $#
 C='C_'
 reps=[]
 $) n in ns:
  if n[0]in('sin','cos'):
   reps.$%((n,C,(-1,0,1)))
  $K n[0]in('floor','$w','ipart'):
   reps.$%((n,$[(n[1],C),(0,Q(1,2),1)))
  $K n[0]=='ceiling':
   reps.$%((n,$](n[1],C),(0,Q(1,2),1)))
  $K n[0]=='round':
   reps.$%((n,$](n[1],C),(Q(-1,2),0,Q(1,2))))
  $(:
   reps.$%((n,C,(0,Q(1,2),1)))
 if $5(reps)>1:
  $! $#
 n,r,cs=reps[0]
 g=replnode_(f,n,r)
 $e=[]
 $) c in cs:
  v=$v($Q(g,C,c),x,a,dirn)
  if $&(v,'$v'):
   $! $#
  $e.$%(v)
 if $e[0]==$e[1]==$e[2]$* $e[0]!='$F':
  $! $e[0]
 $! '$F'
$, replnode_(f,w,r):
 if f==w:
  $! r
 if $/(f)is $- $0 or f[0]=='Q':
  $! f
 $! simp((f[0],)+$0(replnode_(b,w,r)$) b in f[1:]))
$, has_disc(f):
 if $/(f)is $- $0 or f[0]=='Q':
  $! $3
 if f[0]in('floor','ceiling','sign','ipart','round','fpart','$w','when','$H','mod'):
  $! $E
 $) a in f[1:]:
  if has_disc(a):
   $! $E
 $! $3
''')
_x(r'''$, lim_side(f,x,sub_,a):
 g=$Q(f,x,sub_)
 try:
  r=lead_t(g)
  if r is $#:
   $! 0
  al,c=r
  if has(c,TV):
   $l $i()
  if ncmp(al,0)>0:
   $! 0
  if has(c,LNT)$* al==0:
   $! lnt_lim(c)
  if has(c,LNT):
   v=lnt_sign(c)
   if $/(v)is $1:
    $! '$F'
   if v==0:
    $l $i()
   $! '$M' if v>0 $(('*',-1,'$M')
  if al==0:
   $! c
  if $- $2(c):
   $! $:(c,'$M')
  v=$S(c)
  if $/(v)is $1:
   $! '$F'
  $! '$M' if v>0 $(('*',-1,'$M')
 $9($i,$R,$D,$U,TypeError,$`):
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
  $! $;([lnexp(b)$) b in g[1:]])
 if h=='^':
  if g[1]=='e':
   $! g[2]
  $! $:(g[2],lnexp(g[1]))
 if $C(g)$* $_(g)>0:
  $! fn('ln',g)
 $! fn('ln',g)
$, lim_log(g,$<=0):
 if head(g)$- in('*','^'):
  $! $#
 v=$#
 $) t in(1e-3,1e-2,1e-1):
  try:
   v=$S(g,{TV:t})
  $9 $6:
   v=$#
  if v is $- $# $* $/(v)is $- $1 $* v==v $* v!=0 $* $H(v)!=$A('$M'):
   $T
  v=$#
 if v is $#:
  $! $#
 sg=1 if v>0 $(-1
 L=lim_val($.(lnexp($:(sg,g))),$<)
 if L is $# or $&(L,'$v')or L=='$F':
  $! $#
 if L=='$M':
  $! '$M' if sg>0 $(('*',-1,'$M')
 if L==('*',-1,'$M'):
  $! 0
 if $2(L):
  $! $:(sg,pw('e',L))
 $! $#
$, lim_val(g,$<):
 try:
  r=lead_t(g)
  if r is $#:
   $! 0
  al,c=r
  if has(c,TV):
   $l $i()
  if ncmp(al,0)>0:
   $! 0
  if has(c,LNT)$* al==0:
   $! lnt_lim(c)
  if has(c,LNT):
   v=lnt_sign(c)
   $! '$M' if v>0 $(('*',-1,'$M')
  if al==0:
   $! c
  v=$S(c)
  $! '$M' if v>0 $(('*',-1,'$M')
 $9($i,$R,$D,$U,TypeError,$`):
  pass
 r=lim_lh(g,$<+1)
 if r is $# $* $<<3:
  r=lim_log(g,$<+1)
 $! r
$, lim_lh(g,$<):
 if $<>4:
  $! $#
 if $4(g,TV):
  $! g
 h=head(g)
 if h=='^' $* $- $4(g[2],TV):
  L=lim_val($:(g[2],fn('ln',g[1])),$<)
  if L is $#:
   $! $#
  $! pw('e',L)
 if h=='^' $* $C(g[2]):
  L=lim_val(g[1],$<)
  if L is $#:
   $! $#
  if L==0 $* $_(g[2])<0:
   $! '$M'
  $! pw(L,g[2])
 if h=='*':
  nu,de=numer_denom(g)
  if de!=1:
   ln_=lim_val(nu,$<)
   ld=lim_val(de,$<)
   if ln_ is $# or ld is $#:
    $! $#
   if(ln_==0 $* ld==0)or(isinfv(ln_)$* isinfv(ld)):
    $! lim_val($.($O(diff(nu,TV),diff(de,TV))),$<)
   if ld==0:
    s=$S($Q(de,TV,1e-9))
    sn=$S(ln_)if $2(ln_)$* $- isinfv(ln_)$((1 if ln_=='$M' $(-1)
    $! '$M' if(s.$N if $/(s)is $1 $( s)*(sn.$N if $/(sn)is $1 $( sn)>0 $(('*',-1,'$M')
   $! $O(ln_,ld)
  ls=[lim_val(fct,$<)$) fct in g[1:]]
  if $# in ls:
   $! $#
  zero=[i $) i in $+($5(ls))if ls[i]==0]
  infs=[i $) i in $+($5(ls))if isinfv(ls[i])]
  if zero $* infs:
   r=lim_log(g,$<+1)
   if r is $- $#:
    $! r
   i=zero[0]
   j=infs[0]
   $d=$G([g[k+1]$) k in $+($5(ls))if k!=i $* k!=j])
   q=$O(g[i+1],pw(g[j+1],-1))
   r=lim_val(q,$<)
   if r is $#:
    $! $#
   $! $:(r,lim_val($d,$<))
  $! $G(ls)
 if h=='+':
  ls=[lim_val(t,$<)$) t in g[1:]]
  if $# in ls:
   $! $#
  r=$;(ls)
  if r!='$F':
   $! r
  ii=[k $) k in $+($5(ls))if isinfv(ls[k])]
  if $- ii:
   $! $#
  $) i in ii:
   A=g[i+1]
   $d=$;([g[k+1]$) k in $+($5(ls))if k!=i])
   q=lim_val($.($O($d,A)),$<)
   if q is $# or q=='$F' or isinfv(q)or q==-1:
    $8
   $! $:(ls[i],$](1,q))
  $! $#
 if $/(g)is $0 $* $5(g)==2:
  L=lim_val(g[1],$<)
  if L is $#:
   $! $#
  $! fn(h,L)
 $! $#
$, isinfv(v):
 $! v=='$M' or v==('*',-1,'$M')
$, lim_num(g,a):
 try:
  $e=[]
  $) k in $+(4,9):
   t=10.0**(-k)
   $e.$%($S(g,{TV:t}))
  v1=$e[-1]
  v2=$e[-2]
  if $/(v1)is $1 or $/(v2)is $1:
   $!('$v',g)
  if $H(v1)>1e12 $* $H(v1)>$H(v2):
   $! '$M' if v1>0 $(('*',-1,'$M')
  if $H(v1)<1e-6 $* $H(v1)<$H($e[-3])$* $H(v2)<$H($e[-3]):
   $! 0
  if $H(v1-v2)<1e-6*(1+$H(v1)):
   $! exactify_guess(v1)
 $9 $6:
  pass
 $!('$v',g)
$, exactify_guess(v):
 r=float2rat(v,1e-9)
 n,d=nd(r)
 if d<1000:
  $! r
 $! v
$, series_at(f,x,a,order):
 if a=='$M' or a==('*',-1,'$M'):
  sub_=pw(TV,-1)if a=='$M' $( $k(pw(TV,-1))
  back=pw(x,-1)if a=='$M' $( $k(pw(x,-1))
 $(:
  sub_=$](a,TV)
  back=$[(x,a)
 g=$Q(f,x,sub_)
 S=series_t(g,order)
 $! S,back
$, taylor(f,x,n,a=0):
 try:
  S,back=series_at(f,x,a,n)
 $9($i,$R,$D,$U):
  $! taylor_d(f,x,n,a)
 $L=[]
 $) k in S[0]:
  if ncmp(k,n)>0:
   $8
  if $-($/(k)is $w $* k>=0)or has(S[0][k],LNT):
   $!('taylor',f,x,n,a)
  $L.$%($:(S[0][k],pw(back,k)))
 $! $;($L)
$, taylor_d(f,x,n,a):
 $L=[]
 g=f
 fact=1
 $) k in $+(n+1):
  if k:
   fact*=k
   g=diff(g,x)
  v=$Q(g,x,a)
  if has(v,'$F')or v=='$F' or has(v,'$M'):
   $!('taylor',f,x,n,a)
  $L.$%($:($O(v,fact),pw($[(x,a),k)))
 $! $;($L)
$, series_cmd(f,x,n,a=0):
 try:
  S,back=series_at(f,x,a,n)
 $9($i,$R,$D,$U):
  $!('series',f,x,n,a)
 $L=[]
 lnback=fn('ln',back)if $-(a=='$M' or a==('*',-1,'$M'))$( $k(fn('ln',fn('$H',x)))
 $) k in S[0]:
  if ncmp(k,n)>0:
   $8
  c=$Q(S[0][k],LNT,lnback)
  $L.$%($:(c,pw(back,k)))
 $! $;($L)
''')
_x(r'''$, dominant(f,x,a=0):
 if a=='$M' or a==('*',-1,'$M'):
  sub_=pw(TV,-1)if a=='$M' $( $k(pw(TV,-1))
  back=pw(x,-1)if a=='$M' $( $k(pw(x,-1))
  lnback=$k(fn('ln',fn('$H',x)))
 $(:
  sub_=$](a,TV)
  back=$[(x,a)
  lnback=fn('ln',back)
 try:
  r=lead_t($Q(f,x,sub_))
 $9($i,$R,$D,$U):
  $!('dominantterm',f,x,a)
 if r is $#:
  $! 0
 k,c=r
 $! $:($Q(c,LNT,lnback),pw(back,k))
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
 $L=[]
 $) i in $+(j+1):
  $L.$%($:(binom(j+1,i),B[i],pw(n,j+1-i)))
 $! $:(Q(1,j+1),$;($L))
ZETA={2:('Q',1,6),4:('Q',1,90),6:('Q',1,945),8:('Q',1,9450),10:('Q',1,93555)}
$, sumseq(f,k,a,b):
 if $j(a)$* $j(b):
  if b<a-1:
   $! $k(sumseq(f,k,b+1,a-1))
  if b-a<=300:
   $L=[$Q(f,k,j)$) j in $+(a,b+1)]
   $! $;($L)
 if $4(f,k):
  $! $:(f,$]($[(b,a),1))
 cs_=$X(f,k)
 if cs_ is $- $# $* b!='$M':
  res=[]
  $) j in $+($5(cs_)):
   if cs_[j]!=0:
    if j==0:
     res.$%($:(cs_[0],$]($[(b,a),1)))
    $(:
     res.$%($:(cs_[j],$[(powsum(j,b),powsum(j,$[(a,1)))))
  $! $>($;(res))
 r=geomsum(f,k,a,b)
 if r is $- $#:
  $! r
 r=telesum(f,k,a,b)
 if r is $- $#:
  $! r
 if b=='$M' $* $j(a)$* has(f,('fact',k)):
  g=$:(f,('fact',k))
  gs=geomsum(g,k,0,'$M')if $3 $( $#
  cr=expsum(g,k)
  if cr is $- $#:
   C,r=cr
   tot=$:(C,pw('e',r))
   if a>0:
    tot=$[(tot,$;([$:(C,$O(pw(r,j),fact_(j)))$) j in $+(a)]))
   $! tot
 if b=='$M' $* $j(a):
  nu,de=numer_denom(f)
  if $4(nu,k):
   dd=$X(de,k)
   if dd is $- $# $* $5(dd)>=2 $* all([c==0 $) c in dd[:-1]]):
    p=$5(dd)-1
    if p==1:
     $! '$M' if $S($O(nu,dd[-1])).$N>0 $(('*',-1,'$M')
    if p in ZETA $* a>=1:
     z=$:(ZETA[p],pw('pi',p))
     z=$[(z,$;([pw(j,-p)$) j in $+(1,a)]))
     $! $:($O(nu,dd[-1]),z)
 if($j(a)or $2(a))$*(b=='$M' or $j(b))$* freeofall(f,[s $) s in $q(f)if s!=k]):
  $! nsum(f,k,a,b)
 $!('sumseq',f,k,a,b)
$, expsum(g,k):
 if $4(g,k):
  $! g,1
 fs=g[1:]if $&(g,'*')$((g,)
 C=[]
 r=$#
 $) h in fs:
  if $4(h,k):
   C.$%(h)
  $K $&(h,'^')$* $4(h[1],k)$* h[2]==k $* r is $#:
   r=h[1]
  $K $&(h,'^')$* $4(h[1],k)$* $g(h[2],k)$* $g(h[2],k)[1]==0 $* r is $#:
   r=pw(h[1],$g(h[2],k)[0])
  $(:
   $! $#
 if r is $#:
  $! $#
 $! $G(C),r
$, geomsum(f,k,a,b):
 fs=f[1:]if $&(f,'*')$((f,)
 C=[]
 base=$#
 ex=$#
 $) g in fs:
  if $4(g,k):
   C.$%(g)
  $K $&(g,'^')$* $4(g[1],k)$* $g(g[2],k):
   if base is $- $#:
    if g[1]==base or($C(g[1])$* $C(base)):
     lp=$g(g[2],k)
     lb=$g(ex,k)
     if lp[0]==1 $* lb[0]==1:
      C.$%(pw(g[1],lp[1]))
      C.$%(pw(base,lb[1]))
      base=$:(base,g[1])
      ex=k
      $8
    $! $#
   base=g[1]
   ex=g[2]
  $(:
   $! $#
 if base is $#:
  $! $#
 p,q=$g(ex,k)
 r=pw(base,p)
 Cq=$:($G(C),pw(base,q))
 if b=='$M':
  if $2(r):
   v=$S(r)
   if $H(v)<1:
    $! $O($:(Cq,pw(r,a)),$[(1,r))
   $! '$M' if $S(Cq).$N>0 $* v.$N>0 $( '$F'
  $! $#
 if r==1:
  $! $:(Cq,$]($[(b,a),1))
 $! $O($:(Cq,$[(pw(r,$](b,1)),pw(r,a))),$[(r,1))
$, telesum(f,k,a,b):
 if $- hasdenom(f):
  $! $#
 pf=partfrac(f,k)
 if pf is $#:
  $! $#
 $L=pf[1:]if $&(pf,'+')$((pf,)
 groups=[]
 $) t in $L:
  c,r=$a(t)
  if $&(r,'^')$* r[2]==-1:
   lb=$g(r[1],k)
   if lb is $# or lb[0]!=1:
    $! $#
   groups.$%((c,lb[1]))
  $K $4(t,k):
   $! $#
  $(:
   $! $#
 if $- groups:
  $! $#
 s0=groups[0][1]
 tot=0
 ms=[]
 $) c,s in groups:
  m=nsub(s,s0)if $r(s)$* $r(s0)$( $#
  if m is $# or $- $j(m):
   $! $#
  ms.$%(m)
  tot=$](tot,c)
 if tot!=0:
  if b=='$M':
   $! '$M'
  $! $#
 mn=min(ms)
 if mn!=0:
  s0=nadd(s0,mn)
  ms=[m-mn $) m in ms]
 M=max(ms)
 res=[]
 $) idx in $+($5(groups)):
  c=groups[idx][0]
  m=ms[idx]
  part=[]
  $) j in $+(m,M):
   part.$%(pw($](a,j,s0),-1))
  if b!='$M':
   $) j in $+(1,m+1):
    part.$%(pw($](b,j,s0),-1))
  res.$%($:(c,$;(part)))
 $! $;(res)
$, nsum(f,k,a,b):
 av=$w(nreal(a))
 if b=='$M':
  $! nsum_inf(f,k,av)
 s=0.0
 $) n in $+(av,$w(b)+1):
  s+=$S(f,{k:$A(n)})
 $! s
''')
_x(r'''$, nsum_inf(f,k,av):
 L=$v(f,k,'$M')
 if L!=0 $* $- $&(L,'$v'):
  if L=='$F' or $- $2(L):
   $! '$F'
  try:
   v=fv_(L)
  $9 $6:
   $! '$F'
  $! '$M' if v>0 $(('*',-1,'$M')
 $, t(n):
  z=$S(f,{k:$A(n)})
  if $/(z)is $1:
   if $H(z.imag)>1e-12*(1+$H(z.$N)):
    $l $U
   z=z.$N
  $! z
 first=[t(n)$) n in $+(av,av+40)]
 tail=first[10:]
 if all([tail[i]*tail[i+1]<0 $) i in $+($5(tail)-1)]):
  S=[]
  s_=0.0
  $) n in $+(av,av+60):
   s_+=t(n)
   S.$%(s_)
  e1=wynn(S)
  e2=wynn(S[:-10])
  if $H(e1-e2)>1e-8*max(1.0,$H(e1)):
   err('Questionable accuracy: the series may diverge')
  $! e1
 N=av+200
 tn=[t(n)$) n in $+(N,N+20)]
 if all([v>0 $) v in tn])or all([v<0 $) v in tn]):
  try:
   fe=exactify(f)
  $9 $6:
   fe=f
  I=defint(fe,k,N,'$M')
  if I in('$M',('*',-1,'$M')):
   $! I
  if $- $2(I)or has(I,'$F'):
   I=nint(f,k,N,'$M')
  s_=0.0
  $) n in $+(av,N):
   s_+=t(n)
  d1=diff(f,k)
  d3=diff(diff(d1,k),k)
  s_+=fv_(I)+t(N)/2-fv_($Q(d1,k,N))/12+fv_($Q(d3,k,N))/720
  $! s_
 s_=0.0
 prev=$#
 $) n in $+(av,av+20000):
  s_+=t(n)
  if n-av in(9999,19999):
   if prev is $- $# $* $H(s_-prev)>1e-9*max(1.0,$H(s_)):
    err('Questionable accuracy: the series may diverge')
   prev=s_
 $! s_
$, prodseq(f,k,a,b):
 if $j(a)$* $j(b):
  if b<a-1:
   $! pw(prodseq(f,k,b+1,a-1),-1)
  if b-a<=300:
   $! $G([$Q(f,k,j)$) j in $+(a,b+1)])
 if $4(f,k):
  $! pw(f,$]($[(b,a),1))
 if f==k $* a==1:
  $! fn('fact',b)
 if $&(f,'^')$* f[1]==k $* $j(f[2])$* a==1:
  $! pw(fn('fact',b),f[2])
 if $&(f,'*')$* a==1:
  c=[g $) g in f[1:]if $4(g,k)]
  r=[g $) g in f[1:]if $- $4(g,k)]
  if c $* $5(r)==1:
   rr=prodseq(r[0],k,a,b)
   if $- $&(rr,'prodseq'):
    $! $:(pw($G(c),b),rr)
 fs=f[1:]if $&(f,'*')$((f,)
 if $&(f,'^')$* $4(f[1],k):
  $! pw(f[1],sumseq(f[2],k,a,b))
 $!('prodseq',f,k,a,b)
$, texpand(e):
 if $/(e)is $- $0 or e[0]=='Q':
  $! e
 $Y=[texpand(a)$) a in e[1:]]
 e=simp((e[0],)+$0($Y))
 if $/(e)is $- $0:
  $! e
 h=e[0]
 if h in('sin','cos','tan')$* $5(e)==2:
  u=e[1]
  if h=='tan':
   $! texpand($O(fn('sin',u),fn('cos',u)))
  if $&(u,'+'):
   a=u[1]
   b=$;($I(u[2:]))
   sa,ca=texpand(fn('sin',a)),texpand(fn('cos',a))
   sb,cb=texpand(fn('sin',b)),texpand(fn('cos',b))
   if h=='sin':
    $! $>($]($:(sa,cb),$:(ca,sb)))
   $! $>($[($:(ca,cb),$:(sa,sb)))
  c,r=$a(u)
  if $j(c)$* c>1 $* c<=30:
   s1=texpand(fn('sin',r))
   c1=texpand(fn('cos',r))
   z=expand_pow($](c1,$:('i',s1)),c)
   re_,im_=reim(z)
   $! $>(im_ if h=='sin' $( re_)
 $! e
$, trigfactor(f):
 if head(f)in('sin','cos')$* $5(f)==2:
  $![(f[0],f[1])]
 if $&(f,'^')$* head(f[1])in('sin','cos')$* $j(f[2])$* f[2]>0:
  $![(f[1][0],f[1][1])]*f[2]
 $! $#
$, tmul(a,b):
 n1,u=a
 n2,v=b
 if n1=='sin' $* n2=='sin':
  $! $:($s,$[(fn('cos',$[(u,v)),fn('cos',$](u,v))))
 if n1=='cos' $* n2=='cos':
  $! $:($s,$](fn('cos',$[(u,v)),fn('cos',$](u,v))))
 if n1=='cos':
  u,v=v,u
 $! $:($s,$](fn('sin',$](u,v)),fn('sin',$[(u,v))))
$, tcollect(e):
 if $/(e)is $- $0 or e[0]=='Q':
  $! e
 e=$>(e)
 if $&(e,'+'):
  $! $;([tcollect_term(t)$) t in e[1:]])
 $! tcollect_term(e)
$, tcollect_term(t):
 fs=t[1:]if $&(t,'*')$((t,)
 other=[]
 trig=[]
 $) f in fs:
  tf=trigfactor(f)
  if tf is $#:
   other.$%(f)
  $(:
   trig.extend(tf)
 if $5(trig)<=1:
  $! t
 acc=fn(trig[0][0],trig[0][1])
 $) tf in trig[1:]:
  $L=acc[1:]if $&(acc,'+')$((acc,)
  $?=[]
  $) term in $L:
   c,r=$a(term)
   ftf=trigfactor(r)
   if ftf is $# or $5(ftf)!=1:
    if freeof_trig(r):
     $?.$%($:(term,fn(tf[0],tf[1])))
     $8
    $?.$%($:(term,fn(tf[0],tf[1])))
    $8
   $?.$%($:(c,tmul(ftf[0],tf)))
  acc=$>($;($?))
 $! $>($:($G(other),acc))
$, trigargs(e,$?):
 if $/(e)is $- $0 or e[0]=='Q':
  $!
 if e[0]in('sin','cos')$* $5(e)==2:
  if e[1]$- in $?:
   $?.$%(e[1])
 $) a in e[1:]:
  trigargs(a,$?)
$, pyth(e):
 us=[]
 trigargs(e,us)
 if $- us:
  $! e
 $z=e
 bl=$5(fmt(e))
 $) u in us:
  s=fn('sin',u)
  c=fn('cos',u)
  $) a,b in((s,c),(c,s)):
   g=rsquare(e,a,b)
   if g is $- $#:
    g=$>(g)
    l=$5(fmt(g))
    if l<bl:
     $z=g
     bl=l
 $! $z
$, rsquare(e,a,b):
 if $/(e)is $- $0 or e[0]=='Q':
  $! e
 if e[0]=='^' $* e[1]==a $* $j(e[2])$* e[2]>=2:
  $! $:(pw(a,e[2]-2),$[(1,pw(b,2)))
 $! simp((e[0],)+$0(rsquare(t,a,b)$) t in e[1:]))
$, freeof_trig(e):
 $! $- hastrig(e)
$, arclen(f,x,a,b):
 g=$.($>($](1,pw(diff(f,x),2))))
 $! defint($V(g),x,a,b)
$, tangentline(f,x,a):
 d=$Q(diff(f,x),x,a)
 $! $>($]($Q(f,x,a),$:(d,$[(x,a))))
$, normalline(f,x,a):
 d=$Q(diff(f,x),x,a)
 if d==0:
  $!('=',x,a)
 $! $>($[($Q(f,x,a),$O($[(x,a),d)))
$, impdif(eq,x,y,n=1):
 F=$[(eq[1],eq[2])if $&(eq,'=')$( eq
 yp=$.($k($O(diff(F,x),diff(F,y))))
 d=yp
 $) _ in $+(n-1):
  d=$.($](diff(d,x),$:(diff(d,y),yp)))
 $! nice(d)
$, avgrc(f,x,v,h=Q(1,1000)):
 $! $O($[($Q(f,x,$](v,h)),$Q(f,x,v)),h)
$, centraldiff(f,x,v,h=Q(1,1000)):
 $! $O($[($Q(f,x,$](v,h)),$Q(f,x,$[(v,h))),$:(2,h))
$, untan(e):
 if $/(e)is $- $0 or e[0]=='Q':
  $! e
 $Y=[untan(a)$) a in e[1:]]
 if e[0]=='tan' $* $5($Y)==1:
  $! $O(fn('sin',$Y[0]),fn('cos',$Y[0]))
 $! simp((e[0],)+$0($Y))
$, pyth_to(e,which):
 other='cos' if which=='sin' $( 'sin'
 e=untan(e)
 us=[]
 trigargs(e,us)
 $) u in us:
  e=rsquare(e,fn(other,u),fn(which,u))
 $! $>(e)
''')
_x(r'''$, unhold(e):
 if $&(e,'hold'):
  $! simp(e[1])
 $! e
$, $t(e):
 if $- $2(e):
  $! $3
 try:
  v=$S(e)
 $9 $6:
  $! $3
 if $/(v)is $1:
  $! $H(v.imag)<=1e-10*(1+$H(v.$N))
 $! v==v
$, fv(e):
 v=$S(e)
 if $/(v)is $1:
  $! v.$N
 $! v
$, clean(e):
 e=$.(e)
 if $^(e):
  e=evalf(e)
  if has(e,'i'):
   r,i=reim(e)
   if $/(i)is $A $* $H(i)<1e-11*(1+$H(tofl(r)if $C(r)$( 1)):
    e=r
 $! e
class Sols:
 $, __init__($=):
  $=.$e=[]
  $=.all=$3
  $=.fail=$3
  $=.ints=[]
$, $m(f,x,$@=$3,$<=0):
 if $<>6:
  $! $#
 f=$.(unhold(f))
 if $4(f,x):
  if f==0:
   $! 'all'
  if $2(f)or $- $@:
   $![]
  $![]
 nu=numer_of(f)
 if $4(nu,x):
  $![]if nu!=0 $( 'all'
 if $- $@ $* firstabs(nu,x)is $- $# $* $<<4:
  r=abs_cases(nu,x,[],$<)
  if r is $- $# $* r!='interval':
   $![q $) q in r if valid(f,x,q,$@)]
 $f=solve_num(nu,x,$@,$<)
 numeric=$f is $# or($f!='all' $* any([$^(q)$) q in $f]))
 if numeric $* hastrigx(nu,x)$* $<<3:
  try:
   g=tcollect(nu)
  $9 $6:
   g=nu
  if g!=nu:
   s2=$m(g,x,$@,$<+2)
   if s2 is $- $# $* s2!='all' $* $- any([$^(q)$) q in s2]):
    $f=s2
 if $f is $# or $f=='all':
  $! $f
 $?=[]
 $) s in $f:
  if valid(f,x,s,$@):
   $?.$%(s)
 $! $?
$, numer_of(f):
 try:
  c=comdenom(f)
 $9 $6:
  c=f
 $! numer_denom(c)[0]
$, valid(f,x,s,$@):
 if has(s,'n1')or $q(s)$* $- $2(s):
  $! $E
 try:
  v=$Q(f,x,s)
  if v=='$F' or has(v,'$F'):
   $! $3
  if has(v,'$M'):
   $! $3
  vv=$S(v)
  mag=1.0
  if $/(vv)is $1:
   ok=$H(vv)<1e-6
  $(:
   ok=$H(vv)<1e-6
  if $- ok:
   try:
    sc=$S(s)
    ok=$H(vv)<1e-8*(1+$H(sc))*1e4
   $9 $6:
    ok=$3
  if $- $@:
   sv=$S(s)
   if $/(sv)is $1 $* $H(sv.imag)>1e-9*(1+$H(sv.$N)):
    $! $3
  $! ok
 $9($R,$D,$U,TypeError,$`):
  $! $3
$, solve_num(nu,x,$@,$<):
 d=degree(nu,x)
 if d is $- $#:
  r=solve_poly(nu,x,$@)
  if r is $- $#:
   $! r
 fac=factor_expr(nu)
 fac=fac[1]if $&(fac,'hold')$( fac
 if $&(fac,'*'):
  allsol=[]
  $) g in fac[1:]:
   if $&(g,'^')$* $C(g[2])$* $_(g[2])>0:
    g=g[1]
   if $4(g,x):
    $8
   r=$m(g,x,$@,$<+1)
   if r is $#:
    $! numeric_solve(nu,x,$@)
   if r=='all':
    $! 'all'
   allsol.extend(r)
  $! dedup(allsol)
 if $&(fac,'^')$* $C(fac[2])$* $_(fac[2])>0:
  $! $m(fac[1],x,$@,$<+1)
 r=isolate(nu,0,x,$@,$<)
 if r is $- $#:
  $! r
 r=radical_solve(nu,x,$@,$<)
 if r is $- $#:
  $! r
 r=explog_solve(nu,x,$@,$<)
 if r is $- $#:
  $! r
 r=ln_solve(nu,x,$@,$<)
 if r is $- $#:
  $! r
 r=kernel_solve(nu,x,$@,$<)
 if r is $- $#:
  $! r
 if hastrigx(nu,x):
  g=texpand(nu)
  if g!=nu:
   r=kernel_solve(g,x,$@,$<+1)
   if r is $#:
    fg=factor_expr(g)
    fg=fg[1]if $&(fg,'hold')$( fg
    if $&(fg,'*'):
     $! solve_num(g,x,$@,$<+1)
   if r is $- $#:
    $! r
  r=trig_lin(nu,x,$@)
  if r is $- $#:
   $! r
 $! numeric_solve(nu,x,$@)
$, radical_solve(nu,x,$@,$<):
 ks=[]
 xkernels(nu,x,ks)
 if $- ks:
  $! $#
 $) k in ks:
  if $-($&(k,'^')$* isq(k[2])$* k[2][1]==1):
   $! $#
 if $5(ks)>1:
  if $<>4 or $5(ks)>3:
   $! $#
  $) k in ks:
   if k[2]!=$s:
    $! $#
  k=ks[0]
  W='W_'
  g=$>($Q(nu,k,W))
  cs_=$X(g,W)
  if cs_ is $# or $5(cs_)!=2:
   $! $#
  A,B=cs_
  g2=$>($[(pw(A,2),$:(pw(B,2),k[1])))
  rs=$m(g2,x,$@,$<+1)
  if rs is $# or rs=='all':
   $! $#
  $![r $) r in rs if valid(nu,x,r,$@)]
 k=ks[0]
 base=k[1]
 q=k[2][2]
 W='W_'
 g=$>($Q(nu,k,W))
 cs_=$X(g,W)
 if cs_ is $# or $5(cs_)!=2 or has(cs_[0],W):
  $! $#
 A,B=cs_
 if degree(A,x)is $# or degree(B,x)is $# or degree(base,x)is $#:
  $! $#
 poly=$>($[(pw($k(A),q),$:(pw(B,q),base)))
 rs=solve_poly(poly,x,$@)
 if rs is $# or rs=='all':
  $! $#
 $?=[]
 $) r in rs:
  if valid(nu,x,r,$@):
   $?.$%(r)
 $! $?
$, expterm(t,x):
 fs=t[1:]if $&(t,'*')$((t,)
 c=[]
 L=[]
 $) f in fs:
  if $4(f,x):
   c.$%(f)
  $K $&(f,'^')$* $4(f[1],x)$* $g(f[2],x)is $- $# $* $t(f[1])$* fv(f[1])>0:
   L.$%($:(f[2],fn('ln',f[1]))if f[1]!='e' $( f[2])
  $(:
   $! $#
 $! $G(c),$;(L)
$, explog_solve(nu,x,$@,$<):
 if $- $&(nu,'+'):
  $! $#
 dep=[t $) t in nu[1:]if $- $4(t,x)]
 ind=$;([t $) t in nu[1:]if $4(t,x)])
 if $5(dep)==2 $* ind==0:
  A=expterm(dep[0],x)
  B=expterm(dep[1],x)
  if A is $# or B is $#:
   $! $#
  r=$.($k($O(B[0],A[0])))
  if $t(r)$* fv(r)<=0 $* $- $@:
   $![]
  eq=$>($[(A[1],$](B[1],fn('ln',r))))
  lx=$g(eq,x)
  if lx is $#:
   $! $#
  $![nice($.($k($O(lx[1],lx[0]))))]
 $! $#
''')
_x(r'''$, ln_solve(nu,x,$@,$<):
 $L=nu[1:]if $&(nu,'+')$((nu,)
 lns=[]
 $d=[]
 $) t in $L:
  c,r=$a(t)
  if $&(r,'log')$* $5(r)==3:
   c=$O(c,fn('ln',r[2]))
   r=('ln',r[1])
  if $&(r,'ln')$* $r(c)$* $- $4(r,x):
   lns.$%((c,r[1]))
  $K $4(t,x):
   $d.$%(t)
  $K $&(r,'ln')$* $2(c)$* $- $4(r,x):
   lns.$%((c,r[1]))
  $(:
   $! $#
 if $5(lns)<2 $* $-($5(lns)==1 $* $d):
  $! $#
 k=rest_k=$;($d)
 c0=lns[0][0]
 if all([c==c0 $) c,u in lns]):
  P=$G([u $) c,u in lns])
  rhs=pw('e',$.($k($O(rest_k,c0))))
 $K all([$r(c)$) c,u in lns]):
  P=$G([pw(u,c)$) c,u in lns])
  rhs=pw('e',$k(rest_k))
 $(:
  $! $#
 rs=$m($[(P,rhs),x,$@,$<+1)
 if rs is $# or rs=='all':
  $! rs
 $?=[]
 $) r in rs:
  if valid(nu,x,r,$@):
   $?.$%(r)
 $! $?
$, hastrigx(e,x):
 if $/(e)is $- $0 or e[0]=='Q':
  $! $3
 if e[0]in('sin','cos','tan')$* has(e,x):
  $! $E
 $) a in e[1:]:
  if hastrigx(a,x):
   $! $E
 $! $3
$, dedup($f):
 $?=[]
 $) s in $f:
  if s $- in $?:
   dup=$3
   $) t in $?:
    try:
     if $2(s)$* $2(t)$* $H($S(s)-$S(t))<1e-12*(1+$H($S(s))):
      dup=$E
      $T
    $9 $6:
     pass
   if $- dup:
    $?.$%(s)
 $! $?
$, sortsols($f):
 $, key(s):
  t=s
  $) w in $q(s):
   if w[0]=='n' $* w[1:].isdigit():
    t=$Q(t,w,0)
  try:
   v=$S(t)
   if $/(v)is $1:
    $!(1,v.$N,v.imag,okey(s))
   $!(0,v,0.0,okey(s))
  $9 $6:
   $!(2,0.0,0.0,okey(s))
 $! sorted($f,key=key)
$, solve_poly(p,x,$@):
 cs=$X(p,x)
 if cs is $#:
  $! $#
 $J cs $* cs[-1]==0:
  cs.pop()
 n=$5(cs)-1
 if n<=0:
  $![]if cs $* cs[0]!=0 $( 'all'
 $f=[]
 k=0
 $J cs[k]==0:
  k+=1
 if k:
  $f.$%(0)
  cs=cs[k:]
  n=$5(cs)-1
 if n==0:
  $! $f
 allrat=$E
 anyfl=$3
 $) c in cs:
  if $- $r(c):
   allrat=$3
  if $^(c):
   anyfl=$E
 if anyfl $* all([$2(c)$) c in cs]):
  $! $f+numroots(cs,$@)
 if allrat:
  cc,fs=ufactor(cs)
  $) g,m in fs:
   $f.extend(solve_small(g,x,$@))
  $! dedup($f)
 if n==1:
  $! $f+[$.($k($O(cs[0],cs[1])))]
 if n==2:
  $! $f+quad(cs[2],cs[1],cs[0],$@)
 fac=factor_expr(p,x)
 fac=fac[1]if $&(fac,'hold')$( fac
 if $&(fac,'*'):
  $) g in fac[1:]:
   if $&(g,'^')$* $C(g[2]):
    g=g[1]
   if $4(g,x):
    $8
   dg=degree(g,x)
   if dg is $- $# $* dg<n:
    r=solve_poly(g,x,$@)
    if r is $#:
     $! $#
    $f.extend(r)
   $(:
    $! $#
  $! dedup($f)
 r=solve_binom(cs,x,$@)
 if r is $- $#:
  $! $f+r
 if all([$2(c)$) c in cs]):
  $! $f+numroots(cs,$@)
 $! $#
$, quad(a,b,c,$@):
 D=$.($>($[($:(b,b),$:(4,a,c))))
 if $t(D)$* $- $@:
  if fv(D)<0:
   $![]
 if D==0:
  $![$.($O($k(b),$:(2,a)))]
 s=$V(D)
 r1=$.($O($[($k(b),s),$:(2,a)))
 r2=$.($O($]($k(b),s),$:(2,a)))
 if $2(r1):
  r1=$>(r1)
  r2=$>(r2)
 $![r1,r2]
$, solve_small(g,x,$@):
 n=$5(g)-1
 if n==1:
  $![Q(-g[0],g[1])]
 if n==2:
  $! quad(g[2],g[1],g[0],$@)
 r=solve_binom(g,x,$@)
 if r is $- $#:
  $! r
 if n==3:
  r=cardano(g,$@)
  if r is $- $#:
   if $5(fmt(r[0]))<=32:
    $! r
 $! numroots(g,$@)
$, solve_binom(cs,x,$@):
 n=$5(cs)-1
 m=0
 $) i in $+(1,n+1):
  if cs[i]!=0:
   m=igcd(m,i)
 if m<=1:
  $! $#
 sub_cs=[cs[i]$) i in $+(0,n+1,m)]
 if $5(sub_cs)-1>2 $* $-($5([c $) c in sub_cs if c!=0])==2):
  $! $#
 u='U_'
 if $5(sub_cs)==2:
  roots_u=[$.($k($O(sub_cs[0],sub_cs[1])))]
 $(:
  roots_u=solve_poly(fromcoeffs(sub_cs,u),u,$@)
  if roots_u is $#:
   $! $#
 $?=[]
 $) r in roots_u:
  $?.extend(nthroots(r,m,$@))
 $! dedup($?)
$, nthroots(r,m,$@):
 if $- $@:
  if $t(r):
   v=fv(r)
   if m%2==1:
    if v<0:
     $![$k(pw($k(r),Q(1,m)))]
    $![pw(r,Q(1,m))]
   if v<0:
    $![]
   if v==0:
    $![0]
   rt=pw(r,Q(1,m))
   $![$k(rt),rt]
  if m%2==1:
   $![pw(r,Q(1,m))]
  rt=pw(r,Q(1,m))
  $![$k(rt),rt]
 if $2(r):
  v=$S(r)
  mod=fn('$H',r)
  ang=fn('$p',r)
  $?=[]
  $) k in $+(m):
   th=$O($](ang,$:(2*k,'pi')),m)
   z=$:(pw(mod,Q(1,m)),$](fn('cos',th),$:('i',fn('sin',th))))
   z=$>(z)
   $?.$%(z)
  $! $?
 rt=pw(r,Q(1,m))
 $![$:(rt,pw('e',$O($:(2*k,'i','pi'),m)))$) k in $+(m)]
$, cardano(g,$@):
 d,c,b,a=[Q(v)if $/(v)is $w $( v $) v in g]
 p=$O($[($:(3,a,c),$:(b,b)),$:(3,a,a))
 q=$O($]($:(2,pw(b,3)),$:(-9,a,b,c),$:(27,a,a,d)),$:(27,pw(a,3)))
 disc=$]($O(pw(q,2),4),$O(pw(p,3),27))
 if $- $r(disc)or $_(disc)<=0:
  $! $#
 s=$V(disc)
 u=$]($k($O(q,2)),s)
 v=$[($k($O(q,2)),s)
 $, cbrt(w):
  wv=fv(w)
  if wv<0:
   $! $k(pw($k(w),Q(1,3)))
  $! pw(w,Q(1,3))
 t=$](cbrt(u),cbrt(v))
 root=$[(t,$O(b,$:(3,a)))
 if $- $@:
  $![root]
 $![root]+[clean(r)$) r in numroots_after(g,root)]
$, numroots_after(g,root):
 rv=fv(root)
 rs=aberth(g)
 $![fromcomplex(z)$) z in rs if $H(z-rv)>1e-6]
$, numroots(cs,$@):
 rs=aberth([evalf(c)if $- $C(c)$( c $) c in cs])
 $?=[]
 $) z in rs:
  if $H(z.imag)<1e-9*(1+$H(z.$N)):
   $?.$%($A(z.$N))
  $K $@:
   $?.$%(fromcomplex(z))
 $! $?
NC=[0]
$, newint():
 NC[0]+=1
 $! 'n'+${(NC[0])
''')
_x(r'''$, isolate(lhs,rhs,x,$@,$<):
 if $<>12:
  $! $#
 if lhs==x:
  $![rhs]
 if $4(lhs,x):
  $! 'all' if $.($[(lhs,rhs))==0 $([]
 h=head(lhs)
 if h=='+':
  dep=[t $) t in lhs[1:]if $- $4(t,x)]
  ind=[t $) t in lhs[1:]if $4(t,x)]
  if $5(dep)==1:
   $! isolate(dep[0],$[(rhs,$;(ind)),x,$@,$<+1)
  $! $#
 if h=='*':
  dep=[t $) t in lhs[1:]if $- $4(t,x)]
  ind=[t $) t in lhs[1:]if $4(t,x)]
  if $5(dep)==1:
   c=$G(ind)
   r=$O(rhs,c)
   if $2(c)$* $&(rhs,'+'):
    r=$>(r)
   $! isolate(dep[0],r,x,$@,$<+1)
  $! $#
 if h=='^':
  b,p=lhs[1],lhs[2]
  if $4(p,x):
   if p==-1 or($C(p)$* $_(p)<0):
    if rhs==0:
     $![]
    $! isolate(pw(b,nneg(p)),pw(rhs,-1),x,$@,$<+1)
   if $/(p)is $w:
    $?=[]
    $) r in nthroots(rhs,p,$@):
     rr=isolate(b,r,x,$@,$<+1)
     if rr is $#:
      $! $#
     if rr=='all':
      $! 'all'
     $?.extend(rr)
    $! $?
   if isq(p):
    pn,pd=p[1],p[2]
    if pd%2==0 $* $- $@ $* $t(rhs)$* fv(rhs)<0:
     $![]
    $! isolate(pw(b,pn),pw(rhs,pd),x,$@,$<+1)
   $! isolate(b,pw(rhs,pw(p,-1)),x,$@,$<+1)
  if $4(b,x):
   if rhs==0:
    $![]
   if $- $@ $* $t(rhs)$* fv(rhs)<0 $* $t(b)$* fv(b)>0:
    $![]
   if b=='e':
    $! isolate(p,fn('ln',rhs),x,$@,$<+1)
   if $C(b)$* $2(rhs):
    $! isolate(p,fn('log',rhs,b),x,$@,$<+1)
   $! isolate(p,$O(fn('ln',rhs),fn('ln',b)),x,$@,$<+1)
  $! $#
 if $/(lhs)is $0 $* $5(lhs)>=2:
  u=lhs[1]
  if $- all([$4(a,x)$) a in lhs[2:]]):
   $! $#
  rs=invfun(h,lhs,rhs,$@)
  if rs is $#:
   $! $#
  $?=[]
  $) r in rs:
   rr=isolate(u,r,x,$@,$<+1)
   if rr is $#:
    $! $#
   if rr=='all':
    $! 'all'
   $?.extend(rr)
  $! $?
 $! $#
$, invfun(h,lhs,r,$@):
 rv=$#
 if $t(r):
  rv=fv(r)
 if h=='ln':
  $![pw('e',r)]
 if h=='log':
  b=lhs[2]if $5(lhs)>2 $( 10
  $![pw(b,r)]
 if h=='$H':
  if rv is $- $#:
   if rv<0:
    $![]
   if rv==0:
    $![0]
  $![$k(r),r]
 if h=='$V':
  $![pw(r,2)]
 if h=='sin':
  if rv is $- $# $* $H(rv)>1 $* $- $@:
   $![]
  n=newint()
  if r==0:
   $![$:(n,'pi')]
  a=fn('$~',r)
  if r==1 or r==-1:
   $![$](a,$:(2,n,'pi'))]
  $![$](a,$:(2,n,'pi')),$]($[('pi',a),$:(2,n,'pi'))]
 if h=='cos':
  if rv is $- $# $* $H(rv)>1 $* $- $@:
   $![]
  n=newint()
  if r==0:
   $![$]($:($s,'pi'),$:(n,'pi'))]
  a=fn('arccos',r)
  if r==1 or r==-1:
   $![$](a,$:(2,n,'pi'))]
  $![$](a,$:(2,n,'pi')),$]($k(a),$:(2,n,'pi'))]
 if h=='tan':
  n=newint()
  $![$](fn('$x',r),$:(n,'pi'))]
 if h=='$~':
  if rv is $- $# $* $H(rv)>$W.pi/2+1e-12:
   $![]
  $![fn('sin',r)]
 if h=='arccos':
  if rv is $- $# $*(rv<-1e-12 or rv>$W.pi+1e-12):
   $![]
  $![fn('cos',r)]
 if h=='$x':
  if rv is $- $# $* $H(rv)>=$W.pi/2:
   $![]
  $![fn('tan',r)]
 if h=='sinh':
  $![fn('arcsinh',r)]
 if h=='cosh':
  if rv is $- $# $* rv<1:
   $![]
  a=fn('arccosh',r)
  $![$k(a),a]
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
$, xkernels(e,x,$?):
 if $/(e)is $- $0 or e[0]=='Q' or $4(e,x):
  $!
 h=e[0]
 if h in('+','*'):
  $) a in e[1:]:
   xkernels(a,x,$?)
  $!
 if h=='^' $* $/(e[2])is $w:
  xkernels(e[1],x,$?)
  $!
 if h=='^' $* isq(e[2])$* e[1]==x:
  k=pw(x,Q(1,e[2][2]))
  if k $- in $?:
   $?.$%(k)
  $!
 if e $- in $?:
  $?.$%(e)
$, kernel_solve(nu,x,$@,$<):
 W='W_'
 g=nu
 exps=[]
 findexp(g,x,exps)
 if exps:
  base=exps[0][0]
  if all([b==base $) b,a,c in exps]):
   gg=0
   $) b,a,c in exps:
    gg=a if gg==0 $( rgcd(gg,a)
   if gg!=0:
    g2=repl_exp(g,x,base,gg,W)
    if $4(g2,x):
     rs=$m(g2,W,$@,$<+1)
     if rs is $# or rs=='all':
      $! rs
     $?=[]
     $) r in rs:
      rr=isolate(pw(base,$:(gg,x)),r,x,$@,$<+1)
      if rr is $#:
       $! $#
      $?.extend(rr)
     $! $?
 ks=[]
 xkernels(g,x,ks)
 if $5(ks)==1 $* ks[0]!=x:
  k=ks[0]
  g2=$Q(g,k,W)
  if $4(g2,x):
   rs=$m(g2,W,$@,$<+1)
   if rs is $# or rs=='all':
    $! rs
   $?=[]
   $) r in rs:
    rr=isolate(k,r,x,$@,$<+1)
    if rr is $#:
     $! $#
    if rr=='all':
     $! 'all'
    $?.extend(rr)
   $! $?
 if $5(ks)==2:
  names=sorted([head(k)$) k in ks])
  if names==['cos','sin']$* ks[0][1]==ks[1][1]:
   u=ks[0][1]
   s=fn('sin',u)
   c=fn('cos',u)
   $) a,b in((c,s),(s,c)):
    g2=$>(g)
    cc=$X($Q(g2,a,W),W)
    if cc is $- $# $* all([cc[i]==0 $) i in $+(1,$5(cc),2)]):
     g3=$>($Q($Q(g2,a,W),W,$V($[(1,pw(b,2)))))
     if $- has(g3,a):
      $! kernel_solve(g3,x,$@,$<+1)if $<<4 $( $#
 $! $#
$, rgcd(a,b):
 if $r(a)$* $r(b):
  an,ad=nd(a)
  bn,bd=nd(b)
  $! Q(igcd(an,bn),ilcm(ad,bd))
 $! a if a==b $( 0
$, findexp(e,x,$?):
 if $/(e)is $- $0 or e[0]=='Q':
  $!
 if e[0]=='^' $* $4(e[1],x)$* $- $4(e[2],x):
  l=$g(e[2],x)
  if l is $- $#:
   $?.$%((e[1],l[0],l[1]))
   $!
  $?.$%(($#,0,0))
  $!
 $) a in e[1:]:
  findexp(a,x,$?)
$, repl_exp(e,x,base,gg,W):
 if $/(e)is $- $0 or e[0]=='Q':
  $! e
 if e[0]=='^' $* e[1]==base $* $- $4(e[2],x):
  l=$g(e[2],x)
  if l is $- $#:
   $! $:(pw(base,l[1]),pw(W,$O(l[0],gg)))
 $! simp((e[0],)+$0(repl_exp(a,x,base,gg,W)$) a in e[1:]))
''')
_x(r'''$, trig_lin(nu,x,$@):
 ks=[]
 xkernels(nu,x,ks)
 if $5(ks)!=2:
  $! $#
 names=sorted([head(k)$) k in ks])
 if names!=['cos','sin']or ks[0][1]!=ks[1][1]:
  $! $#
 u=ks[0][1]
 S='S_'
 C='C_'
 g=$>($Q($Q(nu,fn('sin',u),S),fn('cos',u),C))
 if has(g,x):
  $! $#
 cs_s=$X(g,S)
 if cs_s is $# or $5(cs_s)!=2:
  $! $#
 a=cs_s[1]
 $d=cs_s[0]
 cc=$X($d,C)
 if cc is $# or $5(cc)!=2 or has(a,C):
  $! $#
 b=cc[1]
 c=cc[0]
 if c==0:
  $! isolate(fn('tan',u),$.($k($O(b,a))),x,$@,0)
 R=$V($](pw(a,2),pw(b,2)))
 phi=fn('$x',$O(b,a))
 if $t(a)$* fv(a)<0:
  phi=$](phi,'pi')
 $! isolate(fn('sin',$](u,phi)),$.($k($O(c,R))),x,$@,0)
$, numeric_solve(f,x,$@,lo=$#,hi=$#,maxn=12):
 others=[s $) s in $q(f)if s!=x]
 if others:
  $! $#
 $, F(t):
  try:
   v=$S(f,{x:t})
  $9($D,$U,$`,$R,TypeError):
   $! $#
  if $/(v)is $1:
   if $H(v.imag)>1e-9*(1+$H(v.$N)):
    $! $#
   v=v.$N
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
 $* $H(b)<$H(a)$* $H(b)<$H(c)$*(a>0)==(b>0)==(c>0)$* $H(b)<1e-2):
   r=newton(F,t1)
   if r is $- $# $* t0<=r<=t2:
    roots.$%(r)
  t0,a=t1,b
  t1,b=t2,c
  if $5(roots)>200:
   $T
 if b is $- $# $* b==0 $* a is $- $# $* a!=0:
  roots.$%(t1)
 $?=[]
 $) r in sorted(roots):
  if $- $? or $H(r-$?[-1])>1e-9*(1+$H(r)):
   $?.$%(r)
 if $5($?)>maxn $* lo is $#:
  $?.sort(key=$H)
  $?=sorted($?[:maxn])
 $![snap(r)$) r in $?]
$, snap(r):
 if $H(r-round(r))<1e-12:
  $! $A(round(r))
 $! r
$, bisect(F,a,b,fa,fb):
 $) _ in $+(200):
  m=0.5*(a+b)
  fm=F(m)
  if fm is $#:
   $! $#
  if fm==0 or $H(b-a)<1e-15*(1+$H(m)):
   $T
  if(fm<0)==(fa<0):
   a,fa=m,fm
  $(:
   b,fb=m,fm
 m=0.5*(a+b)
 fm=F(m)
 if fm is $# or $H(fm)>1e-6*(1+$H(fa)+$H(fb)):
  if fm is $- $# $* $H(fm)>1e3:
   $! $#
 $! m
$, newton(F,t):
 $) _ in $+(60):
  v=F(t)
  if v is $#:
   $! $#
  h=1e-7*(1+$H(t))
  v2=F(t+h)
  if v2 is $#:
   $! $#
  d=(v2-v)/h
  if d==0:
   $T
  t2=t-v/d
  if $H(t2-t)<1e-14*(1+$H(t)):
   t=t2
   $T
  t=t2
 v=F(t)
 if v is $- $# $* $H(v)<1e-9:
  $! t
 $! $#
$, nsolve(f,x,guess=$#,lo=$#,hi=$#):
 $, F(t):
  try:
   v=$S(f,{x:t})
  $9($D,$U,$`,$R,TypeError):
   $! $#
  if $/(v)is $1:
   if $H(v.imag)>1e-9*(1+$H(v.$N)):
    $! $#
   v=v.$N
  $! v
 if guess is $- $#:
  r=secant(F,guess,lo,hi)
  if r is $- $#:
   $! r
 if lo is $- $# $* hi is $- $#:
  rs=numeric_solve(f,x,$3,lo,hi)
 $(:
  rs=numeric_solve(f,x,$3)
  if lo is $- $#:
   rs=[r $) r in rs if r>=lo]
  if hi is $- $#:
   rs=[r $) r in rs if r<=hi]
 if rs:
  if guess is $- $#:
   rs.sort(key=$7 r:$H(r-guess))
  $(:
   rs.sort(key=$7 r:$H(r))
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
 if $- $2($Q(f,x,0))or $- $2(diff(f,x)):
  r=ineq_param(rel,f,x)
  if r is $- $#:
   $! r
 $! solve_rels([(rel,f)],x)
$, rel_pairs(cs,x):
 $?=[]
 $) c in cs:
  h=head(c)
  if h=='$*':
   r=rel_pairs(c[1:],x)
   if r is $#:
    $! $#
   $?+=r
  $K h in('<','>','<=','>=','/=','='):
   $?.$%((h,$.($[(c[1],c[2]))))
  $(:
   $! $#
 $) rel,f in $?:
  if $- $4(f,x)$* fvars(f,x):
   $! $#
 $! $?
$, fvars(f,x):
 $! any(w!=x $* w $- in('pi','e','i','$M')$) w in $q(f))
''')
_x(r'''$, solve_rels(pairs,x,anyof=$3):
 pts=[]
 $) rel,f in pairs:
  if $4(f,x):
   $8
  rs=$m(f,x,$3)
  if rs is $#:
   $! $#
  if rs=='all':
   rs=[]
  $) r in rs:
   if $- $t(r):
    if $2(r):
     $8
    $! $#
   pts.$%(r)
  dens=[]
  domainpts(f,x,dens)
  $) d in dens:
   r2=$m(d,x,$3)
   if r2 is $# or r2=='all':
    $8
   $) r in r2:
    if $t(r):
     pts.$%(r)
    $K $- $2(r):
     $! $#
 pts=sortsols(dedup(pts))
 $, ok1(rel,f,t):
  try:
   v=$S(f,{x:t})
  $9 $6:
   $! $3
  if $/(v)is $1:
   if $H(v.imag)>1e-9*(1+$H(v.$N)):
    $! $3
   v=v.$N
  if v!=v:
   $! $3
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
     $! $E
   $! $3
  $! testp1(pairs,p)
 $, testp1(pairs,p):
  $) rel,f in pairs:
   try:
    v=$Q(f,x,p)
    if v=='$F' or has(v,'$F')or has(v,'$M'):
     $! $3
    vv=$S(v)
    if $/(vv)is $1:
     if $H(vv.imag)>=1e-9:
      $! $3
     vv=vv.$N
    if $H(vv)<1e-10:
     vv=0.0
    if $- relok(rel,vv):
     $! $3
   $9 $6:
    $! $3
  $! $E
 $e=[fv(p)$) p in pts]
 if $- $e:
  $! 'true' if test(0.5)$( 'false'
 segs=[('I',$#,pts[0],test($e[0]-max(1.0,$H($e[0]))))]
 $) i in $+($5(pts)):
  p=pts[i]
  segs.$%(('P',p,p,testp(p)))
  if i+1<$5(pts):
   segs.$%(('I',p,pts[i+1],test(0.5*($e[i]+$e[i+1]))))
 segs.$%(('I',pts[-1],$#,test($e[-1]+max(1.0,$H($e[-1])))))
 $! segs_to_bool(segs,x)
$, sgn(e):
 if $2(e):
  try:
   v=fv(e)
  $9 $6:
   $! 0
  $! 1 if v>0 $((-1 if v<0 $( 0)
 if $&(e,'*'):
  s=1
  $) a in e[1:]:
   k=sgn(a)
   if $- k:
    $! 0
   s*=k
  $! s
 if $&(e,'+'):
  ks=[sgn(a)or(2 if nonneg(a)$( 0)$) a in e[1:]]
  if all(k in(1,2)$) k in ks)$* 1 in ks:
   $! 1
  ks=[sgn($k(a))or(2 if nonneg($k(a))$( 0)$) a in e[1:]]
  if all(k in(1,2)$) k in ks)$* 1 in ks:
   $!-1
  $! 0
 if $&(e,'^')$* $j(e[2])$* e[2]%2==1:
  $! sgn(e[1])
 if head(e)=='exp' or($&(e,'^')$* e[1]=='e'):
  $! 1
 $! 0
$, nonneg(e):
 if $&(e,'^')$* $j(e[2])$* e[2]%2==0:
  $! $E
 if head(e)=='$H':
  $! $E
 if $&(e,'*'):
  $! all(nonneg(a)or sgn(a)>0 $) a in e[1:])
 $! sgn(e)>0
$, ineq_param(rel,f,x):
 cs=$X(f,x)
 if cs is $# or $5(cs)!=2:
  $! $#
 a=nice(comdenom(cs[1]))
 b=cs[0]
 v=nice(comdenom($O($k(b),a)))
 k=sgn(a)
 if k:
  $!(rel if k>0 $( FLIP[rel],x,v)
 n=numer_denom(a)[0]
 if rel=='/=':
  $?=[('$*',('/=',x,v),('/=',n,0))]
 $(:
  $?=[('$*',(rel,x,v),('>',a,0)),
 ('$*',(FLIP[rel],x,v),('<',a,0))]
 if $/(n)is ${:
  b=$Q(b,n,0)
 if $2(b):
  if relok(rel,fv(b)):
   $?.$%(('=',n,0))
 $(:
  $?.$%(('$*',('=',n,0),(rel,b,0)))
 $!('or',)+$0($?)if $5($?)>1 $( $?[0]
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
$, domainpts(f,x,$?):
 if $/(f)is $- $0 or f[0]=='Q':
  $!
 h=f[0]
 if h=='^' $* $- $4(f[1],x):
  if $C(f[2])$* $_(f[2])<0:
   $?.$%(f[1])
  if isq(f[2])$* f[2][2]%2==0:
   $?.$%(f[1])
 if h in('ln','log','$H','sign','floor','ceiling')$* $- $4(f[1],x):
  $?.$%(f[1])
 $) a in f[1:]:
  domainpts(a,x,$?)
$, segs_to_bool(segs,x):
 ivs=[]
 cur=$#
 $) kind,a,b,ok in segs:
  if ok:
   if cur is $#:
    if kind=='I':
     cur=[a,$3,b,$3]
    $(:
     cur=[a,$E,b,$E]
   $(:
    cur[2]=b
    cur[3]=(kind=='P')
  $(:
   if cur is $- $#:
    ivs.$%(cur)
    cur=$#
 if cur is $- $#:
  ivs.$%(cur)
 if $- ivs:
  $! 'false'
 if $5(ivs)>=2 $* ivs[0][0]is $# $* ivs[-1][2]is $#:
  okp=$E
  $) i in $+($5(ivs)-1):
   if $-(ivs[i][2]==ivs[i+1][0]$* $- ivs[i][3]$* $- ivs[i+1][1]):
    okp=$3
  if okp:
   ne=[('/=',x,ivs[i][2])$) i in $+($5(ivs)-1)]
   $! ne[0]if $5(ne)==1 $(('$*',)+$0(ne)
 $?=[]
 $) lo,li,hi,hiinc in ivs:
  if lo is $# $* hi is $#:
   $! 'true'
  if lo is $- $# $* hi is $- $# $* lo==hi:
   $?.$%(('=',x,lo))
  $K lo is $#:
   $?.$%(('<=' if hiinc $( '<',x,hi))
  $K hi is $#:
   $?.$%(('>=' if li $( '>',x,lo))
  $(:
   $?.$%(('$*',('<=' if li $( '<',lo,x),('<=' if hiinc $( '<',x,hi)))
 if $5($?)==1:
  $! $?[0]
 $!('or',)+$0($?)
$, eqexpr(eq):
 if $&(eq,'='):
  $! $.($[(eq[1],eq[2]))
 $! eq
$, is_linear_sys(fs,vs):
 $) f in fs:
  $) v in vs:
   d=degree(f,v)
   if d is $# or d>1:
    $! $3
  g=$>(f)
  $) i in $+($5(vs)):
   $) j in $+($5(vs)):
    cs_=$X(g,vs[i])
    if cs_ is $#:
     $! $3
    if $5(cs_)>1 $* has(cs_[1],vs[j]):
     $! $3
 $! $E
''')
_x(r'''$, linsys(fs,vs):
 m=$5(fs)
 n=$5(vs)
 A=[]
 $) f in fs:
  g=$>(f)
  row=[]
  $d=g
  $) v in vs:
   cs_=$X(g,v)
   c=cs_[1]if $5(cs_)>1 $( 0
   row.$%(c)
  const=g
  $) v in vs:
   const=$Q(const,v,0)
  row.$%($k(const))
  A.$%(row)
 piv=[]
 r=0
 $) c in $+(n):
  p=$#
  $) i in $+(r,m):
   if $.(A[i][c])!=0:
    p=i
    $T
  if p is $#:
   $8
  A[r],A[p]=A[p],A[r]
  pv=A[r][c]
  A[r]=[$.($O(a,pv))$) a in A[r]]
  $) i in $+(m):
   if i!=r $* A[i][c]!=0:
    fct=A[i][c]
    A[i]=[$.($>($[(A[i][j],$:(fct,A[r][j]))))$) j in $+(n+1)]
  piv.$%(c)
  r+=1
  if r==m:
   $T
 $) i in $+(r,m):
  if $.(A[i][n])!=0:
   $![]
 sol={}
 free=[c $) c in $+(n)if c $- in piv]
 params={}
 k=1
 $) c in free:
  params[vs[c]]='c'+${(k)
  k+=1
 $) i in $+($5(piv)):
  c=piv[i]
  val=A[i][n]
  $) c2 in free:
   val=$[(val,$:(A[i][c2],params[vs[c2]]))
  sol[vs[c]]=nice($.(val))
 $) c in free:
  sol[vs[c]]=params[vs[c]]
 $![sol]
$, solve_system(eqs,vs,$@=$3,guesses=$#):
 NC[0]=0
 fs=[]
 $) e in eqs:
  f=eqexpr(e)
  f=numer_of(f)if hasdenom_x(f,vs)$( f
  if f!=0:
   fs.$%(f)
 if guesses:
  $! newton_sys(fs,vs,guesses)
 if is_linear_sys(fs,vs):
  $! linsys(fs,vs)
 r=elim(fs,vs,$@,0)
 if r is $#:
  $! newton_sys(fs,vs,[0.0]*$5(vs))
 $?=[]
 $) s in r:
  ok=$E
  $) v in vs:
   if v $- in s:
    s[v]=v
  if $- $@:
   $) v in vs:
    if $2(s[v])$* $- $t(s[v]):
     ok=$3
  if ok $* s $- in $?:
   $?.$%(s)
 $! $?
$, hasdenom_x(f,vs):
 $) v in vs:
  nu,de=numer_denom(f)
  if has(de,v):
   $! $E
 $! $3
$, elim(fs,vs,$@,$<):
 fs=[$.($>(f))$) f in fs]
 fs=[f $) f in fs if f!=0]
 if $- fs:
  $![{}]
 $) f in fs:
  if freeofall(f,vs):
   if $2(f)or f!=0:
    $![]
 if $<>8:
  $! $#
 $z=$#
 $) f in fs:
  inv=[v $) v in vs if has(f,v)]
  if $5(inv)==1:
   $z=(f,inv[0])
   $T
 if $z is $#:
  $) f in fs:
   $) v in vs:
    d=degree(f,v)
    if d==1:
     c=$X(f,v)
     if c is $- $# $* $2(c[1])$* c[1]!=0:
      $z=(f,v)
      $T
   if $z:
    $T
 if $z is $#:
  $) f in fs:
   $) v in vs:
    if degree(f,v)==1:
     $z=(f,v)
     $T
   if $z:
    $T
 if $z is $- $#:
  f,v=$z
  rs=$m(f,v,$@)
  if rs is $#:
   $! $#
  if rs=='all':
   rs=[]
  $?=[]
  $d=[g $) g in fs if g is $- f]
  ovs=[w $) w in vs if w!=v]
  $) r in rs:
   sub_=[$.($Q(g,v,r))$) g in $d]
   rr=elim(sub_,ovs,$@,$<+1)
   if rr is $#:
    $! $#
   $) s in rr:
    s2=dict(s)
    val=r
    $) w in s2:
     val=$Q(val,w,s2[w])
    s2[v]=clean(val)
    $?.$%(s2)
  $! $?
 if $5(fs)>=2 $* $5(vs)>=2:
  y=vs[-1]
  R=resultant(fs[0],fs[1],y)
  if R is $# or R==0:
   $! $#
  rr=elim([R]+fs[2:],vs[:-1],$@,$<+1)
  if rr is $#:
   $! $#
  $?=[]
  $) s in rr:
   gs=[]
   $) g in fs:
    h=g
    $) w in s:
     h=$Q(h,w,s[w])
    gs.$%($.($>(h)))
   ys=elim(gs,[y],$@,$<+1)
   if ys is $#:
    $8
   $) t in ys:
    s2=dict(s)
    s2.update(t)
    $?.$%(s2)
  $! $?
 $! $#
$, resultant(f,g,y):
 a=$X(f,y)
 b=$X(g,y)
 if a is $# or b is $#:
  $! $#
 m=$5(a)-1
 n=$5(b)-1
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
 $! $>(bareiss(M))
$, bareiss(M):
 n=$5(M)
 M=[$I(r)$) r in M]
 sign=1
 prev=1
 $) k in $+(n-1):
  if M[k][k]==0:
   sw=$#
   $) i in $+(k+1,n):
    if M[i][k]!=0:
     sw=i
     $T
   if sw is $#:
    $! 0
   M[k],M[sw]=M[sw],M[k]
   sign=-sign
  $) i in $+(k+1,n):
   $) j in $+(k+1,n):
    num=$>($[($:(M[i][j],M[k][k]),$:(M[i][k],M[k][j])))
    M[i][j]=exdiv(num,prev)
  prev=M[k][k]
 $! $:(sign,M[n-1][n-1])
$, exdiv(a,b):
 if b==1:
  $! a
 if $C(b):
  $! $>($:(a,ninv(b))if $r(b)$( $O(a,b))
 ks=[]
 kernels(a,ks)
 kernels(b,ks)
 sortkernels(ks)
 ra=ratform(a,ks)
 rb=ratform(b,ks)
 if ra is $# or rb is $#:
  $! $.($O(a,b))
 q=$P(p_mul(ra[0],rb[1]),p_mul(ra[1],rb[0]))
 if q is $#:
  $! $.($O(a,b))
 $! p2e(q,ks)
$, newton_sys(fs,vs,guess):
 n=$5(vs)
 if $5(fs)!=n:
  $! $#
 others=[]
 $) f in fs:
  $) s in $q(f):
   if s $- in vs:
    $! $#
 J=[[diff(f,v)$) v in vs]$) f in fs]
 xv=[$A($S(g).$N)if $C(g)or $2(g)$( 0.0 $) g in guess]
 $) it in $+(100):
  env=dict(zip(vs,xv))
  try:
   F=[$S(f,env)$) f in fs]
   Jv=[[$S(J[i][j],env)$) j in $+(n)]$) i in $+(n)]
  $9 $6:
   $! $#
  F=[v.$N if $/(v)is $1 $( v $) v in F]
  Jv=[[v.$N if $/(v)is $1 $( v $) v in r]$) r in Jv]
  dx=linsolve_float(Jv,[-v $) v in F])
  if dx is $#:
   $! $#
  xv=[xv[i]+dx[i]$) i in $+(n)]
  if max([$H(d)$) d in dx])<1e-13*(1+max([$H(v)$) v in xv])):
   $T
 env=dict(zip(vs,xv))
 try:
  if max([$H($S(f,env))$) f in fs])>1e-8:
   $![]
 $9 $6:
  $![]
 $![dict([(vs[i],snap(xv[i]))$) i in $+(n)])]
$, linsolve_float(A,b):
 n=$5(A)
 M=[$I(A[i])+[b[i]]$) i in $+(n)]
 $) c in $+(n):
  p=max($+(c,n),key=$7 i:$H(M[i][c]))
  if $H(M[p][c])<1e-300:
   $! $#
  M[c],M[p]=M[p],M[c]
  $) i in $+(n):
   if i!=c:
    f=M[i][c]/M[c][c]
    $) j in $+(c,n+1):
     M[i][j]-=f*M[c][j]
 $![M[i][n]/M[i][i]$) i in $+(n)]
$, sols_to_bool(x,$f):
 if $f=='all':
  $! 'true'
 if $f is $#:
  $! $#
 if $- $f:
  $! 'false'
 eqs=[('=',x,s)$) s in $f]
 if $5(eqs)==1:
  $! eqs[0]
 $!('or',)+$0(eqs)
''')
_x(r'''$, apply_constraints($f,x,cons):
 if $- cons or $f=='all' or $f is $#:
  $! $f
 lo=$#
 hi=$#
 $?=[]
 expanded=[]
 $) s in $f:
  ns=[w $) w in $q(s)if w[0]=='n' $* w[1:].isdigit()]
  if ns $* $5(ns)==1:
   b=bounds(cons,x)
   if b is $#:
    expanded.$%(s)
    $8
   n=ns[0]
   $) k in $+(-60,61):
    v=$Q(s,n,k)
    expanded.$%(v)
  $(:
   expanded.$%(s)
 $) s in expanded:
  if satisfies(s,x,cons):
   $?.$%(s)
 $! sortsols(dedup($?))
$, bounds(cons,x):
 lo=$#
 hi=$#
 $) c in cons:
  if head(c)in('<','<=','>','>=')$* $2(c[1])$* c[2]==x:
   if c[0]in('<','<='):
    lo=c[1]
   $(:
    hi=c[1]
  $K head(c)in('<','<=','>','>=')$* c[1]==x $* $2(c[2]):
   if c[0]in('<','<='):
    hi=c[2]
   $(:
    lo=c[2]
 if lo is $# or hi is $#:
  $! $#
 $! lo,hi
$, satisfies(s,x,cons):
 $) c in cons:
  h=head(c)
  if h in('<','<=','>','>=','/=','='):
   try:
    a=fv($Q(c[1],x,s))
    b=fv($Q(c[2],x,s))
   $9 $6:
    if $- $2(s):
     $8
    $! $3
   eps=1e-12*(1+$H(a)+$H(b))
   if h=='<' $* $- a<b-eps*0:
    $! $3
   if h=='<=' $* $- a<=b+eps:
    $! $3
   if h=='>' $* $- a>b:
    $! $3
   if h=='>=' $* $- a>=b-eps:
    $! $3
   if h=='/=' $* $H(a-b)<=eps:
    $! $3
   if h=='=' $* $H(a-b)>1e-9*(1+$H(a)+$H(b)):
    $! $3
  $K h=='$*':
   if $- satisfies(s,x,$I(c[1:])):
    $! $3
 $! $E
$, solve(eq,x,$@=$3,cons=$#):
 NC[0]=0
 if $&(eq,'$*')or $&(eq,'$I'):
  $! $#
 h=head(eq)
 if h in('<','>','<=','>=','/='):
  f=$[(eq[1],eq[2])
  cp=rel_pairs(cons,x)if cons $( $#
  if cp:
   $! solve_rels([(h,$.(f))]+cp,x)
  r=solve_ineq(h,f,x)
  $! r
 if h=='=':
  f=$[(eq[1],eq[2])
 $K h=='or':
  if $- $@ $* any([head(q)in('<','>','<=','>=','/=')$) q in eq[1:]]):
   ps=rel_pairs(eq[1:],x)if all([head(q)!='$*' $) q in eq[1:]])$( $#
   if ps:
    r=solve_rels(ps,x,$E)
    if r is $- $#:
     $! r
  $y=[]
  $) e in eq[1:]:
   r=solve(e,x,$@,cons)
   if r is $#:
    $! $#
   if r=='true':
    $! 'true'
   if $&(r,'or'):
    $y.extend([q $) q in r[1:]if q $- in $y])
   $K r!='false' $* r $- in $y:
    $y.$%(r)
  if $- $y:
   $! 'false'
  $!('or',)+$0($y)if $5($y)>1 $( $y[0]
 $K eq=='true':
  $! 'true'
 $(:
  f=eq
 w=firstwhen(f,x)
 if w is $- $#:
  r=solve_when(f,w,x,$@,cons)
  if r is $- $#:
   $! r
 if $- $@ $* firstabs(f,x)is $- $# $* abs_cases(numer_of(f),x,[],0)=='interval':
  r=abs_region(f,x,cons)
  if r is $- $#:
   $! r
 $f=$m(f,x,$@)
 if $f is $#:
  $! $#
 if $f!='all':
  $f=[clean(s)$) s in $f]
  if $- $@:
   $f=[s $) s in $f if $-($2(s)$* $- $t(s))]
   $f=[realpart(s)$) s in $f]
  $f=sortsols(dedup($f))
 if cons:
  $f=apply_constraints($f,x,cons)
 $! sols_to_bool(x,$f)
$, firstabs(f,x):
 if $/(f)is $- $0 or f[0]=='Q':
  $! $#
 if f[0]=='$H' $* $- $4(f[1],x):
  $! f
 $) a in f[1:]:
  w=firstabs(a,x)
  if w is $- $#:
   $! w
 $! $#
$, abs_cases(f,x,conds,$<):
 w=firstabs(f,x)
 if w is $#:
  rs=$m(f,x,$3,$<+1)
  if rs=='all':
   ps=rel_pairs(conds,x)
   r=solve_rels(ps,x)if ps is $- $# $( $#
   if r=='false':
    $![]
   if r is $# or $&(r,'$*')or head(r)in('<','>','<=','>=','/=','or')or r=='true':
    $! 'interval'
   $![r[2]]if $&(r,'=')$( 'interval'
  if rs is $#:
   $! $#
  $?=[]
  $) q in rs:
   ns=[w $) w in $q(q)if w[0]=='n' $* w[1:].isdigit()]
   q0=$Q(q,ns[0],0)if $5(ns)==1 $( q
   if $t(q0)$* satisfies(q0,x,conds):
    $?.$%(q)
  $! $?
 u=w[1]
 $?=[]
 $) g,c in((replnode(f,w,u),('>=',u,0)),(replnode(f,w,$k(u)),('<',u,0))):
  r=abs_cases(g,x,conds+[c],$<)
  if r is $# or r=='interval':
   $! r
  $) q in r:
   if q $- in $?:
    $?.$%(q)
 $! sortsols($?)
$, abs_region(f,x,cons):
 pts=[]
 $, walk(e):
  if $/(e)is $- $0 or e[0]=='Q':
   $!
  if e[0]=='$H' $* $- $4(e[1],x):
   rs=$m(e[1],x,$3)
   if rs $* rs!='all':
    pts.extend([q $) q in rs if $t(q)])
  $) b in e[1:]:
   walk(b)
 walk(f)
 $, ok(t):
  try:
   v=fv($Q(f,x,t))if $- $/(t)is $A $( $S(f,{x:t})
   if $/(v)is $1:
    v=v.$N
   $! $H(v)<1e-9 $* satisfies(t,x,cons or[])
  $9 $6:
   $! $3
 pts=sortsols(dedup(pts))
 if $- pts:
  $! $#
 $e=[fv(p)$) p in pts]
 segs=[('I',$#,pts[0],ok($e[0]-1.0))]
 $) i in $+($5(pts)):
  segs.$%(('P',pts[i],pts[i],ok(pts[i])))
  if i+1<$5(pts):
   segs.$%(('I',pts[i],pts[i+1],ok(0.5*($e[i]+$e[i+1]))))
 segs.$%(('I',pts[-1],$#,ok($e[-1]+1.0)))
 $! segs_to_bool(segs,x)
NOTREL={'<':'>=','>':'<=','<=':'>','>=':'<','=':'/=','/=':'='}
$, firstwhen(f,x):
 if $/(f)is $- $0 or f[0]=='Q':
  $! $#
 if f[0]=='when' $* $- $4(f[1],x):
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
_x(r'''$, solve_when(f,w,x,$@,cons):
 c=w[1]
 cs=$I(c[1:])if head(c)=='$*' $([c]
 if $- all([head(q)in NOTREL $) q in cs]):
  $! $#
 $y=[]
 r=solve(('=',replnode(f,w,w[2]),0),x,$@,(cons or[])+cs)
 if r is $#:
  $! $#
 $y.$%(r)
 if $5(w)>3:
  $) k in $+($5(cs)):
   nc=cs[:k]+[(NOTREL[cs[k][0]],cs[k][1],cs[k][2])]
   r=solve(('=',replnode(f,w,w[3]),0),x,$@,(cons or[])+nc)
   if r is $#:
    $! $#
   $y.$%(r)
 $?=[]
 $) r in $y:
  $) q in(r[1:]if $&(r,'or')$((r,)):
   if q!='false' $* q $- in $?:
    $?.$%(q)
 if 'true' in $?:
  $! $#
 if $- $?:
  $! 'false'
 $! $?[0]if $5($?)==1 $(('or',)+$0($?)
$, realpart(s):
 if $2(s)$* has(s,'i'):
  r,i=reim(s)
  if i==0 or($C(i)$* $H(tofl(i))<1e-12):
   $! r
 $! s
$, zeros(e,x,$@=$3,cons=$#):
 NC[0]=0
 if $&(e,'='):
  e=$[(e[1],e[2])
 if firstwhen(e,x)is $- $#:
  r=solve(('=',e,0),x,$@,cons)
  qs=r[1:]if $&(r,'or')$((r,)
  if r is $- $# $* all([r=='false' or($&(q,'=')$* q[1]==x)$) q in qs]):
   $!('$I',)+$0([q[2]$) q in qs if r!='false'])
 $f=$m(e,x,$@)
 if $f is $#:
  $! $#
 if $f=='all':
  $!('$I',)
 $f=[clean(s)$) s in $f]
 if $- $@:
  $f=[realpart(s)$) s in $f if $-($2(s)$* $- $t(s))]
 $f=sortsols(dedup($f))
 if cons:
  $f=apply_constraints($f,x,cons)
 $!('$I',)+$0($f)
YP=('Y1_','Y2_')
$, desolve(ode,x,y,conds):
 NC[0]=0
 F=eqexpr(ode)if $&(ode,'=')$( ode
 F=$.(F)
 if has(F,YP[1]):
  sol=de2(F,x,y)
  nconst=2
 $(:
  sol=de1(F,x,y)
  nconst=1
 if sol is $#:
  $! $#
 if conds:
  sol=apply_ic(sol,x,y,conds,nconst)
 $! sol
$, de1(F,x,y):
 y1=YP[0]
 cs_=$X(F,y1)
 if cs_ is $- $# $* $5(cs_)==2 $* $4(cs_[1],y1):
  g=$.($k($O(cs_[0],cs_[1])))
 $(:
  rs=$m(F,y1)
  if $- rs or rs=='all' or $5(rs)!=1:
   $! $#
  g=rs[0]
 c1='c1'
 gy=$X($>(g),y)
 if gy is $- $# $* $5(gy)==2 $* $4(gy[1],y):
  P=$k(gy[1])
  Bq=gy[0]
  if Bq==0 or $4(P,x)$* $4(Bq,x)$* $3:
   pass
  mu=pw('e',integrate(P,x))
  mu=dropabs(simp(mu))
  I=$|($.($>($:(mu,Bq))),x)
  if I is $- $#:
   yy=$.($O($](I,c1),mu))
   $!('=',y,nice($>(yy))if $- hasden_free(yy)$( nice(yy))
 sep=separate(g,x,y)
 if sep is $- $#:
  p,q=sep
  L=$|($.(pw(q,-1)),y)
  R=$|(p,x)
  if L is $- $# $* R is $- $#:
   rs=isolate_eq(L,$](R,c1),y)
   if rs is $- $# $* $5(rs)==1:
    $!('=',y,nice(simp(rs[0])))
   G=lncombine(L,y)
   if G is $- $#:
    rs=$m($[(G,$:(c1,pw('e',R))),y)
    if rs $* rs!='all' $* $5(rs)==1:
     $!('=',y,nice(rs[0]))
   $!('=',L,$](R,c1))
 bern_=bernoulli(g,x,y)
 if bern_ is $- $#:
  $! bern_
 V='V_'
 h=$.($Q(g,y,$:(V,x)))
 if $4(h,x)$* has(h,V):
  dv=$.($[(h,V))
  if dv!=0:
   L=$|($.(pw(dv,-1)),V)
   if L is $- $#:
    R=$](fn('ln',fn('$H',x)),c1)
    rs=isolate_eq(L,R,V)
    if rs is $- $# $* $5(rs)==1:
     $!('=',y,nice($>($:(x,rs[0]))))
    L2=$Q(L,V,$O(y,x))
    $!('=',L2,R)
 $! $#
$, dropabs(e):
 if $/(e)is $- $0 or e[0]=='Q':
  $! e
 if e[0]=='$H':
  $! dropabs(e[1])
 $! simp((e[0],)+$0(dropabs(a)$) a in e[1:]))
$, lncombine(L,y):
 $L=L[1:]if $&(L,'+')$((L,)
 fs=[]
 $) t in $L:
  c,r=$a(t)
  if $&(r,'ln')$* $r(c):
   u=r[1]
   if $&(u,'$H'):
    u=u[1]
   fs.$%(pw(u,c))
  $(:
   $! $#
 if $5(fs)<1:
  $! $#
 $! $.($G(fs))
$, hasden_free(e):
 $! $3
$, isolate_eq(L,R,y):
 try:
  r=isolate(L,R,y,$3,0)
 $9 $6:
  $! $#
 if r is $# or r=='all':
  $! $#
 $! r
$, separate(g,x,y):
 if $4(g,y):
  $! g,1
 if $4(g,x):
  $! 1,g
 fs=g[1:]if $&(g,'*')$((g,)
 px=[]
 qy=[]
 $) f in fs:
  if $4(f,y):
   px.$%(f)
  $K $4(f,x):
   qy.$%(f)
  $K $&(f,'^')$* $4(f[1],x)$* $4(f[1],y)$* $&(f[2],'+'):
   tx=[t $) t in f[2][1:]if $4(t,y)]
   ty=[t $) t in f[2][1:]if $4(t,x)]
   if $5(tx)+$5(ty)!=$5(f[2])-1:
    $! $#
   px.$%(pw(f[1],$;(tx)))
   qy.$%(pw(f[1],$;(ty)))
  $(:
   $! $#
 $! $G(px),$G(qy)
$, expand_exp(e):
 if $/(e)is $- $0 or e[0]=='Q':
  $! e
 if e[0]=='^' $* $&(e[2],'+')$*(e[1]=='e' or $C(e[1])):
  $! $G([pw(e[1],t)$) t in e[2][1:]])
 $! simp((e[0],)+$0(expand_exp(a)$) a in e[1:]))
$, bernoulli(g,x,y):
 g=$>(g)
 $L=g[1:]if $&(g,'+')$((g,)
 groups={}
 $) t in $L:
  k=$#
  fs=t[1:]if $&(t,'*')$((t,)
  $d=[]
  $) f in fs:
   if f==y:
    k=1 if k is $# $( $#
   $K $&(f,'^')$* f[1]==y $* $C(f[2]):
    k=f[2]
   $K $4(f,y):
    $d.$%(f)
   $(:
    $! $#
  if k is $#:
   $! $#
  groups[k]=$](groups.get(k,0),$G($d))
 if $5(groups)!=2 or 1 $- in groups:
  $! $#
 n=[k $) k in groups if k!=1][0]
 a=groups[1]
 b=groups[n]
 m=nsub(1,n)
 V='V_'
 vs=de1($[(YP[0],$:(m,$]($:(a,V),b))),x,V)
 if vs is $# or $- $&(vs,'=')or vs[1]!=V:
  $! $#
 $!('=',y,nice(pw(vs[2],ninv(m))))
''')
_x(r'''$, de2(F,x,y):
 y1,y2=YP
 c1,c2='c1','c2'
 G=$>(F)
 a=$X(G,y2)
 if a is $# or $5(a)!=2:
  $! $#
 A=a[1]
 $d=a[0]
 b=$X($d,y1)
 if b is $# or $5(b)>2:
  $! $#
 B=b[1]if $5(b)==2 $( 0
 $d=b[0]
 c=$X($d,y)
 if c is $# or $5(c)>2:
  $! $#
 C=c[1]if $5(c)==2 $( 0
 g=$k(c[0])
 $) t in(A,B,C):
  if has(t,y)or has(t,y1)or has(t,y2):
   $! $#
 if $4(A,x)$* $4(B,x)$* $4(C,x):
  y1s,y2s=charsol(A,B,C,x)
 $(:
  ce=cauchy_euler(A,B,C,x)
  if ce is $#:
   if C==0:
    V='V_'
    r=de1($]($:(A,YP[0]),$:(B,V),$k(g)),x,V)
    if r is $# or $- $&(r,'=')or r[1]!=V:
     $! $#
    r2=$|($Q(r[2],'c1','c2'),x)
    if r2 is $#:
     $! $#
    $!('=',y,$](r2,c1))
   $! $#
  y1s,y2s=ce
 yh=$]($:(c1,y1s),$:(c2,y2s))
 if g==0:
  $!('=',y,yh)
 W=pyth($.($>($[($:(y1s,diff(y2s,x)),$:(diff(y1s,x),y2s)))))
 gg=$.($O(g,A))
 I1=$|($.($>($O($:(y2s,gg),W))),x)
 I2=$|($.($>($O($:(y1s,gg),W))),x)
 if I1 is $# or I2 is $#:
  $! $#
 yp=pyth($>($]($:($k(y1s),I1),$:(y2s,I2))))
 $!('=',y,nice($](yh,yp)))
$, charsol(A,B,C,x):
 D=$.($>($[($:(B,B),$:(4,A,C))))
 if $t(D)$* fv(D)<0:
  al=$.($O($k(B),$:(2,A)))
  be=$.($O($V($k(D)),$:(2,A)))
  ex=pw('e',$:(al,x))
  $! $:(ex,fn('cos',$:(be,x))),$:(ex,fn('sin',$:(be,x)))
 if D==0:
  r=$.($O($k(B),$:(2,A)))
  $! pw('e',$:(r,x)),$:(x,pw('e',$:(r,x)))
 s=$V(D)
 r1=$.($O($]($k(B),s),$:(2,A)))
 r2=$.($O($[($k(B),s),$:(2,A)))
 $! pw('e',$:(r1,x)),pw('e',$:(r2,x))
$, cauchy_euler(A,B,C,x):
 a=$.($O(A,pw(x,2)))
 b=$.($O(B,x))
 if $-($4(a,x)$* $4(b,x)$* $4(C,x)):
  $! $#
 aa=a
 bb=$[(b,a)
 cc=C
 D=$.($>($[($:(bb,bb),$:(4,aa,cc))))
 lx=fn('ln',x)
 if $t(D)$* fv(D)<0:
  al=$.($O($k(bb),$:(2,aa)))
  be=$.($O($V($k(D)),$:(2,aa)))
  $! $:(pw(x,al),fn('cos',$:(be,lx))),$:(pw(x,al),fn('sin',$:(be,lx)))
 if D==0:
  r=$.($O($k(bb),$:(2,aa)))
  $! pw(x,r),$:(pw(x,r),lx)
 s=$V(D)
 r1=$.($O($]($k(bb),s),$:(2,aa)))
 r2=$.($O($[($k(bb),s),$:(2,aa)))
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
   eqs.$%(('=',$Q(e,x,x0),v))
 $(:
  $) order,x0,v in conds:
   if order==0:
    eqs.$%($Q($Q(sol,x,x0),y,v))
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
   r=(r[0],$Q(r[1],c,s[c]),$Q(r[2],c,s[c]))
 if r[1]==y:
  $!('=',y,nice(r[2]))
 rs2=isolate_eq(r[1],r[2],y)
 if rs2 is $- $# $* $5(rs2)>=1:
  $) cand in rs2:
   ok=$E
   $) order,x0,v in conds:
    if order==0:
     try:
      if $H($S($Q(cand,x,x0))-$S(v))>1e-9:
       ok=$3
     $9 $6:
      pass
   if ok:
    $!('=',y,nice(cand))
 $! r
$, fextreme(f,x,kind,lo=$#,hi=$#):
 NC[0]=0
 d=$.(diff(f,x))
 cands=[]
 rs=$m(d,x)
 if rs is $#:
  rs=numeric_solve(d,x,$3,tofl($S(lo))if lo is $- $# $* $2(lo)$( $#,
 tofl($S(hi))if hi is $- $# $* $2(hi)$( $#)or[]
 if rs=='all':
  $! 'true'
 exp_=[]
 $) r in rs:
  ns=[w $) w in $q(r)if w[0]=='n' $* w[1:].isdigit()]
  if ns $* lo is $- $# $* hi is $- $#:
   $) k in $+(-50,51):
    exp_.$%($Q(r,ns[0],k))
  $K ns:
   exp_.$%(r)
  $(:
   exp_.$%(r)
 rs=exp_
 $) r in rs:
  r=clean(r)
  ns=[w $) w in $q(r)if w[0]=='n' $* w[1:].isdigit()]
  if ns:
   cands.$%(r)
   $8
  if $- $t(r):
   $8
  if lo is $- $# $* fv(r)<fv(lo)-1e-12:
   $8
  if hi is $- $# $* fv(r)>fv(hi)+1e-12:
   $8
  cands.$%(r)
 ends=[]
 ends.$%(lo if lo is $- $# $(('*',-1,'$M'))
 ends.$%(hi if hi is $- $# $( '$M')
 $z=$#
 bv=$#
 pts=[]
 $) c in cands+ends:
  if c=='$M' or c==('*',-1,'$M'):
   v=$v(f,x,c)
  $(:
   cz=c
   $) w in $q(c):
    if w[0]=='n' $* w[1:].isdigit():
     cz=$Q(cz,w,0)
   v=$Q(f,x,cz)
   if has(v,'$F'):
    $8
  try:
   if v=='$M':
    vv=$A('$M')
   $K v==('*',-1,'$M'):
    vv=$A('-$M')
   $(:
    vv=fv(v)
  $9 $6:
   $8
  if kind=='max':
   vv=-vv
  pts.$%((vv,c))
 if $- pts:
  $! $#
 pts.sort(key=$7 p:p[0])
 m=pts[0][0]
 if m==$A('-$M'):
  win=[p[1]$) p in pts if p[0]==m]
 $(:
  win=[p[1]$) p in pts if $H(p[0]-m)<=1e-10*(1+$H(m))]
 win=sortsols(dedup(win))
 eqs=[('=',x,w)$) w in win]
 $! eqs[0]if $5(eqs)==1 $(('or',)+$0(eqs)
''')
_x(r'''$, nfextreme(f,x,kind,lo=$#,hi=$#):
 sg=1.0 if kind=='min' $(-1.0
 $, F(t):
  try:
   v=$S(f,{x:t})
   if $/(v)is $1:
    v=v.$N
   $! sg*v
  $9 $6:
   $! $A('$M')
 if lo is $# or hi is $#:
  a=-100.0 if lo is $# $( lo
  b=100.0 if hi is $# $( hi
 $(:
  a,b=lo,hi
 N=400
 $z=a
 bv=F(a)
 $) i in $+(N+1):
  t=a+(b-a)*i/N
  v=F(t)
  if v<bv:
   bv=v
   $z=t
 h=(b-a)/N
 l=max(a,$z-h)
 r=min(b,$z+h)
 g=($W.$V(5)-1)/2
 $) _ in $+(200):
  c=r-g*(r-l)
  d=l+g*(r-l)
  if F(c)<F(d):
   r=d
  $(:
   l=c
  if $H(r-l)<1e-12*(1+$H(l)):
   $T
 t=0.5*(l+r)
 $) side,bound in((1.0,hi),(-1.0,lo)):
  if bound is $#:
   vs=[F(side*10.0**k)$) k in(3,5,7)]
   if vs[0]<=bv $* vs[1]<=vs[0]$* vs[2]<=vs[1]$* vs[2]<bv:
    $! '$M' if side>0 $(('*',-1,'$M')
 try:
  d=diff(f,x)
  $, G(u):
   try:
    v=$S(d,{x:u})
    $! v.$N if $/(v)is $1 $( v
   $9 $6:
    $! $#
  t2=newton(G,t)
  if t2 is $- $# $* $H(t2-t)<10*h $*(lo is $# or t2>=lo)$*(hi is $# or t2<=hi):
   t=t2
 $9 $6:
  pass
 $! snap(t)
$, domain(f,x):
 conds=[]
 domconds(f,x,conds)
 if $- conds:
  $!('<',('*',-1,'$M'),x)if $3 $( 'true'
 pts=[]
 $) rel,g in conds:
  rs=$m(g,x)
  if rs is $#:
   $! $#
  if rs=='all':
   $8
  $) r in rs:
   if $t(r):
    pts.$%(r)
 pts=sortsols(dedup(pts))
 $, ok(t):
  $) rel,g in conds:
   try:
    v=$S(g,{x:t})
   $9 $6:
    $! $3
   if $/(v)is $1:
    if $H(v.imag)>1e-9:
     $! $3
    v=v.$N
   if $- relok(rel,v):
    $! $3
  $! $E
 $, okexact(p):
  $) rel,g in conds:
   try:
    v=$Q(g,x,p)
    vv=fv(v)
   $9 $6:
    $! $3
   if $H(vv)<1e-12:
    vv=0.0
   if $- relok(rel,vv):
    $! $3
  $! $E
 $e=[fv(p)$) p in pts]
 if $- $e:
  $! 'true' if ok(0.5)$( 'false'
 segs=[('I',$#,pts[0],ok($e[0]-max(1.0,$H($e[0]))))]
 $) i in $+($5(pts)):
  segs.$%(('P',pts[i],pts[i],okexact(pts[i])))
  if i+1<$5(pts):
   segs.$%(('I',pts[i],pts[i+1],ok(0.5*($e[i]+$e[i+1]))))
 segs.$%(('I',pts[-1],$#,ok($e[-1]+max(1.0,$H($e[-1])))))
 $! segs_to_bool(segs,x)
$, domconds(f,x,$?):
 if $/(f)is $- $0 or f[0]=='Q' or $4(f,x):
  $!
 h=f[0]
 if h=='^':
  b,p=f[1],f[2]
  if $C(p)$* $_(p)<0:
   $?.$%(('/=',b))
  if isq(p)$* p[2]%2==0:
   $?.$%(('>=' if $_(p)>0 $( '>',b))
 $K h in('ln','log'):
  $?.$%(('>',f[1]))
 $K h in('$~','arccos'):
  $?.$%(('<=',$[(fn('$H',f[1]),1)))
 $K h=='tan':
  $?.$%(('/=',fn('cos',f[1])))
 $) a in f[1:]:
  domconds(a,x,$?)
''')
_x(r'''import $W
$, ismat(e):
 $! $&(e,'mat')
$, $c(e):
 $! $&(e,'$I')
$, $n(M):
 $![$I(r[1:])$) r in M[1:]]
$, mk(R):
 $!('mat',)+$0(('$I',)+$0(r)$) r in R)
$, lst(xs):
 $!('$I',)+$0(xs)
$, dims(M):
 $! $5(M)-1,$5(M[1])-1
$, tomat(e):
 if ismat(e):
  $! e
 if $c(e):
  $! mk([$I(e[1:])])
 err("Matrix expected")
$, ac(e):
 $! $.($>(e))if hasdenom(e)$( $>(e)
$, m_add(A,B,sgn=1):
 if dims(A)!=dims(B):
  err("Dimension error")
 a=$n(A)
 b=$n(B)
 $! mk([[$](a[i][j],$:(sgn,b[i][j]))$) j in $+($5(a[0]))]$) i in $+($5(a))])
$, m_scale(A,c):
 $! mk([[$:(c,v)$) v in r]$) r in $n(A)])
$, m_map(A,f):
 $! mk([[f(v)$) v in r]$) r in $n(A)])
$, m_mul(A,B):
 a=$n(A)
 b=$n(B)
 if $5(a[0])!=$5(b):
  err("Dimension error")
 n=$5(b)
 $! mk([[ac($;([$:(a[i][k],b[k][j])$) k in $+(n)]))$) j in $+($5(b[0]))]$) i in $+($5(a))])
$, ident(n):
 $! mk([[1 if i==j $( 0 $) j in $+(n)]$) i in $+(n)])
$, m_pow(A,k):
 m,n=dims(A)
 if m!=n:
  err("Square matrix required")
 if k<0:
  A=m_inv(A)
  k=-k
 R=ident(n)
 $J k>0:
  if k&1:
   R=m_mul(R,A)
  k>>=1
  if k:
   A=m_mul(A,A)
 $! R
$, transpose(A):
 if $c(A):
  $! mk([[v]$) v in A[1:]])
 a=$n(A)
 $! mk([[a[i][j]$) i in $+($5(a))]$) j in $+($5(a[0]))])
$, det(A):
 a=$n(A)
 n=$5(a)
 if n!=$5(a[0]):
  err("Square matrix required")
 if n==1:
  $! a[0][0]
 if n==2:
  $! ac($[($:(a[0][0],a[1][1]),$:(a[0][1],a[1][0])))
 if n==3:
  t=[]
  $) j in $+(3):
   minor=$[($:(a[1][(j+1)%3],a[2][(j+2)%3]),$:(a[1][(j+2)%3],a[2][(j+1)%3]))
   t.$%($:(a[0][j],minor))
  $! ac($;(t))
 M=[$I(r)$) r in a]
 sign=1
 prev=1
 $) k in $+(n-1):
  if ac(M[k][k])==0:
   sw=$#
   $) i in $+(k+1,n):
    if ac(M[i][k])!=0:
     sw=i
     $T
   if sw is $#:
    $! 0
   M[k],M[sw]=M[sw],M[k]
   sign=-sign
  $) i in $+(k+1,n):
   $) j in $+(k+1,n):
    M[i][j]=ac($O($[($:(M[i][j],M[k][k]),$:(M[i][k],M[k][j])),prev))
  prev=M[k][k]
 $! ac($:(sign,M[n-1][n-1]))
$, iszero(v):
 v=ac(v)
 if v==0:
  $! $E
 if $/(v)is $A $* $H(v)<1e-13:
  $! $E
 $! $3
$, rref(A,full=$E):
 M=[$I(r)$) r in $n(A)]
 m=$5(M)
 n=$5(M[0])
 r=0
 $) c in $+(n):
  if r>=m:
   $T
  p=$#
  if hasfloat_m(M):
   $z=0.0
   $) i in $+(r,m):
    try:
     v=$H($S(M[i][c]))
    $9 $6:
     v=1.0 if $- iszero(M[i][c])$( 0.0
    if v>$z+1e-14:
     $z=v
     p=i
   if $z<1e-13:
    p=$#
  $(:
   $) i in $+(r,m):
    if $- iszero(M[i][c]):
     p=i
     $T
  if p is $#:
   $8
  M[r],M[p]=M[p],M[r]
  pv=M[r][c]
  if full:
   M[r]=[ac($O(v,pv))$) v in M[r]]
  $(:
   M[r]=[ac($O(v,pv))$) v in M[r]]
  rng=$+(m)if full $( $+(r+1,m)
  $) i in rng:
   if i!=r $* $- iszero(M[i][c]):
    f=M[i][c]
    M[i]=[ac($[(M[i][j],$:(f,M[r][j])))$) j in $+(n)]
  r+=1
 $) i in $+(m):
  $) j in $+(n):
   if $/(M[i][j])is $A $* $H(M[i][j])<1e-13:
    M[i][j]=0.0
 $! mk(M)
$, hasfloat_m(M):
 $) r in M:
  $) v in r:
   if $^(v):
    $! $E
 $! $3
$, minor(a,i,j):
 $![[a[r][c]$) c in $+($5(a))if c!=j]$) r in $+($5(a))if r!=i]
$, m_inv(A):
 m,n=dims(A)
 if m!=n:
  err("Square matrix required")
 a0=$n(A)
 if n<=3 $* $- all([$C(v)$) r in a0 $) v in r]):
  D=det(A)
  if iszero(D):
   err("Singular matrix")
  if n==1:
   $! mk([[nice(pw(D,-1))]])
  $?=[]
  $) i in $+(n):
   row=[]
   $) j in $+(n):
    c=det(mk(minor(a0,j,i)))
    if(i+j)%2:
     c=$k(c)
    row.$%(nice(ac($O(c,D))))
   $?.$%(row)
  $! mk($?)
 a=$n(A)
 aug=mk([a[i]+[1 if i==j $( 0 $) j in $+(n)]$) i in $+(n)])
 R=$n(rref(aug))
 $) i in $+(n):
  $) j in $+(n):
   if $- iszero($[(R[i][j],1 if i==j $( 0)):
    err("Singular matrix")
 $! mk([[nice(R[i][n+j])$) j in $+(n)]$) i in $+(n)])
$, trace(A):
 a=$n(A)
 $! $;([a[i][i]$) i in $+($5(a))])
$, charpoly(A,lam):
 a=$n(A)
 n=$5(a)
 if n!=$5(a[0]):
  err("Square matrix required")
 I=ident(n)
 Mk=mk([[0]*n $) _ in $+(n)])
 cs=[0]*(n+1)
 cs[n]=1
 $) k in $+(1,n+1):
  Mk=m_add(m_mul(A,Mk),m_scale(I,cs[n-k+1]))
  cs[n-k]=ac($O($k(trace(m_mul(A,Mk))),k))
 $! $;([$:(cs[k],pw(lam,k))$) k in $+(n+1)])
$, eigvl(A):
 if hasfloat_m($n(A)):
  try:
   E=m_map(A,exactify)
  $9 $6:
   E=$#
  if E is $- $# $* $- hasfloat_m($n(E)):
   $! evalf(eigvl(E))
 lam='L_'
 p=charpoly(A,lam)
 f=p
 if $- hasfloat_m($n(A)):
  try:
   f=factor_expr(p)
  $9 $6:
   f=p
  if $&(f,'hold'):
   f=f[1]
 $?=[]
 $) g in(f[1:]if $&(f,'*')$((f,)):
  k=1
  if $&(g,'^')$* $j(g[2])$* g[2]>0:
   g,k=g[1],g[2]
  if $4(g,lam):
   $8
  z=zeros(g,lam,$E)
  if z is $#:
   err("Cannot compute eigenvalues")
  z=$I(z[1:])
  d=degree(g,lam)
  $) v in z:
   m=mult(g,lam,v,d)if d is $- $# $* $5(z)<d $( 1
   $?+=[v]*(k*m)
 if $- $?:
  err("Cannot compute eigenvalues")
 $, key(v):
  if $- $2(v):
   $!(1,0.0,0.0,okey(v))
  z=$1($S(v))
  $!(0,-$H(z),-z.$N,-z.imag)
 $?.sort(key=key)
 $! lst($?)
$, mult(g,lam,v,d):
 m=1
 h=g
 $J m<d:
  h=diff_(h,lam)
  w=$Q(h,lam,v)
  if $^(w)or $^(v):
   try:
    if $H($1($S(w)))>1e-6*(1+$H($1($S(v))))**d:
     $T
   $9 $6:
    $T
  $K $- iszero(ac($>(w))):
   $T
  m+=1
 $! m
$, diff_(e,x):
 $! diff(e,x)
''')
_x(r'''$, nullspace(A):
 R=$n(rref(A))
 m=$5(R)
 n=$5(R[0])
 piv=[]
 $) i in $+(m):
  $) j in $+(n):
   if $- iszero(R[i][j]):
    piv.$%((i,j))
    $T
 pc=[j $) i,j in piv]
 free=[j $) j in $+(n)if j $- in pc]
 basis=[]
 $) f in free:
  v=[0]*n
  v[f]=1
  $) i,j in piv:
   v[j]=ac($k(R[i][f]))
  basis.$%(v)
 $! basis
$, eigvc(A):
 if hasfloat_m($n(A)):
  try:
   E=m_map(A,exactify)
  $9 $6:
   E=$#
  if E is $- $# $* $- hasfloat_m($n(E)):
   $! evalf(eigvc(E))
 $e=eigvl(A)
 n=dims(A)[0]
 cols=[]
 seen=[]
 $) lv in $e[1:]:
  if lv in seen:
   $8
  seen.$%(lv)
  if $^(lv)or hasfloat_m($n(A)):
   cols.$%(numeigvec(A,lv))
   $8
  B=m_add(A,m_scale(ident(n),lv),-1)
  B=m_map(B,$7 v:ac(v))
  ns=nullspace(B)
  $) v in ns:
   cols.$%(unitvec(v))
 if $- cols:
  err("Cannot compute eigenvectors")
 M=mk([[cols[j][i]$) j in $+($5(cols))]$) i in $+(n)])
 $) c in cols:
  $) v in c:
   if esize(v)>60:
    $! evalf(M)
 $! M
$, numeigvec(A,lam):
 a=[[$1($S(c))$) c in r]$) r in $n(A)]
 n=$5(a)
 mu=$1($S(lam))
 mu+=1e-9*(1+$H(mu))
 M=[[a[i][j]-(mu if i==j $( 0)$) j in $+(n)]$) i in $+(n)]
 x=[$1(1.0+0.37*i)$) i in $+(n)]
 $) it in $+(4):
  y=clsolve(M,x)
  big=max([$H(v)$) v in y])or 1.0
  x=[v/big $) v in y]
 nrm=$W.$V(sum([$H(v)**2 $) v in x]))or 1.0
 x=[v/nrm $) v in x]
 k=0
 $) i in $+(n):
  if $H(x[i])>$H(x[k])+1e-12:
   k=i
 ph=x[k]/$H(x[k])
 $?=[]
 $) v in x:
  v=v/ph
  re=0.0 if $H(v.$N)<1e-12 $( v.$N
  im=0.0 if $H(v.imag)<1e-12 $( v.imag
  $?.$%(re if im==0.0 $( fromcomplex($1(re,im)))
 $! $?
$, clsolve(M,b):
 n=$5(M)
 a=[$I(M[i])+[b[i]]$) i in $+(n)]
 $) c in $+(n):
  p=c
  $) r in $+(c+1,n):
   if $H(a[r][c])>$H(a[p][c]):
    p=r
  a[c],a[p]=a[p],a[c]
  if $H(a[c][c])<1e-14:
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
$, coefs(e,$?):
 if $C(e):
  $?.$%(e)
 $K $&(e,'+'):
  $) t in e[1:]:
   coefs(t,$?)
 $K $&(e,'*')$* $C(e[1]):
  $?.$%(e[1])
 $(:
  $?.$%(1)
$, unitvec(v):
 if hasfloat_m([v]):
  nrm=$V($;([$:(c,fn('conj',c))$) c in v]))
  $![nice(ac($O(c,nrm)))$) c in v]
 cs=[]
 $) c in v:
  coefs(c,cs)
 den=1
 num=0
 $) q in cs:
  if $r(q)$* q!=0:
   a,b=nd(q)
   den=ilcm(den,b)
   num=igcd(num,a)
 k=Q(den,num)if num $( 1
 $) c in v:
  if $- iszero(c):
   if isneg(c):
    k=$k(k)
   $T
 w=[ac($>($:(k,c)))$) c in v]
 n2=ac($>($;([$:(c,fn('conj',c))$) c in w])))
 r=$V(n2)
 if $C(r)or $- $&(r,'^'):
  $![ac($O(c,r))$) c in w]
 inv=('^',r[1],$k(r[2]))
 $![c if iszero(c)$(('*',c,inv)if $&(c,'+')$( $:(c,inv)$) c in w]
$, esize(e):
 if $/(e)is $- $0 or e[0]=='Q':
  $! 1
 k=1
 $) a in e[1:]:
  k+=esize(a)
 $! k
$, lu(A):
 a=[$I(r)$) r in $n(A)]
 m=$5(a)
 n=$5(a[0])
 L=[[1 if i==j $( 0 $) j in $+(m)]$) i in $+(m)]
 P=$I($+(m))
 U=a
 $) k in $+(min(m,n)):
  p=$#
  if hasfloat_m(U):
   $z=-1.0
   $) i in $+(k,m):
    v=$H($S(U[i][k]))
    if v>$z:
     $z=v
     p=i
   if $z<1e-14:
    p=$#
  $(:
   $) i in $+(k,m):
    if $- iszero(U[i][k]):
     p=i
     $T
  if p is $#:
   $8
  if p!=k:
   U[k],U[p]=U[p],U[k]
   P[k],P[p]=P[p],P[k]
   $) j in $+(k):
    L[k][j],L[p][j]=L[p][j],L[k][j]
  $) i in $+(k+1,m):
   f=ac($O(U[i][k],U[k][k]))
   L[i][k]=f
   U[i]=[ac($[(U[i][j],$:(f,U[k][j])))$) j in $+(n)]
 Pm=[[1 if P[i]==j $( 0 $) j in $+(m)]$) i in $+(m)]
 $! mk(L),mk(U),mk(Pm)
$, qr(A):
 a=$n(A)
 m=$5(a)
 n=$5(a[0])
 cols=[[a[i][j]$) i in $+(m)]$) j in $+(n)]
 Qc=[]
 R=[[0]*n $) _ in $+(n)]
 $) j in $+(n):
  v=cols[j]
  $) k in $+($5(Qc)):
   r=ac($;([$:(Qc[k][i],v[i])$) i in $+(m)]))
   R[k][j]=r
   v=[ac($[(v[i],$:(r,Qc[k][i])))$) i in $+(m)]
  nrm=nice($V(ac($;([pw(c,2)$) c in v]))))
  R[j][j]=nrm
  if iszero(nrm):
   Qc.$%([0]*m)
  $(:
   Qc.$%([nice(ac($O(c,nrm)))$) c in v])
 Qm=mk([[Qc[j][i]$) j in $+(n)]$) i in $+(m)])
 $! Qm,mk(R)
$, crossp(u,v):
 a=vec(u)
 b=vec(v)
 if $5(a)==2:
  a=a+[0]
  b=b+[0]
 if $5(a)!=3 or $5(b)!=3:
  err("Dimension error")
 r=[ac($[($:(a[1],b[2]),$:(a[2],b[1]))),
 ac($[($:(a[2],b[0]),$:(a[0],b[2]))),
 ac($[($:(a[0],b[1]),$:(a[1],b[0])))]
 $! revec(r,u)
$, vec(u):
 if $c(u):
  $! $I(u[1:])
 if ismat(u):
  R=$n(u)
  if $5(R)==1:
   $! R[0]
  if $5(R[0])==1:
   $![r[0]$) r in R]
 err("Vector expected")
$, revec(r,like):
 if $c(like):
  $! lst(r)
 R=$n(like)
 if $5(R)==1:
  $! mk([r])
 $! mk([[v]$) v in r])
$, dotp(u,v):
 a=vec(u)
 b=vec(v)
 if $5(a)!=$5(b):
  err("Dimension error")
 $! ac($;([$:(a[i],b[i])$) i in $+($5(a))]))
$, norm(A):
 if $c(A)or ismat(A)$*(dims(A)[0]==1 or dims(A)[1]==1):
  v=vec(A)
  $! nice($V(ac($;([$:(c,fn('conj',c))$) c in v]))))
 $! nice($V(ac($;([$:(c,fn('conj',c))$) r in $n(A)$) c in r]))))
$, unitv(u):
 nrm=norm(u)
 $! revec([nice(ac($O(c,nrm)))$) c in vec(u)],u)
$, rownorm(A):
 if $- ismat(A):
  err('Argument must be a matrix')
 $! maxexpr([ac($;([fn('$H',c)$) c in r]))$) r in $n(A)])
$, colnorm(A):
 if $- ismat(A):
  err('Argument must be a matrix')
 $! rownorm(transpose(A))
$, maxexpr(xs):
 $z=$#
 bv=$#
 $) x in xs:
  v=$S(x)
  if $z is $# or v>bv:
   $z=x
   bv=v
 $! $z
''')
_x(r'''$, augment(A,B):
 if $c(A)$* $c(B):
  $! A+B[1:]
 a=$n(tomat(A))
 b=$n(tomat(B))
 if $5(a)!=$5(b):
  err("Dimension error")
 $! mk([a[i]+b[i]$) i in $+($5(a))])
$, colaugment(A,B):
 a=$n(tomat(A))
 b=$n(tomat(B))
 if $5(a[0])!=$5(b[0]):
  err("Dimension error")
 $! mk(a+b)
$, submat(A,r1=1,c1=1,r2=$#,c2=$#):
 a=$n(A)
 if r2 is $#:
  r2=$5(a)
 if c2 is $#:
  c2=$5(a[0])
 $! mk([a[i][c1-1:c2]$) i in $+(r1-1,r2)])
$, rowswap(A,i,j):
 a=$n(A)
 a[i-1],a[j-1]=a[j-1],a[i-1]
 $! mk(a)
$, rowadd(A,i,j):
 a=$n(A)
 a[j-1]=[$](a[j-1][k],a[i-1][k])$) k in $+($5(a[0]))]
 $! mk(a)
$, mrow(c,A,i):
 a=$n(A)
 a[i-1]=[$:(c,v)$) v in a[i-1]]
 $! mk(a)
$, mrowadd(c,A,i,j):
 a=$n(A)
 a[j-1]=[ac($](a[j-1][k],$:(c,a[i-1][k])))$) k in $+($5(a[0]))]
 $! mk(a)
$, diag(A):
 if $c(A):
  n=$5(A)-1
  $! mk([[A[i+1]if i==j $( 0 $) j in $+(n)]$) i in $+(n)])
 a=$n(A)
 if $5(a)==1 or $5(a[0])==1:
  v=vec(A)
  $! diag(lst(v))
 $! lst([a[i][i]$) i in $+(min($5(a),$5(a[0])))])
$, matlist(A):
 $! lst([v $) r in $n(A)$) v in r])
$, listmat(L,c=$#):
 xs=$I(L[1:])
 if c is $#:
  c=$5(xs)
 if $- $j(c)or c<1:
  err('Invalid number of columns')
 $?=[]
 $J xs:
  r=xs[:c]
  xs=xs[c:]
  $J $5(r)<c:
   r.$%(0)
  $?.$%(r)
 $! mk($?)
$, simult(A,b):
 a=$n(A)
 n=$5(a)
 bb=$n(tomat(b))if ismat(b)$([[v]$) v in b[1:]]
 if $5(bb)!=n:
  bb=$n(transpose(b))
 k=$5(bb[0])
 R=$n(rref(mk([a[i]+bb[i]$) i in $+(n)])))
 $) i in $+(n):
  if iszero(R[i][i]):
   err("Singular matrix")
 $! mk([[nice(R[i][n+j])$) j in $+(k)]$) i in $+(n)])
$, cumsum(L):
 if $c(L):
  $?=[]
  s=0
  $) v in L[1:]:
   s=$](s,v)
   $?.$%(s)
  $! lst($?)
 a=$n(L)
 $?=[]
 acc=[0]*$5(a[0])
 $) r in a:
  acc=[$](acc[j],r[j])$) j in $+($5(r))]
  $?.$%($I(acc))
 $! mk($?)
$, polar_vec(u):
 v=vec(u)
 if $5(v)==2:
  r=nice($V(ac($](pw(v[0],2),pw(v[1],2)))))
  th=fn('$p',$](v[0],$:('i',v[1])))
  $!('${','['+fmtx(r)+' \u2220'+fmtx(th)+']')
 err("Dimension error")
$, fmtx(e):
 $! fmt(e)
$, cylind(u):
 v=vec(u)
 if $5(v)!=3:
  err("Dimension error")
 r=nice($V(ac($](pw(v[0],2),pw(v[1],2)))))
 th=fn('$p',$](v[0],$:('i',v[1])))
 $!('${','['+fmtx(r)+' \u2220'+fmtx(th)+' '+fmtx(v[2])+']')
$, sphere(u):
 v=vec(u)
 if $5(v)!=3:
  err("Dimension error")
 rho=nice($V(ac($](pw(v[0],2),pw(v[1],2),pw(v[2],2)))))
 th=fn('$p',$](v[0],$:('i',v[1])))
 ph=fn('arccos',$O(v[2],rho))if rho!=0 $( 0
 $!('${','['+fmtx(rho)+' \u2220'+fmtx(th)+' \u2220'+fmtx(ph)+']')
$, lsum(L,a=1,b=$#):
 xs=$I(L[1:])
 if b is $#:
  b=$5(xs)
 $! $;(xs[a-1:b])
$, lprod(L,a=1,b=$#):
 xs=$I(L[1:])
 if b is $#:
  b=$5(xs)
 $! $G(xs[a-1:b])
$, mean(L,F=$#):
 xs=$I(L[1:])
 if F is $#:
  $! $O($;(xs),$5(xs))
 fs=$I(F[1:])
 $! $O($;([$:(xs[i],fs[i])$) i in $+($5(xs))]),$;(fs))
$, sortkey(v):
 try:
  x=$S(v)
  $! x.$N if $/(x)is $1 $( x
 $9 $6:
  $! 0.0
$, median(L):
 xs=sorted($I(L[1:]),key=sortkey)
 n=$5(xs)
 if n%2:
  $! xs[n//2]
 $! $O($](xs[n//2-1],xs[n//2]),2)
$, variance(L,pop=$3):
 xs=$I(L[1:])
 n=$5(xs)
 m=mean(L)
 s=$;([pw($[(v,m),2)$) v in xs])
 $! ac($O(s,n if pop $( n-1))
$, stddev(L,pop=$3):
 $! nice($V(variance(L,pop)))
$, sorta(L):
 $! lst(sorted($I(L[1:]),key=sortkey))
$, sortd(L):
 $! lst(sorted($I(L[1:]),key=sortkey,reverse=$E))
$, deltalist(L):
 xs=$I(L[1:])
 $! lst([$[(xs[i+1],xs[i])$) i in $+($5(xs)-1)])
''')
_x(r'''SET={'$p':'rad','mode':'auto','$@':'$N'}
$, lmap(f,a):
 if $c(a):
  $!('$I',)+$0(lmap(f,v)$) v in a[1:])
 if ismat(a):
  $!('mat',)+$0(lmap(f,r)$) r in a[1:])
 $! f(a)
$, lmap2(f,a,b):
 if $c(a)$* $c(b):
  if $5(a)!=$5(b):
   err("Dimension error")
  $!('$I',)+$0(lmap2(f,a[i],b[i])$) i in $+(1,$5(a)))
 if $c(a):
  $!('$I',)+$0(lmap2(f,v,b)$) v in a[1:])
 if $c(b):
  $!('$I',)+$0(lmap2(f,a,v)$) v in b[1:])
 if ismat(a)$* ismat(b):
  $!('mat',)+$0(lmap2(f,a[i],b[i])$) i in $+(1,$5(a)))
 if ismat(a):
  $!('mat',)+$0(lmap2(f,r,b)$) r in a[1:])
 if ismat(b):
  $!('mat',)+$0(lmap2(f,a,r)$) r in b[1:])
 $! f(a,b)
$, vadd(a,b):
 if ismat(a)$* ismat(b):
  $! m_add(a,b)
 if $c(a)or $c(b)or ismat(a)or ismat(b):
  $! lmap2($],a,b)
 if isrel(a)or isrel(b):
  $! relop($],a,b)
 if isstr(a)or isstr(b):
  err("Data $/ error")
 $! $](a,b)
$, vsub(a,b):
 $! vadd(a,vneg(b))
$, vneg(a):
 $! lmap($k,a)if $- isrel(a)$((a[0],$k(a[1]),$k(a[2]))
$, vmul(a,b):
 if ismat(a)$* ismat(b):
  $! m_mul(a,b)
 if ismat(a)$* $c(b)or $c(a)$* ismat(b):
  $! m_mul(tomat(a),tomat(b)if ismat(b)$( transpose(b))
 if $c(a)or $c(b)or ismat(a)or ismat(b):
  $! lmap2($:,a,b)
 if isrel(a)or isrel(b):
  $! relop($:,a,b)
 $! $:(a,b)
$, vdiv(a,b):
 if ismat(b):
  if ismat(a):
   $! m_mul(a,m_inv(b))
  $! vmul(a,m_inv(b))
 if $c(a)or $c(b)or ismat(a):
  $! lmap2($O,a,b)
 if isrel(a)or isrel(b):
  $! relop($O,a,b)
 if b==0 $* $2(a):
  $! '$F'
 $! $O(a,b)
$, vpow(a,b):
 if ismat(a):
  if $/(b)is $w:
   $! m_pow(a,b)
  if b=='T_t':
   $! transpose(a)
  err("Domain error")
 if $c(a)or $c(b):
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
 $! $&(e,'${')
$, dotop(op,a,b):
 if op=='.*':
  $! lmap2($:,a,b)
 if op=='./':
  $! lmap2($O,a,b)
 $! lmap2(pw,a,b)
$, rel(op,a,b):
 if $c(a)or $c(b):
  $! lmap2($7 x,y:rel(op,x,y),a,b)
 if isstr(a)$* isstr(b):
  r=cmpstr(op,a[1],b[1])
  if r is $- $#:
   $! 'true' if r $( 'false'
 d=$.($[(a,b))if $-(isstr(a)or isstr(b))$( $#
 if d is $- $# $* $2(d)$* d!='$F':
  try:
   v=$S(d)
  $9 $6:
   v=$#
  if v is $- $#:
   if $/(v)is $1:
    if op=='=':
     $! 'true' if $H(v)<1e-13 $( 'false'
    if op=='/=':
     $! 'false' if $H(v)<1e-13 $( 'true'
    err("Non-$N comparison")
   if d==0 or $H(v)<1e-300:
    v=0.0
   $(:
    try:
     sc=$H($S(a))+$H($S(b))
    $9 $6:
     sc=0.0
    if $H(v)<1e-12*(1+sc):
     v=0.0
   r={'=':v==0,'/=':v!=0,'<':v<0,'>':v>0,'<=':v<=0,'>=':v>=0}[op]
   $! 'true' if r $( 'false'
 if d is $- $# $* op in('=','/=')$* $- $2(d):
  try:
   z=expand_full(d)if hasattr(PO,'expand_full')$( $>(d)
  $9 $6:
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
  $! $E
 if v=='false':
  $! $3
 $! $#
$, land(a,b):
 ta=tobool(a)
 tb=tobool(b)
 if ta is $3 or tb is $3:
  $! 'false'
 if ta is $E:
  $! b
 if tb is $E:
  $! a
 $! flat('$*',a,b)
$, lor(a,b):
 ta=tobool(a)
 tb=tobool(b)
 if ta is $E or tb is $E:
  $! 'true'
 if ta is $3:
  $! b
 if tb is $3:
  $! a
 $! flat('or',a,b)
$, flat(op,a,b):
 xs=[]
 $) v in(a,b):
  if $&(v,op):
   xs.extend(v[1:])
  $(:
   xs.$%(v)
 $!(op,)+$0(xs)
$, lnot(a):
 t=tobool(a)
 if t is $- $#:
  $! 'false' if t $( 'true'
 if $j(a):
  $!~a
 neg_={'<':'>=','>':'<=','<=':'>','>=':'<','=':'/=','/=':'='}
 if isrel(a):
  $!(neg_[a[0]],a[1],a[2])
 $!('$-',a)
$, lxor(a,b):
 ta=tobool(a)
 tb=tobool(b)
 if ta is $- $# $* tb is $- $#:
  $! 'true' if ta!=tb $( 'false'
 if $j(a)$* $j(b):
  $! a^b
 $!('xor',a,b)
$, need_int(n):
 if isfl(n)$* finite(n)$* n==$W.floor(n):
  $! $w(n)
 if $- $j(n):
  err("Argument must be an integer")
 $! n
$, gcd_(a,b):
 if $r(a)$* $r(b):
  an,ad=nd(a)
  bn,bd=nd(b)
  $! Q(igcd(an,bn),ilcm(ad,bd))
 if isfl(a)or isfl(b):
  $! $A(igcd($w(a),$w(b)))
 $! poly_gcd_expr(a,b)
$, lcm_(a,b):
 if $r(a)$* $r(b):
  an,ad=nd(a)
  bn,bd=nd(b)
  $! Q(ilcm(an,bn),igcd(ad,bd))
 g=gcd_(a,b)
 $! $.($O($:(a,b),g))
$, mod_(a,b):
 if $&(a,'^')$* $j(a[1])$* $j(a[2])$* a[2]>0 $* $j(b)$* b!=0:
  r=powmod(a[1],a[2],$H(b))
  $! r-$H(b)if b<0 $* r $( r
 if $C(a)$* $C(b):
  if b==0:
   $! a
  $! nsub(a,nmul(b,nfloor(ndiv(a,b))))
 $!('mod',a,b)
$, remain_(a,b):
 if $C(a)$* $C(b):
  if b==0:
   $! a
  q=ndiv(a,b)
  t=nfloor(q)if $_(q)>=0 $(-nfloor(nneg(q))
  $! nsub(a,nmul(b,t))
 $!('remain',a,b)
$, intdiv_(a,b):
 q=ndiv(a,b)
 if $_(q)>=0:
  $! nfloor(q)
 $!-nfloor(nneg(q))
$, bigcomb(n,k):
 if $-($j(n)$* $j(k))or k<=0:
  $! $3
 m=min(k,$H(n-k))if n>=k $( k
 $! m*ibits(n)>MAXBITS
$, ncr_(n,k):
 if $j(n)$* $j(k):
  if k<0 or(n>=0 $* k>n):
   $! 0
  if bigcomb(n,k):
   $!('ncr',n,k)
  $! binom(n,k)if n>=0 $( gen_ncr(n,k)
 if $j(k)$* k>=0:
  $! gen_ncr(n,k)
 if isfl(n)or isfl(k):
  $! CA_gamma_ratio(n,k)
 $!('ncr',n,k)
$, gen_ncr(n,k):
 r=1
 $) i in $+(k):
  r=$:(r,$[(n,i))
 f=1
 $) i in $+(2,k+1):
  f*=i
 $! $:(r,Q(1,f))
''')
_x(r'''$, npr_(n,k):
 if $j(n)$* $j(k)$* k*ibits(n)>MAXBITS:
  $!('npr',n,k)
 if $j(k)$* k>=0:
  r=1
  $) i in $+(k):
   r=$:(r,$[(n,i))
  $! r
 $!('npr',n,k)
$, CA_gamma_ratio(n,k):
 n=tofl(n)
 k=tofl(k)
 $! gamma(n+1)/(gamma(k+1)*gamma(n-k+1))
$, isprime_(n):
 n=need_int(n)
 if $H(n)>>1024:
  err('Number too large $) isPrime')
 $! 'true' if isprime($H(n))$( 'false'
$, round_(x,d=0):
 if $2(x)$* $- $C(x):
  x=evalf(x)
 if $C(x):
  if $r(x)$* d==0:
   $! nfloor(nadd(x,$s))if $_(x)>=0 $(-nfloor(nadd(nneg(x),$s))
  v=tofl(x)
  if $- finite(v):
   $! x
  p=10.0**d
  r=$W.floor($H(v)*p+0.5)/p
  $! r if v>=0 $(-r
 $!('round',x,d)
$, ipart_(x):
 if $2(x)$* $- $C(x):
  x=evalf(x)
 if $C(x):
  if $/(x)is $A:
   $! $A($w(x))
  $! nfloor(x)if $_(x)>=0 $(-nfloor(nneg(x))
 $!('ipart',x)
$, fpart_(x):
 i=ipart_(x)
 if $&(i,'ipart'):
  $!('fpart',x)
 $! $[(x,i)
$, approx_(e):
 $! evalf(e)
$, exact_(e,tol=$#):
 if tol is $- $#:
  tol=tofl(tol)
 $! exactify(e,tol)
$, approxfraction(e,tol=$#):
 t=tofl(tol)if tol is $- $# $( 5e-14
 $! lmap($7 v:float2rat(tofl(evalf(v)),t)if $2(v)$( exactify(v,t),e)
$, left_(e,n=$#):
 if isrel(e):
  $! e[1]
 if $c(e):
  $!('$I',)+e[1:1+n]
 if isstr(e):
  $!('${',e[1][:n])
 err("Argument error")
$, right_(e,n=$#):
 if isrel(e):
  $! e[2]
 if $c(e):
  $!('$I',)+(e[$5(e)-n:]if n $(())
 if isstr(e):
  $!('${',e[1][$5(e[1])-n:]if n $( '')
 err("Argument error")
$, mid_(e,start,n=$#):
 if isstr(e):
  s=e[1][start-1:]
  $!('${',s if n is $# $( s[:n])
 xs=$I(e[1:])[start-1:]
 $!('$I',)+$0(xs if n is $# $( xs[:n])
$, dim_(e):
 if $c(e):
  $! $5(e)-1
 if ismat(e):
  r,c=dims(e)
  $!('$I',r,c)
 if isstr(e):
  $! $5(e[1])
 err("Argument error")
$, max_(a,b=$#):
 if b is $#:
  xs=$I(a[1:])if $c(a)$([a]
  $! maxexpr(xs)
 $! lmap2($7 x,y:x if cmpv(x,y)>=0 $( y,a,b)
$, min_(a,b=$#):
 if b is $#:
  xs=$I(a[1:])if $c(a)$([a]
  $z=$#
  bv=$#
  $) x in xs:
   v=$S(x)
   if $z is $# or v<bv:
    $z=x
    bv=v
  $! $z
 $! lmap2($7 x,y:x if cmpv(x,y)<=0 $( y,a,b)
$, cmpv(x,y):
 if $2(x)$* $2(y):
  d=$S($[(x,y))
  d=d.$N if $/(d)is $1 $( d
  $! 1 if d>0 $((-1 if d<0 $( 0)
 err("Cannot compare")
$, when_(c,a,b=$#,u=$#):
 if b=='$F':
  b=$#
 t=tobool(c)
 if t is $E:
  $! a
 if t is $3:
  $! b if b is $- $# $( '$F'
 if b is $#:
  $!('when',c,a)
 if u is $#:
  $!('when',c,a,b)
 $! u
$, piecewise_(*a):
 a=$I(a)
 if $5(a)<2:
  err('Wrong number of arguments')
 if $5(a)%2==1:
  r=a[-1]
  a=a[:-1]
 $(:
  r=$#
 $) i in $+($5(a)-2,-1,-2):
  r=when_(a[i+1],a[i],r)
 $! r
$, string_(e):
 if isstr(e):
  $! e
 $!('${',fmt(e))
$, char_(n):
 $!('${',chr(need_int(n)))
$, ord_(s):
 $! ord(s[1][0])
$, instring_(s,t,start=1):
 i=s[1].find(t[1],start-1)
 $! i+1
$, polyeval(L,x):
 r=0
 $) c in L[1:]:
  r=$]($:(r,x),c)
 $! $>(r)
$, randpoly(v,n):
 import random
 $! $;([$:(random.randint(-9,9),pw(v,k))$) k in $+(n+1)])
$, randmat(r,c):
 import random
 $! mk([[random.randint(-9,9)$) _ in $+(c)]$) _ in $+(r)])
$, newmat(r,c):
 $! mk([[0]*c $) _ in $+(r)])
$, newlist(n):
 $!('$I',)+(0,)*n
$, rand_(n=$#):
 import random
 if n is $#:
  $! random.random()
 $!('$I',)+$0(random.random()$) _ in $+(n))
$, randint_(a,b,n=$#):
 import random
 if n is $#:
  $! random.randint(a,b)
 $!('$I',)+$0(random.randint(a,b)$) _ in $+(n))
$, count_(*$Y):
 n=0
 $) a in $Y:
  n+=($5(a)-1)if $c(a)$( 1
 $! n
$, erf(x):
 if $H(x)<2.5:
  s=0.0
  t=x
  k=0
  $J $E:
   term=t/(2*k+1)
   s+=term
   k+=1
   t=-t*x*x/k
   if $H(term)<1e-17:
    $T
  $! 2/$W.$V($W.pi)*s
 z=$H(x)
 t=0.0
 $) k in $+(60,0,-1):
  t=(k/2.0)/(z+t)
 erfc=$W.exp(-z*z)/$W.$V($W.pi)/(z+t)
 $!(1-erfc)if x>0 $((erfc-1)
$, numarg(v):
 if v=='$M':
  $! $A('$M')
 if v==('*',-1,'$M'):
  $! $A('-$M')
 if $2(v):
  x=cv(v)if $- $C(v)$( tofl(v)
  if x is $- $# $* $/(x)is $- $1:
   $! x
 err('Numeric argument required')
$, normcdf(lo,hi,mu=0.0,sig=1.0):
 mu=numarg(mu)
 sig=numarg(sig)
 $, F(v):
  if v=='$M':
   $! 1.0
  if v==('*',-1,'$M'):
   $! 0.0
  z=(numarg(v)-mu)/sig
  $! 0.5*(1+erf(z/$W.$V(2)))
 $! F(hi)-F(lo)
$, normpdf(x,mu=0.0,sig=1.0):
 x=numarg(x)
 s=numarg(sig)
 $! $W.exp(-0.5*((x-numarg(mu))/s)**2)/(s*$W.$V(2*$W.pi))
$, invnorm(p,mu=0.0,sig=1.0):
 p=numarg(p)
 mu=numarg(mu)
 sig=numarg(sig)
 if $- 0<p<1:
  err('Area must be between 0 $* 1')
 lo,hi=-40.0,40.0
 $) _ in $+(200):
  m=0.5*(lo+hi)
  if 0.5*(1+erf(m/$W.$V(2)))<p:
   lo=m
  $(:
   hi=m
 $! mu+sig*0.5*(lo+hi)
$, binompdf(n,p,x=$#):
 if x is $#:
  $!('$I',)+$0(binompdf(n,p,k)$) k in $+(n+1))
 if $r(p):
  $! $:(binom(n,x),pw(p,x),pw($[(1,p),n-x))
 p=tofl(p)
 $! binom(n,x)*p**x*(1-p)**(n-x)
$, binomcdf(n,p,a,b=$#):
 if b is $#:
  a,b=0,a
 $! $;([binompdf(n,p,k)$) k in $+($w(a),$w(b)+1)])
$, poisspdf(lam,x):
 $! evalf($:(pw(lam,x),pw('e',$k(lam)),Q(1,fact_int(x))))
$, poisscdf(lam,a,b=$#):
 if b is $#:
  a,b=0,a
 $! $;([poisspdf(lam,k)$) k in $+($w(a),$w(b)+1)])
$, geompdf(p,x):
 $! $:(p,pw($[(1,p),x-1))
$, geomcdf(p,a,b=$#):
 if b is $#:
  a,b=1,a
 $! $;([geompdf(p,k)$) k in $+($w(a),$w(b)+1)])
$, fact_int(n):
 r=1
 $) k in $+(2,n+1):
  r*=k
 $! r
$, toang(x):
 a=SET['$p']
 if a=='deg':
  $! $:(x,$O('pi',180))
 if a=='grad':
  $! $:(x,$O('pi',200))
 $! x
''')
_x(r'''$, fromang(x):
 a=SET['$p']
 if a=='deg':
  $! $>($:(x,$O(180,'pi')))
 if a=='grad':
  $! $>($:(x,$O(200,'pi')))
 $! x
TRIG=('sin','cos','tan','sec','csc','cot')
ITRIG=('$~','arccos','$x','arcsec','arccsc','arccot')
$, mathfn($B):
 $, f(*a):
  if $B in TRIG $* SET['$p']!='rad':
   $! lmap($7 u:fn($B,toang(u)),a[0])
  if $B in ITRIG $* SET['$p']!='rad':
   $! lmap($7 u:fromang(fn($B,u)),a[0])
  if $5(a)==1:
   $! lmap($7 u:fn($B,u),a[0])
  $! fn($B,*a)
 $! f
$, angle_fn(z):
 $! lmap($7 u:fromang(fn('$p',u)),z)
F={}
$) _n in('sin','cos','tan','sec','csc','cot','$~','arccos',
 '$x','arcsec','arccsc','arccot','sinh','cosh','tanh',
 'sech','csch','coth','arcsinh','arccosh','arctanh',
 'arcsech','arccsch','arccoth','ln','exp','$H','sign',
 'floor','ceiling','$N','imag','conj','fact'):
 F[_n]=mathfn(_n)
ALIAS={'asin':'$~','acos':'arccos','atan':'$x','asinh':'arcsinh',
 'acosh':'arccosh','atanh':'arctanh','ceil':'ceiling',
 'factorial':'fact','derivative':'d','$Z':'$Z',
 'int_':'$Z','sumseq':'sumseq','prodseq':'prodseq',
 'lim':'$v','nderiv':'nderivative','polycoef':'polycoeffs',
 'stddevsamp':'stddev','varsamp':'variance','cumsum':'cumulativesum',
 'nsolve':'nsolve','arg':'$p','inv':'inverse','mat2list':'matlist',
 'list2mat':'listmat','explist':'explist','tran':'transpose',
 'log10':'log10','sqr':'$V','diff':'d','deriv':'d',
 'differentiate':'d','integrate':'$Z','avg':'mean',
 'average':'mean'}
F['$V']=$7 u:lmap($V,u)
F['root']=$7 u,n=2:lmap($7 v:fn('root',v,n),u)
F['cbrt']=$7 u:lmap($7 v:fn('root',v,3),u)
F['log']=$7 u,b=$#:lmap($7 v:fn('ln',v)if b is $# $( fn('log',v,b),u)
F['atan2']=$7 y,x:lmap2($7 b,a:fromang(fn('$p',$](a,$:('i',b)))),y,x)
F['log10']=$7 u:lmap($7 v:fn('log',v,10),u)
F['$p']=angle_fn
F['round']=$7 x,d=0:lmap($7 v:round_(v,d),x)
F['ipart']=$7 x:lmap(ipart_,x)
F['$w']=$7 x:lmap($7 v:fn('floor',v),x)
F['fpart']=$7 x:lmap(fpart_,x)
F['gcd']=$7 a,b:lmap2(gcd_,a,b)
F['lcm']=$7 a,b:lmap2(lcm_,a,b)
F['mod']=$7 a,b:lmap2(mod_,a,b)
F['remain']=$7 a,b:lmap2(remain_,a,b)
F['intdiv']=$7 a,b:lmap2(intdiv_,a,b)
F['ncr']=$7 a,b:lmap2(ncr_,a,b)
F['npr']=$7 a,b:lmap2(npr_,a,b)
F['isprime']=isprime_
F['approx']=approx_
F['exact']=exact_
F['approxrational']=approxfraction
F['getnum']=$7 e:lmap(getnum,e)
F['getdenom']=$7 e:lmap(getden,e)
F['polyeval']=polyeval
F['polygcd']=$7 a,b:poly_gcd_expr(a,b)
F['randpoly']=randpoly
F['texpand']=$7 e:lmap($7 v:texpand(v),e)
F['tcollect']=$7 e:lmap($7 v:tcollect(v),e)
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
F['rref']=$7 A,tol=$#:rref(A,$E)
F['ref']=$7 A,tol=$#:ref_(A)
F['inverse']=m_inv
F['rowdim']=$7 A:dims(A)[0]
F['coldim']=$7 A:dims(A)[1]
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
F['lu']=$7 A,tol=$#:('$I',)+lu(A)
F['qr']=$7 A,tol=$#:('$I',)+qr(A)
F['newmat']=newmat
F['newlist']=newlist
F['randmat']=randmat
F['matlist']=matlist
F['listmat']=listmat
F['simult']=simult
F['cumulativesum']=cumsum
F['sum']=$7 L,a=1,b=$#:lsum(L,a,b)if $c(L)$( colwise(L,lsum)
F['product']=$7 L,a=1,b=$#:lprod(L,a,b)if $c(L)$( colwise(L,lprod)
F['mean']=$7 L,f=$#:mean(L,f)if $c(L)$( colwise(L,mean)
F['median']=median
F['stddev']=$7 L:stddev(L)
F['stddevpop']=$7 L:stddev(L,$E)
F['variance']=$7 L:variance(L)
F['varpop']=$7 L:variance(L,$E)
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
F['getmode']=$7*a:('${','$p='+SET['$p']+' mode='+SET['mode']+' $@='+SET['$@'])
$, colwise(M,f):
 cols=$n(transpose(M))
 $! mk([[f(('$I',)+$0(c))$) c in cols]])
$, ref_(A):
 $! rref(A,$3)
$, conv(e,$B,$Y):
 if $B=='decimal':
  $! evalf(e)
 if $B=='approxfraction':
  $! approxfraction(e,$Y[0]if $Y $( $#)
 if $B in('dms','dd','rad','grad','deg'):
  $! angconv(e,$B)
 if $B=='polar':
  if $c(e)or ismat(e):
   $! polar_vec(e)
  r=$.(fn('$H',e))
  th=fn('$p',e)
  $!('${','('+fmt(r)+'\u2220'+fmt(fromang(th))+')')
 if $B=='rect':
  if $c(e)or ismat(e):
   $! e
  r,i=reim(e)
  $! $](r,$:('i',i))
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
  $! tologbase(e,$Y[0])
 if $B=='sin':
  $! pyth_to(e,'sin')
 if $B=='cos':
  $! pyth_to(e,'cos')
 err("Unknown conversion "+$B)
''')
_x(r'''$, angconv(e,$B):
 if $B=='dms':
  v=tofl(evalf(e))
  if SET['$p']=='rad':
   v=v*180/$W.pi
  $K SET['$p']=='grad':
   v=v*0.9
  sg='-' if v<0 $( ''
  v=$H(v)
  d=$w(v)
  m=$w((v-d)*60)
  s=((v-d)*60-m)*60
  if s>59.9999995:
   s=0.0
   m+=1
  if m==60:
   m=0
   d+=1
  ss=('%.4f'%s).rstrip('0').rstrip('.')
  $!('${',sg+${(d)+'\u00b0'+${(m)+"'"+ss+'"')
 if $B=='dd':
  if SET['$p']=='rad':
   $! evalf($:(e,$O(180,'pi')))
  $! evalf(e)
 if $B=='rad':
  if SET['$p']=='deg':
   $! $:(e,$O('pi',180))
  if SET['$p']=='grad':
   $! $:(e,$O('pi',200))
  $! e
 if $B=='grad':
  if SET['$p']=='deg':
   $! $:(e,Q(10,9))
  if SET['$p']=='rad':
   $! $:(e,$O(200,'pi'))
  $! e
 if SET['$p']=='rad':
  $! $:(e,$O(180,'pi'))
 $! e
$, baseconv(e,$B):
 n=need_int(e)
 if $B=='base10':
  $! n
 if $B=='base2':
  s=bin(n)if n>=0 $( '-'+bin(-n)
  $!('${',s.replace('0b','0b'))
 s=hex(n)if n>=0 $( '-'+hex(-n)
 $!('${',s.replace('0x','0h').upper().replace('0H','0h'))
$, toexp(e):
 if $/(e)is $- $0 or e[0]=='Q':
  $! e
 $Y=[toexp(a)$) a in e[1:]]
 h=e[0]
 if $5($Y)==1:
  u=$Y[0]
  if h=='sinh':
   $! $:($s,$[(pw('e',u),pw('e',$k(u))))
  if h=='cosh':
   $! $:($s,$](pw('e',u),pw('e',$k(u))))
  if h=='tanh':
   $! $O($[(pw('e',u),pw('e',$k(u))),$](pw('e',u),pw('e',$k(u))))
  if h=='sin':
   iu=$:('i',u)
   $! $O($[(pw('e',iu),pw('e',$k(iu))),$:(2,'i'))
  if h=='cos':
   iu=$:('i',u)
   $! $:($s,$](pw('e',iu),pw('e',$k(iu))))
  if h=='arcsinh':
   $! fn('ln',$](u,$V($](pw(u,2),1))))
  if h=='arccosh':
   $! fn('ln',$](u,$V($[(pw(u,2),1))))
  if h=='arctanh':
   $! $:($s,fn('ln',$O($](1,u),$[(1,u))))
 $! simp((h,)+$0($Y))
$, toln(e):
 if $/(e)is $- $0 or e[0]=='Q':
  $! e
 $Y=[toln(a)$) a in e[1:]]
 if e[0]=='log':
  b=$Y[1]if $5($Y)>1 $( 10
  $! $O(fn('ln',$Y[0]),fn('ln',b))
 $! simp((e[0],)+$0($Y))
$, tologbase(e,b):
 e=toln(e)
 $, walk(t):
  if $/(t)is $- $0 or t[0]=='Q':
   $! t
  if t[0]=='ln':
   $! $O(('log',walk(t[1]),b),('log','e',b))
  $!(t[0],)+$0(walk(a)$) a in t[1:])
 $!('hold',walk(e))
''')
_x(r'''VERSION='1.1'
ENV={}
UFUN={}
ASSUME=[]
STATE={'ans':0,'$@':$3,'tmpf':[]}
COMPLEXF=('csolve','czeros','cfactor','cpolyroots','eigvl','eigvc','conj',
 '$N','imag','$p')
$, isfunc(n):
 $!(n in F or n in SF or n in UFUN or n in ALIAS
 or n in STATE['tmpf']or n in('expr','$V','log','root'))
$, lookup(n):
 if n in ENV:
  $! ENV[n]
 if n=='ans':
  $! STATE['ans']
 if n=='i':
  STATE['$@']=$E
 $! n
$, ev(t):
 tt=$/(t)
 if tt is $w or tt is $A:
  $! t
 if tt is ${:
  $! lookup(t)
 h=t[0]
 if h=='+':
  a=ev(t[1])
  b=ev(t[2])
  $! vadd(a,b)
 if h=='-':
  $! vsub(ev(t[1]),ev(t[2]))
 if h=='$k':
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
  $! lmap($7 a:fn('fact',a),ev(t[1]))
 if h=='%':
  $! lmap($7 a:$O(a,100),ev(t[1]))
 if h=='deg':
  v=ev(t[1])
  if SET['$p']=='rad':
   $! lmap($7 a:$:(a,$O('pi',180)),v)
  if SET['$p']=='grad':
   $! lmap($7 a:$:(a,Q(10,9)),v)
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
 if h=='$I':
  $!('$I',)+$0(ev(a)$) a in t[1:])
 if h=='mat':
  $!('mat',)+$0(('$I',)+$0(ev(a)$) a in r[1:])$) r in t[1:])
 if h=='${':
  $! t
 if h=='&':
  a=ev(t[1])
  b=ev(t[2])
  $!('${',string_(a)[1]+string_(b)[1])
 if h=='index':
  $! ev_index(ev(t[1]),[ev(a)$) a in t[2:]])
 if h=='prime':
  $! t[1]+"'"*t[2]
 if h=='primecall':
  $!('call',t[1]+"'"*t[2])+$0(ev(a)$) a in t[3:])
 if h=='polar':
  STATE['$@']=$E
  $! $:(ev(t[1]),pw('e',$:('i',toang(ev(t[2])))))
 if h=='conv':
  $! ev_conv(t)
 err('Syntax error')
$, evw(raw,names):
 saved={}
 $) n in names:
  if n in ENV:
   saved[n]=ENV.pop(n)
 try:
  $! ev(raw)
 finally:
  $) n in saved:
   ENV[n]=saved[n]
$, split_and(c):
 if $&(c,'$*'):
  $! split_and(c[1])+split_and(c[2])
 $![c]
$, ev_with(t):
 conds=split_and(t[2])
 pairs={}
 ineq=[]
 $) c in conds:
  if $&(c,'=')$* $/(c[1])is ${:
   pairs[c[1]]=ev(c[2])
  $(:
   v=evw(c,$I(pairs.keys()))
   if $&(v,'$*'):
    ineq.extend($I(v[1:]))
   $K v!='true':
    ineq.$%(v)
 n0=$5(ASSUME)
 ASSUME.extend(ineq)
 try:
  r=evw(t[1],$I(pairs.keys()))
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
 if $/(a)is ${ $* b==0:
  v=a
  pos=h in('>','>=')
 $K $/(b)is ${ $* a==0:
  v=b
  pos=h in('<','<=')
 $(:
  $! r
 rep=v if pos $( $k(v)
 r=$Q(r,('$H',v),rep)
 r=$Q(r,('sign',v),1 if pos $(-1)
 $! r
$, target_fn(t):
 if $&(t,'call'):
  $! t[1],[p $) p in t[2:]]
 if $&(t,'*')$* $/(t[1])is ${:
  p=t[2]
  $! t[1],[p]
 $! $#
$, ev_store(raw,tgt):
 tf=target_fn(tgt)
 if tf is $- $#:
  $! ev_define(tgt,raw)
 if $/(tgt)is $- ${:
  err('Invalid variable $B')
 if tgt in SPECIAL or tgt in F or tgt in SF:
  err('Reserved $B')
 v=ev(raw)
 ENV[tgt]=unhold(v)if $- $&(v,'${')$( v
 $! v
$, ev_define(lhs,rhs):
 tf=target_fn(lhs)
 if tf is $#:
  if $/(lhs)is ${:
   $! ev_store(rhs,lhs)
  err('Invalid definition')
 $B,params=tf
 $) p in params:
  if $/(p)is $- ${:
   err('Invalid parameter')
 body=unhold(evw(rhs,params))
 UFUN[$B]=(params,body)
 if $B in STATE['tmpf']:
  STATE['tmpf'].remove($B)
 $!('${','Done')
$, ev_index(a,idx):
 if $- idx:
  err('Invalid index')
 if $&(a,'$I'):
  i=idx[0]
  if $- $j(i)or i<1 or i>=$5(a):
   err('Invalid index')
  $! a[i]
 if $&(a,'mat'):
  $) k in idx:
   if $- $j(k)or k<1:
    err('Invalid index')
  if $5(idx)==1:
   if $5(a)==2:
    if idx[0]>=$5(a[1]):
     err('Invalid index')
    $! a[1][idx[0]]
   if idx[0]>=$5(a):
    err('Invalid index')
   $!('mat',a[idx[0]])
  if idx[0]>=$5(a)or idx[1]>=$5(a[idx[0]]):
   err('Invalid index')
  $! a[idx[0]][idx[1]]
 if $&(a,'${'):
  k=idx[0]
  if $5(idx)!=1 or $- $j(k)or k<1 or k>$5(a[1]):
   err('Invalid index')
  $!('${',a[1][k-1])
 err('Invalid index')
$, ev_conv(t):
 e=t[1]
 $B=t[2]
 $Y=[ev(a)$) a in t[3:]]
 if $B=='$I':
  if e=='exp':
   $! explist($Y[0],$Y[1])
  if e=='mat':
   $! matlist($Y[0])
  err('Unknown conversion')
 if $B=='mat' $* e=='$I':
  $! listmat(*$Y)
 v=ev(e)
 v=finalize(v,$E)
 $! builtin($B,conv,(v,$B,$Y))
$, explist(e,v):
 $?=[]
 $y=e[1:]if $&(e,'or')$((e,)
 $) p in $y:
  if $&(p,'=')$* p[1]==v:
   $?.$%(p[2])
 $!('$I',)+$0($?)
$, call($B,raw):
 $B=ALIAS.get($B,$B)
 if $B in UFUN:
  params,body=UFUN[$B]
  $Y=[ev(a)$) a in raw]
  if $5($Y)!=$5(params):
   err('Wrong number of arguments')
  $! subsd(body,dict(zip(params,$Y)))
 f=SF.get($B)
 if f is $- $#:
  if $B in COMPLEXF:
   STATE['$@']=$E
  $! builtin($B,f,(raw,))
 f=F.get($B)
 if f is $- $#:
  $Y=[ev(a)$) a in raw]
  if $B in COMPLEXF:
   STATE['$@']=$E
  $! builtin($B,f,$Y)
 if $B=='expr':
  s=ev(raw[0])
  $! ev(parse(s[1],isfunc))
 $Y=[ev(a)$) a in raw]
 $!('call',$B)+$0($Y)
''')
_x(r'''$, builtin($B,f,$Y):
 try:
  $! f(*$Y)
 $9 $R as ex:
  if ${(ex).$u('Wrong number of arguments'):
   argerr($B)
  $l
 $9 TypeError as ex:
  msg=${(ex)
  if 'positional' in msg or 'takes' in msg or 'required' in msg or 'missing' in msg:
   argerr($B)
  err('Invalid argument $) '+$B)
 $9(IndexError,$U,AttributeError,KeyError):
  err('Invalid argument $) '+$B)
 $9 $`:
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
 err('Wrong number of arguments $) '+n+('\n'+sy.split('\n')[0]if sy $( ''))
$, suggest($B):
 if $5($B)<4:
  $! $#
 $z=$#
 $) k in tinames():
  if $H($5(k)-$5($B))>1:
   $8
  if close(k,$B.lower()):
   $z=tinames()[k]
   $T
 $! $z
$, close(a,b):
 if a==b:
  $! $3
 if $5(a)==$5(b):
  d=[i $) i in $+($5(a))if a[i]!=b[i]]
  if $5(d)==2 $* d[1]==d[0]+1 $* a[d[0]]==b[d[1]]$* a[d[1]]==b[d[0]]:
   $! $E
  $! $5(d)==1
 if $5(a)>$5(b):
  a,b=b,a
 $) i in $+($5(b)):
  if b[:i]+b[i+1:]==a:
   $! $E
 $! $3
$, unknown_calls(e,$?):
 if $/(e)is $- $0 or $- e or e[0]=='Q':
  $!
 if e[0]=='call' $* e[1]$- in UFUN $* e[1]$- in STATE['tmpf']$* e[1]$- in $?:
  $?.$%(e[1])
 $) a in e[1:]:
  unknown_calls(a,$?)
$, var_of(raw):
 if $/(raw)is ${:
  $! raw,$#
 if $&(raw,'='):
  if $/(raw[1])is $- ${:
   err('Variable expected')
  $! raw[1],ev(raw[2])
 err('Variable expected')
$, $}(a,lo,hi):
 if $5(a)<lo or $5(a)>hi:
  err('Wrong number of arguments')
$, $h(a,k=1):
 v,val=var_of(a[k])
 e=unhold(evw(a[0],[v]))
 $! e,v,val
$, post_subst(r,v,val):
 if val is $- $#:
  $! $Q(r,v,val)
 if v in ENV:
  $! $Q(r,v,ENV[v])
 $! r
$, sf_d(a):
 $}(a,2,3)
 e,v,val=$h(a)
 n=ev(a[2])if $5(a)>2 $( 1
 if $- $j(n):
  err('Order must be an integer')
 r=lmap($7 u:nice(diff(u,v,n)),e)
 $! post_subst(r,v,val)
$, sf_int(a):
 $}(a,2,4)
 e,v,val=$h(a)
 if $5(a)==2:
  $! lmap($7 u:nice(integrate(u,v)),e)
 if $5(a)==3:
  c=ev(a[2])
  $! lmap($7 u:$](nice(integrate(u,v)),c),e)
 lo=ev(a[2])
 hi=ev(a[3])
 $! lmap($7 u:nice(defint(u,v,lo,hi)),e)
$, sf_limit(a):
 $}(a,3,4)
 e,v,val=$h(a)
 pt=ev(a[2])
 dirn=0
 if $5(a)>3:
  d=ev(a[3])
  if $- $C(d):
   err('Direction must be -1, 0 or 1')
  dirn=0 if d==0 $((1 if $_(d)>0 $(-1)
 $, L(u):
  r=$v(u,v,pt,dirn)
  if $&(r,'$v'):
   $!('$v',u,v,pt)if dirn==0 $(('$v',u,v,pt,dirn)
  $! nice(r)
 $! lmap(L,e)
$, cs_bounds(a,i):
 $! ev(a[i]),ev(a[i+1])
$, sf_sum(a):
 $}(a,4,4)
 e,v,val=$h(a)
 lo,hi=cs_bounds(a,2)
 r=sumseq(e,v,lo,hi)
 $! prefer_fact(nice(r))
$, prefer_fact(r):
 if $&(r,'+')$* $- $^(r)$* $5($q(r))==1:
  try:
   f=factor_expr(r)
   if $&(f,'hold')$* $&(f[1],'*'):
    $! f
  $9 $6:
   pass
 $! r
$, sf_prod(a):
 $}(a,4,4)
 e,v,val=$h(a)
 lo,hi=cs_bounds(a,2)
 $! prodseq(e,v,lo,hi)
$, sf_seq(a):
 $}(a,4,5)
 e,v,val=$h(a)
 lo,hi=cs_bounds(a,2)
 st=ev(a[4])if $5(a)>4 $( 1
 $?=[]
 k=lo
 cnt=0
 $J ncmp(k,hi)<=0 if $C(k)$( $3:
  $?.$%($Q(e,v,k))
  k=nadd(k,st)
  cnt+=1
  if cnt>5000:
   err('Too many elements')
 $!('$I',)+$0($?)
$, sf_taylor(a):
 $}(a,3,4)
 e,v,val=$h(a)
 n=ev(a[2])
 pt=ev(a[3])if $5(a)>3 $( 0
 $! lmap($7 u:taylor(u,v,n,pt),e)
$, sf_series(a):
 $}(a,3,4)
 e,v,val=$h(a)
 n=ev(a[2])
 pt=ev(a[3])if $5(a)>3 $( 0
 $! lmap($7 u:series_cmd(u,v,n,pt),e)
$, sf_dominant(a):
 $}(a,2,3)
 e,v,val=$h(a)
 pt=ev(a[2])if $5(a)>2 $( 0
 $! lmap($7 u:dominant(u,v,pt),e)
$, solvevars(rawvs):
 vs=[]
 gs=[]
 $) r in rawvs:
  if $&(r,'$I'):
   $) q in r[1:]:
    v,g=var_of(q)
    vs.$%(v)
    gs.$%(g)
  $(:
   v,g=var_of(r)
   vs.$%(v)
   gs.$%(g)
 $! vs,gs
$, eqlist(e):
 if $&(e,'$*'):
  $?=[]
  $) p in e[1:]:
   $?.extend(eqlist(p))
  $! $?
 if $&(e,'$I'):
  $! $I(e[1:])
 $![e]
$, cons_for(v):
 $?=[]
 $) c in ASSUME:
  if has(c,v):
   $?.$%(c)
 $! $?
$, sf_solve(a,$@=$3):
 if $5(a)<2:
  err('Wrong number of arguments')
 vs,gs=solvevars(a[1:])
 e=evw(a[0],vs)
 eqs=eqlist(e)
 if $5(vs)==1 $* $5(eqs)==1:
  v=vs[0]
  eq=eqs[0]
  if gs[0]is $- $#:
   f=$[(eq[1],eq[2])if $&(eq,'=')$( eq
   r=nsolve(f,v,tofl(evalf(gs[0])))
   $!('=',v,r)if r is $- $# $( 'false'
  r=solve(eq,v,$@,cons_for(v))
  if r is $#:
   f=$[(eq[1],eq[2])if $&(eq,'=')$( eq
   ns=numeric_solve(f,v,$@)if head(eq)=='=' or head(eq)is $# $( $#
   if ns:
    r=sols_to_bool(v,apply_constraints(ns,v,cons_for(v)))
   $(:
    $!('solve',eq,v)
  $! finish_sol(r)
 if $5(eqs)>1 $* any([head(q)in('<','>','<=','>=','/=')$) q in eqs]):
  if $5(vs)>1:
   $!('solve',e)+$0(vs)
  $! finish_sol(solve_and(eqs,vs[0],$@))
 $f=solve_system(eqs,vs,$@,gs if any([g is $- $# $) g in gs])$( $#)
 if $f is $#:
  $!('solve',e)+$0(vs)
 if $- $f:
  $! 'false'
 $?=[]
 $) s in $f:
  conj=[('=',v,clean(s.get(v,v)))$) v in vs]
  $?.$%(conj[0]if $5(conj)==1 $(('$*',)+$0(conj))
 $! finish_sol($?[0]if $5($?)==1 $(('or',)+$0($?))
''')
_x(r'''$, solve_and(eqs,v,$@):
 cons=cons_for(v)
 $) i in $+($5(eqs)):
  if head(eqs[i])=='=':
   $d=eqs[:i]+eqs[i+1:]
   r=solve(eqs[i],v,$@,$d+cons)
   if r is $#:
    $!('solve',('$*',)+$0(eqs),v)
   $! r
 ps=rel_pairs(eqs+cons,v)
 r=solve_rels(ps,v)if ps is $- $# $( $#
 if r is $#:
  $!('solve',('$*',)+$0(eqs),v)
 $! r
$, finish_sol(r):
 ns=[]
 $, walk(e):
  if $/(e)is ${ $* e[0]=='n' $* e[1:].isdigit()$* e $- in ns:
   ns.$%(e)
  $K $/(e)is $0 $* e $* e[0]!='Q':
   $) a in e[1:]:
    walk(a)
 walk(r)
 if $- ns or ns==['n%d'%(i+1)$) i in $+($5(ns))]:
  $! r
 tmp=dict([(ns[i],'N%d_'%i)$) i in $+($5(ns))])
 r=subsd(r,tmp)
 $! subsd(r,dict([('N%d_'%i,'n%d'%(i+1))$) i in $+($5(ns))]))
$, sf_csolve(a):
 $! sf_solve(a,$E)
$, sf_zeros(a,$@=$3):
 $}(a,2,2)
 vs,gs=solvevars(a[1:])
 e=evw(a[0],vs)
 if $5(vs)==1 $* $- $&(e,'$I'):
  r=zeros(e,vs[0],$@,cons_for(vs[0]))
  if r is $#:
   ns=numeric_solve(e,vs[0],$@)
   $!('$I',)+$0(ns or[])
  $! r
 eqs=eqlist(e)
 $f=solve_system(eqs,vs,$@)
 if $- $f:
  $!('$I',)
 $! mk([[clean(s.get(v,v))$) v in vs]$) s in $f])
$, sf_czeros(a):
 $! sf_zeros(a,$E)
$, sf_nsolve(a):
 $}(a,2,4)
 v,g=var_of(a[1])
 e=unhold(evw(a[0],[v]))
 f=$[(e[1],e[2])if $&(e,'=')$( e
 lo=tofl(evalf(ev(a[2])))if $5(a)>2 $( $#
 hi=tofl(evalf(ev(a[3])))if $5(a)>3 $( $#
 $) c in cons_for(v):
  b=bounds([c],v)if $3 $( $#
 cb=bounds(cons_for(v),v)
 if cb is $- $#:
  lo,hi=tofl(evalf(cb[0])),tofl(evalf(cb[1]))
 r=nsolve(f,v,tofl(evalf(g))if g is $- $# $( $#,lo,hi)
 if r is $#:
  $!('${','No solution found')
 $! r
$, sf_desolve(a):
 $}(a,3,3)
 x=a[1]
 y=a[2]
 if $/(x)is $- ${ or $/(y)is $- ${:
  err('Variable expected')
 $y=split_and(a[0])
 ode=$#
 conds=[]
 $) p in $y:
  if $&(p,'=')$* $&(p[1],'primecall')$* p[1][1]==y:
   conds.$%((p[1][2],evw(p[1][3],[x,y]),evw(p[2],[x,y])))
  $K $&(p,'=')$* $&(p[1],'*')$* p[1][1]==y $* $- hasprime(p):
   conds.$%((0,ev(p[1][2]),ev(p[2])))
  $K $&(p,'=')$* $&(p[1],'call')$* p[1][1]==y:
   conds.$%((0,ev(p[1][2]),ev(p[2])))
  $(:
   ode=p
 if ode is $#:
  err('ODE expected')
 o=evw(ode,[x,y,y+"'",y+"''"])
 o=$Q($Q(o,y+"''",YP[1]),y+"'",YP[0])
 r=desolve(o,x,y,conds)
 if r is $#:
  $!('desolve',o,x,y)
 $! r
$, hasprime(t):
 if $/(t)is $- $0:
  $! $3
 if t[0]in('prime','primecall'):
  $! $E
 $) a in t[1:]:
  if hasprime(a):
   $! $E
 $! $3
$, bnd_args(a,i,v):
 lo=ev(a[i])if $5(a)>i $( $#
 hi=ev(a[i+1])if $5(a)>i+1 $( $#
 cb=bounds(cons_for(v),v)
 if cb is $- $#:
  lo,hi=cb
 $(:
  $) c in cons_for(v):
   h=head(c)
   if h in('>','>=')$* c[1]==v:
    lo=c[2]
   $K h in('<','<=')$* c[1]==v:
    hi=c[2]
 $! lo,hi
$, sf_fmin(a,kind='min'):
 $}(a,2,4)
 e,v,val=$h(a)
 lo,hi=bnd_args(a,2,v)
 r=fextreme(e,v,kind,lo,hi)
 if r is $#:
  $!('f'+kind,e,v)
 $! r
$, sf_fmax(a):
 $! sf_fmin(a,'max')
$, sf_nfmin(a,kind='min'):
 $}(a,2,4)
 e,v,val=$h(a)
 lo,hi=bnd_args(a,2,v)
 $! nfextreme(e,v,kind,tofl(evalf(lo))if lo is $- $# $( $#,
 tofl(evalf(hi))if hi is $- $# $( $#)
$, sf_nfmax(a):
 $! sf_nfmin(a,'max')
$, sf_nint(a):
 $}(a,4,4)
 e,v,val=$h(a)
 lo,hi=cs_bounds(a,2)
 $! nint_split(e,v,lo,hi)
$, sf_arclen(a):
 $}(a,4,4)
 e,v,val=$h(a)
 lo,hi=cs_bounds(a,2)
 $! nice(arclen(e,v,lo,hi))
$, pt_arg(a):
 if $5(a)==2 $* $&(a[1],'='):
  v,p=var_of(a[1])
  e=evw(a[0],[v])
  $! e,v,p
 $}(a,3,3)
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
 $}(a,3,4)
 x,_=var_of(a[1])
 y,_=var_of(a[2])
 e=evw(a[0],[x,y])
 n=ev(a[3])if $5(a)>3 $( 1
 $! impdif(e,x,y,n)
$, rc_args(a):
 v,val=var_of(a[1])
 e=unhold(evw(a[0],[v]))
 h=ev(a[2])if $5(a)>2 $( 0.001
 if val is $#:
  val=v
 $! e,v,val,h
$, sf_avgrc(a):
 $}(a,2,3)
 e,v,val,h=rc_args(a)
 $! lmap($7 u:$>(avgrc(u,v,val,h)),e)
$, sf_central(a):
 $}(a,2,3)
 e,v,val,h=rc_args(a)
 $! lmap($7 u:$>(centraldiff(u,v,val,h)),e)
$, sf_nderiv(a):
 $}(a,2,3)
 v,val=var_of(a[1])
 e=unhold(evw(a[0],[v]))
 n=ev(a[2])if $5(a)>2 $( 1
 if val is $#:
  val=ENV.get(v)
  if val is $#:
   err('Value required: var=value')
 $! evalf($Q(diff(e,v,n),v,val))
$, opt_var(a,i):
 if $5(a)>i:
  v,_=var_of(a[i])
  $! v
 $! $#
$, sf_expand(a):
 $}(a,1,2)
 v=opt_var(a,1)
 e=ev(a[0])
 $! expand_full(unhold(e),v)
$, sf_factor(a,$@=$3):
 $}(a,1,2)
 v=opt_var(a,1)
 e=unhold(ev(a[0]))
 $! factor_expr(e,v,$@)
$, sf_cfactor(a):
 $! sf_factor(a,$E)
$, sf_comdenom(a):
 $}(a,1,2)
 $! comdenom(unhold(ev(a[0])))
$, sf_propfrac(a):
 $}(a,1,2)
 v=opt_var(a,1)
 $! lmap($7 u:propfrac(u,v),unhold(ev(a[0])))
$, polyvar(e,a,i):
 v=opt_var(a,i)
 if v is $#:
  ss=$q(e)
  v='x' if 'x' in ss or $- ss $( ss[0]
 $! v
$, sf_polycoeffs(a):
 $}(a,1,2)
 e=unhold(ev(a[0]))
 v=polyvar(e,a,1)
 cs=$X(e,v)
 if cs is $#:
  err('Polynomial expected')
 $J $5(cs)>1 $* cs[-1]==0:
  cs.pop()
 $!('$I',)+$0(reversed(cs))
$, sf_polydegree(a):
 $}(a,1,2)
 e=unhold(ev(a[0]))
 v=polyvar(e,a,1)
 d=degree($>(e),v)
 if d is $#:
  err('Polynomial expected')
 if e==0:
  $!('*',-1,'$M')
 $! d
$, sf_polyquo(a,which=0):
 $}(a,2,3)
 p=unhold(ev(a[0]))
 q=unhold(ev(a[1]))
 v=polyvar($](p,q),a,2)
 cp=$X(p,v)
 cq=$X(q,v)
 if cp is $# or cq is $#:
  err('Polynomial expected')
 qq,rr=e_divmod(cp,cq)
 $! fromcoeffs(qq if which==0 $( rr,v)
$, sf_polyrem(a):
 $! sf_polyquo(a,1)
''')
_x(r'''$, sf_polyroots(a,$@=$3):
 $}(a,1,2)
 if $5(a)==1:
  L=ev(a[0])
  if $- $&(L,'$I'):
   err('List expected')
  v='X_'
  e=polyeval(L,v)
 $(:
  v,_=var_of(a[1])
  e=evw(a[0],[v])
 r=zeros(e,v,$@)
 $! r if r is $- $# $(('$I',)
$, sf_cpolyroots(a):
 $! sf_polyroots(a,$E)
$, sf_linsolve(a):
 vs,gs=solvevars(a[1:])
 e=evw(a[0],vs)
 eqs=eqlist(e)
 fs=[eqexpr(q)$) q in eqs]
 if $- is_linear_sys(fs,vs):
  err('Argument error: $g system required')
 $f=linsys(fs,vs)
 if $- $f:
  $! 'false'
 $!('$I',)+$0($f[0][v]$) v in vs)
$, sf_domain(a):
 $}(a,2,2)
 e,v,val=$h(a)
 r=domain(e,v)
 $! r if r is $- $# $(('domain',e,v)
$, sf_completesq(a):
 $}(a,2,2)
 v,_=var_of(a[1])
 e=unhold(evw(a[0],[v]))
 if $&(e,'='):
  lhs=complete_sq($[(e[1],e[2]),v,$E)
  $! lhs
 $! complete_sq(e,v,$3)
$, complete_sq(e,v,eq):
 cs=$X(e,v)
 if cs is $# or $5(cs)!=3:
  err('Quadratic expected')
 c,b,a=cs
 h=$.($O(b,$:(2,a)))
 k=$.($[(c,$O($:(b,b),$:(4,a))))
 sq=('^',$](v,h),2)
 t=sq if a==1 $(('*',a,sq)
 if eq:
  $!('=',('hold',t),$k(k))
 if k==0:
  $!('hold',t)
 $!('hold',('+',t,k))
$, sf_constructmat(a):
 $}(a,5,5)
 i,_=var_of(a[1])
 j,_=var_of(a[2])
 e=evw(a[0],[i,j])
 r=ev(a[3])
 c=ev(a[4])
 $! mk([[subsd(e,{i:ii,j:jj})$) jj in $+(1,c+1)]$) ii in $+(1,r+1)])
$, sf_charpoly(a):
 $}(a,2,2)
 A=ev(a[0])
 v=a[1]if $/(a[1])is ${ $( ev(a[1])
 $! charpoly(A,v)
$, sf_simplify(a):
 e=unhold(ev(a[0]))
 $! nice(pyth(e))
SF={
 'd':sf_d,'$Z':sf_int,'$v':sf_limit,'sumseq':sf_sum,
 'prodseq':sf_prod,'seq':sf_seq,'taylor':sf_taylor,'series':sf_series,
 'dominantterm':sf_dominant,'solve':sf_solve,'csolve':sf_csolve,
 'zeros':sf_zeros,'czeros':sf_czeros,'nsolve':sf_nsolve,
 'desolve':sf_desolve,'fmin':sf_fmin,'fmax':sf_fmax,'nfmin':sf_nfmin,
 'nfmax':sf_nfmax,'nint':sf_nint,'arclen':sf_arclen,
 'tangentline':sf_tangent,'normalline':sf_normal,'impdif':sf_impdif,
 'avgrc':sf_avgrc,'centraldiff':sf_central,'nderivative':sf_nderiv,
 '$>':sf_expand,'factor':sf_factor,'cfactor':sf_cfactor,
 'comdenom':sf_comdenom,'propfrac':sf_propfrac,
 'polycoeffs':sf_polycoeffs,'polydegree':sf_polydegree,
 'polyquotient':sf_polyquo,'polyremainder':sf_polyrem,
 'polyroots':sf_polyroots,'cpolyroots':sf_cpolyroots,
 'linsolve':sf_linsolve,'domain':sf_domain,
 'completesquare':sf_completesq,'constructmat':sf_constructmat,
 'charpoly':sf_charpoly,'simplify':sf_simplify,
 }
$, when_simp(c,a,b=$#):
 t=tobool(rel(c[0],c[1],c[2]))if isrel(c)$( tobool(c)
 if t is $E:
  $! a
 if t is $3:
  $! b if b is $- $# $( '$F'
 $! $#
$o['when']=when_simp
$, finalize(r,quiet=$3):
 if $&(r,'${'):
  $! r
 if $- $&(r,'hold'):
  r=$.(r)if $-($&(r,'$I')or $&(r,'mat'))$( lmap($.,r)
  if needpyth(r):
   r=pyth(r)
  if SET['mode']=='approx' or $^(r):
   r=evalf(r)
  $K SET['mode']=='exact':
   r=exactify(r)
 if SET['$@']=='$N' $* $- STATE['$@']$* has(r,'i')$* $- quiet:
  err('Non-$N result')
 $! r
$, sqtrig(e,$?):
 if $/(e)is $- $0 or e[0]=='Q':
  $!
 if e[0]=='^' $* head(e[1])in('sin','cos')$* $j(e[2])$* e[2]>=2:
  $?.$%((e[1][0],e[1][1]))
 $) a in e[1:]:
  sqtrig(a,$?)
$, needpyth(r):
 if $- $&(r,'+'):
  $! $3
 $?=[]
 sqtrig(r,$?)
 $) n,u in $?:
  if(('cos' if n=='sin' $( 'sin'),u)in $?:
   $! $E
 $! $3
$, pre_register(s):
 low=s.replace(' ','').lower()
 cands=[]
 if ':=' in low:
  cands.$%(low.split(':=')[0])
 if low.$u('define'):
  cands.$%(low[6:].split('=')[0])
 $) arrow in('->','\u2192','=:'):
  if arrow in low:
   cands.$%(low.split(arrow)[-1])
 $) c in cands:
  i=c.find('(')
  if i>0:
   nm=c[:i]
   ok=$E
   $) ch in nm:
    if $-(ch.isalpha()or ch.isdigit()or ch=='_'):
     ok=$3
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
  SET['$p']='deg'
  $! 'Angle: degree'
 if k in('rad','radian'):
  SET['$p']='rad'
  $! 'Angle: radian'
 if k in('grad','gradian'):
  SET['$p']='grad'
  $! 'Angle: gradian'
 if k in('approx','auto','exact'):
  SET['mode']=k
  $! 'Mode: '+k
 if k in('$N','$1','rect'):
  SET['$@']='$N' if k=='$N' $( 'rect'
  $! 'Complex format: '+SET['$@']
 if k in('digits','$A'):
  if $5(p)>1 $* $- p[1].isdigit():
   $! 'Use :digits n with n from 1 to 15'
  n=$w(p[1])if $5(p)>1 $( 10
  OPT['digits']=max(1,min(15,n))
  $! 'Digits: '+${(OPT['digits'])
 if k=='ascii':
  OPT['uni']=$3
  $! 'ASCII output'
 if k in('unicode','uni'):
  OPT['uni']=$E
  $! 'Unicode output'
 if k=='vars':
  $?=[]
  $) n in sorted(ENV):
   $?.$%(n+' = '+fmt(ENV[n]))
  $) n in sorted(UFUN):
   ps,b=UFUN[n]
   $?.$%(n+'('+','.join(ps)+') = '+fmt(b))
  $! '\n'.join($?)if $? $( '(none)'
 if k in('clear','clearaz','reset'):
  ENV.clear()
  UFUN.clear()
  $! 'Cleared'
 if k in('mem','memory'):
  try:
   import gc
   gc.collect()
   $! 'Memory: %d KB free, %d KB used'%(gc.mem_free()//1024,gc.mem_alloc()//1024)
  $9 $6:
   $! 'Memory information is $- available'
 if k in('mode','modes','getmode'):
  $!('$p='+SET['$p']+' mode='+SET['mode']+' $@='+SET['$@']+
 ' digits='+${(OPT['digits']))
 if k=='test':
  _load('cashelp')
  saved=(dict(SET),dict(OPT))
  SET.update({'$p':'rad','mode':'auto','$@':'$N'})
  OPT.update({'uni':$E,'digits':10})
  try:
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
  try:
   from ti_system import get_key
  $9 ImportError:
   $! 'The key test needs the calculator (ti_system)'
  print('Press keys; esc twice to stop')
  last=''
  $J $E:
   key=get_key(1)
   print(repr(key))
   if key=='esc' $* last=='esc':
    $! ''
   last=key
 if k in('help','?','h'):
  _load('cashelp')
  $! help(p[1]if $5(p)>1 $( $#)
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
 if low.$u('help'):
  $! command(low)
 if low.$u('delvar'):
  $) n in low[6:].replace(',',' ').split():
   ENV.pop(n,$#)
   UFUN.pop(n,$#)
  keep()
  $! 'Done'
 if low in('clearaz','clear'):
  $! command('clear')
 pre_register(s)
 t=parse(s,isfunc)
 STATE['$@']=(SET['$@']!='$N')
 r=ev(t)
 r=finalize(r)
 if $-($&(t,'define')or($&(r,'${')$* r[1]=='Done')):
  STATE['ans']=unhold(r)if $- $&(r,'${')$( r
 keep()
 $?=fmt_top(r)
 un=[]
 unknown_calls(r,un)
 $) n in un:
  g=suggest(n)
  if g:
   $?+='\n('+n+' is $- a command; did you mean '+g+'?)'
 $! $?
KEEP='ncasmem'
$, memtext():
 u=OPT['uni']
 OPT['uni']=$3
 try:
  $?=[':'+SET['$p'],':'+SET['mode'],
 ':'+('$N' if SET['$@']=='$N' $( '$1'),
 ':digits '+${(OPT['digits'])]
  if $- u:
   $?.$%(':ascii')
  $) n in sorted(ENV):
   $?.$%(n+':='+fmt(ENV[n]))
  $) n in sorted(UFUN):
   ps,b=UFUN[n]
   $?.$%(n+'('+','.join(ps)+'):='+fmt(b))
 finally:
  OPT['uni']=u
 $! '\n'.join([l $) l in $? if $5(l)<2000 $* all([0<ord(c)<128 $) c in l])])
$, pack(t):
 $?=[]
 $) i in $+(0,$5(t),6):
  n=0
  $) c in reversed(t[i:i+6]):
   n=n*128+ord(c)
  $?.$%(n)
 $! $?
$, unpack(xs):
 cs=[]
 $) v in xs:
  n=$w(round(v))
  $J n:
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
 try:
  from ti_system import store_list
  store_list(KEEP,pack(t)or[0])
 $9 $6:
  pass
$, restore():
 if STATE.get('kept')is $- $#:
  $!
 STATE['kept']=memtext()
 try:
  from ti_system import recall_list
  t=unpack(recall_list(KEEP))
 $9 $6:
  $!
 STATE['restoring']=$E
 try:
  $) line in t.split('\n'):
   try:
    run(line)
   $9 $6:
    pass
 finally:
  STATE['restoring']=$3
 STATE['ans']=0
 STATE['kept']=memtext()
$, menu():
 _load('casmenu')
 runmenu(run)
GUI=$E
$, gui():
 if $- GUI:
  $! 'The full-screen mode is the separate program ncasgui.'
 try:
  import casgui
 $9 ImportError as ex:
  if 'casgui' $- in ${(ex):
   $l
  $! 'casgui is $- installed (needed $) the full-screen mode); using text mode.'
 restore()
 $! casgui.rungui(run)
$, startgui():
 r=gui()
 if r:
  print(r)
  print('The text version is the program ncastext.')
$, start():
 try:
  import ti_draw
 $9 ImportError:
  $! cas()
 r=gui()
 if r:
  print(r)
  cas()
$, ver():
 $! 'nCAS '+VERSION
$, calc(s):
 try:
  $! run(s)
 $9 $R as ex:
  $! 'Error: '+${(ex)
$, prompt():
 p=[]
 if SET['$p']!='rad':
  p.$%(SET['$p'])
 if SET['mode']!='auto':
  p.$%(SET['mode'])
 if SET['$@']!='$N':
  p.$%('$@')
 $! ' '.join(p)+'> '
''')
_x(r'''$, cas():
 restore()
 print('nCAS '+VERSION+' $) TI-Nspire CX II')
 print(('? help, m menu, g full screen, q quit')if GUI $( '? help, m menu, q quit')
 blank=0
 $J $E:
  try:
   s=input(prompt())
  $9(EOFError,KeyboardInterrupt):
   $T
  s=s.strip()
  if s in('q','quit','exit',':q'):
   $T
  if $- s:
   blank+=1
   if blank>=2:
    print('($/ q $* enter to quit)')
    blank=0
   $8
  blank=0
  if s.lower()in('m','menu'):
   try:
    menu()
   $9 $6 as ex:
    print('Error: '+${(ex))
   $8
  if s.lower()in('g','gui'):
   try:
    r=gui()
   $9 $6 as ex:
    r='Error: '+${(ex)
   if r:
    print(r)
   $8
  try:
   $?=run(s)
   if $?:
    print($?)
  $9 $R as ex:
   print('Error: '+${(ex))
  $9 $D:
   print('Error: Division by zero')
  $9 MemoryError:
   try:
    import gc
    gc.collect()
   $9 ImportError:
    pass
   print('Error: Out of memory')
  $9 KeyboardInterrupt:
   print('Break')
  $9 RuntimeError as ex:
   print('Error: Too $1 ('+${(ex)+')')
  $9 $6 as ex:
   print('Error: '+${(ex))
''')
_L['cashelp']=(r'''CATS=(
 ('alg','Algebra','solve csolve zeros czeros nsolve linsolve factor cfactor $> comdenom propfrac getnum getdenom completesquare polycoeffs polydegree polyquotient polyremainder polygcd polyroots cpolyroots polyeval tExpand tCollect simplify exact approx domain'),
 ('calc','Calculus','d $Z $v sumseq prodseq taylor series dominantTerm deSolve impDif arcLen tangentLine normalLine fMin fMax nfMin nfMax nInt nDerivative avgRC centralDiff'),
 ('mat','Matrix/vector','det identity transpose rref ref inverse eigVl eigVc charPoly LU QR trace norm rowNorm colNorm diag augment colAugment subMat rowSwap rowAdd mRow mRowAdd crossP dotP unitV simult constructMat newMat randMat dim rowDim colDim mat>$I $I>mat'),
 ('num','Numbers','gcd lcm mod remain intDiv isPrime nCr nPr ! floor ceiling round iPart fPart sign $H $N imag conj $p'),
 ('$I','Lists/stats','seq sum product mean median stdDev stdDevPop variance varPop max min sortA sortD cumulativeSum deltaList augment left right mid count normPdf normCdf invNorm binomPdf binomCdf poissPdf poissCdf geomPdf geomCdf'),
 ('conv','Conversions (expr>>$B)','>>Decimal >>approxFraction() >>DMS >>DD >>Rad >>Grad >>Polar >>Rect >>Cylind >>Sphere >>exp >>ln >>logbase() >>sin >>cos >>Base2 >>Base10 >>Base16 exp>$I()'),
 ('cmd','Commands',':deg :rad :grad :auto :exact :approx :$N :$1 :digits n :ascii :unicode :vars :clear :mode :mem  delvar a  q=quit'),
 )
SYN={
 'solve':'solve(eqn,var) solve(eqn,var=guess)\nsolve(ineq,var) solve(eq1 $* eq2,{x,y})\nsolve(...)|x>0  (n1,n2..=any integer)',
 'csolve':'cSolve(eqn,var) $1 solutions',
 'zeros':'zeros(expr,var) -> $I of roots\nzeros({e1,e2},{x,y}) -> matrix',
 'czeros':'cZeros(expr,var) $1 roots',
 'nsolve':'nSolve(eqn,var[=guess][,lo,hi])',
 'linsolve':'linSolve({eq1,eq2},{x,y})',
 'factor':'factor(expr[,var]) factor(integer)\nwith var: irrational factors',
 'cfactor':'cFactor(expr[,var]) $1 factors',
 '$>':'$>(expr[,var]) incl. partial fractions',
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
 'polyroots':'polyRoots(poly,var) polyRoots({$X})',
 'cpolyroots':'cPolyRoots(poly,var)',
 'polyeval':'polyEval({$X},x)',
 'texpand':'tExpand(expr) $> trig of sums/multiples',
 'tcollect':'tCollect(expr) products -> multiple angles',
 'simplify':'simplify(expr) extra simplification',
 'exact':'exact(expr[,tol]) floats -> fractions',
 'approx':'approx(expr) decimal value',
 'domain':'domain(expr,var)',
 'd':'d(expr,var[,order])  d(expr,var)|var=val\nderivative(...) same',
 '$Z':'$Z(expr,var) antiderivative\nintegral(expr,var,a,b) definite\n(\u222b also accepted)',
 '$v':'$v(expr,var,point[,dir]) dir:-1 left,1 right\npoint may be $M or -$M',
 'sumseq':'sumSeq(expr,var,lo,hi)  (\u03a3) hi may be $M',
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
 'nint':'nInt(expr,var,a,b) numeric $Z',
 'nderivative':'nDerivative(expr,var=val[,order])',
 'avgrc':'avgRC(expr,var[=val][,h])',
 'centraldiff':'centralDiff(expr,var[=val][,h])',
 'det':'det(M)','inverse':'M^-1 or inverse(M)','rref':'rref(M)','ref':'ref(M)',
 'eigvl':'eigVl(M) eigenvalues','eigvc':'eigVc(M) unit eigenvectors (columns)',
 'charpoly':'charPoly(M,var)','lu':'LU(M) -> {L,U,P} with P*M=L*U','qr':'QR(M) -> {Q,R}',
 'simult':'simult(A,b) solves A*x=b','constructmat':'constructMat(expr,i,j,$n,cols)',
 'crossp':'crossP(u,v)','dotp':'dotP(u,v)','unitv':'unitV(v)','norm':'norm(M)',
 'seq':'seq(expr,var,lo,hi[,step])',
 'ncr':'nCr(n,k)','npr':'nPr(n,k)','gcd':'gcd(a,b)','lcm':'lcm(a,b)',
 'mod':'mod(a,b)','isprime':'isPrime(n)',
 'define':'Define f(x)=expr   or   f(x):=expr\nexpr->a  or  a:=expr   delvar a',
 'with':'expr|x=3   expr|x>0   solve(...)|0<=x<=2pi',
 'menu':'m or menu: numbered menus build the\ncommand $) you; 0 back, q quit.\nMatrices may be typed 1,2;3,4',
 'syntax':'implicit mult: 2x  3(x+1)  x(x+1)\n^ or ** power, $V( or \u221a, pi, e, i, $M\n<= >= /= $* or $-, ans = last result\nlog(x)=ln(x) ([ln] key); log10(x), log(x,b)',
 'log':'log(x) natural log (= ln, the [ln] key)\nlog10(x) base 10, log(x,b) base b',
 }
$, help($B=$#):
 if $B is $#:
  $?=['nCAS help: ?topic or ?command']
  $) k,t,items in CATS:
   $?.$%('?'+k+'  '+t)
  $?.$%('?define ?with ?syntax ?menu')
  $?.$%('m = menus (no typing of names)')
  $! '\n'.join($?)
 $B=$B.lower().replace('(','').strip()
 $) k,t,items in CATS:
  if $B==k:
   $! t+':\n'+items
 if $B in SYN:
  $! SYN[$B]
 $) k in SYN:
  if k.$u($B):
   $! SYN[k]
 $! 'No help $) '+$B
''',
r'''SELFTEST=(
 ('factor(x^2-5x+6)','(x-2)*(x-3)'),
 ('$>((x+1)^3)','x^3+3*x^2+3*x+1'),
 ('solve(x^2-5x+6=0,x)','x=2 or x=3'),
 ('solve(x^2=2,x)','x=-\u221a2 or x=\u221a2'),
 ('d(x^3*sin(x),x)','x^3*cos(x)+3*x^2*sin(x)'),
 ('$Z(x*e^x,x)','x*e^x-e^x'),
 ('$Z(1/(1+x^2),x,0,1)','\u03c0/4'),
 ('$v(sin(x)/x,x,0)','1'),
 ('taylor(e^x,x,3)','x^3/6+x^2/2+x+1'),
 ('sumSeq(k,k,1,n)','n*(n+1)/2'),
 ("deSolve(y'=y,x,y)",'y=c1*e^x'),
 ('det([[1,2][3,4]])','-2'),
 ('[[1,2][3,4]]^-1','[[-2,1][3/2,-1/2]]'),
 ('$V(12)','2*\u221a3'),
 ('cSolve(x^2+1=0,x)','x=-i or x=i'),
 ('factor(360)','2^3*3^2*5'),
 ('solve(x^2-4>0,x)','x<-2 or x>2'),
 ('nSolve(cos(x)=x,x)','0.7390851332'),
 )
$, selftest(run):
 ok=0
 $?=[]
 $) q,a in SELFTEST:
  try:
   r=run(q)
  $9 $6 as ex:
   r='ERR '+${(ex)
  if r==a:
   ok+=1
  $(:
   $?.$%('FAIL '+q+' -> '+r)
 $?.$%('%d/%d tests passed'%(ok,$5(SELFTEST)))
 $! '\n'.join($?)
''',)
_L['casmenu']=(r'''ALG=(
 ('Expand','$>(@1`,@2`)',(('$b',$#),('Var (blank=all)',''))),
 ('Factor','factor(@1`,@2`)',(('$b',$#),('Var (blank=Q)',''))),
 ('cFactor','cFactor(@1`,@2`)',(('$b',$#),('Var (blank=all)',''))),
 ('Simplify','simplify(@1)',(('$b',$#),)),
 ('comDenom','comDenom(@1)',(('$b',$#),)),
 ('propFrac','propFrac(@1`,@2`)',(('$b',$#),('Var',''))),
 ('Partial frac','$>(@1,@2)',(('Rational expr',$#),('Var','x'))),
 ('Complete sq','completeSquare(@1,@2)',(('Quadratic/eqn',$#),('Var','x'))),
 ('Poly divide','polyQuotient(@1,@2,@3)',(('Dividend',$#),('Divisor',$#),('Var','x'))),
 ('Poly remain','polyRemainder(@1,@2,@3)',(('Dividend',$#),('Divisor',$#),('Var','x'))),
 ('Poly gcd','polyGcd(@1,@2)',(('Poly 1',$#),('Poly 2',$#))),
 ('Substitute','(@1)|@2=@3',(('$b',$#),('Var','x'),('Value',$#))),
 ('tExpand','tExpand(@1)',(('$b',$#),)),
 ('tCollect','tCollect(@1)',(('$b',$#),)),
 ('Decimal','approx(@1)',(('$b',$#),)),
 ('Exact','exact(@1)',(('$b',$#),)),
 )
CALC=(
 ('Derivative','d(@1,@2`,@3`)',(('f',$#),('Var','x'),('Order',''))),
 ('Deriv at pt','d(@1,@2)|@2=@3',(('f',$#),('Var','x'),('At',$#))),
 ('Integral','$Z(@1,@2)',(('f',$#),('Var','x'))),
 ('Def $Z','$Z(@1,@2,@3,@4)',(('f',$#),('Var','x'),('Lower ($M ok)',$#),('Upper',$#))),
 ('Limit','$v(@1,@2,@3`,@4`)',(('f',$#),('Var','x'),('Point ($M ok)','0'),('Side 1/-1',''))),
 ('Taylor','taylor(@1,@2,@3`,@4`)',(('f',$#),('Var','x'),('Order','5'),('Point',''))),
 ('Series','series(@1,@2,@3`,@4`)',(('f',$#),('Var','x'),('Order','5'),('Point',''))),
 ('Sum (sigma)','sumSeq(@1,@2,@3,@4)',(('Term',$#),('Index','k'),('From','1'),('To ($M ok)','n'))),
 ('Product','prodSeq(@1,@2,@3,@4)',(('Term',$#),('Index','k'),('From','1'),('To','n'))),
 ('deSolve',"deSolve(@1` $* @2`` $* @3`,@4,@5)",
 (("ODE, use y' y''",$#),('Cond eg y(0)=1',''),("Cond eg y'(0)=0",''),('x var','x'),('y var','y'))),
 ('Implicit d/dx','impDif(@1,@2,@3)',(('Equation',$#),('x var','x'),('y var','y'))),
 ('Tangent line','tangentLine(@1,@2,@3)',(('f',$#),('Var','x'),('At',$#))),
 ('Normal line','normalLine(@1,@2,@3)',(('f',$#),('Var','x'),('At',$#))),
 ('Arc length','arcLen(@1,@2,@3,@4)',(('f',$#),('Var','x'),('From',$#),('To',$#))),
 ('fMin','fMin(@1,@2`,@3,@4`)',(('f',$#),('Var','x'),('Lower',''),('Upper',''))),
 ('fMax','fMax(@1,@2`,@3,@4`)',(('f',$#),('Var','x'),('Lower',''),('Upper',''))),
 ('Numeric $|','nInt(@1,@2,@3,@4)',(('f',$#),('Var','x'),('Lower',$#),('Upper',$#))),
 )
SOLV=(
 ('Solve','solve(@1,@2)`|@3`',(('Equation/ineq',$#),('Var','x'),('Condition eg x>0',''))),
 ('cSolve','cSolve(@1,@2)',(('Equation',$#),('Var','x'))),
 ('Zeros','zeros(@1,@2)',(('$b',$#),('Var','x'))),
 ('cZeros','cZeros(@1,@2)',(('$b',$#),('Var','x'))),
 ('nSolve','nSolve(@1,@2`,@3,@4`)',(('Equation',$#),('Var or x=guess','x'),('Lower',''),('Upper',''))),
 ('System 2 eqs','solve(@1 $* @2,{@3})',(('Eq 1',$#),('Eq 2',$#),('Vars','x,y'))),
 ('System 3 eqs','solve(@1 $* @2 $* @3,{@4})',(('Eq 1',$#),('Eq 2',$#),('Eq 3',$#),('Vars','x,y,z'))),
 ('Poly roots','polyRoots(@1,@2)',(('Polynomial',$#),('Var','x'))),
 ('Domain','domain(@1,@2)',(('$b',$#),('Var','x'))),
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
 ('Factor $w','factor(@1)',(('Integer',$#),)),
 ('isPrime','isPrime(@1)',(('Integer',$#),)),
 ('gcd','gcd(@1,@2)',(('a',$#),('b',$#))),
 ('lcm','lcm(@1,@2)',(('a',$#),('b',$#))),
 ('mod','mod(@1,@2)',(('a',$#),('b',$#))),
 ('nCr','nCr(@1,@2)',(('n',$#),('r',$#))),
 ('nPr','nPr(@1,@2)',(('n',$#),('r',$#))),
 ('Factorial','(@1)!',(('n',$#),)),
 ('Real part','$N(@1)',(('Complex z',$#),)),
 ('Imag part','imag(@1)',(('Complex z',$#),)),
 ('Conjugate','conj(@1)',(('Complex z',$#),)),
 ('|z|','$H(@1)',(('Complex z',$#),)),
 ('Angle','$p(@1)',(('Complex z',$#),)),
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
 ('normCdf','normCdf(@1,@2`,@3,@4`)',(('Lower (-$M ok)',$#),('Upper',$#),('mu',''),('sigma',''))),
 ('invNorm','invNorm(@1`,@2,@3`)',(('Area',$#),('mu',''),('sigma',''))),
 ('binomPdf','binomPdf(@1,@2,@3)',(('n',$#),('p',$#),('x',$#))),
 ('binomCdf','binomCdf(@1,@2,@3,@4)',(('n',$#),('p',$#),('Lower','0'),('Upper',$#))),
 )
''',
r'''CONV=(
 ('>Decimal','(@1)>>Decimal',(('$b',$#),)),
 ('>Fraction','(@1)>>approxFraction()',(('Decimal',$#),)),
 ('>DMS','(@1)>>DMS',(('Angle',$#),)),
 ('>Polar','(@1)>>Polar',(('Complex/vector',$#),)),
 ('>Rect','(@1)>>Rect',(('Complex',$#),)),
 ('>exp form','(@1)>>exp',(('$b',$#),)),
 ('>ln form','(@1)>>ln',(('$b',$#),)),
 ('>sin form','(@1)>>sin',(('$b',$#),)),
 ('>cos form','(@1)>>cos',(('$b',$#),)),
 ('>Binary','(@1)>>Base2',(('Integer',$#),)),
 ('>Hex','(@1)>>Base16',(('Integer',$#),)),
 )
SETS=(
 ('Degree',':deg',()),
 ('Radian',':rad',()),
 ('Auto mode',':auto',()),
 ('Exact mode',':exact',()),
 ('Approx mode',':approx',()),
 ('Real res',':$N',()),
 ('Complex res',':$1',()),
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
 ('Number/$@',NUMB),('Lists/stats',LIST),('Convert',CONV),
 ('Settings',SETS),
 )
KEYS='123456789abcdefghijklmnop'
class Quit($6):
 pass
$, ask(q):
 try:
  s=input(q)
 $9 EOFError:
  $l Quit()
 s=s.strip()
 if s.lower()in('q','quit'):
  $l Quit()
 $! s
$, show(title,labels):
 print('-- '+title+' --')
 line=''
 $) i in $+($5(labels)):
  cell=KEYS[i]+' '+labels[i]
  if line:
   print(line+' '*max(1,16-$5(line))+cell)
   line=''
  $(:
   line=cell
 if line:
  print(line)
 print('0 back  q quit')
$, pick(title,labels):
 show(title,labels)
 $J $E:
  s=ask('#: ').lower()
  if s in('','0'):
   $! $#
  i=KEYS.find(s)
  if $5(s)==1 $* 0<=i<$5(labels):
   $! i
  print('Choose '+KEYS[0]+'-'+KEYS[$5(labels)-1]+', 0 or q')
$, matrix_text(s):
 s=s.strip()
 if s $* s[0]$- in '[(' $*(';' in s or ',' in s):
  $! '['+s+']'
 $! s
$, build(item):
 label,tpl,prompts=item
 $e=[]
 $) p in prompts:
  q=p[0]
  d=p[1]
  hint='' if $- d $( ' ['+d+']'
  s=ask(q+hint+': ')
  if $- s:
   if d is $#:
    print('(cancelled)')
    $! $#
   s=d
  if $5(p)>2 $* p[2]=='m' $* s:
   s=matrix_text(s)
  $e.$%(s)
 $! fill(tpl,$e)
$, fill(tpl,$e):
 $?=''
 $y=tpl.split('`')
 $) k in $+($5($y)):
  seg=$y[k]
  if k%2==1:
   blank=$3
   $) i in $+($5($e)):
    if('@'+${(i+1))in seg $* $- $e[i]:
     blank=$E
   if blank:
    $8
  $?+=seg
 res=''
 i=0
 $J i<$5($?):
  c=$?[i]
  if c=='@' $* i+1<$5($?)$* '1'<=$?[i+1]<='9':
   res+=$e[$w($?[i+1])-1]
   i+=2
  $(:
   res+=c
   i+=1
 $! res
$, runmenu(run):
 print('Menus: pick a number or letter.')
 print("Type ans $) the last result.")
 try:
  $J $E:
   k=pick('nCAS menu',[m[0]$) m in MAIN])
   if k is $#:
    $!
   title,items=MAIN[k]
   $J $E:
    j=pick(title,[it[0]$) it in items])
    if j is $#:
     $T
    cmd=build(items[j])
    if cmd is $#:
     $8
    print('> '+cmd)
    try:
     $?=run(cmd)
    $9 $R as ex:
     $?='Error: '+${(ex)
    $9 $D:
     $?='Error: Division by zero'
    $9 MemoryError:
     $?='Error: Out of memory'
    $9 RuntimeError as ex:
     $?='Error: Too $1'
    $9 Quit:
     $l
    $9 $6 as ex:
     $?='Error: '+${(ex)
    if $?:
     print($?)
    ask('(enter) ')
 $9 Quit:
  $!
 $9 KeyboardInterrupt:
  $!
''',)
_x('GUI=False')
del _x
cas()
