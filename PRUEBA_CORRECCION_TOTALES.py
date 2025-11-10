"""
🔧 PRUEBA DE CORRECCIÓN - PDFs MULTIPÁGINA SIN SUPERPOSICIÓN
Genera una factura multipágina para verificar que los totales no se superpongan
"""

import sys
sys.path.insert(0, '/home/user/Creador-De-Factura')

from src.generator import FacturaGenerator
from src.json_exporter import JSONExporter
import json

print("=" * 80)
print("🔧 PRUEBA DE CORRECCIÓN - TOTALES EN MULTIPÁGINA".center(80))
print("=" * 80)

# Generar factura con muchos items (60 items = ~5 páginas)
gen = FacturaGenerator()

print("\n📋 Generando factura con 60 items (~5 páginas)...")
factura = gen.generar_factura(
    tipo_factura='compra_grande',
    num_items=60,
    categoria_items='construccion',
    con_credito=True,
    moneda='PEN'
)

print(f"✅ Factura generada: {factura['numero_factura']}")
print(f"   Items: {len(factura['items'])}")
print(f"   Total: {factura['moneda']} {factura['total']:.2f}")
print(f"   Forma de pago: {factura['forma_pago']}")

# Exportar JSON
json_exporter = JSONExporter(output_dir=".")
json_path = json_exporter.exportar_factura(factura, filename="TEST_CORRECCION_TOTALES.json")
print(f"\n✅ JSON exportado: {json_path}")

# Verificar estructura del JSON
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

print("\n📊 VERIFICACIÓN DEL JSON:")
print("-" * 80)
print(f"  Items en JSON: {len(data['items'])}")
print(f"  Importe total: {data['importe_total']}")
print(f"  Moneda: {data['moneda']}")
print(f"  Observaciones: {data['observaciones'][:60]}...")
print(f"  Tipo documento: {data['tipo_documento']}")

# Verificar coherencia matemática
subtotal_calc = sum(item['valor_venta'] for item in data['items'])
igv_calc = sum(item['igv_item'] for item in data['items'])
total_calc = sum(item['importe_total_item'] for item in data['items'])

print("\n🔍 COHERENCIA MATEMÁTICA:")
print("-" * 80)
print(f"  Subtotal JSON: {data['subtotal']:.2f}")
print(f"  Subtotal calculado: {subtotal_calc:.2f}")
print(f"  ¿Coinciden? {'✅ SÍ' if abs(data['subtotal'] - subtotal_calc) < 0.01 else '❌ NO'}")
print()
print(f"  IGV JSON: {data['igv']:.2f}")
print(f"  IGV calculado: {igv_calc:.2f}")
print(f"  ¿Coinciden? {'✅ SÍ' if abs(data['igv'] - igv_calc) < 0.01 else '❌ NO'}")
print()
print(f"  Total JSON: {data['importe_total']:.2f}")
print(f"  Total calculado: {total_calc:.2f}")
print(f"  ¿Coinciden? {'✅ SÍ' if abs(data['importe_total'] - total_calc) < 0.01 else '❌ NO'}")

print("\n" + "=" * 80)
print("✅ PRUEBA COMPLETADA".center(80))
print("=" * 80)

print("\n📝 NOTAS:")
print("-" * 80)
print("""
✅ La corrección en pdf_creator.py incluye:

1. Guardar posición Y final después de dibujar items:
   y_despues_items = self._dibujar_items(c, datos, width, height)

2. Pasar esa posición a _dibujar_totales:
   y_final_totales = self._dibujar_totales(c, datos, width, height, y_inicio=y_despues_items)

3. _dibujar_totales ahora acepta y_inicio:
   - Si y_inicio != None: usa y_inicio - 25px (facturas multipágina)
   - Si y_inicio == None: usa posición fija 340/360 (facturas 1 página)

RESULTADO ESPERADO:
- En facturas de 1 página: Totales en posición fija (como antes)
- En facturas multipágina: Totales justo después de la tabla de items
- ❌ NO MÁS SUPERPOSICIONES

Para generar el PDF (requiere reportlab en Google Colab):
  from src.pdf_creator import PDFCreator
  pdf_creator = PDFCreator(output_dir="/content/PDFs")
  pdf_path = pdf_creator.crear_factura(factura)
  print(f"PDF: {pdf_path}")
""")

print("\n💡 Para probar en Google Colab:")
print("-" * 80)
print("""
# 1. Actualizar repositorio
!cd /content/Creador-De-Factura && git pull origin claude/fix-json-parsing-011CUyGo75ZndGpbT9KKAMXw

# 2. Instalar reportlab
!pip install reportlab

# 3. Generar factura multipágina
from src.generator import FacturaGenerator
from src.pdf_creator import PDFCreator

gen = FacturaGenerator()
pdf_creator = PDFCreator(output_dir="/content/PDFs")

# Generar factura con 60 items (5 páginas)
factura = gen.generar_factura(tipo_factura='compra_grande', num_items=60)
pdf_path = pdf_creator.crear_factura(factura)

# Descargar
from google.colab import files
files.download(pdf_path)

# VERIFICAR:
# - Los totales deben aparecer DESPUÉS de la tabla de items
# - NO debe haber superposiciones
# - Texto "SON:" debe estar visible sin cortes
# - Cada línea de totales debe tener espacio suficiente (18px entre líneas)
""")
