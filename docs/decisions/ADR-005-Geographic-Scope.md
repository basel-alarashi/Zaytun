# ADR-005 — Single-Country V1

**Status:** Accepted  
**Date:** 2026-09-07

## Context

The product should launch as a coherent marketplace rather than implementing international logistics, currencies, and regulatory variation prematurely.

## Decision

V1 supports one country.

The data/domain model should avoid unnecessary assumptions that would make future countries impossible, but multi-country behavior is not implemented.

## Consequences

Positive:
- simpler addresses;
- simpler delivery rules;
- simpler currency assumptions;
- focused V1.

Negative:
- no international marketplace in V1.
