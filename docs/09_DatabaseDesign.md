# Zaytun — Database Design

**Database:** MySQL

## 1. Design Principles

- Model domain ownership explicitly.
- Preserve historical order information.
- Use foreign keys and constraints where appropriate.
- Design indexes around actual query patterns.
- Treat migrations as source-controlled changes.
- Avoid using database structure as a substitute for business rules.

## 2. Core Entities

### User

Represents authentication identity and role.

Key concepts:
- id
- email/username identity
- password credential representation
- role
- active state
- timestamps

### FarmerProfile

One farmer-specific profile associated with a User.

Key concepts:
- id
- user_id
- farm/storefront name
- description
- location fields
- public status
- timestamps

### Category

Controlled product classification.

Key concepts:
- id
- name
- slug
- active state

### Unit

Controlled measurement unit.

Examples may include:
- g
- kg
- ml
- L
- piece
- dozen
- bunch
- box
- package

The final allowed catalogue should be controlled rather than arbitrary free text.

### Product

A sellable organic item belonging to one farmer.

Key concepts:
- id
- farmer_id
- category_id
- unit_id
- name
- description
- price
- stock_quantity
- active/available state
- timestamps

### Address

A consumer delivery address.

Key concepts:
- id
- consumer_id
- country_id or supported-country reference if implemented
- region
- city
- address lines
- postal code where applicable
- label
- default flag
- timestamps

### Cart

A consumer's current shopping cart.

Key concepts:
- id
- consumer_id
- farmer_id (V1 single-farmer constraint)
- timestamps

### CartItem

A product and quantity in a cart.

Key concepts:
- id
- cart_id
- product_id
- quantity
- timestamps

Uniqueness:
- one cart should contain at most one row per product.

### Order

Confirmed purchase transaction.

Key concepts:
- id
- consumer_id
- farmer_id
- delivery address snapshot
- subtotal
- delivery fee if introduced
- total
- currency
- status
- timestamps

The order must preserve enough information to remain historically understandable if the product/storefront changes later.

### OrderItem

Historical purchase line.

Key concepts:
- id
- order_id
- product_id nullable depending on deletion policy
- product_name_snapshot
- unit_price_snapshot
- unit_snapshot
- quantity
- line_total

Order items should not depend on current product price/name to reconstruct historical purchases.

### Payment

Financial state associated with an order.

Key concepts:
- id
- order_id
- method
- status
- amount
- currency
- provider
- provider_reference
- timestamps

### Review

Consumer feedback for a product.

Key concepts:
- id
- consumer_id
- product_id
- order_item/order reference as required for eligibility
- rating
- comment
- moderation status
- timestamps

A uniqueness rule should be selected during implementation for the desired review policy.

### Country / Region

V1 enables one country but the geographic model should not make future expansion unnecessarily difficult.

## 3. Relationship Overview

```text
User
├── 0..1 FarmerProfile
├── 1..N Addresses (consumer)
├── 1 Cart (consumer)
└── 1..N Orders (consumer)

FarmerProfile
└── 1..N Products

Category
└── 1..N Products

Unit
└── 1..N Products

Cart
└── 1..N CartItems
      └── 1 Product

Order
├── 1..N OrderItems
├── 1 Payment
└── 1 Farmer + 1 Consumer

Product
└── 0..N Reviews
```

## 4. Important Invariants

1. Product belongs to exactly one farmer.
2. Farmer can modify only owned products.
3. Cart belongs to exactly one consumer.
4. V1 cart belongs to at most one farmer.
5. Order belongs to exactly one consumer and one farmer.
6. Order total is server-calculated.
7. Order item price is historical and must not be recalculated from current product price.
8. Product stock cannot become negative.
9. Review eligibility comes from purchase history, not frontend claims.
10. Admin authorization is server-enforced.
11. Order transitions follow an explicit state machine.
12. Payment state and order state are distinct.

## 5. Delete Semantics

Default principle:
- avoid destructive deletion of records required for historical orders;
- prefer inactive/soft-delete behavior for products, categories, and storefronts where history depends on them;
- determine explicit `CASCADE`, `RESTRICT`, or `SET NULL` behavior for each relationship during implementation.

## 6. Index Strategy

Likely indexes:
- User unique email/identity;
- FarmerProfile user_id;
- Product farmer_id;
- Product category_id;
- Product active/available;
- Product searchable fields as supported by MySQL strategy;
- Cart consumer_id;
- CartItem cart_id + product_id unique;
- Order consumer_id + created_at;
- Order farmer_id + created_at;
- Order status;
- OrderItem order_id;
- Review product_id;
- Review consumer_id.

Indexes must be validated against real query patterns rather than added mechanically.

## 7. Concurrency

Checkout must consider concurrent purchases of limited stock.

The final implementation should use an appropriate transactional strategy so two simultaneous checkouts cannot safely consume the same inventory.

## 8. Migration Discipline

Every schema change must be represented by a version-controlled migration and tested against a clean database setup.
