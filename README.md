# IDB_JOVEM_BACKEND

## Subindo o ambiente do zero

Pré-requisitos: Docker + Docker Compose, e um arquivo `.env` na raiz com as variáveis usadas pelos composes (Postgres local, Supabase, Keycloak, Google OAuth).

Os comandos abaixo estão em PowerShell (Windows). Em bash basta usar a mesma sintaxe.

### Fluxo DEV (Postgres local + Keycloak + backend)

Usa apenas o `docker-compose.yml`. Sobe um Postgres local em `localhost:5434`, o Keycloak em `localhost:8080` e o backend em `localhost:8000`.

```powershell
# 1. Para tudo e zera volumes (apaga o banco local)
docker compose down -v

# 2. Rebuild forcado da imagem do backend
docker compose build --no-cache jovem-backend

# 3. Sobe Postgres + Keycloak + backend
docker compose up -d

# 4. Aplica as migrations no Postgres local
docker compose exec jovem-backend alembic upgrade head

# 5. (opcional) Acompanha logs do backend
docker compose logs -f jovem-backend
```

### Fluxo PROD (Supabase + Keycloak + backend, sem Postgres local)

Combina `docker-compose.yml` com o overlay `docker-compose.supabase.yml`, que aponta backend e Keycloak para o Supabase e remove a dependencia do `db` local. O serviço `db` nao e instanciado porque subimos apenas `jovem-backend` e `keycloak` explicitamente.

```powershell
# 1. Para tudo e remove volumes locais (nao afeta o Supabase)
docker compose -f docker-compose.yml -f docker-compose.supabase.yml down -v

# 2. Rebuild forcado da imagem
docker compose -f docker-compose.yml -f docker-compose.supabase.yml build --no-cache jovem-backend

# 3. Sobe apenas backend + keycloak (ambos apontam para o Supabase)
docker compose -f docker-compose.yml -f docker-compose.supabase.yml up -d jovem-backend keycloak

# 4. Aplica migrations no Supabase
docker compose -f docker-compose.yml -f docker-compose.supabase.yml exec jovem-backend alembic upgrade head

# 5. (opcional) Logs do backend
docker compose -f docker-compose.yml -f docker-compose.supabase.yml logs -f jovem-backend
```

## Testes e Lint

Os mesmos comandos rodados pelo CI (`.github/workflows/ci.yml`). Pré-requisito: `pip install -r requirements.txt`.

### Lint (Pylint)

```powershell
pylint src/ --fail-under=6.0 --disable=C0114,C0115,C0116,E0401,R0801 --ignore=migrations
```

### Testes + coverage (Pytest)

Usa a configuração de `pytest.ini` (exclui testes marcados como `endpoint` e gera coverage em `htmlcov/` e `coverage.xml`).

```powershell
pytest
```

### Testes de endpoint (contra container rodando)

Sobe o backend antes (ver "Fluxo DEV" acima) e rode:

```powershell
pytest tests/endpoint/ -v -m endpoint
```

## Keycloak — Gerar token de acesso

Pré-requisito: Keycloak rodando (fluxo DEV em `localhost:8080`) com o realm `jovem` e o client `jovem-backend` configurados. Ajuste `username`/`password` para um usuário existente no realm.

```powershell
$response = Invoke-RestMethod -Method Post `
    -Uri "http://localhost:8080/realms/jovem/protocol/openid-connect/token" `
    -ContentType "application/x-www-form-urlencoded" `
    -Body @{
        username   = "admin"
        password   = "admin"
        client_id  = "jovem-backend"
        grant_type = "password"
    }
$response.access_token
```

O `access_token` retornado pode ser usado no header `Authorization: Bearer <token>` das chamadas para o backend.
