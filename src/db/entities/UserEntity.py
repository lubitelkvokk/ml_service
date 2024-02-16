from sqlalchemy.orm import relationship

from db_init import Base
from sqlalchemy import Column, Integer, String, DateTime, func

class DBUser(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)  # Предполагается, что это поле для хранения хэшированного пароля
    login = Column(String(255), nullable=False, unique=True)
    email = Column(String(255), nullable=False, unique=True)  # Добавлено поле email, как было запрошено ранее
    registration_date = Column(DateTime(timezone=True), default=func.now())

    accounts = relationship('Account', back_populates='user')