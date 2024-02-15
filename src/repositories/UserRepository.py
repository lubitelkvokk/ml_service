from src.repositories.Repository import Repository
from sqlalchemy import select
from src.models.User import UserDB
from src.api.dependencies.create_db import async_session_maker


class UserRepository(Repository):
    sqlalchemy_model = UserDB

    async def get_by_username(self, username: str):
        async with async_session_maker() as session:
            statement = select(self.sqlalchemy_model).filter_by(username=username)
            result = await session.execute(statement)
            return result.scalar_one_or_none()


user_repository = UserRepository()