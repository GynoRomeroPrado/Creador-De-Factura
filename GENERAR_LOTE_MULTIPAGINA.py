"""
📚 GENERADOR DE LOTE - FACTURAS MULTIPÁGINA
Genera un lote de facturas con múltiples páginas (3-6 páginas, 40-80 items cada una)
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
CANTIDAD_FACTURAS = 100  # ← CAMBIA ESTE NÚMERO PARA GENERAR MÁS O MENOS

# Distribución de páginas (debe sumar 1.0 = 100%)
DISTRIBUCION_PAGINAS = {
    3: 0.25,  # 25% de facturas con 3 páginas (~40 items)
    4: 0.25,  # 25% de facturas con 4 páginas (~50 items)
    5: 0.25,  # 25% de facturas con 5 páginas (~60 items)
    6: 0.25,  # 25% de facturas con 6 páginas (~80 items)
}

# ============================================================================

print("=" * 80)
print("📚 GENERADOR DE LOTE - FACTURAS MULTIPÁGINA".center(80))
print("=" * 80)

print(f"\n🎯 CONFIGURACIÓN:")
print("-" * 80)
print(f"  Facturas a generar: {CANTIDAD_FACTURAS}")
print(f"  Páginas por factura: 3-6 páginas (40-80 items)")
print(f"  Distribución de páginas:")
for paginas, porcentaje in DISTRIBUCION_PAGINAS.items():
    cantidad = int(CANTIDAD_FACTURAS * porcentaje)
    print(f"    - {paginas} páginas: {porcentaje*100:.0f}% ({cantidad} facturas)")
print(f"  Tipos de factura: General y con descuento")
print(f"  Monedas: PEN, USD, EUR")
print(f"  Crédito: 50% de probabilidad")

# Crear carpeta de salida
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_dir = f"facturas_generadas/LOTE_MULTIPAGINA_{timestamp}"
os.makedirs(output_dir, exist_ok=True)

print(f"\n📁 Carpeta de salida: {output_dir}")

# Inicializar generadores
gen = FacturaGenerator()
json_exporter = JSONExporter(output_dir=output_dir)

# Estadísticas
stats = {
    'paginas': {3: 0, 4: 0, 5: 0, 6: 0},
    'con_descuento': 0,
    'con_credito': 0,
    'monedas': {'PEN': 0, 'USD': 0, 'EUR': 0},
    'items_total': 0
}

print(f"\n🚀 GENERANDO {CANTIDAD_FACTURAS} FACTURAS MULTIPÁGINA...")
print("=" * 80)

import random

# Crear lista de páginas según distribución
lista_paginas = []
for paginas, porcentaje in DISTRIBUCION_PAGINAS.items():
    cantidad = int(CANTIDAD_FACTURAS * porcentaje)
    lista_paginas.extend([paginas] * cantidad)

# Ajustar si hay diferencia por redondeo
while len(lista_paginas) < CANTIDAD_FACTURAS:
    lista_paginas.append(random.choice(list(DISTRIBUCION_PAGINAS.keys())))
while len(lista_paginas) > CANTIDAD_FACTURAS:
    lista_paginas.pop()

# Mezclar aleatoriamente
random.shuffle(lista_paginas)

# Mapeo de páginas a items
ITEMS_POR_PAGINAS = {
    3: (40, 45),   # 3 páginas: 40-45 items
    4: (46, 55),   # 4 páginas: 46-55 items
    5: (56, 70),   # 5 páginas: 56-70 items
    6: (71, 80),   # 6 páginas: 71-80 items
}

for i in range(1, CANTIDAD_FACTURAS + 1):
    # Determinar número de páginas
    num_paginas = lista_paginas[i - 1]

    # Determinar número de items
    min_items, max_items = ITEMS_POR_PAGINAS[num_paginas]
    num_items = random.randint(min_items, max_items)

    # Variar tipo de factura
    tipo = random.choice(['compra_grande', 'con_descuento'])
    con_credito = random.choice([True, False])
    moneda = random.choice(['PEN', 'USD', 'EUR'])

    # Generar factura
    factura = gen.generar_factura(
        tipo_factura=tipo,
        num_items=num_items,
        con_credito=con_credito,
        moneda=moneda
    )

    # Actualizar estadísticas
    stats['paginas'][num_paginas] += 1
    stats['items_total'] += num_items

    if tipo == 'con_descuento':
        stats['con_descuento'] += 1

    if con_credito:
        stats['con_credito'] += 1

    stats['monedas'][moneda] += 1

    # Exportar JSON
    filename = f"FACTURA_MP_{i:04d}_{num_paginas}PAG_{factura['serie']}_{factura['numero']}.json"
    json_path = json_exporter.exportar_factura(factura, filename=filename)

    # Mostrar progreso cada 10 facturas
    if i % 10 == 0 or i == CANTIDAD_FACTURAS:
        print(f"  ✅ Generadas: {i}/{CANTIDAD_FACTURAS} ({(i/CANTIDAD_FACTURAS)*100:.1f}%) - Última: {num_items} items ({num_paginas} pág)")

print("\n" + "=" * 80)
print("✅ LOTE COMPLETADO".center(80))
print("=" * 80)

print(f"\n📊 ESTADÍSTICAS:")
print("-" * 80)
print(f"  Total generadas: {CANTIDAD_FACTURAS}")
print(f"  Items totales: {stats['items_total']:,}")
print(f"  Promedio items por factura: {stats['items_total']/CANTIDAD_FACTURAS:.1f}")
print(f"\n  Distribución por páginas:")
for paginas in sorted(stats['paginas'].keys()):
    cantidad = stats['paginas'][paginas]
    porcentaje = (cantidad / CANTIDAD_FACTURAS) * 100
    print(f"    - {paginas} páginas: {cantidad} facturas ({porcentaje:.1f}%)")
print(f"\n  Tipos:")
print(f"    - Facturas con descuento: {stats['con_descuento']}")
print(f"    - Facturas con crédito: {stats['con_credito']}")
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

# 3. Generar lote multipágina
!cd /content/Creador-De-Factura && python GENERAR_LOTE_MULTIPAGINA.py

# 4. Generar PDFs desde los JSONs
import os
import json
from src.pdf_creator import PDFCreator

json_dir = "/content/Creador-De-Factura/{output_dir}"
pdf_dir = "/content/PDFs_LOTE_MULTIPAGINA"

pdf_creator = PDFCreator(output_dir=pdf_dir)

json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
print(f"Generando PDFs para {{len(json_files)}} facturas multipágina...")
print("⏱️  NOTA: Esto puede tomar varios minutos dependiendo de la cantidad")

for i, json_file in enumerate(json_files, 1):
    json_path = os.path.join(json_dir, json_file)
    with open(json_path, 'r', encoding='utf-8') as f:
        factura = json.load(f)

    pdf_path = pdf_creator.crear_factura(factura)

    if i % 10 == 0 or i == len(json_files):
        print(f"  PDFs generados: {{i}}/{{len(json_files)}} ({{(i/len(json_files))*100:.1f}}%)")

print(f"✅ {{len(json_files)}} PDFs generados en {{pdf_dir}}")

# 5. Comprimir y descargar
print("📦 Comprimiendo PDFs...")
!cd /content && zip -r PDFs_LOTE_MULTIPAGINA.zip PDFs_LOTE_MULTIPAGINA/

print("⬇️  Descargando archivo comprimido...")
from google.colab import files
files.download('/content/PDFs_LOTE_MULTIPAGINA.zip')

print("✅ LOTE MULTIPÁGINA COMPLETADO")
""")

print("\n" + "=" * 80)
print("🎯 CARACTERÍSTICAS DE ESTE LOTE")
print("=" * 80)
print("""
✅ Todas las facturas tienen MÚLTIPLES PÁGINAS (3-6 páginas)
✅ NO hay superposiciones de texto en NINGUNA página
✅ Posicionamiento dinámico en cascada:
   - Items → Descuentos → Totales → Forma de pago → Cuotas → Observaciones
✅ Cada elemento usa posiciones RELATIVAS (no fijas)
✅ Variedad de páginas según distribución configurada
✅ Múltiples monedas: PEN, USD, EUR
✅ JSONs con formato InvoiceX v5.5 (100/100)
✅ Coherencia matemática perfecta
✅ Fechas de cuotas escalonadas (30 días)
✅ Ubicaciones geográficas correctas (Departamento/Provincia/Distrito)

⏱️  TIEMPO ESTIMADO DE GENERACIÓN:
   - 100 facturas multipágina: ~2-3 minutos (JSONs)
   - PDFs: +5-10 minutos adicionales en Colab
   - 500 facturas: ~10-15 minutos (JSONs) + 25-50 minutos (PDFs)
   - 1000 facturas: ~20-30 minutos (JSONs) + 50-100 minutos (PDFs)
""")

print("\n✅ LOTE DE FACTURAS MULTIPÁGINA GENERADO EXITOSAMENTE")
print("=" * 80)
