# React/TypeScript Web Application Stack

Opinionated, production-grade React/TypeScript stack. Use these libraries by default when building frontend applications. Do not substitute alternatives unless the user explicitly requests them.

> **React 19.2+ is the baseline**, paired with **React Compiler v1.0** (stable — enable by default on new projects). Create React App is sunset; use Vite 8 to scaffold. Tailwind v4 uses CSS-first config, not `tailwind.config.js`.

## Stack Overview

| Layer        | Library                     | Version                          | Package                                                                                                   |
| ------------ | --------------------------- | -------------------------------- | --------------------------------------------------------------------------------------------------------- |
| Framework    | React                       | 19.2+ (compiler v1 stable)       | `react` `react-dom`                                                                                       |
| Routing      | TanStack Router             | 1.x                              | `@tanstack/react-router`                                                                                  |
| Server State | TanStack Query              | 5.x                              | `@tanstack/react-query`                                                                                   |
| Tables       | TanStack Table              | 8.x (v9 in alpha)                | `@tanstack/react-table`                                                                                   |
| Forms        | TanStack Form               | 1.x                              | `@tanstack/react-form`                                                                                    |
| Animation    | Motion                      | 12.x                             | `motion` (import from `motion/react`)                                                                     |
| Charts       | Recharts                    | 3.x                              | `recharts`                                                                                                |
| Custom Viz   | D3.js                       | 7.x (frozen — no 2024+ releases) | `d3` + `@types/d3`                                                                                        |
| 3D           | React Three Fiber + Drei    | 9.x / 10.x (drei v11 alpha)      | `@react-three/fiber` `@react-three/drei` `three`                                                          |
| Drag & Drop  | dnd-kit                     | v6.x classic or 2.x reorg        | `@dnd-kit/core` + sortable/utilities (classic); new projects can opt into `@dnd-kit/react` (0.x, pre-1.0) |
| Node Graphs  | XY Flow (React Flow)        | 12.x                             | `@xyflow/react`                                                                                           |
| UI Blocks    | blocks.so + shadcn/ui       | shadcn CLI v4.x                  | `shadcn` CLI registry — note shadcn is migrating from Radix Primitives toward `base-ui`                   |
| CSS          | Tailwind CSS                | 4.x (CSS-first config)           | `tailwindcss` + `@tailwindcss/vite`                                                                       |
| Backend      | AWS Amplify Gen 2           | 1.x                              | `@aws-amplify/backend`                                                                                    |
| Database     | Aurora (PostgreSQL or DSQL) | DSQL GA across 15 regions        | Aurora DSQL as serverless-Postgres default; Aurora Serverless v2 for heavier relational workloads         |

## Installation (Full Stack)

```bash
# Core TanStack
npm install @tanstack/react-router @tanstack/react-query @tanstack/react-table @tanstack/react-form

# DevTools (dev only)
npm install -D @tanstack/react-router-devtools @tanstack/react-query-devtools

# Animation
npm install motion

# Visualization
npm install recharts d3 @types/d3

# 3D (requires React 19)
npm install three @react-three/fiber @react-three/drei @types/three

# Drag & Drop
npm install @dnd-kit/core @dnd-kit/sortable @dnd-kit/utilities

# Node-Based Graphs
npm install @xyflow/react

# UI Blocks (via shadcn registry)
npx shadcn@latest add https://blocks.so/r/login-01.json
```

## Library Reference Files

For detailed patterns and code examples, read the specific library reference:

- `tanstack-router.md` — File-based routing, type-safe search params, preloading
- `tanstack-query.md` — queryOptions pattern, prefetching, invalidation
- `tanstack-table.md` — Headless tables, sorting, filtering, pagination
- `tanstack-form.md` — Field validation, Zod adapters, form subscription
- `motion.md` — Variants, AnimatePresence, layout animations, scroll-linked
- `visualization.md` — Recharts (standard charts) vs D3 (custom viz) decision + patterns
- `react-three-fiber.md` — Canvas, useFrame, model loading, product viewers
- `dnd-kit.md` — Sortable lists, sensors, collision detection
- `xy-flow.md` — Node-based UIs, workflow editors, event hooks, styling, auto-layout
- `ui-blocks.md` — blocks.so registry, shadcn/ui, category catalog
- `amplify-aurora.md` — Amplify Gen 2 SQL connector, custom queries, DynamoDB coexistence
