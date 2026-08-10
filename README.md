# AI Engineering with FastAPI, Transformers & Supabase

A FastAPI service that exposes Hugging Face `transformers` pipelines for **text generation** and **sentiment analysis**, and persists every request/response pair to a **Supabase (Postgres)** database.

## Features

- `POST /generate_text` — text generation using `Qwen/Qwen2.5-1.5B`
- `POST /analyze_sentiment` — sentiment analysis using `distilbert-base-uncased-finetuned-sst-2-english`
- `GET /` — health check reporting whether the models are loaded
- Every request is saved to Supabase Postgres (`text_generation` / `sentiment_analysis` tables)

## Project structure

```
app/
  main.py                # FastAPI app, routes, model loading (lifespan)
  models_validation.py    # Pydantic request/response models
  postgres_database.py    # Supabase Postgres connection + persistence
  sqlite_database.py      # Legacy local SQLite persistence (unused by main.py)
database/                 # Local SQLite file storage (gitignored)
Dockerfile
Makefile
requirements.in
runbook.md                # Step-by-step setup & usage guide
```

## Prerequisites

- [uv](https://docs.astral.sh/uv/)
- A Supabase project with a Postgres database

## Quick start

See [runbook.md](runbook.md) for the full step-by-step guide. Summary:

1. Install `uv` and create a virtual environment.
2. Create a `.env` file with your Supabase **Transaction pooler** connection details:
   ```
   DB_HOST=aws-0-<region>.pooler.supabase.com
   DB_PORT=6543
   DB_NAME=postgres
   DB_USER=postgres.<project-ref>
   DB_PASSWORD=<your-db-password>
   ```
   > Use the Transaction pooler host, not the direct `db.<project-ref>.supabase.co` host — the direct host is IPv6-only and will fail to connect from inside Docker.
3. Install dependencies:
   ```bash
   make install-deps
   ```
4. Run the server:
   ```bash
   fastapi dev
   ```
5. Call the API (see [runbook.md](runbook.md) for full `curl` examples).

## Running with Docker

```bash
docker build -t ai_engineering .
docker run --env-file .env -p 8000:8000 ai_engineering:latest
```

`.env` is gitignored and must never be committed; it's passed to the container at runtime via `--env-file`.
