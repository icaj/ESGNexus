
from __future__ import annotations

import io
import json
import threading
import traceback
from contextlib import redirect_stdout, redirect_stderr
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .ml_pipeline.main import start as executar_pipeline_kaggle

ROOT_DIR = Path(__file__).resolve().parent.parent
STATUS_FILE = ROOT_DIR / "data" / "processado" / "treinamento_status.json"
LOG_FILE = ROOT_DIR / "data" / "processado" / "treinamento_pipeline.log"
LOCK = threading.Lock()
_thread: threading.Thread | None = None


def _agora() -> str:
    return datetime.now(timezone.utc).isoformat()


def _salvar_status(status: dict[str, Any]) -> dict[str, Any]:
    STATUS_FILE.parent.mkdir(parents=True, exist_ok=True)
    status["atualizado_em"] = _agora()
    STATUS_FILE.write_text(json.dumps(status, ensure_ascii=False, indent=2), encoding="utf-8")
    return status


def obter_status_treinamento() -> dict[str, Any]:
    if STATUS_FILE.exists():
        try:
            return json.loads(STATUS_FILE.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {"status": "NAO_EXECUTADO", "mensagem": "Nenhum treinamento foi executado ainda.", "log_tail": ""}


def _artefatos() -> dict[str, Any]:
    arquivos = []
    for pasta in [ROOT_DIR / "modelos", ROOT_DIR / "data" / "bronze", ROOT_DIR / "data" / "processado"]:
        if pasta.exists():
            for item in pasta.glob("*"):
                if item.is_file():
                    arquivos.append({
                        "arquivo": str(item.relative_to(ROOT_DIR)),
                        "tamanho_bytes": item.stat().st_size,
                        "modificado_em": datetime.fromtimestamp(item.stat().st_mtime, timezone.utc).isoformat(),
                    })
    return {"arquivos": sorted(arquivos, key=lambda x: x["arquivo"])}


def _executar() -> None:
    buffer = io.StringIO()
    status_base = {
        "status": "EXECUTANDO",
        "mensagem": "Pipeline de treinamento iniciado.",
        "iniciado_em": _agora(),
        "finalizado_em": None,
        "erro": None,
        "artefatos": {},
        "log_tail": "",
    }
    _salvar_status(status_base)
    try:
        with redirect_stdout(buffer), redirect_stderr(buffer):
            executar_pipeline_kaggle()
        log = buffer.getvalue()
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        LOG_FILE.write_text(log, encoding="utf-8")
        _salvar_status({
            **status_base,
            "status": "CONCLUIDO",
            "mensagem": "Pipeline concluido com sucesso. Modelos e artefatos gerados.",
            "finalizado_em": _agora(),
            "artefatos": _artefatos(),
            "log_tail": log[-8000:],
        })
    except Exception as exc:
        log = buffer.getvalue() + "\n" + traceback.format_exc()
        LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
        LOG_FILE.write_text(log, encoding="utf-8")
        _salvar_status({
            **status_base,
            "status": "ERRO",
            "mensagem": f"Falha ao executar pipeline: {exc}",
            "finalizado_em": _agora(),
            "erro": str(exc),
            "log_tail": log[-8000:],
        })


def iniciar_treinamento(force: bool = False) -> dict[str, Any]:
    global _thread
    with LOCK:
        if _thread and _thread.is_alive():
            return {"status": "EXECUTANDO", "mensagem": "Ja existe um treinamento em execucao."}
        status_atual = obter_status_treinamento()
        if status_atual.get("status") == "CONCLUIDO" and not force:
            return {"status": "CONCLUIDO", "mensagem": "Modelo ja treinado. Use force=true para retreinar.", **status_atual}
        _thread = threading.Thread(target=_executar, daemon=True)
        _thread.start()
        return {"status": "EXECUTANDO", "mensagem": "Treinamento iniciado em segundo plano."}
