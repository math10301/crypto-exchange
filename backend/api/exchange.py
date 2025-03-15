from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.user import User
from models.account import Account
from models.transaction import Transaction
from database.init_db import SessionLocal
from pydantic import BaseModel

router = APIRouter()

class ExchangeRequest(BaseModel):
    user_id: int
    from_currency: str
    to_currency: str
    amount: float

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/exchange")
def exchange_currency(exchange_request: ExchangeRequest, db: Session = Depends(get_db)):
    user_account = db.query(Account).filter(Account.user_id == exchange_request.user_id).first()
    if not user_account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    
    # Простая логика обмена криптовалют (может быть дополнена более сложной логикой)
    if exchange_request.from_currency == "fiat" and user_account.fiat_balance >= exchange_request.amount:
        user_account.fiat_balance -= exchange_request.amount
        user_account.crypto_balance += exchange_request.amount * 0.95  # Учитываем комиссию 5%
    elif exchange_request.from_currency == "crypto" and user_account.crypto_balance >= exchange_request.amount:
        user_account.crypto_balance -= exchange_request.amount
        user_account.fiat_balance += exchange_request.amount * 0.95  # Учитываем комиссию 5%
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient funds or invalid currency")

    db.commit()
    return {"message": "Exchange successful"}