from fastapi import FastAPI
from app.util.database import init_db
from app.controller.locador import router as locadores_router

app = FastAPI(title="APP using FastAPI + SQLModel with MVC pattern")

init_db()

app.include_router(locadores_router)

@app.get("/")
def health():
    return {"status": "ok"}
