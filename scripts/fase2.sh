#!/bin/bash
# Espera a que la campaña escriba FIN y lanza la fase 2 (medios y repaso). Uso: scripts/fase2.sh [horas] [paralelo]
export PATH="$HOME/.local/bin:$HOME/.nvm/versions/node/v24.19.0/bin:$HOME/.pyenv/shims:/usr/local/bin:/usr/bin:/bin"
cd "$(dirname "$0")/.." || exit 1
until grep -q "^[0-9:]* FIN" tmp/campana.log 2>/dev/null; do sleep 60; done
echo "$(date +%H:%M:%S) campaña terminada; arranca fase 2" >> tmp/medios.log
python3 scripts/medios.py "${1:-3}" "${2:-3}"
