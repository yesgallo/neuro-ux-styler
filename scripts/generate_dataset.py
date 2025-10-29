
import json

# 10 ejemplos base
base_examples = [
  {
    "input": {
      "name": "EcoCart",
      "mission": "Hacer el comercio electrónico más sostenible",
      "values": "sostenibilidad, transparencia, innovación",
      "audience": "millennials conscientes del medio ambiente",
      "sector": "e-commerce"
    },
    "output": {
      "palette": ["#10B981", "#D97706", "#F9FAFB", "#F3F4F6", "#1F2937"],
      "font": "Inter",
      "tokens": {
        "radii": "8px",
        "spacing": "16px",
        "shadow": "0 1px 2px 0 rgba(0,0,0,0.05)"
      }
    }
  },
  {
    "input": {
      "name": "FinTrust",
      "mission": "Brindar servicios financieros seguros y transparentes",
      "values": "confianza, seguridad, profesionalismo",
      "audience": "empresas y profesionales",
      "sector": "fintech"
    },
    "output": {
      "palette": ["#1E40AF", "#0E7490", "#F3F4F6", "#9CA3AF", "#111827"],
      "font": "Roboto",
      "tokens": {
        "radii": "4px",
        "spacing": "12px",
        "shadow": "0 2px 4px 0 rgba(0,0,0,0.1)"
      }
    }
  },
  {
    "input": {
      "name": "TechNova",
      "mission": "Desarrollar herramientas tecnológicas innovadoras",
      "values": "innovación, eficiencia, minimalismo",
      "audience": "desarrolladores y startups",
      "sector": "software"
    },
    "output": {
      "palette": ["#7C3AED", "#EC4899", "#000000", "#111827", "#F9FAFB"],
      "font": "Manrope",
      "tokens": {
        "radii": "6px",
        "spacing": "14px",
        "shadow": "0 4px 6px -1px rgba(0,0,0,0.1)"
      }
    }
  },
  {
    "input": {
      "name": "LuxeStyle",
      "mission": "Ofrecer moda de alta gama sostenible",
      "values": "lujo, elegancia, exclusividad",
      "audience": "clientes premium",
      "sector": "moda"
    },
    "output": {
      "palette": ["#D4AF37", "#000000", "#FFFFFF", "#F5F5F5", "#212121"],
      "font": "Playfair Display",
      "tokens": {
        "radii": "2px",
        "spacing": "18px",
        "shadow": "0 8px 16px rgba(0,0,0,0.15)"
      }
    }
  },
  {
    "input": {
      "name": "Mindful",
      "mission": "Promover el bienestar mental accesible",
      "values": "calma, empatía, crecimiento",
      "audience": "adultos jóvenes",
      "sector": "salud"
    },
    "output": {
      "palette": ["#60A5FA", "#F472B6", "#F0F9FF", "#E0F2FE", "#0F172A"],
      "font": "Nunito",
      "tokens": {
        "radii": "12px",
        "spacing": "20px",
        "shadow": "0 2px 8px rgba(96, 165, 250, 0.2)"
      }
    }
  },
  {
    "input": {
      "name": "EduPath",
      "mission": "Hacer la educación personalizada y accesible",
      "values": "aprendizaje, inclusión, futuro",
      "audience": "estudiantes de todas las edades",
      "sector": "educación"
    },
    "output": {
      "palette": ["#0D9488", "#F59E0B", "#F8FAFC", "#F1F5F9", "#0F172A"],
      "font": "Open Sans",
      "tokens": {
        "radii": "8px",
        "spacing": "16px",
        "shadow": "0 1px 3px rgba(0,0,0,0.1)"
      }
    }
  },
  {
    "input": {
      "name": "GameForge",
      "mission": "Crear experiencias de juego inmersivas",
      "values": "diversión, comunidad, creatividad",
      "audience": "gamers y streamers",
      "sector": "gaming"
    },
    "output": {
      "palette": ["#EF4444", "#8B5CF6", "#000000", "#111827", "#F1F5F9"],
      "font": "Poppins",
      "tokens": {
        "radii": "10px",
        "spacing": "14px",
        "shadow": "0 0 12px rgba(239, 68, 68, 0.3)"
      }
    }
  },
  {
    "input": {
      "name": "HomeEase",
      "mission": "Hogares inteligentes y cómodos",
      "values": "comodidad, tecnología, simplicidad",
      "audience": "familias modernas",
      "sector": "iot"
    },
    "output": {
      "palette": ["#6B7280", "#10B981", "#FFFFFF", "#F9FAFB", "#111827"],
      "font": "DM Sans",
      "tokens": {
        "radii": "12px",
        "spacing": "16px",
        "shadow": "0 4px 12px rgba(0,0,0,0.08)"
      }
    }
  },
  {
    "input": {
      "name": "Bloom",
      "mission": "Belleza natural y cuidado consciente",
      "values": "autenticidad, cuidado, suavidad",
      "audience": "mujeres 25-40",
      "sector": "belleza"
    },
    "output": {
      "palette": ["#F472B6", "#10B981", "#FEF9F9", "#FCE7E7", "#292525"],
      "font": "Quicksand",
      "tokens": {
        "radii": "16px",
        "spacing": "18px",
        "shadow": "0 2px 6px rgba(244, 114, 182, 0.2)"
      }
    }
  },
  {
    "input": {
      "name": "TravelJoy",
      "mission": "Experiencias de viaje únicas y auténticas",
      "values": "aventura, descubrimiento, libertad",
      "audience": "viajeros millennials",
      "sector": "turismo"
    },
    "output": {
      "palette": ["#F59E0B", "#059669", "#FEF3C7", "#FDE68A", "#1C1917"],
      "font": "Montserrat",
      "tokens": {
        "radii": "6px",
        "spacing": "16px",
        "shadow": "0 4px 8px rgba(245, 158, 11, 0.25)"
      }
    }
  }
]

# Generar 200 ejemplos
dataset = []
for i in range(20):
    for example in base_examples:
        new_example = example.copy()
        # Añadir variación en el público para evitar duplicados exactos
        audiences = [
            "millennials", "gen z", "profesionales", "familias", "emprendedores",
            "estudiantes", "jóvenes adultos", "clientes premium", "comunidades online", "usuarios globales"
        ]
        new_example["input"]["audience"] = audiences[i % len(audiences)]
        dataset.append(new_example)

# Guardar
with open("backend/data/dataset.json", "w", encoding="utf-8") as f:
    json.dump(dataset, f, indent=2, ensure_ascii=False)

print("✅ Dataset de 200 ejemplos generado en backend/data/dataset.json")