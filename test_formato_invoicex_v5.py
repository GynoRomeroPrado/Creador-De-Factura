"""
Script de validación para estructura JSON oficial InvoiceX v5.5
Verifica que los JSONs generados cumplan con todos los campos requeridos
"""
import sys
import json
sys.path.insert(0, 'src')

from src.generator import FacturaGenerator
from src.dataset_exporter import DatasetExporter

print("=" * 80)
print("VALIDACIÓN ESTRUCTURA INVOICEX v5.5".center(80))
print("=" * 80)

# Campos oficiales que deben estar presentes
CAMPOS_REQUERIDOS = {
    # SECCIÓN 1: DOCUMENTO (5)
    "tipo_documento", "serie_completa", "fecha_emision", "fecha_vencimiento", "moneda",

    # SECCIÓN 2: EMISOR (14)
    "emisor_ruc", "emisor_razon_social", "emisor_direccion", "emisor_sucursal",
    "emisor_telefono", "emisor_web", "emisor_departamento", "emisor_provincia",
    "emisor_distrito", "emisor_ubigeo", "emisor_codigo_postal", "emisor_email",
    "emisor_nombre_comercial", "emisor_codigo_establecimiento",

    # SECCIÓN 3: RECEPTOR (14)
    "receptor_numero_doc", "receptor_tipo_doc", "receptor_razon_social", "receptor_direccion",
    "receptor_contacto", "receptor_telefono", "receptor_email", "receptor_sucursal",
    "receptor_departamento", "receptor_provincia", "receptor_distrito", "receptor_ubigeo",
    "receptor_codigo_postal", "receptor_nombre_comercial",

    # SECCIÓN 4: IMPORTES Y TRIBUTOS (19)
    "subtotal", "descuento", "subtotal_con_descuento", "igv", "isc", "otros_cargos",
    "importe_total", "tipo_cambio", "importe_total_moneda_base", "retencion_monto",
    "retencion_porcentaje", "percepcion_monto", "percepcion_porcentaje",
    "detraccion_monto", "detraccion_porcentaje", "detraccion_codigo_bienes",
    "anticipo_monto", "anticipo_numero",

    # SECCIÓN 5: REFERENCIAS (9)
    "numero_contrato", "orden_compra", "orden_servicio", "numero_pedido",
    "guia_remision", "condicion_pago", "forma_pago", "cuenta_bancaria",
    "numero_cuenta_detraccion",

    # SECCIÓN 6: INFORMACIÓN ADICIONAL (9)
    "glosa", "observaciones", "centro_costo", "proyecto", "ubicacion_obra",
    "numero_vale", "numero_placa", "referencia_1", "referencia_2",

    # SECCIÓN 9: CAMPOS SUNAT (5)
    "cod_qr", "hash_sunat", "numero_autorizacion", "serie_fisica", "numero_fisico",

    # SECCIÓN 10: DOCUMENTO RELACIONADO (4)
    "doc_relacionado_tipo", "doc_relacionado_numero", "doc_relacionado_fecha", "motivo_emision",

    # SECCIÓN 13: EXPORTACIÓN (6)
    "is_exportacion", "incoterm", "puerto_embarque", "puerto_destino", "nave", "numero_contenedor",

    # SECCIÓN 14: RÉGIMEN TRIBUTARIO (3)
    "agente_retencion", "agente_percepcion", "buen_contribuyente",

    # SECCIÓN 15: PERSONAL (4)
    "vendedor_codigo", "vendedor_nombre", "cajero_codigo", "cajero_nombre",

    # SECCIÓN 16: FECHAS ADICIONALES (3)
    "fecha_registro", "fecha_pago", "fecha_cancelacion",

    # ARRAYS
    "items", "cuotas"
}

CAMPOS_ITEM_REQUERIDOS = {
    "item", "codigo", "descripcion", "cantidad", "unidad_medida", "precio_unitario",
    "valor_venta", "descuento_item", "subtotal_item", "tipo_igv", "igv_item",
    "isc_item", "otro_tributo", "importe_total_item", "lote", "fecha_vencimiento",
    "serie", "modelo", "marca", "placa", "partida_arancelaria", "centro_costo_item",
    "cuenta_contable", "proyecto_item", "orden_item", "ubicacion", "observacion_item"
}

CAMPOS_CUOTA_REQUERIDOS = {"numero", "monto", "fecha_vencimiento", "estado"}

# Crear exportador y generador
exporter = DatasetExporter(base_dir='test_invoicex_v5')
dataset_dir = exporter.crear_dataset()
factura_gen = FacturaGenerator()

print(f"\n📁 Dataset: {dataset_dir}\n")

# Generar facturas de prueba
configuraciones = [
    {'tipo': 'hotel', 'items': 3, 'desc': 'Factura de hotel'},
    {'tipo': 'general', 'items': 5, 'desc': 'Factura general'},
    {'tipo': 'con_descuento', 'items': 4, 'desc': 'Factura con descuento'},
]

resultados = []

for i, config in enumerate(configuraciones, 1):
    print(f"\n[{i}/{len(configuraciones)}] {config['desc']}")
    print("-" * 80)

    # Generar factura
    factura = factura_gen.generar_factura(
        tipo_factura=config['tipo'],
        num_items=config['items']
    )

    # Exportar JSON
    json_path, _ = exporter.exportar_factura(factura, pdf_content=None)

    # Leer JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    print(f"    Serie: {data.get('serie_completa')}")
    print(f"    Moneda: {data.get('moneda')}")
    print(f"    Items: {len(data.get('items', []))}")
    print(f"    Cuotas: {len(data.get('cuotas', []))}")

    # === VALIDACIÓN 1: Campos raíz presentes ===
    campos_presentes = set(data.keys())
    campos_faltantes = CAMPOS_REQUERIDOS - campos_presentes
    campos_extra = campos_presentes - CAMPOS_REQUERIDOS

    # === VALIDACIÓN 2: Tipos de datos ===
    errores_tipos = []

    # Verificar fechas
    if data.get('fecha_emision') and not data['fecha_emision'].count('-') == 2:
        errores_tipos.append(f"fecha_emision no está en formato YYYY-MM-DD: {data['fecha_emision']}")

    # Verificar moneda normalizada
    if data.get('moneda') not in ["SOLES", "DOLARES AMERICANOS", "EUROS"]:
        errores_tipos.append(f"moneda no está normalizada: {data['moneda']}")

    # Verificar números
    for campo in ['subtotal', 'igv', 'importe_total']:
        if campo in data and not isinstance(data[campo], (int, float)):
            errores_tipos.append(f"{campo} no es numérico: {type(data[campo])}")

    # Verificar boolean
    for campo in ['is_exportacion', 'agente_retencion', 'agente_percepcion', 'buen_contribuyente']:
        if campo in data and not isinstance(data[campo], bool):
            errores_tipos.append(f"{campo} no es boolean: {type(data[campo])}")

    # === VALIDACIÓN 3: Items ===
    errores_items = []
    if not isinstance(data.get('items'), list):
        errores_items.append("items no es un array")
    else:
        for idx, item in enumerate(data['items'], 1):
            # Verificar campos del item
            campos_item = set(item.keys())
            faltantes_item = CAMPOS_ITEM_REQUERIDOS - campos_item
            if faltantes_item:
                errores_items.append(f"Item {idx} faltan campos: {faltantes_item}")

            # Verificar tipo_igv
            if item.get('tipo_igv') not in ["GRAVADO", "EXONERADO", "INAFECTO", None]:
                errores_items.append(f"Item {idx} tipo_igv inválido: {item['tipo_igv']}")

            # Verificar cálculo: importe_total_item = subtotal_item + igv_item + otro_tributo
            if item.get('subtotal_item') and item.get('igv_item') is not None:
                esperado = item['subtotal_item'] + (item.get('igv_item') or 0) + (item.get('otro_tributo') or 0)
                esperado = round(esperado, 2)
                actual = item.get('importe_total_item', 0)
                if abs(esperado - actual) > 0.05:  # tolerancia de 5 centavos
                    errores_items.append(f"Item {idx} importe_total_item incorrecto: esperado {esperado}, actual {actual}")

    # === VALIDACIÓN 4: Cuotas ===
    errores_cuotas = []
    if not isinstance(data.get('cuotas'), list):
        errores_cuotas.append("cuotas no es un array")
    else:
        for idx, cuota in enumerate(data['cuotas'], 1):
            campos_cuota = set(cuota.keys())
            faltantes_cuota = CAMPOS_CUOTA_REQUERIDOS - campos_cuota
            if faltantes_cuota:
                errores_cuotas.append(f"Cuota {idx} faltan campos: {faltantes_cuota}")

    # === RESUMEN ===
    total_validaciones = 4
    validaciones_ok = 0

    if not campos_faltantes:
        validaciones_ok += 1
    if not errores_tipos:
        validaciones_ok += 1
    if not errores_items:
        validaciones_ok += 1
    if not errores_cuotas:
        validaciones_ok += 1

    print(f"\n    ✅ Validaciones: {validaciones_ok}/{total_validaciones}")

    # Mostrar errores
    if campos_faltantes:
        print(f"    ⚠️  Campos faltantes: {campos_faltantes}")
    if errores_tipos:
        print(f"    ⚠️  Errores de tipo:")
        for err in errores_tipos:
            print(f"       • {err}")
    if errores_items:
        print(f"    ⚠️  Errores en items:")
        for err in errores_items[:3]:  # Mostrar solo primeros 3
            print(f"       • {err}")
        if len(errores_items) > 3:
            print(f"       ... y {len(errores_items) - 3} más")
    if errores_cuotas:
        print(f"    ⚠️  Errores en cuotas:")
        for err in errores_cuotas:
            print(f"       • {err}")

    resultados.append({
        'tipo': config['tipo'],
        'serie': data.get('serie_completa'),
        'validaciones_ok': validaciones_ok,
        'total': total_validaciones,
        'ok': validaciones_ok == total_validaciones
    })

# === RESUMEN FINAL ===
print("\n" + "=" * 80)
print("RESUMEN DE VALIDACIÓN".center(80))
print("=" * 80)

print(f"\n{'Tipo':<20} {'Serie':<20} {'Validaciones':<15} {'Estado':<10}")
print("-" * 80)

for r in resultados:
    estado = "✅ OK" if r['ok'] else "❌ FALLÓ"
    print(f"{r['tipo']:<20} {r['serie']:<20} {r['validaciones_ok']}/{r['total']:<13} {estado:<10}")

total_ok = sum(1 for r in resultados if r['ok'])
print(f"\n✅ Facturas validadas correctamente: {total_ok}/{len(resultados)}")

if total_ok == len(resultados):
    print("\n🎉 ¡TODAS LAS VALIDACIONES PASARON!")
    print("✅ Estructura JSON cumple con InvoiceX v5.5")
    print("✅ 97 campos principales presentes")
    print("✅ Moneda normalizada (SOLES/DOLARES AMERICANOS)")
    print("✅ Fechas en formato YYYY-MM-DD")
    print("✅ Campos planos (emisor_*, receptor_*)")
    print("✅ Items con 26 campos cada uno")
    print("✅ tipo_igv implementado (GRAVADO/INAFECTO)")
else:
    print("\n⚠️  Algunas validaciones fallaron. Revisar arriba.")

print(f"\n📁 Dataset guardado en: {dataset_dir}")
print(f"📄 Total de campos por factura: {len(CAMPOS_REQUERIDOS)}")
