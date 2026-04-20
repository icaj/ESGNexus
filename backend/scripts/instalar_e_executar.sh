#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_YML="$ROOT_DIR/src/main/resources/application.yml"
APP_PROD_YML="$ROOT_DIR/application-prod.yml"

echo "[1/7] Verificando sistema operacional..."
if ! command -v apt >/dev/null 2>&1; then
  echo "Este script foi preparado para Ubuntu/Debian (apt)."
  echo "Instale manualmente: Java 21, Maven e MariaDB e depois execute ./executar_backend.sh"
  exit 1
fi

echo "[2/7] Instalando pacotes do sistema..."
sudo apt update
sudo apt install -y openjdk-21-jdk maven mariadb-server curl unzip

echo "[3/7] Habilitando e iniciando MariaDB..."
sudo systemctl enable mariadb
sudo systemctl restart mariadb

echo "[4/7] Criando banco e usuario da aplicacao..."
sudo mysql <<'SQL'
CREATE DATABASE IF NOT EXISTS esg_nexus CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'esg_user'@'localhost' IDENTIFIED BY 'esg_pass';
ALTER USER 'esg_user'@'localhost' IDENTIFIED BY 'esg_pass';
GRANT ALL PRIVILEGES ON esg_nexus.* TO 'esg_user'@'localhost';
FLUSH PRIVILEGES;
SQL

echo "[5/7] Validando estrutura do projeto..."
if [[ ! -f "$ROOT_DIR/pom.xml" ]]; then
  echo "Arquivo pom.xml nao encontrado em: $ROOT_DIR"
  echo "Coloque este script na raiz do backend Spring Boot."
  exit 1
fi

if [[ ! -f "$APP_YML" ]]; then
  echo "Arquivo application.yml nao encontrado em: $APP_YML"
  exit 1
fi

echo "[6/7] Compilando projeto com Maven..."
cd "$ROOT_DIR"
mvn clean package -DskipTests

echo "[7/7] Iniciando aplicacao..."
if [[ -f "$APP_PROD_YML" ]]; then
  echo "Usando configuracao externa: application-prod.yml"
  SPRING_CONFIG_ADDITIONAL_LOCATION="file:$APP_PROD_YML" \
  nohup java -jar target/esg-nexus-backend-0.0.1-SNAPSHOT.jar \
    --spring.profiles.active=prod \
    > backend.log 2>&1 &
else
  nohup java -jar target/esg-nexus-backend-0.0.1-SNAPSHOT.jar > backend.log 2>&1 &
fi

echo $! > backend.pid
sleep 5

echo "Aplicacao iniciada."
echo "PID: $(cat backend.pid)"
echo "Log: $ROOT_DIR/backend.log"
echo "Swagger: http://localhost:8080/swagger-ui.html"
echo "Para parar: ./parar_backend.sh"
