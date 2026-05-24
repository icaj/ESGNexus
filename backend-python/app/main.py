from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.config import settings
from app.db.schema import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Eventos de inicializacao/finalizacao da aplicacao.

    Substitui o antigo @app.on_event("startup"), que foi descontinuado
    nas versoes recentes do FastAPI/Starlette.
    """
    init_db()
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.1",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok", "app": settings.app_name}


app.include_router(router)
