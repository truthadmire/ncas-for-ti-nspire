from cascore import*
OPT={'uni':True,'digits':10}
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
USYM={'pi':'\u03c0','inf':'\u221e','theta':'\u03b8'}
REL={'=':'=','<':'<','>':'>','<=':'\u2264','>=':'\u2265','/=':'\u2260'}
PRIO='xyztuvwsrqpnmlkjhgfdcba'
def fmt(e):
 return pr(e,False)[0]
def ffloat(x):
 if x!=x:
  return 'undef'
 if x==float('inf'):
  return USYM['inf']if OPT['uni']else 'inf'
 if x==float('-inf'):
  return '-'+(USYM['inf']if OPT['uni']else 'inf')
 if x==0:
  return '0.'
 d=OPT['digits']
 s=('%.'+str(d)+'g')%x
 m=s
 ex=''
 if 'e' in s:
  m,ex=s.split('e')
  ex=int(ex)
  ex='E'+str(ex)
 if '.' in m:
  m=m.rstrip('0')
 else:
  m=m+'.'
 return m+ex
def fnum(x):
 t=type(x)
 if t is int:
  return str(x),(P_ATOM if x>=0 else P_NEG)
 if t is float:
  s=ffloat(x)
  return s,(P_ATOM if not s.startswith('-')else P_NEG)
 s=str(x[1])+'/'+str(x[2])
 return s,(P_PROD if x[1]>0 else P_NEG)
def psym(e):
 if OPT['uni']and e in USYM:
  return USYM[e]
 return e
def paren(s,p,need):
 if p<need:
  return '('+s+')'
 return s
def pr(e,keep):
 t=type(e)
 if t is int or t is float:
  return fnum(e)
 if t is str:
  return psym(e),P_ATOM
 h=e[0]
 if h=='Q':
  return fnum(e)
 if h=='+':
  return pr_sum(e,keep)
 if h=='*':
  return pr_prod(e,keep)
 if h=='^':
  return pr_pow(e,keep)
 if h=='hold':
  return pr(e[1],True)
 keep=False
 if h=='list':
  return '{'+','.join([pr(a,keep)[0]for a in e[1:]])+'}',P_ATOM
 if h=='mat' and len(e)==2:
  return '['+','.join([pr(a,keep)[0]for a in e[1][1:]])+']',P_ATOM
 if h=='mat':
  rows=[]
  for r in e[1:]:
   rows.append('['+','.join([pr(a,keep)[0]for a in r[1:]])+']')
  return '['+''.join(rows)+']',P_ATOM
 if h=='str':
  return '"'+e[1]+'"',P_ATOM
 if h in REL:
  op=REL[h]if OPT['uni']else h
  a=pr(e[1],keep)
  b=pr(e[2],keep)
  return paren(a[0],a[1],P_SUM)+op+paren(b[0],b[1],P_SUM),P_REL
 if h=='and' and len(e)==3 and head(e[1])in('<','<=')and head(e[2])in('<','<=')and e[1][2]==e[2][1]:
  op1=REL[e[1][0]]if OPT['uni']else e[1][0]
  op2=REL[e[2][0]]if OPT['uni']else e[2][0]
  return pr(e[1][1],False)[0]+op1+pr(e[1][2],False)[0]+op2+pr(e[2][2],False)[0],P_REL
 if h=='and' or h=='or':
  p=P_AND if h=='and' else P_OR
  ss=[]
  for a in e[1:]:
   s,q=pr(a,keep)
   ss.append(paren(s,q,p+1))
  return(' '+h+' ').join(ss),p
 if h=='not':
  s,q=pr(e[1],keep)
  return 'not '+paren(s,q,P_NOT+1),P_NOT
 if h=='abs':
  return '|'+pr(e[1],keep)[0]+'|',P_ATOM
 if h=='fact':
  s,q=pr(e[1],keep)
  return paren(s,q,P_ATOM)+'!',P_POST
 if h=='log':
  if len(e)==2 or e[2]==10:
   return 'log10('+pr(e[1],keep)[0]+')',P_ATOM
  return 'log('+pr(e[1],keep)[0]+','+pr(e[2],keep)[0]+')',P_ATOM
 if h=='call':
  return e[1]+'('+','.join([pr(a,keep)[0]for a in e[2:]])+')',P_ATOM
 if h=='prime':
  return e[1]+"'"*e[2],P_ATOM
 if h=='integral':
  nm='\u222b' if OPT['uni']else 'integral'
  return nm+'('+','.join([pr(a,keep)[0]for a in e[1:]])+')',P_ATOM
 if h=='sumseq':
  nm='\u03a3' if OPT['uni']else 'sumseq'
  return nm+'('+','.join([pr(a,keep)[0]for a in e[1:]])+')',P_ATOM
 if h=='prodseq':
  nm='\u03a0' if OPT['uni']else 'prodseq'
  return nm+'('+','.join([pr(a,keep)[0]for a in e[1:]])+')',P_ATOM
 if h=='sqrt' or h=='root':
  pass
 h=TINAME.get(h,h)
 return h+'('+','.join([pr(a,keep)[0]for a in e[1:]])+')',P_ATOM
TINAME={'ncr':'nCr','npr':'nPr'}
MAINV='xyzt'
def varprio(v):
 i=MAINV.find(v)if len(v)==1 else-1
 if i<0:
  return(100,v)
 return(i,v)
def facprio(v):
 i=MAINV.find(v)if len(v)==1 else-1
 if i<0:
  return(0,v)
 return(1,str(i))
def termdegs(t,d):
 c,r=coef_rest(t)
 fs=r[1:]if isnode(r,'*')else(r,)
 for f in fs:
  if type(f)is str and f not in SPECIAL:
   d[f]=d.get(f,0)+1
  elif isnode(f,'^')and type(f[1])is str and f[1]not in SPECIAL and isnum(f[2]):
   d[f[1]]=d.get(f[1],0)+tofl(f[2])
  elif isnode(f,'^')and isnum(f[2]):
   for v in symbols(f[1]):
    d[v]=d.get(v,0)+tofl(f[2])*0.001
  elif not isnum(f)and type(f)is not str:
   for v in symbols(f):
    d[v]=d.get(v,0)+0.0001
def sumkeys(terms):
 vs=[]
 degs=[]
 for t in terms:
  d={}
  termdegs(t,d)
  degs.append(d)
  for v in d:
   if v not in vs:
    vs.append(v)
 vs.sort(key=varprio)
 mv=[v for v in vs if varprio(v)[0]<100]
 ov=[v for v in vs if varprio(v)[0]>=100]
 keys=[]
 for k in range(len(terms)):
  t=terms[k]
  d=degs[k]
  if isnum(t):
   keys.append((2,(),0,0,(),''))
  elif not d:
   cat=3 if has(t,'i')else 1
   keys.append((cat,(),0,1 if isneg(t)else 0,(),okey(coef_rest(t)[1])))
  else:
   keys.append((0,tuple([-d.get(v,0)for v in mv]),-sum([d.get(v,0)for v in ov]),
 1 if isneg(t)else 0,tuple([-d.get(v,0)for v in ov]),okey(coef_rest(t)[1])))
 return keys
def pr_sum(e,keep):
 terms=list(e[1:])
 if not keep:
  ks=sumkeys(terms)
  idx=list(range(len(terms)))
  idx.sort(key=lambda i:ks[i])
  terms=[terms[i]for i in idx]
 out=''
 first=True
 for t in terms:
  s,p=pr(t,False)
  if p<P_SUM+1 and not s.startswith('-')and p<=P_SUM:
   s='('+s+')'
  if first:
   out=s
   first=False
  elif s.startswith('-'):
   out+=s
  else:
   out+='+'+s
 return out,P_SUM
def fackey(f):
 if f=='pi' or f=='e' or isrrad(f)or isnum(f):
  return(0,(0,''),okey(f))
 if f=='i':
  return(3,(0,''),'')
 if type(f)is str:
  return(1,facprio(f),'')
 if isnode(f,'^')and type(f[1])is str:
  if f[1]=='e':
   return(2,(0,''),okey(f))
  return(1,facprio(f[1]),okey(f))
 if isnode(f,'+')or(isnode(f,'^')and isnode(f[1],'+')):
  return(4,(0,''),okey(f))
 return(2,(0,''),okey(f))
def pr_factor(f,keep,first):
 s,p=pr(f,keep)
 if p<P_PROD or(p==P_PROD and not first)or(s.startswith('-')and not first):
  return '('+s+')'
 return s
def pr_prod(e,keep):
 fs=list(e[1:])
 coef=1
 if fs and isnum(fs[0])and not keep:
  coef=fs[0]
  fs=fs[1:]
 num=[]
 den=[]
 for f in fs:
  if isnode(f,'^')and isnum(f[2])and nsign(f[2])<0:
   ex=nneg(f[2])
   den.append(f[1]if ex==1 else('^',f[1],ex))
  elif isq(f)and keep:
   num.append(f[1])
   den.append(f[2])
  else:
   num.append(f)
 if not keep:
  num.sort(key=fackey)
  den.sort(key=fackey)
 sign=''
 if keep and num and isnum(num[0])and nsign(num[0])<0:
  sign='-'
  if num[0]==-1:
   num=num[1:]
  else:
   num[0]=nneg(num[0])
 cn=coef
 cd=1
 if isnum(coef):
  if nsign(coef)<0:
   sign='-'
   coef=nneg(coef)
  if isq(coef):
   cn=coef[1]
   cd=coef[2]
  else:
   cn=coef
 if keep:
  num=[f for f in num if f!=1]or[1]
 if sign and den and not keep:
  sums=[k for k in range(len(num))if isnode(num[k],'+')]
  dsums=[k for k in range(len(den))if isnode(den[k],'+')]
  if len(sums)==1 and any([isneg(t)for t in num[sums[0]][1:]]):
   num=list(num)
   num[sums[0]]=mul(-1,num[sums[0]])
   sign=''
  elif len(dsums)==1 and not sums and len(den[dsums[0]])==3 and isconst(den[dsums[0]])and any([isneg(t)for t in den[dsums[0]][1:]]):
   den=list(den)
   den[dsums[0]]=mul(-1,den[dsums[0]])
   sign=''
 parts=[]
 if cn!=1 or type(cn)is float:
  parts.append(fnum(cn)[0])
 for f in num:
  parts.append(pr_factor(f,False,not parts))
 if not parts:
  parts.append('1')
 ns='*'.join(parts)
 if cd!=1:
  den.insert(0,cd)
 if not den:
  if sign and len(num)==1 and cn==1 and pr(num[0],False)[1]<=P_SUM:
   return sign+'('+pr(num[0],False)[0]+')',P_NEG
  return sign+ns,(P_NEG if sign else P_PROD)
 if len(parts)==1 and len(num)==1 and cn==1:
  s,p=pr(num[0],False)
  ns=paren(s,p,P_PROD+1)if p<P_PROD else s
  if s.startswith('-'):
   ns='('+s+')'
 dparts=[]
 for f in den:
  dparts.append(pr_factor(f,False,not dparts))
 ds='*'.join(dparts)
 if len(den)>1:
  ds='('+ds+')'
 else:
  s,p=pr(den[0],False)
  if p<=P_PROD or s.startswith('-'):
   ds='('+s+')'
 return sign+ns+'/'+ds,(P_NEG if sign else P_PROD)
def pr_pow(e,keep):
 b=e[1]
 x=e[2]
 if isnum(x)and nsign(x)<0 and not keep:
  ex=nneg(x)
  d=b if ex==1 else('^',b,ex)
  s,p=pr(d,False)
  if p<=P_PROD or s.startswith('-'):
   s='('+s+')'
  return '1/'+s,P_PROD
 if x==HALF:
  s,p=pr(b,False)
  if OPT['uni']:
   if(type(b)is int and b>=0)or(type(b)is str):
    return '\u221a'+s,P_POW
   return '\u221a('+s+')',P_ATOM
  return 'sqrt('+s+')',P_ATOM
 bs,bp=pr(b,False)
 if bp<=P_POW or bs.startswith('-')or isnode(b,'fact'):
  bs='('+bs+')'
 xs,xp=pr(x,False)
 if not((type(x)is int and x>=0)or(type(x)is str)):
  xs='('+xs+')'
 return bs+'^'+xs,P_POW
def fmt_top(e):
 if isnode(e,'mat')and len(e)>2:
  rows=[]
  for r in e[1:]:
   rows.append('['+','.join([fmt(a)for a in r[1:]])+']')
  if sum([len(r)for r in rows])>28:
   return '['+('\n '.join(rows))+']'
  return '['+''.join(rows)+']'
 if isnode(e,'str'):
  return e[1]
 return fmt(e)
