import json
import numpy as np
from sklearn.preprocessing import LabelEncoder
import joblib

class DataProcessor:
    def __init__(self):
        # ===== PARA DATOS DE DISEÑO UX =====
        self.good_palettes = [
            ["#000000", "#FFFFFF", "#3498DB"],
            ["#2C3E50", "#ECF0F1", "#E74C3C"],
            ["#1ABC9C", "#FFFFFF", "#34495E"],
            ["#F39C12", "#FFFFFF", "#2C3E50"],
            ["#9B59B6", "#FFFFFF", "#2C3E50"],
        ]
        
        self.bad_palettes = [
            ["#FF00FF", "#FFFF00", "#00FFFF"],
            ["#FF0000", "#00FF00", "#0000FF"],
            ["#8B4513", "#556B2F", "#2F4F4F"],
            ["#FFC0CB", "#FFB6C1", "#FFE4E1"],
            ["#000000", "#111111", "#222222"],
        ]
        
        self.good_fonts = [
            "Roboto", "Open Sans", "Montserrat", "Lato", "Inter", 
            "Source Sans Pro", "Poppins", "Nunito", "Work Sans", "IBM Plex Sans",
            "Georgia", "Helvetica", "Arial"
        ]
        
        self.bad_fonts = [
            "Comic Sans MS", "Papyrus", "Curlz MT", "Jokerman", 
            "Impact", "Courier New", "Brush Script"
        ]
        
        self.good_layouts = ["grid", "flex", "masonry", "card-based", "sidebar"]
        self.bad_layouts = ["table", "frame", "absolute", "inline"]
        
        self.good_spacing = ["medium", "wide", "comfortable", "standard"]
        self.neutral_spacing = ["compact"]
        self.bad_spacing = ["none", "cramped", "excessive"]
        
        self.good_contrast = ["high", "medium-high", "accessible"]
        self.bad_contrast = ["low", "none", "inverted"]
        
        # ===== PARA DATOS DE BRANDING =====
        self.color_palettes = self._load_color_palettes()
        self.fonts_catalog = self._load_fonts()
        self.components = self._load_components()
        
    def _load_color_palettes(self):
        """Paletas de colores por sector"""
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
        }
    
    def _load_fonts(self):
        """Tipografías por estilo"""
        return {
            'tech': {'primary': 'Inter', 'secondary': 'Roboto Mono'},
            'creative': {'primary': 'Poppins', 'secondary': 'Montserrat'},
            'professional': {'primary': 'Roboto', 'secondary': 'Open Sans'},
            'elegant': {'primary': 'Playfair Display', 'secondary': 'Lato'},
            'modern': {'primary': 'Work Sans', 'secondary': 'Space Grotesk'},
            'minimal': {'primary': 'IBM Plex Sans', 'secondary': 'Source Sans Pro'},
        }
    
    def _load_components(self):
        """Estilos de componentes"""
        return {
            'modern': {
                'borderRadius': '12px',
                'buttonStyle': 'rounded',
                'buttonRadius': '12px',
                'cardRadius': '16px',
                'inputRadius': '12px',
                'shadowSize': 'medium',
                'shadow': '0 4px 6px -1px rgba(0, 0, 0, 0.1)',
                'spacing': 'spacious'
            },
            'minimal': {
                'borderRadius': '4px',
                'buttonStyle': 'sharp',
                'buttonRadius': '4px',
                'cardRadius': '8px',
                'inputRadius': '4px',
                'shadowSize': 'none',
                'shadow': 'none',
                'spacing': 'compact'
            },
            'soft': {
                'borderRadius': '24px',
                'buttonStyle': 'pill',
                'buttonRadius': '24px',
                'cardRadius': '20px',
                'inputRadius': '24px',
                'shadowSize': 'soft',
                'shadow': '0 2px 8px rgba(0, 0, 0, 0.08)',
                'spacing': 'comfortable'
            },
        }

    def _detect_input_type(self, data):
        """Detecta si es input de branding o diseño UX"""
        has_branding = any(k in data for k in ['name', 'mission', 'values', 'sector', 'audience'])
        has_ux_design = any(k in data for k in ['palette', 'fonts', 'layout', 'spacing', 'contrast'])
        
        if has_ux_design:
            return 'ux_design'
        elif has_branding:
            return 'branding'
        else:
            return 'unknown'

    def _convert_branding_to_ux(self, data):
        """Convierte datos de branding a formato UX design"""
        # Analizar keywords de branding
        full_text = (data.get('mission', '') + ' ' + data.get('values', '')).lower()
        keywords = self._analyze_keywords(full_text)
        sector = data.get('sector', 'general')
        
        # Generar paleta basada en keywords y sector
        if keywords.get('luxury'):
            palette = self.color_palettes['luxury'][:3]
        elif keywords.get('eco'):
            palette = self.color_palettes['eco_friendly'][:3]
        elif keywords.get('creative'):
            palette = self.color_palettes['creative_vibrant'][:3]
        elif keywords.get('professional'):
            palette = self.color_palettes['professional'][:3]
        else:
            sector_map = {
                'tecnología': 'tech_modern',
                'salud': 'health',
                'finanzas': 'finance',
                'educación': 'education',
                'entretenimiento': 'entertainment',
            }
            style = sector_map.get(sector, 'tech_modern')
            palette = self.color_palettes[style][:3]
        
        # Generar fuentes basada en keywords
        if keywords.get('luxury') or keywords.get('professional'):
            fonts = ["Georgia", "Helvetica"]
        elif keywords.get('creative'):
            fonts = ["Montserrat", "Poppins"]
        elif keywords.get('modern'):
            fonts = ["Inter", "Roboto"]
        else:
            fonts = ["Roboto", "Open Sans"]
        
        # Layout y spacing basados en keywords
        layout = "grid" if keywords.get('modern') else "flex"
        spacing = "wide" if keywords.get('creative') else "medium"
        contrast = "high" if keywords.get('professional') else "medium-high"
        
        # Crear objeto UX design
        ux_data = {
            'palette': palette,
            'fonts': fonts,
            'layout': layout,
            'spacing': spacing,
            'contrast': contrast
        }
        
        return ux_data, keywords

    def _analyze_keywords(self, text):
        """Analiza palabras clave en el texto"""
        text = text.lower()
        
        keywords = {
            'modern': any(kw in text for kw in ['modern', 'innovación', 'tecnología', 'digital', 'futuro', 'ia']),
            'professional': any(kw in text for kw in ['profesional', 'confianza', 'calidad', 'excelencia', 'serio']),
            'creative': any(kw in text for kw in ['creativo', 'arte', 'diseño', 'único', 'original']),
            'luxury': any(kw in text for kw in ['lujo', 'premium', 'exclusivo', 'élite', 'sofisticado']),
            'eco': any(kw in text for kw in ['sostenible', 'eco', 'verde', 'natural', 'orgánico', 'medio ambiente']),
        }
        
        return keywords

    # ===== MÉTODOS DE ANÁLISIS UX =====
    
    def _analyze_palette_quality(self, palette):
        """Analiza calidad de paleta"""
        if not palette or len(palette) == 0:
            return 0.0
        
        palette_str = str(sorted(palette))
        
        for good_pal in self.good_palettes:
            if str(sorted(good_pal)) == palette_str:
                return 1.0
        
        for bad_pal in self.bad_palettes:
            if str(sorted(bad_pal)) == palette_str:
                return 0.0
        
        score = 0.5
        has_light = any(self._is_light_color(c) for c in palette)
        has_dark = any(not self._is_light_color(c) for c in palette)
        if has_light and has_dark:
            score += 0.2
        
        if 3 <= len(palette) <= 5:
            score += 0.1
        
        saturated_count = sum(1 for c in palette if self._is_highly_saturated(c))
        if saturated_count >= 3:
            score -= 0.2
        
        return max(0.0, min(1.0, score))

    def _is_light_color(self, hex_color):
        """Determina si un color es claro"""
        try:
            hex_color = hex_color.replace("#", "")
            r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
            luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255
            return luminance > 0.5
        except:
            return False

    def _is_highly_saturated(self, hex_color):
        """Determina si un color está muy saturado"""
        try:
            hex_color = hex_color.replace("#", "")
            r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
            max_val = max(r, g, b)
            min_val = min(r, g, b)
            if max_val == 0:
                return False
            saturation = (max_val - min_val) / max_val
            return saturation > 0.8
        except:
            return False

    def _analyze_fonts_quality(self, fonts):
        """Analiza calidad de fuentes"""
        if not fonts or len(fonts) == 0:
            return 0.0
        
        score = 0.5
        good_count = sum(1 for font in fonts if any(gf.lower() in font.lower() for gf in self.good_fonts))
        bad_count = sum(1 for font in fonts if any(bf.lower() in font.lower() for bf in self.bad_fonts))
        
        if good_count > 0 and bad_count == 0:
            score = 1.0
        elif bad_count > 0 and good_count == 0:
            score = 0.0
        elif good_count > bad_count:
            score = 0.7
        elif bad_count > good_count:
            score = 0.3
        
        return score

    def _encode_layout(self, layout):
        """Codifica layout"""
        if layout in self.good_layouts:
            return 1.0
        elif layout in self.bad_layouts:
            return 0.0
        else:
            return 0.5

    def _encode_spacing(self, spacing):
        """Codifica spacing"""
        if spacing in self.good_spacing:
            return 1.0
        elif hasattr(self, 'neutral_spacing') and spacing in self.neutral_spacing:
            return 0.6
        elif spacing in self.bad_spacing:
            return 0.0
        else:
            return 0.5

    def _encode_contrast(self, contrast):
        """Codifica contraste"""
        if contrast in self.good_contrast:
            return 1.0
        elif contrast in self.bad_contrast:
            return 0.0
        else:
            return 0.5

    def encode_input(self, data):
        """
        Codifica datos de entrada (branding O diseño UX)
        Retorna: (features, metadata, extra1)
        """
        input_type = self._detect_input_type(data)
        
        # ✅ CONVERSIÓN: Si es branding, convertir a UX
        if input_type == 'branding':
            print(f"🔄 Convirtiendo datos de branding a diseño UX...")
            ux_data, keywords = self._convert_branding_to_ux(data)
            data = ux_data
        else:
            keywords = {}
        
        # Ahora procesar como UX design
        palette = data.get('palette', [])
        fonts = data.get('fonts', [])
        layout = data.get('layout', 'grid')
        spacing = data.get('spacing', 'medium')
        contrast = data.get('contrast', 'high')
        
        # Analizar cada aspecto
        palette_score = self._analyze_palette_quality(palette)
        fonts_score = self._analyze_fonts_quality(fonts)
        layout_score = self._encode_layout(layout)
        spacing_score = self._encode_spacing(spacing)
        contrast_score = self._encode_contrast(contrast)
        
        # Features adicionales
        palette_size = min(len(palette) / 5.0, 1.0) if palette else 0.0
        fonts_count = min(len(fonts) / 3.0, 1.0) if fonts else 0.0
        
        has_white = any('#FFF' in str(c).upper() or '#FFFFFF' in str(c).upper() for c in palette) if palette else False
        has_black = any('#000' in str(c).upper() or '#000000' in str(c).upper() for c in palette) if palette else False
        has_classic_combo = 1.0 if (has_white or has_black) else 0.5
        
        has_contrast_in_palette = 1.0 if (
            palette and 
            any(self._is_light_color(c) for c in palette) and 
            any(not self._is_light_color(c) for c in palette)
        ) else 0.0
        
        # Vector de features (14 dimensiones)
        features = [
            palette_score,
            fonts_score,
            layout_score,
            spacing_score,
            contrast_score,
            palette_size,
            fonts_count,
            has_classic_combo,
            has_contrast_in_palette,
            palette_score * contrast_score,
            fonts_score * layout_score,
            spacing_score * layout_score,
            (palette_score + fonts_score) / 2,
            (layout_score + spacing_score + contrast_score) / 3
        ]
        
        metadata = {
            'palette_quality': palette_score,
            'fonts_quality': fonts_score,
            'layout_quality': layout_score,
            'spacing_quality': spacing_score,
            'contrast_quality': contrast_score,
            'keywords': keywords,
            'converted_ux_data': data
        }
        
        print(f"🔑 Keywords extraídos: {[k for k, v in keywords.items() if v] if keywords else 'ninguno'}")
        
        return np.array(features).reshape(1, -1), metadata, None

    def generate_ui_kit(self, prediction, metadata, sector=None, audience=None):
        """Genera UI Kit basado en predicción"""
        confidence = float(prediction[0][0])
        
        # Extraer keywords y datos UX convertidos
        keywords = metadata.get('keywords', {})
        ux_data = metadata.get('converted_ux_data', {})
        
        # Usar los datos convertidos para generar el UI Kit
        palette = ux_data.get('palette', self.color_palettes['tech_modern'][:3])
        
        # Seleccionar fuentes
        if keywords.get('luxury'):
            fonts = self.fonts_catalog['elegant']
        elif keywords.get('creative'):
            fonts = self.fonts_catalog['creative']
        elif keywords.get('professional'):
            fonts = self.fonts_catalog['professional']
        else:
            fonts = self.fonts_catalog['modern']
        
        # Seleccionar componentes
        if keywords.get('modern'):
            components = self.components['modern']
        elif keywords.get('professional'):
            components = self.components['minimal']
        else:
            components = self.components['soft']
        
        # Generar UI Kit completo
        ui_kit = {
            'colors': {
                'primary': palette[0] if len(palette) > 0 else '#2DD4BF',
                'secondary': palette[1] if len(palette) > 1 else '#0F172A',
                'accent': palette[2] if len(palette) > 2 else '#3B82F6',
                'background': '#FFFFFF',
                'text': '#1E293B'
            },
            'typography': fonts,
            'components': components,
            'tokens': self._generate_design_tokens(components),
            'confidence': confidence,
            'style': {
                'keywords': [k for k, v in keywords.items() if v] if keywords else []
            }
        }
        
        return ui_kit

    def _generate_design_tokens(self, components):
        """Genera tokens de diseño"""
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
                'md': '16px',
                'lg': '18px',
                'xl': '24px',
                'xxl': '32px'
            }
        }