import os
import json
import numpy as np
from sklearn.model_selection import train_test_split
from model import NeuroUXModel
from data_processor import DataProcessor

class Trainer:
    def __init__(self):
        self.data_path = os.path.join(os.path.dirname(__file__), 'data', 'combined_training_data.json')
        self.dataset_path = self.data_path
        self.model = NeuroUXModel()
        self.processor = DataProcessor()
        
    def load_training_data(self):
        """
        Carga el dataset combinado y maneja ambos formatos (lista o objeto).
        """
        if not os.path.exists(self.dataset_path):
            raise FileNotFoundError(f"Dataset no encontrado: {self.dataset_path}")
        
        with open(self.dataset_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # ✅ CORREGIDO: Detectar y manejar ambos formatos
        if isinstance(data, list):
            # Si es una lista, asumimos que es training_data directamente
            print("ℹ️ Formato detectado: Lista simple")
            training_data = data
            feedback_data = []
            pending_feedback = []
        elif isinstance(data, dict):
            # Si es un objeto, extraer las secciones
            print("ℹ️ Formato detectado: Objeto con secciones")
            training_data = data.get('training_data', [])
            feedback_data = data.get('feedback_data', [])
            pending_feedback = data.get('pending_feedback', [])
        else:
            raise ValueError(f"Formato de datos no reconocido: {type(data)}")
        
        print(f"✅ Cargados {len(training_data)} ejemplos de entrenamiento")
        print(f"✅ Cargados {len(feedback_data)} ejemplos de feedback")
        print(f"✅ Cargados {len(pending_feedback)} feedbacks pendientes")
        
        return training_data, feedback_data, pending_feedback
    
    def prepare_dataset(self):
        """Prepara el dataset combinando todos los datos disponibles"""
        training_data, feedback_data, pending_feedback = self.load_training_data()
        all_data = training_data + feedback_data + pending_feedback
        
        X = []
        y = []
        
        for item in all_data:
            # ✅ Validación de datos
            if not isinstance(item, dict) or 'input' not in item:
                print(f"⚠️ Saltando item inválido: {item}")
                continue
                
            try:
                features, _, _, _ = self.processor.encode_input(item['input'])
                X.append(features[0])
                
                rating = item.get('rating', 0.5)
                y.append(1 if rating >= 0.7 else 0)
            except Exception as e:
                print(f"⚠️ Error procesando item: {e}")
                continue
        
        if len(X) == 0:
            raise ValueError("No se pudieron procesar datos válidos del dataset")
        
        return np.array(X), np.array(y)
    
    def train_model(self, epochs=100, test_size=0.2, incremental=False):
        """Entrena el modelo con el dataset completo"""
        print("📊 Cargando y preparando datos...")
        X, y = self.prepare_dataset()
        print(f"✅ Dataset cargado: {len(X)} muestras")
        
        # ✅ Validar que hay suficientes datos
        if len(X) < 10:
            raise ValueError(f"Dataset muy pequeño: {len(X)} muestras. Se necesitan al menos 10.")
        
        # ✅ CARGAR MODELO EXISTENTE (si es incremental)
        if incremental:
            model_path = os.path.join(os.path.dirname(__file__), 'data', 'models', 'neuro_ux_model.h5')
            if os.path.exists(model_path):
                print("🔄 Cargando modelo existente para entrenamiento incremental...")
                self.model.load_model()
            else:
                print("⚠️ No se encontró modelo previo, entrenando desde cero...")
                print(f"   Buscado en: {model_path}")
        
        X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=test_size, random_state=42)
        print(f"🔄 Entrenamiento: {len(X_train)} | Validación: {len(X_val)}")
        
        print("\n🚀 Iniciando entrenamiento...")
        history = self.model.train(X_train, y_train, X_val, y_val, epochs=epochs)
        metrics = self.model.evaluate(X_val, y_val)
        
        print(f"\n✨ Resultados finales:")
        print(f"   - Loss: {metrics['loss']:.4f}")
        print(f"   - Accuracy: {metrics['accuracy']:.4f}")
        print(f"   - AUC: {metrics.get('auc', 0.0):.4f}")
        
        # ✅ GUARDAR EL MODELO ACTUALIZADO
        self.model.save_model()
        return history, metrics
    
    def add_feedback(self, input_data, rating, feedback_text):
        """Agrega un nuevo feedback a la cola de pendientes"""
        # ✅ Cargar o crear estructura de datos
        if not os.path.exists(self.data_path):
            data = {
                'training_data': [],
                'feedback_data': [],
                'pending_feedback': []
            }
        else:
            with open(self.data_path, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
            
            # ✅ Convertir lista a objeto si es necesario
            if isinstance(loaded_data, list):
                data = {
                    'training_data': loaded_data,
                    'feedback_data': [],
                    'pending_feedback': []
                }
            else:
                data = loaded_data
        
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
        """Reentrena usando todos los datos incluyendo feedbacks pendientes"""
        try:
            print("🔄 Iniciando reentrenamiento...")
            
            # Cargar datos
            if not os.path.exists(self.data_path):
                raise FileNotFoundError(f"No existe el archivo de datos: {self.data_path}")
            
            with open(self.data_path, 'r', encoding='utf-8') as f:
                loaded_data = json.load(f)
            
            # ✅ Manejar ambos formatos
            if isinstance(loaded_data, list):
                data = {
                    'training_data': loaded_data,
                    'feedback_data': [],
                    'pending_feedback': []
                }
            else:
                data = loaded_data
            
            pending = data.get('pending_feedback', [])
            if len(pending) < 5:
                raise ValueError(f"No hay suficientes feedbacks pendientes. Tienes: {len(pending)}, se necesitan al menos 5")
            
            print(f"📊 Reentrenando con {len(pending)} feedbacks nuevos")
            
            # ✅ Cargar modelo existente antes de reentrenar
            model_path = os.path.join(os.path.dirname(__file__), 'model', 'neuro_ux_model.h5')
            if os.path.exists(model_path):
                print("🔄 Cargando modelo existente...")
                self.model.load_model()
            
            # Combinar todos los datos
            all_data = data.get('training_data', []) + data.get('feedback_data', []) + pending
            
            X = []
            y = []
            for item in all_data: 
                if not isinstance(item, dict) or 'input' not in item: 
                    print(f"⚠️ Saltando item inválido: {item}")
                    continue
                
                try:
                    features, _, _, _ = self.processor.encode_input(item['input'])
                    X.append(features[0])
                    rating = item.get('rating', 0.5)
                    y.append(1 if rating >= 0.7 else 0)
                except Exception as e:
                    print(f"⚠️ Error procesando item: {e}")
                    continue
            
            if len(X) == 0:
                raise ValueError("No se pudieron procesar datos válidos")
            
            X = np.array(X)
            y = np.array(y)
            
            print(f"✅ Total de datos para reentrenamiento: {len(X)} muestras")
            
            # Dividir
            X_train, X_val, y_train, y_val = train_test_split(
                X, y, test_size=0.2, random_state=42
            )
            
            # Entrenar
            print("\n🚀 Reentrenando modelo...")
            history = self.model.train(X_train, y_train, X_val, y_val, epochs=50)
            metrics = self.model.evaluate(X_val, y_val)
            
            print(f"\n✨ Resultados del reentrenamiento:")
            print(f"   - Loss: {metrics['loss']:.4f}")
            print(f"   - Accuracy: {metrics['accuracy']:.4f}")
            print(f"   - AUC: {metrics.get('auc', 0.0):.4f}")
            
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