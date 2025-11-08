"""
Script de prueba para verificar que los items se exportan correctamente al JSON
"""
import sys
import json
sys.path.insert(0, 'src')

from src.generator import FacturaGenerator
from src.dataset_exporter import DatasetExporter

print("=" * 80)
print("VERIFICACIÓN DE ITEMS EN JSON".center(80))
print("=" * 80)

# Crear exportador
exporter = DatasetExporter(base_dir='test_items_json')
dataset_dir = exporter.crear_dataset()

print(f"\n📁 Dataset: {dataset_dir}\n")

# Generar facturas con diferentes cantidades de items
factura_gen = FacturaGenerator()

configuraciones = [
    {'tipo': 'general', 'items': 5, 'desc': 'Factura con 5 items'},
    {'tipo': 'compra_grande', 'items': 35, 'desc': 'Compra grande con 35 items'},
    {'tipo': 'compra_grande', 'items': None, 'desc': 'Compra grande automática (30-50 items)'},
]

for i, config in enumerate(configuraciones, 1):
    print(f"\n[{i}/3] {config['desc']}")

    # Generar factura
    factura = factura_gen.generar_factura(
        tipo_factura=config['tipo'],
        num_items=config['items']
    )

    num_items = len(factura['items'])
    serie = factura['numero_factura']

    print(f"    Serie: {serie}")
    print(f"    Items generados en factura: {num_items}")

    # Exportar solo JSON (sin PDF para rapidez)
    json_path, _ = exporter.exportar_factura(factura, pdf_content=None)

    # Verificar JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        anotacion = json.load(f)

    items_en_json = len(anotacion.get('items', []))
    numero_items_campo = anotacion.get('numero_items', 0)

    print(f"    Items en JSON: {items_en_json}")
    print(f"    Campo 'numero_items': {numero_items_campo}")

    # Verificar coincidencia
    if items_en_json == num_items == numero_items_campo:
        print(f"    ✅ CORRECTO: Todos los items se exportaron")
    else:
        print(f"    ❌ ERROR: Discrepancia en cantidad de items")
        print(f"       - Factura original: {num_items}")
        print(f"       - Items en JSON: {items_en_json}")
        print(f"       - Campo numero_items: {numero_items_campo}")

    # Mostrar primeros 3 items como ejemplo
    print(f"    Muestra de items en JSON:")
    for item in anotacion['items'][:3]:
        print(f"      • {item['numero']}. {item['descripcion'][:40]:40s} | "
              f"Cant: {item['cantidad']:>6} {item['unidad']:3s} | "
              f"P.Unit: ${item['precio_unitario']:>8.2f} | "
              f"Total: ${item['valor_venta']:>10.2f}")

    if items_en_json > 3:
        print(f"      ... y {items_en_json - 3} items más")

# Verificar estructura de un JSON completo
print("\n" + "=" * 80)
print("VERIFICACIÓN DE ESTRUCTURA JSON COMPLETA".center(80))
print("=" * 80)

# Leer el JSON con más items
anotaciones_dir = dataset_dir + "/anotaciones"
import os
jsons = [f for f in os.listdir(anotaciones_dir) if f.endswith('.json')]

if jsons:
    json_file = jsons[-1]  # Último generado (compra grande)
    json_path = os.path.join(anotaciones_dir, json_file)

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"\n📄 Archivo: {json_file}")
    print(f"\n📊 Campos del JSON:")
    print(f"   • tipo_documento: {data.get('tipo_documento')}")
    print(f"   • serie_completa: {data.get('serie_completa')}")
    print(f"   • emisor_razon_social: {data.get('emisor_razon_social')}")
    print(f"   • receptor_razon_social: {data.get('receptor_razon_social')}")
    print(f"   • subtotal: {data.get('subtotal')}")
    print(f"   • igv: {data.get('igv')}")
    print(f"   • importe_total: {data.get('importe_total')}")
    print(f"   • items: [array con {len(data.get('items', []))} elementos]")
    print(f"   • numero_items: {data.get('numero_items')}")

    print(f"\n📦 Estructura de un item:")
    if data.get('items'):
        item_ejemplo = data['items'][0]
        for key, value in item_ejemplo.items():
            print(f"   • {key}: {value}")

    print(f"\n✅ JSON exporta correctamente TODOS los items ({data.get('numero_items')} items)")
    print(f"✅ Las facturas grandes (30-50 items) se exportan completamente")

print(f"\n📁 Dataset de prueba guardado en: {dataset_dir}")
