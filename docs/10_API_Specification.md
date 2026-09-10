# Zaytun — REST API Specification

**Base path:** `/api/v1/`

This document defines the conceptual contract. Exact serializer fields and pagination/error schemas become canonical when implemented and tested.

## 1. Conventions

### Success

Use conventional HTTP semantics:
- `200` successful retrieval/update;
- `201` successful creation;
- `204` successful deletion where appropriate.

### Client errors

- `400` invalid request/business validation;
- `401` unauthenticated;
- `403` authenticated but unauthorized;
- `404` resource unavailable/not found;
- `409` conflict where appropriate.

### Server errors

- `500` unexpected server failure, without leaking implementation details.

## 2. Authentication

```text
POST /auth/register/
POST /auth/login/
POST /auth/logout/
GET /auth/csrf/
GET  /auth/me/
```

The authentication implementation (session or token strategy) is an ADR decision. (Added in '/decisions/ADR-007-Authentication.md')

## 3. Farmers & Storefronts

```text
GET    /farmers/
GET    /farmers/{id}/
PATCH  /farmers/me/
GET    /farmers/{id}/storefront/
PATCH  /farmers/me/storefront/
```

Farmer-owned write operations must derive ownership from authenticated identity.

## 4. Categories & Units

```text
GET    /categories/
GET    /categories/{id}/

GET    /units/
```

Admin-only management endpoints:

```text
POST   /admin/categories/
PATCH  /admin/categories/{id}/
DELETE /admin/categories/{id}/
```

## 5. Products

Public:

```text
GET    /products/
GET    /products/{id}/
```

Farmer:

```text
POST   /farmer/products/
PATCH  /farmer/products/{id}/
DELETE /farmer/products/{id}/
GET    /farmer/products/
```

Supported query concepts may include:

```text
?q=
&category=
&farmer=
&available=
&page=
```

The server owns final filtering, authorization, and pagination behavior.

## 6. Cart

```text
GET    /cart/
POST   /cart/items/
PATCH  /cart/items/{id}/
DELETE /cart/items/{id}/
DELETE /cart/
```

Adding a product from another farmer must return a defined conflict/validation response.

## 7. Addresses

```text
GET    /addresses/
POST   /addresses/
GET    /addresses/{id}/
PATCH  /addresses/{id}/
DELETE /addresses/{id}/
```

Ownership is derived from authentication.

## 8. Checkout & Orders

```text
POST   /checkout/
GET    /orders/
GET    /orders/{id}/
POST   /orders/{id}/cancel/
```

Farmer:

```text
GET    /farmer/orders/
POST   /farmer/orders/{id}/confirm/
POST   /farmer/orders/{id}/prepare/
POST   /farmer/orders/{id}/out-for-delivery/
POST   /farmer/orders/{id}/deliver/
POST   /farmer/orders/{id}/reject/
```

Exact transition endpoints may instead be represented as one transition endpoint if that produces a clearer contract.

## 9. Payments

```text
POST /orders/{id}/payment/
GET  /orders/{id}/payment/
```

For a provider integration, provider-specific callback/webhook endpoints should be isolated and protected by provider verification.

## 10. Reviews

```text
GET    /products/{id}/reviews/
POST   /products/{id}/reviews/
PATCH  /reviews/{id}/
DELETE /reviews/{id}/
```

The server determines eligibility from authenticated purchase history.

## 11. Administration

Conceptual endpoints:

```text
GET    /admin/users/
PATCH  /admin/users/{id}/
GET    /admin/farmers/
PATCH  /admin/farmers/{id}/
GET    /admin/products/
PATCH  /admin/products/{id}/
GET    /admin/reviews/
PATCH  /admin/reviews/{id}/
GET    /admin/orders/
```

## 12. Error Contract

Preferred shape:

```json
{
  "code": "VALIDATION_ERROR",
  "message": "The request could not be processed.",
  "details": {
    "field": ["Reason"]
  }
}
```

Do not expose stack traces, SQL errors, secrets, or internal implementation details.

## 13. API Rules

- Never trust client-supplied ownership.
- Never trust client-supplied final totals.
- Never trust client-supplied role.
- Validate quantities and availability server-side.
- Revalidate cart contents at checkout.
- Enforce order transitions server-side.
- Use pagination for potentially large collections.
- Keep response representations separate from database implementation details.
