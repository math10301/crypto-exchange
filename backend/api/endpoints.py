from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.user import User
from models.account import Account
from models.transaction import Transaction
from database.init_db import SessionLocal
from auth.auth import verify_password, get_password_hash, create_access_token
from pydantic import BaseModel

router = APIRouter()

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class TransferRequest(BaseModel):
    from_account_id: int
    to_account_id: int
    amount: float

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    # Создание счета для нового пользователя
    db_account = Account(user_id=db_user.id)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_user

@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.username == user.username).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    access_token = create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/account/{user_id}")
def get_account_balance(user_id: int, db: Session = Depends(get_db)):
    db_account = db.query(Account).filter(Account.user_id == user_id).first()
    if not db_account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    return db_account

@router.post("/transfer")
def transfer_funds(transfer: TransferRequest, db: Session = Depends(get_db)):
    from_account = db.query(Account).filter(Account.id == transfer.from_account_id).first()
    to_account = db.query(Account).filter(Account.id == transfer.to_account_id).first()
    if not from_account or not to_account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Account not found")
    if from_account.fiat_balance < transfer.amount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient funds")
    from_account.fiat_balance -= transfer.amount
    to_account.fiat_balance += transfer.amount
    db.commit()
    return {"message": "Transfer successful"}
