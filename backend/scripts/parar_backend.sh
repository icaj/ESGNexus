#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PID_FILE="$ROOT_DIR/backend.pid"

if [[ ! -f "$PID_FILE" ]]; then
  echo "Arquivo backend.pid nao encontrado. Nada para parar."
  exit 0
fi

PID="$(cat "$PID_FILE")"
if ps -p "$PID" >/dev/null 2>&1; then
  echo "Parando backend PID $PID..."
  kill "$PID"
  sleep 3
  if ps -p "$PID" >/dev/null 2>&1; then
    echo "Processo ainda ativo. Forcando parada..."
    kill -9 "$PID"
  fi
  echo "Backend parado."
else
  echo "PID $PID nao esta em execucao."
fi

rm -f "$PID_FILE"
