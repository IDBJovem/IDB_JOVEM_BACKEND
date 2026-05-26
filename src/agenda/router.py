from fastapi import APIRouter, Header, HTTPException, Query, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.agenda.repository import RepositorioAgenda
from src.agenda.schema import EventoResponse, RespostaEventoAgenda, SolicitacaoEventoAgenda

# Criamos o roteador definindo o prefixo da URL e a "tag" para a documentação
router = APIRouter(prefix="/agenda", tags=["Agenda do Google"])

autenticacao_bearer = HTTPBearer(auto_error=False)

@router.get("/evento", response_model=list[EventoResponse])
def listar_evento(
    autorizacao: str = Header(None, alias="Authorization"),
    credenciais: HTTPAuthorizationCredentials = Security(autenticacao_bearer),
    meses: int = Query(6, ge=1, le=24),
):
    """
    Rota para listar os evento da agenda em um intervalo de meses.
    """
    # 1. Instanciamos o repositório (passando o token do cabeçalho se existir)
    token = autorizacao
    if not token and credenciais:
        token = f"Bearer {credenciais.credentials}"
    repositorio = RepositorioAgenda(token_acesso=token)

    # 2. Chamamos o método que busca os dados
    evento = repositorio.listar_evento(meses)

    # 3. Retornamos a lista (o FastAPI valida tudo usando o response_model)
    return evento


@router.post("/evento", response_model=RespostaEventoAgenda, status_code=status.HTTP_201_CREATED)
def criar_evento(
    solicitacao: SolicitacaoEventoAgenda,
    autorizacao: str = Header(None, alias="Authorization"),
    credenciais: HTTPAuthorizationCredentials = Security(autenticacao_bearer),
):
    """
    Rota para criar um evento no Google Calendar.
    """
    token = autorizacao
    if not token and credenciais:
        token = f"Bearer {credenciais.credentials}"
    if not token:
        raise HTTPException(status_code=401, detail="Token de acesso ausente")

    repositorio = RepositorioAgenda(token_acesso=token)
    try:
        return repositorio.criar_evento(solicitacao)
    except RuntimeError as erro:
        raise HTTPException(status_code=502, detail=str(erro)) from erro


@router.delete("/evento/{id_google}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_evento(
    id_google: str,
    autorizacao: str = Header(None, alias="Authorization"),
    credenciais: HTTPAuthorizationCredentials = Security(autenticacao_bearer),
):
    """
    Rota para excluir um evento no Google Calendar.
    """
    token = autorizacao
    if not token and credenciais:
        token = f"Bearer {credenciais.credentials}"
    if not token:
        raise HTTPException(status_code=401, detail="Token de acesso ausente")

    repositorio = RepositorioAgenda(token_acesso=token)
    try:
        repositorio.excluir_evento(id_google)
    except RuntimeError as erro:
        raise HTTPException(status_code=502, detail=str(erro)) from erro
