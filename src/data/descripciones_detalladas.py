#!/usr/bin/env python3
"""
Descripciones Detalladas de Productos
=====================================

Genera descripciones realistas de productos con variantes de marca, tipo,
presentación, color, tamaño y especificaciones técnicas.

Uso:
    from src.data.descripciones_detalladas import generar_descripcion_producto

    desc = generar_descripcion_producto('restaurante', 'CEVICHE CLASICO')
    # Resultado: "CEVICHE CLASICO DE PESCADO FRESCO - PORCIÓN PERSONAL"

    desc = generar_descripcion_producto('farmacia', 'PARACETAMOL')
    # Resultado: "PARACETAMOL 500MG - MARCA GENFARMA - CAJA X 20 TABLETAS"
"""

import random
from typing import Dict, List, Optional, Tuple


# Marcas por categoría de producto
MARCAS = {
    # Alimentación
    'lacteos': ['GLORIA', 'LAIVE', 'PURA VIDA', 'BELLA HOLANDESA', 'ANCHOR'],
    'gaseosas': ['COCA COLA', 'INCA KOLA', 'PEPSI', 'SPRITE', 'FANTA', 'KOLA REAL'],
    'cerveza': ['CRISTAL', 'PILSEN', 'CUSQUEÑA', 'CORONA', 'HEINEKEN'],
    'snacks': ['LAYS', 'PIQUEO', 'KARINTO', 'CUATES', 'DORITOS'],
    'galletas': ['FIELD', 'VICTORIA', 'SODA', 'TENTACIÓN', 'MOROCHAS'],
    'agua': ['SAN LUIS', 'CIELO', 'SAN MATEO', 'SOCOSANI'],
    'aceite': ['PRIMOR', 'COCINERO', 'BELLS', 'CAPRI'],
    'arroz': ['COSTEÑO', 'PAISANA', 'FARAÓN', 'SUPERIOR'],
    'azucar': ['CARTAVIO', 'PARAMONGA', 'CASA GRANDE'],

    # Farmacia
    'analgesicos': ['GENFARMA', 'FARMINDUSTRIA', 'ROEMMERS', 'BAYER', 'NOVARTIS'],
    'antibioticos': ['GENFAR', 'FARMINDUSTRIA', 'PFIZER', 'AMOXIDAL'],
    'vitaminas': ['CENTRUM', 'SUPRADYN', 'PHARMATON', 'REDOXON'],
    'jarabe': ['ABRILAR', 'BISOLVON', 'NASTIZOL', 'INISTON'],

    # Ferretería
    'cemento': ['SOL', 'ANDINO', 'ATLAS', 'INKA'],
    'pintura': ['CPP', 'TEKNO', 'VENCEDOR', 'ANYPSA'],
    'herramientas': ['STANLEY', 'TRUPER', 'BLACK & DECKER', 'DEWALT', 'MAKITA'],
    'tuberia': ['PAVCO', 'TIGRE', 'NICOLL'],
    'cable': ['INDECO', 'MARVIT', 'CEPER'],

    # Electrodomésticos
    'tv': ['LG', 'SAMSUNG', 'SONY', 'TCL', 'HISENSE'],
    'refrigeradora': ['LG', 'SAMSUNG', 'INDURAMA', 'BOSCH', 'MABE'],
    'lavadora': ['LG', 'SAMSUNG', 'ELECTROLUX', 'WHIRLPOOL', 'BOSCH'],
    'cocina': ['INDURAMA', 'BOSCH', 'SOLE', 'KLIMATIC'],
    'microondas': ['LG', 'SAMSUNG', 'PANASONIC', 'OSTER'],
    'licuadora': ['OSTER', 'IMACO', 'THOMAS', 'PHILIPS'],

    # Tecnología
    'laptop': ['HP', 'LENOVO', 'DELL', 'ASUS', 'ACER'],
    'celular': ['SAMSUNG', 'XIAOMI', 'HUAWEI', 'APPLE', 'MOTOROLA'],
    'impresora': ['HP', 'EPSON', 'CANON', 'BROTHER'],

    # Automotriz
    'neumaticos': ['GOODYEAR', 'MICHELIN', 'PIRELLI', 'BRIDGESTONE', 'HANKOOK'],
    'bateria': ['ETNA', 'BOSCH', 'RECORD', 'AC DELCO'],
    'aceite_motor': ['MOBIL', 'CASTROL', 'SHELL', 'REPSOL', 'VISTONY'],
    'filtro': ['BOSCH', 'MANN', 'FRAM', 'PUROLATOR'],

    # Limpieza
    'detergente': ['ARIEL', 'MARSELLA', 'BOLÍVAR', 'ACE'],
    'suavizante': ['SUAVITEL', 'DOWNY', 'MAGIA BLANCA'],
    'lejia': ['CLOROX', 'ALICORP', 'SAPOLIO'],

    # Genérica
    'generica': ['MARCA PROPIA', 'GENÉRICO', 'IMPORTADO', 'NACIONAL'],
}


# Presentaciones por tipo de producto
PRESENTACIONES = {
    'medicamento': [
        'CAJA X {cant} TABLETAS',
        'CAJA X {cant} CÁPSULAS',
        'FRASCO X {cant}ML',
        'BLISTER X {cant} UNIDADES',
        'SOBRE X {cant}G',
    ],
    'alimento': [
        'UNIDAD',
        'PACK X {cant}',
        'CAJA X {cant} UNIDADES',
        'BOLSA X {cant}G',
        'KILO',
        'MEDIA DOCENA',
        'DOCENA',
    ],
    'bebida': [
        'BOTELLA X {cant}ML',
        'LATA X {cant}ML',
        'PACK X {cant} UNIDADES',
        'CAJA X {cant}L',
    ],
    'construccion': [
        'BOLSA X {cant}KG',
        'UNIDAD',
        'METRO',
        'CAJA X {cant} UNIDADES',
        'ROLLO X {cant}M',
        'GALON',
        'BALDE X {cant}L',
    ],
    'electrodomestico': [
        'UNIDAD',
    ],
    'tecnologia': [
        'UNIDAD',
    ],
    'repuesto': [
        'UNIDAD',
        'JUEGO X {cant}',
        'PAR',
        'SET X {cant} PIEZAS',
    ],
    'servicio': [
        'SERVICIO',
        'HORA',
        'MES',
        'SESIÓN',
    ],
    'generico': [
        'UNIDAD',
        'PACK X {cant}',
        'CAJA X {cant}',
    ],
}


# Variantes por tipo de producto
VARIANTES = {
    'color': ['BLANCO', 'NEGRO', 'ROJO', 'AZUL', 'VERDE', 'AMARILLO', 'GRIS', 'PLATEADO', 'DORADO'],
    'tamaño': ['S', 'M', 'L', 'XL', 'PEQUEÑO', 'MEDIANO', 'GRANDE', 'FAMILIAR'],
    'sabor': ['FRESA', 'VAINILLA', 'CHOCOLATE', 'LIMÓN', 'NARANJA', 'MANZANA', 'UVA'],
    'temperatura': ['FRÍO', 'CALIENTE', 'NATURAL'],
    'tipo_carne': ['POLLO', 'RES', 'PESCADO', 'CERDO', 'MIXTO'],
    'tipo_leche': ['ENTERA', 'DESCREMADA', 'LIGHT', 'DESLACTOSADA', 'EVAPORADA'],
    'tipo_pan': ['FRANCÉS', 'CIABATTA', 'INTEGRAL', 'PITA', 'CHAPATA'],
}


# Especificaciones técnicas por categoría
ESPECIFICACIONES = {
    'tv': [
        '{pulgadas}" {tipo}',
        '{pulgadas}" {resolucion}',
        '{pulgadas}" {tipo} {resolucion}',
    ],
    'tv_pulgadas': ['32', '43', '50', '55', '65', '75'],
    'tv_tipo': ['LED', 'SMART TV', 'QLED', '4K'],
    'tv_resolucion': ['HD', 'FULL HD', '4K', 'UHD'],

    'refrigeradora': [
        '{capacidad}L {tipo}',
        '{puertas} PUERTAS {capacidad}L',
        '{tipo} {capacidad}L {clase}',
    ],
    'refri_capacidad': ['250', '300', '350', '400', '450', '500'],
    'refri_tipo': ['NO FROST', 'FROST', 'SIDE BY SIDE'],
    'refri_puertas': ['1', '2', '3'],
    'refri_clase': ['CLASE A', 'CLASE A+', 'CLASE A++'],

    'laptop': [
        '{procesador} {ram}GB RAM {disco}',
        '{marca_proc} {modelo} {ram}GB',
        '{pantalla}" {procesador} {ram}GB',
    ],
    'laptop_procesador': ['CORE I3', 'CORE I5', 'CORE I7', 'RYZEN 5', 'RYZEN 7'],
    'laptop_marca_proc': ['INTEL', 'AMD'],
    'laptop_modelo': ['CORE I3 10MA GEN', 'CORE I5 11VA GEN', 'RYZEN 5 5500U'],
    'laptop_ram': ['4', '8', '16', '32'],
    'laptop_disco': ['256GB SSD', '512GB SSD', '1TB HDD', '1TB SSD'],
    'laptop_pantalla': ['14', '15.6', '17'],

    'celular': [
        '{almacenamiento} {ram}GB RAM',
        '{almacenamiento} {camara}MP',
        '{pantalla}" {almacenamiento} {ram}GB',
    ],
    'celular_almacenamiento': ['64GB', '128GB', '256GB', '512GB'],
    'celular_ram': ['4', '6', '8', '12'],
    'celular_camara': ['48', '64', '108', '200'],
    'celular_pantalla': ['6.1', '6.5', '6.7'],

    'neumatico': [
        'MEDIDA {medida}',
        'ARO {aro} {medida}',
        'RADIAL {medida}',
    ],
    'neumatico_medida': ['175/70R13', '185/65R14', '195/55R15', '205/55R16', '215/55R17'],
    'neumatico_aro': ['13', '14', '15', '16', '17', '18'],

    'pintura': [
        'GALON {tipo}',
        '{tipo} {color}',
        'GALON {tipo} {acabado}',
    ],
    'pintura_tipo': ['LÁTEX', 'ESMALTE', 'TEMPLE', 'ANTICORROSIVO'],
    'pintura_acabado': ['MATE', 'SATINADO', 'SEMI MATE', 'BRILLANTE'],

    'cemento': [
        'BOLSA X {peso}KG {tipo}',
    ],
    'cemento_peso': ['42.5'],
    'cemento_tipo': ['TIPO I', 'TIPO II', 'TIPO V', 'PORTLAND'],

    'medicamento': [
        '{dosis}MG',
        '{dosis}MG/{cantidad}ML',
        '{dosis}G CREMA',
    ],
    'med_dosis': ['500', '250', '100', '50', '25', '10', '5'],
    'med_cantidad': ['5', '10', '15', '20', '30', '60', '100', '120'],
}


def generar_descripcion_producto(
    sector: str,
    producto_base: str,
    incluir_marca: bool = True,
    incluir_presentacion: bool = True,
    incluir_variante: bool = True,
    incluir_especificaciones: bool = True
) -> str:
    """
    Genera una descripción detallada y realista de un producto.

    Args:
        sector: Sector del negocio (restaurante, farmacia, ferreteria, etc.)
        producto_base: Nombre base del producto
        incluir_marca: Si True, agrega marca al producto (70% probabilidad)
        incluir_presentacion: Si True, agrega presentación (80% probabilidad)
        incluir_variante: Si True, agrega variantes (50% probabilidad)
        incluir_especificaciones: Si True, agrega specs técnicas (60% probabilidad)

    Returns:
        str: Descripción completa del producto

    Ejemplos:
        >>> generar_descripcion_producto('farmacia', 'PARACETAMOL')
        'PARACETAMOL 500MG - GENFARMA - CAJA X 20 TABLETAS'

        >>> generar_descripcion_producto('restaurante', 'CEVICHE')
        'CEVICHE DE PESCADO FRESCO - PORCIÓN PERSONAL'

        >>> generar_descripcion_producto('electrodomesticos', 'TELEVISOR')
        'TELEVISOR LG 55" SMART TV 4K'
    """
    partes = [producto_base]

    # Agregar especificaciones técnicas según el producto
    if incluir_especificaciones and random.random() < 0.60:
        specs = _obtener_especificaciones(producto_base)
        if specs:
            partes[0] = f"{partes[0]} {specs}"

    # Agregar variantes (color, tamaño, tipo, etc.)
    if incluir_variante and random.random() < 0.50:
        variante = _obtener_variante(sector, producto_base)
        if variante:
            partes.append(variante)

    # Agregar marca
    if incluir_marca and random.random() < 0.70:
        marca = _obtener_marca(producto_base, sector)
        if marca:
            partes.append(f"MARCA {marca}")

    # Agregar presentación
    if incluir_presentacion and random.random() < 0.80:
        presentacion = _obtener_presentacion(sector, producto_base)
        if presentacion:
            partes.append(presentacion)

    return ' - '.join(partes)


def _obtener_marca(producto: str, sector: str) -> Optional[str]:
    """Obtiene una marca apropiada para el producto."""
    producto_lower = producto.lower()

    # Mapeo de palabras clave a categorías de marca
    mapeo_marcas = {
        'leche': 'lacteos',
        'yogurt': 'lacteos',
        'queso': 'lacteos',
        'mantequilla': 'lacteos',
        'gaseosa': 'gaseosas',
        'refresco': 'gaseosas',
        'coca': 'gaseosas',
        'inca kola': 'gaseosas',
        'cerveza': 'cerveza',
        'snack': 'snacks',
        'papas': 'snacks',
        'galleta': 'galletas',
        'agua': 'agua',
        'aceite': 'aceite',
        'arroz': 'arroz',
        'azucar': 'azucar',
        'paracetamol': 'analgesicos',
        'ibuprofeno': 'analgesicos',
        'amoxicilina': 'antibioticos',
        'vitamina': 'vitaminas',
        'jarabe': 'jarabe',
        'cemento': 'cemento',
        'pintura': 'pintura',
        'taladro': 'herramientas',
        'martillo': 'herramientas',
        'destornillador': 'herramientas',
        'tuberia': 'tuberia',
        'tubo': 'tuberia',
        'cable': 'cable',
        'televisor': 'tv',
        'tv': 'tv',
        'refrigeradora': 'refrigeradora',
        'lavadora': 'lavadora',
        'cocina': 'cocina',
        'microondas': 'microondas',
        'licuadora': 'licuadora',
        'laptop': 'laptop',
        'celular': 'celular',
        'smartphone': 'celular',
        'impresora': 'impresora',
        'neumatico': 'neumaticos',
        'llanta': 'neumaticos',
        'bateria': 'bateria',
        'aceite motor': 'aceite_motor',
        'filtro': 'filtro',
        'detergente': 'detergente',
        'suavizante': 'suavizante',
        'lejia': 'lejia',
    }

    for keyword, categoria in mapeo_marcas.items():
        if keyword in producto_lower:
            if categoria in MARCAS:
                return random.choice(MARCAS[categoria])

    # Si no encuentra categoría específica, usar genérica (20% probabilidad)
    if random.random() < 0.20:
        return random.choice(MARCAS['generica'])

    return None


def _obtener_presentacion(sector: str, producto: str) -> Optional[str]:
    """Obtiene una presentación apropiada para el producto."""
    producto_lower = producto.lower()

    # Mapeo de productos a tipo de presentación
    if any(kw in producto_lower for kw in ['paracetamol', 'ibuprofeno', 'amoxicilina', 'tableta', 'capsula']):
        tipo_presentacion = 'medicamento'
        cantidades = [10, 20, 30, 50, 100]
    elif any(kw in producto_lower for kw in ['jarabe', 'suspension']):
        tipo_presentacion = 'medicamento'
        cantidades = [60, 100, 120, 150]
    elif any(kw in producto_lower for kw in ['gaseosa', 'agua', 'bebida', 'jugo']):
        tipo_presentacion = 'bebida'
        cantidades = [300, 500, 600, 1000, 1500, 2000, 3000]
    elif any(kw in producto_lower for kw in ['cemento', 'arena', 'yeso', 'pintura']):
        tipo_presentacion = 'construccion'
        cantidades = [1, 5, 10, 20, 42.5]
    elif any(kw in producto_lower for kw in ['televisor', 'refrigeradora', 'lavadora', 'cocina', 'laptop']):
        tipo_presentacion = 'electrodomestico'
        cantidades = [1]
    elif any(kw in producto_lower for kw in ['neumatico', 'bateria', 'filtro', 'bujia']):
        tipo_presentacion = 'repuesto'
        cantidades = [1, 2, 4]
    elif sector in ['restaurante', 'spa', 'gym', 'odontologia']:
        tipo_presentacion = 'servicio'
        cantidades = [1]
    else:
        # Alimentos y productos genéricos
        tipo_presentacion = 'alimento'
        cantidades = [1, 2, 6, 12, 250, 500, 1000]

    if tipo_presentacion in PRESENTACIONES:
        plantilla = random.choice(PRESENTACIONES[tipo_presentacion])
        cantidad = random.choice(cantidades)

        # Reemplazar {cant} si existe en la plantilla
        if '{cant}' in plantilla:
            return plantilla.format(cant=cantidad)
        else:
            return plantilla

    return None


def _obtener_variante(sector: str, producto: str) -> Optional[str]:
    """Obtiene una variante apropiada para el producto."""
    producto_lower = producto.lower()

    # Variantes por tipo de producto
    if 'ceviche' in producto_lower or 'tiradito' in producto_lower:
        return f"DE {random.choice(VARIANTES['tipo_carne'])}"

    if 'lomo saltado' in producto_lower or 'pollo a la brasa' in producto_lower:
        tamaño = random.choice(['PERSONAL', 'PARA 2', 'FAMILIAR'])
        return f"PORCIÓN {tamaño}"

    if 'leche' in producto_lower:
        return random.choice(VARIANTES['tipo_leche'])

    if 'sandwich' in producto_lower or 'hamburguesa' in producto_lower:
        return f"PAN {random.choice(VARIANTES['tipo_pan'])}"

    if 'refresco' in producto_lower or 'jugo' in producto_lower:
        return f"SABOR {random.choice(VARIANTES['sabor'])}"

    if any(kw in producto_lower for kw in ['polo', 'camisa', 'pantalon', 'zapatilla']):
        return f"TALLA {random.choice(VARIANTES['tamaño'][:4])}"

    if any(kw in producto_lower for kw in ['pintura', 'esmalte', 'barniz']):
        return f"COLOR {random.choice(VARIANTES['color'])}"

    # Genérico: color para productos variados
    if random.random() < 0.30:
        return random.choice(VARIANTES['color'])

    return None


def _obtener_especificaciones(producto: str) -> Optional[str]:
    """Obtiene especificaciones técnicas para el producto."""
    producto_lower = producto.lower()

    # TV
    if 'televisor' in producto_lower or producto_lower == 'tv':
        plantilla = random.choice(ESPECIFICACIONES['tv'])
        return plantilla.format(
            pulgadas=random.choice(ESPECIFICACIONES['tv_pulgadas']),
            tipo=random.choice(ESPECIFICACIONES['tv_tipo']),
            resolucion=random.choice(ESPECIFICACIONES['tv_resolucion'])
        )

    # Refrigeradora
    if 'refrigeradora' in producto_lower or 'refrigerador' in producto_lower:
        plantilla = random.choice(ESPECIFICACIONES['refrigeradora'])
        return plantilla.format(
            capacidad=random.choice(ESPECIFICACIONES['refri_capacidad']),
            tipo=random.choice(ESPECIFICACIONES['refri_tipo']),
            puertas=random.choice(ESPECIFICACIONES['refri_puertas']),
            clase=random.choice(ESPECIFICACIONES['refri_clase'])
        )

    # Laptop
    if 'laptop' in producto_lower or 'notebook' in producto_lower:
        plantilla = random.choice(ESPECIFICACIONES['laptop'])
        return plantilla.format(
            procesador=random.choice(ESPECIFICACIONES['laptop_procesador']),
            marca_proc=random.choice(ESPECIFICACIONES['laptop_marca_proc']),
            modelo=random.choice(ESPECIFICACIONES['laptop_modelo']),
            ram=random.choice(ESPECIFICACIONES['laptop_ram']),
            disco=random.choice(ESPECIFICACIONES['laptop_disco']),
            pantalla=random.choice(ESPECIFICACIONES['laptop_pantalla'])
        )

    # Celular
    if 'celular' in producto_lower or 'smartphone' in producto_lower:
        plantilla = random.choice(ESPECIFICACIONES['celular'])
        return plantilla.format(
            almacenamiento=random.choice(ESPECIFICACIONES['celular_almacenamiento']),
            ram=random.choice(ESPECIFICACIONES['celular_ram']),
            camara=random.choice(ESPECIFICACIONES['celular_camara']),
            pantalla=random.choice(ESPECIFICACIONES['celular_pantalla'])
        )

    # Neumático
    if 'neumatico' in producto_lower or 'llanta' in producto_lower:
        plantilla = random.choice(ESPECIFICACIONES['neumatico'])
        return plantilla.format(
            medida=random.choice(ESPECIFICACIONES['neumatico_medida']),
            aro=random.choice(ESPECIFICACIONES['neumatico_aro'])
        )

    # Pintura
    if 'pintura' in producto_lower:
        plantilla = random.choice(ESPECIFICACIONES['pintura'])
        return plantilla.format(
            tipo=random.choice(ESPECIFICACIONES['pintura_tipo']),
            color=random.choice(VARIANTES['color']),
            acabado=random.choice(ESPECIFICACIONES['pintura_acabado'])
        )

    # Cemento
    if 'cemento' in producto_lower:
        plantilla = random.choice(ESPECIFICACIONES['cemento'])
        return plantilla.format(
            peso=random.choice(ESPECIFICACIONES['cemento_peso']),
            tipo=random.choice(ESPECIFICACIONES['cemento_tipo'])
        )

    # Medicamentos
    if any(kw in producto_lower for kw in ['paracetamol', 'ibuprofeno', 'amoxicilina', 'diclofenaco']):
        plantilla = random.choice(ESPECIFICACIONES['medicamento'][:2])  # Solo dosis en MG
        return plantilla.format(
            dosis=random.choice(ESPECIFICACIONES['med_dosis']),
            cantidad=random.choice(ESPECIFICACIONES['med_cantidad'])
        )

    return None


def generar_descripcion_servicio(tipo_servicio: str, sector: str) -> str:
    """
    Genera descripción de servicios (restaurante, spa, gym, etc.).

    Args:
        tipo_servicio: Nombre del servicio base
        sector: Sector del negocio

    Returns:
        str: Descripción del servicio
    """
    descripciones_especiales = {
        'restaurante': {
            'SERVICIO DELIVERY': 'SERVICIO DE DELIVERY - ZONA {zona}',
            'PROPINA': 'PROPINA - SERVICIO AL CLIENTE',
            'CUBIERTO': 'DERECHO DE CUBIERTO',
        },
        'spa': {
            'MASAJE': 'MASAJE {tipo} - {duracion} MINUTOS',
            'FACIAL': 'TRATAMIENTO FACIAL {tipo}',
            'DEPILACION': 'DEPILACIÓN {zona}',
        },
        'gym': {
            'MEMBRESIA': 'MEMBRESÍA {tipo} - {duracion}',
            'ENTRENAMIENTO': 'ENTRENAMIENTO PERSONALIZADO - SESIÓN',
            'CLASE': 'CLASE DE {tipo}',
        },
    }

    if sector in descripciones_especiales:
        for keyword, plantilla in descripciones_especiales[sector].items():
            if keyword in tipo_servicio:
                # Reemplazar variables en la plantilla
                if '{zona}' in plantilla:
                    zonas = ['MIRAFLORES', 'SAN ISIDRO', 'SURCO', 'LA MOLINA']
                    return plantilla.format(zona=random.choice(zonas))
                elif '{tipo}' in plantilla and sector == 'spa':
                    tipos = ['RELAJANTE', 'DESCONTRACTURANTE', 'DEPORTIVO', 'PIEDRAS CALIENTES']
                    return plantilla.format(tipo=random.choice(tipos), duracion=random.choice(['30', '60', '90']))
                elif '{tipo}' in plantilla and sector == 'gym':
                    if 'MEMBRESIA' in keyword:
                        tipos = ['MENSUAL', 'TRIMESTRAL', 'SEMESTRAL', 'ANUAL']
                        duraciones = ['1 MES', '3 MESES', '6 MESES', '12 MESES']
                        idx = random.randint(0, len(tipos)-1)
                        return plantilla.format(tipo=tipos[idx], duracion=duraciones[idx])
                    else:
                        tipos = ['YOGA', 'PILATES', 'SPINNING', 'ZUMBA', 'CROSSFIT']
                        return plantilla.format(tipo=random.choice(tipos))
                elif '{zona}' in plantilla:
                    zonas = ['PIERNAS', 'BRAZOS', 'ESPALDA', 'FACIAL', 'COMPLETA']
                    return plantilla.format(zona=random.choice(zonas))
                else:
                    return plantilla

    return tipo_servicio


# Estadísticas para debugging
def imprimir_estadisticas():
    """Imprime estadísticas de la base de datos de descripciones."""
    total_categorias_marca = len(MARCAS)
    total_marcas = sum(len(marcas) for marcas in MARCAS.values())
    total_tipos_presentacion = len(PRESENTACIONES)
    total_variantes = sum(len(v) for v in VARIANTES.values())

    print(f"📝 Base de Datos de Descripciones Detalladas")
    print(f"   • Categorías de marcas: {total_categorias_marca}")
    print(f"   • Total de marcas: {total_marcas}")
    print(f"   • Tipos de presentación: {total_tipos_presentacion}")
    print(f"   • Variantes disponibles: {total_variantes}")
    print(f"\nCategorías principales:")
    print(f"   • Alimentación: {len(MARCAS['lacteos']) + len(MARCAS['gaseosas']) + len(MARCAS['snacks'])} marcas")
    print(f"   • Farmacia: {len(MARCAS['analgesicos']) + len(MARCAS['antibioticos']) + len(MARCAS['vitaminas'])} marcas")
    print(f"   • Ferretería: {len(MARCAS['cemento']) + len(MARCAS['pintura']) + len(MARCAS['herramientas'])} marcas")
    print(f"   • Electrodomésticos: {len(MARCAS['tv']) + len(MARCAS['refrigeradora']) + len(MARCAS['lavadora'])} marcas")


if __name__ == '__main__':
    # Pruebas
    print("\n" + "="*80)
    print("PRUEBA: Generación de Descripciones Detalladas")
    print("="*80 + "\n")

    imprimir_estadisticas()

    print("\n" + "-"*80)
    print("Ejemplos de descripciones generadas:")
    print("-"*80)

    # Ejemplos por sector
    ejemplos = [
        ('farmacia', 'PARACETAMOL'),
        ('farmacia', 'AMOXICILINA'),
        ('restaurante', 'CEVICHE CLASICO'),
        ('restaurante', 'LOMO SALTADO'),
        ('ferreteria', 'CEMENTO'),
        ('ferreteria', 'PINTURA'),
        ('electrodomesticos', 'TELEVISOR'),
        ('electrodomesticos', 'REFRIGERADORA'),
        ('supermercado', 'LECHE'),
        ('supermercado', 'GASEOSA'),
        ('automotriz', 'NEUMATICO'),
        ('automotriz', 'ACEITE MOTOR'),
    ]

    for i, (sector, producto) in enumerate(ejemplos, 1):
        descripcion = generar_descripcion_producto(sector, producto)
        print(f"{i:2}. [{sector:20}] {descripcion}")

    print("\n" + "-"*80)
    print("Ejemplos de servicios:")
    print("-"*80)

    servicios = [
        ('restaurante', 'SERVICIO DELIVERY'),
        ('spa', 'MASAJE'),
        ('gym', 'MEMBRESIA'),
        ('gym', 'CLASE'),
    ]

    for sector, servicio in servicios:
        descripcion = generar_descripcion_servicio(servicio, sector)
        print(f"   • [{sector:15}] {descripcion}")

    print("\n" + "="*80)
    print("✅ Pruebas completadas")
    print("="*80 + "\n")
