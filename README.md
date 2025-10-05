# Global Liquidity Indices Platform

This repository contains the scaffolding for a full-stack system that publishes the Global Liquidity Indices (GLI). The stack
combines a FastAPI backend, Celery-based ETL pipeline, PostgreSQL/Timescale storage, Redis caching, and a Next.js 14 dashboard.

## Structure

```
backend/   # FastAPI app, Celery tasks, ETL utilities, tests
frontend/  # Next.js 14 dashboard with Tailwind UI components
docker-compose.yml  # Development orchestration for TimescaleDB, Redis, API, worker, web
```

## Getting Started

1. Copy `.env.example` to `.env` and adjust secrets and feature flags.
2. Build and start the stack with Docker Compose:

   ```bash
   docker compose up --build
   ```

3. Run backend tests locally:

   ```bash
   cd backend
   poetry install
   pytest
   ```

4. For frontend development:

   ```bash
   cd frontend
   npm install
   npm run dev
   ```

## Next Steps

The scaffolding ships with placeholder data-fetchers and dummy data inside the Celery task. To make the indices live you will
need to:

- Implement the individual ETL modules under `backend/backend/etl/` to download and persist data from FRED, ECB, BoJ, BoE, BIS, and others.
- Replace the placeholder composite calculation in `build_indices_task` with the full pipeline including database writes to the
  `series_observation` and `index_values` tables.
- Extend the API routers with authentication for mutating endpoints and enrich the responses with additional metadata such as
  component z-scores.
- Wire the frontend to the live API endpoints for controls, rebasing, and vintage comparisons.

This baseline provides a clean foundation with typing, testing, and containerisation so the macro team can focus on the domain
logic.
