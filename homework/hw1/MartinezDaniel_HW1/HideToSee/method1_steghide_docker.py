
"""
HideToSee - Método 1: steghide via Docker + Atbash decode
1. Usa steghide (via Docker) para extraer texto oculto en el JPEG
2. Aplica Atbash cipher para decodificar el texto extraído
"""

import subprocess
import os
import re

import os
BASE = os.path.dirname(os.path.abspath(__file__))
IMAGE_FILE = os.path.join(BASE, "atbash.jpg")

def extract_with_steghide(image_path):
    
    #Extrae datos ocultos del JPEG usando steghide con contraseña vacía.
    #Corre steghide dentro de un contenedor Docker Ubuntu.
    #para esto requerimos docker instalado y corriendo.
    
    abs_path = os.path.abspath(image_path)
    folder = os.path.dirname(abs_path)
    filename = os.path.basename(abs_path)

    cmd = [
        "docker", "run", "--rm",
        "-v", f"{folder}:/data",
        "ubuntu:22.04",
        "bash", "-c",
        f"apt-get update -qq && apt-get install -y steghide -qq 2>/dev/null && "
        f"cd /data && steghide extract -sf {filename} -p '' -f && cat encrypted.txt"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip()

def atbash_decode(text):
    
    #Aplica el cifrado Atbash: cada letra se sustituye por su opuesta en el alfabeto.

    
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
    print(f"[*] Extrayendo datos ocultos de: {IMAGE_FILE}")
    print(f"[*] Usando steghide via Docker (Ubuntu 22.04)...")
    output = extract_with_steghide(IMAGE_FILE)

    # Obtener la última línea (el texto cifrado)
    encrypted = output.strip().split('\n')[-1]
    print(f"[*] Texto extraído (Atbash): {encrypted}")

    flag = atbash_decode(encrypted)
    print(f"[*] Decodificado con Atbash: {flag}")

    if "picoCTF{" in flag:
        match = re.search(r'picoCTF\{[^}]+\}', flag)
        print(f"\n[FLAG] {match.group()}")

if __name__ == "__main__":
    main()
