import os
import shutil
import random
from src.generator import FacturaGenerator
from src.pdf_creator import PDFFactura

def generar_lote_final():
    output_dir = "facturas_finales"
    
    # Limpiar directorio si existe, o crearlo
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    gen = FacturaGenerator()
    
    # Listas de opciones
    tipos_factura = [
        'general', 'hotel', 'restaurante', 'transporte', 
        'servicios_profesionales', 'con_descuento'
    ]
    estilos = [
        "clasico", "moderno", "minimalista", 
        "corporativo", "creativo", "industrial"
    ]
    
    print(f"Generando 20 facturas diversas en '{output_dir}'...")

    for i in range(1, 21):
        # Selección aleatoria pero ponderada para asegurar variedad
        tipo = random.choice(tipos_factura)
        estilo = random.choice(estilos)
        
        # Opciones adicionales aleatorias
        con_credito = random.choice([True, False])
        
        # Generar datos
        datos = gen.generar_factura(tipo_factura=tipo, con_credito=con_credito)
        
        # Casos especiales aleatorios para probar robustez
        if i % 5 == 0: # Cada 5 facturas, una con descripción larga
            datos['items'][0]['descripcion'] = "Ítem con descripción extendida para prueba de ajuste de texto en el documento final. " * 5
        
        if i % 7 == 0: # Cada 7 facturas, una con muchos ítems
            for k in range(15):
                datos['items'].append({
                    'numero': k + 10,
                    'descripcion': f"Item extra {k}",
                    'unidad': 'UND',
                    'cantidad': 1,
                    'precio_unitario': 10,
                    'valor_venta': 10,
                    'total': 11.8
                })
                
        if i % 4 == 0: # Cada 4 facturas, observaciones largas
            datos['observaciones'] = "Observaciones extensas para verificar el comportamiento del pie de página dinámico. " * 3

        # Crear PDF
        pdf = PDFFactura(output_dir=output_dir, estilo=estilo)
        filename = f"{i:02d}_Factura_{tipo.capitalize()}_{estilo.capitalize()}.pdf"
        
        try:
            ruta = pdf.crear_factura(datos, filename=filename)
            print(f"[{i}/20] Generada: {filename}")
        except Exception as e:
            print(f"[{i}/20] Error generando {filename}: {e}")

    print(f"\n✅ Proceso completado. 20 facturas disponibles en '{output_dir}'.")

if __name__ == "__main__":
    generar_lote_final()
