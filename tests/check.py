# Regression check: compares nCAS output with the golden files.
#   python3 tests/check.py [moduledir]        (CPython)
#   micropython tests/check.py dist           (MicroPython)
#   python3 tests/check.py src --update       (rewrite golden files)
import sys
d = sys.argv[1] if len(sys.argv) > 1 else 'src'
sys.path.insert(0, d)
if '--one' in sys.argv:
    import ncastext as cas  # single-file build (runs cas() on import; stdin must be empty)
    CASError = cas.CASError
else:
    import cas
    from cascore import CASError

def cases(f):
    src = open(f).read()
    a = src.index('"""') + 3
    b = src.index('"""', a)
    return [l for l in src[a:b].strip().split('\n') if l]

def result(line):
    try:
        return cas.run(line).replace('\n', ' | ')
    except CASError as ex:
        return 'Error: ' + str(ex)
    except ZeroDivisionError:
        return 'Error: Division by zero'
    except Exception as ex:
        return '!!PYEXC ' + str(ex)

update = '--update' in sys.argv
bad = 0
total = 0
for name in ('run_cases', 'edge_cases'):
    cas.run(':clear')
    lines = cases('tests/' + name + '.py')
    got = [l + '  =>  ' + result(l) for l in lines]
    gold = 'tests/' + name + '.expected'
    if update:
        f = open(gold, 'w')
        f.write('\n'.join(got) + '\n')
        f.close()
        continue
    exp = open(gold).read().strip().split('\n')
    for i in range(len(got)):
        total += 1
        e = exp[i] if i < len(exp) else '<missing>'
        if got[i] != e:
            bad += 1
            print('MISMATCH: ' + got[i])
            print('   expect: ' + e)
        if '!!PYEXC' in got[i]:
            print('PYTHON EXCEPTION: ' + got[i])
print(('updated golden files' if update else '%d/%d match' % (total - bad, total)))
