import os
import shutil
import random
from src.generator import FacturaGenerator
from src.pdf_creator import PDFFactura

def generar_lote_realista():
    output_dir = "facturas_realistas_final"
    
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)
    os.makedirs(output_dir)

    gen = FacturaGenerator()
    
    # Tipos y estilos variados
    escenarios = [
        ('hotel', 'corporativo'),
        ('restaurante', 'creativo'),
        ('transporte', 'industrial'),
        ('servicios_profesionales', 'clasico'),
        ('general', 'moderno'), # Tech items
        ('general', 'minimalista'), # Construccion items
        ('con_descuento', 'corporativo'),
        ('compra_grande', 'industrial'),
    ]
    
    print(f"Generando 20 facturas realistas en '{output_dir}'...")

    for i in range(1, 21):
        if i <= len(escenarios):
            tipo, estilo = escenarios[i-1]
            # Forzar categorías específicas para los generales
            cat = None
            if i == 5: cat = 'tech'
            if i == 6: cat = 'construccion'
        else:
            tipo = random.choice(FacturaGenerator.TIPOS_FACTURA)
            estilo = random.choice(["clasico", "moderno", "minimalista", "corporativo", "creativo", "industrial"])
            cat = None

        # Generar datos
        datos = gen.generar_factura(tipo_factura=tipo, categoria_items=cat)
        
        # Crear PDF
        pdf = PDFFactura(output_dir=output_dir, estilo=estilo)
        filename = f"{i:02d}_{datos['industria'].capitalize()}_{estilo.capitalize()}.pdf"
        
        try:
            ruta = pdf.crear_factura(datos, filename=filename)
            print(f"[{i}/20] Generada: {filename} (Industria: {datos['industria']})")
        except Exception as e:
            print(f"[{i}/20] Error generando {filename}: {e}")
            import traceback
            traceback.print_exc()

    print(f"\n✅ Proceso completado. Revisar '{output_dir}'.")

if __name__ == "__main__":
    generar_lote_realista()
