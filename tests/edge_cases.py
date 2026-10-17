import sys
sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else 'src')
import cas
from cascore import CASError
CASES = """
solve(x^2=4)
d(x^2)
factor()
[[1,2][3]]
1/0
0/0
ln(0)
tan(π/2)
x/0
inf-inf
undef+1
{1,2}+{1,2,3}
det([[1,2,3]])
sqrt(x)^2
(-8)^(1/3)
2^(1/2)*2^(1/3)
e^(i*π)
log(8,2)
log10(1000)
log(e^2)
ln(-1)
:complex
ln(-1)
sqrt(-4)
i^i
:real
atan2(1,1)
asin(1)
1.5E3
2e3
abs(x)^2
sqrt(x^2)
x^0
0^0
(x^2)^(1/2)
(x^3)^(1/3)
10^-2
-2^2
(-2)^2
2^3^2
3!!
50!
nCr(50,25)
1/3+0.5
√2*1.0
solve(x^2=2.0,x)
x+
sin(
foo(3)
f(x):=x+1
f(f(2))
:deg
sin(30)
cos(60)
arcsin(1)
solve(sin(x)=1/2,x)
:rad
:approx
1/3
π
:auto
expand((x+y+z)^4)
factor(x^10-1)
solve(x^6-1=0,x)
integral(x^3*cos(x^2),x)
integral(1/(x^3+1),x)
integral(tan(x)^3,x)
integral(e^x*cos(2x),x)
integral(1/(x*sqrt(x^2-1)),x)
integral(sin(x)^4*cos(x)^3,x)
integral(x/(x^4+1),x)
integral(ln(x)^2,x)
integral(1/(1+e^x),x)
limit(x^(1/x),x,inf)
limit((sin(x)-x)/x^3,x,0)
limit(x*sin(1/x),x,0)
limit(sin(x),x,inf)
limit((2^x-1)/x,x,0)
limit(n!/n^n,n,inf)
taylor(1/cos(x),x,6)
taylor(arctan(x),x,7)
series(sqrt(1+x),x,3)
solve(x^3-3x+1=0,x)
solve(2^x=3^(x-1),x)
solve(ln(x)+ln(x-1)=ln(6),x)
solve(sqrt(x)+sqrt(x-5)=5,x)
solve(x/(x-1)=2/(x-1),x)
solve(cos(2x)=sin(x),x)
solve(x^4+x^2-6=0,x)
cSolve(x^3=-8,x)
solve(x^2+y^2=4 and x*y=1,{x,y})
solve(x+2y+3z=6 and 2x-y+z=2 and x+y-z=1,{x,y,z})
deSolve(y'=-y/x,x,y)
deSolve(y''-4y'+4y=x,x,y)
deSolve(y'=y*(1-y),x,y)
deSolve(y'+2x*y=x,x,y)
eigVl([[1,2][2,1]])
eigVc([[1,2][2,1]])
[[1,2][3,4]]^2
[[a,b][c,d]]^-1
rref([[1,2,3][2,4,6]])
det(identity(4))
dim([[1,2,3][4,5,6]])
[[1,2][3,4]].*[[1,2][3,4]]
{1,2,3}^2
sum(seq(1/k,k,1,10))
mean({a,b,c})
expr("2+3")
string(x^2)
"ab"&"cd"
dim("hello")
{1,2,3}[2]
[[1,2][3,4]][2,1]
a:=3
b:=a+1
b
delvar a
b
a
:vars
:clear
q
(x^2-1)/(x-1)
integral(sec(x)^3,x)
integral(sec(x)^3,x,0,pi/4)
integral(csc(x)^3,x)
integral(sec(x)^4,x)
derivative(integral(sec(x)^6,x),x)|x=1
impDif(y^3-x y=2,x,y)
solve(r*(p+q)/(p*q)<5,r)
solve(a*x<5,x)
solve(k*x<=k,x)
solve(a*x/=5,x)
solve((a^2+1)*x>3,x)
eigVl([[a,1],[0,a]])
eigVl([[a,b],[b,a]])
eigVc([[a,b],[b,a]])
eigVl([[1,1],[0,1]])
eigVl([[1.5,0],[0,1.5]])
eigVc([[1.5,0],[0,1.5]])
expand((a+b+c+d+z)^30)
expand((x+y)^3000)
newMat(500,500)
seq(k,k,1,100000)
randPoly(x,5000)
expand((a+b+c)^4)
2+3
:clearans
ans+1
approx(3^5000+1-3^5000)
approx(nCr(1000,500))
approx(800!/798!)
1/6+1/10
(2/15)*(45/8)
""".strip().split('\n')
for line in CASES:
    try:
        out = cas.run(line)
    except CASError as ex:
        out = 'Error: ' + str(ex)
    except ZeroDivisionError:
        out = 'Error: Division by zero'
    except Exception as ex:
        out = '!!PYEXC ' + type(ex).__name__ + ': ' + str(ex)
    print(line + '  =>  ' + str(out).replace('\n', ' | '))
