# Parte 4: Firmas digitales

**Estudiante:** Juan Diego Chicaiza, María Emilia Granda, Sebastián Encalada 
**Tema:** Autenticación y no repudio

## 1. Flujo de creación de la firma

En un sistema real, AutoDrive HQ no debería firmar solo un nombre de archivo. Lo correcto es firmar un **manifiesto de actualización** que incluya:

- versión del firmware
- plataforma o ECU objetivo
- tamaño del firmware
- hash SHA-256 del firmware
- fecha de emisión
- fecha de expiración
- contador anti-rollback

## 1.1 ¿Qué se hashea?

El componente crítico es:

\[
H_f = \text{SHA-256}(\text{imagen del firmware})
\]

Ese hash representa de forma compacta el contenido exacto del binario. Si cambia un solo bit del firmware, el hash cambia drásticamente y deja de coincidir con el valor autorizado.

## 1.2 ¿Qué clave se usa para firmar?

La firma se genera con la **clave privada de HQ**.

La verificación se realiza con la **clave pública de HQ**, obtenida del certificado X.509 validado por el vehículo.

## 1.3 Corrección importante sobre la explicación simplificada

En muchos cursos introductorios se dice:

> "La firma digital consiste en cifrar el hash con la clave privada."

Esa frase ayuda a crear intuición, pero técnicamente es una simplificación. En una implementación moderna con RSA, el flujo real es más preciso:

1. se calcula el hash del mensaje o del manifiesto
2. ese hash se codifica según un esquema de firma, por ejemplo RSA-PSS
3. se aplica la primitiva de firma RSA con la clave privada

Así que la forma correcta de expresarlo es:

> HQ firma una representación codificada derivada del hash usando su clave privada.

## 2. No repudio

## 2.1 ¿Cómo ayuda la firma digital si AutoDrive intenta negar el envío?

Si un update defectuoso provoca un accidente, AutoDrive podría intentar afirmar que nunca autorizó exactamente esa versión. La firma digital dificulta muchísimo esa negación porque:

1. la firma valida con la clave pública certificada de AutoDrive HQ
2. el manifiesto firmado contiene el hash exacto del firmware y sus metadatos
3. un tercero independiente puede verificar la firma sin depender de la palabra de AutoDrive

Eso produce evidencia técnica de que el poseedor de la clave privada de HQ autorizó ese artefacto concreto.

## 2.2 Diferencia entre integridad y no repudio

Un checksum o hash por sí solo demuestra integridad, es decir:

> "el archivo no cambió respecto del valor esperado"

Una firma digital demuestra algo más fuerte:

> "la entidad dueña de la clave privada correspondiente autorizó este contenido exacto"

Esa diferencia es la base del no repudio.

## 2.3 Matiz legal

La criptografía aporta **no repudio técnico**, pero para que exista un no repudio sólido también desde el punto de vista legal y forense hacen falta controles operativos:

- custodia estricta de la clave privada
- uso de HSM
- registros de auditoría
- trazabilidad de aprobación de releases
- sellos de tiempo
- políticas de revocación y rotación de claves

Por tanto, la mejor formulación es:

> La firma digital proporciona evidencia técnica fuerte de que AutoDrive autorizó una versión específica del firmware y, combinada con controles operativos y registros de auditoría, sustenta el no repudio legal.

## Referencias

1. RFC 8017, *PKCS #1 v2.2: RSA Cryptography Specifications*.
2. NIST FIPS 205, *Stateless Hash-Based Digital Signature Standard*.
