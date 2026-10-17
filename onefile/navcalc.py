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
_W={'!': 'return', '#': 'None', '%': 'except', '&': 'range', '(': 'def', ')': 'else', '*': 'append', '+': 'ValueError', ',': 'unit_tool', '-': 'for', '.': 'withunit', '/': 'title', '0': 'UNITS', '1': 'ti_draw', '2': 'elif', '3': 'status', '4': 'True', '5': 'text', '6': 'len', '7': 'kind', '8': 'last', '9': 'math', ':': 'C_DIM', ';': 'ImportError', '<': 'while', '=': 'ARITH', '>': 'done', '?': 'fmtnum', '@': 'helpscreen', 'A': 'labels', 'B': 'resvec', 'C': 'temp', 'D': 'values', 'E': 'rows', 'F': 'top', 'G': 'vals', 'H': 'Crosswind', 'I': 'Exception', 'J': 'TypeError', 'K': 'break', 'L': 'deviation', 'M': 'press', 'N': 'print', 'O': 'base', 'P': 'navcalc', 'Q': 'try', 'R': 'abs', 'S': 'alt', 'T': 'Avgas', 'U': 'C_TXT', 'V': 'False', 'W': 'Pressure', 'X': 'TOOLS', 'Y': 'altitude', 'Z': 'continue', '[': 'show_', ']': 'not', '^': 'C_BART', '_': 'UTOOLS', '`': 'time', 'a': 'and', 'b': 'extra', 'c': 'right', 'd': 'spd', 'e': 'speed', 'f': 'tdiff', 'g': 'sel', 'h': 'hdg', 'i': 'key', 'j': 'txt'}
_x(r'''import $9
VERSION='1.0'
RAD=$9.pi/180
LH=18
RH=17
BASE=14
AW=7
C_BAR=(30,60,130)
$^=(255,255,255)
$U=(0,0,0)
C_RES=(0,70,170)
C_ERR=(190,0,0)
C_SEL=(205,225,255)
$:=(110,110,110)
C_CUR=(220,0,0)
C_WHITE=(255,255,255)
ENTER=('enter','ret','$!','center','\r','\n')
MENU=('menu',)
BACKTAB=('shift+tab','shift tab','shifttab','backtab','btab')
DELKEYS=('del','backspace','bksp')
NEG=('-','neg','(-)','\u2212','\u207b')
KEYS='123456789abcdefghijklmnop'
LBKG=0.45359237
AVGAS=6.0
JETA=6.7
$0={
 '$d':(('kt',1.0,0,1),('mph',1.150779,0,1),('km/h',1.852,0,1)),
 'dist':(('nm',1.0,0,1),('sm',1.150779,0,1),('km',1.852,0,1)),
 '$S':(('ft',1.0,0,0),('m',0.3048,0,0)),
 '$C':(('\u00b0C',1.0,0,1),('\u00b0F',1.8,32,1)),
 '$M':(('inHg',1/33.8639,0,2),('hPa',1.0,0,1)),
 'fuel':(('USG',1.0,0,1),('L',3.785412,0,1),('Imp gal',0.832674,0,1),
 ('lb $T',AVGAS,0,0),('kg $T',AVGAS*LBKG,0,0),
 ('lb Jet-A',JETA,0,0),('kg Jet-A',JETA*LBKG,0,0)),
 'rate':(('gph',1.0,0,1),('L/h',3.785412,0,1),
 ('pph $T',AVGAS,0,0),('pph Jet-A',JETA,0,0)),
 '$`':(('h:mm',1.0,0,0),('min',1.0,0,1),('h',1/60.0,0,2)),
 '$h':(('\u00b0',1.0,0,0),),
 'ang':(('\u00b0',1.0,0,1),),
 'mach':(('M',1.0,0,3),),
 }
$0['sspd']=$0['$d']
$0['rwy']=$0['$h']
HDG=('$h','rwy')
POS=('$d','dist','$`','fuel','rate','mach','$M')
DEF={'$d':100.0,'sspd':10.0,'dist':100.0,'$`':60.0,'fuel':20.0,
 'rate':10.0,'$S':3000.0,'$C':15.0,'$M':1013.25,'mach':0.3,
 '$h':0.0,'rwy':0.0,'ang':0.0}
$==($+,ZeroDivisionError,OverflowError,$J)
$( $?(x,dec):
 s=('%.'+str(dec)+'f')%x
 if s[:1]=='-' $a float(s)==0:
  s=s[1:]
 $! s
$( hmm(m):
 if $R(m)>1e7:
  $! $?(m,0)
 t=int($9.floor($R(m)+0.5))
 $!('-' if m<0 $a t $) '')+'%d:%02d'%(t//60,t%60)
$( show(x,$7,u=0):
 if $7 in HDG:
  r=int($9.floor(x%360+0.5))%360
  $! '%03d'%(r or 360)
 un=$0[$7][u]
 if un[0]=='h:mm':
  $! hmm(x)
 $! $?(x*un[1]+un[2],un[3])
$( edtext(x,$7,u):
 un=$0[$7][u]
 if un[0]=='h:mm':
  $! hmm(x)
 s=$?(x*un[1]+un[2],un[3]+2)
 if '.' in s:
  s=s.rstrip('0').rstrip('.')
 $! s
$( $f(x,u):
 $! $?(x*$0['$C'][u][1],1)+' '+$0['$C'][u][0]
$( $.(x,$7,u):
 $! show(x,$7,u)+' '+$0[$7][u][0]
$( parse(s,$7,u):
 if ':' in s:
  if $7!='$`':
   raise $+
  a,b=s.split(':',1)
  m=$R(float(a or '0'))*60+float(b or '0')
  $!-m if s[:1]=='-' $) m
 x=float(s)
 if $7=='rwy' $a '.' $] in s $a 'E' $] in s $a 0<x<=36:
  x*=10
 un=$0[$7][u]
 $!(x-un[2])/un[1]
$( norm180(a):
 a=a%360
 $! a-360 if a>180 $) a
$( pw(a,b):
 if a<0:
  raise $+
 $! a**b
P0=1013.25
T0=288.15
KF=6.8755856e-6
A0=661.4786
$( delta(pa):
 $! pw(1-KF*pa,5.2558797)
$( isa(pa):
 $! 15-0.0019812*pa
$( palt(ia,qnh):
 $! ia+(1-pw(qnh/P0,0.190284))/KF
$( dalt(pa,oat):
 sigma=delta(pa)/((oat+273.15)/T0)
 $!(1-pw(sigma,0.234969))/KF
$( sound(oat):
 $! 38.967854*$9.sqrt(oat+273.15)
$( cas2mach(cas,pa):
 qc=pw(1+0.2*(cas/A0)**2,3.5)-1
 $! $9.sqrt(5*(pw(qc/delta(pa)+1,2/7.0)-1))
$( F(label,$7,default=$#,unit=0,fixed=0):
 $!(label,$7,default,unit,fixed)
$( T($/,fields,n,eqs,$b=$#,fast=$#,one=0):
 $!{'$/':$/,'f':fields,'n':n,'eqs':eqs,'$b':$b,
 'fast':fast,'one':one}
$( sc(a):
 $! $9.sin(a*RAD),$9.cos(a*RAD)
VECS=((4,1,1),(2,3,-1),(0,5,-1))
$( wind_eqs(v):
 x=y=0.0
 $- d,m,s in VECS:
  a,b=sc(v[d])
  x+=s*v[m]*a
  y+=s*v[m]*b
 $![x/100,y/100]
$( wind_fast(v,bl):
 b=set(bl)
 $- d,m,s in VECS:
  if b==set((d,m)):
   x=y=0.0
   $- d2,m2,s2 in VECS:
    if d2!=d:
     a,c=sc(v[d2])
     x-=s2*v[m2]*a/s
     y-=s2*v[m2]*c/s
   $![$9.atan2(x,y)/RAD%360,$9.sqrt(x*x+y*y)][::1 if bl[0]==d $)-1]
 if b==set((4,5)):
  a,c=sc(v[2]-v[0])
  if v[1]<=0:
   $! $V
  s=v[3]*a/v[1]
  if $R(s)>1:
   $! $V
  wca=$9.asin(s)/RAD
  gs=v[1]*$9.cos(wca*RAD)-v[3]*c
  if gs<0:
   $! $V
  r={4:(v[0]+wca)%360,5:gs}
  $![r[i]$- i in bl]
 $! $#
$( wind_extra(v,u):
 wca=norm180(v[4]-v[0])
 side='' if $R(wca)<0.05 $)(' R' if wca>0 $) ' L')
 hw=v[3]*sc(v[2]-v[0])[1]
 $![('Wind corr. angle',$?($R(wca),1)+'\u00b0'+side),
 ('Magnetic heading',show(v[4]-v[6],'$h')+'\u00b0'),
 ('Headwind' if hw>=-0.05 $) 'Tailwind',$.($R(hw),'$d',u[1]))]
$( xw_eqs(v):
 a,c=sc(v[1]-v[0])
 $![(v[3]-v[2]*a)/10,(v[4]-v[2]*c)/10]
$( xw_fast(v,bl):
 b=set(bl)
 if b==set((3,4)):
  a,c=sc(v[1]-v[0])
  r={3:v[2]*a,4:v[2]*c}
 $2 b==set((1,2)):
  r={1:(v[0]+$9.atan2(v[3],v[4])/RAD)%360,
 2:$9.sqrt(v[3]**2+v[4]**2)}
 $):
  $! $#
 $![r[i]$- i in bl]
$( xw_extra(v,u):
 out=[]
 if $R(v[3])>=0.05:
  out.$*(('$H from','$c' if v[3]>0 $) 'left'))
 if v[4]<-0.05:
  out.$*(('TAILWIND',$.(-v[4],'$d',u[2])))
 $! out
$( tsd_eqs(v):
 $![(v[1]-v[0]*v[2]/60)/100]
$( tsd_extra(v,u):
 $![('Per minute',$.(v[0]/60,'dist',u[1]))]
$( fuel_eqs(v):
 $![(v[2]-v[0]*v[1]/60)/10]
$( fuel_extra(v,u):
 $![('+45 min reserve',$.(v[2]+v[0]*0.75,'fuel',u[2]))]
$( alt_eqs(v):
 $![(v[3]-palt(v[0],v[1]))/1000,(v[4]-dalt(v[3],v[2]))/1000]
$( alt_extra(v,u):
 t=isa(v[3])
 $![('ISA temperature',$.(t,'$C',u[2])),
 ('ISA $L',$f(v[2]-t,u[2]))]
$( tas_eqs(v):
 $![(v[4]-cas2mach(v[0],v[1]))*10,(v[3]-v[4]*sound(v[2]))/100]
$( tas_extra(v,u):
 $![('ISA $L',$f(v[2]-isa(v[1]),u[2])),
 ('Speed of sound',$.(sound(v[2]),'$d',u[3]))]
$( ta_eqs(v):
 ia,oat,el,ta=v
 $![(ta-el-(ia-el)*(oat+273.15)/(isa(ia)+273.15))/1000]
$( ta_extra(v,u):
 $![('ISA $L',$f(v[1]-isa(v[0]),u[1])),
 ('Correction',$.(v[3]-v[0],'$S',u[3]))]
$( cb_eqs(v):
 $![(v[2]-(v[0]-v[1])*400)/1000]
$( cb_extra(v,u):
 $![('Base MSL',$.(v[2]+v[3],'$S',u[2])),
 ('Spread',$f(v[0]-v[1],u[0]))]
''')
_x(r'''$X=[
 T('Wind triangle',[F('$4 course','$h'),F('$4 airspeed','$d'),
 F('Wind from','$h'),F('Wind $e','$d'),
 F('$4 heading','$h'),F('Ground $e','$d'),
 F('Variation E+ W-','ang',0.0)],
 2,wind_eqs,wind_extra,wind_fast),
 T('$H',[F('Runway (27=270)','rwy'),F('Wind from','$h'),
 F('Wind $e','$d'),F('$H (+R)','sspd'),
 F('Headwind','sspd')],
 2,xw_eqs,xw_extra,xw_fast),
 T('Time $e distance',[F('Ground $e','$d'),F('Distance','dist'),
 F('Time','$`')],1,tsd_eqs,tsd_extra),
 T('Fuel',[F('Fuel flow','rate'),F('Time','$`'),F('Fuel','fuel')],
 1,fuel_eqs,fuel_extra),
 T('Altitudes / DA',[F('Indicated $S','$S'),F('Altimeter','$M'),
 F('OAT','$C'),F('$W $S','$S'),
 F('Density $S','$S')],2,alt_eqs,alt_extra),
 T('Airspeed / TAS',[F('CAS (IAS)','$d'),F('$W $S','$S'),
 F('OAT','$C'),F('$4 airspeed','$d'),
 F('Mach','mach')],2,tas_eqs,tas_extra),
 T('$4 $Y',[F('Indicated $S','$S'),F('OAT at $Y','$C'),
 F('Station elev','$S',0.0),F('$4 $Y','$S')],
 1,ta_eqs,ta_extra),
 T('Cloud $O',[F('Temperature','$C'),F('Dew point','$C'),
 F('Base AGL','$S'),F('Field elev','$S',0.0)],
 1,cb_eqs,cb_extra),
 ]
$( unit_eqs(v):
 $![v[i]-v[0]$- i in $&(1,$6(v))]
$( $,($/,$7,$A):
 fs=[F($A[i],$7,$#,i,1)$- i in $&($6($A))]
 $! T($/,fs,$6(fs)-1,unit_eqs,one=1)
$_=[
 $,('Speed','$d',('Knots','Miles/hour','Km/hour')),
 $,('Distance','dist',('Nautical mi','Statute mi','Kilometres')),
 $,('Altitude','$S',('Feet','Metres')),
 $,('Temperature','$C',('Celsius','Fahrenheit')),
 $,('$W','$M',('Inches Hg','hPa / mb')),
 $,('Fuel','fuel',('US gallons','Litres','Imp gallons','$T 6.0 lb/g','$T',
 'Jet-A 6.7 lb/g','Jet-A')),
 $,('Fuel flow','rate',('US gal/hour','Litres/hour','$T','Jet-A')),
 ]
$( resid(t,v):
 $! max([$R(r)$- r in t['eqs'](v)])
$( solve(t,$G,$8=$#):
 fs=t['f']
 v=list($G)
 bl=[]
 $- i in $&($6(fs)):
  if v[i]is $#:
   if fs[i][2]is $#:
    bl.$*(i)
   $):
    v[i]=fs[i][2]
 n=t['n']
 if $6(bl)>n:
  k=$6(bl)-n
  $! v,'enter %d more value%s'%(k,'s' if k>1 $) ''),[]
 if $6(bl)<n:
  if $] bl:
   $Q:
    ok=resid(t,v)<1e-6
   $% $=:
    ok=$V
   $! v,('all $D agree' if ok $) '$D disagree: clear one'),[]
  $! v,'too many $D: clear %d'%(n-$6(bl)),[]
 x=$#
 if t['fast']:
  $Q:
   x=t['fast'](v,bl)
  $% $=:
   x=$#
  if x is $V:
   $! v,'no solution',[]
  if x is $] $#:
   x=fix(t,bl,x)
 sing=0
 if x is $#:
  ss=seeds(t,v,bl,$8)
  $- s in ss:
   x=newton(t,v,bl,s)
   if x=='singular':
    sing+=1
    x=$#
   $2 x is $] $#:
    x=fix(t,bl,x)
    if x is $] $#:
     $K
 if x is $#:
  if sing==$6(ss):
   $! v,'these blanks need more info',[]
  $! v,'no solution',[]
 $- j in $&($6(bl)):
  v[bl[j]]=x[j]
 $! v,'solved',bl
$( fix(t,bl,x):
 out=[]
 $- j in $&($6(bl)):
  k=t['f'][bl[j]][1]
  a=x[j]
  if a!=a or $R(a)>1e9:
   $! $#
  if k in HDG:
   a=a%360
  $2 k in POS:
   if a<-1e-9 or(k=='$M' $a a<=0):
    $! $#
   a=max(a,0.0)
  $2 k=='$C' $a a<=-273.15:
   $! $#
  out.$*(a)
 $! out
$( cmean(angles):
 x=y=0.0
 $- a in angles:
  s,c=sc(a)
  x+=s
  y+=c
 if $R(x)+$R(y)<1e-9:
  $! 0.0
 $! $9.atan2(x,y)/RAD%360
$( seeds(t,v,bl,$8):
 fs=t['f']
 hd=cmean([v[i]$- i in $&($6(fs))if fs[i][1]in HDG $a v[i]is $] $#])
 $O=[]
 $- i in bl:
  k=fs[i][1]
  if $8 $a $8.get(i)is $] $#:
   $O.$*($8[i])
  $2 k in HDG:
   $O.$*(hd)
  $):
   $O.$*(DEF[k])
 out=[$O]
 $h=[fs[i][1]in HDG $- i in bl]
 if $4 in $h:
  $- r in(0,90,180,270):
   out.$*([$O[j]+r+20*j if $h[j]$) $O[j]$- j in $&($6(bl))])
 $- f in(0.2,4.0):
  out.$*([$O[j]if $h[j]$) $O[j]*f $- j in $&($6(bl))])
 $! out
$( $B(t,v,bl,x):
 w=list(v)
 $- j in $&($6(bl)):
  w[bl[j]]=x[j]
 $! t['eqs'](w)
$( newton(t,v,bl,x):
 n=$6(bl)
 x=list(x)
 $Q:
  f=$B(t,v,bl,x)
  nf=max([$R(r)$- r in f])
 $% $=:
  $! $#
 $- it in $&(40):
  if nf<1e-10:
   $! x
  cols=[]
  $- j in $&(n):
   h=1e-5*max(1.0,$R(x[j]))
   xp=list(x)
   xm=list(x)
   xp[j]+=h
   xm[j]-=h
   $Q:
    fp=$B(t,v,bl,xp)
    fm=$B(t,v,bl,xm)
   $% $=:
    fp=$#
   if fp is $#:
    $Q:
     fp=$B(t,v,bl,xp)
     fm=f
     h/=2
    $% $=:
     $! $#
   cols.$*([(fp[i]-fm[i])/(2*h)$- i in $&(n)])
  dx=gauss([[cols[j][i]$- j in $&(n)]+[-f[i]]$- i in $&(n)],n)
  if dx is $#:
   $! 'singular' if it==0 $) $#
  lam=1.0
  $< $4:
   xn=[x[j]+lam*dx[j]$- j in $&(n)]
   $Q:
    fn=$B(t,v,bl,xn)
    nn=max([$R(r)$- r in fn])
   $% $=:
    nn=$#
   if nn is $] $# $a nn<nf:
    $K
   lam/=2
   if lam<1e-3:
    $! x if nf<1e-8 $) $#
  x,f,nf=xn,fn,nn
 $! x if nf<1e-8 $) $#
$( gauss(a,n):
 big=0.0
 $- r in a:
  $- e in r[:n]:
   big=max(big,$R(e))
 $- c in $&(n):
  p=c
  $- r in $&(c+1,n):
   if $R(a[r][c])>$R(a[p][c]):
    p=r
  if $R(a[p][c])<=1e-7*big:
   $! $#
  a[c],a[p]=a[p],a[c]
  $- r in $&(n):
   if r!=c:
    m=a[r][c]/a[c][c]
    $- k in $&(c,n+1):
     a[r][k]-=m*a[c][k]
 $![a[i][n]/a[i][i]$- i in $&(n)]
$( calc(t,$G,$8=$#):
 v,msg,$>=solve(t,$G,$8)
 ex=[]
 if t['$b']$a $# $] in v:
  u=[f[3]$- f in t['f']]
  $Q:
   ex=t['$b'](v,u)
  $% $=:
   ex=[]
 $! v,msg,$>,ex
G={}
MEM={}
''')
_x(r'''$( $P():
 $i=findkey()
 $Q:
  import $1
 $% $;:
  $1=$#
 if $i is $# or $1 is $#:
  $N('$P: no full-screen mode here (%s), $5 version.'
 %('no $i function' if $i is $# $) 'no $1'))
  $! textmode()
 G['d']=$1
 G['$i']=$i
 G['cmode']=0
 $Q:
  w,h=$1.get_screen_dim()
  w=int(w)
  h=int(h)
 $% $I:
  w,h=318,212
 G['w']=w
 G['h']=h
 $Q:
  $1.use_buffer()
  G['buffer']=$4
 $% $I:
  G['buffer']=$V
 $Q:
  mainmenu()
 $% KeyboardInterrupt:
  pass
 $Q:
  color(C_WHITE)
  $1.fill_rect(0,0,w,h)
  $[()
 $% $I:
  pass
MAIN=[t['$/']$- t in $X]+['Units','Help','Key test']
$( mainmenu():
 $< $4:
  a=choose('$P '+VERSION+'   esc quits',MAIN)
  if a is $#:
   $!
  if a<$6($X):
   form($X[a])
  $2 MAIN[a]=='Units':
   $< $4:
    b=choose('Units',[t['$/']$- t in $_])
    if b is $#:
     $K
    form($_[b])
  $2 MAIN[a]=='Help':
   $@()
  $):
   keytest()
KEYFN=('get_key','getkey','getKey','wait_key','waitkey')
$( findkey():
 $- mn in('ti_system','$1','ti_plotlib'):
  $Q:
   m=__import__(mn)
  $% $;:
   $Z
  $- fn in KEYFN:
   f=getattr(m,fn,$#)
   if f is $] $#:
    $! keyfun(f)
 $! $#
$( keyfun(f):
 $Q:
  from $` import sleep
 $% $;:
  sleep=$#
 mode=[1]
 $( wait(x=1):
  if mode[0]:
   $Q:
    $! str(f(1))
   $% $J:
    mode[0]=0
  $< $4:
   k=f()
   if k:
    $! str(k)
   if sleep:
    sleep(0.02)
 $! wait
$( color(c):
 d=G['d']
 if G['cmode']==0:
  $Q:
   d.set_color(c[0],c[1],c[2])
   $!
  $% $J:
   G['cmode']=1
 d.set_color(c)
$( $5(x,y,s,c):
 color(c)
 G['d'].draw_text(x,y+BASE,s)
$( box(x,y,w,h,c):
 color(c)
 G['d'].fill_rect(x,y,w,h)
$( $[():
 if G['buffer']:
  G['d'].paint_buffer()
$( bars($/,$3):
 w=G['w']
 h=G['h']
 box(0,0,w,h,C_WHITE)
 box(0,0,w,LH,C_BAR)
 $5(4,0,$/,$^)
 box(0,h-LH,w,LH,C_BAR)
 $5(4,h-LH,$3[:(w-8)//AW],$^)
$( choose($/,$A):
 n=$6($A)
 i=G.get('ch',{}).get($/,0)
 $E=(G['h']-2*LH-4)//LH
 $F=0
 $< $4:
  if i<$F:
   $F=i
  if i>=$F+$E:
   $F=i-$E+1
  bars($/,'enter or 1-9 a-p picks   esc back')
  y=LH+2
  $- j in $&($F,min(n,$F+$E)):
   if j==i:
    box(0,y,G['w'],LH,C_SEL)
   $5(8,y,KEYS[j]if j<$6(KEYS)$) ' ',$:)
   $5(26,y,$A[j],$U)
   y+=LH
  if $F+$E<n:
   $5(G['w']-16,y-LH,'v',$:)
  $[()
  k=G['$i'](1)
  if k=='up':
   i=(i-1)%n
  $2 k=='down':
   i=(i+1)%n
  $2 k in ENTER or k=='$c':
   $K
  $2 k in('esc','left')or k in MENU:
   $! $#
  $2 $6(k)==1 $a k in KEYS[:n]:
   i=KEYS.index(k)
   $K
 G.setdefault('ch',{})[$/]=i
 $! i
$( newstate(t):
 $!{'$j':['' $- f in t['f']],'u':[f[3]$- f in t['f']],
 '$g':0,'$F':0,'$8':{}}
$( $D(t,st):
 v=[]
 bad=$#
 $- i in $&($6(t['f'])):
  s=st['$j'][i]
  if s=='':
   v.$*($#)
   $Z
  $Q:
   v.$*(parse(s,t['f'][i][1],st['u'][i]))
  $% $+:
   v.$*($#)
   if bad is $#:
    bad=i
 $! v,bad
$( form(t):
 st=MEM.get(t['$/'])
 if st is $#:
  st=newstate(t)
  MEM[t['$/']]=st
 msg=''
 $< $4:
  $G,bad=$D(t,st)
  if bad is $] $#:
   v,$3,$>,ex=$G,'$] a number: '+t['f'][bad][0],[],[]
  $):
   v,$3,$>,ex=calc(t,$G,st['$8'])
   st['$8']=dict([(i,v[i])$- i in $>])
  drawform(t,st,v,$>,ex,msg or $3,bad is $] $# or $3[:2]in('no','to','va'))
  msg=''
  k=G['$i'](1)
  r=formkey(t,st,k,v,$>)
  if r=='back':
   $!
  if r:
   msg=r
$( unitname(t,st,i):
 f=t['f'][i]
 $! $0[f[1]][st['u'][i]][0]
$( formkey(t,st,k,v,$>):
 fs=t['f']
 n=$6(fs)
 i=st['$g']
 s=st['$j'][i]
 if k in('esc',)or k in MENU:
  $! 'back'
 if k=='up' or k in BACKTAB:
  st['$g']=(i-1)%n
 $2 k in('down','tab')or k in ENTER:
  st['$g']=(i+1)%n
 $2 k in('left','$c'):
  us=$0[fs[i][1]]
  if fs[i][4]or $6(us)<2:
   $! 'this field has one unit'
  old=st['u'][i]
  new=(old+(1 if k=='$c' $)-1))%$6(us)
  if s:
   $Q:
    st['$j'][i]=edtext(parse(s,fs[i][1],old),fs[i][1],new)
   $% $+:
    pass
  st['u'][i]=new
 $2 k in DELKEYS:
  st['$j'][i]=s[:-1]
 $2 k=='clear':
  st['$j'][i]=''
 $2 k in NEG:
  if s[-1:]=='E':
   st['$j'][i]=s+'-'
  $2 s[:1]=='-':
   st['$j'][i]=s[1:]
  $):
   st['$j'][i]='-'+s
 $2 k in('.',':')or($6(k)==1 $a '0'<=k<='9')or k in('E','ee','EE'):
  c='E' if k in('ee','EE')$) k
  if c==':' $a fs[i][1]!='$`':
   $! ': is only $- times (h:mm)'
  if t['one']:
   $- j in $&(n):
    if j!=i:
     st['$j'][j]=''
  if $6(s)<12:
   st['$j'][i]=s+c
 $2 k in('?','help','cat','catalog'):
  $@()
 $):
  $! '$i '+repr(k)[:20]+': $] used here'
 $! $#
$( drawform(t,st,v,$>,ex,$3,err):
 w=G['w']
 h=G['h']
 fs=t['f']
 n=$6(fs)
 $E=(h-2*LH-2)//RH
 total=n+$6(ex)
 $g=st['$g']
 $F=st['$F']
 if $g<$F:
  $F=$g
 if $g>=$F+$E:
  $F=$g-$E+1
 if $g==n-1:
  $F=max($F,min($g,total-$E))
 st['$F']=$F
 bars(t['$/'],$3)
 if err:
  box(0,h-LH,w,LH,C_ERR)
  $5(4,h-LH,$3[:(w-8)//AW],$^)
 xv=w-70
 y=LH+1
 $- j in $&($F,min(total,$F+$E)):
  if j<n:
   f=fs[j]
   if j==$g:
    box(0,y,w,RH,C_SEL)
   $5(6,y,f[0],$U)
   s=st['$j'][j]
   c=$U
   if s=='':
    if v[j]is $#:
     s,c='?',$:
    $):
     s=show(v[j],f[1],st['u'][j])
     c=C_RES if j in $> $) $:
   $5(xv-AW*$6(s),y,s,c)
   if j==$g:
    box(xv+1,y+2,2,RH-4,C_CUR)
   $5(xv+6,y,unitname(t,st,j),$:)
  $):
   lab,val=ex[j-n]
   $5(6,y,lab,$:)
   $5(w-6-AW*$6(val),y,val,C_RES)
  y+=RH
 if $F+$E<total:
  $5(w-12,y-RH,'v',$:)
 $[()
''')
_x(r'''HELP=(
 'Type the $D you know; blank',
 'fields (?) are solved as you type.',
 'up/down/tab/enter   next field',
 'left/$c   change the unit',
 'del  backspace    clear  blank field',
 '(-)  sign    esc/menu  tool list',
 'Blue = solved. Grey = default.',
 'Runway 27 = 270. Time 1:30 or 90.',
 'Variation: East +, West -.',
 'IAS is taken as CAS.',
 )
$( $@():
 bars('$P help','$M any $i')
 y=LH+1
 $- s in HELP:
  $5(6,y,s,$U)
  y+=RH
 $[()
 G['$i'](1)
$( keytest():
 $8=''
 $< $4:
  bars('Key test','esc twice to stop')
  $5(10,3*LH,'Last $i:',$:)
  $5(10,4*LH+4,repr($8),$U)
  $[()
  k=G['$i'](1)
  if k=='esc' $a $8=='esc':
   $!
  $8=k
$( textmode():
 all_=$X+$_
 $< $4:
  $N('')
  $- i in $&($6(all_)):
   $N('%2d %s%s'%(i+1,all_[i]['$/'],' (units)' if i>=$6($X)$) ''))
  s=input('tool number (q quits): ').strip()
  if s in('q','quit',''):
   $!
  $Q:
   t=all_[int(s)-1]
  $%($+,IndexError):
   $Z
  $G=[]
  $- f in t['f']:
   un=$0[f[1]][f[3]][0]
   $< $4:
    a=input('%s [%s]: '%(f[0],un)).strip()
    if a=='':
     $G.$*($#)
     $K
    $Q:
     $G.$*(parse(a,f[1],f[3]))
     $K
    $% $+:
     $N('$] a number')
  v,msg,$>,ex=calc(t,$G)
  $N('-- '+msg)
  $- i in $&($6(t['f'])):
   f=t['f'][i]
   if v[i]is $] $#:
    $N('%-17s %s %s%s'%(f[0],show(v[i],f[1],f[3]),
 $0[f[1]][f[3]][0],'  *' if i in $> $) ''))
  $- lab,val in ex:
   $N('%-17s %s'%(lab,val))
''')
del _x
navcalc()
