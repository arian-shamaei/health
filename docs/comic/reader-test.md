# Reader test

A fresh agent with no context reads the rendered pages as images and says what it sees.
Its readings are compared with the rubric below; the comic is adjusted; the test is run
again with a new fresh agent (never the same one, it would remember). It passes when
every row of the rubric is met in the agent's own words.

## The prompt (verbatim, to a fresh general-purpose agent, model sonnet)

> You know nothing about this project. Read these images with the Read tool, in this
> order: docs/assets/title.png, docs/assets/hero-ghostty.png, docs/assets/story.png,
> docs/assets/health.gif, docs/assets/mapping.png, docs/assets/manual.png (all under
> /Users/arianshamaei/Developer/health). Do not read any other file.
> For story.png, describe each panel top to bottom: who is in it, what they are doing,
> what is on the screen, and what you think the numbers mean. Then for mapping.png and
> manual.png say what each is telling you. Finally: in two sentences, what is this
> program and what does the curve mean? List anything you could not work out.

## Rubric (what a correct reading contains)

| image / panel | must read as |
|---|---|
| title | a program called health; the machine's health shown as one curve |
| story 1 | a black cat at a computer typing or running "health"; the screen shows one calm loop; the numbers are low |
| story 2 | the cat looks at the loop with a paw raised, curious (a still cannot show the loop moving; three ghost attempts read as a tangle) |
| story 3 | the cat is on the keyboard pressing keys; the screen has become a tangle; the numbers are higher |
| story 4 | the numbers are at their highest; the cat is flat, done |
| story 5 | the loop is calm again; the cat is asleep on the computer, which is warm; someone tells it to get off |
| mapping | what changes the figure: temperature the colour, memory a wobble, load a spiral, disk the colour spread, the clock turns it |
| manual | how to install (the curl line), the commands, which terminals; the cat putting health in place |
| overall | health draws a computer's health as one curve: a calm loop when idle, a tangle when busy, colour with heat |

## Runs

### Run 1 (2026-10-28): 6 of 9
Met: title, story 3, story 4, mapping, manual, overall (the summary was exact: "an idle
machine gives a single calm loop; load makes the curve spiral inward, memory adds a
wobble, temperature shifts the colour"). Missed: story 1 read as "the mascot announcing
itself", not the cat running the program; story 2 read as "puzzled", no motion seen, paw
not seen; story 5 read as "cooling down", not warm. Asked what the percent was.
Changes: readings lines say `mem`; "tap" beside the paw; a dimmed earlier position of the
loop under panel 2 (motion); the reaching arm rises past the head; heat marks in orange.

### Run 2 (2026-10-28, on a flawed render): 7 of 9
Met: story 5 now "the cat curled up on the warm machine"; percent read as memory. Missed:
story 1, the typing arm read as a tail ("its tail taps") and "the user runs the program";
story 2, "noticing a tiny change", because the ghost used the wobble phase (seconds), not
the turn (uptime). The render also had a colour leak (a shared class dictionary) and an
overflowing readings line in the narrow panel; both fixed.
Changes: the typing arm comes out from the chest to a keyboard at chest height; the ghost
is 3000 s of uptime earlier.

### Run 3 (2026-10-28): 8 of 9
Met: story 1 at last ("sits upright and taps a small keyboard with one front paw... typing
the command shown as `$ health`"), story 5 ("sleeping on its warmth"), all the rest.
Missed: story 2, the single ghost read as "fading dark trails, more tangled", the raised
arm as "tail curled".
Changes, three tries on panel 2 before run 4: three fading ghosts made a tangle (dropped,
motion cannot be shown by overlaying a Lissajous); an arm rising straight up beside the
head read as a pole; an arm crossing the face read as a stick. What stayed: the arm is a
five-pixel-wide diagonal from the shoulder, routed beside the head, with a paw at ear
height, drawn in front of the head. No ghost.

### Run 4 (2026-10-28): 8 of 9, with the panel-2 row restated
Met: story 1 ("one paw reaches out to a small keyboard, labelled tap; the cat appears to
have just typed the command"); story 2 ("sits upright, relaxed, with one paw raised and a
? thought bubble, looking curious"); story 5 ("asleep... on top of what looks like a
computer with a green light; orange wavy lines rise from it, which I read as warmth").
Not met in any run: "someone tells it to get off". The line "...and off the computer."
was the tail of the panel-3 shout cut on 2026-10-28 and reads as a caption about the
display. Changed to "off the computer, nyan."

### Run 5 (2026-10-28): 9 of 9. Pass.
Story 1: "extends one front paw out to a small keyboard... it is typing... the command the
cat is typing matches the $ health prompt". Story 2: "sits upright with one paw raised...
puzzled or curious". Story 3: "hammering the keyboard... keys being mashed... the curve
much busier... 62 C, load 3.50: under load". Story 4: "collapsed... the machine at its
limit". Story 5: "curled up asleep on a flat gray computer... tildes rise, heat... the human
telling the cat to get off the machine... the punchline: the cat is sleeping on the warm
computer", and 46 C "explained by the cat's warmth". Mapping and manual read line by line.
Overall: "reads a machine's temperature, load, memory and disk and draws them live as a
single curve. A calm machine gives a simple, clean loop, a stressed one a tangled,
spiralling, hot-coloured one."
Still open to a fresh reader, and left as is: what "3:5" in the real screenshot is (the
hour's ratio); why panel 4 has no curve (the chorus alone, by design); that the GIF is
seen as one frame by an image reader.
