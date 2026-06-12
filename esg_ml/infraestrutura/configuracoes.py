# esg_ml/infraestrutura/configuracoes.py
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Configuracoes(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', extra='ignore')

    nome_aplicacao:      str  = 'ESG Nexus Enterprise'
    diretorio_artefatos: Path = Path('artifacts')

    # Caminhos derivados (nexus_v2)
    @property
    def pasta_bronze(self) -> Path:
        return self.diretorio_artefatos.parent / 'data' / 'bronze'

    @property
    def pasta_saida(self) -> Path:
        return self.diretorio_artefatos.parent / 'data' / 'processado'

    @property
    def pasta_resultados(self) -> Path:
        return self.diretorio_artefatos.parent / 'data' / 'resultados'

    # MLflow
    mlflow_tracking_uri: str = 'http://localhost:5000'
    mlflow_experimento:  str = 'esg-nexus-fornecedores'

    # JWT / segurança (Enterprise)
    segredo_jwt:                str = 'troque-esta-chave-em-producao'
    algoritmo_jwt:              str = 'HS256'
    minutos_expiracao_token:    int = 480
