"""
Ejemplo de PDFFactura Mejorado con Elementos Visuales
- Logos de empresas
- Códigos QR
- Íconos de pago
- Íconos de contacto
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from typing import Dict
import os
import requests
from io import BytesIO
import qrcode
from PIL import Image
import random


class PDFFacturaMejorado:
    """Genera PDFs de facturas con elementos visuales realistas"""

    FONT_TITLE = "Helvetica-Bold"
    FONT_NORMAL = "Helvetica"
    FONT_BOLD = "Helvetica-Bold"
    FONT_ITALIC = "Helvetica-Oblique"

    def __init__(self, output_dir: str = "facturas_generadas", use_online_resources: bool = True):
        self.output_dir = output_dir
        self.use_online_resources = use_online_resources
        os.makedirs(output_dir, exist_ok=True)

        # Cache para imágenes descargadas
        self.image_cache = {}

    def _descargar_imagen(self, url, max_retries=2):
        """Descarga imagen desde URL con caché"""
        # Verificar caché
        if url in self.image_cache:
            return self.image_cache[url]

        if not self.use_online_resources:
            return None

        for intento in range(max_retries):
            try:
                response = requests.get(url, timeout=3)
                if response.status_code == 200:
                    img_data = BytesIO(response.content)
                    self.image_cache[url] = img_data
                    return img_data
            except Exception as e:
                if intento == max_retries - 1:
                    print(f"⚠️ No se pudo descargar: {url[:50]}...")
                continue
        return None

    def _generar_logo_empresa(self, razon_social):
        """Genera logo de empresa usando UI Avatars"""
        # Limpiar nombre
        nombre = razon_social[:30].replace(" ", "+")

        # Colores según tipo de empresa
        colores = {
            'TURISMO': '1976D2',
            'HOTEL': '7B1FA2',
            'CONSTRUCCION': 'F57C00',
            'SEGURO': '388E3C',
            'INMOBILIARIA': 'E53935',
        }

        bg_color = 'random'
        for keyword, color in colores.items():
            if keyword in razon_social.upper():
                bg_color = color
                break

        url = f"https://ui-avatars.com/api/?name={nombre}&size=200&background={bg_color}&color=fff&bold=true&font-size=0.4&rounded=true"
        return url

    def _generar_qr_local(self, datos_qr):
        """Genera código QR localmente"""
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
        except Exception as e:
            print(f"⚠️ Error generando QR: {e}")
            return None

    def _dibujar_logo_empresa(self, c, datos, width, height):
        """Dibuja logo de la empresa en esquina superior izquierda"""
        razon_social = datos['emisor']['razon_social']
        logo_url = self._generar_logo_empresa(razon_social)

        logo_data = self._descargar_imagen(logo_url)

        if logo_data:
            try:
                # Posición
                logo_x = 30
                logo_y = height - 120
                logo_size = 90

                # Dibujar
                logo_data.seek(0)  # Reset buffer
                c.drawImage(
                    ImageReader(logo_data),
                    logo_x,
                    logo_y,
                    width=logo_size,
                    height=logo_size,
                    preserveAspectRatio=True,
                    mask='auto'
                )
            except Exception as e:
                print(f"⚠️ Error dibujando logo: {e}")
                # Fallback: dibujar recuadro con iniciales
                self._dibujar_logo_fallback(c, razon_social, logo_x, logo_y, logo_size)

    def _dibujar_logo_fallback(self, c, razon_social, x, y, size):
        """Logo de respaldo cuando falla la descarga"""
        # Obtener iniciales
        palabras = razon_social.split()
        iniciales = ''.join([p[0] for p in palabras[:3]]).upper()

        # Dibujar círculo
        c.setFillColor(colors.HexColor('#2C3E50'))
        c.circle(x + size/2, y + size/2, size/2, fill=True, stroke=False)

        # Dibujar iniciales
        c.setFillColor(colors.white)
        c.setFont(self.FONT_BOLD, size/3)
        c.drawCentredString(x + size/2, y + size/2 - size/8, iniciales)
        c.setFillColor(colors.black)

    def _dibujar_qr_code(self, c, datos, width, height):
        """Dibuja código QR en esquina inferior derecha"""
        # Formato SUNAT: RUC|TipoDoc|Serie|Numero|Fecha|Total
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
                # Posición
                qr_x = width - 130
                qr_y = 50
                qr_size = 80

                qr_image.seek(0)
                c.drawImage(
                    ImageReader(qr_image),
                    qr_x,
                    qr_y,
                    width=qr_size,
                    height=qr_size,
                    preserveAspectRatio=True
                )

                # Texto debajo
                c.setFont(self.FONT_ITALIC, 6)
                c.setFillColor(colors.grey)
                c.drawCentredString(qr_x + qr_size/2, qr_y - 8, "Escanea para verificar")
                c.setFillColor(colors.black)

            except Exception as e:
                print(f"⚠️ Error dibujando QR: {e}")

    def _dibujar_iconos_pago(self, c, datos, width, height):
        """Dibuja íconos de métodos de pago en el pie"""
        payment_icons = [
            ('Visa', 'https://cdn.simpleicons.org/visa/1A1F71'),
            ('MC', 'https://cdn.simpleicons.org/mastercard/EB001B'),
            ('Efectivo', 'https://api.iconify.design/mdi/cash.svg?color=%23388E3C'),
        ]

        x_start = 30
        y = 38
        icon_size = 18
        spacing = 30

        c.setFont(self.FONT_BOLD, 7)
        c.setFillColor(colors.grey)
        c.drawString(x_start, y + icon_size + 5, "Aceptamos:")

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
                except:
                    # Fallback: texto
                    c.setFont(self.FONT_NORMAL, 6)
                    c.drawString(x_start + (i * spacing), y, nombre)

        c.setFillColor(colors.black)

    def _dibujar_pie_con_iconos(self, c, datos, width, height):
        """Pie de página con íconos de contacto"""
        y = 20
        icon_size = 10

        contactos = [
            ('phone', datos['emisor']['telefono'], 'https://api.iconify.design/mdi/phone.svg?color=%23666666'),
            ('email', datos['emisor']['email'], 'https://api.iconify.design/mdi/email.svg?color=%23666666'),
        ]

        x_start = width / 2 - 150
        spacing = 150

        for i, (tipo, texto, icon_url) in enumerate(contactos):
            x = x_start + (i * spacing)

            # Ícono
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
                except:
                    pass

            # Texto
            c.setFont(self.FONT_NORMAL, 7)
            c.setFillColor(colors.grey)
            c.drawString(x + icon_size + 3, y, texto[:30])

        c.setFillColor(colors.black)

    def _dibujar_marca_agua(self, c, datos, width, height):
        """Marca de agua diagonal"""
        c.saveState()

        # Configurar
        c.setFillColor(colors.grey, alpha=0.08)
        c.setFont(self.FONT_BOLD, 55)

        # Centrar y rotar
        c.translate(width/2, height/2)
        c.rotate(45)

        # Texto
        c.drawCentredString(0, 0, "FACTURA FICTICIA")

        c.restoreState()

    def _dibujar_encabezado_simple(self, c, datos, width, height):
        """Encabezado básico para el ejemplo"""
        # Recuadro RUC
        c.setStrokeColor(colors.black)
        c.setLineWidth(2)
        c.rect(width - 180, height - 120, 150, 90)

        # RUC
        c.setFont(self.FONT_BOLD, 14)
        c.drawCentredString(width - 105, height - 45, "R.U.C.")
        c.setFont(self.FONT_BOLD, 13)
        c.drawCentredString(width - 105, height - 65, datos['emisor']['ruc'])

        # Tipo
        c.setFont(self.FONT_BOLD, 12)
        c.drawCentredString(width - 105, height - 85, "FACTURA ELECTRÓNICA")

        # Número
        c.setFont(self.FONT_BOLD, 14)
        numero_completo = f"{datos['serie']}-{datos['numero']}"
        c.drawCentredString(width - 105, height - 105, numero_completo)

        # Datos emisor (al lado del logo)
        y = height - 50
        c.setFont(self.FONT_BOLD, 11)
        c.drawString(135, y, datos['emisor']['razon_social'][:40])

        c.setFont(self.FONT_NORMAL, 8)
        y -= 13
        c.drawString(135, y, f"Dir: {datos['emisor']['direccion'][:45]}")
        y -= 11
        c.drawString(135, y, f"Tel: {datos['emisor']['telefono']}")
        y -= 11
        c.drawString(135, y, f"Email: {datos['emisor']['email'][:35]}")

    def crear_factura_ejemplo(self, datos: Dict, filename: str = "factura_ejemplo.pdf"):
        """
        Crea factura de ejemplo con elementos visuales
        """
        filepath = os.path.join(self.output_dir, filename)

        # Crear PDF
        c = canvas.Canvas(filepath, pagesize=A4)
        width, height = A4

        print("🎨 Generando factura con elementos visuales...")

        # 1. Marca de agua (fondo)
        print("   - Marca de agua")
        self._dibujar_marca_agua(c, datos, width, height)

        # 2. Logo empresa
        print("   - Logo de empresa")
        self._dibujar_logo_empresa(c, datos, width, height)

        # 3. Encabezado
        print("   - Encabezado")
        self._dibujar_encabezado_simple(c, datos, width, height)

        # 4. Código QR
        print("   - Código QR")
        self._dibujar_qr_code(c, datos, width, height)

        # 5. Íconos de pago
        print("   - Íconos de pago")
        self._dibujar_iconos_pago(c, datos, width, height)

        # 6. Pie con íconos
        print("   - Pie de página con íconos")
        self._dibujar_pie_con_iconos(c, datos, width, height)

        # 7. Texto final
        c.setFont(self.FONT_ITALIC, 7)
        c.setFillColor(colors.grey)
        c.drawCentredString(width / 2, 10, "Factura generada con elementos visuales mejorados")

        c.save()
        print(f"✅ Factura guardada: {filepath}")
        return filepath


# ====================
# EJEMPLO DE USO
# ====================

if __name__ == "__main__":
    from datetime import datetime

    # Datos de ejemplo
    datos_factura = {
        'emisor': {
            'ruc': '20438637380',
            'razon_social': 'TURISMO DIAS S.A.',
            'direccion': 'AV. NICOLAS DE PIEROLA #1079 TRUJILLO',
            'telefono': '(044) 123-4567',
            'email': 'contacto@turismodias.com',
        },
        'serie': 'F596',
        'numero': '00023196',
        'fecha_emision': datetime.now(),
        'total': 1250.50,
    }

    # Crear generador
    pdf_gen = PDFFacturaMejorado(
        output_dir="ejemplos_visuales",
        use_online_resources=True  # Cambiar a False para modo offline
    )

    # Generar factura
    archivo = pdf_gen.crear_factura_ejemplo(datos_factura)

    print(f"\n🎉 ¡Factura creada exitosamente!")
    print(f"📄 Archivo: {archivo}")
    print(f"\n💡 Elementos incluidos:")
    print(f"   ✅ Logo de empresa (UI Avatars)")
    print(f"   ✅ Código QR (generado localmente)")
    print(f"   ✅ Íconos de métodos de pago (Simple Icons)")
    print(f"   ✅ Íconos de contacto (Iconify)")
    print(f"   ✅ Marca de agua 'FACTURA FICTICIA'")
