# Generador de Facturas Ficticias 🧾

Sistema automatizado para analizar facturas existentes y generar nuevas facturas con datos ficticios coherentes y realistas.

## 🎯 Características

### Generación Automatizada
- ✅ RUC válidos con dígito verificador correcto
- ✅ Razones sociales de empresas peruanas ficticias
- ✅ Direcciones realistas de Perú
- ✅ Ítems variados (construcción, comida, servicios)
- ✅ Fechas del año 2025 (enero-diciembre)
- ✅ Múltiples monedas (Soles, Dólares, Euros)
- ✅ Cálculos correctos de IGV (18%) y totales
- ✅ Conversión automática de montos a letras
- ✅ Cuotas de crédito con fechas de vencimiento
- ✅ Operaciones exoneradas e inafectas (cuando aplica)
- ✅ Números de contrato opcionales
- ✅ Periodos facturados
- ✅ Formas de pago variadas

### Análisis de Facturas Originales
- 📄 Soporte para PDF
- 🖼️ Soporte para imágenes (PNG, JPG, TIFF)
- 🔍 Detección automática de archivos

## 📋 Requisitos

- Python 3.8 o superior
- pip (gestor de paquetes)

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone <repository-url>
cd Creador-De-Factura
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

Las dependencias principales son:
- `reportlab` - Generación de PDFs
- `faker` - Datos ficticios adicionales
- `python-dateutil` - Manejo de fechas

## 💻 Uso

### Uso Básico

```bash
# Generar 10 facturas (por defecto)
python main.py

# Generar 50 facturas
python main.py --cantidad 50

# Generar 100 facturas en directorio específico
python main.py --cantidad 100 --output ./mis_facturas/
```

### Analizar Facturas Originales

Si tienes facturas originales que quieres examinar:

```bash
# Colocar tus facturas en la carpeta facturas_originales/
# Luego ejecutar:
python main.py --analizar --input ./facturas_originales/

# Analizar y generar
python main.py --analizar --input ./facturas_originales/ --cantidad 50
```

### Ejemplos de Uso Programático

```bash
# Ver ejemplos de uso del código
python ejemplo_uso.py
```

### 🌐 Uso en Google Colab

Si prefieres ejecutar el sistema en la nube sin instalar nada localmente:

1. **Abrir el notebook en Google Colab:**
   - Sube `Generador_Facturas_Colab.ipynb` a Google Colab
   - O abre directamente desde GitHub: [Abrir en Colab](https://colab.research.google.com/github/GynoRomeroPrado/Creador-De-Factura/blob/main/Generador_Facturas_Colab.ipynb)

2. **Ejecutar todas las celdas:**
   - El notebook instalará automáticamente las dependencias
   - Clonará el repositorio
   - Montará tu Google Drive
   - Generará las facturas (PDFs y JSONs)
   - Guardará todo en `MyDrive/Facturas_Generadas/`

3. **Configuración:**
   - Ajusta `CANTIDAD_FACTURAS` en la celda de configuración
   - Elige si generar PDFs y/o JSONs
   - Las facturas se guardan automáticamente en tu Drive

**Características del Notebook:**
- ✅ Instalación automática de dependencias
- ✅ Guardado automático en Google Drive
- ✅ Exportación a JSON y PDF
- ✅ Validación de cálculos
- ✅ Resumen estadístico
- ✅ Descarga opcional en ZIP

### 📤 Exportación a JSON

El sistema incluye exportación completa a JSON para integración con otras herramientas:

```python
from src.json_exporter import JSONExporter

# Crear exportador
exporter = JSONExporter(output_dir="mi_carpeta")

# Exportar una factura
archivo = exporter.exportar_factura(factura_data)

# Exportar múltiples facturas
archivo_consolidado = exporter.exportar_multiple(lista_facturas, "todas.json")

# Crear resumen estadístico
resumen = exporter.crear_resumen(lista_facturas)
```

**Formato JSON incluye:**
- Todos los datos de la factura
- Fechas en formato ISO 8601
- Estructura anidada para items, cuotas, descuentos
- Datos específicos de hotel/seguro cuando aplica
- Metadatos de generación

## 📁 Estructura del Proyecto

```
.
├── main.py                          # Punto de entrada principal
├── ejemplo_uso.py                   # Ejemplos de uso
├── test_validacion.py               # Script de validación de cálculos
├── test_imports_validacion.py       # Test de importaciones
├── requirements.txt                 # Dependencias Python
├── README.md                        # Este archivo
├── GUIA_USO.md                     # Guía detallada de uso
├── Generador_Facturas_Colab.ipynb  # Notebook de Google Colab
├── src/
│   ├── __init__.py
│   ├── utils.py                    # Utilidades (RUC, letras, datos, hotel, seguro)
│   ├── generator.py                # Generador de facturas (4 tipos)
│   ├── pdf_creator.py              # Creador de PDFs (tipografía uniforme)
│   └── json_exporter.py            # Exportador a JSON
├── facturas_originales/            # Facturas de referencia (16 archivos)
└── facturas_generadas/             # Aquí se guardan las generadas
```

## 📊 Tipos de Facturas Generadas

El sistema genera **4 tipos diferentes** de facturas con características específicas:

### 1. **Factura General** (`general`)
Factura estándar con items variados de construcción, comida o servicios.

### 2. **Factura de Hotel** (`hotel`)
- ✅ Check-in y Check-out con fechas específicas
- ✅ Número de noches calculado
- ✅ Datos del huésped
- ✅ Código de reserva
- ✅ Código de grupo (cuando aplica)
- ✅ Items típicos: ALOJAMIENTO, ALIMENTACION, LAVANDERIA, TELEFONO, MINIBAR
- ✅ "Cargo al ítem" adicional por línea

### 3. **Factura de Seguro** (`seguro`)
- ✅ Número de póliza
- ✅ Vigencia (inicio y fin)
- ✅ Datos del vehículo (placa, marca, modelo, año)
- ✅ Datos del asegurado
- ✅ Items típicos: SOAT, POLIZA, SEGURO VEHICULAR, COBERTURA

### 4. **Factura con Descuento** (`con_descuento`)
- ✅ Tabla de descuentos detallada
- ✅ Columnas: GRAVADO, EXONER., IGV, ICBPER, TOTAL, DETRAC.
- ✅ Tipos de descuento: porcentual, fijo, por volumen, por pronto pago
- ✅ Recálculo automático de totales

### Categorías de Items

1. **Construcción**: Cemento, arena, fierro, ladrillos, tuberías, etc.
2. **Comida**: Arroz, aceite, carne, pescado, productos de primera necesidad
3. **Servicios**: Mantenimiento, instalación, consultoría, transporte
4. **Hoteles**: Alojamiento, alimentación, lavandería, teléfono, minibar
5. **Combustibles**: Gasolina, diésel, GLP, aceites lubricantes
6. **Seguros**: SOAT, pólizas, coberturas, asistencia
7. **Seguridad**: Cámaras, alarmas, guardianía, monitoreo

### Características Financieras

- **Operación Gravada**: Con IGV del 18%
- **Operación Exonerada**: Sin IGV (20% de probabilidad)
- **Operación Inafecta**: Sin IGV (10% de probabilidad)
- **Totales**: Siempre coherentes y correctos

### Formas de Pago

- Efectivo
- Transferencia bancaria
- Cheque
- Depósito en cuenta
- Crédito a 30, 60, 90 días (con cuotas)

### Monedas

- PEN - Soles peruanos (S/)
- USD - Dólares americanos ($)
- EUR - Euros (€)

## 🔧 Personalización

### Agregar más items

Edita `src/utils.py` y añade items a las listas:
- `ItemsGenerator.CONSTRUCCION`
- `ItemsGenerator.COMIDA`
- `ItemsGenerator.SERVICIOS`

### Cambiar diseño de PDF

Edita `src/pdf_creator.py` y modifica los métodos de dibujo.

### Agregar más datos

Edita `src/utils.py`:
- `DatosPersonas.NOMBRES`
- `DatosPersonas.APELLIDOS`
- `DatosPersonas.EMPRESAS_NOMBRES`
- etc.

## 📖 Documentación Adicional

Ver **GUIA_USO.md** para documentación detallada.

## ⚠️ Notas Importantes

1. **Solo para pruebas**: Este software genera datos ficticios para desarrollo y testing
2. **No para producción**: No usar para generar documentos tributarios reales
3. **RUCs ficticios**: Aunque válidos en formato, no corresponden a empresas reales
4. **Sin valor legal**: Los documentos generados no tienen validez legal

## 🎓 Ejemplos de Salida

Una factura típica incluye:

- Número de factura: F001-000123
- Fecha de emisión: 15/03/2025
- Emisor con RUC, razón social, dirección
- Receptor con RUC, razón social, dirección
- Items detallados con cantidades y precios
- Subtotales (Op. Gravada, Exonerada, Inafecta)
- IGV (18%)
- Total numérico
- Total en letras: "MIL DOSCIENTOS CINCUENTA CON 50/100 SOLES"
- Forma de pago
- Cuotas (si es a crédito)

## 🤝 Contribuir

Las mejoras son bienvenidas. Áreas de mejora:

- OCR para extraer datos de facturas originales
- Clonación de diseños de facturas existentes
- Más tipos de comprobantes (boletas, notas de crédito)
- Exportación a XML (formato SUNAT)
- Interfaz gráfica

## 📄 Licencia

Este proyecto es de código abierto para propósitos educativos y de desarrollo.
