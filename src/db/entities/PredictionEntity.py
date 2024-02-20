from datetime import datetime

from sqlalchemy.orm import relationship

from db_init import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey, Float


class DBPrediction(Base):
    __tablename__ = 'predictions'

    id = Column(Integer, primary_key=True, autoincrement=True)
    action_id = Column(Integer, ForeignKey("actions.id"))
    user_id = Column(Integer, ForeignKey('users.id'))
    model_id = Column(Integer, ForeignKey('models.id'))
    created_at = Column(DateTime, default=datetime.utcnow)

    gender = Column(Boolean, nullable=False, default=True)
    body_mass_index = Column(Float, nullable=False)
    physical_activity = Column(Boolean, nullable=False, default=True)
    insulin_level = Column(Float, nullable=False)
    diabetes = Column(Integer, nullable=True)
    glucose_level = Column(Float, nullable=False)
    glucose_tolerance_test = Column(Float, nullable=False)
    prediction_result = Column(String(255), nullable=False)

    # action = relationship('DBAction', back_populates='predictions')
    # user = relationship('DBUser', back_populates='predictions')
    # model = relationship('DBModel', back_populates='predictions')
