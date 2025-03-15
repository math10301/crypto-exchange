from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.user import User
from models.account import Account
from database.init_db import SessionLocal
from pydantic import BaseModel

router = APIRouter()

class ExternalTransaction(BaseModel):
    user_id: int
    amount: float
    currency: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/external/deposit")
def external_deposit(transaction: ExternalTransaction, db: Session = Depends(get_db)):
    user_account = db.query(Account).filter(Account.user_id == transaction.user_id).first()
    if not user_account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    
    if transaction.currency == "fiat":
        user_account.fiat_balance += transaction.amount
    elif transaction.currency == "crypto":
        user_account.crypto_balance += transaction.amount
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid currency")

    db.commit()
    return {"message": "Deposit successful"}

@router.post("/external/withdraw")
def external_withdraw(transaction: ExternalTransaction, db: Session = Depends(get_db)):
    user_account = db.query(Account).filter(Account.user_id == transaction.user_id).first()
    if not user_account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    
    if transaction.currency == "fiat" and user_account.fiat_balance >= transaction.amount:
        user_account.fiat_balance -= transaction.amount
    elif transaction.currency == "crypto" and user_account.crypto_balance >= transaction.amount:
        user_account.crypto_balance -= transaction.amount
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient funds or invalid currency")

    db.commit()
    return {"message": "Withdrawal successful"}