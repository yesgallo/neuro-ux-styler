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
        
    def _load_color_palettes(self):
        """Paletas de colores predefinidas"""
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
            'minimal': ['#000000', '#FFFFFF', '#F5F5F5', '#737373', '#E5E5E5']
        }
    
    def _load_fonts(self):
        """Tipografías gratuitas de Google Fonts"""
        return {
            'tech': {'primary': 'Inter', 'secondary': 'Roboto Mono'},
            'creative': {'primary': 'Poppins', 'secondary': 'Montserrat'},
            'professional': {'primary': 'Roboto', 'secondary': 'Open Sans'},
            'elegant': {'primary': 'Playfair Display', 'secondary': 'Lato'},
            'modern': {'primary': 'Work Sans', 'secondary': 'Space Grotesk'},
            'minimal': {'primary': 'IBM Plex Sans', 'secondary': 'Source Sans Pro'},
            'friendly': {'primary': 'Nunito', 'secondary': 'Quicksand'},
            'bold': {'primary': 'Raleway', 'secondary': 'Oswald'}
        }
    
    def _load_components(self):
        """Estilos de componentes"""
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
            }
        }
    
    def encode_input(self, data):
        """Codifica los datos de entrada para la red neuronal"""
        # Extraer características de texto
        name_len = len(data.get('name', ''))
        mission_len = len(data.get('mission', ''))
        values_count = len(data.get('values', '').split(','))
        
        # Codificar sector y audiencia
        sector = data.get('sector', 'general')
        audience = data.get('audience', 'general')
        
        # Análisis de palabras clave en misión y valores
        text = (data.get('mission', '') + ' ' + data.get('values', '')).lower()
        keywords = {
            'modern': any(word in text for word in ['modern', 'innovación', 'tecnología', 'digital']),
            'professional': any(word in text for word in ['profesional', 'confianza', 'calidad', 'excelencia']),
            'creative': any(word in text for word in ['creativo', 'arte', 'diseño', 'único']),
            'friendly': any(word in text for word in ['amigable', 'cercano', 'accesible', 'simple']),
            'luxury': any(word in text for word in ['lujo', 'premium', 'exclusivo', 'élite']),
            'eco': any(word in text for word in ['sostenible', 'eco', 'verde', 'natural', 'medio ambiente'])
        }
        
        # Vector de características
        features = [
            name_len / 100,  # Normalizado
            mission_len / 500,  # Normalizado
            values_count / 10,  # Normalizado
            int(keywords['modern']),
            int(keywords['professional']),
            int(keywords['creative']),
            int(keywords['friendly']),
            int(keywords['luxury']),
            int(keywords['eco'])
        ]
        
        return np.array(features).reshape(1, -1), keywords, sector, audience
    
    def generate_ui_kit(self, prediction, keywords, sector, audience):
        """Genera el UI Kit basado en la predicción"""
        # Seleccionar paleta de colores
        color_style = self._select_color_style(keywords, sector)
        colors = self.color_palettes.get(color_style, self.color_palettes['minimal'])
        
        # Seleccionar tipografías
        font_style = self._select_font_style(keywords)
        fonts = self.fonts.get(font_style, self.fonts['modern'])
        
        # Seleccionar componentes
        component_style = self._select_component_style(keywords)
        components = self.components.get(component_style, self.components['modern'])
        
        # Generar tokens de diseño
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
                'component_style': component_style
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
            'alimentos': 'eco_friendly'
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
        if keywords.get('luxury'):
            return 'elegant'
        elif keywords.get('creative'):
            return 'creative'
        elif keywords.get('professional'):
            return 'professional'
        elif keywords.get('friendly'):
            return 'friendly'
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