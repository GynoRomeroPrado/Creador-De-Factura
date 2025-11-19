#!/usr/bin/env python3
"""
Códigos de Producto (SKU y EAN-13)
===================================

Genera códigos de producto realistas:
- SKU (Stock Keeping Unit): Códigos internos por sector
- EAN-13: Códigos de barras internacionales con dígito verificador

Uso:
    from src.data.codigos_producto import generar_sku, generar_ean13

    sku = generar_sku('farmacia', 'PARACETAMOL')
    # Resultado: "MED-PARA-500"

    ean = generar_ean13()
    # Resultado: "7750182001234" (con dígito verificador válido)
"""

import random
from typing import Optional


# Prefijos de SKU por sector
PREFIJOS_SKU = {
    'farmacia': ['MED', 'FARM', 'VIT', 'SUP', 'ANT', 'JAR'],
    'restaurante': ['ALI', 'BEB', 'PLA', 'COM', 'ENT', 'POST'],
    'ferreteria': ['HERR', 'MAT', 'PINF', 'ELEC', 'TUBE', 'CEM'],
    'supermercado': ['ALI', 'BEB', 'LIMP', 'PERS', 'HOGAR', 'DESP'],
    'electrodomesticos': ['ELEC', 'LINB', 'COCI', 'REFR', 'LAV', 'TV'],
    'veterinaria': ['VET', 'ALIM', 'ACC', 'MED', 'JUG', 'HIG'],
    'gym': ['EQUIP', 'SUPL', 'ROPA', 'ACC', 'PROT'],
    'spa': ['TRAT', 'PROD', 'SERV', 'TERAPMASAJ'],
    'educacion': ['LIB', 'UTIL', 'UNIF', 'MAT', 'EQUIP'],
    'odontologia': ['DENT', 'IMPL', 'ORTO', 'CONS', 'TRAT'],
    'automotriz': ['AUTO', 'NEUM', 'ACEI', 'FILT', 'BAT', 'REP'],
    'libreria': ['LIB', 'UTIL', 'ART', 'PAPE', 'IMPR'],
    'panaderia': ['PAN', 'PAST', 'TORTA', 'DULCE', 'SAL'],
    'optica': ['LENT', 'MONT', 'ACC', 'SOL', 'CONT'],
    'floristeria': ['FLOR', 'PLANT', 'ARRE', 'MACET', 'SEMIL'],
}

# Prefijos EAN-13 de Perú (775-779)
PREFIJOS_EAN_PERU = ['775', '776', '777', '778', '779']


def generar_sku(sector: str, producto_base: Optional[str] = None) -> str:
    """
    Genera un SKU (Stock Keeping Unit) realista para un producto.

    Formato típico: PREFIJO-CODIGO-VARIANTE
    Ejemplos:
        - MED-PARA-500 (Paracetamol 500mg)
        - HERR-MART-6 (Martillo 6")
        - ALI-ARROZ-1KG (Arroz 1kg)

    Args:
        sector: Sector del negocio
        producto_base: Nombre del producto (opcional)

    Returns:
        SKU generado

    Ejemplos:
        >>> generar_sku('farmacia', 'PARACETAMOL')
        'MED-PARA-500'

        >>> generar_sku('ferreteria', 'MARTILLO')
        'HERR-MART-6'
    """
    # Seleccionar prefijo según sector
    if sector in PREFIJOS_SKU:
        prefijo = random.choice(PREFIJOS_SKU[sector])
    else:
        prefijo = 'PROD'

    # Generar código basado en producto o aleatorio
    if producto_base:
        codigo = _generar_codigo_producto(producto_base)
    else:
        codigo = f"{random.randint(1000, 9999)}"

    # Generar variante/sufijo
    variante = generar_variante_sku(sector)

    return f"{prefijo}-{codigo}-{variante}"


def _generar_codigo_producto(producto: str) -> str:
    """
    Genera un código basado en el nombre del producto.

    Toma las primeras 4 letras del producto.

    Ejemplos:
        "PARACETAMOL" -> "PARA"
        "MARTILLO" -> "MART"
        "ARROZ" -> "ARROZ"  (si es corto, se mantiene)
    """
    # Limpiar el producto
    producto_limpio = producto.upper().replace(' ', '').replace('-', '')

    # Tomar primeras 4 letras (o menos si es corto)
    codigo = producto_limpio[:4]

    return codigo


def generar_variante_sku(sector: str) -> str:
    """
    Genera una variante/sufijo para el SKU según el sector.

    Ejemplos por sector:
        - Farmacia: "500MG", "250ML", "20TAB"
        - Ferretería: "6IN", "1M", "10KG"
        - Alimentos: "1KG", "500G", "2L"
    """
    variantes_sector = {
        'farmacia': [
            f"{random.choice([500, 250, 100, 50, 25, 10])}MG",
            f"{random.choice([500, 250, 120, 100, 60])}ML",
            f"{random.choice([20, 30, 50, 100])}TAB",
            f"{random.choice([10, 20, 30])}CAPS",
        ],
        'ferreteria': [
            f"{random.choice([6, 8, 10, 12, 14, 16])}IN",
            f"{random.choice([1, 2, 3, 5, 10])}M",
            f"{random.choice([1, 5, 10, 25, 50])}KG",
            f"{random.choice([1, 2, 5, 10])}L",
        ],
        'supermercado': [
            f"{random.choice([1, 2, 5, 10])}KG",
            f"{random.choice([250, 500, 1000, 2000])}G",
            f"{random.choice([1, 2, 3])}L",
            f"{random.choice([6, 12, 24])}UND",
        ],
        'electrodomesticos': [
            f"{random.choice([32, 43, 50, 55, 65])}IN",  # TV
            f"{random.choice([250, 300, 350, 400])}L",   # Refrigeradora
            f"{random.choice([4, 8, 16])}GB",            # RAM
        ],
    }

    if sector in variantes_sector:
        return random.choice(variantes_sector[sector])

    # Variante genérica
    return f"{random.randint(1, 999):03d}"


def generar_ean13() -> str:
    """
    Genera un código EAN-13 válido con dígito verificador correcto.

    EAN-13 se compone de:
    - 3 dígitos: Prefijo del país (775-779 para Perú)
    - 4-6 dígitos: Código de empresa
    - 3-5 dígitos: Código de producto
    - 1 dígito: Dígito verificador (calculado)

    Returns:
        EAN-13 de 13 dígitos con dígito verificador válido

    Ejemplos:
        >>> ean = generar_ean13()
        >>> len(ean)
        13
        >>> ean.isdigit()
        True
    """
    # Prefijo de país (Perú)
    prefijo_pais = random.choice(PREFIJOS_EAN_PERU)

    # Código de empresa (4-6 dígitos)
    codigo_empresa = f"{random.randint(1000, 99999):05d}"

    # Código de producto (4 dígitos)
    codigo_producto = f"{random.randint(1000, 9999):04d}"

    # Primeros 12 dígitos
    codigo_base = prefijo_pais + codigo_empresa + codigo_producto

    # Calcular dígito verificador
    digito_verificador = calcular_digito_verificador_ean13(codigo_base)

    return codigo_base + str(digito_verificador)


def calcular_digito_verificador_ean13(codigo_12_digitos: str) -> int:
    """
    Calcula el dígito verificador de un código EAN-13.

    Algoritmo:
    1. Sumar los dígitos en posiciones impares (1, 3, 5, ...) con peso 1
    2. Sumar los dígitos en posiciones pares (2, 4, 6, ...) con peso 3
    3. Sumar ambos resultados
    4. Dígito verificador = (10 - (suma % 10)) % 10

    Args:
        codigo_12_digitos: Primeros 12 dígitos del EAN-13

    Returns:
        Dígito verificador (0-9)

    Ejemplos:
        >>> calcular_digito_verificador_ean13("775018200123")
        4
    """
    if len(codigo_12_digitos) != 12:
        raise ValueError("El código debe tener 12 dígitos")

    suma = 0
    for i, digito in enumerate(codigo_12_digitos):
        peso = 1 if i % 2 == 0 else 3
        suma += int(digito) * peso

    digito_verificador = (10 - (suma % 10)) % 10
    return digito_verificador


def validar_ean13(ean13: str) -> bool:
    """
    Valida si un código EAN-13 es correcto.

    Args:
        ean13: Código EAN-13 de 13 dígitos

    Returns:
        True si es válido, False si no

    Ejemplos:
        >>> validar_ean13("7750182001234")
        True
    """
    if not ean13.isdigit() or len(ean13) != 13:
        return False

    codigo_base = ean13[:12]
    digito_verificador_esperado = int(ean13[12])

    digito_verificador_calculado = calcular_digito_verificador_ean13(codigo_base)

    return digito_verificador_esperado == digito_verificador_calculado


def generar_lote(sector: str) -> str:
    """
    Genera un número de lote realista según el sector.

    Formato típico: LYYYYMM-NNN
    Ejemplos:
        - L202410-001 (Farmacia)
        - L2024-10-A (Alimentos)

    Args:
        sector: Sector del negocio

    Returns:
        Número de lote

    Ejemplos:
        >>> lote = generar_lote('farmacia')
        >>> 'L2024' in lote
        True
    """
    año = random.randint(2023, 2025)
    mes = random.randint(1, 12)

    if sector in ['farmacia', 'supermercado', 'panaderia']:
        # Formato: LYYYYMM-NNN
        numero = random.randint(1, 999)
        return f"L{año}{mes:02d}-{numero:03d}"

    # Formato genérico: LYYYYMM-A/B/C
    letra = random.choice(['A', 'B', 'C', 'D', 'E'])
    return f"L{año}-{mes:02d}-{letra}"


# Estadísticas para debugging
def imprimir_estadisticas():
    """Imprime estadísticas de códigos de producto."""
    total_sectores = len(PREFIJOS_SKU)
    total_prefijos = sum(len(prefijos) for prefijos in PREFIJOS_SKU.values())

    print(f"🏷️  Códigos de Producto")
    print(f"   • Sectores con SKU: {total_sectores}")
    print(f"   • Total de prefijos SKU: {total_prefijos}")
    print(f"   • Prefijos EAN-13 Perú: {', '.join(PREFIJOS_EAN_PERU)}")

    print(f"\nPrefijos SKU por sector:")
    for sector, prefijos in PREFIJOS_SKU.items():
        print(f"   • {sector}: {', '.join(prefijos)}")


if __name__ == '__main__':
    # Pruebas
    print("\n" + "="*80)
    print("PRUEBA: Generación de Códigos de Producto")
    print("="*80 + "\n")

    imprimir_estadisticas()

    print("\n" + "-"*80)
    print("Ejemplos de SKU generados:")
    print("-"*80)

    sectores_prueba = ['farmacia', 'ferreteria', 'supermercado', 'electrodomesticos']

    for sector in sectores_prueba:
        print(f"\n{sector.upper()}:")
        for i in range(3):
            sku = generar_sku(sector)
            print(f"   {i+1}. {sku}")

    print("\n" + "-"*80)
    print("Ejemplos de EAN-13 generados (con validación):")
    print("-"*80)

    for i in range(5):
        ean = generar_ean13()
        valido = "✓" if validar_ean13(ean) else "✗"
        print(f"   {i+1}. {ean} {valido}")

    print("\n" + "-"*80)
    print("Ejemplos de lotes generados:")
    print("-"*80)

    for sector in ['farmacia', 'supermercado', 'panaderia']:
        lote = generar_lote(sector)
        print(f"   • {sector}: {lote}")

    print("\n" + "="*80)
    print("✅ Pruebas completadas")
    print("="*80 + "\n")
