from fastapi.responses import HTMLResponse
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.coin import Coin  # Импортируем модель валют
from fastapi.templating import Jinja2Templates
from schemas import UserUpdate, CoinCreate, UserResponse  # Используем Pydantic-модели
from typing import List

router = APIRouter()
templates = Jinja2Templates(directory="templates")

# Админ-панель
@router.get("/", response_class=HTMLResponse)
def admin_panel(request: Request, db: Session = Depends(get_db)):
    users = db.query(User).all()
    coins = db.query(Coin).all()
    return templates.TemplateResponse("admin.html", {"request": request, "users": users, "coins": coins})

# Получение списка пользователей
@router.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()

# Обновление баланса пользователя
@router.put("/users/{user_id}", response_model=UserResponse)
def update_user_balance(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.balance = user_update.balance
    db.commit()
    db.refresh(user)
    return user

# Добавление новой криптовалюты
@router.post("/coins", response_model=CoinCreate)
def create_coin(coin: CoinCreate, db: Session = Depends(get_db)):
    new_coin = Coin(name=coin.name, market_cap=coin.market_cap, price=coin.price)
    db.add(new_coin)
    db.commit()
    db.refresh(new_coin)
    return new_coin
