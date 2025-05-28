# 🌍 World Bank Blacklist API

API desarrollada con FastAPI para consultar la lista de empresas inhabilitadas por el Banco Mundial. Extrae los datos en tiempo real mediante web scraping y expone los endpoints para búsqueda y depuración.



## 🚀 Características

- Consulta por nombre en la blacklist del World Bank.
- Actualización automática de datos cada 3 días.
- Documentación Swagger y ReDoc generada automáticamente.
- Endpoint de salud para monitoreo.
- Listo para despliegue local o en producción.

---

## 📦 Requisitos

- Python 3.9+
- pip
- Navegador Chromium (automáticamente gestionado por Playwright)

---

## ⚙️ Instalación

### Clona el repositorio
```bash
git clone https://github.com/sebasgone/RiskScraper.git
```
### Crea un entorno virtual
```bash
python -m venv venv
source venv/bin/activate  
```
### Instala dependencias
```bash
pip install -r requirements.txt
```
### Instala browsers para Playwright
```bash
playwright install
```
### Ejecución local
```bash
uvicorn main:app --reload
```

## Documentación interactiva de API

**Swagger UI:** http://localhost:8000/docs
**ReDoc:** http://localhost:8000/redoc

## 📡 Endpoints principales

- 'GET /search/worldbank': Busca por nombre en la lista negra del World Bank
- 'GET /health': Verifica estado y fecha de última descarga
- 'GET /debug/raw': Devuelve la tabla completa en formato JSON (debug)

## 📁 Estructura del proyecto

```
├── main.py                  # App principal con endpoints
├── app/
│   ├── models/              # Modelos Pydantic
│   │   └── records.py
│   └── scrapers/            # Lógica de scraping
│       └── world_bank.py
├── .env                     # Variables de entorno incluidas
├── requirements.txt         # Dependencias
├── README.md
```
# ✍️ Autor
Sebastián García Tolentino
AI Developer
https://www.linkedin.com/in/sebasgone21/
