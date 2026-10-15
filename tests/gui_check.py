# Drives the graphical mode (casgui) with simulated keys on a desktop, using
# the stand-in ti_draw / ti_system modules in tests/mock.
#   python3 tests/gui_check.py [src|dist|onefile] [-v]
#   micropython tests/gui_check.py dist
import sys
where = 'src'
for a in sys.argv[1:]:
    if a != '-v':
        where = a
verbose = '-v' in sys.argv
sys.path.insert(0, 'tests/mock')
sys.path.insert(0, where)
import ti_system
import ti_draw


def word(s):
    return list(s)


K = []
# 1 typing and evaluating
K += word('solve(x^2-5x+6=0,x)') + ['enter']
# 2 command menu: Calculus > Derivative puts d(|,x) on the line
K += ['menu', '2', '1'] + word('sin(x)^2') + ['enter']
# 3 an operator on an empty line starts with ans
K += ['*', '2', 'enter']
# 4 history: up twice selects the previous input, enter copies it
K += ['up', 'up', 'up', 'enter', 'enter']
# 5 matrix item: det([|])
K += ['menu', '4', '1'] + word('1,2;3,4') + ['enter']
# 6 settings run at once: degree mode
K += ['menu', '8', '1']
K += word('sin(30)') + ['enter']
K += ['menu', '8', '2']
# 7 errors, unknown keys, trig popup, editing keys
K += word('1/0') + ['enter'] + word('2*') + ['enter']
K += ['foo']
K += ['trig', '2', 'pi', 'enter']
K += word('abc') + ['left', 'left', 'del', 'enter']
K += word('x+1') + ['clear'] + word('2+3') + ['enter']
# 8 square and sqrt keys (names not confirmed on the device)
K += ['sqrt'] + word('8') + ['right', 'square', 'enter']
# 9 self-test from the Settings menu
K += ['menu', '8', 'd']
# 10 a long line scrolls
K += word('1+2+3+4+5+6+7+8+9+10+11+12+13+14+15+16+17+18+19+20')
SHOT_LONG = len(K)
K += ['enter']
# 12 matrix template: 2x3 typed as digits, cells filled with tab
K += ['menu', '9', '1', '2', '3', 'enter', '1', 'tab', '2', 'tab', '3', 'tab', '4', 'tab', '5', 'tab', '6', 'enter', 'enter']
# 13 template inside det([|]) from the Matrix menu (default 2x2)
K += ['menu', '4', '1', 'menu', '9', '1', 'enter', '1', 'tab', '2', 'tab', '3', 'tab', '4', 'enter', 'enter']
# 14 simult with a matrix template and a column-vector template, ';' from symbols
K += word('simult(') + ['menu', '9', '1', 'enter', '2', 'tab', '1', 'tab', '1', 'tab', '-', '1', 'enter']
K += [','] + ['menu', '9', '2', 'down', 'enter', '5', 'down', '1', 'enter'] + [')', 'enter']
K += word('[7,8') + ['menu', 'a', 'enter'] + word('9,0]') + ['enter']
# 16 Symbols page: sqrt( ) (row 3, column 4) and store -> (row 2, last column)
K += ['menu', 'a', 'down', 'down', 'right', 'right', 'right', 'enter', '9', 'enter']
# (the page reopens on the last symbol used, sqrt: 4 to the left is ->)
K += ['5', 'menu', 'a'] + ['left'] * 4 + ['enter'] + word('qq') + ['enter'] + word('qq*2') + ['enter']
# 17 symbols page wraps and esc closes without typing
K += ['menu', 'a', 'up', 'left', 'esc', '1', 'enter']
# 15 esc in the grid cancels
K += ['menu', '9', '1', 'enter', '5', 'esc', 'clear']
# 18 ctrl layer: separate ctrl key, combined name, finished symbol, doc as ctrl
K += ['ctrl', '('] + word('1,2') + ['enter']                       # [1,2]
K += ['ctrl+)'] + word('1,2') + ['enter']                          # {1,2}
K += ['ctrl', 'square', '9', 'enter']                              # sqrt(9)
K += ['ctrl', '^', '3', 'right', '8', 'enter']                     # root(8,3): index first
K += word('pi') + ['ctrl', 'enter']                                # approx(pi)
K += ['5', 'ctrl', 'var'] + word('ww') + ['enter'] + word('ww+1') + ['enter']
K += word('abc') + ['clear', 'ctrl', 'esc', 'right', 'right', 'right'] + word('de') + ['enter']
K += word('1/3') + ['\u2248']                                       # approx(1/3)
K += ['1', 'ctrl', '=', '2'] + ['2', 'enter']                      # 1/=2
K += ['doc', '('] + word('7') + ['enter']                          # [7]
K += ['ctrl', 'trig', 'x', 'ctrl', '.']                            # help page, unused ctrl
K += ['menu', '9', '1', 'enter', 'ctrl', 'square', '4', ')', 'tab', '1', 'tab', '1', 'tab', '1', 'enter', 'enter']
# 19 2D entry: fraction template (ctrl /), up/down between slots, mixed terms
K += ['ctrl', '/', '3', 'down'] + word('x+1') + ['right', 'enter']          # 3/(x+1)
K += ['2', 'ctrl', '/', '1', 'down', '3', 'right', '+', '1', 'enter']        # 2(1/3)+1 = 5/3
K += ['ctrl', '/', 'down', '4', 'up', '8', 'right', 'enter']                 # 8/4 = 2
K += ['exp', '(', 'x', '+', '1', ')', 'right', 'enter']                      # e^(x+1)
K += ['menu', '9', '4', '7', 'down', '9', 'right', 'enter']                   # Templates > Fraction
K += ['ctrl', '/', 'del', '5', 'enter']                                      # empty template deleted
K += ['ctrl', '/', 'sqrt', '2', 'right', 'down', '2', 'right', 'enter']      # sqrt(2)/2
K += ['x', '^', '-', '1', '+', '1', 'enter']                                 # x^(-1)+1
# 20 tab = next field, menu = commands, catalog = A-Z list
K += ['menu', '2', '4'] + word('x^2') + ['tab', 'tab', '0', 'tab', '1', 'enter']   # integral(x^2,x,0,1)
K += ['ctrl', '/', '1', 'tab', '2', 'tab', '+', '1', 'enter']                     # 1/2+1 (tab leaves at the end)
K += ['ctrl', '/', '5', 'tab', '6', 'shift+tab', '0', 'tab', 'tab', 'enter']      # shift+tab back: 50/6
K += ['catalog', 'z', 'enter'] + word('x^2-1,x') + ['enter']                       # zeros(x^2-1,x)
K += ['ctrl', 'tab', '3', '1'] + word('x^2=4') + ['enter']                        # ctrl tab opens the menu
# 21 matrix template next to an empty [] (cursor moved one place) fills it
K += ['menu', '4', '8', 'left', 'menu', '9', '1', 'enter', '8', 'tab', '5', 'tab', '7', 'tab', '9', 'enter', 'enter']
K += ['menu', '4', '1', 'right', 'menu', '9', '1', 'enter', '1', 'tab', '2', 'tab', '3', 'tab', '4', 'enter', 'enter']
# 11 esc leaves the history, clears the line, then quits
K += ['up', 'esc'] + word('7') + ['esc', 'esc']
K += ['never']          # must not be read: esc on an empty line quits
ti_system.KEYS[:] = K

# record every evaluation (input and result): results are drawn in 2D, so
# they are checked here rather than read off the screen
LOG = []


def hook():
    for name in ('casgui', 'ncasgui'):
        m = sys.modules.get(name)
        if m is not None and hasattr(m, 'evaluate'):
            orig = m.evaluate

            def ev(run, s, orig=orig, m=m):
                orig(run, s)
                LOG.append(s)
                LOG.append(m.G['hist'][-1][1])
            m.evaluate = ev
            return


ti_system.HOOK.append(hook)

if where == 'onefile':
    import ncasgui       # runs startgui() on import
else:
    import cas
    cas.start()

frames = ti_draw.FRAMES
want = ['x=2 or x=3', '> ', 'd(sin(x)^2,x)', '2*cos(x)*sin(x)',
        'ans*2', '4*cos(x)*sin(x)', 'det([1,2;3,4])', '-2',
        'sin(30)', '1/2', '1/0', 'undef', 'Error: Incomplete expression',
        "key 'foo' not used", 'cos(\u03c0)', '-1', 'bc', '5',
        'sqrt(8)^2', '8', '18/18 tests passed', '[1,2,3;4,5,6]', '[[1,2,3][4,5,6]]',
        'det([1,2;3,4])', 'simult([2,1;1,-1],[5;1])', '[[2][1]]', '[7,8;9,0]', '[[7,8][9,0]]', 'sqrt(9)', '5->qq', 'qq*2', '10', '[1,2]', '{1,2}', 'root(8,3)', 'approx(pi)', '3.141592654', '5->ww', 'ww+1', '6',
        'abcde', 'approx(1/3)', '0.3333333333', '1/=2', 'true', '[7]', 'ctrl+. not used',
        '[sqrt(4),1;1,1]', '[[2,1][1,1]]', '3/(x+1)', '2(1/3)+1', '5/3', '8/4', 'e^(x+1)', '7/9', 'sqrt(2)/2', '\u221a2/2',
        'x^(-1)+1', 'integral(x^2,x,0,1)', '1/3', '(1/2)+1', '3/2', '50/6', '25/3', 'zeros(x^2-1,x)', '{-1,1}',
        'solve(x^2=4,x)', 'x=-2 or x=2', 'menu: commands', 'eigVc([8,5;7,9])', '210', 'nCAS  DEG', 'nCAS  RAD']
want.remove('> ')
bad = []
for w in want:
    for f in frames + LOG:
        if w in f:
            break
    else:
        bad.append(w)
if len(LOG) < 100:
    bad.append('evaluations not recorded: %d' % len(LOG))
if ti_system.KEYS != ['never']:
    bad.append('keys left over: ' + repr(ti_system.KEYS[:5]))
if verbose:
    for i in (8, 30, SHOT_LONG - 2, len(frames) - 1):
        if 0 <= i < len(frames):
            print('--- frame %d' % i)
            print(frames[i])
for w in bad:
    print('MISSING: ' + repr(w))
print('gui check: %d/%d, %d frames' % (len(want) + 1 - len(bad), len(want) + 1, len(frames)))
