#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
#source .venv/bin/activate
nohup streamlit run app.py --server.address 0.0.0.0 --server.port 8501 > frontend.log 2>&1 &
echo $! > frontend.pid
echo "Frontend iniciado em http://localhost:8501"
echo "PID: $(cat frontend.pid)"
