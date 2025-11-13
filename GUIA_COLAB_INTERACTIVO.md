# 🎯 GUÍA DE USO - GENERADOR INTERACTIVO PARA GOOGLE COLAB

## 📋 Descripción

Este script te permite generar facturas de forma interactiva en Google Colab. Te preguntará:
- ✅ ¿Cuántas facturas de **1 página** quieres? (10-15 items)
- ✅ ¿Cuántas facturas **multipágina** quieres? (3-6 páginas, 40-80 items)

---

## 🚀 USO EN GOOGLE COLAB

### Paso 1: Clonar el repositorio y preparar entorno

```python
# Clonar repositorio
!git clone https://github.com/GynoRomeroPrado/Creador-De-Factura.git
%cd Creador-De-Factura

# Actualizar a la rama correcta
!git checkout claude/fix-json-parsing-011CUyGo75ZndGpbT9KKAMXw
!git pull origin claude/fix-json-parsing-011CUyGo75ZndGpbT9KKAMXw

# Instalar dependencias
!pip install reportlab -q
```

### Paso 2: Ejecutar el generador interactivo

```python
# Ejecutar el script interactivo
!python COLAB_GENERAR_INTERACTIVO.py
```

### Paso 3: Responder las preguntas

El script te preguntará:

```
¿Cuántas facturas de 1 página deseas generar? (0-1000): 50
¿Cuántas facturas multipágina deseas generar? (0-1000): 20
```

Luego mostrará un resumen y pedirá confirmación:

```
📊 RESUMEN DE GENERACIÓN
  Facturas de 1 página: 50
  Facturas multipágina: 20
  TOTAL A GENERAR: 70

¿Proceder con la generación? (s/n): s
```

### Paso 4: Decidir si generar PDFs

Una vez generados los JSONs, el script preguntará:

```
¿Deseas generar los PDFs ahora? (s/n): s
```

- **Si respondes 's'**: Generará los PDFs automáticamente y los comprimirá
- **Si respondes 'n'**: Solo generará los JSONs (puedes generar PDFs después)

### Paso 5: Descargar los PDFs (si los generaste)

Si elegiste generar PDFs, ejecuta:

```python
from google.colab import files
files.download('/content/PDFs_LOTE_YYYYMMDD_HHMMSS.zip')
```

*(Reemplaza YYYYMMDD_HHMMSS con el timestamp que te muestre el script)*

---

## 📊 CARACTERÍSTICAS

### Facturas de 1 Página
- **Items:** 10-15 por factura
- **Páginas:** 1 página exacta
- **Tipos:** General, con descuento, con crédito
- **Monedas:** PEN, USD, EUR (aleatorio)

### Facturas Multipágina
- **Items:** 40-80 por factura
- **Páginas:** 3-6 páginas (distribución aleatoria)
- **Tipos:** Compra grande, con descuento, con crédito
- **Monedas:** PEN, USD, EUR (aleatorio)

### Distribución de Páginas (Multipágina)
- 3 páginas: ~40-45 items
- 4 páginas: ~46-55 items
- 5 páginas: ~56-70 items
- 6 páginas: ~71-80 items

---

## 📁 ESTRUCTURA DE ARCHIVOS GENERADOS

```
facturas_generadas/LOTE_INTERACTIVO_20250110_120530/
├── FACTURA_0001_1PAG_F123_456789.json
├── FACTURA_0002_1PAG_F234_567890.json
├── ...
├── FACTURA_0051_4PAG_F345_678901.json
├── FACTURA_0052_5PAG_F456_789012.json
└── ...

PDFs_LOTE_20250110_120530/
├── FACTURA_0001_1PAG_F123_456789.pdf
├── FACTURA_0002_1PAG_F234_567890.pdf
└── ...
```

**Nombres de archivo incluyen:**
- Número secuencial: `FACTURA_0001`
- Número de páginas: `1PAG`, `3PAG`, `4PAG`, etc.
- Serie y número: `F123_456789`

---

## ⏱️ TIEMPOS ESTIMADOS

| Cantidad Total | JSONs | PDFs | Total |
|----------------|-------|------|-------|
| 10 facturas | ~5 seg | ~30 seg | ~35 seg |
| 50 facturas | ~25 seg | ~2.5 min | ~3 min |
| 100 facturas | ~50 seg | ~5 min | ~6 min |
| 500 facturas | ~4 min | ~25 min | ~29 min |

*Tiempos en Google Colab con GPU gratuita*

---

## 💡 CONSEJOS

1. **Para pruebas:** Genera 5-10 de cada tipo
2. **Para datasets pequeños:** 20-50 de cada tipo
3. **Para datasets grandes:** 100-500 de cada tipo
4. **Límite máximo:** 1000 de cada tipo

5. **Si no necesitas PDFs inmediatamente:**
   - Responde 'n' cuando pregunte por PDFs
   - Descarga solo los JSONs (más rápido)
   - Genera PDFs localmente después

6. **Si el proceso se interrumpe:**
   - Los JSONs ya generados estarán guardados
   - Puedes generar PDFs manualmente después

---

## 🔧 GENERAR PDFs MANUALMENTE (DESPUÉS)

Si no generaste los PDFs durante el proceso interactivo:

```python
import os
import json
from src.pdf_creator import PDFFactura

# Configurar directorios
json_dir = "facturas_generadas/LOTE_INTERACTIVO_YYYYMMDD_HHMMSS"  # Ajusta el timestamp
pdf_dir = "/content/PDFs_MANUAL"

# Crear generador de PDFs
pdf_creator = PDFFactura(output_dir=pdf_dir)

# Generar PDFs
json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
print(f"Generando {len(json_files)} PDFs...")

for i, json_file in enumerate(json_files, 1):
    json_path = os.path.join(json_dir, json_file)
    with open(json_path, 'r', encoding='utf-8') as f:
        factura = json.load(f)

    pdf_creator.crear_factura(factura)

    if i % 10 == 0:
        print(f"  Progreso: {i}/{len(json_files)}")

print(f"✅ {len(json_files)} PDFs generados")

# Comprimir y descargar
!cd /content && zip -r PDFs_MANUAL.zip PDFs_MANUAL/
from google.colab import files
files.download('/content/PDFs_MANUAL.zip')
```

---

## ✅ VENTAJAS DEL MODO INTERACTIVO

✅ **Flexible:** Decides exactamente cuántas facturas de cada tipo
✅ **Confirmación:** Muestra resumen antes de generar
✅ **Control de PDFs:** Decides si generar PDFs o solo JSONs
✅ **Estadísticas detalladas:** Muestra distribución de páginas, monedas, tipos
✅ **Nombres claros:** Los archivos incluyen número de páginas en el nombre
✅ **Cancelable:** Puedes cancelar en cualquier momento con Ctrl+C

---

## 📞 EJEMPLOS DE USO

### Ejemplo 1: Dataset pequeño para pruebas
```
¿Cuántas facturas de 1 página deseas generar? (0-1000): 10
¿Cuántas facturas multipágina deseas generar? (0-1000): 5

Resultado: 10 facturas de 1 pág + 5 multipágina = 15 total
```

### Ejemplo 2: Dataset balanceado
```
¿Cuántas facturas de 1 página deseas generar? (0-1000): 50
¿Cuántas facturas multipágina deseas generar? (0-1000): 50

Resultado: 50 facturas de 1 pág + 50 multipágina = 100 total
```

### Ejemplo 3: Solo facturas de 1 página
```
¿Cuántas facturas de 1 página deseas generar? (0-1000): 100
¿Cuántas facturas multipágina deseas generar? (0-1000): 0

Resultado: 100 facturas de 1 pág = 100 total
```

### Ejemplo 4: Solo facturas multipágina
```
¿Cuántas facturas de 1 página deseas generar? (0-1000): 0
¿Cuántas facturas multipágina deseas generar? (0-1000): 200

Resultado: 200 facturas multipágina = 200 total
```

---

## 🎉 ¡LISTO PARA USAR!

Ahora puedes generar facturas de forma interactiva en Google Colab. El script te guiará paso a paso.

**Branch:** `claude/fix-json-parsing-011CUyGo75ZndGpbT9KKAMXw`
**Script:** `COLAB_GENERAR_INTERACTIVO.py`
