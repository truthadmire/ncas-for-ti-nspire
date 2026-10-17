# onefile.py - merge the nCAS modules (src/*.py) into ONE program file
# (onefile/ncas.py) that can be pasted into a single TI-Nspire Python program.
#
# - internal imports (import caspoly as PO, from cascore import *, ...) are removed
# - qualified references such as PO.factor_expr become plain names
# - top-level names defined in several modules: identical definitions are
#   kept once, different ones are renamed with a module prefix
# - the result is minified with tools/build.py (1-space indent, ASCII only)
# - the file ends with start(): the graphical mode on the calculator, else
#   the text command loop
#
# Two outputs, each stored as text parts (string literals) that are compiled
# one at a time with exec(), so the calculator never compiles 250 KB at once;
# cashelp, casmenu and casgui are compiled on first use:
#   onefile/ncastext.py   text mode only (no casgui)
#   onefile/ncasgui.py    full-screen mode (ti_draw + ti_system.get_key)
import ast
import io
import os
import sys
import tokenize

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'src')
OUT = os.path.join(ROOT, 'onefile')
sys.path.insert(0, os.path.join(ROOT, 'tools'))
import build as build_mod

MODS = ['cascore', 'casout', 'casparse', 'caspoly', 'cascalc', 'cassolve',
        'casmat', 'casfun', 'cashelp', 'casmenu', 'casgui', 'cas']
ALLMODS = MODS[:]
LAZY = ['cashelp', 'casmenu', 'casgui']     # compiled only when first used
CHUNK = 6000                      # target size of one text part (bytes)
PREFIX = {'cascore': 'co', 'casout': 'ou', 'casparse': 'pa', 'caspoly': 'po',
          'cascalc': 'ca', 'cassolve': 'so', 'casmat': 'ma', 'casfun': 'fn',
          'cashelp': 'he', 'casmenu': 'me', 'casgui': 'gu', 'cas': 'cs', 'casx': 'cx'}


def top_defs(tree, text):
    # name -> source text of its top-level definition(s)
    out = {}
    lines = text.split('\n')
    for node in tree.body:
        names = []
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            names = [node.name]
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    names.append(t.id)
                elif isinstance(t, ast.Tuple):
                    names += [e.id for e in t.elts if isinstance(e, ast.Name)]
        elif isinstance(node, ast.For) and isinstance(node.target, ast.Name):
            names = [node.target.id]
        seg = '\n'.join(lines[node.lineno - 1:node.end_lineno])
        for n in names:
            out.setdefault(n, []).append((seg, node))
    return out


def import_info(tree):
    # alias -> module for 'import casX as Y' / 'import casX';
    # name -> module for 'from casX import name'; and line ranges to delete
    alias = {}
    names = {}
    ranges = []
    lazy = {}       # line -> lazy module imported there (inside a function)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            internal = [a for a in node.names if a.name in MODS]
            if internal:
                if len(internal) != len(node.names):
                    raise SystemExit('mixed import not supported')
                for a in internal:
                    alias[a.asname or a.name] = a.name
                    if a.name in LAZY:
                        if node.col_offset == 0 or len(node.names) != 1:
                            raise SystemExit('lazy module imported at top level: ' + a.name)
                        lazy[node.lineno] = a.name
                ranges.append((node.lineno, node.end_lineno))
        elif isinstance(node, ast.ImportFrom) and node.module in MODS:
            for a in node.names:
                if a.name != '*':
                    names[a.asname or a.name] = (node.module, a.name)
            ranges.append((node.lineno, node.end_lineno))
    return alias, names, ranges, lazy


def merge(mods):
    # merged, renamed source of each module in mods
    global MODS
    MODS = mods
    texts = {}
    trees = {}
    defs = {}
    for m in MODS:
        texts[m] = open(os.path.join(SRC, m + '.py'), encoding='utf-8').read()
        trees[m] = ast.parse(texts[m])
        defs[m] = top_defs(trees[m], texts[m])

    # final name of each (module, name); duplicates to drop
    final = {}
    first = {}
    drop = {m: [] for m in MODS}
    for m in MODS:
        for n, items in defs[m].items():
            if n not in first:
                first[n] = (m, items)
                final[(m, n)] = n
                continue
            fm, fitems = first[n]
            same = [s for s, _ in items] == [s for s, _ in fitems]
            if same:
                if fm in LAZY and m not in LAZY:
                    raise SystemExit('%s.%s is only kept in lazy module %s' % (m, n, fm))
                final[(m, n)] = n
                for s, node in items:
                    drop[m].append((node.lineno, node.end_lineno))
            else:
                final[(m, n)] = PREFIX[m] + '_' + n
                print('renamed %s.%s -> %s' % (m, n, final[(m, n)]))

    def resolve(mod, name):
        # final name for a name looked up in module 'mod'
        if (mod, name) in final:
            return final[(mod, name)]
        return name

    out_parts = []
    for m in MODS:
        alias, imported, ranges, lazy = import_info(trees[m])
        text = texts[m]
        lines = text.split('\n')
        dead = set()
        for a, b in ranges + drop[m]:
            for i in range(a, b + 1):
                dead.add(i)
        # bare-name map for this module
        bare = {}
        for n in defs[m]:
            bare[n] = final[(m, n)]
        for n, (src, orig) in imported.items():
            if n not in bare:
                bare[n] = resolve(src, orig)
        toks = list(tokenize.generate_tokens(io.StringIO(text).readline))
        # build replacement edits: (row, col_start, col_end, newtext)
        edits = []
        i = 0
        while i < len(toks):
            t = toks[i]
            if t.type == tokenize.NAME:
                prev = toks[i - 1] if i > 0 else None
                after_dot = prev is not None and prev.type == tokenize.OP and prev.string == '.'
                if (not after_dot and t.string in alias and i + 2 < len(toks)
                        and toks[i + 1].string == '.' and toks[i + 2].type == tokenize.NAME):
                    target = alias[t.string]
                    newname = resolve(target, toks[i + 2].string)
                    if t.start[0] != toks[i + 2].end[0]:
                        raise SystemExit('split qualified name')
                    edits.append((t.start[0], t.start[1], toks[i + 2].end[1], newname))
                    i += 3
                    continue
                if not after_dot and t.string in bare and bare[t.string] != t.string:
                    nxt = toks[i + 1] if i + 1 < len(toks) else None
                    if nxt is not None and nxt.type == tokenize.OP and nxt.string == '=' and in_call(toks, i):
                        pass  # keyword argument name
                    else:
                        edits.append((t.start[0], t.start[1], t.end[1], bare[t.string]))
            i += 1
        by_row = {}
        for r, a, b, s in edits:
            by_row.setdefault(r, []).append((a, b, s))
        new_lines = []
        for idx, line in enumerate(lines, 1):
            if idx in lazy:
                ind = len(line) - len(line.lstrip(' '))
                new_lines.append(' ' * ind + "_load('%s')" % lazy[idx])
                continue
            if idx in dead:
                # keep indentation-correct placeholder if this was the only
                # statement of a block
                ind = len(line) - len(line.lstrip(' '))
                new_lines.append(' ' * ind + 'pass' if needs_pass(lines, idx, dead) else '')
                continue
            for a, b, s in sorted(by_row.get(idx, []), reverse=True):
                line = line[:a] + s + line[b:]
            new_lines.append(line)
        body = '\n'.join(new_lines)
        k = body.find("\nif __name__ == '__main__':")
        if k >= 0:
            body = body[:k] + '\n'
        out_parts.append((m, body))

    # check the merged program as a whole
    ast.parse('\n'.join(b for _, b in out_parts))
    return out_parts


ALL = ALLMODS
VARIANTS = (
    # file, modules, code run after loading, first line of the file
    ('ncastext', [m for m in ALL if m != 'casgui'], 'GUI=False\ncas()',
     'ncastext - nCAS text version for TI-Nspire CX II. Run it (ctrl+R): ? help, m menus, q quit.'),
    ('ncasx', ['cascore', 'casout', 'casparse', 'casx'], 'xcalc()',
     'ncasx - nCAS exact calculator for TI-Nspire CX II. Run it (ctrl+R), type an expression; q quits.'),
    ('ncasgui', ALL, 'startgui()',
     'ncasgui - nCAS full-screen version for TI-Nspire CX II. Run it (ctrl+R): tab menus, esc quits.'),
)


def main():
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    for name, mods, tail, title in VARIANTS:
        build(name, merge(mods), tail, title)


def build(name, out_parts, tail, title):
    # parts are stored with frequent words replaced by '$' + one character
    # (see dictionary()) and decoded by _u() before exec
    parts = [(m, chunks(build_mod.minify(body))) for m, body in out_parts]
    words = dictionary([c for _, cs in parts for c in cs])
    lines = ['# ' + title, LOADER, '_W=' + repr(words)]
    lazy = []
    nparts = 0
    for m, cs in parts:
        nparts += len(cs)
        lits = [literal(encode(c, words)) for c in cs]
        if m in LAZY:
            lazy.append("_L['%s']=(%s,)" % (m, ',\n'.join(lits)))
        else:
            lines += ['_x(%s)' % c for c in lits]
    lines += lazy
    t = tail.split('\n')
    lines += ['_x(%r)' % l for l in t[:-1]]
    lines.append('del _x\n' + t[-1] + '\n')
    full = '\n'.join(lines)
    ast.parse(full)
    write(os.path.join(OUT, name + '.py'), full)
    print('  %d text parts' % nparts)

LOADER = '''# The program is kept below as text and compiled one part at a time, which needs
# much less memory than compiling everything at once. Do not edit the text parts.
try:
 import gc
except ImportError:
 gc = None
try:
 exec
except NameError:
 print('exec() is missing: use the module install (dist/)')
 raise SystemExit
_L = {}
_P = {}     # parts of a lazy module already compiled (a failed load can be retried)
# the helpers are compiled from text too, so that nothing compiled from this
# file itself keeps the text parts in memory once the program has ended
exec(\"\"\"def _u(s):
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
 _P.pop(m, None)\"\"\")
print('Loading nCAS...')'''

# characters that may follow '$' in a code (no quotes or backslash, so the
# parts stay valid raw strings)
CODES = ''.join(c for c in map(chr, range(33, 127)) if c not in '$\'"\\')


def dictionary(texts):
    # the words whose replacement by a 2-character code saves the most
    import collections, re
    cnt = collections.Counter()
    for t in texts:
        if '$' in t:
            raise SystemExit("'$' appears in the program text")
        cnt.update(re.findall(r'[A-Za-z_][A-Za-z_0-9]*', t))
    best = sorted(cnt, key=lambda w: (-(len(w) - 2) * cnt[w], w))
    best = [w for w in best if (len(w) - 2) * cnt[w] > len(w) + 8]
    return dict(zip(CODES, best))


def encode(text, words):
    import re
    inv = dict((w, '$' + c) for c, w in words.items())
    out = re.sub(r'[A-Za-z_][A-Za-z_0-9]*', lambda m: inv.get(m.group(0), m.group(0)), text)
    # decoding must give back the text exactly
    p = out.split('$')
    if p[0] + ''.join(words[q[0]] + q[1:] for q in p[1:]) != text:
        raise SystemExit('encoding is not reversible')
    return out


def chunks(text):
    # split minified code into parts of whole top-level statements
    tree = ast.parse(text)
    lines = text.split('\n')
    starts = [n.lineno - 1 for n in tree.body] + [len(lines)]
    out = []
    cur = ''
    for a, b in zip(starts, starts[1:]):
        stmt = '\n'.join(lines[a:b]).rstrip('\n') + '\n'
        if cur and len(cur) + len(stmt) > CHUNK:
            out.append(cur)
            cur = ''
        cur += stmt
    if cur:
        out.append(cur)
    return out


def literal(code):
    # code as a raw triple-quoted string; the text stays readable and every
    # line keeps its own length (the TI editor does not like huge lines)
    for q in ("'''", '"""'):
        if q not in code and not code.endswith('\\'):
            return 'r' + q + code + q
    return repr(code)


def write(p, text):
    text.encode('ascii')
    open(p, 'w', encoding='ascii', newline='\n').write(text)
    print('wrote %s: %d bytes, %d lines' % (p, len(text), text.count('\n')))


def in_call(toks, i):
    # is token i inside parentheses (keyword argument position)?
    depth = 0
    j = i - 1
    while j >= 0:
        s = toks[j].string
        if toks[j].type == tokenize.OP:
            if s in ')]}':
                depth += 1
            elif s in '([{':
                if depth == 0:
                    return s == '('
                depth -= 1
        if toks[j].type in (tokenize.NEWLINE,):
            return False
        j -= 1
    return False


def needs_pass(lines, idx, dead):
    # True if line idx (deleted) was the only statement of its block
    line = lines[idx - 1]
    ind = len(line) - len(line.lstrip(' '))
    if ind == 0:
        return False
    # previous live non-blank line must end with ':' and next live line
    # must be dedented for this to be the only statement
    j = idx - 2
    while j >= 0 and (j + 1 in dead or not lines[j].strip()):
        j -= 1
    if j < 0 or not lines[j].rstrip().endswith(':'):
        return False
    k = idx
    while k < len(lines) and (k + 1 in dead or not lines[k].strip()):
        k += 1
    if k >= len(lines):
        return True
    nind = len(lines[k]) - len(lines[k].lstrip(' '))
    return nind < ind


if __name__ == '__main__':
    main()
