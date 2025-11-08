#!/usr/bin/env python3
"""
Ejemplo de uso del generador de facturas

Este script muestra cómo usar las diferentes funciones del sistema
"""

# Primero asegúrate de instalar las dependencias:
# pip install -r requirements.txt

from src.generator import FacturaGenerator
from src.pdf_creator import PDFFactura
from src.utils import RUCGenerator, MontoLetras, DatosPersonas


def ejemplo_1_generar_factura_simple():
    """Ejemplo 1: Generar una factura simple"""
    print("="*60)
    print("EJEMPLO 1: Generar una factura simple")
    print("="*60)

    gen = FacturaGenerator()
    factura = gen.generar_factura()

    print(f"\nFactura: {factura['numero_factura']}")
    print(f"Fecha: {factura['fecha_emision'].strftime('%d/%m/%Y')}")
    print(f"Emisor: {factura['emisor']['razon_social']}")
    print(f"Cliente: {factura['receptor']['razon_social']}")
    print(f"Total: {factura['simbolo_moneda']}{factura['total']:.2f}")
    print(f"Son: {factura['total_letras']}")
    print()


def ejemplo_2_factura_construccion():
    """Ejemplo 2: Generar factura de construcción"""
    print("="*60)
    print("EJEMPLO 2: Factura de construcción")
    print("="*60)

    gen = FacturaGenerator()
    factura = gen.generar_factura(
        categoria_items='construccion',
        num_items=5,
        moneda='PEN',
        con_credito=False
    )

    print(f"\nFactura: {factura['numero_factura']}")
    print(f"Categoría: Construcción")
    print(f"Moneda: {factura['nombre_moneda']}")
    print(f"\nItems:")
    for item in factura['items']:
        print(f"  - {item['descripcion']}")
        print(f"    {item['cantidad']} {item['unidad']} x {factura['simbolo_moneda']}{item['precio_unitario']:.2f} = {factura['simbolo_moneda']}{item['valor_venta']:.2f}")

    print(f"\nSubtotal: {factura['simbolo_moneda']}{factura['op_gravada']:.2f}")
    print(f"IGV 18%: {factura['simbolo_moneda']}{factura['igv']:.2f}")
    print(f"TOTAL: {factura['simbolo_moneda']}{factura['total']:.2f}")
    print()


def ejemplo_3_factura_credito():
    """Ejemplo 3: Factura a crédito con cuotas"""
    print("="*60)
    print("EJEMPLO 3: Factura a crédito")
    print("="*60)

    gen = FacturaGenerator()
    factura = gen.generar_factura(
        categoria_items='servicios',
        con_credito=True
    )

    print(f"\nFactura: {factura['numero_factura']}")
    print(f"Forma de pago: {factura['forma_pago']}")
    print(f"Total: {factura['simbolo_moneda']}{factura['total']:.2f}")

    print(f"\nCuotas:")
    suma = 0
    for cuota in factura['cuotas']:
        print(f"  Cuota {cuota['numero']}: {factura['simbolo_moneda']}{cuota['monto']:.2f} - Vencimiento: {cuota['fecha_vencimiento'].strftime('%d/%m/%Y')}")
        suma += cuota['monto']

    print(f"\nSuma de cuotas: {factura['simbolo_moneda']}{suma:.2f}")
    print(f"Total factura: {factura['simbolo_moneda']}{factura['total']:.2f}")
    print(f"Diferencia: {factura['simbolo_moneda']}{abs(suma - factura['total']):.2f}")
    print()


def ejemplo_4_generar_pdf():
    """Ejemplo 4: Generar PDF de factura"""
    print("="*60)
    print("EJEMPLO 4: Generar PDF")
    print("="*60)

    gen = FacturaGenerator()
    pdf_gen = PDFFactura(output_dir="ejemplos_pdf")

    factura = gen.generar_factura(
        categoria_items='comida',
        num_items=8,
        moneda='USD',
        con_credito=True
    )

    archivo = pdf_gen.crear_factura(factura)
    print(f"\nPDF generado: {archivo}")
    print(f"Factura: {factura['numero_factura']}")
    print(f"Total: {factura['simbolo_moneda']}{factura['total']:.2f}")
    print()


def ejemplo_5_utilidades():
    """Ejemplo 5: Usar utilidades directamente"""
    print("="*60)
    print("EJEMPLO 5: Utilidades")
    print("="*60)

    # Generar RUC
    print("\nRUCs generados:")
    for _ in range(3):
        print(f"  {RUCGenerator.generar_ruc()}")

    # Convertir montos a letras
    print("\nMontos a letras:")
    montos = [1234.56, 999.99, 10000.00]
    for monto in montos:
        print(f"  {monto} -> {MontoLetras.convertir(monto, 'SOLES')}")

    # Generar datos de personas
    print("\nDatos de personas:")
    for _ in range(2):
        print(f"  {DatosPersonas.generar_nombre_persona()}")
        print(f"  {DatosPersonas.generar_razon_social()}")
        print(f"  {DatosPersonas.generar_direccion()}")
        print()


def ejemplo_6_batch():
    """Ejemplo 6: Generar múltiples facturas"""
    print("="*60)
    print("EJEMPLO 6: Generación en lote")
    print("="*60)

    gen = FacturaGenerator()
    pdf_gen = PDFFactura(output_dir="facturas_batch")

    cantidad = 10
    print(f"\nGenerando {cantidad} facturas...\n")

    for i in range(cantidad):
        factura = gen.generar_factura()
        archivo = pdf_gen.crear_factura(factura)
        print(f"  [{i+1}/{cantidad}] {factura['numero_factura']} -> {archivo}")

    print(f"\nTodas las facturas generadas en: facturas_batch/")
    print()


def main():
    """Ejecutar todos los ejemplos"""
    print("\n" + "="*60)
    print("EJEMPLOS DE USO - GENERADOR DE FACTURAS")
    print("="*60 + "\n")

    try:
        ejemplo_1_generar_factura_simple()
        input("Presiona ENTER para continuar...")

        ejemplo_2_factura_construccion()
        input("Presiona ENTER para continuar...")

        ejemplo_3_factura_credito()
        input("Presiona ENTER para continuar...")

        ejemplo_4_generar_pdf()
        input("Presiona ENTER para continuar...")

        ejemplo_5_utilidades()
        input("Presiona ENTER para continuar...")

        ejemplo_6_batch()

        print("="*60)
        print("TODOS LOS EJEMPLOS COMPLETADOS")
        print("="*60)

    except KeyboardInterrupt:
        print("\n\nEjemplos interrumpidos.")
    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
