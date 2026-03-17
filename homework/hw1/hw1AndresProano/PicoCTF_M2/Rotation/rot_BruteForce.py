cipher = "xqkwKBN{z0bib1wv_l3kzgxb3l_4k71n5j0}"
NEEDLE = "picoCTF{"

def caesar_decrypt(text, shift):
    out = []
    for c in text:
        if 'a' <= c <= 'z':
            out.append(chr((ord(c) - ord('a') - shift) % 26 + ord('a')))
        elif 'A' <= c <= 'Z':
            out.append(chr((ord(c) - ord('A') - shift) % 26 + ord('A')))
        else:
            out.append(c)
    return "".join(out)

for shift in range(26):
    candidate = caesar_decrypt(cipher, shift)
    if NEEDLE in candidate:
        print(f"[+] Shift correcto: {shift}")
        print(f"[+] Flag: {candidate}")
        break
else:
    print("[-] No se encontró una salida con el patrón esperado.")