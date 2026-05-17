# Aqui que fica as rotas HTTP (Endpoints) usando FastAPI.
# Arquivo usado para comunicação entre o front-end e o back-end.
# Arquivo é meramente ilustrativo e deve ser ajustado de acordo com o nosso projeto.
from fastapi import APIRouter, HTTPException, status
from src.eventos.interfaces import SimulacaoServicoCalendario
from src.eventos.schemas import SchemaCriarEvento, SchemaRespostaEvento
from src.eventos.services import ServicoEvento

router = APIRouter(prefix="/eventos", tags=["eventos"])

@router.post(
    "/",
    response_model=SchemaRespostaEvento,
    status_code=status.HTTP_201_CREATED,
)

def criar_novo_evento(payload: SchemaCriarEvento):
    # Configure o Keucloak de rotas aqui.

    # Foi passado None, pois ainda não foi feito a conexão real com o banco.
    mock_repositorio = None

    mock_calendario = SimulacaoServicoCalendario()

    servico = ServicoEvento(repositorio=mock_repositorio, servico_calendario=mock_calendario)

    try:
        return servico.executar_criacao_evento(payload)
    except ValueError as erro:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(erro)) from erro
