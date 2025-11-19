# 🍩 Donut para Extracción de Facturas Peruanas

**Document Understanding Transformer** entrenado para extraer datos estructurados de facturas peruanas sin OCR tradicional.

---

## 🎯 ¿Qué es Donut?

Donut es un modelo **visual transformer end-to-end** que:

- ✅ **NO requiere OCR** - Procesa imágenes directamente
- ✅ **Extrae JSON estructurado** - De imagen a datos estructurados
- ✅ **Basado en Transformers** - Arquitectura Swin + BART
- ✅ **Fine-tunable** - Entrenable con datasets personalizados
- ✅ **State-of-the-art** - Resultados superiores a pipelines OCR tradicionales

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Factura   │ ───▶ │    Donut    │ ───▶ │    JSON     │
│   (imagen)  │      │   Model     │      │ Estructurado│
└─────────────┘      └─────────────┘      └─────────────┘
```

---

## 📚 Documentación

Este proyecto incluye documentación completa en 4 archivos:

### 1. [DONUT_TRAINING_FORMAT.md](DONUT_TRAINING_FORMAT.md)
- Formato de datos de entrenamiento
- Estructura de directorios
- Formato metadata.jsonl
- Ground truth JSON
- Reglas de preprocesamiento

### 2. [DONUT_TASK_PROMPTS.md](DONUT_TASK_PROMPTS.md)
- Definición de task prompts
- Multi-task learning
- Prompts por tipo de factura
- Configuración de inferencia

### 3. [DONUT_FINE_TUNING_GUIDE.md](DONUT_FINE_TUNING_GUIDE.md)
- Guía completa de fine-tuning
- Configuración de hardware/software
- Script de entrenamiento
- Hiperparámetros óptimos
- Monitoreo con TensorBoard/W&B

### 4. [DONUT_DATA_SCHEMA.md](DONUT_DATA_SCHEMA.md)
- Esquema de datos (3 niveles)
- Validaciones por tipo
- Métricas de evaluación
- Tree Edit Distance, F1 Score

---

## 🚀 Quick Start

### Paso 1: Convertir Dataset

Convierte tus JSONs + imágenes al formato Donut:

```bash
python scripts/convert_to_donut_format.py \
    --input-json "Datos extraidos de Originales/anotaciones" \
    --input-images "Datos extraidos de Originales/facturas_procesadas" \
    --output "dataset_donut" \
    --schema intermedio \
    --split 0.8 0.1 0.1
```

**Resultado:**
```
dataset_donut/
├── train/
│   ├── metadata.jsonl
│   └── images/
├── validation/
│   ├── metadata.jsonl
│   └── images/
└── test/
    ├── metadata.jsonl
    └── images/
```

### Paso 2: Instalar Dependencias

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
pip install transformers==4.36.0
pip install datasets sentencepiece pillow
pip install pytorch-lightning==1.9.5
pip install zss  # Para Tree Edit Distance
```

### Paso 3: Entrenar Modelo

```bash
# Usando el script incluido
python scripts/train.py
```

O con configuración personalizada:

```python
from transformers import DonutProcessor, VisionEncoderDecoderModel

# Cargar modelo base
processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base")
model = VisionEncoderDecoderModel.from_pretrained("naver-clova-ix/donut-base")

# Configurar y entrenar
# (Ver DONUT_FINE_TUNING_GUIDE.md para código completo)
```

### Paso 4: Inferencia

```python
from transformers import DonutProcessor, VisionEncoderDecoderModel
from PIL import Image
import torch

# Cargar modelo entrenado
processor = DonutProcessor.from_pretrained("modelo_entrenado/")
model = VisionEncoderDecoderModel.from_pretrained("modelo_entrenado/")

# Cargar factura
image = Image.open("factura.jpg").convert("RGB")

# Procesar
pixel_values = processor(image, return_tensors="pt").pixel_values
task_prompt = "<s_invoice_peru>"
decoder_input_ids = processor.tokenizer(
    task_prompt,
    add_special_tokens=False,
    return_tensors="pt"
).input_ids

# Generar JSON
outputs = model.generate(
    pixel_values,
    decoder_input_ids=decoder_input_ids,
    max_length=2048
)

# Resultado
result = processor.token2json(processor.batch_decode(outputs.sequences)[0])
print(result)
```

---

## 📊 Niveles de Esquema

### Básico (20 campos)
- Ideal para: POC, validación rápida
- F1 Score esperado: > 0.90
- Tiempo de entrenamiento: ~2-4 horas
- Dataset mínimo: 200 facturas

### Intermedio (50 campos) ⭐ **Recomendado**
- Ideal para: Producción estándar
- F1 Score esperado: 0.85-0.90
- Tiempo de entrenamiento: ~6-10 horas
- Dataset mínimo: 500 facturas

### Completo (97 campos)
- Ideal para: Máxima precisión
- F1 Score esperado: 0.70-0.80
- Tiempo de entrenamiento: ~15-24 horas
- Dataset mínimo: 2000 facturas

---

## 🎯 Task Prompts Disponibles

```python
task_prompts = {
    "<s_invoice_peru>": "Extracción completa de factura",
    "<s_invoice_header>": "Solo cabecera (rápido)",
    "<s_invoice_items>": "Solo items",
    "<s_invoice_totals>": "Solo totales",
    "<s_invoice_hotel>": "Factura de hotel especializada"
}
```

---

## 📈 Resultados Esperados

### Con 500 facturas de entrenamiento (esquema intermedio)

| Métrica | Valor |
|---------|-------|
| F1 Score | 0.87 |
| Precision | 0.89 |
| Recall | 0.85 |
| Tree Edit Distance | < 5.0 |
| Exact Match | 45% |

### Con 2000 facturas de entrenamiento (esquema completo)

| Métrica | Valor |
|---------|-------|
| F1 Score | 0.78 |
| Precision | 0.82 |
| Recall | 0.74 |
| Tree Edit Distance | < 8.0 |
| Exact Match | 25% |

---

## 🔧 Configuración Recomendada

### Hardware

```yaml
GPU: RTX 3090 / A100 (16GB+ VRAM)
RAM: 32GB+
Storage: 100GB SSD
```

### Hiperparámetros (Dataset Mediano 500-2000 facturas)

```yaml
num_train_epochs: 30
learning_rate: 3e-5
batch_size: 1
gradient_accumulation_steps: 8
max_length: 2048
image_size: [1280, 960]
fp16: true
```

---

## 📁 Estructura del Proyecto

```
Creador-De-Factura/
├── DONUT_README.md                 # Este archivo
├── DONUT_TRAINING_FORMAT.md        # Formato de datos
├── DONUT_TASK_PROMPTS.md           # Task prompts
├── DONUT_FINE_TUNING_GUIDE.md      # Guía de entrenamiento
├── DONUT_DATA_SCHEMA.md            # Esquema de datos
│
├── scripts/
│   ├── convert_to_donut_format.py  # Conversión de datos
│   ├── train.py                    # Script de entrenamiento
│   ├── evaluate.py                 # Evaluación
│   └── inference.py                # Inferencia
│
├── configs/
│   └── training_config.yaml        # Configuración de training
│
├── dataset_donut/                  # Dataset convertido
│   ├── train/
│   ├── validation/
│   └── test/
│
└── Datos extraidos de Originales/  # Datos originales
    ├── anotaciones/                # JSONs
    └── facturas_procesadas/        # Imágenes
```

---

## 🎓 Tutoriales

### Tutorial 1: Entrenar con Dataset Pequeño

```bash
# 1. Convertir datos (esquema básico)
python scripts/convert_to_donut_format.py \
    --input-json "Datos extraidos de Originales/anotaciones" \
    --input-images "Datos extraidos de Originales/facturas_procesadas" \
    --output "dataset_small" \
    --schema basico

# 2. Modificar configs/training_config.yaml
#    - num_train_epochs: 50
#    - learning_rate: 1e-5

# 3. Entrenar
python scripts/train.py

# 4. Evaluar
python scripts/evaluate.py --model checkpoints/best_model
```

### Tutorial 2: Multi-Task Learning

Ver [DONUT_TASK_PROMPTS.md](DONUT_TASK_PROMPTS.md) para configuración multi-task.

---

## ❓ FAQ

### ¿Cuántas facturas necesito?

- **Mínimo:** 200 facturas (esquema básico)
- **Recomendado:** 500-1000 facturas (esquema intermedio)
- **Óptimo:** 2000+ facturas (esquema completo)

### ¿Qué GPU necesito?

- **Mínimo:** RTX 3060 (12GB) - batch_size=1, esquema básico
- **Recomendado:** RTX 3090 (24GB) - batch_size=1-2, esquema intermedio
- **Óptimo:** A100 (40GB) - batch_size=4, esquema completo

### ¿Cuánto tarda el entrenamiento?

- **Dataset pequeño (200):** 2-4 horas
- **Dataset mediano (500):** 6-10 horas
- **Dataset grande (2000):** 15-24 horas

### ¿Puedo usar CPU?

Sí, pero será muy lento (10-20x más lento). No recomendado para entrenamiento.

### ¿Funciona con facturas escaneadas de baja calidad?

Sí, pero se recomienda:
- Resolución mínima: 150 DPI
- Aplicar data augmentation
- Incluir ejemplos de baja calidad en el dataset de entrenamiento

---

## 🔗 Enlaces Útiles

- **Paper Original:** [OCR-free Document Understanding Transformer](https://arxiv.org/abs/2111.15664)
- **Modelo Base:** [naver-clova-ix/donut-base](https://huggingface.co/naver-clova-ix/donut-base)
- **Hugging Face Docs:** [Donut Documentation](https://huggingface.co/docs/transformers/model_doc/donut)
- **GitHub Original:** [clovaai/donut](https://github.com/clovaai/donut)

---

## 📞 Soporte

Para preguntas o problemas:

1. Revisa la documentación completa en los 4 archivos MD
2. Verifica que tu dataset esté en el formato correcto
3. Consulta los ejemplos en `scripts/`

---

## ✅ Checklist de Implementación

Antes de empezar el entrenamiento:

```
✓ Hardware/Software
[ ] GPU con 16GB+ VRAM
[ ] PyTorch con CUDA instalado
[ ] Transformers 4.36.0 instalado
[ ] 100GB+ de espacio libre

✓ Datos
[ ] JSONs de facturas en formato correcto (97 campos)
[ ] Imágenes de facturas (PDF/JPG/PNG)
[ ] Correspondencia JSON-Imagen verificada
[ ] Mínimo 200 pares JSON-Imagen

✓ Preparación
[ ] Dataset convertido con convert_to_donut_format.py
[ ] metadata.jsonl generado y validado
[ ] Splits train/val/test creados
[ ] Estadísticas del dataset revisadas

✓ Configuración
[ ] training_config.yaml ajustado
[ ] Task prompts definidos
[ ] Nivel de esquema seleccionado
[ ] Hiperparámetros configurados

✓ Entrenamiento
[ ] Script de training probado
[ ] TensorBoard/W&B configurado
[ ] Checkpoints configurados
[ ] Early stopping configurado

✓ Validación
[ ] Script de evaluación preparado
[ ] Métricas de validación definidas
[ ] Dataset de test separado
```

---

**Última actualización:** 2025-01-19
**Versión:** 1.0
**Compatibilidad:** Donut Base (naver-clova-ix)
