# Parte 4: Firmas Digitales (Autenticación)

## 1. El Flujo de Trabajo: Creación de la Firma

El proceso de firmar digitalmente una actualización de firmware sigue un enfoque de "hash primero, luego firmar". En lugar de firmar directamente el archivo de 2GB completo, AutoDrive HQ primero lo reduce a una huella digital compacta y de tamaño fijo usando una función hash criptográfica, y luego firma esa huella con su clave privada. Este diseño es tanto práctico como criptográficamente sólido.

### ¿Qué se hashea?

El binario completo del firmware de 2GB (Update.bin) se pasa por **SHA-256**, produciendo un digest fijo de 256 bits (32 bytes). Este digest actúa como una huella única del contenido exacto del archivo. SHA-256 está definido en **FIPS 180-4** (NIST, *Secure Hash Standard*, 2012), el estándar federal que especifica todos los algoritmos de la familia SHA-2 [1]. Según este estándar, incluso el cambio más pequeño en la entrada producirá, con probabilidad abrumadora, un digest completamente diferente, una propiedad esencial para detectar cualquier manipulación.

La razón por la que HQ hashea primero, en lugar de firmar el archivo completo, se reduce a dos limitaciones concretas:

- **Rendimiento:** Las operaciones RSA son computacionalmente costosas a nivel de algoritmo. Ejecutar RSA sobre 2GB de datos sería impráctico, especialmente para vehículos operando en campo con hardware limitado. Al hashear primero, la entrada a RSA es siempre un valor fijo de 32 bytes independientemente del tamaño del firmware.
- **Restricción de tamaño:** RSA solo puede operar sobre datos más pequeños que el módulo n de la clave. Para una clave de 2048 bits, eso significa un máximo de 256 bytes por operación — demasiado pequeño para procesar un binario grande en un solo paso. El hash elimina esta restricción por completo, ya que la salida siempre es menor que el módulo.

### ¿Qué clave se usa?

El digest del hash se firma usando la **Clave Privada de HQ**. Esta es la asimetría fundamental que hace funcionar las firmas digitales:

- **Cifrado** usa la clave pública del destinatario, para que solo él pueda descifrar.
- **Firma** usa la clave privada del emisor, para que cualquiera con la clave pública del emisor pueda verificar que solo él pudo haber producido la firma.

Dado que solo AutoDrive HQ controla su clave privada, una firma válida es prueba criptográfica del origen.

### Esquema de firma: RSASSA-PSS vs. PKCS#1 v1.5

Vale la pena entender que el firmado RSA en bruto no se usa directamente en la práctica. Las implementaciones reales aplican un esquema de relleno (padding) al hash antes de la operación RSA. Existen dos esquemas: **RSASSA-PKCS1-v1.5** (el estándar más antiguo) y **RSASSA-PSS** (Probabilistic Signature Scheme).

Ambos están especificados en **RFC 8017** (IETF, *PKCS #1: RSA Cryptography Specifications Version 2.2*, noviembre 2016) [2]. El RFC establece explícitamente que, si bien no se conocen ataques prácticos contra RSASSA-PKCS1-v1.5, "en aras de una mayor robustez, RSASSA-PSS es **requerido** en nuevas aplicaciones". La diferencia clave es que PSS introduce un relleno aleatorio antes de firmar, lo que significa que dos operaciones de firma sobre el mismo hash producen resultados diferentes cada vez. Esto cierra ciertas vulnerabilidades teóricas a las que los esquemas deterministas son susceptibles, y RSASSA-PSS cuenta con una prueba formal de seguridad bajo el modelo de oráculo aleatorio, algo de lo que PKCS1-v1.5 carece.

Para la implementación de AutoDrive, RSASSA-PSS es la elección apropiada.

### Flujo completo de firma

1. HQ calcula: `hash = SHA-256(Update.bin)`  *(según FIPS 180-4)*
2. HQ firma: `firma = RSASSA-PSS_Sign(hash, ClavePrivada_HQ)`  *(según RFC 8017)*
3. HQ transmite al vehículo: `Update.bin` + `firma` + `certificado de HQ`

### Flujo de verificación (lado del vehículo)

1. El vehículo valida el certificado de HQ a través de la cadena de confianza (como se describe en la Parte 3).
2. El vehículo extrae la clave pública de HQ del certificado verificado.
3. El vehículo calcula independientemente: `hash_local = SHA-256(Update.bin)`
4. El vehículo verifica la firma: `válido = RSASSA-PSS_Verify(firma, hash_local, ClavePublica_HQ)`
5. Si la verificación retorna verdadero, la actualización es auténtica e intacta — procede la instalación. De lo contrario, se rechaza la actualización.

Si el firmware fue modificado en tránsito, `hash_local` diferirá de lo que la firma codifica y la verificación fallará. Si un atacante intenta forjar una firma desde cero, necesitaría la clave privada de HQ, la cual no posee.

---

## 2. No Repudio

El no repudio significa que el autor de una acción no puede negar de manera creíble haberla producido. En el contexto de AutoDrive, si una actualización de firmware defectuosa causa que un vehículo falle, HQ podría intentar afirmar que nunca autorizó esa versión específica. Las firmas digitales hacen que esta negación sea insostenible — tanto técnica como legalmente.

### Cómo la firma garantiza el no repudio

El argumento descansa en una cadena clara de lógica:

1. **Solo HQ posee la clave privada** utilizada para producir la firma. Esta clave es generada y almacenada en la infraestructura segura de HQ y nunca es transmitida ni compartida externamente.
2. **La firma está matemáticamente vinculada** tanto a la clave privada de HQ como al contenido exacto del firmware. No es un sello de aprobación genérico — se calcula a partir del hash de ese archivo específico. La misma clave privada no puede usarse para "reutilizar" una firma en una versión de firmware diferente.
3. **Cualquier tercero puede verificar independientemente** la firma usando la clave pública de HQ, que está incorporada en su certificado emitido públicamente. Esto significa que un tribunal, una aseguradora, o un regulador de seguridad pueden confirmar la autoría sin depender del relato de ninguna de las partes.

Concretamente: si el registro de un vehículo contiene una firma RSASSA-PSS válida de HQ sobre la versión X del firmware, HQ no puede afirmar que no autorizó la versión X, porque solo la clave privada de HQ pudo haber producido esa firma.

### Reconocimiento legal de las firmas digitales

Las firmas digitales basadas en infraestructura de clave pública tienen peso legal en las principales jurisdicciones:

- **Unión Europea - Reglamento eIDAS (UE) N.º 910/2014** [3]: En vigor desde julio de 2016, este reglamento establece que las Firmas Electrónicas Cualificadas (QES) — basadas en un certificado cualificado emitido por un proveedor de servicios de confianza — son legalmente equivalentes a las firmas manuscritas y son admisibles como prueba en todos los estados miembros de la UE.
- **Estados Unidos - Ley de Firmas Electrónicas en el Comercio Global y Nacional (ESIGN Act), Ley Pública 106-229** [4]: Promulgada el 30 de junio de 2000, esta ley federal establece que un contrato o firma "no puede ser negado de efecto legal, validez o ejecutabilidad únicamente porque esté en formato electrónico". Las firmas electrónicas basadas en PKI cumplen este estándar.

### Requisitos de responsabilidad específicos del sector automotriz

Más allá de la legislación general sobre firmas electrónicas, la industria automotriz tiene su propio marco regulatorio. El **Reglamento ONU N.º 156** (UNECE WP.29, en vigor desde 2022) [5] exige que los fabricantes de vehículos implementen un Sistema de Gestión de Actualizaciones de Software (SUMS) certificado que mantenga un registro verificable y trazable de cada actualización de software distribuida a los vehículos — incluyendo evidencia criptográfica de autorización. El reglamento está armonizado con la norma **ISO 24089** (*Ingeniería de Actualización de Software para Vehículos de Carretera*).

Esto significa que AutoDrive no solo está criptográficamente vinculado por la firma digital, sino que también está legalmente obligado bajo la regulación automotriz internacional a mantener registros que puedan ser auditados de forma independiente. El sistema de firma digital descrito anteriormente satisface directamente este requisito: cada actualización es trazable a una versión específica de firmware, una marca de tiempo específica y un acto de autorización específico por parte de HQ, verificable por reguladores, tribunales o auditores mucho tiempo después del hecho.

---

### Referencias

[1] NIST, *FIPS 180-4: Secure Hash Standard (SHS)*, marzo 2012. Disponible en: https://csrc.nist.gov/pubs/fips/180-4/upd1/final

[2] K. Moriarty et al., *RFC 8017: PKCS #1: RSA Cryptography Specifications Version 2.2*, IETF, noviembre 2016. Disponible en: https://www.rfc-editor.org/rfc/rfc8017.html

[3] Parlamento Europeo, *Reglamento (UE) N.º 910/2014 (eIDAS)*, en vigor desde el 1 de julio de 2016. Disponible en: https://eur-lex.europa.eu/eli/reg/2014/910/oj/eng

[4] Congreso de los EE. UU., *Electronic Signatures in Global and National Commerce Act*, Ley Pública 106-229, promulgada el 30 de junio de 2000. Codificada en 15 U.S.C. § 7001. Disponible en: https://www.congress.gov/bill/106th-congress/house-bill/1714

[5] UNECE WP.29, *Reglamento ONU N.º 156: Actualización de Software y Sistema de Gestión de Actualizaciones de Software*, en vigor desde 2022. Disponible en: https://unece.org/transport/documents/2021/03/standards/un-regulation-no-156-software-update-and-software-update
