import json
import os
import numpy as np
import tensorflow_hub as hub
from sklearn.metrics.pairwise import cosine_similarity

# Cargar datos
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
PALETTES_PATH = os.path.join(BASE_DIR, "data", "palettes.json")
FONTS_PATH = os.path.join(BASE_DIR, "data", "typographies.json")

with open(PALETTES_PATH, "r", encoding="utf-8") as f:
    PALETTES = json.load(f)

with open(FONTS_PATH, "r", encoding="utf-8") as f:
    FONTS = json.load(f)

# Cargar modelo USE (solo una vez)
use_model = hub.load("https://tfhub.dev/google/universal-sentence-encoder/4")

def get_embedding(text: str):
    return use_model([text]).numpy()[0]

def find_closest_palette(embedding: np.ndarray):
    best_score = -1
    best_palette = PALETTES[0]
    for p in PALETTES:
        keywords = " ".join(p["keywords"] + p["sector"])
        kw_emb = get_embedding(keywords)
        score = cosine_similarity([embedding], [kw_emb])[0][0]
        if score > best_score:
            best_score = score
            best_palette = p
    return best_palette

def select_font(sector: str, values: str):
    text = f"{sector} {values}"
    emb = get_embedding(text)
    best_score = -1
    best_font = FONTS[0]
    for f in FONTS:
        attr_text = " ".join(f["attributes"])
        attr_emb = get_embedding(attr_text)
        score = cosine_similarity([emb], [attr_emb])[0][0]
        if score > best_score:
            best_score = score
            best_font = f
    return best_font

def generate_tokens():
    return {
        "spacing": {"xs": "4px", "sm": "8px", "md": "16px", "lg": "24px", "xl": "32px"},
        "radii": {"none": "0px", "sm": "4px", "md": "8px", "lg": "12px", "full": "9999px"},
        "shadows": {
            "sm": "0 1px 2px 0 rgba(0,0,0,0.05)",
            "md": "0 4px 6px -1px rgba(0,0,0,0.1)",
            "lg": "0 10px 15px -3px rgba(0,0,0,0.1)"
        },
        "opacity": {"disabled": "0.6"}
    }

def explain_choices(palette, font):
    return (
        f"Paleta inspirada en '{', '.join(palette['keywords'])}' para transmitir coherencia con tu sector. "
        f"Tipografía '{font['name']}' seleccionada por su alineación con los valores de tu marca."
    )

def to_css(palette, tokens):
    lines = [":root {"]
    for k, v in palette.items():
        if k in ["primary", "secondary"]:
            lines.append(f"  --color-{k}: {v};")
    for cat, vals in tokens.items():
        for name, val in vals.items():
            lines.append(f"  --{cat}-{name}: {val};")
    lines.append("}")
    return "\n".join(lines)

def to_figma_tokens(palette, typography, tokens):
    figma = {"color": {}, "fontFamily": {}, "spacing": {}, "radii": {}, "shadow": {}}
    figma["color"]["primary"] = {"value": palette["primary"]}
    figma["color"]["secondary"] = {"value": palette["secondary"]}
    figma["fontFamily"]["base"] = {"value": typography["name"]}
    for k, v in tokens["spacing"].items():
        figma["spacing"][k] = {"value": v}
    for k, v in tokens["radii"].items():
        figma["radii"][k] = {"value": v}
    return figma

def generate_ux_kit(brand_input: dict):
    full_text = f"{brand_input['mission']} {brand_input['values']} {brand_input['sector']}"
    emb = get_embedding(full_text)
    
    palette = find_closest_palette(emb)
    font = select_font(brand_input["sector"], brand_input["values"])
    tokens = generate_tokens()
    explanation = explain_choices(palette, font)
    
    css = to_css(palette, tokens)
    figma = to_figma_tokens(palette, font, tokens)
    json_export = {
        "palette": palette,
        "typography": font,
        "tokens": tokens
    }
    
    return {
        "palette": {
            "primary": palette["primary"],
            "secondary": palette["secondary"],
            "neutral": palette["neutral"]
        },
        "typography": {
            "family": font["name"],
            "importUrl": font["import"]
        },
        "tokens": tokens,
        "explanation": explanation,
        "exports": {
            "css": css,
            "json": json_export,
            "figma": figma
        }
    }