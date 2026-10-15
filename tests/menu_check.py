# Drives the menu mode with simulated keypad input and checks the results.
#   python3 tests/menu_check.py [python3|micropython] [dist|onefile]
import subprocess, sys
exe = sys.argv[1] if len(sys.argv) > 1 else 'python3'
where = sys.argv[2] if len(sys.argv) > 2 else 'dist'
keys = ['m', '2', '1', 'x^3*sin(x)', '', '', '',
        '4', 'e^(-x)', 'x', '0', 'inf', '', '0',
        '3', '6', 'x+y=5', 'x-y=1', '', '',
        '1', 'sin(x)=1/2', 'x', '0<=x<=2pi', '', '0',
        '4', '1', '1,2;3,4', '', '2', '1,2;3,4', '', '0',
        '1', '8', 'x^2+6x+5', 'x', '', '2', 'x^4-16', '', '', '0',
        '2', 'a', "y''+y=0", 'y(0)=1', "y'(0)=0", '', '', '', '0',
        '5', '1', '360', '', '0',
        '7', '1', 'pi', '', '0',
        '1', 'z', '0', '0', 'q', 'q']
want = ['> d(x^3*sin(x),x)', 'x^3*cos(x)+3*x^2*sin(x)',
        '> integral(e^(-x),x,0,inf)', '\n1\n',
        '> solve(x+y=5 and x-y=1,{x,y})', 'x=3 and y=2',
        '> solve(sin(x)=1/2,x)|0<=x<=2pi', 'x=π/6 or x=5*π/6',
        '> det([1,2;3,4])', '\n-2\n', '> ([1,2;3,4])^-1', '[[-2,1][3/2,-1/2]]',
        '> completeSquare(x^2+6x+5,x)', '(x+3)^2-4',
        '> factor(x^4-16)', '(x-2)*(x+2)*(x^2+4)',
        "> deSolve(y''+y=0 and y(0)=1 and y'(0)=0,x,y)", 'y=cos(x)',
        '> factor(360)', '2^3*3^2*5',
        '> (pi)>>Decimal', '3.141592654',
        'Choose 1-g, 0 or q']
prog = 'ncastext.py' if where == 'onefile' else 'ncas.py'
r = subprocess.run([exe, prog], cwd=where, input='\n'.join(keys) + '\n',
                   capture_output=True, text=True)
out = r.stdout
bad = [w for w in want if w not in out]
for w in bad:
    print('MISSING: ' + repr(w))
print('menu check: %d/%d expected outputs found' % (len(want) - len(bad), len(want)))
if r.returncode:
    print(r.stderr[-800:])
