# Zaytun 🌿

> **Fuel for a longer life.**

Zaytun is a full-stack portfolio project for connecting farmers with consumers through an organic food marketplace.

## Stack

- Django
- Django REST API
- React
- MySQL

## V1 Product

Zaytun V1 supports:

- Consumers, Farmers, and Admins
- Farmer storefronts
- Organic product listings
- Flexible controlled measurement units
- Product discovery
- Single-farmer shopping carts
- Checkout and orders
- Farmer-managed delivery
- Product reviews
- Cash on Delivery
- Optional sandbox/test payment integration
- Responsive web experience

## Documentation

Start with:

1. `01_ProjectVision.md`
2. `02_Glossary.md`
3. `05_FunctionalRequirements.md`
4. `06_NonFunctionalRequirements.md`
5. `08_Architecture.md`
6. `09_DatabaseDesign.md`
7. `10_API_Specification.md`
8. `03_ProductBacklog.md`
9. `04_ProjectRoadmap.md`

Architectural rationale is stored under `decisions/`.

Sprint execution plans are stored under `sprints/`.

## Engineering Principles

Zaytun follows the project's senior-developer constitution and universal project-builder workflow:

- understand the product before coding;
- model the domain before designing endpoints;
- keep requirements separate from implementation;
- enforce ownership and authorization on the server;
- treat data integrity as a product feature;
- test unhappy paths;
- measure performance before optimizing;
- document important decisions;
- finish with release hardening rather than feature creep.

## V1 Boundary

V1 is a single-country, farmer-delivered marketplace where each cart/order contains products from one farmer.

Multi-farmer orders, delivery fleets, multi-country operation, and production payment processing are future scope.
