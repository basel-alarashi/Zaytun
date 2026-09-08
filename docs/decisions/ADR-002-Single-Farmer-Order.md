# ADR-002 — Single-Farmer Cart and Order

**Status:** Accepted  
**Date:** 2026-09-07

## Context

A multi-farmer marketplace cart introduces split fulfillment, delivery, payment allocation, cancellation, and partial-failure complexity.

## Decision

V1 permits a cart and resulting order to contain products from exactly one farmer.

## Consequences

Positive:
- simpler checkout;
- simpler delivery ownership;
- simpler order lifecycle;
- easier stock handling;
- clearer farmer responsibilities.

Negative:
- consumers cannot combine products from multiple farmers in one checkout.

## Future

Multi-farmer carts and split orders are explicitly future scope and require a new architecture/domain review.
