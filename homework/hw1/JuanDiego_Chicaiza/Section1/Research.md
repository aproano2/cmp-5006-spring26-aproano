# Research

En un **cifrado de sustitución simple (monoalfabético)**:

* Cada letra del texto plano se reemplaza **siempre por la misma letra**.
* Las frecuencias del idioma (por ejemplo, la alta frecuencia de la “E”) se mantienen visibles, solo “renombradas”.
* Esto permite romper el sistema mediante **análisis de frecuencia**.

Los siguientes sistemas superan esa debilidad de distintas maneras:

| Sistema      | Cómo supera la sustitución simple                              |
| ------------ | -------------------------------------------------------------- |
| **Vigenère** | Usa múltiples alfabetos (polialfabético)                       |
| **Hill**     | Cifra bloques usando álgebra lineal                            |
| **Playfair** | Cifra pares de letras (dígrafos)                               |
| **Enigma**   | Cambia el alfabeto en cada pulsación (mecánico + combinatorio) |

---

# Cifrado de Vigenère

## Mecanismo: La Tabula Recta

El cifrado de **Vigenère** es un sistema **polialfabético** basado en una tabla llamada **Tabula Recta**, que contiene 26 alfabetos desplazados.

### Procedimiento:

1. Se elige una **palabra clave**.
2. La clave se repite hasta igualar la longitud del mensaje.
3. Para cada posición:

   * Fila → letra de la clave
   * Columna → letra del texto plano
   * Intersección → letra cifrada

Ejemplo clásico:

```
Texto:   ATTACKATDAWN
Clave:   LEMONLEMONLE
Cifrado: LXFOPVEFRNHR
```

---

## ¿Por qué complica el análisis de frecuencia?

En sustitución simple:

```
E → siempre la misma letra
```

En Vigenère:

```
E → puede convertirse en muchas letras distintas
(depende de la letra de la clave en esa posición)
```

Eso distribuye la frecuencia de letras y elimina los picos evidentes.

Pero la clave se repite.
Si se descubre su longitud, el texto puede dividirse en columnas, y cada columna es un **César independiente**.

---

## Cómo se rompe: Método de Kasiski

El **examen de Kasiski**:

1. Busca secuencias repetidas en el texto cifrado.
2. Mide la distancia entre repeticiones.
3. Factoriza esas distancias.
4. El MCD sugiere la **longitud de la clave**.

Una vez conocida la longitud, se aplica análisis de frecuencia por columnas.

---

# Cifrado de Hill

El cifrado de **Hill (1929)** introduce álgebra lineal en criptografía.

## Base Matemática

1. Se asignan valores:

   ```
   A=0, B=1, ..., Z=25
   ```
2. Se elige una matriz clave (K) de tamaño (n \times n).
3. El texto se divide en bloques de tamaño (n).
4. Se aplica:

[
C \equiv K \cdot P \pmod{26}
]

---

## ¿Por qué es más avanzado?

* No cifra letras individuales.
* Cada letra cifrada depende de **todo el bloque**.
* Una misma letra puede cifrarse distinto según su contexto.

Esto rompe el análisis de frecuencia simple.

---

## Requisitos matemáticos para descifrar

La matriz debe ser **invertible módulo 26**.

Condición esencial:

[
\gcd(\det(K), 26) = 1
]

Como:

[
26 = 2 \times 13
]

El determinante no debe ser múltiplo de 2 ni de 13.

Si no es invertible → el mensaje no puede descifrarse.

---

# Cifrado Playfair

Playfair cifra **pares de letras (dígrafos)** en lugar de letras individuales.

---

## Construcción del cuadro 5×5

1. Elegir palabra clave.
2. Escribir letras sin repetir.
3. Completar con el resto del alfabeto.
4. Combinar I/J.

Ejemplo de preparación del texto:

* Separar en pares.
* Insertar X si hay letras repetidas.
* Rellenar con X si queda una sola.

---

## Reglas de cifrado

Para cada par:

1. **Misma fila** → mover a la derecha.
2. **Misma columna** → mover hacia abajo.
3. **Rectángulo** → intercambiar columnas.

---

## Uso histórico

* Inventado por Charles Wheatstone (1854).
* Adoptado por fuerzas británicas en WWI.
* Usado como respaldo en WWII.

### ¿Por qué era “field-ready”?

Solo requería papel y lápiz
Más seguro que sustitución simple
Rápido de usar
Adecuado para mensajes tácticos

---

# Máquina Enigma

La **Enigma** llevó la sustitución polialfabética al nivel mecánico.

---

## Lógica de los rotores

Cada rotor:

* Implementa un cableado interno (sustitución).
* Gira con cada pulsación.
* Cambia el alfabeto efectivo en cada letra.

Resultado:

La sustitución cambia **en cada pulsación**.

---

## El reflector

Funciona como espejo eléctrico:

* Devuelve la señal por otro camino.
* Hace que cifrado y descifrado sean el mismo proceso.

Consecuencia importante:

Ninguna letra puede cifrarse como sí misma.

Esto fue una debilidad explotada por criptoanalistas.

---

## Plugboard (Steckerbrett)

Intercambia pares de letras antes y después de los rotores.

Con 10 cables:

[
150,738,274,937,250
]

configuraciones posibles solo en el plugboard.

Esto multiplica (no suma) el espacio total de claves.

---

# Comparación

| Sistema  | Unidad criptográfica   | Defensa principal             | Debilidad clave                     |
| -------- | ---------------------- | ----------------------------- | ----------------------------------- |
| Vigenère | Letra (polialfabético) | Cambia alfabeto por posición  | Clave periódica                     |
| Hill     | Bloque (vector)        | Mezcla lineal modular         | Ataque por texto conocido           |
| Playfair | Dígrafo                | Aumenta espacio estadístico   | Análisis de pares                   |
| Enigma   | Letra (dinámica)       | Rotor + reflector + plugboard | Errores humanos + propiedad no self |

