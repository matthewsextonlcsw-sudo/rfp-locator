#!/bin/zsh
cd -- "${0:A:h}"
if [[ ! -x .venv/bin/python ]]; then
  print 'Install dependencies from this folder first: uv sync --locked --group dev'
  read '?Press Return to close.'
  exit 1
fi
exec .venv/bin/python -m app "$@"
