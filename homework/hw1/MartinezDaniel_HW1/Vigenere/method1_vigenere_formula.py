
#Vigenere - Método 1: Fórmula matemática
#Descifra aplicando la fórmula directa del cifrado Vigenere plain = (cipher - key_shift) mod 26
#La clave 'CYLAB' se cicla solo sobre caracteres alfabéticos.

import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
CIPHER_FILE = os.path.join(BASE, "cipher.txt")
KEY = "CYLAB"

def vigenere_decrypt(ciphertext, key):

    key = key.upper()
    result = []
    key_idx = 0

    for c in ciphertext:
        if c.isalpha():
            shift = ord(key[key_idx % len(key)]) - ord('A')
            if c.isupper():
                plain = chr((ord(c) - ord('A') - shift) % 26 + ord('A'))
            else:
                plain = chr((ord(c) - ord('a') - shift) % 26 + ord('a'))
            result.append(plain)
            key_idx += 1
        else:
            result.append(c)

    return ''.join(result)

def main():
    with open(CIPHER_FILE) as f:
        ciphertext = f.read().strip()

    print(f"[*] Ciphertext: {ciphertext}")
    print(f"[*] Key:        {KEY}")
    print()

    # Mostrar cómo funciona el descifrado carácter por carácter (primeras letras)
    print("[*] Proceso de descifrado (primeras 7 letras):")
    key_idx = 0
    for c in ciphertext:
        if c.isalpha() and key_idx < 7:
            k = KEY[key_idx % len(KEY)]
            shift = ord(k) - ord('A')
            base = ord('A') if c.isupper() else ord('a')
            plain = chr((ord(c) - base - shift) % 26 + base)
            print(f"    '{c}' - key='{k}'(shift={shift}) -> '{plain}'")
            key_idx += 1

    plaintext = vigenere_decrypt(ciphertext, KEY)
    print(f"\n[*] Plaintext: {plaintext}")

    match = re.search(r'picoCTF\{[^}]+\}', plaintext)
    if match:
        print(f"\n[FLAG] {match.group()}")

if __name__ == "__main__":
    main()
