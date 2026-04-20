#!/usr/bin/env bash
set -e

BASE_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$BASE_DIR"

echo "[1/6] Atualizando pacotes..."
sudo apt update

echo "[2/6] Instalando Node.js LTS, npm, unzip e curl..."
sudo apt install -y curl unzip ca-certificates gnupg

if ! command -v node >/dev/null 2>&1; then
  curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
  sudo apt install -y nodejs
fi

echo "[3/6] Validando versoes..."
node -v
npm -v

echo "[4/6] Instalando dependencias do projeto..."
npm install

echo "[5/6] Garantindo arquivo .env.local..."
if [ ! -f .env.local ]; then
  if [ -f .env.local.exemplo ]; then
    cp .env.local.exemplo .env.local
  else
    cat > .env.local <<ENV
NEXT_PUBLIC_API_URL=http://localhost:8080
ENV
  fi
fi

echo "[6/6] Iniciando frontend em segundo plano..."
if [ -f frontend.pid ] && ps -p "$(cat frontend.pid)" >/dev/null 2>&1; then
  echo "Frontend ja esta em execucao com PID $(cat frontend.pid)"
  exit 0
fi

nohup npm run dev > frontend.log 2>&1 &
echo $! > frontend.pid

echo "Frontend iniciado."
echo "PID: $(cat frontend.pid)"
echo "Log: $BASE_DIR/frontend.log"
echo "URL esperada: http://localhost:3000"
