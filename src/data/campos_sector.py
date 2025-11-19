#!/usr/bin/env python3
"""
Campos Específicos por Sector
==============================

Genera campos adicionales que aparecen solo en ciertos sectores:
- Ferretería: guía de remisión, orden de compra, detracción
- Restaurante: propina, delivery, mesa, mozo
- Spa/Gym: número de socio, terapeuta, entrenador
- Farmacia: receta médica

Uso:
    from src.data.campos_sector import generar_campos_sector

    campos = generar_campos_sector('restaurante', total_factura=150.00)
    # Resultado: {'propina': 15.00, 'cargo_delivery': 8.00, 'numero_mesa': '12', 'mozo': 'Carlos R.'}
"""

import random
from typing import Optional, Dict, Any
from datetime import datetime, timedelta


# ============================================================================
# FERRETERÍA
# ============================================================================

def generar_guia_remision(probabilidad: float = 0.60) -> Optional[str]:
    """
    Genera número de guía de remisión (60% de facturas de ferretería).

    Formato: GRR-XXXX-YYYYYYYY (GRR = Guía Remisión Remitente)

    Returns:
        Número de guía o None

    Ejemplo:
        >>> generar_guia_remision()
        'GRR-T001-00012345'
    """
    if random.random() > probabilidad:
        return None

    # Serie (4 dígitos con T al inicio)
    serie = f"T{random.randint(1, 999):03d}"

    # Número correlativo (8 dígitos)
    numero = random.randint(1, 99999999)

    return f"GRR-{serie}-{numero:08d}"


def generar_orden_compra(probabilidad: float = 0.50) -> Optional[str]:
    """
    Genera número de orden de compra (50% de facturas de ferretería).

    Formato: OC-YYYY-NNNNNN

    Returns:
        Número de orden de compra o None

    Ejemplo:
        >>> generar_orden_compra()
        'OC-2024-001234'
    """
    if random.random() > probabilidad:
        return None

    # Año
    año = random.randint(2023, 2025)

    # Número correlativo (6 dígitos)
    numero = random.randint(1, 999999)

    return f"OC-{año}-{numero:06d}"


def generar_detraccion(
    total_factura: float,
    moneda: str = 'PEN'
) -> Optional[Dict[str, Any]]:
    """
    Genera detracción SPOT (Sistema de Pago de Obligaciones Tributarias).

    La detracción aplica a:
    - Materiales de construcción (10%)
    - Servicios de construcción (4%)
    - Solo facturas >= S/ 700

    Args:
        total_factura: Total de la factura
        moneda: 'PEN' o 'USD'

    Returns:
        dict con 'porcentaje' y 'monto', o None si no aplica

    Ejemplo:
        >>> generar_detraccion(1000.00, 'PEN')
        {'porcentaje': 10.0, 'monto': 100.00, 'aplica': True}
    """
    # Detracción solo aplica en Soles >= 700
    if moneda != 'PEN' or total_factura < 700:
        return None

    # 70% de facturas de ferretería >= 700 soles tienen detracción
    if random.random() > 0.70:
        return None

    # Porcentajes de detracción según tipo de material
    # 10% = Materiales de construcción
    # 4% = Servicios de construcción
    porcentajes = [10.0, 4.0]
    pesos = [80, 20]  # 80% materiales, 20% servicios

    porcentaje = random.choices(porcentajes, weights=pesos, k=1)[0]
    monto = round(total_factura * (porcentaje / 100), 2)

    return {
        'porcentaje': porcentaje,
        'monto': monto,
        'aplica': True,
        'tipo': 'Materiales de construcción' if porcentaje == 10.0 else 'Servicios de construcción'
    }


def generar_campos_ferreteria(total_factura: float, moneda: str = 'PEN') -> Dict[str, Any]:
    """
    Genera todos los campos específicos de ferretería.

    Returns:
        dict con campos específicos
    """
    campos = {}

    # Guía de remisión
    guia = generar_guia_remision()
    if guia:
        campos['guia_remision'] = guia

    # Orden de compra
    orden = generar_orden_compra()
    if orden:
        campos['orden_compra'] = orden

    # Detracción
    detraccion = generar_detraccion(total_factura, moneda)
    if detraccion:
        campos['detraccion_porcentaje'] = detraccion['porcentaje']
        campos['detraccion_monto'] = detraccion['monto']

    return campos


# ============================================================================
# RESTAURANTE
# ============================================================================

NOMBRES_MOZOS = [
    'Carlos R.', 'María G.', 'José L.', 'Ana M.', 'Pedro S.',
    'Lucía F.', 'Miguel A.', 'Carmen T.', 'Jorge P.', 'Rosa V.',
    'Alberto C.', 'Patricia N.', 'Fernando D.', 'Isabel H.', 'Ricardo M.',
    'Sofía B.', 'Andrés Q.', 'Elena R.', 'Daniel W.', 'Claudia Z.',
]


def generar_propina(
    total_factura: float,
    probabilidad: float = 0.50
) -> Optional[float]:
    """
    Genera monto de propina (50% de facturas de restaurante).

    Típicamente 10% del total, pero puede variar entre 5-15%.

    Args:
        total_factura: Total de la factura SIN propina
        probabilidad: Probabilidad de que haya propina

    Returns:
        Monto de propina o None

    Ejemplo:
        >>> generar_propina(100.00)
        10.00  # 10%
    """
    if random.random() > probabilidad:
        return None

    # Porcentajes de propina típicos en Perú
    porcentajes = [5, 10, 15]
    pesos = [20, 70, 10]  # 70% da 10%, 20% da 5%, 10% da 15%

    porcentaje = random.choices(porcentajes, weights=pesos, k=1)[0]
    propina = round(total_factura * (porcentaje / 100), 2)

    return propina


def generar_cargo_delivery(
    total_factura: float,
    probabilidad: float = 0.30
) -> Optional[float]:
    """
    Genera cargo por delivery (30% de facturas de restaurante).

    Típicamente entre S/ 5.00 - S/ 15.00 según distancia.

    Args:
        total_factura: Total de la factura
        probabilidad: Probabilidad de que sea delivery

    Returns:
        Monto de cargo delivery o None

    Ejemplo:
        >>> generar_cargo_delivery(80.00)
        8.00
    """
    if random.random() > probabilidad:
        return None

    # Cargos típicos de delivery en Lima
    cargos = [5.00, 6.00, 7.00, 8.00, 10.00, 12.00, 15.00]
    pesos = [15, 20, 25, 20, 10, 7, 3]  # Más común S/ 7-8

    cargo = random.choices(cargos, weights=pesos, k=1)[0]

    return cargo


def generar_numero_mesa(probabilidad: float = 0.70) -> Optional[str]:
    """
    Genera número de mesa (70% de facturas de restaurante).

    Returns:
        Número de mesa o None

    Ejemplo:
        >>> generar_numero_mesa()
        '12'
    """
    if random.random() > probabilidad:
        return None

    # Restaurantes típicos tienen 15-50 mesas
    # Distribución: más facturas de mesas bajas (1-20)
    if random.random() < 0.70:
        # 70% mesas 1-20
        mesa = random.randint(1, 20)
    else:
        # 30% mesas 21-50
        mesa = random.randint(21, 50)

    return str(mesa)


def generar_mozo(probabilidad: float = 0.60) -> Optional[str]:
    """
    Genera nombre del mozo (60% de facturas de restaurante).

    Returns:
        Nombre del mozo o None

    Ejemplo:
        >>> generar_mozo()
        'Carlos R.'
    """
    if random.random() > probabilidad:
        return None

    return random.choice(NOMBRES_MOZOS)


def generar_campos_restaurante(total_factura: float) -> Dict[str, Any]:
    """
    Genera todos los campos específicos de restaurante.

    Args:
        total_factura: Total SIN propina ni delivery

    Returns:
        dict con campos específicos
    """
    campos = {}

    # Propina
    propina = generar_propina(total_factura)
    if propina:
        campos['propina'] = propina

    # Cargo delivery
    cargo_delivery = generar_cargo_delivery(total_factura)
    if cargo_delivery:
        campos['cargo_delivery'] = cargo_delivery

    # Número de mesa (solo si NO es delivery)
    if not cargo_delivery:
        numero_mesa = generar_numero_mesa()
        if numero_mesa:
            campos['numero_mesa'] = numero_mesa

        # Mozo (solo si hay mesa)
        if numero_mesa:
            mozo = generar_mozo()
            if mozo:
                campos['mozo'] = mozo

    return campos


# ============================================================================
# SPA / GYM
# ============================================================================

NOMBRES_TERAPEUTAS = [
    'Dra. Ana Rodríguez', 'Dr. Carlos Méndez', 'Dra. María Santos',
    'Lic. Patricia López', 'Lic. Jorge Vega', 'Dra. Lucía Romero',
    'Lic. Fernando Castro', 'Dra. Isabel Torres', 'Lic. Miguel Ángel Ruiz',
    'Dra. Carmen Flores', 'Lic. Ricardo Silva', 'Dra. Rosa Gutiérrez',
]

NOMBRES_ENTRENADORES = [
    'Prof. Carlos Pérez', 'Prof. María González', 'Lic. José Ramírez',
    'Prof. Ana Martínez', 'Lic. Pedro Sánchez', 'Prof. Lucía Fernández',
    'Lic. Miguel Torres', 'Prof. Carmen López', 'Lic. Jorge Díaz',
    'Prof. Patricia Castro', 'Lic. Fernando Ruiz', 'Prof. Isabel Vargas',
]


def generar_numero_socio(probabilidad: float = 0.80) -> Optional[str]:
    """
    Genera número de socio (80% de facturas de gym/spa).

    Formato: SOC-XXXXXX

    Returns:
        Número de socio o None

    Ejemplo:
        >>> generar_numero_socio()
        'SOC-012345'
    """
    if random.random() > probabilidad:
        return None

    # Número correlativo (6 dígitos)
    numero = random.randint(1, 999999)

    return f"SOC-{numero:06d}"


def generar_terapeuta(probabilidad: float = 0.70) -> Optional[str]:
    """
    Genera nombre del terapeuta (70% de facturas de spa).

    Returns:
        Nombre del terapeuta o None

    Ejemplo:
        >>> generar_terapeuta()
        'Dra. Ana Rodríguez'
    """
    if random.random() > probabilidad:
        return None

    return random.choice(NOMBRES_TERAPEUTAS)


def generar_entrenador(probabilidad: float = 0.60) -> Optional[str]:
    """
    Genera nombre del entrenador (60% de facturas de gym).

    Returns:
        Nombre del entrenador o None

    Ejemplo:
        >>> generar_entrenador()
        'Prof. Carlos Pérez'
    """
    if random.random() > probabilidad:
        return None

    return random.choice(NOMBRES_ENTRENADORES)


def generar_campos_spa() -> Dict[str, Any]:
    """
    Genera campos específicos de spa.

    Returns:
        dict con campos específicos
    """
    campos = {}

    # Número de socio
    numero_socio = generar_numero_socio()
    if numero_socio:
        campos['numero_socio'] = numero_socio

    # Terapeuta
    terapeuta = generar_terapeuta()
    if terapeuta:
        campos['terapeuta'] = terapeuta

    return campos


def generar_campos_gym() -> Dict[str, Any]:
    """
    Genera campos específicos de gym.

    Returns:
        dict con campos específicos
    """
    campos = {}

    # Número de socio
    numero_socio = generar_numero_socio()
    if numero_socio:
        campos['numero_socio'] = numero_socio

    # Entrenador
    entrenador = generar_entrenador()
    if entrenador:
        campos['entrenador'] = entrenador

    return campos


# ============================================================================
# FARMACIA
# ============================================================================

def generar_receta_medica(probabilidad: float = 0.40) -> Optional[str]:
    """
    Genera número de receta médica (40% de facturas de farmacia).

    Formato: RM-YYYY-NNNNNN

    Returns:
        Número de receta médica o None

    Ejemplo:
        >>> generar_receta_medica()
        'RM-2024-012345'
    """
    if random.random() > probabilidad:
        return None

    # Año
    año = random.randint(2023, 2025)

    # Número correlativo (6 dígitos)
    numero = random.randint(1, 999999)

    return f"RM-{año}-{numero:06d}"


def generar_campos_farmacia() -> Dict[str, Any]:
    """
    Genera campos específicos de farmacia.

    Returns:
        dict con campos específicos
    """
    campos = {}

    # Receta médica
    receta = generar_receta_medica()
    if receta:
        campos['receta_medica'] = receta

    return campos


# ============================================================================
# FUNCIÓN PRINCIPAL
# ============================================================================

def generar_campos_sector(
    sector: str,
    total_factura: float,
    moneda: str = 'PEN'
) -> Dict[str, Any]:
    """
    Genera campos específicos según el sector.

    Args:
        sector: Nombre del sector ('restaurante', 'ferreteria', 'farmacia', etc.)
        total_factura: Total de la factura (SIN propina ni delivery)
        moneda: 'PEN' o 'USD'

    Returns:
        dict con campos específicos del sector

    Ejemplos:
        >>> generar_campos_sector('restaurante', 150.00)
        {'propina': 15.00, 'numero_mesa': '12', 'mozo': 'Carlos R.'}

        >>> generar_campos_sector('ferreteria', 1000.00, 'PEN')
        {'guia_remision': 'GRR-T001-00012345', 'detraccion_porcentaje': 10.0, 'detraccion_monto': 100.00}

        >>> generar_campos_sector('farmacia', 80.00)
        {'receta_medica': 'RM-2024-012345'}

        >>> generar_campos_sector('gym', 200.00)
        {'numero_socio': 'SOC-012345', 'entrenador': 'Prof. Carlos Pérez'}
    """
    campos = {}

    if sector == 'ferreteria':
        campos = generar_campos_ferreteria(total_factura, moneda)

    elif sector == 'restaurante':
        campos = generar_campos_restaurante(total_factura)

    elif sector == 'spa':
        campos = generar_campos_spa()

    elif sector == 'gym':
        campos = generar_campos_gym()

    elif sector == 'farmacia':
        campos = generar_campos_farmacia()

    # Otros sectores no tienen campos específicos adicionales
    return campos


def generar_otros_cargos(sector: str, total_factura: float) -> Optional[float]:
    """
    Genera otros cargos adicionales según el sector.

    Args:
        sector: Nombre del sector
        total_factura: Total de la factura

    Returns:
        Monto de otros cargos o None

    Ejemplos:
        >>> generar_otros_cargos('electrodomesticos', 500.00)
        25.00  # Cargo por instalación

        >>> generar_otros_cargos('veterinaria', 150.00)
        30.00  # Cargo por visita a domicilio
    """
    # Probabilidad de otros cargos según sector
    probabilidades = {
        'electrodomesticos': 0.40,  # Instalación, garantía extendida
        'veterinaria': 0.30,         # Visita a domicilio
        'optica': 0.25,              # Ajuste de monturas
        'automotriz': 0.50,          # Mano de obra
        'libreria': 0.10,            # Empaque especial
        'floristeria': 0.35,         # Arreglo especial
    }

    prob = probabilidades.get(sector, 0.10)  # 10% por defecto

    if random.random() > prob:
        return None

    # Generar cargo según sector
    if sector == 'electrodomesticos':
        # Cargo por instalación (5-10% del total)
        porcentaje = random.uniform(0.05, 0.10)
        return round(total_factura * porcentaje, 2)

    elif sector == 'veterinaria':
        # Cargo fijo por visita
        cargos = [20.00, 25.00, 30.00, 35.00, 40.00]
        return random.choice(cargos)

    elif sector == 'optica':
        # Cargo por ajuste
        cargos = [10.00, 15.00, 20.00]
        return random.choice(cargos)

    elif sector == 'automotriz':
        # Mano de obra (10-30% del total)
        porcentaje = random.uniform(0.10, 0.30)
        return round(total_factura * porcentaje, 2)

    elif sector == 'libreria':
        # Empaque especial
        cargos = [5.00, 8.00, 10.00]
        return random.choice(cargos)

    elif sector == 'floristeria':
        # Arreglo especial
        cargos = [15.00, 20.00, 25.00, 30.00]
        return random.choice(cargos)

    else:
        # Genérico: 2-5% del total
        porcentaje = random.uniform(0.02, 0.05)
        return round(total_factura * porcentaje, 2)


# Estadísticas para debugging
def imprimir_estadisticas():
    """Imprime estadísticas de campos por sector."""
    print(f"🏪 Campos Específicos por Sector")

    print(f"\n🔨 FERRETERÍA:")
    print(f"   • guia_remision: 60% de facturas")
    print(f"   • orden_compra: 50% de facturas")
    print(f"   • detraccion: Solo facturas >= S/ 700 (10% o 4%)")

    print(f"\n🍽️  RESTAURANTE:")
    print(f"   • propina: 50% de facturas (5-15% del total)")
    print(f"   • cargo_delivery: 30% de facturas (S/ 5-15)")
    print(f"   • numero_mesa: 70% de facturas presenciales")
    print(f"   • mozo: 60% de facturas con mesa")

    print(f"\n💆 SPA:")
    print(f"   • numero_socio: 80% de facturas")
    print(f"   • terapeuta: 70% de facturas")

    print(f"\n🏋️  GYM:")
    print(f"   • numero_socio: 80% de facturas")
    print(f"   • entrenador: 60% de facturas")

    print(f"\n💊 FARMACIA:")
    print(f"   • receta_medica: 40% de facturas")

    print(f"\n💰 OTROS CARGOS:")
    print(f"   • Electrodomésticos: 40% (instalación)")
    print(f"   • Veterinaria: 30% (visita domicilio)")
    print(f"   • Óptica: 25% (ajuste)")
    print(f"   • Automotriz: 50% (mano de obra)")


if __name__ == '__main__':
    # Pruebas
    print("\n" + "="*80)
    print("PRUEBA: Generación de Campos Específicos por Sector")
    print("="*80 + "\n")

    imprimir_estadisticas()

    print("\n" + "-"*80)
    print("Ejemplos por sector:")
    print("-"*80)

    # Ferretería
    print("\n🔨 FERRETERÍA (Total: S/ 1,200.00):")
    for i in range(3):
        campos = generar_campos_sector('ferreteria', 1200.00, 'PEN')
        print(f"   {i+1}. {campos}")

    # Restaurante
    print("\n🍽️  RESTAURANTE (Total: S/ 150.00):")
    for i in range(3):
        campos = generar_campos_sector('restaurante', 150.00)
        print(f"   {i+1}. {campos}")

    # Spa
    print("\n💆 SPA (Total: S/ 200.00):")
    for i in range(3):
        campos = generar_campos_sector('spa', 200.00)
        print(f"   {i+1}. {campos}")

    # Gym
    print("\n🏋️  GYM (Total: S/ 180.00):")
    for i in range(3):
        campos = generar_campos_sector('gym', 180.00)
        print(f"   {i+1}. {campos}")

    # Farmacia
    print("\n💊 FARMACIA (Total: S/ 80.00):")
    for i in range(3):
        campos = generar_campos_sector('farmacia', 80.00)
        print(f"   {i+1}. {campos}")

    # Otros cargos
    print("\n" + "-"*80)
    print("Ejemplos de otros cargos:")
    print("-"*80)

    sectores_otros = ['electrodomesticos', 'veterinaria', 'automotriz']
    for sector in sectores_otros:
        print(f"\n{sector.upper()}:")
        for i in range(3):
            cargo = generar_otros_cargos(sector, 500.00)
            if cargo:
                print(f"   {i+1}. S/ {cargo:.2f}")
            else:
                print(f"   {i+1}. Sin cargo adicional")

    print("\n" + "="*80)
    print("✅ Pruebas completadas")
    print("="*80 + "\n")
