"""
Testes de Integração — Aula 2
Testam operações diretas no banco de dados (SQLite em memória).
"""
import pytest
from app.models import ProdutoDB


def test_criar_produto_persiste_no_banco(db_session):
    """Testa se um produto criado é persistido no banco"""
    produto = ProdutoDB(nome="SSD", descricao="SSD 1TB", preco=599.90)
    db_session.add(produto)
    db_session.commit()
    db_session.refresh(produto)

    recuperado = db_session.query(ProdutoDB).filter(ProdutoDB.nome == "SSD").first()
    assert recuperado is not None
    assert float(recuperado.preco) == pytest.approx(599.90)


def test_atualizar_produto_no_banco(db_session):
    """Testa atualização de produto no banco"""
    produto = ProdutoDB(nome="Monitor", descricao="Monitor 24\"", preco=1000.00)
    db_session.add(produto)
    db_session.commit()

    produto.preco = 900.00
    db_session.commit()

    verificado = db_session.query(ProdutoDB).filter(ProdutoDB.id == produto.id).first()
    assert float(verificado.preco) == pytest.approx(900.00)


def test_deletar_produto_do_banco(db_session):
    """Testa deleção de produto no banco"""
    produto = ProdutoDB(nome="Teclado", descricao="Teclado USB", preco=200.00)
    db_session.add(produto)
    db_session.commit()
    produto_id = produto.id

    db_session.delete(produto)
    db_session.commit()

    verificado = db_session.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
    assert verificado is None


def test_buscar_multiplos_produtos(db_session):
    """Testa busca de múltiplos produtos com filtro"""
    db_session.add(ProdutoDB(nome="Notebook Dell", descricao="Notebook i7", preco=4000.00))
    db_session.add(ProdutoDB(nome="Notebook HP", descricao="Notebook Ryzen", preco=3500.00))
    db_session.add(ProdutoDB(nome="Mouse", descricao="Mouse Wireless", preco=100.00))
    db_session.commit()

    notebooks = db_session.query(ProdutoDB).filter(
        ProdutoDB.nome.ilike("%Notebook%")
    ).all()
    assert len(notebooks) == 2


def test_contar_produtos(db_session):
    """Testa contagem de produtos"""
    db_session.add(ProdutoDB(nome="P1", descricao="Desc1", preco=100.00))
    db_session.add(ProdutoDB(nome="P2", descricao="Desc2", preco=200.00))
    db_session.add(ProdutoDB(nome="P3", descricao="Desc3", preco=300.00))
    db_session.commit()

    total = db_session.query(ProdutoDB).count()
    assert total == 3
