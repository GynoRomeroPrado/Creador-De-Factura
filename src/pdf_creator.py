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

    def _normalizar_datos(self, datos: Dict) -> Dict:
        """
        Convierte formato plano (InvoiceX v5.5) a formato anidado si es necesario.
        Mantiene compatibilidad con ambos formatos.

        Args:
            datos: Diccionario en formato plano o anidado

        Returns:
            Diccionario en formato anidado (compatible con pdf_creator)
        """
        # Detectar si es formato plano (tiene campos con prefijo emisor_)
        if 'emisor_ruc' in datos or 'receptor_numero_doc' in datos:
            # Convertir formato plano a anidado
            from datetime import datetime

            # Parsear fecha_emision si es string
            fecha_emision = datos.get('fecha_emision')
            if isinstance(fecha_emision, str):
                try:
                    fecha_emision = datetime.strptime(fecha_emision, '%Y-%m-%d')
                except:
                    fecha_emision = datetime.now()

            # Parsear fecha_vencimiento si existe
            fecha_vencimiento = datos.get('fecha_vencimiento')
            if isinstance(fecha_vencimiento, str) and fecha_vencimiento:
                try:
                    fecha_vencimiento = datetime.strptime(fecha_vencimiento, '%Y-%m-%d')
                except:
                    fecha_vencimiento = None

            # Parsear cuotas si existen
            cuotas = datos.get('cuotas', [])
            if cuotas:
                for cuota in cuotas:
                    if 'fecha_vencimiento' in cuota and isinstance(cuota['fecha_vencimiento'], str):
                        try:
                            cuota['fecha_vencimiento'] = datetime.strptime(cuota['fecha_vencimiento'], '%Y-%m-%d')
                        except:
                            pass

            # Determinar descuento
            descuento = None
            if datos.get('descuento_total', 0) > 0:
                descuento = {
                    'codigo': datos.get('descuento_codigo', '00'),
                    'motivo': datos.get('descuento_motivo', 'Descuento'),
                    'factor': datos.get('descuento_factor', 0.0),
                    'monto': datos.get('descuento_total', 0.0),
                    'base': datos.get('descuento_base', 0.0)
                }

            # Mapear moneda (formato plano usa nombres completos, formato anidado usa códigos)
            moneda_dato = datos.get('moneda', 'PEN')
            if moneda_dato in ['SOLES', 'PEN', 'S/']:
                moneda_codigo = 'PEN'
                simbolo_moneda = 'S/'
                nombre_moneda = 'SOLES'
            elif moneda_dato in ['DOLARES AMERICANOS', 'DOLARES', 'DÓLARES', 'USD', '$']:
                moneda_codigo = 'USD'
                simbolo_moneda = '$'
                nombre_moneda = 'DOLARES'
            elif moneda_dato in ['EUROS', 'EUR', '€']:
                moneda_codigo = 'EUR'
                simbolo_moneda = '€'
                nombre_moneda = 'EUROS'
            else:
                # Fallback: asumir que es código y generar valores por defecto
                moneda_codigo = moneda_dato
                simbolo_moneda = datos.get('simbolo_moneda', 'S/')
                nombre_moneda = moneda_dato

            # Normalizar items (formato plano usa campos diferentes)
            items_normalizados = []
            for item_plano in datos.get('items', []):
                # Detectar si el item ya está en formato anidado
                if 'numero' in item_plano:
                    # Ya está normalizado, usar directamente
                    items_normalizados.append(item_plano)
                else:
                    # Convertir de formato plano a anidado
                    item_normalizado = {
                        'numero': item_plano.get('item', item_plano.get('numero', 0)),
                        'descripcion': item_plano.get('descripcion', ''),
                        'cantidad': item_plano.get('cantidad', 0.0),
                        'unidad': item_plano.get('unidad_medida', item_plano.get('unidad', 'NIU')),
                        'precio_unitario': item_plano.get('precio_unitario', 0.0),
                        'valor_venta': item_plano.get('valor_venta', 0.0)
                    }

                    # Campos opcionales
                    if 'codigo' in item_plano and item_plano['codigo']:
                        item_normalizado['codigo'] = item_plano['codigo']

                    if 'descuento_item' in item_plano and item_plano['descuento_item'] > 0:
                        item_normalizado['descuento'] = item_plano['descuento_item']

                    if 'cargo_item' in item_plano and item_plano['cargo_item'] > 0:
                        item_normalizado['cargo_item'] = item_plano['cargo_item']

                    if 'tipo_igv' in item_plano:
                        item_normalizado['tipo_igv'] = item_plano['tipo_igv']

                    if 'igv_item' in item_plano:
                        item_normalizado['igv'] = item_plano['igv_item']

                    if 'importe_total_item' in item_plano:
                        item_normalizado['importe_total'] = item_plano['importe_total_item']

                    items_normalizados.append(item_normalizado)

            # Convertir a formato anidado
            return {
                'emisor': {
                    'ruc': datos.get('emisor_ruc', ''),
                    'razon_social': datos.get('emisor_razon_social', ''),
                    'nombre_comercial': datos.get('emisor_nombre_comercial', ''),
                    'direccion': datos.get('emisor_direccion', ''),
                    'ubigeo': datos.get('emisor_ubigeo', ''),
                    'departamento': datos.get('emisor_departamento', ''),
                    'provincia': datos.get('emisor_provincia', ''),
                    'distrito': datos.get('emisor_distrito', ''),
                    'urbanizacion': datos.get('emisor_urbanizacion', ''),
                    'codigo_pais': datos.get('emisor_codigo_pais', 'PE'),
                    'telefono': datos.get('emisor_telefono', ''),
                    'email': datos.get('emisor_email', '')
                },
                'receptor': {
                    'tipo_documento': datos.get('receptor_tipo_documento', '6'),
                    'ruc': datos.get('receptor_numero_doc', ''),
                    'razon_social': datos.get('receptor_razon_social', ''),
                    'nombre_comercial': datos.get('receptor_nombre_comercial', ''),
                    'direccion': datos.get('receptor_direccion', ''),
                    'ubigeo': datos.get('receptor_ubigeo', ''),
                    'departamento': datos.get('receptor_departamento', ''),
                    'provincia': datos.get('receptor_provincia', ''),
                    'distrito': datos.get('receptor_distrito', ''),
                    'urbanizacion': datos.get('receptor_urbanizacion', ''),
                    'codigo_pais': datos.get('receptor_codigo_pais', 'PE'),
                    'telefono': datos.get('receptor_telefono', ''),
                    'email': datos.get('receptor_email', '')
                },
                'tipo_comprobante': datos.get('tipo_documento', 'FACTURA ELECTRONICA'),
                'serie': datos.get('serie', 'F001'),
                'numero': datos.get('numero', '000001'),
                'numero_factura': datos.get('serie_completa', f"{datos.get('serie', 'F001')}-{datos.get('numero', '000001')}"),
                'fecha_emision': fecha_emision,
                'fecha_vencimiento': fecha_vencimiento,
                'moneda': moneda_codigo,
                'simbolo_moneda': simbolo_moneda,
                'nombre_moneda': nombre_moneda,
                'items': items_normalizados,
                'op_gravada': datos.get('op_gravada', 0.0),
                'op_exonerada': datos.get('op_exonerada', 0.0),
                'op_inafecta': datos.get('op_inafecta', 0.0),
                'op_gratuitas': datos.get('op_gratuitas', 0.0),
                'igv': datos.get('igv', 0.0),
                'total': datos.get('importe_total', datos.get('total', 0.0)),
                'total_letras': datos.get('observaciones', ''),
                'descuento': descuento,
                'total_cargos': datos.get('total_cargos', 0.0),
                'otros_cargos': datos.get('otros_cargos', 0.0),
                'forma_pago': datos.get('forma_pago', 'CONTADO'),
                'con_credito': len(datos.get('cuotas', [])) > 0,
                'cuotas': cuotas,
                'observaciones': datos.get('observaciones', ''),
                'datos_hotel': self._extraer_datos_hotel(datos),
                'datos_seguro': self._extraer_datos_seguro(datos),
                'detraccion': datos.get('detraccion', 0.0),
                'detraccion_porcentaje': datos.get('detraccion_porcentaje', 0.0)
            }
        else:
            # Ya está en formato anidado, retornar sin cambios
            return datos

    def _extraer_datos_hotel(self, datos: Dict) -> Dict:
        """Extrae datos de hotel desde referencia_1 si existe"""
        referencia_1 = datos.get('referencia_1', '')
        if not referencia_1:
            return None

        # Si tiene formato de hotel (Checkin/CheckOut)
        if 'Checkin' in referencia_1 or 'CheckOut' in referencia_1:
            try:
                # Parsear la referencia_1
                # Formato esperado: "Checkin: DD-MM-YYYY, CheckOut: DD-MM-YYYY, Reserva: XXX, Habitación: YYY"
                partes = referencia_1.split(',')
                hotel_data = {}

                for parte in partes:
                    if ':' in parte:
                        clave, valor = parte.split(':', 1)
                        clave = clave.strip()
                        valor = valor.strip()

                        if clave == 'Checkin':
                            from datetime import datetime
                            try:
                                hotel_data['checkin'] = datetime.strptime(valor, '%d-%m-%Y')
                            except:
                                hotel_data['checkin'] = valor
                        elif clave == 'CheckOut':
                            from datetime import datetime
                            try:
                                hotel_data['checkout'] = datetime.strptime(valor, '%d-%m-%Y')
                            except:
                                hotel_data['checkout'] = valor
                        elif clave == 'Reserva':
                            hotel_data['codigo_reserva'] = valor
                        elif clave == 'Habitación':
                            hotel_data['numero_habitacion'] = valor
                        elif clave == 'Huésped':
                            hotel_data['nombre_huesped'] = valor

                return hotel_data if hotel_data else None
            except:
                return None

        return None

    def _extraer_datos_seguro(self, datos: Dict) -> Dict:
        """Extrae datos de seguro desde referencia_1 si existe"""
        referencia_1 = datos.get('referencia_1', '')
        if not referencia_1:
            return None

        # Si tiene formato de seguro (Póliza/Asegurado)
        if 'Póliza' in referencia_1 or 'Asegurado' in referencia_1:
            try:
                partes = referencia_1.split(',')
                seguro_data = {}

                for parte in partes:
                    if ':' in parte:
                        clave, valor = parte.split(':', 1)
                        clave = clave.strip()
                        valor = valor.strip()

                        if clave == 'Póliza':
                            seguro_data['numero_poliza'] = valor
                        elif clave == 'Asegurado':
                            seguro_data['nombre_asegurado'] = valor
                        elif clave == 'Vigencia':
                            seguro_data['vigencia_poliza'] = valor
                        elif clave == 'Tipo':
                            seguro_data['tipo_seguro'] = valor

                return seguro_data if seguro_data else None
            except:
                return None

        return None

    def crear_factura(self, datos: Dict, filename: str = None) -> str:
        """
        Crea un PDF de factura

        Args:
            datos: Diccionario con todos los datos de la factura (formato plano o anidado)
            filename: Nombre del archivo (si None, se genera automático)

        Returns:
            Ruta del archivo generado
        """
        # IMPORTANTE: Normalizar datos al formato anidado si es necesario
        datos = self._normalizar_datos(datos)

        if filename is None:
            # Generar nombre automático
            fecha_emision = datos.get('fecha_emision')
            if hasattr(fecha_emision, 'strftime'):
                fecha_str = fecha_emision.strftime('%Y%m%d')
            elif isinstance(fecha_emision, str):
                fecha_str = fecha_emision.replace('-', '')[:8]
            else:
                fecha_str = 'YYYYMMDD'

            serie = datos.get('serie', 'F001')
            numero = datos.get('numero', '000001')
            tipo = datos.get('tipo_factura', 'general')
            filename = f"Factura_{tipo}_{serie}_{numero}_{fecha_str}.pdf"

        filepath = os.path.join(self.output_dir, filename)

        # Crear PDF
        c = canvas.Canvas(filepath, pagesize=A4)
        width, height = A4

        # ========== FLUJO DE DIBUJO CON POSICIONES RELATIVAS ==========
        # Cada función retorna la posición Y donde terminó de dibujar
        # La siguiente función comienza desde esa posición Y

        # 1. Header (posición fija en top)
        self._dibujar_encabezado(c, datos, width, height)
        self._dibujar_datos_emisor(c, datos, width, height)
        self._dibujar_datos_receptor(c, datos, width, height)

        # 2. Info adicional (hotel o seguro) - posición fija pero calculada
        if datos.get('datos_hotel'):
            self._dibujar_info_hotel(c, datos, width, height)
            y_inicio_items = height - 260  # Ajustar por info hotel
        elif datos.get('datos_seguro'):
            self._dibujar_info_seguro(c, datos, width, height)
            y_inicio_items = height - 260  # Ajustar por info seguro
        else:
            y_inicio_items = height - 220  # Sin info adicional

        # 3. Tabla de items (RETORNA posición Y final)
        y_actual = self._dibujar_items(c, datos, width, height, y_inicio=y_inicio_items)

        # 4. Descuentos (solo si aplica)
        if datos.get('descuento'):
            y_actual = self._dibujar_descuentos(c, datos, width, height, y_inicio=y_actual)

        # 5. Totales (siempre)
        y_actual = self._dibujar_totales(c, datos, width, height, y_inicio=y_actual)

        # 6. Pie: forma de pago, cuotas, observaciones (TODO relativo)
        self._dibujar_pie(c, datos, width, height, y_inicial=y_actual)

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

    def _dibujar_items(self, c, datos, width, height, y_inicio=None):
        """
        Dibuja la tabla de items con soporte para múltiples páginas

        Args:
            c: Canvas de reportlab
            datos: Datos de la factura
            width: Ancho de página
            height: Alto de página
            y_inicio: Posición Y donde empezar (si None, calcula automáticamente)

        Returns:
            Posición Y final después de dibujar todos los items
        """
        # Usar posición proporcionada o calcular
        if y_inicio is not None:
            y_start = y_inicio
        else:
            # Calcular posición por defecto (para facturas sin flujo relativo)
            if datos.get('datos_hotel') or datos.get('datos_seguro'):
                y_start = height - 260
            else:
                y_start = height - 220

        # Función para dibujar encabezado de tabla
        def dibujar_encabezado_tabla(y_pos):
            c.setFillColor(colors.HexColor('#E8E8E8'))
            c.rect(30, y_pos - 18, width - 60, 18, fill=True, stroke=False)
            c.setFillColor(colors.black)
            c.setFont(self.FONT_BOLD, 8)
            c.drawString(35, y_pos - 12, "ITEM")
            c.drawString(65, y_pos - 12, "DESCRIPCIÓN")
            c.drawString(320, y_pos - 12, "UND")
            c.drawString(360, y_pos - 12, "CANT.")
            c.drawString(410, y_pos - 12, "P.UNIT")
            c.drawRightString(width - 35, y_pos - 12, "TOTAL")
            return y_pos - 35

        # Encabezado inicial
        y = dibujar_encabezado_tabla(y_start)
        c.setFont(self.FONT_NORMAL, 8)

        for i, item in enumerate(datos['items']):
            # Calcular cuántas líneas necesitará la descripción
            desc = item['descripcion']
            max_chars_por_linea = 35

            if len(desc) <= max_chars_por_linea:
                lineas_descripcion = 1
            else:
                # Calcular número de líneas
                palabras = desc.split()
                lineas_temp = []
                linea_actual = []
                longitud_actual = 0

                for palabra in palabras:
                    if longitud_actual + len(palabra) + 1 <= max_chars_por_linea:
                        linea_actual.append(palabra)
                        longitud_actual += len(palabra) + 1
                    else:
                        if linea_actual:
                            lineas_temp.append(" ".join(linea_actual))
                        linea_actual = [palabra]
                        longitud_actual = len(palabra) + 1

                if linea_actual:
                    lineas_temp.append(" ".join(linea_actual))

                lineas_descripcion = min(len(lineas_temp), 3)

            # Calcular espacio necesario según líneas de descripción
            espacio_base = 15 + ((lineas_descripcion - 1) * 9)
            espacio_necesario = espacio_base if 'cargo_item' not in item else espacio_base + 10

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

            # Descripción (dividir en líneas si es muy larga)
            desc = item['descripcion']
            max_chars_por_linea = 35

            if len(desc) <= max_chars_por_linea:
                # Descripción corta, una sola línea
                c.drawString(65, y, desc)
                lineas_desc = 1
            else:
                # Descripción larga, dividir en palabras y crear líneas
                palabras = desc.split()
                lineas = []
                linea_actual = []
                longitud_actual = 0

                for palabra in palabras:
                    if longitud_actual + len(palabra) + 1 <= max_chars_por_linea:
                        linea_actual.append(palabra)
                        longitud_actual += len(palabra) + 1
                    else:
                        if linea_actual:
                            lineas.append(" ".join(linea_actual))
                        linea_actual = [palabra]
                        longitud_actual = len(palabra) + 1

                if linea_actual:
                    lineas.append(" ".join(linea_actual))

                # Dibujar cada línea
                for i, linea in enumerate(lineas[:3]):  # Máximo 3 líneas
                    c.drawString(65, y - (i * 9), linea)

                lineas_desc = min(len(lineas), 3)

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

            # Ajustar Y según líneas de descripción
            y -= 15 + ((lineas_desc - 1) * 9)

        # Línea final de tabla
        c.setStrokeColor(colors.grey)
        c.setLineWidth(0.5)
        c.line(30, y + 5, width - 30, y + 5)

        return y

    def _dibujar_descuentos(self, c, datos, width, height, y_inicio=None):
        """
        Dibuja la tabla de descuentos si existe

        Args:
            c: Canvas de reportlab
            datos: Datos de la factura
            width: Ancho de página
            height: Alto de página
            y_inicio: Posición Y donde empezar (si None, usa posición fija)

        Returns:
            Posición Y final después de dibujar descuentos
        """
        # Usar posición relativa si se proporciona, sino usar fija
        if y_inicio is not None:
            y = y_inicio - 30  # 30px de separación después de items
        else:
            y = 195  # Posición fija para facturas simples (retrocompatibilidad)

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

        # Retornar posición Y final (con margen de 20px)
        return y - 20

    def _dibujar_totales(self, c, datos, width, height, y_inicio=None):
        """
        Dibuja los totales

        Args:
            c: Canvas de reportlab
            datos: Datos de la factura
            width: Ancho de página
            height: Alto de página
            y_inicio: Posición Y donde empezar (si None, usa posición fija para facturas simples)
        """
        # Si se proporciona y_inicio (facturas multipágina), usar esa posición
        # Si no, usar posición fija (facturas de 1 página)
        if y_inicio is not None:
            # Dejar espacio después de los items
            y = y_inicio - 25  # 25px de separación después de la tabla de items
        else:
            # Posición fija para facturas simples (1 página)
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
        # Calcular espacio necesario para el pie
        espacio_necesario = 100  # Mínimo para forma de pago
        if datos['con_credito'] and datos['cuotas']:
            espacio_necesario += 60 + (len(datos['cuotas']) * 12)  # Cuotas
        if datos.get('observaciones'):
            espacio_necesario += 40  # Observaciones

        # Determinar posición inicial
        if y_inicial is not None:
            y = y_inicial - 5

            # Si no hay espacio suficiente, crear NUEVA PÁGINA
            if y < espacio_necesario:
                c.showPage()

                # Encabezado simple en nueva página
                c.setFont(self.FONT_BOLD, 12)
                c.drawString(30, height - 40, f"{datos['emisor']['razon_social'][:50]}")
                c.setFont(self.FONT_NORMAL, 9)
                c.drawString(30, height - 55, f"Factura: {datos['numero_factura']}")

                # Línea separadora
                c.setStrokeColor(colors.grey)
                c.line(30, height - 65, width - 30, height - 65)

                # Empezar desde arriba en nueva página
                y = height - 90
        else:
            y = 200

        # Forma de pago
        c.setFont(self.FONT_BOLD, 9)
        c.drawString(30, y, "FORMA DE PAGO:")
        c.setFont(self.FONT_NORMAL, 9)
        c.drawString(130, y, datos['forma_pago'])

        # Cuotas si es a crédito
        if datos['con_credito'] and datos['cuotas']:
            y -= 22
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
            y -= 20
            c.setFont(self.FONT_BOLD, 8)
            c.drawString(30, y, "OBSERVACIONES:")
            c.setFont(self.FONT_NORMAL, 7)
            y -= 12
            obs = datos['observaciones']
            if len(obs) > 80:
                # Partir en dos líneas
                c.drawString(35, y, obs[:80])
                y -= 10
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
