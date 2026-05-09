# Frontend Domain

**Important**: If the project requirements indicate "API only", "backend only", "CLI tool", or any non-browser-facing application, respond with a brief note that frontend research is not applicable and skip all research.

## Categories

- **Meta-Frameworks** (RESEARCH): Next.js, Remix, Nuxt, SvelteKit, Astro, SolidStart, Analog, etc.
- **Component Libraries** (RESEARCH): shadcn/ui, Radix UI, Ark UI, Mantine, Headless UI, daisyUI, Park UI, etc.
- **State Management** (RESEARCH): Zustand, Jotai, TanStack Query, Nanostores, Pinia, Svelte stores, signals, etc.
- **CSS Approach** (RESEARCH): Tailwind CSS, vanilla-extract, Panda CSS, CSS Modules, UnoCSS, StyleX, etc.
- **Build Tools**: vite (default), Turbopack, Rspack, esbuild, etc.
- **Testing**: vitest (default), Playwright, Testing Library, Cypress, etc.
- **Schema Validation**: zod (default), valibot, arktype, etc.

## Framework Selection Context

When evaluating meta-frameworks, consider these project signals:

| Signal                    | Leans Toward                                |
| ------------------------- | ------------------------------------------- |
| SEO-critical content site | Astro, Next.js (SSG)                        |
| Highly interactive SPA    | Next.js (App Router), SvelteKit, SolidStart |
| E-commerce / marketing    | Next.js, Remix, Astro                       |
| Dashboard / admin panel   | Next.js, SvelteKit, Remix                   |
| Documentation site        | Astro, VitePress, Starlight                 |
| Mobile-first PWA          | Next.js, SvelteKit, Remix                   |

## Domain-Specific Artifacts

Provide a `package.json` snippet with all recommended frontend dependencies, grouped by purpose with comments.

## Additional Quality Checks

- [ ] Framework choice aligns with rendering model needs (SSR/SSG/SPA)
