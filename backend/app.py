from flask import Flask, request, jsonify
from flask_cors import CORS
from model import NeuroUXModel
from data_processor import DataProcessor
from training import Trainer
import os

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
        prediction = model.predict(features)
        ui_kit = processor.generate_ui_kit(prediction, keywords, sector, audience)
        ui_kit['input_data'] = data
        
        return jsonify({'success': True, 'ui_kit': ui_kit})
        
    except Exception as e:
        print("❌ Error en /generate:", str(e))
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
            'pending_feedback': len(pending_feedback),      # para reentrenar
            'total_feedback': total_historical              # total histórico
        })
        
    except Exception as e:
        print("❌ Error en /feedback:", str(e))
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/retrain', methods=['POST'])
def retrain_model():
    """Reentrena el modelo con nuevo feedback"""
    try:
        training_data, feedback_data = trainer.load_training_data()
        
        if len(feedback_data) < 5:
            return jsonify({
                'success': False,
                'message': f'Necesitas al menos 5 feedbacks. Tienes: {len(feedback_data)}'
            }), 400
        
        # ✅ Reentrenar con el método corregido
        history, metrics = trainer.retrain_with_feedback()
        
        # ✅ Recargar el modelo en memoria
        model.load_model()
        
        return jsonify({
            'success': True,
            'message': 'Modelo reentrenado exitosamente',
            'metrics': {
                'accuracy': float(metrics['accuracy']),
                'loss': float(metrics['loss']),
                'auc': float(metrics.get('auc', 0.0))
            },
            'feedback_count': len(feedback_data)
        })
        
    except Exception as e:
        print("❌ Error en /retrain:", str(e))  # ← Verás el error real en la terminal
        return jsonify({'success': False, 'error': str(e)}), 500

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
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("🚀 Iniciando Neuro UX Styler API...")
    print("📍 Servidor corriendo en http://localhost:5001")
    app.run(debug=True, port=5001)