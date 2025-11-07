"""
Generador de datos sintéticos BALANCEADOS para entrenamiento de UX
Incluye ejemplos BUENOS y MALOS para que el modelo aprenda a diferenciar
"""
import json
import random
import os

# Datos base para generar ejemplos
PALETTES = {
    "good": [
        ["#000000", "#FFFFFF", "#3498DB"],  # Clásico B/N con azul
        ["#2C3E50", "#ECF0F1", "#E74C3C"],  # Slate con rojo
        ["#1ABC9C", "#FFFFFF", "#34495E"],  # Turquesa profesional
        ["#F39C12", "#FFFFFF", "#2C3E50"],  # Naranja moderno
        ["#9B59B6", "#FFFFFF", "#2C3E50"],  # Púrpura elegante
    ],
    "bad": [
        ["#FF00FF", "#FFFF00", "#00FFFF"],  # Colores chillones
        ["#FF0000", "#00FF00", "#0000FF"],  # RGB puro (muy saturado)
        ["#8B4513", "#556B2F", "#2F4F4F"],  # Tonos oscuros sin contraste
        ["#FFC0CB", "#FFB6C1", "#FFE4E1"],  # Demasiado pastel
        ["#000000", "#111111", "#222222"],  # Sin contraste
    ]
}

FONTS = {
    "good": [
        ["Roboto", "Open Sans"],
        ["Montserrat", "Lato"],
        ["Inter", "Source Sans Pro"],
        ["Poppins", "Nunito"],
        ["Work Sans", "IBM Plex Sans"],
    ],
    "bad": [
        ["Comic Sans MS", "Papyrus"],
        ["Curlz MT", "Jokerman"],
        ["Impact", "Courier New"],
        ["Times New Roman", "Arial"],  # No combina bien
        ["Brush Script", "Lucida Handwriting"],
    ]
}

LAYOUTS = {
    "good": ["grid", "flex", "masonry", "card-based"],
    "bad": ["table", "frame", "absolute", "inline"]
}

SPACING = {
    "good": ["medium", "wide", "comfortable"],
    "bad": ["none", "cramped", "excessive"]
}

CONTRAST = {
    "good": ["high", "medium-high", "accessible"],
    "bad": ["low", "none", "inverted"]
}

def generate_good_example():
    """Genera un ejemplo de BUEN diseño UX"""
    return {
        "input": {
            "palette": random.choice(PALETTES["good"]),
            "fonts": random.choice(FONTS["good"]),
            "layout": random.choice(LAYOUTS["good"]),
            "spacing": random.choice(SPACING["good"]),
            "contrast": random.choice(CONTRAST["good"])
        },
        "rating": random.uniform(0.75, 1.0),  # Buenos: 0.75-1.0
        "category": "good"
    }

def generate_bad_example():
    """Genera un ejemplo de MAL diseño UX"""
    return {
        "input": {
            "palette": random.choice(PALETTES["bad"]),
            "fonts": random.choice(FONTS["bad"]),
            "layout": random.choice(LAYOUTS["bad"]),
            "spacing": random.choice(SPACING["bad"]),
            "contrast": random.choice(CONTRAST["bad"])
        },
        "rating": random.uniform(0.1, 0.4),  # Malos: 0.1-0.4
        "category": "bad"
    }

def generate_mixed_example():
    """Genera un ejemplo MIXTO (algunos aspectos buenos, otros malos)"""
    # Mezclar elementos buenos y malos
    is_mostly_good = random.random() > 0.5
    
    if is_mostly_good:
        # Mayoría bueno, algunos malos
        example = {
            "input": {
                "palette": random.choice(PALETTES["good"]),
                "fonts": random.choice(FONTS["good"]),
                "layout": random.choice(LAYOUTS["good"]),
                "spacing": random.choice(SPACING["bad"]),  # Un aspecto malo
                "contrast": random.choice(CONTRAST["good"])
            },
            "rating": random.uniform(0.5, 0.75),  # Regular-bueno
            "category": "mixed-good"
        }
    else:
        # Mayoría malo, algunos buenos
        example = {
            "input": {
                "palette": random.choice(PALETTES["bad"]),
                "fonts": random.choice(FONTS["bad"]),
                "layout": random.choice(LAYOUTS["bad"]),
                "spacing": random.choice(SPACING["good"]),  # Un aspecto bueno
                "contrast": random.choice(CONTRAST["bad"])
            },
            "rating": random.uniform(0.3, 0.5),  # Malo-regular
            "category": "mixed-bad"
        }
    
    return example

def generate_balanced_dataset(total=300):
    """
    Genera un dataset balanceado con distribución realista:
    - 40% buenos (rating 0.75-1.0)
    - 30% malos (rating 0.1-0.4)
    - 30% mixtos (rating 0.3-0.75)
    """
    dataset = []
    
    # Calcular cantidades
    n_good = int(total * 0.40)
    n_bad = int(total * 0.30)
    n_mixed = total - n_good - n_bad
    
    print(f"📊 Generando dataset balanceado:")
    print(f"   - Buenos: {n_good}")
    print(f"   - Malos: {n_bad}")
    print(f"   - Mixtos: {n_mixed}")
    print(f"   - Total: {total}")
    
    # Generar buenos
    for _ in range(n_good):
        dataset.append(generate_good_example())
    
    # Generar malos
    for _ in range(n_bad):
        dataset.append(generate_bad_example())
    
    # Generar mixtos
    for _ in range(n_mixed):
        dataset.append(generate_mixed_example())
    
    # Mezclar aleatoriamente
    random.shuffle(dataset)
    
    return dataset

def save_dataset(dataset, filename="balanced_training_data.json"):
    """Guarda el dataset en formato estructurado"""
    data_dir = os.path.join(os.path.dirname(__file__), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    filepath = os.path.join(data_dir, filename)
    
    # Guardar en formato estructurado
    structured_data = {
        "training_data": dataset,
        "feedback_data": [],
        "pending_feedback": []
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(structured_data, f, indent=2, ensure_ascii=False)
    
    print(f"\n✅ Dataset guardado en: {filepath}")
    return filepath

def show_statistics(dataset):
    """Muestra estadísticas del dataset generado"""
    import numpy as np
    
    ratings = [item['rating'] for item in dataset]
    ratings_array = np.array(ratings)
    
    print("\n" + "=" * 60)
    print("📈 ESTADÍSTICAS DEL DATASET GENERADO")
    print("=" * 60)
    
    print(f"\n📊 Ratings:")
    print(f"   - Mínimo: {ratings_array.min():.3f}")
    print(f"   - Máximo: {ratings_array.max():.3f}")
    print(f"   - Promedio: {ratings_array.mean():.3f}")
    print(f"   - Desv. Estándar: {ratings_array.std():.3f}")
    
    print(f"\n📊 Distribución:")
    ranges = [
        (0.0, 0.3, "Malo"),
        (0.3, 0.5, "Regular"),
        (0.5, 0.7, "Bueno"),
        (0.7, 0.9, "Muy bueno"),
        (0.9, 1.1, "Excelente")
    ]
    
    for min_r, max_r, label in ranges:
        count = np.sum((ratings_array >= min_r) & (ratings_array < max_r))
        percentage = (count / len(ratings)) * 100
        bar = "█" * int(percentage / 5)
        print(f"   {label:15s} {bar:20s} {count:3d} ({percentage:5.1f}%)")
    
    print(f"\n📊 Clases (threshold=0.7):")
    buenos = np.sum(ratings_array >= 0.7)
    malos = len(ratings) - buenos
    print(f"   - Buenos (≥0.7): {buenos} ({buenos/len(ratings)*100:.1f}%)")
    print(f"   - Malos (<0.7): {malos} ({malos/len(ratings)*100:.1f}%)")

def main():
    print("=" * 60)
    print("🎨 GENERADOR DE DATOS BALANCEADOS PARA UX")
    print("=" * 60)
    
    # Generar dataset
    dataset = generate_balanced_dataset(total=300)
    
    # Mostrar estadísticas
    show_statistics(dataset)
    
    # Guardar
    save_dataset(dataset, "balanced_training_data.json")
    
    print("\n" + "=" * 60)
    print("✅ DATASET BALANCEADO CREADO")
    print("=" * 60)
    print("\n💡 Próximos pasos:")
    print("   1. Reemplaza 'combined_training_data.json' con este nuevo dataset")
    print("   2. Ejecuta: python training.py")
    print("   3. Prueba: python test_model.py")
    print("=" * 60)

if __name__ == "__main__":
    main()