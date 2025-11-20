"""
Creador de PDFs de facturas - Versión mejorada con elementos visuales realistas
Incluye: logos, códigos QR, íconos de pago y contacto
Con soporte para layouts variables basados en facturas reales
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from typing import Dict, Optional
import os
import random

# Import layouts
from src.pdf_layouts import (
    obtener_layout_aleatorio,
    obtener_layout_por_nombre,
    calcular_posicion,
    LAYOUTS_DISPONIBLES
)

# Imports para elementos visuales (con manejo de errores)
try:
    import requests
    from PIL import Image
    from io import BytesIO
    ONLINE_RESOURCES_AVAILABLE = True
except ImportError:
    ONLINE_RESOURCES_AVAILABLE = False
    print("⚠️ requests/PIL no disponible. Instalar con: pip install requests pillow")

try:
    import qrcode
    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False
    print("⚠️ qrcode no disponible. Instalar con: pip install qrcode[pil]")


class PDFFactura:
    """Genera PDFs de facturas con diseño profesional, tipografía uniforme y elementos visuales

    Con soporte para layouts variables basados en facturas reales peruanas.
    """

    # Colores por tipo de empresa (usado para logos)
    EMPRESA_COLORES = {
        'TURISMO': '1976D2',
        'HOTEL': '7B1FA2',
        'CONSTRUCCION': 'F57C00',
        'SEGURO': '388E3C',
        'INMOBILIARIA': 'E53935',
        'RESTAURANTE': 'D84315',
        'TRANSPORTE': '0277BD',
    }

    def __init__(
        self,
        output_dir: str = "facturas_generadas",
        use_visual_elements: bool = True,
        layout_name: str = None,
        tipo_factura: str = None
    ):
        """
        Inicializa el generador de PDFs de facturas

        Args:
            output_dir: Directorio de salida para PDFs
            use_visual_elements: Si True, incluye logos, QR, íconos
            layout_name: Nombre específico de layout ('costa_del_sol', 'casa_andina', etc.)
                        Si None, selecciona aleatoriamente según tipo_factura
            tipo_factura: Tipo de factura ('hotel', 'seguro', etc.) para selección automática de layout
        """
        self.output_dir = output_dir
        self.use_visual_elements = use_visual_elements
        self.image_cache = {}  # Caché para imágenes descargadas
        os.makedirs(output_dir, exist_ok=True)

        # Seleccionar layout
        if layout_name:
            self.layout = obtener_layout_por_nombre(layout_name)
        else:
            self.layout = obtener_layout_aleatorio(tipo_factura)

        # Extraer características del layout
        self.layout_config = self.layout['caracteristicas']

        # Configurar fuentes del layout
        self.FONT_COMPANY = self.layout_config['font_company'][0]
        self.FONT_COMPANY_SIZE = self.layout_config['font_company'][1]
        self.FONT_HEADERS = self.layout_config['font_headers'][0]
        self.FONT_HEADERS_SIZE = self.layout_config['font_headers'][1]
        self.FONT_CONTENT = self.layout_config['font_content'][0]
        self.FONT_CONTENT_SIZE = self.layout_config['font_content'][1]
        self.FONT_SMALL = self.layout_config['font_small'][0]
        self.FONT_SMALL_SIZE = self.layout_config['font_small'][1]

        # Fallbacks para compatibilidad
        self.FONT_TITLE = self.FONT_HEADERS
        self.FONT_NORMAL = self.FONT_CONTENT
        self.FONT_BOLD = self.FONT_HEADERS
        self.FONT_ITALIC = "Helvetica-Oblique"

    # ========================================
    # MÉTODOS PARA ELEMENTOS VISUALES
    # ========================================

    def _descargar_imagen(self, url: str, max_retries: int = 2) -> Optional[BytesIO]:
        """Descarga imagen desde URL con caché y reintentos"""
        if not ONLINE_RESOURCES_AVAILABLE or not self.use_visual_elements:
            return None

        # Verificar caché
        if url in self.image_cache:
            cached = self.image_cache[url]
            cached.seek(0)  # Reset posición
            return cached

        # Descargar
        for intento in range(max_retries):
            try:
                response = requests.get(url, timeout=3)
                if response.status_code == 200:
                    img_data = BytesIO(response.content)
                    self.image_cache[url] = img_data
                    return img_data
            except Exception:
                if intento == max_retries - 1:
                    return None
                continue
        return None

    def _generar_logo_url(self, razon_social: str) -> str:
        """Genera URL de logo usando UI Avatars con color del layout"""
        # Limpiar y limitar nombre
        nombre = razon_social[:30].replace(" ", "+")

        # Usar color del layout
        bg_color = self.layout_config['logo_color']

        # Si no tiene color específico, buscar por tipo de empresa
        if bg_color == 'random' or not bg_color:
            for keyword, color in self.EMPRESA_COLORES.items():
                if keyword in razon_social.upper():
                    bg_color = color
                    break
            if bg_color == 'random':
                bg_color = 'random'

        return f"https://ui-avatars.com/api/?name={nombre}&size=200&background={bg_color}&color=fff&bold=true&font-size=0.4&rounded=true"

    def _generar_qr_local(self, datos_qr: str) -> Optional[BytesIO]:
        """Genera código QR localmente"""
        if not QR_AVAILABLE:
            return None

        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=2,
            )
            qr.add_data(datos_qr)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")

            buffer = BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            return buffer
        except Exception:
            return None

    def _dibujar_logo_fallback(self, c, razon_social: str, x: float, y: float, size: float):
        """Dibuja logo de respaldo cuando falla la descarga (círculo con iniciales)"""
        # Obtener iniciales
        palabras = razon_social.split()
        iniciales = ''.join([p[0] for p in palabras[:3]]).upper()

        # Dibujar círculo de fondo
        c.setFillColor(colors.HexColor('#2C3E50'))
        c.circle(x + size/2, y + size/2, size/2, fill=True, stroke=False)

        # Dibujar iniciales
        c.setFillColor(colors.white)
        c.setFont(self.FONT_BOLD, size/3)
        c.drawCentredString(x + size/2, y + size/2 - size/8, iniciales)
        c.setFillColor(colors.black)

    def _dibujar_logo_empresa(self, c, datos: Dict, width: float, height: float):
        """Dibuja logo de la empresa usando configuración del layout"""
        if not self.use_visual_elements:
            return

        razon_social = datos['emisor']['razon_social']
        logo_url = self._generar_logo_url(razon_social)

        # Obtener posición y tamaño del layout
        logo_x, logo_y = calcular_posicion(
            self.layout_config['logo_position'],
            width,
            height
        )
        logo_size = self.layout_config['logo_size']

        # Intentar descargar logo
        logo_data = self._descargar_imagen(logo_url)

        if logo_data:
            try:
                logo_data.seek(0)
                c.drawImage(
                    ImageReader(logo_data),
                    logo_x,
                    logo_y,
                    width=logo_size,
                    height=logo_size,
                    preserveAspectRatio=True,
                    mask='auto'
                )
                return
            except Exception:
                pass

        # Fallback: dibujar logo simple
        self._dibujar_logo_fallback(c, razon_social, logo_x, logo_y, logo_size)

    def _dibujar_qr_code(self, c, datos: Dict, width: float, height: float):
        """Dibuja código QR usando configuración del layout"""
        if not self.use_visual_elements:
            return

        # Datos del QR según formato SUNAT
        ruc = datos['emisor']['ruc']
        serie = datos['serie']
        numero = datos['numero']
        fecha = datos['fecha_emision'].strftime('%Y%m%d')
        total = f"{datos['total']:.2f}"
        qr_data = f"{ruc}|03|{serie}|{numero}|{fecha}|{total}"

        # Generar QR localmente
        qr_image = self._generar_qr_local(qr_data)

        if qr_image:
            try:
                # Obtener posición y tamaño del layout
                qr_x, qr_y = calcular_posicion(
                    self.layout_config['qr_position'],
                    width,
                    height
                )
                qr_size = self.layout_config['qr_size']

                qr_image.seek(0)
                c.drawImage(
                    ImageReader(qr_image),
                    qr_x,
                    qr_y,
                    width=qr_size,
                    height=qr_size,
                    preserveAspectRatio=True
                )

                # Texto debajo del QR
                c.setFont(self.FONT_ITALIC, 6)
                c.setFillColor(colors.grey)
                c.drawCentredString(qr_x + qr_size/2, qr_y - 8, "Escanea para verificar")
                c.setFillColor(colors.black)
            except Exception:
                pass

    def _dibujar_iconos_pago(self, c, datos: Dict, width: float, height: float):
        """Dibuja íconos de métodos de pago usando configuración del layout"""
        if not self.use_visual_elements or not ONLINE_RESOURCES_AVAILABLE:
            return

        payment_icons = [
            ('Visa', 'https://cdn.simpleicons.org/visa/1A1F71'),
            ('MC', 'https://cdn.simpleicons.org/mastercard/EB001B'),
            ('Cash', 'https://api.iconify.design/mdi/cash.svg?color=%23388E3C'),
        ]

        # Obtener posición del layout
        x_start, y = calcular_posicion(
            self.layout_config['payment_icons_position'],
            width,
            height
        )
        icon_size = 18
        spacing = 30

        # Etiqueta
        c.setFont(self.FONT_BOLD, 7)
        c.setFillColor(colors.grey)
        c.drawString(x_start, y + icon_size + 5, "Aceptamos:")

        # Dibujar íconos
        for i, (nombre, icon_url) in enumerate(payment_icons):
            icon_data = self._descargar_imagen(icon_url)
            if icon_data:
                try:
                    icon_data.seek(0)
                    c.drawImage(
                        ImageReader(icon_data),
                        x_start + (i * spacing),
                        y,
                        width=icon_size,
                        height=icon_size,
                        preserveAspectRatio=True,
                        mask='auto'
                    )
                except Exception:
                    # Fallback: mostrar texto
                    c.setFont(self.FONT_NORMAL, 6)
                    c.drawString(x_start + (i * spacing), y, nombre)

        c.setFillColor(colors.black)

    def _dibujar_pie_con_iconos(self, c, datos: Dict, width: float, height: float):
        """Pie de página con íconos de contacto usando color del layout"""
        if not self.use_visual_elements or not ONLINE_RESOURCES_AVAILABLE:
            return

        y = 20
        icon_size = 10

        # Obtener color de íconos del layout
        icon_color = self.layout_config['contact_icons_color'].replace('#', '%23')

        contactos = [
            ('phone', datos['emisor']['telefono'], f'https://api.iconify.design/mdi/phone.svg?color={icon_color}'),
            ('email', datos['emisor']['email'], f'https://api.iconify.design/mdi/email.svg?color={icon_color}'),
        ]

        x_start = width / 2 - 150
        spacing = 150

        for i, (tipo, texto, icon_url) in enumerate(contactos):
            x = x_start + (i * spacing)

            # Descargar y dibujar ícono
            icon_data = self._descargar_imagen(icon_url)
            if icon_data:
                try:
                    icon_data.seek(0)
                    c.drawImage(
                        ImageReader(icon_data),
                        x,
                        y - 2,
                        width=icon_size,
                        height=icon_size,
                        preserveAspectRatio=True,
                        mask='auto'
                    )
                except Exception:
                    pass

            # Texto al lado del ícono
            c.setFont(self.FONT_NORMAL, 7)
            c.setFillColor(colors.grey)
            c.drawString(x + icon_size + 3, y, texto[:30])

        c.setFillColor(colors.black)

    def _dibujar_marca_agua(self, c, datos: Dict, width: float, height: float):
        """Dibuja marca de agua usando configuración del layout"""
        if not self.use_visual_elements:
            return

        c.saveState()

        # Obtener configuración del layout
        rotation = self.layout_config['watermark_rotation']
        alpha = self.layout_config['watermark_alpha']
        size = self.layout_config['watermark_size']

        # Configurar transparencia y fuente
        c.setFillColor(colors.grey, alpha=alpha)
        c.setFont(self.FONT_BOLD, size)

        # Centrar y rotar
        c.translate(width/2, height/2)
        c.rotate(rotation)

        # Dibujar texto
        c.drawCentredString(0, 0, "FACTURA FICTICIA")

        c.restoreState()

    # ========================================
    # MÉTODOS ORIGINALES (MODIFICADOS)
    # ========================================

    def crear_factura(self, datos: Dict, filename: str = None) -> str:
        """
        Crea un PDF de factura

        Args:
            datos: Diccionario con todos los datos de la factura
            filename: Nombre del archivo (si None, se genera automático)

        Returns:
            Ruta del archivo generado
        """
        if filename is None:
            fecha_str = datos['fecha_emision'].strftime('%Y%m%d')
            tipo = datos.get('tipo_factura', 'general')
            filename = f"Factura_{tipo}_{datos['serie']}_{datos['numero']}_{fecha_str}.pdf"

        filepath = os.path.join(self.output_dir, filename)

        # Crear PDF
        c = canvas.Canvas(filepath, pagesize=A4)
        width, height = A4

        # ========================================
        # 0. FONDO DE PÁGINA (si el layout lo especifica)
        # ========================================
        if self.layout_config['background_shading']:
            c.setFillColor(self.layout_config['background_color'])
            c.rect(0, 0, width, height, fill=True, stroke=False)
            c.setFillColor(colors.black)  # Restaurar

        # ========================================
        # 1. ELEMENTOS VISUALES DE FONDO
        # ========================================
        self._dibujar_marca_agua(c, datos, width, height)

        # ========================================
        # 2. LOGO DE EMPRESA (antes del encabezado)
        # ========================================
        self._dibujar_logo_empresa(c, datos, width, height)

        # ========================================
        # 3. CONTENIDO PRINCIPAL (código original)
        # ========================================
        self._dibujar_encabezado(c, datos, width, height)
        self._dibujar_datos_emisor(c, datos, width, height)
        self._dibujar_datos_receptor(c, datos, width, height)

        # Datos específicos de hotel si aplica
        if datos.get('datos_hotel'):
            self._dibujar_info_hotel(c, datos, width, height)

        # Datos específicos de seguro si aplica
        if datos.get('datos_seguro'):
            self._dibujar_info_seguro(c, datos, width, height)

        self._dibujar_items(c, datos, width, height)

        # Descuentos si aplica
        if datos.get('descuento'):
            self._dibujar_descuentos(c, datos, width, height)

        # Dibujar totales y obtener posición final Y
        y_final_totales = self._dibujar_totales(c, datos, width, height)

        # Dibujar pie usando la posición Y del bloque anterior
        self._dibujar_pie(c, datos, width, height, y_inicial=y_final_totales)

        # ========================================
        # 4. ELEMENTOS VISUALES FINALES
        # ========================================
        self._dibujar_qr_code(c, datos, width, height)
        self._dibujar_iconos_pago(c, datos, width, height)
        self._dibujar_pie_con_iconos(c, datos, width, height)

        c.save()
        return filepath

    def _dibujar_encabezado(self, c, datos, width, height):
        """Dibuja el encabezado de la factura usando configuración del layout"""
        # Obtener configuración del layout
        header_box_color = self.layout_config['header_box_color']
        header_box_border = self.layout_config['header_box_border']
        header_text_color = self.layout_config['header_text_color']

        # Recuadro del RUC y tipo de comprobante
        c.setStrokeColor(header_box_color if header_box_color != colors.white else colors.black)
        c.setLineWidth(header_box_border)

        # Si el fondo del header no es blanco, rellenarlo
        if header_box_color != colors.white:
            c.setFillColor(header_box_color)
            c.rect(width - 180, height - 120, 150, 90, fill=True, stroke=True)
        else:
            c.rect(width - 180, height - 120, 150, 90, fill=False, stroke=True)

        # Configurar color de texto
        c.setFillColor(header_text_color)

        # RUC
        c.setFont(self.FONT_BOLD, 14)
        c.drawCentredString(width - 105, height - 45, "R.U.C.")

        c.setFont(self.FONT_BOLD, 13)
        c.drawCentredString(width - 105, height - 65, datos['emisor']['ruc'])

        # Tipo de comprobante
        c.setFont(self.FONT_BOLD, 12)
        c.drawCentredString(width - 105, height - 85, datos['tipo_comprobante'])

        # Número
        c.setFont(self.FONT_BOLD, 14)
        c.drawCentredString(width - 105, height - 105, datos['numero_factura'])

        # Restaurar color negro para el resto
        c.setFillColor(colors.black)

    def _dibujar_datos_emisor(self, c, datos, width, height):
        """Dibuja los datos del emisor"""
        y = height - 50

        c.setFont(self.FONT_BOLD, 12)
        razon_social = datos['emisor']['razon_social']
        # Truncar si es muy largo
        if len(razon_social) > 45:
            razon_social = razon_social[:42] + "..."
        c.drawString(30, y, razon_social)

        c.setFont(self.FONT_NORMAL, 9)
        y -= 15
        c.drawString(30, y, f"Dirección: {datos['emisor']['direccion'][:60]}")

        y -= 12
        c.drawString(30, y, f"Teléfono: {datos['emisor']['telefono']}")

        y -= 12
        c.drawString(30, y, f"Email: {datos['emisor']['email']}")

    def _dibujar_datos_receptor(self, c, datos, width, height):
        """Dibuja los datos del receptor y fecha"""
        y = height - 135

        # Línea separadora
        c.setStrokeColor(colors.grey)
        c.setLineWidth(0.5)
        c.line(30, y + 5, width - 30, y + 5)

        y -= 10

        c.setFont(self.FONT_BOLD, 9)
        c.drawString(30, y, "SEÑOR(ES):")
        c.setFont(self.FONT_NORMAL, 9)
        razon_cliente = datos['receptor']['razon_social']
        if len(razon_cliente) > 50:
            razon_cliente = razon_cliente[:47] + "..."
        c.drawString(100, y, razon_cliente)

        y -= 14
        c.setFont(self.FONT_BOLD, 9)
        c.drawString(30, y, "RUC:")
        c.setFont(self.FONT_NORMAL, 9)
        c.drawString(100, y, datos['receptor']['ruc'])

        y -= 14
        c.setFont(self.FONT_BOLD, 9)
        c.drawString(30, y, "DIRECCIÓN:")
        c.setFont(self.FONT_NORMAL, 9)
        direccion = datos['receptor']['direccion']
        if len(direccion) > 50:
            direccion = direccion[:47] + "..."
        c.drawString(100, y, direccion)

        # Fecha en el lado derecho
        y_fecha = height - 145
        c.setFont(self.FONT_BOLD, 9)
        c.drawRightString(width - 100, y_fecha, "FECHA EMISIÓN:")
        c.setFont(self.FONT_NORMAL, 9)
        c.drawRightString(width - 30, y_fecha, datos['fecha_emision'].strftime('%d/%m/%Y'))

        y_fecha -= 14
        c.setFont(self.FONT_BOLD, 9)
        c.drawRightString(width - 100, y_fecha, "MONEDA:")
        c.setFont(self.FONT_NORMAL, 9)
        c.drawRightString(width - 30, y_fecha, datos['nombre_moneda'])

        if datos.get('numero_contrato'):
            y_fecha -= 14
            c.setFont(self.FONT_BOLD, 9)
            c.drawRightString(width - 100, y_fecha, "CONTRATO:")
            c.setFont(self.FONT_NORMAL, 9)
            c.drawRightString(width - 30, y_fecha, datos['numero_contrato'])

        if datos.get('periodo_facturado'):
            y_fecha -= 14
            c.setFont(self.FONT_BOLD, 9)
            c.drawRightString(width - 100, y_fecha, "PERIODO:")
            c.setFont(self.FONT_NORMAL, 9)
            c.drawRightString(width - 30, y_fecha, datos['periodo_facturado'])

    def _dibujar_info_hotel(self, c, datos, width, height):
        """Dibuja información adicional de hotel con formato mejorado"""
        y = height - 205
        hotel = datos['datos_hotel']

        # Encabezado de sección con fondo
        c.setFillColor(colors.HexColor('#2C3E50'))
        c.rect(30, y - 2, width - 60, 16, fill=True, stroke=False)

        c.setFillColor(colors.white)
        c.setFont(self.FONT_BOLD, 9)
        c.drawString(35, y + 3, "Información adicional")

        c.setFillColor(colors.black)
        y -= 18

        # Datos de estadía
        c.setFont(self.FONT_BOLD, 8)
        c.drawString(30, y, "CheckIn:")
        c.setFont(self.FONT_NORMAL, 8)
        c.drawString(80, y, hotel['checkin'].strftime('%d-%m-%Y'))

        c.setFont(self.FONT_BOLD, 8)
        c.drawString(160, y, "CheckOut:")
        c.setFont(self.FONT_NORMAL, 8)
        c.drawString(215, y, hotel['checkout'].strftime('%d-%m-%Y'))

        y -= 12
        c.setFont(self.FONT_BOLD, 8)
        c.drawString(30, y, "Reserva:")
        c.setFont(self.FONT_NORMAL, 8)
        c.drawString(80, y, str(hotel['reserva']))

        y -= 12
        c.setFont(self.FONT_BOLD, 8)
        c.drawString(30, y, "Huésped:")
        c.setFont(self.FONT_NORMAL, 8)
        c.drawString(80, y, hotel['huesped'][:50])

        y -= 12
        c.setFont(self.FONT_BOLD, 8)
        c.drawString(30, y, "Noches:")
        c.setFont(self.FONT_NORMAL, 8)
        c.drawString(80, y, str(hotel['noches']))

        # Habitación
        if hotel.get('habitacion'):
            c.setFont(self.FONT_BOLD, 8)
            c.drawString(160, y, "Habitación:")
            c.setFont(self.FONT_NORMAL, 8)
            c.drawString(220, y, hotel['habitacion'])

        # Grupo (si existe)
        if hotel.get('codigo_grupo'):
            y -= 12
            c.setFont(self.FONT_BOLD, 8)
            c.drawString(30, y, "Código de Grupo:")
            c.setFont(self.FONT_NORMAL, 8)
            c.drawString(110, y, str(hotel['codigo_grupo']))

            c.setFont(self.FONT_BOLD, 8)
            c.drawString(200, y, "Nombre de Grupo:")
            c.setFont(self.FONT_NORMAL, 8)
            c.drawString(285, y, str(hotel['nombre_grupo']))

    def _dibujar_info_seguro(self, c, datos, width, height):
        """Dibuja información adicional de seguro"""
        y = height - 205
        seguro = datos['datos_seguro']

        c.setFont(self.FONT_BOLD, 9)
        c.drawString(30, y, "INFORMACIÓN DE PÓLIZA")

        y -= 15
        c.setFont(self.FONT_NORMAL, 8)
        c.drawString(30, y, f"Póliza: {seguro['numero_poliza']}")
        c.drawString(180, y, f"Documento: {seguro['numero_documento'][:25]}")

        y -= 12
        c.drawString(30, y, f"Giro: {seguro['giro']}")
        c.drawString(180, y, f"Vehículo: {seguro['vehiculo']}")

        y -= 12
        vig_inicio = seguro['vigencia_inicio'].strftime('%d/%m/%Y')
        vig_fin = seguro['vigencia_fin'].strftime('%d/%m/%Y')
        c.drawString(30, y, f"Vigencia: {vig_inicio} - {vig_fin}")

    def _dibujar_items(self, c, datos, width, height):
        """Dibuja la tabla de items con soporte para múltiples páginas"""
        # Ajustar posición inicial según si hay datos de hotel/seguro
        if datos.get('datos_hotel') or datos.get('datos_seguro'):
            y_start = height - 260
        else:
            y_start = height - 220

        # Función para dibujar encabezado de tabla usando layout
        def dibujar_encabezado_tabla(y_pos):
            # Usar colores del layout
            table_header_bg = self.layout_config['table_header_bg']
            table_header_text = self.layout_config['table_header_text']
            table_border_color = self.layout_config['table_border_color']
            table_border_width = self.layout_config['table_border_width']

            # Dibujar encabezado con colores del layout
            c.setFillColor(table_header_bg)
            c.setStrokeColor(table_border_color)
            c.setLineWidth(table_border_width)
            c.rect(30, y_pos - 18, width - 60, 18, fill=True, stroke=True)

            c.setFillColor(table_header_text)
            c.setFont(self.FONT_BOLD, 8)
            c.drawString(35, y_pos - 12, "ITEM")
            c.drawString(65, y_pos - 12, "DESCRIPCIÓN")
            c.drawString(320, y_pos - 12, "UND")
            c.drawString(360, y_pos - 12, "CANT.")
            c.drawString(410, y_pos - 12, "P.UNIT")
            c.drawRightString(width - 35, y_pos - 12, "TOTAL")

            c.setFillColor(colors.black)
            return y_pos - 35

        # Encabezado inicial
        y = dibujar_encabezado_tabla(y_start)
        c.setFont(self.FONT_NORMAL, 8)

        for i, item in enumerate(datos['items']):
            # Si no hay espacio suficiente, crear nueva página
            espacio_necesario = 15 if 'cargo_item' not in item else 25
            if y < (70 + espacio_necesario):
                # Pie de página de continuación
                c.setFont(self.FONT_ITALIC, 7)
                c.setFillColor(colors.grey)
                c.drawCentredString(width / 2, 50, f"Continúa en página siguiente... (Item {i+1}/{len(datos['items'])})")

                # Nueva página
                c.showPage()

                # Encabezado de nueva página
                c.setFont(self.FONT_BOLD, 12)
                c.drawString(30, height - 40, f"{datos['emisor']['razon_social'][:50]}")
                c.setFont(self.FONT_NORMAL, 9)
                c.drawString(30, height - 55, f"Factura: {datos['numero_factura']}")

                # Línea separadora
                c.setStrokeColor(colors.grey)
                c.line(30, height - 65, width - 30, height - 65)

                # Encabezado de tabla en nueva página
                y = dibujar_encabezado_tabla(height - 80)
                c.setFont(self.FONT_NORMAL, 8)
                c.setFillColor(colors.black)

            c.drawString(35, y, str(item['numero']))

            # Descripción (truncar si es muy larga)
            desc = item['descripcion']
            if len(desc) > 35:
                desc = desc[:32] + "..."
            c.drawString(65, y, desc)

            c.drawString(320, y, item['unidad'])

            # Cantidad con decimales si aplica
            if isinstance(item['cantidad'], float):
                c.drawRightString(395, y, f"{item['cantidad']:.3f}")
            else:
                c.drawRightString(395, y, str(item['cantidad']))

            c.drawRightString(455, y, f"{datos['simbolo_moneda']} {item['precio_unitario']:.2f}")
            c.drawRightString(width - 35, y, f"{datos['simbolo_moneda']} {item['valor_venta']:.2f}")

            # Si tiene cargo por item (hoteles), mostrarlo
            if 'cargo_item' in item and item['cargo_item'] > 0:
                y -= 10
                c.setFont(self.FONT_ITALIC, 7)
                c.drawString(65, y, f"Cargo al ítem")
                c.drawRightString(width - 35, y, f"+ {datos['simbolo_moneda']} {item['cargo_item']:.2f}")
                c.setFont(self.FONT_NORMAL, 8)

            y -= 15

        # Línea final de tabla
        c.setStrokeColor(colors.grey)
        c.setLineWidth(0.5)
        c.line(30, y + 5, width - 30, y + 5)

        return y

    def _dibujar_descuentos(self, c, datos, width, height):
        """Dibuja la tabla de descuentos si existe"""
        y = 195
        descuento = datos['descuento']

        c.setFont(self.FONT_BOLD, 9)
        c.drawString(30, y, "DESCUENTOS")

        y -= 15
        c.setFont(self.FONT_NORMAL, 8)

        # Encabezado de tabla de descuentos
        c.setFillColor(colors.HexColor('#F0F0F0'))
        c.rect(30, y - 12, width - 60, 12, fill=True, stroke=False)

        c.setFillColor(colors.black)
        c.setFont(self.FONT_BOLD, 7)
        c.drawString(35, y - 8, "DESCRIPCIÓN")
        c.drawString(200, y - 8, "GRAVADO")
        c.drawString(260, y - 8, "EXONER.")
        c.drawString(320, y - 8, "IGV")
        c.drawString(370, y - 8, "ICBPER")
        c.drawString(420, y - 8, "TOTAL")
        c.drawString(480, y - 8, "DETRAC.")

        y -= 20
        c.setFont(self.FONT_NORMAL, 7)
        c.drawString(35, y, descuento['descripcion'])
        c.drawString(200, y, f"{datos['simbolo_moneda']} {descuento['gravado']:.2f}")
        c.drawString(260, y, f"{datos['simbolo_moneda']} {descuento['exonerado']:.2f}")
        c.drawString(320, y, f"{datos['simbolo_moneda']} {descuento['igv']:.2f}")
        c.drawString(370, y, f"{datos['simbolo_moneda']} {descuento['icbper']:.2f}")
        c.drawString(420, y, f"{datos['simbolo_moneda']} {descuento['total']:.2f}")
        c.drawString(480, y, f"{datos['simbolo_moneda']} {descuento['detraccion']:.2f}")

    def _dibujar_totales(self, c, datos, width, height):
        """Dibuja los totales"""
        # Posición inicial aumentada para evitar superposiciones
        # ANTES: 300/320  →  AHORA: 340/360 (+40px)
        y = 340 if datos.get('descuento') else 360

        # Recuadro de totales
        x_inicio = width - 220

        # Op. Gravada
        c.setFont(self.FONT_BOLD, 9)
        c.drawString(x_inicio, y, "OP. GRAVADAS:")
        c.setFont(self.FONT_NORMAL, 9)
        c.drawRightString(width - 30, y, f"{datos['simbolo_moneda']} {datos['op_gravada']:.2f}")

        if datos.get('op_gratuitas', 0) > 0:
            y -= 18  # AUMENTADO: 14 → 16 → 18px
            c.setFont(self.FONT_BOLD, 9)
            c.drawString(x_inicio, y, "OP. GRATUITAS:")
            c.setFont(self.FONT_NORMAL, 9)
            c.drawRightString(width - 30, y, f"{datos['simbolo_moneda']} {datos['op_gratuitas']:.2f}")

        if datos['op_exonerada'] > 0:
            y -= 18  # AUMENTADO: 14 → 16 → 18px
            c.setFont(self.FONT_BOLD, 9)
            c.drawString(x_inicio, y, "OP. EXONERADAS:")
            c.setFont(self.FONT_NORMAL, 9)
            c.drawRightString(width - 30, y, f"{datos['simbolo_moneda']} {datos['op_exonerada']:.2f}")

        if datos['op_inafecta'] > 0:
            y -= 18  # AUMENTADO: 14 → 16 → 18px
            c.setFont(self.FONT_BOLD, 9)
            c.drawString(x_inicio, y, "OP. INAFECTAS:")
            c.setFont(self.FONT_NORMAL, 9)
            c.drawRightString(width - 30, y, f"{datos['simbolo_moneda']} {datos['op_inafecta']:.2f}")

        if datos.get('descuento'):
            y -= 18  # AUMENTADO: 14 → 16 → 18px
            c.setFont(self.FONT_BOLD, 9)
            c.drawString(x_inicio, y, "TOTAL DCTO GLOBAL:")
            c.setFont(self.FONT_NORMAL, 9)
            c.drawRightString(width - 30, y, f"{datos['simbolo_moneda']} {datos['descuento']['monto']:.2f}")

        y -= 18  # AUMENTADO: 14 → 16 → 18px (IGV)
        c.setFont(self.FONT_BOLD, 9)
        c.drawString(x_inicio, y, "IGV 18%:")
        c.setFont(self.FONT_NORMAL, 9)
        c.drawRightString(width - 30, y, f"{datos['simbolo_moneda']} {datos['igv']:.2f}")

        if datos.get('total_cargos', 0) > 0:
            y -= 18  # AUMENTADO: 14 → 16 → 18px
            c.setFont(self.FONT_BOLD, 9)
            c.drawString(x_inicio, y, "TOTAL CARGOS:")
            c.setFont(self.FONT_NORMAL, 9)
            c.drawRightString(width - 30, y, f"{datos['simbolo_moneda']} {datos['total_cargos']:.2f}")

        if datos.get('otros_cargos', 0) > 0:
            y -= 18  # AUMENTADO: 14 → 16 → 18px
            c.setFont(self.FONT_BOLD, 9)
            c.drawString(x_inicio, y, "OTROS CARGOS:")
            c.setFont(self.FONT_NORMAL, 9)
            c.drawRightString(width - 30, y, f"{datos['simbolo_moneda']} {datos['otros_cargos']:.2f}")

        # Total
        y -= 25  # AUMENTADO: 20 → 22 → 25px
        c.setFillColor(colors.HexColor('#E8E8E8'))
        # Aumentar padding y altura de casilla
        c.rect(x_inicio - 10, y - 4, 200, 26, fill=True, stroke=True)

        c.setFillColor(colors.black)
        c.setFont(self.FONT_BOLD, 11)
        c.drawString(x_inicio, y + 6, "IMPORTE TOTAL:")  # AUMENTADO: +3 → +5 → +6
        c.setFont(self.FONT_BOLD, 11)
        c.drawRightString(width - 30, y + 6, f"{datos['simbolo_moneda']} {datos['total']:.2f}")

        # Monto en letras
        y -= 40  # AUMENTADO: 30 → 35 → 40px
        c.setFont(self.FONT_BOLD, 8)
        c.drawString(30, y, "SON:")
        c.setFont(self.FONT_NORMAL, 8)

        # Dividir el texto si es muy largo
        texto_letras = datos['total_letras']
        max_chars = 75
        lineas_usadas = 1
        if len(texto_letras) > max_chars:
            # Partir en múltiples líneas
            palabras = texto_letras.split()
            lineas = []
            linea_actual = []
            longitud_actual = 0

            for palabra in palabras:
                if longitud_actual + len(palabra) < max_chars:
                    linea_actual.append(palabra)
                    longitud_actual += len(palabra) + 1
                else:
                    lineas.append(" ".join(linea_actual))
                    linea_actual = [palabra]
                    longitud_actual = len(palabra) + 1

            if linea_actual:
                lineas.append(" ".join(linea_actual))

            for i, linea in enumerate(lineas):
                c.drawString(60, y - (i * 10), linea)
            lineas_usadas = len(lineas)
        else:
            c.drawString(60, y, texto_letras)

        # Calcular posición Y final (después del "SON:")
        y_final = y - (lineas_usadas * 10) - 25  # AUMENTADO: 15px → 25px de margen

        return y_final

    def _dibujar_pie(self, c, datos, width, height, y_inicial=None):
        """Dibuja el pie de la factura"""
        # Usar y_inicial si se proporciona, sino usar posición por defecto
        # Asegurar que no baje más del margen inferior
        if y_inicial is not None:
            y = y_inicial - 5  # Solo 5px de separación ya que y_final tiene 25px de margen
            y = max(y, 160)  # AUMENTADO: 180 → 160px del fondo (más espacio disponible)
        else:
            y = 200

        # Forma de pago
        c.setFont(self.FONT_BOLD, 9)
        c.drawString(30, y, "FORMA DE PAGO:")
        c.setFont(self.FONT_NORMAL, 9)
        c.drawString(130, y, datos['forma_pago'])

        # Cuotas si es a crédito
        if datos['con_credito'] and datos['cuotas']:
            y -= 22  # AUMENTADO: 20 → 22px
            c.setFont(self.FONT_BOLD, 8)
            c.drawString(30, y, "DATOS DE CUOTA:")

            # Encabezado de tabla de cuotas
            y -= 15
            c.setFillColor(colors.HexColor('#F0F0F0'))
            c.rect(30, y - 10, 300, 12, fill=True, stroke=False)

            c.setFillColor(colors.black)
            c.setFont(self.FONT_BOLD, 7)
            c.drawString(35, y - 6, "Nº CUOTA")
            c.drawString(100, y - 6, "MONTO")
            c.drawString(200, y - 6, "FECHA VENCIMIENTO")

            y -= 18
            c.setFont(self.FONT_NORMAL, 8)
            for cuota in datos['cuotas']:
                texto = f"{cuota['numero']}"
                c.drawString(45, y, texto)
                c.drawString(100, y, f"{datos['simbolo_moneda']} {cuota['monto']:.2f}")
                c.drawString(200, y, cuota['fecha_vencimiento'].strftime('%d/%m/%Y'))
                y -= 12

                if y < 60:  # Si no hay espacio
                    break

        # Observaciones
        if datos.get('observaciones'):
            y = max(y - 20, 55)  # AUMENTADO: 15 → 20px, margen 60 → 55px
            c.setFont(self.FONT_BOLD, 8)
            c.drawString(30, y, "OBSERVACIONES:")
            c.setFont(self.FONT_NORMAL, 7)
            y -= 12  # AUMENTADO: 10 → 12px
            obs = datos['observaciones']
            if len(obs) > 80:
                # Partir en dos líneas
                c.drawString(35, y, obs[:80])
                y -= 10  # AUMENTADO: 8 → 10px
                c.drawString(35, y, obs[80:160])
            else:
                c.drawString(35, y, obs)

        # Pie de página
        c.setFont(self.FONT_ITALIC, 7)
        c.setFillColor(colors.grey)
        c.drawCentredString(width / 2, 35, "Representación impresa de la Factura Electrónica")
        c.drawCentredString(width / 2, 25, f"Generado el {datos['fecha_emision'].strftime('%d/%m/%Y a las %H:%M')}")


if __name__ == "__main__":
    from generator import FacturaGenerator

    # Test: generar facturas de diferentes tipos
    gen = FacturaGenerator()
    pdf_gen = PDFFactura(output_dir="test_pdfs")

    print("Generando factura de HOTEL...")
    factura_hotel = gen.generar_factura(tipo_factura='hotel', con_credito=True)
    archivo1 = pdf_gen.crear_factura(factura_hotel)
    print(f"✓ Hotel: {archivo1}")

    print("\nGenerando factura con DESCUENTOS...")
    factura_desc = gen.generar_factura(tipo_factura='con_descuento', con_credito=False)
    archivo2 = pdf_gen.crear_factura(factura_desc)
    print(f"✓ Descuento: {archivo2}")

    print("\nGenerando factura de SEGURO...")
    factura_seg = gen.generar_factura(tipo_factura='seguro')
    archivo3 = pdf_gen.crear_factura(factura_seg)
    print(f"✓ Seguro: {archivo3}")

    print("\nGenerando factura GENERAL...")
    factura_gen = gen.generar_factura(tipo_factura='general', categoria_items='construccion')
    archivo4 = pdf_gen.crear_factura(factura_gen)
    print(f"✓ General: {archivo4}")

    print("\n✅ Todas las pruebas completadas!")
