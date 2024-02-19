import pandas as pd
from fastapi import FastAPI, Depends, Form, HTTPException, APIRouter, Request
from sqlalchemy.orm import Session
from starlette.templating import Jinja2Templates

from src.db.entities.UserEntity import DBUser
from src.db.session import get_db  # Убедитесь, что путь к функции get_db верный
from src.services.security_service import get_current_user
from src.services.user_service import user_service
from src.services.account_service import account_service
from src.db.repository.users_repository import authenticate_user
import joblib

router = APIRouter(prefix="/main", tags=["main"])
templates = Jinja2Templates(directory="templates")


@router.post("/predict/")
async def make_prediction(
        request: Request,
        db: Session = Depends(get_db),
        age_group: int = Form(...),
        RIDAGEYR: float = Form(...),
        RIAGENDR: int = Form(...),
        PAQ605: int = Form(...),
        BMXBMI: float = Form(...),
        LBXGLU: float = Form(...),
        LBXGLT: float = Form(...),
        LBXIN: float = Form(...),
        current_user: DBUser = Depends(get_current_user)
):

    data = {
        'age_group': [age_group],
        'RIDAGEYR': [RIDAGEYR],
        'RIAGENDR': [RIAGENDR],
        'PAQ605': [PAQ605],
        'BMXBMI': [BMXBMI],
        'LBXGLU': [LBXGLU],
        'LBXGLT': [LBXGLT],
        'LBXIN': [LBXIN]
    }
    df = pd.DataFrame(data)

    # Загрузка модели и получение предсказания
    model = joblib.load('dummy_model.pkl')  # Путь к модели
    predictions = model.predict(df)

    # Списание средств со счёта пользователя
    # Предполагается, что вы можете получить ID пользователя из токена
    user_id = ...  # Извлеките ID пользователя из токена
    account = user_service.get_user_account(user_id, db)  # Нужно реализовать этот метод в user_service
    model_cost = 50  # Стоимость использования модели
    if account.cash < model_cost:
        raise HTTPException(status_code=400, detail="Not enough funds")
    account_service.change_balance(account.id, -model_cost, db)
    account_service.create_action(account.id, -model_cost, db)  # Регистрация операции списания

    # Возвращение результата предсказания
    return templates.TemplateResponse("home.html", {"request": request, "prediction": predictions[0]})
