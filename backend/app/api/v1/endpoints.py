from fastapi import APIRouter
from app.models.brand import BrandInput
from app.services.ux_generator import generate_ux_kit

router = APIRouter()

@router.post("/generate")
def generate_kit(input: BrandInput):
    result = generate_ux_kit(input.dict())
    return result