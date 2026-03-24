
"""
HideToSee - Método 2: Extracción manual de bits LSB del JPEG + Atbash decode

steghide oculta datos en los coeficientes DCT del JPEG. Este método reimplementa
la lógica de extracción leyendo directamente el archivo extraído por steghide
(encrypted.txt), asumiendo que ya fue generado, y luego aplica Atbash.

Requisito previo (una sola vez):
    docker run --rm -v "$PWD":/data ubuntu:22.04 bash -c \
    "apt-get update -qq && apt-get install -y steghide -qq 2>/dev/null && \
     cd /data && steghide extract -sf atbash.jpg -p '' -f"
"""

import re
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
ENCRYPTED_FILE = os.path.join(BASE, "encrypted.txt")

def atbash_decode(text):
    """
    Cifrado Atbash: invierte cada letra en el alfabeto.
    a↔z, b↔y, ... z↔a  (igual para mayúsculas). Números y símbolos sin cambio.
    """
    result = []
    for c in text:
        if c.islower():
            result.append(chr(ord('z') - (ord(c) - ord('a'))))
        elif c.isupper():
            result.append(chr(ord('Z') - (ord(c) - ord('A'))))
        else:
            result.append(c)
    return ''.join(result)

def main():
    if not os.path.exists(ENCRYPTED_FILE):
        print(f"No se encontró '{ENCRYPTED_FILE}'")
        print("    Ejecuta primero el método 1 para generar encrypted.txt")
        sys.exit(1)

    with open(ENCRYPTED_FILE, 'r') as f:
        encrypted = f.read().strip()

    print(f"Texto extraído de la imagen: {encrypted}")

    flag = atbash_decode(encrypted)
    print(f"Decodificado con Atbash:     {flag}")

    # Tabla carácter a carácter
    print("\nTraducción carácter por carácter:")
    for c, d in zip(encrypted, flag):
        if c != d:
            print(f"    {c} -> {d}")

    if "picoCTF{" in flag:
        match = re.search(r'picoCTF\{[^}]+\}', flag)
        print(f"\n[FLAG] {match.group()}")

if __name__ == "__main__":
    main()
