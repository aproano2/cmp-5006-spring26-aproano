# Parte 5: Desafío de Diseño de Sistema - Protocolo de Actualización Segura

## Resumen General

El siguiente protocolo utiliza un Sistema Híbrido: la criptografía asimétrica (RSA) se encarga del intercambio de claves y la autenticación, mientras que la criptografía simétrica (AES-256) se encarga del cifrado real del archivo de firmware de gran tamaño. La razón de esta separación es fundamental: RSA es matemáticamente seguro pero computacionalmente lento, no puede procesar eficientemente gigabytes de datos. AES es extremadamente rápido para grandes volúmenes de datos pero requiere que una clave secreta compartida sea establecida de forma segura primero. El enfoque híbrido utiliza cada algoritmo donde mejor se desempeña, combinando sus fortalezas.

---

### Protocolo Paso a Paso

**Fase 1: Preparación (AutoDrive HQ)**

1. HQ genera una **clave de sesión AES-256** aleatoria específica para esta actualización. Se genera una nueva clave para cada actualización de forma independiente, lo que significa que si la clave de sesión de una actualización fuera comprometida en el futuro, no afectaría a ninguna otra actualización, cada una está aislada.

2. HQ cifra el archivo de firmware de 2GB usando **AES-256-GCM**:
   `firmware_cifrado = AES-256-GCM(Update.bin, clave_sesion)`
   Se elige el modo GCM (Galois/Counter Mode) porque es un esquema de *cifrado autenticado*, proporciona simultáneamente confidencialidad (nadie puede leer el texto plano) e integridad (cualquier modificación al texto cifrado es detectable mediante una etiqueta de autenticación). Este modo está estandarizado en **NIST SP 800-38D** (*Recommendation for Block Cipher Modes of Operation: Galois/Counter Mode (GCM) and GMAC*, noviembre 2007) [1], que define GCM como aprobado para uso federal con cifrados en bloque que operan sobre bloques de 128 bits, como AES.

3. HQ calcula el hash SHA-256 del firmware **original en texto plano**:
   `hash_firmware = SHA-256(Update.bin)`
   SHA-256 está especificado en **FIPS 180-4** [2].

4. HQ firma el hash con su clave privada usando RSASSA-PSS (según **RFC 8017** [3]):
   `firma = RSASSA-PSS_Sign(hash_firmware, ClavePrivada_HQ)`

5. HQ cifra la clave de sesión AES usando la **clave pública RSA del vehículo**:
   `clave_sesion_cifrada = RSA_Encrypt(clave_sesion, ClavePublica_Vehiculo)`
   Solo ese vehículo específico posee la clave privada correspondiente, por lo que solo él puede recuperar la clave de sesión.

6. HQ ensambla el paquete de actualización completo:
   `{ firmware_cifrado, clave_sesion_cifrada, firma, certificado_HQ, version_firmware, timestamp }`

---

**Fase 2: Transmisión**

7. HQ envía el paquete de actualización al vehículo. El canal en sí puede estar protegido por **TLS 1.3** (especificado en RFC 8446), que añade una capa externa de cifrado a nivel de transporte. Sin embargo, el protocolo está diseñado para ser seguro de forma independiente a la capa de transporte, cada elemento sensible del paquete está protegido a nivel de aplicación. Si TLS fuera vulnerado o eludido, el atacante aún se enfrentaría a la clave de sesión cifrada con RSA y al firmware firmado de forma independiente. Este diseño por capas es un principio estándar en ingeniería de seguridad conocido como defensa en profundidad.

---

**Fase 3: Verificación e Instalación (Vehículo)**

8. El vehículo valida el **certificado X.509** de HQ (cuyo perfil está definido en **RFC 5280** [4]) mediante:
   - Verificar que el certificado fue firmado por el certificado de la CA Raíz preinstalado en el vehículo en la fábrica.
   - Confirmar que el certificado no ha expirado (revisando el campo `notAfter`).
   - Comprobar que el certificado no ha sido revocado — ya sea mediante una Lista de Revocación de Certificados (CRL) en caché o a través del Protocolo de Estado de Certificados en Línea (OCSP), ambos definidos dentro del marco RFC 5280.
   - Si alguna de estas verificaciones falla → rechazar la actualización inmediatamente.

9. El vehículo descifra la clave de sesión usando su propia clave privada RSA:
   `clave_sesion = RSA_Decrypt(clave_sesion_cifrada, ClavePrivada_Vehiculo)`

10. El vehículo descifra el firmware usando la clave de sesión recuperada:
    `Update.bin = AES-256-GCM_Decrypt(firmware_cifrado, clave_sesion)`
    Si la **etiqueta de autenticación** GCM no coincide, significa que el texto cifrado fue alterado después del cifrado — el vehículo rechaza la actualización en este paso, antes incluso de examinar la firma.

11. El vehículo recalcula el hash del firmware descifrado:
    `hash_local = SHA-256(Update.bin)`

12. El vehículo verifica la firma de HQ usando la clave pública de HQ (extraída del certificado validado):
    `válido = RSASSA-PSS_Verify(firma, hash_local, ClavePublica_HQ)`

13. Si la verificación es exitosa: `hash_local` coincide con lo que HQ firmó, el firmware es auténtico e inalterado → proceder con la instalación. De lo contrario → rechazar la actualización.

14. El vehículo registra la versión del firmware, su hash, la firma de HQ y la marca de tiempo en un registro interno protegido almacenado en almacenamiento seguro resistente a manipulaciones. Este registro sirve como un rastro de auditoría verificable, satisfaciendo los requisitos de trazabilidad del Reglamento ONU N.º 156 (UNECE WP.29) [5], que exige que todas las actualizaciones de software distribuidas a vehículos sean trazables y auditables por autoridades externas.

---

## Tabla de Requisitos

| Requisito | Cómo lo logra el diseño |
|:---|:---|
| **1. Intercambio Seguro de Claves** | La clave de sesión AES-256 está cifrada con la clave pública RSA del vehículo (Paso 5), por lo que solo ese vehículo puede recuperarla con su clave privada (Paso 9). Un paquete interceptado es inútil para un atacante sin la clave privada del vehículo. Además, se genera una clave de sesión nueva por cada actualización: incluso si una clave pasada fuera comprometida en el futuro, no expondría ninguna otra actualización, cada una está protegida de forma independiente. |
| **2. Confidencialidad** | El firmware de 2GB está cifrado con AES-256-GCM (Paso 2), estandarizado en NIST SP 800-38D [1]. Este cifrado proporciona cifrado de alto rendimiento adecuado para archivos grandes, un competidor que monitoree la red solo verá texto cifrado. Sin la clave de sesión (protegida con RSA), el código del firmware es ilegible. TLS 1.3 en el canal de transporte (Paso 7) añade una segunda capa de confidencialidad. |
| **3. Integridad** | La integridad se aplica en dos puntos independientes. Primero, la etiqueta de autenticación integrada en AES-256-GCM (NIST SP 800-38D) detecta cualquier modificación al texto cifrado durante el tránsito (Paso 10). Segundo, el vehículo recalcula el hash SHA-256 del firmware descifrado (FIPS 180-4) y lo verifica contra la firma RSASSA-PSS de HQ (RFC 8017) en los Pasos 11–13. Ambas verificaciones deben pasar, un archivo que supera la etiqueta GCM pero falla la comparación de firma es igualmente rechazado. |
| **4. Autenticación** | El vehículo verifica el certificado X.509 de HQ (RFC 5280) contra la CA Raíz instalada en fábrica (Paso 8), incluyendo verificaciones de expiración y revocación. Esto confirma que la clave pública en el certificado pertenece genuinamente a AutoDrive HQ y no a un servidor suplantado. La firma digital RSASSA-PSS (Paso 12) confirma además que el titular de la clave privada de HQ autorizó específicamente esta versión exacta del firmware. |
| **5. No Repudio** | La firma RSASSA-PSS de HQ (Paso 4) vincula criptográficamente la identidad de HQ al contenido exacto del firmware. Dado que solo HQ posee la clave privada, no puede negar haber autorizado esta versión específica. El registro de auditoría resistente a manipulaciones del vehículo (Paso 14) preserva la firma, el hash, la versión y la marca de tiempo como evidencia verificable de forma independiente — satisfaciendo tanto los requisitos criptográficos de las firmas basadas en RSA como el mandato de trazabilidad del Reglamento ONU N.º 156 [5]. Cualquier tercero con acceso al certificado público de HQ puede verificar la cadena de evidencia sin depender del relato de ninguna de las partes. |

---

### Referencias

[1] NIST, *SP 800-38D: Recommendation for Block Cipher Modes of Operation: Galois/Counter Mode (GCM) and GMAC*, noviembre 2007. Disponible en: https://csrc.nist.gov/pubs/sp/800/38/d/final

[2] NIST, *FIPS 180-4: Secure Hash Standard (SHS)*, marzo 2012. Disponible en: https://csrc.nist.gov/pubs/fips/180-4/upd1/final

[3] K. Moriarty et al., *RFC 8017: PKCS #1: RSA Cryptography Specifications Version 2.2*, IETF, noviembre 2016. Disponible en: https://www.rfc-editor.org/rfc/rfc8017.html

[4] D. Cooper et al., *RFC 5280: Internet X.509 Public Key Infrastructure Certificate and CRL Profile*, IETF, mayo 2008. Disponible en: https://datatracker.ietf.org/doc/html/rfc5280

[5] UNECE WP.29, *Reglamento ONU N.º 156: Actualización de Software y Sistema de Gestión de Actualizaciones de Software*, en vigor desde 2022. Disponible en: https://unece.org/transport/documents/2021/03/standards/un-regulation-no-156-software-update-and-software-update
