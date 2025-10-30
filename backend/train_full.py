import os
import json
import random
import numpy as np
from sklearn.model_selection import train_test_split
from model import NeuroUXModel
from data_processor import DataProcessor

# === 1. GENERAR DATOS SINTÉTICOS DE ALTA CALIDAD ===
def generate_synthetic_data(num_samples=100):
    """Genera datos sintéticos con ratings altos (0.8–1.0)"""
    NAMES = [
        "TechFlow", "GreenRoots", "MindfulHR", "NovaLabs", "UrbanRide", "ArtisanCraft",
        "EduFuture", "ZenSpace", "CryptoTrust", "BloomKids", "SkylineBuild", "PulseHealth",
        "StyleHive", "DataShield", "TerraFarms", "SoundScape", "LegalEase", "GlowBeauty"
    ]
    
    MISSIONS = [
        "Innovación {sector} para el futuro",
        "Soluciones {sector} con enfoque en {value1} y {value2}",
        "Transformar el {sector} mediante {value1}",
        "Experiencias {sector} diseñadas para {audience}",
        "Impulsar el crecimiento de {audience} con {value1}"
    ]
    
    VALUES = [
        "innovación", "tecnología", "excelencia", "sostenibilidad", "calidad", "confianza",
        "creatividad", "eficiencia", "transparencia", "seguridad", "accesibilidad", "ética"
    ]
    
    SECTORS = [
        "tecnología", "salud", "finanzas", "educación", "moda", "alimentos", "medio ambiente",
        "fitness", "diseño", "recursos humanos", "ciencia", "movilidad", "arte", "música"
    ]
    
    AUDIENCES = [
        "empresas B2B", "consumidores conscientes", "jóvenes urbanos", "familias",
        "emprendedores", "instituciones académicas", "clientes premium"
    ]

    synthetic = []
    for _ in range(num_samples):
        sector = random.choice(SECTORS)
        audience = random.choice(AUDIENCES)
        value1, value2 = random.sample(VALUES, 2)
        
        mission = random.choice(MISSIONS).format(
            sector=sector,
            audience=audience,
            value1=value1,
            value2=value2
        )
        
        values = ", ".join(random.sample(VALUES, random.randint(3, 5)))
        
        synthetic.append({
            "input": {
                "name": random.choice(NAMES),
                "mission": mission,
                "values": values,
                "sector": sector,
                "audience": audience
            },
            "rating": round(random.uniform(0.85, 1.0), 2),  # Rating alto
            "feedback": "excelente"
        })
    
    return synthetic

# === 2. CARGAR DATOS REALES ===
def load_real_data(data_path):
    """Carga datos reales: training + feedback + pending"""
    if not os.path.exists(data_path):
        return [], [], []
    
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    training = data.get('training_data', [])
    feedback = data.get('feedback_data', [])
    pending = data.get('pending_feedback', [])
    
    return training, feedback, pending

# === 3. ENTRENAMIENTO COMPLETO ===
def train_full_model():
    print("=" * 60)
    print("🧠 NEURO UX STYLER - ENTRENAMIENTO COMPLETO")
    print("=" * 60)
    
    # Rutas
    data_path = 'data/combined_training_data.json'
    model_path = 'neuro_ux_model.keras'
    
    # Cargar datos reales
    training_data, feedback_data, pending_feedback = load_real_data(data_path)
    print(f"✅ Datos reales cargados:")
    print(f"   - Training: {len(training_data)}")
    print(f"   - Feedback usados: {len(feedback_data)}")
    print(f"   - Feedback pendientes: {len(pending_feedback)}")
    
    # Generar datos sintéticos
    synthetic_data = generate_synthetic_data(num_samples=150)
    print(f"✨ Datos sintéticos generados: {len(synthetic_data)} (ratings altos)")
    
    # Combinar TODO
    all_data = training_data + feedback_data + pending_feedback + synthetic_data
    print(f"📊 Total de muestras para entrenamiento: {len(all_data)}")
    
    if len(all_data) < 20:
        print("❌ No hay suficientes datos. Añade más ejemplos.")
        return
    
    # Preparar features
    processor = DataProcessor()
    X, y = [], []
    
    for item in all_data:
        try:
            features, _, _, _ = processor.encode_input(item['input'])
            X.append(features[0])
            y.append(item.get('rating', 0.5))
        except Exception as e:
            print(f"⚠️ Error al procesar item: {e}")
            continue
    
    X = np.array(X)
    y = np.array(y)
    print(f"✅ Features preparados: {X.shape}")
    
    # Dividir
    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    
    # Entrenar
    print("\n🚀 Iniciando entrenamiento...")
    model = NeuroUXModel()
    history = model.train(X_train, y_train, X_val, y_val, epochs=120)
    metrics = model.evaluate(X_val, y_val)
    
    # Guardar
    model.save_model()
    
    print("\n" + "="*60)
    print("✅ ENTRENAMIENTO COMPLETO FINALIZADO")
    print("="*60)
    print(f"🎯 Precisión: {metrics['accuracy']*100:.2f}%")
    print(f"📉 Pérdida: {metrics['loss']:.4f}")
    print(f"📈 AUC: {metrics.get('auc', 0.0):.4f}")
    print(f"💾 Modelo guardado en: {model_path}")
    
    # Vaciar feedbacks pendientes (opcional)
    if os.path.exists(data_path):
        with open(data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        data['pending_feedback'] = []
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print("🗑️ Feedbacks pendientes limpiados (listos para nuevos)")

if __name__ == "__main__":
    train_full_model()