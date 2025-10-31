import os
import json
import numpy as np
from sklearn.model_selection import train_test_split
from model import NeuroUXModel
from data_processor import DataProcessor

class Trainer:
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), 'data', 'combined_training_data.json')
        self.model = NeuroUXModel()
        self.processor = DataProcessor()
        
    def load_training_data(self):
        """Carga todos los datos: training + feedback usados + feedback pendientes"""
        with open(self.data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return (
            data['training_data'],
            data.get('feedback_data', []),
            data.get('pending_feedback', [])
        )
    
    def prepare_dataset(self):
        """Prepara el dataset combinando todos los datos disponibles"""
        training_data, feedback_data, pending_feedback = self.load_training_data()
        all_data = training_data + feedback_data + pending_feedback
        
        X = []
        y = []
        
        for item in all_data:
            features, _, _, _ = self.processor.encode_input(item['input'])
            X.append(features[0])
            
            # ✅ Convertir rating a clase binaria
            rating = item.get('rating', 0.5)
            y.append(1 if rating >= 0.7 else 0)
        
        return np.array(X), np.array(y)
    
    def train_model(self, epochs=100, test_size=0.2):
        """Entrena el modelo completo (usado solo al inicio)"""
        print("📊 Cargando y preparando datos...")
        X, y = self.prepare_dataset()
        print(f"✅ Dataset cargado: {len(X)} muestras")
        
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=test_size, random_state=42)
        print(f"🔄 Entrenamiento: {len(X_train)} | Validación: {len(X_val)}")
        
        print("\n🚀 Iniciando entrenamiento...")
        history = self.model.train(X_train, y_train, X_val, y_val, epochs=epochs)
        metrics = self.model.evaluate(X_val, y_val)
        
        print(f"\n✨ Resultados finales:")
        print(f"   - Loss: {metrics['loss']:.4f}")
        print(f"   - Accuracy: {metrics['accuracy']:.4f}")
        print(f"   - AUC: {metrics.get('auc', 0.0):.4f}")
        
        self.model.save_model()
        return history, metrics
    
    def add_feedback(self, input_data, rating, feedback_text):
        """Agrega un nuevo feedback a la cola de pendientes"""
        with open(self.data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        if 'pending_feedback' not in data:
            data['pending_feedback'] = []
        
        data['pending_feedback'].append({
            'input': input_data,
            'rating': rating,
            'feedback': feedback_text
        })
        
        with open(self.data_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        pending_count = len(data['pending_feedback'])
        print(f"✅ Feedback agregado. Pendientes: {pending_count} registros")
        return pending_count
    
    def retrain_with_feedback(self):
        """Reentrena usando solo feedbacks pendientes"""
        try:
            print("🔄 Iniciando reentrenamiento...")
            
            # Cargar datos
            with open(self.data_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            pending = data.get('pending_feedback', [])
            if len(pending) < 5:
                raise ValueError(f"No hay suficientes feedbacks pendientes. Tienes: {len(pending)}")
            
            print(f"📊 Reentrenando con {len(pending)} feedbacks nuevos")
            
            # Combinar todos los datos
            all_data = data.get('training_data', []) + data.get('feedback_data', []) + pending
            
            X = []
            y = []
            for item in all_data: 
                if 'input' not in item: 
                    print(f"⚠️ Saltando item sin 'input': {item}")
                    continue
                features, _, _, _ = self.processor.encode_input(item['input'])
                X.append(features[0])
                # ✅ CORREGIDO: usar clase binaria, no rating
                rating = item.get('rating', 0.5)
                y.append(1 if rating >= 0.7 else 0)
            
            X = np.array(X)
            y = np.array(y)
            
            # Dividir
            X_train, X_val, y_train, y_val = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Entrenar
            history = self.model.train(X_train, y_train, X_val, y_val, epochs=50)
            metrics = self.model.evaluate(X_val, y_val)
            
            # Guardar modelo
            self.model.save_model()
            
            # Mover feedbacks usados de 'pending' a 'feedback_data'
            if 'feedback_data' not in data:
                data['feedback_data'] = []
            
            data['feedback_data'].extend(pending)
            data['pending_feedback'] = []  # Vaciar la cola de pendientes
            
            with open(self.data_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Reentrenamiento completado. {len(pending)} feedbacks procesados.")
            return history, metrics
            
        except Exception as e:
            print(f"❌ Error en retrain_with_feedback: {str(e)}")
            raise

if __name__ == "__main__":
    trainer = Trainer()
    print("=" * 60)
    print("🧠 NEURO UX STYLER - ENTRENAMIENTO INICIAL")
    print("=" * 60)
    
    history, metrics = trainer.train_model(epochs=100)
    
    print("\n✅ Entrenamiento inicial completado!")
    print(f"🎯 Precisión: {metrics['accuracy']*100:.1f}%")