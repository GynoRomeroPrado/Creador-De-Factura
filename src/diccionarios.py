"""
Diccionarios mejorados para generación de datos ficticios
Basado en combinatoria para mayor variedad y realismo
Sistema expandido con 500,000+ combinaciones posibles
"""
import random

# ============================================================================
# GENERADOR DE NOMBRES DE EMPRESAS
# ============================================================================

PREFIJOS_EMPRESA = [
    # Modernos/Tech (50+)
    "Nova", "Altura", "Brisa", "Vitalis", "Prisma", "Eterna", "Nexus", "Horizonte",
    "Impulso", "Dinámica", "Ágora", "Vertex", "Eco", "Lumina", "Prime", "Senda",
    "Forte", "Clave", "NeoGen", "Avance", "Momentum", "Aura", "Orbit", "Zenith",
    "Magna", "Axis", "Innovis", "Inspira", "Quadro", "Fusión", "Vértice", "Linea",
    "Génesis", "Armonía", "Eficientia", "Impacto", "Crescendo", "Globaliza", "Lumen",
    "Propulsa", "Supra", "Evoluciona", "Aria", "Progreso", "Infinito", "Optimus",
    "Omega", "Alpha", "Beta", "Gamma", "Delta", "Sigma", "Theta",

    # Digitales (40+)
    "Pixel", "Digital", "Tech", "Cloud", "Quantum", "Byte", "Core", "Smart",
    "Hyper", "Sync", "Net", "Data", "Omni", "Grid", "Cyber", "Digi", "Ultra",
    "Opti", "Flow", "Pulse", "Spark", "Matrix", "Verse", "Meta", "Crypto",
    "Blockchain", "AI", "Neural", "Logic", "Binary", "Code", "Algo", "Nano",
    "Macro", "Micro", "Mega", "Giga", "Tera", "Quantum", "Photon",

    # Comerciales/Industriales (60+)
    "Crafters", "Forge", "Nest", "Track", "Vault", "Edge", "Connect", "Logic",
    "Tornillo", "Ferretería", "Proyecto", "Martillo", "Mayorista", "Stock",
    "Distribuidora", "Macro", "Compra", "Casa", "Almacén", "Depósito",
    "Comercial", "Industrial", "Fábrica", "Manufactura", "Productora", "Ensambladora",
    "Importadora", "Exportadora", "Trading", "Market", "Mercado", "Tienda",
    "Bodega", "Abastecedora", "Proveedora", "Suministros", "Repuestos", "Autopartes",
    "Maquinaria", "Equipos", "Herramientas", "Materiales", "Insumos", "Productos",
    "Acabados", "Revestimientos", "Pisos", "Techos", "Ventanas", "Puertas",
    "Sanitarios", "Grifería", "Electricidad", "Iluminación", "Cables", "Tuberías",

    # Hoteles (30+)
    "Hotel", "Hospedaje", "Posada", "Resort", "Suites", "Inn", "Lodge", "Palace",
    "Grand", "Premium", "Plaza", "Royal", "Continental", "Imperial", "Boutique",
    "Residencial", "Apart", "Hostal", "Albergue", "Casa de Huéspedes", "B&B",
    "Ecolodge", "Glamping", "Hacienda", "Refugio", "Paraíso", "Oasis", "Mirador",
    "Vista", "Panorama",

    # Servicios Mineros (25+)
    "Minera", "Extractora", "Yacimientos", "Recursos", "Exploraciones", "Minerales",
    "Aurifer", "Cuprífer", "Polimetálica", "Canteras", "Petróleos", "Hidrocarburos",
    "Geológica", "Prospección", "Perforaciones", "Voladura", "Procesadora",
    "Refinería", "Fundición", "Concentradora", "Lixiviación", "Flotación",
    "Amalgama", "Metalúrgica", "Siderúrgica",

    # Alimentos y Bebidas (30+)
    "Alimentos", "Bebidas", "Panificadora", "Pastelería", "Repostería", "Panadería",
    "Lácteos", "Quesería", "Yogurt", "Embutidos", "Carnes", "Pescadería",
    "Mariscos", "Frutas", "Verduras", "Granos", "Cereales", "Harinas",
    "Aceites", "Conservas", "Enlatados", "Congelados", "Refrigerados", "Frescos",
    "Orgánicos", "Naturales", "Saludables", "Gourmet", "Delicatessen", "Catering",

    # Servicios Generales (20+)
    "Servicios", "Consultoría", "Asesoría", "Soluciones", "Grupo", "Corporación",
    "Asociados", "Alianza", "Consorcio", "Integra", "Multi", "Omni", "Total",
    "Integral", "Completa", "Global", "Universal", "Continental", "Internacional",
    "Transregional"
]

SUFIJOS_EMPRESA = [
    # Corporativos (40+)
    " Solutions", " Group", " Global", " Consulting", " Innovación", " Ventures",
    " Creativo", " Empresarial", " Proyectos", " Partners", " Capital", " Corporativo",
    " Hub", " Business", " Ideas", " Dynamics", " Corp", " Labs", " Studio", " Works",
    " Holdings", " Retail", " Services", " Logistics", " Enterprises", " Industries",
    " International", " Worldwide", " Alliance", " Associates", " Consortium",
    " Federation", " Network", " Coalition", " Union", " Syndicate", " Circle",
    " Cluster", " Collective", " Cooperative",

    # Alimentación (15+)
    " Foods", " Beverages", " Alimentos", " Catering", " Gastronómica",
    " Nutrition", " Organic", " Natural", " Fresh", " Gourmet", " Delicatessen",
    " Sabor", " Cocina", " Chef", " Bistro",

    # Construcción (20+)
    " Construcciones", " Materiales", " Ferretería", " Distribución", " Suministros",
    " Acabados", " Infraestructura", " Proyectos", " Inmobiliaria", " Desarrollos",
    " Edificaciones", " Obras", " Contratistas", " Arquitectura", " Ingeniería",
    " Estructuras", " Cimentaciones", " Pavimentos", " Instalaciones", " Reformas",

    # Tech (25+)
    " Digital", " Tech", " Cloud", " Analytics", " Data", " Systems", " Software",
    " Hardware", " Networks", " Security", " Intelligence", " Automation",
    " Robotics", " IoT", " AI", " Machine Learning", " Blockchain", " Crypto",
    " Apps", " Web", " Mobile", " E-commerce", " Fintech", " EdTech", " HealthTech",

    # General (20+)
    " Industrial", " Comercial", " Trading", " Import", " Export", " Mayorista",
    " Minorista", " Distribuidora", " Proveedora", " Intermediaria", " Broker",
    " Agente", " Representante", " Franquicia", " Cadena", " Sucursales",
    " Outlets", " Showroom", " Boutique", " Store",

    # Turismo/Hotelería (15+)
    " Hoteles", " Turismo", " Hospitalidad", " Resorts", " Lodging",
    " Travel", " Tours", " Viajes", " Expediciones", " Aventuras",
    " Ecoturismo", " Destinos", " Vacaciones", " Excursiones", " Rutas",

    # Minería (15+)
    " Mining", " Resources", " Exploration", " del Perú", " Andina", " del Norte",
    " Extractiva", " Yacimientos", " Minas", " Canteras", " Minerales",
    " Metalurgia", " Fundición", " Refinería", " Procesamiento",

    # Servicios Profesionales (20+)
    " Abogados", " Legales", " Auditores", " Contadores", " Financiera",
    " Inversiones", " Seguros", " Corredores", " Asesoría", " Consultoría",
    " Capacitación", " Training", " Academia", " Instituto", " Centro de Estudios",
    " Investigación", " Desarrollo", " I+D", " Think Tank", " Lab",

    # Salud (15+)
    " Salud", " Médica", " Clínica", " Hospital", " Laboratorio",
    " Farmacia", " Medicamentos", " Diagnóstico", " Terapias", " Rehabilitación",
    " Wellness", " Spa", " Estética", " Nutrición", " Fitness"
]

GEOGRAFICOS = [
    # Regiones amplias
    "Latam", "Iberia", "Andes", "Pacífico", "Cono Sur", "Caribe", "Europa",
    "Andina", "Mediterránea", "Metropolitana", "del Sur", "del Norte", "Central",
    "Oriental", "Occidental", "Internacional",

    # Perú - Departamentos
    "Perú", "Lima", "Arequipa", "Cusco", "Trujillo", "Cajamarca", "Piura",
    "Puno", "Ica", "Tacna", "Huancayo", "Ayacucho", "Huaraz", "Chiclayo",
    "Iquitos", "Huánuco", "Pucallpa", "Moquegua", "Tumbes", "Amazonas",
    "Ucayali", "Loreto", "Madre de Dios", "San Martín", "Junín", "Ancash",

    # Específicos
    "del Callao", "de la Libertad", "de Lambayeque", "de Áncash",
    "de Apurímac", "de Huancavelica", "de Pasco",

    # Zonas geográficas
    "del Valle", "de la Costa", "de la Sierra", "de la Selva",
    "Amazónica", "Altiplánica", "Costera", "Serrana"
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
    # Lima - Principales avenidas
    "Av. Javier Prado", "Av. Arequipa", "Av. Universitaria", "Av. La Marina",
    "Av. Venezuela", "Av. Abancay", "Av. Petit Thouars", "Av. Brasil",
    "Av. Benavides", "Av. Larco", "Av. José Pardo", "Av. Salaverry",
    "Av. Comandante Espinar", "Av. Angamos", "Av. República de Panama",
    "Av. Aramburú", "Av. Conquistadores", "Av. Camino Real", "Av. El Derby",
    "Av. Paseo de la República", "Av. Alfonso Ugarte", "Av. Colonial",
    "Av. Túpac Amaru", "Av. Aviación", "Av. Tomás Marsano", "Av. Primavera",
    "Av. Separadora Industrial", "Av. Los Próceres", "Av. Guardia Civil",
    "Av. La Molina", "Av. El Polo", "Av. Santa Cruz", "Av. San Felipe",
    "Av. Canadá", "Av. Del Ejército", "Av. Circunvalación", "Av. Metropolitana",
    "Av. Universitaria", "Av. Oscar R. Benavides", "Av. Óscar Benavides",

    # Lima - Calles y jirones
    "Calle Las Begonias", "Calle Schell", "Calle Tarata", "Calle Berlin",
    "Calle Los Pinos", "Calle Alcanfores", "Calle Martín Olaya",
    "Jr. de la Unión", "Jr. Carabaya", "Jr. Lampa", "Jr. Ucayali",
    "Jr. Ancash", "Jr. Huallaga", "Jr. Cusco", "Jr. Quilca",
    "Malecón Cisneros", "Malecón de la Reserva", "Malecón 28 de Julio",

    # Arequipa
    "Av. El Sol", "Av. Ejército", "Av. Cayma", "Av. Goyeneche",
    "Av. Parra", "Calle Mercaderes", "Calle Santa Catalina",

    # Cusco
    "Av. La Cultura", "Av. El Sol", "Av. Garcilaso", "Av. Los Incas",
    "Calle Triunfo", "Calle Plateros", "Plaza de Armas",

    # Trujillo
    "Av. España", "Av. América", "Av. Larco", "Av. Mansiche",

    # Chiclayo
    "Av. Balta", "Av. Bolognesi", "Av. Luis Gonzáles",

    # Piura
    "Av. Grau", "Av. Sánchez Cerro", "Av. Loreto",

    # General
    "Av. Fitzcarrald", "Av. Bolognesi", "Av. 28 de Julio", "Av. 2 de Mayo",
    "Av. Progreso", "Av. Industrial", "Av. Los Héroes", "Av. Pachacútec"
]

CALLES_LATAM = [
    # Colombia
    "Carrera 7", "Carrera 13", "Carrera 15", "Calle 72", "Calle 100",

    # México
    "Av. Reforma", "Av. Insurgentes", "Paseo de la Reforma",

    # Chile
    "Av. Apoquindo", "Av. Providencia", "Av. Vitacura", "Av. Las Condes",

    # Argentina
    "Av. 9 de Julio", "Av. Santa Fe", "Av. Corrientes", "Av. Córdoba",

    # Ecuador
    "Av. Amazonas", "Av. 6 de Diciembre", "Av. 10 de Agosto",

    # Uruguay
    "Av. 18 de Julio", "Rambla",

    # España
    "Gran Vía", "Passeig de Gràcia", "Calle Larios", "Av. Colón",

    # Brasil
    "Av. Paulista", "Rua das Flores", "Av. Atlântica"
]

BARRIOS_LIMA = [
    # Lima Norte
    "Independencia", "Los Olivos", "San Martín de Porres", "Comas", "Puente Piedra",
    "Carabayllo", "Santa Rosa", "Ancón",

    # Lima Centro
    "Cercado de Lima", "Breña", "La Victoria", "Rímac", "San Luis",

    # Lima Este
    "Ate", "Santa Anita", "El Agustino", "San Juan de Lurigancho",
    "Lurigancho-Chosica", "Chaclacayo", "La Molina", "Cieneguilla",

    # Lima Sur
    "Chorrillos", "Villa El Salvador", "Villa María del Triunfo",
    "San Juan de Miraflores", "Lurín", "Pachacámac", "Punta Hermosa",
    "Punta Negra", "San Bartolo", "Santa María del Mar",

    # Lima Moderna
    "Miraflores", "San Isidro", "San Borja", "Surco", "La Molina",
    "Lince", "Jesús María", "Magdalena", "Pueblo Libre", "San Miguel",
    "Barranco",

    # Callao
    "Callao", "Bellavista", "La Perla", "La Punta", "Carmen de la Legua",
    "Ventanilla"
]

BARRIOS_LATAM = [
    # Bogotá
    "Chapinero", "Usaquén", "Suba", "Engativá", "Kennedy",

    # CDMX
    "Polanco", "Condesa", "Roma", "Coyoacán", "Santa Fe",

    # Santiago
    "Las Condes", "Providencia", "Vitacura", "Lo Barnechea", "Ñuñoa",

    # Buenos Aires
    "Palermo", "Recoleta", "Belgrano", "San Telmo", "Puerto Madero",
    "Balvanera", "Monserrat", "Retiro", "Vicente López",

    # Quito
    "La Mariscal", "Carolina", "González Suárez",

    # Montevideo
    "Pocitos", "Punta Carretas", "Centro",

    # España
    "Centro", "Salamanca", "Chamberí", "Eixample"
]

CIUDADES_PERU = [
    # Costa
    "Lima", "Callao", "Trujillo", "Chiclayo", "Piura", "Ica", "Tacna",
    "Tumbes", "Chimbote", "Sullana", "Pisco", "Chincha", "Paita",

    # Sierra
    "Arequipa", "Cusco", "Huancayo", "Cajamarca", "Ayacucho", "Huaraz",
    "Puno", "Abancay", "Huánuco", "Cerro de Pasco", "Huancavelica",
    "Tarma", "Jauja",

    # Selva
    "Iquitos", "Pucallpa", "Tarapoto", "Yurimaguas", "Puerto Maldonado",
    "Tingo María", "Moyobamba"
]

CIUDADES_LATAM = [
    # Sudamérica
    "Bogotá", "Santiago", "Quito", "Buenos Aires", "Montevideo",
    "São Paulo", "Río de Janeiro", "Caracas", "La Paz", "Asunción",

    # México
    "CDMX", "Guadalajara", "Monterrey", "Puebla", "Tijuana",

    # España
    "Madrid", "Barcelona", "Valencia", "Sevilla", "Málaga",

    # Otros
    "Córdoba", "Mendoza", "Rosario", "Medellín", "Cali", "Guayaquil"
]

# ============================================================================
# DATOS DE PERSONAS (NOMBRES Y APELLIDOS PERUANOS)
# ============================================================================

NOMBRES_MASCULINOS = [
    "Carlos", "José", "Juan", "Luis", "Miguel", "Jorge", "Fernando", "Ricardo",
    "Roberto", "Pedro", "Francisco", "Andrés", "Daniel", "Javier", "Raúl",
    "Manuel", "Alberto", "Eduardo", "Alejandro", "Antonio", "Diego", "Pablo",
    "César", "Oscar", "Arturo", "Enrique", "Rafael", "Víctor", "Mario",
    "Sergio", "Julio", "Gonzalo", "Gustavo", "Hernán", "Felipe", "Marco",
    "David", "Samuel", "Gabriel", "Leonardo", "Sebastián", "Mateo", "Lucas",
    "Nicolás", "Joaquín", "Emilio", "Adrián", "Martín", "Hugo", "Iván"
]

NOMBRES_FEMENINOS = [
    "María", "Ana", "Carmen", "Rosa", "Teresa", "Patricia", "Isabel", "Elena",
    "Julia", "Laura", "Andrea", "Lucía", "Gabriela", "Daniela", "Carolina",
    "Valentina", "Sofía", "Isabella", "Camila", "Natalia", "Paula", "Diana",
    "Sandra", "Mónica", "Cecilia", "Beatriz", "Susana", "Claudia", "Verónica",
    "Alejandra", "Marcela", "Silvia", "Adriana", "Rocío", "Pilar", "Cristina",
    "Lorena", "Mercedes", "Raquel", "Gloria", "Yolanda", "Mariana", "Fernanda",
    "Victoria", "Catalina", "Angélica", "Blanca", "Eugenia", "Norma", "Elsa"
]

APELLIDOS_PERUANOS = [
    # Muy comunes
    "García", "Rodríguez", "López", "Martínez", "González", "Pérez", "Sánchez",
    "Ramírez", "Torres", "Flores", "Rivera", "Gómez", "Díaz", "Cruz", "Morales",
    "Reyes", "Ramos", "Gutiérrez", "Ortiz", "Mendoza", "Chávez", "Ruiz",
    "Hernández", "Castillo", "Vega", "Romero", "Medina", "Jiménez", "Guerrero",
    "Castro", "Vargas", "Rojas", "Aguilar", "Paredes", "Silva", "Quispe",

    # Apellidos andinos comunes
    "Quispe", "Huamán", "Mamani", "Condori", "Ccori", "Yupanqui", "Puma",
    "Ttito", "Apaza", "Calisaya", "Chambi", "Choque", "Inca", "Pari",

    # Apellidos costeños
    "Távara", "Zapata", "Valencia", "Benites", "Chirinos", "Sandoval",
    "Figueroa", "Montes", "Farfán", "Cordero", "Córdova", "Arce",

    # Otros comunes
    "Fernández", "Alvarez", "Delgado", "Herrera", "Espinoza", "Salazar",
    "Valdez", "Prado", "Ibarra", "Carrasco", "Fuentes", "Navarro", "Cabrera",
    "Maldonado", "Miranda", "Campos", "Vera", "Contreras", "Rosas", "Luna",
    "Benavides", "Palomino", "Villanueva", "Santos", "Vargas", "Núñez",
    "Mendez", "Cáceres", "Moreno", "Bustamante", "Palacios", "Santana",
    "Velásquez", "Montoya", "Hidalgo", "Zavala", "Alvarado", "Bravo"
]

def generar_nombre_completo(genero=None):
    """
    Genera nombre completo peruano
    genero: 'M' o 'F', si es None elige aleatorio
    """
    if genero is None:
        genero = random.choice(['M', 'F'])

    if genero == 'M':
        nombre = random.choice(NOMBRES_MASCULINOS)
    else:
        nombre = random.choice(NOMBRES_FEMENINOS)

    # 30% tiene segundo nombre
    if random.random() < 0.3:
        if genero == 'M':
            nombre += " " + random.choice(NOMBRES_MASCULINOS)
        else:
            nombre += " " + random.choice(NOMBRES_FEMENINOS)

    # Siempre 2 apellidos
    apellido1 = random.choice(APELLIDOS_PERUANOS)
    apellido2 = random.choice(APELLIDOS_PERUANOS)

    return f"{nombre} {apellido1} {apellido2}"


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
    ("Caramelos de miel natural", "KGM", (7.00, 14.00)),
    ("Chicles en bola colores", "KGM", (6.00, 12.00)),
    ("Chocolate amargo 70%", "KGM", (18.00, 40.00)),
    ("Chocolate blanco", "KGM", (16.00, 38.00)),
    ("Gomitas de ositos", "KGM", (9.00, 22.00)),
    ("Caramelos de mantequilla", "KGM", (8.00, 16.00)),
    ("Piruletas grandes", "NIU", (0.50, 2.00)),
    ("Chicle en tabletas", "NIU", (0.30, 1.00)),
    ("Caramelos de café", "KGM", (7.00, 15.00)),
    ("Alfajores surtidos", "NIU", (2.00, 5.00)),
    ("Obleas rellenas", "KGM", (8.00, 18.00)),
    ("Galletas de chocolate", "KGM", (6.00, 14.00)),
    ("Galletas dulces surtidas", "KGM", (5.00, 12.00)),
    ("Barras energéticas", "NIU", (3.00, 7.00)),
    ("Maní confitado", "KGM", (10.00, 25.00)),
    ("Almendras con chocolate", "KGM", (22.00, 50.00)),
    ("Pasas con chocolate", "KGM", (12.00, 28.00)),
    ("Chupetines sabor frutas", "NIU", (0.40, 1.50)),
    ("Caramelos masticables", "KGM", (7.00, 16.00)),
    ("Chicles en láminas", "NIU", (0.50, 1.50)),
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
    ("Agua con gas", "LTR", (1.50, 3.50)),
    ("Refresco de naranja", "LTR", (2.00, 5.00)),
    ("Refresco de limón", "LTR", (2.00, 5.00)),
    ("Gaseosa sabor manzana", "LTR", (2.00, 5.00)),
    ("Bebida de soya", "LTR", (3.00, 7.00)),
    ("Leche de almendras", "LTR", (5.00, 12.00)),
    ("Leche deslactosada", "LTR", (3.50, 7.50)),
    ("Yogurt bebible", "LTR", (4.00, 9.00)),
    ("Jugo de manzana", "LTR", (3.50, 7.50)),
    ("Jugo de piña", "LTR", (3.50, 7.50)),
    ("Néctar de durazno", "LTR", (3.00, 6.50)),
    ("Néctar de mango", "LTR", (3.00, 6.50)),
    ("Café frío", "LTR", (6.00, 12.00)),
    ("Té verde frío", "LTR", (4.00, 8.00)),
    ("Té negro frío", "LTR", (4.00, 8.00)),
    ("Mate de coca", "LTR", (2.50, 5.50)),
    ("Chicha morada", "LTR", (3.00, 7.00)),
    ("Refresco de maracuyá", "LTR", (3.50, 7.00)),
    ("Agua de coco", "LTR", (5.00, 11.00)),
    ("Smoothie de frutas", "LTR", (6.00, 13.00)),
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
    ("Cerveza negra", "LTR", (4.00, 10.00)),
    ("Cerveza de trigo", "LTR", (5.00, 12.00)),
    ("Cerveza lager", "LTR", (3.00, 8.00)),
    ("Vino rosado", "LTR", (30.00, 95.00)),
    ("Vino espumante", "LTR", (40.00, 150.00)),
    ("Champagne brut", "LTR", (80.00, 300.00)),
    ("Pisco puro", "LTR", (35.00, 90.00)),
    ("Pisco acholado", "LTR", (30.00, 80.00)),
    ("Tequila silver", "LTR", (45.00, 120.00)),
    ("Tequila reposado", "LTR", (55.00, 150.00)),
    ("Cognac VSOP", "LTR", (90.00, 280.00)),
    ("Brandy reserva", "LTR", (40.00, 110.00)),
    ("Licor de café", "LTR", (30.00, 75.00)),
    ("Licor de menta", "LTR", (25.00, 65.00)),
    ("Vermouth rosso", "LTR", (20.00, 55.00)),
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
    ("Cemento blanco", "BG", (18.00, 25.00)),
    ("Cemento gris tipo I", "BG", (21.00, 27.00)),
    ("Arena gruesa", "M3", (40.00, 60.00)),
    ("Piedra chancada 1/2\"", "M3", (55.00, 75.00)),
    ("Piedra chancada 3/4\"", "M3", (52.00, 72.00)),
    ("Cal hidratada", "BG", (10.00, 18.00)),
    ("Ladrillo King Kong 18 huecos", "MIL", (400.00, 600.00)),
    ("Ladrillo pastelero", "MIL", (320.00, 520.00)),
    ("Ladrillo pandereta", "MIL", (280.00, 480.00)),
    ("Adoquines de concreto", "M2", (25.00, 45.00)),
    ("Varilla corrugada 1/2\" x 9m", "NIU", (28.00, 42.00)),
    ("Varilla corrugada 5/8\" x 9m", "NIU", (42.00, 62.00)),
    ("Alambre recocido N°8", "KGM", (4.50, 8.50)),
    ("Alambre recocido N°16", "KGM", (5.00, 9.00)),
    ("Malla electrosoldada 6x6", "M2", (12.00, 22.00)),
    ("Pintura esmalte sintético", "GLI", (40.00, 90.00)),
    ("Pintura óleo mate exterior", "GLI", (45.00, 95.00)),
    ("Imprimante para muros", "GLI", (30.00, 65.00)),
    ("Laca transparente", "GLI", (38.00, 85.00)),
    ("Thinner acrílico", "GLI", (15.00, 30.00)),
    ("Barniz marino", "GLI", (50.00, 120.00)),
    ("Tubo PVC SAP 2\" x 3m", "NIU", (15.00, 28.00)),
    ("Tubo PVC SAP 3\" x 3m", "NIU", (22.00, 38.00)),
    ("Tubo PVC SAP 4\" x 3m", "NIU", (35.00, 55.00)),
    ("Tubo desagüe PVC 2\" x 3m", "NIU", (12.00, 22.00)),
    ("Tubo desagüe PVC 4\" x 3m", "NIU", (28.00, 48.00)),
    ("Codo PVC 90° 2\"", "NIU", (2.50, 5.50)),
    ("Codo PVC 45° 2\"", "NIU", (2.00, 4.50)),
    ("Tee PVC 2\"", "NIU", (3.00, 6.00)),
    ("Cable THW 14 AWG", "MTR", (1.80, 3.50)),
    ("Cable THW 10 AWG", "MTR", (3.00, 6.00)),
    ("Interruptor simple 15A", "NIU", (4.00, 9.00)),
    ("Interruptor doble 15A", "NIU", (6.00, 12.00)),
    ("Tomacorriente doble con tierra", "NIU", (5.00, 11.00)),
    ("Caja octagonal galvanizada", "NIU", (2.50, 5.00)),
    ("Tubo conduit PVC 3/4\" x 3m", "NIU", (7.00, 14.00)),
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
    ("Brocha 1\" cerdas naturales", "NIU", (5.00, 12.00)),
    ("Brocha 3\" cerdas sintéticas", "NIU", (10.00, 20.00)),
    ("Rodillo 4\" espuma", "NIU", (8.00, 16.00)),
    ("Espátula 3\" acero inoxidable", "NIU", (7.00, 14.00)),
    ("Llana dentada 8x8mm", "NIU", (15.00, 30.00)),
    ("Martillo bola 8 oz", "NIU", (18.00, 35.00)),
    ("Martillo goma 12 oz", "NIU", (20.00, 40.00)),
    ("Combo 6 lb", "NIU", (35.00, 65.00)),
    ("Cincel plano 1/2\"", "NIU", (10.00, 20.00)),
    ("Serrucho costilla 16\"", "NIU", (28.00, 55.00)),
    ("Sierra arco ajustable", "NIU", (15.00, 30.00)),
    ("Hoja sierra arco 12\" 24TPI", "NIU", (2.00, 5.00)),
    ("Taladro atornillador inalámbrico", "NIU", (250.00, 480.00)),
    ("Sierra circular 7-1/4\"", "NIU", (280.00, 550.00)),
    ("Lijadora orbital", "NIU", (180.00, 350.00)),
    ("Rotomartillo 26mm SDS-Plus", "NIU", (380.00, 720.00)),
    ("Llave francesa 12\"", "NIU", (22.00, 45.00)),
    ("Llave stillson 14\"", "NIU", (28.00, 55.00)),
    ("Juego llaves mixtas 8 pzas", "JGO", (45.00, 90.00)),
    ("Juego dados 1/2\" 20 pzas", "JGO", (80.00, 160.00)),
    ("Alicate presión 10\"", "NIU", (22.00, 45.00)),
    ("Alicate corte diagonal 8\"", "NIU", (20.00, 40.00)),
    ("Destornillador plano 8\"", "NIU", (7.00, 14.00)),
    ("Juego destornilladores 6 pzas", "JGO", (25.00, 50.00)),
    ("Arco sierra marco ajustable", "NIU", (12.00, 25.00)),
    ("Guantes cuero reforzado", "PAR", (8.00, 16.00)),
    ("Guantes anticorte nivel 5", "PAR", (15.00, 30.00)),
    ("Guantes dieléctricos clase 0", "PAR", (35.00, 70.00)),
    ("Casco con barbiquejo", "NIU", (18.00, 38.00)),
    ("Gafas protección UV", "NIU", (12.00, 25.00)),
    ("Careta facial policarbonato", "NIU", (20.00, 40.00)),
    ("Mascarilla reutilizable filtros", "NIU", (25.00, 50.00)),
    ("Respirador media cara", "NIU", (45.00, 90.00)),
    ("Tapones auditivos espuma", "PAR", (1.00, 3.00)),
    ("Orejeras de seguridad", "NIU", (18.00, 35.00)),
    ("Arnés seguridad 5 puntos", "NIU", (85.00, 170.00)),
    ("Chaleco reflectivo", "NIU", (10.00, 20.00)),
    ("Botas punta acero", "PAR", (60.00, 120.00)),
    ("Cinta métrica 8m", "NIU", (20.00, 40.00)),
    ("Flexómetro 10m", "NIU", (25.00, 50.00)),
    ("Nivel láser autonivelante", "NIU", (180.00, 350.00)),
    ("Escuadra carpintero 12\"", "NIU", (18.00, 35.00)),
]

# Alimentos generales
ALIMENTOS = [
    ("Arroz extra", "KGM", (2.80, 5.50)),
    ("Azúcar blanca", "KGM", (2.50, 4.50)),
    ("Sal de mesa", "KGM", (1.20, 2.50)),
    ("Aceite vegetal", "LTR", (5.00, 11.00)),
    ("Fideos spaghetti", "KGM", (3.00, 6.00)),
    ("Harina de trigo", "KGM", (2.50, 5.00)),
    ("Leche evaporada", "NIU", (3.00, 6.00)),
    ("Atún en conserva", "NIU", (4.50, 9.00)),
    ("Conserva de pescado", "NIU", (4.00, 8.00)),
    ("Menestras variadas", "KGM", (4.00, 8.00)),
    ("Lentejas", "KGM", (4.50, 8.50)),
    ("Frijoles", "KGM", (4.00, 7.50)),
    ("Garbanzo", "KGM", (5.00, 9.00)),
    ("Avena en hojuelas", "KGM", (3.50, 7.00)),
    ("Quinua", "KGM", (12.00, 22.00)),
    ("Kiwicha", "KGM", (10.00, 18.00)),
    ("Café molido", "KGM", (15.00, 35.00)),
    ("Té en bolsitas", "NIU", (5.00, 12.00)),
    ("Mantequilla", "KGM", (12.00, 25.00)),
    ("Margarina", "KGM", (6.00, 13.00)),
    ("Mayonesa", "KGM", (8.00, 16.00)),
    ("Ketchup", "KGM", (6.00, 12.00)),
    ("Mostaza", "KGM", (5.00, 10.00)),
    ("Vinagre", "LTR", (3.00, 6.00)),
    ("Salsa de tomate", "KGM", (4.00, 9.00)),
    ("Mermelada", "KGM", (7.00, 15.00)),
    ("Miel de abeja", "KGM", (18.00, 38.00)),
    ("Galletas saladas", "KGM", (4.00, 9.00)),
    ("Pan molde", "NIU", (4.50, 9.00)),
    ("Huevos", "NIU", (0.50, 1.20)),
]

# Combustibles
COMBUSTIBLES = [
    ("Gasolina 90 octanos", "GLI", (13.50, 16.50)),
    ("Gasolina 95 octanos", "GLI", (15.00, 18.00)),
    ("Gasolina 97 octanos", "GLI", (16.00, 19.50)),
    ("Diésel B5", "GLI", (13.00, 16.00)),
    ("Diésel B5-S50", "GLI", (13.50, 16.50)),
    ("GLP (Gas Licuado de Petróleo)", "GLI", (3.00, 5.00)),
    ("GNV (Gas Natural Vehicular)", "M3", (1.50, 2.50)),
    ("Aceite motor sintético 5W-30", "GLI", (35.00, 80.00)),
    ("Aceite motor semi-sintético 10W-40", "GLI", (25.00, 60.00)),
    ("Aceite motor mineral 20W-50", "GLI", (20.00, 45.00)),
    ("Aceite transmisión ATF", "LTR", (18.00, 40.00)),
    ("Aceite hidráulico ISO 68", "GLI", (22.00, 50.00)),
    ("Grasa multiuso", "KGM", (8.00, 18.00)),
    ("Refrigerante motor", "GLI", (15.00, 35.00)),
    ("Líquido de frenos DOT 3", "LTR", (12.00, 25.00)),
]

# Servicios de hotel
SERVICIOS_HOTEL = [
    ("ALOJAMIENTO habitación estándar", "NIU", (80.00, 250.00)),
    ("ALOJAMIENTO suite", "NIU", (200.00, 600.00)),
    ("ALOJAMIENTO habitación doble", "NIU", (120.00, 350.00)),
    ("ALIMENTACIÓN desayuno buffet", "NIU", (25.00, 60.00)),
    ("ALIMENTACIÓN almuerzo ejecutivo", "NIU", (35.00, 80.00)),
    ("ALIMENTACIÓN cena", "NIU", (40.00, 120.00)),
    ("ALIMENTACIÓN room service", "NIU", (30.00, 100.00)),
    ("LAVANDERIA servicio express", "KGM", (15.00, 35.00)),
    ("LAVANDERIA servicio estándar", "KGM", (10.00, 25.00)),
    ("TELEFONO llamadas nacionales", "MIN", (0.50, 2.00)),
    ("TELEFONO llamadas internacionales", "MIN", (2.00, 8.00)),
    ("MINIBAR consumo", "NIU", (5.00, 35.00)),
    ("MINIBAR bebidas", "NIU", (8.00, 25.00)),
    ("MINIBAR snacks", "NIU", (4.00, 15.00)),
    ("WIFI premium 24h", "NIU", (15.00, 35.00)),
    ("ESTACIONAMIENTO", "NIU", (15.00, 40.00)),
    ("TRASLADO aeropuerto", "NIU", (30.00, 80.00)),
    ("SPA masaje", "HOR", (80.00, 200.00)),
    ("GYM acceso", "NIU", (10.00, 30.00)),
    ("PISCINA toallas", "NIU", (5.00, 15.00)),
]

# Servicios mineros
SERVICIOS_MINEROS = [
    ("PERFORACION diamantina", "MTR", (120.00, 280.00)),
    ("PERFORACION rotativa", "MTR", (80.00, 180.00)),
    ("VOLADURA controlada", "M3", (15.00, 35.00)),
    ("TRANSPORTE mineral", "TM", (8.00, 20.00)),
    ("CARGUIO con excavadora", "HOR", (180.00, 350.00)),
    ("ACARREO con camión 30T", "HOR", (150.00, 300.00)),
    ("SOSTENIMIENTO con pernos", "MTR", (25.00, 55.00)),
    ("SOSTENIMIENTO con shotcrete", "M3", (180.00, 380.00)),
    ("VENTILACION instalación ductos", "MTR", (45.00, 95.00)),
    ("DESAGUE bombeo", "HOR", (80.00, 160.00)),
    ("TOPOGRAFIA levantamiento", "HOR", (90.00, 180.00)),
    ("GEOLOGIA muestreo", "NIU", (25.00, 60.00)),
    ("ENSAYES metalúrgicos", "NIU", (150.00, 400.00)),
    ("MANTENIMIENTO equipo pesado", "HOR", (120.00, 280.00)),
    ("CHANCADO primario", "TM", (3.50, 8.00)),
    ("MOLIENDA", "TM", (5.00, 12.00)),
    ("FLOTACION", "TM", (8.00, 18.00)),
    ("LIXIVIACION", "TM", (6.00, 14.00)),
]

# Seguridad
SEGURIDAD = [
    ("Cámara CCTV 1080p", "NIU", (180.00, 450.00)),
    ("Cámara IP 4MP", "NIU", (250.00, 600.00)),
    ("DVR 8 canales", "NIU", (380.00, 850.00)),
    ("NVR 16 canales", "NIU", (550.00, 1200.00)),
    ("Disco duro vigilancia 2TB", "NIU", (280.00, 550.00)),
    ("Cable coaxial RG59", "MTR", (1.50, 3.50)),
    ("Cable UTP Cat6", "MTR", (1.20, 2.80)),
    ("Fuente poder 12V 5A", "NIU", (35.00, 75.00)),
    ("Alarma residencial inalámbrica", "NIU", (250.00, 600.00)),
    ("Sensor movimiento PIR", "NIU", (25.00, 60.00)),
    ("Sensor magnético puerta", "NIU", (15.00, 35.00)),
    ("Sirena exterior 120dB", "NIU", (45.00, 95.00)),
    ("Panel control alarma", "NIU", (180.00, 450.00)),
    ("Cerradura electromagnética", "NIU", (150.00, 350.00)),
    ("Control acceso biométrico", "NIU", (550.00, 1300.00)),
    ("Barrera vehicular", "NIU", (1800.00, 3500.00)),
    ("Guardianía 12 horas", "HOR", (15.00, 35.00)),
    ("Monitoreo 24/7 mensual", "MES", (180.00, 450.00)),
]

# Electrónicos
ELECTRONICOS = [
    ("Notebook Intel Core i5", "NIU", (1800.00, 3500.00)),
    ("Notebook Intel Core i7", "NIU", (2800.00, 5500.00)),
    ("PC escritorio completa", "NIU", (1500.00, 3200.00)),
    ("Monitor LED 24\"", "NIU", (450.00, 950.00)),
    ("Monitor LED 27\"", "NIU", (650.00, 1400.00)),
    ("Teclado mecánico", "NIU", (180.00, 450.00)),
    ("Mouse inalámbrico", "NIU", (35.00, 85.00)),
    ("Impresora multifuncional", "NIU", (380.00, 850.00)),
    ("Impresora láser", "NIU", (550.00, 1200.00)),
    ("Scanner documentos", "NIU", (280.00, 650.00)),
    ("Tablet 10\" Android", "NIU", (450.00, 1100.00)),
    ("Smartphone gama media", "NIU", (550.00, 1300.00)),
    ("Smartphone gama alta", "NIU", (1800.00, 4500.00)),
    ("Auriculares Bluetooth", "NIU", (80.00, 250.00)),
    ("Parlante portátil", "NIU", (120.00, 350.00)),
    ("Cargador rápido USB-C", "NIU", (35.00, 85.00)),
    ("Powerbank 10000mAh", "NIU", (55.00, 130.00)),
    ("Router Wi-Fi 6", "NIU", (180.00, 450.00)),
    ("Switch 24 puertos", "NIU", (550.00, 1300.00)),
    ("Proyector Full HD", "NIU", (1200.00, 2800.00)),
]

# Limpieza
LIMPIEZA = [
    ("Detergente líquido", "LTR", (8.00, 18.00)),
    ("Detergente en polvo", "KGM", (6.00, 14.00)),
    ("Jabón líquido manos", "LTR", (5.00, 12.00)),
    ("Shampoo", "LTR", (10.00, 25.00)),
    ("Acondicionador", "LTR", (12.00, 28.00)),
    ("Lejía concentrada", "LTR", (3.00, 7.00)),
    ("Desinfectante pisos", "LTR", (6.00, 14.00)),
    ("Limpia vidrios", "LTR", (5.00, 12.00)),
    ("Limpia baños", "LTR", (7.00, 16.00)),
    ("Suavizante ropa", "LTR", (8.00, 18.00)),
    ("Quitamanchas", "LTR", (10.00, 22.00)),
    ("Desengrasante industrial", "LTR", (12.00, 28.00)),
    ("Cera para pisos", "LTR", (15.00, 35.00)),
    ("Lustrador muebles", "LTR", (10.00, 24.00)),
    ("Ambientador spray", "NIU", (6.00, 14.00)),
    ("Escoba cerdas duras", "NIU", (12.00, 25.00)),
    ("Trapeador microfibra", "NIU", (15.00, 32.00)),
    ("Recogedor metálico", "NIU", (8.00, 18.00)),
    ("Balde plástico 20L", "NIU", (10.00, 22.00)),
    ("Guantes limpieza", "PAR", (3.00, 8.00)),
    ("Paños microfibra", "NIU", (5.00, 12.00)),
    ("Esponja multiuso", "NIU", (2.00, 5.00)),
    ("Bolsas basura 50L", "PKT", (8.00, 18.00)),
    ("Papel higiénico 4 rollos", "PKT", (5.00, 12.00)),
    ("Papel toalla rollo", "NIU", (3.00, 7.00)),
]

# Agrupar por categoría para fácil acceso
ITEMS_POR_CATEGORIA = {
    'caramelos': CARAMELOS,
    'bebidas_no_alc': BEBIDAS_NO_ALC,
    'bebidas_alc': BEBIDAS_ALC,
    'construccion': MATERIALES_CONSTRUCCION,
    'herramientas': HERRAMIENTAS_EPP,
    'alimentos': ALIMENTOS,
    'combustibles': COMBUSTIBLES,
    'servicios_hotel': SERVICIOS_HOTEL,
    'servicios_mineros': SERVICIOS_MINEROS,
    'seguridad': SEGURIDAD,
    'electronicos': ELECTRONICOS,
    'limpieza': LIMPIEZA,
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


def generar_item_aleatorio(categoria=None):
    """Genera un item aleatorio de cualquier categoría o de una específica"""
    if categoria and categoria in ITEMS_POR_CATEGORIA:
        items = ITEMS_POR_CATEGORIA[categoria]
    else:
        # Todas las categorías juntas
        items = []
        for cat_items in ITEMS_POR_CATEGORIA.values():
            items.extend(cat_items)

    item, unidad, rango = random.choice(items)
    return generar_item_con_variantes(item), unidad, rango


if __name__ == "__main__":
    # Pruebas
    print("=" * 70)
    print("PRUEBAS DE DICCIONARIOS MEJORADOS".center(70))
    print("=" * 70)

    print("\n🏢 EMPRESAS GENERALES (5 ejemplos):")
    for _ in range(5):
        print(f"  • {generar_nombre_empresa('general')}")

    print("\n🏨 HOTELES (5 ejemplos):")
    for _ in range(5):
        print(f"  • {generar_nombre_empresa('hotel')}")

    print("\n🛡️ ASEGURADORAS (5 ejemplos):")
    for _ in range(5):
        print(f"  • {generar_nombre_empresa('seguro')}")

    print("\n📍 DIRECCIONES PERÚ (5 ejemplos):")
    for _ in range(5):
        print(f"  • {generar_direccion('Peru')}")

    print("\n👤 NOMBRES COMPLETOS (5 ejemplos):")
    for _ in range(5):
        print(f"  • {generar_nombre_completo()}")

    print("\n" + "=" * 70)
    print("ITEMS POR CATEGORÍA".center(70))
    print("=" * 70)

    # Mostrar estadísticas de cada categoría
    total_items = 0
    for cat_name, items_list in ITEMS_POR_CATEGORIA.items():
        count = len(items_list)
        total_items += count
        print(f"\n📦 {cat_name.upper().replace('_', ' ')}: {count} items")
        # Mostrar 3 ejemplos con variantes
        for i in range(min(3, count)):
            item, unidad, rango = items_list[i]
            item_variante = generar_item_con_variantes(item)
            print(f"  • {item_variante} ({unidad}) - S/{rango[0]:.2f}-{rango[1]:.2f}")

    print("\n" + "=" * 70)
    print(f"TOTAL DE ITEMS: {total_items}".center(70))
    print("=" * 70)

    # Mostrar mejora vs. versión anterior
    print("\n📊 MEJORA RESPECTO A VERSIÓN ANTERIOR:")
    print(f"  • Empresas: De ~50 fijas → ~500,000+ combinaciones")
    print(f"  • Direcciones: De ~500 → ~100,000+ combinaciones")
    print(f"  • Items: De ~400 → {total_items}+ items base")
    print(f"  • Con variantes: {total_items} × 2-3 variantes → ~{total_items * 2}+ items únicos")
    print("\n✅ Sistema de diccionarios listo para generación masiva de facturas")
