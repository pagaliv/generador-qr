#!/usr/bin/env python3
import argparse
import sys

import cv2
import qrcode


def leer_qr(ruta_imagen: str) -> str:
    imagen = cv2.imread(ruta_imagen)
    if imagen is None:
        raise FileNotFoundError(f"No se pudo abrir la imagen: {ruta_imagen}")

    detector = cv2.QRCodeDetector()
    datos, _, _ = detector.detectAndDecode(imagen)

    if not datos:
        raise ValueError("No se detectó ningún código QR en la imagen")

    return datos


def crear_qr(contenido: str, ruta_salida: str) -> None:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )
    qr.add_data(contenido)
    qr.make(fit=True)

    imagen = qr.make_image(fill_color="black", back_color="white")
    imagen.save(ruta_salida)


def convertir_a_eterno(ruta_entrada: str, ruta_salida: str) -> str:
    contenido = leer_qr(ruta_entrada)
    crear_qr(contenido, ruta_salida)
    return contenido


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Generador de códigos QR eternos: crea QR estáticos que codifican "
            "su contenido directamente, sin depender de enlaces o servicios "
            "que puedan caducar."
        )
    )
    subparsers = parser.add_subparsers(dest="comando", required=True)

    p_crear = subparsers.add_parser("crear", help="Crea un QR nuevo a partir de un texto o URL")
    p_crear.add_argument("contenido", help="Texto, URL u otro dato a codificar")
    p_crear.add_argument("-o", "--salida", default="qr_generado.png", help="Ruta del archivo PNG de salida")

    p_leer = subparsers.add_parser("leer", help="Lee y muestra el contenido de un QR existente")
    p_leer.add_argument("imagen", help="Ruta de la imagen del QR a leer")

    p_convertir = subparsers.add_parser(
        "convertir",
        help="Lee un QR existente y genera uno nuevo y eterno con el mismo contenido",
    )
    p_convertir.add_argument("imagen", help="Ruta de la imagen del QR de entrada")
    p_convertir.add_argument("-o", "--salida", default="qr_eterno.png", help="Ruta del archivo PNG de salida")

    args = parser.parse_args()

    try:
        if args.comando == "crear":
            crear_qr(args.contenido, args.salida)
            print(f"QR creado en: {args.salida}")
        elif args.comando == "leer":
            contenido = leer_qr(args.imagen)
            print(contenido)
        elif args.comando == "convertir":
            contenido = convertir_a_eterno(args.imagen, args.salida)
            print(f"Contenido detectado: {contenido}")
            print(f"QR eterno guardado en: {args.salida}")
    except (FileNotFoundError, ValueError) as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
