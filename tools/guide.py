# Builds site/guide.html, the complete usage guide on the website. Every
# screen in it is real: each example's keys are sent to the program running
# against the stand-in display and keypad in tests/mock, and the last frame is
# drawn as SVG. The text-mode transcripts are real nCAS output too.
#   python3 tools/guide.py            (run from the repository root)
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, 'site', 'guide.html')

# --------------------------------------------------------------- examples
# Keys are written as on the keypad: [menu] is a key, plain words are typed.
# The arrows are [▲] [▼] [◄] [►]; [ctrl] [÷] is ctrl then the divide key.
LABEL = {'▲': 'up', '▼': 'down', '◄': 'left', '►': 'right', '÷': '/', '×': '*',
         'x²': 'square', 'shift tab': 'shift+tab', 'catalog': 'catalog', '(−)': '(-)',
         '−': '-', 'EE': 'EE', '√': 'sqrt'}


def keys(s):
    # the strokes as the program reads them, and as the page shows them
    out = []
    show = []
    for tok in s.split():
        if tok.startswith('[') and tok.endswith(']') and len(tok) > 2:
            k = tok[1:-1].replace('_', ' ')
            out.append(LABEL.get(k, k))
            show.append(('k', k))
        else:
            t = tok.replace('_', ' ')
            out += list(t)
            show.append(('t', t))
    return out, show


GUI = 'gui'
NAV = 'nav'
UNIT = 'unit'

SECTIONS = []


def section(sid, eyebrow, title, intro):
    SECTIONS.append({'id': sid, 'eyebrow': eyebrow, 'title': title, 'intro': intro, 'items': []})


def card(title, what, k='', prog=GUI, pre=(), wide=False):
    SECTIONS[-1]['items'].append({'kind': 'card', 'title': title, 'what': what, 'k': k,
                                  'prog': prog, 'pre': list(pre), 'wide': wide})


def term(title, what, lines, prog='text'):
    SECTIONS[-1]['items'].append({'kind': 'term', 'title': title, 'what': what,
                                  'lines': lines, 'prog': prog})


def html(s):
    SECTIONS[-1]['items'].append({'kind': 'html', 'html': s})


# ---- getting started
section('start', 'Getting started', 'Install, run, and check that it works.',
        'nCAS is five independent programs, each a single Python file in a TI-Nspire '
        'document. Install the ones you want; none of them needs the others.')
html('''<div class="table-wrap"><table class="plain">
<thead><tr><th>Program</th><th>What it is</th><th>Size</th><th>Needs</th></tr></thead><tbody>
<tr><td class="in">ncasgui</td><td>The full-screen CAS: 2D entry with templates, menus, catalog, results drawn as math.</td><td>277 KB · 14 parts</td><td>OS with <code>ti_draw</code> and <code>get_key</code></td></tr>
<tr><td class="in">ncastext</td><td>The same CAS at a <code>&gt;</code> prompt in the Python Shell, with numbered menus.</td><td>240 KB · 13 parts</td><td>any OS with Python</td></tr>
<tr><td class="in">ncasx</td><td>A small, fast exact calculator: exact value plus decimal, no menus.</td><td>59 KB · 3 parts</td><td>any OS with Python</td></tr>
<tr><td class="in">navcalc</td><td>Aviation (E6B) calculator: wind, crosswind, time-speed-distance, fuel, altitudes, airspeed.</td><td>21 KB · 2 parts</td><td><code>ti_draw</code> (else Shell)</td></tr>
<tr><td class="in">unitconv</td><td>Unit converter: 16 categories, about 150 units, all converting as you type.</td><td>15 KB · 1 part</td><td><code>ti_draw</code> (else Shell)</td></tr>
</tbody></table></div>
<div class="steps">
<div class="step"><span class="n">step 1</span><h3>Download</h3><p>Get the <code>.tns</code> documents from the <a href="https://github.com/truthadmire/ncas-for-ti-nspire/releases/latest" target="_blank" rel="noopener">latest release</a>.</p></div>
<div class="step"><span class="n">step 2</span><h3>Send to the handheld</h3><p>Connect by USB and drag the document onto the calculator in the TI-Nspire software (My Documents).</p></div>
<div class="step"><span class="n">step 3</span><h3>Run</h3><p>Open the document and press <b>ctrl R</b>. On a CX II the CAS starts full screen; Press-to-Test must be off.</p></div>
</div>
<div class="alt"><div><h3>Or build a document yourself</h3>
<p>The TI editor refuses very large pastes, so a helper puts a program on the clipboard one part at a time. Make a new Python program with the name shown, paste each part at the end, then <b>Check Syntax &amp; Save</b>.</p>
<div class="copyline"><code>python3 tools/paste_parts.py onefile/ncasgui.py 20000</code></div>
<p class="small">Use <code>ncastext.py</code>, <code>ncasx.py</code>, <code>navcalc.py</code> or <code>unitconv.py</code> for the others. The helper prints how many lines the program should have after each part.</p></div>
<div class="callout"><strong>Saved between runs</strong><p>Settings, variables and functions are kept in the document (list <code>ncasmem</code>), so they are still there after a restart. Save the document to keep them after closing it.</p>
<strong style="margin-top:8px">Exams</strong><p>Press-to-Test hides every file, nCAS included. Check what your exam allows.</p></div></div>''')
card('Check the installation', 'Settings ▸ Self-test runs 18 problems (factor, solve, integral, limit, deSolve, matrices…). All of them should pass.',
     '[menu] [8] [d]')

# ---- ncasgui basics
section('gui', 'ncasgui', 'The full-screen mode.',
        'Modelled on the CAS Calculator app: type on the entry line at the bottom, press enter, '
        'and the input (left) and result (right) go into the history, drawn in 2D. The status '
        'bar shows the angle unit, the mode and real/complex, or the syntax of the command you are typing.')
card('Type and evaluate', 'Type a command with TI’s name and syntax and press enter. Results are exact unless you type a decimal.',
     'solve(x^2-5x+6=0,x) [enter] 1/3+1/6+sqrt(8) [enter]')
card('Continue from the last answer', 'An operator typed on an empty line starts with ans, as on the CAS.',
     '* 3 [enter]', pre=['2^10'])
card('Reuse an earlier entry', '▲ and ▼ select earlier inputs and results; enter copies the selected one to the entry line.',
     '[▲] [▲]', pre=['factor(x^2-1)', 'expand((x+1)^3)'])
card('See the syntax while you type', 'Inside a command’s brackets the status bar shows how to call it.',
     'integral(x*sin(x)')
card('Command menus', 'menu opens eight groups of commands. Pick with the arrows and enter, or the number or letter shown.',
     '[menu] [2]')
card('A menu fills in the command', 'The command goes on the line with the cursor where the first value belongs; tab jumps to the next argument.',
     '[menu] [2] [1] sin(x)^2')
card('Catalog A–Z', 'Every command with its syntax under the list. Type a letter to jump; enter puts name() on the line.',
     '[catalog] [t]')
card('Trig functions', 'The trig key lists sin, cos, tan, their inverses, hyperbolic functions, sec, csc and cot.',
     '[trig] [1] pi/6 [enter]')
card('Decimal answer', 'ctrl enter gives the decimal value of the line (or of the last answer).',
     'pi/7 [ctrl] [enter]')
card('Your variables', 'var lists ans and every variable and function you stored, with its value. Pick one to type its name.',
     '[var]', pre=['a:=5', 'm:=[1,2;3,4]', 'f(x):=x^2+1'])
card('ctrl keys at a glance', 'ctrl trig shows what each blue ctrl label does in nCAS.',
     '[ctrl] [trig]')
card('Settings', 'Degree/radian, Auto/Exact/Approx, real/complex, digits, variables, self-test, memory and the key test.',
     '[menu] [8]')

# ---- 2D entry
section('entry', 'ncasgui · 2D entry', 'Fractions, powers, roots and calculus, as templates.',
        'The entry line is 2D: templates have slots you type into. ◄ ► move through the slots, '
        '▲ ▼ move between numerator and denominator or between the limits, and tab jumps to the next empty field.')
card('Fraction', 'ctrl ÷ opens a fraction. ▼ goes to the denominator, ► leaves it.',
     '[ctrl] [÷] 1 [▼] 3 [►] +1/6 [enter]')
card('Powers', '^ opens an exponent. Typing + − × ÷ = , or ) at its end leaves it automatically.',
     'factor(x [^] 3 -8) [enter]')
card('Square and n-th roots', 'ctrl x² is √, ctrl ^ is the n-th root (the index first, then ► to the radicand).',
     '[ctrl] [x²] 12 [►] [enter] [ctrl] [^] 4 [►] 81 [enter]')
card('Indefinite integral', 'menu ▸ 9 Templates ▸ a. The variable slot starts as x.',
     '[menu] [9] [a] x*e [^] 2x [►] [►] [enter]')
card('Definite integral', 'Limits in their own slots: ▲ moves from the lower limit to the upper one.',
     '[menu] [9] [b] 0 [▲] pi [►] sin(x) [enter]')
card('Derivative d/dx', 'menu ▸ 9 Templates ▸ c. The cursor starts in the function; the variable is x.',
     '[menu] [9] [c] x [^] 3 [►] *sin(x) [enter]')
card('Brackets step over', 'A function key types both brackets. Typing ) where one already is steps over it, so typing out sin(x) never leaves an extra one.',
     '[sin] x ) +1 [enter]')
card('Brackets close at enter', 'Brackets you leave open are closed when you press enter, as on the CAS.',
     'factor(x [^] 2 -1 [enter]')
card('Start or end of the line', 'ctrl ◄ jumps to the start of the line and ctrl ► to the end, from anywhere, even inside a template.',
     '2+3 [ctrl] [◄] 1 [ctrl] [►] 0 [enter]')
card('A word at a time', 'shift ◄ ► move over a whole name, number or template: sin( is one step.',
     'sin(x)+cos(y) [shift] [◄] [shift] [◄] [shift] [◄] 2*')
card('Matrix grid', 'Templates ▸ Matrix m×n: choose the size (up to 9×9), type in the cells, tab or arrows to move, enter to put it on the line.',
     '[menu] [9] [1] [enter] 8 [tab] 5 [tab] 7 [tab] 9')
card('Edit a matrix on the line', 'The matrix stays a grid on the entry line. ◄ ► go through the cells, ▲ ▼ up and down; typing , or ; at the end of a cell goes to the next cell or row; ] or ) leaves the matrix.',
     '[menu] [9] [1] [enter] 1 [tab] 2 [tab] 3 [tab] 4 [enter] [◄] [▲]')
card('Matrix commands', 'A matrix item puts the brackets on the line; the matrix template then fills them.',
     '[menu] [4] [7] [menu] [9] [1] [enter] 8 [tab] 5 [tab] 7 [tab] 9 [enter] [enter]')
card('Symbols', 'menu ▸ a Symbols: 40 characters that cannot be typed while a program runs (; [ ] { } | := → ≠ ≤ ≥ ° …).',
     '[menu] [a]')
card('“with” and relations', 'ctrl = lists ≠ ≤ ≥ | and >>. Here | substitutes a value.',
     'x [^] 2 [►] +1 [ctrl] [=] [7] x=3 [enter]')
card('Define a function', 'f(x):=… (or Define f(x)=…) defines a function; it is saved in the document.',
     'f(x):=x [^] 2 [►] +1 [enter] f(3) [enter]')
card('Solve with a condition', 'A condition after | restricts the solutions; in degree mode angles are in degrees.',
     'solve(sin(x)=1/2,x)|0<=x<=360 [enter]', pre=[':deg'])
html('''<h3 class="sub">Keys in the full-screen mode</h3>
<div class="table-wrap"><table class="plain keys2">
<thead><tr><th>Key</th><th>Action</th></tr></thead><tbody>
<tr><td><span class="kc">enter</span></td><td>evaluate the line; on a selected history item, copy it to the line</td></tr>
<tr><td><span class="kc">◄</span> <span class="kc">►</span></td><td>move the cursor (through template slots too)</td></tr>
<tr><td><span class="kc">ctrl</span> <span class="kc">◄</span> <span class="kc">►</span></td><td>start · end of the line</td></tr>
<tr><td><span class="kc">shift</span> <span class="kc">◄</span> <span class="kc">►</span></td><td>a whole name, number or template at a time</td></tr>
<tr><td><span class="kc">)</span> <span class="kc">]</span> <span class="kc">}</span></td><td>step over a closing bracket that is already there; open brackets close at enter</td></tr>
<tr><td><span class="kc">var</span></td><td>list ans, your variables and functions; enter types the name</td></tr>
<tr><td><span class="kc">▲</span> <span class="kc">▼</span></td><td>between template slots; otherwise select earlier inputs and results (a tall result scrolls first)</td></tr>
<tr><td><span class="kc">del</span> · <span class="kc">clear</span></td><td>delete to the left · clear the line</td></tr>
<tr><td><span class="kc">tab</span> · <span class="kc">shift</span> <span class="kc">tab</span></td><td>next · previous field (template slots, arguments after commas)</td></tr>
<tr><td><span class="kc">menu</span></td><td>command menus, Templates (9) and Symbols (a)</td></tr>
<tr><td><span class="kc">catalog</span></td><td>every command A–Z with its syntax</td></tr>
<tr><td><span class="kc">trig</span></td><td>trig and hyperbolic functions</td></tr>
<tr><td><span class="kc">esc</span></td><td>leave the selection · clear the line · quit (on an empty line)</td></tr>
</tbody></table></div>
<h3 class="sub">ctrl functions (the blue labels)</h3>
<div class="table-wrap"><table class="plain keys2">
<thead><tr><th>ctrl +</th><th>gives</th><th>ctrl +</th><th>gives</th></tr></thead><tbody>
<tr><td><span class="kc">(</span></td><td><code>[ ]</code></td><td><span class="kc">)</span></td><td><code>{ }</code></td></tr>
<tr><td><span class="kc">^</span></td><td>n-th root</td><td><span class="kc">x²</span></td><td>√</td></tr>
<tr><td><span class="kc">e<sup>x</sup></span></td><td><code>ln()</code></td><td><span class="kc">10<sup>x</sup></span></td><td><code>log10()</code></td></tr>
<tr><td><span class="kc">=</span></td><td>≠ ≤ ≥ | &gt;&gt; list</td><td><span class="kc">(−)</span></td><td><code>ans</code></td></tr>
<tr><td><span class="kc">×</span></td><td><code>" "</code></td><td><span class="kc">÷</span></td><td>fraction</td></tr>
<tr><td><span class="kc">var</span></td><td><code>-&gt;</code> store</td><td><span class="kc">enter</span></td><td>≈ decimal</td></tr>
<tr><td><span class="kc">del</span></td><td>clear the line</td><td><span class="kc">esc</span></td><td>undo</td></tr>
<tr><td><span class="kc">◄</span></td><td>start of the line</td><td><span class="kc">►</span></td><td>end of the line</td></tr>
<tr><td><span class="kc">catalog</span></td><td>Symbols page</td><td><span class="kc">trig</span></td><td>this help</td></tr>
</tbody></table></div>
<p class="fine">If the calculator reports ctrl as its own key, press ctrl then the key; <b>doc</b> also works as ctrl. A key nCAS does not use is named in the status bar.</p>''')

# ---- typing rules
section('syntax', 'Typing math', 'Syntax and commands, the same in every program.',
        'Command names and arguments follow the TI-Nspire CAS Reference Guide, and names are case-insensitive. '
        'These rules hold in ncasgui, ncastext and (for arithmetic) ncasx.')
html('''<div class="table-wrap"><table class="plain">
<thead><tr><th>You type</th><th>Meaning</th></tr></thead><tbody>
<tr><td class="in">2x  3(x+1)  x(x+1)</td><td>implicit multiplication</td></tr>
<tr><td class="in">x^2  x**2</td><td>power</td></tr>
<tr><td class="in">sqrt(x)  √x  root(x,3)</td><td>roots</td></tr>
<tr><td class="in">pi  e  i  inf</td><td>π, Euler’s e, the imaginary unit, ∞ (<code>e</code> and <code>i</code> are reserved)</td></tr>
<tr><td class="in">ln(x)  log(x)</td><td>natural log (the ln key types <code>log(</code>)</td></tr>
<tr><td class="in">log10(x)  log(x,b)</td><td>base-10 and base-b logs</td></tr>
<tr><td class="in">= /= &lt; &gt; &lt;= &gt;= and or not</td><td>relations and logic</td></tr>
<tr><td class="in">expr|x=3  expr|x&gt;0</td><td>“with”: substitute or add a condition</td></tr>
<tr><td class="in">f(x):=x^2  Define f(x)=x^2</td><td>define a function</td></tr>
<tr><td class="in">5-&gt;a  a:=5  delvar a</td><td>store and delete a variable</td></tr>
<tr><td class="in">expr&gt;&gt;Decimal</td><td>conversion ► (also <code>@&gt;</code>)</td></tr>
<tr><td class="in">ans</td><td>the last result</td></tr>
<tr><td class="in">{1,2,3}</td><td>list</td></tr>
<tr><td class="in">[1,2;3,4]  [[1,2][3,4]]</td><td>matrix</td></tr>
<tr><td class="in">1.5E3</td><td>scientific notation</td></tr>
<tr><td class="in">y'  y''</td><td>derivatives inside <code>deSolve</code></td></tr>
</tbody></table></div>
<h3 class="sub">Commands that start with a colon</h3>
<div class="table-wrap"><table class="plain">
<thead><tr><th>Command</th><th>Does</th></tr></thead><tbody>
<tr><td class="in">:deg  :rad  :grad</td><td>angle unit</td></tr>
<tr><td class="in">:auto  :exact  :approx</td><td>Auto (exact unless a decimal is typed), Exact, Approximate</td></tr>
<tr><td class="in">:real  :complex</td><td>real or complex results</td></tr>
<tr><td class="in">:digits n</td><td>significant digits shown for decimals (1–15)</td></tr>
<tr><td class="in">:vars  :clear</td><td>show · delete your variables and functions</td></tr>
<tr><td class="in">:clearans  :clearhist  :free</td><td>reset ans · clear history and undo · both, to free memory</td></tr>
<tr><td class="in">:test  :mem  :keys</td><td>self-test · memory in use · key test</td></tr>
<tr><td class="in">:ascii  :unicode</td><td>plain or symbol output (text mode)</td></tr>
</tbody></table></div>''')

# ---- ncastext
section('text', 'ncastext', 'The command line in the Python Shell.',
        'Type a command at the <code>&gt;</code> prompt and press enter. <code>m</code> opens numbered menus that '
        'build the command for you, <code>?</code> shows help, <code>q</code> quits. The prompt shows settings that '
        'differ from the defaults, such as <code>deg&gt;</code>.')
term('Commands at the prompt', 'The same commands and results as the full-screen mode, as text.',
     ['factor(x^4-16)', 'integral(x*e^(2x),x)', 'solve(x^2-4>0,x)', '[1,2;3,4]^-1'])
term('Settings and the prompt', 'A setting changes the prompt, so you always see the mode you are in.',
     [':deg', 'solve(sin(x)=1/2,x)|0<=x<=360', ':rad'])
term('Variables and functions', 'Definitions are saved in the document and come back the next time you run the program.',
     ['f(x):=x^2+1', 'f(3)', '5->a', 'a^2', 'd(f(x)*a,x)'])
term('Help', '<code>?</code> lists the help topics; <code>?name</code> shows a command’s syntax.',
     ['?integral', '?with'])
html('''<h3 class="sub">Menu mode</h3>
<p class="body">At the prompt type <code>m</code>. Pick items by number or letter and answer the questions; enter accepts the default in brackets, <code>0</code> goes back and <code>q</code> leaves. nCAS shows the command it built and runs it.</p>
<div class="term">-- nCAS menu --
1 Algebra       2 Calculus
3 Solve         4 Matrix
5 Number/cplx   6 Lists/stats
7 Convert       8 Settings
<span class="p">#:</span> 2
-- Calculus --
1 Derivative    2 Deriv at pt
3 Integral      4 Def integral  ...
<span class="p">#:</span> 4
<span class="p">f:</span> e^(-x)
<span class="p">Var [x]:</span>
<span class="p">Lower (inf ok):</span> 0
<span class="p">Upper:</span> inf
<span class="p">&gt;</span> integral(e^(-x),x,0,inf)
<span class="r">1</span></div>
<p class="fine">Matrices can be typed as <code>1,2;3,4</code> in the menus. From the Shell, <code>cas()</code> restarts the text mode and <code>gui()</code> opens the full-screen mode.</p>''')

# ---- ncasx
section('x', 'ncasx', 'A small exact calculator.',
        'Type an expression and get the exact value, with its decimal when they differ. No menus and no modes; '
        'it loads three times faster than the full CAS. <code>q</code> quits.')
term('Exact values', 'Radicals, fractions and big integers stay exact.',
     ['1/(1+sqrt(2))', 'sin(pi/12)', '2^100', 'nCr(52,5)', 'factor(2024)'], prog='x')
term('Variables and relations', 'Store with := or ->; a relation gives true or false.',
     ['r:=3', 'pi*r^2', 'sqrt(2)^2=2', 'mod(7^222,10)'], prog='x')

# ---- navcalc
section('nav', 'navcalc', 'Aviation calculator (E6B).',
        'Pick a tool. Each tool is a form: type the values you know and leave the others blank; the blank '
        'fields (?) are solved as you type, in blue. Any field can be the blank one. A value can be a sum '
        'such as <code>120+15</code>, and ◄ ► change a field’s unit.')
card('The tools', 'Arrows and enter, or the number. Units has speed, distance, altitude, temperature, pressure, fuel and fuel flow.',
     '', prog=NAV)
card('Wind triangle', 'Course, airspeed and wind give heading, ground speed and the wind correction angle.',
     '[1] 90 [enter] 120 [enter] 360 [enter] 20', prog=NAV)
card('Change a unit', '◄ ► on a field cycle its unit; the value is converted.',
     '[1] 90 [enter] 120 [enter] 360 [enter] 20 [▼] [▼] [►]', prog=NAV)
card('Time, speed, distance', 'Times are h:mm (1:30) or minutes. Leave the one you want blank.',
     '[3] 120 [▼] [▼] 1:30', prog=NAV)
card('Sums in a field', 'Add the legs of a route in the distance field: the total is used.',
     '[3] 120 [▼] 45+38+52', prog=NAV)
card('Crosswind', 'Runway 27 means 270°. Crosswind + is from the right.',
     '[2] 27 [enter] 300 [enter] 15', prog=NAV)
card('Density altitude', 'Indicated altitude, altimeter setting and temperature give pressure and density altitude.',
     '[5] 5000 [enter] 29.92 [enter] 30', prog=NAV)
html('''<p class="fine">Keys: <b>▲ ▼ tab enter</b> move between fields, <b>◄ ►</b> change the unit, <b>del</b> deletes, <b>clear</b> blanks a field, <b>(−)</b> changes the sign, <b>esc</b>/<b>menu</b> back to the list. The status bar says what is missing (“enter 1 more value”, “too many values: clear 1”, “no solution”). ICAO standard atmosphere; for planning and training, not a certified instrument.</p>''')

# ---- unitconv
section('unit', 'unitconv', 'Unit converter.',
        'Pick a category: every unit in it is listed. Type a value in any row and all the other rows convert as you '
        'type. The typed row is black with the cursor; converted values are blue; the status bar shows the selected '
        'row to 12 digits.')
card('Categories', 'Length, area, volume, mass, temperature, time, speed, pressure, energy, power, force, angle, data size, fuel economy, density, frequency.',
     '', prog=UNIT)
card('Type in any row', 'Here 1 mile: every length unit at once.',
     '[1] [▼] [▼] [▼] [▼] [▼] [▼] 1', prog=UNIT)
card('Sums', 'A value can be a sum: 5 ft 7 in typed as inches.',
     '[1] [▼] [▼] [▼] 5*12+7', prog=UNIT)
card('Negative values', '(−) changes the sign: −40 is the same in °C and °F.',
     '[5] [clear] [(−)] 40', prog=UNIT)
card('Edit a converted value', 'del on a blue row copies its value for editing; that row becomes the typed one.',
     '[1] [▼] [▼] [▼] [▼] [▼] [▼] 1 [▼] [del] [del]', prog=UNIT)
html('''<p class="fine">Keys: <b>▲ ▼ tab enter</b> move, <b>◄ ►</b> page up/down, <b>del</b> deletes, <b>clear</b> empties the row, <b>EE</b> exponent (1.5E6), <b>?</b> help, <b>esc</b>/<b>menu</b> back to the categories. Factors are the exact definitions.</p>''')

# ---- troubleshooting
section('help', 'Troubleshooting', 'When something does not work.',
        'Most problems on a real calculator come from key names, memory, or a paste that went wrong.')
card('Key test', 'Settings ▸ Key test shows the name of every key you press (esc twice to stop). Send those names if a key does nothing.',
     '[menu] [8] [f] [x]')
html('''<div class="faq">
<div><h3>“key … not used”</h3><p>The status bar names a key nCAS does not use. Open the key test, note the name, and report it on GitHub.</p></div>
<div><h3>Out of memory</h3><p>nCAS shortens the history and keeps going; your variables stay. <code>:free</code> clears history, undo and ans. Very large requests stop at once with “Resource limit”.</p></div>
<div><h3>The program does not start</h3><p>Turn Press-to-Test off. If the full-screen mode cannot read keys on an older OS, ncasgui opens a compact screen mode in the Shell instead (type, <code>m</code> for menus, <code>q</code> quits).</p></div>
<div><h3>Syntax error after pasting</h3><p>A part was pasted twice or missed. Compare the line count with what <code>paste_parts.py</code> printed, or start a new program and paste again.</p></div>
<div><h3>A long calculation</h3><p>Exact big-integer work cannot be interrupted on the calculator, so nCAS refuses huge powers and factorials up front instead of freezing.</p></div>
<div><h3>Report a problem</h3><p>Open an issue on <a href="https://github.com/truthadmire/ncas-for-ti-nspire/issues" target="_blank" rel="noopener">GitHub</a> with the input, what you saw, and a photo if the screen looks wrong.</p></div>
</div>''')

# ---- reference (filled from cashelp)
section('ref', 'Reference', 'Every command.',
        'Grouped as in the catalog. Commands with a syntax line show it; the rest take the arguments you would expect. '
        'In ncasgui the catalog shows the same lines; in the text programs type <code>?name</code>.')

# --------------------------------------------------------------- running
RUNNER = r'''
import sys, json
sys.path.insert(0, 'tests/mock'); sys.path.insert(0, 'src')
import ti_system, ti_draw
prog, pre, K = json.loads(sys.argv[1])
last = [[]]
cur = [[]]
paint = ti_draw.paint_buffer
def grab():
    cur[0] = list(ti_draw._ops)
    paint()
ti_draw.paint_buffer = grab
def get_key(wait=0):
    while ti_system.HOOK:
        ti_system.HOOK.pop(0)()
    if ti_system.KEYS:
        return ti_system.KEYS.pop(0)
    last[0] = cur[0]          # the screen after the last key
    raise KeyboardInterrupt()
ti_system.get_key = get_key
keys = []
for e in pre:
    keys += list(e) + ['enter']
ti_system.KEYS[:] = keys + K
if prog == 'gui':
    import cas
    try:
        cas.gui()
    except KeyboardInterrupt:
        pass
elif prog == 'nav':
    import navcalc
    navcalc.navcalc()
else:
    import unitconv
    unitconv.unitconv()
print(json.dumps(last[0]))
'''

TEXTRUN = r'''
import sys, json
sys.path.insert(0, 'src')
prog, lines = json.loads(sys.argv[1])
out = []
if prog == 'x':
    import casx
    for s in lines:
        p = 'deg> ' if casx.ST['deg'] else '> '
        out.append([p, s, casx.run(s)])
else:
    import cas
    for s in lines:
        p = cas.prompt()
        try:
            r = cas.run(s)
        except Exception as ex:
            r = 'Error: ' + str(ex)
        out.append([p, s, r])
print(json.dumps(out))
'''


def run(code, arg):
    r = subprocess.run([sys.executable, '-c', code, json.dumps(arg)], capture_output=True,
                       text=True, cwd=ROOT)
    if r.returncode:
        sys.stderr.write(r.stderr)
        raise SystemExit('example failed: %r' % (arg,))
    return json.loads(r.stdout)


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')


def rgb(c):
    return '#%02x%02x%02x' % tuple(c)


def svg(ops, label):
    out = []
    for o in ops:
        if o[0] == 'rect':
            out.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>' % (o[1], o[2], o[3], o[4], rgb(o[5])))
        elif o[0] == 'line':
            out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s"/>' % (o[1], o[2], o[3], o[4], rgb(o[5])))
        elif o[0] == 'text':
            out.append('<text x="%d" y="%d" fill="%s">%s</text>' % (o[1], o[2], rgb(o[4]), esc(o[3])))
    body = ''.join(out)
    return ('<svg class="mini" viewBox="0 0 318 212" role="img" aria-label="%s"><g class="scr" xml:space="preserve">%s</g></svg>'
            % (esc(label), body))


def strokes(show):
    out = []
    for kind, t in show:
        out.append('<span class="kc%s">%s</span>' % (' ty' if kind == 't' else '', esc(t)))
    return '<div class="strokes" aria-label="Keys">%s</div>' % ''.join(out)


def reference():
    sys.path.insert(0, os.path.join(ROOT, 'src'))
    import cashelp
    from casout import TINAME
    parts = ['<div class="ref">']
    for key, title, words in cashelp.CATS:
        if key == 'cmd':
            continue
        rows = []
        for w in words.split():
            name = TINAME.get(w.lower(), w) if w[0].isalpha() else w
            syn = cashelp.SYN.get(w.lower())
            rows.append('<li><code>%s</code>%s</li>' % (
                esc(name), ('<span>' + esc(syn).replace('\n', '<br>') + '</span>') if syn else ''))
        parts.append('<div class="refcat"><h3>%s <small>%d</small></h3><ul>%s</ul></div>'
                     % (esc(title), len(rows), ''.join(rows)))
    parts.append('</div>')
    return ''.join(parts)


def build():
    toc = []
    body = []
    for sec in SECTIONS:
        toc.append('<a href="#%s">%s</a>' % (sec['id'], esc(sec['eyebrow'])))
        b = ['<section id="%s"><div class="sec-head"><p class="eyebrow">%s</p><h2>%s</h2><p>%s</p></div>'
             % (sec['id'], esc(sec['eyebrow']), esc(sec['title']), sec['intro'])]
        figs = []

        def flush():
            if figs:
                b.append('<div class="cards">' + ''.join(figs) + '</div>')
                del figs[:]
        for it in sec['items']:
            if it['kind'] == 'html':
                flush()
                b.append(it['html'])
            elif it['kind'] == 'card':
                K, show = keys(it['k'])
                ops = run(RUNNER, [it['prog'], it['pre'], K])
                pre = ''
                if it['pre']:
                    pre = '<p class="pre">Before: <code>%s</code></p>' % esc('</code>, <code>'.join(it['pre']))
                figs.append('<figure>%s<figcaption><h3>%s</h3><p class="what">%s</p>%s%s</figcaption></figure>'
                            % (svg(ops, it['title']), esc(it['title']), esc(it['what']), pre,
                               strokes(show) if show else ''))
                sys.stdout.write('.')
                sys.stdout.flush()
            else:
                rows = run(TEXTRUN, [it['prog'], it['lines']])
                t = []
                for p, s, r in rows:
                    t.append('<span class="p">%s</span>%s\n<span class="r">%s</span>' % (esc(p), esc(s), esc(r)))
                figs.append('<figure class="tfig"><div class="term">%s</div><figcaption><h3>%s</h3><p class="what">%s</p></figcaption></figure>'
                            % ('\n'.join(t), esc(it['title']), it['what']))
        flush()
        if sec['id'] == 'ref':
            b.append(reference())
        b.append('</section>')
        body.append(''.join(b))
    page = TEMPLATE.replace('__TOC__', '\n'.join(toc)).replace('__BODY__', '\n'.join(body))
    with open(OUT, 'w') as f:
        f.write(page)
    print('\nwrote %s (%d KB)' % (OUT, len(page) // 1024))


TEMPLATE = open(os.path.join(ROOT, 'tools', 'guide_template.html')).read()

if __name__ == '__main__':
    build()
