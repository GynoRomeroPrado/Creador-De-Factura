"""
Exportador de facturas a JSON
"""
import json
import os
from datetime import datetime
from typing import Dict, List


class JSONExporter:
    """Exporta facturas a formato JSON"""

    def __init__(self, output_dir: str = "facturas_json"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def exportar_factura(self, datos: Dict, filename: str = None) -> str:
        """
        Exporta una factura a JSON

        Args:
            datos: Diccionario con todos los datos de la factura
            filename: Nombre del archivo (si None, se genera automático)

        Returns:
            Ruta del archivo generado
        """
        if filename is None:
            fecha_str = datos['fecha_emision'].strftime('%Y%m%d')
            tipo = datos.get('tipo_factura', 'general')
            filename = f"Factura_{tipo}_{datos['serie']}_{datos['numero']}_{fecha_str}.json"

        filepath = os.path.join(self.output_dir, filename)

        # Convertir fechas a strings para JSON
        datos_json = self._preparar_para_json(datos)

        # Guardar JSON
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(datos_json, f, ensure_ascii=False, indent=2)

        return filepath

    def exportar_multiple(self, facturas: List[Dict], filename: str = "facturas.json") -> str:
        """
        Exporta múltiples facturas a un solo archivo JSON

        Args:
            facturas: Lista de facturas
            filename: Nombre del archivo

        Returns:
            Ruta del archivo generado
        """
        filepath = os.path.join(self.output_dir, filename)

        # Preparar todas las facturas
        facturas_json = [self._preparar_para_json(f) for f in facturas]

        # Crear estructura con metadata
        output = {
            "metadata": {
                "total_facturas": len(facturas_json),
                "fecha_generacion": datetime.now().isoformat(),
                "version": "1.0"
            },
            "facturas": facturas_json
        }

        # Guardar JSON
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output, f, ensure_ascii=False, indent=2)

        return filepath

    def _preparar_para_json(self, datos: Dict) -> Dict:
        """
        Prepara los datos para serialización JSON convirtiendo objetos datetime

        Args:
            datos: Diccionario con datos de factura

        Returns:
            Diccionario serializable a JSON
        """
        datos_copia = {}

        for key, value in datos.items():
            if isinstance(value, datetime):
                # Convertir datetime a string ISO
                datos_copia[key] = value.isoformat()
            elif isinstance(value, dict):
                # Recursivo para diccionarios anidados
                datos_copia[key] = self._preparar_dict(value)
            elif isinstance(value, list):
                # Procesar listas
                datos_copia[key] = [
                    self._preparar_dict(item) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                datos_copia[key] = value

        return datos_copia

    def _preparar_dict(self, d: Dict) -> Dict:
        """Prepara un diccionario anidado para JSON"""
        resultado = {}
        for key, value in d.items():
            if isinstance(value, datetime):
                resultado[key] = value.isoformat()
            elif isinstance(value, dict):
                resultado[key] = self._preparar_dict(value)
            elif isinstance(value, list):
                resultado[key] = [
                    self._preparar_dict(item) if isinstance(item, dict) else item
                    for item in value
                ]
            else:
                resultado[key] = value
        return resultado

    def crear_resumen(self, facturas: List[Dict]) -> Dict:
        """
        Crea un resumen estadístico de las facturas

        Args:
            facturas: Lista de facturas

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

            # Monedas
            moneda = f['moneda']
            monedas[moneda] = monedas.get(moneda, 0) + 1

            # Totales por moneda
            if moneda not in total_por_moneda:
                total_por_moneda[moneda] = 0
            total_por_moneda[moneda] += f['total']

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
            "porcentaje_credito": round(con_credito / len(facturas) * 100, 1),
            "porcentaje_descuento": round(con_descuento / len(facturas) * 100, 1)
        }

        return resumen


if __name__ == "__main__":
    from generator import FacturaGenerator

    # Test
    gen = FacturaGenerator()
    exporter = JSONExporter(output_dir="test_json")

    print("Generando y exportando facturas a JSON...")

    facturas = []
    for i in range(5):
        factura = gen.generar_factura()
        archivo = exporter.exportar_factura(factura)
        facturas.append(factura)
        print(f"✓ Exportada: {archivo}")

    # Exportar todas juntas
    archivo_multiple = exporter.exportar_multiple(facturas, "todas_facturas.json")
    print(f"\n✓ Archivo múltiple: {archivo_multiple}")

    # Crear resumen
    resumen = exporter.crear_resumen(facturas)
    print(f"\n=== RESUMEN ===")
    print(json.dumps(resumen, indent=2, ensure_ascii=False))
