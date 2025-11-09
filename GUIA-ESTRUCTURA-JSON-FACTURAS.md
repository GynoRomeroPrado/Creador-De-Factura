# 📋 GUÍA COMPLETA - ESTRUCTURA JSON PARA FACTURAS

**Versión:** 5.5
**Fecha:** 2025-01-09
**Sistema:** Extracción con Gemini 2.5 Pro

---

## 🎯 RESUMEN EJECUTIVO

Esta es la estructura **OBLIGATORIA** que debe tener TODOS los JSON de facturas extraídas.

### ✅ Características principales:
- **97 campos base** en nivel raíz (estructura plana, NO anidada)
- **Array de items** con 26 campos por producto/servicio
- **Array de cuotas** para facturas a crédito
- **Formato de fechas:** `YYYY-MM-DD` (ejemplo: `2023-11-13`)
- **Moneda normalizada:** `SOLES` o `DOLARES AMERICANOS` (no símbolos ni códigos)
- **Campos vacíos:** usar `null` (NO strings vacíos `""`)
- **Arrays vacíos:** `[]` cuando no hay datos

---

## 📊 ESTRUCTURA COMPLETA (97 CAMPOS + ITEMS + CUOTAS)

```json
{
  // ═══════════════════════════════════════════════════════════════
  // SECCIÓN 1: DOCUMENTO (5 campos)
  // ═══════════════════════════════════════════════════════════════

  "tipo_documento": "FACTURA ELECTRONICA",
  "serie_completa": "F001-00000123",
  "fecha_emision": "2025-01-15",
  "fecha_vencimiento": "2025-02-14",
  "moneda": "SOLES",

  // ═══════════════════════════════════════════════════════════════
  // SECCIÓN 2: EMISOR (14 campos) - TODOS EN NIVEL RAÍZ
  // ═══════════════════════════════════════════════════════════════

  "emisor_ruc": "20123456789",
  "emisor_razon_social": "EMPRESA EJEMPLO S.A.C.",
  "emisor_nombre_comercial": "EJEMPLO",
  "emisor_direccion": "AV. PRINCIPAL 123",
  "emisor_sucursal": null,
  "emisor_departamento": "LIMA",
  "emisor_provincia": "LIMA",
  "emisor_distrito": "MIRAFLORES",
  "emisor_ubigeo": "150122",
  "emisor_codigo_postal": null,
  "emisor_telefono": "(51-1) 123-4567",
  "emisor_email": "contacto@ejemplo.com",
  "emisor_web": "www.ejemplo.com",
  "emisor_codigo_establecimiento": null,

  // ═══════════════════════════════════════════════════════════════
  // SECCIÓN 3: RECEPTOR (14 campos) - TODOS EN NIVEL RAÍZ
  // ═══════════════════════════════════════════════════════════════

  "receptor_numero_doc": "20987654321",
  "receptor_tipo_doc": "RUC",
  "receptor_razon_social": "CLIENTE EJEMPLO S.R.L.",
  "receptor_nombre_comercial": null,
  "receptor_direccion": "JR. COMERCIO 456",
  "receptor_contacto": null,
  "receptor_departamento": "LIMA",
  "receptor_provincia": "LIMA",
  "receptor_distrito": "SURCO",
  "receptor_ubigeo": "150140",
  "receptor_codigo_postal": null,
  "receptor_telefono": null,
  "receptor_email": null,
  "receptor_sucursal": null,

  // ═══════════════════════════════════════════════════════════════
  // SECCIÓN 4: IMPORTES Y TRIBUTOS (17 campos)
  // ═══════════════════════════════════════════════════════════════

  "subtotal": 1250.00,
  "descuento": 0.00,
  "subtotal_con_descuento": 1250.00,
  "igv": 225.00,
  "isc": null,
  "otros_cargos": 0.00,
  "importe_total": 1475.00,
  "tipo_cambio": null,
  "importe_total_moneda_base": null,
  "retencion_monto": null,
  "retencion_porcentaje": null,
  "percepcion_monto": null,
  "percepcion_porcentaje": null,
  "detraccion_monto": 147.50,
  "detraccion_porcentaje": 10.0,
  "detraccion_codigo_bienes": null,
  "anticipo_monto": null,
  "anticipo_numero": null,

  // ═══════════════════════════════════════════════════════════════
  // SECCIÓN 5: REFERENCIAS Y PAGOS (9 campos)
  // ═══════════════════════════════════════════════════════════════

  "numero_contrato": "CW120329",
  "orden_compra": "OC-2025-001",
  "orden_servicio": null,
  "numero_pedido": null,
  "guia_remision": "T001-00000123",
  "condicion_pago": "Credito 30 dias",
  "forma_pago": "TRANSFERENCIA",
  "cuenta_bancaria": null,
  "numero_cuenta_detraccion": "00000347620",

  // ═══════════════════════════════════════════════════════════════
  // SECCIÓN 6: INFORMACIÓN ADICIONAL (18 campos)
  // ═══════════════════════════════════════════════════════════════

  "glosa": "Venta de productos varios",
  "observaciones": "SON: MIL CUATROCIENTOS SETENTA Y CINCO CON 00/100 SOLES",
  "centro_costo": null,
  "proyecto": null,
  "ubicacion_obra": null,
  "numero_vale": null,
  "numero_placa": null,
  "referencia_1": null,
  "referencia_2": null,
  "cod_qr": null,
  "hash_sunat": null,
  "numero_autorizacion": null,
  "serie_fisica": null,
  "numero_fisico": null,
  "doc_relacionado_tipo": null,
  "doc_relacionado_numero": null,
  "doc_relacionado_fecha": null,
  "motivo_emision": null,

  // ═══════════════════════════════════════════════════════════════
  // SECCIÓN 7: CLASIFICACIÓN (9 campos)
  // ═══════════════════════════════════════════════════════════════

  "is_exportacion": false,
  "incoterm": null,
  "puerto_embarque": null,
  "puerto_destino": null,
  "nave": null,
  "numero_contenedor": null,
  "agente_retencion": true,
  "agente_percepcion": false,
  "buen_contribuyente": false,

  // ═══════════════════════════════════════════════════════════════
  // SECCIÓN 8: PERSONAL (4 campos)
  // ═══════════════════════════════════════════════════════════════

  "vendedor_codigo": null,
  "vendedor_nombre": null,
  "cajero_codigo": null,
  "cajero_nombre": null,

  // ═══════════════════════════════════════════════════════════════
  // SECCIÓN 9: FECHAS ADICIONALES (3 campos)
  // ═══════════════════════════════════════════════════════════════

  "fecha_registro": null,
  "fecha_pago": null,
  "fecha_cancelacion": null,

  // ═══════════════════════════════════════════════════════════════
  // SECCIÓN 10: ITEMS (ARRAY - 26 campos por item)
  // ═══════════════════════════════════════════════════════════════

  "items": [
    {
      "item": 1,
      "codigo": "PROD001",
      "descripcion": "Descripción completa del producto/servicio",
      "cantidad": 10.0,
      "unidad_medida": "UND",
      "precio_unitario": 100.00,
      "valor_venta": 1000.00,
      "descuento_item": 0.00,
      "subtotal_item": 1000.00,
      "tipo_igv": "GRAVADO",
      "igv_item": 180.00,
      "isc_item": null,
      "otro_tributo": null,
      "importe_total_item": 1180.00,
      "lote": null,
      "fecha_vencimiento": null,
      "serie": null,
      "modelo": null,
      "marca": null,
      "placa": null,
      "partida_arancelaria": null,
      "centro_costo_item": null,
      "cuenta_contable": null,
      "proyecto_item": null,
      "orden_item": null,
      "ubicacion": null,
      "observacion_item": null
    },
    {
      "item": 2,
      "codigo": "PROD002",
      "descripcion": "Otro producto",
      "cantidad": 5.0,
      "unidad_medida": "UND",
      "precio_unitario": 50.00,
      "valor_venta": 250.00,
      "descuento_item": 0.00,
      "subtotal_item": 250.00,
      "tipo_igv": "GRAVADO",
      "igv_item": 45.00,
      "isc_item": null,
      "otro_tributo": null,
      "importe_total_item": 295.00,
      "lote": null,
      "fecha_vencimiento": null,
      "serie": null,
      "modelo": null,
      "marca": null,
      "placa": null,
      "partida_arancelaria": null,
      "centro_costo_item": null,
      "cuenta_contable": null,
      "proyecto_item": null,
      "orden_item": null,
      "ubicacion": null,
      "observacion_item": null
    }
  ],

  // ═══════════════════════════════════════════════════════════════
  // SECCIÓN 11: CUOTAS (ARRAY - para facturas a crédito)
  // ═══════════════════════════════════════════════════════════════

  "cuotas": [
    {
      "numero": 1,
      "monto": 737.50,
      "fecha_vencimiento": "2025-02-14",
      "estado": "PENDIENTE"
    },
    {
      "numero": 2,
      "monto": 737.50,
      "fecha_vencimiento": "2025-03-14",
      "estado": "PENDIENTE"
    }
  ]
}
```

---

## 🔍 VALIDACIONES CRÍTICAS

### ✅ ESTRUCTURA
- [ ] **97 campos base** presentes (pueden ser `null` pero DEBEN existir)
- [ ] Todos los campos en **nivel raíz** (NO estructura anidada tipo `emisor: {}`)
- [ ] Array `items` presente (mínimo 1 item)
- [ ] Array `cuotas` presente (puede estar vacío `[]` si es contado)

### ✅ FORMATOS
- [ ] Fechas: `YYYY-MM-DD` (ejemplo: `2023-11-13`)
- [ ] Moneda: `SOLES` o `DOLARES AMERICANOS` (NO "PEN", "S/", "$", etc.)
- [ ] Números: tipo `number` (NO strings)
- [ ] Campos vacíos: `null` (NO `""`)
- [ ] Booleanos: `true` o `false` (NO strings)

### ✅ ITEMS (26 campos obligatorios por item)
- [ ] `item`: número secuencial (1, 2, 3...)
- [ ] `codigo`: puede ser `null`
- [ ] `descripcion`: string completo
- [ ] `cantidad`: tipo `number`
- [ ] `unidad_medida`: string (UND, NIU, KGM, etc.)
- [ ] `precio_unitario`: tipo `number`
- [ ] `valor_venta`: tipo `number`
- [ ] `descuento_item`: tipo `number`
- [ ] `subtotal_item`: tipo `number`
- [ ] `tipo_igv`: string (GRAVADO, EXONERADO, INAFECTO)
- [ ] `igv_item`: tipo `number`
- [ ] `isc_item`: `null` o `number`
- [ ] `otro_tributo`: `null` o `number`
- [ ] `importe_total_item`: tipo `number`
- [ ] 12 campos opcionales restantes: pueden ser `null`

### ✅ CUOTAS (cuando aplica)
- [ ] Si `condicion_pago` contiene "CREDITO" o "CRÉDITO": DEBE tener cuotas
- [ ] Cada cuota tiene: `numero`, `monto`, `fecha_vencimiento`, `estado`

---

## ❌ ERRORES COMUNES A EVITAR

### 1. **Estructura Anidada** ❌
```json
// MAL - NO HACER ESTO
{
  "emisor": {
    "ruc": "20123456789",
    "razon_social": "EMPRESA S.A."
  }
}
```

```json
// BIEN ✅
{
  "emisor_ruc": "20123456789",
  "emisor_razon_social": "EMPRESA S.A."
}
```

### 2. **Moneda con Símbolos** ❌
```json
// MAL
"moneda": "PEN"
"moneda": "S/"
"simbolo_moneda": "S/"
```

```json
// BIEN ✅
"moneda": "SOLES"
```

### 3. **Fechas con Hora/Formato ISO** ❌
```json
// MAL
"fecha_emision": "2025-12-23T00:00:00"
```

```json
// BIEN ✅
"fecha_emision": "2025-12-23"
```

### 4. **Strings Vacíos en Vez de Null** ❌
```json
// MAL
"emisor_telefono": ""
```

```json
// BIEN ✅
"emisor_telefono": null
```

### 5. **Campos Extras No Definidos** ❌
```json
// MAL - Estos campos NO existen en la estructura
"tipo_factura": "seguro"
"op_gravada": 166625.45
"total_letras": "..."
"datos_hotel": null
```

### 6. **Items con Campos Faltantes** ❌
```json
// MAL - Solo 6 campos
{
  "numero": 1,
  "descripcion": "...",
  "cantidad": 10,
  "precio_unitario": 100.00,
  "valor_venta": 1000.00,
  "unidad": "UND"
}
```

```json
// BIEN ✅ - 26 campos completos
{
  "item": 1,
  "codigo": null,
  "descripcion": "...",
  "cantidad": 10.0,
  "unidad_medida": "UND",
  "precio_unitario": 100.00,
  "valor_venta": 1000.00,
  "descuento_item": 0.00,
  "subtotal_item": 1000.00,
  "tipo_igv": "GRAVADO",
  "igv_item": 180.00,
  "isc_item": null,
  "otro_tributo": null,
  "importe_total_item": 1180.00,
  "lote": null,
  "fecha_vencimiento": null,
  "serie": null,
  "modelo": null,
  "marca": null,
  "placa": null,
  "partida_arancelaria": null,
  "centro_costo_item": null,
  "cuenta_contable": null,
  "proyecto_item": null,
  "orden_item": null,
  "ubicacion": null,
  "observacion_item": null
}
```

---

## 📌 CHECKLIST DE VALIDACIÓN RÁPIDA

Use este checklist para verificar cualquier JSON de factura:

```
✅ ESTRUCTURA BASE
[ ] Tiene exactamente 97 campos base + items + cuotas
[ ] Todos los campos están en nivel raíz (NO anidados)
[ ] No tiene campos extras no definidos

✅ SECCIONES COMPLETAS
[ ] Sección 1: Documento (5 campos)
[ ] Sección 2: Emisor (14 campos con prefijo emisor_)
[ ] Sección 3: Receptor (14 campos con prefijo receptor_)
[ ] Sección 4: Importes (17 campos)
[ ] Sección 5: Referencias (9 campos)
[ ] Sección 6: Adicionales (18 campos)
[ ] Sección 7: Clasificación (9 campos)
[ ] Sección 8: Personal (4 campos)
[ ] Sección 9: Fechas adicionales (3 campos)

✅ ITEMS
[ ] Array items presente
[ ] Cada item tiene 26 campos
[ ] Campo "item" es número secuencial (1, 2, 3...)
[ ] Campo "unidad_medida" (NO "unidad")

✅ CUOTAS
[ ] Array cuotas presente
[ ] Si es crédito, tiene al menos 1 cuota
[ ] Cada cuota tiene: numero, monto, fecha_vencimiento, estado

✅ FORMATOS
[ ] Fechas: YYYY-MM-DD
[ ] Moneda: SOLES o DOLARES AMERICANOS
[ ] Campos vacíos: null (NO "")
[ ] Números: tipo number (NO strings)
```

---

## 🎯 EJEMPLO REAL VALIDADO

Este es un ejemplo de un JSON **CORRECTO** generado por nuestro sistema:

Ver archivo: `G:\Extraccion Data\Datos extraidos de Dataset completo 0811\anotaciones\20553327971-4987822-F596-23196.json`

**Características:**
- ✅ 97 campos base completos
- ✅ Items con 26 campos
- ✅ Estructura plana (no anidada)
- ✅ Formatos correctos
- ✅ Validación matemática correcta

---

## 📞 CONTACTO Y SOPORTE

Si encuentras un JSON que NO cumple con esta estructura:

1. **Verificar origen**: ¿Fue generado por nuestro sistema con Gemini 2.5 Pro?
2. **Comparar con ejemplo**: Usar el JSON de ejemplo como referencia
3. **Revisar el prompt**: Verificar que `process_batch.py` tenga el prompt completo
4. **Re-procesar**: Si es necesario, volver a procesar la factura

---

**IMPORTANTE:** Esta estructura es OBLIGATORIA para integración con la base de datos v5.5. Cualquier JSON que no cumpla con estos 97 campos + items + cuotas será RECHAZADO por el sistema de importación.

---

**Última actualización:** 2025-01-09
**Generado por:** Sistema de extracción con Gemini 2.5 Pro
