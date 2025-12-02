from dataclasses import dataclass
from reportlab.lib import colors
from reportlab.lib.colors import Color

@dataclass
class InvoiceStyle:
    """Configuración de estilo para la factura"""
    name: str
    
    # Fuentes
    font_title: str = "Helvetica-Bold"
    font_normal: str = "Helvetica"
    font_bold: str = "Helvetica-Bold"
    font_italic: str = "Helvetica-Oblique"
    
    # Tamaños de fuente
    size_title: int = 14
    size_subtitle: int = 12
    size_normal: int = 9
    size_small: int = 8
    
    # Colores
    color_primary: Color = colors.black
    color_secondary: Color = colors.HexColor('#2C3E50')
    color_background_header: Color = colors.HexColor('#E8E8E8')
    color_text_header: Color = colors.black
    
    # Alineaciones (left, center, right)
    align_header: str = "center"
    align_title: str = "right"
    
    # Márgenes y espaciado
    margin_x: int = 30
    line_height: int = 12

    # Nuevos atributos visuales
    border_color: Color = colors.black  # Color de los bordes de recuadros
    table_header_bg: Color = colors.HexColor('#E8E8E8')  # Fondo del encabezado de tablas
    table_header_text: Color = colors.black  # Color texto encabezado tabla
    alternating_row_colors: bool = False  # Si las filas de la tabla tienen colores alternos
    row_bg_color: Color = colors.HexColor('#F5F5F5')  # Color de fila alterna
    font_mono: str = "Courier"  # Fuente monoespaciada para datos numéricos alineados

# Estilos predefinidos

# 1. Estilo Clásico: Sobrio, estándar, ideal para facturación tradicional
ESTILO_CLASICO = InvoiceStyle(
    name="Clásico",
    color_primary=colors.black,
    color_secondary=colors.HexColor('#2C3E50'),
    color_background_header=colors.HexColor('#E8E8E8'),
    border_color=colors.black,
    table_header_bg=colors.HexColor('#E8E8E8'),
    table_header_text=colors.black
)

# 2. Estilo Moderno: Colores azules, diseño limpio, sin bordes pesados
ESTILO_MODERNO = InvoiceStyle(
    name="Moderno",
    font_title="Helvetica-Bold",
    font_normal="Helvetica",
    color_primary=colors.HexColor('#2980B9'),  # Azul moderno
    color_secondary=colors.HexColor('#34495E'),  # Azul oscuro grisáceo
    color_background_header=colors.HexColor('#D6EAF8'),  # Azul muy claro
    align_header="left",
    align_title="left",
    border_color=colors.HexColor('#BDC3C7'),  # Borde gris suave
    table_header_bg=colors.HexColor('#3498DB'),  # Encabezado tabla azul
    table_header_text=colors.white,  # Texto blanco en encabezado
    alternating_row_colors=True,  # Filas alternas para mejor lectura
    row_bg_color=colors.HexColor('#EBF5FB')  # Color fila alterna suave
)

# 3. Estilo Minimalista: Blanco y negro, fuentes monoespaciadas, sin fondos
ESTILO_MINIMALISTA = InvoiceStyle(
    name="Minimalista",
    font_title="Courier-Bold",
    font_normal="Courier",
    font_bold="Courier-Bold",
    font_italic="Courier-Oblique",
    font_mono="Courier",
    color_primary=colors.black,
    color_secondary=colors.grey,
    color_background_header=colors.white, # Sin fondo
    align_header="right",
    align_title="right",
    border_color=colors.black,
    table_header_bg=colors.white,
    table_header_text=colors.black,
    alternating_row_colors=False
)

# 4. Estilo Corporativo: Serio, tonos grises y azul marino, estructura sólida
ESTILO_CORPORATIVO = InvoiceStyle(
    name="Corporativo",
    font_title="Times-Bold",  # Fuente con serifa para toque formal
    font_normal="Times-Roman",
    font_bold="Times-Bold",
    font_italic="Times-Italic",
    color_primary=colors.HexColor('#1A5276'),  # Azul marino oscuro
    color_secondary=colors.HexColor('#566573'),  # Gris pizarra
    color_background_header=colors.HexColor('#EAEDED'),  # Gris muy claro
    align_header="center",
    align_title="center",
    border_color=colors.HexColor('#2E4053'),  # Borde oscuro
    table_header_bg=colors.HexColor('#212F3D'),  # Encabezado oscuro
    table_header_text=colors.white,
    alternating_row_colors=True,
    row_bg_color=colors.HexColor('#F2F4F4')
)

# 5. Estilo Creativo: Colores vibrantes, diseño más atrevido
ESTILO_CREATIVO = InvoiceStyle(
    name="Creativo",
    font_title="Helvetica-Bold",
    font_normal="Helvetica",
    color_primary=colors.HexColor('#8E44AD'),  # Púrpura
    color_secondary=colors.HexColor('#D35400'),  # Naranja quemado
    color_background_header=colors.HexColor('#F5EEF8'),  # Púrpura muy claro
    align_header="left",
    align_title="right",  # Título a la derecha para asimetría
    border_color=colors.HexColor('#AF7AC5'),
    table_header_bg=colors.HexColor('#9B59B6'),
    table_header_text=colors.white,
    alternating_row_colors=True,
    row_bg_color=colors.HexColor('#FEF9E7')  # Fondo crema suave
)

# 6. Estilo Industrial: Alto contraste, negro y amarillo, líneas gruesas
ESTILO_INDUSTRIAL = InvoiceStyle(
    name="Industrial",
    font_title="Helvetica-Bold",
    font_normal="Helvetica",
    color_primary=colors.black,
    color_secondary=colors.black,
    color_background_header=colors.HexColor('#F1C40F'),  # Amarillo seguridad
    align_header="left",
    align_title="left",
    border_color=colors.black,
    table_header_bg=colors.black,
    table_header_text=colors.HexColor('#F1C40F'),  # Texto amarillo sobre negro
    alternating_row_colors=False,
    line_height=14  # Un poco más espaciado
)

# Diccionario maestro de estilos disponibles
STYLES = {
    "clasico": ESTILO_CLASICO,
    "moderno": ESTILO_MODERNO,
    "minimalista": ESTILO_MINIMALISTA,
    "corporativo": ESTILO_CORPORATIVO,
    "creativo": ESTILO_CREATIVO,
    "industrial": ESTILO_INDUSTRIAL
}
