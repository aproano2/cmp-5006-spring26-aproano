# Rotation – picoCTF (Solución local)

## Objetivo
Descifrar el texto:

`xqkwKBN{z0bib1wv_l3kzgxb3l_4k71n5j0}`

hasta obtener una flag válida con formato `picoCTF{...}`.

## Análisis y elección del método
El nombre del reto (“rotation”) y el hint (“Sometimes rotation is right”) sugieren un cifrado de rotación tipo **Caesar / ROT-n**, donde cada letra se desplaza `n` posiciones en el alfabeto (módulo 26).  
Como el espacio de claves es pequeño (solo 26 desplazamientos posibles), se puede resolver de forma confiable con **fuerza bruta**.

## Método local (fuerza bruta ROT-0 a ROT-25)
Se implementó un script que prueba todos los desplazamientos (0–25) y muestra la salida.

Criterio para identificar la respuesta correcta:
- La salida debe contener el prefijo típico de picoCTF: `picoCTF{`

Al ejecutar el script, se observó:

`Shift 8: picoCTF{r0tat1on_d3crypt3d_4c71f5b0}`

## Resultado (Flag final)
`picoCTF{r0tat1on_d3crypt3d_4c71f5b0}`

## Nota técnica
Este ataque funciona porque:
- ROT-n tiene solo 26 claves posibles.
- Probarlas todas es rápido y garantiza encontrar el texto correcto cuando se conoce el formato esperado (aquí, `picoCTF{`).