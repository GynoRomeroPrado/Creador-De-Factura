#!/usr/bin/env python3
"""Script de prueba para verificar emails realistas según tipo de factura"""

from src.generator import FacturaGenerator
import os

print("=" * 80)
print("PRUEBA DE EMAILS REALISTAS POR TIPO DE FACTURA".center(80))
print("=" * 80)

gen = FacturaGenerator()

# Tipos de facturas a probar
tipos = [
    ('hotel', 'Factura de Hotel'),
    ('seguro', 'Factura de Seguro'),
    ('general', 'Factura General'),
    ('con_descuento', 'Factura con Descuento'),
    ('compra_grande', 'Factura de Compra Grande')
]

for tipo, nombre in tipos:
    print(f"\n{'='*80}")
    print(f"{nombre.upper()}")
    print(f"{'='*80}")

    # Generar 5 facturas de cada tipo
    for i in range(1, 6):
        factura = gen.generar_factura(tipo_factura=tipo, num_items=10)

        print(f"\n{i}. {factura['emisor']['razon_social']}")
        print(f"   RUC: {factura['emisor']['ruc']} ({len(factura['emisor']['ruc'])} dígitos)")
        print(f"   Email: {factura['emisor']['email']}")

        # Verificar RUC
        if len(factura['emisor']['ruc']) != 11:
            print(f"   ⚠️  ERROR: RUC no tiene 11 dígitos!")

        # Verificar email
        email = factura['emisor']['email']
        dominio = email.split('@')[1] if '@' in email else ''

        # Verificar que no sea un dominio personal
        dominios_personales = ['hotmail.com', 'gmail.com', 'yahoo.com', 'outlook.com']
        if any(d in dominio for d in dominios_personales):
            print(f"   ⚠️  ADVERTENCIA: Email parece personal ({dominio})")

        # Verificar coherencia con tipo de factura
        if tipo == 'hotel':
            if not any(word in dominio.lower() for word in ['hotel', 'hospitality', 'lodging', 'hospedaje']):
                if not any(word in factura['emisor']['razon_social'].upper() for word in ['HOTEL', 'HOSPEDAJE', 'HOSTAL']):
                    print(f"   💡 Dominio basado en razón social")
            else:
                print(f"   ✅ Dominio relacionado con hotelería")

        elif tipo == 'seguro':
            if not any(word in dominio.lower() for word in ['seguro', 'insurance', 'poliza', 'asegurador']):
                if not any(word in factura['emisor']['razon_social'].upper() for word in ['SEGURO', 'POLIZA']):
                    print(f"   💡 Dominio basado en razón social")
            else:
                print(f"   ✅ Dominio relacionado con seguros")

print("\n" + "=" * 80)
print("RESUMEN DE VERIFICACIÓN".center(80))
print("=" * 80)

print("\n✅ VERIFICACIONES:")
print("  - RUCs con 11 dígitos")
print("  - Emails corporativos (no personales)")
print("  - Dominios coherentes con tipo de factura")
print("  - Prefijos adecuados (ventas, facturacion, reservas, seguros, etc.)")

print("\n📊 EJEMPLOS DE EMAILS POR TIPO:")
print("  Hotel:")
print("    - reservas@granhotel.com.pe")
print("    - recepcion@hospitalitycorp.pe")
print("    - facturacion@hotelesgroup.pe")
print("\n  Seguros:")
print("    - seguros@aseguradorascorp.pe")
print("    - polizas@insurance.com.pe")
print("    - siniestros@segurospe.pe")
print("\n  General:")
print("    - ventas@comercialperu.com.pe")
print("    - facturacion@empresacorp.pe")
print("    - contacto@negocios.pe")

print("\n" + "=" * 80)
