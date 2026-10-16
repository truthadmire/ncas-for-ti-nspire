# The 2D layout of every result in the golden files must mean the same as the
# text: the layout is turned back into text (ed_text) and compared with nCAS.
#   python3 tests/layout_check.py
import sys
sys.path.insert(0, 'tests/mock')
sys.path.insert(0, 'src')
import cas, casgui
from cascore import CASError
casgui.G['w'] = 318
outs = []
for f in ('tests/run_cases.expected', 'tests/edge_cases.expected'):
    for line in open(f, encoding='utf-8'):
        if '  =>  ' in line:
            r = line.split('  =>  ', 1)[1].rstrip('\n').replace(' | ', '\n')
            if not r.startswith('Error'):
                outs.append(r)


def back(row):
    # layout -> text; matrices row by row
    s = ''
    for it in row:
        if type(it) is str:
            s += {'·': '*', '≠': '/=', '≤': '<=', '≥': '>='}.get(it, it)
        elif it[0] == 'mat':
            s += '[' + ';'.join([','.join([back(c) for c in r]) for r in it[1]]) + ']'
        else:
            s += casgui.ed_text([it])
    return s


laid = same = differ = 0
for r in outs:
    lt = casgui.tolayout(r)
    if lt is None:
        continue
    laid += 1
    t = back(lt[0])
    plain = r.replace('\n ', '').replace('\n', '')
    if t == plain:
        same += 1
        continue
    cas.ENV.clear()
    pt = ')|x=0.731 and y=1.37 and n=3 and k=2 and a=1.9 and b=0.6 and t=0.4'
    vals = []
    for e in (plain, t):
        try:
            vals.append(cas.run('approx(' + e + pt))
        except Exception as ex:
            vals.append('error: ' + str(ex))
    a, b = vals
    if a == b:
        same += 1
    else:
        differ += 1
        print('DIFF %r\n     2D as text: %r\n     %s | %s' % (plain, t, a, b))
print('layout check: %d results, %d drawn in 2D, %d same, %d differ' % (len(outs), laid, same, differ))
if differ:
    sys.exit(1)
