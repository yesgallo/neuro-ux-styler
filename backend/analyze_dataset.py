
import json
import os
import numpy as np
from collections import Counter

def analyze_dataset():
   
    
    print("=" * 60)
    print("🔍 ANÁLISIS DEL DATASET")
    print("=" * 60)
    
    data_path = os.path.join(os.path.dirname(__file__), 'data', 'combined_training_data.json')
    
    if not os.path.exists(data_path):
        print(f"❌ No se encontró: {data_path}")
        return
    
    with open(data_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Manejar ambos formatos
    if isinstance(data, list):
        all_data = data
        print("📄 Formato: Lista directa")
    else:
        training = data.get('training_data', [])
        feedback = data.get('feedback_data', [])
        pending = data.get('pending_feedback', [])
        all_data = training + feedback + pending
        print(f"📄 Formato: Objeto estructurado")
        print(f"   - Training data: {len(training)}")
        print(f"   - Feedback data: {len(feedback)}")
        print(f"   - Pending: {len(pending)}")
    
    print(f"\n📊 Total de ejemplos: {len(all_data)}")
    
    if len(all_data) == 0:
        print("❌ Dataset vacío!")
        return
    
    # Analizar ratings
    print("\n" + "=" * 60)
    print("📈 DISTRIBUCIÓN DE RATINGS")
    print("=" * 60)
    
    ratings = []
    for item in all_data:
        if isinstance(item, dict) and 'rating' in item:
            ratings.append(item['rating'])
    
    if not ratings:
        print("⚠️ No se encontraron ratings en los datos")
        print("\nℹ️ Estructura de ejemplo encontrada:")
        if all_data:
            print(json.dumps(all_data[0], indent=2)[:300])
        return
    
    ratings = np.array(ratings)
    
    print(f"\n📊 Estadísticas de ratings:")
    print(f"   - Mínimo: {ratings.min():.3f}")
    print(f"   - Máximo: {ratings.max():.3f}")
    print(f"   - Promedio: {ratings.mean():.3f}")
    print(f"   - Mediana: {np.median(ratings):.3f}")
    print(f"   - Desv. Estándar: {ratings.std():.3f}")
    
    # Análisis de distribución
    print(f"\n📊 Distribución por rangos:")
    ranges = [
        (0.0, 0.3, "Malo (0.0-0.3)"),
        (0.3, 0.5, "Regular (0.3-0.5)"),
        (0.5, 0.7, "Bueno (0.5-0.7)"),
        (0.7, 0.9, "Muy bueno (0.7-0.9)"),
        (0.9, 1.1, "Excelente (0.9-1.0)")
    ]
    
    for min_r, max_r, label in ranges:
        count = np.sum((ratings >= min_r) & (ratings < max_r))
        percentage = (count / len(ratings)) * 100
        bar = "█" * int(percentage / 5)
        print(f"   {label:25s} {bar:20s} {count:3d} ({percentage:5.1f}%)")
    
    # Análisis de clases (bueno/malo)
    print(f"\n📊 Clasificación binaria (threshold=0.7):")
    buenos = np.sum(ratings >= 0.7)
    malos = len(ratings) - buenos
    print(f"   - Buenos (≥0.7): {buenos} ({buenos/len(ratings)*100:.1f}%)")
    print(f"   - Malos (<0.7): {malos} ({malos/len(ratings)*100:.1f}%)")
    
    # Análisis de variabilidad
    print(f"\n🎯 Análisis de variabilidad:")
    unique_ratings = len(np.unique(ratings))
    print(f"   - Valores únicos de rating: {unique_ratings}")
    
    if ratings.std() < 0.1:
        print("   ⚠️ PROBLEMA: Muy poca variabilidad en los datos")
        print("   💡 Solución: Agrega ejemplos con ratings más diversos")
    elif buenos < 5 or malos < 5:
        print("   ⚠️ PROBLEMA: Dataset desbalanceado")
        print(f"   💡 Solución: Necesitas al menos 5 ejemplos de cada clase")
    else:
        print("   ✅ Variabilidad adecuada")
    
    # Analizar features
    print("\n" + "=" * 60)
    print("🎨 ANÁLISIS DE CARACTERÍSTICAS")
    print("=" * 60)
    
    sample_input = None
    for item in all_data:
        if isinstance(item, dict) and 'input' in item:
            sample_input = item['input']
            break
    
    if sample_input:
        print("\n📝 Estructura de input encontrada:")
        print(json.dumps(sample_input, indent=2, ensure_ascii=False))
        
        # Analizar qué features se están usando
        print(f"\n🔑 Features detectados:")
        for key, value in sample_input.items():
            value_type = type(value).__name__
            value_preview = str(value)[:50]
            print(f"   - {key}: {value_type} = {value_preview}")
    
    # Recomendaciones
    print("\n" + "=" * 60)
    print("💡 RECOMENDACIONES")
    print("=" * 60)
    
    issues = []
    
    if len(all_data) < 50:
        issues.append("Dataset pequeño: Genera más datos sintéticos (recomendado: 100+)")
    
    if ratings.std() < 0.15:
        issues.append("Poca variabilidad: Agrega ejemplos con ratings más extremos (0.0-0.3 y 0.8-1.0)")
    
    if buenos < 10 or malos < 10:
        issues.append("Clases desbalanceadas: Balancea los ejemplos buenos y malos")
    
    if unique_ratings < 10:
        issues.append("Pocos valores únicos: Usa ratings más variados (no solo 0.5, 0.7, etc.)")
    
    if issues:
        for i, issue in enumerate(issues, 1):
            print(f"\n{i}. ⚠️ {issue}")
    else:
        print("\n✅ Tu dataset parece estar bien estructurado")
        print("   El problema puede estar en el DataProcessor o en la arquitectura del modelo")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    analyze_dataset()