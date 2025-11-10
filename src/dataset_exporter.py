"""
Exportador de facturas en formato Dataset
Estructura:
  facturas_generadas/
    Dataset_YYYYMMDD_HHMM/
      anotaciones/       (JSONs)
      facturas_procesadas/ (PDFs)
      rechazadas/        (vacía)
      reportes/          (vacía)
"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Optional


class DatasetExporter:
    """Exporta facturas en estructura de dataset con anotaciones y PDFs"""

    # Mapeo de ciudades/provincias a departamentos del Perú
    DEPARTAMENTOS_PERU = {
        # Ciudades principales a departamentos
        "CHICLAYO": "LAMBAYEQUE",
        "LAMBAYEQUE": "LAMBAYEQUE",
        "CHIMBOTE": "ANCASH",
        "HUARAZ": "ANCASH",
        "TRUJILLO": "LA LIBERTAD",
        "PIURA": "PIURA",
        "SULLANA": "PIURA",
        "TALARA": "PIURA",
        "IQUITOS": "LORETO",
        "CUSCO": "CUSCO",
        "AREQUIPA": "AREQUIPA",
        "TACNA": "TACNA",
        "ICA": "ICA",
        "HUANCAYO": "JUNIN",
        "PUNO": "PUNO",
        "AYACUCHO": "AYACUCHO",
        "CAJAMARCA": "CAJAMARCA",
        "HUÁNUCO": "HUANUCO",
        "PUCALLPA": "UCAYALI",
        "TARAPOTO": "SAN MARTIN",
        "TUMBES": "TUMBES",
        "MOQUEGUA": "MOQUEGUA",
        "PUERTO MALDONADO": "MADRE DE DIOS",
        "CHINCHA": "ICA",
        "CALLAO": "CALLAO",
        "JULIACA": "PUNO",
        # Lima y provincias
        "LIMA": "LIMA",
        "SAN ISIDRO": "LIMA",
        "MIRAFLORES": "LIMA",
        "SAN BORJA": "LIMA",
        "SURCO": "LIMA",
        "LA MOLINA": "LIMA",
        "SAN MIGUEL": "LIMA",
        "BARRANCO": "LIMA",
        "CHORRILLOS": "LIMA",
    }

    def __init__(self, base_dir: str = "facturas_generadas"):
        """
        Inicializa el exportador
        Args:
            base_dir: Directorio base donde se creará el dataset
        """
        self.base_dir = base_dir
        self.dataset_dir = None
        self.anotaciones_dir = None
        self.procesadas_dir = None
        self.rechazadas_dir = None
        self.reportes_dir = None

    def crear_dataset(self, timestamp: Optional[datetime] = None) -> str:
        """
        Crea la estructura de carpetas del dataset
        Args:
            timestamp: Fecha/hora para el nombre del dataset (None = ahora)
        Returns:
            Ruta del directorio del dataset
        """
        if timestamp is None:
            timestamp = datetime.now()

        # Formato: Dataset_YYYYMMDD_HHMM
        dataset_name = timestamp.strftime("Dataset_%Y%m%d_%H%M")
        self.dataset_dir = os.path.join(self.base_dir, dataset_name)

        # Crear subcarpetas
        self.anotaciones_dir = os.path.join(self.dataset_dir, "anotaciones")
        self.procesadas_dir = os.path.join(self.dataset_dir, "facturas_procesadas")
        self.rechazadas_dir = os.path.join(self.dataset_dir, "rechazadas")
        self.reportes_dir = os.path.join(self.dataset_dir, "reportes")

        # Crear todas las carpetas
        for carpeta in [self.anotaciones_dir, self.procesadas_dir,
                       self.rechazadas_dir, self.reportes_dir]:
            os.makedirs(carpeta, exist_ok=True)

        return self.dataset_dir

    def convertir_factura_a_anotacion(self, factura: Dict) -> Dict:
        """
        Convierte una factura generada al formato de anotación oficial InvoiceX v5.5
        Args:
            factura: Diccionario con datos de factura generada
        Returns:
            Diccionario con formato de anotación (97 campos + items + cuotas)
        """
        import random

        # ========== SECCIÓN 1: DOCUMENTO (5 campos) ==========

        # Normalizar tipo de documento (sin tildes, mayúsculas)
        # Soporta: "FACTURA ELECTRONICA" y "BOLETA DE VENTA ELECTRONICA"
        tipo_doc = factura.get("tipo_comprobante", "FACTURA ELECTRONICA")
        tipo_doc = tipo_doc.upper().replace("Ó", "O").replace("É", "E")

        # Asegurar que incluye "ELECTRONICA" y formato correcto
        if "BOLETA" in tipo_doc:
            tipo_doc = "BOLETA DE VENTA ELECTRONICA"
        elif "FACTURA" in tipo_doc:
            tipo_doc = "FACTURA ELECTRONICA"
        else:
            # Por defecto
            tipo_doc = "FACTURA ELECTRONICA"

        # Serie completa
        serie_completa = factura.get("numero_factura", "F001-000001")

        # Fechas en formato YYYY-MM-DD (sin hora)
        fecha_emision = factura.get("fecha_emision")
        if isinstance(fecha_emision, datetime):
            fecha_emision_str = fecha_emision.strftime("%Y-%m-%d")
        else:
            fecha_emision_str = str(fecha_emision) if fecha_emision else None

        fecha_vencimiento = factura.get("fecha_vencimiento")
        if isinstance(fecha_vencimiento, datetime):
            fecha_vencimiento_str = fecha_vencimiento.strftime("%Y-%m-%d")
        else:
            fecha_vencimiento_str = fecha_emision_str

        # Normalizar moneda según InvoiceX v5.5
        moneda_codigo = factura.get("moneda", "PEN")
        if moneda_codigo in ["PEN", "S/", "SOLES"]:
            moneda = "SOLES"
        elif moneda_codigo in ["USD", "$", "DOLARES", "DÓLARES"]:
            moneda = "DOLARES AMERICANOS"
        elif moneda_codigo in ["EUR", "€", "EUROS"]:
            moneda = "EUROS"
        else:
            moneda = moneda_codigo

        # ========== SECCIÓN 2: EMISOR (14 campos) ==========

        emisor_data = factura.get("emisor", {})

        # Extraer ubicación de la dirección si está disponible
        direccion_emisor = emisor_data.get("direccion", "")
        # Intentar parsear departamento, provincia, distrito de la dirección
        # Formato típico: "Av. Principal 123, Distrito, Provincia"
        partes_dir_emisor = [p.strip() for p in direccion_emisor.split(",")]

        # ========== SECCIÓN 3: RECEPTOR (14 campos) ==========

        receptor_data = factura.get("receptor", {})
        receptor_numero_doc = receptor_data.get("ruc", "")

        # Determinar tipo de documento
        if receptor_numero_doc:
            if len(receptor_numero_doc) == 11:
                receptor_tipo_doc = "RUC"
            elif len(receptor_numero_doc) == 8:
                receptor_tipo_doc = "DNI"
            else:
                receptor_tipo_doc = "RUC"
        else:
            receptor_tipo_doc = None

        # Extraer ubicación del receptor
        direccion_receptor = receptor_data.get("direccion", "")
        partes_dir_receptor = [p.strip() for p in direccion_receptor.split(",")]

        # ========== SECCIÓN 4: IMPORTES Y TRIBUTOS (19 campos) ==========
        # IMPORTANTE: Los totales se calcularán DESPUÉS de procesar los items
        # para asegurar coherencia matemática

        # Descuento
        descuento = factura.get("descuento_total", 0.0)
        if descuento > 0:
            descuento = round(descuento, 2)
        else:
            descuento = 0.0

        # Tipo de cambio (solo si es moneda extranjera)
        tipo_cambio = None
        importe_total_moneda_base = None

        # Retenciones, percepciones (no implementados)
        retencion_monto = None
        retencion_porcentaje = None
        percepcion_monto = None
        percepcion_porcentaje = None

        # Detracción (se calculará después de obtener importe_total)
        detraccion_monto = None
        detraccion_porcentaje = None
        detraccion_codigo_bienes = None
        tiene_detraccion = random.random() < 0.15  # 15% de facturas con detracción

        # Anticipos (no implementados)
        anticipo_monto = None
        anticipo_numero = None

        # ========== SECCIÓN 5: REFERENCIAS (9 campos) ==========

        numero_contrato = f"CW{random.randint(100000, 999999)}"

        # Orden de compra (aleatorio)
        orden_compra = None
        if random.random() < 0.3:
            orden_compra = f"OC-2025-{random.randint(1000, 9999)}"

        orden_servicio = None
        numero_pedido = None

        # Guía de remisión (aleatorio)
        guia_remision = None
        if random.random() < 0.25:
            guia_remision = f"T001-{random.randint(10000, 99999):08d}"

        # Condición y forma de pago
        forma_pago_original = factura.get("forma_pago", "CONTADO")
        if "CREDITO" in forma_pago_original.upper():
            condicion_pago = "Credito 30 dias"
            forma_pago = random.choice(["TRANSFERENCIA", "DEPOSITO EN CUENTA", "CREDITO"])
        else:
            condicion_pago = "Contado"
            forma_pago = random.choice(["TRANSFERENCIA", "EFECTIVO", "TARJETA", "YAPE", "PLIN"])

        cuenta_bancaria = None
        numero_cuenta_detraccion = None
        if detraccion_monto:
            numero_cuenta_detraccion = f"00000{random.randint(100000, 999999)}"

        # ========== SECCIÓN 6: INFORMACIÓN ADICIONAL (9 campos) ==========

        # Glosa
        glosa = None
        if random.random() < 0.3:
            glosas = [
                "Venta de productos varios",
                "Servicios profesionales",
                "Provision de materiales",
                "Servicios de construccion"
            ]
            glosa = random.choice(glosas)

        # Observaciones: se generará DESPUÉS de calcular importe_total
        # (ver después del procesamiento de items)
        observaciones = None

        centro_costo = None
        proyecto = None
        ubicacion_obra = None
        numero_vale = None
        numero_placa = None

        # Para hoteles, agregar datos a referencia_1 (NO a observaciones)
        referencia_1 = None
        if factura.get("datos_hotel"):
            hotel = factura["datos_hotel"]
            hotel_parts = []

            if hotel.get("checkin"):
                checkin = hotel["checkin"]
                if isinstance(checkin, datetime):
                    checkin_str = checkin.strftime("%d-%m-%Y")
                else:
                    checkin_str = str(checkin)
                hotel_parts.append(f"Checkin: {checkin_str}")

            if hotel.get("checkout"):
                checkout = hotel["checkout"]
                if isinstance(checkout, datetime):
                    checkout_str = checkout.strftime("%d-%m-%Y")
                else:
                    checkout_str = str(checkout)
                hotel_parts.append(f"CheckOut: {checkout_str}")

            if hotel.get("reserva"):
                hotel_parts.append(f"Reserva: {hotel['reserva']}")

            if hotel.get("noches"):
                hotel_parts.append(f"Noches: {hotel['noches']}")

            if hotel.get("huesped"):
                # Convertir nombre a formato APELLIDOS,NOMBRES en mayúsculas
                huesped = hotel["huesped"].upper()
                hotel_parts.append(f"Huésped: {huesped}")

            if hotel_parts:
                referencia_1 = ", ".join(hotel_parts)

        referencia_2 = None

        # ========== SECCIÓN 7: ITEMS (Array) ==========

        # Detectar si es factura de hotel
        es_hotel = factura.get("tipo_factura") == "hotel" or factura.get("datos_hotel") is not None

        items = []
        for i, item_orig in enumerate(factura.get("items", []), 1):
            valor_venta = round(item_orig.get("valor_venta", 0), 2)

            # Código del item (solo hoteles tienen código 90111500)
            codigo = "90111500" if es_hotel else None

            # Descuento del item (null para hoteles, 0.0 para generales)
            descuento_item = None if es_hotel else 0.0

            # Subtotal del item (después del descuento)
            subtotal_item = valor_venta

            # Determinar tipo de IGV
            tipo_igv = "GRAVADO"
            igv_item = round(subtotal_item * 0.18, 2)

            # ISC del item
            isc_item = None

            # Otro tributo
            # Para hoteles: 10% del valor_venta (cargo adicional por servicio)
            # Para generales: null
            otro_tributo = None
            if es_hotel:
                otro_tributo = round(valor_venta * 0.10, 2)

            # Importe total del item
            # Fórmula oficial: subtotal_item + igv_item + otro_tributo
            importe_total_item = subtotal_item + igv_item
            if otro_tributo:
                importe_total_item += otro_tributo
            importe_total_item = round(importe_total_item, 2)

            item_data = {
                "item": i,
                "codigo": codigo,
                "descripcion": item_orig.get("descripcion", ""),
                "cantidad": item_orig.get("cantidad", 0),
                "unidad_medida": item_orig.get("unidad", "NIU"),
                "precio_unitario": round(item_orig.get("precio_unitario", 0), 2),
                "valor_venta": valor_venta,
                "descuento_item": descuento_item,
                "subtotal_item": subtotal_item,
                "tipo_igv": tipo_igv,
                "igv_item": igv_item,
                "isc_item": isc_item,
                "otro_tributo": otro_tributo,
                "importe_total_item": importe_total_item,
                "lote": None,
                "fecha_vencimiento": None,
                "serie": None,
                "modelo": None,
                "marca": None,
                "placa": None,
                "partida_arancelaria": None,
                "centro_costo_item": None,
                "cuenta_contable": None,
                "proyecto_item": None,
                "orden_item": None,
                "ubicacion": None,
                "observacion_item": None
            }

            items.append(item_data)

        # ========== RECALCULAR TOTALES BASADOS EN ITEMS PROCESADOS ==========
        # IMPORTANTE: Recalcular para asegurar coherencia matemática

        # Subtotal: Suma de todos los valor_venta de los items
        subtotal = round(sum(item["valor_venta"] for item in items), 2)

        # Subtotal con descuento
        subtotal_con_descuento = round(subtotal - descuento, 2)

        # IGV: Suma de todos los igv_item
        igv = round(sum(item["igv_item"] for item in items), 2)

        # ISC (no implementado)
        isc = None

        # Otros cargos: Suma de todos los otro_tributo (cargo adicional hoteles)
        otros_cargos = 0.0
        for item in items:
            if item["otro_tributo"] is not None:
                otros_cargos += item["otro_tributo"]
        otros_cargos = round(otros_cargos, 2)

        # Importe total: Suma de todos los importe_total_item
        importe_total = round(sum(item["importe_total_item"] for item in items), 2)

        # Verificación matemática (opcional, para debugging)
        # importe_total_calculado = subtotal_con_descuento + igv + otros_cargos
        # if abs(importe_total - importe_total_calculado) > 0.10:
        #     print(f"⚠️ Diferencia en totales: {importe_total} vs {importe_total_calculado}")

        # ========== CALCULAR DETRACCIÓN (Ahora que tenemos importe_total) ==========
        if tiene_detraccion:
            detraccion_porcentaje = 10.0
            detraccion_monto = round(importe_total * 0.10, 2)

        # ========== GENERAR OBSERVACIONES (Monto en letras) ==========
        # IMPORTANTE: Generamos observaciones AQUÍ (después de calcular importe_total)
        # para asegurar que coincida con el total real

        from .utils import MontoLetras

        # Convertir moneda a formato esperado por MontoLetras
        if moneda == "SOLES":
            moneda_letras = "SOLES"
        elif moneda == "DOLARES AMERICANOS":
            moneda_letras = "DOLARES"
        elif moneda == "EUROS":
            moneda_letras = "EUROS"
        else:
            moneda_letras = moneda

        # Convertir importe_total a letras
        total_letras = MontoLetras.convertir(importe_total, moneda_letras)

        # Variar formato para realismo (basado en ejemplos reales)
        formato = random.choice([
            f"SON: {total_letras}",  # Formato más común
            f"Monto en letra: {total_letras}",  # Hoteles
            f"** ({total_letras}) **",  # Algunos hoteles
        ])
        observaciones = formato

        # ========== SECCIÓN 8: CUOTAS (Array) ==========

        cuotas = []
        if "CREDITO" in forma_pago_original.upper() and random.random() < 0.4:
            # Generar 2-4 cuotas
            num_cuotas = random.choice([2, 3, 4])
            monto_cuota = round(importe_total / num_cuotas, 2)

            for i in range(1, num_cuotas + 1):
                # Ajustar última cuota para redondeo
                if i == num_cuotas:
                    monto_cuota = round(importe_total - (monto_cuota * (num_cuotas - 1)), 2)

                # Fecha de vencimiento: escalonar cada 30 días
                # Cuota 1: fecha_vencimiento + 0 días
                # Cuota 2: fecha_vencimiento + 30 días
                # Cuota 3: fecha_vencimiento + 60 días, etc.
                try:
                    # Parsear fecha_vencimiento_str a datetime
                    fecha_base = datetime.strptime(fecha_vencimiento_str, "%Y-%m-%d")
                    # Escalonar: primera cuota en fecha_vencimiento, luego +30 días cada una
                    fecha_cuota = fecha_base + timedelta(days=30 * (i - 1))
                    fecha_cuota_str = fecha_cuota.strftime("%Y-%m-%d")
                except Exception:
                    # Si hay error, usar fecha_vencimiento_str
                    fecha_cuota_str = fecha_vencimiento_str

                cuotas.append({
                    "numero": i,
                    "monto": monto_cuota,
                    "fecha_vencimiento": fecha_cuota_str,
                    "estado": None
                })

        # ========== SECCIÓN 9: CAMPOS SUNAT (5 campos) ==========

        cod_qr = None
        hash_sunat = None
        numero_autorizacion = None
        serie_fisica = None
        numero_fisico = None

        # ========== SECCIÓN 10: DOCUMENTO RELACIONADO (4 campos) ==========

        doc_relacionado_tipo = None
        doc_relacionado_numero = None
        doc_relacionado_fecha = None
        motivo_emision = None

        # ========== SECCIÓN 11: UBICACIÓN EMISOR (8 campos) ==========

        # Intentar extraer de dirección
        # Formato típico: "Calle 123, Distrito, Provincia, Departamento"
        # o "Calle 123, Distrito, Ciudad" (cuando provincia = departamento)

        if len(partes_dir_emisor) >= 4:
            # Formato completo: Calle, Distrito, Provincia, Departamento
            ciudad = partes_dir_emisor[-1].upper()
            emisor_provincia = partes_dir_emisor[-2].upper()
            emisor_distrito = partes_dir_emisor[-3].upper()
            # Mapear ciudad a departamento correcto
            emisor_departamento = self.DEPARTAMENTOS_PERU.get(ciudad, ciudad)
        elif len(partes_dir_emisor) >= 3:
            # Formato: Calle, Distrito, Ciudad (asumir que ciudad es departamento y provincia)
            ciudad = partes_dir_emisor[-1].upper()
            emisor_distrito = partes_dir_emisor[-2].upper()
            # Mapear ciudad a departamento correcto
            emisor_departamento = self.DEPARTAMENTOS_PERU.get(ciudad, ciudad)
            emisor_provincia = emisor_departamento  # Mismo que departamento
        elif len(partes_dir_emisor) >= 2:
            # Solo Calle, Ciudad
            ciudad = partes_dir_emisor[-1].upper()
            emisor_departamento = self.DEPARTAMENTOS_PERU.get(ciudad, ciudad)
            emisor_provincia = emisor_departamento
            emisor_distrito = None
        else:
            # Por defecto
            emisor_departamento = "LIMA"
            emisor_provincia = "LIMA"
            emisor_distrito = None

        emisor_ubigeo = None
        emisor_codigo_postal = None
        emisor_codigo_establecimiento = None

        # ========== SECCIÓN 12: UBICACIÓN RECEPTOR (6 campos) ==========

        # Misma lógica para receptor con mapeo de departamentos
        if len(partes_dir_receptor) >= 4:
            ciudad = partes_dir_receptor[-1].upper()
            receptor_provincia = partes_dir_receptor[-2].upper()
            receptor_distrito = partes_dir_receptor[-3].upper()
            # Mapear ciudad a departamento correcto
            receptor_departamento = self.DEPARTAMENTOS_PERU.get(ciudad, ciudad)
        elif len(partes_dir_receptor) >= 3:
            ciudad = partes_dir_receptor[-1].upper()
            receptor_distrito = partes_dir_receptor[-2].upper()
            # Mapear ciudad a departamento correcto
            receptor_departamento = self.DEPARTAMENTOS_PERU.get(ciudad, ciudad)
            receptor_provincia = receptor_departamento  # Mismo que departamento
        elif len(partes_dir_receptor) >= 2:
            ciudad = partes_dir_receptor[-1].upper()
            receptor_departamento = self.DEPARTAMENTOS_PERU.get(ciudad, ciudad)
            receptor_provincia = receptor_departamento
            receptor_distrito = None
        else:
            receptor_departamento = None
            receptor_provincia = None
            receptor_distrito = None

        receptor_ubigeo = None
        receptor_codigo_postal = None

        # ========== SECCIÓN 13: EXPORTACIÓN (6 campos) ==========

        is_exportacion = False
        incoterm = None
        puerto_embarque = None
        puerto_destino = None
        nave = None
        numero_contenedor = None

        # ========== SECCIÓN 14: RÉGIMEN TRIBUTARIO (3 campos) ==========

        agente_retencion = random.choice([True, False])
        agente_percepcion = False
        buen_contribuyente = random.choice([True, False])

        # ========== SECCIÓN 15: PERSONAL (4 campos) ==========

        vendedor_codigo = None
        vendedor_nombre = None
        cajero_codigo = None
        cajero_nombre = None

        # ========== SECCIÓN 16: FECHAS ADICIONALES (3 campos) ==========

        fecha_registro = None
        fecha_pago = None
        fecha_cancelacion = None

        # ========== CONSTRUIR JSON FINAL (Estructura InvoiceX v5.5) ==========

        anotacion = {
            # SECCIÓN 1: DOCUMENTO (5 campos)
            "tipo_documento": tipo_doc,
            "serie_completa": serie_completa,
            "fecha_emision": fecha_emision_str,
            "fecha_vencimiento": fecha_vencimiento_str,
            "moneda": moneda,

            # SECCIÓN 2: EMISOR (14 campos)
            "emisor_ruc": emisor_data.get("ruc", ""),
            "emisor_razon_social": emisor_data.get("razon_social", ""),
            "emisor_direccion": direccion_emisor,
            "emisor_sucursal": None,
            "emisor_telefono": emisor_data.get("telefono"),
            "emisor_web": None,
            "emisor_departamento": emisor_departamento,
            "emisor_provincia": emisor_provincia,
            "emisor_distrito": emisor_distrito,
            "emisor_ubigeo": emisor_ubigeo,
            "emisor_codigo_postal": emisor_codigo_postal,
            "emisor_email": emisor_data.get("email"),
            "emisor_nombre_comercial": emisor_data.get("nombre_comercial") or emisor_data.get("razon_social", ""),
            "emisor_codigo_establecimiento": emisor_codigo_establecimiento,

            # SECCIÓN 3: RECEPTOR (14 campos)
            "receptor_numero_doc": receptor_numero_doc,
            "receptor_tipo_doc": receptor_tipo_doc,
            "receptor_razon_social": receptor_data.get("razon_social", ""),
            "receptor_direccion": direccion_receptor,
            "receptor_contacto": None,
            "receptor_telefono": receptor_data.get("telefono"),
            "receptor_email": receptor_data.get("email"),
            "receptor_sucursal": None,
            "receptor_departamento": receptor_departamento,
            "receptor_provincia": receptor_provincia,
            "receptor_distrito": receptor_distrito,
            "receptor_ubigeo": receptor_ubigeo,
            "receptor_codigo_postal": receptor_codigo_postal,
            "receptor_nombre_comercial": None,

            # SECCIÓN 4: IMPORTES Y TRIBUTOS (19 campos)
            "subtotal": subtotal,
            "descuento": descuento,
            "subtotal_con_descuento": subtotal_con_descuento,
            "igv": igv,
            "isc": isc,
            "otros_cargos": otros_cargos,
            "importe_total": importe_total,
            "tipo_cambio": tipo_cambio,
            "importe_total_moneda_base": importe_total_moneda_base,
            "retencion_monto": retencion_monto,
            "retencion_porcentaje": retencion_porcentaje,
            "percepcion_monto": percepcion_monto,
            "percepcion_porcentaje": percepcion_porcentaje,
            "detraccion_monto": detraccion_monto,
            "detraccion_porcentaje": detraccion_porcentaje,
            "detraccion_codigo_bienes": detraccion_codigo_bienes,
            "anticipo_monto": anticipo_monto,
            "anticipo_numero": anticipo_numero,

            # SECCIÓN 5: REFERENCIAS (9 campos)
            "numero_contrato": numero_contrato,
            "orden_compra": orden_compra,
            "orden_servicio": orden_servicio,
            "numero_pedido": numero_pedido,
            "guia_remision": guia_remision,
            "condicion_pago": condicion_pago,
            "forma_pago": forma_pago,
            "cuenta_bancaria": cuenta_bancaria,
            "numero_cuenta_detraccion": numero_cuenta_detraccion,

            # SECCIÓN 6: INFORMACIÓN ADICIONAL (9 campos)
            "glosa": glosa,
            "observaciones": observaciones,
            "centro_costo": centro_costo,
            "proyecto": proyecto,
            "ubicacion_obra": ubicacion_obra,
            "numero_vale": numero_vale,
            "numero_placa": numero_placa,
            "referencia_1": referencia_1,
            "referencia_2": referencia_2,

            # SECCIÓN 9: CAMPOS SUNAT (5 campos)
            "cod_qr": cod_qr,
            "hash_sunat": hash_sunat,
            "numero_autorizacion": numero_autorizacion,
            "serie_fisica": serie_fisica,
            "numero_fisico": numero_fisico,

            # SECCIÓN 10: DOCUMENTO RELACIONADO (4 campos)
            "doc_relacionado_tipo": doc_relacionado_tipo,
            "doc_relacionado_numero": doc_relacionado_numero,
            "doc_relacionado_fecha": doc_relacionado_fecha,
            "motivo_emision": motivo_emision,

            # SECCIÓN 13: EXPORTACIÓN (6 campos)
            "is_exportacion": is_exportacion,
            "incoterm": incoterm,
            "puerto_embarque": puerto_embarque,
            "puerto_destino": puerto_destino,
            "nave": nave,
            "numero_contenedor": numero_contenedor,

            # SECCIÓN 14: RÉGIMEN TRIBUTARIO (3 campos)
            "agente_retencion": agente_retencion,
            "agente_percepcion": agente_percepcion,
            "buen_contribuyente": buen_contribuyente,

            # SECCIÓN 15: PERSONAL (4 campos)
            "vendedor_codigo": vendedor_codigo,
            "vendedor_nombre": vendedor_nombre,
            "cajero_codigo": cajero_codigo,
            "cajero_nombre": cajero_nombre,

            # SECCIÓN 16: FECHAS ADICIONALES (3 campos)
            "fecha_registro": fecha_registro,
            "fecha_pago": fecha_pago,
            "fecha_cancelacion": fecha_cancelacion,

            # SECCIÓN 7: ITEMS (Array)
            "items": items,

            # SECCIÓN 8: CUOTAS (Array)
            "cuotas": cuotas
        }

        return anotacion

    def _generar_observaciones(self, factura: Dict) -> Optional[str]:
        """Genera texto de observaciones basado en tipo de factura"""
        observaciones = []

        # Monto en letras
        if factura.get("total_letras"):
            observaciones.append(f"Monto en letra: {factura['total_letras']}.")

        # Datos de hotel si aplica
        if factura.get("datos_hotel"):
            hotel = factura["datos_hotel"]
            obs_hotel = []
            if hotel.get("huesped"):
                obs_hotel.append(f"Huésped: {hotel['huesped']}")
            if hotel.get("reserva"):
                obs_hotel.append(f"Reserva: {hotel['reserva']}")
            if hotel.get("checkin"):
                checkin = hotel["checkin"]
                if isinstance(checkin, datetime):
                    checkin = checkin.strftime("%d-%m-%Y")
                obs_hotel.append(f"CheckIn: {checkin}")
            if hotel.get("checkout"):
                checkout = hotel["checkout"]
                if isinstance(checkout, datetime):
                    checkout = checkout.strftime("%d-%m-%Y")
                obs_hotel.append(f"CheckOut: {checkout}")
            if hotel.get("noches"):
                obs_hotel.append(f"Noches: {hotel['noches']}")

            if obs_hotel:
                observaciones.append(". ".join(obs_hotel) + ".")

        # Notas estándar
        import random
        if random.random() < 0.3:
            observaciones.append("Representación impresa de la Factura Electrónica")

        if random.random() < 0.2:
            observaciones.append("Agente de retención de IGV incorporado por Resolución de Superintendencia")

        return " ".join(observaciones) if observaciones else None

    def exportar_factura(self, factura: Dict, pdf_content: Optional[bytes] = None) -> tuple:
        """
        Exporta una factura al dataset
        Args:
            factura: Datos de la factura
            pdf_content: Contenido del PDF (bytes) o None si no hay PDF
        Returns:
            Tupla (ruta_json, ruta_pdf)
        """
        if not self.dataset_dir:
            self.crear_dataset()

        # Obtener serie completa para nombre de archivo
        serie_completa = factura.get("numero_factura", "F001-000001")
        # Limpiar nombre (reemplazar caracteres no válidos)
        nombre_archivo = serie_completa.replace(" ", "_").replace("/", "-")

        # Convertir a formato de anotación
        anotacion = self.convertir_factura_a_anotacion(factura)

        # Guardar JSON
        json_path = os.path.join(self.anotaciones_dir, f"{nombre_archivo}.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(anotacion, f, indent=2, ensure_ascii=False)

        # Guardar PDF si existe
        pdf_path = None
        if pdf_content:
            pdf_path = os.path.join(self.procesadas_dir, f"{nombre_archivo}.pdf")
            with open(pdf_path, 'wb') as f:
                f.write(pdf_content)

        return json_path, pdf_path

    def obtener_estadisticas(self) -> Dict:
        """Retorna estadísticas del dataset"""
        if not self.dataset_dir or not os.path.exists(self.dataset_dir):
            return {}

        num_anotaciones = len([f for f in os.listdir(self.anotaciones_dir)
                               if f.endswith('.json')])
        num_pdfs = len([f for f in os.listdir(self.procesadas_dir)
                       if f.endswith('.pdf')])

        return {
            "dataset": os.path.basename(self.dataset_dir),
            "anotaciones": num_anotaciones,
            "pdfs": num_pdfs,
            "rechazadas": 0,
            "reportes": 0
        }
