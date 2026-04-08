# Parte 1: Generación de Claves RSA (La Mecánica)

## 1. Cálculo Manual (p = 11, q = 13)

### Paso 1: Calcular n y φ(n)

**Módulo público n:**
```
n = p × q = 11 × 13 = 143
```

**Función totiente de Euler φ(n):**
```
φ(n) = (p - 1)(q - 1) = (11 - 1)(13 - 1) = 10 × 12 = 120
```

---

### Paso 2: Elegir e (Exponente de Clave Pública)

e debe cumplir dos condiciones: **1 < e < 120** y **gcd(e, φ(n)) = 1** (e y φ(n) deben ser coprimos).

Candidato: **e = 7**. Verificación usando el Algoritmo de Euclides:

```
gcd(7, 120):
  120 = 17 × 7 + 1
    7 =  7 × 1 + 0
             ↑
         gcd = 1
```

El residuo llega a 0 después de que el residuo anterior fue 1, por lo que **gcd(7, 120) = 1**. La condición se cumple y **e = 7** es válido.

---

### Paso 3: Calcular d (Exponente de Clave Privada)

d es el inverso multiplicativo de e módulo φ(n), es decir, necesitamos:

```
d × 7 ≡ 1 (mod 120)
```

Se calcula usando el **Algoritmo de Euclides Extendido**, que expresa el gcd como combinación lineal de los dos números:

```
De la división anterior:
  1 = 120 - 17 × 7

Reescribiendo:
  1 ≡ -17 × 7 (mod 120)

Por lo tanto:
  d ≡ -17 (mod 120)
  d = 120 - 17 = 103
```

**Verificación:**
```
7 × 103 = 721
721 ÷ 120 = 6, con residuo 1   →   721 = 6 × 120 + 1
Por lo tanto: 7 × 103 ≡ 1 (mod 120) 
```

---

### Claves Generadas

| Clave | Valor |
|:---|:---|
| **Clave Pública** (e, n) | (7, 143) |
| **Clave Privada** (d, n) | (103, 143) |

---

### Paso 4: Verificación con m = 2

#### Cifrado: c = m^e mod n

```
c = 2^7 mod 143

128 < 143  →  128 mod 143 = 128

Resultado: c = 128
```

#### Descifrado: m = c^d mod n = 128^103 mod 143

Calcular 128^103 mod 143 directamente sería inmanejable. Se usa el **Teorema Chino del Resto (CRT)**, que descompone el cálculo en dos módulos más pequeños aprovechando que n = 11 × 13.

---

**Parte A — Reducir c módulo p y q:**

```
128 mod 11:
  11 × 11 = 121
  128 - 121 = 7
  → 128 ≡ 7 (mod 11)

128 mod 13:
  13 × 9 = 117
  128 - 117 = 11
  → 128 ≡ 11 (mod 13)
```

---

**Parte B — Reducir el exponente d usando el Pequeño Teorema de Fermat:**

El Pequeño Teorema de Fermat establece que para cualquier primo p y número a no divisible por p:
```
a^(p-1) ≡ 1 (mod p)
```

Aplicado a cada módulo:

```
Módulo 11  (p-1 = 10):
  103 = 10 × 10 + 3
  → 103 mod 10 = 3
  → 7^103 ≡ 7^3 (mod 11)

Módulo 13  (q-1 = 12):
  103 = 8 × 12 + 7
  → 103 mod 12 = 7
  → 11^103 ≡ 11^7 (mod 13)
```

---

**Parte C — Calcular 7^3 mod 11:**

```
7^2 = 49
49 mod 11:  11 × 4 = 44  →  49 - 44 = 5  →  7^2 ≡ 5 (mod 11)

7^3 = 7^2 × 7 = 5 × 7 = 35
35 mod 11:  11 × 3 = 33  →  35 - 33 = 2  →  7^3 ≡ 2 (mod 11)
```

---

**Parte D — Calcular 11^7 mod 13:**

```
11^2 = 121
121 mod 13:  13 × 9 = 117  →  121 - 117 = 4  →  11^2 ≡ 4 (mod 13)

11^4 = (11^2)^2 = 4^2 = 16
16 mod 13:  16 - 13 = 3  →  11^4 ≡ 3 (mod 13)

11^7 = 11^4 × 11^2 × 11^1 = 3 × 4 × 11 = 132
132 mod 13:  13 × 10 = 130  →  132 - 130 = 2  →  11^7 ≡ 2 (mod 13)
```

---

**Parte E — Reconstrucción con CRT:**

```
x ≡ 2 (mod 11)
x ≡ 2 (mod 13)
```

Ambos resultados son idénticos (2). Como gcd(11, 13) = 1, el CRT garantiza una solución única módulo 143:

```
x = 2 (mod 143)
```

**El mensaje descifrado es 2, coincidiendo con el mensaje original m = 2. Las claves funcionan correctamente.**

---

## 2. Lógica de Implementación: ¿Por qué encontrar d es computacionalmente imposible?

Para recuperar la clave privada d, un atacante que solo conoce n y e necesitaría calcular:

```
d ≡ e^(-1) (mod φ(n))
```

Esto requiere conocer φ(n) = (p - 1)(q - 1), lo que a su vez requiere **factorizar n en sus componentes primos p y q**.

En un sistema RSA de 2048 bits, n es el producto de dos números primos de aproximadamente 1024 bits cada uno (~309 dígitos decimales). La dificultad de factorizar tales números es lo que hace seguro a RSA, y esto depende de varios aspectos clave:

- **Mejor algoritmo conocido:** La Criba General del Cuerpo de Números (GNFS, por sus siglas en inglés) es el algoritmo clásico más eficiente para factorizar enteros grandes. Su complejidad temporal es sub-exponencial: L_n[1/3, (64/9)^(1/3)], lo que para una clave de 2048 bits se traduce en aproximadamente 2^112 operaciones, muy por encima de lo que cualquier hardware actual o futuro cercano puede realizar.

- **Récords actuales de factorización:** El número RSA más grande jamás factorizado es RSA-250 (829 bits, 250 dígitos decimales), logrado en febrero de 2020 por Boudot, Gaudry, Guillevic, Heninger, Thomé y Zimmermann usando aproximadamente 2.700 años-núcleo de CPU de cómputo distribuido en clusters de investigación en Francia, Alemania y Estados Unidos [1]. Extrapolando este esfuerzo a 2048 bits, el cómputo requerido crece en muchos órdenes de magnitud, las estimaciones lo sitúan en miles de millones de años con la tecnología actual.

- **Sin atajos clásicos conocidos:** Las computadoras clásicas no tienen ningún algoritmo de tiempo polinomial conocido para la factorización de enteros. Si bien el algoritmo cuántico de Shor podría teóricamente factorizar enteros en tiempo polinomial, el hardware cuántico tolerante a fallos necesario para romper RSA de 2048 bits, estimado en miles de qubits lógicos con corrección de errores — aún no existe.

- **Salvaguardas en la generación de claves:** Las implementaciones del mundo real añaden protecciones adicionales: los primos p y q se eligen como "primos fuertes" (donde p-1 y p+1 también tienen factores primos grandes), deben diferir significativamente en tamaño para prevenir el método de factorización de Fermat, y d debe ser suficientemente grande para prevenir el ataque de fracciones continuas de Wiener, que puede recuperar d cuando es demasiado pequeño en relación con n.

- **Recomendación NIST:** El **NIST SP 800-57 Part 1 Rev. 5** (*Recommendation for Key Management*, 2020) [2] clasifica RSA de 2048 bits como proveedora de 112 bits de fortaleza de seguridad y la considera aceptable para su uso hasta el 31 de diciembre de 2030. Para datos que requieran protección más allá de esa fecha, NIST recomienda migrar a RSA de al menos 3072 bits, que proporciona 128 bits de fortaleza de seguridad.

En resumen, la seguridad de RSA no descansa en una prueba matemática de que factorizar es difícil (esto sigue siendo un problema abierto en la teoría de la complejidad), sino en décadas de esfuerzo criptanalítico que han fallado consistentemente en producir un método eficiente de factorización para números grandes. La factorización de RSA-250 en 2020, que requirió años de cómputo para un número de menos de la mitad del tamaño de una clave RSA-2048 estándar — ilustra cuán amplia es la brecha que aún existe entre las capacidades actuales y los tamaños de clave del mundo real.

---

### Referencias

[1] F. Boudot, P. Gaudry, A. Guillevic, N. Heninger, E. Thomé, P. Zimmermann, *Factoring RSA-250*, anuncio del 28 de febrero de 2020. Disponible en: https://www.schneier.com/blog/archives/2020/04/rsa-250_factore.html

[2] NIST, *SP 800-57 Part 1 Rev. 5: Recommendation for Key Management: Part 1 – General*, 2020. Disponible en: https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final
