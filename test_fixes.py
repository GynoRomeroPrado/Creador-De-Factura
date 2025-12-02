import os
import random
from datetime import datetime
from src.generator import FacturaGenerator
from src.pdf_creator import PDFFactura

def generar_facturas_prueba():
    output_dir = "facturas_verificacion_final"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    gen = FacturaGenerator()
    estilos = ["clasico", "moderno", "minimalista", "corporativo", "creativo", "industrial"]
    
    print(f"Generando 10 facturas de prueba en '{output_dir}'...")

    # 1. Factura con Item de Descripción MUY LARGA (Test de división)
    print("1. Generando Factura con Descripción Larga...")
    datos = gen.generar_factura(tipo_factura='general')
    datos['items'][0]['descripcion'] = "Este es un ítem de prueba con una descripción extremadamente larga para verificar que el sistema de división de texto funciona correctamente. " * 10
    datos['items'][0]['cantidad'] = 1
    datos['items'][0]['precio_unitario'] = 100.00
    datos['items'][0]['valor_venta'] = 100.00
    datos['items'][0]['total'] = 118.00
    pdf = PDFFactura(output_dir=output_dir, estilo="clasico")
    pdf.crear_factura(datos, filename="01_Descripcion_Larga_Clasico.pdf")

    # 2. Factura con MUCHOS items (Test de salto de página múltiple)
    print("2. Generando Factura con Múltiples Páginas...")
    datos = gen.generar_factura(tipo_factura='general')
    # Añadir 30 items
    items_extra = []
    for i in range(30):
        items_extra.append({
            'numero': i + 2,
            'descripcion': f"Item extra número {i+2} para llenar espacio",
            'unidad': 'NIU',
            'cantidad': 1,
            'precio_unitario': 10.00,
            'valor_venta': 10.00,
            'total': 11.80
        })
    datos['items'].extend(items_extra)
    # Recalcular totales simplificado
    datos['op_gravada'] = sum(i['valor_venta'] for i in datos['items'])
    datos['igv'] = datos['op_gravada'] * 0.18
    datos['total'] = datos['op_gravada'] + datos['igv']
    pdf = PDFFactura(output_dir=output_dir, estilo="moderno")
    pdf.crear_factura(datos, filename="02_Multiples_Paginas_Moderno.pdf")

    # 3. Factura de Hotel con muchos cargos (Test de pie de página dinámico)
    print("3. Generando Factura Hotel Compleja...")
    datos = gen.generar_factura(tipo_factura='hotel', con_credito=True)
    pdf = PDFFactura(output_dir=output_dir, estilo="corporativo")
    pdf.crear_factura(datos, filename="03_Hotel_Corporativo.pdf")

    # 4. Factura con Descuentos y Totales complejos
    print("4. Generando Factura con Descuentos...")
    datos = gen.generar_factura(tipo_factura='con_descuento')
    pdf = PDFFactura(output_dir=output_dir, estilo="industrial")
    pdf.crear_factura(datos, filename="04_Descuentos_Industrial.pdf")

    # 5. Factura Restaurante (Estilo Creativo)
    print("5. Generando Factura Restaurante...")
    datos = gen.generar_factura(tipo_factura='restaurante')
    pdf = PDFFactura(output_dir=output_dir, estilo="creativo")
    pdf.crear_factura(datos, filename="05_Restaurante_Creativo.pdf")

    # 6. Factura Transporte (Estilo Minimalista)
    print("6. Generando Factura Transporte...")
    datos = gen.generar_factura(tipo_factura='transporte')
    pdf = PDFFactura(output_dir=output_dir, estilo="minimalista")
    pdf.crear_factura(datos, filename="06_Transporte_Minimalista.pdf")

    # 7. Factura Servicios Profesionales (Estilo Clásico)
    print("7. Generando Factura Servicios...")
    datos = gen.generar_factura(tipo_factura='servicios_profesionales')
    pdf = PDFFactura(output_dir=output_dir, estilo="clasico")
    pdf.crear_factura(datos, filename="07_Servicios_Clasico.pdf")

    # 8. Factura con Item Largo Y Muchos Items (Caso extremo)
    print("8. Generando Factura Extrema (Larga + Muchos Items)...")
    datos = gen.generar_factura(tipo_factura='general')
    datos['items'][0]['descripcion'] = "Descripción larga al inicio. " * 5
    for i in range(15):
        datos['items'].append({
            'numero': i + 2,
            'descripcion': f"Item de relleno {i+2}",
            'unidad': 'ZZ',
            'cantidad': 1,
            'precio_unitario': 50.00,
            'valor_venta': 50.00,
            'total': 59.00
        })
    pdf = PDFFactura(output_dir=output_dir, estilo="creativo")
    pdf.crear_factura(datos, filename="08_Extrema_Creativo.pdf")

    # 9. Factura con Pie de Página grande (Observaciones largas)
    print("9. Generando Factura con Observaciones Largas...")
    datos = gen.generar_factura(tipo_factura='general')
    datos['observaciones'] = "Esta es una observación muy larga que debería ocupar varias líneas en el pie de página para verificar que no se superpone con el total y que el layout dinámico funciona correctamente. " * 5
    pdf = PDFFactura(output_dir=output_dir, estilo="corporativo")
    pdf.crear_factura(datos, filename="09_Observaciones_Largas_Corp.pdf")

    # 10. Factura Estándar (Control)
    print("10. Generando Factura Estándar de Control...")
    datos = gen.generar_factura(tipo_factura='general')
    pdf = PDFFactura(output_dir=output_dir, estilo="moderno")
    pdf.crear_factura(datos, filename="10_Estandar_Moderno.pdf")

    print(f"\n✅ Se generaron 10 facturas en '{output_dir}'. Por favor revisar.")

if __name__ == "__main__":
    generar_facturas_prueba()
