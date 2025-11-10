"""
🎯 SCRIPT PARA GOOGLE COLAB - GENERACIÓN MASIVA DE FACTURAS
Genera múltiples facturas con variación automática de páginas

INSTRUCCIONES PARA GOOGLE COLAB:
1. Copia este código completo en una celda de Colab
2. Modifica solo la sección "CONFIGURACIÓN" (líneas marcadas con ###)
3. Ejecuta la celda
4. Espera a que termine
5. Descarga los archivos generados

"""

# ============================================================================
# ### CONFIGURACIÓN - MODIFICA ESTO ###
# ============================================================================

CANTIDAD_FACTURAS = 100    # 🔢 ¿Cuántas facturas quieres generar?
GENERAR_PDFS = True         # 📄 ¿Generar PDFs? (True/False)

# Distribución de páginas (ajusta los porcentajes, deben sumar 1.0)
DISTRIBUCION = {
    3: 0.25,  # 25% con 3 páginas (~40-45 items)
    4: 0.25,  # 25% con 4 páginas (~50-55 items)
    5: 0.25,  # 25% con 5 páginas (~60-70 items)
    6: 0.25,  # 25% con 6 páginas (~75-80 items)
}

# Monedas a usar (puedes quitar las que no necesites)
MONEDAS = ['PEN', 'USD', 'EUR']

# Probabilidad de generar facturas a crédito (0.0 = todas al contado, 1.0 = todas a crédito)
PROBABILIDAD_CREDITO = 0.5  # 50%

# ============================================================================
# NO MODIFICAR DEBAJO DE ESTA LÍNEA
# ============================================================================

print("=" * 80)
print("🚀 INICIANDO GENERACIÓN DE FACTURAS".center(80))
print("=" * 80)

# Paso 1: Instalar dependencias
print("\n📦 Paso 1/5: Instalando dependencias...")
import os

if GENERAR_PDFS:
    print("   Instalando reportlab para generar PDFs...")
    os.system('pip install reportlab -q')
    print("   ✅ reportlab instalado")
else:
    print("   ⚠️  PDFs deshabilitados, solo se generarán JSONs")

# Paso 2: Clonar/actualizar repositorio
print("\n📥 Paso 2/5: Configurando repositorio...")

repo_path = '/content/Creador-De-Factura'

if not os.path.exists(repo_path):
    print("   Clonando repositorio...")
    os.system(f'git clone https://github.com/GynoRomeroPrado/Creador-De-Factura.git {repo_path}')
else:
    print("   Actualizando repositorio...")
    os.system(f'cd {repo_path} && git pull')

print("   ✅ Repositorio listo")

# Paso 3: Cambiar al directorio
os.chdir(repo_path)
print(f"   Directorio actual: {os.getcwd()}")

# Paso 4: Importar módulos
print("\n📚 Paso 3/5: Importando módulos...")

import sys
sys.path.insert(0, repo_path)

from src.generator import FacturaGenerator
from src.json_exporter import JSONExporter

if GENERAR_PDFS:
    try:
        from src.pdf_creator import PDFCreator
    except ImportError:
        print("   ⚠️  No se pudo importar PDFCreator, se deshabilitarán los PDFs")
        GENERAR_PDFS = False

import random
from datetime import datetime
import json

print("   ✅ Módulos importados")

# Paso 5: Validar configuración
print("\n⚙️  Paso 4/5: Validando configuración...")

# Validar que la distribución sume aproximadamente 1.0
suma_dist = sum(DISTRIBUCION.values())
if abs(suma_dist - 1.0) > 0.01:
    print(f"   ⚠️  ADVERTENCIA: La distribución suma {suma_dist:.2f}, debería sumar 1.0")
    # Normalizar
    factor = 1.0 / suma_dist
    DISTRIBUCION = {k: v * factor for k, v in DISTRIBUCION.items()}
    print(f"   ✅ Distribución normalizada automáticamente")

print("\n📋 CONFIGURACIÓN FINAL:")
print("-" * 80)
print(f"   Facturas a generar: {CANTIDAD_FACTURAS}")
print(f"   Generar PDFs: {'✅ Sí' if GENERAR_PDFS else '❌ No'}")
print(f"   Monedas: {', '.join(MONEDAS)}")
print(f"   Probabilidad crédito: {PROBABILIDAD_CREDITO*100:.0f}%")
print(f"\n   Distribución de páginas:")
for paginas, prob in sorted(DISTRIBUCION.items()):
    num_facturas = int(CANTIDAD_FACTURAS * prob)
    print(f"     {paginas} páginas: {prob*100:.0f}% (~{num_facturas} facturas)")
print("-" * 80)

# Paso 6: Generar facturas
print(f"\n🔄 Paso 5/5: Generando {CANTIDAD_FACTURAS} facturas...")
print("=" * 80)

# Inicializar generadores
gen = FacturaGenerator()
json_exporter = JSONExporter(output_dir="/content/FACTURAS_JSONs")

if GENERAR_PDFS:
    pdf_creator = PDFCreator(output_dir="/content/FACTURAS_PDFs")

# Categorías disponibles
CATEGORIAS = ['construccion', 'servicios', None]

# Almacenar resultados
resultados = []
errores = []

# Generar facturas
for i in range(1, CANTIDAD_FACTURAS + 1):
    try:
        # Determinar número de páginas según distribución
        rand = random.random()
        acumulado = 0
        paginas_objetivo = 3

        for pags, prob in sorted(DISTRIBUCION.items()):
            acumulado += prob
            if rand <= acumulado:
                paginas_objetivo = pags
                break

        # Calcular items según páginas objetivo
        items_base = (paginas_objetivo - 1) * 15 + 15
        variacion = random.randint(-5, 5)
        num_items = max(40, min(90, items_base + variacion))

        # Seleccionar parámetros aleatorios
        moneda = random.choice(MONEDAS)
        categoria = random.choice(CATEGORIAS)
        con_credito = random.random() < PROBABILIDAD_CREDITO

        # Generar factura
        factura = gen.generar_factura(
            tipo_factura='compra_grande',
            num_items=num_items,
            categoria_items=categoria,
            con_credito=con_credito,
            moneda=moneda
        )

        paginas_reales = (len(factura['items']) // 15) + 1

        # Generar JSON
        json_path = json_exporter.exportar_factura(factura)

        # Generar PDF
        pdf_path = None
        if GENERAR_PDFS:
            try:
                pdf_path = pdf_creator.crear_factura(factura)
            except Exception as e:
                print(f"  [{i}/{CANTIDAD_FACTURAS}] ⚠️  Error PDF: {str(e)[:50]}")

        resultados.append({
            'numero': i,
            'serie': factura['numero_factura'],
            'items': len(factura['items']),
            'paginas': paginas_reales,
            'moneda': factura['moneda'],
            'total': factura['total'],
            'credito': con_credito,
            'json': json_path,
            'pdf': pdf_path
        })

        # Mostrar progreso
        if i % 20 == 0 or i == CANTIDAD_FACTURAS:
            print(f"  ✅ Progreso: {i}/{CANTIDAD_FACTURAS} ({i/CANTIDAD_FACTURAS*100:.0f}%) - "
                  f"Última: {factura['numero_factura']} ({paginas_reales} pág)")

    except Exception as e:
        errores.append({'numero': i, 'error': str(e)})
        print(f"  ❌ Error en factura {i}: {str(e)[:50]}")

# Generar estadísticas
print("\n" + "=" * 80)
print("📊 ESTADÍSTICAS FINALES".center(80))
print("=" * 80)

if resultados:
    # Contar por páginas
    por_paginas = {}
    for r in resultados:
        pags = r['paginas']
        por_paginas[pags] = por_paginas.get(pags, 0) + 1

    # Contar por moneda
    por_moneda = {}
    for r in resultados:
        mon = r['moneda']
        por_moneda[mon] = por_moneda.get(mon, 0) + 1

    # Totales
    total_items = sum(r['items'] for r in resultados)
    promedio_items = total_items / len(resultados)
    promedio_paginas = sum(r['paginas'] for r in resultados) / len(resultados)

    print(f"\n✅ Generadas exitosamente: {len(resultados)}/{CANTIDAD_FACTURAS}")
    if errores:
        print(f"❌ Errores: {len(errores)}")

    print(f"\n📄 Distribución por páginas:")
    print("-" * 80)
    for pags in sorted(por_paginas.keys()):
        count = por_paginas[pags]
        porcentaje = (count / len(resultados)) * 100
        barra = "█" * int(porcentaje / 2)
        print(f"  {pags} páginas: {count:4d} ({porcentaje:5.1f}%) {barra}")

    print(f"\n💰 Distribución por moneda:")
    print("-" * 80)
    for mon in sorted(por_moneda.keys()):
        count = por_moneda[mon]
        porcentaje = (count / len(resultados)) * 100
        print(f"  {mon}: {count:4d} ({porcentaje:5.1f}%)")

    print(f"\n📈 Resumen:")
    print("-" * 80)
    print(f"  Total items: {total_items:,}")
    print(f"  Promedio items/factura: {promedio_items:.1f}")
    print(f"  Promedio páginas/factura: {promedio_paginas:.1f}")
    print(f"  Con crédito: {sum(1 for r in resultados if r['credito'])}")
    print(f"  Al contado: {sum(1 for r in resultados if not r['credito'])}")

print(f"\n📁 Ubicación de archivos:")
print("-" * 80)
print(f"  JSONs: /content/FACTURAS_JSONs/")
if GENERAR_PDFS:
    print(f"  PDFs: /content/FACTURAS_PDFs/")

print("\n" + "=" * 80)
print("✅ GENERACIÓN COMPLETADA".center(80))
print("=" * 80)

# Guardar resumen en JSON
resumen = {
    'fecha_generacion': datetime.now().isoformat(),
    'configuracion': {
        'cantidad_solicitada': CANTIDAD_FACTURAS,
        'cantidad_generada': len(resultados),
        'generar_pdfs': GENERAR_PDFS,
        'monedas': MONEDAS,
        'probabilidad_credito': PROBABILIDAD_CREDITO,
        'distribucion_paginas': DISTRIBUCION
    },
    'estadisticas': {
        'por_paginas': por_paginas,
        'por_moneda': por_moneda,
        'promedio_items': promedio_items,
        'promedio_paginas': promedio_paginas,
        'total_errores': len(errores)
    },
    'facturas': resultados[:10]  # Solo las primeras 10 para no hacer el archivo muy grande
}

with open('/content/RESUMEN_GENERACION.json', 'w', encoding='utf-8') as f:
    json.dump(resumen, f, indent=2, ensure_ascii=False)

print("\n📊 Resumen guardado en: /content/RESUMEN_GENERACION.json")

# ============================================================================
# DESCARGAR ARCHIVOS
# ============================================================================

print("\n💾 DESCARGAR ARCHIVOS:")
print("=" * 80)
print("""
Para descargar los archivos generados, ejecuta esto en una nueva celda:

# Opción 1: Comprimir y descargar todo
!zip -r /content/facturas.zip /content/FACTURAS_JSONs /content/FACTURAS_PDFs
from google.colab import files
files.download('/content/facturas.zip')

# Opción 2: Descargar solo JSONs
!zip -r /content/facturas_json.zip /content/FACTURAS_JSONs
files.download('/content/facturas_json.zip')

# Opción 3: Ver archivos generados
!ls -lh /content/FACTURAS_JSONs/ | head -20
""")

print("\n🎉 ¡LISTO! Tus facturas están generadas.")
print("=" * 80)
