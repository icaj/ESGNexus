# Scripts prontos para o backend ESG Nexus

Coloque estes arquivos na raiz do backend, no mesmo nivel do `pom.xml`.

## Arquivos
- `instalar_e_executar.sh`
- `executar_backend.sh`
- `parar_backend.sh`
- `application-prod.yml`

## Permissao de execucao
```bash
chmod +x instalar_e_executar.sh executar_backend.sh parar_backend.sh
```

## Uso rapido
### Instalar dependencias do sistema, preparar banco e iniciar o backend
```bash
./instalar_e_executar.sh
```

### Apenas compilar e iniciar o backend
```bash
./executar_backend.sh
```

### Parar o backend
```bash
./parar_backend.sh
```

## Variaveis opcionais antes de executar
```bash
export DB_HOST=localhost
export DB_PORT=3306
export DB_NAME=esg_nexus
export DB_USER=esg_user
export DB_PASSWORD=esg_pass
export JWT_SECRET='uma-chave-forte-com-tamanho-adequado'
```

## Observacoes
- O script de instalacao foi preparado para Ubuntu/Debian.
- O backend sera iniciado em background e gravara logs em `backend.log`.
- O PID ficara salvo em `backend.pid`.
