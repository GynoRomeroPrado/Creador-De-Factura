# 🍩 Formato de Datos de Entrenamiento para Donut

**Modelo:** Document Understanding Transformer (Donut)
**Versión:** Compatible con naver-clova-ix/donut-base
**Fecha:** 2025-01-19
**Propósito:** Extracción de datos estructurados de facturas peruanas

---

## 📋 ¿Qué es Donut?

**Donut (Document Understanding Transformer)** es un modelo visual transformer que:

- ✅ **NO requiere OCR** - Procesa imágenes directamente
- ✅ **End-to-end** - De imagen a JSON estructurado
- ✅ **Basado en Transformer** - Arquitectura encoder-decoder
- ✅ **Fine-tunable** - Se puede entrenar con datasets específicos
- ✅ **Multi-task** - Soporta diferentes tipos de tareas

### Arquitectura

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Imagen    │ ───▶ │   Swin      │ ───▶ │   BART      │ ───▶  JSON
│  (Factura)  │      │  Transformer│      │  Decoder    │
└─────────────┘      └─────────────┘      └─────────────┘
                      (Encoder)            (Decoder)
```

---

## 📊 Formato de Dataset para Donut

### Estructura de Directorios

```
dataset/
├── train/
│   ├── metadata.jsonl          # Anotaciones de entrenamiento
│   └── images/
│       ├── factura_001.jpg
│       ├── factura_002.jpg
│       └── ...
├── validation/
│   ├── metadata.jsonl
│   └── images/
│       ├── factura_val_001.jpg
│       └── ...
└── test/
    ├── metadata.jsonl
    └── images/
        ├── factura_test_001.jpg
        └── ...
```

### Formato metadata.jsonl

Cada línea del archivo `metadata.jsonl` es un JSON con:

```json
{
  "file_name": "factura_001.jpg",
  "ground_truth": "{\"gt_parse\": {\"tipo_documento\": \"FACTURA ELECTRONICA\", \"serie_completa\": \"F596-00023196\", ...}}"
}
```

**Características:**
- Una línea por documento
- `file_name`: nombre del archivo de imagen
- `ground_truth`: JSON stringificado con estructura específica
- Debe incluir el wrapper `{"gt_parse": {...}}`

---

## 🎯 Formato Ground Truth para Facturas

### Versión Simplificada (Campos Principales)

Para empezar el entrenamiento, usa estos **20 campos críticos**:

```json
{
  "gt_parse": {
    "tipo_documento": "FACTURA ELECTRONICA",
    "serie_completa": "F596-00023196",
    "fecha_emision": "2023-11-13",
    "moneda": "SOLES",
    "emisor_ruc": "20438637380",
    "emisor_razon_social": "TURISMO DIAS S.A.",
    "receptor_numero_doc": "20553327971",
    "receptor_razon_social": "PENTATECH CONSTRUCCION S.A.C",
    "subtotal": 110.0,
    "igv": 0.0,
    "importe_total": 110.0,
    "items": [
      {
        "item": 1,
        "descripcion": "SERVICIO DE TRANSPORTE",
        "cantidad": 1.0,
        "precio_unitario": 110.0,
        "valor_venta": 110.0,
        "tipo_igv": "EXONERADO",
        "igv_item": 0.0,
        "importe_total_item": 110.0
      }
    ]
  }
}
```

### Versión Completa (97 Campos)

Para entrenamiento avanzado, usa la estructura completa:

```json
{
  "gt_parse": {
    "tipo_documento": "FACTURA ELECTRONICA",
    "serie_completa": "F020-00051515",
    "fecha_emision": "2025-08-20",
    "fecha_vencimiento": "2025-09-19",
    "moneda": "DOLARES AMERICANOS",

    "emisor_ruc": "20484327948",
    "emisor_razon_social": "INMOBILIARIA Y SERVICIOS MASARIS S.A.C.",
    "emisor_nombre_comercial": "COSTA DEL SOL HOTELES",
    "emisor_direccion": "JR. CRUZ DE PIEDRA 707",
    "emisor_sucursal": "Costa del Sol Wyndham Cajamarca",
    "emisor_departamento": "CAJAMARCA",
    "emisor_provincia": "CAJAMARCA",
    "emisor_distrito": "CAJAMARCA",
    "emisor_ubigeo": null,
    "emisor_codigo_postal": null,
    "emisor_telefono": null,
    "emisor_email": null,
    "emisor_web": null,
    "emisor_codigo_establecimiento": null,

    "receptor_numero_doc": "20137291313",
    "receptor_tipo_doc": "RUC",
    "receptor_razon_social": "MINERA YANACOCHA S.R.L.",
    "receptor_nombre_comercial": null,
    "receptor_direccion": "AV. SANTA CRUZ NRO. 120",
    "receptor_contacto": "FRASER VILLABLANCA,CRISTIAN ALEJANDRO",
    "receptor_departamento": "LIMA",
    "receptor_provincia": "LIMA",
    "receptor_distrito": "SAN ISIDRO",
    "receptor_ubigeo": null,
    "receptor_codigo_postal": null,
    "receptor_telefono": null,
    "receptor_email": null,
    "receptor_sucursal": null,

    "subtotal": 120.44,
    "descuento": 0.0,
    "subtotal_con_descuento": 120.44,
    "igv": 21.68,
    "isc": null,
    "otros_cargos": 12.04,
    "importe_total": 154.17,

    "items": [
      {
        "item": 1,
        "codigo": "90111500",
        "descripcion": "ALIMENTACION",
        "cantidad": 1.0,
        "unidad_medida": "NIU",
        "precio_unitario": 8.73,
        "valor_venta": 8.73,
        "tipo_igv": "GRAVADO",
        "igv_item": 1.57,
        "importe_total_item": 10.3
      },
      {
        "item": 2,
        "codigo": "90111500",
        "descripcion": "ALOJAMIENTO",
        "cantidad": 2.0,
        "unidad_medida": "NIU",
        "precio_unitario": 55.86,
        "valor_venta": 111.72,
        "tipo_igv": "GRAVADO",
        "igv_item": 20.11,
        "importe_total_item": 131.83,
        "observacion_item": "CheckIn: 18-08-2025. CheckOut: 20-08-2025"
      }
    ],

    "cuotas": [
      {
        "numero": 1,
        "monto": 154.17,
        "fecha_vencimiento": "2025-09-19"
      }
    ]
  }
}
```

---

## 🔧 Reglas de Preprocesamiento

### 1. Imágenes

```python
# Configuración recomendada
IMAGE_SIZE = (1280, 960)  # Ancho x Alto
FORMAT = "RGB"
EXTENSION = ".jpg"  # o .png
DPI = 150  # mínimo recomendado
```

**Transformaciones:**
- Redimensionar manteniendo aspect ratio
- Padding para alcanzar tamaño objetivo
- Normalización de colores
- Convertir PDFs a imágenes (una página por imagen)

### 2. Texto (Ground Truth)

```python
# Normalización de campos
- Fechas: formato YYYY-MM-DD
- Números: float sin separadores de miles
- Moneda: texto completo ("SOLES", "DOLARES AMERICANOS")
- Null: usar null JSON, NO strings vacíos
- Booleanos: true/false en minúsculas
```

### 3. Tokenización Especial

Donut usa tokens especiales para estructurar la salida:

```
<s_tipo_documento>FACTURA ELECTRONICA</s_tipo_documento>
<s_serie_completa>F596-00023196</s_serie_completa>
<s_fecha_emision>2023-11-13</s_fecha_emision>
```

**Importante:** El modelo aprende a generar estos tokens automáticamente.

---

## 📝 Ejemplo Completo de metadata.jsonl

```jsonl
{"file_name": "factura_001.jpg", "ground_truth": "{\"gt_parse\": {\"tipo_documento\": \"FACTURA ELECTRONICA\", \"serie_completa\": \"F596-00023196\", \"fecha_emision\": \"2023-11-13\", \"moneda\": \"SOLES\", \"emisor_ruc\": \"20438637380\", \"emisor_razon_social\": \"TURISMO DIAS S.A.\", \"receptor_numero_doc\": \"20553327971\", \"receptor_razon_social\": \"PENTATECH CONSTRUCCION S.A.C\", \"subtotal\": 110.0, \"igv\": 0.0, \"importe_total\": 110.0, \"items\": [{\"item\": 1, \"descripcion\": \"SERVICIO DE TRANSPORTE\", \"cantidad\": 1.0, \"precio_unitario\": 110.0, \"valor_venta\": 110.0, \"tipo_igv\": \"EXONERADO\", \"igv_item\": 0.0, \"importe_total_item\": 110.0}]}}"}
{"file_name": "factura_002.jpg", "ground_truth": "{\"gt_parse\": {\"tipo_documento\": \"FACTURA ELECTRONICA\", \"serie_completa\": \"F020-00051515\", \"fecha_emision\": \"2025-08-20\", \"moneda\": \"DOLARES AMERICANOS\", \"emisor_ruc\": \"20484327948\", \"emisor_razon_social\": \"INMOBILIARIA Y SERVICIOS MASARIS S.A.C.\", \"receptor_numero_doc\": \"20137291313\", \"receptor_razon_social\": \"MINERA YANACOCHA S.R.L.\", \"subtotal\": 120.44, \"igv\": 21.68, \"importe_total\": 154.17, \"items\": [{\"item\": 1, \"descripcion\": \"ALIMENTACION\", \"cantidad\": 1.0, \"precio_unitario\": 8.73, \"valor_venta\": 8.73, \"tipo_igv\": \"GRAVADO\", \"igv_item\": 1.57, \"importe_total_item\": 10.3}, {\"item\": 2, \"descripcion\": \"ALOJAMIENTO\", \"cantidad\": 2.0, \"precio_unitario\": 55.86, \"valor_venta\": 111.72, \"tipo_igv\": \"GRAVADO\", \"igv_item\": 20.11, \"importe_total_item\": 131.83}]}}"}
```

---

## 🎯 Splits Recomendados

Para un dataset de facturas:

```python
TRAIN_RATIO = 0.80      # 80% entrenamiento
VALIDATION_RATIO = 0.10 # 10% validación
TEST_RATIO = 0.10       # 10% prueba

# Ejemplo con 1000 facturas:
# - train: 800 facturas
# - validation: 100 facturas
# - test: 100 facturas
```

**Estrategia de Split:**
- Aleatorio con seed fijo para reproducibilidad
- Balancear tipos de facturas (hotel, general, seguros, etc.)
- Balancear monedas (soles, dólares)
- Balancear operaciones (gravadas, exoneradas, inafectas)

---

## ⚡ Optimizaciones de Performance

### 1. Data Augmentation

```python
augmentations = [
    "rotation": (-5, 5),          # Rotación ligera
    "brightness": (0.8, 1.2),     # Variación de brillo
    "contrast": (0.8, 1.2),       # Variación de contraste
    "noise": "gaussian",          # Ruido gaussiano
    "blur": (0, 2),               # Desenfoque ligero
    "perspective": True           # Transformación perspectiva
]
```

### 2. Campos Jerárquicos

Para campos complejos como `items`, usa sub-estructuras:

```json
{
  "items": [
    {
      "item": 1,
      "basic": {
        "descripcion": "...",
        "cantidad": 1.0
      },
      "pricing": {
        "precio_unitario": 110.0,
        "valor_venta": 110.0
      },
      "taxes": {
        "tipo_igv": "EXONERADO",
        "igv_item": 0.0
      }
    }
  ]
}
```

### 3. Multi-Task Learning

Entrena el modelo para múltiples tareas:

```python
tasks = [
    "invoice_parsing",      # Extracción completa
    "header_extraction",    # Solo cabecera
    "items_extraction",     # Solo items
    "totals_extraction"     # Solo totales
]
```

---

## 🚨 Validaciones Críticas

Antes de usar un JSON como ground truth, validar:

```python
validations = {
    "estructura": [
        "✓ Tiene campo gt_parse",
        "✓ Todos los campos obligatorios presentes",
        "✓ Arrays items y cuotas presentes"
    ],
    "formatos": [
        "✓ Fechas en formato YYYY-MM-DD",
        "✓ Números como float/int, no strings",
        "✓ Moneda en texto completo",
        "✓ Campos vacíos como null"
    ],
    "consistencia": [
        "✓ Suma items = subtotal",
        "✓ subtotal * 1.18 = total (si gravado)",
        "✓ Items numerados secuencialmente"
    ]
}
```

---

## 📊 Métricas de Evaluación

Para medir performance del modelo:

```python
metrics = {
    "Tree Edit Distance (TED)": "Mide similitud estructural",
    "F1-Score por campo": "Precisión individual de campos",
    "Exact Match": "Coincidencia exacta del JSON completo",
    "ANLS (Average Normalized Levenshtein Similarity)": "Similitud de texto"
}
```

---

## 🔗 Siguiente Paso

Ver **DONUT_TASK_PROMPTS.md** para aprender a definir prompts y tareas específicas.

---

**Referencias:**
- Paper original: [OCR-free Document Understanding Transformer](https://arxiv.org/abs/2111.15664)
- Modelo base: `naver-clova-ix/donut-base`
- Hugging Face: https://huggingface.co/naver-clova-ix/donut-base
