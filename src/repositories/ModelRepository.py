from src.repositories.Repository import Repository
from sqlalchemy import select
from src.models.MlModels import MLModel
from db_init import async_session_maker


class ModelRepository(Repository):
    sqlalchemy_model = MLModel

    async def get_by_modelname(self, modelname: str):
        async with async_session_maker() as session:
            statement = select(self.sqlalchemy_model).where(self.sqlalchemy_model.modelname == modelname)
            result = await session.execute(statement)
            return result.scalar_one_or_none()


model_repository = ModelRepository()