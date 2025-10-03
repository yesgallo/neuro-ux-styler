from pydantic import BaseModel
from typing import List

class BrandInput(BaseModel):
    name: str
    mission: str
    values: str
    audience: str
    sector: str

class UXKit(BaseModel):
    palette: dict
    typography: dict
    tokens: dict
    explanation: str
    exports: dict  # css, json, figma