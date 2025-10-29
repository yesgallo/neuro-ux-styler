import json

# Cargar datos reales
with open('data/training_data.json', 'r', encoding='utf-8') as f:
    real_data = json.load(f)

# Cargar datos sintéticos
with open('data/synthetic_data.json', 'r', encoding='utf-8') as f:
    synthetic_data = json.load(f)

# Combinar
combined = {
    "training_data": real_data["training_data"] + synthetic_data["training_data"],
    "feedback_data": []
}

# Guardar
with open('data/combined_training_data.json', 'w', encoding='utf-8') as f:
    json.dump(combined, f, ensure_ascii=False, indent=2)

print(f"✅ Combinado: {len(combined['training_data'])} ejemplos totales")