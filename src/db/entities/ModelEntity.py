from db_init import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func


class DBModel(Base):
    __tablename__ = 'models'
    # table_args = {'extend_existing': True}

    id = Column(Integer, primary_key=True, autoincrement=True)
    model_name = Column(String(255), nullable=False)
    cost = Column(Integer, nullable=False)
