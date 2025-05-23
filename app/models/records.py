from pydantic import BaseModel


class BlackRecords(BaseModel):
    FIRM_NAME: str
    CODE: str
    ADDRESS: str
    COUNTRY: str
    FROM_DATE: str
    TO_DATE: str
    GROUNDS: str
