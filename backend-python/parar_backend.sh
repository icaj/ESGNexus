#!/usr/bin/env bash
set -e

if [ ! -f "backend-python.pid" ]; then
  echo "Arquivo backend-python.pid nao encontrado."
  exit 0
fi

PID=$(cat backend-python.pid)
if kill -0 "$PID" 2>/dev/null; then
  kill "$PID"
  echo "Backend parado. PID: $PID"
else
  echo "Processo nao estava em execucao."
fi

rm -f backend-python.pid
