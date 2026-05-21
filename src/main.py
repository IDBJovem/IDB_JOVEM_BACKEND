from pydantic import BaseModel
from fastapi import FastAPI, status

from src.admin.routers import router as admin_router
from src.atividade.routers import router as atividade_router
from src.banda_palestrante.routers import router as banda_palestrante_router
from src.eventos.routers import router as eventos_router
from src.voluntario.routers import router as voluntario_router

app = FastAPI()

app.include_router(admin_router)
app.include_router(atividade_router)
app.include_router(banda_palestrante_router)
app.include_router(eventos_router)
app.include_router(voluntario_router)


class EventCreate(BaseModel):
    title: str
    date: str
    location: str
    description: str | None = None
    capacity: int | None = None


@app.get("/")
def read_root():
    return {"message": "IDB Jovem Backend está rodando!"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/events", status_code=status.HTTP_201_CREATED)
def create_event(event: EventCreate):
    return {
        "id": 1,
        "title": event.title,
        "date": event.date,
        "location": event.location,
        "description": event.description,
        "capacity": event.capacity,
    }
