from fastapi import APIRouter, Depends, Header, HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.database import obter_banco
from src.formulario.repository import RepositorioFormulario
from src.formulario.schema import RespostaInscricaoFormulario

router = APIRouter(prefix="/formulario", tags=["Formulario (Google Forms)"])

autenticacao_bearer = HTTPBearer(auto_error=False)

@router.get(
    "/evento/{evento_id}/inscricoes",
    response_model=list[RespostaInscricaoFormulario],
)
def listar_inscricoes(
    evento_id: int,
    autorizacao: str = Header(None, alias="Authorization"),
    credenciais: HTTPAuthorizationCredentials = Security(autenticacao_bearer),
    db=Depends(obter_banco),
):
    """
    Rota para listar as inscricoes de voluntarios do evento.
    """
    token = autorizacao
    if not token and credenciais:
        token = f"Bearer {credenciais.credentials}"
    if not token:
        raise HTTPException(status_code=401, detail="Token de acesso ausente")

    repositorio = RepositorioFormulario(token_acesso=token)
    try:
        return repositorio.listar_inscricoes(db, evento_id)
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro)) from erro
    except RuntimeError as erro:
        raise HTTPException(status_code=502, detail=str(erro)) from erro
