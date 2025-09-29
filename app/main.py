from fastapi import FastAPI

app = FastAPI(title="APP using FastAPI + SQLModel with MVC pattern")

@app.get("/")
def health():
    return {"status": "ok"}
