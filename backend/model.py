import numpy as np
import os
import json

import importlib
import importlib.util

tf = None
keras = None
layers = models = callbacks = optimizers = None


if importlib.util.find_spec("tensorflow") is not None:
    tf = importlib.import_module("tensorflow")
    keras = getattr(tf, "keras", None)
    if keras is not None:
        layers = getattr(keras, "layers", None)
        models = getattr(keras, "models", None)
        callbacks = getattr(keras, "callbacks", None)
        optimizers = getattr(keras, "optimizers", None)
elif importlib.util.find_spec("keras") is not None:
    keras = importlib.import_module("keras")
    layers = getattr(keras, "layers", None)
    models = getattr(keras, "models", None)
    callbacks = getattr(keras, "callbacks", None)
    optimizers = getattr(keras, "optimizers", None)
else:
    tf = None
    keras = None
    layers = models = callbacks = optimizers = None

class NeuroUXModel:
    def __init__(self):
        model_dir = os.path.join(os.path.dirname(__file__), 'data', 'models')
        os.makedirs(model_dir, exist_ok=True)
        self.model_path = os.path.join(model_dir, 'neuro_ux_model.h5')
        self.model = None
        self.history = None
        self.build_model()
        
    def build_model(self):
        # Asegurarse de que TensorFlow esté cargado
        if tf is None or keras is None:
            print("❌ Error: TensorFlow/Keras no está instalado o no se pudo importar.")
            raise ImportError("TensorFlow o Keras es requerido para construir el modelo.")
            
        from tensorflow.keras.models import Sequential
        from tensorflow.keras.layers import Dense, Dropout
        from tensorflow.keras.metrics import AUC

        model = Sequential([
            Dense(64, activation='relu', input_shape=(14,)),
            Dropout(0.3),
            Dense(32, activation='relu'),
            Dropout(0.3),
            Dense(16, activation='relu'),
            Dense(1, activation='sigmoid')  # Probabilidad de que sea "bueno"
        ])
        
        model.compile(
            optimizer='adam',
            loss='binary_crossentropy', 
            metrics=['accuracy', AUC(name='auc')]
        )
        
        self.model = model
        return model
    
    def train(self, X_train, y_train, X_val, y_val, epochs=100):
        """Entrena el modelo"""
        if self.model is None:
            self.build_model()
        
        # Callbacks para mejorar el entrenamiento
        from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
        
        callbacks_list = [
            EarlyStopping(
                monitor='val_loss',
                patience=15,
                restore_best_weights=True
            ),
            ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=0.00001
            ),
            ModelCheckpoint(
                self.model_path,
                monitor='val_accuracy',
                save_best_only=True,
                verbose=0 # Reducir el ruido en la consola
            )
        ]
        
        # Entrenar
        self.history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=32,
            callbacks=callbacks_list,
            verbose=1
        )
        
        return self.history
    
    def predict(self, X):
        """Realiza predicciones"""
        if self.model is None:
            self.load_model()
        
        prediction = self.model.predict(X, verbose=0)
        return prediction
    
    def save_model(self):
        """Guarda el modelo en la ruta configurada"""
        if self.model is not None:
            self.model.save(self.model_path)
            print(f"✅ Modelo guardado en {self.model_path}")
        else:
            print("⚠️ No hay modelo para guardar")
    
    def load_model(self, path=None):
        """
        Carga el modelo desde disco.
        Si no se especifica path, usa self.model_path
        """
        if keras is None:
            print("⚠️ Keras no está disponible. No se puede cargar el modelo.")
            self.build_model()
            return False
            
        from tensorflow.keras.models import load_model
        
        # ✅ CORREGIDO: Usar self.model_path si no se especifica path
        load_path = path if path is not None else self.model_path
        
        if os.path.exists(load_path):
            try:
                self.model = load_model(load_path)
                print(f"✅ Modelo cargado desde {load_path}")
                return True
            except Exception as e:
                print(f"❌ Error cargando modelo desde {load_path}: {e}")
                print("🔄 Construyendo modelo nuevo...")
                self.build_model()
                return False
        else:
            print(f"⚠️ No se encontró modelo en {load_path}")
            print("🔄 Construyendo modelo nuevo...")
            self.build_model()
            return False
    
    def evaluate(self, X_test, y_test):
        """Evalúa el modelo"""
        if self.model is None:
            print("⚠️ No hay modelo cargado, intentando cargar...")
            if not self.load_model():
                print("❌ No se pudo cargar ni construir el modelo para evaluar.")
                return {'loss': -1, 'accuracy': 0, 'auc': 0}
        
        results = self.model.evaluate(X_test, y_test, verbose=0)
        metrics = {
            'loss': results[0],
            'accuracy': results[1],
            'auc': results[2] if len(results) > 2 else 0.0 # Asegurar que auc exista
        }
        return metrics
    
    def get_training_history(self):
        """Retorna el historial de entrenamiento"""
        if self.history is None:
            return None
        
        return {
            'loss': [float(x) for x in self.history.history['loss']],
            'val_loss': [float(x) for x in self.history.history['val_loss']],
            'accuracy': [float(x) for x in self.history.history['accuracy']],
            'val_accuracy': [float(x) for x in self.history.history['val_accuracy']]
        }