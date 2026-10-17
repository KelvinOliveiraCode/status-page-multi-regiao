"""FastAPI: health checks multi-regiao com status page agregada.

Todas as regioes sao simuladas localmente: nenhuma chamada de rede real e
feita. O resultado e deterministico (sem random, sem relogio), o que permite
testes reproduziveis com TestClient.
"""

from __future__ import annotations

from typing import Dict

from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel


class RegionHealth(BaseModel):
    """Resultado do health check de uma unica regiao."""

    region: str
    status: str  # "healthy" | "degraded" | "unhealthy"
    endpoint: str
    simulated: bool = True


class StatusPage(BaseModel):
    """Status page agregada com o estado de todas as regioes."""

    overall: str
    regions: Dict[str, RegionHealth]
    total: int
    healthy: int
    degraded: int
    unhealthy: int


# Regioes simuladas: id da regiao -> endpoint simulado (nao e acessado de fato).
REGIONS: Dict[str, str] = {
    "us-east-1": "http://us-east-1.local/health",
    "eu-west-1": "http://eu-west-1.local/health",
    "sa-east-1": "http://sa-east-1.local/health",
    "ap-southeast-1": "http://ap-southeast-1.local/health",
}

# Status fixo por regiao (simulacao deterministica, sem rede).
REGION_STATUS: Dict[str, str] = {
    "us-east-1": "healthy",
    "eu-west-1": "healthy",
    "sa-east-1": "degraded",
    "ap-southeast-1": "healthy",
}


def compute_overall(statuses: Dict[str, str]) -> str:
    """Retorna o status agregado de um dicionario regiao -> status.

    Regras: unhealthy se houver qualquer unhealthy; degraded se houver
    qualquer degraded e nenhum unhealthy; healthy caso contrario.
    """
    if any(status == "unhealthy" for status in statuses.values()):
        return "unhealthy"
    if any(status == "degraded" for status in statuses.values()):
        return "degraded"
    return "healthy"


def check_region(region: str) -> RegionHealth:
    """Executa o health check simulado de uma regiao.

    Levanta KeyError quando a regiao nao existe no catalogo REGIONS.
    """
    if region not in REGIONS:
        raise KeyError(f"Regiao desconhecida: {region}")
    return RegionHealth(
        region=region,
        status=REGION_STATUS[region],
        endpoint=REGIONS[region],
        simulated=True,
    )


def build_status_page() -> StatusPage:
    """Constrói a status page agregada de todas as regioes simuladas."""
    results = {region: check_region(region) for region in REGIONS}
    statuses = {region: health.status for region, health in results.items()}
    overall = compute_overall(statuses)
    counts: Dict[str, int] = {"healthy": 0, "degraded": 0, "unhealthy": 0}
    for health in results.values():
        counts[health.status] += 1
    return StatusPage(
        overall=overall,
        regions=results,
        total=len(results),
        healthy=counts["healthy"],
        degraded=counts["degraded"],
        unhealthy=counts["unhealthy"],
    )


app = FastAPI(
    title="Status Page Multi-Regiao",
    description="Health checks simulados por regiao com status page agregada.",
    version="0.1.0",
)


@app.get("/", response_model=StatusPage)
def status_page() -> StatusPage:
    """Status page agregada: estado geral e detalhe por regiao."""
    return build_status_page()


@app.get("/health", response_model=Dict[str, RegionHealth])
def health_all() -> Dict[str, RegionHealth]:
    """Health check de todas as regioes simuladas."""
    return {region: check_region(region) for region in REGIONS}


@app.get("/health/{region}", response_model=RegionHealth)
def health_region(
    region: str = Path(..., description="ID da regiao, ex: us-east-1"),
) -> RegionHealth:
    """Health check de uma unica regiao simulada.

    Retorna 404 quando a regiao nao existe no catalogo.
    """
    try:
        return check_region(region)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


def main() -> None:
    """Inicia o servidor uvicorn (uso local apenas)."""
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
