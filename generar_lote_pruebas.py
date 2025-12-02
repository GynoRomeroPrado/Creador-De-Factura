import os
import random
from src.generator import FacturaGenerator
from src.pdf_creator import PDFFactura

def generar_lote_pruebas():
    # Nombre de la carpeta solicitada
    output_dir = "pruebas_creacion_facturas"
    os.makedirs(output_dir, exist_ok=True)
    
    gen = FacturaGenerator()
    
    # Definir combinaciones interesantes de Estilo + Tipo
    # (Estilo, Tipo de Factura, Sufijo Archivo)
    combinaciones = [
        ("corporativo", "servicios_profesionales", "Servicios_Corp"),
        ("creativo", "restaurante", "Restaurante_Creativo"),
        ("industrial", "transporte", "Transporte_Ind"),
        ("clasico", "hotel", "Hotel_Clasico"),
        ("moderno", "con_descuento", "Venta_Moderna"),
        ("minimalista", "general", "General_Minimal"),
        ("corporativo", "compra_grande", "CompraGrande_Corp"),
        ("creativo", "servicios_profesionales", "Servicios_Creativo"),
        ("industrial", "construccion", "Construccion_Ind"), # Tipo forzado via categoria
        ("moderno", "restaurante", "Restaurante_Moderno")
    ]
    
    print(f"Generando 10 facturas de prueba en '{output_dir}'...\n")
    
    for i in range(10):
        # Si tenemos menos combinaciones definidas que 10, repetimos o elegimos al azar
        if i < len(combinaciones):
            estilo, tipo, sufijo = combinaciones[i]
            categoria = None
            
            # Caso especial para construcción que no es un tipo_factura per se en el generador
            if tipo == "construccion":
                tipo_factura = "general"
                categoria = "construccion"
            else:
                tipo_factura = tipo
        else:
            # Aleatorio para completar
            estilo = random.choice(["clasico", "moderno", "minimalista", "corporativo", "creativo", "industrial"])
            tipo_factura = random.choice(["general", "hotel", "restaurante", "transporte", "servicios_profesionales"])
            sufijo = f"Aleatorio_{i+1}"
            categoria = None

        print(f"[{i+1}/10] Generando: Estilo {estilo.upper()} - Tipo {tipo_factura.upper()}")
        
        # Generar datos
        datos = gen.generar_factura(tipo_factura=tipo_factura, categoria_items=categoria)
        
        # Crear PDF
        pdf_gen = PDFFactura(output_dir=output_dir, estilo=estilo)
        nombre_archivo = f"Factura_{i+1:02d}_{sufijo}.pdf"
        ruta = pdf_gen.crear_factura(datos, filename=nombre_archivo)
        
        print(f"   -> Creado: {ruta}")

    print("\n✅ Generación completada exitosamente.")

if __name__ == "__main__":
    generar_lote_pruebas()
