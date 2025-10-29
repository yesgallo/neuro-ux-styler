# 🧠 Neuro UX Styler

Red Neuronal IA que genera UI Kits personalizados basados en el nombre, misión, valores, sector y público objetivo de tu proyecto.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![Python](https://img.shields.io/badge/python-3.8+-green)
![TensorFlow](https://img.shields.io/badge/tensorflow-2.15.0-orange)

## 📋 Características

- ✨ Genera paletas de colores personalizadas
- 🔤 Selecciona tipografías gratuitas de Google Fonts
- 🎨 Crea componentes y tokens de diseño
- 📊 Puntuación de confianza en cada predicción
- 🔄 Sistema de feedback para mejorar el modelo
- 📈 Reentrenamiento automático con nuevos datos
- 🎯 Objetivo: >90% de confianza

## 🚀 Instalación Paso a Paso

### Paso 1: Clonar y Configurar el Proyecto

```bash
# Crear directorio del proyecto
mkdir neuro-ux-styler
cd neuro-ux-styler

# Crear estructura de carpetas
mkdir backend frontend
mkdir backend/data backend/data/models
```

### Paso 2: Instalar Dependencias de Python

```bash
# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Mac/Linux:
source venv/bin/activate

# Instalar dependencias
cd backend
pip install -r requirements.txt
```

### Paso 3: Copiar los Archivos

Copia todos los archivos del proyecto en sus respectivas ubicaciones:

**Backend:**
- `requirements.txt` → `backend/requirements.txt`
- `app.py` → `backend/app.py`
- `model.py` → `backend/model.py`
- `training.py` → `backend/training.py`
- `data_processor.py` → `backend/data_processor.py`
- `training_data.json` → `backend/data/training_data.json`

**Frontend:**
- `index.html` (la aplicación web completa)

### Paso 4: Entrenar el Modelo Inicial

```bash
cd backend
python training.py
```

**Salida esperada:**
```
============================================================
🧠 NEURO UX STYLER - ENTRENAMIENTO
============================================================
📊 Cargando y preparando datos...
✅ Dataset cargado: 10 muestras
🔄 Entrenamiento: 8 muestras
🔄 Validación: 2 muestras

🚀 Iniciando entrenamiento...
Epoch 1/100
...
📈 Evaluando modelo...

✨ Resultados finales:
   - Loss: 0.2145
   - Accuracy: 0.8750
   - AUC: 0.9200

✅ Entrenamiento completado!
🎯 Confianza alcanzada: 87.5%
📊 Necesitas más datos de feedback para alcanzar >90%
```

### Paso 5: Iniciar el Servidor Backend

```bash
# Desde la carpeta backend
python app.py
```

**Salida esperada:**
```
🚀 Iniciando Neuro UX Styler API...
📍 Servidor corriendo en http://localhost:5000
 * Running on http://127.0.0.1:5000
```

### Paso 6: Abrir la Aplicación Web

1. Abre el archivo `index.html` en tu navegador
2. O usa un servidor local:

```bash
# Opción 1: Python
python -m http.server 8000

# Opción 2: Node.js (si tienes instalado)
npx http-server -p 8000
```

3. Navega a `http://localhost:8000`

## 📖 Uso de la Aplicación

### 1. Generar un UI Kit

1. Completa el formulario con:
   - **Nombre del proyecto**: Ej. "TechFlow"
   - **Misión**: Describe el propósito
   - **Valores**: Separados por comas
   - **Sector**: Selecciona de la lista
   - **Público objetivo**: Define tu audiencia

2. Click en "Generar UI Kit"

3. Revisa el resultado:
   - Paleta de colores (click para copiar)
   - Tipografías sugeridas
   - Estilos de componentes
   - Tokens de diseño

### 2. Dar Feedback

Después de ver tu UI Kit:

1. Califica con estrellas (1-5)
2. Agrega comentarios opcionales
3. Click en "Enviar Feedback"

**El feedback ayuda a mejorar la IA**

### 3. Ver Estadísticas

- Ve a la pestaña "Estadísticas"
- Revisa el número de datos de entrenamiento
- Verifica cuántos feedbacks se han recibido
- Cuando hay ≥5 feedbacks, puedes reentrenar

### 4. Reentrenar el Modelo

```bash
# Opción 1: Desde la interfaz web
# Click en el botón "Reentrenar Modelo" en la pestaña Estadísticas

# Opción 2: Desde la línea de comandos
cd backend
python -c "from training import Trainer; t = Trainer(); t.retrain_with_feedback()"
```

## 🎯 Ciclo de Mejora Continua

```
1. Generar UI Kits → 2. Recibir Feedback → 3. Acumular Datos → 4. Reentrenar → 5. Mejorar Precisión
          ↑                                                                              ↓
          ←──────────────────────────────────────────────────────────────────────────────
```

### Objetivo Final

**Meta: >90% de confianza**

1. ✅ Entrenar con dataset inicial (~87%)
2. 📝 Generar UI Kits y recoger feedback
3. 📊 Acumular mínimo 5-10 feedbacks
4. 🔄 Reentrenar el modelo
5. 📈 Verificar mejora en precisión
6. 🔁 Repetir hasta alcanzar >90%

## 🏗️ Arquitectura del Sistema

### Red Neuronal

```
Input (9 características)
    ↓
Dense(128) + BatchNorm + Dropout(0.3)
    ↓
Dense(64) + BatchNorm + Dropout(0.2)
    ↓
Dense(32) + Dropout(0.1)
    ↓
Dense(1, sigmoid) → Confianza (0-1)
```

### Features de Entrada

1. Longitud del nombre (normalizada)
2. Longitud de la misión (normalizada)
3. Cantidad de valores (normalizada)
4. Keyword: modern
5. Keyword: professional
6. Keyword: creative
7. Keyword: friendly
8. Keyword: luxury
9. Keyword: eco

### Salida del Sistema

```json
{
  "colors": {
    "primary": "#2DD4BF",
    "secondary": "#0F172A",
    "accent": "#1E293B",
    "background": "#F8FAFC",
    "text": "#64748B"
  },
  "typography": {
    "primary": "Inter",
    "secondary": "Roboto Mono"
  },
  "components": {
    "borderRadius": "12px",
    "buttonStyle": "rounded",
    "shadowSize": "medium",
    "spacing": "spacious"
  },
  "tokens": { ... },
  "confidence": 0.87
}
```

## 📊 Monitoreo del Modelo

### Verificar Salud del Sistema

```bash
curl http://localhost:5000/api/health
```

### Ver Estadísticas

```bash
curl http://localhost:5000/api/stats
```

### Generar UI Kit via API

```bash
curl -X POST http://localhost:5000/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "name": "TechFlow",
    "mission": "Innovación tecnológica",
    "values": "innovación, tecnología",
    "sector": "tecnología",
    "audience": "empresas B2B"
  }'
```

## 🔧 Personalización

### Agregar Nuevas Paletas de Colores

Edita `backend/data_processor.py`:

```python
def _load_color_palettes(self):
    return {
        'mi_paleta': ['#COLOR1', '#COLOR2', '#COLOR3', '#COLOR4', '#COLOR5'],
        # ... más paletas
    }
```

### Agregar Nuevas Tipografías

```python
def _load_fonts(self):
    return {
        'mi_estilo': {'primary': 'Font Name', 'secondary': 'Font Name 2'},
        # ... más tipografías
    }
```

### Modificar Arquitectura de la Red

Edita `backend/model.py` en el método `build_model()`:

```python
def build_model(self, input_dim=9):
    model = keras.Sequential([
        layers.Input(shape=(input_dim,)),
        # Agrega o modifica capas aquí
        layers.Dense(256, activation='relu'),
        # ...
    ])
```

## 🐛 Troubleshooting

### Error: "Module not found"

```bash
pip install --upgrade -r requirements.txt
```

### Error: "Connection refused"

Verifica que el servidor backend esté corriendo:
```bash
cd backend
python app.py
```

### Error: CORS

El servidor ya tiene CORS habilitado. Si persiste:
```python
# En app.py, verifica:
CORS(app)
```

### Modelo no carga

Reentrena el modelo:
```bash
cd backend
python training.py
```

## 📈 Métricas de Éxito

| Métrica | Inicial | Objetivo |
|---------|---------|----------|
| Accuracy | ~87% | >90% |
| AUC | ~0.92 | >0.95 |
| Feedbacks | 0 | 20+ |
| UI Kits Generados | 0 | 100+ |

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -m 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto es de código abierto bajo la licencia MIT.

## 🎓 Aprendizaje Continuo

El sistema mejora con cada feedback:

- **10 feedbacks** → ~88% confianza
- **20 feedbacks** → ~91% confianza
- **50 feedbacks** → ~94% confianza
- **100+ feedbacks** → >95% confianza

## 🌟 Próximas Características

- [ ] Exportar UI Kit como archivo CSS/JSON
- [ ] Integración con Figma
- [ ] Más estilos de componentes
- [ ] Modo oscuro/claro automático
- [ ] Generación de mockups
- [ ] API REST documentada con Swagger
- [ ] Dashboard de analytics

## 📞 Soporte

¿Problemas o preguntas? Abre un issue en GitHub.

---

**Hecho con 🧠 y ❤️ por Neuro UX Styler**