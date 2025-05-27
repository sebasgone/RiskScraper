from typing import List

from fastapi.middleware.cors import CORSMiddleware
from fastapi import Depends, FastAPI, HTTPException

from app.models.records import BlackRecords
from app.scrapers.world_bank import WorldBankScraper

app = FastAPI(title="World Bank Black-List API")

# Middleware CORS para permitir peticiones desde cualquier origen.
# En producción se recomienda restringir los orígenes permitidos (allow_origins) por seguridad.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #  Permitir solicitudes desde el frontend en 5174
    allow_credentials=True,
    allow_methods=["*"],  #  Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  #  Permitir todos los headers
)


# Única instancia del scraper en memoria
scraper = WorldBankScraper()


@app.on_event("startup")
async def startup_event():
    # Descarga de inicialización de blacklist
    await scraper.refresh_if_needed()


# Dependencia de inyección para el scraper
def get_scraper() -> WorldBankScraper:
    return scraper


# Endpoint de búsqueda principal
@app.get("/search/worldbank", response_model=List[BlackRecords])
async def search_worldbank(
    name: str, bank_scraper: WorldBankScraper = Depends(get_scraper)
):
    """
    Busca un nombre en la lista negra del Banco Mundial.

    Parámetros:
    - name (str): Nombre o fragmento de nombre a buscar en la lista negra del Banco Mundial.

    Retorna:
    - Lista de coincidencias con los registros encontrados.
    """

    try:
        filter_data = await bank_scraper.search(name)
    except Exception as e:
        # En caso de que el scraper falle
        raise HTTPException(status_code=502, detail=str(e))
    return filter_data


# Endpoint de status para validar actividad del servicio
@app.get("/health")
def health():
    """
    Endpoint para validar que el servicio está activo.

    Usado para debbuging.
    """
    return {
        "status": "ok",
        "last_fetched": (
            scraper.last_fetched.isoformat() if scraper.last_fetched else None
        ),
    }


# Endpoint de debug para validar descarga de datos
@app.get("/debug/raw")
async def debug_raw(sb: WorldBankScraper = Depends(get_scraper)):
    """
    Retorna la tabla original obtenida del Banco Mundial en formato JSON.

    Este endpoint fue usado para validación y debugging.
    """
    # Se valida que la tabla esté cargada
    await sb.refresh_if_needed()

    df = sb.table

    return df.to_dict(orient="split")
