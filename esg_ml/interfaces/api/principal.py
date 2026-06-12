# esg_ml/interfaces/api/principal.py
from pathlib import Path
from tempfile import NamedTemporaryFile
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from esg_ml.infraestrutura.banco_dados import criar_tabelas
from esg_ml.infraestrutura.configuracoes import Configuracoes
from esg_ml.infraestrutura.registro_log import configurar_registro_log
from esg_ml.interfaces.api.rotas_auth import roteador as roteador_auth
from esg_ml.interfaces.api.rotas_enterprise import roteador as roteador_enterprise

configurar_registro_log()
conf = Configuracoes()
aplicacao = FastAPI(title=conf.nome_aplicacao, version='1.0.0-merged')
aplicacao.add_middleware(CORSMiddleware,
    allow_origins=['http://localhost:5173','http://localhost:3000','http://localhost:8501'],
    allow_credentials=True, allow_methods=['*'], allow_headers=['*'])
criar_tabelas()
aplicacao.include_router(roteador_auth)
aplicacao.include_router(roteador_enterprise)

@aplicacao.get('/saude')
def verificar_saude() -> dict:
    from esg_ml.adaptadores.saida.repositorio_modelo_joblib import RepositorioModeloJoblib
    rep = RepositorioModeloJoblib(conf.diretorio_artefatos)
    return {
        'status': 'ok',
        'modelo_knn_carregado': rep.existe('modelo_knn'),
        'modelo_rf_carregado':  rep.existe('modelo_rf'),
        'config_carregado':     rep.existe('config'),
    }

app = aplicacao
