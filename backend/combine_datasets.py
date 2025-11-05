
import json
import os

def load_dataset(file_path, key=None):
    """Carga un dataset. Si key está definido, extrae esa clave del dict."""
    with open(file_path) as f:
        data = json.load(f)
        if isinstance(data, dict):
            if key is None:
                # Si no se especifica clave, intenta adivinar
                if 'training_data' in data:
                    key = 'training_data'
                else:
                    raise KeyError(f"No se especificó clave y no se encontró 'training_data' en {file_path}. Claves disponibles: {list(data.keys())}")
            if key in data:
                return data[key]
            else:
                raise KeyError(f"La clave '{key}' no existe en {file_path}. Claves disponibles: {list(data.keys())}")
        elif isinstance(data, list):
            return data
        else:
            raise ValueError(f"Formato no soportado en {file_path}: {type(data)}")

# Carga los datasets
training_data = load_dataset('data/training_data.json', key='training_data')
real_data = load_dataset('data/real_data.json')  
synthetic_data = load_dataset('data/synthetic_data.json', key='training_data')

# Combina
combined_data = training_data + real_data + synthetic_data

# Guarda
os.makedirs('data', exist_ok=True)
with open('data/combined_training_data.json', 'w') as f:
    json.dump(combined_data, f, indent=2)

print(f"✅ Dataset combinado: {len(combined_data)} ejemplos")
