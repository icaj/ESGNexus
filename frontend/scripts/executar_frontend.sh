#!/usr/bin/env bash
set -e

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$BASE_DIR"

if ! command -v node >/dev/null 2>&1; then
  echo "Node.js nao encontrado. Execute primeiro ./instalar_e_executar_frontend.sh"
  exit 1
fi

if [ ! -d node_modules ]; then
  echo "Dependencias nao encontradas. Executando npm install..."
  npm install
fi

if [ ! -f .env.local ]; then
  cat > .env.local <<ENV
NEXT_PUBLIC_API_URL=http://localhost:8080
ENV
fi

if [ -f frontend.pid ] && ps -p "$(cat frontend.pid)" >/dev/null 2>&1; then
  echo "Frontend ja esta em execucao com PID $(cat frontend.pid)"
  exit 0
fi

nohup npm run dev > frontend.log 2>&1 &
echo $! > frontend.pid

echo "Frontend iniciado com sucesso."
echo "PID: $(cat frontend.pid)"
echo "Acesse: http://localhost:3000"
