from cascore import*
from casout import fmt,fmt_top,OPT
from casparse import parse,closeup
import caspoly as PO
import cascalc as CA
import cassolve as SO
import casmat as MA
import casfun as FN
from casfun import SET,lmap,vadd,vsub,vneg,vmul,vdiv,vpow,rel
VERSION='1.2'
ENV={}
UFUN={}
ASSUME=[]
STATE={'ans':0,'cplx':False,'tmpf':[]}
COMPLEXF=('csolve','czeros','cfactor','cpolyroots','eigvl','eigvc','conj',
 'real','imag','angle')
def isfunc(n):
 return(n in FN.F or n in SF or n in UFUN or n in FN.ALIAS
 or n in STATE['tmpf']or n in('expr','sqrt','log','root'))
def lookup(n):
 if n in ENV:
  return ENV[n]
 if n=='ans':
  return STATE['ans']
 if n=='i':
  STATE['cplx']=True
 return n
def ev(t):
 tt=type(t)
 if tt is int or tt is float:
  return t
 if tt is str:
  return lookup(t)
 h=t[0]
 if h=='+':
  a=ev(t[1])
  b=ev(t[2])
  return vadd(a,b)
 if h=='-':
  return vsub(ev(t[1]),ev(t[2]))
 if h=='neg':
  return vneg(ev(t[1]))
 if h=='*':
  return vmul(ev(t[1]),ev(t[2]))
 if h=='/':
  return vdiv(ev(t[1]),ev(t[2]))
 if h=='^':
  return vpow(ev(t[1]),ev(t[2]))
 if h in('.*','./','.^'):
  return FN.dotop(h,ev(t[1]),ev(t[2]))
 if h=='!':
  return lmap(lambda a:fn('fact',a),ev(t[1]))
 if h=='%':
  return lmap(lambda a:div(a,100),ev(t[1]))
 if h=='deg':
  v=ev(t[1])
  if SET['angle']=='rad':
   return lmap(lambda a:mul(a,div('pi',180)),v)
  if SET['angle']=='grad':
   return lmap(lambda a:mul(a,Q(10,9)),v)
  return v
 if h in('=','<','>','<=','>=','/='):
  return rel(h,ev(t[1]),ev(t[2]))
 if h=='and':
  return FN.land(ev(t[1]),ev(t[2]))
 if h=='or':
  return FN.lor(ev(t[1]),ev(t[2]))
 if h=='not':
  return FN.lnot(ev(t[1]))
 if h=='xor':
  return FN.lxor(ev(t[1]),ev(t[2]))
 if h=='nor':
  return FN.lnot(FN.lor(ev(t[1]),ev(t[2])))
 if h=='nand':
  return FN.lnot(FN.land(ev(t[1]),ev(t[2])))
 if h=='=>':
  return FN.lor(FN.lnot(ev(t[1])),ev(t[2]))
 if h=='<=>':
  return FN.lnot(FN.lxor(ev(t[1]),ev(t[2])))
 if h=='|':
  return ev_with(t)
 if h=='store':
  return ev_store(t[1],t[2])
 if h=='define':
  return ev_define(t[1],t[2])
 if h=='call':
  return call(t[1],t[2:])
 if h=='list':
  return('list',)+tuple(ev(a)for a in t[1:])
 if h=='mat':
  return('mat',)+tuple(('list',)+tuple(ev(a)for a in r[1:])for r in t[1:])
 if h=='str':
  return t
 if h=='&':
  a=ev(t[1])
  b=ev(t[2])
  return('str',FN.string_(a)[1]+FN.string_(b)[1])
 if h=='index':
  return ev_index(ev(t[1]),[ev(a)for a in t[2:]])
 if h=='prime':
  return t[1]+"'"*t[2]
 if h=='primecall':
  return('call',t[1]+"'"*t[2])+tuple(ev(a)for a in t[3:])
 if h=='polar':
  STATE['cplx']=True
  return mul(ev(t[1]),pw('e',mul('i',FN.toang(ev(t[2])))))
 if h=='conv':
  return ev_conv(t)
 err('Syntax error')
def evw(raw,names):
 saved={}
 for n in names:
  if n in ENV:
   saved[n]=ENV.pop(n)
 try:
  return ev(raw)
 finally:
  for n in saved:
   ENV[n]=saved[n]
def split_and(c):
 if isnode(c,'and'):
  return split_and(c[1])+split_and(c[2])
 return[c]
def ev_with(t):
 conds=split_and(t[2])
 pairs={}
 ineq=[]
 for c in conds:
  if isnode(c,'=')and type(c[1])is str:
   pairs[c[1]]=ev(c[2])
  else:
   v=evw(c,list(pairs.keys()))
   if isnode(v,'and'):
    ineq.extend(list(v[1:]))
   elif v!='true':
    ineq.append(v)
 n0=len(ASSUME)
 ASSUME.extend(ineq)
 try:
  r=evw(t[1],list(pairs.keys()))
 finally:
  del ASSUME[n0:]
 if pairs:
  r=subsd(unhold(r),pairs)
 for c in ineq:
  r=assume_sign(r,c)
 return r
def unhold(e):
 if isnode(e,'hold'):
  return simp(e[1])
 return e
def assume_sign(r,c):
 h=head(c)
 if h not in('<','>','<=','>='):
  return r
 a,b=c[1],c[2]
 if type(a)is str and b==0:
  v=a
  pos=h in('>','>=')
 elif type(b)is str and a==0:
  v=b
  pos=h in('<','<=')
 else:
  return r
 rep=v if pos else neg(v)
 r=subs(r,('abs',v),rep)
 r=subs(r,('sign',v),1 if pos else-1)
 return r
def target_fn(t):
 if isnode(t,'call'):
  return t[1],[p for p in t[2:]]
 if isnode(t,'*')and type(t[1])is str:
  p=t[2]
  return t[1],[p]
 return None
def ev_store(raw,tgt):
 tf=target_fn(tgt)
 if tf is not None:
  return ev_define(tgt,raw)
 if type(tgt)is not str:
  err('Invalid variable name')
 if tgt in SPECIAL or tgt in FN.F or tgt in SF:
  err('Reserved name')
 v=ev(raw)
 ENV[tgt]=unhold(v)if not isnode(v,'str')else v
 return v
def ev_define(lhs,rhs):
 tf=target_fn(lhs)
 if tf is None:
  if type(lhs)is str:
   return ev_store(rhs,lhs)
  err('Invalid definition')
 name,params=tf
 for p in params:
  if type(p)is not str:
   err('Invalid parameter')
 body=unhold(evw(rhs,params))
 UFUN[name]=(params,body)
 if name in STATE['tmpf']:
  STATE['tmpf'].remove(name)
 return('str','Done')
def ev_index(a,idx):
 if not idx:
  err('Invalid index')
 if isnode(a,'list'):
  i=idx[0]
  if not isint(i)or i<1 or i>=len(a):
   err('Invalid index')
  return a[i]
 if isnode(a,'mat'):
  for k in idx:
   if not isint(k)or k<1:
    err('Invalid index')
  if len(idx)==1:
   if len(a)==2:
    if idx[0]>=len(a[1]):
     err('Invalid index')
    return a[1][idx[0]]
   if idx[0]>=len(a):
    err('Invalid index')
   return('mat',a[idx[0]])
  if idx[0]>=len(a)or idx[1]>=len(a[idx[0]]):
   err('Invalid index')
  return a[idx[0]][idx[1]]
 if isnode(a,'str'):
  k=idx[0]
  if len(idx)!=1 or not isint(k)or k<1 or k>len(a[1]):
   err('Invalid index')
  return('str',a[1][k-1])
 err('Invalid index')
def ev_conv(t):
 e=t[1]
 name=t[2]
 args=[ev(a)for a in t[3:]]
 if name=='list':
  if e=='exp':
   return explist(args[0],args[1])
  if e=='mat':
   return MA.matlist(args[0])
  err('Unknown conversion')
 if name=='mat' and e=='list':
  return MA.listmat(*args)
 v=ev(e)
 v=finalize(v,True)
 return builtin(name,FN.conv,(v,name,args))
def explist(e,v):
 out=[]
 parts=e[1:]if isnode(e,'or')else(e,)
 for p in parts:
  if isnode(p,'=')and p[1]==v:
   out.append(p[2])
 return('list',)+tuple(out)
def call(name,raw):
 name=FN.ALIAS.get(name,name)
 if name=='approx' and len(raw)==1:
  v=fastnum(raw[0])
  if v is not None:
   return v
 if name in UFUN:
  params,body=UFUN[name]
  args=[ev(a)for a in raw]
  if len(args)!=len(params):
   err('Wrong number of arguments')
  return subsd(body,dict(zip(params,args)))
 f=SF.get(name)
 if f is not None:
  if name in COMPLEXF:
   STATE['cplx']=True
  return builtin(name,f,(raw,))
 f=FN.F.get(name)
 if f is not None:
  args=[ev(a)for a in raw]
  if name in COMPLEXF:
   STATE['cplx']=True
  return builtin(name,f,args)
 if name=='expr':
  s=ev(raw[0])
  return ev(parse(s[1],isfunc))
 args=[ev(a)for a in raw]
 return('call',name)+tuple(args)
class NoNum(Exception):
 pass
NUMF={'sin':math.sin,'cos':math.cos,'tan':math.tan,'arcsin':math.asin,
 'arccos':math.acos,'arctan':math.atan,'ln':math.log,'log':math.log,
 'log10':math.log10,'sqrt':math.sqrt,'exp':math.exp,'abs':abs,
 'sinh':math.sinh,'cosh':math.cosh,'tanh':math.tanh}
TRIGF=('sin','cos','tan')
ATRIGF=('arcsin','arccos','arctan')
NUMST={'big':0.0,'cost':0.0}
def lfact(n):
 return math.lgamma(n+1.0)
def fastnum(t):
 NUMST['big']=0.0
 NUMST['cost']=0.0
 try:
  v=numev(t)
 except(NoNum,ValueError,OverflowError,ZeroDivisionError,TypeError):
  return None
 if NUMST['cost']<2000 or v!=v:
  return None
 if v!=0 and abs(v)!=float('inf')and abs(v)<1e-8*NUMST['big']:
  return None
 if v==0 and NUMST['big']>0:
  return None
 return v
def numev(t):
 tt=type(t)
 if tt is int:
  return float(t)
 if tt is float:
  return t
 if tt is str:
  if t=='pi':
   return math.pi
  if t=='e':
   return math.e
  v=ENV.get(t)
  if type(v)in(int,float)or isq(v):
   return tofl(v)
  raise NoNum()
 h=t[0]
 if h in('+','-'):
  a=numev(t[1])
  b=numev(t[2])
  NUMST['big']=max(NUMST['big'],abs(a),abs(b))
  return a+b if h=='+' else a-b
 if h=='*':
  return numev(t[1])*numev(t[2])
 if h=='/':
  return numev(t[1])/numev(t[2])
 if h=='neg':
  return-numev(t[1])
 if h=='^':
  b=numev(t[1])
  x=numev(t[2])
  if b<0 and x!=int(x):
   raise NoNum()
  if abs(b)>1:
   NUMST['cost']+=abs(x)*math.log(abs(b),2)
  return b**x if abs(x*math.log(abs(b)or 1.0))<709 else(float('inf')if b>0 or x%2==0 else-float('inf'))
 if h=='!':
  n=numev(t[1])
  if n<0 or n!=int(n):
   raise NoNum()
  lf=lfact(n)
  NUMST['cost']+=lf/math.log(2)
  return math.exp(lf)if lf<709 else float('inf')
 if h=='call':
  name=FN.ALIAS.get(t[1],t[1])
  args=[numev(a)for a in t[2:]]
  if name in('ncr','npr')and len(args)==2:
   n,k=args
   if n!=int(n)or k!=int(k)or k<0 or k>n:
    raise NoNum()
   lv=lfact(n)-lfact(n-k)-(lfact(k)if name=='ncr' else 0)
   NUMST['cost']+=lv/math.log(2)
   return float(round(math.exp(lv)))if lv<36 else(math.exp(lv)if lv<709 else float('inf'))
  f=NUMF.get(name)
  if f is None or len(args)!=1:
   raise NoNum()
  x=args[0]
  if name in TRIGF and SET['angle']!='rad':
   x=x*(math.pi/180 if SET['angle']=='deg' else math.pi/200)
  r=f(x)
  if name in ATRIGF and SET['angle']!='rad':
   r=r*(180/math.pi if SET['angle']=='deg' else 200/math.pi)
  return r
 raise NoNum()
def builtin(name,f,args):
 try:
  return f(*args)
 except CASError as ex:
  if str(ex).startswith('Wrong number of arguments'):
   argerr(name)
  raise
 except TypeError as ex:
  msg=str(ex)
  if 'positional' in msg or 'takes' in msg or 'required' in msg or 'missing' in msg:
   argerr(name)
  err('Invalid argument for '+name)
 except(IndexError,ValueError,AttributeError,KeyError):
  err('Invalid argument for '+name)
 except OverflowError:
  err('Number too large in '+name)
def tinames():
 c=STATE.get('tinames')
 if c is None:
  import cashelp
  c={}
  for key,title,words in cashelp.CATS:
   for wd in words.split():
    if wd[0].isalpha():
     c[wd.lower()]=wd
  STATE['tinames']=c
 return c
def argerr(name):
 import cashelp
 n=tinames().get(name,name)
 sy=cashelp.SYN.get(name)
 err('Wrong number of arguments for '+n+('\n'+sy.split('\n')[0]if sy else ''))
def suggest(name):
 if len(name)<4:
  return None
 best=None
 for k in tinames():
  if abs(len(k)-len(name))>1:
   continue
  if close(k,name.lower()):
   best=tinames()[k]
   break
 return best
def close(a,b):
 if a==b:
  return False
 if len(a)==len(b):
  d=[i for i in range(len(a))if a[i]!=b[i]]
  if len(d)==2 and d[1]==d[0]+1 and a[d[0]]==b[d[1]]and a[d[1]]==b[d[0]]:
   return True
  return len(d)==1
 if len(a)>len(b):
  a,b=b,a
 for i in range(len(b)):
  if b[:i]+b[i+1:]==a:
   return True
 return False
def unknown_calls(e,out):
 if type(e)is not tuple or not e or e[0]=='Q':
  return
 if e[0]=='call' and e[1]not in UFUN and e[1]not in STATE['tmpf']and e[1]not in out:
  out.append(e[1])
 for a in e[1:]:
  unknown_calls(a,out)
def var_of(raw):
 if type(raw)is str:
  return raw,None
 if isnode(raw,'='):
  if type(raw[1])is not str:
   err('Variable expected')
  return raw[1],ev(raw[2])
 err('Variable expected')
def nargs(a,lo,hi):
 if len(a)<lo or len(a)>hi:
  err('Wrong number of arguments')
def onevar_expr(a,k=1):
 v,val=var_of(a[k])
 e=unhold(evw(a[0],[v]))
 return e,v,val
def post_subst(r,v,val):
 if val is not None:
  return subs(r,v,val)
 if v in ENV:
  return subs(r,v,ENV[v])
 return r
def sf_d(a):
 nargs(a,2,3)
 e,v,val=onevar_expr(a)
 n=ev(a[2])if len(a)>2 else 1
 if not isint(n):
  err('Order must be an integer')
 r=lmap(lambda u:CA.nice(CA.diff(u,v,n)),e)
 return post_subst(r,v,val)
def sf_int(a):
 nargs(a,2,4)
 e,v,val=onevar_expr(a)
 if len(a)==2:
  return lmap(lambda u:CA.nice(CA.integrate(u,v)),e)
 if len(a)==3:
  c=ev(a[2])
  return lmap(lambda u:add(CA.nice(CA.integrate(u,v)),c),e)
 lo=ev(a[2])
 hi=ev(a[3])
 return lmap(lambda u:CA.nice(CA.defint(u,v,lo,hi)),e)
def sf_limit(a):
 nargs(a,3,4)
 e,v,val=onevar_expr(a)
 pt=ev(a[2])
 dirn=0
 if len(a)>3:
  d=ev(a[3])
  if not isnum(d):
   err('Direction must be -1, 0 or 1')
  dirn=0 if d==0 else(1 if nsign(d)>0 else-1)
 def L(u):
  r=CA.limit(u,v,pt,dirn)
  if isnode(r,'limit'):
   return('limit',u,v,pt)if dirn==0 else('limit',u,v,pt,dirn)
  return CA.nice(r)
 return lmap(L,e)
def bounds(a,i):
 return ev(a[i]),ev(a[i+1])
def sf_sum(a):
 nargs(a,4,4)
 e,v,val=onevar_expr(a)
 lo,hi=bounds(a,2)
 r=CA.sumseq(e,v,lo,hi)
 return prefer_fact(CA.nice(r))
def prefer_fact(r):
 if isnode(r,'+')and not hasfloat(r)and len(symbols(r))==1:
  try:
   f=PO.factor_expr(r)
   if isnode(f,'hold')and isnode(f[1],'*'):
    return f
  except Exception:
   pass
 return r
def sf_prod(a):
 nargs(a,4,4)
 e,v,val=onevar_expr(a)
 lo,hi=bounds(a,2)
 return CA.prodseq(e,v,lo,hi)
def sf_seq(a):
 nargs(a,4,5)
 e,v,val=onevar_expr(a)
 lo,hi=bounds(a,2)
 st=ev(a[4])if len(a)>4 else 1
 out=[]
 k=lo
 cnt=0
 while ncmp(k,hi)<=0 if isnum(k)else False:
  out.append(subs(e,v,k))
  k=nadd(k,st)
  cnt+=1
  if cnt>MAXLEN:
   toobig('seq would make more than %d elements'%MAXLEN)
 return('list',)+tuple(out)
def sf_taylor(a):
 nargs(a,3,4)
 e,v,val=onevar_expr(a)
 n=ev(a[2])
 pt=ev(a[3])if len(a)>3 else 0
 return lmap(lambda u:CA.taylor(u,v,n,pt),e)
def sf_series(a):
 nargs(a,3,4)
 e,v,val=onevar_expr(a)
 n=ev(a[2])
 pt=ev(a[3])if len(a)>3 else 0
 return lmap(lambda u:CA.series_cmd(u,v,n,pt),e)
def sf_dominant(a):
 nargs(a,2,3)
 e,v,val=onevar_expr(a)
 pt=ev(a[2])if len(a)>2 else 0
 return lmap(lambda u:CA.dominant(u,v,pt),e)
def solvevars(rawvs):
 vs=[]
 gs=[]
 for r in rawvs:
  if isnode(r,'list'):
   for q in r[1:]:
    v,g=var_of(q)
    vs.append(v)
    gs.append(g)
  else:
   v,g=var_of(r)
   vs.append(v)
   gs.append(g)
 return vs,gs
def eqlist(e):
 if isnode(e,'and'):
  out=[]
  for p in e[1:]:
   out.extend(eqlist(p))
  return out
 if isnode(e,'list'):
  return list(e[1:])
 return[e]
def cons_for(v):
 out=[]
 for c in ASSUME:
  if has(c,v):
   out.append(c)
 return out
def sf_solve(a,cplx=False):
 if len(a)<2:
  err('Wrong number of arguments')
 vs,gs=solvevars(a[1:])
 e=evw(a[0],vs)
 eqs=eqlist(e)
 if len(vs)==1 and len(eqs)==1:
  v=vs[0]
  eq=eqs[0]
  if gs[0]is not None:
   f=sub(eq[1],eq[2])if isnode(eq,'=')else eq
   r=SO.nsolve(f,v,tofl(evalf(gs[0])))
   return('=',v,r)if r is not None else 'false'
  r=SO.solve(eq,v,cplx,cons_for(v))
  if r is None:
   f=sub(eq[1],eq[2])if isnode(eq,'=')else eq
   ns=SO.numeric_solve(f,v,cplx)if head(eq)=='=' or head(eq)is None else None
   if ns:
    r=SO.sols_to_bool(v,SO.apply_constraints(ns,v,cons_for(v)))
   else:
    return('solve',eq,v)
  return finish_sol(r)
 if len(eqs)>1 and any([head(q)in('<','>','<=','>=','/=')for q in eqs]):
  if len(vs)>1:
   return('solve',e)+tuple(vs)
  return finish_sol(solve_and(eqs,vs[0],cplx))
 sols=SO.solve_system(eqs,vs,cplx,gs if any([g is not None for g in gs])else None)
 if sols is None:
  return('solve',e)+tuple(vs)
 if not sols:
  return 'false'
 out=[]
 for s in sols:
  conj=[('=',v,SO.clean(s.get(v,v)))for v in vs]
  out.append(conj[0]if len(conj)==1 else('and',)+tuple(conj))
 return finish_sol(out[0]if len(out)==1 else('or',)+tuple(out))
def solve_and(eqs,v,cplx):
 cons=cons_for(v)
 for i in range(len(eqs)):
  if head(eqs[i])=='=':
   rest=eqs[:i]+eqs[i+1:]
   r=SO.solve(eqs[i],v,cplx,rest+cons)
   if r is None:
    return('solve',('and',)+tuple(eqs),v)
   return r
 ps=SO.rel_pairs(eqs+cons,v)
 r=SO.solve_rels(ps,v)if ps is not None else None
 if r is None:
  return('solve',('and',)+tuple(eqs),v)
 return r
def finish_sol(r):
 ns=[]
 def walk(e):
  if type(e)is str and e[0]=='n' and e[1:].isdigit()and e not in ns:
   ns.append(e)
  elif type(e)is tuple and e and e[0]!='Q':
   for a in e[1:]:
    walk(a)
 walk(r)
 if not ns or ns==['n%d'%(i+1)for i in range(len(ns))]:
  return r
 tmp=dict([(ns[i],'N%d_'%i)for i in range(len(ns))])
 r=subsd(r,tmp)
 return subsd(r,dict([('N%d_'%i,'n%d'%(i+1))for i in range(len(ns))]))
def sf_csolve(a):
 return sf_solve(a,True)
def sf_zeros(a,cplx=False):
 nargs(a,2,2)
 vs,gs=solvevars(a[1:])
 e=evw(a[0],vs)
 if len(vs)==1 and not isnode(e,'list'):
  r=SO.zeros(e,vs[0],cplx,cons_for(vs[0]))
  if r is None:
   ns=SO.numeric_solve(e,vs[0],cplx)
   return('list',)+tuple(ns or[])
  return r
 eqs=eqlist(e)
 sols=SO.solve_system(eqs,vs,cplx)
 if not sols:
  return('list',)
 return MA.mk([[SO.clean(s.get(v,v))for v in vs]for s in sols])
def sf_czeros(a):
 return sf_zeros(a,True)
def sf_nsolve(a):
 nargs(a,2,4)
 v,g=var_of(a[1])
 e=unhold(evw(a[0],[v]))
 f=sub(e[1],e[2])if isnode(e,'=')else e
 lo=tofl(evalf(ev(a[2])))if len(a)>2 else None
 hi=tofl(evalf(ev(a[3])))if len(a)>3 else None
 for c in cons_for(v):
  b=SO.bounds([c],v)if False else None
 cb=SO.bounds(cons_for(v),v)
 if cb is not None:
  lo,hi=tofl(evalf(cb[0])),tofl(evalf(cb[1]))
 r=SO.nsolve(f,v,tofl(evalf(g))if g is not None else None,lo,hi)
 if r is None:
  return('str','No solution found')
 return r
def sf_desolve(a):
 nargs(a,3,3)
 x=a[1]
 y=a[2]
 if type(x)is not str or type(y)is not str:
  err('Variable expected')
 parts=split_and(a[0])
 ode=None
 conds=[]
 for p in parts:
  if isnode(p,'=')and isnode(p[1],'primecall')and p[1][1]==y:
   conds.append((p[1][2],evw(p[1][3],[x,y]),evw(p[2],[x,y])))
  elif isnode(p,'=')and isnode(p[1],'*')and p[1][1]==y and not hasprime(p):
   conds.append((0,ev(p[1][2]),ev(p[2])))
  elif isnode(p,'=')and isnode(p[1],'call')and p[1][1]==y:
   conds.append((0,ev(p[1][2]),ev(p[2])))
  else:
   ode=p
 if ode is None:
  err('ODE expected')
 o=evw(ode,[x,y,y+"'",y+"''"])
 o=subs(subs(o,y+"''",SO.YP[1]),y+"'",SO.YP[0])
 r=SO.desolve(o,x,y,conds)
 if r is None:
  return('desolve',o,x,y)
 return r
def hasprime(t):
 if type(t)is not tuple:
  return False
 if t[0]in('prime','primecall'):
  return True
 for a in t[1:]:
  if hasprime(a):
   return True
 return False
def bnd_args(a,i,v):
 lo=ev(a[i])if len(a)>i else None
 hi=ev(a[i+1])if len(a)>i+1 else None
 cb=SO.bounds(cons_for(v),v)
 if cb is not None:
  lo,hi=cb
 else:
  for c in cons_for(v):
   h=head(c)
   if h in('>','>=')and c[1]==v:
    lo=c[2]
   elif h in('<','<=')and c[1]==v:
    hi=c[2]
 return lo,hi
def sf_fmin(a,kind='min'):
 nargs(a,2,4)
 e,v,val=onevar_expr(a)
 lo,hi=bnd_args(a,2,v)
 r=SO.fextreme(e,v,kind,lo,hi)
 if r is None:
  return('f'+kind,e,v)
 return r
def sf_fmax(a):
 return sf_fmin(a,'max')
def sf_nfmin(a,kind='min'):
 nargs(a,2,4)
 e,v,val=onevar_expr(a)
 lo,hi=bnd_args(a,2,v)
 return SO.nfextreme(e,v,kind,tofl(evalf(lo))if lo is not None else None,
 tofl(evalf(hi))if hi is not None else None)
def sf_nfmax(a):
 return sf_nfmin(a,'max')
def sf_nint(a):
 nargs(a,4,4)
 e,v,val=onevar_expr(a)
 lo,hi=bounds(a,2)
 return CA.nint_split(e,v,lo,hi)
def sf_arclen(a):
 nargs(a,4,4)
 e,v,val=onevar_expr(a)
 lo,hi=bounds(a,2)
 return CA.nice(CA.arclen(e,v,lo,hi))
def pt_arg(a):
 if len(a)==2 and isnode(a[1],'='):
  v,p=var_of(a[1])
  e=evw(a[0],[v])
  return e,v,p
 nargs(a,3,3)
 v,_=var_of(a[1])
 e=unhold(evw(a[0],[v]))
 return e,v,ev(a[2])
def sf_tangent(a):
 e,v,p=pt_arg(a)
 return CA.tangentline(e,v,p)
def sf_normal(a):
 e,v,p=pt_arg(a)
 return CA.normalline(e,v,p)
def sf_impdif(a):
 nargs(a,3,4)
 x,_=var_of(a[1])
 y,_=var_of(a[2])
 e=evw(a[0],[x,y])
 n=ev(a[3])if len(a)>3 else 1
 return CA.impdif(e,x,y,n)
def rc_args(a):
 v,val=var_of(a[1])
 e=unhold(evw(a[0],[v]))
 h=ev(a[2])if len(a)>2 else 0.001
 if val is None:
  val=v
 return e,v,val,h
def sf_avgrc(a):
 nargs(a,2,3)
 e,v,val,h=rc_args(a)
 return lmap(lambda u:expand(CA.avgrc(u,v,val,h)),e)
def sf_central(a):
 nargs(a,2,3)
 e,v,val,h=rc_args(a)
 return lmap(lambda u:expand(CA.centraldiff(u,v,val,h)),e)
def sf_nderiv(a):
 nargs(a,2,3)
 v,val=var_of(a[1])
 e=unhold(evw(a[0],[v]))
 n=ev(a[2])if len(a)>2 else 1
 if val is None:
  val=ENV.get(v)
  if val is None:
   err('Value required: var=value')
 return evalf(subs(CA.diff(e,v,n),v,val))
def opt_var(a,i):
 if len(a)>i:
  v,_=var_of(a[i])
  return v
 return None
def sf_expand(a):
 nargs(a,1,2)
 v=opt_var(a,1)
 e=ev(a[0])
 return PO.expand_full(unhold(e),v)
def sf_factor(a,cplx=False):
 nargs(a,1,2)
 v=opt_var(a,1)
 e=unhold(ev(a[0]))
 return PO.factor_expr(e,v,cplx)
def sf_cfactor(a):
 return sf_factor(a,True)
def sf_comdenom(a):
 nargs(a,1,2)
 return PO.comdenom(unhold(ev(a[0])))
def sf_propfrac(a):
 nargs(a,1,2)
 v=opt_var(a,1)
 return lmap(lambda u:PO.propfrac(u,v),unhold(ev(a[0])))
def polyvar(e,a,i):
 v=opt_var(a,i)
 if v is None:
  ss=symbols(e)
  v='x' if 'x' in ss or not ss else ss[0]
 return v
def sf_polycoeffs(a):
 nargs(a,1,2)
 e=unhold(ev(a[0]))
 v=polyvar(e,a,1)
 cs=coeffs(e,v)
 if cs is None:
  err('Polynomial expected')
 while len(cs)>1 and cs[-1]==0:
  cs.pop()
 return('list',)+tuple(reversed(cs))
def sf_polydegree(a):
 nargs(a,1,2)
 e=unhold(ev(a[0]))
 v=polyvar(e,a,1)
 d=degree(expand(e),v)
 if d is None:
  err('Polynomial expected')
 if e==0:
  return('*',-1,'inf')
 return d
def sf_polyquo(a,which=0):
 nargs(a,2,3)
 p=unhold(ev(a[0]))
 q=unhold(ev(a[1]))
 v=polyvar(add(p,q),a,2)
 cp=coeffs(p,v)
 cq=coeffs(q,v)
 if cp is None or cq is None:
  err('Polynomial expected')
 qq,rr=PO.e_divmod(cp,cq)
 return fromcoeffs(qq if which==0 else rr,v)
def sf_polyrem(a):
 return sf_polyquo(a,1)
def sf_polyroots(a,cplx=False):
 nargs(a,1,2)
 if len(a)==1:
  L=ev(a[0])
  if not isnode(L,'list'):
   err('List expected')
  v='X_'
  e=FN.polyeval(L,v)
 else:
  v,_=var_of(a[1])
  e=evw(a[0],[v])
 r=SO.zeros(e,v,cplx)
 return r if r is not None else('list',)
def sf_cpolyroots(a):
 return sf_polyroots(a,True)
def sf_linsolve(a):
 vs,gs=solvevars(a[1:])
 e=evw(a[0],vs)
 eqs=eqlist(e)
 fs=[SO.eqexpr(q)for q in eqs]
 if not SO.is_linear_sys(fs,vs):
  err('Argument error: linear system required')
 sols=SO.linsys(fs,vs)
 if not sols:
  return 'false'
 return('list',)+tuple(sols[0][v]for v in vs)
def sf_domain(a):
 nargs(a,2,2)
 e,v,val=onevar_expr(a)
 r=SO.domain(e,v)
 return r if r is not None else('domain',e,v)
def sf_completesq(a):
 nargs(a,2,2)
 v,_=var_of(a[1])
 e=unhold(evw(a[0],[v]))
 if isnode(e,'='):
  lhs=complete_sq(sub(e[1],e[2]),v,True)
  return lhs
 return complete_sq(e,v,False)
def complete_sq(e,v,eq):
 cs=coeffs(e,v)
 if cs is None or len(cs)!=3:
  err('Quadratic expected')
 c,b,a=cs
 h=PO.autocancel(div(b,mul(2,a)))
 k=PO.autocancel(sub(c,div(mul(b,b),mul(4,a))))
 sq=('^',add(v,h),2)
 t=sq if a==1 else('*',a,sq)
 if eq:
  return('=',('hold',t),neg(k))
 if k==0:
  return('hold',t)
 return('hold',('+',t,k))
def sf_constructmat(a):
 nargs(a,5,5)
 i,_=var_of(a[1])
 j,_=var_of(a[2])
 e=evw(a[0],[i,j])
 r=ev(a[3])
 c=ev(a[4])
 cells(r,c)
 return MA.mk([[subsd(e,{i:ii,j:jj})for jj in range(1,c+1)]for ii in range(1,r+1)])
def sf_charpoly(a):
 nargs(a,2,2)
 A=ev(a[0])
 v=a[1]if type(a[1])is str else ev(a[1])
 return MA.charpoly(A,v)
def sf_simplify(a):
 e=unhold(ev(a[0]))
 return CA.nice(CA.pyth(e))
SF={
 'd':sf_d,'integral':sf_int,'limit':sf_limit,'sumseq':sf_sum,
 'prodseq':sf_prod,'seq':sf_seq,'taylor':sf_taylor,'series':sf_series,
 'dominantterm':sf_dominant,'solve':sf_solve,'csolve':sf_csolve,
 'zeros':sf_zeros,'czeros':sf_czeros,'nsolve':sf_nsolve,
 'desolve':sf_desolve,'fmin':sf_fmin,'fmax':sf_fmax,'nfmin':sf_nfmin,
 'nfmax':sf_nfmax,'nint':sf_nint,'arclen':sf_arclen,
 'tangentline':sf_tangent,'normalline':sf_normal,'impdif':sf_impdif,
 'avgrc':sf_avgrc,'centraldiff':sf_central,'nderivative':sf_nderiv,
 'expand':sf_expand,'factor':sf_factor,'cfactor':sf_cfactor,
 'comdenom':sf_comdenom,'propfrac':sf_propfrac,
 'polycoeffs':sf_polycoeffs,'polydegree':sf_polydegree,
 'polyquotient':sf_polyquo,'polyremainder':sf_polyrem,
 'polyroots':sf_polyroots,'cpolyroots':sf_cpolyroots,
 'linsolve':sf_linsolve,'domain':sf_domain,
 'completesquare':sf_completesq,'constructmat':sf_constructmat,
 'charpoly':sf_charpoly,'simplify':sf_simplify,
 }
def when_simp(c,a,b=None):
 t=FN.tobool(FN.rel(c[0],c[1],c[2]))if FN.isrel(c)else FN.tobool(c)
 if t is True:
  return a
 if t is False:
  return b if b is not None else 'undef'
 return None
FSIMP['when']=when_simp
def finalize(r,quiet=False):
 if isnode(r,'str'):
  return r
 if not isnode(r,'hold'):
  r=PO.autocancel(r)if not(isnode(r,'list')or isnode(r,'mat'))else lmap(PO.autocancel,r)
  if needpyth(r):
   r=CA.pyth(r)
  if SET['mode']=='approx' or hasfloat(r):
   r=evalf(r)
  elif SET['mode']=='exact':
   r=exactify(r)
 if SET['cplx']=='real' and not STATE['cplx']and has(r,'i')and not quiet:
  err('Non-real result')
 return r
def sqtrig(e,out):
 if type(e)is not tuple or e[0]=='Q':
  return
 if e[0]=='^' and head(e[1])in('sin','cos')and isint(e[2])and e[2]>=2:
  out.append((e[1][0],e[1][1]))
 for a in e[1:]:
  sqtrig(a,out)
def needpyth(r):
 if not isnode(r,'+'):
  return False
 out=[]
 sqtrig(r,out)
 for n,u in out:
  if(('cos' if n=='sin' else 'sin'),u)in out:
   return True
 return False
def pre_register(s):
 low=s.replace(' ','').lower()
 cands=[]
 if ':=' in low:
  cands.append(low.split(':=')[0])
 if low.startswith('define'):
  cands.append(low[6:].split('=')[0])
 for arrow in('->','\u2192','=:'):
  if arrow in low:
   cands.append(low.split(arrow)[-1])
 for c in cands:
  i=c.find('(')
  if i>0:
   nm=c[:i]
   ok=True
   for ch in nm:
    if not(ch.isalpha()or ch.isdigit()or ch=='_'):
     ok=False
   if ok and nm not in STATE['tmpf']:
    STATE['tmpf'].append(nm)
def command(c):
 r=command0(c)
 keep()
 return r
def command0(c):
 p=c.split()
 if not p:
  return ''
 k=p[0]
 if k in('deg','degree'):
  SET['angle']='deg'
  return 'Angle: degree'
 if k in('rad','radian'):
  SET['angle']='rad'
  return 'Angle: radian'
 if k in('grad','gradian'):
  SET['angle']='grad'
  return 'Angle: gradian'
 if k in('approx','auto','exact'):
  SET['mode']=k
  return 'Mode: '+k
 if k in('real','complex','rect'):
  SET['cplx']='real' if k=='real' else 'rect'
  return 'Complex format: '+SET['cplx']
 if k in('digits','float'):
  if len(p)>1 and not p[1].isdigit():
   return 'Use :digits n with n from 1 to 15'
  n=int(p[1])if len(p)>1 else 10
  OPT['digits']=max(1,min(15,n))
  return 'Digits: '+str(OPT['digits'])
 if k=='ascii':
  OPT['uni']=False
  return 'ASCII output'
 if k in('unicode','uni'):
  OPT['uni']=True
  return 'Unicode output'
 if k=='vars':
  out=[]
  for n in sorted(ENV):
   out.append(n+' = '+fmt(ENV[n]))
  for n in sorted(UFUN):
   ps,b=UFUN[n]
   out.append(n+'('+','.join(ps)+') = '+fmt(b))
  return '\n'.join(out)if out else '(none)'
 if k in('clear','clearaz','reset'):
  ENV.clear()
  UFUN.clear()
  return 'Cleared variables and functions'
 if k=='clearans':
  STATE['ans']=0
  return 'ans cleared'
 if k in('clearhist','clearhistory'):
  return 'The history is kept only in the full-screen mode'
 if k=='free':
  STATE['ans']=0
  STATE['tinames']=None
  try:
   import gc
   gc.collect()
   return 'ans cleared, %d KB free'%(gc.mem_free()//1024)
  except Exception:
   return 'ans cleared'
 if k in('mem','memory'):
  try:
   import gc
   gc.collect()
   return 'Memory: %d KB free, %d KB used'%(gc.mem_free()//1024,gc.mem_alloc()//1024)
  except Exception:
   return 'Memory information is not available'
 if k in('mode','modes','getmode'):
  return('angle='+SET['angle']+' mode='+SET['mode']+' cplx='+SET['cplx']+
 ' digits='+str(OPT['digits']))
 if k=='test':
  import cashelp
  saved=(dict(SET),dict(OPT))
  SET.update({'angle':'rad','mode':'auto','cplx':'real'})
  OPT.update({'uni':True,'digits':10})
  try:
   return cashelp.selftest(run)
  finally:
   SET.update(saved[0])
   OPT.update(saved[1])
 if k in('menu','m'):
  menu()
  return ''
 if k in('gui','g'):
  return gui()
 if k=='keys':
  try:
   from ti_system import get_key
  except ImportError:
   return 'The key test needs the calculator (ti_system)'
  print('Press keys; esc twice to stop')
  last=''
  while True:
   key=get_key(1)
   print(repr(key))
   if key=='esc' and last=='esc':
    return ''
   last=key
 if k in('help','?','h'):
  import cashelp
  return cashelp.help(p[1]if len(p)>1 else None)
 return 'Unknown command :'+k
def run(s):
 s=s.strip()
 if not s:
  return ''
 low=s.lower()
 if low[0]==':':
  return command(low[1:])
 if low[0]=='?':
  return command('help '+low[1:].strip())
 if low.startswith('help'):
  return command(low)
 if low.startswith('delvar'):
  for n in low[6:].replace(',',' ').split():
   ENV.pop(n,None)
   UFUN.pop(n,None)
  keep()
  return 'Done'
 if low in('clearaz','clear'):
  return command('clear')
 s=closeup(s)
 pre_register(s)
 t=parse(s,isfunc)
 STATE['cplx']=(SET['cplx']!='real')
 r=fastnum(t)if SET['mode']=='approx' else None
 if r is None:
  r=ev(t)
 r=finalize(r)
 if not(isnode(t,'define')or(isnode(r,'str')and r[1]=='Done')):
  STATE['ans']=unhold(r)if not isnode(r,'str')else r
 keep()
 out=fmt_top(r)
 un=[]
 unknown_calls(r,un)
 for n in un:
  g=suggest(n)
  if g:
   out+='\n('+n+' is not a command; did you mean '+g+'?)'
 return out
KEEP='ncasmem'
def memtext():
 u=OPT['uni']
 OPT['uni']=False
 try:
  out=[':'+SET['angle'],':'+SET['mode'],
 ':'+('real' if SET['cplx']=='real' else 'complex'),
 ':digits '+str(OPT['digits'])]
  if not u:
   out.append(':ascii')
  for n in sorted(ENV):
   out.append(n+':='+fmt(ENV[n]))
  for n in sorted(UFUN):
   ps,b=UFUN[n]
   out.append(n+'('+','.join(ps)+'):='+fmt(b))
 finally:
  OPT['uni']=u
 return '\n'.join([l for l in out if len(l)<2000 and all([0<ord(c)<128 for c in l])])
def pack(t):
 out=[]
 for i in range(0,len(t),6):
  n=0
  for c in reversed(t[i:i+6]):
   n=n*128+ord(c)
  out.append(n)
 return out
def unpack(xs):
 cs=[]
 for v in xs:
  n=int(round(v))
  while n:
   cs.append(chr(n%128))
   n//=128
 return ''.join(cs)
def keep():
 if STATE.get('kept')is None or STATE.get('restoring'):
  return
 t=memtext()
 if t==STATE['kept']:
  return
 STATE['kept']=t
 try:
  from ti_system import store_list
  store_list(KEEP,pack(t)or[0])
 except Exception:
  pass
def restore():
 if STATE.get('kept')is not None:
  return
 STATE['kept']=memtext()
 try:
  from ti_system import recall_list
  t=unpack(recall_list(KEEP))
 except Exception:
  return
 STATE['restoring']=True
 try:
  for line in t.split('\n'):
   try:
    run(line)
   except Exception:
    pass
 finally:
  STATE['restoring']=False
 STATE['ans']=0
 STATE['kept']=memtext()
def menu():
 import casmenu
 casmenu.runmenu(run)
GUI=True
def gui():
 if not GUI:
  return 'The full-screen mode is the separate program ncasgui.'
 try:
  import casgui
 except ImportError as ex:
  if 'casgui' not in str(ex):
   raise
  return 'casgui is not installed (needed for the full-screen mode); using text mode.'
 restore()
 return casgui.rungui(run)
def startgui():
 r=gui()
 if r:
  print(r)
  print('The text version is the program ncastext.')
def start():
 try:
  import ti_draw
 except ImportError:
  return cas()
 r=gui()
 if r:
  print(r)
  cas()
def ver():
 return 'nCAS '+VERSION
def calc(s):
 try:
  return run(s)
 except CASError as ex:
  return 'Error: '+str(ex)
def prompt():
 p=[]
 if SET['angle']!='rad':
  p.append(SET['angle'])
 if SET['mode']!='auto':
  p.append(SET['mode'])
 if SET['cplx']!='real':
  p.append('cplx')
 return ' '.join(p)+'> '
def cas():
 restore()
 print('nCAS '+VERSION+' for TI-Nspire CX II')
 print(('? help, m menu, g full screen, q quit')if GUI else '? help, m menu, q quit')
 blank=0
 while True:
  try:
   s=input(prompt())
  except(EOFError,KeyboardInterrupt):
   break
  s=s.strip()
  if s in('q','quit','exit',':q'):
   break
  if not s:
   blank+=1
   if blank>=2:
    print('(type q and enter to quit)')
    blank=0
   continue
  blank=0
  if s.lower()in('m','menu'):
   try:
    menu()
   except Exception as ex:
    print('Error: '+str(ex))
   continue
  if s.lower()in('g','gui'):
   try:
    r=gui()
   except Exception as ex:
    r='Error: '+str(ex)
   if r:
    print(r)
   continue
  try:
   out=run(s)
   if out:
    print(out)
  except CASError as ex:
   print('Error: '+str(ex))
  except ZeroDivisionError:
   print('Error: Division by zero')
  except MemoryError:
   try:
    import gc
    gc.collect()
   except ImportError:
    pass
   print('Error: Out of memory')
  except KeyboardInterrupt:
   print('Break')
  except RuntimeError as ex:
   print('Error: Too complex ('+str(ex)+')')
  except Exception as ex:
   print('Error: '+str(ex))
if __name__=='__main__':
 cas()
