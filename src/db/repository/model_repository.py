from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.db.session import get_db

from src.db.entities import ModelEntity  # Убедитесь, что импорт указывает на правильный путь


def create_new_model(model_name: str, cost: int, db: Session):
    db_model = ModelEntity(
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


# Предполагаем, что db - это сессия SQLAlchemy, которую вы получили где-то в вашем приложении
# Пример вызова функции с созданием новой модели

create_new_model(model_name="dummy", cost=15, db=get_db())
