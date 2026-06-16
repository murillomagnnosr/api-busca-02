# API de Busca — Aula 2

Evolução da Aula 1 com **banco de dados, testes de integração, mocks e tratamento de erros**.

## Instalação

```bash
uv venv --python 3.12
.venv\Scripts\activate.bat
uv pip install -r requirements.txt
```

## Rodar a API

```bash
uvicorn app.main:app --reload
```

Acesse: http://localhost:8000/docs

## Rodar Testes

```bash
# Todos
pytest -v

# Por tipo
pytest tests/test_integration.py -v
pytest tests/test_mocks.py -v
pytest tests/test_errors.py -v
```

## Incrementos da Aula 2

✅ Banco de dados SQLite  
✅ Testes de integração com banco real  
✅ Mocks de API externa  
✅ Testes de cenários de erro  
✅ Status codes HTTP corretos (404, 422, 503)  
✅ Pipeline CI automático  

## Documentação

Veja [CENARIOS_TESTADOS.md](CENARIOS_TESTADOS.md) para detalhe completo de cada teste.

## Total de Testes

**17 testes** cobrindo 3 categorias:
- 6 testes de integração
- 4 testes com mock
- 7 testes de erro
