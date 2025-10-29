import os
import json
import numpy as np
from sklearn.model_selection import train_test_split
from model import NeuroUXModel
from data_processor import DataProcessor

class Trainer:
    def __init__(self):
        self.model = NeuroUXModel()
        self.processor = DataProcessor()
        self.data_path = os.path.join(os.path.dirname(__file__), 'data', 'training_data.json')
        
    def load_training_data(self):
        """Carga los datos de entrenamiento"""
        with open(self.data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data['training_data'], data.get('feedback_data', [])
    
    def prepare_dataset(self):
        """Prepara el dataset para entrenamiento"""
        training_data, feedback_data = self.load_training_data()
        
        # Combinar datos iniciales y feedback
        all_data = training_data + feedback_data
        
        X = []
        y = []
        
        for item in all_data:
            # Codificar entrada
            features, _, _, _ = self.processor.encode_input(item['input'])
            X.append(features[0])
            
            # Rating como etiqueta (normalizado a 0-1)
            rating = item.get('rating', 0.5)
            y.append(rating)
        
        X = np.array(X)
        y = np.array(y)
        
        return X, y
    
    def train_model(self, epochs=100, test_size=0.2):
        """Entrena el modelo completo"""
        print("📊 Cargando y preparando datos...")
        X, y = self.prepare_dataset()
        
        print(f"✅ Dataset cargado: {len(X)} muestras")
        
        # Dividir en entrenamiento y validación
        X_train, X_val, y_train, y_val = train_test_split(
            X, y, test_size=test_size, random_state=42
        )
        
        print(f"🔄 Entrenamiento: {len(X_train)} muestras")
        print(f"🔄 Validación: {len(X_val)} muestras")
        
        # Entrenar
        print("\n🚀 Iniciando entrenamiento...")
        history = self.model.train(X_train, y_train, X_val, y_val, epochs=epochs)
        
        # Evaluar
        print("\n📈 Evaluando modelo...")
        metrics = self.model.evaluate(X_val, y_val)
        
        print(f"\n✨ Resultados finales:")
        print(f"   - Loss: {metrics['loss']:.4f}")
        print(f"   - Accuracy: {metrics['accuracy']:.4f}")
        print(f"   - AUC: {metrics['auc']:.4f}")
        
        # Guardar modelo
        self.model.save_model()
        
        return history, metrics
    
    def add_feedback(self, input_data, rating, feedback_text):
        """Agrega feedback del usuario para reentrenamiento"""
        with open(self.data_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Agregar nuevo feedback
        feedback_entry = {
            'input': input_data,
            'rating': rating,
            'feedback': feedback_text
        }
        
        if 'feedback_data' not in data:
            data['feedback_data'] = []
        
        data['feedback_data'].append(feedback_entry)
        
        # Guardar
        with open(self.data_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ Feedback agregado. Total: {len(data['feedback_data'])} registros")
        
        return len(data['feedback_data'])
    
    def retrain_with_feedback(self):
        """Reentrena el modelo con nuevo feedback"""
        feedback_data, _ = self.load_training_data()
        
        if len(feedback_data) < 5:
            print("⚠️  Necesitas al menos 5 feedbacks para reentrenar")
            return False
        
        print(f"🔄 Reentrenando con {len(feedback_data)} nuevos datos...")
        return self.train_model(epochs=50)

if __name__ == "__main__":
    trainer = Trainer()
    
    print("=" * 60)
    print("🧠 NEURO UX STYLER - ENTRENAMIENTO")
    print("=" * 60)
    
    # Entrenar modelo inicial
    history, metrics = trainer.train_model(epochs=100)
    
    print("\n✅ Entrenamiento completado!")
    print(f"🎯 Confianza alcanzada: {metrics['accuracy']*100:.1f}%")
    
    if metrics['accuracy'] >= 0.9:
        print("🎉 ¡Objetivo alcanzado! (>90% confianza)")
    else:
        print(f"📊 Necesitas más datos de feedback para alcanzar >90%")