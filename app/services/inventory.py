"""Inventory hold/release service."""

from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.policies import InventoryHoldPolicy
from app.repositories import InventoryReservationRepository, ProductRepository


class InventoryService:
    """Service for inventory hold/release operations."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self.reservation_repo = InventoryReservationRepository(session)
        self.product_repo = ProductRepository(session)

    async def hold_items(
        self, order_id: int | None, items: list[dict[str, int | float]]
    ) -> list[int]:
        reservation_ids: list[int] = []
        for item in items:
            product_id = int(item["product_id"])
            quantity = int(item["quantity"])
            product = await self.product_repo.get_by_id(product_id)
            if product is None or product.stock_quantity is None:
                continue

            product.stock_quantity = max(product.stock_quantity - quantity, 0)
            if product.stock_quantity == 0:
                product.in_stock = False

            reservation = await self.reservation_repo.create(
                order_id=order_id,
                product_id=product_id,
                quantity=quantity,
                status="held",
                reason="order_create",
                expires_at=InventoryHoldPolicy.expires_at(),
            )
            reservation_ids.append(reservation.id)

        return reservation_ids

    async def attach_holds_to_order(self, order_id: int, reservation_ids: list[int]) -> None:
        for reservation_id in reservation_ids:
            reservation = await self.reservation_repo.get_by_id(reservation_id)
            if reservation and reservation.order_id is None and reservation.status == "held":
                reservation.order_id = order_id

    async def release_holds_for_order(self, order_id: int, reason: str) -> int:
        reservations = await self.reservation_repo.get_held_by_order(order_id)
        released = 0
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        for reservation in reservations:
            product = await self.product_repo.get_by_id(reservation.product_id)
            if product and product.stock_quantity is not None:
                product.stock_quantity += reservation.quantity
                product.in_stock = True

            reservation.status = "released"
            reservation.reason = reason
            reservation.released_at = now
            released += 1
        return released

    async def commit_holds_for_order(self, order_id: int) -> int:
        reservations = await self.reservation_repo.get_held_by_order(order_id)
        committed = 0
        for reservation in reservations:
            reservation.status = "committed"
            reservation.reason = "order_confirmed"
            committed += 1
        return committed

    async def release_expired_holds(self) -> int:
        reservations = await self.reservation_repo.get_expired_holds()
        released = 0
        now = datetime.now(timezone.utc).replace(tzinfo=None)
        for reservation in reservations:
            product = await self.product_repo.get_by_id(reservation.product_id)
            if product and product.stock_quantity is not None:
                product.stock_quantity += reservation.quantity
                product.in_stock = True

            reservation.status = "released"
            reservation.reason = "hold_expired"
            reservation.released_at = now
            released += 1

        if released > 0:
            await self.session.commit()
        return released
