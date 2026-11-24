# WattLab - Simulador de Consumo y Costo Energético

## 1. Presentación del proyecto
- **Nombre de la aplicación:** WattLab.
- **Propósito:** Estimar el consumo eléctrico diario y mensual, el costo en pesos colombianos (COP), la emisión estimada de CO2 y el ahorro potencial bajo un escenario de optimización.
- **Problema o necesidad:** Muchas personas y pequeños negocios desconocen cuánto representa un equipo o hábito de uso en su factura mensual antes de tomar decisiones de ahorro o eficiencia.
- **Funcionalidad principal:** Recibe parámetros de uso y tarifa mediante un formulario web, valida los datos, calcula métricas energéticas y compara el escenario base frente a uno optimizado.

## 2. Tecnologías utilizadas
- **Python 3.12:** Lenguaje principal para la lógica de cálculo, validación y pruebas.
- **FastAPI:** Framework web para definir rutas (GET y POST), procesar formularios y servir respuestas HTTP.
- **Jinja2:** Motor de plantillas HTML para renderizar formularios, mensajes de validación y resultados dinámicos.
- **pytest y FastAPI TestClient:** Framework de pruebas automatizadas para verificar lógica de negocio, rutas y casos inválidos.
- **Uvicorn:** Servidor ASGI para ejecutar la aplicación en entorno local.

## 3. Arquitectura y organización
- `app/simulator.py`: Contiene la lógica principal (`SimulationInput`, `SimulationResult`, `validate_simulation_input`, `classify_efficiency` y `simulate_energy`).
- `app/main.py`: Define la instancia de FastAPI y las rutas `/health`, `/` y `/simulate`.
- `templates/base.html` y `templates/index.html`: Plantillas Jinja2 con diseño responsivo, formulario y vista de resultados/errores.
- `tests/test_app.py`: Suite de pruebas automatizadas con `pytest`.
- `requirements.txt`: Dependencias del proyecto.

## 4. Funcionamiento de la aplicación
1. El usuario accede a `/` y FastAPI renderiza `index.html` con Jinja2.
2. El usuario envía el formulario mediante `POST /simulate`.
3. `app/main.py` convierte los datos y ejecuta `simulate_energy()` en `app/simulator.py`.
4. Si hay datos inválidos (como potencia menor o igual a 0 o más de 24 horas al día), se captura `ValueError` y Jinja2 muestra los mensajes de error en la interfaz.
5. Si los datos son válidos, se calculan consumo diario/mensual, costo COP, CO2 y escenario optimizado con ahorro mensual y anual, mostrándolos en `index.html`.

## 5. Instalación y ejecución
1. **Requisitos:** Python 3.10 o superior y `pip`.
2. **Crear y activar entorno virtual (PowerShell):** `python -m venv .venv` y `.\.venv\Scripts\Activate.ps1` (previo `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`).
3. **Instalar dependencias:** `pip install -r requirements.txt`.
4. **Iniciar el servidor:** `uvicorn app.main:app --reload`.
5. **Abrir en el navegador:** `http://127.0.0.1:8000`.
6. **Usar la funcionalidad:** Ingresa equipo, potencia (W), horas/día, días/mes, tarifa COP/kWh y porcentaje de reducción, luego haz clic en **Calcular simulación**.

## 6. Pruebas automatizadas
Ejecuta las pruebas desde la raíz del proyecto con `pytest -v`.
- `test_health_route_returns_ok`: Verifica `GET /health` -> espera HTTP 200 y `{"status": "ok", "service": "WattLab"}`.
- `test_home_page_renders_jinja_template`: Verifica `GET /` -> espera HTTP 200 y renderizado HTML de `WattLab`.
- `test_simulate_energy_expected_calculation`: Prueba 100W, 5h/día, 30 días, 800 COP/kWh y 25% de reducción -> espera 15.0 kWh/mes, ,000.0 COP y ,000.0 COP de ahorro mensual.
- `test_post_simulate_invalid_hours_shows_validation_error`: Envía `hours_per_day="30"` a `POST /simulate` -> espera mensaje de error de validación en HTML.
- `test_simulate_energy_raises_on_invalid_watts`: Envía `watts=0` a `simulate_energy` -> espera `ValueError`.

## 7. Evidencias de funcionamiento
- **Interfaz principal:** `![Interfaz principal](docs/interfaz.png)`
- **Validación de entrada inválida:** `![Validación de error](docs/validacion.png)`
- **Resultado del procesamiento:** `![Resultado de simulación](docs/resultado.png)`
- **Pruebas con pytest:** `![Pruebas pytest](docs/pytest.png)`

## 8. Conclusiones
Separar la lógica de cálculo y validación en `app/simulator.py` permitió probar las reglas matemáticas de forma directa y rápida, mientras que `TestClient` facilitó validar el flujo completo de rutas y plantillas Jinja2. Manejar explícitamente los errores de rango y conversión evita fallos inesperados y ofrece retroalimentación clara al usuario.