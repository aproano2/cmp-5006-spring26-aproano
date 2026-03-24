
"""
Vigenere - Método 2: Tabula Recta (Cuadrado de Vigenère)
Descifra usando la tabla de Vigenère (26x26) como lo haría un criptógrafo
clásico: busca la columna del carácter cifrado en la fila de la clave
para encontrar el carácter en texto claro.
"""

import os
import re
import string

BASE = os.path.dirname(os.path.abspath(__file__))
CIPHER_FILE = os.path.join(BASE, "cipher.txt")
KEY = "CYLAB"

def build_tabula_recta():
    """
    Construye la Tabula Recta (cuadrado de Vigenère) 26x26.
    tabla[i][j] = letra cifrada cuando plain=j y key=i
    """
    alpha = string.ascii_uppercase
    tabla = {}
    for i, k in enumerate(alpha):
        tabla[k] = {}
        for j, p in enumerate(alpha):
            cipher_letter = alpha[(i + j) % 26]
            tabla[k][cipher_letter] = p
    return tabla

def vigenere_decrypt_tabula(ciphertext, key, tabla):
    """
    Descifra usando la tabula recta:
    dado el carácter de clave (fila) y el carácter cifrado (columna),
    busca el texto claro en la tabla.
    """
    key = key.upper()
    result = []
    key_idx = 0

    for c in ciphertext:
        if c.isalpha():
            k = key[key_idx % len(key)]
            if c.isupper():
                plain = tabla[k][c]
            else:
                plain = tabla[k][c.upper()].lower()
            result.append(plain)
            key_idx += 1
        else:
            result.append(c)

    return ''.join(result)

def print_tabula_sample(tabla):

    #Muestra un fragmento de la Tabula Recta para las letras de la clave
    print("Fragmento de la Tabula Recta (filas de la clave CYLAB):")
    header = "    Key | " + " ".join(string.ascii_uppercase[:10]) + " ..."
    print(header)
    print("    " + "-" * 45)
    for k in KEY:
        row = " ".join(tabla[k][c] for c in string.ascii_uppercase[:10])
        print(f"     {k}  | {row} ...")

def main():
    with open(CIPHER_FILE) as f:
        ciphertext = f.read().strip()

    tabla = build_tabula_recta()
    print_tabula_sample(tabla)

    print(f"\nCiphertext: {ciphertext}")
    print(f"Key:        {KEY}")

    plaintext = vigenere_decrypt_tabula(ciphertext, KEY, tabla)
    print(f"Plaintext:  {plaintext}")

    match = re.search(r'picoCTF\{[^}]+\}', plaintext)
    if match:
        print(f"\n[FLAG] {match.group()}")

if __name__ == "__main__":
    main()
