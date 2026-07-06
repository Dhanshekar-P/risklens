# RiskLens

Production-oriented Financial Risk Intelligence Platform built using FastAPI.

## Features

- JWT Authentication
- Portfolio Management
- Historical Market Data
- Risk Analytics
- AI Risk Insights
- Dockerized Deployment

## Tech Stack

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Docker
- JWT
- Pandas
- NumPy

## Run

```bash
docker compose up -d

source venv/bin/activate

uvicorn app.main:app --reload
```

## API Docs

```
http://127.0.0.1:8000/docs
```
