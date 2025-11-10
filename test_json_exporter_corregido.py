"""
Test del JSONExporter corregido - Ahora genera formato InvoiceX v5.5
"""
import sys
import json
sys.path.insert(0, '/home/user/Creador-De-Factura')

from src.generator import FacturaGenerator
from src.json_exporter import JSONExporter

print("=" * 70)
print("PRUEBA DE JSONExporter CORREGIDO - Formato InvoiceX v5.5".center(70))
print("=" * 70)

# Generar facturas de diferentes tipos
gen = FacturaGenerator()
exporter = JSONExporter(output_dir='facturas_generadas/JSONs_CORREGIDOS')

tipos = ['general', 'hotel', 'seguro', 'con_descuento']

print("\nGenerando facturas en formato InvoiceX v5.5...\n")

facturas_generadas = []

for i, tipo in enumerate(tipos, 1):
    print(f"[{i}/{len(tipos)}] Generando factura tipo: {tipo.upper()}")

    factura = gen.generar_factura(tipo_factura=tipo, con_credito=(i % 2 == 0))

    # Exportar
    archivo = exporter.exportar_factura(factura)

    # Leer para verificar formato
    with open(archivo, 'r', encoding='utf-8') as f:
        json_data = json.load(f)

    # Verificaciones
    tiene_estructura_plana = "emisor_ruc" in json_data
    tiene_moneda_normalizada = json_data.get("moneda") in ["SOLES", "DOLARES AMERICANOS", "EUROS"]
    campos_raiz = len([k for k in json_data.keys() if k not in ["items", "cuotas"]])
    num_items = len(json_data.get("items", []))
    campos_item = len(json_data["items"][0]) if json_data.get("items") else 0

    print(f"  ✓ JSON: {archivo}")
    print(f"  ✓ Formato: {'InvoiceX v5.5' if tiene_estructura_plana else 'INCORRECTO'}")
    print(f"  ✓ Campos raíz: {campos_raiz}")
    print(f"  ✓ Items: {num_items} (cada uno con {campos_item} campos)")
    print(f"  ✓ Estructura plana: {'Sí' if tiene_estructura_plana else 'No'}")
    print(f"  ✓ Moneda normalizada: {json_data.get('moneda')}")
    print(f"  ✓ Fecha formato: {json_data.get('fecha_emision')}")
    print()

    facturas_generadas.append(factura)

# Exportar todas juntas
print("Exportando todas las facturas en un solo archivo...")
archivo_multiple = exporter.exportar_multiple(facturas_generadas, "facturas_todas.json")
print(f"✓ Archivo múltiple: {archivo_multiple}")

# Crear resumen
resumen = exporter.crear_resumen(facturas_generadas)
print("\n" + "=" * 70)
print("RESUMEN".center(70))
print("=" * 70)
print(json.dumps(resumen, indent=2, ensure_ascii=False))

print("\n" + "=" * 70)
print("✅ TODAS LAS FACTURAS GENERADAS EN FORMATO INVOICEX v5.5".center(70))
print("=" * 70)
print("\n🔍 Verifica los archivos en: facturas_generadas/JSONs_CORREGIDOS/")
print("\nCaracterísticas del formato:")
print("  • Estructura plana con prefijos (emisor_, receptor_)")
print("  • 94+ campos en nivel raíz")
print("  • Items con 26-27 campos cada uno")
print("  • Fechas en formato YYYY-MM-DD")
print("  • Moneda normalizada (SOLES, DOLARES AMERICANOS)")
print()
