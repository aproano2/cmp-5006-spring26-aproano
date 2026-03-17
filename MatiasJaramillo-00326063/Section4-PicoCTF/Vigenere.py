# El ejercicio de PicoCTF dice Can you decrypt this message?
# Decrypt this message using this key "CYLAB".

print("Primer approach con búsqueda sobre Tabla de Vigenere")

import string

letters = string.ascii_uppercase

vigenere_table = []

#Generamos la tabla de Vigenere
for i in range(26):
    row = letters[i:] + letters[:i]
    vigenere_table.append(list(row))

clave="CYLAB"
mensaje_encriptado="rgnoDVD{O0NU_WQ3_G1G3O3T3_A1AH3S_cc82272b}"
mensaje_desencriptado=""
contador_clave_idx=0

mensaje_encriptado=mensaje_encriptado.upper()

#Recorremos la tabla con la clave
for letra_encriptada in list(mensaje_encriptado):
    if(letra_encriptada not in letters):
        mensaje_desencriptado=mensaje_desencriptado+(letra_encriptada)
        continue
    letra_clave=clave[contador_clave_idx]
    fila_letra_clave=(list(vigenere_table[letters.index(letra_clave)]))
    letra_desencriptada=letters[fila_letra_clave.index(letra_encriptada)]
    mensaje_desencriptado=mensaje_desencriptado+(letra_desencriptada)
    contador_clave_idx = (contador_clave_idx + 1) % len(clave)

print(f"El mensaje desencriptado con el 1er approach es: {mensaje_desencriptado}")

print("Segundo approach más eficiente empleando aritmética modular")

letters = string.ascii_uppercase
clave = "CYLAB"
mensaje_encriptado = "rgnoDVD{O0NU_WQ3_G1G3O3T3_A1AH3S_f85729e7}"

mensaje_desencriptado = ""
contador_clave_idx = 0

mensaje_encriptado = mensaje_encriptado.upper()

for letra_encriptada in mensaje_encriptado:
    if letra_encriptada not in letters:
        mensaje_desencriptado += letra_encriptada
        continue
    letra_idx = letters.index(letra_encriptada)
    clave_idx = letters.index(clave[contador_clave_idx]) 
    # Desciframos usando módulo
    letra_desencriptada_idx = (letra_idx - clave_idx) % 26
    mensaje_desencriptado += letters[letra_desencriptada_idx]
    # Pasamos a la siguiente letra de la clave
    contador_clave_idx = (contador_clave_idx + 1) % len(clave)

print(f"El mensaje desencriptado con el 2do approach es: {mensaje_desencriptado}")
