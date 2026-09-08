# ADR-001 — Full-Stack Architecture

**Status:** Accepted  
**Date:** 2026-09-07

## Context

Zaytun is a portfolio full-stack marketplace requiring a browser frontend, backend API, persistent relational data, authentication, authorization, and business workflows.

## Decision

Use:
- React for frontend presentation;
- Django for backend application/API;
- RESTful HTTP/JSON as the application boundary;
- MySQL for relational persistence.

The backend will maintain clear responsibility boundaries between API handling, application/business workflows, and persistence.

## Alternatives Considered

### Monolithic Django-rendered UI

Rejected because the project explicitly requires React and RESTful API skills.

### Microservices

Rejected for V1 because the complexity is not justified by the current scale.

### Separate service for every domain

Rejected as premature. Feature-oriented Django organization is sufficient initially.

## Consequences

Positive:
- strong portfolio demonstration of API-driven full-stack development;
- clear frontend/backend boundary;
- relational database suited to orders and ownership;
- relatively straightforward deployment.

Negative:
- more moving parts than server-rendered Django;
- API contract must be maintained explicitly.

## Revisit When

Reconsider if scale, realtime collaboration, external integrations, or deployment constraints materially change.
