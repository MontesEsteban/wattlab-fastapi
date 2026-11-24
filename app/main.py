from pathlib import Path
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.simulator import SimulationInput, simulate_energy

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app = FastAPI(
    title="WattLab - Simulador de Consumo Energético",
    description="Aplicación web con FastAPI y Jinja2 para estimar y optimizar consumo eléctrico.",
    version="1.0.0",
)

DEFAULT_FORM_VALUES = {
    "device_name": "Aire acondicionado split inverter",
    "watts": "1200",
    "hours_per_day": "8",
    "days_per_month": "30",
    "tariff_cop_per_kwh": "850",
    "reduction_percent": "20",
}


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok", "service": "WattLab"}


@app.get("/", response_class=HTMLResponse)
def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "form": DEFAULT_FORM_VALUES,
            "errors": [],
            "result": None,
        },
    )


@app.post("/simulate", response_class=HTMLResponse)
def run_simulation(
    request: Request,
    device_name: str = Form(...),
    watts: str = Form(...),
    hours_per_day: str = Form(...),
    days_per_month: str = Form(...),
    tariff_cop_per_kwh: str = Form(...),
    reduction_percent: str = Form("20"),
) -> HTMLResponse:
    form_values = {
        "device_name": device_name,
        "watts": watts,
        "hours_per_day": hours_per_day,
        "days_per_month": days_per_month,
        "tariff_cop_per_kwh": tariff_cop_per_kwh,
        "reduction_percent": reduction_percent,
    }

    errors: list[str] = []
    try:
        sim_input = SimulationInput(
            device_name=device_name,
            watts=float(watts),
            hours_per_day=float(hours_per_day),
            days_per_month=int(float(days_per_month)),
            tariff_cop_per_kwh=float(tariff_cop_per_kwh),
            reduction_percent=float(reduction_percent),
        )
        result = simulate_energy(sim_input)
    except ValueError as exc:
        if "could not convert string to float" in str(exc) or "invalid literal" in str(exc):
            errors = ["Asegúrate de ingresar valores numéricos válidos en potencia, horas, días, tarifa y reducción."]
        else:
            errors = [msg.strip() for msg in str(exc).split("|") if msg.strip()]
        result = None

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "form": form_values,
            "errors": errors,
            "result": result,
        },
    )