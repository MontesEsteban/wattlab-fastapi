import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.simulator import SimulationInput, simulate_energy

client = TestClient(app)


def test_health_route_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "service": "WattLab"}


def test_home_page_renders_jinja_template():
    response = client.get("/")
    assert response.status_code == 200
    assert "WattLab" in response.text
    assert "Parámetros del escenario" in response.text


def test_simulate_energy_expected_calculation():
    data = SimulationInput(
        device_name="Computador portátil",
        watts=100.0,
        hours_per_day=5.0,
        days_per_month=30,
        tariff_cop_per_kwh=800.0,
        reduction_percent=25.0,
    )
    res = simulate_energy(data)
    assert res.daily_kwh == 0.5
    assert res.monthly_kwh == 15.0
    assert res.monthly_cost_cop == 12000.0
    assert res.optimized_monthly_kwh == 11.25
    assert res.monthly_savings_cop == 3000.0
    assert res.efficiency_rating == "Bajo"


def test_post_simulate_invalid_hours_shows_validation_error():
    response = client.post(
        "/simulate",
        data={
            "device_name": "Servidor local",
            "watts": "500",
            "hours_per_day": "30",
            "days_per_month": "30",
            "tariff_cop_per_kwh": "850",
            "reduction_percent": "10",
        },
    )
    assert response.status_code == 200
    assert "Revisa los datos ingresados" in response.text
    assert "entre 0.1 y 24 horas" in response.text


def test_simulate_energy_raises_on_invalid_watts():
    invalid = SimulationInput(
        device_name="Equipo inválido",
        watts=0,
        hours_per_day=4,
        days_per_month=30,
        tariff_cop_per_kwh=850,
    )
    with pytest.raises(ValueError):
        simulate_energy(invalid)