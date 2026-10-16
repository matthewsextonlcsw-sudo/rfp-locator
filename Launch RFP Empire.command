#!/bin/zsh
cd -- "${0:A:h}" || exit 1
umask 077
fail() {
  print 'Setup could not finish. Check your internet connection and folder permissions, then run this launcher again. See README.md for help.'
  if [[ -t 0 ]]; then read '?Press Return to close.'; fi
  exit 1
}
if [[ ! -x .bootstrap/uv ]]; then
  print 'First launch: installing uv 0.11.6 from Astral into this folder. No administrator access is needed.'
  mkdir -p .bootstrap || fail
  installer=$(mktemp .bootstrap/install-uv.XXXXXX) || fail
  trap 'rm -f -- "$installer"' EXIT
  curl --proto '=https' --tlsv1.2 -fLsS --connect-timeout 20 --max-time 120 https://astral.sh/uv/0.11.6/install.sh -o "$installer" || fail
  UV_INSTALL_DIR="$PWD/.bootstrap" UV_NO_MODIFY_PATH=1 sh "$installer" || fail
  rm -f -- "$installer"
  trap - EXIT
fi
print 'Preparing RFP Locator. Python 3.12 and locked dependencies download automatically on first launch.'
UV_LINK_MODE=copy .bootstrap/uv sync --locked --no-dev || fail
print 'Opening the local app. Keep this terminal open; stop the service from Settings when finished.'
exec .venv/bin/python -m app "$@"
