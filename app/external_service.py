import httpx


class ExternalServiceError(Exception):
    """Erro ao chamar serviço externo"""
    pass


async def validar_preco(preco: float) -> bool:
    """
    Chama API externa para validar se o preço está em um intervalo aceitável.

    Esta função é mockada nos testes para não fazer chamadas HTTP reais.
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                "https://api.pricing-service.example.com/validate",
                params={"preco": preco},
                timeout=5.0,
            )
            response.raise_for_status()
            return response.json().get("valido", True)
    except httpx.TimeoutException:
        raise ExternalServiceError("Serviço de preços respondeu lentamente")
    except httpx.HTTPStatusError:
        raise ExternalServiceError("Serviço de preços indisponível (erro 5xx)")
    except httpx.RequestError:
        raise ExternalServiceError("Falha de conexão com serviço de preços")
