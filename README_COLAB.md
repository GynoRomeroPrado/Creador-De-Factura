# 🧾 Procesador de Dataset de Facturas para Google Colab

## 📋 Descripción

Este proyecto proporciona herramientas para procesar y aumentar un dataset de facturas en Google Colab. Realiza las siguientes operaciones:

1. **Renombrado correlativo** de facturas y sus archivos JSON
2. **Generación de variaciones** mediante desplazamientos de píxeles en diferentes direcciones
3. **Mantenimiento de correspondencia** entre cada factura y su anotación JSON

## 🎯 Características

- ✅ Soporta imágenes (JPG, PNG) y PDFs
- ✅ Renombrado automático correlativo (factura_0001, factura_0002, etc.)
- ✅ Data augmentation con 16 transformaciones por factura:
  - 8 direcciones principales (arriba, abajo, izquierda, derecha, 4 diagonales)
  - 8 direcciones intermedias (desplazamientos más pequeños)
- ✅ Generación automática de JSON para cada variación
- ✅ Reporte detallado del proceso

## 📁 Estructura del Proyecto

```
Creador-De-Factura/
├── Invoice_Dataset_Processor.ipynb    # Notebook de Google Colab (RECOMENDADO)
├── colab_invoice_augmentation.py      # Script Python alternativo
└── README_COLAB.md                     # Este archivo
```

## 🚀 Uso en Google Colab (Método Recomendado)

### Paso 1: Subir el Notebook a Google Colab

1. Ve a [Google Colab](https://colab.research.google.com/)
2. Haz clic en **"Archivo" → "Abrir notebook"**
3. Selecciona la pestaña **"Subir"**
4. Sube el archivo `Invoice_Dataset_Processor.ipynb`

### Paso 2: Preparar tus Facturas en Google Drive

Organiza tus archivos de la siguiente manera:

```
Google Drive/
└── Facturas/
    ├── factura1.pdf
    ├── factura1.json
    ├── factura2.jpg
    ├── factura2.json
    ├── factura3.png
    ├── factura3.json
    └── ...
```

**Importante:** Cada factura debe tener su correspondiente archivo JSON con el mismo nombre base.

### Paso 3: Ejecutar el Notebook

1. **Ejecuta la celda 1:** Instala dependencias
2. **Ejecuta la celda 2:** Monta Google Drive (te pedirá autorización)
3. **Ejecuta la celda 3:** Configura las rutas

   **⚠️ IMPORTANTE:** Modifica estas variables:

   ```python
   INPUT_FOLDER = "/content/drive/MyDrive/Facturas"  # Tu carpeta de entrada
   OUTPUT_FOLDER = "/content/drive/MyDrive/Facturas_Procesadas"  # Carpeta de salida
   PIXEL_RANGE = 10  # Rango de desplazamiento en píxeles
   ```

4. **Ejecuta la celda 4:** Carga las funciones
5. **Ejecuta la celda 5:** Procesa las facturas
6. **Ejecuta la celda 6 (opcional):** Visualiza resultados
7. **Ejecuta la celda 7 (opcional):** Descarga el reporte

## 📊 Estructura de Salida

Después de ejecutar el procesamiento, obtendrás:

```
Facturas_Procesadas/
├── organized/                          # Facturas renombradas
│   ├── factura_0001.pdf
│   ├── factura_0001.json
│   ├── factura_0002.jpg
│   ├── factura_0002.json
│   └── ...
├── augmented/                          # Facturas aumentadas
│   ├── factura_0001_aug_01_derecha.png
│   ├── factura_0001_aug_01_derecha.json
│   ├── factura_0001_aug_02_izquierda.png
│   ├── factura_0001_aug_02_izquierda.json
│   └── ...
└── dataset_report.json                 # Reporte del proceso
```

## 📄 Formato del JSON Aumentado

Cada factura aumentada tiene un JSON con la siguiente estructura:

```json
{
  "archivo_factura": "factura_0001_aug_01_derecha.png",
  "id_correlativo": "factura_0001_aug_01_derecha",
  "emisor": "...",
  "receptor": "...",
  "ruc": "...",
  "...": "... (campos originales de tu JSON) ...",
  "augmentation": {
    "original_file": "factura_0001.pdf",
    "transformation": "derecha",
    "shift_x": 10,
    "shift_y": 0
  }
}
```

## 🔧 Transformaciones Aplicadas

Por defecto, se generan **16 variaciones** por factura:

### Desplazamientos Completos (±10px)
1. Derecha
2. Izquierda
3. Abajo
4. Arriba
5. Diagonal superior derecha
6. Diagonal superior izquierda
7. Diagonal inferior derecha
8. Diagonal inferior izquierda

### Desplazamientos Medios (±5px)
9-16. Las mismas 8 direcciones con la mitad del desplazamiento

## ⚙️ Personalización

### Cambiar el Rango de Píxeles

En la celda de configuración, modifica:

```python
PIXEL_RANGE = 15  # Cambia de 10 a 15 píxeles
```

### Modificar las Transformaciones

Edita la función `get_augmentation_configs()` en la celda 4 para agregar más transformaciones:

```python
def get_augmentation_configs(self, pixel_range: int = 10) -> List[Dict]:
    configs = []

    # Agregar más direcciones o transformaciones aquí
    # Ejemplo: rotaciones, cambios de brillo, etc.

    return configs
```

## 📈 Ejemplo de Uso

Si tienes **10 facturas** originales:

- Se renombrarán a: `factura_0001.pdf` hasta `factura_0010.pdf`
- Se generarán: **10 × 16 = 160 facturas aumentadas**
- Total en dataset: **170 facturas** (10 organizadas + 160 aumentadas)

## 🐛 Solución de Problemas

### Error: "La carpeta no existe"

- Verifica que la ruta en `INPUT_FOLDER` sea correcta
- Asegúrate de haber montado Google Drive correctamente

### Error: "No se encontró JSON para factura"

- Cada imagen/PDF debe tener su JSON correspondiente
- Los nombres deben coincidir (ej: `factura1.pdf` y `factura1.json`)

### Error al procesar PDFs

- Verifica que la celda 1 se haya ejecutado correctamente
- Reinstala las dependencias ejecutando de nuevo la celda 1

### Memoria insuficiente

- Procesa las facturas en lotes más pequeños
- Usa una sesión de Colab con más RAM (Colab Pro)

## 💡 Consejos

1. **Haz una copia de seguridad** de tus facturas originales antes de procesar
2. **Ejecuta primero con pocas facturas** para probar el proceso
3. **Revisa el reporte JSON** para verificar estadísticas
4. **Usa PIXEL_RANGE moderado** (5-15px) para mantener facturas realistas
5. **Verifica las imágenes generadas** con la celda de visualización

## 📞 Soporte

Si encuentras problemas:

1. Revisa que todas las celdas se hayan ejecutado en orden
2. Verifica los mensajes de error en la consola
3. Asegúrate de tener espacio suficiente en Google Drive

## 📝 Licencia

Este proyecto es de código abierto y está disponible para uso educativo y comercial.

---

**¡Listo para procesar tus facturas! 🎉**
