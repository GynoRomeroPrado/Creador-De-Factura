# 🚀 Guía de Instalación y Prueba - Elementos Visuales

Todo el código está implementado y listo. Sigue estos pasos para probarlo:

---

## 📦 Paso 1: Instalar Dependencias

```bash
cd /home/user/Creador-De-Factura

# Opción A: Instalar todo
pip install -r requirements.txt

# Opción B: Solo las nuevas dependencias
pip install requests qrcode[pil]
```

**Dependencias nuevas agregadas:**
- `requests>=2.31.0` - Para descargar logos e íconos
- `qrcode[pil]>=7.4.0` - Para generar códigos QR localmente

---

## 🧪 Paso 2: Ejecutar Test

```bash
python test_facturas_visuales.py
```

**Salida esperada:**
```
============================================================
🎨 TEST DE FACTURAS CON ELEMENTOS VISUALES
============================================================

📋 Configuración:
   - Elementos visuales: ACTIVADOS
   - Logos: UI Avatars API
   - QR: Generación local
   - Íconos: Simple Icons + Iconify

============================================================
Generando facturas de prueba...
============================================================

1️⃣  Factura GENERAL - TURISMO DIAS S.A.
   ✅ facturas_test_visuales/Factura_general_F001_00000123_20250119.pdf
   📌 Debe tener: Logo TURISMO (azul), QR, íconos

2️⃣  Factura HOTEL - Costa del Sol
   ✅ facturas_test_visuales/Factura_hotel_F001_00000456_20250119.pdf
   📌 Debe tener: Logo HOTEL (púrpura), QR, íconos

3️⃣  Factura SEGURO
   ✅ facturas_test_visuales/Factura_seguro_F001_00000789_20250119.pdf
   📌 Debe tener: Logo SEGURO (verde), QR, íconos

4️⃣  Factura CON DESCUENTO - Construcción
   ✅ facturas_test_visuales/Factura_con_descuento_F001_00001011_20250119.pdf
   📌 Debe tener: Logo CONSTRUCCION (naranja), QR, íconos

5️⃣  Factura SIN elementos visuales (para comparar)
   ✅ facturas_test_visuales/factura_SIN_visuales.pdf
   📌 Debe tener: Solo texto, sin logos ni QR

============================================================
✅ PRUEBAS COMPLETADAS
============================================================

📁 Archivos generados en: facturas_test_visuales/

🔍 Verifica que las facturas tengan:
   ✓ Logo de empresa (esquina superior izquierda)
   ✓ Código QR (esquina inferior derecha)
   ✓ Íconos de pago (pie de página)
   ✓ Íconos de contacto (teléfono, email)
   ✓ Marca de agua 'FACTURA FICTICIA' (diagonal)

💡 Compara la factura #5 (sin visuales) con las demás
   para ver la diferencia!
```

---

## 📄 Paso 3: Ver las Facturas Generadas

```bash
cd facturas_test_visuales/
ls -la

# Abrir una factura para verificar
# En Linux:
xdg-open Factura_hotel_F001_*.pdf

# En Mac:
open Factura_hotel_F001_*.pdf

# En Windows:
start Factura_hotel_F001_*.pdf
```

---

## 🎨 Paso 4: Usar en tu Código

### Opción 1: Con elementos visuales (por defecto)

```python
from src.generator import FacturaGenerator
from src.pdf_creator import PDFFactura

# Generar datos
gen = FacturaGenerator()
factura = gen.generar_factura(tipo_factura='hotel', con_credito=True)

# Crear PDF CON elementos visuales
pdf = PDFFactura(use_visual_elements=True)  # ← ACTIVADO
archivo = pdf.crear_factura(factura)

print(f"✅ Factura con logos, QR e íconos: {archivo}")
```

### Opción 2: Sin elementos visuales

```python
# Crear PDF SIN elementos visuales (como antes)
pdf = PDFFactura(use_visual_elements=False)  # ← DESACTIVADO
archivo = pdf.crear_factura(factura)

print(f"✅ Factura tradicional: {archivo}")
```

### Opción 3: Generar múltiples facturas

```python
from src.generator import FacturaGenerator
from src.pdf_creator import PDFFactura

gen = FacturaGenerator()
pdf = PDFFactura(output_dir="mis_facturas", use_visual_elements=True)

# Generar 10 facturas de diferentes tipos
tipos = ['general', 'hotel', 'seguro', 'con_descuento']

for i in range(10):
    tipo = tipos[i % len(tipos)]
    factura = gen.generar_factura(tipo_factura=tipo)
    archivo = pdf.crear_factura(factura)
    print(f"{i+1}. {archivo}")
```

---

## 🔧 Verificación del Código (sin ejecutar)

Si no puedes instalar las dependencias, puedes verificar que el código esté bien:

```bash
# Verificar sintaxis de Python
python -m py_compile src/pdf_creator.py
python -m py_compile test_facturas_visuales.py

# Si no hay errores, el código está bien escrito
echo "✅ Código sin errores de sintaxis"
```

---

## 🎯 ¿Qué Deberías Ver en las Facturas?

### Factura CON elementos visuales:

```
┌────────────────────────────────────────────────────────┐
│                                                        │
│  [LOGO]          R.U.C. 20438637380                   │
│   TD            FACTURA ELECTRÓNICA                    │
│                      F001-00000123                     │
│                                                        │
│  TURISMO DIAS S.A.                                    │
│  Dir: Av. Principal 123                               │
│  Tel: (044) 123-4567                                  │
│  Email: contacto@turismodias.com                      │
│                                                        │
│  ────────────────────────────────────────────────      │
│                                                        │
│  Cliente: EMPRESA XYZ S.A.C.                          │
│  RUC: 20987654321                                     │
│                                                        │
│  ────────────────────────────────────────────────      │
│                                                        │
│  Items...                                             │
│  ────────────────────────────────────────────────      │
│                                                        │
│  TOTAL: S/ 1,250.50                                   │
│                                                        │
│  ────────────────────────────────────────────────      │
│                                                        │
│  Aceptamos: [VISA] [MC] [💵]                    [QR]  │
│  [📞] (044) 123-4567  [✉] contacto@...         Escanea│
│                                                verificar│
└────────────────────────────────────────────────────────┘

     Marca de agua diagonal: "FACTURA FICTICIA"
```

### Factura SIN elementos visuales:

```
┌────────────────────────────────────────────────────────┐
│                                                        │
│                    R.U.C. 20438637380                  │
│                  FACTURA ELECTRÓNICA                   │
│                      F001-00000123                     │
│                                                        │
│  TURISMO DIAS S.A.                                    │
│  Dir: Av. Principal 123                               │
│  Tel: (044) 123-4567                                  │
│  Email: contacto@turismodias.com                      │
│                                                        │
│  ────────────────────────────────────────────────      │
│                                                        │
│  Cliente: EMPRESA XYZ S.A.C.                          │
│  RUC: 20987654321                                     │
│                                                        │
│  ────────────────────────────────────────────────      │
│                                                        │
│  Items...                                             │
│  ────────────────────────────────────────────────      │
│                                                        │
│  TOTAL: S/ 1,250.50                                   │
│                                                        │
│  ────────────────────────────────────────────────      │
│                                                        │
│  (Solo texto, sin logos ni QR)                        │
│                                                        │
└────────────────────────────────────────────────────────┘
```

---

## ⚠️ Troubleshooting

### Error: "ModuleNotFoundError: No module named 'requests'"

```bash
pip install requests
```

### Error: "ModuleNotFoundError: No module named 'qrcode'"

```bash
pip install qrcode[pil]
```

### Warning: "⚠️ requests/PIL no disponible"

- Esto es solo un warning
- El código funcionará con fallback (logos simples)
- Para mejores resultados, instala: `pip install requests pillow`

### Warning: "⚠️ qrcode no disponible"

- Esto es solo un warning
- Las facturas se generarán sin código QR
- Para agregar QR, instala: `pip install qrcode[pil]`

### No se ven los logos/íconos

1. Verificar conexión a internet (para descargar desde APIs)
2. Si estás offline, verás logos simples (círculo con iniciales)
3. Los QR siempre funcionan (se generan localmente)

---

## 📊 Resumen de Cambios Implementados

| Archivo | Líneas Agregadas | Descripción |
|---------|------------------|-------------|
| `src/pdf_creator.py` | +436 | 9 métodos nuevos para elementos visuales |
| `test_facturas_visuales.py` | +120 | Script de prueba completo |
| `requirements.txt` | +2 | requests y qrcode |
| **TOTAL** | **+558** | Funcionalidad completa |

---

## ✅ Checklist de Verificación

Después de ejecutar el test, verifica:

```
□ Se generaron 5 PDFs en facturas_test_visuales/
□ Factura #1 tiene logo azul (TURISMO)
□ Factura #2 tiene logo púrpura (HOTEL)
□ Factura #3 tiene logo verde (SEGURO)
□ Factura #4 tiene logo naranja (CONSTRUCCION)
□ Factura #5 NO tiene logos (comparación)
□ Todas excepto #5 tienen código QR en esquina inferior derecha
□ Todas excepto #5 tienen íconos de Visa/Mastercard/Efectivo
□ Todas excepto #5 tienen íconos de teléfono/email
□ Todas excepto #5 tienen marca de agua "FACTURA FICTICIA"
```

---

## 🎉 ¡Listo!

Tu sistema ahora genera facturas con elementos visuales profesionales:
- ✅ Logos automáticos por tipo de empresa
- ✅ Códigos QR escaneables
- ✅ Íconos de métodos de pago
- ✅ Íconos de contacto
- ✅ Marca de agua

Todo está **integrado** en tu código y **listo para usar**.

---

**Siguiente paso:** Ejecuta `python test_facturas_visuales.py` y abre los PDFs generados!
