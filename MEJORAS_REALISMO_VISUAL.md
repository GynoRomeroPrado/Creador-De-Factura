# 🎨 Mejoras de Realismo Visual para Facturas Generadas

**Fecha:** 2025-01-19
**Objetivo:** Agregar logos, íconos, códigos QR y elementos visuales a las facturas generadas

---

## 🔍 Análisis: ¿Qué les falta a nuestras facturas?

### Facturas Reales tienen:
- ✅ **Logo de la empresa** (esquina superior izquierda)
- ✅ **Código QR** (para validación SUNAT)
- ✅ **Íconos de pago** (Visa, Mastercard, efectivo, etc.)
- ✅ **Íconos de certificación** (ISO, SUNAT autorizado, etc.)
- ✅ **Marca de agua** (opcional, "COPIA", "ORIGINAL")
- ✅ **Pie de página con íconos** (teléfono, email, web, ubicación)
- ✅ **Banners promocionales** (opcional)

### Nuestras Facturas tienen:
- ✅ Diseño profesional
- ✅ Tipografía uniforme
- ✅ Tabla de items bien estructurada
- ❌ **Sin logos**
- ❌ **Sin códigos QR**
- ❌ **Sin íconos visuales**
- ❌ **Sin elementos gráficos**

---

## 🎯 Opciones de Implementación

### **OPCIÓN 1: APIs Gratuitas (Recomendado)** ⭐

Usar servicios externos para generar imágenes dinámicamente.

#### **Ventajas:**
- ✅ Gratis para uso comercial
- ✅ Sin límites (la mayoría)
- ✅ Gran variedad de estilos
- ✅ No requiere almacenar archivos

#### **Desventajas:**
- ❌ Requiere conexión a internet
- ❌ Dependencia de servicios externos

---

### **OPCIÓN 2: Biblioteca Local de Imágenes**

Descargar y almacenar íconos/logos localmente.

#### **Ventajas:**
- ✅ No requiere internet
- ✅ Control total de los assets
- ✅ Más rápido

#### **Desventajas:**
- ❌ Requiere espacio de almacenamiento
- ❌ Menor variedad
- ❌ Necesita actualización manual

---

### **OPCIÓN 3: Generación Programática (Python)**

Generar logos/íconos con código Python.

#### **Ventajas:**
- ✅ Sin dependencias externas
- ✅ Personalización total
- ✅ Sin límites de licencia

#### **Desventajas:**
- ❌ Más complejo de implementar
- ❌ Logos genéricos (no realistas)

---

## 📦 APIs Gratuitas Recomendadas

### 1. **Logos de Empresas Ficticias**

#### **UI Avatars** (Texto → Logo)
```
https://ui-avatars.com/api/?name=EMPRESA+SA&size=128&background=random&color=fff&bold=true
```

**Características:**
- Genera logos con iniciales
- Múltiples backgrounds
- Formatos: PNG, SVG
- Sin límites de uso
- Parámetros: nombre, tamaño, color, fuente

**Ejemplo de uso:**
```python
def generar_logo_empresa(razon_social):
    """Genera URL de logo basado en el nombre de la empresa"""
    nombre = razon_social.replace(" ", "+")
    return f"https://ui-avatars.com/api/?name={nombre}&size=200&background=random&color=fff&bold=true&font-size=0.4"

# Ejemplo:
logo_url = generar_logo_empresa("TURISMO DIAS S.A.")
# → https://ui-avatars.com/api/?name=TURISMO+DIAS+S.A.&size=200...
```

#### **DiceBear Avatars** (Estilos variados)
```
https://api.dicebear.com/7.x/initials/svg?seed=EMPRESA&backgroundColor=1e88e5
```

**Características:**
- 20+ estilos diferentes (initials, shapes, bottts, etc.)
- SVG o PNG
- Personalizable
- Sin límites

**Estilos útiles para empresas:**
- `initials` - Iniciales elegantes
- `shapes` - Formas geométricas
- `thumbs` - Iconos simples
- `identicon` - Patrón único por nombre

**Ejemplo:**
```python
DICEBEAR_STYLES = ['initials', 'shapes', 'thumbs', 'identicon']

def generar_logo_dicebear(razon_social, style='initials'):
    seed = razon_social.replace(" ", "")
    colors = ['1e88e5', 'e53935', '43a047', 'fb8c00', '8e24aa']
    bg = random.choice(colors)
    return f"https://api.dicebear.com/7.x/{style}/svg?seed={seed}&backgroundColor={bg}"
```

#### **Boring Avatars** (Diseños minimalistas)
```
https://source.boringavatars.com/beam/200/EMPRESA?colors=264653,2a9d8f,e76f51,f4a261,e9c46a
```

**Características:**
- Estilos: beam, bauhaus, ring, pixel, sunset, marble
- Paletas de color personalizables
- SVG
- Gratis sin límites

---

### 2. **Códigos QR**

#### **GoQR.me API**
```
https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=20438637380-03-F001-00000123
```

**Características:**
- Gratis sin límites
- Tamaños variables
- Formatos: PNG, SVG
- Nivel de corrección ajustable

**Ejemplo:**
```python
def generar_qr_factura(ruc, tipo, serie, numero):
    """Genera QR según formato SUNAT"""
    # Formato: RUC|TipoComprobante|Serie|Numero|FechaEmision|Total
    data = f"{ruc}|03|{serie}|{numero}"
    return f"https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={data}"

# Ejemplo:
qr_url = generar_qr_factura("20438637380", "03", "F001", "00000123")
```

#### **QRCode.js (Local - Python)**
```bash
pip install qrcode[pil]
```

```python
import qrcode
from io import BytesIO

def generar_qr_local(datos):
    """Genera QR localmente sin API"""
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(datos)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Guardar en memoria
    buffer = BytesIO()
    img.save(buffer, format='PNG')
    buffer.seek(0)
    return buffer
```

---

### 3. **Íconos de Pago**

#### **Simple Icons** (Logos de marcas)
```
https://cdn.simpleicons.org/visa/1A1F71
https://cdn.simpleicons.org/mastercard/EB001B
https://cdn.simpleicons.org/americanexpress/006FCF
```

**Características:**
- 2800+ logos de marcas
- SVG
- Personalizable (color)
- Gratis para uso comercial

**Íconos útiles:**
```python
PAYMENT_ICONS = {
    'visa': 'https://cdn.simpleicons.org/visa/1A1F71',
    'mastercard': 'https://cdn.simpleicons.org/mastercard/EB001B',
    'amex': 'https://cdn.simpleicons.org/americanexpress/006FCF',
    'paypal': 'https://cdn.simpleicons.org/paypal/00457C',
}
```

#### **Iconify API**
```
https://api.iconify.design/mdi/cash.svg?color=%23000000&width=24
https://api.iconify.design/mdi/credit-card.svg?color=%23000000&width=24
```

**Características:**
- 200,000+ íconos
- SVG
- Múltiples colecciones (Material Design, FontAwesome, etc.)
- Gratis

**Ejemplo:**
```python
FOOTER_ICONS = {
    'phone': 'https://api.iconify.design/mdi/phone.svg?color=%23666666',
    'email': 'https://api.iconify.design/mdi/email.svg?color=%23666666',
    'web': 'https://api.iconify.design/mdi/web.svg?color=%23666666',
    'location': 'https://api.iconify.design/mdi/map-marker.svg?color=%23666666',
}
```

---

### 4. **Placeholders para Imágenes Genéricas**

#### **Placehold.co**
```
https://placehold.co/600x100/2C3E50/FFFFFF/png?text=BANNER+PROMOCIONAL
```

**Características:**
- Texto personalizado
- Colores personalizables
- Múltiples formatos (PNG, JPEG, WebP, SVG)
- Tamaños variables

**Uso:**
```python
def generar_banner(texto, ancho=600, alto=80):
    texto_encoded = texto.replace(" ", "+")
    return f"https://placehold.co/{ancho}x{alto}/1e88e5/ffffff/png?text={texto_encoded}"
```

#### **Lorem Picsum** (Imágenes aleatorias)
```
https://picsum.photos/200/100?random=123
```

**Características:**
- Fotos reales de stock
- Aleatorias o por ID
- Efectos: blur, grayscale
- Gratis

---

## 💻 Implementación en pdf_creator.py

### Paso 1: Instalar Dependencias

```bash
# Para descargar y usar imágenes desde URLs
pip install pillow requests

# Para QR local (opcional)
pip install qrcode[pil]
```

### Paso 2: Modificar PDFFactura

```python
# Agregar al inicio del archivo
from PIL import Image
import requests
from io import BytesIO
import qrcode

class PDFFactura:
    # ... código existente ...

    def _descargar_imagen(self, url, max_retries=3):
        """Descarga imagen desde URL con reintentos"""
        for intento in range(max_retries):
            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    return BytesIO(response.content)
            except Exception as e:
                if intento == max_retries - 1:
                    print(f"⚠️ Error descargando imagen: {e}")
                    return None
        return None

    def _dibujar_logo_empresa(self, c, datos, width, height):
        """Dibuja logo de la empresa (esquina superior izquierda)"""
        # Generar URL del logo
        razon_social = datos['emisor']['razon_social']
        logo_url = f"https://ui-avatars.com/api/?name={razon_social.replace(' ', '+')}&size=200&background=random&color=fff&bold=true&font-size=0.4"

        # Descargar logo
        logo_data = self._descargar_imagen(logo_url)

        if logo_data:
            try:
                # Posición del logo
                logo_x = 30
                logo_y = height - 120
                logo_size = 90

                # Dibujar imagen
                c.drawImage(
                    Image.open(logo_data),
                    logo_x,
                    logo_y,
                    width=logo_size,
                    height=logo_size,
                    preserveAspectRatio=True,
                    mask='auto'
                )
            except Exception as e:
                print(f"⚠️ Error dibujando logo: {e}")

    def _dibujar_qr_code(self, c, datos, width, height):
        """Dibuja código QR (esquina inferior derecha)"""
        # Datos del QR según formato SUNAT
        ruc = datos['emisor']['ruc']
        serie = datos['serie']
        numero = datos['numero']
        fecha = datos['fecha_emision'].strftime('%Y%m%d')
        total = f"{datos['total']:.2f}"

        # Formato: RUC|TipoDoc|Serie|Numero|Fecha|Total
        qr_data = f"{ruc}|03|{serie}|{numero}|{fecha}|{total}"

        # Opción 1: API externa
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=100x100&data={qr_data}"
        qr_image = self._descargar_imagen(qr_url)

        # Opción 2: Generación local (más rápido)
        if not qr_image:
            qr = qrcode.QRCode(version=1, box_size=5, border=2)
            qr.add_data(qr_data)
            qr.make(fit=True)
            img = qr.make_image(fill_color="black", back_color="white")

            buffer = BytesIO()
            img.save(buffer, format='PNG')
            buffer.seek(0)
            qr_image = buffer

        if qr_image:
            try:
                # Posición del QR (esquina inferior derecha)
                qr_x = width - 130
                qr_y = 50
                qr_size = 80

                c.drawImage(
                    Image.open(qr_image),
                    qr_x,
                    qr_y,
                    width=qr_size,
                    height=qr_size,
                    preserveAspectRatio=True
                )

                # Texto debajo del QR
                c.setFont(self.FONT_ITALIC, 6)
                c.setFillColor(colors.grey)
                c.drawCentredString(qr_x + qr_size/2, qr_y - 10, "Escanea para verificar")
                c.setFillColor(colors.black)

            except Exception as e:
                print(f"⚠️ Error dibujando QR: {e}")

    def _dibujar_iconos_pago(self, c, datos, width, height):
        """Dibuja íconos de métodos de pago aceptados"""
        payment_icons = [
            'https://cdn.simpleicons.org/visa/1A1F71',
            'https://cdn.simpleicons.org/mastercard/EB001B',
            'https://api.iconify.design/mdi/cash.svg?color=%23388E3C',
        ]

        x_start = 30
        y = 35
        icon_size = 20
        spacing = 30

        c.setFont(self.FONT_BOLD, 7)
        c.drawString(x_start, y + icon_size + 5, "Métodos de pago:")

        for i, icon_url in enumerate(payment_icons):
            icon_data = self._descargar_imagen(icon_url)
            if icon_data:
                try:
                    c.drawImage(
                        Image.open(icon_data),
                        x_start + (i * spacing),
                        y,
                        width=icon_size,
                        height=icon_size,
                        preserveAspectRatio=True,
                        mask='auto'
                    )
                except:
                    pass

    def _dibujar_pie_con_iconos(self, c, datos, width, height):
        """Dibuja pie de página con íconos de contacto"""
        y = 20
        icon_size = 10

        contactos = [
            ('phone', datos['emisor']['telefono'], 'https://api.iconify.design/mdi/phone.svg?color=%23666666'),
            ('email', datos['emisor']['email'], 'https://api.iconify.design/mdi/email.svg?color=%23666666'),
            ('web', datos['emisor'].get('web', 'www.empresa.com'), 'https://api.iconify.design/mdi/web.svg?color=%23666666'),
        ]

        x_start = width / 2 - 200
        spacing = 135

        for i, (tipo, texto, icon_url) in enumerate(contactos):
            x = x_start + (i * spacing)

            # Descargar y dibujar ícono
            icon_data = self._descargar_imagen(icon_url)
            if icon_data:
                try:
                    c.drawImage(
                        Image.open(icon_data),
                        x,
                        y - 2,
                        width=icon_size,
                        height=icon_size,
                        preserveAspectRatio=True,
                        mask='auto'
                    )
                except:
                    pass

            # Texto al lado del ícono
            c.setFont(self.FONT_NORMAL, 7)
            c.setFillColor(colors.grey)
            c.drawString(x + icon_size + 3, y, texto[:25])

        c.setFillColor(colors.black)

    def _dibujar_marca_agua(self, c, datos, width, height):
        """Dibuja marca de agua diagonal (opcional)"""
        c.saveState()

        # Configurar transparencia y rotación
        c.setFillColor(colors.grey, alpha=0.1)
        c.setFont(self.FONT_BOLD, 60)

        # Rotar canvas
        c.translate(width/2, height/2)
        c.rotate(45)

        # Dibujar texto
        c.drawCentredString(0, 0, "FACTURA FICTICIA")

        c.restoreState()

    def crear_factura(self, datos: Dict, filename: str = None) -> str:
        """
        Crea un PDF de factura con elementos visuales mejorados
        """
        # ... código existente ...

        # NUEVAS LLAMADAS (agregar en orden correcto)

        # 1. Marca de agua (primero, en el fondo)
        self._dibujar_marca_agua(c, datos, width, height)

        # 2. Logo de empresa (antes del encabezado)
        self._dibujar_logo_empresa(c, datos, width, height)

        # 3. Código existente...
        self._dibujar_encabezado(c, datos, width, height)
        # ... resto del código ...

        # 4. QR Code (antes del pie)
        self._dibujar_qr_code(c, datos, width, height)

        # 5. Íconos de pago (pie de página)
        self._dibujar_iconos_pago(c, datos, width, height)

        # 6. Pie con íconos de contacto
        self._dibujar_pie_con_iconos(c, datos, width, height)

        c.save()
        return filepath
```

---

## 🎨 Mejoras Opcionales Adicionales

### 1. **Banners Promocionales**

```python
def _dibujar_banner_promocional(self, c, datos, width, height):
    """Banner en la parte superior con promoción"""
    if random.random() < 0.3:  # 30% de facturas con banner
        banner_url = "https://placehold.co/540x40/1e88e5/ffffff/png?text=¡Descuento+10%+en+tu+próxima+compra!"
        banner_data = self._descargar_imagen(banner_url)

        if banner_data:
            c.drawImage(
                Image.open(banner_data),
                30,
                height - 20,
                width=540,
                height=40
            )
```

### 2. **Sellos de Certificación**

```python
def _dibujar_sellos(self, c, datos, width, height):
    """Sellos de certificación (ISO, SUNAT, etc.)"""
    sellos = [
        "https://api.dicebear.com/7.x/shapes/svg?seed=ISO9001&backgroundColor=1e88e5",
        "https://api.dicebear.com/7.x/shapes/svg?seed=SUNAT&backgroundColor=e53935",
    ]

    x = width - 100
    y = height - 250
    size = 40

    for i, sello_url in enumerate(sellos):
        sello_data = self._descargar_imagen(sello_url)
        if sello_data:
            c.drawImage(
                Image.open(sello_data),
                x,
                y - (i * 50),
                width=size,
                height=size
            )
```

### 3. **Colores de Marca por Empresa**

```python
EMPRESA_COLORES = {
    'TURISMO': '#1976D2',
    'CONSTRUCCION': '#F57C00',
    'HOTELES': '#7B1FA2',
    'SEGUROS': '#388E3C',
}

def _obtener_color_empresa(self, razon_social):
    """Obtiene color según rubro de empresa"""
    for keyword, color in EMPRESA_COLORES.items():
        if keyword in razon_social.upper():
            return colors.HexColor(color)
    return colors.HexColor('#2C3E50')  # Default
```

---

## 📊 Comparación de Opciones

| Característica | API Externa | Local | Generado |
|----------------|-------------|-------|----------|
| **Variedad** | Alta (miles) | Media | Baja |
| **Velocidad** | Lenta (red) | Rápida | Rápida |
| **Offline** | ❌ | ✅ | ✅ |
| **Realismo** | Alto | Alto | Medio |
| **Licencia** | Gratis | Depende | Libre |
| **Mantenimiento** | Bajo | Medio | Alto |

---

## 🚀 Recomendación Final

### **Estrategia Híbrida** (Lo mejor de ambos mundos)

1. **Logos de empresas:** UI Avatars API (online) + fallback local
2. **Códigos QR:** Generar localmente con qrcode (más rápido)
3. **Íconos de pago:** Simple Icons CDN (online)
4. **Íconos de contacto:** Iconify API (online)

### **Ventajas:**
- ✅ Balance entre velocidad y variedad
- ✅ Funciona offline (con degradación elegante)
- ✅ Sin costos de licencias
- ✅ Fácil de mantener

---

## 🎯 Plan de Implementación

### **Fase 1: Elementos Esenciales** (2-3 horas)
1. ✅ Logo de empresa (UI Avatars)
2. ✅ Código QR (qrcode local)
3. ✅ Modificar `_dibujar_encabezado()` para incluir logo

### **Fase 2: Íconos** (1-2 horas)
4. ✅ Íconos de pago (Simple Icons)
5. ✅ Íconos de contacto en pie (Iconify)
6. ✅ Modificar `_dibujar_pie()` con íconos

### **Fase 3: Extras Opcionales** (1 hora)
7. ⚪ Marca de agua "FACTURA FICTICIA"
8. ⚪ Sellos de certificación
9. ⚪ Banners promocionales

---

## 💡 Código de Ejemplo Completo

Ver archivo: `examples/factura_con_elementos_visuales.py`

---

¿Quieres que implemente alguna de estas opciones en el código?
