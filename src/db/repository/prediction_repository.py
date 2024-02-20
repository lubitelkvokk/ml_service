from datetime import datetime

from sqlalchemy.orm import Session
from src.db.entities.PredictionEntity import DBPrediction

def create_prediction(
        db: Session,
        action_id: int,
        user_id: int,
        model_id: int,
        gender: bool,
        body_mass_index: float,
        physical_activity: bool,
        insulin_level: float,
        diabetes: int,
        glucose_level: float,
        glucose_tolerance_test: float,
        prediction_result: str
):
    new_prediction = DBPrediction(
        action_id=action_id,
        user_id=user_id,
        model_id=model_id,
        gender=gender,
        body_mass_index=body_mass_index,
        physical_activity=physical_activity,
        insulin_level=insulin_level,
        diabetes=diabetes,
        glucose_level=glucose_level,
        glucose_tolerance_test=glucose_tolerance_test,
        prediction_result=prediction_result,
        created_at=datetime.utcnow()
    )
    db.add(new_prediction)
    db.commit()
    db.refresh(new_prediction)
    return new_prediction
