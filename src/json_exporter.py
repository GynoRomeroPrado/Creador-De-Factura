"""
Exportador de facturas a JSON en formato InvoiceX v5.5
IMPORTANTE: Ahora exporta en formato plano con 97 campos según especificación InvoiceX v5.5
"""
import json
import os
from datetime import datetime
from typing import Dict, List


class JSONExporter:
    """Exporta facturas a formato JSON en formato InvoiceX v5.5 (estructura plana con 97 campos)"""

    def __init__(self, output_dir: str = "facturas_json"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # Importar DatasetExporter para usar su método de conversión a InvoiceX v5.5
        from .dataset_exporter import DatasetExporter
        self.dataset_exporter = DatasetExporter()

    def exportar_factura(self, datos: Dict, filename: str = None) -> str:
        """
        Exporta una factura a JSON en formato InvoiceX v5.5 (estructura plana)

        Args:
            datos: Diccionario con todos los datos de la factura (formato interno)
            filename: Nombre del archivo (si None, se genera automático)

        Returns:
            Ruta del archivo generado
        """
        if filename is None:
            fecha_emision = datos.get('fecha_emision')
            if isinstance(fecha_emision, datetime):
                fecha_str = fecha_emision.strftime('%Y%m%d')
            else:
                fecha_str = datetime.now().strftime('%Y%m%d')
            tipo = datos.get('tipo_factura', 'general')
            serie = datos.get('serie', 'F001')
            numero = datos.get('numero', '000001')
            filename = f"Factura_{tipo}_{serie}_{numero}_{fecha_str}.json"

        filepath = os.path.join(self.output_dir, filename)

        # IMPORTANTE: Convertir al formato InvoiceX v5.5 (estructura plana con 97 campos)
        datos_json = self.dataset_exporter.convertir_factura_a_anotacion(datos)

        # Guardar JSON
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(datos_json, f, ensure_ascii=False, indent=2)

        return filepath

    def exportar_multiple(self, facturas: List[Dict], filename: str = "facturas.json") -> str:
        """
        Exporta múltiples facturas a un solo archivo JSON (formato InvoiceX v5.5)

        Args:
            facturas: Lista de facturas (formato interno)
            filename: Nombre del archivo

        Returns:
            Ruta del archivo generado
        """
        filepath = os.path.join(self.output_dir, filename)

        # Convertir todas las facturas a formato InvoiceX v5.5
        facturas_json = [
            self.dataset_exporter.convertir_factura_a_anotacion(f)
            for f in facturas
        ]

        # Crear estructura con metadata
        output = {
            "metadata": {
                "total_facturas": len(facturas_json),
                "fecha_generacion": datetime.now().strftime("%Y-%m-%d"),
                "version": "5.5",
                "formato": "InvoiceX v5.5 - Estructura plana con 97 campos"
            },
            "facturas": facturas_json
        }

        # Guardar JSON
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        return filepath

    def crear_resumen(self, facturas: List[Dict]) -> Dict:
        """
        Crea un resumen estadístico de las facturas

        Args:
            facturas: Lista de facturas (formato interno)

        Returns:
            Diccionario con estadísticas
        """
        if not facturas:
            return {}

        # Contar por tipo
        tipos = {}
        monedas = {}
        total_por_moneda = {}
        con_credito = 0
        con_descuento = 0

        for f in facturas:
            # Tipos
            tipo = f.get('tipo_factura', 'general')
            tipos[tipo] = tipos.get(tipo, 0) + 1

            # Monedas (normalizar)
            moneda_codigo = f.get('moneda', 'PEN')
            if moneda_codigo in ["PEN", "S/", "SOLES"]:
                moneda = "SOLES"
            elif moneda_codigo in ["USD", "$", "DOLARES", "DÓLARES"]:
                moneda = "DOLARES AMERICANOS"
            elif moneda_codigo in ["EUR", "€", "EUROS"]:
                moneda = "EUROS"
            else:
                moneda = moneda_codigo

            monedas[moneda] = monedas.get(moneda, 0) + 1

            # Totales por moneda
            if moneda not in total_por_moneda:
                total_por_moneda[moneda] = 0
            total_por_moneda[moneda] += f.get('total', 0)

            # Créditos
            if f.get('con_credito'):
                con_credito += 1

            # Descuentos
            if f.get('descuento'):
                con_descuento += 1

        resumen = {
            "total_facturas": len(facturas),
            "por_tipo": tipos,
            "por_moneda": monedas,
            "totales_por_moneda": {
                k: round(v, 2) for k, v in total_por_moneda.items()
            },
            "con_credito": con_credito,
            "con_descuento": con_descuento,
            "porcentaje_credito": round(con_credito / len(facturas) * 100, 1) if facturas else 0,
            "porcentaje_descuento": round(con_descuento / len(facturas) * 100, 1) if facturas else 0,
            "formato": "InvoiceX v5.5"
        }

        return resumen


if __name__ == "__main__":
    from generator import FacturaGenerator

    # Test
    gen = FacturaGenerator()
    exporter = JSONExporter(output_dir="test_json")

    print("=" * 70)
    print("GENERANDO FACTURAS EN FORMATO INVOICEX v5.5".center(70))
    print("=" * 70)

    facturas = []
    for i in range(3):
        print(f"\nGenerando factura {i+1}/3...")
        factura = gen.generar_factura()
        archivo = exporter.exportar_factura(factura)
        facturas.append(factura)
        print(f"✓ Exportada: {archivo}")
        print(f"  Formato: InvoiceX v5.5 (estructura plana con 97 campos)")

    # Exportar todas juntas
    archivo_multiple = exporter.exportar_multiple(facturas, "todas_facturas.json")
    print(f"\n✓ Archivo múltiple: {archivo_multiple}")

    # Crear resumen
    resumen = exporter.crear_resumen(facturas)
    print(f"\n=== RESUMEN ===")
    print(json.dumps(resumen, indent=2, ensure_ascii=False))
    print("\n✅ Todas las facturas generadas en formato InvoiceX v5.5")
