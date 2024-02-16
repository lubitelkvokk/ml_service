# db/repository/users.py
from sqlalchemy.orm import Session
from src.db.entities.UserEntity import \
    DBUser  # Предполагается, что вы определили модель пользователя DBUser в db/models/user_model.py
from src.db.schemas.users import UserCreate
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def create_new_user(user: UserCreate, db: Session):
    db_user = DBUser(
        login=user.login,
        username=user.username,
        email=user.email,
        password_hash=get_password_hash(user.password)
        # Убедитесь, что у вас есть поле для хэшированного пароля в модели DBUser
    )
    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except IntegrityError as e:
        db.rollback()
        raise e


def authenticate_user(login: str, password: str, db: Session):
    user = db.query(DBUser).filter(DBUser.login == login).first()
    if not user:
        return False
    if not pwd_context.verify(password, user.password_hash):
        return False
    return user
