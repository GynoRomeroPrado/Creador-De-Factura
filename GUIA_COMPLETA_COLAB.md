# 📚 GUÍA COMPLETA Y EXTENSA - USO EN GOOGLE COLAB

## 📋 ÍNDICE

1. [Introducción](#introducción)
2. [Preparación del Entorno](#preparación-del-entorno)
3. [Método 1: Generador Interactivo (RECOMENDADO)](#método-1-generador-interactivo)
4. [Método 2: Scripts de Lote Predefinidos](#método-2-scripts-de-lote-predefinidos)
5. [Generación de PDFs](#generación-de-pdfs)
6. [Descarga de Archivos](#descarga-de-archivos)
7. [Verificación de Calidad](#verificación-de-calidad)
8. [Troubleshooting](#troubleshooting)
9. [Ejemplos Prácticos Completos](#ejemplos-prácticos-completos)

---

## 1. INTRODUCCIÓN

Este sistema genera facturas electrónicas peruanas con formato InvoiceX v5.5 (100/100 de calidad).

### ✅ Características Principales

- **Facturas de 1 página:** 10-15 items por factura
- **Facturas multipágina:** 3-6 páginas, 40-80 items por factura
- **Emails realistas:** Coherentes con el tipo de empresa (hoteles→@hotel.pe, seguros→@seguros.pe)
- **RUCs válidos:** 11 dígitos con dígito verificador
- **Sin superposiciones:** Texto perfectamente espaciado en PDFs
- **Descripciones completas:** Múltiples líneas, sin truncamiento
- **Formato perfecto:** InvoiceX v5.5 100/100

---

## 2. PREPARACIÓN DEL ENTORNO

### Paso 1: Abrir Google Colab

1. Ve a https://colab.research.google.com/
2. Crea un nuevo notebook: `File > New notebook`
3. Cambia el nombre: `Generador_Facturas_Perú`

### Paso 2: Clonar el Repositorio

Copia y pega este código en una celda de Colab:

```python
# Clonar el repositorio
!git clone https://github.com/GynoRomeroPrado/Creador-De-Factura.git

# Ir al directorio del proyecto
%cd Creador-De-Factura

# Cambiar a la rama correcta
!git checkout claude/fix-json-parsing-011CUyGo75ZndGpbT9KKAMXw

# Actualizar a la última versión
!git pull origin claude/fix-json-parsing-011CUyGo75ZndGpbT9KKAMXw
```

**Presiona:** `Shift + Enter` para ejecutar

**Salida esperada:**
```
Cloning into 'Creador-De-Factura'...
remote: Enumerating objects: 1234, done.
/content/Creador-De-Factura
Already on 'claude/fix-json-parsing-011CUyGo75ZndGpbT9KKAMXw'
Already up to date.
```

### Paso 3: Instalar Dependencias

```python
# Instalar reportlab (necesario para generar PDFs)
!pip install reportlab -q

print("✅ Dependencias instaladas correctamente")
```

**Nota:** `-q` hace que la instalación sea silenciosa (sin mucho output)

---

## 3. MÉTODO 1: GENERADOR INTERACTIVO (RECOMENDADO)

Este es el método **MÁS FÁCIL Y FLEXIBLE**. El script te pregunta cuántas facturas quieres.

### 🎯 Paso a Paso Completo

#### Paso 1: Ejecutar el Generador Interactivo

```python
# Ejecutar el script interactivo
!python COLAB_GENERAR_INTERACTIVO.py
```

#### Paso 2: Responder las Preguntas

El script te hará estas preguntas:

**Pregunta 1: Facturas de 1 página**
```
📄 FACTURAS DE 1 PÁGINA (10-15 items cada una)
────────────────────────────────────────────────────────────────────────────────
¿Cuántas facturas de 1 página deseas generar? (0-1000):
```

**Respuestas sugeridas:**
- Para pruebas: `5` o `10`
- Para dataset pequeño: `50`
- Para dataset mediano: `100`
- Para dataset grande: `500`

**Ejemplo:** Escribe `50` y presiona Enter

---

**Pregunta 2: Facturas multipágina**
```
📚 FACTURAS MULTIPÁGINA (3-6 páginas, 40-80 items cada una)
────────────────────────────────────────────────────────────────────────────────
¿Cuántas facturas multipágina deseas generar? (0-1000):
```

**Respuestas sugeridas:**
- Para pruebas: `5` o `10`
- Para dataset pequeño: `20`
- Para dataset mediano: `50`
- Para dataset grande: `200`

**Ejemplo:** Escribe `20` y presiona Enter

---

**Pregunta 3: Confirmación**
```
================================================================================
                         📊 RESUMEN DE GENERACIÓN
================================================================================
  Facturas de 1 página: 50
  Facturas multipágina: 20
  TOTAL A GENERAR: 70
================================================================================

¿Proceder con la generación? (s/n):
```

**Escribe:** `s` y presiona Enter

---

#### Paso 3: Generación de JSONs

El script comenzará a generar:

```
================================================================================
              📄 GENERANDO 50 FACTURAS DE 1 PÁGINA...
================================================================================
  ✅ Generadas: 10/50 (20.0%)
  ✅ Generadas: 20/50 (40.0%)
  ✅ Generadas: 30/50 (60.0%)
  ✅ Generadas: 40/50 (80.0%)
  ✅ Generadas: 50/50 (100.0%)

================================================================================
              📚 GENERANDO 20 FACTURAS MULTIPÁGINA...
================================================================================
  ✅ Generadas: 10/20 (50.0%) - Última: 55 items (4 pág)
  ✅ Generadas: 20/20 (100.0%) - Última: 72 items (6 pág)
```

**Tiempo estimado:**
- 50 facturas de 1 pág: ~25 segundos
- 20 facturas multipág: ~10 segundos
- **Total:** ~35 segundos

---

#### Paso 4: Estadísticas

Al finalizar, verás:

```
================================================================================
                      ✅ GENERACIÓN DE JSONs COMPLETADA
================================================================================

📊 ESTADÍSTICAS:
────────────────────────────────────────────────────────────────────────────────
  Total generado: 70
  Facturas de 1 página: 50
  Facturas multipágina: 20

  Distribución por páginas:
    - 1 página: 50 facturas
    - 3 páginas: 5 facturas
    - 4 páginas: 6 facturas
    - 5 páginas: 5 facturas
    - 6 páginas: 4 facturas

  Tipos:
    - Con descuento: 18
    - Con crédito: 35

  Monedas:
    - PEN (Soles): 25
    - USD (Dólares): 22
    - EUR (Euros): 23

📁 JSONs guardados en: facturas_generadas/LOTE_INTERACTIVO_20250113_143025
```

---

#### Paso 5: Generar PDFs (Opcional)

El script preguntará:

```
================================================================================
                           📄 GENERACIÓN DE PDFs
================================================================================

¿Deseas generar los PDFs ahora? (s/n):
```

**Opciones:**

**Opción A: Generar PDFs inmediatamente (recomendado)**
- Escribe: `s` y presiona Enter
- El script generará todos los PDFs automáticamente
- Los comprimirá en un archivo ZIP
- Mostrará progreso cada 10 PDFs

**Opción B: Generar PDFs después**
- Escribe: `n` y presiona Enter
- Solo descarga los JSONs por ahora
- Genera PDFs más tarde (ver sección 5)

---

**Si elegiste 's' (generar PDFs):**

```
🔧 Generando PDFs...
⏱️  Esto puede tomar varios minutos dependiendo de la cantidad...
  PDFs generados: 10/70 (14.3%)
  PDFs generados: 20/70 (28.6%)
  PDFs generados: 30/70 (42.9%)
  PDFs generados: 40/70 (57.1%)
  PDFs generados: 50/70 (71.4%)
  PDFs generados: 60/70 (85.7%)
  PDFs generados: 70/70 (100.0%)

✅ 70 PDFs generados en /content/PDFs_LOTE_20250113_143025

📦 Comprimiendo PDFs para descarga...

⬇️  Para descargar los PDFs, ejecuta:
from google.colab import files
files.download('/content/PDFs_LOTE_20250113_143025.zip')
```

**Tiempo estimado para PDFs:**
- 70 facturas: ~3-4 minutos
- 100 facturas: ~5 minutos
- 500 facturas: ~25 minutos

---

#### Paso 6: Descargar los PDFs

En una **NUEVA CELDA**, copia y pega:

```python
from google.colab import files
files.download('/content/PDFs_LOTE_20250113_143025.zip')
```

**⚠️ IMPORTANTE:** Cambia `20250113_143025` por el timestamp que te mostró el script

**O usa este código que encuentra automáticamente el archivo más reciente:**

```python
import os
from google.colab import files

# Buscar el ZIP más reciente
archivos_zip = [f for f in os.listdir('/content') if f.startswith('PDFs_LOTE_') and f.endswith('.zip')]
if archivos_zip:
    archivo_mas_reciente = sorted(archivos_zip)[-1]
    print(f"📦 Descargando: {archivo_mas_reciente}")
    files.download(f'/content/{archivo_mas_reciente}')
    print("✅ Descarga iniciada")
else:
    print("❌ No se encontró ningún archivo ZIP de PDFs")
```

**Presiona:** `Shift + Enter`

El navegador iniciará la descarga automáticamente.

---

### 📊 Resumen del Método Interactivo

**Ventajas:**
✅ Muy fácil de usar (solo responder preguntas)
✅ Flexible (decides cuántas de cada tipo)
✅ Confirmación antes de generar
✅ Estadísticas detalladas
✅ Nombres de archivo claros (`FACTURA_0001_3PAG_...`)
✅ Compresión automática de PDFs

**Desventajas:**
❌ Requiere interacción (no se puede automatizar 100%)

---

## 4. MÉTODO 2: SCRIPTS DE LOTE PREDEFINIDOS

Si prefieres scripts **sin interacción** con cantidades predefinidas.

### Opción A: Lote de 1 Página (50 facturas por defecto)

```python
# Generar 50 facturas de 1 página
!python GENERAR_LOTE_PAGINA_UNICA.py
```

**Para cambiar la cantidad:**

1. Edita el archivo antes de ejecutar:

```python
# Ver la configuración actual
!grep "CANTIDAD_FACTURAS" GENERAR_LOTE_PAGINA_UNICA.py

# Cambiar a 100 facturas
!sed -i 's/CANTIDAD_FACTURAS = 50/CANTIDAD_FACTURAS = 100/' GENERAR_LOTE_PAGINA_UNICA.py

# Ejecutar
!python GENERAR_LOTE_PAGINA_UNICA.py
```

### Opción B: Lote Multipágina (100 facturas por defecto)

```python
# Generar 100 facturas multipágina
!python GENERAR_LOTE_MULTIPAGINA.py
```

**Para cambiar la cantidad:**

```python
# Cambiar a 200 facturas
!sed -i 's/CANTIDAD_FACTURAS = 100/CANTIDAD_FACTURAS = 200/' GENERAR_LOTE_MULTIPAGINA.py

# Ejecutar
!python GENERAR_LOTE_MULTIPAGINA.py
```

**Para cambiar la distribución de páginas:**

```python
# Ver distribución actual
!grep -A 5 "DISTRIBUCION_PAGINAS" GENERAR_LOTE_MULTIPAGINA.py

# Editar manualmente si quieres otra distribución
# Ejemplo: Solo facturas de 6 páginas
!python -c "
with open('GENERAR_LOTE_MULTIPAGINA.py', 'r') as f:
    content = f.read()

content = content.replace(
    '''DISTRIBUCION_PAGINAS = {
    3: 0.25,
    4: 0.25,
    5: 0.25,
    6: 0.25,
}''',
    '''DISTRIBUCION_PAGINAS = {
    3: 0.0,
    4: 0.0,
    5: 0.0,
    6: 1.0,
}''')

with open('GENERAR_LOTE_MULTIPAGINA.py', 'w') as f:
    f.write(content)
"

!python GENERAR_LOTE_MULTIPAGINA.py
```

---

## 5. GENERACIÓN DE PDFs

Si generaste solo JSONs y ahora quieres los PDFs:

### Método Manual: Generar PDFs desde JSONs

```python
import os
import json
from src.pdf_creator import PDFFactura

# =========================================================================
# CONFIGURACIÓN: Cambia estos valores según tu caso
# =========================================================================

# Carpeta donde están los JSONs (cambia el timestamp)
json_dir = "facturas_generadas/LOTE_INTERACTIVO_20250113_143025"

# Carpeta donde se guardarán los PDFs
pdf_dir = "/content/PDFs_MANUAL"

# =========================================================================

# Crear generador de PDFs
pdf_creator = PDFFactura(output_dir=pdf_dir)

# Encontrar todos los JSONs
json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
total = len(json_files)

print(f"📄 Generando PDFs para {total} facturas...")
print(f"📁 JSONs en: {json_dir}")
print(f"📁 PDFs en: {pdf_dir}")
print("⏱️  Esto puede tomar varios minutos...\n")

# Generar PDFs
for i, json_file in enumerate(json_files, 1):
    json_path = os.path.join(json_dir, json_file)

    # Leer JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        factura = json.load(f)

    # Crear PDF
    pdf_path = pdf_creator.crear_factura(factura)

    # Mostrar progreso cada 10 facturas
    if i % 10 == 0 or i == total:
        porcentaje = (i / total) * 100
        print(f"  ✅ PDFs generados: {i}/{total} ({porcentaje:.1f}%)")

print(f"\n✅ {total} PDFs generados exitosamente en {pdf_dir}")
```

### Comprimir y Descargar PDFs

```python
# Comprimir PDFs
print("📦 Comprimiendo PDFs...")
!cd /content && zip -r -q PDFs_MANUAL.zip PDFs_MANUAL/

# Descargar
print("⬇️  Iniciando descarga...")
from google.colab import files
files.download('/content/PDFs_MANUAL.zip')

print("✅ Descarga completada")
```

---

## 6. DESCARGA DE ARCHIVOS

### Opción A: Descargar Solo JSONs

```python
import os
from google.colab import files

# Encontrar la carpeta de JSONs más reciente
facturas_dir = "facturas_generadas"
carpetas = [d for d in os.listdir(facturas_dir) if os.path.isdir(os.path.join(facturas_dir, d))]
carpeta_mas_reciente = sorted(carpetas)[-1]
json_dir = os.path.join(facturas_dir, carpeta_mas_reciente)

print(f"📁 Comprimiendo JSONs de: {json_dir}")

# Comprimir
!cd facturas_generadas && zip -r -q ../{carpeta_mas_reciente}.zip {carpeta_mas_reciente}/

# Descargar
files.download(f'/content/Creador-De-Factura/{carpeta_mas_reciente}.zip')

print("✅ JSONs descargados")
```

### Opción B: Descargar PDFs y JSONs Juntos

```python
# Comprimir ambos
!zip -r -q TODO_FACTURAS.zip facturas_generadas/ PDFs_*/

# Descargar
from google.colab import files
files.download('/content/Creador-De-Factura/TODO_FACTURAS.zip')
```

### Opción C: Listar Archivos para Descarga Selectiva

```python
import os

print("📁 ARCHIVOS DISPONIBLES PARA DESCARGA:\n")

# Listar ZIPs
zips = [f for f in os.listdir('/content') if f.endswith('.zip')]
if zips:
    print("🗜️  Archivos ZIP:")
    for z in sorted(zips):
        size_mb = os.path.getsize(f'/content/{z}') / (1024 * 1024)
        print(f"  - {z} ({size_mb:.1f} MB)")

print("\n📂 Carpetas de facturas:")
for carpeta in sorted(os.listdir('facturas_generadas')):
    if os.path.isdir(f'facturas_generadas/{carpeta}'):
        num_archivos = len(os.listdir(f'facturas_generadas/{carpeta}'))
        print(f"  - {carpeta} ({num_archivos} archivos)")
```

**Para descargar un archivo específico:**

```python
from google.colab import files
files.download('/content/nombre_del_archivo.zip')  # Cambia el nombre
```

---

## 7. VERIFICACIÓN DE CALIDAD

### Verificar JSONs Generados

```python
import json
import os

# Carpeta de JSONs (cambia según tu caso)
json_dir = "facturas_generadas/LOTE_INTERACTIVO_20250113_143025"

json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
print(f"📊 VERIFICANDO {len(json_files)} FACTURAS...\n")

# Verificar 5 facturas de muestra
for json_file in json_files[:5]:
    with open(os.path.join(json_dir, json_file), 'r') as f:
        factura = json.load(f)

    print(f"{'='*80}")
    print(f"📄 {json_file}")
    print(f"{'='*80}")
    print(f"  Razón Social: {factura['emisor']['razon_social']}")
    print(f"  RUC: {factura['emisor']['ruc']} ({len(factura['emisor']['ruc'])} dígitos)")
    print(f"  Email: {factura['emisor']['email']}")
    print(f"  Items: {len(factura['items'])}")
    print(f"  Total: {factura['simbolo_moneda']} {factura['total']:.2f}")
    print(f"  Moneda: {factura['moneda']}")
    print(f"  Con crédito: {'Sí' if factura['con_credito'] else 'No'}")

    # Verificar RUC
    if len(factura['emisor']['ruc']) != 11:
        print(f"  ⚠️  ERROR: RUC no tiene 11 dígitos!")

    # Verificar email
    if any(d in factura['emisor']['email'] for d in ['@hotmail', '@gmail', '@yahoo']):
        print(f"  ⚠️  ADVERTENCIA: Email parece personal")

    print()

print("✅ Verificación completada")
```

### Verificar Descripciones de Items

```python
import json
import os

json_dir = "facturas_generadas/LOTE_INTERACTIVO_20250113_143025"
json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]

# Tomar una factura de muestra
with open(os.path.join(json_dir, json_files[0]), 'r') as f:
    factura = json.load(f)

print(f"📋 DESCRIPCIONES DE ITEMS (Factura de muestra):\n")

for i, item in enumerate(factura['items'][:10], 1):
    desc = item['descripcion']
    largo = len(desc)
    print(f"{i:2d}. [{largo:3d} chars] {desc}")

print(f"\n💡 Las descripciones largas (>35 chars) se mostrarán en múltiples líneas en el PDF")
```

---

## 8. TROUBLESHOOTING

### Problema 1: "ModuleNotFoundError: No module named 'src'"

**Causa:** No estás en el directorio correcto

**Solución:**
```python
# Verificar directorio actual
!pwd

# Si no estás en /content/Creador-De-Factura, ve allí
%cd /content/Creador-De-Factura

# Verificar que los archivos estén ahí
!ls -la src/
```

### Problema 2: "ModuleNotFoundError: No module named 'reportlab'"

**Causa:** reportlab no está instalado

**Solución:**
```python
!pip install reportlab
```

### Problema 3: El script interactivo no pregunta nada

**Causa:** Los scripts interactivos no funcionan bien con `!python`

**Solución:** Usa el Método 2 (scripts de lote predefinidos)

**O ejecuta en modo no interactivo:**
```python
# Crear un script que responda automáticamente
!echo "50\n20\ns\ns" | python COLAB_GENERAR_INTERACTIVO.py
```

Esto equivale a:
- 50 facturas de 1 página
- 20 facturas multipágina
- s (confirmar)
- s (generar PDFs)

### Problema 4: "git: command not found"

**Causa:** Git no está disponible (raro en Colab)

**Solución:** Descarga el ZIP del repositorio

```python
!wget https://github.com/GynoRomeroPrado/Creador-De-Factura/archive/refs/heads/claude/fix-json-parsing-011CUyGo75ZndGpbT9KKAMXw.zip
!unzip claude/fix-json-parsing-011CUyGo75ZndGpbT9KKAMXw.zip
%cd Creador-De-Factura-claude-fix-json-parsing-011CUyGo75ZndGpbT9KKAMXw
```

### Problema 5: Los PDFs tienen superposiciones

**Causa:** Código desactualizado

**Solución:**
```python
# Actualizar el código
%cd /content/Creador-De-Factura
!git pull origin claude/fix-json-parsing-011CUyGo75ZndGpbT9KKAMXw

# Regenerar las facturas
!python COLAB_GENERAR_INTERACTIVO.py
```

### Problema 6: La descarga no inicia

**Causa:** Bloqueador de pop-ups del navegador

**Solución:**
1. Permite pop-ups en el navegador
2. O haz clic derecho en la celda → "Show output in fullscreen"
3. Vuelve a ejecutar la celda de descarga

### Problema 7: Archivo ZIP muy grande

**Causa:** Muchos PDFs (los PDFs pesan más que JSONs)

**Soluciones:**

**Opción A: Descargar solo JSONs**
```python
# Los JSONs pesan ~10KB cada uno vs ~50KB de PDFs
!cd facturas_generadas && zip -r ../JSONs_SOLO.zip */
from google.colab import files
files.download('/content/Creador-De-Factura/JSONs_SOLO.zip')
```

**Opción B: Dividir en partes**
```python
# Comprimir en partes de 100 MB
!zip -r -s 100m PDFs_PARTES.zip PDFs_LOTE_*/
# Esto creará PDFs_PARTES.z01, PDFs_PARTES.z02, etc.

# Descargar cada parte
from google.colab import files
files.download('/content/PDFs_PARTES.zip')
files.download('/content/PDFs_PARTES.z01')
# etc.
```

**Opción C: Subir a Google Drive**
```python
# Montar Google Drive
from google.colab import drive
drive.mount('/content/drive')

# Copiar archivos a Drive
!cp -r /content/PDFs_LOTE_* /content/drive/MyDrive/

print("✅ Archivos copiados a Google Drive")
```

---

## 9. EJEMPLOS PRÁCTICOS COMPLETOS

### Ejemplo 1: Dataset Pequeño para Pruebas (15 facturas)

```python
# 1. Preparar entorno
%cd /content
!git clone https://github.com/GynoRomeroPrado/Creador-De-Factura.git
%cd Creador-De-Factura
!git checkout claude/fix-json-parsing-011CUyGo75ZndGpbT9KKAMXw
!pip install reportlab -q

# 2. Generar facturas (modo automático)
# 10 de 1 página + 5 multipágina
!echo "10\n5\ns\ns" | python COLAB_GENERAR_INTERACTIVO.py

# 3. Descargar
from google.colab import files
import os

zips = [f for f in os.listdir('/content') if 'PDFs_LOTE_' in f and f.endswith('.zip')]
if zips:
    files.download(f'/content/{sorted(zips)[-1]}')
```

**Tiempo total:** ~2 minutos

---

### Ejemplo 2: Dataset Mediano Balanceado (100 facturas)

```python
# 1. Preparar entorno
%cd /content
!git clone https://github.com/GynoRomeroPrado/Creador-De-Factura.git
%cd Creador-De-Factura
!git checkout claude/fix-json-parsing-011CUyGo75ZndGpbT9KKAMXw
!pip install reportlab -q

# 2. Generar facturas
# 50 de 1 página + 50 multipágina
!echo "50\n50\ns\ns" | python COLAB_GENERAR_INTERACTIVO.py

# 3. Verificar JSONs
import json
import os

json_dirs = [d for d in os.listdir('facturas_generadas') if 'LOTE_INTERACTIVO' in d]
json_dir = os.path.join('facturas_generadas', sorted(json_dirs)[-1])
json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]

print(f"✅ {len(json_files)} facturas generadas")

# 4. Descargar
from google.colab import files
zips = [f for f in os.listdir('/content') if 'PDFs_LOTE_' in f and f.endswith('.zip')]
files.download(f'/content/{sorted(zips)[-1]}')
```

**Tiempo total:** ~6 minutos

---

### Ejemplo 3: Solo Facturas de 1 Página (200 facturas)

```python
# 1. Preparar entorno
%cd /content
!git clone https://github.com/GynoRomeroPrado/Creador-De-Factura.git
%cd Creador-De-Factura
!git checkout claude/fix-json-parsing-011CUyGo75ZndGpbT9KKAMXw
!pip install reportlab -q

# 2. Modificar script para 200 facturas
!sed -i 's/CANTIDAD_FACTURAS = 50/CANTIDAD_FACTURAS = 200/' GENERAR_LOTE_PAGINA_UNICA.py

# 3. Generar solo JSONs
!python GENERAR_LOTE_PAGINA_UNICA.py

# 4. Generar PDFs manualmente
import os
import json
from src.pdf_creator import PDFFactura

json_dirs = [d for d in os.listdir('facturas_generadas') if 'LOTE_PAGINA_UNICA' in d]
json_dir = os.path.join('facturas_generadas', sorted(json_dirs)[-1])
pdf_dir = "/content/PDFs_200_FACTURAS"

pdf_creator = PDFFactura(output_dir=pdf_dir)
json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]

print(f"Generando {len(json_files)} PDFs...")
for i, json_file in enumerate(json_files, 1):
    with open(os.path.join(json_dir, json_file), 'r') as f:
        factura = json.load(f)
    pdf_creator.crear_factura(factura)
    if i % 20 == 0:
        print(f"  Progreso: {i}/{len(json_files)}")

print("✅ PDFs generados")

# 5. Comprimir y descargar
!cd /content && zip -r -q PDFs_200.zip PDFs_200_FACTURAS/
from google.colab import files
files.download('/content/PDFs_200.zip')
```

**Tiempo total:** ~10 minutos

---

### Ejemplo 4: Solo Facturas Multipágina de 6 Páginas (50 facturas)

```python
# 1. Preparar entorno
%cd /content
!git clone https://github.com/GynoRomeroPrado/Creador-De-Factura.git
%cd Creador-De-Factura
!git checkout claude/fix-json-parsing-011CUyGo75ZndGpbT9KKAMXw
!pip install reportlab -q

# 2. Modificar para 50 facturas, solo 6 páginas
!sed -i 's/CANTIDAD_FACTURAS = 100/CANTIDAD_FACTURAS = 50/' GENERAR_LOTE_MULTIPAGINA.py

# 3. Cambiar distribución a solo 6 páginas
!python -c "
with open('GENERAR_LOTE_MULTIPAGINA.py', 'r') as f:
    content = f.read()

content = content.replace(
    '''DISTRIBUCION_PAGINAS = {
    3: 0.25,
    4: 0.25,
    5: 0.25,
    6: 0.25,
}''',
    '''DISTRIBUCION_PAGINAS = {
    3: 0.0,
    4: 0.0,
    5: 0.0,
    6: 1.0,
}''')

with open('GENERAR_LOTE_MULTIPAGINA.py', 'w') as f:
    f.write(content)
"

# 4. Generar
!python GENERAR_LOTE_MULTIPAGINA.py

# 5. Generar PDFs y descargar
import os, json
from src.pdf_creator import PDFFactura
from google.colab import files

json_dirs = [d for d in os.listdir('facturas_generadas') if 'LOTE_MULTIPAGINA' in d]
json_dir = os.path.join('facturas_generadas', sorted(json_dirs)[-1])
pdf_dir = "/content/PDFs_6PAG"

pdf_creator = PDFFactura(output_dir=pdf_dir)
json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]

for i, json_file in enumerate(json_files, 1):
    with open(os.path.join(json_dir, json_file), 'r') as f:
        factura = json.load(f)
    pdf_creator.crear_factura(factura)
    if i % 10 == 0:
        print(f"PDFs: {i}/{len(json_files)}")

!cd /content && zip -r -q PDFs_6PAG.zip PDFs_6PAG/
files.download('/content/PDFs_6PAG.zip')
```

**Tiempo total:** ~7 minutos

---

### Ejemplo 5: Dataset Grande a Google Drive (500 facturas)

```python
# 1. Preparar entorno
%cd /content
!git clone https://github.com/GynoRomeroPrado/Creador-De-Factura.git
%cd Creador-De-Factura
!git checkout claude/fix-json-parsing-011CUyGo75ZndGpbT9KKAMXw
!pip install reportlab -q

# 2. Montar Google Drive
from google.colab import drive
drive.mount('/content/drive')

# 3. Generar facturas
# 300 de 1 página + 200 multipágina
!echo "300\n200\ns\nn" | python COLAB_GENERAR_INTERACTIVO.py

# Nota: ponemos 'n' en PDFs para generarlos después

# 4. Copiar JSONs a Drive
!cp -r facturas_generadas/LOTE_INTERACTIVO_* /content/drive/MyDrive/

print("✅ JSONs copiados a Google Drive")

# 5. Generar PDFs en lotes y copiar a Drive
import os, json
from src.pdf_creator import PDFFactura

json_dirs = [d for d in os.listdir('facturas_generadas') if 'LOTE_INTERACTIVO' in d]
json_dir = os.path.join('facturas_generadas', sorted(json_dirs)[-1])
json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]

# Generar en lotes de 100
for lote in range(0, len(json_files), 100):
    pdf_dir = f"/content/drive/MyDrive/PDFs_LOTE_{lote//100 + 1}"
    pdf_creator = PDFFactura(output_dir=pdf_dir)

    for json_file in json_files[lote:lote+100]:
        with open(os.path.join(json_dir, json_file), 'r') as f:
            factura = json.load(f)
        pdf_creator.crear_factura(factura)

    print(f"✅ Lote {lote//100 + 1} completado ({lote+100}/{len(json_files)})")

print("✅ Todos los PDFs guardados en Google Drive")
```

**Tiempo total:** ~30-40 minutos
**Ventaja:** No necesitas descargar, todo queda en Drive

---

## 📌 RESUMEN RÁPIDO

### Para empezar rápidamente:

```python
# COPIA Y PEGA ESTO EN COLAB (TODO EN UNA CELDA)

# 1. Clonar repo
%cd /content
!git clone https://github.com/GynoRomeroPrado/Creador-De-Factura.git
%cd Creador-De-Factura
!git checkout claude/fix-json-parsing-011CUyGo75ZndGpbT9KKAMXw
!pip install reportlab -q

# 2. Generar 20 facturas (10 de 1 pág + 10 multipág)
!echo "10\n10\ns\ns" | python COLAB_GENERAR_INTERACTIVO.py

# 3. Descargar
from google.colab import files
import os
zips = [f for f in os.listdir('/content') if 'PDFs_LOTE_' in f and f.endswith('.zip')]
if zips:
    files.download(f'/content/{sorted(zips)[-1]}')
    print("✅ Descarga iniciada")
```

**¡Eso es todo! En 3-5 minutos tendrás tus facturas.**

---

## 🎓 CONCLUSIÓN

Este sistema te permite generar facturas electrónicas peruanas de alta calidad con:

✅ **Facilidad:** Método interactivo o scripts automáticos
✅ **Flexibilidad:** Decides cuántas y de qué tipo
✅ **Realismo:** Emails corporativos, RUCs válidos, datos coherentes
✅ **Calidad:** InvoiceX v5.5 100/100, sin superposiciones
✅ **Velocidad:** Cientos de facturas en minutos

**¿Preguntas? Revisa la sección de Troubleshooting o ejecuta:**

```python
!cat GUIA_COLAB_INTERACTIVO.md
```

---

**Última actualización:** 2025-01-13
**Branch:** `claude/fix-json-parsing-011CUyGo75ZndGpbT9KKAMXw`
**Versión:** 2.0 (Con emails realistas y descripciones multilínea)
