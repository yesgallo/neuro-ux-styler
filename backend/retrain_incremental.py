import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
backend_dir = os.path.dirname(current_dir) if 'backend' in current_dir else current_dir
sys.path.insert(0, backend_dir)

try:
    from training import Trainer
except ImportError:
    try:
        from backend.training import Trainer
    except ImportError as e:
        print(f"❌ Error importando Trainer: {e}")
        print(f"📁 Directorio actual: {current_dir}")
        print(f"📁 Backend dir: {backend_dir}")
        print(f"📁 sys.path: {sys.path}")
        sys.exit(1)

def main():
    """Ejecuta entrenamiento incremental del modelo"""
    try:
        print("=" * 60)
        print("🧠 NEURO UX STYLER - ENTRENAMIENTO INCREMENTAL")
        print("=" * 60)
        
        trainer = Trainer()
        
        # ✅ Verificar que existe un modelo previo
        model_path = os.path.join(os.path.dirname(__file__), 'data', 'models', 'neuro_ux_model.h5')
        if not os.path.exists(model_path):
            print("⚠️  ADVERTENCIA: No se encontró modelo previo.")
            print("   Se entrenará un modelo nuevo desde cero.")
            response = input("   ¿Deseas continuar? (s/n): ")
            if response.lower() != 's':
                print("❌ Entrenamiento cancelado.")
                return
        
        # ✅ ENTRENAMIENTO INCREMENTAL
        print("\n🔄 Iniciando entrenamiento incremental...")
        history, metrics = trainer.train_model(epochs=30, incremental=True)
        
        print("\n" + "=" * 60)
        print("✅ ENTRENAMIENTO INCREMENTAL COMPLETADO")
        print("=" * 60)
        print(f"🎯 Precisión final: {metrics['accuracy']*100:.1f}%")
        print(f"📉 Loss final: {metrics['loss']:.4f}")
        if 'auc' in metrics:
            print(f"📊 AUC: {metrics['auc']:.4f}")
        print("=" * 60)
        
    except FileNotFoundError as e:
        print(f"\n❌ Error: Archivo no encontrado")
        print(f"   {e}")
        print("\n💡 Sugerencia: Verifica que exista el archivo 'data/combined_training_data.json'")
        sys.exit(1)
        
    except ValueError as e:
        print(f"\n❌ Error de validación: {e}")
        print("\n💡 Sugerencia: Verifica que el dataset tenga suficientes datos válidos")
        sys.exit(1)
        
    except Exception as e:
        print(f"\n❌ Error inesperado durante el entrenamiento:")
        print(f"   {type(e).__name__}: {e}")
        import traceback
        print("\n📋 Traceback completo:")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()