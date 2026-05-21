from fastapi import APIRouter, Header, HTTPException, Query, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.galeria.repository import RepositorioGaleria
from src.galeria.schema import FotoResponse

router = APIRouter(prefix="/galeria", tags=["Galeria do Google Drive"])

autenticacao_bearer = HTTPBearer(auto_error=False)

@router.get("/fotos", response_model=list[FotoResponse])
def listar_fotos(
    pasta: str = Query(..., min_length=1),
    autorizacao: str = Header(None, alias="Authorization"),
    credenciais: HTTPAuthorizationCredentials = Security(autenticacao_bearer),
):
    """
    Rota para listar as fotos armazenadas no Google Drive por nome de pasta.
    """
    token = autorizacao
    if not token and credenciais:
        token = f"Bearer {credenciais.credentials}"
    if not token:
        raise HTTPException(status_code=401, detail="Token de acesso ausente")

    repositorio = RepositorioGaleria(token_acesso=token)
    try:
        return repositorio.listar_fotos(pasta)
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro)) from erro
    except RuntimeError as erro:
        raise HTTPException(status_code=502, detail=str(erro)) from erro
