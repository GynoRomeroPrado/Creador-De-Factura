#!/usr/bin/env python3
"""
Nombres Comerciales por Sector
================================

Genera nombres comerciales realistas que difieren de la razón social.

Uso:
    from src.data.nombres_comerciales import generar_nombre_comercial

    nombre = generar_nombre_comercial('farmacia', 'QUIMIFAR S.A.C.')
    # Resultado: "Inkafarma"
"""

import random
from typing import Optional


# Nombres comerciales conocidos por sector
NOMBRES_COMERCIALES = {
    'farmacia': [
        'Inkafarma', 'Mifarma', 'Boticas Perú', 'Farmacia Universal',
        'Boticas Arcángel', 'Farmacia Deza', 'Boticas Fasa', 'Farmacia Felicidad',
    ],
    'restaurante': [
        'La Mar', 'Central', 'Maido', 'Astrid & Gastón', 'Isolina',
        'Panchita', 'El Mercado', 'La Rosa Náutica', 'Pescados Capitales',
        'El Señorío de Sulco', 'Tanta', 'La Lucha Sanguchería',
    ],
    'ferreteria': [
        'Maestro', 'Sodimac', 'Promart', 'Casa & Ideas', 'Construmart',
        'Fierro Seguro', 'Todo Construcción', 'La Casa del Constructor',
    ],
    'supermercado': [
        'Wong', 'Metro', 'Plaza Vea', 'Tottus', 'Vivanda',
        'Mass', 'Makro', 'Franco',
    ],
    'electrodomesticos': [
        'Hiraoka', 'Curacao', 'EFE', 'La Curacao', 'Carsa',
        'Elektra', 'Tiendas EFE', 'Crediscotia',
    ],
    'gym': [
        'Gold\'s Gym', 'BodyTech', 'SportLife', 'Iron Gym', 'FitnessOne',
        'Smart Fit', 'Pacific Fitness', 'Animal Gym',
    ],
    'spa': [
        'Zen Spa', 'Aqualina Spa', 'Montalvo Spa', 'Ocean Spa', 'Samay Spa',
        'Kalpana Spa', 'Mystique Spa', 'Armonia Spa',
    ],
    'veterinaria': [
        'Pet Center', 'Vet Center', 'Clínica Veterinaria San Francisco',
        'Animal House', 'Mi Mascota', 'Superpet', 'Huellitas',
    ],
    'educacion': [
        'Innova Schools', 'Trilce', 'Saco Oliveros', 'Pamer', 'Aduni',
        'César Vallejo', 'Cibertec', 'San Ignacio de Loyola',
    ],
    'odontologia': [
        'Multident', 'DentEstetica', 'Clínica Dental Roe', 'SmileDent',
        'OdontoSalud', 'ClinDent', 'Dent Laser',
    ],
    'automotriz': [
        'Divemotor', 'Derco', 'Motored', 'Euromotors', 'Inchcape',
        'Auto Center', 'Mitsui Auto', 'Nexus Automotriz',
    ],
    'libreria': [
        'Librerías Crisol', 'Ibero', 'Tai Loy', 'Bazar La Unión',
        'Librería Nacional', 'Libros Peruanos',
    ],
    'panaderia': [
        'Panadería San Antonio', 'San Roque', 'La Unión', 'El Trigal',
        'Pan de la Chola', 'Panificadora Bimbo', 'La Bondiet',
    ],
    'optica': [
        'Óptica GMO', 'Econoópticas', 'Opticentro', 'Ópticas Devlyn',
        'LensCrafters', 'Visión Total',
    ],
    'floristeria': [
        'Rosatel', 'Florerías Unidas', 'Bloom', 'Las Flores de María',
        'Flores Express', 'Jardín Secreto',
    ],
}


def generar_nombre_comercial(
    sector: str,
    razon_social: Optional[str] = None,
    probabilidad_usar: float = 0.70
) -> Optional[str]:
    """
    Genera un nombre comercial para un sector.

    Args:
        sector: Sector del negocio
        razon_social: Razón social (opcional, para extraer nombre)
        probabilidad_usar: Probabilidad de tener nombre comercial (70% por defecto)

    Returns:
        Nombre comercial o None si no aplica

    Ejemplos:
        >>> generar_nombre_comercial('farmacia', 'QUIMIFAR S.A.C.')
        'Inkafarma'

        >>> generar_nombre_comercial('restaurante')
        'La Mar'
    """
    # 70% de las empresas tienen nombre comercial diferente
    if random.random() > probabilidad_usar:
        return None

    # Obtener nombre comercial del sector
    if sector in NOMBRES_COMERCIALES:
        return random.choice(NOMBRES_COMERCIALES[sector])

    # Si no hay nombres predefinidos, extraer de razón social
    if razon_social:
        return _extraer_nombre_de_razon_social(razon_social)

    return None


def _extraer_nombre_de_razon_social(razon_social: str) -> str:
    """
    Extrae un nombre comercial simplificado de la razón social.

    Ejemplos:
        "SUPERMERCADOS PERUANOS S.A.C." -> "Supermercados Peruanos"
        "RESTAURANTE LA MAR E.I.R.L." -> "La Mar"
    """
    # Eliminar sufijos legales
    sufijos = ['S.A.C.', 'S.A.', 'S.R.L.', 'E.I.R.L.', 'SAC', 'SRL', 'EIRL']
    nombre = razon_social

    for sufijo in sufijos:
        nombre = nombre.replace(sufijo, '').strip()

    # Eliminar palabras genéricas del inicio
    palabras_genericas = ['EMPRESA', 'CORPORACION', 'GRUPO', 'COMPAÑIA', 'CIA']
    palabras = nombre.split()

    if palabras and palabras[0].upper() in palabras_genericas:
        palabras = palabras[1:]

    # Capitalizar correctamente
    nombre_limpio = ' '.join(palabras)

    # Si es muy largo, tomar primeras 2-3 palabras
    if len(palabras) > 3:
        nombre_limpio = ' '.join(palabras[:3])

    return nombre_limpio.title()


def generar_tipo_documento(numero_identificacion: str) -> str:
    """
    Determina el tipo de documento según el número de identificación.

    Perú:
        - RUC: 11 dígitos (20, 10, 15, 17)
        - DNI: 8 dígitos
        - CE: 9-12 dígitos (Carnet de Extranjería)

    Args:
        numero_identificacion: Número de documento

    Returns:
        "RUC", "DNI" o "CE"

    Ejemplos:
        >>> generar_tipo_documento("20123456789")
        "RUC"

        >>> generar_tipo_documento("12345678")
        "DNI"
    """
    if not numero_identificacion:
        return "DNI"  # Por defecto

    # Limpiar espacios y guiones
    num = numero_identificacion.replace(' ', '').replace('-', '')

    # RUC: 11 dígitos
    if len(num) == 11 and num.isdigit():
        return "RUC"

    # DNI: 8 dígitos
    if len(num) == 8 and num.isdigit():
        return "DNI"

    # CE: otros casos (9-12 dígitos)
    if 9 <= len(num) <= 12 and num.isdigit():
        return "CE"

    # Por defecto
    return "DNI"


# Estadísticas para debugging
def imprimir_estadisticas():
    """Imprime estadísticas de nombres comerciales."""
    total_sectores = len(NOMBRES_COMERCIALES)
    total_nombres = sum(len(nombres) for nombres in NOMBRES_COMERCIALES.values())

    print(f"📛 Nombres Comerciales por Sector")
    print(f"   • Sectores con nombres: {total_sectores}")
    print(f"   • Total de nombres: {total_nombres}")
    print(f"\nNombres por sector:")
    for sector, nombres in NOMBRES_COMERCIALES.items():
        print(f"   • {sector}: {len(nombres)} nombres")


if __name__ == '__main__':
    # Pruebas
    print("\n" + "="*80)
    print("PRUEBA: Generación de Nombres Comerciales")
    print("="*80 + "\n")

    imprimir_estadisticas()

    print("\n" + "-"*80)
    print("Ejemplos de nombres comerciales generados:")
    print("-"*80)

    sectores_prueba = ['farmacia', 'restaurante', 'ferreteria', 'supermercado', 'gym']

    for sector in sectores_prueba:
        print(f"\n{sector.upper()}:")
        for i in range(3):
            nombre = generar_nombre_comercial(sector)
            print(f"   {i+1}. {nombre}")

    print("\n" + "-"*80)
    print("Ejemplos de tipo de documento:")
    print("-"*80)

    ejemplos_doc = [
        ("20123456789", "RUC esperado"),
        ("12345678", "DNI esperado"),
        ("123456789", "CE esperado"),
    ]

    for num, esperado in ejemplos_doc:
        tipo = generar_tipo_documento(num)
        print(f"   {num} → {tipo} ({esperado})")

    print("\n" + "="*80)
    print("✅ Pruebas completadas")
    print("="*80 + "\n")
