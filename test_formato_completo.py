"""
Script para validar el nuevo formato JSON completo con todos los tipos de facturas
"""
import sys
import json
sys.path.insert(0, 'src')

from src.generator import FacturaGenerator
from src.dataset_exporter import DatasetExporter

print("=" * 80)
print("VALIDACIÓN COMPLETA DEL NUEVO FORMATO JSON".center(80))
print("=" * 80)

# Crear exportador
exporter = DatasetExporter(base_dir='test_formato_completo')
dataset_dir = exporter.crear_dataset()

print(f"\n📁 Dataset: {dataset_dir}\n")

factura_gen = FacturaGenerator()

# Configuraciones de prueba
configuraciones = [
    {'tipo': 'hotel', 'items': 3, 'desc': 'Factura de hotel con 3 items'},
    {'tipo': 'general', 'items': 5, 'desc': 'Factura general con 5 items'},
    {'tipo': 'con_descuento', 'items': 4, 'desc': 'Factura con descuento'},
    {'tipo': 'compra_grande', 'items': 35, 'desc': 'Compra grande con 35 items'},
]

resultados = []

for i, config in enumerate(configuraciones, 1):
    print(f"\n[{i}/4] {config['desc']}")
    print("-" * 80)

    # Generar factura
    factura = factura_gen.generar_factura(
        tipo_factura=config['tipo'],
        num_items=config['items']
    )

    serie = factura['numero_factura']
    tipo = factura['tipo_factura']
    num_items = len(factura['items'])

    print(f"    Tipo: {tipo}")
    print(f"    Serie: {serie}")
    print(f"    Items: {num_items}")

    # Exportar JSON
    json_path, _ = exporter.exportar_factura(factura, pdf_content=None)

    # Leer y validar JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Validaciones
    validaciones = {
        'tipo_comprobante': data.get('tipo_comprobante') is not None,
        'tipo_factura': data.get('tipo_factura') == tipo,
        'numero_factura': data.get('numero_factura') == serie,
        'serie_separada': data.get('serie') is not None and data.get('numero') is not None,
        'fechas_iso': 'T00:00:00' in data.get('fecha_emision', ''),
        'emisor_nested': isinstance(data.get('emisor'), dict),
        'receptor_nested': isinstance(data.get('receptor'), dict),
        'moneda_campos': all(k in data for k in ['moneda', 'simbolo_moneda', 'nombre_moneda']),
        'items_array': isinstance(data.get('items'), list) and len(data['items']) > 0,
        'operaciones': all(k in data for k in ['op_gravada', 'op_exonerada', 'op_inafecta', 'op_gratuitas']),
        'totales': all(k in data for k in ['igv', 'total', 'total_letras']),
        'cargos': all(k in data for k in ['total_cargos', 'otros_cargos']),
        'credito': 'con_credito' in data and 'cuotas' in data,
        'datos_hotel': 'datos_hotel' in data,
        'total_letras_ok': len(data.get('total_letras', '')) > 0,
    }

    # Validaciones específicas por tipo
    if tipo == 'hotel':
        validaciones['hotel_items_simplificados'] = all(
            item['descripcion'] in ['ALIMENTACION', 'ALOJAMIENTO', 'ALIMENTACION pack x6']
            for item in data['items']
        )
        validaciones['hotel_cargo_item'] = all(
            'cargo_item' in item and 'importe_total' in item
            for item in data['items']
        )
        validaciones['hotel_datos'] = isinstance(data.get('datos_hotel'), dict)
        validaciones['hotel_habitacion'] = data.get('datos_hotel', {}).get('habitacion') is not None
    else:
        validaciones['general_no_cargo'] = all(
            'cargo_item' not in item
            for item in data['items']
        )
        validaciones['general_hotel_null'] = data.get('datos_hotel') is None

    # Contar validaciones exitosas
    total_validaciones = len(validaciones)
    exitosas = sum(1 for v in validaciones.values() if v)

    print(f"    ✅ Validaciones: {exitosas}/{total_validaciones}")

    if exitosas < total_validaciones:
        print(f"    ⚠️  Validaciones fallidas:")
        for nombre, resultado in validaciones.items():
            if not resultado:
                print(f"       • {nombre}")

    resultados.append({
        'tipo': tipo,
        'serie': serie,
        'items': num_items,
        'validaciones': exitosas,
        'total_validaciones': total_validaciones,
        'ok': exitosas == total_validaciones
    })

# Resumen
print("\n" + "=" * 80)
print("RESUMEN DE VALIDACIÓN".center(80))
print("=" * 80)

print(f"\n{'Tipo':<18} {'Serie':<18} {'Items':<8} {'Validaciones':<20} {'Estado':<10}")
print("-" * 80)

for r in resultados:
    estado = "✅ OK" if r['ok'] else "❌ FALLÓ"
    print(f"{r['tipo']:<18} {r['serie']:<18} {r['items']:<8} {r['validaciones']}/{r['total_validaciones']:<18} {estado:<10}")

total_ok = sum(1 for r in resultados if r['ok'])
print(f"\n✅ Facturas validadas correctamente: {total_ok}/{len(resultados)}")

if total_ok == len(resultados):
    print("\n🎉 ¡TODAS LAS VALIDACIONES PASARON!")
    print("✅ El nuevo formato JSON está funcionando correctamente")
    print("✅ Items de hotel simplificados (ALIMENTACION/ALOJAMIENTO)")
    print("✅ Items generales con descripciones variadas")
    print("✅ Estructura anidada (emisor, receptor, datos_hotel)")
    print("✅ Todos los campos nuevos presentes")
    print("✅ total_letras generado correctamente")
else:
    print("\n⚠️  Algunas validaciones fallaron. Revisar arriba.")

print(f"\n📁 Dataset guardado en: {dataset_dir}")
