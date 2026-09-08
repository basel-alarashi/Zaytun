# Zaytun — Project Vision

**Product:** Zaytun  
**Tagline:** *Fuel for a longer life.*  
**Version:** V1.0  
**Status:** Canonical / Draft for review  
**Stack:** Django + RESTful API + React + MySQL

---

## 1. Product Identity

Zaytun is a web marketplace that connects consumers with farmers offering organic food and enables consumers to discover, order, and review organic products directly from participating farmers.

Zaytun is intentionally more than a generic CRUD marketplace. Its core identity is the connection between:

**farmer → farm storefront → organic products → consumer → order**

---

## 2. Vision

Create a trustworthy digital marketplace that makes organic food easier to discover and purchase while giving farmers a direct digital storefront through which they can present and sell their products.

---

## 3. Mission

Zaytun aims to:

- make organic food discovery simple;
- give farmers a direct presence in the digital marketplace;
- make product availability and ordering understandable;
- provide a trustworthy product-review mechanism;
- create a foundation that can later expand geographically and operationally.

---

## 4. Problem Statement

Consumers may find it difficult to discover trustworthy organic food producers, compare available products, and order directly from farmers.

Farmers may lack a simple digital channel through which they can present their farm, publish products, manage availability, and receive orders.

Zaytun addresses both sides through one marketplace.

---

## 5. Proposed Solution

Zaytun provides:

1. Consumer accounts and profiles.
2. Farmer accounts and public storefronts.
3. Organic product listings across multiple product categories.
4. Flexible product measurement units.
5. Search and product discovery.
6. A cart restricted to one farmer in V1.
7. Checkout and order management.
8. Farmer-managed order fulfillment/delivery.
9. Product reviews from eligible purchasers.
10. Administration and moderation capabilities.
11. Optional online payment through a test/sandbox gateway when feasible, with Cash on Delivery as the fallback V1 method.

---

## 6. Target Users

### Consumer

A person who wants to discover and purchase organic food from farmers.

Primary goals:

- discover products;
- evaluate product information;
- choose quantities;
- place orders;
- pay using an available method;
- receive the order;
- review purchased products.

### Farmer

A farmer who sells organic products through Zaytun.

Primary goals:

- establish a storefront;
- publish products;
- manage price and availability;
- receive orders;
- prepare and deliver orders;
- maintain a sales history.

### Admin

A platform operator responsible for maintaining marketplace integrity.

Primary goals:

- manage users and farmer accounts;
- moderate products and reviews;
- manage categories and controlled data;
- monitor orders and platform activity;
- resolve administrative issues.

---

## 7. Core Product Principles

1. **Trust first** — product and farmer information should be clear and honest.
2. **Farmer visibility** — farmers are first-class participants, not anonymous suppliers.
3. **Simple ordering** — the V1 purchase journey should be understandable.
4. **Server-enforced rules** — authorization, ownership, pricing, stock, and order rules are enforced by the backend.
5. **Organic marketplace identity** — the product experience should remain centered on organic food.
6. **Extensible foundations** — future geographic and marketplace capabilities should not be blocked unnecessarily.
7. **Scope discipline** — V1 should remain coherent rather than attempting every future marketplace feature.

---

## 8. Core User Journeys

### Consumer journey

Register/login → discover products → inspect product → inspect farmer storefront → add product to cart → checkout → select delivery address → select payment → place order → track order → receive order → review purchased product.

### Farmer journey

Register/login → complete farmer profile/storefront → create product → configure price/unit/availability → receive order → accept/process order → prepare order → deliver order → complete order.

### Admin journey

Login → inspect platform activity → manage users/farmers/products/categories/reviews/orders → moderate or correct permitted data → monitor operational integrity.

---

## 9. V1 Scope

### Included

- Authentication and role-based access.
- Consumer profile.
- Farmer profile and storefront.
- Admin area.
- Product categories.
- Product management.
- Flexible controlled measurement units.
- Product availability/stock.
- Product search and filtering.
- Single-farmer cart.
- Checkout.
- Consumer addresses.
- Orders and order status.
- Farmer-side order management.
- Farmer delivery.
- Product reviews.
- Cash on Delivery.
- Sandbox/test online payment if the selected gateway can be integrated without production financial requirements.
- Responsive web UI.
- REST API.
- Validation, authorization, and data-integrity rules.
- Basic logging/error handling and release hardening.

---

## 10. Explicitly Out of Scope for V1

- Multi-farmer carts and split orders.
- Zaytun-operated delivery fleet.
- Third-party delivery marketplace.
- International/multi-country operation.
- Real production payment processing.
- Consumer-to-consumer marketplace.
- Subscription boxes.
- Auctions.
- Live chat.
- Social networking/following.
- Advanced recommendation/ML systems.
- Complex loyalty/rewards program.
- Native mobile applications.
- Real-time collaborative features.

---

## 11. Future Vision

Potential later versions may introduce:

- multiple countries;
- multi-farmer carts and split fulfillment;
- delivery drivers;
- third-party delivery integrations;
- production payment providers;
- richer farmer verification;
- farm certifications;
- favorites/wishlists;
- notifications;
- promotions and coupons;
- subscriptions;
- analytics dashboards;
- mobile applications;
- advanced search/recommendations.

Future possibilities must not silently become V1 requirements.

---

## 12. Success Criteria

V1 should allow a complete, demonstrable marketplace journey:

> A consumer can discover an organic product from a farmer, add it to a valid cart, place an order, and complete the resulting order lifecycle while the farmer can manage the product and fulfill the order.

Additional success criteria:

- unauthorized users cannot perform protected actions;
- ownership is enforced server-side;
- invalid order states are rejected;
- reviews are limited to eligible purchasers;
- product quantity/unit/price information remains consistent;
- responsive layouts remain usable on desktop, tablet, and mobile;
- the project can be built, migrated, tested, and deployed reproducibly.

---

## 13. Product Boundary

Zaytun V1 is a **single-country, farmer-delivered organic marketplace**.

The marketplace is intentionally constrained to one farmer per order. This simplifies fulfillment while preserving a clean path toward future multi-farmer ordering.

---

## 14. Locked Decisions

| Decision | V1 decision |
|---|---|
| Name | Zaytun |
| Tagline | Fuel for a longer life. |
| Backend | Django |
| API | RESTful API |
| Frontend | React |
| Database | MySQL |
| Geographic scope | One country |
| Delivery | Farmer-delivered |
| Roles | Consumer, Farmer, Admin |
| Products | All organic product categories |
| Units | Flexible controlled units |
| Storefront | Yes |
| Reviews | Product reviews |
| Cart | One farmer per cart/order |
| Responsive | Desktop + tablet + mobile |
| Payment | COD + feasible sandbox/test gateway |

---

## 15. Release Philosophy

V1 is a portfolio-quality product release, not a claim that every production marketplace concern has been solved.

The final release audit must distinguish verified capabilities from future hardening work.
