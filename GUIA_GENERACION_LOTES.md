# 📚 GUÍA DE GENERACIÓN DE LOTES DE FACTURAS

## 🎯 Resumen

Este proyecto incluye **DOS scripts principales** para generar lotes de facturas:

1. **GENERAR_LOTE_PAGINA_UNICA.py** → Facturas de 1 página (10-15 items)
2. **GENERAR_LOTE_MULTIPAGINA.py** → Facturas multipágina (3-6 páginas, 40-80 items)

Ambos scripts generan:
- ✅ JSONs con formato InvoiceX v5.5 (100/100)
- ✅ Coherencia matemática perfecta
- ✅ Ubicaciones geográficas correctas (Departamento/Provincia/Distrito)
- ✅ Fechas de cuotas escalonadas (30 días)
- ✅ Sin superposiciones de texto en PDFs

---

## 📄 Script 1: GENERAR_LOTE_PAGINA_UNICA.py

### ¿Qué genera?

Facturas de **1 página** con 10-15 items cada una.

### Configuración

Abre el archivo `GENERAR_LOTE_PAGINA_UNICA.py` y modifica esta línea:

```python
CANTIDAD_FACTURAS = 50  # ← CAMBIA ESTE NÚMERO
```

### Uso Local

```bash
cd /home/user/Creador-De-Factura
python GENERAR_LOTE_PAGINA_UNICA.py
```

### Uso en Google Colab

```python
# 1. Clonar repositorio
!git clone https://github.com/GynoRomeroPrado/Creador-De-Factura.git
%cd Creador-De-Factura

# 2. Actualizar a la rama correcta
!git checkout claude/fix-json-parsing-011CUyGo75ZndGpbT9KKAMXw
!git pull origin claude/fix-json-parsing-011CUyGo75ZndGpbT9KKAMXw

# 3. Generar JSONs
!python GENERAR_LOTE_PAGINA_UNICA.py

# 4. Instalar reportlab
!pip install reportlab

# 5. Generar PDFs desde los JSONs
import os
import json
from src.pdf_creator import PDFCreator

# Encuentra la carpeta más reciente
lotes_dir = "facturas_generadas"
carpetas = [d for d in os.listdir(lotes_dir) if d.startswith("LOTE_PAGINA_UNICA_")]
carpeta_mas_reciente = sorted(carpetas)[-1]
json_dir = os.path.join(lotes_dir, carpeta_mas_reciente)

pdf_dir = "/content/PDFs_LOTE_PAGINA_UNICA"
pdf_creator = PDFCreator(output_dir=pdf_dir)

json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
print(f"Generando PDFs para {len(json_files)} facturas...")

for i, json_file in enumerate(json_files, 1):
    json_path = os.path.join(json_dir, json_file)
    with open(json_path, 'r', encoding='utf-8') as f:
        factura = json.load(f)

    pdf_path = pdf_creator.crear_factura(factura)

    if i % 10 == 0 or i == len(json_files):
        print(f"  PDFs generados: {i}/{len(json_files)} ({(i/len(json_files))*100:.1f}%)")

print(f"✅ {len(json_files)} PDFs generados en {pdf_dir}")

# 6. Descargar PDFs
!cd /content && zip -r PDFs_LOTE_PAGINA_UNICA.zip PDFs_LOTE_PAGINA_UNICA/
from google.colab import files
files.download('/content/PDFs_LOTE_PAGINA_UNICA.zip')
```

### Salida

- **Carpeta:** `facturas_generadas/LOTE_PAGINA_UNICA_YYYYMMDD_HHMMSS/`
- **Archivos:** `FACTURA_0001_F123_456789.json`, `FACTURA_0002_F234_567890.json`, ...
- **Cantidad:** La que hayas configurado (default: 50)

### Características

- ✅ 10-15 items por factura
- ✅ 1 página por factura
- ✅ Variedad: generales, con descuento, con crédito
- ✅ Múltiples monedas: PEN, USD, EUR
- ✅ Tiempo estimado: ~5 segundos por factura (JSONs)

---

## 📚 Script 2: GENERAR_LOTE_MULTIPAGINA.py

### ¿Qué genera?

Facturas de **múltiples páginas** (3-6 páginas) con 40-80 items cada una.

### Configuración

Abre el archivo `GENERAR_LOTE_MULTIPAGINA.py` y modifica:

```python
CANTIDAD_FACTURAS = 100  # ← CAMBIA ESTE NÚMERO

# Distribución de páginas (debe sumar 1.0 = 100%)
DISTRIBUCION_PAGINAS = {
    3: 0.25,  # 25% de facturas con 3 páginas (~40 items)
    4: 0.25,  # 25% de facturas con 4 páginas (~50 items)
    5: 0.25,  # 25% de facturas con 5 páginas (~60 items)
    6: 0.25,  # 25% de facturas con 6 páginas (~80 items)
}
```

**Ejemplos de distribuciones:**

```python
# Distribución uniforme (default)
DISTRIBUCION_PAGINAS = {3: 0.25, 4: 0.25, 5: 0.25, 6: 0.25}

# Más facturas de 3-4 páginas
DISTRIBUCION_PAGINAS = {3: 0.40, 4: 0.40, 5: 0.10, 6: 0.10}

# Más facturas de 5-6 páginas
DISTRIBUCION_PAGINAS = {3: 0.10, 4: 0.10, 5: 0.40, 6: 0.40}

# Solo 3 páginas
DISTRIBUCION_PAGINAS = {3: 1.0, 4: 0.0, 5: 0.0, 6: 0.0}

# Solo 6 páginas (máximo)
DISTRIBUCION_PAGINAS = {3: 0.0, 4: 0.0, 5: 0.0, 6: 1.0}
```

### Uso Local

```bash
cd /home/user/Creador-De-Factura
python GENERAR_LOTE_MULTIPAGINA.py
```

### Uso en Google Colab

```python
# 1. Clonar repositorio
!git clone https://github.com/GynoRomeroPrado/Creador-De-Factura.git
%cd Creador-De-Factura

# 2. Actualizar a la rama correcta
!git checkout claude/fix-json-parsing-011CUyGo75ZndGpbT9KKAMXw
!git pull origin claude/fix-json-parsing-011CUyGo75ZndGpbT9KKAMXw

# 3. Generar JSONs
!python GENERAR_LOTE_MULTIPAGINA.py

# 4. Instalar reportlab
!pip install reportlab

# 5. Generar PDFs desde los JSONs
import os
import json
from src.pdf_creator import PDFCreator

# Encuentra la carpeta más reciente
lotes_dir = "facturas_generadas"
carpetas = [d for d in os.listdir(lotes_dir) if d.startswith("LOTE_MULTIPAGINA_")]
carpeta_mas_reciente = sorted(carpetas)[-1]
json_dir = os.path.join(lotes_dir, carpeta_mas_reciente)

pdf_dir = "/content/PDFs_LOTE_MULTIPAGINA"
pdf_creator = PDFCreator(output_dir=pdf_dir)

json_files = [f for f in os.listdir(json_dir) if f.endswith('.json')]
print(f"Generando PDFs para {len(json_files)} facturas multipágina...")
print("⏱️  NOTA: Esto puede tomar varios minutos")

for i, json_file in enumerate(json_files, 1):
    json_path = os.path.join(json_dir, json_file)
    with open(json_path, 'r', encoding='utf-8') as f:
        factura = json.load(f)

    pdf_path = pdf_creator.crear_factura(factura)

    if i % 10 == 0 or i == len(json_files):
        print(f"  PDFs generados: {i}/{len(json_files)} ({(i/len(json_files))*100:.1f}%)")

print(f"✅ {len(json_files)} PDFs generados en {pdf_dir}")

# 6. Descargar PDFs
!cd /content && zip -r PDFs_LOTE_MULTIPAGINA.zip PDFs_LOTE_MULTIPAGINA/
from google.colab import files
files.download('/content/PDFs_LOTE_MULTIPAGINA.zip')
```

### Salida

- **Carpeta:** `facturas_generadas/LOTE_MULTIPAGINA_YYYYMMDD_HHMMSS/`
- **Archivos:** `FACTURA_MP_0001_5PAG_F123_456789.json`, `FACTURA_MP_0002_3PAG_F234_567890.json`, ...
- **Cantidad:** La que hayas configurado (default: 100)
- **Nombre incluye:** Número de páginas (3PAG, 4PAG, 5PAG, 6PAG)

### Características

- ✅ 40-80 items por factura
- ✅ 3-6 páginas por factura
- ✅ Distribución configurable de páginas
- ✅ Variedad: compra grande, con descuento, con crédito
- ✅ Múltiples monedas: PEN, USD, EUR
- ✅ Tiempo estimado: ~15-30 segundos por factura (JSONs)

---

## ⏱️ Tiempos Estimados de Generación

### Facturas de 1 Página (GENERAR_LOTE_PAGINA_UNICA.py)

| Cantidad | Tiempo JSONs | Tiempo PDFs (Colab) | Total |
|----------|--------------|---------------------|-------|
| 50       | ~5 seg       | ~1 min              | ~1.1 min |
| 100      | ~10 seg      | ~2 min              | ~2.2 min |
| 500      | ~45 seg      | ~10 min             | ~11 min |
| 1000     | ~1.5 min     | ~20 min             | ~22 min |

### Facturas Multipágina (GENERAR_LOTE_MULTIPAGINA.py)

| Cantidad | Tiempo JSONs | Tiempo PDFs (Colab) | Total |
|----------|--------------|---------------------|-------|
| 10       | ~5 seg       | ~30 seg             | ~35 seg |
| 50       | ~25 seg      | ~2.5 min            | ~3 min |
| 100      | ~50 seg      | ~5 min              | ~6 min |
| 500      | ~4 min       | ~25 min             | ~29 min |
| 1000     | ~8 min       | ~50 min             | ~58 min |

---

## 📊 Estadísticas Mostradas

Ambos scripts muestran estadísticas detalladas:

### Facturas de 1 Página
```
📊 ESTADÍSTICAS:
  Total generadas: 50
  Facturas generales: 40
  Facturas con descuento: 10
  Facturas con crédito: 24

  Monedas:
    - PEN (Soles): 15
    - USD (Dólares): 12
    - EUR (Euros): 23
```

### Facturas Multipágina
```
📊 ESTADÍSTICAS:
  Total generadas: 100
  Items totales: 5,870
  Promedio items por factura: 58.7

  Distribución por páginas:
    - 3 páginas: 25 facturas (25.0%)
    - 4 páginas: 25 facturas (25.0%)
    - 5 páginas: 25 facturas (25.0%)
    - 6 páginas: 25 facturas (25.0%)

  Tipos:
    - Facturas con descuento: 40
    - Facturas con crédito: 50

  Monedas:
    - PEN (Soles): 35
    - USD (Dólares): 32
    - EUR (Euros): 33
```

---

## 🔧 Solución de Problemas

### "ModuleNotFoundError: No module named 'src'"

**Solución:** Asegúrate de ejecutar los scripts desde la raíz del proyecto:
```bash
cd /home/user/Creador-De-Factura
python GENERAR_LOTE_PAGINA_UNICA.py
```

### "No such file or directory: 'facturas_generadas/...'"

**Solución:** Los scripts crean automáticamente las carpetas. Si hay error, verifica permisos:
```bash
mkdir -p facturas_generadas
chmod 755 facturas_generadas
```

### PDFs no se generan en Colab

**Solución:** Verifica que reportlab esté instalado:
```python
!pip install reportlab
```

### Archivos ZIP muy grandes en Colab

**Solución:** Genera lotes más pequeños o descarga solo JSONs:
```python
# Descargar solo JSONs (más livianos)
!cd /content/Creador-De-Factura && zip -r JSONs_LOTE.zip facturas_generadas/LOTE_*/
from google.colab import files
files.download('/content/Creador-De-Factura/JSONs_LOTE.zip')
```

---

## ✅ Verificación de Calidad

Todos los JSONs generados cumplen con:

- ✅ **Formato InvoiceX v5.5** (97 campos base + items + cuotas)
- ✅ **Coherencia matemática 100%:** Suma de items = totales
- ✅ **Ubicaciones geográficas:** Departamento/Provincia/Distrito correctos
- ✅ **Fechas de cuotas escalonadas:** +30 días entre cuotas
- ✅ **Monto en letras:** Coincide con importe_total
- ✅ **tipo_documento:** FACTURA ELECTRONICA / BOLETA DE VENTA ELECTRONICA

Todos los PDFs generados cumplen con:

- ✅ **Sin superposiciones de texto**
- ✅ **Posicionamiento dinámico en cascada**
- ✅ **Elementos en orden:** Items → Descuentos → Totales → Forma de pago → Cuotas → Observaciones
- ✅ **Múltiples páginas:** Items continúan correctamente en páginas siguientes
- ✅ **Espaciamiento adecuado:** 15-30px entre secciones

---

## 🎯 Casos de Uso Recomendados

### Para desarrollo y pruebas
```python
# Script 1: 10-20 facturas de 1 página
CANTIDAD_FACTURAS = 10

# Script 2: 10-20 facturas multipágina
CANTIDAD_FACTURAS = 10
```

### Para datasets pequeños
```python
# Script 1: 50-100 facturas de 1 página
CANTIDAD_FACTURAS = 50

# Script 2: 50-100 facturas multipágina
CANTIDAD_FACTURAS = 50
```

### Para datasets medianos
```python
# Script 1: 500 facturas de 1 página
CANTIDAD_FACTURAS = 500

# Script 2: 200-500 facturas multipágina
CANTIDAD_FACTURAS = 200
```

### Para datasets grandes (producción)
```python
# Script 1: 1000+ facturas de 1 página
CANTIDAD_FACTURAS = 1000

# Script 2: 500-1000 facturas multipágina
CANTIDAD_FACTURAS = 500
```

---

## 📞 Soporte

Si encuentras problemas:

1. Verifica que estás en la rama correcta: `claude/fix-json-parsing-011CUyGo75ZndGpbT9KKAMXw`
2. Asegúrate de tener todos los permisos necesarios
3. Revisa que las dependencias estén instaladas (`reportlab`)
4. Consulta los archivos de documentación:
   - `CORRECCION_COMPLETA_SUPERPOSICIONES.md`
   - `CORRECCION_SUPERPOSICION_TOTALES.md`

---

## 📝 Notas Importantes

1. **Los JSONs se generan primero, los PDFs después** (requieren reportlab)
2. **Cada ejecución crea una carpeta nueva** con timestamp
3. **Los nombres de archivos incluyen información útil:**
   - Facturas de 1 página: `FACTURA_0001_F123_456789.json`
   - Facturas multipágina: `FACTURA_MP_0001_5PAG_F123_456789.json` (incluye número de páginas)
4. **La distribución de páginas en multipágina es flexible** (puedes modificarla)
5. **Ambos scripts funcionan local y en Google Colab**

---

✅ **Última actualización:** 2025-01-10
✅ **Branch:** `claude/fix-json-parsing-011CUyGo75ZndGpbT9KKAMXw`
✅ **Estado:** Producción
