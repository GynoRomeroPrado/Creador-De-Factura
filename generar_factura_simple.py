"""
SCRIPT SIMPLE PARA GENERAR FACTURAS EN FORMATO CORRECTO

USO:
    python generar_factura_simple.py

Este script genera UNA factura y la guarda en formato InvoiceX v5.5
"""
import sys
import json
sys.path.insert(0, '/home/user/Creador-De-Factura')

from src.generator import FacturaGenerator
from src.json_exporter import JSONExporter

print("=" * 70)
print("GENERANDO FACTURA EN FORMATO INVOICEX v5.5".center(70))
print("=" * 70)

# Configuración
tipo = input("\n¿Qué tipo de factura? (hotel/general/seguro/con_descuento) [hotel]: ").strip() or "hotel"
credito = input("¿Con crédito? (s/n) [s]: ").strip().lower() != 'n'

# Generar factura
print(f"\nGenerando factura tipo {tipo.upper()}...")
gen = FacturaGenerator()
factura_interna = gen.generar_factura(tipo_factura=tipo, con_credito=credito)

print(f"\n✓ Factura generada: {factura_interna['numero_factura']}")
print(f"  Emisor: {factura_interna['emisor']['razon_social']}")
print(f"  Receptor: {factura_interna['receptor']['razon_social']}")
print(f"  Total: {factura_interna['simbolo_moneda']}{factura_interna['total']:.2f}")

# IMPORTANTE: Exportar con JSONExporter para formato correcto
exporter = JSONExporter(output_dir="mi_factura")
archivo = exporter.exportar_factura(factura_interna)

print(f"\n✅ JSON guardado en: {archivo}")

# Verificar formato
with open(archivo, 'r', encoding='utf-8') as f:
    json_data = json.load(f)

print("\n" + "=" * 70)
print("VERIFICACIÓN DEL FORMATO".center(70))
print("=" * 70)

# Verificaciones
tiene_emisor_anidado = "emisor" in json_data and isinstance(json_data.get("emisor"), dict)
tiene_emisor_plano = "emisor_ruc" in json_data
moneda = json_data.get("moneda")
fecha = json_data.get("fecha_emision")
campos_raiz = len([k for k in json_data.keys() if k not in ["items", "cuotas"]])

print(f"\n❌ Estructura anidada (emisor: {{}}): {tiene_emisor_anidado}")
print(f"✅ Estructura plana (emisor_ruc): {tiene_emisor_plano}")
print(f"✅ Moneda normalizada: {moneda}")
print(f"✅ Fecha formato YYYY-MM-DD: {fecha}")
print(f"✅ Campos raíz: {campos_raiz}")
print(f"✅ Items (cantidad): {len(json_data.get('items', []))}")
if json_data.get('items'):
    print(f"✅ Item 1 - campos: {len(json_data['items'][0])}")

if tiene_emisor_plano and not tiene_emisor_anidado:
    print("\n🎉 ¡FORMATO CORRECTO! InvoiceX v5.5")
else:
    print("\n⚠️  FORMATO INCORRECTO - Tiene estructura anidada")

print("\n" + "=" * 70)
print(f"\n📄 Ver archivo completo: {archivo}")
print()
