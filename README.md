# WattLab - Simulador de Consumo y Costo EnergÃ©tico

## 1. PresentaciÃ³n del proyecto
- **Nombre de la aplicaciÃ³n:** WattLab.
- **PropÃ³sito:** Estimar el consumo elÃ©ctrico diario y mensual, el costo en pesos colombianos (COP), la emisiÃ³n estimada de CO2 y el ahorro potencial bajo un escenario de optimizaciÃ³n.
- **Problema o necesidad:** Muchas personas y pequeÃ±os negocios desconocen cuÃ¡nto representa un equipo o hÃ¡bito de uso en su factura mensual antes de tomar decisiones de ahorro o eficiencia.
- **Funcionalidad principal:** Recibe parÃ¡metros de uso y tarifa mediante un formulario web, valida los datos, calcula mÃ©tricas energÃ©ticas y compara el escenario base frente a uno optimizado.

## 2. TecnologÃ­as utilizadas
- **Python 3.12:** Lenguaje principal para la lÃ³gica de cÃ¡lculo, validaciÃ³n y pruebas.
- **FastAPI:** Framework web para definir rutas (GET y POST), procesar formularios y servir respuestas HTTP.
- **Jinja2:** Motor de plantillas HTML para renderizar formularios, mensajes de validaciÃ³n y resultados dinÃ¡micos.
- **pytest y FastAPI TestClient:** Framework de pruebas automatizadas para verificar lÃ³gica de negocio, rutas y casos invÃ¡lidos.
- **Uvicorn:** Servidor ASGI para ejecutar la aplicaciÃ³n en entorno local.

## 3. Arquitectura y organizaciÃ³n
- `app/simulator.py`: Contiene la lÃ³gica principal (`SimulationInput`, `SimulationResult`, `validate_simulation_input`, `classify_efficiency` y `simulate_energy`).
- `app/main.py`: Define la instancia de FastAPI y las rutas `/health`, `/` y `/simulate`.
- `templates/base.html` y `templates/index.html`: Plantillas Jinja2 con diseÃ±o responsivo, formulario y vista de resultados/errores.
- `tests/test_app.py`: Suite de pruebas automatizadas con `pytest`.
- `requirements.txt`: Dependencias del proyecto.

## 4. Funcionamiento de la aplicaciÃ³n
1. El usuario accede a `/` y FastAPI renderiza `index.html` con Jinja2.
2. El usuario envÃ­a el formulario mediante `POST /simulate`.
3. `app/main.py` convierte los datos y ejecuta `simulate_energy()` en `app/simulator.py`.
4. Si hay datos invÃ¡lidos (como potencia menor o igual a 0 o mÃ¡s de 24 horas al dÃ­a), se captura `ValueError` y Jinja2 muestra los mensajes de error en la interfaz.
5. Si los datos son vÃ¡lidos, se calculan consumo diario/mensual, costo COP, CO2 y escenario optimizado con ahorro mensual y anual, mostrÃ¡ndolos en `index.html`.

## 5. InstalaciÃ³n y ejecuciÃ³n
1. **Requisitos:** Python 3.10 o superior y `pip`.
2. **Crear y activar entorno virtual (PowerShell):** `python -m venv .venv` y `.\.venv\Scripts\Activate.ps1` (previo `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`).
3. **Instalar dependencias:** `pip install -r requirements.txt`.
4. **Iniciar el servidor:** `uvicorn app.main:app --reload`.
5. **Abrir en el navegador:** `http://127.0.0.1:8000`.
6. **Usar la funcionalidad:** Ingresa equipo, potencia (W), horas/dÃ­a, dÃ­as/mes, tarifa COP/kWh y porcentaje de reducciÃ³n, luego haz clic en **Calcular simulaciÃ³n**.

## 6. Pruebas automatizadas
Ejecuta las pruebas desde la raÃ­z del proyecto con `pytest -v`.
- `test_health_route_returns_ok`: Verifica `GET /health` -> espera HTTP 200 y `{"status": "ok", "service": "WattLab"}`.
- `test_home_page_renders_jinja_template`: Verifica `GET /` -> espera HTTP 200 y renderizado HTML de `WattLab`.
- `test_simulate_energy_expected_calculation`: Prueba 100W, 5h/dÃ­a, 30 dÃ­as, 800 COP/kWh y 25% de reducciÃ³n -> espera 15.0 kWh/mes, ,000.0 COP y ,000.0 COP de ahorro mensual.
- `test_post_simulate_invalid_hours_shows_validation_error`: EnvÃ­a `hours_per_day="30"` a `POST /simulate` -> espera mensaje de error de validaciÃ³n en HTML.
- `test_simulate_energy_raises_on_invalid_watts`: EnvÃ­a `watts=0` a `simulate_energy` -> espera `ValueError`.

## 7. Evidencias de funcionamiento
- **Resultado del procesamiento:** `![Resultado de simulaciÃ³n](docs/resultado.png)`
- **Pruebas con pytest:** `![Pruebas pytest](docs/pytest.png)`

## 8. Conclusiones
Separar la lÃ³gica de cÃ¡lculo y validaciÃ³n en `app/simulator.py` permitiÃ³ probar las reglas matemÃ¡ticas de forma directa y rÃ¡pida, mientras que `TestClient` facilitÃ³ validar el flujo completo de rutas y plantillas Jinja2. Manejar explÃ­citamente los errores de rango y conversiÃ³n evita fallos inesperados y ofrece retroalimentaciÃ³n clara al usuario.
