# 🚀 QUICK START - 5 MINUTOS PARA EMPEZAR

**Sistema validado y listo. Sigue estos pasos:**

---

## 📋 PASO 1: PREPARAR TUS FACTURAS (2 min)

Organiza tus archivos en Google Drive así:

```
Mi Drive/
└── Facturas/
    ├── factura1.pdf
    ├── factura1.json
    ├── factura2.jpg
    ├── factura2.json
    └── ...
```

**Importante:** Cada factura debe tener su JSON con el mismo nombre.

---

## 🔗 PASO 2: ABRIR NOTEBOOK EN COLAB (30 seg)

**Opción A - Link directo (MÁS FÁCIL):**

Haz clic aquí → [Abrir Notebook](https://colab.research.google.com/github/GynoRomeroPrado/Creador-De-Factura/blob/claude/colab-invoice-processor-011CUuowDXaNFjHtgp9gChim/Invoice_Dataset_Processor.ipynb)

**Opción B - Manual:**
1. Ve a https://colab.research.google.com/
2. "Archivo" → "Abrir notebook" → pestaña "GitHub"
3. Pega: `https://github.com/GynoRomeroPrado/Creador-De-Factura`
4. Branch: `claude/colab-invoice-processor-011CUuowDXaNFjHtgp9gChim`
5. Abre: `Invoice_Dataset_Processor.ipynb`

---

## ⚙️ PASO 3: CONFIGURAR RUTAS (1 min)

**Celda 3 del notebook:**

```python
# ⚠️ CAMBIAR ESTAS RUTAS
INPUT_FOLDER = "/content/drive/MyDrive/Facturas"           # ← Tu carpeta
OUTPUT_FOLDER = "/content/drive/MyDrive/Facturas_Procesadas"  # ← Salida

PIXEL_RANGE = 10  # Desplazamiento en píxeles (OK dejar en 10)
```

---

## ▶️ PASO 4: EJECUTAR (2 min)

Ejecuta las celdas **en orden**:

1. **Celda 1:** Instalar dependencias (~45 seg)
2. **Celda 2:** Montar Google Drive (~15 seg, autoriza el acceso)
3. **Celda 3:** Configurar rutas (~1 seg)
4. **Celda 4:** Cargar procesador (~2 seg)
5. **Celda 5:** 🚀 **PROCESAR** (~30 seg por factura)

---

## 📊 PASO 5: VERIFICAR RESULTADOS

Al finalizar verás:

```
======================================================================
📊 REPORTE FINAL
======================================================================

✓ Facturas originales organizadas: 10
✓ Facturas aumentadas generadas: 160
✓ Variaciones por factura: 16
✓ Total facturas en dataset: 170

📁 Carpeta organizadas: /content/drive/MyDrive/Facturas_Procesadas/organized
📁 Carpeta aumentadas: /content/drive/MyDrive/Facturas_Procesadas/augmented

🎉 Proceso completado exitosamente!
```

**En tu Google Drive:**

```
Facturas_Procesadas/
├── organized/          ← 10 facturas renombradas
│   ├── factura_0001.pdf
│   ├── factura_0001.json
│   └── ...
│
├── augmented/          ← 160 facturas aumentadas
│   ├── factura_0001_aug_01_derecha.png
│   ├── factura_0001_aug_01_derecha.json
│   └── ...
│
└── dataset_report.json ← Estadísticas
```

---

## ✅ CHECKLIST RÁPIDO

Antes de ejecutar, verifica:

- [ ] Facturas están en Google Drive
- [ ] Cada factura tiene su JSON
- [ ] Modificaste `INPUT_FOLDER` en Celda 3
- [ ] Tienes espacio suficiente en Drive (~2GB para 10 facturas)

---

## 🎯 RESULTADO ESPERADO

**Input:** 10 facturas
**Output:** 170 facturas (10 organizadas + 160 aumentadas)

**Cada factura genera 16 variaciones:**
- 8 desplazamientos completos (±10px)
- 8 desplazamientos medios (±5px)

**Tiempo total:** ~5-10 minutos para 10 facturas

---

## 🆘 SI ALGO FALLA

**Error común #1:** "Carpeta no encontrada"
- Solución: Verifica la ruta en Celda 3

**Error común #2:** "No se encontraron pares"
- Solución: Cada factura necesita su JSON

**Error común #3:** "Out of memory"
- Solución: Procesa menos facturas a la vez

**Más soluciones:** Lee `VALIDACION_SISTEMA.md` sección 8

---

## 📚 DOCUMENTACIÓN COMPLETA

- `VALIDACION_SISTEMA.md` - Validación completa y troubleshooting
- `COMO_USAR_DESDE_GIT.md` - Guía detallada de uso
- `README_COLAB.md` - Documentación técnica

---

## 🎉 ¡LISTO!

**Tu dataset estará expandido en menos de 10 minutos.**

**Siguiente paso:** Usar tus comandos de Colab para generar bounding boxes sobre las facturas aumentadas.

---

**Versión:** 1.0
**Última actualización:** 2025-11-08
**Estado:** ✅ VALIDADO
