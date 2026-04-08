# Parte 2: Funciones Hash Criptográficas (Verificación de Integridad)

## 1. El Efecto Avalancha

Si se cambia exactamente un bit en el archivo de firmware de 2GB y se pasa nuevamente por SHA-256, aproximadamente el 50% de los bits del hash resultante cambiarán (alrededor de 128 de los 256 bits). Este comportamiento se conoce como el **Efecto Avalancha**, una propiedad descrita formalmente por Horst Feistel en su trabajo fundacional sobre diseño de cifrados en bloque: una función criptográfica exhibe el criterio estricto de avalancha cuando voltear un único bit de entrada hace que cada bit de salida se voltee con una probabilidad del 50%.

SHA-256 está especificado en **FIPS 180-4** (NIST, *Secure Hash Standard*, 2012) [1], que define el conjunto completo de algoritmos de la familia SHA-2. El estándar define SHA-256 como una función hash unidireccional que produce un digest fijo de 256 bits, con el requisito de diseño de que cualquier cambio en la entrada produzca una salida estadísticamente indistinguible de un valor completamente nuevo y aleatorio.

### Cómo SHA-256 logra esto

SHA-256 procesa datos en bloques de 512 bits a través de 64 rondas de compresión. Cada ronda aplica una combinación de operaciones bit a bit (Ch, Maj), adición modular y rotaciones lógicas (Σ0, Σ1) que propagan cualquier pequeño cambio a través de todo el estado interno. Después de procesar incluso el primer bloque modificado, el valor de encadenamiento de 256 bits es completamente diferente, y cada bloque subsiguiente amplifica aún más la divergencia. Para cuando un archivo de 2GB termina de procesarse, un solo bit volteado se ha propagado a través de miles de millones de rondas de compresión.

### Importancia para la detección de ataques Man-in-the-Middle

Esta propiedad es esencial porque elimina la posibilidad de una manipulación sutil. Sin el efecto avalancha, un atacante que realice un ataque MitM podría elaborar cuidadosamente pequeñas modificaciones — por ejemplo, inyectar una rutina de backdoor en el firmware — que produzcan un hash cercano al original. El vehículo podría entonces no detectar la diferencia, especialmente si solo se utiliza una comparación basada en umbral.

Con la propiedad de avalancha de SHA-256, no existe el concepto de un hash "similar", cualquier modificación, por pequeña que sea, produce una salida que parece una cadena completamente aleatoria de 256 bits sin ninguna relación con el original. El vehículo puede por lo tanto realizar una verificación binaria de igualdad simple: o el hash coincide exactamente, o el firmware ha sido manipulado. No existe zona gris, ni ningún ataque que produzca un resultado "suficientemente cercano".

---

## 2. Resistencia a Colisiones

Una **colisión** ocurre cuando dos entradas distintas producen la misma salida hash: dado A ≠ B, pero H(A) = H(B). Por la **Paradoja del Cumpleaños**, encontrar una colisión en una función hash de n bits requiere aproximadamente 2^(n/2) intentos, para SHA-256, esto significa alrededor de 2^128 operaciones, lo cual es computacionalmente inviable con cualquier tecnología previsible.

### Por qué una colisión rompe la seguridad del vehículo

La cadena de seguridad del sistema de actualización de AutoDrive funciona de la siguiente manera:

1. HQ calcula el hash de Update.bin: H(Update.bin)
2. HQ firma ese hash con su clave privada: Firma = Sign(H(Update.bin), ClavePrivada_HQ)
3. El vehículo recibe el archivo + la firma, recalcula el hash y verifica la firma

Si un atacante encuentra una colisión donde H(Virus.bin) = H(Update.bin), esta cadena colapsa por completo:

- **La integridad se rompe:** El vehículo recalcula H(Virus.bin) y obtiene el mismo resultado que H(Update.bin). La verificación de integridad pasa a pesar de que el archivo es completamente diferente.
- **La autenticación se rompe:** La firma digital que HQ creó para Update.bin ahora es **matemáticamente válida** para Virus.bin también, ya que las firmas operan sobre el hash, no directamente sobre el archivo. El vehículo no tiene mecanismo para distinguir entre los dos.
- **El no repudio queda comprometido:** La prueba criptográfica de que HQ autorizó una actualización específica se vuelve ambigua — la misma firma podría corresponder a dos archivos diferentes, haciendo imposible determinar cuál firmó realmente HQ.

### Precedente en el mundo real

Esta no es una preocupación teórica. En 2008, un equipo de investigadores — Alexander Sotirov, Marc Stevens, Jacob Appelbaum, Arjen Lenstra, David Molnar, Dag Arne Osvik y Benne de Weger, demostró un ataque práctico de colisión de prefijo elegido contra MD5 que les permitió crear un certificado de Autoridad Certificadora (CA) falso [2]. Generaron dos certificados diferentes que compartían el mismo hash MD5, logrando forjar un certificado de CA confiable para todos los navegadores principales de la época. El ataque fue presentado en el 25.° Chaos Communication Congress en Berlín el 30 de diciembre de 2008, y un artículo completo fue publicado en las memorias de CRYPTO 2009.

Este ataque del mundo real llevó a la deprecación generalizada de MD5 en certificados digitales y aceleró la adopción de SHA-256 como estándar. También demostró exactamente por qué una colisión no es solo una curiosidad matemática, es un arma práctica que puede eludir por completo las garantías de autenticación de un sistema basado en PKI.

Es precisamente por esto que SHA-256 fue elegido para sistemas como la verificación de firmware. Su resistencia a colisiones de 128 bits (2^128 operaciones para encontrar una colisión) proporciona un margen de seguridad suficiente contra ataques de fuerza bruta y analíticos, y FIPS 180-4 del NIST continúa recomendándolo como función hash estándar para la verificación de integridad en aplicaciones de seguridad crítica [1].

---

### Referencias

[1] NIST, *FIPS 180-4: Secure Hash Standard (SHS)*, marzo 2012. Disponible en: https://csrc.nist.gov/pubs/fips/180-4/upd1/final

[2] A. Sotirov, M. Stevens, J. Appelbaum, A. Lenstra, D. Molnar, D. A. Osvik, B. de Weger, *MD5 Considered Harmful Today: Creating a Rogue CA Certificate*, 25.° Chaos Communication Congress, Berlín, 30 de diciembre de 2008. Disponible en: https://fahrplan.events.ccc.de/congress/2008/Fahrplan/attachments/1251_md5-collisions-1.0.pdf — Versión extendida: https://eprint.iacr.org/2009/111
