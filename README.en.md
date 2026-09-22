# Eternal QR Generator

*Léelo en [español](README.md).*

A Python script that reads an existing QR code and generates a new one that **never expires**.

## Why "eternal"?

Many "free" QR generators on the internet actually create **dynamic QR codes**: the code doesn't contain your content directly, but a short URL pointing to the provider's server (e.g. `qr.provider.com/abc123`). That server redirects to the real content. The problem is:

- If the provider shuts down the service, the redirect breaks, or your free/trial plan expires, the QR code **stops working**, even though the image itself is untouched.
- The provider can see and control how often it's scanned, when, and from where.

This script does the opposite: it **decodes the original QR to extract the real content** (text, URL, etc.) and generates a **new static QR that embeds that content directly inside the code itself**, with no intermediate server involved. As long as the image exists and is readable, the QR will always work — no expiration date, no dependency on third parties.

## Installation

Requires Python 3.8 or later.

### Linux / macOS

```bash
git clone <this-repository-url>
cd generador-qr
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Windows

With **PowerShell** or **Command Prompt (cmd)**:

```powershell
git clone <this-repository-url>
cd generador-qr
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

> Note: on Windows the command is usually `python`, not `python3`. If you don't have Python installed, download it from [python.org](https://www.python.org/downloads/) and check "Add Python to PATH" during setup.

## Usage

The script accepts commands in **either English or Spanish** interchangeably (`create`/`crear`, `read`/`leer`, `convert`/`convertir`).

### 1. Convert an existing QR into an eternal one

Reads the content of a QR code (even a "dynamic" one from an external service) and generates a new one with that same content embedded directly:

```bash
# Linux / macOS
python3 qr_eterno.py convert my_old_qr.png -o eternal_qr.png

# Windows
python qr_eterno.py convert my_old_qr.png -o eternal_qr.png
```

### 2. Create a new QR from text or a URL

```bash
# Linux / macOS
python3 qr_eterno.py create "https://example.com" -o generated_qr.png

# Windows
python qr_eterno.py create "https://example.com" -o generated_qr.png
```

### 3. Read the content of a QR

Useful for checking what's actually encoded in an image:

```bash
# Linux / macOS
python3 qr_eterno.py read my_qr.png

# Windows
python qr_eterno.py read my_qr.png
```

## How it works

1. **Reading (`cv2.QRCodeDetector`)**: OpenCV analyzes the image, locates the QR pattern, and decodes the content into plain text.
2. **Generation (`qrcode`)**: With that content, a new QR code is built using high error correction (`ERROR_CORRECT_H`), which tolerates up to ~30% of damage/smudging on the image and remains readable.
3. The result is a self-contained `.png` image: any QR reader can scan it without an internet connection or external redirects.

## Limitations

- If the original QR is already dynamic and its real content is just a short URL, the "eternal" QR will still point to that same short URL. The script can't know what's behind that URL unless you follow it yourself and use that final content as input to the `create` command.
- "Eternal" refers to the QR code itself not expiring or depending on an external service. It does not guarantee that a web link encoded inside it will keep existing forever.
