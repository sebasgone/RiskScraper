from typing import List

from fastapi import Depends, FastAPI, HTTPException

from app.models.records import BlackRecords
from app.scrapers.world_bank import WorldBankScraper

app = FastAPI(title="Wolrd Bank Black-List API")

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
    Busca 'name' en la lista de empresas inhabilitadas del World Bank.
    La tabla se refresca cada 3 horas según la web de world bank.
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
    Devuelve la tabla de World Bank en formato JSON:
      - index: lista de índices
      - columns: lista de nombres de campos
      - data: lista de registros (filas)
    """
    # Se valida que la tabla esté cargada
    await sb.refresh_if_needed()

    df = sb.table

    return df.to_dict(orient="split")
