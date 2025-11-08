#!/usr/bin/env python3
"""
Script de validación para verificar que todos los cálculos sean correctos
"""
from src.generator import FacturaGenerator
from src.pdf_creator import PDFFactura


def validar_calculo_factura(factura):
    """Valida que todos los cálculos de una factura sean correctos"""
    errores = []

    # Validar suma de items
    suma_items = sum(item['valor_venta'] for item in factura['items'])

    # Si hay cargos por item, sumarlos
    if factura.get('total_cargos', 0) > 0:
        suma_cargos = sum(item.get('cargo_item', 0) for item in factura['items'])
        if abs(suma_cargos - factura['total_cargos']) > 0.02:
            errores.append(f"Suma de cargos no coincide: {suma_cargos} vs {factura['total_cargos']}")

    # Validar IGV (18%)
    igv_esperado = round(factura['op_gravada'] * 0.18, 2)
    if abs(igv_esperado - factura['igv']) > 0.02:
        errores.append(f"IGV incorrecto: esperado {igv_esperado}, obtenido {factura['igv']}")

    # Validar total
    total_esperado = round(
        factura['op_gravada'] +
        factura['igv'] +
        factura['op_exonerada'] +
        factura['op_inafecta'] +
        factura.get('total_cargos', 0) +
        factura.get('otros_cargos', 0),
        2
    )

    if abs(total_esperado - factura['total']) > 0.02:
        errores.append(f"Total incorrecto: esperado {total_esperado}, obtenido {factura['total']}")

    # Validar cuotas si es a crédito
    if factura['con_credito'] and factura['cuotas']:
        suma_cuotas = sum(cuota['monto'] for cuota in factura['cuotas'])
        if abs(suma_cuotas - factura['total']) > 0.02:
            errores.append(f"Suma de cuotas no coincide: {suma_cuotas} vs {factura['total']}")

    return errores


def main():
    print("="*70)
    print("TEST DE VALIDACIÓN - Generador de Facturas")
    print("="*70)

    gen = FacturaGenerator()
    pdf_gen = PDFFactura(output_dir="test_validation")

    tipos = ['general', 'hotel', 'seguro', 'con_descuento']
    total_errores = 0
    total_pruebas = 0

    for tipo in tipos:
        print(f"\n{'='*70}")
        print(f"Probando tipo: {tipo.upper()}")
        print(f"{'='*70}")

        for i in range(5):  # 5 facturas de cada tipo
            total_pruebas += 1

            try:
                # Generar factura
                factura = gen.generar_factura(tipo_factura=tipo)

                # Validar cálculos
                errores = validar_calculo_factura(factura)

                if errores:
                    print(f"\n✗ Factura {factura['numero_factura']} - ERRORES:")
                    for error in errores:
                        print(f"    - {error}")
                    total_errores += len(errores)
                else:
                    print(f"✓ Factura {factura['numero_factura']} - OK (Total: {factura['simbolo_moneda']}{factura['total']:.2f})")

                # Generar PDF
                pdf_gen.crear_factura(factura)

            except Exception as e:
                print(f"✗ Error generando factura: {str(e)}")
                import traceback
                traceback.print_exc()
                total_errores += 1

    print(f"\n{'='*70}")
    print(f"RESUMEN DE VALIDACIÓN")
    print(f"{'='*70}")
    print(f"Total de pruebas: {total_pruebas}")
    print(f"Pruebas exitosas: {total_pruebas - (total_errores if total_errores < total_pruebas else total_pruebas)}")
    print(f"Errores encontrados: {total_errores}")

    if total_errores == 0:
        print(f"\n✅ TODAS LAS VALIDACIONES PASARON CORRECTAMENTE!")
    else:
        print(f"\n⚠️  Se encontraron {total_errores} errores")

    print(f"{'='*70}")


if __name__ == "__main__":
    main()
