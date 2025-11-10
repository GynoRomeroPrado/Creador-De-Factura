#!/usr/bin/env python3
"""Script de test para verificar corrección de superposiciones"""

from src.generator import FacturaGenerator
from src.pdf_creator import PDFFactura
import os

# Crear directorio de salida
os.makedirs("test_correccion_final", exist_ok=True)

# Probar los 3 casos críticos:
tests = [
    {"items": 12, "credito": False, "desc": "1 pagina sin credito"},
    {"items": 75, "credito": True, "desc": "4 paginas con credito"},
    {"items": 95, "credito": True, "desc": "5 paginas con credito"}
]

gen = FacturaGenerator()
pdf_gen = PDFFactura(output_dir="test_correccion_final")

print("=" * 80)
print("PRUEBA DE CORRECCIÓN DE SUPERPOSICIONES".center(80))
print("=" * 80)

for i, test in enumerate(tests, 1):
    print(f"\n{i}. Generando: {test['desc']}...")
    print(f"   Items: {test['items']}, Crédito: {test['credito']}")

    factura = gen.generar_factura(
        tipo_factura='con_descuento',
        num_items=test["items"],
        con_credito=test["credito"]
    )

    pdf_path = pdf_gen.crear_factura(factura)
    print(f"   ✓ PDF generado: {pdf_path}")

print("\n" + "=" * 80)
print("✅ LOS 3 PDFs HAN SIDO GENERADOS")
print("=" * 80)

print("\n🔍 VERIFICACIÓN MANUAL REQUERIDA:")
print("   Abre cada PDF y verifica que NO hay superposiciones:")
print("   1. Items NO se superponen con DESCUENTOS")
print("   2. DESCUENTOS NO se superponen con TOTALES")
print("   3. TOTALES NO se superponen con FORMA DE PAGO")
print("   4. FORMA DE PAGO NO se superpone con DATOS DE CUOTA")
print("   5. DATOS DE CUOTA NO se superpone con OBSERVACIONES")

print("\n📁 Archivos en: test_correccion_final/")
print("=" * 80)
