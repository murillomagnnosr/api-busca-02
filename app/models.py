from sqlalchemy import String, Numeric, Column, Integer
from app.database import Base


class ProdutoDB(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    descricao = Column(String(500), nullable=False)
    preco = Column(Numeric(10, 2), nullable=False)
