# BRIEF — status-page-multi-regiao

## Projeto

`status-page-multi-regiao` (área DevOps/Cloud): health checks multi-região +
status page agregada.

**Caminho:** `C:\Users\Kelvin\AppData\Local\Temp\opencode\github-staging\projects\status-page-multi-regiao\`

**Stack:** Python 3.10+, FastAPI, Pydantic. Testes: pytest + `httpx.TestClient`
(sem rede real).

## Critérios de aceitação (do PLANO_50_PROJETOS.md)

| Critério | Status | Como verificar |
|----------|--------|----------------|
| Health checks funcionam | OK | `python -m pytest -q` — 13 passam |
| Testes que passem | OK | `python -m pytest -q` — 13 passed |
| README PT/EN completo | OK | `README.md` (título, descrição, como usar, testes, licença MIT, autor Kelvin Oliveira) |

## Entregas (arquivos criados)

1. `pyproject.toml` — dependências (fastapi, httpx, uvicorn), entry point,
   config do pytest (`testpaths = ["tests"]`, `pythonpath = ["src"]`).
2. `src/status_page_multi_regiao/__init__.py` — pacote (`__version__ = "0.1.0"`).
3. `src/status_page_multi_regiao/main.py` — app FastAPI:
   - `GET /` — status page agregada (estado geral + detalhe por região).
   - `GET /health` — health check de todas as regiões simuladas.
   - `GET /health/<região>` — health check de uma região (404 se não existir).
   - Regiões simuladas (sem rede): us-east-1 healthy, eu-west-1 healthy,
     sa-east-1 degraded, ap-southeast-1 healthy. Determinístico.
4. `tests/test_health.py` — 13 testes com TestClient, sem rede real.
5. `README.md` — bilíngue PT-BR + EN completo.
6. `BRIEF.md` — este arquivo.

## Como verificar

```bash
cd "C:\Users\Kelvin\AppData\Local\Temp\opencode\github-staging\projects\status-page-multi-regiao\"
python -m pytest -q
```

Esperado: `13 passed in ...s`, output limpo.

Pontos manuais (opcional):

```bash
python -m status_page_multi_regiao.main   # sobe em http://127.0.0.1:8000
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/health/sa-east-1
```

## Caminhos dos documentos-chave

* README: `C:\Users\Kelvin\AppData\Local\Temp\opencode\github-staging\projects\status-page-multi-regiao\README.md`
* BRIEF:  `C:\Users\Kelvin\AppData\Local\Temp\opencode\github-staging\projects\status-page-multi-regiao\BRIEF.md`

**Validador:** workflow manager (sessão que spawnou este subagent).
