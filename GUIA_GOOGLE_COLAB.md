# 📘 Guía Completa: Uso en Google Colab

## 🎯 Problema Común y Solución

### ❌ PROBLEMA: Guardas JSON con formato incorrecto

Si haces esto en Google Colab:

```python
from src.generator import FacturaGenerator
import json

gen = FacturaGenerator()
factura = gen.generar_factura(tipo_factura='hotel')

# ❌ INCORRECTO - Esto guarda con estructura anidada
with open('factura.json', 'w') as f:
    json.dump(factura, f)
```

Obtendrás JSON con formato **INCORRECTO** (estructura anidada):
```json
{
  "tipo_comprobante": "FACTURA ELECTRÓNICA",
  "emisor": {
    "ruc": "20118960689",
    "razon_social": "..."
  },
  "moneda": "EUR"
}
```

### ✅ SOLUCIÓN: Usa `JSONExporter`

```python
from src.generator import FacturaGenerator
from src.json_exporter import JSONExporter

gen = FacturaGenerator()
exporter = JSONExporter(output_dir="/content/facturas")

factura = gen.generar_factura(tipo_factura='hotel')

# ✅ CORRECTO - Esto guarda en formato InvoiceX v5.5
archivo = exporter.exportar_factura(factura)
```

Obtendrás JSON con formato **CORRECTO** (estructura plana):
```json
{
  "tipo_documento": "FACTURA ELECTRONICA",
  "emisor_ruc": "20118960689",
  "emisor_razon_social": "...",
  "moneda": "SOLES"
}
```

---

## 📋 Instrucciones Paso a Paso para Google Colab

### 1. Configurar el Proyecto

```python
# Clonar el repositorio
!git clone https://github.com/GynoRomeroPrado/Creador-De-Factura.git
%cd Creador-De-Factura

# Instalar dependencias
!pip install reportlab pillow
```

### 2. Importar Módulos

```python
import sys
sys.path.insert(0, '/content/Creador-De-Factura')

from src.generator import FacturaGenerator
from src.json_exporter import JSONExporter
from src.dataset_exporter import DatasetExporter
```

### 3. Generar UNA Factura (Método Simple)

```python
# Inicializar
gen = FacturaGenerator()
exporter = JSONExporter(output_dir="/content/facturas")

# Generar factura de hotel
factura = gen.generar_factura(
    tipo_factura='hotel',  # 'hotel', 'general', 'seguro', 'con_descuento'
    con_credito=True,
    moneda='USD'  # 'PEN', 'USD', 'EUR'
)

# Exportar en formato InvoiceX v5.5 ✅
archivo = exporter.exportar_factura(factura)
print(f"✅ JSON guardado: {archivo}")

# Descargar el archivo
from google.colab import files
files.download(archivo)
```

### 4. Generar MÚLTIPLES Facturas (Método Dataset)

```python
# Inicializar
gen = FacturaGenerator()
exporter = DatasetExporter(base_dir="/content/dataset")

# Crear estructura de dataset
exporter.crear_dataset()

# Generar 10 facturas
for i in range(10):
    factura = gen.generar_factura()
    json_path, pdf_path = exporter.exportar_factura(factura)
    print(f"[{i+1}/10] JSON: {json_path}")

# Comprimir y descargar
!cd /content/dataset && zip -r dataset.zip .
files.download('/content/dataset/dataset.zip')
```

### 5. Generar con PDFs

```python
from src.pdf_creator import PDFFactura

# Inicializar
gen = FacturaGenerator()
json_exporter = JSONExporter(output_dir="/content/facturas")
pdf_creator = PDFFactura(output_dir="/content/facturas")

# Generar factura
factura = gen.generar_factura(tipo_factura='hotel')

# Guardar JSON (formato InvoiceX v5.5)
json_path = json_exporter.exportar_factura(factura)

# Generar PDF
pdf_path = pdf_creator.crear_factura(factura)

print(f"✅ JSON: {json_path}")
print(f"✅ PDF: {pdf_path}")

# Descargar ambos
files.download(json_path)
files.download(pdf_path)
```

---

## 🔍 Verificar que el JSON es Correcto

```python
import json

# Leer el JSON generado
with open(archivo, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Verificar estructura
print("Verificación de formato:")
print(f"  ✅ Estructura plana (emisor_ruc): {'emisor_ruc' in data}")
print(f"  ❌ Estructura anidada (emisor): {'emisor' in data and isinstance(data.get('emisor'), dict)}")
print(f"  ✅ Moneda normalizada: {data.get('moneda')}")
print(f"  ✅ Fecha YYYY-MM-DD: {data.get('fecha_emision')}")
print(f"  ✅ Campos raíz: {len([k for k in data.keys() if k not in ['items', 'cuotas']])}")
print(f"  ✅ Campos por item: {len(data['items'][0]) if data.get('items') else 0}")

# Debe mostrar:
# ✅ Estructura plana: True
# ❌ Estructura anidada: False
# ✅ Moneda: SOLES / DOLARES AMERICANOS / EUROS
# ✅ Campos raíz: 94+
# ✅ Campos por item: 26-27
```

---

## 📝 Scripts Recomendados para Colab

### Script 1: Generar Facturas de Diferentes Tipos

```python
# Copiar todo este bloque en una celda de Colab

import sys
sys.path.insert(0, '/content/Creador-De-Factura')

from src.generator import FacturaGenerator
from src.json_exporter import JSONExporter
from google.colab import files

# Configurar
gen = FacturaGenerator()
exporter = JSONExporter(output_dir="/content/mis_facturas")

tipos = ['hotel', 'general', 'seguro', 'con_descuento']

print("Generando facturas en formato InvoiceX v5.5...\n")

archivos = []
for tipo in tipos:
    factura = gen.generar_factura(tipo_factura=tipo, con_credito=True)
    archivo = exporter.exportar_factura(factura)
    archivos.append(archivo)
    print(f"✅ {tipo.upper()}: {archivo}")

# Comprimir y descargar
!cd /content && zip -r facturas.zip mis_facturas/
files.download('/content/facturas.zip')

print("\n✅ Todas las facturas generadas en formato InvoiceX v5.5")
```

### Script 2: Generar Dataset Completo

```python
# Copiar todo este bloque en una celda de Colab

import sys
sys.path.insert(0, '/content/Creador-De-Factura')

from src.generator import FacturaGenerator
from src.dataset_exporter import DatasetExporter
from google.colab import files

# Configurar
cantidad = 20  # Número de facturas a generar
gen = FacturaGenerator()
exporter = DatasetExporter(base_dir="/content/dataset")

# Crear dataset
exporter.crear_dataset()

print(f"Generando {cantidad} facturas...\n")

for i in range(cantidad):
    # Rotar tipos
    tipos = ['general', 'hotel', 'seguro', 'con_descuento']
    tipo = tipos[i % len(tipos)]

    factura = gen.generar_factura(tipo_factura=tipo)
    json_path, _ = exporter.exportar_factura(factura)

    print(f"[{i+1}/{cantidad}] {tipo.upper()}: {json_path}")

# Comprimir y descargar
!cd /content/dataset && zip -r dataset_completo.zip .
files.download('/content/dataset/dataset_completo.zip')

print("\n✅ Dataset completo generado")
```

---

## ⚠️ Errores Comunes y Soluciones

### Error 1: "Estructura anidada detectada"

**Causa:** Guardas el JSON directamente sin usar `JSONExporter`

```python
# ❌ NO HAGAS ESTO
factura = gen.generar_factura()
with open('factura.json', 'w') as f:
    json.dump(factura, f)
```

**Solución:**

```python
# ✅ HAZ ESTO
factura = gen.generar_factura()
exporter = JSONExporter()
exporter.exportar_factura(factura)
```

### Error 2: "Moneda es PEN en lugar de SOLES"

**Causa:** Lees el diccionario interno en lugar del JSON exportado

**Solución:** Lee el archivo JSON exportado, no el diccionario interno

```python
# ✅ Correcto
archivo = exporter.exportar_factura(factura)
with open(archivo, 'r') as f:
    json_correcto = json.load(f)  # Este tiene moneda normalizada
```

### Error 3: "Fechas con formato ISO (T00:00:00)"

**Causa:** Guardas sin pasar por el exportador

**Solución:** Usa siempre `JSONExporter` o `DatasetExporter`

---

## 📚 Archivos de Referencia

En el repositorio tienes estos archivos útiles:

- `DIFERENCIA_FORMATOS.py` - Muestra diferencia entre incorrecto y correcto
- `generar_factura_simple.py` - Script simple para generar una factura
- `test_json_exporter_corregido.py` - Genera ejemplos de prueba
- `ejemplo_json_correcto.json` - Ejemplo de referencia del formato correcto
- `GUIA-ESTRUCTURA-JSON-FACTURAS.md` - Especificación completa InvoiceX v5.5

---

## 🎯 Resumen: Lo Que DEBES Hacer

1. ✅ **SIEMPRE** usa `JSONExporter` o `DatasetExporter`
2. ✅ **NUNCA** guardes el diccionario interno directamente con `json.dump()`
3. ✅ **VERIFICA** que el JSON tenga `emisor_ruc` (plano) y NO `emisor: {}` (anidado)
4. ✅ **CONFIRMA** que la moneda sea `SOLES` / `DOLARES AMERICANOS` / `EUROS`
5. ✅ **REVISA** que las fechas sean `YYYY-MM-DD` (sin hora)

---

## 📞 Más Ayuda

Si tienes dudas:

1. Lee `PROBLEMA_RESUELTO.md` - Explicación completa del problema
2. Ejecuta `DIFERENCIA_FORMATOS.py` - Ve la diferencia lado a lado
3. Compara tu JSON con `ejemplo_json_correcto.json`
4. Verifica que tu JSON tenga 94+ campos raíz y items con 26-27 campos

---

**Última actualización:** 2025-01-10
**Formato:** InvoiceX v5.5
**Estructura:** Plana con 97 campos
