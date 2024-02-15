from db_init import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func, ForeignKey, Float


class DBPrediction(Base):
    __tablename__ = "prediction"
    # table_args = {'extend_existing': True}

    prediction_id = Column(Integer, primary_key=True, autoincrement=True)
    action_id = Column(Integer, ForeignKey("actions.action_id"))
    model_id = Column(Integer, ForeignKey("models.model_id"))
    gender = Column(Boolean, nullable=False, default=True)
    labour_activity = Column(Boolean, nullable=False, default=True)
    bmi = Column(Float, nullable=False)
    diagnose_diabetes = Column(Integer, nullable=False, default=3)
    glucose_level = Column(Float, nullable=False)
    glucose_level2 = Column(Float, nullable=False)
    insulin = Column(Float, nullable=False)
    answer = Column(String(255), nullable=False)
