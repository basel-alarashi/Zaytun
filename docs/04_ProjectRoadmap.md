# Zaytun — Project Roadmap

**Release target:** Zaytun V1.0 portfolio-quality release

## Roadmap Principles

- Sequence by dependency, product value, and risk.
- Discover core marketplace problems early.
- Keep each sprint outcome-oriented.
- Avoid adding future features to V1.
- End with hardening rather than feature expansion.
- A roadmap can change only through an explicit decision.

---

## Sprint 0 — Discovery & Foundation

**Goal:** Establish the product, architecture, repository, development environment, and documentation foundation.

Deliverables:
- Project vision
- Glossary
- Requirements
- Initial domain model
- Architecture decision
- Initial database design
- API strategy
- Backlog
- Roadmap
- Repository structure
- Development environment

---

## Sprint 1 — Technical Foundation

**Goal:** Produce a working full-stack skeleton with a reliable API/frontend/database connection.

Stages:
- A — Django project and configuration
- B — REST API foundation
- C — React foundation and API integration
- D — MySQL connection/migrations
- E — Development quality tooling

Exit:
- Backend runs.
- Frontend runs.
- Database migrations work.
- Frontend can communicate with API.
- Baseline tests run.

---

## Sprint 2 — Identity & Access

**Goal:** Establish users, authentication, roles, and authorization.

Stages:
- A — User/domain model
- B — Authentication API
- C — Role/permission enforcement
- D — React authentication flow
- E — Security tests

Exit:
- Consumer, Farmer, and Admin roles work.
- Protected APIs reject unauthorized access.
- Ownership is server-side.

---

## Sprint 3 — Farmers, Storefronts & Products

**Goal:** Build the supply side of Zaytun.

Stages:
- A — Farmer/storefront/product/category/unit data model
- B — Farmer/product APIs
- C — Farmer management UI
- D — Public storefront/product UI
- E — Validation and tests

Exit:
- Farmer can manage products.
- Consumer can view storefronts and products.
- Availability, price, stock, and unit rules work.

---

## Sprint 4 — Discovery & Shopping Cart

**Goal:** Allow consumers to discover products and construct a valid single-farmer cart.

Stages:
- A — Search/filter query design
- B — Product discovery APIs
- C — Search/category/storefront UI
- D — Cart behavior
- E — Single-farmer constraint and validation

Exit:
- Consumer can discover products.
- Consumer can add/change/remove cart items.
- Cart cannot contain multiple farmers.

---

## Sprint 5 — Checkout, Payments & Orders

**Goal:** Convert valid carts into complete orders and establish the order lifecycle.

Stages:
- A — Order/payment/address model
- B — Checkout/order APIs
- C — COD flow
- D — Sandbox payment integration if feasible
- E — Checkout/order UI
- F — Order state transitions

Exit:
- Valid cart can become an order.
- Invalid stock/ownership/state is rejected.
- Payment state is recorded independently.
- Consumer and farmer can view appropriate order information.

---

## Sprint 6 — Reviews & Administration

**Goal:** Complete trust and platform-management capabilities.

Stages:
- A — Review domain rules
- B — Review APIs
- C — Product review UI
- D — Admin management
- E — Moderation and authorization tests

Exit:
- Eligible consumers can review purchased products.
- Admin can moderate permitted content.
- Unauthorized review/admin operations fail.

---

## Sprint 7 — Hardening & Release

**Goal:** Turn the completed feature set into a verified portfolio-quality release.

Areas:
- Security audit
- Data-integrity audit
- API consistency
- Automated test coverage
- Query/performance inspection
- Responsive UI review
- Accessibility review
- Error/loading/empty states
- Logging and recovery
- Environment configuration
- Deployment
- Documentation synchronization
- README/portfolio presentation
- Release checklist

Exit:
- V1 scope is complete.
- Critical defects are resolved.
- Build/migrations/tests are reproducible.
- Deployment is documented.
- Release evidence exists.

---

## Release Boundary

After Sprint 7, V1 is declared complete unless a critical release-blocking defect requires corrective work.

New major features should enter V1.1/V2 rather than extending V1 indefinitely.
