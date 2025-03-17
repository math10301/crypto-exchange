from sqlalchemy import Column, Integer, String, Float
from database import Base

class Coin(Base):
    __tablename__ = "coins"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    market_cap = Column(Float, default=0)
    price = Column(Float, default=0)
