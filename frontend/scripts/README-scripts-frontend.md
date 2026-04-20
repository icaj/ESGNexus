# Scripts do frontend ESG Nexus

## Arquivos incluidos
- instalar_e_executar_frontend.sh
- executar_frontend.sh
- parar_frontend.sh
- .env.local.exemplo

## Onde colocar
Copie estes arquivos para a raiz do frontend, no mesmo nivel do `package.json`.

## Permissao de execucao
```bash
chmod +x instalar_e_executar_frontend.sh executar_frontend.sh parar_frontend.sh
```

## Instalacao completa + execucao
```bash
./instalar_e_executar_frontend.sh
```

## Apenas executar depois
```bash
./executar_frontend.sh
```

## Parar o frontend
```bash
./parar_frontend.sh
```

## Endereco padrao
- Frontend: `http://localhost:3000`
- Backend esperado: `http://localhost:8080`

## Variavel de ambiente
O frontend usa:
```env
NEXT_PUBLIC_API_URL=http://localhost:8080
```

Se quiser alterar, edite o arquivo `.env.local`.

## Logs e PID
Ao iniciar em segundo plano, os arquivos gerados serao:
- `frontend.log`
- `frontend.pid`

## Requisitos
Scripts preparados para Ubuntu/Debian.

Pacotes utilizados:
- Node.js 20
- npm
- curl
- unzip
