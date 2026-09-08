# Zaytun — Architecture

## 1. Architectural Goal

Use the simplest architecture that clearly separates presentation, API boundaries, application workflows, business rules, and persistence while remaining appropriate for a portfolio full-stack marketplace.

## 2. High-Level Architecture

```text
┌───────────────────────────┐
│          React            │
│ Presentation / UI State   │
└─────────────┬─────────────┘
              │ HTTPS / JSON
              ▼
┌───────────────────────────┐
│      Django REST API      │
│ API / Validation / Auth   │
└─────────────┬─────────────┘
              ▼
┌───────────────────────────┐
│ Application / Domain      │
│ Workflows & Business Rules│
└─────────────┬─────────────┘
              ▼
┌───────────────────────────┐
│ Django ORM / Infrastructure│
└─────────────┬─────────────┘
              ▼
┌───────────────────────────┐
│          MySQL            │
└───────────────────────────┘

External boundary:
Django → Sandbox Payment Provider (optional V1)
```

## 3. Backend Organization

A feature-oriented Django organization is preferred over excessive architectural ceremony.

Conceptual structure:

```text
backend/
├── config/
├── apps/
│   ├── accounts/
│   ├── farmers/
│   ├── catalog/
│   ├── cart/
│   ├── orders/
│   ├── payments/
│   ├── reviews/
│   └── administration/
├── tests/
└── manage.py
```

The exact Django app split may be adjusted if implementation evidence shows a simpler structure is clearer.

## 4. Responsibility Boundaries

### API / Presentation boundary
- HTTP routing
- serializers/request validation
- authentication context
- HTTP status semantics

### Application/business layer
- checkout workflow
- order transitions
- ownership checks
- cart/farmer constraint
- review eligibility
- payment workflow coordination

### Persistence
- Django models
- migrations
- database constraints
- indexes
- transactions

### React
- presentation
- user interaction
- client-side convenience validation
- API communication
- server-state rendering
- local UI state

React shall not become the authoritative source for price, ownership, role, stock, or authorization.

## 5. API Strategy

Use resource-oriented REST endpoints with explicit serializers and consistent error responses.

Example resource families:

```text
/auth/
/users/
/farmers/
/storefronts/
/categories/
/products/
/cart/
/addresses/
/orders/
/payments/
/reviews/
/admin/
```

Exact endpoints are canonicalized in `10_API_Specification.md`.

## 6. Authentication

Authentication mechanism shall be selected and recorded in an ADR before implementation.

Requirements:
- secure credential handling;
- protected API endpoints;
- authenticated identity available to business logic;
- server-side role checks;
- safe logout/expiry behavior.

## 7. Authorization

Authorization follows:

```text
Authenticated identity
        ↓
Role / permission check
        ↓
Ownership / business-rule check
        ↓
Operation
```

Client-provided user IDs, farmer IDs, roles, prices, totals, or privileged flags shall not be trusted.

## 8. Transactions

Operations that modify multiple related records must be considered transactional, especially:
- checkout;
- inventory reservation/decrement;
- payment state changes;
- order state transitions where multiple records change.

The final implementation must explicitly handle partial failure.

## 9. Payment Boundary

Payment provider logic shall remain outside the core order business rules as much as practical.

Conceptual flow:

```text
Checkout
   ↓
Create/prepare payment
   ↓
External provider
   ↓
Verified result/callback
   ↓
Payment record
   ↓
Order state
```

Provider-specific details must not be accepted directly from an untrusted frontend.

## 10. Frontend State

Separate:
- local UI state;
- authenticated user/application state;
- server state;
- transient checkout state.

Do not allow multiple mechanisms to own the same source of truth.

## 11. Security Architecture

Consider:
- password security;
- authentication token/session security;
- CSRF strategy where applicable;
- CORS policy;
- input validation;
- object-level authorization;
- rate limiting where appropriate;
- secure secrets;
- safe error messages;
- dependency/security updates.

## 12. Performance

Measure:
- query counts;
- N+1 patterns;
- pagination;
- payload size;
- frontend rendering;
- redundant requests.

Do not introduce caching or complex optimization until a measurable need exists.

## 13. Deployment

Deployment architecture is intentionally not locked yet.

The production-quality portfolio release must document:
- environment configuration;
- database migration process;
- frontend build;
- backend serving;
- static/media handling;
- secrets;
- logging;
- rollback/recovery expectations.

## 14. Architectural Non-Goals

V1 does not require:
- microservices;
- event sourcing;
- CQRS framework;
- message broker;
- Kubernetes;
- real-time collaboration infrastructure;
- distributed caching infrastructure.

These may be introduced only if a concrete requirement earns them a place.

## 15. Architecture Review Triggers

Revisit architecture if:
- multi-farmer orders become V1 scope;
- delivery drivers are introduced;
- multiple countries are activated;
- production payment requirements change;
- collaboration/realtime features are introduced;
- observed performance measurements justify additional infrastructure.
