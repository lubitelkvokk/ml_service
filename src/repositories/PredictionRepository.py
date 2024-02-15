from src.repositories.Repository import Repository
from src.models.Predictions import Prediction
from src.api.dependencies.create_db import async_session_maker
from sqlalchemy import select, update
from typing import Dict, Any, Type


class PredictionRepository(Repository):
    sqlalchemy_model = Prediction

    async def get_by_user_id(self, user_id: str):
        async with async_session_maker() as session:
            statement = select(self.sqlalchemy_model).filter_by(user_id=user_id)
            result = await session.execute(statement)
            return [row.to_dict() for row in result.scalars()]

    async def update(self, timestamp, update_data: Dict[str, Any]):
        async with async_session_maker() as session:
            statement = (
                update(self.sqlalchemy_model)
                .filter_by(timestamp=timestamp)
                .values(**update_data)
            )
            await session.execute(statement)
            await session.commit()

prediction_repository = PredictionRepository()