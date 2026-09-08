# ADR-003 — Controlled Flexible Product Units

**Status:** Accepted  
**Date:** 2026-09-07

## Context

Organic products can be sold by weight, volume, count, or packaging. A single fixed unit would make the catalog unnecessarily restrictive.

## Decision

Products use a controlled Unit entity/catalog rather than arbitrary free-text units.

Examples:
- kg
- g
- L
- ml
- piece
- dozen
- bunch
- box
- package

Automatic unit detection is not part of V1.

## Consequences

Positive:
- consistent display;
- validation;
- easier filtering and reporting;
- extensibility.

Negative:
- unit catalogue requires administration/design.

## Revisit When

A genuine need for compound units, conversions, variable-weight products, or seller-defined units emerges.
