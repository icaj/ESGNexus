#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"

echo "Instalando dependencias do sistema..."
sudo apt update
sudo apt install -y python3 python3-venv python3-pip build-essential libpq-dev

if [ ! -f .env ]; then
  cp .env.example .env
  echo "Arquivo .env criado a partir de .env.example."
  echo "Edite o arquivo .env e informe a sua DATABASE_URL do NeonDB antes de executar em producao."
fi

echo "Criando ambiente virtual Python..."
python3 -m venv .venv
source .venv/bin/activate

echo "Instalando bibliotecas Python..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Iniciando backend..."
./executar_backend.sh
