import json
import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

def main():
    # Cargar dataset
    with open('backend/data/dataset.json') as f:
        data = json.load(f)
    
    # Preparar textos
    texts = []
    for d in data:
        text = f"{d['input']['name']} {d['input']['mission']} {d['input']['values']} {d['input']['audience']} {d['input']['sector']}"
        texts.append(text)
    
    # Vectorizar texto 
    vectorizer = TfidfVectorizer(stop_words=None)
    X = vectorizer.fit_transform(texts).toarray()
    input_dim = X.shape[1]  
    
    # Preparar salidas (paleta en RGB normalizado)
    y = []
    for d in data:
        rgb_colors = []
        for hex_color in d['output']['palette']:
            hex_color = hex_color.lstrip('#')
            r = int(hex_color[0:2], 16) / 255.0
            g = int(hex_color[2:4], 16) / 255.0
            b = int(hex_color[4:6], 16) / 255.0
            rgb_colors.extend([r, g, b])
        y.append(rgb_colors[:15])  # 5 colores × 3 canales
    
    y = np.array(y)
    
    # Crear modelo con input_dim dinámico
    model = Sequential([
        Dense(256, activation='relu', input_shape=(input_dim,)),
        Dropout(0.3),
        Dense(128, activation='relu'),
        Dropout(0.3),
        Dense(64, activation='relu'),
        Dense(15, activation='sigmoid')
    ])
    
    model.compile(optimizer='adam', loss='mse', metrics=['mae'])
    
    # Entrenar
    print(f"🧠 Entrenando modelo con {input_dim} características...")
    model.fit(X, y, epochs=50, batch_size=16, validation_split=0.2, verbose=1)
    
    # Guardar
    model.save('backend/data/ux_model.h5')
    with open('backend/data/vectorizer.pkl', 'wb') as f:
        pickle.dump(vectorizer, f)
    
    print("✅ Modelo guardado en backend/data/ux_model.h5")

if __name__ == "__main__":
    main()