# health

One-file Python program (`health`, standard library only) that draws a machine's health as
a live harmonograph in the terminal. Public repo: https://github.com/arian-shamaei/health.

- `health` is the whole program: readings, curve, Braille and PNG renderers, the terminal
  protocols (Kitty with Unicode placeholders through tmux, iTerm2, sixel through chafa),
  the live loop, `--once`, `--png`, `--demo`. Its docstring is the mapping's documentation.
- `health.1` is the man page; `install.sh` the curl installer; `docs/render.sh` regenerates
  `docs/assets/` from the tool (the hero is a real screenshot, kept as is).
- Origin: `~/Developer/cat/pi/rawr/harmonograph.py` on the Raspberry Pi account `rawr`.
  This repo is the standalone form; since 2026-10-27 the Pi's login screen runs this
  version too (`health --once`, with the note printed by rawr's `.bash_profile`).
- Releases: a version bump tags `vX.Y.Z` and publishes a GitHub release with `health` and
  `health.1` as its assets (`gh release create vX.Y.Z health health.1`). `install.sh` fetches
  the latest release's assets, and the README's downloads badge counts those fetches; without
  a release the installer and the counter both stop.
- Rules: no dependencies, Python 3.7 syntax (the Mac's python3 is 3.9), every figure in the
  README comes from the renderer or a real screenshot, never a mock. A change to the mapping
  is a change to the docstring, the README table and the man page in the same commit.
- Verify the live loop without a window: `/tmp/ptytest.py`-style, a `pty.fork` that sends
  `q` after two seconds and checks for the alternate-screen sequences and the protocol's
  marker (`\x1b_Ga=T`, `1337;File`, Braille). On Linux the master read ends with EIO, not
  EOF.
