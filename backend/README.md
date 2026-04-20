# ESG Nexus Backend

Backend da solução ESG Nexus em Java + Spring Boot.

## Requisitos
- Java 21
- Maven 3.9+
- MariaDB ou MySQL

## Configuração do banco
Crie um banco chamado `esg_nexus` e ajuste o arquivo `src/main/resources/application.yml`.

## Usuário inicial
- e-mail: `admin@esgnexus.com`
- senha: `admin123`

## Executar localmente
```bash
mvn spring-boot:run
```

## Swagger
- `/swagger-ui.html`

## Endpoints principais
- `POST /api/auth/login`
- `GET /api/dashboard`
- `GET /api/fornecedores`
- `POST /api/fornecedores`
- `GET /api/avaliacoes`
- `POST /api/avaliacoes`
- `GET /api/certificacoes`
- `POST /api/certificacoes`
- `GET /api/alertas`
- `PUT /api/alertas/{id}/resolve`
- `GET /api/configuracoes`
- `POST /api/configuracoes`
