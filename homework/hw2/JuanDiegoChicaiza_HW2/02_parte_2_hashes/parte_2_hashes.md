# Parte 2: Hashes criptográficos

**Estudiante:** Juan Diego Chicaiza, María Emilia Granda, Sebastián Encalada
**Tema:** Integridad y resistencia a colisiones

## 1. El efecto avalancha

Si se cambia exactamente **un bit** en un firmware de 2 GB y luego se vuelve a calcular SHA-256, el nuevo hash debe verse completamente distinto del hash original.

### ¿Cuánto debería cambiar?

SHA-256 produce una salida de 256 bits. En una función hash criptográfica bien diseñada, cada bit de salida debería cambiar con probabilidad cercana a `1/2` cuando el input sufre una modificación mínima. Eso implica un cambio esperado de:

\[
256 \cdot \frac{1}{2} = 128 \text{ bits}
\]

No significa que en todos los casos cambiarán exactamente 128 bits. Significa que la nueva salida debe comportarse como si fuera prácticamente aleatoria respecto de la anterior.

### ¿Por qué esto es importante frente a un ataque Man-in-the-Middle?

Supongamos que AutoDrive HQ firma el hash SHA-256 del firmware oficial. Si un atacante intercepta la descarga y cambia un solo bit:

1. el vehículo recalcula el hash del archivo recibido
2. ese nuevo hash ya no coincide con el hash firmado por HQ
3. la firma digital deja de validar
4. el vehículo rechaza la actualización

Esta propiedad es esencial porque convierte modificaciones diminutas y difíciles de percibir en un error criptográfico evidente. El atacante no puede "ajustar un poco" el archivo esperando que el hash siga siendo parecido: el diseño de la función hash precisamente destruye esa posibilidad.

## 2. Resistencia a colisiones

### ¿Qué es una colisión?

Una **colisión** ocurre cuando dos entradas distintas producen la misma salida hash.

Formalmente:

\[
M_1 \neq M_2 \quad \text{pero} \quad H(M_1)=H(M_2)
\]

En el escenario del homework:

- `Update.bin` es el firmware legítimo
- `Virus.bin` es un firmware malicioso

Si un atacante lograra que:

\[
\text{SHA-256(Update.bin)} = \text{SHA-256(Virus.bin)}
\]

entonces ambas entradas tendrían el mismo resumen criptográfico.

### ¿Por qué eso rompería toda la seguridad del automóvil?

Porque la firma digital normalmente no se aplica byte por byte sobre el archivo completo en forma ingenua, sino sobre una representación derivada de su hash. Entonces ocurriría lo siguiente:

1. HQ firma el hash del archivo legítimo
2. el atacante sustituye el archivo por otro malicioso con el mismo hash
3. el vehículo recalcula el hash y obtiene el mismo valor
4. la firma sigue siendo válida
5. el vehículo acepta un firmware malicioso como si hubiera sido autorizado por HQ

Eso destruye el principio de autenticidad del sistema: la firma ya no estaría unida de forma única a un solo binario.

### Matiz técnico importante

En hash criptográfico conviene distinguir tres propiedades relacionadas:

- **Resistencia a colisiones:** es difícil encontrar dos archivos cualesquiera con el mismo hash.
- **Resistencia a segunda preimagen:** dado un archivo legítimo, es difícil construir otro distinto con el mismo hash.
- **Resistencia a preimagen:** dado un hash, es difícil encontrar una entrada que lo produzca.

En un sistema de actualizaciones, la resistencia a colisiones y la resistencia a segunda preimagen son especialmente relevantes porque la firma necesita representar **de manera única** el firmware autorizado.

### Conclusión de seguridad

El hash no solo sirve para detectar corrupción accidental. También sirve como un "resumen vinculante" del artefacto autorizado. Si un atacante pudiera generar colisiones prácticas contra SHA-256, el modelo completo de integridad y autenticidad del pipeline de actualización colapsaría.

## Referencias

1. NIST FIPS 180-4, *Secure Hash Standard (SHS)*.
2. NIST CSRC Glossary, *Collision*.
3. RFC 8017, sección sobre uso de funciones hash resistentes a colisiones.
