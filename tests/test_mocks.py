"""
Testes com Mock — Aula 2
Mockam a API externa para não fazer chamadas HTTP reais.
"""
from unittest.mock import patch, AsyncMock
import pytest

from app.external_service import ExternalServiceError


@pytest.mark.asyncio
async def test_validar_preco_timeout_levanta_erro():
    """Testa que timeout da API externa levanta ExternalServiceError"""
    import httpx
    with patch("app.external_service.httpx.AsyncClient") as mock_client_class:
        mock_instance = AsyncMock()
        mock_instance.get = AsyncMock(side_effect=httpx.TimeoutException("timeout"))
        mock_instance.__aenter__ = AsyncMock(return_value=mock_instance)
        mock_instance.__aexit__ = AsyncMock(return_value=None)
        mock_client_class.return_value = mock_instance

        from app.external_service import validar_preco
        with pytest.raises(ExternalServiceError, match="respondeu lentamente"):
            await validar_preco(4000.00)


@pytest.mark.asyncio
async def test_criar_produto_quando_api_falha_retorna_503(client):
    """Testa que 503 é retornado quando serviço externo falha"""
    with patch("app.main.validar_preco", new_callable=AsyncMock) as mock_validate:
        mock_validate.side_effect = ExternalServiceError("Serviço indisponível")

        payload = {
            "nome": "Monitor",
            "descricao": "Monitor 27 polegadas",
            "preco": 1500.00
        }
        response = client.post("/produtos", json=payload)

        assert response.status_code == 503
        assert "Serviço" in response.json()["detail"]
