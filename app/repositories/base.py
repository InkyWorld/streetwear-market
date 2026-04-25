"""Base repository with common CRUD operations."""

from typing import Generic, Protocol, Sequence, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class HasId(Protocol):
    id: int


ModelT = TypeVar("ModelT", bound=HasId)


class BaseRepository(Generic[ModelT]):
    """Base repository with common CRUD operations."""

    def __init__(self, session: AsyncSession, model: type[ModelT]):
        self.session = session
        self.model = model

    async def get_by_id(self, id: int) -> ModelT | None:
        """Get item by id."""
        stmt = select(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> Sequence[ModelT]:
        """Get all items with pagination."""
        stmt = select(self.model).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create(self, **kwargs: object) -> ModelT:
        """Create a new item."""
        instance = self.model(**kwargs)
        self.session.add(instance)
        await self.session.flush()
        return instance

    async def update(self, id: int, **kwargs: object) -> ModelT | None:
        """Update an existing item."""
        instance = await self.get_by_id(id)
        if not instance:
            return None
        for key, value in kwargs.items():
            if value is not None:
                setattr(instance, key, value)
        await self.session.flush()
        return instance

    async def delete(self, id: int) -> bool:
        """Delete an item by id."""
        instance = await self.get_by_id(id)
        if not instance:
            return False
        await self.session.delete(instance)
        await self.session.flush()
        return True
