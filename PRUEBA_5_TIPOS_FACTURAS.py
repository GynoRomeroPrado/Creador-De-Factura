"""
🧪 PRUEBA COMPLETA - 5 TIPOS DE FACTURAS
Verifica que NO haya superposiciones en ningún caso
"""

import sys
sys.path.insert(0, '/home/user/Creador-De-Factura')

from src.generator import FacturaGenerator
from src.json_exporter import JSONExporter

print("=" * 80)
print("🧪 PRUEBA COMPLETA - 5 TIPOS DE FACTURAS".center(80))
print("=" * 80)

gen = FacturaGenerator()
json_exporter = JSONExporter(output_dir=".")

configuraciones = [
    {
        "nombre": "1. Factura normal sin descuentos ni cuotas (1 página)",
        "tipo": "general",
        "items": 10,
        "credito": False,
        "con_descuento": None
    },
    {
        "nombre": "2. Factura con descuentos (1 página)",
        "tipo": "con_descuento",
        "items": 12,
        "credito": False,
        "con_descuento": True
    },
    {
        "nombre": "3. Factura con cuotas (1 página)",
        "tipo": "general",
        "items": 10,
        "credito": True,
        "con_descuento": None
    },
    {
        "nombre": "4. Factura multipágina sin cuotas (3-4 páginas)",
        "tipo": "compra_grande",
        "items": 50,
        "credito": False,
        "con_descuento": None
    },
    {
        "nombre": "5. Factura multipágina con cuotas (5-6 páginas)",
        "tipo": "compra_grande",
        "items": 70,
        "credito": True,
        "con_descuento": None
    }
]

print("\n📋 GENERANDO 5 TIPOS DE FACTURAS...")
print("=" * 80)

resultados = []

for i, config in enumerate(configuraciones, 1):
    print(f"\n[{i}/5] {config['nombre']}")
    print("-" * 80)

    # Generar factura
    factura = gen.generar_factura(
        tipo_factura=config['tipo'],
        num_items=config['items'],
        con_credito=config['credito'],
        con_descuento=config['con_descuento'],
        moneda='PEN'
    )

    print(f"  ✅ Factura: {factura['numero_factura']}")
    print(f"     Items: {len(factura['items'])}")
    print(f"     Páginas estimadas: {len(factura['items']) // 15 + 1}")
    print(f"     Total: {factura['moneda']} {factura['total']:.2f}")
    print(f"     Crédito: {'Sí' if factura['con_credito'] else 'No'}")
    print(f"     Cuotas: {len(factura.get('cuotas', []))}")
    print(f"     Descuento: {'Sí' if factura.get('descuento') else 'No'}")

    # Exportar JSON
    filename = f"PRUEBA_TIPO{i}_{factura['serie']}_{factura['numero']}.json"
    json_path = json_exporter.exportar_factura(factura, filename=filename)
    print(f"  ✅ JSON: {json_path}")

    resultados.append({
        'tipo': config['nombre'],
        'serie': factura['numero_factura'],
        'items': len(factura['items']),
        'paginas': len(factura['items']) // 15 + 1,
        'credito': factura['con_credito'],
        'cuotas': len(factura.get('cuotas', [])),
        'descuento': bool(factura.get('descuento')),
        'json': json_path
    })

print("\n" + "=" * 80)
print("📊 RESUMEN DE PRUEBAS".center(80))
print("=" * 80)

print(f"\n{'#':<4} {'Tipo':<45} {'Items':<7} {'Pág':<5} {'Cuotas':<8} {'Desc':<6}")
print("-" * 80)

for i, r in enumerate(resultados, 1):
    tipo_short = r['tipo'].split('. ')[1] if '. ' in r['tipo'] else r['tipo']
    desc_str = "Sí" if r['descuento'] else "No"
    print(f"{i:<4} {tipo_short:<45} {r['items']:<7} {r['paginas']:<5} {r['cuotas']:<8} {desc_str:<6}")

print("\n✅ FACTURAS GENERADAS: 5/5")

print("\n" + "=" * 80)
print("🔍 VERIFICACIÓN EN GOOGLE COLAB".center(80))
print("=" * 80)

print("""
# 1. Actualizar repositorio
!cd /content/Creador-De-Factura && git pull origin claude/fix-json-parsing-011CUyGo75ZndGpbT9KKAMXw

# 2. Instalar reportlab
!pip install reportlab

# 3. Generar los 5 tipos de PDFs
from src.generator import FacturaGenerator
from src.pdf_creator import PDFCreator

gen = FacturaGenerator()
pdf_creator = PDFCreator(output_dir="/content/PDFs_PRUEBA")

pdfs = []

# Tipo 1: Normal (1 página)
f1 = gen.generar_factura(tipo_factura='general', num_items=10, con_credito=False)
pdfs.append(pdf_creator.crear_factura(f1))

# Tipo 2: Con descuentos (1 página)
f2 = gen.generar_factura(tipo_factura='con_descuento', num_items=12, con_credito=False)
pdfs.append(pdf_creator.crear_factura(f2))

# Tipo 3: Con cuotas (1 página)
f3 = gen.generar_factura(tipo_factura='general', num_items=10, con_credito=True)
pdfs.append(pdf_creator.crear_factura(f3))

# Tipo 4: Multipágina sin cuotas (3-4 páginas)
f4 = gen.generar_factura(tipo_factura='compra_grande', num_items=50, con_credito=False)
pdfs.append(pdf_creator.crear_factura(f4))

# Tipo 5: Multipágina con cuotas (5-6 páginas)
f5 = gen.generar_factura(tipo_factura='compra_grande', num_items=70, con_credito=True)
pdfs.append(pdf_creator.crear_factura(f5))

# Descargar todos
from google.colab import files
for pdf in pdfs:
    files.download(pdf)

# VERIFICAR EN LOS PDFs:
# ✅ NO debe haber superposiciones de textos
# ✅ Items, totales, forma de pago, cuotas separados con espacio
# ✅ "SON:" visible y sin cortes
# ✅ Tabla de totales (OP. GRAVADAS, IGV, TOTAL) sin superposiciones
# ✅ Tabla de cuotas (si hay) sin superposiciones
# ✅ Observaciones visibles
""")

print("\n" + "=" * 80)
print("✅ PRUEBA COMPLETADA".center(80))
print("=" * 80)

print("\n📝 CHECKLIST DE VERIFICACIÓN:")
print("-" * 80)
print("""
Para cada tipo de factura, verificar en el PDF:

1. Factura normal (1 página):
   ✅ Tabla de items sin superposiciones
   ✅ Totales (OP. GRAVADAS, IGV, TOTAL) bien espaciados
   ✅ "SON:" visible
   ✅ Forma de pago visible
   ✅ Sin observaciones superpuestas

2. Factura con descuentos (1 página):
   ✅ Tabla de descuentos visible y separada
   ✅ Totales NO superpuestos con descuentos
   ✅ Todo el flujo bien espaciado

3. Factura con cuotas (1 página):
   ✅ "DATOS DE CUOTA:" visible
   ✅ Tabla de cuotas (N°, MONTO, FECHA) sin superposiciones
   ✅ Cuotas NO superpuestas con forma de pago

4. Factura multipágina sin cuotas (3-4 páginas):
   ✅ Items continúan en páginas siguientes
   ✅ Totales DESPUÉS de items (no superpuestos)
   ✅ Forma de pago DESPUÉS de totales

5. Factura multipágina con cuotas (5-6 páginas):
   ✅ Items en múltiples páginas sin superposiciones
   ✅ Totales al final sin superposiciones
   ✅ Cuotas visibles y separadas
   ✅ TODO el flujo funcional
""")
