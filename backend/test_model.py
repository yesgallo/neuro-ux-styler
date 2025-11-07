"""
Script para probar el modelo entrenado con ejemplos
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from model import NeuroUXModel
from data_processor import DataProcessor

def test_predictions():
    """Prueba el modelo con diferentes inputs"""
    
    print("=" * 60)
    print("🧪 PROBANDO MODELO NEURO UX STYLER")
    print("=" * 60)
    
    # Cargar modelo y procesador
    model = NeuroUXModel()
    processor = DataProcessor()
    
    # Verificar que el modelo esté cargado
    if not os.path.exists(model.model_path):
        print("❌ Error: No se encontró el modelo entrenado")
        print(f"   Buscado en: {model.model_path}")
        print("\n💡 Ejecuta primero: python training.py")
        return
    
    model.load_model()
    
    # Casos de prueba
    test_cases = [
        {
            "name": "Diseño Moderno Minimalista",
            "input": {
                "palette": ["#000000", "#FFFFFF", "#FF6B6B"],
                "fonts": ["Inter", "Helvetica"],
                "layout": "grid",
                "spacing": "medium",
                "contrast": "high"
            }
        },
        {
            "name": "Diseño Corporativo Tradicional",
            "input": {
                "palette": ["#003366", "#336699", "#FFFFFF"],
                "fonts": ["Georgia", "Times New Roman"],
                "layout": "sidebar",
                "spacing": "compact",
                "contrast": "medium"
            }
        },
        {
            "name": "Diseño Creativo Vibrante",
            "input": {
                "palette": ["#FF1744", "#00E676", "#2979FF"],
                "fonts": ["Montserrat", "Poppins"],
                "layout": "masonry",
                "spacing": "wide",
                "contrast": "high"
            }
        },
        {
            "name": "Diseño E-commerce Limpio",
            "input": {
                "palette": ["#FFFFFF", "#F5F5F5", "#4CAF50"],
                "fonts": ["Roboto", "Open Sans"],
                "layout": "grid",
                "spacing": "medium",
                "contrast": "medium"
            }
        }
    ]
    
    print("\n🔍 Evaluando diferentes diseños...\n")
    
    results = []
    for i, test in enumerate(test_cases, 1):
        # Procesar input - ✅ CORREGIDO: Ahora son 3 valores, no 4
        features, metadata, _ = processor.encode_input(test["input"])
        
        # Hacer predicción
        prediction = model.predict(features)[0][0]
        
        # Interpretar resultado
        quality = "Excelente" if prediction > 0.8 else \
                  "Bueno" if prediction > 0.6 else \
                  "Regular" if prediction > 0.4 else \
                  "Mejorable"
        
        emoji = "🌟" if prediction > 0.8 else \
                "✅" if prediction > 0.6 else \
                "⚠️" if prediction > 0.4 else \
                "❌"
        
        results.append({
            "name": test["name"],
            "score": prediction,
            "quality": quality,
            "emoji": emoji
        })
        
        print(f"{emoji} Test {i}: {test['name']}")
        print(f"   Score: {prediction:.2%}")
        print(f"   Calidad: {quality}")
        print()
    
    # Resumen
    print("=" * 60)
    print("📊 RESUMEN DE RESULTADOS")
    print("=" * 60)
    
    # Ordenar por score
    results.sort(key=lambda x: x['score'], reverse=True)
    
    print("\n🏆 Ranking de diseños:")
    for i, result in enumerate(results, 1):
        bar = "█" * int(result['score'] * 20)
        print(f"{i}. {result['emoji']} {result['name']}")
        print(f"   {bar} {result['score']:.1%}")
    
    avg_score = sum(r['score'] for r in results) / len(results)
    print(f"\n📈 Score promedio: {avg_score:.1%}")
    
    print("\n" + "=" * 60)
    print("✅ Pruebas completadas")
    print("=" * 60)

def test_custom_input():
    """Permite probar con un input personalizado"""
    print("\n" + "=" * 60)
    print("🎨 PRUEBA PERSONALIZADA")
    print("=" * 60)
    
    model = NeuroUXModel()
    processor = DataProcessor()
    model.load_model()
    
    # Ejemplo de input personalizado
    custom_input = {
        "palette": ["#1a1a1a", "#ffffff", "#ff4081"],
        "fonts": ["Montserrat", "Lato"],
        "layout": "grid",
        "spacing": "wide",
        "contrast": "high"
    }
    
    print("\n📝 Input de prueba:")
    print(f"   Paleta: {custom_input['palette']}")
    print(f"   Fuentes: {custom_input['fonts']}")
    print(f"   Layout: {custom_input['layout']}")
    print(f"   Espaciado: {custom_input['spacing']}")
    print(f"   Contraste: {custom_input['contrast']}")
    
    # Procesar y predecir
    features, _, _, _ = processor.encode_input(custom_input)
    prediction = model.predict(features)[0][0]
    
    print(f"\n🎯 Resultado: {prediction:.2%}")
    
    if prediction > 0.8:
        print("   ⭐ ¡Diseño excelente! Muy recomendado")
    elif prediction > 0.6:
        print("   ✅ Buen diseño, cumple con los estándares")
    elif prediction > 0.4:
        print("   ⚠️ Diseño regular, considera mejoras")
    else:
        print("   ❌ Diseño mejorable, revisa los principios de UX")

if __name__ == "__main__":
    # Ejecutar pruebas predefinidas
    test_predictions()
    
    # Opcional: descomentar para probar input personalizado
    # test_custom_input()