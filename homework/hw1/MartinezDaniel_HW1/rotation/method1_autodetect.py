

#rotation - Método 1: Autodetección del shift


import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
ENCRYPTED_FILE = os.path.join(BASE, "encrypted.txt")

def rot(text, shift):
    #Aplica Caesar cipher con el shift dado. Números y símbolos no cambian.
    result = []
    for c in text:
        if c.islower():
            result.append(chr((ord(c) - ord('a') - shift) % 26 + ord('a')))
        elif c.isupper():
            result.append(chr((ord(c) - ord('A') - shift) % 26 + ord('A')))
        else:
            result.append(c)
    return ''.join(result)

def detect_shift(ciphertext):
    
    # Detecta el shift comparando la primera letra del texto cifradocon p
    first_letter = next(c for c in ciphertext if c.isalpha())
    return (ord(first_letter.lower()) - ord('p')) % 26

def main():
    with open(ENCRYPTED_FILE) as f:
        ciphertext = f.read().strip()

    print(f"[*] Texto cifrado: {ciphertext}")

    shift = detect_shift(ciphertext)
    print(f"[*] Shift detectado: {shift} (ROT{26 - shift})")

    flag = rot(ciphertext, shift)
    print(f"[*] Descifrado:    {flag}")

    if "picoCTF{" in flag:
        match = re.search(r'picoCTF\{[^}]+\}', flag)
        print(f"\n[FLAG] {match.group()}")

if __name__ == "__main__":
    main()
