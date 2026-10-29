#!/usr/bin/env python3
"""Nyan, the mascot, as pixel art: one head with the face states of the cat workspace
(eyes carry the fact, cheeks pink) on a body per pose. Grids are strings, one character
per sprite pixel; render() scales with nearest-neighbour so the pixels stay square.
Keys: . none  d outline  c cream  s stripe  p pink  k eye  w white  n nose."""
from PIL import Image

PALETTE = {
    "d": (120, 120, 132),      # rim: the only thing that separates a black cat from a black page
    "c": (46, 46, 54),         # the coat
    "s": (84, 84, 96),         # sheen on the coat
    "p": (172, 96, 118),       # inside the ears
    "r": (140, 70, 85),        # cheeks
    "k": (10, 10, 12),         # pupils
    "a": (255, 184, 48),       # left eye, amber
    "b": (255, 150, 28),       # right eye, a shade deeper
    "w": (255, 255, 255),
    "n": (120, 80, 95),        # nose
    "h": (200, 200, 212),      # whiskers
    "g": (90, 230, 130),       # an LED
}

HEAD = [
    "..dd..................dd..",
    "..dpd................dpd..",
    "..dppd..............dppd..",
    "..dcppd............dppcd..",
    "..dcccddddddddddddddcccd..",
    "..dccccccccccccccccccccd..",
    "..dcsccccccccccccccccscd..",
    "..dccc...cccccccc...cccd..",     # eyes: 3x3 at cols 6-8 and 17-19, rows 7-9
    "..dccc...cccccccc...cccd..",
    "..dccc...cccccccc...cccd..",
    "..dccccccccccccccccccccd..",
    "hhdcrrccccccnnccccccrrcdhh",     # whiskers either side, nose in the middle
    "..dcrrcccccdccdcccccrrcd..",
    "hhdcccccccccddcccccccccdhh",
    "..dccccccccccccccccccccd..",
    "...dccccccccccccccccccd...",
    "....dddddddddddddddddd....",
]
EYES = {                        # the left eye; the right eye is its mirror in the other amber
    "o_o": ["aaw", "aka", "aaa"],
    "-_-": ["ccc", "hhh", "ccc"],
    "^_^": ["chc", "hch", "ccc"],
    ">_<": ["hcc", "chc", "hcc"],
    "x_x": ["hch", "chc", "hch"],
    "zzz": ["ccc", "hhh", "ccc"],
}


SIT = [                                     # front legs, tail up the right side
    ".....dccccccccccccccd.......",
    "....dcccccccccccccccccd..dd.",
    "....dcsccccccccccccsccd.dcd.",
    "....dcccccccccccccccccd.dcd.",
    "....dcccccccccccccccccdcccd.",
    "....dcsccccccccccccsccdddd..",
    "....dcccccdccccccdcccccd....",
    "....dcccccdccccccdcccccd....",
    "....dcccccdccccccdcccccd....",
    "....dccccccdccccdccccccd....",
    ".....ddddddddddddddddddd....",
]
REACH = [                                   # the sitting cat with one paw up, to the left
    "dd...dccccccccccccccd.......",
    "dcd.dcccccccccccccccccd..dd.",
    "dcd.dcsccccccccccccsccd.dcd.",
    "dcd.dcccccccccccccccccd.dcd.",
    "dcdddcccccccccccccccccdcccd.",
    "dcccccsccccccccccccsccdddd..",
    ".dccccccccdccccccdcccccd....",
    "..dccccccccdccccccdccccd....",
    "...dcccccccdccccccdcccd.....",
    "....dccccccdccccdcccccd.....",
    ".....ddddddddddddddddd......",
]
LONG = [                                    # the body stretched out, four legs, tail up
    "....dccccccccccccccdd...",
    "...dcsccccccsccccccdcd..",
    "..dcccccccccccccccccdcd.",
    ".dcccccccccccccccccccdcd",
    ".dccccccccccccccccccccdd",
    ".dcsccccccsccccccscccccd",
    ".dcccccccccccccccccccccd",
    "..dcccdccccccccccdccccd.",
    "..dcccdccccccccccdccccd.",
    "..dcccdccccccccccdccccd.",
    "..dcccdccccccccccdccccd.",
    "..ddddd..........ddddd..",
]
LOAF = [                                    # curled up, the tail along the front
    ".....dccccccccccccccccccccd.....",
    "...dcscccccccccccccccccsccccd...",
    "..dccccccccccccccccccccccccccd..",
    ".dccccccccccccccccccccccccccccd.",
    ".dccccccccccccccccccccccccccccd.",
    ".dcssssssssssssssssssssccccccccd",
    "..dccccccccccccccccccccccccccd..",
    "...dddddddddddddddddddddddddd...",
]
TYPE = [                                    # sitting, one arm out from the chest onto the keys
    ".....dccccccccccccccd...........",
    "....dcccccccccccccccccd.........",
    "....dcsccccccccccccsccdddddddddd",
    "....dccccccccccccccccccccccccccd",
    "....dcccccccccccccccccdddddddddd",
    "....dcsccccccccccccsccd.........",
    "....dcccccdccccccdcccccd........",
    "....dcccccdccccccdcccccd........",
    "....dcccccdccccccdcccccd........",
    "....dccccccdccccdccccccd........",
    ".....ddddddddddddddddddd........",
]
def _reach():
    """The sitting body shifted right under a head shifted right, with an arm from the
    shoulder rising diagonally up-left beside the head (not across it) to a paw at ear
    height. 34 wide; 16 rows of arm above the 11-row torso."""
    rows = [["."] * 34 for _ in range(16)] + [list("......" + r) for r in SIT]
    for r in range(17, 5, -1):                  # shoulder at (7, 17) up to the paw at (1, 6)
        c = 1 + round((r - 6) * 6 / 11)
        for i, ch in enumerate("dcccd"):        # five wide, so it reads as a leg, not a line
            rows[r][c + i] = ch
    for r, line in ((3, ".dddd."), (4, "dccccd"), (5, "dccccd"), (6, "dddddd")):
        for i, ch in enumerate(line):
            if ch != ".":
                rows[r][i] = ch
    return ["".join(r) for r in rows]


REACH = _reach()
POINT = [r[::-1] for r in REACH]            # the paw up on the right, toward the figure
PROPS = {
    "keys": ["dddddddddddddd",                  # a short keyboard, for one paw
             "dhchchchchchcd",
             "dddddddddddddd"],
    "keyboard": ["dddddddddddddddddddddddddddd",
                 "dhchchchchchchchchchchchchcd",
                 "dddddddddddddddddddddddddddd"],
    "computer": ["dddddddddddddddddddddddddddddddddd",
                 "dccccccccccccccccccccccccccccccgcd",
                 "dcsssssssssssssssssssssssssssscccd",
                 "dddddddddddddddddddddddddddddddddd"],
}
PUSH = [r[::-1] for r in LONG]              # the long body facing right, to push something
BODIES = {"sit": SIT, "reach": REACH, "pounce": LONG, "flat": LONG, "curl": LOAF, "type": TYPE,
          "point": POINT, "push": PUSH}
# (head top-left), (body top-left) per pose
LAYOUT = {"sit": ((0, 0), (0, 16)), "reach": ((6, 0), (0, 0)), "curl": ((3, 0), (0, 15)),
          "type": ((0, 0), (0, 16)), "point": ((2, 0), (0, 0)),
          "pounce": ((0, 0), (18, 10)), "flat": ((0, 0), (18, 10)), "push": ((16, 0), (0, 10))}


def grid(face, pose):
    head = [list(r) for r in HEAD]
    look = {"o_o^": ["aka", "aaw", "aaa"], "o_o>": ["aaw", "aak", "aaa"], "o_o<": ["waa", "kaa", "aaa"]}
    if face in look:
        for i, row in enumerate(look[face]):
            head[7 + i][6:9] = list(row)
            head[7 + i][17:20] = list(row.replace("a", "b"))
    else:
        for i, row in enumerate(EYES[face]):
            head[7 + i][6:9] = list(row)
            head[7 + i][17:20] = list(row[::-1].replace("a", "b"))
    (hx, hy), (bx, by) = LAYOUT[pose]
    body = BODIES[pose]
    w = max(hx + len(HEAD[0]), bx + max(len(b) for b in body))
    h = max(hy + len(HEAD), by + len(body))
    canvas = [["."] * w for _ in range(h)]
    layers = [(body, bx, by), (head, hx, hy)]      # the head is drawn over the body...
    if pose in ("reach", "point"):
        layers.reverse()                          # ...except where the arm crosses in front
    for sheet, ox, oy in layers:
        for y, r in enumerate(sheet):
            for x, ch in enumerate(r):
                if ch != ".":
                    canvas[oy + y][ox + x] = ch
    return ["".join(r) for r in canvas]


def render(face, pose, scale=6):
    """An RGBA image of the sprite at `scale` pixels per sprite pixel; a prop when
    `face` is None and `pose` names one."""
    g = PROPS[pose] if face is None else grid(face, pose)
    h, w = len(g), max(len(r) for r in g)
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    px = img.load()
    for y, row in enumerate(g):
        for x, ch in enumerate(row):
            if ch in PALETTE:
                px[x, y] = PALETTE[ch] + (255,)
    return img.resize((w * scale, h * scale), Image.NEAREST)


if __name__ == "__main__":
    import sys
    poses = [("-_-", "sit"), ("o_o", "reach"), (">_<", "pounce"), ("x_x", "flat"), ("zzz", "curl"), ("^_^", "sit")]
    sheet = Image.new("RGB", (len(poses) * 44 * 6, 30 * 6), (20, 20, 24))
    for i, (face, pose) in enumerate(poses):
        sheet.paste(render(face, pose), (i * 44 * 6, 0), render(face, pose))
    sheet.save(sys.argv[1] if len(sys.argv) > 1 else "nyan-sheet.png")
