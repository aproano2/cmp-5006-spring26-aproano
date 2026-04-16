# picoCTF - HideToSee

## Objetivo
Extraer información oculta dentro de una imagen (`pablo_atbash.jpg`) utilizando análisis forense local y descifrar el contenido hasta obtener la bandera final.

## Observaciones iniciales
- El archivo proporcionado es una imagen JPEG.
- No contiene texto visible a simple vista.
- Es probable que se haya utilizado esteganografía.

## Metodología

### 1. Verificación del archivo

Se confirmó el tipo de archivo:

```bash
file pablo_atbash.jpg
````

Resultado:

```
JPEG image data, JFIF standard 1.01
```

La imagen es válida y no presenta corrupción aparente.

### 2. Búsqueda de texto incrustado

Se intentó localizar texto visible:

```bash
strings pablo_atbash.jpg > output_strings.txt
grep -E "{.*}" output_strings.txt
```

No se encontró ninguna bandera en texto plano, lo que sugiere ocultamiento más avanzado.

### 3. Búsqueda de datos embebidos

Se utilizó:

```bash
binwalk pablo_atbash.jpg
```

No se detectaron archivos comprimidos ni datos agregados al final del archivo. Esto descarta técnicas simples como concatenación de ZIP.

### 4. Identificación de esteganografía

Se utilizó:

```bash
steghide info pablo_atbash.jpg
```

Resultado:

```
embedded file "encrypted.txt"
encrypted: rijndael-128, cbc
compressed: yes
```

Esto confirmó la presencia de un archivo oculto dentro de la imagen, cifrado con AES-128 (Rijndael en modo CBC).

### 5. Extracción del contenido

Se probó extracción con contraseña vacía:

```bash
steghide extract -sf pablo_atbash.jpg -p "" -xf output.txt -f
```

Contenido extraído:

```
krxlXGU{zgyzhs_xizxp_7142uwv9}
```

El texto presenta estructura de bandera pero no es legible aún.

## Segunda Capa: Cifrado Atbash

El contenido extraído está cifrado con Atbash, un cifrado monoalfabético donde el alfabeto se invierte:

* a ↔ z
* b ↔ y
* c ↔ x

Se implementó un script en Python para aplicar la transformación:

```python
def atbash(text):
    result = ""
    for c in text:
        if c.isalpha():
            if c.islower():
                result += chr(ord('z') - (ord(c) - ord('a')))
            else:
                result += chr(ord('Z') - (ord(c) - ord('A')))
        else:
            result += c
    return result

cipher = "krxlXGU{zgyzhs_xizxp_7142uwv9}"
print(atbash(cipher))
```

Resultado:

```
picoCTF{atbash_crack_7142fde9}
```

## Flag

picoCTF{atbash_crack_7142fde9}

## Diferencias respecto a soluciones web

* No se utilizó ninguna herramienta en línea.
* Se realizó análisis forense paso a paso.
* Se identificó manualmente el uso de steghide.
* Se implementó el descifrado Atbash localmente.
* El proceso es completamente reproducible.

## Conceptos aplicados

* Esteganografía (LSB)
* Steghide
* AES-128 (Rijndael-CBC)
* Cifrado clásico Atbash
* Análisis forense básico con herramientas Linux

## Conclusión

El reto combina técnicas de esteganografía y cifrado clásico en múltiples capas. Un enfoque sistemático permitió:

1. Identificar datos ocultos en una imagen.
2. Extraer un archivo cifrado.
3. Aplicar un segundo descifrado clásico.
4. Obtener la bandera final sin depender de herramientas automáticas en línea.

El análisis se realizó completamente en entorno Linux (WSL), utilizando herramientas forenses estándar.


