
"""
rotation - Método 2: Brute force de los 25 shifts posibles
Prueba todos los shifts ROT1–ROT25 e identifica el correcto
buscando 'picoCTF{' en el resultado.
"""

import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
ENCRYPTED_FILE = os.path.join(BASE, "encrypted_rotation.txt")

def rot(text, shift):
    """Aplica Caesar cipher con el shift dado."""
    result = []
    for c in text:
        if c.islower():
            result.append(chr((ord(c) - ord('a') - shift) % 26 + ord('a')))
        elif c.isupper():
            result.append(chr((ord(c) - ord('A') - shift) % 26 + ord('A')))
        else:
            result.append(c)
    return ''.join(result)

def main():
    with open(ENCRYPTED_FILE) as f:
        ciphertext = f.read().strip()

    print(f"Texto cifrado: {ciphertext}")
    print(f"Probando los 25 shifts posibles...\n")

    for shift in range(1, 26):
        candidate = rot(ciphertext, shift)
        marker = "  FLAG ENCONTRADA" if "picoCTF{" in candidate else ""
        print(f"  ROT{shift:02d} (shift -{shift:02d}): {candidate}{marker}")

    # Mostrar resultado final
    for shift in range(1, 26):
        result = rot(ciphertext, shift)
        if "picoCTF{" in result:
            match = re.search(r'picoCTF\{[^}]+\}', result)
            print(f"\n[FLAG] {match.group()}  (shift={shift}, ROT{26-shift})")
            break

if __name__ == "__main__":
    main()
