#!/usr/bin/env python3
import argparse
import string
import re

ALPH = string.ascii_uppercase

def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """
    Descifra Vigenère sobre A-Z.
    - Solo transforma letras (A-Z / a-z).
    - Mantiene dígitos, guiones bajos y llaves intactos.
    - Preserva mayúsculas/minúsculas del ciphertext.
    """
    key = "".join([c for c in key.upper() if c.isalpha()])
    if not key:
        raise ValueError("Key must contain at least one alphabetic character (A-Z).")

    out = []
    ki = 0  # índice del key stream (solo avanza cuando se procesa una letra)

    for ch in ciphertext:
        if ch.isalpha():
            k = key[ki % len(key)]
            shift = ALPH.index(k)

            if ch.isupper():
                idx = ALPH.index(ch)
                out.append(ALPH[(idx - shift) % 26])
            else:
                idx = ALPH.index(ch.upper())
                out.append(ALPH[(idx - shift) % 26].lower())

            ki += 1
        else:
            out.append(ch)

    return "".join(out)

def main():
    ap = argparse.ArgumentParser(description="Local Vigenère decrypt (A-Z only), preserves non-letters.")
    ap.add_argument("-i", "--input", required=True, help="ciphertext file")
    ap.add_argument("-k", "--key", required=True, help="Vigenère key (e.g., CYLAB)")
    ap.add_argument("-o", "--output", default=None, help="optional output file for plaintext")
    args = ap.parse_args()

    ct = open(args.input, "r", encoding="utf-8", errors="ignore").read().strip()
    pt = vigenere_decrypt(ct, args.key)

    m = re.search(r"picoCTF\{[^}]+\}", pt)
    if m:
        print(m.group(0))
    else:
        print(pt)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(pt + "\n")

if __name__ == "__main__":
    main()