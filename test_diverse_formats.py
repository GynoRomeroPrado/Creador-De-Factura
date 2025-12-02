import os
from src.generator import FacturaGenerator
from src.pdf_creator import PDFFactura

def test_diverse_formats():
    output_dir = "test_pdfs_diversos"
    os.makedirs(output_dir, exist_ok=True)
    
    gen = FacturaGenerator()
    
    # 1. Estilo Clásico
    print("Generando factura Clásica...")
    pdf_gen = PDFFactura(output_dir=output_dir, estilo="clasico")
    datos = gen.generar_factura(tipo_factura='general')
    archivo = pdf_gen.crear_factura(datos, filename="factura_clasica.pdf")
    print(f"Generada: {archivo}")
    
    # 2. Estilo Moderno
    print("Generando factura Moderna...")
    pdf_gen = PDFFactura(output_dir=output_dir, estilo="moderno")
    datos = gen.generar_factura(tipo_factura='con_descuento')
    archivo = pdf_gen.crear_factura(datos, filename="factura_moderna.pdf")
    print(f"Generada: {archivo}")
    
    # 3. Estilo Minimalista
    print("Generando factura Minimalista...")
    pdf_gen = PDFFactura(output_dir=output_dir, estilo="minimalista")
    datos = gen.generar_factura(tipo_factura='hotel')
    archivo = pdf_gen.crear_factura(datos, filename="factura_minimalista.pdf")
    print(f"Generada: {archivo}")
    
    # 4. Estilo Corporativo - Servicios Profesionales
    print("Generando factura Corporativa (Servicios)...")
    pdf_gen = PDFFactura(output_dir=output_dir, estilo="corporativo")
    datos = gen.generar_factura(tipo_factura='servicios_profesionales')
    archivo = pdf_gen.crear_factura(datos, filename="factura_corporativa_servicios.pdf")
    print(f"Generada: {archivo}")

    # 5. Estilo Creativo - Restaurante
    print("Generando factura Creativa (Restaurante)...")
    pdf_gen = PDFFactura(output_dir=output_dir, estilo="creativo")
    datos = gen.generar_factura(tipo_factura='restaurante')
    archivo = pdf_gen.crear_factura(datos, filename="factura_creativa_restaurante.pdf")
    print(f"Generada: {archivo}")

    # 6. Estilo Industrial - Transporte
    print("Generando factura Industrial (Transporte)...")
    pdf_gen = PDFFactura(output_dir=output_dir, estilo="industrial")
    datos = gen.generar_factura(tipo_factura='transporte')
    archivo = pdf_gen.crear_factura(datos, filename="factura_industrial_transporte.pdf")
    print(f"Generada: {archivo}")

    # 7. Prueba de texto largo (wrapping)
    print("Generando factura con texto largo...")
    pdf_gen = PDFFactura(output_dir=output_dir, estilo="clasico")
    datos = gen.generar_factura(tipo_factura='general')
    # Forzar texto largo
    datos['items'][0]['descripcion'] = "Esta es una descripción extremadamente larga para probar si el sistema de ajuste de texto funciona correctamente y salta de línea cuando es necesario sin cortar el texto ni superponerse con otras columnas." * 2
    archivo = pdf_gen.crear_factura(datos, filename="factura_texto_largo.pdf")
    print(f"Generada: {archivo}")

if __name__ == "__main__":
    test_diverse_formats()
