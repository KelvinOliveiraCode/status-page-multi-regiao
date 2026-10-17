"""Suíte de testes do status-page-multi-regiao.

Usa TestClient (httpx) sem qualquer chamada de rede real: as regioes sao
simuladas localmente pelo proprio app. Todos os testes sao determinísticos.
"""

from fastapi.testclient import TestClient

from status_page_multi_regiao.main import (
    REGIONS,
    REGION_STATUS,
    build_status_page,
    check_region,
    compute_overall,
    app,
)

client = TestClient(app)


def test_status_page_returns_200_and_aggregated_overall():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["overall"] == "degraded"
    assert data["total"] == len(REGIONS)
    assert (
        data["healthy"] + data["degraded"] + data["unhealthy"] == data["total"]
    )


def test_status_page_includes_every_region():
    response = client.get("/")
    assert set(response.json()["regions"].keys()) == set(REGIONS.keys())


def test_status_page_region_entries_have_expected_shape():
    response = client.get("/")
    for region in REGIONS:
        entry = response.json()["regions"][region]
        assert entry["region"] == region
        assert entry["status"] in ("healthy", "degraded", "unhealthy")
        assert entry["endpoint"] == REGIONS[region]
        assert entry["simulated"] is True


def test_health_all_returns_all_regions():
    response = client.get("/health")
    assert response.status_code == 200
    assert set(response.json().keys()) == set(REGIONS.keys())


def test_health_region_healthy():
    response = client.get("/health/us-east-1")
    assert response.status_code == 200
    assert response.json() == {
        "region": "us-east-1",
        "status": "healthy",
        "endpoint": REGIONS["us-east-1"],
        "simulated": True,
    }


def test_health_region_degraded():
    response = client.get("/health/sa-east-1")
    assert response.status_code == 200
    assert response.json()["status"] == "degraded"


def test_health_unknown_region_returns_404():
    response = client.get("/health/regiao-inexistente")
    assert response.status_code == 404


def test_compute_overall_all_healthy():
    assert compute_overall({"a": "healthy", "b": "healthy"}) == "healthy"


def test_compute_overall_degraded():
    assert compute_overall({"a": "healthy", "b": "degraded"}) == "degraded"


def test_compute_overall_unhealthy_wins_over_degraded():
    assert compute_overall({"a": "degraded", "b": "unhealthy"}) == "unhealthy"


def test_check_region_unknown_raises_keyerror():
    try:
        check_region("xx-inexistente")
    except KeyError:
        return
    raise AssertionError("esperava KeyError para regiao desconhecida")


def test_region_statuses_match_constants():
    for region, expected in REGION_STATUS.items():
        assert check_region(region).status == expected


def test_status_page_is_deterministic():
    first = build_status_page()
    second = build_status_page()
    assert first == second
