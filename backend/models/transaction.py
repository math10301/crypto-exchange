from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

# Модель транзакции
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    currency = Column(String, nullable=False)  # Название валюты
    amount = Column(Float, nullable=False)
    price = Column(Float, nullable=False)  # Цена за единицу
    type = Column(String, nullable=False)  # buy / sell
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="transactions")

# Добавляем связь в модель User
from models.user import User
User.transactions = relationship("Transaction", back_populates="user")
