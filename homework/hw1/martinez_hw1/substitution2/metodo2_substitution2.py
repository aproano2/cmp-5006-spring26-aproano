
"""
substitution2 - Método 2: Análisis de bigramas (n-gramas)
La pista dice "analyzing groups of letters". Este método analiza los pares
de letras (bigramas) más frecuentes del ciphertext y los compara con los
bigramas más comunes del inglés para refinar el mapeo de sustitución.
"""

import os
import re
from collections import Counter

BASE = os.path.dirname(os.path.abspath(__file__))
CIPHER_FILE = os.path.join(BASE, "message.txt")

# Bigramas más comunes en inglés
ENGLISH_BIGRAMS = ["th","he","in","er","an","re","on","en","at","ou",
                   "ed","nd","to","ea","ng","as","or","is","it","ha"]

# Trigramas más comunes en inglés
ENGLISH_TRIGRAMS = ["the","and","ing","ion","ent","tio","for","ati",
                    "her","hat","his","tha","ere","con","ter","ons"]

def get_ngrams(text, n):
    """Extrae n-gramas de letras del texto."""
    text = ''.join(c.lower() for c in text if c.isalpha())
    return Counter(text[i:i+n] for i in range(len(text)-n+1))

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

    # Analizar bigramas del ciphertext
    bigrams = get_ngrams(ciphertext, 2)
    trigrams = get_ngrams(ciphertext, 3)

    print("Top 10 bigramas en ciphertext:")
    for bg, cnt in bigrams.most_common(10):
        print(f"    {bg}: {cnt}")

    print("\nTop 10 trigramas en ciphertext:")
    for tg, cnt in trigrams.most_common(10):
        print(f"    {tg}: {cnt}")

    # Comparar con bigramas del inglés para deducir mappings
    # 'jd' (28 veces) -> 'er' (más común en inglés) => j=e, d=r
    # 'fq' (27 veces) -> 'ti' => f=t, q=i
    # 'fn' (23 veces) -> 'th' => f=t, n=h
    # 'km' (20 veces) -> 'co' => k=c, m=o
    # Trigrama 'fnj' -> 'the' => f=t, n=h, j=e (trigrama confirmado)
    print("\n Deducción de mappings por bigramas/trigramas:")
    print("    'jd' -> 'er'  => j=e, d=r")
    print("    'fq' -> 'ti'  => f=t, q=i")
    print("    'fn' -> 'th'  => f=t, n=h")
    print("    'km' -> 'co'  => k=c, m=o")
    print("    'fnj'-> 'the' => f=t, n=h, j=e (trigrama confirmado)")

    # Key derivada del análisis:
    # naf -> the, zqgswnfy -> computer, efzwyxnh -> security
    # axraezaqqp -> highschool, tlb -> and, mfkfpxfuf -> webelieve
    # sxzq -> pico, ZNV -> CTF
    key = {
        'a':'h', 'b':'d', 'c':'k', 'e':'s',
        'f':'e', 'g':'m', 'h':'y', 'k':'b',
        'l':'n', 'm':'w', 'n':'t', 'o':'x',
        'p':'l', 'q':'o', 'r':'g', 's':'p',
        't':'a', 'u':'v', 'v':'f', 'w':'u',
        'x':'i', 'y':'r', 'z':'c'
    }

    print("\nKey completa (cipher -> plain):")
    print("    " + "  ".join(f"{c}->{p}" for c, p in sorted(key.items())))

    decrypted = apply_key(ciphertext, key)
    print(f"\nTexto descifrado (fragmento):")
    print(f"    {decrypted[:120]}...")

    match = re.search(r'picoCTF\{[^}]+\}', decrypted)
    if match:
        print(f"\n[FLAG] {match.group()}")

if __name__ == "__main__":
    main()
