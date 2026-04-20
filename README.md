# ESG Nexus — Especificação técnica do software

## 1. Visão geral

O **ESG Nexus** será uma plataforma web para **análise, monitoramento e ranking de aderência às práticas ESG** de fornecedores.

A solução terá:

* **Frontend:** Next.js
* **Backend:** Java com Spring Boot
* **Banco de dados:** MySQL ou MariaDB
* **Sistema operacional de implantação:** Linux

## 2. Objetivos do sistema

O sistema deverá permitir:

* autenticação de usuários
* cadastro manual e importação em lote de fornecedores
* manutenção de certificações e evidências ESG
* cálculo de score ESG por fornecedor
* visualização de ranking de fornecedores
* dashboards analíticos
* geração de alertas de vencimento e não conformidade
* parametrização do modelo de avaliação ESG
* controle de usuários, perfis e permissões

---

## 3. Arquitetura da solução

## 3.1 Arquitetura em camadas

### Frontend

Aplicação SPA com **Next.js**.

Responsabilidades:

* login
* telas de cadastro e consulta
* dashboards
* filtros e ranking
* upload/importação de arquivos CSV/XLSX
* consumo da API REST do backend

### Backend

API REST em **Java Spring Boot**.

Responsabilidades:

* autenticação/autorização
* regras de negócio ESG
* cálculo de score e ranking
* importação e validação de fornecedores
* processamento de alertas
* persistência em banco
* auditoria de ações

### Banco de dados

**MySQL/MariaDB** para persistência transacional.

Responsabilidades:

* usuários
* fornecedores
* avaliações
* certificações
* alertas
* parâmetros e pesos ESG
* histórico de score

---

## 4. Arquitetura tecnológica

## 4.1 Frontend

* Next.js 15+
* TypeScript
* Tailwind CSS
* Shadcn UI ou Material UI
* React Hook Form
* Zod para validação
* Axios ou Fetch API
* Recharts para gráficos
* TanStack Table para grids
* NextAuth ou autenticação própria com JWT

## 4.2 Backend

* Java 21
* Spring Boot 3.x
* Spring Web
* Spring Security
* Spring Data JPA
* Hibernate
* Bean Validation
* Flyway ou Liquibase
* OpenAPI / Swagger
* Lombok
* MapStruct
* Apache POI para importação XLSX
* biblioteca CSV para importação em lote

## 4.3 Banco e infraestrutura

* MySQL 8 ou MariaDB 11
* Docker e Docker Compose
* Nginx como reverse proxy
* Linux Ubuntu Server ou Debian

---

## 5. Perfis de usuário

### Administrador

* gerencia usuários
* configura pesos ESG
* aprova regras
* consulta todos os dashboards
* gerencia integrações

### Analista ESG

* cadastra e edita fornecedores
* registra certificações
* avalia critérios ESG
* acompanha alertas
* emite relatórios

### Gestor

* acompanha ranking
* consulta dashboards
* visualiza alertas críticos
* compara fornecedores

### Auditor/Consulta

* acesso somente leitura
* consulta relatórios e evidências

---

## 6. Módulos do sistema

## 6.1 Módulo de autenticação

### Funcionalidades

* login
* logout
* recuperação de senha
* troca de senha
* controle por perfil
* trilha de auditoria

### Tela

* e-mail/usuário
* senha
* botão entrar
* link esqueci minha senha

---

## 6.2 Módulo de fornecedores

### Funcionalidades

* cadastro manual
* edição
* consulta com filtros
* importação CSV/XLSX
* associação de segmento, porte e criticidade
* status do fornecedor
* upload de evidências/documentos

### Dados principais do fornecedor

* razão social
* nome fantasia
* CNPJ
* e-mail
* telefone
* responsável
* segmento
* categoria
* país/estado/cidade
* nível de risco
* status
* data de cadastro

### Tela

* listagem com pesquisa
* botão novo fornecedor
* botão importar fornecedores
* filtros por status, segmento, score e certificação

---

## 6.3 Módulo ESG

### Dimensões avaliadas

* **E**: Ambiental
* **S**: Social
* **G**: Governança

### Funcionalidades

* cadastro de critérios ESG
* definição de pesos por dimensão
* definição de perguntas/indicadores
* avaliação por fornecedor
* anexação de evidências
* cálculo automático de score

### Exemplo de critérios

#### Ambiental

* política ambiental formalizada
* gestão de resíduos
* consumo de água e energia
* emissões de carbono monitoradas

#### Social

* políticas de diversidade e inclusão
* saúde e segurança do trabalho
* combate ao trabalho infantil e análogo à escravidão
* ações com comunidades

#### Governança

* código de ética
* canal de denúncias
* programa anticorrupção
* compliance e transparência

---

## 6.4 Módulo de certificações

### Funcionalidades

* cadastro de certificações
* vínculo ao fornecedor
* registro de validade
* upload de comprovantes
* alertas de vencimento

### Exemplos de certificações

* ISO 14001
* ISO 45001
* ISO 9001
* SA8000
* selo carbono neutro
* outras certificações ESG

### Tela

* listagem por fornecedor
* data de emissão
* data de validade
* status: válida, vencendo, vencida

---

## 6.5 Módulo de ranking

### Funcionalidades

* ranking geral de fornecedores
* ranking por dimensão ESG
* ranking por segmento
* comparação entre fornecedores
* histórico de evolução do score

### Regras do ranking

* score total de 0 a 100
* pesos configuráveis por dimensão
* fornecedor pode ter faixas:

  * A: 90 a 100
  * B: 75 a 89
  * C: 60 a 74
  * D: abaixo de 60

### Fórmula para cálculo de aderencia

```text
Score Final = (Score Ambiental × Peso E) + (Score Social × Peso S) + (Score Governança × Peso G)
```

Exemplo de pesos iniciais:

* Ambiental: 35%
* Social: 30%
* Governança: 35%

---

## 6.6 Módulo de dashboards

### Indicadores principais

* total de fornecedores cadastrados
* total avaliados
* média geral do score ESG
* distribuição por faixa de score
* top 10 fornecedores
* fornecedores críticos
* certificações vencidas ou a vencer
* evolução do score por período

### Gráficos

* barras: top fornecedores
* pizza: distribuição por faixas
* linha: evolução do score
* cards: KPIs principais
* mapa de calor: aderência por critério

---

## 6.7 Módulo de alertas

### Tipos de alerta

* certificação vencendo
* certificação vencida
* fornecedor com score abaixo do mínimo
* fornecedor sem avaliação recente
* fornecedor sem documentação obrigatória
* alteração de score para baixo

### Canais

* alertas em tela
* envio por e-mail

### Tela

* lista de alertas
* severidade
* data do evento
* fornecedor
* status do alerta
* ação tomada

---

## 6.8 Módulo de configurações

### Funcionalidades

* manutenção dos pesos ESG
* cadastro de tipos de certificação
* parâmetros de alertas
* perfis e permissões
* configurações de e-mail
* periodicidade de reavaliação

---

## 7. Estrutura do banco de dados

## 7.1 Tabelas principais

### usuario

* id
* nome
* email
* password_hash
* id_perfil
* ativo
* criado_em
* atualizado_em

### perfil

* id
* nome
* descricao

### fornecedor

* id
* razao_social
* nome_fantasia
* cnpj
* email
* telefone
* nome_contato
* segmento
* categoria
* pais
* estado
* cidade
* nivel_risco
* status
* criado_em
* atualizado_em

### dimensao_esg

* id
* codigo (E, S, G)
* nome
* peso

### criterio_esg

* id
* id_dimensao
* nome
* descricao
* score_max
* obrigatorio
* ativo

### avaliacao_fornecedor

* id
* id_fornecedor
* data_avaliacao
* score_ambiente
* score_social
* score_governanca
* scoire_final
* posicao_rank
* observacoes
* criado_por

### item_avaliacao_fornecedor

* id
* id_avaliacao
* id_criterio
* score
* evidencia_url
* commentario

### certificacao

* id
* nome
* descricao
* emissor

### certificacao_fornecedor

* id
* id_fornecedor
* id_certificacao
* data_emissao
* data_expiracao
* status
* url_arquivo

### alerta

* id
* id_fornecedor
* tipo_alerta
* severidade
* titulo
* descricao
* data_vencimento
* status
* criado_em
* resolvido_em

### config

* id
* chave
* valor

### audit_log

* id
* id_usuario
* acao
* entidade
* id_entidade
* detalhes
* criado_em

---

## 8. Modelo relacional resumido

```text
perfil 1---N usuario
fornecedor 1---N avaliacao_fornecedor
avaliacao_fornecedor 1---N item_avaliacao_fornecedor
dimensao_esg 1---N criterio_esg
criterio_esg 1---N item_avaliacao_fornecedor
fornecedor 1---N certificacao_fornecedor
certifications 1---N certificacao_fornecedor
fornecedor 1---N alerta
usuario 1---N audit_log
```

---

## 9. APIs REST

## 9.1 Autenticação

* POST /api/auth/login
* POST /api/auth/forgot-password
* POST /api/auth/reset-password
* GET /api/auth/me

## 9.2 Fornecedores

* GET /api/suppliers
* GET /api/suppliers/{id}
* POST /api/suppliers
* PUT /api/suppliers/{id}
* DELETE /api/suppliers/{id}
* POST /api/suppliers/import

## 9.3 Avaliações ESG

* GET /api/assessments
* GET /api/assessments/{id}
* POST /api/assessments
* PUT /api/assessments/{id}
* GET /api/suppliers/{id}/score-history

## 9.4 Critérios e configuração ESG

* GET /api/esg/dimensions
* PUT /api/esg/dimensions/weights
* GET /api/esg/criteria
* POST /api/esg/criteria
* PUT /api/esg/criteria/{id}

## 9.5 Certificações

* GET /api/certifications
* POST /api/certifications
* POST /api/suppliers/{id}/certifications
* PUT /api/supplier-certifications/{id}

## 9.6 Ranking e dashboards

* GET /api/ranking
* GET /api/ranking/top10
* GET /api/dashboard/kpis
* GET /api/dashboard/charts

## 9.7 Alertas

* GET /api/alerts
* PUT /api/alerts/{id}/resolve

## 9.8 Usuários e perfis

* GET /api/users
* POST /api/users
* PUT /api/users/{id}
* GET /api/roles

---

## 10. Telas do frontend

## 10.1 Login

* usuário/e-mail
* senha
* recuperar senha

## 10.2 Dashboard principal

* cards com KPIs
* ranking dos top fornecedores
* gráfico por dimensão ESG
* alertas recentes
* certificações próximas do vencimento

## 10.3 Fornecedores

* listagem
* filtro avançado
* formulário de cadastro
* importação em lote
* detalhes do fornecedor

## 10.4 Avaliação ESG

* formulário por critérios
* campos de score
* upload de evidências
* observações

## 10.5 Certificações

* listagem
* cadastro
* validade
* comprovantes

## 10.6 Ranking

* tabela ranqueada
* filtros por segmento/categoria
* comparação entre fornecedores

## 10.7 Alertas

* listagem por severidade
* filtro por status
* ação de resolução

## 10.8 Configurações

* pesos ESG
* parâmetros de alerta
* usuários
* perfis
* tipos de certificação

---

## 11. Estrutura de pastas

## 11.1 Frontend Next.js

```text
frontend/
  src/
    app/
      login/
      dashboard/
      suppliers/
      ranking/
      alerts/
      settings/
    components/
      ui/
      charts/
      forms/
      layout/
    services/
      api.ts
      auth.ts
      suppliers.ts
      dashboard.ts
    types/
    hooks/
    lib/
  public/
  package.json
```

## 11.2 Backend Java Spring Boot

```text
backend/
  src/main/java/com/esgnexus/
    config/
    controller/
    service/
    repository/
    domain/
    dto/
    mapper/
    security/
    exception/
  src/main/resources/
    db/migration/
    application.yml
  pom.xml
```

---

## 12. Requisitos não funcionais

* autenticação segura com JWT
* senhas com hash BCrypt
* logs de auditoria
* responsividade
* suporte a grande volume de fornecedores
* importação em lote eficiente
* API documentada com Swagger
* deploy via Docker em Linux
* backup do banco
* controle de acesso por perfil

---

## 13. Estratégia de implantação em Linux

## 13.1 Componentes

* container do frontend Next.js
* container do backend Spring Boot
* container do MySQL/MariaDB
* container opcional do Nginx

## 13.2 Docker Compose

Serviços sugeridos:

* `frontend`
* `backend`
* `db`
* `nginx`

---

## 14. Exemplo de fluxo principal

1. usuário acessa tela de login
2. backend autentica e retorna token JWT
3. usuário cadastra ou importa fornecedores
4. analista registra avaliações ESG e certificações
5. backend calcula score final
6. sistema atualiza ranking
7. dashboards exibem indicadores
8. alertas são gerados automaticamente quando necessário

---

## 15. Roadmap de implementação

## Fase 1 — MVP

* login
* cadastro de usuários
* cadastro de fornecedores
* importação CSV/XLSX
* cadastro de certificações
* avaliação ESG básica
* ranking simples
* dashboard inicial

## Fase 2

* alertas automáticos
* histórico de score
* comparação de fornecedores
* auditoria completa
* parametrização avançada de pesos

## Fase 3

* workflow de aprovação
* integração com ERP/portais externos
* envio automático de questionários ESG
* BI avançado
* relatórios PDF/Excel

---

## 16. Recomendação de stack final

### Frontend

* Next.js + TypeScript + Tailwind + Shadcn UI

### Backend

* Java 21 + Spring Boot + Spring Security + JPA

### Banco

* MariaDB

### Deploy

* Docker Compose para Linux Ubuntu Server

### Observação

MariaDB foi escolhido para reduzir custo e manter compatibilidade.

---

## 17. Diferenciais competitivos

* score ESG configurável
* ranking comparativo por fornecedor
* monitoramento de vencimento de certificações
* trilha de auditoria
* importação em lote
* foco específico em gestão de fornecedores
* dashboards executivos e operacionais

---

## 18. Próximos passos

Transformar esta especificação em:

1. Adaptação da modelagem física do banco MySQL/MariaDB aos novos requisitos dos dados entregues pelo CESAR
2. Ajustar os wireframes das telas
3. estrutura inicial do projeto Next.js + Spring Boot
4. endpoints REST já implementados
5. docker-compose para rodar em Linux
6. GitHub Actions para CI/CD (a implementar)
