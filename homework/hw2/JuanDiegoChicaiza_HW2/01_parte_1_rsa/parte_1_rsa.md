# Parte 1: Generación de claves RSA

**Estudiante:** Juan Diego Chicaiza, María Emilia Granda, Sebastián Encalada
**Tema:** Mecánica y seguridad de RSA

## 1. Cálculo manual con `p = 11` y `q = 13`

RSA parte de dos números primos y construye una clave pública y una privada relacionadas matemáticamente.

### Paso 1: calcular el módulo `n`

\[
n = p \cdot q = 11 \cdot 13 = 143
\]

El valor `n` aparece tanto en la clave pública como en la privada.

### Paso 2: calcular la función phi de Euler

\[
\varphi(n) = (p-1)(q-1) = 10 \cdot 12 = 120
\]

Este valor es crucial porque la clave privada se construye como el inverso multiplicativo del exponente público módulo `120`.

### Paso 3: elegir el exponente público `e`

Debe cumplirse:

\[
1 < e < \varphi(n), \qquad \gcd(e,\varphi(n)) = 1
\]

Elegimos:

\[
e = 7
\]

porque:

\[
\gcd(7,120)=1
\]

### Paso 4: calcular la clave privada `d`

Buscamos `d` tal que:

\[
e \cdot d \equiv 1 \pmod{\varphi(n)}
\]

Es decir:

\[
7d \equiv 1 \pmod{120}
\]

Usando el algoritmo extendido de Euclides:

\[
120 = 17 \cdot 7 + 1
\]

Entonces:

\[
1 = 120 - 17 \cdot 7
\]

Por lo tanto:

\[
d \equiv -17 \equiv 103 \pmod{120}
\]

Así:

\[
d = 103
\]

## Claves resultantes

- **Clave pública:** `(n,e) = (143,7)`
- **Clave privada:** `(n,d) = (143,103)`

## 1.1 Verificación mediante cifrado y descifrado

Tomemos un mensaje pequeño:

\[
m = 9
\]

El cifrado RSA es:

\[
c = m^e \bmod n = 9^7 \bmod 143
\]

Calculando por exponenciación modular:

- `9^2 = 81`
- `9^4 = 81^2 = 6561 \equiv 126 \pmod{143}`
- `9^7 = 9^4 \cdot 9^2 \cdot 9`

Entonces:

\[
126 \cdot 81 = 10206 \equiv 53 \pmod{143}
\]

y:

\[
53 \cdot 9 = 477 \equiv 48 \pmod{143}
\]

Por tanto:

\[
c = 48
\]

Ahora desciframos:

\[
m' = c^d \bmod n = 48^{103} \bmod 143
\]

En lugar de expandir una potencia enorme, verificamos el resultado módulo `11` y módulo `13`.

### Módulo 11

\[
48 \equiv 4 \pmod{11}
\]

\[
4^5 \equiv 1 \pmod{11}
\]

Como `103 = 20 \cdot 5 + 3`:

\[
4^{103} \equiv (4^5)^{20}\cdot 4^3 \equiv 1^{20}\cdot 64 \equiv 9 \pmod{11}
\]

### Módulo 13

\[
48 \equiv 9 \pmod{13}
\]

Como `103 \bmod 12 = 7`:

\[
9^{103} \equiv 9^7 \pmod{13}
\]

Y:

- `9^2 = 81 \equiv 3 \pmod{13}`
- `9^4 \equiv 3^2 = 9 \pmod{13}`
- `9^7 = 9^4 \cdot 9^2 \cdot 9 \equiv 9 \cdot 3 \cdot 9 = 243 \equiv 9 \pmod{13}`

Por lo tanto:

\[
48^{103} \equiv 9 \pmod{13}
\]

Como el resultado es `9` tanto módulo `11` como módulo `13`, el Teorema Chino del Resto implica:

\[
m' = 9
\]

Eso confirma que el par de claves funciona correctamente.

## 2. ¿Por qué es computacionalmente inviable encontrar `d` en un sistema RSA real de 2048 bits?

En un sistema RSA real, un atacante normalmente conoce solo:

- el módulo `n`
- el exponente público `e`

Para obtener `d`, necesita resolver:

\[
e \cdot d \equiv 1 \pmod{\lambda(n)}
\]

o, en la forma introductoria:

\[
e \cdot d \equiv 1 \pmod{\varphi(n)}
\]

Pero `lambda(n)` o `phi(n)` no pueden calcularse sin conocer los factores primos secretos de `n`, es decir, `p` y `q`.

### La dificultad central: factorizar `n`

La seguridad de RSA depende de que factorizar un módulo grande sea extremadamente difícil. En un sistema de 2048 bits:

1. `n` tiene aproximadamente 617 dígitos decimales.
2. No se conoce un algoritmo clásico de tiempo polinomial para factorizar enteros de ese tamaño.
3. Los mejores ataques públicos clásicos, como el **General Number Field Sieve**, siguen siendo demasiado costosos para módulos RSA bien generados de 2048 bits.
4. NIST todavía trata RSA-2048 como un tamaño con aproximadamente **112 bits de fortaleza de seguridad**, lo cual explica por qué sigue siendo un mínimo habitual en muchos estándares.

### Lo que esto significa realmente

No significa que RSA sea invulnerable. Significa algo más preciso:

> Si las claves fueron generadas correctamente y la implementación es sólida, recuperar `d` a partir de solo `(n,e)` es computacionalmente inviable con tecnología clásica conocida.

### Riesgos reales fuera de la factorización

Aunque factorizar el módulo sea impráctico, un atacante sí podría romper el sistema si ocurre alguno de estos problemas:

- generación débil de números aleatorios
- reutilización o mala elección de primos
- fugas por canales laterales como tiempo, caché, consumo eléctrico o inyección de fallos
- uso de padding inseguro o implementaciones legadas mal diseñadas

Por eso, en ingeniería de seguridad, la afirmación correcta no es simplemente "RSA es seguro", sino:

> RSA-2048 es seguro frente a la recuperación de la clave privada por factorización directa, siempre que la generación de claves, el almacenamiento y la implementación también sean seguros.

## Referencias

1. RFC 8017, *PKCS #1 v2.2: RSA Cryptography Specifications*.
2. NIST SP 800-57 Part 1 Rev. 5, *Recommendation for Key Management*.
