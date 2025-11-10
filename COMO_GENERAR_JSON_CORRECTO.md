# Cómo Generar JSON con Formato Correcto InvoiceX v5.5

## El Problema que Tenías

Antes, el sistema generaba JSONs con **estructura anidada** (incorrecto):

```json
{
  "tipo_comprobante": "FACTURA ELECTRÓNICA",
  "emisor": {
    "ruc": "20484327948",
    "razon_social": "EMPRESA S.A."
  },
  "receptor": {
    "ruc": "20137291313",
    "razon_social": "CLIENTE S.A."
  },
  "moneda": "PEN",
  "simbolo_moneda": "S/",
  "items": [...]
}
```

## La Solución

Ahora el sistema genera JSONs con **estructura plana** (correcto) según InvoiceX v5.5:

```json
{
  "tipo_documento": "FACTURA ELECTRONICA",
  "serie_completa": "F020-00051515",
  "fecha_emision": "2025-08-20",
  "fecha_vencimiento": "2025-09-19",
  "moneda": "DOLARES AMERICANOS",
  "emisor_ruc": "20484327948",
  "emisor_razon_social": "INMOBILIARIA Y SERVICIOS MASARIS S.A.C.",
  "emisor_direccion": "JR. CRUZ DE PIEDRA 707 CAJAMARCA",
  "receptor_numero_doc": "20137291313",
  "receptor_tipo_doc": "RUC",
  "receptor_razon_social": "MINERA YANACOCHA S.R.L.",
  "receptor_direccion": "AV. SANTA CRUZ NRO. 601 LIMA",
  "subtotal": 120.44,
  "igv": 21.68,
  "importe_total": 154.17,
  "items": [...],
  "cuotas": [...]
}
```

## Cómo Generar Facturas con Formato Correcto

### Opción 1: Usar el script de dataset (RECOMENDADO)

Este script genera facturas en el formato correcto automáticamente:

```bash
python generar_dataset.py --cantidad 10
```

Esto crea:
- JSONs en formato InvoiceX v5.5 (estructura plana, 97 campos)
- PDFs de las facturas
- Estructura organizada en carpetas

### Opción 2: Generar un ejemplo de prueba

Para ver un ejemplo del formato correcto:

```bash
python test_json_corregido.py
```

Esto genera el archivo `ejemplo_json_correcto.json` con la estructura completa.

### Opción 3: Código Python directo

```python
from src.generator import FacturaGenerator
from src.dataset_exporter import DatasetExporter

# Generar factura
gen = FacturaGenerator()
factura = gen.generar_factura(tipo_factura='hotel', con_credito=True)

# Convertir a formato InvoiceX v5.5
exporter = DatasetExporter()
json_correcto = exporter.convertir_factura_a_anotacion(factura)

# Guardar
import json
with open('mi_factura.json', 'w', encoding='utf-8') as f:
    json.dump(json_correcto, f, indent=2, ensure_ascii=False)
```

## Características del Formato Correcto

✅ **97 campos base** en nivel raíz
✅ **Estructura plana** (NO objetos anidados)
✅ **Prefijos** `emisor_` y `receptor_` para campos relacionados
✅ **Fechas** en formato `YYYY-MM-DD` (sin hora)
✅ **Moneda** normalizada: `SOLES` o `DOLARES AMERICANOS` (no símbolos)
✅ **Items** con 26 campos cada uno
✅ **Cuotas** para facturas a crédito

## Diferencias Clave

| Campo | ❌ Formato Viejo | ✅ Formato Correcto |
|-------|-----------------|-------------------|
| Tipo | `tipo_comprobante` | `tipo_documento` |
| Serie | `numero_factura` | `serie_completa` |
| Fecha | `2025-08-20T00:00:00` | `2025-08-20` |
| Moneda | `USD` o `$` | `DOLARES AMERICANOS` |
| Emisor | `emisor: { ruc: "..." }` | `emisor_ruc: "..."` |
| Receptor | `receptor: { ruc: "..." }` | `receptor_numero_doc: "..."` |
| Items | 6-10 campos | 26 campos completos |
| Total | `total` | `importe_total` |

## Validación

Para validar que un JSON está correcto, verifica:

1. **Estructura plana**: No debe tener objetos anidados como `emisor: {}`
2. **97 campos base**: Todos los campos del nivel raíz
3. **Items completos**: Cada item debe tener exactamente 26 campos
4. **Formato de fechas**: `YYYY-MM-DD` sin hora
5. **Moneda normalizada**: `SOLES` o `DOLARES AMERICANOS`

## Ejemplo Completo

Ver archivo: `ejemplo_json_correcto.json` (generado con `test_json_corregido.py`)

Este archivo muestra la estructura completa con:
- 94 campos raíz
- 10 items con 26 campos cada uno
- Formato correcto de fechas
- Moneda normalizada
- Estructura plana

## Documentación Oficial

Para más detalles sobre la estructura, ver:
- `GUIA-ESTRUCTURA-JSON-FACTURAS.md` - Especificación completa InvoiceX v5.5
- Archivos de ejemplo en `Datos extraidos de Originales/`
