"""
🎯 GENERADOR DE LOTES DE FACTURAS CON VARIACIÓN DE PÁGINAS
Genera múltiples facturas con variación automática de páginas (3-6 páginas)

USO:
    python GENERAR_LOTE_FACTURAS.py

O desde código:
    from GENERAR_LOTE_FACTURAS import generar_lote_facturas
    generar_lote_facturas(cantidad=100)
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.generator import FacturaGenerator
from src.json_exporter import JSONExporter
import random
from datetime import datetime

def generar_lote_facturas(
    cantidad=50,
    min_items=40,
    max_items=80,
    output_dir="facturas_generadas/LOTE",
    incluir_pdfs=False,
    distribucion_paginas=None,
    monedas=None,
    credito_probabilidad=0.5
):
    """
    Genera un lote de facturas con variación de páginas

    Args:
        cantidad (int): Número de facturas a generar
        min_items (int): Mínimo de items por factura (default: 40 = ~3 páginas)
        max_items (int): Máximo de items por factura (default: 80 = ~6 páginas)
        output_dir (str): Directorio de salida
        incluir_pdfs (bool): Si True, genera PDFs (requiere reportlab)
        distribucion_paginas (dict): Distribución personalizada de páginas
            Ejemplo: {3: 0.2, 4: 0.3, 5: 0.3, 6: 0.2}
            Significa: 20% con 3 páginas, 30% con 4 páginas, etc.
        monedas (list): Lista de monedas a usar (default: ['PEN', 'USD', 'EUR'])
        credito_probabilidad (float): Probabilidad de generar factura a crédito (0.0-1.0)

    Returns:
        dict: Estadísticas de generación
    """

    print("=" * 80)
    print("🎯 GENERADOR DE LOTE DE FACTURAS".center(80))
    print("=" * 80)

    # Configuración
    gen = FacturaGenerator()
    json_exporter = JSONExporter(output_dir=output_dir)

    if incluir_pdfs:
        try:
            from src.pdf_creator import PDFCreator
            pdf_creator = PDFCreator(output_dir=output_dir + "_PDFs")
        except ImportError:
            print("⚠️  reportlab no instalado. No se generarán PDFs.")
            incluir_pdfs = False

    # Configurar monedas
    if monedas is None:
        monedas = ['PEN', 'USD', 'EUR']

    # Configurar distribución de páginas
    if distribucion_paginas is None:
        # Distribución balanceada por defecto
        # Mapeo: páginas -> items aproximados
        distribucion_paginas = {
            3: 0.20,  # 20% con 3 páginas (~40-45 items)
            4: 0.30,  # 30% con 4 páginas (~50-55 items)
            5: 0.30,  # 30% con 5 páginas (~60-70 items)
            6: 0.20,  # 20% con 6 páginas (~75-80 items)
        }

    print(f"\n📋 CONFIGURACIÓN:")
    print("-" * 80)
    print(f"  Cantidad de facturas: {cantidad}")
    print(f"  Rango de items: {min_items}-{max_items}")
    print(f"  Páginas estimadas: {min_items//15 + 1}-{max_items//15 + 1}")
    print(f"  Generar PDFs: {'✅ Sí' if incluir_pdfs else '❌ No'}")
    print(f"  Monedas: {', '.join(monedas)}")
    print(f"  Probabilidad crédito: {credito_probabilidad*100:.0f}%")
    print(f"\n  Distribución de páginas:")
    for paginas, prob in sorted(distribucion_paginas.items()):
        num_facturas = int(cantidad * prob)
        print(f"    {paginas} páginas: {prob*100:.0f}% ({num_facturas} facturas)")
    print("-" * 80)

    # Categorías disponibles
    categorias = ['construccion', 'servicios', None]  # None = mixto

    # Generar facturas
    resultados = []
    errores = []

    print(f"\n🔄 GENERANDO {cantidad} FACTURAS...")
    print("=" * 80)

    for i in range(1, cantidad + 1):
        try:
            # Determinar número de páginas según distribución
            rand = random.random()
            acumulado = 0
            paginas_objetivo = 3

            for pags, prob in sorted(distribucion_paginas.items()):
                acumulado += prob
                if rand <= acumulado:
                    paginas_objetivo = pags
                    break

            # Calcular items según páginas objetivo
            # Fórmula: items ≈ (páginas - 1) * 15 + variación
            items_base = (paginas_objetivo - 1) * 15 + 15
            variacion = random.randint(-5, 5)
            num_items = max(min_items, min(max_items, items_base + variacion))

            # Seleccionar parámetros aleatorios
            moneda = random.choice(monedas)
            categoria = random.choice(categorias)
            con_credito = random.random() < credito_probabilidad

            # Generar factura
            factura = gen.generar_factura(
                tipo_factura='compra_grande',
                num_items=num_items,
                categoria_items=categoria,
                con_credito=con_credito,
                moneda=moneda
            )

            # Calcular páginas reales
            paginas_reales = (len(factura['items']) // 15) + 1

            # Generar JSON
            json_path = json_exporter.exportar_factura(factura)

            # Generar PDF si está habilitado
            pdf_path = None
            if incluir_pdfs:
                try:
                    pdf_path = pdf_creator.crear_factura(factura)
                except Exception as e:
                    print(f"  [{i}/{cantidad}] ⚠️  Error generando PDF: {str(e)}")

            # Guardar resultado
            resultado = {
                'numero': i,
                'serie': factura['numero_factura'],
                'items': len(factura['items']),
                'paginas': paginas_reales,
                'moneda': factura['moneda'],
                'total': factura['total'],
                'credito': con_credito,
                'categoria': categoria or 'mixto',
                'json_path': json_path,
                'pdf_path': pdf_path
            }
            resultados.append(resultado)

            # Mostrar progreso cada 10 facturas
            if i % 10 == 0 or i == cantidad:
                print(f"  [{i}/{cantidad}] ✅ {factura['numero_factura']} - "
                      f"{len(factura['items'])} items (~{paginas_reales} pág) - "
                      f"{factura['moneda']} {factura['total']:.2f}")

        except Exception as e:
            errores.append({
                'numero': i,
                'error': str(e)
            })
            print(f"  [{i}/{cantidad}] ❌ Error: {str(e)}")

    # Generar estadísticas
    print("\n" + "=" * 80)
    print("📊 ESTADÍSTICAS DE GENERACIÓN".center(80))
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
        total_importe = sum(r['total'] for r in resultados)
        promedio_items = total_items / len(resultados)
        promedio_paginas = sum(r['paginas'] for r in resultados) / len(resultados)

        print(f"\n✅ Facturas generadas exitosamente: {len(resultados)}/{cantidad}")
        if errores:
            print(f"❌ Errores: {len(errores)}")

        print(f"\n📄 Distribución por páginas:")
        print("-" * 80)
        for pags in sorted(por_paginas.keys()):
            count = por_paginas[pags]
            porcentaje = (count / len(resultados)) * 100
            barra = "█" * int(porcentaje / 2)
            print(f"  {pags} páginas: {count:4d} facturas ({porcentaje:5.1f}%) {barra}")

        print(f"\n💰 Distribución por moneda:")
        print("-" * 80)
        for mon in sorted(por_moneda.keys()):
            count = por_moneda[mon]
            porcentaje = (count / len(resultados)) * 100
            print(f"  {mon}: {count:4d} facturas ({porcentaje:5.1f}%)")

        print(f"\n📈 Resumen general:")
        print("-" * 80)
        print(f"  Total items: {total_items:,}")
        print(f"  Promedio items/factura: {promedio_items:.1f}")
        print(f"  Promedio páginas/factura: {promedio_paginas:.1f}")
        print(f"  Total importe (aprox): Mixto")
        print(f"  Con crédito: {sum(1 for r in resultados if r['credito'])} facturas")
        print(f"  Al contado: {sum(1 for r in resultados if not r['credito'])} facturas")

    print(f"\n📁 Archivos guardados en:")
    print("-" * 80)
    print(f"  JSONs: {output_dir}/")
    if incluir_pdfs:
        print(f"  PDFs: {output_dir}_PDFs/")

    print("\n" + "=" * 80)
    print("✅ GENERACIÓN COMPLETADA".center(80))
    print("=" * 80)

    # Retornar estadísticas
    return {
        'total_generadas': len(resultados),
        'total_errores': len(errores),
        'resultados': resultados,
        'errores': errores,
        'por_paginas': por_paginas,
        'por_moneda': por_moneda,
        'promedio_items': promedio_items if resultados else 0,
        'promedio_paginas': promedio_paginas if resultados else 0
    }


# ============================================================================
# EJEMPLOS DE USO
# ============================================================================

def ejemplo_basico():
    """Genera 50 facturas con configuración por defecto"""
    return generar_lote_facturas(cantidad=50)


def ejemplo_100_facturas():
    """Genera 100 facturas balanceadas"""
    return generar_lote_facturas(
        cantidad=100,
        min_items=40,
        max_items=80
    )


def ejemplo_personalizado():
    """Genera 30 facturas con configuración personalizada"""
    return generar_lote_facturas(
        cantidad=30,
        min_items=50,
        max_items=70,
        distribucion_paginas={
            4: 0.5,  # 50% con 4 páginas
            5: 0.5,  # 50% con 5 páginas
        },
        monedas=['PEN', 'USD'],  # Solo soles y dólares
        credito_probabilidad=0.7  # 70% a crédito
    )


def ejemplo_muchas_paginas():
    """Genera facturas con muchas páginas (5-6 páginas)"""
    return generar_lote_facturas(
        cantidad=20,
        min_items=60,
        max_items=90,
        distribucion_paginas={
            5: 0.5,  # 50% con 5 páginas
            6: 0.5,  # 50% con 6 páginas
        }
    )


# ============================================================================
# EJECUCIÓN PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Generar lote de facturas con múltiples páginas')
    parser.add_argument('--cantidad', type=int, default=50, help='Número de facturas a generar')
    parser.add_argument('--min-items', type=int, default=40, help='Mínimo de items por factura')
    parser.add_argument('--max-items', type=int, default=80, help='Máximo de items por factura')
    parser.add_argument('--output', type=str, default='facturas_generadas/LOTE', help='Directorio de salida')
    parser.add_argument('--pdfs', action='store_true', help='Generar también PDFs (requiere reportlab)')
    parser.add_argument('--credito', type=float, default=0.5, help='Probabilidad de crédito (0.0-1.0)')

    args = parser.parse_args()

    # Generar lote
    stats = generar_lote_facturas(
        cantidad=args.cantidad,
        min_items=args.min_items,
        max_items=args.max_items,
        output_dir=args.output,
        incluir_pdfs=args.pdfs,
        credito_probabilidad=args.credito
    )

    print(f"\n✅ Proceso completado: {stats['total_generadas']}/{args.cantidad} facturas generadas")
