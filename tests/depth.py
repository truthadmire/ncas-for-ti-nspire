import sys
sys.path.insert(0, 'src')
import cas
files = ['tests/run_cases.py', 'tests/edge_cases.py']
lines = []
for f in files:
    src = open(f).read()
    a = src.index('"""') + 3
    b = src.index('"""', a)
    lines += [l for l in src[a:b].strip().split('\n') if l and l != 'q']
st = {'d': 0, 'max': 0}
def prof(frame, event, arg):
    if event == 'call':
        st['d'] += 1
        if st['d'] > st['max']:
            st['max'] = st['d']
    elif event == 'return':
        st['d'] -= 1
res = []
for l in lines:
    st['d'] = 0
    st['max'] = 0
    sys.setprofile(prof)
    try:
        cas.run(l)
    except Exception:
        pass
    sys.setprofile(None)
    res.append((st['max'], l))
res.sort(key=lambda r: -r[0])
for d, l in res[:15]:
    print(d, l)
