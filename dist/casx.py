from cascore import*
from casout import fmt,OPT
from casparse import parse,closeup
ENV={}
UFUN={}
ST={'ans':0,'deg':False,'tmp':[]}
TRIG=('sin','cos','tan','sec','csc','cot')
ATRIG=('arcsin','arccos','arctan','arcsec','arccsc','arccot')
ALIAS={'asin':'arcsin','acos':'arccos','atan':'arctan','ceil':'ceiling',
 'asinh':'arcsinh','acosh':'arccosh','atanh':'arctanh'}
def num(a,what='an integer'):
 if not isint(a):
  err('Argument must be '+what)
 return a
def x_log(u,b=None):
 return fn('ln',u)if b is None else fn('log',u,b)
def x_root(u,n=2):
 return fn('root',u,n)
def x_gcd(a,b):
 return igcd(num(a),num(b))
def x_lcm(a,b):
 return ilcm(num(a),num(b))
def x_mod(a,b):
 if isnode(a,'^')and isint(a[1])and isint(a[2])and a[2]>0 and isint(b)and b:
  r=1
  m=abs(b)
  x=a[1]%m
  e=a[2]
  while e:
   if e&1:
    r=r*x%m
   x=x*x%m
   e>>=1
  return r-m if b<0 and r else r
 if isnum(a)and isnum(b):
  if b==0:
   return a
  return nsub(a,nmul(b,nfloor(ndiv(a,b))))
 return('mod',a,b)
def x_ncr(n,k):
 num(n)
 num(k)
 if k<0 or k>n:
  return 0
 k=min(k,n-k)
 if k*ibits(n)>MAXBITS:
  err('Result too large')
 r=1
 for i in range(k):
  r=r*(n-i)//(i+1)
 return r
def x_npr(n,k):
 num(n)
 num(k)
 if k<0 or k>n:
  return 0
 if k*ibits(n)>MAXBITS:
  err('Result too large')
 r=1
 for i in range(k):
  r*=n-i
 return r
def primes(n):
 out=[]
 p=2
 step=0
 while p*p<=n:
  if n%p==0:
   k=0
   while n%p==0:
    n//=p
    k+=1
   out.append((p,k))
  p+=1 if p<3 else 2
  step+=1
  if step>300000:
   err('Factor too large to find')
 if n>1:
  out.append((n,1))
 return out
def x_factor(a):
 if not israt(a):
  err('Argument must be an integer or a fraction')
 n,d=nd(a)
 if n==0:
  return 0
 fs=[-1]if n<0 else[]
 for p,k in primes(abs(n)):
  fs.append(p if k==1 else('^',p,k))
 for p,k in primes(d):
  fs.append(('^',p,-k))
 if not fs or fs==[-1]:
  return n
 if len(fs)==1:
  return('hold',fs[0])
 return('hold',('*',)+tuple(fs))
def x_approx(a):
 return evalf(a)
def x_exact(a):
 return exactify(a)
def x_expand(a):
 return expand(a)
EXTRA={'log':x_log,'log10':lambda u:fn('log',u,10),'root':x_root,
 'sqrt':lambda u:fn('sqrt',u),'gcd':x_gcd,'lcm':x_lcm,
 'mod':x_mod,'ncr':x_ncr,'npr':x_npr,'factor':x_factor,
 'approx':x_approx,'exact':x_exact,'expand':x_expand,
 'numer':lambda a:numer_denom(a)[0],'denom':lambda a:numer_denom(a)[1]}
def isfunc(n):
 return(n in FSIMP or n in EXTRA or n in ALIAS or n in UFUN
 or n in ST['tmp'])
def ev(t):
 tt=type(t)
 if tt is int or tt is float:
  return t
 if tt is str:
  if t in ENV:
   return ENV[t]
  if t=='ans':
   return ST['ans']
  return t
 h=t[0]
 if h=='+':
  return add(ev(t[1]),ev(t[2]))
 if h=='-':
  return sub(ev(t[1]),ev(t[2]))
 if h=='*':
  return mul(ev(t[1]),ev(t[2]))
 if h=='/':
  return div(ev(t[1]),ev(t[2]))
 if h=='^':
  return pw(ev(t[1]),ev(t[2]))
 if h=='neg':
  return neg(ev(t[1]))
 if h=='!':
  return fn('fact',ev(t[1]))
 if h=='%':
  return div(ev(t[1]),100)
 if h=='deg':
  v=ev(t[1])
  return v if ST['deg']else mul(v,div('pi',180))
 if h=='call':
  return call(t[1],t[2:])
 if h=='|':
  return ev_with(t[1],t[2])
 if h=='define':
  return define(t[1],t[2])
 if h=='store':
  return define(t[2],t[1])
 if h in('=','<','>','<=','>=','/='):
  return relation(h,ev(t[1]),ev(t[2]))
 if h=='list':
  return('list',)+tuple(ev(a)for a in t[1:])
 err('Not available in ncasx: '+str(h))
def call(name,raw):
 name=ALIAS.get(name,name)
 args=[ev(a)for a in raw]
 if name in UFUN:
  params,body=UFUN[name]
  if len(args)!=len(params):
   err('Wrong number of arguments')
  return subsd(body,dict(zip(params,args)))
 if ST['deg']and name in TRIG and len(args)==1:
  args[0]=mul(args[0],div('pi',180))
 f=EXTRA.get(name)
 try:
  r=f(*args)if f is not None else fn(name,*args)
 except TypeError:
  err('Wrong number of arguments for '+name)
 if ST['deg']and name in ATRIG:
  r=mul(r,div(180,'pi'))
 return r
def ev_with(e,cond):
 d={}
 cs=[cond]
 while cs:
  c=cs.pop()
  if isnode(c,'and'):
   cs.append(c[1])
   cs.append(c[2])
  elif isnode(c,'=')and type(c[1])is str:
   d[c[1]]=ev(c[2])
  else:
   err('Use expr|x=value')
 saved={}
 for k in d:
  if k in ENV:
   saved[k]=ENV.pop(k)
 try:
  v=ev(e)
 finally:
  ENV.update(saved)
 return subsd(v,d)
def define(lhs,rhs):
 if isnode(lhs,'call'):
  name=lhs[1]
  params=list(lhs[2:])
  for p in params:
   if type(p)is not str:
    err('Invalid parameter')
  saved={}
  for p in params:
   if p in ENV:
    saved[p]=ENV.pop(p)
  try:
   body=ev(rhs)
  finally:
   ENV.update(saved)
  UFUN[name]=(params,body)
  return('str','Done')
 if type(lhs)is not str or lhs in SPECIAL or isfunc(lhs):
  err('Invalid variable name')
 v=ev(rhs)
 ENV[lhs]=v
 return v
def relation(op,a,b):
 d=sub(a,b)
 if isnum(d)and type(d)is not complex:
  s=nsign(d)
  ok={'=':s==0,'/=':s!=0,'<':s<0,'>':s>0,
 '<=':s<=0,'>=':s>=0}[op]
  return 'true' if ok else 'false'
 if isconst(d):
  v=nval(d)
  if type(v)is float:
   ok={'=':abs(v)<1e-12,'/=':abs(v)>=1e-12,'<':v<0,'>':v>0,
 '<=':v<=0,'>=':v>=0}[op]
   return 'true' if ok else 'false'
 return(op,a,b)
def register(s):
 low=s.replace(' ','')
 for part in(low.split(':=')[0],low.split('->')[-1]):
  i=part.find('(')
  if i>0 and part[:i].isalpha()and part[:i]not in ST['tmp']:
   ST['tmp'].append(part[:i])
def decimal(r):
 if type(r)is int or type(r)is float or not isconst(r)or has(r,'i'):
  return None
 if type(r)is tuple and r[0]in('str','hold'):
  return None
 try:
  v=evalf(r)
 except Exception:
  return None
 if type(v)is float or(type(v)is tuple and isconst(v)):
  return fmt(v)
 return None
def run(s):
 s=s.strip()
 if not s:
  return ''
 low=s.lower()
 if low in('deg',':deg','degree'):
  ST['deg']=True
  return 'Degree mode'
 if low in('rad',':rad','radian'):
  ST['deg']=False
  return 'Radian mode'
 if low.startswith('digits')or low.startswith(':digits'):
  n=low.split()[-1]
  OPT['digits']=max(1,min(15,int(n)))if n.isdigit()else 10
  return 'Digits: '+str(OPT['digits'])
 if low in('clear',':clear'):
  ENV.clear()
  UFUN.clear()
  return 'Cleared'
 s=closeup(s)
 register(s)
 r=ev(parse(s,isfunc))
 if isnode(r,'str'):
  return r[1]
 if isnode(r,'hold'):
  ST['ans']=simp(r[1])
  return fmt(r)
 ST['ans']=r
 out=fmt(r)
 d=decimal(r)
 if d is not None and d!=out:
  sep='  \u2248 ' if OPT['uni']else '  ~ '
  if len(out)+len(d)+4>32:
   sep='\n  \u2248 ' if OPT['uni']else '\n  ~ '
  out+=sep+d
 return out
def xcalc():
 print('nCAS exact calculator')
 print('Type an expression; q quits')
 blank=0
 while True:
  try:
   s=input('deg> ' if ST['deg']else '> ')
  except(EOFError,KeyboardInterrupt):
   break
  s=s.strip()
  if s.lower()in('q','quit','exit'):
   break
  if not s:
   blank+=1
   if blank>=2:
    print('(type q and enter to quit)')
    blank=0
   continue
  blank=0
  try:
   out=run(s)
  except CASError as ex:
   out='Error: '+str(ex)
  except ZeroDivisionError:
   out='Error: Division by zero'
  except MemoryError:
   out='Error: Out of memory'
  except KeyboardInterrupt:
   out='Break'
  except RuntimeError:
   out='Error: Too complex'
  except Exception as ex:
   out='Error: '+str(ex)
  if out:
   print(out)
if __name__=='__main__':
 xcalc()
