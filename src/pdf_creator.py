"""
Creador de PDFs de facturas
"""
from reportlab.lib.pagesizes import A4, letter
from reportlab.lib.units import mm, cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
from typing import Dict
import os


class PDFFactura:
    """Genera PDFs de facturas con diseño profesional"""

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
            filename = f"Factura_{datos['serie']}_{datos['numero']}_{fecha_str}.pdf"

        filepath = os.path.join(self.output_dir, filename)

        # Crear PDF
        c = canvas.Canvas(filepath, pagesize=A4)
        width, height = A4

        # Dibujar contenido
        self._dibujar_encabezado(c, datos, width, height)
        self._dibujar_datos_emisor(c, datos, width, height)
        self._dibujar_datos_receptor(c, datos, width, height)
        self._dibujar_items(c, datos, width, height)
        self._dibujar_totales(c, datos, width, height)
        self._dibujar_pie(c, datos, width, height)

        c.save()
        return filepath

    def _dibujar_encabezado(self, c, datos, width, height):
        """Dibuja el encabezado de la factura"""
        # Recuadro del RUC y tipo de comprobante
        c.setStrokeColor(colors.black)
        c.setLineWidth(2)
        c.rect(width - 180, height - 120, 150, 90)

        # Título del comprobante
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width - 105, height - 45, "RUC")

        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(width - 105, height - 65, datos['emisor']['ruc'])

        # Tipo de comprobante
        c.setFont("Helvetica-Bold", 14)
        c.drawCentredString(width - 105, height - 90, datos['tipo_comprobante'])

        # Número
        c.setFont("Helvetica-Bold", 16)
        c.drawCentredString(width - 105, height - 110, datos['numero_factura'])

    def _dibujar_datos_emisor(self, c, datos, width, height):
        """Dibuja los datos del emisor"""
        y = height - 60

        c.setFont("Helvetica-Bold", 14)
        c.drawString(30, y, datos['emisor']['razon_social'])

        c.setFont("Helvetica", 10)
        y -= 20
        c.drawString(30, y, f"Dirección: {datos['emisor']['direccion']}")

        y -= 15
        c.drawString(30, y, f"Teléfono: {datos['emisor']['telefono']}")

        y -= 15
        c.drawString(30, y, f"Email: {datos['emisor']['email']}")

    def _dibujar_datos_receptor(self, c, datos, width, height):
        """Dibuja los datos del receptor y fecha"""
        y = height - 150

        # Línea separadora
        c.setStrokeColor(colors.grey)
        c.setLineWidth(1)
        c.line(30, y + 10, width - 30, y + 10)

        c.setFont("Helvetica-Bold", 11)
        c.drawString(30, y, "SEÑOR(ES):")
        c.setFont("Helvetica", 10)
        c.drawString(120, y, datos['receptor']['razon_social'])

        y -= 18
        c.setFont("Helvetica-Bold", 11)
        c.drawString(30, y, "RUC:")
        c.setFont("Helvetica", 10)
        c.drawString(120, y, datos['receptor']['ruc'])

        y -= 18
        c.setFont("Helvetica-Bold", 11)
        c.drawString(30, y, "DIRECCIÓN:")
        c.setFont("Helvetica", 10)
        c.drawString(120, y, datos['receptor']['direccion'])

        # Fecha en el lado derecho
        y_fecha = height - 150
        c.setFont("Helvetica-Bold", 11)
        c.drawRightString(width - 120, y_fecha, "FECHA EMISIÓN:")
        c.setFont("Helvetica", 10)
        c.drawRightString(width - 30, y_fecha, datos['fecha_emision'].strftime('%d/%m/%Y'))

        y_fecha -= 18
        c.setFont("Helvetica-Bold", 11)
        c.drawRightString(width - 120, y_fecha, "MONEDA:")
        c.setFont("Helvetica", 10)
        c.drawRightString(width - 30, y_fecha, datos['nombre_moneda'])

        if datos.get('numero_contrato'):
            y_fecha -= 18
            c.setFont("Helvetica-Bold", 11)
            c.drawRightString(width - 120, y_fecha, "CONTRATO:")
            c.setFont("Helvetica", 10)
            c.drawRightString(width - 30, y_fecha, datos['numero_contrato'])

        if datos.get('periodo_facturado'):
            y_fecha -= 18
            c.setFont("Helvetica-Bold", 11)
            c.drawRightString(width - 120, y_fecha, "PERIODO:")
            c.setFont("Helvetica", 10)
            c.drawRightString(width - 30, y_fecha, datos['periodo_facturado'])

    def _dibujar_items(self, c, datos, width, height):
        """Dibuja la tabla de items"""
        y_start = height - 240

        # Encabezado de tabla
        c.setFillColor(colors.HexColor('#E0E0E0'))
        c.rect(30, y_start - 20, width - 60, 20, fill=True, stroke=False)

        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 9)
        c.drawString(35, y_start - 13, "ITEM")
        c.drawString(65, y_start - 13, "DESCRIPCIÓN")
        c.drawString(330, y_start - 13, "UND")
        c.drawString(380, y_start - 13, "CANT.")
        c.drawString(430, y_start - 13, "P.UNIT")
        c.drawRightString(width - 35, y_start - 13, "TOTAL")

        # Items
        y = y_start - 40
        c.setFont("Helvetica", 8)

        for i, item in enumerate(datos['items']):
            if y < 200:  # Si no hay espacio, advertir (en producción, crear nueva página)
                c.setFont("Helvetica-Italic", 8)
                c.drawString(35, y, "... continúa en página siguiente ...")
                break

            c.drawString(35, y, str(item['numero']))

            # Descripción (puede ser larga, truncar si es necesario)
            desc = item['descripcion']
            if len(desc) > 40:
                desc = desc[:37] + "..."
            c.drawString(65, y, desc)

            c.drawString(330, y, item['unidad'])
            c.drawRightString(415, y, str(item['cantidad']))
            c.drawRightString(470, y, f"{datos['simbolo_moneda']} {item['precio_unitario']:.2f}")
            c.drawRightString(width - 35, y, f"{datos['simbolo_moneda']} {item['valor_venta']:.2f}")

            y -= 18

        # Línea final de tabla
        c.setStrokeColor(colors.grey)
        c.line(30, y + 8, width - 30, y + 8)

        return y

    def _dibujar_totales(self, c, datos, width, height):
        """Dibuja los totales"""
        # Posición fija desde abajo
        y = 280

        # Recuadro de totales
        c.setStrokeColor(colors.black)
        c.setLineWidth(1)
        x_inicio = width - 230

        # Op. Gravada
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x_inicio, y, "OP. GRAVADA:")
        c.setFont("Helvetica", 10)
        c.drawRightString(width - 30, y, f"{datos['simbolo_moneda']} {datos['op_gravada']:.2f}")

        if datos['op_exonerada'] > 0:
            y -= 18
            c.setFont("Helvetica-Bold", 10)
            c.drawString(x_inicio, y, "OP. EXONERADA:")
            c.setFont("Helvetica", 10)
            c.drawRightString(width - 30, y, f"{datos['simbolo_moneda']} {datos['op_exonerada']:.2f}")

        if datos['op_inafecta'] > 0:
            y -= 18
            c.setFont("Helvetica-Bold", 10)
            c.drawString(x_inicio, y, "OP. INAFECTA:")
            c.setFont("Helvetica", 10)
            c.drawRightString(width - 30, y, f"{datos['simbolo_moneda']} {datos['op_inafecta']:.2f}")

        y -= 18
        c.setFont("Helvetica-Bold", 10)
        c.drawString(x_inicio, y, "IGV (18%):")
        c.setFont("Helvetica", 10)
        c.drawRightString(width - 30, y, f"{datos['simbolo_moneda']} {datos['igv']:.2f}")

        # Total
        y -= 25
        c.setFillColor(colors.HexColor('#E0E0E0'))
        c.rect(x_inicio - 10, y - 5, 210, 22, fill=True, stroke=True)

        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(x_inicio, y + 3, "TOTAL:")
        c.setFont("Helvetica-Bold", 12)
        c.drawRightString(width - 30, y + 3, f"{datos['simbolo_moneda']} {datos['total']:.2f}")

        # Monto en letras
        y -= 35
        c.setFont("Helvetica-Bold", 9)
        c.drawString(30, y, "SON:")
        c.setFont("Helvetica", 9)

        # Dividir el texto si es muy largo
        texto_letras = datos['total_letras']
        if len(texto_letras) > 80:
            # Partir en dos líneas
            palabras = texto_letras.split()
            linea1 = []
            linea2 = []
            longitud = 0
            for palabra in palabras:
                if longitud + len(palabra) < 80:
                    linea1.append(palabra)
                    longitud += len(palabra) + 1
                else:
                    linea2.append(palabra)

            c.drawString(65, y, " ".join(linea1))
            y -= 12
            c.drawString(65, y, " ".join(linea2))
        else:
            c.drawString(65, y, texto_letras)

    def _dibujar_pie(self, c, datos, width, height):
        """Dibuja el pie de la factura"""
        y = 180

        # Forma de pago
        c.setFont("Helvetica-Bold", 10)
        c.drawString(30, y, "FORMA DE PAGO:")
        c.setFont("Helvetica", 10)
        c.drawString(150, y, datos['forma_pago'])

        # Cuotas si es a crédito
        if datos['con_credito'] and datos['cuotas']:
            y -= 25
            c.setFont("Helvetica-Bold", 9)
            c.drawString(30, y, "CUOTAS:")

            y -= 15
            c.setFont("Helvetica", 8)
            for cuota in datos['cuotas']:
                texto = f"  Cuota {cuota['numero']}: {datos['simbolo_moneda']} {cuota['monto']:.2f} - Vencimiento: {cuota['fecha_vencimiento'].strftime('%d/%m/%Y')}"
                c.drawString(40, y, texto)
                y -= 12

        # Observaciones
        if datos.get('observaciones'):
            y -= 20
            c.setFont("Helvetica-Bold", 9)
            c.drawString(30, y, "OBSERVACIONES:")
            c.setFont("Helvetica", 8)
            y -= 12
            c.drawString(40, y, datos['observaciones'])

        # Pie de página
        c.setFont("Helvetica-Italic", 7)
        c.setFillColor(colors.grey)
        c.drawCentredString(width / 2, 40, "Representación impresa de la Factura Electrónica")
        c.drawCentredString(width / 2, 30, "Consulte su documento en www.sunat.gob.pe")


if __name__ == "__main__":
    from generator import FacturaGenerator

    # Test: generar una factura y crear PDF
    gen = FacturaGenerator()
    factura = gen.generar_factura(categoria_items='construccion', con_credito=True)

    pdf_gen = PDFFactura()
    archivo = pdf_gen.crear_factura(factura)

    print(f"PDF generado: {archivo}")
