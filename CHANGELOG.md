# Changelog

## 1.1

Wrong answers fixed:
- `solve` with inequalities joined by `and`, chained inequalities (`1<2x+1<7`)
  and lists of inequalities no longer return `false`; `|` conditions now apply
  to inequalities too (`solve(x^2<9,x)|x>0` gives `0<x<3`). Unions are merged
  (`solve(x>1 or x<3,x)` gives `true`).
- `piecewise(e1,c1,e2,c2)` (the template form) no longer gives `undef`;
  piecewise functions integrate, take limits and solve exactly.
- Divergent integrals give `undef`, `∞` or `-∞` instead of a number
  (`integral(1/x,x,-1,1)`, `integral(tan(x),x,0,pi)`); poles of tan, sec and
  transcendental denominators are found. Numeric integrals that do not
  converge report "Questionable accuracy" instead of a wrong value;
  oscillatory integrals such as `integral(sin(x)/x,x,0,inf)` are extrapolated.
- Substitutions no longer lose the sign for x<0 (`integral(x^2/sqrt(9-x^2),x,-3,3)`
  gave 0, now 9π/2); trigonometric substitution for sqrt(a²−x²), sqrt(x²+a²),
  sqrt(x²−a²); definite integrals split at |…| sign changes.
- Limits: factorials (`limit(n!/2^n,n,inf)`), floor/ceiling one-sided limits,
  squeeze cases (`limit(x*sin(1/x),x,0)`), exponential vs power, and
  `limit(1/ln(x),x,inf)` (was ∞, now 0).
- Infinite series: divergence test, alternating series by extrapolation and
  Euler–Maclaurin tail for positive terms (`sumSeq(1/k^1.5,k,1,inf)` is now
  correct to 10 digits; `sumSeq(1/sqrt(k),k,1,inf)` gives ∞).
- Exact constants that agree to 12 digits compare equal (`ln(8)/ln(2)=3` is
  `true`); identities such as `(x+1)^2=x^2+2x+1` give `true`.
- `solve(sin(x)*cos(x)=1/4,x)` and similar trig products are solved exactly.
- Absolute-value equations are solved by sign cases: exact roots and whole
  intervals (`solve(abs(x)+abs(x-2)=2,x)` gives `0≤x≤2`).
- `fMax`/`fMin`/`nfMax`/`nfMin` of unbounded functions give ±∞ instead of
  every critical point.
- `eigVl` lists repeated eigenvalues and accepts letters; decimal matrices
  with repeated eigenvalues give clean results.

New:
- Integrals of sec^n and csc^n, sec·tan, csc·cot, rational functions of sin
  and cos (tan(x/2) substitution, with the jump at x=π handled in definite
  integrals), sinh² and cosh², 1/(x⁴+1) and other quartics without real roots.
- Inequalities with a letter coefficient: `solve(a*x<5,x)` gives one answer
  for each sign of `a`.
- Settings, variables and functions are kept in the document (list variable
  `ncasmem`) and come back after Ctrl+R or reopening the document.
- Full-screen mode: the command syntax shows in the status bar while typing
  its arguments and under the catalog list; results taller than the screen
  scroll line by line.
- Wrong-number-of-arguments errors name the command and show its syntax;
  near-miss names get a hint (`factr` → did you mean factor?); `diff`,
  `deriv`, `integrate`, `avg` and `cbrt` are accepted.
- Text mode prompt shows the active modes (`deg approx> `).

Fixes:
- The module install no longer crashes when `casgui.py` is missing (it falls
  back to text mode); the launcher checks `casgui` too.
- `gui()` and `menu()` typed in the Shell work in the single-file builds.
- Lower memory use: the numeric root scan no longer builds large lists, so
  the self-test passes with a 0.7 MB (ncastext) or 0.9 MB (ncasgui) heap.
- Huge exact roots (`1000000^(101/100)`) no longer stall.
- `tools/paste_parts.py` works on Windows and Linux (clip, wl-copy, xclip,
  xsel, or part files) and names the right document.

## 1.0

First release.
