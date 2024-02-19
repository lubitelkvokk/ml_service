from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from db_init import db

from src.db.entities.ModelEntity import DBModel  # Убедитесь, что импорт указывает на правильный путь


def create_new_model(model_name: str, cost: int, db: Session):
    db_model = DBModel(
        model_name=model_name,
        cost=cost
    )
    try:
        db.add(db_model)
        db.commit()
        db.refresh(db_model)
        return db_model
    except IntegrityError as e:
        db.rollback()
        raise e


