#!/usr/bin/env python3
"""Check the README's ASCII comic renders the same everywhere.

A panel is a file in docs/comic/panels/. Each must be 7-bit ASCII, tab-free,
at most WIDTH columns (a phone-width GitHub code block, about 36; FIG_WIDTH for the
figure panels render.py draws through chafa), and appear
verbatim in README.md inside a ```text fence. Every ```text fence in the README
must be one of the panels, so the panels are the source and the README a copy.
"""
import re
import sys
from pathlib import Path

WIDTH = 36          # a narrative panel: fits a phone
FIG_WIDTH = 72      # a figure panel (*-fig.txt, from render.py): scrolls on a phone
root = Path(__file__).resolve().parents[2]
panels_dir = root / "docs" / "comic" / "panels"
readme = (root / "README.md").read_text()
fences = re.findall(r"^```text\n(.*?)\n```$", readme, re.S | re.M)
errors = []

panels = {}
for p in sorted(panels_dir.glob("*.txt")):
    text = p.read_text().rstrip("\n")
    panels[p.name] = text
    for n, line in enumerate(text.split("\n"), 1):
        if any(ord(c) > 126 or (ord(c) < 32) for c in line):
            errors.append("%s:%d: not 7-bit printable ASCII" % (p.name, n))
        limit = FIG_WIDTH if p.name.endswith("-fig.txt") else WIDTH
        if len(line) > limit:
            errors.append("%s:%d: %d columns, limit %d" % (p.name, n, len(line), limit))
        if line != line.rstrip():
            errors.append("%s:%d: trailing space" % (p.name, n))
    if text not in fences:
        errors.append("%s: not in README.md as a ```text fence" % p.name)

for i, f in enumerate(fences, 1):
    if f not in panels.values():
        errors.append("README.md: ```text fence %d is not a panel file" % i)

for e in errors:
    print(e)
print("%d panels, %d text fences: %s" % (len(panels), len(fences), "clean" if not errors else "%d errors" % len(errors)))
sys.exit(1 if errors else 0)
