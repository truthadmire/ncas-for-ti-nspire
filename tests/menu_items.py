# Runs every menu item once with sample answers; reports syntax/Python errors.
import sys
sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else 'src')
import cas, casmenu as M
from cascore import CASError
SAMPLE = {'Matrix A': '1,2;3,4', 'Matrix B': '5,6;7,8', 'Column b 5;1': '5;1', 'Vector u 1,2,3': '1,2,3',
          'Vector v': '4,5,6', 'Matrix/vector': '3,4', 'Matrix 1,2;3,4': '1,2;3,4', 'Matrix': '2,1;1,2',
          'Integer': '360', 'Complex z': '3+4i', 'Complex': '1+i', 'Complex/vector': '1+i',
          'Data 1,2,3': '1,2,3,4', 'Data': '2,4,4,5', 'Eq 1': 'x+y+z=6', 'Eq 2': 'x-y=0', 'Eq 3': 'z=2',
          'Equation': 'x^2+y^2=1', 'Equation/ineq': 'x^2-4>0', 'Quadratic/eqn': 'x^2+6x+5',
          'Rational expr': '1/(x^2-1)', 'Dividend': 'x^3-1', 'Divisor': 'x-1', 'Poly 1': 'x^2-1',
          'Poly 2': 'x^2+2x+1', 'Polynomial': 'x^3-x', "ODE, use y' y''": "y'=y", 'Term': 'k^2',
          'Lower (-inf ok)': '-1', 'Upper': '1', 'Lower (inf ok)': '0', 'At': '1', 'Value': '2',
          'Angle': '30.5', 'Decimal': '0.75', 'Body': 'x^2+1', 'Name': 'q1', 'Area': '0.975',
          'n': '10', 'r': '3', 'p': '1/2', 'x': '3', 'a': '12', 'b': '18', 'From': '0', 'To': '1',
          'Lower': '0', 'Area': '0.5'}
ok = 0
bad = 0
for title, items in M.MAIN:
    for it in items:
        vals = []
        for p in it[2]:
            q = p[0]
            v = p[1] if p[1] else SAMPLE.get(q, 'x^2-1')
            if title == 'Calculus' and q == 'f':
                v = 'x^2*e^x' if it[0] not in ('fMin', 'fMax') else 'x^2-4x'
            if title == 'Solve' and it[0] in ('Solve', 'cSolve', 'nSolve') and q != 'Var' and 'Cond' not in q and 'Var' not in q and 'Lower' not in q and 'Upper' not in q:
                v = SAMPLE.get(q, 'x^2-4>0') if it[0] == 'Solve' else 'x^3=8'
            if len(p) > 2 and p[2] == 'm':
                v = M.matrix_text(v)
            vals.append(v)
        cmd = M.fill(it[1], vals)
        try:
            out = cas.run(cmd)
            ok += 1
            print('%-14s %-40s -> %s' % (it[0], cmd, out.replace('\n', ' ')[:50]))
        except CASError as ex:
            bad += 1
            print('ERROR %-14s %s -> %s' % (it[0], cmd, ex))
        except Exception as ex:
            bad += 1
            print('PYEXC %-14s %s -> %s %s' % (it[0], cmd, type(ex).__name__, ex))
print('menu items ok: %d, errors: %d' % (ok, bad))
