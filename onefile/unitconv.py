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
_W={'!': 'return', '#': 'ValueError', '%': 'except', '&': 'None', '(': 'ti_draw', ')': 'u00b3', '*': 'vals', '+': 'status', ',': 'while', '-': 'else', '.': 'len', '/': 'Square', '0': 'def', '1': 'ZeroDivisionError', '2': 'ev_unary', '3': 'u00b2', '4': 'elif', '5': 'ImportError', '6': 'text', '7': 'helpscreen', '8': 'title', '9': 'unitconv', ':': 'OverflowError', ';': 'and', '<': 'rows', '=': 'Exception', '>': 'Kilometre', '?': 'TypeError', '@': 'print', 'A': 'raise', 'B': 'top', 'C': 'convert', 'D': 'gallon', 'E': 'C_TXT', 'F': 'Imperial', 'G': 'Kilogram', 'H': 'Pound', 'I': 'continue', 'J': 'show_', 'K': 'split', 'L': 'start', 'M': 'True', 'N': 'rstrip', 'O': 'second', 'P': 'sel', 'Q': 'C_DIM', 'R': 'first', 'S': 'for', 'T': 'range', 'U': 'src', 'V': 'try', 'W': 'txt', 'X': 'u03c0', 'Y': 'value', 'Z': 'CATS', '[': 'key', ']': 'lab'}
_x(r'''import math
VERSION='1.0'
LH=18
RH=17
BASE=14
AW=7
UW=7
C_BAR=(30,60,130)
C_BART=(255,255,255)
$E=(0,0,0)
C_RES=(0,70,170)
C_ERR=(190,0,0)
C_SEL=(205,225,255)
$Q=(110,110,110)
C_CUR=(220,0,0)
C_WHITE=(255,255,255)
ENTER=('enter','ret','$!','center','\r','\n')
MENU=('menu',)
BACKTAB=('shift+tab','shift tab','shifttab','backtab','btab')
DELKEYS=('del','backspace','bksp')
KEYS='123456789abcdefghijklmnop'
MAXT=24
$Z=(
 ('Length','Nanometre|nm|1E-9;Micrometre|\u00b5m|1E-6;Millimetre|mm|0.001;'
 'Centimetre|cm|0.01;*Metre|m|1;$>|km|1000;Thou (mil)|thou|0.0000254;'
 'Inch|in|0.0254;Foot|ft|0.3048;Yard|yd|0.9144;Mile|mi|1609.344;'
 'Nautical mile|nmi|1852;Astronomical unit|au|149597870700;'
 'Light-year|ly|9460730472580800;Parsec|pc|3.0856775814913673E16'),
 ('Area','$/ millimetre|mm\$3|1E-6;$/ centimetre|cm\$3|1E-4;'
 '*$/ metre|m\$3|1;Hectare|ha|10000;$/ kilometre|km\$3|1E6;'
 '$/ inch|in\$3|0.00064516;$/ foot|ft\$3|0.09290304;'
 '$/ yard|yd\$3|0.83612736;Acre|acre|4046.8564224;'
 '$/ mile|mi\$3|2589988.110336'),
 ('Volume','Millilitre (cm\$))|mL|1E-6;*Litre|L|0.001;Cubic metre|m\$)|1;'
 'Cubic inch|in\$)|1.6387064E-5;Cubic foot|ft\$)|0.028316846592;'
 'Cubic yard|yd\$)|0.764554857984;US teaspoon|tsp|4.92892159375E-6;'
 'US tablespoon|tbsp|1.478676478125E-5;US fluid ounce|US floz|2.95735295625E-5;'
 'US cup|cup|2.365882365E-4;US pint|US pt|4.73176473E-4;'
 'US quart|US qt|9.46352946E-4;US $D|US gal|0.003785411784;'
 '$F fluid ounce|UK floz|2.84130625E-5;$F pint|UK pt|5.6826125E-4;'
 '$F $D|UK gal|0.00454609;Oil barrel|bbl|0.158987294928'),
 ('Mass','Milligram|mg|1E-6;Gram|g|0.001;*$G|kg|1;Tonne|t|1000;'
 'Carat|ct|0.0002;Grain|gr|0.00006479891;Ounce|oz|0.028349523125;'
 'Troy ounce|ozt|0.0311034768;$H|lb|0.45359237;Stone|st|6.35029318;'
 'Short ton (US)|US ton|907.18474;Long ton (UK)|UK ton|1016.0469088'),
 ('Temperature','*20*Celsius|\u00b0C|1|273.15;Fahrenheit|\u00b0F|5/9|459.67;'
 'Kelvin|K|1;Rankine|\u00b0R|5/9'),
 ('Time','Nanosecond|ns|1E-9;Microsecond|\u00b5s|1E-6;Millisecond|ms|0.001;'
 'Second|s|1;Minute|min|60;*Hour|h|3600;Day|d|86400;Week|wk|604800;'
 'Month (average)|mo|2629800;Year (365.25 d)|yr|31557600'),
 ('Speed','Metre/$O|m/s|1;*$>/hour|km/h|1/3.6;Mile/hour|mph|0.44704;'
 'Knot|kn|1852/3600;Foot/$O|ft/s|0.3048;Mach (sea level)|Mach|340.294;'
 'Speed of light|c|299792458'),
 ('Pressure','Pascal|Pa|1;Hectopascal|hPa|100;Kilopascal|kPa|1000;'
 'Megapascal|MPa|1E6;Millibar|mbar|100;*Bar|bar|1E5;Atmosphere|atm|101325;'
 '$H/sq inch|psi|4.4482216152605/0.00064516;mm of mercury|mmHg|133.322387415;'
 'Torr|Torr|101325/760;Inch of mercury|inHg|3386.38864;'
 'Inch of water|inH2O|249.08891'),
 ('Energy','Joule|J|1;*Kilojoule|kJ|1000;Megajoule|MJ|1E6;Calorie|cal|4.184;'
 'Kilocalorie (food)|kcal|4184;Watt hour|Wh|3600;Kilowatt hour|kWh|3.6E6;'
 'Electronvolt|eV|1.602176634E-19;British thermal u.|BTU|1055.05585262;'
 'Foot-pound|ft\u00b7lbf|1.3558179483314004;Therm (US)|thm|105480400'),
 ('Power','Watt|W|1;*Kilowatt|kW|1000;Megawatt|MW|1E6;'
 'Horsepower|hp|745.69987158227022;Metric horsepower|PS|735.49875;'
 'BTU/hour|BTU/h|1055.05585262/3600;Foot-pound/$O|ftlbf/s|1.3558179483314004;'
 'Kilocalorie/hour|kcal/h|4184/3600'),
 ('Force','*Newton|N|1;Kilonewton|kN|1000;Dyne|dyn|1E-5;'
 '$G-force|kgf|9.80665;$H-force|lbf|4.4482216152605;'
 'Ounce-force|ozf|0.27801385095378125'),
 ('Angle','*Degree|\u00b0|1;Radian|rad|180/pi;Milliradian|mrad|0.18/pi;'
 'Gradian|grad|0.9;Arcminute|arcmin|1/60;Arcsecond|arcsec|1/3600;'
 'Turn|turn|360'),
 ('Data size','Bit|bit|0.125;Kilobit|kbit|125;Megabit|Mbit|125000;'
 'Gigabit|Gbit|1.25E8;Byte|B|1;Kilobyte|kB|1000;*Megabyte|MB|1E6;'
 'Gigabyte|GB|1E9;Terabyte|TB|1E12;Kibibyte|KiB|1024;Mebibyte|MiB|1048576;'
 'Gibibyte|GiB|1073741824;Tebibyte|TiB|1099511627776'),
 ('Fuel economy','$>/litre|km/L|1;*7.5*Litres/100 km|L/100km|/100;'
 'Miles/$D (US)|mpg US|1.609344/3.785411784;'
 'Miles/$D (UK)|mpg UK|1.609344/4.54609'),
 ('Density','*$G/m\$)|kg/m\$)|1;Gram/cm\$) (kg/L)|g/cm\$)|1000;'
 '$H/ft\$)|lb/ft\$)|0.45359237/0.028316846592;'
 '$H/in\$)|lb/in\$)|0.45359237/1.6387064E-5;'
 '$H/US $D|lb/gal|0.45359237/0.003785411784'),
 ('Frequency','Hertz|Hz|1;Kilohertz|kHz|1000;Megahertz|MHz|1E6;'
 'Gigahertz|GHz|1E9;*Revolutions/min|rpm|1/60;Radian/$O|rad/s|0.5/pi'),
 )
ARITH=($#,$1,$:)
$0 num(s):
 if '/' in s:
  a,b=s.$K('/',1)
  $! num(a)/num(b)
 $! math.pi if s=='pi' $- float(s)
$0 units(c):
 out=[]
 $L=0
 $R='1'
 $S item in $Z[c][1].$K(';'):
  p=item.$K('|')
  $]=p[0]
  if $][:1]=='*':
   $L=$.(out)
   $]=$][1:]
   if '*' in $]:
    $R,$]=$].$K('*',1)
  f=p[2]
  inv=f[:1]=='/'
  out.append(($],p[1],num(f[1:]if inv $- f),
 num(p[3])if $.(p)>3 $- 0.0,inv))
 $! out,$L,$R
$0 tobase(x,u):
 if u[4]:
  $! u[2]/x
 $!(x+u[3])*u[2]
$0 frombase(b,u):
 if u[4]:
  $! u[2]/b
 $! b/u[2]-u[3]
$0 fmt(x,sig=8):
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
   s=s.$N('0').$N('.')
  if $.(s.lstrip('-'))>9 $; '.' not in s:
   s=''
 if not s:
  m,p=(('%.'+str(sig-1)+'e')%x).$K('e')
  if '.' in m:
   m=m.$N('0').$N('.')
  s=m+'E'+str(int(p))
 if s in('-0','-0.'):
  s='0'
 $! s
$0 parse(s):
 $! evalnum(s)
KEYCH={'.':'.','point':'.','decimal':'.','dot':'.','period':'.',
 '-':'-','\u2212':'-','minus':'-','+':'+','plus':'+',
 '*':'*','\u00d7':'*','times':'*','multiply':'*',
 '/':'/','\u00f7':'/','divide':'/','^':'^','power':'^',
 '(':'(',')':')','pi':'\$X','\$X':'\$X','E':'E','e':'E',
 'ee':'E','EE':'E','\u1d07':'E','square':'^2','\$3':'^2','x\$3':'^2'}
''')
_x(r'''$0 keych(k):
 if $.(k)==1 $; '0'<=k<='9':
  $! k
 $! KEYCH.get(k)
$0 evalnum(s):
 t=s.replace(' ','')
 $, t $; t[-1]in '+-*/^(E':
  t=t[:-1]
 if t in('','.'):
  $! $&
 t+=')'*max(0,t.count('(')-t.count(')'))
 p=[0]
 $V:
  v=ev_sum(t,p)
 $%($1,$:,$?):
  $A $#
 if p[0]!=$.(t)or v!=v or abs(v)>1e300:
  $A $#
 $! v
$0 ev_sum(t,p):
 v=ev_prod(t,p)
 $, p[0]<$.(t)$; t[p[0]]in '+-':
  op=t[p[0]]
  p[0]+=1
  w=ev_prod(t,p)
  v=v+w if op=='+' $- v-w
 $! v
$0 ev_prod(t,p):
 v=$2(t,p)
 $, p[0]<$.(t)$; t[p[0]]in '*/(\$X':
  op=t[p[0]]
  if op in '*/':
   p[0]+=1
  w=$2(t,p)
  v=v/w if op=='/' $- v*w
 $! v
$0 $2(t,p):
 if p[0]<$.(t)$; t[p[0]]in '+-':
  neg=t[p[0]]=='-'
  p[0]+=1
  v=$2(t,p)
  $!-v if neg $- v
 v=ev_atom(t,p)
 if p[0]<$.(t)$; t[p[0]]=='^':
  p[0]+=1
  e=$2(t,p)
  if v<0 $; e!=int(e):
   $A $#
  v=float(v)**e
 $! v
$0 ev_atom(t,p):
 i=p[0]
 if i<$.(t)$; t[i]=='(':
  p[0]+=1
  v=ev_sum(t,p)
  if p[0]>=$.(t)or t[p[0]]!=')':
   $A $#
  p[0]+=1
  $! v
 if i<$.(t)$; t[i]=='\$X':
  p[0]+=1
  $! math.pi
 j=i
 $, j<$.(t)$;(t[j].isdigit()or t[j]=='.'):
  j+=1
 if i<j<$.(t)$; t[j]=='E':
  k=j+1
  if k<$.(t)$; t[k]in '+-':
   k+=1
  if k<$.(t)$; t[k].isdigit():
   j=k
   $, j<$.(t)$; t[j].isdigit():
    j+=1
 if j==i:
  $A $#
 p[0]=j
 $! float(t[i:j])
NEGKEYS=('neg','(-)','\u207b','negative')
$0 negkey(s):
 if s=='' or s[-1]in '+-*/^(E':
  $! s+'-'
 if s[:2]=='-(' $; s[-1]==')':
  $! s[2:-1]
 if s[:1]=='-' $; evalnum(s[1:])is not $& $; not[c $S c in s[1:]if c in '+-*/^(']:
  $! s[1:]
 $S c in s:
  if c in '+-*/^(':
   $! '-('+s+')'
 $! '-'+s
$0 $C(us,$U,$W):
 $V:
  x=parse($W)
 $% $#:
  $![$&]*$.(us),'not a number',1
 if x is $&:
  $![$&]*$.(us),'type a $Y',0
 $V:
  b=tobase(x,us[$U])
 $% ARITH:
  $![$&]*$.(us),'no $Y $S '+$W+' '+us[$U][1],1
 $*=[]
 $S u in us:
  $V:
   $*.append(frombase(b,u))
  $% ARITH:
   $*.append($&)
 $*[$U]=x
 if b<-1e-9 $;[u $S u in us if u[3]]:
  $! $*,'below absolute zero',1
 $! $*,'',0
G={}
MEM={}
$0 $9():
 $[=findkey()
 $V:
  import $(
 $% $5:
  $(=$&
 if $[ is $& or $( is $&:
  $@('$9: no full-screen mode here (%s), $6 version.'
 %('no $[ function' if $[ is $& $- 'no $('))
  $! textmode()
 G['d']=$(
 G['$[']=$[
 G['cmode']=0
 $V:
  w,h=$(.get_screen_dim()
  w=int(w)
  h=int(h)
 $% $=:
  w,h=318,212
 G['w']=w
 G['h']=h
 $V:
  $(.use_buffer()
  G['buffer']=$M
 $% $=:
  G['buffer']=False
 $V:
  mainmenu()
 $% KeyboardInterrupt:
  pass
 $V:
  color(C_WHITE)
  $(.fill_rect(0,0,w,h)
  $J()
 $% $=:
  pass
$0 mainmenu():
 main=[c[0]$S c in $Z]+['Help','Key test']
 $, $M:
  a=choose('$9 '+VERSION+'   esc quits',main)
  if a is $&:
   $!
  if a<$.($Z):
   form(a)
  $4 main[a]=='Help':
   $7()
  $-:
   keytest()
KEYFN=('get_key','getkey','getKey','wait_key','waitkey')
$0 findkey():
 $S mn in('ti_system','$(','ti_plotlib'):
  $V:
   m=__import__(mn)
  $% $5:
   $I
  $S fn in KEYFN:
   f=getattr(m,fn,$&)
   if f is not $&:
    $! keyfun(f)
 $! $&
$0 keyfun(f):
 $V:
  from time import sleep
 $% $5:
  sleep=$&
 mode=[1]
 $0 wait(x=1):
  if mode[0]:
   $V:
    $! str(f(1))
   $% $?:
    mode[0]=0
  $, $M:
   k=f()
   if k:
    $! str(k)
   if sleep:
    sleep(0.02)
 $! wait
$0 color(c):
 d=G['d']
 if G['cmode']==0:
  $V:
   d.set_color(c[0],c[1],c[2])
   $!
  $% $?:
   G['cmode']=1
 d.set_color(c)
$0 $6(x,y,s,c):
 color(c)
 G['d'].draw_text(x,y+BASE,s)
$0 box(x,y,w,h,c):
 color(c)
 G['d'].fill_rect(x,y,w,h)
$0 $J():
 if G['buffer']:
  G['d'].paint_buffer()
$0 bars($8,$+,err=0):
 w=G['w']
 h=G['h']
 box(0,0,w,h,C_WHITE)
 box(0,0,w,LH,C_BAR)
 $6(4,0,$8,C_BART)
 box(0,h-LH,w,LH,C_ERR if err $- C_BAR)
 $6(4,h-LH,$+[:(w-8)//AW],C_BART)
$0 choose($8,labels):
 n=$.(labels)
 i=G.get('ch',{}).get($8,0)
 $<=(G['h']-2*LH-4)//LH
 $B=0
 $, $M:
  if i<$B:
   $B=i
  if i>=$B+$<:
   $B=i-$<+1
  bars($8,'enter or 1-9 a-p picks   esc back')
  y=LH+2
  $S j in $T($B,min(n,$B+$<)):
   if j==i:
    box(0,y,G['w'],LH,C_SEL)
   $6(8,y,KEYS[j]if j<$.(KEYS)$- ' ',$Q)
   $6(26,y,labels[j],$E)
   y+=LH
  if $B+$<<n:
   $6(G['w']-16,y-LH,'v',$Q)
  $J()
  k=G['$['](1)
  if k=='up':
   i=(i-1)%n
  $4 k=='down':
   i=(i+1)%n
  $4 k in ENTER or k=='right':
   break
  $4 k in('esc','left')or k in MENU:
   $! $&
  $4 $.(k)==1 $; k in KEYS[:n]:
   i=KEYS.index(k)
   break
 G.setdefault('ch',{})[$8]=i
 $! i
$0 form(c):
 us,$L,$R=units(c)
 st=MEM.get(c)
 if st is $&:
  st={'$U':$L,'$W':$R,'$P':$L,'$B':0}
  MEM[c]=st
 msg=''
 $, $M:
  $*,$+,err=$C(us,st['$U'],st['$W'])
  if msg:
   $+,err=msg,0
  $4 not $+:
   v=$*[st['$P']]
   $+='= '+('-' if v is $& $- fmt(v,12)+' '+us[st['$P']][1])
  drawform($Z[c][0],us,st,$*,$+,err)
  msg=formkey(us,st,G['$['](1),$*)
  if msg=='back':
   $!
''')
_x(r'''$0 formkey(us,st,k,$*):
 n=$.(us)
 i=st['$P']
 page=max(1,(G['h']-2*LH-2)//RH-1)
 if k=='esc' or k in MENU:
  $! 'back'
 if k=='up' or k in BACKTAB:
  st['$P']=(i-1)%n
 $4 k in('down','tab')or k in ENTER:
  st['$P']=(i+1)%n
 $4 k=='left':
  st['$P']=max(0,i-page)
 $4 k=='right':
  st['$P']=min(n-1,i+page)
 $4 k in DELKEYS:
  if i!=st['$U']:
   st['$U']=i
   st['$W']='' if $*[i]is $& $- fmt($*[i],12)
  st['$W']=st['$W'][:-1]
 $4 k=='clear':
  st['$U']=i
  st['$W']=''
 $4 k in NEGKEYS:
  s=st['$W']if i==st['$U']$- ''
  st['$U']=i
  st['$W']=negkey(s)
 $4 keych(k)is not $&:
  if i!=st['$U']:
   st['$U']=i
   st['$W']=''
  if $.(st['$W'])<MAXT:
   st['$W']+=keych(k)
 $4 k in('?','help','cat','catalog'):
  $7()
 $-:
  $! '$[ '+repr(k)[:20]+': not used here'
 $! $&
$0 drawform($8,us,st,$*,$+,err):
 w=G['w']
 h=G['h']
 n=$.(us)
 $<=(h-2*LH-2)//RH
 $P=st['$P']
 $B=st['$B']
 if $P<$B:
  $B=$P
 if $P>=$B+$<:
  $B=$P-$<+1
 $B=max(0,min($B,n-$<))
 st['$B']=$B
 bars('%s   %d/%d'%($8,$P+1,n),$+,err)
 xv=w-10-AW*UW
 y=LH+1
 $S j in $T($B,min(n,$B+$<)):
  u=us[j]
  if j==$P:
   box(0,y,w,RH,C_SEL)
  if j==st['$U']:
   s,c=st['$W'],$E
  $-:
   s='' if $*[j]is $& $- fmt($*[j])
   c=C_RES
  x=xv-AW*$.(s)
  $]=u[0]
  room=(x-14)//AW
  if $.($])>room:
   $]=$][:max(0,room-1)]+'.'
  $6(4,y,$],$E)
  $6(x,y,s,c)
  if j==st['$U']:
   box(xv+1,y+2,2,RH-4,C_CUR)
  $6(xv+6,y,u[1],$Q)
  y+=RH
 $J()
HELP=(
 'Pick a category, then type a $Y',
 'in any row: all $< $C.',
 'up/down/tab/enter   move',
 'left/right   page up/down',
 'del  backspace (edits a result)',
 'clear  empty row    EE  1.5E6',
 'Sums work: 5+3, 3/4, 2^10, 2(1+pi)',
 'esc/menu  back to the categories',
 'Black = typed, blue = converted.',
 'Status bar: the $Y, 12 digits.',
 )
$0 $7():
 bars('$9 help','press any $[')
 y=LH+1
 $S s in HELP:
  $6(6,y,s,$E)
  y+=RH
 $J()
 G['$['](1)
$0 keytest():
 last=''
 $, $M:
  bars('Key test','esc twice to stop')
  $6(10,3*LH,'Last $[:',$Q)
  $6(10,4*LH+4,repr(last),$E)
  $J()
  k=G['$['](1)
  if k=='esc' $; last=='esc':
   $!
  last=k
$0 textmode():
 $, $M:
  $@('')
  $S i in $T($.($Z)):
   $@('%2d %s'%(i+1,$Z[i][0]))
  s=input('category (q quits): ').strip()
  if s in('q','quit',''):
   $!
  $V:
   c=int(s)-1
   if c<0:
    $A IndexError
   us=units(c)[0]
  $%($#,IndexError):
   $I
  $, $M:
   $S i in $T($.(us)):
    $@('%2d %s (%s)'%(i+1,us[i][0],us[i][1]))
   s=input('unit number $; $Y (blank = back): ').strip().$K()
   if not s:
    break
   $V:
    j=int(s[0])-1
    if j<0 or j>=$.(us)or $.(s)!=2:
     $A $#
    $*,msg,err=$C(us,j,s[1])
   $% $#:
    $@('type e.g.  3 12.5')
    $I
   if msg:
    $@('-- '+msg)
   $S i in $T($.(us)):
    if $*[i]is not $&:
     $@('%-18s %s %s'%(us[i][0],fmt($*[i],10),us[i][1]))
''')
del _x
unitconv()
