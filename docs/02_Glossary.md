# Zaytun — Glossary

**Status:** Canonical terminology

## 1. Actors

| Term | Meaning |
|---|---|
| User | Authenticated person with a Zaytun account. |
| Consumer | User who discovers and purchases products. |
| Farmer | User who operates a storefront and sells products. |
| Admin | Authorized platform operator. |

## 2. Marketplace

| Term | Meaning |
|---|---|
| Marketplace | The Zaytun environment connecting consumers and farmers. |
| Storefront | A farmer's public presence containing farmer information and products. |
| Product | A sellable organic food item offered by a farmer. |
| Category | A classification used to organize products. |
| Unit | Controlled measurement used with a product quantity, such as kg, liter, piece, or bunch. |
| Availability | Whether a product can currently be ordered. |
| Stock | Quantity currently available for ordering. |
| Price | Monetary amount associated with the product's defined selling unit. |

## 3. Shopping

| Term | Meaning |
|---|---|
| Cart | A consumer's temporary collection of products awaiting checkout. |
| Cart Item | A product and requested quantity in a cart. |
| Checkout | The process of converting a valid cart into an order. |
| Order | A confirmed purchase request belonging to one consumer and one farmer in V1. |
| Order Item | Snapshot of a product purchase within an order. |
| Order Status | Current lifecycle state of an order. |

## 4. Delivery & Payment

| Term | Meaning |
|---|---|
| Address | A consumer delivery location stored for ordering. |
| Delivery | Farmer-side fulfillment and delivery of an order in V1. |
| Payment Method | The mechanism selected to pay, such as COD or supported sandbox gateway. |
| Payment | The recorded financial state associated with an order. |
| COD | Cash on Delivery. |

## 5. Trust & Feedback

| Term | Meaning |
|---|---|
| Review | Consumer feedback attached to a product. |
| Rating | Numerical score associated with a review. |
| Eligible Reviewer | Consumer who satisfies the business rule required to review a product. |
| Moderation | Administrative handling of content that violates marketplace rules. |

## 6. Geographic Model

| Term | Meaning |
|---|---|
| Country | A supported country. V1 enables one country. |
| Region | First-level geographic subdivision used by the supported country. |
| City | City/locality within a region. |
| Location | Human-readable geographic information associated with a farmer or address. |

## 7. State Vocabulary

Order statuses should use one canonical vocabulary throughout UI, API, database, and tests. Proposed V1 states:

`Pending → Confirmed → Preparing → OutForDelivery → Delivered`

Terminal/exception states:

`Cancelled`, `Rejected`

Payment statuses should be kept separate from order statuses.

## 8. Terms to Avoid

- Do not use **seller** and **farmer** interchangeably in user-facing terminology.
- Do not use **store** and **storefront** interchangeably when referring to the farmer's public profile.
- Do not treat **cart** and **order** as the same object.
- Do not treat **availability** as identical to stock quantity.
- Do not describe a review as proof that a farmer is certified organic.
