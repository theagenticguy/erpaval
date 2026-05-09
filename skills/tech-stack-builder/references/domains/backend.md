# Backend Domain

## Categories

- **Web Frameworks** (RESEARCH): FastAPI, Litestar, Django, Flask, Express, Fastify, Hono, Gin, Axum, etc.
- **ORMs / Data Access** (RESEARCH): SQLAlchemy, SQLModel, Tortoise ORM, Prisma, Drizzle, TypeORM, GORM, Diesel, etc.
- **Task Queues**: dramatiq (default), Celery, BullMQ, Temporal, etc.
- **Caching**: Redis, Memcached, DragonflyDB, KeyDB, Valkey, etc.
- **Auth Libraries** (RESEARCH): Depends on auth model — PassLib, python-jose, authlib, next-auth, lucia, etc.
- **API Approaches** (RESEARCH): REST, GraphQL, gRPC, tRPC — evaluate based on project needs
- **HTTP Clients**: httpx (default), aiohttp, requests, got, ky, etc.
- **Data Validation**: pydantic (default), zod, joi, etc.

## Domain-Specific Artifacts

Provide a `pyproject.toml` or `package.json` snippet (based on language) with all recommended backend dependencies, grouped by purpose with comments.

## Additional Quality Checks

- [ ] Recommendations are coherent (technologies work well together within the backend layer)
