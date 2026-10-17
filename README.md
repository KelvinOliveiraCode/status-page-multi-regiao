# status-page-multi-regiao

## / Descrição

Health checks multi-região com status page agregada, construído em Python +
FastAPI. As regiões são simuladas localmente: **nenhuma chamada de rede real é
feita**. O resultado é determinístico (sem relógio, sem aleatoriedade), o que
permite testes reproduzíveis com `TestClient`.

Regiões simuladas (endpoint falso, não acessado):

| Região | Status |
|--------|--------|
| us-east-1 | healthy |
| eu-west-1 | healthy |
| sa-east-1 | degraded |
| ap-southeast-1 | healthy |

Endpoints:

* `GET /` — status page agregada: estado geral mais detalhe por região.
* `GET /health` — health check de todas as regiões simuladas.
* `GET /health/<região>` — health check de uma região (404 se não existir).

Pilha: Python 3.10+, FastAPI, Pydantic, pytest com `httpx.TestClient`.

---

## Description (EN)

Multi-region health checks with an aggregated status page, built in Python +
FastAPI. Regions are simulated locally: **no real network call is made**.
Results are deterministic (no clock, no randomness), so tests are reproducible
with `httpx.TestClient`.

Simulated regions (fake endpoint, never accessed):

| Region | Status |
|--------|--------|
| us-east-1 | healthy |
| eu-west-1 | healthy |
| sa-east-1 | degraded |
| ap-southeast-1 | healthy |

Endpoints:

* `GET /` — aggregated status page: overall state plus per-region detail.
* `GET /health` — health check of all simulated regions.
* `GET /health/<region>` — health check of one region (404 if it does not exist).

Stack: Python 3.10+, FastAPI, Pydantic, pytest with `httpx.TestClient`.

---

## / Como usar

### Pré-requisitos

Python 3.10 ou superior.

### Instalar dependências

```bash
pip install fastapi uvicorn httpx
```

### Rodar o app

```bash
python -m status_page_multi_regiao.main
```

O servidor sobe em `http://127.0.0.1:8000`.

### Endpoints rápidos

```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/health/sa-east-1
```

---

## How to use (EN)

### Requirements

Python 3.10 or higher.

### Install dependencies

```bash
pip install fastapi uvicorn httpx
```

### Run the app

```bash
python -m status_page_multi_regiao.main
```

The server starts at `http://127.0.0.1:8000`.

### Quick endpoints

```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/health/sa-east-1
```

---

## / Testes

```bash
python -m pytest -q
```

Resultado esperado: todos os testes passam (13 testes, sem rede real).

---

## Tests (EN)

```bash
python -m pytest -q
```

Expected result: all tests pass (13 tests, no real network).

---

## / Licença

MIT.

---

## License (EN)

MIT.

---

## / Autor

Kelvin Oliveira

---

## Author (EN)

Kelvin Oliveira
