# HTMLDocs - Generador de Facturas

Sistema de renderizado de facturas usando HTMLDocs (React + Tailwind).

## Instalación

```bash
cd htmldocs-invoices
npm install
```

## Uso

### Desde Python (integrado)

```python
from src.htmldocs_renderer import HTMLDocsRenderer, crear_pdf_factura

# Opción 1: Función rápida
crear_pdf_factura(datos_factura, 'output.pdf')

# Opción 2: Clase completa
renderer = HTMLDocsRenderer()
datos = renderer.transformar_datos_factura(factura_dict)
renderer.render_factura(datos, 'factura.pdf')
```

### Desde CLI

```bash
# Usar HTMLDocs como renderer
python main.py --cantidad 10 --renderer htmldocs

# Usar reportlab (default)
python main.py --cantidad 10 --renderer reportlab
```

### Desarrollo de templates

```bash
npm run dev  # Inicia servidor de desarrollo
```

## Estructura

```
htmldocs-invoices/
├── documents/
│   └── factura.tsx    # Template React de factura
├── generate-pdf.js    # Script de generación
├── package.json
└── tsconfig.json
```

## Características

- Templates en React/TypeScript
- Estilos con Tailwind CSS
- Soporte para facturas peruanas (SUNAT)
- Tipos: general, hotel, seguro, con descuento
- Multidivisa: PEN, USD, EUR
