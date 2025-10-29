import tensorflow as tf
import pickle
import numpy as np
import os

# Cargar modelo al iniciar
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
model_path = os.path.join(BASE_DIR, "data", "ux_model.h5")
vectorizer_path = os.path.join(BASE_DIR, "data", "vectorizer.pkl")

model = tf.keras.models.load_model(model_path)
with open(vectorizer_path, 'rb') as f:
    vectorizer = pickle.load(f)

def generate_ux_kit(brand_input: dict):
    text = f"{brand_input['name']} {brand_input['mission']} {brand_input['values']} {brand_input['audience']} {brand_input['sector']}"
    X = vectorizer.transform([text]).toarray()
    y_pred = model.predict(X)[0]
    
    hex_palette = []
    for i in range(0, 15, 3):
        r = int(y_pred[i] * 255)
        g = int(y_pred[i+1] * 255)
        b = int(y_pred[i+2] * 255)
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        hex_palette.append(hex_color)
    
    return {
        "palette": {
            "primary": hex_palette[0],
            "secondary": hex_palette[1],
            "neutral": hex_palette[2:5]
        },
        "typography": {
            "family": "Inter",
            "importUrl": "https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap"
        },
        "tokens": {
            "radii": {"md": "8px"},
            "spacing": {"md": "16px"},
            "shadows": {"sm": "0 1px 2px 0 rgba(0,0,0,0.05)"}
        },
        "explanation": "UI Kit generado por red neuronal entrenada",
        "exports": {
            "css": ":root { --color-primary: " + hex_palette[0] + "; }",
            "json": {},
            "figma": {}
        }
    }