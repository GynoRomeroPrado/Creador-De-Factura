"""
Generador de facturas ficticias con datos realistas
Versión mejorada con sectores específicos, direcciones reales,
descripciones detalladas y patrones temporales.
"""
import random
from datetime import datetime
from typing import Dict, List, Optional
from .utils import (
    RUCGenerator, MontoLetras, DatosPersonas,
    GeneradorFechas, ItemsGenerator, DatosHotel,
    DatosSeguro, GeneradorDescuentos
)

# Importar nuevos módulos de datos realistas
try:
    from .data.sectores_especificos import (
        obtener_sector_aleatorio,
        obtener_razon_social,
        obtener_productos_sector,
        generar_precio_realista,
        obtener_rango_items_sector,
        SECTORES_ESPECIFICOS
    )
    from .data.direcciones_reales import (
        generar_direccion_realista,
        generar_par_direcciones,
        obtener_distrito_aleatorio
    )
    from .data.descripciones_detalladas import (
        generar_descripcion_producto,
        generar_descripcion_servicio
    )
    from .data.patrones_temporales import (
        generar_fecha_hora_realista,
        obtener_productos_estacionales,
        obtener_factor_precio_estacional,
        generar_ticket_promedio_estacional
    )
    MODO_REALISTA = True
except ImportError as e:
    print(f"⚠️  Advertencia: No se pudieron cargar módulos de datos realistas: {e}")
    print("    Usando modo de generación básico")
    MODO_REALISTA = False


class FacturaGenerator:
    """Genera facturas ficticias con datos coherentes"""

    MONEDAS = {
        "PEN": {"simbolo": "S/", "nombre": "SOLES"},
        "USD": {"simbolo": "$", "nombre": "DOLARES"},
        "EUR": {"simbolo": "€", "nombre": "EUROS"}
    }

    FORMAS_PAGO = [
        "EFECTIVO",
        "TRANSFERENCIA BANCARIA",
        "CHEQUE",
        "DEPOSITO EN CUENTA",
        "CREDITO 30 DIAS",
        "CREDITO 60 DIAS",
        "CREDITO 90 DIAS",
        "Credito"
    ]

    TIPOS_COMPROBANTE = [
        "FACTURA ELECTRÓNICA",
        "FACTURA"
    ]

    TIPOS_FACTURA = [
        "general",          # Factura normal
        "hotel",            # Factura de hotel con check-in/out
        "seguro",           # Factura de seguro/póliza
        "con_descuento",    # Factura con descuentos
        "compra_grande"     # Factura con muchos items (30-50) para múltiples páginas
    ]

    def __init__(self, usar_datos_realistas: bool = True):
        """
        Inicializa el generador de facturas.

        Args:
            usar_datos_realistas: Si True, usa los nuevos módulos de datos realistas
                                  (sectores, direcciones, descripciones, temporalidad)
        """
        self.ruc_gen = RUCGenerator()
        self.datos_gen = DatosPersonas()
        self.fecha_gen = GeneradorFechas()
        self.items_gen = ItemsGenerator()
        self.hotel_gen = DatosHotel()
        self.seguro_gen = DatosSeguro()
        self.desc_gen = GeneradorDescuentos()
        self.usar_datos_realistas = usar_datos_realistas and MODO_REALISTA

        if self.usar_datos_realistas:
            print("✅ Generador configurado con datos realistas (sectores, direcciones, descripciones)")

    def generar_factura(self,
                       categoria_items: Optional[str] = None,
                       num_items: Optional[int] = None,
                       moneda: Optional[str] = None,
                       con_credito: bool = None,
                       tipo_factura: str = None,
                       con_descuento: bool = None) -> Dict:
        """
        Genera una factura completa con todos los datos coherentes

        Args:
            categoria_items: 'construccion', 'comida', 'servicios', 'hoteles', 'combustibles', 'seguros', 'seguridad' o None
            num_items: Número de items (None para aleatorio)
            moneda: 'PEN', 'USD', 'EUR' o None para aleatorio
            con_credito: True/False o None para aleatorio
            tipo_factura: 'general', 'hotel', 'seguro', 'con_descuento' o None para aleatorio
            con_descuento: True/False o None para aleatorio

        Returns:
            Diccionario con todos los datos de la factura
        """
        # Seleccionar tipo de factura si no se especifica
        if tipo_factura is None:
            tipo_factura = random.choice(self.TIPOS_FACTURA)

        # Ajustar categoría y número de items según tipo de factura
        if tipo_factura == 'hotel' and categoria_items is None:
            categoria_items = 'hoteles'
        elif tipo_factura == 'seguro' and categoria_items is None:
            categoria_items = 'seguros'
        elif tipo_factura == 'compra_grande':
            # Para compras grandes, generar muchos items (30-50)
            if num_items is None:
                num_items = random.randint(30, 50)
            # Usar categoría de construcción o mixta para facturas grandes
            if categoria_items is None:
                categoria_items = random.choice(['construccion', 'alimentos', None])

        # Seleccionar moneda
        if moneda is None:
            moneda = random.choice(list(self.MONEDAS.keys()))

        moneda_info = self.MONEDAS[moneda]

        # ============================================================
        # MODO REALISTA: Usar sectores específicos
        # ============================================================
        sector_seleccionado = None
        if self.usar_datos_realistas and tipo_factura != 'hotel' and tipo_factura != 'seguro':
            # Seleccionar sector aleatorio
            sector_seleccionado = obtener_sector_aleatorio()

            # Generar razón social del sector
            razon_social_emisor = obtener_razon_social(sector_seleccionado)

            # Generar direcciones realistas (par emisor-receptor)
            direccion_emisor, direccion_receptor = generar_par_direcciones()

        # ============================================================
        # MODO BÁSICO: Usar generadores tradicionales
        # ============================================================
        else:
            # Generar emisor (con contexto de tipo_factura)
            if tipo_factura == 'hotel':
                razon_social_emisor = self.hotel_gen.generar_nombre_hotel()
            else:
                razon_social_emisor = self.datos_gen.generar_razon_social(tipo_factura=tipo_factura)

            direccion_emisor = self.datos_gen.generar_direccion()
            direccion_receptor = self.datos_gen.generar_direccion()

        # Construir datos de emisor
        emisor = {
            "ruc": self.ruc_gen.generar_ruc(),
            "razon_social": razon_social_emisor,
            "direccion": direccion_emisor,
            "telefono": self.datos_gen.generar_telefono(),
            "email": self._generar_email(razon_social=razon_social_emisor, tipo_factura=tipo_factura)
        }

        # Generar receptor
        razon_social_receptor = self.datos_gen.generar_razon_social()
        receptor = {
            "ruc": self.ruc_gen.generar_ruc(),
            "razon_social": razon_social_receptor,
            "direccion": direccion_receptor,
            "telefono": self.datos_gen.generar_telefono(),
            "email": self._generar_email(razon_social=razon_social_receptor, tipo_factura='general')
        }

        # ============================================================
        # Fecha de emisión (con patrones temporales si disponible)
        # ============================================================
        if self.usar_datos_realistas and sector_seleccionado:
            fecha_str, hora_str = generar_fecha_hora_realista(sector_seleccionado)
            # Convertir a datetime
            fecha_emision = datetime.strptime(fecha_str, '%Y-%m-%d')
        else:
            fecha_emision = self.fecha_gen.generar_fecha_2025()

        # Número de factura
        serie = f"F{random.randint(1, 999):03d}"
        numero = f"{random.randint(1, 999999):06d}"
        numero_factura = f"{serie}-{numero}"

        # Datos específicos según tipo de factura
        datos_hotel = None
        datos_seguro = None

        if tipo_factura == 'hotel':
            datos_hotel = self.hotel_gen.generar_datos_estadia(fecha_emision)

        if tipo_factura == 'seguro':
            datos_seguro = self.seguro_gen.generar_poliza(fecha_emision)

        # Determinar si tiene cargos por item (típico de hoteles)
        con_cargo_item = (tipo_factura == 'hotel')

        # ============================================================
        # Generar items (con descripciones realistas si disponible)
        # ============================================================
        if self.usar_datos_realistas and sector_seleccionado:
            items = self._generar_items_realistas(
                sector=sector_seleccionado,
                num_items=num_items,
                moneda_info=moneda_info,
                fecha_emision=fecha_emision
            )
        else:
            # Modo básico
            items = self.items_gen.generar_items(num_items, categoria_items, con_cargo_item)

        # Calcular subtotales
        if con_cargo_item:
            # Para hoteles, el subtotal es la suma de valores de venta sin IGV
            # Redondear sumas para evitar errores de punto flotante
            subtotal = round(sum(item["valor_venta"] for item in items), 2)
            total_cargos = round(sum(item.get("cargo_item", 0) for item in items), 2)
        else:
            subtotal = round(sum(item["valor_venta"] for item in items), 2)
            total_cargos = 0.00

        # Determinar si tiene descuento
        if con_descuento is None:
            con_descuento = (tipo_factura == 'con_descuento' or random.random() < 0.15)

        descuento = None
        if con_descuento:
            descuento = self.desc_gen.generar_descuento(subtotal)
            subtotal = round(subtotal - descuento["monto"], 2)

        # Determinar si tiene importes no gravados/exonerados
        tiene_exonerado = random.random() < 0.2  # 20% de probabilidad
        tiene_inafecto = random.random() < 0.1   # 10% de probabilidad

        if tiene_exonerado:
            op_exonerada = round(subtotal * random.uniform(0.1, 0.3), 2)
            subtotal = round(subtotal - op_exonerada, 2)
        else:
            op_exonerada = 0.00

        if tiene_inafecto:
            op_inafecta = round(subtotal * random.uniform(0.05, 0.15), 2)
            subtotal = round(subtotal - op_inafecta, 2)
        else:
            op_inafecta = 0.00

        # Calcular IGV (18% en Perú)
        op_gravada = round(subtotal, 2)
        igv = round(op_gravada * 0.18, 2)

        # Otros cargos (opcionales, típicos en algunas facturas)
        otros_cargos = 0.00
        if random.random() < 0.1:  # 10% de probabilidad
            otros_cargos = round(random.uniform(5.00, 50.00), 2)

        # Total
        total = round(op_gravada + igv + op_exonerada + op_inafecta + total_cargos + otros_cargos, 2)

        # Monto en letras
        total_letras = MontoLetras.convertir(total, moneda_info["nombre"])

        # Forma de pago y crédito
        if con_credito is None:
            con_credito = random.random() < 0.4  # 40% a crédito

        if con_credito:
            forma_pago = random.choice([f for f in self.FORMAS_PAGO if "CREDITO" in f or "Credito" in f])
            num_cuotas = random.choice([1, 2, 3, 4, 6])
            monto_cuota = round(total / num_cuotas, 2)

            # Ajustar última cuota para que sume exacto
            cuotas = []
            suma_cuotas = 0
            for i in range(num_cuotas):
                fecha_venc = self.fecha_gen.generar_cuotas(fecha_emision, num_cuotas)[i][1]
                if i < num_cuotas - 1:
                    cuotas.append({
                        "numero": i + 1,
                        "fecha_vencimiento": fecha_venc,
                        "monto": monto_cuota
                    })
                    suma_cuotas += monto_cuota
                else:
                    # Última cuota ajustada
                    cuotas.append({
                        "numero": i + 1,
                        "fecha_vencimiento": fecha_venc,
                        "monto": round(total - suma_cuotas, 2)
                    })
        else:
            forma_pago = random.choice([f for f in self.FORMAS_PAGO if "CREDITO" not in f and "Credito" not in f])
            cuotas = []

        # Generar número de contrato (opcional)
        numero_contrato = None
        if random.random() < 0.3:  # 30% tienen contrato
            numero_contrato = f"CW{random.randint(100000, 999999)}"

        # Periodo facturado (opcional, más común en servicios)
        periodo_facturado = None
        if categoria_items == 'servicios' or random.random() < 0.2:
            mes_inicio = fecha_emision.month
            año = fecha_emision.year
            periodo_facturado = f"{self._nombre_mes(mes_inicio).upper()} {str(año)[2:]}"

        # Tipo de comprobante
        tipo_comprobante = random.choice(self.TIPOS_COMPROBANTE)

        # Observaciones opcionales
        observaciones = None
        if random.random() < 0.3:
            obs_opciones = [
                "Incluye transporte e instalación",
                "Precio sujeto a disponibilidad de stock",
                "Garantía de 12 meses",
                "Válido hasta fin de mes",
                "Producto nacional de primera calidad",
                "CREDITO 15 DIAS",
                "SIRVASE ENTREGAR LA LLAVE A LA RECEPCION / PLEASE LEAVE THE KEY AT THE DESK"
            ]
            observaciones = random.choice(obs_opciones)

        # ============================================================
        # Metadata adicional para modo realista
        # ============================================================
        metadata_realista = {}
        if self.usar_datos_realistas and sector_seleccionado:
            # Seleccionar tipografía aleatoria (se usará en pdf_creator.py)
            tipografias_disponibles = [
                'Courier',       # 35% - térmica/matriz
                'Arial',         # 25% - moderna
                'Helvetica',     # 20% - profesional
                'Times-Roman',   # 10% - tradicional
                'Calibri',       # 7% - moderna (simulada con Helvetica)
                'Consolas',      # 3% - técnica (simulada con Courier)
            ]
            pesos_tipografias = [35, 25, 20, 10, 7, 3]
            tipografia_seleccionada = random.choices(tipografias_disponibles, weights=pesos_tipografias, k=1)[0]

            metadata_realista = {
                "sector": sector_seleccionado,
                "tipografia": tipografia_seleccionada,
                "modo_realista": True,
            }

        factura_data = {
            "tipo_comprobante": tipo_comprobante,
            "tipo_factura": tipo_factura,
            "numero_factura": numero_factura,
            "serie": serie,
            "numero": numero,
            "fecha_emision": fecha_emision,
            "fecha_vencimiento": fecha_emision if not con_credito else cuotas[-1]["fecha_vencimiento"],

            "emisor": emisor,
            "receptor": receptor,

            "moneda": moneda,
            "simbolo_moneda": moneda_info["simbolo"],
            "nombre_moneda": moneda_info["nombre"],

            "items": items,

            "op_gravada": op_gravada,
            "op_exonerada": op_exonerada,
            "op_inafecta": op_inafecta,
            "op_gratuitas": 0.00,  # Operaciones gratuitas
            "igv": igv,
            "total_cargos": total_cargos,
            "otros_cargos": otros_cargos,
            "total": total,
            "total_letras": total_letras,

            "forma_pago": forma_pago,
            "con_credito": con_credito,
            "cuotas": cuotas,

            "numero_contrato": numero_contrato,
            "periodo_facturado": periodo_facturado,
            "observaciones": observaciones,

            # Datos específicos
            "datos_hotel": datos_hotel,
            "datos_seguro": datos_seguro,
            "descuento": descuento,

            # Metadata de modo realista
            **metadata_realista,
        }

        return factura_data

    def _generar_items_realistas(self,
                                 sector: str,
                                 num_items: Optional[int],
                                 moneda_info: Dict,
                                 fecha_emision: datetime) -> List[Dict]:
        """
        Genera items de factura con datos realistas del sector.

        Args:
            sector: Sector del negocio (restaurante, farmacia, etc.)
            num_items: Número de items (None para automático según sector)
            moneda_info: Información de la moneda
            fecha_emision: Fecha de emisión para determinar estacionalidad

        Returns:
            Lista de items con descripciones realistas
        """
        # Determinar número de items según sector si no se especifica
        if num_items is None:
            rango_min, rango_max = obtener_rango_items_sector(sector)
            num_items = random.randint(rango_min, rango_max)

        # Obtener lista de productos del sector
        # Nota: obtener_productos_sector ya devuelve items completos con precios
        productos_base = SECTORES_ESPECIFICOS[sector]['productos']

        # Seleccionar productos aleatorios
        if num_items > len(productos_base):
            productos_seleccionados = random.choices(productos_base, k=num_items)
        else:
            productos_seleccionados = random.sample(productos_base, num_items)

        # Factor de precio estacional
        mes = fecha_emision.month
        factor_estacional = obtener_factor_precio_estacional(mes)

        items = []
        for i, (producto_base, precio_min, precio_max) in enumerate(productos_seleccionados, 1):
            # Generar descripción detallada
            descripcion = generar_descripcion_producto(
                sector=sector,
                producto_base=producto_base,
                incluir_marca=True,
                incluir_presentacion=True,
                incluir_variante=True,
                incluir_especificaciones=True
            )

            # Generar precio realista con estacionalidad
            precio_base = generar_precio_realista(precio_min, precio_max)
            precio_unitario = round(precio_base * factor_estacional, 2)

            # Cantidad (varía según el producto)
            if sector in ['restaurante', 'spa', 'gym', 'odontologia']:
                # Servicios: típicamente 1 unidad
                cantidad = random.choices([1, 2, 3], weights=[70, 20, 10], k=1)[0]
            elif sector in ['supermercado', 'panaderia']:
                # Supermercado: cantidades variadas
                cantidad = random.choices([1, 2, 3, 4, 5, 6, 12], weights=[20, 25, 20, 15, 10, 5, 5], k=1)[0]
            elif sector in ['farmacia']:
                # Farmacia: típicamente 1-3 unidades
                cantidad = random.choices([1, 2, 3], weights=[60, 30, 10], k=1)[0]
            elif sector in ['ferreteria', 'construccion']:
                # Ferretería: cantidades variadas (materiales)
                cantidad = random.choices([1, 2, 5, 10, 20, 50], weights=[30, 25, 20, 15, 7, 3], k=1)[0]
            else:
                # Genérico
                cantidad = random.choices([1, 2, 3, 4, 5], weights=[40, 25, 15, 10, 10], k=1)[0]

            # Unidad de medida
            unidades_sector = SECTORES_ESPECIFICOS.get(sector, {}).get('unidades', ['UND'])
            unidad = random.choice(unidades_sector)

            # Cálculos
            valor_venta = round(precio_unitario * cantidad, 2)
            igv_item = round(valor_venta * 0.18, 2)
            importe_total = round(valor_venta + igv_item, 2)

            item = {
                "numero": i,
                "descripcion": descripcion,
                "unidad": unidad,
                "cantidad": cantidad,
                "precio_unitario": precio_unitario,
                "valor_venta": valor_venta,
                "igv": igv_item,
                "importe_total": importe_total,
                "descuento": 0.00,
            }

            items.append(item)

        return items

    def _generar_email(self, razon_social: str = None, tipo_factura: str = 'general') -> str:
        """
        Genera un email corporativo ficticio coherente con la razón social y tipo de factura

        Args:
            razon_social: Razón social de la empresa
            tipo_factura: Tipo de factura (hotel, seguro, general, etc.)

        Returns:
            Email corporativo realista
        """
        # Prefijos comunes según tipo de factura
        if tipo_factura == 'hotel':
            prefijos = ["reservas", "recepcion", "facturacion", "contacto", "ventas", "info"]
        elif tipo_factura == 'seguro':
            prefijos = ["seguros", "polizas", "siniestros", "facturacion", "contacto", "ventas"]
        else:
            prefijos = ["ventas", "facturacion", "contacto", "info", "administracion", "cobranzas"]

        # Generar dominio basado en la razón social
        if razon_social:
            # Extraer palabras clave de la razón social
            palabras = razon_social.upper().split()

            # Filtrar palabras comunes que no sirven para dominio
            palabras_excluir = {'S.A.', 'S.A.C.', 'S.R.L.', 'E.I.R.L.', 'SAC', 'SRL',
                               'EIRL', 'CIA', 'COMPAÑIA', 'EMPRESA', 'GRUPO', 'CORPORACION',
                               'SOCIEDAD', 'ANONIMA', 'CERRADA', 'LIMITADA', 'DE', 'LA',
                               'EL', 'LOS', 'LAS', 'DEL', 'Y', 'E'}

            palabras_clave = [p.replace('.', '').replace(',', '') for p in palabras
                             if p not in palabras_excluir and len(p) > 2]

            if palabras_clave:
                # Tomar 1-2 palabras clave para el dominio
                if len(palabras_clave) >= 2:
                    dominio_base = ''.join(palabras_clave[:2]).lower()
                else:
                    dominio_base = palabras_clave[0].lower()

                # Limpiar caracteres especiales
                dominio_base = dominio_base.replace('ñ', 'n').replace('á', 'a').replace('é', 'e')
                dominio_base = dominio_base.replace('í', 'i').replace('ó', 'o').replace('ú', 'u')

                # Limitar longitud del dominio
                if len(dominio_base) > 15:
                    dominio_base = dominio_base[:15]

                # Extensiones específicas por tipo
                if tipo_factura == 'hotel':
                    extensiones = ['.com.pe', '.pe', 'hotel.com', 'hotels.pe']
                elif tipo_factura == 'seguro':
                    extensiones = ['.com.pe', '.pe', 'seguros.pe', 'insurance.pe']
                else:
                    extensiones = ['.com.pe', '.pe', '.com', 'corp.pe']

                dominio = f"{dominio_base}{random.choice(extensiones)}"
            else:
                # Fallback a dominios genéricos pero corporativos
                dominio = self._dominio_generico(tipo_factura)
        else:
            dominio = self._dominio_generico(tipo_factura)

        return f"{random.choice(prefijos)}@{dominio}"

    def _dominio_generico(self, tipo_factura: str) -> str:
        """Genera un dominio genérico pero corporativo según tipo de factura"""
        if tipo_factura == 'hotel':
            return random.choice(["hotelcorp.pe", "hospitality.com.pe", "hotelesgroup.pe", "lodging.pe"])
        elif tipo_factura == 'seguro':
            return random.choice(["seguroscorp.pe", "insurance.com.pe", "aseguradoras.pe", "polizas.pe"])
        else:
            return random.choice(["empresa.com.pe", "comercial.pe", "negocios.com.pe", "corp.pe"])

    def _nombre_mes(self, num_mes: int) -> str:
        """Convierte número de mes a nombre"""
        meses = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        return meses[num_mes - 1]

    def generar_multiples(self, cantidad: int, **kwargs) -> List[Dict]:
        """Genera múltiples facturas"""
        facturas = []
        for i in range(cantidad):
            print(f"Generando factura {i+1}/{cantidad}...")
            factura = self.generar_factura(**kwargs)
            facturas.append(factura)
        return facturas


if __name__ == "__main__":
    # Test
    gen = FacturaGenerator()

    print("=== Generando factura de hotel ===")
    factura = gen.generar_factura(tipo_factura='hotel', con_credito=True)

    print(f"\nFactura: {factura['numero_factura']}")
    print(f"Tipo: {factura['tipo_factura']}")
    print(f"Fecha: {factura['fecha_emision'].strftime('%d/%m/%Y')}")
    print(f"Emisor: {factura['emisor']['razon_social']}")

    if factura['datos_hotel']:
        print(f"\n=== Datos de Hotel ===")
        print(f"Check-in: {factura['datos_hotel']['checkin'].strftime('%d/%m/%Y')}")
        print(f"Check-out: {factura['datos_hotel']['checkout'].strftime('%d/%m/%Y')}")
        print(f"Noches: {factura['datos_hotel']['noches']}")
        print(f"Huésped: {factura['datos_hotel']['huesped']}")
        print(f"Reserva: {factura['datos_hotel']['reserva']}")

    print(f"\nItems:")
    for item in factura['items']:
        cargo_texto = f" + Cargo: {factura['simbolo_moneda']}{item.get('cargo_item', 0):.2f}" if 'cargo_item' in item else ""
        print(f"  {item['descripcion']} - {item['cantidad']} {item['unidad']} x {factura['simbolo_moneda']}{item['precio_unitario']:.2f}{cargo_texto}")

    print(f"\nOp. Gravada: {factura['simbolo_moneda']}{factura['op_gravada']:.2f}")
    print(f"IGV (18%): {factura['simbolo_moneda']}{factura['igv']:.2f}")
    if factura['total_cargos'] > 0:
        print(f"Total Cargos: {factura['simbolo_moneda']}{factura['total_cargos']:.2f}")
    print(f"TOTAL: {factura['simbolo_moneda']}{factura['total']:.2f}")
    print(f"SON: {factura['total_letras']}")

    if factura['con_credito']:
        print(f"\nForma de Pago: {factura['forma_pago']}")
        print("Cuotas:")
        for cuota in factura['cuotas']:
            print(f"  Cuota {cuota['numero']}: {factura['simbolo_moneda']}{cuota['monto']:.2f} - Venc: {cuota['fecha_vencimiento'].strftime('%d/%m/%Y')}")
