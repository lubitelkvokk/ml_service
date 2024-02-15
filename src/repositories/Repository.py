from sqlalchemy import insert, select, update, delete
from typing import Dict, Any, Type
from src.api.dependencies.create_db import async_session_maker, Base
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException

class Repository:
    sqlalchemy_model: Type[Base] = None

    async def add(self, data: Dict[str, Any]) -> int:
        try:
            async with async_session_maker() as session:
                statement = insert(self.sqlalchemy_model).values(**data).returning(self.sqlalchemy_model.id)
                result = await session.execute(statement)
                await session.commit()
                return result.scalar_one()
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Модель с таким именем уже существует")

    async def get_by_id(self, id: int):
        async with async_session_maker() as session:
            statement = select(self.sqlalchemy_model).where(self.sqlalchemy_model.id == id)
            result = await session.execute(statement)
            return result.scalar_one_or_none()

    async def list_all(self):
        async with async_session_maker() as session:
            statement = select(self.sqlalchemy_model)
            result = await session.execute(statement)
            return [row.to_dict() for row in result.scalars()]

    async def update(self, id, update_data: Dict[str, Any]):
        async with async_session_maker() as session:
            statement = (
                update(self.sqlalchemy_model)
                .filter_by(id=id)
                .values(**update_data)
            )

            await session.execute(statement)
            await session.commit()

    async def delete(self, id: int):
        async with async_session_maker() as session:
            statement = delete(self.model).where(self.model.id == id)
            await session.execute(statement)
            await session.commit()
