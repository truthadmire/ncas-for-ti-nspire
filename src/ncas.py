# ncas.py - launcher for nCAS (run this program on the TI-Nspire CX II)
# If nCAS cannot start, it checks every module and says which one is
# missing or has the wrong contents.
try:
    from cas import start
except Exception as ex:
    start = None
    print('nCAS could not start: ' + str(ex))
    print('Checking the modules in PyLib:')
    # each module and a name that only the right file defines
    for m, n in (('cascore', 'simp'), ('casout', 'fmt'), ('casparse', 'parse'),
                 ('caspoly', 'factor_expr'), ('cascalc', 'integrate'),
                 ('cassolve', 'solve'), ('casmat', 'm_inv'), ('casfun', 'conv'),
                 ('cashelp', 'selftest'), ('casmenu', 'runmenu'), ('casgui', 'rungui'),
                 ('cas', 'run')):
        try:
            if hasattr(__import__(m), n):
                msg = 'ok'
            else:
                msg = 'WRONG CONTENTS (paste ' + m + '.py again)'
        except Exception as e:
            msg = str(e)
            if msg == "no module named '" + m + "'":
                msg = 'MISSING (not in PyLib, or misnamed)'
            elif ("'" + m + ".") in msg or msg == "can't import name " + m:
                msg = 'WRONG CONTENTS (paste ' + m + '.py again)'
            else:
                msg = 'BAD: ' + msg
        print(' ' + m + ': ' + msg)
    print('Each module must be in PyLib, in a document with the same name (e.g. cas.tns).')
if start:
    start()
