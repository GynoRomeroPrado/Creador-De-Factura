"""
Diccionarios de datos realistas para la generación de facturas
"""
import random

# Catálogo de Productos Reales
ITEMS_POR_CATEGORIA = {
    'construccion': [
        ("Cemento Sol Tipo I (42.5kg)", "BOL", (26.50, 28.90)),
        ("Ladrillo King Kong 18 Huecos Lark", "MILLAR", (680.00, 750.00)),
        ("Fierro Corrugado Aceros Arequipa 1/2\" x 9m", "VAR", (38.50, 42.00)),
        ("Arena Gruesa (m3)", "M3", (45.00, 60.00)),
        ("Piedra Chancada 1/2\" (m3)", "M3", (55.00, 70.00)),
        ("Tubo PVC SAP Pavco 4\" Desague", "UND", (22.00, 28.00)),
        ("Pegamento para PVC Oatey (1/4 gal)", "UND", (18.00, 25.00)),
        ("Pintura Latex Vencedor Supermate Blanco (4L)", "GLN", (45.00, 55.00)),
        ("Thinner Acrílico Vencedor (Galón)", "GLN", (25.00, 35.00)),
        ("Disco de Corte Metal 4.5\" Dewalt", "UND", (4.50, 8.00)),
        ("Guantes de Cuero Reforzado", "PAR", (12.00, 18.00)),
        ("Casco de Seguridad 3M Blanco", "UND", (25.00, 45.00)),
    ],
    'tech': [
        ("Laptop HP Pavilion 15-dk1000 (i7, 16GB, 512GB SSD)", "UND", (3500.00, 4200.00)),
        ("Monitor LG 24\" IPS Full HD", "UND", (450.00, 600.00)),
        ("Mouse Inalámbrico Logitech M185", "UND", (35.00, 50.00)),
        ("Teclado Mecánico Redragon Kumara", "UND", (120.00, 180.00)),
        ("Disco Duro Externo Toshiba 1TB USB 3.0", "UND", (180.00, 250.00)),
        ("Memoria RAM Kingston Fury 8GB DDR4 3200MHz", "UND", (110.00, 150.00)),
        ("Impresora Multifuncional Epson L3210", "UND", (650.00, 800.00)),
        ("Cable HDMI 2.0 1.8m Ugreen", "UND", (25.00, 40.00)),
        ("Router TP-Link Archer C6 AC1200", "UND", (150.00, 220.00)),
        ("Silla Ergonómica Gamer Cougar", "UND", (600.00, 900.00)),
    ],
    'restaurante': [
        ("Lomo Saltado al Jugo", "PLAT", (38.00, 48.00)),
        ("Ceviche de Pescado Clásico", "PLAT", (35.00, 45.00)),
        ("Ají de Gallina", "PLAT", (28.00, 35.00)),
        ("Arroz con Mariscos", "PLAT", (40.00, 55.00)),
        ("Causa Limeña de Pollo", "ENTR", (18.00, 25.00)),
        ("Pisco Sour Catedral", "BEB", (22.00, 30.00)),
        ("Chicha Morada Jarra 1L", "JAR", (15.00, 22.00)),
        ("Inca Kola 1.5L", "BOT", (10.00, 15.00)),
        ("Suspiro a la Limeña", "POST", (12.00, 18.00)),
        ("Café Espresso", "TAZ", (8.00, 12.00)),
    ],
    'supermercado': [
        ("Arroz Costeño Extra 5kg", "BLS", (18.50, 22.00)),
        ("Aceite Primor Premium 1L", "BOT", (11.00, 14.00)),
        ("Leche Gloria Azul Pack x6", "PCK", (22.00, 26.00)),
        ("Papel Higiénico Elite Doble Hoja x12", "PAQ", (15.00, 20.00)),
        ("Detergente Ariel 2.5kg", "BLS", (35.00, 45.00)),
        ("Pollo Fresco San Fernando (kg)", "KG", (9.50, 12.00)),
        ("Huevos Pardos La Calera x30", "JAB", (16.00, 22.00)),
        ("Yogurt Gloria Fresa 1kg", "BOT", (6.50, 8.50)),
        ("Pan de Molde Bimbo Blanco Grande", "BLS", (12.00, 15.00)),
        ("Gaseosa Coca Cola 3L", "BOT", (10.00, 13.00)),
    ],
    'servicios': [
        ("Servicio de Mantenimiento Preventivo de Servidores", "SRV", (800.00, 1500.00)),
        ("Consultoría en Gestión de Procesos (Horas)", "HOR", (150.00, 300.00)),
        ("Desarrollo de Módulo de Facturación Electrónica", "PROY", (2500.00, 5000.00)),
        ("Soporte Técnico Remoto Mensual", "MES", (500.00, 1200.00)),
        ("Capacitación en Seguridad y Salud Ocupacional", "SES", (400.00, 800.00)),
        ("Servicio de Limpieza Integral de Oficinas", "MES", (1200.00, 2500.00)),
        ("Alquiler de Sala de Conferencias (Día)", "DIA", (800.00, 1500.00)),
        ("Servicio de Courier Local", "ENV", (15.00, 35.00)),
    ],
    'transporte': [
        ("Flete Lima - Arequipa (Carga General)", "VJE", (1800.00, 2500.00)),
        ("Transporte de Personal (Ruta Norte)", "MES", (3500.00, 5000.00)),
        ("Servicio de Mudanza Local (Camión 5TN)", "SRV", (600.00, 1200.00)),
        ("Envío de Paquetería Express", "ENV", (25.00, 80.00)),
        ("Alquiler de Camioneta 4x4 (Día)", "DIA", (250.00, 450.00)),
    ],
    'farmacia': [
        ("Paracetamol 500mg x100 (Genérico)", "CJA", (8.00, 15.00)),
        ("Amoxicilina 500mg x10 (Marca)", "CJA", (25.00, 40.00)),
        ("Alcohol Medicinal 96° 1L", "BOT", (12.00, 18.00)),
        ("Mascarillas KN95 Caja x20", "CJA", (15.00, 25.00)),
        ("Vitamina C 1000mg Efervescente x10", "TUB", (18.00, 28.00)),
        ("Protector Solar Eucerin FPS 50+", "UND", (80.00, 120.00)),
    ]
}

# Nombres de Empresas Realistas
EMPRESAS_REALISTAS = {
    'construccion': [
        "Constructora Los Andes S.A.C.", "Inversiones Inmobiliarias del Sur S.A.",
        "Materiales de Construcción El Roble E.I.R.L.", "Proyectos y Obras Civiles Lima S.A.C."
    ],
    'tech': [
        "Tecnología Digital Avanzada S.A.C.", "Sistemas y Soluciones IT S.R.L.",
        "Innovación Tecnológica del Perú S.A.", "CompuVentas Express E.I.R.L."
    ],
    'restaurante': [
        "Gastronomía Peruana S.A.C.", "Restaurante El Sabor Norteño E.I.R.L.",
        "Inversiones Gastronómicas del Pacífico S.A.", "Cadena de Restaurantes El Buen Gusto S.A.C."
    ],
    'general': [
        "Distribuidora Comercial Lima S.A.C.", "Importaciones Generales del Perú S.R.L.",
        "Servicios Empresariales Integrales S.A.", "Comercializadora Universal E.I.R.L."
    ]
}

def generar_nombre_empresa(tipo: str = None) -> str:
    """Retorna un nombre de empresa realista según el tipo"""
    if tipo in EMPRESAS_REALISTAS:
        return random.choice(EMPRESAS_REALISTAS[tipo])
    # Fallback o aleatorio
    categoria = random.choice(list(EMPRESAS_REALISTAS.keys()))
    return random.choice(EMPRESAS_REALISTAS[categoria])

def generar_direccion(pais: str = 'Peru') -> str:
    """Genera direcciones más detalladas"""
    calles = ["Av. Javier Prado Este", "Av. Arequipa", "Jr. de la Unión", "Av. La Marina", "Calle Los Pinos", "Av. Benavides"]
    numeros = [str(random.randint(100, 5000)) for _ in range(10)]
    distritos = ["San Isidro", "Miraflores", "Santiago de Surco", "La Victoria", "Cercado de Lima", "San Borja"]
    
    return f"{random.choice(calles)} {random.choice(numeros)}, {random.choice(distritos)}, Lima"

def generar_nombre_completo() -> str:
    nombres = ["Juan", "Maria", "Carlos", "Ana", "Luis", "Rosa", "Jorge", "Carmen"]
    apellidos = ["Perez", "Garcia", "Rodriguez", "Lopez", "Sanchez", "Gonzales", "Torres"]
    return f"{random.choice(nombres)} {random.choice(apellidos)} {random.choice(apellidos)}"

def generar_item_con_variantes(descripcion_base: str) -> str:
    """Añade variantes realistas a los items (colores, marcas, series)"""
    if random.random() < 0.3: # 30% de probabilidad de añadir variante
        variantes = ["(Oferta)", "(Importado)", "Color: Negro", "Modelo 2025", "Serie X"]
        return f"{descripcion_base} {random.choice(variantes)}"
    return descripcion_base
