import sys, time
sys.path.insert(0, sys.argv[1] if len(sys.argv) > 1 else 'src')
import cas
files = sys.argv[2:] if len(sys.argv) > 2 else ['tests/run_cases.py', 'tests/edge_cases.py']
lines = []
for f in files:
    src = open(f).read()
    a = src.index('"""') + 3
    b = src.index('"""', a)
    lines += [l for l in src[a:b].strip().split('\n') if l and l != 'q']
res = []
tot = 0.0
for l in lines:
    t0 = time.time()
    try:
        cas.run(l)
    except Exception:
        pass
    dt = time.time() - t0
    tot += dt
    res.append((dt, l))
res.sort(key=lambda r: -r[0])
for dt, l in res[:25]:
    print('%7.3f  %s' % (dt, l))
print('total %.2f s for %d commands' % (tot, len(lines)))
