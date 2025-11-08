#!/usr/bin/env python3
"""
Script para validar que las importaciones funcionen correctamente
Este script se ejecutará en el entorno del usuario donde reportlab esté instalado
"""

def main():
    print("=== TEST DE IMPORTACIONES ===\n")
    
    # Test 1: Importar utilidades
    try:
        from src.utils import RUCGenerator, MontoLetras, ItemsGenerator
        print("✓ Utilidades importadas correctamente")
    except ImportError as e:
        print(f"✗ Error importando utilidades: {e}")
        return False
    
    # Test 2: Importar generador
    try:
        from src.generator import FacturaGenerator
        print("✓ Generador importado correctamente")
    except ImportError as e:
        print(f"✗ Error importando generador: {e}")
        return False
    
    # Test 3: Importar PDF creator
    try:
        from src.pdf_creator import PDFFactura
        print("✓ PDF Creator importado correctamente")
    except ImportError as e:
        print(f"✗ Error importando PDF Creator: {e}")
        return False
    
    # Test 4: Importar JSON exporter
    try:
        from src.json_exporter import JSONExporter
        print("✓ JSON Exporter importado correctamente")
    except ImportError as e:
        print(f"✗ Error importando JSON Exporter: {e}")
        return False
    
    print("\n✅ TODAS LAS IMPORTACIONES EXITOSAS\n")
    
    # Test 5: Generar factura y exportar
    print("=== TEST DE FUNCIONALIDAD ===\n")
    
    try:
        gen = FacturaGenerator()
        factura = gen.generar_factura(tipo_factura='hotel')
        print(f"✓ Factura generada: {factura['numero_factura']}")
        print(f"  Tipo: {factura['tipo_factura']}")
        print(f"  Total: {factura['simbolo_moneda']}{factura['total']:.2f}")
        
        # Validar cálculos
        igv_esperado = round(factura['op_gravada'] * 0.18, 2)
        assert abs(igv_esperado - factura['igv']) <= 0.02, "IGV incorrecto"
        print(f"  ✓ IGV válido: {factura['simbolo_moneda']}{factura['igv']:.2f}")
        
        # Exportar JSON
        exporter = JSONExporter(output_dir="test_output")
        archivo_json = exporter.exportar_factura(factura)
        print(f"✓ JSON exportado: {archivo_json}")
        
        # Exportar PDF
        pdf_gen = PDFFactura(output_dir="test_output")
        archivo_pdf = pdf_gen.crear_factura(factura)
        print(f"✓ PDF creado: {archivo_pdf}")
        
        print("\n✅ TODOS LOS TESTS PASARON CORRECTAMENTE")
        return True
        
    except Exception as e:
        print(f"\n✗ Error en tests: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
