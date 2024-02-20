from src.db.entities.AccountEntity import Account
from src.db.entities.UserEntity import DBUser
from src.db.repository.account_repository import create_new_account, get_account_by_user_id, get_account_by_login
from sqlalchemy.orm import Session
from src.db.repository.account_repository import get_account_balance, update_account_balance
from src.db.repository.action_repository import create_action


class AccountService:
    def create_new_account_by_user(self, user: DBUser, db: Session):
        return create_new_account(user.id, db)

    def get_balance(self, account_id: int, db: Session) -> int:
        return get_account_balance(account_id, db)

    def change_balance(self, account_id: int, currency_spent: int, db: Session):
        update_account_balance(account_id, currency_spent, db)
        create_action(account_id, currency_spent, db)

    def get_account_by_user_id(self, user_id: int, db: Session) -> Account:
        return get_account_by_user_id(user_id, db)

    def get_account_by_login(self, login: str, db: Session) -> Account:
        return get_account_by_login(login, db)


account_service = AccountService()
