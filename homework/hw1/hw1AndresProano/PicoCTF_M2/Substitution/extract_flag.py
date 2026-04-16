#!/usr/bin/env python3
import re
import argparse
import string

ALPH = string.ascii_uppercase

def parse_key_26(s: str):
    """
    Espera 26 letras separadas por espacios, que representan el alfabeto en claro
    correspondiente a las letras cifradas A..Z (mapeo cipher->plain).
    Ejemplo:
      "U B W R G T N B Q E C F O H K V I D S Y M P L A D X"
    """
    parts = s.strip().split()
    if len(parts) != 26:
        raise ValueError("La clave debe contener exactamente 26 letras separadas por espacios.")
    out = []
    for p in parts:
        if len(p) != 1 or p.upper() not in ALPH:
            raise ValueError(f"Elemento inválido en clave: {p}")
        out.append(p.upper())
    return out

def decrypt(ciphertext: str, plain_map_az):
    """
    plain_map_az[i] = letra en claro para la letra cifrada ALPH[i].
    Mantiene caracteres no alfabéticos intactos.
    """
    table = {ALPH[i]: plain_map_az[i] for i in range(26)}
    out = []
    for ch in ciphertext:
        up = ch.upper()
        if up in table:
            dec = table[up]
            out.append(dec.lower() if ch.islower() else dec)
        else:
            out.append(ch)
    return "".join(out)

def extract_flag(text: str):
    m = re.search(r"picoCTF\{[^}]+\}", text)
    return m.group(0) if m else None

def main():
    ap = argparse.ArgumentParser(description="Decrypt a substitution cipher locally using a provided 26-letter key and extract picoCTF flag.")
    ap.add_argument("-i", "--input", required=True, help="ciphertext file (e.g., message.txt)")
    ap.add_argument("-o", "--output", default=None, help="optional: save decrypted text to this file")
    ap.add_argument("--key", default="U B W R G T N B Q E C F O H K V I D S Y M P L A D X",
                    help='26-letter key for A..Z (cipher->plain), space-separated.')
    args = ap.parse_args()

    ct = open(args.input, "r", encoding="utf-8", errors="ignore").read()
    plain_map = parse_key_26(args.key)
    pt = decrypt(ct, plain_map)

    flag = extract_flag(pt)
    if flag:
        print(flag)
    else:
        # Si no aparece como picoCTF{...}, intenta encontrar cualquier {...} largo
        candidates = re.findall(r"\{[A-Za-z0-9_]+\}", pt)
        if candidates:
            best = max(candidates, key=len)
            print(f"No se encontró picoCTF{{...}}. Mejor candidato: {best}")
        else:
            print("No se encontró ninguna bandera con llaves en el texto descifrado.")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(pt)

if __name__ == "__main__":
    main()