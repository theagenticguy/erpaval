# Node.js API Stack

Server-side TypeScript API frameworks. This is a RESEARCH category — choice depends on requirements.

> **Node 24 LTS** is the current baseline (Node 22 is in maintenance; Node 25 is the Current non-LTS line). AWS Lambda supports `nodejs24.x`. Bump any `node = "22"` pins to `node = "24"`.

## Decision Framework

| Use Case                          | Recommendation         | Why                                         |
| --------------------------------- | ---------------------- | ------------------------------------------- |
| Lightweight API, edge-compatible  | **Hono**               | Fastest, runs on Cloudflare/Lambda/Bun/Node |
| Type-safe client-server, monorepo | **tRPC**               | End-to-end TypeScript types, no codegen     |
| Full-featured HTTP server         | **Fastify**            | Mature, plugin ecosystem, schema validation |
| Full-stack React app              | **Next.js API routes** | Colocated with frontend                     |

## Hono Quick Start

```typescript
import { Hono } from 'hono'
import { zValidator } from '@hono/zod-validator'
import { z } from 'zod'

const app = new Hono()

const itemSchema = z.object({
  name: z.string(),
  price: z.number(),
})

app.get('/items/:id', (c) => {
  const id = c.req.param('id')
  return c.json({ id, name: 'Widget', price: 9.99 })
})

app.post('/items', zValidator('json', itemSchema), (c) => {
  const item = c.req.valid('json')
  return c.json(item, 201)
})

export default app
```

## tRPC Quick Start

```typescript
import { initTRPC } from '@trpc/server'
import { z } from 'zod'

const t = initTRPC.create()

const appRouter = t.router({
  getItem: t.procedure
    .input(z.object({ id: z.number() }))
    .query(({ input }) => {
      return { id: input.id, name: 'Widget', price: 9.99 }
    }),
  createItem: t.procedure
    .input(z.object({ name: z.string(), price: z.number() }))
    .mutation(({ input }) => {
      return { ...input, id: 1 }
    }),
})

export type AppRouter = typeof appRouter
```

Client usage (fully typed):

```typescript
import { createTRPCClient } from '@trpc/client'
import type { AppRouter } from './server'

const client = createTRPCClient<AppRouter>({ /* config */ })
const item = await client.getItem.query({ id: 1 }) // typed
```

## Common Patterns

- **Validation**: zod v4 for all input validation (shared between Hono, tRPC, Fastify) — see `core.md` for v3 → v4 migration cheatsheet
- **Database**: Drizzle ORM (type-safe, SQL-like) or Prisma (code-first, migrations)
- **Auth**: Better Auth or Lucia for session-based, jose for JWT
- **Testing**: vitest v4 + supertest (or Hono's `app.request()`)
- **Runtime**: Node 24 LTS locally and in CI; `nodejs24.x` in Lambda
