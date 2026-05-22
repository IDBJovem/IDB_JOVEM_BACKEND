from fastapi import APIRouter, HTTPException, Query
from src.mapa.service import ServicoMapa
from src.shared.utils import validar_coordenadas

router = APIRouter(prefix="/mapa", tags=["mapa"])


@router.get("/endereco")
def buscar_endereco(latitude: float = Query(...), longitude: float = Query(...)):
    try:
        validar_coordenadas(latitude, longitude)

        mapa = ServicoMapa()
        nome_local = mapa.buscar_endereco_por_coordenadas(latitude, longitude)

        if not nome_local:
            raise HTTPException(
                status_code=404,
                detail="Endereço não encontrado para essas coordenadas."
            )

        return {"nome_local": nome_local}

    except ValueError as erro:
        raise HTTPException(status_code=400, detail=str(erro)) from erro
