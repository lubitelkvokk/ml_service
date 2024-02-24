from sqlalchemy.orm import Session

from src.db.schemas.users import UserCreate
from src.db.repository.users_repository import add_new_user
from src.services.account_service import account_service

from starlette.concurrency import run_in_threadpool


class UserService:
    async def create_new_user(self, user: UserCreate, db: Session):
        db_user = await run_in_threadpool(add_new_user, user, db)
        db_account = await run_in_threadpool(account_service.create_new_account_by_user, db_user, db)


user_service = UserService()
