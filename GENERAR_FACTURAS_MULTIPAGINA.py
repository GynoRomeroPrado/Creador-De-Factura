"""
🎯 GENERADOR DE FACTURAS CON MÚLTIPLES PÁGINAS
Genera facturas con 40-60 items para producir PDFs de 3-5 páginas
"""
import sys
sys.path.insert(0, '/home/user/Creador-De-Factura')

from src.generator import FacturaGenerator
from src.pdf_creator import PDFCreator
from src.json_exporter import JSONExporter
import os

print("=" * 80)
print("🎯 GENERADOR DE FACTURAS CON MÚLTIPLES PÁGINAS".center(80))
print("=" * 80)

# Crear generador
gen = FacturaGenerator()
pdf_creator = PDFCreator(output_dir="facturas_generadas/PDFs_MULTIPAGINA")
json_exporter = JSONExporter(output_dir="facturas_generadas/JSONs_MULTIPAGINA")

print("\n📋 CONFIGURACIÓN:")
print("-" * 80)
print("  Tipo de factura: compra_grande")
print("  Items por factura: 40-60 items")
print("  Páginas esperadas: 3-5 páginas")
print("  Categorías: construcción, servicios, productos mixtos")
print("-" * 80)

# Configuraciones para diferentes tipos de facturas multipágina
configuraciones = [
    {
        "nombre": "Factura de Construcción (50 items)",
        "num_items": 50,
        "categoria": "construccion",
        "con_credito": True
    },
    {
        "nombre": "Factura de Servicios (45 items)",
        "num_items": 45,
        "categoria": "servicios",
        "con_credito": False
    },
    {
        "nombre": "Factura Mixta con Descuento (55 items)",
        "num_items": 55,
        "categoria": None,  # Mixta
        "con_credito": True
    },
    {
        "nombre": "Factura Grande con Crédito (60 items)",
        "num_items": 60,
        "categoria": "construccion",
        "con_credito": True
    },
    {
        "nombre": "Factura de Productos (40 items)",
        "num_items": 40,
        "categoria": None,
        "con_credito": False
    }
]

facturas_generadas = []

print("\n🔄 GENERANDO FACTURAS...")
print("=" * 80)

for i, config in enumerate(configuraciones, 1):
    print(f"\n[{i}/{len(configuraciones)}] {config['nombre']}")
    print("-" * 80)

    # Generar factura con tipo_factura='compra_grande' y número específico de items
    factura = gen.generar_factura(
        tipo_factura='compra_grande',
        num_items=config['num_items'],
        categoria_items=config['categoria'],
        con_credito=config['con_credito']
    )

    print(f"  Serie: {factura['numero_factura']}")
    print(f"  Items: {len(factura['items'])} items")
    print(f"  Total: {factura['moneda']} {factura['total']:.2f}")
    print(f"  Forma de pago: {factura['forma_pago']}")

    # Generar PDF
    try:
        pdf_path = pdf_creator.crear_factura(factura)
        print(f"  ✅ PDF: {pdf_path}")

        # Contar páginas del PDF (aproximado)
        # Cada página puede tener ~15-18 items
        paginas_estimadas = max(1, (len(factura['items']) // 15) + 1)
        print(f"  📄 Páginas estimadas: {paginas_estimadas}")

    except Exception as e:
        print(f"  ❌ Error generando PDF: {str(e)}")
        pdf_path = None

    # Generar JSON en formato InvoiceX v5.5
    try:
        json_path = json_exporter.exportar_factura(factura)
        print(f"  ✅ JSON: {json_path}")
    except Exception as e:
        print(f"  ❌ Error generando JSON: {str(e)}")
        json_path = None

    facturas_generadas.append({
        "nombre": config['nombre'],
        "serie": factura['numero_factura'],
        "items": len(factura['items']),
        "total": factura['total'],
        "pdf": pdf_path,
        "json": json_path,
        "paginas_estimadas": paginas_estimadas if pdf_path else 0
    })

print("\n" + "=" * 80)
print("📊 RESUMEN DE FACTURAS GENERADAS".center(80))
print("=" * 80)

print(f"\n{'#':<4} {'Serie':<15} {'Items':<7} {'Páginas':<10} {'Total':<15} {'Archivos':<20}")
print("-" * 80)

for i, factura in enumerate(facturas_generadas, 1):
    pdf_status = "✅ PDF" if factura['pdf'] else "❌ PDF"
    json_status = "✅ JSON" if factura['json'] else "❌ JSON"
    archivos = f"{pdf_status} {json_status}"

    print(f"{i:<4} {factura['serie']:<15} {factura['items']:<7} {factura['paginas_estimadas']:<10} {factura['total']:<15.2f} {archivos:<20}")

print("-" * 80)
print(f"\nTotal facturas generadas: {len(facturas_generadas)}")
print(f"Total con 3+ páginas: {sum(1 for f in facturas_generadas if f['paginas_estimadas'] >= 3)}")

# Estadísticas
total_items = sum(f['items'] for f in facturas_generadas)
total_paginas = sum(f['paginas_estimadas'] for f in facturas_generadas)
promedio_items = total_items / len(facturas_generadas) if facturas_generadas else 0
promedio_paginas = total_paginas / len(facturas_generadas) if facturas_generadas else 0

print(f"\n📈 ESTADÍSTICAS:")
print(f"  Total items: {total_items}")
print(f"  Promedio items/factura: {promedio_items:.1f}")
print(f"  Total páginas estimadas: {total_paginas}")
print(f"  Promedio páginas/factura: {promedio_paginas:.1f}")

print("\n📁 UBICACIÓN DE ARCHIVOS:")
print("-" * 80)
print(f"  PDFs: facturas_generadas/PDFs_MULTIPAGINA/")
print(f"  JSONs: facturas_generadas/JSONs_MULTIPAGINA/")

print("\n" + "=" * 80)
print("✅ GENERACIÓN COMPLETADA".center(80))
print("=" * 80)

print("\n💡 TIPS:")
print("  - Cada PDF tiene aproximadamente 15-18 items por página")
print("  - Facturas con 40 items = ~3 páginas")
print("  - Facturas con 50 items = ~4 páginas")
print("  - Facturas con 60 items = ~5 páginas")
print("  - Revisa los PDFs en: facturas_generadas/PDFs_MULTIPAGINA/")
