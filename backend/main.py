from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path
from api.endpoints import router as api_router
from api.exchange import router as exchange_router
from api.charts import router as charts_router
from api.admin import router as admin_router
from api.integration import router as integration_router

app = FastAPI()

# Гарантируем, что путь к шаблонам правильный
BASE_DIR = Path(__file__).parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app.include_router(api_router, prefix="/api")
app.include_router(exchange_router, prefix="/api")
app.include_router(charts_router, prefix="/api")
app.include_router(admin_router, prefix="/api")
app.include_router(integration_router, prefix="/api")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request, "title": "Crypto Exchange"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
