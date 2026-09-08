# Zaytun — Product Backlog

**Priorities:** Must / Should / Could / Won't for V1

## Epic E01 — Identity & Access

| ID | Feature | Priority | Story |
|---|---|---|---|
| AUTH-001 | Registration | Must | As a user, I can create an account. |
| AUTH-002 | Login/logout | Must | As a user, I can securely access and leave my account. |
| AUTH-003 | Role authorization | Must | As the system, I enforce Consumer/Farmer/Admin permissions. |
| AUTH-004 | Profile | Must | As a user, I can maintain relevant profile information. |

## Epic E02 — Farmer Storefront

| ID | Feature | Priority | Story |
|---|---|---|---|
| FARM-001 | Farmer profile | Must | As a farmer, I can create my public farmer profile. |
| FARM-002 | Storefront | Must | As a consumer, I can view a farmer's storefront. |
| FARM-003 | Farmer product management | Must | As a farmer, I can create, edit, and deactivate my products. |
| FARM-004 | Product availability | Must | As a farmer, I can control whether products are orderable. |

## Epic E03 — Product Discovery

| ID | Feature | Priority | Story |
|---|---|---|---|
| PROD-001 | Categories | Must | As a consumer, I can browse products by category. |
| PROD-002 | Product details | Must | As a consumer, I can inspect product information. |
| PROD-003 | Search | Must | As a consumer, I can search for products. |
| PROD-004 | Filtering | Should | As a consumer, I can narrow product results. |
| PROD-005 | Stock/unit display | Must | As a consumer, I can understand price, unit, and availability. |

## Epic E04 — Cart & Checkout

| ID | Feature | Priority | Story |
|---|---|---|---|
| CART-001 | Add to cart | Must | As a consumer, I can add an available product. |
| CART-002 | Quantity changes | Must | As a consumer, I can change requested quantity. |
| CART-003 | Single-farmer constraint | Must | As the system, I prevent products from different farmers from entering one cart. |
| CART-004 | Cart validation | Must | As the system, I validate availability before checkout. |
| ORDER-001 | Checkout | Must | As a consumer, I can submit a valid cart as an order. |
| ORDER-002 | Address selection | Must | As a consumer, I can choose a delivery address. |
| ORDER-003 | Payment method | Must | As a consumer, I can select an available payment method. |

## Epic E05 — Orders & Fulfillment

| ID | Feature | Priority | Story |
|---|---|---|---|
| ORDER-004 | Order history | Must | As a consumer, I can view my orders. |
| ORDER-005 | Order detail | Must | As a consumer, I can inspect an order and its status. |
| FARM-005 | Farmer order queue | Must | As a farmer, I can see orders containing my products. |
| FARM-006 | Order status transitions | Must | As a farmer, I can advance permitted order states. |
| FARM-007 | Delivery completion | Must | As a farmer, I can mark an order delivered. |
| ORDER-006 | Cancellation | Should | As an authorized actor, I can cancel an order when business rules permit. |

## Epic E06 — Reviews

| ID | Feature | Priority | Story |
|---|---|---|---|
| REVIEW-001 | Product review | Must | As an eligible consumer, I can review a purchased product. |
| REVIEW-002 | Rating | Must | As an eligible consumer, I can rate a purchased product. |
| REVIEW-003 | Review moderation | Must | As an admin, I can moderate permitted review content. |

## Epic E07 — Administration

| ID | Feature | Priority | Story |
|---|---|---|---|
| ADMIN-001 | User management | Must | As an admin, I can manage platform users within permitted operations. |
| ADMIN-002 | Farmer management | Must | As an admin, I can manage farmer accounts/storefront state. |
| ADMIN-003 | Category management | Must | As an admin, I can manage product categories. |
| ADMIN-004 | Product moderation | Must | As an admin, I can moderate product listings. |
| ADMIN-005 | Order visibility | Should | As an admin, I can inspect marketplace orders for support/operations. |

## Epic E08 — Payments

| ID | Feature | Priority | Story |
|---|---|---|---|
| PAY-001 | COD | Must | As a consumer, I can choose Cash on Delivery. |
| PAY-002 | Sandbox gateway | Should | As a consumer, I can use a supported test payment gateway when integration is feasible. |
| PAY-003 | Payment status | Must | As the system, I can record payment state independently from order state. |

## Epic E09 — Quality & Platform

| ID | Feature | Priority | Story |
|---|---|---|---|
| PLAT-001 | REST API validation | Must | As the system, I validate external input consistently. |
| PLAT-002 | Ownership enforcement | Must | As the system, users can access only permitted resources. |
| PLAT-003 | Responsive UI | Must | As a user, I can use Zaytun on desktop, tablet, and mobile. |
| PLAT-004 | Error/loading/empty states | Must | As a user, I receive clear feedback for non-happy paths. |
| PLAT-005 | Automated tests | Must | As the project, important domain and API behavior is protected by tests. |
| PLAT-006 | Release hardening | Must | As the project, security, reliability, performance, accessibility, and deployment are reviewed. |

---

## V1 Out-of-Scope Backlog

| ID | Future Feature |
|---|---|
| FUT-001 | Multi-farmer cart/split orders |
| FUT-002 | Zaytun delivery drivers |
| FUT-003 | Third-party delivery marketplace |
| FUT-004 | Multi-country operation |
| FUT-005 | Production payment processing |
| FUT-006 | Subscriptions |
| FUT-007 | Live chat |
| FUT-008 | Native mobile application |
| FUT-009 | Advanced recommendations |
| FUT-010 | Loyalty/rewards |

---

## Acceptance-Criteria Principle

Every backlog item becomes implementation-ready only when its acceptance criteria are explicit and testable. Large features should be decomposed into smaller stories/tasks before entering a sprint.
