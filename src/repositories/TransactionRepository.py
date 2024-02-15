from src.repositories.Repository import Repository
from src.models.Transaction import Transaction
from sqlalchemy import select, func
from src.api.dependencies.create_db import async_session_maker


class TransactionRepository(Repository):
    sqlalchemy_model = Transaction

    async def get_data_by_data(self):
        async with async_session_maker() as session:
            statement = select(
                func.date(self.sqlalchemy_model.timestamp),
                func.sum(self.sqlalchemy_model.credits)
            ).group_by(func.date(self.sqlalchemy_model.timestamp))
            result = await session.execute(statement)
            data = result.all()
            return data


transaction_repository = TransactionRepository()