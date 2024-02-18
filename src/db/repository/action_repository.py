from sqlalchemy.orm import Session

from src.db.entities.ActionEntity import DBAction  # Убедитесь, что путь к модели верный


def create_action(account_id: int, action_type: str, currency_spent: int, db: Session) -> DBAction:
    action = DBAction(account_id=account_id, currency_spent=currency_spent)
    db.add(action)
    db.commit()
    db.refresh(action)
    return action
