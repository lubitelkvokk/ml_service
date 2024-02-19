from datetime import datetime

import joblib
import pandas as pd
from fastapi import APIRouter, Depends, Request, HTTPException, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.db.entities.ModelEntity import DBModel
from src.db.entities.UserEntity import DBUser
from src.db.repository import action_repository
from src.db.session import get_db
from src.services.account_service import account_service
from src.services.security_service import get_current_user

router = APIRouter(prefix="/home", tags=["home"])
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_home_page(request: Request, current_user: str = Depends(get_current_user)):
    return templates.TemplateResponse("home.html", {"request": request})


@router.post("/")
async def predict(request: Request, db: Session = Depends(get_db), login: DBUser = Depends(get_current_user),
                  model_id: int = Form(...), age_group: int = Form(...), RIDAGEYR: float = Form(...),
                  RIAGENDR: int = Form(...), PAQ605: int = Form(...), BMXBMI: float = Form(...),
                  LBXGLU: float = Form(...), LBXGLT: float = Form(...), LBXIN: float = Form(...)):
    model = db.query(DBModel).filter(DBModel.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")

    account = account_service.get_account_by_login(login, db)
    if account.cash < model.cost:
        raise HTTPException(status_code=400, detail="Not enough funds")

    # Списание средств и запись действия
    account_service.change_balance(account.id, -model.cost, db)
    action_repository.create_action(account.id, -model.cost, db)

    # Загрузка модели и предсказание
    if (model_id == 1):
        loaded_model = joblib.load("dummy_model.pkl")

    # Предположим, что модели сохранены с именем <id>_model.pkl
    data = pd.DataFrame([[age_group, RIDAGEYR, RIAGENDR, PAQ605, BMXBMI, LBXGLU, LBXGLT, LBXIN]],
                        columns=['age_group', 'RIDAGEYR', 'RIAGENDR', 'PAQ605', 'BMXBMI', 'LBXGLU', 'LBXGLT', 'LBXIN'])
    prediction = loaded_model.predict(data)[0]

    return templates.TemplateResponse("home.html", {"request": request, "prediction": prediction})
