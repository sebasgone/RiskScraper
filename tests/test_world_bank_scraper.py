import httpx
import pandas as pd
import pytest
import respx

from app.scrapers.world_bank import WorldBankScraper

# URL que usa el scraper
WORLD_BANK_URL = WorldBankScraper.BANK_URL


@pytest.fixture(scope="module")
def scraper():
    return WorldBankScraper()


@pytest.mark.asyncio
@respx.mock
async def test_download_all_returns_dataframe(scraper):
    # Prepara un HTML de ejemplo con una sola tabla pequeña
    html = """
    <html><body>
      <table>
        <thead>
          <tr>
            <th>Firm Name</th><th>Address</th><th>Country</th>
            <th>From Date</th><th>To Date</th><th>Grounds</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>ACME Corp</td><td>Addr1</td><td>Peru</td>
            <td>2020-01-01</td><td>2023-01-01</td><td>Fraud</td>
          </tr>
          <tr>
            <td>Beta LLC</td><td>Addr2</td><td>USA</td>
            <td>2021-02-02</td><td>2024-02-02</td><td>Corruption</td>
          </tr>
        </tbody>
      </table>
    </body></html>
    """
    # Mockea la descarga de HTML
    respx.get(WORLD_BANK_URL).mock(return_value=httpx.Response(200, text=html))

    table = await scraper.download_all()
    filtered = await scraper.filter_table(table, "ACME")
    ## Testing download
    assert isinstance(table, pd.DataFrame)
    assert table.shape == (2, 6)
    assert list(table["Firm Name"]) == ["ACME Corp", "Beta LLC"]
    ## Testing filtering
    assert isinstance(filtered, pd.DataFrame)
    assert filtered.shape == (1, 6)
    assert filtered.iloc[0]["Firm Name"] == "ACME Corp"
