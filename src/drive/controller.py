from fastapi import APIRouter, HTTPException, Query, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from src.drive.service import ServicoDrive
from src.drive.schema import RespostaDrive

router = APIRouter(prefix="/galeria", tags=["Galeria do Google Drive"])

autenticacao_bearer = HTTPBearer(auto_error=False)

@router.get("/fotos", response_model=list[RespostaDrive])
def listar_fotos(
    pasta: str = Query(..., min_length=1),
    credenciais: HTTPAuthorizationCredentials = Security(autenticacao_bearer),
):
    """
    Rota para listar as fotos armazenadas no Google Drive por nome de pasta.
    """
    token = credenciais.credentials

    if not token:
        raise HTTPException(status_code=401, detail="Token de acesso ausente")

    servico = ServicoDrive(token_acesso=token)
    try:
        return servico.listar_fotos(pasta)
    except ValueError as erro:
        raise HTTPException(status_code=404, detail=str(erro)) from erro
    except RuntimeError as erro:
        raise HTTPException(status_code=502, detail=str(erro)) from erro
