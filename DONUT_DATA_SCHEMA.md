# 🍩 Esquema de Datos Donut para Facturas Peruanas

**Modelo:** Document Understanding Transformer (Donut)
**Versión:** 1.0
**Fecha:** 2025-01-19
**Propósito:** Definición formal del esquema de datos y validaciones

---

## 🎯 Introducción

Este documento define el **esquema de datos** que Donut debe aprender a generar al procesar facturas peruanas.

### Diferencias con Esquema JSON General

```python
# Esquema JSON General (97 campos)
# - Estructura plana
# - Para integración con BD
# - Todos los campos obligatorios

# Esquema Donut (Flexible)
# - Puede ser jerárquico
# - Optimizado para aprendizaje del modelo
# - Campos opcionales según contexto
```

---

## 📊 Niveles de Complejidad del Esquema

### Nivel 1: Básico (20 campos)

**Uso:** Entrenamiento inicial, POC, validación rápida

```json
{
  "tipo_documento": "string",
  "serie_completa": "string",
  "fecha_emision": "date(YYYY-MM-DD)",
  "moneda": "enum(SOLES|DOLARES AMERICANOS)",

  "emisor": {
    "ruc": "string(11)",
    "razon_social": "string"
  },

  "receptor": {
    "numero_doc": "string(11|8)",
    "razon_social": "string"
  },

  "totales": {
    "subtotal": "float",
    "igv": "float",
    "total": "float"
  },

  "items": [
    {
      "item": "int",
      "descripcion": "string",
      "cantidad": "float",
      "precio_unitario": "float",
      "importe_total": "float"
    }
  ]
}
```

**Ventajas:**
- ✅ Rápido de entrenar
- ✅ Menos errores
- ✅ F1 Score alto (> 0.90)

**Limitaciones:**
- ❌ No captura todos los detalles
- ❌ Requiere post-procesamiento

---

### Nivel 2: Intermedio (50 campos)

**Uso:** Producción estándar, balance entre completitud y performance

```json
{
  "documento": {
    "tipo": "string",
    "serie": "string",
    "numero": "string",
    "fecha_emision": "date",
    "fecha_vencimiento": "date|null",
    "moneda": "enum"
  },

  "emisor": {
    "ruc": "string(11)",
    "razon_social": "string",
    "nombre_comercial": "string|null",
    "direccion": "string",
    "departamento": "string",
    "provincia": "string",
    "distrito": "string",
    "telefono": "string|null",
    "email": "string|null",
    "web": "string|null"
  },

  "receptor": {
    "tipo_doc": "enum(RUC|DNI|CE)",
    "numero_doc": "string",
    "razon_social": "string",
    "direccion": "string",
    "departamento": "string|null",
    "provincia": "string|null",
    "distrito": "string|null",
    "contacto": "string|null"
  },

  "importes": {
    "subtotal": "float",
    "descuento": "float",
    "subtotal_con_descuento": "float",
    "igv": "float",
    "isc": "float|null",
    "otros_cargos": "float",
    "total": "float",
    "detraccion_monto": "float|null",
    "detraccion_porcentaje": "float|null"
  },

  "referencias": {
    "orden_compra": "string|null",
    "guia_remision": "string|null",
    "numero_contrato": "string|null",
    "condicion_pago": "string|null",
    "forma_pago": "string|null"
  },

  "items": [
    {
      "item": "int",
      "codigo": "string|null",
      "descripcion": "string",
      "cantidad": "float",
      "unidad_medida": "string",
      "precio_unitario": "float",
      "valor_venta": "float",
      "tipo_igv": "enum(GRAVADO|EXONERADO|INAFECTO)",
      "igv_item": "float",
      "importe_total": "float",
      "observacion": "string|null"
    }
  ],

  "cuotas": [
    {
      "numero": "int",
      "monto": "float",
      "fecha_vencimiento": "date"
    }
  ]
}
```

**Ventajas:**
- ✅ Balance entre completitud y performance
- ✅ Captura mayoría de casos de uso
- ✅ F1 Score alto (0.85-0.90)

---

### Nivel 3: Completo (97 campos)

**Uso:** Máxima precisión, casos especializados

Ver **GUIA-ESTRUCTURA-JSON-FACTURAS.md** para estructura completa.

**Ventajas:**
- ✅ Máxima completitud
- ✅ No requiere post-procesamiento
- ✅ Captura todos los casos edge

**Limitaciones:**
- ❌ Requiere más datos de entrenamiento (> 2000 facturas)
- ❌ Training más lento
- ❌ F1 Score más bajo inicialmente (0.70-0.80)

---

## 🔧 Tipos de Datos Donut

### Primitivos

```python
data_types = {
    "string": "Texto libre",
    "int": "Número entero",
    "float": "Número decimal (2 decimales)",
    "boolean": "true/false",
    "null": "Valor nulo",
    "date": "YYYY-MM-DD",
    "enum": "Valor de conjunto limitado"
}
```

### Compuestos

```python
compound_types = {
    "object": {
        "tipo": "Objeto anidado",
        "ejemplo": {"campo1": "valor1", "campo2": "valor2"}
    },
    "array": {
        "tipo": "Lista de elementos",
        "ejemplo": [{"item": 1}, {"item": 2}]
    }
}
```

---

## 📏 Validaciones por Tipo

### String

```python
validations = {
    "min_length": 1,
    "max_length": 500,
    "trim": True,  # Eliminar espacios inicio/fin
    "uppercase": False,  # Mantener capitalización original
    "allow_empty": False
}

# Ejemplos válidos
"TURISMO DIAS S.A."  ✓
"FACTURA ELECTRONICA"  ✓

# Ejemplos inválidos
""  ✗ (vacío)
"   "  ✗ (solo espacios)
```

### Números (int/float)

```python
validations = {
    "min": 0,
    "max": 999999999.99,
    "decimals": 2,
    "allow_negative": False,
    "allow_zero": True
}

# Ejemplos válidos
110.0  ✓
0.0  ✓
1234.56  ✓

# Ejemplos inválidos
-10.0  ✗ (negativo)
123.456  ✗ (3 decimales)
"110"  ✗ (string, no número)
```

### Fechas

```python
validations = {
    "format": "YYYY-MM-DD",
    "min_year": 2020,
    "max_year": 2030,
    "allow_future": True
}

# Ejemplos válidos
"2023-11-13"  ✓
"2025-08-20"  ✓

# Ejemplos inválidos
"13/11/2023"  ✗ (formato incorrecto)
"2023-11-13T00:00:00"  ✗ (con hora)
"2019-01-01"  ✗ (año muy antiguo)
```

### Enums

```python
enums = {
    "moneda": ["SOLES", "DOLARES AMERICANOS"],
    "tipo_documento": ["FACTURA ELECTRONICA", "BOLETA ELECTRONICA"],
    "tipo_igv": ["GRAVADO", "EXONERADO", "INAFECTO"],
    "tipo_doc_receptor": ["RUC", "DNI", "CE", "PASAPORTE"],
    "unidad_medida": ["NIU", "UND", "KGM", "MTR", "LTR", "GLN", "DZN"]
}

# Ejemplos válidos
"SOLES"  ✓
"GRAVADO"  ✓

# Ejemplos inválidos
"PEN"  ✗ (debe ser "SOLES")
"S/"  ✗
"gravado"  ✗ (debe ser mayúscula)
```

### RUC (Perú)

```python
validations = {
    "length": 11,
    "pattern": r"^\d{11}$",
    "validate_checksum": True  # Opcional
}

# Ejemplos válidos
"20438637380"  ✓
"20484327948"  ✓

# Ejemplos inválidos
"2043863738"  ✗ (10 dígitos)
"20438637380A"  ✗ (contiene letra)
```

---

## 🔍 Validaciones Estructurales

### Consistencia de Totales

```python
def validate_totals(data):
    """Validar que los totales sean consistentes"""

    # 1. Suma de items debe coincidir con subtotal
    items_sum = sum(item["importe_total"] for item in data["items"])
    assert abs(items_sum - data["totales"]["total"]) < 0.01, \
        "Suma de items no coincide con total"

    # 2. IGV debe ser 18% del subtotal (si gravado)
    if data["items"][0]["tipo_igv"] == "GRAVADO":
        expected_igv = data["totales"]["subtotal"] * 0.18
        assert abs(data["totales"]["igv"] - expected_igv) < 0.01, \
            "IGV no es 18% del subtotal"

    # 3. Total = Subtotal + IGV + Otros cargos - Descuento
    expected_total = (
        data["totales"]["subtotal"]
        + data["totales"]["igv"]
        + data["totales"]["otros_cargos"]
        - data["totales"]["descuento"]
    )
    assert abs(data["totales"]["total"] - expected_total) < 0.01, \
        "Total no coincide con cálculo"

    return True
```

### Consistencia de Items

```python
def validate_items(items):
    """Validar array de items"""

    # 1. Items numerados secuencialmente
    for i, item in enumerate(items, start=1):
        assert item["item"] == i, f"Item {i} mal numerado"

    # 2. Cada item tiene cálculos correctos
    for item in items:
        # cantidad * precio_unitario = valor_venta
        expected_venta = item["cantidad"] * item["precio_unitario"]
        assert abs(item["valor_venta"] - expected_venta) < 0.01, \
            f"Item {item['item']}: valor_venta incorrecto"

        # valor_venta + igv_item = importe_total
        expected_total = item["valor_venta"] + item["igv_item"]
        assert abs(item["importe_total"] - expected_total) < 0.01, \
            f"Item {item['item']}: importe_total incorrecto"

    return True
```

### Consistencia de Fechas

```python
def validate_dates(data):
    """Validar fechas"""

    from datetime import datetime, timedelta

    fecha_emision = datetime.strptime(data["fecha_emision"], "%Y-%m-%d")

    # 1. Fecha vencimiento debe ser posterior a emisión
    if data.get("fecha_vencimiento"):
        fecha_venc = datetime.strptime(data["fecha_vencimiento"], "%Y-%m-%d")
        assert fecha_venc >= fecha_emision, \
            "Fecha vencimiento anterior a emisión"

    # 2. Fechas de cuotas deben ser futuras
    for cuota in data.get("cuotas", []):
        fecha_cuota = datetime.strptime(cuota["fecha_vencimiento"], "%Y-%m-%d")
        assert fecha_cuota >= fecha_emision, \
            f"Cuota {cuota['numero']} con fecha inválida"

    # 3. Cuotas deben estar ordenadas
    fechas_cuotas = [
        datetime.strptime(c["fecha_vencimiento"], "%Y-%m-%d")
        for c in data.get("cuotas", [])
    ]
    assert fechas_cuotas == sorted(fechas_cuotas), \
        "Cuotas no están ordenadas cronológicamente"

    return True
```

---

## 🎯 Métricas de Calidad del Esquema

### Tree Edit Distance (TED)

```python
def calculate_ted(predicted, ground_truth):
    """
    Calcula Tree Edit Distance entre dos JSONs

    Mide cuántas operaciones (insertar, eliminar, modificar)
    se necesitan para transformar un JSON en otro
    """
    from zss import simple_distance, Node

    def json_to_tree(obj, name="root"):
        node = Node(name)
        if isinstance(obj, dict):
            for k, v in obj.items():
                node.addkid(json_to_tree(v, k))
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                node.addkid(json_to_tree(item, f"[{i}]"))
        else:
            node.addkid(Node(str(obj)))
        return node

    tree_pred = json_to_tree(predicted)
    tree_gt = json_to_tree(ground_truth)

    distance = simple_distance(tree_pred, tree_gt)
    return distance
```

### F1 Score por Campo

```python
def calculate_field_f1(predicted, ground_truth):
    """
    Calcula F1 score para cada campo del JSON
    """
    def extract_fields(obj, prefix=""):
        fields = {}
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    fields.update(extract_fields(v, f"{prefix}{k}."))
                else:
                    fields[f"{prefix}{k}"] = v
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                fields.update(extract_fields(item, f"{prefix}[{i}]."))
        return fields

    pred_fields = extract_fields(predicted)
    gt_fields = extract_fields(ground_truth)

    # Calcular TP, FP, FN
    tp = sum(1 for k, v in pred_fields.items() if gt_fields.get(k) == v)
    fp = sum(1 for k in pred_fields if k not in gt_fields or pred_fields[k] != gt_fields[k])
    fn = sum(1 for k in gt_fields if k not in pred_fields)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0
    f1 = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return {
        "f1": f1,
        "precision": precision,
        "recall": recall,
        "tp": tp,
        "fp": fp,
        "fn": fn
    }
```

### Exact Match

```python
def calculate_exact_match(predicted, ground_truth):
    """
    Calcula si el JSON es exactamente igual
    """
    import json

    pred_str = json.dumps(predicted, sort_keys=True)
    gt_str = json.dumps(ground_truth, sort_keys=True)

    return pred_str == gt_str
```

---

## 📊 Evaluación por Tipo de Campo

### Campos Críticos (Peso 3x)

Estos campos son esenciales y deben tener > 95% accuracy:

```python
critical_fields = [
    "tipo_documento",
    "serie_completa",
    "fecha_emision",
    "emisor.ruc",
    "emisor.razon_social",
    "receptor.numero_doc",
    "receptor.razon_social",
    "totales.total",
    "moneda"
]
```

### Campos Importantes (Peso 2x)

Deben tener > 90% accuracy:

```python
important_fields = [
    "totales.subtotal",
    "totales.igv",
    "items[].descripcion",
    "items[].cantidad",
    "items[].precio_unitario",
    "items[].importe_total"
]
```

### Campos Opcionales (Peso 1x)

Deben tener > 70% accuracy:

```python
optional_fields = [
    "emisor.telefono",
    "emisor.email",
    "receptor.contacto",
    "referencias.orden_compra",
    "observaciones"
]
```

### Cálculo de Score Ponderado

```python
def calculate_weighted_score(predictions, ground_truths):
    """
    Calcula score ponderado por importancia de campos
    """
    weights = {
        "critical": 3.0,
        "important": 2.0,
        "optional": 1.0
    }

    scores = {
        "critical": [],
        "important": [],
        "optional": []
    }

    for pred, gt in zip(predictions, ground_truths):
        # Calcular accuracy por categoría
        for category, fields in [
            ("critical", critical_fields),
            ("important", important_fields),
            ("optional", optional_fields)
        ]:
            field_scores = []
            for field_path in fields:
                pred_val = get_nested_value(pred, field_path)
                gt_val = get_nested_value(gt, field_path)
                field_scores.append(1.0 if pred_val == gt_val else 0.0)
            scores[category].append(sum(field_scores) / len(field_scores))

    # Calcular score ponderado final
    weighted_score = (
        weights["critical"] * np.mean(scores["critical"])
        + weights["important"] * np.mean(scores["important"])
        + weights["optional"] * np.mean(scores["optional"])
    ) / sum(weights.values())

    return weighted_score
```

---

## 🔗 Siguiente Paso

Ver script de conversión de datos en la carpeta `scripts/`.

---

**Referencias:**
- JSON Schema: https://json-schema.org/
- Tree Edit Distance: https://arxiv.org/abs/1906.08452
