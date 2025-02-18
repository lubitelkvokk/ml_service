
from sqlalchemy.orm import Session
from src.db.entities.UserEntity import \
    DBUser
from src.db.schemas.users import UserCreate
from sqlalchemy.exc import IntegrityError
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def add_new_user(user: UserCreate, db: Session):
    db_user = DBUser(
        login=user.login,
        username=user.username,
        email=user.email,
        password_hash=get_password_hash(user.password)
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

def get_user_by_login(login: str, db: Session):
    user = db.query(DBUser).filter(DBUser.login == login).first()
    return user