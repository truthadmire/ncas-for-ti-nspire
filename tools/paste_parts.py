# paste_parts.py - put a large file on the Mac clipboard in parts, for editors
# that refuse a large paste (the TI-Nspire Python editor).
#   python3 tools/paste_parts.py [file] [part size in characters] [first part]
# (give a first part to carry on after an interruption)
# Every part after the first starts with the line break that ends the previous
# part, so pasting the parts one after another at the end of the program
# rebuilds the file exactly, even if the editor drops a trailing line break.
import os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'onefile', 'ncastext.py')
size = int(sys.argv[2]) if len(sys.argv) > 2 else 40000
first = int(sys.argv[3]) if len(sys.argv) > 3 else 1

def copy(part):
    # the clipboard: pbcopy (macOS), clip (Windows), wl-copy / xclip /
    # xsel (Linux); without any of them each part is written to a file
    for cmd in (['pbcopy'], ['clip'], ['wl-copy'], ['xclip', '-selection', 'clipboard'],
                ['xsel', '--clipboard', '--input']):
        try:
            subprocess.run(cmd, input=part.encode('ascii'), check=True,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return
        except (OSError, subprocess.CalledProcessError):
            continue
    name = '%s.part%d.txt' % (path[:-3], i)
    with open(name, 'w', newline='\n') as f:
        f.write(part)
    print('(no clipboard tool found: open %s, select all and copy it)' % name)

text = open(path).read().rstrip('\n')
parts = []
a = 0
while a < len(text):
    b = len(text)
    if b - a > size:
        b = text.rfind('\n', a + 1, a + size)
        if b <= a:
            raise SystemExit('a line is longer than the part size')
    parts.append(text[a:b])
    a = b
assert ''.join(parts) == text

print('%s: %d characters, %d lines, %d parts' % (os.path.basename(path), len(text),
                                                  text.count('\n') + 1, len(parts)))
print('Make a new Python program named %s (blank), then paste each part at the'
      % os.path.basename(path)[:-3])
print('very end of the program. Do not click elsewhere between pastes.')
done = 0
for i, p in enumerate(parts, 1):
    if i < first:
        done += len(p)
        continue
    copy(p)
    done += len(p)
    last = p[p.rfind('\n') + 1:]
    print()
    print('Part %d of %d is on the clipboard (%d characters).' % (i, len(parts), len(p)))
    print('After pasting, the program should have %d lines and end with:'
          % (text.count('\n', 0, done) + 1))
    print('  ' + last.strip()[:70])
    if i < len(parts):
        try:
            input('Paste it, then press Enter here for the next part... ')
        except (EOFError, KeyboardInterrupt):
            print()
            raise SystemExit('Stopped.')
print()
print('That was the last part. The program should end with: ' + text[text.rfind('\n') + 1:].strip())
print('Now use Check Syntax & Save, and save the document as %s.tns.'
      % os.path.basename(path)[:-3])
