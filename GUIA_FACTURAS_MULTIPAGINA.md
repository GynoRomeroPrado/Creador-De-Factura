# 📄 GUÍA: GENERAR FACTURAS CON MÚLTIPLES PÁGINAS

## 🎯 Objetivo

Generar facturas con **40-80 items** que produzcan PDFs de **3-6 páginas**.

---

## 📊 Páginas por Número de Items

| Items | Páginas Estimadas |
|-------|-------------------|
| 40    | 3 páginas         |
| 50    | 4 páginas         |
| 60    | 5 páginas         |
| 70    | 5 páginas         |
| 80    | 6 páginas         |

**Nota:** Cada página puede contener aproximadamente 15-18 items.

---

## 🚀 OPCIÓN 1: GOOGLE COLAB (Recomendado)

### Paso 1: Abrir Google Colab

1. Ve a [Google Colab](https://colab.research.google.com/)
2. Crea un nuevo notebook o abre uno existente

### Paso 2: Copiar y ejecutar el script

Copia el contenido de `COLAB_GENERAR_MULTIPAGINA.py` en una celda de Colab y ejecútalo.

**O simplemente ejecuta:**

```python
# Clonar repositorio
!git clone https://github.com/GynoRomeroPrado/Creador-De-Factura.git /content/Creador-De-Factura
%cd /content/Creador-De-Factura

# Actualizar a la última versión con correcciones
!git pull origin claude/fix-json-parsing-011CUyGo75ZndGpbT9KKAMXw

# Instalar reportlab
!pip install reportlab

# Generar facturas multipágina
!python COLAB_GENERAR_MULTIPAGINA.py
```

### Paso 3: Descargar archivos

```python
from google.colab import files

# Opción 1: Descargar todo comprimido
!zip -r /content/facturas_multipagina.zip /content/PDFs_MULTIPAGINA /content/JSONs_MULTIPAGINA
files.download('/content/facturas_multipagina.zip')

# Opción 2: Descargar PDF individual
files.download('/content/PDFs_MULTIPAGINA/nombre_del_pdf.pdf')
```

---

## 💻 OPCIÓN 2: LOCAL (Sin PDFs, solo JSONs)

Si no tienes reportlab instalado localmente, puedes generar solo los JSONs:

```bash
cd /ruta/a/Creador-De-Factura
python GENERAR_FACTURAS_MULTIPAGINA_JSON.py
```

Esto generará:
- ✅ 7 facturas en formato JSON (InvoiceX v5.5)
- ✅ Ubicación: `facturas_generadas/JSONs_MULTIPAGINA/`
- ✅ De 3 a 6 páginas estimadas

Luego puedes subir los JSONs a Google Colab para generar los PDFs.

---

## 📝 OPCIÓN 3: GENERAR MANUALMENTE

### Código Python (Local o Colab)

```python
from src.generator import FacturaGenerator
from src.pdf_creator import PDFCreator
from src.json_exporter import JSONExporter

# Inicializar
gen = FacturaGenerator()
pdf_creator = PDFCreator(output_dir="mis_pdfs")
json_exporter = JSONExporter(output_dir="mis_jsons")

# Generar factura con MUCHOS items
factura = gen.generar_factura(
    tipo_factura='compra_grande',  # Importante: usar este tipo
    num_items=60,                   # 60 items = ~5 páginas
    categoria_items='construccion', # O 'servicios', None para mixto
    con_credito=True,               # True/False
    moneda='PEN'                    # 'PEN', 'USD', 'EUR'
)

# Generar PDF (solo funciona si reportlab está instalado)
pdf_path = pdf_creator.crear_factura(factura)
print(f"PDF: {pdf_path}")

# Generar JSON (formato InvoiceX v5.5)
json_path = json_exporter.exportar_factura(factura)
print(f"JSON: {json_path}")
```

---

## 🎨 PERSONALIZACIÓN

### Controlar número de items

```python
# 3 páginas (40 items)
factura = gen.generar_factura(tipo_factura='compra_grande', num_items=40)

# 4 páginas (50 items)
factura = gen.generar_factura(tipo_factura='compra_grande', num_items=50)

# 5 páginas (60 items)
factura = gen.generar_factura(tipo_factura='compra_grande', num_items=60)

# 6 páginas (80 items)
factura = gen.generar_factura(tipo_factura='compra_grande', num_items=80)
```

### Controlar categoría de items

```python
# Construcción
factura = gen.generar_factura(
    tipo_factura='compra_grande',
    num_items=50,
    categoria_items='construccion'
)

# Servicios
factura = gen.generar_factura(
    tipo_factura='compra_grande',
    num_items=50,
    categoria_items='servicios'
)

# Mixto (construcción + servicios + productos)
factura = gen.generar_factura(
    tipo_factura='compra_grande',
    num_items=50,
    categoria_items=None  # None = mixto
)
```

### Controlar forma de pago

```python
# Al contado
factura = gen.generar_factura(
    tipo_factura='compra_grande',
    num_items=50,
    con_credito=False
)

# A crédito (con cuotas escalonadas)
factura = gen.generar_factura(
    tipo_factura='compra_grande',
    num_items=50,
    con_credito=True
)
```

### Controlar moneda

```python
# Soles
factura = gen.generar_factura(tipo_factura='compra_grande', num_items=50, moneda='PEN')

# Dólares
factura = gen.generar_factura(tipo_factura='compra_grande', num_items=50, moneda='USD')

# Euros
factura = gen.generar_factura(tipo_factura='compra_grande', num_items=50, moneda='EUR')
```

---

## 📊 EJEMPLOS YA GENERADOS

Se han generado **7 facturas de ejemplo** con múltiples páginas:

| # | Items | Páginas | Archivo |
|---|-------|---------|---------|
| 1 | 50    | 4       | `Factura_compra_grande_F785_280824_20250913.json` |
| 2 | 45    | 4       | `Factura_compra_grande_F184_687824_20250521.json` |
| 3 | 55    | 4       | `Factura_compra_grande_F403_487989_20251217.json` |
| 4 | 60    | 5       | `Factura_compra_grande_F707_935145_20250318.json` |
| 5 | 40    | 3       | `Factura_compra_grande_F391_017239_20250610.json` |
| 6 | 70    | 5       | `Factura_compra_grande_F741_027366_20250724.json` |
| 7 | 80    | 6       | `Factura_compra_grande_F887_382055_20250901.json` |

**Ubicación:** `facturas_generadas/JSONs_MULTIPAGINA/`

---

## ✅ CARACTERÍSTICAS DE LAS FACTURAS GENERADAS

Todas las facturas cumplen con:

- ✅ **Formato InvoiceX v5.5** (97 campos base + items + cuotas)
- ✅ **Estructura plana** (no anidada)
- ✅ **Coherencia matemática 100%** (subtotal = Σ items)
- ✅ **Monto en letras correcto** (coincide con importe_total)
- ✅ **Ubicación geográfica mapeada** (CHICLAYO→LAMBAYEQUE, etc.)
- ✅ **tipo_documento estandarizado** ("FACTURA ELECTRONICA")
- ✅ **Cuotas escalonadas** (intervalos de 30 días)
- ✅ **Calificación: 100/100**

---

## 🔧 SOLUCIÓN DE PROBLEMAS

### Problema: "ModuleNotFoundError: No module named 'reportlab'"

**Solución:**
```bash
pip install reportlab
```

### Problema: PDFs no se generan

**Causas posibles:**
1. reportlab no instalado → Instalar con `pip install reportlab`
2. No tienes permisos de escritura → Cambiar `output_dir`
3. Error en datos de factura → Verificar que `factura` sea válida

**Solución alternativa:** Genera solo JSONs con `GENERAR_FACTURAS_MULTIPAGINA_JSON.py`

### Problema: Quiero más de 6 páginas

**Solución:** Aumenta el número de items:
```python
factura = gen.generar_factura(
    tipo_factura='compra_grande',
    num_items=100  # ~7 páginas
)
```

---

## 📞 AYUDA ADICIONAL

### Ver items de una factura

```python
print(f"Total items: {len(factura['items'])}")
for i, item in enumerate(factura['items'][:5], 1):
    print(f"{i}. {item['descripcion']} - {item['cantidad']} x {item['precio_unitario']}")
```

### Ver estructura del JSON

```python
import json

with open('factura.json', 'r') as f:
    data = json.load(f)

print(f"Campos principales: {len(data)}")
print(f"Items: {len(data['items'])}")
print(f"Cuotas: {len(data.get('cuotas', []))}")
print(f"Importe total: {data['importe_total']}")
```

### Verificar páginas de un PDF

```python
from PyPDF2 import PdfReader

reader = PdfReader('factura.pdf')
print(f"Páginas reales: {len(reader.pages)}")
```

---

## 🎯 QUICK START

**La forma más rápida de generar facturas multipágina:**

### En Google Colab:
```python
!git clone https://github.com/GynoRomeroPrado/Creador-De-Factura.git /content/Creador-De-Factura
%cd /content/Creador-De-Factura
!pip install reportlab
!python COLAB_GENERAR_MULTIPAGINA.py
```

### En Local:
```bash
git clone https://github.com/GynoRomeroPrado/Creador-De-Factura.git
cd Creador-De-Factura
python GENERAR_FACTURAS_MULTIPAGINA_JSON.py
```

---

**Última actualización:** 2025-01-10
**Branch:** `claude/fix-json-parsing-011CUyGo75ZndGpbT9KKAMXw`
