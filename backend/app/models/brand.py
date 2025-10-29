from pydantic import BaseModel

class BrandInput(BaseModel):
    name: str
    mission: str
    values: str
    audience: str
    sector: str
