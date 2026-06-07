import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from src.evento.controller import (
    criar_evento, buscar_todos_evento, buscar_evento_id,
    atualizar_evento, deletar_evento, pesquisar_eventos, 
    listar_galeria_evento, get_servico,
)


class TestEventoController:
    def test_get_servico(self):
        mock_db = MagicMock()
        servico = get_servico(db=mock_db)
        from src.evento.service import ServicoEvento
        assert isinstance(servico, ServicoEvento)

    def test_criar_evento_sucesso(self):
        mock_servico = MagicMock()
        mock_servico.criar_evento.return_value = MagicMock()
        resultado = criar_evento(solicitar=MagicMock(), servico=mock_servico, _={})
        mock_servico.criar_evento.assert_called_once()

    def test_criar_evento_erro(self):
        mock_servico = MagicMock()
        mock_servico.criar_evento.side_effect = ValueError("Data inválida")
        with pytest.raises(HTTPException) as exc:
            criar_evento(solicitar=MagicMock(), servico=mock_servico, _={})
        assert exc.value.status_code == 400

    def test_pesquisar_eventos(self):
        mock_servico = MagicMock()
        mock_servico.pesquisar_eventos.return_value = []
        resultado = pesquisar_eventos(termo="teste", servico=mock_servico)
        mock_servico.pesquisar_eventos.assert_called_once_with("teste")

    def test_buscar_todos_evento(self):
        mock_servico = MagicMock()
        mock_servico.listar_evento.return_value = []
        resultado = buscar_todos_evento(servico=mock_servico)
        mock_servico.listar_evento.assert_called_once()

    def test_buscar_evento_id_sucesso(self):
        mock_servico = MagicMock()
        mock_servico.buscar_evento.return_value = MagicMock()
        resultado = buscar_evento_id(evento_id=1, servico=mock_servico)
        mock_servico.buscar_evento.assert_called_once_with(1)

    def test_buscar_evento_id_nao_encontrado(self):
        mock_servico = MagicMock()
        mock_servico.buscar_evento.side_effect = ValueError("Não encontrado")
        with pytest.raises(HTTPException) as exc:
            buscar_evento_id(evento_id=1, servico=mock_servico)
        assert exc.value.status_code == 404

    def test_atualizar_evento_sucesso(self):
        mock_servico = MagicMock()
        mock_servico.atualizar_evento.return_value = MagicMock()
        resultado = atualizar_evento(evento_id=1, solicitar=MagicMock(), servico=mock_servico, _={})
        mock_servico.atualizar_evento.assert_called_once()

    def test_atualizar_evento_erro(self):
        mock_servico = MagicMock()
        mock_servico.atualizar_evento.side_effect = ValueError("Erro")
        with pytest.raises(HTTPException) as exc:
            atualizar_evento(evento_id=1, solicitar=MagicMock(), servico=mock_servico, _={})
        assert exc.value.status_code == 400

    def test_deletar_evento_sucesso(self):
        mock_servico = MagicMock()
        deletar_evento(evento_id=1, servico=mock_servico, _={})
        mock_servico.deletar_evento.assert_called_once_with(1)

    def test_deletar_evento_erro(self):
        mock_servico = MagicMock()
        mock_servico.deletar_evento.side_effect = ValueError("Não encontrado")
        with pytest.raises(HTTPException) as exc:
            deletar_evento(evento_id=1, servico=mock_servico, _={})
        assert exc.value.status_code == 404

    @patch("src.evento.controller.ServicoDrive")
    def test_listar_galeria_evento_sucesso(self, mock_drive_class):
        mock_servico = MagicMock()
        mock_evento = MagicMock()
        mock_evento.link_galeria = "PastaFotos"
        mock_servico.buscar_evento.return_value = mock_evento

        mock_drive = MagicMock()
        mock_drive.listar_fotos.return_value = []
        mock_drive_class.return_value = mock_drive

        resultado = listar_galeria_evento(evento_id=1, servico=mock_servico)
        mock_drive.listar_fotos.assert_called_once_with("PastaFotos")

    def test_listar_galeria_evento_sem_link(self):
        mock_servico = MagicMock()
        mock_evento = MagicMock()
        mock_evento.link_galeria = None
        mock_servico.buscar_evento.return_value = mock_evento

        resultado = listar_galeria_evento(evento_id=1, servico=mock_servico)
        assert resultado == []

    def test_listar_galeria_evento_nao_encontrado(self):
        mock_servico = MagicMock()
        mock_servico.buscar_evento.side_effect = ValueError("Não encontrado")
        with pytest.raises(HTTPException) as exc:
            listar_galeria_evento(evento_id=1, servico=mock_servico)
        assert exc.value.status_code == 404

    @patch("src.evento.controller.ServicoDrive")
    def test_listar_galeria_evento_runtime_error(self, mock_drive_class):
        mock_servico = MagicMock()
        mock_evento = MagicMock()
        mock_evento.link_galeria = "Pasta"
        mock_servico.buscar_evento.return_value = mock_evento

        mock_drive = MagicMock()
        mock_drive.listar_fotos.side_effect = RuntimeError("Erro API")
        mock_drive_class.return_value = mock_drive

        with pytest.raises(HTTPException) as exc:
            listar_galeria_evento(evento_id=1, servico=mock_servico)
        assert exc.value.status_code == 502
