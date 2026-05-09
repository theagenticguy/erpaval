# TanStack Router

Use TanStack Router for all routing. This is the Router library only — NOT TanStack Start.

## Setup

```tsx
import {
  createRouter, createRootRoute, createRoute,
  RouterProvider, Link, Outlet,
} from '@tanstack/react-router'

const rootRoute = createRootRoute({
  component: () => (
    <>
      <nav>
        <Link to="/" className="[&.active]:font-bold">Home</Link>
        <Link to="/about" className="[&.active]:font-bold">About</Link>
      </nav>
      <Outlet />
    </>
  ),
})

const indexRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: '/',
  component: () => <h1>Home</h1>,
})

const routeTree = rootRoute.addChildren([indexRoute])
const router = createRouter({ routeTree, defaultPreload: 'intent' })

// CRITICAL: Register for full TypeScript inference
declare module '@tanstack/react-router' {
  interface Register { router: typeof router }
}
```

## Type-Safe Search Params with Zod

```tsx
import { createFileRoute } from '@tanstack/react-router'
import { zodValidator, fallback } from '@tanstack/zod-adapter'
import { z } from 'zod'

const searchSchema = z.object({
  page: fallback(z.number(), 1).default(1),
  category: fallback(z.string(), 'all').default('all'),
})

export const Route = createFileRoute('/products')({
  validateSearch: zodValidator(searchSchema),
  component: () => {
    const { page, category } = Route.useSearch() // fully typed
    return <div>Page {page}, Category: {category}</div>
  },
})
```

## Key Rules

- Always register the router type with `declare module` for global TypeScript inference
- Use file-based routing with `@tanstack/router-plugin` (Vite) for automatic code-splitting
- Search params are JSON-first (supports arrays, objects, dates), validated via `validateSearch`
- Always pass `from` to `useSearch()` / `useNavigate()` for performance with large route trees
- Use `defaultPreload: 'intent'` to preload routes on hover/focus
