#!/usr/bin/env python3
"""Script de prueba para verificar descripciones multilínea en items"""

from src.generator import FacturaGenerator
from src.pdf_creator import PDFFactura
import os

# Crear directorio de salida
os.makedirs("test_descripciones_multilinea", exist_ok=True)

print("=" * 80)
print("PRUEBA DE DESCRIPCIONES MULTILÍNEA EN ITEMS".center(80))
print("=" * 80)

# Generar factura con items variados
gen = FacturaGenerator()

# Generar factura normal (descripciones pueden ser cortas o largas)
print("\n1. Generando factura con descripciones normales...")
factura1 = gen.generar_factura(
    tipo_factura='general',
    num_items=15,
    con_credito=False,
    categoria_items='tecnologia'  # Suele tener descripciones largas
)

pdf_gen = PDFFactura(output_dir="test_descripciones_multilinea")
pdf1 = pdf_gen.crear_factura(factura1)
print(f"   ✓ PDF generado: {pdf1}")

# Generar factura multipágina
print("\n2. Generando factura multipágina con descripciones largas...")
factura2 = gen.generar_factura(
    tipo_factura='general',
    num_items=50,
    con_credito=True,
    categoria_items='tecnologia'
)

pdf2 = pdf_gen.crear_factura(factura2)
print(f"   ✓ PDF generado: {pdf2}")

# Generar factura con descuento
print("\n3. Generando factura con descuento...")
factura3 = gen.generar_factura(
    tipo_factura='con_descuento',
    num_items=20,
    con_credito=False,
    categoria_items='construccion'  # Descripciones técnicas largas
)

pdf3 = pdf_gen.crear_factura(factura3)
print(f"   ✓ PDF generado: {pdf3}")

print("\n" + "=" * 80)
print("✅ 3 PDFs GENERADOS")
print("=" * 80)

print("\n🔍 VERIFICACIÓN:")
print("   Abre los PDFs y verifica que:")
print("   1. Las descripciones largas se muestran en MÚLTIPLES LÍNEAS")
print("   2. NO hay texto cortado con '...'")
print("   3. Las líneas de descripción están bien alineadas")
print("   4. El espaciado entre items es correcto")
print("   5. Los precios y totales están alineados correctamente")

print("\n📁 Archivos en: test_descripciones_multilinea/")

# Mostrar algunas descripciones de ejemplo
print("\n📄 Ejemplos de descripciones en factura 1:")
for i, item in enumerate(factura1['items'][:5]):
    desc = item['descripcion']
    print(f"   Item {i+1}: {desc[:60]}{'...' if len(desc) > 60 else ''}")

print("\n" + "=" * 80)
