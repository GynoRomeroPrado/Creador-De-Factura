# ⚠️ IMPORTANTE: Cómo Generar JSONs Correctamente

## 🚨 Si obtienes JSONs con este formato (INCORRECTO):

```json
{
  "tipo_comprobante": "FACTURA ELECTRÓNICA",
  "tipo_factura": "hotel",
  "emisor": {
    "ruc": "20118960689",
    "razon_social": "Radisson Luxury Huancayo"
  },
  "receptor": {
    "ruc": "20651525978"
  },
  "moneda": "EUR",
  "simbolo_moneda": "€"
}
```

## ✅ Es porque NO estás usando `JSONExporter`

---

## 📝 SOLUCIÓN RÁPIDA

### ❌ NO hagas esto:

```python
from src.generator import FacturaGenerator
import json

gen = FacturaGenerator()
factura = gen.generar_factura(tipo_factura='hotel')

# ❌ INCORRECTO - Guarda formato anidado
with open('factura.json', 'w') as f:
    json.dump(factura, f)
```

### ✅ HAZ esto:

```python
from src.generator import FacturaGenerator
from src.json_exporter import JSONExporter

gen = FacturaGenerator()
exporter = JSONExporter(output_dir="mis_facturas")

factura = gen.generar_factura(tipo_factura='hotel')

# ✅ CORRECTO - Guarda formato InvoiceX v5.5
archivo = exporter.exportar_factura(factura)
```

---

## 🎯 Resultado Correcto

Con `JSONExporter` obtendrás:

```json
{
  "tipo_documento": "FACTURA ELECTRONICA",
  "serie_completa": "F254-560363",
  "fecha_emision": "2025-11-12",
  "moneda": "EUROS",
  "emisor_ruc": "20118960689",
  "emisor_razon_social": "Radisson Luxury Huancayo",
  "emisor_direccion": "Av. Venezuela 6854, Bellavista, Huancavelica",
  "emisor_departamento": "Bellavista",
  "emisor_telefono": "01-2642531",
  "receptor_numero_doc": "20651525978",
  "receptor_tipo_doc": "RUC",
  "receptor_razon_social": "Dinámica Academia S.A.",
  "subtotal": 1268.83,
  "igv": 228.39,
  "importe_total": 1725.61,
  "items": [
    {
      "item": 1,
      "codigo": "90111500",
      "descripcion": "ALOJAMIENTO",
      "cantidad": 9.545,
      "unidad_medida": "NIU",
      "precio_unitario": 87.52,
      "valor_venta": 835.38,
      "descuento_item": null,
      "subtotal_item": 835.38,
      "tipo_igv": "GRAVADO",
      "igv_item": 150.37,
      "otro_tributo": 83.54,
      "importe_total_item": 1069.29,
      "lote": null,
      "fecha_vencimiento": null
    }
  ]
}
```

**✅ Estructura plana con 94+ campos**
**✅ Items con 26-27 campos completos**
**✅ Formato InvoiceX v5.5**

---

## 📚 Guías Disponibles

Elige la guía según dónde estés trabajando:

1. **`GUIA_GOOGLE_COLAB.md`** ← Si usas Google Colab
2. **`PROBLEMA_RESUELTO.md`** ← Explicación completa del problema
3. **`COMO_GENERAR_JSON_CORRECTO.md`** ← Guía general de uso
4. **`GUIA-ESTRUCTURA-JSON-FACTURAS.md`** ← Especificación InvoiceX v5.5

---

## 🔍 Verificar tu JSON

Ejecuta esto para verificar que tu JSON es correcto:

```python
import json

with open('tu_factura.json', 'r') as f:
    data = json.load(f)

# Verificaciones
es_correcto = (
    'emisor_ruc' in data and  # Estructura plana
    data.get('moneda') in ['SOLES', 'DOLARES AMERICANOS', 'EUROS'] and
    len(data.get('fecha_emision', '')) == 10  # YYYY-MM-DD
)

print("✅ Formato correcto" if es_correcto else "❌ Formato incorrecto")
```

---

## 🎓 Scripts de Ejemplo

### Generar UNA factura

```bash
python generar_factura_simple.py
```

### Ver la diferencia entre formatos

```bash
python DIFERENCIA_FORMATOS.py
```

### Generar varias facturas de prueba

```bash
python test_json_exporter_corregido.py
```

---

## 💡 Regla de Oro

**SIEMPRE** usa `JSONExporter` o `DatasetExporter` para guardar JSONs.

**NUNCA** uses `json.dump()` directamente con el diccionario del generador.

---

## 📞 ¿Problemas?

1. Lee `PROBLEMA_RESUELTO.md` primero
2. Ejecuta `DIFERENCIA_FORMATOS.py` para ver la diferencia
3. Compara tu JSON con `ejemplo_json_correcto.json`
4. Verifica que uses `JSONExporter` o `DatasetExporter`

---

**¿Usas Google Colab?** → Lee `GUIA_GOOGLE_COLAB.md`

**¿Necesitas ejemplos?** → Mira `facturas_generadas/JSONs_CORREGIDOS/`

**¿Dudas sobre el formato?** → Lee `GUIA-ESTRUCTURA-JSON-FACTURAS.md`

---

**Última actualización:** 2025-01-10
**Formato:** InvoiceX v5.5 (estructura plana con 97 campos)
