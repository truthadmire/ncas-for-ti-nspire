from cascore import*
import math
from caspoly import autocancel
from cascalc import nice
def ismat(e):
 return isnode(e,'mat')
def islist(e):
 return isnode(e,'list')
def rows(M):
 return[list(r[1:])for r in M[1:]]
def mk(R):
 return('mat',)+tuple(('list',)+tuple(r)for r in R)
def lst(xs):
 return('list',)+tuple(xs)
def dims(M):
 return len(M)-1,len(M[1])-1
def tomat(e):
 if ismat(e):
  return e
 if islist(e):
  return mk([list(e[1:])])
 err("Matrix expected")
def ac(e):
 return autocancel(expand(e))if hasdenom(e)else expand(e)
def hasdenom(e):
 if isnode(e,'^')and isnum(e[2])and nsign(e[2])<0 and not isconst(e[1]):
  return True
 if type(e)is tuple and e[0]in('+','*'):
  for a in e[1:]:
   if hasdenom(a):
    return True
 return False
def m_add(A,B,sgn=1):
 if dims(A)!=dims(B):
  err("Dimension error")
 a=rows(A)
 b=rows(B)
 return mk([[add(a[i][j],mul(sgn,b[i][j]))for j in range(len(a[0]))]for i in range(len(a))])
def m_scale(A,c):
 return mk([[mul(c,v)for v in r]for r in rows(A)])
def m_map(A,f):
 return mk([[f(v)for v in r]for r in rows(A)])
def m_mul(A,B):
 a=rows(A)
 b=rows(B)
 if len(a[0])!=len(b):
  err("Dimension error")
 n=len(b)
 return mk([[ac(add_list([mul(a[i][k],b[k][j])for k in range(n)]))for j in range(len(b[0]))]for i in range(len(a))])
def ident(n):
 return mk([[1 if i==j else 0 for j in range(n)]for i in range(n)])
def m_pow(A,k):
 m,n=dims(A)
 if m!=n:
  err("Square matrix required")
 if k<0:
  A=m_inv(A)
  k=-k
 R=ident(n)
 while k>0:
  if k&1:
   R=m_mul(R,A)
  k>>=1
  if k:
   A=m_mul(A,A)
 return R
def transpose(A):
 if islist(A):
  return mk([[v]for v in A[1:]])
 a=rows(A)
 return mk([[a[i][j]for i in range(len(a))]for j in range(len(a[0]))])
def det(A):
 a=rows(A)
 n=len(a)
 if n!=len(a[0]):
  err("Square matrix required")
 if n==1:
  return a[0][0]
 if n==2:
  return ac(sub(mul(a[0][0],a[1][1]),mul(a[0][1],a[1][0])))
 if n==3:
  t=[]
  for j in range(3):
   minor=sub(mul(a[1][(j+1)%3],a[2][(j+2)%3]),mul(a[1][(j+2)%3],a[2][(j+1)%3]))
   t.append(mul(a[0][j],minor))
  return ac(add_list(t))
 M=[list(r)for r in a]
 sign=1
 prev=1
 for k in range(n-1):
  if ac(M[k][k])==0:
   sw=None
   for i in range(k+1,n):
    if ac(M[i][k])!=0:
     sw=i
     break
   if sw is None:
    return 0
   M[k],M[sw]=M[sw],M[k]
   sign=-sign
  for i in range(k+1,n):
   for j in range(k+1,n):
    M[i][j]=ac(div(sub(mul(M[i][j],M[k][k]),mul(M[i][k],M[k][j])),prev))
  prev=M[k][k]
 return ac(mul(sign,M[n-1][n-1]))
def iszero(v):
 v=ac(v)
 if v==0:
  return True
 if type(v)is float and abs(v)<1e-13:
  return True
 return False
def rref(A,full=True):
 M=[list(r)for r in rows(A)]
 m=len(M)
 n=len(M[0])
 r=0
 for c in range(n):
  if r>=m:
   break
  p=None
  if hasfloat_m(M):
   best=0.0
   for i in range(r,m):
    try:
     v=abs(nval(M[i][c]))
    except Exception:
     v=1.0 if not iszero(M[i][c])else 0.0
    if v>best+1e-14:
     best=v
     p=i
   if best<1e-13:
    p=None
  else:
   for i in range(r,m):
    if not iszero(M[i][c]):
     p=i
     break
  if p is None:
   continue
  M[r],M[p]=M[p],M[r]
  pv=M[r][c]
  if full:
   M[r]=[ac(div(v,pv))for v in M[r]]
  else:
   M[r]=[ac(div(v,pv))for v in M[r]]
  rng=range(m)if full else range(r+1,m)
  for i in rng:
   if i!=r and not iszero(M[i][c]):
    f=M[i][c]
    M[i]=[ac(sub(M[i][j],mul(f,M[r][j])))for j in range(n)]
  r+=1
 for i in range(m):
  for j in range(n):
   if type(M[i][j])is float and abs(M[i][j])<1e-13:
    M[i][j]=0.0
 return mk(M)
def hasfloat_m(M):
 for r in M:
  for v in r:
   if hasfloat(v):
    return True
 return False
def minor(a,i,j):
 return[[a[r][c]for c in range(len(a))if c!=j]for r in range(len(a))if r!=i]
def m_inv(A):
 m,n=dims(A)
 if m!=n:
  err("Square matrix required")
 a0=rows(A)
 if n<=3 and not all([isnum(v)for r in a0 for v in r]):
  D=det(A)
  if iszero(D):
   err("Singular matrix")
  if n==1:
   return mk([[nice(pw(D,-1))]])
  out=[]
  for i in range(n):
   row=[]
   for j in range(n):
    c=det(mk(minor(a0,j,i)))
    if(i+j)%2:
     c=neg(c)
    row.append(nice(ac(div(c,D))))
   out.append(row)
  return mk(out)
 a=rows(A)
 aug=mk([a[i]+[1 if i==j else 0 for j in range(n)]for i in range(n)])
 R=rows(rref(aug))
 for i in range(n):
  for j in range(n):
   if not iszero(sub(R[i][j],1 if i==j else 0)):
    err("Singular matrix")
 return mk([[nice(R[i][n+j])for j in range(n)]for i in range(n)])
def trace(A):
 a=rows(A)
 return add_list([a[i][i]for i in range(len(a))])
def charpoly(A,lam):
 a=rows(A)
 n=len(a)
 if n!=len(a[0]):
  err("Square matrix required")
 I=ident(n)
 Mk=mk([[0]*n for _ in range(n)])
 cs=[0]*(n+1)
 cs[n]=1
 for k in range(1,n+1):
  Mk=m_add(m_mul(A,Mk),m_scale(I,cs[n-k+1]))
  cs[n-k]=ac(div(neg(trace(m_mul(A,Mk))),k))
 return add_list([mul(cs[k],pw(lam,k))for k in range(n+1)])
def eigvl(A):
 from cassolve import zeros
 from caspoly import factor_expr
 if hasfloat_m(rows(A)):
  try:
   E=m_map(A,exactify)
  except Exception:
   E=None
  if E is not None and not hasfloat_m(rows(E)):
   return evalf(eigvl(E))
 lam='L_'
 p=charpoly(A,lam)
 f=p
 if not hasfloat_m(rows(A)):
  try:
   f=factor_expr(p)
  except Exception:
   f=p
  if isnode(f,'hold'):
   f=f[1]
 out=[]
 for g in(f[1:]if isnode(f,'*')else(f,)):
  k=1
  if isnode(g,'^')and isint(g[2])and g[2]>0:
   g,k=g[1],g[2]
  if freeof(g,lam):
   continue
  z=zeros(g,lam,True)
  if z is None:
   err("Cannot compute eigenvalues")
  z=list(z[1:])
  d=degree(g,lam)
  for v in z:
   m=mult(g,lam,v,d)if d is not None and len(z)<d else 1
   out+=[v]*(k*m)
 if not out:
  err("Cannot compute eigenvalues")
 def key(v):
  if not isconst(v):
   return(1,0.0,0.0,okey(v))
  z=complex(nval(v))
  return(0,-abs(z),-z.real,-z.imag)
 out.sort(key=key)
 return lst(out)
def mult(g,lam,v,d):
 m=1
 h=g
 while m<d:
  h=diff_(h,lam)
  w=subs(h,lam,v)
  if hasfloat(w)or hasfloat(v):
   try:
    if abs(complex(nval(w)))>1e-6*(1+abs(complex(nval(v))))**d:
     break
   except Exception:
    break
  elif not iszero(ac(expand(w))):
   break
  m+=1
 return m
def diff_(e,x):
 from cascalc import diff
 return diff(e,x)
def nullspace(A):
 R=rows(rref(A))
 m=len(R)
 n=len(R[0])
 piv=[]
 for i in range(m):
  for j in range(n):
   if not iszero(R[i][j]):
    piv.append((i,j))
    break
 pc=[j for i,j in piv]
 free=[j for j in range(n)if j not in pc]
 basis=[]
 for f in free:
  v=[0]*n
  v[f]=1
  for i,j in piv:
   v[j]=ac(neg(R[i][f]))
  basis.append(v)
 return basis
def eigvc(A):
 if hasfloat_m(rows(A)):
  try:
   E=m_map(A,exactify)
  except Exception:
   E=None
  if E is not None and not hasfloat_m(rows(E)):
   return evalf(eigvc(E))
 vals=eigvl(A)
 n=dims(A)[0]
 cols=[]
 seen=[]
 for lv in vals[1:]:
  if lv in seen:
   continue
  seen.append(lv)
  if hasfloat(lv)or hasfloat_m(rows(A)):
   cols.append(numeigvec(A,lv))
   continue
  B=m_add(A,m_scale(ident(n),lv),-1)
  B=m_map(B,lambda v:ac(v))
  ns=nullspace(B)
  for v in ns:
   cols.append(unitvec(v))
 if not cols:
  err("Cannot compute eigenvectors")
 M=mk([[cols[j][i]for j in range(len(cols))]for i in range(n)])
 for c in cols:
  for v in c:
   if esize(v)>60:
    return evalf(M)
 return M
def numeigvec(A,lam):
 a=[[complex(nval(c))for c in r]for r in rows(A)]
 n=len(a)
 mu=complex(nval(lam))
 mu+=1e-9*(1+abs(mu))
 M=[[a[i][j]-(mu if i==j else 0)for j in range(n)]for i in range(n)]
 x=[complex(1.0+0.37*i)for i in range(n)]
 for it in range(4):
  y=clsolve(M,x)
  big=max([abs(v)for v in y])or 1.0
  x=[v/big for v in y]
 nrm=math.sqrt(sum([abs(v)**2 for v in x]))or 1.0
 x=[v/nrm for v in x]
 k=0
 for i in range(n):
  if abs(x[i])>abs(x[k])+1e-12:
   k=i
 ph=x[k]/abs(x[k])
 out=[]
 for v in x:
  v=v/ph
  re=0.0 if abs(v.real)<1e-12 else v.real
  im=0.0 if abs(v.imag)<1e-12 else v.imag
  out.append(re if im==0.0 else fromcomplex(complex(re,im)))
 return out
def clsolve(M,b):
 n=len(M)
 a=[list(M[i])+[b[i]]for i in range(n)]
 for c in range(n):
  p=c
  for r in range(c+1,n):
   if abs(a[r][c])>abs(a[p][c]):
    p=r
  a[c],a[p]=a[p],a[c]
  if abs(a[c][c])<1e-14:
   a[c][c]=1e-14
  for r in range(c+1,n):
   f=a[r][c]/a[c][c]
   if f:
    for k in range(c,n+1):
     a[r][k]-=f*a[c][k]
 x=[0j]*n
 for i in range(n-1,-1,-1):
  t=a[i][n]
  for k in range(i+1,n):
   t-=a[i][k]*x[k]
  x[i]=t/a[i][i]
 return x
def coefs(e,out):
 if isnum(e):
  out.append(e)
 elif isnode(e,'+'):
  for t in e[1:]:
   coefs(t,out)
 elif isnode(e,'*')and isnum(e[1]):
  out.append(e[1])
 else:
  out.append(1)
def unitvec(v):
 if hasfloat_m([v]):
  nrm=sqrt(add_list([mul(c,fn('conj',c))for c in v]))
  return[nice(ac(div(c,nrm)))for c in v]
 cs=[]
 for c in v:
  coefs(c,cs)
 den=1
 num=0
 for q in cs:
  if israt(q)and q!=0:
   a,b=nd(q)
   den=ilcm(den,b)
   num=igcd(num,a)
 k=Q(den,num)if num else 1
 for c in v:
  if not iszero(c):
   if isneg(c):
    k=neg(k)
   break
 w=[ac(expand(mul(k,c)))for c in v]
 n2=ac(expand(add_list([mul(c,fn('conj',c))for c in w])))
 r=sqrt(n2)
 if isnum(r)or not isnode(r,'^'):
  return[ac(div(c,r))for c in w]
 inv=('^',r[1],neg(r[2]))
 return[c if iszero(c)else('*',c,inv)if isnode(c,'+')else mul(c,inv)for c in w]
def esize(e):
 if type(e)is not tuple or e[0]=='Q':
  return 1
 k=1
 for a in e[1:]:
  k+=esize(a)
 return k
def lu(A):
 a=[list(r)for r in rows(A)]
 m=len(a)
 n=len(a[0])
 L=[[1 if i==j else 0 for j in range(m)]for i in range(m)]
 P=list(range(m))
 U=a
 for k in range(min(m,n)):
  p=None
  if hasfloat_m(U):
   best=-1.0
   for i in range(k,m):
    v=abs(nval(U[i][k]))
    if v>best:
     best=v
     p=i
   if best<1e-14:
    p=None
  else:
   for i in range(k,m):
    if not iszero(U[i][k]):
     p=i
     break
  if p is None:
   continue
  if p!=k:
   U[k],U[p]=U[p],U[k]
   P[k],P[p]=P[p],P[k]
   for j in range(k):
    L[k][j],L[p][j]=L[p][j],L[k][j]
  for i in range(k+1,m):
   f=ac(div(U[i][k],U[k][k]))
   L[i][k]=f
   U[i]=[ac(sub(U[i][j],mul(f,U[k][j])))for j in range(n)]
 Pm=[[1 if P[i]==j else 0 for j in range(m)]for i in range(m)]
 return mk(L),mk(U),mk(Pm)
def qr(A):
 a=rows(A)
 m=len(a)
 n=len(a[0])
 cols=[[a[i][j]for i in range(m)]for j in range(n)]
 Qc=[]
 R=[[0]*n for _ in range(n)]
 for j in range(n):
  v=cols[j]
  for k in range(len(Qc)):
   r=ac(add_list([mul(Qc[k][i],v[i])for i in range(m)]))
   R[k][j]=r
   v=[ac(sub(v[i],mul(r,Qc[k][i])))for i in range(m)]
  nrm=nice(sqrt(ac(add_list([pw(c,2)for c in v]))))
  R[j][j]=nrm
  if iszero(nrm):
   Qc.append([0]*m)
  else:
   Qc.append([nice(ac(div(c,nrm)))for c in v])
 Qm=mk([[Qc[j][i]for j in range(n)]for i in range(m)])
 return Qm,mk(R)
def crossp(u,v):
 a=vec(u)
 b=vec(v)
 if len(a)==2:
  a=a+[0]
  b=b+[0]
 if len(a)!=3 or len(b)!=3:
  err("Dimension error")
 r=[ac(sub(mul(a[1],b[2]),mul(a[2],b[1]))),
 ac(sub(mul(a[2],b[0]),mul(a[0],b[2]))),
 ac(sub(mul(a[0],b[1]),mul(a[1],b[0])))]
 return revec(r,u)
def vec(u):
 if islist(u):
  return list(u[1:])
 if ismat(u):
  R=rows(u)
  if len(R)==1:
   return R[0]
  if len(R[0])==1:
   return[r[0]for r in R]
 err("Vector expected")
def revec(r,like):
 if islist(like):
  return lst(r)
 R=rows(like)
 if len(R)==1:
  return mk([r])
 return mk([[v]for v in r])
def dotp(u,v):
 a=vec(u)
 b=vec(v)
 if len(a)!=len(b):
  err("Dimension error")
 return ac(add_list([mul(a[i],b[i])for i in range(len(a))]))
def norm(A):
 if islist(A)or ismat(A)and(dims(A)[0]==1 or dims(A)[1]==1):
  v=vec(A)
  return nice(sqrt(ac(add_list([mul(c,fn('conj',c))for c in v]))))
 return nice(sqrt(ac(add_list([mul(c,fn('conj',c))for r in rows(A)for c in r]))))
def unitv(u):
 nrm=norm(u)
 return revec([nice(ac(div(c,nrm)))for c in vec(u)],u)
def rownorm(A):
 if not ismat(A):
  err('Argument must be a matrix')
 return maxexpr([ac(add_list([fn('abs',c)for c in r]))for r in rows(A)])
def colnorm(A):
 if not ismat(A):
  err('Argument must be a matrix')
 return rownorm(transpose(A))
def maxexpr(xs):
 best=None
 bv=None
 for x in xs:
  v=nval(x)
  if best is None or v>bv:
   best=x
   bv=v
 return best
def augment(A,B):
 if islist(A)and islist(B):
  return A+B[1:]
 a=rows(tomat(A))
 b=rows(tomat(B))
 if len(a)!=len(b):
  err("Dimension error")
 return mk([a[i]+b[i]for i in range(len(a))])
def colaugment(A,B):
 a=rows(tomat(A))
 b=rows(tomat(B))
 if len(a[0])!=len(b[0]):
  err("Dimension error")
 return mk(a+b)
def submat(A,r1=1,c1=1,r2=None,c2=None):
 a=rows(A)
 if r2 is None:
  r2=len(a)
 if c2 is None:
  c2=len(a[0])
 return mk([a[i][c1-1:c2]for i in range(r1-1,r2)])
def rowswap(A,i,j):
 a=rows(A)
 a[i-1],a[j-1]=a[j-1],a[i-1]
 return mk(a)
def rowadd(A,i,j):
 a=rows(A)
 a[j-1]=[add(a[j-1][k],a[i-1][k])for k in range(len(a[0]))]
 return mk(a)
def mrow(c,A,i):
 a=rows(A)
 a[i-1]=[mul(c,v)for v in a[i-1]]
 return mk(a)
def mrowadd(c,A,i,j):
 a=rows(A)
 a[j-1]=[ac(add(a[j-1][k],mul(c,a[i-1][k])))for k in range(len(a[0]))]
 return mk(a)
def diag(A):
 if islist(A):
  n=len(A)-1
  return mk([[A[i+1]if i==j else 0 for j in range(n)]for i in range(n)])
 a=rows(A)
 if len(a)==1 or len(a[0])==1:
  v=vec(A)
  return diag(lst(v))
 return lst([a[i][i]for i in range(min(len(a),len(a[0])))])
def matlist(A):
 return lst([v for r in rows(A)for v in r])
def listmat(L,c=None):
 xs=list(L[1:])
 if c is None:
  c=len(xs)
 if not isint(c)or c<1:
  err('Invalid number of columns')
 out=[]
 while xs:
  r=xs[:c]
  xs=xs[c:]
  while len(r)<c:
   r.append(0)
  out.append(r)
 return mk(out)
def simult(A,b):
 a=rows(A)
 n=len(a)
 bb=rows(tomat(b))if ismat(b)else[[v]for v in b[1:]]
 if len(bb)!=n:
  bb=rows(transpose(b))
 k=len(bb[0])
 R=rows(rref(mk([a[i]+bb[i]for i in range(n)])))
 for i in range(n):
  if iszero(R[i][i]):
   err("Singular matrix")
 return mk([[nice(R[i][n+j])for j in range(k)]for i in range(n)])
def cumsum(L):
 if islist(L):
  out=[]
  s=0
  for v in L[1:]:
   s=add(s,v)
   out.append(s)
  return lst(out)
 a=rows(L)
 out=[]
 acc=[0]*len(a[0])
 for r in a:
  acc=[add(acc[j],r[j])for j in range(len(r))]
  out.append(list(acc))
 return mk(out)
def polar_vec(u):
 v=vec(u)
 if len(v)==2:
  r=nice(sqrt(ac(add(pw(v[0],2),pw(v[1],2)))))
  th=fn('angle',add(v[0],mul('i',v[1])))
  return('str','['+fmtx(r)+' \u2220'+fmtx(th)+']')
 err("Dimension error")
def fmtx(e):
 from casout import fmt
 return fmt(e)
def cylind(u):
 v=vec(u)
 if len(v)!=3:
  err("Dimension error")
 r=nice(sqrt(ac(add(pw(v[0],2),pw(v[1],2)))))
 th=fn('angle',add(v[0],mul('i',v[1])))
 return('str','['+fmtx(r)+' \u2220'+fmtx(th)+' '+fmtx(v[2])+']')
def sphere(u):
 v=vec(u)
 if len(v)!=3:
  err("Dimension error")
 rho=nice(sqrt(ac(add(pw(v[0],2),pw(v[1],2),pw(v[2],2)))))
 th=fn('angle',add(v[0],mul('i',v[1])))
 ph=fn('arccos',div(v[2],rho))if rho!=0 else 0
 return('str','['+fmtx(rho)+' \u2220'+fmtx(th)+' \u2220'+fmtx(ph)+']')
def lsum(L,a=1,b=None):
 xs=list(L[1:])
 if b is None:
  b=len(xs)
 return add_list(xs[a-1:b])
def lprod(L,a=1,b=None):
 xs=list(L[1:])
 if b is None:
  b=len(xs)
 return mul_list(xs[a-1:b])
def mean(L,F=None):
 xs=list(L[1:])
 if F is None:
  return div(add_list(xs),len(xs))
 fs=list(F[1:])
 return div(add_list([mul(xs[i],fs[i])for i in range(len(xs))]),add_list(fs))
def sortkey(v):
 try:
  x=nval(v)
  return x.real if type(x)is complex else x
 except Exception:
  return 0.0
def median(L):
 xs=sorted(list(L[1:]),key=sortkey)
 n=len(xs)
 if n%2:
  return xs[n//2]
 return div(add(xs[n//2-1],xs[n//2]),2)
def variance(L,pop=False):
 xs=list(L[1:])
 n=len(xs)
 m=mean(L)
 s=add_list([pw(sub(v,m),2)for v in xs])
 return ac(div(s,n if pop else n-1))
def stddev(L,pop=False):
 return nice(sqrt(variance(L,pop)))
def sorta(L):
 return lst(sorted(list(L[1:]),key=sortkey))
def sortd(L):
 return lst(sorted(list(L[1:]),key=sortkey,reverse=True))
def deltalist(L):
 xs=list(L[1:])
 return lst([sub(xs[i+1],xs[i])for i in range(len(xs)-1)])
