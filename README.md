# DevMind

DevMind is a React and FastAPI application for tracking developer activity,
focus, cognitive load, and burnout indicators.

## Repository layout

- `frontend/` — React and Vite browser application
- `backend/app/` — FastAPI application
- `backend/scripts/` — explicit diagnostic and data-management utilities
- `backend/data/sample/` — non-sensitive sample datasets
- `backend/tests/` — backend tests

## Security setup

The browser receives only public configuration such as `VITE_API_BASE_URL`.
Database credentials, JWT secrets, and AI-provider keys belong in
`backend/.env` or the deployment platform's secret manager.

The database credential previously committed to this repository must be
rotated in Neon. Removing it from the current files does not revoke it or
remove it from existing Git history.

## Backend

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

The default development database is SQLite. Set `DATABASE_URL` in
`backend/.env` to use PostgreSQL.

## Frontend

```powershell
cd frontend
npm install
Copy-Item .env.example .env.local
npm run dev
```

## Checks

```powershell
cd backend
python -m pytest
python -m ruff check .

cd ..\frontend
npm run build
npm run lint
```
