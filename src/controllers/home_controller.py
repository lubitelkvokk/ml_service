from datetime import datetime

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from src.db.entities.AccountEntity import Account
from src.db.entities.ActionEntity import DBAction  # Убедитесь, что правильно импортировали DBAction
from src.db.entities.ModelEntity import DBModel
from src.db.session import get_db
from src.services.security_service import get_current_user

router = APIRouter(prefix="/home", tags=["home"])
templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_home_page(request: Request, current_user: str = Depends(get_current_user)):
    return templates.TemplateResponse("home.html", {"request": request})


@router.post("/purchase-model/{model_id}")
async def purchase_model(model_id: int, db: Session = Depends(get_db),
                         current_user: str = Depends(get_current_user)):
    # Получение модели по ID
    model = db.query(DBModel).filter(DBModel.id == model_id).first()
    if not model:
        raise HTTPException(status_code=404, detail="Model not found")

    # Получение аккаунта текущего пользователя
    account = db.query(Account).filter(
        Account.user_id == current_user.id).first()  # Используйте ID текущего пользователя
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    # Проверка достаточности средств
    if account.cash < model.price:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    # Списание средств
    account.cash -= model.price

    # Запись действия
    action = DBAction(account_id=account.id, currency_spent=model.price, created_at=datetime.utcnow())
    db.add(action)

    db.commit()

    return {"message": "Model purchased successfully", "remaining_cash": account.cash}
