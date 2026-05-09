# TypeScript Project Scaffold

Complete project configuration with full quality gates and security pipeline.

## package.json

```json
{
  "name": "myapp",
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage",
    "lint": "biome check .",
    "lint:fix": "biome check . --write",
    "typecheck": "tsc --noEmit",
    "prepare": "lefthook install"
  },
  "devDependencies": {
    "@biomejs/biome": "^2.4.6",
    "@commitlint/cli": "^20.3.1",
    "@commitlint/config-conventional": "^20.4.3",
    "@vitest/coverage-v8": "^3.0.0",
    "knip": "^5.85.0",
    "lefthook": "^2.1.2",
    "typescript": "^5.7.0",
    "vitest": "^3.0.0"
  }
}
```

## biome.json

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
  },
  "javascript": {
    "formatter": {
      "quoteStyle": "single",
      "trailingCommas": "all",
      "semicolons": "asNeeded"
    }
  },
  "files": {
    "ignore": ["node_modules", "dist", "coverage", "*.min.js"]
  }
}
```

The `types` domain enables type-aware rules like `noFloatingPromises`, `noMisusedPromises`, `useAwaitThenable`. The `security` domain covers JS-specific attack vectors (eval, XSS, secrets). For deeper SAST, use semgrep with `p/typescript`.

## tsconfig.json

```json
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
    "verbatimModuleSyntax": true,
    "outDir": "dist"
  },
  "include": ["src"]
}
```

## vitest.config.ts

```typescript
import { defineConfig } from 'vitest/config'

export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'lcov', 'json'],
      include: ['src/**/*.ts'],
      exclude: ['src/**/*.test.ts', 'src/**/*.spec.ts'],
      thresholds: {
        branches: 80,
        functions: 80,
        lines: 80,
        statements: 80,
      },
    },
  },
})
```

## knip.json

```json
{
  "$schema": "https://unpkg.com/knip@5/schema.json",
  "entry": ["src/index.ts"],
  "project": ["src/**/*.ts"],
  "ignore": ["**/*.test.ts", "**/*.spec.ts"],
  "ignoreDependencies": ["@types/node"],
  "rules": {
    "dependencies": "error",
    "devDependencies": "warn",
    "unlisted": "error",
    "exports": "warn",
    "files": "warn"
  }
}
```

## commitlint.config.js

```javascript
export default {
  extends: ['@commitlint/config-conventional'],
  rules: {
    'type-enum': [2, 'always', [
      'feat', 'fix', 'docs', 'style', 'refactor',
      'perf', 'test', 'build', 'ci', 'chore', 'revert',
    ]],
    'subject-case': [2, 'never', ['start-case', 'pascal-case', 'upper-case']],
    'header-max-length': [2, 'always', 100],
  },
}
```

## mise.toml

```toml
[tools]
node = "24"
betterleaks = "latest"
osv-scanner = "latest"
semgrep = "latest"

[tasks]
install = "pnpm install"
dev = "pnpm dev"
build = "pnpm build"
test = "pnpm vitest run"
lint = "pnpm biome check ."
typecheck = "pnpm tsc --noEmit"

[tasks.security]
description = "Run all security scans"
depends = ["security:secrets", "security:sast", "security:deps"]

[tasks."security:secrets"]
description = "Scan for secrets"
run = "betterleaks git --no-banner"

[tasks."security:sast"]
description = "SAST scan with semgrep"
run = "semgrep scan --config p/typescript --config p/owasp-top-ten --error src/"

[tasks."security:deps"]
description = "Audit dependencies"
run = "osv-scanner scan --lockfile pnpm-lock.yaml"

[tasks.check]
description = "Run all checks"
depends = ["lint", "typecheck", "test"]
```

## lefthook.yml

```yaml
pre-commit:
  parallel: true
  jobs:
    - name: biome-check
      glob: "*.{ts,tsx,js,jsx,json,jsonc,css}"
      run: npx @biomejs/biome check --no-errors-on-unmatched --write {staged_files}
      stage_fixed: true

    - name: knip
      run: npx knip --no-progress

commit-msg:
  jobs:
    - name: commitlint
      run: npx commitlint --edit {1}

pre-push:
  parallel: true
  jobs:
    - name: typecheck
      run: npx tsc --noEmit

    - name: test
      run: npx vitest run --no-file-parallelism

    - name: biome-ci
      run: npx @biomejs/biome ci .

    - name: betterleaks
      run: betterleaks git --no-banner

    - name: semgrep
      run: semgrep scan --config p/typescript --config p/owasp-top-ten --error src/
```

## .github/workflows/ci.yml

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:

jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 24
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - run: pnpm biome ci .
      - run: pnpm tsc --noEmit
      - run: pnpm knip

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 24
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - run: pnpm vitest run --coverage

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 24
          cache: pnpm
      - run: pnpm install --frozen-lockfile
      - name: Semgrep
        run: |
          pip install semgrep
          semgrep scan --config p/typescript --config p/owasp-top-ten --error src/
      - name: OSV-Scanner
        uses: google/osv-scanner-action/osv-scanner-action@v2
        with:
          scan-args: --lockfile pnpm-lock.yaml
      - name: Betterleaks
        run: |
          docker run --rm -v "$PWD:/src" ghcr.io/betterleaks/betterleaks:latest \
            git --no-banner --report-format sarif --report-path /src/betterleaks.sarif /src
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      - name: License check
        run: npx license-checker-rseidelsohn --failOn "GPL-3.0;AGPL-3.0" --production
```

## Dockerfile

```dockerfile
# syntax=docker/dockerfile:1

FROM node:24-slim AS base
ENV PNPM_HOME="/pnpm"
ENV PATH="$PNPM_HOME:$PATH"
RUN corepack enable
WORKDIR /app

FROM base AS deps
COPY package.json pnpm-lock.yaml ./
RUN --mount=type=cache,id=pnpm,target=/pnpm/store \
    pnpm install --frozen-lockfile --prod

FROM base AS build
COPY package.json pnpm-lock.yaml ./
RUN --mount=type=cache,id=pnpm,target=/pnpm/store \
    pnpm install --frozen-lockfile
COPY . .
RUN pnpm run build

FROM node:24-slim
RUN addgroup --system --gid 1001 app && \
    adduser --system --uid 1001 --ingroup app app
WORKDIR /app
COPY --from=deps --chown=app:app /app/node_modules ./node_modules
COPY --from=build --chown=app:app /app/dist ./dist
COPY --from=build --chown=app:app /app/package.json ./
USER app
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

## .gitignore

```text
node_modules/
dist/
coverage/
*.sarif
.env
.env.*
```

## .editorconfig

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 2

[*.md]
trim_trailing_whitespace = false
```

## Setup Commands

```bash
# Initialize
pnpm init && pnpm add -D @biomejs/biome typescript vitest lefthook knip @commitlint/cli @commitlint/config-conventional
mise install && lefthook install

# Verify
mise run check
mise run security
```
