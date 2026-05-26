#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
source .venv/bin/activate

HOST=${APP_HOST:-0.0.0.0}
PORT=${APP_PORT:-8080}

nohup uvicorn app.main:app --host "$HOST" --port "$PORT" > backend.log 2>&1 &
echo $! > backend.pid
echo "Backend iniciado em http://localhost:$PORT"
echo "PID: $(cat backend.pid)"
