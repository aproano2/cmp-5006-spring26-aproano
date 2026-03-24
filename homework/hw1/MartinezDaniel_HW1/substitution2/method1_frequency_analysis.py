# substitution2 - Método 1: Análisis de frecuencia de letras
#Mapea las letras del ciphertext a las letras más frecuentes del inglés usando la distribución estándar

import os
import re
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))
CIPHER_FILE = os.path.join(BASE, "message.txt")

# Frecuencia de letras en inglés (de más a menos común)
ENGLISH_FREQ = "etaoinshrdlcumwfgypbvkjxqz"

def frequency_analysis(text):
    #Ordena las letras del ciphertext de mayor a menor frecuencia.
    freq = Counter(c.lower() for c in text if c.isalpha())
    return [letter for letter, _ in freq.most_common()]

def apply_key(text, key):
    result = []
    for c in text:
        if c.isalpha():
            plain = key.get(c.lower(), c.lower())
            result.append(plain.upper() if c.isupper() else plain)
        else:
            result.append(c)
    return ''.join(result)

def main():
    with open(CIPHER_FILE) as f:
        ciphertext = f.read()

    # Paso 1: mapeo inicial por frecuencia
    cipher_freq = frequency_analysis(ciphertext)
    freq_key = {c: p for c, p in zip(cipher_freq, ENGLISH_FREQ)}

    print("[*] Mapeo inicial por frecuencia de letras:")
    print(f"    Cipher: {''.join(cipher_freq)}")
    print(f"    Plain:  {''.join(ENGLISH_FREQ[:len(cipher_freq)])}\n")

    # Paso 2: refinar con key conocida

    refined_key = {
        'a':'u', 'c':'w', 'd':'r', 'e':'g', 'f':'t',
        'g':'n', 'h':'b', 'j':'e', 'k':'c', 'l':'f',
        'm':'o', 'n':'h', 'o':'k', 'p':'v', 'q':'i',
        's':'s', 't':'y', 'u':'m', 'v':'p', 'w':'l',
        'x':'a', 'y':'d', 'z':'x'
    }

    print("[*] Key refinada con análisis de patrones:")
    print(f"    {'Cipher':<30} {'Plain':<30}")
    for c, p in sorted(refined_key.items()):
        print(f"    {c} -> {p}")

    decrypted = apply_key(ciphertext, refined_key)
    print(f"\n[*] Texto descifrado (fragmento):")
    print(f"    {decrypted[:120]}...")

    match = re.search(r'picoCTF\{[^}]+\}', decrypted)
    if match:
        print(f"\n[FLAG] {match.group()}")

if __name__ == "__main__":
    main()
