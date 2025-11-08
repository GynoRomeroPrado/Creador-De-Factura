"""
Utilidades para generación de facturas ficticias
"""
import random
from datetime import datetime, timedelta
from typing import List, Tuple


class RUCGenerator:
    """Generador de RUCs válidos para Perú"""

    @staticmethod
    def generar_ruc() -> str:
        """Genera un RUC de 11 dígitos con dígito verificador válido"""
        # RUC de empresa: empieza con 20
        base = "20" + "".join([str(random.randint(0, 9)) for _ in range(8)])

        # Calcular dígito verificador
        factores = [5, 4, 3, 2, 7, 6, 5, 4, 3, 2]
        suma = sum(int(base[i]) * factores[i] for i in range(10))
        resto = suma % 11
        digito = 11 - resto

        if digito == 10:
            digito = 0
        elif digito == 11:
            digito = 1

        return base + str(digito)


class MontoLetras:
    """Conversor de montos numéricos a letras"""

    UNIDADES = ["", "UNO", "DOS", "TRES", "CUATRO", "CINCO", "SEIS", "SIETE", "OCHO", "NUEVE"]
    DECENAS = ["", "DIEZ", "VEINTE", "TREINTA", "CUARENTA", "CINCUENTA",
               "SESENTA", "SETENTA", "OCHENTA", "NOVENTA"]
    ESPECIALES = {
        11: "ONCE", 12: "DOCE", 13: "TRECE", 14: "CATORCE", 15: "QUINCE",
        16: "DIECISÉIS", 17: "DIECISIETE", 18: "DIECIOCHO", 19: "DIECINUEVE",
        21: "VEINTIUNO", 22: "VEINTIDÓS", 23: "VEINTITRÉS", 24: "VEINTICUATRO",
        25: "VEINTICINCO", 26: "VEINTISÉIS", 27: "VEINTISIETE", 28: "VEINTIOCHO",
        29: "VEINTINUEVE"
    }
    CENTENAS = ["", "CIENTO", "DOSCIENTOS", "TRESCIENTOS", "CUATROCIENTOS",
                "QUINIENTOS", "SEISCIENTOS", "SETECIENTOS", "OCHOCIENTOS", "NOVECIENTOS"]

    @classmethod
    def convertir(cls, monto: float, moneda: str = "SOLES") -> str:
        """
        Convierte un monto a su representación en letras
        Args:
            monto: Cantidad numérica
            moneda: SOLES, DOLARES, EUROS
        Returns:
            String con el monto en letras
        """
        entero = int(monto)
        centavos = int(round((monto - entero) * 100))

        if entero == 0:
            texto = "CERO"
        else:
            texto = cls._convertir_entero(entero)

        # Ajustar singular/plural
        if moneda == "SOLES":
            moneda_texto = "SOL" if entero == 1 else "SOLES"
        elif moneda == "DOLARES":
            moneda_texto = "DÓLAR" if entero == 1 else "DÓLARES"
        elif moneda == "EUROS":
            moneda_texto = "EURO" if entero == 1 else "EUROS"
        else:
            moneda_texto = moneda

        return f"{texto} CON {centavos:02d}/100 {moneda_texto}"

    @classmethod
    def _convertir_entero(cls, numero: int) -> str:
        """Convierte la parte entera a letras"""
        if numero == 0:
            return ""
        elif numero == 100:
            return "CIEN"
        elif numero < 10:
            return cls.UNIDADES[numero]
        elif numero in cls.ESPECIALES:
            return cls.ESPECIALES[numero]
        elif numero < 100:
            decena = numero // 10
            unidad = numero % 10
            if unidad == 0:
                return cls.DECENAS[decena]
            else:
                return f"{cls.DECENAS[decena]} Y {cls.UNIDADES[unidad]}"
        elif numero < 1000:
            centena = numero // 100
            resto = numero % 100
            texto = cls.CENTENAS[centena]
            if resto > 0:
                texto += " " + cls._convertir_entero(resto)
            return texto
        elif numero < 1000000:
            miles = numero // 1000
            resto = numero % 1000
            if miles == 1:
                texto = "MIL"
            else:
                texto = cls._convertir_entero(miles) + " MIL"
            if resto > 0:
                texto += " " + cls._convertir_entero(resto)
            return texto
        elif numero < 1000000000:
            millones = numero // 1000000
            resto = numero % 1000000
            if millones == 1:
                texto = "UN MILLÓN"
            else:
                texto = cls._convertir_entero(millones) + " MILLONES"
            if resto > 0:
                texto += " " + cls._convertir_entero(resto)
            return texto
        else:
            return "NÚMERO DEMASIADO GRANDE"


class DatosPersonas:
    """Generador de datos de personas y empresas ficticias para Perú"""

    NOMBRES = [
        "Juan", "María", "Carlos", "Ana", "Luis", "Rosa", "Pedro", "Carmen",
        "José", "Elena", "Miguel", "Laura", "Jorge", "Patricia", "Roberto",
        "Sofía", "Fernando", "Isabel", "Ricardo", "Gabriela"
    ]

    APELLIDOS = [
        "García", "Rodríguez", "Fernández", "López", "Martínez", "González",
        "Pérez", "Sánchez", "Ramírez", "Torres", "Flores", "Rivera",
        "Gómez", "Díaz", "Cruz", "Morales", "Reyes", "Gutiérrez", "Ortiz", "Mendoza"
    ]

    EMPRESAS_PREFIJOS = [
        "Constructora", "Distribuidora", "Comercial", "Inversiones", "Grupo",
        "Corporación", "Industrias", "Servicios", "Transportes", "Almacenes"
    ]

    EMPRESAS_SUFIJOS = [
        "SAC", "S.A.C.", "S.R.L.", "E.I.R.L.", "S.A."
    ]

    EMPRESAS_NOMBRES = [
        "Los Andes", "El Sol", "San Martín", "Santa Rosa", "La Victoria",
        "El Progreso", "Unión", "Central", "Imperial", "Continental",
        "Del Sur", "Del Norte", "Pacífico", "Atlántico", "Andino"
    ]

    DEPARTAMENTOS_PERU = [
        "Lima", "Arequipa", "Cusco", "Trujillo", "Chiclayo", "Piura",
        "Iquitos", "Huancayo", "Tacna", "Pucallpa"
    ]

    DISTRITOS_LIMA = [
        "Miraflores", "San Isidro", "Surco", "La Molina", "San Borja",
        "Magdalena", "Lince", "Jesús María", "Pueblo Libre", "Breña",
        "San Miguel", "Los Olivos", "Independencia", "San Juan de Lurigancho"
    ]

    CALLES_TIPOS = ["Av.", "Jr.", "Calle", "Psje."]
    CALLES_NOMBRES = [
        "Los Conquistadores", "Arequipa", "Larco", "Pardo", "Brasil",
        "Venezuela", "Argentina", "Javier Prado", "Universitaria", "Colonial",
        "Túpac Amaru", "28 de Julio", "La Marina", "Salaverry", "Benavides"
    ]

    @classmethod
    def generar_nombre_persona(cls) -> str:
        """Genera un nombre completo de persona"""
        nombre = random.choice(cls.NOMBRES)
        apellido1 = random.choice(cls.APELLIDOS)
        apellido2 = random.choice(cls.APELLIDOS)
        return f"{nombre} {apellido1} {apellido2}"

    @classmethod
    def generar_razon_social(cls) -> str:
        """Genera una razón social de empresa"""
        prefijo = random.choice(cls.EMPRESAS_PREFIJOS)
        nombre = random.choice(cls.EMPRESAS_NOMBRES)
        sufijo = random.choice(cls.EMPRESAS_SUFIJOS)
        return f"{prefijo} {nombre} {sufijo}"

    @classmethod
    def generar_direccion(cls) -> str:
        """Genera una dirección peruana"""
        tipo_calle = random.choice(cls.CALLES_TIPOS)
        nombre_calle = random.choice(cls.CALLES_NOMBRES)
        numero = random.randint(100, 9999)
        distrito = random.choice(cls.DISTRITOS_LIMA)

        # A veces agregar número de oficina/departamento
        if random.random() < 0.3:
            extra = f" Of. {random.randint(100, 999)}" if random.random() < 0.5 else f" Dpto. {random.randint(100, 999)}"
            return f"{tipo_calle} {nombre_calle} {numero}{extra}, {distrito}"

        return f"{tipo_calle} {nombre_calle} {numero}, {distrito}"

    @classmethod
    def generar_telefono(cls) -> str:
        """Genera un teléfono peruano"""
        if random.random() < 0.5:
            # Celular
            return f"9{random.randint(10000000, 99999999)}"
        else:
            # Fijo Lima
            return f"01-{random.randint(2000000, 7999999)}"


class GeneradorFechas:
    """Generador de fechas para facturas"""

    @staticmethod
    def generar_fecha_2025() -> datetime:
        """Genera una fecha aleatoria del año 2025"""
        inicio = datetime(2025, 1, 1)
        fin = datetime(2025, 12, 31)
        dias_diff = (fin - inicio).days
        fecha_random = inicio + timedelta(days=random.randint(0, dias_diff))
        return fecha_random

    @staticmethod
    def generar_cuotas(fecha_emision: datetime, num_cuotas: int,
                       dias_entre_cuotas: int = 30) -> List[Tuple[int, datetime, float]]:
        """
        Genera información de cuotas
        Returns: Lista de (numero_cuota, fecha_vencimiento, monto)
        """
        cuotas = []
        for i in range(num_cuotas):
            fecha_venc = fecha_emision + timedelta(days=dias_entre_cuotas * (i + 1))
            cuotas.append((i + 1, fecha_venc))
        return cuotas


class ItemsGenerator:
    """Generador de items para facturas"""

    CONSTRUCCION = [
        ("Cemento Portland Tipo I x 42.5kg", "BOL", (25.00, 35.00)),
        ("Arena Gruesa m3", "M3", (80.00, 120.00)),
        ("Piedra Chancada 1/2\" m3", "M3", (90.00, 130.00)),
        ("Ladrillo King Kong 18 huecos", "UND", (0.80, 1.50)),
        ("Fierro Corrugado 1/2\" x 9m", "UND", (25.00, 40.00)),
        ("Alambre Negro #8 kg", "KG", (4.50, 6.50)),
        ("Clavos con cabeza 3\" kg", "KG", (5.00, 7.00)),
        ("Madera Tornillo 2\"x4\"x10'", "UND", (15.00, 25.00)),
        ("Tubo PVC SAP 2\" x 3m", "UND", (12.00, 20.00)),
        ("Cemento gris x 1kg", "KG", (2.50, 4.00)),
    ]

    COMIDA = [
        ("Arroz Superior x 50kg", "SAC", (120.00, 180.00)),
        ("Aceite Vegetal x 20L", "BID", (85.00, 120.00)),
        ("Azúcar Blanca x 50kg", "SAC", (110.00, 150.00)),
        ("Pollo Entero kg", "KG", (7.50, 9.50)),
        ("Carne de Res kg", "KG", (18.00, 25.00)),
        ("Pescado Fresco kg", "KG", (12.00, 20.00)),
        ("Leche Evaporada x 48 latas", "CJA", (95.00, 130.00)),
        ("Huevos Color x 30 unid", "CAJA", (12.00, 18.00)),
        ("Frijol Canario x 50kg", "SAC", (180.00, 250.00)),
        ("Fideos a Granel kg", "KG", (3.50, 5.00)),
    ]

    SERVICIOS = [
        ("Mantenimiento Preventivo Equipo Industrial", "SRV", (500.00, 2000.00)),
        ("Instalación de Sistema Eléctrico", "SRV", (800.00, 3000.00)),
        ("Servicio de Limpieza Mensual", "MES", (300.00, 1200.00)),
        ("Consultoría Técnica Especializada", "HOR", (80.00, 200.00)),
        ("Transporte de Carga Pesada", "VJE", (400.00, 1500.00)),
        ("Alquiler de Maquinaria Pesada", "DIA", (600.00, 2500.00)),
        ("Servicio de Vigilancia 24hrs", "MES", (1500.00, 3500.00)),
        ("Mantenimiento de Jardinería", "MES", (250.00, 800.00)),
    ]

    @classmethod
    def generar_items(cls, cantidad: int = None, categoria: str = None) -> List[dict]:
        """
        Genera items aleatorios
        Args:
            cantidad: Número de items (si None, aleatorio entre 1-10)
            categoria: 'construccion', 'comida', 'servicios', o None para mixto
        """
        if cantidad is None:
            cantidad = random.randint(1, 10)

        items = []

        # Seleccionar fuente de items
        if categoria == 'construccion':
            fuente = cls.CONSTRUCCION
        elif categoria == 'comida':
            fuente = cls.COMIDA
        elif categoria == 'servicios':
            fuente = cls.SERVICIOS
        else:
            # Mixto
            fuente = cls.CONSTRUCCION + cls.COMIDA + cls.SERVICIOS

        for i in range(cantidad):
            item_base = random.choice(fuente)
            descripcion, unidad, rango_precio = item_base

            cantidad_item = random.randint(1, 100)
            precio_unitario = round(random.uniform(*rango_precio), 2)
            valor_venta = round(cantidad_item * precio_unitario, 2)

            items.append({
                "numero": i + 1,
                "descripcion": descripcion,
                "unidad": unidad,
                "cantidad": cantidad_item,
                "precio_unitario": precio_unitario,
                "valor_venta": valor_venta
            })

        return items


if __name__ == "__main__":
    # Tests
    print("=== Test RUC ===")
    for _ in range(5):
        print(RUCGenerator.generar_ruc())

    print("\n=== Test Monto a Letras ===")
    montos = [1250.50, 10000.00, 999.99, 1.00, 100.00]
    for monto in montos:
        print(f"{monto} -> {MontoLetras.convertir(monto, 'SOLES')}")

    print("\n=== Test Datos Personas ===")
    for _ in range(3):
        print(f"Persona: {DatosPersonas.generar_nombre_persona()}")
        print(f"Empresa: {DatosPersonas.generar_razon_social()}")
        print(f"Dirección: {DatosPersonas.generar_direccion()}")
        print(f"Teléfono: {DatosPersonas.generar_telefono()}")
        print()

    print("=== Test Items ===")
    items = ItemsGenerator.generar_items(5, 'construccion')
    for item in items:
        print(item)
