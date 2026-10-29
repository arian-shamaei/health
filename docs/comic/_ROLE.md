# docs/comic

The README's ASCII comic. `panels/NN-name.txt` are the source, one panel per file; the README
carries each one verbatim inside a ```text fence. `lint.py` proves the copy matches and that
every panel renders the same in every Markdown renderer and terminal.

## The contract (why it renders everywhere)

- Only a fenced code block keeps whitespace and a monospace font in every renderer: GitHub,
  GitLab, pandoc, VS Code, `cat`. `<pre>` and HTML tables do not survive a terminal.
- 7-bit ASCII only. Every monospace font has every glyph at the same width. Box drawing,
  Braille and emoji fall back to other fonts and break alignment.
- No tabs (width varies), no trailing spaces (editors strip them).
- At most 36 columns per panel: a GitHub code block on a phone shows about that before it
  scrolls sideways. A terminal shows 80, GitHub on a desktop about 110, so panels are never
  placed side by side; they stack. The comic reads top to bottom, and the vertical order is
  the time axis.
- ASCII cannot reflow, so the panel is the unit of layout. Markdown stacks the fences at any
  width; that is the only "responsive" behaviour that exists everywhere.
- The character is nyan's cat, in its own face vocabulary (`~/Developer/cat/notes/
  personality.md`): eyes carry the fact, mouth the feeling, arms the action. It never speaks
  a word; words beside it are the narrator's.
- The tool's figure is never drawn by hand (a mock). The strip's figures are real `health --png`
  frames converted to ASCII by chafa (`render.py`: 3x6 px per cell so the 2-px trace stays
  thick, `--symbols ascii-alnum -c none`, hour 0 for the 2:3 family), composed into the
  panels of `storyboard.md` with the cat, bubbles and sounds stamped on top. 72 columns scrolls on a phone; 36 was
  too coarse for a curve. The lint allows 72 for `*-fig.txt` only.
- Backslashes, `<`, `>`, `*` and `_` are safe inside a fence and unsafe outside one.

Verified 2026-10-27: GitHub's renderer (`gh api /markdown`) and pandoc both return a ```text
fence byte for byte, including `\_/\` and `> ^ <`.

## PNG mode (2026-10-28, the current README)

`render.py` has `MODE = "png"`: the story page and the mapping panel are images
(`docs/assets/story.png`, `docs/assets/mapping.png`), each a black page with the real
`health --png` frames pasted into their regions and every other cell of the same text layout
drawn in Menlo on top; frame characters become solid lines, text over a figure gets a black
cell behind it. Pillow, docs only. The manual (install, use, origin) stays a ```text fence so
its commands can be copied. `MODE = "ascii"` gives the all-text version back. The reason:
chafa's ASCII figures read as noise beside the real thing, and once the figures are images the
page can be one image with no gaps between tiers.

## The mascot (2026-10-28)

`nyan.py` draws the cat as pixel art: a black cat (charcoal coat, grey rim so it reads on
the black page, light whiskers, rosy cheeks) with amber eyes a shade apart, left lighter
than right; one head whose 3x3 eyes carry the state (`o_o -_- ^_^ >_< x_x zzz`, the cat workspace's vocabulary), on a
body per pose: sit, reach and point (one paw up, left or right), type (one paw forward
on the keys), pounce and push (stretched, facing left or right), flat, curl (a loaf);
plus props the cat acts on: keys, keyboard, computer. The action per panel is the
panel's purpose; the table is in `storyboard.md`. Grids are strings, one character per pixel, rendered nearest-neighbour at 6 px
per pixel into the PNG pages. `python3 docs/comic/nyan.py sheet.png` draws the pose
sheet for checking. In ascii mode the three-line text cat is used instead.
