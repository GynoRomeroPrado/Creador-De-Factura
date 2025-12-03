import os
import json
import random
from datetime import datetime
from src.generator import FacturaGenerator
from src.pdf_creator import PDFFactura

class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super(DateTimeEncoder, self).default(obj)

def generar_json_pruebas():
    output_dir = "pruebas_json"
    os.makedirs(output_dir, exist_ok=True)
    
    gen = FacturaGenerator()
    pdf_gen = PDFFactura(output_dir=output_dir, estilo="moderno")
    
    print(f"Generando 5 facturas de prueba con JSON en '{output_dir}'...\n")
    
    for i in range(5):
        # Variar tipos para tener diversidad en los JSON
        tipo = random.choice(["general", "hotel", "restaurante", "servicios_profesionales", "transporte"])
        
        print(f"[{i+1}/5] Generando factura tipo: {tipo}")
        
        # Generar datos
        datos = gen.generar_factura(tipo_factura=tipo)
        
        # Nombre base
        nombre_base = f"Factura_{i+1:02d}_{tipo}_{datos['numero']}"
        
        # Guardar JSON
        ruta_json = os.path.join(output_dir, f"{nombre_base}.json")
        with open(ruta_json, 'w', encoding='utf-8') as f:
            json.dump(datos, f, cls=DateTimeEncoder, indent=4, ensure_ascii=False)
            
        # Crear PDF (para referencia visual)
        ruta_pdf = pdf_gen.crear_factura(datos, filename=f"{nombre_base}.pdf")
        
        print(f"   -> JSON: {ruta_json}")
        print(f"   -> PDF:  {ruta_pdf}")

    print("\n✅ Generación completada.")

if __name__ == "__main__":
    generar_json_pruebas()
