from db_init import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func


class DBModel(Base):
    __tablename__ = 'models'
    # table_args = {'extend_existing': True}

    model_id = Column(Integer, primary_key=True, autoincrement=True)
    modelname = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    price = Column(Integer, nullable=False)
