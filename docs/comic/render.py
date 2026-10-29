#!/usr/bin/env python3
"""The comic strip, compiled from docs/comic/storyboard.md: five panels in four tiers,
one tier per file (docs/comic/panels/2N-tierN-fig.txt), each 72 columns of 7-bit ASCII.

Every figure is a real `health --png` frame converted to ASCII by chafa (monochrome,
`--symbols ascii-alnum`), drawn at the panel's own size: the PNG is rendered at 3x6 px
per cell so the 2-px trace stays thick against the cell (at 6x12 the 2:3 loop vanished).
Hour 0 pins the simplest family, 2:3, so the idle loop reads as one loop. The cat, its bubbles, the screen's
text and the sounds are stamped on top. Frames are +-| so the strip is ASCII throughout.
Run from anywhere; needs chafa.
"""
import os
import subprocess
import sys
import tempfile

MODE = "png"          # "ascii": chafa figures in text; "png": real colour frames, text drawn over

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.dirname(os.path.dirname(here))
health = os.path.join(root, "health")
panels = os.path.join(here, "panels")
WIDTH = 72


class Canvas:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.rows = [[" "] * w for _ in range(h)]
        self.colours = {}

    labels = ()
    cat_cells = ()

    def stamp_colour(self, x, y, text, rgb):
        self.stamp(x, y, text)
        for dy, line in enumerate(text.split("\n")):
            for dx, ch in enumerate(line):
                if ch != " ":
                    self.colours[(x + dx, y + dy)] = rgb

    cats = ()

    def prop(self, x, y, name):
        """A pixel prop (keyboard, computer) at cell (x, y), under whatever cat follows."""
        self.cats = self.cats + ((x, y, None, name),)

    def stamp_cat(self, x, y, face, pose="sit"):
        if MODE == "png":
            self.cats = self.cats + ((x, y, face, pose),)
            return
        text = cat(face, pose)
        self.stamp(x, y, text)
        cells = []
        for dy, line in enumerate(text.split("\n")):
            for dx, ch in enumerate(line):
                if ch != " ":
                    cells.append((x + dx, y + dy, ch in "()" and dy == [i for i, l in enumerate(POSES[pose]) if "%s" in l][0]))
        self.cat_cells = self.cat_cells + tuple(cells)

    def stamp(self, x, y, text):
        for dy, line in enumerate(text.split("\n")):
            self.labels = self.labels + ((x, y + dy, len(line)),)
            for dx, ch in enumerate(line):
                if 0 <= y + dy < self.h and 0 <= x + dx < self.w and ch != "\x00":
                    self.rows[y + dy][x + dx] = ch

    def clear(self, x, y, w, h):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                if 0 <= yy < self.h and 0 <= xx < self.w:
                    self.rows[yy][xx] = " "

    def frame(self):
        self.rows[0] = list("+" + "-" * (self.w - 2) + "+")
        self.rows[-1] = list("+" + "-" * (self.w - 2) + "+")
        for r in self.rows[1:-1]:
            r[0] = r[-1] = "|"

    def text(self):
        return "\n".join("".join(r).rstrip() for r in self.rows)

    regions = ()

    def figure(self, x, y, w, h, readings, ghost=None):
        """A real frame in cells (x, y, w, h). In ASCII mode chafa draws it here; in PNG
        mode the region is left black and the frame is pasted in later. `ghost` is a
        second readings string drawn dimmed under the frame: an earlier position, so the
        figure is seen to move."""
        self.regions = self.regions + ((x, y, w, h, readings, ghost),)
        if MODE == "ascii":
            self.stamp(x, y, figure(w, h, readings))


def figure(w, h, readings):
    """A real frame, w x h cells of ASCII."""
    with tempfile.TemporaryDirectory() as d:
        png = os.path.join(d, "f.png")
        subprocess.run([sys.executable, health, "--png", png, "--size", "%dx%d" % (w * 3, h * 6),
                        "--readings", readings], check=True, stdout=subprocess.DEVNULL)
        out = subprocess.run(["chafa", "-f", "symbols", "--symbols", "ascii-alnum", "-c", "none",
                              "--fg-only", "-w", "9", "-p", "on", "--dither", "none",
                              "--size", "%dx%d" % (w, h), "--stretch", png],
                             check=True, stdout=subprocess.PIPE).stdout.decode()
    lines = [l.ljust(w)[:w] for l in out.split("\n")][:h]
    while len(lines) < h:
        lines.append(" " * w)
    return "\n".join(lines)


REST = (38, 0.1, 0.15)
AMBER = (255, 184, 48)


def readings_line(temp, load, mem):
    return "%d C  load %.2f  mem %d %%" % (temp, load, mem * 100)


def stamp_readings(c, x, y, temp, load, mem, fmt="%d C  load %.2f  mem %d %%"):
    """The readings line, with each value that is not at its resting value in amber: the
    highlight says what changed."""
    parts = [("%d C" if "C  " in fmt else "%d C") % temp, "load %.2f" % load, "mem %d" % (mem * 100)]
    line = fmt % (temp, load, mem * 100)
    c.stamp(x, y, line)
    for part, value, rest in zip(parts, (temp, load, mem), REST):
        if abs(value - rest) > 1e-9:
            at = line.index(part)
            c.stamp_colour(x + at, y, part, AMBER)


def pinned(temp, load, mem):
    return "temp=%d,load=%s,mem=%s,disk=0.3,hour=0" % (temp, load, mem)


POSES = {
    # sitting, calm: the default
    "sit":    [r"  /\_/\   ", r" (%s)  ", r" /     \_ ", r"(  | |   )", r" \_|_|__/ "],
    # one paw up, looking at something above
    "reach":  [r"      /\_/\ ", r"  /\ (%s)", r"  \ \ > ^ < ", r"   \ \/   \_", r"    \_|     )", r"      |  | /", r"      (__|_/"],
    # pouncing, both paws down on whatever is below
    "pounce": [r"        /\_/\ ", r"  _____(%s)", r" (      > ^ <_)", r"  \__/\__/\__/"],
    # flat on its back
    "flat":   [r"  /\_/\       ", r" (%s)______ ", r"  > ^ <       )", r" (___________/ "],
    # curled up asleep
    "curl":   [r"     /\_/\    ", r"    (%s)   ", r"   __> ^ <__  ", r"  (  ______  ) ", r"   \(______)/  "],
}


def cat(face, pose="sit"):
    lines = [l.replace("%s", face) if "%s" in l else l for l in POSES[pose]]
    w = max(len(l) for l in lines)
    return "\n".join(l.ljust(w) for l in lines)


def thought(mark):
    return " .---. \n(  %s  )\n `---' \n   o   \n  o    " % mark


def write(name, canvas):
    for i, r in enumerate(canvas.rows):
        assert r[-1] in "|+", "%s row %d runs past the frame: %r" % (name, i, "".join(r))
    text = canvas.text()
    assert all(32 <= ord(c) < 127 or c == "\n" for c in text), name
    with open(os.path.join(panels, name + ".txt"), "w") as f:
        f.write(text + "\n")
    print(name)


def tier1():
    c = Canvas(WIDTH, 16)
    c.figure(21, 1, 49, 11, pinned(38, 0.1, 0.15))
    c.frame()
    c.stamp(3, 1, "$ health")
    c.clear(1, 4, 17, 10)
    c.stamp(2, 4, bubble(["health"]))
    c.prop(14, 11, "keys")
    c.stamp(16, 10, "tap")
    c.stamp_cat(1, 7, "o_o>", "type")
    stamp_readings(c, 21, 12, 38, 0.1, 0.15)
    return c


def tier2():
    c = Canvas(WIDTH, 32)
    # left panel, 24 wide: cols 0..23 ; right panel, 48 wide: cols 24..71 (shared edge at 24)
    c.figure(1, 1, 22, 14, pinned(38, 0.12, 0.15) + ",uptime=3000")
    c.figure(25, 1, 46, 17, pinned(62, 3.5, 0.4))
    # frames
    for y in (0, 31):
        c.stamp(0, y, "+" + "-" * 23 + "+" + "-" * 46 + "+")
    for y in range(1, 31):
        c.rows[y][0] = c.rows[y][24] = c.rows[y][71] = "|"
    # left: ? bubble, cat, readings
    c.clear(1, 15, 22, 16)
    stamp_readings(c, 1, 15, 38, 0.12, 0.15, fmt="%d C load %.2f mem %d%%")
    c.stamp(9, 17, thought("?"))
    c.stamp_cat(2, 22, "o_o^", "reach")
    # right: readings, ! bubble, cat on the keys, tap tap tap
    c.clear(25, 18, 46, 13)
    stamp_readings(c, 26, 18, 62, 3.5, 0.4)
    c.stamp(36, 20, thought("!"))
    c.stamp(44, 23, "j")
    c.stamp(49, 24, ";")
    c.stamp(45, 26, "k")
    c.stamp(53, 27, "l")
    c.stamp(47, 25, "tap tap tap")
    c.prop(33, 30, "keyboard")
    c.stamp_cat(27, 25, ">_<", "pounce")
    return c


def tier3():
    c = Canvas(WIDTH, 9)
    c.frame()
    c.stamp(20, 1, bubble(["The computer is overloaded!"], tail="left"))
    line = "73 C     load 4.70     mem 60 %"
    stamp_readings(c, 38, 6, 73, 4.7, 0.6, fmt="%d C     load %.2f     mem %d %%")
    c.stamp_cat(2, 3, "x_x", "flat")
    return c


def tier4():
    c = Canvas(WIDTH, 19)
    c.frame()
    # the screen, seen from across the room: a box with a small figure and its readings
    sw, sh = 36, 8
    c.stamp(3, 1, "." + "-" * sw + ".")
    for y in range(2, 2 + sh):
        c.rows[y][3] = c.rows[y][4 + sw] = "|"
    c.stamp(3, 2 + sh, "'" + "-" * sw + "'")
    c.figure(4, 2, sw, sh - 1, pinned(46, 0.1, 0.15))
    stamp_readings(c, 5, 1 + sh, 46, 0.1, 0.15)
    c.stamp(44, 3, "Cooling off!")
    c.stamp(16, 11, "z z z")
    c.stamp_colour(19, 12, "~", (255, 150, 60))
    c.stamp_colour(18, 13, "~ ~", (255, 150, 60))
    c.stamp_colour(17, 14, "~ ~ ~", (255, 150, 60))
    c.stamp_colour(18, 15, "~ ~", (255, 150, 60))
    c.prop(2, 16, "computer")
    c.stamp_cat(3, 11, "zzz", "curl")
    return c



# ---- the rest of the README, as panels ------------------------------------------------

def bubble(lines, tail="right"):
    """A speech bubble whose corners sit over the parentheses: the dashed rows are as long
    as the text rows. The tail points down-right or down-left, to the speaker."""
    w = max(len(l) for l in lines)
    out = [" ." + "-" * (w + 3) + "."]
    out += ["(  " + l.ljust(w) + "  )" for l in lines]
    if tail == "right":
        out += [" '" + "-" * (w + 3) + "'/"]
    else:
        out += ["/'" + "-" * (w + 3) + "'"]
    return "\n".join(out)


def tier0():
    c = Canvas(WIDTH, 3)
    c.frame()
    c.stamp(2, 1, "health")
    t = "the machine's health as a Lissajous curve"
    c.stamp(WIDTH - 2 - len(t), 1, t)
    if MODE == "ascii":
        write("10-title-fig", c)
    return c


def tier5():
    """The mapping, shown not told: the resting loop, then the same loop with one reading
    changed at a time, each a real frame, with what you see written under it."""
    c = Canvas(WIDTH, 31)
    rest = dict(temp=38, load=0.1, mem=0.15, disk=0.05, hour=0, uptime=0)
    cases = [("at rest", {}),
             ("hotter: it turns red", dict(temp=78)),
             ("busy: the loops shrink", dict(load=3.0)),
             ("memory full: wobbles", dict(mem=0.9)),
             ("disk full: more colors", dict(disk=0.95)),
             ("time passing: it turns", dict(uptime=3000))]
    w, h = 22, 9
    for i, (label, change) in enumerate(cases):
        r = dict(rest, **change)
        x, y = 1 + (i % 3) * 24, 1 + (i // 3) * 12
        c.figure(x, y, w, h, ",".join("%s=%s" % kv for kv in r.items()))
        stamp_readings(c, x, y + h, r["temp"], r["load"], r["mem"], fmt="%d C load %.2f mem %d%%")
        c.stamp(x + (w - len(label)) // 2, y + h + 1, label)
    c.frame()
    c.stamp_cat(2, 24, "o_o^", "point")
    c.stamp(15, 26, "at rest it draws one still loop. each reading bends it.")
    c.stamp(15, 27, "linux, pi, mac. on a mac it skips the temperature: blue.")
    return c


def tier6():
    c = Canvas(WIDTH, 16)
    c.frame()
    c.stamp(2, 1, bubble(["curl -fsSL https://raw.githubusercontent.com/",
                          "     arian-shamaei/health/main/install.sh | sh"]))
    c.stamp(2, 6, "one file, no dependencies. python 3.7 or newer. linux and macOS.")
    c.stamp(2, 7, "by hand:  git clone https://github.com/arian-shamaei/health")
    c.stamp(2, 8, "          install -m 755 health/health ~/.local/bin/health")
    c.stamp(21, 12, "[ health ]  -->  ~/.local/bin/    and man health")
    c.stamp(21, 13, "undo: rm ~/.local/bin/health and its man page")
    c.stamp_cat(1, 9, "o_o>", "push")
    return c


def tier7():
    rows = [("health", "fills the window; q quits"),
            ("health 4", "4 frames a second (0.5 to 20)"),
            ("health --braille", "dots, not pixels. any terminal"),
            ("health --once", "one drawing with the readings"),
            ("health --png a.png", "one frame to a PNG"),
            ("health --demo DIR", "frames of a build, for a GIF")]
    c = Canvas(WIDTH, len(rows) + 6)
    c.frame()
    c.prop(14, 5, "keys")
    c.stamp_cat(1, 1, "o_o>", "type")
    for i, (cmd, what) in enumerate(rows):
        c.stamp(21, 1 + i, cmd.ljust(20) + what)
    c.stamp(21, len(rows) + 2, "Kitty graphics (Ghostty, kitty, WezTerm, tmux) or")
    c.stamp(21, len(rows) + 3, "iTerm2, sixels via chafa; else Braille in color.")
    c.stamp(21, len(rows) + 4, "HEALTH_FORMAT=kitty|iterm|sixels. man health.")
    return c


def tier8():
    c = Canvas(WIDTH, 8)
    c.frame()
    c.stamp(2, 1, "readings:  /sys/class/thermal  /proc/loadavg  /proc/meminfo  statvfs")
    c.stamp(2, 2, "           getloadavg, sysctl, vm_stat on macOS. no network.")
    c.stamp(2, 4, "vibe coded in Claude Code, corrected by eye in a real terminal.")
    c.stamp(2, 5, "every figure here is drawn by the tool (docs/render.sh, docs/comic)")
    c.stamp(2, 6, "except the screenshot, which is a screenshot.                MIT.")
    return c


def join(*tiers):
    """One page from stacked tiers: each tier's top border replaces the previous bottom."""
    page = Canvas(WIDTH, 0)
    page.rows = list(tiers[0].rows)
    page.regions = tiers[0].regions
    page.labels = tiers[0].labels
    page.cat_cells = tiers[0].cat_cells
    page.cats = tiers[0].cats
    page.colours = dict(tiers[0].colours)
    for t in tiers[1:]:
        off = len(page.rows) - 1
        page.rows = page.rows[:-1] + t.rows
        page.regions += tuple((x, y + off, w, h, r, g) for x, y, w, h, r, g in t.regions)
        page.labels += tuple((x, y + off, n) for x, y, n in t.labels)
        page.cat_cells += tuple((x, y + off, cheek) for x, y, cheek in t.cat_cells)
        page.cats += tuple((x, y + off, f, p) for x, y, f, p in t.cats)
        page.colours.update({(x, y + off): c for (x, y), c in t.colours.items()})
    page.h = len(page.rows)
    return page


def animate(readings, k, fps=10):
    """Frame k of a loop at real speed: the live view advances the wobble phase one second
    per second (a full cycle a minute) and the turn one degree a minute of uptime, so a
    frame is 1/fps of a second of both. A later key wins in --readings."""
    base_up = 0
    for item in readings.split(","):
        if item.startswith("uptime="):
            base_up = float(item[7:])
    t = k / fps
    return readings + ",sec=%g,uptime=%g" % (t % 60, base_up + t)


def write_png(name, canvas, cw=14, ch=28, font_px=23):
    """The page as an image. docs/assets/<name>.png"""
    img = compose(name, canvas, cw, ch, font_px)
    out = os.path.join(root, "docs", "assets", name + ".png")
    img.save(out, optimize=True)
    print(out)


def write_gif(name, canvas, frames=60, cw=14, ch=28, font_px=23):
    """The page as a loop: every figure region moves as the live view does. docs/assets/<name>.gif"""
    from PIL import Image
    imgs = [compose(name, canvas, cw, ch, font_px, k).convert("P", palette=Image.ADAPTIVE, colors=128)
            for k in range(frames)]
    out = os.path.join(root, "docs", "assets", name + ".gif")
    imgs[0].save(out, save_all=True, append_images=imgs[1:], duration=100, loop=0, optimize=True)
    print(out, "%d frames" % frames)


def compose(name, canvas, cw=14, ch=28, font_px=23, k=None):
    """One image of the page: black, the real frames pasted into their regions (frame k of
    the animation when k is given), every other cell drawn as monospace text."""
    for i, r in enumerate(canvas.rows):
        assert r[-1] in "|+", "%s row %d runs past the frame: %r" % (name, i, "".join(r))
    from PIL import Image, ImageDraw, ImageFont
    font = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", font_px)
    img = Image.new("RGB", (canvas.w * cw, canvas.h * ch), (0, 0, 0))
    from PIL import ImageChops
    for x, y, w, h, readings, ghost in canvas.regions:
        if k is not None:
            readings = animate(readings, k)
        with tempfile.TemporaryDirectory() as d:
            png = os.path.join(d, "f.png")
            subprocess.run([sys.executable, health, "--png", png, "--size", "%dx%d" % (w * cw, h * ch),
                            "--readings", readings], check=True, stdout=subprocess.DEVNULL)
            frame = Image.open(png).convert("RGB")
            for g, level in zip(ghost or (), (0.18, 0.3, 0.45)):   # a trail of earlier positions
                subprocess.run([sys.executable, health, "--png", png, "--size", "%dx%d" % (w * cw, h * ch),
                                "--readings", g], check=True, stdout=subprocess.DEVNULL)
                dim = Image.open(png).convert("RGB").point(lambda v, k=level: v * k)
                frame = ImageChops.lighter(frame, dim)
            img.paste(frame, (x * cw, y * ch))
    draw = ImageDraw.Draw(img)
    grey = (120, 120, 130)
    for x, y, n in canvas.labels:          # a label over a figure gets a black bar behind it
        if any(rx <= x < rx + rw and ry <= y < ry + rh for rx, ry, rw, rh, *_ in canvas.regions):
            draw.rectangle([x * cw, y * ch, (x + n) * cw, (y + 1) * ch], fill=(0, 0, 0))
    for y, row in enumerate(canvas.rows):
        for x, ch_ in enumerate(row):
            if ch_ == " ":
                continue
            # frame characters become solid lines: a cell is on the frame if it is on an
            # edge of the page or on a row/column that is all frame characters
            on_frame = ch_ in "+-|" and (y in (0, canvas.h - 1) or all(c in "+-|" for c in row)
                                         or x in (0, canvas.w - 1)
                                         or (ch_ == "|" and sum(1 for r in canvas.rows if r[x] in "|+") > canvas.h // 2))
            if on_frame:
                cx, cy = x * cw + cw // 2, y * ch + ch // 2
                if ch_ in "-+":
                    draw.line([(x * cw, cy), (x * cw + cw, cy)], fill=grey, width=2)
                if ch_ in "|+":
                    draw.line([(cx, y * ch), (cx, y * ch + ch)], fill=grey, width=2)
                continue
            fill = (235, 235, 235)
            for cx_, cy_, cheek in canvas.cat_cells:
                if (cx_, cy_) == (x, y):
                    fill = (255, 130, 150) if cheek else (255, 225, 180)
                    break
            fill = canvas.colours.get((x, y), fill)
            draw.text((x * cw + 1, y * ch + 2), ch_, font=font, fill=fill)
    sys.path.insert(0, here)
    import nyan
    for x, y, face, pose in canvas.cats:        # props first, since they are recorded first
        sprite = nyan.render(face, pose, scale=6)
        img.paste(sprite, (x * cw, y * ch), sprite)
    return img


def all_tiers():
    story = join(tier1(), tier2(), tier3(), tier4())
    if MODE == "png":
        for stale in ("10-title-fig", "20-story-fig", "30-manual-fig"):
            try:
                os.remove(os.path.join(panels, stale + ".txt"))
            except OSError:
                pass
        write_png("title", tier0())
        write_png("story", story)
        write_gif("mapping", tier5())
        write_png("manual", join(tier6(), tier7(), tier8()))
    else:
        tier0()
        write("20-story-fig", story)
        write("30-manual-fig", join(tier5(), tier6(), tier7(), tier8()))


if __name__ == "__main__":
    all_tiers()
