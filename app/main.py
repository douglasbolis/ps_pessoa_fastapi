from fastapi import FastAPI
from util.database import init_db
from controller.endereco import router as enderecos_router
from controller.pessoa import router as pessoas_router

title = "APPeople -> An APP using FastAPI + SQLModel with MVC pattern"
app = FastAPI(title=title)

init_db()

app.include_router(enderecos_router)
app.include_router(pessoas_router)

@app.get("/")
def health():
    return {"status": "ok", "message": title}
# fim_def
