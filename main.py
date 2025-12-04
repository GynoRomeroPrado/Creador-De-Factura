#!/usr/bin/env python3
"""
Generador de Facturas Ficticias - Punto de entrada principal

Uso:
    python main.py --cantidad 50 --output facturas_generadas/
    python main.py --analizar --input facturas_originales/
"""
import argparse
import os
import sys
import json
from datetime import date, datetime
from pathlib import Path
from src.generator import FacturaGenerator
from src.pdf_creator import PDFFactura

class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return super().default(obj)


def flatten_json(factura: dict) -> dict:
    """
    Aplana la estructura del JSON para el dataset de entrenamiento VLM.
    Incluye TODOS los campos disponibles en la factura.
    """
    # Helper para formatear fechas
    def fmt_date(d):
        if hasattr(d, 'strftime'):
            return d.strftime('%Y-%m-%d')
        return str(d)[:10] if d else None

    flat_data = {
        "tipo_documento": "FACTURA ELECTRÓNICA",
        "serie_completa": factura['numero_factura'],
        "fecha_emision": fmt_date(factura['fecha_emision']),
        "fecha_vencimiento": fmt_date(factura.get('fecha_vencimiento')),
        "moneda": factura['nombre_moneda'],
        
        # Emisor plano
        "emisor_ruc": factura['emisor']['ruc'],
        "emisor_razon_social": factura['emisor']['razon_social'],
        "emisor_direccion": factura['emisor']['direccion'],
        "emisor_telefono": factura['emisor']['telefono'],
        "emisor_email": factura['emisor']['email'],
        
        # Receptor plano
        "receptor_numero_doc": factura['receptor']['ruc'],
        "receptor_razon_social": factura['receptor']['razon_social'],
        "receptor_direccion": factura['receptor']['direccion'],
        "receptor_telefono": factura['receptor']['telefono'],
        "receptor_email": factura['receptor']['email'],
        
        # Datos Generales
        "total_letras": factura['total_letras'],
        "forma_pago": factura['forma_pago'],
        "observaciones": factura.get('observaciones'),
        "numero_contrato": factura.get('numero_contrato'),
        "periodo_facturado": factura.get('periodo_facturado'),
        "industria": factura.get('industria'),
        
        # Totales
        "subtotal": round(factura['op_gravada'] + factura['op_exonerada'] + factura['op_inafecta'], 2),
        "op_gravada": factura['op_gravada'],
        "op_exonerada": factura['op_exonerada'],
        "op_inafecta": factura['op_inafecta'],
        "op_gratuitas": factura.get('op_gratuitas', 0.0),
        "igv": factura['igv'],
        "total_cargos": factura.get('total_cargos', 0.0),
        "otros_cargos": factura.get('otros_cargos', 0.0),
        "importe_total": factura['total'],
        
        # Items (lista de objetos)
        "items": factura['items'],
        
        # Cuotas (lista de objetos, si existe)
        "cuotas": [{
            "numero": c['numero'],
            "fecha_vencimiento": fmt_date(c['fecha_vencimiento']),
            "monto": c['monto']
        } for c in factura.get('cuotas', [])] if factura.get('cuotas') else []
    }

    # Aplanar Datos Específicos (Hotel, Seguro, etc.)
    
    # Hotel
    if factura.get('datos_hotel'):
        h = factura['datos_hotel']
        flat_data.update({
            "hotel_checkin": fmt_date(h['checkin']),
            "hotel_checkout": fmt_date(h['checkout']),
            "hotel_huesped": h['huesped'],
            "hotel_reserva": h['reserva'],
            "hotel_noches": h['noches'],
            "hotel_habitacion": h.get('habitacion'),
            "hotel_codigo_grupo": h.get('codigo_grupo'),
            "hotel_nombre_grupo": h.get('nombre_grupo')
        })

    # Seguro
    if factura.get('datos_seguro'):
        s = factura['datos_seguro']
        flat_data.update({
            "seguro_poliza": s['numero_poliza'],
            "seguro_documento": s['numero_documento'],
            "seguro_giro": s['giro'],
            "seguro_vehiculo": s['vehiculo'],
            "seguro_vigencia_inicio": fmt_date(s['vigencia_inicio']),
            "seguro_vigencia_fin": fmt_date(s['vigencia_fin'])
        })

    # Restaurante
    if factura.get('datos_restaurante'):
        r = factura['datos_restaurante']
        flat_data.update({
            "restaurante_mesa": r['mesa'],
            "restaurante_personas": r['personas'],
            "restaurante_mesero": r['mesero'],
            "restaurante_hora_ingreso": r['hora_ingreso'],
            "restaurante_propinas": r['propinas']
        })

    # Transporte
    if factura.get('datos_transporte'):
        t = factura['datos_transporte']
        flat_data.update({
            "transporte_guia_remision": t['guia_remision'],
            "transporte_licencia": t['licencia'],
            "transporte_placa_vehiculo": t['placa_vehiculo'],
            "transporte_conductor": t['conductor'],
            "transporte_origen": t['origen'],
            "transporte_destino": t['destino']
        })

    # Servicios
    if factura.get('datos_servicios'):
        sv = factura['datos_servicios']
        flat_data.update({
            "servicio_orden": sv['orden_servicio'],
            "servicio_conformidad": sv['conformidad_servicio'],
            "servicio_area": sv['area_solicitante'],
            "servicio_proyecto": sv['proyecto']
        })

    # Descuento
    if factura.get('descuento'):
        d = factura['descuento']
        flat_data.update({
            "descuento_descripcion": d['descripcion'],
            "descuento_monto": d['monto'],
            "descuento_gravado": d['gravado'],
            "descuento_exonerado": d['exonerado'],
            "descuento_igv": d['igv'],
            "descuento_total": d['total']
        })

    return flat_data

def generar_facturas(cantidad: int, output_dir: str, verbose: bool = True):
    """
    Genera múltiples facturas ficticias con tipos variados
    """
    if verbose:
        print(f"{'='*60}")
        print(f"Generador de Facturas Ficticias - Versión Mejorada (Fase 2)")
        print(f"{'='*60}")
        print(f"Cantidad a generar: {cantidad}")
        print(f"Directorio de salida: {output_dir}")
        print(f"{'='*60}\n")

    # Crear generadores
    gen_factura = FacturaGenerator()
    gen_pdf = PDFFactura(output_dir=output_dir)

    facturas_generadas = []

    # Tipos de facturas disponibles
    tipos_factura = ['general', 'hotel', 'seguro', 'con_descuento']
    categorias_items = ['construccion', 'comida', 'servicios', 'hoteles', 'combustibles', 'seguros', 'seguridad']

    for i in range(cantidad):
        try:
            if verbose:
                print(f"[{i+1}/{cantidad}] Generando factura...", end=" ")

            # Seleccionar tipo de factura de forma variada
            tipo = tipos_factura[i % len(tipos_factura)]

            # Ajustar categoría según tipo
            if tipo == 'hotel':
                categoria = 'hoteles'
            elif tipo == 'seguro':
                categoria = 'seguros'
            else:
                # Variar entre todas las categorías
                categoria = categorias_items[i % len(categorias_items)]

            # Variar moneda
            monedas_list = ['PEN', 'USD', 'EUR']
            moneda = monedas_list[i % len(monedas_list)]

            # Variar crédito
            con_credito = (i % 3 == 0)  # 1 de cada 3 a crédito

            # Generar datos de factura
            factura = gen_factura.generar_factura(
                tipo_factura=tipo,
                categoria_items=categoria,
                num_items=None,  # Aleatorio
                moneda=moneda,
                con_credito=con_credito
            )

            # Crear PDF
            archivo = gen_pdf.crear_factura(factura)
            
            # Guardar JSON (Estructura Plana Fase 2)
            json_filename = os.path.basename(archivo).replace('.pdf', '.json')
            json_path = os.path.join(output_dir, json_filename)
            
            # Aplanar datos antes de guardar
            flat_factura = flatten_json(factura)
            
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(flat_factura, f, cls=DateEncoder, indent=4, ensure_ascii=False)

            facturas_generadas.append(archivo)

            if verbose:
                tipo_desc = f"[{tipo.upper()}]"
                print(f"✓ {tipo_desc} {factura['numero_factura']} - {factura['simbolo_moneda']}{factura['total']:.2f}")
                print(f"  -> JSON: {json_filename}")

        except Exception as e:
            if verbose:
                print(f"✗ Error: {str(e)}")
                import traceback
                traceback.print_exc()
            continue

    if verbose:
        print(f"\n{'='*60}")
        print(f"Proceso completado:")
        print(f"  - Facturas generadas: {len(facturas_generadas)}/{cantidad}")
        print(f"  - Ubicación: {output_dir}")
        print(f"\nTipos generados:")
        print(f"  - Generales / Construcción / Comida / Servicios")
        print(f"  - Hoteles (con check-in/out, noches, huésped)")
        print(f"  - Seguros (con pólizas y vigencias)")
        print(f"  - Con descuentos (tabla de descuentos)")
        print(f"{'='*60}")

    return facturas_generadas


def analizar_facturas_originales(input_dir: str):
    """
    Analiza facturas originales en el directorio de entrada

    Args:
        input_dir: Directorio con facturas originales
    """
    print(f"{'='*60}")
    print(f"Análisis de Facturas Originales")
    print(f"{'='*60}")
    print(f"Directorio: {input_dir}")
    print(f"{'='*60}\n")

    if not os.path.exists(input_dir):
        print(f"Error: El directorio '{input_dir}' no existe.")
        return

    # Buscar archivos PDF e imágenes
    extensiones = ['.pdf', '.png', '.jpg', '.jpeg', '.tiff', '.tif']
    archivos = []

    for ext in extensiones:
        archivos.extend(Path(input_dir).rglob(f"*{ext}"))

    if not archivos:
        print(f"No se encontraron facturas en '{input_dir}'")
        print(f"Extensiones buscadas: {', '.join(extensiones)}")
        return

    print(f"Se encontraron {len(archivos)} archivos:\n")
    for i, archivo in enumerate(archivos, 1):
        print(f"  {i}. {archivo.name} ({archivo.suffix.upper()[1:]})")

    print(f"\n{'='*60}")
    print("NOTA: El análisis detallado de PDFs e imágenes requiere")
    print("herramientas adicionales (OCR, extracción de PDF).")
    print("Para una implementación completa, se recomienda:")
    print("  - PyPDF2 / pdfplumber para PDFs")
    print("  - Tesseract OCR para imágenes")
    print("  - OpenCV para procesamiento de imágenes")
    print(f"{'='*60}")

    return archivos


def main():
    parser = argparse.ArgumentParser(
        description="Generador de Facturas Ficticias",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:

  # Generar 50 facturas
  python main.py --cantidad 50

  # Generar 100 facturas en directorio específico
  python main.py --cantidad 100 --output ./mis_facturas/

  # Analizar facturas originales
  python main.py --analizar --input ./facturas_originales/

  # Generar facturas basándose en análisis previo
  python main.py --cantidad 200 --input ./facturas_originales/ --output ./generadas/
        """
    )

    parser.add_argument(
        '--cantidad',
        type=int,
        default=10,
        help='Cantidad de facturas a generar (default: 10)'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='facturas_generadas',
        help='Directorio de salida para facturas generadas (default: facturas_generadas)'
    )

    parser.add_argument(
        '--input',
        type=str,
        default='facturas_originales',
        help='Directorio con facturas originales para análisis (default: facturas_originales)'
    )

    parser.add_argument(
        '--analizar',
        action='store_true',
        help='Analizar facturas originales antes de generar'
    )

    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Modo silencioso (sin output detallado)'
    )

    args = parser.parse_args()

    verbose = not args.quiet

    try:
        # Si se solicita análisis, hacerlo primero
        if args.analizar:
            analizar_facturas_originales(args.input)
            print("\n")

        # Generar facturas
        generar_facturas(
            cantidad=args.cantidad,
            output_dir=args.output,
            verbose=verbose
        )

    except KeyboardInterrupt:
        print("\n\nProceso interrumpido por el usuario.")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
