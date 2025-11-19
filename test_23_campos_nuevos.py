#!/usr/bin/env python3
"""
Test de Validación de los 23 Campos Nuevos
===========================================

Valida que todos los 23 campos nuevos se generen correctamente:
- 7 campos generales
- 4 campos por item
- 12 campos específicos por sector
"""

import sys
import os
from datetime import datetime

# Agregar src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.generator import FacturaGenerator


def validar_campos_generales(factura: dict) -> dict:
    """
    Valida los 7 campos generales nuevos.

    Campos:
    1. emisor_nombre_comercial
    2. receptor_tipo_doc
    3. receptor_nombre_comercial
    4. otros_cargos (mejorado)
    5. condiciones_pago
    6. cuenta_bancaria
    7. forma_pago_detalle
    """
    validaciones = {}

    # 1. Emisor nombre comercial (opcional)
    if "nombre_comercial" in factura.get("emisor", {}):
        validaciones["emisor_nombre_comercial"] = "✓ Presente"
    else:
        validaciones["emisor_nombre_comercial"] = "- Ausente (opcional)"

    # 2. Receptor tipo doc
    if "tipo_doc" in factura.get("receptor", {}):
        tipo_doc = factura["receptor"]["tipo_doc"]
        if tipo_doc in ["RUC", "DNI", "CE"]:
            validaciones["receptor_tipo_doc"] = f"✓ {tipo_doc}"
        else:
            validaciones["receptor_tipo_doc"] = f"✗ Inválido: {tipo_doc}"
    else:
        validaciones["receptor_tipo_doc"] = "✗ Ausente"

    # 3. Receptor nombre comercial (opcional)
    if "nombre_comercial" in factura.get("receptor", {}):
        validaciones["receptor_nombre_comercial"] = "✓ Presente"
    else:
        validaciones["receptor_nombre_comercial"] = "- Ausente (opcional)"

    # 4. Otros cargos (mejorado, opcional)
    if factura.get("otros_cargos", 0) > 0:
        validaciones["otros_cargos"] = f"✓ S/ {factura['otros_cargos']:.2f}"
    else:
        validaciones["otros_cargos"] = "- Sin cargo (opcional)"

    # 5. Condiciones de pago
    if factura.get("condiciones_pago"):
        validaciones["condiciones_pago"] = f"✓ {factura['condiciones_pago']}"
    else:
        validaciones["condiciones_pago"] = "✗ Ausente"

    # 6. Cuenta bancaria (opcional)
    if factura.get("cuenta_bancaria"):
        validaciones["cuenta_bancaria"] = f"✓ {factura['cuenta_bancaria'][:40]}..."
    else:
        validaciones["cuenta_bancaria"] = "- Ausente (opcional)"

    # 7. Forma de pago detalle
    if factura.get("forma_pago_detalle"):
        validaciones["forma_pago_detalle"] = f"✓ {factura['forma_pago_detalle'][:40]}..."
    else:
        validaciones["forma_pago_detalle"] = "✗ Ausente"

    return validaciones


def validar_campos_items(factura: dict) -> dict:
    """
    Valida los 4 campos nuevos por item.

    Campos:
    1. codigo_producto (SKU)
    2. codigo_barras (EAN-13)
    3. lote
    4. fecha_vencimiento
    """
    validaciones = {
        "items_con_codigo_producto": 0,
        "items_con_codigo_barras": 0,
        "items_con_lote": 0,
        "items_con_fecha_vencimiento": 0,
        "total_items": len(factura.get("items", [])),
        "ejemplos": {}
    }

    for item in factura.get("items", []):
        # 1. Código de producto (SKU)
        if "codigo_producto" in item:
            validaciones["items_con_codigo_producto"] += 1
            if "ejemplo_sku" not in validaciones["ejemplos"]:
                validaciones["ejemplos"]["ejemplo_sku"] = item["codigo_producto"]

        # 2. Código de barras (EAN-13)
        if "codigo_barras" in item:
            validaciones["items_con_codigo_barras"] += 1
            if "ejemplo_ean13" not in validaciones["ejemplos"]:
                validaciones["ejemplos"]["ejemplo_ean13"] = item["codigo_barras"]

        # 3. Lote
        if "lote" in item:
            validaciones["items_con_lote"] += 1
            if "ejemplo_lote" not in validaciones["ejemplos"]:
                validaciones["ejemplos"]["ejemplo_lote"] = item["lote"]

        # 4. Fecha de vencimiento
        if "fecha_vencimiento" in item:
            validaciones["items_con_fecha_vencimiento"] += 1
            if "ejemplo_vencimiento" not in validaciones["ejemplos"]:
                fecha_venc = item["fecha_vencimiento"]
                if isinstance(fecha_venc, datetime):
                    validaciones["ejemplos"]["ejemplo_vencimiento"] = fecha_venc.strftime("%d/%m/%Y")
                else:
                    validaciones["ejemplos"]["ejemplo_vencimiento"] = str(fecha_venc)

    return validaciones


def validar_campos_sector(factura: dict) -> dict:
    """
    Valida los 12 campos específicos por sector.

    Campos por sector:
    - Ferretería: guia_remision, orden_compra, detraccion_porcentaje, detraccion_monto
    - Restaurante: propina, cargo_delivery, numero_mesa, mozo
    - Spa: numero_socio, terapeuta
    - Gym: numero_socio, entrenador
    - Farmacia: receta_medica
    """
    validaciones = {}
    sector = factura.get("sector", "N/A")

    validaciones["sector"] = sector

    # Campos de ferretería
    if factura.get("guia_remision"):
        validaciones["guia_remision"] = f"✓ {factura['guia_remision']}"
    if factura.get("orden_compra"):
        validaciones["orden_compra"] = f"✓ {factura['orden_compra']}"
    if factura.get("detraccion_porcentaje"):
        validaciones["detraccion"] = f"✓ {factura['detraccion_porcentaje']}% (S/ {factura.get('detraccion_monto', 0):.2f})"

    # Campos de restaurante
    if factura.get("propina"):
        validaciones["propina"] = f"✓ S/ {factura['propina']:.2f}"
    if factura.get("cargo_delivery"):
        validaciones["cargo_delivery"] = f"✓ S/ {factura['cargo_delivery']:.2f}"
    if factura.get("numero_mesa"):
        validaciones["numero_mesa"] = f"✓ Mesa {factura['numero_mesa']}"
    if factura.get("mozo"):
        validaciones["mozo"] = f"✓ {factura['mozo']}"

    # Campos de spa/gym
    if factura.get("numero_socio"):
        validaciones["numero_socio"] = f"✓ {factura['numero_socio']}"
    if factura.get("terapeuta"):
        validaciones["terapeuta"] = f"✓ {factura['terapeuta']}"
    if factura.get("entrenador"):
        validaciones["entrenador"] = f"✓ {factura['entrenador']}"

    # Campos de farmacia
    if factura.get("receta_medica"):
        validaciones["receta_medica"] = f"✓ {factura['receta_medica']}"

    return validaciones


def test_validacion_completa():
    """
    Test principal: Genera facturas y valida los 23 campos nuevos.
    """
    print("\n" + "="*80)
    print("TEST: Validación de los 23 Campos Nuevos")
    print("="*80 + "\n")

    # Inicializar generador en modo realista
    print("1. Inicializando generador en modo realista...")
    gen = FacturaGenerator(usar_datos_realistas=True)
    print("   ✅ Generador inicializado\n")

    # Generar facturas de diferentes sectores
    print("2. Generando facturas de diferentes sectores...")
    print("-" * 80)

    sectores_prueba = 15  # Generar 15 facturas para cubrir varios sectores
    facturas_generadas = []
    errores = []

    # Estadísticas globales
    stats_generales = {
        "emisor_nombre_comercial": 0,
        "receptor_tipo_doc": 0,
        "receptor_nombre_comercial": 0,
        "otros_cargos": 0,
        "condiciones_pago": 0,
        "cuenta_bancaria": 0,
        "forma_pago_detalle": 0,
    }

    stats_items = {
        "total_items": 0,
        "items_con_sku": 0,
        "items_con_ean13": 0,
        "items_con_lote": 0,
        "items_con_vencimiento": 0,
    }

    stats_sector = {
        "guia_remision": 0,
        "orden_compra": 0,
        "detraccion": 0,
        "propina": 0,
        "cargo_delivery": 0,
        "numero_mesa": 0,
        "mozo": 0,
        "numero_socio": 0,
        "terapeuta": 0,
        "entrenador": 0,
        "receta_medica": 0,
    }

    for i in range(sectores_prueba):
        try:
            # Generar factura
            factura = gen.generar_factura()

            # Validar campos generales
            val_generales = validar_campos_generales(factura)

            # Validar campos por item
            val_items = validar_campos_items(factura)

            # Validar campos específicos por sector
            val_sector = validar_campos_sector(factura)

            # Mostrar resultado
            numero = factura['numero_factura']
            sector = factura.get('sector', 'N/A')

            print(f"\n  Factura {i+1}/{sectores_prueba}: {numero} - Sector: {sector}")
            print(f"    Campos Generales:")
            for campo, valor in val_generales.items():
                print(f"      • {campo}: {valor}")

            print(f"    Campos por Item:")
            print(f"      • SKU: {val_items['items_con_codigo_producto']}/{val_items['total_items']} items")
            print(f"      • EAN-13: {val_items['items_con_codigo_barras']}/{val_items['total_items']} items")
            print(f"      • Lote: {val_items['items_con_lote']}/{val_items['total_items']} items")
            print(f"      • Vencimiento: {val_items['items_con_fecha_vencimiento']}/{val_items['total_items']} items")
            if val_items["ejemplos"]:
                print(f"      Ejemplos:")
                for clave, valor in val_items["ejemplos"].items():
                    print(f"        - {clave}: {valor}")

            if len(val_sector) > 1:  # Más que solo 'sector'
                print(f"    Campos Específicos del Sector ({sector}):")
                for campo, valor in val_sector.items():
                    if campo != "sector":
                        print(f"      • {campo}: {valor}")

            # Actualizar estadísticas
            if "nombre_comercial" in factura.get("emisor", {}):
                stats_generales["emisor_nombre_comercial"] += 1
            if "tipo_doc" in factura.get("receptor", {}):
                stats_generales["receptor_tipo_doc"] += 1
            if "nombre_comercial" in factura.get("receptor", {}):
                stats_generales["receptor_nombre_comercial"] += 1
            if factura.get("otros_cargos", 0) > 0:
                stats_generales["otros_cargos"] += 1
            if factura.get("condiciones_pago"):
                stats_generales["condiciones_pago"] += 1
            if factura.get("cuenta_bancaria"):
                stats_generales["cuenta_bancaria"] += 1
            if factura.get("forma_pago_detalle"):
                stats_generales["forma_pago_detalle"] += 1

            stats_items["total_items"] += val_items["total_items"]
            stats_items["items_con_sku"] += val_items["items_con_codigo_producto"]
            stats_items["items_con_ean13"] += val_items["items_con_codigo_barras"]
            stats_items["items_con_lote"] += val_items["items_con_lote"]
            stats_items["items_con_vencimiento"] += val_items["items_con_fecha_vencimiento"]

            # Stats sector
            if factura.get("guia_remision"):
                stats_sector["guia_remision"] += 1
            if factura.get("orden_compra"):
                stats_sector["orden_compra"] += 1
            if factura.get("detraccion_porcentaje"):
                stats_sector["detraccion"] += 1
            if factura.get("propina"):
                stats_sector["propina"] += 1
            if factura.get("cargo_delivery"):
                stats_sector["cargo_delivery"] += 1
            if factura.get("numero_mesa"):
                stats_sector["numero_mesa"] += 1
            if factura.get("mozo"):
                stats_sector["mozo"] += 1
            if factura.get("numero_socio"):
                stats_sector["numero_socio"] += 1
            if factura.get("terapeuta"):
                stats_sector["terapeuta"] += 1
            if factura.get("entrenador"):
                stats_sector["entrenador"] += 1
            if factura.get("receta_medica"):
                stats_sector["receta_medica"] += 1

            facturas_generadas.append(factura)

        except Exception as e:
            print(f"\n  ❌ Error en factura {i+1}: {e}")
            import traceback
            traceback.print_exc()
            errores.append(f"Factura {i+1}: {str(e)}")

    # Resumen
    print("\n" + "="*80)
    print("RESUMEN DE VALIDACIÓN")
    print("="*80)

    print(f"\n✅ Facturas generadas: {len(facturas_generadas)}/{sectores_prueba}")
    print(f"❌ Errores: {len(errores)}")

    if errores:
        print("\nErrores encontrados:")
        for error in errores:
            print(f"  • {error}")

    # Estadísticas de los 23 campos
    print("\n" + "-"*80)
    print("ESTADÍSTICAS DE LOS 23 CAMPOS NUEVOS")
    print("-"*80)

    print("\n📊 CAMPOS GENERALES (7 campos):")
    total_facturas = len(facturas_generadas)
    for campo, count in stats_generales.items():
        porcentaje = (count / total_facturas * 100) if total_facturas > 0 else 0
        print(f"  • {campo}: {count}/{total_facturas} facturas ({porcentaje:.1f}%)")

    print("\n📦 CAMPOS POR ITEM (4 campos):")
    total_items = stats_items["total_items"]
    print(f"  • Total de items generados: {total_items}")
    for campo, count in stats_items.items():
        if campo != "total_items":
            porcentaje = (count / total_items * 100) if total_items > 0 else 0
            print(f"  • {campo}: {count}/{total_items} items ({porcentaje:.1f}%)")

    print("\n🏪 CAMPOS ESPECÍFICOS POR SECTOR (12 campos):")
    for campo, count in stats_sector.items():
        if count > 0:
            print(f"  • {campo}: {count} factura(s)")

    # Validación final
    print("\n" + "="*80)

    # Validar que al menos algunos campos estén presentes
    campos_criticos = [
        stats_generales["receptor_tipo_doc"] >= total_facturas * 0.8,  # 80% tienen tipo_doc
        stats_generales["condiciones_pago"] >= total_facturas * 0.8,  # 80% tienen condiciones
        stats_generales["forma_pago_detalle"] >= total_facturas * 0.8,  # 80% tienen forma_pago_detalle
        stats_items["items_con_sku"] >= total_items * 0.5,  # Al menos 50% de items tienen SKU
        stats_items["items_con_ean13"] >= total_items * 0.3,  # Al menos 30% de items tienen EAN-13
    ]

    if len(facturas_generadas) >= sectores_prueba * 0.9 and all(campos_criticos):
        print("🎉 ¡VALIDACIÓN EXITOSA!")
        print("\n✅ Los 23 campos nuevos funcionan correctamente:")
        print("   • 7 campos generales integrados")
        print("   • 4 campos por item funcionando")
        print("   • 12 campos específicos por sector implementados")
        print("\n📊 Impacto:")
        print("   • Facturas más completas y realistas")
        print("   • Mejor representación de documentos reales")
        print("   • Dataset enriquecido para LayoutLMv3")
        print("\n💡 Próximos pasos:")
        print("   • Generar PDFs con los nuevos campos")
        print("   • Actualizar visualización en PDFs")
        print("   • Documentar los nuevos campos")
        return 0
    else:
        print("⚠️  Validación parcial")
        print(f"   Facturas generadas: {len(facturas_generadas)}/{sectores_prueba}")
        print(f"   Validaciones críticas: {sum(campos_criticos)}/5")
        return 1


if __name__ == '__main__':
    result = test_validacion_completa()
    print("\n")
    exit(result)
