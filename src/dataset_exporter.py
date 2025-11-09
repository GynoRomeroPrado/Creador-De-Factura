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
        import random

        # Tipo de comprobante y factura
        tipo_comprobante = factura.get("tipo_comprobante", "FACTURA ELECTRÓNICA")
        tipo_factura = factura.get("tipo_factura", "general")

        # Serie completa (ej: F689-799377)
        numero_factura = factura.get("numero_factura", "F001-000001")

        # Extraer serie y número
        if "-" in numero_factura:
            serie, numero = numero_factura.split("-", 1)
        else:
            serie = numero_factura[:4]
            numero = numero_factura[4:]

        # Fechas en formato ISO
        fecha_emision = factura.get("fecha_emision")
        if isinstance(fecha_emision, datetime):
            fecha_emision_str = fecha_emision.strftime("%Y-%m-%dT00:00:00")
        else:
            fecha_emision_str = str(fecha_emision)

        fecha_vencimiento = factura.get("fecha_vencimiento")
        if isinstance(fecha_vencimiento, datetime):
            fecha_vencimiento_str = fecha_vencimiento.strftime("%Y-%m-%dT00:00:00")
        else:
            fecha_vencimiento_str = fecha_emision_str

        # Moneda
        moneda_codigo = factura.get("moneda", "PEN")
        if moneda_codigo == "PEN":
            simbolo_moneda = "S/"
            nombre_moneda = "SOLES"
        elif moneda_codigo == "USD":
            simbolo_moneda = "$"
            nombre_moneda = "DOLARES"
        elif moneda_codigo == "EUR":
            simbolo_moneda = "€"
            nombre_moneda = "EUROS"
        else:
            simbolo_moneda = moneda_codigo
            nombre_moneda = moneda_codigo

        # Emisor (nested object)
        emisor_data = factura.get("emisor", {})
        emisor = {
            "ruc": emisor_data.get("ruc", ""),
            "razon_social": emisor_data.get("razon_social", ""),
            "direccion": emisor_data.get("direccion", ""),
            "telefono": emisor_data.get("telefono", ""),
            "email": emisor_data.get("email", "")
        }

        # Receptor (nested object)
        receptor_data = factura.get("receptor", {})
        receptor = {
            "ruc": receptor_data.get("ruc", ""),
            "razon_social": receptor_data.get("razon_social", ""),
            "direccion": receptor_data.get("direccion", ""),
            "telefono": receptor_data.get("telefono", ""),
            "email": receptor_data.get("email", "")
        }

        # Calcular totales de items
        items = []
        op_gravada = 0.0
        total_cargos = 0.0

        for item in factura.get("items", []):
            valor_venta = round(item.get("valor_venta", 0), 2)
            op_gravada += valor_venta

            item_data = {
                "numero": item.get("numero"),
                "descripcion": item.get("descripcion"),
                "unidad": item.get("unidad"),
                "cantidad": item.get("cantidad"),
                "precio_unitario": round(item.get("precio_unitario", 0), 2),
                "valor_venta": valor_venta
            }

            # Agregar cargo_item e importe_total si existe (típico en hoteles)
            if "cargo_item" in item:
                cargo = round(item["cargo_item"], 2)
                item_data["cargo_item"] = cargo
                item_data["importe_total"] = round(valor_venta + cargo, 2)
                total_cargos += cargo

            items.append(item_data)

        # Operaciones
        op_gravada = round(op_gravada, 2)
        op_exonerada = 0.0
        op_inafecta = round(total_cargos, 2)  # Los cargos son inafectos (no tienen IGV)
        op_gratuitas = 0.0

        # IGV y total
        igv = round(factura.get("igv", 0.0), 2)
        total_cargos = round(total_cargos, 2)
        otros_cargos = 0.0
        total = round(factura.get("total", 0.0), 2)

        # Total en letras
        total_letras = factura.get("total_letras", "")

        # Forma de pago
        forma_pago = factura.get("forma_pago", "CONTADO")
        con_credito = "CREDITO" in forma_pago.upper()
        cuotas = []

        # Número de contrato (aleatorio)
        numero_contrato = f"CW{random.randint(100000, 999999)}"

        # Datos de hotel (nested object o null)
        datos_hotel = None
        if factura.get("datos_hotel"):
            hotel_data = factura["datos_hotel"]
            datos_hotel = {
                "checkin": hotel_data["checkin"].strftime("%Y-%m-%dT00:00:00") if isinstance(hotel_data.get("checkin"), datetime) else str(hotel_data.get("checkin")),
                "checkout": hotel_data["checkout"].strftime("%Y-%m-%dT00:00:00") if isinstance(hotel_data.get("checkout"), datetime) else str(hotel_data.get("checkout")),
                "noches": hotel_data.get("noches"),
                "reserva": str(hotel_data.get("reserva", "")),
                "huesped": hotel_data.get("huesped", ""),
                "codigo_grupo": hotel_data.get("codigo_grupo"),
                "nombre_grupo": hotel_data.get("nombre_grupo"),
                "habitacion": hotel_data.get("habitacion")
            }

        # Descuento (si existe)
        descuento = None
        descuento_val = factura.get("descuento_total", 0.0)
        if descuento_val > 0:
            descuento = round(descuento_val, 2)

        # Crear anotación con nuevo formato
        anotacion = {
            "tipo_comprobante": tipo_comprobante,
            "tipo_factura": tipo_factura,
            "numero_factura": numero_factura,
            "serie": serie,
            "numero": numero,
            "fecha_emision": fecha_emision_str,
            "fecha_vencimiento": fecha_vencimiento_str,
            "emisor": emisor,
            "receptor": receptor,
            "moneda": moneda_codigo,
            "simbolo_moneda": simbolo_moneda,
            "nombre_moneda": nombre_moneda,
            "items": items,
            "op_gravada": op_gravada,
            "op_exonerada": op_exonerada,
            "op_inafecta": op_inafecta,
            "op_gratuitas": op_gratuitas,
            "igv": igv,
            "total_cargos": total_cargos,
            "otros_cargos": otros_cargos,
            "total": total,
            "total_letras": total_letras,
            "forma_pago": forma_pago,
            "con_credito": con_credito,
            "cuotas": cuotas,
            "numero_contrato": numero_contrato,
            "periodo_facturado": None,
            "observaciones": None,
            "datos_hotel": datos_hotel,
            "datos_seguro": None,
            "descuento": descuento
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
