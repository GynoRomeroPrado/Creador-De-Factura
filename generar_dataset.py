"""
Script para generar dataset de facturas con estructura organizada
"""
import os
import sys
from datetime import datetime

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.generator import FacturaGenerator
from src.dataset_exporter import DatasetExporter

# Intentar importar PDF creator
try:
    from src.pdf_creator import PDFFactura
    PDF_DISPONIBLE = True
except ImportError:
    PDF_DISPONIBLE = False
    print("⚠️  PDFFactura no disponible. Se generarán solo JSONs.")


def generar_dataset(cantidad: int = 10, con_pdfs: bool = True):
    """
    Genera un dataset completo de facturas
    Args:
        cantidad: Número de facturas a generar
        con_pdfs: Si True, genera PDFs (requiere reportlab)
    """
    print("=" * 70)
    print(f"GENERANDO DATASET DE {cantidad} FACTURAS".center(70))
    print("=" * 70)

    # Crear exportador y estructura
    exporter = DatasetExporter(base_dir="facturas_generadas")
    dataset_dir = exporter.crear_dataset()

    print(f"\n📁 Dataset creado: {os.path.basename(dataset_dir)}")
    print(f"   Ruta: {dataset_dir}")
    print(f"\n📂 Estructura:")
    print(f"   ├── anotaciones/")
    print(f"   ├── facturas_procesadas/")
    print(f"   ├── rechazadas/")
    print(f"   └── reportes/")

    # Generadores
    factura_gen = FacturaGenerator()
    if con_pdfs and PDF_DISPONIBLE:
        pdf_gen = PDFFactura()
    else:
        pdf_gen = None

    # Generar facturas
    print(f"\n🔄 Generando {cantidad} facturas...")
    print()

    # Incluir facturas grandes cada 5 facturas (20% del total)
    tipos_factura = ['general', 'hotel', 'seguro', 'con_descuento', 'compra_grande']
    facturas_por_tipo = {tipo: 0 for tipo in tipos_factura}

    for i in range(cantidad):
        # Seleccionar tipo de factura de forma balanceada
        tipo = tipos_factura[i % len(tipos_factura)]
        facturas_por_tipo[tipo] += 1

        # Generar factura
        factura = factura_gen.generar_factura(tipo_factura=tipo)

        # Generar PDF si está disponible
        pdf_content = None
        if pdf_gen:
            try:
                # Crear PDF en memoria
                pdf_path_temp = f"/tmp/temp_{factura['numero_factura']}.pdf"
                pdf_gen.crear_factura(factura, pdf_path_temp)

                # Leer contenido
                with open(pdf_path_temp, 'rb') as f:
                    pdf_content = f.read()

                # Eliminar temporal
                os.remove(pdf_path_temp)
            except Exception as e:
                print(f"   ⚠️  Error generando PDF: {e}")

        # Exportar al dataset
        json_path, pdf_path = exporter.exportar_factura(factura, pdf_content)

        # Mostrar progreso
        serie = factura['numero_factura']
        emisor = factura['emisor']['razon_social'][:40]
        total = factura['simbolo_moneda'] + f"{factura['total']:,.2f}"

        status = "✅" if pdf_content else "📄"
        print(f"   {status} [{i+1:3d}/{cantidad}] {serie} | {emisor:40s} | {total:>15s}")

    # Estadísticas finales
    print("\n" + "=" * 70)
    print("RESUMEN DEL DATASET".center(70))
    print("=" * 70)

    stats = exporter.obtener_estadisticas()
    print(f"\n📊 Estadísticas:")
    print(f"   • Dataset: {stats['dataset']}")
    print(f"   • Anotaciones (JSON): {stats['anotaciones']}")
    print(f"   • PDFs procesados: {stats['pdfs']}")
    print(f"   • Rechazadas: {stats['rechazadas']}")

    print(f"\n📋 Facturas por tipo:")
    for tipo, cant in facturas_por_tipo.items():
        print(f"   • {tipo.capitalize():15s}: {cant:3d}")

    print(f"\n✅ Dataset completo generado en:")
    print(f"   {dataset_dir}")
    print()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Generar dataset de facturas')
    parser.add_argument('--cantidad', '-n', type=int, default=20,
                       help='Número de facturas a generar (default: 20)')
    parser.add_argument('--sin-pdfs', action='store_true',
                       help='Generar solo JSONs, sin PDFs')

    args = parser.parse_args()

    generar_dataset(
        cantidad=args.cantidad,
        con_pdfs=not args.sin_pdfs
    )
