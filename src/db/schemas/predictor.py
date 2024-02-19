from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class Predictior(BaseModel):
    id: Optional[int] = None
    modelname: str
    file_path: str
    cost: int

class PredictionResponse(BaseModel):
    prediction_id: str
    prediction_model_id: int
    created_at: datetime
    prediction_results: Optional[List[str]]


class PredictionInfo(BaseModel):
    id: Optional[str]
    user_id: int
    model_id: int
    result: Optional[str] = None
    cost: int
    timestamp: datetime
    duration: Optional[int] = None
    is_successful: Optional[bool] = None