#!/bin/sh
# install.sh: one-line installer for `health`.
#
#   curl -fsSL https://raw.githubusercontent.com/arian-shamaei/health/main/install.sh | sh
#
# Copies the one-file program to $PREFIX/bin/health and its man page to
# $PREFIX/share/man/man1/health.1 (PREFIX defaults to ~/.local). Python 3.7 or newer is
# the only requirement. POSIX sh, no bashisms.
#
#   HEALTH_PREFIX   install prefix (default: $HOME/.local)
#   HEALTH_REF      git ref to install (default: main)
#
# Uninstall: rm "$PREFIX/bin/health" "$PREFIX/share/man/man1/health.1"

set -eu

REPO="arian-shamaei/health"
REF="${HEALTH_REF:-main}"
PREFIX="${HEALTH_PREFIX:-$HOME/.local}"
RAW="https://raw.githubusercontent.com/$REPO/$REF"

err()  { printf 'health install: error: %s\n' "$1" >&2; exit 1; }
have() { command -v "$1" >/dev/null 2>&1; }

have python3 || err "python3 is needed (3.7 or newer)"
if have curl; then fetch() { curl -fsSL "$1" -o "$2"; }
elif have wget; then fetch() { wget -q "$1" -O "$2"; }
else err "curl or wget is needed"; fi

tmp="$(mktemp -d)"
trap 'rm -rf "$tmp"' EXIT

fetch "$RAW/health" "$tmp/health"
fetch "$RAW/health.1" "$tmp/health.1"
python3 -m py_compile "$tmp/health" || err "the downloaded file does not compile; try again"

mkdir -p "$PREFIX/bin" "$PREFIX/share/man/man1"
install -m 755 "$tmp/health" "$PREFIX/bin/health"
install -m 644 "$tmp/health.1" "$PREFIX/share/man/man1/health.1"

printf 'installed %s/bin/health (%s)\n' "$PREFIX" "$("$PREFIX/bin/health" --version)"
case ":$PATH:" in
  *":$PREFIX/bin:"*) ;;
  *) printf 'note: %s/bin is not on your PATH\n' "$PREFIX" ;;
esac
printf 'run: health        (q quits)   man health for the page\n'
