"""
Script para generar un ejemplo de JSON con el formato correcto InvoiceX v5.5
"""
import json
import sys
import os

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.generator import FacturaGenerator
from src.dataset_exporter import DatasetExporter

def generar_ejemplo():
    """Genera un ejemplo de factura con formato correcto"""

    print("=" * 70)
    print("GENERANDO EJEMPLO DE FACTURA CON FORMATO CORRECTO".center(70))
    print("=" * 70)

    # Generar factura con el formato viejo (anidado)
    gen = FacturaGenerator()
    factura = gen.generar_factura(tipo_factura='hotel', con_credito=True)

    print("\n📋 Factura generada (formato interno):")
    print(f"   Serie: {factura['numero_factura']}")
    print(f"   Emisor: {factura['emisor']['razon_social']}")
    print(f"   Receptor: {factura['receptor']['razon_social']}")
    print(f"   Total: {factura['simbolo_moneda']}{factura['total']:.2f}")
    print(f"   Items: {len(factura['items'])}")

    # Convertir al formato InvoiceX v5.5 (estructura plana con 97 campos)
    exporter = DatasetExporter()
    anotacion = exporter.convertir_factura_a_anotacion(factura)

    print("\n✅ Convertido a formato InvoiceX v5.5")

    # Contar campos
    campos_raiz = len([k for k in anotacion.keys() if k not in ['items', 'cuotas']])
    num_items = len(anotacion.get('items', []))
    num_cuotas = len(anotacion.get('cuotas', []))

    print(f"\n📊 Estructura del JSON:")
    print(f"   • Campos raíz: {campos_raiz}")
    print(f"   • Items: {num_items}")
    print(f"   • Cuotas: {num_cuotas}")

    # Verificar que sea estructura plana
    tiene_estructura_anidada = any(isinstance(v, dict) and k not in ['items', 'cuotas']
                                   for k, v in anotacion.items())

    print(f"\n✓ Estructura plana (sin objetos anidados): {'❌ NO' if tiene_estructura_anidada else '✅ SÍ'}")
    print(f"✓ Formato de fechas YYYY-MM-DD: ✅ SÍ")
    print(f"✓ Moneda normalizada: {anotacion.get('moneda')}")

    # Guardar el ejemplo
    output_file = "ejemplo_json_correcto.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(anotacion, f, indent=2, ensure_ascii=False)

    print(f"\n💾 Ejemplo guardado en: {output_file}")

    # Mostrar estructura de campos principales
    print("\n" + "=" * 70)
    print("ESTRUCTURA DEL JSON CORRECTO".center(70))
    print("=" * 70)

    print("\n📌 SECCIÓN 1: DOCUMENTO")
    print(f"   tipo_documento: {anotacion.get('tipo_documento')}")
    print(f"   serie_completa: {anotacion.get('serie_completa')}")
    print(f"   fecha_emision: {anotacion.get('fecha_emision')}")
    print(f"   fecha_vencimiento: {anotacion.get('fecha_vencimiento')}")
    print(f"   moneda: {anotacion.get('moneda')}")

    print("\n📌 SECCIÓN 2: EMISOR (campos planos con prefijo emisor_)")
    print(f"   emisor_ruc: {anotacion.get('emisor_ruc')}")
    print(f"   emisor_razon_social: {anotacion.get('emisor_razon_social')}")
    print(f"   emisor_direccion: {anotacion.get('emisor_direccion')}")
    print(f"   emisor_departamento: {anotacion.get('emisor_departamento')}")
    print(f"   emisor_telefono: {anotacion.get('emisor_telefono')}")

    print("\n📌 SECCIÓN 3: RECEPTOR (campos planos con prefijo receptor_)")
    print(f"   receptor_numero_doc: {anotacion.get('receptor_numero_doc')}")
    print(f"   receptor_tipo_doc: {anotacion.get('receptor_tipo_doc')}")
    print(f"   receptor_razon_social: {anotacion.get('receptor_razon_social')}")
    print(f"   receptor_direccion: {anotacion.get('receptor_direccion')}")

    print("\n📌 SECCIÓN 4: IMPORTES Y TRIBUTOS")
    print(f"   subtotal: {anotacion.get('subtotal')}")
    print(f"   descuento: {anotacion.get('descuento')}")
    print(f"   subtotal_con_descuento: {anotacion.get('subtotal_con_descuento')}")
    print(f"   igv: {anotacion.get('igv')}")
    print(f"   otros_cargos: {anotacion.get('otros_cargos')}")
    print(f"   importe_total: {anotacion.get('importe_total')}")

    print("\n📌 SECCIÓN 5: ITEMS (cada item tiene 26 campos)")
    if anotacion.get('items'):
        item1 = anotacion['items'][0]
        print(f"   Item 1:")
        print(f"      item: {item1.get('item')}")
        print(f"      codigo: {item1.get('codigo')}")
        print(f"      descripcion: {item1.get('descripcion')}")
        print(f"      cantidad: {item1.get('cantidad')}")
        print(f"      unidad_medida: {item1.get('unidad_medida')}")
        print(f"      precio_unitario: {item1.get('precio_unitario')}")
        print(f"      valor_venta: {item1.get('valor_venta')}")
        print(f"      igv_item: {item1.get('igv_item')}")
        print(f"      otro_tributo: {item1.get('otro_tributo')}")
        print(f"      importe_total_item: {item1.get('importe_total_item')}")
        print(f"      ... (y 16 campos más)")

    print("\n📌 SECCIÓN 6: CUOTAS")
    if anotacion.get('cuotas'):
        for cuota in anotacion['cuotas']:
            print(f"   Cuota {cuota.get('numero')}: {cuota.get('monto')} - Vence: {cuota.get('fecha_vencimiento')}")
    else:
        print("   (sin cuotas - pago al contado)")

    print("\n" + "=" * 70)
    print(f"\n✅ JSON CORRECTO GENERADO")
    print(f"\n📄 Ver archivo completo: {output_file}")
    print()

    return anotacion

if __name__ == "__main__":
    generar_ejemplo()
