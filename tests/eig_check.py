# Eigenvector property check: every column of eigVc(A) is a unit vector with
# A v = lambda v (lambda = v* A v), for random integer matrices.
#   python3 tests/eig_check.py      micropython tests/eig_check.py
import sys, random
sys.path.insert(0, 'src')
import cas
from cascore import CASError
random.seed(4)
ok = bad = skip = 0
for t in range(160):
    n = random.choice([2, 2, 3])
    M = [[random.randint(-6, 9) for j in range(n)] for i in range(n)]
    m = '[' + ';'.join([','.join([str(x) for x in r]) for r in M]) + ']'
    try:
        cas.run('eigVc(' + m + ')->vv')
        k = int(cas.run('colDim(vv)'))
        good = True
        for c in range(1, k + 1):
            col = 'subMat(vv,1,' + str(c) + ',' + str(n) + ',' + str(c) + ')'
            lam = '(transpose(conj(' + col + '))*' + m + '*' + col + ')[1,1]'
            r = cas.run('approx(norm(' + m + '*' + col + '-' + lam + '*' + col + '))')
            nr = cas.run('approx(norm(' + col + '))')
            if abs(complex(eval(r.replace('i', 'j').replace('\u221e', '1e99')))) > 1e-6 or abs(float(nr) - 1) > 1e-6:
                good = False
        if good:
            ok += 1
        else:
            bad += 1
            print('BAD', m)
    except CASError:
        skip += 1
    except Exception as ex:
        bad += 1
        print('EXC', m, type(ex).__name__, ex)
print('eig check: ok %d bad %d skipped %d' % (ok, bad, skip))
