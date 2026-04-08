# Parte 3: Certificados Digitales (La Cadena de Confianza)

## 1. El Proceso de Solicitud de Firma de Certificado (CSR)

Una Solicitud de Firma de Certificado (CSR, por sus siglas en inglés) es un mensaje con estructura formal definida por **PKCS #10 / RFC 2986** (IETF, *Certification Request Syntax Specification Version 1.7*) [1] que una entidad envía a una Autoridad Certificadora (CA) para solicitar un certificado digital X.509 firmado. El formato especifica que la CSR debe ser firmada con la propia clave privada del solicitante, lo que sirve como prueba de posesión, la CA puede verificar que el solicitante realmente posee la clave privada correspondiente a la clave pública que está enviando.

### Los cuatro elementos principales que AutoDrive HQ debe incluir en la CSR:

1. **Clave Pública:** La clave pública RSA (o ECC) que será incorporada en el certificado. Esta es la clave que los vehículos utilizarán para verificar las firmas digitales de HQ. La CA no genera esta clave, HQ genera su propio par de claves y solo envía la porción pública en la CSR.

2. **Nombre Distinguido del Sujeto (DN):** Un campo de identidad estructurado que sigue la convención de nombres X.500 e identifica al titular del certificado. Para AutoDrive HQ, esto incluiría:
   - **Nombre Común (CN):** p. ej., `updates.autodrive.com`
   - **Organización (O):** p. ej., `AutoDrive Inc.`
   - **Unidad Organizacional (OU):** p. ej., `Firmware Engineering`
   - **País (C)**, **Estado (ST)**, **Localidad (L)**

3. **Identificador del Algoritmo de Firma:** Especifica qué algoritmo se utilizó para firmar la propia CSR (p. ej., SHA-256 con RSA). Esto permite a la CA verificar la integridad de la CSR y confirma que HQ es capaz de realizar operaciones criptográficas con el par de claves enviado.

4. **Firma Digital de la CSR:** Todo el contenido de la CSR es hasheado y firmado con la clave privada de HQ. Esto cumple un doble propósito: demuestra que HQ posee la clave privada correspondiente a la clave pública enviada (prueba de posesión), y garantiza que la CSR no ha sido alterada durante su tránsito hacia la CA.

### El proceso de validación de la CA

Antes de emitir el certificado, la CA realiza un proceso de verificación que varía según el tipo de certificado, tal como está definido en el **perfil de certificado X.509** estandarizado en **RFC 5280** (IETF) [2]:

- **Validación de Dominio (DV):** La CA solo confirma que el solicitante controla el dominio (p. ej., mediante un registro DNS o un desafío por correo electrónico). Es el nivel más simple y rápido.
- **Validación de Organización (OV):** La CA verifica la existencia legal e identidad de la organización a través de registros comerciales y contacto directo.
- **Validación Extendida (EV):** El nivel más riguroso — requiere documentación legal, verificación de dirección física y autorización por parte de un funcionario nombrado. Para un sistema de seguridad crítica como el pipeline de firmware de AutoDrive, un certificado EV sería la elección apropiada, ya que proporciona la mayor garantía de identidad organizacional.

Una vez validado, la CA firma el certificado con su propia clave privada, creando un vínculo a prueba de manipulaciones entre la identidad de HQ y su clave pública que cualquier parte con la clave pública de la CA puede verificar de forma independiente.

---

## 2. Validación del Certificado Raíz

Para que el vehículo pueda verificar el certificado de HQ, el Certificado Raíz de la CA debe estar preinstalado en el almacén de certificados de confianza del vehículo en la fábrica. Específicamente, este es el certificado X.509 autofirmado de la Autoridad Certificadora Raíz que se encuentra en la cima de la cadena de certificados. El formato del certificado X.509 v3 y el algoritmo completo de validación de cadena están definidos en RFC 5280 [2].

### Cómo funciona la cadena de verificación

En la práctica, la cadena típicamente tiene tres niveles:

1. **Certificado de CA Raíz** (preinstalado en el vehículo) → autofirmado, sirve como ancla de confianza
2. **Certificado de CA Intermedia** → firmado por la CA Raíz
3. **Certificado de AutoDrive HQ** → firmado por la CA Intermedia

Cuando el vehículo recibe el certificado de HQ junto con una actualización de firmware, realiza la siguiente validación:

1. Lee el certificado de HQ y extrae el campo del emisor (la CA Intermedia).
2. Verifica la firma del certificado de HQ usando la clave pública de la CA Intermedia.
3. Verifica la firma del certificado de la CA Intermedia usando la clave pública de la CA Raíz.
4. Confirma que el certificado de la CA Raíz existe en su almacén de confianza preinstalado.
5. Comprueba que ningún certificado en la cadena ha expirado (mediante el campo `notAfter`) ni ha sido revocado (mediante CRL u OCSP, ambos definidos en RFC 5280 [2]).

Si alguno de estos pasos falla, el vehículo rechaza el certificado y se niega a instalar la actualización.

### Por qué el Certificado Raíz debe instalarse en fábrica

El Certificado Raíz no puede entregarse a través de la red, esto crearía una dependencia circular: se necesitaría un certificado de confianza para verificar el mismo certificado que establece la confianza. Al incorporarlo en el hardware o firmware protegido del vehículo en la fábrica, se establece un ancla de confianza fuera de línea que es inmune a ataques basados en red y no puede ser sustituida por un atacante.

En sistemas automotrices, esto se almacena típicamente en un elemento protegido por hardware dentro del ECU del vehículo, haciéndolo resistente tanto a manipulaciones de software como físicas. Dos estándares clave gobiernan este requisito:

- **ISO/SAE 21434:2021** (*Road Vehicles — Cybersecurity Engineering*) [3], publicado conjuntamente por ISO y SAE International en agosto de 2021, define los requisitos de ingeniería para la gestión de riesgos de ciberseguridad a lo largo de todo el ciclo de vida del vehículo, incluyendo el almacenamiento seguro de material criptográfico como los certificados raíz.

- **Reglamento ONU N.º 155** (UNECE WP.29) [4], que se volvió obligatorio para las nuevas aprobaciones de tipo vehicular en la UE en julio de 2022, exige que los fabricantes implementen un Sistema de Gestión de Ciberseguridad (CSMS) certificado que cubra la protección de credenciales criptográficas durante toda la vida operativa del vehículo.

En conjunto, ISO/SAE 21434 y UNECE R155 establecen que incorporar una raíz de confianza en fábrica no es solo una buena práctica, es un requisito de ingeniería y regulatorio para los vehículos distribuidos en mercados regulados.

---

### Referencias

[1] M. Nystrom, B. Kaliski, *RFC 2986: PKCS #10: Certification Request Syntax Specification Version 1.7*, IETF, noviembre 2000. Disponible en: https://www.rfc-editor.org/rfc/rfc2986

[2] D. Cooper et al., *RFC 5280: Internet X.509 Public Key Infrastructure Certificate and CRL Profile*, IETF, mayo 2008. Disponible en: https://datatracker.ietf.org/doc/html/rfc5280

[3] ISO/SAE, *ISO/SAE 21434:2021 — Road Vehicles: Cybersecurity Engineering*, publicado agosto 2021. Disponible en: https://www.iso.org/standard/70918.html

[4] UNECE WP.29, *Reglamento ONU N.º 155: Disposiciones Uniformes Relativas a la Aprobación de Vehículos en Materia de Ciberseguridad y Sistema de Gestión de Ciberseguridad*, obligatorio para aprobaciones de tipo en la UE desde julio 2022. Disponible en: https://unece.org/transport/documents/2021/03/standards/un-regulation-no-155-cyber-security-and-cyber-security
