# [FILL: Product Name] — Product Requirements Document

> **Version**: 1.0 (Draft)
> **Date**: [FILL: Date]
> **Author**: AI-Generated via `/draft-prd`
> **Status**: Draft — Pending Review

---

## 1. Executive Summary

[FILL: 3-5 sentences. What is this product? Who is it for? Why does it need to exist? What makes it unique?]

---

## 2. Product Vision

[FILL: 2-3 sentences. Target user + value proposition + differentiator. No implementation details.]

---

## 3. Goals and Non-Goals

### Goals

| #  | Goal   | Success Metric |
| -- | ------ | -------------- |
| G1 | [FILL] | [FILL]         |
| G2 | [FILL] | [FILL]         |
| G3 | [FILL] | [FILL]         |

### Non-Goals

| #   | Non-Goal | Rationale |
| --- | -------- | --------- |
| NG1 | [FILL]   | [FILL]    |
| NG2 | [FILL]   | [FILL]    |
| NG3 | [FILL]   | [FILL]    |

---

## 4. User Personas

### [FILL: Persona 1 Name] — [FILL: Archetype]

| Attribute         | Detail                                    |
| ----------------- | ----------------------------------------- |
| **Role**          | [FILL]                                    |
| **Tech Comfort**  | [FILL: Low / Medium / High]               |
| **Goals**         | [FILL: 2-3 bullet points]                 |
| **Pain Points**   | [FILL: 2-3 bullet points]                 |
| **Usage Pattern** | [FILL: How and when they use the product] |

### [FILL: Persona 2 Name] — [FILL: Archetype]

| Attribute         | Detail                                    |
| ----------------- | ----------------------------------------- |
| **Role**          | [FILL]                                    |
| **Tech Comfort**  | [FILL: Low / Medium / High]               |
| **Goals**         | [FILL: 2-3 bullet points]                 |
| **Pain Points**   | [FILL: 2-3 bullet points]                 |
| **Usage Pattern** | [FILL: How and when they use the product] |

[FILL: Add more personas as needed]

---

## 5. Functional Requirements

### 5.1 User Stories

#### P0 — Must Have (MVP)

| ID     | Story                                                               | Acceptance Criteria       |
| ------ | ------------------------------------------------------------------- | ------------------------- |
| US-001 | As a [FILL: persona], I want [FILL: action] so that [FILL: outcome] | [FILL: testable criteria] |
| US-002 | [FILL]                                                              | [FILL]                    |
| US-003 | [FILL]                                                              | [FILL]                    |
| US-004 | [FILL]                                                              | [FILL]                    |
| US-005 | [FILL]                                                              | [FILL]                    |
| US-006 | [FILL]                                                              | [FILL]                    |
| US-007 | [FILL]                                                              | [FILL]                    |
| US-008 | [FILL]                                                              | [FILL]                    |
| US-009 | [FILL]                                                              | [FILL]                    |
| US-010 | [FILL]                                                              | [FILL]                    |

#### P1 — Should Have (v1.0)

| ID     | Story  | Acceptance Criteria |
| ------ | ------ | ------------------- |
| US-101 | [FILL] | [FILL]              |
| US-102 | [FILL] | [FILL]              |
| US-103 | [FILL] | [FILL]              |

#### P2 — Nice to Have (Future)

| ID     | Story  | Acceptance Criteria |
| ------ | ------ | ------------------- |
| US-201 | [FILL] | [FILL]              |
| US-202 | [FILL] | [FILL]              |

### 5.2 Feature List

| Feature | Stories        | Description | Acceptance Criteria |
| ------- | -------------- | ----------- | ------------------- |
| [FILL]  | US-001, US-002 | [FILL]      | [FILL]              |
| [FILL]  | US-003, US-004 | [FILL]      | [FILL]              |
| [FILL]  | [FILL]         | [FILL]      | [FILL]              |

---

## 6. Information Architecture

```json
[FILL: Route/page tree]

/                          → Landing / Main view
├── /app                   → Authenticated app shell
│   ├── /app/[feature-1]   → [FILL: Description]
│   ├── /app/[feature-2]   → [FILL: Description]
│   └── /app/settings      → User settings
├── /auth
│   ├── /auth/login        → Login page
│   └── /auth/register     → Registration page
└── /api
    └── /api/v1/...        → API endpoints
```

[FILL: Description of navigation hierarchy and key user flows]

---

## 7. Non-Functional Requirements

### 7.1 Performance

| Metric                  | Target                |
| ----------------------- | --------------------- |
| Page load (initial)     | [FILL: e.g., < 2s]    |
| API response (p95)      | [FILL: e.g., < 200ms] |
| Time to interactive     | [FILL: e.g., < 3s]    |
| [FILL: Domain-specific] | [FILL]                |

### 7.2 Security

- **Authentication**: [FILL: Auth model — anonymous, email+password, OAuth, SAML]
- **Authorization**: [FILL: RBAC, ABAC, or simple owner-based]
- **Data Protection**: [FILL: Encryption at rest, in transit, PII handling]
- **OWASP**: [FILL: Key considerations — XSS, CSRF, injection, etc.]
- **API Security**: [FILL: Rate limiting, input validation, CORS policy]

### 7.3 Scalability

- **Expected Growth**: [FILL: User growth trajectory]
- **Bottleneck Awareness**: [FILL: Known scaling challenges]
- **Scaling Strategy**: [FILL: Horizontal, vertical, caching, CDN]

### 7.4 Accessibility

- **WCAG Target**: [FILL: 2.1 AA or 2.1 AAA]
- **Keyboard Navigation**: [FILL: Full keyboard support requirements]
- **Screen Reader**: [FILL: ARIA labels, semantic HTML]
- **Color Contrast**: [FILL: Minimum ratio targets]

### 7.5 Reliability

- **Uptime Target**: [FILL: e.g., 99.9%]
- **Error Budget**: [FILL: Acceptable error rate]
- **Graceful Degradation**: [FILL: Behavior when dependencies fail]
- **Data Durability**: [FILL: Backup and recovery strategy]

### 7.6 Observability

- **Logging**: [FILL: Structured logging, log levels, retention]
- **Metrics**: [FILL: Key business and technical metrics]
- **Alerting**: [FILL: Alert thresholds and escalation]
- **Tracing**: [FILL: Distributed tracing requirements]

---

## 8. Data Models

### 8.1 Entity Definitions

#### [FILL: Entity Name]

| Field        | Type      | Constraints             | Description       |
| ------------ | --------- | ----------------------- | ----------------- |
| `id`         | UUID      | PK                      | Unique identifier |
| `created_at` | timestamp | NOT NULL, DEFAULT now() | Creation time     |
| `updated_at` | timestamp | NOT NULL, DEFAULT now() | Last modification |
| [FILL]       | [FILL]    | [FILL]                  | [FILL]            |

#### [FILL: Entity Name]

| Field        | Type      | Constraints             | Description       |
| ------------ | --------- | ----------------------- | ----------------- |
| `id`         | UUID      | PK                      | Unique identifier |
| `created_at` | timestamp | NOT NULL, DEFAULT now() | Creation time     |
| `updated_at` | timestamp | NOT NULL, DEFAULT now() | Last modification |
| [FILL]       | [FILL]    | [FILL]                  | [FILL]            |

[FILL: Add more entities as needed]

### 8.2 Relationships

| Relationship                        | Type                  | Description |
| ----------------------------------- | --------------------- | ----------- |
| [FILL: Entity A] → [FILL: Entity B] | [FILL: 1:N, N:M, 1:1] | [FILL]      |

### 8.3 Indexes

| Table  | Index  | Columns | Rationale |
| ------ | ------ | ------- | --------- |
| [FILL] | [FILL] | [FILL]  | [FILL]    |

---

## 9. API Contracts

### 9.1 API Design Principles

- **Style**: [FILL: REST, GraphQL, gRPC, or hybrid]
- **Versioning**: [FILL: URL path (/api/v1), header, or query param]
- **Auth**: [FILL: Bearer token, API key, session cookie]
- **Pagination**: [FILL: Cursor-based, offset-based]
- **Error Format**: [FILL: Standard error response shape]

### 9.2 Endpoints

#### [FILL: Feature Area]

| Method | Path   | Auth   | Description | Request | Response |
| ------ | ------ | ------ | ----------- | ------- | -------- |
| [FILL] | [FILL] | [FILL] | [FILL]      | [FILL]  | [FILL]   |

[FILL: Add endpoint groups for each feature area]

---

## 10. Edge Cases and Error States

| #     | Trigger | Expected Behavior | Fallback Strategy |
| ----- | ------- | ----------------- | ----------------- |
| EC-01 | [FILL]  | [FILL]            | [FILL]            |
| EC-02 | [FILL]  | [FILL]            | [FILL]            |
| EC-03 | [FILL]  | [FILL]            | [FILL]            |
| EC-04 | [FILL]  | [FILL]            | [FILL]            |
| EC-05 | [FILL]  | [FILL]            | [FILL]            |

---

## 11. Competitive Landscape

| Product | Type     | Strengths | Weaknesses | Our Advantage |
| ------- | -------- | --------- | ---------- | ------------- |
| [FILL]  | Direct   | [FILL]    | [FILL]     | [FILL]        |
| [FILL]  | Direct   | [FILL]    | [FILL]     | [FILL]        |
| [FILL]  | Indirect | [FILL]    | [FILL]     | [FILL]        |

[FILL: Brief differentiation summary — 2-3 sentences on overall positioning]

---

## 12. Milestones

### MVP (Milestone 1)

**Definition of Done**: [FILL: What makes MVP launchable]

| Feature | Stories | Status  |
| ------- | ------- | ------- |
| [FILL]  | [FILL]  | Planned |
| [FILL]  | [FILL]  | Planned |

### v1.0 (Milestone 2)

**Definition of Done**: [FILL: What makes v1.0 complete]

| Feature                            | Stories | Status  |
| ---------------------------------- | ------- | ------- |
| [FILL: Remaining P0 + selected P1] | [FILL]  | Planned |

---

## 13. Open Questions

| #    | Question | Owner  | Resolution Path |
| ---- | -------- | ------ | --------------- |
| OQ-1 | [FILL]   | [FILL] | [FILL]          |
| OQ-2 | [FILL]   | [FILL] | [FILL]          |
| OQ-3 | [FILL]   | [FILL] | [FILL]          |

---

## 14. Assumptions Log

| #   | Assumption | Confidence              | Source                          | Override?      |
| --- | ---------- | ----------------------- | ------------------------------- | -------------- |
| A-1 | [FILL]     | [FILL: High/Medium/Low] | [FILL: Inferred/User-confirmed] | [FILL: Yes/No] |
| A-2 | [FILL]     | [FILL]                  | [FILL]                          | [FILL]         |
| A-3 | [FILL]     | [FILL]                  | [FILL]                          | [FILL]         |

---

## 15. Tech Stack Requirements Extract

> This section maps PRD decisions to the `/build-stack` intake format.
> Copy this directly into `/build-stack` to generate a technology recommendation.

| Requirement           | Value                                          | Derived From             |
| --------------------- | ---------------------------------------------- | ------------------------ |
| **App Type**          | [FILL]                                         | Section 1, 5             |
| **Stack Layers**      | [FILL: Backend, Frontend, Infrastructure, AWS] | Section 6, 7             |
| **Primary Language**  | [FILL]                                         | Section 7, 9             |
| **Deployment Target** | [FILL]                                         | Section 7.3, Assumptions |
| **Compute Model**     | [FILL]                                         | Section 7.3, Assumptions |
| **Expected Scale**    | [FILL]                                         | Section 7.3              |
| **Team Size**         | [FILL]                                         | Assumptions              |
| **Must-Haves**        | [FILL: Derived from P0 features and NFRs]      | Section 5, 7             |
| **Already Decided**   | [FILL: Any tech locked in by PRD decisions]    | Section 7, 8, 9          |
| **Avoid List**        | [FILL: Any tech explicitly excluded]           | Non-goals, Assumptions   |
