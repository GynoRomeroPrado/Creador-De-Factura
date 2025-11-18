#!/usr/bin/env python3
"""
Patrones Temporales y Estacionalidad
====================================

Implementa patrones realistas de comportamiento temporal para facturas:
- Productos estacionales por mes
- Horarios pico por tipo de negocio
- Días de mayor/menor venta
- Variaciones de ticket según temporada

Uso:
    from src.data.patrones_temporales import generar_fecha_hora_realista

    fecha, hora = generar_fecha_hora_realista('restaurante')
    # Resultado: ('2024-03-15', '13:45')  # Viernes, hora pico almuerzo
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple


# Productos estacionales por mes
PRODUCTOS_ESTACIONALES = {
    1: {  # Enero
        'nombre': 'Verano / Año Nuevo',
        'productos': [
            'BLOQUEADOR SOLAR',
            'SOMBRERO',
            'LENTES DE SOL',
            'SANDALIAS',
            'TRAJE DE BAÑO',
            'COOLER',
            'HIELO',
            'BEBIDAS FRIAS',
        ],
        'factor_precio': 1.10,  # 10% más caro
    },
    2: {  # Febrero
        'nombre': 'Verano / San Valentín',
        'productos': [
            'ROSAS',
            'CHOCOLATES',
            'PELUCHES',
            'TARJETAS',
            'VINO',
            'BLOQUEADOR SOLAR',
            'BEBIDAS FRIAS',
        ],
        'factor_precio': 1.15,  # 15% más caro (San Valentín)
    },
    3: {  # Marzo
        'nombre': 'Inicio de Clases',
        'productos': [
            'CUADERNOS',
            'LAPICEROS',
            'MOCHILAS',
            'UNIFORMES',
            'LONCHERAS',
            'LIBROS',
            'CALCULADORA',
            'FORROS',
        ],
        'factor_precio': 1.20,  # 20% más caro (útiles escolares)
    },
    4: {  # Abril
        'nombre': 'Otoño / Semana Santa',
        'productos': [
            'PESCADO',
            'MARISCOS',
            'BACALAO',
            'HABAS',
            'FANESCA',
            'CRUCES DE PAN',
        ],
        'factor_precio': 1.12,
    },
    5: {  # Mayo
        'nombre': 'Día de la Madre',
        'productos': [
            'FLORES',
            'PERFUMES',
            'JOYAS',
            'CARTERAS',
            'ROPA',
            'ELECTRODOMESTICOS',
            'VAJILLA',
        ],
        'factor_precio': 1.18,  # 18% más caro
    },
    6: {  # Junio
        'nombre': 'Invierno / Día del Padre',
        'productos': [
            'ROPA ABRIGADA',
            'HERRAMIENTAS',
            'TECNOLOGIA',
            'LICORES',
            'PARRILLAS',
            'CALEFACCIÓN',
            'FRAZADAS',
        ],
        'factor_precio': 1.15,
    },
    7: {  # Julio
        'nombre': 'Fiestas Patrias',
        'productos': [
            'BANDERAS',
            'ESCARAPELAS',
            'PARRILLAS',
            'CARBÓN',
            'CERVEZA',
            'ANTICUCHOS',
            'CHICHA',
        ],
        'factor_precio': 1.25,  # 25% más caro (Fiestas Patrias)
    },
    8: {  # Agosto
        'nombre': 'Invierno',
        'productos': [
            'FRAZADAS',
            'ROPA ABRIGADA',
            'CALEFACCIÓN',
            'CHOCOLATE CALIENTE',
            'TE',
            'VITAMINA C',
        ],
        'factor_precio': 1.08,
    },
    9: {  # Septiembre
        'nombre': 'Primavera',
        'productos': [
            'FLORES',
            'PLANTAS',
            'ROPA PRIMAVERA',
            'ANTIHISTAMÍNICOS',
            'JARDINERIA',
        ],
        'factor_precio': 1.05,
    },
    10: {  # Octubre
        'nombre': 'Señor de los Milagros / Halloween',
        'productos': [
            'VELAS MORADAS',
            'INCIENSO',
            'HÁBITO MORADO',
            'TURRON',
            'DISFRACES',
            'DULCES',
            'DECORACIÓN HALLOWEEN',
        ],
        'factor_precio': 1.10,
    },
    11: {  # Noviembre
        'nombre': 'Black Friday / Cyber',
        'productos': [
            'TECNOLOGIA',
            'ELECTRODOMESTICOS',
            'ROPA',
            'JUGUETES',
        ],
        'factor_precio': 0.75,  # 25% descuento (Black Friday)
    },
    12: {  # Diciembre
        'nombre': 'Navidad / Año Nuevo',
        'productos': [
            'PANETÓN',
            'CHOCOLATE CALIENTE',
            'ÁRBOL DE NAVIDAD',
            'LUCES NAVIDEÑAS',
            'JUGUETES',
            'REGALOS',
            'PAVO',
            'CHAMPAGNE',
            'FUEGOS ARTIFICIALES',
        ],
        'factor_precio': 1.30,  # 30% más caro (Navidad)
    },
}


# Horarios pico por tipo de negocio
HORARIOS_PICO = {
    'restaurante': {
        'lunes_viernes': [
            (7, 9, 0.15),   # Desayuno 15%
            (12, 15, 0.40),  # Almuerzo 40% (PICO)
            (19, 22, 0.30),  # Cena 30%
            (15, 19, 0.10),  # Entre comidas 10%
            (22, 23, 0.05),  # Cierre 5%
        ],
        'sabado_domingo': [
            (8, 11, 0.20),   # Desayuno/Brunch 20%
            (12, 16, 0.40),  # Almuerzo 40%
            (19, 23, 0.35),  # Cena 35%
            (16, 19, 0.05),  # Entre comidas 5%
        ],
    },
    'farmacia': {
        'lunes_viernes': [
            (7, 9, 0.15),    # Mañana temprano
            (12, 14, 0.20),  # Almuerzo
            (18, 21, 0.35),  # Salida del trabajo (PICO)
            (9, 12, 0.15),   # Media mañana
            (14, 18, 0.10),  # Tarde
            (21, 23, 0.05),  # Noche
        ],
        'sabado_domingo': [
            (9, 13, 0.40),   # Mañana (PICO)
            (13, 18, 0.35),  # Tarde
            (18, 21, 0.20),  # Noche
            (21, 22, 0.05),  # Cierre
        ],
    },
    'ferreteria': {
        'lunes_viernes': [
            (7, 9, 0.20),    # Inicio obra
            (9, 13, 0.40),   # Mañana (PICO)
            (13, 14, 0.05),  # Almuerzo
            (14, 18, 0.30),  # Tarde
            (18, 19, 0.05),  # Cierre
        ],
        'sabado': [
            (8, 13, 0.50),   # Mañana (PICO - proyectos personales)
            (13, 18, 0.40),  # Tarde
            (18, 19, 0.10),  # Cierre
        ],
        'domingo': [],  # Cerrado
    },
    'supermercado': {
        'lunes_viernes': [
            (7, 9, 0.10),    # Temprano
            (12, 14, 0.15),  # Almuerzo
            (17, 21, 0.50),  # Salida del trabajo (PICO)
            (9, 12, 0.15),   # Media mañana
            (14, 17, 0.05),  # Tarde baja
            (21, 23, 0.05),  # Noche
        ],
        'sabado_domingo': [
            (8, 14, 0.50),   # Mañana (PICO - compras semanales)
            (14, 20, 0.40),  # Tarde
            (20, 22, 0.10),  # Noche
        ],
    },
    'spa': {
        'lunes_viernes': [
            (10, 14, 0.25),  # Mañana
            (14, 18, 0.35),  # Tarde (PICO)
            (18, 21, 0.30),  # Noche
            (9, 10, 0.10),   # Apertura
        ],
        'sabado_domingo': [
            (9, 13, 0.40),   # Mañana (PICO)
            (13, 18, 0.45),  # Tarde
            (18, 20, 0.15),  # Cierre
        ],
    },
    'gym': {
        'lunes_viernes': [
            (6, 9, 0.35),    # Mañana antes del trabajo (PICO)
            (12, 14, 0.10),  # Almuerzo
            (18, 22, 0.45),  # Salida del trabajo (PICO)
            (9, 12, 0.05),   # Media mañana
            (14, 18, 0.05),  # Tarde baja
        ],
        'sabado_domingo': [
            (8, 12, 0.50),   # Mañana (PICO)
            (12, 18, 0.35),  # Tarde
            (18, 20, 0.15),  # Cierre
        ],
    },
    'educacion': {
        'lunes_viernes': [
            (8, 10, 0.30),   # Entrada
            (10, 13, 0.30),  # Mañana
            (14, 17, 0.30),  # Tarde
            (17, 18, 0.10),  # Salida
        ],
        'sabado': [
            (8, 13, 0.60),   # Mañana
            (13, 16, 0.40),  # Tarde
        ],
        'domingo': [],  # Cerrado
    },
    'generico': {
        'lunes_viernes': [
            (9, 13, 0.35),   # Mañana
            (13, 14, 0.10),  # Almuerzo
            (14, 18, 0.40),  # Tarde (PICO)
            (18, 19, 0.15),  # Cierre
        ],
        'sabado': [
            (9, 14, 0.60),   # Mañana (PICO)
            (14, 18, 0.40),  # Tarde
        ],
        'domingo': [],  # Cerrado
    },
}


# Distribución de ventas por día de la semana
DISTRIBUCION_DIAS = {
    'restaurante': {
        'lunes': 0.10,
        'martes': 0.10,
        'miercoles': 0.12,
        'jueves': 0.15,
        'viernes': 0.23,  # PICO
        'sabado': 0.20,
        'domingo': 0.10,
    },
    'farmacia': {
        'lunes': 0.16,
        'martes': 0.15,
        'miercoles': 0.15,
        'jueves': 0.14,
        'viernes': 0.14,
        'sabado': 0.18,  # PICO
        'domingo': 0.08,
    },
    'ferreteria': {
        'lunes': 0.18,
        'martes': 0.18,
        'miercoles': 0.17,
        'jueves': 0.16,
        'viernes': 0.16,
        'sabado': 0.15,  # Proyectos personales
        'domingo': 0.00,  # Cerrado
    },
    'supermercado': {
        'lunes': 0.12,
        'martes': 0.12,
        'miercoles': 0.14,
        'jueves': 0.15,
        'viernes': 0.18,
        'sabado': 0.20,  # PICO (compra semanal)
        'domingo': 0.09,
    },
    'generico': {
        'lunes': 0.14,
        'martes': 0.14,
        'miercoles': 0.15,
        'juernes': 0.16,
        'viernes': 0.18,
        'sabado': 0.16,
        'domingo': 0.07,
    },
}


def generar_fecha_hora_realista(
    sector: str = 'generico',
    fecha_inicio: Optional[datetime] = None,
    fecha_fin: Optional[datetime] = None
) -> Tuple[str, str]:
    """
    Genera una fecha y hora realista según el sector del negocio.

    Args:
        sector: Tipo de negocio (restaurante, farmacia, etc.)
        fecha_inicio: Fecha mínima (default: hace 1 año)
        fecha_fin: Fecha máxima (default: hoy)

    Returns:
        Tuple[str, str]: (fecha en formato 'YYYY-MM-DD', hora en formato 'HH:MM')

    Ejemplos:
        >>> generar_fecha_hora_realista('restaurante')
        ('2024-03-15', '13:45')  # Viernes, hora pico de almuerzo

        >>> generar_fecha_hora_realista('farmacia')
        ('2024-06-22', '19:30')  # Sábado, tarde
    """
    # Rango de fechas
    if fecha_fin is None:
        fecha_fin = datetime.now()
    if fecha_inicio is None:
        fecha_inicio = fecha_fin - timedelta(days=365)

    # Mapeo de sectores a categorías de horarios
    mapeo_horarios = {
        'restaurante': 'restaurante',
        'farmacia': 'farmacia',
        'ferreteria': 'ferreteria',
        'supermercado': 'supermercado',
        'spa': 'spa',
        'gym': 'gym',
        'educacion': 'educacion',
        'electrodomesticos': 'generico',
        'veterinaria': 'generico',
        'odontologia': 'generico',
        'automotriz': 'ferreteria',  # Similar horario
        'libreria': 'generico',
        'panaderia': 'supermercado',  # Similar horario
        'optica': 'generico',
        'floristeria': 'generico',
    }

    categoria = mapeo_horarios.get(sector, 'generico')

    # Distribución de días para este sector
    dist_dias = DISTRIBUCION_DIAS.get(categoria, DISTRIBUCION_DIAS['generico'])

    # Generar fecha ponderada por día de semana
    intentos = 0
    while intentos < 100:  # Máximo 100 intentos
        # Fecha aleatoria en el rango
        dias_diff = (fecha_fin - fecha_inicio).days
        fecha_random = fecha_inicio + timedelta(days=random.randint(0, dias_diff))

        # Día de la semana
        dia_semana = fecha_random.strftime('%A').lower()
        mapeo_dias = {
            'monday': 'lunes',
            'tuesday': 'martes',
            'wednesday': 'miercoles',
            'thursday': 'jueves',
            'friday': 'viernes',
            'saturday': 'sabado',
            'sunday': 'domingo',
        }
        dia_espanol = mapeo_dias[dia_semana]

        # Probabilidad de este día
        prob_dia = dist_dias.get(dia_espanol, 0.14)

        # Aceptar o rechazar según probabilidad
        if random.random() < prob_dia * 7:  # Multiplicar por 7 para normalizar
            break

        intentos += 1
    else:
        # Si no se encontró en 100 intentos, usar fecha aleatoria
        dias_diff = (fecha_fin - fecha_inicio).days
        fecha_random = fecha_inicio + timedelta(days=random.randint(0, dias_diff))
        dia_semana = fecha_random.strftime('%A').lower()
        dia_espanol = mapeo_dias[dia_semana]

    # Generar hora según el día y sector
    horarios = HORARIOS_PICO.get(categoria, HORARIOS_PICO['generico'])

    # Seleccionar horarios según día
    if dia_espanol in ['lunes', 'martes', 'miercoles', 'jueves', 'viernes']:
        if 'lunes_viernes' in horarios:
            franjas = horarios['lunes_viernes']
        else:
            franjas = horarios.get('generico', [(9, 18, 1.0)])
    elif dia_espanol == 'sabado':
        if 'sabado' in horarios:
            franjas = horarios['sabado']
        elif 'sabado_domingo' in horarios:
            franjas = horarios['sabado_domingo']
        else:
            franjas = horarios.get('lunes_viernes', [(9, 18, 1.0)])
    else:  # domingo
        if 'domingo' in horarios:
            franjas = horarios['domingo']
        elif 'sabado_domingo' in horarios:
            franjas = horarios['sabado_domingo']
        else:
            franjas = []

    # Si no hay horarios (ej: ferretería domingo), usar fecha diferente
    if not franjas:
        # Intentar un día diferente
        fecha_random = fecha_inicio + timedelta(days=random.randint(0, dias_diff))
        dia_semana = fecha_random.strftime('%A').lower()
        dia_espanol = mapeo_dias[dia_semana]
        franjas = horarios.get('lunes_viernes', [(9, 18, 1.0)])

    # Seleccionar franja horaria ponderada
    horas = [f[0] for f in franjas]
    pesos = [f[2] for f in franjas]
    franja_seleccionada = random.choices(franjas, weights=pesos, k=1)[0]

    hora_inicio, hora_fin, _ = franja_seleccionada

    # Generar hora específica dentro de la franja
    minutos_inicio = hora_inicio * 60
    minutos_fin = hora_fin * 60
    minutos_random = random.randint(minutos_inicio, minutos_fin - 1)

    hora = minutos_random // 60
    minuto = minutos_random % 60

    # Redondear minutos a múltiplos de 5 (más realista)
    minuto = (minuto // 5) * 5

    fecha_str = fecha_random.strftime('%Y-%m-%d')
    hora_str = f"{hora:02d}:{minuto:02d}"

    return fecha_str, hora_str


def obtener_productos_estacionales(mes: Optional[int] = None) -> List[str]:
    """
    Obtiene lista de productos estacionales para un mes.

    Args:
        mes: Mes (1-12). Si None, usa mes actual.

    Returns:
        List[str]: Lista de productos estacionales
    """
    if mes is None:
        mes = datetime.now().month

    return PRODUCTOS_ESTACIONALES.get(mes, {}).get('productos', [])


def obtener_factor_precio_estacional(mes: Optional[int] = None) -> float:
    """
    Obtiene factor de precio según temporada.

    Args:
        mes: Mes (1-12). Si None, usa mes actual.

    Returns:
        float: Factor multiplicador (ej: 1.20 = 20% más caro)
    """
    if mes is None:
        mes = datetime.now().month

    return PRODUCTOS_ESTACIONALES.get(mes, {}).get('factor_precio', 1.0)


def es_temporada_alta(sector: str, mes: Optional[int] = None) -> bool:
    """
    Determina si es temporada alta para un sector.

    Args:
        sector: Tipo de negocio
        mes: Mes (1-12). Si None, usa mes actual.

    Returns:
        bool: True si es temporada alta
    """
    if mes is None:
        mes = datetime.now().month

    # Temporadas altas por sector
    temporadas_altas = {
        'restaurante': [7, 12],  # Fiestas Patrias, Navidad
        'farmacia': [1, 2, 3, 6, 7, 8],  # Verano e invierno (gripes)
        'ferreteria': [1, 2, 3, 6, 7],  # Verano (construcción)
        'supermercado': [12, 3, 7],  # Navidad, Inicio de clases, Fiestas Patrias
        'electrodomesticos': [5, 6, 11, 12],  # Día Madre/Padre, Black Friday, Navidad
        'floristeria': [2, 5, 10],  # San Valentín, Día Madre, Señor de los Milagros
        'jugueteria': [7, 12],  # Fiestas Patrias, Navidad
        'libreria': [3, 4],  # Inicio de clases
    }

    meses_altos = temporadas_altas.get(sector, [])
    return mes in meses_altos


def generar_ticket_promedio_estacional(
    ticket_base: float,
    sector: str,
    mes: Optional[int] = None
) -> float:
    """
    Ajusta ticket promedio según estacionalidad.

    Args:
        ticket_base: Ticket promedio base
        sector: Tipo de negocio
        mes: Mes (1-12). Si None, usa mes actual.

    Returns:
        float: Ticket promedio ajustado
    """
    if mes is None:
        mes = datetime.now().month

    # Factor estacional general
    factor_general = obtener_factor_precio_estacional(mes)

    # Factor específico del sector
    if es_temporada_alta(sector, mes):
        factor_sector = 1.15  # 15% más en temporada alta
    else:
        factor_sector = 0.95  # 5% menos en temporada baja

    # Black Friday (Noviembre) - descuentos
    if mes == 11 and sector in ['electrodomesticos', 'tecnologia', 'ropa']:
        factor_sector = 0.80  # 20% descuento

    return ticket_base * factor_general * factor_sector


def obtener_nombre_temporada(mes: Optional[int] = None) -> str:
    """
    Obtiene el nombre de la temporada/evento del mes.

    Args:
        mes: Mes (1-12). Si None, usa mes actual.

    Returns:
        str: Nombre de la temporada
    """
    if mes is None:
        mes = datetime.now().month

    return PRODUCTOS_ESTACIONALES.get(mes, {}).get('nombre', 'Temporada Regular')


# Estadísticas para debugging
def imprimir_estadisticas():
    """Imprime estadísticas de patrones temporales."""
    print(f"📅 Patrones Temporales y Estacionalidad")
    print(f"   • Temporadas definidas: {len(PRODUCTOS_ESTACIONALES)}")
    print(f"   • Tipos de negocio con horarios: {len(HORARIOS_PICO)}")
    print(f"   • Distribuciones de días: {len(DISTRIBUCION_DIAS)}")

    print(f"\nTemporadas del año:")
    for mes, data in PRODUCTOS_ESTACIONALES.items():
        nombre_mes = datetime(2024, mes, 1).strftime('%B').capitalize()
        productos = len(data['productos'])
        factor = data['factor_precio']
        signo = '+' if factor > 1.0 else ''
        porcentaje = (factor - 1.0) * 100
        print(f"   • {nombre_mes:12} - {data['nombre']:30} ({productos} productos, {signo}{porcentaje:+.0f}%)")


if __name__ == '__main__':
    # Pruebas
    print("\n" + "="*80)
    print("PRUEBA: Patrones Temporales y Estacionalidad")
    print("="*80 + "\n")

    imprimir_estadisticas()

    print("\n" + "-"*80)
    print("Ejemplos de fechas/horas generadas:")
    print("-"*80)

    sectores_prueba = ['restaurante', 'farmacia', 'ferreteria', 'supermercado', 'spa', 'gym']

    for sector in sectores_prueba:
        print(f"\n{sector.upper()}:")
        for i in range(3):
            fecha, hora = generar_fecha_hora_realista(sector)
            # Parsear fecha para mostrar día de semana
            dt = datetime.strptime(fecha, '%Y-%m-%d')
            dia_semana = dt.strftime('%A')
            mes = dt.month
            temporada = obtener_nombre_temporada(mes)
            print(f"   {i+1}. {fecha} ({dia_semana:9}) {hora} - {temporada}")

    print("\n" + "-"*80)
    print("Productos estacionales por mes:")
    print("-"*80)

    for mes in [2, 5, 7, 12]:
        nombre_mes = datetime(2024, mes, 1).strftime('%B').capitalize()
        productos = obtener_productos_estacionales(mes)
        factor = obtener_factor_precio_estacional(mes)
        print(f"\n{nombre_mes} (factor: {factor:.2f}):")
        for prod in productos[:5]:  # Solo primeros 5
            print(f"   • {prod}")

    print("\n" + "="*80)
    print("✅ Pruebas completadas")
    print("="*80 + "\n")
