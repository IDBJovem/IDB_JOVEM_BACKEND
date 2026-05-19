# Aqui que fica as rotas HTTP (Endpoints) usando FastAPI.
# Arquivo usado para comunicação entre o front-end e o back-end.
# Arquivo é meramente ilustrativo e deve ser ajustado de acordo com o nosso projeto.
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from src.eventos.interfaces import SimulacaoServicoCalendario
from src.eventos.schemas import SchemaCriarEvento, SchemaRespostaEvento
from src.eventos.services import ServicoEvento
from src.security import verificar_roles

router = APIRouter(prefix="/eventos", tags=["eventos"])

BANCO_MOCK_EVENTOS: List[SchemaRespostaEvento] = [
    SchemaRespostaEvento(
        id=1,
        titulo="Entrega do PC2",
        data_inicio=datetime(2026, 5, 20, 9, 0, 0),
        data_fim=datetime(2026, 5, 20, 11, 0, 0),
        link_calendario="https://calendar.google.com/calendar/mock-idb-jovem",
    )
]


@router.get("/", response_model=List[SchemaRespostaEvento])
def listar_eventos():
    """Retorna a lista de eventos cadastrados no sistema."""
    return BANCO_MOCK_EVENTOS


@router.post(
    "/",
    response_model=SchemaRespostaEvento,
    status_code=status.HTTP_201_CREATED,
)

def criar_novo_evento(
    payload: SchemaCriarEvento,
    usuario_logado: dict = Depends(verificar_roles(["admin", "superadmin"])),
):
    # Configure o Keucloak de rotas aqui.

    # Foi passado None, pois ainda não foi feito a conexão real com o banco.
    mock_repositorio = None

    mock_calendario = SimulacaoServicoCalendario()

    servico = ServicoEvento(
        repositorio=mock_repositorio,
        servico_calendario=mock_calendario,
    )

    try:
        evento_criado = servico.executar_criacao_evento(payload)
        BANCO_MOCK_EVENTOS.append(SchemaRespostaEvento(**evento_criado))
        return evento_criado
    except ValueError as erro:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(erro)) from erro
