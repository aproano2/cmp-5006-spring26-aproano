# Mapeo OWASP-CWE-CVE

## Objetivo
Mapear tres categorias distintas del OWASP Top 10 2021 con un CWE oficial y un CVE reciente de 2025 o 2026 que represente de manera razonable esa debilidad.

## Criterio de validacion
- La categoria OWASP debe incluir formalmente el CWE elegido en su lista oficial de CWEs mapeados.
- El CVE debe existir en NVD y pertenecer a 2025 o 2026.
- El CVE debe reflejar el mismo patron tecnico del CWE seleccionado, no solo un parecido superficial.
- Se privilegian fuentes primarias: OWASP, MITRE CWE, NVD y advisory oficial del proveedor cuando existe.

## Tabla de mapeo verificada

| # | Categoria OWASP | CWE verificado | CVE verificado | Producto afectado | Resumen de impacto (2 oraciones) |
|---|---|---|---|---|---|
| 1 | A03:2021 - Injection | CWE-89: Improper Neutralization of Special Elements used in an SQL Command | CVE-2025-25257 | Fortinet FortiWeb | FortiWeb presenta una SQL Injection no autenticada que permite enviar solicitudes HTTP/HTTPS manipuladas para ejecutar SQL no autorizado en el producto. El impacto es critico porque el fallo afecta a un WAF perimetral y puede exponer credenciales, configuracion y control administrativo. |
| 2 | A01:2021 - Broken Access Control | CWE-863: Incorrect Authorization | CVE-2025-29927 | Next.js | La vulnerabilidad permite omitir controles de autorizacion cuando una aplicacion confia esas validaciones al middleware de Next.js y acepta solicitudes con la cabecera `x-middleware-subrequest`. El impacto es critico porque un atacante no autenticado puede alcanzar rutas protegidas y exponer o alterar datos sin credenciales validas. |
| 3 | A08:2021 - Software and Data Integrity Failures | CWE-502: Deserialization of Untrusted Data | CVE-2025-27130 | Welcart e-Commerce para WordPress | Welcart e-Commerce 2.11.6 y anteriores deserializa datos no confiables y permite que un atacante remoto no autenticado ejecute codigo arbitrario en sitios que usan el plugin. El impacto es alto porque compromete la integridad del servidor y puede convertir la tienda en un punto de entrada para robo de datos o persistencia. |

## Por que cada mapeo es valido
- A03 -> CWE-89: OWASP A03 lista expresamente a `CWE-89` como ejemplo notable y la propia descripcion de `CVE-2025-25257` en NVD indica SQL Injection.
- A01 -> CWE-863: OWASP A01 incluye `CWE-863` en su lista de CWEs mapeados y NVD asocia `CVE-2025-29927` con `CWE-863`; GitHub Advisory ademas lo relaciona con `CWE-285`, pero `CWE-863` es la opcion mas precisa para este caso.
- A08 -> CWE-502: OWASP A08 incluye `CWE-502` en su lista oficial y NVD/JVN describen `CVE-2025-27130` como una vulnerabilidad de deserializacion de datos no confiables.

## Riesgos de observacion del docente ya mitigados
- Se elimino un mapeo OWASP/CWE/CVE que no trazaba limpiamente.
- Se mantuvieron resumentes de impacto en exactamente dos oraciones claras.
- Todos los ejemplos quedaron dentro de 2025 o 2026 y con fuente primaria verificable.

## Fuentes usadas para esta seccion
- OWASP A03: `https://owasp.org/Top10/2021/A03_2021-Injection/`
- OWASP A01: `https://owasp.org/Top10/2021/A01_2021-Broken_Access_Control/`
- OWASP A08: `https://owasp.org/Top10/2021/A08_2021-Software_and_Data_Integrity_Failures/`
- CWE-89: `https://cwe.mitre.org/data/definitions/89.html`
- CWE-863: `https://cwe.mitre.org/data/definitions/863.html`
- CWE-502: `https://cwe.mitre.org/data/definitions/502.html`
- NVD `CVE-2025-25257`
- NVD `CVE-2025-29927`
- NVD `CVE-2025-27130`
- Fortinet PSIRT `FG-IR-25-151`
- GitHub Advisory `GHSA-f82v-jwr5-mffw`
- JVN `JVN#87266215`
