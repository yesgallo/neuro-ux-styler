"""
Agrega ejemplos corporativos/tradicionales al dataset
"""
import json
import os
import random

def generate_corporate_examples(count=30):
    """Genera ejemplos de diseños corporativos buenos"""
    
    corporate_palettes = [
        ["#003366", "#336699", "#FFFFFF"],  # Azul corporativo
        ["#1a1a2e", "#16213e", "#0f3460"],  # Azul oscuro profesional
        ["#2C3E50", "#34495E", "#ECF0F1"],  # Gris azulado
        ["#004d40", "#00796b", "#ffffff"],  # Verde corporativo
        ["#1565C0", "#1976D2", "#E3F2FD"],  # Azul tecnológico
    ]
    
    corporate_fonts = [
        ["Georgia", "Helvetica"],
        ["Times New Roman", "Arial"],
        ["Garamond", "Calibri"],
        ["Palatino", "Verdana"],
    ]
    
    corporate_layouts = ["sidebar", "grid", "flex"]
    corporate_spacing = ["compact", "standard", "medium"]
    corporate_contrast = ["medium", "medium-high", "high"]
    
    examples = []
    for _ in range(count):
        example = {
            "input": {
                "palette": random.choice(corporate_palettes),
                "fonts": random.choice(corporate_fonts),
                "layout": random.choice(corporate_layouts),
                "spacing": random.choice(corporate_spacing),
                "contrast": random.choice(corporate_contrast)
            },
            "rating": random.uniform(0.65, 0.85),  # Buenos pero no excelentes
            "category": "corporate-good"
        }
        examples.append(example)
    
    return examples

def add_to_dataset():
    """Agrega ejemplos corporativos al dataset existente"""
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'combined_training_data.json')
    
    if not os.path.exists(data_path):
        print("❌ No se encontró combined_training_data.json")
        return
    
    # Cargar dataset actual
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Generar ejemplos corporativos
    corporate_examples = generate_corporate_examples(30)
    
    # Agregar al dataset
    if isinstance(data, dict):
        if 'training_data' in data:
            data['training_data'].extend(corporate_examples)
        else:
            data['training_data'] = corporate_examples
    else:
        # Si es lista, convertir a objeto
        data = {
            'training_data': data + corporate_examples,
            'feedback_data': [],
            'pending_feedback': []
        }
    
    # Guardar
    with open(data_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    total = len(data['training_data']) if isinstance(data, dict) else len(data)
    print(f"✅ Agregados 30 ejemplos corporativos")
    print(f"📊 Total en dataset: {total} ejemplos")
    print("\n💡 Ahora ejecuta: python retrain_incremental.py")

if __name__ == "__main__":
    print("=" * 60)
    print("🏢 AGREGANDO EJEMPLOS CORPORATIVOS AL DATASET")
    print("=" * 60)
    add_to_dataset()