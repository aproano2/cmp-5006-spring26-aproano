# Guess My Cheese (Part 2)
## Método 2 – Precomputación tipo “Rainbow Table”

---

## 1. Contexto del problema

El servidor nos proporciona el siguiente hash SHA-256:

```
0d0b4e33c20cb9a03c2e115199810388d55da48b03a36f2724a6f44c3cc6641f
```

Sabemos por los *hints* que:

1. Se utiliza SHA-256.
2. La sal consiste exactamente en **2 caracteres hexadecimales**.
3. Se menciona el concepto de *rainbow tables*.

Un nibble = 4 bits  
2 nibbles = 8 bits = 1 byte  

Por lo tanto, la sal tiene **256 posibles valores (00–ff)**.

El problema consiste en encontrar:

- El nombre del queso (de una lista dada)
- El valor de la sal (1 byte en hexadecimal)

Tal que:

```
SHA256( queso_normalizado + salt_byte ) = hash_objetivo
```

---

## 2. ¿Qué es una Rainbow Table?

Una *rainbow table* es una estructura de datos que contiene hashes precomputados asociados a posibles entradas.

En lugar de calcular y comparar el hash en cada intento, se:

1. Generan todas las combinaciones posibles.
2. Se almacenan en un diccionario:
   ```
   hash → (queso, sal)
   ```
3. Se busca directamente el hash objetivo en la tabla.

Esto reduce el problema a una búsqueda en tiempo constante O(1).

Este enfoque es diferente al brute force clásico porque:
- Primero se genera la tabla completa.
- Luego se realiza una sola búsqueda directa.

---

## 3. Justificación Matemática

El espacio total de búsqueda es:

```
(# quesos en la lista) × 256 posibles sales
```

Si la lista contiene N quesos:

```
Espacio total = N × 256
```

Este espacio es pequeño, por lo que es completamente viable precomputar todas las combinaciones.

Dado que SHA-256 es determinístico:

```
Si input₁ = input₂  →  hash₁ = hash₂
```

Entonces basta con encontrar la combinación correcta.

---

## 4. Implementación en Python

```python
import hashlib

# Hash proporcionado por el servidor
target_hash = "0d0b4e33c20cb9a03c2e115199810388d55da48b03a36f2724a6f44c3cc6641f"

# Leer lista de quesos
with open("pablo_cheese_list.txt", "r", encoding="utf-8") as f:
    cheeses = [line.strip() for line in f if line.strip()]

# Diccionario tipo rainbow table
tabla = {}

for cheese in cheeses:
    # Normalización observada en el reto
    base = cheese.lower().encode("utf-8")
    
    for salt in range(256):
        candidate = base + bytes([salt])
        hash_value = hashlib.sha256(candidate).hexdigest()
        tabla[hash_value] = (cheese, format(salt, "02x"))

# Búsqueda directa
if target_hash in tabla:
    cheese, salt_hex = tabla[target_hash]
    print("ENCONTRADO")
    print("Queso:", cheese)
    print("Salt (hex):", salt_hex)
else:
    print("No encontrado")
```

---

## 5. Resultado

Se obtuvo:

- Queso: `Anejo Enchilado`
- Sal: `74`

Verificando:

```
SHA256("anejo enchilado" + 0x74) 
= 0d0b4e33c20cb9a03c2e115199810388d55da48b03a36f2724a6f44c3cc6641f
```

---

## 6. ¿Por qué funciona este método?

Funciona porque:

1. El espacio de búsqueda es pequeño.
2. La sal es extremadamente corta (1 byte).
3. SHA-256 es determinístico.
4. No existe mecanismo adicional de protección como:
   - Sal larga
   - Iteraciones múltiples (PBKDF2)
   - bcrypt
   - Argon2

Este reto demuestra por qué una sal de 8 bits es criptográficamente insegura.

---

## 7. Diferencia con el Método 1

| Método 1 | Método 2 |
|----------|----------|
| Compara en cada iteración | Precomputa todo primero |
| Búsqueda secuencial | Búsqueda en diccionario |
| Más simple | Conceptualmente más avanzado |
| No usa almacenamiento intermedio | Usa estructura hash |

---

## 8. Lección de Seguridad

Este reto ilustra que:

- Una sal de 1 byte es trivial de romper.
- Los hashes sin mecanismos de endurecimiento son vulnerables.
- Los ataques tipo diccionario siguen siendo efectivos.
- Las rainbow tables son viables cuando el espacio de búsqueda es pequeño.

En entornos reales se recomienda:

- Sal de al menos 128 bits.
- Funciones de derivación de claves como:
  - PBKDF2
  - bcrypt
  - scrypt
  - Argon2

---

## 9. Referencias

- NIST FIPS 180-4 – Secure Hash Standard (SHA-256)
- RFC 8018 – PKCS #5: Password-Based Cryptography Specification
- A. Menezes, P. van Oorschot, S. Vanstone – Handbook of Applied Cryptography
- Wikipedia – Rainbow Table Attack
- OWASP Password Storage Cheat Sheet

---

## 10. Conclusión

El Método 2 demuestra un enfoque estructurado y más eficiente que el brute force clásico.  
Además, conecta directamente con el hint proporcionado en el reto sobre *rainbow tables*.

Este método no rompe SHA-256, sino que explota la debilidad del espacio de entrada reducido.