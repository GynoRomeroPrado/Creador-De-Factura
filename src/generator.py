"""
Generador de facturas ficticias
"""
import random
from datetime import datetime
from typing import Dict, List, Optional
from .utils import (
    RUCGenerator, MontoLetras, DatosPersonas,
    GeneradorFechas, ItemsGenerator
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
        "CREDITO 90 DIAS"
    ]

    TIPOS_COMPROBANTE = [
        "FACTURA ELECTRÓNICA",
        "FACTURA"
    ]

    def __init__(self):
        self.ruc_gen = RUCGenerator()
        self.datos_gen = DatosPersonas()
        self.fecha_gen = GeneradorFechas()
        self.items_gen = ItemsGenerator()

    def generar_factura(self,
                       categoria_items: Optional[str] = None,
                       num_items: Optional[int] = None,
                       moneda: Optional[str] = None,
                       con_credito: bool = None) -> Dict:
        """
        Genera una factura completa con todos los datos coherentes

        Args:
            categoria_items: 'construccion', 'comida', 'servicios' o None para mixto
            num_items: Número de items (None para aleatorio)
            moneda: 'PEN', 'USD', 'EUR' o None para aleatorio
            con_credito: True/False o None para aleatorio

        Returns:
            Diccionario con todos los datos de la factura
        """
        # Seleccionar moneda
        if moneda is None:
            moneda = random.choice(list(self.MONEDAS.keys()))

        moneda_info = self.MONEDAS[moneda]

        # Generar emisor
        emisor = {
            "ruc": self.ruc_gen.generar_ruc(),
            "razon_social": self.datos_gen.generar_razon_social(),
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
        serie = f"F{random.randint(1, 999):03d}"
        numero = f"{random.randint(1, 999999):06d}"
        numero_factura = f"{serie}-{numero}"

        # Generar items
        items = self.items_gen.generar_items(num_items, categoria_items)

        # Calcular subtotales
        subtotal = sum(item["valor_venta"] for item in items)

        # Determinar si tiene importes no gravados/exonerados
        tiene_exonerado = random.random() < 0.2  # 20% de probabilidad
        tiene_inafecto = random.random() < 0.1   # 10% de probabilidad

        if tiene_exonerado:
            op_exonerada = round(subtotal * random.uniform(0.1, 0.3), 2)
            subtotal -= op_exonerada
        else:
            op_exonerada = 0.00

        if tiene_inafecto:
            op_inafecta = round(subtotal * random.uniform(0.05, 0.15), 2)
            subtotal -= op_inafecta
        else:
            op_inafecta = 0.00

        # Calcular IGV (18% en Perú)
        op_gravada = subtotal
        igv = round(op_gravada * 0.18, 2)
        total = round(op_gravada + igv + op_exonerada + op_inafecta, 2)

        # Monto en letras
        total_letras = MontoLetras.convertir(total, moneda_info["nombre"])

        # Forma de pago y crédito
        if con_credito is None:
            con_credito = random.random() < 0.4  # 40% a crédito

        if con_credito:
            forma_pago = random.choice([f for f in self.FORMAS_PAGO if "CREDITO" in f])
            num_cuotas = random.choice([2, 3, 4, 6])
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
            forma_pago = random.choice([f for f in self.FORMAS_PAGO if "CREDITO" not in f])
            cuotas = []

        # Generar número de contrato (opcional)
        numero_contrato = None
        if random.random() < 0.3:  # 30% tienen contrato
            numero_contrato = f"CTR-{random.randint(1000, 9999)}-{fecha_emision.year}"

        # Periodo facturado (opcional, más común en servicios)
        periodo_facturado = None
        if categoria_items == 'servicios' or random.random() < 0.2:
            mes_inicio = fecha_emision.month
            año = fecha_emision.year
            periodo_facturado = f"{self._nombre_mes(mes_inicio)} {año}"

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
                "Producto nacional de primera calidad"
            ]
            observaciones = random.choice(obs_opciones)

        return {
            "tipo_comprobante": tipo_comprobante,
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
            "igv": igv,
            "total": total,
            "total_letras": total_letras,

            "forma_pago": forma_pago,
            "con_credito": con_credito,
            "cuotas": cuotas,

            "numero_contrato": numero_contrato,
            "periodo_facturado": periodo_facturado,
            "observaciones": observaciones
        }

    def _generar_email(self) -> str:
        """Genera un email corporativo ficticio"""
        dominios = ["empresa.com", "corp.pe", "negocio.com.pe", "comercial.pe"]
        prefijos = ["ventas", "facturacion", "contacto", "info", "administracion"]
        return f"{random.choice(prefijos)}@{random.choice(dominios)}"

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

    print("=== Generando factura de construcción ===")
    factura = gen.generar_factura(categoria_items='construccion', con_credito=True)

    print(f"\nFactura: {factura['numero_factura']}")
    print(f"Fecha: {factura['fecha_emision'].strftime('%d/%m/%Y')}")
    print(f"Emisor: {factura['emisor']['razon_social']}")
    print(f"RUC: {factura['emisor']['ruc']}")
    print(f"Cliente: {factura['receptor']['razon_social']}")
    print(f"RUC: {factura['receptor']['ruc']}")
    print(f"\nItems:")
    for item in factura['items']:
        print(f"  {item['descripcion']} - {item['cantidad']} {item['unidad']} x {factura['simbolo_moneda']}{item['precio_unitario']:.2f}")
    print(f"\nOp. Gravada: {factura['simbolo_moneda']}{factura['op_gravada']:.2f}")
    print(f"IGV (18%): {factura['simbolo_moneda']}{factura['igv']:.2f}")
    print(f"TOTAL: {factura['simbolo_moneda']}{factura['total']:.2f}")
    print(f"SON: {factura['total_letras']}")

    if factura['con_credito']:
        print(f"\nForma de Pago: {factura['forma_pago']}")
        print("Cuotas:")
        for cuota in factura['cuotas']:
            print(f"  Cuota {cuota['numero']}: {factura['simbolo_moneda']}{cuota['monto']:.2f} - Venc: {cuota['fecha_vencimiento'].strftime('%d/%m/%Y')}")
