#!/usr/bin/env bash
set -Eeuo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_PROD_YML="$ROOT_DIR/application-prod.yml"
JAR_FILE="$ROOT_DIR/target/esg-nexus-backend-0.0.1-SNAPSHOT.jar"
PID_FILE="$ROOT_DIR/backend.pid"
LOG_FILE="$ROOT_DIR/backend.log"

cd "$ROOT_DIR"

if [[ ! -f pom.xml ]]; then
  echo "Arquivo pom.xml nao encontrado. Execute este script na raiz do backend."
  exit 1
fi

if [[ -f "$PID_FILE" ]] && ps -p "$(cat "$PID_FILE")" >/dev/null 2>&1; then
  echo "Backend ja esta em execucao com PID $(cat "$PID_FILE")."
  exit 0
fi

echo "Compilando pacote..."
mvn clean package -DskipTests

if [[ ! -f "$JAR_FILE" ]]; then
  echo "JAR nao encontrado em $JAR_FILE"
  exit 1
fi

echo "Iniciando backend..."
if [[ -f "$APP_PROD_YML" ]]; then
  SPRING_CONFIG_ADDITIONAL_LOCATION="file:$APP_PROD_YML" \
  nohup java -jar "$JAR_FILE" --spring.profiles.active=prod > "$LOG_FILE" 2>&1 &
else
  nohup java -jar "$JAR_FILE" > "$LOG_FILE" 2>&1 &
fi

echo $! > "$PID_FILE"
sleep 5

echo "Backend iniciado com PID $(cat "$PID_FILE")"
echo "Log: $LOG_FILE"
echo "Swagger: http://localhost:8080/swagger-ui.html"
