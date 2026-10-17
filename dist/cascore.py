import math
class CASError(Exception):
 pass
class ResourceLimit(CASError):
 pass
def err(msg):
 raise CASError(msg)
MAXTERMS=2000
MAXCELLS=2500
MAXLEN=5000
def toobig(what):
 raise ResourceLimit('Resource limit: '+what)
def cells(r,c):
 if not(isint(r)and isint(c))or r<1 or c<1:
  err('Dimensions must be positive integers')
 if r*c>MAXCELLS:
  toobig('a %dx%d matrix has more than %d entries'%(r,c,MAXCELLS))
CONSTS=('pi','e','i')
SPECIAL=('pi','e','i','inf','undef','true','false')
def igcd(a,b):
 if a<0:
  a=-a
 if b<0:
  b=-b
 while b:
  a,b=b,a%b
 return a
def ilcm(a,b):
 if a==0 or b==0:
  return 0
 return abs(a//igcd(a,b)*b)
def Q(n,d=1):
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
  return n
 return('Q',n,d)
HALF=('Q',1,2)
def isq(x):
 return type(x)is tuple and x[0]=='Q'
def isint(x):
 return type(x)is int
def isfl(x):
 return type(x)is float
def israt(x):
 t=type(x)
 return t is int or(t is tuple and x[0]=='Q')
def isnum(x):
 t=type(x)
 return t is int or t is float or(t is tuple and x[0]=='Q')
def nd(x):
 if type(x)is int:
  return x,1
 return x[1],x[2]
def tofl(x):
 t=type(x)
 if t is float:
  return x
 if t is int:
  return float(x)
 return x[1]/x[2]
def nadd(a,b):
 ta=type(a)
 tb=type(b)
 if ta is int and tb is int:
  return a+b
 if ta is float or tb is float:
  return tofl(a)+tofl(b)
 an,ad=nd(a)
 bn,bd=nd(b)
 if ad==bd:
  return Q(an+bn,ad)
 g=igcd(ad,bd)
 if g>1:
  ad//=g
  return Q(an*(bd//g)+bn*ad,ad*bd)
 return Q(an*bd+bn*ad,ad*bd)
def nmul(a,b):
 ta=type(a)
 tb=type(b)
 if ta is int and tb is int:
  return a*b
 if ta is float or tb is float:
  return tofl(a)*tofl(b)
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
 return Q(an*bn,ad*bd)
def nneg(a):
 if type(a)is tuple:
  return('Q',-a[1],a[2])
 return-a
def nsub(a,b):
 return nadd(a,nneg(b))
def ninv(a):
 t=type(a)
 if t is float:
  if a==0.0:
   err("Division by zero")
  return 1.0/a
 n,d=nd(a)
 return Q(d,n)
def ndiv(a,b):
 return nmul(a,ninv(b))
def nsign(a):
 if type(a)is tuple:
  a=a[1]
 if a>0:
  return 1
 if a<0:
  return-1
 return 0
def ncmp(a,b):
 return nsign(nsub(a,b))
def nfloor(a):
 t=type(a)
 if t is int:
  return a
 if t is float:
  if a!=a or a in(float('inf'),float('-inf')):
   err("Domain error")
  return int(math.floor(a))
 return a[1]//a[2]
def nabs(a):
 if nsign(a)<0:
  return nneg(a)
 return a
def nipow(a,k):
 if k<0:
  return nipow(ninv(a),-k)
 if type(a)is float:
  return a**k
 n,d=nd(a)
 return Q(n**k,d**k)
def iroot(n,k):
 if n<2:
  return n
 x=int(math.pow(n,1.0/k))if n<10**300 else 1<<((len(bin(n))-2)//k+1)
 if x<1:
  x=1
 while True:
  y=((k-1)*x+n//(x**(k-1)))//k
  if y>=x:
   break
  x=y
 while x**k>n:
  x-=1
 while(x+1)**k<=n:
  x+=1
 return x
def isqrt(n):
 return iroot(n,2)
SMALLP=None
def smallprimes():
 global SMALLP
 if SMALLP is None:
  N=1000
  s=bytearray(N)
  ps=[]
  for i in range(2,N):
   if not s[i]:
    ps.append(i)
    for j in range(i*i,N,i):
     s[j]=1
  SMALLP=ps
 return SMALLP
def isnode(e,h):
 return type(e)is tuple and e[0]==h
def head(e):
 if type(e)is tuple:
  return e[0]
 return None
def okey(e):
 return repr(e)
def has(e,x):
 if e==x:
  return True
 if type(e)is tuple and e[0]!='Q':
  for a in e[1:]:
   if has(a,x):
    return True
 return False
def freeof(e,x):
 return not has(e,x)
def freeofall(e,xs):
 for x in xs:
  if has(e,x):
   return False
 return True
def symbols(e,out=None):
 if out is None:
  out=[]
 t=type(e)
 if t is str:
  if e not in SPECIAL and e not in out:
   out.append(e)
 elif t is tuple and e[0]!='Q' and e[0]!='str':
  for a in e[1:]:
   symbols(a,out)
 return out
def isconst(e):
 t=type(e)
 if t is str:
  return e in SPECIAL
 if t is tuple and e[0]!='Q':
  if e[0]=='str':
   return False
  for a in e[1:]:
   if not isconst(a):
    return False
 return True
def hasfloat(e):
 t=type(e)
 if t is float:
  return True
 if t is tuple and e[0]!='Q':
  for a in e[1:]:
   if hasfloat(a):
    return True
 return False
def coef_rest(a):
 if type(a)is tuple and a[0]=='*' and isnum(a[1]):
  if len(a)==3:
   return a[1],a[2]
  return a[1],('*',)+a[2:]
 return 1,a
def cmul(c,r):
 if type(c)is int and c==1:
  return r
 if type(r)is tuple and r[0]=='*':
  if isnum(r[1]):
   c=nmul(c,r[1])
   if type(c)is int and c==1:
    return('*',)+r[2:]if len(r)>3 else r[2]
   return('*',c)+r[2:]
  return('*',c)+r[1:]
 return('*',c,r)
def add(*args):
 return add_list(args)
def add_list(args):
 num=0
 terms={}
 order=[]
 st=list(args)
 infs=0
 while st:
  a=st.pop()
  t=type(a)
  if t is int or t is float:
   num=nadd(num,a)
   continue
  if t is tuple:
   h=a[0]
   if h=='Q':
    num=nadd(num,a)
    continue
   if h=='+':
    st.extend(a[1:])
    continue
   if h=='*' and isnum(a[1]):
    c=a[1]
    r=a[2]if len(a)==3 else('*',)+a[2:]
   else:
    c=1
    r=a
  else:
   if a=='undef':
    return 'undef'
   c=1
   r=a
  if r=='inf':
   s=nsign(c)
   if s==0:
    continue
   if infs and infs!=s:
    return 'undef'
   infs=s
   continue
  if r in terms:
   terms[r]=nadd(terms[r],c)
  else:
   terms[r]=c
   order.append(r)
 if infs:
  return 'inf' if infs>0 else('*',-1,'inf')
 out=[]
 for r in order:
  c=terms[r]
  if c==0:
   continue
  out.append(cmul(c,r))
 if num!=0 or not out:
  if out and num==0:
   pass
  else:
   out.append(num)
 if len(out)==1:
  return out[0]
 out.sort(key=okey)
 return('+',)+tuple(out)
def isrrad(e):
 return type(e)is tuple and e[0]=='^' and type(e[1])is int and isq(e[2])
def mul(*args):
 return mul_list(args)
def mul_list(args):
 coef=1
 bases={}
 order=[]
 st=list(args)
 while st:
  a=st.pop()
  t=type(a)
  if t is int or t is float:
   coef=nmul(coef,a)
   continue
  if t is tuple:
   h=a[0]
   if h=='Q':
    coef=nmul(coef,a)
    continue
   if h=='*':
    st.extend(a[1:])
    continue
   if h=='^':
    b=a[1]
    x=a[2]
   else:
    b=a
    x=1
  else:
   if a=='undef':
    return 'undef'
   b=a
   x=1
  if b in bases:
   bases[b]=add(bases[b],x)
  else:
   bases[b]=x
   order.append(b)
 if coef==0:
  if 'inf' in bases:
   return 'undef'
  for b in order:
   if b=='undef' or has(b,'undef'):
    return 'undef'
  return coef
 facs=[]
 rad={}
 radorder=[]
 def collect(p):
  c=1
  t=type(p)
  if t is int or t is float or(t is tuple and p[0]=='Q'):
   return p
  if t is tuple and p[0]=='*':
   items=p[1:]
  else:
   items=(p,)
  for f in items:
   if isnum(f):
    c=nmul(c,f)
   elif isrrad(f):
    ex=f[2]
    if ex in rad:
     rad[ex]=rad[ex]*f[1]
     radorder.append(None)
    else:
     rad[ex]=f[1]
     radorder.append(ex)
   else:
    facs.append(f)
  return c
 for b in order:
  p=pw(b,bases[b])
  if p=='undef':
   return 'undef'
  coef=nmul(coef,collect(p))
 if rad:
  multi=len(radorder)!=len(rad)
  if multi:
   items=[(ex,rad[ex])for ex in radorder if ex is not None]
   rad.clear()
   del radorder[:]
   pend=[]
   for ex,b in items:
    pend.append(pw_num(b,ex))
   for p in pend:
    coef=nmul(coef,collect(p))
  for ex in rad:
   facs.append(('^',rad[ex],ex))
 if coef==0:
  return 0
 if 'inf' in facs:
  if len(facs)==1 or True:
   coef=nsign(coef)if type(coef)is not float else(1.0 if coef>0 else-1.0)
   if type(coef)is float:
    coef=int(coef)
 if not facs:
  return coef
 if len(facs)>1:
  algs=[f for f in facs if isnode(f,'+')and isalg(f)]
  if algs and all([isalg(f)for f in facs]):
   r=coef
   for f in facs:
    r=expand_mul(r,f)
   return r
 if len(facs)==1:
  f=facs[0]
  if type(coef)is int and coef==1:
   return f
  if type(f)is tuple and f[0]=='+':
   return add_list([mul(coef,t)for t in f[1:]])
  return('*',coef,f)
 facs.sort(key=okey)
 if type(coef)is int and coef==1:
  return('*',)+tuple(facs)
 return('*',coef)+tuple(facs)
def neg(a):
 return mul(-1,a)
def sub(a,b):
 return add(a,mul(-1,b))
def div(a,b):
 return mul(a,pw(b,-1))
def inv(a):
 return pw(a,-1)
def sqrt(a):
 return pw(a,HALF)
def factor_int_small(n):
 fs=[]
 for p in smallprimes():
  if p*p>n:
   break
  if n%p==0:
   k=0
   while n%p==0:
    n//=p
    k+=1
   fs.append((p,k))
 return fs,n
def radical(n,q):
 if n<2:
  return n,1
 a=1
 m=1
 fs,rest=factor_int_small(n)
 for p,k in fs:
  a*=p**(k//q)
  m*=p**(k%q)
 if rest>1:
  r=iroot(rest,q)
  if r**q==rest:
   a*=r
  else:
   m*=rest
 return a,m
def ipow_root(n,p,q):
 if ibits(n)*p>2000 or q>60:
  return('^',n,Q(p,q))
 a,m=radical(n**p,q)if p>1 else radical(n,q)
 if m==1:
  return a
 ex=Q(1,q)
 k=2
 best=None
 while(1<<k)<=m and k<=64:
  r=iroot(m,k)
  if r**k==m:
   best=(r,k)
  k+=1
 if best is not None:
  m=best[0]
  ex=Q(best[1],q)
 if ex==1:
  return a*m
 if isint(ex):
  return a*m**ex
 if a==1:
  return('^',m,ex)
 return('*',a,('^',m,ex))
MAXBITS=12000
def ibits(n):
 if n==0:
  return 0
 h='%x'%abs(n)
 v=int(h[0],16)
 return 4*len(h)-(3 if v<2 else 2 if v<4 else 1 if v<8 else 0)
def bigpow(b,x):
 n,d=nd(b)
 if d==1 and abs(n)<=1:
  return False
 return abs(x)*(ibits(n)+(ibits(d)if d>1 else 0))>MAXBITS
def pw_num(b,x):
 if type(b)is float or type(x)is float:
  bf=tofl(b)
  xf=tofl(x)
  if bf==0.0:
   if xf>0:
    return 0.0
   if xf==0:
    return 1.0
   return 'undef'
  if bf!=bf or xf!=xf:
   return 'undef'
  if bf<0 and(xf in(float('inf'),float('-inf'))or xf!=math.floor(xf)):
   if israt(x)and nd(x)[1]%2==1:
    r=(-bf)**xf
    return-r if nd(x)[0]%2 else r
   z=complex(bf)**xf
   return fromcomplex(z)
  try:
   return bf**xf
  except OverflowError:
   return 'inf'
 if type(x)is int:
  if b==0:
   if x<0:
    return 'undef'
   return 0
  if bigpow(b,x):
   return('^',b,x)
  return nipow(b,x)
 p,q=nd(x)
 if b==0:
  return 0 if p>0 else 'undef'
 if nsign(b)<0:
  if q%2==1:
   r=pw_num(nneg(b),x)
   if p%2:
    return mul(-1,r)
   return r
  if q==2:
   return mul(pw('i',p),pw_num(nneg(b),x))
  return('^',b,x)
 if b==1:
  return 1
 n,d=nd(b)
 k=p//q
 if bigpow(b,k+1):
  return('^',b,x)
 f=Q(p-k*q,q)
 res=nipow(b,k)
 if f==0:
  return res
 fp,fq=nd(f)
 parts=[]
 if n>1:
  parts.append(ipow_root(n,fp,fq))
 if d>1:
  parts.append(Q(1,d))
  parts.append(ipow_root(d,fq-fp,fq))
 c=res
 facs=[]
 for pt in parts:
  if isnum(pt):
   c=nmul(c,pt)
  elif pt[0]=='*':
   c=nmul(c,pt[1])
   facs.append(pt[2])
  else:
   facs.append(pt)
 if len(facs)==2:
  if facs[0][2]==facs[1][2]:
   return mul(c,pw_num(facs[0][1]*facs[1][1],facs[0][2]))
  facs.sort(key=okey)
 if not facs:
  return c
 if c==1:
  if len(facs)==1:
   return facs[0]
  return('*',)+tuple(facs)
 return('*',c)+tuple(facs)
def isposconst(e):
 if isnum(e):
  return nsign(e)>0
 if e=='pi' or e=='e':
  return True
 if isrrad(e):
  return e[1]>0
 if isnode(e,'^')and(e[1]=='e' or e[1]=='pi')and isreal_expr(e[2]):
  return True
 return False
def isalg(e):
 t=type(e)
 if t is int or t is float:
  return True
 if t is str:
  return e=='i'
 h=e[0]
 if h=='Q':
  return True
 if h=='^':
  return isnum(e[1])and isnum(e[2])
 if h=='+' or h=='*':
  for a in e[1:]:
   if not isalg(a):
    return False
  return True
 return False
def pw(b,x):
 if x==0:
  if b=='undef' or b=='inf':
   return 'undef'
  return 1
 if type(x)is int and x==1:
  return b
 if b=='undef' or x=='undef':
  return 'undef'
 bn=isnum(b)
 xn=isnum(x)
 if bn and xn:
  return pw_num(b,x)
 if b==1 and type(b)is int:
  return 1
 if b=='inf':
  if xn:
   return 'inf' if nsign(x)>0 else 0
  if x=='inf':
   return 'inf'
 if xn and b==0:
  return 0 if nsign(x)>0 else 'undef'
 if b=='i' and type(x)is int:
  r=x%4
  return(1,'i',-1,('*',-1,'i'))[r]
 if x=='inf' and bn:
  if nabs(b)==1:
   return 'undef' if b==1 else 'undef'
  if ncmp(nabs(b),1)>0:
   return 'inf' if nsign(b)>0 else 'undef'
  return 0
 if b=='e':
  if x=='inf':
   return 'inf'
  if isnode(x,'*')and len(x)==3 and x[1]==-1 and x[2]=='inf':
   return 0
  if type(x)is float:
   return math.exp(x)
  if isnode(x,'ln'):
   return x[1]
  if isnode(x,'*'):
   c,r=coef_rest(x)
   if isnode(r,'ln')and israt(c):
    return pw(r[1],c)
  if isnode(x,'+'):
   outs=[]
   rest=[]
   for t in x[1:]:
    c,r=coef_rest(t)
    if isnode(r,'ln')and israt(c):
     outs.append(pw(r[1],c))
    else:
     rest.append(t)
   if outs:
    return mul_list(outs+[pw('e',add_list(rest))])
  if isnode(x,'*')and 'i' in x and 'pi' in x:
   c,r=coef_rest(x)
   if r==('*','i','pi')and israt(c):
    return add(cos_(mul(c,'pi')),mul('i',sin_(mul(c,'pi'))))
 if b!='e' and isconst(b)and isconst(x)and not israt(x)and(has(b,'i')or has(x,'i'))and not hasfloat(x):
  L=fn('ln',b)
  if not isnode(L,'ln')and not(isnode(L,'+')and any([isnode(t,'ln')for t in L[1:]])):
   return pw('e',expand(mul(x,L)))
 if type(b)is tuple:
  h=b[0]
  if h=='^':
   bb=b[1]
   ee=b[2]
   if type(x)is int:
    return pw(bb,mul(ee,x))
   if isposconst(bb):
    return pw(bb,mul(ee,x))
   if israt(ee)and israt(x):
    r=nmul(ee,x)
    if type(ee)is int:
     if ee%2==0:
      if type(r)is int and r%2==0:
       return pw(bb,r)
      return pw(fn('abs',bb),r)
     return pw(bb,r)
    if nd(ee)[0]%2==1 and nd(ee)[1]%2==1:
     return pw(bb,r)
    if nd(ee)[0]%2==1:
     return pw(bb,r)
  elif h=='*':
   if type(x)is int:
    return mul_list([pw(f,x)for f in b[1:]])
   outs=[]
   rest=[]
   for f in b[1:]:
    if isnum(f):
     if nsign(f)>0:
      outs.append(pw(f,x))
     elif f!=-1:
      outs.append(pw(nneg(f),x))
      rest.append(-1)
     else:
      rest.append(f)
    elif isposconst(f)or isnode(f,'abs'):
     outs.append(pw(f,x))
    else:
     rest.append(f)
   if outs:
    return mul_list(outs+[pw(mul_list(rest),x)])
  elif h=='abs':
   if type(x)is int and x%2==0:
    return pw(b[1],x)
  elif h=='+':
   if x==HALF and isalg(b)and not has(b,'i'):
    dn=denest(b)
    if dn is not None:
     return dn
   if isq(x)and x[2]==2 and nsign(x)<0 and isalg(b)and not has(b,'i'):
    dn=denest(b)
    if dn is not None:
     return pw(pw(dn,-1),-x[1])if x[1]!=-1 else pw(dn,-1)
   if type(x)is int and x!=1 and not isalg(b):
    c=sumcontent(b)
    if c!=1:
     return mul(pw(c,x),pw(mul(ninv(c),b),x))
    if leadneg(b):
     nb=mul(-1,b)
     if x%2==0:
      return pw(nb,x)
     return mul(-1,pw(nb,x))
   if type(x)is int and isalg(b):
    if x>0 and x<=64:
     return expand_pow(b,x)
    if x<0 and x>=-64:
     r=rationalize_inv(b)
     if r is not None:
      if x==-1:
       return r
      return expand_pow(r,-x)
 return('^',b,x)
def tdeg(r):
 d=0
 fs=r[1:]if isnode(r,'*')else(r,)
 for f in fs:
  if type(f)is str and f not in SPECIAL:
   d+=1
  elif isnode(f,'^')and type(f[1])is str and f[1]not in SPECIAL and isnum(f[2]):
   d+=tofl(f[2])
 return d
def leadneg(b):
 best=None
 bk=None
 for t in b[1:]:
  if isnum(t):
   continue
  c,r=coef_rest(t)
  k=(-tdeg(r),okey(r))
  if bk is None or k<bk:
   bk=k
   best=c
 if best is None:
  return False
 return nsign(best)<0 if isnum(best)else False
def sumcontent(b):
 g=0
 L=1
 for t in b[1:]:
  c,r=coef_rest(t)
  if not israt(c):
   return 1
  n,d=nd(c)
  g=igcd(g,n)
  L=ilcm(L,d)
 if g==0:
  return 1
 return Q(g,L)
def denest(b):
 a=0
 c=0
 n=None
 for t in b[1:]:
  if israt(t):
   a=nadd(a,t)
   continue
  cc,r=coef_rest(t)
  if isrrad(r)and r[2]==HALF and israt(cc)and(n is None or n==r[1]):
   n=r[1]
   c=nadd(c,cc)
  else:
   return None
 if n is None or c==0:
  return None
 d2=nsub(nmul(a,a),nmul(nmul(c,c),n))
 if nsign(d2)<0:
  return None
 dn,dd=nd(d2)
 rn=isqrt(dn)
 rd=isqrt(dd)
 if rn*rn!=dn or rd*rd!=dd:
  return None
 d=Q(rn,rd)
 p=ndiv(nadd(a,d),2)
 m=ndiv(nsub(a,d),2)
 if nsign(p)<0 or nsign(m)<0:
  return None
 r=add(pw(p,HALF),mul(nsign(c),pw(m,HALF)))
 if isnode(r,'+')and len(r)<=3:
  return r
 return None
def expand_mul(a,b):
 ta=a[1:]if isnode(a,'+')else(a,)
 tb=b[1:]if isnode(b,'+')else(b,)
 if len(ta)*len(tb)>4*MAXTERMS:
  toobig('the expansion would have more than %d terms'%MAXTERMS)
 out=[]
 for u in ta:
  for v in tb:
   out.append(mul(u,v))
 return add_list(out)
def expand_pow(b,n):
 t=len(b)-1 if isnode(b,'+')else 1
 if t>1 and not isconst(b):
  c=1
  for k in range(1,t):
   c=c*(n+k)//k
   if c>MAXTERMS:
    toobig('the expansion would have more than %d terms'%MAXTERMS)
 r=1
 p=b
 while n>0:
  if n&1:
   r=expand_mul(r,p)
  n>>=1
  if n:
   p=expand_mul(p,p)
 return r
def rationalize_inv(b):
 re_,im_=reim(b)
 if im_!=0:
  d=add(mul(re_,re_),mul(im_,im_))
  d=expand(d)
  if isnode(d,'+'):
   r2=rationalize_inv(d)
   if r2 is None:
    return None
  else:
   r2=pw(d,-1)
  return expand_mul(sub(re_,mul('i',im_)),r2)
 terms=b[1:]if isnode(b,'+')else(b,)
 kern=None
 kerns=[]
 for t in terms:
  c,r=coef_rest(t)
  if r!=1 and not isnum(r):
   if isrrad(r)and r[2]==HALF:
    if r not in kerns:
     kerns.append(r)
   else:
    return None
 if not kerns or len(kerns)>3:
  return None
 kern=kerns[0]
 if len(kerns)>1:
  A=add_list([t for t in terms if coef_rest(t)[1]!=kern])
  B=add_list([coef_rest(t)[0]for t in terms if coef_rest(t)[1]==kern])
  den=expand(sub(mul(A,A),mul(B,B,kern[1])))
  if den==0:
   return None
  if isnode(den,'+'):
   r2=rationalize_inv(den)
   if r2 is None:
    return None
  else:
   r2=pw(den,-1)
  return expand_mul(sub(A,mul(B,kern)),r2)
 a0=0
 a1=0
 for t in terms:
  c,r=coef_rest(t)
  if r==kern:
   a1=nadd(a1,c)
  else:
   a0=add(a0,t)
 den=sub(mul(a0,a0),mul(nmul(a1,a1),kern[1]))
 if den==0:
  return None
 return expand_mul(sub(a0,mul(a1,kern)),pw(den,-1))
def reim(e):
 t=type(e)
 if t is int or t is float:
  return e,0
 if t is str:
  if e=='i':
   return 0,1
  return e,0
 h=e[0]
 if h=='Q':
  return e,0
 if h=='+':
  rs=[]
  ims=[]
  for a in e[1:]:
   r,i=reim(a)
   rs.append(r)
   ims.append(i)
  return add_list(rs),add_list(ims)
 if h=='*':
  r=1
  i=0
  for a in e[1:]:
   ar,ai=reim(a)
   if ai==0:
    r=mul(r,ar)
    i=mul(i,ar)
   else:
    r,i=sub(mul(r,ar),mul(i,ai)),add(mul(r,ai),mul(i,ar))
  return r,i
 if h=='^':
  b=e[1]
  x=e[2]
  if not has(b,'i')and not has(x,'i'):
   if isnum(x)and not israt(x):
    return e,0
   if israt(x)and nd(x)[1]%2==0:
    if isconst(b):
     v=cv(b)
     if v is not None and type(v)is not complex and v<0:
      return reim_generic(e)
    return e,0
   return e,0
  if type(x)is int:
   br,bi=reim(b)
   if x>0:
    z=expand_pow(add(br,mul('i',bi)),x)
    if has(z,'i')and z!=e:
     return reim(z)
   elif isconst(b):
    r=rationalize_inv(b)
    if r is not None:
     return reim(expand_pow(r,-x))if x!=-1 else reim(r)
  return reim_generic(e)
 if h in('list','mat','str'):
  return e,0
 for a in e[1:]:
  if has(a,'i'):
   return reim_generic(e)
 return e,0
def cv(u):
 try:
  v=nval(u)
 except(CASError,ValueError,ZeroDivisionError,OverflowError,TypeError):
  return None
 if v!=v:
  return None
 if type(v)is complex:
  if v.real!=v.real or v.imag!=v.imag:
   return None
  if abs(v.real)==float('inf')or abs(v.imag)==float('inf'):
   return None
 elif abs(v)==float('inf'):
  return None
 return v
def reim_generic(e):
 if isconst(e):
  v=cv(e)
  if v is None:
   return('real',e),('imag',e)
  z=complex(v)
  return z.real,z.imag
 return('real',e),('imag',e)
def conj(e):
 r,i=reim(e)
 return sub(r,mul('i',i))
def fromcomplex(z):
 if type(z)is not complex:
  return z
 if z.imag==0:
  return z.real
 if z.real==0:
  return mul(z.imag,'i')
 return add(z.real,mul(z.imag,'i'))
FSIMP={}
def fn(name,*args):
 if len(args)==1 and type(args[0])is list:
  args=tuple(args[0])
 for a in(args[:1]if name=='when' else args):
  if a=='undef':
   return 'undef'
 f=FSIMP.get(name)
 if f is not None:
  r=f(*args)
  if r is not None:
   return r
 return(name,)+tuple(args)
def isneg(e):
 if isnum(e):
  return nsign(e)<0
 if isnode(e,'*'):
  return isnum(e[1])and nsign(e[1])<0
 if isnode(e,'+'):
  return leadneg(e)
 return False
def isreal_expr(e):
 if isnum(e):
  return True
 if type(e)is str:
  return e!='i' and e!='undef'
 return not has(e,'i')
def fval(name,x):
 return fromcomplex(NUMF[name](x))
def fvalc(name,u):
 try:
  v=NUMF[name](nval(u))
 except(CASError,ValueError,ZeroDivisionError,OverflowError,TypeError):
  return None
 if type(v)is complex:
  if v.real!=v.real or v.imag!=v.imag:
   return None
 elif v!=v:
  return None
 return fromcomplex(v)
def pi_coef(u):
 if u=='pi':
  return 1
 if u==0:
  return 0
 if isnode(u,'*')and len(u)==3 and u[2]=='pi' and israt(u[1]):
  return u[1]
 return None
def split_pi(u):
 if isnode(u,'+'):
  for t in u[1:]:
   c=pi_coef(t)
   if c is not None and c!=0:
    rest=add_list([s for s in u[1:]if s is not t])
    return c,rest
 return None
TRIGT=None
def trig_table():
 global TRIGT
 if TRIGT is None:
  s2=sqrt(2)
  s3=sqrt(3)
  s5=sqrt(5)
  s6=sqrt(6)
  q=Q
  T={}
  T[0]=0
  T[q(1,12)]=mul(q(1,4),sub(s6,s2))
  T[q(1,10)]=mul(q(1,4),sub(s5,1))
  T[q(1,8)]=mul(HALF,sqrt(sub(2,s2)))
  T[q(1,6)]=HALF
  T[q(1,5)]=mul(q(1,4),sqrt(sub(10,mul(2,s5))))
  T[q(1,4)]=mul(HALF,s2)
  T[q(3,10)]=mul(q(1,4),add(s5,1))
  T[q(1,3)]=mul(HALF,s3)
  T[q(3,8)]=mul(HALF,sqrt(add(2,s2)))
  T[q(2,5)]=mul(q(1,4),sqrt(add(10,mul(2,s5))))
  T[q(5,12)]=mul(q(1,4),add(s6,s2))
  T[HALF]=1
  TT={}
  TT[0]=0
  TT[q(1,12)]=sub(2,s3)
  TT[q(1,8)]=sub(s2,1)
  TT[q(1,6)]=mul(q(1,3),s3)
  TT[q(1,4)]=1
  TT[q(1,3)]=s3
  TT[q(3,8)]=add(s2,1)
  TT[q(5,12)]=add(2,s3)
  TT[q(1,5)]=sqrt(sub(5,mul(2,s5)))
  TT[q(2,5)]=sqrt(add(5,mul(2,s5)))
  TT[q(1,10)]=mul(q(1,5),sqrt(sub(25,mul(10,s5))))
  TT[q(3,10)]=mul(q(1,5),sqrt(add(25,mul(10,s5))))
  TRIGT=(T,TT)
 return TRIGT
def sin_pi(c):
 c=nsub(c,nmul(2,nfloor(nmul(c,HALF))))
 sg=1
 if ncmp(c,1)>=0:
  c=nsub(c,1)
  sg=-1
 if ncmp(c,HALF)>0:
  c=nsub(1,c)
 T=trig_table()[0]
 if c in T:
  return mul(sg,T[c])
 if sg<0:
  return neg(('sin',mul(c,'pi')))
 return('sin',mul(c,'pi'))
def tan_pi(c):
 c=nsub(c,nfloor(c))
 sg=1
 if ncmp(c,HALF)>0:
  c=nsub(1,c)
  sg=-1
 if c==HALF:
  return 'undef'
 TT=trig_table()[1]
 if c in TT:
  return mul(sg,TT[c])
 return mul(sg,('tan',mul(c,'pi')))
def sin_(u):
 if isnum(u):
  if u==0:
   return 0
  if type(u)is float:
   return math.sin(u)
  if nsign(u)<0:
   return neg(fn('sin',neg(u)))
  return None
 if u=='inf' or u==('*',-1,'inf'):
  return 'undef'
 c=pi_coef(u)
 if c is not None:
  return sin_pi(c)
 if hasfloat(u)and isconst(u):
  return fvalc('sin',u)
 if isneg(u):
  return neg(fn('sin',neg(u)))
 sp=split_pi(u)
 if sp is not None:
  c,rest=sp
  c=nsub(c,nmul(2,nfloor(nmul(c,HALF))))
  if c==0:
   return fn('sin',rest)
  if c==1:
   return neg(fn('sin',rest))
  if c==HALF:
   return fn('cos',rest)
  if c==Q(3,2):
   return neg(fn('cos',rest))
  if ncmp(c,1)>0:
   return('sin',add(rest,mul(nsub(c,2),'pi')))
  return('sin',add(rest,mul(c,'pi')))
 if isnode(u,'arcsin'):
  return u[1]
 if isnode(u,'arccos'):
  return sqrt(sub(1,pw(u[1],2)))
 if isnode(u,'arctan'):
  return div(u[1],sqrt(add(1,pw(u[1],2))))
 return None
def cos_(u):
 if isnum(u):
  if u==0:
   return 1
  if type(u)is float:
   return math.cos(u)
  if nsign(u)<0:
   return fn('cos',neg(u))
  return None
 if u=='inf' or u==('*',-1,'inf'):
  return 'undef'
 c=pi_coef(u)
 if c is not None:
  return sin_pi(nadd(c,HALF))
 if hasfloat(u)and isconst(u):
  return fvalc('cos',u)
 if isneg(u):
  return fn('cos',neg(u))
 sp=split_pi(u)
 if sp is not None:
  c,rest=sp
  c=nsub(c,nmul(2,nfloor(nmul(c,HALF))))
  if c==0:
   return fn('cos',rest)
  if c==1:
   return neg(fn('cos',rest))
  if c==HALF:
   return neg(fn('sin',rest))
  if c==Q(3,2):
   return fn('sin',rest)
  if ncmp(c,1)>0:
   return('cos',add(rest,mul(nsub(c,2),'pi')))
  return('cos',add(rest,mul(c,'pi')))
 if isnode(u,'arccos'):
  return u[1]
 if isnode(u,'arcsin'):
  return sqrt(sub(1,pw(u[1],2)))
 if isnode(u,'arctan'):
  return pw(add(1,pw(u[1],2)),Q(-1,2))
 return None
def tan_(u):
 if isnum(u):
  if u==0:
   return 0
  if type(u)is float:
   return math.tan(u)
  if nsign(u)<0:
   return neg(fn('tan',neg(u)))
  return None
 c=pi_coef(u)
 if c is not None:
  return tan_pi(c)
 if hasfloat(u)and isconst(u):
  return fvalc('tan',u)
 if isneg(u):
  return neg(fn('tan',neg(u)))
 sp=split_pi(u)
 if sp is not None:
  c,rest=sp
  c=nsub(c,nfloor(c))
  if c==0:
   return fn('tan',rest)
  if c==HALF:
   return neg(pw(fn('tan',rest),-1))
  return('tan',add(rest,mul(c,'pi')))
 if isnode(u,'arctan'):
  return u[1]
 return None
INVT=None
def inv_table():
 global INVT
 if INVT is None:
  T,TT=trig_table()
  S={}
  for k in T:
   S[T[k]]=k
  Tn={}
  for k in TT:
   Tn[TT[k]]=k
  INVT=(S,Tn)
 return INVT
def asin_(u):
 if isnum(u):
  if type(u)is float:
   if-1.0<=u<=1.0:
    return math.asin(u)
   return fval('arcsin',u)
 if isneg(u):
  return neg(fn('arcsin',neg(u)))
 S=inv_table()[0]
 if u in S:
  return mul(S[u],'pi')
 if isconst(u)and hasfloat(u):
  return fvalc('arcsin',u)
 return None
def acos_(u):
 if isnum(u)and type(u)is float:
  if-1.0<=u<=1.0:
   return math.acos(u)
  return fval('arccos',u)
 a=asin_(u)
 if a is not None and not isnode(a,'arcsin')and freeof(a,'arcsin'):
  return sub(mul(HALF,'pi'),a)
 if isneg(u):
  return sub('pi',fn('arccos',neg(u)))
 return None
def atan_(u):
 if isnum(u):
  if type(u)is float:
   return math.atan(u)
 if u=='inf':
  return mul(HALF,'pi')
 if u==('*',-1,'inf'):
  return mul(Q(-1,2),'pi')
 if isneg(u):
  return neg(fn('arctan',neg(u)))
 Tn=inv_table()[1]
 if u in Tn:
  return mul(Tn[u],'pi')
 if isconst(u)and hasfloat(u):
  return fvalc('arctan',u)
 return None
def ln_(u):
 if isnum(u):
  if u==1:
   return 0
  if u==0:
   return('*',-1,'inf')
  if type(u)is float:
   if u>0:
    return math.log(u)
   return add(math.log(-u),mul(math.pi,'i'))
  if nsign(u)<0:
   return add(fn('ln',nneg(u)),mul('i','pi'))
  n,d=nd(u)
  if n==1:
   return neg(fn('ln',d))
  return None
 if u=='e':
  return 1
 if u=='inf':
  return 'inf'
 if u=='i':
  return mul(HALF,'i','pi')
 if isnode(u,'^'):
  if u[1]=='e' and isreal_expr(u[2]):
   return u[2]
  if isposconst(u[1])and isreal_expr(u[2])and isnum(u[2]):
   return mul(u[2],fn('ln',u[1]))
 if isconst(u)and hasfloat(u):
  return fvalc('ln',u)
 return None
def log_(u,b=10):
 if isnum(u)and isnum(b):
  if type(u)is float or type(b)is float:
   a1=fvalc('ln',u)
   a2=fvalc('ln',b)
   if a1 is not None and a2 is not None and a2!=0:
    return div(a1,a2)
   return None
  if u==1:
   return 0
  if israt(u)and israt(b)and nsign(u)>0 and nsign(b)>0 and b!=1:
   k=exact_log(u,b)
   if k is not None:
    return k
 if u==b:
  return 1
 if isnode(u,'^')and u[1]==b and isreal_expr(u[2]):
  return u[2]
 if isconst(u)and isconst(b)and(hasfloat(u)or hasfloat(b)):
  a1=fvalc('ln',u)
  a2=fvalc('ln',b)
  if a1 is not None and a2 is not None and a2!=0:
   return div(a1,a2)
  return None
 return None
def exact_log(u,b):
 un,ud=nd(u)
 bn,bd=nd(b)
 lu=math.log(tofl(u))
 lb=math.log(tofl(b))
 if lb==0:
  return None
 k=lu/lb
 for den in range(1,13):
  num=int(round(k*den))
  if abs(k*den-num)<1e-9:
   kk=Q(num,den)
   if pw_num(b,kk)==u:
    return kk
   return None
 return None
def abs_(u):
 if isnum(u):
  return nabs(u)
 if u=='inf' or u==('*',-1,'inf'):
  return 'inf'
 if isnode(u,'abs'):
  return u
 if isnode(u,'^')and type(u[2])is int and u[2]%2==0 and isreal_expr(u[1]):
  return u
 if has(u,'i'):
  r,i=reim(u)
  if i!=0 and not has(r,'i')and not has(i,'i'):
   return sqrt(add(pw(r,2),pw(i,2)))
 if isconst(u):
  v=cv(u)
  if v is not None and type(v)is not complex:
   if v>=0:
    return u
   return neg(u)
 if isnode(u,'*'):
  outs=[]
  rest=[]
  for f in u[1:]:
   if isnum(f):
    outs.append(nabs(f))
   elif isconst(f):
    outs.append(abs_(f)or('abs',f))
   elif isnode(f,'^')and type(f[2])is int and f[2]%2==0:
    outs.append(f)
   elif isnode(f,'^')and f[1]=='e':
    outs.append(f)
   else:
    rest.append(f)
  if outs:
   return mul_list(outs+[fn('abs',mul_list(rest))])
 if isneg(u):
  return fn('abs',neg(u))
 if isnode(u,'^')and u[1]=='e' and isreal_expr(u[2]):
  return u
 return None
def sign_(u):
 if isnum(u):
  return nsign(u)if type(u)is not float else float(nsign(u))
 if u=='inf':
  return 1
 if isconst(u):
  v=cv(u)
  if v is not None and type(v)is not complex:
   return 1 if v>0 else(-1 if v<0 else 0)
 if isnode(u,'*')and isnum(u[1]):
  return mul(nsign(u[1]),fn('sign',cmul(nabs(u[1]),coef_rest(u)[1])))
 if isnode(u,'^')and type(u[2])is int and u[2]%2==0:
  return None
 return None
def finite(v):
 return v==v and v!=float('inf')and v!=float('-inf')
def floor_(u):
 if isnum(u):
  if type(u)is float:
   return float(math.floor(u))if finite(u)else None
  return nfloor(u)
 if isconst(u)and not has(u,'i'):
  v=cv(u)
  if v is not None and type(v)is not complex:
   return int(math.floor(v))
 return None
def ceil_(u):
 f=floor_(neg(u))
 if f is not None:
  return neg(f)
 return None
def sinh_(u):
 if u==0:
  return 0
 if isneg(u):
  return neg(fn('sinh',neg(u)))
 if isnode(u,'arcsinh'):
  return u[1]
 return None
def cosh_(u):
 if u==0:
  return 1
 if isneg(u):
  return fn('cosh',neg(u))
 if isnode(u,'arccosh'):
  return u[1]
 return None
def tanh_(u):
 if u==0:
  return 0
 if isneg(u):
  return neg(fn('tanh',neg(u)))
 return None
def odd0(name):
 def g(u):
  if u==0:
   return 0
  if isneg(u):
   return neg(fn(name,neg(u)))
  return None
 return g
def fact_(u):
 if type(u)is int:
  if u<0:
   return 'undef'
  if u>1000:
   return None
  r=1
  for k in range(2,u+1):
   r*=k
  return r
 if isq(u)and u[2]==2 and u[1]>0:
  n=u[1]
  r=mul(sqrt('pi'),Q(1,1))
  k=Q(1,2)
  while ncmp(k,u)<=0:
   r=mul(r,k)
   k=nadd(k,1)
  return r
 if type(u)is float:
  if u<0 and u==math.floor(u):
   return 'undef'
  try:
   return gamma(u+1.0)
  except(OverflowError,ZeroDivisionError,ValueError):
   return 'inf' if u>0 else 'undef'
 return None
def gamma(x):
 try:
  return math.gamma(x)
 except AttributeError:
  pass
 if x<0.5:
  return math.pi/(math.sin(math.pi*x)*gamma(1.0-x))
 x-=1.0
 g=7
 c=(0.99999999999980993,676.5203681218851,-1259.1392167224028,
 771.32342877765313,-176.61502916214059,12.507343278686905,
 -0.13857109526572012,9.9843695780195716e-6,1.5056327351493116e-7)
 a=c[0]
 t=x+g+0.5
 for k in range(1,9):
  a+=c[k]/(x+k)
 h=t**((x+0.5)/2)
 return math.sqrt(2*math.pi)*h*math.exp(-t)*h*a
def real_(u):
 if isconst(u)or has(u,'i'):
  r,i=reim(u)
  if not isnode(r,'real'):
   return r
 if isreal_expr(u):
  return u
 return None
def imag_(u):
 if isreal_expr(u):
  return 0
 r,i=reim(u)
 if not isnode(i,'imag'):
  return i
 return None
def conj_(u):
 if isreal_expr(u):
  return u
 r,i=reim(u)
 if not isnode(r,'real'):
  return sub(r,mul('i',i))
 return None
def angle_(u):
 r,i=reim(u)
 if isnode(r,'real')or isnode(i,'imag'):
  return None
 if i==0:
  if isconst(r):
   v=cv(r)
   if v is not None and type(v)is not complex:
    if v>=0:
     return 0
    return 'pi'
  return None
 if r==0:
  if isconst(i):
   v=cv(i)
   if v is not None and type(v)is not complex:
    return mul(Q(1 if v>0 else-1,2),'pi')
  return None
 if isconst(r)and isconst(i):
  vr=cv(r)
  vi=cv(i)
  if vr is None or vi is None or type(vr)is complex or type(vi)is complex:
   return None
  a=fn('arctan',div(i,r))
  if vr<0:
   if vi>=0:
    a=add(a,'pi')
   else:
    a=sub(a,'pi')
  return a
 return None
FSIMP['sin']=sin_
FSIMP['cos']=cos_
FSIMP['tan']=tan_
FSIMP['arcsin']=asin_
FSIMP['arccos']=acos_
FSIMP['arctan']=atan_
FSIMP['ln']=ln_
FSIMP['log']=log_
FSIMP['abs']=abs_
FSIMP['sign']=sign_
FSIMP['floor']=floor_
FSIMP['ceiling']=ceil_
FSIMP['sinh']=sinh_
FSIMP['cosh']=cosh_
FSIMP['tanh']=tanh_
FSIMP['arcsinh']=odd0('arcsinh')
FSIMP['arctanh']=odd0('arctanh')
FSIMP['arccosh']=lambda u:0 if u==1 else None
FSIMP['fact']=fact_
FSIMP['real']=real_
FSIMP['imag']=imag_
FSIMP['conj']=conj_
FSIMP['angle']=angle_
FSIMP['exp']=lambda u:pw('e',u)
FSIMP['sqrt']=lambda u:pw(u,HALF)
FSIMP['sec']=lambda u:pw(fn('cos',u),-1)
FSIMP['csc']=lambda u:pw(fn('sin',u),-1)
FSIMP['cot']=lambda u:pw(fn('tan',u),-1)
FSIMP['sech']=lambda u:pw(fn('cosh',u),-1)
FSIMP['csch']=lambda u:pw(fn('sinh',u),-1)
FSIMP['coth']=lambda u:pw(fn('tanh',u),-1)
FSIMP['arcsec']=lambda u:fn('arccos',pw(u,-1))
FSIMP['arccsc']=lambda u:fn('arcsin',pw(u,-1))
FSIMP['arccot']=lambda u:sub(mul(HALF,'pi'),fn('arctan',u))
FSIMP['arcsech']=lambda u:fn('arccosh',pw(u,-1))
FSIMP['arccsch']=lambda u:fn('arcsinh',pw(u,-1))
FSIMP['arccoth']=lambda u:fn('arctanh',pw(u,-1))
def root_(u,n=2):
 return pw(u,pw(n,-1))
FSIMP['root']=root_
import cmath
def _c(f):
 def g(x):
  try:
   if type(x)is complex:
    return f[1](x)
   return f[0](x)
  except(ValueError,TypeError):
   return f[1](complex(x))
 return g
def _ln(x):
 if type(x)is not complex and x>0:
  return math.log(x)
 if x==0:
  return float('-inf')
 return cmath.log(complex(x))
def _asinr(x):
 if-1<=x<=1:
  return math.asin(x)
 raise ValueError
def _acosr(x):
 if-1<=x<=1:
  return math.acos(x)
 raise ValueError
def _casin(z):
 return-1j*cmath.log(1j*z+cmath.sqrt(1-z*z))
def _cacos(z):
 return math.pi/2-_casin(z)
def _catan(z):
 return 0.5j*cmath.log((1-1j*z)/(1+1j*z))
def _sinh(x):
 return(cmath.exp(x)-cmath.exp(-x))/2 if type(x)is complex else(math.exp(x)-math.exp(-x))/2
def _cosh(x):
 return(cmath.exp(x)+cmath.exp(-x))/2 if type(x)is complex else(math.exp(x)+math.exp(-x))/2
def _tanh(x):
 if type(x)is not complex:
  if x>20:
   return 1.0
  if x<-20:
   return-1.0
  a=math.exp(2*x)
  return(a-1)/(a+1)
 a=cmath.exp(2*x)
 return(a-1)/(a+1)
def _asinh(x):
 if type(x)is not complex:
  return math.log(x+math.sqrt(x*x+1))if x>=0 else-math.log(-x+math.sqrt(x*x+1))
 return cmath.log(x+cmath.sqrt(x*x+1))
def _acosh(x):
 if type(x)is not complex and x>=1:
  return math.log(x+math.sqrt(x*x-1))
 x=complex(x)
 return cmath.log(x+cmath.sqrt(x+1)*cmath.sqrt(x-1))
def _atanh(x):
 if type(x)is not complex and-1<x<1:
  return 0.5*math.log((1+x)/(1-x))
 x=complex(x)
 return 0.5*cmath.log((1+x)/(1-x))
def _sign(x):
 if type(x)is complex:
  return x/abs(x)if x!=0 else 0.0
 return 1.0 if x>0 else(-1.0 if x<0 else 0.0)
def _floor(x):
 if type(x)is complex:
  return complex(math.floor(x.real),math.floor(x.imag))
 return float(math.floor(x))
def _ceil(x):
 if type(x)is complex:
  return complex(math.ceil(x.real),math.ceil(x.imag))
 return float(math.ceil(x))
def _real(x):
 return x.real if type(x)is complex else x
def _imag(x):
 return x.imag if type(x)is complex else 0.0
def _conj(x):
 return x.conjugate()if type(x)is complex else x
def _angle(x):
 if type(x)is complex:
  return cmath.phase(x)
 return 0.0 if x>=0 else math.pi
def _fact(x):
 if type(x)is complex:
  raise ValueError
 return gamma(x+1.0)
NUMF={
 'sin':_c((math.sin,cmath.sin)),'cos':_c((math.cos,cmath.cos)),
 'tan':_c((math.tan,lambda z:cmath.sin(z)/cmath.cos(z))),
 'arcsin':_c((_asinr,_casin)),'arccos':_c((_acosr,_cacos)),
 'arctan':_c((math.atan,_catan)),
 'ln':_ln,'exp':_c((math.exp,cmath.exp)),
 'sqrt':_c((lambda x:math.sqrt(x)if x>=0 else cmath.sqrt(x),cmath.sqrt)),
 'abs':abs,'sign':_sign,'floor':_floor,'ceiling':_ceil,
 'sinh':_sinh,'cosh':_cosh,'tanh':_tanh,
 'arcsinh':_asinh,'arccosh':_acosh,'arctanh':_atanh,
 'real':_real,'imag':_imag,'conj':_conj,'angle':_angle,
 'fact':_fact,
 }
def nfun_call(name,vals):
 if name=='log':
  b=vals[1]if len(vals)>1 else 10.0
  return _ln(vals[0])/_ln(b)
 if name=='root':
  n=vals[1]if len(vals)>1 else 2.0
  return npow(vals[0],1.0/n)
 if name=='round':
  d=int(vals[1])if len(vals)>1 else 0
  return round(vals[0],d)
 if name=='when':
  return vals[1]if vals[0]else(vals[2]if len(vals)>2 else float('nan'))
 if name=='max':
  return max(vals)
 if name=='min':
  return min(vals)
 if name=='mod':
  return vals[0]-vals[1]*math.floor(vals[0]/vals[1])if vals[1]!=0 else vals[0]
 f=NUMF.get(name)
 if f is None:
  if name in('sec','csc','cot','sech','csch','coth'):
   base={'sec':'cos','csc':'sin','cot':'tan','sech':'cosh','csch':'sinh','coth':'tanh'}[name]
   return 1.0/NUMF[base](vals[0])
  if name in('arcsec','arccsc','arccot','arcsech','arccsch','arccoth'):
   base={'arcsec':'arccos','arccsc':'arcsin','arccot':'arctan','arcsech':'arccosh','arccsch':'arcsinh','arccoth':'arctanh'}[name]
   return NUMF[base](1.0/vals[0])
  if name in('ipart','int'):
   return float(int(vals[0]))
  if name=='fpart':
   return vals[0]-int(vals[0])
  err("Cannot evaluate "+name)
 return f(vals[0])
def npow(a,b):
 if type(a)is not complex and type(b)is not complex:
  if a<0 and(b!=b or b in(float('inf'),float('-inf'))or b!=math.floor(b)):
   return complex(a)**b
  if a==0 and b<0:
   raise ZeroDivisionError
  try:
   return a**b
  except OverflowError:
   return float('inf')
 if a==0:
  return 0.0
 return complex(a)**b
NCONST={'pi':math.pi,'e':math.e,'i':1j,'inf':float('inf')}
def nval(e,env=None):
 t=type(e)
 if t is int:
  try:
   return float(e)
  except OverflowError:
   return 'inf' if e>0 else('*',-1,'inf')
 if t is float:
  return e
 if t is str:
  if env is not None and e in env:
   return env[e]
  v=NCONST.get(e)
  if v is None:
   err("Not numeric: "+e)
  return v
 h=e[0]
 if h=='Q':
  return e[1]/e[2]
 if h=='+':
  s=0.0
  for a in e[1:]:
   s=s+nval(a,env)
  return s
 if h=='*':
  s=1.0
  for a in e[1:]:
   s=s*nval(a,env)
  return s
 if h=='^':
  b=e[1]
  x=e[2]
  if isq(x)and x[2]%2==1:
   bv=nval(b,env)
   if type(bv)is not complex and bv<0:
    r=(-bv)**(x[1]/x[2])
    return-r if x[1]%2 else r
   return npow(bv,x[1]/x[2])
  if type(x)is int:
   bv=nval(b,env)
   if bv==0 and x<0:
    raise ZeroDivisionError
   return bv**x
  return npow(nval(b,env),nval(x,env))
 if h in('list','mat','str','Q'):
  err("Not numeric")
 if h=='when':
  c=nbool(e[1],env)
  if c:
   return nval(e[2],env)
  return nval(e[3],env)if len(e)>3 else float('nan')
 vals=[nval(a,env)for a in e[1:]]
 return nfun_call(h,vals)
def nbool(c,env):
 h=head(c)
 if h in('<','>','<=','>=','=','/='):
  a=nval(c[1],env)
  b=nval(c[2],env)
  if type(a)is complex:
   a=a.real
  if type(b)is complex:
   b=b.real
  if h=='<':
   return a<b
  if h=='>':
   return a>b
  if h=='<=':
   return a<=b
  if h=='>=':
   return a>=b
  if h=='=':
   return a==b
  return a!=b
 if h=='and':
  for a in c[1:]:
   if not nbool(a,env):
    return False
  return True
 if h=='or':
  for a in c[1:]:
   if nbool(a,env):
    return True
  return False
 if h=='not':
  return not nbool(c[1],env)
 if c=='true':
  return True
 if c=='false':
  return False
 err("Not a condition")
def nreal(e,env=None):
 v=nval(e,env)
 if type(v)is complex:
  if abs(v.imag)>1e-9*(1+abs(v.real)):
   raise ValueError
  return v.real
 return v
def simp(e):
 t=type(e)
 if t is not tuple:
  return e
 h=e[0]
 if h=='Q' or h=='str' or h=='hold':
  if h=='hold':
   return simp(e[1])
  return e
 args=[simp(a)for a in e[1:]]
 if h=='+':
  return add_list(args)
 if h=='*':
  return mul_list(args)
 if h=='^':
  return pw(args[0],args[1])
 if h in('list','mat','=','<','>','<=','>=','/=','and','or','not'):
  return(h,)+tuple(args)
 return fn(h,args)
def subs(e,old,new):
 if e==old:
  return new
 t=type(e)
 if t is not tuple or e[0]=='Q' or e[0]=='str':
  return e
 ch=False
 args=[]
 for a in e[1:]:
  b=subs(a,old,new)
  if b is not a:
   ch=True
  args.append(b)
 if not ch:
  return e
 return simp((e[0],)+tuple(args))
def subsd(e,d):
 t=type(e)
 if t is str:
  if e in d:
   return d[e]
  return e
 if t is not tuple or e[0]=='Q' or e[0]=='str':
  return e
 ch=False
 args=[]
 for a in e[1:]:
  b=subsd(a,d)
  if b is not a:
   ch=True
  args.append(b)
 if not ch:
  return e
 return simp((e[0],)+tuple(args))
def mapexpr(f,e):
 if isnode(e,'list'):
  return('list',)+tuple(mapexpr(f,a)for a in e[1:])
 if isnode(e,'mat'):
  return('mat',)+tuple(mapexpr(f,a)for a in e[1:])
 return f(e)
def expand(e):
 t=type(e)
 if t is not tuple:
  return e
 h=e[0]
 if h=='Q' or h=='str':
  return e
 if h=='+':
  return add_list([expand(a)for a in e[1:]])
 if h=='*':
  r=1
  for f in e[1:]:
   r=expand_mul(r,expand(f))
  return r
 if h=='^':
  b=expand(e[1])
  x=expand(e[2])
  if isnode(b,'+')and type(x)is int:
   if x>0:
    return expand_pow(b,x)
   if x<0:
    return pw(expand_pow(b,-x),-1)
  if isnode(b,'*')and type(x)is int:
   return expand(mul_list([pw(f,x)for f in b[1:]]))
  if b=='e' and isnode(x,'+'):
   return mul_list([pw('e',a)for a in x[1:]])
  if isnode(x,'+')and isnum(b):
   return mul_list([pw(b,a)for a in x[1:]])
  return pw(b,x)
 if h in('list','mat','=','<','>','<=','>=','/=','and','or','not'):
  return(h,)+tuple(expand(a)for a in e[1:])
 return fn(h,[expand(a)for a in e[1:]])
def evalf(e):
 t=type(e)
 if t is int:
  return float(e)
 if t is float:
  return e
 if t is str:
  if e=='pi':
   return math.pi
  if e=='e':
   return math.e
  return e
 h=e[0]
 if h=='Q':
  return e[1]/e[2]
 if h=='str':
  return e
 if isconst(e)and h not in('list','mat','=','<','>','<=','>=','/=','and','or','not'):
  try:
   v=nval(e)
   if type(v)is complex:
    return fromcomplex(v)
   if v!=v:
    return 'undef'
   if v==float('inf'):
    return 'inf'
   if v==float('-inf'):
    return('*',-1,'inf')
   return v
  except(ZeroDivisionError,ValueError,OverflowError,TypeError):
   pass
  except CASError:
   pass
 args=[evalf(a)for a in e[1:]]
 if h=='^' and type(e[2])is int:
  args[1]=e[2]
 return simp((h,)+tuple(args))
def exactify(e,tol=None):
 t=type(e)
 if t is float:
  return float2rat(e,tol)
 if t is tuple and e[0]!='Q' and e[0]!='str':
  return simp((e[0],)+tuple(exactify(a,tol)for a in e[1:]))
 return e
def float2rat(x,tol=None):
 if x!=x:
  return 'undef'
 if x==float('inf'):
  return 'inf'
 if x==float('-inf'):
  return('*',-1,'inf')
 if x==math.floor(x)and abs(x)<1e18:
  return int(x)
 if tol is None:
  tol=5e-14*max(1.0,abs(x))
 h0,h1=0,1
 k0,k1=1,0
 y=x
 for _ in range(60):
  a=math.floor(y)
  h0,h1=h1,int(a)*h1+h0
  k0,k1=k1,int(a)*k1+k0
  if abs(h1/k1-x)<=tol:
   break
  f=y-a
  if f==0:
   break
  y=1.0/f
 return Q(h1,k1)
def degree(e,x):
 if freeof(e,x):
  return 0
 if e==x:
  return 1
 h=head(e)
 if h=='+':
  d=0
  for a in e[1:]:
   k=degree(a,x)
   if k is None:
    return None
   if k>d:
    d=k
  return d
 if h=='*':
  d=0
  for a in e[1:]:
   k=degree(a,x)
   if k is None:
    return None
   d+=k
  return d
 if h=='^' and type(e[2])is int and e[2]>0:
  k=degree(e[1],x)
  if k is None:
   return None
  return k*e[2]
 return None
def coeffs(e,x):
 e=expand(e)
 if freeof(e,x):
  return[e]
 terms=e[1:]if isnode(e,'+')else(e,)
 cs={}
 mx=0
 for t in terms:
  if isnode(t,'*'):
   k=0
   rest=[]
   for f in t[1:]:
    if f==x:
     k+=1
    elif isnode(f,'^')and f[1]==x and type(f[2])is int and f[2]>0:
     k+=f[2]
    elif freeof(f,x):
     rest.append(f)
    else:
     return None
   c=mul_list(rest)
  elif t==x:
   k=1
   c=1
  elif isnode(t,'^')and t[1]==x and type(t[2])is int and t[2]>0:
   k=t[2]
   c=1
  elif freeof(t,x):
   k=0
   c=t
  else:
   return None
  cs[k]=add(cs.get(k,0),c)
  if k>mx:
   mx=k
 return[cs.get(k,0)for k in range(mx+1)]
def fromcoeffs(cs,x):
 return add_list([mul(cs[k],pw(x,k))for k in range(len(cs))])
def numer_denom(e):
 if isnode(e,'*'):
  nu=[]
  de=[]
  for f in e[1:]:
   if isq(f):
    nu.append(f[1])
    de.append(f[2])
   elif isnode(f,'^')and isnum(f[2])and nsign(f[2])<0:
    de.append(pw(f[1],nneg(f[2])))
   else:
    nu.append(f)
  return mul_list(nu),mul_list(de)
 if isq(e):
  return e[1],e[2]
 if isnode(e,'^')and isnum(e[2])and nsign(e[2])<0:
  return 1,pw(e[1],nneg(e[2]))
 return e,1
