from pydantic import BaseModel, Field


class ProdutoBase(BaseModel):
    nome: str = Field(..., min_length=1, description="Nome do produto")
    descricao: str = Field(..., min_length=1, description="Descrição")
    preco: float = Field(..., gt=0, description="Preço deve ser positivo")


class ProdutoCreate(ProdutoBase):
    pass


class Produto(ProdutoBase):
    id: int

    class Config:
        from_attributes = True
