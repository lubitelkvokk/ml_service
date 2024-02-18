from sqlalchemy.orm import relationship

from db_init import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    cash = Column(Integer, nullable=False)

    user = relationship('DBUser', back_populates='accounts')
    actions = relationship('DBAction', back_populates='account')

