import subprocess
import string

#Se obtiene texto oculto en imagen atbash.jpg con el uso de la herramienta stegseek como se observa en la captura de pantalla "UsoAtbashSobreImagen" usando wordlist de passwords rockyou.txt (extraido de https://www.kaggle.com/datasets/wjburns/common-password-list-rockyoutxt?resource=download) en caso la imagen este protegida por una clave
#La salida de stegseek esta en atbash.jpg.out

#Usamos el cifrado atbash para desencriptar la salida de atbash.jpg.out

with open("atbash.jpg.out", "r", encoding="utf-8") as f:
    texto_encriptado = f.read()

print(texto_encriptado)

texto_encriptado=texto_encriptado.lower()

#Como primer approach hacemos la traduccion directamente mediante la generación de un diccionario para cifrado Atbash

diccionario_atbash={}

for i in range (ord('z'),ord('a')-1,-1):

    diccionario_atbash[chr(i)]=chr(ord('z')-(i-ord('a')))

print(diccionario_atbash)

texto_desencriptado=""

for caracter in texto_encriptado:

    if(caracter in diccionario_atbash.keys()):
        texto_desencriptado=texto_desencriptado+diccionario_atbash[caracter]
    else:
        texto_desencriptado=texto_desencriptado+caracter

print("Texto desencriptado con primer approach:")
print(texto_desencriptado)

#Como segundo approach hacemos la traduccion directamente con la formula matematica de Atbash sin la necesidad de recurrir a un diccionario para hacerlo más directo

texto_desencriptado = ""

for c in texto_encriptado:
    if c.isalpha():
        if c.islower():
            texto_desencriptado += chr(ord('a') + ord('z') - ord(c))
        else:
            texto_desencriptado += chr(ord('A') + ord('Z') - ord(c))
    else:
        texto_desencriptado += c

print("Texto desencriptado con segundo approach:")
print(texto_desencriptado)
