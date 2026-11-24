from dataclasses import dataclass


@dataclass(frozen=True)
class SimulationInput:
    device_name: str
    watts: float
    hours_per_day: float
    days_per_month: int
    tariff_cop_per_kwh: float
    reduction_percent: float = 20.0


@dataclass(frozen=True)
class SimulationResult:
    device_name: str
    daily_kwh: float
    monthly_kwh: float
    monthly_cost_cop: float
    monthly_co2_kg: float
    optimized_monthly_kwh: float
    optimized_monthly_cost_cop: float
    monthly_savings_cop: float
    annual_savings_cop: float
    efficiency_rating: str


CO2_KG_PER_KWH = 0.165


def validate_simulation_input(data: SimulationInput) -> list[str]:
    errors: list[str] = []

    if not data.device_name or not data.device_name.strip():
        errors.append("El nombre del equipo o escenario no puede estar vacío.")
    elif len(data.device_name.strip()) > 80:
        errors.append("El nombre del equipo no debe superar los 80 caracteres.")

    if data.watts <= 0 or data.watts > 50000:
        errors.append("La potencia debe ser mayor que 0 W y menor o igual a 50,000 W.")

    if data.hours_per_day <= 0 or data.hours_per_day > 24:
        errors.append("Las horas de uso diario deben estar entre 0.1 y 24 horas.")

    if data.days_per_month < 1 or data.days_per_month > 31:
        errors.append("Los días al mes deben estar entre 1 y 31.")

    if data.tariff_cop_per_kwh <= 0 or data.tariff_cop_per_kwh > 10000:
        errors.append("La tarifa por kWh debe ser mayor que 0 y menor o igual a 10,000 COP.")

    if data.reduction_percent < 0 or data.reduction_percent > 90:
        errors.append("El porcentaje de optimización debe estar entre 0% y 90%.")

    return errors


def classify_efficiency(monthly_kwh: float) -> str:
    if monthly_kwh < 25:
        return "Bajo"
    if monthly_kwh < 90:
        return "Moderado"
    if monthly_kwh < 200:
        return "Alto"
    return "Crítico"


def simulate_energy(data: SimulationInput) -> SimulationResult:
    errors = validate_simulation_input(data)
    if errors:
        raise ValueError(" | ".join(errors))

    clean_name = data.device_name.strip()
    daily_kwh = (data.watts * data.hours_per_day) / 1000.0
    monthly_kwh = daily_kwh * data.days_per_month
    monthly_cost_cop = monthly_kwh * data.tariff_cop_per_kwh
    monthly_co2_kg = monthly_kwh * CO2_KG_PER_KWH

    factor_keep = 1.0 - (data.reduction_percent / 100.0)
    optimized_monthly_kwh = monthly_kwh * factor_keep
    optimized_monthly_cost_cop = optimized_monthly_kwh * data.tariff_cop_per_kwh
    monthly_savings_cop = monthly_cost_cop - optimized_monthly_cost_cop
    annual_savings_cop = monthly_savings_cop * 12.0

    return SimulationResult(
        device_name=clean_name,
        daily_kwh=round(daily_kwh, 3),
        monthly_kwh=round(monthly_kwh, 2),
        monthly_cost_cop=round(monthly_cost_cop, 2),
        monthly_co2_kg=round(monthly_co2_kg, 2),
        optimized_monthly_kwh=round(optimized_monthly_kwh, 2),
        optimized_monthly_cost_cop=round(optimized_monthly_cost_cop, 2),
        monthly_savings_cop=round(monthly_savings_cop, 2),
        annual_savings_cop=round(annual_savings_cop, 2),
        efficiency_rating=classify_efficiency(monthly_kwh),
    )