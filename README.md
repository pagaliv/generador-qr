# Generador de QR Eterno

Script en Python para leer un código QR existente y generar uno nuevo que **nunca caduca**.

## ¿Por qué "eterno"?

Muchos generadores de QR "gratuitos" en internet en realidad crean **QR dinámicos**: el código no contiene tu contenido directamente, sino una URL corta que apunta a un servidor del proveedor (por ejemplo `qr.provedor.com/abc123`). Ese servidor redirige al contenido real. El problema es que:

- Si el proveedor cierra el servicio, deja de funcionar la redirección o vence tu plan gratuito/de prueba, el QR **deja de funcionar**, aunque la imagen siga intacta.
- El proveedor puede ver y controlar cuántas veces se escanea, cuándo y desde dónde.

Este script hace lo contrario: **decodifica el QR original para extraer el contenido real** (texto, URL, etc.) y genera un **QR estático nuevo que incluye ese contenido directamente dentro del propio código**, sin pasar por ningún servidor intermedio. Mientras la imagen exista y sea legible, el QR funcionará siempre, sin fecha de caducidad ni dependencia de terceros.

## Instalación

Requiere Python 3.8+.

```bash
pip install -r requirements.txt
```

## Uso

El script expone tres comandos:

### 1. Convertir un QR existente en uno eterno

Lee el contenido de un QR (aunque sea uno "dinámico" de un servicio externo) y genera uno nuevo con ese mismo contenido embebido directamente:

```bash
python qr_eterno.py convertir mi_qr_viejo.png -o qr_eterno.png
```

### 2. Crear un QR nuevo desde texto o URL

```bash
python qr_eterno.py crear "https://ejemplo.com" -o qr_generado.png
```

### 3. Leer el contenido de un QR

Útil para comprobar qué está codificado realmente en una imagen:

```bash
python qr_eterno.py leer mi_qr.png
```

## Cómo funciona

1. **Lectura (`cv2.QRCodeDetector`)**: OpenCV analiza la imagen, localiza el patrón del QR y decodifica el contenido en texto plano.
2. **Generación (`qrcode`)**: Con ese contenido, se construye un nuevo código QR usando corrección de errores alta (`ERROR_CORRECT_H`), que tolera hasta un ~30% de daño/manchas en la imagen y sigue siendo legible.
3. El resultado es una imagen `.png` autocontenida: cualquier lector de QR puede escanearla sin conexión a internet ni redirecciones externas.

## Limitaciones

- Si el QR original ya es dinámico y su contenido real es simplemente una URL corta, el QR "eterno" seguirá apuntando a esa misma URL corta. El script no puede saber qué hay detrás de esa URL a menos que la sigas tú mismo y uses ese contenido final como entrada del comando `crear`.
- La "eternidad" se refiere a que el propio código QR no expira ni depende de un servicio externo. No garantiza que un enlace web codificado dentro de él siga existiendo para siempre.
