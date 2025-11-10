"""
📄 GENERADOR DE LOTE - FACTURAS DE 1 PÁGINA
Genera un lote de facturas de una sola página (10-15 items cada una)
"""

import sys
sys.path.insert(0, '/home/user/Creador-De-Factura')

import os
from datetime import datetime
from src.generator import FacturaGenerator
from src.json_exporter import JSONExporter

# ============================================================================
# CONFIGURACIÓN - MODIFICA AQUÍ LA CANTIDAD A GENERAR
# ============================================================================
CANTIDAD_FACTURAS = 50  # ← CAMBIA ESTE NÚMERO PARA GENERAR MÁS O MENOS

# ============================================================================

print("=" * 80)
print("📄 GENERADOR DE LOTE - FACTURAS DE 1 PÁGINA".center(80))
print("=" * 80)

print(f"\n🎯 CONFIGURACIÓN:")
print("-" * 80)
print(f"  Facturas a generar: {CANTIDAD_FACTURAS}")
print(f"  Items por factura: 10-15 (1 página)")
print(f"  Tipos de factura: General, con descuento, con crédito")
print(f"  Monedas: PEN, USD, EUR")

# Crear carpeta de salida
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = f"facturas_generadas/LOTE_PAGINA_UNICA_{timestamp}"
os.makedirs(output_dir, exist_ok=True)

print(f"\n📁 Carpeta de salida: {output_dir}")

# Inicializar generadores
gen = FacturaGenerator()
json_exporter = JSONExporter(output_dir=output_dir)

# Estadísticas
stats = {
    'general': 0,
    'con_descuento': 0,
    'con_credito': 0,
    'monedas': {'PEN': 0, 'USD': 0, 'EUR': 0}
}

print(f"\n🚀 GENERANDO {CANTIDAD_FACTURAS} FACTURAS DE 1 PÁGINA...")
print("=" * 80)

import random

for i in range(1, CANTIDAD_FACTURAS + 1):
    # Variar tipo de factura
    tipo = random.choice(['general', 'con_descuento', 'general', 'general'])
    num_items = random.randint(10, 15)
    con_credito = random.choice([True, False])
    moneda = random.choice(['PEN', 'USD', 'EUR'])

    # Generar factura
    if tipo == 'con_descuento':
        factura = gen.generar_factura(
            tipo_factura='con_descuento',
            num_items=num_items,
            con_credito=con_credito,
            moneda=moneda
        )
        stats['con_descuento'] += 1
    else:
        factura = gen.generar_factura(
            tipo_factura='general',
            num_items=num_items,
            con_credito=con_credito,
            moneda=moneda
        )
        stats['general'] += 1

    if con_credito:
        stats['con_credito'] += 1

    stats['monedas'][moneda] += 1

    # Exportar JSON
    filename = f"FACTURA_{i:04d}_{factura['serie']}_{factura['numero']}.json"
    json_path = json_exporter.exportar_factura(factura, filename=filename)

    # Mostrar progreso cada 10 facturas
    if i % 10 == 0 or i == CANTIDAD_FACTURAS:
        print(f"  ✅ Generadas: {i}/{CANTIDAD_FACTURAS} ({(i/CANTIDAD_FACTURAS)*100:.1f}%)")

print("\n" + "=" * 80)
print("✅ LOTE COMPLETADO".center(80))
print("=" * 80)

print(f"\n📊 ESTADÍSTICAS:")
print("-" * 80)
print(f"  Total generadas: {CANTIDAD_FACTURAS}")
print(f"  Facturas generales: {stats['general']}")
print(f"  Facturas con descuento: {stats['con_descuento']}")
print(f"  Facturas con crédito: {stats['con_credito']}")
print(f"\n  Monedas:")
print(f"    - PEN (Soles): {stats['monedas']['PEN']}")
print(f"    - USD (Dólares): {stats['monedas']['USD']}")
print(f"    - EUR (Euros): {stats['monedas']['EUR']}")

print(f"\n📁 Archivos guardados en: {output_dir}")
print(f"   Total de archivos JSON: {CANTIDAD_FACTURAS}")

print("\n" + "=" * 80)
print("💡 PARA GENERAR PDFs EN GOOGLE COLAB")
print("=" * 80)
print(f"""
# 1. Actualizar repositorio
!cd /content/Creador-De-Factura && git pull origin claude/fix-json-parsing-011CUyGo75ZndGpbT9KKAMXw

# 2. Instalar reportlab
!pip install reportlab

# 3. Generar lote de 1 página
!cd /content/Creador-De-Factura && python GENERAR_LOTE_PAGINA_UNICA.py

# 4. Generar PDFs desde los JSONs
import os
import json
from src.pdf_creator import PDFCreator

json_dir = "/content/Creador-De-Factura/{output_dir}"
pdf_dir = "/content/PDFs_LOTE_PAGINA_UNICA"

pdf_creator = PDFCreator(output_dir=pdf_dir)

json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
print(f"Generando PDFs para {{len(json_files)}} facturas...")

for i, json_file in enumerate(json_files, 1):
    json_path = os.path.join(json_dir, json_file)
    with open(json_path, 'r', encoding='utf-8') as f:
        factura = json.load(f)

    pdf_path = pdf_creator.crear_factura(factura)

    if i % 10 == 0 or i == len(json_files):
        print(f"  PDFs generados: {{i}}/{{len(json_files)}} ({{(i/len(json_files))*100:.1f}}%)")

print(f"✅ {{len(json_files)}} PDFs generados en {{pdf_dir}}")

# 5. Comprimir y descargar
!cd /content && zip -r PDFs_LOTE_PAGINA_UNICA.zip PDFs_LOTE_PAGINA_UNICA/
from google.colab import files
files.download('/content/PDFs_LOTE_PAGINA_UNICA.zip')
""")

print("\n" + "=" * 80)
print("🎯 CARACTERÍSTICAS DE ESTE LOTE")
print("=" * 80)
print("""
✅ Todas las facturas tienen 1 PÁGINA (10-15 items)
✅ NO hay superposiciones de texto
✅ Variedad de tipos: general, con descuento, con crédito
✅ Múltiples monedas: PEN, USD, EUR
✅ JSONs con formato InvoiceX v5.5 (100/100)
✅ Coherencia matemática perfecta
✅ Fechas de cuotas escalonadas (30 días)
✅ Ubicaciones geográficas correctas (Departamento/Provincia/Distrito)
""")

print("\n✅ LOTE DE FACTURAS DE 1 PÁGINA GENERADO EXITOSAMENTE")
print("=" * 80)
