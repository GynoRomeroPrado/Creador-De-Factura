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
from datetime import datetime
from typing import Dict, Optional


class DatasetExporter:
    """Exporta facturas en estructura de dataset con anotaciones y PDFs"""

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
        Convierte una factura generada al formato de anotación
        Args:
            factura: Diccionario con datos de factura generada
        Returns:
            Diccionario con formato de anotación
        """
        # Determinar tipo_documento
        tipo_doc = factura.get("tipo_comprobante", "FACTURA ELECTRÓNICA")

        # Serie completa (ej: F020-00051515)
        serie_completa = factura.get("numero_factura", "F001-000001")

        # Fechas
        fecha_emision = factura.get("fecha_emision")
        if isinstance(fecha_emision, datetime):
            # Variar formato de fecha aleatoriamente para realismo
            import random
            formato = random.choice([
                "%d-%m-%Y",      # 20-08-2025
                "%d/%m/%Y",      # 11/07/2025
                "%Y-%m-%d"       # 2025-07-24
            ])
            fecha_emision_str = fecha_emision.strftime(formato)
        else:
            fecha_emision_str = str(fecha_emision)

        # Fecha vencimiento (30 días después)
        fecha_vencimiento = factura.get("fecha_vencimiento")
        if fecha_vencimiento:
            if isinstance(fecha_vencimiento, datetime):
                import random
                formato = random.choice(["%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d"])
                fecha_vencimiento_str = fecha_vencimiento.strftime(formato)
            else:
                fecha_vencimiento_str = str(fecha_vencimiento)
        else:
            # 30 días después de emisión
            from datetime import timedelta
            if isinstance(fecha_emision, datetime):
                fecha_venc = fecha_emision + timedelta(days=30)
                import random
                formato = random.choice(["%d-%m-%Y", "%d/%m/%Y", "%Y-%m-%d"])
                fecha_vencimiento_str = fecha_venc.strftime(formato)
            else:
                fecha_vencimiento_str = None

        # Moneda
        moneda_codigo = factura.get("moneda", "PEN")
        if moneda_codigo == "PEN":
            moneda = "SOLES"
        elif moneda_codigo == "USD":
            moneda = "USD"
        elif moneda_codigo == "EUR":
            moneda = "EUROS"
        else:
            moneda = moneda_codigo

        # Variar formato de moneda aleatoriamente
        import random
        if moneda == "USD":
            moneda = random.choice(["USD", "DÓLARES AMERICANOS"])
        elif moneda == "SOLES":
            moneda = random.choice(["SOLES", "S/"])

        # Emisor
        emisor = factura.get("emisor", {})
        emisor_ruc = emisor.get("ruc", "")
        emisor_razon_social = emisor.get("razon_social", "")
        emisor_nombre_comercial = emisor.get("nombre_comercial") or emisor_razon_social
        emisor_direccion = emisor.get("direccion", "")
        emisor_telefono = emisor.get("telefono")
        emisor_email = emisor.get("email")

        # Receptor
        receptor = factura.get("receptor", {})
        receptor_numero_doc = receptor.get("ruc", "")
        receptor_razon_social = receptor.get("razon_social", "")
        receptor_direccion = receptor.get("direccion", "")

        # Importes
        # El subtotal es la base imponible (op_gravada)
        subtotal = factura.get("op_gravada", factura.get("subtotal", 0.0))
        igv = factura.get("igv", 0.0)
        importe_total = factura.get("total", 0.0)
        descuento = factura.get("descuento_total", 0.0) if factura.get("descuento_total", 0.0) > 0 else None
        otros_cargos = factura.get("total_cargos", 0.0) if factura.get("total_cargos", 0.0) > 0 else None

        # Condición de pago
        forma_pago = factura.get("forma_pago", "")
        if "CREDITO" in forma_pago.upper():
            condicion_pago = random.choice(["Credito", "Crédito"])
        else:
            condicion_pago = "Contado"

        # Observaciones
        observaciones = self._generar_observaciones(factura)

        # Glosa (monto en letras)
        glosa = factura.get("monto_letras")
        if glosa and moneda in ["SOLES", "S/"]:
            glosa = glosa.upper()

        # Crear anotación
        anotacion = {
            "tipo_documento": tipo_doc,
            "serie_completa": serie_completa,
            "fecha_emision": fecha_emision_str,
            "fecha_vencimiento": fecha_vencimiento_str,
            "moneda": moneda,
            "emisor_ruc": emisor_ruc,
            "emisor_razon_social": emisor_razon_social,
            "emisor_nombre_comercial": emisor_nombre_comercial,
            "emisor_direccion": emisor_direccion,
            "emisor_telefono": emisor_telefono,
            "emisor_email": emisor_email,
            "receptor_numero_doc": receptor_numero_doc,
            "receptor_tipo_doc": "RUC" if receptor_numero_doc else None,
            "receptor_razon_social": receptor_razon_social,
            "receptor_direccion": receptor_direccion,
            "subtotal": round(subtotal, 2),
            "igv": round(igv, 2),
            "importe_total": round(importe_total, 2),
            "descuento": descuento,
            "otros_cargos": otros_cargos,
            "numero_contrato": None,
            "orden_compra": None,
            "guia_remision": None,
            "condicion_pago": condicion_pago,
            "observaciones": observaciones,
            "glosa": glosa,
            "detraccion_porcentaje": None,
            "detraccion_monto": None
        }

        return anotacion

    def _generar_observaciones(self, factura: Dict) -> Optional[str]:
        """Genera texto de observaciones basado en tipo de factura"""
        observaciones = []

        # Monto en letras
        if factura.get("monto_letras"):
            observaciones.append(f"Monto en letra: {factura['monto_letras']}.")

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
