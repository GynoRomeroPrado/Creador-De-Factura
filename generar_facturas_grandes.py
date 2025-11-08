"""
Script para generar facturas con muchos items (múltiples páginas)
"""
import sys
sys.path.insert(0, 'src')

from src.generator import FacturaGenerator
from src.pdf_creator import PDFFactura
from src.dataset_exporter import DatasetExporter


def generar_facturas_con_muchos_items():
    """Genera facturas con diferentes cantidades de items para probar múltiples páginas"""

    print("=" * 80)
    print("GENERANDO FACTURAS CON MUCHOS ITEMS (MÚLTIPLES PÁGINAS)".center(80))
    print("=" * 80)

    # Crear generadores
    factura_gen = FacturaGenerator()
    pdf_gen = PDFFactura(output_dir='facturas_generadas/facturas_grandes')
    exporter = DatasetExporter(base_dir='facturas_generadas/facturas_grandes')
    dataset_dir = exporter.crear_dataset()

    print(f"\n📁 Dataset: {dataset_dir}\n")

    # Generar facturas con diferentes cantidades
    configuraciones = [
        {'tipo': 'compra_grande', 'items': None, 'descripcion': 'Compra grande automática (30-50 items)'},
        {'tipo': 'general', 'items': 40, 'descripcion': 'Factura general con 40 items'},
        {'tipo': 'compra_grande', 'items': 60, 'descripcion': 'Compra grande con 60 items (3+ páginas)'},
        {'tipo': 'general', 'items': 25, 'descripcion': 'Factura general con 25 items'},
        {'tipo': 'compra_grande', 'items': None, 'descripcion': 'Compra grande automática (30-50 items)'},
    ]

    facturas_generadas = []

    for i, config in enumerate(configuraciones, 1):
        print(f"\n[{i}/5] Generando: {config['descripcion']}")

        # Generar factura
        factura = factura_gen.generar_factura(
            tipo_factura=config['tipo'],
            num_items=config['items']
        )

        num_items = len(factura['items'])
        total = factura['total']
        serie = factura['numero_factura']

        print(f"    Serie: {serie}")
        print(f"    Items: {num_items}")
        print(f"    Total: {factura['simbolo_moneda']}{total:,.2f}")

        # Generar PDF
        try:
            pdf_path = pdf_gen.crear_factura(factura)
            print(f"    PDF: ✅ Generado")

            # Leer PDF para exportar
            with open(pdf_path, 'rb') as f:
                pdf_content = f.read()

            # Exportar a dataset
            json_path, _ = exporter.exportar_factura(factura, pdf_content)
            print(f"    JSON: ✅ Exportado")

            # Estimar páginas (aproximado: 25-30 items por página)
            paginas_estimadas = max(1, (num_items // 28) + 1)
            print(f"    Páginas estimadas: {paginas_estimadas}")

            facturas_generadas.append({
                'serie': serie,
                'items': num_items,
                'total': total,
                'paginas': paginas_estimadas,
                'pdf': pdf_path
            })

        except Exception as e:
            print(f"    ❌ Error: {e}")

    # Resumen
    print("\n" + "=" * 80)
    print("RESUMEN".center(80))
    print("=" * 80)

    print(f"\n{'Serie':<18} {'Items':<8} {'Total':<15} {'Páginas':<10}")
    print("-" * 65)

    for f in facturas_generadas:
        print(f"{f['serie']:<18} {f['items']:<8} ${f['total']:>12,.2f} {f['paginas']:<10}")

    print(f"\n✅ Total facturas generadas: {len(facturas_generadas)}")
    print(f"✅ Dataset guardado en: {dataset_dir}")

    # Items por factura
    total_items = sum(f['items'] for f in facturas_generadas)
    promedio_items = total_items / len(facturas_generadas) if facturas_generadas else 0

    print(f"\n📊 Estadísticas:")
    print(f"   • Total de items: {total_items}")
    print(f"   • Promedio por factura: {promedio_items:.1f} items")
    print(f"   • Factura con más items: {max(f['items'] for f in facturas_generadas)} items")
    print(f"   • Factura con menos items: {min(f['items'] for f in facturas_generadas)} items")

    print("\n💡 Revisa los PDFs para verificar que las páginas se crean correctamente.")


if __name__ == "__main__":
    generar_facturas_con_muchos_items()
