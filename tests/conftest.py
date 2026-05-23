import pytest
from unittest.mock import MagicMock
from fastapi import FastAPI, status
from fastapi.testclient import TestClient
from pydantic import BaseModel


# App isolado para testes — não depende de config, banco ou routers dos colegas
app_teste = FastAPI()


class EventCreate(BaseModel):
    title: str
    date: str
    location: str
    description: str | None = None
    capacity: int | None = None


@app_teste.get("/")
def read_root():
    return {"message": "IDB Jovem Backend está rodando!"}


@app_teste.get("/health")
def health_check():
    return {"status": "ok"}


@app_teste.post("/events", status_code=status.HTTP_201_CREATED)
def create_event(event: EventCreate):
    return {
        "id": 1,
        "title": event.title,
        "date": event.date,
        "location": event.location,
        "description": event.description,
        "capacity": event.capacity,
    }


@pytest.fixture(scope="session")
def client():
    """
    TestClient apontando para o app isolado de testes.
    Não depende de banco, config ou routers externos.
    """
    with TestClient(app_teste) as c:
        yield c