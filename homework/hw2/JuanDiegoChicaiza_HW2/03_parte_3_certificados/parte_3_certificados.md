# Parte 3: Certificados digitales y cadena de confianza

**Estudiante:** Juan Diego Chicaiza, María Emilia Granda, Sebastián Encalada
**Tema:** CSR, X.509 y trust anchors

## 1. Proceso de CSR (Certificate Signing Request)

Un **CSR** es la solicitud estructurada que AutoDrive HQ envía a una Autoridad Certificadora (CA) para que esta emita un certificado X.509 firmado.

El flujo general es:

1. HQ genera un par de claves.
2. HQ construye la solicitud CSR.
3. HQ firma la CSR con la clave privada asociada a la clave pública incluida en la solicitud.
4. La CA valida la identidad del solicitante y, si todo es correcto, emite el certificado.

## 1.1 Cuatro piezas principales de información que HQ debe enviar

De acuerdo con PKCS #10 y la práctica habitual de PKI, las cuatro piezas centrales son:

### 1. Información de identidad del sujeto

Es el **Distinguished Name (DN)** del solicitante, por ejemplo:

- `CN` (Common Name)
- `O` (Organization)
- `OU` (Organizational Unit)
- `L` (Locality)
- `ST` (State/Province)
- `C` (Country)

En otras palabras, esta parte responde a la pregunta: **¿quién dice ser AutoDrive HQ?**

### 2. La clave pública del sujeto

La CSR incluye la clave pública que la CA va a certificar. El propósito de la CA es afirmar:

> "Esta clave pública pertenece a la entidad identificada como AutoDrive HQ."

### 3. Atributos o extensiones solicitadas

La CSR puede pedir extensiones para el certificado final, por ejemplo:

- Subject Alternative Name (SAN)
- Key Usage
- Extended Key Usage
- Basic Constraints

Esto permite indicar para qué se usará el certificado, por ejemplo autenticación de servidor o firma de código.

### 4. La firma digital sobre la CSR

La CSR debe ir firmada con la clave privada correspondiente a la clave pública incluida. Esto prueba **posesión de la clave privada**. Sin esa prueba, alguien podría intentar pedir un certificado para una clave pública ajena.

## 1.2 Aclaración práctica importante

En el mundo real, la CA suele pedir evidencia adicional fuera de la CSR, por ejemplo:

- validación de dominio
- validación organizacional
- documentos legales

Sin embargo, dentro del objeto criptográfico CSR, las cuatro piezas anteriores son las fundamentales.

## 2. ¿Qué certificado raíz debe estar preinstalado en el vehículo?

El vehículo necesita confiar en el **certificado raíz que actúa como trust anchor** para validar la cadena de certificados de AutoDrive HQ.

La verificación correcta no es confiar ciegamente en el certificado de HQ como un archivo aislado. La verificación correcta es:

`Certificado de HQ -> CA intermedia(s) -> CA raíz confiable`

## 2.1 Respuesta precisa

El certificado raíz que debe estar preinstalado en la computadora del auto es:

> **el certificado raíz de la CA cuya clave pública sirve como ancla de confianza para validar la cadena X.509 del certificado de AutoDrive HQ.**

## 2.2 Dos escenarios posibles

### Caso 1: AutoDrive usa una CA pública

El vehículo debe traer instalado el certificado raíz exacto de esa PKI pública, o el conjunto mínimo de raíces que permitan validar la cadena específica usada por HQ.

### Caso 2: AutoDrive usa una PKI privada corporativa

El vehículo debe traer preinstalado el certificado autofirmado de la **AutoDrive Root CA**.

## 2.3 Por qué esto importa

Sin ese trust anchor, el auto no tiene una base segura para decidir si la clave pública presentada por HQ es legítima o si fue sustituida por un atacante. En otras palabras:

- el certificado de HQ por sí solo no crea confianza
- la confianza la crea la **cadena** que termina en una raíz previamente provisionada en fábrica

Por eso, en sistemas embebidos y automotrices, la instalación del certificado raíz en fábrica es parte crítica del modelo de seguridad.

## Referencias

1. RFC 2986, *PKCS #10: Certification Request Syntax Specification*.
2. RFC 5280, *Internet X.509 Public Key Infrastructure Certificate and CRL Profile*.
