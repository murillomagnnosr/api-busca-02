# Guia de Apresentação — Aula 2

## Antes de Começar

**Abra 3 janelas (ou abas de terminal):**
1. **Terminal 1:** VS Code ou File Explorer (mostrar estrutura)
2. **Terminal 2:** Rodar os testes
3. **Terminal 3:** Rodar o Swagger UI no navegador

---

## 0️⃣ Introdução (1 minuto)

```
"Apresento a evolução do projeto da Aula 1 com incrementos avançados:
banco de dados real, testes de integração, simulação de falhas 
e testes automatizados no GitHub Actions."
```

---

## 1️⃣ Mostrar a Estrutura (1 minuto)

**Abra o VS Code:**

```
api-busca-02/
├── app/
│   ├── main.py              ← FastAPI + BD
│   ├── database.py          ← SQLAlchemy + SQLite
│   ├── models.py            ← Tabela produtos
│   ├── schemas.py           ← Validação Pydantic
│   └── external_service.py  ← API externa mockada
├── tests/
│   ├── conftest.py          ← Fixtures (BD de teste)
│   ├── test_errors.py       ← 7 testes de erro
│   ├── test_integration.py  ← 5 testes de integração
│   └── test_mocks.py        ← 2 testes com mock
├── CENARIOS_TESTADOS.md     ← Documentação completa
└── .github/workflows/ci.yml ← Pipeline CI
```

**Explique:** "A estrutura é simples mas robusta. O ponto principal é 
como cada camada (banco, validação, testes) funciona em conjunto."

---

## 2️⃣ Executar os Testes (2 minutos)

**Terminal 2, execute:**

```powershell
cd C:\Users\muril\api-busca-02
.venv\Scripts\activate.ps1
pytest -v
```

**Resultado esperado:**

```
============================= 14 passed ======================
tests/test_errors.py::test_produto_preco_negativo_levanta_erro PASSED
tests/test_errors.py::test_produto_preco_zero_levanta_erro PASSED
tests/test_errors.py::test_produto_nome_vazio_levanta_erro PASSED
tests/test_errors.py::test_produto_descricao_vazia_levanta_erro PASSED
tests/test_errors.py::test_criar_produto_sem_nome_retorna_422 PASSED
tests/test_errors.py::test_criar_produto_preco_negativo_retorna_422 PASSED
tests/test_errors.py::test_produto_com_dados_validos_é_aceito PASSED
tests/test_integration.py::test_criar_produto_persiste_no_banco PASSED
tests/test_integration.py::test_atualizar_produto_no_banco PASSED
tests/test_integration.py::test_deletar_produto_do_banco PASSED
tests/test_integration.py::test_buscar_multiplos_produtos PASSED
tests/test_integration.py::test_contar_produtos PASSED
tests/test_mocks.py::test_validar_preco_timeout_levanta_erro PASSED
tests/test_mocks.py::test_criar_produto_quando_api_falha_retorna_503 PASSED
```

**Pause aqui e explique:**

> "14 testes cobrindo 3 cenários:
> - **7 testes de erro:** validam que dados inválidos são rejeitados
> - **5 testes de integração:** verificam que dados persistem no banco real
> - **2 testes de mock:** simulam a API externa falhando"

---

## 3️⃣ Mostrar um Teste (1 minuto)

**Abra `tests/test_integration.py` no VS Code:**

```python
def test_criar_produto_persiste_no_banco(db_session):
    """Testa se um produto criado é persistido no banco"""
    produto = ProdutoDB(nome="SSD", descricao="SSD 1TB", preco=599.90)
    db_session.add(produto)
    db_session.commit()
    db_session.refresh(produto)

    recuperado = db_session.query(ProdutoDB).filter(ProdutoDB.nome == "SSD").first()
    assert recuperado is not None
    assert float(recuperado.preco) == pytest.approx(599.90)
```

**Explique:**

> "Este teste mostra a **integração real com o banco**:
> 1. Insere um produto no SQLite em memória
> 2. Faz commit (persiste)
> 3. Busca de volta pelo nome
> 4. Valida que está lá com o preço correto"

---

## 4️⃣ Mostrar um Teste de Erro (1 minuto)

**Abra `tests/test_errors.py`:**

```python
def test_produto_preco_negativo_levanta_erro():
    """Valida que preço negativo é rejeitado pelo Pydantic"""
    with pytest.raises(ValidationError):
        ProdutoCreate(
            nome="Produto",
            descricao="Com preço inválido",
            preco=-100.0  # ← Inválido
        )
```

**Explique:**

> "Este teste valida **rejeição de dados ruins**:
> - Tenta criar um produto com preço negativo
> - Espera que o Pydantic lance ValidationError
> - Se isso não acontecer, o teste falha"

---

## 5️⃣ Mostrar um Mock (1 minuto)

**Abra `tests/test_mocks.py`:**

```python
@pytest.mark.asyncio
async def test_validar_preco_timeout_levanta_erro():
    """Testa que timeout da API externa levanta ExternalServiceError"""
    import httpx
    with patch("app.external_service.httpx.AsyncClient") as mock_client_class:
        mock_instance = AsyncMock()
        mock_instance.get = AsyncMock(side_effect=httpx.TimeoutException("timeout"))
        # ...
        
        with pytest.raises(ExternalServiceError, match="respondeu lentamente"):
            await validar_preco(4000.00)
```

**Explique:**

> "Este teste **simula uma falha da API externa**:
> 1. Mock substitui `httpx.get` por um objeto controlado
> 2. Configuramos para lançar TimeoutException
> 3. Testamos que a aplicação trata isso corretamente
> 4. **Sem fazer chamada HTTP real** — rápido e isolado"

---

## 6️⃣ Rodar a API (2 minutos)

**Terminal 3, execute:**

```powershell
cd C:\Users\muril\api-busca-02
.venv\Scripts\activate.ps1
uvicorn app.main:app --reload
```

**Abra no navegador:** http://localhost:8000/docs

**Teste 3 endpoints:**

### 1. POST /produtos (criar)
```json
{
  "nome": "SSD Samsung 1TB",
  "descricao": "SSD rápido 1000 MB/s",
  "preco": 599.90
}
```
**Resultado:** `201 Created` com ID gerado

### 2. GET /produtos (listar)
**Resultado:** Lista com os produtos

### 3. POST /produtos (teste de erro — preço negativo)
```json
{
  "nome": "Produto",
  "descricao": "Teste",
  "preco": -100.0
}
```
**Resultado:** `422 Unprocessable Entity`

---

## 7️⃣ Mostrar o Documento de Cenários (1 minuto)

**Abra `CENARIOS_TESTADOS.md`:**

> "Este arquivo documenta **cada teste e por que testa**:
> - Qual cenário ele cobre
> - O que está sendo validado
> - Por que é importante"

---

## 8️⃣ Mostrar o Pipeline CI (30 segundos)

**Abra `.github/workflows/ci.yml`:**

```yaml
- name: Testes de Integração
  run: pytest tests/test_integration.py -v

- name: Testes com Mock
  run: pytest tests/test_mocks.py -v

- name: Testes de Erro
  run: pytest tests/test_errors.py -v
```

**Explique:**

> "A cada push no GitHub, estes testes rodam **automaticamente**:
> - Se algum falhar, o pipeline inteiro falha
> - Garante qualidade antes de mesclar no main"

---

## 9️⃣ Diferenciais vs Aula 1 (1 minuto)

| Feature | Aula 1 | Aula 2 |
|---------|--------|--------|
| Banco de dados | Memória (lista) | **SQLite real** |
| Persistência | Não | **Sim (CRUD completo)** |
| Testes de integração | Não | **5 testes** |
| Testes de erro | Não | **7 testes** |
| Mock de API externa | Não | **2 testes** |
| Cenários de falha | Não | **Timeout, conexão recusada** |
| Status codes corretos | Não | **200, 201, 422, 503** |
| CI automático | Básico | **Completo** |
| **Total de testes** | **5** | **14** |

---

## 🎯 Responder Perguntas Possíveis

### "Por que usar SQLite em memória nos testes?"

> "Porque:
> 1. **Cada teste começa limpo** — sem dados do teste anterior
> 2. **Rápido** — sem I/O de disco
> 3. **Isolado** — não interfere no banco real
> 4. **Idêntico** — mesma lógica SQL que o PostgreSQL"

### "O que é um Mock?"

> "Um mock substitui uma dependência real (API externa) por um objeto 
> que você controla. Podemos simular erros sem esperar que a API real falhe."

### "Como o CI funciona?"

> "A cada push, o GitHub Actions executa o arquivo `.github/workflows/ci.yml`.
> Se os testes falharem, a build fica vermelha e o merge é bloqueado."

### "Qual é a diferença entre integração e unitário?"

> "**Unitário:** testa uma função isolada (sem banco, sem HTTP)
> **Integração:** testa com banco real ou componentes reais"

---

## ⏱️ Timeline Recomendada

```
0-2 min   → Mostrar estrutura + explicar arquitetura
2-6 min   → Rodar pytest (mostrar 14 testes passando)
6-8 min   → Explicar 3 testes (erro, integração, mock)
8-12 min  → Rodar API e testar endpoints no Swagger
12-13 min → Mostrar CI + CENARIOS_TESTADOS.md
13-15 min → Responder perguntas
```

---

## Entregáveis Apresentados

✅ Repositório criado com estrutura clara  
✅ Aplicação FastAPI rodando  
✅ Banco de dados SQLite integrado  
✅ **14 testes automatizados**  
✅ Testes de integração com banco real  
✅ Testes de erro (422, 404, 503)  
✅ Mocks de API externa  
✅ Pipeline CI automático  
✅ Documentação dos cenários  
✅ README + guia de execução  
