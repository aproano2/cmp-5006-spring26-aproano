# Homework 3: Web Defense & Privacy Compliance

## Documento principal de entrega
El documento principal para revision academica es [report/final_report.md](</C:/Users/pablo/Desktop/SEMESTRE12/Seguridad/cmp-5006-homework-3/report/final_report.md>). Ese archivo resume los cinco literales y apunta a las evidencias y anexos tecnicos correspondientes.

## Curso y autores
- Curso: CMP-5006 Seguridad de la Informacion
- Integrantes: Pablo Alvarado y Andres Proano
- Fecha de verificacion documental: 2026-05-05

## Resumen ejecutivo
Este repositorio contiene la entrega del Homework 3 sobre defensa web y cumplimiento de privacidad. El trabajo cubre cinco frentes: mapeo OWASP/CWE/CVE, contexto regulatorio ecuatoriano, dos retos reales de picoCTF Web Exploitation, despliegue de DVWA con WAF y un Privacy Notice para la fintech ficticia QuitoCash alineado con GDPR y LOPDP.

La documentacion fue revisada con criterio tecnico, legal y academico. La estructura final fue simplificada para eliminar archivos de seguimiento interno y dejar una ruta de lectura clara, profesional y apta para entrega.

## Objetivos
- Demostrar capacidad de analisis de vulnerabilidades usando OWASP Top 10, CWE y CVE reales.
- Explicar con precision los derechos del titular en la LOPDP y su enforcement frente al modelo europeo del GDPR.
- Evidenciar dos ejercicios practicos de explotacion web en un entorno autorizado.
- Probar una defensa compensatoria con ModSecurity frente a Command Injection en DVWA.
- Diseniar un aviso de privacidad profesional para QuitoCash con base legal, derechos y minimizacion de datos.

## Ruta recomendada de revision
1. Leer el informe final: [report/final_report.md](</C:/Users/pablo/Desktop/SEMESTRE12/Seguridad/cmp-5006-homework-3/report/final_report.md>)
2. Revisar las evidencias visuales en `evidence/`
3. Consultar los anexos de `docs/` por seccion
4. Consultar `waf/` y `docker/` para los artefactos tecnicos del laboratorio

## Estructura del repositorio

| Ruta | Contenido | Uso en la entrega |
|---|---|---|
| `report/final_report.md` | Informe final consolidado | Documento principal |
| `docs/01_owasp_cwe_cve_mapping.md` | Mapeo OWASP, CWE y CVE | Literal 1 |
| `docs/02_lopdp_ecuador_context.md` | LOPDP, ocho derechos y comparacion con GDPR | Literal 2 |
| `docs/03_picoctf_writeups.md` | Write-ups de dos retos Web Exploitation | Literal 3 |
| `docs/04_dvwa_waf_deployment.md` | Procedimiento, resultados y defensa WAF | Literal 4 |
| `docs/05_quitocash_privacy_notice.md` | Privacy Notice de QuitoCash y minimizacion | Literal 5 |
| `docs/references.md` | Referencias oficiales y fecha de consulta | Soporte |
| `evidence/` | Capturas de picoCTF, DVWA y WAF | Evidencia |
| `waf/` | Regla custom y notas del laboratorio | Evidencia tecnica |
| `docker/` | Base reproducible de DVWA local | Reproducibilidad |

## Requisitos y herramientas usadas
- Docker / Docker Compose para DVWA y MariaDB.
- DVWA (`vulnerables/web-dvwa`) como entorno vulnerable local.
- `owasp/modsecurity-crs:nginx` como proxy inverso con ModSecurity.
- Regla custom `id:1001001` para bloquear `;` y `|` en `ARGS`.
- Navegador web para picoCTF y capturas del laboratorio.
- Fuentes oficiales para verificacion documental:
  - OWASP
  - MITRE CWE
  - NVD / advisory oficial del proveedor
  - Registro Oficial / SPDP Ecuador
  - EUR-Lex / EDPB

## Reproducibilidad del laboratorio
- `docker/docker-compose.dvwa_base.yml` levanta `DVWA + MariaDB` en `localhost:8080`.
- `docker/docker-compose.dvwa_waf.yml` agrega `ModSecurity + CRS` delante de DVWA en `localhost:8081`.
- Esta separacion permite distinguir con claridad el acceso directo a la aplicacion vulnerable y el acceso protegido por el WAF.

## Tabla de entregables

| Seccion | Estado | Archivo principal | Evidencia asociada |
|---|---|---|---|
| 1. OWASP y CWE Mapping | Completo y verificado | `docs/01_owasp_cwe_cve_mapping.md` | `docs/references.md` |
| 2. Ecuadorian Context | Completo y corregido contra fuente oficial | `docs/02_lopdp_ecuador_context.md` | `docs/references.md` |
| 3. picoCTF | Completo | `docs/03_picoctf_writeups.md` | `evidence/picoctf/` |
| 4. DVWA + WAF | Completo | `docs/04_dvwa_waf_deployment.md` | `evidence/dvwa_attack/`, `evidence/waf_blocking/`, `waf/` |
| 5. Privacy Engineering Task | Completo | `docs/05_quitocash_privacy_notice.md` | `docs/references.md` |

## Metodologia por seccion

### 1. OWASP, CWE y CVE
Se eligieron tres categorias del OWASP Top 10 2021 y se verifico que el CWE seleccionado aparezca en la lista oficial mapeada por OWASP. Luego se confirmo cada CVE en NVD y, cuando existia, se contrasto con el advisory oficial del proveedor o base primaria asociada.

### 2. LOPDP y GDPR
Se reviso el texto vigente de la LOPDP, el Reglamento General, resoluciones y material institucional de la SPDP. La comparacion con GDPR se baso en EUR-Lex y material oficial del EDPB, con foco en autoridad de control, sanciones, reclamos, remedios y cooperacion transfronteriza.

### 3. picoCTF
Se resolvieron dos retos oficiales de la categoria Web Exploitation y se documentaron write-ups breves con la logica de resolucion. Las capturas incluidas muestran la flag recuperada en el flujo de entrega del reto.

### 4. DVWA y WAF
Se levanto DVWA localmente con Docker, se ejecuto Command Injection en nivel `Low` y luego se interpuso un WAF con ModSecurity. La defensa se valido con una regla que bloquea `;` y `|` en argumentos HTTP y produce `403 Forbidden`.

### 5. QuitoCash
Se redacto un Privacy Notice academico con enfoque de cumplimiento dual GDPR + LOPDP. El aviso mapea finalidades con bases legales, incorpora portabilidad y oposicion de forma expresa y documenta la clausula de decisiones automatizadas para la funcion de IA.

## Evidencias incluidas
- `evidence/picoctf/challenge_1/picoctf_webdecode_flag.png`
- `evidence/picoctf/challenge_2/picoctf_web_gauntlet_flag.png`
- `evidence/dvwa_attack/dvwa_command_injection_before_waf.png`
- `evidence/waf_blocking/dvwa_blocked_after_waf_403.png`
- `evidence/waf_blocking/modsecurity_log_block.png`

## Resumen OWASP, CWE y CVE

| Categoria OWASP | CWE validado | CVE validado | Observacion |
|---|---|---|---|
| A03:2021 Injection | CWE-89 | CVE-2025-25257 | SQL Injection no autenticada en FortiWeb |
| A01:2021 Broken Access Control | CWE-863 | CVE-2025-29927 | Bypass de autorizacion en middleware de Next.js |
| A08:2021 Software and Data Integrity Failures | CWE-502 | CVE-2025-27130 | Deserializacion insegura en Welcart e-Commerce |

## Resumen LOPDP y GDPR
- La LOPDP reconoce ocho derechos del titular en los articulos 12, 13, 14, 15, 16, 17, 19 y 20; el articulo 18 regula excepciones, no un derecho adicional.
- La SPDP ya cuenta con potestad sancionadora, tramita reclamos, puede iniciar actuaciones previas, inspecciones y auditorias, y puede ordenar medidas provisionales.
- Frente al GDPR, Ecuador tiene una sola autoridad nacional y un ecosistema sancionatorio mucho mas reciente.
- La UE opera con autoridades por Estado miembro coordinadas por el EDPB y con el mecanismo de one-stop-shop para casos transfronterizos.

## Resumen picoCTF
- Reto 1: `WebDecode`
  - Tecnica: inspeccion del DOM y decodificacion base64.
  - Flag documentada: `picoCTF{web_succ3ssfully_d3c0ded_07b91c79}`
- Reto 2: `Web Gauntlet`
  - Tecnica: SQL Injection con bypass progresivo de denylist y lectura posterior de `filter.php`.
  - Flag documentada: `picoCTF{y0u_m4d3_1t_79a0ddc6}`

## Resumen DVWA y WAF
- Antes del WAF, `127.0.0.1; whoami` devuelve `www-data` en el modulo de Command Injection de DVWA.
- Despues del WAF, el mismo patron queda bloqueado por la regla custom `id:1001001`.
- La captura posterior muestra `403 Forbidden` y el log evidencia el match sobre `ARGS:ip`.
- Control compensatorio documentado: la regla no cubre `&&`, `||`, backticks ni `$()`.

## Privacy Notice QuitoCash
- Archivo principal: `docs/05_quitocash_privacy_notice.md`
- Contiene:
  - identidad del responsable
  - finalidades y bases legales
  - destinatarios y transferencias
  - conservacion
  - portabilidad y oposicion
  - decisiones automatizadas
  - seguridad y reclamos

## Data minimization
Tres datos que QuitoCash podria querer recolectar pero no deberia recolectar:
- lista completa de contactos del telefono
- geolocalizacion GPS continua en segundo plano
- contenido de SMS, WhatsApp o redes sociales

La justificacion se documenta en `docs/05_quitocash_privacy_notice.md`.

## Referencias
- Referencias completas y verificadas: `docs/references.md`
- Fecha de consulta externa usada en la verificacion final: `2026-05-05`

## Limitaciones y supuestos
- No se alteraron imagenes ni se genero evidencia nueva.
- Las capturas de picoCTF muestran la flag recuperada en el flujo del reto, pero no incluyen un banner de confirmacion explicito; esto no invalida la evidencia, aunque una futura mejora visual podria reforzarla.
- La captura previa del ataque en DVWA evidencia la ejecucion de `whoami` mediante la salida `www-data`; el payload exacto queda explicado en el write-up y corroborado indirectamente por el bloqueo posterior y el log del WAF.
- El presente trabajo no constituye asesoria legal profesional; es una entrega academica basada en fuentes oficiales.

## Notas de reproducibilidad
1. Levantar DVWA con `docker compose -f docker/docker-compose.dvwa_base.yml up -d`.
2. Inicializar DVWA y fijar seguridad en `Low`.
3. Ejecutar el payload `127.0.0.1; whoami` en `Command Injection`.
4. Cargar ModSecurity con la regla del repositorio.
5. Repetir la prueba a traves del puerto del WAF y confirmar `403 Forbidden`.
6. Revisar el log para verificar el `id:1001001`.

## Validacion local de DVWA y WAF
Esta validacion es solo para laboratorio local. No usar objetivos externos.

### 1. Validar el compose base de DVWA
```powershell
docker compose -f docker/docker-compose.dvwa_base.yml config
docker compose -f docker/docker-compose.dvwa_base.yml up -d
docker ps -a
curl.exe -i http://localhost:8080/
docker logs dvwa_lab --tail 50
docker logs dvwa_db --tail 50
```

Resultado esperado:
- `dvwa_lab` y `dvwa_db` en estado `Up`
- `http://localhost:8080/` responde y redirige o sirve `login.php`

### 2. Preparar DVWA para la prueba
Antes de probar el ataque hay que:
- abrir `http://localhost:8080/setup.php`
- pulsar `Create / Reset Database`
- iniciar sesion con `admin / password`
- fijar `DVWA Security` en `Low`

### 3. Validar ataque directo a DVWA
Con una sesion valida de DVWA, copiar `PHPSESSID` desde el navegador y ejecutar:

```powershell
curl.exe -i -X POST "http://localhost:8080/vulnerabilities/exec/" `
  -H "Content-Type: application/x-www-form-urlencoded" `
  -b "PHPSESSID=<SESSION_ID>; security=low" `
  --data "ip=127.0.0.1;whoami&Submit=Submit"
```

Resultado esperado:
- respuesta `HTTP/1.1 200 OK`
- salida del `ping`
- aparicion de `www-data` o usuario equivalente del servidor

### 4. Levantar el WAF desde el repositorio
```powershell
docker compose -f docker/docker-compose.dvwa_base.yml -f docker/docker-compose.dvwa_waf.yml up -d
```

Comprobaciones inmediatas:
```powershell
docker ps -a
curl.exe -i http://localhost:8081/
docker logs dvwa_waf --tail 100
```

Resultado esperado:
- el contenedor `dvwa_waf` aparece en `Up`
- `localhost:8081` responde
- los logs muestran arranque correcto del proxy/WAF

### 5. Validar bloqueo a traves del WAF
Con una sesion valida de DVWA:

```powershell
curl.exe -i -X POST "http://localhost:8081/vulnerabilities/exec/" `
  -H "Content-Type: application/x-www-form-urlencoded" `
  -b "PHPSESSID=<SESSION_ID>; security=low" `
  --data "ip=127.0.0.1;whoami&Submit=Submit"
```

Resultado esperado:
- respuesta `HTTP/1.1 403 Forbidden`
- el backend DVWA no debe devolver `www-data`
- `docker logs dvwa_waf --tail 100` debe mostrar el bloqueo por la regla custom

### 6. Validar logs del WAF
```powershell
docker logs dvwa_waf 2>&1 | Select-String "1001001"
docker logs dvwa_waf 2>&1 | Select-String "ARGS:ip"
```

Resultado esperado:
- aparicion del `id "1001001"`
- coincidencia sobre `ARGS:ip`
- presencia del valor malicioso con `;` o `|`

## Declaracion etica
Todas las pruebas de explotacion documentadas en este repositorio fueron realizadas exclusivamente en entornos autorizados, locales o de laboratorio: picoCTF y DVWA desplegado en localhost. No se probaron tecnicas de ataque sobre sistemas reales, servicios de terceros ni infraestructura ajena.
