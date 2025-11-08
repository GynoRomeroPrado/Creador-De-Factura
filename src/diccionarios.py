"""
Diccionarios mejorados para generación de datos ficticios
Basado en combinatoria para mayor variedad y realismo
"""
import random

# ============================================================================
# GENERADOR DE NOMBRES DE EMPRESAS
# ============================================================================

PREFIJOS_EMPRESA = [
    # Modernos/Tech
    "Nova", "Altura", "Brisa", "Vitalis", "Prisma", "Eterna", "Nexus", "Horizonte", 
    "Impulso", "Dinámica", "Ágora", "Vertex", "Eco", "Lumina", "Prime", "Senda",
    "Forte", "Clave", "NeoGen", "Avance", "Momentum", "Aura", "Orbit", "Zenith",
    "Magna", "Axis", "Innovis", "Inspira", "Quadro", "Fusión", "Vértice", "Linea",
    "Génesis", "Armonía", "Eficientia", "Impacto", "Crescendo", "Globaliza", "Lumen",
    "Propulsa", "Supra", "Evoluciona", "Aria", "Progreso", "Infinito", "Optimus",
    
    # Digitales
    "Pixel", "Digital", "Tech", "Cloud", "Quantum", "Byte", "Core", "Smart",
    "Hyper", "Sync", "Net", "Data", "Omni", "Grid", "Cyber", "Digi", "Ultra",
    "Opti", "Flow", "Pulse", "Spark", "Matrix", "Verse",
    
    # Comerciales/Industriales
    "Crafters", "Forge", "Nest", "Track", "Vault", "Edge", "Connect", "Logic",
    "Tornillo", "Ferretería", "Proyecto", "Martillo", "Mayorista", "Stock",
    "Distribuidora", "Macro", "Compra", "Casa", "Almacén", "Depósito",
    
    # Hoteles
    "Hotel", "Hospedaje", "Posada", "Resort", "Suites", "Inn", "Lodge", "Palace",
    "Grand", "Premium", "Plaza", "Royal", "Continental", "Imperial",
    
    # Servicios Mineros
    "Minera", "Extractora", "Yacimientos", "Recursos", "Exploraciones", "Minerales",
    
    # Servicios Generales
    "Servicios", "Consultoría", "Asesoría", "Soluciones", "Grupo", "Corporación"
]

SUFIJOS_EMPRESA = [
    # Corporativos
    " Solutions", " Group", " Global", " Consulting", " Innovación", " Ventures",
    " Creativo", " Empresarial", " Proyectos", " Partners", " Capital", " Corporativo",
    " Hub", " Business", " Ideas", " Dynamics", " Corp", " Labs", " Studio", " Works",
    " Holdings", " Retail", " Services", " Logistics",
    
    # Alimentación
    " Foods", " Beverages", " Alimentos", " Catering", " Gastronómica",
    
    # Construcción
    " Construcciones", " Materiales", " Ferretería", " Distribución", " Suministros",
    " Acabados", " Infraestructura",
    
    # Tech
    " Digital", " Tech", " Cloud", " Analytics", " Data", " Systems", " Software",
    
    # General
    " Industrial", " Comercial", " Trading", " Import", " Export", " Mayorista",
    
    # Turismo/Hotelería
    " Hoteles", " Turismo", " Hospitalidad", " Resorts", " Lodging",
    
    # Minería
    " Mining", " Resources", " Exploration", " del Perú", " Andina", " del Norte"
]

GEOGRAFICOS = [
    "Latam", "Iberia", "Andes", "Pacífico", "Cono Sur", "Caribe", "Europa",
    "Andina", "Mediterránea", "Metropolitana", "del Sur", "del Norte", "Central",
    "Oriental", "Occidental", "Internacional", "Perú", "Lima", "Arequipa",
    "Cusco", "Trujillo", "Cajamarca", "Piura"
]

TIPOS_SOCIEDAD = [
    " S.A.C.", " S.R.L.", " E.I.R.L.", " S.A.", " S.A.A.", " S.C.R.L."
]

def generar_nombre_empresa(tipo_factura=None):
    """
    Genera nombre de empresa según el tipo de factura
    tipo_factura: 'hotel', 'seguro', 'general', 'con_descuento'
    """
    if tipo_factura == 'hotel':
        # Nombres más orientados a hotelería
        prefijos_hotel = ["Hotel", "Hospedaje", "Posada", "Resort", "Suites", "Inn", 
                         "Lodge", "Palace", "Grand", "Premium", "Casa", "Plaza"]
        sufijos_hotel = [" Hoteles", " Resorts", " & Spa", " Boutique", " Premium",
                        " Plaza", " Suites", " Inn", " Lodge"]
        
        base = random.choice(prefijos_hotel)
        
        # 70% añade un nombre propio/geográfico
        if random.random() < 0.7:
            nombres = ["Costa del Sol", "Andina", "Libertador", "Country Club", 
                      "Sheraton", "Westin", "Marriott", "Hilton", "El Pardo",
                      "Los Delfines", "Las Américas", "Miraflores", "San Isidro",
                      "Cusco", "Machu Picchu", "Paracas", "Colca"]
            base += " " + random.choice(nombres)
        
        # 50% añade sufijo
        if random.random() < 0.5:
            base += random.choice(sufijos_hotel)
            
    elif tipo_factura == 'seguro':
        # Nombres de aseguradoras
        prefijos_seguro = ["Seguros", "Aseguradora", "Protección", "Cobertura",
                          "Rímac", "Pacífico", "Mapfre", "La Positiva", "Protecta"]
        sufijos_seguro = [" Seguros", " del Perú", " S.A.", " Compañía de Seguros"]
        
        base = random.choice(prefijos_seguro)
        if random.random() < 0.6:
            base += random.choice(sufijos_seguro)
            
    else:
        # General: usa el sistema combinatorio original
        base = random.choice(PREFIJOS_EMPRESA) + random.choice(SUFIJOS_EMPRESA)
        
        # 30% añade un sufijo geográfico
        if random.random() < 0.3:
            base += " " + random.choice(GEOGRAFICOS)
        
        # 20% añade un número
        if random.random() < 0.2:
            base += " " + str(random.randint(1, 999))
    
    # 80% añade tipo de sociedad
    if random.random() < 0.8:
        base += random.choice(TIPOS_SOCIEDAD)
    
    return base.strip()


# ============================================================================
# GENERADOR DE DIRECCIONES GEO-ESPECÍFICAS
# ============================================================================

CALLES_PERU = [
    # Lima
    "Av. Javier Prado", "Av. Arequipa", "Av. Universitaria", "Av. La Marina",
    "Av. Venezuela", "Av. Abancay", "Av. Petit Thouars", "Av. Brasil",
    "Av. Benavides", "Av. Larco", "Av. José Pardo", "Av. Salaverry",
    "Av. Comandante Espinar", "Av. Angamos", "Av. República de Panama",
    "Av. Aramburú", "Av. Conquistadores", "Av. Camino Real", "Av. El Derby",
    "Calle Las Begonias", "Jr. de la Unión", "Jr. Carabaya",
    # Provincias
    "Av. El Sol", "Av. La Cultura", "Av. Grau", "Av. Fitzcarrald",
    "Av. España", "Av. Ejercito", "Av. Bolognesi"
]

CALLES_LATAM = [
    "Av. Libertad", "Av. Siempre Viva", "Calle Falsa", "Gran Vía",
    "Passeig de Gràcia", "Av. 9 de Julio", "Calle 50", "Av. Amazonas",
    "Av. Apoquindo", "Av. 18 de Julio", "Carrera 7", "Carrera 13",
    "Av. Reforma", "Rua das Flores", "Av. Paulista", "Av. Providencia",
    "Av. Vitacura", "Av. Santa Fe", "Av. Corrientes", "Av. 6 de Diciembre",
    "Av. Boyacá", "Calle Larios", "Av. Colón"
]

BARRIOS_LIMA = [
    "Miraflores", "San Isidro", "Lince", "Jesús María", "Magdalena",
    "Pueblo Libre", "San Miguel", "La Molina", "Surco", "Barranco",
    "Chorrillos", "San Borja", "Ate", "Santa Anita", "Los Olivos",
    "Independencia", "San Martín de Porres", "Breña", "La Victoria",
    "Cercado de Lima"
]

BARRIOS_LATAM = [
    "Centro", "Chapinero", "Las Condes", "Providencia", "Recoleta",
    "Palermo", "Balvanera", "La Mariscal", "San Nicolás", "Vicente López",
    "Kennedy", "Usaquén", "El Cangrejo", "Bela Vista", "Monserrat", "Retiro"
]

CIUDADES_PERU = [
    "Lima", "Arequipa", "Cusco", "Trujillo", "Chiclayo", "Piura", "Iquitos",
    "Huancayo", "Tacna", "Ica", "Puno", "Cajamarca", "Ayacucho", "Huaraz"
]

CIUDADES_LATAM = [
    "Bogotá", "CDMX", "Santiago", "Quito", "Buenos Aires", "Madrid",
    "Barcelona", "Montevideo", "São Paulo", "Valencia", "Málaga",
    "Guadalajara", "Córdoba", "Mendoza", "Panamá"
]

def generar_direccion(pais="Peru"):
    """Genera dirección realista según el país"""
    
    if pais == "Peru":
        via = random.choice(CALLES_PERU)
        barrio = random.choice(BARRIOS_LIMA)
        ciudad = random.choice(CIUDADES_PERU)
    else:
        via = random.choice(CALLES_LATAM)
        barrio = random.choice(BARRIOS_LATAM)
        ciudad = random.choice(CIUDADES_LATAM)
    
    num = f"{random.randint(100, 9999)}"
    
    # 40% usa formato con número y complemento
    if random.random() < 0.4:
        complementos = ["Piso", "Depto", "Oficina", "Local", "Int.", "Torre"]
        complemento = random.choice(complementos) + f" {random.randint(1, 50)}"
        if random.random() < 0.3:
            # Añade letra
            complemento += chr(random.randint(65, 72))  # A-H
        linea = f"{via} {num}, {complemento}"
    else:
        linea = f"{via} {num}"
    
    # Formato completo
    return f"{linea}, {barrio}, {ciudad}"


# ============================================================================
# CATÁLOGO DE ITEMS EXTENDIDO
# ============================================================================

# Caramelos y dulces
CARAMELOS = [
    ("Paquete surtido de caramelos frutales", "KGM", (5.00, 15.00)),
    ("Gomitas ácidas mix", "KGM", (8.00, 20.00)),
    ("Caja de chicles de menta sin azúcar", "NIU", (12.00, 25.00)),
    ("Chocolate con leche", "KGM", (15.00, 35.00)),
    ("Paletas artesanales", "NIU", (1.00, 3.00)),
    ("Caramelos duros de eucalipto", "KGM", (6.00, 12.00)),
    ("Bombones surtidos", "KGM", (25.00, 60.00)),
    ("Turrón de maní", "NIU", (3.00, 8.00)),
    ("Malvaviscos", "KGM", (10.00, 22.00)),
    ("Barra de cereal con chocolate", "NIU", (2.00, 5.00)),
]

# Bebidas no alcohólicas
BEBIDAS_NO_ALC = [
    ("Bebida gaseosa cola", "LTR", (2.00, 5.00)),
    ("Agua mineral sin gas", "LTR", (1.00, 3.00)),
    ("Jugo de naranja", "LTR", (4.00, 8.00)),
    ("Bebida energética", "LTR", (5.00, 10.00)),
    ("Té helado limón", "LTR", (3.00, 6.00)),
    ("Agua saborizada", "LTR", (2.00, 4.00)),
    ("Limonada natural", "LTR", (3.00, 7.00)),
    ("Refresco de uva", "LTR", (2.00, 5.00)),
    ("Soda tónica", "LTR", (3.00, 6.00)),
    ("Bebida isotónica", "LTR", (4.00, 8.00)),
]

# Bebidas alcohólicas
BEBIDAS_ALC = [
    ("Cerveza rubia pack", "NIU", (18.00, 35.00)),
    ("Cerveza artesanal IPA", "LTR", (12.00, 25.00)),
    ("Vino tinto Malbec", "LTR", (35.00, 120.00)),
    ("Vino blanco Sauvignon Blanc", "LTR", (30.00, 100.00)),
    ("Ron añejo", "LTR", (50.00, 150.00)),
    ("Whisky blended", "LTR", (80.00, 250.00)),
    ("Vodka triple destilado", "LTR", (40.00, 100.00)),
    ("Ginebra London Dry", "LTR", (60.00, 180.00)),
    ("Sidra espumante", "LTR", (15.00, 35.00)),
    ("Aperitivo amargo", "LTR", (25.00, 70.00)),
]

# Materiales de construcción
MATERIALES_CONSTRUCCION = [
    ("Cemento Portland bolsa", "BG", (22.00, 28.00)),
    ("Arena fina", "M3", (45.00, 65.00)),
    ("Grava 3/4\"", "M3", (50.00, 70.00)),
    ("Yeso construcción", "BG", (8.00, 15.00)),
    ("Ladrillo hueco 12x18x33", "MIL", (350.00, 550.00)),
    ("Bloque de hormigón 20x20x40", "NIU", (3.00, 6.00)),
    ("Varilla corrugada 3/8\" x 9m", "NIU", (18.00, 28.00)),
    ("Clavos 3\" caja", "KGM", (5.00, 10.00)),
    ("Tornillos para madera 1\" caja", "NIU", (8.00, 15.00)),
    ("Pintura látex interior", "GLI", (35.00, 80.00)),
    ("Silicona neutra", "NIU", (8.00, 15.00)),
    ("Cinta aisladora", "NIU", (2.00, 5.00)),
    ("Lámpara LED 9W E27", "NIU", (10.00, 20.00)),
    ("Tubo PVC 1/2\" x 3m", "NIU", (8.00, 15.00)),
    ("Cable THHN 12 AWG", "MTR", (2.50, 5.00)),
]

# Herramientas y EPP
HERRAMIENTAS_EPP = [
    ("Brocha 2\" cerdas mixtas", "NIU", (8.00, 15.00)),
    ("Rodillo 9\" felpa media", "NIU", (12.00, 25.00)),
    ("Martillo uña 16 oz", "NIU", (25.00, 50.00)),
    ("Serrucho 20\"", "NIU", (30.00, 60.00)),
    ("Taladro percutor 13mm", "NIU", (180.00, 350.00)),
    ("Amoladora angular 4-1/2\"", "NIU", (150.00, 300.00)),
    ("Llave ajustable 10\"", "NIU", (20.00, 40.00)),
    ("Alicate universal 8\"", "NIU", (18.00, 35.00)),
    ("Destornillador Phillips 6\"", "NIU", (8.00, 15.00)),
    ("Guantes de obrero", "PAR", (5.00, 12.00)),
    ("Casco de seguridad clase E", "NIU", (15.00, 35.00)),
    ("Gafas de seguridad", "NIU", (10.00, 20.00)),
    ("Mascarilla N95", "NIU", (2.00, 5.00)),
    ("Cinta métrica 5m", "NIU", (15.00, 30.00)),
    ("Nivel burbuja 24\"", "NIU", (25.00, 50.00)),
]

# Agrupar por categoría para fácil acceso
ITEMS_POR_CATEGORIA = {
    'caramelos': CARAMELOS,
    'bebidas_no_alc': BEBIDAS_NO_ALC,
    'bebidas_alc': BEBIDAS_ALC,
    'construccion': MATERIALES_CONSTRUCCION,
    'herramientas': HERRAMIENTAS_EPP,
}

# Variantes que se pueden añadir
VARIANTES_SABOR = [
    " limón", " manzana", " frutos rojos", " vainilla", " chocolate",
    " cereza", " naranja", " fresa", " piña", " coco"
]

VARIANTES_MARCA = [
    " marca económica", " marca premium", " importado", " nacional",
    " artesanal", " orgánico"
]

VARIANTES_PRESENTACION = [
    " pack x3", " pack x6", " pack x12", " pack x24", " a granel",
    " caja x10", " caja x20"
]

VARIANTES_CARACTERISTICA = [
    " sin gluten", " sin azúcar", " bajo sodio", " light", " diet",
    " zero", " sin lactosa"
]

def generar_item_con_variantes(descripcion_base):
    """Añade variantes aleatorias a un item base"""
    resultado = descripcion_base
    
    # 30% añade sabor (solo para alimentos/bebidas)
    if random.random() < 0.3:
        if any(palabra in descripcion_base.lower() for palabra in 
               ['bebida', 'jugo', 'té', 'caramelo', 'gomita', 'chocolate', 'chicle']):
            resultado += random.choice(VARIANTES_SABOR)
    
    # 20% añade marca
    if random.random() < 0.2:
        resultado += random.choice(VARIANTES_MARCA)
    
    # 25% añade presentación
    if random.random() < 0.25:
        resultado += random.choice(VARIANTES_PRESENTACION)
    
    # 15% añade característica (solo alimentos/bebidas)
    if random.random() < 0.15:
        if any(palabra in descripcion_base.lower() for palabra in 
               ['bebida', 'jugo', 'té', 'caramelo', 'chocolate']):
            resultado += random.choice(VARIANTES_CARACTERISTICA)
    
    return resultado.strip()


if __name__ == "__main__":
    # Pruebas
    print("=== PRUEBAS DE DICCIONARIOS ===\n")
    
    print("Empresas generales:")
    for _ in range(5):
        print(f"  - {generar_nombre_empresa('general')}")
    
    print("\nHoteles:")
    for _ in range(5):
        print(f"  - {generar_nombre_empresa('hotel')}")
    
    print("\nDirecciones Perú:")
    for _ in range(5):
        print(f"  - {generar_direccion('Peru')}")
    
    print("\nItems con variantes (construcción):")
    for item, unidad, rango in MATERIALES_CONSTRUCCION[:5]:
        print(f"  - {generar_item_con_variantes(item)}")
