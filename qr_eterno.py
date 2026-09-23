#!/usr/bin/env python3
"""Generador de QR eterno / Eternal QR generator.

Comandos disponibles en español e inglés (equivalentes):
Available commands in Spanish and English (equivalent):

    crear     / create
    leer      / read
    convertir / convert
"""
import argparse
import sys

import cv2
import qrcode


def read_qr(image_path: str) -> str:
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"No se pudo abrir la imagen / Could not open image: {image_path}")

    detector = cv2.QRCodeDetector()
    data, _, _ = detector.detectAndDecode(image)

    if not data:
        raise ValueError(
            "No se detectó ningún código QR en la imagen / No QR code was detected in the image"
        )

    return data


def create_qr(content: str, output_path: str) -> None:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(content)
    qr.make(fit=True)

    image = qr.make_image(fill_color="black", back_color="white")
    image.save("qr-gen/"+output_path)


def convert_to_eternal(input_path: str, output_path: str) -> str:
    content = read_qr(input_path)
    create_qr(content, output_path)
    return content


# Alias en español, mismas funciones / Spanish aliases, same functions
leer_qr = read_qr
crear_qr = create_qr
convertir_a_eterno = convert_to_eternal


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Generador de codigos QR eternos: crea QR estaticos que codifican su "
            "contenido directamente, sin depender de enlaces o servicios que puedan "
            "caducar.\n"
            "Eternal QR code generator: creates static QR codes that encode their "
            "content directly, without depending on links or services that can expire."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    p_create = subparsers.add_parser(
        "create",
        aliases=["crear"],
        help="Crea un QR nuevo a partir de un texto o URL / Create a new QR from text or a URL",
    )
    p_create.add_argument("content", help="Texto, URL u otro dato a codificar / Text, URL or other data to encode")
    p_create.add_argument(
        "-o", "--output", default="qr_generado.png",
        help="Ruta del archivo PNG de salida / Output PNG file path",
    )

    p_read = subparsers.add_parser(
        "read",
        aliases=["leer"],
        help="Lee y muestra el contenido de un QR existente / Read and print the content of an existing QR",
    )
    p_read.add_argument("image", help="Ruta de la imagen del QR a leer / Path to the QR image to read")

    p_convert = subparsers.add_parser(
        "convert",
        aliases=["convertir"],
        help=(
            "Lee un QR existente y genera uno nuevo y eterno con el mismo contenido / "
            "Read an existing QR and generate a new eternal one with the same content"
        ),
    )
    p_convert.add_argument("image", help="Ruta de la imagen del QR de entrada / Path to the input QR image")
    p_convert.add_argument(
        "-o", "--output", default="qr_eterno.png",
        help="Ruta del archivo PNG de salida / Output PNG file path",
    )

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    try:
        if args.command in ("create", "crear"):
            create_qr(args.content, args.output)
            print(f"QR creado en / QR created at: {args.output}")
        elif args.command in ("read", "leer"):
            content = read_qr(args.image)
            print(content)
        elif args.command in ("convert", "convertir"):
            content = convert_to_eternal(args.image, args.output)
            print(f"Contenido detectado / Detected content: {content}")
            print(f"QR eterno guardado en / Eternal QR saved at: {args.output}")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
