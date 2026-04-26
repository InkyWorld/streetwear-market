## Architecture Pain Points

### 1) Business Logic Coupling Across Layers (High)
- **Smell**: Pricing logic, stock checks, and persistence concerns were mixed inside `OrderService`.
- **Why it hurts**: Hard to test pricing independently and difficult to extend with promotions without touching order workflow code.
- **Recommendation**: Keep pricing rules in `app/domain` and orchestration in dedicated services (`PricingService`, `InventoryService`).

### 2) Inventory Lifecycle Was Implicit (High)
- **Smell**: Stock was decremented directly at order creation with no reservation records.
- **Why it hurts**: No traceability for who reserved stock, when hold expires, or why stock was returned.
- **Recommendation**: Use explicit `inventory_reservations` table and statuses (`held`, `committed`, `released`).

### 3) Limited Explainability of Price Decisions (Medium)
- **Smell**: API only returned final total, without applied rules.
- **Why it hurts**: Hard to debug customer claims and impossible to verify promotion effects from API contract.
- **Recommendation**: Persist and return `pricing_breakdown` with applied rules and discount amounts.

### 4) Workflow Tightness and Side Effects (Medium)
- **Smell**: Status transitions and inventory side effects were disconnected.
- **Why it hurts**: Cancelling an order could leave implicit stock state mismatches.
- **Recommendation**: Tie transition actions to clear policies (`confirm -> commit hold`, `cancel -> release hold`).

## Prioritized Improvements

1. **High**: Introduce transaction-bound domain events for order lifecycle transitions.
2. **Medium**: Add repository query interfaces for reporting (promotion efficiency, reservation leakage).
3. **Low**: Normalize promotion strategy into extensible classes for new promo types.
