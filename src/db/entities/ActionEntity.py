from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from db_init import Base


class DBAction(Base):
    __tablename__ = 'actions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    account_id = Column(Integer, ForeignKey('accounts.id'))
    currency_spent = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    account = relationship('Account', back_populates='actions')
