# ADR-007 — Authentication Mechanism

**Status:** Accepted
**Date:** 2026-09-08

## Context

`08_Architecture.md` §6 requires the authentication mechanism to be decided and recorded before implementation begins. Zaytun's frontend (React) and backend (Django REST) are separate applications communicating over HTTPS/JSON, but are expected to be served from a configuration where cross-site cookie handling can be controlled (e.g. same-site deployment or a configured proxy in development).

Two realistic options exist for a Django + DRF + React stack:

- **Session-based authentication** using Django's built-in session framework, with CSRF protection for unsafe methods.
- **Token-based authentication** (DRF Token or JWT), which avoids cookie/CSRF concerns but introduces token storage, refresh, and revocation concerns on the frontend.

## Decision

Zaytun V1 uses **session-based authentication**:

- Django's session framework establishes the authenticated identity after `POST /auth/login/`.
- The session cookie is `HttpOnly` and `Secure` in production, with `SameSite` configured appropriately for the deployment topology.
- CSRF protection is enabled for all unsafe HTTP methods (`POST`, `PATCH`, `DELETE`); the frontend reads the CSRF token via Django's standard mechanism and sends it on mutating requests.
- CORS is configured (via `django-cors-headers`, already installed) to allow only the known frontend origin(s), with credentials enabled.
- `GET /auth/me/` is the source of truth the frontend uses to determine the current authenticated identity and role after page load/refresh — the frontend does not persist or trust a client-side copy of the user/role as authoritative.
- Logout invalidates the server-side session.

## Consequences

Positive:
- Reuses Django's mature, well-tested session/CSRF security machinery rather than hand-rolling token issuance and revocation.
- No token storage on the client (no `localStorage`/`sessionStorage` token, reducing XSS token-theft surface).
- Simpler mental model for a single first-party frontend, which matches Zaytun's V1 scope (no third-party API consumers, no native mobile app).

Negative:
- Requires correct CORS + `SameSite`/`Secure` cookie configuration across dev and production; misconfiguration is a common source of "login works locally, breaks in deployment" bugs.
- Less convenient than tokens if a native mobile client or third-party API consumer is introduced later (see Revisit When).
- Requires the frontend to explicitly handle CSRF token retrieval/attachment on mutating requests.

## Revisit When

- A native mobile application (FUT-008) or third-party API consumer is introduced, where cookie-based sessions are impractical.
- Zaytun needs to support multiple frontend origins/subdomains in a way that materially complicates cookie scope.
