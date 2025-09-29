# BrainTrail — AI Knowledge Hub (MVP)

## Stack
- FastAPI + SQLAlchemy + pgvector
- Next.js 14 + Tailwind
- Postgres 16, Redis 7, (optional) Ollama, Nginx, Docker Compose

## Quick start
1) `cp .env.example .env`
2) `docker compose up --build` (or `make up`)
3) In another terminal: `make seed`
4) Go to `http://localhost` → Setup → create a goal → Roadmap → Learn
5) Ask a question; use **Search** for contexts and **Answer** for streamed LLM reply.

## Notes
- Embeddings default to local SentenceTransformers (offline-friendly dev).
- Tutor answers stream via SSE; cached for 1h in Redis.
- Swap provider via `LLM_PROVIDER={openai|ollama}`.
- For production, set `RUN_CREATE_ALL=false` and use Alembic migrations.

## Development Commands

```bash
# Start all services
make up

# Stop all services
make down

# View logs
make logs

# Database operations
make seed        # Seed sample data
make migrate     # Apply migrations

# Access services
make psql        # Database shell
```

## Project Structure

```
ai-knowledge-hub/
├── README.md
├── .env.example
├── docker-compose.yml
├── Makefile
├── infra/
│   ├── initdb/01_init.sql
│   └── nginx/default.conf
├── api/
│   ├── Dockerfile
│   ├── pyproject.toml
│   ├── alembic/  (created after init)
│   ├── alembic.ini
│   ├── README.md
│   └── app/
│       ├── main.py
│       ├── core/{config.py,security.py}
│       ├── db.py
│       ├── models.py
│       ├── schemas.py
│       ├── deps.py
│       ├── crud/
│       │   ├── users.py
│       │   ├── goals.py (placeholder for future)
│       │   ├── resources.py (placeholder for future)
│       │   └── progress.py (placeholder for future)
│       ├── routers/
│       │   ├── auth.py
│       │   ├── goals.py
│       │   ├── resources.py
│       │   ├── progress.py
│       │   ├── quiz.py (placeholder)
│       │   └── tutor.py
│       ├── services/
│       │   ├── embeddings.py
│       │   ├── rag.py
│       │   ├── llm.py
│       │   ├── cache.py
│       │   └── ranking.py
│       └── seed.py
├── web/
│   ├── Dockerfile
│   ├── package.json
│   ├── next.config.mjs
│   ├── postcss.config.mjs
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   └── src/
│       ├── app/
│       │   ├── globals.css
│       │   ├── layout.tsx
│       │   ├── page.tsx
│       │   ├── setup/page.tsx
│       │   ├── roadmap/[id]/page.tsx
│       │   ├── learn/[moduleId]/page.tsx
│       │   └── dashboard/page.tsx (placeholder)
│       ├── components/{Navbar.tsx,ProgressBar.tsx,Badge.tsx,ResourceCard.tsx,ChatPanel.tsx}
│       └── lib/api.ts
└── .github/workflows/ci.yml
```

## Next Steps (after MVP runs)

* Auto-ingest pipelines (RSS + simple scrapers) → Celery worker (optional).
* Adaptive quizzes: generate items server-side from module objectives and contexts; store in `quizzes`.
* Gamification tables (streaks, badges) and a dashboard summary.
* Add Redis caches to `/goals/{id}` and resource lists.
* Add auth cookies (HttpOnly) and refresh tokens for production.
* Cloud deploy (Azure Web App / AWS ECS) + container registry + environment secrets.
