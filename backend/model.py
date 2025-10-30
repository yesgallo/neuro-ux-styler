import numpy as np
import os
import json

try:
    import tensorflow as tf
    keras = tf.keras
    from tensorflow.keras import layers, models, callbacks, optimizers
except Exception:
    from tensorflow import keras
    from tensorflow.keras import layers, models, callbacks, optimizers

class NeuroUXModel:
    def __init__(self):
        self.model = None
        self.history = None
        self.model_path = 'data/models/neuro_ux_model.h5'
        self.confidence_threshold = 0.7
        
    def build_model(self, input_dim=9):
        """Construye la arquitectura de la red neuronal"""
        model = keras.Sequential([
            # Capa de entrada
            layers.Input(shape=(input_dim,)),
            
            # Primera capa oculta con normalización
            layers.Dense(128, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.3),
            
            # Segunda capa oculta
            layers.Dense(64, activation='relu'),
            layers.BatchNormalization(),
            layers.Dropout(0.2),
            
            # Tercera capa oculta
            layers.Dense(32, activation='relu'),
            layers.Dropout(0.1),
            
            # Capa de salida (confianza de la predicción)
            layers.Dense(1, activation='sigmoid')
        ])
        
        # Compilar el modelo
        model.compile(
            optimizer=keras.optimizers.Adam(learning_rate=0.001),
            loss='binary_crossentropy',
            metrics=['accuracy', 'AUC']
        )
        
        self.model = model
        return model
    
    def train(self, X_train, y_train, X_val, y_val, epochs=100):
        """Entrena el modelo"""
        if self.model is None:
            self.build_model(input_dim=X_train.shape[1])
        
        # Callbacks para mejorar el entrenamiento
        callbacks = [
            keras.callbacks.EarlyStopping(
                monitor='val_loss',
                patience=15,
                restore_best_weights=True
            ),
            keras.callbacks.ReduceLROnPlateau(
                monitor='val_loss',
                factor=0.5,
                patience=5,
                min_lr=0.00001
            ),
            keras.callbacks.ModelCheckpoint(
                self.model_path,
                monitor='val_accuracy',
                save_best_only=True
            )
        ]
        
        # Entrenar
        self.history = self.model.fit(
            X_train, y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=32,
            callbacks=callbacks,
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
        """Guarda el modelo entrenado"""
        if self.model is not None:
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            self.model.save(self.model_path)
            print(f"Modelo guardado en {self.model_path}")
    
    def load_model(self):
        """Carga un modelo previamente entrenado"""
        if os.path.exists(self.model_path):
            self.model = keras.models.load_model(self.model_path)
            print(f"Modelo cargado desde {self.model_path}")
            return True
        else:
            print("No se encontró modelo guardado. Construyendo nuevo modelo...")
            self.build_model()
            return False
    
    def evaluate(self, X_test, y_test):
        """Evalúa el modelo"""
        if self.model is None:
            self.load_model()
        
        results = self.model.evaluate(X_test, y_test, verbose=0)
        metrics = {
            'loss': results[0],
            'accuracy': results[1],
            'auc': results[2]
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