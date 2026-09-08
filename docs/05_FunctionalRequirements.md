# Zaytun — Functional Requirements

## Authentication & Identity

- **AUTH-001** The system shall allow a user to register.
- **AUTH-002** The system shall allow authenticated users to log in and log out.
- **AUTH-003** The system shall distinguish Consumer, Farmer, and Admin roles.
- **AUTH-004** Protected operations shall require authentication.
- **AUTH-005** Authorization shall be enforced server-side.
- **AUTH-006** Users shall be prevented from modifying resources they do not own unless their role explicitly permits it.

## Farmer & Storefront

- **FARM-001** A farmer shall have a public storefront.
- **FARM-002** A farmer shall be able to maintain permitted storefront information.
- **FARM-003** A farmer shall be able to create products.
- **FARM-004** A farmer shall be able to edit products they own.
- **FARM-005** A farmer shall be able to control product availability.
- **FARM-006** Product price, quantity, and unit shall be validated.
- **FARM-007** Consumers shall be able to view a farmer storefront.
- **FARM-008** Consumers shall be able to view products belonging to a storefront.

## Products

- **PROD-001** Products shall belong to a farmer.
- **PROD-002** Products shall support categories.
- **PROD-003** Products shall support controlled measurement units.
- **PROD-004** Products shall expose current price and availability.
- **PROD-005** Product search shall be supported.
- **PROD-006** Product filtering shall be supported where included in V1.
- **PROD-007** Product stock shall not become negative through valid operations.

## Cart

- **CART-001** An authenticated consumer shall have a cart.
- **CART-002** A cart shall contain cart items.
- **CART-003** A cart shall contain products from only one farmer in V1.
- **CART-004** Consumers shall be able to add, remove, and update cart items.
- **CART-005** The system shall validate product availability and quantity before checkout.
- **CART-006** Client-supplied totals shall not be trusted as authoritative order totals.

## Checkout & Orders

- **ORDER-001** A valid cart shall be convertible into an order.
- **ORDER-002** An order shall belong to one consumer and one farmer in V1.
- **ORDER-003** An order shall contain immutable purchase-line information sufficient to preserve what was ordered.
- **ORDER-004** An order shall use a controlled lifecycle.
- **ORDER-005** Invalid state transitions shall be rejected.
- **ORDER-006** A consumer shall be able to view their own orders.
- **ORDER-007** A farmer shall be able to view orders belonging to them.
- **ORDER-008** A farmer shall be able to perform permitted fulfillment transitions.
- **ORDER-009** Delivery shall be farmer-managed in V1.

## Addresses

- **ADDR-001** A consumer shall be able to maintain delivery addresses.
- **ADDR-002** A consumer shall only access their own addresses.
- **ADDR-003** Checkout shall require a valid delivery address.
- **ADDR-004** The order shall preserve the delivery information required by the order record even if the consumer later edits an address.

## Payments

- **PAY-001** Cash on Delivery shall be supported.
- **PAY-002** The system may support a sandbox/test online gateway if technically and operationally feasible for V1.
- **PAY-003** Payment status shall be represented independently from order status.
- **PAY-004** The backend shall validate gateway callbacks/results rather than trusting frontend payment claims.
- **PAY-005** Payment identifiers and provider responses required for reconciliation shall be retained according to the final payment design.

## Reviews

- **REVIEW-001** A consumer shall be able to review an eligible purchased product.
- **REVIEW-002** Reviews shall contain a rating and optional written content according to final UI requirements.
- **REVIEW-003** Review ownership shall be enforced server-side.
- **REVIEW-004** Eligibility shall be determined from server-side order/purchase data.
- **REVIEW-005** Admin shall be able to moderate permitted reviews.

## Administration

- **ADMIN-001** Admins shall have protected administrative capabilities.
- **ADMIN-002** Admins shall be able to manage permitted users/farmers.
- **ADMIN-003** Admins shall be able to manage product categories.
- **ADMIN-004** Admins shall be able to moderate permitted products and reviews.
- **ADMIN-005** Admin operations shall be authorized server-side.

## UX States

- **UX-001** The frontend shall represent loading states.
- **UX-002** The frontend shall represent empty states.
- **UX-003** The frontend shall represent validation and API errors.
- **UX-004** The frontend shall represent unavailable/out-of-stock products.
- **UX-005** The frontend shall provide feedback for successful and failed important actions.
