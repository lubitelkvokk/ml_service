from datetime import datetime

import joblib
import pandas as pd
from fastapi import APIRouter, Depends, Request, HTTPException, Form
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.db.entities.ModelEntity import DBModel
from src.db.entities.UserEntity import DBUser
from src.db.repository import action_repository
from src.db.repository.prediction_repository import create_prediction
from src.db.repository.users_repository import get_user_by_login
from src.db.session import get_db
from src.services.account_service import account_service
from src.services.security_service import get_current_user

router = APIRouter(prefix="/home", tags=["home"])
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_home_page(request: Request, login: str = Depends(get_current_user), db: Session = Depends(get_db)):
    account = account_service.get_account_by_login(login, db)
    return templates.TemplateResponse("home.html", {"request": request, "balance": account.cash})


@router.post("/")
async def predict(request: Request, db: Session = Depends(get_db), login: DBUser = Depends(get_current_user),
                  model_id: int = Form(...), age_group: int = Form(...), RIDAGEYR: float = Form(...),
                  RIAGENDR: int = Form(...), PAQ605: int = Form(...), BMXBMI: float = Form(...),
                  LBXGLU: float = Form(...), LBXGLT: float = Form(...), LBXIN: float = Form(...)):
    model = db.query(DBModel).filter(DBModel.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")

    # Проверка и списание средств
    account = account_service.get_account_by_login(login, db)

    if account.cash < model.cost:
        return templates.TemplateResponse("home.html",
                                          {"request": request,
                                           # "prediction": prediction_result,
                                           "balance": "Not enough money"})
        # raise HTTPException(status_code=400, detail="Not enough funds")
    account_service.change_balance(account.id, model.cost, db)

    # Создание записи действия
    action = action_repository.create_action(account_id=account.id, currency_spent=model.cost, db=db)
    if model_id == 1:
        loaded_model = joblib.load("dummy_model.pkl")
    elif model_id == 2:
        # loaded_model = joblib.load("svc_model.pkl")
        loaded_model = joblib.load("rf_model.pkl")
    # else model_id == 3:
    #
    # Предсказание и сохранение результата
      # Предположим, что модели сохранены с именем <id>_model.pkl
    data = pd.DataFrame([[age_group, RIDAGEYR, RIAGENDR, PAQ605, BMXBMI, LBXGLU, LBXGLT, LBXIN]],
                        columns=['age_group', 'RIDAGEYR', 'RIAGENDR', 'PAQ605', 'BMXBMI', 'LBXGLU', 'LBXGLT', 'LBXIN'])
    prediction = loaded_model.predict(data)[0]
    print(prediction)
    prediction_result = "Positive" if prediction == 1 else "Negative"
    create_prediction(
        db=db,
        action_id=action.id,
        user_id=get_user_by_login(login, db).id,
        model_id=model.id,
        gender=RIAGENDR == 1,
        body_mass_index=BMXBMI,
        physical_activity=PAQ605 == 1,
        insulin_level=LBXIN,
        diabetes=prediction,
        glucose_level=LBXGLU,
        glucose_tolerance_test=LBXGLT,
        prediction_result=prediction_result
    )

    return templates.TemplateResponse("home.html",
                                      {"request": request,
                                       "prediction": prediction_result,
                                       "balance": account.cash})
