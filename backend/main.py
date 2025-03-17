from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from sqlalchemy.orm import Session
from database import get_db
from routers.auth import router as auth_router
from routers.trade import router as trade_router
from routers.wallet import router as wallet_router
from routers.admin import router as admin_router
from routers.dashboard import router as dashboard_router

# Настройки пути к шаблонам
BASE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Инициализация приложения
app = FastAPI()

# Монтирование статики
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Подключение роутов
app.include_router(auth_router, prefix="/auth")
app.include_router(trade_router, prefix="/trade")
app.include_router(wallet_router, prefix="/wallet")
app.include_router(admin_router, prefix="/admin")
app.include_router(dashboard_router, prefix="/dashboard")

# Маршрут для главной страницы
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request, db: Session = Depends(get_db)):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Crypto Exchange"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
