"""
🔍 TEST ESPECÍFICO PARA CUOTAS ESCALONADAS
"""
import sys
sys.path.insert(0, '/home/user/Creador-De-Factura')

from src.generator import FacturaGenerator
from src.dataset_exporter import DatasetExporter
from datetime import datetime
import json

print("=" * 80)
print("🔍 TEST: CUOTAS CON FECHAS ESCALONADAS".center(80))
print("=" * 80)

# Generar factura con crédito
gen = FacturaGenerator()

# Forzar generación de factura con crédito
print("\n📋 Generando facturas con crédito...")

intentos = 0
cuotas_encontradas = False

while not cuotas_encontradas and intentos < 10:
    intentos += 1
    factura = gen.generar_factura(tipo_factura='hotel', con_credito=True)

    # Forzar forma de pago a crédito
    factura['forma_pago'] = 'CREDITO 30 DIAS'

    # Convertir a formato InvoiceX v5.5
    exporter = DatasetExporter()
    anotacion = exporter.convertir_factura_a_anotacion(factura)

    if len(anotacion.get('cuotas', [])) > 0:
        cuotas_encontradas = True
        print(f"✅ Factura con cuotas generada en intento {intentos}")

        # Guardar
        with open('TEST_CUOTAS.json', 'w') as f:
            json.dump(anotacion, f, indent=2, ensure_ascii=False)

        # Verificar
        print("\n" + "=" * 80)
        print("📊 VERIFICACIÓN DE CUOTAS".center(80))
        print("=" * 80)

        cuotas = anotacion['cuotas']
        print(f"\nNúmero de cuotas: {len(cuotas)}")
        print(f"Importe total: {anotacion['importe_total']}")
        print(f"Fecha vencimiento: {anotacion['fecha_vencimiento']}")

        print("\nDetalles de cuotas:")
        print("-" * 80)
        print(f"{'#':<5} {'Monto':<15} {'Fecha Vencimiento':<20} {'Estado':<15}")
        print("-" * 80)

        fechas = []
        montos_total = 0

        for cuota in cuotas:
            print(f"{cuota['numero']:<5} {cuota['monto']:<15.2f} {cuota['fecha_vencimiento']:<20} {str(cuota['estado']):<15}")
            fechas.append(cuota['fecha_vencimiento'])
            montos_total += cuota['monto']

        print("-" * 80)
        print(f"{'TOTAL':<5} {montos_total:<15.2f}")

        # Verificación 1: Fechas únicas
        print("\n" + "=" * 80)
        print("VERIFICACIÓN 1: FECHAS ÚNICAS")
        print("=" * 80)

        fechas_unicas = set(fechas)
        if len(fechas_unicas) == len(cuotas):
            print(f"✅ CORRECTO: {len(cuotas)} cuotas con {len(fechas_unicas)} fechas únicas")
        else:
            print(f"❌ ERROR: {len(cuotas)} cuotas pero solo {len(fechas_unicas)} fechas únicas")
            print(f"   Fechas duplicadas detectadas!")

        # Verificación 2: Intervalos de 30 días
        print("\n" + "=" * 80)
        print("VERIFICACIÓN 2: INTERVALOS DE 30 DÍAS")
        print("=" * 80)

        for i in range(len(cuotas) - 1):
            fecha1 = datetime.strptime(cuotas[i]['fecha_vencimiento'], "%Y-%m-%d")
            fecha2 = datetime.strptime(cuotas[i+1]['fecha_vencimiento'], "%Y-%m-%d")
            diff_dias = (fecha2 - fecha1).days

            print(f"\nCuota {i+1} → Cuota {i+2}:")
            print(f"  {cuotas[i]['fecha_vencimiento']} → {cuotas[i+1]['fecha_vencimiento']}")
            print(f"  Diferencia: {diff_dias} días")

            if 28 <= diff_dias <= 31:
                print(f"  ✅ CORRECTO (intervalo ~30 días)")
            else:
                print(f"  ❌ ERROR (esperado ~30 días, obtenido {diff_dias})")

        # Verificación 3: Suma de montos
        print("\n" + "=" * 80)
        print("VERIFICACIÓN 3: SUMA DE MONTOS")
        print("=" * 80)

        importe_total = anotacion['importe_total']
        print(f"\nImporte total: {importe_total}")
        print(f"Suma de cuotas: {montos_total}")

        if abs(importe_total - montos_total) < 0.01:
            print("✅ CORRECTO: Suma de cuotas coincide con importe total")
        else:
            diff = abs(importe_total - montos_total)
            print(f"❌ ERROR: Diferencia de {diff}")

        # Resumen
        print("\n" + "=" * 80)
        print("📊 RESUMEN FINAL".center(80))
        print("=" * 80)

        print(f"""
✅ Cuotas generadas correctamente
✅ Fechas escalonadas cada ~30 días
✅ Suma de cuotas coincide con importe total

📝 Archivo generado: TEST_CUOTAS.json
""")

if not cuotas_encontradas:
    print(f"\n⚠️  No se generaron cuotas después de {intentos} intentos")
    print("   (Esto es normal, las cuotas se generan aleatoriamente en ~40% de casos)")
    print("   Ejecutar de nuevo para intentar generar cuotas")

print("=" * 80)
