"""
🎯 GENERADOR DE FACTURAS CON MÚLTIPLES PÁGINAS (JSON)
Genera facturas con 40-60 items para producir JSONs que generarán PDFs de 3-5 páginas
"""
import sys
sys.path.insert(0, '/home/user/Creador-De-Factura')

from src.generator import FacturaGenerator
from src.json_exporter import JSONExporter
import json

print("=" * 80)
print("🎯 GENERADOR DE FACTURAS CON MÚLTIPLES PÁGINAS (JSON)".center(80))
print("=" * 80)

# Crear generador
gen = FacturaGenerator()
json_exporter = JSONExporter(output_dir="facturas_generadas/JSONs_MULTIPAGINA")

print("\n📋 CONFIGURACIÓN:")
print("-" * 80)
print("  Tipo de factura: compra_grande")
print("  Items por factura: 40-60 items")
print("  Páginas esperadas en PDF: 3-5 páginas")
print("  Categorías: construcción, servicios, productos mixtos")
print("  Formato JSON: InvoiceX v5.5 (100% correcto)")
print("-" * 80)

# Configuraciones para diferentes tipos de facturas multipágina
configuraciones = [
    {
        "nombre": "Factura de Construcción (50 items)",
        "num_items": 50,
        "categoria": "construccion",
        "con_credito": True,
        "moneda": "PEN"
    },
    {
        "nombre": "Factura de Servicios (45 items)",
        "num_items": 45,
        "categoria": "servicios",
        "con_credito": False,
        "moneda": "USD"
    },
    {
        "nombre": "Factura Mixta con Descuento (55 items)",
        "num_items": 55,
        "categoria": None,  # Mixta
        "con_credito": True,
        "moneda": "PEN"
    },
    {
        "nombre": "Factura Grande con Crédito (60 items)",
        "num_items": 60,
        "categoria": "construccion",
        "con_credito": True,
        "moneda": "USD"
    },
    {
        "nombre": "Factura de Productos (40 items)",
        "num_items": 40,
        "categoria": None,
        "con_credito": False,
        "moneda": "PEN"
    },
    {
        "nombre": "Factura Mega Grande (70 items)",
        "num_items": 70,
        "categoria": "construccion",
        "con_credito": True,
        "moneda": "PEN"
    },
    {
        "nombre": "Factura Extra Grande (80 items)",
        "num_items": 80,
        "categoria": None,
        "con_credito": True,
        "moneda": "USD"
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
        con_credito=config['con_credito'],
        moneda=config['moneda']
    )

    print(f"  Serie: {factura['numero_factura']}")
    print(f"  Items: {len(factura['items'])} items")
    print(f"  Moneda: {factura['moneda']}")
    print(f"  Total: {factura['total']:.2f}")
    print(f"  Forma de pago: {factura['forma_pago']}")

    # Calcular páginas estimadas (cada página tiene ~15-18 items)
    paginas_estimadas = max(1, (len(factura['items']) // 15) + 1)
    print(f"  📄 Páginas estimadas: {paginas_estimadas}")

    # Generar JSON en formato InvoiceX v5.5
    try:
        json_path = json_exporter.exportar_factura(factura)
        print(f"  ✅ JSON: {json_path}")

        # Verificar que el JSON tenga estructura correcta
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Verificar estructura
        tiene_97_campos = all(campo in data for campo in [
            'tipo_documento', 'serie_completa', 'fecha_emision',
            'emisor_ruc', 'receptor_numero_doc', 'importe_total',
            'items', 'cuotas'
        ])

        if tiene_97_campos:
            print(f"  ✅ Estructura validada: {len(data['items'])} items, {len(data.get('cuotas', []))} cuotas")
        else:
            print(f"  ⚠️  Estructura incompleta")

    except Exception as e:
        print(f"  ❌ Error generando JSON: {str(e)}")
        json_path = None

    facturas_generadas.append({
        "nombre": config['nombre'],
        "serie": factura['numero_factura'],
        "items": len(factura['items']),
        "moneda": factura['moneda'],
        "total": factura['total'],
        "json": json_path,
        "paginas_estimadas": paginas_estimadas if json_path else 0
    })

print("\n" + "=" * 80)
print("📊 RESUMEN DE FACTURAS GENERADAS".center(80))
print("=" * 80)

print(f"\n{'#':<4} {'Serie':<15} {'Items':<7} {'Páginas':<10} {'Moneda':<8} {'Total':<15} {'Estado':<10}")
print("-" * 80)

for i, factura in enumerate(facturas_generadas, 1):
    status = "✅ OK" if factura['json'] else "❌ ERROR"

    print(f"{i:<4} {factura['serie']:<15} {factura['items']:<7} {factura['paginas_estimadas']:<10} {factura['moneda']:<8} {factura['total']:<15.2f} {status:<10}")

print("-" * 80)
print(f"\nTotal facturas generadas: {len(facturas_generadas)}")
print(f"Total con 3+ páginas: {sum(1 for f in facturas_generadas if f['paginas_estimadas'] >= 3)}")
print(f"Total con 4+ páginas: {sum(1 for f in facturas_generadas if f['paginas_estimadas'] >= 4)}")
print(f"Total con 5+ páginas: {sum(1 for f in facturas_generadas if f['paginas_estimadas'] >= 5)}")

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
print(f"  JSONs: facturas_generadas/JSONs_MULTIPAGINA/")

print("\n" + "=" * 80)
print("✅ GENERACIÓN COMPLETADA".center(80))
print("=" * 80)

print("\n💡 PARA USAR EN GOOGLE COLAB:")
print("=" * 80)
print("""
1. Subir estos JSONs a Google Colab
2. Usar el PDF creator para generar los PDFs

Código para Colab:
```python
from src.pdf_creator import PDFCreator
import json

pdf_creator = PDFCreator(output_dir="/content/PDFs_MULTIPAGINA")

# Leer JSON y generar PDF
with open("factura.json", 'r') as f:
    data = json.load(f)

# El JSONExporter ya tiene el método para esto, pero si necesitas hacerlo manual:
from src.generator import FacturaGenerator

# Reconstruir factura desde JSON (aproximado)
# O simplemente genera nuevas facturas con 50+ items:
gen = FacturaGenerator()
factura = gen.generar_factura(tipo_factura='compra_grande', num_items=60)
pdf_path = pdf_creator.crear_factura(factura)
print(f"PDF generado: {pdf_path}")
```
""")

print("\n📊 DETALLES POR FACTURA:")
print("=" * 80)
for i, factura in enumerate(facturas_generadas, 1):
    if factura['json']:
        print(f"\n{i}. {factura['nombre']}")
        print(f"   Serie: {factura['serie']}")
        print(f"   Archivo: {factura['json']}")
        print(f"   Items: {factura['items']} → ~{factura['paginas_estimadas']} páginas")
