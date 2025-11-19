#!/usr/bin/env python3
"""
Script de prueba para facturas con elementos visuales
Genera facturas de diferentes tipos para verificar logos, QR, íconos
"""

import sys
import os

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from generator import FacturaGenerator
from pdf_creator import PDFFactura

def main():
    print("=" * 60)
    print("🎨 TEST DE FACTURAS CON ELEMENTOS VISUALES")
    print("=" * 60)
    print()

    # Crear generadores
    gen = FacturaGenerator()

    # Crear generador de PDFs con elementos visuales
    print("📋 Configuración:")
    print("   - Elementos visuales: ACTIVADOS")
    print("   - Logos: UI Avatars API")
    print("   - QR: Generación local")
    print("   - Íconos: Simple Icons + Iconify")
    print()

    pdf_gen = PDFFactura(
        output_dir="facturas_test_visuales",
        use_visual_elements=True  # ACTIVAR elementos visuales
    )

    print("=" * 60)
    print("Generando facturas de prueba...")
    print("=" * 60)
    print()

    # 1. Factura GENERAL (Turismo)
    print("1️⃣  Factura GENERAL - TURISMO DIAS S.A.")
    factura1 = gen.generar_factura(tipo_factura='general', con_credito=False)
    archivo1 = pdf_gen.crear_factura(factura1)
    print(f"   ✅ {archivo1}")
    print(f"   📌 Debe tener: Logo TURISMO (azul), QR, íconos")
    print()

    # 2. Factura HOTEL
    print("2️⃣  Factura HOTEL - Costa del Sol")
    factura2 = gen.generar_factura(tipo_factura='hotel', con_credito=True)
    archivo2 = pdf_gen.crear_factura(factura2)
    print(f"   ✅ {archivo2}")
    print(f"   📌 Debe tener: Logo HOTEL (púrpura), QR, íconos")
    print()

    # 3. Factura SEGURO
    print("3️⃣  Factura SEGURO")
    factura3 = gen.generar_factura(tipo_factura='seguro', con_credito=False)
    archivo3 = pdf_gen.crear_factura(factura3)
    print(f"   ✅ {archivo3}")
    print(f"   📌 Debe tener: Logo SEGURO (verde), QR, íconos")
    print()

    # 4. Factura CON DESCUENTO
    print("4️⃣  Factura CON DESCUENTO - Construcción")
    factura4 = gen.generar_factura(tipo_factura='con_descuento', categoria_items='construccion')
    archivo4 = pdf_gen.crear_factura(factura4)
    print(f"   ✅ {archivo4}")
    print(f"   📌 Debe tener: Logo CONSTRUCCION (naranja), QR, íconos")
    print()

    # 5. Factura SIN elementos visuales (comparación)
    print("5️⃣  Factura SIN elementos visuales (para comparar)")
    pdf_gen_sin = PDFFactura(
        output_dir="facturas_test_visuales",
        use_visual_elements=False  # DESACTIVAR elementos visuales
    )
    factura5 = gen.generar_factura(tipo_factura='general')
    archivo5 = pdf_gen_sin.crear_factura(factura5, filename="factura_SIN_visuales.pdf")
    print(f"   ✅ {archivo5}")
    print(f"   📌 Debe tener: Solo texto, sin logos ni QR")
    print()

    print("=" * 60)
    print("✅ PRUEBAS COMPLETADAS")
    print("=" * 60)
    print()
    print(f"📁 Archivos generados en: facturas_test_visuales/")
    print()
    print("🔍 Verifica que las facturas tengan:")
    print("   ✓ Logo de empresa (esquina superior izquierda)")
    print("   ✓ Código QR (esquina inferior derecha)")
    print("   ✓ Íconos de pago (pie de página)")
    print("   ✓ Íconos de contacto (teléfono, email)")
    print("   ✓ Marca de agua 'FACTURA FICTICIA' (diagonal)")
    print()
    print("💡 Compara la factura #5 (sin visuales) con las demás")
    print("   para ver la diferencia!")
    print()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
