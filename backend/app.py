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
        
        # Validar datos requeridos
        required_fields = ['name', 'mission', 'values', 'sector', 'audience']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'error': f'Campo requerido: {field}'
                }), 400
        
        # Procesar entrada
        features, keywords, sector, audience = processor.encode_input(data)
        
        # Predecir confianza
        prediction = model.predict(features)
        
        # Generar UI Kit
        ui_kit = processor.generate_ui_kit(prediction, keywords, sector, audience)
        
        # Agregar datos de entrada para feedback
        ui_kit['input_data'] = data
        
        return jsonify({
            'success': True,
            'ui_kit': ui_kit
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

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
        
        # Guardar feedback
        count = trainer.add_feedback(input_data, rating, feedback)
        
        return jsonify({
            'success': True,
            'message': 'Feedback guardado correctamente',
            'total_feedback': count
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/retrain', methods=['POST'])
def retrain_model():
    """Reentrena el modelo con nuevo feedback"""
    try:
        # Verificar si hay suficiente feedback
        training_data, feedback_data = trainer.load_training_data()
        
        if len(feedback_data) < 5:
            return jsonify({
                'success': False,
                'message': f'Necesitas al menos 5 feedbacks. Tienes: {len(feedback_data)}'
            }), 400
        
        # Reentrenar
        history, metrics = trainer.retrain_with_feedback()
        
        # Recargar modelo
        model.load_model()
        
        return jsonify({
            'success': True,
            'message': 'Modelo reentrenado exitosamente',
            'metrics': {
                'accuracy': float(metrics['accuracy']),
                'loss': float(metrics['loss']),
                'auc': float(metrics['auc'])
            },
            'feedback_count': len(feedback_data)
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Obtiene estadísticas del modelo"""
    try:
        training_data, feedback_data = trainer.load_training_data()
        
        return jsonify({
            'success': True,
            'stats': {
                'training_samples': len(training_data),
                'feedback_samples': len(feedback_data),
                'total_samples': len(training_data) + len(feedback_data),
                'model_loaded': model.model is not None,
                'ready_for_retrain': len(feedback_data) >= 5
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    print("🚀 Iniciando Neuro UX Styler API...")
    print("📍 Servidor corriendo en http://localhost:5001")
    app.run(debug=True, port=5001)