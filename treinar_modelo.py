#!/usr/bin/env python3
"""Entry point: treina os modelos ESG com dados Kaggle (CRISP-DM Fases 2–6)."""
import argparse, sys
from esg_ml.aplicacao.servico_treinamento import ServicoTreinamento

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--mlflow', action='store_true', help='Registrar no MLflow')
    args = parser.parse_args()
    metricas = ServicoTreinamento().treinar(usar_mlflow=args.mlflow)
    print('\nMétricas finais:')
    for k,v in metricas.items(): print(f'  {k}: {v}')
