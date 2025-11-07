from flask import Flask, request, jsonify
from flask_cors import CORS
from model import NeuroUXModel
from data_processor import DataProcessor
from training import Trainer
import os
import traceback

app = Flask(__name__)

# CORS permisivo para desarrollo
CORS(app, resources={
    r"/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Inicializar componentes
model = NeuroUXModel()
processor = DataProcessor()
trainer = Trainer()

# Cargar modelo al iniciar
print("🔄 Cargando modelo...")
try:
    model.load_model()
    print("✅ Modelo cargado correctamente")
except Exception as e:
    print(f"⚠️ Error al cargar modelo: {e}")

@app.route('/health', methods=['GET', 'OPTIONS'])
@app.route('/api/health', methods=['GET', 'OPTIONS'])
def health_check():
    """Endpoint de salud"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model.model is not None
    })

@app.route('/generate', methods=['POST', 'OPTIONS'])
@app.route('/api/generate', methods=['POST', 'OPTIONS'])
def generate_ui_kit():
    """Genera un UI Kit basado en los datos de entrada"""
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        data = request.json
        print(f"📥 Datos recibidos: {data}")
        
        if not data:
            return jsonify({'success': False, 'error': 'No se recibieron datos'}), 400
        
        # Valores por defecto
        input_data = {
            'name': data.get('name', ''),
            'mission': data.get('mission', ''),
            'values': data.get('values', ''),
            'sector': data.get('sector', 'general'),
            'audience': data.get('audience', 'general')
        }
        
        # ✅ CORREGIDO: encode_input retorna 3 valores
        features, metadata, _ = processor.encode_input(input_data)
        prediction = model.predict(features)
        confidence = float(prediction[0][0])
        
        # ✅ CORREGIDO: generate_ui_kit recibe 3 parámetros
        ui_kit = processor.generate_ui_kit(prediction, metadata, None)
        
        response = {
            'success': True,
            'ui_kit': {
                'colors': ui_kit.get('colors', {}),
                'typography': ui_kit.get('typography', {}),
                'components': ui_kit.get('components', {}),
                'tokens': ui_kit.get('tokens', {}),
                'confidence': confidence,
                'style': ui_kit.get('style', {})
            }
        }
        
        print(f"✅ UI Kit generado con confianza: {confidence:.2%}")
        return jsonify(response)
        
    except Exception as e:
        error_msg = str(e)
        print(f"❌ Error en /generate: {error_msg}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': error_msg
        }), 500

@app.route('/feedback', methods=['POST', 'OPTIONS'])
@app.route('/api/feedback', methods=['POST', 'OPTIONS'])
def submit_feedback():
    """Recibe feedback del usuario"""
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        data = request.json
        print(f"📥 Feedback recibido: {data}")
        
        input_data = data.get('input_data')
        rating = data.get('rating')
        feedback = data.get('feedback', '')
        
        if not input_data or rating is None:
            return jsonify({
                'success': False,
                'error': 'Se requiere input_data y rating'
            }), 400
        
        pending_count = trainer.add_feedback(input_data, rating, feedback)
        training_data, feedback_data, pending_feedback = trainer.load_training_data()
        total_historical = len(feedback_data) + len(pending_feedback)
        
        print(f"✅ Feedback guardado. Pendientes: {pending_count}")
        
        return jsonify({
            'success': True,
            'message': 'Feedback guardado correctamente',
            'pending_feedback': len(pending_feedback),
            'total_feedback': total_historical
        })
        
    except Exception as e:
        print(f"❌ Error en /feedback: {str(e)}")
        traceback.print_exc()
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/retrain', methods=['POST', 'OPTIONS'])
@app.route('/api/retrain', methods=['POST', 'OPTIONS'])
def retrain_model():
    """Reentrena el modelo"""
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        print("\n🔄 Solicitud de reentrenamiento recibida...")
        
        training_data, feedback_data, pending_feedback = trainer.load_training_data()
        pending_count = len(pending_feedback)
        
        print(f"📊 Feedback pendiente: {pending_count}")
        
        if pending_count < 5:
            message = f'Necesitas al menos 5 feedbacks nuevos. Tienes: {pending_count}'
            print(f"⚠️ {message}")
            return jsonify({
                'success': False,
                'message': message,
                'pending_count': pending_count
            }), 400
        
        total_before = len(feedback_data) + pending_count
        
        print(f"🚀 Iniciando reentrenamiento con {pending_count} feedbacks...")
        history, metrics = trainer.retrain_with_feedback()
        
        print("📥 Recargando modelo actualizado...")
        model.load_model()
        
        _, _, new_pending = trainer.load_training_data()
        
        print(f"✅ Reentrenamiento completado")
        print(f"   - Accuracy: {metrics['accuracy']:.4f}")
        print(f"   - Loss: {metrics['loss']:.4f}")
        
        return jsonify({
            'success': True,
            'message': 'Modelo reentrenado exitosamente',
            'metrics': {
                'accuracy': float(metrics['accuracy']),
                'loss': float(metrics['loss']),
                'auc': float(metrics.get('auc', 0.0))
            },
            'pending_feedback': len(new_pending),
            'total_feedback': total_before
        })
        
    except Exception as e:
        error_trace = traceback.format_exc()
        print("❌ Error en /retrain:")
        print(error_trace)
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/stats', methods=['GET', 'OPTIONS'])
@app.route('/api/stats', methods=['GET', 'OPTIONS'])
def get_stats():
    """Obtiene estadísticas"""
    if request.method == 'OPTIONS':
        return '', 204
        
    try:
        training_data, feedback_data, pending_feedback = trainer.load_training_data()
        
        return jsonify({
            'success': True,
            'stats': {
                'training_samples': len(training_data),
                'feedback_samples': len(feedback_data),
                'pending_feedback': len(pending_feedback),
                'total_samples': len(training_data) + len(feedback_data) + len(pending_feedback),
                'model_loaded': model.model is not None,
                'ready_for_retrain': len(pending_feedback) >= 5
            }
        })
    except Exception as e:
        print(f"❌ Error en /stats: {str(e)}")
        traceback.print_exc()
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 NEURO UX STYLER API")
    print("=" * 60)
    print("📍 Servidor: http://localhost:5001")
    print("🏥 Health check: http://localhost:5001/health")
    print("📊 Stats: http://localhost:5001/stats")
    print("=" * 60)
    app.run(debug=True, port=5001, host='0.0.0.0')