# unitconv - unit converter for TI-Nspire CX II. Run it (ctrl+R): pick a category, esc quits.
# The program is kept below as text and compiled one part at a time, which needs
# much less memory than compiling everything at once. Do not edit the text parts.
try:
 import gc
except ImportError:
 gc = None
try:
 exec
except NameError:
 print('exec() is missing: paste src/unitconv.py instead')
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
print('Loading unitconv...')
_W={'!': 'return', '#': 'except', '%': 'ti_draw', '&': 'None', '(': 'ValueError', ')': 'u00b3', '*': 'vals', '+': 'status', ',': 'Square', '-': 'else', '.': 'elif', '/': 'ImportError', '0': 'text', '1': 'def', '2': 'helpscreen', '3': 'title', '4': 'u00b2', '5': 'unitconv', '6': 'while', '7': 'rows', '8': 'Exception', '9': 'Kilometre', ':': 'len', ';': 'print', '<': 'top', '=': 'convert', '>': 'gallon', '?': 'C_TXT', '@': 'Imperial', 'A': 'Kilogram', 'B': 'Pound', 'C': 'continue', 'D': 'show_', 'E': 'split', 'F': 'start', 'G': 'txt', 'H': 'True', 'I': 'rstrip', 'J': 'second', 'K': 'sel', 'L': 'C_DIM', 'M': 'first', 'N': 'range', 'O': 'src', 'P': 'value', 'Q': 'CATS', 'R': 'try', 'S': 'for', 'T': 'key', 'U': 'lab'}
_x(r'''import math
VERSION='1.0'
LH=18
RH=17
BASE=14
AW=7
UW=7
C_BAR=(30,60,130)
C_BART=(255,255,255)
$?=(0,0,0)
C_RES=(0,70,170)
C_ERR=(190,0,0)
C_SEL=(205,225,255)
$L=(110,110,110)
C_CUR=(220,0,0)
C_WHITE=(255,255,255)
ENTER=('enter','ret','$!','center','\r','\n')
MENU=('menu',)
BACKTAB=('shift+tab','shift tab','shifttab','backtab','btab')
DELKEYS=('del','backspace','bksp')
NEG=('-','neg','(-)','\u2212','\u207b')
KEYS='123456789abcdefghijklmnop'
$Q=(
 ('Length','Nanometre|nm|1E-9;Micrometre|\u00b5m|1E-6;Millimetre|mm|0.001;'
 'Centimetre|cm|0.01;*Metre|m|1;$9|km|1000;Thou (mil)|thou|0.0000254;'
 'Inch|in|0.0254;Foot|ft|0.3048;Yard|yd|0.9144;Mile|mi|1609.344;'
 'Nautical mile|nmi|1852;Astronomical unit|au|149597870700;'
 'Light-year|ly|9460730472580800;Parsec|pc|3.0856775814913673E16'),
 ('Area','$, millimetre|mm\$4|1E-6;$, centimetre|cm\$4|1E-4;'
 '*$, metre|m\$4|1;Hectare|ha|10000;$, kilometre|km\$4|1E6;'
 '$, inch|in\$4|0.00064516;$, foot|ft\$4|0.09290304;'
 '$, yard|yd\$4|0.83612736;Acre|acre|4046.8564224;'
 '$, mile|mi\$4|2589988.110336'),
 ('Volume','Millilitre (cm\$))|mL|1E-6;*Litre|L|0.001;Cubic metre|m\$)|1;'
 'Cubic inch|in\$)|1.6387064E-5;Cubic foot|ft\$)|0.028316846592;'
 'Cubic yard|yd\$)|0.764554857984;US teaspoon|tsp|4.92892159375E-6;'
 'US tablespoon|tbsp|1.478676478125E-5;US fluid ounce|US floz|2.95735295625E-5;'
 'US cup|cup|2.365882365E-4;US pint|US pt|4.73176473E-4;'
 'US quart|US qt|9.46352946E-4;US $>|US gal|0.003785411784;'
 '$@ fluid ounce|UK floz|2.84130625E-5;$@ pint|UK pt|5.6826125E-4;'
 '$@ $>|UK gal|0.00454609;Oil barrel|bbl|0.158987294928'),
 ('Mass','Milligram|mg|1E-6;Gram|g|0.001;*$A|kg|1;Tonne|t|1000;'
 'Carat|ct|0.0002;Grain|gr|0.00006479891;Ounce|oz|0.028349523125;'
 'Troy ounce|ozt|0.0311034768;$B|lb|0.45359237;Stone|st|6.35029318;'
 'Short ton (US)|US ton|907.18474;Long ton (UK)|UK ton|1016.0469088'),
 ('Temperature','*20*Celsius|\u00b0C|1|273.15;Fahrenheit|\u00b0F|5/9|459.67;'
 'Kelvin|K|1;Rankine|\u00b0R|5/9'),
 ('Time','Nanosecond|ns|1E-9;Microsecond|\u00b5s|1E-6;Millisecond|ms|0.001;'
 'Second|s|1;Minute|min|60;*Hour|h|3600;Day|d|86400;Week|wk|604800;'
 'Month (average)|mo|2629800;Year (365.25 d)|yr|31557600'),
 ('Speed','Metre/$J|m/s|1;*$9/hour|km/h|1/3.6;Mile/hour|mph|0.44704;'
 'Knot|kn|1852/3600;Foot/$J|ft/s|0.3048;Mach (sea level)|Mach|340.294;'
 'Speed of light|c|299792458'),
 ('Pressure','Pascal|Pa|1;Hectopascal|hPa|100;Kilopascal|kPa|1000;'
 'Megapascal|MPa|1E6;Millibar|mbar|100;*Bar|bar|1E5;Atmosphere|atm|101325;'
 '$B/sq inch|psi|4.4482216152605/0.00064516;mm of mercury|mmHg|133.322387415;'
 'Torr|Torr|101325/760;Inch of mercury|inHg|3386.38864;'
 'Inch of water|inH2O|249.08891'),
 ('Energy','Joule|J|1;*Kilojoule|kJ|1000;Megajoule|MJ|1E6;Calorie|cal|4.184;'
 'Kilocalorie (food)|kcal|4184;Watt hour|Wh|3600;Kilowatt hour|kWh|3.6E6;'
 'Electronvolt|eV|1.602176634E-19;British thermal u.|BTU|1055.05585262;'
 'Foot-pound|ft\u00b7lbf|1.3558179483314004;Therm (US)|thm|105480400'),
 ('Power','Watt|W|1;*Kilowatt|kW|1000;Megawatt|MW|1E6;'
 'Horsepower|hp|745.69987158227022;Metric horsepower|PS|735.49875;'
 'BTU/hour|BTU/h|1055.05585262/3600;Foot-pound/$J|ftlbf/s|1.3558179483314004;'
 'Kilocalorie/hour|kcal/h|4184/3600'),
 ('Force','*Newton|N|1;Kilonewton|kN|1000;Dyne|dyn|1E-5;'
 '$A-force|kgf|9.80665;$B-force|lbf|4.4482216152605;'
 'Ounce-force|ozf|0.27801385095378125'),
 ('Angle','*Degree|\u00b0|1;Radian|rad|180/pi;Milliradian|mrad|0.18/pi;'
 'Gradian|grad|0.9;Arcminute|arcmin|1/60;Arcsecond|arcsec|1/3600;'
 'Turn|turn|360'),
 ('Data size','Bit|bit|0.125;Kilobit|kbit|125;Megabit|Mbit|125000;'
 'Gigabit|Gbit|1.25E8;Byte|B|1;Kilobyte|kB|1000;*Megabyte|MB|1E6;'
 'Gigabyte|GB|1E9;Terabyte|TB|1E12;Kibibyte|KiB|1024;Mebibyte|MiB|1048576;'
 'Gibibyte|GiB|1073741824;Tebibyte|TiB|1099511627776'),
 ('Fuel economy','$9/litre|km/L|1;*7.5*Litres/100 km|L/100km|/100;'
 'Miles/$> (US)|mpg US|1.609344/3.785411784;'
 'Miles/$> (UK)|mpg UK|1.609344/4.54609'),
 ('Density','*$A/m\$)|kg/m\$)|1;Gram/cm\$) (kg/L)|g/cm\$)|1000;'
 '$B/ft\$)|lb/ft\$)|0.45359237/0.028316846592;'
 '$B/in\$)|lb/in\$)|0.45359237/1.6387064E-5;'
 '$B/US $>|lb/gal|0.45359237/0.003785411784'),
 ('Frequency','Hertz|Hz|1;Kilohertz|kHz|1000;Megahertz|MHz|1E6;'
 'Gigahertz|GHz|1E9;*Revolutions/min|rpm|1/60;Radian/$J|rad/s|0.5/pi'),
 )
ARITH=($(,ZeroDivisionError,OverflowError)
$1 num(s):
 if '/' in s:
  a,b=s.$E('/',1)
  $! num(a)/num(b)
 $! math.pi if s=='pi' $- float(s)
$1 units(c):
 out=[]
 $F=0
 $M='1'
 $S item in $Q[c][1].$E(';'):
  p=item.$E('|')
  $U=p[0]
  if $U[:1]=='*':
   $F=$:(out)
   $U=$U[1:]
   if '*' in $U:
    $M,$U=$U.$E('*',1)
  f=p[2]
  inv=f[:1]=='/'
  out.append(($U,p[1],num(f[1:]if inv $- f),
 num(p[3])if $:(p)>3 $- 0.0,inv))
 $! out,$F,$M
$1 tobase(x,u):
 if u[4]:
  $! u[2]/x
 $!(x+u[3])*u[2]
$1 frombase(b,u):
 if u[4]:
  $! u[2]/b
 $! b/u[2]-u[3]
$1 fmt(x,sig=8):
 if x!=x:
  $! 'undef'
 if x==0:
  $! '0'
 a=abs(x)
 if a>1e308:
  $! '-inf' if x<0 $- 'inf'
 e=int(math.floor(math.log10(a)))
 s=''
 if-3<=e<9:
  s=('%.'+str(max(0,sig-1-e))+'f')%x
  if '.' in s:
   s=s.$I('0').$I('.')
  if $:(s.lstrip('-'))>9 and '.' not in s:
   s=''
 if not s:
  m,p=(('%.'+str(sig-1)+'e')%x).$E('e')
  if '.' in m:
   m=m.$I('0').$I('.')
  s=m+'E'+str(int(p))
 if s in('-0','-0.'):
  s='0'
 $! s
$1 parse(s):
 t=s
 $6 t[-1:]in('E','-'):
  t=t[:-1]
 if t in('','.','-.'):
  $! $&
 $! float(t)
''')
_x(r'''$1 $=(us,$O,$G):
 $R:
  x=parse($G)
 $# $(:
  $![$&]*$:(us),'not a number',1
 if x is $&:
  $![$&]*$:(us),'type a $P',0
 $R:
  b=tobase(x,us[$O])
 $# ARITH:
  $![$&]*$:(us),'no $P $S '+$G+' '+us[$O][1],1
 $*=[]
 $S u in us:
  $R:
   $*.append(frombase(b,u))
  $# ARITH:
   $*.append($&)
 $*[$O]=x
 if b<-1e-9 and[u $S u in us if u[3]]:
  $! $*,'below absolute zero',1
 $! $*,'',0
G={}
MEM={}
$1 $5():
 $T=findkey()
 $R:
  import $%
 $# $/:
  $%=$&
 if $T is $& or $% is $&:
  $;('$5: no full-screen mode here (%s), $0 version.'
 %('no $T function' if $T is $& $- 'no $%'))
  $! textmode()
 G['d']=$%
 G['$T']=$T
 G['cmode']=0
 $R:
  w,h=$%.get_screen_dim()
  w=int(w)
  h=int(h)
 $# $8:
  w,h=318,212
 G['w']=w
 G['h']=h
 $R:
  $%.use_buffer()
  G['buffer']=$H
 $# $8:
  G['buffer']=False
 $R:
  mainmenu()
 $# KeyboardInterrupt:
  pass
 $R:
  color(C_WHITE)
  $%.fill_rect(0,0,w,h)
  $D()
 $# $8:
  pass
$1 mainmenu():
 main=[c[0]$S c in $Q]+['Help','Key test']
 $6 $H:
  a=choose('$5 '+VERSION+'   esc quits',main)
  if a is $&:
   $!
  if a<$:($Q):
   form(a)
  $. main[a]=='Help':
   $2()
  $-:
   keytest()
KEYFN=('get_key','getkey','getKey','wait_key','waitkey')
$1 findkey():
 $S mn in('ti_system','$%','ti_plotlib'):
  $R:
   m=__import__(mn)
  $# $/:
   $C
  $S fn in KEYFN:
   f=getattr(m,fn,$&)
   if f is not $&:
    $! keyfun(f)
 $! $&
$1 keyfun(f):
 $R:
  from time import sleep
 $# $/:
  sleep=$&
 mode=[1]
 $1 wait(x=1):
  if mode[0]:
   $R:
    $! str(f(1))
   $# TypeError:
    mode[0]=0
  $6 $H:
   k=f()
   if k:
    $! str(k)
   if sleep:
    sleep(0.02)
 $! wait
$1 color(c):
 d=G['d']
 if G['cmode']==0:
  $R:
   d.set_color(c[0],c[1],c[2])
   $!
  $# TypeError:
   G['cmode']=1
 d.set_color(c)
$1 $0(x,y,s,c):
 color(c)
 G['d'].draw_text(x,y+BASE,s)
$1 box(x,y,w,h,c):
 color(c)
 G['d'].fill_rect(x,y,w,h)
$1 $D():
 if G['buffer']:
  G['d'].paint_buffer()
$1 bars($3,$+,err=0):
 w=G['w']
 h=G['h']
 box(0,0,w,h,C_WHITE)
 box(0,0,w,LH,C_BAR)
 $0(4,0,$3,C_BART)
 box(0,h-LH,w,LH,C_ERR if err $- C_BAR)
 $0(4,h-LH,$+[:(w-8)//AW],C_BART)
$1 choose($3,labels):
 n=$:(labels)
 i=G.get('ch',{}).get($3,0)
 $7=(G['h']-2*LH-4)//LH
 $<=0
 $6 $H:
  if i<$<:
   $<=i
  if i>=$<+$7:
   $<=i-$7+1
  bars($3,'enter or 1-9 a-p picks   esc back')
  y=LH+2
  $S j in $N($<,min(n,$<+$7)):
   if j==i:
    box(0,y,G['w'],LH,C_SEL)
   $0(8,y,KEYS[j]if j<$:(KEYS)$- ' ',$L)
   $0(26,y,labels[j],$?)
   y+=LH
  if $<+$7<n:
   $0(G['w']-16,y-LH,'v',$L)
  $D()
  k=G['$T'](1)
  if k=='up':
   i=(i-1)%n
  $. k=='down':
   i=(i+1)%n
  $. k in ENTER or k=='right':
   break
  $. k in('esc','left')or k in MENU:
   $! $&
  $. $:(k)==1 and k in KEYS[:n]:
   i=KEYS.index(k)
   break
 G.setdefault('ch',{})[$3]=i
 $! i
$1 form(c):
 us,$F,$M=units(c)
 st=MEM.get(c)
 if st is $&:
  st={'$O':$F,'$G':$M,'$K':$F,'$<':0}
  MEM[c]=st
 msg=''
 $6 $H:
  $*,$+,err=$=(us,st['$O'],st['$G'])
  if msg:
   $+,err=msg,0
  $. not $+:
   v=$*[st['$K']]
   $+='= '+('-' if v is $& $- fmt(v,12)+' '+us[st['$K']][1])
  drawform($Q[c][0],us,st,$*,$+,err)
  msg=formkey(us,st,G['$T'](1),$*)
  if msg=='back':
   $!
$1 formkey(us,st,k,$*):
 n=$:(us)
 i=st['$K']
 page=max(1,(G['h']-2*LH-2)//RH-1)
 if k=='esc' or k in MENU:
  $! 'back'
 if k=='up' or k in BACKTAB:
  st['$K']=(i-1)%n
 $. k in('down','tab')or k in ENTER:
  st['$K']=(i+1)%n
 $. k=='left':
  st['$K']=max(0,i-page)
 $. k=='right':
  st['$K']=min(n-1,i+page)
 $. k in DELKEYS:
  if i!=st['$O']:
   st['$O']=i
   st['$G']='' if $*[i]is $& $- fmt($*[i],12)
  st['$G']=st['$G'][:-1]
 $. k=='clear':
  st['$O']=i
  st['$G']=''
 $. k in NEG:
  s=st['$G']if i==st['$O']$- ''
  st['$O']=i
  if s[-1:]=='E':
   st['$G']=s+'-'
  $. s[:1]=='-':
   st['$G']=s[1:]
  $-:
   st['$G']='-'+s
 $. k=='.' or($:(k)==1 and '0'<=k<='9')or k in('E','ee','EE'):
  if i!=st['$O']:
   st['$O']=i
   st['$G']=''
  if $:(st['$G'])<14:
   st['$G']+='E' if k in('ee','EE')$- k
 $. k in('?','help','cat','catalog'):
  $2()
 $-:
  $! '$T '+repr(k)[:20]+': not used here'
 $! $&
$1 drawform($3,us,st,$*,$+,err):
 w=G['w']
 h=G['h']
 n=$:(us)
 $7=(h-2*LH-2)//RH
 $K=st['$K']
 $<=st['$<']
 if $K<$<:
  $<=$K
 if $K>=$<+$7:
  $<=$K-$7+1
 $<=max(0,min($<,n-$7))
 st['$<']=$<
 bars('%s   %d/%d'%($3,$K+1,n),$+,err)
 xv=w-10-AW*UW
 y=LH+1
 $S j in $N($<,min(n,$<+$7)):
  u=us[j]
  if j==$K:
   box(0,y,w,RH,C_SEL)
  if j==st['$O']:
   s,c=st['$G'],$?
  $-:
   s='' if $*[j]is $& $- fmt($*[j])
   c=C_RES
  x=xv-AW*$:(s)
  $U=u[0]
  room=(x-14)//AW
  if $:($U)>room:
   $U=$U[:max(0,room-1)]+'.'
  $0(4,y,$U,$?)
  $0(x,y,s,c)
  if j==st['$O']:
   box(xv+1,y+2,2,RH-4,C_CUR)
  $0(xv+6,y,u[1],$L)
  y+=RH
 $D()
HELP=(
 'Pick a category, then type a $P',
 'in any row: all $7 $=.',
 'up/down/tab/enter   move',
 'left/right   page up/down',
 'del  backspace (edits a result)',
 'clear  empty row    (-)  sign',
 'EE  exponent: 1.5E6 = 1500000',
 'esc/menu  back to the categories',
 'Black = typed, blue = converted.',
 'Status bar: the $P, 12 digits.',
 )
$1 $2():
 bars('$5 help','press any $T')
 y=LH+1
 $S s in HELP:
  $0(6,y,s,$?)
  y+=RH
 $D()
 G['$T'](1)
''')
_x(r'''$1 keytest():
 last=''
 $6 $H:
  bars('Key test','esc twice to stop')
  $0(10,3*LH,'Last $T:',$L)
  $0(10,4*LH+4,repr(last),$?)
  $D()
  k=G['$T'](1)
  if k=='esc' and last=='esc':
   $!
  last=k
$1 textmode():
 $6 $H:
  $;('')
  $S i in $N($:($Q)):
   $;('%2d %s'%(i+1,$Q[i][0]))
  s=input('category (q quits): ').strip()
  if s in('q','quit',''):
   $!
  $R:
   c=int(s)-1
   if c<0:
    raise IndexError
   us=units(c)[0]
  $#($(,IndexError):
   $C
  $6 $H:
   $S i in $N($:(us)):
    $;('%2d %s (%s)'%(i+1,us[i][0],us[i][1]))
   s=input('unit number and $P (blank = back): ').strip().$E()
   if not s:
    break
   $R:
    j=int(s[0])-1
    if j<0 or j>=$:(us)or $:(s)!=2:
     raise $(
    $*,msg,err=$=(us,j,s[1])
   $# $(:
    $;('type e.g.  3 12.5')
    $C
   if msg:
    $;('-- '+msg)
   $S i in $N($:(us)):
    if $*[i]is not $&:
     $;('%-18s %s %s'%(us[i][0],fmt($*[i],10),us[i][1]))
''')
del _x
unitconv()
