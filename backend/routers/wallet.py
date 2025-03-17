from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from pydantic import BaseModel

router = APIRouter()

# Модель для пополнения/вывода
class WalletTransaction(BaseModel):
    user_id: int
    amount: float
    action: str  # deposit / withdraw

@router.post("/wallet")
def manage_wallet(transaction: WalletTransaction, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == transaction.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if transaction.action == "deposit":
        user.balance += transaction.amount
    elif transaction.action == "withdraw":
        if user.balance < transaction.amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")
        user.balance -= transaction.amount
    else:
        raise HTTPException(status_code=400, detail="Invalid action")
    
    db.commit()
    return {"message": "Transaction successful", "new_balance": user.balance}
