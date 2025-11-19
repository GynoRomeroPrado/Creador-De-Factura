#!/usr/bin/env python3
"""
Datos Bancarios Peruanos
=========================

Genera datos bancarios realistas para facturas peruanas:
- Cuentas bancarias por banco (CCI, cuenta corriente, cuenta ahorro)
- Números de cuenta con formato válido por banco
- Soporte para PEN (Soles) y USD (Dólares)

Uso:
    from src.data.datos_bancarios import generar_cuenta_bancaria

    cuenta = generar_cuenta_bancaria('PEN', 'BCP')
    # Resultado: "BCP 193-1234567-0-89 (Soles)"
"""

import random
from typing import Optional, Tuple


# Bancos peruanos principales con sus códigos
BANCOS_PERU = {
    'BCP': {
        'nombre_completo': 'Banco de Crédito del Perú',
        'codigo': '002',
        'peso': 30,  # Market share aproximado
        'formato_cuenta_corriente': '193-XXXXXXX-0-XX',  # 13 dígitos
        'formato_cuenta_ahorro': '194-XXXXXXX-0-XX',
        'formato_cci': '00219300XXXXXXX0XX',  # 20 dígitos (002=código, 193=cuenta corriente)
    },
    'INTERBANK': {
        'nombre_completo': 'Interbank',
        'codigo': '003',
        'peso': 20,
        'formato_cuenta_corriente': '200-XXXXXXX-X-XX',
        'formato_cuenta_ahorro': '898-XXXXXXX-X-XX',
        'formato_cci': '00320000XXXXXXXXX',
    },
    'BBVA': {
        'nombre_completo': 'BBVA Continental',
        'codigo': '011',
        'peso': 18,
        'formato_cuenta_corriente': '0011-XXXX-XXXXXXXX-XX',
        'formato_cuenta_ahorro': '0011-XXXX-XXXXXXXX-XX',
        'formato_cci': '01101100XXXXXXXXXXXX',
    },
    'SCOTIABANK': {
        'nombre_completo': 'Scotiabank Perú',
        'codigo': '009',
        'peso': 15,
        'formato_cuenta_corriente': 'XXX-XXXXXXX',
        'formato_cuenta_ahorro': 'XXX-XXXXXXX',
        'formato_cci': '009XXX00XXXXXXX000XX',
    },
    'BANBIF': {
        'nombre_completo': 'BanBif',
        'codigo': '038',
        'peso': 5,
        'formato_cuenta_corriente': '700-XXXXXXX-X-XX',
        'formato_cuenta_ahorro': '800-XXXXXXX-X-XX',
        'formato_cci': '03870000XXXXXXXXX',
    },
    'PICHINCHA': {
        'nombre_completo': 'Banco Pichincha',
        'codigo': '028',
        'peso': 4,
        'formato_cuenta_corriente': '2XXX-XXXXXXX-X-XX',
        'formato_cuenta_ahorro': '3XXX-XXXXXXX-X-XX',
        'formato_cci': '028200XXXXXXXXXXXX',
    },
    'GNB': {
        'nombre_completo': 'GNB Perú',
        'codigo': '053',
        'peso': 3,
        'formato_cuenta_corriente': 'XXX-XXXXXXX-XXX',
        'formato_cuenta_ahorro': 'XXX-XXXXXXX-XXX',
        'formato_cci': '053XXX00XXXXXXXXXXX',
    },
    'BCRP': {
        'nombre_completo': 'Banco de la Nación',
        'codigo': '018',
        'peso': 5,
        'formato_cuenta_corriente': '00-XXX-XXXXXX',
        'formato_cuenta_ahorro': '04-XXX-XXXXXX',
        'formato_cci': '01800000XXXXXXXXXXX',
    },
}


# Tipos de cuenta
TIPOS_CUENTA = {
    'corriente': {
        'nombre': 'Cuenta Corriente',
        'abreviatura': 'Cta. Cte.',
        'peso': 60,  # 60% son cuentas corrientes en empresas
    },
    'ahorro': {
        'nombre': 'Cuenta de Ahorros',
        'abreviatura': 'Cta. Ahorros',
        'peso': 25,  # 25% cuentas de ahorro
    },
    'cci': {
        'nombre': 'CCI (Código de Cuenta Interbancario)',
        'abreviatura': 'CCI',
        'peso': 15,  # 15% usan CCI directamente
    },
}


def generar_cuenta_bancaria(
    moneda: str = 'PEN',
    banco: Optional[str] = None,
    tipo_cuenta: Optional[str] = None,
    incluir_nombre_banco: bool = True
) -> str:
    """
    Genera un número de cuenta bancaria realista.

    Args:
        moneda: 'PEN' (Soles) o 'USD' (Dólares)
        banco: Nombre corto del banco ('BCP', 'INTERBANK', etc.) o None para aleatorio
        tipo_cuenta: 'corriente', 'ahorro', 'cci', o None para aleatorio
        incluir_nombre_banco: Si True, incluye el nombre del banco en el resultado

    Returns:
        Número de cuenta bancaria formateado

    Ejemplos:
        >>> generar_cuenta_bancaria('PEN', 'BCP', 'corriente')
        'BCP 193-1234567-0-89 (Soles)'

        >>> generar_cuenta_bancaria('USD', 'INTERBANK', 'ahorro')
        'INTERBANK 898-7654321-2-45 (Dólares)'

        >>> generar_cuenta_bancaria('PEN', tipo_cuenta='cci')
        'CCI 00219301234567089 (Soles)'
    """
    # Seleccionar banco si no se especificó
    if banco is None:
        banco = _seleccionar_banco_aleatorio()

    # Validar que el banco exista
    if banco not in BANCOS_PERU:
        banco = 'BCP'  # Fallback al más común

    # Seleccionar tipo de cuenta si no se especificó
    if tipo_cuenta is None:
        tipo_cuenta = _seleccionar_tipo_cuenta_aleatorio()

    # Validar tipo de cuenta
    if tipo_cuenta not in TIPOS_CUENTA:
        tipo_cuenta = 'corriente'  # Fallback

    # Generar número de cuenta según el formato del banco
    info_banco = BANCOS_PERU[banco]

    if tipo_cuenta == 'corriente':
        formato = info_banco['formato_cuenta_corriente']
    elif tipo_cuenta == 'ahorro':
        formato = info_banco['formato_cuenta_ahorro']
    else:  # cci
        formato = info_banco['formato_cci']

    # Reemplazar X por dígitos aleatorios
    numero_cuenta = _generar_numero_desde_formato(formato)

    # Formatear resultado
    nombre_moneda = 'Soles' if moneda == 'PEN' else 'Dólares'

    if tipo_cuenta == 'cci':
        # Para CCI, mostrar "CCI" en lugar del nombre del banco
        if incluir_nombre_banco:
            return f"CCI {numero_cuenta} ({nombre_moneda})"
        else:
            return numero_cuenta
    else:
        # Para cuentas normales
        if incluir_nombre_banco:
            return f"{banco} {numero_cuenta} ({nombre_moneda})"
        else:
            return numero_cuenta


def generar_cuenta_bancaria_completa(
    moneda: str = 'PEN',
    banco: Optional[str] = None
) -> dict:
    """
    Genera datos bancarios completos para una factura.

    Returns:
        dict con 'banco', 'numero_cuenta', 'tipo_cuenta', 'moneda', 'texto_completo'

    Ejemplo:
        >>> datos = generar_cuenta_bancaria_completa('PEN', 'BCP')
        >>> print(datos)
        {
            'banco': 'BCP',
            'banco_nombre_completo': 'Banco de Crédito del Perú',
            'numero_cuenta': '193-1234567-0-89',
            'tipo_cuenta': 'corriente',
            'tipo_cuenta_nombre': 'Cuenta Corriente',
            'moneda': 'PEN',
            'moneda_nombre': 'Soles',
            'texto_completo': 'BCP 193-1234567-0-89 (Soles)',
            'cci': '00219301234567089'  # Opcional, si tipo_cuenta='cci'
        }
    """
    # Seleccionar banco si no se especificó
    if banco is None:
        banco = _seleccionar_banco_aleatorio()

    # Validar banco
    if banco not in BANCOS_PERU:
        banco = 'BCP'

    # Seleccionar tipo de cuenta
    tipo_cuenta = _seleccionar_tipo_cuenta_aleatorio()

    # Generar número de cuenta
    info_banco = BANCOS_PERU[banco]

    if tipo_cuenta == 'corriente':
        formato = info_banco['formato_cuenta_corriente']
    elif tipo_cuenta == 'ahorro':
        formato = info_banco['formato_cuenta_ahorro']
    else:  # cci
        formato = info_banco['formato_cci']

    numero_cuenta = _generar_numero_desde_formato(formato)

    # Generar CCI adicional si no es ya CCI
    cci = None
    if tipo_cuenta != 'cci':
        formato_cci = info_banco['formato_cci']
        cci = _generar_numero_desde_formato(formato_cci)
    else:
        cci = numero_cuenta

    # Formatear resultado
    nombre_moneda = 'Soles' if moneda == 'PEN' else 'Dólares'
    texto_completo = generar_cuenta_bancaria(moneda, banco, tipo_cuenta, incluir_nombre_banco=True)

    resultado = {
        'banco': banco,
        'banco_nombre_completo': info_banco['nombre_completo'],
        'numero_cuenta': numero_cuenta,
        'tipo_cuenta': tipo_cuenta,
        'tipo_cuenta_nombre': TIPOS_CUENTA[tipo_cuenta]['nombre'],
        'moneda': moneda,
        'moneda_nombre': nombre_moneda,
        'texto_completo': texto_completo,
    }

    # Agregar CCI si existe
    if cci:
        resultado['cci'] = cci

    return resultado


def _seleccionar_banco_aleatorio() -> str:
    """
    Selecciona un banco aleatorio según su peso (market share).

    Returns:
        Código corto del banco (ej: 'BCP', 'INTERBANK')
    """
    bancos = list(BANCOS_PERU.keys())
    pesos = [BANCOS_PERU[b]['peso'] for b in bancos]

    return random.choices(bancos, weights=pesos, k=1)[0]


def _seleccionar_tipo_cuenta_aleatorio() -> str:
    """
    Selecciona un tipo de cuenta aleatorio según su peso.

    Returns:
        'corriente', 'ahorro', o 'cci'
    """
    tipos = list(TIPOS_CUENTA.keys())
    pesos = [TIPOS_CUENTA[t]['peso'] for t in tipos]

    return random.choices(tipos, weights=pesos, k=1)[0]


def _generar_numero_desde_formato(formato: str) -> str:
    """
    Genera un número de cuenta a partir de un formato con X.

    Args:
        formato: String con X que serán reemplazadas por dígitos
                Ejemplo: "193-XXXXXXX-0-XX"

    Returns:
        Número de cuenta generado
        Ejemplo: "193-1234567-0-89"
    """
    resultado = ""

    for char in formato:
        if char == 'X':
            resultado += str(random.randint(0, 9))
        else:
            resultado += char

    return resultado


def generar_condiciones_pago(dias_credito: Optional[int] = None) -> str:
    """
    Genera condiciones de pago realistas.

    Args:
        dias_credito: Días de crédito (None para aleatorio)

    Returns:
        Texto de condiciones de pago

    Ejemplos:
        >>> generar_condiciones_pago(30)
        "Crédito a 30 días"

        >>> generar_condiciones_pago(0)
        "Contado"
    """
    if dias_credito is None:
        # Distribución realista de condiciones de pago
        opciones = [0, 7, 15, 30, 45, 60, 90]
        pesos = [40, 5, 10, 25, 10, 7, 3]  # 40% contado, 25% a 30 días
        dias_credito = random.choices(opciones, weights=pesos, k=1)[0]

    if dias_credito == 0:
        return "Contado"
    elif dias_credito == 7:
        return "Crédito a 7 días"
    elif dias_credito == 15:
        return "Crédito a 15 días"
    elif dias_credito == 30:
        return "Crédito a 30 días"
    elif dias_credito == 45:
        return "Crédito a 45 días"
    elif dias_credito == 60:
        return "Crédito a 60 días"
    elif dias_credito == 90:
        return "Crédito a 90 días"
    else:
        return f"Crédito a {dias_credito} días"


def generar_forma_pago_detalle(moneda: str = 'PEN') -> Tuple[str, str]:
    """
    Genera forma de pago detallada.

    Args:
        moneda: 'PEN' o 'USD'

    Returns:
        Tupla (forma_pago, forma_pago_detalle)

    Ejemplos:
        >>> generar_forma_pago_detalle('PEN')
        ("Transferencia bancaria", "Transferencia BCP - Op. 123456789")

        >>> generar_forma_pago_detalle('USD')
        ("Efectivo", "Efectivo - Dólares")
    """
    # Distribución de formas de pago
    formas_pago = [
        ('Transferencia bancaria', 50),
        ('Efectivo', 25),
        ('Tarjeta de crédito', 15),
        ('Tarjeta de débito', 7),
        ('Cheque', 3),
    ]

    formas, pesos = zip(*formas_pago)
    forma_pago = random.choices(formas, weights=pesos, k=1)[0]

    # Generar detalle según forma de pago
    if forma_pago == 'Transferencia bancaria':
        banco = _seleccionar_banco_aleatorio()
        operacion = random.randint(100000000, 999999999)
        detalle = f"Transferencia {banco} - Op. {operacion}"

    elif forma_pago == 'Efectivo':
        moneda_nombre = 'Soles' if moneda == 'PEN' else 'Dólares'
        detalle = f"Efectivo - {moneda_nombre}"

    elif forma_pago == 'Tarjeta de crédito':
        tipos_tarjeta = ['VISA', 'Mastercard', 'American Express', 'Diners']
        tipo = random.choice(tipos_tarjeta)
        ultimos_digitos = random.randint(1000, 9999)
        detalle = f"{tipo} **** {ultimos_digitos}"

    elif forma_pago == 'Tarjeta de débito':
        tipos_tarjeta = ['VISA Débito', 'Mastercard Débito']
        tipo = random.choice(tipos_tarjeta)
        ultimos_digitos = random.randint(1000, 9999)
        detalle = f"{tipo} **** {ultimos_digitos}"

    else:  # Cheque
        banco = _seleccionar_banco_aleatorio()
        numero_cheque = random.randint(10000000, 99999999)
        detalle = f"Cheque {banco} N° {numero_cheque}"

    return (forma_pago, detalle)


# Estadísticas para debugging
def imprimir_estadisticas():
    """Imprime estadísticas de datos bancarios."""
    total_bancos = len(BANCOS_PERU)
    total_market_share = sum(b['peso'] for b in BANCOS_PERU.values())

    print(f"🏦 Datos Bancarios Peruanos")
    print(f"   • Total de bancos: {total_bancos}")
    print(f"   • Market share total: {total_market_share}%")

    print(f"\nBancos por market share:")
    bancos_ordenados = sorted(
        BANCOS_PERU.items(),
        key=lambda x: x[1]['peso'],
        reverse=True
    )

    for codigo, info in bancos_ordenados:
        print(f"   • {codigo} ({info['nombre_completo']}): {info['peso']}%")

    print(f"\nTipos de cuenta:")
    for tipo, info in TIPOS_CUENTA.items():
        print(f"   • {info['nombre']}: {info['peso']}%")


if __name__ == '__main__':
    # Pruebas
    print("\n" + "="*80)
    print("PRUEBA: Generación de Datos Bancarios")
    print("="*80 + "\n")

    imprimir_estadisticas()

    print("\n" + "-"*80)
    print("Ejemplos de cuentas bancarias generadas:")
    print("-"*80)

    # Generar cuentas de diferentes bancos
    print("\nCuentas por banco (Soles):")
    for banco in ['BCP', 'INTERBANK', 'BBVA', 'SCOTIABANK']:
        cuenta = generar_cuenta_bancaria('PEN', banco, 'corriente')
        print(f"   • {cuenta}")

    print("\nCuentas de ahorro (Dólares):")
    for i in range(3):
        cuenta = generar_cuenta_bancaria('USD', tipo_cuenta='ahorro')
        print(f"   {i+1}. {cuenta}")

    print("\nCódigos CCI:")
    for i in range(3):
        cuenta = generar_cuenta_bancaria('PEN', tipo_cuenta='cci')
        print(f"   {i+1}. {cuenta}")

    print("\n" + "-"*80)
    print("Ejemplos de datos bancarios completos:")
    print("-"*80)

    for i in range(3):
        datos = generar_cuenta_bancaria_completa('PEN')
        print(f"\n{i+1}. {datos['banco_nombre_completo']}")
        print(f"   • Tipo: {datos['tipo_cuenta_nombre']}")
        print(f"   • Número: {datos['numero_cuenta']}")
        print(f"   • Moneda: {datos['moneda_nombre']}")
        if 'cci' in datos and datos['cci'] != datos['numero_cuenta']:
            print(f"   • CCI: {datos['cci']}")
        print(f"   • Completo: {datos['texto_completo']}")

    print("\n" + "-"*80)
    print("Condiciones de pago:")
    print("-"*80)

    for dias in [0, 7, 15, 30, 45, 60, 90]:
        condicion = generar_condiciones_pago(dias)
        print(f"   • {condicion}")

    print("\n" + "-"*80)
    print("Formas de pago detalladas:")
    print("-"*80)

    for i in range(8):
        forma, detalle = generar_forma_pago_detalle('PEN')
        print(f"   {i+1}. {forma}: {detalle}")

    print("\n" + "="*80)
    print("✅ Pruebas completadas")
    print("="*80 + "\n")
