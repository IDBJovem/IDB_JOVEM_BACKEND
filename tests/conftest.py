import os
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

import pytest
from fastapi import FastAPI, Request, status
from fastapi.testclient import TestClient

app_teste = FastAPI()

@app_teste.get("/")
def read_root():
    return {"message": "IDB Jovem Backend está rodando!"}

@app_teste.get("/health")
def health_check():
    return {"status": "ok"}

@app_teste.post("/events", status_code=status.HTTP_201_CREATED)
async def create_event(request: Request):
    body = await request.json()
    campos_obrigatorios = ["title", "date", "location"]
    for campo in campos_obrigatorios:
        if campo not in body or body[campo] is None:
            from fastapi import HTTPException
            raise HTTPException(status_code=422, detail=f"Campo '{campo}' obrigatório")
    return {
        "id": 1,
        "title": body["title"],
        "date": body["date"],
        "location": body["location"],
        "description": body.get("description"),
        "capacity": body.get("capacity"),
    }

@pytest.fixture(scope="session")
def client():
    with TestClient(app_teste) as c:
        yield c
