from pydantic import BaseModel
from fastapi import FastAPI, status
from starlette.middleware.sessions import SessionMiddleware
from src.agenda.router import router as agenda_router
from src.galeria.router import router as galeria_router
from src.auth.router import router as auth_router
from src.config import configuracoes

from src.admin.routers import router as admin_router
from src.atividade.routers import router as atividade_router
from src.banda_palestrante.routers import router as banda_palestrante_router
from src.eventos.routers import router as eventos_router
from src.voluntario.routers import router as voluntario_router

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=configuracoes.SECRET_KEY)

app.include_router(auth_router)
app.include_router(agenda_router)
app.include_router(galeria_router)

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
