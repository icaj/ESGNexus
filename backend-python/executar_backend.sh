#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

if [ ! -d .venv ]; then
  python3 -m venv .venv
fi

source .venv/bin/activate
pip install -r requirements.txt >/dev/null

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Arquivo .env criado. Configure a DATABASE_URL do NeonDB antes de usar em producao."
fi

if [ -f backend.pid ] && kill -0 "$(cat backend.pid)" 2>/dev/null; then
  echo "Backend ja esta em execucao. PID: $(cat backend.pid)"
  exit 0
fi

nohup uvicorn app.main:app --host 0.0.0.0 --port 8080 > backend.log 2>&1 &
echo $! > backend.pid

echo "Backend iniciado em http://localhost:8080"
echo "Documentacao: http://localhost:8080/docs"
echo "PID: $(cat backend.pid)"
echo "Log: backend.log"
