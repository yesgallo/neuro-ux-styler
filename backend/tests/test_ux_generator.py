from app.services.ux_generator import generate_ux_kit

def test_generate_ux_kit():
    input_data = {
        "name": "EcoCart",
        "mission": "Hacer e-commerce sostenible",
        "values": "sostenibilidad, transparencia",
        "audience": "millennials",
        "sector": "e-commerce"
    }
    result = generate_ux_kit(input_data)
    assert "palette" in result
    assert "primary" in result["palette"]
    assert result["palette"]["primary"] == "#10B981"  # según tu paleta