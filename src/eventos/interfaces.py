# Módulo de interfaces para o serviço de calendário.
# Foi criado para não deixar o projeto parado enquanto as APIs não estão prontas.
# Coloque aqui as interface e simulações de integração

from abc import ABC, abstractmethod
from datetime import datetime

class IServicoCalendario(ABC):
    # Interface: Tudo o que for relacionado a integração com o
    # Google Calendar deve seguir essa estrutura de função.

    @abstractmethod
    def criar_evento_agenda(self, titulo: str, inicio: datetime, fim: datetime) -> str:
        # Coloque o código da função aqui
        pass

class SimulacaoServicoCalendario(IServicoCalendario):
    # Simulação: Simula a criação de um evento no calendário,
    # apenas imprimindo os detalhes e retornando um link fictício.

    def criar_evento_agenda(self, titulo: str, inicio: datetime, fim: datetime) -> str:
        print(f"[MOCK] Agendando evento: '{titulo}' de {inicio} a {fim}")
        return "https://calendar.google.com/calendar/mock-idb-jovem"
