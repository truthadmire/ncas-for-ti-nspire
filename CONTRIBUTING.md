# Contributing

Reports from real calculators are the most useful contribution: open an issue
with the **Report from a calculator** form. It asks for the OS version, the
program, the exact input and output, and the `:test` / `:mem` results.

## Changing the code

- Edit only `src/`. `dist/` (minified modules) and `onefile/` (the paste-in
  programs) are generated:

  ```
  python3 tools/build.py
  python3 tools/onefile.py
  ```

  Commit the regenerated files together with the source; CI checks they match.
- The calculator runs MicroPython with about 2 MB of heap: no `str.isalnum`,
  no `signal`, no `random.Random`, no file I/O. Avoid backslash line
  continuations (the minifier does not handle them) and very large exact
  integers (big-integer arithmetic cannot be interrupted on the calculator).
- Run the tests from the repository root:

  ```
  python3 tests/check.py src
  micropython -X heapsize=2000000 tests/check.py dist
  python3 tests/menu_items.py
  python3 tests/gui_check.py
  python3 tests/cursor_check.py
  python3 tests/verify.py
  ```

  Every test script exits with status 1 when something fails. If an output
  change is intended, review it and run `python3 tests/check.py src --update`.
- `python3 tools/shots.py` redraws the README pictures in `docs/img/`.
