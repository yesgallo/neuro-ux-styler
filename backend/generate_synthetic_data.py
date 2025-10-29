import json
import random
import os

# === BANCOS DE PALABRAS MEJORADOS ===

NAMES = [
    "Nexus", "Verve", "Aura", "Pulse", "Lume", "Strive", "Bloom", "Forge", "Echo", "Zenith",
    "Apex", "Orbit", "Vista", "Crest", "Motive", "Nova", "Trove", "Quill", "Rise", "Haven",
    "Flux", "Muse", "Kinetix", "Solis", "Aether", "Prism", "Vanta", "Lyra", "Onyx", "Cove",
    "CaseFile", "ShadowLine", "Verdict", "Clue", "Evidence", "Redacted", "ColdCase", "Dossier"
]

MISSION_TEMPLATES = [
    "Innovación {adjective} en el sector {sector} para {audience}",
    "Transformar el {sector} con enfoque en {value1} y {value2}",
    "Soluciones {adjective} que empoderan a {audience}",
    "Reimaginar el futuro del {sector} mediante {value1}",
    "Experiencias {adjective} diseñadas para {audience}",
    "Impulsar el crecimiento de {audience} con {value1} y {value2}",
    "Conectar a {audience} con el poder del {sector} {adjective}",
    "Liderar la revolución {adjective} en {sector}",
    "Desentrañar los secretos del {sector} con precisión y estilo",
    "Documentar la verdad del {sector} para {audience}"
]

ADJECTIVES = [
    "inteligente", "sostenible", "ética", "accesible", "futura", "humana", "ágil", "segura",
    "inclusiva", "eficiente", "creativa", "robusta", "transparente", "moderna", "confiable",
    "oscuro", "misterioso", "inmersivo", "cinematográfico", "retro", "minimalista", "lujoso"
]

# Valores + Estilos de diseño integrados
VALUES_AND_STYLES = [
    # Valores genéricos
    "innovación", "tecnología", "excelencia", "sostenibilidad", "naturaleza", "responsabilidad",
    "eco-friendly", "exclusividad", "elegancia", "calidad premium", "sofisticación", "salud",
    "confianza", "profesionalismo", "empatía", "seguridad", "crecimiento", "transparencia",
    "educación", "accesibilidad", "diversión", "creatividad", "comunidad", "originalidad",
    "pasión", "rapidez", "frescura", "motivación", "bienestar", "ética", "equidad", "rigor",
    "impacto", "autenticidad", "individualidad", "privacidad", "pureza", "eficacia", "estabilidad",
    
    # ESTILOS DE DISEÑO EXPLÍCITOS (¡clave para tu modelo!)
    "oscuro", "true crime", "archivo policial", "evidencia board", "tipografía serif",
    "texturas de papel envejecido", "minimalista", "neón cyberpunk", "retro años 80",
    "lujoso dorado", "grunge", "futurista", "handwritten", "monocromático", "alto contraste",
    "ilustraciones detalladas", "fotografía en blanco y negro", "glitch art", "vintage",
    "glassmorphism", "brutalismo web", "dark academia", "color blocking", "tipografía display"
]

SECTORS = [
    "tecnología", "salud", "finanzas", "educación", "entretenimiento", "moda", "alimentos",
    "medio ambiente", "fitness", "diseño", "recursos humanos", "ciencia", "movilidad",
    "transporte", "automotriz", "arte", "música", "pyme", "cosmética", "agro", "legal",
    "judicial", "construcción", "ciberseguridad", "bienestar", "energía", "turismo",
    "logística", "retail", "telecomunicaciones", "farmacéutico", "aeroespacial", "robótica",
    "ia", "blockchain", "gaming", "deportes", "ong", "gobierno", "true crime", "misterio",
    "periodismo", "historia", "forense"
]

AUDIENCES = [
    "empresas B2B", "consumidores conscientes", "clase alta", "pacientes", "empresas",
    "estudiantes", "jóvenes", "creadores", "urbanos ocupados", "deportistas",
    "familias urbanas", "startups", "instituciones académicas", "adultos mayores",
    "millennials", "emprendedores", "mujeres conscientes", "equipos de desarrollo",
    "clientes retail", "niños de 6 a 12 años", "ONGs", "gobiernos locales",
    "aficionados al misterio", "detectives aficionados", "comunidades de true crime"
]

# === FUNCIÓN PRINCIPAL ===

def generate_synthetic_entry():
    sector = random.choice(SECTORS)
    audience = random.choice(AUDIENCES)
    adjective = random.choice(ADJECTIVES)
    value1, value2 = random.sample(VALUES_AND_STYLES, 2)
    
    # Generar nombre (más temático si es true crime/misterio)
    if sector in ["true crime", "misterio", "forense", "judicial"]:
        name = random.choice([
            "CaseFile", "ShadowLine", "Verdict", "Clue", "Evidence", "Redacted", 
            "ColdCase", "Dossier", "TheTruth", "Unsolved", "ArchiveX", "BlackBox"
        ])
    else:
        base = random.choice(NAMES)
        suffix = random.choice(["Labs", "Studio", "Co", "Group", "Hub", ""])
        name = (base + suffix).strip()
    
    # Generar misión
    mission = random.choice(MISSION_TEMPLATES).format(
        adjective=adjective,
        sector=sector,
        audience=audience,
        value1=value1,
        value2=value2
    )
    
    # Generar 4-6 valores/estilos
    num_items = random.randint(4, 6)
    selected_items = random.sample(VALUES_AND_STYLES, num_items)
    
    return {
        "input": {
            "name": name,
            "mission": mission,
            "values": ", ".join(selected_items),
            "sector": sector,
            "audience": audience
        },
        "rating": round(random.uniform(0.75, 1.0), 2),
        "feedback": random.choice(["excelente", "muy bueno", "destacado", "inmersivo", "profesional", "auténtico"])
    }

def generate_dataset(num_samples=200, output_path="data/synthetic_data.json"):
    print(f"🧠 Generando {num_samples} ejemplos sintéticos con estilos de diseño...")
    
    data = []
    for _ in range(num_samples):
        data.append(generate_synthetic_entry())
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump({"training_data": data, "feedback_data": []}, f, ensure_ascii=False, indent=2)
    
    print(f"✅ Dataset guardado en: {output_path}")
    unique_sectors = set(entry['input']['sector'] for entry in data)
    print(f"📊 Sectores únicos: {len(unique_sectors)} | Ej: {list(unique_sectors)[:5]}")

if __name__ == "__main__":
    generate_dataset(num_samples=300, output_path="data/synthetic_data.json")