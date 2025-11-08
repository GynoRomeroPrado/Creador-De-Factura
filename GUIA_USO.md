# Guía de Uso - Generador de Facturas Ficticias

## Instalación

### 1. Requisitos previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

## Uso Básico

### Generar facturas ficticias

```bash
# Generar 10 facturas (por defecto)
python main.py

# Generar 50 facturas
python main.py --cantidad 50

# Generar 100 facturas en un directorio específico
python main.py --cantidad 100 --output ./mis_facturas/
```

### Analizar facturas originales

Si tienes facturas originales que quieres analizar antes de generar nuevas:

```bash
# Analizar facturas en la carpeta facturas_originales/
python main.py --analizar --input ./facturas_originales/

# Analizar y luego generar
python main.py --analizar --input ./facturas_originales/ --cantidad 50
```

## Características de las Facturas Generadas

El software genera facturas con las siguientes características:

### Datos Variables

1. **RUC** - Genera RUCs válidos de 11 dígitos con dígito verificador correcto
2. **Razón Social** - Nombres de empresas ficticias peruanas
3. **Direcciones** - Direcciones realistas de Lima y otras ciudades
4. **Teléfonos** - Números de teléfono fijos y celulares
5. **Fechas** - Todas las fechas son del año 2025 (desde enero hasta diciembre)

### Items

Las facturas incluyen items de diferentes categorías:

- **Construcción**: Cemento, arena, piedra, fierro, ladrillos, etc.
- **Comida**: Arroz, aceite, azúcar, carne, pescado, etc.
- **Servicios**: Mantenimiento, instalación, consultoría, transporte, etc.

### Cálculos Financieros

Todos los cálculos son correctos y coherentes:

- **Operación Gravada**: Base imponible
- **IGV (18%)**: Calculado sobre la operación gravada
- **Operación Exonerada**: Aplicable en algunos casos (20% de probabilidad)
- **Operación Inafecta**: Aplicable ocasionalmente (10% de probabilidad)
- **Total**: Suma correcta de todos los conceptos
- **Monto en Letras**: Conversión automática del total a palabras

### Formas de Pago

- Efectivo
- Transferencia bancaria
- Cheque
- Depósito en cuenta
- Crédito a 30, 60 o 90 días

### Pago a Crédito

Cuando la factura es a crédito, incluye:

- Número de cuotas (2, 3, 4 o 6)
- Monto por cuota
- Fecha de vencimiento de cada cuota
- La suma de todas las cuotas coincide exactamente con el total

### Monedas

Las facturas se generan en:

- **PEN** - Soles (S/)
- **USD** - Dólares ($)
- **EUR** - Euros (€)

### Datos Opcionales

Algunas facturas incluyen:

- **Número de Contrato**: 30% de probabilidad
- **Periodo Facturado**: Común en servicios
- **Observaciones**: 30% de probabilidad

## Estructura de Archivos Generados

Los archivos PDF se nombran automáticamente:

```
Factura_F001_000123_20250315.pdf
```

Donde:
- `F001` es la serie
- `000123` es el número
- `20250315` es la fecha (AAAAMMDD)

## Ejemplos de Uso Avanzado

### Generar facturas solo de construcción

Modifica el archivo `main.py` temporalmente:

```python
factura = gen_factura.generar_factura(
    categoria_items='construccion',  # o 'comida', 'servicios'
    num_items=5,                     # número fijo de items
    moneda='PEN',                    # solo soles
    con_credito=True                 # solo a crédito
)
```

### Personalización

Puedes editar los archivos en `src/` para personalizar:

- `utils.py`: Agregar más nombres, empresas, direcciones, items
- `generator.py`: Modificar lógica de generación
- `pdf_creator.py`: Cambiar diseño de las facturas

## Solución de Problemas

### Error: "No module named 'reportlab'"

```bash
pip install reportlab
```

### Error: "Permission denied"

Asegúrate de tener permisos de escritura en el directorio de salida:

```bash
chmod +w facturas_generadas/
```

### Las facturas no se ven bien

Verifica que tienes instaladas todas las dependencias:

```bash
pip install -r requirements.txt --upgrade
```

## Notas Importantes

1. **RUCs Ficticios**: Aunque tienen formato válido, son completamente ficticios
2. **Datos de Ejemplo**: Todos los datos son generados aleatoriamente
3. **Uso Legal**: Este software es solo para propósitos de prueba y desarrollo
4. **No para Producción**: No usar para generar documentos tributarios reales

## Próximas Mejoras

- [ ] OCR para extraer datos de facturas originales en imagen
- [ ] Extracción de fuentes tipográficas de PDFs originales
- [ ] Clonación de diseño de facturas originales
- [ ] Generación de más tipos de comprobantes (Boletas, Notas de Crédito, etc.)
- [ ] Exportación a otros formatos (Excel, JSON, XML)
- [ ] Validación contra SUNAT (en modo simulación)

## Soporte

Para reportar problemas o sugerencias, contactar al desarrollador.
