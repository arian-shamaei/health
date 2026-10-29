# Storyboard: "the string"

Nyan never presents health. It is the login screen of the Pi it lives on; the reader
meets it the way a guest does. Then the cat mistakes the slowly turning trace for a
string, and the strip spins out on a feedback loop: paws land on keys, load rises, the
trace tangles and moves more, the cat paws harder. The chorus is the readings line. Nyan narrates in caption boxes, to itself, after the
fact; its face in the panel stays wordless, as its spec says.

```
┌────────────────────────────────────────────────────────────────┐
│ 1                                                   72 x 14    │
│   $ health                                                     │
│                           .--.                                 │
│                          (    )                                │
│   .--------.              `--'                                 │
│  (  health  )                                                  │
│   `-------'/                                                   │
│    /\_/\  /                                                    │
│   ( -_- )                                                      │
│   38 C  load 0.10  15 %                                        │
├──────────────────────┬─────────────────────────────────────────┤
│ 2           24 x 30  │ 3                           47 x 30     │
│                      │                                         │
│        .--.          │                                         │
│       (    )         │            ,-~=#@$%&@#=~-.              │
│        `--'          │           {#@$%&@#$%&@#$%&}             │
│          \           │           {&@#$%&@#$%&@#$%}             │
│           \          │            `~=#@$%&@#=~-'               │
│     .---.            │  62 C  load 3.50  40 %                  │
│    (  ?  )           │                                         │
│     `---'            │           .---.                         │
│      o               │          (  !  )                        │
│     o                │           `---'                         │
│   /\_/\              │             o                           │
│  ( o_o )/            │            o                            │
│  38 C  load 0.12     │     /\_/\    tap tap tap                │
│                      │    ( >_< )/                             │
│                      │  [:::::::::::::::::::::]                │
├──────────────────────┴─────────────────────────────────────────┤
│ 4                                                   72 x 8     │
│                                                                │
│                                                                │
│                 73 C     load 4.70     60 %                    │
│                                                                │
│  /\_/\                                                         │
│ ( x_x )                                                        │
├────────────────────────────────────────────────────────────────┤
│ 5                                                   72 x 14    │
│   .--------------------.                                       │
│   |        .--.        |   < ...and off the computer.          │
│   |       (    )       |                                       │
│   |        `--'        |                                       │
│   |  46 C  load 0.10   |                                       │
│   `--------------------'                                       │
│     ~  ~  ~                                                    │
│    /\_/\                                                       │
│   ( zzz )                                                      │
│  [________]                                                    │
└────────────────────────────────────────────────────────────────┘
```

## Words on the page

- The cat speaks health's commands, and one line. In panel 1 it says `health`, a speech
  bubble with a tail, and the screen shows `$ health`. Its thoughts are punctuation: `?`
  in 2, `!` in 3, in thought bubbles with the `o o` trail. In panel 4 it says
  "The computer is overloaded!" (added 2026-10-28). Panel 5's caption is "Cooling off!".
- One off-panel line from the person who logged in, the `<` pointing out of the panel:
  `...and off the computer.` in 5. (The panel 3 line was cut on 2026-10-28.)
- The screen's own text: `$ health` and the readings line.
- Sounds: `zzz`, `tap tap tap`. Heat off the box in 5 is `~ ~ ~`.
- No narrator, no captions. The reader tests at the bottom are why.

## The beats

1. **Prologos.** A guest logs in. The screen is `health --once` exactly as the Pi prints
   it: one curve, the readings under it. The cat is asleep in the corner. Nothing is
   explained; the chorus walks in with the screen.
2. **Episode, narrow.** The live figure turns on its own (the uptime phase). The cat
   wakes. To a cat a slowly moving line is a string. One paw up, eyes on it.
3. **Episode, the climax.** The paw lands on the keys; the typed row is cat typing. Load
   rises, the trace spirals and the whole figure moves more, which is more string. The
   loop closes: the cat is the load. No lettering, the tangle is the panel.
4. **Stasimon.** No figure. The chorus alone reads the peak numbers. The cat is done.
5. **Exodos.** The curve has locked, the paws have stopped, the cat is asleep on the Pi
   itself. The chorus is nearly back to panel 1, except the temperature. The one
   departure left in the figure is the cat.

## Why it introduces health without presenting it

- Panel 1 is a real artifact, not an explanation: the login screen the Pi shows.
- Panel 3 shows the mapping by causing it: keys, load, spiral. The reader sees load
  become shape before any table says so.
- Panel 5 shows a second reading on its own: heat without load warms the hue but does
  not spiral. The figure separates the two, and the cat is the proof.

## Layout rules

- One column, 72 wide, each tier one ```text fence; tier 2 is two panels in one fence
  (24 + 1 + 47). Heights 14, 30, 8, 14: tall where the strip is loud.
- The cat sits bottom-left in every panel but 4, where it is at the chorus line's edge.
- The chorus is the only text that moves: in with the screen, full voice, alone, nearly
  home. Panel 1 and 5 share a composition; the differences are the Pi and the hue.
- Figures are real `health --png` frames through chafa at each panel's size. Readings
  pinned: 1 `temp=38,load=0.1,mem=0.15`; 2 `temp=38,load=0.12,mem=0.15`;
  3 `temp=62,load=3.5,mem=0.4`; 5 `temp=46,load=0.1,mem=0.15`; disk 0.3, hour 14 throughout.
  Panel 4 has no figure; its numbers are the peak, `temp=73,load=4.7,mem=0.6`.
- Panel 2's figure turns: two frames of the same readings at different uptimes, drawn as
  the faint previous position and the current one, if chafa keeps the ghost readable.

## Reader test, 2026-10-28

A fresh reader with no context (a subagent told to read as a 75-year-old who only uses
email, given the page alone) answered: health is "the computer's way of showing how it
feels, drawn as a loop"; a loop means resting, a tangle working hard, orange hot; the
numbers are "for people who like numbers" and not needed; the story retold correctly in
two sentences. Stumbles: "load" in the number lines (unexplained by design, but still a
stumble); panel 2's "that is the time" (reworded above); "[ pi ]" (now "[computer]"); the
Greek titles (margin notes, never in the strip). Colour cannot be seen in text, so "blue"
and "orange" rest on the words; the colour GIF under the strip in the README carries it.

Wordless draft, same reader: got "health" as the thing run and "a check of how the
machine is doing", and that neat loop goes with low numbers and calm cat, tangle with
high. Did NOT get: that the cat caused it (the `@@@@` string bubble read as the tangle),
who was tapping, why panel 5 is warm, or that the box is the computer. The causal chain
is the story, so three pictures were fixed rather than words added: the bubble holds one
word, the keyboard is drawn under the cat, and panel 5 shows the screen on the box.

Third draft (string? bubble, keyboard drawn, screen on the box), same reader: still
read the tapping as "the person taps the keys", could not place "string?", and saw no
reason for the warmth. The cat as three lines of ASCII cannot be seen pawing a keyboard.
Fourth draft adds two off-panel lines from the person who logged in.

Fourth draft (two off-panel lines), same reader: the cause landed. Retold as "the cat
got onto the keyboard, the screen filled with a tangle, the numbers climbed, someone
shouted, the cat got off, the machine cooled and went quiet". Loop read as "quiet",
tangle as "trouble", health as "the name of the check". Still could not place
"string?"/"string!" (fourth reader in a row), and read panel 5's warmth as cooling off
after the trouble rather than the cat on the box. Decision pending: drop the string
bubbles and show the cat swatting at the moving loop instead.

## The cat's action per panel (2026-10-28, the pixel-art cat)

Each panel's action is the panel's purpose, acted out, never decoration:

| panel | purpose | the cat | eyes |
|---|---|---|---|
| 1 | nyan runs health | sits at the keys, one paw on a key | open, on the screen |
| 2 | notices the loop move | one paw up toward the figure | open, raised |
| 3 | chases it onto the keys | sprawled on the keyboard, letters flying | pressed shut |
| 4 | the peak numbers | flat out | crossed |
| 5 | asleep on the warm computer | a loaf on the computer, LED on, heat rising | shut, z z z |
| mapping | what each reading does | one paw up at the figure | open, raised |
| install | puts health in place | pushes a box marked health toward the bin | open, on the box |
| use | the commands | at the keys, paw on a key | open, on the list |

Poses and props live in `nyan.py`: sit, reach, point, type, pounce, flat, curl, push; the
keys (short keyboard), the keyboard, the computer. A face can carry a look direction
(`o_o^`, `o_o>`, `o_o<`), which is not mirrored between the eyes.
