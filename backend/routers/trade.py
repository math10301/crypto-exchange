from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.user import User
from models.transaction import Transaction
from pydantic import BaseModel

router = APIRouter()

# Модель для сделки
class TradeRequest(BaseModel):
    user_id: int
    currency: str
    amount: float
    price: float
    type: str  # buy / sell

@router.post("/trade")
def trade_crypto(trade: TradeRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == trade.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    total_cost = trade.amount * trade.price
    
    if trade.type == "buy":
        if user.balance < total_cost:
            raise HTTPException(status_code=400, detail="Insufficient balance")
        user.balance -= total_cost
    elif trade.type == "sell":
        user.balance += total_cost
    else:
        raise HTTPException(status_code=400, detail="Invalid trade type")
    
    # Создаём запись о сделке
    transaction = Transaction(
        user_id=user.id,
        currency=trade.currency,
        amount=trade.amount,
        price=trade.price,
        type=trade.type
    )
    
    db.add(transaction)
    db.commit()
    db.refresh(transaction)
    return {"message": "Trade successful", "transaction": transaction.id}
