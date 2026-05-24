# Aqui que fica as rotas HTTP (Endpoints) usando FastAPI.
# Arquivo usado para comunicação entre o front-end e o back-end.
# Arquivo é meramente ilustrativo e deve ser ajustado de acordo com o nosso projeto.

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.database import obter_banco
from src.eventos.repository import RepositorioEvento
from src.eventos.model import Evento
from src.eventos.schema import RespostaEvento, SolicitacaoEvento
from src.security import verificar_roles

router = APIRouter(
    prefix="/eventos",
    tags=["eventos"],
    responses={404: {"description": "Not found"}},
)

@router.post("/",
    response_model=RespostaEvento,
    status_code=status.HTTP_201_CREATED
)

def criar_evento(
    request: SolicitacaoEvento,
    db: Session = Depends(obter_banco),
    usuario_logado: dict = Depends(verificar_roles(["admin", "superadmin"])),
):

    eventos = RepositorioEvento.save(db, Evento(**request.model_dump()))

    return eventos

get_session = obter_banco
