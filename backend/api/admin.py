from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.user import User
from database.init_db import SessionLocal
from pydantic import BaseModel

router = APIRouter()

class UpdateBalanceRequest(BaseModel):
    user_id: int
    fiat_balance: float
    crypto_balance: float

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/admin/update_balance")
def update_user_balance(update_request: UpdateBalanceRequest, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == update_request.user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db_user.fiat_balance = update_request.fiat_balance
    db_user.crypto_balance = update_request.crypto_balance
    db.commit()
    return {"message": "User balance updated"}

@router.delete("/admin/delete_user/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    db.delete(db_user)
    db.commit()
    return {"message": "User deleted"}