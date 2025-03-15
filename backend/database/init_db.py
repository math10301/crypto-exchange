from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.user import Base as UserBase
from models.transaction import Base as TransactionBase
from models.account import Base as AccountBase

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    UserBase.metadata.create_all(bind=engine)
    TransactionBase.metadata.create_all(bind=engine)
    AccountBase.metadata.create_all(bind=engine)