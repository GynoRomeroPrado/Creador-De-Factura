# 🍩 Guía de Fine-Tuning Donut para Facturas Peruanas

**Modelo:** Document Understanding Transformer (Donut)
**Versión:** Compatible con naver-clova-ix/donut-base
**Fecha:** 2025-01-19
**Hardware Recomendado:** GPU con 16GB+ VRAM (RTX 3090, A100, V100)

---

## 🎯 Objetivo

Entrenar Donut para extraer automáticamente datos estructurados de facturas peruanas sin necesidad de OCR tradicional.

---

## 📋 Pre-requisitos

### 1. Hardware

```python
# Mínimo Recomendado
GPU_MEMORY = "16GB"  # RTX 3090, A100
RAM = "32GB"
STORAGE = "100GB SSD"

# Óptimo
GPU_MEMORY = "40GB+"  # A100 40GB/80GB
RAM = "64GB+"
STORAGE = "500GB NVMe SSD"
```

### 2. Software

```bash
# Python 3.8+
python --version  # >= 3.8

# PyTorch con CUDA
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118

# Transformers
pip install transformers==4.36.0

# Otras dependencias
pip install datasets
pip install sentencepiece
pip install pillow
pip install nltk
pip install timm
pip install pytorch-lightning==1.9.5
pip install zss  # Para Tree Edit Distance
```

### 3. Dataset Preparado

```
dataset/
├── train/
│   ├── metadata.jsonl  # Anotaciones
│   └── images/         # Imágenes de facturas
├── validation/
│   ├── metadata.jsonl
│   └── images/
└── test/
    ├── metadata.jsonl
    └── images/
```

Ver **DONUT_TRAINING_FORMAT.md** para formato detallado.

---

## 🚀 Paso 1: Preparar el Entorno

### Crear Proyecto

```bash
# Crear directorio
mkdir donut-invoice-peru
cd donut-invoice-peru

# Crear ambiente virtual
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### Estructura de Proyecto

```
donut-invoice-peru/
├── data/
│   ├── train/
│   ├── validation/
│   └── test/
├── models/
│   ├── checkpoints/
│   └── final/
├── scripts/
│   ├── train.py
│   ├── evaluate.py
│   └── inference.py
├── configs/
│   └── training_config.yaml
├── logs/
└── requirements.txt
```

---

## 🔧 Paso 2: Configuración de Training

### Archivo: `configs/training_config.yaml`

```yaml
# ========================================
# Configuración de Modelo
# ========================================
model:
  name: "naver-clova-ix/donut-base"
  pretrained: true
  resume_from_checkpoint: null

# ========================================
# Configuración de Dataset
# ========================================
dataset:
  train_dir: "./data/train"
  val_dir: "./data/validation"
  test_dir: "./data/test"
  image_size: [1280, 960]  # [width, height]
  max_length: 2048
  task_prompt: "<s_invoice_peru>"

# ========================================
# Configuración de Training
# ========================================
training:
  output_dir: "./models/checkpoints"
  num_train_epochs: 30
  per_device_train_batch_size: 1
  per_device_eval_batch_size: 1
  gradient_accumulation_steps: 8  # Batch efectivo = 1 * 8 = 8
  learning_rate: 3e-5
  warmup_steps: 500
  weight_decay: 0.01
  logging_steps: 100
  eval_steps: 500
  save_steps: 500
  save_total_limit: 5
  fp16: true  # Mixed precision training
  dataloader_num_workers: 4
  remove_unused_columns: false
  eval_strategy: "steps"
  save_strategy: "steps"
  load_best_model_at_end: true
  metric_for_best_model: "f1"
  greater_is_better: true

# ========================================
# Configuración de Optimizer
# ========================================
optimizer:
  type: "AdamW"
  betas: [0.9, 0.999]
  eps: 1e-8

# ========================================
# Configuración de Scheduler
# ========================================
scheduler:
  type: "cosine"
  num_cycles: 0.5

# ========================================
# Configuración de Generación
# ========================================
generation:
  max_length: 2048
  early_stopping: true
  num_beams: 1
  use_cache: true
  bad_words_ids: [[3]]  # UNK token

# ========================================
# Data Augmentation
# ========================================
augmentation:
  enabled: true
  rotation_range: [-5, 5]
  brightness_range: [0.8, 1.2]
  contrast_range: [0.8, 1.2]
  gaussian_noise: 0.01
```

---

## 📝 Paso 3: Script de Training

### Archivo: `scripts/train.py`

```python
#!/usr/bin/env python3
"""
Script de entrenamiento para Donut en facturas peruanas
"""

import os
import json
import re
from pathlib import Path
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

import torch
from torch.utils.data import Dataset
from PIL import Image
import pytorch_lightning as pl
from pytorch_lightning.callbacks import ModelCheckpoint, EarlyStopping
from pytorch_lightning.loggers import WandbLogger, TensorBoardLogger

from transformers import (
    DonutProcessor,
    VisionEncoderDecoderModel,
    VisionEncoderDecoderConfig
)

# ========================================
# Dataset Personalizado
# ========================================

class InvoiceDataset(Dataset):
    """Dataset de facturas para Donut"""

    def __init__(
        self,
        dataset_dir: str,
        processor: DonutProcessor,
        max_length: int = 2048,
        task_prompt: str = "<s_invoice_peru>",
        image_size: Tuple[int, int] = (1280, 960),
        augment: bool = False
    ):
        self.dataset_dir = Path(dataset_dir)
        self.processor = processor
        self.max_length = max_length
        self.task_prompt = task_prompt
        self.image_size = image_size
        self.augment = augment

        # Leer metadata
        self.annotations = self._load_annotations()

    def _load_annotations(self) -> List[Dict]:
        """Cargar anotaciones desde metadata.jsonl"""
        annotations = []
        metadata_file = self.dataset_dir / "metadata.jsonl"

        with open(metadata_file, "r", encoding="utf-8") as f:
            for line in f:
                data = json.loads(line.strip())
                annotations.append(data)

        return annotations

    def __len__(self) -> int:
        return len(self.annotations)

    def __getitem__(self, idx: int) -> Dict[str, Any]:
        annotation = self.annotations[idx]

        # Cargar imagen
        image_path = self.dataset_dir / "images" / annotation["file_name"]
        image = Image.open(image_path).convert("RGB")

        # Aplicar data augmentation (opcional)
        if self.augment:
            image = self._augment_image(image)

        # Procesar imagen
        pixel_values = self.processor(
            image,
            return_tensors="pt"
        ).pixel_values.squeeze()

        # Procesar ground truth
        ground_truth = json.loads(annotation["ground_truth"])
        target_sequence = self.processor.token2json(ground_truth)

        # Tokenizar target
        target = self.processor.tokenizer(
            target_sequence,
            add_special_tokens=False,
            max_length=self.max_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt"
        )

        # Preparar labels (input_ids con -100 para tokens de padding)
        labels = target["input_ids"].squeeze()
        labels[labels == self.processor.tokenizer.pad_token_id] = -100

        return {
            "pixel_values": pixel_values,
            "labels": labels,
            "target_sequence": target_sequence
        }

    def _augment_image(self, image: Image.Image) -> Image.Image:
        """Aplicar data augmentation"""
        # Implementar augmentations aquí
        # (rotación, brillo, contraste, etc.)
        return image


# ========================================
# Lightning Module
# ========================================

class DonutInvoiceModel(pl.LightningModule):
    """Lightning module para entrenamiento de Donut"""

    def __init__(
        self,
        config: Dict,
        processor: DonutProcessor,
        model: VisionEncoderDecoderModel
    ):
        super().__init__()
        self.config = config
        self.processor = processor
        self.model = model
        self.save_hyperparameters(ignore=["processor", "model"])

    def training_step(self, batch, batch_idx):
        pixel_values = batch["pixel_values"]
        labels = batch["labels"]

        outputs = self.model(
            pixel_values=pixel_values,
            labels=labels
        )

        loss = outputs.loss
        self.log("train/loss", loss, on_step=True, on_epoch=True, prog_bar=True)

        return loss

    def validation_step(self, batch, batch_idx):
        pixel_values = batch["pixel_values"]
        labels = batch["labels"]
        target_sequences = batch["target_sequence"]

        # Calcular loss
        outputs = self.model(
            pixel_values=pixel_values,
            labels=labels
        )

        loss = outputs.loss
        self.log("val/loss", loss, on_step=False, on_epoch=True, prog_bar=True)

        # Generar predicciones
        decoder_input_ids = self.processor.tokenizer(
            self.config["dataset"]["task_prompt"],
            add_special_tokens=False,
            return_tensors="pt"
        ).input_ids.to(self.device)

        generated = self.model.generate(
            pixel_values,
            decoder_input_ids=decoder_input_ids,
            max_length=self.config["dataset"]["max_length"],
            early_stopping=True,
            pad_token_id=self.processor.tokenizer.pad_token_id,
            eos_token_id=self.processor.tokenizer.eos_token_id,
            use_cache=True,
            num_beams=1,
            return_dict_in_generate=True
        )

        # Decodificar
        predictions = self.processor.batch_decode(
            generated.sequences,
            skip_special_tokens=True
        )

        # Calcular métricas
        metrics = self._calculate_metrics(predictions, target_sequences)

        for key, value in metrics.items():
            self.log(f"val/{key}", value, on_step=False, on_epoch=True)

        return {"loss": loss, "metrics": metrics}

    def _calculate_metrics(
        self,
        predictions: List[str],
        targets: List[str]
    ) -> Dict[str, float]:
        """Calcular F1, Precision, Recall"""
        # Implementar cálculo de métricas
        # Tree Edit Distance, F1 por campo, etc.
        return {
            "f1": 0.85,  # Placeholder
            "precision": 0.87,
            "recall": 0.83
        }

    def configure_optimizers(self):
        optimizer = torch.optim.AdamW(
            self.parameters(),
            lr=self.config["training"]["learning_rate"],
            betas=self.config["optimizer"]["betas"],
            eps=self.config["optimizer"]["eps"],
            weight_decay=self.config["training"]["weight_decay"]
        )

        scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
            optimizer,
            T_max=self.trainer.max_epochs
        )

        return {
            "optimizer": optimizer,
            "lr_scheduler": {
                "scheduler": scheduler,
                "interval": "epoch"
            }
        }


# ========================================
# Main Training Loop
# ========================================

def main():
    import yaml

    # Cargar configuración
    with open("configs/training_config.yaml", "r") as f:
        config = yaml.safe_load(f)

    # Cargar modelo y processor
    processor = DonutProcessor.from_pretrained(config["model"]["name"])
    model = VisionEncoderDecoderModel.from_pretrained(config["model"]["name"])

    # Configurar decoder
    model.config.decoder_start_token_id = processor.tokenizer.convert_tokens_to_ids(
        ["<s>"]
    )[0]
    model.config.pad_token_id = processor.tokenizer.pad_token_id

    # Crear datasets
    train_dataset = InvoiceDataset(
        dataset_dir=config["dataset"]["train_dir"],
        processor=processor,
        max_length=config["dataset"]["max_length"],
        task_prompt=config["dataset"]["task_prompt"],
        augment=config["augmentation"]["enabled"]
    )

    val_dataset = InvoiceDataset(
        dataset_dir=config["dataset"]["val_dir"],
        processor=processor,
        max_length=config["dataset"]["max_length"],
        task_prompt=config["dataset"]["task_prompt"],
        augment=False
    )

    # Crear dataloaders
    train_dataloader = torch.utils.data.DataLoader(
        train_dataset,
        batch_size=config["training"]["per_device_train_batch_size"],
        shuffle=True,
        num_workers=config["training"]["dataloader_num_workers"]
    )

    val_dataloader = torch.utils.data.DataLoader(
        val_dataset,
        batch_size=config["training"]["per_device_eval_batch_size"],
        shuffle=False,
        num_workers=config["training"]["dataloader_num_workers"]
    )

    # Crear Lightning module
    pl_model = DonutInvoiceModel(
        config=config,
        processor=processor,
        model=model
    )

    # Callbacks
    checkpoint_callback = ModelCheckpoint(
        dirpath=config["training"]["output_dir"],
        filename="donut-invoice-{epoch:02d}-{val/f1:.4f}",
        monitor="val/f1",
        mode="max",
        save_top_k=config["training"]["save_total_limit"],
        save_last=True
    )

    early_stop_callback = EarlyStopping(
        monitor="val/f1",
        patience=5,
        mode="max"
    )

    # Logger
    logger = TensorBoardLogger("logs", name="donut-invoice")

    # Trainer
    trainer = pl.Trainer(
        max_epochs=config["training"]["num_train_epochs"],
        accelerator="gpu",
        devices=1,
        precision=16 if config["training"]["fp16"] else 32,
        gradient_clip_val=1.0,
        accumulate_grad_batches=config["training"]["gradient_accumulation_steps"],
        callbacks=[checkpoint_callback, early_stop_callback],
        logger=logger,
        log_every_n_steps=config["training"]["logging_steps"],
        val_check_interval=config["training"]["eval_steps"]
    )

    # Entrenar
    trainer.fit(
        pl_model,
        train_dataloaders=train_dataloader,
        val_dataloaders=val_dataloader
    )

    print("✅ Entrenamiento completado!")
    print(f"Mejor modelo guardado en: {checkpoint_callback.best_model_path}")


if __name__ == "__main__":
    main()
```

---

## 🎯 Paso 4: Ejecutar Training

### Comando Básico

```bash
# Activar ambiente
source venv/bin/activate

# Ejecutar training
python scripts/train.py
```

### Con Monitoreo TensorBoard

```bash
# Terminal 1: Training
python scripts/train.py

# Terminal 2: TensorBoard
tensorboard --logdir logs/
# Abrir http://localhost:6006
```

### Con Weights & Biases

```python
# Instalar wandb
pip install wandb
wandb login

# En train.py, cambiar logger:
logger = WandbLogger(
    project="donut-invoice-peru",
    name="run-001"
)
```

---

## 📊 Paso 5: Monitoreo y Métricas

### Métricas a Vigilar

```python
metrics_to_track = {
    "train/loss": "Debe disminuir constantemente",
    "val/loss": "Debe disminuir sin overfitting",
    "val/f1": "Objetivo: > 0.90",
    "val/precision": "Objetivo: > 0.92",
    "val/recall": "Objetivo: > 0.88",
    "val/ted": "Tree Edit Distance, debe ser bajo",
    "learning_rate": "Monitorear scheduler"
}
```

### Señales de Problemas

```python
warning_signs = {
    "train_loss estancado": "Learning rate muy bajo o datos muy difíciles",
    "val_loss aumentando": "Overfitting - reducir epochs o añadir regularización",
    "f1 < 0.70": "Problema con datos o configuración",
    "NaN loss": "Learning rate muy alto o problema en datos"
}
```

---

## 🔧 Paso 6: Hiperparámetros Óptimos

### Recomendaciones Basadas en Tamaño de Dataset

#### Dataset Pequeño (< 500 facturas)

```yaml
training:
  num_train_epochs: 50
  learning_rate: 1e-5
  weight_decay: 0.05
  gradient_accumulation_steps: 16
augmentation:
  enabled: true  # Muy importante
```

#### Dataset Mediano (500-2000 facturas)

```yaml
training:
  num_train_epochs: 30
  learning_rate: 3e-5
  weight_decay: 0.01
  gradient_accumulation_steps: 8
augmentation:
  enabled: true
```

#### Dataset Grande (> 2000 facturas)

```yaml
training:
  num_train_epochs: 20
  learning_rate: 5e-5
  weight_decay: 0.001
  gradient_accumulation_steps: 4
augmentation:
  enabled: false  # Opcional
```

---

## 🚀 Paso 7: Inferencia con Modelo Entrenado

### Script: `scripts/inference.py`

```python
from transformers import DonutProcessor, VisionEncoderDecoderModel
from PIL import Image
import torch
import json

# Cargar modelo entrenado
model_path = "./models/checkpoints/donut-invoice-epoch=25-val_f1=0.9234.ckpt"
processor = DonutProcessor.from_pretrained("naver-clova-ix/donut-base")
model = VisionEncoderDecoderModel.from_pretrained(model_path)

model.eval()
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

# Cargar imagen de factura
image = Image.open("test_invoice.jpg").convert("RGB")

# Procesar
pixel_values = processor(image, return_tensors="pt").pixel_values.to(device)

# Task prompt
task_prompt = "<s_invoice_peru>"
decoder_input_ids = processor.tokenizer(
    task_prompt,
    add_special_tokens=False,
    return_tensors="pt"
).input_ids.to(device)

# Generar
with torch.no_grad():
    outputs = model.generate(
        pixel_values,
        decoder_input_ids=decoder_input_ids,
        max_length=2048,
        early_stopping=True,
        pad_token_id=processor.tokenizer.pad_token_id,
        eos_token_id=processor.tokenizer.eos_token_id,
        use_cache=True,
        num_beams=1,
        return_dict_in_generate=True
    )

# Decodificar
sequence = processor.batch_decode(outputs.sequences)[0]
result = processor.token2json(sequence)

# Guardar resultado
with open("output.json", "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print("✅ Extracción completada!")
print(json.dumps(result, indent=2, ensure_ascii=False))
```

---

## 🔗 Siguiente Paso

Ver **DONUT_DATA_SCHEMA.md** para detalles del esquema de datos y validaciones.

---

**Referencias:**
- Lightning Docs: https://lightning.ai/docs/pytorch/stable/
- Donut GitHub: https://github.com/clovaai/donut
- Transformers Trainer: https://huggingface.co/docs/transformers/main_classes/trainer
