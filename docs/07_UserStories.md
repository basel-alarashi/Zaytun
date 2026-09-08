# Zaytun — User Stories & Acceptance Criteria

## Consumer Stories

### US-CONS-001 — Register

**As a consumer, I want to create an account so that I can place orders.**

Acceptance criteria:
- Valid registration creates an account.
- Invalid required data is rejected.
- Duplicate account identity is rejected.
- New users receive the intended default role.
- Sensitive credentials are not exposed in API responses.

### US-CONS-002 — Discover products

**As a consumer, I want to browse organic products so that I can find food to buy.**

Acceptance criteria:
- Product listings show essential information.
- Unavailable products are clearly represented.
- Pagination works when applicable.
- Search/filter inputs are validated.

### US-CONS-003 — View farmer storefront

**As a consumer, I want to view a farmer storefront so that I know who offers the products.**

Acceptance criteria:
- Public storefront displays permitted farmer information.
- Products belonging to the farmer are displayed.
- Disabled/inactive products follow marketplace visibility rules.

### US-CONS-004 — Build a cart

**As a consumer, I want to add products to my cart so that I can purchase them.**

Acceptance criteria:
- Available product can be added.
- Quantity cannot exceed permitted availability.
- A second farmer's product cannot be added to an existing single-farmer cart without the defined replacement action.

### US-CONS-005 — Checkout

**As a consumer, I want to place a valid order so that the farmer can fulfill it.**

Acceptance criteria:
- Cart is revalidated server-side.
- Address is valid and owned by the consumer.
- Price/quantity are calculated server-side.
- Order is associated with one farmer.
- Order and relevant inventory/payment records remain consistent after success.

### US-CONS-006 — Track order

**As a consumer, I want to view order status so that I know what is happening.**

Acceptance criteria:
- Consumer sees only their orders.
- Status is displayed using canonical vocabulary.
- Invalid transitions are not exposed as valid actions.

### US-CONS-007 — Review product

**As a consumer, I want to review a purchased product so that I can share my experience.**

Acceptance criteria:
- Eligibility is checked server-side.
- Consumer cannot review a product they did not purchase.
- Review belongs to the authenticated consumer.
- Rating is validated.
- Moderated/removed reviews follow defined visibility rules.

## Farmer Stories

### US-FARM-001 — Manage storefront

**As a farmer, I want to maintain my storefront so that consumers can learn about my farm.**

Acceptance criteria:
- Farmer can modify only their storefront.
- Required information is validated.
- Public consumers can view the resulting storefront.

### US-FARM-002 — Manage products

**As a farmer, I want to publish and maintain products so that consumers can order them.**

Acceptance criteria:
- Farmer can create products they own.
- Farmer cannot modify another farmer's products.
- Price, stock, unit, category, and availability are validated.

### US-FARM-003 — Fulfill order

**As a farmer, I want to process and deliver orders so that consumers receive their purchases.**

Acceptance criteria:
- Farmer sees only relevant orders.
- Only permitted transitions are allowed.
- Delivery completion records the appropriate final state.
- Invalid/unauthorized transitions fail.

## Admin Stories

### US-ADMIN-001 — Moderate marketplace

**As an admin, I want to manage permitted marketplace data so that Zaytun remains trustworthy.**

Acceptance criteria:
- Admin endpoints require admin authorization.
- Admin actions are restricted to defined capabilities.
- Important administrative changes are auditable where required.

## Cross-Cutting Story

### US-SYS-001 — Safe failure

**As a user, I want failures to be clear and recoverable so that I do not lose trust in the application.**

Acceptance criteria:
- API validation failures are understandable.
- Loading states are visible.
- Failed operations do not falsely appear successful.
- Important retry/recovery paths are available where appropriate.
