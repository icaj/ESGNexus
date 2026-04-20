#!/usr/bin/env bash
set -e

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$BASE_DIR"

if [ ! -f frontend.pid ]; then
  echo "Arquivo frontend.pid nao encontrado. Nada para parar."
  exit 0
fi

PID=$(cat frontend.pid)

if ps -p "$PID" >/dev/null 2>&1; then
  kill "$PID"
  sleep 2
  if ps -p "$PID" >/dev/null 2>&1; then
    echo "Processo ainda ativo. Forcando encerramento..."
    kill -9 "$PID"
  fi
  echo "Frontend parado com sucesso."
else
  echo "Processo PID $PID nao estava em execucao."
fi

rm -f frontend.pid
