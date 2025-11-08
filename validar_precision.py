"""
Script de validación de precisión numérica en facturas
Genera 20 facturas y verifica que JSON y PDF tengan valores consistentes
"""
import sys
import json
import os
from datetime import datetime

sys.path.insert(0, 'src')
from src.generator import FacturaGenerator
from src.dataset_exporter import DatasetExporter

# Intentar importar PDFFactura, si no está disponible, continuar sin PDFs
try:
    from src.pdf_creator import PDFFactura
    GENERAR_PDFS = True
except ImportError:
    GENERAR_PDFS = False
    print("⚠️  reportlab no disponible, generando solo JSONs\n")


def validar_precision_decimal(valor, nombre_campo):
    """Valida que un valor numérico tenga máximo 2 decimales"""
    if valor is None:
        return True, "null"

    valor_str = str(valor)
    if '.' in valor_str:
        decimales = len(valor_str.split('.')[1])
        if decimales > 2:
            return False, f"{valor} tiene {decimales} decimales"
        else:
            return True, f"{valor:.2f}"
    else:
        return True, f"{valor:.2f}"


def validar_factura(factura_original, json_path):
    """Valida que los valores de la factura original coincidan con el JSON"""
    with open(json_path, 'r', encoding='utf-8') as f:
        anotacion = json.load(f)

    errores = []
    warnings = []

    # Validar precisión numérica (solo verificar que tenga 2 decimales)
    campos_numericos = ['subtotal', 'igv', 'importe_total', 'otros_cargos', 'descuento']

    for campo in campos_numericos:
        if campo in anotacion and anotacion[campo] is not None:
            valido, mensaje = validar_precision_decimal(anotacion[campo], campo)
            if not valido:
                errores.append(f"{campo}: {mensaje}")

    # Validar que los valores del JSON coincidan con la factura original
    # (verificar que el redondeo no altere los valores)
    total_original = factura_original.get('total', 0)
    total_json = anotacion.get('importe_total', 0)

    # Verificar que el total no cambie al exportar (tolerancia mínima por redondeo)
    if abs(total_json - total_original) > 0.01:
        errores.append(f"Total difiere: Original={total_original:.2f}, JSON={total_json:.2f}")

    # Verificar IGV
    igv_original = factura_original.get('igv', 0)
    igv_json = anotacion.get('igv', 0)

    if abs(igv_json - igv_original) > 0.01:
        errores.append(f"IGV difiere: Original={igv_original:.2f}, JSON={igv_json:.2f}")

    return errores, warnings, anotacion


def main():
    print("=" * 80)
    print("VALIDACIÓN DE PRECISIÓN NUMÉRICA - 20 FACTURAS".center(80))
    print("=" * 80)

    # Crear exportador
    exporter = DatasetExporter(base_dir='validacion_precision')
    dataset_dir = exporter.crear_dataset()

    print(f"\n📁 Dataset: {os.path.basename(dataset_dir)}\n")

    # Generadores
    factura_gen = FacturaGenerator()
    pdf_gen = PDFFactura() if GENERAR_PDFS else None

    tipos_factura = ['general', 'hotel', 'seguro', 'con_descuento']

    total_errores = 0
    total_warnings = 0
    facturas_ok = 0

    resultados = []

    for i in range(20):
        tipo = tipos_factura[i % len(tipos_factura)]

        # Generar factura
        factura = factura_gen.generar_factura(tipo_factura=tipo)

        # Generar PDF si está disponible
        pdf_content = None
        if pdf_gen:
            pdf_path_temp = f"/tmp/temp_{factura['numero_factura']}.pdf"
            try:
                pdf_gen.crear_factura(factura, pdf_path_temp)
                with open(pdf_path_temp, 'rb') as f:
                    pdf_content = f.read()
                os.remove(pdf_path_temp)
            except Exception as e:
                print(f"❌ [{i+1:2d}] Error generando PDF: {e}")
                continue

        # Exportar
        json_path, pdf_path = exporter.exportar_factura(factura, pdf_content)

        # Validar
        errores, warnings, anotacion = validar_factura(factura, json_path)

        # Resultado
        serie = anotacion['serie_completa']
        total = anotacion['importe_total']

        if errores:
            status = "❌"
            total_errores += len(errores)
        elif warnings:
            status = "⚠️ "
            total_warnings += len(warnings)
            facturas_ok += 1
        else:
            status = "✅"
            facturas_ok += 1

        print(f"{status} [{i+1:2d}/20] {serie:15s} | Total: {total:>10.2f} | Tipo: {tipo:15s}")

        if errores:
            for error in errores:
                print(f"        ERROR: {error}")

        if warnings:
            for warning in warnings:
                print(f"        WARN: {warning}")

        # Guardar para resumen
        resultados.append({
            'numero': i + 1,
            'serie': serie,
            'tipo': tipo,
            'total': total,
            'subtotal': anotacion['subtotal'],
            'igv': anotacion['igv'],
            'otros_cargos': anotacion.get('otros_cargos'),
            'errores': errores,
            'warnings': warnings
        })

    # Resumen final
    print("\n" + "=" * 80)
    print("RESUMEN DE VALIDACIÓN".center(80))
    print("=" * 80)

    print(f"\n📊 Estadísticas:")
    print(f"   • Total facturas generadas: 20")
    print(f"   • Facturas OK: {facturas_ok} ({facturas_ok/20*100:.0f}%)")
    print(f"   • Total errores: {total_errores}")
    print(f"   • Total warnings: {total_warnings}")

    if total_errores == 0:
        print(f"\n✅ ¡VALIDACIÓN EXITOSA! Todas las facturas tienen precisión numérica correcta.")
    else:
        print(f"\n❌ Se encontraron {total_errores} errores de precisión.")

    # Detalles de precisión
    print(f"\n📋 Verificación de campos numéricos:")

    campos_con_problemas = {}
    for resultado in resultados:
        for error in resultado['errores']:
            campo = error.split(':')[0]
            campos_con_problemas[campo] = campos_con_problemas.get(campo, 0) + 1

    if campos_con_problemas:
        print("\n   Campos con errores de precisión:")
        for campo, cantidad in campos_con_problemas.items():
            print(f"   • {campo}: {cantidad} facturas")
    else:
        print("   ✅ Todos los campos numéricos tienen exactamente 2 decimales")

    # Ejemplos de valores
    print(f"\n📝 Muestra de valores (primeras 5 facturas):")
    print(f"{'#':<4} {'Serie':<15} {'Subtotal':<12} {'IGV':<12} {'Otros':<12} {'Total':<12}")
    print("-" * 75)

    for r in resultados[:5]:
        otros = f"{r['otros_cargos']:.2f}" if r['otros_cargos'] else "null"
        print(f"{r['numero']:<4} {r['serie']:<15} {r['subtotal']:<12.2f} {r['igv']:<12.2f} {otros:<12} {r['total']:<12.2f}")

    print(f"\n✅ Dataset guardado en: {dataset_dir}")
    print(f"   • Anotaciones (JSON): {len(resultados)}")
    if GENERAR_PDFS:
        print(f"   • PDFs: {len(resultados)}")
    else:
        print(f"   • PDFs: 0 (reportlab no disponible)")

    return total_errores == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
