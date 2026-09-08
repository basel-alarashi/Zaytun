# Zaytun — Non-Functional Requirements

## NFR-001 Security

The application shall use secure authentication, authorization, input validation, secret management, and safe error handling appropriate to a portfolio-quality web application.

## NFR-002 Authorization

All protected business actions shall be authorized on the server. UI visibility shall never be treated as authorization.

## NFR-003 Data Integrity

Important domain constraints shall be enforced at the appropriate application/database boundaries, including ownership, uniqueness, valid states, and non-negative quantities.

## NFR-004 API Consistency

REST API responses, validation errors, authentication failures, authorization failures, and resource-not-found semantics shall be consistent.

## NFR-005 Maintainability

Backend, frontend, domain/business rules, and infrastructure responsibilities shall remain understandable and cohesive.

## NFR-006 Testability

Important domain rules and API boundaries shall have automated tests. Tests shall include unhappy paths and authorization failures.

## NFR-007 Performance

Performance shall be measured before optimization. Query count, query shape, payload size, frontend rendering, and avoidable round trips shall be inspected before release.

Initial portfolio targets:
- ordinary API requests should normally complete within an acceptable interactive range in local/representative deployment;
- common listing endpoints should avoid obvious N+1 query patterns;
- product listings should use pagination for potentially large result sets.

Exact thresholds shall be validated after representative data exists.

## NFR-008 Responsive Design

The application shall remain usable across desktop, tablet, and mobile viewport sizes.

## NFR-009 Accessibility

Core flows shall support semantic structure, readable contrast, keyboard navigation, labels, focus behavior, and accessible feedback.

## NFR-010 Reliability

Important operations shall fail explicitly rather than silently succeeding. Partial failure scenarios shall be considered for checkout, payment, stock changes, and order transitions.

## NFR-011 Observability

The deployed application shall provide sufficient logs/error information to diagnose important backend failures without leaking sensitive implementation details.

## NFR-012 Configuration

Environment-specific settings and secrets shall not be hard-coded into source control.

## NFR-013 Portability

The architecture shall avoid unnecessary coupling to one payment provider or geographic configuration where doing so would materially block future expansion.

## NFR-014 Documentation

Meaningful architecture, domain, API, database, roadmap, and release decisions shall be documented and kept synchronized.

## NFR-015 Browser Support

The supported browser matrix shall be documented before release. The project shall prioritize current mainstream desktop and mobile browsers.

## NFR-016 Scalability

V1 does not require internet-scale infrastructure. Database indexes, pagination, ownership queries, and service boundaries should nevertheless avoid obvious designs that make ordinary growth unnecessarily expensive.
