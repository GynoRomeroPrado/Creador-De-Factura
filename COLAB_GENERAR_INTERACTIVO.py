"""
🎯 GENERADOR INTERACTIVO DE FACTURAS PARA GOOGLE COLAB
Pregunta cuántas facturas de 1 página y multipágina deseas generar
"""

import sys
sys.path.insert(0, '/content/Creador-De-Factura')

import os
from datetime import datetime
from src.generator import FacturaGenerator
from src.json_exporter import JSONExporter
from src.pdf_creator import PDFFactura
import random

def generar_lote_interactivo():
    """Genera facturas preguntando al usuario cuántas desea de cada tipo"""

    print("=" * 80)
    print("🎯 GENERADOR INTERACTIVO DE FACTURAS".center(80))
    print("=" * 80)

    # Preguntar cantidad de facturas de 1 página
    print("\n📄 FACTURAS DE 1 PÁGINA (10-15 items cada una)")
    print("-" * 80)
    while True:
        try:
            cantidad_1_pagina = int(input("¿Cuántas facturas de 1 página deseas generar? (0-1000): "))
            if 0 <= cantidad_1_pagina <= 1000:
                break
            else:
                print("⚠️  Por favor ingresa un número entre 0 y 1000")
        except ValueError:
            print("⚠️  Por favor ingresa un número válido")

    # Preguntar cantidad de facturas multipágina
    print("\n📚 FACTURAS MULTIPÁGINA (3-6 páginas, 40-80 items cada una)")
    print("-" * 80)
    while True:
        try:
            cantidad_multipagina = int(input("¿Cuántas facturas multipágina deseas generar? (0-1000): "))
            if 0 <= cantidad_multipagina <= 1000:
                break
            else:
                print("⚠️  Por favor ingresa un número entre 0 y 1000")
        except ValueError:
            print("⚠️  Por favor ingresa un número válido")

    # Verificar que al menos haya una factura
    total = cantidad_1_pagina + cantidad_multipagina
    if total == 0:
        print("\n⚠️  No se generará ninguna factura. Saliendo...")
        return

    # Confirmar
    print("\n" + "=" * 80)
    print("📊 RESUMEN DE GENERACIÓN".center(80))
    print("=" * 80)
    print(f"  Facturas de 1 página: {cantidad_1_pagina}")
    print(f"  Facturas multipágina: {cantidad_multipagina}")
    print(f"  TOTAL A GENERAR: {total}")
    print("=" * 80)

    confirmacion = input("\n¿Proceder con la generación? (s/n): ").lower()
    if confirmacion != 's':
        print("❌ Generación cancelada")
        return

    # Crear carpeta de salida
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = f"facturas_generadas/LOTE_INTERACTIVO_{timestamp}"
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n📁 Carpeta de salida: {output_dir}")

    # Inicializar generadores
    gen = FacturaGenerator()
    json_exporter = JSONExporter(output_dir=output_dir)

    # Estadísticas
    stats = {
        'pagina_unica': 0,
        'multipagina': 0,
        'con_descuento': 0,
        'con_credito': 0,
        'monedas': {'PEN': 0, 'USD': 0, 'EUR': 0},
        'paginas': {1: 0, 3: 0, 4: 0, 5: 0, 6: 0}
    }

    contador_total = 0

    # GENERAR FACTURAS DE 1 PÁGINA
    if cantidad_1_pagina > 0:
        print("\n" + "=" * 80)
        print(f"📄 GENERANDO {cantidad_1_pagina} FACTURAS DE 1 PÁGINA...")
        print("=" * 80)

        for i in range(1, cantidad_1_pagina + 1):
            tipo = random.choice(['general', 'con_descuento', 'general', 'general'])
            num_items = random.randint(10, 15)
            con_credito = random.choice([True, False])
            moneda = random.choice(['PEN', 'USD', 'EUR'])

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

            if con_credito:
                stats['con_credito'] += 1

            stats['monedas'][moneda] += 1
            stats['pagina_unica'] += 1
            stats['paginas'][1] += 1
            contador_total += 1

            filename = f"FACTURA_{contador_total:04d}_1PAG_{factura['serie']}_{factura['numero']}.json"
            json_exporter.exportar_factura(factura, filename=filename)

            if i % 10 == 0 or i == cantidad_1_pagina:
                print(f"  ✅ Generadas: {i}/{cantidad_1_pagina} ({(i/cantidad_1_pagina)*100:.1f}%)")

    # GENERAR FACTURAS MULTIPÁGINA
    if cantidad_multipagina > 0:
        print("\n" + "=" * 80)
        print(f"📚 GENERANDO {cantidad_multipagina} FACTURAS MULTIPÁGINA...")
        print("=" * 80)

        # Distribución de páginas
        ITEMS_POR_PAGINAS = {
            3: (40, 45),
            4: (46, 55),
            5: (56, 70),
            6: (71, 80),
        }

        for i in range(1, cantidad_multipagina + 1):
            num_paginas = random.choice([3, 4, 5, 6])
            min_items, max_items = ITEMS_POR_PAGINAS[num_paginas]
            num_items = random.randint(min_items, max_items)

            tipo = random.choice(['compra_grande', 'con_descuento'])
            con_credito = random.choice([True, False])
            moneda = random.choice(['PEN', 'USD', 'EUR'])

            factura = gen.generar_factura(
                tipo_factura=tipo,
                num_items=num_items,
                con_credito=con_credito,
                moneda=moneda
            )

            if tipo == 'con_descuento':
                stats['con_descuento'] += 1

            if con_credito:
                stats['con_credito'] += 1

            stats['monedas'][moneda] += 1
            stats['multipagina'] += 1
            stats['paginas'][num_paginas] += 1
            contador_total += 1

            filename = f"FACTURA_{contador_total:04d}_{num_paginas}PAG_{factura['serie']}_{factura['numero']}.json"
            json_exporter.exportar_factura(factura, filename=filename)

            if i % 10 == 0 or i == cantidad_multipagina:
                print(f"  ✅ Generadas: {i}/{cantidad_multipagina} ({(i/cantidad_multipagina)*100:.1f}%) - Última: {num_items} items ({num_paginas} pág)")

    # MOSTRAR ESTADÍSTICAS
    print("\n" + "=" * 80)
    print("✅ GENERACIÓN DE JSONs COMPLETADA".center(80))
    print("=" * 80)

    print(f"\n📊 ESTADÍSTICAS:")
    print("-" * 80)
    print(f"  Total generado: {contador_total}")
    print(f"  Facturas de 1 página: {stats['pagina_unica']}")
    print(f"  Facturas multipágina: {stats['multipagina']}")

    if stats['multipagina'] > 0:
        print(f"\n  Distribución por páginas:")
        if stats['paginas'][1] > 0:
            print(f"    - 1 página: {stats['paginas'][1]} facturas")
        for pag in [3, 4, 5, 6]:
            if stats['paginas'][pag] > 0:
                print(f"    - {pag} páginas: {stats['paginas'][pag]} facturas")

    print(f"\n  Tipos:")
    print(f"    - Con descuento: {stats['con_descuento']}")
    print(f"    - Con crédito: {stats['con_credito']}")

    print(f"\n  Monedas:")
    print(f"    - PEN (Soles): {stats['monedas']['PEN']}")
    print(f"    - USD (Dólares): {stats['monedas']['USD']}")
    print(f"    - EUR (Euros): {stats['monedas']['EUR']}")

    print(f"\n📁 JSONs guardados en: {output_dir}")

    # GENERAR PDFs
    print("\n" + "=" * 80)
    print("📄 GENERACIÓN DE PDFs".center(80))
    print("=" * 80)

    generar_pdfs = input("\n¿Deseas generar los PDFs ahora? (s/n): ").lower()

    if generar_pdfs == 's':
        print("\n🔧 Generando PDFs...")
        print("⏱️  Esto puede tomar varios minutos dependiendo de la cantidad...")

        pdf_dir = f"/content/PDFs_LOTE_{timestamp}"
        pdf_creator = PDFFactura(output_dir=pdf_dir)

        json_files = [f for f in os.listdir(output_dir) if f.endswith('.json')]

        for i, json_file in enumerate(json_files, 1):
            import json
            json_path = os.path.join(output_dir, json_file)
            with open(json_path, 'r', encoding='utf-8') as f:
                factura = json.load(f)

            pdf_creator.crear_factura(factura)

            if i % 10 == 0 or i == len(json_files):
                print(f"  PDFs generados: {i}/{len(json_files)} ({(i/len(json_files))*100:.1f}%)")

        print(f"\n✅ {len(json_files)} PDFs generados en {pdf_dir}")

        # Comprimir PDFs
        print("\n📦 Comprimiendo PDFs para descarga...")
        os.system(f"cd /content && zip -q -r PDFs_LOTE_{timestamp}.zip PDFs_LOTE_{timestamp}/")

        print("\n⬇️  Para descargar los PDFs, ejecuta:")
        print(f"from google.colab import files")
        print(f"files.download('/content/PDFs_LOTE_{timestamp}.zip')")
    else:
        print("\n⏭️  PDFs no generados. Puedes generarlos después con:")
        print(f"\nimport os, json")
        print(f"from src.pdf_creator import PDFFactura")
        print(f"")
        print(f"pdf_creator = PDFFactura(output_dir='/content/PDFs')")
        print(f"json_dir = '{output_dir}'")
        print(f"")
        print(f"for json_file in os.listdir(json_dir):")
        print(f"    if json_file.endswith('.json'):")
        print(f"        with open(os.path.join(json_dir, json_file), 'r') as f:")
        print(f"            factura = json.load(f)")
        print(f"        pdf_creator.crear_factura(factura)")

    print("\n" + "=" * 80)
    print("🎉 PROCESO COMPLETADO".center(80))
    print("=" * 80)


# Ejecutar si se llama directamente
if __name__ == "__main__":
    try:
        generar_lote_interactivo()
    except KeyboardInterrupt:
        print("\n\n❌ Proceso interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
