# Cenários Testados — Aula 2

## 1. Testes de Integração (test_integration.py)

Testam a aplicação com **banco de dados REAL** (SQLite em memória).

| Cenário | O que testa | Arquivo |
|---------|-----------|---------|
| `test_criar_produto_persiste_no_banco` | Inserção → leitura do banco | `test_integration.py` |
| `test_listar_produtos_via_endpoint` | GET /produtos com dados reais | `test_integration.py` |
| `test_buscar_produto_por_id_banco_real` | GET /produtos/{id} com banco real | `test_integration.py` |
| `test_buscar_sem_resultado` | GET com ID inexistente | `test_integration.py` |
| `test_busca_por_texto_funciona` | GET /buscar?q= com ILIKE | `test_integration.py` |
| `test_criar_produto_via_endpoint` | POST persiste no banco | `test_integration.py` |

**Por que banco em memória?**
- Cada teste começa com banco limpo
- Sem I/O de disco → testes rápidos
- Sem efeitos colaterais entre testes
- Identico ao comportamento do banco real para as operações testadas

---

## 2. Testes com Mock (test_mocks.py)

Mockam a **API externa** para não fazer chamadas HTTP reais.

### O que é Mock?
Um mock substitui uma dependência real (API externa) por um objeto que você controla.

| Cenário | Mock aplicado | O que testa |
|---------|---------------|-----------|
| `test_validar_preco_sucesso` | `httpx.AsyncClient` → resposta fake | Serviço processa resultado correto |
| `test_validar_preco_timeout` | `httpx.AsyncClient` → TimeoutException | Timeout vira ExternalServiceError |
| `test_criar_produto_com_api_externa_mockada` | `validar_preco` → AsyncMock | Endpoint chama API com parametros corretos |
| `test_criar_produto_quando_api_falha` | `validar_preco` → ExternalServiceError | Endpoint retorna 503 quando API falha |

**Por que mockar?**
- Não faz chamadas HTTP reais (rápido)
- Testa o que acontece quando API falha (sem aguardar crash real)
- Testes isolados — não dependem da disponibilidade da API

---

## 3. Testes de Cenários de Erro (test_errors.py)

Testam o comportamento em condições **adversas**.

### Validação de Entrada (422 Unprocessable Entity)
| Cenário | Por quê falha |
|---------|--------------|
| `test_produto_preco_negativo_levanta_erro` | Violação: `preco > 0` |
| `test_produto_preco_zero_levanta_erro` | Violação: `preco > 0` |
| `test_produto_nome_vazio_levanta_erro` | Violação: `min_length=1` |
| `test_criar_produto_sem_nome_retorna_422` | Campo obrigatório faltando |
| `test_criar_produto_preco_negativo_retorna_422` | Campo com valor inválido |

### Recurso Não Encontrado (404 Not Found)
| Cenário | Comportamento |
|---------|--------------|
| `test_get_produto_inexistente_retorna_404` | GET /produtos/99999 → 404 |

### Lista Vazia (não é erro)
| Cenário | Comportamento |
|---------|--------------|
| `test_busca_vazia_retorna_lista_nao_erro` | GET /buscar?q=xyz → 200 com `[]` |

---

## 4. Pipeline CI (.github/workflows/ci.yml)

A cada push no GitHub, os testes rodam **automaticamente**:

```yaml
- pytest tests/test_integration.py     (6 testes)
- pytest tests/test_mocks.py           (4 testes)
- pytest tests/test_errors.py          (7 testes)
```

Resultado: **17 testes** executados automaticamente.

---

## Resumo de Incrementos da Aula 2

| Feature | Aula 1 | Aula 2 |
|---------|--------|--------|
| Banco de dados | Memória (lista Python) | SQLite (persistência) |
| Testes de integração | Não | Sim (6 testes) |
| Testes com mock | Não | Sim (4 testes) |
| Testes de erro | Não | Sim (7 testes) |
| API externa | Não | Sim (mockada) |
| Status codes errados | 200 para tudo | 404, 422, 503 corretos |
| Cenários de falha | Não testados | Timeout, conexão recusada |
| CI automático | Básico | Completo com matriz de testes |
| Total de testes | 5 | **17** |

---

## Como executar

```bash
# Todos os testes
pytest -v

# Por categoria
pytest tests/test_integration.py -v  # Integração
pytest tests/test_mocks.py -v        # Mocks
pytest tests/test_errors.py -v       # Erros
```
