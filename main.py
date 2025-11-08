#!/usr/bin/env python3
"""
Generador de Facturas Ficticias - Punto de entrada principal

Uso:
    python main.py --cantidad 50 --output facturas_generadas/
    python main.py --analizar --input facturas_originales/
"""
import argparse
import os
import sys
from pathlib import Path
from src.generator import FacturaGenerator
from src.pdf_creator import PDFFactura


def generar_facturas(cantidad: int, output_dir: str, verbose: bool = True):
    """
    Genera múltiples facturas ficticias

    Args:
        cantidad: Número de facturas a generar
        output_dir: Directorio de salida
        verbose: Mostrar progreso
    """
    if verbose:
        print(f"{'='*60}")
        print(f"Generador de Facturas Ficticias")
        print(f"{'='*60}")
        print(f"Cantidad a generar: {cantidad}")
        print(f"Directorio de salida: {output_dir}")
        print(f"{'='*60}\n")

    # Crear generadores
    gen_factura = FacturaGenerator()
    gen_pdf = PDFFactura(output_dir=output_dir)

    facturas_generadas = []

    for i in range(cantidad):
        try:
            if verbose:
                print(f"[{i+1}/{cantidad}] Generando factura...", end=" ")

            # Generar factura con parámetros aleatorios variados
            # Variar categorías de items
            categorias = ['construccion', 'comida', 'servicios', None]  # None = mixto
            categoria = categorias[i % len(categorias)]

            # Variar número de items
            num_items = None  # Aleatorio entre 1-10

            # Variar moneda
            monedas = ['PEN', 'USD', 'EUR', None]  # None = aleatorio
            moneda = monedas[i % len(monedas)]

            # Variar crédito
            con_credito = (i % 3 == 0)  # 1 de cada 3 a crédito

            # Generar datos de factura
            factura = gen_factura.generar_factura(
                categoria_items=categoria,
                num_items=num_items,
                moneda=moneda,
                con_credito=con_credito
            )

            # Crear PDF
            archivo = gen_pdf.crear_factura(factura)

            facturas_generadas.append(archivo)

            if verbose:
                print(f"✓ {factura['numero_factura']} - {os.path.basename(archivo)}")

        except Exception as e:
            if verbose:
                print(f"✗ Error: {str(e)}")
            continue

    if verbose:
        print(f"\n{'='*60}")
        print(f"Proceso completado:")
        print(f"  - Facturas generadas: {len(facturas_generadas)}/{cantidad}")
        print(f"  - Ubicación: {output_dir}")
        print(f"{'='*60}")

    return facturas_generadas


def analizar_facturas_originales(input_dir: str):
    """
    Analiza facturas originales en el directorio de entrada

    Args:
        input_dir: Directorio con facturas originales
    """
    print(f"{'='*60}")
    print(f"Análisis de Facturas Originales")
    print(f"{'='*60}")
    print(f"Directorio: {input_dir}")
    print(f"{'='*60}\n")

    if not os.path.exists(input_dir):
        print(f"Error: El directorio '{input_dir}' no existe.")
        return

    # Buscar archivos PDF e imágenes
    extensiones = ['.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.tif']
    archivos = []

    for ext in extensiones:
        archivos.extend(Path(input_dir).rglob(f"*{ext}"))

    if not archivos:
        print(f"No se encontraron facturas en '{input_dir}'")
        print(f"Extensiones buscadas: {', '.join(extensiones)}")
        return

    print(f"Se encontraron {len(archivos)} archivos:\n")
    for i, archivo in enumerate(archivos, 1):
        print(f"  {i}. {archivo.name} ({archivo.suffix.upper()[1:]})")

    print(f"\n{'='*60}")
    print("NOTA: El análisis detallado de PDFs e imágenes requiere")
    print("herramientas adicionales (OCR, extracción de PDF).")
    print("Para una implementación completa, se recomienda:")
    print("  - PyPDF2 / pdfplumber para PDFs")
    print("  - Tesseract OCR para imágenes")
    print("  - OpenCV para procesamiento de imágenes")
    print(f"{'='*60}")

    return archivos


def main():
    parser = argparse.ArgumentParser(
        description="Generador de Facturas Ficticias",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:

  # Generar 50 facturas
  python main.py --cantidad 50

  # Generar 100 facturas en directorio específico
  python main.py --cantidad 100 --output ./mis_facturas/

  # Analizar facturas originales
  python main.py --analizar --input ./facturas_originales/

  # Generar facturas basándose en análisis previo
  python main.py --cantidad 200 --input ./facturas_originales/ --output ./generadas/
        """
    )

    parser.add_argument(
        '--cantidad',
        type=int,
        default=10,
        help='Cantidad de facturas a generar (default: 10)'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='facturas_generadas',
        help='Directorio de salida para facturas generadas (default: facturas_generadas)'
    )

    parser.add_argument(
        '--input',
        type=str,
        default='facturas_originales',
        help='Directorio con facturas originales para análisis (default: facturas_originales)'
    )

    parser.add_argument(
        '--analizar',
        action='store_true',
        help='Analizar facturas originales antes de generar'
    )

    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Modo silencioso (sin output detallado)'
    )

    args = parser.parse_args()

    verbose = not args.quiet

    try:
        # Si se solicita análisis, hacerlo primero
        if args.analizar:
            analizar_facturas_originales(args.input)
            print("\n")

        # Generar facturas
        generar_facturas(
            cantidad=args.cantidad,
            output_dir=args.output,
            verbose=verbose
        )

    except KeyboardInterrupt:
        print("\n\nProceso interrumpido por el usuario.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
