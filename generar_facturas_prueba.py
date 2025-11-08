#!/usr/bin/env python3
"""
Generador de facturas de prueba
Genera 2 facturas: 1 de hotel y 1 tipo Yanacocha (servicios/construcción)
"""
import sys
import json
import os
from datetime import datetime

# Agregar directorio al path
sys.path.insert(0, '/home/user/Creador-De-Factura')

# Importar directamente sin pasar por __init__
import importlib.util

# Cargar generator.py
spec = importlib.util.spec_from_file_location("generator", "/home/user/Creador-De-Factura/src/generator.py")
generator_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(generator_module)
FacturaGenerator = generator_module.FacturaGenerator

# Cargar json_exporter.py
spec = importlib.util.spec_from_file_location("json_exporter", "/home/user/Creador-De-Factura/src/json_exporter.py")
json_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(json_module)
JSONExporter = json_module.JSONExporter

print("=" * 80)
print("GENERANDO FACTURAS DE PRUEBA")
print("=" * 80)

# Crear generadores
gen = FacturaGenerator()
json_exporter = JSONExporter(output_dir="facturas_generadas/JSONs")

facturas_generadas = []

# ============================================================================
# FACTURA 1: HOTEL
# ============================================================================
print("\n[1/2] Generando factura de HOTEL...")

factura_hotel = gen.generar_factura(
    tipo_factura='hotel',
    categoria_items='hoteles',
    moneda='PEN',
    con_credito=True
)

facturas_generadas.append(factura_hotel)

print(f"✓ Factura Hotel generada: {factura_hotel['numero_factura']}")
print(f"  Emisor: {factura_hotel['emisor']['razon_social']}")
print(f"  Fecha: {factura_hotel['fecha_emision'].strftime('%d/%m/%Y')}")
print(f"  Total: {factura_hotel['simbolo_moneda']}{factura_hotel['total']:.2f}")

if factura_hotel.get('datos_hotel'):
    hotel_info = factura_hotel['datos_hotel']
    print(f"  Check-in: {hotel_info['checkin'].strftime('%d/%m/%Y')}")
    print(f"  Check-out: {hotel_info['checkout'].strftime('%d/%m/%Y')}")
    print(f"  Noches: {hotel_info['noches']}")
    print(f"  Huésped: {hotel_info['huesped']}")
    print(f"  Reserva: {hotel_info['reserva']}")

print(f"  Items: {len(factura_hotel['items'])} items")
for item in factura_hotel['items']:
    cargo_txt = f" + Cargo: {factura_hotel['simbolo_moneda']}{item.get('cargo_item', 0):.2f}" if 'cargo_item' in item else ""
    print(f"    - {item['descripcion']}: {item['cantidad']} x {factura_hotel['simbolo_moneda']}{item['precio_unitario']:.2f}{cargo_txt}")

# Exportar JSON
archivo_json_hotel = json_exporter.exportar_factura(factura_hotel)
print(f"  JSON: {archivo_json_hotel}")

# ============================================================================
# FACTURA 2: TIPO YANACOCHA (Servicios/Construcción)
# ============================================================================
print("\n[2/2] Generando factura tipo YANACOCHA (Servicios Mineros)...")

factura_yanacocha = gen.generar_factura(
    tipo_factura='general',
    categoria_items='servicios',  # Servicios como Yanacocha
    moneda='USD',
    con_credito=True
)

# Personalizar emisor para que parezca empresa minera
factura_yanacocha['emisor']['razon_social'] = "SERVICIOS MINEROS DEL PERU S.A.C."
factura_yanacocha['receptor']['razon_social'] = "MINERA YANACOCHA S.R.L."

facturas_generadas.append(factura_yanacocha)

print(f"✓ Factura Servicios generada: {factura_yanacocha['numero_factura']}")
print(f"  Emisor: {factura_yanacocha['emisor']['razon_social']}")
print(f"  Receptor: {factura_yanacocha['receptor']['razon_social']}")
print(f"  Fecha: {factura_yanacocha['fecha_emision'].strftime('%d/%m/%Y')}")
print(f"  Total: {factura_yanacocha['simbolo_moneda']}{factura_yanacocha['total']:.2f}")
print(f"  Items: {len(factura_yanacocha['items'])} items")
for item in factura_yanacocha['items']:
    print(f"    - {item['descripcion']}: {item['cantidad']} {item['unidad']} x {factura_yanacocha['simbolo_moneda']}{item['precio_unitario']:.2f}")

# Exportar JSON
archivo_json_yanacocha = json_exporter.exportar_factura(factura_yanacocha)
print(f"  JSON: {archivo_json_yanacocha}")

# ============================================================================
# INTENTAR GENERAR PDFs
# ============================================================================
print("\n" + "=" * 80)
print("INTENTANDO GENERAR PDFs...")
print("=" * 80)

try:
    # Cargar pdf_creator.py
    spec = importlib.util.spec_from_file_location("pdf_creator", "/home/user/Creador-De-Factura/src/pdf_creator.py")
    pdf_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pdf_module)
    PDFFactura = pdf_module.PDFFactura
    
    pdf_gen = PDFFactura(output_dir="facturas_generadas/PDFs")
    
    print("\n[PDF 1/2] Generando PDF de hotel...")
    archivo_pdf_hotel = pdf_gen.crear_factura(factura_hotel)
    print(f"✓ PDF Hotel: {archivo_pdf_hotel}")
    
    print("\n[PDF 2/2] Generando PDF de servicios...")
    archivo_pdf_yanacocha = pdf_gen.crear_factura(factura_yanacocha)
    print(f"✓ PDF Servicios: {archivo_pdf_yanacocha}")
    
    print("\n✅ AMBOS PDFs GENERADOS EXITOSAMENTE!")
    
except Exception as e:
    print(f"\n⚠️  No se pudieron generar PDFs en este entorno")
    print(f"   Razón: {str(e)}")
    print("   Los PDFs se generarán correctamente en Google Colab")

# ============================================================================
# VALIDAR CÁLCULOS
# ============================================================================
print("\n" + "=" * 80)
print("VALIDANDO CÁLCULOS")
print("=" * 80)

for idx, factura in enumerate(facturas_generadas, 1):
    print(f"\nFactura {idx}: {factura['numero_factura']}")
    
    # Validar IGV
    igv_esperado = round(factura['op_gravada'] * 0.18, 2)
    igv_ok = abs(igv_esperado - factura['igv']) <= 0.02
    print(f"  IGV (18%): {factura['simbolo_moneda']}{factura['igv']:.2f} (esperado: {igv_esperado:.2f}) {'✓' if igv_ok else '✗'}")
    
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
    total_ok = abs(total_esperado - factura['total']) <= 0.02
    print(f"  Total: {factura['simbolo_moneda']}{factura['total']:.2f} (esperado: {total_esperado:.2f}) {'✓' if total_ok else '✗'}")
    
    # Validar cuotas
    if factura['con_credito'] and factura['cuotas']:
        suma_cuotas = sum(c['monto'] for c in factura['cuotas'])
        cuotas_ok = abs(suma_cuotas - factura['total']) <= 0.02
        print(f"  Cuotas: {len(factura['cuotas'])} cuotas, suma={factura['simbolo_moneda']}{suma_cuotas:.2f} {'✓' if cuotas_ok else '✗'}")

# ============================================================================
# RESUMEN FINAL
# ============================================================================
print("\n" + "=" * 80)
print("RESUMEN FINAL")
print("=" * 80)

resumen = json_exporter.crear_resumen(facturas_generadas)

print(f"\n📊 Facturas generadas: {resumen['total_facturas']}")
print(f"\n📋 Por tipo:")
for tipo, cant in resumen['por_tipo'].items():
    print(f"   - {tipo.upper()}: {cant}")

print(f"\n💰 Por moneda:")
for moneda, cant in resumen['por_moneda'].items():
    print(f"   - {moneda}: {cant} factura(s)")

print(f"\n💵 Totales:")
for moneda, total in resumen['totales_por_moneda'].items():
    simbolo = {'PEN': 'S/', 'USD': '$', 'EUR': '€'}.get(moneda, '')
    print(f"   - {moneda}: {simbolo}{total:,.2f}")

print(f"\n📈 Estadísticas:")
print(f"   - Con crédito: {resumen['con_credito']} ({resumen['porcentaje_credito']}%)")
print(f"   - Con descuento: {resumen['con_descuento']} ({resumen['porcentaje_descuento']}%)")

# Guardar resumen
with open('facturas_generadas/JSONs/resumen_prueba.json', 'w', encoding='utf-8') as f:
    json.dump(resumen, f, ensure_ascii=False, indent=2)

print("\n✅ GENERACIÓN COMPLETADA")
print(f"   JSONs guardados en: facturas_generadas/JSONs/")
print(f"   Resumen: facturas_generadas/JSONs/resumen_prueba.json")

print("\n" + "=" * 80)
