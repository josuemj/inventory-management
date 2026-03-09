# Inventory Management API

Backend en FastAPI con arquitectura monolítica modular para inventario.

## Stack

- FastAPI
- SQLAlchemy
- PostgreSQL

## Estructura

```text
app/
  api/
  core/
  db/
  modules/
    companies/
    users/
db/
  inventory-creation.sql
```

## Configuración

1. Crear entorno virtual e instalar dependencias:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Crear archivo `.env` desde `.env.example` y ajustar credenciales:

```powershell
Copy-Item .env.example .env
```

3. Ejecutar script SQL en db local para crear la base de datos y tablas:

- [db/inventory-creation.sql](C:/Users/josue/coding/inventory-management/db/inventory-creation.sql)

## Ejecutar API

```powershell
uvicorn app.main:app --reload
```

Docs:

- `http://127.0.0.1:8000/docs`

## Endpoints base

- `GET /health`
- `GET /api/v1/companies`
- `POST /api/v1/companies`
- `GET /api/v1/users`
- `POST /api/v1/users`
