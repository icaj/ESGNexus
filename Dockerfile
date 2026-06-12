# ── Estágio de build ──────────────────────────────────────────────────────────
FROM python:3.11-slim-bookworm AS builder

WORKDIR /app

# Dependências de sistema necessárias para compilar extensões C do psycopg
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --prefix=/install -r requirements.txt


# ── Estágio de produção ───────────────────────────────────────────────────────
FROM python:3.11-slim-bookworm

WORKDIR /app

# ca-certificates: necessário para conexões TLS com NeonDB e outros serviços em nuvem
RUN apt-get update && apt-get install -y --no-install-recommends \
        ca-certificates \
        libpq5 \
    && rm -rf /var/lib/apt/lists/*

# Copia apenas os pacotes instalados (sem ferramentas de build)
COPY --from=builder /install /usr/local

# Usuário não-root para execução segura em produção (GCP / Cloud Run)
RUN groupadd --gid 1001 appgroup \
    && useradd --uid 1001 --gid appgroup --no-create-home appuser

COPY --chown=appuser:appgroup . .

# Cria diretórios de dados com permissão correta
RUN mkdir -p artifacts data/bronze data/processado data/resultados \
    && chown -R appuser:appgroup artifacts data

USER appuser

# Porta padrão da API; o Streamlit usa 8501
EXPOSE 8000 8501

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH="/usr/local/bin:$PATH"

CMD ["uvicorn", "esg_ml.interfaces.api.principal:app", "--host", "0.0.0.0", "--port", "8000"]
