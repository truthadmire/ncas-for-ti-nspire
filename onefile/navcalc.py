# navcalc - aviation (E6B) calculator for TI-Nspire CX II. Run it (ctrl+R): pick a tool, esc quits.
# The program is kept below as text and compiled one part at a time, which needs
# much less memory than compiling everything at once. Do not edit the text parts.
try:
 import gc
except ImportError:
 gc = None
try:
 exec
except NameError:
 print('exec() is missing: paste src/navcalc.py instead')
 raise SystemExit
_L = {}
_P = {}     # parts of a lazy module already compiled (a failed load can be retried)
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
 ps = _L.get(m)
 if ps is None:
  return
 i = _P.get(m, 0)
 while i < len(ps):
  if gc:
   gc.collect()
  exec(_u(ps[i]), globals())
  i += 1
  _P[m] = i
 del _L[m]
 _P.pop(m, None)""")
print('Loading navcalc...')
_W={'!': 'return', '#': 'None', '%': 'ValueError', '&': 'except', '(': 'range', ')': 'def', '*': 'else', '+': 'append', ',': 'for', '-': 'unit_tool', '.': 'withunit', '/': 'title', '0': 'len', '1': 'UNITS', '2': 'ti_draw', '3': 'while', '4': 'elif', '5': 'status', '6': 'True', '7': 'text', '8': 'kind', '9': 'math', ':': 'ZeroDivisionError', ';': 'and', '<': 'ev_unary', '=': 'last', '>': 'TypeError', '?': 'C_DIM', '@': 'ImportError', 'A': 'ARITH', 'B': 'done', 'C': 'fmtnum', 'D': 'helpscreen', 'E': 'labels', 'F': 'raise', 'G': 'resvec', 'H': 'temp', 'I': 'values', 'J': 'OverflowError', 'K': 'rows', 'L': 'top', 'M': 'vals', 'N': 'Crosswind', 'O': 'Exception', 'P': 'break', 'Q': 'deviation', 'R': 'press', 'S': 'print', 'T': 'try', 'U': 'abs', 'V': 'base', 'W': 'isdigit', 'X': 'navcalc', 'Y': 'alt', 'Z': 'Avgas', '[': 'C_TXT', ']': 'False', '^': 'Pressure', '_': 'TOOLS', '`': 'altitude', 'a': 'continue', 'b': 'not', 'c': 'show_', 'd': 'C_BART', 'e': 'UTOOLS', 'f': 'time', 'g': 'extra', 'h': 'float', 'i': 'right', 'j': 'spd', 'k': 'speed', 'l': 'tdiff', 'm': 'u03c0', 'n': 'sel', 'o': 'hdg', 'p': 'key'}
_x(r'''import $9
VERSION='1.0'
RAD=$9.pi/180
LH=18
RH=17
BASE=14
AW=7
C_BAR=(30,60,130)
$d=(255,255,255)
$[=(0,0,0)
C_RES=(0,70,170)
C_ERR=(190,0,0)
C_SEL=(205,225,255)
$?=(110,110,110)
C_CUR=(220,0,0)
C_WHITE=(255,255,255)
ENTER=('enter','ret','$!','center','\r','\n')
MENU=('menu',)
BACKTAB=('shift+tab','shift tab','shifttab','backtab','btab')
DELKEYS=('del','backspace','bksp')
KEYS='123456789abcdefghijklmnop'
MAXT=24
LBKG=0.45359237
AVGAS=6.0
JETA=6.7
$1={
 '$j':(('kt',1.0,0,1),('mph',1.150779,0,1),('km/h',1.852,0,1)),
 'dist':(('nm',1.0,0,1),('sm',1.150779,0,1),('km',1.852,0,1)),
 '$Y':(('ft',1.0,0,0),('m',0.3048,0,0)),
 '$H':(('\u00b0C',1.0,0,1),('\u00b0F',1.8,32,1)),
 '$R':(('inHg',1/33.8639,0,2),('hPa',1.0,0,1)),
 'fuel':(('USG',1.0,0,1),('L',3.785412,0,1),('Imp gal',0.832674,0,1),
 ('lb $Z',AVGAS,0,0),('kg $Z',AVGAS*LBKG,0,0),
 ('lb Jet-A',JETA,0,0),('kg Jet-A',JETA*LBKG,0,0)),
 'rate':(('gph',1.0,0,1),('L/h',3.785412,0,1),
 ('pph $Z',AVGAS,0,0),('pph Jet-A',JETA,0,0)),
 '$f':(('h:mm',1.0,0,0),('min',1.0,0,1),('h',1/60.0,0,2)),
 '$o':(('\u00b0',1.0,0,0),),
 'ang':(('\u00b0',1.0,0,1),),
 'mach':(('M',1.0,0,3),),
 }
$1['sspd']=$1['$j']
$1['rwy']=$1['$o']
HDG=('$o','rwy')
POS=('$j','dist','$f','fuel','rate','mach','$R')
DEF={'$j':100.0,'sspd':10.0,'dist':100.0,'$f':60.0,'fuel':20.0,
 'rate':10.0,'$Y':3000.0,'$H':15.0,'$R':1013.25,'mach':0.3,
 '$o':0.0,'rwy':0.0,'ang':0.0}
$A=($%,$:,$J,$>)
$) $C(x,dec):
 s=('%.'+str(dec)+'f')%x
 if s[:1]=='-' $; $h(s)==0:
  s=s[1:]
 $! s
$) hmm(m):
 if $U(m)>1e7:
  $! $C(m,0)
 t=int($9.floor($U(m)+0.5))
 $!('-' if m<0 $; t $* '')+'%d:%02d'%(t//60,t%60)
$) show(x,$8,u=0):
 if $8 in HDG:
  r=int($9.floor(x%360+0.5))%360
  $! '%03d'%(r or 360)
 un=$1[$8][u]
 if un[0]=='h:mm':
  $! hmm(x)
 $! $C(x*un[1]+un[2],un[3])
$) edtext(x,$8,u):
 un=$1[$8][u]
 if un[0]=='h:mm':
  $! hmm(x)
 s=$C(x*un[1]+un[2],un[3]+2)
 if '.' in s:
  s=s.rstrip('0').rstrip('.')
 $! s
$) $l(x,u):
 $! $C(x*$1['$H'][u][1],1)+' '+$1['$H'][u][0]
$) $.(x,$8,u):
 $! show(x,$8,u)+' '+$1[$8][u][0]
$) parse(s,$8,u):
 if ':' in s:
  if $8!='$f':
   $F $%
  a,b=s.split(':',1)
  m=$U($h(a or '0'))*60+$h(b or '0')
  $!-m if s[:1]=='-' $* m
 x=evalnum(s)
 if x is $#:
  $F $%
 if $8=='rwy' $; s.$W()$; 0<x<=36:
  x*=10
 un=$1[$8][u]
 $!(x-un[2])/un[1]
KEYCH={'.':'.','point':'.','decimal':'.','dot':'.','period':'.',
 '-':'-','\u2212':'-','minus':'-','+':'+','plus':'+',
 '*':'*','\u00d7':'*','times':'*','multiply':'*',
 '/':'/','\u00f7':'/','divide':'/','^':'^','power':'^',
 '(':'(',')':')','pi':'\$m','\$m':'\$m','E':'E','e':'E',
 'ee':'E','EE':'E','\u1d07':'E','square':'^2','\u00b2':'^2','x\u00b2':'^2'}
$) keych(k):
 if $0(k)==1 $; '0'<=k<='9':
  $! k
 $! KEYCH.get(k)
$) evalnum(s):
 t=s.replace(' ','')
 $3 t $; t[-1]in '+-*/^(E':
  t=t[:-1]
 if t in('','.'):
  $! $#
 t+=')'*max(0,t.count('(')-t.count(')'))
 p=[0]
 $T:
  v=ev_sum(t,p)
 $&($:,$J,$>):
  $F $%
 if p[0]!=$0(t)or v!=v or $U(v)>1e300:
  $F $%
 $! v
$) ev_sum(t,p):
 v=ev_prod(t,p)
 $3 p[0]<$0(t)$; t[p[0]]in '+-':
  op=t[p[0]]
  p[0]+=1
  w=ev_prod(t,p)
  v=v+w if op=='+' $* v-w
 $! v
$) ev_prod(t,p):
 v=$<(t,p)
 $3 p[0]<$0(t)$; t[p[0]]in '*/(\$m':
  op=t[p[0]]
  if op in '*/':
   p[0]+=1
  w=$<(t,p)
  v=v/w if op=='/' $* v*w
 $! v
$) $<(t,p):
 if p[0]<$0(t)$; t[p[0]]in '+-':
  neg=t[p[0]]=='-'
  p[0]+=1
  v=$<(t,p)
  $!-v if neg $* v
 v=ev_atom(t,p)
 if p[0]<$0(t)$; t[p[0]]=='^':
  p[0]+=1
  e=$<(t,p)
  if v<0 $; e!=int(e):
   $F $%
  v=$h(v)**e
 $! v
$) ev_atom(t,p):
 i=p[0]
 if i<$0(t)$; t[i]=='(':
  p[0]+=1
  v=ev_sum(t,p)
  if p[0]>=$0(t)or t[p[0]]!=')':
   $F $%
  p[0]+=1
  $! v
 if i<$0(t)$; t[i]=='\$m':
  p[0]+=1
  $! $9.pi
 j=i
 $3 j<$0(t)$;(t[j].$W()or t[j]=='.'):
  j+=1
 if i<j<$0(t)$; t[j]=='E':
  k=j+1
  if k<$0(t)$; t[k]in '+-':
   k+=1
  if k<$0(t)$; t[k].$W():
   j=k
   $3 j<$0(t)$; t[j].$W():
    j+=1
 if j==i:
  $F $%
 p[0]=j
 $! $h(t[i:j])
NEGKEYS=('neg','(-)','\u207b','negative')
$) negkey(s):
 if s=='' or s[-1]in '+-*/^(E':
  $! s+'-'
 if s[:2]=='-(' $; s[-1]==')':
  $! s[2:-1]
 if s[:1]=='-' $; evalnum(s[1:])is $b $# $; $b[c $, c in s[1:]if c in '+-*/^(']:
  $! s[1:]
 $, c in s:
  if c in '+-*/^(':
   $! '-('+s+')'
 $! '-'+s
$) norm180(a):
 a=a%360
 $! a-360 if a>180 $* a
$) pw(a,b):
 if a<0:
  $F $%
 $! a**b
P0=1013.25
T0=288.15
KF=6.8755856e-6
A0=661.4786
$) delta(pa):
 $! pw(1-KF*pa,5.2558797)
$) isa(pa):
 $! 15-0.0019812*pa
$) palt(ia,qnh):
 $! ia+(1-pw(qnh/P0,0.190284))/KF
$) dalt(pa,oat):
 sigma=delta(pa)/((oat+273.15)/T0)
 $!(1-pw(sigma,0.234969))/KF
$) sound(oat):
 $! 38.967854*$9.sqrt(oat+273.15)
$) cas2mach(cas,pa):
 qc=pw(1+0.2*(cas/A0)**2,3.5)-1
 $! $9.sqrt(5*(pw(qc/delta(pa)+1,2/7.0)-1))
$) F(label,$8,default=$#,unit=0,fixed=0):
 $!(label,$8,default,unit,fixed)
$) T($/,fields,n,eqs,$g=$#,fast=$#,one=0):
 $!{'$/':$/,'f':fields,'n':n,'eqs':eqs,'$g':$g,
 'fast':fast,'one':one}
$) sc(a):
 $! $9.sin(a*RAD),$9.cos(a*RAD)
VECS=((4,1,1),(2,3,-1),(0,5,-1))
$) wind_eqs(v):
 x=y=0.0
 $, d,m,s in VECS:
  a,b=sc(v[d])
  x+=s*v[m]*a
  y+=s*v[m]*b
 $![x/100,y/100]
''')
_x(r'''$) wind_fast(v,bl):
 b=set(bl)
 $, d,m,s in VECS:
  if b==set((d,m)):
   x=y=0.0
   $, d2,m2,s2 in VECS:
    if d2!=d:
     a,c=sc(v[d2])
     x-=s2*v[m2]*a/s
     y-=s2*v[m2]*c/s
   $![$9.atan2(x,y)/RAD%360,$9.sqrt(x*x+y*y)][::1 if bl[0]==d $*-1]
 if b==set((4,5)):
  a,c=sc(v[2]-v[0])
  if v[1]<=0:
   $! $]
  s=v[3]*a/v[1]
  if $U(s)>1:
   $! $]
  wca=$9.asin(s)/RAD
  gs=v[1]*$9.cos(wca*RAD)-v[3]*c
  if gs<0:
   $! $]
  r={4:(v[0]+wca)%360,5:gs}
  $![r[i]$, i in bl]
 $! $#
$) wind_extra(v,u):
 wca=norm180(v[4]-v[0])
 side='' if $U(wca)<0.05 $*(' R' if wca>0 $* ' L')
 hw=v[3]*sc(v[2]-v[0])[1]
 $![('Wind corr. angle',$C($U(wca),1)+'\u00b0'+side),
 ('Magnetic heading',show(v[4]-v[6],'$o')+'\u00b0'),
 ('Headwind' if hw>=-0.05 $* 'Tailwind',$.($U(hw),'$j',u[1]))]
$) xw_eqs(v):
 a,c=sc(v[1]-v[0])
 $![(v[3]-v[2]*a)/10,(v[4]-v[2]*c)/10]
$) xw_fast(v,bl):
 b=set(bl)
 if b==set((3,4)):
  a,c=sc(v[1]-v[0])
  r={3:v[2]*a,4:v[2]*c}
 $4 b==set((1,2)):
  r={1:(v[0]+$9.atan2(v[3],v[4])/RAD)%360,
 2:$9.sqrt(v[3]**2+v[4]**2)}
 $*:
  $! $#
 $![r[i]$, i in bl]
$) xw_extra(v,u):
 out=[]
 if $U(v[3])>=0.05:
  out.$+(('$N from','$i' if v[3]>0 $* 'left'))
 if v[4]<-0.05:
  out.$+(('TAILWIND',$.(-v[4],'$j',u[2])))
 $! out
$) tsd_eqs(v):
 $![(v[1]-v[0]*v[2]/60)/100]
$) tsd_extra(v,u):
 $![('Per minute',$.(v[0]/60,'dist',u[1]))]
$) fuel_eqs(v):
 $![(v[2]-v[0]*v[1]/60)/10]
$) fuel_extra(v,u):
 $![('+45 min reserve',$.(v[2]+v[0]*0.75,'fuel',u[2]))]
$) alt_eqs(v):
 $![(v[3]-palt(v[0],v[1]))/1000,(v[4]-dalt(v[3],v[2]))/1000]
$) alt_extra(v,u):
 t=isa(v[3])
 $![('ISA temperature',$.(t,'$H',u[2])),
 ('ISA $Q',$l(v[2]-t,u[2]))]
$) tas_eqs(v):
 $![(v[4]-cas2mach(v[0],v[1]))*10,(v[3]-v[4]*sound(v[2]))/100]
$) tas_extra(v,u):
 $![('ISA $Q',$l(v[2]-isa(v[1]),u[2])),
 ('Speed of sound',$.(sound(v[2]),'$j',u[3]))]
$) ta_eqs(v):
 ia,oat,el,ta=v
 $![(ta-el-(ia-el)*(oat+273.15)/(isa(ia)+273.15))/1000]
$) ta_extra(v,u):
 $![('ISA $Q',$l(v[1]-isa(v[0]),u[1])),
 ('Correction',$.(v[3]-v[0],'$Y',u[3]))]
$) cb_eqs(v):
 $![(v[2]-(v[0]-v[1])*400)/1000]
$) cb_extra(v,u):
 $![('Base MSL',$.(v[2]+v[3],'$Y',u[2])),
 ('Spread',$l(v[0]-v[1],u[0]))]
$_=[
 T('Wind triangle',[F('$6 course','$o'),F('$6 airspeed','$j'),
 F('Wind from','$o'),F('Wind $k','$j'),
 F('$6 heading','$o'),F('Ground $k','$j'),
 F('Variation E+ W-','ang',0.0)],
 2,wind_eqs,wind_extra,wind_fast),
 T('$N',[F('Runway (27=270)','rwy'),F('Wind from','$o'),
 F('Wind $k','$j'),F('$N (+R)','sspd'),
 F('Headwind','sspd')],
 2,xw_eqs,xw_extra,xw_fast),
 T('Time $k distance',[F('Ground $k','$j'),F('Distance','dist'),
 F('Time','$f')],1,tsd_eqs,tsd_extra),
 T('Fuel',[F('Fuel flow','rate'),F('Time','$f'),F('Fuel','fuel')],
 1,fuel_eqs,fuel_extra),
 T('Altitudes / DA',[F('Indicated $Y','$Y'),F('Altimeter','$R'),
 F('OAT','$H'),F('$^ $Y','$Y'),
 F('Density $Y','$Y')],2,alt_eqs,alt_extra),
 T('Airspeed / TAS',[F('CAS (IAS)','$j'),F('$^ $Y','$Y'),
 F('OAT','$H'),F('$6 airspeed','$j'),
 F('Mach','mach')],2,tas_eqs,tas_extra),
 T('$6 $`',[F('Indicated $Y','$Y'),F('OAT at $`','$H'),
 F('Station elev','$Y',0.0),F('$6 $`','$Y')],
 1,ta_eqs,ta_extra),
 T('Cloud $V',[F('Temperature','$H'),F('Dew point','$H'),
 F('Base AGL','$Y'),F('Field elev','$Y',0.0)],
 1,cb_eqs,cb_extra),
 ]
$) unit_eqs(v):
 $![v[i]-v[0]$, i in $((1,$0(v))]
$) $-($/,$8,$E):
 fs=[F($E[i],$8,$#,i,1)$, i in $(($0($E))]
 $! T($/,fs,$0(fs)-1,unit_eqs,one=1)
$e=[
 $-('Speed','$j',('Knots','Miles/hour','Km/hour')),
 $-('Distance','dist',('Nautical mi','Statute mi','Kilometres')),
 $-('Altitude','$Y',('Feet','Metres')),
 $-('Temperature','$H',('Celsius','Fahrenheit')),
 $-('$^','$R',('Inches Hg','hPa / mb')),
 $-('Fuel','fuel',('US gallons','Litres','Imp gallons','$Z 6.0 lb/g','$Z',
 'Jet-A 6.7 lb/g','Jet-A')),
 $-('Fuel flow','rate',('US gal/hour','Litres/hour','$Z','Jet-A')),
 ]
$) resid(t,v):
 $! max([$U(r)$, r in t['eqs'](v)])
$) solve(t,$M,$==$#):
 fs=t['f']
 v=list($M)
 bl=[]
 $, i in $(($0(fs)):
  if v[i]is $#:
   if fs[i][2]is $#:
    bl.$+(i)
   $*:
    v[i]=fs[i][2]
 n=t['n']
 if $0(bl)>n:
  k=$0(bl)-n
  $! v,'enter %d more value%s'%(k,'s' if k>1 $* ''),[]
 if $0(bl)<n:
  if $b bl:
   $T:
    ok=resid(t,v)<1e-6
   $& $A:
    ok=$]
   $! v,('all $I agree' if ok $* '$I disagree: clear one'),[]
  $! v,'too many $I: clear %d'%(n-$0(bl)),[]
 x=$#
 if t['fast']:
  $T:
   x=t['fast'](v,bl)
  $& $A:
   x=$#
  if x is $]:
   $! v,'no solution',[]
  if x is $b $#:
   x=fix(t,bl,x)
 sing=0
 if x is $#:
  ss=seeds(t,v,bl,$=)
  $, s in ss:
   x=newton(t,v,bl,s)
   if x=='singular':
    sing+=1
    x=$#
   $4 x is $b $#:
    x=fix(t,bl,x)
    if x is $b $#:
     $P
 if x is $#:
  if sing==$0(ss):
   $! v,'these blanks need more info',[]
  $! v,'no solution',[]
 $, j in $(($0(bl)):
  v[bl[j]]=x[j]
 $! v,'solved',bl
$) fix(t,bl,x):
 out=[]
 $, j in $(($0(bl)):
  k=t['f'][bl[j]][1]
  a=x[j]
  if a!=a or $U(a)>1e9:
   $! $#
  if k in HDG:
   a=a%360
  $4 k in POS:
   if a<-1e-9 or(k=='$R' $; a<=0):
    $! $#
   a=max(a,0.0)
  $4 k=='$H' $; a<=-273.15:
   $! $#
  out.$+(a)
 $! out
$) cmean(angles):
 x=y=0.0
 $, a in angles:
  s,c=sc(a)
  x+=s
  y+=c
 if $U(x)+$U(y)<1e-9:
  $! 0.0
 $! $9.atan2(x,y)/RAD%360
''')
_x(r'''$) seeds(t,v,bl,$=):
 fs=t['f']
 hd=cmean([v[i]$, i in $(($0(fs))if fs[i][1]in HDG $; v[i]is $b $#])
 $V=[]
 $, i in bl:
  k=fs[i][1]
  if $= $; $=.get(i)is $b $#:
   $V.$+($=[i])
  $4 k in HDG:
   $V.$+(hd)
  $*:
   $V.$+(DEF[k])
 out=[$V]
 $o=[fs[i][1]in HDG $, i in bl]
 if $6 in $o:
  $, r in(0,90,180,270):
   out.$+([$V[j]+r+20*j if $o[j]$* $V[j]$, j in $(($0(bl))])
 $, f in(0.2,4.0):
  out.$+([$V[j]if $o[j]$* $V[j]*f $, j in $(($0(bl))])
 $! out
$) $G(t,v,bl,x):
 w=list(v)
 $, j in $(($0(bl)):
  w[bl[j]]=x[j]
 $! t['eqs'](w)
$) newton(t,v,bl,x):
 n=$0(bl)
 x=list(x)
 $T:
  f=$G(t,v,bl,x)
  nf=max([$U(r)$, r in f])
 $& $A:
  $! $#
 $, it in $((40):
  if nf<1e-10:
   $! x
  cols=[]
  $, j in $((n):
   h=1e-5*max(1.0,$U(x[j]))
   xp=list(x)
   xm=list(x)
   xp[j]+=h
   xm[j]-=h
   $T:
    fp=$G(t,v,bl,xp)
    fm=$G(t,v,bl,xm)
   $& $A:
    fp=$#
   if fp is $#:
    $T:
     fp=$G(t,v,bl,xp)
     fm=f
     h/=2
    $& $A:
     $! $#
   cols.$+([(fp[i]-fm[i])/(2*h)$, i in $((n)])
  dx=gauss([[cols[j][i]$, j in $((n)]+[-f[i]]$, i in $((n)],n)
  if dx is $#:
   $! 'singular' if it==0 $* $#
  lam=1.0
  $3 $6:
   xn=[x[j]+lam*dx[j]$, j in $((n)]
   $T:
    fn=$G(t,v,bl,xn)
    nn=max([$U(r)$, r in fn])
   $& $A:
    nn=$#
   if nn is $b $# $; nn<nf:
    $P
   lam/=2
   if lam<1e-3:
    $! x if nf<1e-8 $* $#
  x,f,nf=xn,fn,nn
 $! x if nf<1e-8 $* $#
$) gauss(a,n):
 big=0.0
 $, r in a:
  $, e in r[:n]:
   big=max(big,$U(e))
 $, c in $((n):
  p=c
  $, r in $((c+1,n):
   if $U(a[r][c])>$U(a[p][c]):
    p=r
  if $U(a[p][c])<=1e-7*big:
   $! $#
  a[c],a[p]=a[p],a[c]
  $, r in $((n):
   if r!=c:
    m=a[r][c]/a[c][c]
    $, k in $((c,n+1):
     a[r][k]-=m*a[c][k]
 $![a[i][n]/a[i][i]$, i in $((n)]
$) calc(t,$M,$==$#):
 v,msg,$B=solve(t,$M,$=)
 ex=[]
 if t['$g']$; $# $b in v:
  u=[f[3]$, f in t['f']]
  $T:
   ex=t['$g'](v,u)
  $& $A:
   ex=[]
 $! v,msg,$B,ex
G={}
MEM={}
$) $X():
 $p=findkey()
 $T:
  import $2
 $& $@:
  $2=$#
 if $p is $# or $2 is $#:
  $S('$X: no full-screen mode here (%s), $7 version.'
 %('no $p function' if $p is $# $* 'no $2'))
  $! textmode()
 G['d']=$2
 G['$p']=$p
 G['cmode']=0
 $T:
  w,h=$2.get_screen_dim()
  w=int(w)
  h=int(h)
 $& $O:
  w,h=318,212
 G['w']=w
 G['h']=h
 $T:
  $2.use_buffer()
  G['buffer']=$6
 $& $O:
  G['buffer']=$]
 $T:
  mainmenu()
 $& KeyboardInterrupt:
  pass
 $T:
  color(C_WHITE)
  $2.fill_rect(0,0,w,h)
  $c()
 $& $O:
  pass
MAIN=[t['$/']$, t in $_]+['Units','Help','Key test']
$) mainmenu():
 $3 $6:
  a=choose('$X '+VERSION+'   esc quits',MAIN)
  if a is $#:
   $!
  if a<$0($_):
   form($_[a])
  $4 MAIN[a]=='Units':
   $3 $6:
    b=choose('Units',[t['$/']$, t in $e])
    if b is $#:
     $P
    form($e[b])
  $4 MAIN[a]=='Help':
   $D()
  $*:
   keytest()
KEYFN=('get_key','getkey','getKey','wait_key','waitkey')
$) findkey():
 $, mn in('ti_system','$2','ti_plotlib'):
  $T:
   m=__import__(mn)
  $& $@:
   $a
  $, fn in KEYFN:
   f=getattr(m,fn,$#)
   if f is $b $#:
    $! keyfun(f)
 $! $#
$) keyfun(f):
 $T:
  from $f import sleep
 $& $@:
  sleep=$#
 mode=[1]
 $) wait(x=1):
  if mode[0]:
   $T:
    $! str(f(1))
   $& $>:
    mode[0]=0
  $3 $6:
   k=f()
   if k:
    $! str(k)
   if sleep:
    sleep(0.02)
 $! wait
$) color(c):
 d=G['d']
 if G['cmode']==0:
  $T:
   d.set_color(c[0],c[1],c[2])
   $!
  $& $>:
   G['cmode']=1
 d.set_color(c)
$) $7(x,y,s,c):
 color(c)
 G['d'].draw_text(x,y+BASE,s)
$) box(x,y,w,h,c):
 color(c)
 G['d'].fill_rect(x,y,w,h)
$) $c():
 if G['buffer']:
  G['d'].paint_buffer()
$) bars($/,$5):
 w=G['w']
 h=G['h']
 box(0,0,w,h,C_WHITE)
 box(0,0,w,LH,C_BAR)
 $7(4,0,$/,$d)
 box(0,h-LH,w,LH,C_BAR)
 $7(4,h-LH,$5[:(w-8)//AW],$d)
$) choose($/,$E):
 n=$0($E)
 i=G.get('ch',{}).get($/,0)
 $K=(G['h']-2*LH-4)//LH
 $L=0
 $3 $6:
  if i<$L:
   $L=i
  if i>=$L+$K:
   $L=i-$K+1
  bars($/,'enter or 1-9 a-p picks   esc back')
  y=LH+2
  $, j in $(($L,min(n,$L+$K)):
   if j==i:
    box(0,y,G['w'],LH,C_SEL)
   $7(8,y,KEYS[j]if j<$0(KEYS)$* ' ',$?)
   $7(26,y,$E[j],$[)
   y+=LH
  if $L+$K<n:
   $7(G['w']-16,y-LH,'v',$?)
  $c()
  k=G['$p'](1)
  if k=='up':
   i=(i-1)%n
  $4 k=='down':
   i=(i+1)%n
  $4 k in ENTER or k=='$i':
   $P
  $4 k in('esc','left')or k in MENU:
   $! $#
  $4 $0(k)==1 $; k in KEYS[:n]:
   i=KEYS.index(k)
   $P
 G.setdefault('ch',{})[$/]=i
 $! i
$) newstate(t):
 $!{'txt':['' $, f in t['f']],'u':[f[3]$, f in t['f']],
 '$n':0,'$L':0,'$=':{}}
$) $I(t,st):
 v=[]
 bad=$#
 $, i in $(($0(t['f'])):
  s=st['txt'][i]
  if s=='':
   v.$+($#)
   $a
  $T:
   v.$+(parse(s,t['f'][i][1],st['u'][i]))
  $& $%:
   v.$+($#)
   if bad is $#:
    bad=i
 $! v,bad
$) form(t):
 st=MEM.get(t['$/'])
 if st is $#:
  st=newstate(t)
  MEM[t['$/']]=st
 msg=''
 $3 $6:
  $M,bad=$I(t,st)
  if bad is $b $#:
   v,$5,$B,ex=$M,'$b a number: '+t['f'][bad][0],[],[]
  $*:
   v,$5,$B,ex=calc(t,$M,st['$='])
   st['$=']=dict([(i,v[i])$, i in $B])
  drawform(t,st,v,$B,ex,msg or $5,bad is $b $# or $5[:2]in('no','to','va'))
  msg=''
  k=G['$p'](1)
  r=formkey(t,st,k,v,$B)
  if r=='back':
   $!
  if r:
   msg=r
$) unitname(t,st,i):
 f=t['f'][i]
 $! $1[f[1]][st['u'][i]][0]
''')
_x(r'''$) formkey(t,st,k,v,$B):
 fs=t['f']
 n=$0(fs)
 i=st['$n']
 s=st['txt'][i]
 if k in('esc',)or k in MENU:
  $! 'back'
 if k=='up' or k in BACKTAB:
  st['$n']=(i-1)%n
 $4 k in('down','tab')or k in ENTER:
  st['$n']=(i+1)%n
 $4 k in('left','$i'):
  us=$1[fs[i][1]]
  if fs[i][4]or $0(us)<2:
   $! 'this field has one unit'
  old=st['u'][i]
  new=(old+(1 if k=='$i' $*-1))%$0(us)
  if s:
   $T:
    st['txt'][i]=edtext(parse(s,fs[i][1],old),fs[i][1],new)
   $& $%:
    pass
  st['u'][i]=new
 $4 k in DELKEYS:
  st['txt'][i]=s[:-1]
 $4 k=='clear':
  st['txt'][i]=''
 $4 k in NEGKEYS:
  st['txt'][i]=negkey(s)
 $4 k==':' or keych(k)is $b $#:
  c=keych(k)or k
  if c==':' $; fs[i][1]!='$f':
   $! ': is only $, times (h:mm)'
  if t['one']:
   $, j in $((n):
    if j!=i:
     st['txt'][j]=''
  if $0(s)<MAXT:
   st['txt'][i]=s+c
 $4 k in('?','help','cat','catalog'):
  $D()
 $*:
  $! '$p '+repr(k)[:20]+': $b used here'
 $! $#
$) drawform(t,st,v,$B,ex,$5,err):
 w=G['w']
 h=G['h']
 fs=t['f']
 n=$0(fs)
 $K=(h-2*LH-2)//RH
 total=n+$0(ex)
 $n=st['$n']
 $L=st['$L']
 if $n<$L:
  $L=$n
 if $n>=$L+$K:
  $L=$n-$K+1
 if $n==n-1:
  $L=max($L,min($n,total-$K))
 st['$L']=$L
 bars(t['$/'],$5)
 if err:
  box(0,h-LH,w,LH,C_ERR)
  $7(4,h-LH,$5[:(w-8)//AW],$d)
 xv=w-70
 y=LH+1
 $, j in $(($L,min(total,$L+$K)):
  if j<n:
   f=fs[j]
   if j==$n:
    box(0,y,w,RH,C_SEL)
   $7(6,y,f[0],$[)
   s=st['txt'][j]
   c=$[
   if s=='':
    if v[j]is $#:
     s,c='?',$?
    $*:
     s=show(v[j],f[1],st['u'][j])
     c=C_RES if j in $B $* $?
   room=(xv-14)//AW-$0(f[0])
   if $0(s)>room:
    s='<'+s[$0(s)-room+1:]
   $7(xv-AW*$0(s),y,s,c)
   if j==$n:
    box(xv+1,y+2,2,RH-4,C_CUR)
   $7(xv+6,y,unitname(t,st,j),$?)
  $*:
   lab,val=ex[j-n]
   $7(6,y,lab,$?)
   $7(w-6-AW*$0(val),y,val,C_RES)
  y+=RH
 if $L+$K<total:
  $7(w-12,y-RH,'v',$?)
 $c()
HELP=(
 'Type the $I you know; blank',
 'fields (?) are solved as you type.',
 'up/down/tab/enter   next field',
 'left/$i   change the unit',
 'del  backspace    clear  blank field',
 'Sums work: 120+15, 3/4, 2^10, 2(1+pi)',
 'esc/menu  tool list.  IAS = CAS.',
 'Blue = solved. Grey = default.',
 'Runway 27 = 270. Time 1:30 or 90.',
 'Variation: East +, West -.',
 )
$) $D():
 bars('$X help','$R any $p')
 y=LH+1
 $, s in HELP:
  $7(6,y,s,$[)
  y+=RH
 $c()
 G['$p'](1)
$) keytest():
 $==''
 $3 $6:
  bars('Key test','esc twice to stop')
  $7(10,3*LH,'Last $p:',$?)
  $7(10,4*LH+4,repr($=),$[)
  $c()
  k=G['$p'](1)
  if k=='esc' $; $==='esc':
   $!
  $==k
$) textmode():
 all_=$_+$e
 $3 $6:
  $S('')
  $, i in $(($0(all_)):
   $S('%2d %s%s'%(i+1,all_[i]['$/'],' (units)' if i>=$0($_)$* ''))
  s=input('tool number (q quits): ').strip()
  if s in('q','quit',''):
   $!
  $T:
   t=all_[int(s)-1]
  $&($%,IndexError):
   $a
  $M=[]
  $, f in t['f']:
   un=$1[f[1]][f[3]][0]
   $3 $6:
    a=input('%s [%s]: '%(f[0],un)).strip()
    if a=='':
     $M.$+($#)
     $P
    $T:
     $M.$+(parse(a,f[1],f[3]))
     $P
    $& $%:
     $S('$b a number')
  v,msg,$B,ex=calc(t,$M)
  $S('-- '+msg)
  $, i in $(($0(t['f'])):
   f=t['f'][i]
   if v[i]is $b $#:
    $S('%-17s %s %s%s'%(f[0],show(v[i],f[1],f[3]),
 $1[f[1]][f[3]][0],'  *' if i in $B $* ''))
  $, lab,val in ex:
   $S('%-17s %s'%(lab,val))
''')
del _x
navcalc()
