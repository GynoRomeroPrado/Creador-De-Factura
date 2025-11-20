"""
Test de Variabilidad de Layouts
Genera facturas con los 5 layouts diferentes extraídos de facturas reales
"""

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from src.generator import FacturaGenerator
from src.pdf_creator import PDFFactura
from src.pdf_layouts import listar_layouts, obtener_info_layout


def main():
    print("=" * 70)
    print("🎨 TEST DE VARIABILIDAD DE LAYOUTS")
    print("=" * 70)
    print()
    print("Generando facturas con 5 layouts diferentes basados en facturas reales")
    print()

    # Crear directorio de salida
    output_dir = "facturas_test_layouts"
    os.makedirs(output_dir, exist_ok=True)

    # Generador de datos
    gen = FacturaGenerator()

    # Obtener lista de layouts disponibles
    layouts = listar_layouts()
    print(f"📋 Layouts disponibles: {len(layouts)}")
    print()

    # Generar una factura para cada layout
    facturas_generadas = []

    for i, layout_name in enumerate(layouts, 1):
        info = obtener_info_layout(layout_name)

        print(f"{i}️⃣  Layout: {info['nombre']} ({info['industria']})")
        print(f"   Clave: {layout_name}")

        # Determinar tipo de factura según industria
        tipo_map = {
            "Hotelería": "hotel",
            "Hotelería Premium": "hotel",
            "Hotelería Corporativa": "hotel",
            "Minería / Construcción": "construccion",
            "Seguros": "seguro"
        }
        tipo_factura = tipo_map.get(info['industria'], 'general')

        # Generar datos de factura
        if tipo_factura == "hotel":
            factura_data = gen.generar_factura(tipo_factura='hotel', con_credito=True)
        elif tipo_factura == "construccion":
            factura_data = gen.generar_factura(tipo_factura='general', categoria_items='construccion', con_credito=False)
        elif tipo_factura == "seguro":
            factura_data = gen.generar_factura(tipo_factura='seguro', con_credito=False)
        else:
            factura_data = gen.generar_factura(tipo_factura='general', con_credito=True)

        # Crear PDF con layout específico
        pdf_gen = PDFFactura(
            output_dir=output_dir,
            use_visual_elements=True,
            layout_name=layout_name
        )

        # Nombre de archivo personalizado
        filename = f"Layout_{i}_{layout_name}_{factura_data['serie']}_{factura_data['numero']}.pdf"
        archivo = pdf_gen.crear_factura(factura_data, filename=filename)

        facturas_generadas.append({
            'numero': i,
            'layout': info['nombre'],
            'industria': info['industria'],
            'archivo': archivo
        })

        print(f"   ✅ {os.path.basename(archivo)}")
        print()

    # Resumen final
    print("=" * 70)
    print("✅ PRUEBAS COMPLETADAS")
    print("=" * 70)
    print()
    print(f"📁 Archivos generados en: {output_dir}/")
    print()

    print("📊 Resumen de layouts generados:")
    print()
    for factura in facturas_generadas:
        print(f"   {factura['numero']}. {factura['layout']} ({factura['industria']})")
        print(f"      → {os.path.basename(factura['archivo'])}")

    print()
    print("=" * 70)
    print("🔍 VERIFICACIÓN DE VARIABILIDAD")
    print("=" * 70)
    print()
    print("Abre los PDFs y verifica que cada uno tiene:")
    print()
    print("   ✓ Logo en DIFERENTES posiciones")
    print("   ✓ Código QR en DIFERENTES ubicaciones")
    print("   ✓ Colores de encabezado DIFERENTES")
    print("   ✓ Colores de tabla DIFERENTES")
    print("   ✓ Fuentes con DIFERENTES tamaños y pesos")
    print("   ✓ Marca de agua con DIFERENTES rotaciones")
    print("   ✓ Fondos con DIFERENTES tonalidades (blanco, gris claro, gris medio)")
    print()
    print("💡 Comparación esperada:")
    print()
    print("   1. Costa del Sol:")
    print("      - Logo: esquina inferior izquierda (rotado)")
    print("      - Fondo: Blanco")
    print("      - Encabezado: Azul marino oscuro (#1A237E)")
    print("      - Tabla: Azul índigo (#283593)")
    print()
    print("   2. Casa Andina:")
    print("      - Logo: esquina superior izquierda")
    print("      - Fondo: Blanco")
    print("      - Encabezado: Blanco con borde")
    print("      - Tabla: Gris muy claro (#F5F5F5)")
    print()
    print("   3. Estelar:")
    print("      - Logo: esquina superior izquierda")
    print("      - Fondo: Gris muy claro (#FAFAFA)")
    print("      - Encabezado: Azul corporativo (#01579B)")
    print("      - Tabla: Azul (#0288D1)")
    print()
    print("   4. Yanacocha:")
    print("      - Logo: esquina superior izquierda")
    print("      - Fondo: Gris (#E8E8E8)")
    print("      - Encabezado: Gris oscuro (#424242)")
    print("      - Tabla: Gris medio (#616161)")
    print("      - QR: esquina inferior IZQUIERDA (diferente)")
    print()
    print("   5. Pacífico Seguros:")
    print("      - Logo: esquina superior izquierda (más pequeño)")
    print("      - Fondo: Blanco")
    print("      - Encabezado: Verde (#2E7D32)")
    print("      - Tabla: Verde (#4CAF50)")
    print("      - QR: inferior CENTRADO (único)")
    print()
    print("=" * 70)
    print()
    print("✅ Para Donut, esta variabilidad es CRÍTICA:")
    print()
    print("   - Con layouts variables → Donut aprende ESTRUCTURA (75-85% precisión)")
    print("   - Sin variabilidad → Donut memoriza POSICIONES (30-40% precisión)")
    print()
    print("🎯 Siguiente paso: Entrena Donut con estos PDFs diversos!")
    print()


if __name__ == "__main__":
    main()
