# Instrucciones para Colocar Facturas Originales

## Ubicación de las Facturas

Para que el sistema pueda analizar tus facturas originales, debes colocarlas en la carpeta:

```
facturas_originales/
```

## Formatos Soportados

El sistema puede detectar y trabajar con los siguientes formatos:

### Documentos PDF
- `.pdf` - Facturas en formato PDF

### Imágenes
- `.png` - Imágenes PNG
- `.jpg` / `.jpeg` - Imágenes JPEG
- `.tiff` / `.tif` - Imágenes TIFF

## Cómo Colocar las Facturas

### Opción 1: Copiar directamente

```bash
# En Linux/Mac
cp /ruta/a/tus/facturas/*.pdf facturas_originales/
cp /ruta/a/tus/facturas/*.jpg facturas_originales/

# En Windows
copy C:\ruta\a\tus\facturas\*.pdf facturas_originales\
copy C:\ruta\a\tus\facturas\*.jpg facturas_originales\
```

### Opción 2: Desde Google Drive

Si tienes tus facturas en Google Drive:

1. **Descargar desde Google Drive**
   - Abre Google Drive en tu navegador
   - Selecciona la carpeta con las facturas
   - Click derecho → Descargar
   - Se descargará un archivo ZIP

2. **Extraer el ZIP**
   ```bash
   unzip facturas.zip -d facturas_originales/
   ```

3. **Verificar**
   ```bash
   ls facturas_originales/
   ```

### Opción 3: Usar el comando de análisis

Una vez que tengas las facturas en la carpeta, ejecuta:

```bash
python main.py --analizar --input facturas_originales/
```

Esto mostrará:
- Número de archivos encontrados
- Tipos de archivo
- Nombres de los archivos

## Estructura Recomendada

```
facturas_originales/
├── factura_001.pdf
├── factura_002.pdf
├── factura_003.jpg
├── factura_004.png
├── factura_005.pdf
└── ... (hasta 10 archivos como mencionaste)
```

## Ejemplo de Uso Completo

### 1. Colocar las facturas

```bash
# Copiar tus 10 facturas a la carpeta
cp ~/Downloads/facturas/*.* facturas_originales/
```

### 2. Verificar que se copiaron

```bash
ls -la facturas_originales/
```

Deberías ver algo como:

```
total 24
drwxr-xr-x  12 usuario  staff   384 Nov  8 10:30 .
drwxr-xr-x   8 usuario  staff   256 Nov  8 10:00 ..
-rw-r--r--   1 usuario  staff  1234 Nov  8 10:30 factura_001.pdf
-rw-r--r--   1 usuario  staff  2345 Nov  8 10:30 factura_002.pdf
-rw-r--r--   1 usuario  staff  3456 Nov  8 10:30 factura_003.jpg
...
```

### 3. Analizar las facturas

```bash
python main.py --analizar --input facturas_originales/
```

### 4. Generar nuevas facturas basadas en el análisis

```bash
python main.py --cantidad 50 --output facturas_generadas/
```

## Desde Google Drive (Paso a Paso)

### Si tienes un enlace de Google Drive:

1. **Compartir la carpeta**
   - Asegúrate de que la carpeta esté compartida con "Cualquiera con el enlace"

2. **Descargar usando el navegador**
   - Abre el enlace en tu navegador
   - Click en "Descargar todo" o selecciona los archivos
   - Guarda el archivo ZIP

3. **Extraer a la carpeta del proyecto**
   ```bash
   cd /ruta/al/proyecto/Creador-De-Factura
   unzip ~/Downloads/facturas.zip -d facturas_originales/
   ```

4. **Limpiar archivos innecesarios**
   ```bash
   # Eliminar archivos ocultos de Mac si existen
   rm -rf facturas_originales/._*
   rm -rf facturas_originales/.DS_Store
   ```

### Si tienes Google Drive sincronizado:

```bash
# Si usas Google Drive Desktop
cp ~/GoogleDrive/MisFacturas/*.pdf facturas_originales/
```

## Solución de Problemas

### No se encuentran las facturas

```bash
# Verifica que estás en la carpeta correcta del proyecto
pwd

# Debe mostrar algo como: /home/usuario/Creador-De-Factura

# Verifica que la carpeta facturas_originales existe
ls -d facturas_originales/

# Verifica el contenido
ls -la facturas_originales/
```

### Las facturas están en subcarpetas

Si tus facturas están organizadas en subcarpetas:

```bash
facturas_originales/
├── 2024/
│   ├── factura_001.pdf
│   └── factura_002.pdf
└── 2025/
    ├── factura_003.pdf
    └── factura_004.pdf
```

El sistema las encontrará automáticamente usando búsqueda recursiva.

### Permisos de lectura

Si tienes problemas de permisos:

```bash
# Dar permisos de lectura
chmod -R +r facturas_originales/
```

## Próximos Pasos

Una vez que tengas tus facturas originales en la carpeta:

1. **Analizar**: `python main.py --analizar`
2. **Generar**: `python main.py --cantidad 100`
3. **Revisar**: Las facturas generadas estarán en `facturas_generadas/`

## Nota Importante

El sistema actualmente **detecta** las facturas originales pero **no extrae automáticamente** sus datos (requeriría OCR y procesamiento de PDF avanzado).

Las facturas generadas se crean con datos **aleatorios ficticios** pero siguiendo patrones realistas de facturas peruanas.

Para una versión futura con extracción automática de datos de las facturas originales, se necesitarían herramientas adicionales como:
- `pytesseract` (OCR)
- `pdfplumber` (extracción de PDF)
- `opencv` (procesamiento de imágenes)
