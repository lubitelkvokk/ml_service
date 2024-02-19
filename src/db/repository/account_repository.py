from sqlalchemy.orm import Session

from src.db.entities.AccountEntity import Account
from src.db.entities.UserEntity import DBUser
from src.db.schemas.users import UserCreate
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext


def create_new_account(user_id: int, db: Session):
    db_account = Account(
        user_id=user_id,
        cash=100
    )
    try:
        db.add(db_account)
        db.commit()
        db.refresh(db_account)
        return db_account
    except IntegrityError as e:
        db.rollback()
        raise e


def get_account_balance(account_id: int, db: Session) -> int:
    account = db.query(Account).filter(Account.account_id == account_id).first()
    if account:
        return account.cash
    else:
        raise Exception("Account not found")


def update_account_balance(account_id: int, currency_spent: int, db: Session) -> Account:
    account = db.query(Account).filter(Account.id == account_id).first()
    if account:
        if account.cash - currency_spent < 0:
            raise Exception("Not enough money")
        account.cash -= currency_spent  # change может быть положительным (увеличение) или отрицательным (уменьшение)
        db.commit()
        return account
    else:
        raise Exception("Account not found")


def get_account_by_user_id(user_id: int, db: Session) -> Account:
    account = db.query(Account).filter(Account.user_id == user_id).first()
    if not account:
        raise Exception("Account not found")
    return account

def get_account_by_login(login: str, db: Session):
    # Поиск пользователя по логину
    user = db.query(DBUser).filter(DBUser.login == login).first()
    if not user:
        raise Exception("User not found")

    # Получение аккаунта пользователя
    account = db.query(Account).filter(Account.user_id == user.id).first()
    if not account:
        raise Exception("Account not found")

    return account