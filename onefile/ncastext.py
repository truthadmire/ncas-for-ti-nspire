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
_W={'!': 'return', '#': 'None', '%': 'append', '&': 'isnode', '(': 'else', ')': 'for', '*': 'range', '+': 'and', ',': 'def', '-': 'autocancel', '.': 'not', '/': 'type', '0': 'complex', '1': 'tuple', '2': 'False', '3': 'len', '4': 'lambda', '5': 'isconst', '6': 'add_list', '7': 'continue', '8': 'freeof', '9': 'mul', ':': 'self', ';': 'expand', '<': 'except', '=': 'Exception', '>': 'depth', '?': 'out', '@': 'isnum', 'A': 'cplx', 'B': 'ZeroDivisionError', 'C': 'float', 'D': 'name', 'E': 'mul_list', 'F': 'True', 'G': 'list', 'H': 'while', 'I': 'abs', 'J': 'elif', 'K': 'p_divexact', 'L': 'undef', 'M': 'CASError', 'N': 'terms', 'O': 'ValueError', 'P': 'math', 'Q': 'real', 'R': 'args', 'S': 'nval', 'T': 'sqrt', 'U': 'OverflowError', 'V': 'coef_rest', 'W': 'subs', 'X': 'break', 'Y': 'div', 'Z': 'Expression', '[': 'islist', ']': 'inf', '^': 'coeffs', '_': 'rest', '`': 'hasfloat', 'a': 'nsign', 'b': 'sub', 'c': 'add', 'd': 'onevar_expr', 'e': 'sols', 'f': 'linear', 'g': 'vals', 'h': 'NoSeries', 'i': 'isint', 'j': 'rows', 'k': 'FSIMP', 'l': 'integral', 'm': 'israt', 'n': 'raise', 'o': 'neg', 'p': 'angle', 'q': 'int', 'r': 'startswith', 's': 'nargs', 't': 'arctan', 'u': 'str', 'v': 'factor_expr', 'w': 'arcsin', 'x': 'solve_eq', 'y': 'isrealc', 'z': 'p_const', '{': 'symbols', '|': 'HALF', '}': 'best', '~': 'expr'}
_x(r'''import $P
class $M($=):
 pass
$, err(msg):
 $n $M(msg)
CONSTS=('pi','e','i')
SPECIAL=('pi','e','i','$]','$L','true','false')
$, igcd(a,b):
 if a<0:
  a=-a
 if b<0:
  b=-b
 $H b:
  a,b=b,a%b
 $! a
$, ilcm(a,b):
 if a==0 or b==0:
  $! 0
 $! $I(a//igcd(a,b)*b)
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
$|=('Q',1,2)
$, isq(x):
 $! $/(x)is $1 $+ x[0]=='Q'
$, $i(x):
 $! $/(x)is $q
$, isfl(x):
 $! $/(x)is $C
$, $m(x):
 t=$/(x)
 $! t is $q or(t is $1 $+ x[0]=='Q')
$, $@(x):
 t=$/(x)
 $! t is $q or t is $C or(t is $1 $+ x[0]=='Q')
$, nd(x):
 if $/(x)is $q:
  $! x,1
 $! x[1],x[2]
$, tofl(x):
 t=$/(x)
 if t is $C:
  $! x
 if t is $q:
  $! $C(x)
 $! x[1]/x[2]
$, nadd(a,b):
 ta=$/(a)
 tb=$/(b)
 if ta is $q $+ tb is $q:
  $! a+b
 if ta is $C or tb is $C:
  $! tofl(a)+tofl(b)
 an,ad=nd(a)
 bn,bd=nd(b)
 $! Q(an*bd+bn*ad,ad*bd)
$, nmul(a,b):
 ta=$/(a)
 tb=$/(b)
 if ta is $q $+ tb is $q:
  $! a*b
 if ta is $C or tb is $C:
  $! tofl(a)*tofl(b)
 an,ad=nd(a)
 bn,bd=nd(b)
 $! Q(an*bn,ad*bd)
$, nneg(a):
 if $/(a)is $1:
  $!('Q',-a[1],a[2])
 $!-a
$, nsub(a,b):
 $! nadd(a,nneg(b))
$, ninv(a):
 t=$/(a)
 if t is $C:
  if a==0.0:
   err("Division by zero")
  $! 1.0/a
 n,d=nd(a)
 $! Q(d,n)
$, ndiv(a,b):
 $! nmul(a,ninv(b))
$, $a(a):
 if $/(a)is $1:
  a=a[1]
 if a>0:
  $! 1
 if a<0:
  $!-1
 $! 0
$, ncmp(a,b):
 $! $a(nsub(a,b))
$, nfloor(a):
 t=$/(a)
 if t is $q:
  $! a
 if t is $C:
  if a!=a or a in($C('$]'),$C('-$]')):
   err("Domain error")
  $! $q($P.floor(a))
 $! a[1]//a[2]
$, nabs(a):
 if $a(a)<0:
  $! nneg(a)
 $! a
$, nipow(a,k):
 if k<0:
  $! nipow(ninv(a),-k)
 if $/(a)is $C:
  $! a**k
 n,d=nd(a)
 $! Q(n**k,d**k)
$, iroot(n,k):
 if n<2:
  $! n
 x=$q($P.pow(n,1.0/k))if n<10**300 $( 1<<(($3(bin(n))-2)//k+1)
 if x<1:
  x=1
 $H $F:
  y=((k-1)*x+n//(x**(k-1)))//k
  if y>=x:
   $X
  x=y
 $H x**k>n:
  x-=1
 $H(x+1)**k<=n:
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
  $) i in $*(2,N):
   if $. s[i]:
    ps.$%(i)
    $) j in $*(i*i,N,i):
     s[j]=1
  SMALLP=ps
 $! SMALLP
$, $&(e,h):
 $! $/(e)is $1 $+ e[0]==h
$, head(e):
 if $/(e)is $1:
  $! e[0]
 $! $#
$, okey(e):
 $! repr(e)
$, has(e,x):
 if e==x:
  $! $F
 if $/(e)is $1 $+ e[0]!='Q':
  $) a in e[1:]:
   if has(a,x):
    $! $F
 $! $2
$, $8(e,x):
 $! $. has(e,x)
$, freeofall(e,xs):
 $) x in xs:
  if has(e,x):
   $! $2
 $! $F
$, ${(e,$?=$#):
 if $? is $#:
  $?=[]
 t=$/(e)
 if t is $u:
  if e $. in SPECIAL $+ e $. in $?:
   $?.$%(e)
 $J t is $1 $+ e[0]!='Q' $+ e[0]!='$u':
  $) a in e[1:]:
   ${(a,$?)
 $! $?
$, $5(e):
 t=$/(e)
 if t is $u:
  $! e in SPECIAL
 if t is $1 $+ e[0]!='Q':
  if e[0]=='$u':
   $! $2
  $) a in e[1:]:
   if $. $5(a):
    $! $2
 $! $F
$, $`(e):
 t=$/(e)
 if t is $C:
  $! $F
 if t is $1 $+ e[0]!='Q':
  $) a in e[1:]:
   if $`(a):
    $! $F
 $! $2
$, $V(a):
 if $/(a)is $1 $+ a[0]=='*' $+ $@(a[1]):
  if $3(a)==3:
   $! a[1],a[2]
  $! a[1],('*',)+a[2:]
 $! 1,a
$, cmul(c,r):
 if $/(c)is $q $+ c==1:
  $! r
 if $/(r)is $1 $+ r[0]=='*':
  if $@(r[1]):
   c=nmul(c,r[1])
   if $/(c)is $q $+ c==1:
    $!('*',)+r[2:]if $3(r)>3 $( r[2]
   $!('*',c)+r[2:]
  $!('*',c)+r[1:]
 $!('*',c,r)
$, $c(*$R):
 $! $6($R)
$, $6($R):
 num=0
 $N={}
 order=[]
 st=$G($R)
 infs=0
 $H st:
  a=st.pop()
  t=$/(a)
  if t is $q or t is $C:
   num=nadd(num,a)
   $7
  if t is $1:
   h=a[0]
   if h=='Q':
    num=nadd(num,a)
    $7
   if h=='+':
    st.extend(a[1:])
    $7
   if h=='*' $+ $@(a[1]):
    c=a[1]
    r=a[2]if $3(a)==3 $(('*',)+a[2:]
   $(:
    c=1
    r=a
  $(:
   if a=='$L':
    $! '$L'
   c=1
   r=a
  if r=='$]':
   s=$a(c)
   if s==0:
    $7
   if infs $+ infs!=s:
    $! '$L'
   infs=s
   $7
  if r in $N:
   $N[r]=nadd($N[r],c)
  $(:
   $N[r]=c
   order.$%(r)
 if infs:
  $! '$]' if infs>0 $(('*',-1,'$]')
 $?=[]
 $) r in order:
  c=$N[r]
  if c==0:
   $7
  $?.$%(cmul(c,r))
 if num!=0 or $. $?:
  if $? $+ num==0:
   pass
  $(:
   $?.$%(num)
 if $3($?)==1:
  $! $?[0]
 $?.sort(key=okey)
 $!('+',)+$1($?)
$, isrrad(e):
 $! $/(e)is $1 $+ e[0]=='^' $+ $/(e[1])is $q $+ isq(e[2])
$, $9(*$R):
 $! $E($R)
''')
_x(r'''$, $E($R):
 coef=1
 bases={}
 order=[]
 st=$G($R)
 $H st:
  a=st.pop()
  t=$/(a)
  if t is $q or t is $C:
   coef=nmul(coef,a)
   $7
  if t is $1:
   h=a[0]
   if h=='Q':
    coef=nmul(coef,a)
    $7
   if h=='*':
    st.extend(a[1:])
    $7
   if h=='^':
    b=a[1]
    x=a[2]
   $(:
    b=a
    x=1
  $(:
   if a=='$L':
    $! '$L'
   b=a
   x=1
  if b in bases:
   bases[b]=$c(bases[b],x)
  $(:
   bases[b]=x
   order.$%(b)
 if coef==0:
  if '$]' in bases:
   $! '$L'
  $) b in order:
   if b=='$L' or has(b,'$L'):
    $! '$L'
  $! coef
 facs=[]
 rad={}
 radorder=[]
 $, collect(p):
  c=1
  t=$/(p)
  if t is $q or t is $C or(t is $1 $+ p[0]=='Q'):
   $! p
  if t is $1 $+ p[0]=='*':
   items=p[1:]
  $(:
   items=(p,)
  $) f in items:
   if $@(f):
    c=nmul(c,f)
   $J isrrad(f):
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
  if p=='$L':
   $! '$L'
  coef=nmul(coef,collect(p))
 if rad:
  multi=$3(radorder)!=$3(rad)
  if multi:
   items=[(ex,rad[ex])$) ex in radorder if ex is $. $#]
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
 if '$]' in facs:
  if $3(facs)==1 or $F:
   coef=$a(coef)if $/(coef)is $. $C $((1.0 if coef>0 $(-1.0)
   if $/(coef)is $C:
    coef=$q(coef)
 if $. facs:
  $! coef
 if $3(facs)>1:
  algs=[f $) f in facs if $&(f,'+')$+ isalg(f)]
  if algs $+ all([isalg(f)$) f in facs]):
   r=coef
   $) f in facs:
    r=expand_mul(r,f)
   $! r
 if $3(facs)==1:
  f=facs[0]
  if $/(coef)is $q $+ coef==1:
   $! f
  if $/(f)is $1 $+ f[0]=='+':
   $! $6([$9(coef,t)$) t in f[1:]])
  $!('*',coef,f)
 facs.sort(key=okey)
 if $/(coef)is $q $+ coef==1:
  $!('*',)+$1(facs)
 $!('*',coef)+$1(facs)
$, $o(a):
 $! $9(-1,a)
$, $b(a,b):
 $! $c(a,$9(-1,b))
$, $Y(a,b):
 $! $9(a,pw(b,-1))
$, inv(a):
 $! pw(a,-1)
$, $T(a):
 $! pw(a,$|)
$, factor_int_small(n):
 fs=[]
 $) p in smallprimes():
  if p*p>n:
   $X
  if n%p==0:
   k=0
   $H n%p==0:
    n//=p
    k+=1
   fs.$%((p,k))
 $! fs,n
$, radical(n,q):
 if n<2:
  $! n,1
 a=1
 m=1
 fs,$_=factor_int_small(n)
 $) p,k in fs:
  a*=p**(k//q)
  m*=p**(k%q)
 if $_>1:
  r=iroot($_,q)
  if r**q==$_:
   a*=r
  $(:
   m*=$_
 $! a,m
$, ipow_root(n,p,q):
 a,m=radical(n**p,q)if p>1 $( radical(n,q)
 if m==1:
  $! a
 ex=Q(1,q)
 k=2
 $}=$#
 $H(1<<k)<=m:
  r=iroot(m,k)
  if r**k==m:
   $}=(r,k)
  k+=1
 if $} is $. $#:
  m=$}[0]
  ex=Q($}[1],q)
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
 h='%x'%$I(n)
 v=$q(h[0],16)
 $! 4*$3(h)-(3 if v<2 $( 2 if v<4 $( 1 if v<8 $( 0)
$, bigpow(b,x):
 n,d=nd(b)
 if d==1 $+ $I(n)<=1:
  $! $2
 $! $I(x)*(ibits(n)+(ibits(d)if d>1 $( 0))>MAXBITS
$, pw_num(b,x):
 if $/(b)is $C or $/(x)is $C:
  bf=tofl(b)
  xf=tofl(x)
  if bf==0.0:
   if xf>0:
    $! 0.0
   if xf==0:
    $! 1.0
   $! '$L'
  if bf!=bf or xf!=xf:
   $! '$L'
  if bf<0 $+(xf in($C('$]'),$C('-$]'))or xf!=$P.floor(xf)):
   if $m(x)$+ nd(x)[1]%2==1:
    r=(-bf)**xf
    $!-r if nd(x)[0]%2 $( r
   z=$0(bf)**xf
   $! fromcomplex(z)
  try:
   $! bf**xf
  $< $U:
   $! '$]'
 if $/(x)is $q:
  if b==0:
   if x<0:
    $! '$L'
   $! 0
  if bigpow(b,x):
   $!('^',b,x)
  $! nipow(b,x)
 p,q=nd(x)
 if b==0:
  $! 0 if p>0 $( '$L'
 if $a(b)<0:
  if q%2==1:
   r=pw_num(nneg(b),x)
   if p%2:
    $! $9(-1,r)
   $! r
  if q==2:
   $! $9(pw('i',p),pw_num(nneg(b),x))
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
 $) pt in parts:
  if $@(pt):
   c=nmul(c,pt)
  $J pt[0]=='*':
   c=nmul(c,pt[1])
   facs.$%(pt[2])
  $(:
   facs.$%(pt)
 if $3(facs)==2:
  if facs[0][2]==facs[1][2]:
   $! $9(c,pw_num(facs[0][1]*facs[1][1],facs[0][2]))
  facs.sort(key=okey)
 if $. facs:
  $! c
 if c==1:
  if $3(facs)==1:
   $! facs[0]
  $!('*',)+$1(facs)
 $!('*',c)+$1(facs)
$, isposconst(e):
 if $@(e):
  $! $a(e)>0
 if e=='pi' or e=='e':
  $! $F
 if isrrad(e):
  $! e[1]>0
 if $&(e,'^')$+(e[1]=='e' or e[1]=='pi')$+ isreal_expr(e[2]):
  $! $F
 $! $2
$, isalg(e):
 t=$/(e)
 if t is $q or t is $C:
  $! $F
 if t is $u:
  $! e=='i'
 h=e[0]
 if h=='Q':
  $! $F
 if h=='^':
  $! $@(e[1])$+ $@(e[2])
 if h=='+' or h=='*':
  $) a in e[1:]:
   if $. isalg(a):
    $! $2
  $! $F
 $! $2
''')
_x(r'''$, pw(b,x):
 if x==0:
  if b=='$L' or b=='$]':
   $! '$L'
  $! 1
 if $/(x)is $q $+ x==1:
  $! b
 if b=='$L' or x=='$L':
  $! '$L'
 bn=$@(b)
 xn=$@(x)
 if bn $+ xn:
  $! pw_num(b,x)
 if b==1 $+ $/(b)is $q:
  $! 1
 if b=='$]':
  if xn:
   $! '$]' if $a(x)>0 $( 0
  if x=='$]':
   $! '$]'
 if xn $+ b==0:
  $! 0 if $a(x)>0 $( '$L'
 if b=='i' $+ $/(x)is $q:
  r=x%4
  $!(1,'i',-1,('*',-1,'i'))[r]
 if x=='$]' $+ bn:
  if nabs(b)==1:
   $! '$L' if b==1 $( '$L'
  if ncmp(nabs(b),1)>0:
   $! '$]' if $a(b)>0 $( '$L'
  $! 0
 if b=='e':
  if x=='$]':
   $! '$]'
  if $&(x,'*')$+ $3(x)==3 $+ x[1]==-1 $+ x[2]=='$]':
   $! 0
  if $/(x)is $C:
   $! $P.exp(x)
  if $&(x,'ln'):
   $! x[1]
  if $&(x,'*'):
   c,r=$V(x)
   if $&(r,'ln')$+ $m(c):
    $! pw(r[1],c)
  if $&(x,'+'):
   outs=[]
   $_=[]
   $) t in x[1:]:
    c,r=$V(t)
    if $&(r,'ln')$+ $m(c):
     outs.$%(pw(r[1],c))
    $(:
     $_.$%(t)
   if outs:
    $! $E(outs+[pw('e',$6($_))])
  if $&(x,'*')$+ 'i' in x $+ 'pi' in x:
   c,r=$V(x)
   if r==('*','i','pi')$+ $m(c):
    $! $c(cos_($9(c,'pi')),$9('i',sin_($9(c,'pi'))))
 if b!='e' $+ $5(b)$+ $5(x)$+ $. $m(x)$+(has(b,'i')or has(x,'i'))$+ $. $`(x):
  L=fn('ln',b)
  if $. $&(L,'ln')$+ $.($&(L,'+')$+ any([$&(t,'ln')$) t in L[1:]])):
   $! pw('e',$;($9(x,L)))
 if $/(b)is $1:
  h=b[0]
  if h=='^':
   bb=b[1]
   ee=b[2]
   if $/(x)is $q:
    $! pw(bb,$9(ee,x))
   if isposconst(bb):
    $! pw(bb,$9(ee,x))
   if $m(ee)$+ $m(x):
    r=nmul(ee,x)
    if $/(ee)is $q:
     if ee%2==0:
      if $/(r)is $q $+ r%2==0:
       $! pw(bb,r)
      $! pw(fn('$I',bb),r)
     $! pw(bb,r)
    if nd(ee)[0]%2==1 $+ nd(ee)[1]%2==1:
     $! pw(bb,r)
    if nd(ee)[0]%2==1:
     $! pw(bb,r)
  $J h=='*':
   if $/(x)is $q:
    $! $E([pw(f,x)$) f in b[1:]])
   outs=[]
   $_=[]
   $) f in b[1:]:
    if $@(f):
     if $a(f)>0:
      outs.$%(pw(f,x))
     $J f!=-1:
      outs.$%(pw(nneg(f),x))
      $_.$%(-1)
     $(:
      $_.$%(f)
    $J isposconst(f)or $&(f,'$I'):
     outs.$%(pw(f,x))
    $(:
     $_.$%(f)
   if outs:
    $! $E(outs+[pw($E($_),x)])
  $J h=='$I':
   if $/(x)is $q $+ x%2==0:
    $! pw(b[1],x)
  $J h=='+':
   if x==$| $+ isalg(b)$+ $. has(b,'i'):
    dn=denest(b)
    if dn is $. $#:
     $! dn
   if isq(x)$+ x[2]==2 $+ $a(x)<0 $+ isalg(b)$+ $. has(b,'i'):
    dn=denest(b)
    if dn is $. $#:
     $! pw(pw(dn,-1),-x[1])if x[1]!=-1 $( pw(dn,-1)
   if $/(x)is $q $+ x!=1 $+ $. isalg(b):
    c=sumcontent(b)
    if c!=1:
     $! $9(pw(c,x),pw($9(ninv(c),b),x))
    if leadneg(b):
     nb=$9(-1,b)
     if x%2==0:
      $! pw(nb,x)
     $! $9(-1,pw(nb,x))
   if $/(x)is $q $+ isalg(b):
    if x>0 $+ x<=64:
     $! expand_pow(b,x)
    if x<0 $+ x>=-64:
     r=rationalize_inv(b)
     if r is $. $#:
      if x==-1:
       $! r
      $! expand_pow(r,-x)
 $!('^',b,x)
$, tdeg(r):
 d=0
 fs=r[1:]if $&(r,'*')$((r,)
 $) f in fs:
  if $/(f)is $u $+ f $. in SPECIAL:
   d+=1
  $J $&(f,'^')$+ $/(f[1])is $u $+ f[1]$. in SPECIAL $+ $@(f[2]):
   d+=tofl(f[2])
 $! d
$, leadneg(b):
 $}=$#
 bk=$#
 $) t in b[1:]:
  if $@(t):
   $7
  c,r=$V(t)
  k=(-tdeg(r),okey(r))
  if bk is $# or k<bk:
   bk=k
   $}=c
 if $} is $#:
  $! $2
 $! $a($})<0 if $@($})$( $2
$, sumcontent(b):
 g=0
 L=1
 $) t in b[1:]:
  c,r=$V(t)
  if $. $m(c):
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
  if $m(t):
   a=nadd(a,t)
   $7
  cc,r=$V(t)
  if isrrad(r)$+ r[2]==$| $+ $m(cc)$+(n is $# or n==r[1]):
   n=r[1]
   c=nadd(c,cc)
  $(:
   $! $#
 if n is $# or c==0:
  $! $#
 d2=nsub(nmul(a,a),nmul(nmul(c,c),n))
 if $a(d2)<0:
  $! $#
 dn,dd=nd(d2)
 rn=isqrt(dn)
 rd=isqrt(dd)
 if rn*rn!=dn or rd*rd!=dd:
  $! $#
 d=Q(rn,rd)
 p=ndiv(nadd(a,d),2)
 m=ndiv(nsub(a,d),2)
 if $a(p)<0 or $a(m)<0:
  $! $#
 r=$c(pw(p,$|),$9($a(c),pw(m,$|)))
 if $&(r,'+')$+ $3(r)<=3:
  $! r
 $! $#
$, expand_mul(a,b):
 ta=a[1:]if $&(a,'+')$((a,)
 tb=b[1:]if $&(b,'+')$((b,)
 $?=[]
 $) u in ta:
  $) v in tb:
   $?.$%($9(u,v))
 $! $6($?)
$, expand_pow(b,n):
 r=1
 p=b
 $H n>0:
  if n&1:
   r=expand_mul(r,p)
  n>>=1
  if n:
   p=expand_mul(p,p)
 $! r
$, rationalize_inv(b):
 re_,im_=reim(b)
 if im_!=0:
  d=$c($9(re_,re_),$9(im_,im_))
  d=$;(d)
  if $&(d,'+'):
   r2=rationalize_inv(d)
   if r2 is $#:
    $! $#
  $(:
   r2=pw(d,-1)
  $! expand_mul($b(re_,$9('i',im_)),r2)
 $N=b[1:]if $&(b,'+')$((b,)
 kern=$#
 kerns=[]
 $) t in $N:
  c,r=$V(t)
  if r!=1 $+ $. $@(r):
   if isrrad(r)$+ r[2]==$|:
    if r $. in kerns:
     kerns.$%(r)
   $(:
    $! $#
 if $. kerns or $3(kerns)>3:
  $! $#
 kern=kerns[0]
 if $3(kerns)>1:
  A=$6([t $) t in $N if $V(t)[1]!=kern])
  B=$6([$V(t)[0]$) t in $N if $V(t)[1]==kern])
  den=$;($b($9(A,A),$9(B,B,kern[1])))
  if den==0:
   $! $#
  if $&(den,'+'):
   r2=rationalize_inv(den)
   if r2 is $#:
    $! $#
  $(:
   r2=pw(den,-1)
  $! expand_mul($b(A,$9(B,kern)),r2)
 a0=0
 a1=0
 $) t in $N:
  c,r=$V(t)
  if r==kern:
   a1=nadd(a1,c)
  $(:
   a0=$c(a0,t)
 den=$b($9(a0,a0),$9(nmul(a1,a1),kern[1]))
 if den==0:
  $! $#
 $! expand_mul($b(a0,$9(a1,kern)),pw(den,-1))
''')
_x(r'''$, reim(e):
 t=$/(e)
 if t is $q or t is $C:
  $! e,0
 if t is $u:
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
  $! $6(rs),$6(ims)
 if h=='*':
  r=1
  i=0
  $) a in e[1:]:
   ar,ai=reim(a)
   if ai==0:
    r=$9(r,ar)
    i=$9(i,ar)
   $(:
    r,i=$b($9(r,ar),$9(i,ai)),$c($9(r,ai),$9(i,ar))
  $! r,i
 if h=='^':
  b=e[1]
  x=e[2]
  if $. has(b,'i')$+ $. has(x,'i'):
   if $@(x)$+ $. $m(x):
    $! e,0
   if $m(x)$+ nd(x)[1]%2==0:
    if $5(b):
     v=cv(b)
     if v is $. $# $+ $/(v)is $. $0 $+ v<0:
      $! reim_generic(e)
    $! e,0
   $! e,0
  if $/(x)is $q:
   br,bi=reim(b)
   if x>0:
    z=expand_pow($c(br,$9('i',bi)),x)
    if has(z,'i')$+ z!=e:
     $! reim(z)
   $J $5(b):
    r=rationalize_inv(b)
    if r is $. $#:
     $! reim(expand_pow(r,-x))if x!=-1 $( reim(r)
  $! reim_generic(e)
 if h in('$G','mat','$u'):
  $! e,0
 $) a in e[1:]:
  if has(a,'i'):
   $! reim_generic(e)
 $! e,0
$, cv(u):
 try:
  v=$S(u)
 $<($M,$O,$B,$U,TypeError):
  $! $#
 if v!=v:
  $! $#
 if $/(v)is $0:
  if v.$Q!=v.$Q or v.imag!=v.imag:
   $! $#
  if $I(v.$Q)==$C('$]')or $I(v.imag)==$C('$]'):
   $! $#
 $J $I(v)==$C('$]'):
  $! $#
 $! v
$, reim_generic(e):
 if $5(e):
  v=cv(e)
  if v is $#:
   $!('$Q',e),('imag',e)
  z=$0(v)
  $! z.$Q,z.imag
 $!('$Q',e),('imag',e)
$, conj(e):
 r,i=reim(e)
 $! $b(r,$9('i',i))
$, fromcomplex(z):
 if $/(z)is $. $0:
  $! z
 if z.imag==0:
  $! z.$Q
 if z.$Q==0:
  $! $9(z.imag,'i')
 $! $c(z.$Q,$9(z.imag,'i'))
$k={}
$, fn($D,*$R):
 if $3($R)==1 $+ $/($R[0])is $G:
  $R=$1($R[0])
 $) a in $R:
  if a=='$L':
   $! '$L'
 f=$k.get($D)
 if f is $. $#:
  r=f(*$R)
  if r is $. $#:
   $! r
 $!($D,)+$1($R)
$, isneg(e):
 if $@(e):
  $! $a(e)<0
 if $&(e,'*'):
  $! $@(e[1])$+ $a(e[1])<0
 if $&(e,'+'):
  $! leadneg(e)
 $! $2
$, isreal_expr(e):
 if $@(e):
  $! $F
 if $/(e)is $u:
  $! e!='i' $+ e!='$L'
 $! $. has(e,'i')
$, fval($D,x):
 $! fromcomplex(NUMF[$D](x))
$, fvalc($D,u):
 try:
  v=NUMF[$D]($S(u))
 $<($M,$O,$B,$U,TypeError):
  $! $#
 if $/(v)is $0:
  if v.$Q!=v.$Q or v.imag!=v.imag:
   $! $#
 $J v!=v:
  $! $#
 $! fromcomplex(v)
$, pi_coef(u):
 if u=='pi':
  $! 1
 if u==0:
  $! 0
 if $&(u,'*')$+ $3(u)==3 $+ u[2]=='pi' $+ $m(u[1]):
  $! u[1]
 $! $#
$, split_pi(u):
 if $&(u,'+'):
  $) t in u[1:]:
   c=pi_coef(t)
   if c is $. $# $+ c!=0:
    $_=$6([s $) s in u[1:]if s is $. t])
    $! c,$_
 $! $#
TRIGT=$#
$, trig_table():
 global TRIGT
 if TRIGT is $#:
  s2=$T(2)
  s3=$T(3)
  s5=$T(5)
  s6=$T(6)
  q=Q
  T={}
  T[0]=0
  T[q(1,12)]=$9(q(1,4),$b(s6,s2))
  T[q(1,10)]=$9(q(1,4),$b(s5,1))
  T[q(1,8)]=$9($|,$T($b(2,s2)))
  T[q(1,6)]=$|
  T[q(1,5)]=$9(q(1,4),$T($b(10,$9(2,s5))))
  T[q(1,4)]=$9($|,s2)
  T[q(3,10)]=$9(q(1,4),$c(s5,1))
  T[q(1,3)]=$9($|,s3)
  T[q(3,8)]=$9($|,$T($c(2,s2)))
  T[q(2,5)]=$9(q(1,4),$T($c(10,$9(2,s5))))
  T[q(5,12)]=$9(q(1,4),$c(s6,s2))
  T[$|]=1
  TT={}
  TT[0]=0
  TT[q(1,12)]=$b(2,s3)
  TT[q(1,8)]=$b(s2,1)
  TT[q(1,6)]=$9(q(1,3),s3)
  TT[q(1,4)]=1
  TT[q(1,3)]=s3
  TT[q(3,8)]=$c(s2,1)
  TT[q(5,12)]=$c(2,s3)
  TT[q(1,5)]=$T($b(5,$9(2,s5)))
  TT[q(2,5)]=$T($c(5,$9(2,s5)))
  TT[q(1,10)]=$9(q(1,5),$T($b(25,$9(10,s5))))
  TT[q(3,10)]=$9(q(1,5),$T($c(25,$9(10,s5))))
  TRIGT=(T,TT)
 $! TRIGT
$, sin_pi(c):
 c=nsub(c,nmul(2,nfloor(nmul(c,$|))))
 sg=1
 if ncmp(c,1)>=0:
  c=nsub(c,1)
  sg=-1
 if ncmp(c,$|)>0:
  c=nsub(1,c)
 T=trig_table()[0]
 if c in T:
  $! $9(sg,T[c])
 if sg<0:
  $! $o(('sin',$9(c,'pi')))
 $!('sin',$9(c,'pi'))
$, tan_pi(c):
 c=nsub(c,nfloor(c))
 sg=1
 if ncmp(c,$|)>0:
  c=nsub(1,c)
  sg=-1
 if c==$|:
  $! '$L'
 TT=trig_table()[1]
 if c in TT:
  $! $9(sg,TT[c])
 $! $9(sg,('tan',$9(c,'pi')))
$, sin_(u):
 if $@(u):
  if u==0:
   $! 0
  if $/(u)is $C:
   $! $P.sin(u)
  $! $#
 if u=='$]' or u==('*',-1,'$]'):
  $! '$L'
 c=pi_coef(u)
 if c is $. $#:
  $! sin_pi(c)
 if $`(u)$+ $5(u):
  $! fvalc('sin',u)
 if isneg(u):
  $! $o(fn('sin',$o(u)))
 sp=split_pi(u)
 if sp is $. $#:
  c,$_=sp
  c=nsub(c,nmul(2,nfloor(nmul(c,$|))))
  if c==0:
   $! fn('sin',$_)
  if c==1:
   $! $o(fn('sin',$_))
  if c==$|:
   $! fn('cos',$_)
  if c==Q(3,2):
   $! $o(fn('cos',$_))
  if ncmp(c,1)>0:
   $!('sin',$c($_,$9(nsub(c,2),'pi')))
  $!('sin',$c($_,$9(c,'pi')))
 if $&(u,'$w'):
  $! u[1]
 if $&(u,'arccos'):
  $! $T($b(1,pw(u[1],2)))
 if $&(u,'$t'):
  $! $Y(u[1],$T($c(1,pw(u[1],2))))
 $! $#
''')
_x(r'''$, cos_(u):
 if $@(u):
  if u==0:
   $! 1
  if $/(u)is $C:
   $! $P.cos(u)
  $! $#
 if u=='$]' or u==('*',-1,'$]'):
  $! '$L'
 c=pi_coef(u)
 if c is $. $#:
  $! sin_pi(nadd(c,$|))
 if $`(u)$+ $5(u):
  $! fvalc('cos',u)
 if isneg(u):
  $! fn('cos',$o(u))
 sp=split_pi(u)
 if sp is $. $#:
  c,$_=sp
  c=nsub(c,nmul(2,nfloor(nmul(c,$|))))
  if c==0:
   $! fn('cos',$_)
  if c==1:
   $! $o(fn('cos',$_))
  if c==$|:
   $! $o(fn('sin',$_))
  if c==Q(3,2):
   $! fn('sin',$_)
  if ncmp(c,1)>0:
   $!('cos',$c($_,$9(nsub(c,2),'pi')))
  $!('cos',$c($_,$9(c,'pi')))
 if $&(u,'arccos'):
  $! u[1]
 if $&(u,'$w'):
  $! $T($b(1,pw(u[1],2)))
 if $&(u,'$t'):
  $! pw($c(1,pw(u[1],2)),Q(-1,2))
 $! $#
$, tan_(u):
 if $@(u):
  if u==0:
   $! 0
  if $/(u)is $C:
   $! $P.tan(u)
  $! $#
 c=pi_coef(u)
 if c is $. $#:
  $! tan_pi(c)
 if $`(u)$+ $5(u):
  $! fvalc('tan',u)
 if isneg(u):
  $! $o(fn('tan',$o(u)))
 sp=split_pi(u)
 if sp is $. $#:
  c,$_=sp
  c=nsub(c,nfloor(c))
  if c==0:
   $! fn('tan',$_)
  if c==$|:
   $! $o(pw(fn('tan',$_),-1))
  $!('tan',$c($_,$9(c,'pi')))
 if $&(u,'$t'):
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
 if $@(u):
  if $/(u)is $C:
   if-1.0<=u<=1.0:
    $! $P.asin(u)
   $! fval('$w',u)
 if isneg(u):
  $! $o(fn('$w',$o(u)))
 S=inv_table()[0]
 if u in S:
  $! $9(S[u],'pi')
 if $5(u)$+ $`(u):
  $! fvalc('$w',u)
 $! $#
$, acos_(u):
 if $@(u)$+ $/(u)is $C:
  if-1.0<=u<=1.0:
   $! $P.acos(u)
  $! fval('arccos',u)
 a=asin_(u)
 if a is $. $# $+ $. $&(a,'$w')$+ $8(a,'$w'):
  $! $b($9($|,'pi'),a)
 if isneg(u):
  $! $b('pi',fn('arccos',$o(u)))
 $! $#
$, atan_(u):
 if $@(u):
  if $/(u)is $C:
   $! $P.atan(u)
 if u=='$]':
  $! $9($|,'pi')
 if u==('*',-1,'$]'):
  $! $9(Q(-1,2),'pi')
 if isneg(u):
  $! $o(fn('$t',$o(u)))
 Tn=inv_table()[1]
 if u in Tn:
  $! $9(Tn[u],'pi')
 if $5(u)$+ $`(u):
  $! fvalc('$t',u)
 $! $#
$, ln_(u):
 if $@(u):
  if u==1:
   $! 0
  if u==0:
   $!('*',-1,'$]')
  if $/(u)is $C:
   if u>0:
    $! $P.log(u)
   $! $c($P.log(-u),$9($P.pi,'i'))
  if $a(u)<0:
   $! $c(fn('ln',nneg(u)),$9('i','pi'))
  n,d=nd(u)
  if n==1:
   $! $o(fn('ln',d))
  $! $#
 if u=='e':
  $! 1
 if u=='$]':
  $! '$]'
 if u=='i':
  $! $9($|,'i','pi')
 if $&(u,'^'):
  if u[1]=='e' $+ isreal_expr(u[2]):
   $! u[2]
  if isposconst(u[1])$+ isreal_expr(u[2])$+ $@(u[2]):
   $! $9(u[2],fn('ln',u[1]))
 if $5(u)$+ $`(u):
  $! fvalc('ln',u)
 $! $#
$, log_(u,b=10):
 if $@(u)$+ $@(b):
  if $/(u)is $C or $/(b)is $C:
   a1=fvalc('ln',u)
   a2=fvalc('ln',b)
   if a1 is $. $# $+ a2 is $. $# $+ a2!=0:
    $! $Y(a1,a2)
   $! $#
  if u==1:
   $! 0
  if $m(u)$+ $m(b)$+ $a(u)>0 $+ $a(b)>0 $+ b!=1:
   k=exact_log(u,b)
   if k is $. $#:
    $! k
 if u==b:
  $! 1
 if $&(u,'^')$+ u[1]==b $+ isreal_expr(u[2]):
  $! u[2]
 if $5(u)$+ $5(b)$+($`(u)or $`(b)):
  a1=fvalc('ln',u)
  a2=fvalc('ln',b)
  if a1 is $. $# $+ a2 is $. $# $+ a2!=0:
   $! $Y(a1,a2)
  $! $#
 $! $#
$, exact_log(u,b):
 un,ud=nd(u)
 bn,bd=nd(b)
 lu=$P.log(tofl(u))
 lb=$P.log(tofl(b))
 if lb==0:
  $! $#
 k=lu/lb
 $) den in $*(1,13):
  num=$q(round(k*den))
  if $I(k*den-num)<1e-9:
   kk=Q(num,den)
   if pw_num(b,kk)==u:
    $! kk
   $! $#
 $! $#
$, abs_(u):
 if $@(u):
  $! nabs(u)
 if u=='$]' or u==('*',-1,'$]'):
  $! '$]'
 if $&(u,'$I'):
  $! u
 if $&(u,'^')$+ $/(u[2])is $q $+ u[2]%2==0 $+ isreal_expr(u[1]):
  $! u
 if has(u,'i'):
  r,i=reim(u)
  if i!=0 $+ $. has(r,'i')$+ $. has(i,'i'):
   $! $T($c(pw(r,2),pw(i,2)))
 if $5(u):
  v=cv(u)
  if v is $. $# $+ $/(v)is $. $0:
   if v>=0:
    $! u
   $! $o(u)
 if $&(u,'*'):
  outs=[]
  $_=[]
  $) f in u[1:]:
   if $@(f):
    outs.$%(nabs(f))
   $J $5(f):
    outs.$%(abs_(f)or('$I',f))
   $J $&(f,'^')$+ $/(f[2])is $q $+ f[2]%2==0:
    outs.$%(f)
   $J $&(f,'^')$+ f[1]=='e':
    outs.$%(f)
   $(:
    $_.$%(f)
  if outs:
   $! $E(outs+[fn('$I',$E($_))])
 if isneg(u):
  $! fn('$I',$o(u))
 if $&(u,'^')$+ u[1]=='e' $+ isreal_expr(u[2]):
  $! u
 $! $#
$, sign_(u):
 if $@(u):
  $! $a(u)if $/(u)is $. $C $( $C($a(u))
 if u=='$]':
  $! 1
 if $5(u):
  v=cv(u)
  if v is $. $# $+ $/(v)is $. $0:
   $! 1 if v>0 $((-1 if v<0 $( 0)
 if $&(u,'*')$+ $@(u[1]):
  $! $9($a(u[1]),fn('sign',cmul(nabs(u[1]),$V(u)[1])))
 if $&(u,'^')$+ $/(u[2])is $q $+ u[2]%2==0:
  $! $#
 $! $#
$, finite(v):
 $! v==v $+ v!=$C('$]')$+ v!=$C('-$]')
$, floor_(u):
 if $@(u):
  if $/(u)is $C:
   $! $C($P.floor(u))if finite(u)$( $#
  $! nfloor(u)
 if $5(u)$+ $. has(u,'i'):
  v=cv(u)
  if v is $. $# $+ $/(v)is $. $0:
   $! $q($P.floor(v))
 $! $#
$, ceil_(u):
 f=floor_($o(u))
 if f is $. $#:
  $! $o(f)
 $! $#
$, sinh_(u):
 if u==0:
  $! 0
 if isneg(u):
  $! $o(fn('sinh',$o(u)))
 if $&(u,'arcsinh'):
  $! u[1]
 $! $#
''')
_x(r'''$, cosh_(u):
 if u==0:
  $! 1
 if isneg(u):
  $! fn('cosh',$o(u))
 if $&(u,'arccosh'):
  $! u[1]
 $! $#
$, tanh_(u):
 if u==0:
  $! 0
 if isneg(u):
  $! $o(fn('tanh',$o(u)))
 $! $#
$, odd0($D):
 $, g(u):
  if u==0:
   $! 0
  if isneg(u):
   $! $o(fn($D,$o(u)))
  $! $#
 $! g
$, fact_(u):
 if $/(u)is $q:
  if u<0:
   $! '$L'
  if u>1000:
   $! $#
  r=1
  $) k in $*(2,u+1):
   r*=k
  $! r
 if isq(u)$+ u[2]==2 $+ u[1]>0:
  n=u[1]
  r=$9($T('pi'),Q(1,1))
  k=Q(1,2)
  $H ncmp(k,u)<=0:
   r=$9(r,k)
   k=nadd(k,1)
  $! r
 if $/(u)is $C:
  if u<0 $+ u==$P.floor(u):
   $! '$L'
  try:
   $! gamma(u+1.0)
  $<($U,$B,$O):
   $! '$]' if u>0 $( '$L'
 $! $#
$, gamma(x):
 try:
  $! $P.gamma(x)
 $< AttributeError:
  pass
 if x<0.5:
  $! $P.pi/($P.sin($P.pi*x)*gamma(1.0-x))
 x-=1.0
 g=7
 c=(0.99999999999980993,676.5203681218851,-1259.1392167224028,
 771.32342877765313,-176.61502916214059,12.507343278686905,
 -0.13857109526572012,9.9843695780195716e-6,1.5056327351493116e-7)
 a=c[0]
 t=x+g+0.5
 $) k in $*(1,9):
  a+=c[k]/(x+k)
 h=t**((x+0.5)/2)
 $! $P.$T(2*$P.pi)*h*$P.exp(-t)*h*a
$, real_(u):
 if $5(u)or has(u,'i'):
  r,i=reim(u)
  if $. $&(r,'$Q'):
   $! r
 if isreal_expr(u):
  $! u
 $! $#
$, imag_(u):
 if isreal_expr(u):
  $! 0
 r,i=reim(u)
 if $. $&(i,'imag'):
  $! i
 $! $#
$, conj_(u):
 if isreal_expr(u):
  $! u
 r,i=reim(u)
 if $. $&(r,'$Q'):
  $! $b(r,$9('i',i))
 $! $#
$, angle_(u):
 r,i=reim(u)
 if $&(r,'$Q')or $&(i,'imag'):
  $! $#
 if i==0:
  if $5(r):
   v=cv(r)
   if v is $. $# $+ $/(v)is $. $0:
    if v>=0:
     $! 0
    $! 'pi'
  $! $#
 if r==0:
  if $5(i):
   v=cv(i)
   if v is $. $# $+ $/(v)is $. $0:
    $! $9(Q(1 if v>0 $(-1,2),'pi')
  $! $#
 if $5(r)$+ $5(i):
  vr=cv(r)
  vi=cv(i)
  if vr is $# or vi is $# or $/(vr)is $0 or $/(vi)is $0:
   $! $#
  a=fn('$t',$Y(i,r))
  if vr<0:
   if vi>=0:
    a=$c(a,'pi')
   $(:
    a=$b(a,'pi')
  $! a
 $! $#
$k['sin']=sin_
$k['cos']=cos_
$k['tan']=tan_
$k['$w']=asin_
$k['arccos']=acos_
$k['$t']=atan_
$k['ln']=ln_
$k['log']=log_
$k['$I']=abs_
$k['sign']=sign_
$k['floor']=floor_
$k['ceiling']=ceil_
$k['sinh']=sinh_
$k['cosh']=cosh_
$k['tanh']=tanh_
$k['arcsinh']=odd0('arcsinh')
$k['arctanh']=odd0('arctanh')
$k['arccosh']=$4 u:0 if u==1 $( $#
$k['fact']=fact_
$k['$Q']=real_
$k['imag']=imag_
$k['conj']=conj_
$k['$p']=angle_
$k['exp']=$4 u:pw('e',u)
$k['$T']=$4 u:pw(u,$|)
$k['sec']=$4 u:pw(fn('cos',u),-1)
$k['csc']=$4 u:pw(fn('sin',u),-1)
$k['cot']=$4 u:pw(fn('tan',u),-1)
$k['sech']=$4 u:pw(fn('cosh',u),-1)
$k['csch']=$4 u:pw(fn('sinh',u),-1)
$k['coth']=$4 u:pw(fn('tanh',u),-1)
$k['arcsec']=$4 u:fn('arccos',pw(u,-1))
$k['arccsc']=$4 u:fn('$w',pw(u,-1))
$k['arccot']=$4 u:$b($9($|,'pi'),fn('$t',u))
$k['arcsech']=$4 u:fn('arccosh',pw(u,-1))
$k['arccsch']=$4 u:fn('arcsinh',pw(u,-1))
$k['arccoth']=$4 u:fn('arctanh',pw(u,-1))
$, root_(u,n=2):
 $! pw(u,pw(n,-1))
$k['root']=root_
import cmath
$, _c(f):
 $, g(x):
  try:
   if $/(x)is $0:
    $! f[1](x)
   $! f[0](x)
  $<($O,TypeError):
   $! f[1]($0(x))
 $! g
$, _ln(x):
 if $/(x)is $. $0 $+ x>0:
  $! $P.log(x)
 if x==0:
  $! $C('-$]')
 $! cmath.log($0(x))
$, _asinr(x):
 if-1<=x<=1:
  $! $P.asin(x)
 $n $O
$, _acosr(x):
 if-1<=x<=1:
  $! $P.acos(x)
 $n $O
$, _casin(z):
 $!-1j*cmath.log(1j*z+cmath.$T(1-z*z))
$, _cacos(z):
 $! $P.pi/2-_casin(z)
$, _catan(z):
 $! 0.5j*cmath.log((1-1j*z)/(1+1j*z))
$, _sinh(x):
 $!(cmath.exp(x)-cmath.exp(-x))/2 if $/(x)is $0 $(($P.exp(x)-$P.exp(-x))/2
$, _cosh(x):
 $!(cmath.exp(x)+cmath.exp(-x))/2 if $/(x)is $0 $(($P.exp(x)+$P.exp(-x))/2
$, _tanh(x):
 if $/(x)is $. $0:
  if x>20:
   $! 1.0
  if x<-20:
   $!-1.0
  a=$P.exp(2*x)
  $!(a-1)/(a+1)
 a=cmath.exp(2*x)
 $!(a-1)/(a+1)
$, _asinh(x):
 if $/(x)is $. $0:
  $! $P.log(x+$P.$T(x*x+1))if x>=0 $(-$P.log(-x+$P.$T(x*x+1))
 $! cmath.log(x+cmath.$T(x*x+1))
$, _acosh(x):
 if $/(x)is $. $0 $+ x>=1:
  $! $P.log(x+$P.$T(x*x-1))
 x=$0(x)
 $! cmath.log(x+cmath.$T(x+1)*cmath.$T(x-1))
$, _atanh(x):
 if $/(x)is $. $0 $+-1<x<1:
  $! 0.5*$P.log((1+x)/(1-x))
 x=$0(x)
 $! 0.5*cmath.log((1+x)/(1-x))
$, _sign(x):
 if $/(x)is $0:
  $! x/$I(x)if x!=0 $( 0.0
 $! 1.0 if x>0 $((-1.0 if x<0 $( 0.0)
$, _floor(x):
 if $/(x)is $0:
  $! $0($P.floor(x.$Q),$P.floor(x.imag))
 $! $C($P.floor(x))
$, _ceil(x):
 if $/(x)is $0:
  $! $0($P.ceil(x.$Q),$P.ceil(x.imag))
 $! $C($P.ceil(x))
$, _real(x):
 $! x.$Q if $/(x)is $0 $( x
$, _imag(x):
 $! x.imag if $/(x)is $0 $( 0.0
$, _conj(x):
 $! x.conjugate()if $/(x)is $0 $( x
$, _angle(x):
 if $/(x)is $0:
  $! cmath.phase(x)
 $! 0.0 if x>=0 $( $P.pi
$, _fact(x):
 if $/(x)is $0:
  $n $O
 $! gamma(x+1.0)
''')
_x(r'''NUMF={
 'sin':_c(($P.sin,cmath.sin)),'cos':_c(($P.cos,cmath.cos)),
 'tan':_c(($P.tan,$4 z:cmath.sin(z)/cmath.cos(z))),
 '$w':_c((_asinr,_casin)),'arccos':_c((_acosr,_cacos)),
 '$t':_c(($P.atan,_catan)),
 'ln':_ln,'exp':_c(($P.exp,cmath.exp)),
 '$T':_c(($4 x:$P.$T(x)if x>=0 $( cmath.$T(x),cmath.$T)),
 '$I':$I,'sign':_sign,'floor':_floor,'ceiling':_ceil,
 'sinh':_sinh,'cosh':_cosh,'tanh':_tanh,
 'arcsinh':_asinh,'arccosh':_acosh,'arctanh':_atanh,
 '$Q':_real,'imag':_imag,'conj':_conj,'$p':_angle,
 'fact':_fact,
 }
$, nfun_call($D,$g):
 if $D=='log':
  b=$g[1]if $3($g)>1 $( 10.0
  $! _ln($g[0])/_ln(b)
 if $D=='root':
  n=$g[1]if $3($g)>1 $( 2.0
  $! npow($g[0],1.0/n)
 if $D=='round':
  d=$q($g[1])if $3($g)>1 $( 0
  $! round($g[0],d)
 if $D=='when':
  $! $g[1]if $g[0]$( $g[2]
 if $D=='max':
  $! max($g)
 if $D=='min':
  $! min($g)
 if $D=='mod':
  $! $g[0]-$g[1]*$P.floor($g[0]/$g[1])if $g[1]!=0 $( $g[0]
 f=NUMF.get($D)
 if f is $#:
  if $D in('sec','csc','cot','sech','csch','coth'):
   base={'sec':'cos','csc':'sin','cot':'tan','sech':'cosh','csch':'sinh','coth':'tanh'}[$D]
   $! 1.0/NUMF[base]($g[0])
  if $D in('arcsec','arccsc','arccot','arcsech','arccsch','arccoth'):
   base={'arcsec':'arccos','arccsc':'$w','arccot':'$t','arcsech':'arccosh','arccsch':'arcsinh','arccoth':'arctanh'}[$D]
   $! NUMF[base](1.0/$g[0])
  if $D in('ipart','$q'):
   $! $C($q($g[0]))
  if $D=='fpart':
   $! $g[0]-$q($g[0])
  err("Cannot evaluate "+$D)
 $! f($g[0])
$, npow(a,b):
 if $/(a)is $. $0 $+ $/(b)is $. $0:
  if a<0 $+(b!=b or b in($C('$]'),$C('-$]'))or b!=$P.floor(b)):
   $! $0(a)**b
  if a==0 $+ b<0:
   $n $B
  try:
   $! a**b
  $< $U:
   $! $C('$]')
 if a==0:
  $! 0.0
 $! $0(a)**b
NCONST={'pi':$P.pi,'e':$P.e,'i':1j,'$]':$C('$]')}
$, $S(e,env=$#):
 t=$/(e)
 if t is $q:
  try:
   $! $C(e)
  $< $U:
   $! '$]' if e>0 $(('*',-1,'$]')
 if t is $C:
  $! e
 if t is $u:
  if env is $. $# $+ e in env:
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
  if isq(x)$+ x[2]%2==1:
   bv=$S(b,env)
   if $/(bv)is $. $0 $+ bv<0:
    r=(-bv)**(x[1]/x[2])
    $!-r if x[1]%2 $( r
   $! npow(bv,x[1]/x[2])
  if $/(x)is $q:
   bv=$S(b,env)
   if bv==0 $+ x<0:
    $n $B
   $! bv**x
  $! npow($S(b,env),$S(x,env))
 if h in('$G','mat','$u','Q'):
  err("Not numeric")
 if h=='when':
  c=nbool(e[1],env)
  $! $S(e[2]if c $( e[3],env)if $3(e)>3 or c $( $S(e[2],env)
 $g=[$S(a,env)$) a in e[1:]]
 $! nfun_call(h,$g)
$, nbool(c,env):
 h=head(c)
 if h in('<','>','<=','>=','=','/='):
  a=$S(c[1],env)
  b=$S(c[2],env)
  if $/(a)is $0:
   a=a.$Q
  if $/(b)is $0:
   b=b.$Q
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
 if h=='$+':
  $) a in c[1:]:
   if $. nbool(a,env):
    $! $2
  $! $F
 if h=='or':
  $) a in c[1:]:
   if nbool(a,env):
    $! $F
  $! $2
 if h=='$.':
  $! $. nbool(c[1],env)
 if c=='true':
  $! $F
 if c=='false':
  $! $2
 err("Not a condition")
$, nreal(e,env=$#):
 v=$S(e,env)
 if $/(v)is $0:
  if $I(v.imag)>1e-9*(1+$I(v.$Q)):
   $n $O
  $! v.$Q
 $! v
$, simp(e):
 t=$/(e)
 if t is $. $1:
  $! e
 h=e[0]
 if h=='Q' or h=='$u' or h=='hold':
  if h=='hold':
   $! simp(e[1])
  $! e
 $R=[simp(a)$) a in e[1:]]
 if h=='+':
  $! $6($R)
 if h=='*':
  $! $E($R)
 if h=='^':
  $! pw($R[0],$R[1])
 if h in('$G','mat','=','<','>','<=','>=','/=','$+','or','$.'):
  $!(h,)+$1($R)
 $! fn(h,$R)
$, $W(e,old,new):
 if e==old:
  $! new
 t=$/(e)
 if t is $. $1 or e[0]=='Q' or e[0]=='$u':
  $! e
 ch=$2
 $R=[]
 $) a in e[1:]:
  b=$W(a,old,new)
  if b is $. a:
   ch=$F
  $R.$%(b)
 if $. ch:
  $! e
 $! simp((e[0],)+$1($R))
$, subsd(e,d):
 t=$/(e)
 if t is $u:
  if e in d:
   $! d[e]
  $! e
 if t is $. $1 or e[0]=='Q' or e[0]=='$u':
  $! e
 ch=$2
 $R=[]
 $) a in e[1:]:
  b=subsd(a,d)
  if b is $. a:
   ch=$F
  $R.$%(b)
 if $. ch:
  $! e
 $! simp((e[0],)+$1($R))
$, mapexpr(f,e):
 if $&(e,'$G'):
  $!('$G',)+$1(mapexpr(f,a)$) a in e[1:])
 if $&(e,'mat'):
  $!('mat',)+$1(mapexpr(f,a)$) a in e[1:])
 $! f(e)
$, $;(e):
 t=$/(e)
 if t is $. $1:
  $! e
 h=e[0]
 if h=='Q' or h=='$u':
  $! e
 if h=='+':
  $! $6([$;(a)$) a in e[1:]])
 if h=='*':
  r=1
  $) f in e[1:]:
   r=expand_mul(r,$;(f))
  $! r
 if h=='^':
  b=$;(e[1])
  x=$;(e[2])
  if $&(b,'+')$+ $/(x)is $q:
   if x>0:
    $! expand_pow(b,x)
   if x<0:
    $! pw(expand_pow(b,-x),-1)
  if $&(b,'*')$+ $/(x)is $q:
   $! $;($E([pw(f,x)$) f in b[1:]]))
  if b=='e' $+ $&(x,'+'):
   $! $E([pw('e',a)$) a in x[1:]])
  if $&(x,'+')$+ $@(b):
   $! $E([pw(b,a)$) a in x[1:]])
  $! pw(b,x)
 if h in('$G','mat','=','<','>','<=','>=','/=','$+','or','$.'):
  $!(h,)+$1($;(a)$) a in e[1:])
 $! fn(h,[$;(a)$) a in e[1:]])
''')
_x(r'''$, evalf(e):
 t=$/(e)
 if t is $q:
  $! $C(e)
 if t is $C:
  $! e
 if t is $u:
  if e=='pi':
   $! $P.pi
  if e=='e':
   $! $P.e
  $! e
 h=e[0]
 if h=='Q':
  $! e[1]/e[2]
 if h=='$u':
  $! e
 if $5(e)$+ h $. in('$G','mat','=','<','>','<=','>=','/=','$+','or','$.'):
  try:
   v=$S(e)
   if $/(v)is $0:
    $! fromcomplex(v)
   if v!=v:
    $! '$L'
   if v==$C('$]'):
    $! '$]'
   if v==$C('-$]'):
    $!('*',-1,'$]')
   $! v
  $<($B,$O,$U,TypeError):
   pass
  $< $M:
   pass
 $R=[evalf(a)$) a in e[1:]]
 if h=='^' $+ $/(e[2])is $q:
  $R[1]=e[2]
 $! simp((h,)+$1($R))
$, exactify(e,tol=$#):
 t=$/(e)
 if t is $C:
  $! float2rat(e,tol)
 if t is $1 $+ e[0]!='Q' $+ e[0]!='$u':
  $! simp((e[0],)+$1(exactify(a,tol)$) a in e[1:]))
 $! e
$, float2rat(x,tol=$#):
 if x!=x:
  $! '$L'
 if x==$C('$]'):
  $! '$]'
 if x==$C('-$]'):
  $!('*',-1,'$]')
 if x==$P.floor(x)$+ $I(x)<1e18:
  $! $q(x)
 if tol is $#:
  tol=5e-14*max(1.0,$I(x))
 h0,h1=0,1
 k0,k1=1,0
 y=x
 $) _ in $*(60):
  a=$P.floor(y)
  h0,h1=h1,$q(a)*h1+h0
  k0,k1=k1,$q(a)*k1+k0
  if $I(h1/k1-x)<=tol:
   $X
  f=y-a
  if f==0:
   $X
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
 if h=='^' $+ $/(e[2])is $q $+ e[2]>0:
  k=degree(e[1],x)
  if k is $#:
   $! $#
  $! k*e[2]
 $! $#
$, $^(e,x):
 e=$;(e)
 if $8(e,x):
  $![e]
 $N=e[1:]if $&(e,'+')$((e,)
 cs={}
 mx=0
 $) t in $N:
  if $&(t,'*'):
   k=0
   $_=[]
   $) f in t[1:]:
    if f==x:
     k+=1
    $J $&(f,'^')$+ f[1]==x $+ $/(f[2])is $q $+ f[2]>0:
     k+=f[2]
    $J $8(f,x):
     $_.$%(f)
    $(:
     $! $#
   c=$E($_)
  $J t==x:
   k=1
   c=1
  $J $&(t,'^')$+ t[1]==x $+ $/(t[2])is $q $+ t[2]>0:
   k=t[2]
   c=1
  $J $8(t,x):
   k=0
   c=t
  $(:
   $! $#
  cs[k]=$c(cs.get(k,0),c)
  if k>mx:
   mx=k
 $![cs.get(k,0)$) k in $*(mx+1)]
$, fromcoeffs(cs,x):
 $! $6([$9(cs[k],pw(x,k))$) k in $*($3(cs))])
$, numer_denom(e):
 if $&(e,'*'):
  nu=[]
  de=[]
  $) f in e[1:]:
   if isq(f):
    nu.$%(f[1])
    de.$%(f[2])
   $J $&(f,'^')$+ $@(f[2])$+ $a(f[2])<0:
    de.$%(pw(f[1],nneg(f[2])))
   $(:
    nu.$%(f)
  $! $E(nu),$E(de)
 if isq(e):
  $! e[1],e[2]
 if $&(e,'^')$+ $@(e[2])$+ $a(e[2])<0:
  $! 1,pw(e[1],nneg(e[2]))
 $! e,1
''')
_x(r'''OPT={'uni':$F,'digits':10}
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
USYM={'pi':'\u03c0','$]':'\u221e','theta':'\u03b8'}
REL={'=':'=','<':'<','>':'>','<=':'\u2264','>=':'\u2265','/=':'\u2260'}
PRIO='xyztuvwsrqpnmlkjhgfdcba'
$, fmt(e):
 $! pr(e,$2)[0]
$, ffloat(x):
 if x!=x:
  $! '$L'
 if x==$C('$]'):
  $! USYM['$]']if OPT['uni']$( '$]'
 if x==$C('-$]'):
  $! '-'+(USYM['$]']if OPT['uni']$( '$]')
 if x==0:
  $! '0.'
 d=OPT['digits']
 s=('%.'+$u(d)+'g')%x
 m=s
 ex=''
 if 'e' in s:
  m,ex=s.split('e')
  ex=$q(ex)
  ex='E'+$u(ex)
 if '.' in m:
  m=m.rstrip('0')
 $(:
  m=m+'.'
 $! m+ex
$, fnum(x):
 t=$/(x)
 if t is $q:
  $! $u(x),(P_ATOM if x>=0 $( P_NEG)
 if t is $C:
  s=ffloat(x)
  $! s,(P_ATOM if $. s.$r('-')$( P_NEG)
 s=$u(x[1])+'/'+$u(x[2])
 $! s,(P_PROD if x[1]>0 $( P_NEG)
$, psym(e):
 if OPT['uni']$+ e in USYM:
  $! USYM[e]
 $! e
$, paren(s,p,need):
 if p<need:
  $! '('+s+')'
 $! s
$, pr(e,keep):
 t=$/(e)
 if t is $q or t is $C:
  $! fnum(e)
 if t is $u:
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
  $! pr(e[1],$F)
 keep=$2
 if h=='$G':
  $! '{'+','.join([pr(a,keep)[0]$) a in e[1:]])+'}',P_ATOM
 if h=='mat' $+ $3(e)==2:
  $! '['+','.join([pr(a,keep)[0]$) a in e[1][1:]])+']',P_ATOM
 if h=='mat':
  $j=[]
  $) r in e[1:]:
   $j.$%('['+','.join([pr(a,keep)[0]$) a in r[1:]])+']')
  $! '['+''.join($j)+']',P_ATOM
 if h=='$u':
  $! '"'+e[1]+'"',P_ATOM
 if h in REL:
  op=REL[h]if OPT['uni']$( h
  a=pr(e[1],keep)
  b=pr(e[2],keep)
  $! paren(a[0],a[1],P_SUM)+op+paren(b[0],b[1],P_SUM),P_REL
 if h=='$+' $+ $3(e)==3 $+ head(e[1])in('<','<=')$+ head(e[2])in('<','<=')$+ e[1][2]==e[2][1]:
  op1=REL[e[1][0]]if OPT['uni']$( e[1][0]
  op2=REL[e[2][0]]if OPT['uni']$( e[2][0]
  $! pr(e[1][1],$2)[0]+op1+pr(e[1][2],$2)[0]+op2+pr(e[2][2],$2)[0],P_REL
 if h=='$+' or h=='or':
  p=P_AND if h=='$+' $( P_OR
  ss=[]
  $) a in e[1:]:
   s,q=pr(a,keep)
   ss.$%(paren(s,q,p+1))
  $!(' '+h+' ').join(ss),p
 if h=='$.':
  s,q=pr(e[1],keep)
  $! '$. '+paren(s,q,P_NOT+1),P_NOT
 if h=='$I':
  $! '|'+pr(e[1],keep)[0]+'|',P_ATOM
 if h=='fact':
  s,q=pr(e[1],keep)
  $! paren(s,q,P_ATOM)+'!',P_POST
 if h=='log':
  if $3(e)==2 or e[2]==10:
   $! 'log10('+pr(e[1],keep)[0]+')',P_ATOM
  $! 'log('+pr(e[1],keep)[0]+','+pr(e[2],keep)[0]+')',P_ATOM
 if h=='call':
  $! e[1]+'('+','.join([pr(a,keep)[0]$) a in e[2:]])+')',P_ATOM
 if h=='prime':
  $! e[1]+"'"*e[2],P_ATOM
 if h=='$l':
  nm='\u222b' if OPT['uni']$( '$l'
  $! nm+'('+','.join([pr(a,keep)[0]$) a in e[1:]])+')',P_ATOM
 if h=='sumseq':
  nm='\u03a3' if OPT['uni']$( 'sumseq'
  $! nm+'('+','.join([pr(a,keep)[0]$) a in e[1:]])+')',P_ATOM
 if h=='prodseq':
  nm='\u03a0' if OPT['uni']$( 'prodseq'
  $! nm+'('+','.join([pr(a,keep)[0]$) a in e[1:]])+')',P_ATOM
 if h=='$T' or h=='root':
  pass
 h=TINAME.get(h,h)
 $! h+'('+','.join([pr(a,keep)[0]$) a in e[1:]])+')',P_ATOM
TINAME={'ncr':'nCr','npr':'nPr'}
MAINV='xyzt'
$, varprio(v):
 i=MAINV.find(v)if $3(v)==1 $(-1
 if i<0:
  $!(100,v)
 $!(i,v)
$, facprio(v):
 i=MAINV.find(v)if $3(v)==1 $(-1
 if i<0:
  $!(0,v)
 $!(1,$u(i))
$, termdegs(t,d):
 c,r=$V(t)
 fs=r[1:]if $&(r,'*')$((r,)
 $) f in fs:
  if $/(f)is $u $+ f $. in SPECIAL:
   d[f]=d.get(f,0)+1
  $J $&(f,'^')$+ $/(f[1])is $u $+ f[1]$. in SPECIAL $+ $@(f[2]):
   d[f[1]]=d.get(f[1],0)+tofl(f[2])
  $J $&(f,'^')$+ $@(f[2]):
   $) v in ${(f[1]):
    d[v]=d.get(v,0)+tofl(f[2])*0.001
  $J $. $@(f)$+ $/(f)is $. $u:
   $) v in ${(f):
    d[v]=d.get(v,0)+0.0001
$, sumkeys($N):
 vs=[]
 degs=[]
 $) t in $N:
  d={}
  termdegs(t,d)
  degs.$%(d)
  $) v in d:
   if v $. in vs:
    vs.$%(v)
 vs.sort(key=varprio)
 mv=[v $) v in vs if varprio(v)[0]<100]
 ov=[v $) v in vs if varprio(v)[0]>=100]
 keys=[]
 $) k in $*($3($N)):
  t=$N[k]
  d=degs[k]
  if $@(t):
   keys.$%((2,(),0,0,(),''))
  $J $. d:
   cat=3 if has(t,'i')$( 1
   keys.$%((cat,(),0,1 if isneg(t)$( 0,(),okey($V(t)[1])))
  $(:
   keys.$%((0,$1([-d.get(v,0)$) v in mv]),-sum([d.get(v,0)$) v in ov]),
 1 if isneg(t)$( 0,$1([-d.get(v,0)$) v in ov]),okey($V(t)[1])))
 $! keys
$, pr_sum(e,keep):
 $N=$G(e[1:])
 if $. keep:
  ks=sumkeys($N)
  idx=$G($*($3($N)))
  idx.sort(key=$4 i:ks[i])
  $N=[$N[i]$) i in idx]
 $?=''
 first=$F
 $) t in $N:
  s,p=pr(t,$2)
  if p<P_SUM+1 $+ $. s.$r('-')$+ p<=P_SUM:
   s='('+s+')'
  if first:
   $?=s
   first=$2
  $J s.$r('-'):
   $?+=s
  $(:
   $?+='+'+s
 $! $?,P_SUM
$, fackey(f):
 if f=='pi' or f=='e' or isrrad(f)or $@(f):
  $!(0,(0,''),okey(f))
 if f=='i':
  $!(3,(0,''),'')
 if $/(f)is $u:
  $!(1,facprio(f),'')
 if $&(f,'^')$+ $/(f[1])is $u:
  if f[1]=='e':
   $!(2,(0,''),okey(f))
  $!(1,facprio(f[1]),okey(f))
 if $&(f,'+')or($&(f,'^')$+ $&(f[1],'+')):
  $!(4,(0,''),okey(f))
 $!(2,(0,''),okey(f))
$, pr_factor(f,keep,first):
 s,p=pr(f,keep)
 if p<P_PROD or(p==P_PROD $+ $. first)or(s.$r('-')$+ $. first):
  $! '('+s+')'
 $! s
''')
_x(r'''$, pr_prod(e,keep):
 fs=$G(e[1:])
 coef=1
 if fs $+ $@(fs[0])$+ $. keep:
  coef=fs[0]
  fs=fs[1:]
 num=[]
 den=[]
 $) f in fs:
  if $&(f,'^')$+ $@(f[2])$+ $a(f[2])<0:
   ex=nneg(f[2])
   den.$%(f[1]if ex==1 $(('^',f[1],ex))
  $J isq(f)$+ keep:
   num.$%(f[1])
   den.$%(f[2])
  $(:
   num.$%(f)
 if $. keep:
  num.sort(key=fackey)
  den.sort(key=fackey)
 sign=''
 if keep $+ num $+ $@(num[0])$+ $a(num[0])<0:
  sign='-'
  if num[0]==-1:
   num=num[1:]
  $(:
   num[0]=nneg(num[0])
 cn=coef
 cd=1
 if $@(coef):
  if $a(coef)<0:
   sign='-'
   coef=nneg(coef)
  if isq(coef):
   cn=coef[1]
   cd=coef[2]
  $(:
   cn=coef
 if keep:
  num=[f $) f in num if f!=1]or[1]
 if sign $+ den $+ $. keep:
  sums=[k $) k in $*($3(num))if $&(num[k],'+')]
  dsums=[k $) k in $*($3(den))if $&(den[k],'+')]
  if $3(sums)==1 $+ any([isneg(t)$) t in num[sums[0]][1:]]):
   num=$G(num)
   num[sums[0]]=$9(-1,num[sums[0]])
   sign=''
  $J $3(dsums)==1 $+ $. sums $+ $3(den[dsums[0]])==3 $+ $5(den[dsums[0]])$+ any([isneg(t)$) t in den[dsums[0]][1:]]):
   den=$G(den)
   den[dsums[0]]=$9(-1,den[dsums[0]])
   sign=''
 parts=[]
 if cn!=1 or $/(cn)is $C:
  parts.$%(fnum(cn)[0])
 $) f in num:
  parts.$%(pr_factor(f,$2,$. parts))
 if $. parts:
  parts.$%('1')
 ns='*'.join(parts)
 if cd!=1:
  den.insert(0,cd)
 if $. den:
  if sign $+ $3(num)==1 $+ cn==1 $+ pr(num[0],$2)[1]<=P_SUM:
   $! sign+'('+pr(num[0],$2)[0]+')',P_NEG
  $! sign+ns,(P_NEG if sign $( P_PROD)
 if $3(parts)==1 $+ $3(num)==1 $+ cn==1:
  s,p=pr(num[0],$2)
  ns=paren(s,p,P_PROD+1)if p<P_PROD $( s
  if s.$r('-'):
   ns='('+s+')'
 dparts=[]
 $) f in den:
  dparts.$%(pr_factor(f,$2,$. dparts))
 ds='*'.join(dparts)
 if $3(den)>1:
  ds='('+ds+')'
 $(:
  s,p=pr(den[0],$2)
  if p<=P_PROD or s.$r('-'):
   ds='('+s+')'
 $! sign+ns+'/'+ds,(P_NEG if sign $( P_PROD)
$, pr_pow(e,keep):
 b=e[1]
 x=e[2]
 if $@(x)$+ $a(x)<0 $+ $. keep:
  ex=nneg(x)
  d=b if ex==1 $(('^',b,ex)
  s,p=pr(d,$2)
  if p<=P_PROD or s.$r('-'):
   s='('+s+')'
  $! '1/'+s,P_PROD
 if x==$|:
  s,p=pr(b,$2)
  if OPT['uni']:
   if($/(b)is $q $+ b>=0)or($/(b)is $u):
    $! '\u221a'+s,P_POW
   $! '\u221a('+s+')',P_ATOM
  $! '$T('+s+')',P_ATOM
 bs,bp=pr(b,$2)
 if bp<=P_POW or bs.$r('-')or $&(b,'fact'):
  bs='('+bs+')'
 xs,xp=pr(x,$2)
 if $.(($/(x)is $q $+ x>=0)or($/(x)is $u)):
  xs='('+xs+')'
 $! bs+'^'+xs,P_POW
$, fmt_top(e):
 if $&(e,'mat')$+ $3(e)>2:
  $j=[]
  $) r in e[1:]:
   $j.$%('['+','.join([fmt(a)$) a in r[1:]])+']')
  if sum([$3(r)$) r in $j])>28:
   $! '['+('\n '.join($j))+']'
  $! '['+''.join($j)+']'
 if $&(e,'$u'):
  $! e[1]
 $! fmt(e)
''')
_x(r'''REPL=(
 ('**','^'),('==','='),('!=','/='),
 ('sin\u207b\u00b9','$w'),('cos\u207b\u00b9','arccos'),('tan\u207b\u00b9','$t'),
 ('\u2212','-'),('\u2013','-'),('\u00d7','*'),('\u00b7','*'),
 ('\u2022','*'),('\u22c5','*'),('\u00f7','/'),('\u2264','<='),
 ('\u2265','>='),('\u2260','/='),('\u2192','->'),('\u21d2','=>'),
 ('\u21d4','<=>'),('\u207b\u00b9','^(-1)'),('\u00b2','^2'),
 ('\u00b3','^3'),('\u03c0',' pi '),('\u221e',' $] '),
 ('\u212f',' e '),('\u2148',' i '),('\u03b8','theta'),
 ('\u222b',' $l'),('\u03a3',' sumseq'),('\u2211',' sumseq'),
 ('\u03a0',' prodseq'),('\u220f',' prodseq'),('\u1d07','E'),
 ('\u2032',"'"),('\u2033',"''"),('@i',' i '),('@e',' e '),
 ('@>','\u25ba'),('@d','\u00b0'),('@t','\u1d40'),('\u2044','/'),
 ('infinity','$]'),('\u03b1','alpha'),('\u03b2','beta'),
 ('\u03bb','$4'),('\u03bc','mu'),('\u03c3','sigma'),
 ('\u0394','delta'),
 )
OPS=('<=>','=>','->','=:',':=','<=','>=','/=','<>','.^','.*',
 './','.+','.-','>>','+','-','*','/','^','(',')','{','}',
 '[',']',',',';','=','<','>','|','!','%','&','\u00b0',
 '\u2220','\u25ba','\u221a',"'",'\u1d40')
KEYW=('$+','or','xor','$.','nor','nand')
NOTLETTER='\u221a\u00b0\u2220\u25ba\u1d40'
$, normalize(s):
 $) a,b in REPL:
  if a in s:
   s=s.replace(a,b)
 $! s
$, isletter(c):
 if c=='_':
  $! $F
 o=ord(c)
 if o>127:
  $! c $. in NOTLETTER
 $!('a'<=c<='z')or('A'<=c<='Z')
$, isdig(c):
 $! '0'<=c<='9'
$, tokenize(s):
 s=normalize(s)
 toks=[]
 i=0
 n=$3(s)
 $H i<n:
  c=s[i]
  if c==' ' or c=='\t':
   i+=1
   $7
  if c=='0' $+ i+2<n $+ s[i+1]in 'bBhH':
   base=2 if s[i+1]in 'bB' $( 16
   j=i+2
   dg='01' if base==2 $( '0123456789abcdefABCDEF'
   $H j<n $+ s[j]in dg:
    j+=1
   if j>i+2:
    toks.$%(('num',$q(s[i+2:j],base)))
    i=j
    $7
  if isdig(c)or(c=='.' $+ i+1<n $+ isdig(s[i+1])):
   j=i
   $H j<n $+ isdig(s[j]):
    j+=1
   isf=$2
   if j<n $+ s[j]=='.' $+ $.(j+1<n $+ s[j+1]in '^*/+-' $+ $. isdig(s[j+1])):
    isf=$F
    j+=1
    $H j<n $+ isdig(s[j]):
     j+=1
   if j<n $+(s[j]=='E' or(s[j]=='e' $+ j+1<n $+ isdig(s[j+1]))):
    k=j+1
    if k<n $+ s[k]in '+-':
     k+=1
    if k<n $+ isdig(s[k]):
     isf=$F
     j=k
     $H j<n $+ isdig(s[j]):
      j+=1
   txt=s[i:j]
   if isf:
    toks.$%(('num',$C(txt)))
   $(:
    toks.$%(('num',$q(txt)))
   i=j
   $7
  if isletter(c):
   j=i
   $H j<n $+(isletter(s[j])or isdig(s[j])):
    j+=1
   $D=s[i:j].lower()
   toks.$%(('id',$D))
   i=j
   k=0
   $H i<n $+ s[i]=="'":
    k+=1
    i+=1
   if k:
    toks.$%(('prime',k))
   $7
  if c=='"':
   j=s.find('"',i+1)
   if j<0:
    $n $M('Missing "')
   toks.$%(('$u',s[i+1:j]))
   i=j+1
   $7
  $) op in OPS:
   if s.$r(op,i):
    i+=$3(op)
    if op=='<>':
     op='/='
    if op=='>>':
     op='\u25ba'
    toks.$%(('op',op))
    $X
  $(:
   $n $M('Invalid character: '+c)
 toks.$%(('end',$#))
 $! toks
''')
_x(r'''class Parser:
 $, __init__($:,toks,isfunc):
  $:.t=toks
  $:.i=0
  $:.isfunc=isfunc
 $, peek($:):
  $! $:.t[$:.i]
 $, nxt($:):
  tk=$:.t[$:.i]
  $:.i+=1
  $! tk
 $, isop($:,op):
  tk=$:.t[$:.i]
  $! tk[0]=='op' $+ tk[1]==op
 $, isid($:,$D):
  tk=$:.t[$:.i]
  $! tk[0]=='id' $+ tk[1]==$D
 $, expect($:,op):
  if $. $:.isop(op):
   tk=$:.peek()
   $n $M('Missing '+op)
  $:.i+=1
 $, top($:):
  e=$:.store()
  $H $:.isop('\u25ba'):
   $:.nxt()
   tk=$:.nxt()
   if tk[0]!='id':
    $n $M('Syntax error after conversion')
   $R=[]
   if $:.isop('('):
    $:.nxt()
    $R=$:.$R(')')
   e=('conv',e,tk[1])+$1($R)
  if $:.peek()[0]!='end':
   tk=$:.peek()
   $n $M('Syntax error near '+$u(tk[1])if tk[1]is $. $# $( 'Syntax error')
  $! e
 $, store($:):
  if $:.isid('define'):
   $:.nxt()
   lhs=$:.sum()
   if $. $:.isop('='):
    $n $M('Define needs =')
   $:.nxt()
   rhs=$:.wth()
   $!('define',lhs,rhs)
  e=$:.wth()
  if $:.isop('->')or $:.isop('=:'):
   $:.nxt()
   tgt=$:.wth()
   $!('store',e,tgt)
  if $:.isop(':='):
   $:.nxt()
   rhs=$:.wth()
   $!('define',e,rhs)
  $! e
 $, wth($:):
  e=$:.iff()
  $H $:.isop('|'):
   $:.nxt()
   c=$:.iff()
   e=('|',e,c)
  $! e
 $, iff($:):
  e=$:.imp()
  $H $:.isop('<=>'):
   $:.nxt()
   e=('<=>',e,$:.imp())
  $! e
 $, imp($:):
  e=$:.xor()
  $H $:.isop('=>'):
   $:.nxt()
   e=('=>',e,$:.xor())
  $! e
 $, xor($:):
  e=$:.lor()
  $H $:.isid('xor')or $:.isid('nor')or $:.isid('nand'):
   op=$:.nxt()[1]
   e=(op,e,$:.lor())
  $! e
 $, lor($:):
  e=$:.land()
  $H $:.isid('or'):
   $:.nxt()
   e=('or',e,$:.land())
  $! e
 $, land($:):
  e=$:.lnot()
  $H $:.isid('$+'):
   $:.nxt()
   e=('$+',e,$:.lnot())
  $! e
 $, lnot($:):
  if $:.isid('$.'):
   $:.nxt()
   $!('$.',$:.lnot())
  $! $:.rel()
 $, rel($:):
  a=$:.sum()
  tk=$:.peek()
  if tk[0]=='op' $+ tk[1]in('=','/=','<','>','<=','>='):
   $:.nxt()
   b=$:.sum()
   r=(tk[1],a,b)
   tk2=$:.peek()
   if tk2[0]=='op' $+ tk2[1]in('<','>','<=','>='):
    $:.nxt()
    c=$:.sum()
    r=('$+',r,(tk2[1],b,c))
   $! r
  $! a
 $, sum($:):
  a=$:.prod()
  $H $F:
   tk=$:.peek()
   if tk[0]=='op' $+ tk[1]in('+','-','.+','.-','&'):
    $:.nxt()
    b=$:.prod()
    op=tk[1]
    if op=='.+':
     op='+'
    $J op=='.-':
     op='-'
    a=(op,a,b)
   $(:
    $! a
 $, startsprimary($:):
  tk=$:.peek()
  if tk[0]=='num' or tk[0]=='$u':
   $! $F
  if tk[0]=='id':
   $! tk[1]$. in KEYW
  if tk[0]=='op':
   $! tk[1]in('(','{','\u221a')
  $! $2
 $, prod($:):
  a=$:.unary()
  $H $F:
   tk=$:.peek()
   if tk[0]=='op' $+ tk[1]in('*','/','.*','./'):
    $:.nxt()
    b=$:.unary()
    op=tk[1]
    a=(op,a,b)
   $J $:.startsprimary():
    b=$:.pw()
    a=('*',a,b)
   $(:
    $! a
 $, unary($:):
  if $:.isop('-'):
   $:.nxt()
   $!('$o',$:.unary())
  if $:.isop('+'):
   $:.nxt()
   $! $:.unary()
  $! $:.pw()
 $, pw($:):
  b=$:.post()
  if $:.isop('^')or $:.isop('.^'):
   op=$:.nxt()[1]
   if $:.isop('\u1d40')or $:.isid('t')$+ $2:
    pass
   x=$:.unary()
   $!('^' if op=='^' $( '.^',b,x)
  $! b
 $, post($:):
  a=$:.primary()
  $H $F:
   if $:.isop('!'):
    $:.nxt()
    a=('!',a)
   $J $:.isop('%'):
    $:.nxt()
    a=('%',a)
   $J $:.isop('\u00b0'):
    $:.nxt()
    a=('deg',a)
   $J $:.isop('\u1d40'):
    $:.nxt()
    a=('call','transpose',a)
   $J $:.isop('['):
    $:.nxt()
    idx=$:.$R(']')
    a=('index',a)+$1(idx)
   $(:
    $! a
 $, $R($:,close):
  $?=[]
  if $:.isop(close):
   $:.nxt()
   $! $?
  $H $F:
   $?.$%($:.store_in())
   if $:.isop(','):
    $:.nxt()
    $7
   $:.expect(close)
   $! $?
 $, store_in($:):
  e=$:.wth()
  $! e
 $, primary($:):
  tk=$:.nxt()
  k=tk[0]
  if k=='num':
   $! tk[1]
  if k=='$u':
   $!('$u',tk[1])
  if k=='id':
   $D=tk[1]
   if $D in KEYW:
    $n $M('Syntax error: '+$D)
   if $:.peek()[0]=='prime':
    n=$:.nxt()[1]
    if $:.isop('('):
     $:.nxt()
     a=$:.$R(')')
     $!('primecall',$D,n)+$1(a)
    $!('prime',$D,n)
   if $:.isop('(')$+($:.isfunc($D)or($3($D)>1 $+ $D $. in('pi','$]','$L','theta'))):
    $:.nxt()
    a=$:.$R(')')
    $!('call',$D)+$1(a)
   $! $D
  if k=='op':
   op=tk[1]
   if op=='(':
    e=$:.store_in()
    if $:.isop('\u2220'):
     $:.nxt()
     th=$:.store_in()
     $:.expect(')')
     $!('polar',e,th)
    $:.expect(')')
    $! e
   if op=='{':
    $!('$G',)+$1($:.$R('}'))
   if op=='[':
    $! $:.matrix()
   if op=='\u221a':
    $!('call','$T',$:.post())
   if op=='-':
    $!('$o',$:.pw())
  if k=='end':
   $n $M('Incomplete expression')
  $n $M('Syntax error near '+$u(tk[1]))
 $, matrix($:):
  $j=[]
  if $:.isop('['):
   $H $:.isop('['):
    $:.nxt()
    $j.$%(('$G',)+$1($:.$R(']')))
    if $:.isop(','):
     $:.nxt()
   $:.expect(']')
  $(:
   row=[]
   $H $F:
    if $:.isop(']'):
     $:.nxt()
     $X
    row.$%($:.store_in())
    if $:.isop(','):
     $:.nxt()
    $J $:.isop(';'):
     $:.nxt()
     $j.$%(('$G',)+$1(row))
     row=[]
    $J $:.isop(']'):
     $7
    $(:
     $n $M('Missing ]')
   $j.$%(('$G',)+$1(row))
  n=$3($j[0])
  $) r in $j:
   if $3(r)!=n:
    $n $M('Dimension error')
  $!('mat',)+$1($j)
''')
_x(r'''$, parse(s,isfunc):
 toks=tokenize(s)
 if toks[0][0]=='end':
  $n $M('Empty input')
 $! Parser(toks,isfunc).top()
''')
_x(r'''import cmath
$, $z(c,nv):
 if c==0:
  $!{}
 $!{(0,)*nv:c}
$, p_add(A,B):
 C=dict(A)
 $) m in B:
  v=C.get(m,0)+B[m]
  if v:
   C[m]=v
  $J m in C:
   del C[m]
 $! C
$, p_neg(A):
 $! dict([(m,-A[m])$) m in A])
$, p_sub(A,B):
 $! p_add(A,p_neg(B))
$, madd(a,b):
 $! $1([a[i]+b[i]$) i in $*($3(a))])
$, p_mul(A,B):
 C={}
 $) a in A:
  ca=A[a]
  $) b in B:
   m=madd(a,b)
   v=C.get(m,0)+ca*B[b]
   if v:
    C[m]=v
   $J m in C:
    del C[m]
 $! C
$, p_scale(A,c):
 if c==0:
  $!{}
 $! dict([(m,A[m]*c)$) m in A])
$, p_pow(A,n):
 nv=$3(next(iter(A)))if A $( 0
 R=$z(1,nv)
 $H n>0:
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
 if $. A:
  $! $F
 $) m in A:
  if sum(m):
   $! $2
 $! $F
$, p_cval(A):
 $) m in A:
  $! A[m]
 $! 0
$, p_vars(A,nv):
 $![k $) k in $*(nv)if p_deg(A,k)>0]
$, p_mono(nv,k,d):
 m=[0]*nv
 m[k]=d
 $! $1(m)
$, $K(A,B):
 if $. B:
  err("Division by zero")
 lmB=max(B)
 lcB=B[lmB]
 nv=$3(lmB)
 Qt={}
 R=dict(A)
 cnt=0
 $H R:
  cnt+=1
  if cnt>5000:
   $! $#
  lmR=max(R)
  d=[]
  $) i in $*(nv):
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
  $) m in B:
   mm=madd(m,d)
   v=R.get(mm,0)-q*B[m]
   if v:
    R[mm]=v
   $J mm in R:
    del R[mm]
 $! Qt
$, p_icont(A):
 g=0
 $) m in A:
  g=igcd(g,A[m])
  if g==1:
   $X
 $! g
$, p_normsign(A):
 if A $+ A[max(A)]<0:
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
  if p_isconst(g)$+ $I(p_cval(g))==1:
   $! $z(1,nv)
 $! p_normsign(g)
EVP=(3,5,7,11,13,17,19,23,29,31,37,41)
$, p_at(A,pt):
 s=0
 $) m in A:
  t=A[m]
  $) i in $*($3(m)):
   if m[i]:
    t*=pt[i]**m[i]
  s+=t
 $! s
$, p_gcd(A,B,nv):
 if $. A:
  $! p_normsign(B)
 if $. B:
  $! p_normsign(A)
 if nv $+($3(A)>2 or $3(B)>2):
  c=igcd(p_icont(A),p_icont(B))
  ok=$F
  $) sh in(0,1):
   pt=[EVP[(i+sh*5)%$3(EVP)]*(1+sh)+i $) i in $*(nv)]
   g=igcd(p_at(A,pt),p_at(B,pt))
   if g!=c:
    ok=$2
    $X
  if ok:
   $! $z(c,nv)
 $! p_gcd0(A,B,nv)
$, p_gcd0(A,B,nv):
 if $. A:
  $! p_normsign(B)
 if $. B:
  $! p_normsign(A)
 vs=[]
 $) k in $*(nv):
  if p_deg(A,k)>0 or p_deg(B,k)>0:
   vs.$%(k)
 if $. vs:
  $! $z(igcd(p_cval(A),p_cval(B)),nv)
 k=vs[0]
 if p_deg(A,k)==0 or p_deg(B,k)==0:
  if p_deg(A,k)==0:
   $! p_gcd(A,p_cont(B,k,nv),nv)
  $! p_gcd(p_cont(A,k,nv),B,nv)
 cA=p_cont(A,k,nv)
 cB=p_cont(B,k,nv)
 c=p_gcd(cA,cB,nv)
 pA=$K(A,cA)
 pB=$K(B,cB)
 if p_deg(pA,k)<p_deg(pB,k):
  pA,pB=pB,pA
 $H pB $+ p_deg(pB,k)>0:
  r=prem(pA,pB,k,nv)
  pA=pB
  if $. r:
   pB={}
   $X
  pB=$K(r,p_cont(r,k,nv))
 if pB:
  g=$z(1,nv)
 $(:
  g=$K(pA,p_cont(pA,k,nv))
 $! p_normsign(p_mul(c,g))
$, prem(A,B,k,nv):
 dB=p_deg(B,k)
 lcB=p_lc(B,k)
 R=A
 $H R $+ p_deg(R,k)>=dB:
  dR=p_deg(R,k)
  lcR=p_lc(R,k)
  t=p_mul(lcR,{p_mono(nv,k,dR-dB):1})
  R=p_sub(p_mul(R,lcB),p_mul(t,B))
 $! R
$, p_sqfree(P,k,nv):
 dP=p_diff(P,k)
 a=p_gcd(P,dP,nv)
 b=$K(P,a)
 c=$K(dP,a)
 d=p_sub(c,p_diff(b,k))
 res=[]
 i=1
 $H p_deg(b,k)>0:
  a=p_gcd(b,d,nv)
  if p_deg(a,k)>0:
   res.$%((a,i))
  b=$K(b,a)
  c=$K(d,a)
  d=p_sub(c,p_diff(b,k))
  i+=1
  if i>200:
   $X
 $! res
$, p_sqrt(D):
 if $. D:
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
 hm=$1([x//2 $) x in lm])
 S={hm:r}
 nv=$3(lm)
 $) _ in $*($3(D)+3):
  R=p_sub(D,p_mul(S,S))
  if $. R:
   $! S
  lmR=max(R)
  lmS=max(S)
  m=[]
  $) i in $*(nv):
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
 if $/(x)is $q:
  $! b,x
 if isq(x):
  $! pw(b,Q(1,x[2])),x[1]
 c,r=$V(x)
 if $/(c)is $q $+ c!=1:
  $! pw(b,r),c
 if isq(c):
  $! pw(b,$9(Q(1,c[2]),r)),c[1]
 $! e,1
$, kernels(e,ks):
 t=$/(e)
 if t is $q or t is $C:
  $!
 if t is $u:
  if e $. in ks:
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
  if $/(e[2])is $q:
   kernels(e[1],ks)
   $!
  k,n=splitpow(e)
  if k==e or $. $&(k,'^')or $F:
   if $&(k,'^')$+ $/(k[2])is $q:
    kernels(k,ks)
    $!
   if k $. in ks:
    ks.$%(k)
  $!
 if e $. in ks:
  ks.$%(e)
$, sortkernels(ks):
 ks.sort(key=$4 k:varprio(k)if $/(k)is $u $((200,okey(k)))
 $! ks
''')
_x(r'''$, ratform(e,ks):
 nv=$3(ks)
 t=$/(e)
 if t is $q:
  $! $z(e,nv),$z(1,nv)
 if t is $C:
  $! $#
 if t is $1 $+ e[0]=='Q':
  $! $z(e[1],nv),$z(e[2],nv)
 if e in ks:
  $!{p_mono(nv,ks.index(e),1):1},$z(1,nv)
 h=e[0]
 if h=='+':
  N={}
  D=$z(1,nv)
  $) a in e[1:]:
   r=ratform(a,ks)
   if r is $#:
    $! $#
   n,d=r
   if D==d:
    N=p_add(N,n)
   $(:
    g=p_gcd(D,d,nv)
    d1=$K(d,g)
    D1=$K(D,g)
    N=p_add(p_mul(N,d1),p_mul(n,D1))
    D=p_mul(D,d1)
  $! N,D
 if h=='*':
  N=$z(1,nv)
  D=$z(1,nv)
  $) a in e[1:]:
   r=ratform(a,ks)
   if r is $#:
    $! $#
   N=p_mul(N,r[0])
   D=p_mul(D,r[1])
  $! N,D
 if h=='^':
  if $/(e[2])is $q:
   b=e[1]
   n=e[2]
  $(:
   b,n=splitpow(e)
  if b in ks $+ b!=e or(b==e):
   if b $. in ks:
    $! $#
   k=ks.index(b)
   if n>=0:
    $!{p_mono(nv,k,n):1},$z(1,nv)
   $! $z(1,nv),{p_mono(nv,k,-n):1}
  r=ratform(b,ks)
  if r is $#:
   $! $#
  if n>=0:
   $! p_pow(r[0],n),p_pow(r[1],n)
  $! p_pow(r[1],-n),p_pow(r[0],-n)
 $! $#
$, p2e(P,ks):
 $N=[]
 $) m in P:
  fs=[P[m]]
  $) i in $*($3(m)):
   if m[i]:
    fs.$%(pw(ks[i],m[i]))
  $N.$%($E(fs))
 $! $6($N)
$, cancel_pair(N,D,nv):
 g=p_gcd(N,D,nv)
 if $. p_isconst(g)or p_cval(g)!=1:
  N=$K(N,g)
  D=$K(D,g)
 if D $+ D[max(D)]<0:
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
 N,D=cancel_pair(r[0],r[1],$3(ks))
 $! N,D,ks
$, comdenom(e):
 if $&(e,'$G')or $&(e,'mat'):
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
 if $&(num,'+')$+ $&(den,'+')or den==1 or $@(den):
  $! $Y(num,den)
 $! $Y(num,den)
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
 $! $/(e)is $1 $+ e[0]in('=','<','>','<=','>=','/=')
$, hasdenom(e):
 if $&(e,'^')$+ $@(e[2])$+ $a(e[2])<0 $+ $. $5(e[1]):
  $! $F
 if $/(e)is $1 $+ e[0]in('+','*'):
  $) a in e[1:]:
   if hasdenom(a):
    $! $F
 $! $2
$, $-(e):
 t=$/(e)
 if t is $. $1 or e[0]=='Q' or e[0]=='$u':
  $! e
 h=e[0]
 $R=[$-(a)$) a in e[1:]]
 e2=simp((h,)+$1($R))if h!='hold' $( e
 if $. $&(e2,'*'):
  $! e2
 hasden=$2
 hassum=$2
 $) f in e2[1:]:
  if $&(f,'^')$+ $@(f[2])$+ $a(f[2])<0 $+ $. $5(f[1]):
   if $&(f[1],'+')or($&(f[1],'^')$+ $&(f[1][1],'+')):
    hasden=$F
  if $&(f,'+')or($&(f,'^')$+ $&(f[1],'+')):
   hassum=$F
 if $.(hasden $+ hassum)$+ $. hasden:
  $! e2
 if $`(e2):
  $! e2
 ks=[]
 kernels(e2,ks)
 sortkernels(ks)
 nv=$3(ks)
 if nv==0 or nv>6:
  $! e2
 nums=[]
 dens=[]
 $) f in e2[1:]:
  if $&(f,'^')$+ $@(f[2])$+ $a(f[2])<0:
   dens.$%(pw(f[1],nneg(f[2])))
  $(:
   nums.$%(f)
 num=$E(nums)
 den=$E(dens)
 rn=ratform(num,ks)
 rd=ratform(den,ks)
 if rn is $# or rd is $#:
  $! e2
 if $3(rn[0])*$3(rd[1])>400 or $3(rn[1])*$3(rd[0])>400:
  $! e2
 N=p_mul(rn[0],rd[1])
 D=p_mul(rn[1],rd[0])
 if $3(N)>80 or $3(D)>80 or p_tdeg(N)>30 or p_tdeg(D)>30:
  $! e2
 g=p_gcd(N,D,nv)
 if p_isconst(g):
  $! e2
 N=$K(N,g)
 D=$K(D,g)
 if D $+ D[max(D)]<0:
  N=p_neg(N)
  D=p_neg(D)
 $! $Y(p2e(N,ks),p2e(D,ks))
$, u_trim(a):
 a=$G(a)
 $H a $+ a[-1]==0:
  a.pop()
 $! a
$, u_add(a,b):
 n=max($3(a),$3(b))
 $! u_trim([nadd(a[i]if i<$3(a)$( 0,b[i]if i<$3(b)$( 0)$) i in $*(n)])
$, u_neg(a):
 $![nneg(c)$) c in a]
$, u_sub(a,b):
 $! u_add(a,u_neg(b))
$, u_mul(a,b):
 if $. a or $. b:
  $![]
 r=[0]*($3(a)+$3(b)-1)
 $) i in $*($3(a)):
  if a[i]==0:
   $7
  $) j in $*($3(b)):
   r[i+j]=nadd(r[i+j],nmul(a[i],b[j]))
 $! u_trim(r)
$, u_scale(a,c):
 $! u_trim([nmul(x,c)$) x in a])
$, u_divmod(a,b):
 b=u_trim(b)
 if $. b:
  err("Division by zero")
 a=u_trim(a)
 q=[0]*max($3(a)-$3(b)+1,0)
 r=$G(a)
 lb=b[-1]
 $H $3(r)>=$3(b)$+ r:
  c=ndiv(r[-1],lb)
  k=$3(r)-$3(b)
  q[k]=c
  $) j in $*($3(b)):
   r[k+j]=nsub(r[k+j],nmul(c,b[j]))
  r=u_trim(r[:-1])if r[-1]==0 or $F $( r
  r=u_trim(r)
 $! u_trim(q),r
$, u_monic(a):
 if $. a:
  $! a
 $! u_scale(a,ninv(a[-1]))
$, u_egcd(a,b):
 r0,r1=u_trim(a),u_trim(b)
 s0,s1=[1],[]
 t0,t1=[],[1]
 $H r1:
  q,r=u_divmod(r0,r1)
  r0,r1=r1,r
  s0,s1=s1,u_sub(s0,u_mul(q,s1))
  t0,t1=t1,u_sub(t0,u_mul(q,t1))
 if $. r0:
  $! r0,s0,t0
 c=ninv(r0[-1])
 $! u_scale(r0,c),u_scale(s0,c),u_scale(t0,c)
$, u_toexpr(a,x):
 $! $6([$9(a[i],pw(x,i))$) i in $*($3(a))if a[i]!=0])
$, u_from_expr(e,x):
 cs=$^(e,x)
 if cs is $#:
  $! $#
 $) c in cs:
  if $. $m(c):
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
 a=$G(a)
 if $3(a)<$3(b):
  $! $#
 q=[0]*($3(a)-$3(b)+1)
 lb=b[-1]
 $) k in $*($3(a)-$3(b),-1,-1):
  c=a[k+$3(b)-1]
  if c%lb:
   $! $#
  c//=lb
  q[k]=c
  if c:
   $) j in $*($3(b)):
    a[k+j]-=c*b[j]
 $) x in a:
  if x:
   $! $#
 $! q
''')
_x(r'''$, aberth(c):
 c=[$0(tofl(x))if $/(x)is $. $0 $( x $) x in c]
 $H c $+ c[-1]==0:
  c.pop()
 n=$3(c)-1
 if n<1:
  $![]
 zeros=0
 $H $I(c[0])==0:
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
 $) i in $*(n):
  v=$I(a[i])**(1.0/(n-i))
  if v>r:
   r=v
 r=max(r,1e-3)
 z=[r*cmath.exp(1j*(2*$P.pi*k/n+0.4))$) k in $*(n)]
 $) it in $*(600):
  mx=0.0
  $) k in $*(n):
   zk=z[k]
   p=a[n]
   dp=0j
   $) j in $*(n-1,-1,-1):
    dp=dp*zk+p
    p=p*zk+a[j]
   if p==0:
    $7
   ratio=p/dp if dp!=0 $( 1e-3
   s=0j
   $) j in $*(n):
    if j!=k:
     d=zk-z[j]
     if d!=0:
      s+=1/d
   den=1-ratio*s
   w=ratio/den if den!=0 $( ratio
   z[k]=zk-w
   aw=$I(w)
   if aw>mx*(1+$I(zk))or $F:
    mx=max(mx,aw/(1+$I(zk)))
  if mx<1e-15:
   $X
 res=[]
 $) zk in z:
  $) _ in $*(3):
   p=c[n]
   dp=0j
   $) j in $*(n-1,-1,-1):
    dp=dp*zk+p
    p=p*zk+c[j]
   if dp==0:
    $X
   zk=zk-p/dp
  res.$%(zk)
 $! $?+res
$, divisors_int(n,limit=400):
 n=$I(n)
 if n==0:
  $![1]
 fs,$_=factor_int_small(n)
 if $_>1:
  fs.$%(($_,1))
 ds=[1]
 $) p,k in fs:
  nd_=[]
  $) d in ds:
   v=d
   $) _ in $*(k+1):
    nd_.$%(v)
    v*=p
  ds=nd_
  if $3(ds)>limit:
   $! $#
 ds.sort()
 $! ds
$, combos(n,k):
 idx=$G($*(k))
 $H $F:
  yield idx
  i=k-1
  $H i>=0 $+ idx[i]==i+n-k:
   i-=1
  if i<0:
   $!
  idx[i]+=1
  $) j in $*(i+1,k):
   idx[j]=idx[j-1]+1
$, ifactor_sqf(f):
 n=$3(f)-1
 if n<=1:
  $![f]
 res=[]
 $H f[0]==0:
  res.$%([0,1])
  f=f[1:]
 if $3(f)-1<=1:
  $! res+[f]if $3(f)>1 $( res
 roots=aberth(f)
 lcd=divisors_int(f[-1])or[1]
 $_=[]
 $) r in roots:
  found=$2
  if $I(r.imag)<1e-6*(1+$I(r.$Q)):
   $) q in lcd:
    p=$q(round(r.$Q*q))
    if p==0 $+ $I(r.$Q)>0.5/q:
     $7
    g=[-p,q]
    if igcd(p,q)!=1:
     $7
    qq=i_divexact(f,g)
    if qq is $. $#:
     res.$%(g)
     f=qq
     found=$F
     $X
  if $. found:
   $_.$%(r)
 if $3(f)-1<=3:
  if $3(f)>1:
   res.$%(f)
  $! res
 roots=$_
 if $3(roots)!=$3(f)-1:
  roots=aberth(f)
 lcd=divisors_int(f[-1])or[1]
 d=2
 $H d<=($3(f)-1)//2 $+ $3(roots)<=24:
  done=$2
  $) idx in combos($3(roots),d):
   pc=[1+0j]
   $) i in idx:
    r=roots[i]
    nw=[0j]*($3(pc)+1)
    $) j in $*($3(pc)):
     nw[j+1]+=pc[j]
     nw[j]-=pc[j]*r
    pc=nw
   ok=$F
   $) v in pc:
    if $I(v.imag)>1e-6*(1+$I(v.$Q)):
     ok=$2
     $X
   if $. ok:
    $7
   $) q in lcd:
    g=[]
    good=$F
    $) v in pc:
     x=v.$Q*q
     ix=$q(round(x))
     if $I(x-ix)>1e-5*(1+$I(x)):
      good=$2
      $X
     g.$%(ix)
    if $. good:
     $7
    qq=i_divexact(f,g)
    if qq is $. $#:
     res.$%(g)
     f=qq
     roots=[roots[i]$) i in $*($3(roots))if i $. in idx]
     done=$F
     $X
   if done:
    $X
  if $. done:
   d+=1
 if $3(f)>1:
  res.$%(f)
 $! res
$, ufactor(a):
 ints,c=u_toint(u_trim(a))
 if $3(ints)<=1:
  $! nmul(c,ints[0]if ints $( 0),[]
 nv=1
 P=dict([((i,),ints[i])$) i in $*($3(ints))if ints[i]])
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
 $! dict([(p_mono(nv,k,i),f[i])$) i in $*($3(f))if f[i]])
$, mfactor(P,nv):
 if $. P:
  $! 0,[]
 c=p_icont(P)
 if P[max(P)]<0:
  c=-c
 P=p_scale(P,1)if c==1 $( dict([(m,P[m]//c)$) m in P])
 res=[]
 mins=[min([m[k]$) m in P])$) k in $*(nv)]
 $) k in $*(nv):
  if mins[k]>0:
   res.$%(({p_mono(nv,k,1):1},mins[k]))
 if sum(mins):
  mn=$1(mins)
  P=dict([($1([m[i]-mn[i]$) i in $*(nv)]),P[m])$) m in P])
 c2=mfac_rec(P,nv,res,1)
 $! c*c2,res
$, mfac_rec(P,nv,res,mult):
 vs=p_vars(P,nv)
 if $. vs:
  $! p_cval(P)**mult if P $( 0
 if $3(vs)==1:
  k=vs[0]
  fl=[0]*(p_deg(P,k)+1)
  $) m in P:
   fl[m[k]]=P[m]
  cc,fs=ufactor(fl)
  $) g,i in fs:
   res.$%((i2p(g,nv,k),i*mult))
  $! cc**mult if $/(cc)is $q $( nipow(cc,mult)
 vs.sort(key=$4 k:p_deg(P,k))
 k=vs[0]
 cst=1
 C=p_cont(P,k,nv)
 if $. p_isconst(C):
  cst=mfac_rec(C,nv,res,mult)
  P=$K(P,C)
 $J p_cval(C)!=1:
  P=$K(P,C)
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
  $J s!=d:
   $! $2
 $! $F
''')
_x(r'''$, msplit(F,nv,$>):
 vs=p_vars(F,nv)
 if $3(vs)<=1:
  if $. vs:
   $![F]
  k=vs[0]
  fl=[0]*(p_deg(F,k)+1)
  $) m in F:
   fl[m[k]]=F[m]
  cc,fs=ufactor(fl)
  $?=[]
  $) g,i in fs:
   $) _ in $*(i):
    $?.$%(i2p(g,nv,k))
  $! $? if $? $([F]
 if $>>8:
  $![F]
 $) k in vs:
  if p_deg(F,k)==1:
   pass
 if $3(vs)==2 $+ ishomog(F):
  a,b=vs
  fl=[0]*(p_deg(F,a)+1)
  $) m in F:
   fl[m[a]]=F[m]
  cc,fs=ufactor(fl)
  if $3(fs)>1 or(fs $+ fs[0][1]>1):
   $?=[]
   $) g,i in fs:
    d=$3(g)-1
    G={}
    $) j in $*($3(g)):
     if g[j]:
      m=[0]*nv
      m[a]=j
      m[b]=d-j
      G[$1(m)]=g[j]
    $) _ in $*(i):
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
   if S is $. $# $+ S:
    x={p_mono(nv,k,1):1}
    base=p_add(p_mul(p_scale(A,2),x),B)
    G1=p_sub(base,S)
    G2=p_add(base,S)
    G1=$K(G1,p_mul(p_cont(G1,k,nv),$z(p_icont($K(G1,p_cont(G1,k,nv))),nv)))
    G2=$K(G2,p_mul(p_cont(G2,k,nv),$z(p_icont($K(G2,p_cont(G2,k,nv))),nv)))
    if G1 $+ G2:
     $! msplit(G1,nv,$>+1)+msplit(G2,nv,$>+1)
 $) k in vs:
  if p_deg(F,k)<2:
   $7
  lc=p_lc(F,k)
  tc=p_coeff(F,k,0)
  da=pdivisors(lc,nv)
  db=pdivisors(tc,nv)
  if da is $# or db is $# or $3(da)*$3(db)>3000:
   $7
  x={p_mono(nv,k,1):1}
  $) a in da:
   ax=p_mul(a,x)
   $) b in db:
    $) s in(1,-1):
     G=p_add(ax,p_scale(b,s))
     Qt=$K(F,G)
     if Qt is $. $#:
      $![G]+msplit(Qt,nv,$>+1)
 $![F]
$, pdivisors(P,nv):
 c,fs=mfactor(P,nv)
 di=divisors_int(c,60)
 if di is $#:
  $! $#
 ds=[$z(d,nv)$) d in di]
 $) g,m in fs:
  nds=[]
  $) d in ds:
   v=d
   $) _ in $*(m+1):
    nds.$%(v)
    v=p_mul(v,g)
  ds=nds
  if $3(ds)>300:
   $! $#
 $! ds
$, factor_int_full(n):
 fs={}
 if n<0:
  n=-n
 st=[n]
 $H st:
  m=st.pop()
  if m==1:
   $7
  small,m=factor_int_small(m)
  $) p,k in small:
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
 $![(p,fs[p])$) p in ks]
$, powmod(b,e,m):
 r=1
 b%=m
 $H e>0:
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
 $H d%2==0:
  d//=2
  s+=1
 $) a in(2,3,5,7,11,13,17,19,23,29,31,37):
  x=powmod(a,d,n)
  if x==1 or x==n-1:
   $7
  $) _ in $*(s-1):
   x=x*x%n
   if x==n-1:
    $X
  $(:
   $! $2
 $! $F
$, rho(n):
 if n%2==0:
  $! 2
 r=iroot(n,2)
 if r*r==n:
  $! r
 c=1
 $H $F:
  x=2
  y=2
  d=1
  cnt=0
  $H d==1:
   x=(x*x+c)%n
   y=(y*y+c)%n
   y=(y*y+c)%n
   d=igcd($I(x-y),n)
   cnt+=1
   if cnt>10000:
    $X
  if d!=n $+ d!=1:
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
 if $. fs:
  $! 1
 if $3(fs)==1 $+ fs[0]==-1:
  $!-1
 if $3(fs)==1:
  $!('hold',fs[0])
 $!('hold',('*',)+$1(fs))
$, $v(e,var=$#,$A=$2):
 if $m(e):
  $! factor_rat_held(e)
 if $&(e,'$G')or $&(e,'mat'):
  $! mapexpr($4 a:$v(a,var,$A),e)
 if isrel(e):
  $!(e[0],$v(e[1],var,$A),$v(e[2],var,$A))
 if $`(e):
  $! e
 ks=[]
 kernels(e,ks)
 sortkernels(ks)
 nv=$3(ks)
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
  nfac.extend(split_radical(p2e(g,ks),m,var,$A))
 dfac=[]
 $) g,m in fd:
  dfac.extend(split_radical(p2e(g,ks),m,var,$A))
 items=[]
 $) f,m in nfac:
  if $@(f):
   const=nmul(const,nipow(f,m))
  $(:
   items.$%((f,m))
 ditems=[]
 $) f,m in dfac:
  if $@(f):
   const=ndiv(const,nipow(f,m))
  $(:
   ditems.$%((f,m))
 items.sort(key=$4 fm:fsortkey(fm[0]))
 ditems.sort(key=$4 fm:fsortkey(fm[0]))
 $?=[]
 if const!=1 or($. items $+ $. ditems):
  $?.$%(const)
 $) f,m in items:
  $?.$%(f if m==1 $(('^',f,m))
 $) f,m in ditems:
  $?.$%(('^',f,-m))
 if $3($?)==1:
  if $&($?[0],'^')or $@($?[0]):
   $!('hold',$?[0])if $. $@($?[0])$( $?[0]
  $! $?[0]
 $!('hold',('*',)+$1($?))
$, fsortkey(f):
 ss=${(f)
 ss.sort(key=varprio)
 d=0
 if ss:
  d=degree(f,ss[0])
  if d is $#:
   d=99
 $!($3(ss),okey(ss),d,okey(f))
$, split_radical(f,m,var,$A):
 if var is $# $+ $. $A:
  $![(f,m)]
 vs=${(f)
 if var is $#:
  if $3(vs)!=1:
   $![(f,m)]
  x=vs[0]
 $(:
  x=var
 cs=$^(f,x)
 if cs is $# or $3(cs)!=3:
  if cs is $. $# $+ $3(cs)==2 $+ $A:
   $![(f,m)]
  $![(f,m)]
 c,b,a=cs
 D=$;($b($9(b,b),$9(4,a,c)))
 if $. $5(D):
  if var is $#:
   $![(f,m)]
 $(:
  v=$S(D)
  if $/(v)is $0:
   v=v.$Q
  if v<0 $+ $. $A:
   $![(f,m)]
 sD=$T(D)
 r1=$Y($c($o(b),sD),$9(2,a))
 r2=$Y($b($o(b),sD),$9(2,a))
 res=[(a,m)]if a!=1 $([]
 res.$%(($b(x,r2),m))
 res.$%(($b(x,r1),m))
 $! res
''')
_x(r'''$, partfrac(e,x):
 r=to_ratform(e)
 if r is $#:
  $! $#
 N,D,ks=r
 if x $. in ks:
  $! $#
 k=ks.index(x)
 $) v in p_vars(N,$3(ks))+p_vars(D,$3(ks)):
  if v!=k:
   $! $#
 nv=$3(ks)
 num=[0]*(max(p_deg(N,k),0)+1)
 $) m in N:
  num[m[k]]=N[m]
 den=[0]*(p_deg(D,k)+1)
 $) m in D:
  den[m[k]]=D[m]
 if $3(den)<=1:
  $! $#
 q,rem=u_divmod(num,den)
 cc,fs=ufactor(den)
 $N=[u_toexpr(q,x)]
 if rem:
  parts=[u_trim(pw_list(f,m))$) f,m in fs]
  rem=u_scale(rem,ninv(cc))
  $) j in $*($3(fs)):
   f,m=fs[j]
   Pj=parts[j]
   others=[1]
   $) i in $*($3(fs)):
    if i!=j:
     others=u_mul(others,parts[i])
   g,s,t=u_egcd(others,Pj)
   Aj=u_divmod(u_mul(rem,s),Pj)[1]
   fe=u_toexpr(f,x)
   $) p in $*(m,0,-1):
    if $. Aj:
     $X
    qq,cj=u_divmod(Aj,f)
    if cj:
     $N.$%($Y(u_toexpr(cj,x),pw(fe,p)))
    Aj=qq
 $! $6($N)
$, pw_list(f,m):
 r=[1]
 $) _ in $*(m):
  r=u_mul(r,f)
 $! r
$, propfrac(e,x=$#):
 if $m(e):
  n,d=nd(e)
  if d==1:
   $! e
  qn=$I(n)//d
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
  vs=p_vars(D,$3(ks))
  if $. vs:
   $! e
  x=ks[vs[0]]
 num=p2e(N,ks)
 den=p2e(D,ks)
 cn=$^(num,x)
 cd=$^(den,x)
 if cn is $# or cd is $# or $3(cd)<=1:
  $! e
 qq,rr=e_divmod(cn,cd)
 $! $c(fromcoeffs(qq,x),$Y(fromcoeffs(rr,x),den))
$, e_divmod(a,b):
 a=[$;(c)$) c in a]
 b=[$;(c)$) c in b]
 $H b $+ b[-1]==0:
  b.pop()
 $H a $+ a[-1]==0:
  a.pop()
 if $. b:
  err("Division by zero")
 q=[0]*max($3(a)-$3(b)+1,1)
 r=$G(a)
 lb=b[-1]
 $H $3(r)>=$3(b)$+ r:
  c=$-($Y(r[-1],lb))
  kk=$3(r)-$3(b)
  q[kk]=c
  $) j in $*($3(b)):
   r[kk+j]=$;($b(r[kk+j],$9(c,b[j])))
  r.pop()
  $H r $+ r[-1]==0:
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
 nv=$3(ks)
 g=p_gcd(ra[0],rb[0],nv)
 if $. ks:
  $! p_cval(g)
 $! p2e(g,ks)
$, expand_full(e,var=$#):
 if $&(e,'$G')or $&(e,'mat'):
  $! mapexpr($4 a:expand_full(a,var),e)
 if isrel(e):
  $!(e[0],expand_full(e[1],var),expand_full(e[2],var))
 x=$;(e)
 if $. hasdenom(x)or $`(x):
  $! x
 if var is $#:
  ks=${(x)
  ks.sort(key=varprio)
  $) v in ks:
   r=partfrac(x,v)
   if r is $. $#:
    $! $;(r)
  $! x
 r=partfrac(x,var)
 if r is $. $#:
  $! $;(r)
 $! x
''')
_x(r'''TV='T_'
LNT='LNT_'
VV='V_'
class $h($=):
 pass
$, dfun($D,u):
 if $D=='sin':
  $! fn('cos',u)
 if $D=='cos':
  $! $o(fn('sin',u))
 if $D=='tan':
  $! pw(fn('cos',u),-2)
 if $D=='$w':
  $! pw($b(1,pw(u,2)),Q(-1,2))
 if $D=='arccos':
  $! $o(pw($b(1,pw(u,2)),Q(-1,2)))
 if $D=='$t':
  $! pw($c(pw(u,2),1),-1)
 if $D=='sinh':
  $! fn('cosh',u)
 if $D=='cosh':
  $! fn('sinh',u)
 if $D=='tanh':
  $! pw(fn('cosh',u),-2)
 if $D=='arcsinh':
  $! pw($c(pw(u,2),1),Q(-1,2))
 if $D=='arccosh':
  $! pw($b(pw(u,2),1),Q(-1,2))
 if $D=='arctanh':
  $! pw($b(1,pw(u,2)),-1)
 if $D=='ln':
  $! pw(u,-1)
 if $D=='$I':
  $! fn('sign',u)
 if $D in('sign','floor','ceiling','round','ipart','$q'):
  $! 0
 $! $#
$, diff(e,x,n=1):
 if n<0:
  r=e
  $) _ in $*(-n):
   r=integrate(r,x)
  $! r
 $) _ in $*(n):
  e=diff1(e,x)
 $! e
$, diff1(e,x):
 if $&(e,'$G')or $&(e,'mat'):
  $! mapexpr($4 a:diff1(a,x),e)
 if $&(e,'=')or $&(e,'<')or $&(e,'>'):
  $!(e[0],diff1(e[1],x),diff1(e[2],x))
 if $8(e,x):
  $! 0
 if e==x:
  $! 1
 h=e[0]
 if h=='+':
  $! $6([diff1(a,x)$) a in e[1:]])
 if h=='*':
  fs=e[1:]
  $N=[]
  $) i in $*($3(fs)):
   d=diff1(fs[i],x)
   if d!=0:
    $N.$%($E([d]+[fs[j]$) j in $*($3(fs))if j!=i]))
  $! $6($N)
 if h=='^':
  b=e[1]
  p=e[2]
  if $8(p,x):
   $! $9(p,pw(b,$b(p,1)),diff1(b,x))
  if $8(b,x):
   $! $9(e,fn('ln',b),diff1(p,x))
  $! $9(e,$c($9(diff1(p,x),fn('ln',b)),$Y($9(p,diff1(b,x)),b)))
 if h=='log':
  b=e[2]if $3(e)>2 $( 10
  $! diff1($Y(fn('ln',e[1]),fn('ln',b)),x)
 if h=='when':
  $! fn('when',e[1],diff1(e[2],x),diff1(e[3],x))if $3(e)>3 $( fn('when',e[1],diff1(e[2],x))
 if h=='$l' $+ $3(e)==3 $+ e[2]==x:
  $! e[1]
 if h=='$l' $+ $3(e)==5 $+ $8(e[1],x)is $2 $+ e[2]!=x:
  f,v,a,b=e[1],e[2],e[3],e[4]
  $! $b($9($W(f,v,b),diff1(b,x)),$9($W(f,v,a),diff1(a,x)))
 if $3(e)==2:
  d=dfun(h,e[1])
  if d is $. $#:
   $! $9(d,diff1(e[1],x))
 $!('d',e,x)
$, $f(u,x):
 cs=$^(u,x)
 if cs is $# or $3(cs)!=2 or cs[1]==0:
  $! $#
 $! cs[1],cs[0]
$, nice(e):
 try:
  e=$-(e)
 $< $=:
  $! e
 if $. hasdenom(e)or $`(e)or $&(e,'$G')or $&(e,'mat'):
  $! e
 $}=e
 bl=$3(fmt(e))
 if bl>400:
  $! e
 $) f in(comdenom,$v):
  try:
   c=f(e)
   l=$3(fmt(c))
   if l<bl:
    $}=c
    bl=l
  $< $=:
   pass
 $! $}
BUDGET=[0]
$, integrate(f,x,$>=0):
 BUDGET[0]=0
 r=integ(f,x,$>)
 if r is $#:
  $!('$l',f,x)
 $! r
$, integ(f,x,$>=0):
 if $>>7:
  $! $#
 if $>==0:
  BUDGET[0]=0
 BUDGET[0]+=1
 if BUDGET[0]>400:
  $! $#
 if $8(f,x):
  $! $9(f,x)
 if f==x:
  $! $9($|,pw(x,2))
 h=f[0]if $/(f)is $1 $( $#
 if h=='+':
  $?=[]
  $) t in f[1:]:
   r=integ(t,x,$>+1)
   if r is $#:
    $! integ_whole(f,x,$>)
   $?.$%(r)
  $! $6($?)
 if h=='*':
  c=[g $) g in f[1:]if $8(g,x)]
  v=[g $) g in f[1:]if $. $8(g,x)]
  if c:
   r=integ($E(v),x,$>)
   if r is $#:
    $! $#
   $! $9($E(c),r)
 r=itable(f,x)
 if r is $. $#:
  $! r
 $! integ_whole(f,x,$>)
$, integ_whole(f,x,$>):
 d=degree(f,x)
 if d is $. $#:
  g=$;(f)
  if g!=f:
   $! integ(g,x,$>+1)
 r=irational(f,x)
 if r is $. $#:
  $! r
 r=itanpow(f,x,$>)
 if r is $. $#:
  $! r
 r=isecpow(f,x,$>)
 if r is $. $#:
  $! r
 r=isubst(f,x,$>)
 if r is $. $#:
  $! r
 if hastrig(f):
  g=tcollect(f)
  if g!=f:
   r=integ(g,x,$>+1)
   if r is $. $#:
    $! r
 r=iparts(f,x,$>)
 if r is $. $#:
  $! r
 g=$;(f)
 if g!=f:
  r=integ(g,x,$>+1)
  if r is $. $#:
   $! r
 $! $#
''')
_x(r'''$, itable(f,x):
 h=head(f)
 if h=='^':
  b=f[1]
  p=f[2]
  if $8(p,x):
   lb=$f(b,x)
   if lb is $. $#:
    a=lb[0]
    if p==-1:
     $! $Y(fn('ln',fn('$I',b)),a)
    $! $Y(pw(b,$c(p,1)),$9(a,$c(p,1)))
   if(p==$| or p==Q(-1,2))$+ degree(b,x)==2:
    $! iquadrad(b,p,x)
   if $3(b)==2 $+ head(b)in('sin','cos','tan','sinh','cosh')$+ $/(b)is $1:
    lu=$f(b[1],x)
    if lu is $. $#:
     a=lu[0]
     u=b[1]
     n=b[0]
     if n=='cos' $+ p==-2:
      $! $Y(fn('tan',u),a)
     if n=='sin' $+ p==-2:
      $! $Y($o(pw(fn('tan',u),-1)),a)
     if n=='cos' $+ p==-1:
      $! $Y(fn('ln',fn('$I',$c(pw(fn('cos',u),-1),fn('tan',u)))),a)
     if n=='sin' $+ p==-1:
      $! $Y(fn('ln',fn('$I',fn('tan',$9($|,u)))),a)
     if n=='tan' $+ p==-1:
      $! $Y(fn('ln',fn('$I',fn('sin',u))),a)
     if n=='cosh' $+ p==-2:
      $! $Y(fn('tanh',u),a)
  if $8(b,x):
   lu=$f(p,x)
   if lu is $. $#:
    a=lu[0]
    if b=='e':
     $! $Y(f,a)
    $! $Y(f,$9(a,fn('ln',b)))
  $! $#
 if $/(f)is $1 $+ $3(f)==2:
  u=f[1]
  lu=$f(u,x)
  if lu is $#:
   $! $#
  a=lu[0]
  r=$#
  if h=='sin':
   r=$o(fn('cos',u))
  $J h=='cos':
   r=fn('sin',u)
  $J h=='tan':
   r=$o(fn('ln',fn('$I',fn('cos',u))))
  $J h=='sinh':
   r=fn('cosh',u)
  $J h=='cosh':
   r=fn('sinh',u)
  $J h=='tanh':
   r=fn('ln',fn('cosh',u))
  $J h=='ln':
   r=$b($9(u,fn('ln',u)),u)
  $J h=='$t':
   r=$b($9(u,fn('$t',u)),$9($|,fn('ln',$c(pw(u,2),1))))
  $J h=='$w':
   r=$c($9(u,fn('$w',u)),$T($b(1,pw(u,2))))
  $J h=='arccos':
   r=$b($9(u,fn('arccos',u)),$T($b(1,pw(u,2))))
  $J h=='$I':
   r=$9($|,u,fn('$I',u))
  $J h=='sign':
   r=fn('$I',u)
  $J h=='arcsinh':
   r=$b($9(u,fn('arcsinh',u)),$T($c(pw(u,2),1)))
  $J h=='arctanh':
   r=$c($9(u,fn('arctanh',u)),$9($|,fn('ln',$b(1,pw(u,2)))))
  if r is $. $#:
   $! $Y(r,a)
 if h=='log' $+ $3(f)==3:
  lu=$f(f[1],x)
  if lu is $. $#:
   u=f[1]
   $! $Y($b($9(u,fn('ln',u)),u),$9(lu[0],fn('ln',f[2])))
 $! $#
$, iquadrad(b,p,x):
 cs=$^(b,x)
 C,B,A=cs
 if $. $5(A):
  $! $#
 av=$S(A)
 if $/(av)is $0:
  $! $#
 D=$b($9(B,B),$9(4,A,C))
 if p==Q(-1,2):
  if av<0:
   $! $9(pw($o(A),Q(-1,2)),fn('$w',$Y($o($c($9(2,A,x),B)),$T(D))))
  sA=$T(A)
  $! $9(pw(A,Q(-1,2)),fn('ln',fn('$I',$c($T(b),$9(sA,x),$Y(B,$9(2,sA))))))
 J=iquadrad(b,Q(-1,2),x)
 if J is $#:
  $! $#
 $! $c($Y($9($c($9(2,A,x),B),$T(b)),$9(4,A)),
 $9($Y($b($9(4,A,C),$9(B,B)),$9(8,A)),J))
$, irational(f,x):
 ks=[]
 kernels(f,ks)
 $) k in ks:
  if k!=x:
   $! $#
 if $. hasdenom(f):
  $! $#
 pf=partfrac(f,x)
 if pf is $#:
  $! $#
 $N=pf[1:]if $&(pf,'+')$((pf,)
 $?=[]
 $) t in $N:
  if $. hasdenom(t):
   r=integ(t,x,5)
   if r is $#:
    $! $#
   $?.$%(r)
   $7
  fs=t[1:]if $&(t,'*')$((t,)
  num=[]
  den=$#
  k=1
  $) g in fs:
   if $&(g,'^')$+ $/(g[2])is $q $+ g[2]<0:
    den=g[1]
    k=-g[2]
   $(:
    num.$%(g)
  if den is $#:
   $! $#
  N=$E(num)
  dg=degree(den,x)
  if dg==1:
   r=integ(t,x,5)
   if r is $#:
    $! $#
   $?.$%(r)
  $J dg==2:
   r=iquadfrac(N,den,k,x)
   if r is $#:
    $! $#
   $?.$%(r)
  $(:
   $! $#
 $! $6($?)
$, iquadfrac(N,Qd,k,x):
 cs=$^(N,x)
 if cs is $# or $3(cs)>2:
  $! $#
 n0=cs[0]
 n1=cs[1]if $3(cs)>1 $( 0
 C,B,A=$^(Qd,x)
 res=[]
 if n1!=0:
  if k==1:
   D=$b($9(B,B),$9(4,A,C))
   dv=$S(D)if $5(D)$( 0
   arg=Qd if($/(dv)is $. $0 $+ dv<0 $+ $S(A)>0)$( fn('$I',Qd)
   res.$%($9($Y(n1,$9(2,A)),fn('ln',arg)))
  $(:
   res.$%($9($Y(n1,$9(2,A)),$Y(-1,$9(k-1,pw(Qd,k-1)))))
 c0=$b(n0,$Y($9(n1,B),$9(2,A)))
 if c0!=0:
  J=jquad(A,B,C,Qd,k,x)
  if J is $#:
   $! $#
  res.$%($9(c0,J))
 $! $6(res)
$, jquad(A,B,C,Qd,k,x):
 D=$;($b($9(B,B),$9(4,A,C)))
 if k==1:
  if $. $5(D):
   $! $#
  dv=$S(D)
  if $/(dv)is $0:
   $! $#
  L=$c($9(2,A,x),B)
  if dv<0:
   s=$T($o(D))
   $! $9($Y(2,s),fn('$t',$Y(L,s)))
  if dv>0:
   s=$T(D)
   $! $9(pw(s,-1),fn('ln',fn('$I',$Y($b(L,s),$c(L,s)))))
  $! $Y(-2,L)
 Jp=jquad(A,B,C,Qd,k-1,x)
 if Jp is $#:
  $! $#
 Dl=$o(D)
 L=$c($9(2,A,x),B)
 $! $c($9($Y(L,$9(k-1,Dl)),pw(Qd,1-k)),
 $9($Y($9(2*k-3,2,A),$9(k-1,Dl)),Jp))
$, itanpow(f,x,$>):
 if $&(f,'^')$+ $&(f[1],'tan')$+ $/(f[2])is $q $+ f[2]>=2:
  u=f[1][1]
  lu=$f(u,x)
  if lu is $#:
   $! $#
  n=f[2]
  a=lu[0]
  t=f[1]
  first=$Y(pw(t,n-1),$9(n-1,a))
  $_=integ(pw(t,n-2),x,$>+1)
  if $_ is $#:
   $! $#
  $! $b(first,$_)
 $! $#
$, isecpow(f,x,$>):
 if($&(f,'^')$+ head(f[1])in('cos','sin')$+ $3(f[1])==2
 $+ $/(f[2])is $q $+ f[2]<=-3):
  u=f[1][1]
  lu=$f(u,x)
  if lu is $#:
   $! $#
  n=-f[2]
  a=lu[0]
  if f[1][0]=='cos':
   first=$9(pw(fn('cos',u),2-n),fn('tan',u))
  $(:
   first=$o($9(pw(fn('sin',u),2-n),pw(fn('tan',u),-1)))
  $_=integ(pw(f[1],2-n),x,$>+1)
  if $_ is $#:
   $! $#
  $! $c($Y(first,$9(n-1,a)),$9(Q(n-2,n-1),$_))
 $! $#
''')
_x(r'''$, cands(f,x,$?):
 if $/(f)is $. $1 or $8(f,x)or f[0]=='Q':
  $!
 h=f[0]
 if h=='+' or h=='*':
  $) a in f[1:]:
   cands(a,x,$?)
  $!
 if h=='^':
  if f[1]!=x $+ $. $8(f[1],x)$+ f[1]$. in $?:
   $?.$%(f[1])
  if isq(f[2])$+ $. $8(f[1],x):
   rad=pw(f[1],Q(1,f[2][2]))
   if rad $. in $?:
    $?.$%(rad)
  if $. $8(f[2],x)$+ f[2]$. in $?:
   $?.$%(f[2])
   if f $. in $?:
    $?.$%(f)
  if f[1]==x $+ f $. in $? $+ $@(f[2])$+ f[2]!=-1:
   $?.$%(f)
   if $i(f[2])$+ f[2]%2==0 $+ f[2]>2 $+ pw(x,2)$. in $?:
    $?.$%(pw(x,2))
  cands(f[1],x,$?)
  cands(f[2],x,$?)
  $!
 if f $. in $?:
  $?.$%(f)
 $) a in f[1:]:
  if a!=x $+ $. $8(a,x)$+ a $. in $?:
   $?.$%(a)
  cands(a,x,$?)
$, subst_kernel(q,u,V,x):
 if $&(u,'^')$+ u[1]==x $+ $@(u[2]):
  q2=$W(q,x,pw(V,pw(u[2],-1)))
  $! $W(q2,fn('$I',V),V)
 if $&(u,'ln'):
  lu=$f(u[1],x)
  if lu is $. $#:
   a,b=lu
   $! $W(q,x,$Y($b(pw('e',V),b),a))
 if $&(u,'^')$+ isq(u[2])$+ $. $8(u[1],x):
  cs_=$^(u[1],x)
  q2=$W(q,u,V)
  if cs_ is $. $# $+ $. $8(q2,x):
   nz=[k $) k in $*(1,$3(cs_))if cs_[k]!=0]
   if $3(nz)==1:
    k=nz[0]
    xk=$Y($b(pw(V,pw(u[2],-1)),cs_[0]),cs_[k])
    q3=$W(q2,x,pw(xk,Q(1,k)))
    if $8(q3,x):
     $! q3
  $! q2
 if $&(u,'^')$+ u[1]=='e':
  lu=$f(u[2],x)
  if lu is $. $# $+ lu[1]==0:
   a=lu[0]
   $! subst_exp(q,a,V,x)
 $! $W(q,u,V)
$, subst_exp(q,a,V,x):
 if $/(q)is $. $1 or q[0]=='Q':
  $! q
 if q[0]=='^' $+ q[1]=='e':
  lm=$f(q[2],x)
  if lm is $. $#:
   $! $9(pw(V,$Y(lm[0],a)),pw('e',lm[1]))
 $! simp((q[0],)+$1(subst_exp(b,a,V,x)$) b in q[1:]))
$, isubst(f,x,$>):
 if $>>5:
  $! $#
 VV='V%d_'%$>
 $H has(f,VV)or VV==x:
  VV=VV+'_'
 cs=[]
 cands(f,x,cs)
 fracf=hasfracpow(f,x)
 big=$3(okey(f))>500
 $) u in cs[:14]:
  if u==x:
   $7
  du=diff(u,x)
  if du==0:
   $7
  q=$Y(f,du)
  if $. big:
   q=$-(q)
  q2=subst_kernel(q,u,VV,x)
  if $8(q2,x)$+(fracf or $. hasfracpow(q2,VV))$+ $3(okey(q2))<800:
   r=integ(q2,VV,$>+2)
   if r is $. $#:
    $! $W(r,VV,u)
 $) u in cs:
  if $&(u,'+'):
   lu=$f(u,x)
   if lu is $. $#:
    a,b=lu
    g=$;($Y($W(f,x,$Y($b(VV,b),a)),a))
    r=integ(g,VV,$>+2)
    if r is $. $#:
     $! $W(r,VV,u)
 $! $#
$, hasfracpow(e,x):
 if $/(e)is $. $1 or e[0]=='Q':
  $! $2
 if e[0]=='^' $+ $. $i(e[2])$+ $. $8(e[1],x):
  $! $F
 $) a in e[1:]:
  if hasfracpow(a,x):
   $! $F
 $! $2
$, hastrig(f):
 if $/(f)is $. $1 or f[0]=='Q':
  $! $2
 if f[0]in('sin','cos'):
  $! $F
 $) a in f[1:]:
  if hastrig(a):
   $! $F
 $! $2
$, ispoly(e,x):
 $! degree(e,x)is $. $#
$, iparts(f,x,$>):
 if $>>5:
  $! $#
 fs=f[1:]if $&(f,'*')$((f,)
 P=[]
 G=[]
 $) g in fs:
  if ispoly(g,x):
   P.$%(g)
  $(:
   G.$%(g)
 if $3(G)==2:
  ex=$#
  tr=$#
  $) g in G:
   if $&(g,'^')$+ g[1]=='e' $+ $f(g[2],x):
    ex=g
   $J head(g)in('sin','cos')$+ $f(g[1],x):
    tr=g
  if ex is $. $# $+ tr is $. $# $+ $. P:
   a=$f(ex[2],x)[0]
   b=$f(tr[1],x)[0]
   u=tr[1]
   den=$c($9(a,a),$9(b,b))
   if tr[0]=='sin':
    r=$9(ex,$b($9(a,fn('sin',u)),$9(b,fn('cos',u))))
   $(:
    r=$9(ex,$c($9(a,fn('cos',u)),$9(b,fn('sin',u))))
   $! $Y(r,den)
  $! $#
 if $3(G)!=1:
  $! $#
 g=G[0]
 Pp=$E(P)
 gh=head(g)
 tabular=$2
 if $&(g,'^')$+ g[1]=='e' $+ $f(g[2],x):
  tabular=$F
 $J $&(g,'^')$+ $@(g[1])$+ $f(g[2],x):
  tabular=$F
 $J gh in('sin','cos','sinh','cosh')$+ $f(g[1],x):
  tabular=$F
 if tabular $+ P:
  res=[]
  sg=1
  Gi=g
  Pd=Pp
  $) _ in $*(40):
   Gi=integ(Gi,x,$>+1)
   if Gi is $#:
    $! $#
   res.$%($9(sg,Pd,Gi))
   Pd=diff(Pd,x)
   sg=-sg
   if Pd==0:
    $! $6(res)
  $! $#
 if gh in('ln','$t','$w','arccos','log','arcsinh','arctanh')or($&(g,'^')$+ head(g[1])in('ln','$w','$t')$+ $i(g[2])$+ g[2]>0):
  V=integ(Pp,x,$>+1)
  if V is $#:
   $! $#
  $_=integ($-($;($9(V,diff(g,x)))),x,$>+1)
  if $_ is $#:
   $! $#
  $! $b($9(g,V),$_)
 $! $#
$, defint(f,x,a,b):
 if a==b:
  $! 0
 BUDGET[0]=0
 F=integ(f,x)
 if F is $. $# $+ $. $`(f):
  sing=singular_points(f,x,a,b)
  if sing is $#:
   sing=[]
  pts=[a]+sing+[b]
  total=0
  $) i in $*($3(pts)-1):
   lo=pts[i]
   hi=pts[i+1]
   vb=limit(F,x,hi,-1 if $. isinf(hi)$( 0)
   va=limit(F,x,lo,1 if $. isinf(lo)$( 0)
   if $&(vb,'limit')or $&(va,'limit'):
    total=$#
    $X
   total=$c(total,$b(vb,va))
  if total is $. $# $+ total!='$L':
   $! total
 if $5(a)$+ $5(b)$+ freeofall(f,[s $) s in ${(f)if s!=x]):
  try:
   $! nint(f,x,a,b)
  $< $=:
   pass
 $!('$l',f,x,a,b)
$, isinf(v):
 $! v=='$]' or v==('*',-1,'$]')
$, singular_points(f,x,a,b):
 if $.($5(a)$+ $5(b)):
  $![]
 try:
  av=nreal(a)if $. isinf(a)$((-1e300 if a!='$]' $( 1e300)
  bv=nreal(b)if $. isinf(b)$((1e300 if b=='$]' $(-1e300)
 $< $=:
  $![]
 lo,hi=min(av,bv),max(av,bv)
 pts=[]
 dens=[]
 collect_dens(f,x,dens)
 $) d in dens:
  u=u_from_expr(d,x)
  if u is $# or $3(u)<2:
   $7
  $) r in aberth(u):
   if $I(r.imag)<1e-9 $+ lo<r.$Q<hi:
    rr=exactify(r.$Q)if $I(r.$Q-round(r.$Q))<1e-12 $( r.$Q
    pts.$%(rr)
 pts.sort(key=$4 p:tofl(p))
 if av>bv:
  pts.reverse()
 $! pts
''')
_x(r'''$, collect_dens(f,x,$?):
 if $/(f)is $. $1 or f[0]=='Q':
  $!
 if f[0]=='^' $+ $@(f[2])$+ $a(f[2])<0 $+ $. $8(f[1],x):
  $?.$%(f[1])
 if f[0]=='ln' or f[0]=='tan':
  pass
 $) a in f[1:]:
  collect_dens(a,x,$?)
$, nint(f,x,a,b,tol=1e-10):
 r=nint0(f,x,a,b,tol)
 if $/(r)is $0:
  if $I(r.imag)<1e-12*(1+$I(r.$Q)):
   $! r.$Q
  $! fromcomplex(r)
 $! r
$, nint0(f,x,a,b,tol=1e-10):
 sgn=1.0
 av=a
 bv=b
 if isinf(a)or isinf(b):
  if a=='$]' or b==('*',-1,'$]'):
   $!-nint0(f,x,b,a,tol)
  if isinf(a)$+ isinf(b):
   g=$4 t:_nv(f,x,t/(1-t*t))*(1+t*t)/(1-t*t)**2
   $! _gk_adapt(g,-1.0,1.0,tol,0)
  if isinf(b):
   a0=nreal(a)
   g=$4 t:_nv(f,x,a0+t/(1-t))/(1-t)**2
   $! _gk_adapt(g,0.0,1.0,tol,0)
  b0=nreal(b)
  g=$4 t:_nv(f,x,b0-(1-t)/t)/(t*t)
  $! _gk_adapt(g,0.0,1.0,tol,0)
 a0=nreal(a)
 b0=nreal(b)
 g=$4 t:_nv(f,x,t)
 $! _gk_adapt(g,a0,b0,tol,0)
$, _nv(f,x,t):
 try:
  v=$S(f,{x:t})
 $< $B:
  $! 0.0
 $<($O,$U):
  $! 0.0
 if $/(v)is $0:
  if $I(v.imag)>1e-12*(1+$I(v.$Q)):
   $! v
  v=v.$Q
 if v!=v or v in($C('$]'),$C('-$]')):
  $! 0.0
 $! v
XGK=(0.991455371120812639206854697526329,0.949107912342758524526189684047851,
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
 $) j in $*(7):
  dx=h*XGK[j]
  f1=g(c-dx)
  f2=g(c+dx)
  rk+=WGK[j]*(f1+f2)
  if j%2==1:
   rg+=WG[j//2]*(f1+f2)
 $! rk*h,$I((rk-rg)*h)
$, _gk_adapt(g,a,b,tol,$>):
 r,e=_gk(g,a,b)
 if e<=tol*max(1.0,$I(r))or $>>18:
  $! r
 m=0.5*(a+b)
 $! _gk_adapt(g,a,m,tol/2,$>+1)+_gk_adapt(g,m,b,tol/2,$>+1)
BIGP=10**6
$, s_const(c):
 if c==0:
  $!({},BIGP)
 $!({0:c},BIGP)
$, s_val(A):
 if $. A[0]:
  $! A[1]
 m=$#
 $) k in A[0]:
  if m is $# or ncmp(k,m)<0:
   m=k
 $! m
$, cs(c):
 c=$;(c)
 if hasdenom(c):
  c=$-(c)
 $! c
$, s_add(A,B):
 p=A[1]if ncmp(A[1],B[1])<0 $( B[1]
 d={}
 $) S in(A,B):
  $) k in S[0]:
   if ncmp(k,p)<0:
    d[k]=$c(d.get(k,0),S[0][k])
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
    d[k]=$c(d.get(k,0),$9(A[0][a],B[0][b]))
 $?={}
 $) k in d:
  v=cs(d[k])
  if v!=0:
   $?[k]=v
 $!($?,p)
$, s_scale(A,c,shift=0):
 $?={}
 $) k in A[0]:
  v=cs($9(A[0][k],c))
  if v!=0:
   $?[nadd(k,shift)]=v
 $!($?,nadd(A[1],shift))
$, s_lead(A):
 if $. A[0]:
  $n $h()
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
 $) k in $*(1,$3(coefs)):
  P=s_mul(P,U)
  if $. P[0]:
   $X
  if coefs[k]!=0:
   res=s_add(res,s_scale(P,coefs[k]))
 $! res
$, nterms(U):
 v=s_val(U)
 if ncmp(v,0)<=0:
  $n $h()
 p=U[1]
 if ncmp(p,BIGP)>=0:
  $! 0 if $. U[0]$( 30
 n=nfloor(ndiv(p,v))+1
 if n>30:
  n=30
 $! n
$, s_pow(A,p):
 if $/(p)is $q $+ p>=0:
  R=({0:1},BIGP)
  $) _ in $*(p):
   R=s_mul(R,A)
  $! R
 a,c,U=s_split(A)
 n=nterms(U)if U[0]$( 0
 coefs=[1]
 b=1
 $) k in $*(1,n+1):
  b=$9(b,$Y($b(p,k-1),k))
  coefs.$%(b)
 S=s_powser(U,coefs)if U[0]$(({0:1},U[1])
 ap=$9(a,p)
 if $. $m(ap):
  $n $h()
 cp=pw(c,p)
 $! s_scale(S,cp,ap)
$, s_exp(A):
 neg_=[k $) k in A[0]if ncmp(k,0)<0]
 if neg_:
  $n $h()
 c0=A[0].get(0,0)
 U=(dict([(k,A[0][k])$) k in A[0]if k!=0]),A[1])
 shift=0
 if has(c0,LNT):
  cc=$^(c0,LNT)
  if cc is $# or $3(cc)!=2 or $. $m(cc[1]):
   $n $h()
  shift=cc[1]
  c0=cc[0]
 n=nterms(U)if U[0]$( 0
 coefs=[1]
 f=1
 $) k in $*(1,n+1):
  f=f*k
  coefs.$%(Q(1,f))
 S=s_powser(U,coefs)if U[0]$(({0:1},U[1])
 $! s_scale(S,pw('e',c0),shift)
$, s_ln(A):
 a,c,U=s_split(A)
 n=nterms(U)if U[0]$( 0
 coefs=[0]
 $) k in $*(1,n+1):
  coefs.$%(Q((-1)**(k+1),k))
 S=s_powser(U,coefs)if U[0]$(({},U[1])
 base=$c(fn('ln',c),$9(a,LNT))
 $! s_add(S,(({0:base}if base!=0 $({}),BIGP))
''')
_x(r'''$, s_fun($D,A):
 neg_=[k $) k in A[0]if ncmp(k,0)<0]
 if neg_:
  if $D=='$t':
   a,c=s_lead(A)
   sg=$S(c)
   sg=1 if($/(sg)is $. $0 $+ sg>0)$(-1
   inv_=s_pow(A,-1)
   $! s_add(s_const($9(sg,$|,'pi')),s_scale(s_fun('$t',inv_),-1))
  if $D=='tanh':
   a,c=s_lead(A)
   $! s_const(1 if $S(c).$Q>0 $(-1)
  $n $h()
 c0=A[0].get(0,0)
 if has(c0,LNT):
  $n $h()
 U=(dict([(k,A[0][k])$) k in A[0]if k!=0]),A[1])
 if $D=='$I' or $D=='sign':
  a,c=s_lead(A)
  v=$S($W(c,LNT,-1000))if has(c,LNT)$( $S(c)
  if $/(v)is $0:
   $n $h()
  sg=1 if v>0 $(-1
  if $D=='sign':
   $! s_const(sg)
  $! s_scale(A,sg)
 if $D in('floor','ceiling','ipart','round','$q','fpart'):
  $n $h()
 n=nterms(U)if U[0]$( 0
 z='Z_'
 g=fn($D,z)
 coefs=[$W(g,z,c0)]
 fact=1
 $) k in $*(1,n+1):
  g=diff(g,z)
  fact*=k
  coefs.$%(cs($Y($W(g,z,c0),fact)))
 $) cc in coefs:
  if has(cc,'$L')or cc=='$L' or has(cc,'$]'):
   $n $h()
 if $. U[0]:
  $! s_const(coefs[0])if $F $( $#
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
   if $m(p):
    $! trunc(s_pow(B,p),N)
   if $5(p)or $F:
    a,c,U=s_split(B)
    if a!=0:
     $n $h()
    $! trunc(s_pow(B,p),N)
  if $8(b,TV):
   $! trunc(s_exp(s_scale(ser(p,N),fn('ln',b))),N)
  $! trunc(s_exp(s_mul(ser(p,N),s_ln(ser(b,N)))),N)
 if h=='ln':
  $! trunc(s_ln(ser(e[1],N)),N)
 if h=='log':
  b=e[2]if $3(e)>2 $( 10
  $! trunc(s_scale(s_ln(ser(e[1],N)),pw(fn('ln',b),-1)),N)
 if $3(e)==2:
  $! trunc(s_fun(h,ser(e[1],N)),N)
 $n $h()
$, trunc(A,N):
 if ncmp(A[1],N)<=0:
  $! A
 $!(dict([(k,A[0][k])$) k in A[0]if ncmp(k,N)<0]),N)
$, series_t(e,order,need=$#):
 extra=3
 $) _ in $*(4):
  S=ser(e,nadd(order,extra))
  if ncmp(S[1],order)>0 $+(need is $# or S[0]):
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
$, lnt_sign(c):
 cc=$^(c,LNT)
 if cc is $#:
  v=$S($W(c,LNT,-1e6))
  $! v
 k=$3(cc)-1
 lead=cc[k]
 v=$S(lead)
 if $/(v)is $0:
  $! v
 if k%2:
  v=-v
 $! v
$, limit(f,x,a,dirn=0):
 if $&(f,'$G')or $&(f,'mat'):
  $! mapexpr($4 g:limit(g,x,a,dirn),f)
 if $8(f,x):
  $! f
 if a=='$]' or a==('*',-1,'$]'):
  sub_=pw(TV,-1)if a=='$]' $( $o(pw(TV,-1))
  $! lim_side(f,x,sub_,a)
 if dirn==0 $+ $. has_disc(f):
  try:
   v=$W(f,x,a)
   if v!='$L' $+ $8(v,'$L')$+ $. has(v,'$]'):
    v2=v
    if $5(v2):
     vv=$S(v2)
     if $/(vv)is $0 $+ $I(vv.imag)>1e-12 $+ $8(f,'i'):
      $n $O
    $! v
  $<($M,$B,$O,TypeError):
   pass
 if dirn==1:
  $! lim_side(f,x,$c(a,TV),a)
 if dirn==-1:
  $! lim_side(f,x,$b(a,TV),a)
 r=lim_side(f,x,$c(a,TV),a)
 l=lim_side(f,x,$b(a,TV),a)
 if r==l:
  $! r
 if $&(r,'limit')or $&(l,'limit'):
  $!('limit',f,x,a)
 try:
  if $5(r)$+ $5(l)$+ $. has(r,'$]')$+ $. has(l,'$]'):
   if $I($S(r)-$S(l))<1e-12:
    $! r
 $< $=:
  pass
 $! '$L'
$, has_disc(f):
 if $/(f)is $. $1 or f[0]=='Q':
  $! $2
 if f[0]in('floor','ceiling','sign','ipart','round','fpart','$q','when','$I','mod'):
  $! $F
 $) a in f[1:]:
  if has_disc(a):
   $! $F
 $! $2
$, lim_side(f,x,sub_,a):
 g=$W(f,x,sub_)
 try:
  r=lead_t(g)
  if r is $#:
   $! 0
  al,c=r
  if has(c,TV):
   $n $h()
  if ncmp(al,0)>0:
   $! 0
  if has(c,LNT):
   v=lnt_sign(c)
   if $/(v)is $0:
    $! '$L'
   if v==0:
    $n $h()
   $! '$]' if v>0 $(('*',-1,'$]')
  if al==0:
   $! c
  if $. $5(c):
   $! $9(c,'$]')
  v=$S(c)
  if $/(v)is $0:
   $! '$L'
  $! '$]' if v>0 $(('*',-1,'$]')
 $<($h,$M,$B,$O,TypeError,$U):
  pass
 r=lim_lh(g,0)
 if r is $. $#:
  $! r
 $! lim_num(g,a)
$, lim_val(g,$>):
 try:
  r=lead_t(g)
  if r is $#:
   $! 0
  al,c=r
  if has(c,TV):
   $n $h()
  if ncmp(al,0)>0:
   $! 0
  if has(c,LNT):
   v=lnt_sign(c)
   $! '$]' if v>0 $(('*',-1,'$]')
  if al==0:
   $! c
  v=$S(c)
  $! '$]' if v>0 $(('*',-1,'$]')
 $<($h,$M,$B,$O,TypeError,$U):
  pass
 $! lim_lh(g,$>+1)
''')
_x(r'''$, lim_lh(g,$>):
 if $>>4:
  $! $#
 if $8(g,TV):
  $! g
 h=head(g)
 if h=='^' $+ $. $8(g[2],TV):
  L=lim_val($9(g[2],fn('ln',g[1])),$>)
  if L is $#:
   $! $#
  $! pw('e',L)
 if h=='^' $+ $@(g[2]):
  L=lim_val(g[1],$>)
  if L is $#:
   $! $#
  if L==0 $+ $a(g[2])<0:
   $! '$]'
  $! pw(L,g[2])
 if h=='*':
  nu,de=numer_denom(g)
  if de!=1:
   ln_=lim_val(nu,$>)
   ld=lim_val(de,$>)
   if ln_ is $# or ld is $#:
    $! $#
   if(ln_==0 $+ ld==0)or(isinfv(ln_)$+ isinfv(ld)):
    $! lim_val($-($Y(diff(nu,TV),diff(de,TV))),$>)
   if ld==0:
    s=$S($W(de,TV,1e-9))
    sn=$S(ln_)if $5(ln_)$+ $. isinfv(ln_)$((1 if ln_=='$]' $(-1)
    $! '$]' if(s.$Q if $/(s)is $0 $( s)*(sn.$Q if $/(sn)is $0 $( sn)>0 $(('*',-1,'$]')
   $! $Y(ln_,ld)
  ls=[lim_val(fct,$>)$) fct in g[1:]]
  if $# in ls:
   $! $#
  zero=[i $) i in $*($3(ls))if ls[i]==0]
  infs=[i $) i in $*($3(ls))if isinfv(ls[i])]
  if zero $+ infs:
   i=zero[0]
   j=infs[0]
   $_=$E([g[k+1]$) k in $*($3(ls))if k!=i $+ k!=j])
   q=$Y(g[i+1],pw(g[j+1],-1))
   r=lim_val(q,$>)
   if r is $#:
    $! $#
   $! $9(r,lim_val($_,$>))
  $! $E(ls)
 if h=='+':
  ls=[lim_val(t,$>)$) t in g[1:]]
  if $# in ls:
   $! $#
  r=$6(ls)
  if r!='$L':
   $! r
  ii=[k $) k in $*($3(ls))if isinfv(ls[k])]
  if $. ii:
   $! $#
  i=ii[0]
  A=g[i+1]
  $_=$6([g[k+1]$) k in $*($3(ls))if k!=i])
  q=lim_val($-($Y($_,A)),$>)
  if q is $# or q=='$L':
   $! $#
  $! $9(ls[i],$c(1,q))if q!=-1 $( $#
 if $/(g)is $1 $+ $3(g)==2:
  L=lim_val(g[1],$>)
  if L is $#:
   $! $#
  $! fn(h,L)
 $! $#
$, isinfv(v):
 $! v=='$]' or v==('*',-1,'$]')
$, lim_num(g,a):
 try:
  $g=[]
  $) k in $*(4,9):
   t=10.0**(-k)
   $g.$%($S(g,{TV:t}))
  v1=$g[-1]
  v2=$g[-2]
  if $/(v1)is $0 or $/(v2)is $0:
   $!('limit',g)
  if $I(v1)>1e12 $+ $I(v1)>$I(v2):
   $! '$]' if v1>0 $(('*',-1,'$]')
  if $I(v1-v2)<1e-6*(1+$I(v1)):
   $! exactify_guess(v1)
 $< $=:
  pass
 $!('limit',g)
$, exactify_guess(v):
 r=float2rat(v,1e-9)
 n,d=nd(r)
 if d<1000:
  $! r
 $! v
$, series_at(f,x,a,order):
 if a=='$]' or a==('*',-1,'$]'):
  sub_=pw(TV,-1)if a=='$]' $( $o(pw(TV,-1))
  back=pw(x,-1)if a=='$]' $( $o(pw(x,-1))
 $(:
  sub_=$c(a,TV)
  back=$b(x,a)
 g=$W(f,x,sub_)
 S=series_t(g,order)
 $! S,back
$, taylor(f,x,n,a=0):
 try:
  S,back=series_at(f,x,a,n)
 $<($h,$M,$B,$O):
  $! taylor_d(f,x,n,a)
 $N=[]
 $) k in S[0]:
  if ncmp(k,n)>0:
   $7
  if $.($/(k)is $q $+ k>=0)or has(S[0][k],LNT):
   $!('taylor',f,x,n,a)
  $N.$%($9(S[0][k],pw(back,k)))
 $! $6($N)
$, taylor_d(f,x,n,a):
 $N=[]
 g=f
 fact=1
 $) k in $*(n+1):
  if k:
   fact*=k
   g=diff(g,x)
  v=$W(g,x,a)
  if has(v,'$L')or v=='$L' or has(v,'$]'):
   $!('taylor',f,x,n,a)
  $N.$%($9($Y(v,fact),pw($b(x,a),k)))
 $! $6($N)
$, series_cmd(f,x,n,a=0):
 try:
  S,back=series_at(f,x,a,n)
 $<($h,$M,$B,$O):
  $!('series',f,x,n,a)
 $N=[]
 lnback=fn('ln',back)if $.(a=='$]' or a==('*',-1,'$]'))$( $o(fn('ln',fn('$I',x)))
 $) k in S[0]:
  if ncmp(k,n)>0:
   $7
  c=$W(S[0][k],LNT,lnback)
  $N.$%($9(c,pw(back,k)))
 $! $6($N)
$, dominant(f,x,a=0):
 if a=='$]' or a==('*',-1,'$]'):
  sub_=pw(TV,-1)if a=='$]' $( $o(pw(TV,-1))
  back=pw(x,-1)if a=='$]' $( $o(pw(x,-1))
  lnback=$o(fn('ln',fn('$I',x)))
 $(:
  sub_=$c(a,TV)
  back=$b(x,a)
  lnback=fn('ln',back)
 try:
  r=lead_t($W(f,x,sub_))
 $<($h,$M,$B,$O):
  $!('dominantterm',f,x,a)
 if r is $#:
  $! 0
 k,c=r
 $! $9($W(c,LNT,lnback),pw(back,k))
$, bern(n):
 B=[1]
 $) m in $*(1,n+1):
  s=0
  c=1
  $) k in $*(m):
   s=nadd(s,nmul(binom(m+1,k),B[k]))
  B.$%(nneg(ndiv(s,m+1)))
 $! B
$, binom(n,k):
 if k<0 or k>n:
  $! 0
 r=1
 $) i in $*(1,k+1):
  r=r*(n-k+i)//i
 $! r
$, powsum(j,n):
 B=bern(j)
 if j>=1:
  B[1]=Q(1,2)
 $N=[]
 $) i in $*(j+1):
  $N.$%($9(binom(j+1,i),B[i],pw(n,j+1-i)))
 $! $9(Q(1,j+1),$6($N))
ZETA={2:('Q',1,6),4:('Q',1,90),6:('Q',1,945),8:('Q',1,9450),10:('Q',1,93555)}
''')
_x(r'''$, sumseq(f,k,a,b):
 if $i(a)$+ $i(b):
  if b<a-1:
   $! $o(sumseq(f,k,b+1,a-1))
  if b-a<=300:
   $N=[$W(f,k,j)$) j in $*(a,b+1)]
   $! $6($N)
 if $8(f,k):
  $! $9(f,$c($b(b,a),1))
 cs_=$^(f,k)
 if cs_ is $. $# $+ b!='$]':
  res=[]
  $) j in $*($3(cs_)):
   if cs_[j]!=0:
    if j==0:
     res.$%($9(cs_[0],$c($b(b,a),1)))
    $(:
     res.$%($9(cs_[j],$b(powsum(j,b),powsum(j,$b(a,1)))))
  $! $;($6(res))
 r=geomsum(f,k,a,b)
 if r is $. $#:
  $! r
 r=telesum(f,k,a,b)
 if r is $. $#:
  $! r
 if b=='$]' $+ $i(a)$+ has(f,('fact',k)):
  g=$9(f,('fact',k))
  gs=geomsum(g,k,0,'$]')if $2 $( $#
  cr=expsum(g,k)
  if cr is $. $#:
   C,r=cr
   tot=$9(C,pw('e',r))
   if a>0:
    tot=$b(tot,$6([$9(C,$Y(pw(r,j),fact_(j)))$) j in $*(a)]))
   $! tot
 if b=='$]' $+ $i(a):
  nu,de=numer_denom(f)
  if $8(nu,k):
   dd=$^(de,k)
   if dd is $. $# $+ $3(dd)>=2 $+ all([c==0 $) c in dd[:-1]]):
    p=$3(dd)-1
    if p==1:
     $! '$]' if $S($Y(nu,dd[-1])).$Q>0 $(('*',-1,'$]')
    if p in ZETA $+ a>=1:
     z=$9(ZETA[p],pw('pi',p))
     z=$b(z,$6([pw(j,-p)$) j in $*(1,a)]))
     $! $9($Y(nu,dd[-1]),z)
 if($i(a)or $5(a))$+(b=='$]' or $i(b))$+ freeofall(f,[s $) s in ${(f)if s!=k]):
  $! nsum(f,k,a,b)
 $!('sumseq',f,k,a,b)
$, expsum(g,k):
 if $8(g,k):
  $! g,1
 fs=g[1:]if $&(g,'*')$((g,)
 C=[]
 r=$#
 $) h in fs:
  if $8(h,k):
   C.$%(h)
  $J $&(h,'^')$+ $8(h[1],k)$+ h[2]==k $+ r is $#:
   r=h[1]
  $J $&(h,'^')$+ $8(h[1],k)$+ $f(h[2],k)$+ $f(h[2],k)[1]==0 $+ r is $#:
   r=pw(h[1],$f(h[2],k)[0])
  $(:
   $! $#
 if r is $#:
  $! $#
 $! $E(C),r
$, geomsum(f,k,a,b):
 fs=f[1:]if $&(f,'*')$((f,)
 C=[]
 base=$#
 ex=$#
 $) g in fs:
  if $8(g,k):
   C.$%(g)
  $J $&(g,'^')$+ $8(g[1],k)$+ $f(g[2],k):
   if base is $. $#:
    if g[1]==base or($@(g[1])$+ $@(base)):
     lp=$f(g[2],k)
     lb=$f(ex,k)
     if lp[0]==1 $+ lb[0]==1:
      C.$%(pw(g[1],lp[1]))
      C.$%(pw(base,lb[1]))
      base=$9(base,g[1])
      ex=k
      $7
    $! $#
   base=g[1]
   ex=g[2]
  $(:
   $! $#
 if base is $#:
  $! $#
 p,q=$f(ex,k)
 r=pw(base,p)
 Cq=$9($E(C),pw(base,q))
 if b=='$]':
  if $5(r):
   v=$S(r)
   if $I(v)<1:
    $! $Y($9(Cq,pw(r,a)),$b(1,r))
   $! '$]' if $S(Cq).$Q>0 $+ v.$Q>0 $( '$L'
  $! $#
 if r==1:
  $! $9(Cq,$c($b(b,a),1))
 $! $Y($9(Cq,$b(pw(r,$c(b,1)),pw(r,a))),$b(r,1))
$, telesum(f,k,a,b):
 if $. hasdenom(f):
  $! $#
 pf=partfrac(f,k)
 if pf is $#:
  $! $#
 $N=pf[1:]if $&(pf,'+')$((pf,)
 groups=[]
 $) t in $N:
  c,r=$V(t)
  if $&(r,'^')$+ r[2]==-1:
   lb=$f(r[1],k)
   if lb is $# or lb[0]!=1:
    $! $#
   groups.$%((c,lb[1]))
  $J $8(t,k):
   $! $#
  $(:
   $! $#
 if $. groups:
  $! $#
 s0=groups[0][1]
 tot=0
 ms=[]
 $) c,s in groups:
  m=nsub(s,s0)if $m(s)$+ $m(s0)$( $#
  if m is $# or $. $i(m):
   $! $#
  ms.$%(m)
  tot=$c(tot,c)
 if tot!=0:
  if b=='$]':
   $! '$]'
  $! $#
 mn=min(ms)
 if mn!=0:
  s0=nadd(s0,mn)
  ms=[m-mn $) m in ms]
 M=max(ms)
 res=[]
 $) idx in $*($3(groups)):
  c=groups[idx][0]
  m=ms[idx]
  part=[]
  $) j in $*(m,M):
   part.$%(pw($c(a,j,s0),-1))
  if b!='$]':
   $) j in $*(1,m+1):
    part.$%(pw($c(b,j,s0),-1))
  res.$%($9(c,$6(part)))
 $! $6(res)
$, nsum(f,k,a,b):
 av=$q(nreal(a))
 if b=='$]':
  s=0.0
  prev=$#
  n=av
  chk=0
  $H n<av+200000:
   v=$S(f,{k:$C(n)})
   s+=v
   n+=1
   if n-av>50 $+ $I(v)<1e-15*(1+$I(s)):
    chk+=1
    if chk>20:
     $X
   $(:
    chk=0
  $! s
 s=0.0
 $) n in $*(av,$q(b)+1):
  s+=$S(f,{k:$C(n)})
 $! s
$, prodseq(f,k,a,b):
 if $i(a)$+ $i(b):
  if b<a-1:
   $! pw(prodseq(f,k,b+1,a-1),-1)
  if b-a<=300:
   $! $E([$W(f,k,j)$) j in $*(a,b+1)])
 if $8(f,k):
  $! pw(f,$c($b(b,a),1))
 if f==k $+ a==1:
  $! fn('fact',b)
 if $&(f,'^')$+ f[1]==k $+ $i(f[2])$+ a==1:
  $! pw(fn('fact',b),f[2])
 if $&(f,'*')$+ a==1:
  c=[g $) g in f[1:]if $8(g,k)]
  r=[g $) g in f[1:]if $. $8(g,k)]
  if c $+ $3(r)==1:
   rr=prodseq(r[0],k,a,b)
   if $. $&(rr,'prodseq'):
    $! $9(pw($E(c),b),rr)
 fs=f[1:]if $&(f,'*')$((f,)
 if $&(f,'^')$+ $8(f[1],k):
  $! pw(f[1],sumseq(f[2],k,a,b))
 $!('prodseq',f,k,a,b)
$, texpand(e):
 if $/(e)is $. $1 or e[0]=='Q':
  $! e
 $R=[texpand(a)$) a in e[1:]]
 e=simp((e[0],)+$1($R))
 if $/(e)is $. $1:
  $! e
 h=e[0]
 if h in('sin','cos','tan')$+ $3(e)==2:
  u=e[1]
  if h=='tan':
   $! texpand($Y(fn('sin',u),fn('cos',u)))
  if $&(u,'+'):
   a=u[1]
   b=$6($G(u[2:]))
   sa,ca=texpand(fn('sin',a)),texpand(fn('cos',a))
   sb,cb=texpand(fn('sin',b)),texpand(fn('cos',b))
   if h=='sin':
    $! $;($c($9(sa,cb),$9(ca,sb)))
   $! $;($b($9(ca,cb),$9(sa,sb)))
  c,r=$V(u)
  if $i(c)$+ c>1 $+ c<=30:
   s1=texpand(fn('sin',r))
   c1=texpand(fn('cos',r))
   z=expand_pow($c(c1,$9('i',s1)),c)
   re_,im_=reim(z)
   $! $;(im_ if h=='sin' $( re_)
 $! e
$, trigfactor(f):
 if head(f)in('sin','cos')$+ $3(f)==2:
  $![(f[0],f[1])]
 if $&(f,'^')$+ head(f[1])in('sin','cos')$+ $i(f[2])$+ f[2]>0:
  $![(f[1][0],f[1][1])]*f[2]
 $! $#
''')
_x(r'''$, tmul(a,b):
 n1,u=a
 n2,v=b
 if n1=='sin' $+ n2=='sin':
  $! $9($|,$b(fn('cos',$b(u,v)),fn('cos',$c(u,v))))
 if n1=='cos' $+ n2=='cos':
  $! $9($|,$c(fn('cos',$b(u,v)),fn('cos',$c(u,v))))
 if n1=='cos':
  u,v=v,u
 $! $9($|,$c(fn('sin',$c(u,v)),fn('sin',$b(u,v))))
$, tcollect(e):
 if $/(e)is $. $1 or e[0]=='Q':
  $! e
 e=$;(e)
 if $&(e,'+'):
  $! $6([tcollect_term(t)$) t in e[1:]])
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
 if $3(trig)<=1:
  $! t
 acc=fn(trig[0][0],trig[0][1])
 $) tf in trig[1:]:
  $N=acc[1:]if $&(acc,'+')$((acc,)
  $?=[]
  $) term in $N:
   c,r=$V(term)
   ftf=trigfactor(r)
   if ftf is $# or $3(ftf)!=1:
    if freeof_trig(r):
     $?.$%($9(term,fn(tf[0],tf[1])))
     $7
    $?.$%($9(term,fn(tf[0],tf[1])))
    $7
   $?.$%($9(c,tmul(ftf[0],tf)))
  acc=$;($6($?))
 $! $;($9($E(other),acc))
$, trigargs(e,$?):
 if $/(e)is $. $1 or e[0]=='Q':
  $!
 if e[0]in('sin','cos')$+ $3(e)==2:
  if e[1]$. in $?:
   $?.$%(e[1])
 $) a in e[1:]:
  trigargs(a,$?)
$, pyth(e):
 us=[]
 trigargs(e,us)
 if $. us:
  $! e
 $}=e
 bl=$3(fmt(e))
 $) u in us:
  s=fn('sin',u)
  c=fn('cos',u)
  $) a,b in((s,c),(c,s)):
   g=rsquare(e,a,b)
   if g is $. $#:
    g=$;(g)
    l=$3(fmt(g))
    if l<bl:
     $}=g
     bl=l
 $! $}
$, rsquare(e,a,b):
 if $/(e)is $. $1 or e[0]=='Q':
  $! e
 if e[0]=='^' $+ e[1]==a $+ $i(e[2])$+ e[2]>=2:
  $! $9(pw(a,e[2]-2),$b(1,pw(b,2)))
 $! simp((e[0],)+$1(rsquare(t,a,b)$) t in e[1:]))
$, freeof_trig(e):
 $! $. hastrig(e)
$, arclen(f,x,a,b):
 g=$-($;($c(1,pw(diff(f,x),2))))
 $! defint($T(g),x,a,b)
$, tangentline(f,x,a):
 d=$W(diff(f,x),x,a)
 $! $;($c($W(f,x,a),$9(d,$b(x,a))))
$, normalline(f,x,a):
 d=$W(diff(f,x),x,a)
 if d==0:
  $!('=',x,a)
 $! $;($b($W(f,x,a),$Y($b(x,a),d)))
$, impdif(eq,x,y,n=1):
 F=$b(eq[1],eq[2])if $&(eq,'=')$( eq
 yp=$-($o($Y(diff(F,x),diff(F,y))))
 d=yp
 $) _ in $*(n-1):
  d=$-($c(diff(d,x),$9(diff(d,y),yp)))
 $! nice(d)
$, avgrc(f,x,v,h=Q(1,1000)):
 $! $Y($b($W(f,x,$c(v,h)),$W(f,x,v)),h)
$, centraldiff(f,x,v,h=Q(1,1000)):
 $! $Y($b($W(f,x,$c(v,h)),$W(f,x,$b(v,h))),$9(2,h))
$, untan(e):
 if $/(e)is $. $1 or e[0]=='Q':
  $! e
 $R=[untan(a)$) a in e[1:]]
 if e[0]=='tan' $+ $3($R)==1:
  $! $Y(fn('sin',$R[0]),fn('cos',$R[0]))
 $! simp((e[0],)+$1($R))
$, pyth_to(e,which):
 other='cos' if which=='sin' $( 'sin'
 e=untan(e)
 us=[]
 trigargs(e,us)
 $) u in us:
  e=rsquare(e,fn(other,u),fn(which,u))
 $! $;(e)
''')
_x(r'''$, unhold(e):
 if $&(e,'hold'):
  $! simp(e[1])
 $! e
$, $y(e):
 if $. $5(e):
  $! $2
 try:
  v=$S(e)
 $< $=:
  $! $2
 if $/(v)is $0:
  $! $I(v.imag)<=1e-10*(1+$I(v.$Q))
 $! v==v
$, fv(e):
 v=$S(e)
 if $/(v)is $0:
  $! v.$Q
 $! v
$, clean(e):
 e=$-(e)
 if $`(e):
  e=evalf(e)
  if has(e,'i'):
   r,i=reim(e)
   if $/(i)is $C $+ $I(i)<1e-11*(1+$I(tofl(r)if $@(r)$( 1)):
    e=r
 $! e
class Sols:
 $, __init__($:):
  $:.$g=[]
  $:.all=$2
  $:.fail=$2
  $:.ints=[]
$, $x(f,x,$A=$2,$>=0):
 if $>>6:
  $! $#
 f=$-(unhold(f))
 if $8(f,x):
  if f==0:
   $! 'all'
  if $5(f)or $. $A:
   $![]
  $![]
 nu=numer_of(f)
 if $8(nu,x):
  $![]if nu!=0 $( 'all'
 $e=solve_num(nu,x,$A,$>)
 if $e is $# or $e=='all':
  $! $e
 $?=[]
 $) s in $e:
  if valid(f,x,s,$A):
   $?.$%(s)
 $! $?
$, numer_of(f):
 try:
  c=comdenom(f)
 $< $=:
  c=f
 $! numer_denom(c)[0]
$, valid(f,x,s,$A):
 if has(s,'n1')or ${(s)$+ $. $5(s):
  $! $F
 try:
  v=$W(f,x,s)
  if v=='$L' or has(v,'$L'):
   $! $2
  if has(v,'$]'):
   $! $2
  vv=$S(v)
  mag=1.0
  if $/(vv)is $0:
   ok=$I(vv)<1e-6
  $(:
   ok=$I(vv)<1e-6
  if $. ok:
   try:
    sc=$S(s)
    ok=$I(vv)<1e-8*(1+$I(sc))*1e4
   $< $=:
    ok=$2
  if $. $A:
   sv=$S(s)
   if $/(sv)is $0 $+ $I(sv.imag)>1e-9*(1+$I(sv.$Q)):
    $! $2
  $! ok
 $<($M,$B,$O,TypeError,$U):
  $! $2
$, solve_num(nu,x,$A,$>):
 d=degree(nu,x)
 if d is $. $#:
  r=solve_poly(nu,x,$A)
  if r is $. $#:
   $! r
 fac=$v(nu)
 fac=fac[1]if $&(fac,'hold')$( fac
 if $&(fac,'*'):
  allsol=[]
  $) g in fac[1:]:
   if $&(g,'^')$+ $@(g[2])$+ $a(g[2])>0:
    g=g[1]
   if $8(g,x):
    $7
   r=$x(g,x,$A,$>+1)
   if r is $#:
    $! numeric_solve(nu,x,$A)
   if r=='all':
    $! 'all'
   allsol.extend(r)
  $! dedup(allsol)
 if $&(fac,'^')$+ $@(fac[2])$+ $a(fac[2])>0:
  $! $x(fac[1],x,$A,$>+1)
 r=isolate(nu,0,x,$A,$>)
 if r is $. $#:
  $! r
 r=radical_solve(nu,x,$A,$>)
 if r is $. $#:
  $! r
 r=explog_solve(nu,x,$A,$>)
 if r is $. $#:
  $! r
 r=ln_solve(nu,x,$A,$>)
 if r is $. $#:
  $! r
 r=kernel_solve(nu,x,$A,$>)
 if r is $. $#:
  $! r
 if hastrigx(nu,x):
  g=texpand(nu)
  if g!=nu:
   r=kernel_solve(g,x,$A,$>+1)
   if r is $#:
    fg=$v(g)
    fg=fg[1]if $&(fg,'hold')$( fg
    if $&(fg,'*'):
     $! solve_num(g,x,$A,$>+1)
   if r is $. $#:
    $! r
  r=trig_lin(nu,x,$A)
  if r is $. $#:
   $! r
 $! numeric_solve(nu,x,$A)
$, radical_solve(nu,x,$A,$>):
 ks=[]
 xkernels(nu,x,ks)
 if $. ks:
  $! $#
 $) k in ks:
  if $.($&(k,'^')$+ isq(k[2])$+ k[2][1]==1):
   $! $#
 if $3(ks)>1:
  if $>>4 or $3(ks)>3:
   $! $#
  $) k in ks:
   if k[2]!=$|:
    $! $#
  k=ks[0]
  W='W_'
  g=$;($W(nu,k,W))
  cs_=$^(g,W)
  if cs_ is $# or $3(cs_)!=2:
   $! $#
  A,B=cs_
  g2=$;($b(pw(A,2),$9(pw(B,2),k[1])))
  rs=$x(g2,x,$A,$>+1)
  if rs is $# or rs=='all':
   $! $#
  $![r $) r in rs if valid(nu,x,r,$A)]
 k=ks[0]
 base=k[1]
 q=k[2][2]
 W='W_'
 g=$;($W(nu,k,W))
 cs_=$^(g,W)
 if cs_ is $# or $3(cs_)!=2 or has(cs_[0],W):
  $! $#
 A,B=cs_
 if degree(A,x)is $# or degree(B,x)is $# or degree(base,x)is $#:
  $! $#
 poly=$;($b(pw($o(A),q),$9(pw(B,q),base)))
 rs=solve_poly(poly,x,$A)
 if rs is $# or rs=='all':
  $! $#
 $?=[]
 $) r in rs:
  if valid(nu,x,r,$A):
   $?.$%(r)
 $! $?
$, expterm(t,x):
 fs=t[1:]if $&(t,'*')$((t,)
 c=[]
 L=[]
 $) f in fs:
  if $8(f,x):
   c.$%(f)
  $J $&(f,'^')$+ $8(f[1],x)$+ $f(f[2],x)is $. $# $+ $y(f[1])$+ fv(f[1])>0:
   L.$%($9(f[2],fn('ln',f[1]))if f[1]!='e' $( f[2])
  $(:
   $! $#
 $! $E(c),$6(L)
$, explog_solve(nu,x,$A,$>):
 if $. $&(nu,'+'):
  $! $#
 dep=[t $) t in nu[1:]if $. $8(t,x)]
 ind=$6([t $) t in nu[1:]if $8(t,x)])
 if $3(dep)==2 $+ ind==0:
  A=expterm(dep[0],x)
  B=expterm(dep[1],x)
  if A is $# or B is $#:
   $! $#
  r=$-($o($Y(B[0],A[0])))
  if $y(r)$+ fv(r)<=0 $+ $. $A:
   $![]
  eq=$;($b(A[1],$c(B[1],fn('ln',r))))
  lx=$f(eq,x)
  if lx is $#:
   $! $#
  $![nice($-($o($Y(lx[1],lx[0]))))]
 $! $#
$, ln_solve(nu,x,$A,$>):
 $N=nu[1:]if $&(nu,'+')$((nu,)
 lns=[]
 $_=[]
 $) t in $N:
  c,r=$V(t)
  if $&(r,'log')$+ $3(r)==3:
   c=$Y(c,fn('ln',r[2]))
   r=('ln',r[1])
  if $&(r,'ln')$+ $m(c)$+ $. $8(r,x):
   lns.$%((c,r[1]))
  $J $8(t,x):
   $_.$%(t)
  $J $&(r,'ln')$+ $5(c)$+ $. $8(r,x):
   lns.$%((c,r[1]))
  $(:
   $! $#
 if $3(lns)<2 $+ $.($3(lns)==1 $+ $_):
  $! $#
 k=rest_k=$6($_)
 c0=lns[0][0]
 if all([c==c0 $) c,u in lns]):
  P=$E([u $) c,u in lns])
  rhs=pw('e',$-($o($Y(rest_k,c0))))
 $J all([$m(c)$) c,u in lns]):
  P=$E([pw(u,c)$) c,u in lns])
  rhs=pw('e',$o(rest_k))
 $(:
  $! $#
 rs=$x($b(P,rhs),x,$A,$>+1)
 if rs is $# or rs=='all':
  $! rs
 $?=[]
 $) r in rs:
  if valid(nu,x,r,$A):
   $?.$%(r)
 $! $?
$, hastrigx(e,x):
 if $/(e)is $. $1 or e[0]=='Q':
  $! $2
 if e[0]in('sin','cos','tan')$+ has(e,x):
  $! $F
 $) a in e[1:]:
  if hastrigx(a,x):
   $! $F
 $! $2
''')
_x(r'''$, dedup($e):
 $?=[]
 $) s in $e:
  if s $. in $?:
   dup=$2
   $) t in $?:
    try:
     if $5(s)$+ $5(t)$+ $I($S(s)-$S(t))<1e-12*(1+$I($S(s))):
      dup=$F
      $X
    $< $=:
     pass
   if $. dup:
    $?.$%(s)
 $! $?
$, sortsols($e):
 $, key(s):
  t=s
  $) w in ${(s):
   if w[0]=='n' $+ w[1:].isdigit():
    t=$W(t,w,0)
  try:
   v=$S(t)
   if $/(v)is $0:
    $!(1,v.$Q,v.imag,okey(s))
   $!(0,v,0.0,okey(s))
  $< $=:
   $!(2,0.0,0.0,okey(s))
 $! sorted($e,key=key)
$, solve_poly(p,x,$A):
 cs=$^(p,x)
 if cs is $#:
  $! $#
 $H cs $+ cs[-1]==0:
  cs.pop()
 n=$3(cs)-1
 if n<=0:
  $![]if cs $+ cs[0]!=0 $( 'all'
 $e=[]
 k=0
 $H cs[k]==0:
  k+=1
 if k:
  $e.$%(0)
  cs=cs[k:]
  n=$3(cs)-1
 if n==0:
  $! $e
 allrat=$F
 anyfl=$2
 $) c in cs:
  if $. $m(c):
   allrat=$2
  if $`(c):
   anyfl=$F
 if anyfl $+ all([$5(c)$) c in cs]):
  $! $e+numroots(cs,$A)
 if allrat:
  cc,fs=ufactor(cs)
  $) g,m in fs:
   $e.extend(solve_small(g,x,$A))
  $! dedup($e)
 if n==1:
  $! $e+[$-($o($Y(cs[0],cs[1])))]
 if n==2:
  $! $e+quad(cs[2],cs[1],cs[0],$A)
 fac=$v(p,x)
 fac=fac[1]if $&(fac,'hold')$( fac
 if $&(fac,'*'):
  $) g in fac[1:]:
   if $&(g,'^')$+ $@(g[2]):
    g=g[1]
   if $8(g,x):
    $7
   dg=degree(g,x)
   if dg is $. $# $+ dg<n:
    r=solve_poly(g,x,$A)
    if r is $#:
     $! $#
    $e.extend(r)
   $(:
    $! $#
  $! dedup($e)
 r=solve_binom(cs,x,$A)
 if r is $. $#:
  $! $e+r
 if all([$5(c)$) c in cs]):
  $! $e+numroots(cs,$A)
 $! $#
$, quad(a,b,c,$A):
 D=$-($;($b($9(b,b),$9(4,a,c))))
 if $y(D)$+ $. $A:
  if fv(D)<0:
   $![]
 if D==0:
  $![$-($Y($o(b),$9(2,a)))]
 s=$T(D)
 r1=$-($Y($b($o(b),s),$9(2,a)))
 r2=$-($Y($c($o(b),s),$9(2,a)))
 if $5(r1):
  r1=$;(r1)
  r2=$;(r2)
 $![r1,r2]
$, solve_small(g,x,$A):
 n=$3(g)-1
 if n==1:
  $![Q(-g[0],g[1])]
 if n==2:
  $! quad(g[2],g[1],g[0],$A)
 r=solve_binom(g,x,$A)
 if r is $. $#:
  $! r
 if n==3:
  r=cardano(g,$A)
  if r is $. $#:
   if $3(fmt(r[0]))<=32:
    $! r
 $! numroots(g,$A)
$, solve_binom(cs,x,$A):
 n=$3(cs)-1
 m=0
 $) i in $*(1,n+1):
  if cs[i]!=0:
   m=igcd(m,i)
 if m<=1:
  $! $#
 sub_cs=[cs[i]$) i in $*(0,n+1,m)]
 if $3(sub_cs)-1>2 $+ $.($3([c $) c in sub_cs if c!=0])==2):
  $! $#
 u='U_'
 if $3(sub_cs)==2:
  roots_u=[$-($o($Y(sub_cs[0],sub_cs[1])))]
 $(:
  roots_u=solve_poly(fromcoeffs(sub_cs,u),u,$A)
  if roots_u is $#:
   $! $#
 $?=[]
 $) r in roots_u:
  $?.extend(nthroots(r,m,$A))
 $! dedup($?)
$, nthroots(r,m,$A):
 if $. $A:
  if $y(r):
   v=fv(r)
   if m%2==1:
    if v<0:
     $![$o(pw($o(r),Q(1,m)))]
    $![pw(r,Q(1,m))]
   if v<0:
    $![]
   if v==0:
    $![0]
   rt=pw(r,Q(1,m))
   $![$o(rt),rt]
  if m%2==1:
   $![pw(r,Q(1,m))]
  rt=pw(r,Q(1,m))
  $![$o(rt),rt]
 if $5(r):
  v=$S(r)
  mod=fn('$I',r)
  ang=fn('$p',r)
  $?=[]
  $) k in $*(m):
   th=$Y($c(ang,$9(2*k,'pi')),m)
   z=$9(pw(mod,Q(1,m)),$c(fn('cos',th),$9('i',fn('sin',th))))
   z=$;(z)
   $?.$%(z)
  $! $?
 rt=pw(r,Q(1,m))
 $![$9(rt,pw('e',$Y($9(2*k,'i','pi'),m)))$) k in $*(m)]
$, cardano(g,$A):
 d,c,b,a=[Q(v)if $/(v)is $q $( v $) v in g]
 p=$Y($b($9(3,a,c),$9(b,b)),$9(3,a,a))
 q=$Y($c($9(2,pw(b,3)),$9(-9,a,b,c),$9(27,a,a,d)),$9(27,pw(a,3)))
 disc=$c($Y(pw(q,2),4),$Y(pw(p,3),27))
 if $. $m(disc)or $a(disc)<=0:
  $! $#
 s=$T(disc)
 u=$c($o($Y(q,2)),s)
 v=$b($o($Y(q,2)),s)
 $, cbrt(w):
  wv=fv(w)
  if wv<0:
   $! $o(pw($o(w),Q(1,3)))
  $! pw(w,Q(1,3))
 t=$c(cbrt(u),cbrt(v))
 root=$b(t,$Y(b,$9(3,a)))
 if $. $A:
  $![root]
 $![root]+[clean(r)$) r in numroots_after(g,root)]
$, numroots_after(g,root):
 rv=fv(root)
 rs=aberth(g)
 $![fromcomplex(z)$) z in rs if $I(z-rv)>1e-6]
$, numroots(cs,$A):
 rs=aberth([evalf(c)if $. $@(c)$( c $) c in cs])
 $?=[]
 $) z in rs:
  if $I(z.imag)<1e-9*(1+$I(z.$Q)):
   $?.$%($C(z.$Q))
  $J $A:
   $?.$%(fromcomplex(z))
 $! $?
NC=[0]
$, newint():
 NC[0]+=1
 $! 'n'+$u(NC[0])
''')
_x(r'''$, isolate(lhs,rhs,x,$A,$>):
 if $>>12:
  $! $#
 if lhs==x:
  $![rhs]
 if $8(lhs,x):
  $! 'all' if $-($b(lhs,rhs))==0 $([]
 h=head(lhs)
 if h=='+':
  dep=[t $) t in lhs[1:]if $. $8(t,x)]
  ind=[t $) t in lhs[1:]if $8(t,x)]
  if $3(dep)==1:
   $! isolate(dep[0],$b(rhs,$6(ind)),x,$A,$>+1)
  $! $#
 if h=='*':
  dep=[t $) t in lhs[1:]if $. $8(t,x)]
  ind=[t $) t in lhs[1:]if $8(t,x)]
  if $3(dep)==1:
   c=$E(ind)
   r=$Y(rhs,c)
   if $5(c)$+ $&(rhs,'+'):
    r=$;(r)
   $! isolate(dep[0],r,x,$A,$>+1)
  $! $#
 if h=='^':
  b,p=lhs[1],lhs[2]
  if $8(p,x):
   if p==-1 or($@(p)$+ $a(p)<0):
    if rhs==0:
     $![]
    $! isolate(pw(b,nneg(p)),pw(rhs,-1),x,$A,$>+1)
   if $/(p)is $q:
    $?=[]
    $) r in nthroots(rhs,p,$A):
     rr=isolate(b,r,x,$A,$>+1)
     if rr is $#:
      $! $#
     if rr=='all':
      $! 'all'
     $?.extend(rr)
    $! $?
   if isq(p):
    pn,pd=p[1],p[2]
    if pd%2==0 $+ $. $A $+ $y(rhs)$+ fv(rhs)<0:
     $![]
    $! isolate(pw(b,pn),pw(rhs,pd),x,$A,$>+1)
   $! isolate(b,pw(rhs,pw(p,-1)),x,$A,$>+1)
  if $8(b,x):
   if rhs==0:
    $![]
   if $. $A $+ $y(rhs)$+ fv(rhs)<0 $+ $y(b)$+ fv(b)>0:
    $![]
   if b=='e':
    $! isolate(p,fn('ln',rhs),x,$A,$>+1)
   if $@(b)$+ $5(rhs):
    $! isolate(p,fn('log',rhs,b),x,$A,$>+1)
   $! isolate(p,$Y(fn('ln',rhs),fn('ln',b)),x,$A,$>+1)
  $! $#
 if $/(lhs)is $1 $+ $3(lhs)>=2:
  u=lhs[1]
  if $. all([$8(a,x)$) a in lhs[2:]]):
   $! $#
  rs=invfun(h,lhs,rhs,$A)
  if rs is $#:
   $! $#
  $?=[]
  $) r in rs:
   rr=isolate(u,r,x,$A,$>+1)
   if rr is $#:
    $! $#
   if rr=='all':
    $! 'all'
   $?.extend(rr)
  $! $?
 $! $#
$, invfun(h,lhs,r,$A):
 rv=$#
 if $y(r):
  rv=fv(r)
 if h=='ln':
  $![pw('e',r)]
 if h=='log':
  b=lhs[2]if $3(lhs)>2 $( 10
  $![pw(b,r)]
 if h=='$I':
  if rv is $. $#:
   if rv<0:
    $![]
   if rv==0:
    $![0]
  $![$o(r),r]
 if h=='$T':
  $![pw(r,2)]
 if h=='sin':
  if rv is $. $# $+ $I(rv)>1 $+ $. $A:
   $![]
  n=newint()
  if r==0:
   $![$9(n,'pi')]
  a=fn('$w',r)
  if r==1 or r==-1:
   $![$c(a,$9(2,n,'pi'))]
  $![$c(a,$9(2,n,'pi')),$c($b('pi',a),$9(2,n,'pi'))]
 if h=='cos':
  if rv is $. $# $+ $I(rv)>1 $+ $. $A:
   $![]
  n=newint()
  if r==0:
   $![$c($9($|,'pi'),$9(n,'pi'))]
  a=fn('arccos',r)
  if r==1 or r==-1:
   $![$c(a,$9(2,n,'pi'))]
  $![$c(a,$9(2,n,'pi')),$c($o(a),$9(2,n,'pi'))]
 if h=='tan':
  n=newint()
  $![$c(fn('$t',r),$9(n,'pi'))]
 if h=='$w':
  if rv is $. $# $+ $I(rv)>$P.pi/2+1e-12:
   $![]
  $![fn('sin',r)]
 if h=='arccos':
  if rv is $. $# $+(rv<-1e-12 or rv>$P.pi+1e-12):
   $![]
  $![fn('cos',r)]
 if h=='$t':
  if rv is $. $# $+ $I(rv)>=$P.pi/2:
   $![]
  $![fn('tan',r)]
 if h=='sinh':
  $![fn('arcsinh',r)]
 if h=='cosh':
  if rv is $. $# $+ rv<1:
   $![]
  a=fn('arccosh',r)
  $![$o(a),a]
 if h=='tanh':
  if rv is $. $# $+ $I(rv)>=1:
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
 if $/(e)is $. $1 or e[0]=='Q' or $8(e,x):
  $!
 h=e[0]
 if h in('+','*'):
  $) a in e[1:]:
   xkernels(a,x,$?)
  $!
 if h=='^' $+ $/(e[2])is $q:
  xkernels(e[1],x,$?)
  $!
 if h=='^' $+ isq(e[2])$+ e[1]==x:
  k=pw(x,Q(1,e[2][2]))
  if k $. in $?:
   $?.$%(k)
  $!
 if e $. in $?:
  $?.$%(e)
$, kernel_solve(nu,x,$A,$>):
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
    if $8(g2,x):
     rs=$x(g2,W,$A,$>+1)
     if rs is $# or rs=='all':
      $! rs
     $?=[]
     $) r in rs:
      rr=isolate(pw(base,$9(gg,x)),r,x,$A,$>+1)
      if rr is $#:
       $! $#
      $?.extend(rr)
     $! $?
 ks=[]
 xkernels(g,x,ks)
 if $3(ks)==1 $+ ks[0]!=x:
  k=ks[0]
  g2=$W(g,k,W)
  if $8(g2,x):
   rs=$x(g2,W,$A,$>+1)
   if rs is $# or rs=='all':
    $! rs
   $?=[]
   $) r in rs:
    rr=isolate(k,r,x,$A,$>+1)
    if rr is $#:
     $! $#
    if rr=='all':
     $! 'all'
    $?.extend(rr)
   $! $?
 if $3(ks)==2:
  names=sorted([head(k)$) k in ks])
  if names==['cos','sin']$+ ks[0][1]==ks[1][1]:
   u=ks[0][1]
   s=fn('sin',u)
   c=fn('cos',u)
   $) a,b in((c,s),(s,c)):
    g2=$;(g)
    cc=$^($W(g2,a,W),W)
    if cc is $. $# $+ all([cc[i]==0 $) i in $*(1,$3(cc),2)]):
     g3=$;($W($W(g2,a,W),W,$T($b(1,pw(b,2)))))
     if $. has(g3,a):
      $! kernel_solve(g3,x,$A,$>+1)if $><4 $( $#
 $! $#
$, rgcd(a,b):
 if $m(a)$+ $m(b):
  an,ad=nd(a)
  bn,bd=nd(b)
  $! Q(igcd(an,bn),ilcm(ad,bd))
 $! a if a==b $( 0
$, findexp(e,x,$?):
 if $/(e)is $. $1 or e[0]=='Q':
  $!
 if e[0]=='^' $+ $8(e[1],x)$+ $. $8(e[2],x):
  l=$f(e[2],x)
  if l is $. $#:
   $?.$%((e[1],l[0],l[1]))
   $!
  $?.$%(($#,0,0))
  $!
 $) a in e[1:]:
  findexp(a,x,$?)
$, repl_exp(e,x,base,gg,W):
 if $/(e)is $. $1 or e[0]=='Q':
  $! e
 if e[0]=='^' $+ e[1]==base $+ $. $8(e[2],x):
  l=$f(e[2],x)
  if l is $. $#:
   $! $9(pw(base,l[1]),pw(W,$Y(l[0],gg)))
 $! simp((e[0],)+$1(repl_exp(a,x,base,gg,W)$) a in e[1:]))
''')
_x(r'''$, trig_lin(nu,x,$A):
 ks=[]
 xkernels(nu,x,ks)
 if $3(ks)!=2:
  $! $#
 names=sorted([head(k)$) k in ks])
 if names!=['cos','sin']or ks[0][1]!=ks[1][1]:
  $! $#
 u=ks[0][1]
 S='S_'
 C='C_'
 g=$;($W($W(nu,fn('sin',u),S),fn('cos',u),C))
 if has(g,x):
  $! $#
 cs_s=$^(g,S)
 if cs_s is $# or $3(cs_s)!=2:
  $! $#
 a=cs_s[1]
 $_=cs_s[0]
 cc=$^($_,C)
 if cc is $# or $3(cc)!=2 or has(a,C):
  $! $#
 b=cc[1]
 c=cc[0]
 if c==0:
  $! isolate(fn('tan',u),$-($o($Y(b,a))),x,$A,0)
 R=$T($c(pw(a,2),pw(b,2)))
 phi=fn('$t',$Y(b,a))
 if $y(a)$+ fv(a)<0:
  phi=$c(phi,'pi')
 $! isolate(fn('sin',$c(u,phi)),$-($o($Y(c,R))),x,$A,0)
$, numeric_solve(f,x,$A,lo=$#,hi=$#,maxn=12):
 others=[s $) s in ${(f)if s!=x]
 if others:
  $! $#
 $, F(t):
  try:
   v=$S(f,{x:t})
  $<($B,$O,$U,$M,TypeError):
   $! $#
  if $/(v)is $0:
   if $I(v.imag)>1e-9*(1+$I(v.$Q)):
    $! $#
   v=v.$Q
  if v!=v:
   $! $#
  $! v
 pts=[]
 if lo is $. $# $+ hi is $. $#:
  N=400
  $) i in $*(N+1):
   pts.$%(lo+(hi-lo)*i/N)
 $(:
  $) i in $*(-400,401):
   pts.$%(i*0.05)
  $) k in $*(-40,61):
   v=10**(k/10.0)
   if v>20:
    pts.$%(v)
    pts.$%(-v)
  pts.sort()
 roots=[]
 prev=$#
 pv=$#
 vals0=[F(t)$) t in pts]
 $) k in $*($3(pts)):
  t=pts[k]
  v=vals0[k]
  if v is $. $# $+ v==0:
   a=vals0[k-1]if k>0 $( $#
   b=vals0[k+1]if k+1<$3(pts)$( $#
   if(a is $. $# $+ a!=0)or(b is $. $# $+ b!=0):
    roots.$%(t)
  $J v is $. $# $+ pv is $. $# $+ v!=0 $+ pv!=0 $+(v<0)!=(pv<0):
   r=bisect(F,prev,t,pv,v)
   if r is $. $#:
    roots.$%(r)
  prev=t
  pv=v
  if $3(roots)>40:
   $X
 $g=[(pts[k],vals0[k])$) k in $*($3(pts))]
 $) i in $*(1,$3($g)-1):
  t0,a=$g[i-1]
  t1,b=$g[i]
  t2,c=$g[i+1]
  if a is $# or b is $# or c is $#:
   $7
  if b!=0 $+ $I(b)<$I(a)$+ $I(b)<$I(c)$+(a>0)==(b>0)==(c>0)$+ $I(b)<1e-2:
   r=newton(F,t1)
   if r is $. $# $+ t0<=r<=t2:
    roots.$%(r)
 $?=[]
 $) r in sorted(roots):
  if $. $? or $I(r-$?[-1])>1e-9*(1+$I(r)):
   $?.$%(r)
 if $3($?)>maxn $+ lo is $#:
  $?=$?[:maxn]
 $![snap(r)$) r in $?]
$, snap(r):
 if $I(r-round(r))<1e-12:
  $! $C(round(r))
 $! r
$, bisect(F,a,b,fa,fb):
 $) _ in $*(200):
  m=0.5*(a+b)
  fm=F(m)
  if fm is $#:
   $! $#
  if fm==0 or $I(b-a)<1e-15*(1+$I(m)):
   $X
  if(fm<0)==(fa<0):
   a,fa=m,fm
  $(:
   b,fb=m,fm
 m=0.5*(a+b)
 fm=F(m)
 if fm is $# or $I(fm)>1e-6*(1+$I(fa)+$I(fb)):
  if fm is $. $# $+ $I(fm)>1e3:
   $! $#
 $! m
$, newton(F,t):
 $) _ in $*(60):
  v=F(t)
  if v is $#:
   $! $#
  h=1e-7*(1+$I(t))
  v2=F(t+h)
  if v2 is $#:
   $! $#
  d=(v2-v)/h
  if d==0:
   $X
  t2=t-v/d
  if $I(t2-t)<1e-14*(1+$I(t)):
   t=t2
   $X
  t=t2
 v=F(t)
 if v is $. $# $+ $I(v)<1e-9:
  $! t
 $! $#
$, nsolve(f,x,guess=$#,lo=$#,hi=$#):
 $, F(t):
  try:
   v=$S(f,{x:t})
  $<($B,$O,$U,$M,TypeError):
   $! $#
  if $/(v)is $0:
   if $I(v.imag)>1e-9*(1+$I(v.$Q)):
    $! $#
   v=v.$Q
  $! v
 if guess is $. $#:
  r=secant(F,guess,lo,hi)
  if r is $. $#:
   $! r
 if lo is $. $# $+ hi is $. $#:
  rs=numeric_solve(f,x,$2,lo,hi)
 $(:
  rs=numeric_solve(f,x,$2)
  if lo is $. $#:
   rs=[r $) r in rs if r>=lo]
  if hi is $. $#:
   rs=[r $) r in rs if r<=hi]
 if rs:
  if guess is $. $#:
   rs.sort(key=$4 r:$I(r-guess))
  $(:
   rs.sort(key=$4 r:$I(r))
  $! rs[0]
 $! $#
$, secant(F,g,lo,hi):
 t=g
 r=newton(F,t)
 if r is $. $# $+(lo is $# or r>=lo)$+(hi is $# or r<=hi):
  $! r
 $! $#
FLIP={'<':'>','>':'<','<=':'>=','>=':'<=','/=':'/='}
$, solve_ineq(rel,f,x):
 f=$-(f)
 if $. $5($W(f,x,0))or $. $5(diff(f,x)):
  r=ineq_param(rel,f,x)
  if r is $. $#:
   $! r
 pts=[]
 rs=$x(f,x,$2)
 if rs is $#:
  $! $#
 if rs=='all':
  rs=[]
 $) r in rs:
  if $. $y(r):
   $! $#
  pts.$%(r)
 dens=[]
 domainpts(f,x,dens)
 $) d in dens:
  r2=$x(d,x,$2)
  if r2 is $# or r2=='all':
   $7
  $) r in r2:
   if $y(r):
    pts.$%(r)
   $(:
    $! $#
 pts=dedup(pts)
 pts=sortsols(pts)
 $, test(t):
  try:
   v=$S(f,{x:t})
  $< $=:
   $! $2
  if $/(v)is $0:
   if $I(v.imag)>1e-9*(1+$I(v.$Q)):
    $! $2
   v=v.$Q
  if v!=v:
   $! $2
  $! relok(rel,v)
 $g=[fv(p)$) p in pts]
 segs=[]
 if $. $g:
  ok=test(0.5)
  $! 'true' if ok $( 'false'
 first=$g[0]-max(1.0,$I($g[0]))
 segs.$%(('I',$#,pts[0],test(first)))
 $) i in $*($3(pts)):
  p=pts[i]
  okp=$2
  try:
   v=$W(f,x,p)
   if v!='$L' $+ $. has(v,'$L')$+ $. has(v,'$]'):
    vv=$S(v)
    if $/(vv)is $0:
     vv=vv.$Q if $I(vv.imag)<1e-9 $( $#
    if vv is $. $#:
     if $I(vv)<1e-10:
      vv=0.0
     okp=relok(rel,vv)
  $< $=:
   okp=$2
  segs.$%(('P',p,p,okp))
  if i+1<$3(pts):
   m=0.5*($g[i]+$g[i+1])
   segs.$%(('I',p,pts[i+1],test(m)))
 last=$g[-1]+max(1.0,$I($g[-1]))
 segs.$%(('I',pts[-1],$#,test(last)))
 $! segs_to_bool(segs,x)
''')
_x(r'''$, sgn(e):
 if $5(e):
  try:
   v=fv(e)
  $< $=:
   $! 0
  $! 1 if v>0 $((-1 if v<0 $( 0)
 if $&(e,'*'):
  s=1
  $) a in e[1:]:
   k=sgn(a)
   if $. k:
    $! 0
   s*=k
  $! s
 if $&(e,'+'):
  ks=[sgn(a)or(2 if nonneg(a)$( 0)$) a in e[1:]]
  if all(k in(1,2)$) k in ks)$+ 1 in ks:
   $! 1
  ks=[sgn($o(a))or(2 if nonneg($o(a))$( 0)$) a in e[1:]]
  if all(k in(1,2)$) k in ks)$+ 1 in ks:
   $!-1
  $! 0
 if $&(e,'^')$+ $i(e[2])$+ e[2]%2==1:
  $! sgn(e[1])
 if head(e)=='exp' or($&(e,'^')$+ e[1]=='e'):
  $! 1
 $! 0
$, nonneg(e):
 if $&(e,'^')$+ $i(e[2])$+ e[2]%2==0:
  $! $F
 if head(e)=='$I':
  $! $F
 if $&(e,'*'):
  $! all(nonneg(a)or sgn(a)>0 $) a in e[1:])
 $! sgn(e)>0
$, ineq_param(rel,f,x):
 cs=$^(f,x)
 if cs is $# or $3(cs)!=2:
  $! $#
 a=nice(comdenom(cs[1]))
 b=cs[0]
 v=nice(comdenom($Y($o(b),a)))
 k=sgn(a)
 if k:
  $!(rel if k>0 $( FLIP[rel],x,v)
 n=numer_denom(a)[0]
 if rel=='/=':
  $?=[('$+',('/=',x,v),('/=',n,0))]
 $(:
  $?=[('$+',(rel,x,v),('>',a,0)),
 ('$+',(FLIP[rel],x,v),('<',a,0))]
 if $/(n)is $u:
  b=$W(b,n,0)
 if $5(b):
  if relok(rel,fv(b)):
   $?.$%(('=',n,0))
 $(:
  $?.$%(('$+',('=',n,0),(rel,b,0)))
 $!('or',)+$1($?)if $3($?)>1 $( $?[0]
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
 if $/(f)is $. $1 or f[0]=='Q':
  $!
 h=f[0]
 if h=='^' $+ $. $8(f[1],x):
  if $@(f[2])$+ $a(f[2])<0:
   $?.$%(f[1])
  if isq(f[2])$+ f[2][2]%2==0:
   $?.$%(f[1])
 if h in('ln','log','$I','sign','floor','ceiling')$+ $. $8(f[1],x):
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
     cur=[a,$2,b,$2]
    $(:
     cur=[a,$F,b,$F]
   $(:
    cur[2]=b
    cur[3]=(kind=='P')
  $(:
   if cur is $. $#:
    ivs.$%(cur)
    cur=$#
 if cur is $. $#:
  ivs.$%(cur)
 if $. ivs:
  $! 'false'
 if $3(ivs)>=2 $+ ivs[0][0]is $# $+ ivs[-1][2]is $#:
  okp=$F
  $) i in $*($3(ivs)-1):
   if $.(ivs[i][2]==ivs[i+1][0]$+ $. ivs[i][3]$+ $. ivs[i+1][1]):
    okp=$2
  if okp:
   ne=[('/=',x,ivs[i][2])$) i in $*($3(ivs)-1)]
   $! ne[0]if $3(ne)==1 $(('$+',)+$1(ne)
 $?=[]
 $) lo,li,hi,hiinc in ivs:
  if lo is $# $+ hi is $#:
   $! 'true'
  if lo is $. $# $+ hi is $. $# $+ lo==hi:
   $?.$%(('=',x,lo))
  $J lo is $#:
   $?.$%(('<=' if hiinc $( '<',x,hi))
  $J hi is $#:
   $?.$%(('>=' if li $( '>',x,lo))
  $(:
   $?.$%(('$+',('<=' if li $( '<',lo,x),('<=' if hiinc $( '<',x,hi)))
 if $3($?)==1:
  $! $?[0]
 $!('or',)+$1($?)
$, eqexpr(eq):
 if $&(eq,'='):
  $! $-($b(eq[1],eq[2]))
 $! eq
$, is_linear_sys(fs,vs):
 $) f in fs:
  $) v in vs:
   d=degree(f,v)
   if d is $# or d>1:
    $! $2
  g=$;(f)
  $) i in $*($3(vs)):
   $) j in $*($3(vs)):
    cs_=$^(g,vs[i])
    if cs_ is $#:
     $! $2
    if $3(cs_)>1 $+ has(cs_[1],vs[j]):
     $! $2
 $! $F
$, linsys(fs,vs):
 m=$3(fs)
 n=$3(vs)
 A=[]
 $) f in fs:
  g=$;(f)
  row=[]
  $_=g
  $) v in vs:
   cs_=$^(g,v)
   c=cs_[1]if $3(cs_)>1 $( 0
   row.$%(c)
  const=g
  $) v in vs:
   const=$W(const,v,0)
  row.$%($o(const))
  A.$%(row)
 piv=[]
 r=0
 $) c in $*(n):
  p=$#
  $) i in $*(r,m):
   if $-(A[i][c])!=0:
    p=i
    $X
  if p is $#:
   $7
  A[r],A[p]=A[p],A[r]
  pv=A[r][c]
  A[r]=[$-($Y(a,pv))$) a in A[r]]
  $) i in $*(m):
   if i!=r $+ A[i][c]!=0:
    fct=A[i][c]
    A[i]=[$-($;($b(A[i][j],$9(fct,A[r][j]))))$) j in $*(n+1)]
  piv.$%(c)
  r+=1
  if r==m:
   $X
 $) i in $*(r,m):
  if $-(A[i][n])!=0:
   $![]
 sol={}
 free=[c $) c in $*(n)if c $. in piv]
 params={}
 k=1
 $) c in free:
  params[vs[c]]='c'+$u(k)
  k+=1
 $) i in $*($3(piv)):
  c=piv[i]
  val=A[i][n]
  $) c2 in free:
   val=$b(val,$9(A[i][c2],params[vs[c2]]))
  sol[vs[c]]=nice($-(val))
 $) c in free:
  sol[vs[c]]=params[vs[c]]
 $![sol]
$, solve_system(eqs,vs,$A=$2,guesses=$#):
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
 r=elim(fs,vs,$A,0)
 if r is $#:
  $! newton_sys(fs,vs,[0.0]*$3(vs))
 $?=[]
 $) s in r:
  ok=$F
  $) v in vs:
   if v $. in s:
    s[v]=v
  if $. $A:
   $) v in vs:
    if $5(s[v])$+ $. $y(s[v]):
     ok=$2
  if ok $+ s $. in $?:
   $?.$%(s)
 $! $?
$, hasdenom_x(f,vs):
 $) v in vs:
  nu,de=numer_denom(f)
  if has(de,v):
   $! $F
 $! $2
''')
_x(r'''$, elim(fs,vs,$A,$>):
 fs=[$-($;(f))$) f in fs]
 fs=[f $) f in fs if f!=0]
 if $. fs:
  $![{}]
 $) f in fs:
  if freeofall(f,vs):
   if $5(f)or f!=0:
    $![]
 if $>>8:
  $! $#
 $}=$#
 $) f in fs:
  inv=[v $) v in vs if has(f,v)]
  if $3(inv)==1:
   $}=(f,inv[0])
   $X
 if $} is $#:
  $) f in fs:
   $) v in vs:
    d=degree(f,v)
    if d==1:
     c=$^(f,v)
     if c is $. $# $+ $5(c[1])$+ c[1]!=0:
      $}=(f,v)
      $X
   if $}:
    $X
 if $} is $#:
  $) f in fs:
   $) v in vs:
    if degree(f,v)==1:
     $}=(f,v)
     $X
   if $}:
    $X
 if $} is $. $#:
  f,v=$}
  rs=$x(f,v,$A)
  if rs is $#:
   $! $#
  if rs=='all':
   rs=[]
  $?=[]
  $_=[g $) g in fs if g is $. f]
  ovs=[w $) w in vs if w!=v]
  $) r in rs:
   sub_=[$-($W(g,v,r))$) g in $_]
   rr=elim(sub_,ovs,$A,$>+1)
   if rr is $#:
    $! $#
   $) s in rr:
    s2=dict(s)
    val=r
    $) w in s2:
     val=$W(val,w,s2[w])
    s2[v]=clean(val)
    $?.$%(s2)
  $! $?
 if $3(fs)>=2 $+ $3(vs)>=2:
  y=vs[-1]
  R=resultant(fs[0],fs[1],y)
  if R is $# or R==0:
   $! $#
  rr=elim([R]+fs[2:],vs[:-1],$A,$>+1)
  if rr is $#:
   $! $#
  $?=[]
  $) s in rr:
   gs=[]
   $) g in fs:
    h=g
    $) w in s:
     h=$W(h,w,s[w])
    gs.$%($-($;(h)))
   ys=elim(gs,[y],$A,$>+1)
   if ys is $#:
    $7
   $) t in ys:
    s2=dict(s)
    s2.update(t)
    $?.$%(s2)
  $! $?
 $! $#
$, resultant(f,g,y):
 a=$^(f,y)
 b=$^(g,y)
 if a is $# or b is $#:
  $! $#
 m=$3(a)-1
 n=$3(b)-1
 if m<1 or n<1:
  $! $#
 N=m+n
 M=[]
 $) i in $*(n):
  row=[0]*N
  $) j in $*(m+1):
   row[i+j]=a[m-j]
  M.$%(row)
 $) i in $*(m):
  row=[0]*N
  $) j in $*(n+1):
   row[i+j]=b[n-j]
  M.$%(row)
 $! $;(bareiss(M))
$, bareiss(M):
 n=$3(M)
 M=[$G(r)$) r in M]
 sign=1
 prev=1
 $) k in $*(n-1):
  if M[k][k]==0:
   sw=$#
   $) i in $*(k+1,n):
    if M[i][k]!=0:
     sw=i
     $X
   if sw is $#:
    $! 0
   M[k],M[sw]=M[sw],M[k]
   sign=-sign
  $) i in $*(k+1,n):
   $) j in $*(k+1,n):
    num=$;($b($9(M[i][j],M[k][k]),$9(M[i][k],M[k][j])))
    M[i][j]=exdiv(num,prev)
  prev=M[k][k]
 $! $9(sign,M[n-1][n-1])
$, exdiv(a,b):
 if b==1:
  $! a
 if $@(b):
  $! $;($9(a,ninv(b))if $m(b)$( $Y(a,b))
 ks=[]
 kernels(a,ks)
 kernels(b,ks)
 sortkernels(ks)
 ra=ratform(a,ks)
 rb=ratform(b,ks)
 if ra is $# or rb is $#:
  $! $-($Y(a,b))
 q=$K(p_mul(ra[0],rb[1]),p_mul(ra[1],rb[0]))
 if q is $#:
  $! $-($Y(a,b))
 $! p2e(q,ks)
$, newton_sys(fs,vs,guess):
 n=$3(vs)
 if $3(fs)!=n:
  $! $#
 others=[]
 $) f in fs:
  $) s in ${(f):
   if s $. in vs:
    $! $#
 J=[[diff(f,v)$) v in vs]$) f in fs]
 xv=[$C($S(g).$Q)if $@(g)or $5(g)$( 0.0 $) g in guess]
 $) it in $*(100):
  env=dict(zip(vs,xv))
  try:
   F=[$S(f,env)$) f in fs]
   Jv=[[$S(J[i][j],env)$) j in $*(n)]$) i in $*(n)]
  $< $=:
   $! $#
  F=[v.$Q if $/(v)is $0 $( v $) v in F]
  Jv=[[v.$Q if $/(v)is $0 $( v $) v in r]$) r in Jv]
  dx=linsolve_float(Jv,[-v $) v in F])
  if dx is $#:
   $! $#
  xv=[xv[i]+dx[i]$) i in $*(n)]
  if max([$I(d)$) d in dx])<1e-13*(1+max([$I(v)$) v in xv])):
   $X
 env=dict(zip(vs,xv))
 try:
  if max([$I($S(f,env))$) f in fs])>1e-8:
   $![]
 $< $=:
  $![]
 $![dict([(vs[i],snap(xv[i]))$) i in $*(n)])]
$, linsolve_float(A,b):
 n=$3(A)
 M=[$G(A[i])+[b[i]]$) i in $*(n)]
 $) c in $*(n):
  p=max($*(c,n),key=$4 i:$I(M[i][c]))
  if $I(M[p][c])<1e-300:
   $! $#
  M[c],M[p]=M[p],M[c]
  $) i in $*(n):
   if i!=c:
    f=M[i][c]/M[c][c]
    $) j in $*(c,n+1):
     M[i][j]-=f*M[c][j]
 $![M[i][n]/M[i][i]$) i in $*(n)]
$, sols_to_bool(x,$e):
 if $e=='all':
  $! 'true'
 if $e is $#:
  $! $#
 if $. $e:
  $! 'false'
 eqs=[('=',x,s)$) s in $e]
 if $3(eqs)==1:
  $! eqs[0]
 $!('or',)+$1(eqs)
$, apply_constraints($e,x,cons):
 if $. cons or $e=='all' or $e is $#:
  $! $e
 lo=$#
 hi=$#
 $?=[]
 expanded=[]
 $) s in $e:
  ns=[w $) w in ${(s)if w[0]=='n' $+ w[1:].isdigit()]
  if ns $+ $3(ns)==1:
   b=bounds(cons,x)
   if b is $#:
    expanded.$%(s)
    $7
   n=ns[0]
   $) k in $*(-60,61):
    v=$W(s,n,k)
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
  if head(c)in('<','<=','>','>=')$+ $5(c[1])$+ c[2]==x:
   if c[0]in('<','<='):
    lo=c[1]
   $(:
    hi=c[1]
  $J head(c)in('<','<=','>','>=')$+ c[1]==x $+ $5(c[2]):
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
    a=fv($W(c[1],x,s))
    b=fv($W(c[2],x,s))
   $< $=:
    if $. $5(s):
     $7
    $! $2
   eps=1e-12*(1+$I(a)+$I(b))
   if h=='<' $+ $. a<b-eps*0:
    $! $2
   if h=='<=' $+ $. a<=b+eps:
    $! $2
   if h=='>' $+ $. a>b:
    $! $2
   if h=='>=' $+ $. a>=b-eps:
    $! $2
   if h=='/=' $+ $I(a-b)<=eps:
    $! $2
  $J h=='$+':
   if $. satisfies(s,x,$G(c[1:])):
    $! $2
 $! $F
''')
_x(r'''$, solve(eq,x,$A=$2,cons=$#):
 NC[0]=0
 if $&(eq,'$+')or $&(eq,'$G'):
  $! $#
 h=head(eq)
 if h in('<','>','<=','>=','/='):
  f=$b(eq[1],eq[2])
  r=solve_ineq(h,f,x)
  $! r
 if h=='=':
  f=$b(eq[1],eq[2])
 $J h=='or':
  parts=[]
  $) e in eq[1:]:
   r=solve(e,x,$A,cons)
   if r is $#:
    $! $#
   if r!='false':
    parts.$%(r)
  if $. parts:
   $! 'false'
  $!('or',)+$1(parts)if $3(parts)>1 $( parts[0]
 $J eq=='true':
  $! 'true'
 $(:
  f=eq
 $e=$x(f,x,$A)
 if $e is $#:
  $! $#
 if $e!='all':
  $e=[clean(s)$) s in $e]
  if $. $A:
   $e=[s $) s in $e if $.($5(s)$+ $. $y(s))]
   $e=[realpart(s)$) s in $e]
  $e=sortsols(dedup($e))
 if cons:
  $e=apply_constraints($e,x,cons)
 $! sols_to_bool(x,$e)
$, realpart(s):
 if $5(s)$+ has(s,'i'):
  r,i=reim(s)
  if i==0 or($@(i)$+ $I(tofl(i))<1e-12):
   $! r
 $! s
$, zeros(e,x,$A=$2,cons=$#):
 NC[0]=0
 if $&(e,'='):
  e=$b(e[1],e[2])
 $e=$x(e,x,$A)
 if $e is $#:
  $! $#
 if $e=='all':
  $!('$G',)
 $e=[clean(s)$) s in $e]
 if $. $A:
  $e=[realpart(s)$) s in $e if $.($5(s)$+ $. $y(s))]
 $e=sortsols(dedup($e))
 if cons:
  $e=apply_constraints($e,x,cons)
 $!('$G',)+$1($e)
YP=('Y1_','Y2_')
$, desolve(ode,x,y,conds):
 NC[0]=0
 F=eqexpr(ode)if $&(ode,'=')$( ode
 F=$-(F)
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
 cs_=$^(F,y1)
 if cs_ is $. $# $+ $3(cs_)==2 $+ $8(cs_[1],y1):
  g=$-($o($Y(cs_[0],cs_[1])))
 $(:
  rs=$x(F,y1)
  if $. rs or rs=='all' or $3(rs)!=1:
   $! $#
  g=rs[0]
 c1='c1'
 gy=$^($;(g),y)
 if gy is $. $# $+ $3(gy)==2 $+ $8(gy[1],y):
  P=$o(gy[1])
  Bq=gy[0]
  if Bq==0 or $8(P,x)$+ $8(Bq,x)$+ $2:
   pass
  mu=pw('e',integrate(P,x))
  mu=dropabs(simp(mu))
  I=integ($-($;($9(mu,Bq))),x)
  if I is $. $#:
   yy=$-($Y($c(I,c1),mu))
   $!('=',y,nice($;(yy))if $. hasden_free(yy)$( nice(yy))
 sep=separate(g,x,y)
 if sep is $. $#:
  p,q=sep
  L=integ($-(pw(q,-1)),y)
  R=integ(p,x)
  if L is $. $# $+ R is $. $#:
   rs=isolate_eq(L,$c(R,c1),y)
   if rs is $. $# $+ $3(rs)==1:
    $!('=',y,nice(simp(rs[0])))
   G=lncombine(L,y)
   if G is $. $#:
    rs=$x($b(G,$9(c1,pw('e',R))),y)
    if rs $+ rs!='all' $+ $3(rs)==1:
     $!('=',y,nice(rs[0]))
   $!('=',L,$c(R,c1))
 bern_=bernoulli(g,x,y)
 if bern_ is $. $#:
  $! bern_
 V='V_'
 h=$-($W(g,y,$9(V,x)))
 if $8(h,x)$+ has(h,V):
  dv=$-($b(h,V))
  if dv!=0:
   L=integ($-(pw(dv,-1)),V)
   if L is $. $#:
    R=$c(fn('ln',fn('$I',x)),c1)
    rs=isolate_eq(L,R,V)
    if rs is $. $# $+ $3(rs)==1:
     $!('=',y,nice($;($9(x,rs[0]))))
    L2=$W(L,V,$Y(y,x))
    $!('=',L2,R)
 $! $#
$, dropabs(e):
 if $/(e)is $. $1 or e[0]=='Q':
  $! e
 if e[0]=='$I':
  $! dropabs(e[1])
 $! simp((e[0],)+$1(dropabs(a)$) a in e[1:]))
$, lncombine(L,y):
 $N=L[1:]if $&(L,'+')$((L,)
 fs=[]
 $) t in $N:
  c,r=$V(t)
  if $&(r,'ln')$+ $m(c):
   u=r[1]
   if $&(u,'$I'):
    u=u[1]
   fs.$%(pw(u,c))
  $(:
   $! $#
 if $3(fs)<1:
  $! $#
 $! $-($E(fs))
$, hasden_free(e):
 $! $2
$, isolate_eq(L,R,y):
 try:
  r=isolate(L,R,y,$2,0)
 $< $=:
  $! $#
 if r is $# or r=='all':
  $! $#
 $! r
$, separate(g,x,y):
 if $8(g,y):
  $! g,1
 if $8(g,x):
  $! 1,g
 fs=g[1:]if $&(g,'*')$((g,)
 px=[]
 qy=[]
 $) f in fs:
  if $8(f,y):
   px.$%(f)
  $J $8(f,x):
   qy.$%(f)
  $J $&(f,'^')$+ $8(f[1],x)$+ $8(f[1],y)$+ $&(f[2],'+'):
   tx=[t $) t in f[2][1:]if $8(t,y)]
   ty=[t $) t in f[2][1:]if $8(t,x)]
   if $3(tx)+$3(ty)!=$3(f[2])-1:
    $! $#
   px.$%(pw(f[1],$6(tx)))
   qy.$%(pw(f[1],$6(ty)))
  $(:
   $! $#
 $! $E(px),$E(qy)
$, expand_exp(e):
 if $/(e)is $. $1 or e[0]=='Q':
  $! e
 if e[0]=='^' $+ $&(e[2],'+')$+(e[1]=='e' or $@(e[1])):
  $! $E([pw(e[1],t)$) t in e[2][1:]])
 $! simp((e[0],)+$1(expand_exp(a)$) a in e[1:]))
$, bernoulli(g,x,y):
 g=$;(g)
 $N=g[1:]if $&(g,'+')$((g,)
 groups={}
 $) t in $N:
  k=$#
  fs=t[1:]if $&(t,'*')$((t,)
  $_=[]
  $) f in fs:
   if f==y:
    k=1 if k is $# $( $#
   $J $&(f,'^')$+ f[1]==y $+ $@(f[2]):
    k=f[2]
   $J $8(f,y):
    $_.$%(f)
   $(:
    $! $#
  if k is $#:
   $! $#
  groups[k]=$c(groups.get(k,0),$E($_))
 if $3(groups)!=2 or 1 $. in groups:
  $! $#
 n=[k $) k in groups if k!=1][0]
 a=groups[1]
 b=groups[n]
 m=nsub(1,n)
 V='V_'
 vs=de1($b(YP[0],$9(m,$c($9(a,V),b))),x,V)
 if vs is $# or $. $&(vs,'=')or vs[1]!=V:
  $! $#
 $!('=',y,nice(pw(vs[2],ninv(m))))
''')
_x(r'''$, de2(F,x,y):
 y1,y2=YP
 c1,c2='c1','c2'
 G=$;(F)
 a=$^(G,y2)
 if a is $# or $3(a)!=2:
  $! $#
 A=a[1]
 $_=a[0]
 b=$^($_,y1)
 if b is $# or $3(b)>2:
  $! $#
 B=b[1]if $3(b)==2 $( 0
 $_=b[0]
 c=$^($_,y)
 if c is $# or $3(c)>2:
  $! $#
 C=c[1]if $3(c)==2 $( 0
 g=$o(c[0])
 $) t in(A,B,C):
  if has(t,y)or has(t,y1)or has(t,y2):
   $! $#
 if $8(A,x)$+ $8(B,x)$+ $8(C,x):
  y1s,y2s=charsol(A,B,C,x)
 $(:
  ce=cauchy_euler(A,B,C,x)
  if ce is $#:
   if C==0:
    V='V_'
    r=de1($c($9(A,YP[0]),$9(B,V),$o(g)),x,V)
    if r is $# or $. $&(r,'=')or r[1]!=V:
     $! $#
    r2=integ($W(r[2],'c1','c2'),x)
    if r2 is $#:
     $! $#
    $!('=',y,$c(r2,c1))
   $! $#
  y1s,y2s=ce
 yh=$c($9(c1,y1s),$9(c2,y2s))
 if g==0:
  $!('=',y,yh)
 W=pyth($-($;($b($9(y1s,diff(y2s,x)),$9(diff(y1s,x),y2s)))))
 gg=$-($Y(g,A))
 I1=integ($-($;($Y($9(y2s,gg),W))),x)
 I2=integ($-($;($Y($9(y1s,gg),W))),x)
 if I1 is $# or I2 is $#:
  $! $#
 yp=pyth($;($c($9($o(y1s),I1),$9(y2s,I2))))
 $!('=',y,nice($c(yh,yp)))
$, charsol(A,B,C,x):
 D=$-($;($b($9(B,B),$9(4,A,C))))
 if $y(D)$+ fv(D)<0:
  al=$-($Y($o(B),$9(2,A)))
  be=$-($Y($T($o(D)),$9(2,A)))
  ex=pw('e',$9(al,x))
  $! $9(ex,fn('cos',$9(be,x))),$9(ex,fn('sin',$9(be,x)))
 if D==0:
  r=$-($Y($o(B),$9(2,A)))
  $! pw('e',$9(r,x)),$9(x,pw('e',$9(r,x)))
 s=$T(D)
 r1=$-($Y($c($o(B),s),$9(2,A)))
 r2=$-($Y($b($o(B),s),$9(2,A)))
 $! pw('e',$9(r1,x)),pw('e',$9(r2,x))
$, cauchy_euler(A,B,C,x):
 a=$-($Y(A,pw(x,2)))
 b=$-($Y(B,x))
 if $.($8(a,x)$+ $8(b,x)$+ $8(C,x)):
  $! $#
 aa=a
 bb=$b(b,a)
 cc=C
 D=$-($;($b($9(bb,bb),$9(4,aa,cc))))
 lx=fn('ln',x)
 if $y(D)$+ fv(D)<0:
  al=$-($Y($o(bb),$9(2,aa)))
  be=$-($Y($T($o(D)),$9(2,aa)))
  $! $9(pw(x,al),fn('cos',$9(be,lx))),$9(pw(x,al),fn('sin',$9(be,lx)))
 if D==0:
  r=$-($Y($o(bb),$9(2,aa)))
  $! pw(x,r),$9(pw(x,r),lx)
 s=$T(D)
 r1=$-($Y($c($o(bb),s),$9(2,aa)))
 r2=$-($Y($b($o(bb),s),$9(2,aa)))
 $! pw(x,r1),pw(x,r2)
$, apply_ic(sol,x,y,conds,nconst):
 cs_=['c1','c2'][:nconst]
 eqs=[]
 if sol[1]==y:
  Y=sol[2]
  $) order,x0,v in conds:
   e=Y
   $) _ in $*(order):
    e=diff(e,x)
   eqs.$%(('=',$W(e,x,x0),v))
 $(:
  $) order,x0,v in conds:
   if order==0:
    eqs.$%($W($W(sol,x,x0),y,v))
 used=[c $) c in cs_ if has(sol,c)]
 if $. eqs or $. used:
  $! sol
 rs=solve_system(eqs,used)
 if $. rs:
  $! 'false'
 s=rs[0]
 r=sol
 $) c in used:
  if c in s:
   r=(r[0],$W(r[1],c,s[c]),$W(r[2],c,s[c]))
 if r[1]==y:
  $!('=',y,nice(r[2]))
 rs2=isolate_eq(r[1],r[2],y)
 if rs2 is $. $# $+ $3(rs2)>=1:
  $) cand in rs2:
   ok=$F
   $) order,x0,v in conds:
    if order==0:
     try:
      if $I($S($W(cand,x,x0))-$S(v))>1e-9:
       ok=$2
     $< $=:
      pass
   if ok:
    $!('=',y,nice(cand))
 $! r
$, fextreme(f,x,kind,lo=$#,hi=$#):
 NC[0]=0
 d=$-(diff(f,x))
 cands=[]
 rs=$x(d,x)
 if rs is $#:
  rs=numeric_solve(d,x,$2,tofl($S(lo))if lo is $. $# $+ $5(lo)$( $#,
 tofl($S(hi))if hi is $. $# $+ $5(hi)$( $#)or[]
 if rs=='all':
  $! 'true'
 exp_=[]
 $) r in rs:
  ns=[w $) w in ${(r)if w[0]=='n' $+ w[1:].isdigit()]
  if ns $+ lo is $. $# $+ hi is $. $#:
   $) k in $*(-50,51):
    exp_.$%($W(r,ns[0],k))
  $J ns:
   exp_.$%(r)
  $(:
   exp_.$%(r)
 rs=exp_
 $) r in rs:
  r=clean(r)
  ns=[w $) w in ${(r)if w[0]=='n' $+ w[1:].isdigit()]
  if ns:
   cands.$%(r)
   $7
  if $. $y(r):
   $7
  if lo is $. $# $+ fv(r)<fv(lo)-1e-12:
   $7
  if hi is $. $# $+ fv(r)>fv(hi)+1e-12:
   $7
  cands.$%(r)
 ends=[]
 ends.$%(lo if lo is $. $# $(('*',-1,'$]'))
 ends.$%(hi if hi is $. $# $( '$]')
 $}=$#
 bv=$#
 pts=[]
 $) c in cands+ends:
  if c=='$]' or c==('*',-1,'$]'):
   v=limit(f,x,c)
  $(:
   cz=c
   $) w in ${(c):
    if w[0]=='n' $+ w[1:].isdigit():
     cz=$W(cz,w,0)
   v=$W(f,x,cz)
   if has(v,'$L'):
    $7
  try:
   if v=='$]':
    vv=$C('$]')
   $J v==('*',-1,'$]'):
    vv=$C('-$]')
   $(:
    vv=fv(v)
  $< $=:
   $7
  if kind=='max':
   vv=-vv
  pts.$%((vv,c))
 if $. pts:
  $! $#
 pts.sort(key=$4 p:p[0])
 m=pts[0][0]
 win=[p[1]$) p in pts if $I(p[0]-m)<=1e-10*(1+$I(m))or p[0]==m]
 win=sortsols(dedup(win))
 eqs=[('=',x,w)$) w in win]
 $! eqs[0]if $3(eqs)==1 $(('or',)+$1(eqs)
$, nfextreme(f,x,kind,lo=$#,hi=$#):
 sg=1.0 if kind=='min' $(-1.0
 $, F(t):
  try:
   v=$S(f,{x:t})
   if $/(v)is $0:
    v=v.$Q
   $! sg*v
  $< $=:
   $! $C('$]')
 if lo is $# or hi is $#:
  a=-100.0 if lo is $# $( lo
  b=100.0 if hi is $# $( hi
 $(:
  a,b=lo,hi
 N=400
 $}=a
 bv=F(a)
 $) i in $*(N+1):
  t=a+(b-a)*i/N
  v=F(t)
  if v<bv:
   bv=v
   $}=t
 h=(b-a)/N
 l=max(a,$}-h)
 r=min(b,$}+h)
 g=($P.$T(5)-1)/2
 $) _ in $*(200):
  c=r-g*(r-l)
  d=l+g*(r-l)
  if F(c)<F(d):
   r=d
  $(:
   l=c
  if $I(r-l)<1e-12*(1+$I(l)):
   $X
 t=0.5*(l+r)
 try:
  d=diff(f,x)
  $, G(u):
   try:
    v=$S(d,{x:u})
    $! v.$Q if $/(v)is $0 $( v
   $< $=:
    $! $#
  t2=newton(G,t)
  if t2 is $. $# $+ $I(t2-t)<10*h $+(lo is $# or t2>=lo)$+(hi is $# or t2<=hi):
   t=t2
 $< $=:
  pass
 $! snap(t)
''')
_x(r'''$, domain(f,x):
 conds=[]
 domconds(f,x,conds)
 if $. conds:
  $!('<',('*',-1,'$]'),x)if $2 $( 'true'
 pts=[]
 $) rel,g in conds:
  rs=$x(g,x)
  if rs is $#:
   $! $#
  if rs=='all':
   $7
  $) r in rs:
   if $y(r):
    pts.$%(r)
 pts=sortsols(dedup(pts))
 $, ok(t):
  $) rel,g in conds:
   try:
    v=$S(g,{x:t})
   $< $=:
    $! $2
   if $/(v)is $0:
    if $I(v.imag)>1e-9:
     $! $2
    v=v.$Q
   if $. relok(rel,v):
    $! $2
  $! $F
 $, okexact(p):
  $) rel,g in conds:
   try:
    v=$W(g,x,p)
    vv=fv(v)
   $< $=:
    $! $2
   if $I(vv)<1e-12:
    vv=0.0
   if $. relok(rel,vv):
    $! $2
  $! $F
 $g=[fv(p)$) p in pts]
 if $. $g:
  $! 'true' if ok(0.5)$( 'false'
 segs=[('I',$#,pts[0],ok($g[0]-max(1.0,$I($g[0]))))]
 $) i in $*($3(pts)):
  segs.$%(('P',pts[i],pts[i],okexact(pts[i])))
  if i+1<$3(pts):
   segs.$%(('I',pts[i],pts[i+1],ok(0.5*($g[i]+$g[i+1]))))
 segs.$%(('I',pts[-1],$#,ok($g[-1]+max(1.0,$I($g[-1])))))
 $! segs_to_bool(segs,x)
$, domconds(f,x,$?):
 if $/(f)is $. $1 or f[0]=='Q' or $8(f,x):
  $!
 h=f[0]
 if h=='^':
  b,p=f[1],f[2]
  if $@(p)$+ $a(p)<0:
   $?.$%(('/=',b))
  if isq(p)$+ p[2]%2==0:
   $?.$%(('>=' if $a(p)>0 $( '>',b))
 $J h in('ln','log'):
  $?.$%(('>',f[1]))
 $J h in('$w','arccos'):
  $?.$%(('<=',$b(fn('$I',f[1]),1)))
 $J h=='tan':
  $?.$%(('/=',fn('cos',f[1])))
 $) a in f[1:]:
  domconds(a,x,$?)
''')
_x(r'''import $P
$, ismat(e):
 $! $&(e,'mat')
$, $[(e):
 $! $&(e,'$G')
$, $j(M):
 $![$G(r[1:])$) r in M[1:]]
$, mk(R):
 $!('mat',)+$1(('$G',)+$1(r)$) r in R)
$, lst(xs):
 $!('$G',)+$1(xs)
$, dims(M):
 $! $3(M)-1,$3(M[1])-1
$, tomat(e):
 if ismat(e):
  $! e
 if $[(e):
  $! mk([$G(e[1:])])
 err("Matrix expected")
$, ac(e):
 $! $-($;(e))if hasdenom(e)$( $;(e)
$, m_add(A,B,sgn=1):
 if dims(A)!=dims(B):
  err("Dimension error")
 a=$j(A)
 b=$j(B)
 $! mk([[$c(a[i][j],$9(sgn,b[i][j]))$) j in $*($3(a[0]))]$) i in $*($3(a))])
$, m_scale(A,c):
 $! mk([[$9(c,v)$) v in r]$) r in $j(A)])
$, m_map(A,f):
 $! mk([[f(v)$) v in r]$) r in $j(A)])
$, m_mul(A,B):
 a=$j(A)
 b=$j(B)
 if $3(a[0])!=$3(b):
  err("Dimension error")
 n=$3(b)
 $! mk([[ac($6([$9(a[i][k],b[k][j])$) k in $*(n)]))$) j in $*($3(b[0]))]$) i in $*($3(a))])
$, ident(n):
 $! mk([[1 if i==j $( 0 $) j in $*(n)]$) i in $*(n)])
$, m_pow(A,k):
 m,n=dims(A)
 if m!=n:
  err("Square matrix required")
 if k<0:
  A=m_inv(A)
  k=-k
 R=ident(n)
 $H k>0:
  if k&1:
   R=m_mul(R,A)
  k>>=1
  if k:
   A=m_mul(A,A)
 $! R
$, transpose(A):
 if $[(A):
  $! mk([[v]$) v in A[1:]])
 a=$j(A)
 $! mk([[a[i][j]$) i in $*($3(a))]$) j in $*($3(a[0]))])
$, det(A):
 a=$j(A)
 n=$3(a)
 if n!=$3(a[0]):
  err("Square matrix required")
 if n==1:
  $! a[0][0]
 if n==2:
  $! ac($b($9(a[0][0],a[1][1]),$9(a[0][1],a[1][0])))
 if n==3:
  t=[]
  $) j in $*(3):
   minor=$b($9(a[1][(j+1)%3],a[2][(j+2)%3]),$9(a[1][(j+2)%3],a[2][(j+1)%3]))
   t.$%($9(a[0][j],minor))
  $! ac($6(t))
 M=[$G(r)$) r in a]
 sign=1
 prev=1
 $) k in $*(n-1):
  if ac(M[k][k])==0:
   sw=$#
   $) i in $*(k+1,n):
    if ac(M[i][k])!=0:
     sw=i
     $X
   if sw is $#:
    $! 0
   M[k],M[sw]=M[sw],M[k]
   sign=-sign
  $) i in $*(k+1,n):
   $) j in $*(k+1,n):
    M[i][j]=ac($Y($b($9(M[i][j],M[k][k]),$9(M[i][k],M[k][j])),prev))
  prev=M[k][k]
 $! ac($9(sign,M[n-1][n-1]))
$, iszero(v):
 v=ac(v)
 if v==0:
  $! $F
 if $/(v)is $C $+ $I(v)<1e-13:
  $! $F
 $! $2
$, rref(A,full=$F):
 M=[$G(r)$) r in $j(A)]
 m=$3(M)
 n=$3(M[0])
 r=0
 $) c in $*(n):
  if r>=m:
   $X
  p=$#
  if hasfloat_m(M):
   $}=0.0
   $) i in $*(r,m):
    try:
     v=$I($S(M[i][c]))
    $< $=:
     v=1.0 if $. iszero(M[i][c])$( 0.0
    if v>$}+1e-14:
     $}=v
     p=i
   if $}<1e-13:
    p=$#
  $(:
   $) i in $*(r,m):
    if $. iszero(M[i][c]):
     p=i
     $X
  if p is $#:
   $7
  M[r],M[p]=M[p],M[r]
  pv=M[r][c]
  if full:
   M[r]=[ac($Y(v,pv))$) v in M[r]]
  $(:
   M[r]=[ac($Y(v,pv))$) v in M[r]]
  rng=$*(m)if full $( $*(r+1,m)
  $) i in rng:
   if i!=r $+ $. iszero(M[i][c]):
    f=M[i][c]
    M[i]=[ac($b(M[i][j],$9(f,M[r][j])))$) j in $*(n)]
  r+=1
 $) i in $*(m):
  $) j in $*(n):
   if $/(M[i][j])is $C $+ $I(M[i][j])<1e-13:
    M[i][j]=0.0
 $! mk(M)
$, hasfloat_m(M):
 $) r in M:
  $) v in r:
   if $`(v):
    $! $F
 $! $2
$, minor(a,i,j):
 $![[a[r][c]$) c in $*($3(a))if c!=j]$) r in $*($3(a))if r!=i]
$, m_inv(A):
 m,n=dims(A)
 if m!=n:
  err("Square matrix required")
 a0=$j(A)
 if n<=3 $+ $. all([$@(v)$) r in a0 $) v in r]):
  D=det(A)
  if iszero(D):
   err("Singular matrix")
  if n==1:
   $! mk([[nice(pw(D,-1))]])
  $?=[]
  $) i in $*(n):
   row=[]
   $) j in $*(n):
    c=det(mk(minor(a0,j,i)))
    if(i+j)%2:
     c=$o(c)
    row.$%(nice(ac($Y(c,D))))
   $?.$%(row)
  $! mk($?)
 a=$j(A)
 aug=mk([a[i]+[1 if i==j $( 0 $) j in $*(n)]$) i in $*(n)])
 R=$j(rref(aug))
 $) i in $*(n):
  $) j in $*(n):
   if $. iszero($b(R[i][j],1 if i==j $( 0)):
    err("Singular matrix")
 $! mk([[nice(R[i][n+j])$) j in $*(n)]$) i in $*(n)])
$, trace(A):
 a=$j(A)
 $! $6([a[i][i]$) i in $*($3(a))])
$, charpoly(A,lam):
 a=$j(A)
 n=$3(a)
 if n!=$3(a[0]):
  err("Square matrix required")
 I=ident(n)
 Mk=mk([[0]*n $) _ in $*(n)])
 cs=[0]*(n+1)
 cs[n]=1
 $) k in $*(1,n+1):
  Mk=m_add(m_mul(A,Mk),m_scale(I,cs[n-k+1]))
  cs[n-k]=ac($Y($o(trace(m_mul(A,Mk))),k))
 $! $6([$9(cs[k],pw(lam,k))$) k in $*(n+1)])
$, eigvl(A):
 if hasfloat_m($j(A)):
  try:
   E=m_map(A,exactify)
  $< $=:
   E=$#
  if E is $. $# $+ $. hasfloat_m($j(E)):
   $! evalf(eigvl(E))
 lam='L_'
 p=charpoly(A,lam)
 f=p
 if $. hasfloat_m($j(A)):
  try:
   f=$v(p)
  $< $=:
   f=p
  if $&(f,'hold'):
   f=f[1]
 $?=[]
 $) g in(f[1:]if $&(f,'*')$((f,)):
  k=1
  if $&(g,'^')$+ $i(g[2])$+ g[2]>0:
   g,k=g[1],g[2]
  if $8(g,lam):
   $7
  z=zeros(g,lam,$F)
  if z is $#:
   err("Cannot compute eigenvalues")
  z=$G(z[1:])
  d=degree(g,lam)
  $) v in z:
   m=mult(g,lam,v,d)if d is $. $# $+ $3(z)<d $( 1
   $?+=[v]*(k*m)
 if $. $?:
  err("Cannot compute eigenvalues")
 $, key(v):
  if $. $5(v):
   $!(1,0.0,0.0,okey(v))
  z=$0($S(v))
  $!(0,-$I(z),-z.$Q,-z.imag)
 $?.sort(key=key)
 $! lst($?)
$, mult(g,lam,v,d):
 m=1
 h=g
 $H m<d:
  h=diff_(h,lam)
  w=$W(h,lam,v)
  if $`(w)or $`(v):
   try:
    if $I($0($S(w)))>1e-6*(1+$I($0($S(v))))**d:
     $X
   $< $=:
    $X
  $J $. iszero(ac($;(w))):
   $X
  m+=1
 $! m
$, diff_(e,x):
 $! diff(e,x)
''')
_x(r'''$, nullspace(A):
 R=$j(rref(A))
 m=$3(R)
 n=$3(R[0])
 piv=[]
 $) i in $*(m):
  $) j in $*(n):
   if $. iszero(R[i][j]):
    piv.$%((i,j))
    $X
 pc=[j $) i,j in piv]
 free=[j $) j in $*(n)if j $. in pc]
 basis=[]
 $) f in free:
  v=[0]*n
  v[f]=1
  $) i,j in piv:
   v[j]=ac($o(R[i][f]))
  basis.$%(v)
 $! basis
$, eigvc(A):
 if hasfloat_m($j(A)):
  try:
   E=m_map(A,exactify)
  $< $=:
   E=$#
  if E is $. $# $+ $. hasfloat_m($j(E)):
   $! evalf(eigvc(E))
 $g=eigvl(A)
 n=dims(A)[0]
 cols=[]
 seen=[]
 $) lv in $g[1:]:
  if lv in seen:
   $7
  seen.$%(lv)
  if $`(lv)or hasfloat_m($j(A)):
   cols.$%(numeigvec(A,lv))
   $7
  B=m_add(A,m_scale(ident(n),lv),-1)
  B=m_map(B,$4 v:ac(v))
  ns=nullspace(B)
  $) v in ns:
   cols.$%(unitvec(v))
 if $. cols:
  err("Cannot compute eigenvectors")
 M=mk([[cols[j][i]$) j in $*($3(cols))]$) i in $*(n)])
 $) c in cols:
  $) v in c:
   if esize(v)>60:
    $! evalf(M)
 $! M
$, numeigvec(A,lam):
 a=[[$0($S(c))$) c in r]$) r in $j(A)]
 n=$3(a)
 mu=$0($S(lam))
 mu+=1e-9*(1+$I(mu))
 M=[[a[i][j]-(mu if i==j $( 0)$) j in $*(n)]$) i in $*(n)]
 x=[$0(1.0+0.37*i)$) i in $*(n)]
 $) it in $*(4):
  y=clsolve(M,x)
  big=max([$I(v)$) v in y])or 1.0
  x=[v/big $) v in y]
 nrm=$P.$T(sum([$I(v)**2 $) v in x]))or 1.0
 x=[v/nrm $) v in x]
 k=0
 $) i in $*(n):
  if $I(x[i])>$I(x[k])+1e-12:
   k=i
 ph=x[k]/$I(x[k])
 $?=[]
 $) v in x:
  v=v/ph
  re=0.0 if $I(v.$Q)<1e-12 $( v.$Q
  im=0.0 if $I(v.imag)<1e-12 $( v.imag
  $?.$%(re if im==0.0 $( fromcomplex($0(re,im)))
 $! $?
$, clsolve(M,b):
 n=$3(M)
 a=[$G(M[i])+[b[i]]$) i in $*(n)]
 $) c in $*(n):
  p=c
  $) r in $*(c+1,n):
   if $I(a[r][c])>$I(a[p][c]):
    p=r
  a[c],a[p]=a[p],a[c]
  if $I(a[c][c])<1e-14:
   a[c][c]=1e-14
  $) r in $*(c+1,n):
   f=a[r][c]/a[c][c]
   if f:
    $) k in $*(c,n+1):
     a[r][k]-=f*a[c][k]
 x=[0j]*n
 $) i in $*(n-1,-1,-1):
  t=a[i][n]
  $) k in $*(i+1,n):
   t-=a[i][k]*x[k]
  x[i]=t/a[i][i]
 $! x
$, coefs(e,$?):
 if $@(e):
  $?.$%(e)
 $J $&(e,'+'):
  $) t in e[1:]:
   coefs(t,$?)
 $J $&(e,'*')$+ $@(e[1]):
  $?.$%(e[1])
 $(:
  $?.$%(1)
$, unitvec(v):
 if hasfloat_m([v]):
  nrm=$T($6([$9(c,fn('conj',c))$) c in v]))
  $![nice(ac($Y(c,nrm)))$) c in v]
 cs=[]
 $) c in v:
  coefs(c,cs)
 den=1
 num=0
 $) q in cs:
  if $m(q)$+ q!=0:
   a,b=nd(q)
   den=ilcm(den,b)
   num=igcd(num,a)
 k=Q(den,num)if num $( 1
 $) c in v:
  if $. iszero(c):
   if isneg(c):
    k=$o(k)
   $X
 w=[ac($;($9(k,c)))$) c in v]
 n2=ac($;($6([$9(c,fn('conj',c))$) c in w])))
 r=$T(n2)
 if $@(r)or $. $&(r,'^'):
  $![ac($Y(c,r))$) c in w]
 inv=('^',r[1],$o(r[2]))
 $![c if iszero(c)$(('*',c,inv)if $&(c,'+')$( $9(c,inv)$) c in w]
$, esize(e):
 if $/(e)is $. $1 or e[0]=='Q':
  $! 1
 k=1
 $) a in e[1:]:
  k+=esize(a)
 $! k
$, lu(A):
 a=[$G(r)$) r in $j(A)]
 m=$3(a)
 n=$3(a[0])
 L=[[1 if i==j $( 0 $) j in $*(m)]$) i in $*(m)]
 P=$G($*(m))
 U=a
 $) k in $*(min(m,n)):
  p=$#
  if hasfloat_m(U):
   $}=-1.0
   $) i in $*(k,m):
    v=$I($S(U[i][k]))
    if v>$}:
     $}=v
     p=i
   if $}<1e-14:
    p=$#
  $(:
   $) i in $*(k,m):
    if $. iszero(U[i][k]):
     p=i
     $X
  if p is $#:
   $7
  if p!=k:
   U[k],U[p]=U[p],U[k]
   P[k],P[p]=P[p],P[k]
   $) j in $*(k):
    L[k][j],L[p][j]=L[p][j],L[k][j]
  $) i in $*(k+1,m):
   f=ac($Y(U[i][k],U[k][k]))
   L[i][k]=f
   U[i]=[ac($b(U[i][j],$9(f,U[k][j])))$) j in $*(n)]
 Pm=[[1 if P[i]==j $( 0 $) j in $*(m)]$) i in $*(m)]
 $! mk(L),mk(U),mk(Pm)
$, qr(A):
 a=$j(A)
 m=$3(a)
 n=$3(a[0])
 cols=[[a[i][j]$) i in $*(m)]$) j in $*(n)]
 Qc=[]
 R=[[0]*n $) _ in $*(n)]
 $) j in $*(n):
  v=cols[j]
  $) k in $*($3(Qc)):
   r=ac($6([$9(Qc[k][i],v[i])$) i in $*(m)]))
   R[k][j]=r
   v=[ac($b(v[i],$9(r,Qc[k][i])))$) i in $*(m)]
  nrm=nice($T(ac($6([pw(c,2)$) c in v]))))
  R[j][j]=nrm
  if iszero(nrm):
   Qc.$%([0]*m)
  $(:
   Qc.$%([nice(ac($Y(c,nrm)))$) c in v])
 Qm=mk([[Qc[j][i]$) j in $*(n)]$) i in $*(m)])
 $! Qm,mk(R)
$, crossp(u,v):
 a=vec(u)
 b=vec(v)
 if $3(a)==2:
  a=a+[0]
  b=b+[0]
 if $3(a)!=3 or $3(b)!=3:
  err("Dimension error")
 r=[ac($b($9(a[1],b[2]),$9(a[2],b[1]))),
 ac($b($9(a[2],b[0]),$9(a[0],b[2]))),
 ac($b($9(a[0],b[1]),$9(a[1],b[0])))]
 $! revec(r,u)
$, vec(u):
 if $[(u):
  $! $G(u[1:])
 if ismat(u):
  R=$j(u)
  if $3(R)==1:
   $! R[0]
  if $3(R[0])==1:
   $![r[0]$) r in R]
 err("Vector expected")
$, revec(r,like):
 if $[(like):
  $! lst(r)
 R=$j(like)
 if $3(R)==1:
  $! mk([r])
 $! mk([[v]$) v in r])
$, dotp(u,v):
 a=vec(u)
 b=vec(v)
 if $3(a)!=$3(b):
  err("Dimension error")
 $! ac($6([$9(a[i],b[i])$) i in $*($3(a))]))
$, norm(A):
 if $[(A)or ismat(A)$+(dims(A)[0]==1 or dims(A)[1]==1):
  v=vec(A)
  $! nice($T(ac($6([$9(c,fn('conj',c))$) c in v]))))
 $! nice($T(ac($6([$9(c,fn('conj',c))$) r in $j(A)$) c in r]))))
$, unitv(u):
 nrm=norm(u)
 $! revec([nice(ac($Y(c,nrm)))$) c in vec(u)],u)
$, rownorm(A):
 if $. ismat(A):
  err('Argument must be a matrix')
 $! maxexpr([ac($6([fn('$I',c)$) c in r]))$) r in $j(A)])
$, colnorm(A):
 if $. ismat(A):
  err('Argument must be a matrix')
 $! rownorm(transpose(A))
$, maxexpr(xs):
 $}=$#
 bv=$#
 $) x in xs:
  v=$S(x)
  if $} is $# or v>bv:
   $}=x
   bv=v
 $! $}
''')
_x(r'''$, augment(A,B):
 if $[(A)$+ $[(B):
  $! A+B[1:]
 a=$j(tomat(A))
 b=$j(tomat(B))
 if $3(a)!=$3(b):
  err("Dimension error")
 $! mk([a[i]+b[i]$) i in $*($3(a))])
$, colaugment(A,B):
 a=$j(tomat(A))
 b=$j(tomat(B))
 if $3(a[0])!=$3(b[0]):
  err("Dimension error")
 $! mk(a+b)
$, submat(A,r1=1,c1=1,r2=$#,c2=$#):
 a=$j(A)
 if r2 is $#:
  r2=$3(a)
 if c2 is $#:
  c2=$3(a[0])
 $! mk([a[i][c1-1:c2]$) i in $*(r1-1,r2)])
$, rowswap(A,i,j):
 a=$j(A)
 a[i-1],a[j-1]=a[j-1],a[i-1]
 $! mk(a)
$, rowadd(A,i,j):
 a=$j(A)
 a[j-1]=[$c(a[j-1][k],a[i-1][k])$) k in $*($3(a[0]))]
 $! mk(a)
$, mrow(c,A,i):
 a=$j(A)
 a[i-1]=[$9(c,v)$) v in a[i-1]]
 $! mk(a)
$, mrowadd(c,A,i,j):
 a=$j(A)
 a[j-1]=[ac($c(a[j-1][k],$9(c,a[i-1][k])))$) k in $*($3(a[0]))]
 $! mk(a)
$, diag(A):
 if $[(A):
  n=$3(A)-1
  $! mk([[A[i+1]if i==j $( 0 $) j in $*(n)]$) i in $*(n)])
 a=$j(A)
 if $3(a)==1 or $3(a[0])==1:
  v=vec(A)
  $! diag(lst(v))
 $! lst([a[i][i]$) i in $*(min($3(a),$3(a[0])))])
$, matlist(A):
 $! lst([v $) r in $j(A)$) v in r])
$, listmat(L,c=$#):
 xs=$G(L[1:])
 if c is $#:
  c=$3(xs)
 if $. $i(c)or c<1:
  err('Invalid number of columns')
 $?=[]
 $H xs:
  r=xs[:c]
  xs=xs[c:]
  $H $3(r)<c:
   r.$%(0)
  $?.$%(r)
 $! mk($?)
$, simult(A,b):
 a=$j(A)
 n=$3(a)
 bb=$j(tomat(b))if ismat(b)$([[v]$) v in b[1:]]
 if $3(bb)!=n:
  bb=$j(transpose(b))
 k=$3(bb[0])
 R=$j(rref(mk([a[i]+bb[i]$) i in $*(n)])))
 $) i in $*(n):
  if iszero(R[i][i]):
   err("Singular matrix")
 $! mk([[nice(R[i][n+j])$) j in $*(k)]$) i in $*(n)])
$, cumsum(L):
 if $[(L):
  $?=[]
  s=0
  $) v in L[1:]:
   s=$c(s,v)
   $?.$%(s)
  $! lst($?)
 a=$j(L)
 $?=[]
 acc=[0]*$3(a[0])
 $) r in a:
  acc=[$c(acc[j],r[j])$) j in $*($3(r))]
  $?.$%($G(acc))
 $! mk($?)
$, polar_vec(u):
 v=vec(u)
 if $3(v)==2:
  r=nice($T(ac($c(pw(v[0],2),pw(v[1],2)))))
  th=fn('$p',$c(v[0],$9('i',v[1])))
  $!('$u','['+fmtx(r)+' \u2220'+fmtx(th)+']')
 err("Dimension error")
$, fmtx(e):
 $! fmt(e)
$, cylind(u):
 v=vec(u)
 if $3(v)!=3:
  err("Dimension error")
 r=nice($T(ac($c(pw(v[0],2),pw(v[1],2)))))
 th=fn('$p',$c(v[0],$9('i',v[1])))
 $!('$u','['+fmtx(r)+' \u2220'+fmtx(th)+' '+fmtx(v[2])+']')
$, sphere(u):
 v=vec(u)
 if $3(v)!=3:
  err("Dimension error")
 rho=nice($T(ac($c(pw(v[0],2),pw(v[1],2),pw(v[2],2)))))
 th=fn('$p',$c(v[0],$9('i',v[1])))
 ph=fn('arccos',$Y(v[2],rho))if rho!=0 $( 0
 $!('$u','['+fmtx(rho)+' \u2220'+fmtx(th)+' \u2220'+fmtx(ph)+']')
$, lsum(L,a=1,b=$#):
 xs=$G(L[1:])
 if b is $#:
  b=$3(xs)
 $! $6(xs[a-1:b])
$, lprod(L,a=1,b=$#):
 xs=$G(L[1:])
 if b is $#:
  b=$3(xs)
 $! $E(xs[a-1:b])
$, mean(L,F=$#):
 xs=$G(L[1:])
 if F is $#:
  $! $Y($6(xs),$3(xs))
 fs=$G(F[1:])
 $! $Y($6([$9(xs[i],fs[i])$) i in $*($3(xs))]),$6(fs))
$, sortkey(v):
 try:
  x=$S(v)
  $! x.$Q if $/(x)is $0 $( x
 $< $=:
  $! 0.0
$, median(L):
 xs=sorted($G(L[1:]),key=sortkey)
 n=$3(xs)
 if n%2:
  $! xs[n//2]
 $! $Y($c(xs[n//2-1],xs[n//2]),2)
$, variance(L,pop=$2):
 xs=$G(L[1:])
 n=$3(xs)
 m=mean(L)
 s=$6([pw($b(v,m),2)$) v in xs])
 $! ac($Y(s,n if pop $( n-1))
$, stddev(L,pop=$2):
 $! nice($T(variance(L,pop)))
$, sorta(L):
 $! lst(sorted($G(L[1:]),key=sortkey))
$, sortd(L):
 $! lst(sorted($G(L[1:]),key=sortkey,reverse=$F))
$, deltalist(L):
 xs=$G(L[1:])
 $! lst([$b(xs[i+1],xs[i])$) i in $*($3(xs)-1)])
''')
_x(r'''SET={'$p':'rad','mode':'auto','$A':'$Q'}
$, lmap(f,a):
 if $[(a):
  $!('$G',)+$1(lmap(f,v)$) v in a[1:])
 if ismat(a):
  $!('mat',)+$1(lmap(f,r)$) r in a[1:])
 $! f(a)
$, lmap2(f,a,b):
 if $[(a)$+ $[(b):
  if $3(a)!=$3(b):
   err("Dimension error")
  $!('$G',)+$1(lmap2(f,a[i],b[i])$) i in $*(1,$3(a)))
 if $[(a):
  $!('$G',)+$1(lmap2(f,v,b)$) v in a[1:])
 if $[(b):
  $!('$G',)+$1(lmap2(f,a,v)$) v in b[1:])
 if ismat(a)$+ ismat(b):
  $!('mat',)+$1(lmap2(f,a[i],b[i])$) i in $*(1,$3(a)))
 if ismat(a):
  $!('mat',)+$1(lmap2(f,r,b)$) r in a[1:])
 if ismat(b):
  $!('mat',)+$1(lmap2(f,a,r)$) r in b[1:])
 $! f(a,b)
$, vadd(a,b):
 if ismat(a)$+ ismat(b):
  $! m_add(a,b)
 if $[(a)or $[(b)or ismat(a)or ismat(b):
  $! lmap2($c,a,b)
 if isrel(a)or isrel(b):
  $! relop($c,a,b)
 if isstr(a)or isstr(b):
  err("Data $/ error")
 $! $c(a,b)
$, vsub(a,b):
 $! vadd(a,vneg(b))
$, vneg(a):
 $! lmap($o,a)if $. isrel(a)$((a[0],$o(a[1]),$o(a[2]))
$, vmul(a,b):
 if ismat(a)$+ ismat(b):
  $! m_mul(a,b)
 if ismat(a)$+ $[(b)or $[(a)$+ ismat(b):
  $! m_mul(tomat(a),tomat(b)if ismat(b)$( transpose(b))
 if $[(a)or $[(b)or ismat(a)or ismat(b):
  $! lmap2($9,a,b)
 if isrel(a)or isrel(b):
  $! relop($9,a,b)
 $! $9(a,b)
$, vdiv(a,b):
 if ismat(b):
  if ismat(a):
   $! m_mul(a,m_inv(b))
  $! vmul(a,m_inv(b))
 if $[(a)or $[(b)or ismat(a):
  $! lmap2($Y,a,b)
 if isrel(a)or isrel(b):
  $! relop($Y,a,b)
 if b==0 $+ $5(a):
  $! '$L'
 $! $Y(a,b)
$, vpow(a,b):
 if ismat(a):
  if $/(b)is $q:
   $! m_pow(a,b)
  if b=='T_t':
   $! transpose(a)
  err("Domain error")
 if $[(a)or $[(b):
  $! lmap2(pw,a,b)
 if isrel(a):
  $!(a[0],pw(a[1],b),pw(a[2],b))
 $! pw(a,b)
$, relop(f,a,b):
 if isrel(a)$+ isrel(b):
  $!(a[0],f(a[1],b[1]),f(a[2],b[2]))
 if isrel(a):
  $!(a[0],f(a[1],b),f(a[2],b))
 $!(b[0],f(a,b[1]),f(a,b[2]))
$, isstr(e):
 $! $&(e,'$u')
$, dotop(op,a,b):
 if op=='.*':
  $! lmap2($9,a,b)
 if op=='./':
  $! lmap2($Y,a,b)
 $! lmap2(pw,a,b)
$, rel(op,a,b):
 if $[(a)or $[(b):
  $! lmap2($4 x,y:rel(op,x,y),a,b)
 if isstr(a)$+ isstr(b):
  r=cmpstr(op,a[1],b[1])
  if r is $. $#:
   $! 'true' if r $( 'false'
 d=$-($b(a,b))if $.(isstr(a)or isstr(b))$( $#
 if d is $. $# $+ $5(d)$+ d!='$L':
  try:
   v=$S(d)
  $< $=:
   v=$#
  if v is $. $#:
   if $/(v)is $0:
    if op=='=':
     $! 'true' if $I(v)<1e-13 $( 'false'
    if op=='/=':
     $! 'false' if $I(v)<1e-13 $( 'true'
    err("Non-$Q comparison")
   if d==0 or $I(v)<1e-300:
    v=0.0
   r={'=':v==0,'/=':v!=0,'<':v<0,'>':v>0,'<=':v<=0,'>=':v>=0}[op]
   $! 'true' if r $( 'false'
 if op=='=' $+ d==0:
  $! 'true'
 $!(op,a,b)
$, cmpstr(op,a,b):
 if op=='=':
  $! a==b
 if op=='/=':
  $! a!=b
 $! $#
$, tobool(v):
 if v=='true':
  $! $F
 if v=='false':
  $! $2
 $! $#
$, land(a,b):
 ta=tobool(a)
 tb=tobool(b)
 if ta is $2 or tb is $2:
  $! 'false'
 if ta is $F:
  $! b
 if tb is $F:
  $! a
 $! flat('$+',a,b)
$, lor(a,b):
 ta=tobool(a)
 tb=tobool(b)
 if ta is $F or tb is $F:
  $! 'true'
 if ta is $2:
  $! b
 if tb is $2:
  $! a
 $! flat('or',a,b)
$, flat(op,a,b):
 xs=[]
 $) v in(a,b):
  if $&(v,op):
   xs.extend(v[1:])
  $(:
   xs.$%(v)
 $!(op,)+$1(xs)
$, lnot(a):
 t=tobool(a)
 if t is $. $#:
  $! 'false' if t $( 'true'
 if $i(a):
  $!~a
 neg_={'<':'>=','>':'<=','<=':'>','>=':'<','=':'/=','/=':'='}
 if isrel(a):
  $!(neg_[a[0]],a[1],a[2])
 $!('$.',a)
$, lxor(a,b):
 ta=tobool(a)
 tb=tobool(b)
 if ta is $. $# $+ tb is $. $#:
  $! 'true' if ta!=tb $( 'false'
 if $i(a)$+ $i(b):
  $! a^b
 $!('xor',a,b)
$, need_int(n):
 if isfl(n)$+ finite(n)$+ n==$P.floor(n):
  $! $q(n)
 if $. $i(n):
  err("Argument must be an integer")
 $! n
$, gcd_(a,b):
 if $m(a)$+ $m(b):
  an,ad=nd(a)
  bn,bd=nd(b)
  $! Q(igcd(an,bn),ilcm(ad,bd))
 if isfl(a)or isfl(b):
  $! $C(igcd($q(a),$q(b)))
 $! poly_gcd_expr(a,b)
$, lcm_(a,b):
 if $m(a)$+ $m(b):
  an,ad=nd(a)
  bn,bd=nd(b)
  $! Q(ilcm(an,bn),igcd(ad,bd))
 g=gcd_(a,b)
 $! $-($Y($9(a,b),g))
$, mod_(a,b):
 if $&(a,'^')$+ $i(a[1])$+ $i(a[2])$+ a[2]>0 $+ $i(b)$+ b!=0:
  r=powmod(a[1],a[2],$I(b))
  $! r-$I(b)if b<0 $+ r $( r
 if $@(a)$+ $@(b):
  if b==0:
   $! a
  $! nsub(a,nmul(b,nfloor(ndiv(a,b))))
 $!('mod',a,b)
$, remain_(a,b):
 if $@(a)$+ $@(b):
  if b==0:
   $! a
  q=ndiv(a,b)
  t=nfloor(q)if $a(q)>=0 $(-nfloor(nneg(q))
  $! nsub(a,nmul(b,t))
 $!('remain',a,b)
$, intdiv_(a,b):
 q=ndiv(a,b)
 if $a(q)>=0:
  $! nfloor(q)
 $!-nfloor(nneg(q))
$, bigcomb(n,k):
 if $.($i(n)$+ $i(k))or k<=0:
  $! $2
 m=min(k,$I(n-k))if n>=k $( k
 $! m*ibits(n)>MAXBITS
$, ncr_(n,k):
 if $i(n)$+ $i(k):
  if k<0 or(n>=0 $+ k>n):
   $! 0
  if bigcomb(n,k):
   $!('ncr',n,k)
  $! binom(n,k)if n>=0 $( gen_ncr(n,k)
 if $i(k)$+ k>=0:
  $! gen_ncr(n,k)
 if isfl(n)or isfl(k):
  $! CA_gamma_ratio(n,k)
 $!('ncr',n,k)
$, gen_ncr(n,k):
 r=1
 $) i in $*(k):
  r=$9(r,$b(n,i))
 f=1
 $) i in $*(2,k+1):
  f*=i
 $! $9(r,Q(1,f))
$, npr_(n,k):
 if $i(n)$+ $i(k)$+ k*ibits(n)>MAXBITS:
  $!('npr',n,k)
 if $i(k)$+ k>=0:
  r=1
  $) i in $*(k):
   r=$9(r,$b(n,i))
  $! r
 $!('npr',n,k)
$, CA_gamma_ratio(n,k):
 n=tofl(n)
 k=tofl(k)
 $! gamma(n+1)/(gamma(k+1)*gamma(n-k+1))
''')
_x(r'''$, isprime_(n):
 n=need_int(n)
 if $I(n)>>1024:
  err('Number too large $) isPrime')
 $! 'true' if isprime($I(n))$( 'false'
$, round_(x,d=0):
 if $5(x)$+ $. $@(x):
  x=evalf(x)
 if $@(x):
  if $m(x)$+ d==0:
   $! nfloor(nadd(x,$|))if $a(x)>=0 $(-nfloor(nadd(nneg(x),$|))
  v=tofl(x)
  if $. finite(v):
   $! x
  p=10.0**d
  r=$P.floor($I(v)*p+0.5)/p
  $! r if v>=0 $(-r
 $!('round',x,d)
$, ipart_(x):
 if $5(x)$+ $. $@(x):
  x=evalf(x)
 if $@(x):
  if $/(x)is $C:
   $! $C($q(x))
  $! nfloor(x)if $a(x)>=0 $(-nfloor(nneg(x))
 $!('ipart',x)
$, fpart_(x):
 i=ipart_(x)
 if $&(i,'ipart'):
  $!('fpart',x)
 $! $b(x,i)
$, approx_(e):
 $! evalf(e)
$, exact_(e,tol=$#):
 if tol is $. $#:
  tol=tofl(tol)
 $! exactify(e,tol)
$, approxfraction(e,tol=$#):
 t=tofl(tol)if tol is $. $# $( 5e-14
 $! lmap($4 v:float2rat(tofl(evalf(v)),t)if $5(v)$( exactify(v,t),e)
$, left_(e,n=$#):
 if isrel(e):
  $! e[1]
 if $[(e):
  $!('$G',)+e[1:1+n]
 if isstr(e):
  $!('$u',e[1][:n])
 err("Argument error")
$, right_(e,n=$#):
 if isrel(e):
  $! e[2]
 if $[(e):
  $!('$G',)+(e[$3(e)-n:]if n $(())
 if isstr(e):
  $!('$u',e[1][$3(e[1])-n:]if n $( '')
 err("Argument error")
$, mid_(e,start,n=$#):
 if isstr(e):
  s=e[1][start-1:]
  $!('$u',s if n is $# $( s[:n])
 xs=$G(e[1:])[start-1:]
 $!('$G',)+$1(xs if n is $# $( xs[:n])
$, dim_(e):
 if $[(e):
  $! $3(e)-1
 if ismat(e):
  r,c=dims(e)
  $!('$G',r,c)
 if isstr(e):
  $! $3(e[1])
 err("Argument error")
$, max_(a,b=$#):
 if b is $#:
  xs=$G(a[1:])if $[(a)$([a]
  $! maxexpr(xs)
 $! lmap2($4 x,y:x if cmpv(x,y)>=0 $( y,a,b)
$, min_(a,b=$#):
 if b is $#:
  xs=$G(a[1:])if $[(a)$([a]
  $}=$#
  bv=$#
  $) x in xs:
   v=$S(x)
   if $} is $# or v<bv:
    $}=x
    bv=v
  $! $}
 $! lmap2($4 x,y:x if cmpv(x,y)<=0 $( y,a,b)
$, cmpv(x,y):
 if $5(x)$+ $5(y):
  d=$S($b(x,y))
  d=d.$Q if $/(d)is $0 $( d
  $! 1 if d>0 $((-1 if d<0 $( 0)
 err("Cannot compare")
$, when_(c,a,b=$#,u=$#):
 t=tobool(c)
 if t is $F:
  $! a
 if t is $2:
  $! b if b is $. $# $( '$L'
 if b is $#:
  $!('when',c,a)
 if u is $#:
  $!('when',c,a,b)
 $! u
$, piecewise_(*a):
 a=$G(a)
 if $3(a)%2==1:
  r=a[-1]
  a=a[:-1]
 $(:
  r='$L'
 $) i in $*($3(a)-2,-1,-2):
  r=when_(a[i+1],a[i],r)
 $! r
$, string_(e):
 if isstr(e):
  $! e
 $!('$u',fmt(e))
$, char_(n):
 $!('$u',chr(need_int(n)))
$, ord_(s):
 $! ord(s[1][0])
$, instring_(s,t,start=1):
 i=s[1].find(t[1],start-1)
 $! i+1
$, polyeval(L,x):
 r=0
 $) c in L[1:]:
  r=$c($9(r,x),c)
 $! $;(r)
$, randpoly(v,n):
 import random
 $! $6([$9(random.randint(-9,9),pw(v,k))$) k in $*(n+1)])
$, randmat(r,c):
 import random
 $! mk([[random.randint(-9,9)$) _ in $*(c)]$) _ in $*(r)])
$, newmat(r,c):
 $! mk([[0]*c $) _ in $*(r)])
$, newlist(n):
 $!('$G',)+(0,)*n
$, rand_(n=$#):
 import random
 if n is $#:
  $! random.random()
 $!('$G',)+$1(random.random()$) _ in $*(n))
$, randint_(a,b,n=$#):
 import random
 if n is $#:
  $! random.randint(a,b)
 $!('$G',)+$1(random.randint(a,b)$) _ in $*(n))
$, count_(*$R):
 n=0
 $) a in $R:
  n+=($3(a)-1)if $[(a)$( 1
 $! n
$, erf(x):
 if $I(x)<2.5:
  s=0.0
  t=x
  k=0
  $H $F:
   term=t/(2*k+1)
   s+=term
   k+=1
   t=-t*x*x/k
   if $I(term)<1e-17:
    $X
  $! 2/$P.$T($P.pi)*s
 z=$I(x)
 t=0.0
 $) k in $*(60,0,-1):
  t=(k/2.0)/(z+t)
 erfc=$P.exp(-z*z)/$P.$T($P.pi)/(z+t)
 $!(1-erfc)if x>0 $((erfc-1)
$, numarg(v):
 if v=='$]':
  $! $C('$]')
 if v==('*',-1,'$]'):
  $! $C('-$]')
 if $5(v):
  x=cv(v)if $. $@(v)$( tofl(v)
  if x is $. $# $+ $/(x)is $. $0:
   $! x
 err('Numeric argument required')
$, normcdf(lo,hi,mu=0.0,sig=1.0):
 mu=numarg(mu)
 sig=numarg(sig)
 $, F(v):
  if v=='$]':
   $! 1.0
  if v==('*',-1,'$]'):
   $! 0.0
  z=(numarg(v)-mu)/sig
  $! 0.5*(1+erf(z/$P.$T(2)))
 $! F(hi)-F(lo)
$, normpdf(x,mu=0.0,sig=1.0):
 x=numarg(x)
 s=numarg(sig)
 $! $P.exp(-0.5*((x-numarg(mu))/s)**2)/(s*$P.$T(2*$P.pi))
$, invnorm(p,mu=0.0,sig=1.0):
 p=numarg(p)
 mu=numarg(mu)
 sig=numarg(sig)
 if $. 0<p<1:
  err('Area must be between 0 $+ 1')
 lo,hi=-40.0,40.0
 $) _ in $*(200):
  m=0.5*(lo+hi)
  if 0.5*(1+erf(m/$P.$T(2)))<p:
   lo=m
  $(:
   hi=m
 $! mu+sig*0.5*(lo+hi)
$, binompdf(n,p,x=$#):
 if x is $#:
  $!('$G',)+$1(binompdf(n,p,k)$) k in $*(n+1))
 if $m(p):
  $! $9(binom(n,x),pw(p,x),pw($b(1,p),n-x))
 p=tofl(p)
 $! binom(n,x)*p**x*(1-p)**(n-x)
$, binomcdf(n,p,a,b=$#):
 if b is $#:
  a,b=0,a
 $! $6([binompdf(n,p,k)$) k in $*($q(a),$q(b)+1)])
$, poisspdf(lam,x):
 $! evalf($9(pw(lam,x),pw('e',$o(lam)),Q(1,fact_int(x))))
$, poisscdf(lam,a,b=$#):
 if b is $#:
  a,b=0,a
 $! $6([poisspdf(lam,k)$) k in $*($q(a),$q(b)+1)])
$, geompdf(p,x):
 $! $9(p,pw($b(1,p),x-1))
$, geomcdf(p,a,b=$#):
 if b is $#:
  a,b=1,a
 $! $6([geompdf(p,k)$) k in $*($q(a),$q(b)+1)])
$, fact_int(n):
 r=1
 $) k in $*(2,n+1):
  r*=k
 $! r
$, toang(x):
 a=SET['$p']
 if a=='deg':
  $! $9(x,$Y('pi',180))
 if a=='grad':
  $! $9(x,$Y('pi',200))
 $! x
$, fromang(x):
 a=SET['$p']
 if a=='deg':
  $! $;($9(x,$Y(180,'pi')))
 if a=='grad':
  $! $;($9(x,$Y(200,'pi')))
 $! x
TRIG=('sin','cos','tan','sec','csc','cot')
ITRIG=('$w','arccos','$t','arcsec','arccsc','arccot')
''')
_x(r'''$, mathfn($D):
 $, f(*a):
  if $D in TRIG $+ SET['$p']!='rad':
   $! lmap($4 u:fn($D,toang(u)),a[0])
  if $D in ITRIG $+ SET['$p']!='rad':
   $! lmap($4 u:fromang(fn($D,u)),a[0])
  if $3(a)==1:
   $! lmap($4 u:fn($D,u),a[0])
  $! fn($D,*a)
 $! f
$, angle_fn(z):
 $! lmap($4 u:fromang(fn('$p',u)),z)
F={}
$) _n in('sin','cos','tan','sec','csc','cot','$w','arccos',
 '$t','arcsec','arccsc','arccot','sinh','cosh','tanh',
 'sech','csch','coth','arcsinh','arccosh','arctanh',
 'arcsech','arccsch','arccoth','ln','exp','$I','sign',
 'floor','ceiling','$Q','imag','conj','fact'):
 F[_n]=mathfn(_n)
ALIAS={'asin':'$w','acos':'arccos','atan':'$t','asinh':'arcsinh',
 'acosh':'arccosh','atanh':'arctanh','ceil':'ceiling',
 'factorial':'fact','derivative':'d','$l':'$l',
 'int_':'$l','sumseq':'sumseq','prodseq':'prodseq',
 'lim':'limit','nderiv':'nderivative','polycoef':'polycoeffs',
 'stddevsamp':'stddev','varsamp':'variance','cumsum':'cumulativesum',
 'nsolve':'nsolve','arg':'$p','inv':'inverse','mat2list':'matlist',
 'list2mat':'listmat','explist':'explist','tran':'transpose',
 'log10':'log10','sqr':'$T'}
F['$T']=$4 u:lmap($T,u)
F['root']=$4 u,n=2:lmap($4 v:fn('root',v,n),u)
F['log']=$4 u,b=$#:lmap($4 v:fn('ln',v)if b is $# $( fn('log',v,b),u)
F['atan2']=$4 y,x:lmap2($4 b,a:fromang(fn('$p',$c(a,$9('i',b)))),y,x)
F['log10']=$4 u:lmap($4 v:fn('log',v,10),u)
F['$p']=angle_fn
F['round']=$4 x,d=0:lmap($4 v:round_(v,d),x)
F['ipart']=$4 x:lmap(ipart_,x)
F['$q']=$4 x:lmap($4 v:fn('floor',v),x)
F['fpart']=$4 x:lmap(fpart_,x)
F['gcd']=$4 a,b:lmap2(gcd_,a,b)
F['lcm']=$4 a,b:lmap2(lcm_,a,b)
F['mod']=$4 a,b:lmap2(mod_,a,b)
F['remain']=$4 a,b:lmap2(remain_,a,b)
F['intdiv']=$4 a,b:lmap2(intdiv_,a,b)
F['ncr']=$4 a,b:lmap2(ncr_,a,b)
F['npr']=$4 a,b:lmap2(npr_,a,b)
F['isprime']=isprime_
F['approx']=approx_
F['exact']=exact_
F['approxrational']=approxfraction
F['getnum']=$4 e:lmap(getnum,e)
F['getdenom']=$4 e:lmap(getden,e)
F['polyeval']=polyeval
F['polygcd']=$4 a,b:poly_gcd_expr(a,b)
F['randpoly']=randpoly
F['texpand']=$4 e:lmap($4 v:texpand(v),e)
F['tcollect']=$4 e:lmap($4 v:tcollect(v),e)
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
F['rref']=$4 A,tol=$#:rref(A,$F)
F['ref']=$4 A,tol=$#:ref_(A)
F['inverse']=m_inv
F['rowdim']=$4 A:dims(A)[0]
F['coldim']=$4 A:dims(A)[1]
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
F['lu']=$4 A,tol=$#:('$G',)+lu(A)
F['qr']=$4 A,tol=$#:('$G',)+qr(A)
F['newmat']=newmat
F['newlist']=newlist
F['randmat']=randmat
F['matlist']=matlist
F['listmat']=listmat
F['simult']=simult
F['cumulativesum']=cumsum
F['sum']=$4 L,a=1,b=$#:lsum(L,a,b)if $[(L)$( colwise(L,lsum)
F['product']=$4 L,a=1,b=$#:lprod(L,a,b)if $[(L)$( colwise(L,lprod)
F['mean']=$4 L,f=$#:mean(L,f)if $[(L)$( colwise(L,mean)
F['median']=median
F['stddev']=$4 L:stddev(L)
F['stddevpop']=$4 L:stddev(L,$F)
F['variance']=$4 L:variance(L)
F['varpop']=$4 L:variance(L,$F)
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
F['getmode']=$4*a:('$u','$p='+SET['$p']+' mode='+SET['mode']+' $A='+SET['$A'])
$, colwise(M,f):
 cols=$j(transpose(M))
 $! mk([[f(('$G',)+$1(c))$) c in cols]])
$, ref_(A):
 $! rref(A,$2)
$, conv(e,$D,$R):
 if $D=='decimal':
  $! evalf(e)
 if $D=='approxfraction':
  $! approxfraction(e,$R[0]if $R $( $#)
 if $D in('dms','dd','rad','grad','deg'):
  $! angconv(e,$D)
 if $D=='polar':
  if $[(e)or ismat(e):
   $! polar_vec(e)
  r=$-(fn('$I',e))
  th=fn('$p',e)
  $!('$u','('+fmt(r)+'\u2220'+fmt(fromang(th))+')')
 if $D=='rect':
  if $[(e)or ismat(e):
   $! e
  r,i=reim(e)
  $! $c(r,$9('i',i))
 if $D=='cylind':
  $! cylind(e)
 if $D=='sphere':
  $! sphere(e)
 if $D in('base2','base10','base16'):
  $! baseconv(e,$D)
 if $D=='exp':
  $! toexp(e)
 if $D=='ln':
  $! toln(e)
 if $D=='logbase':
  $! tologbase(e,$R[0])
 if $D=='sin':
  $! pyth_to(e,'sin')
 if $D=='cos':
  $! pyth_to(e,'cos')
 err("Unknown conversion "+$D)
$, angconv(e,$D):
 if $D=='dms':
  v=tofl(evalf(e))
  if SET['$p']=='rad':
   v=v*180/$P.pi
  $J SET['$p']=='grad':
   v=v*0.9
  sg='-' if v<0 $( ''
  v=$I(v)
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
  $!('$u',sg+$u(d)+'\u00b0'+$u(m)+"'"+ss+'"')
 if $D=='dd':
  if SET['$p']=='rad':
   $! evalf($9(e,$Y(180,'pi')))
  $! evalf(e)
 if $D=='rad':
  if SET['$p']=='deg':
   $! $9(e,$Y('pi',180))
  if SET['$p']=='grad':
   $! $9(e,$Y('pi',200))
  $! e
 if $D=='grad':
  if SET['$p']=='deg':
   $! $9(e,Q(10,9))
  if SET['$p']=='rad':
   $! $9(e,$Y(200,'pi'))
  $! e
 if SET['$p']=='rad':
  $! $9(e,$Y(180,'pi'))
 $! e
''')
_x(r'''$, baseconv(e,$D):
 n=need_int(e)
 if $D=='base10':
  $! n
 if $D=='base2':
  s=bin(n)if n>=0 $( '-'+bin(-n)
  $!('$u',s.replace('0b','0b'))
 s=hex(n)if n>=0 $( '-'+hex(-n)
 $!('$u',s.replace('0x','0h').upper().replace('0H','0h'))
$, toexp(e):
 if $/(e)is $. $1 or e[0]=='Q':
  $! e
 $R=[toexp(a)$) a in e[1:]]
 h=e[0]
 if $3($R)==1:
  u=$R[0]
  if h=='sinh':
   $! $9($|,$b(pw('e',u),pw('e',$o(u))))
  if h=='cosh':
   $! $9($|,$c(pw('e',u),pw('e',$o(u))))
  if h=='tanh':
   $! $Y($b(pw('e',u),pw('e',$o(u))),$c(pw('e',u),pw('e',$o(u))))
  if h=='sin':
   iu=$9('i',u)
   $! $Y($b(pw('e',iu),pw('e',$o(iu))),$9(2,'i'))
  if h=='cos':
   iu=$9('i',u)
   $! $9($|,$c(pw('e',iu),pw('e',$o(iu))))
  if h=='arcsinh':
   $! fn('ln',$c(u,$T($c(pw(u,2),1))))
  if h=='arccosh':
   $! fn('ln',$c(u,$T($b(pw(u,2),1))))
  if h=='arctanh':
   $! $9($|,fn('ln',$Y($c(1,u),$b(1,u))))
 $! simp((h,)+$1($R))
$, toln(e):
 if $/(e)is $. $1 or e[0]=='Q':
  $! e
 $R=[toln(a)$) a in e[1:]]
 if e[0]=='log':
  b=$R[1]if $3($R)>1 $( 10
  $! $Y(fn('ln',$R[0]),fn('ln',b))
 $! simp((e[0],)+$1($R))
$, tologbase(e,b):
 e=toln(e)
 $, walk(t):
  if $/(t)is $. $1 or t[0]=='Q':
   $! t
  if t[0]=='ln':
   $! $Y(('log',walk(t[1]),b),('log','e',b))
  $!(t[0],)+$1(walk(a)$) a in t[1:])
 $!('hold',walk(e))
''')
_x(r'''VERSION='1.0'
ENV={}
UFUN={}
ASSUME=[]
STATE={'ans':0,'$A':$2,'tmpf':[]}
COMPLEXF=('csolve','czeros','cfactor','cpolyroots','eigvl','eigvc','conj',
 '$Q','imag','$p')
$, isfunc(n):
 $!(n in F or n in SF or n in UFUN or n in ALIAS
 or n in STATE['tmpf']or n in('$~','$T','log','root'))
$, lookup(n):
 if n in ENV:
  $! ENV[n]
 if n=='ans':
  $! STATE['ans']
 if n=='i':
  STATE['$A']=$F
 $! n
$, ev(t):
 tt=$/(t)
 if tt is $q or tt is $C:
  $! t
 if tt is $u:
  $! lookup(t)
 h=t[0]
 if h=='+':
  a=ev(t[1])
  b=ev(t[2])
  $! vadd(a,b)
 if h=='-':
  $! vsub(ev(t[1]),ev(t[2]))
 if h=='$o':
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
  $! lmap($4 a:fn('fact',a),ev(t[1]))
 if h=='%':
  $! lmap($4 a:$Y(a,100),ev(t[1]))
 if h=='deg':
  v=ev(t[1])
  if SET['$p']=='rad':
   $! lmap($4 a:$9(a,$Y('pi',180)),v)
  if SET['$p']=='grad':
   $! lmap($4 a:$9(a,Q(10,9)),v)
  $! v
 if h in('=','<','>','<=','>=','/='):
  $! rel(h,ev(t[1]),ev(t[2]))
 if h=='$+':
  $! land(ev(t[1]),ev(t[2]))
 if h=='or':
  $! lor(ev(t[1]),ev(t[2]))
 if h=='$.':
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
 if h=='$G':
  $!('$G',)+$1(ev(a)$) a in t[1:])
 if h=='mat':
  $!('mat',)+$1(('$G',)+$1(ev(a)$) a in r[1:])$) r in t[1:])
 if h=='$u':
  $! t
 if h=='&':
  a=ev(t[1])
  b=ev(t[2])
  $!('$u',string_(a)[1]+string_(b)[1])
 if h=='index':
  $! ev_index(ev(t[1]),[ev(a)$) a in t[2:]])
 if h=='prime':
  $! t[1]+"'"*t[2]
 if h=='primecall':
  $!('call',t[1]+"'"*t[2])+$1(ev(a)$) a in t[3:])
 if h=='polar':
  STATE['$A']=$F
  $! $9(ev(t[1]),pw('e',$9('i',toang(ev(t[2])))))
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
 if $&(c,'$+'):
  $! split_and(c[1])+split_and(c[2])
 $![c]
$, ev_with(t):
 conds=split_and(t[2])
 pairs={}
 ineq=[]
 $) c in conds:
  if $&(c,'=')$+ $/(c[1])is $u:
   pairs[c[1]]=ev(c[2])
  $(:
   v=evw(c,$G(pairs.keys()))
   if $&(v,'$+'):
    ineq.extend($G(v[1:]))
   $J v!='true':
    ineq.$%(v)
 n0=$3(ASSUME)
 ASSUME.extend(ineq)
 try:
  r=evw(t[1],$G(pairs.keys()))
 finally:
  del ASSUME[n0:]
 if pairs:
  r=subsd(unhold(r),pairs)
 $) c in ineq:
  r=assume_sign(r,c)
 $! r
$, assume_sign(r,c):
 h=head(c)
 if h $. in('<','>','<=','>='):
  $! r
 a,b=c[1],c[2]
 if $/(a)is $u $+ b==0:
  v=a
  pos=h in('>','>=')
 $J $/(b)is $u $+ a==0:
  v=b
  pos=h in('<','<=')
 $(:
  $! r
 rep=v if pos $( $o(v)
 r=$W(r,('$I',v),rep)
 r=$W(r,('sign',v),1 if pos $(-1)
 $! r
$, target_fn(t):
 if $&(t,'call'):
  $! t[1],[p $) p in t[2:]]
 if $&(t,'*')$+ $/(t[1])is $u:
  p=t[2]
  $! t[1],[p]
 $! $#
$, ev_store(raw,tgt):
 tf=target_fn(tgt)
 if tf is $. $#:
  $! ev_define(tgt,raw)
 if $/(tgt)is $. $u:
  err('Invalid variable $D')
 if tgt in SPECIAL or tgt in F or tgt in SF:
  err('Reserved $D')
 v=ev(raw)
 ENV[tgt]=unhold(v)if $. $&(v,'$u')$( v
 $! v
$, ev_define(lhs,rhs):
 tf=target_fn(lhs)
 if tf is $#:
  if $/(lhs)is $u:
   $! ev_store(rhs,lhs)
  err('Invalid definition')
 $D,params=tf
 $) p in params:
  if $/(p)is $. $u:
   err('Invalid parameter')
 body=unhold(evw(rhs,params))
 UFUN[$D]=(params,body)
 if $D in STATE['tmpf']:
  STATE['tmpf'].remove($D)
 $!('$u','Done')
$, ev_index(a,idx):
 if $. idx:
  err('Invalid index')
 if $&(a,'$G'):
  i=idx[0]
  if $. $i(i)or i<1 or i>=$3(a):
   err('Invalid index')
  $! a[i]
 if $&(a,'mat'):
  $) k in idx:
   if $. $i(k)or k<1:
    err('Invalid index')
  if $3(idx)==1:
   if $3(a)==2:
    if idx[0]>=$3(a[1]):
     err('Invalid index')
    $! a[1][idx[0]]
   if idx[0]>=$3(a):
    err('Invalid index')
   $!('mat',a[idx[0]])
  if idx[0]>=$3(a)or idx[1]>=$3(a[idx[0]]):
   err('Invalid index')
  $! a[idx[0]][idx[1]]
 if $&(a,'$u'):
  k=idx[0]
  if $3(idx)!=1 or $. $i(k)or k<1 or k>$3(a[1]):
   err('Invalid index')
  $!('$u',a[1][k-1])
 err('Invalid index')
$, ev_conv(t):
 e=t[1]
 $D=t[2]
 $R=[ev(a)$) a in t[3:]]
 if $D=='$G':
  if e=='exp':
   $! explist($R[0],$R[1])
  if e=='mat':
   $! matlist($R[0])
  err('Unknown conversion')
 if $D=='mat' $+ e=='$G':
  $! listmat(*$R)
 v=ev(e)
 v=finalize(v,$F)
 $! builtin($D,conv,(v,$D,$R))
$, explist(e,v):
 $?=[]
 parts=e[1:]if $&(e,'or')$((e,)
 $) p in parts:
  if $&(p,'=')$+ p[1]==v:
   $?.$%(p[2])
 $!('$G',)+$1($?)
$, call($D,raw):
 $D=ALIAS.get($D,$D)
 if $D in UFUN:
  params,body=UFUN[$D]
  $R=[ev(a)$) a in raw]
  if $3($R)!=$3(params):
   err('Wrong number of arguments')
  $! subsd(body,dict(zip(params,$R)))
 f=SF.get($D)
 if f is $. $#:
  if $D in COMPLEXF:
   STATE['$A']=$F
  $! builtin($D,f,(raw,))
 f=F.get($D)
 if f is $. $#:
  $R=[ev(a)$) a in raw]
  if $D in COMPLEXF:
   STATE['$A']=$F
  $! builtin($D,f,$R)
 if $D=='$~':
  s=ev(raw[0])
  $! ev(parse(s[1],isfunc))
 $R=[ev(a)$) a in raw]
 $!('call',$D)+$1($R)
''')
_x(r'''$, builtin($D,f,$R):
 try:
  $! f(*$R)
 $< TypeError as ex:
  msg=$u(ex)
  if 'positional' in msg or 'takes' in msg or 'required' in msg or 'missing' in msg:
   err('Wrong number of arguments $) '+$D)
  err('Invalid argument $) '+$D)
 $<(IndexError,$O,AttributeError,KeyError):
  err('Invalid argument $) '+$D)
 $< $U:
  err('Number too large in '+$D)
$, var_of(raw):
 if $/(raw)is $u:
  $! raw,$#
 if $&(raw,'='):
  if $/(raw[1])is $. $u:
   err('Variable expected')
  $! raw[1],ev(raw[2])
 err('Variable expected')
$, $s(a,lo,hi):
 if $3(a)<lo or $3(a)>hi:
  err('Wrong number of arguments')
$, $d(a,k=1):
 v,val=var_of(a[k])
 e=unhold(evw(a[0],[v]))
 $! e,v,val
$, post_subst(r,v,val):
 if val is $. $#:
  $! $W(r,v,val)
 if v in ENV:
  $! $W(r,v,ENV[v])
 $! r
$, sf_d(a):
 $s(a,2,3)
 e,v,val=$d(a)
 n=ev(a[2])if $3(a)>2 $( 1
 if $. $i(n):
  err('Order must be an integer')
 r=lmap($4 u:nice(diff(u,v,n)),e)
 $! post_subst(r,v,val)
$, sf_int(a):
 $s(a,2,4)
 e,v,val=$d(a)
 if $3(a)==2:
  $! lmap($4 u:nice(integrate(u,v)),e)
 if $3(a)==3:
  c=ev(a[2])
  $! lmap($4 u:$c(nice(integrate(u,v)),c),e)
 lo=ev(a[2])
 hi=ev(a[3])
 $! lmap($4 u:nice(defint(u,v,lo,hi)),e)
$, sf_limit(a):
 $s(a,3,4)
 e,v,val=$d(a)
 pt=ev(a[2])
 dirn=0
 if $3(a)>3:
  d=ev(a[3])
  if $. $@(d):
   err('Direction must be -1, 0 or 1')
  dirn=0 if d==0 $((1 if $a(d)>0 $(-1)
 $, L(u):
  r=limit(u,v,pt,dirn)
  if $&(r,'limit'):
   $!('limit',u,v,pt)if dirn==0 $(('limit',u,v,pt,dirn)
  $! nice(r)
 $! lmap(L,e)
$, cs_bounds(a,i):
 $! ev(a[i]),ev(a[i+1])
$, sf_sum(a):
 $s(a,4,4)
 e,v,val=$d(a)
 lo,hi=cs_bounds(a,2)
 r=sumseq(e,v,lo,hi)
 $! prefer_fact(nice(r))
$, prefer_fact(r):
 if $&(r,'+')$+ $. $`(r)$+ $3(${(r))==1:
  try:
   f=$v(r)
   if $&(f,'hold')$+ $&(f[1],'*'):
    $! f
  $< $=:
   pass
 $! r
$, sf_prod(a):
 $s(a,4,4)
 e,v,val=$d(a)
 lo,hi=cs_bounds(a,2)
 $! prodseq(e,v,lo,hi)
$, sf_seq(a):
 $s(a,4,5)
 e,v,val=$d(a)
 lo,hi=cs_bounds(a,2)
 st=ev(a[4])if $3(a)>4 $( 1
 $?=[]
 k=lo
 cnt=0
 $H ncmp(k,hi)<=0 if $@(k)$( $2:
  $?.$%($W(e,v,k))
  k=nadd(k,st)
  cnt+=1
  if cnt>5000:
   err('Too many elements')
 $!('$G',)+$1($?)
$, sf_taylor(a):
 $s(a,3,4)
 e,v,val=$d(a)
 n=ev(a[2])
 pt=ev(a[3])if $3(a)>3 $( 0
 $! lmap($4 u:taylor(u,v,n,pt),e)
$, sf_series(a):
 $s(a,3,4)
 e,v,val=$d(a)
 n=ev(a[2])
 pt=ev(a[3])if $3(a)>3 $( 0
 $! lmap($4 u:series_cmd(u,v,n,pt),e)
$, sf_dominant(a):
 $s(a,2,3)
 e,v,val=$d(a)
 pt=ev(a[2])if $3(a)>2 $( 0
 $! lmap($4 u:dominant(u,v,pt),e)
$, solvevars(rawvs):
 vs=[]
 gs=[]
 $) r in rawvs:
  if $&(r,'$G'):
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
 if $&(e,'$+'):
  $?=[]
  $) p in e[1:]:
   $?.extend(eqlist(p))
  $! $?
 if $&(e,'$G'):
  $! $G(e[1:])
 $![e]
$, cons_for(v):
 $?=[]
 $) c in ASSUME:
  if has(c,v):
   $?.$%(c)
 $! $?
$, sf_solve(a,$A=$2):
 if $3(a)<2:
  err('Wrong number of arguments')
 vs,gs=solvevars(a[1:])
 e=evw(a[0],vs)
 eqs=eqlist(e)
 if $3(vs)==1 $+ $3(eqs)==1:
  v=vs[0]
  eq=eqs[0]
  if gs[0]is $. $#:
   f=$b(eq[1],eq[2])if $&(eq,'=')$( eq
   r=nsolve(f,v,tofl(evalf(gs[0])))
   $!('=',v,r)if r is $. $# $( 'false'
  r=solve(eq,v,$A,cons_for(v))
  if r is $#:
   f=$b(eq[1],eq[2])if $&(eq,'=')$( eq
   ns=numeric_solve(f,v,$A)if head(eq)=='=' or head(eq)is $# $( $#
   if ns:
    r=sols_to_bool(v,apply_constraints(ns,v,cons_for(v)))
   $(:
    $!('solve',eq,v)
  $! finish_sol(r)
 $e=solve_system(eqs,vs,$A,gs if any([g is $. $# $) g in gs])$( $#)
 if $e is $#:
  $!('solve',e)+$1(vs)
 if $. $e:
  $! 'false'
 $?=[]
 $) s in $e:
  conj=[('=',v,clean(s.get(v,v)))$) v in vs]
  $?.$%(conj[0]if $3(conj)==1 $(('$+',)+$1(conj))
 $! finish_sol($?[0]if $3($?)==1 $(('or',)+$1($?))
$, finish_sol(r):
 $! r
$, sf_csolve(a):
 $! sf_solve(a,$F)
$, sf_zeros(a,$A=$2):
 $s(a,2,2)
 vs,gs=solvevars(a[1:])
 e=evw(a[0],vs)
 if $3(vs)==1 $+ $. $&(e,'$G'):
  r=zeros(e,vs[0],$A,cons_for(vs[0]))
  if r is $#:
   ns=numeric_solve(e,vs[0],$A)
   $!('$G',)+$1(ns or[])
  $! r
 eqs=eqlist(e)
 $e=solve_system(eqs,vs,$A)
 if $. $e:
  $!('$G',)
 $! mk([[clean(s.get(v,v))$) v in vs]$) s in $e])
$, sf_czeros(a):
 $! sf_zeros(a,$F)
$, sf_nsolve(a):
 $s(a,2,4)
 v,g=var_of(a[1])
 e=unhold(evw(a[0],[v]))
 f=$b(e[1],e[2])if $&(e,'=')$( e
 lo=tofl(evalf(ev(a[2])))if $3(a)>2 $( $#
 hi=tofl(evalf(ev(a[3])))if $3(a)>3 $( $#
 $) c in cons_for(v):
  b=bounds([c],v)if $2 $( $#
 cb=bounds(cons_for(v),v)
 if cb is $. $#:
  lo,hi=tofl(evalf(cb[0])),tofl(evalf(cb[1]))
 r=nsolve(f,v,tofl(evalf(g))if g is $. $# $( $#,lo,hi)
 if r is $#:
  $!('$u','No solution found')
 $! r
''')
_x(r'''$, sf_desolve(a):
 $s(a,3,3)
 x=a[1]
 y=a[2]
 if $/(x)is $. $u or $/(y)is $. $u:
  err('Variable expected')
 parts=split_and(a[0])
 ode=$#
 conds=[]
 $) p in parts:
  if $&(p,'=')$+ $&(p[1],'primecall')$+ p[1][1]==y:
   conds.$%((p[1][2],evw(p[1][3],[x,y]),evw(p[2],[x,y])))
  $J $&(p,'=')$+ $&(p[1],'*')$+ p[1][1]==y $+ $. hasprime(p):
   conds.$%((0,ev(p[1][2]),ev(p[2])))
  $J $&(p,'=')$+ $&(p[1],'call')$+ p[1][1]==y:
   conds.$%((0,ev(p[1][2]),ev(p[2])))
  $(:
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
 if $/(t)is $. $1:
  $! $2
 if t[0]in('prime','primecall'):
  $! $F
 $) a in t[1:]:
  if hasprime(a):
   $! $F
 $! $2
$, bnd_args(a,i,v):
 lo=ev(a[i])if $3(a)>i $( $#
 hi=ev(a[i+1])if $3(a)>i+1 $( $#
 cb=bounds(cons_for(v),v)
 if cb is $. $#:
  lo,hi=cb
 $(:
  $) c in cons_for(v):
   h=head(c)
   if h in('>','>=')$+ c[1]==v:
    lo=c[2]
   $J h in('<','<=')$+ c[1]==v:
    hi=c[2]
 $! lo,hi
$, sf_fmin(a,kind='min'):
 $s(a,2,4)
 e,v,val=$d(a)
 lo,hi=bnd_args(a,2,v)
 r=fextreme(e,v,kind,lo,hi)
 if r is $#:
  $!('f'+kind,e,v)
 $! r
$, sf_fmax(a):
 $! sf_fmin(a,'max')
$, sf_nfmin(a,kind='min'):
 $s(a,2,4)
 e,v,val=$d(a)
 lo,hi=bnd_args(a,2,v)
 $! nfextreme(e,v,kind,tofl(evalf(lo))if lo is $. $# $( $#,
 tofl(evalf(hi))if hi is $. $# $( $#)
$, sf_nfmax(a):
 $! sf_nfmin(a,'max')
$, sf_nint(a):
 $s(a,4,4)
 e,v,val=$d(a)
 lo,hi=cs_bounds(a,2)
 $! nint(e,v,lo,hi)
$, sf_arclen(a):
 $s(a,4,4)
 e,v,val=$d(a)
 lo,hi=cs_bounds(a,2)
 $! nice(arclen(e,v,lo,hi))
$, pt_arg(a):
 if $3(a)==2 $+ $&(a[1],'='):
  v,p=var_of(a[1])
  e=evw(a[0],[v])
  $! e,v,p
 $s(a,3,3)
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
 $s(a,3,4)
 x,_=var_of(a[1])
 y,_=var_of(a[2])
 e=evw(a[0],[x,y])
 n=ev(a[3])if $3(a)>3 $( 1
 $! impdif(e,x,y,n)
$, rc_args(a):
 v,val=var_of(a[1])
 e=unhold(evw(a[0],[v]))
 h=ev(a[2])if $3(a)>2 $( 0.001
 if val is $#:
  val=v
 $! e,v,val,h
$, sf_avgrc(a):
 $s(a,2,3)
 e,v,val,h=rc_args(a)
 $! lmap($4 u:$;(avgrc(u,v,val,h)),e)
$, sf_central(a):
 $s(a,2,3)
 e,v,val,h=rc_args(a)
 $! lmap($4 u:$;(centraldiff(u,v,val,h)),e)
$, sf_nderiv(a):
 $s(a,2,3)
 v,val=var_of(a[1])
 e=unhold(evw(a[0],[v]))
 n=ev(a[2])if $3(a)>2 $( 1
 if val is $#:
  val=ENV.get(v)
  if val is $#:
   err('Value required: var=value')
 $! evalf($W(diff(e,v,n),v,val))
$, opt_var(a,i):
 if $3(a)>i:
  v,_=var_of(a[i])
  $! v
 $! $#
$, sf_expand(a):
 $s(a,1,2)
 v=opt_var(a,1)
 e=ev(a[0])
 $! expand_full(unhold(e),v)
$, sf_factor(a,$A=$2):
 $s(a,1,2)
 v=opt_var(a,1)
 e=unhold(ev(a[0]))
 $! $v(e,v,$A)
$, sf_cfactor(a):
 $! sf_factor(a,$F)
$, sf_comdenom(a):
 $s(a,1,2)
 $! comdenom(unhold(ev(a[0])))
$, sf_propfrac(a):
 $s(a,1,2)
 v=opt_var(a,1)
 $! lmap($4 u:propfrac(u,v),unhold(ev(a[0])))
$, polyvar(e,a,i):
 v=opt_var(a,i)
 if v is $#:
  ss=${(e)
  v='x' if 'x' in ss or $. ss $( ss[0]
 $! v
$, sf_polycoeffs(a):
 $s(a,1,2)
 e=unhold(ev(a[0]))
 v=polyvar(e,a,1)
 cs=$^(e,v)
 if cs is $#:
  err('Polynomial expected')
 $H $3(cs)>1 $+ cs[-1]==0:
  cs.pop()
 $!('$G',)+$1(reversed(cs))
$, sf_polydegree(a):
 $s(a,1,2)
 e=unhold(ev(a[0]))
 v=polyvar(e,a,1)
 d=degree($;(e),v)
 if d is $#:
  err('Polynomial expected')
 if e==0:
  $!('*',-1,'$]')
 $! d
$, sf_polyquo(a,which=0):
 $s(a,2,3)
 p=unhold(ev(a[0]))
 q=unhold(ev(a[1]))
 v=polyvar($c(p,q),a,2)
 cp=$^(p,v)
 cq=$^(q,v)
 if cp is $# or cq is $#:
  err('Polynomial expected')
 qq,rr=e_divmod(cp,cq)
 $! fromcoeffs(qq if which==0 $( rr,v)
$, sf_polyrem(a):
 $! sf_polyquo(a,1)
$, sf_polyroots(a,$A=$2):
 $s(a,1,2)
 if $3(a)==1:
  L=ev(a[0])
  if $. $&(L,'$G'):
   err('List expected')
  v='X_'
  e=polyeval(L,v)
 $(:
  v,_=var_of(a[1])
  e=evw(a[0],[v])
 r=zeros(e,v,$A)
 $! r if r is $. $# $(('$G',)
$, sf_cpolyroots(a):
 $! sf_polyroots(a,$F)
$, sf_linsolve(a):
 vs,gs=solvevars(a[1:])
 e=evw(a[0],vs)
 eqs=eqlist(e)
 fs=[eqexpr(q)$) q in eqs]
 if $. is_linear_sys(fs,vs):
  err('Argument error: $f system required')
 $e=linsys(fs,vs)
 if $. $e:
  $! 'false'
 $!('$G',)+$1($e[0][v]$) v in vs)
$, sf_domain(a):
 $s(a,2,2)
 e,v,val=$d(a)
 r=domain(e,v)
 $! r if r is $. $# $(('domain',e,v)
$, sf_completesq(a):
 $s(a,2,2)
 v,_=var_of(a[1])
 e=unhold(evw(a[0],[v]))
 if $&(e,'='):
  lhs=complete_sq($b(e[1],e[2]),v,$F)
  $! lhs
 $! complete_sq(e,v,$2)
$, complete_sq(e,v,eq):
 cs=$^(e,v)
 if cs is $# or $3(cs)!=3:
  err('Quadratic expected')
 c,b,a=cs
 h=$-($Y(b,$9(2,a)))
 k=$-($b(c,$Y($9(b,b),$9(4,a))))
 sq=('^',$c(v,h),2)
 t=sq if a==1 $(('*',a,sq)
 if eq:
  $!('=',('hold',t),$o(k))
 if k==0:
  $!('hold',t)
 $!('hold',('+',t,k))
$, sf_constructmat(a):
 $s(a,5,5)
 i,_=var_of(a[1])
 j,_=var_of(a[2])
 e=evw(a[0],[i,j])
 r=ev(a[3])
 c=ev(a[4])
 $! mk([[subsd(e,{i:ii,j:jj})$) jj in $*(1,c+1)]$) ii in $*(1,r+1)])
$, sf_charpoly(a):
 $s(a,2,2)
 A=ev(a[0])
 v=a[1]if $/(a[1])is $u $( ev(a[1])
 $! charpoly(A,v)
$, sf_simplify(a):
 e=unhold(ev(a[0]))
 $! nice(pyth(e))
''')
_x(r'''SF={
 'd':sf_d,'$l':sf_int,'limit':sf_limit,'sumseq':sf_sum,
 'prodseq':sf_prod,'seq':sf_seq,'taylor':sf_taylor,'series':sf_series,
 'dominantterm':sf_dominant,'solve':sf_solve,'csolve':sf_csolve,
 'zeros':sf_zeros,'czeros':sf_czeros,'nsolve':sf_nsolve,
 'desolve':sf_desolve,'fmin':sf_fmin,'fmax':sf_fmax,'nfmin':sf_nfmin,
 'nfmax':sf_nfmax,'nint':sf_nint,'arclen':sf_arclen,
 'tangentline':sf_tangent,'normalline':sf_normal,'impdif':sf_impdif,
 'avgrc':sf_avgrc,'centraldiff':sf_central,'nderivative':sf_nderiv,
 '$;':sf_expand,'factor':sf_factor,'cfactor':sf_cfactor,
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
 if t is $F:
  $! a
 if t is $2:
  $! b if b is $. $# $( '$L'
 $! $#
$k['when']=when_simp
$, finalize(r,quiet=$2):
 if $&(r,'$u'):
  $! r
 if $. $&(r,'hold'):
  r=$-(r)if $.($&(r,'$G')or $&(r,'mat'))$( lmap($-,r)
  if needpyth(r):
   r=pyth(r)
  if SET['mode']=='approx' or $`(r):
   r=evalf(r)
  $J SET['mode']=='exact':
   r=exactify(r)
 if SET['$A']=='$Q' $+ $. STATE['$A']$+ has(r,'i')$+ $. quiet:
  err('Non-$Q result')
 $! r
$, sqtrig(e,$?):
 if $/(e)is $. $1 or e[0]=='Q':
  $!
 if e[0]=='^' $+ head(e[1])in('sin','cos')$+ $i(e[2])$+ e[2]>=2:
  $?.$%((e[1][0],e[1][1]))
 $) a in e[1:]:
  sqtrig(a,$?)
$, needpyth(r):
 if $. $&(r,'+'):
  $! $2
 $?=[]
 sqtrig(r,$?)
 $) n,u in $?:
  if(('cos' if n=='sin' $( 'sin'),u)in $?:
   $! $F
 $! $2
$, pre_register(s):
 low=s.replace(' ','').lower()
 cands=[]
 if ':=' in low:
  cands.$%(low.split(':=')[0])
 if low.$r('define'):
  cands.$%(low[6:].split('=')[0])
 $) arrow in('->','\u2192','=:'):
  if arrow in low:
   cands.$%(low.split(arrow)[-1])
 $) c in cands:
  i=c.find('(')
  if i>0:
   nm=c[:i]
   ok=$F
   $) ch in nm:
    if $.(ch.isalpha()or ch.isdigit()or ch=='_'):
     ok=$2
   if ok $+ nm $. in STATE['tmpf']:
    STATE['tmpf'].$%(nm)
$, command(c):
 p=c.split()
 if $. p:
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
 if k in('$Q','$0','rect'):
  SET['$A']='$Q' if k=='$Q' $( 'rect'
  $! 'Complex format: '+SET['$A']
 if k in('digits','$C'):
  if $3(p)>1 $+ $. p[1].isdigit():
   $! 'Use :digits n with n from 1 to 15'
  n=$q(p[1])if $3(p)>1 $( 10
  OPT['digits']=max(1,min(15,n))
  $! 'Digits: '+$u(OPT['digits'])
 if k=='ascii':
  OPT['uni']=$2
  $! 'ASCII output'
 if k in('unicode','uni'):
  OPT['uni']=$F
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
  $< $=:
   $! 'Memory information is $. available'
 if k in('mode','modes','getmode'):
  $!('$p='+SET['$p']+' mode='+SET['mode']+' $A='+SET['$A']+
 ' digits='+$u(OPT['digits']))
 if k=='test':
  _load('cashelp')
  saved=(dict(SET),dict(OPT))
  SET.update({'$p':'rad','mode':'auto','$A':'$Q'})
  OPT.update({'uni':$F,'digits':10})
  try:
   $! selftest(run)
  finally:
   SET.update(saved[0])
   OPT.update(saved[1])
 if k in('menu','m'):
  cs_menu()
  $! ''
 if k in('gui','g'):
  $! gui()
 if k=='keys':
  try:
   from ti_system import get_key
  $< ImportError:
   $! 'The key test needs the calculator (ti_system)'
  print('Press keys; esc twice to stop')
  last=''
  $H $F:
   key=get_key(1)
   print(repr(key))
   if key=='esc' $+ last=='esc':
    $! ''
   last=key
 if k in('help','?','h'):
  _load('cashelp')
  $! help(p[1]if $3(p)>1 $( $#)
 $! 'Unknown command :'+k
$, run(s):
 s=s.strip()
 if $. s:
  $! ''
 low=s.lower()
 if low[0]==':':
  $! command(low[1:])
 if low[0]=='?':
  $! command('help '+low[1:].strip())
 if low.$r('help'):
  $! command(low)
 if low.$r('delvar'):
  $) n in low[6:].replace(',',' ').split():
   ENV.pop(n,$#)
   UFUN.pop(n,$#)
  $! 'Done'
 if low in('clearaz','clear'):
  $! command('clear')
 pre_register(s)
 t=parse(s,isfunc)
 STATE['$A']=(SET['$A']!='$Q')
 r=ev(t)
 r=finalize(r)
 if $.($&(t,'define')or($&(r,'$u')$+ r[1]=='Done')):
  STATE['ans']=unhold(r)if $. $&(r,'$u')$( r
 $! fmt_top(r)
$, cs_menu():
 _load('casmenu')
 menu(run)
GUI=$F
$, gui():
 if $. GUI:
  $! 'The full-screen mode is the separate program ncasgui.'
 import casgui
 $! casgui.gui(run)
$, startgui():
 r=gui()
 if r:
  print(r)
  print('The text version is the program ncastext.')
$, start():
 try:
  import ti_draw
 $< ImportError:
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
 $< $M as ex:
  $! 'Error: '+$u(ex)
''')
_x(r'''$, cas():
 print('nCAS '+VERSION+' $) TI-Nspire CX II')
 print(('? help, m menu, g full screen, q quit')if GUI $( '? help, m menu, q quit')
 blank=0
 $H $F:
  try:
   s=input('> ')
  $<(EOFError,KeyboardInterrupt):
   $X
  s=s.strip()
  if s in('q','quit','exit',':q'):
   $X
  if $. s:
   blank+=1
   if blank>=2:
    print('($/ q $+ enter to quit)')
    blank=0
   $7
  blank=0
  if s.lower()in('m','menu'):
   try:
    cs_menu()
   $< $= as ex:
    print('Error: '+$u(ex))
   $7
  if s.lower()in('g','gui'):
   try:
    r=gui()
   $< $= as ex:
    r='Error: '+$u(ex)
   if r:
    print(r)
   $7
  try:
   $?=run(s)
   if $?:
    print($?)
  $< $M as ex:
   print('Error: '+$u(ex))
  $< $B:
   print('Error: Division by zero')
  $< MemoryError:
   try:
    import gc
    gc.collect()
   $< ImportError:
    pass
   print('Error: Out of memory')
  $< KeyboardInterrupt:
   print('Break')
  $< RuntimeError as ex:
   print('Error: Too $0 ('+$u(ex)+')')
  $< $= as ex:
   print('Error: '+$u(ex))
''')
_L['cashelp']=(r'''CATS=(
 ('alg','Algebra','solve csolve zeros czeros nsolve linsolve factor cfactor $; comdenom propfrac getnum getdenom completesquare polycoeffs polydegree polyquotient polyremainder polygcd polyroots cpolyroots polyeval tExpand tCollect simplify exact approx domain'),
 ('calc','Calculus','d $l limit sumseq prodseq taylor series dominantTerm deSolve impDif arcLen tangentLine normalLine fMin fMax nfMin nfMax nInt nDerivative avgRC centralDiff'),
 ('mat','Matrix/vector','det identity transpose rref ref inverse eigVl eigVc charPoly LU QR trace norm rowNorm colNorm diag augment colAugment subMat rowSwap rowAdd mRow mRowAdd crossP dotP unitV simult constructMat newMat randMat dim rowDim colDim mat>$G $G>mat'),
 ('num','Numbers','gcd lcm mod remain intDiv isPrime nCr nPr ! floor ceiling round iPart fPart sign $I $Q imag conj $p'),
 ('$G','Lists/stats','seq sum product mean median stdDev stdDevPop variance varPop max min sortA sortD cumulativeSum deltaList augment left right mid count normPdf normCdf invNorm binomPdf binomCdf poissPdf poissCdf geomPdf geomCdf'),
 ('conv','Conversions ($~>>$D)','>>Decimal >>approxFraction() >>DMS >>DD >>Rad >>Grad >>Polar >>Rect >>Cylind >>Sphere >>exp >>ln >>logbase() >>sin >>cos >>Base2 >>Base10 >>Base16 exp>$G()'),
 ('cmd','Commands',':deg :rad :grad :auto :exact :approx :$Q :$0 :digits n :ascii :unicode :vars :clear :mode :mem  delvar a  q=quit'),
 )
SYN={
 'solve':'solve(eqn,var) solve(eqn,var=guess)\nsolve(ineq,var) solve(eq1 $+ eq2,{x,y})\nsolve(...)|x>0  (n1,n2..=any integer)',
 'csolve':'cSolve(eqn,var) $0 solutions',
 'zeros':'zeros($~,var) -> $G of roots\nzeros({e1,e2},{x,y}) -> matrix',
 'czeros':'cZeros($~,var) $0 roots',
 'nsolve':'nSolve(eqn,var[=guess][,lo,hi])',
 'linsolve':'linSolve({eq1,eq2},{x,y})',
 'factor':'factor($~[,var]) factor(integer)\nwith var: irrational factors',
 'cfactor':'cFactor($~[,var]) $0 factors',
 '$;':'$;($~[,var]) incl. partial fractions',
 'comdenom':'comDenom($~) common denominator',
 'propfrac':'propFrac($~[,var]) proper fraction',
 'getnum':'getNum($~) numerator',
 'getdenom':'getDenom($~) denominator',
 'completesquare':'completeSquare(expr_or_eqn,var)',
 'polycoeffs':'polyCoeffs(poly[,var]) -> {an..a0}',
 'polydegree':'polyDegree(poly[,var])',
 'polyquotient':'polyQuotient(p1,p2[,var])',
 'polyremainder':'polyRemainder(p1,p2[,var])',
 'polygcd':'polyGcd(p1,p2)',
 'polyroots':'polyRoots(poly,var) polyRoots({$^})',
 'cpolyroots':'cPolyRoots(poly,var)',
 'polyeval':'polyEval({$^},x)',
 'texpand':'tExpand($~) $; trig of sums/multiples',
 'tcollect':'tCollect($~) products -> multiple angles',
 'simplify':'simplify($~) extra simplification',
 'exact':'exact($~[,tol]) floats -> fractions',
 'approx':'approx($~) decimal value',
 'domain':'domain($~,var)',
 'd':'d($~,var[,order])  d($~,var)|var=val\nderivative(...) same',
 '$l':'$l($~,var) antiderivative\nintegral($~,var,a,b) definite\n(\u222b also accepted)',
 'limit':'limit($~,var,point[,dir]) dir:-1 left,1 right\npoint may be $] or -$]',
 'sumseq':'sumSeq($~,var,lo,hi)  (\u03a3) hi may be $]',
 'prodseq':'prodSeq($~,var,lo,hi)  (\u03a0)',
 'taylor':'taylor($~,var,order[,point])',
 'series':'series($~,var,order[,point])',
 'dominantterm':'dominantTerm($~,var[,point])',
 'desolve':"deSolve(ode,x,y) use y' $+ y''\ndeSolve(y''+y=0 $+ y(0)=0 $+ y'(0)=1,x,y)",
 'impdif':'impDif(eqn,x,y[,order]) dy/dx',
 'arclen':'arcLen($~,var,a,b)',
 'tangentline':'tangentLine($~,var,point)',
 'normalline':'normalLine($~,var,point)',
 'fmin':'fMin($~,var[,lo,hi]) -> var=value',
 'fmax':'fMax($~,var[,lo,hi])',
 'nfmin':'nfMin($~,var[,lo,hi]) numeric',
 'nfmax':'nfMax($~,var[,lo,hi]) numeric',
 'nint':'nInt($~,var,a,b) numeric $l',
 'nderivative':'nDerivative($~,var=val[,order])',
 'avgrc':'avgRC($~,var[=val][,h])',
 'centraldiff':'centralDiff($~,var[=val][,h])',
 'det':'det(M)','inverse':'M^-1 or inverse(M)','rref':'rref(M)','ref':'ref(M)',
 'eigvl':'eigVl(M) eigenvalues','eigvc':'eigVc(M) unit eigenvectors (columns)',
 'charpoly':'charPoly(M,var)','lu':'LU(M) -> {L,U,P} with P*M=L*U','qr':'QR(M) -> {Q,R}',
 'simult':'simult(A,b) solves A*x=b','constructmat':'constructMat($~,i,j,$j,cols)',
 'crossp':'crossP(u,v)','dotp':'dotP(u,v)','unitv':'unitV(v)','norm':'norm(M)',
 'seq':'seq($~,var,lo,hi[,step])',
 'ncr':'nCr(n,k)','npr':'nPr(n,k)','gcd':'gcd(a,b)','lcm':'lcm(a,b)',
 'mod':'mod(a,b)','isprime':'isPrime(n)',
 'define':'Define f(x)=$~   or   f(x):=$~\nexpr->a  or  a:=$~   delvar a',
 'with':'$~|x=3   $~|x>0   solve(...)|0<=x<=2pi',
 'menu':'m or menu: numbered menus build the\ncommand $) you; 0 back, q quit.\nMatrices may be typed 1,2;3,4',
 'syntax':'implicit mult: 2x  3(x+1)  x(x+1)\n^ or ** power, $T( or \u221a, pi, e, i, $]\n<= >= /= $+ or $., ans = last result\nlog(x)=ln(x) ([ln] key); log10(x), log(x,b)',
 'log':'log(x) natural log (= ln, the [ln] key)\nlog10(x) base 10, log(x,b) base b',
 }
$, help($D=$#):
 if $D is $#:
  $?=['nCAS help: ?topic or ?command']
  $) k,t,items in CATS:
   $?.$%('?'+k+'  '+t)
  $?.$%('?define ?with ?syntax ?menu')
  $?.$%('m = menus (no typing of names)')
  $! '\n'.join($?)
 $D=$D.lower().replace('(','').strip()
 $) k,t,items in CATS:
  if $D==k:
   $! t+':\n'+items
 if $D in SYN:
  $! SYN[$D]
 $) k in SYN:
  if k.$r($D):
   $! SYN[k]
 $! 'No help $) '+$D
''',
r'''SELFTEST=(
 ('factor(x^2-5x+6)','(x-2)*(x-3)'),
 ('$;((x+1)^3)','x^3+3*x^2+3*x+1'),
 ('solve(x^2-5x+6=0,x)','x=2 or x=3'),
 ('solve(x^2=2,x)','x=-\u221a2 or x=\u221a2'),
 ('d(x^3*sin(x),x)','x^3*cos(x)+3*x^2*sin(x)'),
 ('$l(x*e^x,x)','x*e^x-e^x'),
 ('$l(1/(1+x^2),x,0,1)','\u03c0/4'),
 ('limit(sin(x)/x,x,0)','1'),
 ('taylor(e^x,x,3)','x^3/6+x^2/2+x+1'),
 ('sumSeq(k,k,1,n)','n*(n+1)/2'),
 ("deSolve(y'=y,x,y)",'y=c1*e^x'),
 ('det([[1,2][3,4]])','-2'),
 ('[[1,2][3,4]]^-1','[[-2,1][3/2,-1/2]]'),
 ('$T(12)','2*\u221a3'),
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
  $< $= as ex:
   r='ERR '+$u(ex)
  if r==a:
   ok+=1
  $(:
   $?.$%('FAIL '+q+' -> '+r)
 $?.$%('%d/%d tests passed'%(ok,$3(SELFTEST)))
 $! '\n'.join($?)
''',)
_L['casmenu']=(r'''ALG=(
 ('Expand','$;(@1`,@2`)',(('$Z',$#),('Var (blank=all)',''))),
 ('Factor','factor(@1`,@2`)',(('$Z',$#),('Var (blank=Q)',''))),
 ('cFactor','cFactor(@1`,@2`)',(('$Z',$#),('Var (blank=all)',''))),
 ('Simplify','simplify(@1)',(('$Z',$#),)),
 ('comDenom','comDenom(@1)',(('$Z',$#),)),
 ('propFrac','propFrac(@1`,@2`)',(('$Z',$#),('Var',''))),
 ('Partial frac','$;(@1,@2)',(('Rational $~',$#),('Var','x'))),
 ('Complete sq','completeSquare(@1,@2)',(('Quadratic/eqn',$#),('Var','x'))),
 ('Poly divide','polyQuotient(@1,@2,@3)',(('Dividend',$#),('Divisor',$#),('Var','x'))),
 ('Poly remain','polyRemainder(@1,@2,@3)',(('Dividend',$#),('Divisor',$#),('Var','x'))),
 ('Poly gcd','polyGcd(@1,@2)',(('Poly 1',$#),('Poly 2',$#))),
 ('Substitute','(@1)|@2=@3',(('$Z',$#),('Var','x'),('Value',$#))),
 ('tExpand','tExpand(@1)',(('$Z',$#),)),
 ('tCollect','tCollect(@1)',(('$Z',$#),)),
 ('Decimal','approx(@1)',(('$Z',$#),)),
 ('Exact','exact(@1)',(('$Z',$#),)),
 )
CALC=(
 ('Derivative','d(@1,@2`,@3`)',(('f',$#),('Var','x'),('Order',''))),
 ('Deriv at pt','d(@1,@2)|@2=@3',(('f',$#),('Var','x'),('At',$#))),
 ('Integral','$l(@1,@2)',(('f',$#),('Var','x'))),
 ('Def $l','$l(@1,@2,@3,@4)',(('f',$#),('Var','x'),('Lower ($] ok)',$#),('Upper',$#))),
 ('Limit','limit(@1,@2,@3`,@4`)',(('f',$#),('Var','x'),('Point ($] ok)','0'),('Side 1/-1',''))),
 ('Taylor','taylor(@1,@2,@3`,@4`)',(('f',$#),('Var','x'),('Order','5'),('Point',''))),
 ('Series','series(@1,@2,@3`,@4`)',(('f',$#),('Var','x'),('Order','5'),('Point',''))),
 ('Sum (sigma)','sumSeq(@1,@2,@3,@4)',(('Term',$#),('Index','k'),('From','1'),('To ($] ok)','n'))),
 ('Product','prodSeq(@1,@2,@3,@4)',(('Term',$#),('Index','k'),('From','1'),('To','n'))),
 ('deSolve',"deSolve(@1` $+ @2`` $+ @3`,@4,@5)",
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
 ('Zeros','zeros(@1,@2)',(('$Z',$#),('Var','x'))),
 ('cZeros','cZeros(@1,@2)',(('$Z',$#),('Var','x'))),
 ('nSolve','nSolve(@1,@2`,@3,@4`)',(('Equation',$#),('Var or x=guess','x'),('Lower',''),('Upper',''))),
 ('System 2 eqs','solve(@1 $+ @2,{@3})',(('Eq 1',$#),('Eq 2',$#),('Vars','x,y'))),
 ('System 3 eqs','solve(@1 $+ @2 $+ @3,{@4})',(('Eq 1',$#),('Eq 2',$#),('Eq 3',$#),('Vars','x,y,z'))),
 ('Poly roots','polyRoots(@1,@2)',(('Polynomial',$#),('Var','x'))),
 ('Domain','domain(@1,@2)',(('$Z',$#),('Var','x'))),
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
 ('Real part','$Q(@1)',(('Complex z',$#),)),
 ('Imag part','imag(@1)',(('Complex z',$#),)),
 ('Conjugate','conj(@1)',(('Complex z',$#),)),
 ('|z|','$I(@1)',(('Complex z',$#),)),
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
 ('normCdf','normCdf(@1,@2`,@3,@4`)',(('Lower (-$] ok)',$#),('Upper',$#),('mu',''),('sigma',''))),
 ('invNorm','invNorm(@1`,@2,@3`)',(('Area',$#),('mu',''),('sigma',''))),
 ('binomPdf','binomPdf(@1,@2,@3)',(('n',$#),('p',$#),('x',$#))),
 ('binomCdf','binomCdf(@1,@2,@3,@4)',(('n',$#),('p',$#),('Lower','0'),('Upper',$#))),
 )
''',
r'''CONV=(
 ('>Decimal','(@1)>>Decimal',(('$Z',$#),)),
 ('>Fraction','(@1)>>approxFraction()',(('Decimal',$#),)),
 ('>DMS','(@1)>>DMS',(('Angle',$#),)),
 ('>Polar','(@1)>>Polar',(('Complex/vector',$#),)),
 ('>Rect','(@1)>>Rect',(('Complex',$#),)),
 ('>exp form','(@1)>>exp',(('$Z',$#),)),
 ('>ln form','(@1)>>ln',(('$Z',$#),)),
 ('>sin form','(@1)>>sin',(('$Z',$#),)),
 ('>cos form','(@1)>>cos',(('$Z',$#),)),
 ('>Binary','(@1)>>Base2',(('Integer',$#),)),
 ('>Hex','(@1)>>Base16',(('Integer',$#),)),
 )
SETS=(
 ('Degree',':deg',()),
 ('Radian',':rad',()),
 ('Auto mode',':auto',()),
 ('Exact mode',':exact',()),
 ('Approx mode',':approx',()),
 ('Real res',':$Q',()),
 ('Complex res',':$0',()),
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
 ('Number/$A',NUMB),('Lists/stats',LIST),('Convert',CONV),
 ('Settings',SETS),
 )
KEYS='123456789abcdefghijklmnop'
class Quit($=):
 pass
$, ask(q):
 try:
  s=input(q)
 $< EOFError:
  $n Quit()
 s=s.strip()
 if s.lower()in('q','quit'):
  $n Quit()
 $! s
$, show(title,labels):
 print('-- '+title+' --')
 line=''
 $) i in $*($3(labels)):
  cell=KEYS[i]+' '+labels[i]
  if line:
   print(line+' '*max(1,16-$3(line))+cell)
   line=''
  $(:
   line=cell
 if line:
  print(line)
 print('0 back  q quit')
$, pick(title,labels):
 show(title,labels)
 $H $F:
  s=ask('#: ').lower()
  if s in('','0'):
   $! $#
  i=KEYS.find(s)
  if $3(s)==1 $+ 0<=i<$3(labels):
   $! i
  print('Choose '+KEYS[0]+'-'+KEYS[$3(labels)-1]+', 0 or q')
$, matrix_text(s):
 s=s.strip()
 if s $+ s[0]$. in '[(' $+(';' in s or ',' in s):
  $! '['+s+']'
 $! s
$, build(item):
 label,tpl,prompts=item
 $g=[]
 $) p in prompts:
  q=p[0]
  d=p[1]
  hint='' if $. d $( ' ['+d+']'
  s=ask(q+hint+': ')
  if $. s:
   if d is $#:
    print('(cancelled)')
    $! $#
   s=d
  if $3(p)>2 $+ p[2]=='m' $+ s:
   s=matrix_text(s)
  $g.$%(s)
 $! fill(tpl,$g)
$, fill(tpl,$g):
 $?=''
 parts=tpl.split('`')
 $) k in $*($3(parts)):
  seg=parts[k]
  if k%2==1:
   blank=$2
   $) i in $*($3($g)):
    if('@'+$u(i+1))in seg $+ $. $g[i]:
     blank=$F
   if blank:
    $7
  $?+=seg
 res=''
 i=0
 $H i<$3($?):
  c=$?[i]
  if c=='@' $+ i+1<$3($?)$+ '1'<=$?[i+1]<='9':
   res+=$g[$q($?[i+1])-1]
   i+=2
  $(:
   res+=c
   i+=1
 $! res
$, menu(run):
 print('Menus: pick a number or letter.')
 print("Type ans $) the last result.")
 try:
  $H $F:
   k=pick('nCAS menu',[m[0]$) m in MAIN])
   if k is $#:
    $!
   title,items=MAIN[k]
   $H $F:
    j=pick(title,[it[0]$) it in items])
    if j is $#:
     $X
    cmd=build(items[j])
    if cmd is $#:
     $7
    print('> '+cmd)
    try:
     $?=run(cmd)
    $< $M as ex:
     $?='Error: '+$u(ex)
    $< $B:
     $?='Error: Division by zero'
    $< MemoryError:
     $?='Error: Out of memory'
    $< RuntimeError as ex:
     $?='Error: Too $0'
    $< Quit:
     $n
    $< $= as ex:
     $?='Error: '+$u(ex)
    if $?:
     print($?)
    ask('(enter) ')
 $< Quit:
  $!
 $< KeyboardInterrupt:
  $!
''',)
_x('GUI=False')
del _x
cas()
