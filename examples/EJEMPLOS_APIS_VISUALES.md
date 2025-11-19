# 🎨 Ejemplos Prácticos de APIs Visuales

Aquí puedes **probar las URLs directamente en tu navegador** para ver los resultados.

---

## 🏢 Logos de Empresas

### UI Avatars
Crea logos con las iniciales de la empresa:

```
https://ui-avatars.com/api/?name=TURISMO+DIAS+SA&size=200&background=1976D2&color=fff&bold=true
```
👉 **Prueba esto:** Abre el link anterior en tu navegador

**Variaciones:**
```
# Fondo aleatorio
https://ui-avatars.com/api/?name=HOTEL+COSTA+DEL+SOL&size=200&background=random&color=fff&bold=true

# Fondo rojo
https://ui-avatars.com/api/?name=INMOBILIARIA+MASARIS&size=200&background=E53935&color=fff&bold=true

# Fondo verde (seguros)
https://ui-avatars.com/api/?name=SEGUROS+PACIFICO&size=200&background=388E3C&color=fff&bold=true

# Redondeado
https://ui-avatars.com/api/?name=CONSTRUCCIONES+SAC&size=200&background=F57C00&color=fff&bold=true&rounded=true
```

### DiceBear Avatars
Logos con diferentes estilos:

```
# Estilo "initials" (iniciales elegantes)
https://api.dicebear.com/7.x/initials/svg?seed=TurismoSA&backgroundColor=1e88e5

# Estilo "shapes" (formas geométricas)
https://api.dicebear.com/7.x/shapes/svg?seed=HotelCostaSol&backgroundColor=7b1fa2

# Estilo "thumbs" (iconos simples)
https://api.dicebear.com/7.x/thumbs/svg?seed=InmobiliariaMasaris&backgroundColor=e53935

# Estilo "identicon" (patrón único)
https://api.dicebear.com/7.x/identicon/svg?seed=SegurosDelPeru&backgroundColor=388e3c
```

### Boring Avatars
Diseños minimalistas:

```
# Estilo "beam"
https://source.boringavatars.com/beam/200/TurismoDias?colors=264653,2a9d8f,e76f51,f4a261,e9c46a

# Estilo "bauhaus"
https://source.boringavatars.com/bauhaus/200/HotelCostaSol?colors=264653,2a9d8f,e76f51,f4a261,e9c46a

# Estilo "ring"
https://source.boringavatars.com/ring/200/InmobiliariaMasaris?colors=264653,2a9d8f,e76f51,f4a261,e9c46a

# Estilo "sunset"
https://source.boringavatars.com/sunset/200/SegurosPacifico?colors=264653,2a9d8f,e76f51,f4a261,e9c46a
```

---

## 📱 Códigos QR

### GoQR.me API

```
# QR básico
https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=20438637380-03-F001-00000123

# QR grande
https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=20438637380|03|F001|00000123

# QR con formato SUNAT completo
https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=20438637380|03|F596|23196|20231113|110.00
```

**Formato SUNAT:**
```
RUC | TipoDoc | Serie | Numero | FechaYYYYMMDD | Total
20438637380 | 03 | F596 | 23196 | 20231113 | 110.00
```

---

## 💳 Íconos de Métodos de Pago

### Simple Icons (Logos de marcas)

```
# Visa (azul oficial)
https://cdn.simpleicons.org/visa/1A1F71

# Mastercard (rojo/naranja oficial)
https://cdn.simpleicons.org/mastercard/EB001B

# American Express (azul oficial)
https://cdn.simpleicons.org/americanexpress/006FCF

# PayPal
https://cdn.simpleicons.org/paypal/00457C

# Personalizado (negro)
https://cdn.simpleicons.org/visa/000000

# Personalizado (gris)
https://cdn.simpleicons.org/mastercard/666666
```

### Iconify (Íconos genéricos)

```
# Efectivo
https://api.iconify.design/mdi/cash.svg?color=%23388E3C&width=32

# Tarjeta de crédito
https://api.iconify.design/mdi/credit-card.svg?color=%23000000&width=32

# Billetera
https://api.iconify.design/mdi/wallet.svg?color=%23F57C00&width=32

# Banco
https://api.iconify.design/mdi/bank.svg?color=%231976D2&width=32
```

---

## 📞 Íconos de Contacto

```
# Teléfono (gris)
https://api.iconify.design/mdi/phone.svg?color=%23666666&width=24

# Email (gris)
https://api.iconify.design/mdi/email.svg?color=%23666666&width=24

# Sitio web (gris)
https://api.iconify.design/mdi/web.svg?color=%23666666&width=24

# Ubicación (gris)
https://api.iconify.design/mdi/map-marker.svg?color=%23666666&width=24

# WhatsApp (verde)
https://api.iconify.design/mdi/whatsapp.svg?color=%2325D366&width=24

# Facebook (azul)
https://api.iconify.design/mdi/facebook.svg?color=%231877F2&width=24
```

---

## 🎯 Placeholders y Banners

### Placehold.co

```
# Banner promocional básico
https://placehold.co/600x80/1e88e5/ffffff/png?text=DESCUENTO+10%25

# Banner con colores personalizados
https://placehold.co/600x80/e53935/ffffff/png?text=¡OFERTA+ESPECIAL!

# Imagen de fondo para header
https://placehold.co/800x200/2c3e50/ffffff/png?text=TURISMO+DIAS+S.A.

# Sello de garantía
https://placehold.co/100x100/388e3c/ffffff/png?text=ISO+9001
```

---

## 🎨 Tabla Comparativa de Servicios

| Servicio | Tipo | Formato | Personalización | Límites |
|----------|------|---------|-----------------|---------|
| **UI Avatars** | Logos texto | PNG | Alta | Ilimitado |
| **DiceBear** | Logos gráficos | SVG/PNG | Media | Ilimitado |
| **Boring Avatars** | Logos abstractos | SVG | Media | Ilimitado |
| **GoQR.me** | QR codes | PNG/SVG | Baja | Ilimitado |
| **Simple Icons** | Logos marcas | SVG | Baja | Ilimitado |
| **Iconify** | Íconos | SVG | Alta | Ilimitado |
| **Placehold.co** | Placeholders | PNG/SVG/WebP | Alta | Ilimitado |

---

## 🚀 Prueba Rápida en Python

```python
import requests
from PIL import Image
from io import BytesIO

# Descargar logo
url = "https://ui-avatars.com/api/?name=TURISMO+DIAS&size=200&background=1976D2&color=fff&bold=true"
response = requests.get(url)
img = Image.open(BytesIO(response.content))
img.show()  # Muestra la imagen

# Guardar localmente
img.save("logo_ejemplo.png")
print("✅ Logo guardado!")
```

---

## 🎯 Recomendaciones por Elemento

### Para Logos de Empresas:
1. **Primera opción:** UI Avatars (más realista, texto claro)
2. **Segunda opción:** DiceBear initials (elegante)
3. **Tercera opción:** Boring Avatars beam (moderno)

### Para Códigos QR:
1. **Recomendado:** Generar localmente con `qrcode` (más rápido)
2. **Alternativa:** GoQR.me API (si no quieres instalar librerías)

### Para Íconos de Pago:
1. **Logos de marcas:** Simple Icons (oficiales)
2. **Íconos genéricos:** Iconify mdi (Material Design)

### Para Íconos de Contacto:
1. **Única opción:** Iconify (mejor variedad)

---

## 💡 Tips de Uso

### 1. Caché de Imágenes
Descarga las imágenes una vez y guárdalas:
```python
image_cache = {}

def get_cached_image(url):
    if url not in image_cache:
        response = requests.get(url, timeout=3)
        image_cache[url] = BytesIO(response.content)
    return image_cache[url]
```

### 2. Fallback para Offline
```python
def download_with_fallback(url, fallback_path=None):
    try:
        response = requests.get(url, timeout=3)
        return BytesIO(response.content)
    except:
        if fallback_path and os.path.exists(fallback_path):
            return open(fallback_path, 'rb')
        return None
```

### 3. Colores Según Tipo de Empresa
```python
EMPRESA_COLORS = {
    'TURISMO': '1976D2',      # Azul
    'HOTEL': '7B1FA2',        # Púrpura
    'CONSTRUCCION': 'F57C00', # Naranja
    'SEGURO': '388E3C',       # Verde
    'INMOBILIARIA': 'E53935', # Rojo
    'RESTAURANTE': 'D84315',  # Rojo oscuro
    'TRANSPORTE': '0277BD',   # Azul claro
}
```

---

## 🔗 Enlaces Útiles

- **UI Avatars Docs:** https://ui-avatars.com/
- **DiceBear Docs:** https://www.dicebear.com/
- **Iconify Browse:** https://icon-sets.iconify.design/
- **Simple Icons Search:** https://simpleicons.org/
- **QR Code Generator (Python):** https://pypi.org/project/qrcode/

---

## ✅ Checklist de Implementación

```
□ Instalar dependencias (requests, pillow, qrcode)
□ Probar URLs de logos en el navegador
□ Probar generar QR localmente
□ Implementar función de descarga con caché
□ Implementar función de fallback
□ Agregar logos al PDF
□ Agregar QR al PDF
□ Agregar íconos de pago
□ Agregar íconos de contacto
□ Testear con y sin internet
```

---

¡Listo! Ahora tienes todo lo necesario para agregar elementos visuales realistas a tus facturas. 🎉
