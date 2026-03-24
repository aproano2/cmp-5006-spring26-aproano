# picoCTF - Vigenere (Classic Crypto)

## Objetivo
Descifrar un mensaje cifrado con el cifrado Vigenère utilizando la clave proporcionada `CYLAB`, de forma completamente local y reproducible.

## Observaciones iniciales
- El reto especifica explícitamente que el cifrado es Vigenère y entrega la clave.
- El ciphertext contiene letras, dígitos, guiones bajos y llaves (formato típico `picoCTF{...}`).
- En implementaciones clásicas, Vigenère opera sobre el alfabeto A–Z; caracteres no alfabéticos suelen preservarse.

## Hipótesis
1. El cifrado aplica Vigenère únicamente a letras (A–Z), ignorando dígitos, `_`, `{` y `}`.
2. La clave `CYLAB` se repite para cada letra cifrada (key stream), avanzando solo cuando se procesa una letra.

Estas hipótesis se validan si al descifrar aparece una cadena con el patrón `picoCTF{...}` y el texto resultante es coherente.

## Metodología
Vigenère es un cifrado polialfabético donde cada letra se desplaza según la letra correspondiente de la clave.

Representación:
- A=0, B=1, ..., Z=25
- Cifrado:    C = (P + K) mod 26
- Descifrado: P = (C - K) mod 26

Para mantener compatibilidad con el formato de flags:
- Se descifran solo letras.
- Se preservan los caracteres no alfabéticos.
- Se conserva el caso (mayúsculas/minúsculas) del ciphertext.

## Implementación local
Archivos:
- `message.txt`: ciphertext del reto.
- `vigenere_decrypt.py`: script local para descifrado Vigenère.
- `plaintext.txt`: salida del descifrado.

Ejecución:
```bash
python vigenere_decrypt.py -i message.txt -k CYLAB -o plaintext.txt
```

## Validación

Se valida buscando el patrón `picoCTF{...}` en el resultado. El script imprime la flag directamente si la detecta.

## Diferencias respecto a soluciones tipo web

* No se usó CyberChef ni herramientas en línea.
* El descifrado se implementó en Python con aritmética modular (mod 26) y reglas explícitas para el key stream.
* El proceso es reproducible: misma entrada + misma clave => misma salida.

## Flag

picoCTF{D0NT_US3_V1G3N3R3_C1PH3R_ae82272q}

