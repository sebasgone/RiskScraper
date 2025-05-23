import os
from datetime import datetime, timedelta

import pandas as pd
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from playwright.async_api import async_playwright

load_dotenv()


class WorldBankScraper:

    BANK_URL = os.getenv("FONT_URL_WORLD_BANK")
    SELECTOR_BODY_TABLE_BANK = os.getenv("SELECTOR_BODY_TABLE_BANK")
    table: pd.DataFrame = pd.DataFrame()
    last_fetched: datetime | None = None
    period_refresh = timedelta(days=3)

    async def fetch_html(
        self, url: str, params: dict | None = None, headers: dict | None = None
    ) -> BeautifulSoup:
        """
        Realiza una petición GET asíncrona a `url` con params/headers,
        lanza excepción si el status no es 200,
        y devuelve un objeto BeautifulSoup del HTML recibido.
        """
        # Arranca un browser headless para extraer tabla una vez cargada
        async with async_playwright() as pw:
            browser = await pw.chromium.launch(headless=True)
            page = await browser.new_page()

            # Navega la url y espera a que la tabla aparezca
            await page.goto(url)

            # Inspección para extracción del objeto beatiful soup de la tabla
            await page.wait_for_selector(self.SELECTOR_BODY_TABLE_BANK)

            # captura html ya renderizado por javascript, completamente cargado
            loaded_html = await page.content()
            await browser.close()

            return BeautifulSoup(loaded_html, "lxml")

    async def refresh_if_needed(self):

        current_time = datetime.utcnow()

        if self.last_fetched is None or (
            current_time - self.last_fetched > self.period_refresh
        ):
            full_html = await self.fetch_html(self.BANK_URL)
            rows = full_html.select(self.SELECTOR_BODY_TABLE_BANK)
            # Extraer formateado en el tipo Dataframe la tabla completa
            records = []
            for row in rows:
                # Cada td[role="gridcell"] es una celda de tu tabla
                cols = row.select('td[role="gridcell"]')
                # Extraes el texto interior de cada <td>
                values = [td.get_text(strip=True).upper() for td in cols]
                records.append(values)

            cols_names = [
                "FIRM_NAME",
                "CODE",
                "ADDRESS",
                "COUNTRY",
                "FROM_DATE",
                "TO_DATE",
                "GROUNDS",
            ]

            self.table = pd.DataFrame(records, columns=cols_names)

            self.last_fetched = current_time

    async def search(self, query: str):
        # Garantizamos datos actualizados
        await self.refresh_if_needed()
        # Filtro y máscara por consulta
        bool_df = self.table.astype(str).apply(
            lambda col: col.str.contains(query.upper(), case=False, na=False)
        )
        mask = bool_df.any(axis=1)
        df = self.table[mask]

        return df.to_dict(orient="records")
