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
_W={'!': 'return', '#': 'None', '%': 'append', '&': 'else', '(': 'isnode', ')': 'for', '*': 'range', '+': 'and', ',': 'def', '-': 'not', '.': 'autocancel', '/': 'type', '0': 'len', '1': 'complex', '2': 'False', '3': 'tuple', '4': 'continue', '5': 'lambda', '6': 'except', '7': 'isconst', '8': 'add_list', '9': 'freeof', ':': 'mul', ';': 'self', '<': 'out', '=': 'expand', '>': 'Exception', '?': 'elif', '@': 'depth', 'A': 'True', 'B': 'name', 'C': 'ZeroDivisionError', 'D': 'isnum', 'E': 'cplx', 'F': 'float', 'G': 'while', 'H': 'mul_list', 'I': 'list', 'J': 'abs', 'K': 'p_divexact', 'L': 'sqrt', 'M': 'undef', 'N': 'args', 'O': 'CASError', 'P': 'ValueError', 'Q': 'terms', 'R': 'break', 'S': 'real', 'T': 'rows', 'U': 'math', 'V': 'nval', 'W': 'OverflowError', 'X': 'coef_rest', 'Y': 'subs', 'Z': 'div', '[': 'inf', ']': 'Expression', '^': 'islist', '_': 'coeffs', '`': 'rest', 'a': 'hasfloat', 'b': 'nsign', 'c': 'sub', 'd': 'add', 'e': 'onevar_expr', 'f': 'sols', 'g': 'vals', 'h': 'linear', 'i': 'NoSeries', 'j': 'integral', 'k': 'isint', 'l': 'symbols', 'm': 'FSIMP', 'n': 'raise', 'o': 'KeyboardInterrupt', 'p': 'str', 'q': 'israt', 'r': 'neg', 's': 'angle', 't': 'int', 'u': 'arctan', 'v': 'print', 'w': 'arcsin', 'x': 'startswith', 'y': 'nargs', 'z': 'factor_expr', '{': 'extend', '|': 'solve_eq', '}': 'isrealc', '~': 'p_const'}
_x(r'''import $U
class $O($>):
 pass
$, err(msg):
 $n $O(msg)
CONSTS=('pi','e','i')
SPECIAL=('pi','e','i','$[','$M','true','false')
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
HALF=('Q',1,2)
$, isq(x):
 $! $/(x)is $3 $+ x[0]=='Q'
$, $k(x):
 $! $/(x)is $t
$, isfl(x):
 $! $/(x)is $F
$, $q(x):
 t=$/(x)
 $! t is $t or(t is $3 $+ x[0]=='Q')
$, $D(x):
 t=$/(x)
 $! t is $t or t is $F or(t is $3 $+ x[0]=='Q')
$, nd(x):
 if $/(x)is $t:
  $! x,1
 $! x[1],x[2]
$, tofl(x):
 t=$/(x)
 if t is $F:
  $! x
 if t is $t:
  $! $F(x)
 $! x[1]/x[2]
$, nadd(a,b):
 ta=$/(a)
 tb=$/(b)
 if ta is $t $+ tb is $t:
  $! a+b
 if ta is $F or tb is $F:
  $! tofl(a)+tofl(b)
 an,ad=nd(a)
 bn,bd=nd(b)
 $! Q(an*bd+bn*ad,ad*bd)
$, nmul(a,b):
 ta=$/(a)
 tb=$/(b)
 if ta is $t $+ tb is $t:
  $! a*b
 if ta is $F or tb is $F:
  $! tofl(a)*tofl(b)
 an,ad=nd(a)
 bn,bd=nd(b)
 $! Q(an*bn,ad*bd)
$, nneg(a):
 if $/(a)is $3:
  $!('Q',-a[1],a[2])
 $!-a
$, nsub(a,b):
 $! nadd(a,nneg(b))
$, ninv(a):
 t=$/(a)
 if t is $F:
  if a==0.0:
   err("Division by zero")
  $! 1.0/a
 n,d=nd(a)
 $! Q(d,n)
$, ndiv(a,b):
 $! nmul(a,ninv(b))
$, $b(a):
 if $/(a)is $3:
  a=a[1]
 if a>0:
  $! 1
 if a<0:
  $!-1
 $! 0
$, ncmp(a,b):
 $! $b(nsub(a,b))
$, nfloor(a):
 t=$/(a)
 if t is $t:
  $! a
 if t is $F:
  if a!=a or a in($F('$['),$F('-$[')):
   err("Domain error")
  $! $t($U.floor(a))
 $! a[1]//a[2]
$, nabs(a):
 if $b(a)<0:
  $! nneg(a)
 $! a
$, nipow(a,k):
 if k<0:
  $! nipow(ninv(a),-k)
 if $/(a)is $F:
  $! a**k
 n,d=nd(a)
 $! Q(n**k,d**k)
$, iroot(n,k):
 if n<2:
  $! n
 x=$t($U.pow(n,1.0/k))if n<10**300 $& 1<<(($0(bin(n))-2)//k+1)
 if x<1:
  x=1
 $G $A:
  y=((k-1)*x+n//(x**(k-1)))//k
  if y>=x:
   $R
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
  $) i in $*(2,N):
   if $- s[i]:
    ps.$%(i)
    $) j in $*(i*i,N,i):
     s[j]=1
  SMALLP=ps
 $! SMALLP
$, $((e,h):
 $! $/(e)is $3 $+ e[0]==h
$, head(e):
 if $/(e)is $3:
  $! e[0]
 $! $#
$, okey(e):
 $! repr(e)
$, has(e,x):
 if e==x:
  $! $A
 if $/(e)is $3 $+ e[0]!='Q':
  $) a in e[1:]:
   if has(a,x):
    $! $A
 $! $2
$, $9(e,x):
 $! $- has(e,x)
$, freeofall(e,xs):
 $) x in xs:
  if has(e,x):
   $! $2
 $! $A
$, $l(e,$<=$#):
 if $< is $#:
  $<=[]
 t=$/(e)
 if t is $p:
  if e $- in SPECIAL $+ e $- in $<:
   $<.$%(e)
 $? t is $3 $+ e[0]!='Q' $+ e[0]!='$p':
  $) a in e[1:]:
   $l(a,$<)
 $! $<
$, $7(e):
 t=$/(e)
 if t is $p:
  $! e in SPECIAL
 if t is $3 $+ e[0]!='Q':
  if e[0]=='$p':
   $! $2
  $) a in e[1:]:
   if $- $7(a):
    $! $2
 $! $A
$, $a(e):
 t=$/(e)
 if t is $F:
  $! $A
 if t is $3 $+ e[0]!='Q':
  $) a in e[1:]:
   if $a(a):
    $! $A
 $! $2
$, $X(a):
 if $/(a)is $3 $+ a[0]=='*' $+ $D(a[1]):
  if $0(a)==3:
   $! a[1],a[2]
  $! a[1],('*',)+a[2:]
 $! 1,a
$, cmul(c,r):
 if $/(c)is $t $+ c==1:
  $! r
 if $/(r)is $3 $+ r[0]=='*':
  if $D(r[1]):
   c=nmul(c,r[1])
   if $/(c)is $t $+ c==1:
    $!('*',)+r[2:]if $0(r)>3 $& r[2]
   $!('*',c)+r[2:]
  $!('*',c)+r[1:]
 $!('*',c,r)
$, $d(*$N):
 $! $8($N)
$, $8($N):
 num=0
 $Q={}
 order=[]
 st=$I($N)
 infs=0
 $G st:
  a=st.pop()
  t=$/(a)
  if t is $t or t is $F:
   num=nadd(num,a)
   $4
  if t is $3:
   h=a[0]
   if h=='Q':
    num=nadd(num,a)
    $4
   if h=='+':
    st.${(a[1:])
    $4
   if h=='*' $+ $D(a[1]):
    c=a[1]
    r=a[2]if $0(a)==3 $&('*',)+a[2:]
   $&:
    c=1
    r=a
  $&:
   if a=='$M':
    $! '$M'
   c=1
   r=a
  if r=='$[':
   s=$b(c)
   if s==0:
    $4
   if infs $+ infs!=s:
    $! '$M'
   infs=s
   $4
  if r in $Q:
   $Q[r]=nadd($Q[r],c)
  $&:
   $Q[r]=c
   order.$%(r)
 if infs:
  $! '$[' if infs>0 $&('*',-1,'$[')
 $<=[]
 $) r in order:
  c=$Q[r]
  if c==0:
   $4
  $<.$%(cmul(c,r))
 if num!=0 or $- $<:
  if $< $+ num==0:
   pass
  $&:
   $<.$%(num)
 if $0($<)==1:
  $! $<[0]
 $<.sort(key=okey)
 $!('+',)+$3($<)
$, isrrad(e):
 $! $/(e)is $3 $+ e[0]=='^' $+ $/(e[1])is $t $+ isq(e[2])
$, $:(*$N):
 $! $H($N)
''')
_x(r'''$, $H($N):
 coef=1
 bases={}
 order=[]
 st=$I($N)
 $G st:
  a=st.pop()
  t=$/(a)
  if t is $t or t is $F:
   coef=nmul(coef,a)
   $4
  if t is $3:
   h=a[0]
   if h=='Q':
    coef=nmul(coef,a)
    $4
   if h=='*':
    st.${(a[1:])
    $4
   if h=='^':
    b=a[1]
    x=a[2]
   $&:
    b=a
    x=1
  $&:
   if a=='$M':
    $! '$M'
   b=a
   x=1
  if b in bases:
   bases[b]=$d(bases[b],x)
  $&:
   bases[b]=x
   order.$%(b)
 if coef==0:
  if '$[' in bases:
   $! '$M'
  $) b in order:
   if b=='$M' or has(b,'$M'):
    $! '$M'
  $! coef
 facs=[]
 rad={}
 radorder=[]
 $, collect(p):
  c=1
  t=$/(p)
  if t is $t or t is $F or(t is $3 $+ p[0]=='Q'):
   $! p
  if t is $3 $+ p[0]=='*':
   items=p[1:]
  $&:
   items=(p,)
  $) f in items:
   if $D(f):
    c=nmul(c,f)
   $? isrrad(f):
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
  if p=='$M':
   $! '$M'
  coef=nmul(coef,collect(p))
 if rad:
  multi=$0(radorder)!=$0(rad)
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
 if '$[' in facs:
  if $0(facs)==1 or $A:
   coef=$b(coef)if $/(coef)is $- $F $&(1.0 if coef>0 $&-1.0)
   if $/(coef)is $F:
    coef=$t(coef)
 if $- facs:
  $! coef
 if $0(facs)>1:
  algs=[f $) f in facs if $((f,'+')$+ isalg(f)]
  if algs $+ all([isalg(f)$) f in facs]):
   r=coef
   $) f in facs:
    r=expand_mul(r,f)
   $! r
 if $0(facs)==1:
  f=facs[0]
  if $/(coef)is $t $+ coef==1:
   $! f
  if $/(f)is $3 $+ f[0]=='+':
   $! $8([$:(coef,t)$) t in f[1:]])
  $!('*',coef,f)
 facs.sort(key=okey)
 if $/(coef)is $t $+ coef==1:
  $!('*',)+$3(facs)
 $!('*',coef)+$3(facs)
$, $r(a):
 $! $:(-1,a)
$, $c(a,b):
 $! $d(a,$:(-1,b))
$, $Z(a,b):
 $! $:(a,pw(b,-1))
$, inv(a):
 $! pw(a,-1)
$, $L(a):
 $! pw(a,HALF)
$, factor_int_small(n):
 fs=[]
 $) p in smallprimes():
  if p*p>n:
   $R
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
 fs,$`=factor_int_small(n)
 $) p,k in fs:
  a*=p**(k//q)
  m*=p**(k%q)
 if $`>1:
  r=iroot($`,q)
  if r**q==$`:
   a*=r
  $&:
   m*=$`
 $! a,m
$, ipow_root(n,p,q):
 a,m=radical(n**p,q)if p>1 $& radical(n,q)
 if m==1:
  $! a
 ex=Q(1,q)
 k=2
 best=$#
 $G(1<<k)<=m:
  r=iroot(m,k)
  if r**k==m:
   best=(r,k)
  k+=1
 if best is $- $#:
  m=best[0]
  ex=Q(best[1],q)
 if ex==1:
  $! a*m
 if $k(ex):
  $! a*m**ex
 if a==1:
  $!('^',m,ex)
 $!('*',a,('^',m,ex))
MAXBITS=12000
$, ibits(n):
 if n==0:
  $! 0
 h='%x'%$J(n)
 v=$t(h[0],16)
 $! 4*$0(h)-(3 if v<2 $& 2 if v<4 $& 1 if v<8 $& 0)
$, bigpow(b,x):
 n,d=nd(b)
 if d==1 $+ $J(n)<=1:
  $! $2
 $! $J(x)*(ibits(n)+(ibits(d)if d>1 $& 0))>MAXBITS
$, pw_num(b,x):
 if $/(b)is $F or $/(x)is $F:
  bf=tofl(b)
  xf=tofl(x)
  if bf==0.0:
   if xf>0:
    $! 0.0
   if xf==0:
    $! 1.0
   $! '$M'
  if bf!=bf or xf!=xf:
   $! '$M'
  if bf<0 $+(xf in($F('$['),$F('-$['))or xf!=$U.floor(xf)):
   if $q(x)$+ nd(x)[1]%2==1:
    r=(-bf)**xf
    $!-r if nd(x)[0]%2 $& r
   z=$1(bf)**xf
   $! fromcomplex(z)
  try:
   $! bf**xf
  $6 $W:
   $! '$['
 if $/(x)is $t:
  if b==0:
   if x<0:
    $! '$M'
   $! 0
  if bigpow(b,x):
   $!('^',b,x)
  $! nipow(b,x)
 p,q=nd(x)
 if b==0:
  $! 0 if p>0 $& '$M'
 if $b(b)<0:
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
 parts=[]
 if n>1:
  parts.$%(ipow_root(n,fp,fq))
 if d>1:
  parts.$%(Q(1,d))
  parts.$%(ipow_root(d,fq-fp,fq))
 c=res
 facs=[]
 $) pt in parts:
  if $D(pt):
   c=nmul(c,pt)
  $? pt[0]=='*':
   c=nmul(c,pt[1])
   facs.$%(pt[2])
  $&:
   facs.$%(pt)
 if $0(facs)==2:
  if facs[0][2]==facs[1][2]:
   $! $:(c,pw_num(facs[0][1]*facs[1][1],facs[0][2]))
  facs.sort(key=okey)
 if $- facs:
  $! c
 if c==1:
  if $0(facs)==1:
   $! facs[0]
  $!('*',)+$3(facs)
 $!('*',c)+$3(facs)
$, isposconst(e):
 if $D(e):
  $! $b(e)>0
 if e=='pi' or e=='e':
  $! $A
 if isrrad(e):
  $! e[1]>0
 if $((e,'^')$+(e[1]=='e' or e[1]=='pi')$+ isreal_expr(e[2]):
  $! $A
 $! $2
$, isalg(e):
 t=$/(e)
 if t is $t or t is $F:
  $! $A
 if t is $p:
  $! e=='i'
 h=e[0]
 if h=='Q':
  $! $A
 if h=='^':
  $! $D(e[1])$+ $D(e[2])
 if h=='+' or h=='*':
  $) a in e[1:]:
   if $- isalg(a):
    $! $2
  $! $A
 $! $2
''')
_x(r'''$, pw(b,x):
 if x==0:
  if b=='$M' or b=='$[':
   $! '$M'
  $! 1
 if $/(x)is $t $+ x==1:
  $! b
 if b=='$M' or x=='$M':
  $! '$M'
 bn=$D(b)
 xn=$D(x)
 if bn $+ xn:
  $! pw_num(b,x)
 if b==1 $+ $/(b)is $t:
  $! 1
 if b=='$[':
  if xn:
   $! '$[' if $b(x)>0 $& 0
  if x=='$[':
   $! '$['
 if xn $+ b==0:
  $! 0 if $b(x)>0 $& '$M'
 if b=='i' $+ $/(x)is $t:
  r=x%4
  $!(1,'i',-1,('*',-1,'i'))[r]
 if x=='$[' $+ bn:
  if nabs(b)==1:
   $! '$M' if b==1 $& '$M'
  if ncmp(nabs(b),1)>0:
   $! '$[' if $b(b)>0 $& '$M'
  $! 0
 if b=='e':
  if x=='$[':
   $! '$['
  if $((x,'*')$+ $0(x)==3 $+ x[1]==-1 $+ x[2]=='$[':
   $! 0
  if $/(x)is $F:
   $! $U.exp(x)
  if $((x,'ln'):
   $! x[1]
  if $((x,'*'):
   c,r=$X(x)
   if $((r,'ln')$+ $q(c):
    $! pw(r[1],c)
  if $((x,'+'):
   outs=[]
   $`=[]
   $) t in x[1:]:
    c,r=$X(t)
    if $((r,'ln')$+ $q(c):
     outs.$%(pw(r[1],c))
    $&:
     $`.$%(t)
   if outs:
    $! $H(outs+[pw('e',$8($`))])
  if $((x,'*')$+ 'i' in x $+ 'pi' in x:
   c,r=$X(x)
   if r==('*','i','pi')$+ $q(c):
    $! $d(cos_($:(c,'pi')),$:('i',sin_($:(c,'pi'))))
 if b!='e' $+ $7(b)$+ $7(x)$+ $- $q(x)$+(has(b,'i')or has(x,'i'))$+ $- $a(x):
  L=fn('ln',b)
  if $- $((L,'ln')$+ $-($((L,'+')$+ any([$((t,'ln')$) t in L[1:]])):
   $! pw('e',$=($:(x,L)))
 if $/(b)is $3:
  h=b[0]
  if h=='^':
   bb=b[1]
   ee=b[2]
   if $/(x)is $t:
    $! pw(bb,$:(ee,x))
   if isposconst(bb):
    $! pw(bb,$:(ee,x))
   if $q(ee)$+ $q(x):
    r=nmul(ee,x)
    if $/(ee)is $t:
     if ee%2==0:
      if $/(r)is $t $+ r%2==0:
       $! pw(bb,r)
      $! pw(fn('$J',bb),r)
     $! pw(bb,r)
    if nd(ee)[0]%2==1 $+ nd(ee)[1]%2==1:
     $! pw(bb,r)
    if nd(ee)[0]%2==1:
     $! pw(bb,r)
  $? h=='*':
   if $/(x)is $t:
    $! $H([pw(f,x)$) f in b[1:]])
   outs=[]
   $`=[]
   $) f in b[1:]:
    if $D(f):
     if $b(f)>0:
      outs.$%(pw(f,x))
     $? f!=-1:
      outs.$%(pw(nneg(f),x))
      $`.$%(-1)
     $&:
      $`.$%(f)
    $? isposconst(f)or $((f,'$J'):
     outs.$%(pw(f,x))
    $&:
     $`.$%(f)
   if outs:
    $! $H(outs+[pw($H($`),x)])
  $? h=='$J':
   if $/(x)is $t $+ x%2==0:
    $! pw(b[1],x)
  $? h=='+':
   if x==HALF $+ isalg(b)$+ $- has(b,'i'):
    dn=denest(b)
    if dn is $- $#:
     $! dn
   if isq(x)$+ x[2]==2 $+ $b(x)<0 $+ isalg(b)$+ $- has(b,'i'):
    dn=denest(b)
    if dn is $- $#:
     $! pw(pw(dn,-1),-x[1])if x[1]!=-1 $& pw(dn,-1)
   if $/(x)is $t $+ x!=1 $+ $- isalg(b):
    c=sumcontent(b)
    if c!=1:
     $! $:(pw(c,x),pw($:(ninv(c),b),x))
    if leadneg(b):
     nb=$:(-1,b)
     if x%2==0:
      $! pw(nb,x)
     $! $:(-1,pw(nb,x))
   if $/(x)is $t $+ isalg(b):
    if x>0 $+ x<=64:
     $! expand_pow(b,x)
    if x<0 $+ x>=-64:
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
  if $/(f)is $p $+ f $- in SPECIAL:
   d+=1
  $? $((f,'^')$+ $/(f[1])is $p $+ f[1]$- in SPECIAL $+ $D(f[2]):
   d+=tofl(f[2])
 $! d
$, leadneg(b):
 best=$#
 bk=$#
 $) t in b[1:]:
  if $D(t):
   $4
  c,r=$X(t)
  k=(-tdeg(r),okey(r))
  if bk is $# or k<bk:
   bk=k
   best=c
 if best is $#:
  $! $2
 $! $b(best)<0 if $D(best)$& $2
$, sumcontent(b):
 g=0
 L=1
 $) t in b[1:]:
  c,r=$X(t)
  if $- $q(c):
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
  if $q(t):
   a=nadd(a,t)
   $4
  cc,r=$X(t)
  if isrrad(r)$+ r[2]==HALF $+ $q(cc)$+(n is $# or n==r[1]):
   n=r[1]
   c=nadd(c,cc)
  $&:
   $! $#
 if n is $# or c==0:
  $! $#
 d2=nsub(nmul(a,a),nmul(nmul(c,c),n))
 if $b(d2)<0:
  $! $#
 dn,dd=nd(d2)
 rn=isqrt(dn)
 rd=isqrt(dd)
 if rn*rn!=dn or rd*rd!=dd:
  $! $#
 d=Q(rn,rd)
 p=ndiv(nadd(a,d),2)
 m=ndiv(nsub(a,d),2)
 if $b(p)<0 or $b(m)<0:
  $! $#
 r=$d(pw(p,HALF),$:($b(c),pw(m,HALF)))
 if $((r,'+')$+ $0(r)<=3:
  $! r
 $! $#
$, expand_mul(a,b):
 ta=a[1:]if $((a,'+')$&(a,)
 tb=b[1:]if $((b,'+')$&(b,)
 $<=[]
 $) u in ta:
  $) v in tb:
   $<.$%($:(u,v))
 $! $8($<)
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
  d=$d($:(re_,re_),$:(im_,im_))
  d=$=(d)
  if $((d,'+'):
   r2=rationalize_inv(d)
   if r2 is $#:
    $! $#
  $&:
   r2=pw(d,-1)
  $! expand_mul($c(re_,$:('i',im_)),r2)
 $Q=b[1:]if $((b,'+')$&(b,)
 kern=$#
 kerns=[]
 $) t in $Q:
  c,r=$X(t)
  if r!=1 $+ $- $D(r):
   if isrrad(r)$+ r[2]==HALF:
    if r $- in kerns:
     kerns.$%(r)
   $&:
    $! $#
 if $- kerns or $0(kerns)>3:
  $! $#
 kern=kerns[0]
 if $0(kerns)>1:
  A=$8([t $) t in $Q if $X(t)[1]!=kern])
  B=$8([$X(t)[0]$) t in $Q if $X(t)[1]==kern])
  den=$=($c($:(A,A),$:(B,B,kern[1])))
  if den==0:
   $! $#
  if $((den,'+'):
   r2=rationalize_inv(den)
   if r2 is $#:
    $! $#
  $&:
   r2=pw(den,-1)
  $! expand_mul($c(A,$:(B,kern)),r2)
 a0=0
 a1=0
 $) t in $Q:
  c,r=$X(t)
  if r==kern:
   a1=nadd(a1,c)
  $&:
   a0=$d(a0,t)
 den=$c($:(a0,a0),$:(nmul(a1,a1),kern[1]))
 if den==0:
  $! $#
 $! expand_mul($c(a0,$:(a1,kern)),pw(den,-1))
''')
_x(r'''$, reim(e):
 t=$/(e)
 if t is $t or t is $F:
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
  $! $8(rs),$8(ims)
 if h=='*':
  r=1
  i=0
  $) a in e[1:]:
   ar,ai=reim(a)
   if ai==0:
    r=$:(r,ar)
    i=$:(i,ar)
   $&:
    r,i=$c($:(r,ar),$:(i,ai)),$d($:(r,ai),$:(i,ar))
  $! r,i
 if h=='^':
  b=e[1]
  x=e[2]
  if $- has(b,'i')$+ $- has(x,'i'):
   if $D(x)$+ $- $q(x):
    $! e,0
   if $q(x)$+ nd(x)[1]%2==0:
    if $7(b):
     v=cv(b)
     if v is $- $# $+ $/(v)is $- $1 $+ v<0:
      $! reim_generic(e)
    $! e,0
   $! e,0
  if $/(x)is $t:
   br,bi=reim(b)
   if x>0:
    z=expand_pow($d(br,$:('i',bi)),x)
    if has(z,'i')$+ z!=e:
     $! reim(z)
   $? $7(b):
    r=rationalize_inv(b)
    if r is $- $#:
     $! reim(expand_pow(r,-x))if x!=-1 $& reim(r)
  $! reim_generic(e)
 if h in('$I','mat','$p'):
  $! e,0
 $) a in e[1:]:
  if has(a,'i'):
   $! reim_generic(e)
 $! e,0
$, cv(u):
 try:
  v=$V(u)
 $6($O,$P,$C,$W,TypeError):
  $! $#
 if v!=v:
  $! $#
 if $/(v)is $1:
  if v.$S!=v.$S or v.imag!=v.imag:
   $! $#
  if $J(v.$S)==$F('$[')or $J(v.imag)==$F('$['):
   $! $#
 $? $J(v)==$F('$['):
  $! $#
 $! v
$, reim_generic(e):
 if $7(e):
  v=cv(e)
  if v is $#:
   $!('$S',e),('imag',e)
  z=$1(v)
  $! z.$S,z.imag
 $!('$S',e),('imag',e)
$, conj(e):
 r,i=reim(e)
 $! $c(r,$:('i',i))
$, fromcomplex(z):
 if $/(z)is $- $1:
  $! z
 if z.imag==0:
  $! z.$S
 if z.$S==0:
  $! $:(z.imag,'i')
 $! $d(z.$S,$:(z.imag,'i'))
$m={}
$, fn($B,*$N):
 if $0($N)==1 $+ $/($N[0])is $I:
  $N=$3($N[0])
 $) a in $N:
  if a=='$M':
   $! '$M'
 f=$m.get($B)
 if f is $- $#:
  r=f(*$N)
  if r is $- $#:
   $! r
 $!($B,)+$3($N)
$, isneg(e):
 if $D(e):
  $! $b(e)<0
 if $((e,'*'):
  $! $D(e[1])$+ $b(e[1])<0
 if $((e,'+'):
  $! leadneg(e)
 $! $2
$, isreal_expr(e):
 if $D(e):
  $! $A
 if $/(e)is $p:
  $! e!='i' $+ e!='$M'
 $! $- has(e,'i')
$, fval($B,x):
 $! fromcomplex(NUMF[$B](x))
$, fvalc($B,u):
 try:
  v=NUMF[$B]($V(u))
 $6($O,$P,$C,$W,TypeError):
  $! $#
 if $/(v)is $1:
  if v.$S!=v.$S or v.imag!=v.imag:
   $! $#
 $? v!=v:
  $! $#
 $! fromcomplex(v)
$, pi_coef(u):
 if u=='pi':
  $! 1
 if u==0:
  $! 0
 if $((u,'*')$+ $0(u)==3 $+ u[2]=='pi' $+ $q(u[1]):
  $! u[1]
 $! $#
$, split_pi(u):
 if $((u,'+'):
  $) t in u[1:]:
   c=pi_coef(t)
   if c is $- $# $+ c!=0:
    $`=$8([s $) s in u[1:]if s is $- t])
    $! c,$`
 $! $#
TRIGT=$#
$, trig_table():
 global TRIGT
 if TRIGT is $#:
  s2=$L(2)
  s3=$L(3)
  s5=$L(5)
  s6=$L(6)
  q=Q
  T={}
  T[0]=0
  T[q(1,12)]=$:(q(1,4),$c(s6,s2))
  T[q(1,10)]=$:(q(1,4),$c(s5,1))
  T[q(1,8)]=$:(HALF,$L($c(2,s2)))
  T[q(1,6)]=HALF
  T[q(1,5)]=$:(q(1,4),$L($c(10,$:(2,s5))))
  T[q(1,4)]=$:(HALF,s2)
  T[q(3,10)]=$:(q(1,4),$d(s5,1))
  T[q(1,3)]=$:(HALF,s3)
  T[q(3,8)]=$:(HALF,$L($d(2,s2)))
  T[q(2,5)]=$:(q(1,4),$L($d(10,$:(2,s5))))
  T[q(5,12)]=$:(q(1,4),$d(s6,s2))
  T[HALF]=1
  TT={}
  TT[0]=0
  TT[q(1,12)]=$c(2,s3)
  TT[q(1,8)]=$c(s2,1)
  TT[q(1,6)]=$:(q(1,3),s3)
  TT[q(1,4)]=1
  TT[q(1,3)]=s3
  TT[q(3,8)]=$d(s2,1)
  TT[q(5,12)]=$d(2,s3)
  TT[q(1,5)]=$L($c(5,$:(2,s5)))
  TT[q(2,5)]=$L($d(5,$:(2,s5)))
  TT[q(1,10)]=$:(q(1,5),$L($c(25,$:(10,s5))))
  TT[q(3,10)]=$:(q(1,5),$L($d(25,$:(10,s5))))
  TRIGT=(T,TT)
 $! TRIGT
$, sin_pi(c):
 c=nsub(c,nmul(2,nfloor(nmul(c,HALF))))
 sg=1
 if ncmp(c,1)>=0:
  c=nsub(c,1)
  sg=-1
 if ncmp(c,HALF)>0:
  c=nsub(1,c)
 T=trig_table()[0]
 if c in T:
  $! $:(sg,T[c])
 if sg<0:
  $! $r(('sin',$:(c,'pi')))
 $!('sin',$:(c,'pi'))
$, tan_pi(c):
 c=nsub(c,nfloor(c))
 sg=1
 if ncmp(c,HALF)>0:
  c=nsub(1,c)
  sg=-1
 if c==HALF:
  $! '$M'
 TT=trig_table()[1]
 if c in TT:
  $! $:(sg,TT[c])
 $! $:(sg,('tan',$:(c,'pi')))
$, sin_(u):
 if $D(u):
  if u==0:
   $! 0
  if $/(u)is $F:
   $! $U.sin(u)
  $! $#
 if u=='$[' or u==('*',-1,'$['):
  $! '$M'
 c=pi_coef(u)
 if c is $- $#:
  $! sin_pi(c)
 if $a(u)$+ $7(u):
  $! fvalc('sin',u)
 if isneg(u):
  $! $r(fn('sin',$r(u)))
 sp=split_pi(u)
 if sp is $- $#:
  c,$`=sp
  c=nsub(c,nmul(2,nfloor(nmul(c,HALF))))
  if c==0:
   $! fn('sin',$`)
  if c==1:
   $! $r(fn('sin',$`))
  if c==HALF:
   $! fn('cos',$`)
  if c==Q(3,2):
   $! $r(fn('cos',$`))
  if ncmp(c,1)>0:
   $!('sin',$d($`,$:(nsub(c,2),'pi')))
  $!('sin',$d($`,$:(c,'pi')))
 if $((u,'$w'):
  $! u[1]
 if $((u,'arccos'):
  $! $L($c(1,pw(u[1],2)))
 if $((u,'$u'):
  $! $Z(u[1],$L($d(1,pw(u[1],2))))
 $! $#
''')
_x(r'''$, cos_(u):
 if $D(u):
  if u==0:
   $! 1
  if $/(u)is $F:
   $! $U.cos(u)
  $! $#
 if u=='$[' or u==('*',-1,'$['):
  $! '$M'
 c=pi_coef(u)
 if c is $- $#:
  $! sin_pi(nadd(c,HALF))
 if $a(u)$+ $7(u):
  $! fvalc('cos',u)
 if isneg(u):
  $! fn('cos',$r(u))
 sp=split_pi(u)
 if sp is $- $#:
  c,$`=sp
  c=nsub(c,nmul(2,nfloor(nmul(c,HALF))))
  if c==0:
   $! fn('cos',$`)
  if c==1:
   $! $r(fn('cos',$`))
  if c==HALF:
   $! $r(fn('sin',$`))
  if c==Q(3,2):
   $! fn('sin',$`)
  if ncmp(c,1)>0:
   $!('cos',$d($`,$:(nsub(c,2),'pi')))
  $!('cos',$d($`,$:(c,'pi')))
 if $((u,'arccos'):
  $! u[1]
 if $((u,'$w'):
  $! $L($c(1,pw(u[1],2)))
 if $((u,'$u'):
  $! pw($d(1,pw(u[1],2)),Q(-1,2))
 $! $#
$, tan_(u):
 if $D(u):
  if u==0:
   $! 0
  if $/(u)is $F:
   $! $U.tan(u)
  $! $#
 c=pi_coef(u)
 if c is $- $#:
  $! tan_pi(c)
 if $a(u)$+ $7(u):
  $! fvalc('tan',u)
 if isneg(u):
  $! $r(fn('tan',$r(u)))
 sp=split_pi(u)
 if sp is $- $#:
  c,$`=sp
  c=nsub(c,nfloor(c))
  if c==0:
   $! fn('tan',$`)
  if c==HALF:
   $! $r(pw(fn('tan',$`),-1))
  $!('tan',$d($`,$:(c,'pi')))
 if $((u,'$u'):
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
 if $D(u):
  if $/(u)is $F:
   if-1.0<=u<=1.0:
    $! $U.asin(u)
   $! fval('$w',u)
 if isneg(u):
  $! $r(fn('$w',$r(u)))
 S=inv_table()[0]
 if u in S:
  $! $:(S[u],'pi')
 if $7(u)$+ $a(u):
  $! fvalc('$w',u)
 $! $#
$, acos_(u):
 if $D(u)$+ $/(u)is $F:
  if-1.0<=u<=1.0:
   $! $U.acos(u)
  $! fval('arccos',u)
 a=asin_(u)
 if a is $- $# $+ $- $((a,'$w')$+ $9(a,'$w'):
  $! $c($:(HALF,'pi'),a)
 if isneg(u):
  $! $c('pi',fn('arccos',$r(u)))
 $! $#
$, atan_(u):
 if $D(u):
  if $/(u)is $F:
   $! $U.atan(u)
 if u=='$[':
  $! $:(HALF,'pi')
 if u==('*',-1,'$['):
  $! $:(Q(-1,2),'pi')
 if isneg(u):
  $! $r(fn('$u',$r(u)))
 Tn=inv_table()[1]
 if u in Tn:
  $! $:(Tn[u],'pi')
 if $7(u)$+ $a(u):
  $! fvalc('$u',u)
 $! $#
$, ln_(u):
 if $D(u):
  if u==1:
   $! 0
  if u==0:
   $!('*',-1,'$[')
  if $/(u)is $F:
   if u>0:
    $! $U.log(u)
   $! $d($U.log(-u),$:($U.pi,'i'))
  if $b(u)<0:
   $! $d(fn('ln',nneg(u)),$:('i','pi'))
  n,d=nd(u)
  if n==1:
   $! $r(fn('ln',d))
  $! $#
 if u=='e':
  $! 1
 if u=='$[':
  $! '$['
 if u=='i':
  $! $:(HALF,'i','pi')
 if $((u,'^'):
  if u[1]=='e' $+ isreal_expr(u[2]):
   $! u[2]
  if isposconst(u[1])$+ isreal_expr(u[2])$+ $D(u[2]):
   $! $:(u[2],fn('ln',u[1]))
 if $7(u)$+ $a(u):
  $! fvalc('ln',u)
 $! $#
$, log_(u,b=10):
 if $D(u)$+ $D(b):
  if $/(u)is $F or $/(b)is $F:
   a1=fvalc('ln',u)
   a2=fvalc('ln',b)
   if a1 is $- $# $+ a2 is $- $# $+ a2!=0:
    $! $Z(a1,a2)
   $! $#
  if u==1:
   $! 0
  if $q(u)$+ $q(b)$+ $b(u)>0 $+ $b(b)>0 $+ b!=1:
   k=exact_log(u,b)
   if k is $- $#:
    $! k
 if u==b:
  $! 1
 if $((u,'^')$+ u[1]==b $+ isreal_expr(u[2]):
  $! u[2]
 if $7(u)$+ $7(b)$+($a(u)or $a(b)):
  a1=fvalc('ln',u)
  a2=fvalc('ln',b)
  if a1 is $- $# $+ a2 is $- $# $+ a2!=0:
   $! $Z(a1,a2)
  $! $#
 $! $#
$, exact_log(u,b):
 un,ud=nd(u)
 bn,bd=nd(b)
 lu=$U.log(tofl(u))
 lb=$U.log(tofl(b))
 if lb==0:
  $! $#
 k=lu/lb
 $) den in $*(1,13):
  num=$t(round(k*den))
  if $J(k*den-num)<1e-9:
   kk=Q(num,den)
   if pw_num(b,kk)==u:
    $! kk
   $! $#
 $! $#
$, abs_(u):
 if $D(u):
  $! nabs(u)
 if u=='$[' or u==('*',-1,'$['):
  $! '$['
 if $((u,'$J'):
  $! u
 if $((u,'^')$+ $/(u[2])is $t $+ u[2]%2==0 $+ isreal_expr(u[1]):
  $! u
 if has(u,'i'):
  r,i=reim(u)
  if i!=0 $+ $- has(r,'i')$+ $- has(i,'i'):
   $! $L($d(pw(r,2),pw(i,2)))
 if $7(u):
  v=cv(u)
  if v is $- $# $+ $/(v)is $- $1:
   if v>=0:
    $! u
   $! $r(u)
 if $((u,'*'):
  outs=[]
  $`=[]
  $) f in u[1:]:
   if $D(f):
    outs.$%(nabs(f))
   $? $7(f):
    outs.$%(abs_(f)or('$J',f))
   $? $((f,'^')$+ $/(f[2])is $t $+ f[2]%2==0:
    outs.$%(f)
   $? $((f,'^')$+ f[1]=='e':
    outs.$%(f)
   $&:
    $`.$%(f)
  if outs:
   $! $H(outs+[fn('$J',$H($`))])
 if isneg(u):
  $! fn('$J',$r(u))
 if $((u,'^')$+ u[1]=='e' $+ isreal_expr(u[2]):
  $! u
 $! $#
$, sign_(u):
 if $D(u):
  $! $b(u)if $/(u)is $- $F $& $F($b(u))
 if u=='$[':
  $! 1
 if $7(u):
  v=cv(u)
  if v is $- $# $+ $/(v)is $- $1:
   $! 1 if v>0 $&(-1 if v<0 $& 0)
 if $((u,'*')$+ $D(u[1]):
  $! $:($b(u[1]),fn('sign',cmul(nabs(u[1]),$X(u)[1])))
 if $((u,'^')$+ $/(u[2])is $t $+ u[2]%2==0:
  $! $#
 $! $#
$, finite(v):
 $! v==v $+ v!=$F('$[')$+ v!=$F('-$[')
$, floor_(u):
 if $D(u):
  if $/(u)is $F:
   $! $F($U.floor(u))if finite(u)$& $#
  $! nfloor(u)
 if $7(u)$+ $- has(u,'i'):
  v=cv(u)
  if v is $- $# $+ $/(v)is $- $1:
   $! $t($U.floor(v))
 $! $#
$, ceil_(u):
 f=floor_($r(u))
 if f is $- $#:
  $! $r(f)
 $! $#
$, sinh_(u):
 if u==0:
  $! 0
 if isneg(u):
  $! $r(fn('sinh',$r(u)))
 if $((u,'arcsinh'):
  $! u[1]
 $! $#
''')
_x(r'''$, cosh_(u):
 if u==0:
  $! 1
 if isneg(u):
  $! fn('cosh',$r(u))
 if $((u,'arccosh'):
  $! u[1]
 $! $#
$, tanh_(u):
 if u==0:
  $! 0
 if isneg(u):
  $! $r(fn('tanh',$r(u)))
 $! $#
$, odd0($B):
 $, g(u):
  if u==0:
   $! 0
  if isneg(u):
   $! $r(fn($B,$r(u)))
  $! $#
 $! g
$, fact_(u):
 if $/(u)is $t:
  if u<0:
   $! '$M'
  if u>1000:
   $! $#
  r=1
  $) k in $*(2,u+1):
   r*=k
  $! r
 if isq(u)$+ u[2]==2 $+ u[1]>0:
  n=u[1]
  r=$:($L('pi'),Q(1,1))
  k=Q(1,2)
  $G ncmp(k,u)<=0:
   r=$:(r,k)
   k=nadd(k,1)
  $! r
 if $/(u)is $F:
  if u<0 $+ u==$U.floor(u):
   $! '$M'
  try:
   $! gamma(u+1.0)
  $6($W,$C,$P):
   $! '$[' if u>0 $& '$M'
 $! $#
$, gamma(x):
 try:
  $! $U.gamma(x)
 $6 AttributeError:
  pass
 if x<0.5:
  $! $U.pi/($U.sin($U.pi*x)*gamma(1.0-x))
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
 $! $U.$L(2*$U.pi)*h*$U.exp(-t)*h*a
$, real_(u):
 if $7(u)or has(u,'i'):
  r,i=reim(u)
  if $- $((r,'$S'):
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
 if $- $((r,'$S'):
  $! $c(r,$:('i',i))
 $! $#
$, angle_(u):
 r,i=reim(u)
 if $((r,'$S')or $((i,'imag'):
  $! $#
 if i==0:
  if $7(r):
   v=cv(r)
   if v is $- $# $+ $/(v)is $- $1:
    if v>=0:
     $! 0
    $! 'pi'
  $! $#
 if r==0:
  if $7(i):
   v=cv(i)
   if v is $- $# $+ $/(v)is $- $1:
    $! $:(Q(1 if v>0 $&-1,2),'pi')
  $! $#
 if $7(r)$+ $7(i):
  vr=cv(r)
  vi=cv(i)
  if vr is $# or vi is $# or $/(vr)is $1 or $/(vi)is $1:
   $! $#
  a=fn('$u',$Z(i,r))
  if vr<0:
   if vi>=0:
    a=$d(a,'pi')
   $&:
    a=$c(a,'pi')
  $! a
 $! $#
$m['sin']=sin_
$m['cos']=cos_
$m['tan']=tan_
$m['$w']=asin_
$m['arccos']=acos_
$m['$u']=atan_
$m['ln']=ln_
$m['log']=log_
$m['$J']=abs_
$m['sign']=sign_
$m['floor']=floor_
$m['ceiling']=ceil_
$m['sinh']=sinh_
$m['cosh']=cosh_
$m['tanh']=tanh_
$m['arcsinh']=odd0('arcsinh')
$m['arctanh']=odd0('arctanh')
$m['arccosh']=$5 u:0 if u==1 $& $#
$m['fact']=fact_
$m['$S']=real_
$m['imag']=imag_
$m['conj']=conj_
$m['$s']=angle_
$m['exp']=$5 u:pw('e',u)
$m['$L']=$5 u:pw(u,HALF)
$m['sec']=$5 u:pw(fn('cos',u),-1)
$m['csc']=$5 u:pw(fn('sin',u),-1)
$m['cot']=$5 u:pw(fn('tan',u),-1)
$m['sech']=$5 u:pw(fn('cosh',u),-1)
$m['csch']=$5 u:pw(fn('sinh',u),-1)
$m['coth']=$5 u:pw(fn('tanh',u),-1)
$m['arcsec']=$5 u:fn('arccos',pw(u,-1))
$m['arccsc']=$5 u:fn('$w',pw(u,-1))
$m['arccot']=$5 u:$c($:(HALF,'pi'),fn('$u',u))
$m['arcsech']=$5 u:fn('arccosh',pw(u,-1))
$m['arccsch']=$5 u:fn('arcsinh',pw(u,-1))
$m['arccoth']=$5 u:fn('arctanh',pw(u,-1))
$, root_(u,n=2):
 $! pw(u,pw(n,-1))
$m['root']=root_
import cmath
$, _c(f):
 $, g(x):
  try:
   if $/(x)is $1:
    $! f[1](x)
   $! f[0](x)
  $6($P,TypeError):
   $! f[1]($1(x))
 $! g
$, _ln(x):
 if $/(x)is $- $1 $+ x>0:
  $! $U.log(x)
 if x==0:
  $! $F('-$[')
 $! cmath.log($1(x))
$, _asinr(x):
 if-1<=x<=1:
  $! $U.asin(x)
 $n $P
$, _acosr(x):
 if-1<=x<=1:
  $! $U.acos(x)
 $n $P
$, _casin(z):
 $!-1j*cmath.log(1j*z+cmath.$L(1-z*z))
$, _cacos(z):
 $! $U.pi/2-_casin(z)
$, _catan(z):
 $! 0.5j*cmath.log((1-1j*z)/(1+1j*z))
$, _sinh(x):
 $!(cmath.exp(x)-cmath.exp(-x))/2 if $/(x)is $1 $&($U.exp(x)-$U.exp(-x))/2
$, _cosh(x):
 $!(cmath.exp(x)+cmath.exp(-x))/2 if $/(x)is $1 $&($U.exp(x)+$U.exp(-x))/2
$, _tanh(x):
 if $/(x)is $- $1:
  if x>20:
   $! 1.0
  if x<-20:
   $!-1.0
  a=$U.exp(2*x)
  $!(a-1)/(a+1)
 a=cmath.exp(2*x)
 $!(a-1)/(a+1)
$, _asinh(x):
 if $/(x)is $- $1:
  $! $U.log(x+$U.$L(x*x+1))if x>=0 $&-$U.log(-x+$U.$L(x*x+1))
 $! cmath.log(x+cmath.$L(x*x+1))
$, _acosh(x):
 if $/(x)is $- $1 $+ x>=1:
  $! $U.log(x+$U.$L(x*x-1))
 x=$1(x)
 $! cmath.log(x+cmath.$L(x+1)*cmath.$L(x-1))
$, _atanh(x):
 if $/(x)is $- $1 $+-1<x<1:
  $! 0.5*$U.log((1+x)/(1-x))
 x=$1(x)
 $! 0.5*cmath.log((1+x)/(1-x))
$, _sign(x):
 if $/(x)is $1:
  $! x/$J(x)if x!=0 $& 0.0
 $! 1.0 if x>0 $&(-1.0 if x<0 $& 0.0)
$, _floor(x):
 if $/(x)is $1:
  $! $1($U.floor(x.$S),$U.floor(x.imag))
 $! $F($U.floor(x))
$, _ceil(x):
 if $/(x)is $1:
  $! $1($U.ceil(x.$S),$U.ceil(x.imag))
 $! $F($U.ceil(x))
$, _real(x):
 $! x.$S if $/(x)is $1 $& x
$, _imag(x):
 $! x.imag if $/(x)is $1 $& 0.0
$, _conj(x):
 $! x.conjugate()if $/(x)is $1 $& x
$, _angle(x):
 if $/(x)is $1:
  $! cmath.phase(x)
 $! 0.0 if x>=0 $& $U.pi
$, _fact(x):
 if $/(x)is $1:
  $n $P
 $! gamma(x+1.0)
''')
_x(r'''NUMF={
 'sin':_c(($U.sin,cmath.sin)),'cos':_c(($U.cos,cmath.cos)),
 'tan':_c(($U.tan,$5 z:cmath.sin(z)/cmath.cos(z))),
 '$w':_c((_asinr,_casin)),'arccos':_c((_acosr,_cacos)),
 '$u':_c(($U.atan,_catan)),
 'ln':_ln,'exp':_c(($U.exp,cmath.exp)),
 '$L':_c(($5 x:$U.$L(x)if x>=0 $& cmath.$L(x),cmath.$L)),
 '$J':$J,'sign':_sign,'floor':_floor,'ceiling':_ceil,
 'sinh':_sinh,'cosh':_cosh,'tanh':_tanh,
 'arcsinh':_asinh,'arccosh':_acosh,'arctanh':_atanh,
 '$S':_real,'imag':_imag,'conj':_conj,'$s':_angle,
 'fact':_fact,
 }
$, nfun_call($B,$g):
 if $B=='log':
  b=$g[1]if $0($g)>1 $& 10.0
  $! _ln($g[0])/_ln(b)
 if $B=='root':
  n=$g[1]if $0($g)>1 $& 2.0
  $! npow($g[0],1.0/n)
 if $B=='round':
  d=$t($g[1])if $0($g)>1 $& 0
  $! round($g[0],d)
 if $B=='when':
  $! $g[1]if $g[0]$& $g[2]
 if $B=='max':
  $! max($g)
 if $B=='min':
  $! min($g)
 if $B=='mod':
  $! $g[0]-$g[1]*$U.floor($g[0]/$g[1])if $g[1]!=0 $& $g[0]
 f=NUMF.get($B)
 if f is $#:
  if $B in('sec','csc','cot','sech','csch','coth'):
   base={'sec':'cos','csc':'sin','cot':'tan','sech':'cosh','csch':'sinh','coth':'tanh'}[$B]
   $! 1.0/NUMF[base]($g[0])
  if $B in('arcsec','arccsc','arccot','arcsech','arccsch','arccoth'):
   base={'arcsec':'arccos','arccsc':'$w','arccot':'$u','arcsech':'arccosh','arccsch':'arcsinh','arccoth':'arctanh'}[$B]
   $! NUMF[base](1.0/$g[0])
  if $B in('ipart','$t'):
   $! $F($t($g[0]))
  if $B=='fpart':
   $! $g[0]-$t($g[0])
  err("Cannot evaluate "+$B)
 $! f($g[0])
$, npow(a,b):
 if $/(a)is $- $1 $+ $/(b)is $- $1:
  if a<0 $+(b!=b or b in($F('$['),$F('-$['))or b!=$U.floor(b)):
   $! $1(a)**b
  if a==0 $+ b<0:
   $n $C
  try:
   $! a**b
  $6 $W:
   $! $F('$[')
 if a==0:
  $! 0.0
 $! $1(a)**b
NCONST={'pi':$U.pi,'e':$U.e,'i':1j,'$[':$F('$[')}
$, $V(e,env=$#):
 t=$/(e)
 if t is $t:
  try:
   $! $F(e)
  $6 $W:
   $! '$[' if e>0 $&('*',-1,'$[')
 if t is $F:
  $! e
 if t is $p:
  if env is $- $# $+ e in env:
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
   s=s+$V(a,env)
  $! s
 if h=='*':
  s=1.0
  $) a in e[1:]:
   s=s*$V(a,env)
  $! s
 if h=='^':
  b=e[1]
  x=e[2]
  if isq(x)$+ x[2]%2==1:
   bv=$V(b,env)
   if $/(bv)is $- $1 $+ bv<0:
    r=(-bv)**(x[1]/x[2])
    $!-r if x[1]%2 $& r
   $! npow(bv,x[1]/x[2])
  if $/(x)is $t:
   bv=$V(b,env)
   if bv==0 $+ x<0:
    $n $C
   $! bv**x
  $! npow($V(b,env),$V(x,env))
 if h in('$I','mat','$p','Q'):
  err("Not numeric")
 if h=='when':
  c=nbool(e[1],env)
  $! $V(e[2]if c $& e[3],env)if $0(e)>3 or c $& $V(e[2],env)
 $g=[$V(a,env)$) a in e[1:]]
 $! nfun_call(h,$g)
$, nbool(c,env):
 h=head(c)
 if h in('<','>','<=','>=','=','/='):
  a=$V(c[1],env)
  b=$V(c[2],env)
  if $/(a)is $1:
   a=a.$S
  if $/(b)is $1:
   b=b.$S
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
 v=$V(e,env)
 if $/(v)is $1:
  if $J(v.imag)>1e-9*(1+$J(v.$S)):
   $n $P
  $! v.$S
 $! v
$, simp(e):
 t=$/(e)
 if t is $- $3:
  $! e
 h=e[0]
 if h=='Q' or h=='$p' or h=='hold':
  if h=='hold':
   $! simp(e[1])
  $! e
 $N=[simp(a)$) a in e[1:]]
 if h=='+':
  $! $8($N)
 if h=='*':
  $! $H($N)
 if h=='^':
  $! pw($N[0],$N[1])
 if h in('$I','mat','=','<','>','<=','>=','/=','$+','or','$-'):
  $!(h,)+$3($N)
 $! fn(h,$N)
$, $Y(e,old,new):
 if e==old:
  $! new
 t=$/(e)
 if t is $- $3 or e[0]=='Q' or e[0]=='$p':
  $! e
 ch=$2
 $N=[]
 $) a in e[1:]:
  b=$Y(a,old,new)
  if b is $- a:
   ch=$A
  $N.$%(b)
 if $- ch:
  $! e
 $! simp((e[0],)+$3($N))
$, subsd(e,d):
 t=$/(e)
 if t is $p:
  if e in d:
   $! d[e]
  $! e
 if t is $- $3 or e[0]=='Q' or e[0]=='$p':
  $! e
 ch=$2
 $N=[]
 $) a in e[1:]:
  b=subsd(a,d)
  if b is $- a:
   ch=$A
  $N.$%(b)
 if $- ch:
  $! e
 $! simp((e[0],)+$3($N))
$, mapexpr(f,e):
 if $((e,'$I'):
  $!('$I',)+$3(mapexpr(f,a)$) a in e[1:])
 if $((e,'mat'):
  $!('mat',)+$3(mapexpr(f,a)$) a in e[1:])
 $! f(e)
$, $=(e):
 t=$/(e)
 if t is $- $3:
  $! e
 h=e[0]
 if h=='Q' or h=='$p':
  $! e
 if h=='+':
  $! $8([$=(a)$) a in e[1:]])
 if h=='*':
  r=1
  $) f in e[1:]:
   r=expand_mul(r,$=(f))
  $! r
 if h=='^':
  b=$=(e[1])
  x=$=(e[2])
  if $((b,'+')$+ $/(x)is $t:
   if x>0:
    $! expand_pow(b,x)
   if x<0:
    $! pw(expand_pow(b,-x),-1)
  if $((b,'*')$+ $/(x)is $t:
   $! $=($H([pw(f,x)$) f in b[1:]]))
  if b=='e' $+ $((x,'+'):
   $! $H([pw('e',a)$) a in x[1:]])
  if $((x,'+')$+ $D(b):
   $! $H([pw(b,a)$) a in x[1:]])
  $! pw(b,x)
 if h in('$I','mat','=','<','>','<=','>=','/=','$+','or','$-'):
  $!(h,)+$3($=(a)$) a in e[1:])
 $! fn(h,[$=(a)$) a in e[1:]])
''')
_x(r'''$, evalf(e):
 t=$/(e)
 if t is $t:
  $! $F(e)
 if t is $F:
  $! e
 if t is $p:
  if e=='pi':
   $! $U.pi
  if e=='e':
   $! $U.e
  $! e
 h=e[0]
 if h=='Q':
  $! e[1]/e[2]
 if h=='$p':
  $! e
 if $7(e)$+ h $- in('$I','mat','=','<','>','<=','>=','/=','$+','or','$-'):
  try:
   v=$V(e)
   if $/(v)is $1:
    $! fromcomplex(v)
   if v!=v:
    $! '$M'
   if v==$F('$['):
    $! '$['
   if v==$F('-$['):
    $!('*',-1,'$[')
   $! v
  $6($C,$P,$W,TypeError):
   pass
  $6 $O:
   pass
 $N=[evalf(a)$) a in e[1:]]
 if h=='^' $+ $/(e[2])is $t:
  $N[1]=e[2]
 $! simp((h,)+$3($N))
$, exactify(e,tol=$#):
 t=$/(e)
 if t is $F:
  $! float2rat(e,tol)
 if t is $3 $+ e[0]!='Q' $+ e[0]!='$p':
  $! simp((e[0],)+$3(exactify(a,tol)$) a in e[1:]))
 $! e
$, float2rat(x,tol=$#):
 if x!=x:
  $! '$M'
 if x==$F('$['):
  $! '$['
 if x==$F('-$['):
  $!('*',-1,'$[')
 if x==$U.floor(x)$+ $J(x)<1e18:
  $! $t(x)
 if tol is $#:
  tol=5e-14*max(1.0,$J(x))
 h0,h1=0,1
 k0,k1=1,0
 y=x
 $) _ in $*(60):
  a=$U.floor(y)
  h0,h1=h1,$t(a)*h1+h0
  k0,k1=k1,$t(a)*k1+k0
  if $J(h1/k1-x)<=tol:
   $R
  f=y-a
  if f==0:
   $R
  y=1.0/f
 $! Q(h1,k1)
$, degree(e,x):
 if $9(e,x):
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
 if h=='^' $+ $/(e[2])is $t $+ e[2]>0:
  k=degree(e[1],x)
  if k is $#:
   $! $#
  $! k*e[2]
 $! $#
$, $_(e,x):
 e=$=(e)
 if $9(e,x):
  $![e]
 $Q=e[1:]if $((e,'+')$&(e,)
 cs={}
 mx=0
 $) t in $Q:
  if $((t,'*'):
   k=0
   $`=[]
   $) f in t[1:]:
    if f==x:
     k+=1
    $? $((f,'^')$+ f[1]==x $+ $/(f[2])is $t $+ f[2]>0:
     k+=f[2]
    $? $9(f,x):
     $`.$%(f)
    $&:
     $! $#
   c=$H($`)
  $? t==x:
   k=1
   c=1
  $? $((t,'^')$+ t[1]==x $+ $/(t[2])is $t $+ t[2]>0:
   k=t[2]
   c=1
  $? $9(t,x):
   k=0
   c=t
  $&:
   $! $#
  cs[k]=$d(cs.get(k,0),c)
  if k>mx:
   mx=k
 $![cs.get(k,0)$) k in $*(mx+1)]
$, fromcoeffs(cs,x):
 $! $8([$:(cs[k],pw(x,k))$) k in $*($0(cs))])
$, numer_denom(e):
 if $((e,'*'):
  nu=[]
  de=[]
  $) f in e[1:]:
   if isq(f):
    nu.$%(f[1])
    de.$%(f[2])
   $? $((f,'^')$+ $D(f[2])$+ $b(f[2])<0:
    de.$%(pw(f[1],nneg(f[2])))
   $&:
    nu.$%(f)
  $! $H(nu),$H(de)
 if isq(e):
  $! e[1],e[2]
 if $((e,'^')$+ $D(e[2])$+ $b(e[2])<0:
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
USYM={'pi':'\u03c0','$[':'\u221e','theta':'\u03b8'}
REL={'=':'=','<':'<','>':'>','<=':'\u2264','>=':'\u2265','/=':'\u2260'}
PRIO='xyztuvwsrqpnmlkjhgfdcba'
$, fmt(e):
 $! pr(e,$2)[0]
$, ffloat(x):
 if x!=x:
  $! '$M'
 if x==$F('$['):
  $! USYM['$[']if OPT['uni']$& '$['
 if x==$F('-$['):
  $! '-'+(USYM['$[']if OPT['uni']$& '$[')
 if x==0:
  $! '0.'
 d=OPT['digits']
 s=('%.'+$p(d)+'g')%x
 m=s
 ex=''
 if 'e' in s:
  m,ex=s.split('e')
  ex=$t(ex)
  ex='E'+$p(ex)
 if '.' in m:
  m=m.rstrip('0')
 $&:
  m=m+'.'
 $! m+ex
$, fnum(x):
 t=$/(x)
 if t is $t:
  $! $p(x),(P_ATOM if x>=0 $& P_NEG)
 if t is $F:
  s=ffloat(x)
  $! s,(P_ATOM if $- s.$x('-')$& P_NEG)
 s=$p(x[1])+'/'+$p(x[2])
 $! s,(P_PROD if x[1]>0 $& P_NEG)
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
 if t is $t or t is $F:
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
 if h=='$I':
  $! '{'+','.join([pr(a,keep)[0]$) a in e[1:]])+'}',P_ATOM
 if h=='mat' $+ $0(e)==2:
  $! '['+','.join([pr(a,keep)[0]$) a in e[1][1:]])+']',P_ATOM
 if h=='mat':
  $T=[]
  $) r in e[1:]:
   $T.$%('['+','.join([pr(a,keep)[0]$) a in r[1:]])+']')
  $! '['+''.join($T)+']',P_ATOM
 if h=='$p':
  $! '"'+e[1]+'"',P_ATOM
 if h in REL:
  op=REL[h]if OPT['uni']$& h
  a=pr(e[1],keep)
  b=pr(e[2],keep)
  $! paren(a[0],a[1],P_SUM)+op+paren(b[0],b[1],P_SUM),P_REL
 if h=='$+' $+ $0(e)==3 $+ head(e[1])in('<','<=')$+ head(e[2])in('<','<=')$+ e[1][2]==e[2][1]:
  op1=REL[e[1][0]]if OPT['uni']$& e[1][0]
  op2=REL[e[2][0]]if OPT['uni']$& e[2][0]
  $! pr(e[1][1],$2)[0]+op1+pr(e[1][2],$2)[0]+op2+pr(e[2][2],$2)[0],P_REL
 if h=='$+' or h=='or':
  p=P_AND if h=='$+' $& P_OR
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
  if $0(e)==2 or e[2]==10:
   $! 'log10('+pr(e[1],keep)[0]+')',P_ATOM
  $! 'log('+pr(e[1],keep)[0]+','+pr(e[2],keep)[0]+')',P_ATOM
 if h=='call':
  $! e[1]+'('+','.join([pr(a,keep)[0]$) a in e[2:]])+')',P_ATOM
 if h=='prime':
  $! e[1]+"'"*e[2],P_ATOM
 if h=='$j':
  nm='\u222b' if OPT['uni']$& '$j'
  $! nm+'('+','.join([pr(a,keep)[0]$) a in e[1:]])+')',P_ATOM
 if h=='sumseq':
  nm='\u03a3' if OPT['uni']$& 'sumseq'
  $! nm+'('+','.join([pr(a,keep)[0]$) a in e[1:]])+')',P_ATOM
 if h=='prodseq':
  nm='\u03a0' if OPT['uni']$& 'prodseq'
  $! nm+'('+','.join([pr(a,keep)[0]$) a in e[1:]])+')',P_ATOM
 if h=='$L' or h=='root':
  pass
 h=TINAME.get(h,h)
 $! h+'('+','.join([pr(a,keep)[0]$) a in e[1:]])+')',P_ATOM
TINAME={'ncr':'nCr','npr':'nPr'}
MAINV='xyzt'
$, varprio(v):
 i=MAINV.find(v)if $0(v)==1 $&-1
 if i<0:
  $!(100,v)
 $!(i,v)
$, facprio(v):
 i=MAINV.find(v)if $0(v)==1 $&-1
 if i<0:
  $!(0,v)
 $!(1,$p(i))
$, termdegs(t,d):
 c,r=$X(t)
 fs=r[1:]if $((r,'*')$&(r,)
 $) f in fs:
  if $/(f)is $p $+ f $- in SPECIAL:
   d[f]=d.get(f,0)+1
  $? $((f,'^')$+ $/(f[1])is $p $+ f[1]$- in SPECIAL $+ $D(f[2]):
   d[f[1]]=d.get(f[1],0)+tofl(f[2])
  $? $((f,'^')$+ $D(f[2]):
   $) v in $l(f[1]):
    d[v]=d.get(v,0)+tofl(f[2])*0.001
  $? $- $D(f)$+ $/(f)is $- $p:
   $) v in $l(f):
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
 $) k in $*($0($Q)):
  t=$Q[k]
  d=degs[k]
  if $D(t):
   keys.$%((2,(),0,0,(),''))
  $? $- d:
   cat=3 if has(t,'i')$& 1
   keys.$%((cat,(),0,1 if isneg(t)$& 0,(),okey($X(t)[1])))
  $&:
   keys.$%((0,$3([-d.get(v,0)$) v in mv]),-sum([d.get(v,0)$) v in ov]),
 1 if isneg(t)$& 0,$3([-d.get(v,0)$) v in ov]),okey($X(t)[1])))
 $! keys
$, pr_sum(e,keep):
 $Q=$I(e[1:])
 if $- keep:
  ks=sumkeys($Q)
  idx=$I($*($0($Q)))
  idx.sort(key=$5 i:ks[i])
  $Q=[$Q[i]$) i in idx]
 $<=''
 first=$A
 $) t in $Q:
  s,p=pr(t,$2)
  if p<P_SUM+1 $+ $- s.$x('-')$+ p<=P_SUM:
   s='('+s+')'
  if first:
   $<=s
   first=$2
  $? s.$x('-'):
   $<+=s
  $&:
   $<+='+'+s
 $! $<,P_SUM
$, fackey(f):
 if f=='pi' or f=='e' or isrrad(f)or $D(f):
  $!(0,(0,''),okey(f))
 if f=='i':
  $!(3,(0,''),'')
 if $/(f)is $p:
  $!(1,facprio(f),'')
 if $((f,'^')$+ $/(f[1])is $p:
  if f[1]=='e':
   $!(2,(0,''),okey(f))
  $!(1,facprio(f[1]),okey(f))
 if $((f,'+')or($((f,'^')$+ $((f[1],'+')):
  $!(4,(0,''),okey(f))
 $!(2,(0,''),okey(f))
$, pr_factor(f,keep,first):
 s,p=pr(f,keep)
 if p<P_PROD or(p==P_PROD $+ $- first)or(s.$x('-')$+ $- first):
  $! '('+s+')'
 $! s
''')
_x(r'''$, pr_prod(e,keep):
 fs=$I(e[1:])
 coef=1
 if fs $+ $D(fs[0])$+ $- keep:
  coef=fs[0]
  fs=fs[1:]
 num=[]
 den=[]
 $) f in fs:
  if $((f,'^')$+ $D(f[2])$+ $b(f[2])<0:
   ex=nneg(f[2])
   den.$%(f[1]if ex==1 $&('^',f[1],ex))
  $? isq(f)$+ keep:
   num.$%(f[1])
   den.$%(f[2])
  $&:
   num.$%(f)
 if $- keep:
  num.sort(key=fackey)
  den.sort(key=fackey)
 sign=''
 if keep $+ num $+ $D(num[0])$+ $b(num[0])<0:
  sign='-'
  if num[0]==-1:
   num=num[1:]
  $&:
   num[0]=nneg(num[0])
 cn=coef
 cd=1
 if $D(coef):
  if $b(coef)<0:
   sign='-'
   coef=nneg(coef)
  if isq(coef):
   cn=coef[1]
   cd=coef[2]
  $&:
   cn=coef
 if keep:
  num=[f $) f in num if f!=1]or[1]
 if sign $+ den $+ $- keep:
  sums=[k $) k in $*($0(num))if $((num[k],'+')]
  dsums=[k $) k in $*($0(den))if $((den[k],'+')]
  if $0(sums)==1 $+ any([isneg(t)$) t in num[sums[0]][1:]]):
   num=$I(num)
   num[sums[0]]=$:(-1,num[sums[0]])
   sign=''
  $? $0(dsums)==1 $+ $- sums $+ $0(den[dsums[0]])==3 $+ $7(den[dsums[0]])$+ any([isneg(t)$) t in den[dsums[0]][1:]]):
   den=$I(den)
   den[dsums[0]]=$:(-1,den[dsums[0]])
   sign=''
 parts=[]
 if cn!=1 or $/(cn)is $F:
  parts.$%(fnum(cn)[0])
 $) f in num:
  parts.$%(pr_factor(f,$2,$- parts))
 if $- parts:
  parts.$%('1')
 ns='*'.join(parts)
 if cd!=1:
  den.insert(0,cd)
 if $- den:
  if sign $+ $0(num)==1 $+ cn==1 $+ pr(num[0],$2)[1]<=P_SUM:
   $! sign+'('+pr(num[0],$2)[0]+')',P_NEG
  $! sign+ns,(P_NEG if sign $& P_PROD)
 if $0(parts)==1 $+ $0(num)==1 $+ cn==1:
  s,p=pr(num[0],$2)
  ns=paren(s,p,P_PROD+1)if p<P_PROD $& s
  if s.$x('-'):
   ns='('+s+')'
 dparts=[]
 $) f in den:
  dparts.$%(pr_factor(f,$2,$- dparts))
 ds='*'.join(dparts)
 if $0(den)>1:
  ds='('+ds+')'
 $&:
  s,p=pr(den[0],$2)
  if p<=P_PROD or s.$x('-'):
   ds='('+s+')'
 $! sign+ns+'/'+ds,(P_NEG if sign $& P_PROD)
$, pr_pow(e,keep):
 b=e[1]
 x=e[2]
 if $D(x)$+ $b(x)<0 $+ $- keep:
  ex=nneg(x)
  d=b if ex==1 $&('^',b,ex)
  s,p=pr(d,$2)
  if p<=P_PROD or s.$x('-'):
   s='('+s+')'
  $! '1/'+s,P_PROD
 if x==HALF:
  s,p=pr(b,$2)
  if OPT['uni']:
   if($/(b)is $t $+ b>=0)or($/(b)is $p):
    $! '\u221a'+s,P_POW
   $! '\u221a('+s+')',P_ATOM
  $! '$L('+s+')',P_ATOM
 bs,bp=pr(b,$2)
 if bp<=P_POW or bs.$x('-')or $((b,'fact'):
  bs='('+bs+')'
 xs,xp=pr(x,$2)
 if $-(($/(x)is $t $+ x>=0)or($/(x)is $p)):
  xs='('+xs+')'
 $! bs+'^'+xs,P_POW
$, fmt_top(e):
 if $((e,'mat')$+ $0(e)>2:
  $T=[]
  $) r in e[1:]:
   $T.$%('['+','.join([fmt(a)$) a in r[1:]])+']')
  if sum([$0(r)$) r in $T])>28:
   $! '['+('\n '.join($T))+']'
  $! '['+''.join($T)+']'
 if $((e,'$p'):
  $! e[1]
 $! fmt(e)
''')
_x(r'''REPL=(
 ('**','^'),('==','='),('!=','/='),
 ('sin\u207b\u00b9','$w'),('cos\u207b\u00b9','arccos'),('tan\u207b\u00b9','$u'),
 ('\u2212','-'),('\u2013','-'),('\u00d7','*'),('\u00b7','*'),
 ('\u2022','*'),('\u22c5','*'),('\u00f7','/'),('\u2264','<='),
 ('\u2265','>='),('\u2260','/='),('\u2192','->'),('\u21d2','=>'),
 ('\u21d4','<=>'),('\u207b\u00b9','^(-1)'),('\u00b2','^2'),
 ('\u00b3','^3'),('\u03c0',' pi '),('\u221e',' $[ '),
 ('\u212f',' e '),('\u2148',' i '),('\u03b8','theta'),
 ('\u222b',' $j'),('\u03a3',' sumseq'),('\u2211',' sumseq'),
 ('\u03a0',' prodseq'),('\u220f',' prodseq'),('\u1d07','E'),
 ('\u2032',"'"),('\u2033',"''"),('@i',' i '),('@e',' e '),
 ('@>','\u25ba'),('@d','\u00b0'),('@t','\u1d40'),('\u2044','/'),
 ('infinity','$['),('\u03b1','alpha'),('\u03b2','beta'),
 ('\u03bb','$5'),('\u03bc','mu'),('\u03c3','sigma'),
 ('\u0394','delta'),
 )
OPS=('<=>','=>','->','=:',':=','<=','>=','/=','<>','.^','.*',
 './','.+','.-','>>','+','-','*','/','^','(',')','{','}',
 '[',']',',',';','=','<','>','|','!','%','&','\u00b0',
 '\u2220','\u25ba','\u221a',"'",'\u1d40')
KEYW=('$+','or','xor','$-','nor','nand')
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
 n=$0(s)
 $G i<n:
  c=s[i]
  if c==' ' or c=='\t':
   i+=1
   $4
  if c=='0' $+ i+2<n $+ s[i+1]in 'bBhH':
   base=2 if s[i+1]in 'bB' $& 16
   j=i+2
   dg='01' if base==2 $& '0123456789abcdefABCDEF'
   $G j<n $+ s[j]in dg:
    j+=1
   if j>i+2:
    toks.$%(('num',$t(s[i+2:j],base)))
    i=j
    $4
  if isdig(c)or(c=='.' $+ i+1<n $+ isdig(s[i+1])):
   j=i
   $G j<n $+ isdig(s[j]):
    j+=1
   isf=$2
   if j<n $+ s[j]=='.' $+ $-(j+1<n $+ s[j+1]in '^*/+-' $+ $- isdig(s[j+1])):
    isf=$A
    j+=1
    $G j<n $+ isdig(s[j]):
     j+=1
   if j<n $+(s[j]=='E' or(s[j]=='e' $+ j+1<n $+ isdig(s[j+1]))):
    k=j+1
    if k<n $+ s[k]in '+-':
     k+=1
    if k<n $+ isdig(s[k]):
     isf=$A
     j=k
     $G j<n $+ isdig(s[j]):
      j+=1
   txt=s[i:j]
   if isf:
    toks.$%(('num',$F(txt)))
   $&:
    toks.$%(('num',$t(txt)))
   i=j
   $4
  if isletter(c):
   j=i
   $G j<n $+(isletter(s[j])or isdig(s[j])):
    j+=1
   $B=s[i:j].lower()
   toks.$%(('id',$B))
   i=j
   k=0
   $G i<n $+ s[i]=="'":
    k+=1
    i+=1
   if k:
    toks.$%(('prime',k))
   $4
  if c=='"':
   j=s.find('"',i+1)
   if j<0:
    $n $O('Missing "')
   toks.$%(('$p',s[i+1:j]))
   i=j+1
   $4
  $) op in OPS:
   if s.$x(op,i):
    i+=$0(op)
    if op=='<>':
     op='/='
    if op=='>>':
     op='\u25ba'
    toks.$%(('op',op))
    $R
  $&:
   $n $O('Invalid character: '+c)
 toks.$%(('end',$#))
 $! toks
''')
_x(r'''class Parser:
 $, __init__($;,toks,isfunc):
  $;.t=toks
  $;.i=0
  $;.isfunc=isfunc
 $, peek($;):
  $! $;.t[$;.i]
 $, nxt($;):
  tk=$;.t[$;.i]
  $;.i+=1
  $! tk
 $, isop($;,op):
  tk=$;.t[$;.i]
  $! tk[0]=='op' $+ tk[1]==op
 $, isid($;,$B):
  tk=$;.t[$;.i]
  $! tk[0]=='id' $+ tk[1]==$B
 $, expect($;,op):
  if $- $;.isop(op):
   tk=$;.peek()
   $n $O('Missing '+op)
  $;.i+=1
 $, top($;):
  e=$;.store()
  $G $;.isop('\u25ba'):
   $;.nxt()
   tk=$;.nxt()
   if tk[0]!='id':
    $n $O('Syntax error after conversion')
   $N=[]
   if $;.isop('('):
    $;.nxt()
    $N=$;.$N(')')
   e=('conv',e,tk[1])+$3($N)
  if $;.peek()[0]!='end':
   tk=$;.peek()
   $n $O('Syntax error near '+$p(tk[1])if tk[1]is $- $# $& 'Syntax error')
  $! e
 $, store($;):
  if $;.isid('define'):
   $;.nxt()
   lhs=$;.sum()
   if $- $;.isop('='):
    $n $O('Define needs =')
   $;.nxt()
   rhs=$;.wth()
   $!('define',lhs,rhs)
  e=$;.wth()
  if $;.isop('->')or $;.isop('=:'):
   $;.nxt()
   tgt=$;.wth()
   $!('store',e,tgt)
  if $;.isop(':='):
   $;.nxt()
   rhs=$;.wth()
   $!('define',e,rhs)
  $! e
 $, wth($;):
  e=$;.iff()
  $G $;.isop('|'):
   $;.nxt()
   c=$;.iff()
   e=('|',e,c)
  $! e
 $, iff($;):
  e=$;.imp()
  $G $;.isop('<=>'):
   $;.nxt()
   e=('<=>',e,$;.imp())
  $! e
 $, imp($;):
  e=$;.xor()
  $G $;.isop('=>'):
   $;.nxt()
   e=('=>',e,$;.xor())
  $! e
 $, xor($;):
  e=$;.lor()
  $G $;.isid('xor')or $;.isid('nor')or $;.isid('nand'):
   op=$;.nxt()[1]
   e=(op,e,$;.lor())
  $! e
 $, lor($;):
  e=$;.land()
  $G $;.isid('or'):
   $;.nxt()
   e=('or',e,$;.land())
  $! e
 $, land($;):
  e=$;.lnot()
  $G $;.isid('$+'):
   $;.nxt()
   e=('$+',e,$;.lnot())
  $! e
 $, lnot($;):
  if $;.isid('$-'):
   $;.nxt()
   $!('$-',$;.lnot())
  $! $;.rel()
 $, rel($;):
  a=$;.sum()
  tk=$;.peek()
  if tk[0]=='op' $+ tk[1]in('=','/=','<','>','<=','>='):
   $;.nxt()
   b=$;.sum()
   r=(tk[1],a,b)
   tk2=$;.peek()
   if tk2[0]=='op' $+ tk2[1]in('<','>','<=','>='):
    $;.nxt()
    c=$;.sum()
    r=('$+',r,(tk2[1],b,c))
   $! r
  $! a
 $, sum($;):
  a=$;.prod()
  $G $A:
   tk=$;.peek()
   if tk[0]=='op' $+ tk[1]in('+','-','.+','.-','&'):
    $;.nxt()
    b=$;.prod()
    op=tk[1]
    if op=='.+':
     op='+'
    $? op=='.-':
     op='-'
    a=(op,a,b)
   $&:
    $! a
 $, startsprimary($;):
  tk=$;.peek()
  if tk[0]=='num' or tk[0]=='$p':
   $! $A
  if tk[0]=='id':
   $! tk[1]$- in KEYW
  if tk[0]=='op':
   $! tk[1]in('(','{','\u221a')
  $! $2
 $, prod($;):
  a=$;.unary()
  $G $A:
   tk=$;.peek()
   if tk[0]=='op' $+ tk[1]in('*','/','.*','./'):
    $;.nxt()
    b=$;.unary()
    op=tk[1]
    a=(op,a,b)
   $? $;.startsprimary():
    b=$;.pw()
    a=('*',a,b)
   $&:
    $! a
 $, unary($;):
  if $;.isop('-'):
   $;.nxt()
   $!('$r',$;.unary())
  if $;.isop('+'):
   $;.nxt()
   $! $;.unary()
  $! $;.pw()
 $, pw($;):
  b=$;.post()
  if $;.isop('^')or $;.isop('.^'):
   op=$;.nxt()[1]
   if $;.isop('\u1d40')or $;.isid('t')$+ $2:
    pass
   x=$;.unary()
   $!('^' if op=='^' $& '.^',b,x)
  $! b
 $, post($;):
  a=$;.primary()
  $G $A:
   if $;.isop('!'):
    $;.nxt()
    a=('!',a)
   $? $;.isop('%'):
    $;.nxt()
    a=('%',a)
   $? $;.isop('\u00b0'):
    $;.nxt()
    a=('deg',a)
   $? $;.isop('\u1d40'):
    $;.nxt()
    a=('call','transpose',a)
   $? $;.isop('['):
    $;.nxt()
    idx=$;.$N(']')
    a=('index',a)+$3(idx)
   $&:
    $! a
 $, $N($;,close):
  $<=[]
  if $;.isop(close):
   $;.nxt()
   $! $<
  $G $A:
   $<.$%($;.store_in())
   if $;.isop(','):
    $;.nxt()
    $4
   $;.expect(close)
   $! $<
 $, store_in($;):
  e=$;.wth()
  $! e
 $, primary($;):
  tk=$;.nxt()
  k=tk[0]
  if k=='num':
   $! tk[1]
  if k=='$p':
   $!('$p',tk[1])
  if k=='id':
   $B=tk[1]
   if $B in KEYW:
    $n $O('Syntax error: '+$B)
   if $;.peek()[0]=='prime':
    n=$;.nxt()[1]
    if $;.isop('('):
     $;.nxt()
     a=$;.$N(')')
     $!('primecall',$B,n)+$3(a)
    $!('prime',$B,n)
   if $;.isop('(')$+($;.isfunc($B)or($0($B)>1 $+ $B $- in('pi','$[','$M','theta'))):
    $;.nxt()
    a=$;.$N(')')
    $!('call',$B)+$3(a)
   $! $B
  if k=='op':
   op=tk[1]
   if op=='(':
    e=$;.store_in()
    if $;.isop('\u2220'):
     $;.nxt()
     th=$;.store_in()
     $;.expect(')')
     $!('polar',e,th)
    $;.expect(')')
    $! e
   if op=='{':
    $!('$I',)+$3($;.$N('}'))
   if op=='[':
    $! $;.matrix()
   if op=='\u221a':
    $!('call','$L',$;.post())
   if op=='-':
    $!('$r',$;.pw())
  if k=='end':
   $n $O('Incomplete expression')
  $n $O('Syntax error near '+$p(tk[1]))
 $, matrix($;):
  $T=[]
  if $;.isop('['):
   $G $;.isop('['):
    $;.nxt()
    $T.$%(('$I',)+$3($;.$N(']')))
    if $;.isop(','):
     $;.nxt()
   $;.expect(']')
  $&:
   row=[]
   $G $A:
    if $;.isop(']'):
     $;.nxt()
     $R
    row.$%($;.store_in())
    if $;.isop(','):
     $;.nxt()
    $? $;.isop(';'):
     $;.nxt()
     $T.$%(('$I',)+$3(row))
     row=[]
    $? $;.isop(']'):
     $4
    $&:
     $n $O('Missing ]')
   $T.$%(('$I',)+$3(row))
  n=$0($T[0])
  $) r in $T:
   if $0(r)!=n:
    $n $O('Dimension error')
  $!('mat',)+$3($T)
''')
_x(r'''$, parse(s,isfunc):
 toks=tokenize(s)
 if toks[0][0]=='end':
  $n $O('Empty input')
 $! Parser(toks,isfunc).top()
''')
_x(r'''import cmath
$, $~(c,nv):
 if c==0:
  $!{}
 $!{(0,)*nv:c}
$, p_add(A,B):
 C=dict(A)
 $) m in B:
  v=C.get(m,0)+B[m]
  if v:
   C[m]=v
  $? m in C:
   del C[m]
 $! C
$, p_neg(A):
 $! dict([(m,-A[m])$) m in A])
$, p_sub(A,B):
 $! p_add(A,p_neg(B))
$, madd(a,b):
 $! $3([a[i]+b[i]$) i in $*($0(a))])
$, p_mul(A,B):
 C={}
 $) a in A:
  ca=A[a]
  $) b in B:
   m=madd(a,b)
   v=C.get(m,0)+ca*B[b]
   if v:
    C[m]=v
   $? m in C:
    del C[m]
 $! C
$, p_scale(A,c):
 if c==0:
  $!{}
 $! dict([(m,A[m]*c)$) m in A])
$, p_pow(A,n):
 nv=$0(next(iter(A)))if A $& 0
 R=$~(1,nv)
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
 $![k $) k in $*(nv)if p_deg(A,k)>0]
$, p_mono(nv,k,d):
 m=[0]*nv
 m[k]=d
 $! $3(m)
$, $K(A,B):
 if $- B:
  err("Division by zero")
 lmB=max(B)
 lcB=B[lmB]
 nv=$0(lmB)
 Qt={}
 R=dict(A)
 cnt=0
 $G R:
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
  d=$3(d)
  Qt[d]=Qt.get(d,0)+q
  $) m in B:
   mm=madd(m,d)
   v=R.get(mm,0)-q*B[m]
   if v:
    R[mm]=v
   $? mm in R:
    del R[mm]
 $! Qt
$, p_icont(A):
 g=0
 $) m in A:
  g=igcd(g,A[m])
  if g==1:
   $R
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
  if p_isconst(g)$+ $J(p_cval(g))==1:
   $! $~(1,nv)
 $! p_normsign(g)
EVP=(3,5,7,11,13,17,19,23,29,31,37,41)
$, p_at(A,pt):
 s=0
 $) m in A:
  t=A[m]
  $) i in $*($0(m)):
   if m[i]:
    t*=pt[i]**m[i]
  s+=t
 $! s
$, p_gcd(A,B,nv):
 if $- A:
  $! p_normsign(B)
 if $- B:
  $! p_normsign(A)
 if nv $+($0(A)>2 or $0(B)>2):
  c=igcd(p_icont(A),p_icont(B))
  ok=$A
  $) sh in(0,1):
   pt=[EVP[(i+sh*5)%$0(EVP)]*(1+sh)+i $) i in $*(nv)]
   g=igcd(p_at(A,pt),p_at(B,pt))
   if g!=c:
    ok=$2
    $R
  if ok:
   $! $~(c,nv)
 $! p_gcd0(A,B,nv)
$, p_gcd0(A,B,nv):
 if $- A:
  $! p_normsign(B)
 if $- B:
  $! p_normsign(A)
 vs=[]
 $) k in $*(nv):
  if p_deg(A,k)>0 or p_deg(B,k)>0:
   vs.$%(k)
 if $- vs:
  $! $~(igcd(p_cval(A),p_cval(B)),nv)
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
 $G pB $+ p_deg(pB,k)>0:
  r=prem(pA,pB,k,nv)
  pA=pB
  if $- r:
   pB={}
   $R
  pB=$K(r,p_cont(r,k,nv))
 if pB:
  g=$~(1,nv)
 $&:
  g=$K(pA,p_cont(pA,k,nv))
 $! p_normsign(p_mul(c,g))
$, prem(A,B,k,nv):
 dB=p_deg(B,k)
 lcB=p_lc(B,k)
 R=A
 $G R $+ p_deg(R,k)>=dB:
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
 $G p_deg(b,k)>0:
  a=p_gcd(b,d,nv)
  if p_deg(a,k)>0:
   res.$%((a,i))
  b=$K(b,a)
  c=$K(d,a)
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
 $) x in lm:
  if x%2:
   $! $#
 r=isqrt(lc)
 if r*r!=lc:
  $! $#
 hm=$3([x//2 $) x in lm])
 S={hm:r}
 nv=$0(lm)
 $) _ in $*($0(D)+3):
  R=p_sub(D,p_mul(S,S))
  if $- R:
   $! S
  lmR=max(R)
  lmS=max(S)
  m=[]
  $) i in $*(nv):
   x=lmR[i]-lmS[i]
   if x<0:
    $! $#
   m.$%(x)
  m=$3(m)
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
 if $/(x)is $t:
  $! b,x
 if isq(x):
  $! pw(b,Q(1,x[2])),x[1]
 c,r=$X(x)
 if $/(c)is $t $+ c!=1:
  $! pw(b,r),c
 if isq(c):
  $! pw(b,$:(Q(1,c[2]),r)),c[1]
 $! e,1
$, kernels(e,ks):
 t=$/(e)
 if t is $t or t is $F:
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
  if $/(e[2])is $t:
   kernels(e[1],ks)
   $!
  k,n=splitpow(e)
  if k==e or $- $((k,'^')or $A:
   if $((k,'^')$+ $/(k[2])is $t:
    kernels(k,ks)
    $!
   if k $- in ks:
    ks.$%(k)
  $!
 if e $- in ks:
  ks.$%(e)
$, sortkernels(ks):
 ks.sort(key=$5 k:varprio(k)if $/(k)is $p $&(200,okey(k)))
 $! ks
''')
_x(r'''$, ratform(e,ks):
 nv=$0(ks)
 t=$/(e)
 if t is $t:
  $! $~(e,nv),$~(1,nv)
 if t is $F:
  $! $#
 if t is $3 $+ e[0]=='Q':
  $! $~(e[1],nv),$~(e[2],nv)
 if e in ks:
  $!{p_mono(nv,ks.index(e),1):1},$~(1,nv)
 h=e[0]
 if h=='+':
  N={}
  D=$~(1,nv)
  $) a in e[1:]:
   r=ratform(a,ks)
   if r is $#:
    $! $#
   n,d=r
   if D==d:
    N=p_add(N,n)
   $&:
    g=p_gcd(D,d,nv)
    d1=$K(d,g)
    D1=$K(D,g)
    N=p_add(p_mul(N,d1),p_mul(n,D1))
    D=p_mul(D,d1)
  $! N,D
 if h=='*':
  N=$~(1,nv)
  D=$~(1,nv)
  $) a in e[1:]:
   r=ratform(a,ks)
   if r is $#:
    $! $#
   N=p_mul(N,r[0])
   D=p_mul(D,r[1])
  $! N,D
 if h=='^':
  if $/(e[2])is $t:
   b=e[1]
   n=e[2]
  $&:
   b,n=splitpow(e)
  if b in ks $+ b!=e or(b==e):
   if b $- in ks:
    $! $#
   k=ks.index(b)
   if n>=0:
    $!{p_mono(nv,k,n):1},$~(1,nv)
   $! $~(1,nv),{p_mono(nv,k,-n):1}
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
  $) i in $*($0(m)):
   if m[i]:
    fs.$%(pw(ks[i],m[i]))
  $Q.$%($H(fs))
 $! $8($Q)
$, cancel_pair(N,D,nv):
 g=p_gcd(N,D,nv)
 if $- p_isconst(g)or p_cval(g)!=1:
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
 N,D=cancel_pair(r[0],r[1],$0(ks))
 $! N,D,ks
$, comdenom(e):
 if $((e,'$I')or $((e,'mat'):
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
 if $((num,'+')$+ $((den,'+')or den==1 or $D(den):
  $! $Z(num,den)
 $! $Z(num,den)
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
 $! $/(e)is $3 $+ e[0]in('=','<','>','<=','>=','/=')
$, hasdenom(e):
 if $((e,'^')$+ $D(e[2])$+ $b(e[2])<0 $+ $- $7(e[1]):
  $! $A
 if $/(e)is $3 $+ e[0]in('+','*'):
  $) a in e[1:]:
   if hasdenom(a):
    $! $A
 $! $2
$, $.(e):
 t=$/(e)
 if t is $- $3 or e[0]=='Q' or e[0]=='$p':
  $! e
 h=e[0]
 $N=[$.(a)$) a in e[1:]]
 e2=simp((h,)+$3($N))if h!='hold' $& e
 if $- $((e2,'*'):
  $! e2
 hasden=$2
 hassum=$2
 $) f in e2[1:]:
  if $((f,'^')$+ $D(f[2])$+ $b(f[2])<0 $+ $- $7(f[1]):
   if $((f[1],'+')or($((f[1],'^')$+ $((f[1][1],'+')):
    hasden=$A
  if $((f,'+')or($((f,'^')$+ $((f[1],'+')):
   hassum=$A
 if $-(hasden $+ hassum)$+ $- hasden:
  $! e2
 if $a(e2):
  $! e2
 ks=[]
 kernels(e2,ks)
 sortkernels(ks)
 nv=$0(ks)
 if nv==0 or nv>6:
  $! e2
 nums=[]
 dens=[]
 $) f in e2[1:]:
  if $((f,'^')$+ $D(f[2])$+ $b(f[2])<0:
   dens.$%(pw(f[1],nneg(f[2])))
  $&:
   nums.$%(f)
 num=$H(nums)
 den=$H(dens)
 rn=ratform(num,ks)
 rd=ratform(den,ks)
 if rn is $# or rd is $#:
  $! e2
 if $0(rn[0])*$0(rd[1])>400 or $0(rn[1])*$0(rd[0])>400:
  $! e2
 N=p_mul(rn[0],rd[1])
 D=p_mul(rn[1],rd[0])
 if $0(N)>80 or $0(D)>80 or p_tdeg(N)>30 or p_tdeg(D)>30:
  $! e2
 g=p_gcd(N,D,nv)
 if p_isconst(g):
  $! e2
 N=$K(N,g)
 D=$K(D,g)
 if D $+ D[max(D)]<0:
  N=p_neg(N)
  D=p_neg(D)
 $! $Z(p2e(N,ks),p2e(D,ks))
$, u_trim(a):
 a=$I(a)
 $G a $+ a[-1]==0:
  a.pop()
 $! a
$, u_add(a,b):
 n=max($0(a),$0(b))
 $! u_trim([nadd(a[i]if i<$0(a)$& 0,b[i]if i<$0(b)$& 0)$) i in $*(n)])
$, u_neg(a):
 $![nneg(c)$) c in a]
$, u_sub(a,b):
 $! u_add(a,u_neg(b))
$, u_mul(a,b):
 if $- a or $- b:
  $![]
 r=[0]*($0(a)+$0(b)-1)
 $) i in $*($0(a)):
  if a[i]==0:
   $4
  $) j in $*($0(b)):
   r[i+j]=nadd(r[i+j],nmul(a[i],b[j]))
 $! u_trim(r)
$, u_scale(a,c):
 $! u_trim([nmul(x,c)$) x in a])
$, u_divmod(a,b):
 b=u_trim(b)
 if $- b:
  err("Division by zero")
 a=u_trim(a)
 q=[0]*max($0(a)-$0(b)+1,0)
 r=$I(a)
 lb=b[-1]
 $G $0(r)>=$0(b)$+ r:
  c=ndiv(r[-1],lb)
  k=$0(r)-$0(b)
  q[k]=c
  $) j in $*($0(b)):
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
 $! $8([$:(a[i],pw(x,i))$) i in $*($0(a))if a[i]!=0])
$, u_from_expr(e,x):
 cs=$_(e,x)
 if cs is $#:
  $! $#
 $) c in cs:
  if $- $q(c):
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
 if $0(a)<$0(b):
  $! $#
 q=[0]*($0(a)-$0(b)+1)
 lb=b[-1]
 $) k in $*($0(a)-$0(b),-1,-1):
  c=a[k+$0(b)-1]
  if c%lb:
   $! $#
  c//=lb
  q[k]=c
  if c:
   $) j in $*($0(b)):
    a[k+j]-=c*b[j]
 $) x in a:
  if x:
   $! $#
 $! q
''')
_x(r'''$, aberth(c):
 c=[$1(tofl(x))if $/(x)is $- $1 $& x $) x in c]
 $G c $+ c[-1]==0:
  c.pop()
 n=$0(c)-1
 if n<1:
  $![]
 zeros=0
 $G $J(c[0])==0:
  c.pop(0)
  zeros+=1
  n-=1
 $<=[0j]*zeros
 if n<1:
  $! $<
 if n==1:
  $! $<+[-c[0]/c[1]]
 a=[x/c[-1]$) x in c]
 r=0.0
 $) i in $*(n):
  v=$J(a[i])**(1.0/(n-i))
  if v>r:
   r=v
 r=max(r,1e-3)
 z=[r*cmath.exp(1j*(2*$U.pi*k/n+0.4))$) k in $*(n)]
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
    $4
   ratio=p/dp if dp!=0 $& 1e-3
   s=0j
   $) j in $*(n):
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
   $R
 res=[]
 $) zk in z:
  $) _ in $*(3):
   p=c[n]
   dp=0j
   $) j in $*(n-1,-1,-1):
    dp=dp*zk+p
    p=p*zk+c[j]
   if dp==0:
    $R
   zk=zk-p/dp
  res.$%(zk)
 $! $<+res
$, divisors_int(n,limit=400):
 n=$J(n)
 if n==0:
  $![1]
 fs,$`=factor_int_small(n)
 if $`>1:
  fs.$%(($`,1))
 ds=[1]
 $) p,k in fs:
  nd_=[]
  $) d in ds:
   v=d
   $) _ in $*(k+1):
    nd_.$%(v)
    v*=p
  ds=nd_
  if $0(ds)>limit:
   $! $#
 ds.sort()
 $! ds
$, combos(n,k):
 idx=$I($*(k))
 $G $A:
  yield idx
  i=k-1
  $G i>=0 $+ idx[i]==i+n-k:
   i-=1
  if i<0:
   $!
  idx[i]+=1
  $) j in $*(i+1,k):
   idx[j]=idx[j-1]+1
$, ifactor_sqf(f):
 n=$0(f)-1
 if n<=1:
  $![f]
 res=[]
 $G f[0]==0:
  res.$%([0,1])
  f=f[1:]
 if $0(f)-1<=1:
  $! res+[f]if $0(f)>1 $& res
 roots=aberth(f)
 lcd=divisors_int(f[-1])or[1]
 $`=[]
 $) r in roots:
  found=$2
  if $J(r.imag)<1e-6*(1+$J(r.$S)):
   $) q in lcd:
    p=$t(round(r.$S*q))
    if p==0 $+ $J(r.$S)>0.5/q:
     $4
    g=[-p,q]
    if igcd(p,q)!=1:
     $4
    qq=i_divexact(f,g)
    if qq is $- $#:
     res.$%(g)
     f=qq
     found=$A
     $R
  if $- found:
   $`.$%(r)
 if $0(f)-1<=3:
  if $0(f)>1:
   res.$%(f)
  $! res
 roots=$`
 if $0(roots)!=$0(f)-1:
  roots=aberth(f)
 lcd=divisors_int(f[-1])or[1]
 d=2
 $G d<=($0(f)-1)//2 $+ $0(roots)<=24:
  done=$2
  $) idx in combos($0(roots),d):
   pc=[1+0j]
   $) i in idx:
    r=roots[i]
    nw=[0j]*($0(pc)+1)
    $) j in $*($0(pc)):
     nw[j+1]+=pc[j]
     nw[j]-=pc[j]*r
    pc=nw
   ok=$A
   $) v in pc:
    if $J(v.imag)>1e-6*(1+$J(v.$S)):
     ok=$2
     $R
   if $- ok:
    $4
   $) q in lcd:
    g=[]
    good=$A
    $) v in pc:
     x=v.$S*q
     ix=$t(round(x))
     if $J(x-ix)>1e-5*(1+$J(x)):
      good=$2
      $R
     g.$%(ix)
    if $- good:
     $4
    qq=i_divexact(f,g)
    if qq is $- $#:
     res.$%(g)
     f=qq
     roots=[roots[i]$) i in $*($0(roots))if i $- in idx]
     done=$A
     $R
   if done:
    $R
  if $- done:
   d+=1
 if $0(f)>1:
  res.$%(f)
 $! res
$, ufactor(a):
 ints,c=u_toint(u_trim(a))
 if $0(ints)<=1:
  $! nmul(c,ints[0]if ints $& 0),[]
 nv=1
 P=dict([((i,),ints[i])$) i in $*($0(ints))if ints[i]])
 $<=[]
 mn=min([m[0]$) m in P])
 if mn>0:
  $<.$%(([0,1],mn))
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
    $<.$%((g,i))
 $&:
  c=nmul(c,p_cval(P))
 $! c,$<
$, i2p(f,nv,k):
 $! dict([(p_mono(nv,k,i),f[i])$) i in $*($0(f))if f[i]])
$, mfactor(P,nv):
 if $- P:
  $! 0,[]
 c=p_icont(P)
 if P[max(P)]<0:
  c=-c
 P=p_scale(P,1)if c==1 $& dict([(m,P[m]//c)$) m in P])
 res=[]
 mins=[min([m[k]$) m in P])$) k in $*(nv)]
 $) k in $*(nv):
  if mins[k]>0:
   res.$%(({p_mono(nv,k,1):1},mins[k]))
 if sum(mins):
  mn=$3(mins)
  P=dict([($3([m[i]-mn[i]$) i in $*(nv)]),P[m])$) m in P])
 c2=mfac_rec(P,nv,res,1)
 $! c*c2,res
$, mfac_rec(P,nv,res,mult):
 vs=p_vars(P,nv)
 if $- vs:
  $! p_cval(P)**mult if P $& 0
 if $0(vs)==1:
  k=vs[0]
  fl=[0]*(p_deg(P,k)+1)
  $) m in P:
   fl[m[k]]=P[m]
  cc,fs=ufactor(fl)
  $) g,i in fs:
   res.$%((i2p(g,nv,k),i*mult))
  $! cc**mult if $/(cc)is $t $& nipow(cc,mult)
 vs.sort(key=$5 k:p_deg(P,k))
 k=vs[0]
 cst=1
 C=p_cont(P,k,nv)
 if $- p_isconst(C):
  cst=mfac_rec(C,nv,res,mult)
  P=$K(P,C)
 $? p_cval(C)!=1:
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
  $? s!=d:
   $! $2
 $! $A
''')
_x(r'''$, msplit(F,nv,$@):
 vs=p_vars(F,nv)
 if $0(vs)<=1:
  if $- vs:
   $![F]
  k=vs[0]
  fl=[0]*(p_deg(F,k)+1)
  $) m in F:
   fl[m[k]]=F[m]
  cc,fs=ufactor(fl)
  $<=[]
  $) g,i in fs:
   $) _ in $*(i):
    $<.$%(i2p(g,nv,k))
  $! $< if $< $&[F]
 if $@>8:
  $![F]
 $) k in vs:
  if p_deg(F,k)==1:
   pass
 if $0(vs)==2 $+ ishomog(F):
  a,b=vs
  fl=[0]*(p_deg(F,a)+1)
  $) m in F:
   fl[m[a]]=F[m]
  cc,fs=ufactor(fl)
  if $0(fs)>1 or(fs $+ fs[0][1]>1):
   $<=[]
   $) g,i in fs:
    d=$0(g)-1
    G={}
    $) j in $*($0(g)):
     if g[j]:
      m=[0]*nv
      m[a]=j
      m[b]=d-j
      G[$3(m)]=g[j]
    $) _ in $*(i):
     $<.$%(G)
   $! $<
  $![F]
 $) k in vs:
  if p_deg(F,k)==2:
   A=p_coeff(F,k,2)
   B=p_coeff(F,k,1)
   C=p_coeff(F,k,0)
   D=p_sub(p_mul(B,B),p_scale(p_mul(A,C),4))
   S=p_sqrt(D)if D $&{}
   if S is $- $# $+ S:
    x={p_mono(nv,k,1):1}
    base=p_add(p_mul(p_scale(A,2),x),B)
    G1=p_sub(base,S)
    G2=p_add(base,S)
    G1=$K(G1,p_mul(p_cont(G1,k,nv),$~(p_icont($K(G1,p_cont(G1,k,nv))),nv)))
    G2=$K(G2,p_mul(p_cont(G2,k,nv),$~(p_icont($K(G2,p_cont(G2,k,nv))),nv)))
    if G1 $+ G2:
     $! msplit(G1,nv,$@+1)+msplit(G2,nv,$@+1)
 $) k in vs:
  if p_deg(F,k)<2:
   $4
  lc=p_lc(F,k)
  tc=p_coeff(F,k,0)
  da=pdivisors(lc,nv)
  db=pdivisors(tc,nv)
  if da is $# or db is $# or $0(da)*$0(db)>3000:
   $4
  x={p_mono(nv,k,1):1}
  $) a in da:
   ax=p_mul(a,x)
   $) b in db:
    $) s in(1,-1):
     G=p_add(ax,p_scale(b,s))
     Qt=$K(F,G)
     if Qt is $- $#:
      $![G]+msplit(Qt,nv,$@+1)
 $![F]
$, pdivisors(P,nv):
 c,fs=mfactor(P,nv)
 di=divisors_int(c,60)
 if di is $#:
  $! $#
 ds=[$~(d,nv)$) d in di]
 $) g,m in fs:
  nds=[]
  $) d in ds:
   v=d
   $) _ in $*(m+1):
    nds.$%(v)
    v=p_mul(v,g)
  ds=nds
  if $0(ds)>300:
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
   $4
  small,m=factor_int_small(m)
  $) p,k in small:
   fs[p]=fs.get(p,0)+k
  if m==1:
   $4
  if m>>1024:
   err('Number too large to factor')
  if isprime(m):
   fs[m]=fs.get(m,0)+1
   $4
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
   $4
  $) _ in $*(s-1):
   x=x*x%n
   if x==n-1:
    $R
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
    $R
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
  fs.$%(p if k==1 $&('^',p,k))
 $) p,k in factor_int_full(d):
  fs.$%(('^',p,-k))
 if $- fs:
  $! 1
 if $0(fs)==1 $+ fs[0]==-1:
  $!-1
 if $0(fs)==1:
  $!('hold',fs[0])
 $!('hold',('*',)+$3(fs))
$, $z(e,var=$#,$E=$2):
 if $q(e):
  $! factor_rat_held(e)
 if $((e,'$I')or $((e,'mat'):
  $! mapexpr($5 a:$z(a,var,$E),e)
 if isrel(e):
  $!(e[0],$z(e[1],var,$E),$z(e[2],var,$E))
 if $a(e):
  $! e
 ks=[]
 kernels(e,ks)
 sortkernels(ks)
 nv=$0(ks)
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
  nfac.${(split_radical(p2e(g,ks),m,var,$E))
 dfac=[]
 $) g,m in fd:
  dfac.${(split_radical(p2e(g,ks),m,var,$E))
 items=[]
 $) f,m in nfac:
  if $D(f):
   const=nmul(const,nipow(f,m))
  $&:
   items.$%((f,m))
 ditems=[]
 $) f,m in dfac:
  if $D(f):
   const=ndiv(const,nipow(f,m))
  $&:
   ditems.$%((f,m))
 items.sort(key=$5 fm:fsortkey(fm[0]))
 ditems.sort(key=$5 fm:fsortkey(fm[0]))
 $<=[]
 if const!=1 or($- items $+ $- ditems):
  $<.$%(const)
 $) f,m in items:
  $<.$%(f if m==1 $&('^',f,m))
 $) f,m in ditems:
  $<.$%(('^',f,-m))
 if $0($<)==1:
  if $(($<[0],'^')or $D($<[0]):
   $!('hold',$<[0])if $- $D($<[0])$& $<[0]
  $! $<[0]
 $!('hold',('*',)+$3($<))
$, fsortkey(f):
 ss=$l(f)
 ss.sort(key=varprio)
 d=0
 if ss:
  d=degree(f,ss[0])
  if d is $#:
   d=99
 $!($0(ss),okey(ss),d,okey(f))
$, split_radical(f,m,var,$E):
 if var is $# $+ $- $E:
  $![(f,m)]
 vs=$l(f)
 if var is $#:
  if $0(vs)!=1:
   $![(f,m)]
  x=vs[0]
 $&:
  x=var
 cs=$_(f,x)
 if cs is $# or $0(cs)!=3:
  if cs is $- $# $+ $0(cs)==2 $+ $E:
   $![(f,m)]
  $![(f,m)]
 c,b,a=cs
 D=$=($c($:(b,b),$:(4,a,c)))
 if $- $7(D):
  if var is $#:
   $![(f,m)]
 $&:
  v=$V(D)
  if $/(v)is $1:
   v=v.$S
  if v<0 $+ $- $E:
   $![(f,m)]
 sD=$L(D)
 r1=$Z($d($r(b),sD),$:(2,a))
 r2=$Z($c($r(b),sD),$:(2,a))
 res=[(a,m)]if a!=1 $&[]
 res.$%(($c(x,r2),m))
 res.$%(($c(x,r1),m))
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
 $) v in p_vars(N,$0(ks))+p_vars(D,$0(ks)):
  if v!=k:
   $! $#
 nv=$0(ks)
 num=[0]*(max(p_deg(N,k),0)+1)
 $) m in N:
  num[m[k]]=N[m]
 den=[0]*(p_deg(D,k)+1)
 $) m in D:
  den[m[k]]=D[m]
 if $0(den)<=1:
  $! $#
 q,rem=u_divmod(num,den)
 cc,fs=ufactor(den)
 $Q=[u_toexpr(q,x)]
 if rem:
  parts=[u_trim(pw_list(f,m))$) f,m in fs]
  rem=u_scale(rem,ninv(cc))
  $) j in $*($0(fs)):
   f,m=fs[j]
   Pj=parts[j]
   others=[1]
   $) i in $*($0(fs)):
    if i!=j:
     others=u_mul(others,parts[i])
   g,s,t=u_egcd(others,Pj)
   Aj=u_divmod(u_mul(rem,s),Pj)[1]
   fe=u_toexpr(f,x)
   $) p in $*(m,0,-1):
    if $- Aj:
     $R
    qq,cj=u_divmod(Aj,f)
    if cj:
     $Q.$%($Z(u_toexpr(cj,x),pw(fe,p)))
    Aj=qq
 $! $8($Q)
$, pw_list(f,m):
 r=[1]
 $) _ in $*(m):
  r=u_mul(r,f)
 $! r
$, propfrac(e,x=$#):
 if $q(e):
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
  vs=p_vars(D,$0(ks))
  if $- vs:
   $! e
  x=ks[vs[0]]
 num=p2e(N,ks)
 den=p2e(D,ks)
 cn=$_(num,x)
 cd=$_(den,x)
 if cn is $# or cd is $# or $0(cd)<=1:
  $! e
 qq,rr=e_divmod(cn,cd)
 $! $d(fromcoeffs(qq,x),$Z(fromcoeffs(rr,x),den))
$, e_divmod(a,b):
 a=[$=(c)$) c in a]
 b=[$=(c)$) c in b]
 $G b $+ b[-1]==0:
  b.pop()
 $G a $+ a[-1]==0:
  a.pop()
 if $- b:
  err("Division by zero")
 q=[0]*max($0(a)-$0(b)+1,1)
 r=$I(a)
 lb=b[-1]
 $G $0(r)>=$0(b)$+ r:
  c=$.($Z(r[-1],lb))
  kk=$0(r)-$0(b)
  q[kk]=c
  $) j in $*($0(b)):
   r[kk+j]=$=($c(r[kk+j],$:(c,b[j])))
  r.pop()
  $G r $+ r[-1]==0:
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
 nv=$0(ks)
 g=p_gcd(ra[0],rb[0],nv)
 if $- ks:
  $! p_cval(g)
 $! p2e(g,ks)
$, expand_full(e,var=$#):
 if $((e,'$I')or $((e,'mat'):
  $! mapexpr($5 a:expand_full(a,var),e)
 if isrel(e):
  $!(e[0],expand_full(e[1],var),expand_full(e[2],var))
 x=$=(e)
 if $- hasdenom(x)or $a(x):
  $! x
 if var is $#:
  ks=$l(x)
  ks.sort(key=varprio)
  $) v in ks:
   r=partfrac(x,v)
   if r is $- $#:
    $! $=(r)
  $! x
 r=partfrac(x,var)
 if r is $- $#:
  $! $=(r)
 $! x
''')
_x(r'''TV='T_'
LNT='LNT_'
VV='V_'
class $i($>):
 pass
$, dfun($B,u):
 if $B=='sin':
  $! fn('cos',u)
 if $B=='cos':
  $! $r(fn('sin',u))
 if $B=='tan':
  $! pw(fn('cos',u),-2)
 if $B=='$w':
  $! pw($c(1,pw(u,2)),Q(-1,2))
 if $B=='arccos':
  $! $r(pw($c(1,pw(u,2)),Q(-1,2)))
 if $B=='$u':
  $! pw($d(pw(u,2),1),-1)
 if $B=='sinh':
  $! fn('cosh',u)
 if $B=='cosh':
  $! fn('sinh',u)
 if $B=='tanh':
  $! pw(fn('cosh',u),-2)
 if $B=='arcsinh':
  $! pw($d(pw(u,2),1),Q(-1,2))
 if $B=='arccosh':
  $! pw($c(pw(u,2),1),Q(-1,2))
 if $B=='arctanh':
  $! pw($c(1,pw(u,2)),-1)
 if $B=='ln':
  $! pw(u,-1)
 if $B=='$J':
  $! fn('sign',u)
 if $B in('sign','floor','ceiling','round','ipart','$t'):
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
 if $((e,'$I')or $((e,'mat'):
  $! mapexpr($5 a:diff1(a,x),e)
 if $((e,'=')or $((e,'<')or $((e,'>'):
  $!(e[0],diff1(e[1],x),diff1(e[2],x))
 if $9(e,x):
  $! 0
 if e==x:
  $! 1
 h=e[0]
 if h=='+':
  $! $8([diff1(a,x)$) a in e[1:]])
 if h=='*':
  fs=e[1:]
  $Q=[]
  $) i in $*($0(fs)):
   d=diff1(fs[i],x)
   if d!=0:
    $Q.$%($H([d]+[fs[j]$) j in $*($0(fs))if j!=i]))
  $! $8($Q)
 if h=='^':
  b=e[1]
  p=e[2]
  if $9(p,x):
   $! $:(p,pw(b,$c(p,1)),diff1(b,x))
  if $9(b,x):
   $! $:(e,fn('ln',b),diff1(p,x))
  $! $:(e,$d($:(diff1(p,x),fn('ln',b)),$Z($:(p,diff1(b,x)),b)))
 if h=='log':
  b=e[2]if $0(e)>2 $& 10
  $! diff1($Z(fn('ln',e[1]),fn('ln',b)),x)
 if h=='when':
  $! fn('when',e[1],diff1(e[2],x),diff1(e[3],x))if $0(e)>3 $& fn('when',e[1],diff1(e[2],x))
 if h=='$j' $+ $0(e)==3 $+ e[2]==x:
  $! e[1]
 if h=='$j' $+ $0(e)==5 $+ $9(e[1],x)is $2 $+ e[2]!=x:
  f,v,a,b=e[1],e[2],e[3],e[4]
  $! $c($:($Y(f,v,b),diff1(b,x)),$:($Y(f,v,a),diff1(a,x)))
 if $0(e)==2:
  d=dfun(h,e[1])
  if d is $- $#:
   $! $:(d,diff1(e[1],x))
 $!('d',e,x)
$, $h(u,x):
 cs=$_(u,x)
 if cs is $# or $0(cs)!=2 or cs[1]==0:
  $! $#
 $! cs[1],cs[0]
$, nice(e):
 try:
  e=$.(e)
 $6 $>:
  $! e
 if $- hasdenom(e)or $a(e)or $((e,'$I')or $((e,'mat'):
  $! e
 best=e
 bl=$0(fmt(e))
 if bl>400:
  $! e
 $) f in(comdenom,$z):
  try:
   c=f(e)
   l=$0(fmt(c))
   if l<bl:
    best=c
    bl=l
  $6 $>:
   pass
 $! best
BUDGET=[0]
$, integrate(f,x,$@=0):
 BUDGET[0]=0
 r=integ(f,x,$@)
 if r is $#:
  $!('$j',f,x)
 $! r
$, integ(f,x,$@=0):
 if $@>7:
  $! $#
 if $@==0:
  BUDGET[0]=0
 BUDGET[0]+=1
 if BUDGET[0]>400:
  $! $#
 if $9(f,x):
  $! $:(f,x)
 if f==x:
  $! $:(HALF,pw(x,2))
 h=f[0]if $/(f)is $3 $& $#
 if h=='+':
  $<=[]
  $) t in f[1:]:
   r=integ(t,x,$@+1)
   if r is $#:
    $! integ_whole(f,x,$@)
   $<.$%(r)
  $! $8($<)
 if h=='*':
  c=[g $) g in f[1:]if $9(g,x)]
  v=[g $) g in f[1:]if $- $9(g,x)]
  if c:
   r=integ($H(v),x,$@)
   if r is $#:
    $! $#
   $! $:($H(c),r)
 r=itable(f,x)
 if r is $- $#:
  $! r
 $! integ_whole(f,x,$@)
$, integ_whole(f,x,$@):
 d=degree(f,x)
 if d is $- $#:
  g=$=(f)
  if g!=f:
   $! integ(g,x,$@+1)
 r=irational(f,x)
 if r is $- $#:
  $! r
 r=itanpow(f,x,$@)
 if r is $- $#:
  $! r
 r=isecpow(f,x,$@)
 if r is $- $#:
  $! r
 r=isubst(f,x,$@)
 if r is $- $#:
  $! r
 if hastrig(f):
  g=tcollect(f)
  if g!=f:
   r=integ(g,x,$@+1)
   if r is $- $#:
    $! r
 r=iparts(f,x,$@)
 if r is $- $#:
  $! r
 g=$=(f)
 if g!=f:
  r=integ(g,x,$@+1)
  if r is $- $#:
   $! r
 $! $#
''')
_x(r'''$, itable(f,x):
 h=head(f)
 if h=='^':
  b=f[1]
  p=f[2]
  if $9(p,x):
   lb=$h(b,x)
   if lb is $- $#:
    a=lb[0]
    if p==-1:
     $! $Z(fn('ln',fn('$J',b)),a)
    $! $Z(pw(b,$d(p,1)),$:(a,$d(p,1)))
   if(p==HALF or p==Q(-1,2))$+ degree(b,x)==2:
    $! iquadrad(b,p,x)
   if $0(b)==2 $+ head(b)in('sin','cos','tan','sinh','cosh')$+ $/(b)is $3:
    lu=$h(b[1],x)
    if lu is $- $#:
     a=lu[0]
     u=b[1]
     n=b[0]
     if n=='cos' $+ p==-2:
      $! $Z(fn('tan',u),a)
     if n=='sin' $+ p==-2:
      $! $Z($r(pw(fn('tan',u),-1)),a)
     if n=='cos' $+ p==-1:
      $! $Z(fn('ln',fn('$J',$d(pw(fn('cos',u),-1),fn('tan',u)))),a)
     if n=='sin' $+ p==-1:
      $! $Z(fn('ln',fn('$J',fn('tan',$:(HALF,u)))),a)
     if n=='tan' $+ p==-1:
      $! $Z(fn('ln',fn('$J',fn('sin',u))),a)
     if n=='cosh' $+ p==-2:
      $! $Z(fn('tanh',u),a)
  if $9(b,x):
   lu=$h(p,x)
   if lu is $- $#:
    a=lu[0]
    if b=='e':
     $! $Z(f,a)
    $! $Z(f,$:(a,fn('ln',b)))
  $! $#
 if $/(f)is $3 $+ $0(f)==2:
  u=f[1]
  lu=$h(u,x)
  if lu is $#:
   $! $#
  a=lu[0]
  r=$#
  if h=='sin':
   r=$r(fn('cos',u))
  $? h=='cos':
   r=fn('sin',u)
  $? h=='tan':
   r=$r(fn('ln',fn('$J',fn('cos',u))))
  $? h=='sinh':
   r=fn('cosh',u)
  $? h=='cosh':
   r=fn('sinh',u)
  $? h=='tanh':
   r=fn('ln',fn('cosh',u))
  $? h=='ln':
   r=$c($:(u,fn('ln',u)),u)
  $? h=='$u':
   r=$c($:(u,fn('$u',u)),$:(HALF,fn('ln',$d(pw(u,2),1))))
  $? h=='$w':
   r=$d($:(u,fn('$w',u)),$L($c(1,pw(u,2))))
  $? h=='arccos':
   r=$c($:(u,fn('arccos',u)),$L($c(1,pw(u,2))))
  $? h=='$J':
   r=$:(HALF,u,fn('$J',u))
  $? h=='sign':
   r=fn('$J',u)
  $? h=='arcsinh':
   r=$c($:(u,fn('arcsinh',u)),$L($d(pw(u,2),1)))
  $? h=='arctanh':
   r=$d($:(u,fn('arctanh',u)),$:(HALF,fn('ln',$c(1,pw(u,2)))))
  if r is $- $#:
   $! $Z(r,a)
 if h=='log' $+ $0(f)==3:
  lu=$h(f[1],x)
  if lu is $- $#:
   u=f[1]
   $! $Z($c($:(u,fn('ln',u)),u),$:(lu[0],fn('ln',f[2])))
 $! $#
$, iquadrad(b,p,x):
 cs=$_(b,x)
 C,B,A=cs
 if $- $7(A):
  $! $#
 av=$V(A)
 if $/(av)is $1:
  $! $#
 D=$c($:(B,B),$:(4,A,C))
 if p==Q(-1,2):
  if av<0:
   $! $:(pw($r(A),Q(-1,2)),fn('$w',$Z($r($d($:(2,A,x),B)),$L(D))))
  sA=$L(A)
  $! $:(pw(A,Q(-1,2)),fn('ln',fn('$J',$d($L(b),$:(sA,x),$Z(B,$:(2,sA))))))
 J=iquadrad(b,Q(-1,2),x)
 if J is $#:
  $! $#
 $! $d($Z($:($d($:(2,A,x),B),$L(b)),$:(4,A)),
 $:($Z($c($:(4,A,C),$:(B,B)),$:(8,A)),J))
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
 $<=[]
 $) t in $Q:
  if $- hasdenom(t):
   r=integ(t,x,5)
   if r is $#:
    $! $#
   $<.$%(r)
   $4
  fs=t[1:]if $((t,'*')$&(t,)
  num=[]
  den=$#
  k=1
  $) g in fs:
   if $((g,'^')$+ $/(g[2])is $t $+ g[2]<0:
    den=g[1]
    k=-g[2]
   $&:
    num.$%(g)
  if den is $#:
   $! $#
  N=$H(num)
  dg=degree(den,x)
  if dg==1:
   r=integ(t,x,5)
   if r is $#:
    $! $#
   $<.$%(r)
  $? dg==2:
   r=iquadfrac(N,den,k,x)
   if r is $#:
    $! $#
   $<.$%(r)
  $&:
   $! $#
 $! $8($<)
$, iquadfrac(N,Qd,k,x):
 cs=$_(N,x)
 if cs is $# or $0(cs)>2:
  $! $#
 n0=cs[0]
 n1=cs[1]if $0(cs)>1 $& 0
 C,B,A=$_(Qd,x)
 res=[]
 if n1!=0:
  if k==1:
   D=$c($:(B,B),$:(4,A,C))
   dv=$V(D)if $7(D)$& 0
   arg=Qd if($/(dv)is $- $1 $+ dv<0 $+ $V(A)>0)$& fn('$J',Qd)
   res.$%($:($Z(n1,$:(2,A)),fn('ln',arg)))
  $&:
   res.$%($:($Z(n1,$:(2,A)),$Z(-1,$:(k-1,pw(Qd,k-1)))))
 c0=$c(n0,$Z($:(n1,B),$:(2,A)))
 if c0!=0:
  J=jquad(A,B,C,Qd,k,x)
  if J is $#:
   $! $#
  res.$%($:(c0,J))
 $! $8(res)
$, jquad(A,B,C,Qd,k,x):
 D=$=($c($:(B,B),$:(4,A,C)))
 if k==1:
  if $- $7(D):
   $! $#
  dv=$V(D)
  if $/(dv)is $1:
   $! $#
  L=$d($:(2,A,x),B)
  if dv<0:
   s=$L($r(D))
   $! $:($Z(2,s),fn('$u',$Z(L,s)))
  if dv>0:
   s=$L(D)
   $! $:(pw(s,-1),fn('ln',fn('$J',$Z($c(L,s),$d(L,s)))))
  $! $Z(-2,L)
 Jp=jquad(A,B,C,Qd,k-1,x)
 if Jp is $#:
  $! $#
 Dl=$r(D)
 L=$d($:(2,A,x),B)
 $! $d($:($Z(L,$:(k-1,Dl)),pw(Qd,1-k)),
 $:($Z($:(2*k-3,2,A),$:(k-1,Dl)),Jp))
$, itanpow(f,x,$@):
 if $((f,'^')$+ $((f[1],'tan')$+ $/(f[2])is $t $+ f[2]>=2:
  u=f[1][1]
  lu=$h(u,x)
  if lu is $#:
   $! $#
  n=f[2]
  a=lu[0]
  t=f[1]
  first=$Z(pw(t,n-1),$:(n-1,a))
  $`=integ(pw(t,n-2),x,$@+1)
  if $` is $#:
   $! $#
  $! $c(first,$`)
 $! $#
$, isecpow(f,x,$@):
 if($((f,'^')$+ head(f[1])in('cos','sin')$+ $0(f[1])==2
 $+ $/(f[2])is $t $+ f[2]<=-3):
  u=f[1][1]
  lu=$h(u,x)
  if lu is $#:
   $! $#
  n=-f[2]
  a=lu[0]
  if f[1][0]=='cos':
   first=$:(pw(fn('cos',u),2-n),fn('tan',u))
  $&:
   first=$r($:(pw(fn('sin',u),2-n),pw(fn('tan',u),-1)))
  $`=integ(pw(f[1],2-n),x,$@+1)
  if $` is $#:
   $! $#
  $! $d($Z(first,$:(n-1,a)),$:(Q(n-2,n-1),$`))
 $! $#
''')
_x(r'''$, cands(f,x,$<):
 if $/(f)is $- $3 or $9(f,x)or f[0]=='Q':
  $!
 h=f[0]
 if h=='+' or h=='*':
  $) a in f[1:]:
   cands(a,x,$<)
  $!
 if h=='^':
  if f[1]!=x $+ $- $9(f[1],x)$+ f[1]$- in $<:
   $<.$%(f[1])
  if isq(f[2])$+ $- $9(f[1],x):
   rad=pw(f[1],Q(1,f[2][2]))
   if rad $- in $<:
    $<.$%(rad)
  if $- $9(f[2],x)$+ f[2]$- in $<:
   $<.$%(f[2])
   if f $- in $<:
    $<.$%(f)
  if f[1]==x $+ f $- in $< $+ $D(f[2])$+ f[2]!=-1:
   $<.$%(f)
   if $k(f[2])$+ f[2]%2==0 $+ f[2]>2 $+ pw(x,2)$- in $<:
    $<.$%(pw(x,2))
  cands(f[1],x,$<)
  cands(f[2],x,$<)
  $!
 if f $- in $<:
  $<.$%(f)
 $) a in f[1:]:
  if a!=x $+ $- $9(a,x)$+ a $- in $<:
   $<.$%(a)
  cands(a,x,$<)
$, subst_kernel(q,u,V,x):
 if $((u,'^')$+ u[1]==x $+ $D(u[2]):
  q2=$Y(q,x,pw(V,pw(u[2],-1)))
  $! $Y(q2,fn('$J',V),V)
 if $((u,'ln'):
  lu=$h(u[1],x)
  if lu is $- $#:
   a,b=lu
   $! $Y(q,x,$Z($c(pw('e',V),b),a))
 if $((u,'^')$+ isq(u[2])$+ $- $9(u[1],x):
  cs_=$_(u[1],x)
  q2=$Y(q,u,V)
  if cs_ is $- $# $+ $- $9(q2,x):
   nz=[k $) k in $*(1,$0(cs_))if cs_[k]!=0]
   if $0(nz)==1:
    k=nz[0]
    xk=$Z($c(pw(V,pw(u[2],-1)),cs_[0]),cs_[k])
    q3=$Y(q2,x,pw(xk,Q(1,k)))
    if $9(q3,x):
     $! q3
  $! q2
 if $((u,'^')$+ u[1]=='e':
  lu=$h(u[2],x)
  if lu is $- $# $+ lu[1]==0:
   a=lu[0]
   $! subst_exp(q,a,V,x)
 $! $Y(q,u,V)
$, subst_exp(q,a,V,x):
 if $/(q)is $- $3 or q[0]=='Q':
  $! q
 if q[0]=='^' $+ q[1]=='e':
  lm=$h(q[2],x)
  if lm is $- $#:
   $! $:(pw(V,$Z(lm[0],a)),pw('e',lm[1]))
 $! simp((q[0],)+$3(subst_exp(b,a,V,x)$) b in q[1:]))
$, isubst(f,x,$@):
 if $@>5:
  $! $#
 VV='V%d_'%$@
 $G has(f,VV)or VV==x:
  VV=VV+'_'
 cs=[]
 cands(f,x,cs)
 fracf=hasfracpow(f,x)
 big=$0(okey(f))>500
 $) u in cs[:14]:
  if u==x:
   $4
  du=diff(u,x)
  if du==0:
   $4
  q=$Z(f,du)
  if $- big:
   q=$.(q)
  q2=subst_kernel(q,u,VV,x)
  if $9(q2,x)$+(fracf or $- hasfracpow(q2,VV))$+ $0(okey(q2))<800:
   r=integ(q2,VV,$@+2)
   if r is $- $#:
    $! $Y(r,VV,u)
 $) u in cs:
  if $((u,'+'):
   lu=$h(u,x)
   if lu is $- $#:
    a,b=lu
    g=$=($Z($Y(f,x,$Z($c(VV,b),a)),a))
    r=integ(g,VV,$@+2)
    if r is $- $#:
     $! $Y(r,VV,u)
 $! $#
$, hasfracpow(e,x):
 if $/(e)is $- $3 or e[0]=='Q':
  $! $2
 if e[0]=='^' $+ $- $k(e[2])$+ $- $9(e[1],x):
  $! $A
 $) a in e[1:]:
  if hasfracpow(a,x):
   $! $A
 $! $2
$, hastrig(f):
 if $/(f)is $- $3 or f[0]=='Q':
  $! $2
 if f[0]in('sin','cos'):
  $! $A
 $) a in f[1:]:
  if hastrig(a):
   $! $A
 $! $2
$, ispoly(e,x):
 $! degree(e,x)is $- $#
$, iparts(f,x,$@):
 if $@>5:
  $! $#
 fs=f[1:]if $((f,'*')$&(f,)
 P=[]
 G=[]
 $) g in fs:
  if ispoly(g,x):
   P.$%(g)
  $&:
   G.$%(g)
 if $0(G)==2:
  ex=$#
  tr=$#
  $) g in G:
   if $((g,'^')$+ g[1]=='e' $+ $h(g[2],x):
    ex=g
   $? head(g)in('sin','cos')$+ $h(g[1],x):
    tr=g
  if ex is $- $# $+ tr is $- $# $+ $- P:
   a=$h(ex[2],x)[0]
   b=$h(tr[1],x)[0]
   u=tr[1]
   den=$d($:(a,a),$:(b,b))
   if tr[0]=='sin':
    r=$:(ex,$c($:(a,fn('sin',u)),$:(b,fn('cos',u))))
   $&:
    r=$:(ex,$d($:(a,fn('cos',u)),$:(b,fn('sin',u))))
   $! $Z(r,den)
  $! $#
 if $0(G)!=1:
  $! $#
 g=G[0]
 Pp=$H(P)
 gh=head(g)
 tabular=$2
 if $((g,'^')$+ g[1]=='e' $+ $h(g[2],x):
  tabular=$A
 $? $((g,'^')$+ $D(g[1])$+ $h(g[2],x):
  tabular=$A
 $? gh in('sin','cos','sinh','cosh')$+ $h(g[1],x):
  tabular=$A
 if tabular $+ P:
  res=[]
  sg=1
  Gi=g
  Pd=Pp
  $) _ in $*(40):
   Gi=integ(Gi,x,$@+1)
   if Gi is $#:
    $! $#
   res.$%($:(sg,Pd,Gi))
   Pd=diff(Pd,x)
   sg=-sg
   if Pd==0:
    $! $8(res)
  $! $#
 if gh in('ln','$u','$w','arccos','log','arcsinh','arctanh')or($((g,'^')$+ head(g[1])in('ln','$w','$u')$+ $k(g[2])$+ g[2]>0):
  V=integ(Pp,x,$@+1)
  if V is $#:
   $! $#
  $`=integ($.($=($:(V,diff(g,x)))),x,$@+1)
  if $` is $#:
   $! $#
  $! $c($:(g,V),$`)
 $! $#
$, defint(f,x,a,b):
 if a==b:
  $! 0
 BUDGET[0]=0
 F=integ(f,x)
 if F is $- $# $+ $- $a(f):
  sing=singular_points(f,x,a,b)
  if sing is $#:
   sing=[]
  pts=[a]+sing+[b]
  total=0
  $) i in $*($0(pts)-1):
   lo=pts[i]
   hi=pts[i+1]
   vb=limit(F,x,hi,-1 if $- isinf(hi)$& 0)
   va=limit(F,x,lo,1 if $- isinf(lo)$& 0)
   if $((vb,'limit')or $((va,'limit'):
    total=$#
    $R
   total=$d(total,$c(vb,va))
  if total is $- $# $+ total!='$M':
   $! total
 if $7(a)$+ $7(b)$+ freeofall(f,[s $) s in $l(f)if s!=x]):
  try:
   $! nint(f,x,a,b)
  $6 $>:
   pass
 $!('$j',f,x,a,b)
$, isinf(v):
 $! v=='$[' or v==('*',-1,'$[')
$, singular_points(f,x,a,b):
 if $-($7(a)$+ $7(b)):
  $![]
 try:
  av=nreal(a)if $- isinf(a)$&(-1e300 if a!='$[' $& 1e300)
  bv=nreal(b)if $- isinf(b)$&(1e300 if b=='$[' $&-1e300)
 $6 $>:
  $![]
 lo,hi=min(av,bv),max(av,bv)
 pts=[]
 dens=[]
 collect_dens(f,x,dens)
 $) d in dens:
  u=u_from_expr(d,x)
  if u is $# or $0(u)<2:
   $4
  $) r in aberth(u):
   if $J(r.imag)<1e-9 $+ lo<r.$S<hi:
    rr=exactify(r.$S)if $J(r.$S-round(r.$S))<1e-12 $& r.$S
    pts.$%(rr)
 pts.sort(key=$5 p:tofl(p))
 if av>bv:
  pts.reverse()
 $! pts
''')
_x(r'''$, collect_dens(f,x,$<):
 if $/(f)is $- $3 or f[0]=='Q':
  $!
 if f[0]=='^' $+ $D(f[2])$+ $b(f[2])<0 $+ $- $9(f[1],x):
  $<.$%(f[1])
 if f[0]=='ln' or f[0]=='tan':
  pass
 $) a in f[1:]:
  collect_dens(a,x,$<)
$, nint(f,x,a,b,tol=1e-10):
 r=nint0(f,x,a,b,tol)
 if $/(r)is $1:
  if $J(r.imag)<1e-12*(1+$J(r.$S)):
   $! r.$S
  $! fromcomplex(r)
 $! r
$, nint0(f,x,a,b,tol=1e-10):
 sgn=1.0
 av=a
 bv=b
 if isinf(a)or isinf(b):
  if a=='$[' or b==('*',-1,'$['):
   $!-nint0(f,x,b,a,tol)
  if isinf(a)$+ isinf(b):
   g=$5 t:_nv(f,x,t/(1-t*t))*(1+t*t)/(1-t*t)**2
   $! _gk_adapt(g,-1.0,1.0,tol,0)
  if isinf(b):
   a0=nreal(a)
   g=$5 t:_nv(f,x,a0+t/(1-t))/(1-t)**2
   $! _gk_adapt(g,0.0,1.0,tol,0)
  b0=nreal(b)
  g=$5 t:_nv(f,x,b0-(1-t)/t)/(t*t)
  $! _gk_adapt(g,0.0,1.0,tol,0)
 a0=nreal(a)
 b0=nreal(b)
 g=$5 t:_nv(f,x,t)
 $! _gk_adapt(g,a0,b0,tol,0)
$, _nv(f,x,t):
 try:
  v=$V(f,{x:t})
 $6 $C:
  $! 0.0
 $6($P,$W):
  $! 0.0
 if $/(v)is $1:
  if $J(v.imag)>1e-12*(1+$J(v.$S)):
   $! v
  v=v.$S
 if v!=v or v in($F('$['),$F('-$[')):
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
 $! rk*h,$J((rk-rg)*h)
$, _gk_adapt(g,a,b,tol,$@):
 r,e=_gk(g,a,b)
 if e<=tol*max(1.0,$J(r))or $@>18:
  $! r
 m=0.5*(a+b)
 $! _gk_adapt(g,a,m,tol/2,$@+1)+_gk_adapt(g,m,b,tol/2,$@+1)
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
 c=$=(c)
 if hasdenom(c):
  c=$.(c)
 $! c
$, s_add(A,B):
 p=A[1]if ncmp(A[1],B[1])<0 $& B[1]
 d={}
 $) S in(A,B):
  $) k in S[0]:
   if ncmp(k,p)<0:
    d[k]=$d(d.get(k,0),S[0][k])
 $<={}
 $) k in d:
  v=cs(d[k])
  if v!=0:
   $<[k]=v
 $!($<,p)
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
    d[k]=$d(d.get(k,0),$:(A[0][a],B[0][b]))
 $<={}
 $) k in d:
  v=cs(d[k])
  if v!=0:
   $<[k]=v
 $!($<,p)
$, s_scale(A,c,shift=0):
 $<={}
 $) k in A[0]:
  v=cs($:(A[0][k],c))
  if v!=0:
   $<[nadd(k,shift)]=v
 $!($<,nadd(A[1],shift))
$, s_lead(A):
 if $- A[0]:
  $n $i()
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
 $) k in $*(1,$0(coefs)):
  P=s_mul(P,U)
  if $- P[0]:
   $R
  if coefs[k]!=0:
   res=s_add(res,s_scale(P,coefs[k]))
 $! res
$, nterms(U):
 v=s_val(U)
 if ncmp(v,0)<=0:
  $n $i()
 p=U[1]
 if ncmp(p,BIGP)>=0:
  $! 0 if $- U[0]$& 30
 n=nfloor(ndiv(p,v))+1
 if n>30:
  n=30
 $! n
$, s_pow(A,p):
 if $/(p)is $t $+ p>=0:
  R=({0:1},BIGP)
  $) _ in $*(p):
   R=s_mul(R,A)
  $! R
 a,c,U=s_split(A)
 n=nterms(U)if U[0]$& 0
 coefs=[1]
 b=1
 $) k in $*(1,n+1):
  b=$:(b,$Z($c(p,k-1),k))
  coefs.$%(b)
 S=s_powser(U,coefs)if U[0]$&({0:1},U[1])
 ap=$:(a,p)
 if $- $q(ap):
  $n $i()
 cp=pw(c,p)
 $! s_scale(S,cp,ap)
$, s_exp(A):
 neg_=[k $) k in A[0]if ncmp(k,0)<0]
 if neg_:
  $n $i()
 c0=A[0].get(0,0)
 U=(dict([(k,A[0][k])$) k in A[0]if k!=0]),A[1])
 shift=0
 if has(c0,LNT):
  cc=$_(c0,LNT)
  if cc is $# or $0(cc)!=2 or $- $q(cc[1]):
   $n $i()
  shift=cc[1]
  c0=cc[0]
 n=nterms(U)if U[0]$& 0
 coefs=[1]
 f=1
 $) k in $*(1,n+1):
  f=f*k
  coefs.$%(Q(1,f))
 S=s_powser(U,coefs)if U[0]$&({0:1},U[1])
 $! s_scale(S,pw('e',c0),shift)
$, s_ln(A):
 a,c,U=s_split(A)
 n=nterms(U)if U[0]$& 0
 coefs=[0]
 $) k in $*(1,n+1):
  coefs.$%(Q((-1)**(k+1),k))
 S=s_powser(U,coefs)if U[0]$&({},U[1])
 base=$d(fn('ln',c),$:(a,LNT))
 $! s_add(S,(({0:base}if base!=0 $&{}),BIGP))
''')
_x(r'''$, s_fun($B,A):
 neg_=[k $) k in A[0]if ncmp(k,0)<0]
 if neg_:
  if $B=='$u':
   a,c=s_lead(A)
   sg=$V(c)
   sg=1 if($/(sg)is $- $1 $+ sg>0)$&-1
   inv_=s_pow(A,-1)
   $! s_add(s_const($:(sg,HALF,'pi')),s_scale(s_fun('$u',inv_),-1))
  if $B=='tanh':
   a,c=s_lead(A)
   $! s_const(1 if $V(c).$S>0 $&-1)
  $n $i()
 c0=A[0].get(0,0)
 if has(c0,LNT):
  $n $i()
 U=(dict([(k,A[0][k])$) k in A[0]if k!=0]),A[1])
 if $B=='$J' or $B=='sign':
  a,c=s_lead(A)
  v=$V($Y(c,LNT,-1000))if has(c,LNT)$& $V(c)
  if $/(v)is $1:
   $n $i()
  sg=1 if v>0 $&-1
  if $B=='sign':
   $! s_const(sg)
  $! s_scale(A,sg)
 if $B in('floor','ceiling','ipart','round','$t','fpart'):
  $n $i()
 n=nterms(U)if U[0]$& 0
 z='Z_'
 g=fn($B,z)
 coefs=[$Y(g,z,c0)]
 fact=1
 $) k in $*(1,n+1):
  g=diff(g,z)
  fact*=k
  coefs.$%(cs($Z($Y(g,z,c0),fact)))
 $) cc in coefs:
  if has(cc,'$M')or cc=='$M' or has(cc,'$['):
   $n $i()
 if $- U[0]:
  $! s_const(coefs[0])if $A $& $#
 $! s_powser(U,coefs)
$, ser(e,N):
 if $9(e,TV):
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
  if $9(p,TV):
   B=ser(b,N)
   if $q(p):
    $! trunc(s_pow(B,p),N)
   if $7(p)or $A:
    a,c,U=s_split(B)
    if a!=0:
     $n $i()
    $! trunc(s_pow(B,p),N)
  if $9(b,TV):
   $! trunc(s_exp(s_scale(ser(p,N),fn('ln',b))),N)
  $! trunc(s_exp(s_mul(ser(p,N),s_ln(ser(b,N)))),N)
 if h=='ln':
  $! trunc(s_ln(ser(e[1],N)),N)
 if h=='log':
  b=e[2]if $0(e)>2 $& 10
  $! trunc(s_scale(s_ln(ser(e[1],N)),pw(fn('ln',b),-1)),N)
 if $0(e)==2:
  $! trunc(s_fun(h,ser(e[1],N)),N)
 $n $i()
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
 cc=$_(c,LNT)
 if cc is $#:
  v=$V($Y(c,LNT,-1e6))
  $! v
 k=$0(cc)-1
 lead=cc[k]
 v=$V(lead)
 if $/(v)is $1:
  $! v
 if k%2:
  v=-v
 $! v
$, limit(f,x,a,dirn=0):
 if $((f,'$I')or $((f,'mat'):
  $! mapexpr($5 g:limit(g,x,a,dirn),f)
 if $9(f,x):
  $! f
 if a=='$[' or a==('*',-1,'$['):
  sub_=pw(TV,-1)if a=='$[' $& $r(pw(TV,-1))
  $! lim_side(f,x,sub_,a)
 if dirn==0 $+ $- has_disc(f):
  try:
   v=$Y(f,x,a)
   if v!='$M' $+ $9(v,'$M')$+ $- has(v,'$['):
    v2=v
    if $7(v2):
     vv=$V(v2)
     if $/(vv)is $1 $+ $J(vv.imag)>1e-12 $+ $9(f,'i'):
      $n $P
    $! v
  $6($O,$C,$P,TypeError):
   pass
 if dirn==1:
  $! lim_side(f,x,$d(a,TV),a)
 if dirn==-1:
  $! lim_side(f,x,$c(a,TV),a)
 r=lim_side(f,x,$d(a,TV),a)
 l=lim_side(f,x,$c(a,TV),a)
 if r==l:
  $! r
 if $((r,'limit')or $((l,'limit'):
  $!('limit',f,x,a)
 try:
  if $7(r)$+ $7(l)$+ $- has(r,'$[')$+ $- has(l,'$['):
   if $J($V(r)-$V(l))<1e-12:
    $! r
 $6 $>:
  pass
 $! '$M'
$, has_disc(f):
 if $/(f)is $- $3 or f[0]=='Q':
  $! $2
 if f[0]in('floor','ceiling','sign','ipart','round','fpart','$t','when','$J','mod'):
  $! $A
 $) a in f[1:]:
  if has_disc(a):
   $! $A
 $! $2
$, lim_side(f,x,sub_,a):
 g=$Y(f,x,sub_)
 try:
  r=lead_t(g)
  if r is $#:
   $! 0
  al,c=r
  if has(c,TV):
   $n $i()
  if ncmp(al,0)>0:
   $! 0
  if has(c,LNT):
   v=lnt_sign(c)
   if $/(v)is $1:
    $! '$M'
   if v==0:
    $n $i()
   $! '$[' if v>0 $&('*',-1,'$[')
  if al==0:
   $! c
  if $- $7(c):
   $! $:(c,'$[')
  v=$V(c)
  if $/(v)is $1:
   $! '$M'
  $! '$[' if v>0 $&('*',-1,'$[')
 $6($i,$O,$C,$P,TypeError,$W):
  pass
 r=lim_lh(g,0)
 if r is $- $#:
  $! r
 $! lim_num(g,a)
$, lim_val(g,$@):
 try:
  r=lead_t(g)
  if r is $#:
   $! 0
  al,c=r
  if has(c,TV):
   $n $i()
  if ncmp(al,0)>0:
   $! 0
  if has(c,LNT):
   v=lnt_sign(c)
   $! '$[' if v>0 $&('*',-1,'$[')
  if al==0:
   $! c
  v=$V(c)
  $! '$[' if v>0 $&('*',-1,'$[')
 $6($i,$O,$C,$P,TypeError,$W):
  pass
 $! lim_lh(g,$@+1)
''')
_x(r'''$, lim_lh(g,$@):
 if $@>4:
  $! $#
 if $9(g,TV):
  $! g
 h=head(g)
 if h=='^' $+ $- $9(g[2],TV):
  L=lim_val($:(g[2],fn('ln',g[1])),$@)
  if L is $#:
   $! $#
  $! pw('e',L)
 if h=='^' $+ $D(g[2]):
  L=lim_val(g[1],$@)
  if L is $#:
   $! $#
  if L==0 $+ $b(g[2])<0:
   $! '$['
  $! pw(L,g[2])
 if h=='*':
  nu,de=numer_denom(g)
  if de!=1:
   ln_=lim_val(nu,$@)
   ld=lim_val(de,$@)
   if ln_ is $# or ld is $#:
    $! $#
   if(ln_==0 $+ ld==0)or(isinfv(ln_)$+ isinfv(ld)):
    $! lim_val($.($Z(diff(nu,TV),diff(de,TV))),$@)
   if ld==0:
    s=$V($Y(de,TV,1e-9))
    sn=$V(ln_)if $7(ln_)$+ $- isinfv(ln_)$&(1 if ln_=='$[' $&-1)
    $! '$[' if(s.$S if $/(s)is $1 $& s)*(sn.$S if $/(sn)is $1 $& sn)>0 $&('*',-1,'$[')
   $! $Z(ln_,ld)
  ls=[lim_val(fct,$@)$) fct in g[1:]]
  if $# in ls:
   $! $#
  zero=[i $) i in $*($0(ls))if ls[i]==0]
  infs=[i $) i in $*($0(ls))if isinfv(ls[i])]
  if zero $+ infs:
   i=zero[0]
   j=infs[0]
   $`=$H([g[k+1]$) k in $*($0(ls))if k!=i $+ k!=j])
   q=$Z(g[i+1],pw(g[j+1],-1))
   r=lim_val(q,$@)
   if r is $#:
    $! $#
   $! $:(r,lim_val($`,$@))
  $! $H(ls)
 if h=='+':
  ls=[lim_val(t,$@)$) t in g[1:]]
  if $# in ls:
   $! $#
  r=$8(ls)
  if r!='$M':
   $! r
  ii=[k $) k in $*($0(ls))if isinfv(ls[k])]
  if $- ii:
   $! $#
  i=ii[0]
  A=g[i+1]
  $`=$8([g[k+1]$) k in $*($0(ls))if k!=i])
  q=lim_val($.($Z($`,A)),$@)
  if q is $# or q=='$M':
   $! $#
  $! $:(ls[i],$d(1,q))if q!=-1 $& $#
 if $/(g)is $3 $+ $0(g)==2:
  L=lim_val(g[1],$@)
  if L is $#:
   $! $#
  $! fn(h,L)
 $! $#
$, isinfv(v):
 $! v=='$[' or v==('*',-1,'$[')
$, lim_num(g,a):
 try:
  $g=[]
  $) k in $*(4,9):
   t=10.0**(-k)
   $g.$%($V(g,{TV:t}))
  v1=$g[-1]
  v2=$g[-2]
  if $/(v1)is $1 or $/(v2)is $1:
   $!('limit',g)
  if $J(v1)>1e12 $+ $J(v1)>$J(v2):
   $! '$[' if v1>0 $&('*',-1,'$[')
  if $J(v1-v2)<1e-6*(1+$J(v1)):
   $! exactify_guess(v1)
 $6 $>:
  pass
 $!('limit',g)
$, exactify_guess(v):
 r=float2rat(v,1e-9)
 n,d=nd(r)
 if d<1000:
  $! r
 $! v
$, series_at(f,x,a,order):
 if a=='$[' or a==('*',-1,'$['):
  sub_=pw(TV,-1)if a=='$[' $& $r(pw(TV,-1))
  back=pw(x,-1)if a=='$[' $& $r(pw(x,-1))
 $&:
  sub_=$d(a,TV)
  back=$c(x,a)
 g=$Y(f,x,sub_)
 S=series_t(g,order)
 $! S,back
$, taylor(f,x,n,a=0):
 try:
  S,back=series_at(f,x,a,n)
 $6($i,$O,$C,$P):
  $! taylor_d(f,x,n,a)
 $Q=[]
 $) k in S[0]:
  if ncmp(k,n)>0:
   $4
  if $-($/(k)is $t $+ k>=0)or has(S[0][k],LNT):
   $!('taylor',f,x,n,a)
  $Q.$%($:(S[0][k],pw(back,k)))
 $! $8($Q)
$, taylor_d(f,x,n,a):
 $Q=[]
 g=f
 fact=1
 $) k in $*(n+1):
  if k:
   fact*=k
   g=diff(g,x)
  v=$Y(g,x,a)
  if has(v,'$M')or v=='$M' or has(v,'$['):
   $!('taylor',f,x,n,a)
  $Q.$%($:($Z(v,fact),pw($c(x,a),k)))
 $! $8($Q)
$, series_cmd(f,x,n,a=0):
 try:
  S,back=series_at(f,x,a,n)
 $6($i,$O,$C,$P):
  $!('series',f,x,n,a)
 $Q=[]
 lnback=fn('ln',back)if $-(a=='$[' or a==('*',-1,'$['))$& $r(fn('ln',fn('$J',x)))
 $) k in S[0]:
  if ncmp(k,n)>0:
   $4
  c=$Y(S[0][k],LNT,lnback)
  $Q.$%($:(c,pw(back,k)))
 $! $8($Q)
$, dominant(f,x,a=0):
 if a=='$[' or a==('*',-1,'$['):
  sub_=pw(TV,-1)if a=='$[' $& $r(pw(TV,-1))
  back=pw(x,-1)if a=='$[' $& $r(pw(x,-1))
  lnback=$r(fn('ln',fn('$J',x)))
 $&:
  sub_=$d(a,TV)
  back=$c(x,a)
  lnback=fn('ln',back)
 try:
  r=lead_t($Y(f,x,sub_))
 $6($i,$O,$C,$P):
  $!('dominantterm',f,x,a)
 if r is $#:
  $! 0
 k,c=r
 $! $:($Y(c,LNT,lnback),pw(back,k))
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
 $Q=[]
 $) i in $*(j+1):
  $Q.$%($:(binom(j+1,i),B[i],pw(n,j+1-i)))
 $! $:(Q(1,j+1),$8($Q))
ZETA={2:('Q',1,6),4:('Q',1,90),6:('Q',1,945),8:('Q',1,9450),10:('Q',1,93555)}
''')
_x(r'''$, sumseq(f,k,a,b):
 if $k(a)$+ $k(b):
  if b<a-1:
   $! $r(sumseq(f,k,b+1,a-1))
  if b-a<=300:
   $Q=[$Y(f,k,j)$) j in $*(a,b+1)]
   $! $8($Q)
 if $9(f,k):
  $! $:(f,$d($c(b,a),1))
 cs_=$_(f,k)
 if cs_ is $- $# $+ b!='$[':
  res=[]
  $) j in $*($0(cs_)):
   if cs_[j]!=0:
    if j==0:
     res.$%($:(cs_[0],$d($c(b,a),1)))
    $&:
     res.$%($:(cs_[j],$c(powsum(j,b),powsum(j,$c(a,1)))))
  $! $=($8(res))
 r=geomsum(f,k,a,b)
 if r is $- $#:
  $! r
 r=telesum(f,k,a,b)
 if r is $- $#:
  $! r
 if b=='$[' $+ $k(a)$+ has(f,('fact',k)):
  g=$:(f,('fact',k))
  gs=geomsum(g,k,0,'$[')if $2 $& $#
  cr=expsum(g,k)
  if cr is $- $#:
   C,r=cr
   tot=$:(C,pw('e',r))
   if a>0:
    tot=$c(tot,$8([$:(C,$Z(pw(r,j),fact_(j)))$) j in $*(a)]))
   $! tot
 if b=='$[' $+ $k(a):
  nu,de=numer_denom(f)
  if $9(nu,k):
   dd=$_(de,k)
   if dd is $- $# $+ $0(dd)>=2 $+ all([c==0 $) c in dd[:-1]]):
    p=$0(dd)-1
    if p==1:
     $! '$[' if $V($Z(nu,dd[-1])).$S>0 $&('*',-1,'$[')
    if p in ZETA $+ a>=1:
     z=$:(ZETA[p],pw('pi',p))
     z=$c(z,$8([pw(j,-p)$) j in $*(1,a)]))
     $! $:($Z(nu,dd[-1]),z)
 if($k(a)or $7(a))$+(b=='$[' or $k(b))$+ freeofall(f,[s $) s in $l(f)if s!=k]):
  $! nsum(f,k,a,b)
 $!('sumseq',f,k,a,b)
$, expsum(g,k):
 if $9(g,k):
  $! g,1
 fs=g[1:]if $((g,'*')$&(g,)
 C=[]
 r=$#
 $) h in fs:
  if $9(h,k):
   C.$%(h)
  $? $((h,'^')$+ $9(h[1],k)$+ h[2]==k $+ r is $#:
   r=h[1]
  $? $((h,'^')$+ $9(h[1],k)$+ $h(h[2],k)$+ $h(h[2],k)[1]==0 $+ r is $#:
   r=pw(h[1],$h(h[2],k)[0])
  $&:
   $! $#
 if r is $#:
  $! $#
 $! $H(C),r
$, geomsum(f,k,a,b):
 fs=f[1:]if $((f,'*')$&(f,)
 C=[]
 base=$#
 ex=$#
 $) g in fs:
  if $9(g,k):
   C.$%(g)
  $? $((g,'^')$+ $9(g[1],k)$+ $h(g[2],k):
   if base is $- $#:
    if g[1]==base or($D(g[1])$+ $D(base)):
     lp=$h(g[2],k)
     lb=$h(ex,k)
     if lp[0]==1 $+ lb[0]==1:
      C.$%(pw(g[1],lp[1]))
      C.$%(pw(base,lb[1]))
      base=$:(base,g[1])
      ex=k
      $4
    $! $#
   base=g[1]
   ex=g[2]
  $&:
   $! $#
 if base is $#:
  $! $#
 p,q=$h(ex,k)
 r=pw(base,p)
 Cq=$:($H(C),pw(base,q))
 if b=='$[':
  if $7(r):
   v=$V(r)
   if $J(v)<1:
    $! $Z($:(Cq,pw(r,a)),$c(1,r))
   $! '$[' if $V(Cq).$S>0 $+ v.$S>0 $& '$M'
  $! $#
 if r==1:
  $! $:(Cq,$d($c(b,a),1))
 $! $Z($:(Cq,$c(pw(r,$d(b,1)),pw(r,a))),$c(r,1))
$, telesum(f,k,a,b):
 if $- hasdenom(f):
  $! $#
 pf=partfrac(f,k)
 if pf is $#:
  $! $#
 $Q=pf[1:]if $((pf,'+')$&(pf,)
 groups=[]
 $) t in $Q:
  c,r=$X(t)
  if $((r,'^')$+ r[2]==-1:
   lb=$h(r[1],k)
   if lb is $# or lb[0]!=1:
    $! $#
   groups.$%((c,lb[1]))
  $? $9(t,k):
   $! $#
  $&:
   $! $#
 if $- groups:
  $! $#
 s0=groups[0][1]
 tot=0
 ms=[]
 $) c,s in groups:
  m=nsub(s,s0)if $q(s)$+ $q(s0)$& $#
  if m is $# or $- $k(m):
   $! $#
  ms.$%(m)
  tot=$d(tot,c)
 if tot!=0:
  if b=='$[':
   $! '$['
  $! $#
 mn=min(ms)
 if mn!=0:
  s0=nadd(s0,mn)
  ms=[m-mn $) m in ms]
 M=max(ms)
 res=[]
 $) idx in $*($0(groups)):
  c=groups[idx][0]
  m=ms[idx]
  part=[]
  $) j in $*(m,M):
   part.$%(pw($d(a,j,s0),-1))
  if b!='$[':
   $) j in $*(1,m+1):
    part.$%(pw($d(b,j,s0),-1))
  res.$%($:(c,$8(part)))
 $! $8(res)
$, nsum(f,k,a,b):
 av=$t(nreal(a))
 if b=='$[':
  s=0.0
  prev=$#
  n=av
  chk=0
  $G n<av+200000:
   v=$V(f,{k:$F(n)})
   s+=v
   n+=1
   if n-av>50 $+ $J(v)<1e-15*(1+$J(s)):
    chk+=1
    if chk>20:
     $R
   $&:
    chk=0
  $! s
 s=0.0
 $) n in $*(av,$t(b)+1):
  s+=$V(f,{k:$F(n)})
 $! s
$, prodseq(f,k,a,b):
 if $k(a)$+ $k(b):
  if b<a-1:
   $! pw(prodseq(f,k,b+1,a-1),-1)
  if b-a<=300:
   $! $H([$Y(f,k,j)$) j in $*(a,b+1)])
 if $9(f,k):
  $! pw(f,$d($c(b,a),1))
 if f==k $+ a==1:
  $! fn('fact',b)
 if $((f,'^')$+ f[1]==k $+ $k(f[2])$+ a==1:
  $! pw(fn('fact',b),f[2])
 if $((f,'*')$+ a==1:
  c=[g $) g in f[1:]if $9(g,k)]
  r=[g $) g in f[1:]if $- $9(g,k)]
  if c $+ $0(r)==1:
   rr=prodseq(r[0],k,a,b)
   if $- $((rr,'prodseq'):
    $! $:(pw($H(c),b),rr)
 fs=f[1:]if $((f,'*')$&(f,)
 if $((f,'^')$+ $9(f[1],k):
  $! pw(f[1],sumseq(f[2],k,a,b))
 $!('prodseq',f,k,a,b)
$, texpand(e):
 if $/(e)is $- $3 or e[0]=='Q':
  $! e
 $N=[texpand(a)$) a in e[1:]]
 e=simp((e[0],)+$3($N))
 if $/(e)is $- $3:
  $! e
 h=e[0]
 if h in('sin','cos','tan')$+ $0(e)==2:
  u=e[1]
  if h=='tan':
   $! texpand($Z(fn('sin',u),fn('cos',u)))
  if $((u,'+'):
   a=u[1]
   b=$8($I(u[2:]))
   sa,ca=texpand(fn('sin',a)),texpand(fn('cos',a))
   sb,cb=texpand(fn('sin',b)),texpand(fn('cos',b))
   if h=='sin':
    $! $=($d($:(sa,cb),$:(ca,sb)))
   $! $=($c($:(ca,cb),$:(sa,sb)))
  c,r=$X(u)
  if $k(c)$+ c>1 $+ c<=30:
   s1=texpand(fn('sin',r))
   c1=texpand(fn('cos',r))
   z=expand_pow($d(c1,$:('i',s1)),c)
   re_,im_=reim(z)
   $! $=(im_ if h=='sin' $& re_)
 $! e
$, trigfactor(f):
 if head(f)in('sin','cos')$+ $0(f)==2:
  $![(f[0],f[1])]
 if $((f,'^')$+ head(f[1])in('sin','cos')$+ $k(f[2])$+ f[2]>0:
  $![(f[1][0],f[1][1])]*f[2]
 $! $#
''')
_x(r'''$, tmul(a,b):
 n1,u=a
 n2,v=b
 if n1=='sin' $+ n2=='sin':
  $! $:(HALF,$c(fn('cos',$c(u,v)),fn('cos',$d(u,v))))
 if n1=='cos' $+ n2=='cos':
  $! $:(HALF,$d(fn('cos',$c(u,v)),fn('cos',$d(u,v))))
 if n1=='cos':
  u,v=v,u
 $! $:(HALF,$d(fn('sin',$d(u,v)),fn('sin',$c(u,v))))
$, tcollect(e):
 if $/(e)is $- $3 or e[0]=='Q':
  $! e
 e=$=(e)
 if $((e,'+'):
  $! $8([tcollect_term(t)$) t in e[1:]])
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
   trig.${(tf)
 if $0(trig)<=1:
  $! t
 acc=fn(trig[0][0],trig[0][1])
 $) tf in trig[1:]:
  $Q=acc[1:]if $((acc,'+')$&(acc,)
  $<=[]
  $) term in $Q:
   c,r=$X(term)
   ftf=trigfactor(r)
   if ftf is $# or $0(ftf)!=1:
    if freeof_trig(r):
     $<.$%($:(term,fn(tf[0],tf[1])))
     $4
    $<.$%($:(term,fn(tf[0],tf[1])))
    $4
   $<.$%($:(c,tmul(ftf[0],tf)))
  acc=$=($8($<))
 $! $=($:($H(other),acc))
$, trigargs(e,$<):
 if $/(e)is $- $3 or e[0]=='Q':
  $!
 if e[0]in('sin','cos')$+ $0(e)==2:
  if e[1]$- in $<:
   $<.$%(e[1])
 $) a in e[1:]:
  trigargs(a,$<)
$, pyth(e):
 us=[]
 trigargs(e,us)
 if $- us:
  $! e
 best=e
 bl=$0(fmt(e))
 $) u in us:
  s=fn('sin',u)
  c=fn('cos',u)
  $) a,b in((s,c),(c,s)):
   g=rsquare(e,a,b)
   if g is $- $#:
    g=$=(g)
    l=$0(fmt(g))
    if l<bl:
     best=g
     bl=l
 $! best
$, rsquare(e,a,b):
 if $/(e)is $- $3 or e[0]=='Q':
  $! e
 if e[0]=='^' $+ e[1]==a $+ $k(e[2])$+ e[2]>=2:
  $! $:(pw(a,e[2]-2),$c(1,pw(b,2)))
 $! simp((e[0],)+$3(rsquare(t,a,b)$) t in e[1:]))
$, freeof_trig(e):
 $! $- hastrig(e)
$, arclen(f,x,a,b):
 g=$.($=($d(1,pw(diff(f,x),2))))
 $! defint($L(g),x,a,b)
$, tangentline(f,x,a):
 d=$Y(diff(f,x),x,a)
 $! $=($d($Y(f,x,a),$:(d,$c(x,a))))
$, normalline(f,x,a):
 d=$Y(diff(f,x),x,a)
 if d==0:
  $!('=',x,a)
 $! $=($c($Y(f,x,a),$Z($c(x,a),d)))
$, impdif(eq,x,y,n=1):
 F=$c(eq[1],eq[2])if $((eq,'=')$& eq
 yp=$.($r($Z(diff(F,x),diff(F,y))))
 d=yp
 $) _ in $*(n-1):
  d=$.($d(diff(d,x),$:(diff(d,y),yp)))
 $! nice(d)
$, avgrc(f,x,v,h=Q(1,1000)):
 $! $Z($c($Y(f,x,$d(v,h)),$Y(f,x,v)),h)
$, centraldiff(f,x,v,h=Q(1,1000)):
 $! $Z($c($Y(f,x,$d(v,h)),$Y(f,x,$c(v,h))),$:(2,h))
$, untan(e):
 if $/(e)is $- $3 or e[0]=='Q':
  $! e
 $N=[untan(a)$) a in e[1:]]
 if e[0]=='tan' $+ $0($N)==1:
  $! $Z(fn('sin',$N[0]),fn('cos',$N[0]))
 $! simp((e[0],)+$3($N))
$, pyth_to(e,which):
 other='cos' if which=='sin' $& 'sin'
 e=untan(e)
 us=[]
 trigargs(e,us)
 $) u in us:
  e=rsquare(e,fn(other,u),fn(which,u))
 $! $=(e)
''')
_x(r'''$, unhold(e):
 if $((e,'hold'):
  $! simp(e[1])
 $! e
$, $}(e):
 if $- $7(e):
  $! $2
 try:
  v=$V(e)
 $6 $>:
  $! $2
 if $/(v)is $1:
  $! $J(v.imag)<=1e-10*(1+$J(v.$S))
 $! v==v
$, fv(e):
 v=$V(e)
 if $/(v)is $1:
  $! v.$S
 $! v
$, clean(e):
 e=$.(e)
 if $a(e):
  e=evalf(e)
  if has(e,'i'):
   r,i=reim(e)
   if $/(i)is $F $+ $J(i)<1e-11*(1+$J(tofl(r)if $D(r)$& 1)):
    e=r
 $! e
class Sols:
 $, __init__($;):
  $;.$g=[]
  $;.all=$2
  $;.fail=$2
  $;.ints=[]
$, $|(f,x,$E=$2,$@=0):
 if $@>6:
  $! $#
 f=$.(unhold(f))
 if $9(f,x):
  if f==0:
   $! 'all'
  if $7(f)or $- $E:
   $![]
  $![]
 nu=numer_of(f)
 if $9(nu,x):
  $![]if nu!=0 $& 'all'
 $f=solve_num(nu,x,$E,$@)
 if $f is $# or $f=='all':
  $! $f
 $<=[]
 $) s in $f:
  if valid(f,x,s,$E):
   $<.$%(s)
 $! $<
$, numer_of(f):
 try:
  c=comdenom(f)
 $6 $>:
  c=f
 $! numer_denom(c)[0]
$, valid(f,x,s,$E):
 if has(s,'n1')or $l(s)$+ $- $7(s):
  $! $A
 try:
  v=$Y(f,x,s)
  if v=='$M' or has(v,'$M'):
   $! $2
  if has(v,'$['):
   $! $2
  vv=$V(v)
  mag=1.0
  if $/(vv)is $1:
   ok=$J(vv)<1e-6
  $&:
   ok=$J(vv)<1e-6
  if $- ok:
   try:
    sc=$V(s)
    ok=$J(vv)<1e-8*(1+$J(sc))*1e4
   $6 $>:
    ok=$2
  if $- $E:
   sv=$V(s)
   if $/(sv)is $1 $+ $J(sv.imag)>1e-9*(1+$J(sv.$S)):
    $! $2
  $! ok
 $6($O,$C,$P,TypeError,$W):
  $! $2
$, solve_num(nu,x,$E,$@):
 d=degree(nu,x)
 if d is $- $#:
  r=solve_poly(nu,x,$E)
  if r is $- $#:
   $! r
 fac=$z(nu)
 fac=fac[1]if $((fac,'hold')$& fac
 if $((fac,'*'):
  allsol=[]
  $) g in fac[1:]:
   if $((g,'^')$+ $D(g[2])$+ $b(g[2])>0:
    g=g[1]
   if $9(g,x):
    $4
   r=$|(g,x,$E,$@+1)
   if r is $#:
    $! numeric_solve(nu,x,$E)
   if r=='all':
    $! 'all'
   allsol.${(r)
  $! dedup(allsol)
 if $((fac,'^')$+ $D(fac[2])$+ $b(fac[2])>0:
  $! $|(fac[1],x,$E,$@+1)
 r=isolate(nu,0,x,$E,$@)
 if r is $- $#:
  $! r
 r=radical_solve(nu,x,$E,$@)
 if r is $- $#:
  $! r
 r=explog_solve(nu,x,$E,$@)
 if r is $- $#:
  $! r
 r=ln_solve(nu,x,$E,$@)
 if r is $- $#:
  $! r
 r=kernel_solve(nu,x,$E,$@)
 if r is $- $#:
  $! r
 if hastrigx(nu,x):
  g=texpand(nu)
  if g!=nu:
   r=kernel_solve(g,x,$E,$@+1)
   if r is $#:
    fg=$z(g)
    fg=fg[1]if $((fg,'hold')$& fg
    if $((fg,'*'):
     $! solve_num(g,x,$E,$@+1)
   if r is $- $#:
    $! r
  r=trig_lin(nu,x,$E)
  if r is $- $#:
   $! r
 $! numeric_solve(nu,x,$E)
$, radical_solve(nu,x,$E,$@):
 ks=[]
 xkernels(nu,x,ks)
 if $- ks:
  $! $#
 $) k in ks:
  if $-($((k,'^')$+ isq(k[2])$+ k[2][1]==1):
   $! $#
 if $0(ks)>1:
  if $@>4 or $0(ks)>3:
   $! $#
  $) k in ks:
   if k[2]!=HALF:
    $! $#
  k=ks[0]
  W='W_'
  g=$=($Y(nu,k,W))
  cs_=$_(g,W)
  if cs_ is $# or $0(cs_)!=2:
   $! $#
  A,B=cs_
  g2=$=($c(pw(A,2),$:(pw(B,2),k[1])))
  rs=$|(g2,x,$E,$@+1)
  if rs is $# or rs=='all':
   $! $#
  $![r $) r in rs if valid(nu,x,r,$E)]
 k=ks[0]
 base=k[1]
 q=k[2][2]
 W='W_'
 g=$=($Y(nu,k,W))
 cs_=$_(g,W)
 if cs_ is $# or $0(cs_)!=2 or has(cs_[0],W):
  $! $#
 A,B=cs_
 if degree(A,x)is $# or degree(B,x)is $# or degree(base,x)is $#:
  $! $#
 poly=$=($c(pw($r(A),q),$:(pw(B,q),base)))
 rs=solve_poly(poly,x,$E)
 if rs is $# or rs=='all':
  $! $#
 $<=[]
 $) r in rs:
  if valid(nu,x,r,$E):
   $<.$%(r)
 $! $<
$, expterm(t,x):
 fs=t[1:]if $((t,'*')$&(t,)
 c=[]
 L=[]
 $) f in fs:
  if $9(f,x):
   c.$%(f)
  $? $((f,'^')$+ $9(f[1],x)$+ $h(f[2],x)is $- $# $+ $}(f[1])$+ fv(f[1])>0:
   L.$%($:(f[2],fn('ln',f[1]))if f[1]!='e' $& f[2])
  $&:
   $! $#
 $! $H(c),$8(L)
$, explog_solve(nu,x,$E,$@):
 if $- $((nu,'+'):
  $! $#
 dep=[t $) t in nu[1:]if $- $9(t,x)]
 ind=$8([t $) t in nu[1:]if $9(t,x)])
 if $0(dep)==2 $+ ind==0:
  A=expterm(dep[0],x)
  B=expterm(dep[1],x)
  if A is $# or B is $#:
   $! $#
  r=$.($r($Z(B[0],A[0])))
  if $}(r)$+ fv(r)<=0 $+ $- $E:
   $![]
  eq=$=($c(A[1],$d(B[1],fn('ln',r))))
  lx=$h(eq,x)
  if lx is $#:
   $! $#
  $![nice($.($r($Z(lx[1],lx[0]))))]
 $! $#
$, ln_solve(nu,x,$E,$@):
 $Q=nu[1:]if $((nu,'+')$&(nu,)
 lns=[]
 $`=[]
 $) t in $Q:
  c,r=$X(t)
  if $((r,'log')$+ $0(r)==3:
   c=$Z(c,fn('ln',r[2]))
   r=('ln',r[1])
  if $((r,'ln')$+ $q(c)$+ $- $9(r,x):
   lns.$%((c,r[1]))
  $? $9(t,x):
   $`.$%(t)
  $? $((r,'ln')$+ $7(c)$+ $- $9(r,x):
   lns.$%((c,r[1]))
  $&:
   $! $#
 if $0(lns)<2 $+ $-($0(lns)==1 $+ $`):
  $! $#
 k=rest_k=$8($`)
 c0=lns[0][0]
 if all([c==c0 $) c,u in lns]):
  P=$H([u $) c,u in lns])
  rhs=pw('e',$.($r($Z(rest_k,c0))))
 $? all([$q(c)$) c,u in lns]):
  P=$H([pw(u,c)$) c,u in lns])
  rhs=pw('e',$r(rest_k))
 $&:
  $! $#
 rs=$|($c(P,rhs),x,$E,$@+1)
 if rs is $# or rs=='all':
  $! rs
 $<=[]
 $) r in rs:
  if valid(nu,x,r,$E):
   $<.$%(r)
 $! $<
$, hastrigx(e,x):
 if $/(e)is $- $3 or e[0]=='Q':
  $! $2
 if e[0]in('sin','cos','tan')$+ has(e,x):
  $! $A
 $) a in e[1:]:
  if hastrigx(a,x):
   $! $A
 $! $2
''')
_x(r'''$, dedup($f):
 $<=[]
 $) s in $f:
  if s $- in $<:
   dup=$2
   $) t in $<:
    try:
     if $7(s)$+ $7(t)$+ $J($V(s)-$V(t))<1e-12*(1+$J($V(s))):
      dup=$A
      $R
    $6 $>:
     pass
   if $- dup:
    $<.$%(s)
 $! $<
$, sortsols($f):
 $, key(s):
  t=s
  $) w in $l(s):
   if w[0]=='n' $+ w[1:].isdigit():
    t=$Y(t,w,0)
  try:
   v=$V(t)
   if $/(v)is $1:
    $!(1,v.$S,v.imag,okey(s))
   $!(0,v,0.0,okey(s))
  $6 $>:
   $!(2,0.0,0.0,okey(s))
 $! sorted($f,key=key)
$, solve_poly(p,x,$E):
 cs=$_(p,x)
 if cs is $#:
  $! $#
 $G cs $+ cs[-1]==0:
  cs.pop()
 n=$0(cs)-1
 if n<=0:
  $![]if cs $+ cs[0]!=0 $& 'all'
 $f=[]
 k=0
 $G cs[k]==0:
  k+=1
 if k:
  $f.$%(0)
  cs=cs[k:]
  n=$0(cs)-1
 if n==0:
  $! $f
 allrat=$A
 anyfl=$2
 $) c in cs:
  if $- $q(c):
   allrat=$2
  if $a(c):
   anyfl=$A
 if anyfl $+ all([$7(c)$) c in cs]):
  $! $f+numroots(cs,$E)
 if allrat:
  cc,fs=ufactor(cs)
  $) g,m in fs:
   $f.${(solve_small(g,x,$E))
  $! dedup($f)
 if n==1:
  $! $f+[$.($r($Z(cs[0],cs[1])))]
 if n==2:
  $! $f+quad(cs[2],cs[1],cs[0],$E)
 fac=$z(p,x)
 fac=fac[1]if $((fac,'hold')$& fac
 if $((fac,'*'):
  $) g in fac[1:]:
   if $((g,'^')$+ $D(g[2]):
    g=g[1]
   if $9(g,x):
    $4
   dg=degree(g,x)
   if dg is $- $# $+ dg<n:
    r=solve_poly(g,x,$E)
    if r is $#:
     $! $#
    $f.${(r)
   $&:
    $! $#
  $! dedup($f)
 r=solve_binom(cs,x,$E)
 if r is $- $#:
  $! $f+r
 if all([$7(c)$) c in cs]):
  $! $f+numroots(cs,$E)
 $! $#
$, quad(a,b,c,$E):
 D=$.($=($c($:(b,b),$:(4,a,c))))
 if $}(D)$+ $- $E:
  if fv(D)<0:
   $![]
 if D==0:
  $![$.($Z($r(b),$:(2,a)))]
 s=$L(D)
 r1=$.($Z($c($r(b),s),$:(2,a)))
 r2=$.($Z($d($r(b),s),$:(2,a)))
 if $7(r1):
  r1=$=(r1)
  r2=$=(r2)
 $![r1,r2]
$, solve_small(g,x,$E):
 n=$0(g)-1
 if n==1:
  $![Q(-g[0],g[1])]
 if n==2:
  $! quad(g[2],g[1],g[0],$E)
 r=solve_binom(g,x,$E)
 if r is $- $#:
  $! r
 if n==3:
  r=cardano(g,$E)
  if r is $- $#:
   if $0(fmt(r[0]))<=32:
    $! r
 $! numroots(g,$E)
$, solve_binom(cs,x,$E):
 n=$0(cs)-1
 m=0
 $) i in $*(1,n+1):
  if cs[i]!=0:
   m=igcd(m,i)
 if m<=1:
  $! $#
 sub_cs=[cs[i]$) i in $*(0,n+1,m)]
 if $0(sub_cs)-1>2 $+ $-($0([c $) c in sub_cs if c!=0])==2):
  $! $#
 u='U_'
 if $0(sub_cs)==2:
  roots_u=[$.($r($Z(sub_cs[0],sub_cs[1])))]
 $&:
  roots_u=solve_poly(fromcoeffs(sub_cs,u),u,$E)
  if roots_u is $#:
   $! $#
 $<=[]
 $) r in roots_u:
  $<.${(nthroots(r,m,$E))
 $! dedup($<)
$, nthroots(r,m,$E):
 if $- $E:
  if $}(r):
   v=fv(r)
   if m%2==1:
    if v<0:
     $![$r(pw($r(r),Q(1,m)))]
    $![pw(r,Q(1,m))]
   if v<0:
    $![]
   if v==0:
    $![0]
   rt=pw(r,Q(1,m))
   $![$r(rt),rt]
  if m%2==1:
   $![pw(r,Q(1,m))]
  rt=pw(r,Q(1,m))
  $![$r(rt),rt]
 if $7(r):
  v=$V(r)
  mod=fn('$J',r)
  ang=fn('$s',r)
  $<=[]
  $) k in $*(m):
   th=$Z($d(ang,$:(2*k,'pi')),m)
   z=$:(pw(mod,Q(1,m)),$d(fn('cos',th),$:('i',fn('sin',th))))
   z=$=(z)
   $<.$%(z)
  $! $<
 rt=pw(r,Q(1,m))
 $![$:(rt,pw('e',$Z($:(2*k,'i','pi'),m)))$) k in $*(m)]
$, cardano(g,$E):
 d,c,b,a=[Q(v)if $/(v)is $t $& v $) v in g]
 p=$Z($c($:(3,a,c),$:(b,b)),$:(3,a,a))
 q=$Z($d($:(2,pw(b,3)),$:(-9,a,b,c),$:(27,a,a,d)),$:(27,pw(a,3)))
 disc=$d($Z(pw(q,2),4),$Z(pw(p,3),27))
 if $- $q(disc)or $b(disc)<=0:
  $! $#
 s=$L(disc)
 u=$d($r($Z(q,2)),s)
 v=$c($r($Z(q,2)),s)
 $, cbrt(w):
  wv=fv(w)
  if wv<0:
   $! $r(pw($r(w),Q(1,3)))
  $! pw(w,Q(1,3))
 t=$d(cbrt(u),cbrt(v))
 root=$c(t,$Z(b,$:(3,a)))
 if $- $E:
  $![root]
 $![root]+[clean(r)$) r in numroots_after(g,root)]
$, numroots_after(g,root):
 rv=fv(root)
 rs=aberth(g)
 $![fromcomplex(z)$) z in rs if $J(z-rv)>1e-6]
$, numroots(cs,$E):
 rs=aberth([evalf(c)if $- $D(c)$& c $) c in cs])
 $<=[]
 $) z in rs:
  if $J(z.imag)<1e-9*(1+$J(z.$S)):
   $<.$%($F(z.$S))
  $? $E:
   $<.$%(fromcomplex(z))
 $! $<
NC=[0]
$, newint():
 NC[0]+=1
 $! 'n'+$p(NC[0])
''')
_x(r'''$, isolate(lhs,rhs,x,$E,$@):
 if $@>12:
  $! $#
 if lhs==x:
  $![rhs]
 if $9(lhs,x):
  $! 'all' if $.($c(lhs,rhs))==0 $&[]
 h=head(lhs)
 if h=='+':
  dep=[t $) t in lhs[1:]if $- $9(t,x)]
  ind=[t $) t in lhs[1:]if $9(t,x)]
  if $0(dep)==1:
   $! isolate(dep[0],$c(rhs,$8(ind)),x,$E,$@+1)
  $! $#
 if h=='*':
  dep=[t $) t in lhs[1:]if $- $9(t,x)]
  ind=[t $) t in lhs[1:]if $9(t,x)]
  if $0(dep)==1:
   c=$H(ind)
   r=$Z(rhs,c)
   if $7(c)$+ $((rhs,'+'):
    r=$=(r)
   $! isolate(dep[0],r,x,$E,$@+1)
  $! $#
 if h=='^':
  b,p=lhs[1],lhs[2]
  if $9(p,x):
   if p==-1 or($D(p)$+ $b(p)<0):
    if rhs==0:
     $![]
    $! isolate(pw(b,nneg(p)),pw(rhs,-1),x,$E,$@+1)
   if $/(p)is $t:
    $<=[]
    $) r in nthroots(rhs,p,$E):
     rr=isolate(b,r,x,$E,$@+1)
     if rr is $#:
      $! $#
     if rr=='all':
      $! 'all'
     $<.${(rr)
    $! $<
   if isq(p):
    pn,pd=p[1],p[2]
    if pd%2==0 $+ $- $E $+ $}(rhs)$+ fv(rhs)<0:
     $![]
    $! isolate(pw(b,pn),pw(rhs,pd),x,$E,$@+1)
   $! isolate(b,pw(rhs,pw(p,-1)),x,$E,$@+1)
  if $9(b,x):
   if rhs==0:
    $![]
   if $- $E $+ $}(rhs)$+ fv(rhs)<0 $+ $}(b)$+ fv(b)>0:
    $![]
   if b=='e':
    $! isolate(p,fn('ln',rhs),x,$E,$@+1)
   if $D(b)$+ $7(rhs):
    $! isolate(p,fn('log',rhs,b),x,$E,$@+1)
   $! isolate(p,$Z(fn('ln',rhs),fn('ln',b)),x,$E,$@+1)
  $! $#
 if $/(lhs)is $3 $+ $0(lhs)>=2:
  u=lhs[1]
  if $- all([$9(a,x)$) a in lhs[2:]]):
   $! $#
  rs=invfun(h,lhs,rhs,$E)
  if rs is $#:
   $! $#
  $<=[]
  $) r in rs:
   rr=isolate(u,r,x,$E,$@+1)
   if rr is $#:
    $! $#
   if rr=='all':
    $! 'all'
   $<.${(rr)
  $! $<
 $! $#
$, invfun(h,lhs,r,$E):
 rv=$#
 if $}(r):
  rv=fv(r)
 if h=='ln':
  $![pw('e',r)]
 if h=='log':
  b=lhs[2]if $0(lhs)>2 $& 10
  $![pw(b,r)]
 if h=='$J':
  if rv is $- $#:
   if rv<0:
    $![]
   if rv==0:
    $![0]
  $![$r(r),r]
 if h=='$L':
  $![pw(r,2)]
 if h=='sin':
  if rv is $- $# $+ $J(rv)>1 $+ $- $E:
   $![]
  n=newint()
  if r==0:
   $![$:(n,'pi')]
  a=fn('$w',r)
  if r==1 or r==-1:
   $![$d(a,$:(2,n,'pi'))]
  $![$d(a,$:(2,n,'pi')),$d($c('pi',a),$:(2,n,'pi'))]
 if h=='cos':
  if rv is $- $# $+ $J(rv)>1 $+ $- $E:
   $![]
  n=newint()
  if r==0:
   $![$d($:(HALF,'pi'),$:(n,'pi'))]
  a=fn('arccos',r)
  if r==1 or r==-1:
   $![$d(a,$:(2,n,'pi'))]
  $![$d(a,$:(2,n,'pi')),$d($r(a),$:(2,n,'pi'))]
 if h=='tan':
  n=newint()
  $![$d(fn('$u',r),$:(n,'pi'))]
 if h=='$w':
  if rv is $- $# $+ $J(rv)>$U.pi/2+1e-12:
   $![]
  $![fn('sin',r)]
 if h=='arccos':
  if rv is $- $# $+(rv<-1e-12 or rv>$U.pi+1e-12):
   $![]
  $![fn('cos',r)]
 if h=='$u':
  if rv is $- $# $+ $J(rv)>=$U.pi/2:
   $![]
  $![fn('tan',r)]
 if h=='sinh':
  $![fn('arcsinh',r)]
 if h=='cosh':
  if rv is $- $# $+ rv<1:
   $![]
  a=fn('arccosh',r)
  $![$r(a),a]
 if h=='tanh':
  if rv is $- $# $+ $J(rv)>=1:
   $![]
  $![fn('arctanh',r)]
 if h=='arcsinh':
  $![fn('sinh',r)]
 if h=='arccosh':
  $![fn('cosh',r)]
 if h=='arctanh':
  $![fn('tanh',r)]
 $! $#
$, xkernels(e,x,$<):
 if $/(e)is $- $3 or e[0]=='Q' or $9(e,x):
  $!
 h=e[0]
 if h in('+','*'):
  $) a in e[1:]:
   xkernels(a,x,$<)
  $!
 if h=='^' $+ $/(e[2])is $t:
  xkernels(e[1],x,$<)
  $!
 if h=='^' $+ isq(e[2])$+ e[1]==x:
  k=pw(x,Q(1,e[2][2]))
  if k $- in $<:
   $<.$%(k)
  $!
 if e $- in $<:
  $<.$%(e)
$, kernel_solve(nu,x,$E,$@):
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
    if $9(g2,x):
     rs=$|(g2,W,$E,$@+1)
     if rs is $# or rs=='all':
      $! rs
     $<=[]
     $) r in rs:
      rr=isolate(pw(base,$:(gg,x)),r,x,$E,$@+1)
      if rr is $#:
       $! $#
      $<.${(rr)
     $! $<
 ks=[]
 xkernels(g,x,ks)
 if $0(ks)==1 $+ ks[0]!=x:
  k=ks[0]
  g2=$Y(g,k,W)
  if $9(g2,x):
   rs=$|(g2,W,$E,$@+1)
   if rs is $# or rs=='all':
    $! rs
   $<=[]
   $) r in rs:
    rr=isolate(k,r,x,$E,$@+1)
    if rr is $#:
     $! $#
    if rr=='all':
     $! 'all'
    $<.${(rr)
   $! $<
 if $0(ks)==2:
  names=sorted([head(k)$) k in ks])
  if names==['cos','sin']$+ ks[0][1]==ks[1][1]:
   u=ks[0][1]
   s=fn('sin',u)
   c=fn('cos',u)
   $) a,b in((c,s),(s,c)):
    g2=$=(g)
    cc=$_($Y(g2,a,W),W)
    if cc is $- $# $+ all([cc[i]==0 $) i in $*(1,$0(cc),2)]):
     g3=$=($Y($Y(g2,a,W),W,$L($c(1,pw(b,2)))))
     if $- has(g3,a):
      $! kernel_solve(g3,x,$E,$@+1)if $@<4 $& $#
 $! $#
$, rgcd(a,b):
 if $q(a)$+ $q(b):
  an,ad=nd(a)
  bn,bd=nd(b)
  $! Q(igcd(an,bn),ilcm(ad,bd))
 $! a if a==b $& 0
$, findexp(e,x,$<):
 if $/(e)is $- $3 or e[0]=='Q':
  $!
 if e[0]=='^' $+ $9(e[1],x)$+ $- $9(e[2],x):
  l=$h(e[2],x)
  if l is $- $#:
   $<.$%((e[1],l[0],l[1]))
   $!
  $<.$%(($#,0,0))
  $!
 $) a in e[1:]:
  findexp(a,x,$<)
$, repl_exp(e,x,base,gg,W):
 if $/(e)is $- $3 or e[0]=='Q':
  $! e
 if e[0]=='^' $+ e[1]==base $+ $- $9(e[2],x):
  l=$h(e[2],x)
  if l is $- $#:
   $! $:(pw(base,l[1]),pw(W,$Z(l[0],gg)))
 $! simp((e[0],)+$3(repl_exp(a,x,base,gg,W)$) a in e[1:]))
''')
_x(r'''$, trig_lin(nu,x,$E):
 ks=[]
 xkernels(nu,x,ks)
 if $0(ks)!=2:
  $! $#
 names=sorted([head(k)$) k in ks])
 if names!=['cos','sin']or ks[0][1]!=ks[1][1]:
  $! $#
 u=ks[0][1]
 S='S_'
 C='C_'
 g=$=($Y($Y(nu,fn('sin',u),S),fn('cos',u),C))
 if has(g,x):
  $! $#
 cs_s=$_(g,S)
 if cs_s is $# or $0(cs_s)!=2:
  $! $#
 a=cs_s[1]
 $`=cs_s[0]
 cc=$_($`,C)
 if cc is $# or $0(cc)!=2 or has(a,C):
  $! $#
 b=cc[1]
 c=cc[0]
 if c==0:
  $! isolate(fn('tan',u),$.($r($Z(b,a))),x,$E,0)
 R=$L($d(pw(a,2),pw(b,2)))
 phi=fn('$u',$Z(b,a))
 if $}(a)$+ fv(a)<0:
  phi=$d(phi,'pi')
 $! isolate(fn('sin',$d(u,phi)),$.($r($Z(c,R))),x,$E,0)
$, numeric_solve(f,x,$E,lo=$#,hi=$#,maxn=12):
 others=[s $) s in $l(f)if s!=x]
 if others:
  $! $#
 $, F(t):
  try:
   v=$V(f,{x:t})
  $6($C,$P,$W,$O,TypeError):
   $! $#
  if $/(v)is $1:
   if $J(v.imag)>1e-9*(1+$J(v.$S)):
    $! $#
   v=v.$S
  if v!=v:
   $! $#
  $! v
 pts=[]
 if lo is $- $# $+ hi is $- $#:
  N=400
  $) i in $*(N+1):
   pts.$%(lo+(hi-lo)*i/N)
 $&:
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
 $) k in $*($0(pts)):
  t=pts[k]
  v=vals0[k]
  if v is $- $# $+ v==0:
   a=vals0[k-1]if k>0 $& $#
   b=vals0[k+1]if k+1<$0(pts)$& $#
   if(a is $- $# $+ a!=0)or(b is $- $# $+ b!=0):
    roots.$%(t)
  $? v is $- $# $+ pv is $- $# $+ v!=0 $+ pv!=0 $+(v<0)!=(pv<0):
   r=bisect(F,prev,t,pv,v)
   if r is $- $#:
    roots.$%(r)
  prev=t
  pv=v
  if $0(roots)>40:
   $R
 $g=[(pts[k],vals0[k])$) k in $*($0(pts))]
 $) i in $*(1,$0($g)-1):
  t0,a=$g[i-1]
  t1,b=$g[i]
  t2,c=$g[i+1]
  if a is $# or b is $# or c is $#:
   $4
  if b!=0 $+ $J(b)<$J(a)$+ $J(b)<$J(c)$+(a>0)==(b>0)==(c>0)$+ $J(b)<1e-2:
   r=newton(F,t1)
   if r is $- $# $+ t0<=r<=t2:
    roots.$%(r)
 $<=[]
 $) r in sorted(roots):
  if $- $< or $J(r-$<[-1])>1e-9*(1+$J(r)):
   $<.$%(r)
 if $0($<)>maxn $+ lo is $#:
  $<=$<[:maxn]
 $![snap(r)$) r in $<]
$, snap(r):
 if $J(r-round(r))<1e-12:
  $! $F(round(r))
 $! r
$, bisect(F,a,b,fa,fb):
 $) _ in $*(200):
  m=0.5*(a+b)
  fm=F(m)
  if fm is $#:
   $! $#
  if fm==0 or $J(b-a)<1e-15*(1+$J(m)):
   $R
  if(fm<0)==(fa<0):
   a,fa=m,fm
  $&:
   b,fb=m,fm
 m=0.5*(a+b)
 fm=F(m)
 if fm is $# or $J(fm)>1e-6*(1+$J(fa)+$J(fb)):
  if fm is $- $# $+ $J(fm)>1e3:
   $! $#
 $! m
$, newton(F,t):
 $) _ in $*(60):
  v=F(t)
  if v is $#:
   $! $#
  h=1e-7*(1+$J(t))
  v2=F(t+h)
  if v2 is $#:
   $! $#
  d=(v2-v)/h
  if d==0:
   $R
  t2=t-v/d
  if $J(t2-t)<1e-14*(1+$J(t)):
   t=t2
   $R
  t=t2
 v=F(t)
 if v is $- $# $+ $J(v)<1e-9:
  $! t
 $! $#
$, nsolve(f,x,guess=$#,lo=$#,hi=$#):
 $, F(t):
  try:
   v=$V(f,{x:t})
  $6($C,$P,$W,$O,TypeError):
   $! $#
  if $/(v)is $1:
   if $J(v.imag)>1e-9*(1+$J(v.$S)):
    $! $#
   v=v.$S
  $! v
 if guess is $- $#:
  r=secant(F,guess,lo,hi)
  if r is $- $#:
   $! r
 if lo is $- $# $+ hi is $- $#:
  rs=numeric_solve(f,x,$2,lo,hi)
 $&:
  rs=numeric_solve(f,x,$2)
  if lo is $- $#:
   rs=[r $) r in rs if r>=lo]
  if hi is $- $#:
   rs=[r $) r in rs if r<=hi]
 if rs:
  if guess is $- $#:
   rs.sort(key=$5 r:$J(r-guess))
  $&:
   rs.sort(key=$5 r:$J(r))
  $! rs[0]
 $! $#
$, secant(F,g,lo,hi):
 t=g
 r=newton(F,t)
 if r is $- $# $+(lo is $# or r>=lo)$+(hi is $# or r<=hi):
  $! r
 $! $#
FLIP={'<':'>','>':'<','<=':'>=','>=':'<=','/=':'/='}
$, solve_ineq(rel,f,x):
 f=$.(f)
 if $- $7($Y(f,x,0))or $- $7(diff(f,x)):
  r=ineq_param(rel,f,x)
  if r is $- $#:
   $! r
 pts=[]
 rs=$|(f,x,$2)
 if rs is $#:
  $! $#
 if rs=='all':
  rs=[]
 $) r in rs:
  if $- $}(r):
   $! $#
  pts.$%(r)
 dens=[]
 domainpts(f,x,dens)
 $) d in dens:
  r2=$|(d,x,$2)
  if r2 is $# or r2=='all':
   $4
  $) r in r2:
   if $}(r):
    pts.$%(r)
   $&:
    $! $#
 pts=dedup(pts)
 pts=sortsols(pts)
 $, test(t):
  try:
   v=$V(f,{x:t})
  $6 $>:
   $! $2
  if $/(v)is $1:
   if $J(v.imag)>1e-9*(1+$J(v.$S)):
    $! $2
   v=v.$S
  if v!=v:
   $! $2
  $! relok(rel,v)
 $g=[fv(p)$) p in pts]
 segs=[]
 if $- $g:
  ok=test(0.5)
  $! 'true' if ok $& 'false'
 first=$g[0]-max(1.0,$J($g[0]))
 segs.$%(('I',$#,pts[0],test(first)))
 $) i in $*($0(pts)):
  p=pts[i]
  okp=$2
  try:
   v=$Y(f,x,p)
   if v!='$M' $+ $- has(v,'$M')$+ $- has(v,'$['):
    vv=$V(v)
    if $/(vv)is $1:
     vv=vv.$S if $J(vv.imag)<1e-9 $& $#
    if vv is $- $#:
     if $J(vv)<1e-10:
      vv=0.0
     okp=relok(rel,vv)
  $6 $>:
   okp=$2
  segs.$%(('P',p,p,okp))
  if i+1<$0(pts):
   m=0.5*($g[i]+$g[i+1])
   segs.$%(('I',p,pts[i+1],test(m)))
 last=$g[-1]+max(1.0,$J($g[-1]))
 segs.$%(('I',pts[-1],$#,test(last)))
 $! segs_to_bool(segs,x)
''')
_x(r'''$, sgn(e):
 if $7(e):
  try:
   v=fv(e)
  $6 $>:
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
  if all(k in(1,2)$) k in ks)$+ 1 in ks:
   $! 1
  ks=[sgn($r(a))or(2 if nonneg($r(a))$& 0)$) a in e[1:]]
  if all(k in(1,2)$) k in ks)$+ 1 in ks:
   $!-1
  $! 0
 if $((e,'^')$+ $k(e[2])$+ e[2]%2==1:
  $! sgn(e[1])
 if head(e)=='exp' or($((e,'^')$+ e[1]=='e'):
  $! 1
 $! 0
$, nonneg(e):
 if $((e,'^')$+ $k(e[2])$+ e[2]%2==0:
  $! $A
 if head(e)=='$J':
  $! $A
 if $((e,'*'):
  $! all(nonneg(a)or sgn(a)>0 $) a in e[1:])
 $! sgn(e)>0
$, ineq_param(rel,f,x):
 cs=$_(f,x)
 if cs is $# or $0(cs)!=2:
  $! $#
 a=nice(comdenom(cs[1]))
 b=cs[0]
 v=nice(comdenom($Z($r(b),a)))
 k=sgn(a)
 if k:
  $!(rel if k>0 $& FLIP[rel],x,v)
 n=numer_denom(a)[0]
 if rel=='/=':
  $<=[('$+',('/=',x,v),('/=',n,0))]
 $&:
  $<=[('$+',(rel,x,v),('>',a,0)),
 ('$+',(FLIP[rel],x,v),('<',a,0))]
 if $/(n)is $p:
  b=$Y(b,n,0)
 if $7(b):
  if relok(rel,fv(b)):
   $<.$%(('=',n,0))
 $&:
  $<.$%(('$+',('=',n,0),(rel,b,0)))
 $!('or',)+$3($<)if $0($<)>1 $& $<[0]
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
$, domainpts(f,x,$<):
 if $/(f)is $- $3 or f[0]=='Q':
  $!
 h=f[0]
 if h=='^' $+ $- $9(f[1],x):
  if $D(f[2])$+ $b(f[2])<0:
   $<.$%(f[1])
  if isq(f[2])$+ f[2][2]%2==0:
   $<.$%(f[1])
 if h in('ln','log','$J','sign','floor','ceiling')$+ $- $9(f[1],x):
  $<.$%(f[1])
 $) a in f[1:]:
  domainpts(a,x,$<)
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
 if $0(ivs)>=2 $+ ivs[0][0]is $# $+ ivs[-1][2]is $#:
  okp=$A
  $) i in $*($0(ivs)-1):
   if $-(ivs[i][2]==ivs[i+1][0]$+ $- ivs[i][3]$+ $- ivs[i+1][1]):
    okp=$2
  if okp:
   ne=[('/=',x,ivs[i][2])$) i in $*($0(ivs)-1)]
   $! ne[0]if $0(ne)==1 $&('$+',)+$3(ne)
 $<=[]
 $) lo,li,hi,hiinc in ivs:
  if lo is $# $+ hi is $#:
   $! 'true'
  if lo is $- $# $+ hi is $- $# $+ lo==hi:
   $<.$%(('=',x,lo))
  $? lo is $#:
   $<.$%(('<=' if hiinc $& '<',x,hi))
  $? hi is $#:
   $<.$%(('>=' if li $& '>',x,lo))
  $&:
   $<.$%(('$+',('<=' if li $& '<',lo,x),('<=' if hiinc $& '<',x,hi)))
 if $0($<)==1:
  $! $<[0]
 $!('or',)+$3($<)
$, eqexpr(eq):
 if $((eq,'='):
  $! $.($c(eq[1],eq[2]))
 $! eq
$, is_linear_sys(fs,vs):
 $) f in fs:
  $) v in vs:
   d=degree(f,v)
   if d is $# or d>1:
    $! $2
  g=$=(f)
  $) i in $*($0(vs)):
   $) j in $*($0(vs)):
    cs_=$_(g,vs[i])
    if cs_ is $#:
     $! $2
    if $0(cs_)>1 $+ has(cs_[1],vs[j]):
     $! $2
 $! $A
$, linsys(fs,vs):
 m=$0(fs)
 n=$0(vs)
 A=[]
 $) f in fs:
  g=$=(f)
  row=[]
  $`=g
  $) v in vs:
   cs_=$_(g,v)
   c=cs_[1]if $0(cs_)>1 $& 0
   row.$%(c)
  const=g
  $) v in vs:
   const=$Y(const,v,0)
  row.$%($r(const))
  A.$%(row)
 piv=[]
 r=0
 $) c in $*(n):
  p=$#
  $) i in $*(r,m):
   if $.(A[i][c])!=0:
    p=i
    $R
  if p is $#:
   $4
  A[r],A[p]=A[p],A[r]
  pv=A[r][c]
  A[r]=[$.($Z(a,pv))$) a in A[r]]
  $) i in $*(m):
   if i!=r $+ A[i][c]!=0:
    fct=A[i][c]
    A[i]=[$.($=($c(A[i][j],$:(fct,A[r][j]))))$) j in $*(n+1)]
  piv.$%(c)
  r+=1
  if r==m:
   $R
 $) i in $*(r,m):
  if $.(A[i][n])!=0:
   $![]
 sol={}
 free=[c $) c in $*(n)if c $- in piv]
 params={}
 k=1
 $) c in free:
  params[vs[c]]='c'+$p(k)
  k+=1
 $) i in $*($0(piv)):
  c=piv[i]
  val=A[i][n]
  $) c2 in free:
   val=$c(val,$:(A[i][c2],params[vs[c2]]))
  sol[vs[c]]=nice($.(val))
 $) c in free:
  sol[vs[c]]=params[vs[c]]
 $![sol]
$, solve_system(eqs,vs,$E=$2,guesses=$#):
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
 r=elim(fs,vs,$E,0)
 if r is $#:
  $! newton_sys(fs,vs,[0.0]*$0(vs))
 $<=[]
 $) s in r:
  ok=$A
  $) v in vs:
   if v $- in s:
    s[v]=v
  if $- $E:
   $) v in vs:
    if $7(s[v])$+ $- $}(s[v]):
     ok=$2
  if ok $+ s $- in $<:
   $<.$%(s)
 $! $<
$, hasdenom_x(f,vs):
 $) v in vs:
  nu,de=numer_denom(f)
  if has(de,v):
   $! $A
 $! $2
''')
_x(r'''$, elim(fs,vs,$E,$@):
 fs=[$.($=(f))$) f in fs]
 fs=[f $) f in fs if f!=0]
 if $- fs:
  $![{}]
 $) f in fs:
  if freeofall(f,vs):
   if $7(f)or f!=0:
    $![]
 if $@>8:
  $! $#
 best=$#
 $) f in fs:
  inv=[v $) v in vs if has(f,v)]
  if $0(inv)==1:
   best=(f,inv[0])
   $R
 if best is $#:
  $) f in fs:
   $) v in vs:
    d=degree(f,v)
    if d==1:
     c=$_(f,v)
     if c is $- $# $+ $7(c[1])$+ c[1]!=0:
      best=(f,v)
      $R
   if best:
    $R
 if best is $#:
  $) f in fs:
   $) v in vs:
    if degree(f,v)==1:
     best=(f,v)
     $R
   if best:
    $R
 if best is $- $#:
  f,v=best
  rs=$|(f,v,$E)
  if rs is $#:
   $! $#
  if rs=='all':
   rs=[]
  $<=[]
  $`=[g $) g in fs if g is $- f]
  ovs=[w $) w in vs if w!=v]
  $) r in rs:
   sub_=[$.($Y(g,v,r))$) g in $`]
   rr=elim(sub_,ovs,$E,$@+1)
   if rr is $#:
    $! $#
   $) s in rr:
    s2=dict(s)
    val=r
    $) w in s2:
     val=$Y(val,w,s2[w])
    s2[v]=clean(val)
    $<.$%(s2)
  $! $<
 if $0(fs)>=2 $+ $0(vs)>=2:
  y=vs[-1]
  R=resultant(fs[0],fs[1],y)
  if R is $# or R==0:
   $! $#
  rr=elim([R]+fs[2:],vs[:-1],$E,$@+1)
  if rr is $#:
   $! $#
  $<=[]
  $) s in rr:
   gs=[]
   $) g in fs:
    h=g
    $) w in s:
     h=$Y(h,w,s[w])
    gs.$%($.($=(h)))
   ys=elim(gs,[y],$E,$@+1)
   if ys is $#:
    $4
   $) t in ys:
    s2=dict(s)
    s2.update(t)
    $<.$%(s2)
  $! $<
 $! $#
$, resultant(f,g,y):
 a=$_(f,y)
 b=$_(g,y)
 if a is $# or b is $#:
  $! $#
 m=$0(a)-1
 n=$0(b)-1
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
 $! $=(bareiss(M))
$, bareiss(M):
 n=$0(M)
 M=[$I(r)$) r in M]
 sign=1
 prev=1
 $) k in $*(n-1):
  if M[k][k]==0:
   sw=$#
   $) i in $*(k+1,n):
    if M[i][k]!=0:
     sw=i
     $R
   if sw is $#:
    $! 0
   M[k],M[sw]=M[sw],M[k]
   sign=-sign
  $) i in $*(k+1,n):
   $) j in $*(k+1,n):
    num=$=($c($:(M[i][j],M[k][k]),$:(M[i][k],M[k][j])))
    M[i][j]=exdiv(num,prev)
  prev=M[k][k]
 $! $:(sign,M[n-1][n-1])
$, exdiv(a,b):
 if b==1:
  $! a
 if $D(b):
  $! $=($:(a,ninv(b))if $q(b)$& $Z(a,b))
 ks=[]
 kernels(a,ks)
 kernels(b,ks)
 sortkernels(ks)
 ra=ratform(a,ks)
 rb=ratform(b,ks)
 if ra is $# or rb is $#:
  $! $.($Z(a,b))
 q=$K(p_mul(ra[0],rb[1]),p_mul(ra[1],rb[0]))
 if q is $#:
  $! $.($Z(a,b))
 $! p2e(q,ks)
$, newton_sys(fs,vs,guess):
 n=$0(vs)
 if $0(fs)!=n:
  $! $#
 others=[]
 $) f in fs:
  $) s in $l(f):
   if s $- in vs:
    $! $#
 J=[[diff(f,v)$) v in vs]$) f in fs]
 xv=[$F($V(g).$S)if $D(g)or $7(g)$& 0.0 $) g in guess]
 $) it in $*(100):
  env=dict(zip(vs,xv))
  try:
   F=[$V(f,env)$) f in fs]
   Jv=[[$V(J[i][j],env)$) j in $*(n)]$) i in $*(n)]
  $6 $>:
   $! $#
  F=[v.$S if $/(v)is $1 $& v $) v in F]
  Jv=[[v.$S if $/(v)is $1 $& v $) v in r]$) r in Jv]
  dx=linsolve_float(Jv,[-v $) v in F])
  if dx is $#:
   $! $#
  xv=[xv[i]+dx[i]$) i in $*(n)]
  if max([$J(d)$) d in dx])<1e-13*(1+max([$J(v)$) v in xv])):
   $R
 env=dict(zip(vs,xv))
 try:
  if max([$J($V(f,env))$) f in fs])>1e-8:
   $![]
 $6 $>:
  $![]
 $![dict([(vs[i],snap(xv[i]))$) i in $*(n)])]
$, linsolve_float(A,b):
 n=$0(A)
 M=[$I(A[i])+[b[i]]$) i in $*(n)]
 $) c in $*(n):
  p=max($*(c,n),key=$5 i:$J(M[i][c]))
  if $J(M[p][c])<1e-300:
   $! $#
  M[c],M[p]=M[p],M[c]
  $) i in $*(n):
   if i!=c:
    f=M[i][c]/M[c][c]
    $) j in $*(c,n+1):
     M[i][j]-=f*M[c][j]
 $![M[i][n]/M[i][i]$) i in $*(n)]
$, sols_to_bool(x,$f):
 if $f=='all':
  $! 'true'
 if $f is $#:
  $! $#
 if $- $f:
  $! 'false'
 eqs=[('=',x,s)$) s in $f]
 if $0(eqs)==1:
  $! eqs[0]
 $!('or',)+$3(eqs)
$, apply_constraints($f,x,cons):
 if $- cons or $f=='all' or $f is $#:
  $! $f
 lo=$#
 hi=$#
 $<=[]
 expanded=[]
 $) s in $f:
  ns=[w $) w in $l(s)if w[0]=='n' $+ w[1:].isdigit()]
  if ns $+ $0(ns)==1:
   b=bounds(cons,x)
   if b is $#:
    expanded.$%(s)
    $4
   n=ns[0]
   $) k in $*(-60,61):
    v=$Y(s,n,k)
    expanded.$%(v)
  $&:
   expanded.$%(s)
 $) s in expanded:
  if satisfies(s,x,cons):
   $<.$%(s)
 $! sortsols(dedup($<))
$, bounds(cons,x):
 lo=$#
 hi=$#
 $) c in cons:
  if head(c)in('<','<=','>','>=')$+ $7(c[1])$+ c[2]==x:
   if c[0]in('<','<='):
    lo=c[1]
   $&:
    hi=c[1]
  $? head(c)in('<','<=','>','>=')$+ c[1]==x $+ $7(c[2]):
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
   try:
    a=fv($Y(c[1],x,s))
    b=fv($Y(c[2],x,s))
   $6 $>:
    if $- $7(s):
     $4
    $! $2
   eps=1e-12*(1+$J(a)+$J(b))
   if h=='<' $+ $- a<b-eps*0:
    $! $2
   if h=='<=' $+ $- a<=b+eps:
    $! $2
   if h=='>' $+ $- a>b:
    $! $2
   if h=='>=' $+ $- a>=b-eps:
    $! $2
   if h=='/=' $+ $J(a-b)<=eps:
    $! $2
  $? h=='$+':
   if $- satisfies(s,x,$I(c[1:])):
    $! $2
 $! $A
''')
_x(r'''$, solve(eq,x,$E=$2,cons=$#):
 NC[0]=0
 if $((eq,'$+')or $((eq,'$I'):
  $! $#
 h=head(eq)
 if h in('<','>','<=','>=','/='):
  f=$c(eq[1],eq[2])
  r=solve_ineq(h,f,x)
  $! r
 if h=='=':
  f=$c(eq[1],eq[2])
 $? h=='or':
  parts=[]
  $) e in eq[1:]:
   r=solve(e,x,$E,cons)
   if r is $#:
    $! $#
   if r!='false':
    parts.$%(r)
  if $- parts:
   $! 'false'
  $!('or',)+$3(parts)if $0(parts)>1 $& parts[0]
 $? eq=='true':
  $! 'true'
 $&:
  f=eq
 $f=$|(f,x,$E)
 if $f is $#:
  $! $#
 if $f!='all':
  $f=[clean(s)$) s in $f]
  if $- $E:
   $f=[s $) s in $f if $-($7(s)$+ $- $}(s))]
   $f=[realpart(s)$) s in $f]
  $f=sortsols(dedup($f))
 if cons:
  $f=apply_constraints($f,x,cons)
 $! sols_to_bool(x,$f)
$, realpart(s):
 if $7(s)$+ has(s,'i'):
  r,i=reim(s)
  if i==0 or($D(i)$+ $J(tofl(i))<1e-12):
   $! r
 $! s
$, zeros(e,x,$E=$2,cons=$#):
 NC[0]=0
 if $((e,'='):
  e=$c(e[1],e[2])
 $f=$|(e,x,$E)
 if $f is $#:
  $! $#
 if $f=='all':
  $!('$I',)
 $f=[clean(s)$) s in $f]
 if $- $E:
  $f=[realpart(s)$) s in $f if $-($7(s)$+ $- $}(s))]
 $f=sortsols(dedup($f))
 if cons:
  $f=apply_constraints($f,x,cons)
 $!('$I',)+$3($f)
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
 cs_=$_(F,y1)
 if cs_ is $- $# $+ $0(cs_)==2 $+ $9(cs_[1],y1):
  g=$.($r($Z(cs_[0],cs_[1])))
 $&:
  rs=$|(F,y1)
  if $- rs or rs=='all' or $0(rs)!=1:
   $! $#
  g=rs[0]
 c1='c1'
 gy=$_($=(g),y)
 if gy is $- $# $+ $0(gy)==2 $+ $9(gy[1],y):
  P=$r(gy[1])
  Bq=gy[0]
  if Bq==0 or $9(P,x)$+ $9(Bq,x)$+ $2:
   pass
  mu=pw('e',integrate(P,x))
  mu=dropabs(simp(mu))
  I=integ($.($=($:(mu,Bq))),x)
  if I is $- $#:
   yy=$.($Z($d(I,c1),mu))
   $!('=',y,nice($=(yy))if $- hasden_free(yy)$& nice(yy))
 sep=separate(g,x,y)
 if sep is $- $#:
  p,q=sep
  L=integ($.(pw(q,-1)),y)
  R=integ(p,x)
  if L is $- $# $+ R is $- $#:
   rs=isolate_eq(L,$d(R,c1),y)
   if rs is $- $# $+ $0(rs)==1:
    $!('=',y,nice(simp(rs[0])))
   G=lncombine(L,y)
   if G is $- $#:
    rs=$|($c(G,$:(c1,pw('e',R))),y)
    if rs $+ rs!='all' $+ $0(rs)==1:
     $!('=',y,nice(rs[0]))
   $!('=',L,$d(R,c1))
 bern_=bernoulli(g,x,y)
 if bern_ is $- $#:
  $! bern_
 V='V_'
 h=$.($Y(g,y,$:(V,x)))
 if $9(h,x)$+ has(h,V):
  dv=$.($c(h,V))
  if dv!=0:
   L=integ($.(pw(dv,-1)),V)
   if L is $- $#:
    R=$d(fn('ln',fn('$J',x)),c1)
    rs=isolate_eq(L,R,V)
    if rs is $- $# $+ $0(rs)==1:
     $!('=',y,nice($=($:(x,rs[0]))))
    L2=$Y(L,V,$Z(y,x))
    $!('=',L2,R)
 $! $#
$, dropabs(e):
 if $/(e)is $- $3 or e[0]=='Q':
  $! e
 if e[0]=='$J':
  $! dropabs(e[1])
 $! simp((e[0],)+$3(dropabs(a)$) a in e[1:]))
$, lncombine(L,y):
 $Q=L[1:]if $((L,'+')$&(L,)
 fs=[]
 $) t in $Q:
  c,r=$X(t)
  if $((r,'ln')$+ $q(c):
   u=r[1]
   if $((u,'$J'):
    u=u[1]
   fs.$%(pw(u,c))
  $&:
   $! $#
 if $0(fs)<1:
  $! $#
 $! $.($H(fs))
$, hasden_free(e):
 $! $2
$, isolate_eq(L,R,y):
 try:
  r=isolate(L,R,y,$2,0)
 $6 $>:
  $! $#
 if r is $# or r=='all':
  $! $#
 $! r
$, separate(g,x,y):
 if $9(g,y):
  $! g,1
 if $9(g,x):
  $! 1,g
 fs=g[1:]if $((g,'*')$&(g,)
 px=[]
 qy=[]
 $) f in fs:
  if $9(f,y):
   px.$%(f)
  $? $9(f,x):
   qy.$%(f)
  $? $((f,'^')$+ $9(f[1],x)$+ $9(f[1],y)$+ $((f[2],'+'):
   tx=[t $) t in f[2][1:]if $9(t,y)]
   ty=[t $) t in f[2][1:]if $9(t,x)]
   if $0(tx)+$0(ty)!=$0(f[2])-1:
    $! $#
   px.$%(pw(f[1],$8(tx)))
   qy.$%(pw(f[1],$8(ty)))
  $&:
   $! $#
 $! $H(px),$H(qy)
$, expand_exp(e):
 if $/(e)is $- $3 or e[0]=='Q':
  $! e
 if e[0]=='^' $+ $((e[2],'+')$+(e[1]=='e' or $D(e[1])):
  $! $H([pw(e[1],t)$) t in e[2][1:]])
 $! simp((e[0],)+$3(expand_exp(a)$) a in e[1:]))
$, bernoulli(g,x,y):
 g=$=(g)
 $Q=g[1:]if $((g,'+')$&(g,)
 groups={}
 $) t in $Q:
  k=$#
  fs=t[1:]if $((t,'*')$&(t,)
  $`=[]
  $) f in fs:
   if f==y:
    k=1 if k is $# $& $#
   $? $((f,'^')$+ f[1]==y $+ $D(f[2]):
    k=f[2]
   $? $9(f,y):
    $`.$%(f)
   $&:
    $! $#
  if k is $#:
   $! $#
  groups[k]=$d(groups.get(k,0),$H($`))
 if $0(groups)!=2 or 1 $- in groups:
  $! $#
 n=[k $) k in groups if k!=1][0]
 a=groups[1]
 b=groups[n]
 m=nsub(1,n)
 V='V_'
 vs=de1($c(YP[0],$:(m,$d($:(a,V),b))),x,V)
 if vs is $# or $- $((vs,'=')or vs[1]!=V:
  $! $#
 $!('=',y,nice(pw(vs[2],ninv(m))))
''')
_x(r'''$, de2(F,x,y):
 y1,y2=YP
 c1,c2='c1','c2'
 G=$=(F)
 a=$_(G,y2)
 if a is $# or $0(a)!=2:
  $! $#
 A=a[1]
 $`=a[0]
 b=$_($`,y1)
 if b is $# or $0(b)>2:
  $! $#
 B=b[1]if $0(b)==2 $& 0
 $`=b[0]
 c=$_($`,y)
 if c is $# or $0(c)>2:
  $! $#
 C=c[1]if $0(c)==2 $& 0
 g=$r(c[0])
 $) t in(A,B,C):
  if has(t,y)or has(t,y1)or has(t,y2):
   $! $#
 if $9(A,x)$+ $9(B,x)$+ $9(C,x):
  y1s,y2s=charsol(A,B,C,x)
 $&:
  ce=cauchy_euler(A,B,C,x)
  if ce is $#:
   if C==0:
    V='V_'
    r=de1($d($:(A,YP[0]),$:(B,V),$r(g)),x,V)
    if r is $# or $- $((r,'=')or r[1]!=V:
     $! $#
    r2=integ($Y(r[2],'c1','c2'),x)
    if r2 is $#:
     $! $#
    $!('=',y,$d(r2,c1))
   $! $#
  y1s,y2s=ce
 yh=$d($:(c1,y1s),$:(c2,y2s))
 if g==0:
  $!('=',y,yh)
 W=pyth($.($=($c($:(y1s,diff(y2s,x)),$:(diff(y1s,x),y2s)))))
 gg=$.($Z(g,A))
 I1=integ($.($=($Z($:(y2s,gg),W))),x)
 I2=integ($.($=($Z($:(y1s,gg),W))),x)
 if I1 is $# or I2 is $#:
  $! $#
 yp=pyth($=($d($:($r(y1s),I1),$:(y2s,I2))))
 $!('=',y,nice($d(yh,yp)))
$, charsol(A,B,C,x):
 D=$.($=($c($:(B,B),$:(4,A,C))))
 if $}(D)$+ fv(D)<0:
  al=$.($Z($r(B),$:(2,A)))
  be=$.($Z($L($r(D)),$:(2,A)))
  ex=pw('e',$:(al,x))
  $! $:(ex,fn('cos',$:(be,x))),$:(ex,fn('sin',$:(be,x)))
 if D==0:
  r=$.($Z($r(B),$:(2,A)))
  $! pw('e',$:(r,x)),$:(x,pw('e',$:(r,x)))
 s=$L(D)
 r1=$.($Z($d($r(B),s),$:(2,A)))
 r2=$.($Z($c($r(B),s),$:(2,A)))
 $! pw('e',$:(r1,x)),pw('e',$:(r2,x))
$, cauchy_euler(A,B,C,x):
 a=$.($Z(A,pw(x,2)))
 b=$.($Z(B,x))
 if $-($9(a,x)$+ $9(b,x)$+ $9(C,x)):
  $! $#
 aa=a
 bb=$c(b,a)
 cc=C
 D=$.($=($c($:(bb,bb),$:(4,aa,cc))))
 lx=fn('ln',x)
 if $}(D)$+ fv(D)<0:
  al=$.($Z($r(bb),$:(2,aa)))
  be=$.($Z($L($r(D)),$:(2,aa)))
  $! $:(pw(x,al),fn('cos',$:(be,lx))),$:(pw(x,al),fn('sin',$:(be,lx)))
 if D==0:
  r=$.($Z($r(bb),$:(2,aa)))
  $! pw(x,r),$:(pw(x,r),lx)
 s=$L(D)
 r1=$.($Z($d($r(bb),s),$:(2,aa)))
 r2=$.($Z($c($r(bb),s),$:(2,aa)))
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
   eqs.$%(('=',$Y(e,x,x0),v))
 $&:
  $) order,x0,v in conds:
   if order==0:
    eqs.$%($Y($Y(sol,x,x0),y,v))
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
   r=(r[0],$Y(r[1],c,s[c]),$Y(r[2],c,s[c]))
 if r[1]==y:
  $!('=',y,nice(r[2]))
 rs2=isolate_eq(r[1],r[2],y)
 if rs2 is $- $# $+ $0(rs2)>=1:
  $) cand in rs2:
   ok=$A
   $) order,x0,v in conds:
    if order==0:
     try:
      if $J($V($Y(cand,x,x0))-$V(v))>1e-9:
       ok=$2
     $6 $>:
      pass
   if ok:
    $!('=',y,nice(cand))
 $! r
$, fextreme(f,x,kind,lo=$#,hi=$#):
 NC[0]=0
 d=$.(diff(f,x))
 cands=[]
 rs=$|(d,x)
 if rs is $#:
  rs=numeric_solve(d,x,$2,tofl($V(lo))if lo is $- $# $+ $7(lo)$& $#,
 tofl($V(hi))if hi is $- $# $+ $7(hi)$& $#)or[]
 if rs=='all':
  $! 'true'
 exp_=[]
 $) r in rs:
  ns=[w $) w in $l(r)if w[0]=='n' $+ w[1:].isdigit()]
  if ns $+ lo is $- $# $+ hi is $- $#:
   $) k in $*(-50,51):
    exp_.$%($Y(r,ns[0],k))
  $? ns:
   exp_.$%(r)
  $&:
   exp_.$%(r)
 rs=exp_
 $) r in rs:
  r=clean(r)
  ns=[w $) w in $l(r)if w[0]=='n' $+ w[1:].isdigit()]
  if ns:
   cands.$%(r)
   $4
  if $- $}(r):
   $4
  if lo is $- $# $+ fv(r)<fv(lo)-1e-12:
   $4
  if hi is $- $# $+ fv(r)>fv(hi)+1e-12:
   $4
  cands.$%(r)
 ends=[]
 ends.$%(lo if lo is $- $# $&('*',-1,'$['))
 ends.$%(hi if hi is $- $# $& '$[')
 best=$#
 bv=$#
 pts=[]
 $) c in cands+ends:
  if c=='$[' or c==('*',-1,'$['):
   v=limit(f,x,c)
  $&:
   cz=c
   $) w in $l(c):
    if w[0]=='n' $+ w[1:].isdigit():
     cz=$Y(cz,w,0)
   v=$Y(f,x,cz)
   if has(v,'$M'):
    $4
  try:
   if v=='$[':
    vv=$F('$[')
   $? v==('*',-1,'$['):
    vv=$F('-$[')
   $&:
    vv=fv(v)
  $6 $>:
   $4
  if kind=='max':
   vv=-vv
  pts.$%((vv,c))
 if $- pts:
  $! $#
 pts.sort(key=$5 p:p[0])
 m=pts[0][0]
 win=[p[1]$) p in pts if $J(p[0]-m)<=1e-10*(1+$J(m))or p[0]==m]
 win=sortsols(dedup(win))
 eqs=[('=',x,w)$) w in win]
 $! eqs[0]if $0(eqs)==1 $&('or',)+$3(eqs)
$, nfextreme(f,x,kind,lo=$#,hi=$#):
 sg=1.0 if kind=='min' $&-1.0
 $, F(t):
  try:
   v=$V(f,{x:t})
   if $/(v)is $1:
    v=v.$S
   $! sg*v
  $6 $>:
   $! $F('$[')
 if lo is $# or hi is $#:
  a=-100.0 if lo is $# $& lo
  b=100.0 if hi is $# $& hi
 $&:
  a,b=lo,hi
 N=400
 best=a
 bv=F(a)
 $) i in $*(N+1):
  t=a+(b-a)*i/N
  v=F(t)
  if v<bv:
   bv=v
   best=t
 h=(b-a)/N
 l=max(a,best-h)
 r=min(b,best+h)
 g=($U.$L(5)-1)/2
 $) _ in $*(200):
  c=r-g*(r-l)
  d=l+g*(r-l)
  if F(c)<F(d):
   r=d
  $&:
   l=c
  if $J(r-l)<1e-12*(1+$J(l)):
   $R
 t=0.5*(l+r)
 try:
  d=diff(f,x)
  $, G(u):
   try:
    v=$V(d,{x:u})
    $! v.$S if $/(v)is $1 $& v
   $6 $>:
    $! $#
  t2=newton(G,t)
  if t2 is $- $# $+ $J(t2-t)<10*h $+(lo is $# or t2>=lo)$+(hi is $# or t2<=hi):
   t=t2
 $6 $>:
  pass
 $! snap(t)
''')
_x(r'''$, domain(f,x):
 conds=[]
 domconds(f,x,conds)
 if $- conds:
  $!('<',('*',-1,'$['),x)if $2 $& 'true'
 pts=[]
 $) rel,g in conds:
  rs=$|(g,x)
  if rs is $#:
   $! $#
  if rs=='all':
   $4
  $) r in rs:
   if $}(r):
    pts.$%(r)
 pts=sortsols(dedup(pts))
 $, ok(t):
  $) rel,g in conds:
   try:
    v=$V(g,{x:t})
   $6 $>:
    $! $2
   if $/(v)is $1:
    if $J(v.imag)>1e-9:
     $! $2
    v=v.$S
   if $- relok(rel,v):
    $! $2
  $! $A
 $, okexact(p):
  $) rel,g in conds:
   try:
    v=$Y(g,x,p)
    vv=fv(v)
   $6 $>:
    $! $2
   if $J(vv)<1e-12:
    vv=0.0
   if $- relok(rel,vv):
    $! $2
  $! $A
 $g=[fv(p)$) p in pts]
 if $- $g:
  $! 'true' if ok(0.5)$& 'false'
 segs=[('I',$#,pts[0],ok($g[0]-max(1.0,$J($g[0]))))]
 $) i in $*($0(pts)):
  segs.$%(('P',pts[i],pts[i],okexact(pts[i])))
  if i+1<$0(pts):
   segs.$%(('I',pts[i],pts[i+1],ok(0.5*($g[i]+$g[i+1]))))
 segs.$%(('I',pts[-1],$#,ok($g[-1]+max(1.0,$J($g[-1])))))
 $! segs_to_bool(segs,x)
$, domconds(f,x,$<):
 if $/(f)is $- $3 or f[0]=='Q' or $9(f,x):
  $!
 h=f[0]
 if h=='^':
  b,p=f[1],f[2]
  if $D(p)$+ $b(p)<0:
   $<.$%(('/=',b))
  if isq(p)$+ p[2]%2==0:
   $<.$%(('>=' if $b(p)>0 $& '>',b))
 $? h in('ln','log'):
  $<.$%(('>',f[1]))
 $? h in('$w','arccos'):
  $<.$%(('<=',$c(fn('$J',f[1]),1)))
 $? h=='tan':
  $<.$%(('/=',fn('cos',f[1])))
 $) a in f[1:]:
  domconds(a,x,$<)
''')
_x(r'''import $U
$, ismat(e):
 $! $((e,'mat')
$, $^(e):
 $! $((e,'$I')
$, $T(M):
 $![$I(r[1:])$) r in M[1:]]
$, mk(R):
 $!('mat',)+$3(('$I',)+$3(r)$) r in R)
$, lst(xs):
 $!('$I',)+$3(xs)
$, dims(M):
 $! $0(M)-1,$0(M[1])-1
$, tomat(e):
 if ismat(e):
  $! e
 if $^(e):
  $! mk([$I(e[1:])])
 err("Matrix expected")
$, ac(e):
 $! $.($=(e))if hasdenom(e)$& $=(e)
$, m_add(A,B,sgn=1):
 if dims(A)!=dims(B):
  err("Dimension error")
 a=$T(A)
 b=$T(B)
 $! mk([[$d(a[i][j],$:(sgn,b[i][j]))$) j in $*($0(a[0]))]$) i in $*($0(a))])
$, m_scale(A,c):
 $! mk([[$:(c,v)$) v in r]$) r in $T(A)])
$, m_map(A,f):
 $! mk([[f(v)$) v in r]$) r in $T(A)])
$, m_mul(A,B):
 a=$T(A)
 b=$T(B)
 if $0(a[0])!=$0(b):
  err("Dimension error")
 n=$0(b)
 $! mk([[ac($8([$:(a[i][k],b[k][j])$) k in $*(n)]))$) j in $*($0(b[0]))]$) i in $*($0(a))])
$, ident(n):
 $! mk([[1 if i==j $& 0 $) j in $*(n)]$) i in $*(n)])
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
 if $^(A):
  $! mk([[v]$) v in A[1:]])
 a=$T(A)
 $! mk([[a[i][j]$) i in $*($0(a))]$) j in $*($0(a[0]))])
$, det(A):
 a=$T(A)
 n=$0(a)
 if n!=$0(a[0]):
  err("Square matrix required")
 if n==1:
  $! a[0][0]
 if n==2:
  $! ac($c($:(a[0][0],a[1][1]),$:(a[0][1],a[1][0])))
 if n==3:
  t=[]
  $) j in $*(3):
   minor=$c($:(a[1][(j+1)%3],a[2][(j+2)%3]),$:(a[1][(j+2)%3],a[2][(j+1)%3]))
   t.$%($:(a[0][j],minor))
  $! ac($8(t))
 M=[$I(r)$) r in a]
 sign=1
 prev=1
 $) k in $*(n-1):
  if ac(M[k][k])==0:
   sw=$#
   $) i in $*(k+1,n):
    if ac(M[i][k])!=0:
     sw=i
     $R
   if sw is $#:
    $! 0
   M[k],M[sw]=M[sw],M[k]
   sign=-sign
  $) i in $*(k+1,n):
   $) j in $*(k+1,n):
    M[i][j]=ac($Z($c($:(M[i][j],M[k][k]),$:(M[i][k],M[k][j])),prev))
  prev=M[k][k]
 $! ac($:(sign,M[n-1][n-1]))
$, iszero(v):
 v=ac(v)
 if v==0:
  $! $A
 if $/(v)is $F $+ $J(v)<1e-13:
  $! $A
 $! $2
$, rref(A,full=$A):
 M=[$I(r)$) r in $T(A)]
 m=$0(M)
 n=$0(M[0])
 r=0
 $) c in $*(n):
  if r>=m:
   $R
  p=$#
  if hasfloat_m(M):
   best=0.0
   $) i in $*(r,m):
    try:
     v=$J($V(M[i][c]))
    $6 $>:
     v=1.0 if $- iszero(M[i][c])$& 0.0
    if v>best+1e-14:
     best=v
     p=i
   if best<1e-13:
    p=$#
  $&:
   $) i in $*(r,m):
    if $- iszero(M[i][c]):
     p=i
     $R
  if p is $#:
   $4
  M[r],M[p]=M[p],M[r]
  pv=M[r][c]
  if full:
   M[r]=[ac($Z(v,pv))$) v in M[r]]
  $&:
   M[r]=[ac($Z(v,pv))$) v in M[r]]
  rng=$*(m)if full $& $*(r+1,m)
  $) i in rng:
   if i!=r $+ $- iszero(M[i][c]):
    f=M[i][c]
    M[i]=[ac($c(M[i][j],$:(f,M[r][j])))$) j in $*(n)]
  r+=1
 $) i in $*(m):
  $) j in $*(n):
   if $/(M[i][j])is $F $+ $J(M[i][j])<1e-13:
    M[i][j]=0.0
 $! mk(M)
$, hasfloat_m(M):
 $) r in M:
  $) v in r:
   if $a(v):
    $! $A
 $! $2
$, minor(a,i,j):
 $![[a[r][c]$) c in $*($0(a))if c!=j]$) r in $*($0(a))if r!=i]
$, m_inv(A):
 m,n=dims(A)
 if m!=n:
  err("Square matrix required")
 a0=$T(A)
 if n<=3 $+ $- all([$D(v)$) r in a0 $) v in r]):
  D=det(A)
  if iszero(D):
   err("Singular matrix")
  if n==1:
   $! mk([[nice(pw(D,-1))]])
  $<=[]
  $) i in $*(n):
   row=[]
   $) j in $*(n):
    c=det(mk(minor(a0,j,i)))
    if(i+j)%2:
     c=$r(c)
    row.$%(nice(ac($Z(c,D))))
   $<.$%(row)
  $! mk($<)
 a=$T(A)
 aug=mk([a[i]+[1 if i==j $& 0 $) j in $*(n)]$) i in $*(n)])
 R=$T(rref(aug))
 $) i in $*(n):
  $) j in $*(n):
   if $- iszero($c(R[i][j],1 if i==j $& 0)):
    err("Singular matrix")
 $! mk([[nice(R[i][n+j])$) j in $*(n)]$) i in $*(n)])
$, trace(A):
 a=$T(A)
 $! $8([a[i][i]$) i in $*($0(a))])
$, charpoly(A,lam):
 a=$T(A)
 n=$0(a)
 if n!=$0(a[0]):
  err("Square matrix required")
 I=ident(n)
 Mk=mk([[0]*n $) _ in $*(n)])
 cs=[0]*(n+1)
 cs[n]=1
 $) k in $*(1,n+1):
  Mk=m_add(m_mul(A,Mk),m_scale(I,cs[n-k+1]))
  cs[n-k]=ac($Z($r(trace(m_mul(A,Mk))),k))
 $! $8([$:(cs[k],pw(lam,k))$) k in $*(n+1)])
$, eigvl(A):
 if hasfloat_m($T(A)):
  try:
   E=m_map(A,exactify)
  $6 $>:
   E=$#
  if E is $- $# $+ $- hasfloat_m($T(E)):
   $! evalf(eigvl(E))
 lam='L_'
 p=charpoly(A,lam)
 f=p
 if $- hasfloat_m($T(A)):
  try:
   f=$z(p)
  $6 $>:
   f=p
  if $((f,'hold'):
   f=f[1]
 $<=[]
 $) g in(f[1:]if $((f,'*')$&(f,)):
  k=1
  if $((g,'^')$+ $k(g[2])$+ g[2]>0:
   g,k=g[1],g[2]
  if $9(g,lam):
   $4
  z=zeros(g,lam,$A)
  if z is $#:
   err("Cannot compute eigenvalues")
  z=$I(z[1:])
  d=degree(g,lam)
  $) v in z:
   m=mult(g,lam,v,d)if d is $- $# $+ $0(z)<d $& 1
   $<+=[v]*(k*m)
 if $- $<:
  err("Cannot compute eigenvalues")
 $, key(v):
  if $- $7(v):
   $!(1,0.0,0.0,okey(v))
  z=$1($V(v))
  $!(0,-$J(z),-z.$S,-z.imag)
 $<.sort(key=key)
 $! lst($<)
$, mult(g,lam,v,d):
 m=1
 h=g
 $G m<d:
  h=diff_(h,lam)
  w=$Y(h,lam,v)
  if $a(w)or $a(v):
   try:
    if $J($1($V(w)))>1e-6*(1+$J($1($V(v))))**d:
     $R
   $6 $>:
    $R
  $? $- iszero(ac($=(w))):
   $R
  m+=1
 $! m
$, diff_(e,x):
 $! diff(e,x)
''')
_x(r'''$, nullspace(A):
 R=$T(rref(A))
 m=$0(R)
 n=$0(R[0])
 piv=[]
 $) i in $*(m):
  $) j in $*(n):
   if $- iszero(R[i][j]):
    piv.$%((i,j))
    $R
 pc=[j $) i,j in piv]
 free=[j $) j in $*(n)if j $- in pc]
 basis=[]
 $) f in free:
  v=[0]*n
  v[f]=1
  $) i,j in piv:
   v[j]=ac($r(R[i][f]))
  basis.$%(v)
 $! basis
$, eigvc(A):
 if hasfloat_m($T(A)):
  try:
   E=m_map(A,exactify)
  $6 $>:
   E=$#
  if E is $- $# $+ $- hasfloat_m($T(E)):
   $! evalf(eigvc(E))
 $g=eigvl(A)
 n=dims(A)[0]
 cols=[]
 seen=[]
 $) lv in $g[1:]:
  if lv in seen:
   $4
  seen.$%(lv)
  if $a(lv)or hasfloat_m($T(A)):
   cols.$%(numeigvec(A,lv))
   $4
  B=m_add(A,m_scale(ident(n),lv),-1)
  B=m_map(B,$5 v:ac(v))
  ns=nullspace(B)
  $) v in ns:
   cols.$%(unitvec(v))
 if $- cols:
  err("Cannot compute eigenvectors")
 M=mk([[cols[j][i]$) j in $*($0(cols))]$) i in $*(n)])
 $) c in cols:
  $) v in c:
   if esize(v)>60:
    $! evalf(M)
 $! M
$, numeigvec(A,lam):
 a=[[$1($V(c))$) c in r]$) r in $T(A)]
 n=$0(a)
 mu=$1($V(lam))
 mu+=1e-9*(1+$J(mu))
 M=[[a[i][j]-(mu if i==j $& 0)$) j in $*(n)]$) i in $*(n)]
 x=[$1(1.0+0.37*i)$) i in $*(n)]
 $) it in $*(4):
  y=clsolve(M,x)
  big=max([$J(v)$) v in y])or 1.0
  x=[v/big $) v in y]
 nrm=$U.$L(sum([$J(v)**2 $) v in x]))or 1.0
 x=[v/nrm $) v in x]
 k=0
 $) i in $*(n):
  if $J(x[i])>$J(x[k])+1e-12:
   k=i
 ph=x[k]/$J(x[k])
 $<=[]
 $) v in x:
  v=v/ph
  re=0.0 if $J(v.$S)<1e-12 $& v.$S
  im=0.0 if $J(v.imag)<1e-12 $& v.imag
  $<.$%(re if im==0.0 $& fromcomplex($1(re,im)))
 $! $<
$, clsolve(M,b):
 n=$0(M)
 a=[$I(M[i])+[b[i]]$) i in $*(n)]
 $) c in $*(n):
  p=c
  $) r in $*(c+1,n):
   if $J(a[r][c])>$J(a[p][c]):
    p=r
  a[c],a[p]=a[p],a[c]
  if $J(a[c][c])<1e-14:
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
$, coefs(e,$<):
 if $D(e):
  $<.$%(e)
 $? $((e,'+'):
  $) t in e[1:]:
   coefs(t,$<)
 $? $((e,'*')$+ $D(e[1]):
  $<.$%(e[1])
 $&:
  $<.$%(1)
$, unitvec(v):
 if hasfloat_m([v]):
  nrm=$L($8([$:(c,fn('conj',c))$) c in v]))
  $![nice(ac($Z(c,nrm)))$) c in v]
 cs=[]
 $) c in v:
  coefs(c,cs)
 den=1
 num=0
 $) q in cs:
  if $q(q)$+ q!=0:
   a,b=nd(q)
   den=ilcm(den,b)
   num=igcd(num,a)
 k=Q(den,num)if num $& 1
 $) c in v:
  if $- iszero(c):
   if isneg(c):
    k=$r(k)
   $R
 w=[ac($=($:(k,c)))$) c in v]
 n2=ac($=($8([$:(c,fn('conj',c))$) c in w])))
 r=$L(n2)
 if $D(r)or $- $((r,'^'):
  $![ac($Z(c,r))$) c in w]
 inv=('^',r[1],$r(r[2]))
 $![c if iszero(c)$&('*',c,inv)if $((c,'+')$& $:(c,inv)$) c in w]
$, esize(e):
 if $/(e)is $- $3 or e[0]=='Q':
  $! 1
 k=1
 $) a in e[1:]:
  k+=esize(a)
 $! k
$, lu(A):
 a=[$I(r)$) r in $T(A)]
 m=$0(a)
 n=$0(a[0])
 L=[[1 if i==j $& 0 $) j in $*(m)]$) i in $*(m)]
 P=$I($*(m))
 U=a
 $) k in $*(min(m,n)):
  p=$#
  if hasfloat_m(U):
   best=-1.0
   $) i in $*(k,m):
    v=$J($V(U[i][k]))
    if v>best:
     best=v
     p=i
   if best<1e-14:
    p=$#
  $&:
   $) i in $*(k,m):
    if $- iszero(U[i][k]):
     p=i
     $R
  if p is $#:
   $4
  if p!=k:
   U[k],U[p]=U[p],U[k]
   P[k],P[p]=P[p],P[k]
   $) j in $*(k):
    L[k][j],L[p][j]=L[p][j],L[k][j]
  $) i in $*(k+1,m):
   f=ac($Z(U[i][k],U[k][k]))
   L[i][k]=f
   U[i]=[ac($c(U[i][j],$:(f,U[k][j])))$) j in $*(n)]
 Pm=[[1 if P[i]==j $& 0 $) j in $*(m)]$) i in $*(m)]
 $! mk(L),mk(U),mk(Pm)
$, qr(A):
 a=$T(A)
 m=$0(a)
 n=$0(a[0])
 cols=[[a[i][j]$) i in $*(m)]$) j in $*(n)]
 Qc=[]
 R=[[0]*n $) _ in $*(n)]
 $) j in $*(n):
  v=cols[j]
  $) k in $*($0(Qc)):
   r=ac($8([$:(Qc[k][i],v[i])$) i in $*(m)]))
   R[k][j]=r
   v=[ac($c(v[i],$:(r,Qc[k][i])))$) i in $*(m)]
  nrm=nice($L(ac($8([pw(c,2)$) c in v]))))
  R[j][j]=nrm
  if iszero(nrm):
   Qc.$%([0]*m)
  $&:
   Qc.$%([nice(ac($Z(c,nrm)))$) c in v])
 Qm=mk([[Qc[j][i]$) j in $*(n)]$) i in $*(m)])
 $! Qm,mk(R)
$, crossp(u,v):
 a=vec(u)
 b=vec(v)
 if $0(a)==2:
  a=a+[0]
  b=b+[0]
 if $0(a)!=3 or $0(b)!=3:
  err("Dimension error")
 r=[ac($c($:(a[1],b[2]),$:(a[2],b[1]))),
 ac($c($:(a[2],b[0]),$:(a[0],b[2]))),
 ac($c($:(a[0],b[1]),$:(a[1],b[0])))]
 $! revec(r,u)
$, vec(u):
 if $^(u):
  $! $I(u[1:])
 if ismat(u):
  R=$T(u)
  if $0(R)==1:
   $! R[0]
  if $0(R[0])==1:
   $![r[0]$) r in R]
 err("Vector expected")
$, revec(r,like):
 if $^(like):
  $! lst(r)
 R=$T(like)
 if $0(R)==1:
  $! mk([r])
 $! mk([[v]$) v in r])
$, dotp(u,v):
 a=vec(u)
 b=vec(v)
 if $0(a)!=$0(b):
  err("Dimension error")
 $! ac($8([$:(a[i],b[i])$) i in $*($0(a))]))
$, norm(A):
 if $^(A)or ismat(A)$+(dims(A)[0]==1 or dims(A)[1]==1):
  v=vec(A)
  $! nice($L(ac($8([$:(c,fn('conj',c))$) c in v]))))
 $! nice($L(ac($8([$:(c,fn('conj',c))$) r in $T(A)$) c in r]))))
$, unitv(u):
 nrm=norm(u)
 $! revec([nice(ac($Z(c,nrm)))$) c in vec(u)],u)
$, rownorm(A):
 if $- ismat(A):
  err('Argument must be a matrix')
 $! maxexpr([ac($8([fn('$J',c)$) c in r]))$) r in $T(A)])
$, colnorm(A):
 if $- ismat(A):
  err('Argument must be a matrix')
 $! rownorm(transpose(A))
$, maxexpr(xs):
 best=$#
 bv=$#
 $) x in xs:
  v=$V(x)
  if best is $# or v>bv:
   best=x
   bv=v
 $! best
''')
_x(r'''$, augment(A,B):
 if $^(A)$+ $^(B):
  $! A+B[1:]
 a=$T(tomat(A))
 b=$T(tomat(B))
 if $0(a)!=$0(b):
  err("Dimension error")
 $! mk([a[i]+b[i]$) i in $*($0(a))])
$, colaugment(A,B):
 a=$T(tomat(A))
 b=$T(tomat(B))
 if $0(a[0])!=$0(b[0]):
  err("Dimension error")
 $! mk(a+b)
$, submat(A,r1=1,c1=1,r2=$#,c2=$#):
 a=$T(A)
 if r2 is $#:
  r2=$0(a)
 if c2 is $#:
  c2=$0(a[0])
 $! mk([a[i][c1-1:c2]$) i in $*(r1-1,r2)])
$, rowswap(A,i,j):
 a=$T(A)
 a[i-1],a[j-1]=a[j-1],a[i-1]
 $! mk(a)
$, rowadd(A,i,j):
 a=$T(A)
 a[j-1]=[$d(a[j-1][k],a[i-1][k])$) k in $*($0(a[0]))]
 $! mk(a)
$, mrow(c,A,i):
 a=$T(A)
 a[i-1]=[$:(c,v)$) v in a[i-1]]
 $! mk(a)
$, mrowadd(c,A,i,j):
 a=$T(A)
 a[j-1]=[ac($d(a[j-1][k],$:(c,a[i-1][k])))$) k in $*($0(a[0]))]
 $! mk(a)
$, diag(A):
 if $^(A):
  n=$0(A)-1
  $! mk([[A[i+1]if i==j $& 0 $) j in $*(n)]$) i in $*(n)])
 a=$T(A)
 if $0(a)==1 or $0(a[0])==1:
  v=vec(A)
  $! diag(lst(v))
 $! lst([a[i][i]$) i in $*(min($0(a),$0(a[0])))])
$, matlist(A):
 $! lst([v $) r in $T(A)$) v in r])
$, listmat(L,c=$#):
 xs=$I(L[1:])
 if c is $#:
  c=$0(xs)
 if $- $k(c)or c<1:
  err('Invalid number of columns')
 $<=[]
 $G xs:
  r=xs[:c]
  xs=xs[c:]
  $G $0(r)<c:
   r.$%(0)
  $<.$%(r)
 $! mk($<)
$, simult(A,b):
 a=$T(A)
 n=$0(a)
 bb=$T(tomat(b))if ismat(b)$&[[v]$) v in b[1:]]
 if $0(bb)!=n:
  bb=$T(transpose(b))
 k=$0(bb[0])
 R=$T(rref(mk([a[i]+bb[i]$) i in $*(n)])))
 $) i in $*(n):
  if iszero(R[i][i]):
   err("Singular matrix")
 $! mk([[nice(R[i][n+j])$) j in $*(k)]$) i in $*(n)])
$, cumsum(L):
 if $^(L):
  $<=[]
  s=0
  $) v in L[1:]:
   s=$d(s,v)
   $<.$%(s)
  $! lst($<)
 a=$T(L)
 $<=[]
 acc=[0]*$0(a[0])
 $) r in a:
  acc=[$d(acc[j],r[j])$) j in $*($0(r))]
  $<.$%($I(acc))
 $! mk($<)
$, polar_vec(u):
 v=vec(u)
 if $0(v)==2:
  r=nice($L(ac($d(pw(v[0],2),pw(v[1],2)))))
  th=fn('$s',$d(v[0],$:('i',v[1])))
  $!('$p','['+fmtx(r)+' \u2220'+fmtx(th)+']')
 err("Dimension error")
$, fmtx(e):
 $! fmt(e)
$, cylind(u):
 v=vec(u)
 if $0(v)!=3:
  err("Dimension error")
 r=nice($L(ac($d(pw(v[0],2),pw(v[1],2)))))
 th=fn('$s',$d(v[0],$:('i',v[1])))
 $!('$p','['+fmtx(r)+' \u2220'+fmtx(th)+' '+fmtx(v[2])+']')
$, sphere(u):
 v=vec(u)
 if $0(v)!=3:
  err("Dimension error")
 rho=nice($L(ac($d(pw(v[0],2),pw(v[1],2),pw(v[2],2)))))
 th=fn('$s',$d(v[0],$:('i',v[1])))
 ph=fn('arccos',$Z(v[2],rho))if rho!=0 $& 0
 $!('$p','['+fmtx(rho)+' \u2220'+fmtx(th)+' \u2220'+fmtx(ph)+']')
$, lsum(L,a=1,b=$#):
 xs=$I(L[1:])
 if b is $#:
  b=$0(xs)
 $! $8(xs[a-1:b])
$, lprod(L,a=1,b=$#):
 xs=$I(L[1:])
 if b is $#:
  b=$0(xs)
 $! $H(xs[a-1:b])
$, mean(L,F=$#):
 xs=$I(L[1:])
 if F is $#:
  $! $Z($8(xs),$0(xs))
 fs=$I(F[1:])
 $! $Z($8([$:(xs[i],fs[i])$) i in $*($0(xs))]),$8(fs))
$, sortkey(v):
 try:
  x=$V(v)
  $! x.$S if $/(x)is $1 $& x
 $6 $>:
  $! 0.0
$, median(L):
 xs=sorted($I(L[1:]),key=sortkey)
 n=$0(xs)
 if n%2:
  $! xs[n//2]
 $! $Z($d(xs[n//2-1],xs[n//2]),2)
$, variance(L,pop=$2):
 xs=$I(L[1:])
 n=$0(xs)
 m=mean(L)
 s=$8([pw($c(v,m),2)$) v in xs])
 $! ac($Z(s,n if pop $& n-1))
$, stddev(L,pop=$2):
 $! nice($L(variance(L,pop)))
$, sorta(L):
 $! lst(sorted($I(L[1:]),key=sortkey))
$, sortd(L):
 $! lst(sorted($I(L[1:]),key=sortkey,reverse=$A))
$, deltalist(L):
 xs=$I(L[1:])
 $! lst([$c(xs[i+1],xs[i])$) i in $*($0(xs)-1)])
''')
_x(r'''SET={'$s':'rad','mode':'auto','$E':'$S'}
$, lmap(f,a):
 if $^(a):
  $!('$I',)+$3(lmap(f,v)$) v in a[1:])
 if ismat(a):
  $!('mat',)+$3(lmap(f,r)$) r in a[1:])
 $! f(a)
$, lmap2(f,a,b):
 if $^(a)$+ $^(b):
  if $0(a)!=$0(b):
   err("Dimension error")
  $!('$I',)+$3(lmap2(f,a[i],b[i])$) i in $*(1,$0(a)))
 if $^(a):
  $!('$I',)+$3(lmap2(f,v,b)$) v in a[1:])
 if $^(b):
  $!('$I',)+$3(lmap2(f,a,v)$) v in b[1:])
 if ismat(a)$+ ismat(b):
  $!('mat',)+$3(lmap2(f,a[i],b[i])$) i in $*(1,$0(a)))
 if ismat(a):
  $!('mat',)+$3(lmap2(f,r,b)$) r in a[1:])
 if ismat(b):
  $!('mat',)+$3(lmap2(f,a,r)$) r in b[1:])
 $! f(a,b)
$, vadd(a,b):
 if ismat(a)$+ ismat(b):
  $! m_add(a,b)
 if $^(a)or $^(b)or ismat(a)or ismat(b):
  $! lmap2($d,a,b)
 if isrel(a)or isrel(b):
  $! relop($d,a,b)
 if isstr(a)or isstr(b):
  err("Data $/ error")
 $! $d(a,b)
$, vsub(a,b):
 $! vadd(a,vneg(b))
$, vneg(a):
 $! lmap($r,a)if $- isrel(a)$&(a[0],$r(a[1]),$r(a[2]))
$, vmul(a,b):
 if ismat(a)$+ ismat(b):
  $! m_mul(a,b)
 if ismat(a)$+ $^(b)or $^(a)$+ ismat(b):
  $! m_mul(tomat(a),tomat(b)if ismat(b)$& transpose(b))
 if $^(a)or $^(b)or ismat(a)or ismat(b):
  $! lmap2($:,a,b)
 if isrel(a)or isrel(b):
  $! relop($:,a,b)
 $! $:(a,b)
$, vdiv(a,b):
 if ismat(b):
  if ismat(a):
   $! m_mul(a,m_inv(b))
  $! vmul(a,m_inv(b))
 if $^(a)or $^(b)or ismat(a):
  $! lmap2($Z,a,b)
 if isrel(a)or isrel(b):
  $! relop($Z,a,b)
 if b==0 $+ $7(a):
  $! '$M'
 $! $Z(a,b)
$, vpow(a,b):
 if ismat(a):
  if $/(b)is $t:
   $! m_pow(a,b)
  if b=='T_t':
   $! transpose(a)
  err("Domain error")
 if $^(a)or $^(b):
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
 $! $((e,'$p')
$, dotop(op,a,b):
 if op=='.*':
  $! lmap2($:,a,b)
 if op=='./':
  $! lmap2($Z,a,b)
 $! lmap2(pw,a,b)
$, rel(op,a,b):
 if $^(a)or $^(b):
  $! lmap2($5 x,y:rel(op,x,y),a,b)
 if isstr(a)$+ isstr(b):
  r=cmpstr(op,a[1],b[1])
  if r is $- $#:
   $! 'true' if r $& 'false'
 d=$.($c(a,b))if $-(isstr(a)or isstr(b))$& $#
 if d is $- $# $+ $7(d)$+ d!='$M':
  try:
   v=$V(d)
  $6 $>:
   v=$#
  if v is $- $#:
   if $/(v)is $1:
    if op=='=':
     $! 'true' if $J(v)<1e-13 $& 'false'
    if op=='/=':
     $! 'false' if $J(v)<1e-13 $& 'true'
    err("Non-$S comparison")
   if d==0 or $J(v)<1e-300:
    v=0.0
   r={'=':v==0,'/=':v!=0,'<':v<0,'>':v>0,'<=':v<=0,'>=':v>=0}[op]
   $! 'true' if r $& 'false'
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
 $! flat('$+',a,b)
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
   xs.${(v[1:])
  $&:
   xs.$%(v)
 $!(op,)+$3(xs)
$, lnot(a):
 t=tobool(a)
 if t is $- $#:
  $! 'false' if t $& 'true'
 if $k(a):
  $!~a
 neg_={'<':'>=','>':'<=','<=':'>','>=':'<','=':'/=','/=':'='}
 if isrel(a):
  $!(neg_[a[0]],a[1],a[2])
 $!('$-',a)
$, lxor(a,b):
 ta=tobool(a)
 tb=tobool(b)
 if ta is $- $# $+ tb is $- $#:
  $! 'true' if ta!=tb $& 'false'
 if $k(a)$+ $k(b):
  $! a^b
 $!('xor',a,b)
$, need_int(n):
 if isfl(n)$+ finite(n)$+ n==$U.floor(n):
  $! $t(n)
 if $- $k(n):
  err("Argument must be an integer")
 $! n
$, gcd_(a,b):
 if $q(a)$+ $q(b):
  an,ad=nd(a)
  bn,bd=nd(b)
  $! Q(igcd(an,bn),ilcm(ad,bd))
 if isfl(a)or isfl(b):
  $! $F(igcd($t(a),$t(b)))
 $! poly_gcd_expr(a,b)
$, lcm_(a,b):
 if $q(a)$+ $q(b):
  an,ad=nd(a)
  bn,bd=nd(b)
  $! Q(ilcm(an,bn),igcd(ad,bd))
 g=gcd_(a,b)
 $! $.($Z($:(a,b),g))
$, mod_(a,b):
 if $((a,'^')$+ $k(a[1])$+ $k(a[2])$+ a[2]>0 $+ $k(b)$+ b!=0:
  r=powmod(a[1],a[2],$J(b))
  $! r-$J(b)if b<0 $+ r $& r
 if $D(a)$+ $D(b):
  if b==0:
   $! a
  $! nsub(a,nmul(b,nfloor(ndiv(a,b))))
 $!('mod',a,b)
$, remain_(a,b):
 if $D(a)$+ $D(b):
  if b==0:
   $! a
  q=ndiv(a,b)
  t=nfloor(q)if $b(q)>=0 $&-nfloor(nneg(q))
  $! nsub(a,nmul(b,t))
 $!('remain',a,b)
$, intdiv_(a,b):
 q=ndiv(a,b)
 if $b(q)>=0:
  $! nfloor(q)
 $!-nfloor(nneg(q))
$, bigcomb(n,k):
 if $-($k(n)$+ $k(k))or k<=0:
  $! $2
 m=min(k,$J(n-k))if n>=k $& k
 $! m*ibits(n)>MAXBITS
$, ncr_(n,k):
 if $k(n)$+ $k(k):
  if k<0 or(n>=0 $+ k>n):
   $! 0
  if bigcomb(n,k):
   $!('ncr',n,k)
  $! binom(n,k)if n>=0 $& gen_ncr(n,k)
 if $k(k)$+ k>=0:
  $! gen_ncr(n,k)
 if isfl(n)or isfl(k):
  $! CA_gamma_ratio(n,k)
 $!('ncr',n,k)
$, gen_ncr(n,k):
 r=1
 $) i in $*(k):
  r=$:(r,$c(n,i))
 f=1
 $) i in $*(2,k+1):
  f*=i
 $! $:(r,Q(1,f))
$, npr_(n,k):
 if $k(n)$+ $k(k)$+ k*ibits(n)>MAXBITS:
  $!('npr',n,k)
 if $k(k)$+ k>=0:
  r=1
  $) i in $*(k):
   r=$:(r,$c(n,i))
  $! r
 $!('npr',n,k)
$, CA_gamma_ratio(n,k):
 n=tofl(n)
 k=tofl(k)
 $! gamma(n+1)/(gamma(k+1)*gamma(n-k+1))
''')
_x(r'''$, isprime_(n):
 n=need_int(n)
 if $J(n)>>1024:
  err('Number too large $) isPrime')
 $! 'true' if isprime($J(n))$& 'false'
$, round_(x,d=0):
 if $7(x)$+ $- $D(x):
  x=evalf(x)
 if $D(x):
  if $q(x)$+ d==0:
   $! nfloor(nadd(x,HALF))if $b(x)>=0 $&-nfloor(nadd(nneg(x),HALF))
  v=tofl(x)
  if $- finite(v):
   $! x
  p=10.0**d
  r=$U.floor($J(v)*p+0.5)/p
  $! r if v>=0 $&-r
 $!('round',x,d)
$, ipart_(x):
 if $7(x)$+ $- $D(x):
  x=evalf(x)
 if $D(x):
  if $/(x)is $F:
   $! $F($t(x))
  $! nfloor(x)if $b(x)>=0 $&-nfloor(nneg(x))
 $!('ipart',x)
$, fpart_(x):
 i=ipart_(x)
 if $((i,'ipart'):
  $!('fpart',x)
 $! $c(x,i)
$, approx_(e):
 $! evalf(e)
$, exact_(e,tol=$#):
 if tol is $- $#:
  tol=tofl(tol)
 $! exactify(e,tol)
$, approxfraction(e,tol=$#):
 t=tofl(tol)if tol is $- $# $& 5e-14
 $! lmap($5 v:float2rat(tofl(evalf(v)),t)if $7(v)$& exactify(v,t),e)
$, left_(e,n=$#):
 if isrel(e):
  $! e[1]
 if $^(e):
  $!('$I',)+e[1:1+n]
 if isstr(e):
  $!('$p',e[1][:n])
 err("Argument error")
$, right_(e,n=$#):
 if isrel(e):
  $! e[2]
 if $^(e):
  $!('$I',)+(e[$0(e)-n:]if n $&())
 if isstr(e):
  $!('$p',e[1][$0(e[1])-n:]if n $& '')
 err("Argument error")
$, mid_(e,start,n=$#):
 if isstr(e):
  s=e[1][start-1:]
  $!('$p',s if n is $# $& s[:n])
 xs=$I(e[1:])[start-1:]
 $!('$I',)+$3(xs if n is $# $& xs[:n])
$, dim_(e):
 if $^(e):
  $! $0(e)-1
 if ismat(e):
  r,c=dims(e)
  $!('$I',r,c)
 if isstr(e):
  $! $0(e[1])
 err("Argument error")
$, max_(a,b=$#):
 if b is $#:
  xs=$I(a[1:])if $^(a)$&[a]
  $! maxexpr(xs)
 $! lmap2($5 x,y:x if cmpv(x,y)>=0 $& y,a,b)
$, min_(a,b=$#):
 if b is $#:
  xs=$I(a[1:])if $^(a)$&[a]
  best=$#
  bv=$#
  $) x in xs:
   v=$V(x)
   if best is $# or v<bv:
    best=x
    bv=v
  $! best
 $! lmap2($5 x,y:x if cmpv(x,y)<=0 $& y,a,b)
$, cmpv(x,y):
 if $7(x)$+ $7(y):
  d=$V($c(x,y))
  d=d.$S if $/(d)is $1 $& d
  $! 1 if d>0 $&(-1 if d<0 $& 0)
 err("Cannot compare")
$, when_(c,a,b=$#,u=$#):
 t=tobool(c)
 if t is $A:
  $! a
 if t is $2:
  $! b if b is $- $# $& '$M'
 if b is $#:
  $!('when',c,a)
 if u is $#:
  $!('when',c,a,b)
 $! u
$, piecewise_(*a):
 a=$I(a)
 if $0(a)%2==1:
  r=a[-1]
  a=a[:-1]
 $&:
  r='$M'
 $) i in $*($0(a)-2,-1,-2):
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
  r=$d($:(r,x),c)
 $! $=(r)
$, randpoly(v,n):
 import random
 $! $8([$:(random.randint(-9,9),pw(v,k))$) k in $*(n+1)])
$, randmat(r,c):
 import random
 $! mk([[random.randint(-9,9)$) _ in $*(c)]$) _ in $*(r)])
$, newmat(r,c):
 $! mk([[0]*c $) _ in $*(r)])
$, newlist(n):
 $!('$I',)+(0,)*n
$, rand_(n=$#):
 import random
 if n is $#:
  $! random.random()
 $!('$I',)+$3(random.random()$) _ in $*(n))
$, randint_(a,b,n=$#):
 import random
 if n is $#:
  $! random.randint(a,b)
 $!('$I',)+$3(random.randint(a,b)$) _ in $*(n))
$, count_(*$N):
 n=0
 $) a in $N:
  n+=($0(a)-1)if $^(a)$& 1
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
    $R
  $! 2/$U.$L($U.pi)*s
 z=$J(x)
 t=0.0
 $) k in $*(60,0,-1):
  t=(k/2.0)/(z+t)
 erfc=$U.exp(-z*z)/$U.$L($U.pi)/(z+t)
 $!(1-erfc)if x>0 $&(erfc-1)
$, numarg(v):
 if v=='$[':
  $! $F('$[')
 if v==('*',-1,'$['):
  $! $F('-$[')
 if $7(v):
  x=cv(v)if $- $D(v)$& tofl(v)
  if x is $- $# $+ $/(x)is $- $1:
   $! x
 err('Numeric argument required')
$, normcdf(lo,hi,mu=0.0,sig=1.0):
 mu=numarg(mu)
 sig=numarg(sig)
 $, F(v):
  if v=='$[':
   $! 1.0
  if v==('*',-1,'$['):
   $! 0.0
  z=(numarg(v)-mu)/sig
  $! 0.5*(1+erf(z/$U.$L(2)))
 $! F(hi)-F(lo)
$, normpdf(x,mu=0.0,sig=1.0):
 x=numarg(x)
 s=numarg(sig)
 $! $U.exp(-0.5*((x-numarg(mu))/s)**2)/(s*$U.$L(2*$U.pi))
$, invnorm(p,mu=0.0,sig=1.0):
 p=numarg(p)
 mu=numarg(mu)
 sig=numarg(sig)
 if $- 0<p<1:
  err('Area must be between 0 $+ 1')
 lo,hi=-40.0,40.0
 $) _ in $*(200):
  m=0.5*(lo+hi)
  if 0.5*(1+erf(m/$U.$L(2)))<p:
   lo=m
  $&:
   hi=m
 $! mu+sig*0.5*(lo+hi)
$, binompdf(n,p,x=$#):
 if x is $#:
  $!('$I',)+$3(binompdf(n,p,k)$) k in $*(n+1))
 if $q(p):
  $! $:(binom(n,x),pw(p,x),pw($c(1,p),n-x))
 p=tofl(p)
 $! binom(n,x)*p**x*(1-p)**(n-x)
$, binomcdf(n,p,a,b=$#):
 if b is $#:
  a,b=0,a
 $! $8([binompdf(n,p,k)$) k in $*($t(a),$t(b)+1)])
$, poisspdf(lam,x):
 $! evalf($:(pw(lam,x),pw('e',$r(lam)),Q(1,fact_int(x))))
$, poisscdf(lam,a,b=$#):
 if b is $#:
  a,b=0,a
 $! $8([poisspdf(lam,k)$) k in $*($t(a),$t(b)+1)])
$, geompdf(p,x):
 $! $:(p,pw($c(1,p),x-1))
$, geomcdf(p,a,b=$#):
 if b is $#:
  a,b=1,a
 $! $8([geompdf(p,k)$) k in $*($t(a),$t(b)+1)])
$, fact_int(n):
 r=1
 $) k in $*(2,n+1):
  r*=k
 $! r
$, toang(x):
 a=SET['$s']
 if a=='deg':
  $! $:(x,$Z('pi',180))
 if a=='grad':
  $! $:(x,$Z('pi',200))
 $! x
$, fromang(x):
 a=SET['$s']
 if a=='deg':
  $! $=($:(x,$Z(180,'pi')))
 if a=='grad':
  $! $=($:(x,$Z(200,'pi')))
 $! x
TRIG=('sin','cos','tan','sec','csc','cot')
ITRIG=('$w','arccos','$u','arcsec','arccsc','arccot')
''')
_x(r'''$, mathfn($B):
 $, f(*a):
  if $B in TRIG $+ SET['$s']!='rad':
   $! lmap($5 u:fn($B,toang(u)),a[0])
  if $B in ITRIG $+ SET['$s']!='rad':
   $! lmap($5 u:fromang(fn($B,u)),a[0])
  if $0(a)==1:
   $! lmap($5 u:fn($B,u),a[0])
  $! fn($B,*a)
 $! f
$, angle_fn(z):
 $! lmap($5 u:fromang(fn('$s',u)),z)
F={}
$) _n in('sin','cos','tan','sec','csc','cot','$w','arccos',
 '$u','arcsec','arccsc','arccot','sinh','cosh','tanh',
 'sech','csch','coth','arcsinh','arccosh','arctanh',
 'arcsech','arccsch','arccoth','ln','exp','$J','sign',
 'floor','ceiling','$S','imag','conj','fact'):
 F[_n]=mathfn(_n)
ALIAS={'asin':'$w','acos':'arccos','atan':'$u','asinh':'arcsinh',
 'acosh':'arccosh','atanh':'arctanh','ceil':'ceiling',
 'factorial':'fact','derivative':'d','$j':'$j',
 'int_':'$j','sumseq':'sumseq','prodseq':'prodseq',
 'lim':'limit','nderiv':'nderivative','polycoef':'polycoeffs',
 'stddevsamp':'stddev','varsamp':'variance','cumsum':'cumulativesum',
 'nsolve':'nsolve','arg':'$s','inv':'inverse','mat2list':'matlist',
 'list2mat':'listmat','explist':'explist','tran':'transpose',
 'log10':'log10','sqr':'$L'}
F['$L']=$5 u:lmap($L,u)
F['root']=$5 u,n=2:lmap($5 v:fn('root',v,n),u)
F['log']=$5 u,b=$#:lmap($5 v:fn('ln',v)if b is $# $& fn('log',v,b),u)
F['atan2']=$5 y,x:lmap2($5 b,a:fromang(fn('$s',$d(a,$:('i',b)))),y,x)
F['log10']=$5 u:lmap($5 v:fn('log',v,10),u)
F['$s']=angle_fn
F['round']=$5 x,d=0:lmap($5 v:round_(v,d),x)
F['ipart']=$5 x:lmap(ipart_,x)
F['$t']=$5 x:lmap($5 v:fn('floor',v),x)
F['fpart']=$5 x:lmap(fpart_,x)
F['gcd']=$5 a,b:lmap2(gcd_,a,b)
F['lcm']=$5 a,b:lmap2(lcm_,a,b)
F['mod']=$5 a,b:lmap2(mod_,a,b)
F['remain']=$5 a,b:lmap2(remain_,a,b)
F['intdiv']=$5 a,b:lmap2(intdiv_,a,b)
F['ncr']=$5 a,b:lmap2(ncr_,a,b)
F['npr']=$5 a,b:lmap2(npr_,a,b)
F['isprime']=isprime_
F['approx']=approx_
F['exact']=exact_
F['approxrational']=approxfraction
F['getnum']=$5 e:lmap(getnum,e)
F['getdenom']=$5 e:lmap(getden,e)
F['polyeval']=polyeval
F['polygcd']=$5 a,b:poly_gcd_expr(a,b)
F['randpoly']=randpoly
F['texpand']=$5 e:lmap($5 v:texpand(v),e)
F['tcollect']=$5 e:lmap($5 v:tcollect(v),e)
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
F['rref']=$5 A,tol=$#:rref(A,$A)
F['ref']=$5 A,tol=$#:ref_(A)
F['inverse']=m_inv
F['rowdim']=$5 A:dims(A)[0]
F['coldim']=$5 A:dims(A)[1]
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
F['lu']=$5 A,tol=$#:('$I',)+lu(A)
F['qr']=$5 A,tol=$#:('$I',)+qr(A)
F['newmat']=newmat
F['newlist']=newlist
F['randmat']=randmat
F['matlist']=matlist
F['listmat']=listmat
F['simult']=simult
F['cumulativesum']=cumsum
F['sum']=$5 L,a=1,b=$#:lsum(L,a,b)if $^(L)$& colwise(L,lsum)
F['product']=$5 L,a=1,b=$#:lprod(L,a,b)if $^(L)$& colwise(L,lprod)
F['mean']=$5 L,f=$#:mean(L,f)if $^(L)$& colwise(L,mean)
F['median']=median
F['stddev']=$5 L:stddev(L)
F['stddevpop']=$5 L:stddev(L,$A)
F['variance']=$5 L:variance(L)
F['varpop']=$5 L:variance(L,$A)
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
F['getmode']=$5*a:('$p','$s='+SET['$s']+' mode='+SET['mode']+' $E='+SET['$E'])
$, colwise(M,f):
 cols=$T(transpose(M))
 $! mk([[f(('$I',)+$3(c))$) c in cols]])
$, ref_(A):
 $! rref(A,$2)
$, conv(e,$B,$N):
 if $B=='decimal':
  $! evalf(e)
 if $B=='approxfraction':
  $! approxfraction(e,$N[0]if $N $& $#)
 if $B in('dms','dd','rad','grad','deg'):
  $! angconv(e,$B)
 if $B=='polar':
  if $^(e)or ismat(e):
   $! polar_vec(e)
  r=$.(fn('$J',e))
  th=fn('$s',e)
  $!('$p','('+fmt(r)+'\u2220'+fmt(fromang(th))+')')
 if $B=='rect':
  if $^(e)or ismat(e):
   $! e
  r,i=reim(e)
  $! $d(r,$:('i',i))
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
  $! tologbase(e,$N[0])
 if $B=='sin':
  $! pyth_to(e,'sin')
 if $B=='cos':
  $! pyth_to(e,'cos')
 err("Unknown conversion "+$B)
$, angconv(e,$B):
 if $B=='dms':
  v=tofl(evalf(e))
  if SET['$s']=='rad':
   v=v*180/$U.pi
  $? SET['$s']=='grad':
   v=v*0.9
  sg='-' if v<0 $& ''
  v=$J(v)
  d=$t(v)
  m=$t((v-d)*60)
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
  if SET['$s']=='rad':
   $! evalf($:(e,$Z(180,'pi')))
  $! evalf(e)
 if $B=='rad':
  if SET['$s']=='deg':
   $! $:(e,$Z('pi',180))
  if SET['$s']=='grad':
   $! $:(e,$Z('pi',200))
  $! e
 if $B=='grad':
  if SET['$s']=='deg':
   $! $:(e,Q(10,9))
  if SET['$s']=='rad':
   $! $:(e,$Z(200,'pi'))
  $! e
 if SET['$s']=='rad':
  $! $:(e,$Z(180,'pi'))
 $! e
''')
_x(r'''$, baseconv(e,$B):
 n=need_int(e)
 if $B=='base10':
  $! n
 if $B=='base2':
  s=bin(n)if n>=0 $& '-'+bin(-n)
  $!('$p',s.replace('0b','0b'))
 s=hex(n)if n>=0 $& '-'+hex(-n)
 $!('$p',s.replace('0x','0h').upper().replace('0H','0h'))
$, toexp(e):
 if $/(e)is $- $3 or e[0]=='Q':
  $! e
 $N=[toexp(a)$) a in e[1:]]
 h=e[0]
 if $0($N)==1:
  u=$N[0]
  if h=='sinh':
   $! $:(HALF,$c(pw('e',u),pw('e',$r(u))))
  if h=='cosh':
   $! $:(HALF,$d(pw('e',u),pw('e',$r(u))))
  if h=='tanh':
   $! $Z($c(pw('e',u),pw('e',$r(u))),$d(pw('e',u),pw('e',$r(u))))
  if h=='sin':
   iu=$:('i',u)
   $! $Z($c(pw('e',iu),pw('e',$r(iu))),$:(2,'i'))
  if h=='cos':
   iu=$:('i',u)
   $! $:(HALF,$d(pw('e',iu),pw('e',$r(iu))))
  if h=='arcsinh':
   $! fn('ln',$d(u,$L($d(pw(u,2),1))))
  if h=='arccosh':
   $! fn('ln',$d(u,$L($c(pw(u,2),1))))
  if h=='arctanh':
   $! $:(HALF,fn('ln',$Z($d(1,u),$c(1,u))))
 $! simp((h,)+$3($N))
$, toln(e):
 if $/(e)is $- $3 or e[0]=='Q':
  $! e
 $N=[toln(a)$) a in e[1:]]
 if e[0]=='log':
  b=$N[1]if $0($N)>1 $& 10
  $! $Z(fn('ln',$N[0]),fn('ln',b))
 $! simp((e[0],)+$3($N))
$, tologbase(e,b):
 e=toln(e)
 $, walk(t):
  if $/(t)is $- $3 or t[0]=='Q':
   $! t
  if t[0]=='ln':
   $! $Z(('log',walk(t[1]),b),('log','e',b))
  $!(t[0],)+$3(walk(a)$) a in t[1:])
 $!('hold',walk(e))
''')
_x(r'''VERSION='1.0'
ENV={}
UFUN={}
ASSUME=[]
STATE={'ans':0,'$E':$2,'tmpf':[]}
COMPLEXF=('csolve','czeros','cfactor','cpolyroots','eigvl','eigvc','conj',
 '$S','imag','$s')
$, isfunc(n):
 $!(n in F or n in SF or n in UFUN or n in ALIAS
 or n in STATE['tmpf']or n in('expr','$L','log','root'))
$, lookup(n):
 if n in ENV:
  $! ENV[n]
 if n=='ans':
  $! STATE['ans']
 if n=='i':
  STATE['$E']=$A
 $! n
$, ev(t):
 tt=$/(t)
 if tt is $t or tt is $F:
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
 if h=='$r':
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
  $! lmap($5 a:fn('fact',a),ev(t[1]))
 if h=='%':
  $! lmap($5 a:$Z(a,100),ev(t[1]))
 if h=='deg':
  v=ev(t[1])
  if SET['$s']=='rad':
   $! lmap($5 a:$:(a,$Z('pi',180)),v)
  if SET['$s']=='grad':
   $! lmap($5 a:$:(a,Q(10,9)),v)
  $! v
 if h in('=','<','>','<=','>=','/='):
  $! rel(h,ev(t[1]),ev(t[2]))
 if h=='$+':
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
  $!('$I',)+$3(ev(a)$) a in t[1:])
 if h=='mat':
  $!('mat',)+$3(('$I',)+$3(ev(a)$) a in r[1:])$) r in t[1:])
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
  $!('call',t[1]+"'"*t[2])+$3(ev(a)$) a in t[3:])
 if h=='polar':
  STATE['$E']=$A
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
 if $((c,'$+'):
  $! split_and(c[1])+split_and(c[2])
 $![c]
$, ev_with(t):
 conds=split_and(t[2])
 pairs={}
 ineq=[]
 $) c in conds:
  if $((c,'=')$+ $/(c[1])is $p:
   pairs[c[1]]=ev(c[2])
  $&:
   v=evw(c,$I(pairs.keys()))
   if $((v,'$+'):
    ineq.${($I(v[1:]))
   $? v!='true':
    ineq.$%(v)
 n0=$0(ASSUME)
 ASSUME.${(ineq)
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
 if $/(a)is $p $+ b==0:
  v=a
  pos=h in('>','>=')
 $? $/(b)is $p $+ a==0:
  v=b
  pos=h in('<','<=')
 $&:
  $! r
 rep=v if pos $& $r(v)
 r=$Y(r,('$J',v),rep)
 r=$Y(r,('sign',v),1 if pos $&-1)
 $! r
$, target_fn(t):
 if $((t,'call'):
  $! t[1],[p $) p in t[2:]]
 if $((t,'*')$+ $/(t[1])is $p:
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
 if $((a,'$I'):
  i=idx[0]
  if $- $k(i)or i<1 or i>=$0(a):
   err('Invalid index')
  $! a[i]
 if $((a,'mat'):
  $) k in idx:
   if $- $k(k)or k<1:
    err('Invalid index')
  if $0(idx)==1:
   if $0(a)==2:
    if idx[0]>=$0(a[1]):
     err('Invalid index')
    $! a[1][idx[0]]
   if idx[0]>=$0(a):
    err('Invalid index')
   $!('mat',a[idx[0]])
  if idx[0]>=$0(a)or idx[1]>=$0(a[idx[0]]):
   err('Invalid index')
  $! a[idx[0]][idx[1]]
 if $((a,'$p'):
  k=idx[0]
  if $0(idx)!=1 or $- $k(k)or k<1 or k>$0(a[1]):
   err('Invalid index')
  $!('$p',a[1][k-1])
 err('Invalid index')
$, ev_conv(t):
 e=t[1]
 $B=t[2]
 $N=[ev(a)$) a in t[3:]]
 if $B=='$I':
  if e=='exp':
   $! explist($N[0],$N[1])
  if e=='mat':
   $! matlist($N[0])
  err('Unknown conversion')
 if $B=='mat' $+ e=='$I':
  $! listmat(*$N)
 v=ev(e)
 v=finalize(v,$A)
 $! builtin($B,conv,(v,$B,$N))
$, explist(e,v):
 $<=[]
 parts=e[1:]if $((e,'or')$&(e,)
 $) p in parts:
  if $((p,'=')$+ p[1]==v:
   $<.$%(p[2])
 $!('$I',)+$3($<)
$, call($B,raw):
 $B=ALIAS.get($B,$B)
 if $B in UFUN:
  params,body=UFUN[$B]
  $N=[ev(a)$) a in raw]
  if $0($N)!=$0(params):
   err('Wrong number of arguments')
  $! subsd(body,dict(zip(params,$N)))
 f=SF.get($B)
 if f is $- $#:
  if $B in COMPLEXF:
   STATE['$E']=$A
  $! builtin($B,f,(raw,))
 f=F.get($B)
 if f is $- $#:
  $N=[ev(a)$) a in raw]
  if $B in COMPLEXF:
   STATE['$E']=$A
  $! builtin($B,f,$N)
 if $B=='expr':
  s=ev(raw[0])
  $! ev(parse(s[1],isfunc))
 $N=[ev(a)$) a in raw]
 $!('call',$B)+$3($N)
''')
_x(r'''$, builtin($B,f,$N):
 try:
  $! f(*$N)
 $6 TypeError as ex:
  msg=$p(ex)
  if 'positional' in msg or 'takes' in msg or 'required' in msg or 'missing' in msg:
   err('Wrong number of arguments $) '+$B)
  err('Invalid argument $) '+$B)
 $6(IndexError,$P,AttributeError,KeyError):
  err('Invalid argument $) '+$B)
 $6 $W:
  err('Number too large in '+$B)
$, var_of(raw):
 if $/(raw)is $p:
  $! raw,$#
 if $((raw,'='):
  if $/(raw[1])is $- $p:
   err('Variable expected')
  $! raw[1],ev(raw[2])
 err('Variable expected')
$, $y(a,lo,hi):
 if $0(a)<lo or $0(a)>hi:
  err('Wrong number of arguments')
$, $e(a,k=1):
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
 $y(a,2,3)
 e,v,val=$e(a)
 n=ev(a[2])if $0(a)>2 $& 1
 if $- $k(n):
  err('Order must be an integer')
 r=lmap($5 u:nice(diff(u,v,n)),e)
 $! post_subst(r,v,val)
$, sf_int(a):
 $y(a,2,4)
 e,v,val=$e(a)
 if $0(a)==2:
  $! lmap($5 u:nice(integrate(u,v)),e)
 if $0(a)==3:
  c=ev(a[2])
  $! lmap($5 u:$d(nice(integrate(u,v)),c),e)
 lo=ev(a[2])
 hi=ev(a[3])
 $! lmap($5 u:nice(defint(u,v,lo,hi)),e)
$, sf_limit(a):
 $y(a,3,4)
 e,v,val=$e(a)
 pt=ev(a[2])
 dirn=0
 if $0(a)>3:
  d=ev(a[3])
  if $- $D(d):
   err('Direction must be -1, 0 or 1')
  dirn=0 if d==0 $&(1 if $b(d)>0 $&-1)
 $, L(u):
  r=limit(u,v,pt,dirn)
  if $((r,'limit'):
   $!('limit',u,v,pt)if dirn==0 $&('limit',u,v,pt,dirn)
  $! nice(r)
 $! lmap(L,e)
$, cs_bounds(a,i):
 $! ev(a[i]),ev(a[i+1])
$, sf_sum(a):
 $y(a,4,4)
 e,v,val=$e(a)
 lo,hi=cs_bounds(a,2)
 r=sumseq(e,v,lo,hi)
 $! prefer_fact(nice(r))
$, prefer_fact(r):
 if $((r,'+')$+ $- $a(r)$+ $0($l(r))==1:
  try:
   f=$z(r)
   if $((f,'hold')$+ $((f[1],'*'):
    $! f
  $6 $>:
   pass
 $! r
$, sf_prod(a):
 $y(a,4,4)
 e,v,val=$e(a)
 lo,hi=cs_bounds(a,2)
 $! prodseq(e,v,lo,hi)
$, sf_seq(a):
 $y(a,4,5)
 e,v,val=$e(a)
 lo,hi=cs_bounds(a,2)
 st=ev(a[4])if $0(a)>4 $& 1
 $<=[]
 k=lo
 cnt=0
 $G ncmp(k,hi)<=0 if $D(k)$& $2:
  $<.$%($Y(e,v,k))
  k=nadd(k,st)
  cnt+=1
  if cnt>5000:
   err('Too many elements')
 $!('$I',)+$3($<)
$, sf_taylor(a):
 $y(a,3,4)
 e,v,val=$e(a)
 n=ev(a[2])
 pt=ev(a[3])if $0(a)>3 $& 0
 $! lmap($5 u:taylor(u,v,n,pt),e)
$, sf_series(a):
 $y(a,3,4)
 e,v,val=$e(a)
 n=ev(a[2])
 pt=ev(a[3])if $0(a)>3 $& 0
 $! lmap($5 u:series_cmd(u,v,n,pt),e)
$, sf_dominant(a):
 $y(a,2,3)
 e,v,val=$e(a)
 pt=ev(a[2])if $0(a)>2 $& 0
 $! lmap($5 u:dominant(u,v,pt),e)
$, solvevars(rawvs):
 vs=[]
 gs=[]
 $) r in rawvs:
  if $((r,'$I'):
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
 if $((e,'$+'):
  $<=[]
  $) p in e[1:]:
   $<.${(eqlist(p))
  $! $<
 if $((e,'$I'):
  $! $I(e[1:])
 $![e]
$, cons_for(v):
 $<=[]
 $) c in ASSUME:
  if has(c,v):
   $<.$%(c)
 $! $<
$, sf_solve(a,$E=$2):
 if $0(a)<2:
  err('Wrong number of arguments')
 vs,gs=solvevars(a[1:])
 e=evw(a[0],vs)
 eqs=eqlist(e)
 if $0(vs)==1 $+ $0(eqs)==1:
  v=vs[0]
  eq=eqs[0]
  if gs[0]is $- $#:
   f=$c(eq[1],eq[2])if $((eq,'=')$& eq
   r=nsolve(f,v,tofl(evalf(gs[0])))
   $!('=',v,r)if r is $- $# $& 'false'
  r=solve(eq,v,$E,cons_for(v))
  if r is $#:
   f=$c(eq[1],eq[2])if $((eq,'=')$& eq
   ns=numeric_solve(f,v,$E)if head(eq)=='=' or head(eq)is $# $& $#
   if ns:
    r=sols_to_bool(v,apply_constraints(ns,v,cons_for(v)))
   $&:
    $!('solve',eq,v)
  $! finish_sol(r)
 $f=solve_system(eqs,vs,$E,gs if any([g is $- $# $) g in gs])$& $#)
 if $f is $#:
  $!('solve',e)+$3(vs)
 if $- $f:
  $! 'false'
 $<=[]
 $) s in $f:
  conj=[('=',v,clean(s.get(v,v)))$) v in vs]
  $<.$%(conj[0]if $0(conj)==1 $&('$+',)+$3(conj))
 $! finish_sol($<[0]if $0($<)==1 $&('or',)+$3($<))
$, finish_sol(r):
 $! r
$, sf_csolve(a):
 $! sf_solve(a,$A)
$, sf_zeros(a,$E=$2):
 $y(a,2,2)
 vs,gs=solvevars(a[1:])
 e=evw(a[0],vs)
 if $0(vs)==1 $+ $- $((e,'$I'):
  r=zeros(e,vs[0],$E,cons_for(vs[0]))
  if r is $#:
   ns=numeric_solve(e,vs[0],$E)
   $!('$I',)+$3(ns or[])
  $! r
 eqs=eqlist(e)
 $f=solve_system(eqs,vs,$E)
 if $- $f:
  $!('$I',)
 $! mk([[clean(s.get(v,v))$) v in vs]$) s in $f])
$, sf_czeros(a):
 $! sf_zeros(a,$A)
$, sf_nsolve(a):
 $y(a,2,4)
 v,g=var_of(a[1])
 e=unhold(evw(a[0],[v]))
 f=$c(e[1],e[2])if $((e,'=')$& e
 lo=tofl(evalf(ev(a[2])))if $0(a)>2 $& $#
 hi=tofl(evalf(ev(a[3])))if $0(a)>3 $& $#
 $) c in cons_for(v):
  b=bounds([c],v)if $2 $& $#
 cb=bounds(cons_for(v),v)
 if cb is $- $#:
  lo,hi=tofl(evalf(cb[0])),tofl(evalf(cb[1]))
 r=nsolve(f,v,tofl(evalf(g))if g is $- $# $& $#,lo,hi)
 if r is $#:
  $!('$p','No solution found')
 $! r
''')
_x(r'''$, sf_desolve(a):
 $y(a,3,3)
 x=a[1]
 y=a[2]
 if $/(x)is $- $p or $/(y)is $- $p:
  err('Variable expected')
 parts=split_and(a[0])
 ode=$#
 conds=[]
 $) p in parts:
  if $((p,'=')$+ $((p[1],'primecall')$+ p[1][1]==y:
   conds.$%((p[1][2],evw(p[1][3],[x,y]),evw(p[2],[x,y])))
  $? $((p,'=')$+ $((p[1],'*')$+ p[1][1]==y $+ $- hasprime(p):
   conds.$%((0,ev(p[1][2]),ev(p[2])))
  $? $((p,'=')$+ $((p[1],'call')$+ p[1][1]==y:
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
 if $/(t)is $- $3:
  $! $2
 if t[0]in('prime','primecall'):
  $! $A
 $) a in t[1:]:
  if hasprime(a):
   $! $A
 $! $2
$, bnd_args(a,i,v):
 lo=ev(a[i])if $0(a)>i $& $#
 hi=ev(a[i+1])if $0(a)>i+1 $& $#
 cb=bounds(cons_for(v),v)
 if cb is $- $#:
  lo,hi=cb
 $&:
  $) c in cons_for(v):
   h=head(c)
   if h in('>','>=')$+ c[1]==v:
    lo=c[2]
   $? h in('<','<=')$+ c[1]==v:
    hi=c[2]
 $! lo,hi
$, sf_fmin(a,kind='min'):
 $y(a,2,4)
 e,v,val=$e(a)
 lo,hi=bnd_args(a,2,v)
 r=fextreme(e,v,kind,lo,hi)
 if r is $#:
  $!('f'+kind,e,v)
 $! r
$, sf_fmax(a):
 $! sf_fmin(a,'max')
$, sf_nfmin(a,kind='min'):
 $y(a,2,4)
 e,v,val=$e(a)
 lo,hi=bnd_args(a,2,v)
 $! nfextreme(e,v,kind,tofl(evalf(lo))if lo is $- $# $& $#,
 tofl(evalf(hi))if hi is $- $# $& $#)
$, sf_nfmax(a):
 $! sf_nfmin(a,'max')
$, sf_nint(a):
 $y(a,4,4)
 e,v,val=$e(a)
 lo,hi=cs_bounds(a,2)
 $! nint(e,v,lo,hi)
$, sf_arclen(a):
 $y(a,4,4)
 e,v,val=$e(a)
 lo,hi=cs_bounds(a,2)
 $! nice(arclen(e,v,lo,hi))
$, pt_arg(a):
 if $0(a)==2 $+ $((a[1],'='):
  v,p=var_of(a[1])
  e=evw(a[0],[v])
  $! e,v,p
 $y(a,3,3)
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
 $y(a,3,4)
 x,_=var_of(a[1])
 y,_=var_of(a[2])
 e=evw(a[0],[x,y])
 n=ev(a[3])if $0(a)>3 $& 1
 $! impdif(e,x,y,n)
$, rc_args(a):
 v,val=var_of(a[1])
 e=unhold(evw(a[0],[v]))
 h=ev(a[2])if $0(a)>2 $& 0.001
 if val is $#:
  val=v
 $! e,v,val,h
$, sf_avgrc(a):
 $y(a,2,3)
 e,v,val,h=rc_args(a)
 $! lmap($5 u:$=(avgrc(u,v,val,h)),e)
$, sf_central(a):
 $y(a,2,3)
 e,v,val,h=rc_args(a)
 $! lmap($5 u:$=(centraldiff(u,v,val,h)),e)
$, sf_nderiv(a):
 $y(a,2,3)
 v,val=var_of(a[1])
 e=unhold(evw(a[0],[v]))
 n=ev(a[2])if $0(a)>2 $& 1
 if val is $#:
  val=ENV.get(v)
  if val is $#:
   err('Value required: var=value')
 $! evalf($Y(diff(e,v,n),v,val))
$, opt_var(a,i):
 if $0(a)>i:
  v,_=var_of(a[i])
  $! v
 $! $#
$, sf_expand(a):
 $y(a,1,2)
 v=opt_var(a,1)
 e=ev(a[0])
 $! expand_full(unhold(e),v)
$, sf_factor(a,$E=$2):
 $y(a,1,2)
 v=opt_var(a,1)
 e=unhold(ev(a[0]))
 $! $z(e,v,$E)
$, sf_cfactor(a):
 $! sf_factor(a,$A)
$, sf_comdenom(a):
 $y(a,1,2)
 $! comdenom(unhold(ev(a[0])))
$, sf_propfrac(a):
 $y(a,1,2)
 v=opt_var(a,1)
 $! lmap($5 u:propfrac(u,v),unhold(ev(a[0])))
$, polyvar(e,a,i):
 v=opt_var(a,i)
 if v is $#:
  ss=$l(e)
  v='x' if 'x' in ss or $- ss $& ss[0]
 $! v
$, sf_polycoeffs(a):
 $y(a,1,2)
 e=unhold(ev(a[0]))
 v=polyvar(e,a,1)
 cs=$_(e,v)
 if cs is $#:
  err('Polynomial expected')
 $G $0(cs)>1 $+ cs[-1]==0:
  cs.pop()
 $!('$I',)+$3(reversed(cs))
$, sf_polydegree(a):
 $y(a,1,2)
 e=unhold(ev(a[0]))
 v=polyvar(e,a,1)
 d=degree($=(e),v)
 if d is $#:
  err('Polynomial expected')
 if e==0:
  $!('*',-1,'$[')
 $! d
$, sf_polyquo(a,which=0):
 $y(a,2,3)
 p=unhold(ev(a[0]))
 q=unhold(ev(a[1]))
 v=polyvar($d(p,q),a,2)
 cp=$_(p,v)
 cq=$_(q,v)
 if cp is $# or cq is $#:
  err('Polynomial expected')
 qq,rr=e_divmod(cp,cq)
 $! fromcoeffs(qq if which==0 $& rr,v)
$, sf_polyrem(a):
 $! sf_polyquo(a,1)
$, sf_polyroots(a,$E=$2):
 $y(a,1,2)
 if $0(a)==1:
  L=ev(a[0])
  if $- $((L,'$I'):
   err('List expected')
  v='X_'
  e=polyeval(L,v)
 $&:
  v,_=var_of(a[1])
  e=evw(a[0],[v])
 r=zeros(e,v,$E)
 $! r if r is $- $# $&('$I',)
$, sf_cpolyroots(a):
 $! sf_polyroots(a,$A)
$, sf_linsolve(a):
 vs,gs=solvevars(a[1:])
 e=evw(a[0],vs)
 eqs=eqlist(e)
 fs=[eqexpr(q)$) q in eqs]
 if $- is_linear_sys(fs,vs):
  err('Argument error: $h system required')
 $f=linsys(fs,vs)
 if $- $f:
  $! 'false'
 $!('$I',)+$3($f[0][v]$) v in vs)
$, sf_domain(a):
 $y(a,2,2)
 e,v,val=$e(a)
 r=domain(e,v)
 $! r if r is $- $# $&('domain',e,v)
$, sf_completesq(a):
 $y(a,2,2)
 v,_=var_of(a[1])
 e=unhold(evw(a[0],[v]))
 if $((e,'='):
  lhs=complete_sq($c(e[1],e[2]),v,$A)
  $! lhs
 $! complete_sq(e,v,$2)
$, complete_sq(e,v,eq):
 cs=$_(e,v)
 if cs is $# or $0(cs)!=3:
  err('Quadratic expected')
 c,b,a=cs
 h=$.($Z(b,$:(2,a)))
 k=$.($c(c,$Z($:(b,b),$:(4,a))))
 sq=('^',$d(v,h),2)
 t=sq if a==1 $&('*',a,sq)
 if eq:
  $!('=',('hold',t),$r(k))
 if k==0:
  $!('hold',t)
 $!('hold',('+',t,k))
$, sf_constructmat(a):
 $y(a,5,5)
 i,_=var_of(a[1])
 j,_=var_of(a[2])
 e=evw(a[0],[i,j])
 r=ev(a[3])
 c=ev(a[4])
 $! mk([[subsd(e,{i:ii,j:jj})$) jj in $*(1,c+1)]$) ii in $*(1,r+1)])
$, sf_charpoly(a):
 $y(a,2,2)
 A=ev(a[0])
 v=a[1]if $/(a[1])is $p $& ev(a[1])
 $! charpoly(A,v)
$, sf_simplify(a):
 e=unhold(ev(a[0]))
 $! nice(pyth(e))
''')
_x(r'''SF={
 'd':sf_d,'$j':sf_int,'limit':sf_limit,'sumseq':sf_sum,
 'prodseq':sf_prod,'seq':sf_seq,'taylor':sf_taylor,'series':sf_series,
 'dominantterm':sf_dominant,'solve':sf_solve,'csolve':sf_csolve,
 'zeros':sf_zeros,'czeros':sf_czeros,'nsolve':sf_nsolve,
 'desolve':sf_desolve,'fmin':sf_fmin,'fmax':sf_fmax,'nfmin':sf_nfmin,
 'nfmax':sf_nfmax,'nint':sf_nint,'arclen':sf_arclen,
 'tangentline':sf_tangent,'normalline':sf_normal,'impdif':sf_impdif,
 'avgrc':sf_avgrc,'centraldiff':sf_central,'nderivative':sf_nderiv,
 '$=':sf_expand,'factor':sf_factor,'cfactor':sf_cfactor,
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
  $! b if b is $- $# $& '$M'
 $! $#
$m['when']=when_simp
$, finalize(r,quiet=$2):
 if $((r,'$p'):
  $! r
 if $- $((r,'hold'):
  r=$.(r)if $-($((r,'$I')or $((r,'mat'))$& lmap($.,r)
  if needpyth(r):
   r=pyth(r)
  if SET['mode']=='approx' or $a(r):
   r=evalf(r)
  $? SET['mode']=='exact':
   r=exactify(r)
 if SET['$E']=='$S' $+ $- STATE['$E']$+ has(r,'i')$+ $- quiet:
  err('Non-$S result')
 $! r
$, sqtrig(e,$<):
 if $/(e)is $- $3 or e[0]=='Q':
  $!
 if e[0]=='^' $+ head(e[1])in('sin','cos')$+ $k(e[2])$+ e[2]>=2:
  $<.$%((e[1][0],e[1][1]))
 $) a in e[1:]:
  sqtrig(a,$<)
$, needpyth(r):
 if $- $((r,'+'):
  $! $2
 $<=[]
 sqtrig(r,$<)
 $) n,u in $<:
  if(('cos' if n=='sin' $& 'sin'),u)in $<:
   $! $A
 $! $2
$, pre_register(s):
 low=s.replace(' ','').lower()
 cands=[]
 if ':=' in low:
  cands.$%(low.split(':=')[0])
 if low.$x('define'):
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
   if ok $+ nm $- in STATE['tmpf']:
    STATE['tmpf'].$%(nm)
$, command(c):
 p=c.split()
 if $- p:
  $! ''
 k=p[0]
 if k in('deg','degree'):
  SET['$s']='deg'
  $! 'Angle: degree'
 if k in('rad','radian'):
  SET['$s']='rad'
  $! 'Angle: radian'
 if k in('grad','gradian'):
  SET['$s']='grad'
  $! 'Angle: gradian'
 if k in('approx','auto','exact'):
  SET['mode']=k
  $! 'Mode: '+k
 if k in('$S','$1','rect'):
  SET['$E']='$S' if k=='$S' $& 'rect'
  $! 'Complex format: '+SET['$E']
 if k in('digits','$F'):
  if $0(p)>1 $+ $- p[1].isdigit():
   $! 'Use :digits n with n from 1 to 15'
  n=$t(p[1])if $0(p)>1 $& 10
  OPT['digits']=max(1,min(15,n))
  $! 'Digits: '+$p(OPT['digits'])
 if k=='ascii':
  OPT['uni']=$2
  $! 'ASCII output'
 if k in('unicode','uni'):
  OPT['uni']=$A
  $! 'Unicode output'
 if k=='vars':
  $<=[]
  $) n in sorted(ENV):
   $<.$%(n+' = '+fmt(ENV[n]))
  $) n in sorted(UFUN):
   ps,b=UFUN[n]
   $<.$%(n+'('+','.join(ps)+') = '+fmt(b))
  $! '\n'.join($<)if $< $& '(none)'
 if k in('clear','clearaz','reset'):
  ENV.clear()
  UFUN.clear()
  $! 'Cleared'
 if k in('mem','memory'):
  try:
   import gc
   gc.collect()
   $! 'Memory: %d KB free, %d KB used'%(gc.mem_free()//1024,gc.mem_alloc()//1024)
  $6 $>:
   $! 'Memory information is $- available'
 if k in('mode','modes','getmode'):
  $!('$s='+SET['$s']+' mode='+SET['mode']+' $E='+SET['$E']+
 ' digits='+$p(OPT['digits']))
 if k=='test':
  _load('cashelp')
  saved=(dict(SET),dict(OPT))
  SET.update({'$s':'rad','mode':'auto','$E':'$S'})
  OPT.update({'uni':$A,'digits':10})
  try:
   $! selftest(run)
  finally:
   SET.update(saved[0])
   OPT.update(saved[1])
 if k in('menu','m'):
  cs_menu()
  $! ''
 if k in('gui','g'):
  $! cs_gui()
 if k=='keys':
  try:
   from ti_system import get_key
  $6 ImportError:
   $! 'The key test needs the calculator (ti_system)'
  $v('Press keys; esc twice to stop')
  last=''
  $G $A:
   key=get_key(1)
   $v(repr(key))
   if key=='esc' $+ last=='esc':
    $! ''
   last=key
 if k in('help','?','h'):
  _load('cashelp')
  $! help(p[1]if $0(p)>1 $& $#)
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
 if low.$x('help'):
  $! command(low)
 if low.$x('delvar'):
  $) n in low[6:].replace(',',' ').split():
   ENV.pop(n,$#)
   UFUN.pop(n,$#)
  $! 'Done'
 if low in('clearaz','clear'):
  $! command('clear')
 pre_register(s)
 t=parse(s,isfunc)
 STATE['$E']=(SET['$E']!='$S')
 r=ev(t)
 r=finalize(r)
 if $-($((t,'define')or($((r,'$p')$+ r[1]=='Done')):
  STATE['ans']=unhold(r)if $- $((r,'$p')$& r
 $! fmt_top(r)
$, cs_menu():
 _load('casmenu')
 menu(run)
GUI=$A
$, cs_gui():
 if $- GUI:
  $! 'The full-screen mode is the separate program ncasgui.'
 _load('casgui')
 $! gui(run)
$, startgui():
 r=cs_gui()
 if r:
  $v(r)
  $v('The text version is the program ncastext.')
$, start():
 try:
  import ti_draw
 $6 ImportError:
  $! cas()
 r=cs_gui()
 if r:
  $v(r)
  cas()
$, ver():
 $! 'nCAS '+VERSION
$, calc(s):
 try:
  $! run(s)
 $6 $O as ex:
  $! 'Error: '+$p(ex)
''')
_x(r'''$, cas():
 $v('nCAS '+VERSION+' $) TI-Nspire CX II')
 $v(('? help, m menu, g full screen, q quit')if GUI $& '? help, m menu, q quit')
 blank=0
 $G $A:
  try:
   s=input('> ')
  $6(EOFError,$o):
   $R
  s=s.strip()
  if s in('q','quit','exit',':q'):
   $R
  if $- s:
   blank+=1
   if blank>=2:
    $v('($/ q $+ enter to quit)')
    blank=0
   $4
  blank=0
  if s.lower()in('m','menu'):
   try:
    cs_menu()
   $6 $> as ex:
    $v('Error: '+$p(ex))
   $4
  if s.lower()in('g','gui'):
   try:
    r=cs_gui()
   $6 $> as ex:
    r='Error: '+$p(ex)
   if r:
    $v(r)
   $4
  try:
   $<=run(s)
   if $<:
    $v($<)
  $6 $O as ex:
   $v('Error: '+$p(ex))
  $6 $C:
   $v('Error: Division by zero')
  $6 MemoryError:
   try:
    import gc
    gc.collect()
   $6 ImportError:
    pass
   $v('Error: Out of memory')
  $6 $o:
   $v('Break')
  $6 RuntimeError as ex:
   $v('Error: Too $1 ('+$p(ex)+')')
  $6 $> as ex:
   $v('Error: '+$p(ex))
''')
_L['cashelp']=(r'''CATS=(
 ('alg','Algebra','solve csolve zeros czeros nsolve linsolve factor cfactor $= comdenom propfrac getnum getdenom completesquare polycoeffs polydegree polyquotient polyremainder polygcd polyroots cpolyroots polyeval tExpand tCollect simplify exact approx domain'),
 ('calc','Calculus','d $j limit sumseq prodseq taylor series dominantTerm deSolve impDif arcLen tangentLine normalLine fMin fMax nfMin nfMax nInt nDerivative avgRC centralDiff'),
 ('mat','Matrix/vector','det identity transpose rref ref inverse eigVl eigVc charPoly LU QR trace norm rowNorm colNorm diag augment colAugment subMat rowSwap rowAdd mRow mRowAdd crossP dotP unitV simult constructMat newMat randMat dim rowDim colDim mat>$I $I>mat'),
 ('num','Numbers','gcd lcm mod remain intDiv isPrime nCr nPr ! floor ceiling round iPart fPart sign $J $S imag conj $s'),
 ('$I','Lists/stats','seq sum product mean median stdDev stdDevPop variance varPop max min sortA sortD cumulativeSum deltaList augment left right mid count normPdf normCdf invNorm binomPdf binomCdf poissPdf poissCdf geomPdf geomCdf'),
 ('conv','Conversions (expr>>$B)','>>Decimal >>approxFraction() >>DMS >>DD >>Rad >>Grad >>Polar >>Rect >>Cylind >>Sphere >>exp >>ln >>logbase() >>sin >>cos >>Base2 >>Base10 >>Base16 exp>$I()'),
 ('cmd','Commands',':deg :rad :grad :auto :exact :approx :$S :$1 :digits n :ascii :unicode :vars :clear :mode :mem  delvar a  q=quit'),
 )
SYN={
 'solve':'solve(eqn,var) solve(eqn,var=guess)\nsolve(ineq,var) solve(eq1 $+ eq2,{x,y})\nsolve(...)|x>0  (n1,n2..=any integer)',
 'csolve':'cSolve(eqn,var) $1 solutions',
 'zeros':'zeros(expr,var) -> $I of roots\nzeros({e1,e2},{x,y}) -> matrix',
 'czeros':'cZeros(expr,var) $1 roots',
 'nsolve':'nSolve(eqn,var[=guess][,lo,hi])',
 'linsolve':'linSolve({eq1,eq2},{x,y})',
 'factor':'factor(expr[,var]) factor(integer)\nwith var: irrational factors',
 'cfactor':'cFactor(expr[,var]) $1 factors',
 '$=':'$=(expr[,var]) incl. partial fractions',
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
 'polyroots':'polyRoots(poly,var) polyRoots({$_})',
 'cpolyroots':'cPolyRoots(poly,var)',
 'polyeval':'polyEval({$_},x)',
 'texpand':'tExpand(expr) $= trig of sums/multiples',
 'tcollect':'tCollect(expr) products -> multiple angles',
 'simplify':'simplify(expr) extra simplification',
 'exact':'exact(expr[,tol]) floats -> fractions',
 'approx':'approx(expr) decimal value',
 'domain':'domain(expr,var)',
 'd':'d(expr,var[,order])  d(expr,var)|var=val\nderivative(...) same',
 '$j':'$j(expr,var) antiderivative\nintegral(expr,var,a,b) definite\n(\u222b also accepted)',
 'limit':'limit(expr,var,point[,dir]) dir:-1 left,1 right\npoint may be $[ or -$[',
 'sumseq':'sumSeq(expr,var,lo,hi)  (\u03a3) hi may be $[',
 'prodseq':'prodSeq(expr,var,lo,hi)  (\u03a0)',
 'taylor':'taylor(expr,var,order[,point])',
 'series':'series(expr,var,order[,point])',
 'dominantterm':'dominantTerm(expr,var[,point])',
 'desolve':"deSolve(ode,x,y) use y' $+ y''\ndeSolve(y''+y=0 $+ y(0)=0 $+ y'(0)=1,x,y)",
 'impdif':'impDif(eqn,x,y[,order]) dy/dx',
 'arclen':'arcLen(expr,var,a,b)',
 'tangentline':'tangentLine(expr,var,point)',
 'normalline':'normalLine(expr,var,point)',
 'fmin':'fMin(expr,var[,lo,hi]) -> var=value',
 'fmax':'fMax(expr,var[,lo,hi])',
 'nfmin':'nfMin(expr,var[,lo,hi]) numeric',
 'nfmax':'nfMax(expr,var[,lo,hi]) numeric',
 'nint':'nInt(expr,var,a,b) numeric $j',
 'nderivative':'nDerivative(expr,var=val[,order])',
 'avgrc':'avgRC(expr,var[=val][,h])',
 'centraldiff':'centralDiff(expr,var[=val][,h])',
 'det':'det(M)','inverse':'M^-1 or inverse(M)','rref':'rref(M)','ref':'ref(M)',
 'eigvl':'eigVl(M) eigenvalues','eigvc':'eigVc(M) unit eigenvectors (columns)',
 'charpoly':'charPoly(M,var)','lu':'LU(M) -> {L,U,P} with P*M=L*U','qr':'QR(M) -> {Q,R}',
 'simult':'simult(A,b) solves A*x=b','constructmat':'constructMat(expr,i,j,$T,cols)',
 'crossp':'crossP(u,v)','dotp':'dotP(u,v)','unitv':'unitV(v)','norm':'norm(M)',
 'seq':'seq(expr,var,lo,hi[,step])',
 'ncr':'nCr(n,k)','npr':'nPr(n,k)','gcd':'gcd(a,b)','lcm':'lcm(a,b)',
 'mod':'mod(a,b)','isprime':'isPrime(n)',
 'define':'Define f(x)=expr   or   f(x):=expr\nexpr->a  or  a:=expr   delvar a',
 'with':'expr|x=3   expr|x>0   solve(...)|0<=x<=2pi',
 'menu':'m or menu: numbered menus build the\ncommand $) you; 0 back, q quit.\nMatrices may be typed 1,2;3,4',
 'syntax':'implicit mult: 2x  3(x+1)  x(x+1)\n^ or ** power, $L( or \u221a, pi, e, i, $[\n<= >= /= $+ or $-, ans = last result\nlog(x)=ln(x) ([ln] key); log10(x), log(x,b)',
 'log':'log(x) natural log (= ln, the [ln] key)\nlog10(x) base 10, log(x,b) base b',
 }
$, help($B=$#):
 if $B is $#:
  $<=['nCAS help: ?topic or ?command']
  $) k,t,items in CATS:
   $<.$%('?'+k+'  '+t)
  $<.$%('?define ?with ?syntax ?menu')
  $<.$%('m = menus (no typing of names)')
  $! '\n'.join($<)
 $B=$B.lower().replace('(','').strip()
 $) k,t,items in CATS:
  if $B==k:
   $! t+':\n'+items
 if $B in SYN:
  $! SYN[$B]
 $) k in SYN:
  if k.$x($B):
   $! SYN[k]
 $! 'No help $) '+$B
''',
r'''SELFTEST=(
 ('factor(x^2-5x+6)','(x-2)*(x-3)'),
 ('$=((x+1)^3)','x^3+3*x^2+3*x+1'),
 ('solve(x^2-5x+6=0,x)','x=2 or x=3'),
 ('solve(x^2=2,x)','x=-\u221a2 or x=\u221a2'),
 ('d(x^3*sin(x),x)','x^3*cos(x)+3*x^2*sin(x)'),
 ('$j(x*e^x,x)','x*e^x-e^x'),
 ('$j(1/(1+x^2),x,0,1)','\u03c0/4'),
 ('limit(sin(x)/x,x,0)','1'),
 ('taylor(e^x,x,3)','x^3/6+x^2/2+x+1'),
 ('sumSeq(k,k,1,n)','n*(n+1)/2'),
 ("deSolve(y'=y,x,y)",'y=c1*e^x'),
 ('det([[1,2][3,4]])','-2'),
 ('[[1,2][3,4]]^-1','[[-2,1][3/2,-1/2]]'),
 ('$L(12)','2*\u221a3'),
 ('cSolve(x^2+1=0,x)','x=-i or x=i'),
 ('factor(360)','2^3*3^2*5'),
 ('solve(x^2-4>0,x)','x<-2 or x>2'),
 ('nSolve(cos(x)=x,x)','0.7390851332'),
 )
$, selftest(run):
 ok=0
 $<=[]
 $) q,a in SELFTEST:
  try:
   r=run(q)
  $6 $> as ex:
   r='ERR '+$p(ex)
  if r==a:
   ok+=1
  $&:
   $<.$%('FAIL '+q+' -> '+r)
 $<.$%('%d/%d tests passed'%(ok,$0(SELFTEST)))
 $! '\n'.join($<)
''',)
_L['casmenu']=(r'''ALG=(
 ('Expand','$=(@1`,@2`)',(('$]',$#),('Var (blank=all)',''))),
 ('Factor','factor(@1`,@2`)',(('$]',$#),('Var (blank=Q)',''))),
 ('cFactor','cFactor(@1`,@2`)',(('$]',$#),('Var (blank=all)',''))),
 ('Simplify','simplify(@1)',(('$]',$#),)),
 ('comDenom','comDenom(@1)',(('$]',$#),)),
 ('propFrac','propFrac(@1`,@2`)',(('$]',$#),('Var',''))),
 ('Partial frac','$=(@1,@2)',(('Rational expr',$#),('Var','x'))),
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
 ('Integral','$j(@1,@2)',(('f',$#),('Var','x'))),
 ('Def $j','$j(@1,@2,@3,@4)',(('f',$#),('Var','x'),('Lower ($[ ok)',$#),('Upper',$#))),
 ('Limit','limit(@1,@2,@3`,@4`)',(('f',$#),('Var','x'),('Point ($[ ok)','0'),('Side 1/-1',''))),
 ('Taylor','taylor(@1,@2,@3`,@4`)',(('f',$#),('Var','x'),('Order','5'),('Point',''))),
 ('Series','series(@1,@2,@3`,@4`)',(('f',$#),('Var','x'),('Order','5'),('Point',''))),
 ('Sum (sigma)','sumSeq(@1,@2,@3,@4)',(('Term',$#),('Index','k'),('From','1'),('To ($[ ok)','n'))),
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
 ('Zeros','zeros(@1,@2)',(('$]',$#),('Var','x'))),
 ('cZeros','cZeros(@1,@2)',(('$]',$#),('Var','x'))),
 ('nSolve','nSolve(@1,@2`,@3,@4`)',(('Equation',$#),('Var or x=guess','x'),('Lower',''),('Upper',''))),
 ('System 2 eqs','solve(@1 $+ @2,{@3})',(('Eq 1',$#),('Eq 2',$#),('Vars','x,y'))),
 ('System 3 eqs','solve(@1 $+ @2 $+ @3,{@4})',(('Eq 1',$#),('Eq 2',$#),('Eq 3',$#),('Vars','x,y,z'))),
 ('Poly roots','polyRoots(@1,@2)',(('Polynomial',$#),('Var','x'))),
 ('Domain','domain(@1,@2)',(('$]',$#),('Var','x'))),
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
 ('Factor $t','factor(@1)',(('Integer',$#),)),
 ('isPrime','isPrime(@1)',(('Integer',$#),)),
 ('gcd','gcd(@1,@2)',(('a',$#),('b',$#))),
 ('lcm','lcm(@1,@2)',(('a',$#),('b',$#))),
 ('mod','mod(@1,@2)',(('a',$#),('b',$#))),
 ('nCr','nCr(@1,@2)',(('n',$#),('r',$#))),
 ('nPr','nPr(@1,@2)',(('n',$#),('r',$#))),
 ('Factorial','(@1)!',(('n',$#),)),
 ('Real part','$S(@1)',(('Complex z',$#),)),
 ('Imag part','imag(@1)',(('Complex z',$#),)),
 ('Conjugate','conj(@1)',(('Complex z',$#),)),
 ('|z|','$J(@1)',(('Complex z',$#),)),
 ('Angle','$s(@1)',(('Complex z',$#),)),
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
 ('normCdf','normCdf(@1,@2`,@3,@4`)',(('Lower (-$[ ok)',$#),('Upper',$#),('mu',''),('sigma',''))),
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
 ('Real res',':$S',()),
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
 ('Number/$E',NUMB),('Lists/stats',LIST),('Convert',CONV),
 ('Settings',SETS),
 )
KEYS='123456789abcdefghijklmnop'
class Quit($>):
 pass
$, ask(q):
 try:
  s=input(q)
 $6 EOFError:
  $n Quit()
 s=s.strip()
 if s.lower()in('q','quit'):
  $n Quit()
 $! s
$, show(title,labels):
 $v('-- '+title+' --')
 line=''
 $) i in $*($0(labels)):
  cell=KEYS[i]+' '+labels[i]
  if line:
   $v(line+' '*max(1,16-$0(line))+cell)
   line=''
  $&:
   line=cell
 if line:
  $v(line)
 $v('0 back  q quit')
$, pick(title,labels):
 show(title,labels)
 $G $A:
  s=ask('#: ').lower()
  if s in('','0'):
   $! $#
  i=KEYS.find(s)
  if $0(s)==1 $+ 0<=i<$0(labels):
   $! i
  $v('Choose '+KEYS[0]+'-'+KEYS[$0(labels)-1]+', 0 or q')
$, matrix_text(s):
 s=s.strip()
 if s $+ s[0]$- in '[(' $+(';' in s or ',' in s):
  $! '['+s+']'
 $! s
$, build(item):
 label,tpl,prompts=item
 $g=[]
 $) p in prompts:
  q=p[0]
  d=p[1]
  hint='' if $- d $& ' ['+d+']'
  s=ask(q+hint+': ')
  if $- s:
   if d is $#:
    $v('(cancelled)')
    $! $#
   s=d
  if $0(p)>2 $+ p[2]=='m' $+ s:
   s=matrix_text(s)
  $g.$%(s)
 $! fill(tpl,$g)
$, fill(tpl,$g):
 $<=''
 parts=tpl.split('`')
 $) k in $*($0(parts)):
  seg=parts[k]
  if k%2==1:
   blank=$2
   $) i in $*($0($g)):
    if('@'+$p(i+1))in seg $+ $- $g[i]:
     blank=$A
   if blank:
    $4
  $<+=seg
 res=''
 i=0
 $G i<$0($<):
  c=$<[i]
  if c=='@' $+ i+1<$0($<)$+ '1'<=$<[i+1]<='9':
   res+=$g[$t($<[i+1])-1]
   i+=2
  $&:
   res+=c
   i+=1
 $! res
$, menu(run):
 $v('Menus: pick a number or letter.')
 $v("Type ans $) the last result.")
 try:
  $G $A:
   k=pick('nCAS menu',[m[0]$) m in MAIN])
   if k is $#:
    $!
   title,items=MAIN[k]
   $G $A:
    j=pick(title,[it[0]$) it in items])
    if j is $#:
     $R
    cmd=build(items[j])
    if cmd is $#:
     $4
    $v('> '+cmd)
    try:
     $<=run(cmd)
    $6 $O as ex:
     $<='Error: '+$p(ex)
    $6 $C:
     $<='Error: Division by zero'
    $6 MemoryError:
     $<='Error: Out of memory'
    $6 RuntimeError as ex:
     $<='Error: Too $1'
    $6 Quit:
     $n
    $6 $> as ex:
     $<='Error: '+$p(ex)
    if $<:
     $v($<)
    ask('(enter) ')
 $6 Quit:
  $!
 $6 $o:
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
TEXT={'space':' ','$L':'$L(','\u221a':'$L(','pi':'\u03c0',
 'exp':'e^','ln':'ln(','log':'log10(','square':'^2','\u00b2':'^2',
 'ee':'E','EE':'E','\u1d07':'E','$r':'-','(-)':'-','\u2212':'-',
 '\u00d7':'*','\u00f7':'/','\u2264':'<=','\u2265':'>=','\u2260':'/=',
 '\u2192':'->','ans':'ans','theta':'\u03b8','$J':'$J(',
 'sin':'sin(','cos':'cos(','tan':'tan(','sin\u207b\u00b9':'$w(',
 'cos\u207b\u00b9':'arccos(','tan\u207b\u00b9':'$u(','$[':'$[',
 'i':'i','e':'e'}
gu_TRIG=('sin(','cos(','tan(','$w(','arccos(','$u(',
 'sinh(','cosh(','tanh(','sec(','csc(','cot(')
NEEDANS='+*/^'
G={}
$, gui(run):
 G.setdefault('hist',[])
 key=findkey()
 try:
  import ti_draw
 $6 ImportError:
  ti_draw=$#
 if key is $# or ti_draw is $#:
  $! screen(run,key is $#)
 G['d']=ti_draw
 G['key']=key
 G['cmode']=0
 G['gui']=$A
 try:
  w,h=ti_draw.get_screen_dim()
  w=$t(w)
  h=$t(h)
 $6 $>:
  w,h=318,212
 G['w']=w
 G['h']=h
 G['$T']=(h-2*LH-5)//LH
 G['ncell']=(w-16)//CW
 G['wrap']=(w-12)//AW
 ed_reset()
 G['sel']=$#
 G['top']=$#
 G['msg']=''
 try:
  ti_draw.use_buffer()
  G['buffer']=$A
 $6 $>:
  G['buffer']=$2
 try:
  loop(run)
 $6 $o:
  pass
 $! ''
KEYFN=('get_key','getkey','getKey','wait_key','waitkey')
$, findkey():
 $) mn in('ti_system','ti_draw','ti_plotlib'):
  try:
   m=__import__(mn)
  $6 ImportError:
   $4
  $) fn in KEYFN:
   f=getattr(m,fn,$#)
   if f is $- $#:
    $! keyfun(f)
 $! tibasic()
TINAMES={'ent':'enter','dow':'down','lef':'left','rig':'right',
 'cle':'clear','men':'menu','tri':'trig','hom':'home',
 'ctr':'ctrl','shi':'shift','cen':'center','ret':'$!',
 'squ':'square','spa':'space','sqr':'$L','bac':'backspace'}
$, tibasic():
 try:
  import ti_system
  ev=ti_system.eval_function
 $6(ImportError,AttributeError):
  $! $#
 try:
  if ev('ncaskey',0)!=0:
   $! $#
 $6 $>:
  $! $#
 $, wait(x=1):
  c=$t(ev('ncaskey',1))
  s=''
  $) v in(c>>32,(c>>16)&65535,c&65535):
   s+=chr(v)
  s=s.rstrip(' ')or ' '
  $! TINAMES.get(s,s)
 $! wait
$, keyfun(f):
 try:
  from time import sleep
 $6 ImportError:
  sleep=$#
 mode=[1]
 $, wait(x=1):
  if mode[0]:
   try:
    $! $p(f(1))
   $6 TypeError:
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
  try:
   d.set_color(c[0],c[1],c[2])
   $!
  $6 TypeError:
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
 $<=[]
 $G $0(s)>n:
  $<.$%(s[:n])
  s=s[n:]
 $<.$%(s)
 $! $<
$, selected():
 s=G['sel']
 if s is $#:
  $! $#
 k=$0(G['hist'])-1-s//2
 $!(k,'$<' if s%2==0 $& 'in')
$, status():
 if G['msg']:
  $! G['msg']
 a=SET['$s'].upper()
 m=SET['mode'].upper()
 c='REAL' if SET['$E']=='$S' $& 'CPLX'
 $! 'nCAS  '+a+' '+m+' '+c+('   menu: commands' if G.get('gui')$& '')
$, draw():
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
   end=$0(bl)-1
   start=startfor(bl,end,avail)
  $&:
   idx=[i $) i in $*($0(bl))if(bl[i][3],bl[i][4])==sel]
   a=idx[0]
   b=idx[-1]
   end=min(G.get('hend',$0(bl)-1),$0(bl)-1)
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
  $) i in $*(start,end+1):
   kind,data,bh,k,part=bl[i]
   if last is $- $# $+ k!=last:
    box(2,y-1,w-4,1,C_RULE)
   if sel is $- $# $+(k,part)==sel:
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
 if $- G['row']$+ $- G['path']$+ s $+ s[0]in NEEDANS $+ G['hist']:
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
 try:
  $<=run(s)
 $6 $O as ex:
  $<='Error: '+$p(ex)
  bad=$A
 $6 $C:
  $<='Error: Division by zero'
  bad=$A
 $6 MemoryError:
  $<='Error: Out of memory'
  bad=$A
 $6 RuntimeError:
  $<='Error: Too $1'
  bad=$A
 $6 $o:
  $<='Interrupted'
  bad=$A
 $6 $> as ex:
  $<='Error: '+$p(ex)
  bad=$A
 G['msg']=''
 if $< is $#:
  $<=''
 G['hist'].$%((s,$<,bad))
 if $0(G['hist'])>MAXH:
  G['hist'].pop(0)
''',
r'''$, loop(run):
 $G $A:
  draw()
  k=G['key'](1)
  G['msg']=''
  if $- k:
   $4
  before=ed_snap()
  a=ctrlaction(k)
  if a=='wait':
   G['msg']='ctrl  (next key: blue label)'
   $4
  if a is $- $#:
   doaction(run,a,k)
  $&:
   key(run,k)
  if ed_text()!=before[3]$+ a!=('undo',):
   G.setdefault('undo',[]).$%(before)
   del G['undo'][:-30]
$, key(run,k):
 if k=='esc':
  if G['sel']is $- $#:
   G['sel']=$#
  $? G['row']:
   ed_reset()
  $&:
   $n $o
 $? k in ENTER:
  if G['sel']is $- $#:
   k2,part=selected()
   inp,res,bad=G['hist'][k2]
   G['sel']=$#
   insert(inp if part=='in' $& res.replace('\n ','').replace('\n',''))
  $? ed_text().strip():
   s=ed_text()
   ed_reset()
   special(run,s)
 $? k in('up','down')$+ G['sel']is $# $+ ed_vert(1 if k=='down' $&-1):
  pass
 $? k=='up':
  n=2*$0(G['hist'])
  if n:
   G['sel']=0 if G['sel']is $# $& min(G['sel']+1,n-1)
 $? k=='down':
  if G['sel']is $- $#:
   G['sel']=$# if G['sel']==0 $& G['sel']-1
 $? k=='left':
  G['sel']=$#
  ed_left()
 $? k=='right':
  G['sel']=$#
  ed_right()
 $? k in('del','backspace'):
  G['sel']=$#
  ed_del()
 $? k=='clear':
  G['sel']=$#
  ed_reset()
 $? k in MENU:
  G['sel']=$#
  r=menus()
  if r is $- $#:
   act(run,r)
 $? k in TABKEYS or k in BACKTAB:
  G['sel']=$#
  ed_tab(-1 if k in BACKTAB $& 1)
 $? k in CATKEYS:
  G['sel']=$#
  catalog()
 $? k in TEMPLKEYS:
  G['sel']=$#
  templates()
 $? k in SYMKEYS:
  G['sel']=$#
  gu_symbols()
 $? k=='trig':
  G['sel']=$#
  j=choose('Trig',gu_TRIG)
  if j is $- $#:
   insert(gu_TRIG[j]+')',1)
 $? k in TEXT:
  G['sel']=$#
  t=TEXT[k]
  if t.endswith('('):
   insert(t+')',1)
  $&:
   insert(t)
 $? $0(k)==1:
  G['sel']=$#
  ed_autoexit(k)
  insert(k)
 $&:
  G['msg']='key '+repr(k)+' $- used'
CTRLKEYS=('ctrl','doc')
CTRL={'(':('ins','[]',1),')':('ins','{}',1),'^':('ins','root(,)',2),
 '^2':('ins','$L()',1),'e^':('ins','ln()',1),'10^':('ins','log10()',1),
 '=':('rel',),'trig':('help',),'del':('clear',),'clear':('clear',),
 '-':('ins','ans',0),'*':('ins','""',1),'/':('ins','()/()',4),
 'enter':('approx',),'var':('ins','->',0),'esc':('undo',),
 'cat':('$l',),'catalog':('$l',),'book':('$l',),
 'template':('ins',':=',0),'templates':('ins',':=',0),'templ':('ins',':=',0),
 'tmpl':('ins',':=',0),'tab':('menu',),'menu':('$l',)}
DIRECT={'[]':('ins','[]',1),'{}':('ins','{}',1),'""':('ins','""',1),
 '()':('ins','()',1),'\u2248':('approx',),'approx':('approx',),
 'undo':('undo',),'sto':('ins','->',0),'sto\u2192':('ins','->',0),
 'store':('ins','->',0),'\u2254':('ins',':=',0),':=':('ins',':=',0),
 'nroot':('ins','root(,)',2),'root':('ins','root(,)',2),'help':('help',),
 '10^x':('ins','10^',0),'pow10':('ins','10^',0),'10^':('ins','10^',0)}
RELS=(('=','='),('\u2260  $- equal','/='),('<','<'),('>','>'),
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
 if $0(k)>4 $+ k[:4].lower()=='ctrl':
  r=k[4:].lstrip('+-_ ')
  $! CTRL.get(ctrlbase(r))or CTRL.get(r)or('none',k)
 $! DIRECT.get(k)
$, doaction(run,a,k):
 G['sel']=$#
 kind=a[0]
 if kind=='ins':
  insert(a[1],a[2])
 $? kind=='clear':
  ed_reset()
 $? kind=='undo':
  u=G.get('undo')
  if u:
   ed_restore(u.pop())
 $? kind=='approx':
  s=ed_text().strip()
  if $- s $+ G['hist']:
   s='ans'
  if s:
   ed_reset()
   evaluate(run,'approx('+s+')')
 $? kind=='rel':
  j=choose('Relations',[r[0]$) r in RELS])
  if j is $- $#:
   insert(RELS[j][1])
 $? kind=='$l':
  gu_symbols()
 $? kind=='menu':
  r=menus()
  if r is $- $#:
   act(run,r)
 $? kind=='help':
  panel('ctrl keys','any key to close')
  $) i in $*($0(CTRLHELP)):
   text(10,LH+4+i*LH,CTRLHELP[i],C_TXT)
  gu_show()
  G['key'](1)
 $&:
  G['msg']='ctrl+'+$p(a[1])+' $- used'
$, special(run,s):
 low=s.strip().lower()
 if low in(':keys','keys'):
  keytest()
 $? low in('q','quit',':q'):
  $n $o
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
  if k=='esc' $+ last=='esc':
   $!
  last=k
$, choose(title,labels,jump=$2):
 n=$0(labels)
 i=0
 $T=G['$T']-1
 top=0
 w=G['w']
 $G $A:
  if i<top:
   top=i
  if i>=top+$T:
   top=i-$T+1
  box(10,LH+4,w-20,($T+1)*LH+6,C_DIM)
  box(11,LH+5,w-22,($T+1)*LH+4,(255,255,255))
  box(11,LH+5,w-22,LH,C_BAR)
  text(16,LH+5,title,C_BART)
  y=2*LH+7
  $) j in $*(top,min(n,top+$T)):
   if j==i:
    box(12,y,w-24,LH,C_SEL)
   key=KEYS[j]if j<$0(KEYS)$+ $- jump $& ' '
   text(16,y,key,C_DIM)
   text(34,y,labels[j],C_TXT)
   y+=LH
  if top+$T<n:
   text(w-30,y-LH,'v',C_DIM)
  gu_show()
  k=G['key'](1)
  if k=='up':
   i=(i-1)%n
  $? k=='down':
   i=(i+1)%n
  $? k in ENTER or k=='right':
   $! i
  $? k in('esc','left')or k in MENU:
   $! $#
  $? jump $+ $0(k)==1 $+ k.isalpha():
   c=k.lower()
   $) d in $*(1,n+1):
    if labels[(i+d)%n][:1].lower()==c:
     i=(i+d)%n
     $R
  $? $- jump $+ $0(k)==1 $+ k in KEYS[:n]:
   $! KEYS.index(k)
''',
r'''$, menus():
 _load('casmenu')
 main=MAIN
 $G $A:
  a=choose('Menu',[m[0]$) m in main]+['Templates','Symbols'])
  if a is $#:
   $! $#
  if a==$0(main):
   templates()
   $! $#
  if a==$0(main)+1:
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
 $g=[]
 mark='\u0001'
 first=$A
 $) p in prompts:
  d=p[1]
  if d is $#:
   v='[]' if $0(p)>2 $+ p[2]=='m' $& ''
   if first:
    v='['+mark+']' if v $& mark
    first=$2
  $&:
   v=d
  $g.$%(v)
 s=fill(tpl,$g)
 i=s.find(mark)
 if i<0:
  i=$0(s)
 $&:
  s=s[:i]+s[i+1:]
 ed_chars(s)
 G['pos']-=$0(s)-i
$, screen(run,nokeys=$A):
 G['gui']=$2
 G['msg']=''
 try:
  import ti_system
  have=[n $) n in dir(ti_system)if n[0]!='_']
 $6 ImportError:
  have=$#
 $v('nCAS screen mode: this OS gives programs no single-key input.')
 if have is $#:
  $v('(no ti_system module)')
 $&:
  $v('ti_system: '+' '.join(have))
 $T=4
 $G $A:
  hist=G['hist']
  $v('-'*30)
  first=max(0,$0(hist)-$T)
  $) k in $*(first,$0(hist)):
   inp,res,bad=hist[k]
   $v('#'+$p(k+1)+' '+inp)
   $) r in res.split('\n'):
    $v('   '+r)
  $v(status()+'  m menu  q quit')
  try:
   s=input('> ').strip()
  $6(EOFError,$o):
   $! ''
  if s in('q','quit',':q'):
   $! ''
  if s in('m','menu'):
   cmd=pickmenu()
   if $- cmd:
    $4
   $v('> '+cmd)
   s=cmd
  if $- s:
   $4
  s=refs(s,hist)
  if s.strip().lower()in(':keys','keys'):
   $v('No key reading on this OS.')
   $4
  evaluate(run,s)
$, pickmenu():
 _load('casmenu')
 try:
  $G $A:
   k=pick('nCAS menu',[m[0]$) m in MAIN])
   if k is $#:
    $! $#
   title,items=MAIN[k]
   j=pick(title,[it[0]$) it in items])
   if j is $#:
    $4
   cmd=build(items[j])
   if cmd:
    $! cmd
 $6 Quit:
  $! $#
$, refs(s,hist):
 $<=''
 i=0
 $G i<$0(s):
  if s[i]=='#' $+ i+1<$0(s)$+ s[i+1].isdigit():
   j=i+1
   $G j<$0(s)$+ s[j].isdigit():
    j+=1
   n=$t(s[i+1:j])
   if 1<=n<=$0(hist)$+ $- hist[n-1][2]:
    $<+='('+hist[n-1][1].split('\n')[0]+')'
   $&:
    $<+=s[i:j]
   i=j
  $&:
   $<+=s[i]
   i+=1
 $! $<
TEMPLKEYS=('template','templates','templ','tmpl')
SYMKEYS=('$l','symbol','punc','?!','?!>','palette')
TPLS=('Matrix m\u00d7n','Column vector','Row vector')
SYMS=(
 (';',';',0,'next row in a matrix [1,2;3,4]'),(',',',',0,'separates arguments'),
 ('[ ]','[]',1,'matrix or vector'),('{ }','{}',1,'$I {1,2,3}'),
 ('( )','()',1,'parentheses'),('|','|',0,'with: x^2|x=3'),
 ("'","'",0,"derivative in deSolve: y'"),('" "','""',1,'text'),
 ('=','=',0,'equation'),('\u2260','/=',0,'$- equal'),
 ('<','<',0,'less than'),('>','>',0,'greater than'),
 ('\u2264','<=',0,'less or equal'),('\u2265','>=',0,'greater or equal'),
 (':=',':=',0,'define: f(x):=x^2'),('\u2192','->',0,'store: 5->a'),
 ('^','^',0,'power'),('^2','^2',0,'square'),
 ('^-1','^-1',0,'inverse: [1,2;3,4]^-1'),('\u221a','$L()',1,'square root'),
 ('root','root(,)',2,'n-th root: root(8,3)'),('!','!',0,'factorial'),
 ('\u03c0','\u03c0',0,'pi'),('e','e',0,"Euler's number"),
 ('i','i',0,'imaginary unit'),('\u221e','$[',0,'infinity'),
 ('\u00b0','\u00b0',0,'degrees: sin(30\u00b0)'),('E','E',0,'times 10^: 2E3'),
 ('>>','>>',0,'convert: pi>>Decimal'),('%','%',0,'percent'),
 ('$+',' $+ ',0,'both: x>0 $+ x<1'),('or',' or ',0,'either'),
 ('$-','$- ',0,'negation'),('ans','ans',0,'last result'),
 (':',':',0,'command: :deg :rad :test'),('_','_',0,'underscore'),
 ('&','&',0,'join text'),('x','x',0,'variable x'),
 ('y','y',0,'variable y'),('t','t',0,'variable t'),
 )
SCOLS=8
$, templates():
 j=choose('Templates',$I(TPLS)+[t[0]$) t in MATHTPL])
 if j is $#:
  $!
 if j>=$0(TPLS):
  insert(MATHTPL[j-$0(TPLS)][1])
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
  if 0<=a $+ a+1<$0(r)$+ r[a]=='[' $+ r[a+1]==']':
   G['pos']=a+1
   s=s[1:-1]
   $R
 ed_chars(s)
$, gu_symbols():
 n=$0(SYMS)
 $T=(n+SCOLS-1)//SCOLS
 k0=G.get('symk',0)
 w=G['w']
 cw=(w-8)//SCOLS
 ch=LH+6
 $G $A:
  panel('Symbols',SYMS[k0][3])
  y0=LH+4
  $) r in $*($T):
   $) c in $*(SCOLS):
    k=r*SCOLS+c
    if k>=n:
     $R
    x=4+c*cw
    y=y0+r*ch
    box(x+1,y+1,cw-2,ch-2,C_SEL if k==k0 $& C_BOX)
    lab=SYMS[k][0]
    text(x+max(2,(cw-$0(lab)*AW)//2),y+2,lab,C_TXT)
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
  $? key=='left':
   k0=(k0-1)%n
  $? key=='down':
   k0=k0+SCOLS if k0+SCOLS<n $& k0%SCOLS
  $? key=='up':
   if k0-SCOLS>=0:
    k0-=SCOLS
   $&:
    last=($T-1)*SCOLS+k0%SCOLS
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
''',
r'''$, gridsize(r,c,fix):
 typed=[]
 $G $A:
  panel('Matrix size','arrows or digits, enter OK, esc cancel')
  text(20,2*LH,'Rows: '+$p(r)+'    Columns: '+$p(c),C_TXT)
  cw=min(24,(G['w']-40)//max(c,1))
  ch=min(16,(G['h']-6*LH)//max(r,1))
  $) i in $*(r):
   $) j in $*(c):
    box(20+j*cw,4*LH+i*ch,cw-3,ch-3,C_SEL)
  gu_show()
  k=G['key'](1)
  if k=='esc':
   $! $#
  if k in ENTER:
   $!(r,c)
  if k=='up' $+ fix!='r':
   r=min(9,r+1)
  $? k=='down' $+ fix!='r':
   r=max(1,r-1)
  $? k=='right' $+ fix!='c':
   c=min(9,c+1)
  $? k=='left' $+ fix!='c':
   c=max(1,c-1)
  $? $0(k)==1 $+ '1'<=k<='9':
   if fix=='c':
    r=$t(k)
   $? fix=='r':
    c=$t(k)
   $&:
    typed.$%($t(k))
    if $0(typed)==1:
     r=typed[0]
    $&:
     c=typed[1]
     typed=[]
$, keytext(k):
 if k in TEXT:
  $! TEXT[k]
 if $0(k)==1:
  $! k
 $! $#
$, grid(r,c):
 cells=[['']*c $) i in $*(r)]
 i=0
 j=0
 w=G['w']
 cw=max(30,min(80,(w-24)//c))
 ncw=max(1,(cw-6)//AW)
 $T=G['$T']
 $G $A:
  panel('Matrix '+$p(r)+'\u00d7'+$p(c),
 'tab/arrows move, enter done, esc cancel')
  top=max(0,i-$T+2)
  y0=LH+6
  nshow=min(r-top,$T-1)
  box(8,y0,2,nshow*(LH+4),C_TXT)
  box(8,y0,5,2,C_TXT)
  box(8,y0+nshow*(LH+4)-2,5,2,C_TXT)
  x1=14+c*cw
  box(x1,y0,2,nshow*(LH+4),C_TXT)
  box(x1-3,y0,5,2,C_TXT)
  box(x1-3,y0+nshow*(LH+4)-2,5,2,C_TXT)
  $) a in $*(top,top+nshow):
   y=y0+(a-top)*(LH+4)
   $) b in $*(c):
    x=14+b*cw
    cur=(a==i $+ b==j)
    box(x+1,y+1,cw-4,LH+2,C_SEL if cur $& C_BOX)
    t=cells[a][b]
    if $0(t)>ncw:
     t=t[-ncw:]
    text(x+3,y+2,t,C_TXT)
    if cur:
     box(x+3+$0(t)*AW,y+3,2,LH-2,C_CUR)
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
  $? k=='left':
   j-=1
   if j<0:
    j=c-1
    i=(i-1)%r
  $? k=='down':
   i=(i+1)%r
  $? k=='up':
   i=(i-1)%r
  $? k in('del','backspace'):
   cells[i][j]=cells[i][j][:-1]
  $? k=='clear':
   cells[i][j]=''
  $&:
   a=ctrlaction(k)
   if a is $- $# $+ a!='wait' $+ a[0]=='ins':
    t=a[1][:$0(a[1])-a[2]]
   $? a is $- $#:
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
 '$L()':('','$L',''),'root(,)':('','root',''),
 '()/()':('','frac',''),'$J()':('','$J',''),
 'e^':('e','pow',''),'10^':('10','pow','')}
MATHTPL=(('Fraction','()/()'),('Power  x^n','^'),('Square root','$L()'),
 ('n-th root','root(,)'),('Absolute value','$J()'),('e^x','e^'))
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
$, ed_parent():
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
 n=3 if kind in('frac','root')$& 2
 node=[kind]+[[]$) i in $*(n-1)]
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
 if p<$0(r):
  if $/(r[p])is $p:
   G['pos']=p+1
  $&:
   G['path'].$%((p,1))
   G['pos']=0
 $? G['path']:
  i,sl=G['path'][-1]
  par,node=ed_parent()
  if sl+1<$0(node):
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
   G['path'].$%((p-1,$0(node)-1))
   G['pos']=$0(node[-1])
 $? G['path']:
  i,sl=G['path'][-1]
  par,node=ed_parent()
  if sl>1:
   G['path'][-1]=(i,sl-1)
   G['pos']=$0(node[sl-1])
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
   G['pos']=min(G['pos'],$0(node[t]))
 $? k=='pow' $+ d>0:
  G['path'].pop()
  G['pos']=i+1
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
   G['path'].$%((p-1,$0(it)-1))
   G['pos']=$0(it[-1])
 $? G['path']:
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
 if node[0]!='pow' or G['pos']!=$0(r)or $- r:
  $!
 $@=0
 $) it in r:
  if it=='(':
   $@+=1
  $? it==')':
   $@-=1
 if $@<=0:
  G['pos']=G['path'].pop()[0]+1
$, ed_text(row=$#):
 if row is $#:
  row=G['row']
 $<=''
 $) it in row:
  if $/(it)is $p:
   $<+=it
   $4
  k=it[0]
  if k=='frac':
   f=grp(ed_text(it[1]),$A)+'/'+grp(ed_text(it[2]),$2)
   $<+=f if $0(row)==1 $& '('+f+')'
  $? k=='pow':
   e=ed_text(it[1])
   $<+='^'+(e if e.isdigit()or($0(e)==1 $+ e.isalpha())or enclosed(e)
 $& '('+e+')')
  $? k=='$L':
   $<+='$L('+ed_text(it[1])+')'
  $? k=='root':
   $<+='root('+ed_text(it[2])+','+ed_text(it[1])+')'
  $? k=='$J':
   $<+='$J('+ed_text(it[1])+')'
 $! $<
$, enclosed(s):
 if $0(s)<2 or s[0]!='(' or s[-1]!=')':
  $! $2
 $@=0
 $) i in $*($0(s)):
  if s[i]=='(':
   $@+=1
  $? s[i]==')':
   $@-=1
   if $@==0 $+ i<$0(s)-1:
    $! $2
 $! $A
''',
r'''$, grp(s,num):
 ok=s!=''
 digits=$A
 $) c in s:
  if $-(c.isdigit()or c=='.'):
   digits=$2
  if $-(c.isdigit()or c=='.' or c.isalpha()):
   ok=$2
 if ok $+ $- digits $+ $- s.isalpha():
  ok=$2
 i=s.find('(')
 if i>0 $+ s[:i].isalpha()$+ enclosed(s[i:]):
  ok=$A
 $! s if ok or enclosed(s)$& '('+s+')'
$, ed_cp(row):
 $![it if $/(it)is $p $&[it[0]]+[ed_cp(r)$) r in it[1:]]$) it in row]
$, ed_snap():
 $!(ed_cp(G['row']),$I(G['path']),G['pos'],ed_text())
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
 w,a,d=meas(it[1])
 $!(w+11,a+3,d)
$, line(x1,y1,x2,y2):
 color(G.get('ink',C_TXT))
 try:
  G['d'].draw_line(x1,y1,x2,y2)
 $6 $>:
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
 $) i in $*($0(row)):
  if cur $+ i==G['pos']:
   G['cxy']=(x,y,A_,D_)
  x+=itemdraw(row[i],x,y,dr)
 if cur $+ G['pos']==$0(row):
  G['cxy']=(x,y,A_,D_)
 $! x-x0
$, itemdraw(it,x,y,dr):
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
  $) i in $*($0(it[1])):
   cx=x+5
   r=it[1][i]
   $) j in $*($0(r)):
    w2=meas(r[j])[0]
    rowdraw(r[j],cx+(cw[j]-w2)//2,cy+ra[i],dr)
    cx+=cw[j]+8
   cy+=ra[i]+rd[i]+7
  $! W
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
$, catalog():
 _load('cashelp')
 names=[]
 $) key,title,words in CATS:
  if key in('conv','cmd'):
   $4
  $) wd in words.split():
   if wd[0].isalpha()$+ wd $- in names $+ okname(wd):
    names.$%(wd)
 names.sort(key=$5 t:t.lower())
 j=choose('Catalog: $/ a letter',names,$A)
 if j is $- $#:
  insert(names[j]+'()',1)
$, okname(wd):
 $) c in wd:
  if $-(c.isalpha()or c.isdigit()or c=='_'):
   $! $2
 $! $A
$, ed_stops():
 $<=[]
 $, walk(row,path):
  $) i in $*($0(row)+1):
   $<.$%((path,i,(i>0 $+ row[i-1]==',')or(bool(path)$+ i==$0(row))))
   if i<$0(row)$+ $/(row[i])is $- $p:
    $) sl in $*(1,$0(row[i])):
     walk(row[i][sl],path+[(i,sl)])
 walk(G['row'],[])
 $! $<
$, ed_tab(d):
 ps=ed_stops()
 cur=0
 $) j in $*($0(ps)):
  if ps[j][0]==G['path']$+ ps[j][1]==G['pos']:
   cur=j
 t=$0(ps)-1 if d>0 $& 0
 if d>0:
  $) j in $*(cur+1,$0(ps)):
   if ps[j][2]:
    t=j
    $R
 $&:
  $) j in $*(cur-1,-1,-1):
   if ps[j][2]:
    t=j
    $R
 G['path']=$I(ps[t][0])
 G['pos']=ps[t][1]
SAFE='0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_+-*/^().,;=<>{}[]! \u221a\u03c0\u221e\u2260\u2264\u2265\u03b8'
SHOW={'pi':'\u03c0','$[':'\u221e','theta':'\u03b8'}
SHOWF={'sumseq':'\u03a3','prodseq':'\u03a0','$j':'\u222b'}
REL2={'=':'=','/=':'\u2260','<':'<','>':'>','<=':'\u2264','>=':'\u2265'}
DOT='\u00b7'
$, anyfunc(n):
 $! $A
$, tolayout(s):
 c=G.setdefault('lay',{})
 if s in c:
  $! c[s]
 t=s.replace('\n ','').replace('\n','')
 ok=t!='' $+ $0(t)<400
 $) ch in t:
  if ch $- in SAFE:
   ok=$2
   $R
 if ok:
  u=t.replace(' $+ ','').replace(' or ','').replace(' xor ','').replace('$- ','')
  if ' ' in u:
   ok=$2
 r=$#
 if ok:
  try:
   r=[]
   lay(parse(t,anyfunc),r)
   w,a,d=meas(r)
   r=(r,w,a,d)
  $6 $>:
   r=$#
 if $0(c)>80:
  c.clear()
 c[s]=r
 $! r
$, prec(t):
 if $/(t)is $- $3:
  $! 5
 h=t[0]
 if h in('+','-'):
  $! 1
 if h in('*','$r'):
  $! 2
 if h=='^':
  $! 4
 if h in REL2:
  $! 0
 if h in('$+','or','xor','$-'):
  $!-1
 $! 5
$, layp(t,$<,need):
 if need:
  $<.$%('(')
  lay(t,$<)
  $<.$%(')')
 $&:
  lay(t,$<)
$, sublay(t):
 r=[]
 lay(t,r)
 $! r
''',
r'''$, lay(t,$<):
 tt=$/(t)
 if tt is $t:
  $<.${($I($p(t)))
  $!
 if tt is $F:
  $<.${($I(fmt(t)))
  $!
 if tt is $p:
  $<.${($I(SHOW.get(t,t)))
  $!
 h=t[0]
 if h=='+' or h=='-':
  lay(t[1],$<)
  $<.$%(h)
  layp(t[2],$<,prec(t[2])<=(1 if h=='-' $& 0)
 or($/(t[2])is $3 $+ t[2][0]=='$r'))
 $? h=='*':
  layp(t[1],$<,prec(t[1])<2)
  $<.$%(DOT)
  layp(t[2],$<,prec(t[2])<2 or($/(t[2])is $3 $+ t[2][0]=='$r'))
 $? h=='$r':
  $<.$%('-')
  layp(t[1],$<,prec(t[1])<=1)
 $? h=='/':
  $<.$%(['frac',sublay(t[1]),sublay(t[2])])
 $? h=='^':
  b=t[1]
  need=prec(b)<5 or($/(b)is $3 $+(b[0]=='/' or(b[0]=='call' $+ b[1]in('$L','root'))))
  layp(b,$<,need)
  $<.$%(['pow',sublay(t[2])])
 $? h=='call':
  $B=t[1]
  $N=t[2:]
  if $B=='$L' $+ $0($N)==1:
   $<.$%(['$L',sublay($N[0])])
  $? $B=='root' $+ $0($N)==2:
   $<.$%(['root',sublay($N[1]),sublay($N[0])])
  $? $B=='$J' $+ $0($N)==1:
   $<.$%(['$J',sublay($N[0])])
  $&:
   nm=SHOWF.get($B)if OPT['uni']$& $#
   $<.${($I(nm or tiname($B)))
   $<.$%('(')
   $) i in $*($0($N)):
    if i:
     $<.$%(',')
    lay($N[i],$<)
   $<.$%(')')
 $? h=='$I':
  $<.$%('{')
  $) i in $*(1,$0(t)):
   if i>1:
    $<.$%(',')
   lay(t[i],$<)
  $<.$%('}')
 $? h=='mat':
  $<.$%(['mat',[[sublay(c)$) c in r[1:]]$) r in t[1:]]])
 $? h in REL2:
  lay(t[1],$<)
  $<.${($I(REL2[h]))
  lay(t[2],$<)
 $? h in('$+','or','xor'):
  lay(t[1],$<)
  $<.${($I(' '+h+' '))
  lay(t[2],$<)
 $? h=='$-':
  $<.${($I('$- '))
  layp(t[1],$<,prec(t[1])<0)
 $? h=='!':
  layp(t[1],$<,prec(t[1])<5 or $/(t[1])is $3 $+ t[1][0]=='/')
  $<.$%('!')
 $&:
  $n $P('no 2D form')
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
$, matsize($T):
 nc=max([$0(r)$) r in $T])
 cw=[0]*nc
 ra=[]
 rd=[]
 $) r in $T:
  a=A_
  d=D_
  $) j in $*($0(r)):
   w,ca,cd=meas(r[j])
   cw[j]=max(cw[j],w)
   a=max(a,ca)
   d=max(d,cd)
  ra.$%(a)
  rd.$%(d)
 W=sum(cw)+8*(nc-1)+10
 H=sum(ra)+sum(rd)+7*($0($T)-1)
 $! cw,ra,rd,W,H
$, blocks():
 $<=[]
 n=G['wrap']
 w=G['w']
 $) k in $*($0(G['hist'])):
  inp,res,bad=G['hist'][k]
  $) part,s,col in(('in',inp,C_TXT),('$<',res,C_ERR if bad $& C_RES)):
   lt=$# if bad $& tolayout(s)
   if lt is $- $#:
    r,rw,ra,rd=lt
    if rw<=w-10:
     $<.$%(('2d',(r,rw,ra,rd,col),ra+rd+4,k,part))
     $4
   pre='  ' if part=='$<' $& ''
   $) line in s.split('\n'):
    $) t in wrap(line,n-$0(pre)):
     $<.$%(('txt',(pre+t,col),LH,k,part))
 $! $<
$, startfor(bl,end,avail):
 hh=0
 i=end
 $G i>=0 $+ hh+bl[i][2]<=avail:
  hh+=bl[i][2]
  i-=1
 $! min(i+1,end)
$, fitfrom(bl,start,avail):
 hh=0
 i=start
 $G i<$0(bl)$+ hh+bl[i][2]<=avail:
  hh+=bl[i][2]
  i+=1
 $! max(start,i-1)
''',)
del _x
startgui()
