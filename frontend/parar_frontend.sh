#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

if [ -f frontend.pid ]; then
  kill "$(cat frontend.pid)" 2>/dev/null || true
  rm -f frontend.pid
  echo "Frontend parado."
else
  pkill -f "streamlit run app.py" 2>/dev/null || true
  echo "Nenhum frontend.pid encontrado. Tentativa de parada por processo realizada."
fi
