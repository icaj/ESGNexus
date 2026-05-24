# Atualizacao do backend FastAPI

Esta versao remove o uso de `@app.on_event("startup")`, que esta obsoleto no FastAPI, e passa a usar o mecanismo recomendado `lifespan` com `asynccontextmanager`.

Tambem foi fixada a versao do pacote `bcrypt==4.0.1` para evitar o erro:

```text
AttributeError: module 'bcrypt' has no attribute '__about__'
```

## Como atualizar dependencias

```bash
source .venv/bin/activate
pip install -r requirements.txt --upgrade --force-reinstall
```

## Como executar

```bash
./executar_backend.sh
```

Ou diretamente:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8080
```
