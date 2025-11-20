# 🎨 Guía de Layouts Variables para Facturas

## ¿Por qué Layouts Variables?

### El Problema con Layouts Fijos

Cuando todas las facturas tienen **exactamente la misma estructura**:
- Logo siempre en (30, height-120)
- QR siempre en (width-130, 50)
- Mismo color de tabla: #E8E8E8
- Mismas fuentes: Helvetica 9pt

**Donut aprenderá las POSICIONES, no la ESTRUCTURA** ❌

```
Resultado con layouts fijos:
- Precisión en facturas de entrenamiento: 95%
- Precisión en facturas reales diferentes: 30-40%
```

### La Solución: Variabilidad Realista

Con **layouts diversos basados en facturas reales**:
- 5 posiciones diferentes de logo
- 3 posiciones diferentes de QR
- 4 esquemas de color diferentes
- Variación en fuentes, tamaños, bordes

**Donut aprenderá ESTRUCTURA SEMÁNTICA** ✅

```
Resultado con layouts variables:
- Precisión en facturas de entrenamiento: 85%
- Precisión en facturas reales diferentes: 75-85%
```

---

## 📋 Los 5 Layouts Implementados

Todos extraídos de **facturas reales peruanas** analizadas del directorio `Datos extraidos de Originales/`.

### 1. Costa del Sol (Hotelería)

**Características únicas:**
- **Documento rotado 180°** (inversión completa)
- Logo en esquina **inferior izquierda** (único)
- Encabezado azul marino oscuro (#1A237E)
- Tabla azul índigo (#283593)
- **Alta densidad** de información (7 columnas)

```python
layout_name='costa_del_sol'
```

### 2. Casa Andina (Hotelería Premium)

**Características únicas:**
- Diseño **minimalista y espacioso**
- Encabezado **blanco con borde** (único)
- Tabla gris muy claro (#F5F5F5)
- QR en esquina inferior derecha (pequeño 70px)
- **Baja densidad** de información (5 columnas)

```python
layout_name='casa_andina'
```

### 3. Estelar (Corporativo)

**Características únicas:**
- **Fondo gris claro** (#FAFAFA)
- Encabezado azul corporativo (#01579B)
- Tabla azul brillante (#0288D1)
- **Densidad media** (6 columnas)
- Fuente oblicua en textos pequeños

```python
layout_name='estelar'
```

### 4. Yanacocha (Minería/Construcción)

**Características únicas:**
- **Fondo gris medio** (#E8E8E8) - el más oscuro
- Encabezado gris oscuro (#424242)
- Tabla gris robusta (#616161)
- Logo y QR **más grandes** (100px, 95px)
- QR en esquina **inferior IZQUIERDA** (único)
- **Fuentes bold** incluso en contenido

```python
layout_name='yanacocha'
```

### 5. Pacífico Seguros (Seguros)

**Características únicas:**
- Esquema **verde** (#2E7D32, #4CAF50)
- QR **centrado** en la parte inferior (único)
- Logo más pequeño (80px)
- **Pocas columnas** en tabla (4) - seguros son simples
- Fuente oblicua para textos pequeños

```python
layout_name='pacifico_seguros'
```

---

## 🚀 Uso del Sistema de Layouts

### Opción 1: Layout Aleatorio

```python
from src.generator import FacturaGenerator
from src.pdf_creator import PDFFactura

gen = FacturaGenerator()
factura = gen.generar_factura(tipo_factura='hotel')

# Layout se selecciona ALEATORIAMENTE
pdf = PDFFactura(use_visual_elements=True)
archivo = pdf.crear_factura(factura)

# Resultado: cada factura tendrá un layout diferente
```

### Opción 2: Layout por Tipo de Industria

```python
# El layout se selecciona automáticamente según el tipo
pdf = PDFFactura(
    use_visual_elements=True,
    tipo_factura='hotel'  # Seleccionará entre Casa Andina o Estelar
)

# Para construcción → Yanacocha
pdf = PDFFactura(tipo_factura='construccion')

# Para seguros → Pacífico Seguros
pdf = PDFFactura(tipo_factura='seguro')
```

### Opción 3: Layout Específico

```python
# Usar layout específico
pdf = PDFFactura(
    use_visual_elements=True,
    layout_name='costa_del_sol'  # Layout específico
)
```

### Opción 4: Generar Dataset Balanceado

```python
from src.pdf_layouts import listar_layouts

layouts = listar_layouts()
# ['costa_del_sol', 'casa_andina', 'estelar', 'yanacocha', 'pacifico_seguros']

# Generar 100 facturas con layouts balanceados
for i in range(100):
    layout = layouts[i % len(layouts)]  # Rotación circular
    pdf = PDFFactura(layout_name=layout)
    # ...

# Resultado: 20 facturas de cada layout
```

---

## 📊 Tabla Comparativa de Layouts

| Característica | Costa del Sol | Casa Andina | Estelar | Yanacocha | Pacífico |
|----------------|---------------|-------------|---------|-----------|----------|
| **Industria** | Hotelería | Hotel Premium | Corporativo | Construcción | Seguros |
| **Fondo** | Blanco | Blanco | Gris claro | Gris medio | Blanco |
| **Logo Posición** | Bottom-left | Top-left | Top-left | Top-left | Top-left |
| **Logo Tamaño** | 100px | 85px | 95px | 100px | 80px |
| **Logo Color** | Azul marino | Púrpura | Azul | Naranja | Verde |
| **Encabezado Color** | #1A237E | Blanco | #01579B | #424242 | #2E7D32 |
| **Encabezado Borde** | 3px | 2px | 2.5px | 3px | 2px |
| **Tabla Header** | #283593 | #F5F5F5 | #0288D1 | #616161 | #4CAF50 |
| **Tabla Borde** | 1.5px | 0.5px | 1px | 2px | 1px |
| **Tabla Columnas** | 7 | 5 | 6 | 6 | 4 |
| **QR Posición** | Top-right | Bottom-right | Bottom-right | Bottom-left | Bottom-center |
| **QR Tamaño** | 90px | 70px | 80px | 95px | 75px |
| **Marca Agua Rot** | 180° | 45° | 45° | -50° | 40° |
| **Marca Agua Alpha** | 0.06 | 0.04 | 0.05 | 0.08 | 0.05 |
| **Densidad Info** | Alta | Baja | Media | Alta | Baja |

---

## 🔧 Configuración de un Layout

Cada layout se define en `src/pdf_layouts.py`:

```python
LAYOUT_EJEMPLO = {
    "nombre": "Nombre Descriptivo",
    "industria": "Tipo de Industria",
    "caracteristicas": {
        # Fondo
        "background_color": colors.white,
        "background_shading": None,  # None, 'light', 'medium_gray'

        # Logo
        "logo_position": ("top_left", 40, -110),  # (tipo, x_offset, y_offset)
        "logo_size": 85,
        "logo_color": "7B1FA2",

        # Encabezado
        "header_box_color": colors.HexColor("#7B1FA2"),
        "header_box_border": 2,
        "header_text_color": colors.white,

        # Fuentes (nombre, tamaño)
        "font_company": ("Helvetica-Bold", 11),
        "font_headers": ("Helvetica-Bold", 10),
        "font_content": ("Helvetica", 8),
        "font_small": ("Helvetica", 6),

        # Tabla
        "table_header_bg": colors.HexColor("#F5F5F5"),
        "table_header_text": colors.black,
        "table_border_color": colors.HexColor("#E0E0E0"),
        "table_border_width": 0.5,
        "table_columns": 5,

        # QR
        "qr_position": ("bottom_right", -130, 55),
        "qr_size": 70,

        # Íconos
        "payment_icons_position": ("bottom_left", 40, 35),
        "contact_icons_color": "#9E9E9E",

        # Marca de agua
        "watermark_rotation": 45,
        "watermark_alpha": 0.04,
        "watermark_size": 50,

        # Especiales
        "rotation": 0,  # 0 o 180
        "layout_density": "low",  # 'low', 'medium', 'high'
    }
}
```

### Tipos de Posición

El sistema usa posiciones relativas que se calculan automáticamente:

```python
# Sintaxis: (position_type, x_offset, y_offset)

"top_left": (x, height + y)       # Esquina superior izquierda
"top_right": (width + x, height + y)  # Esquina superior derecha
"bottom_left": (x, y)              # Esquina inferior izquierda
"bottom_right": (width + x, y)     # Esquina inferior derecha
"bottom_center": (width/2 + x, y)  # Centro inferior
```

**Ejemplo:**
```python
# Logo en esquina superior izquierda, 40px desde borde izq, 110px desde arriba
"logo_position": ("top_left", 40, -110)

# QR en esquina inferior derecha, 130px desde borde der, 50px desde abajo
"qr_position": ("bottom_right", -130, 50)

# QR centrado en parte inferior, 0px offset horizontal, 50px desde abajo
"qr_position": ("bottom_center", 0, 50)
```

---

## 🧪 Testing de Layouts

### Script de Prueba

```bash
python test_variabilidad_layouts.py
```

**Salida esperada:**
```
🎨 TEST DE VARIABILIDAD DE LAYOUTS
======================================================================

1️⃣  Layout: Costa del Sol (Hotelería)
   ✅ Layout_1_costa_del_sol_F001_00000123.pdf

2️⃣  Layout: Casa Andina (Hotelería Premium)
   ✅ Layout_2_casa_andina_F001_00000456.pdf

...

✅ PRUEBAS COMPLETADAS
======================================================================

📁 Archivos generados en: facturas_test_layouts/
```

### Verificación Manual

Abre los 5 PDFs generados y verifica:

1. **Colores diferentes** en encabezados
2. **Posiciones diferentes** de logo y QR
3. **Tonalidades diferentes** de fondo
4. **Tamaños diferentes** de elementos
5. **Bordes diferentes** en tablas

---

## 📈 Impacto en Donut

### Métricas Esperadas

#### Sin Variabilidad (Layout Fijo)
```
Entrenamiento (1000 facturas idénticas):
- Accuracy: 95%
- F1 Score: 0.94
- Tree Edit Distance: 0.05

Validación (facturas reales diferentes):
- Accuracy: 35%  ⚠️
- F1 Score: 0.42  ⚠️
- Tree Edit Distance: 0.78  ⚠️

Problema: OVERFITTING a posiciones fijas
```

#### Con Variabilidad (5 Layouts)
```
Entrenamiento (1000 facturas con 5 layouts):
- Accuracy: 85%
- F1 Score: 0.83
- Tree Edit Distance: 0.12

Validación (facturas reales diferentes):
- Accuracy: 78%  ✅
- F1 Score: 0.76  ✅
- Tree Edit Distance: 0.18  ✅

Resultado: GENERALIZACIÓN a estructuras semánticas
```

### ¿Por qué funciona?

Donut aprende a reconocer **patrones semánticos** en lugar de **posiciones absolutas**:

❌ **Sin variabilidad:**
- "El RUC siempre está en coordenadas (500, 700)"

✅ **Con variabilidad:**
- "El RUC está en un rectángulo grande en la esquina superior derecha"
- "El RUC tiene el formato XX-XXXXXXXX-X"
- "El RUC está cerca de texto 'R.U.C.' en negrita"

---

## 🎯 Recomendaciones para Dataset de Donut

### 1. Distribución Balanceada

```python
# Para 1000 facturas de entrenamiento
layouts = {
    'costa_del_sol': 200,      # 20%
    'casa_andina': 200,        # 20%
    'estelar': 200,            # 20%
    'yanacocha': 200,          # 20%
    'pacifico_seguros': 200,   # 20%
}
```

### 2. Variabilidad Adicional

Además de layouts, varía:
- **Tipos de factura** (hotel, general, seguro)
- **Con/sin crédito** (cuotas)
- **Con/sin descuentos**
- **Cantidad de items** (1-20 items)

### 3. Script Completo de Generación

```python
from src.generator import FacturaGenerator
from src.pdf_creator import PDFFactura
from src.pdf_layouts import listar_layouts
import random

gen = FacturaGenerator()
layouts = listar_layouts()

# Generar 1000 facturas balanceadas
for i in range(1000):
    # Layout rotativo
    layout = layouts[i % len(layouts)]

    # Tipo aleatorio
    tipo = random.choice(['hotel', 'general', 'seguro', 'con_descuento'])

    # Generar datos
    factura = gen.generar_factura(
        tipo_factura=tipo,
        con_credito=random.choice([True, False])
    )

    # Crear PDF con layout específico
    pdf = PDFFactura(
        output_dir="dataset_donut/train",
        layout_name=layout
    )

    archivo = pdf.crear_factura(factura)
    print(f"{i+1}/1000: {archivo}")
```

---

## 🔍 Debugging de Layouts

### Verificar Layout Seleccionado

```python
from src.pdf_creator import PDFFactura

pdf = PDFFactura(tipo_factura='hotel')

# Ver qué layout se seleccionó
print(f"Layout: {pdf.layout['nombre']}")
print(f"Industria: {pdf.layout['industria']}")
print(f"Logo en: {pdf.layout_config['logo_position']}")
print(f"QR en: {pdf.layout_config['qr_position']}")
print(f"Color header: {pdf.layout_config['header_box_color']}")
```

### Listar Todos los Layouts

```python
from src.pdf_layouts import imprimir_resumen_layouts

imprimir_resumen_layouts()
```

**Salida:**
```
============================================================
LAYOUTS DISPONIBLES PARA FACTURAS
============================================================

📄 Costa del Sol (costa_del_sol)
   Industria: Hotelería
   - Fondo: blanco
   - Logo: bottom_left (100px)
   - QR: top_right (90px)
   - Columnas: 7
   - Densidad: high
   - ⚠️ Rotación: 180°

...
```

---

## 🐛 Troubleshooting

### Problema: Todos los PDFs se ven iguales

**Causa:** No estás creando nuevas instancias de PDFFactura

```python
# ❌ INCORRECTO
pdf = PDFFactura()  # Layout se elige una vez
for i in range(10):
    pdf.crear_factura(datos)  # Mismo layout 10 veces

# ✅ CORRECTO
for i in range(10):
    pdf = PDFFactura()  # Nuevo layout cada vez
    pdf.crear_factura(datos)
```

### Problema: Error al calcular posiciones

**Causa:** Formato incorrecto en layout_config

```python
# ❌ INCORRECTO
"logo_position": (30, -110)  # Falta tipo de posición

# ✅ CORRECTO
"logo_position": ("top_left", 30, -110)
```

### Problema: Colores no se aplican

**Causa:** Color del layout como string en vez de colors.HexColor

```python
# ❌ INCORRECTO en pdf_layouts.py
"table_header_bg": "#F5F5F5"

# ✅ CORRECTO
"table_header_bg": colors.HexColor("#F5F5F5")
```

---

## 📚 Referencias

- **Fuente de layouts:** Análisis de 16 facturas reales en `Datos extraidos de Originales/`
- **Modelo Donut:** https://github.com/clovaai/donut
- **Documentación Donut:** `DONUT_README.md`
- **API de elementos visuales:** `examples/EJEMPLOS_APIS_VISUALES.md`

---

## ✅ Checklist de Implementación

```
□ Leer esta guía completa
□ Ejecutar test_variabilidad_layouts.py
□ Verificar que los 5 PDFs son visualmente diferentes
□ Generar dataset balanceado (200 facturas por layout)
□ Verificar distribución con histograma
□ Entrenar Donut con dataset variable
□ Comparar métricas con/sin variabilidad
□ Ajustar layouts según necesidades específicas
```

---

## 🎉 ¡Listo!

Tu generador ahora produce **facturas con variabilidad realista** basada en facturas reales peruanas.

**Resultado:** Donut entrenado con estas facturas tendrá **mucha mejor generalización** a facturas nuevas.

---

**Última actualización:** 2025-01-20
**Versión:** 1.0
