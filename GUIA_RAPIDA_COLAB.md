# 🚀 GUÍA RÁPIDA - GENERAR LOTES DE FACTURAS EN GOOGLE COLAB

## ⚡ MÉTODO RÁPIDO (Copy & Paste)

### Paso 1: Abre Google Colab
Ir a: https://colab.research.google.com/

### Paso 2: Copia este código
Abre el archivo `COLAB_GENERAR_LOTE.py` y copia TODO el contenido.

### Paso 3: Pega en Colab
Crea una nueva celda y pega el código completo.

### Paso 4: Configura
Modifica solo estas líneas al inicio del código:

```python
# ============================================================================
# ### CONFIGURACIÓN - MODIFICA ESTO ###
# ============================================================================

CANTIDAD_FACTURAS = 100    # 🔢 ¿Cuántas facturas quieres generar?
GENERAR_PDFS = True         # 📄 ¿Generar PDFs? (True/False)

# Distribución de páginas (ajusta los porcentajes, deben sumar 1.0)
DISTRIBUCION = {
    3: 0.25,  # 25% con 3 páginas (~40-45 items)
    4: 0.25,  # 25% con 4 páginas (~50-55 items)
    5: 0.25,  # 25% con 5 páginas (~60-70 items)
    6: 0.25,  # 25% con 6 páginas (~75-80 items)
}

# Monedas a usar
MONEDAS = ['PEN', 'USD', 'EUR']

# Probabilidad de generar facturas a crédito
PROBABILIDAD_CREDITO = 0.5  # 50%
```

### Paso 5: Ejecuta
Presiona el botón ▶ o Shift+Enter

### Paso 6: Espera
El script:
- Instalará las dependencias necesarias
- Clonará el repositorio
- Generará las facturas
- Mostrará estadísticas

### Paso 7: Descarga
Al terminar, ejecuta esto en una nueva celda:

```python
# Comprimir y descargar todo
!zip -r /content/facturas.zip /content/FACTURAS_JSONs /content/FACTURAS_PDFs
from google.colab import files
files.download('/content/facturas.zip')
```

---

## 📋 EJEMPLOS DE CONFIGURACIÓN

### Ejemplo 1: 50 facturas balanceadas
```python
CANTIDAD_FACTURAS = 50
GENERAR_PDFS = True
DISTRIBUCION = {3: 0.25, 4: 0.25, 5: 0.25, 6: 0.25}
MONEDAS = ['PEN', 'USD', 'EUR']
PROBABILIDAD_CREDITO = 0.5
```

### Ejemplo 2: 200 facturas, mayoría con 4-5 páginas
```python
CANTIDAD_FACTURAS = 200
GENERAR_PDFS = True
DISTRIBUCION = {3: 0.1, 4: 0.4, 5: 0.4, 6: 0.1}
MONEDAS = ['PEN', 'USD']
PROBABILIDAD_CREDITO = 0.6
```

### Ejemplo 3: 100 facturas, solo con muchas páginas (5-6)
```python
CANTIDAD_FACTURAS = 100
GENERAR_PDFS = True
DISTRIBUCION = {5: 0.5, 6: 0.5}
MONEDAS = ['PEN']
PROBABILIDAD_CREDITO = 0.7
```

### Ejemplo 4: 500 facturas, solo JSONs (sin PDFs)
```python
CANTIDAD_FACTURAS = 500
GENERAR_PDFS = False  # Más rápido, solo genera JSONs
DISTRIBUCION = {3: 0.2, 4: 0.3, 5: 0.3, 6: 0.2}
MONEDAS = ['PEN', 'USD', 'EUR']
PROBABILIDAD_CREDITO = 0.5
```

### Ejemplo 5: 30 facturas, todas con 3 páginas
```python
CANTIDAD_FACTURAS = 30
GENERAR_PDFS = True
DISTRIBUCION = {3: 1.0}  # 100% con 3 páginas
MONEDAS = ['USD']
PROBABILIDAD_CREDITO = 0.3
```

---

## 🎯 CONTROL DE PÁGINAS

| Páginas | Items aproximados | % sugerido |
|---------|-------------------|------------|
| 3       | 40-45             | 20-30%     |
| 4       | 50-55             | 25-35%     |
| 5       | 60-70             | 25-35%     |
| 6       | 75-85             | 10-20%     |

**Importante:** Los porcentajes en `DISTRIBUCION` deben sumar 1.0 (100%)

---

## ⚙️ PARÁMETROS EXPLICADOS

### `CANTIDAD_FACTURAS`
- Número total de facturas a generar
- Mínimo recomendado: 10
- Máximo recomendado: 1000 (puede tardar)
- Ejemplo: `100`

### `GENERAR_PDFS`
- `True`: Genera JSONs + PDFs (tarda más)
- `False`: Solo JSONs (más rápido)
- Recomendación: `True` si necesitas PDFs, `False` si solo quieres datos

### `DISTRIBUCION`
- Define qué % de facturas tendrá cada número de páginas
- Debe sumar 1.0
- Ejemplo balanceado: `{3: 0.25, 4: 0.25, 5: 0.25, 6: 0.25}`
- Ejemplo muchas páginas: `{5: 0.5, 6: 0.5}`

### `MONEDAS`
- Lista de monedas a usar
- Opciones: `'PEN'`, `'USD'`, `'EUR'`
- Se selecciona aleatoriamente para cada factura
- Ejemplo: `['PEN', 'USD']`

### `PROBABILIDAD_CREDITO`
- Probabilidad de que la factura sea a crédito (con cuotas)
- Valor entre 0.0 y 1.0
- `0.0` = Todas al contado
- `0.5` = 50% a crédito, 50% al contado
- `1.0` = Todas a crédito

---

## 📊 SALIDA DEL SCRIPT

El script mostrará:

```
================================================================================
                    🚀 INICIANDO GENERACIÓN DE FACTURAS
================================================================================

📦 Paso 1/5: Instalando dependencias...
   ✅ reportlab instalado

📥 Paso 2/5: Configurando repositorio...
   ✅ Repositorio listo

📚 Paso 3/5: Importando módulos...
   ✅ Módulos importados

⚙️  Paso 4/5: Validando configuración...

📋 CONFIGURACIÓN FINAL:
--------------------------------------------------------------------------------
   Facturas a generar: 100
   Generar PDFs: ✅ Sí
   Monedas: PEN, USD, EUR
   Probabilidad crédito: 50%

   Distribución de páginas:
     3 páginas: 25% (~25 facturas)
     4 páginas: 25% (~25 facturas)
     5 páginas: 25% (~25 facturas)
     6 páginas: 25% (~25 facturas)
--------------------------------------------------------------------------------

🔄 Paso 5/5: Generando 100 facturas...
================================================================================
  ✅ Progreso: 20/100 (20%) - Última: F123-456789 (4 pág)
  ✅ Progreso: 40/100 (40%) - Última: F456-789012 (5 pág)
  ✅ Progreso: 60/100 (60%) - Última: F789-012345 (3 pág)
  ✅ Progreso: 80/100 (80%) - Última: F012-345678 (6 pág)
  ✅ Progreso: 100/100 (100%) - Última: F345-678901 (4 pág)

================================================================================
                           📊 ESTADÍSTICAS FINALES
================================================================================

✅ Generadas exitosamente: 100/100

📄 Distribución por páginas:
--------------------------------------------------------------------------------
  3 páginas:   25 (25.0%) ████████████
  4 páginas:   26 (26.0%) █████████████
  5 páginas:   24 (24.0%) ████████████
  6 páginas:   25 (25.0%) ████████████

💰 Distribución por moneda:
--------------------------------------------------------------------------------
  EUR:   32 (32.0%)
  PEN:   35 (35.0%)
  USD:   33 (33.0%)

📈 Resumen:
--------------------------------------------------------------------------------
  Total items: 5,750
  Promedio items/factura: 57.5
  Promedio páginas/factura: 4.5
  Con crédito: 51
  Al contado: 49

📁 Ubicación de archivos:
--------------------------------------------------------------------------------
  JSONs: /content/FACTURAS_JSONs/
  PDFs: /content/FACTURAS_PDFs/

================================================================================
                          ✅ GENERACIÓN COMPLETADA
================================================================================
```

---

## 💾 CÓMO DESCARGAR LOS ARCHIVOS

### Opción 1: Descargar todo comprimido
```python
!zip -r /content/facturas.zip /content/FACTURAS_JSONs /content/FACTURAS_PDFs
from google.colab import files
files.download('/content/facturas.zip')
```

### Opción 2: Solo JSONs
```python
!zip -r /content/jsons.zip /content/FACTURAS_JSONs
from google.colab import files
files.download('/content/jsons.zip')
```

### Opción 3: Solo PDFs
```python
!zip -r /content/pdfs.zip /content/FACTURAS_PDFs
from google.colab import files
files.download('/content/pdfs.zip')
```

### Opción 4: Archivo individual
```python
from google.colab import files
files.download('/content/FACTURAS_JSONs/Factura_compra_grande_F123_456789_20250101.json')
```

---

## 🔍 VER ARCHIVOS GENERADOS

### Listar JSONs
```python
!ls -lh /content/FACTURAS_JSONs/ | head -20
```

### Listar PDFs
```python
!ls -lh /content/FACTURAS_PDFs/ | head -20
```

### Ver contenido de un JSON
```python
import json
with open('/content/FACTURAS_JSONs/[nombre_archivo].json', 'r') as f:
    data = json.load(f)
    print(f"Items: {len(data['items'])}")
    print(f"Total: {data['importe_total']}")
    print(f"Moneda: {data['moneda']}")
```

---

## ⏱️ TIEMPO DE GENERACIÓN ESTIMADO

| Cantidad | Con PDFs | Solo JSONs |
|----------|----------|------------|
| 10       | ~30 seg  | ~10 seg    |
| 50       | ~2 min   | ~40 seg    |
| 100      | ~4 min   | ~1.5 min   |
| 200      | ~8 min   | ~3 min     |
| 500      | ~20 min  | ~7 min     |
| 1000     | ~40 min  | ~15 min    |

---

## ✅ CARACTERÍSTICAS DE LAS FACTURAS

Todas las facturas generadas cumplen:

- ✅ Formato InvoiceX v5.5 (97 campos base + items + cuotas)
- ✅ Estructura plana correcta
- ✅ Coherencia matemática 100%
- ✅ Monto en letras coincide con importe_total
- ✅ Ubicación geográfica mapeada correctamente
- ✅ tipo_documento estandarizado ("FACTURA ELECTRONICA")
- ✅ Cuotas escalonadas cada 30 días (si es a crédito)
- ✅ Calificación: 100/100

---

## 🆘 SOLUCIÓN DE PROBLEMAS

### Error: "ModuleNotFoundError: No module named 'reportlab'"
**Solución:** El script instala reportlab automáticamente. Si falla, ejecuta:
```python
!pip install reportlab
```

### Error: "Memory error" o "Runtime crashed"
**Causa:** Generando demasiadas facturas a la vez
**Solución:** Reduce `CANTIDAD_FACTURAS` a 100-200

### Los PDFs tardan mucho
**Solución:** Cambia `GENERAR_PDFS = False` para solo generar JSONs (más rápido)

### La distribución no funciona como esperaba
**Solución:** Verifica que los porcentajes sumen 1.0:
```python
sum(DISTRIBUCION.values())  # Debe dar 1.0
```

---

## 🎯 QUICK START - COPIAR Y PEGAR

Para generar **100 facturas balanceadas** con PDFs:

```python
# Solo cambia CANTIDAD_FACTURAS y ejecuta
CANTIDAD_FACTURAS = 100
# El resto del código de COLAB_GENERAR_LOTE.py va aquí
```

Para generar **500 facturas solo JSONs** (rápido):

```python
CANTIDAD_FACTURAS = 500
GENERAR_PDFS = False  # Más rápido
# El resto del código de COLAB_GENERAR_LOTE.py va aquí
```

---

## 📞 AYUDA ADICIONAL

Si necesitas ayuda, revisa:
- `GUIA_FACTURAS_MULTIPAGINA.md` - Guía completa
- `RESUMEN_CORRECCIONES_100.md` - Detalles del formato JSON
- `GENERAR_LOTE_FACTURAS.py` - Versión avanzada con más opciones

---

**Última actualización:** 2025-01-10
**Branch:** `claude/fix-json-parsing-011CUyGo75ZndGpbT9KKAMXw`
