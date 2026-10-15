# casparse.py - tokenizer and parser for TI-Nspire style input
from cascore import CASError

REPL = (
    ('**', '^'), ('==', '='), ('!=', '/='),
    ('sin⁻¹', 'arcsin'), ('cos⁻¹', 'arccos'), ('tan⁻¹', 'arctan'),
    ('−', '-'), ('–', '-'), ('×', '*'), ('·', '*'),
    ('•', '*'), ('⋅', '*'), ('÷', '/'), ('≤', '<='),
    ('≥', '>='), ('≠', '/='), ('→', '->'), ('⇒', '=>'),
    ('⇔', '<=>'), ('⁻¹', '^(-1)'), ('²', '^2'),
    ('³', '^3'), ('π', ' pi '), ('∞', ' inf '),
    ('ℯ', ' e '), ('ⅈ', ' i '), ('θ', 'theta'),
    ('∫', ' integral'), ('Σ', ' sumseq'), ('∑', ' sumseq'),
    ('Π', ' prodseq'), ('∏', ' prodseq'), ('ᴇ', 'E'),
    ('′', "'"), ('″', "''"), ('@i', ' i '), ('@e', ' e '),
    ('@>', '►'), ('@d', '°'), ('@t', 'ᵀ'), ('⁄', '/'),
    ('infinity', 'inf'), ('α', 'alpha'), ('β', 'beta'),
    ('λ', 'lambda'), ('μ', 'mu'), ('σ', 'sigma'),
    ('Δ', 'delta'),
)

OPS = ('<=>', '=>', '->', '=:', ':=', '<=', '>=', '/=', '<>', '.^', '.*',
       './', '.+', '.-', '>>', '+', '-', '*', '/', '^', '(', ')', '{', '}',
       '[', ']', ',', ';', '=', '<', '>', '|', '!', '%', '&', '°',
       '∠', '►', '√', "'", 'ᵀ')

KEYW = ('and', 'or', 'xor', 'not', 'nor', 'nand')
NOTLETTER = '√°∠►ᵀ'

def normalize(s):
    for a, b in REPL:
        if a in s:
            s = s.replace(a, b)
    return s

def isletter(c):
    if c == '_':
        return True
    o = ord(c)
    if o > 127:
        return c not in NOTLETTER
    return ('a' <= c <= 'z') or ('A' <= c <= 'Z')

def isdig(c):
    return '0' <= c <= '9'

def tokenize(s):
    s = normalize(s)
    toks = []
    i = 0
    n = len(s)
    while i < n:
        c = s[i]
        if c == ' ' or c == '\t':
            i += 1
            continue
        if c == '0' and i + 2 < n and s[i + 1] in 'bBhH':
            base = 2 if s[i + 1] in 'bB' else 16
            j = i + 2
            dg = '01' if base == 2 else '0123456789abcdefABCDEF'
            while j < n and s[j] in dg:
                j += 1
            if j > i + 2:
                toks.append(('num', int(s[i + 2:j], base)))
                i = j
                continue
        if isdig(c) or (c == '.' and i + 1 < n and isdig(s[i + 1])):
            j = i
            while j < n and isdig(s[j]):
                j += 1
            isf = False
            if j < n and s[j] == '.' and not (j + 1 < n and s[j + 1] in '^*/+-' and not isdig(s[j + 1])):
                isf = True
                j += 1
                while j < n and isdig(s[j]):
                    j += 1
            if j < n and (s[j] == 'E' or (s[j] == 'e' and j + 1 < n and isdig(s[j + 1]))):
                k = j + 1
                if k < n and s[k] in '+-':
                    k += 1
                if k < n and isdig(s[k]):
                    isf = True
                    j = k
                    while j < n and isdig(s[j]):
                        j += 1
            txt = s[i:j]
            if isf:
                toks.append(('num', float(txt)))
            else:
                toks.append(('num', int(txt)))
            i = j
            continue
        if isletter(c):
            j = i
            while j < n and (isletter(s[j]) or isdig(s[j])):
                j += 1
            name = s[i:j].lower()
            toks.append(('id', name))
            i = j
            k = 0
            while i < n and s[i] == "'":
                k += 1
                i += 1
            if k:
                toks.append(('prime', k))
            continue
        if c == '"':
            j = s.find('"', i + 1)
            if j < 0:
                raise CASError('Missing "')
            toks.append(('str', s[i + 1:j]))
            i = j + 1
            continue
        for op in OPS:
            if s.startswith(op, i):
                i += len(op)
                if op == '<>':
                    op = '/='
                if op == '>>':
                    op = '►'
                toks.append(('op', op))
                break
        else:
            raise CASError('Invalid character: ' + c)
    toks.append(('end', None))
    return toks

class Parser:
    def __init__(self, toks, isfunc):
        self.t = toks
        self.i = 0
        self.isfunc = isfunc

    def peek(self):
        return self.t[self.i]

    def nxt(self):
        tk = self.t[self.i]
        self.i += 1
        return tk

    def isop(self, op):
        tk = self.t[self.i]
        return tk[0] == 'op' and tk[1] == op

    def isid(self, name):
        tk = self.t[self.i]
        return tk[0] == 'id' and tk[1] == name

    def expect(self, op):
        if not self.isop(op):
            tk = self.peek()
            raise CASError('Missing ' + op)
        self.i += 1

    def top(self):
        e = self.store()
        while self.isop('►'):
            self.nxt()
            tk = self.nxt()
            if tk[0] != 'id':
                raise CASError('Syntax error after conversion')
            args = []
            if self.isop('('):
                self.nxt()
                args = self.args(')')
            e = ('conv', e, tk[1]) + tuple(args)
        if self.peek()[0] != 'end':
            tk = self.peek()
            raise CASError('Syntax error near ' + str(tk[1]) if tk[1] is not None else 'Syntax error')
        return e

    def store(self):
        if self.isid('define'):
            self.nxt()
            lhs = self.sum()
            if not self.isop('='):
                raise CASError('Define needs =')
            self.nxt()
            rhs = self.wth()
            return ('define', lhs, rhs)
        e = self.wth()
        if self.isop('->') or self.isop('=:'):
            self.nxt()
            tgt = self.wth()
            return ('store', e, tgt)
        if self.isop(':='):
            self.nxt()
            rhs = self.wth()
            return ('define', e, rhs)
        return e

    def wth(self):
        e = self.iff()
        while self.isop('|'):
            self.nxt()
            c = self.iff()
            e = ('|', e, c)
        return e

    def iff(self):
        e = self.imp()
        while self.isop('<=>'):
            self.nxt()
            e = ('<=>', e, self.imp())
        return e

    def imp(self):
        e = self.xor()
        while self.isop('=>'):
            self.nxt()
            e = ('=>', e, self.xor())
        return e

    def xor(self):
        e = self.lor()
        while self.isid('xor') or self.isid('nor') or self.isid('nand'):
            op = self.nxt()[1]
            e = (op, e, self.lor())
        return e

    def lor(self):
        e = self.land()
        while self.isid('or'):
            self.nxt()
            e = ('or', e, self.land())
        return e

    def land(self):
        e = self.lnot()
        while self.isid('and'):
            self.nxt()
            e = ('and', e, self.lnot())
        return e

    def lnot(self):
        if self.isid('not'):
            self.nxt()
            return ('not', self.lnot())
        return self.rel()

    def rel(self):
        a = self.sum()
        tk = self.peek()
        if tk[0] == 'op' and tk[1] in ('=', '/=', '<', '>', '<=', '>='):
            self.nxt()
            b = self.sum()
            r = (tk[1], a, b)
            tk2 = self.peek()
            if tk2[0] == 'op' and tk2[1] in ('<', '>', '<=', '>='):
                self.nxt()
                c = self.sum()
                r = ('and', r, (tk2[1], b, c))
            return r
        return a

    def sum(self):
        a = self.prod()
        while True:
            tk = self.peek()
            if tk[0] == 'op' and tk[1] in ('+', '-', '.+', '.-', '&'):
                self.nxt()
                b = self.prod()
                op = tk[1]
                if op == '.+':
                    op = '+'
                elif op == '.-':
                    op = '-'
                a = (op, a, b)
            else:
                return a

    def startsprimary(self):
        tk = self.peek()
        if tk[0] == 'num' or tk[0] == 'str':
            return True
        if tk[0] == 'id':
            return tk[1] not in KEYW
        if tk[0] == 'op':
            return tk[1] in ('(', '{', '√')
        return False

    def prod(self):
        a = self.unary()
        while True:
            tk = self.peek()
            if tk[0] == 'op' and tk[1] in ('*', '/', '.*', './'):
                self.nxt()
                b = self.unary()
                op = tk[1]
                a = (op, a, b)
            elif self.startsprimary():
                b = self.pw()
                a = ('*', a, b)
            else:
                return a

    def unary(self):
        if self.isop('-'):
            self.nxt()
            return ('neg', self.unary())
        if self.isop('+'):
            self.nxt()
            return self.unary()
        return self.pw()

    def pw(self):
        b = self.post()
        if self.isop('^') or self.isop('.^'):
            op = self.nxt()[1]
            if self.isop('ᵀ') or self.isid('t') and False:
                pass
            x = self.unary()
            return ('^' if op == '^' else '.^', b, x)
        return b

    def post(self):
        a = self.primary()
        while True:
            if self.isop('!'):
                self.nxt()
                a = ('!', a)
            elif self.isop('%'):
                self.nxt()
                a = ('%', a)
            elif self.isop('°'):
                self.nxt()
                a = ('deg', a)
            elif self.isop('ᵀ'):
                self.nxt()
                a = ('call', 'transpose', a)
            elif self.isop('['):
                self.nxt()
                idx = self.args(']')
                a = ('index', a) + tuple(idx)
            else:
                return a

    def args(self, close):
        out = []
        if self.isop(close):
            self.nxt()
            return out
        while True:
            out.append(self.store_in())
            if self.isop(','):
                self.nxt()
                continue
            self.expect(close)
            return out

    def store_in(self):
        e = self.wth()
        return e

    def primary(self):
        tk = self.nxt()
        k = tk[0]
        if k == 'num':
            return tk[1]
        if k == 'str':
            return ('str', tk[1])
        if k == 'id':
            name = tk[1]
            if name in KEYW:
                raise CASError('Syntax error: ' + name)
            if self.peek()[0] == 'prime':
                n = self.nxt()[1]
                if self.isop('('):
                    self.nxt()
                    a = self.args(')')
                    return ('primecall', name, n) + tuple(a)
                return ('prime', name, n)
            if self.isop('(') and (self.isfunc(name) or (len(name) > 1 and name not in ('pi', 'inf', 'undef', 'theta'))):
                self.nxt()
                a = self.args(')')
                return ('call', name) + tuple(a)
            return name
        if k == 'op':
            op = tk[1]
            if op == '(':
                e = self.store_in()
                if self.isop('∠'):
                    self.nxt()
                    th = self.store_in()
                    self.expect(')')
                    return ('polar', e, th)
                self.expect(')')
                return e
            if op == '{':
                return ('list',) + tuple(self.args('}'))
            if op == '[':
                return self.matrix()
            if op == '√':
                return ('call', 'sqrt', self.post())
            if op == '-':
                return ('neg', self.pw())
        if k == 'end':
            raise CASError('Incomplete expression')
        raise CASError('Syntax error near ' + str(tk[1]))

    def matrix(self):
        rows = []
        if self.isop('['):
            while self.isop('['):
                self.nxt()
                rows.append(('list',) + tuple(self.args(']')))
                if self.isop(','):
                    self.nxt()
            self.expect(']')
        else:
            row = []
            while True:
                if self.isop(']'):
                    self.nxt()
                    break
                row.append(self.store_in())
                if self.isop(','):
                    self.nxt()
                elif self.isop(';'):
                    self.nxt()
                    rows.append(('list',) + tuple(row))
                    row = []
                elif self.isop(']'):
                    continue
                else:
                    raise CASError('Missing ]')
            rows.append(('list',) + tuple(row))
        n = len(rows[0])
        for r in rows:
            if len(r) != n:
                raise CASError('Dimension error')
        return ('mat',) + tuple(rows)

def parse(s, isfunc):
    toks = tokenize(s)
    if toks[0][0] == 'end':
        raise CASError('Empty input')
    return Parser(toks, isfunc).top()
