"""
Datos específicos por sector para generar facturas más realistas.
Incluye 15+ sectores con productos, precios y características propias.
"""

import random
from typing import Dict, List, Tuple

# ============================================================================
# SECTORES Y SUS CARACTERÍSTICAS ESPECÍFICAS
# ============================================================================

SECTORES_ESPECIFICOS = {
    'restaurante': {
        'peso': 15,  # Probabilidad relativa de selección
        'razones_sociales': [
            'RESTAURANTE LA MAR',
            'CENTRAL RESTAURANTE',
            'MAIDO COCINA NIKKEI',
            'OSSO CARNICERIA Y SALUMERIA',
            'ASTRID Y GASTON',
            'EL MERCADO',
            'FIESTA RESTAURANTE GOURMET',
            'LA ROSA NAUTICA',
            'ISOLINA TABERNA PERUANA',
            'TANTA RESTAURANTE',
        ],
        'sufijos': ['SAC', 'EIRL', 'SRL'],
        'productos': [
            ('CEVICHE CLASICO', 35, 65),
            ('LOMO SALTADO', 28, 45),
            ('ANTICUCHO DE CORAZON', 18, 32),
            ('AJI DE GALLINA', 22, 35),
            ('CAUSA LIMEÑA', 18, 28),
            ('ARROZ CON MARISCOS', 32, 48),
            ('TACU TACU CON LOMO', 28, 42),
            ('CHAUFA DE POLLO', 18, 28),
            ('CHICHARRON DE PESCADO', 32, 45),
            ('SUDADO DE PESCADO', 28, 38),
            ('PISCO SOUR', 18, 28),
            ('CHILCANO', 15, 25),
            ('INCA KOLA 1.5L', 8, 12),
            ('CERVEZA CUSQUEÑA', 12, 18),
            ('AGUA SAN LUIS 625ML', 3, 5),
        ],
        'unidades': ['UND', 'PORCION'],
        'rangos_ticket': (80, 250),
        'items_tipicos': (2, 8),
        'horario_pico': (12, 15, 19, 22),  # Almuerzo y cena
    },

    'farmacia': {
        'peso': 12,
        'razones_sociales': [
            'INKAFARMA',
            'MIFARMA',
            'BOTICAS ARCANGEL',
            'BOTICAS Y SALUD',
            'FARMACIA UNIVERSAL',
            'BOTICAS PERU',
            'FARMACIAS PERUANAS',
        ],
        'sufijos': ['SAC', 'SRL'],
        'productos': [
            ('PARACETAMOL 500MG X 20 TAB', 5, 12),
            ('IBUPROFENO 400MG X 10 TAB', 8, 15),
            ('AMOXICILINA 500MG X 12 CAP', 15, 25),
            ('LORATADINA 10MG X 10 TAB', 8, 14),
            ('OMEPRAZOL 20MG X 14 CAP', 12, 20),
            ('ALCOHOL GEL 250ML', 12, 18),
            ('MASCARILLA KN95 X 10 UND', 18, 28),
            ('VITAMINA C 1000MG X 30 TAB', 25, 40),
            ('COMPLEJO B X 30 TAB', 20, 35),
            ('TERMOMETRO DIGITAL', 25, 45),
            ('GASAS ESTERILES X 50 UND', 8, 15),
            ('CURITAS SURTIDAS X 100 UND', 12, 18),
        ],
        'unidades': ['UND', 'CAJA', 'FRASCO', 'BLISTER'],
        'items_tipicos': (1, 5),
    },

    'ferreteria': {
        'peso': 10,
        'razones_sociales': [
            'SODIMAC PERU',
            'PROMART HOMECENTER',
            'MAESTRO HOME CENTER',
            'ACE HOMECENTER',
            'CONSTRURAMA',
        ],
        'sufijos': ['SAC', 'SRL'],
        'productos': [
            ('CEMENTO PORTLAND TIPO I X 42.5KG', 22, 28),
            ('FIERRO CORRUGADO 1/2" X 9M', 25, 35),
            ('FIERRO CORRUGADO 3/8" X 9M', 18, 25),
            ('ALAMBRE RECOCIDO N°16 X KG', 4, 6),
            ('PINTURA LATEX BLANCO BALDE 5GL', 85, 120),
            ('PINTURA ESMALTE GRIS PERLA 1GL', 35, 55),
            ('THINNER ACRILICO 1GL', 18, 28),
            ('LIJA PARA MADERA N°80 X 10 UND', 8, 12),
            ('BROCHA 4" CERDA NATURAL', 15, 25),
            ('RODILLO LANA 9" + BANDEJA', 18, 28),
            ('TORNILLO AUTOPERFORANTE 1" X 100', 12, 18),
            ('CLAVOS 3" X KG', 8, 12),
            ('TUBO PVC 2" X 3M', 15, 22),
            ('CODO PVC 2" X 90°', 3, 5),
            ('PEGAMENTO PVC 250ML', 12, 18),
        ],
        'unidades': ['UND', 'BOLSA', 'BALDE', 'VARILLA', 'KG'],
        'items_tipicos': (3, 15),
    },

    'supermercado': {
        'peso': 14,
        'razones_sociales': [
            'SUPERMERCADOS PERUANOS',
            'PLAZA VEA',
            'WONG',
            'METRO',
            'TOTTUS',
            'MASS',
        ],
        'sufijos': ['SAC'],
        'productos': [
            ('ARROZ SUPERIOR X 5KG', 18, 25),
            ('ACEITE VEGETAL PRIMOR 1L', 8, 12),
            ('AZUCAR BLANCA X KG', 3, 4.5),
            ('LECHE GLORIA ENTERA X 12 UND', 35, 45),
            ('HUEVOS PARDOS X 30 UND', 15, 20),
            ('POLLO ENTERO X KG', 8, 12),
            ('PAN INTEGRAL BIMBO', 4, 6),
            ('PAPEL HIGIENICO ELITE X 24 ROLLOS', 28, 38),
            ('DETERGENTE ARIEL 2.6KG', 28, 35),
            ('JABON BOLIVAR X 3 UND', 5, 8),
            ('SHAMPOO SEDAL 400ML', 12, 18),
            ('PASTA DENTAL COLGATE 150G', 8, 12),
        ],
        'unidades': ['UND', 'KG', 'PAQUETE'],
        'items_tipicos': (8, 25),
    },

    'electrodomesticos': {
        'peso': 6,
        'razones_sociales': [
            'HIRAOKA',
            'CARSA',
            'EFE',
            'ELEKTRA',
            'COOLBOX STORE',
        ],
        'sufijos': ['SAC', 'EIRL'],
        'productos': [
            ('REFRIGERADORA SAMSUNG 300L NO FROST', 1200, 1800),
            ('LAVADORA LG 12KG TURBO WASH', 900, 1400),
            ('COCINA INDURAMA 4 HORNILLAS', 450, 680),
            ('MICROONDAS PANASONIC 0.9CF', 250, 380),
            ('LICUADORA OSTER 3 VELOCIDADES', 120, 180),
            ('PLANCHA ELECTROLUX VAPOR', 65, 95),
            ('ASPIRADORA ELECTROLUX 1400W', 280, 420),
            ('VENTILADOR DE PIE IMACO 18"', 80, 120),
            ('TV LG 43" SMART TV 4K', 1100, 1600),
            ('LAPTOP HP 15.6" CORE I5 8GB', 1800, 2400),
        ],
        'unidades': ['UND'],
        'items_tipicos': (1, 3),
    },

    'veterinaria': {
        'peso': 5,
        'razones_sociales': [
            'VETERINARIA PET VET',
            'CLINICA VETERINARIA SAN FRANCISCO',
            'PET CENTER',
            'VETERINARIA ANIMAL HOUSE',
        ],
        'sufijos': ['EIRL', 'SAC'],
        'productos': [
            ('CONSULTA VETERINARIA GENERAL', 40, 80),
            ('VACUNA ANTIRRÁBICA CANINA', 35, 55),
            ('VACUNA SEXTUPLE CANINA', 45, 70),
            ('DESPARASITACIÓN INTERNA CANINA', 25, 40),
            ('CONTROL DE PULGAS/GARRAPATAS', 30, 50),
            ('ALIMENTO ROYAL CANIN ADULTO 15KG', 180, 250),
            ('ALIMENTO RICOCAN ADULTO 20KG', 85, 120),
            ('SNACKS DENTALES X 10 UND', 15, 25),
            ('SHAMPOO ANTIPULGAS 500ML', 25, 40),
            ('COLLAR ANTIPULGAS', 35, 55),
        ],
        'unidades': ['UND', 'SERVICIO'],
        'items_tipicos': (1, 4),
    },

    'gym': {
        'peso': 4,
        'razones_sociales': [
            'GOLD\'S GYM',
            'BODYTECH',
            'SPORTLIFE',
            'FIT CLUB',
            'TRAINING CENTER',
        ],
        'sufijos': ['SAC', 'EIRL'],
        'productos': [
            ('MEMBRESIA MENSUAL', 120, 180),
            ('MEMBRESIA TRIMESTRAL', 320, 480),
            ('CLASE FUNCIONAL X 10 SESIONES', 150, 200),
            ('CLASE SPINNING X 10 SESIONES', 140, 190),
            ('ENTRENAMIENTO PERSONALIZADO X 8 SESIONES', 280, 400),
            ('PROTEINA WHEY OPTIMUM 2LB', 120, 160),
            ('CREATINA MICRONIZADA 300G', 65, 95),
            ('BCAA 200 CAPS', 75, 110),
            ('SHAKER + TOALLA GYM', 25, 35),
        ],
        'unidades': ['SERVICIO', 'UND'],
        'items_tipicos': (1, 3),
    },

    'spa': {
        'peso': 3,
        'razones_sociales': [
            'MONTALVO SPA',
            'ZEN SPA & WELLNESS',
            'AROMA SPA',
            'ESSENZA SPA',
        ],
        'sufijos': ['SAC', 'EIRL'],
        'productos': [
            ('MASAJE RELAJANTE 60MIN', 80, 120),
            ('MASAJE DESCONTRACTURANTE 90MIN', 110, 160),
            ('FACIAL HIDRATANTE', 90, 140),
            ('EXFOLIACION CORPORAL', 70, 110),
            ('REFLEXOLOGIA 45MIN', 60, 90),
            ('MANICURE + PEDICURE', 40, 70),
            ('DEPILACION PIERNAS COMPLETAS', 60, 90),
            ('SAUNA + JACUZZI', 50, 80),
        ],
        'unidades': ['SERVICIO'],
        'items_tipicos': (1, 3),
    },

    'educacion': {
        'peso': 8,
        'razones_sociales': [
            'COLEGIO SAN JOSE',
            'I.E. SANTA MARIA',
            'COLEGIO ALPAMAYO',
            'I.E. SAN PEDRO',
            'ACADEMIA PAMER',
            'INSTITUTO TOULOUSE LAUTREC',
        ],
        'sufijos': ['SAC', 'ASOCIACION', 'EIRL'],
        'productos': [
            ('MATRICULA SEMESTRE 2025-I', 800, 1500),
            ('PENSION MARZO 2025', 350, 650),
            ('PENSION ABRIL 2025', 350, 650),
            ('MATERIAL DIDACTICO ANUAL', 50, 120),
            ('UNIFORME COMPLETO', 180, 280),
            ('LIBROS Y TEXTOS', 120, 220),
            ('CUOTA DE INGRESO', 500, 1200),
        ],
        'unidades': ['SERVICIO', 'UND'],
        'items_tipicos': (1, 3),
    },

    'odontologia': {
        'peso': 5,
        'razones_sociales': [
            'CLINICA DENTAL DENTAMAX',
            'CENTRO ODONTOLOGICO SONRIE',
            'CLINICA DENTAL ORTODONCIA',
            'DENTAL CARE PERU',
        ],
        'sufijos': ['SAC', 'EIRL'],
        'productos': [
            ('LIMPIEZA DENTAL', 80, 150),
            ('CONSULTA ODONTOLOGICA', 40, 70),
            ('RESINA DENTAL 1 PIEZA', 100, 180),
            ('ENDODONCIA 1 CONDUCTO', 250, 400),
            ('EXTRACCION SIMPLE', 80, 130),
            ('ORTODONCIA MENSUALIDAD', 200, 350),
            ('BRACKETS METALICOS', 800, 1200),
            ('PROFILAXIS + FLUORIZACIÓN', 90, 140),
        ],
        'unidades': ['SERVICIO'],
        'items_tipicos': (1, 2),
    },

    'automotriz': {
        'peso': 7,
        'razones_sociales': [
            'AUTOSERVICIOS PEREZ',
            'TALLER MECANICO EL ROBLE',
            'LUBRICENTRO EXPRESS',
            'MULTISERVICIOS AUTOMOTRIZ',
        ],
        'sufijos': ['EIRL', 'SAC'],
        'productos': [
            ('CAMBIO DE ACEITE MOTOR + FILTRO', 120, 180),
            ('ALINEACION Y BALANCEO 4 RUEDAS', 80, 120),
            ('PASTILLAS DE FRENO DELANTERAS', 150, 250),
            ('PASTILLAS DE FRENO TRASERAS', 120, 200),
            ('BATERIA 12V 60AH', 280, 420),
            ('NEUMATICO 185/65 R15', 180, 280),
            ('CAMBIO DE LIQUIDO DE FRENOS', 60, 90),
            ('ESCANEO COMPUTARIZADO', 50, 80),
            ('LIMPIEZA DE INYECTORES', 100, 150),
        ],
        'unidades': ['SERVICIO', 'UND'],
        'items_tipicos': (1, 4),
    },

    'libreria': {
        'peso': 6,
        'razones_sociales': [
            'LIBRERIA NACIONAL',
            'TAI LOY',
            'LIBRERIA IBERO',
            'BOOKS & BITS',
        ],
        'sufijos': ['SAC', 'EIRL'],
        'productos': [
            ('CUADERNO ALPHA 100 HOJAS', 8, 12),
            ('LAPICERO FABER CASTELL AZUL', 1.5, 3),
            ('RESALTADOR STABILO X 4 COLORES', 12, 18),
            ('BORRADOR ARTESCO', 1, 2),
            ('CORRECTOR LIQUIDO', 3, 5),
            ('PAPEL BOND A4 X 500 HOJAS', 15, 22),
            ('ARCHIVADOR PLASTIFICADO', 8, 14),
            ('CALCULADORA CIENTIFICA CASIO', 45, 75),
            ('MOCHILA ESCOLAR', 60, 100),
            ('TIJERA METALICA', 8, 14),
        ],
        'unidades': ['UND', 'PAQUETE'],
        'items_tipicos': (3, 10),
    },

    'panaderia': {
        'peso': 8,
        'razones_sociales': [
            'PANADERIA LA BONBONNIERE',
            'BEMBOS PANADERIA',
            'PAN DE LA CHOLA',
            'PANADERIA SAN ANTONIO',
        ],
        'sufijos': ['EIRL', 'SAC'],
        'productos': [
            ('PAN FRANCES X 6 UND', 2, 4),
            ('PAN INTEGRAL X 6 UND', 4, 7),
            ('TORTA DE CHOCOLATE 1KG', 35, 55),
            ('EMPANADA DE POLLO X UND', 3, 5),
            ('ALFAJOR ARTESANAL X UND', 2.5, 4),
            ('CROISSANT X UND', 3.5, 6),
            ('QUEQUE INGLES X PORCION', 4, 7),
            ('DONAS SURTIDAS X 6 UND', 12, 18),
        ],
        'unidades': ['UND', 'KG', 'PORCION'],
        'items_tipicos': (3, 12),
    },

    'optica': {
        'peso': 4,
        'razones_sociales': [
            'OPTICAS GMO',
            'ECONOPTICAS',
            'OPTICAS LUX',
            'VISION CENTER',
        ],
        'sufijos': ['SAC', 'EIRL'],
        'productos': [
            ('EXAMEN OPTOMETRICO COMPLETO', 40, 70),
            ('LENTES MONOFOCALES + ARMAZON', 180, 350),
            ('LENTES PROGRESIVOS + ARMAZON', 450, 750),
            ('LENTES DE CONTACTO MENSUAL X 2 UND', 60, 100),
            ('SOLUCION MULTIPROPOSITO 360ML', 25, 40),
            ('ESTUCHE PARA LENTES', 15, 25),
            ('ARMAZON METALICO', 80, 150),
            ('LENTES DE SOL POLARIZADOS', 120, 250),
        ],
        'unidades': ['SERVICIO', 'UND'],
        'items_tipicos': (1, 3),
    },

    'floristeria': {
        'peso': 3,
        'razones_sociales': [
            'FLORISTERIA ROSATEL',
            'FLORES DEL CAMPO',
            'AROMA FLORAL',
        ],
        'sufijos': ['SAC', 'EIRL'],
        'productos': [
            ('RAMO DE 12 ROSAS ROJAS', 45, 75),
            ('ARREGLO FLORAL MEDIANO', 80, 130),
            ('ARREGLO FLORAL GRANDE', 150, 250),
            ('ORQUIDEA EN MACETA', 60, 95),
            ('CORONA FUNEBRE', 180, 320),
            ('RAMO DE GIRASOLES X 6', 35, 60),
            ('BOUQUET MIXTO', 55, 90),
        ],
        'unidades': ['UND'],
        'items_tipicos': (1, 2),
    },
}

# ============================================================================
# FUNCIONES AUXILIARES
# ============================================================================

def obtener_sector_aleatorio() -> str:
    """Selecciona un sector aleatorio ponderado por su peso."""
    sectores = list(SECTORES_ESPECIFICOS.keys())
    pesos = [SECTORES_ESPECIFICOS[s]['peso'] for s in sectores]
    return random.choices(sectores, weights=pesos, k=1)[0]


def obtener_razon_social(sector: str) -> str:
    """Genera razón social con sufijo legal."""
    datos = SECTORES_ESPECIFICOS[sector]
    base = random.choice(datos['razones_sociales'])
    sufijo = random.choice(datos['sufijos'])
    return f"{base} {sufijo}"


def obtener_productos_sector(sector: str, cantidad: int) -> List[Dict]:
    """Obtiene productos aleatorios de un sector."""
    datos = SECTORES_ESPECIFICOS[sector]
    productos_disponibles = datos['productos']

    # Si pide más productos de los disponibles, repetir algunos
    if cantidad > len(productos_disponibles):
        productos_seleccionados = random.choices(productos_disponibles, k=cantidad)
    else:
        productos_seleccionados = random.sample(productos_disponibles, cantidad)

    items = []
    for i, (nombre, precio_min, precio_max) in enumerate(productos_seleccionados, 1):
        # Generar precio realista con psicología de precios
        precio = generar_precio_realista(precio_min, precio_max)
        cantidad_item = random.randint(1, 5) if sector in ['supermercado', 'libreria'] else random.randint(1, 3)
        unidad = random.choice(datos['unidades'])

        items.append({
            'numero': i,
            'descripcion': nombre,
            'cantidad': cantidad_item,
            'unidad': unidad,
            'precio_unitario': precio,
            'valor_venta': round(precio * cantidad_item, 2)
        })

    return items


def generar_precio_realista(precio_min: float, precio_max: float) -> float:
    """
    Genera precio con variación realista y psicología de precios.
    Redondea a .00, .50, .90, .95, .99 (terminaciones psicológicas).
    """
    precio_base = random.uniform(precio_min, precio_max)

    # Terminaciones psicológicas comunes en retail
    terminaciones = [0.00, 0.50, 0.90, 0.95, 0.99]
    pesos_terminaciones = [20, 15, 30, 20, 15]  # .90 es más común

    terminacion = random.choices(terminaciones, weights=pesos_terminaciones, k=1)[0]
    precio_final = int(precio_base) + terminacion

    return round(precio_final, 2)


def obtener_rango_items_sector(sector: str) -> Tuple[int, int]:
    """Retorna el rango típico de items para un sector."""
    datos = SECTORES_ESPECIFICOS.get(sector, {})
    return datos.get('items_tipicos', (3, 10))


# ============================================================================
# DATOS EXPORTABLES
# ============================================================================

__all__ = [
    'SECTORES_ESPECIFICOS',
    'obtener_sector_aleatorio',
    'obtener_razon_social',
    'obtener_productos_sector',
    'generar_precio_realista',
    'obtener_rango_items_sector',
]
