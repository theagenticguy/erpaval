# PRD Quality Criteria

Minimum quality bar for each section of the PRD. Use this as a checklist during synthesis (Phase 3) to ensure completeness before writing the final document.

---

## Section Quality Requirements

### 1. Executive Summary

- [ ] 3-5 sentences maximum
- [ ] States what the product is, who it's for, and why it matters
- [ ] Mentions the core differentiator or unique value
- [ ] Readable by a non-technical stakeholder

### 2. Product Vision

- [ ] 2-3 sentences with: target user + value proposition + differentiator
- [ ] Answers "why does this need to exist?"
- [ ] Does NOT describe implementation details

### 3. Goals and Non-Goals

- [ ] At least 3 goals, each measurable or verifiable
- [ ] At least 3 non-goals, each preventing scope creep on a plausible extension
- [ ] Goals are outcomes ("users can X"), not outputs ("build Y feature")
- [ ] Non-goals are explicit exclusions, not just "we won't do bad things"

### 4. User Personas

- [ ] At least 2 personas
- [ ] Each has: name, role/archetype, goals (2-3), pain points (2-3), tech comfort level
- [ ] Personas are distinct — they use the product differently
- [ ] At least one persona represents the primary target user

### 5. Functional Requirements (User Stories)

- [ ] At least 10 P0 (must-have) stories
- [ ] Each story follows "As a [persona], I want [action] so that [outcome]"
- [ ] Stories grouped by feature area
- [ ] Priority levels: P0 (MVP), P1 (v1.0), P2 (future)
- [ ] Every P0 story maps to at least one feature with acceptance criteria
- [ ] Acceptance criteria are testable (not vague like "works well")

### 6. Information Architecture

- [ ] Route/page tree showing all screens/views
- [ ] Each route has a purpose description
- [ ] Navigation hierarchy is clear
- [ ] Covers both authenticated and unauthenticated states (if applicable)

### 7. Non-Functional Requirements

Must cover at minimum:

- [ ] **Performance**: response time targets, throughput expectations
- [ ] **Security**: auth model, data protection, OWASP considerations
- [ ] **Scalability**: growth expectations, bottleneck awareness
- [ ] **Accessibility**: WCAG level target, keyboard navigation, screen reader support
- [ ] **Reliability**: uptime target, error budget, graceful degradation
- [ ] **Observability**: logging, metrics, alerting expectations

### 8. Data Models

- [ ] All core entities defined
- [ ] Each entity has: field name, type, constraints, description
- [ ] Relationships between entities are explicit (1:1, 1:N, N:M)
- [ ] Primary keys and indexes noted
- [ ] Soft delete vs hard delete strategy stated
- [ ] Timestamps (created_at, updated_at) on all entities

### 9. API Contracts

- [ ] Every user-facing feature has corresponding endpoint(s)
- [ ] Each endpoint specifies: method, path, request body/params, response shape, status codes
- [ ] Auth requirements per endpoint (public, authenticated, admin)
- [ ] Pagination strategy for list endpoints
- [ ] Error response format is consistent

### 10. Edge Cases and Error States

- [ ] At least 5 edge cases identified
- [ ] Each has: trigger condition, expected behavior, fallback strategy
- [ ] Covers: network failures, invalid input, concurrent operations, empty states, rate limiting
- [ ] LLM-specific edge cases if AI features present (token limits, API failures, hallucination handling, cost spikes)

### 11. Competitive Landscape

- [ ] 3-7 comparable products analyzed
- [ ] Each with: strengths, weaknesses, our differentiation
- [ ] At least 1 direct competitor and 1 indirect/adjacent competitor
- [ ] Honest about where competitors are stronger

### 12. Milestones

- [ ] MVP defined as strict subset of P0 features
- [ ] v1.0 includes remaining P0 + selected P1 features
- [ ] MVP is launchable and useful on its own
- [ ] Clear criteria for what "done" means for each milestone

### 13. Open Questions

- [ ] At least 3 genuine unknowns
- [ ] Each question identifies who can answer it or how to resolve it
- [ ] Questions are not things the PRD should have answered (that's a quality gap)
- [ ] Includes both product questions and technical questions

### 14. Assumptions Log

- [ ] Every inference made during Phase 1 is logged
- [ ] Each assumption has: statement, confidence level (High/Medium/Low), override flag
- [ ] User-confirmed assumptions marked as confirmed
- [ ] Low-confidence assumptions flagged for validation

### 15. Tech Stack Requirements Extract

- [ ] Maps directly to `/build-stack` intake format
- [ ] Includes: app type, layers needed, suggested language(s), deployment target, compute model, expected scale, team size, must-haves, already-decided, avoid list
- [ ] Derived from PRD decisions (not invented independently)
- [ ] Ready to copy-paste into `/build-stack`

---

## Cross-Section Consistency Checks

- [ ] Every persona appears in at least one user story
- [ ] Every P0 feature has acceptance criteria AND a corresponding API endpoint
- [ ] Data model entities cover all features (no feature references data that doesn't exist)
- [ ] NFR targets are realistic for the inferred scale
- [ ] Edge cases reference real features from the functional requirements
- [ ] MVP milestone features are a subset of the P0 stories
- [ ] Goals are achievable with the defined MVP
- [ ] Non-goals don't contradict any defined features
