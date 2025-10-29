import json
import numpy as np
from sklearn.preprocessing import LabelEncoder
import joblib

class DataProcessor:
    def __init__(self):
        self.sector_encoder = LabelEncoder()
        self.audience_encoder = LabelEncoder()
        self.color_palettes = self._load_color_palettes()
        self.fonts = self._load_fonts()
        self.components = self._load_components()
        self.textures = self._load_textures()
        
    def _load_color_palettes(self):
        """Paletas de colores predefinidas (ampliadas)"""
        return {
            'tech_modern': ['#2DD4BF', '#0F172A', '#1E293B', '#F8FAFC', '#64748B'],
            'creative_vibrant': ['#F43F5E', '#8B5CF6', '#FCD34D', '#FFFFFF', '#1F2937'],
            'professional': ['#1E40AF', '#FFFFFF', '#F3F4F6', '#111827', '#6B7280'],
            'eco_friendly': ['#10B981', '#065F46', '#D1FAE5', '#FFFFFF', '#374151'],
            'luxury': ['#7C3AED', '#1F2937', '#F9FAFB', '#D4AF37', '#000000'],
            'health': ['#3B82F6', '#DBEAFE', '#FFFFFF', '#1E3A8A', '#60A5FA'],
            'finance': ['#059669', '#064E3B', '#ECFDF5', '#1F2937', '#10B981'],
            'education': ['#F59E0B', '#FBBF24', '#FEF3C7', '#78350F', '#FFFFFF'],
            'entertainment': ['#EC4899', '#BE185D', '#FCE7F3', '#831843', '#F472B6'],
            'minimal': ['#000000', '#FFFFFF', '#F5F5F5', '#737373', '#E5E5E5'],
            'true_crime': ['#0F172A', '#1E293B', '#334155', '#2DD4BF', '#F8FAFC'],
            'vintage': ['#2D1B0D', '#5C4033', '#C19A6B', '#F5F5DC', '#8B4513'],
            'dark_academia': ['#2B2D42', '#8D99AE', '#EDF2F4', '#EF233C', '#D90429'],
            'cyberpunk': ['#FF2E63', '#05D9E8', '#1A1A2E', '#16213E', '#FFFFFF']
        }
    
    def _load_fonts(self):
        """Tipografías gratuitas de Google Fonts (ampliadas)"""
        return {
            'tech': {'primary': 'Inter', 'secondary': 'Roboto Mono'},
            'creative': {'primary': 'Poppins', 'secondary': 'Montserrat'},
            'professional': {'primary': 'Roboto', 'secondary': 'Open Sans'},
            'elegant': {'primary': 'Playfair Display', 'secondary': 'Lato'},
            'modern': {'primary': 'Work Sans', 'secondary': 'Space Grotesk'},
            'minimal': {'primary': 'IBM Plex Sans', 'secondary': 'Source Sans Pro'},
            'friendly': {'primary': 'Nunito', 'secondary': 'Quicksand'},
            'bold': {'primary': 'Raleway', 'secondary': 'Oswald'},
            'true_crime': {'primary': 'Cinzel', 'secondary': 'IBM Plex Mono'},
            'vintage': {'primary': 'Cormorant Garamond', 'secondary': 'Libre Baskerville'},
            'cyberpunk': {'primary': 'Orbitron', 'secondary': 'Share Tech Mono'}
        }
    
    def _load_components(self):
        """Estilos de componentes (ampliados)"""
        return {
            'modern': {
                'borderRadius': '12px',
                'buttonStyle': 'rounded',
                'shadowSize': 'medium',
                'spacing': 'spacious'
            },
            'minimal': {
                'borderRadius': '4px',
                'buttonStyle': 'sharp',
                'shadowSize': 'none',
                'spacing': 'compact'
            },
            'soft': {
                'borderRadius': '24px',
                'buttonStyle': 'pill',
                'shadowSize': 'soft',
                'spacing': 'comfortable'
            },
            'corporate': {
                'borderRadius': '8px',
                'buttonStyle': 'squared',
                'shadowSize': 'subtle',
                'spacing': 'standard'
            },
            'true_crime': {
                'borderRadius': '0px',
                'buttonStyle': 'evidence-tag',
                'shadowSize': 'none',
                'spacing': 'tight'
            },
            'vintage': {
                'borderRadius': '6px',
                'buttonStyle': 'paper-cut',
                'shadowSize': 'paper',
                'spacing': 'classic'
            }
        }
    
    def _load_textures(self):
        """Texturas para fondos y elementos"""
        return {
            'true_crime': 'paper_crack.png',
            'vintage': 'paper_texture.jpg',
            'minimal': 'none',
            'default': 'none'
        }

    def _analyze_keywords(self, text):
        """Analiza palabras clave con soporte para nuevos estilos"""
        text = text.lower()
        
        style_definitions = {
            'modern': ['modern', 'innovación', 'tecnología', 'digital', 'futuro', 'ia', 'smart', 'ágil'],
            'professional': ['profesional', 'confianza', 'calidad', 'excelencia', 'serio', 'corporativo', 'seguro'],
            'creative': ['creativo', 'arte', 'diseño', 'único', 'original', 'imaginación', 'expresivo', 'artístico'],
            'friendly': ['amigable', 'cercano', 'accesible', 'simple', 'humano', 'cálido', 'fácil'],
            'luxury': ['lujo', 'premium', 'exclusivo', 'élite', 'sofisticado', 'elegante', 'dorado', 'alta gama'],
            'eco': ['sostenible', 'eco', 'verde', 'natural', 'orgánico', 'medio ambiente', 'reciclado', 'limpio'],
            'dark': ['oscuro', 'dark', 'nocturno', 'sombra', 'misterioso', 'forense', 'crimen'],
            'true_crime': ['true crime', 'crimen', 'evidencia', 'archivo policial', 'caso', 'detective', 'misterio', 'investigación', 'policía', 'dossier'],
            'vintage': ['vintage', 'retro', 'antiguo', 'clásico', 'años', 'papel envejecido', 'tipografía serif', 'histórico'],
            'cyberpunk': ['cyberpunk', 'neón', 'digital', 'glitch', 'futurista', 'hacker', 'matrix', 'sci-fi'],
            'minimalist': ['minimalista', 'simple', 'limpio', 'espacio en blanco', 'esencial', 'menos es más']
        }
        
        detected = {}
        for style, keywords in style_definitions.items():
            detected[style] = any(kw in text for kw in keywords)
        
        return detected

    def encode_input(self, data):
        """Codifica los datos de entrada para la red neuronal"""
        name_len = len(data.get('name', ''))
        mission_len = len(data.get('mission', ''))
        values_list = [v.strip() for v in data.get('values', '').split(',') if v.strip()]
        values_count = len(values_list)
        
        sector = data.get('sector', 'general')
        audience = data.get('audience', 'general')
        
        full_text = (data.get('mission', '') + ' ' + data.get('values', '')).lower()
        keywords = self._analyze_keywords(full_text)
        
        features = [
            min(name_len / 50.0, 1.0),
            min(mission_len / 300.0, 1.0),
            min(values_count / 8.0, 1.0),
            int(keywords.get('modern', False)),
            int(keywords.get('professional', False)),
            int(keywords.get('creative', False)),
            int(keywords.get('friendly', False)),
            int(keywords.get('luxury', False)),
            int(keywords.get('eco', False)),
            int(keywords.get('dark', False)),
            int(keywords.get('true_crime', False)),
            int(keywords.get('vintage', False)),
            int(keywords.get('cyberpunk', False)),
            int(keywords.get('minimalist', False))
        ]
        
        return np.array(features).reshape(1, -1), keywords, sector, audience

    def generate_ui_kit(self, prediction, keywords, sector, audience):
        """Genera el UI Kit basado en la predicción y análisis de estilo"""
        if keywords.get('true_crime') or keywords.get('dark'):
            color_style = 'true_crime'
            font_style = 'true_crime'
            component_style = 'true_crime'
            texture = self.textures['true_crime']
        elif keywords.get('vintage'):
            color_style = 'vintage'
            font_style = 'vintage'
            component_style = 'vintage'
            texture = self.textures['vintage']
        elif keywords.get('cyberpunk'):
            color_style = 'cyberpunk'
            font_style = 'cyberpunk'
            component_style = 'modern'
            texture = 'none'
        else:
            color_style = self._select_color_style(keywords, sector)
            font_style = self._select_font_style(keywords)
            component_style = self._select_component_style(keywords)
            texture = 'none'
        
        colors = self.color_palettes.get(color_style, self.color_palettes['minimal'])
        fonts = self.fonts.get(font_style, self.fonts['modern'])
        components = self.components.get(component_style, self.components['modern'])
        tokens = self._generate_design_tokens(colors, fonts, components)
        
        return {
            'colors': {
                'primary': colors[0],
                'secondary': colors[1],
                'accent': colors[2],
                'background': colors[3],
                'text': colors[4]
            },
            'typography': fonts,
            'components': components,
            'tokens': tokens,
            'confidence': float(prediction[0][0]),
            'style': {
                'color_style': color_style,
                'font_style': font_style,
                'component_style': component_style,
                'texture': texture
            }
        }

    def _select_color_style(self, keywords, sector):
        """Selecciona el estilo de color basado en keywords y sector"""
        sector_map = {
            'tecnología': 'tech_modern',
            'salud': 'health',
            'finanzas': 'finance',
            'educación': 'education',
            'entretenimiento': 'entertainment',
            'moda': 'luxury',
            'alimentos': 'eco_friendly',
            'medio ambiente': 'eco_friendly',
            'ciencia': 'tech_modern',
            'movilidad': 'tech_modern',
            'transporte': 'professional',
            'automotriz': 'luxury',
            'arte': 'creative_vibrant',
            'música': 'entertainment',
            'pyme': 'professional',
            'cosmética': 'luxury',
            'agro': 'eco_friendly',
            'legal': 'professional',
            'judicial': 'professional',
            'construcción': 'professional',
            'ciberseguridad': 'tech_modern',
            'bienestar': 'health',
            'energía': 'eco_friendly',
            'turismo': 'creative_vibrant',
            'logística': 'professional',
            'retail': 'creative_vibrant',
            'telecomunicaciones': 'tech_modern',
            'farmacéutico': 'health',
            'aeroespacial': 'tech_modern',
            'robótica': 'tech_modern',
            'ia': 'tech_modern',
            'blockchain': 'tech_modern',
            'gaming': 'entertainment',
            'deportes': 'health',
            'ong': 'eco_friendly',
            'gobierno': 'professional',
            'true crime': 'true_crime',
            'misterio': 'true_crime',
            'periodismo': 'professional',
            'historia': 'vintage',
            'forense': 'true_crime'
        }
        
        if keywords.get('luxury'):
            return 'luxury'
        elif keywords.get('eco'):
            return 'eco_friendly'
        elif keywords.get('creative'):
            return 'creative_vibrant'
        elif keywords.get('professional'):
            return 'professional'
        else:
            return sector_map.get(sector, 'tech_modern')
    
    def _select_font_style(self, keywords):
        """Selecciona el estilo de tipografía"""
        if keywords.get('luxury') or keywords.get('vintage'):
            return 'elegant'
        elif keywords.get('creative'):
            return 'creative'
        elif keywords.get('professional'):
            return 'professional'
        elif keywords.get('friendly'):
            return 'friendly'
        elif keywords.get('true_crime'):
            return 'true_crime'
        elif keywords.get('cyberpunk'):
            return 'cyberpunk'
        elif keywords.get('vintage'):
            return 'vintage'
        else:
            return 'modern'
    
    def _select_component_style(self, keywords):
        """Selecciona el estilo de componentes"""
        if keywords.get('modern'):
            return 'modern'
        elif keywords.get('professional'):
            return 'corporate'
        elif keywords.get('friendly'):
            return 'soft'
        elif keywords.get('true_crime'):
            return 'true_crime'
        elif keywords.get('vintage'):
            return 'vintage'
        else:
            return 'minimal'

    def _generate_design_tokens(self, colors, fonts, components):
        """Genera tokens de diseño completos"""
        return {
            'spacing': {
                'xs': '4px',
                'sm': '8px',
                'md': '16px',
                'lg': '24px',
                'xl': '32px'
            },
            'fontSize': {
                'xs': '12px',
                'sm': '14px',
                'base': '16px',
                'lg': '18px',
                'xl': '24px',
                'xxl': '32px'
            },
            'borderRadius': components['borderRadius'],
            'shadow': {
                'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
                'md': '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                'lg': '0 10px 15px -3px rgba(0, 0, 0, 0.1)'
            }
        }