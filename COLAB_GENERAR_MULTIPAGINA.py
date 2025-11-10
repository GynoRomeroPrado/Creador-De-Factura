"""
🎯 SCRIPT PARA GOOGLE COLAB - GENERAR FACTURAS MULTIPÁGINA
Genera facturas con 40-80 items que producen PDFs de 3-6 páginas

INSTRUCCIONES PARA GOOGLE COLAB:
1. Clonar el repositorio
2. Instalar dependencias
3. Ejecutar este script
"""

# ============================================================================
# PASO 1: INSTALACIÓN Y CONFIGURACIÓN
# ============================================================================

# Instalar reportlab (necesario para generar PDFs)
print("📦 Instalando dependencias...")
!pip install reportlab -q

# Clonar o actualizar repositorio
import os
if not os.path.exists('/content/Creador-De-Factura'):
    print("📥 Clonando repositorio...")
    !git clone https://github.com/GynoRomeroPrado/Creador-De-Factura.git /content/Creador-De-Factura
else:
    print("🔄 Actualizando repositorio...")
    !cd /content/Creador-De-Factura && git pull

# Cambiar al directorio
os.chdir('/content/Creador-De-Factura')

# Importar módulos
import sys
sys.path.insert(0, '/content/Creador-De-Factura')

from src.generator import FacturaGenerator
from src.pdf_creator import PDFCreator
from src.json_exporter import JSONExporter

print("✅ Configuración completa\n")

# ============================================================================
# PASO 2: CONFIGURACIÓN DE FACTURAS MULTIPÁGINA
# ============================================================================

print("=" * 80)
print("🎯 GENERADOR DE FACTURAS MULTIPÁGINA".center(80))
print("=" * 80)

gen = FacturaGenerator()
pdf_creator = PDFCreator(output_dir="/content/PDFs_MULTIPAGINA")
json_exporter = JSONExporter(output_dir="/content/JSONs_MULTIPAGINA")

# Configuraciones (puedes modificar esto según necesites)
configuraciones = [
    {"nombre": "Construcción - 50 items (4 páginas)", "items": 50, "categoria": "construccion", "credito": True, "moneda": "PEN"},
    {"nombre": "Servicios - 45 items (3 páginas)", "items": 45, "categoria": "servicios", "credito": False, "moneda": "USD"},
    {"nombre": "Mixta - 60 items (5 páginas)", "items": 60, "categoria": None, "credito": True, "moneda": "PEN"},
    {"nombre": "Grande - 70 items (5 páginas)", "items": 70, "categoria": "construccion", "credito": True, "moneda": "USD"},
    {"nombre": "Extra Grande - 80 items (6 páginas)", "items": 80, "categoria": None, "credito": True, "moneda": "PEN"},
]

print(f"\n📋 Se generarán {len(configuraciones)} facturas multipágina")
print("-" * 80)

# ============================================================================
# PASO 3: GENERAR FACTURAS
# ============================================================================

resultados = []

for i, config in enumerate(configuraciones, 1):
    print(f"\n[{i}/{len(configuraciones)}] Generando: {config['nombre']}")
    print("-" * 80)

    try:
        # Generar factura
        factura = gen.generar_factura(
            tipo_factura='compra_grande',
            num_items=config['items'],
            categoria_items=config['categoria'],
            con_credito=config['credito'],
            moneda=config['moneda']
        )

        print(f"  ✅ Factura generada: {factura['numero_factura']}")
        print(f"     Items: {len(factura['items'])}")
        print(f"     Total: {factura['moneda']} {factura['total']:.2f}")

        # Generar PDF
        pdf_path = pdf_creator.crear_factura(factura)
        print(f"  ✅ PDF: {pdf_path}")

        # Generar JSON (formato InvoiceX v5.5)
        json_path = json_exporter.exportar_factura(factura)
        print(f"  ✅ JSON: {json_path}")

        # Calcular páginas estimadas
        paginas = (len(factura['items']) // 15) + 1
        print(f"  📄 Páginas estimadas: {paginas}")

        resultados.append({
            'nombre': config['nombre'],
            'serie': factura['numero_factura'],
            'items': len(factura['items']),
            'paginas': paginas,
            'pdf': pdf_path,
            'json': json_path,
            'total': factura['total']
        })

    except Exception as e:
        print(f"  ❌ Error: {str(e)}")

# ============================================================================
# PASO 4: RESUMEN
# ============================================================================

print("\n" + "=" * 80)
print("📊 RESUMEN DE GENERACIÓN".center(80))
print("=" * 80)

print(f"\n{'#':<4} {'Items':<7} {'Páginas':<10} {'Serie':<15} {'Total':<15}")
print("-" * 80)

for i, r in enumerate(resultados, 1):
    print(f"{i:<4} {r['items']:<7} {r['paginas']:<10} {r['serie']:<15} {r['total']:<15.2f}")

print("-" * 80)
print(f"\nTotal generadas: {len(resultados)}")
print(f"Con 3+ páginas: {sum(1 for r in resultados if r['paginas'] >= 3)}")
print(f"Con 4+ páginas: {sum(1 for r in resultados if r['paginas'] >= 4)}")
print(f"Con 5+ páginas: {sum(1 for r in resultados if r['paginas'] >= 5)}")

print("\n📁 ARCHIVOS GENERADOS:")
print("-" * 80)
print(f"  PDFs: /content/PDFs_MULTIPAGINA/")
print(f"  JSONs: /content/JSONs_MULTIPAGINA/")

print("\n" + "=" * 80)
print("✅ GENERACIÓN COMPLETADA".center(80))
print("=" * 80)

# ============================================================================
# PASO 5: DESCARGAR ARCHIVOS (OPCIONAL)
# ============================================================================

print("\n💡 PARA DESCARGAR ARCHIVOS:")
print("-" * 80)
print("""
# Opción 1: Descargar PDFs individualmente
from google.colab import files
files.download('/content/PDFs_MULTIPAGINA/Factura_compra_grande_FXXX_XXXXXX_XXXXXXXX.pdf')

# Opción 2: Comprimir y descargar todo
!zip -r /content/facturas_multipagina.zip /content/PDFs_MULTIPAGINA /content/JSONs_MULTIPAGINA
files.download('/content/facturas_multipagina.zip')

# Opción 3: Listar todos los PDFs generados
!ls -lh /content/PDFs_MULTIPAGINA/
""")

# ============================================================================
# BONUS: VERIFICAR UN PDF
# ============================================================================

print("\n🔍 VERIFICAR CONTENIDO DE UN PDF:")
print("-" * 80)

if resultados:
    primer_pdf = resultados[0]['pdf']
    print(f"Primer PDF generado: {primer_pdf}")
    print(f"Páginas estimadas: {resultados[0]['paginas']}")
    print(f"Items: {resultados[0]['items']}")

    print("\n💡 Para visualizar el PDF en Colab:")
    print(f"""
from google.colab import files
import os

# Mostrar el PDF
if os.path.exists('{primer_pdf}'):
    from IPython.display import IFrame
    IFrame('{primer_pdf}', width=800, height=600)
""")
