# Homework 3: Web Defense & Privacy Compliance - Informe Final

## Portada
- Curso: CMP-5006 Seguridad de la Informacion
- Deber: Homework 3 - Web Defense & Privacy Compliance
- Autores: Pablo Alvarado y Andres Proano
- Fecha: 2026-05-05

## Resumen ejecutivo
El presente informe desarrolla los cinco literales exigidos en el deber: mapeo OWASP/CWE/CVE, contexto ecuatoriano de proteccion de datos, dos retos de picoCTF Web Exploitation, despliegue de DVWA con defensa WAF y aviso de privacidad para QuitoCash. La documentacion se apoya en anexos tematicos, capturas de evidencia y referencias oficiales para mantener trazabilidad tecnica y academica.

## 1. OWASP, CWE y CVE
Se seleccionaron tres categorias del OWASP Top 10:2025 y para cada una se identifico un CWE representativo y un CVE reciente que ejemplifica la debilidad en un producto real.

| Categoria OWASP | CWE | CVE | Producto | Impacto resumido |
|---|---|---|---|---|
| A05:2025 Injection | CWE-89: Improper Neutralization of Special Elements used in an SQL Command | CVE-2025-25257 | Fortinet FortiWeb | FortiWeb presenta una SQL Injection no autenticada que permite enviar solicitudes HTTP/HTTPS manipuladas para ejecutar SQL no autorizado en el producto. El impacto es critico porque el fallo afecta a un WAF perimetral y puede exponer credenciales, configuracion y control administrativo. |
| A01:2025 Broken Access Control | CWE-863: Incorrect Authorization | CVE-2025-29927 | Next.js | La vulnerabilidad permite omitir controles de autorizacion cuando una aplicacion confia esas validaciones al middleware de Next.js y acepta solicitudes con la cabecera `x-middleware-subrequest`. El impacto es critico porque un atacante no autenticado puede alcanzar rutas protegidas y exponer o alterar datos sin credenciales validas. |
| A08:2025 Software or Data Integrity Failures | CWE-502: Deserialization of Untrusted Data | CVE-2025-27130 | Welcart e-Commerce | Welcart e-Commerce 2.11.6 y anteriores deserializa datos no confiables y permite que un atacante remoto no autenticado ejecute codigo arbitrario en sitios que usan el plugin. El impacto es alto porque compromete la integridad del servidor y puede convertir la tienda en un punto de entrada para robo de datos o persistencia. |

Anexo tematico: `docs/01_owasp_cwe_cve_mapping.md`

## 2. Contexto ecuatoriano: LOPDP y comparacion con GDPR
La Ley Organica de Proteccion de Datos Personales del Ecuador reconoce ocho derechos generales del titular. Para esta entrega se toman los articulos 12, 13, 14, 15, 16, 17, 19 y 20, mientras que el articulo 18 regula excepciones y no un derecho adicional.

Los ocho derechos son:
- derecho a la informacion
- derecho de acceso
- derecho de rectificacion y actualizacion
- derecho de eliminacion
- derecho de oposicion
- derecho a la portabilidad
- derecho a la suspension del tratamiento
- derecho a no ser objeto de decisiones basadas unica o parcialmente en valoraciones automatizadas

En Ecuador, la Superintendencia de Proteccion de Datos Personales actua como autoridad unica nacional de control. Puede recibir reclamos, realizar actuaciones previas, investigar, inspeccionar, auditar, ordenar medidas correctivas y aplicar sanciones administrativas.

Frente al GDPR, la LOPDP comparte una arquitectura similar de derechos, bases legales y responsabilidad demostrada, pero opera en un ecosistema regulatorio mas reciente. En la Union Europea, en cambio, existe una autoridad por Estado miembro coordinada por el EDPB, con mecanismos de cooperacion transfronteriza mas desarrollados y multas potencialmente mas altas conforme al articulo 83 del GDPR.

Anexo tematico: `docs/02_lopdp_ecuador_context.md`

## 3. Hands-on Exploitation and Defense: picoCTF
Se documentaron dos retos oficiales de la categoria Web Exploitation.

### 3.1 WebDecode
- Categoria: Web Exploitation
- Dificultad: Easy
- Logica empleada: inspeccion del DOM y deteccion de una cadena codificada en base64; posterior decodificacion con `atob()`.
- Flag documentada: `picoCTF{web_succ3ssfully_d3c0ded_07b91c79}`
- Evidencia: `evidence/picoctf/challenge_1/picoctf_webdecode_flag.png`

### 3.2 Web Gauntlet
- Categoria: Web Exploitation
- Dificultad: Medium
- Logica empleada: bypass progresivo de filtros de entrada para explotar SQL Injection y alcanzar la lectura de `filter.php`.
- Flag documentada: `picoCTF{y0u_m4d3_1t_79a0ddc6}`
- Evidencia: `evidence/picoctf/challenge_2/picoctf_web_gauntlet_flag.png`

Estos ejercicios muestran dos lecciones distintas: que la informacion expuesta en el cliente no esta protegida por simple codificacion, y que las denylist de palabras clave no sustituyen consultas parametrizadas ni controles seguros de validacion.

Anexo tematico: `docs/03_picoctf_writeups.md`

## 4. WAF Deployment con DVWA
El laboratorio se construyo con Docker y distingue dos rutas de acceso:
- `localhost:8080` para DVWA directo
- `localhost:8081` para DVWA detras de `owasp/modsecurity-crs:nginx`

La reproducibilidad del entorno queda resuelta con:
- `docker/docker-compose.dvwa_base.yml`
- `docker/docker-compose.dvwa_waf.yml`

La regla utilizada para el bloqueo se define en `waf/modsecurity_rules/block_command_separators.conf`:

```conf
SecRule ARGS "@rx [;|]" \
    "id:1001001,phase:2,deny,status:403,log,msg:'Bloqueo de posible separador de command injection (; o |) en ARGS'"
```

### 4.1 Antes del WAF
Con DVWA en nivel `Low`, el modulo `Command Injection` acepta el payload `127.0.0.1; whoami` y devuelve `www-data`. Esto demuestra que la aplicacion concatena entrada del usuario con comandos del sistema operativo.

Evidencia:
- `evidence/dvwa_attack/dvwa_command_injection_before_waf.png`

### 4.2 Despues del WAF
Al repetir el mismo patron a traves del puerto protegido `8081`, ModSecurity bloquea la solicitud y responde con `403 Forbidden`. El registro del WAF muestra coincidencia sobre `ARGS:ip` y activa la regla `id "1001001"`.

Evidencias:
- `evidence/waf_blocking/dvwa_blocked_after_waf_403.png`
- `evidence/waf_blocking/modsecurity_log_block.png`

### 4.3 Interpretacion tecnica
Este resultado demuestra que el WAF funciona como control compensatorio efectivo para el patron solicitado por el enunciado. Sin embargo, la regla no cubre evasiones como `&&`, `||`, backticks o `$()`, por lo que no reemplaza la correccion segura del codigo fuente.

Anexos tecnicos:
- `docs/04_dvwa_waf_deployment.md`
- `waf/notes.md`
- `docker/README.md`

## 5. Privacy Engineering Task: QuitoCash
Se redacto un aviso de privacidad academico para la fintech ficticia QuitoCash, alineado con GDPR y LOPDP. El texto incorpora identidad del responsable, categorias de datos, finalidades del tratamiento, bases legales, destinatarios, transferencias internacionales, conservacion, seguridad, mecanismo de reclamo y ejercicio de derechos.

Las bases legales se asignan por finalidad y no de forma generica: la ejecucion del contrato sustenta la apertura y operacion de la cuenta, el cumplimiento de obligaciones legales cubre verificaciones regulatorias y registros exigidos al sector financiero, el interes legitimo se utiliza para prevencion de fraude y seguridad, y el consentimiento sirve de base para analitica opcional y personalizacion no esencial.

El aviso incluye de forma expresa:
- base legal diferenciada por finalidad
- derecho a la portabilidad
- derecho de oposicion
- clausula sobre decisiones automatizadas para la funcion de IA `Spending Insights`

Tambien explica que la portabilidad y la oposicion pueden ejercerse mediante los canales de contacto del responsable, y que las decisiones automatizadas asociadas a `Spending Insights` no deben operar como unica base para efectos juridicos adversos sin posibilidad de intervencion humana, revision y objecion del titular.

Tambien se identificaron tres datos que QuitoCash podria querer recolectar pero no deberia recolectar por minimizacion:
- lista completa de contactos del telefono
- geolocalizacion GPS continua en segundo plano
- contenido de SMS, WhatsApp o redes sociales

Anexo tematico: `docs/05_quitocash_privacy_notice.md`

## Conclusiones
El trabajo integra analisis de vulnerabilidades, cumplimiento normativo, practica ofensiva controlada, defensa perimetral y privacidad por diseno. La seccion de DVWA y WAF demuestra un flujo completo de ataque y bloqueo en laboratorio local, mientras que las secciones legales y documentales completan la perspectiva de seguridad y cumplimiento exigida por el deber.

## Referencias
Las referencias oficiales y tecnicas consolidadas constan en `docs/references.md`.
