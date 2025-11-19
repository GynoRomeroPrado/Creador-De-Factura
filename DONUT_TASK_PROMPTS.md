# 🍩 Task Prompts para Donut - Facturas Peruanas

**Modelo:** Document Understanding Transformer (Donut)
**Versión:** Compatible con naver-clova-ix/donut-base
**Fecha:** 2025-01-19
**Propósito:** Definición de tareas y prompts para extracción de facturas

---

## 🎯 ¿Qué son los Task Prompts?

Los **task prompts** son instrucciones que le indican a Donut **qué tipo de información extraer** del documento.

### Diferencia con Modelos de Lenguaje

```python
# ❌ INCORRECTO - No es un LLM con instrucciones en lenguaje natural
prompt = "Por favor extrae todos los datos de esta factura"

# ✅ CORRECTO - Es un token especial de tarea
task_prompt = "<s_invoice_peru>"
```

**Características:**
- Son **tokens especiales** aprendidos durante el entrenamiento
- Definen el **formato de salida** esperado
- Permiten **multi-task learning** (un modelo, varias tareas)
- Se colocan **al inicio** de la secuencia de decoder

---

## 📋 Task Prompts Definidos para Facturas Peruanas

### 1. Extracción Completa de Factura

**Task Prompt:** `<s_invoice_peru>`

**Descripción:** Extrae todos los 97 campos + items + cuotas

**Uso:**
```python
from transformers import DonutProcessor, VisionEncoderDecoderModel

processor = DonutProcessor.from_pretrained("model_path")
model = VisionEncoderDecoderModel.from_pretrained("model_path")

# Preparar imagen
pixel_values = processor(image, return_tensors="pt").pixel_values

# Generar con task prompt
task_prompt = "<s_invoice_peru>"
decoder_input_ids = processor.tokenizer(
    task_prompt,
    add_special_tokens=False,
    return_tensors="pt"
).input_ids

# Inferencia
outputs = model.generate(
    pixel_values,
    decoder_input_ids=decoder_input_ids,
    max_length=model.decoder.config.max_position_embeddings,
    early_stopping=True,
    pad_token_id=processor.tokenizer.pad_token_id,
    eos_token_id=processor.tokenizer.eos_token_id,
    use_cache=True,
    num_beams=1,
    bad_words_ids=[[processor.tokenizer.unk_token_id]],
    return_dict_in_generate=True,
)

# Decodificar resultado
sequence = processor.batch_decode(outputs.sequences)[0]
result = processor.token2json(sequence)
```

**Salida Esperada:**
```json
{
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
  "items": [...],
  "cuotas": [...]
}
```

---

### 2. Extracción Solo Cabecera

**Task Prompt:** `<s_invoice_header>`

**Descripción:** Extrae solo información del encabezado (sin items ni cuotas)

**Campos Incluidos:**
```python
header_fields = [
    "tipo_documento",
    "serie_completa",
    "fecha_emision",
    "fecha_vencimiento",
    "moneda",
    "emisor_ruc",
    "emisor_razon_social",
    "emisor_direccion",
    "receptor_numero_doc",
    "receptor_razon_social",
    "receptor_direccion"
]
```

**Uso:**
```python
task_prompt = "<s_invoice_header>"
```

**Ventajas:**
- Más rápido (menos tokens generados)
- Útil para clasificación de documentos
- Ideal para validación inicial

---

### 3. Extracción Solo Items

**Task Prompt:** `<s_invoice_items>`

**Descripción:** Extrae solo el array de items/productos

**Salida Esperada:**
```json
{
  "items": [
    {
      "item": 1,
      "codigo": "90111500",
      "descripcion": "SERVICIO DE TRANSPORTE",
      "cantidad": 1.0,
      "unidad_medida": "NIU",
      "precio_unitario": 110.0,
      "valor_venta": 110.0,
      "tipo_igv": "EXONERADO",
      "igv_item": 0.0,
      "importe_total_item": 110.0
    }
  ]
}
```

**Uso:**
```python
task_prompt = "<s_invoice_items>"
```

---

### 4. Extracción Solo Totales

**Task Prompt:** `<s_invoice_totals>`

**Descripción:** Extrae solo campos de importes y tributos

**Campos Incluidos:**
```python
totals_fields = [
    "subtotal",
    "descuento",
    "subtotal_con_descuento",
    "igv",
    "isc",
    "otros_cargos",
    "importe_total",
    "detraccion_monto",
    "detraccion_porcentaje"
]
```

**Uso:**
```python
task_prompt = "<s_invoice_totals>"
```

---

### 5. Extracción Tipo Hotel

**Task Prompt:** `<s_invoice_hotel>`

**Descripción:** Extracción especializada para facturas de hoteles

**Campos Adicionales:**
```python
hotel_fields = [
    "referencia_1",  # Número de reserva
    "referencia_2",  # Código de grupo
    "receptor_contacto",  # Huésped
    "items[].observacion_item"  # Check-in/Check-out
]
```

**Ejemplo de Salida:**
```json
{
  "tipo_documento": "FACTURA ELECTRONICA",
  "serie_completa": "F020-00051515",
  "emisor_razon_social": "COSTA DEL SOL HOTELES",
  "receptor_contacto": "FRASER VILLABLANCA,CRISTIAN ALEJANDRO",
  "referencia_1": "Reserva: 8806/2025",
  "referencia_2": "Código de Grupo: 4108",
  "items": [
    {
      "item": 1,
      "descripcion": "ALIMENTACION",
      "cantidad": 1.0,
      "precio_unitario": 8.73,
      "importe_total_item": 10.3
    },
    {
      "item": 2,
      "descripcion": "ALOJAMIENTO",
      "cantidad": 2.0,
      "precio_unitario": 55.86,
      "importe_total_item": 131.83,
      "observacion_item": "CheckIn: 18-08-2025. CheckOut: 20-08-2025. Noches: 2"
    }
  ]
}
```

---

### 6. Clasificación de Tipo de Factura

**Task Prompt:** `<s_invoice_classify>`

**Descripción:** Clasifica el tipo de factura

**Salida Esperada:**
```json
{
  "tipo_factura": "hotel",
  "confianza": 0.95
}
```

**Tipos Posibles:**
- `"general"` - Factura estándar
- `"hotel"` - Factura de hotel/hospedaje
- `"seguro"` - Factura de seguro/póliza
- `"transporte"` - Factura de transporte
- `"con_descuento"` - Factura con descuentos aplicados

---

## 🔧 Configuración de Training para Cada Task

### Dataset Multi-Task

```python
# Estructura de metadata.jsonl para multi-task
{
  "file_name": "factura_001.jpg",
  "ground_truth": "{\"gt_parse\": {...}}",
  "tasks": [
    "invoice_peru",
    "invoice_header",
    "invoice_items",
    "invoice_totals"
  ]
}
```

### Training Loop Multi-Task

```python
from transformers import Trainer

# Configurar entrenamiento
training_args = {
    "task_prompts": {
        "invoice_peru": "<s_invoice_peru>",
        "invoice_header": "<s_invoice_header>",
        "invoice_items": "<s_invoice_items>",
        "invoice_totals": "<s_invoice_totals>",
        "invoice_hotel": "<s_invoice_hotel>"
    },
    "task_sampling": "proportional",  # Samplear tareas proporcionalmente
    "max_length": 2048,
    "early_stopping": True
}

# Durante training, seleccionar task aleatoriamente
import random

def get_task_prompt(example):
    task = random.choice(example["tasks"])
    return training_args["task_prompts"][task]
```

---

## 🎨 Diseño de Nuevos Task Prompts

### Plantilla para Crear Nuevos Prompts

```python
# 1. Definir el token
new_task_token = "<s_invoice_custom>"

# 2. Agregar al tokenizer
processor.tokenizer.add_special_tokens({
    "additional_special_tokens": [new_task_token]
})

# 3. Redimensionar embeddings del modelo
model.decoder.resize_token_embeddings(len(processor.tokenizer))

# 4. Preparar ground truth específico
def prepare_custom_ground_truth(full_json):
    return {
        "campo_especifico_1": full_json["campo_especifico_1"],
        "campo_especifico_2": full_json["campo_especifico_2"]
    }

# 5. Entrenar con este nuevo task
```

### Ejemplo: Task para Validación de Totales

```python
# Task: Verificar si los totales son correctos
task_prompt = "<s_invoice_validate>"

# Ground truth:
{
  "gt_parse": {
    "totales_correctos": true,
    "errores": [],
    "subtotal": 120.44,
    "igv": 21.68,
    "total": 154.17,
    "calculo_verificado": "120.44 * 1.18 = 142.12 (base) + 12.04 (otros) = 154.16"
  }
}
```

---

## 📊 Mejores Prácticas

### 1. Longitud de Secuencias

```python
task_max_lengths = {
    "invoice_peru": 2048,      # Completo, requiere más tokens
    "invoice_header": 512,     # Solo header, más rápido
    "invoice_items": 1024,     # Items variables
    "invoice_totals": 256,     # Solo números, muy rápido
    "invoice_classify": 128    # Solo clasificación
}
```

### 2. Beam Search por Task

```python
task_beam_configs = {
    "invoice_peru": {
        "num_beams": 4,
        "length_penalty": 1.0
    },
    "invoice_header": {
        "num_beams": 1,  # Greedy, más rápido
        "length_penalty": 1.0
    },
    "invoice_items": {
        "num_beams": 3,
        "length_penalty": 0.8  # Permite más tokens
    }
}
```

### 3. Post-procesamiento por Task

```python
def post_process(result, task):
    if task == "invoice_peru":
        # Validar estructura completa
        return validate_full_invoice(result)

    elif task == "invoice_totals":
        # Validar cálculos
        return validate_calculations(result)

    elif task == "invoice_classify":
        # Solo retornar tipo
        return result["tipo_factura"]
```

---

## 🧪 Testing de Prompts

### Script de Evaluación

```python
import json
from pathlib import Path

def evaluate_task_prompt(model, processor, test_images, task_prompt):
    results = {
        "total": len(test_images),
        "correct": 0,
        "errors": []
    }

    for img_path, ground_truth in test_images:
        # Cargar imagen
        image = Image.open(img_path)

        # Procesar
        pixel_values = processor(image, return_tensors="pt").pixel_values

        # Generar
        decoder_input_ids = processor.tokenizer(
            task_prompt,
            add_special_tokens=False,
            return_tensors="pt"
        ).input_ids

        outputs = model.generate(
            pixel_values,
            decoder_input_ids=decoder_input_ids,
            max_length=2048
        )

        # Decodificar
        sequence = processor.batch_decode(outputs.sequences)[0]
        prediction = processor.token2json(sequence)

        # Comparar
        if prediction == ground_truth:
            results["correct"] += 1
        else:
            results["errors"].append({
                "image": str(img_path),
                "predicted": prediction,
                "expected": ground_truth
            })

    # Calcular accuracy
    results["accuracy"] = results["correct"] / results["total"]
    return results

# Uso
task_results = evaluate_task_prompt(
    model,
    processor,
    test_images,
    "<s_invoice_peru>"
)
print(f"Accuracy: {task_results['accuracy']:.2%}")
```

---

## 🚀 Optimización de Inferencia

### Caché de Prompts

```python
# Pre-tokenizar task prompts
task_prompt_cache = {}

for task_name, task_token in task_prompts.items():
    task_prompt_cache[task_name] = processor.tokenizer(
        task_token,
        add_special_tokens=False,
        return_tensors="pt"
    ).input_ids

# Usar en inferencia
decoder_input_ids = task_prompt_cache["invoice_peru"]
```

### Batching por Task

```python
def batch_process_by_task(images, task_prompt, batch_size=4):
    results = []

    for i in range(0, len(images), batch_size):
        batch = images[i:i+batch_size]

        # Procesar batch
        pixel_values = processor(
            batch,
            return_tensors="pt"
        ).pixel_values

        # Generar para todo el batch
        decoder_input_ids = task_prompt_cache[task_prompt]

        outputs = model.generate(
            pixel_values,
            decoder_input_ids=decoder_input_ids.repeat(len(batch), 1),
            max_length=2048
        )

        # Decodificar batch
        sequences = processor.batch_decode(outputs.sequences)
        batch_results = [processor.token2json(seq) for seq in sequences]
        results.extend(batch_results)

    return results
```

---

## 🔗 Siguiente Paso

Ver **DONUT_FINE_TUNING_GUIDE.md** para aprender a entrenar el modelo con estos task prompts.

---

**Referencias:**
- Donut Task Prompts: https://huggingface.co/docs/transformers/model_doc/donut
- Multi-Task Learning: https://arxiv.org/abs/2111.15664
