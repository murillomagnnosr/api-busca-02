"""
Testes de Cenários de Erro — Aula 2
Testam o comportamento em condições adversas.
"""
import pytest
from pydantic import ValidationError

from app.schemas import ProdutoCreate


def test_produto_preco_negativo_levanta_erro():
    """Valida que preço negativo é rejeitado pelo Pydantic"""
    with pytest.raises(ValidationError):
        ProdutoCreate(
            nome="Produto",
            descricao="Com preço inválido",
            preco=-100.0
        )


def test_produto_preco_zero_levanta_erro():
    """Valida que preço zero é rejeitado pelo Pydantic"""
    with pytest.raises(ValidationError):
        ProdutoCreate(
            nome="Produto",
            descricao="Com preço zero",
            preco=0
        )


def test_produto_nome_vazio_levanta_erro():
    """Valida que nome vazio é rejeitado"""
    with pytest.raises(ValidationError):
        ProdutoCreate(
            nome="",
            descricao="Nome vazio",
            preco=100.0
        )


def test_produto_descricao_vazia_levanta_erro():
    """Valida que descrição vazia é rejeitada"""
    with pytest.raises(ValidationError):
        ProdutoCreate(
            nome="Produto",
            descricao="",
            preco=100.0
        )


def test_criar_produto_sem_nome_retorna_422(client):
    """Testa validação de entrada — campo obrigatório faltando"""
    payload = {
        "descricao": "Sem nome",
        "preco": 100.0
    }
    response = client.post("/produtos", json=payload)
    assert response.status_code == 422


def test_criar_produto_preco_negativo_retorna_422(client):
    """Testa validação de entrada — preço inválido"""
    payload = {
        "nome": "Produto",
        "descricao": "Preço negativo",
        "preco": -50.0
    }
    response = client.post("/produtos", json=payload)
    assert response.status_code == 422


def test_produto_com_dados_validos_é_aceito():
    """Testa que produto válido é aceito"""
    produto = ProdutoCreate(
        nome="Notebook",
        descricao="Notebook Dell i7",
        preco=4000.00
    )
    assert produto.nome == "Notebook"
    assert produto.preco == 4000.00
