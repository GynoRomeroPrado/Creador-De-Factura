# 🚀 Cómo Usar el Procesador desde GitHub en Google Colab

## 📊 Resumen Rápido

**Iteraciones:** 16 variaciones por cada factura

**Resultado:** Si tienes 10 facturas → generarás 160 aumentadas = **170 total**

---

## 🎯 Método 1: Usar el Notebook Directamente (RECOMENDADO)

### Opción A: Abrir desde GitHub

1. Ve a Google Colab: https://colab.research.google.com/

2. Haz clic en **"Archivo" → "Abrir notebook"**

3. Selecciona la pestaña **"GitHub"**

4. Pega esta URL:
   ```
   https://github.com/GynoRomeroPrado/Creador-De-Factura
   ```

5. Selecciona el branch: `claude/colab-invoice-processor-011CUuowDXaNFjHtgp9gChim`

6. Abre el archivo: `Invoice_Dataset_Processor.ipynb`

7. **¡Listo!** Ejecuta las celdas en orden

### Opción B: Link Directo (más fácil)

Abre directamente este link en tu navegador:

```
https://colab.research.google.com/github/GynoRomeroPrado/Creador-De-Factura/blob/claude/colab-invoice-processor-011CUuowDXaNFjHtgp9gChim/Invoice_Dataset_Processor.ipynb
```

---

## 🎯 Método 2: Clonar el Repositorio en Colab

Si prefieres trabajar con el código Python directamente:

### Paso 1: Crear un nuevo notebook en Colab

### Paso 2: Ejecuta esta celda para clonar el repo

```python
# Clonar repositorio
!git clone https://github.com/GynoRomeroPrado/Creador-De-Factura.git
%cd Creador-De-Factura

# Cambiar al branch correcto
!git checkout claude/colab-invoice-processor-011CUuowDXaNFjHtgp9gChim

# Verificar archivos
!ls -la
```

### Paso 3: Usar el script Python

```python
# Importar el módulo
from colab_invoice_augmentation import InvoiceDatasetProcessor
from google.colab import drive

# Montar Drive
drive.mount('/content/drive')

# Configurar rutas
INPUT_FOLDER = "/content/drive/MyDrive/Facturas"
OUTPUT_FOLDER = "/content/drive/MyDrive/Facturas_Procesadas"
PIXEL_RANGE = 10

# Crear procesador
processor = InvoiceDatasetProcessor(INPUT_FOLDER, OUTPUT_FOLDER)

# Ejecutar proceso
organized_pairs = processor.rename_and_organize()
total_generated = processor.augment_dataset(organized_pairs, PIXEL_RANGE)
report = processor.generate_dataset_report()

# Ver resultados
print(f"Facturas generadas: {report['facturas_aumentadas_generadas']}")
print(f"Total en dataset: {report['total_facturas_dataset']}")
```

---

## 📋 Requisitos de tu Carpeta de Drive

Tu carpeta debe tener esta estructura:

```
Drive/Facturas/
├── factura_cualquier_nombre.pdf    ← Imagen o PDF
├── factura_cualquier_nombre.json   ← JSON con la data extraída
├── otra_factura.jpg
├── otra_factura.json
└── ...
```

**Importante:**
- Cada factura debe tener su JSON correspondiente
- El JSON contiene toda la data extraída (emisor, receptor, RUC, montos, etc.)
- Los nombres de archivos no importan, se renombrarán automáticamente

---

## 🔄 Iteraciones Generadas

### Total: 16 variaciones por factura

#### 8 Desplazamientos Completos (±10px):
1. `derecha` → imagen movida 10px a la derecha
2. `izquierda` → imagen movida 10px a la izquierda
3. `abajo` → imagen movida 10px hacia abajo
4. `arriba` → imagen movida 10px hacia arriba
5. `diagonal_superior_derecha` → (+10px, -10px)
6. `diagonal_superior_izquierda` → (-10px, -10px)
7. `diagonal_inferior_derecha` → (+10px, +10px)
8. `diagonal_inferior_izquierda` → (-10px, +10px)

#### 8 Desplazamientos Medios (±5px):
9-16. Las mismas 8 direcciones con la mitad del desplazamiento

**Nombres generados:**
```
factura_0001_aug_01_derecha.png
factura_0001_aug_02_izquierda.png
factura_0001_aug_03_abajo.png
...
factura_0001_aug_16_diagonal_inferior_izquierda_medio.png
```

---

## 📊 Ejemplo de Ejecución

### Entrada:
```
Facturas/
├── random_name_123.pdf
├── random_name_123.json
├── otra_factura.jpg
├── otra_factura.json
```

### Salida:
```
Facturas_Procesadas/
├── organized/
│   ├── factura_0001.pdf           ← Renombrada
│   ├── factura_0001.json          ← JSON actualizado
│   ├── factura_0002.jpg
│   └── factura_0002.json
│
├── augmented/
│   ├── factura_0001_aug_01_derecha.png
│   ├── factura_0001_aug_01_derecha.json
│   ├── factura_0001_aug_02_izquierda.png
│   ├── factura_0001_aug_02_izquierda.json
│   ... (16 variaciones × 2 facturas = 32 archivos)
│   ├── factura_0002_aug_16_diagonal_inferior_izquierda_medio.png
│   └── factura_0002_aug_16_diagonal_inferior_izquierda_medio.json
│
└── dataset_report.json            ← Reporte de estadísticas
```

### Estadísticas:
- **Facturas originales:** 2
- **Facturas aumentadas:** 32 (2 × 16)
- **Total en dataset:** 34

---

## ⚙️ Personalización

### Cambiar el rango de píxeles

En la celda de configuración, modifica:

```python
PIXEL_RANGE = 15  # Cambiar de 10 a 15 píxeles
```

Esto generará desplazamientos de ±15px y ±7.5px (en lugar de ±10px y ±5px)

### Modificar las iteraciones

Si quieres agregar más transformaciones, edita la función `get_augmentation_configs()` en el archivo `colab_invoice_augmentation.py`

---

## 📝 JSON Generado

Cada factura aumentada mantiene **TODA la data original** y agrega metadata:

```json
{
  "filename": "factura_0001_aug_01_derecha",
  "fecha_extraccion": "2025-11-05T17:15:20.413106",
  "datos_extraidos": {
    "tipo_documento": "FACTURA",
    "emisor_ruc": "20505670443",
    "emisor_razon_social": "...",
    "total": 364.8,
    ...
  },
  "metricas": {
    "total_campos": 47,
    "campos_extraidos": 34,
    ...
  },
  "augmentation": {
    "original_file": "factura_0001.pdf",
    "transformation": "derecha",
    "shift_x": 10,
    "shift_y": 0
  }
}
```

---

## ❓ Preguntas Frecuentes

### ¿Por qué 16 iteraciones?

Es un balance entre:
- **Diversidad:** Suficientes variaciones para entrenar modelos robustos
- **Eficiencia:** No genera archivos innecesarios
- **Cobertura:** 8 direcciones × 2 magnitudes cubre todas las orientaciones

### ¿Puedo cambiar el número de iteraciones?

Sí, modifica la función `get_augmentation_configs()`. Puedes agregar:
- Más rangos de píxeles (±3px, ±7px, ±15px)
- Rotaciones
- Cambios de brillo
- Etc.

### ¿Los bounding boxes se actualizan automáticamente?

No, el JSON mantiene la **data extraída** (texto, números, etc.) sin cambios. Los **bounding boxes se generarán después en Colab** usando otros comandos, ya que las coordenadas cambiarán según el desplazamiento aplicado.

### ¿Qué formato de imagen se genera?

Todas las facturas aumentadas se guardan como **PNG** de alta calidad (quality=95) para mantener la claridad del texto.

---

## 🎯 Próximos Pasos

Después de generar el dataset aumentado:

1. **Verifica** las imágenes generadas en la carpeta `augmented/`
2. **Ejecuta tus comandos** en Colab para generar bounding boxes
3. **Entrena** tu modelo con el dataset expandido

---

**¿Listo para empezar? ¡Abre el notebook y ejecuta! 🚀**
