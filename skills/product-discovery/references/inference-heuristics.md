# Inference Heuristics — Signal-to-Inference Mapping

Use these tables to derive product requirements from a user's short prompt. The goal is to infer ~80% of the PRD from a single sentence. Make every inference explicit so the user can override.

---

## Contents

- App Type Detection
- Feature Inference from Keywords
- Persona Inference
- Scale Inference
- Deployment Inference
- Auth Inference
- Data Persistence Inference
- Complexity Inference
- Using These Tables

## App Type Detection

| Signal in Prompt                            | Inferred App Type         | Confidence |
| ------------------------------------------- | ------------------------- | ---------- |
| "web page", "website", "web app", "site"    | Web application           | High       |
| "API", "service", "endpoint", "backend"     | API service               | High       |
| "mobile", "iOS", "Android", "phone"         | Mobile app / PWA          | High       |
| "CLI", "command line", "terminal", "script" | CLI tool                  | High       |
| "dashboard", "admin panel", "portal"        | Internal web app          | High       |
| "marketplace", "store", "e-commerce"        | E-commerce platform       | High       |
| "pipeline", "ETL", "data", "ingest"         | Data pipeline             | High       |
| "extension", "plugin", "add-on"             | Browser/IDE extension     | Medium     |
| "bot", "slack bot", "discord bot"           | Chat bot / Integration    | High       |
| "library", "SDK", "package"                 | Library / SDK             | High       |
| No explicit signal                          | Web application (default) | Low        |

## Feature Inference from Keywords

| Signal                                     | Inferred Features                                          | Inferred NFRs                                          |
| ------------------------------------------ | ---------------------------------------------------------- | ------------------------------------------------------ |
| "left/right pane", "split view", "sidebar" | Split-pane layout, resizable panels                        | Desktop-first responsive design                        |
| "every X seconds", "real-time", "live"     | Background polling/streaming, auto-refresh                 | Low-latency updates, WebSocket or SSE                  |
| "LLM", "AI", "GPT", "Claude", "agent"      | LLM API integration, prompt management, response streaming | Token cost tracking, rate limiting, API key management |
| "notes", "editor", "writing"               | Rich text editor, auto-save, content persistence           | Offline capability, conflict resolution                |
| "login", "sign up", "account"              | Auth system, user profiles, sessions                       | Security (OWASP), password hashing, session management |
| "share", "collaborate", "team"             | Multi-user, sharing, permissions                           | Real-time sync, conflict resolution, RBAC              |
| "search", "filter", "find"                 | Full-text search, filtering, sorting                       | Search indexing, query performance                     |
| "upload", "file", "image", "media"         | File upload, storage, media handling                       | File size limits, virus scanning, CDN delivery         |
| "notification", "alert", "email"           | Notification system, email integration                     | Delivery reliability, rate limiting                    |
| "payment", "subscribe", "billing"          | Payment processing, subscription management                | PCI compliance, financial accuracy                     |
| "chart", "graph", "analytics", "metrics"   | Data visualization, reporting                              | Query performance, caching                             |
| "drag and drop", "reorder", "kanban"       | Drag-and-drop UI, state persistence                        | Optimistic updates, undo/redo                          |
| "schedule", "cron", "recurring"            | Job scheduling, cron tasks                                 | Reliability, exactly-once execution                    |
| "export", "download", "PDF", "CSV"         | Export functionality, format conversion                    | Background processing for large exports                |
| "version", "history", "undo"               | Version history, audit trail                               | Storage growth management                              |

## Persona Inference

| Signal                           | Primary Persona                    | Secondary Persona |
| -------------------------------- | ---------------------------------- | ----------------- |
| "personal", "my own", "I want"   | Solo user / Individual             | —                 |
| "team", "company", "org"         | Team member                        | Team admin        |
| "students", "learning", "course" | Student / Learner                  | Instructor        |
| "customers", "users", "public"   | End user (consumer)                | Business admin    |
| "developers", "API", "SDK"       | Developer                          | DevOps engineer   |
| "writers", "content", "blog"     | Content creator                    | Editor / Reviewer |
| No persona signal                | Power user (tech-savvy individual) | Casual user       |

## Scale Inference

| Signal                                | Inferred Scale        | User Count    | Storage      |
| ------------------------------------- | --------------------- | ------------- | ------------ |
| "personal", "just me", "side project" | Low                   | 1-10          | < 1 GB       |
| "small team", "startup", "internal"   | Medium                | 10-1,000      | 1-100 GB     |
| "SaaS", "public", "marketplace"       | High                  | 1,000-100,000 | 100 GB-10 TB |
| "enterprise", "millions", "global"    | Very High             | 100,000+      | 10 TB+       |
| No scale signal                       | Medium (safe default) | 10-1,000      | 1-100 GB     |

## Deployment Inference

| Signal                   | Inferred Target          | Compute Model       |
| ------------------------ | ------------------------ | ------------------- |
| No mention of hosting    | AWS (default)            | Containers          |
| "serverless", "lambda"   | AWS                      | Serverless (Lambda) |
| "static", "JAMstack"     | Vercel / S3+CloudFront   | Static + API        |
| "self-hosted", "on-prem" | Self-hosted              | VMs or Containers   |
| "edge", "CDN"            | CloudFront / Vercel Edge | Edge functions      |
| "Kubernetes", "K8s"      | AWS EKS or self-hosted   | Containers (K8s)    |

## Auth Inference

| Signal                              | Inferred Auth Model                 |
| ----------------------------------- | ----------------------------------- |
| No users mentioned, "personal tool" | Anonymous / Local-only              |
| "login", "sign up", "accounts"      | Email + password, OAuth optional    |
| "team", "workspace"                 | OAuth / SSO (Google, GitHub)        |
| "enterprise", "SAML", "SSO"         | SAML + RBAC + MFA                   |
| "API key", "token"                  | API key auth                        |
| "public", "anyone can"              | Anonymous read, authenticated write |

## Data Persistence Inference

| Signal                              | Inferred Storage                           | Rationale                            |
| ----------------------------------- | ------------------------------------------ | ------------------------------------ |
| "notes", "documents", "content"     | PostgreSQL + full-text search              | Structured content with search needs |
| "real-time", "chat", "messages"     | PostgreSQL + Redis (pub/sub)               | Transactional + real-time layer      |
| "files", "images", "uploads"        | S3 + PostgreSQL (metadata)                 | Blob storage + relational metadata   |
| "analytics", "events", "logs"       | ClickHouse or DynamoDB                     | Write-heavy, append-only             |
| "cache", "session"                  | Redis                                      | Ephemeral, fast access               |
| "graph", "relationships", "network" | PostgreSQL (with ltree/adjacency) or Neo4j | Relationship-heavy data              |
| No data signal                      | PostgreSQL (safe default)                  | Most versatile starting point        |

## Complexity Inference

| Signal                          | MVP Complexity | Estimated Core Entities | Estimated Endpoints |
| ------------------------------- | -------------- | ----------------------- | ------------------- |
| Single-feature description      | Simple         | 2-4                     | 5-10                |
| 2-3 features mentioned          | Moderate       | 4-8                     | 10-20               |
| Multi-feature with integrations | Complex        | 8-15                    | 20-40               |
| Platform / marketplace          | Very Complex   | 15+                     | 40+                 |

---

## Using These Tables

1. **Parse the user's prompt** word by word against the signal columns
2. **Combine inferences** — a single prompt will match multiple tables
3. **Note confidence levels** — High confidence inferences become PRD facts; Low/Medium become explicit assumptions
4. **Flag conflicts** — if signals contradict (e.g., "personal" + "enterprise"), flag as a question for the user
5. **Default aggressively** — it's better to state an assumption the user can correct than to ask a question they find obvious
