"""
Generador de facturas ficticias
"""
import random
from datetime import datetime
from typing import Dict, List, Optional
from .utils import (
    RUCGenerator, MontoLetras, DatosPersonas,
    GeneradorFechas, ItemsGenerator, DatosHotel,
    DatosSeguro, GeneradorDescuentos, DatosRestaurante,
    DatosTransporte, DatosServicios
)


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
        "compra_grande",    # Factura con muchos items (30-50) para múltiples páginas
        "restaurante",      # Factura de consumo en restaurante
        "transporte",       # Factura de transporte de carga/pasajeros
        "servicios_profesionales" # Factura por honorarios/servicios
    ]

    def __init__(self):
        self.ruc_gen = RUCGenerator()
        self.datos_gen = DatosPersonas()
        self.fecha_gen = GeneradorFechas()
        self.items_gen = ItemsGenerator()
        self.hotel_gen = DatosHotel()
        self.seguro_gen = DatosSeguro()
        self.desc_gen = GeneradorDescuentos()
        self.rest_gen = DatosRestaurante()
        self.trans_gen = DatosTransporte()
        self.serv_gen = DatosServicios()

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
        elif tipo_factura == 'restaurante' and categoria_items is None:
            categoria_items = 'restaurante'
        elif tipo_factura == 'transporte' and categoria_items is None:
            categoria_items = 'transporte'
        elif tipo_factura == 'servicios_profesionales' and categoria_items is None:
            categoria_items = 'servicios'

        # Seleccionar moneda
        if moneda is None:
            moneda = random.choice(list(self.MONEDAS.keys()))

        moneda_info = self.MONEDAS[moneda]

        # Generar emisor (ahora con contexto de tipo_factura)
        if tipo_factura == 'hotel':
            razon_social_emisor = self.hotel_gen.generar_nombre_hotel()
        else:
            razon_social_emisor = self.datos_gen.generar_razon_social(tipo_factura=tipo_factura)

        emisor = {
            "ruc": self.ruc_gen.generar_ruc(),
            "razon_social": razon_social_emisor,
            "direccion": self.datos_gen.generar_direccion(),
            "telefono": self.datos_gen.generar_telefono(),
            "email": self._generar_email()
        }

        # Generar receptor
        receptor = {
            "ruc": self.ruc_gen.generar_ruc(),
            "razon_social": self.datos_gen.generar_razon_social(),
            "direccion": self.datos_gen.generar_direccion(),
            "telefono": self.datos_gen.generar_telefono(),
            "email": self._generar_email()
        }

        # Fecha de emisión
        fecha_emision = self.fecha_gen.generar_fecha_2025()

        # Número de factura
        serie_prefix = random.choice(['F', 'FE', 'E', 'FA'])
        serie = f"{serie_prefix}{random.randint(1, 999):03d}"
        numero = f"{random.randint(1, 999999):06d}"
        numero_factura = f"{serie}-{numero}"

        # Datos específicos según tipo de factura
        datos_hotel = None
        datos_seguro = None

        if tipo_factura == 'hotel':
            datos_hotel = self.hotel_gen.generar_datos_estadia(fecha_emision)

        if tipo_factura == 'seguro':
            datos_seguro = self.seguro_gen.generar_poliza(fecha_emision)

        # Datos nuevos
        datos_restaurante = None
        datos_transporte = None
        datos_servicios = None

        if tipo_factura == 'restaurante':
            datos_restaurante = self.rest_gen.generar_datos_restaurante()
        
        if tipo_factura == 'transporte':
            datos_transporte = self.trans_gen.generar_datos_transporte()
            
        if tipo_factura == 'servicios_profesionales':
            datos_servicios = self.serv_gen.generar_datos_servicio()

        # Determinar si tiene cargos por item (típico de hoteles)
        con_cargo_item = (tipo_factura == 'hotel')

        # Generar items
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
            "datos_restaurante": datos_restaurante,
            "datos_transporte": datos_transporte,
            "datos_servicios": datos_servicios,
            "datos_servicios": datos_servicios,
            "descuento": descuento,
            "industria": self._determinar_industria(tipo_factura, categoria_items),
        }

        return factura_data

    def _generar_email(self) -> str:
        """Genera un email corporativo ficticio"""
        dominios = ["empresa.com", "corp.pe", "negocio.com.pe", "comercial.pe", "hotel.com.pe"]
        prefijos = ["ventas", "facturacion", "contacto", "info", "administracion", "reservas"]
        return f"{random.choice(prefijos)}@{random.choice(dominios)}"

    def _nombre_mes(self, num_mes: int) -> str:
        """Convierte número de mes a nombre"""
        meses = [
            "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
            "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
        ]
        return meses[num_mes - 1]

    def _determinar_industria(self, tipo_factura, categoria_items):
        """Determina el tipo de industria para el logo"""
        if tipo_factura == 'hotel': return 'hotel'
        if tipo_factura == 'restaurante': return 'restaurante'
        if tipo_factura == 'transporte': return 'transporte'
        
        # Mapeo por categoría de items
        if categoria_items == 'construccion': return 'construccion'
        if categoria_items == 'tech': return 'tech'
        if categoria_items == 'comida': return 'restaurante'
        
        return 'general'

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
