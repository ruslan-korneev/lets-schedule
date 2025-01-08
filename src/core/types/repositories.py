from collections.abc import Sequence
from typing import Generic, TypeVar, cast

from sqlalchemy import func, inspect, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db import SAModel

_MT = TypeVar("_MT", bound=SAModel)


class BaseRepository(Generic[_MT]):
    _model: type[_MT]
    _session: AsyncSession

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_by_id(self, id_: int) -> _MT:
        """
        Get model instance by id
        """
        query = select(self._model).where(self._model.id == id_)
        result = await self._session.execute(query)
        return result.scalar_one()

    async def get_all(self) -> Sequence[_MT]:
        """
        Get all model instances
        """
        query = select(self._model)
        result = await self._session.execute(query)
        return result.scalars().all()

    @staticmethod
    def is_modified(data: _MT) -> bool:
        """
        Check if model instance has been modified
        """
        inspr = inspect(data)
        return inspr.modified or not inspr.has_identity

    async def save(self, data: _MT) -> _MT:
        """
        Save a new model instance or update if exists
        """
        if not self.is_modified(data):
            return data

        self._session.add(data)
        await self._session.flush()
        await self._session.refresh(data)

        return data

    async def save_many(self, data: list[_MT]) -> list[_MT]:
        self._session.add_all(data)
        await self._session.flush()
        return data

    async def delete(self, instance: _MT) -> None:
        """
        Delete a model instance from database
        """
        await self._session.delete(instance)
        await self._session.flush()

    async def count(self) -> int:
        query = select(func.count(self._model.id))
        result = await self._session.execute(query)
        return cast(int, result.scalar())
