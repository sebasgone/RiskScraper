from pydantic import BaseModel, Field


class BlackRecords(BaseModel):
    """
    Modelo que representa un registro de empresa sancionada por el World Bank.
    Cada campo corresponde a una columna de la tabla extraída.
    """
    FIRM_NAME: str = Field(..., description="Nombre de la empresa sancionada")
    CODE: str = Field(..., description="Código de identificación interno")
    ADDRESS: str = Field(..., description="Dirección registrada de la empresa")
    COUNTRY: str = Field(..., description="País de origen de la empresa")
    FROM_DATE: str = Field(..., description="Fecha de inicio de la sanción")
    TO_DATE: str = Field(..., description="Fecha de fin de la sanción (si aplica)")
    GROUNDS: str = Field(..., description="Motivos de la sanción")
