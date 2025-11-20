"""
Configuraciones de Layouts para Facturas Realistas
Basadas en análisis de facturas reales peruanas

Define 5 layouts principales extraídos de facturas reales:
1. COSTA_DEL_SOL - Estilo hotelero con rotación, headers azul marino
2. CASA_ANDINA - Minimalista limpio, fondo blanco
3. ESTELAR - Corporativo moderno con información detallada
4. YANACOCHA - Estilo robusto con fondo gris (minería/construcción)
5. PACIFICO_SEGUROS - Diseño especializado para seguros
"""

from typing import Dict, List, Any
from reportlab.lib import colors
import random


# ==========================================
# LAYOUTS REALES EXTRAÍDOS
# ==========================================

LAYOUT_COSTA_DEL_SOL = {
    "nombre": "Costa del Sol",
    "industria": "Hotelería",
    "caracteristicas": {
        # Fondo y colores
        "background_color": colors.white,
        "background_shading": None,

        # Logo
        "logo_position": ("bottom_left", 30, 50),  # Rotado
        "logo_size": 100,
        "logo_color": "1A237E",  # Azul marino oscuro

        # Encabezado
        "header_position": ("top_right", -180, -120),
        "header_box_color": colors.HexColor("#1A237E"),  # Azul marino
        "header_box_border": 3,
        "header_text_color": colors.white,

        # Fuentes
        "font_company": ("Helvetica-Bold", 12),
        "font_headers": ("Helvetica-Bold", 11),
        "font_content": ("Helvetica", 9),
        "font_small": ("Helvetica", 7),

        # Tabla
        "table_header_bg": colors.HexColor("#283593"),  # Azul índigo
        "table_header_text": colors.white,
        "table_border_color": colors.HexColor("#5C6BC0"),
        "table_border_width": 1.5,
        "table_columns": 7,  # Muchas columnas

        # QR
        "qr_position": ("top_right", -130, -50),
        "qr_size": 90,

        # Íconos
        "payment_icons_position": ("bottom_left", 30, 40),
        "contact_icons_color": "#1A237E",

        # Marca de agua
        "watermark_rotation": -45,
        "watermark_alpha": 0.06,
        "watermark_size": 60,

        # Orientación especial
        "rotation": 180,  # Documento rotado
        "layout_density": "high",  # Alta densidad de información
    }
}

LAYOUT_CASA_ANDINA = {
    "nombre": "Casa Andina",
    "industria": "Hotelería Premium",
    "caracteristicas": {
        # Fondo minimalista
        "background_color": colors.white,
        "background_shading": None,

        # Logo
        "logo_position": ("top_left", 40, -110),
        "logo_size": 85,
        "logo_color": "7B1FA2",  # Púrpura

        # Encabezado limpio
        "header_position": ("top_right", -180, -120),
        "header_box_color": colors.white,
        "header_box_border": 2,
        "header_text_color": colors.black,

        # Fuentes elegantes
        "font_company": ("Helvetica", 11),  # Sin bold
        "font_headers": ("Helvetica-Bold", 10),
        "font_content": ("Helvetica", 8),
        "font_small": ("Helvetica", 6),

        # Tabla minimalista
        "table_header_bg": colors.HexColor("#F5F5F5"),  # Gris muy claro
        "table_header_text": colors.black,
        "table_border_color": colors.HexColor("#E0E0E0"),
        "table_border_width": 0.5,
        "table_columns": 5,  # Columnas moderadas

        # QR discreto
        "qr_position": ("bottom_right", -130, 55),
        "qr_size": 70,

        # Íconos sutiles
        "payment_icons_position": ("bottom_left", 40, 35),
        "contact_icons_color": "#9E9E9E",  # Gris

        # Marca de agua sutil
        "watermark_rotation": 45,
        "watermark_alpha": 0.04,
        "watermark_size": 50,

        # Normal
        "rotation": 0,
        "layout_density": "low",  # Baja densidad, espacioso
    }
}

LAYOUT_ESTELAR = {
    "nombre": "Estelar San Isidro",
    "industria": "Hotelería Corporativa",
    "caracteristicas": {
        # Fondo corporativo
        "background_color": colors.HexColor("#FAFAFA"),
        "background_shading": "light",

        # Logo corporativo
        "logo_position": ("top_left", 35, -115),
        "logo_size": 95,
        "logo_color": "0277BD",  # Azul corporativo

        # Encabezado detallado
        "header_position": ("top_right", -190, -130),
        "header_box_color": colors.HexColor("#01579B"),
        "header_box_border": 2.5,
        "header_text_color": colors.white,

        # Fuentes corporativas
        "font_company": ("Helvetica-Bold", 11),
        "font_headers": ("Helvetica-Bold", 10),
        "font_content": ("Helvetica", 8),
        "font_small": ("Helvetica-Oblique", 7),

        # Tabla corporativa
        "table_header_bg": colors.HexColor("#0288D1"),
        "table_header_text": colors.white,
        "table_border_color": colors.HexColor("#4FC3F7"),
        "table_border_width": 1,
        "table_columns": 6,

        # QR estándar
        "qr_position": ("bottom_right", -125, 50),
        "qr_size": 80,

        # Íconos corporativos
        "payment_icons_position": ("bottom_left", 35, 38),
        "contact_icons_color": "#0277BD",

        # Marca de agua corporativa
        "watermark_rotation": 45,
        "watermark_alpha": 0.05,
        "watermark_size": 55,

        # Normal
        "rotation": 0,
        "layout_density": "medium",
    }
}

LAYOUT_YANACOCHA = {
    "nombre": "Yanacocha / Minera",
    "industria": "Minería / Construcción",
    "caracteristicas": {
        # Fondo robusto gris
        "background_color": colors.HexColor("#E8E8E8"),
        "background_shading": "medium_gray",

        # Logo robusto
        "logo_position": ("top_left", 30, -120),
        "logo_size": 100,
        "logo_color": "F57C00",  # Naranja/amarillo

        # Encabezado robusto
        "header_position": ("top_right", -185, -125),
        "header_box_color": colors.HexColor("#424242"),  # Gris oscuro
        "header_box_border": 3,
        "header_text_color": colors.white,

        # Fuentes robustas
        "font_company": ("Helvetica-Bold", 12),
        "font_headers": ("Helvetica-Bold", 11),
        "font_content": ("Helvetica-Bold", 9),  # Bold en contenido
        "font_small": ("Helvetica", 7),

        # Tabla robusta
        "table_header_bg": colors.HexColor("#616161"),  # Gris medio
        "table_header_text": colors.white,
        "table_border_color": colors.HexColor("#424242"),
        "table_border_width": 2,
        "table_columns": 6,

        # QR grande
        "qr_position": ("bottom_left", 35, 45),  # Izquierda en vez de derecha
        "qr_size": 95,

        # Íconos robustos
        "payment_icons_position": ("bottom_right", -150, 40),  # Invertido
        "contact_icons_color": "#424242",

        # Marca de agua robusta
        "watermark_rotation": -50,
        "watermark_alpha": 0.08,
        "watermark_size": 65,

        # Normal
        "rotation": 0,
        "layout_density": "high",
    }
}

LAYOUT_PACIFICO_SEGUROS = {
    "nombre": "Pacífico Seguros",
    "industria": "Seguros",
    "caracteristicas": {
        # Fondo limpio
        "background_color": colors.white,
        "background_shading": None,

        # Logo seguros
        "logo_position": ("top_left", 35, -105),
        "logo_size": 80,
        "logo_color": "388E3C",  # Verde seguros

        # Encabezado especializado
        "header_position": ("top_right", -175, -115),
        "header_box_color": colors.HexColor("#2E7D32"),
        "header_box_border": 2,
        "header_text_color": colors.white,

        # Fuentes profesionales
        "font_company": ("Helvetica", 10),
        "font_headers": ("Helvetica-Bold", 9),
        "font_content": ("Helvetica", 8),
        "font_small": ("Helvetica-Oblique", 6),

        # Tabla especializada
        "table_header_bg": colors.HexColor("#4CAF50"),
        "table_header_text": colors.white,
        "table_border_color": colors.HexColor("#81C784"),
        "table_border_width": 1,
        "table_columns": 4,  # Pocas columnas (seguros simples)

        # QR centrado abajo
        "qr_position": ("bottom_center", 0, 50),  # Centrado
        "qr_size": 75,

        # Íconos especializados
        "payment_icons_position": ("bottom_left", 35, 35),
        "contact_icons_color": "#388E3C",

        # Marca de agua sutil
        "watermark_rotation": 40,
        "watermark_alpha": 0.05,
        "watermark_size": 52,

        # Normal
        "rotation": 0,
        "layout_density": "low",  # Seguros tienen menos líneas de detalle
    }
}


# ==========================================
# REGISTRO DE LAYOUTS
# ==========================================

LAYOUTS_DISPONIBLES = {
    "costa_del_sol": LAYOUT_COSTA_DEL_SOL,
    "casa_andina": LAYOUT_CASA_ANDINA,
    "estelar": LAYOUT_ESTELAR,
    "yanacocha": LAYOUT_YANACOCHA,
    "pacifico_seguros": LAYOUT_PACIFICO_SEGUROS,
}


# ==========================================
# MAPEO POR TIPO DE EMPRESA
# ==========================================

LAYOUTS_POR_INDUSTRIA = {
    "hotel": ["casa_andina", "estelar"],
    "turismo": ["costa_del_sol", "estelar"],
    "construccion": ["yanacocha"],
    "seguro": ["pacifico_seguros"],
    "inmobiliaria": ["yanacocha", "estelar"],
    "general": ["casa_andina", "estelar"],
    "con_descuento": ["casa_andina", "estelar", "yanacocha"],
}


# ==========================================
# FUNCIONES AUXILIARES
# ==========================================

def obtener_layout_aleatorio(tipo_factura: str = None) -> Dict[str, Any]:
    """
    Retorna un layout aleatorio.
    Si se especifica tipo_factura, elige de los layouts apropiados para esa industria.

    Args:
        tipo_factura: 'hotel', 'turismo', 'construccion', 'seguro', etc.

    Returns:
        Diccionario con configuración de layout
    """
    if tipo_factura and tipo_factura in LAYOUTS_POR_INDUSTRIA:
        layout_keys = LAYOUTS_POR_INDUSTRIA[tipo_factura]
        layout_key = random.choice(layout_keys)
    else:
        layout_key = random.choice(list(LAYOUTS_DISPONIBLES.keys()))

    return LAYOUTS_DISPONIBLES[layout_key]


def obtener_layout_por_nombre(nombre: str) -> Dict[str, Any]:
    """
    Obtiene layout específico por nombre.

    Args:
        nombre: 'costa_del_sol', 'casa_andina', 'estelar', 'yanacocha', 'pacifico_seguros'

    Returns:
        Diccionario con configuración de layout

    Raises:
        KeyError: Si el nombre no existe
    """
    if nombre not in LAYOUTS_DISPONIBLES:
        raise KeyError(f"Layout '{nombre}' no encontrado. Disponibles: {list(LAYOUTS_DISPONIBLES.keys())}")

    return LAYOUTS_DISPONIBLES[nombre]


def listar_layouts() -> List[str]:
    """Retorna lista de nombres de layouts disponibles"""
    return list(LAYOUTS_DISPONIBLES.keys())


def obtener_info_layout(nombre: str) -> Dict[str, str]:
    """
    Obtiene información básica de un layout.

    Returns:
        Dict con 'nombre' e 'industria'
    """
    layout = obtener_layout_por_nombre(nombre)
    return {
        "nombre": layout["nombre"],
        "industria": layout["industria"]
    }


def calcular_posicion(base_pos: tuple, width: float, height: float) -> tuple:
    """
    Calcula posición absoluta desde configuración relativa.

    Args:
        base_pos: Tupla ('position_type', x, y) donde:
                  - 'top_left': (x, height + y)
                  - 'top_right': (width + x, height + y)
                  - 'bottom_left': (x, y)
                  - 'bottom_right': (width + x, y)
                  - 'bottom_center': (width/2 + x, y)
        width: Ancho de página
        height: Alto de página

    Returns:
        Tupla (x, y) en coordenadas absolutas
    """
    position_type, x_offset, y_offset = base_pos

    if position_type == "top_left":
        return (x_offset, height + y_offset)
    elif position_type == "top_right":
        return (width + x_offset, height + y_offset)
    elif position_type == "bottom_left":
        return (x_offset, y_offset)
    elif position_type == "bottom_right":
        return (width + x_offset, y_offset)
    elif position_type == "bottom_center":
        return (width / 2 + x_offset, y_offset)
    else:
        # Fallback
        return (x_offset, y_offset)


# ==========================================
# INFORMACIÓN DE LAYOUTS
# ==========================================

def imprimir_resumen_layouts():
    """Imprime resumen de todos los layouts disponibles"""
    print("=" * 60)
    print("LAYOUTS DISPONIBLES PARA FACTURAS")
    print("=" * 60)

    for key, layout in LAYOUTS_DISPONIBLES.items():
        print(f"\n📄 {layout['nombre']} ({key})")
        print(f"   Industria: {layout['industria']}")
        carac = layout['caracteristicas']
        print(f"   - Fondo: {carac.get('background_shading', 'blanco')}")
        print(f"   - Logo: {carac['logo_position'][0]} ({carac['logo_size']}px)")
        print(f"   - QR: {carac['qr_position'][0]} ({carac['qr_size']}px)")
        print(f"   - Columnas: {carac['table_columns']}")
        print(f"   - Densidad: {carac['layout_density']}")
        if carac.get('rotation', 0) != 0:
            print(f"   - ⚠️ Rotación: {carac['rotation']}°")

    print("\n" + "=" * 60)
    print(f"Total: {len(LAYOUTS_DISPONIBLES)} layouts diferentes")
    print("=" * 60)


if __name__ == "__main__":
    # Demo
    imprimir_resumen_layouts()

    print("\n\n🎲 Ejemplo de selección aleatoria:")
    for i in range(3):
        layout = obtener_layout_aleatorio()
        print(f"   {i+1}. {layout['nombre']} - {layout['industria']}")

    print("\n\n🏨 Ejemplo de selección por industria (hotel):")
    for i in range(3):
        layout = obtener_layout_aleatorio('hotel')
        print(f"   {i+1}. {layout['nombre']}")
