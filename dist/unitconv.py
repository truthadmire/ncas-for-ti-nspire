import math
VERSION='1.0'
LH=18
RH=17
BASE=14
AW=7
UW=7
C_BAR=(30,60,130)
C_BART=(255,255,255)
C_TXT=(0,0,0)
C_RES=(0,70,170)
C_ERR=(190,0,0)
C_SEL=(205,225,255)
C_DIM=(110,110,110)
C_CUR=(220,0,0)
C_WHITE=(255,255,255)
ENTER=('enter','ret','return','center','\r','\n')
MENU=('menu',)
BACKTAB=('shift+tab','shift tab','shifttab','backtab','btab')
DELKEYS=('del','backspace','bksp')
KEYS='123456789abcdefghijklmnop'
MAXT=24
CATS=(
 ('Length','Nanometre|nm|1E-9;Micrometre|\u00b5m|1E-6;Millimetre|mm|0.001;'
 'Centimetre|cm|0.01;*Metre|m|1;Kilometre|km|1000;Thou (mil)|thou|0.0000254;'
 'Inch|in|0.0254;Foot|ft|0.3048;Yard|yd|0.9144;Mile|mi|1609.344;'
 'Nautical mile|nmi|1852;Astronomical unit|au|149597870700;'
 'Light-year|ly|9460730472580800;Parsec|pc|3.0856775814913673E16'),
 ('Area','Square millimetre|mm\u00b2|1E-6;Square centimetre|cm\u00b2|1E-4;'
 '*Square metre|m\u00b2|1;Hectare|ha|10000;Square kilometre|km\u00b2|1E6;'
 'Square inch|in\u00b2|0.00064516;Square foot|ft\u00b2|0.09290304;'
 'Square yard|yd\u00b2|0.83612736;Acre|acre|4046.8564224;'
 'Square mile|mi\u00b2|2589988.110336'),
 ('Volume','Millilitre (cm\u00b3)|mL|1E-6;*Litre|L|0.001;Cubic metre|m\u00b3|1;'
 'Cubic inch|in\u00b3|1.6387064E-5;Cubic foot|ft\u00b3|0.028316846592;'
 'Cubic yard|yd\u00b3|0.764554857984;US teaspoon|tsp|4.92892159375E-6;'
 'US tablespoon|tbsp|1.478676478125E-5;US fluid ounce|US floz|2.95735295625E-5;'
 'US cup|cup|2.365882365E-4;US pint|US pt|4.73176473E-4;'
 'US quart|US qt|9.46352946E-4;US gallon|US gal|0.003785411784;'
 'Imperial fluid ounce|UK floz|2.84130625E-5;Imperial pint|UK pt|5.6826125E-4;'
 'Imperial gallon|UK gal|0.00454609;Oil barrel|bbl|0.158987294928'),
 ('Mass','Milligram|mg|1E-6;Gram|g|0.001;*Kilogram|kg|1;Tonne|t|1000;'
 'Carat|ct|0.0002;Grain|gr|0.00006479891;Ounce|oz|0.028349523125;'
 'Troy ounce|ozt|0.0311034768;Pound|lb|0.45359237;Stone|st|6.35029318;'
 'Short ton (US)|US ton|907.18474;Long ton (UK)|UK ton|1016.0469088'),
 ('Temperature','*20*Celsius|\u00b0C|1|273.15;Fahrenheit|\u00b0F|5/9|459.67;'
 'Kelvin|K|1;Rankine|\u00b0R|5/9'),
 ('Time','Nanosecond|ns|1E-9;Microsecond|\u00b5s|1E-6;Millisecond|ms|0.001;'
 'Second|s|1;Minute|min|60;*Hour|h|3600;Day|d|86400;Week|wk|604800;'
 'Month (average)|mo|2629800;Year (365.25 d)|yr|31557600'),
 ('Speed','Metre/second|m/s|1;*Kilometre/hour|km/h|1/3.6;Mile/hour|mph|0.44704;'
 'Knot|kn|1852/3600;Foot/second|ft/s|0.3048;Mach (sea level)|Mach|340.294;'
 'Speed of light|c|299792458'),
 ('Pressure','Pascal|Pa|1;Hectopascal|hPa|100;Kilopascal|kPa|1000;'
 'Megapascal|MPa|1E6;Millibar|mbar|100;*Bar|bar|1E5;Atmosphere|atm|101325;'
 'Pound/sq inch|psi|4.4482216152605/0.00064516;mm of mercury|mmHg|133.322387415;'
 'Torr|Torr|101325/760;Inch of mercury|inHg|3386.38864;'
 'Inch of water|inH2O|249.08891'),
 ('Energy','Joule|J|1;*Kilojoule|kJ|1000;Megajoule|MJ|1E6;Calorie|cal|4.184;'
 'Kilocalorie (food)|kcal|4184;Watt hour|Wh|3600;Kilowatt hour|kWh|3.6E6;'
 'Electronvolt|eV|1.602176634E-19;British thermal u.|BTU|1055.05585262;'
 'Foot-pound|ft\u00b7lbf|1.3558179483314004;Therm (US)|thm|105480400'),
 ('Power','Watt|W|1;*Kilowatt|kW|1000;Megawatt|MW|1E6;'
 'Horsepower|hp|745.69987158227022;Metric horsepower|PS|735.49875;'
 'BTU/hour|BTU/h|1055.05585262/3600;Foot-pound/second|ftlbf/s|1.3558179483314004;'
 'Kilocalorie/hour|kcal/h|4184/3600'),
 ('Force','*Newton|N|1;Kilonewton|kN|1000;Dyne|dyn|1E-5;'
 'Kilogram-force|kgf|9.80665;Pound-force|lbf|4.4482216152605;'
 'Ounce-force|ozf|0.27801385095378125'),
 ('Angle','*Degree|\u00b0|1;Radian|rad|180/pi;Milliradian|mrad|0.18/pi;'
 'Gradian|grad|0.9;Arcminute|arcmin|1/60;Arcsecond|arcsec|1/3600;'
 'Turn|turn|360'),
 ('Data size','Bit|bit|0.125;Kilobit|kbit|125;Megabit|Mbit|125000;'
 'Gigabit|Gbit|1.25E8;Byte|B|1;Kilobyte|kB|1000;*Megabyte|MB|1E6;'
 'Gigabyte|GB|1E9;Terabyte|TB|1E12;Kibibyte|KiB|1024;Mebibyte|MiB|1048576;'
 'Gibibyte|GiB|1073741824;Tebibyte|TiB|1099511627776'),
 ('Fuel economy','Kilometre/litre|km/L|1;*7.5*Litres/100 km|L/100km|/100;'
 'Miles/gallon (US)|mpg US|1.609344/3.785411784;'
 'Miles/gallon (UK)|mpg UK|1.609344/4.54609'),
 ('Density','*Kilogram/m\u00b3|kg/m\u00b3|1;Gram/cm\u00b3 (kg/L)|g/cm\u00b3|1000;'
 'Pound/ft\u00b3|lb/ft\u00b3|0.45359237/0.028316846592;'
 'Pound/in\u00b3|lb/in\u00b3|0.45359237/1.6387064E-5;'
 'Pound/US gallon|lb/gal|0.45359237/0.003785411784'),
 ('Frequency','Hertz|Hz|1;Kilohertz|kHz|1000;Megahertz|MHz|1E6;'
 'Gigahertz|GHz|1E9;*Revolutions/min|rpm|1/60;Radian/second|rad/s|0.5/pi'),
 )
ARITH=(ValueError,ZeroDivisionError,OverflowError)
def num(s):
 if '/' in s:
  a,b=s.split('/',1)
  return num(a)/num(b)
 return math.pi if s=='pi' else float(s)
def units(c):
 out=[]
 start=0
 first='1'
 for item in CATS[c][1].split(';'):
  p=item.split('|')
  lab=p[0]
  if lab[:1]=='*':
   start=len(out)
   lab=lab[1:]
   if '*' in lab:
    first,lab=lab.split('*',1)
  f=p[2]
  inv=f[:1]=='/'
  out.append((lab,p[1],num(f[1:]if inv else f),
 num(p[3])if len(p)>3 else 0.0,inv))
 return out,start,first
def tobase(x,u):
 if u[4]:
  return u[2]/x
 return(x+u[3])*u[2]
def frombase(b,u):
 if u[4]:
  return u[2]/b
 return b/u[2]-u[3]
def fmt(x,sig=8):
 if x!=x:
  return 'undef'
 if x==0:
  return '0'
 a=abs(x)
 if a>1e308:
  return '-inf' if x<0 else 'inf'
 e=int(math.floor(math.log10(a)))
 s=''
 if-3<=e<9:
  s=('%.'+str(max(0,sig-1-e))+'f')%x
  if '.' in s:
   s=s.rstrip('0').rstrip('.')
  if len(s.lstrip('-'))>9 and '.' not in s:
   s=''
 if not s:
  m,p=(('%.'+str(sig-1)+'e')%x).split('e')
  if '.' in m:
   m=m.rstrip('0').rstrip('.')
  s=m+'E'+str(int(p))
 if s in('-0','-0.'):
  s='0'
 return s
def parse(s):
 return evalnum(s)
KEYCH={'.':'.','point':'.','decimal':'.','dot':'.','period':'.',
 '-':'-','\u2212':'-','minus':'-','+':'+','plus':'+',
 '*':'*','\u00d7':'*','times':'*','multiply':'*',
 '/':'/','\u00f7':'/','divide':'/','^':'^','power':'^',
 '(':'(',')':')','pi':'\u03c0','\u03c0':'\u03c0','E':'E','e':'E',
 'ee':'E','EE':'E','\u1d07':'E','square':'^2','\u00b2':'^2','x\u00b2':'^2'}
def keych(k):
 if len(k)==1 and '0'<=k<='9':
  return k
 return KEYCH.get(k)
def evalnum(s):
 t=s.replace(' ','')
 while t and t[-1]in '+-*/^(E':
  t=t[:-1]
 if t in('','.'):
  return None
 t+=')'*max(0,t.count('(')-t.count(')'))
 p=[0]
 try:
  v=ev_sum(t,p)
 except(ZeroDivisionError,OverflowError,TypeError):
  raise ValueError
 if p[0]!=len(t)or v!=v or abs(v)>1e300:
  raise ValueError
 return v
def ev_sum(t,p):
 v=ev_prod(t,p)
 while p[0]<len(t)and t[p[0]]in '+-':
  op=t[p[0]]
  p[0]+=1
  w=ev_prod(t,p)
  v=v+w if op=='+' else v-w
 return v
def ev_prod(t,p):
 v=ev_unary(t,p)
 while p[0]<len(t)and t[p[0]]in '*/(\u03c0':
  op=t[p[0]]
  if op in '*/':
   p[0]+=1
  w=ev_unary(t,p)
  v=v/w if op=='/' else v*w
 return v
def ev_unary(t,p):
 if p[0]<len(t)and t[p[0]]in '+-':
  neg=t[p[0]]=='-'
  p[0]+=1
  v=ev_unary(t,p)
  return-v if neg else v
 v=ev_atom(t,p)
 if p[0]<len(t)and t[p[0]]=='^':
  p[0]+=1
  e=ev_unary(t,p)
  if v<0 and e!=int(e):
   raise ValueError
  v=float(v)**e
 return v
def ev_atom(t,p):
 i=p[0]
 if i<len(t)and t[i]=='(':
  p[0]+=1
  v=ev_sum(t,p)
  if p[0]>=len(t)or t[p[0]]!=')':
   raise ValueError
  p[0]+=1
  return v
 if i<len(t)and t[i]=='\u03c0':
  p[0]+=1
  return math.pi
 j=i
 while j<len(t)and(t[j].isdigit()or t[j]=='.'):
  j+=1
 if i<j<len(t)and t[j]=='E':
  k=j+1
  if k<len(t)and t[k]in '+-':
   k+=1
  if k<len(t)and t[k].isdigit():
   j=k
   while j<len(t)and t[j].isdigit():
    j+=1
 if j==i:
  raise ValueError
 p[0]=j
 return float(t[i:j])
NEGKEYS=('neg','(-)','\u207b','negative')
def negkey(s):
 if s=='' or s[-1]in '+-*/^(E':
  return s+'-'
 if s[:2]=='-(' and s[-1]==')':
  return s[2:-1]
 if s[:1]=='-' and evalnum(s[1:])is not None and not[c for c in s[1:]if c in '+-*/^(']:
  return s[1:]
 for c in s:
  if c in '+-*/^(':
   return '-('+s+')'
 return '-'+s
def convert(us,src,txt):
 try:
  x=parse(txt)
 except ValueError:
  return[None]*len(us),'not a number',1
 if x is None:
  return[None]*len(us),'type a value',0
 try:
  b=tobase(x,us[src])
 except ARITH:
  return[None]*len(us),'no value for '+txt+' '+us[src][1],1
 vals=[]
 for u in us:
  try:
   vals.append(frombase(b,u))
  except ARITH:
   vals.append(None)
 vals[src]=x
 if b<-1e-9 and[u for u in us if u[3]]:
  return vals,'below absolute zero',1
 return vals,'',0
G={}
MEM={}
def unitconv():
 key=findkey()
 try:
  import ti_draw
 except ImportError:
  ti_draw=None
 if key is None or ti_draw is None:
  print('unitconv: no full-screen mode here (%s), text version.'
 %('no key function' if key is None else 'no ti_draw'))
  return textmode()
 G['d']=ti_draw
 G['key']=key
 G['cmode']=0
 try:
  w,h=ti_draw.get_screen_dim()
  w=int(w)
  h=int(h)
 except Exception:
  w,h=318,212
 G['w']=w
 G['h']=h
 try:
  ti_draw.use_buffer()
  G['buffer']=True
 except Exception:
  G['buffer']=False
 try:
  mainmenu()
 except KeyboardInterrupt:
  pass
 try:
  color(C_WHITE)
  ti_draw.fill_rect(0,0,w,h)
  show_()
 except Exception:
  pass
def mainmenu():
 main=[c[0]for c in CATS]+['Help','Key test']
 while True:
  a=choose('unitconv '+VERSION+'   esc quits',main)
  if a is None:
   return
  if a<len(CATS):
   form(a)
  elif main[a]=='Help':
   helpscreen()
  else:
   keytest()
KEYFN=('get_key','getkey','getKey','wait_key','waitkey')
def findkey():
 for mn in('ti_system','ti_draw','ti_plotlib'):
  try:
   m=__import__(mn)
  except ImportError:
   continue
  for fn in KEYFN:
   f=getattr(m,fn,None)
   if f is not None:
    return keyfun(f)
 return None
def keyfun(f):
 try:
  from time import sleep
 except ImportError:
  sleep=None
 mode=[1]
 def wait(x=1):
  if mode[0]:
   try:
    return str(f(1))
   except TypeError:
    mode[0]=0
  while True:
   k=f()
   if k:
    return str(k)
   if sleep:
    sleep(0.02)
 return wait
def color(c):
 d=G['d']
 if G['cmode']==0:
  try:
   d.set_color(c[0],c[1],c[2])
   return
  except TypeError:
   G['cmode']=1
 d.set_color(c)
def text(x,y,s,c):
 color(c)
 G['d'].draw_text(x,y+BASE,s)
def box(x,y,w,h,c):
 color(c)
 G['d'].fill_rect(x,y,w,h)
def show_():
 if G['buffer']:
  G['d'].paint_buffer()
def bars(title,status,err=0):
 w=G['w']
 h=G['h']
 box(0,0,w,h,C_WHITE)
 box(0,0,w,LH,C_BAR)
 text(4,0,title,C_BART)
 box(0,h-LH,w,LH,C_ERR if err else C_BAR)
 text(4,h-LH,status[:(w-8)//AW],C_BART)
def choose(title,labels):
 n=len(labels)
 i=G.get('ch',{}).get(title,0)
 rows=(G['h']-2*LH-4)//LH
 top=0
 while True:
  if i<top:
   top=i
  if i>=top+rows:
   top=i-rows+1
  bars(title,'enter or 1-9 a-p picks   esc back')
  y=LH+2
  for j in range(top,min(n,top+rows)):
   if j==i:
    box(0,y,G['w'],LH,C_SEL)
   text(8,y,KEYS[j]if j<len(KEYS)else ' ',C_DIM)
   text(26,y,labels[j],C_TXT)
   y+=LH
  if top+rows<n:
   text(G['w']-16,y-LH,'v',C_DIM)
  show_()
  k=G['key'](1)
  if k=='up':
   i=(i-1)%n
  elif k=='down':
   i=(i+1)%n
  elif k in ENTER or k=='right':
   break
  elif k in('esc','left')or k in MENU:
   return None
  elif len(k)==1 and k in KEYS[:n]:
   i=KEYS.index(k)
   break
 G.setdefault('ch',{})[title]=i
 return i
def form(c):
 us,start,first=units(c)
 st=MEM.get(c)
 if st is None:
  st={'src':start,'txt':first,'sel':start,'top':0}
  MEM[c]=st
 msg=''
 while True:
  vals,status,err=convert(us,st['src'],st['txt'])
  if msg:
   status,err=msg,0
  elif not status:
   v=vals[st['sel']]
   status='= '+('-' if v is None else fmt(v,12)+' '+us[st['sel']][1])
  drawform(CATS[c][0],us,st,vals,status,err)
  msg=formkey(us,st,G['key'](1),vals)
  if msg=='back':
   return
def formkey(us,st,k,vals):
 n=len(us)
 i=st['sel']
 page=max(1,(G['h']-2*LH-2)//RH-1)
 if k=='esc' or k in MENU:
  return 'back'
 if k=='up' or k in BACKTAB:
  st['sel']=(i-1)%n
 elif k in('down','tab')or k in ENTER:
  st['sel']=(i+1)%n
 elif k=='left':
  st['sel']=max(0,i-page)
 elif k=='right':
  st['sel']=min(n-1,i+page)
 elif k in DELKEYS:
  if i!=st['src']:
   st['src']=i
   st['txt']='' if vals[i]is None else fmt(vals[i],12)
  st['txt']=st['txt'][:-1]
 elif k=='clear':
  st['src']=i
  st['txt']=''
 elif k in NEGKEYS:
  s=st['txt']if i==st['src']else ''
  st['src']=i
  st['txt']=negkey(s)
 elif keych(k)is not None:
  if i!=st['src']:
   st['src']=i
   st['txt']=''
  if len(st['txt'])<MAXT:
   st['txt']+=keych(k)
 elif k in('?','help','cat','catalog'):
  helpscreen()
 else:
  return 'key '+repr(k)[:20]+': not used here'
 return None
def drawform(title,us,st,vals,status,err):
 w=G['w']
 h=G['h']
 n=len(us)
 rows=(h-2*LH-2)//RH
 sel=st['sel']
 top=st['top']
 if sel<top:
  top=sel
 if sel>=top+rows:
  top=sel-rows+1
 top=max(0,min(top,n-rows))
 st['top']=top
 bars('%s   %d/%d'%(title,sel+1,n),status,err)
 xv=w-10-AW*UW
 y=LH+1
 for j in range(top,min(n,top+rows)):
  u=us[j]
  if j==sel:
   box(0,y,w,RH,C_SEL)
  if j==st['src']:
   s,c=st['txt'],C_TXT
  else:
   s='' if vals[j]is None else fmt(vals[j])
   c=C_RES
  x=xv-AW*len(s)
  lab=u[0]
  room=(x-14)//AW
  if len(lab)>room:
   lab=lab[:max(0,room-1)]+'.'
  text(4,y,lab,C_TXT)
  text(x,y,s,c)
  if j==st['src']:
   box(xv+1,y+2,2,RH-4,C_CUR)
  text(xv+6,y,u[1],C_DIM)
  y+=RH
 show_()
HELP=(
 'Pick a category, then type a value',
 'in any row: all rows convert.',
 'up/down/tab/enter   move',
 'left/right   page up/down',
 'del  backspace (edits a result)',
 'clear  empty row    EE  1.5E6',
 'Sums work: 5+3, 3/4, 2^10, 2(1+pi)',
 'esc/menu  back to the categories',
 'Black = typed, blue = converted.',
 'Status bar: the value, 12 digits.',
 )
def helpscreen():
 bars('unitconv help','press any key')
 y=LH+1
 for s in HELP:
  text(6,y,s,C_TXT)
  y+=RH
 show_()
 G['key'](1)
def keytest():
 last=''
 while True:
  bars('Key test','esc twice to stop')
  text(10,3*LH,'Last key:',C_DIM)
  text(10,4*LH+4,repr(last),C_TXT)
  show_()
  k=G['key'](1)
  if k=='esc' and last=='esc':
   return
  last=k
def textmode():
 while True:
  print('')
  for i in range(len(CATS)):
   print('%2d %s'%(i+1,CATS[i][0]))
  s=input('category (q quits): ').strip()
  if s in('q','quit',''):
   return
  try:
   c=int(s)-1
   if c<0:
    raise IndexError
   us=units(c)[0]
  except(ValueError,IndexError):
   continue
  while True:
   for i in range(len(us)):
    print('%2d %s (%s)'%(i+1,us[i][0],us[i][1]))
   s=input('unit number and value (blank = back): ').strip().split()
   if not s:
    break
   try:
    j=int(s[0])-1
    if j<0 or j>=len(us)or len(s)!=2:
     raise ValueError
    vals,msg,err=convert(us,j,s[1])
   except ValueError:
    print('type e.g.  3 12.5')
    continue
   if msg:
    print('-- '+msg)
   for i in range(len(us)):
    if vals[i]is not None:
     print('%-18s %s %s'%(us[i][0],fmt(vals[i],10),us[i][1]))
if __name__=='__main__':
 unitconv()
