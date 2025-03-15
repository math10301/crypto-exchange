import matplotlib.pyplot as plt
import io
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from database.init_db import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/chart/{currency}")
def get_currency_chart(currency: str, db: Session = Depends(get_db)):
    # Пример данных для графика (можно заменить на реальные данные из БД)
    dates = ["2025-03-01", "2025-03-02", "2025-03-03", "2025-03-04", "2025-03-05"]
    prices = [100, 110, 105, 115, 120]

    plt.figure()
    plt.plot(dates, prices, label=currency)
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(f'{currency} Price Over Time')
    plt.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")