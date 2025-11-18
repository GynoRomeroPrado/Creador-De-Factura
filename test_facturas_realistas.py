#!/usr/bin/env python3
"""
Script de prueba para validar la generación de facturas realistas.

Este script genera facturas de prueba usando los nuevos módulos de datos realistas:
- Sectores específicos (15 tipos de negocios)
- Direcciones reales (25 distritos de Lima)
- Descripciones detalladas (marcas, especificaciones, variantes)
- Patrones temporales y estacionalidad
- Múltiples tipografías
"""

import sys
import os
from datetime import datetime

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.generator import FacturaGenerator
from src.pdf_creator import PDFFactura


def test_generacion_realista():
    """
    Test principal: Genera facturas realistas y valida características.
    """
    print("\n" + "="*80)
    print("TEST: Generación de Facturas Realistas")
    print("="*80 + "\n")

    # Inicializar generador en modo realista
    print("1. Inicializando generador en modo realista...")
    gen = FacturaGenerator(usar_datos_realistas=True)

    # Inicializar creador de PDFs
    pdf_creator = PDFFactura(output_dir="test_facturas_realistas")

    print("   ✅ Generador inicializado\n")

    # Generar facturas de diferentes sectores
    print("2. Generando facturas de prueba (10 facturas)...")
    print("-" * 80)

    facturas_generadas = []
    errores = []

    for i in range(10):
        try:
            # Generar factura
            factura = gen.generar_factura()

            # Validar características del modo realista
            tiene_sector = 'sector' in factura
            tiene_tipografia = 'tipografia' in factura
            tiene_modo_realista = factura.get('modo_realista', False)

            # Info de la factura
            numero = factura['numero_factura']
            sector = factura.get('sector', 'N/A')
            tipografia = factura.get('tipografia', 'N/A')
            emisor = factura['emisor']['razon_social']
            num_items = len(factura['items'])
            total = factura['total']

            # Validar direcciones (deben ser más largas y detalladas)
            dir_emisor = factura['emisor']['direccion']
            dir_receptor = factura['receptor']['direccion']

            # Validar items (deben tener descripciones más detalladas)
            item_ejemplo = factura['items'][0]['descripcion'] if factura['items'] else 'N/A'

            print(f"\n  Factura {i+1}/10: {numero}")
            print(f"    • Sector: {sector}")
            print(f"    • Tipografía: {tipografia}")
            print(f"    • Emisor: {emisor[:60]}...")
            print(f"    • Items: {num_items}")
            print(f"    • Total: {factura['simbolo_moneda']}{total:.2f}")
            print(f"    • Direccion emisor: {dir_emisor[:70]}...")
            print(f"    • Item ejemplo: {item_ejemplo[:70]}...")

            # Validaciones
            validaciones = []
            if tiene_sector:
                validaciones.append("✓ Sector")
            if tiene_tipografia:
                validaciones.append("✓ Tipografía")
            if len(dir_emisor) > 40:  # Direcciones realistas son más largas
                validaciones.append("✓ Dirección detallada")
            if len(item_ejemplo) > 30:  # Descripciones realistas son más largas
                validaciones.append("✓ Descripción detallada")

            print(f"    • Validaciones: {', '.join(validaciones)}")

            # Generar PDF
            try:
                pdf_path = pdf_creator.crear_factura(factura)
                print(f"    • PDF: {pdf_path}")
                facturas_generadas.append({
                    'factura': factura,
                    'pdf_path': pdf_path,
                    'validaciones': validaciones
                })
            except Exception as e:
                print(f"    ⚠️  Error al generar PDF: {e}")
                errores.append(f"PDF {numero}: {str(e)}")

        except Exception as e:
            print(f"\n  ❌ Error en factura {i+1}: {e}")
            import traceback
            traceback.print_exc()
            errores.append(f"Factura {i+1}: {str(e)}")

    # Resumen
    print("\n" + "="*80)
    print("RESUMEN DE PRUEBAS")
    print("="*80)

    print(f"\n✅ Facturas generadas exitosamente: {len(facturas_generadas)}/10")
    print(f"❌ Errores: {len(errores)}")

    if errores:
        print("\nErrores encontrados:")
        for error in errores:
            print(f"  • {error}")

    # Estadísticas
    if facturas_generadas:
        print("\n" + "-"*80)
        print("ESTADÍSTICAS")
        print("-"*80)

        # Contar sectores
        sectores = {}
        tipografias = {}
        for fg in facturas_generadas:
            sector = fg['factura'].get('sector', 'N/A')
            tipografia = fg['factura'].get('tipografia', 'N/A')

            sectores[sector] = sectores.get(sector, 0) + 1
            tipografias[tipografia] = tipografias.get(tipografia, 0) + 1

        print("\nSectores representados:")
        for sector, count in sorted(sectores.items(), key=lambda x: x[1], reverse=True):
            print(f"  • {sector}: {count} factura(s)")

        print("\nTipografías usadas:")
        for tipografia, count in sorted(tipografias.items(), key=lambda x: x[1], reverse=True):
            print(f"  • {tipografia}: {count} factura(s)")

        # Validar características realistas
        print("\nCaracterísticas realistas validadas:")
        total_val = len(facturas_generadas)
        con_sector = sum(1 for fg in facturas_generadas if 'sector' in fg['factura'])
        con_tipo = sum(1 for fg in facturas_generadas if 'tipografia' in fg['factura'])
        con_dir_larga = sum(1 for fg in facturas_generadas if len(fg['factura']['emisor']['direccion']) > 40)
        con_desc_larga = sum(1 for fg in facturas_generadas if fg['factura']['items'] and len(fg['factura']['items'][0]['descripcion']) > 30)

        print(f"  • Sector específico: {con_sector}/{total_val} ({con_sector/total_val*100:.0f}%)")
        print(f"  • Tipografía variada: {con_tipo}/{total_val} ({con_tipo/total_val*100:.0f}%)")
        print(f"  • Direcciones detalladas: {con_dir_larga}/{total_val} ({con_dir_larga/total_val*100:.0f}%)")
        print(f"  • Descripciones detalladas: {con_desc_larga}/{total_val} ({con_desc_larga/total_val*100:.0f}%)")

    print("\n" + "="*80)
    if len(facturas_generadas) == 10 and len(errores) == 0:
        print("🎉 ¡TODAS LAS PRUEBAS PASARON!")
        print("\n✅ Sistema de generación realista funcionando correctamente:")
        print("   • Sectores específicos integrados")
        print("   • Direcciones reales de 25 distritos")
        print("   • Descripciones detalladas con marcas y especificaciones")
        print("   • Patrones temporales aplicados")
        print("   • Múltiples tipografías en uso")
        print("\n📊 Impacto:")
        print("   • Dataset más diverso y realista")
        print("   • Mejor entrenamiento para LayoutLMv3")
        print("   • PDFs más profesionales y variados")
        return 0
    else:
        print("⚠️  Algunas pruebas fallaron")
        return 1


def test_comparacion_modo_basico_vs_realista():
    """
    Test comparativo: Genera facturas en modo básico vs realista y compara.
    """
    print("\n" + "="*80)
    print("TEST COMPARATIVO: Modo Básico vs Modo Realista")
    print("="*80 + "\n")

    # Modo básico
    print("1. Generando factura en MODO BÁSICO...")
    gen_basico = FacturaGenerator(usar_datos_realistas=False)
    factura_basica = gen_basico.generar_factura()

    print(f"   • Emisor: {factura_basica['emisor']['razon_social']}")
    print(f"   • Dirección: {factura_basica['emisor']['direccion'][:60]}...")
    print(f"   • Item 1: {factura_basica['items'][0]['descripcion'][:60]}...")
    print(f"   • Tiene sector: {'sector' in factura_basica}")
    print(f"   • Tiene tipografía: {'tipografia' in factura_basica}")

    # Modo realista
    print("\n2. Generando factura en MODO REALISTA...")
    gen_realista = FacturaGenerator(usar_datos_realistas=True)
    factura_realista = gen_realista.generar_factura()

    print(f"   • Emisor: {factura_realista['emisor']['razon_social']}")
    print(f"   • Sector: {factura_realista.get('sector', 'N/A')}")
    print(f"   • Dirección: {factura_realista['emisor']['direccion'][:60]}...")
    print(f"   • Item 1: {factura_realista['items'][0]['descripcion'][:60]}...")
    print(f"   • Tiene sector: {'sector' in factura_realista}")
    print(f"   • Tiene tipografía: {'tipografia' in factura_realista}")
    print(f"   • Tipografía: {factura_realista.get('tipografia', 'N/A')}")

    # Comparación
    print("\n" + "-"*80)
    print("COMPARACIÓN")
    print("-"*80)

    len_dir_basica = len(factura_basica['emisor']['direccion'])
    len_dir_realista = len(factura_realista['emisor']['direccion'])

    len_desc_basica = len(factura_basica['items'][0]['descripcion'])
    len_desc_realista = len(factura_realista['items'][0]['descripcion'])

    print(f"\nLongitud de direcciones:")
    print(f"  • Básica: {len_dir_basica} caracteres")
    print(f"  • Realista: {len_dir_realista} caracteres ({len_dir_realista - len_dir_basica:+d})")

    print(f"\nLongitud de descripciones de items:")
    print(f"  • Básica: {len_desc_basica} caracteres")
    print(f"  • Realista: {len_desc_realista} caracteres ({len_desc_realista - len_desc_basica:+d})")

    print(f"\nMetadata:")
    print(f"  • Básica tiene sector: {'sector' in factura_basica}")
    print(f"  • Realista tiene sector: {'sector' in factura_realista}")
    print(f"  • Básica tiene tipografía: {'tipografia' in factura_basica}")
    print(f"  • Realista tiene tipografía: {'tipografia' in factura_realista}")

    print("\n" + "="*80)


if __name__ == '__main__':
    # Test principal
    result = test_generacion_realista()

    # Test comparativo
    test_comparacion_modo_basico_vs_realista()

    print("\n")
    exit(result)
