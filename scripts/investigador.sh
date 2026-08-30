#!/bin/bash
# Lanza el investigador en tmux. Uso: scripts/investigador.sh [start|stop|log]
export PATH="$HOME/.local/bin:$HOME/.nvm/versions/node/v24.19.0/bin:$HOME/.pyenv/shims:/usr/local/bin:/usr/bin:/bin"
cd "$(dirname "$0")/.." || exit 1
case "${1:-start}" in
  start) tmux kill-session -t investigador 2>/dev/null; mkdir -p tmp
         tmux new-session -d -s investigador "cd '$PWD' && export PATH='$PATH' && python3 scripts/investigador.py 8787 2>&1 | tee -a tmp/investigador.log; sleep 30"
         sleep 2; curl -s -m 5 http://127.0.0.1:8787/ && echo || { echo "no arranca:"; tail -20 tmp/investigador.log; } ;;
  stop) tmux kill-session -t investigador ;;
  log) tail -50 tmp/investigador.log ;;
esac
