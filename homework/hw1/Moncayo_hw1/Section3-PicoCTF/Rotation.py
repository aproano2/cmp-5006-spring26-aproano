#Primer approach que usamos se baso en generar funcion de rotacion y luego por brute force probar diferentes rotaciones hasta obtener texto desencriptado

print("Primer approach con testing de varias rotaciones bajo implementacion matematica de la rotacion")

def rotation(text, rotation):
    result = ""
    text = str(text)

    for c in text:
        if c.isalpha():
            
            base = ord('A') if c.isupper() else ord('a')
            # Aplicamos rotación con formula matematica
            shifted = (ord(c) - base + rotation) % 26 + base
            result += chr(shifted)
        else:
            # Mantenemos números y símbolos igual
            result += c

    return result

cypher_text= "xqkwKBN{z0bib1wv_l3kzgxb3l_949in1i1}"

for i in range (1,26):
    print(rotation(cypher_text,i))

print("Segundo approach con creacion de alfabeto rotado y traduccion con dicho alfabeto")

import string

def rotation(text, shift):
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase

    rotated_lower = lower[shift:] + lower[:shift]
    rotated_upper = upper[shift:] + upper[:shift]

    translation_table = str.maketrans(
        lower + upper,
        rotated_lower + rotated_upper
    )

    return text.translate(translation_table)

cypher_text = "xqkwKBN{z0bib1wv_l3kzgxb3l_949in1i1}"

for i in range(1, 26):
    print(rotation(cypher_text, i))