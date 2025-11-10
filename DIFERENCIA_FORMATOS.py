"""
DEMOSTRACIÓN: Diferencia entre formato INCORRECTO y CORRECTO

Este script muestra la DIFERENCIA entre:
1. ❌ Guardar el JSON directamente desde el generador (INCORRECTO)
2. ✅ Usar JSONExporter para guardar en formato InvoiceX v5.5 (CORRECTO)
"""
import sys
import json
sys.path.insert(0, '/home/user/Creador-De-Factura')

from src.generator import FacturaGenerator
from src.json_exporter import JSONExporter

print("=" * 80)
print("DEMOSTRACIÓN: FORMATO INCORRECTO vs CORRECTO".center(80))
print("=" * 80)

# Generar factura
gen = FacturaGenerator()
factura = gen.generar_factura(tipo_factura='hotel', con_credito=True)

print(f"\n📋 Factura generada: {factura['numero_factura']}")
print(f"   Emisor: {factura['emisor']['razon_social']}")
print(f"   Total: {factura['simbolo_moneda']}{factura['total']:.2f}")

# ============================================================================
# MÉTODO INCORRECTO ❌ - Guardar directamente el diccionario interno
# ============================================================================
print("\n" + "=" * 80)
print("❌ MÉTODO INCORRECTO: Guardar directamente desde el generador".center(80))
print("=" * 80)

# Simular lo que hace el usuario cuando guarda directamente
from datetime import datetime

def preparar_json_incorrecto(datos):
    """Convierte datetime a strings pero mantiene estructura anidada"""
    datos_copia = {}
    for key, value in datos.items():
        if isinstance(value, datetime):
            datos_copia[key] = value.isoformat()
        elif isinstance(value, dict):
            datos_copia[key] = preparar_json_incorrecto(value)
        elif isinstance(value, list):
            datos_copia[key] = [
                preparar_json_incorrecto(item) if isinstance(item, dict) else item
                for item in value
            ]
        else:
            datos_copia[key] = value
    return datos_copia

json_incorrecto = preparar_json_incorrecto(factura)

# Guardar
with open('factura_INCORRECTA.json', 'w', encoding='utf-8') as f:
    json.dump(json_incorrecto, f, indent=2, ensure_ascii=False)

print("\n🔍 Estructura del JSON INCORRECTO:")
print(f"   • Tiene 'emisor' anidado: {'emisor' in json_incorrecto and isinstance(json_incorrecto['emisor'], dict)}")
print(f"   • Tiene 'emisor_ruc' plano: {'emisor_ruc' in json_incorrecto}")
print(f"   • Campo tipo: {json_incorrecto.get('tipo_comprobante')}")
print(f"   • Moneda: {json_incorrecto.get('moneda')}")
print(f"   • Fecha: {json_incorrecto.get('fecha_emision')}")
print(f"   • Campos raíz: {len([k for k in json_incorrecto.keys() if k not in ['items', 'cuotas']])}")
if json_incorrecto.get('items'):
    print(f"   • Item 1 - campos: {len(json_incorrecto['items'][0])}")

print("\n📄 Guardado en: factura_INCORRECTA.json")

# ============================================================================
# MÉTODO CORRECTO ✅ - Usar JSONExporter
# ============================================================================
print("\n" + "=" * 80)
print("✅ MÉTODO CORRECTO: Usar JSONExporter (formato InvoiceX v5.5)".center(80))
print("=" * 80)

exporter = JSONExporter(output_dir=".")
archivo_correcto = exporter.exportar_factura(factura, filename="factura_CORRECTA.json")

# Leer para mostrar
with open(archivo_correcto, 'r', encoding='utf-8') as f:
    json_correcto = json.load(f)

print("\n🔍 Estructura del JSON CORRECTO:")
print(f"   • Tiene 'emisor' anidado: {'emisor' in json_correcto and isinstance(json_correcto.get('emisor'), dict)}")
print(f"   • Tiene 'emisor_ruc' plano: {'emisor_ruc' in json_correcto}")
print(f"   • Campo tipo: {json_correcto.get('tipo_documento')}")
print(f"   • Moneda: {json_correcto.get('moneda')}")
print(f"   • Fecha: {json_correcto.get('fecha_emision')}")
print(f"   • Campos raíz: {len([k for k in json_correcto.keys() if k not in ['items', 'cuotas']])}")
if json_correcto.get('items'):
    print(f"   • Item 1 - campos: {len(json_correcto['items'][0])}")

print("\n📄 Guardado en: factura_CORRECTA.json")

# ============================================================================
# COMPARACIÓN
# ============================================================================
print("\n" + "=" * 80)
print("COMPARACIÓN LADO A LADO".center(80))
print("=" * 80)

print("\n" + "-" * 80)
print("CAMPO".ljust(30) + "INCORRECTO".ljust(30) + "CORRECTO".ljust(20))
print("-" * 80)

comparaciones = [
    ("Estructura", "Anidada (emisor: {})", "Plana (emisor_ruc)"),
    ("Tipo documento", json_incorrecto.get("tipo_comprobante", "N/A"), json_correcto.get("tipo_documento", "N/A")),
    ("Serie", json_incorrecto.get("numero_factura", "N/A"), json_correcto.get("serie_completa", "N/A")),
    ("Moneda", json_incorrecto.get("moneda", "N/A"), json_correcto.get("moneda", "N/A")),
    ("Fecha", json_incorrecto.get("fecha_emision", "N/A")[:10], json_correcto.get("fecha_emision", "N/A")),
    ("Emisor RUC", "emisor.ruc", "emisor_ruc"),
    ("Receptor RUC", "receptor.ruc", "receptor_numero_doc"),
    ("Campos raíz", str(len([k for k in json_incorrecto.keys() if k not in ['items', 'cuotas']])),
     str(len([k for k in json_correcto.keys() if k not in ['items', 'cuotas']]))),
    ("Campos por item", str(len(json_incorrecto['items'][0])) if json_incorrecto.get('items') else "0",
     str(len(json_correcto['items'][0])) if json_correcto.get('items') else "0"),
]

for campo, incorrecto, correcto in comparaciones:
    print(f"{campo.ljust(30)}{str(incorrecto).ljust(30)}{str(correcto).ljust(20)}")

print("-" * 80)

# ============================================================================
# CONCLUSIÓN
# ============================================================================
print("\n" + "=" * 80)
print("🎯 CONCLUSIÓN".center(80))
print("=" * 80)

print("""
❌ NO HAGAS ESTO:

   factura = gen.generar_factura()
   with open('factura.json', 'w') as f:
       json.dump(factura, f)  # ❌ Formato incorrecto (anidado)


✅ HAZ ESTO EN SU LUGAR:

   factura = gen.generar_factura()
   exporter = JSONExporter()
   exporter.exportar_factura(factura)  # ✅ Formato correcto (InvoiceX v5.5)


📝 ARCHIVOS GENERADOS PARA COMPARAR:
   • factura_INCORRECTA.json  - Formato anidado (lo que NO quieres)
   • factura_CORRECTA.json    - Formato InvoiceX v5.5 (lo que SÍ quieres)

Abre ambos archivos y compáralos para ver la diferencia.
""")

print("=" * 80)
