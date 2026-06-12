# esg_ml/adaptadores/entrada/leitor_fornecedores_pandas.py
# Porta: RepositorioEmpresas → CSV/Excel com colunas nexus_v2
import sys
import pandas as pd
from pathlib import Path
from typing import List
from esg_ml.dominio.entidades.empresa import Empresa, ScoreESG

COLUNAS_REQ = ['name','industry','environment_score','social_score','governance_score']

class LeitorFornecedoresPandas:
    def __init__(self, caminho):
        self.caminho = Path(caminho)

    def ler(self) -> List[Empresa]:
        return self.listar_empresas()

    def listar_empresas(self) -> List[Empresa]:
        try:
            df = (pd.read_excel(self.caminho)
                  if self.caminho.suffix.lower() in {'.xlsx','.xls'}
                  else pd.read_csv(self.caminho))
        except FileNotFoundError:
            print(f'[ERRO] Arquivo não encontrado: {self.caminho}')
            sys.exit(1)
        ausentes = [c for c in COLUNAS_REQ if c not in df.columns]
        if ausentes:
            raise ValueError(f'Colunas obrigatórias ausentes: {ausentes}')
        return [
            Empresa(
                name=str(row['name']),
                industry=str(row.get('industry','Unknown')),
                scores=ScoreESG(
                    environment_score=int(row['environment_score']),
                    social_score=int(row['social_score']),
                    governance_score=int(row['governance_score']),
                )
            )
            for _, row in df.iterrows()
        ]
