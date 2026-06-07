import pytest
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from src.admin.controller import criar_admin, listar_admins, buscar_admin, deletar_admin, get_servico


class TestAdminController:
    def test_get_servico(self):
        mock_db = MagicMock()
        servico = get_servico(db=mock_db)
        from src.admin.service import ServicoAdmin
        assert isinstance(servico, ServicoAdmin)

    def test_criar_admin_sucesso(self):
        mock_servico = MagicMock()
        mock_servico.criar_admin.return_value = MagicMock()
        resultado = criar_admin(solicitacao=MagicMock(), servico=mock_servico, _={})
        mock_servico.criar_admin.assert_called_once()

    def test_criar_admin_erro(self):
        mock_servico = MagicMock()
        mock_servico.criar_admin.side_effect = ValueError("E-mail duplicado")
        with pytest.raises(HTTPException) as exc:
            criar_admin(solicitacao=MagicMock(), servico=mock_servico, _={})
        assert exc.value.status_code == 400

    def test_listar_admins(self):
        mock_servico = MagicMock()
        mock_servico.listar_admins.return_value = []
        resultado = listar_admins(servico=mock_servico, _={})
        mock_servico.listar_admins.assert_called_once()

    def test_buscar_admin_sucesso(self):
        mock_servico = MagicMock()
        mock_servico.buscar_admin.return_value = MagicMock()
        resultado = buscar_admin(admin_id=1, servico=mock_servico, _={})
        mock_servico.buscar_admin.assert_called_once_with(1)

    def test_buscar_admin_nao_encontrado(self):
        mock_servico = MagicMock()
        mock_servico.buscar_admin.side_effect = ValueError("Não encontrado")
        with pytest.raises(HTTPException) as exc:
            buscar_admin(admin_id=1, servico=mock_servico, _={})
        assert exc.value.status_code == 404

    def test_deletar_admin_sucesso(self):
        mock_servico = MagicMock()
        usuario = {"sub": "uuid-1"}
        deletar_admin(admin_id=1, servico=mock_servico, usuario_logado=usuario)
        mock_servico.deletar_admin.assert_called_once_with(1, usuario)

    def test_deletar_admin_erro(self):
        mock_servico = MagicMock()
        mock_servico.deletar_admin.side_effect = ValueError("Não pode deletar")
        with pytest.raises(HTTPException) as exc:
            deletar_admin(admin_id=1, servico=mock_servico, usuario_logado={})
        assert exc.value.status_code == 400
