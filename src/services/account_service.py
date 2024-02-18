from src.db.entities.AccountEntity import Account
from src.db.entities.UserEntity import DBUser
from src.db.repository.account_repository import create_new_account
from sqlalchemy.orm import Session
from src.db.repository.account_repository import get_account_balance, update_account_balance
from src.db.repository.action_repository import create_action


class AccountService:
    def create_new_account_by_user(self, user: DBUser, db: Session):
        return create_new_account(user.id, db)

    def get_balance(self, account_id: int, db: Session) -> int:
        return get_account_balance(account_id, db)

    def change_balance(self, account_id: int, change: int, db: Session):
        update_account_balance(account_id, change, db)
        action_type = "Deposit" if change > 0 else "Withdrawal"
        create_action(account_id, action_type, change, db)


account_service = AccountService()
