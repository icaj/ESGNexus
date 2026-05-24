#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"

if [ -f backend.pid ]; then
  kill "$(cat backend.pid)" 2>/dev/null || true
  rm -f backend.pid
  echo "Backend parado."
else
  pkill -f "uvicorn app.main:app" 2>/dev/null || true
  echo "Nenhum backend.pid encontrado. Tentativa de parada por processo realizada."
fi
