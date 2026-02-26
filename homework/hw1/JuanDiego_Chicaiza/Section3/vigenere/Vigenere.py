import string
from itertools import cycle

with open('cipher.txt', 'r') as f:
    ciphertext = f.read().strip()

key = "CYLAB"

# Method 1: Iterative Character Math
def decrypt_method1(text, key):
    decrypted = ""
    key_idx = 0
    for char in text:
        if char.isupper():
            shift = ord(key[key_idx % len(key)].upper()) - ord('A')
            decrypted += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            key_idx += 1
        elif char.islower():
            shift = ord(key[key_idx % len(key)].lower()) - ord('a') # using lower key shift
            # Wait, Vigenere shift is typically 0-25 based on 'A', regardless of case of text.
            # So shift = ord(key[key_idx % len(key)].upper()) - ord('A')
            shift = ord(key[key_idx % len(key)].upper()) - ord('A')
            decrypted += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            key_idx += 1
        else:
            decrypted += char
    return decrypted

# Method 2: Generator expression with cycle
def decrypt_method2(text, key):
    def decrypt_char(c, k):
        if c.isupper():
            shift = ord(k.upper()) - ord('A')
            return chr((ord(c) - ord('A') - shift) % 26 + ord('A'))
        elif c.islower():
            shift = ord(k.upper()) - ord('A')
            return chr((ord(c) - ord('a') - shift) % 26 + ord('a'))
        return c

    def key_generator(key):
        for k in cycle(key):
            yield k

    kg = key_generator(key)
    return ''.join(decrypt_char(c, next(kg) if c.isalpha() else '') for c in text)

print("Method 1 Output:", decrypt_method1(ciphertext, key))
print("Method 2 Output:", decrypt_method2(ciphertext, key))
