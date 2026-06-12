from __future__ import annotations

from datetime import datetime
import os

from airflow import DAG
from airflow.operators.bash import BashOperator

URL_API = os.getenv("ESG_NEXUS_API_URL", "http://api:8000")

with DAG(
    dag_id="dag_treinamento_esg",
    start_date=datetime(2026, 1, 1),
    schedule="0 2 * * *",
    catchup=False,
    tags=["esg", "machine-learning", "fornecedores"],
) as dag:
    verificar_api = BashOperator(
        task_id="verificar_api",
        bash_command=f"curl --fail --silent {URL_API}/saude",
    )

    treinar_modelo = BashOperator(
        task_id="treinar_modelo_esg",
        bash_command=f"curl --fail --silent -X POST {URL_API}/treinar",
    )

    gerar_dashboards = BashOperator(
        task_id="gerar_dashboards_html",
        bash_command=f"curl --fail --silent -X POST {URL_API}/dashboards/gerar",
    )

    verificar_api >> treinar_modelo >> gerar_dashboards
