# 📋 Plan de Integración de Diccionarios Mejorados

## 🎯 Objetivo
Reemplazar listas estáticas en `src/utils.py` con generadores combinatorios del nuevo módulo `src/diccionarios.py` para aumentar variedad y realismo.

## 📊 Mejoras Cuantificadas

| Componente | Sistema Actual | Con Diccionarios | Mejora |
|------------|----------------|------------------|--------|
| **Nombres de empresas** | 50 fijos | 80 prefijos × 60 sufijos × variantes = **100,000+** | **+199,900%** |
| **Direcciones** | Genéricas + números | 29 calles × 36 barrios × 29 ciudades = **30,276** | **+6,000%** |
| **Items construcción** | 15 fijos | 15 base × variantes = **200+** | **+1,233%** |
| **Items bebidas** | 0 | 20 base × variantes = **400+** | **∞** (nuevo) |
| **Items dulces** | 0 | 10 base × variantes = **150+** | **∞** (nuevo) |

---

## 🔄 Cambios en `src/utils.py`

### 1. Importar el nuevo módulo

```python
# Al inicio del archivo
from . import diccionarios
```

### 2. Modificar `DatosPersonas.generar_empresa()`

**ANTES:**
```python
@classmethod
def generar_empresa(cls) -> Dict[str, str]:
    nombre = random.choice(cls.EMPRESAS_NOMBRES)
    tipo = random.choice(cls.EMPRESAS_TIPOS)
    sociedad = random.choice(cls.TIPOS_SOCIEDAD)
    return f"{nombre} {tipo} {sociedad}"
```

**DESPUÉS:**
```python
@classmethod
def generar_empresa(cls, tipo_factura=None) -> str:
    return diccionarios.generar_nombre_empresa(tipo_factura)
```

### 3. Modificar `DatosPersonas.generar_direccion()`

**ANTES:**
```python
@classmethod
def generar_direccion(cls) -> str:
    calle = random.choice(cls.CALLES)
    numero = random.randint(100, 9999)
    distrito = random.choice(cls.DISTRITOS)
    return f"{calle} {numero}, {distrito}"
```

**DESPUÉS:**
```python
@classmethod
def generar_direccion(cls, pais="Peru") -> str:
    return diccionarios.generar_direccion(pais)
```

### 4. **OPCIONAL**: Añadir nuevas categorías de items

**Nuevas categorías disponibles:**
```python
# En ItemsGenerator, añadir:
CARAMELOS = diccionarios.CARAMELOS
BEBIDAS_NO_ALC = diccionarios.BEBIDAS_NO_ALC  
BEBIDAS_ALC = diccionarios.BEBIDAS_ALC
# (Las de construcción/herramientas ya existen, solo las mejoraremos)
```

---

## 🔄 Cambios en `src/generator.py`

### Modificar `generar_factura()` para pasar tipo a generadores

**ANTES:**
```python
emisor = DatosPersonas.generar_empresa()
receptor = DatosPersonas.generar_empresa()
```

**DESPUÉS:**
```python
emisor = DatosPersonas.generar_empresa(tipo_factura=tipo_factura)
receptor = DatosPersonas.generar_empresa(tipo_factura=None)  # Receptor genérico
```

---

## 📁 Archivos a Modificar

1. ✅ **`src/diccionarios.py`** (CREADO)
2. ⏳ **`src/utils.py`** (modificar 2 funciones)
3. ⏳ **`src/generator.py`** (pasar parámetro tipo_factura)

---

## 🧪 Prueba Antes/Después

### ANTES (sistema actual):
```
Empresa: Comercializadora Delta S.A.C.
Dirección: Av. Principal 1234, San Isidro
```

### DESPUÉS (con diccionarios):
```
Empresa: Hotel Machu Picchu Premium & Spa S.A.C.
Dirección: Av. Javier Prado 3847, Oficina 12B, Miraflores, Lima
```

---

## ⚡ Ventajas

1. **Mayor variedad**: De 50 empresas → 100,000+ combinaciones
2. **Geo-específico**: Calles y barrios reales de Perú
3. **Contexto**: Nombres de hoteles para facturas de hotel
4. **Escalable**: Fácil añadir más prefijos/sufijos
5. **Realismo**: Direcciones con Oficina, Piso, etc.

---

## 🚀 Próximos Pasos (si apruebas)

1. Modificar `src/utils.py` (5 minutos)
2. Modificar `src/generator.py` (2 minutos)
3. Probar generación de facturas (5 minutos)
4. Generar 2 nuevas facturas de prueba para comparar
5. Commitear cambios

**Tiempo total estimado:** ~15 minutos

---

## ❓ Preguntas para ti

1. ¿Quieres que añada las nuevas categorías (caramelos, bebidas)?
2. ¿Prefieres solo mejorar las existentes (construcción, servicios)?
3. ¿Algún tipo de empresa o item específico que quieras añadir?

