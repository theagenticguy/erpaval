# TypeScript Core Stack

Settled defaults for all TypeScript/JavaScript projects.

Versions to target:

| Tool       | Version | Note                                                                        |
| ---------- | ------- | --------------------------------------------------------------------------- |
| TypeScript | 6.x     | Current major                                                               |
| Node       | 24 LTS  | Current LTS (prior: 22 maintenance). AWS Lambda supports `nodejs24.x`.      |
| pnpm       | 10.x    | v11 is in late RC; 10 is the stable pick                                    |
| Biome      | 2.4.x   | `eslint` + `prettier` replacement                                           |
| Vite       | 8.x     | **Vite 8 uses Rolldown as its single default bundler** — not esbuild+Rollup |
| Vitest     | 4.x     | v4 is current stable (post v3 → v4 bump); v5 still beta                     |
| Zod        | 4.x     | **Zod 4 introduced breaking changes** — see Schema Validation section below |

## Package Management: pnpm

Faster, disk-efficient, strict by default. Replaces npm and yarn.

```bash
# Install
corepack enable
corepack prepare pnpm@latest --activate

# Common commands
pnpm install          # Install from lockfile
pnpm add <pkg>        # Add dependency
pnpm add -D <pkg>     # Add dev dependency
pnpm remove <pkg>     # Remove dependency
pnpm dlx <tool>       # One-off tool execution (like npx)
```

Always commit `pnpm-lock.yaml`.

## Linting & Formatting: biome

Replaces eslint + prettier in a single, fast tool. v2 introduces a domain system for framework-specific rules.

```json
{
  "$schema": "https://biomejs.dev/schema.json",
  "linter": {
    "enabled": true,
    "rules": {
      "recommended": true,
      "security": {
        "noGlobalEval": "error",
        "noDangerouslySetInnerHtml": "error",
        "noDangerouslySetInnerHtmlWithChildren": "error",
        "noBlankTarget": "error",
        "noSecrets": "error"
      },
      "suspicious": {
        "noExplicitAny": "error",
        "noGlobalAssign": "error"
      }
    },
    "domains": {
      "react": "recommended",
      "types": "all"
    }
  },
  "formatter": {
    "enabled": true,
    "indentStyle": "space",
    "indentWidth": 2,
    "lineWidth": 100
  }
}
```

The `security` domain covers 5 JS-specific rules (eval, XSS, secrets). The `types` domain enables type-aware rules like `noFloatingPromises`, `noMisusedPromises`, `useAwaitThenable`. Available domains: `next`, `playwright`, `react`, `solid`, `test`, `types`, `vue`.

Biome's security coverage is narrow (5 rules) compared to ruff's bandit rules (60+). Use **semgrep** with `p/typescript` for deeper SAST coverage.

```bash
pnpm biome check .          # Lint + format check
pnpm biome check . --write  # Auto-fix
pnpm biome ci .             # CI mode (no writes, strict)
```

## TypeScript Config: Strict Mode

```json
// tsconfig.json
{
  "compilerOptions": {
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "exactOptionalPropertyTypes": true,
    "noImplicitOverride": true,
    "moduleResolution": "bundler",
    "module": "ESNext",
    "target": "ES2022",
    "lib": ["ES2022", "DOM", "DOM.Iterable"],
    "skipLibCheck": true,
    "isolatedModules": true,
    "verbatimModuleSyntax": true
  }
}
```

## Schema Validation: zod v4

TypeScript-first schema validation. **Zod 4 (shipped 2025) introduced breaking changes** — the codemod at `pnpm dlx zod-migration` covers most of them.

```typescript
import { z } from 'zod'

const UserSchema = z.object({
  name: z.string().min(1),
  email: z.email(),                      // v4: standalone, not `.email()` method
  age: z.number().int().positive().optional(),
})

type User = z.infer<typeof UserSchema>

const result = UserSchema.safeParse(input)
if (result.success) {
  // result.data is typed as User
}
```

### Zod 3 → 4 migration cheatsheet

| v3                                                | v4                                                           |
| ------------------------------------------------- | ------------------------------------------------------------ |
| `z.string().email()` / `.uuid()` / `.url()`       | `z.email()` / `z.uuid()` / `z.url()` (standalone)            |
| `{ message, invalid_type_error, required_error }` | Unified `error` param: `error: (ctx) => "..."`               |
| `z.function().args(...).returns(...)`             | `z.function({ input: [...], output: ... })` factory          |
| `.merge()` / `.format()` / `.flatten()`           | Deprecated — use `z.extend()` / flatten via `z.treeifyError` |
| `z.number().int()`                                | Now safe-int only; infinites rejected by `z.number()`        |

## Testing: vitest

Native Vite integration, jest-compatible API.

```typescript
// vitest.config.ts
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    globals: true,
    environment: 'jsdom', // or 'node' for non-browser
  },
})
```

## Dead Code Detection: knip

```bash
pnpm add -D knip
pnpm knip           # Find unused files, deps, exports
pnpm knip --fix     # Auto-remove unused exports
```

## Bundler: vite v8

Universal standard for frontend builds and dev server. **Vite 8 ships Rolldown as the single default bundler** — replacing the esbuild+Rollup split that defined v1–v7. Oxc is the compiler. Plugin API still overlaps with Rollup but isn't identical; old plugins may need updates.

```bash
pnpm create vite my-app --template react-ts
```

Performance snapshot: Linear reported 46s → 6s production builds after the Vite 8 upgrade. For migration detail, see <https://vite.dev/blog/announcing-vite8>.
