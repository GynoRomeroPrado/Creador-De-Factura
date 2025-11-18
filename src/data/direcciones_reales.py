#!/usr/bin/env python3
"""
Direcciones Reales por Distrito de Lima
========================================

Base de datos de direcciones auténticas organizadas por 25 distritos de Lima.
Incluye calles reales, códigos postales, zonas comerciales y referencias.

Uso:
    from src.data.direcciones_reales import generar_direccion_realista

    direccion = generar_direccion_realista()
    direccion_miraflores = generar_direccion_realista(distrito='miraflores')
"""

import random
from typing import Dict, List, Optional, Tuple


# Base de datos de direcciones por distrito
DIRECCIONES_POR_DISTRITO = {
    'miraflores': {
        'peso': 12,  # Peso para selección ponderada
        'codigo_postal': '15074',
        'calles': [
            ('Av. Larco', 100, 1500),
            ('Av. Pardo', 100, 800),
            ('Av. Benavides', 200, 2000),
            ('Av. Arequipa', 2500, 5000),
            ('Calle Schell', 100, 600),
            ('Calle Shell', 100, 500),
            ('Av. Diagonal', 100, 800),
            ('Av. José Pardo', 100, 900),
            ('Calle Alcanfores', 100, 700),
            ('Av. Comandante Espinar', 100, 900),
            ('Calle Recavarren', 100, 500),
            ('Jr. De la Unión', 700, 1100),
            ('Av. La Mar', 100, 1200),
            ('Calle Porta', 100, 400),
            ('Av. Reducto', 100, 1500),
        ],
        'referencias': [
            'Parque Kennedy',
            'Larcomar',
            'Óvalo Gutiérrez',
            'Huaca Pucllana',
            'Parque del Amor',
        ],
        'tipos_establecimiento': {
            'oficina': 0.35,
            'departamento': 0.25,
            'local_comercial': 0.30,
            'casa': 0.10,
        }
    },

    'san_isidro': {
        'peso': 10,
        'codigo_postal': '15073',
        'calles': [
            ('Av. Javier Prado Este', 100, 1000),
            ('Av. República de Panamá', 3000, 6000),
            ('Av. Conquistadores', 100, 1500),
            ('Av. Camino Real', 100, 1500),
            ('Calle Las Begonias', 100, 800),
            ('Av. Paseo de la República', 3000, 5500),
            ('Calle Los Eucaliptos', 100, 700),
            ('Av. Dos de Mayo', 100, 2000),
            ('Calle Las Camelias', 100, 900),
            ('Av. Arequipa', 2000, 4500),
            ('Calle Rivera Navarrete', 100, 800),
            ('Av. Central', 100, 600),
            ('Calle Choquehuanca', 100, 700),
            ('Av. Salaverry', 2000, 3500),
        ],
        'referencias': [
            'Centro Empresarial Real',
            'Golf Los Incas',
            'Bosque El Olivar',
            'Country Club Lima Hotel',
            'Municipalidad de San Isidro',
        ],
        'tipos_establecimiento': {
            'oficina': 0.50,
            'departamento': 0.20,
            'local_comercial': 0.25,
            'casa': 0.05,
        }
    },

    'surco': {
        'peso': 11,
        'codigo_postal': '15023',
        'calles': [
            ('Av. Primavera', 100, 2000),
            ('Av. Tomás Marsano', 1000, 3500),
            ('Av. Benavides', 2500, 5500),
            ('Av. El Derby', 100, 500),
            ('Av. Caminos del Inca', 100, 1500),
            ('Av. Santiago de Surco', 1000, 4500),
            ('Calle Monte Bello', 100, 400),
            ('Av. Velasco Astete', 100, 2500),
            ('Av. Javier Prado Este', 3000, 6000),
            ('Av. Angamos Este', 1000, 3000),
            ('Calle Los Precursores', 100, 600),
            ('Av. Aviación', 2000, 4500),
        ],
        'referencias': [
            'Jockey Plaza',
            'Plaza Molitalia',
            'CC Chacarilla',
            'Municipalidad de Surco',
            'Universidad de Lima',
        ],
        'tipos_establecimiento': {
            'oficina': 0.30,
            'departamento': 0.35,
            'local_comercial': 0.25,
            'casa': 0.10,
        }
    },

    'san_borja': {
        'peso': 8,
        'codigo_postal': '15036',
        'calles': [
            ('Av. Aviación', 1000, 3500),
            ('Av. Javier Prado Este', 1500, 2800),
            ('Av. San Luis', 1000, 2800),
            ('Av. Guardia Civil', 100, 1500),
            ('Av. Del Aire', 100, 2000),
            ('Av. Angamos Este', 1500, 2500),
            ('Av. San Borja Norte', 100, 1500),
            ('Av. Boulevard', 100, 500),
            ('Calle Las Artes', 100, 600),
            ('Av. Primavera', 100, 500),
        ],
        'referencias': [
            'Pentagonito',
            'Museo de la Nación',
            'Biblioteca Nacional',
            'San Borja Plaza',
            'Parque de las Letras',
        ],
        'tipos_establecimiento': {
            'oficina': 0.35,
            'departamento': 0.40,
            'local_comercial': 0.20,
            'casa': 0.05,
        }
    },

    'la_molina': {
        'peso': 9,
        'codigo_postal': '15024',
        'calles': [
            ('Av. La Molina', 100, 3000),
            ('Av. Raúl Ferrero', 100, 2500),
            ('Av. Javier Prado Este', 5000, 8500),
            ('Av. La Universidad', 100, 2000),
            ('Av. Los Fresnos', 100, 1500),
            ('Av. La Fontana', 100, 1200),
            ('Av. Separadora Industrial', 100, 2000),
            ('Calle Los Ingenieros', 100, 500),
            ('Av. El Corregidor', 100, 1500),
        ],
        'referencias': [
            'Universidad Agraria',
            'Megaplaza',
            'Molina Plaza',
            'Camacho',
            'Municipalidad La Molina',
        ],
        'tipos_establecimiento': {
            'oficina': 0.25,
            'departamento': 0.30,
            'local_comercial': 0.30,
            'casa': 0.15,
        }
    },

    'lima_centro': {
        'peso': 14,
        'codigo_postal': '15001',
        'calles': [
            ('Jr. De la Unión', 100, 900),
            ('Av. Abancay', 100, 1500),
            ('Jr. Carabaya', 100, 800),
            ('Jr. Lampa', 100, 700),
            ('Av. Nicolás de Piérola', 100, 1200),
            ('Jr. Ucayali', 100, 900),
            ('Av. Tacna', 100, 1500),
            ('Jr. Azángaro', 100, 800),
            ('Av. Emancipación', 100, 1000),
            ('Jr. Huallaga', 100, 700),
            ('Av. Alfonso Ugarte', 100, 2000),
            ('Jr. Quilca', 100, 500),
        ],
        'referencias': [
            'Plaza Mayor',
            'Palacio de Gobierno',
            'Catedral de Lima',
            'Jr. de la Unión',
            'Plaza San Martín',
        ],
        'tipos_establecimiento': {
            'oficina': 0.40,
            'departamento': 0.10,
            'local_comercial': 0.45,
            'casa': 0.05,
        }
    },

    'lince': {
        'peso': 6,
        'codigo_postal': '15046',
        'calles': [
            ('Av. Arequipa', 1500, 3500),
            ('Av. Petit Thouars', 2000, 4500),
            ('Av. Arenales', 1000, 3000),
            ('Av. Comandante Jiménez', 100, 800),
            ('Av. Inca Garcilaso de la Vega', 100, 1500),
            ('Calle José Sabogal', 100, 500),
            ('Av. Ignacio Merino', 100, 1000),
        ],
        'referencias': [
            'Campo de Marte',
            'Estadio Nacional',
            'Municipalidad de Lince',
            'Clínica San Felipe',
        ],
        'tipos_establecimiento': {
            'oficina': 0.30,
            'departamento': 0.35,
            'local_comercial': 0.30,
            'casa': 0.05,
        }
    },

    'jesus_maria': {
        'peso': 7,
        'codigo_postal': '15072',
        'calles': [
            ('Av. Brasil', 500, 3000),
            ('Av. Salaverry', 1000, 2500),
            ('Av. San Felipe', 100, 2000),
            ('Av. Horacio Urteaga', 100, 1500),
            ('Av. Arenales', 100, 1500),
            ('Av. General Garzón', 100, 1800),
            ('Av. Pershing', 100, 800),
        ],
        'referencias': [
            'Campo de Marte',
            'Museo de Arte',
            'Hospital Militar',
            'Supermercados Peruanos',
        ],
        'tipos_establecimiento': {
            'oficina': 0.35,
            'departamento': 0.30,
            'local_comercial': 0.30,
            'casa': 0.05,
        }
    },

    'pueblo_libre': {
        'peso': 6,
        'codigo_postal': '15084',
        'calles': [
            ('Av. La Mar', 500, 2500),
            ('Av. Brasil', 100, 2000),
            ('Av. Universitaria', 100, 1500),
            ('Av. Bolívar', 100, 2000),
            ('Av. Vivanco', 100, 1000),
            ('Calle San Martín', 100, 800),
        ],
        'referencias': [
            'Museo Nacional',
            'Parque Castilla',
            'Plaza Bolívar',
            'Quinta Heeren',
        ],
        'tipos_establecimiento': {
            'oficina': 0.25,
            'departamento': 0.30,
            'local_comercial': 0.35,
            'casa': 0.10,
        }
    },

    'magdalena': {
        'peso': 5,
        'codigo_postal': '15086',
        'calles': [
            ('Av. Brasil', 3000, 5500),
            ('Av. Javier Prado Oeste', 100, 1500),
            ('Av. Universitaria', 1500, 3000),
            ('Av. Faustino Sánchez Carrión', 100, 1500),
            ('Calle Leoncio Prado', 100, 600),
        ],
        'referencias': [
            'Costa Verde',
            'Clínica Anglo Americana',
            'Universidad del Pacífico',
            'Plaza Vea Magdalena',
        ],
        'tipos_establecimiento': {
            'oficina': 0.30,
            'departamento': 0.35,
            'local_comercial': 0.25,
            'casa': 0.10,
        }
    },

    'san_miguel': {
        'peso': 8,
        'codigo_postal': '15088',
        'calles': [
            ('Av. La Marina', 1000, 4000),
            ('Av. Universitaria', 3500, 6000),
            ('Av. Gregorio Escobedo', 100, 1500),
            ('Av. Elmer Faucett', 100, 3000),
            ('Av. Bertello', 100, 1000),
            ('Calle Maranga', 100, 800),
        ],
        'referencias': [
            'Plaza San Miguel',
            'Universidad Católica',
            'Parque de las Leyendas',
            'Av. La Marina',
        ],
        'tipos_establecimiento': {
            'oficina': 0.25,
            'departamento': 0.30,
            'local_comercial': 0.35,
            'casa': 0.10,
        }
    },

    'callao': {
        'peso': 9,
        'codigo_postal': '07001',
        'calles': [
            ('Av. Óscar R. Benavides', 1000, 5000),
            ('Av. Sáenz Peña', 100, 2000),
            ('Av. Guardia Chalaca', 100, 2500),
            ('Av. Argentina', 100, 3000),
            ('Jr. Constitución', 100, 800),
            ('Av. Néstor Gambetta', 100, 4000),
        ],
        'referencias': [
            'Puerto del Callao',
            'Plaza Grau',
            'Fortaleza Real Felipe',
            'Aeropuerto Jorge Chávez',
        ],
        'tipos_establecimiento': {
            'oficina': 0.30,
            'departamento': 0.20,
            'local_comercial': 0.40,
            'casa': 0.10,
        }
    },

    'breña': {
        'peso': 5,
        'codigo_postal': '15082',
        'calles': [
            ('Av. Arica', 100, 1500),
            ('Av. Venezuela', 100, 2500),
            ('Av. Brasil', 100, 1000),
            ('Jr. Tizón y Bueno', 100, 800),
            ('Av. Bolivia', 100, 1500),
        ],
        'referencias': [
            'Plaza Bolognesi',
            'Hospital del Niño',
            'Parque Castilla',
        ],
        'tipos_establecimiento': {
            'oficina': 0.30,
            'departamento': 0.30,
            'local_comercial': 0.35,
            'casa': 0.05,
        }
    },

    'los_olivos': {
        'peso': 10,
        'codigo_postal': '15304',
        'calles': [
            ('Av. Universitaria', 6500, 9000),
            ('Av. Alfredo Mendiola', 3000, 7000),
            ('Av. Carlos Izaguirre', 100, 3000),
            ('Av. Naranjal', 100, 2000),
            ('Av. Antúnez de Mayolo', 100, 2500),
            ('Av. Las Palmeras', 100, 2000),
        ],
        'referencias': [
            'Megaplaza',
            'Plaza Norte',
            'Municipalidad Los Olivos',
            'Parque Zonal Lloque Yupanqui',
        ],
        'tipos_establecimiento': {
            'oficina': 0.25,
            'departamento': 0.25,
            'local_comercial': 0.40,
            'casa': 0.10,
        }
    },

    'independencia': {
        'peso': 7,
        'codigo_postal': '15311',
        'calles': [
            ('Av. Túpac Amaru', 1000, 5000),
            ('Av. Los Alisos', 100, 2000),
            ('Av. Chinchaysuyo', 100, 1500),
            ('Av. Canta Callao', 100, 2500),
        ],
        'referencias': [
            'Parque El Ermitaño',
            'Plaza Túpac Amaru',
            'Hospital Cayetano Heredia',
        ],
        'tipos_establecimiento': {
            'oficina': 0.20,
            'departamento': 0.25,
            'local_comercial': 0.45,
            'casa': 0.10,
        }
    },

    'san_martin_de_porres': {
        'peso': 9,
        'codigo_postal': '15101',
        'calles': [
            ('Av. Universitaria', 4000, 7500),
            ('Av. Perú', 100, 4000),
            ('Av. Canta Callao', 2500, 5000),
            ('Av. Alfredo Mendiola', 1000, 4000),
            ('Av. Dominicos', 100, 1500),
            ('Av. Tomás Valle', 100, 2000),
        ],
        'referencias': [
            'Universidad Cayetano Heredia',
            'Plaza Norte',
            'Estadio Iván Elías Moreno',
        ],
        'tipos_establecimiento': {
            'oficina': 0.25,
            'departamento': 0.30,
            'local_comercial': 0.35,
            'casa': 0.10,
        }
    },

    'rimac': {
        'peso': 5,
        'codigo_postal': '15093',
        'calles': [
            ('Av. Francisco Pizarro', 100, 2000),
            ('Jr. Trujillo', 100, 1000),
            ('Av. Gran Chimú', 100, 1500),
            ('Jr. Hualgayoc', 100, 800),
        ],
        'referencias': [
            'Cerro San Cristóbal',
            'Alameda de los Descalzos',
            'Convento de los Descalzos',
        ],
        'tipos_establecimiento': {
            'oficina': 0.25,
            'departamento': 0.25,
            'local_comercial': 0.40,
            'casa': 0.10,
        }
    },

    'la_victoria': {
        'peso': 8,
        'codigo_postal': '15018',
        'calles': [
            ('Av. Iquitos', 100, 2000),
            ('Av. México', 100, 2500),
            ('Av. Aviación', 100, 1500),
            ('Jr. Parinacochas', 100, 1500),
            ('Av. 28 de Julio', 100, 2000),
        ],
        'referencias': [
            'Gamarra',
            'Mercado Mayorista',
            'Parque de la Muralla',
        ],
        'tipos_establecimiento': {
            'oficina': 0.20,
            'departamento': 0.15,
            'local_comercial': 0.60,
            'casa': 0.05,
        }
    },

    'ate': {
        'peso': 9,
        'codigo_postal': '15026',
        'calles': [
            ('Av. Separadora Industrial', 2000, 5000),
            ('Av. Nicolás Ayllón', 1000, 5000),
            ('Av. Los Frutales', 100, 2000),
            ('Av. Metropolitana', 100, 3000),
            ('Av. Javier Prado Este', 9000, 12000),
        ],
        'referencias': [
            'Puruchuco',
            'Real Plaza Puruchuco',
            'Parque Zonal Huáscar',
        ],
        'tipos_establecimiento': {
            'oficina': 0.25,
            'departamento': 0.20,
            'local_comercial': 0.45,
            'casa': 0.10,
        }
    },

    'santa_anita': {
        'peso': 7,
        'codigo_postal': '15009',
        'calles': [
            ('Av. Los Ruiseñores', 100, 2000),
            ('Av. Carretera Central', 1000, 4000),
            ('Av. Nicolás Ayllón', 5000, 8000),
            ('Av. Héroes del Cenepa', 100, 1500),
        ],
        'referencias': [
            'Terrapuerto Yerbateros',
            'Plaza Lima Sur',
            'Parque Industrial',
        ],
        'tipos_establecimiento': {
            'oficina': 0.20,
            'departamento': 0.25,
            'local_comercial': 0.45,
            'casa': 0.10,
        }
    },

    'villa_el_salvador': {
        'peso': 8,
        'codigo_postal': '15842',
        'calles': [
            ('Av. Revolución', 100, 3000),
            ('Av. Pachacútec', 100, 5000),
            ('Av. El Sol', 100, 2000),
            ('Av. Central', 100, 3000),
            ('Av. 200 Millas', 100, 2500),
        ],
        'referencias': [
            'Parque Industrial',
            'Megaplaza Villa El Salvador',
            'CEFOP',
        ],
        'tipos_establecimiento': {
            'oficina': 0.20,
            'departamento': 0.25,
            'local_comercial': 0.45,
            'casa': 0.10,
        }
    },

    'villa_maria_del_triunfo': {
        'peso': 7,
        'codigo_postal': '15810',
        'calles': [
            ('Av. Pachacútec', 5000, 8000),
            ('Av. Salvador Allende', 100, 2000),
            ('Av. Lima', 100, 2500),
            ('Av. 26 de Noviembre', 100, 1500),
        ],
        'referencias': [
            'Cerro Puquio',
            'José Gálvez',
            'Nueva Esperanza',
        ],
        'tipos_establecimiento': {
            'oficina': 0.15,
            'departamento': 0.30,
            'local_comercial': 0.45,
            'casa': 0.10,
        }
    },

    'chorrillos': {
        'peso': 7,
        'codigo_postal': '15063',
        'calles': [
            ('Av. Huaylas', 100, 3000),
            ('Av. Defensores del Morro', 100, 2000),
            ('Av. Guardia Civil Sur', 100, 1500),
            ('Av. Alameda Sur', 100, 2000),
        ],
        'referencias': [
            'Morro Solar',
            'Playa La Herradura',
            'Regatas Lima',
        ],
        'tipos_establecimiento': {
            'oficina': 0.20,
            'departamento': 0.30,
            'local_comercial': 0.40,
            'casa': 0.10,
        }
    },

    'barranco': {
        'peso': 5,
        'codigo_postal': '15063',
        'calles': [
            ('Av. Grau', 100, 1500),
            ('Av. República de Panamá', 6000, 7000),
            ('Av. San Martín', 100, 800),
            ('Jr. Domeyer', 100, 400),
            ('Av. Pedro de Osma', 100, 500),
        ],
        'referencias': [
            'Puente de los Suspiros',
            'Malecón Barranco',
            'Parque Municipal',
            'MATE Museo',
        ],
        'tipos_establecimiento': {
            'oficina': 0.25,
            'departamento': 0.30,
            'local_comercial': 0.35,
            'casa': 0.10,
        }
    },

    'comas': {
        'peso': 8,
        'codigo_postal': '15314',
        'calles': [
            ('Av. Túpac Amaru', 5000, 9000),
            ('Av. Universitaria', 9000, 12000),
            ('Av. Revolución', 100, 3000),
            ('Av. Micaela Bastidas', 100, 2000),
        ],
        'referencias': [
            'Plaza Comas',
            'Parque Zonal Sinchi Roca',
            'Universidad Nacional Federico Villarreal',
        ],
        'tipos_establecimiento': {
            'oficina': 0.20,
            'departamento': 0.25,
            'local_comercial': 0.45,
            'casa': 0.10,
        }
    },
}


# Complementos para direcciones (se agregan aleatoriamente)
COMPLEMENTOS_DIRECCION = {
    'oficina': [
        'Oficina {num}',
        'Of. {num}',
        'Piso {piso}, Oficina {num}',
        'Torre {torre}, Oficina {num}',
        'Torre {torre}, Piso {piso}, Of. {num}',
    ],
    'departamento': [
        'Dpto. {num}',
        'Departamento {num}',
        'Piso {piso}, Dpto. {num}',
        'Torre {torre}, Dpto. {num}',
        'Torre {torre}, Piso {piso}, Dpto. {num}',
        'Int. {num}',
    ],
    'local_comercial': [
        'Local {num}',
        'Stand {num}',
        'Tienda {num}',
        'Galería {nombre}, Stand {num}',
    ],
    'casa': [
        'Casa {num}',
        '',  # A veces solo la dirección
    ],
}

# Nombres de torres para edificios
TORRES = ['A', 'B', 'C', 'D', '1', '2', '3', 'Norte', 'Sur', 'Este', 'Oeste', 'Central']

# Nombres de galerías comerciales
GALERIAS = ['Las Malvinas', 'Guizado', 'Virgen del Carmen', 'El Inca', 'Santa Rosa', 'Bazar Gamarra']


def generar_direccion_realista(
    distrito: Optional[str] = None,
    tipo_establecimiento: Optional[str] = None,
    incluir_referencia: bool = True
) -> str:
    """
    Genera una dirección realista de Lima.

    Args:
        distrito: Distrito específico (opcional). Si no se especifica, se selecciona uno ponderado.
        tipo_establecimiento: 'oficina', 'departamento', 'local_comercial', 'casa' (opcional)
        incluir_referencia: Si True, puede agregar referencia al final (30% probabilidad)

    Returns:
        str: Dirección completa realista

    Ejemplos:
        >>> generar_direccion_realista()
        'Av. Larco 456, Oficina 302, Miraflores, Lima 15074'

        >>> generar_direccion_realista(distrito='san_isidro', tipo_establecimiento='oficina')
        'Calle Las Begonias 475, Piso 8, Oficina 802, San Isidro, Lima 15073'
    """
    # Seleccionar distrito (ponderado o específico)
    if distrito is None:
        distritos = list(DIRECCIONES_POR_DISTRITO.keys())
        pesos = [DIRECCIONES_POR_DISTRITO[d]['peso'] for d in distritos]
        distrito = random.choices(distritos, weights=pesos, k=1)[0]

    distrito_data = DIRECCIONES_POR_DISTRITO[distrito]

    # Seleccionar calle y número
    calle, num_min, num_max = random.choice(distrito_data['calles'])
    numero = random.randint(num_min, num_max)

    # Seleccionar tipo de establecimiento (ponderado o específico)
    if tipo_establecimiento is None:
        tipos = list(distrito_data['tipos_establecimiento'].keys())
        pesos_tipos = list(distrito_data['tipos_establecimiento'].values())
        tipo_establecimiento = random.choices(tipos, weights=pesos_tipos, k=1)[0]

    # Generar complemento (Torre, Oficina, Dpto, etc.)
    complemento = ''
    if random.random() < 0.70:  # 70% de las direcciones tienen complemento
        plantillas = COMPLEMENTOS_DIRECCION[tipo_establecimiento]
        plantilla = random.choice(plantillas)

        if plantilla:
            params = {
                'num': random.randint(101, 999),
                'piso': random.randint(1, 15),
                'torre': random.choice(TORRES),
                'nombre': random.choice(GALERIAS),
            }
            complemento = ', ' + plantilla.format(**params)

    # Construir dirección base
    distrito_nombre = distrito.replace('_', ' ').title()
    codigo_postal = distrito_data['codigo_postal']

    direccion = f"{calle} {numero}{complemento}, {distrito_nombre}, Lima {codigo_postal}"

    # Agregar referencia (30% probabilidad)
    if incluir_referencia and random.random() < 0.30 and distrito_data['referencias']:
        referencia = random.choice(distrito_data['referencias'])
        direccion += f", Ref: {referencia}"

    return direccion


def obtener_distrito_aleatorio() -> str:
    """
    Selecciona un distrito aleatorio con ponderación.

    Returns:
        str: Nombre del distrito
    """
    distritos = list(DIRECCIONES_POR_DISTRITO.keys())
    pesos = [DIRECCIONES_POR_DISTRITO[d]['peso'] for d in distritos]
    return random.choices(distritos, weights=pesos, k=1)[0]


def obtener_codigo_postal(distrito: str) -> str:
    """
    Obtiene el código postal de un distrito.

    Args:
        distrito: Nombre del distrito

    Returns:
        str: Código postal
    """
    return DIRECCIONES_POR_DISTRITO.get(distrito, {}).get('codigo_postal', '15001')


def generar_par_direcciones(mismo_distrito: bool = False) -> Tuple[str, str]:
    """
    Genera un par de direcciones para emisor y receptor.

    Args:
        mismo_distrito: Si True, ambas direcciones son del mismo distrito (20% más común)

    Returns:
        Tuple[str, str]: (direccion_emisor, direccion_receptor)
    """
    distrito_emisor = obtener_distrito_aleatorio()

    # 20% de las facturas son dentro del mismo distrito
    if mismo_distrito or random.random() < 0.20:
        distrito_receptor = distrito_emisor
    else:
        distrito_receptor = obtener_distrito_aleatorio()

    # Emisor suele ser oficina o local comercial
    tipo_emisor = random.choice(['oficina', 'local_comercial', 'oficina', 'oficina'])

    # Receptor es más variado
    tipo_receptor = random.choice(['oficina', 'departamento', 'local_comercial', 'casa'])

    direccion_emisor = generar_direccion_realista(
        distrito=distrito_emisor,
        tipo_establecimiento=tipo_emisor,
        incluir_referencia=False  # Emisor no necesita referencia
    )

    direccion_receptor = generar_direccion_realista(
        distrito=distrito_receptor,
        tipo_establecimiento=tipo_receptor,
        incluir_referencia=True  # Receptor puede tener referencia
    )

    return direccion_emisor, direccion_receptor


def obtener_distritos_disponibles() -> List[str]:
    """
    Retorna lista de todos los distritos disponibles.

    Returns:
        List[str]: Lista de nombres de distritos
    """
    return list(DIRECCIONES_POR_DISTRITO.keys())


def obtener_info_distrito(distrito: str) -> Dict:
    """
    Obtiene información completa de un distrito.

    Args:
        distrito: Nombre del distrito

    Returns:
        Dict: Información del distrito (calles, código postal, referencias, etc.)
    """
    return DIRECCIONES_POR_DISTRITO.get(distrito, {})


# Estadísticas para debugging
def imprimir_estadisticas():
    """Imprime estadísticas de la base de datos de direcciones."""
    total_distritos = len(DIRECCIONES_POR_DISTRITO)
    total_calles = sum(len(d['calles']) for d in DIRECCIONES_POR_DISTRITO.values())
    total_referencias = sum(len(d['referencias']) for d in DIRECCIONES_POR_DISTRITO.values())

    print(f"📍 Base de Datos de Direcciones de Lima")
    print(f"   • Distritos: {total_distritos}")
    print(f"   • Calles/Avenidas: {total_calles}")
    print(f"   • Referencias: {total_referencias}")
    print(f"\nDistritos disponibles:")
    for distrito, data in DIRECCIONES_POR_DISTRITO.items():
        distrito_nombre = distrito.replace('_', ' ').title()
        print(f"   • {distrito_nombre} (CP: {data['codigo_postal']}, {len(data['calles'])} calles)")


if __name__ == '__main__':
    # Pruebas
    print("\n" + "="*80)
    print("PRUEBA: Generación de Direcciones Realistas")
    print("="*80 + "\n")

    imprimir_estadisticas()

    print("\n" + "-"*80)
    print("Ejemplos de direcciones generadas:")
    print("-"*80)

    for i in range(10):
        direccion = generar_direccion_realista()
        print(f"{i+1:2}. {direccion}")

    print("\n" + "-"*80)
    print("Par de direcciones (Emisor-Receptor):")
    print("-"*80)

    for i in range(3):
        emisor, receptor = generar_par_direcciones()
        print(f"\nPar {i+1}:")
        print(f"   Emisor:   {emisor}")
        print(f"   Receptor: {receptor}")

    print("\n" + "="*80)
    print("✅ Pruebas completadas")
    print("="*80 + "\n")
