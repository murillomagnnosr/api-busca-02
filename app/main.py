from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db, create_tables
from app.models import ProdutoDB
from app.schemas import Produto, ProdutoCreate
from app.external_service import validar_preco, ExternalServiceError

app = FastAPI(
    title="API de Busca - Aula 2",
    description="API com banco de dados, testes de integração e mocks",
    version="0.2.0"
)


@app.on_event("startup")
def startup():
    create_tables()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/produtos", response_model=list[Produto])
def listar_produtos(db: Session = Depends(get_db)):
    return db.query(ProdutoDB).all()


@app.get("/produtos/{produto_id}", response_model=Produto)
def get_produto(produto_id: int, db: Session = Depends(get_db)):
    produto = db.query(ProdutoDB).filter(ProdutoDB.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=404, detail="Produto não encontrado")
    return produto


@app.get("/buscar", response_model=list[Produto])
def buscar(q: Optional[str] = None, db: Session = Depends(get_db)):
    if not q:
        return db.query(ProdutoDB).all()

    termo = f"%{q}%"
    return db.query(ProdutoDB).filter(
        ProdutoDB.nome.ilike(termo) | ProdutoDB.descricao.ilike(termo)
    ).all()


@app.post("/produtos", response_model=Produto, status_code=201)
async def criar_produto(produto: ProdutoCreate, db: Session = Depends(get_db)):
    # Testa serviço externo (será mockado nos testes)
    try:
        await validar_preco(produto.preco)
    except ExternalServiceError as e:
        raise HTTPException(status_code=503, detail=str(e))

    novo = ProdutoDB(
        nome=produto.nome,
        descricao=produto.descricao,
        preco=produto.preco
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return novo
