# build.py - make compact, ASCII-only copies of the nCAS modules for the
# TI-Nspire (src/*.py -> dist/*.py): drops comments and blank lines, uses
# 1-space indentation, removes spaces that are not needed between tokens
# and escapes non-ASCII characters as \uXXXX.
import io, os, sys, tokenize

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'src')
DST = os.path.join(ROOT, 'dist')

def esc(line):
    out = []
    for c in line:
        o = ord(c)
        if o < 128:
            out.append(c)
        elif o < 0x10000:
            out.append('\\u%04x' % o)
        else:
            raise ValueError('non-BMP character')
    return ''.join(out)

def minify(text):
    out = []
    depth = 0
    for raw in text.split('\n'):
        line = raw.rstrip()
        s = line.lstrip(' ')
        if not s or (s.startswith('#') and depth == 0):
            continue
        n = len(line) - len(s)
        if depth == 0:
            if n % 4:
                raise ValueError('odd indentation: ' + raw)
            ind = ' ' * (n // 4)
        else:
            ind = ' '
        out.append(ind + esc(s))
        # track bracket depth (strings in this code base never contain
        # unbalanced brackets across lines)
        depth += bracket_delta(s)
    return tighten('\n'.join(out) + '\n')

WORD = (tokenize.NAME, tokenize.NUMBER, tokenize.STRING)
SKIP = (tokenize.NL, tokenize.NEWLINE, tokenize.INDENT, tokenize.DEDENT,
        tokenize.COMMENT, tokenize.ENDMARKER)

def toks(text):
    return [t for t in tokenize.generate_tokens(io.StringIO(text).readline)
            if t.type not in SKIP]

def tighten(text):
    # rebuild every line with a space only between two names, numbers or
    # strings ('return x', 'a in b'); keeps the line structure and indentation
    lines = text.split('\n')
    rows = {}
    for t in toks(text):
        if t.start[0] != t.end[0]:
            return text             # a token spanning lines: leave as is
        rows.setdefault(t.start[0], []).append(t)
    out = []
    for i, line in enumerate(lines, 1):
        ts = rows.get(i)
        if not ts:
            out.append(line)
            continue
        parts = [line[:len(line) - len(line.lstrip(' '))]]
        prev = None
        for t in ts:
            if prev is not None and prev.type in WORD and t.type in WORD:
                parts.append(' ')
            parts.append(t.string)
            prev = t
        out.append(''.join(parts))
    new = '\n'.join(out)
    a = [(t.type, t.string) for t in toks(text)]
    b = [(t.type, t.string) for t in toks(new)]
    if a != b:
        raise ValueError('tighten changed the tokens')
    return new

def bracket_delta(s):
    d = 0
    q = None
    i = 0
    while i < len(s):
        c = s[i]
        if q:
            if c == '\\':
                i += 2
                continue
            if c == q:
                q = None
        elif c in '\'"':
            q = c
        elif c == '#':
            break
        elif c in '([{':
            d += 1
        elif c in ')]}':
            d -= 1
        i += 1
    return d

def main():
    if not os.path.isdir(DST):
        os.makedirs(DST)
    total = 0
    for name in sorted(os.listdir(SRC)):
        if not name.endswith('.py'):
            continue
        text = open(os.path.join(SRC, name), encoding='utf-8').read()
        m = minify(text)
        open(os.path.join(DST, name), 'w', encoding='ascii', newline='\n').write(m)
        total += len(m)
        print('%-12s %6d -> %6d bytes' % (name, len(text.encode('utf-8')), len(m)))
    print('total %d bytes' % total)

if __name__ == '__main__':
    main()
