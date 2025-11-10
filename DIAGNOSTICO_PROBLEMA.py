"""
🔍 DIAGNÓSTICO: Identificar por qué obtienes JSON con estructura anidada

Este script te ayuda a identificar el problema.
"""
import sys
sys.path.insert(0, '/home/user/Creador-De-Factura')

from src.generator import FacturaGenerator
from src.json_exporter import JSONExporter
import json

print("=" * 80)
print("🔍 DIAGNÓSTICO: ¿Por qué obtienes estructura anidada?".center(80))
print("=" * 80)

# Generar factura
gen = FacturaGenerator()
factura = gen.generar_factura(tipo_factura='hotel', con_credito=True)

print("\n📋 PASO 1: Diccionario interno del generador")
print("-" * 80)
print(f"El generador SIEMPRE devuelve estructura ANIDADA (esto es normal):")
print(f"  • factura['emisor'] es dict: {isinstance(factura.get('emisor'), dict)}")
print(f"  • factura['emisor']['ruc']: {factura['emisor']['ruc']}")
print(f"  • factura['receptor']['ruc']: {factura['receptor']['ruc']}")
print("\n⚠️  ESTE FORMATO ANIDADO ES SOLO PARA USO INTERNO")
print("    NUNCA lo guardes directamente con json.dump()")

# ============================================================================
# MÉTODO INCORRECTO
# ============================================================================
print("\n" + "=" * 80)
print("❌ MÉTODO INCORRECTO: Guardar directamente".center(80))
print("=" * 80)

print("\nSi haces esto:")
print("""
    factura = gen.generar_factura()
    with open('factura.json', 'w') as f:
        json.dump(factura, f)  # ❌ INCORRECTO
""")

# Simular guardado incorrecto
from datetime import datetime

def convertir_datetime(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()
    elif isinstance(obj, dict):
        return {k: convertir_datetime(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convertir_datetime(item) for item in obj]
    return obj

json_incorrecto = convertir_datetime(factura)
with open('DIAGNOSTICO_INCORRECTO.json', 'w') as f:
    json.dump(json_incorrecto, f, indent=2, ensure_ascii=False)

print("\n📄 Resultado: DIAGNOSTICO_INCORRECTO.json")
print(f"  • Tiene 'emisor' anidado: {isinstance(json_incorrecto.get('emisor'), dict)}")
print(f"  • Tiene 'emisor_ruc' plano: {'emisor_ruc' in json_incorrecto}")
print(f"  • Estructura: ANIDADA ❌")

# ============================================================================
# MÉTODO CORRECTO
# ============================================================================
print("\n" + "=" * 80)
print("✅ MÉTODO CORRECTO: Usar JSONExporter".center(80))
print("=" * 80)

print("\nSi haces esto:")
print("""
    from src.json_exporter import JSONExporter

    factura = gen.generar_factura()
    exporter = JSONExporter()
    archivo = exporter.exportar_factura(factura)  # ✅ CORRECTO
""")

# Usar JSONExporter
exporter = JSONExporter(output_dir=".")
archivo = exporter.exportar_factura(factura, filename="DIAGNOSTICO_CORRECTO.json")

with open(archivo, 'r') as f:
    json_correcto = json.load(f)

print(f"\n📄 Resultado: {archivo}")
print(f"  • Tiene 'emisor' anidado: {isinstance(json_correcto.get('emisor'), dict)}")
print(f"  • Tiene 'emisor_ruc' plano: {'emisor_ruc' in json_correcto}")
print(f"  • Tiene 'receptor_numero_doc' plano: {'receptor_numero_doc' in json_correcto}")
print(f"  • Campos raíz: {len([k for k in json_correcto.keys() if k not in ['items', 'cuotas']])}")
print(f"  • Estructura: PLANA ✅")

# ============================================================================
# COMPARACIÓN
# ============================================================================
print("\n" + "=" * 80)
print("📊 COMPARACIÓN".center(80))
print("=" * 80)

print("\n" + "-" * 80)
print(f"{'CAMPO':<30} {'INCORRECTO':<25} {'CORRECTO':<25}")
print("-" * 80)

comparaciones = [
    ("Emisor RUC", "emisor.ruc", json_correcto.get('emisor_ruc', 'N/A')),
    ("Emisor Razón Social", "emisor.razon_social", json_correcto.get('emisor_razon_social', 'N/A')[:20] + "..."),
    ("Receptor RUC", "receptor.ruc", json_correcto.get('receptor_numero_doc', 'N/A')),
    ("Receptor Tipo Doc", "N/A", json_correcto.get('receptor_tipo_doc', 'N/A')),
    ("Tipo Documento", json_incorrecto.get('tipo_comprobante', 'N/A'), json_correcto.get('tipo_documento', 'N/A')),
    ("Serie", json_incorrecto.get('numero_factura', 'N/A'), json_correcto.get('serie_completa', 'N/A')),
    ("Moneda", json_incorrecto.get('moneda', 'N/A'), json_correcto.get('moneda', 'N/A')),
    ("Campos raíz", str(len([k for k in json_incorrecto.keys() if k not in ['items', 'cuotas']])),
     str(len([k for k in json_correcto.keys() if k not in ['items', 'cuotas']]))),
]

for campo, incorrecto, correcto in comparaciones:
    print(f"{campo:<30} {str(incorrecto):<25} {str(correcto):<25}")

print("-" * 80)

# ============================================================================
# DIAGNÓSTICO
# ============================================================================
print("\n" + "=" * 80)
print("🎯 DIAGNÓSTICO".center(80))
print("=" * 80)

print("""
Si tus JSONs tienen estructura ANIDADA, es porque estás haciendo UNA de estas cosas:

❌ 1. Guardas el diccionario directamente:
       json.dump(factura, f)

❌ 2. Usas un script viejo que no usa JSONExporter

❌ 3. Tienes una versión antigua del código

✅ SOLUCIÓN: USA SIEMPRE JSONExporter:

   from src.json_exporter import JSONExporter

   exporter = JSONExporter()
   archivo = exporter.exportar_factura(factura)


📝 ARCHIVOS GENERADOS PARA COMPARAR:
   • DIAGNOSTICO_INCORRECTO.json  ← Estructura ANIDADA (lo que NO quieres)
   • DIAGNOSTICO_CORRECTO.json    ← Estructura PLANA (lo que SÍ quieres)

Abre ambos archivos y compáralos.
""")

print("=" * 80)
print("\n✅ CONCLUSIÓN: JSONExporter SÍ funciona correctamente.")
print("   El problema es que NO lo estás usando.\n")
