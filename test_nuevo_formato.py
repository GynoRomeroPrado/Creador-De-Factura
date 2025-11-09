"""
Script para generar facturas de prueba con los nuevos formatos
"""
import sys
sys.path.insert(0, 'src')

from src.generator import FacturaGenerator
from src.dataset_exporter import DatasetExporter
import json

print("="*80)
print("GENERANDO FACTURAS DE PRUEBA - NUEVO FORMATO".center(80))
print("="*80)

# Crear exportador
exporter = DatasetExporter(base_dir='test_nuevo_formato')
dataset_dir = exporter.crear_dataset()

factura_gen = FacturaGenerator()

# Generar 1 factura de hotel
print("\n1. FACTURA DE HOTEL")
print("-" * 80)
factura_hotel = factura_gen.generar_factura(tipo_factura='hotel', num_items=3)

print(f"Serie: {factura_hotel['numero_factura']}")
print(f"Emisor: {factura_hotel['emisor']['razon_social']}")
print(f"\nItems:")
for item in factura_hotel['items']:
    print(f"  {item['numero']}. {item['descripcion']}")
    print(f"     Cantidad: {item['cantidad']} {item['unidad']}")
    print(f"     P.Unit: ${item['precio_unitario']:.2f}")
    print(f"     Valor: ${item['valor_venta']:.2f}")
    if 'cargo_item' in item:
        print(f"     + Cargo al item: ${item['cargo_item']:.2f}")

print(f"\nDatos de Hotel:")
hotel = factura_hotel['datos_hotel']
print(f"  CheckIn: {hotel['checkin'].strftime('%d-%m-%Y')}")
print(f"  CheckOut: {hotel['checkout'].strftime('%d-%m-%Y')}")
print(f"  Noches: {hotel['noches']}")
print(f"  Reserva: {hotel['reserva']}")
print(f"  Huésped: {hotel['huesped']}")
print(f"  Habitación: {hotel.get('habitacion', 'N/A')}")
if hotel.get('codigo_grupo'):
    print(f"  Grupo: {hotel['codigo_grupo']} - {hotel['nombre_grupo']}")

# Exportar JSON
json_path, _ = exporter.exportar_factura(factura_hotel, pdf_content=None)
print(f"\n✅ JSON exportado: {json_path}")

# Verificar JSON
with open(json_path, 'r', encoding='utf-8') as f:
    anotacion_hotel = json.load(f)

print(f"✅ Items en JSON: {len(anotacion_hotel.get('items', []))}")
print(f"✅ Tiene 'numero_items': {anotacion_hotel.get('numero_items')}")

# Generar 1 factura general
print("\n\n2. FACTURA GENERAL")
print("-" * 80)
factura_general = factura_gen.generar_factura(tipo_factura='general', num_items=5)

print(f"Serie: {factura_general['numero_factura']}")
print(f"Emisor: {factura_general['emisor']['razon_social']}")
print(f"\nItems:")
for item in factura_general['items'][:3]:
    print(f"  {item['numero']}. {item['descripcion'][:50]}")
    print(f"     Cantidad: {item['cantidad']} {item['unidad']}")
    print(f"     Valor: ${item['valor_venta']:.2f}")
print(f"  ... y {len(factura_general['items']) - 3} items más")

# Exportar JSON
json_path, _ = exporter.exportar_factura(factura_general, pdf_content=None)
print(f"\n✅ JSON exportado: {json_path}")

print("\n" + "="*80)
print("RESUMEN".center(80))
print("="*80)
print(f"\n✅ Facturas generadas: 2")
print(f"✅ Dataset: {dataset_dir}")
print(f"\n📋 Diferencias clave:")
print(f"  • Items de hotel: ALIMENTACION, ALOJAMIENTO (simplificados)")
print(f"  • Items generales: Productos específicos variados")
print(f"  • Hotel tiene: cargo_item, datos_hotel completos con habitación")
print(f"  • General: Sin cargo_item, datos_hotel = null")
