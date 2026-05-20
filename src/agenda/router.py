from fastapi import APIRouter, Header, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.agenda.repository import RepositorioAgenda
from src.agenda.schema import EventoResponse

# Criamos o roteador definindo o prefixo da URL e a "tag" para a documentação
router = APIRouter(prefix="/agenda", tags=["Agenda do Google"])

autenticacao_bearer = HTTPBearer(auto_error=False)

@router.get("/eventos", response_model=list[EventoResponse])
def listar_eventos(
    autorizacao: str = Header(None, alias="Authorization"),
    credenciais: HTTPAuthorizationCredentials = Security(autenticacao_bearer),
):
    """
    Rota para listar os próximos eventos da agenda.
    """
    # 1. Instanciamos o repositório (passando o token do cabeçalho se existir)
    token = autorizacao
    if not token and credenciais:
        token = f"Bearer {credenciais.credentials}"
    repositorio = RepositorioAgenda(token_acesso=token)

    # 2. Chamamos o método que busca os dados
    eventos = repositorio.listar_eventos()

    # 3. Retornamos a lista (o FastAPI valida tudo usando o response_model)
    return eventos
