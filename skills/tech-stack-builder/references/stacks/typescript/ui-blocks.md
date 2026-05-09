# UI Blocks: blocks.so + shadcn/ui

blocks.so is a free, open-source (MIT) library of 60+ pre-built UI blocks on React + Tailwind CSS + shadcn/ui.

**Categories**: Stats (15), Dialogs (12), Login/Signup (9), File Upload (6), Sidebar (6), AI Components (5), Form Layout (5), Tables (5), Command Menu (3), Grid List (3), Onboarding (1).

## Install via shadcn Registry

```json
// components.json
{
  "registries": {
    "@blocks": "https://blocks.so/r/{name}.json"
  }
}
```

```bash
npx shadcn@latest add @blocks/login-01
npx shadcn@latest add @blocks/sidebar-01
npx shadcn@latest add @blocks/stats-01
npx shadcn@latest add @blocks/dialog-01
```

Or install directly by URL:

```bash
npx shadcn@latest add https://blocks.so/r/login-01.json
```

**When to use**: Clean app-level UI blocks — login forms, dialogs, sidebars, stats dashboards, data tables. Not for marketing/landing pages (use shadcnblocks.com for that) or motion-heavy components (use Magic UI or Aceternity UI).
