"""
Creador de PDFs de facturas - Versión mejorada con soporte completo
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from typing import Dict
import os


class PDFFactura:
    """Genera PDFs de facturas con diseño profesional y tipografía uniforme"""

    # Tipografía uniforme - Helvetica family
    FONT_TITLE = "Helvetica-Bold"
    FONT_NORMAL = "Helvetica"
    FONT_BOLD = "Helvetica-Bold"
    FONT_ITALIC = "Helvetica-Oblique"

    def __init__(self, output_dir: str = "facturas_generadas"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

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

        # Dibujar contenido
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

        c.save()
        return filepath

    def _dibujar_encabezado(self, c, datos, width, height):
        """Dibuja el encabezado de la factura"""
        # Recuadro del RUC y tipo de comprobante
        c.setStrokeColor(colors.black)
        c.setLineWidth(2)
        c.rect(width - 180, height - 120, 150, 90)

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
        """Dibuja información adicional de hotel"""
        y = height - 205
        hotel = datos['datos_hotel']

        c.setFont(self.FONT_BOLD, 9)
        c.drawString(30, y, "INFORMACIÓN ADICIONAL")

        y -= 15
        c.setFont(self.FONT_NORMAL, 8)
        c.drawString(30, y, f"CheckIn: {hotel['checkin'].strftime('%d-%m-%Y')}")
        c.drawString(150, y, f"CheckOut: {hotel['checkout'].strftime('%d-%m-%Y')}")
        c.drawString(280, y, f"Noches: {hotel['noches']}")

        y -= 12
        c.drawString(30, y, f"Reserva: {hotel['reserva']}")
        c.drawString(150, y, f"Huésped: {hotel['huesped'][:30]}")

        if hotel.get('codigo_grupo'):
            y -= 12
            c.drawString(30, y, f"Código de Grupo: {hotel['codigo_grupo']}")
            c.drawString(150, y, f"Nombre de Grupo: {hotel['nombre_grupo']}")

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
        """Dibuja la tabla de items"""
        # Ajustar posición inicial según si hay datos de hotel/seguro
        if datos.get('datos_hotel') or datos.get('datos_seguro'):
            y_start = height - 260
        else:
            y_start = height - 220

        # Encabezado de tabla
        c.setFillColor(colors.HexColor('#E8E8E8'))
        c.rect(30, y_start - 18, width - 60, 18, fill=True, stroke=False)

        c.setFillColor(colors.black)
        c.setFont(self.FONT_BOLD, 8)
        c.drawString(35, y_start - 12, "ITEM")
        c.drawString(65, y_start - 12, "DESCRIPCIÓN")
        c.drawString(320, y_start - 12, "UND")
        c.drawString(360, y_start - 12, "CANT.")
        c.drawString(410, y_start - 12, "P.UNIT")
        c.drawRightString(width - 35, y_start - 12, "TOTAL")

        # Items
        y = y_start - 35
        c.setFont(self.FONT_NORMAL, 8)

        for i, item in enumerate(datos['items']):
            if y < 220:  # Si no hay espacio, advertir
                c.setFont(self.FONT_ITALIC, 7)
                c.drawString(35, y, "... más items en página siguiente ...")
                break

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
