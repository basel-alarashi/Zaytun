# ADR-004 — V1 Payment Strategy

**Status:** Accepted with implementation gate  
**Date:** 2026-09-07

## Context

The project should demonstrate a payment workflow if it can do so safely without requiring real financial transactions.

## Decision

Cash on Delivery is mandatory for V1.

A sandbox/test payment gateway may be integrated when a suitable provider can be used without production financial processing. The provider must be isolated behind a payment boundary and its callbacks/results verified server-side.

## Consequences

Positive:
- V1 remains usable even without external payment integration;
- portfolio can demonstrate payment concepts when feasible;
- production financial risk is avoided.

Negative:
- external sandbox integration adds complexity;
- provider-specific behavior requires testing.

## Revisit When

Production payments become a requirement.
