from fastapi import APIRouter, status, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.database import obter_banco
from src.evento.repository import RepositorioEvento
from src.evento.service import ServicoEvento
from src.evento.schema import RespostaEvento, SolicitacaoEvento
from src.calendario.service import ServicoCalendario
from src.drive.schema import RespostaDrive
from src.drive.service import ServicoDrive
from src.mapa.service import ServicoMapa


router = APIRouter(prefix="/evento", tags=["evento"])
security = HTTPBearer()


def get_servico(
    db: Session = Depends(obter_banco),
    credenciais: HTTPAuthorizationCredentials = Depends(security)
):
    if not credenciais:
        raise HTTPException(status_code=401, detail="Token de acesso ausente.")

    token = credenciais.credentials

    repositorio = RepositorioEvento(db)
    calendario = ServicoCalendario(token_acesso=token)
    mapa = ServicoMapa()
    return ServicoEvento(repositorio, calendario, mapa)


@router.post("/", response_model=RespostaEvento, status_code=status.HTTP_201_CREATED)
def criar_evento(
    solicitar: SolicitacaoEvento,
    servico: ServicoEvento = Depends(get_servico)
):
    try:
        return servico.criar_evento(solicitar)

    except ValueError as erro:
        raise HTTPException(status_code=400, detail= str(erro)) from erro


@router.get("/", response_model=list[RespostaEvento])
def buscar_todos_evento(servico: ServicoEvento = Depends(get_servico)):
    return servico.listar_evento()


@router.get("/{evento_id}", response_model=RespostaEvento)
def buscar_evento_id(evento_id: int, servico: ServicoEvento = Depends(get_servico)):

    try:
        return servico.buscar_evento(evento_id)

    except ValueError as erro:
        raise HTTPException(status_code=404, detail= str(erro)) from erro


@router.put("/{evento_id}", response_model=RespostaEvento)
def atualizar_evento(
    evento_id: int,
    solicitar: SolicitacaoEvento,
    servico: ServicoEvento = Depends(get_servico)
):
    try:
        return servico.atualizar_evento(evento_id, solicitar)

    except ValueError as erro:
        raise HTTPException(status_code=400, detail = str(erro)) from erro


@router.delete("/{evento_id}", status_code=204)
def deletar_evento(evento_id: int, servico: ServicoEvento = Depends(get_servico)):
    try:
        servico.deletar_evento(evento_id)

    except ValueError as erro:
        raise HTTPException(status_code=404, detail = str(erro)) from erro

@router.get("/{evento_id}/galeria", response_model=list[RespostaDrive])
def listar_galeria_evento(
    evento_id: int,
    credenciais: HTTPAuthorizationCredentials = Depends(security),
    servico: ServicoEvento = Depends(get_servico)
):
    try:
        if not credenciais:
            raise HTTPException(
                status_code=401,
                detail="Token de acesso ausente."
            )

        token = credenciais.credentials

        evento = servico.buscar_evento(evento_id)

        if not evento.link_galeria:
            return []

        drive = ServicoDrive(token_acesso=token)

        return drive.listar_fotos(evento.link_galeria)

    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro)) from erro

    except RuntimeError as erro:
        raise HTTPException(status_code=502, detail=str(erro)) from erro
