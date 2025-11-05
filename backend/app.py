from flask import Flask, request, jsonify
from flask_cors import CORS
from model import NeuroUXModel
from data_processor import DataProcessor
from training import Trainer
import os
import traceback

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Inicializar componentes
model = NeuroUXModel()
processor = DataProcessor()
trainer = Trainer()

# Cargar modelo al iniciar
model.load_model()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint de salud"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model.model is not None
    })

@app.route('/api/generate', methods=['POST'])
def generate_ui_kit():
    """Genera un UI Kit basado en los datos de entrada"""
    try:
        data = request.json
        
        required_fields = ['name', 'mission', 'values', 'sector', 'audience']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Campo requerido: {field}'}), 400
        
        features, keywords, sector, audience = processor.encode_input(data)
        prediction = model.predict(features)  # Valor entre 0.0 y 1.0
        confidence = float(prediction[0][0])  # Ya es la confianza
        ui_kit = processor.generate_ui_kit(prediction, keywords, sector, audience)
        ui_kit['confidence'] = confidence  # Guarda la probabilidad directamente
        
        return jsonify({'success': True, 'ui_kit': ui_kit})
        
    except Exception as e:
        print("❌ Error en /generate:", str(e))
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/feedback', methods=['POST'])
def submit_feedback():
    """Recibe feedback del usuario"""
    try:
        data = request.json
        
        input_data = data.get('input_data')
        rating = data.get('rating')  # 0-1
        feedback = data.get('feedback', '')
        
        if not input_data or rating is None:
            return jsonify({
                'error': 'Se requiere input_data y rating'
            }), 400
        
        # Guardar feedback (se añade a pending_feedback)
        pending_count = trainer.add_feedback(input_data, rating, feedback)
        
        # Obtener conteos actualizados
        training_data, feedback_data, pending_feedback = trainer.load_training_data()
        total_historical = len(feedback_data) + len(pending_feedback)
        
        return jsonify({
            'success': True,
            'message': 'Feedback guardado correctamente',
            'pending_feedback': len(pending_feedback),
            'total_feedback': total_historical
        })
        
    except Exception as e:
        print("❌ Error en /feedback:", str(e))
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/retrain', methods=['POST'])
def retrain_model():
    """Reentrena el modelo con feedbacks pendientes"""
    try:
        print("\n🔄 Solicitud de reentrenamiento recibida...")
        
        # Cargar datos actuales
        training_data, feedback_data, pending_feedback = trainer.load_training_data()
        pending_count = len(pending_feedback)
        
        print(f"📊 Estado actual:")
        print(f"   - Training data: {len(training_data)}")
        print(f"   - Feedback usado: {len(feedback_data)}")
        print(f"   - Feedback pendiente: {pending_count}")
        
        if pending_count < 5:
            message = f'Necesitas al menos 5 feedbacks nuevos. Tienes: {pending_count}'
            print(f"⚠️ {message}")
            return jsonify({
                'success': False,
                'message': message,
                'pending_count': pending_count
            }), 400
        
        # Guardar total histórico ANTES del reentrenamiento
        total_before = len(feedback_data) + pending_count
        
        print(f"🚀 Iniciando reentrenamiento con {pending_count} feedbacks...")
        
        # Reentrenar (esto moverá pending → feedback_data y vaciará pending)
        history, metrics = trainer.retrain_with_feedback()
        
        # Recargar modelo en memoria
        print("📥 Recargando modelo actualizado...")
        model.load_model()
        
        # Cargar estado NUEVO
        _, _, new_pending = trainer.load_training_data()
        
        print(f"✅ Reentrenamiento completado exitosamente")
        print(f"   - Accuracy: {metrics['accuracy']:.4f}")
        print(f"   - Loss: {metrics['loss']:.4f}")
        print(f"   - AUC: {metrics.get('auc', 0.0):.4f}")
        
        return jsonify({
            'success': True,
            'message': 'Modelo reentrenado exitosamente',
            'metrics': {
                'accuracy': float(metrics['accuracy']),
                'loss': float(metrics['loss']),
                'auc': float(metrics.get('auc', 0.0))
            },
            'pending_feedback': len(new_pending),  # Siempre 0 tras reentrenar
            'total_feedback': total_before         # Total antes del reentrenamiento
        })
        
    except ValueError as ve:
        print(f"⚠️ Error de validación: {str(ve)}")
        return jsonify({
            'success': False,
            'error': str(ve)
        }), 400
        
    except FileNotFoundError as fe:
        print(f"❌ Archivo no encontrado: {str(fe)}")
        return jsonify({
            'success': False,
            'error': 'No se encontró el archivo de datos de entrenamiento'
        }), 404
        
    except Exception as e:
        error_trace = traceback.format_exc()
        print("❌ Error en /retrain:")
        print(error_trace)
        return jsonify({
            'success': False,
            'error': str(e),
            'details': error_trace
        }), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Obtiene estadísticas del modelo"""
    try:
        training_data, feedback_data, pending_feedback = trainer.load_training_data()
        
        return jsonify({
            'success': True,
            'stats': {
                'training_samples': len(training_data),
                'feedback_samples': len(feedback_data),      # feedbacks ya usados
                'pending_feedback': len(pending_feedback),   # feedbacks nuevos
                'total_samples': len(training_data) + len(feedback_data) + len(pending_feedback),
                'model_loaded': model.model is not None,
                'ready_for_retrain': len(pending_feedback) >= 5  # Solo si hay 5 nuevos
            }
        })
    except Exception as e:
        print("❌ Error en /stats:", str(e))
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Iniciando Neuro UX Styler API...")
    print("📍 Servidor corriendo en http://localhost:5001")
    app.run(debug=True, port=5001)