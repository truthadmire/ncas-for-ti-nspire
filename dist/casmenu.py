from cascore import CASError
ALG=(
 ('Expand','expand(@1`,@2`)',(('Expression',None),('Var (blank=all)',''))),
 ('Factor','factor(@1`,@2`)',(('Expression',None),('Var (blank=Q)',''))),
 ('cFactor','cFactor(@1`,@2`)',(('Expression',None),('Var (blank=all)',''))),
 ('Simplify','simplify(@1)',(('Expression',None),)),
 ('comDenom','comDenom(@1)',(('Expression',None),)),
 ('propFrac','propFrac(@1`,@2`)',(('Expression',None),('Var',''))),
 ('Partial frac','expand(@1,@2)',(('Rational expr',None),('Var','x'))),
 ('Complete sq','completeSquare(@1,@2)',(('Quadratic/eqn',None),('Var','x'))),
 ('Poly divide','polyQuotient(@1,@2,@3)',(('Dividend',None),('Divisor',None),('Var','x'))),
 ('Poly remain','polyRemainder(@1,@2,@3)',(('Dividend',None),('Divisor',None),('Var','x'))),
 ('Poly gcd','polyGcd(@1,@2)',(('Poly 1',None),('Poly 2',None))),
 ('Substitute','(@1)|@2=@3',(('Expression',None),('Var','x'),('Value',None))),
 ('tExpand','tExpand(@1)',(('Expression',None),)),
 ('tCollect','tCollect(@1)',(('Expression',None),)),
 ('Decimal','approx(@1)',(('Expression',None),)),
 ('Exact','exact(@1)',(('Expression',None),)),
 )
CALC=(
 ('Derivative','d(@1,@2`,@3`)',(('f',None),('Var','x'),('Order',''))),
 ('Deriv at pt','d(@1,@2)|@2=@3',(('f',None),('Var','x'),('At',None))),
 ('Integral','integral(@1,@2)',(('f',None),('Var','x'))),
 ('Def integral','integral(@1,@2,@3,@4)',(('f',None),('Var','x'),('Lower (inf ok)',None),('Upper',None))),
 ('Limit','limit(@1,@2,@3`,@4`)',(('f',None),('Var','x'),('Point (inf ok)','0'),('Side 1/-1',''))),
 ('Taylor','taylor(@1,@2,@3`,@4`)',(('f',None),('Var','x'),('Order','5'),('Point',''))),
 ('Series','series(@1,@2,@3`,@4`)',(('f',None),('Var','x'),('Order','5'),('Point',''))),
 ('Sum (sigma)','sumSeq(@1,@2,@3,@4)',(('Term',None),('Index','k'),('From','1'),('To (inf ok)','n'))),
 ('Product','prodSeq(@1,@2,@3,@4)',(('Term',None),('Index','k'),('From','1'),('To','n'))),
 ('deSolve',"deSolve(@1` and @2`` and @3`,@4,@5)",
 (("ODE, use y' y''",None),('Cond eg y(0)=1',''),("Cond eg y'(0)=0",''),('x var','x'),('y var','y'))),
 ('Implicit d/dx','impDif(@1,@2,@3)',(('Equation',None),('x var','x'),('y var','y'))),
 ('Tangent line','tangentLine(@1,@2,@3)',(('f',None),('Var','x'),('At',None))),
 ('Normal line','normalLine(@1,@2,@3)',(('f',None),('Var','x'),('At',None))),
 ('Arc length','arcLen(@1,@2,@3,@4)',(('f',None),('Var','x'),('From',None),('To',None))),
 ('fMin','fMin(@1,@2`,@3,@4`)',(('f',None),('Var','x'),('Lower',''),('Upper',''))),
 ('fMax','fMax(@1,@2`,@3,@4`)',(('f',None),('Var','x'),('Lower',''),('Upper',''))),
 ('Numeric integ','nInt(@1,@2,@3,@4)',(('f',None),('Var','x'),('Lower',None),('Upper',None))),
 )
SOLV=(
 ('Solve','solve(@1,@2)`|@3`',(('Equation/ineq',None),('Var','x'),('Condition eg x>0',''))),
 ('cSolve','cSolve(@1,@2)',(('Equation',None),('Var','x'))),
 ('Zeros','zeros(@1,@2)',(('Expression',None),('Var','x'))),
 ('cZeros','cZeros(@1,@2)',(('Expression',None),('Var','x'))),
 ('nSolve','nSolve(@1,@2`,@3,@4`)',(('Equation',None),('Var or x=guess','x'),('Lower',''),('Upper',''))),
 ('System 2 eqs','solve(@1 and @2,{@3})',(('Eq 1',None),('Eq 2',None),('Vars','x,y'))),
 ('System 3 eqs','solve(@1 and @2 and @3,{@4})',(('Eq 1',None),('Eq 2',None),('Eq 3',None),('Vars','x,y,z'))),
 ('Poly roots','polyRoots(@1,@2)',(('Polynomial',None),('Var','x'))),
 ('Domain','domain(@1,@2)',(('Expression',None),('Var','x'))),
 )
MATX=(
 ('det','det(@1)',(('Matrix 1,2;3,4',None,'m'),)),
 ('Inverse','(@1)^-1',(('Matrix',None,'m'),)),
 ('rref','rref(@1)',(('Matrix',None,'m'),)),
 ('Transpose','transpose(@1)',(('Matrix',None,'m'),)),
 ('A*B','(@1)*(@2)',(('Matrix A',None,'m'),('Matrix B',None,'m'))),
 ('A^n','(@1)^(@2)',(('Matrix',None,'m'),('Power n','2'))),
 ('Eigenvalues','eigVl(@1)',(('Matrix',None,'m'),)),
 ('Eigenvectors','eigVc(@1)',(('Matrix',None,'m'),)),
 ('charPoly','charPoly(@1,@2)',(('Matrix',None,'m'),('Var','x'))),
 ('Solve Ax=b','simult(@1,@2)',(('Matrix A',None,'m'),('Column b 5;1',None,'m'))),
 ('LU','LU(@1)',(('Matrix',None,'m'),)),
 ('QR','QR(@1)',(('Matrix',None,'m'),)),
 ('Dot product','dotP(@1,@2)',(('Vector u 1,2,3',None,'m'),('Vector v',None,'m'))),
 ('Cross product','crossP(@1,@2)',(('Vector u 1,2,3',None,'m'),('Vector v',None,'m'))),
 ('Norm','norm(@1)',(('Matrix/vector',None,'m'),)),
 ('Identity','identity(@1)',(('Size n','3'),)),
 )
NUMB=(
 ('Factor int','factor(@1)',(('Integer',None),)),
 ('isPrime','isPrime(@1)',(('Integer',None),)),
 ('gcd','gcd(@1,@2)',(('a',None),('b',None))),
 ('lcm','lcm(@1,@2)',(('a',None),('b',None))),
 ('mod','mod(@1,@2)',(('a',None),('b',None))),
 ('nCr','nCr(@1,@2)',(('n',None),('r',None))),
 ('nPr','nPr(@1,@2)',(('n',None),('r',None))),
 ('Factorial','(@1)!',(('n',None),)),
 ('Real part','real(@1)',(('Complex z',None),)),
 ('Imag part','imag(@1)',(('Complex z',None),)),
 ('Conjugate','conj(@1)',(('Complex z',None),)),
 ('|z|','abs(@1)',(('Complex z',None),)),
 ('Angle','angle(@1)',(('Complex z',None),)),
 ('Polar form','(@1)>>Polar',(('Complex z',None),)),
 )
LIST=(
 ('Mean','mean({@1})',(('Data 1,2,3',None),)),
 ('Median','median({@1})',(('Data',None),)),
 ('Std dev (s)','stdDev({@1})',(('Data',None),)),
 ('Variance (s2)','variance({@1})',(('Data',None),)),
 ('Sum','sum({@1})',(('Data',None),)),
 ('Sort up','sortA({@1})',(('Data',None),)),
 ('Sequence','seq(@1,@2,@3,@4)',(('Term',None),('Var','k'),('From','1'),('To','10'))),
 ('normCdf','normCdf(@1,@2`,@3,@4`)',(('Lower (-inf ok)',None),('Upper',None),('mu',''),('sigma',''))),
 ('invNorm','invNorm(@1`,@2,@3`)',(('Area',None),('mu',''),('sigma',''))),
 ('binomPdf','binomPdf(@1,@2,@3)',(('n',None),('p',None),('x',None))),
 ('binomCdf','binomCdf(@1,@2,@3,@4)',(('n',None),('p',None),('Lower','0'),('Upper',None))),
 )
CONV=(
 ('>Decimal','(@1)>>Decimal',(('Expression',None),)),
 ('>Fraction','(@1)>>approxFraction()',(('Decimal',None),)),
 ('>DMS','(@1)>>DMS',(('Angle',None),)),
 ('>Polar','(@1)>>Polar',(('Complex/vector',None),)),
 ('>Rect','(@1)>>Rect',(('Complex',None),)),
 ('>exp form','(@1)>>exp',(('Expression',None),)),
 ('>ln form','(@1)>>ln',(('Expression',None),)),
 ('>sin form','(@1)>>sin',(('Expression',None),)),
 ('>cos form','(@1)>>cos',(('Expression',None),)),
 ('>Binary','(@1)>>Base2',(('Integer',None),)),
 ('>Hex','(@1)>>Base16',(('Integer',None),)),
 )
SETS=(
 ('Degree',':deg',()),
 ('Radian',':rad',()),
 ('Auto mode',':auto',()),
 ('Exact mode',':exact',()),
 ('Approx mode',':approx',()),
 ('Real res',':real',()),
 ('Complex res',':complex',()),
 ('Digits',':digits @1',(('Digits 1-15','10'),)),
 ('Show vars',':vars',()),
 ('Clear vars',':clear',()),
 ('Define f(x)','@1(@2):=@3',(('Name','f'),('Params','x'),('Body',None))),
 ('Store var','@1:=@2',(('Name',None),('Value',None))),
 ('Self-test',':test',()),
 ('Memory',':mem',()),
 ('Key test',':keys',()),
 )
MAIN=(
 ('Algebra',ALG),('Calculus',CALC),('Solve',SOLV),('Matrix',MATX),
 ('Number/cplx',NUMB),('Lists/stats',LIST),('Convert',CONV),
 ('Settings',SETS),
 )
KEYS='123456789abcdefghijklmnop'
class Quit(Exception):
 pass
def ask(q):
 try:
  s=input(q)
 except EOFError:
  raise Quit()
 s=s.strip()
 if s.lower()in('q','quit'):
  raise Quit()
 return s
def show(title,labels):
 print('-- '+title+' --')
 line=''
 for i in range(len(labels)):
  cell=KEYS[i]+' '+labels[i]
  if line:
   print(line+' '*max(1,16-len(line))+cell)
   line=''
  else:
   line=cell
 if line:
  print(line)
 print('0 back  q quit')
def pick(title,labels):
 show(title,labels)
 while True:
  s=ask('#: ').lower()
  if s in('','0'):
   return None
  i=KEYS.find(s)
  if len(s)==1 and 0<=i<len(labels):
   return i
  print('Choose '+KEYS[0]+'-'+KEYS[len(labels)-1]+', 0 or q')
def matrix_text(s):
 s=s.strip()
 if s and s[0]not in '[(' and(';' in s or ',' in s):
  return '['+s+']'
 return s
def build(item):
 label,tpl,prompts=item
 vals=[]
 for p in prompts:
  q=p[0]
  d=p[1]
  hint='' if not d else ' ['+d+']'
  s=ask(q+hint+': ')
  if not s:
   if d is None:
    print('(cancelled)')
    return None
   s=d
  if len(p)>2 and p[2]=='m' and s:
   s=matrix_text(s)
  vals.append(s)
 return fill(tpl,vals)
def fill(tpl,vals):
 out=''
 parts=tpl.split('`')
 for k in range(len(parts)):
  seg=parts[k]
  if k%2==1:
   blank=False
   for i in range(len(vals)):
    if('@'+str(i+1))in seg and not vals[i]:
     blank=True
   if blank:
    continue
  out+=seg
 res=''
 i=0
 while i<len(out):
  c=out[i]
  if c=='@' and i+1<len(out)and '1'<=out[i+1]<='9':
   res+=vals[int(out[i+1])-1]
   i+=2
  else:
   res+=c
   i+=1
 return res
def menu(run):
 print('Menus: pick a number or letter.')
 print("Type ans for the last result.")
 try:
  while True:
   k=pick('nCAS menu',[m[0]for m in MAIN])
   if k is None:
    return
   title,items=MAIN[k]
   while True:
    j=pick(title,[it[0]for it in items])
    if j is None:
     break
    cmd=build(items[j])
    if cmd is None:
     continue
    print('> '+cmd)
    try:
     out=run(cmd)
    except CASError as ex:
     out='Error: '+str(ex)
    except ZeroDivisionError:
     out='Error: Division by zero'
    except MemoryError:
     out='Error: Out of memory'
    except RuntimeError as ex:
     out='Error: Too complex'
    except Quit:
     raise
    except Exception as ex:
     out='Error: '+str(ex)
    if out:
     print(out)
    ask('(enter) ')
 except Quit:
  return
 except KeyboardInterrupt:
  return
