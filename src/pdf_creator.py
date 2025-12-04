"""
Creador de PDFs de facturas - Versión mejorada con soporte de estilos y ajuste de texto
"""
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib import colors
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
from typing import Dict, Union
import os
import random
import copy
from .styles import InvoiceStyle, STYLES, ESTILO_CLASICO
from .logo_drawer import LogoDrawer
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

class PDFFactura:
    """Genera PDFs de facturas con diseño profesional, tipografía uniforme y estilos configurables"""

    def __init__(self, output_dir: str = "facturas_generadas", estilo: Union[str, InvoiceStyle] = "clasico"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        
        if isinstance(estilo, str):
            self.style = STYLES.get(estilo, ESTILO_CLASICO)
        else:
            self.style = estilo

    def crear_factura(self, datos: Dict, filename: str = None) -> str:
        """
        Crea un PDF de factura
        """
        if filename is None:
            fecha_str = datos['fecha_emision'].strftime('%Y%m%d')
            tipo = datos.get('tipo_factura', 'general')
            filename = f"Factura_{tipo}_{datos['serie']}_{datos['numero']}_{fecha_str}.pdf"

        filepath = os.path.join(self.output_dir, filename)

        # Guardar estilo original para restaurarlo al final
        original_style = self.style
        
        try:
            # --- LÓGICA DE RANDOMIZACIÓN (AUMENTO DE DATOS) ---
            # 1. Moneda al aire para layout invertido (50% probabilidad)
            layout_variant = random.choice(['standard', 'inverted'])
            
            # Crear una copia superficial del estilo para modificarlo temporalmente
            # Usamos copy.copy() porque InvoiceStyle es un dataclass (mutable)
            temp_style = copy.copy(self.style)
            
            if layout_variant == 'inverted':
                # Invertir alineaciones: Emisor a la derecha, Receptor a la izquierda
                temp_style.align_header = 'right'
                temp_style.align_title = 'right'
            
            # 2. Variación de tamaño de fuente del Emisor (10pt - 14pt)
            # Esto ayuda a que el modelo no dependa del tamaño para identificar al emisor
            temp_style.size_title = random.randint(10, 14)
            
            # Aplicar estilo temporal
            self.style = temp_style
            # --------------------------------------------------

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

            # Datos específicos de restaurante
            if datos.get('datos_restaurante'):
                self._dibujar_info_restaurante(c, datos, width, height)

            # Datos específicos de transporte
            if datos.get('datos_transporte'):
                self._dibujar_info_transporte(c, datos, width, height)

            # Datos específicos de servicios
            if datos.get('datos_servicios'):
                self._dibujar_info_servicios(c, datos, width, height)

            # Dibujar items y obtener posición final Y
            y_final_items = self._dibujar_items(c, datos, width, height)

            # Descuentos si aplica, usando la posición Y de items
            if datos.get('descuento'):
                y_final_items = self._dibujar_descuentos(c, datos, width, height, y_inicial=y_final_items)

            # Dibujar totales y obtener posición final Y
            # Pasamos y_final_items como punto de partida
            y_final_totales = self._dibujar_totales(c, datos, width, height, y_inicial=y_final_items)

            # Dibujar pie usando la posición Y del bloque anterior
            self._dibujar_pie(c, datos, width, height, y_inicial=y_final_totales)

            c.save()
            return filepath
            
        finally:
            # Restaurar estilo original para no afectar siguientes facturas
            self.style = original_style

    def _get_string_width(self, c, text, font, size):
        return c.stringWidth(text, font, size)

    def _draw_wrapped_text(self, c, text, x, y, max_width, font, size, align='left'):
        """Dibuja texto que se ajusta al ancho, saltando de línea si es necesario"""
        c.setFont(font, size)
        lines = simpleSplit(text, font, size, max_width)
        
        height_consumed = 0
        for line in lines:
            if align == 'right':
                c.drawRightString(x, y - height_consumed, line)
            elif align == 'center':
                c.drawCentredString(x, y - height_consumed, line)
            else:
                c.drawString(x, y - height_consumed, line)
            height_consumed += self.style.line_height
            
        return y - height_consumed + (self.style.line_height - size) # Retorna la nueva posición Y

    def _dibujar_encabezado_pagina_nueva(self, c, datos, width, height):
        """Dibuja un encabezado simplificado para páginas adicionales"""
        x = self.style.margin_x
        c.setFont(self.style.font_bold, 12)
        c.setFillColor(colors.black)
        c.drawString(x, height - 50, f"{datos['emisor']['razon_social'][:50]}")
        c.setFont(self.style.font_normal, 9)
        c.drawString(x, height - 65, f"Factura: {datos['numero_factura']}")

        # Línea separadora
        c.setStrokeColor(colors.grey)
        c.line(x, height - 75, width - x, height - 75)

    def _dibujar_encabezado(self, c, datos, width, height):
        """Dibuja el encabezado de la factura con soporte para alineación y estilos"""
        # Configurar colores y fuentes según estilo
        c.setStrokeColor(self.style.border_color)
        c.setLineWidth(2)
        
        # Determinar posición del recuadro RUC según alineación
        if self.style.align_header == "left":
            x_ruc = width - 180
            # Logo o nombre de empresa a la izquierda
            x_empresa = self.style.margin_x
            align_empresa = "left"
        elif self.style.align_header == "right":
            x_ruc = self.style.margin_x
            # Logo o nombre de empresa a la derecha
            x_empresa = width - self.style.margin_x
            align_empresa = "right"
        else: # center
            x_ruc = width - 180 # RUC siempre a la derecha en estilo clásico/centrado por convención, o podría ir abajo
            x_empresa = self.style.margin_x # Empresa ocupa el resto
            align_empresa = "left" # Por defecto

        # Dibujar recuadro RUC
        # Si es estilo minimalista o industrial, el borde puede ser diferente
        if self.style.name != "Minimalista":
            c.rect(x_ruc, height - 120, 150, 90)
        
        # Contenido del RUC
        c.setFillColor(self.style.color_primary)
        c.setFont(self.style.font_bold, 14)
        # Ajustar posición Y para dar más margen superior dentro del cuadro
        c.drawCentredString(x_ruc + 75, height - 50, "R.U.C.")

        c.setFont(self.style.font_bold, 13)
        c.drawCentredString(x_ruc + 75, height - 70, datos['emisor']['ruc'])

        # Tipo de comprobante
        c.setFillColor(self.style.color_secondary)
        c.setFont(self.style.font_bold, 10) # Reducir un poco fuente para evitar desborde
        # Wrapping para tipo de comprobante si es muy largo
        tipo_comp = datos['tipo_comprobante']
        if len(tipo_comp) > 20:
             c.setFont(self.style.font_bold, 9)
        
        c.drawCentredString(x_ruc + 75, height - 90, tipo_comp)
        c.setFillColor(colors.black)

        # Número
        c.setFont(self.style.font_bold, 14)
        c.drawCentredString(x_ruc + 75, height - 110, datos['numero_factura'])

    def _dibujar_info_restaurante(self, c, datos, width, height):
        """Dibuja información específica de restaurante"""
        y = height - 205
        rest = datos['datos_restaurante']
        x = self.style.margin_x

        # Título de sección
        c.setFillColor(self.style.color_secondary)
        c.setFont(self.style.font_bold, self.style.size_normal)
        c.drawString(x, y, "DETALLE DE CONSUMO")
        
        y -= 15
        c.setFillColor(colors.black)
        c.setFont(self.style.font_normal, self.style.size_small)
        
        # Dibujar datos en dos columnas
        c.drawString(x, y, f"Mesa: {rest['mesa']}")
        c.drawString(x + 100, y, f"Personas: {rest['personas']}")
        c.drawString(x + 200, y, f"Mesero: {rest['mesero']}")
        
        y -= 12
        c.drawString(x, y, f"Hora Ingreso: {rest['hora_ingreso']}")
        c.drawString(x + 100, y, f"Propina Sugerida: {datos['simbolo_moneda']} {rest['propinas']:.2f}")

    def _dibujar_info_transporte(self, c, datos, width, height):
        """Dibuja información específica de transporte"""
        y = height - 205
        trans = datos['datos_transporte']
        x = self.style.margin_x

        c.setFillColor(self.style.color_secondary)
        c.setFont(self.style.font_bold, self.style.size_normal)
        c.drawString(x, y, "INFORMACIÓN DE TRASLADO")
        
        y -= 15
        c.setFillColor(colors.black)
        c.setFont(self.style.font_normal, self.style.size_small)
        
        c.drawString(x, y, f"Guía Remisión: {trans['guia_remision']}")
        c.drawString(x + 200, y, f"Licencia: {trans['licencia']}")
        
        y -= 12
        c.drawString(x, y, f"Vehículo: {trans['placa_vehiculo']}")
        c.drawString(x + 200, y, f"Conductor: {trans['conductor']}")
        
        y -= 12
        c.setFont(self.style.font_bold, self.style.size_small)
        c.drawString(x, y, f"Origen: {trans['origen']}")
        c.drawString(x + 200, y, f"Destino: {trans['destino']}")

    def _dibujar_info_servicios(self, c, datos, width, height):
        """Dibuja información específica de servicios profesionales"""
        y = height - 205
        serv = datos['datos_servicios']
        x = self.style.margin_x

        c.setFillColor(self.style.color_secondary)
        c.setFont(self.style.font_bold, self.style.size_normal)
        c.drawString(x, y, "DATOS DEL SERVICIO")
        
        y -= 15
        c.setFillColor(colors.black)
        c.setFont(self.style.font_normal, self.style.size_small)
        
        c.drawString(x, y, f"Orden Servicio: {serv['orden_servicio']}")
        c.drawString(x + 200, y, f"Conformidad: {serv['conformidad_servicio']}")
        
        y -= 12
        c.drawString(x, y, f"Área: {serv['area_solicitante']}")
        
        y -= 12
        c.setFont(self.style.font_bold, self.style.size_small)
        c.drawString(x, y, f"Proyecto: {serv['proyecto']}")

    def _dibujar_datos_emisor(self, c, datos, width, height):
        """Dibuja los datos del emisor con logo y lógica robusta de alineación"""
        y = height - 50
        
        # Configuración del Logo
        logo_size = 60
        logo_padding = 15
        industria = datos.get('industria', 'general')
        
        c.setFont(self.style.font_title, self.style.size_title)
        c.setFillColor(self.style.color_primary)
        
        razon_social = datos['emisor']['razon_social']
        
        # 1. Definir el área disponible y posición del logo
        if self.style.align_header == "right":
            # Bloque a la derecha, RUC a la izquierda
            x_start = 200 
            x_end = width - self.style.margin_x
            
            # Logo a la derecha del todo
            logo_x = x_end - logo_size
            logo_y = y - logo_size + 15
            
            # El texto termina antes del logo
            x_end_text = x_end - logo_size - logo_padding
            x_start_text = x_start
            
            # Dibujar Logo
            LogoDrawer.draw_logo(c, logo_x, logo_y, logo_size, razon_social, industria)
            
        else:
            # Bloque a la izquierda (Default), RUC a la derecha
            x_start = self.style.margin_x
            x_end = width - 250
            
            # Logo a la izquierda del todo
            logo_x = x_start
            logo_y = y - logo_size + 15
            
            # El texto empieza después del logo
            x_start_text = x_start + logo_size + logo_padding
            x_end_text = x_end
            
            # Dibujar Logo
            LogoDrawer.draw_logo(c, logo_x, logo_y, logo_size, razon_social, industria)

        ancho_disponible = x_end_text - x_start_text

        # 2. Calcular punto de anclaje (x_anchor)
        if self.style.align_title == 'right':
            x_anchor = x_end_text
        elif self.style.align_title == 'center':
            x_anchor = x_start_text + (ancho_disponible / 2)
        else: # left
            x_anchor = x_start_text

        # 3. Dibujar Razón Social
        y = self._draw_wrapped_text(c, razon_social, x_anchor, y, ancho_disponible, self.style.font_title, self.style.size_title, align=self.style.align_title)

        c.setFillColor(colors.black)
        c.setFont(self.style.font_normal, self.style.size_normal)
        y -= 5
        
        # 4. Dibujar detalles
        align_text = self.style.align_title
        
        y = self._draw_wrapped_text(c, f"Dirección: {datos['emisor']['direccion']}", x_anchor, y, ancho_disponible, self.style.font_normal, self.style.size_normal, align=align_text)
        
        if align_text == 'right':
            c.drawRightString(x_anchor, y, f"Teléfono: {datos['emisor']['telefono']}")
        elif align_text == 'center':
            c.drawCentredString(x_anchor, y, f"Teléfono: {datos['emisor']['telefono']}")
        else:
            c.drawString(x_anchor, y, f"Teléfono: {datos['emisor']['telefono']}")
        y -= self.style.line_height
        
        if align_text == 'right':
            c.drawRightString(x_anchor, y, f"Email: {datos['emisor']['email']}")
        elif align_text == 'center':
            c.drawCentredString(x_anchor, y, f"Email: {datos['emisor']['email']}")
        else:
            c.drawString(x_anchor, y, f"Email: {datos['emisor']['email']}")

    def _dibujar_datos_receptor(self, c, datos, width, height):
        """Dibuja los datos del receptor y fecha"""
        y = height - 135
        x = self.style.margin_x

        # Línea separadora
        c.setStrokeColor(colors.grey)
        c.setLineWidth(0.5)
        c.line(x, y + 5, width - x, y + 5)

        y -= 10

        c.setFont(self.style.font_bold, self.style.size_normal)
        c.drawString(x, y, "SEÑOR(ES):")
        c.setFont(self.style.font_normal, self.style.size_normal)
        
        razon_cliente = datos['receptor']['razon_social']
        # Wrapping para cliente
        self._draw_wrapped_text(c, razon_cliente, x + 70, y, 300, self.style.font_normal, self.style.size_normal)

        y -= 14
        c.setFont(self.style.font_bold, self.style.size_normal)
        c.drawString(x, y, "RUC:")
        c.setFont(self.style.font_normal, self.style.size_normal)
        c.drawString(x + 70, y, datos['receptor']['ruc'])

        y -= 14
        c.setFont(self.style.font_bold, self.style.size_normal)
        c.drawString(x, y, "DIRECCIÓN:")
        c.setFont(self.style.font_normal, self.style.size_normal)
        
        direccion = datos['receptor']['direccion']
        self._draw_wrapped_text(c, direccion, x + 70, y, 300, self.style.font_normal, self.style.size_normal)

        # Fecha en el lado derecho
        y_fecha = height - 145
        x_fecha_label = width - 100
        x_fecha_val = width - 30
        
        c.setFont(self.style.font_bold, self.style.size_normal)
        c.drawRightString(x_fecha_label, y_fecha, "FECHA EMISIÓN:")
        c.setFont(self.style.font_normal, self.style.size_normal)
        c.drawRightString(x_fecha_val, y_fecha, datos['fecha_emision'].strftime('%d/%m/%Y'))

        y_fecha -= 14
        c.setFont(self.style.font_bold, self.style.size_normal)
        c.drawRightString(x_fecha_label, y_fecha, "MONEDA:")
        c.setFont(self.style.font_normal, self.style.size_normal)
        c.drawRightString(x_fecha_val, y_fecha, datos['nombre_moneda'])

        if datos.get('numero_contrato'):
            y_fecha -= 14
            c.setFont(self.style.font_bold, self.style.size_normal)
            c.drawRightString(x_fecha_label, y_fecha, "CONTRATO:")
            c.setFont(self.style.font_normal, self.style.size_normal)
            c.drawRightString(x_fecha_val, y_fecha, datos['numero_contrato'])

        if datos.get('periodo_facturado'):
            y_fecha -= 14
            c.setFont(self.style.font_bold, self.style.size_normal)
            c.drawRightString(x_fecha_label, y_fecha, "PERIODO:")
            c.setFont(self.style.font_normal, self.style.size_normal)
            c.drawRightString(x_fecha_val, y_fecha, datos['periodo_facturado'])

    def _dibujar_info_hotel(self, c, datos, width, height):
        """Dibuja información adicional de hotel con formato mejorado"""
        y = height - 205
        hotel = datos['datos_hotel']
        x = self.style.margin_x

        # Encabezado de sección con fondo
        c.setFillColor(self.style.color_secondary)
        c.rect(x, y - 2, width - (x*2), 16, fill=True, stroke=False)

        c.setFillColor(colors.white)
        c.setFont(self.style.font_bold, self.style.size_normal)
        c.drawString(x + 5, y + 3, "Información adicional")

        c.setFillColor(colors.black)
        y -= 18

        # Datos de estadía
        c.setFont(self.style.font_bold, self.style.size_small)
        c.drawString(x, y, "CheckIn:")
        c.setFont(self.style.font_normal, self.style.size_small)
        c.drawString(x + 50, y, hotel['checkin'].strftime('%d-%m-%Y'))

        c.setFont(self.style.font_bold, self.style.size_small)
        c.drawString(x + 130, y, "CheckOut:")
        c.setFont(self.style.font_normal, self.style.size_small)
        c.drawString(x + 185, y, hotel['checkout'].strftime('%d-%m-%Y'))

        y -= 12
        c.setFont(self.style.font_bold, self.style.size_small)
        c.drawString(x, y, "Reserva:")
        c.setFont(self.style.font_normal, self.style.size_small)
        c.drawString(x + 50, y, str(hotel['reserva']))

        y -= 12
        c.setFont(self.style.font_bold, self.style.size_small)
        c.drawString(x, y, "Huésped:")
        c.setFont(self.style.font_normal, self.style.size_small)
        c.drawString(x + 50, y, hotel['huesped'][:50])

        y -= 12
        c.setFont(self.style.font_bold, self.style.size_small)
        c.drawString(x, y, "Noches:")
        c.setFont(self.style.font_normal, self.style.size_small)
        c.drawString(x + 50, y, str(hotel['noches']))

        # Habitación
        if hotel.get('habitacion'):
            c.setFont(self.style.font_bold, self.style.size_small)
            c.drawString(x + 130, y, "Habitación:")
            c.setFont(self.style.font_normal, self.style.size_small)
            c.drawString(x + 190, y, hotel['habitacion'])

        # Grupo (si existe)
        if hotel.get('codigo_grupo'):
            y -= 12
            c.setFont(self.style.font_bold, self.style.size_small)
            c.drawString(x, y, "Código de Grupo:")
            c.setFont(self.style.font_normal, self.style.size_small)
            c.drawString(x + 80, y, str(hotel['codigo_grupo']))

            c.setFont(self.style.font_bold, self.style.size_small)
            c.drawString(x + 170, y, "Nombre de Grupo:")
            c.setFont(self.style.font_normal, self.style.size_small)
            c.drawString(x + 255, y, str(hotel['nombre_grupo']))

    def _dibujar_info_seguro(self, c, datos, width, height):
        """Dibuja información adicional de seguro"""
        y = height - 205
        seguro = datos['datos_seguro']
        x = self.style.margin_x

        c.setFont(self.style.font_bold, self.style.size_normal)
        c.drawString(x, y, "INFORMACIÓN DE PÓLIZA")

        y -= 15
        c.setFont(self.style.font_normal, self.style.size_small)
        c.drawString(x, y, f"Póliza: {seguro['numero_poliza']}")
        c.drawString(x + 150, y, f"Documento: {seguro['numero_documento'][:25]}")

        y -= 12
        c.drawString(x, y, f"Giro: {seguro['giro']}")
        c.drawString(x + 150, y, f"Vehículo: {seguro['vehiculo']}")

        y -= 12
        vig_inicio = seguro['vigencia_inicio'].strftime('%d/%m/%Y')
        vig_fin = seguro['vigencia_fin'].strftime('%d/%m/%Y')
        c.drawString(x, y, f"Vigencia: {vig_inicio} - {vig_fin}")

    def _dibujar_items(self, c, datos, width, height):
        """Dibuja la tabla de items con soporte para múltiples páginas y división de items largos"""
        # Ajustar posición inicial según si hay datos adicionales
        espacio_extra = 0
        if datos.get('datos_hotel') or datos.get('datos_seguro') or datos.get('datos_restaurante') or datos.get('datos_transporte') or datos.get('datos_servicios'):
            espacio_extra = 60 # Más espacio para los bloques de datos
            
        y_start = height - 220 - espacio_extra

        x = self.style.margin_x
        
        # Función para dibujar encabezado de tabla
        def dibujar_encabezado_tabla(y_pos):
            c.setFillColor(self.style.table_header_bg)
            c.rect(x, y_pos - 18, width - (x*2), 18, fill=True, stroke=False)
            c.setFillColor(self.style.table_header_text)
            c.setFont(self.style.font_bold, self.style.size_small)
            
            c.drawString(x + 5, y_pos - 12, "ITEM")
            c.drawString(x + 35, y_pos - 12, "DESCRIPCIÓN")
            c.drawString(x + 290, y_pos - 12, "UND")
            c.drawString(x + 330, y_pos - 12, "CANT.")
            c.drawString(x + 380, y_pos - 12, "P.UNIT")
            c.drawRightString(width - x - 5, y_pos - 12, "TOTAL")
            return y_pos - 35

        # Encabezado inicial
        y = dibujar_encabezado_tabla(y_start)
        c.setFont(self.style.font_normal, self.style.size_small)

        for i, item in enumerate(datos['items']):
            # Calcular líneas de descripción
            desc_lines = simpleSplit(item['descripcion'], self.style.font_normal, self.style.size_small, 250)
            total_lines = len(desc_lines)
            
            # Altura base por línea
            line_height = self.style.line_height
            
            # Altura extra si hay cargo
            cargo_height = 10 if 'cargo_item' in item and item['cargo_item'] > 0 else 0
            
            # Altura total requerida para el item completo
            total_item_height = (total_lines * line_height) + 5 + cargo_height
            
            # Espacio disponible en la página actual (dejando margen inferior de 100)
            espacio_disponible = y - 100
            
            # Si el item cabe completo, dibujarlo normal
            if total_item_height <= espacio_disponible:
                lines_to_draw = desc_lines
                item_height = total_item_height
                draw_values = True
                draw_cargo = True
                remaining_lines = []
            else:
                # El item NO cabe completo. Calcular cuántas líneas caben.
                # Necesitamos al menos espacio para 2 líneas para que valga la pena dividir
                lines_capacity = int((espacio_disponible - 5) / line_height)
                
                if lines_capacity < 2:
                    # Si caben menos de 2 líneas, mejor saltar de página directamente
                    c.showPage()
                    self._dibujar_encabezado_pagina_nueva(c, datos, width, height)
                    y = dibujar_encabezado_tabla(height - 90)
                    c.setFont(self.style.font_normal, self.style.size_small)
                    
                    # Ahora estamos en nueva página, evaluamos de nuevo si cabe completo
                    espacio_disponible = y - 100
                    if total_item_height <= espacio_disponible:
                        lines_to_draw = desc_lines
                        item_height = total_item_height
                        draw_values = True
                        draw_cargo = True
                        remaining_lines = []
                    else:
                        # Aún no cabe (item gigante), dividir
                        lines_capacity = int((espacio_disponible - 5) / line_height)
                        lines_to_draw = desc_lines[:lines_capacity]
                        remaining_lines = desc_lines[lines_capacity:]
                        item_height = (len(lines_to_draw) * line_height) + 5
                        draw_values = True # Dibujamos valores en la primera parte
                        draw_cargo = False # Cargo va al final
                else:
                    # Dividir en la página actual
                    lines_to_draw = desc_lines[:lines_capacity]
                    remaining_lines = desc_lines[lines_capacity:]
                    item_height = (len(lines_to_draw) * line_height) + 5
                    draw_values = True
                    draw_cargo = False

            # Bucle para dibujar partes del item (puede ser 1 parte o más si se divide)
            while True:
                # Dibujar fondo de fila alterna si corresponde
                if self.style.alternating_row_colors and i % 2 == 1:
                    c.setFillColor(self.style.row_bg_color)
                    c.rect(x, y - 5, width - (x*2), item_height, fill=True, stroke=False)
                    c.setFillColor(colors.black)

                # Dibujar número de item solo en la primera parte
                if draw_values:
                    c.setFillColor(colors.black)
                    c.drawString(x + 5, y, str(item['numero']))

                # Dibujar líneas de descripción
                y_desc = y
                for line in lines_to_draw:
                    c.drawString(x + 35, y_desc, line)
                    y_desc -= line_height

                # Dibujar valores numéricos solo en la primera parte
                if draw_values:
                    c.drawString(x + 290, y, item['unidad'])
                    if isinstance(item['cantidad'], float):
                        c.drawRightString(x + 365, y, f"{item['cantidad']:.3f}")
                    else:
                        c.drawRightString(x + 365, y, str(item['cantidad']))
                    c.drawRightString(x + 425, y, f"{datos['simbolo_moneda']} {item['precio_unitario']:.2f}")
                    c.drawRightString(width - x - 5, y, f"{datos['simbolo_moneda']} {item['valor_venta']:.2f}")

                # Dibujar cargo si corresponde y es la última parte
                if draw_cargo and 'cargo_item' in item and item['cargo_item'] > 0:
                    c.setFont(self.style.font_italic, 7)
                    c.drawString(x + 35, y_desc, f"Cargo al ítem")
                    c.drawRightString(width - x - 5, y_desc, f"+ {datos['simbolo_moneda']} {item['cargo_item']:.2f}")
                    c.setFont(self.style.font_normal, self.style.size_small)
                    y_desc -= 10

                # Actualizar Y
                y = y_desc - 5

                # Si quedan líneas pendientes, preparar siguiente página
                if remaining_lines:
                    # Pie de página de continuación
                    c.setFont(self.style.font_italic, 7)
                    c.setFillColor(colors.grey)
                    c.drawCentredString(width / 2, 50, f"Continúa en página siguiente... (Item {i+1})")
                    
                    c.showPage()
                    self._dibujar_encabezado_pagina_nueva(c, datos, width, height)
                    y = dibujar_encabezado_tabla(height - 90)
                    c.setFont(self.style.font_normal, self.style.size_small)
                    c.setFillColor(colors.black)
                    
                    # Calcular qué cabe en la nueva página
                    espacio_disponible = y - 100
                    total_remaining_height = (len(remaining_lines) * line_height) + 5 + cargo_height
                    
                    if total_remaining_height <= espacio_disponible:
                        lines_to_draw = remaining_lines
                        item_height = total_remaining_height
                        remaining_lines = []
                        draw_values = False # Ya se dibujaron
                        draw_cargo = True # Cargo va al final
                    else:
                        # Aún no cabe todo, seguir dividiendo
                        lines_capacity = int((espacio_disponible - 5) / line_height)
                        lines_to_draw = remaining_lines[:lines_capacity]
                        remaining_lines = remaining_lines[lines_capacity:]
                        item_height = (len(lines_to_draw) * line_height) + 5
                        draw_values = False
                        draw_cargo = False
                else:
                    break # Terminamos con este item

        # Línea final de tabla
        c.setStrokeColor(colors.grey)
        c.setLineWidth(0.5)
        c.line(x, y + 5, width - x, y + 5)

        return y

    def _dibujar_descuentos(self, c, datos, width, height, y_inicial=None):
        """Dibuja la tabla de descuentos si existe"""
        # Calcular posición inicial
        if y_inicial is not None:
            y = y_inicial - 20
        else:
            y = 195 # Fallback (no debería usarse con layout dinámico)

        # Verificar espacio suficiente (aprox 60 unidades)
        if y < 60:
            c.showPage()
            # Redibujar encabezado básico si es necesario
            self._dibujar_encabezado_pagina_nueva(c, datos, width, height)
            y = height - 100

        descuento = datos['descuento']
        x = self.style.margin_x

        c.setFont(self.style.font_bold, self.style.size_normal)
        c.drawString(x, y, "DESCUENTOS")

        y -= 15
        c.setFont(self.style.font_normal, self.style.size_small)

        # Encabezado de tabla de descuentos
        c.setFillColor(self.style.color_background_header)
        c.rect(x, y - 12, width - (x*2), 12, fill=True, stroke=False)

        c.setFillColor(self.style.color_text_header)
        c.setFont(self.style.font_bold, 7)
        c.drawString(x + 5, y - 8, "DESCRIPCIÓN")
        c.drawString(x + 170, y - 8, "GRAVADO")
        c.drawString(x + 230, y - 8, "EXONER.")
        c.drawString(x + 290, y - 8, "IGV")
        c.drawString(x + 340, y - 8, "ICBPER")
        c.drawString(x + 390, y - 8, "TOTAL")
        c.drawString(x + 450, y - 8, "DETRAC.")

        y -= 20
        c.setFillColor(colors.black)
        c.setFont(self.style.font_normal, 7)
        c.drawString(x + 5, y, descuento['descripcion'])
        c.drawString(x + 170, y, f"{datos['simbolo_moneda']} {descuento['gravado']:.2f}")
        c.drawString(x + 230, y, f"{datos['simbolo_moneda']} {descuento['exonerado']:.2f}")
        c.drawString(x + 290, y, f"{datos['simbolo_moneda']} {descuento['igv']:.2f}")
        c.drawString(x + 340, y, f"{datos['simbolo_moneda']} {descuento['icbper']:.2f}")
        c.drawString(x + 390, y, f"{datos['simbolo_moneda']} {descuento['total']:.2f}")
        c.drawString(x + 450, y, f"{datos['simbolo_moneda']} {descuento['detraccion']:.2f}")
        
        return y - 10 # Retornar nueva posición Y

    def _dibujar_totales(self, c, datos, width, height, y_inicial=None):
        """Dibuja los totales con posicionamiento dinámico"""
        # Calcular altura estimada del bloque de totales
        # Base: ~100 (Total box + letras) + ~20 por cada línea opcional
        altura_estimada = 120
        if datos.get('op_gratuitas', 0) > 0: altura_estimada += 18
        if datos['op_exonerada'] > 0: altura_estimada += 18
        if datos['op_inafecta'] > 0: altura_estimada += 18
        if datos.get('descuento'): altura_estimada += 18
        if datos.get('total_cargos', 0) > 0: altura_estimada += 18
        if datos.get('otros_cargos', 0) > 0: altura_estimada += 18
        
        # Determinar Y inicial
        if y_inicial is not None:
            y = y_inicial - 20 # Margen desde el elemento anterior
        else:
            y = 340 # Fallback

        # Verificar si cabe en la página actual
        # Dejamos un margen inferior de 50 para el pie de página
        if y - altura_estimada < 50:
            c.showPage()
            self._dibujar_encabezado_pagina_nueva(c, datos, width, height)
            y = height - 100 # Reiniciar Y en nueva página

        x_inicio = width - 220
        x_val = width - 30

        # Op. Gravada
        c.setFont(self.style.font_bold, self.style.size_normal)
        c.drawString(x_inicio, y, "OP. GRAVADAS:")
        c.setFont(self.style.font_normal, self.style.size_normal)
        c.drawRightString(x_val, y, f"{datos['simbolo_moneda']} {datos['op_gravada']:.2f}")

        if datos.get('op_gratuitas', 0) > 0:
            y -= 18
            c.setFont(self.style.font_bold, self.style.size_normal)
            c.drawString(x_inicio, y, "OP. GRATUITAS:")
            c.setFont(self.style.font_normal, self.style.size_normal)
            c.drawRightString(x_val, y, f"{datos['simbolo_moneda']} {datos['op_gratuitas']:.2f}")

        if datos['op_exonerada'] > 0:
            y -= 18
            c.setFont(self.style.font_bold, self.style.size_normal)
            c.drawString(x_inicio, y, "OP. EXONERADAS:")
            c.setFont(self.style.font_normal, self.style.size_normal)
            c.drawRightString(x_val, y, f"{datos['simbolo_moneda']} {datos['op_exonerada']:.2f}")

        if datos['op_inafecta'] > 0:
            y -= 18
            c.setFont(self.style.font_bold, self.style.size_normal)
            c.drawString(x_inicio, y, "OP. INAFECTAS:")
            c.setFont(self.style.font_normal, self.style.size_normal)
            c.drawRightString(x_val, y, f"{datos['simbolo_moneda']} {datos['op_inafecta']:.2f}")

        if datos.get('descuento'):
            y -= 18
            c.setFont(self.style.font_bold, self.style.size_normal)
            c.drawString(x_inicio, y, "TOTAL DCTO GLOBAL:")
            c.setFont(self.style.font_normal, self.style.size_normal)
            c.drawRightString(x_val, y, f"{datos['simbolo_moneda']} {datos['descuento']['monto']:.2f}")

        y -= 18
        c.setFont(self.style.font_bold, self.style.size_normal)
        c.drawString(x_inicio, y, "IGV 18%:")
        c.setFont(self.style.font_normal, self.style.size_normal)
        c.drawRightString(x_val, y, f"{datos['simbolo_moneda']} {datos['igv']:.2f}")

        if datos.get('total_cargos', 0) > 0:
            y -= 18
            c.setFont(self.style.font_bold, self.style.size_normal)
            c.drawString(x_inicio, y, "TOTAL CARGOS:")
            c.setFont(self.style.font_normal, self.style.size_normal)
            c.drawRightString(x_val, y, f"{datos['simbolo_moneda']} {datos['total_cargos']:.2f}")

        if datos.get('otros_cargos', 0) > 0:
            y -= 18
            c.setFont(self.style.font_bold, self.style.size_normal)
            c.drawString(x_inicio, y, "OTROS CARGOS:")
            c.setFont(self.style.font_normal, self.style.size_normal)
            c.drawRightString(x_val, y, f"{datos['simbolo_moneda']} {datos['otros_cargos']:.2f}")

        # Total
        y -= 25
        c.setFillColor(self.style.table_header_bg)
        c.setStrokeColor(self.style.border_color)
        c.rect(x_inicio - 10, y - 4, 215, 26, fill=True, stroke=True)

        # Usar color de texto de encabezado para contraste correcto
        c.setFillColor(self.style.table_header_text)
        c.setFont(self.style.font_bold, 11)
        c.drawString(x_inicio, y + 6, "IMPORTE TOTAL:")
        c.setFont(self.style.font_bold, 11)
        c.drawRightString(x_val, y + 6, f"{datos['simbolo_moneda']} {datos['total']:.2f}")

        # Monto en letras
        y -= 40
        c.setFillColor(colors.black)
        c.setFont(self.style.font_bold, self.style.size_small)
        c.drawString(self.style.margin_x, y, "SON:")
        c.setFont(self.style.font_normal, self.style.size_small)

        # Dividir el texto si es muy largo
        texto_letras = datos['total_letras']
        y = self._draw_wrapped_text(c, texto_letras, self.style.margin_x + 30, y, 450, self.style.font_normal, self.style.size_small)

        return y - 25

    def _dibujar_pie(self, c, datos, width, height, y_inicial=None):
        """Dibuja el pie de la factura"""
        if y_inicial is not None:
            y = y_inicial - 20 # Mayor separación del bloque anterior
        else:
            y = 200

        # Verificar si cabe en la página actual
        # Estimamos altura del pie (~80 unidades)
        if y < 80:
            c.showPage()
            self._dibujar_encabezado_pagina_nueva(c, datos, width, height)
            y = height - 100

        x = self.style.margin_x

        # Forma de pago
        c.setFont(self.style.font_bold, self.style.size_normal)
        c.drawString(x, y, "FORMA DE PAGO:")
        c.setFont(self.style.font_normal, self.style.size_normal)
        c.drawString(x + 100, y, datos['forma_pago'])

        # Cuotas si es a crédito
        if datos['con_credito'] and datos['cuotas']:
            # Calcular altura necesaria para las cuotas
            # Encabezado (22) + Tabla Header (15) + Filas (12 * n)
            altura_cuotas = 37 + (len(datos['cuotas']) * 12)
            
            # Verificar si cabe en el espacio actual (dejando 60 de margen para el pie fijo)
            if y - altura_cuotas < 60:
                c.showPage()
                self._dibujar_encabezado_pagina_nueva(c, datos, width, height)
                y = height - 100
                
            y -= 22
            c.setFont(self.style.font_bold, self.style.size_small)
            c.drawString(x, y, "DATOS DE CUOTA:")

            # Encabezado de tabla de cuotas
            y -= 15
            c.setFillColor(self.style.table_header_bg)
            c.rect(x, y - 10, 300, 12, fill=True, stroke=False)

            c.setFillColor(self.style.color_text_header)
            c.setFont(self.style.font_bold, 7)
            c.drawString(x + 5, y - 6, "Nº CUOTA")
            c.drawString(x + 70, y - 6, "MONTO")
            c.drawString(x + 170, y - 6, "FECHA VENCIMIENTO")

            y -= 18
            c.setFillColor(colors.black)
            c.setFont(self.style.font_normal, 8)
            for cuota in datos['cuotas']:
                texto = f"{cuota['numero']}"
                c.drawString(x + 15, y, texto)
                c.drawString(x + 70, y, f"{datos['simbolo_moneda']} {cuota['monto']:.2f}")
                c.drawString(x + 170, y, cuota['fecha_vencimiento'].strftime('%d/%m/%Y'))
                y -= 12

                if y < 60:
                    break

        # Observaciones
        if datos.get('observaciones'):
            y = max(y - 20, 55)
            c.setFont(self.style.font_bold, self.style.size_small)
            c.drawString(x, y, "OBSERVACIONES:")
            c.setFont(self.style.font_normal, 7)
            y -= 12
            
            obs = datos['observaciones']
            self._draw_wrapped_text(c, obs, x + 5, y, 500, self.style.font_normal, 7)

        # Pie de página
        c.setFont(self.style.font_italic, 7)
        c.setFillColor(colors.grey)
        c.drawCentredString(width / 2, 35, "Representación impresa de la Factura Electrónica")
        c.drawCentredString(width / 2, 25, f"Generado el {datos['fecha_emision'].strftime('%d/%m/%Y a las %H:%M')}")

if __name__ == "__main__":
    from generator import FacturaGenerator

    # Test: generar facturas de diferentes tipos y estilos
    gen = FacturaGenerator()
    
    # Prueba Estilo Clásico
    pdf_gen_clasico = PDFFactura(output_dir="test_pdfs", estilo="clasico")
    print("Generando factura de HOTEL (Clásico)...")
    factura_hotel = gen.generar_factura(tipo_factura='hotel', con_credito=True)
    archivo1 = pdf_gen_clasico.crear_factura(factura_hotel, filename="Factura_Clasica.pdf")
    print(f"✓ Hotel: {archivo1}")

    # Prueba Estilo Moderno
    pdf_gen_moderno = PDFFactura(output_dir="test_pdfs", estilo="moderno")
    print("\nGenerando factura con DESCUENTOS (Moderno)...")
    factura_desc = gen.generar_factura(tipo_factura='con_descuento', con_credito=False)
    archivo2 = pdf_gen_moderno.crear_factura(factura_desc, filename="Factura_Moderna.pdf")
    print(f"✓ Descuento: {archivo2}")

    # Prueba Estilo Minimalista
    pdf_gen_minimal = PDFFactura(output_dir="test_pdfs", estilo="minimalista")
    print("\nGenerando factura GENERAL (Minimalista)...")
    factura_gen = gen.generar_factura(tipo_factura='general', categoria_items='construccion')
    archivo3 = pdf_gen_minimal.crear_factura(factura_gen, filename="Factura_Minimalista.pdf")
    print(f"✓ General: {archivo3}")

    print("\n✅ Todas las pruebas completadas!")
