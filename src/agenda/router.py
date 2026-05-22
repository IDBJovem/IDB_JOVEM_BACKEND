from fastapi import APIRouter, Depends, Header, HTTPException, Query, status

from src.agenda.repository import RepositorioAgenda
from src.agenda.schema import EventoResponse, RespostaEventoAgenda, SolicitacaoEventoAgenda
from src.security import verificar_roles

# Criamos o roteador definindo o prefixo da URL e a "tag" para a documentação
router = APIRouter(prefix="/agenda", tags=["Agenda do Google"])

@router.get("/eventos", response_model=list[EventoResponse])
def listar_eventos(
    google_autorizacao: str = Header(None, alias="X-Google-Authorization"),
    meses: int = Query(6, ge=1, le=24),
):
    """
    Rota para listar os eventos da agenda em um intervalo de meses.
    """
    # 1. Instanciamos o repositório (passando o token do cabeçalho se existir)
    token = google_autorizacao
    repositorio = RepositorioAgenda(token_acesso=token)

    # 2. Chamamos o método que busca os dados
    eventos = repositorio.listar_eventos(meses)

    # 3. Retornamos a lista (o FastAPI valida tudo usando o response_model)
    return eventos


@router.post("/eventos", response_model=RespostaEventoAgenda, status_code=status.HTTP_201_CREATED)
def criar_evento(
    solicitacao: SolicitacaoEventoAgenda,
    usuario_logado: dict = Depends(verificar_roles(["admin", "superadmin"])),
    google_autorizacao: str = Header(None, alias="X-Google-Authorization"),
):
    """
    Rota para criar um evento no Google Calendar.
    """
    token = google_autorizacao
    if not token:
        raise HTTPException(status_code=401, detail="Token de acesso ausente")

    repositorio = RepositorioAgenda(token_acesso=token)
    try:
        return repositorio.criar_evento(solicitacao)
    except RuntimeError as erro:
        raise HTTPException(status_code=502, detail=str(erro)) from erro


@router.delete("/eventos/{id_google}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_evento(
    id_google: str,
    usuario_logado: dict = Depends(verificar_roles(["admin", "superadmin"])),
    google_autorizacao: str = Header(None, alias="X-Google-Authorization"),
):
    """
    Rota para excluir um evento no Google Calendar.
    """
    token = google_autorizacao
    if not token:
        raise HTTPException(status_code=401, detail="Token de acesso ausente")

    repositorio = RepositorioAgenda(token_acesso=token)
    try:
        repositorio.excluir_evento(id_google)
    except RuntimeError as erro:
        raise HTTPException(status_code=502, detail=str(erro)) from erro
