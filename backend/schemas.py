from pydantic import BaseModel
from typing import Optional

# Обновление данных пользователя (например, баланс)
class UserUpdate(BaseModel):
    balance: float

# Создание новой криптовалюты
class CoinCreate(BaseModel):
    name: str
    market_cap: float
    price: float

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    balance: Optional[float] = 0.0

    class Config:
        from_attributes = True


print("SCHEMAS LOADED: UserResponse exists")

